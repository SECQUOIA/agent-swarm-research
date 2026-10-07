import numpy as np, json
from mpmath import mp, mpf, sqrt, log, diff, matrix, eig
mp.dps = 40
lbar = (3 - log(2)) / (4 * sqrt(2))
lam = np.load('lukvle10_lam_kkt.npy').copy()
LC = lam[495]
print('lambda_bar exact', lbar, ' binary64', repr(float(LC)), ' diff', mpf(float(LC)) - lbar)
s = -1 / sqrt(2)
def F(a, b):
    return (a*a) ** (b*b + 1) + (b*b) ** (a*a + 1)
L = mpf(float(LC))
ell = lambda a, b: F(a, b) - 2 * L * (a*a + b*b)
print('middle pair value at saddle (binary64 lambda)', ell(s, s))
H = matrix([[diff(ell, (s, s), (2, 0)), diff(ell, (s, s), (1, 1))], [diff(ell, (s, s), (1, 1)), diff(ell, (s, s), (0, 2))]])
E, _ = eig(H)
print('Hessian', H, 'eig', E)
print('grad at saddle', diff(ell, (s, s), (1, 0)), diff(ell, (s, s), (0, 1)))
# multipliers: verifier binary64 after replacement vs 40-digit KKT multipliers of the primal track
kl = {}
for line in open('lukvle10_kkt_lam.txt'):
    p = line.split()
    if len(p) == 2:
        kl[int(p[0])] = mpf(p[1])
print('n kkt lam', len(kl))
lam2 = lam.copy(); lam2[30:961] = LC
d = [abs(mpf(float(lam2[j])) - kl[j]) for j in range(994)]
d0 = [abs(mpf(float(lam[j])) - kl[j]) for j in range(994)]
print('max |lam_verifier(after repl) - lam_KKT| over j<994:', max(d), ' argmax', int(np.argmax([float(x) for x in d])))
print('max |lam_verifier(before repl) - lam_KKT|:', max(d0))
print('l2 norm after repl', sqrt(sum(x*x for x in d)))
print('q range all k=0..995 (q_k=-2 lam_{k-1}, lam_-1=0, q_995=0):', min(-2*float(lam2[k-1]) if 0 <= k-1 < 994 else 0.0 for k in range(996)), max(-2*float(lam2[k-1]) if 0 <= k-1 < 994 else 0.0 for k in range(996)))
