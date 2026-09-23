import itertools, time
from f3_enum import *
from bh import PBH
P = PBH(6, W0=1)
t = time.time()
worst = []
for sigma in itertools.combinations_with_replacement([-4,-3,-2,-1,1,2,3,4], 6):
    if reduce(gcd, [abs(s) for s in sigma]) != 1: continue
    for (a, b, c, bad) in candidates(list(sigma), amax=12):
        coef, const = ecg_from_abc(list(sigma), a, b, c)
        val, z = P.minimize(coef)
        worst.append((val + const, sigma, a, b, c, bad))
worst.sort(key=lambda r: r[0])
print(len(worst), time.time() - t)
for r in worst[:10]: print(r)
