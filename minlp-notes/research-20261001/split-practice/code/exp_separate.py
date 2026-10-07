"""Split separation at practical points (saved by exp_points.py).

For each point Y (order N = n+1) this records
  * numerical rank at several thresholds;
  * the best split in the families with w in {0,+-1}^n and |supp w| = 1, 2, 3
    (best right-hand side computed exactly for each w), by violation and by
    normalised violation  -q/|w|^2;
  * the exact maximum normalised violation over all of Z^N (sep_ratio:
    Dinkelbach + Schnorr-Euchner enumeration);
  * Buchheim-Traversi style maximum violation by MIQP with box |v_i| <= K
    (Gurobi 13.0.2 command line, 1 thread, time limit);
  * Theorem 3 (exact rational, fixed rank) on a rational rank-r matrix close to Y.

Identity used: for v = (v0, w),  q(v) = (v0+t)(v0+t+1) + w^T S w,  t = w^T x,
S = X - x x^T.  So max_v0 (-q) = phi(t) - w^T S w with phi(t) = {t}(1-{t}).

Usage: python3 exp_separate.py OUT.jsonl file1.npz file2.npz ...
"""
import itertools
import json
import os
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice import sep_ratio, thm3_exact  # noqa: E402
from miqp_sep import gurobi_sep  # noqa: E402


def phi(t):
    f = t - np.floor(t)
    return f * (1 - f)


def family_best(Y, k, chunk=200000):
    """Best split with w in {0,+-1}^n, |supp w| = k (global sign fixed)."""
    N = Y.shape[0]; n = N - 1
    x = Y[0, 1:]; S = Y[1:, 1:] - np.outer(x, x)
    best_v = (-np.inf, None); best_r = (-np.inf, None)
    signs = np.array([s for s in itertools.product([1.0, -1.0], repeat=k) if s[0] > 0])
    combs = itertools.combinations(range(n), k)
    while True:
        C = np.array(list(itertools.islice(combs, chunk)))
        if len(C) == 0:
            break
        for s in signs:
            t = (x[C] * s).sum(1)
            var = np.zeros(len(C))
            for a in range(k):
                for b in range(k):
                    var += s[a] * s[b] * S[C[:, a], C[:, b]]
            viol = phi(t) - var
            i = int(np.argmax(viol))
            if viol[i] > best_v[0]:
                best_v = (float(viol[i]), (C[i].tolist(), s.tolist(), float(t[i])))
            if viol[i] / k > best_r[0]:
                best_r = (float(viol[i] / k), (C[i].tolist(), s.tolist()))
    return dict(k=k, max_viol=best_v[0], arg=best_v[1], max_ratio=best_r[0])


def rationalize_rank(Y, r, den=10**6):
    """Exact rational PSD matrix of rank r close to Y: X = P^T C^{-1} P with
    P = rounded rows K of the rank-r truncation, C = P[:, K]; normalised X00 = 1."""
    w, V = np.linalg.eigh(Y)
    idx = np.argsort(w)[::-1][:r]
    Yr = (V[:, idx] * w[idx]) @ V[:, idx].T
    # pivoted Cholesky for well-conditioned pivots
    N = Y.shape[0]; d = np.diag(Yr).copy(); K = []; Lf = np.zeros((N, r))
    for j in range(r):
        p = int(np.argmax(d)); K.append(p)
        Lf[:, j] = (Yr[:, p] - Lf[:, :j] @ Lf[p, :j]) / np.sqrt(d[p])
        d -= Lf[:, j] ** 2; d[K] = -np.inf
    Fr = lambda a: F(int(round(a * den)), den)
    P = [[Fr(Yr[k, j]) for j in range(N)] for k in K]
    for a in range(r):          # symmetric C
        for b in range(r):
            P[a][K[b]] = P[b][K[a]] if b < a else P[a][K[b]]
    C = [[P[a][K[b]] for b in range(r)] for a in range(r)]
    from lattice import mat_inv_frac
    Ci = mat_inv_frac(C)
    CiP = [[sum(Ci[a][c] * P[c][j] for c in range(r)) for j in range(N)] for a in range(r)]
    X = [[sum(P[a][i] * CiP[a][j] for a in range(r)) for j in range(N)] for i in range(N)]
    s = X[0][0]
    X = [[e / s for e in row] for row in X]
    Xf = np.array([[float(e) for e in row] for row in X])
    G = [[e / s for e in row] for row in Ci]
    return X, float(np.abs(Xf - Y).max()), (P, G)


