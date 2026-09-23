"""Reviewer check of hadamard_n (n = 6..9).

(a) Generic polynomial expansion of the OSiL nl tree (sum/product/variable/number/negate/minus)
    into {monomial (sorted tuple of var indices, with repetition): coefficient}; compared with the
    Leibniz expansion of det(B), B[i][j] = b_{i*n+j} (0-based var index), computed here.
    Row e1 / objective / variable bounds and types checked.
(b) Transfer 0/1 -> +-1 checked on random matrices; classical bounds recomputed.
(c) Primal matrices from certs evaluated in the parsed model (exact integers) and by own
    fraction-Gaussian determinant.
"""
import itertools
import json
import math
import random
import sys
import time
from fractions import Fraction as F

from rv_osil import read, strip

OSIL = "/home/sgusev/.cache/minlplib/minlplib/osil/hadamard_{}.osil"
CERT = "/home/sgusev/repo/minlp-notes/research-20260922/benchmark-observations/code/structural/certs/hadamard_{}.json"


def mul(p, q):
    r = {}
    for m1, c1 in p.items():
        for m2, c2 in q.items():
            m = tuple(sorted(m1 + m2))
            r[m] = r.get(m, 0) + c1 * c2
    return {m: c for m, c in r.items() if c != 0}


def add(ps):
    r = {}
    for p in ps:
        for m, c in p.items():
            r[m] = r.get(m, 0) + c
    return {m: c for m, c in r.items() if c != 0}


def expand(node):
    t = strip(node.tag)
    ch = list(node)
    if t == "variable":
        assert not ch
        return {(int(node.attrib["idx"]),): F(node.attrib.get("coef", "1"))}
    if t == "number":
        v = F(node.attrib["value"])
        return {(): v} if v else {}
    if t == "sum":
        return add(expand(c) for c in ch)
    if t == "product":
        p = {(): F(1)}
        for c in ch:
            p = mul(p, expand(c))
        return p
    if t == "negate":
        return {m: -c for m, c in expand(ch[0]).items()}
    if t == "minus":
        a, b = ch
        return add([expand(a), {m: -c for m, c in expand(b).items()}])
    raise ValueError("unhandled node " + t)


def perm_sign(p):
    sgn, seen = 1, [False] * len(p)
    for i in range(len(p)):
        if not seen[i]:
            j, L = i, 0
            while not seen[j]:
                seen[j] = True
                j = p[j]
                L += 1
            if L % 2 == 0:
                sgn = -sgn
    return sgn


def leibniz(n):
    return {tuple(sorted(i * n + p[i] for i in range(n))): perm_sign(p)
            for p in itertools.permutations(range(n))}


def det_frac(M):
    A = [[F(x) for x in row] for row in M]
    n, d = len(A), F(1)
    for k in range(n):
        piv = next((i for i in range(k, n) if A[i][k] != 0), None)
        if piv is None:
            return F(0)
        if piv != k:
            A[k], A[piv] = A[piv], A[k]
            d = -d
        d *= A[k][k]
        for i in range(k + 1, n):
            f = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] -= f * A[k][j]
    return d


def eval_poly(p, x):
    tot = 0
    for m, c in p.items():
        v = c
        for i in m:
            v *= x[i]
        tot += v
    return tot


