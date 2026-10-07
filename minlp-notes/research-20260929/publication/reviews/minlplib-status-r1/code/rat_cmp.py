"""Verifier: exact comparison of two OSiL models whose rows are rational
functions (+, -, *, /, integer powers). Each row becomes N/D with polynomial
N, D (exact rationals); rows a, b are equal iff N_a*D_b - N_b*D_a == 0 and
the bounds (after moving constants) agree. Usage: rat_cmp.py A.osil B.osil"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from poly_cmp_lib import read, tag, padd, pmul, const  # noqa: E402

ONE = {(): Fraction(1)}


def R(e, nm):
    t = tag(e)
    ch = list(e)
    if t == "number":
        return const(Fraction(e.get("value"))), ONE
    if t == "variable":
        return {((nm[int(e.get("idx"))], 1),): Fraction(e.get("coef", "1"))}, ONE
    a = [R(c, nm) for c in ch]
    if t in ("sum", "plus", "minus"):
        if t == "minus":
            a = [a[0], ({k: -v for k, v in a[1][0].items()}, a[1][1])]
        n, d = {}, ONE
        for (n2, d2) in a:
            n = padd(pmul(n, d2), pmul(n2, d)) if d2 != d else padd(n, n2)
            d = pmul(d, d2) if d2 != d else d
        return n, d
    if t == "negate":
        return {k: -v for k, v in a[0][0].items()}, a[0][1]
    if t in ("times", "product"):
        n, d = ONE, ONE
        for (n2, d2) in a:
            n, d = pmul(n, n2), pmul(d, d2)
        return n, d
    if t == "divide":
        return pmul(a[0][0], a[1][1]), pmul(a[0][1], a[1][0])
    if t == "square":
        return pmul(a[0][0], a[0][0]), pmul(a[0][1], a[0][1])
    if t == "power":
        ex = a[1][0]
        if a[1][1] == ONE and list(ex.keys()) == [()] and ex[()].denominator == 1 and ex[()] >= 0:
            n, d = ONE, ONE
            for _ in range(int(ex[()])):
                n, d = pmul(n, a[0][0]), pmul(d, a[0][1])
            return n, d
    raise ValueError("unsupported " + t)


def row(M, i):
    nm = M["vars"]
    lin = M["obj"]["lin"] if i == -1 else M["lin"].get(i, {})
    p = {((nm[j], 1),): c for j, c in lin.items() if c != 0}
    for (a, b, c) in M["quad"].get(i, []):
        p = padd(p, pmul({((nm[a], 1),): Fraction(1)}, {((nm[b], 1),): c}))
    n, d = p, ONE
    if i in M["nl"]:
        n2, d2 = R(M["nl"][i], nm)
        n, d = padd(pmul(n, d2), n2), d2
    k = M["obj"]["const"] if i == -1 else M["cconst"][i]
    if i == -1:
        n = padd(n, pmul(const(k), d))
        bnd = None
    else:
        bnd = (None if M["clb"][i] is None else M["clb"][i] - k, None if M["cub"][i] is None else M["cub"][i] - k)
    return n, d, bnd


A, B = read(sys.argv[1]), read(sys.argv[2])
ia = {n: i for i, n in enumerate(A["cons"])}
ib = {n: i for i, n in enumerate(B["cons"])}
va = {n: (A["type"][j], A["lb"][j], A["ub"][j]) for j, n in enumerate(A["vars"])}
vb = {n: (B["type"][j], B["lb"][j], B["ub"][j]) for j, n in enumerate(B["vars"])}
print("variables identical:", va == vb, "; row names identical:", set(ia) == set(ib))
nd = nu = 0
for name in ["objective"] + list(ia):
    i, j = (-1, -1) if name == "objective" else (ia[name], ib[name])
    try:
        na, da, ba = row(A, i)
        nb, db, bb = row(B, j)
    except ValueError:
        nu += 1
        continue
    diff = padd(pmul(na, db), pmul(nb, da), -1)
    if diff or ba != bb:
        nd += 1
        if nd <= 3:
            print("  differs:", name, "terms", len(diff), "bounds equal", ba == bb)
print(f"rows+objective compared exactly {len(ia) + 1 - nu}; differing {nd}; unsupported {nu}")
