"""Try to improve a catmix primal: snap small singular-arc controls to 0, re-run L-BFGS-B."""
import sys, numpy as np
sys.path.insert(0, '..')
import catmix_model as cmx, catmix_primal as cp
N = int(sys.argv[1]); thr = float(sys.argv[2])
m, K = cmx.extract(N); fm = cmx.FloatModel(K, N)
u = np.load('../logs/catmix%d_u.npy' % N)
J0 = fm.J_grad(u)[0]
v = u.copy(); v[v < thr] = 0.0
u2, J2, kkt = cp.refine(N, K, v)
print(N, 'thr', thr, 'J before %.17g after %.17g improvement %.3e' % (J0, J2, J0 - J2), kkt)
if J2 < J0:
    np.save('../logs/catmix%d_u_snap.npy' % N, u2)
