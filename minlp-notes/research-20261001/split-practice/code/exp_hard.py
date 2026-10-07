"""How hard are the hard instances in practice?

Builds the exact-cover (X3C) matrices of Theorem 1 (h^2 = n+1) and of
Corollary 5 (4 h^2 = max(3, n+1) * Ghat), with and without a planted cover,
and runs
  * the {0,+-1} families with |supp w| <= 3 (polynomial; must fail for q >= 3),
  * exact maximum-violation separation by Schnorr-Euchner enumeration
    (sep_pd_float; the matrices are positive definite),
  * the exact normalised separator sep_ratio,
  * Buchheim-Traversi style MIQP: Gurobi 13.0.2 with |v_i| <= K.
Usage: python3 exp_hard.py OUT.jsonl
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import json
import os
import random
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260928b/side-results'))
import check_split_separation as css  # noqa: E402
from exp_separate import family_best  # noqa: E402
from lattice import sep_pd_float, sep_ratio  # noqa: E402
from miqp_sep import gurobi_sep, scip_sep  # noqa: E402


def x3c(qq, nsets, planted, rng):
    U = list(range(3 * qq))
    sets = []
    if planted:
        P = U[:]; rng.shuffle(P)
        sets += [tuple(sorted(P[3 * k:3 * k + 3])) for k in range(qq)]
    while len(sets) < nsets:
        sets.append(tuple(sorted(rng.sample(U, 3))))
    rng.shuffle(sets)
    return sets


def has_cover(sets, qq):
    """Exact cover by backtracking (element with fewest candidate sets first)."""
    U = set(range(3 * qq))
    by = {e: [S for S in sets if e in S] for e in U}

    def rec(left):
        if not left:
            return True
        e = min(left, key=lambda e: sum(1 for S in by[e] if set(S) <= left))
        for S in by[e]:
            if set(S) <= left and rec(left - set(S)):
                return True
        return False
    return rec(U)


def matrices(sets, qq):
    n = len(sets)
    A = [[int(e in S) for S in sets] for e in range(3 * qq)]
    b = [1] * (3 * qq)
    X1, G = css.reduction(A, b)                      # Theorem 1, h^2 = n + 1
    Ghat = max(abs(G[i][j]) for i in range(n + 2) for j in range(n + 2) if (i, j) != (0, 0))
    h2 = F(max(3, n + 1) * Ghat, 4)
    X5, _ = css.reduction(A, b, h2=h2)               # Corollary 5
    return {"thm1": (X1, F(n + 1)), "cor5": (X5, h2)}


def run_one(qq, nsets, planted, seed, out):
    rng = random.Random(seed)
    sets = x3c(qq, nsets, planted, rng)
    cover = has_cover(sets, qq)
    n = len(sets)
    for kind, (X, h2) in matrices(sets, qq).items():
        Xf = np.array([[float(a) for a in row] for row in X])
        pred = -1.0 / (4 * (n + 1 + float(h2))) if cover else 0.0
        rec = dict(q=qq, n=n, N=n + 2, planted=planted, cover=cover, seed=seed, kind=kind,
                   h2=float(h2), predicted_min_q=pred, cond=float(np.linalg.cond(Xf)))
        for k in (1, 2, 3):
            t = time.time(); fb = family_best(Xf, k)
            rec[f"fam{k}"] = dict(max_viol=fb["max_viol"], time=time.time() - t)
        r = sep_pd_float(Xf, max_nodes=5 * 10**8)
        rec["enum"] = dict(q=r["q"], nodes=r["nodes"], complete=bool(r["complete"]), time=r["time"],
                           supp=None if r["v"] is None else int(sum(1 for a in r["v"][1:] if a != 0)))
        r = sep_ratio(Xf, max_nodes=5 * 10**8)
        rec["ratio"] = dict(ratio=r["ratio"], q=r["q"], nodes=r["nodes"], complete=bool(r["complete"]),
                            time=r["time"], iters=r["iters"])
        for K in (1,):
            g = gurobi_sep(Xf, K=K, timelimit=300, clip=False)
            rec[f"grb{K}"] = dict(q=g["q"], time=g["time"], status=g["status"], bound=g["bound"],
                                  nodes=g["nodes"])
        if qq <= 10:
            g = scip_sep(Xf, K=1, timelimit=300, clip=False)
            rec["scip1"] = dict(q=g["q"], time=g["time"], status=g["status"], bound=g["bound"],
                                nodes=g["nodes"])
        out.write(json.dumps(rec) + "\n"); out.flush()
        print(qq, n, planted, cover, kind, "pred", pred, "enum", rec["enum"]["q"], rec["enum"]["time"],
              "grb", rec["grb1"]["q"], rec["grb1"]["time"], rec["grb1"]["status"], flush=True)


if __name__ == "__main__":
    outp = sys.argv[1]
    with open(outp, "a") as out:
        for qq in (2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 25):
            for planted in (True, False):
                for nsets_factor in (2, 3):
                    run_one(qq, nsets_factor * qq, planted, 1000 * qq + 10 * nsets_factor + planted, out)
