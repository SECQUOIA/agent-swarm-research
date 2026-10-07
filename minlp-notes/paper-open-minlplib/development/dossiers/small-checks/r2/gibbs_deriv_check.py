"""numerical check of the closed-form gradient/Hessian in gibbs_cert.py against central differences (60 digits)"""
import sys
name = sys.argv[1]
sys.argv = ['x', name]
src = open('gibbs_cert.py').read()
exec(src[:src.index('t0 = time.time()')])
iv.dps = 60
mp.dps = 60
F = Fn(phase_atoms[0], lam_str)
def Dmp(a, b):
    return mpmath.mpf(F.D(iv.mpf(a), iv.mpf(b), 1 - iv.mpf(a) - iv.mpf(b)).mid)
worst = 0
h1, h2 = mpmath.mpf('1e-18'), mpmath.mpf('1e-12')
for (y1, y2) in [('0.3', '0.2'), ('0.02', '0.003'), ('0.6', '0.39'), ('1e-5', '0.5'), ('0.0567', '6e-7')]:
    y1, y2 = mpmath.mpf(y1), mpmath.mpf(y2)
    _, gr, (a11, a12, a22) = F.D(iv.mpf(y1), iv.mpf(y2), 1 - iv.mpf(y1) - iv.mpf(y2), 2)
    h2b = min(h2, y2 / 1000, y1 / 1000)
    num = [(Dmp(y1 + h1, y2) - Dmp(y1 - h1, y2)) / (2 * h1),
           (Dmp(y1, y2 + h1) - Dmp(y1, y2 - h1)) / (2 * h1),
           (Dmp(y1 + h2b, y2) - 2 * Dmp(y1, y2) + Dmp(y1 - h2b, y2)) / h2b**2,
           (Dmp(y1 + h2b, y2 + h2b) - Dmp(y1 + h2b, y2 - h2b) - Dmp(y1 - h2b, y2 + h2b) + Dmp(y1 - h2b, y2 - h2b)) / (4 * h2b**2),
           (Dmp(y1, y2 + h2b) - 2 * Dmp(y1, y2) + Dmp(y1, y2 - h2b)) / h2b**2]
    ana = [mpmath.mpf(x.mid) for x in (gr[0], gr[1], a11, a12, a22)]
    rel = max(abs(a - b) / (1 + abs(b)) for a, b in zip(ana, num))
    worst = max(worst, rel)
    print(name, mpmath.nstr(y1, 3), mpmath.nstr(y2, 3), 'max rel diff %s' % mpmath.nstr(rel, 3))
print('worst', mpmath.nstr(worst, 3))
