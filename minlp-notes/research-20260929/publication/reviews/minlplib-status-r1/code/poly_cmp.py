"""Verifier: exact comparison of two OSiL models whose rows are polynomials.
Each row (and the objective) is expanded into a canonical polynomial
{monomial: Fraction} using variable names; the row constant is moved into the
bounds. Rows are compared exactly; for differing rows the largest coefficient
difference is reported. Non-polynomial nodes raise an error (row reported as
'not polynomial').
Usage: python3 poly_cmp.py A.osil B.osil"""
import sys
from collections import defaultdict
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from osil_eval_cmp import read, tag


def padd(a, b, s=1):
    r = defaultdict(Fraction, a)
    for k, v in b.items():
        r[k] += s * v
    return {k: v for k, v in r.items() if v != 0}


def pmul(a, b):
    r = defaultdict(Fraction)
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            d = defaultdict(int)
            for n, e in k1 + k2:
                d[n] += e
            r[tuple(sorted(d.items()))] += v1 * v2
    return {k: v for k, v in r.items() if v != 0}


def const(c):
    return {(): Fraction(c)} if c != 0 else {}


def P(e, nm):
    t = tag(e)
    ch = list(e)
    if t == "number":
        return const(Fraction(e.get("value")))
    if t == "variable":
        return {((nm[int(e.get("idx"))], 1),): Fraction(e.get("coef", "1"))}
    a = [P(c, nm) for c in ch]
    if t in ("sum", "plus"):
        r = {}
        for x in a:
            r = padd(r, x)
        return r
    if t == "minus":
        return padd(a[0], a[1], -1)
    if t == "negate":
        return {k: -v for k, v in a[0].items()}
    if t in ("times", "product"):
        r = const(1)
        for x in a:
            r = pmul(r, x)
        return r
    if t == "square":
        return pmul(a[0], a[0])
    if t == "power":
        ex = a[1]
        if list(ex.keys()) in ([()],) and ex[()].denominator == 1 and ex[()] >= 0:
            r = const(1)
            for _ in range(int(ex[()])):
                r = pmul(r, a[0])
            return r
    if t == "divide":
        d = a[1]
        if list(d.keys()) == [()]:
            return {k: v / d[()] for k, v in a[0].items()}
    raise ValueError("not polynomial: " + t)


def rowpoly(M, i):
    nm = M["vars"]
    lin = M["obj"]["lin"] if i == -1 else M["lin"].get(i, {})
    p = {((nm[j], 1),): c for j, c in lin.items() if c != 0}
    for (a, b, c) in M["quad"].get(i, []):
        p = padd(p, pmul({((nm[a], 1),): Fraction(1)}, {((nm[b], 1),): c}))
    if i in M["nl"]:
        p = padd(p, P(M["nl"][i], nm))
    k = M["obj"]["const"] if i == -1 else M["cconst"][i]
    if i == -1:
        p = padd(p, const(k))
        bnd = None
    else:
        bnd = (None if M["clb"][i] is None else M["clb"][i] - k, None if M["cub"][i] is None else M["cub"][i] - k)
    return p, bnd


A, B = read(sys.argv[1]), read(sys.argv[2])
ia = {n: i for i, n in enumerate(A["cons"])}
ib = {n: i for i, n in enumerate(B["cons"])}
va = {n: (A["type"][j], A["lb"][j], A["ub"][j]) for j, n in enumerate(A["vars"])}
vb = {n: (B["type"][j], B["lb"][j], B["ub"][j]) for j, n in enumerate(B["vars"])}
print("variables identical (names, types, bounds):", va == vb)
ndiff = nnp = 0
for name in ["objective"] + list(ia):
    i, j = (-1, -1) if name == "objective" else (ia[name], ib[name])
    try:
        pa, ba = rowpoly(A, i)
        pb, bb = rowpoly(B, j)
    except ValueError as ex:
        nnp += 1
        continue
    d = padd(pa, pb, -1)
    if d or ba != bb:
        ndiff += 1
        mx = max((abs(v) for v in d.values()), default=0)
        rel = max((abs(v) / max(abs(pa.get(k, 0)), abs(pb.get(k, 0))) for k, v in d.items()), default=0)
        print(f"  {name}: {len(d)} coefficients differ, max abs {float(mx):.3e}, max rel {float(rel):.3e}; bounds equal {ba == bb}"
              + (f"; e.g. {sorted(d.items(), key=lambda kv: -abs(kv[1]))[0]}" if d else ""))
print(f"rows+objective compared {len(ia) + 1 - nnp}; differing {ndiff}; not polynomial {nnp}")
