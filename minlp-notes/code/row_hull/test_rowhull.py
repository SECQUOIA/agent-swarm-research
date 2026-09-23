"""Targeted checks of the row-hull code against brute-force vertex enumeration."""
import itertools
import sys
from pathlib import Path

import numpy as np
import gurobipy as gp
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rowhull.rows import normalize_row
from rowhull.pricing import price
from rowhull.separate import RowSeparator
from rowhull.closedform import residual_bounds


def test_pricing_downward_endpoint_jump_after_inverse_rounding():
    """A fixed lower endpoint has zero gap, independently of the gap oracle.

    With these floats the inverse of z=width is lo+one ulp. Evaluating a
    discontinuous f there used to give a false unit gap and an invalid cut.
    """
    lo, hi, a = 0.1, 1.3, -0.1
    row = normalize_row(
        [("x", a, lo, hi, "t", lambda v: np.where(v <= lo, 0.0, 1.0))],
        "==", a * lo,
    )
    assert row.B == row.items[0].width
    assert row.items[0].gap(np.array([row.B]))[0] == 0.0
    lower, _ = price(row, np.zeros(1), np.ones(1))
    assert lower == 0.0
    assert RowSeparator(row).separate(np.array([row.B]), {0: 0.0}) is None
    # No tolerance snapping: arbitrarily near interior points retain the jump.
    interior = np.nextafter(row.B, 0.0)
    assert row.items[0].gap(np.array([interior]))[0] > 0.99


def random_row(rng, n, equal=False, sense="==", integer=False):
    entries = []
    for i in range(n):
        lo = float(rng.uniform(-1, 1)); hi = lo + (1.0 if equal else float(rng.integers(1, 6) if integer else rng.uniform(0.5, 3)))
        a = 1.0 if equal else float(rng.choice([-1, 1])) * (1.0 if integer else float(rng.uniform(0.5, 2)))
        kind = rng.integers(0, 3)
        q, s = float(rng.uniform(0.5, 2)), float(rng.uniform(-1, 1))
        if kind == 0:
            f = lambda v, q=q, s=s: -q * v ** 2 + s * v
        elif kind == 1:
            f = lambda v, q=q, lo=lo: q * np.sqrt(np.maximum(v - lo, 0.0))
        else:
            f = None                                     # linear item
        entries.append((f"x{i}", a, lo, hi, f"w{i}" if f else None, f))
    const = sum(a * (lo if a > 0 else hi) for _, a, lo, hi, _, _ in entries)
    total = sum(abs(a) * (hi - lo) for _, a, lo, hi, _, _ in entries)
    frac = rng.uniform(0.2, 0.8)
    B = total * frac
    if integer or equal:
        B = np.floor(B) + float(rng.choice([0.25, 0.5, 0.7]))
    return normalize_row(entries, sense, const + B)


def vertices(row):
    n, B, w = row.n, row.B, row.widths
    out = {}
    for mask in range(1 << n):
        tot = sum(w[i] for i in range(n) if mask >> i & 1)
        for j in range(n):
            if mask >> j & 1:
                continue
            r = B - tot
            if -1e-9 <= r <= w[j] + 1e-9:
                r = min(max(r, 0.0), w[j])
                v = np.array([w[i] if mask >> i & 1 else 0.0 for i in range(n)]); v[j] = r
                g = np.zeros(n); g[j] = row.items[j].gap(np.array([r]))[0]
                out[tuple(np.round(v, 10))] = (v, g)
    return list(out.values())


def brute_membership(row, V, z, tp):
    """min s: point in hull with gaps relaxed by rho*s."""
    m = gp.Model(); m.Params.OutputFlag = 0
    lam = m.addVars(len(V), lb=0.0); s = m.addVar(lb=0.0, obj=1.0)
    m.addConstr(lam.sum() == 1)
    for k in range(row.n):
        m.addConstr(gp.quicksum(lam[q] * V[q][0][k] for q in range(len(V))) == z[k])
    for k in row.concave:
        m.addConstr(gp.quicksum(lam[q] * V[q][1][k] for q in range(len(V))) - row.items[k].rho * s <= tp[k])
    m.optimize()
    return m.ObjVal if m.Status == 2 else None


def random_point(rng, V, row):
    lam = rng.dirichlet(np.ones(len(V)) * 0.3)
    z = sum(l * v for l, (v, g) in zip(lam, V))
    hull_tp = sum(l * g for l, (v, g) in zip(lam, V))
    shrink = rng.uniform(0.0, 1.2)
    return z, {k: shrink * hull_tp[k] for k in row.concave}