for n in [int(a) for a in sys.argv[1:]] or [6, 7, 8, 9]:
    t0 = time.time()
    m = read(OSIL.format(n))
    V = m["vars"]
    assert len(V) == n * n + 1
    for v in V[:-1]:
        assert v["type"] == "B" and v["lb"] == 0 and v["ub"] == 1, v
    assert V[-1]["type"] == "C" and V[-1]["lb"] == "-INF" and V[-1]["ub"] == "INF"
    # variable names b1..b_{n^2} in order (row-major interpretation is ours; any fixed
    # bijection works as long as the polynomial is det of that arrangement)
    assert [v["name"] for v in V[:-1]] == [f"b{i}" for i in range(1, n * n + 1)]
    ob = m["objs"]
    assert len(ob) == 1 and ob[0]["sense"] == "max" and ob[0]["lin"] == {n * n: 1} and ob[0]["constant"] == 0
    assert not m["objquad"] and -1 not in m["nl"]
    assert len(m["cons"]) == 1
    c = m["cons"][0]
    assert c["lb"] == 0 and c["ub"] == "INF" and c["constant"] == 0 and c["lin"] == {n * n: -1} and not c["quad"], c
    assert set(m["nl"]) == {0}
    poly = expand(m["nl"][0])
    del m
    L = leibniz(n)
    same = poly == {k: F(v) for k, v in L.items()}
    print(f"hadamard_{n}: {len(poly)} terms; poly == Leibniz det(B) (row-major): {same};"
          f" max monomial degree {max(len(k) for k in poly)}; multilinear:"
          f" {all(len(set(k)) == len(k) for k in poly)}; {time.time() - t0:.1f}s")
    # primal
    cert = json.load(open(CERT.format(n)))
    x = cert["primal_matrix_rowmajor"]
    assert len(x) == n * n and set(x) <= {0, 1}
    B = [x[i * n:(i + 1) * n] for i in range(n)]
    dB = det_frac(B)
    val = eval_poly(poly, x)
    objvar = val  # best feasible objvar for this B
    act = val - objvar
    print(f"   primal: det(B) own Gauss = {dB}, poly(B) = {val}, row e1 activity at objvar=det: {act},"
          f" certificate det {cert['primal_det_exact']}, claimed dual {cert['certified_dual_int']}")
    del poly

# (b) transfer check
random.seed(1)
for n in [6, 7, 8, 9]:
    for _ in range(200):
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        A = [[1] * (n + 1)] + [[1] + [1 - 2 * B[i][j] for j in range(n)] for i in range(n)]
        assert det_frac(A) == (-2) ** n * det_frac(B)
print("transfer det(A) = (-2)^n det(B): verified on 800 random matrices")


def to01(bsq, n):
    """largest integer D with D^2 <= bsq / 4^n"""
    return math.isqrt(bsq // 4 ** n)


for n in [6, 7, 8, 9]:
    mm = n + 1
    out = {"Hadamard": mm ** mm}
    if mm % 2 == 1:
        out["Barba"] = (2 * mm - 1) * (mm - 1) ** (mm - 1)
    if mm % 4 == 2:
        out["Ehlich-Wojtas"] = ((2 * mm - 2) * (mm - 2) ** ((mm - 2) // 2)) ** 2
    if mm % 4 == 3:
        s = 5  # Ehlich's choice for n = 7
        r = mm // s
        v = mm - r * s
        u = s - v
        val = F((mm - 3) ** (mm - s) * (mm - 3 + 4 * r) ** u * (mm + 1 + 4 * r) ** v) * \
            (1 - F(u * r, mm - 3 + 4 * r) - F(v * (r + 1), mm + 1 + 4 * r))
        assert val.denominator == 1
        out["Ehlich(s=5)"] = int(val)
        # check s = 5 is the optimal s among 3..7 for mm = 7 (Ehlich's bound is min over s)
        alts = {}
        for s2 in range(3, 8):
            r2 = mm // s2
            v2 = mm - r2 * s2
            u2 = s2 - v2
            alts[s2] = float(F((mm - 3) ** (mm - s2) * (mm - 3 + 4 * r2) ** u2 * (mm + 1 + 4 * r2) ** v2) *
                             (1 - F(u2 * r2, mm - 3 + 4 * r2) - F(v2 * (r2 + 1), mm + 1 + 4 * r2)))
        print("   m=7 Ehlich expression by s:", alts)
    print(f"n={n} (m={mm}):", {k: (v, to01(v, n), round(math.sqrt(v) / 2 ** n, 4)) for k, v in out.items()})
