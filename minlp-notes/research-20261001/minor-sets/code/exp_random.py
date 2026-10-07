"""Random corners for the minor set S = {det = 0} in R^4 (note, Section 7.1).

sbar ~ N(0, I_4) conditioned on det(sbar) > 0, N rays p_j ~ N(0, I_4), w_j ~ U(0.2, 2).
For corners with finite z_K: support of the minimizer (and whether a support-2 minimizer lies on a
tangent edge), and the one-cut ratios z_family / z_K for scip, bcm, pr, orbit.
Usage: python3 exp_random.py SEED NCORNERS N OUT.jsonl
"""
import sys
import json
import numpy as np
from minor_core import zK, family_bounds, det4, mat, adj

seed, T, N, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = np.random.default_rng(seed)
f = open(out, 'w')
done = 0
tries = 0
while done < T:
    tries += 1
    s = rng.normal(size=4)
    if det4(s) <= 0:
        continue
    P = rng.normal(size=(4, N))
    w = rng.uniform(0.2, 2.0, N)
    zk, lam = zK(s, P, w, return_point=True)
    if not np.isfinite(zk):
        f.write(json.dumps(dict(seed=seed, idx=tries, zK=None)) + '\n')
        continue
    supp = [int(j) for j in np.nonzero(lam > 1e-9 * max(1.0, lam.max()))[0]]
    tstar = s + P @ lam
    tangent = None
    if len(supp) == 2:
        i, j = supp
        d = P[:, i] / w[i] - P[:, j] / w[j]          # edge direction of T* at level z_K
        g = np.array([tstar[3], -tstar[2], -tstar[1], tstar[0]])
        tangent = float(abs(g @ d) / (np.linalg.norm(g) * np.linalg.norm(d)))
    fb = family_bounds(s, P, w, zk, iters=36)
    rec = dict(seed=seed, idx=tries, N=N, zK=float(zk), support=supp, tangent_cos=tangent,
               ratios={k: v['ratio'] for k, v in fb.items()}, upper={k: v['upper'] for k, v in fb.items()},
               detnorm=float(det4(s) / (s @ s)))
    f.write(json.dumps(rec) + '\n')
    f.flush()
    done += 1
f.close()
print('done', done, 'tries', tries)