@pytest.mark.parametrize("seed", range(12))
@pytest.mark.parametrize("sense", ["==", "<=", ">="])
def test_separation_matches_bruteforce(seed, sense):
    rng = np.random.default_rng(seed)
    row = None
    while row is None:
        row = random_row(rng, int(rng.integers(3, 7)), sense=sense, integer=bool(seed % 2))
    V = vertices(row)
    sep = RowSeparator(row)
    for _ in range(6):
        z, tp = random_point(rng, V, row)
        s_star = brute_membership(row, V, z, tp)
        cut = sep.separate(z, tp, tol=1e-7)
        if s_star is None:
            continue
        if s_star > 1e-5:
            assert cut is not None and abs(cut["viol"] - s_star) <= 1e-5 * max(1, s_star)
        else:
            assert cut is None or cut["viol"] <= 1e-5
        if cut is not None:                       # validity at every vertex
            for v, g in V:
                assert cut["omega"] @ g - cut["pi"] @ v - cut["pi0"] >= -1e-7


@pytest.mark.parametrize("seed", range(10))
def test_pricing_lower_bound(seed):
    rng = np.random.default_rng(100 + seed)
    row = None
    while row is None:
        row = random_row(rng, 7)
    V = vertices(row)
    pi = rng.normal(size=row.n); omega = np.abs(rng.normal(size=row.n))
    exact = min(omega @ g - pi @ v for v, g in V)
    lower, cols = price(row, pi, omega, kmax=4000)
    assert abs(lower - exact) <= 1e-8 * max(1, abs(exact))
    lower2, _ = price(row, pi, omega, kmax=8)      # heavy merging: still a lower bound
    assert lower2 <= exact + 1e-9
    assert min(c[3] for c in cols) >= exact - 1e-9


@pytest.mark.parametrize("seed", range(10))
def test_equal_width_closed_form_is_hull(seed):
    rng = np.random.default_rng(200 + seed)
    row = None
    while row is None:
        row = random_row(rng, int(rng.integers(3, 7)), equal=True)
    V = vertices(row)
    rb = residual_bounds(row)
    assert rb is not None
    w = row.widths
    for _ in range(20):
        z, tp = random_point(rng, V, row)
        s_star = brute_membership(row, V, z, tp)
        lhs = 0.0
        for k, it in enumerate(row.items):
            a, b = rb[k]
            assert abs(a - b) < 1e-9
            d = it.gap(np.array([a]))[0]
            terms = [z[k] / a, (w[k] - z[k]) / (w[k] - b)]
            if it.f is not None and d > 1e-12:
                terms.append(tp[k] / d)
            lhs += min(terms)
        if s_star > 1e-6:
            assert lhs < 1 - 1e-9
        elif lhs < 1 - 1e-6:
            raise AssertionError("closed form cuts off a hull point")


@pytest.mark.parametrize("seed", range(10))
def test_closed_form_valid_general_widths(seed):
    rng = np.random.default_rng(300 + seed)
    row = None
    while row is None:
        row = random_row(rng, 6, integer=bool(seed % 2))
    rb = residual_bounds(row)
    if rb is None:
        pytest.skip("degenerate vertex")
    w = row.widths
    for v, g in vertices(row):
        lhs = 0.0
        for k, it in enumerate(row.items):
            if rb[k] is None:
                continue
            a, b = rb[k]
            d = min(it.gap(np.array([a]))[0], it.gap(np.array([b]))[0])
            terms = [v[k] / a, (w[k] - v[k]) / (w[k] - b)]
            if it.f is not None and d > 1e-12:
                terms.append(g[k] / d)
            lhs += min(terms)
        assert lhs >= 1 - 1e-7


def _support_check(n, k, r, w, delta, rng, indicators):
    """min of a random linear objective over the extended form (EF) vs. over the generating points."""
    import itertools
    d = k * w + r
    c = rng.normal(size=n); e = rng.normal(size=n); om = rng.uniform(0, 1, n)
    # generating points
    best = np.inf
    for S in itertools.combinations(range(n), k):
        for j in set(range(n)) - set(S):
            base = sum(c[i] * w for i in S) + c[j] * r + om[j] * delta[j]
            if indicators:   # y_i = 1 forced on S and j, free elsewhere
                base += sum(e[i] for i in S) + e[j] + sum(min(e[i], 0.0) for i in range(n) if i not in S and i != j)
            best = min(best, base)
    m = gp.Model(); m.Params.OutputFlag = 0
    x = m.addVars(n, lb=0, ub=w); tau = m.addVars(n, lb=0); ze = m.addVars(n, lb=0)
    y = m.addVars(n, lb=0, ub=1) if indicators else None
    m.addConstr(x.sum() == d); m.addConstr(ze.sum() == 1)
    for i in range(n):
        m.addConstr(r * ze[i] <= x[i])
        m.addConstr((w - r) * ze[i] <= (w * y[i] if indicators else w) - x[i])
        m.addConstr(delta[i] * ze[i] <= tau[i])
    m.setObjective(gp.quicksum(c[i] * x[i] + om[i] * tau[i] + (e[i] * y[i] if indicators else 0) for i in range(n)))
    m.optimize()
    return best, m.ObjVal


