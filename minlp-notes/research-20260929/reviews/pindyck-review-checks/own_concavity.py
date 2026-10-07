"""Reviewer's own concavity certificate: Psi(theta) <= -mu I (mu = 1/1000) on a box Theta_hull
that contains Theta' (own ranges over own G'), Theta'' (own ranges over the author's G) and the
author's Theta. Branch and bound by bisection; every leaf is proved by own_psi.exact_test
(interval-coefficient affine forms + exact rational matrix test).

Split rule (heuristic only, does not affect validity): at the root, for each parameter of the
groups beta, E, phi, d, u, the float estimate is recomputed for both halves;
sens_k = est_root - max(est_lower_half, est_upper_half). A failing box is bisected in the
parameter with the largest sens_k * (current width / root width).
Output: logs/own_concavity.log, leaves.pkl.
"""
import os
import pickle
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import own_psi as P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = open(os.path.join(HERE, "logs", "own_concavity.log"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


T = 16
RG = pickle.load(open(os.path.join(HERE, "ranges.pkl"), "rb"))
RA = pickle.load(open(os.path.join(HERE, "ranges_authorG.pkl"), "rb"))
AD = pickle.load(open(os.path.join(HERE, "author_data.pkl"), "rb"))
lo0 = {g: np.minimum(np.minimum(np.array(RG["lo"][g]), np.array(RA["lo"][g])), AD["lo0"][g]) for g in P.GR}
hi0 = {g: np.maximum(np.maximum(np.array(RG["hi"][g]), np.array(RA["hi"][g])), AD["hi0"][g]) for g in P.GR}
for src, (l, h) in {"own G'": (RG["lo"], RG["hi"]), "author G": (RA["lo"], RA["hi"]), "author": (AD["lo0"], AD["hi0"])}.items():
    assert all(lo0[g][t] <= l[g][t] and h[g][t] <= hi0[g][t] for g in P.GR for t in range(T)), src
MU_EST = -1e-3


def estimate(lo, hi):
    H = P.psi_af(lo, hi)
    C, A, R = P.point_form(H)
    return P.float_estimate(C, A, R), (C, A, R)


t0 = time.time()
est0, _ = estimate(lo0, hi0)
say(f"root box: float estimate of the bound on lambda_max = {est0:.5f} (need < -0.001)")
sens = {}
for g in ["beta", "E", "phi", "d", "u"]:
    for t in range(T):
        if hi0[g][t] <= lo0[g][t] or (g == "E" and t == 0):
            continue
        mid = 0.5 * (lo0[g][t] + hi0[g][t])
        l1, h1 = {k: v.copy() for k, v in lo0.items()}, {k: v.copy() for k, v in hi0.items()}
        h1[g][t] = mid
        l2, h2 = {k: v.copy() for k, v in lo0.items()}, {k: v.copy() for k, v in hi0.items()}
        l2[g][t] = mid
        e1, _ = estimate(l1, h1)
        e2, _ = estimate(l2, h2)
        sens[(g, t)] = max(est0 - max(e1, e2), 0.0)
top = sorted(sens.items(), key=lambda kv: -kv[1])[:8]
say("root sensitivities (top 8):", [(f"{g}_{t + 1}", round(v, 5)) for (g, t), v in top], f"({time.time() - t0:.0f} s)")

queue = [(lo0, hi0, 0)]
leaves, nfail, splits = [], 0, {}
while queue:
    lo, hi, dep = queue.pop()
    est, (C, A, R) = estimate(lo, hi)
    ok = False
    if est < MU_EST:
        ok, rho = P.exact_test(C, A, R)
    if ok:
        leaves.append((lo, hi, est))
        say(f"  leaf {len(leaves)}: depth {dep}, float estimate {est:.5f}, exact test passed")
        continue
    nfail += 1
    assert dep < 25
    (g, t) = max(sens, key=lambda k: sens[k] * (hi[k[0]][k[1]] - lo[k[0]][k[1]]) / (hi0[k[0]][k[1]] - lo0[k[0]][k[1]]))
    splits[f"{g}_{t + 1}"] = splits.get(f"{g}_{t + 1}", 0) + 1
    mid = 0.5 * (lo[g][t] + hi[g][t])
    assert lo[g][t] < mid < hi[g][t]
    l1, h1 = {k: v.copy() for k, v in lo.items()}, {k: v.copy() for k, v in hi.items()}
    l2, h2 = {k: v.copy() for k, v in lo.items()}, {k: v.copy() for k, v in hi.items()}
    h1[g][t] = mid
    l2[g][t] = mid
    queue += [(l1, h1, dep + 1), (l2, h2, dep + 1)]
say(f"CERTIFIED: Psi(theta) <= -(1/1000) I on the whole hull box: {len(leaves)} leaves, {nfail} split boxes, "
    f"splits {splits}, largest leaf estimate {max(e for _, _, e in leaves):.5f}, total {time.time() - t0:.0f} s")
pickle.dump(dict(lo0=lo0, hi0=hi0, leaves=leaves, splits=splits), open(os.path.join(HERE, "leaves.pkl"), "wb"))
