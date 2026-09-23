import numpy as np, itertools, time
from bh import *
from facets import *
from sample_search import *
P = PBH(6, W0=1)
pts = []
for s in (F13, F14, F15):
    a, c = parse(s)
    val, z = P.minimize(a)
    pts.append(np.round(z*6)/6)
rng = np.random.default_rng(0)
t=time.time()
overall = []
for pi, z in enumerate(pts):
    for r in range(7):
        for S in itertools.combinations(range(6), r):
            zs = switch(6, z, S)
            b, v = search(6, zs, N=200000, rounds=5, rng=rng)
            overall.append((b, pi, S))
overall.sort(key=lambda t: t[0])
print(overall[:10], time.time()-t)
