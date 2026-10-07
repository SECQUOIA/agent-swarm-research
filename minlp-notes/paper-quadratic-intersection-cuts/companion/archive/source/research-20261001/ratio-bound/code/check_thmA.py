"""Checks for Lemma R (orbit sets as {det(F) q >= l^2/4, tr >= 0}) and Theorem A.
(1) Lemma R: for random F with det F > 0 and random points s, sym(F^T M(s)) >= 0 iff
    det(F) q(s) >= l_F(s)^2 / 4 and tr(F^T M(s)) >= 0, with l_F(s) = f1 x - f4 y - f3 w + f2
    (F^T = [[f1, f2], [f3, f4]]).
(2) Theorem A on random bilinear corners (N = 3 and N = 5 rays, random costs):
    bound(D) <= rho_par <= z_A (SDP bisection, certified lower bound of an explicit X) <= 1.
usage: python3 check_thmA.py SEED NINST"""
import sys
import numpy as np
import warnings
import rb

warnings.filterwarnings('ignore')
seed, ninst = int(sys.argv[1]), int(sys.argv[2])
rng = np.random.default_rng(seed)
bad = 0
for k in range(20000):
    F = rng.normal(size=(2, 2))
    if np.linalg.det(F) <= 0:
        F[:, 0] *= -1
    s = rng.normal(size=3) * 3
    A = F.T @ rb.M(s)
    psd = np.linalg.eigvalsh(rb.sym(A))[0] >= 0
    (f1, f2), (f3, f4) = F.T
    ell = f1 * s[0] - f4 * s[1] - f3 * s[2] + f2
    rep = (np.linalg.det(F) * rb.q(s) >= ell * ell / 4) and (np.trace(A) >= 0)
    bad += psd != rep
print('Lemma R: mismatches in 20000 random (F, s):', bad)
viol = 0
worst = []
n = 0
while n < ninst:
    N = 3 if n % 2 == 0 else 5
    sbar = rng.normal(size=3) * 2
    sbar[2] = sbar[0] * sbar[1] + np.exp(rng.normal() * 1.5)
    P = rng.normal(size=(3, N))
    c = np.exp(rng.normal(size=N) * 0.5)
    z, lam = rb.zK(sbar, P, c)
    if not np.isfinite(z):
        continue
    n += 1
    Pt = rb.scaled_rays(P, c, z)
    D = rb.D_inv(sbar, Pt)
    tb = rb.theoremA_bound(D)
    rp, _ = rb.rho_par(sbar, Pt, ngrid=1201)
    cert, hi, _ = rb.zA_ratio(sbar, Pt, iters=25)
    ok = tb <= rp * (1 + 1e-9) and rp <= hi * (1 + 1e-6) + 1e-7 and cert <= 1 + 1e-6
    viol += not ok
    worst.append((rp / max(cert, 1e-12), D, tb, rp, cert, hi, N))
    print('N=%d D=%.4g bound(D)=%.4g rho_par=%.4g zA_cert=%.4g zA_hi=%.4g %s' % (N, D, tb, rp, cert, hi, 'OK' if ok else 'VIOLATION'), flush=True)
print('instances', n, 'violations', viol)
print('max rho_par / zA_cert = %.6f' % max(w[0] for w in worst))
