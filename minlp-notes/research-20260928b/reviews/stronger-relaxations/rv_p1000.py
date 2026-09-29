"""Check 3: independent reproduction of the p = 1000 explicit point (note Section 7.1, verify_construction).
Instance: core generator with n = 30, p = 1000, k = 3, seed = 1, tau0 = 1.5 (lam = 0.75 sqrt(2 n log p)).
(1) OPT by full enumeration of the 166 million triples (rv_enum.opt3);
(2) the two-point failure direction of Theorem 4.4(b): helper half H1, violator l = argmax_{H2} |a_l|;
    Lemma 4.1(ii) point built from my own formulas, with beta minimizing the inflated perspective;
(3) checks: <X'X, E> = 0, global PSD, the Schur sufficient condition E_T - D_T >= 0 on EVERY pair
    (m in Z1, j in F), and exact hull membership (disjunctive SDP) on 60 sampled pairs;
(4) the value Phi of the point versus f(S*) = OPT; and the inflation actually paid."""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import time
import numpy as np
from rv_common import gen_core, fval, hull_margin
from rv_enum import opt3

n, p, k, seed = 30, 1000, 3, 1
X, y, lam, S = gen_core(n, p, k, seed=seed, tau0=1.5)
S = list(S)
fS, bS, r = fval(X, y, lam, S)
a = X.T @ r
nulls = [j for j in range(p) if j not in S]
H1, H2 = nulls[:len(nulls) // 2], nulls[len(nulls) // 2:]
m0 = lam * np.abs(bS).min(); i = S[int(np.argmin(np.abs(bS)))]
l = H2[int(np.argmax(np.abs(a[H2])))]
print(f'lam = {lam:.4f}, f(S*) = {fS:.8f}, S* = {S}, |a_l|/m0 = {abs(a[l])/m0:.4f} (l = {l}), max over all nulls = {np.abs(a[nulls]).max()/m0:.4f}')
t0 = time.time()
OPT, arg = opt3(X, y, lam)
print(f'(1) OPT by enumeration = {OPT:.10f} at {arg}; S* optimal: {sorted(arg) == sorted(S)}  [{time.time()-t0:.0f}s]')

F = S + [l]; Z1 = H1
XF, XZ = X[:, F], X[:, Z1]
W = XZ @ XZ.T; Wi = np.linalg.inv(W)
q = np.einsum('im,im->m', XZ, Wi @ XZ)
theta = np.linalg.eigvalsh(XF.T @ Wi @ XF).max()
Q = X.T @ X + lam * np.eye(p)
print(f'theta_F = {theta:.4f}, q_max = {q.max():.4f}, |Z1| = {len(Z1)}')


def build(t, sig, eps):
    z = np.zeros(p); z[S] = 1; z[i] = 1 - t; z[l] = t
    zF = z[F]
    pen = lam + lam * (1 + eps) * (1 / zF - 1)
    bF = np.linalg.solve(XF.T @ XF + np.diag(pen), XF.T @ y)
    beta = np.zeros(p); beta[F] = bF
    # two-point mixture: supports S (prob 1 - t) and S - i + l (prob t); D = t(1-t) v v'
    bb = np.zeros(p); bb[F] = bF / zF
    v = np.zeros(len(F)); v[F.index(i)] = -bb[i]; v[F.index(l)] = bb[l]
    GF = np.sqrt((1 + sig) * t * (1 - t)) * v[:, None]          # |F| x 1
    C = -XZ.T @ (Wi @ (XF @ GF))                                  # |Z1| x 1
    Lam = (C[:, 0] ** 2) / (sig * (1 - q) ** 2)
    pi = float(np.sum(bF ** 2 * (1 / zF - 1)))
    trK = float(np.sum((1 - q) * Lam))
    Phi = float(np.sum((y - XF @ bF) ** 2) + lam * bF @ bF + lam * (float(np.sum(GF ** 2)) + float(np.sum(C ** 2)) + trK))
    P = float(np.sum((y - XF @ bF) ** 2) + lam * np.sum(bF ** 2 / zF))
    return dict(z=z, beta=beta, GF=GF, C=C, Lam=Lam, pi=pi, Phi=Phi, P=P, t=t, sig=sig, eps=eps, v=v)


best = None
for t in [0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3]:
    for sig in [0.05, 0.1, 0.15, 0.2, 0.3, 0.5]:
        for eps in [0.0, 0.3, 0.6, 1.0]:
            c_ = build(t, sig, eps)
            if best is None or c_['Phi'] < best['Phi']:
                best = c_
c_ = best
print(f"(2) best grid point t = {c_['t']}, sigma = {c_['sig']}, eps(beta) = {c_['eps']}: Phi - f(S*) = {c_['Phi'] - fS:.6f}; "
      f"inflation paid (Phi - P)/(lam pi) = {(c_['Phi'] - c_['P'])/(lam*c_['pi']):.4f}")

# explicit B on I = F u Z1
I = F + Z1
G = np.concatenate([c_['GF'], c_['C']])[:, 0]
PN = np.eye(len(Z1)) - XZ.T @ Wi @ XZ
K = PN @ np.diag(c_['Lam']) @ PN
E = np.outer(G, G); E[len(F):, len(F):] += K
bI = c_['beta'][I]; zI = c_['z'][I]
B = np.outer(bI, bI) + E
XI = X[:, I]
Phi2 = float(y @ y - 2 * (XI.T @ y) @ bI + np.sum((XI.T @ XI + lam * np.eye(len(I))) * B))
print(f"(3) <X'X,E> = {np.sum((XI.T @ XI) * E):.2e}; Phi recomputed from B - f(S*) = {Phi2 - fS:.6f}")
Mg = np.block([[np.ones((1, 1)), bI[None]], [bI[:, None], B]])
print(f"    min eig [[1,b'],[b,B]] (scaled by max|B|) = {np.linalg.eigvalsh(Mg).min()/np.abs(Mg).max():.2e}")
# Schur sufficient condition for every pair (m, j), m in Z1, j in F: [[E_mm, E_mj],[E_jm, E_jj - D_jj]] >= 0
t_ = c_['t']; Dvec = t_ * (1 - t_) * c_['v'] ** 2             # diag D on F
EFF = E[:len(F), :len(F)]
Emm = np.diag(E)[len(F):]
worst = np.inf
for jj in range(len(F)):
    s22 = EFF[jj, jj] - Dvec[jj]
    s12 = E[len(F):, jj]
    detv = Emm * s22 - s12 ** 2
    mn = 0.5 * (Emm + s22 - np.sqrt((Emm - s22) ** 2 + 4 * s12 ** 2))
    worst = min(worst, float((mn / np.maximum(1e-300, np.maximum(Emm, s22))).min()))
print(f"    Schur sufficient condition on all {len(F)*len(Z1)} pairs (Z1 x F): worst scaled min eig = {worst:.2e}")
rng = np.random.default_rng(0)
samp = [(a_, b_) for a_ in range(len(F)) for b_ in range(a_ + 1, len(F))]
samp += [(int(m), int(jj)) for m, jj in zip(rng.choice(np.arange(len(F), len(I)), 44, replace=False), rng.integers(0, len(F), 44))]
samp += [(int(m1), int(m2)) for m1, m2 in zip(rng.choice(np.arange(len(F), len(I)), 10), rng.choice(np.arange(len(F), len(I)), 10)) if m1 != m2]
t0 = time.time()
mg = [hull_margin([zI[a_], zI[b_]], [bI[a_], bI[b_]], B[np.ix_([a_, b_], [a_, b_])]) for a_, b_ in samp]
print(f"    exact H_T membership on {len(samp)} sampled pairs (all inside F): worst margin {min(mg):.2e}  [{time.time()-t0:.0f}s]")
print(f"(4) L_2 (hence sdp_2, SDP1) root <= Phi = f(S*) {c_['Phi'] - fS:+.6f} < OPT = f(S*): {c_['Phi'] < OPT}")
