"""Exact decoding of eg_disc_s, eg_disc2_s, eg_int_s, eg_all_s (Schoonen collection).

Every row has the form   lin(objvar) + negate(sum(T_1, ..., T_97 [, v*coef])) in [lb, ub]
with Gaussian product terms
    T_m = a_m * prod_i exp( gamma_i * (mu_mi + s_i x_i)^2 )
(one factor per decision variable; the order of the factors inside the product
varies and is handled).  Rows with objvar give  objvar >= c_k + g_k(x), where
g_k(x) = sum_m T_km(x) - (linear terms inside the sum); the other rows are side
constraints lb <= -g_k(x) <= ub.  All constants are kept as Fractions.
"""
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "reviews",
                                "open-instances-verification"))
import osilx  # noqa: E402

OSIL = os.environ["MINLPLIB_OSIL_ROOT"]


def decode(name):
    I = osilx.read(os.path.join(OSIL, name + ".osil"))
    names = I["names"]
    nv = len(names)
    o = I["obj"]
    assert o["sense"] == "min" and o["constant"] == "0" and not o["quad"] and o["nl"] is None
    (objv, oc), = o["lin"].items()
    assert oc == "1"
    assert I["lb"][objv] == "-INF" and I["ub"][objv] == "INF"
    dvars = [j for j in range(nv) if j != objv]
    lb = [Fr(I["lb"][j]) for j in dvars]
    ub = [Fr(I["ub"][j]) for j in dvars]
    isint = [I["vt"][j] == "I" for j in dvars]
    assert all(t in ("I", "C") for t in (I["vt"][j] for j in dvars))
    pos = {j: p for p, j in enumerate(dvars)}
    rows = []
    for c in I["cons"]:
        assert c["constant"] == "0" and not c["quad"]
        t = c["nl"]
        assert t[0] == "negate" and t[1][0] == "sum"
        terms, linin = [], {}
        for p in t[1][1:]:
            if p[0] == "var":
                linin[pos[p[1]]] = linin.get(pos[p[1]], Fr(0)) + Fr(p[2])
                continue
            assert p[0] == "product"
            nums = [q for q in p[1:] if q[0] == "num"]
            exps = [q for q in p[1:] if q[0] == "exp"]
            assert len(nums) == 1 and len(exps) == len(p) - 2
            fac = {}
            for e in exps:
                pr = e[1]
                assert pr[0] == "product" and len(pr) == 3
                sq, g = pr[1], pr[2]
                assert sq[0] == "square" and g[0] == "num" and len(sq) == 2
                s = sq[1]
                assert s[0] == "sum" and len(s) == 3 and s[1][0] == "num" and s[2][0] == "var"
                v = pos[s[2][1]]
                assert v not in fac
                fac[v] = (Fr(s[2][2]), Fr(s[1][1]), Fr(g[1]))   # (scale s, mu, gamma)
            assert sorted(fac) == list(range(len(dvars)))
            terms.append((Fr(nums[0][1]), fac))
        lin = {pos[j]: Fr(a) for j, a in c["lin"].items() if j != objv}
        assert not lin
        has_obj = objv in c["lin"]
        if has_obj:
            assert c["lin"][objv] == "1" and osilx.isinf(c["ub"]) and not osilx.isinf(c["lb"])
        rows.append(dict(name=c["name"], obj=has_obj, lb=None if osilx.isinf(c["lb"]) else Fr(c["lb"]),
                         ub=None if osilx.isinf(c["ub"]) else Fr(c["ub"]), terms=terms, linin=linin))
    # per-variable scales must be common to all terms (used for vectorization)
    scale = [None] * len(dvars)
    for r in rows:
        for a, fac in r["terms"]:
            for v, (s, mu, g) in fac.items():
                assert scale[v] is None or scale[v] == s
                scale[v] = s
    return dict(name=name, I=I, objv=objv, dvars=dvars, names=[names[j] for j in dvars], lb=lb, ub=ub,
                isint=isint, rows=rows, scale=scale)


def g_value(M, r, x, exp, num):
    """row function g(x) = sum_m T_m(x) + sum linin*x (so that the row reads lin(objvar) - g(x))."""
    s = num(0)
    for a, fac in r["terms"]:
        e = num(0)
        for v, (sc, mu, g) in fac.items():
            t = num(mu) + num(sc) * x[v]
            e = e + num(g) * t * t
        s = s + num(a) * exp(e)
    for v, c in r["linin"].items():
        s = s + num(c) * x[v]
    return s
