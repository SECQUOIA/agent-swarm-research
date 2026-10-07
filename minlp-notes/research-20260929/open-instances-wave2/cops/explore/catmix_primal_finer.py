"""Re-extract the float-DP policy on a finer theta grid, refine with L-BFGS-B, compare."""
import sys, numpy as np
sys.path.insert(0, '..')
import catmix_model as cmx, catmix_primal as cp
N = int(sys.argv[1]); dth = float(sys.argv[2])
m, K = cmx.extract(N); fm = cmx.FloatModel(K, N)
u_old = np.load('../logs/catmix%d_u.npy' % N); J_old = fm.J_grad(u_old)[0]
upol, dpval = cp.float_dp_policy(N, K, dtheta=dth)
u2, J2, kkt = cp.refine(N, K, upol)
print(N, 'dtheta', dth, 'float DP value %.17g  policy J %.17g  refined J %.17g  old J %.17g  improvement %.3e'
      % (dpval, fm.J_grad(upol)[0], J2, J_old, J_old - J2), kkt, flush=True)
if J2 < J_old:
    np.save('../logs/catmix%d_u_finer.npy' % N, u2)
