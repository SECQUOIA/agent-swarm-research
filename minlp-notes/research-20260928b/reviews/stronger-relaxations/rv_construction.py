"""Check 2: the null-space completion of Lemma 4.1, rebuilt independently, for a genuinely
multi-support mixture (not only the two-point mixture used by the author).

Instance: n = 6, p = 40, k = 3; z = mixture of 5 random 3-subsets of F0 = {0..6}; beta = z * bbar.
Checks:
 (a) global PSD, <X'X, E> = 0, objective identity (o) of Lemma 4.1;
 (b) Lemma 4.1(ii) point: membership in H_T for ALL pairs T (independent disjunctive SDP, margin);
 (c) Lemma 4.1(i) point with r = 3: membership in H_T for a sample of triples;
 (d) negative controls: K = 0 (no null-space noise) and the (ii) point tested against triples;
 (e) Remark 4.5: the moment matrix of (1, zeta, beta) of the explicit random variables is PSD,
     satisfies diag Z = z, diag U = beta, McCormick, Z 1 <= k z, and VIOLATES the product cones;
 (f) the L_2 root value (solved) is <= Phi at the constructed point.
"""
import os as _os
for _v in ["OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "RAYON_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"]:
    _os.environ[_v] = "1"
import itertools, time
import numpy as np
from rv_common import gen_core, hull_margin, Lr, sdp1, zb

rng = np.random.default_rng(7)
n, p, k = 6, 40, 3
X, y, lam, S = gen_core(n, p, k, b=1.0, sigma=0.5, seed=11, lam=np.sqrt(n))
F0 = list(range(7))
sup = [tuple(sorted(rng.choice(F0, k, replace=False))) for _ in range(5)]
w = rng.dirichlet(np.ones(5))
z = np.zeros(p)
for s, ws in zip(sup, w):
    z[list(s)] += ws
F = [j for j in F0 if z[j] > 0]
Z1 = [j for j in range(p) if j not in F]
bbar = rng.standard_normal(p)
beta = np.zeros(p); beta[F] = z[F] * bbar[F]
b = np.zeros(p); b[F] = bbar[F]                    # b = beta / z
ETT = np.zeros((p, p))
for s, ws in zip(sup, w):
    v = np.zeros(p); v[list(s)] = 1; ETT += ws * np.outer(v, v)
D = np.diag(b) @ (ETT - np.outer(z, z)) @ np.diag(b)
pi = float(np.sum(beta[F] ** 2 * (1 / z[F] - 1)))
print('supports', sup, 'weights', np.round(w, 3))
print('z on F', dict(zip(F, np.round(z[F], 3))), ' tr D =', D.trace(), ' pi =', pi)
DF = D[np.ix_(F, F)]
ev, U = np.linalg.eigh(DF); ev = np.clip(ev, 0, None)
DFh = U @ np.diag(np.sqrt(ev)) @ U.T
DFhp = U @ np.diag([1 / np.sqrt(e) if e > 1e-12 else 0 for e in ev]) @ U.T
XF, XZ = X[:, F], X[:, Z1]
W = XZ @ XZ.T; Wi = np.linalg.inv(W)
PN = np.eye(len(Z1)) - XZ.T @ Wi @ XZ
q = np.einsum('im,im->m', XZ, Wi @ XZ)
Q = X.T @ X + lam * np.eye(p)
theta = np.linalg.eigvalsh(XF.T @ Wi @ XF).max()
print(f'theta_F = {theta:.4f}, q_max = {q.max():.4f}, |Z1| = {len(Z1)}')


def point(sig, mode):
    GF = np.sqrt(1 + sig) * DFh
    C = -XZ.T @ Wi @ XF @ GF
    G = np.zeros((p, len(F))); G[F] = GF; G[Z1] = C
    if mode == 'pairs':
        Lam = np.sum(C ** 2, axis=1) / (sig * (1 - q) ** 2)
        K = PN @ np.diag(Lam) @ PN
    elif mode == 'r3':
        eta = max(np.linalg.norm(XZ[:, list(M)].T @ Wi @ XZ[:, list(M)], 2)
                  for M in itertools.combinations(range(len(Z1)), 2))
        cm = max(np.linalg.norm(C[list(M)], 2) ** 2 for M in itertools.combinations(range(len(Z1)), 2))
        kap = (1 + sig) / sig * cm / (1 - eta)
        K = kap * PN
        print(f'  r=3: eta = {eta:.4f}, kappa = {kap:.4f}')
    else:
        K = np.zeros((len(Z1), len(Z1)))
    E = G @ G.T
    E[np.ix_(Z1, Z1)] += K
    B = np.outer(beta, beta) + E
    return B, E, C, K, G


def phi(B):
    return float(y @ y - 2 * (X.T @ y) @ beta + np.sum(Q * B))


P = float(np.sum((y - X @ beta) ** 2) + lam * np.sum(beta[F] ** 2 / z[F]))
sig = 0.3
B, E, C, K, G = point(sig, 'pairs')
M = np.block([[np.ones((1, 1)), beta[None]], [beta[:, None], B]])
print('(a) min eig [[1,b],[b,B]] =', np.linalg.eigvalsh(M).min(), '  <X\'X,E> =', np.sum((X.T @ X) * E))
rhs = P + lam * (sig * pi + np.sum(C ** 2) + np.trace(K))
print(f'    Phi = {phi(B):.10f}, identity (o) rhs = {rhs:.10f}, P = {P:.6f};  '
      f'||C||_F^2 = {np.sum(C**2):.5f} <= (1+sig) theta pi = {(1+sig)*theta*pi:.5f}')
bound_ii = P + lam * pi * (sig + (1 + sig) * theta * (1 + 1 / (sig * (1 - q.max()))))
print(f'    Lemma 4.1(ii) bound = {bound_ii:.6f} >= Phi: {bound_ii >= phi(B) - 1e-9}')


def margins(Bm, sets):
    out = []
    for T in sets:
        T = list(T)
        out.append(hull_margin([z[i] for i in T], [beta[i] for i in T], Bm[np.ix_(T, T)]))
    return np.array(out)


t0 = time.time()
pairs = list(itertools.combinations(range(p), 2))
mp = margins(B, pairs)
print(f'(b) (ii)-point, all {len(pairs)} pairs: worst margin {mp.min():.2e}  (#< -1e-7: {(mp < -1e-7).sum()})  [{time.time()-t0:.0f}s]')

B3, E3, C3, K3, _ = point(sig, 'r3')
print('    r=3 point: <X\'X,E> =', np.sum((X.T @ X) * E3), ' Phi - P =', phi(B3) - P, ' lam*pi =', lam * pi)
trip = [T for T in itertools.combinations(range(p), 3)]
mixed = [T for T in trip if any(i in F for i in T) and any(i in Z1 for i in T)]
inF = [T for T in trip if all(i in F for i in T)]
samp = inF + [mixed[i] for i in rng.choice(len(mixed), 500, replace=False)]
t0 = time.time()
m3 = margins(B3, samp)
print(f'(c) (i)-point r=3: {len(samp)} triples ({len(inF)} inside F, 500 mixed sampled): worst margin {m3.min():.2e} '
      f'(#< -1e-7: {(m3 < -1e-7).sum()})  [{time.time()-t0:.0f}s]')

B0, *_ = point(sig, 'none')
m0 = margins(B0, [(j, m) for j in F for m in Z1[:10]])
print(f'(d) control K = 0: worst pair margin {m0.min():.2e} (#< -1e-7: {(m0 < -1e-7).sum()} of {len(m0)})')
mt = margins(B, [T for T in samp[:200]])
print(f'    control: the pairs-only point tested on 200 triples: worst margin {mt.min():.2e} (#< -1e-7: {(mt < -1e-7).sum()})')

# (e) Remark 4.5 moment matrix of (1, zeta, beta)
EzZ = ETT
Ezb = np.zeros((p, p))       # E[zeta beta']
for s, ws in zip(sup, w):
    v = np.zeros(p); v[list(s)] = 1
    xi = b * v
    Ezb[:, F] += ws * np.outer(v, xi[F])
Ezfl = np.zeros((p, len(F)))  # E[zeta (xi - beta)_F']
for s, ws in zip(sup, w):
    v = np.zeros(p); v[list(s)] = 1
    Ezfl += ws * np.outer(v, (b * v - beta)[F])
Ezb[:, Z1] = (1 + sig) ** -0.5 * Ezfl @ DFhp @ C.T
Y = np.zeros((2 * p + 1, 2 * p + 1))
Y[0, 0] = 1; Y[0, 1:p + 1] = Y[1:p + 1, 0] = z; Y[0, p + 1:] = Y[p + 1:, 0] = beta
Y[1:p + 1, 1:p + 1] = EzZ; Y[1:p + 1, p + 1:] = Ezb; Y[p + 1:, 1:p + 1] = Ezb.T; Y[p + 1:, p + 1:] = B
Zm, Um = EzZ, Ezb
off = ~np.eye(p, dtype=bool)
mc = max((Zm - np.minimum.outer(z, z))[off].max(), (-Zm)[off].max(), (np.add.outer(z, z) - 1 - Zm)[off].max())
pc = (Um ** 2 - Zm * np.diag(B)[None, :])[off]
print(f'(e) Remark 4.5 moment matrix: min eig {np.linalg.eigvalsh(Y).min():.2e}; |diag Z - z| = {np.abs(np.diag(Zm)-z).max():.1e}; '
      f'|diag U - beta| = {np.abs(np.diag(Um)-beta).max():.1e}; McCormick max viol {mc:.1e}; '
      f'max(Z1 - k z) = {(Zm.sum(1) - k*z).max():.1e}')
print(f'    product cones U_jm^2 <= Z_jm B_mm: max violation {pc.max():.3e} ({(pc > 1e-9).sum()} of {pc.size} violated)')

# (f) solved relaxations vs the constructed point
t0 = time.time()
L2root = Lr(X, y, lam, k, 2)
s1 = sdp1(X, y, lam, k)
print(f'(f) sdp1 root = {s1:.6f}, L2 root = {L2root:.6f}, Phi(point) = {phi(B):.6f}; L2 <= Phi: {L2root <= phi(B) + 1e-7}  [{time.time()-t0:.0f}s]')
zbz = zb(X, y, lam, k, fix_z=z)
print(f'    zb with first moments fixed at this z: {zbz:.6f} (vs Phi(point) {phi(B):.6f}, P(z,beta) {P:.6f})')
