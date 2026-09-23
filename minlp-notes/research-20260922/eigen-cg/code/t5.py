import itertools
from f3_enum import *
cnt=0
for n in (3,4,5,6):
    found = 0
    for sigma in itertools.combinations_with_replacement([-4,-3,-2,-1,1,2,3,4], n):
        if reduce(gcd, [abs(s) for s in sigma]) != 1: continue
        c = candidates(list(sigma), amax=12)
        if c:
            found += 1
            if found <= 3: print(n, sigma, c[:2])
    print(n, "sigmas with negative f at a non-subset-sum:", found)
