"""waterno2_T model: exact OSIL data as polynomial rows, plus period partition.

Rows are stored as polynomials: dict {monomial: coef_str}, where a monomial is
a sorted tuple of variable indices with repetition (() = constant term).
All coefficients stay decimal strings (convert with Fraction or mpmath).

The OSIL reader is the independent verifier's `osilx.py` (keeps decimal
strings exactly; records any `constant` attributes).
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys
import collections
from fractions import Fraction

sys.path.insert(0, _RESEARCH + "/reviews/"
                   "open-instances-verification")
import osilx  # noqa: E402

OSIL = _os.path.expanduser("~/.cache/minlplib/minlplib/osil/waterno2_{:02d}.osil")


def _poly_of_tree(t):
    """Nonlinear trees in waterno2 are only power(var, 3); return monomial dict."""
    if t[0] == "power":
        v, n = t[1], t[2]
        assert v[0] == "var" and n[0] == "num", t
        k = int(Fraction(n[1]))
        assert Fraction(n[1]) == k and k >= 2
        return {(v[1],) * k: v[2]}
    raise NotImplementedError(t)


def load(T):
    m = osilx.read(OSIL.format(T))
    assert m["obj"]["constant"] == "0" and not m["obj"]["quad"] and m["obj"]["nl"] is None
    assert m["obj"]["sense"] == "min"
    rows = []
    for c in m["cons"]:
        assert c["constant"] == "0"
        p = {}
        for j, a in c["lin"].items():
            p[(j,)] = a
        for i, j, a in c["quad"]:
            key = tuple(sorted((i, j)))
            assert key not in p
            p[key] = a
        if c["nl"] is not None:
            for key, a in _poly_of_tree(c["nl"]).items():
                assert key not in p
                p[key] = a
        rows.append(dict(name=c["name"], poly=p, lb=c["lb"], ub=c["ub"]))
    return dict(T=T, names=m["names"], lb=m["lb"], ub=m["ub"], vt=m["vt"],
                obj=m["obj"]["lin"], rows=rows)


def row_vars(r):
    s = set()
    for mono in r["poly"]:
        s.update(mono)
    return s


def partition(M):
    """Identify periods and linking rows.

    Linking candidates: (a) the single row that contains exactly T variables
    and no other structure (horizon row); (b) copy rows x_a - x_b = 0 whose two
    variables both appear in tank-balance rows (rows with a 3600 coefficient).
    Everything else must split into T components of equal size; the function
    asserts this and orders periods along the link chain.
    """
    T = M["T"]
    rows = M["rows"]
    nv = len(M["names"])
    balance_vars = set()
    for r in rows:
        if any(abs(Fraction(a)) == 3600 for a in r["poly"].values()):
            balance_vars |= row_vars(r)
    link, horizon = [], []
    for i, r in enumerate(rows):
        p = r["poly"]
        vs = row_vars(r)
        if (len(p) == 2 and all(len(k) == 1 for k in p) and sorted(Fraction(a) for a in p.values()) == [-1, 1]
                and r["lb"] == "0" and r["ub"] == "0" and vs <= balance_vars):
            link.append(i)
        elif len(vs) == T and all(len(k) == 1 and Fraction(a) == 1 for k, a in p.items()) and T > 1:
            horizon.append(i)
    # union-find over variables using the non-linking rows
    par = list(range(nv))

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a
    removed = set(link) | set(horizon)
    for i, r in enumerate(rows):
        if i in removed:
            continue
        vs = sorted(row_vars(r))
        for v in vs[1:]:
            a, b = find(vs[0]), find(v)
            if a != b:
                par[a] = b
    for j in M["obj"]:
        pass  # objective is separable (a sum), it does not link
    comp = collections.defaultdict(list)
    for v in range(nv):
        comp[find(v)].append(v)
    comps = sorted(comp.values(), key=len, reverse=True)
    return dict(link=link, horizon=horizon, comps=comps)


def structure(M):
    """Periods in time order, rows per period, linking rows, horizon rows.

    Returns dict with
      per_vars[t]  : sorted variable indices of period t (t = 0..T-1)
      per_rows[t]  : row indices whose variables all lie in period t
      link[t]      : rows linking period t and t+1, as (row, var_t, var_t1)
      horizon      : rows touching more than two periods
    Time direction: period 0 is the chain end that contains fixed variables
    (initial tank levels); asserted below.
    """
    T = M["T"]
    rows = M["rows"]
    P = partition(M)
    comps = P["comps"]
    assert len(comps) == T and len({len(c) for c in comps}) == 1, [len(c) for c in comps]
    cid = {}
    for k, c in enumerate(comps):
        for v in c:
            cid[v] = k
    per_rows = collections.defaultdict(list)
    cross, horizon = [], []
    for i, r in enumerate(rows):
        ks = {cid[v] for v in row_vars(r)}
        if len(ks) == 1:
            per_rows[ks.pop()].append(i)
        elif len(ks) == 2 and i in P["link"]:
            cross.append(i)
        else:
            horizon.append(i)
    adj = collections.defaultdict(set)
    for i in cross:
        a, b = {cid[v] for v in row_vars(rows[i])}
        adj[a].add(b)
        adj[b].add(a)
    ends = [k for k in range(T) if len(adj[k]) <= 1]
    if T == 1:
        order = [0]
    else:
        assert len(ends) == 2 and all(len(adj[k]) <= 2 for k in range(T))
        fixed = lambda k: sum(1 for v in comps[k] if M["lb"][v] == M["ub"][v])
        start = max(ends, key=fixed)
        assert fixed(start) > fixed(min(ends, key=fixed)), [fixed(k) for k in range(T)]
        order, prev = [start], None
        while len(order) < T:
            nxt = [k for k in adj[order[-1]] if k != prev]
            assert len(nxt) == 1
            prev = order[-1]
            order.append(nxt[0])
    pos = {k: t for t, k in enumerate(order)}
    link = collections.defaultdict(list)
    for i in cross:
        vs = sorted(row_vars(rows[i]), key=lambda v: pos[cid[v]])
        t0, t1 = pos[cid[vs[0]]], pos[cid[vs[1]]]
        assert t1 == t0 + 1, (i, t0, t1)
        link[t0].append((i, vs[0], vs[1]))
    return dict(per_vars=[sorted(comps[k]) for k in order],
                per_rows=[per_rows[k] for k in order],
                link=[link[t] for t in range(T - 1)], horizon=horizon)