@pytest.mark.parametrize("seed", range(20))
@pytest.mark.parametrize("indicators", [False, True])
def test_equal_width_support_functions(seed, indicators):
    rng = np.random.default_rng(400 + seed)
    n = int(rng.integers(3, 7)); k = int(rng.integers(1, n)); k = min(k, n - 1)
    w = float(rng.uniform(0.5, 3)); r = float(rng.uniform(0.1, 0.9)) * w
    delta = rng.uniform(0.0, 1.0, n) * (rng.random(n) > 0.2)      # some items without a concave term
    best, ef = _support_check(n, k, r, w, delta, rng, indicators)
    assert abs(best - ef) <= 1e-7 * max(1, abs(best))


@pytest.mark.parametrize("seed", range(15))
@pytest.mark.parametrize("sense", ["<=", ">="])
def test_equal_width_inequality_rows(seed, sense):
    """Support functions of the extended rows of Theorem 2(b) against vertex enumeration (with slack item)."""
    from rowhull.closedform import equal_width_inequality_rows
    rng = np.random.default_rng(500 + seed)
    row = None
    while row is None or row.slack is None:
        row = random_row(rng, int(rng.integers(3, 7)), equal=True, sense=sense)
    out = equal_width_inequality_rows(row, "t")
    if out is None:
        pytest.skip("no concave gain")
    V = vertices(row)
    m = gp.Model(); m.Params.OutputFlag = 0
    names = [it.var for it in row.items if it.var is not None]
    x = {nm: m.addVar(lb=it.lo, ub=it.hi) for nm, it in zip(names, row.items)}
    tv = {next(iter(it.tvar)): m.addVar(lb=-gp.GRB.INFINITY) for it in row.items if it.f is not None}
    allv = {**x, **tv, **{k: m.addVar(lb=lb, ub=ub) for k, (lb, ub, _t) in out[0].items()}}
    for rowd, sn, rhs in out[1]:
        lhs = gp.quicksum(c * allv[k] for k, c in rowd.items())
        m.addConstr(lhs <= rhs if sn == "<=" else lhs >= rhs if sn == ">=" else lhs == rhs)
    # the row itself and the chords
    zsum = gp.quicksum(it.a * (x[it.var] - it.lo) if it.a > 0 else (-it.a) * (it.hi - x[it.var])
                       for it in row.items if it.var is not None)
    m.addConstr(zsum <= row.B0 if sense == "<=" else zsum >= row.B0)
    for it in row.items:
        if it.f is not None:
            m.addConstr(tv[next(iter(it.tvar))] >= it.chord[0] + it.chord[1] * x[it.var])
    for _ in range(5):
        c = rng.normal(size=row.n); om = rng.uniform(0, 1, row.n)
        best = np.inf
        for v, g in V:
            val = 0.0
            for k, it in enumerate(row.items):
                if it.var is None:
                    continue
                xv = it.v_of_z(v[k])
                val += c[k] * xv
                if it.f is not None:
                    val += om[k] * (g[k] + it.chord[0] + it.chord[1] * xv)
            best = min(best, val)
        m.setObjective(gp.quicksum(c[k] * x[it.var] + (om[k] * tv[next(iter(it.tvar))] if it.f is not None else 0)
                                   for k, it in enumerate(row.items) if it.var is not None))
        m.optimize()
        assert abs(m.ObjVal - best) <= 1e-7 * max(1, abs(best))


@pytest.mark.parametrize("seed", range(40))
@pytest.mark.parametrize("decimals", [1, 2])
def test_pricing_with_coinciding_sums(seed, decimals):
    """Regression (independent code review): widths with few decimals give subset sums that agree
    only up to rounding; the state with the largest profit must survive."""
    rng = np.random.default_rng(900 + seed)
    n = 10
    entries = []
    for i in range(n):
        wdt = round(float(rng.uniform(1, 6)), decimals)
        q = float(rng.uniform(0.5, 2))
        entries.append((f"x{i}", 1.0, 0.0, wdt, f"w{i}", lambda v, q=q: -q * v ** 2))
    B = round(float(rng.uniform(0.3, 0.7)) * sum(e[3] for e in entries), decimals) + 0.013
    row = normalize_row(entries, "==", B)
    V = vertices(row)
    for _ in range(5):
        pi = rng.normal(size=row.n); omega = np.abs(rng.normal(size=row.n))
        exact = min(omega @ g - pi @ v for v, g in V)
        for kmax in (4000, 30):
            lower, _ = price(row, pi, omega, kmax=kmax)
            assert lower <= exact + 1e-8 * max(1, abs(exact))
        lower, _ = price(row, pi, omega, kmax=4000)
        assert abs(lower - exact) <= 1e-7 * max(1, abs(exact))
