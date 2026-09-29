"""Explicit null-space completion (Lemma B.1 of thresholds.md) at the root, for large p.

For an instance whose perspective root certificate fails with a violator l in the second
half Z2 of the nulls, build the lifted point (z, beta, B) of the construction:
  z = 1_S - t e_i + t e_l,  mixture of the supports S (prob 1-t) and S-i+l (prob t),
  B = beta beta' + g g' (rows F u Z1) + P_N Lambda P_N (block Z1), Lambda = diag(C_m^2/(sigma(1-q_m)^2)),
with g_F = sqrt((1+sigma) t (1-t)) v,  v = b_i e_i - b_l e_l,  g_Z1 = -X_Z1' W^{-1} X_F g_F,
and check numerically:
  (1) <X'X, B - beta beta'> = 0 and the objective Phi = y'y - 2y'X beta + <X'X + lam I, B>;
  (2) global PSD of [[1, beta'], [beta, B]];
  (3) every Atamturk-Gomez pair constraint (sdp_2) over all pairs;
  (4) exact lifted pairwise-hull membership (L_2) for a sample of pairs, by a small SDP;
  (5) the spartrahedron constraint k Diag(B) >= B (not covered by the theorem; reported only).
Prints Phi - f(S*) (negative = the relaxations sdp_1, sdp_2, L_2 have root value < f(S*)).
usage: verify_construction.py n p k seed [tau0]
"""
import os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS"]:
    os.environ[_v] = "1"
import sys, time
import numpy as np
import cvxpy as cp
from relax import instance, ridge

