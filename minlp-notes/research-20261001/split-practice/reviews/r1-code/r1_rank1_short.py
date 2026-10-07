"""Reviewer r1: do short maximum-violation representatives exist at the rank-1
rational neighbours of rank-1 roots?  (Independent of stream code.)

For a numerically rank-1 root Y we take the rank-1 neighbour l(x~) with x~ the
first column rounded to a 1e-6 grid, p = D(1, x~) primitive, and look for a
short v with p^T v = -floor(D/2) (Theorem 4 of the split note: these are
exactly the maximum-violation splits of l(x~)) by LLL with an embedding
(sympy DomainMatrix.lll, exact).  We then evaluate q at the stored float
matrix exactly and compare with the logged Theorem 3 result.
Usage (from split-practice/): python3 reviews/r1-code/r1_rank1_short.py K
"""
import json
import math
import os
import sys
from fractions import Fraction as F

import numpy as np
from sympy.polys.domains import ZZ
from sympy.polys.matrices import DomainMatrix

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
K = int(sys.argv[1]) if len(sys.argv) > 1 else 10


def q_exact(Y, v):
    nz = [i for i in range(len(v)) if v[i]]
    s = F(0)
    for i in nz:
        for j in nz:
            s += v[i] * v[j] * F(float(Y[i, j]))
        s += v[i] * F(float(Y[i, 0]))
    return s


def short_solution(p, m, M=None):
    """short integer v with p.v = m via LLL on [[I, M p], [0, -M m * 1, c]]"""
    N = len(p)
    M = M or 10 ** 12
    c = 1
    rows = []
    for i in range(N):
        rows.append([int(i == j) for j in range(N)] + [M * p[i], 0])
    rows.append([0] * N + [-M * m, c])
    B = DomainMatrix([[ZZ(a) for a in r] for r in rows], (N + 1, N + 2), ZZ).lll()
    best = None
    for r in B.to_Matrix().tolist():
        r = [int(a) for a in r]
        if r[N] == 0 and abs(r[N + 1]) == c:
            v = r[:N] if r[N + 1] == c else [-a for a in r[:N]]
            if sum(a * b for a, b in zip(p, v)) == m:
                if best is None or max(map(abs, v)) < max(map(abs, best)):
                    best = v
    return best


if __name__ == "__main__":
    recs = [json.loads(l) for k in range(3) for l in open(os.path.join(ROOT, f"logs/sep_run2_s{k}.jsonl"))]
    roots = [d for d in recs if d["file"].endswith("root.npz") and d.get("thm3", {}).get("rank") == 1 and "error" not in d["thm3"]]
    setdir = lambda f: "points_" + ("BT" if f.startswith("bt") else "DM") + f.split("_n")[1].split("_")[0]
    print(len(roots), "rank-1 roots with a Theorem 3 value; checking", min(K, len(roots)))
    nsane = 0; done = 0
    for d in roots[:K]:
        Y = np.load(os.path.join(ROOT, "data", setdir(d["file"]), d["file"]))["Y"]; Y = (Y + Y.T) / 2
        x = [F(round(a * 10 ** 6), 10 ** 6) for a in Y[0, 1:] / Y[0, 0]]
        D = 1
        for a in x:
            D = D * a.denominator // math.gcd(D, a.denominator)
        p = [D] + [int(a * D) for a in x]
        g = 0
        for a in p:
            g = math.gcd(g, a)
        assert g == 1
        m = -(D // 2)
        v = short_solution(p, m)
        if v is None:
            print(d["file"], "no short solution found by LLL embedding"); continue
        qn = F(m * (m + D), D * D)
        qY = float(q_exact(Y, v))
        sane = -0.25 - 1e-6 <= qY < 0
        nsane += sane; done += 1
        print(f"{d['file']:36s} D={D} max|v|={max(map(abs, v))} supp(w)={sum(1 for a in v[1:] if a)} q(neighbour)={float(qn):.12f} "
              f"q(stored Y)={qY:.6f} {'sane' if sane else 'NOT sane'} | logged thm3: digits {d['thm3']['vmax_digits']} q_at_Y {d['thm3']['q_at_Y']}")
    print(f"short representatives sane at stored Y: {nsane}/{done}")
