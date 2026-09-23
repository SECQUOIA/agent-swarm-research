"""Author verification of reduced-profile circuits, branches, and recovery.

No repository implementation is imported. Exact Fraction/SymPy calculations
check certificates and recovered state flows. The independently assembled
state-arc LP is only a numerical membership cross-check, with statuses 0/2
required explicitly. This script is not a proof of the parameter theorems.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import math
import random

import numpy as np
import sympy as S
from scipy.optimize import linprog


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def normals(m, full=False):
    positive = {tuple(a) for a in product((0, 1), repeat=m) if any(a)}
    negative = positive if full else {(1,)*m} | {
        tuple(int(j == k) for j in range(m)) for k in range(m)}
    return sorted(positive | {tuple(-x for x in a) for a in negative})


@lru_cache(None)
def library(m, full=False):
    ns = normals(m, full)
    circuits, bases = [], []
    for size in range(2, m+2):
        for ix in combinations(range(len(ns)), size):
            kernel = S.Matrix([ns[i] for i in ix]).T.nullspace()
            if len(kernel) != 1:
                continue
            v = kernel[0]
            if all(x < 0 for x in v):
                v = -v
            if not all(x > 0 for x in v):
                continue
            den = math.lcm(*(int(x.q) for x in v))
            w = [int(x*den) for x in v]
            g = math.gcd(*w)
            circuits.append((ix, tuple(x//g for x in w)))
    if not full:
        for ix in combinations(range(len(ns)), m):
            b = S.Matrix([ns[i] for i in ix])
            if b.det():
                inv = b.inv()
                bases.append((ix, [[F(x) for x in inv.row(j)] for j in range(m)]))
    return ns, circuits, bases


def profile_rows(x, lam, obs, L):
    m = len(lam)-1
    unit = lambda j, sign=1: tuple(sign*int(k == j-1) for k in range(m))
    rows = []
    add = lambda a, b: rows.append((tuple(a), F(b)))
    total = 1-x[-1]
    add((1,)*m, total)
    add((-1,)*m, lam[0]-total)
    for j in range(1, m+1):
        add(unit(j), lam[j]); add(unit(j, -1), 0)
        if (2*L, j) in obs:
            w = lam[j]-obs[2*L, j]
            add(unit(j), w); add(unit(j, -1), -w)
    for i in range(L):
        A, B, T = set(), set(), set()
        rhs = x[2*i]
        for j in range(1, m+1):
            a, b = obs.get((2*i, j)), obs.get((2*i+1, j))
            if a is not None and b is not None:
                T.add(j); rhs -= a
                add(unit(j), a+b); add(unit(j, -1), -a-b)
            elif a is not None:
                A.add(j); rhs -= a; add(unit(j, -1), -a)
            elif b is not None:
                B.add(j); rhs += b; add(unit(j, -1), -b)
        add([int(j in B) for j in range(1, m+1)], rhs)
        add([int(j in A | T) for j in range(1, m+1)], total-rhs)
    return rows


def recover(x, lam, obs, L):
    m = len(lam)-1
    ns, circuits, bases = library(m)
    rows = profile_rows(x, lam, obs, L)
    if any(v < 0 for v in obs.values()) or any(not any(a) and b < 0 for a, b in rows):
        return None
    bounds = {a: min(b for aa, b in rows if aa == a) for a in set(a for a, b in rows) if any(a)}
    for ix, weight in circuits:
        if all(ns[k] in bounds for k in ix) and sum(w* bounds[ns[k]] for k, w in zip(ix, weight)) < 0:
            return None
    candidate = None
    if m == 2:
        l1, l2, ls = (-bounds[(-1, 0)], -bounds[(0, -1)], -bounds[(-1, -1)])
        u1, u2, us = (bounds[(1, 0)], bounds[(0, 1)], bounds[(1, 1)])
        assert l1 <= u1 and l2 <= u2 and ls <= us and l1+l2 <= us and ls <= u1+u2
        total = max(ls, l1+l2)
        a = max(l1, total-u2)
        candidate = [a, total-a]
    else:
        for ix, inverse in bases:
            if not all(ns[k] in bounds for k in ix):
                continue
            trial = [dot(row, [bounds[ns[k]] for k in ix]) for row in inverse]
            if all(dot(a, trial) <= b for a, b in bounds.items()):
                candidate = trial
                break
    assert candidate is not None
    assert all(dot(a, candidate) <= b for a, b in rows)
    w = [1-x[-1]-sum(candidate)] + candidate
    flows = [[F(0)]*(2*L+1) for _ in lam]
    for j in range(m+1):
        flows[j][-1] = lam[j]-w[j]
    for i in range(L):
        unknown = []
        for j in range(m+1):
            if (2*i, j) in obs:
                flows[j][2*i] = obs[2*i, j]
            elif (2*i+1, j) in obs:
                flows[j][2*i] = w[j]-obs[2*i+1, j]
            else:
                unknown.append(j)
        remaining = x[2*i]-sum(f[2*i] for f in flows)
        for j in unknown:
            flows[j][2*i] = min(w[j], remaining)
            remaining -= flows[j][2*i]
        assert remaining == 0
        for j in range(m+1):
            flows[j][2*i+1] = w[j]-flows[j][2*i]
    check_flows(x, lam, obs, flows, L)
    return flows


def check_flows(x, lam, obs, f, L):
    for j in range(len(lam)):
        assert all(0 <= val <= lam[j] for val in f[j])
        for i in range(L):
            assert f[j][2*i]+f[j][2*i+1]+f[j][-1] == lam[j]
    assert [sum(row[e] for row in f) for e in range(2*L+1)] == x
    assert all(f[j][e] == val for (e, j), val in obs.items())


def arc_lp(x, lam, obs, L):
    arcs = [(i, i+1) for i in range(L) for _ in range(2)] + [(0, L)]
    E, d = len(arcs), len(lam)
    rows, rhs = [], []
    for j in range(d):
        for node in range(L+1):
            row = [0]*(d*E)
            for e, (a, b) in enumerate(arcs):
                row[j*E+e] = int(b == node)-int(a == node)
            rows.append(row)
            rhs.append(float(lam[j]*(int(node == L)-int(node == 0))))
    for e in range(E):
        row = [0]*(d*E)
        for j in range(d): row[j*E+e] = 1
        rows.append(row); rhs.append(float(x[e]))
    for (e, j), value in obs.items():
        row = [0]*(d*E); row[j*E+e] = 1
        rows.append(row); rhs.append(float(value))
    result = linprog(np.zeros(d*E), A_eq=rows, b_eq=rhs,
                     bounds=[(0, float(lam[j])) for j in range(d) for _ in arcs], method='highs')
    assert result.status in (0, 2), (result.status, result.message)
    return result.status == 0


def branches(m):
    """All affine row branches for all observation categories at once."""
    symbols = S.symbols('xh ' + ' '.join(f'x{i}' for i in range(4**m)))
    xh, xs = symbols[0], symbols[1:]
    rows = []
    unit = lambda j, s=1: tuple(s*int(k == j) for k in range(m))
    add = lambda a, expr: rows.append((tuple(a), S.expand(expr)))
    add((1,)*m, -xh); add((-1,)*m, xh)
    for j in range(m):
        h = S.Symbol(f'h{j}')
        add(unit(j), 0); add(unit(j, -1), 0)
        add(unit(j), -h); add(unit(j, -1), h)
    for i, cat in enumerate(product('ABTU', repeat=m)):
        R = xs[i]
        for j, kind in enumerate(cat):
            a, b = S.symbols(f'a{i}_{j} b{i}_{j}')
            if kind in 'AT': R -= a
            if kind == 'B': R += b
            if kind == 'A': add(unit(j, -1), -a)
            if kind == 'B': add(unit(j, -1), -b)
            if kind == 'T': add(unit(j), a+b); add(unit(j, -1), -a-b)
        add([int(c == 'B') for c in cat], R)
        add([int(c in 'AT') for c in cat], -xh-R)
    ns, cs, _ = library(m)
    count = 0
    if m == 3:
        groups = {normal: [expr for a, expr in rows if a == normal] for normal in ns}
        coefficient_rows = {a: [expr.as_coefficients_dict() for expr in branches]
                            for a, branches in groups.items()}
        coordinates = set().union(*(expr.free_symbols for _, expr in rows))
        repaired = 0
        for ix, weights in cs:
            for coordinate in coordinates:
                low = sum(weight*min(row.get(coordinate, 0) for row in coefficient_rows[ns[k]])
                          for k, weight in zip(ix, weights))
                high = sum(weight*max(row.get(coordinate, 0) for row in coefficient_rows[ns[k]])
                           for k, weight in zip(ix, weights))
                limit = 2 if coordinate == xh else 1
                assert -limit <= low <= high <= limit, (coordinate, low, high)
                count += 1
            for sign in (-1, 1):
                selected_groups = []
                extreme = 0
                for k, weight in zip(ix, weights):
                    extremum = (min if sign < 0 else max)(expr.coeff(xh) for expr in groups[ns[k]])
                    extreme += weight*extremum
                    selected_groups.append([expr for expr in groups[ns[k]] if expr.coeff(xh) == extremum])
                if extreme != 2*sign:
                    continue
                for selected in product(*selected_groups):
                    expr = S.expand(sum(w*rhs for w, rhs in zip(weights, selected)))
                    chosen = next(i for i, x in enumerate(xs) if expr.coeff(x) == sign)
                    repair = S.expand(expr-sign*(xs[chosen]+S.Symbol(f'xb{chosen}')+xh))
                    assert all(abs(value) <= 1 for value in repair.as_coefficients_dict().values()), repair
                    repaired += 1
        assert repaired > 0
        return dict(coordinate_extrema_checks=count, repaired_extreme_branches=repaired)
    for ix, weights in cs:
        for selected in product(*[[rhs for normal, rhs in rows if normal == ns[k]] for k in ix]):
            expr = S.expand(sum(w*rhs for w, rhs in zip(weights, selected)))
            assert all(abs(value) <= 1 for value in expr.as_coefficients_dict().values()), expr
            count += 1
    for normal, expr in rows:
        if not any(normal):
            assert all(abs(value) <= 1 for value in expr.as_coefficients_dict().values())
    return count


def main():
    counts = {}
    for full, expected in ((False, [1, 5, 16]), (True, [1, 5, 41])):
        records = []
        for m, want in enumerate(expected, 1):
            ns, cs, bs = library(m, full)
            assert len(cs) == want
            records.append(dict(dimension=m, normals=len(ns), circuits=len(cs),
                                maximum_weight=max(max(w) for _, w in cs), bases=len(bs)))
        counts['unreduced' if full else 'reduced'] = records
    counts['exact_affine_branches'] = {m: branches(m) for m in (1, 2, 3)}
    rng = random.Random(57025)
    checks = dict(cases=0, exact_recoveries=0, exact_rejections=0,
                  numerical_feasible=0, numerical_infeasible=0, zero_weight_cases=0)
    for m, L, trial in product((1, 2, 3), (1, 2, 4), range(24)):
        raw = [rng.randrange(4) for _ in range(m+1)]
        if not any(raw): raw[0] = 1
        lam = [F(a, sum(raw)) for a in raw]
        w = [v*F(rng.randrange(5), 4) for v in lam]
        original = [[F(0)]*(2*L+1) for _ in lam]
        for j in range(m+1):
            original[j][-1] = lam[j]-w[j]
            for i in range(L):
                original[j][2*i] = w[j]*F(rng.randrange(5), 4)
                original[j][2*i+1] = w[j]-original[j][2*i]
        x = [sum(f[e] for f in original) for e in range(2*L+1)]
        obs = {(e, j): original[j][e] for e in range(2*L+1) for j in range(1, m+1)
               if rng.randrange(3)}
        if trial % 2 and obs:
            key = rng.choice(list(obs)); obs[key] += rng.choice((-1, 1))*F(1, 20)
        f = recover(x, lam, obs, L)
        numeric = arc_lp(x, lam, obs, L)
        assert numeric == (f is not None), (m, L, trial)
        checks['cases'] += 1
        checks['zero_weight_cases'] += int(any(v == 0 for v in lam))
        checks['exact_recoveries' if f is not None else 'exact_rejections'] += 1
        checks['numerical_feasible' if numeric else 'numerical_infeasible'] += 1
    counts['membership_and_recovery'] = checks
    repair_queries = []
    for sign in (-1, 1):
        L = 3
        if sign == -1:
            lam = [F(0)] + [F(1, 3)]*3
            x = [F(2, 5), F(1, 10)]*3+[F(1, 2)]
            obs = {(2*i, i+1): F(0) for i in range(3)}
            violation = 2*(1-x[-1])-sum(x[::2][:-1])+sum(obs.values())+lam[0]
            expected = -F(1, 5)
        else:
            lam = [F(1, 4)]*4
            x = [F(1, 20), F(9, 20)]*3+[F(1, 2)]
            obs = {(2*i+1, j): F(1, 20) for i, pair in enumerate(((1, 2), (1, 3), (2, 3))) for j in pair}
            violation = sum(x[::2][:-1])+sum(obs.values())+2*(lam[0]-(1-x[-1]))
            expected = -F(1, 20)
        assert violation == expected
        assert all(max(0, x[e]+lam[j]-1) <= value <= min(x[e], lam[j]) for (e, j), value in obs.items())
        assert recover(x, lam, obs, L) is None
        assert not arc_lp(x, lam, obs, L)
        # Adding/subtracting the selected gadget equation changes no value.
        assert violation-sign*(x[0]+x[1]+x[-1]-1) == violation
        repair_queries.append(dict(bypass_coefficient=2*sign, exact_violation=str(violation),
                                   numerical_lp_status=2, mccormick_pass=True))
    counts['isolated_bypass_repair_queries'] = repair_queries
    merger_checks = 0
    for a, trial in product((1, 2, 3), range(4)):
        m, L = 6, 2+trial % 2
        labels = [2, 4, 6][:a]
        raw = [rng.randrange(4) for _ in range(m+1)]
        if not any(raw): raw[0] = 1
        lam = [F(value, sum(raw)) for value in raw]
        w = [value*F(rng.randrange(5), 4) for value in lam]
        original = [[F(0)]*(2*L+1) for _ in lam]
        for j in range(m+1):
            original[j][-1] = lam[j]-w[j]
            for i in range(L):
                original[j][2*i] = w[j]*F(rng.randrange(5), 4)
                original[j][2*i+1] = w[j]-original[j][2*i]
        x = [sum(f[e] for f in original) for e in range(2*L+1)]
        obs = {(e, j): original[j][e] for j in labels for e in range(2*L+1)
               if e == 2*L or rng.randrange(2)}
        reduced_lam = [sum(lam[j] for j in range(m+1) if j not in labels)] + [lam[j] for j in labels]
        reduced_obs = {(e, labels.index(j)+1): value for (e, j), value in obs.items()}
        reduced = recover(x, reduced_lam, reduced_obs, L)
        assert reduced is not None
        lifted = [reduced[labels.index(j)+1] if j in labels else
                  [value*lam[j]/reduced_lam[0] if reduced_lam[0] else F(0) for value in reduced[0]]
                  for j in range(m+1)]
        check_flows(x, lam, obs, lifted, L)
        merger_checks += 1
    counts['exact_observed_label_merger_checks'] = merger_checks
    counts['status'] = 'PASS'
    Path(__file__).with_suffix('.json').write_text(json.dumps(counts, indent=2)+'\n')
    print(json.dumps(counts, indent=2))


if __name__ == '__main__':
    main()
