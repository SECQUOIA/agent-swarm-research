"""Period subproblems of waterno2_T as exact polynomial data (verifier's code).

Built from osilx (decimal strings -> Fraction) and the verifier's own period
recovery (vstruct.analyse).  The Lagrangian objective of period t is built here
from the multiplier file, independently of the authors' period.py/rbb.py:

  full Lagrangian  L = f(x) + sum_{s,k} lam[s][k] * (-x_end(s,k) + x_start(s+1,k))
                          + mu * (rhs - sum_t h_t)
  period t objective: sum of its cost variables
                      - lam[t][k]   on x_end(t,k)      (t <= T-2)
                      + lam[t-1][k] on x_start(t,k)    (t >= 1)
                      - mu          on h_t
  constant: mu * rhs.
The k-th link of transition s is the k-th link row of that transition in
row-index order (the authors' convention: tank 1, tank 2, tank 3).
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import sys
from fractions import Fraction as F
sys.path.insert(0, _RESEARCH + "/reviews/open-instances-verification")
import osilx
from vstruct import analyse

_CACHE = {}


def instance(T):
    if T not in _CACHE:
        m, out, sigs, order, per, rows_in, pid, links, hor = analyse(T)
        pos = {c: t for t, c in enumerate(order)}
        idx = {n: i for i, n in enumerate(m["names"])}
        per_vars = [sorted(per[c]) for c in order]
        per_rows = [sorted(rows_in[c]) for c in order]
        rowidx = {c["name"]: i for i, c in enumerate(m["cons"])}
        lk = [[] for _ in range(T - 1)]
        for (name, s, na, ca, nb, cb) in links:
            assert F(ca) == -1 and F(cb) == 1
            lk[s].append((rowidx[name], idx[na], idx[nb]))
        for s in range(T - 1):
            lk[s].sort()
            assert len(lk[s]) == 3
        h = m["cons"][hor[0]]
        hvar = [None] * T
        for v, a in h["lin"].items():
            assert F(a) == 1
            hvar[pos[pid[v]]] = v
        _CACHE[T] = dict(m=m, T=T, per_vars=per_vars, per_rows=per_rows, links=lk,
                         hvar=hvar, hrhs=F(h["lb"]), hname=h["name"])
    return _CACHE[T]


def poly(c):
    """Row -> {monomial(sorted tuple of global var idx): Fraction}."""
    p = {}
    for j, a in c["lin"].items():
        p[(j,)] = p.get((j,), 0) + F(a)
    for i, j, a in c["quad"]:
        k = tuple(sorted((i, j)))
        p[k] = p.get(k, 0) + F(a)
    if c["nl"] is not None:
        t = c["nl"]
        assert t[0] == "power" and t[1][0] == "var" and t[2][0] == "num", t
        e = F(t[2][1])
        assert e.denominator == 1 and e >= 2
        k = (t[1][1],) * int(e)
        p[k] = p.get(k, 0) + F(t[1][2])
    return {k: a for k, a in p.items() if a != 0}


def period_objective(I, t, lam, mu):
    """Exact objective {global var: Fraction} of period t; lam, mu given as floats."""
    m, T = I["m"], I["T"]
    c = {}

    def add(v, a):
        c[v] = c.get(v, 0) + a
    for v in I["per_vars"][t]:
        if v in m["obj"]["lin"]:
            add(v, F(m["obj"]["lin"][v]))
    if t <= T - 2:
        for k, (i, a, b) in enumerate(I["links"][t]):
            add(a, -F(lam[t][k]))
    if t >= 1:
        for k, (i, a, b) in enumerate(I["links"][t - 1]):
            add(b, F(lam[t - 1][k]))
    add(I["hvar"][t], -F(mu))
    return c


def lagrangian_constant(I, mu):
    return F(mu) * I["hrhs"]