n, p, k, seed = (int(a) for a in sys.argv[1:5])
tau0 = float(sys.argv[5]) if len(sys.argv) > 5 else 1.5
X, y, lam, S = instance(n, p, k, seed=seed, tau0=tau0)
S = list(S)
fS, bS, r = ridge(X, y, lam, S)
a = X.T @ r
nulls = [j for j in range(p) if j not in set(S)]
Z1 = np.array(nulls[: len(nulls) // 2]); Z2 = np.array(nulls[len(nulls) // 2:])
m0 = lam * np.abs(bS).min()
iS = int(np.argmin(np.abs(bS))); i = S[iS]
l = int(Z2[np.argmax(np.abs(a[Z2]))])
print(f"n={n} p={p} k={k} seed={seed} lam={lam:.3f} f(S*)={fS:.6f}  max_Z2|a_l|/m0={abs(a[l])/m0:.4f}"
      f"  max_all|a_l|/m0={np.abs(a[nulls]).max()/m0:.4f}")
F = S + [l]
XF = X[:, F]
XZ = X[:, Z1]
W = XZ @ XZ.T
Winv = np.linalg.inv(W)
q_m = np.einsum('ij,jk,ki->i', XZ.T, Winv, XZ)  # x_m' W^{-1} x_m
r_order = 2


def build(t, sigma, eps_guess=0.0):
    z = np.zeros(p); z[S] = 1.0; z[i] = 1 - t; z[l] = t
    # beta: generalized ridge on F with fractional penalty lam*(1+eps_guess)*(1/z-1)
    pen = lam + lam * (1 + eps_guess) * (1.0 / z[F] - 1.0)
    bF = np.linalg.solve(XF.T @ XF + np.diag(pen), XF.T @ y)
    beta = np.zeros(p); beta[F] = bF
    b = beta[F] / z[F]
    v = np.zeros(len(F)); v[F.index(i)] = b[F.index(i)]; v[F.index(l)] = -b[F.index(l)]
    gF = np.sqrt((1 + sigma) * t * (1 - t)) * v
    gZ = -XZ.T @ (Winv @ (XF @ gF))
    # r = 2 (pairs): K = P_N diag(lam_m) P_N with lam_m = C_m^2 / (sigma (1 - q_m)^2), so that
    # K_mm >= (1 - q_m)^2 lam_m = C_m^2 / sigma  (Schur condition for M = {m}); tr K = sum (1 - q_m) lam_m
    lamv = gZ ** 2 / (sigma * (1 - q_m) ** 2)
    kappa = lamv
    pi = t * (1 - t) * (v @ v)  # tr D
    trE = gF @ gF + gZ @ gZ + np.sum((1 - q_m) * lamv)
    Phi = float(np.sum((y - X @ beta) ** 2) + lam * beta @ beta + lam * trE)
    persp = float(np.sum((y - X @ beta) ** 2) + lam * np.sum(beta[F] ** 2 / z[F]))
    return dict(z=z, beta=beta, gF=gF, gZ=gZ, kappa=kappa, pi=pi, Phi=Phi, persp=persp, trE=trE)


best = None
for t in [0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2]:
    for sigma in [0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.2]:
        c = build(t, sigma)
        if best is None or c['Phi'] < best['Phi']:
            best = c; best['t'] = t; best['sigma'] = sigma
c = best
print(f"best t={c['t']} sigma={c['sigma']}: Phi - f(S*) = {c['Phi'] - fS:.6f}   perspective value at same (z,beta) - f(S*) = {c['persp'] - fS:.6f}"
      f"   excess inflation eps_eff = {(c['Phi'] - c['persp']) / (lam * c['pi']):.4f}")

# assemble B on the index set I = F u Z1 (other coordinates have zero rows)
Iidx = np.array(F + list(Z1)); pos = {j: s for s, j in enumerate(Iidx)}
G = np.concatenate([c['gF'], c['gZ']])
PN = np.eye(len(Z1)) - XZ.T @ Winv @ XZ
E = np.outer(G, G); E[len(F):, len(F):] += (PN * c['kappa'][None, :]) @ PN
bI = c['beta'][Iidx]; zI = c['z'][Iidx]
B = np.outer(bI, bI) + E
XI = X[:, Iidx]
print(f"(1) <X'X, B - beta beta'> = {np.sum((XI.T @ XI) * E):.3e}  (should be ~0);  "
      f"Phi recomputed - f(S*) = {float(y @ y - 2 * (X.T @ y)[Iidx] @ bI + np.sum((XI.T @ XI + lam * np.eye(len(Iidx))) * B)) - fS:.6f}")
Mg = np.block([[np.ones((1, 1)), bI[None, :]], [bI[:, None], B]])
print(f"(2) min eig [[1,beta'],[beta,B]] = {np.linalg.eigvalsh(Mg).min():.3e}")
# (3) sdp_2 pair constraints: [[w, b_i, b_j],[b_i, B_ii, B_ij],[b_j, B_ij, B_jj]] >= 0, w = min(1, z_i + z_j)
t0 = time.time()
I1, J1 = np.triu_indices(len(Iidx), 1)
w = np.minimum(1.0, zI[I1] + zI[J1])
mats = np.zeros((len(I1), 3, 3))
mats[:, 0, 0] = w; mats[:, 0, 1] = mats[:, 1, 0] = bI[I1]; mats[:, 0, 2] = mats[:, 2, 0] = bI[J1]
mats[:, 1, 1] = B[I1, I1]; mats[:, 2, 2] = B[J1, J1]; mats[:, 1, 2] = mats[:, 2, 1] = B[I1, J1]
scale = np.maximum(1.0, np.abs(mats).max(axis=(1, 2)))
mins = np.linalg.eigvalsh(mats / scale[:, None, None])[:, 0]
print(f"(3) sdp_2: {len(I1)} pairs on F u Z1 (all other pairs are trivially feasible); min scaled eig = {mins.min():.3e}; "
      f"violations (< -1e-9): {(mins < -1e-9).sum()}  [{time.time() - t0:.1f}s]")


def in_L2(zi, zj, bi, bj, Bii, Bij, Bjj):
    """min slack of the lifted pairwise hull decomposition (>= -tol means member)."""
    l11 = cp.Variable(); u, s, v_, tt = cp.Variable(), cp.Variable(), cp.Variable(), cp.Variable()
    P11 = cp.Variable((3, 3), symmetric=True); R = cp.Variable((2, 2), symmetric=True); d = cp.Variable()
    l10, l01, l00 = zi - l11, zj - l11, 1 - zi - zj + l11
    cons = [l11 >= d, l10 >= d, l01 >= d, l00 >= d, P11[0, 0] == l11, bi == u + P11[0, 1], bj == v_ + P11[0, 2],
            cp.bmat([[cp.reshape(l10, (1, 1), order='C'), cp.reshape(u, (1, 1), order='C')], [cp.reshape(u, (1, 1), order='C'), cp.reshape(s, (1, 1), order='C')]]) >> 0,
            cp.bmat([[cp.reshape(l01, (1, 1), order='C'), cp.reshape(v_, (1, 1), order='C')], [cp.reshape(v_, (1, 1), order='C'), cp.reshape(tt, (1, 1), order='C')]]) >> 0,
            P11 >> 0, R[0, 0] == Bii - s - P11[1, 1], R[1, 1] == Bjj - tt - P11[2, 2], R[0, 1] == Bij - P11[1, 2],
            R - d * np.eye(2) >> 0, P11 - d * np.eye(3) >> 0]
    pr = cp.Problem(cp.Maximize(d), cons)
    pr.solve(solver=cp.CLARABEL)
    return float(d.value) if d.value is not None else -np.inf


rng = np.random.default_rng(0)
sample = [(pos[i], pos[l])] + [(pos[j], pos[l]) for j in S if j != i] + [(pos[j], pos[i]) for j in S if j != i]
Zs = rng.choice(len(Z1), 40, replace=False) + len(F)
sample += [(int(m), pos[l]) for m in Zs[:15]] + [(int(m), pos[i]) for m in Zs[15:25]] + [(int(m), pos[S[0] if S[0] != i else S[1]]) for m in Zs[25:30]]
sample += [(int(Zs[30 + h]), int(Zs[35 + h])) for h in range(5)]
worst = min(in_L2(zI[a_], zI[b_], bI[a_], bI[b_], B[a_, a_], B[a_, b_], B[b_, b_]) for a_, b_ in sample)
print(f"(4) L_2 lifted pair hull: {len(sample)} sampled pairs (incl. all pairs inside F), worst margin = {worst:.3e}  (>= -1e-7 means member)")
spt = np.linalg.eigvalsh(k * np.diag(np.diag(Mg)) - Mg)  # homogenized form, as in Cifuentes-Li (k+1)? report both
spt2 = np.linalg.eigvalsh(k * np.diag(np.diag(B)) - B)
print(f"(5) spartrahedron k Diag(B) - B: min eig = {spt2.min():.3e} (not covered by the theorem)")
