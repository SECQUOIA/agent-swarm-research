"""Verifier: exact structural comparison of the constraint rows of two OSiL
files (by variable and row names): linear coefficients and quadratic terms as
rationals, nonlinear trees serialised with variable names and exact numbers;
row bounds after moving the row constant. Reports rows that differ and
whether the objectives differ.
Usage: python3 struct_cmp.py A.osil B.osil"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from osil_eval_cmp import read, tag


def ser(e, names):
    t = tag(e)
    if t == "number":
        return ("n", Fraction(e.get("value")))
    if t == "variable":
        return ("v", names[int(e.get("idx"))], Fraction(e.get("coef", "1")), tuple(ser(c, names) for c in e))
    return (t,) + tuple(ser(c, names) for c in e)


def rowkey(M, i):
    nm = M["vars"]
    lin = M["obj"]["lin"] if i == -1 else M["lin"].get(i, {})
    L = tuple(sorted((nm[j], c) for j, c in lin.items() if c != 0))
    Q = tuple(sorted((tuple(sorted((nm[p], nm[q]))), c) for p, q, c in M["quad"].get(i, [])))
    N = ser(M["nl"][i], nm) if i in M["nl"] else None
    if i == -1:
        B = (M["obj"]["sense"], M["obj"]["const"])
    else:
        k = M["cconst"][i]
        B = (None if M["clb"][i] is None else M["clb"][i] - k, None if M["cub"][i] is None else M["cub"][i] - k)
    return L, Q, N, B


A, B = read(sys.argv[1]), read(sys.argv[2])
ia = {n: i for i, n in enumerate(A["cons"])}
ib = {n: i for i, n in enumerate(B["cons"])}
va = {n: (A["type"][j], A["lb"][j], A["ub"][j]) for j, n in enumerate(A["vars"])}
vb = {n: (B["type"][j], B["lb"][j], B["ub"][j]) for j, n in enumerate(B["vars"])}
print("variables identical (names, types, bounds):", va == vb)
diff = [n for n in ia if n not in ib or rowkey(A, ia[n]) != rowkey(B, ib[n])]
print(f"rows {len(ia)} vs {len(ib)}; structurally different rows: {len(diff)} {diff[:10]}")
oa, ob = rowkey(A, -1), rowkey(B, -1)
print("objective: linear equal", oa[0] == ob[0], "quad equal", oa[1] == ob[1], "nl equal", oa[2] == ob[2], "sense/const", oa[3], ob[3])