def analyse(path, gurobi_K=(1, 3, 10), gurobi_tl=30, thm3_max_rank=12, families=(1, 2, 3)):
    Y = np.load(path)["Y"]
    Y = (Y + Y.T) / 2
    N = Y.shape[0]
    w = np.linalg.eigvalsh(Y)[::-1]
    rec = dict(file=os.path.basename(path), N=N,
               rank={f"{t:g}": int((w > t * w[0]).sum()) for t in (1e-3, 1e-5, 1e-7, 1e-9)},
               lam_min=float(w[-1]))
    # families
    for k in families:
        if k == 3 and N - 1 > 70:
            continue
        t = time.time(); fb = family_best(Y, k); fb["time"] = time.time() - t
        rec[f"fam{k}"] = fb
    # exact normalised separation
    r = sep_ratio(Y, max_nodes=2 * 10**7)
    v = r["v"]
    rec["ratio"] = dict(ratio=r["ratio"], q=r["q"], iters=r["iters"], nodes=r["nodes"],
                        complete=bool(r["complete"]), time=r["time"],
                        v=None if v is None else [int(a) for a in v],
                        supp=None if v is None else int(sum(1 for a in v[1:] if a != 0)),
                        vmax=None if v is None else int(max(abs(int(a)) for a in v)))
    # B-T style max violation with a box
    for K in gurobi_K:
        g = gurobi_sep(Y, K=K, timelimit=gurobi_tl)
        vv = g["v"]
        rec[f"grb{K}"] = dict(q=g["q"], time=g["time"], status=g["status"], bound=g["bound"],
                              nodes=g["nodes"],
                              supp=None if vv is None else int((vv[1:] != 0).sum()),
                              vmax=None if vv is None else int(np.abs(vv).max()),
                              v=None if vv is None else [int(a) for a in vv])
    # Theorem 3 on a rational rank-r neighbour
    rr = rec["rank"]["1e-05"]
    if rr <= thm3_max_rank:
        t = time.time()
        X, err, fac = rationalize_rank(Y, rr)
        t_rat = time.time() - t
        try:
            res = thm3_exact(X, max_nodes=2 * 10**6, factor=fac)
            vv = res["v"]
            qY = None
            if vv is not None:
                from lattice import q_exact
                YF = [[F(float(e)) for e in row] for row in Y]   # exact value of the float matrix
                qe = q_exact(YF, vv)
                try:
                    qY = float(qe)
                except OverflowError:
                    qY = ("+" if qe > 0 else "-") + "1e%d" % (len(str(abs(qe.numerator))) - len(str(qe.denominator)))
            rec["thm3"] = dict(rank=res["rank"], q=float(res["q"]), q_at_Y=qY, err=err,
                               vmax_digits=len(str(res.get("vmax"))),
                               vmax_raw_digits=len(str(res.get("vmax_raw"))),
                               vmax=res.get("vmax") if len(str(res.get("vmax"))) < 18 else None,
                               supp=None if vv is None else int(sum(1 for a in vv[1:] if a != 0)),
                               delta_digits=len(str(res["delta"])), nodes=res["nodes"],
                               complete=bool(res["complete"]),
                               first_complete=bool(res["first_complete"]),
                               second_complete=bool(res["second_complete"]),
                               optimum_certified=bool(res["optimum_certified"]), t_rat=t_rat,
                               t_setup=res["t_setup"], t_enum=res["t_enum"], time=res["time"])
        except Exception as e:
            rec["thm3"] = dict(error=str(e)[:200], rank=rr, err=err)
    return rec


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.integer):
        return int(o)
    return o


if __name__ == "__main__":
    out = sys.argv[1]
    done = set()
    if os.path.exists(out):
        done = {json.loads(l)["file"] for l in open(out)}
    with open(out, "a") as f:
        for p in sys.argv[2:]:
            if os.path.basename(p) in done:
                continue
            rec = analyse(p)
            f.write(json.dumps(_clean(rec)) + "\n"); f.flush()
            print(rec["file"], rec["rank"], "ratio", round(rec["ratio"]["ratio"], 5),
                  "grb1", rec["grb1"]["q"], flush=True)
