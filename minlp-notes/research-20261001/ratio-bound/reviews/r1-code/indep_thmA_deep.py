"""Reviewer: Theorem A / Corollary A' on deep corners (vertex close to dS, D large). usage: python3 indep_thmA_deep.py SEED N"""
import sys, numpy as np, indep_checks as I
I.rng = np.random.default_rng(int(sys.argv[1]))
n = int(sys.argv[2])
viol = 0; vc = 0; ncor = 0; mins = []
for it in range(n):
    N = 3 if it % 2 == 0 else 4
    while True:
        sbar = I.rng.normal(size=3)
        sbar[2] = sbar[0]*sbar[1] + 10.0**I.rng.uniform(-7, -2)
        P = I.rng.normal(size=(3, N)); c = I.rng.uniform(0.2, 2, size=N)
        z = I.zK(sbar, P, c)
        if np.isfinite(z) and z > 1e-9: break
    Pt = P*(z/c)
    X, Y = np.max(abs(Pt[0])), np.max(abs(Pt[1])); D = np.sqrt(X*Y/I.q(sbar))
    rp = I.rho_par(sbar, Pt)
    mins.append((rp/I.fD(D), D))
    if rp < I.fD(D)*(1-1e-9): viol += 1
    mus = []
    for j in range(N):
        p = Pt[:, j]; A = -p[0]*p[1]; B = np.array([-sbar[1], -sbar[0], 1.0]) @ p; g0 = I.q(sbar)
        if ((A > 0 and B*B < 4*A*g0) or (A >= 0 and B >= 0)) and B < 0: mus.append(-I.rel_disc(sbar, p))
    mu = min(mus) if mus else 1.0
    if mu > 0 and D >= 1:
        ncor += 1; gam = np.sqrt((1-mu)/(1+mu)); gD = max(gam, 1/D)
        if rp < (1/(D*(gD+np.sqrt(1+gD*gD))))*(1-1e-9): vc += 1
mins.sort()
print('deep corners %d: D range %.3g..%.3g, violations of Theorem A %d, min rho_par/f(D) %.4f at D=%.3g; Corollary A applicable %d, violations %d'
      % (n, min(m[1] for m in mins), max(m[1] for m in mins), viol, mins[0][0], mins[0][1], ncor, vc))
print('PASS' if viol == 0 and vc == 0 else 'FAIL')
