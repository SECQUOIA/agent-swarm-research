import itertools, time, sys
from f3_enum import *
from bh import PBH
from perturb_milp import PerturbSearch
P = PBH(6, W0=1)
S = PerturbSearch(P)
t = time.time()
R = int(sys.argv[1]) if len(sys.argv) > 1 else 3
nb = 0; hits = []
res_all = []
for sigma in itertools.combinations_with_replacement([k for k in range(-R, R+1) if k], 6):
    if reduce(gcd, [abs(x) for x in sigma]) != 1: continue
    g = reduce(gcd, [abs(sigma[i]*sigma[j]) for i in range(6) for j in range(i+1, 6)])
    S_ = subset_sums(sigma)
    for m_ in range(1, 25):
        a = Fr(m_, 2*g)
        b0 = b_coset(list(sigma), a)
        if b0 is None: continue
        lo, hi = min(S_) - 2, max(S_) + 2
        for k in range(math.floor(-2*a*hi - b0) - 1, math.ceil(-2*a*lo - b0) + 2):
            b = b0 + k
            v02 = b*b/(4*a)
            if v02.denominator != 1 or v02 == 0: continue
            nb += 1
            r = S.run(list(sigma), a, b, int(v02))
            res_all.append((r[0] if r else None, sigma, a, b))
            if r and r[1] is not None:
                hits.append((sigma, a, b, r)); print("HIT", sigma, a, b, r, flush=True)
print("bases", nb, "hits", len(hits), time.time()-t)
vals = sorted([x for x in res_all if x[0] is not None], key=lambda x: x[0])
print(vals[:5])
