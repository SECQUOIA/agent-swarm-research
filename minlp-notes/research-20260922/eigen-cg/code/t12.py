import numpy as np, itertools, time
from vertices6 import Z6
from sample_search import switch
from linesearch import LineSearch
rng = np.random.default_rng(0)
t = time.time()
res = []
for name, z6 in Z6.items():
    z = np.array(z6) / 6
    for r in range(7):
        for S in itertools.combinations(range(6), r):
            zs = switch(6, z, S)
            ls = LineSearch(6, zs)
            f, v = ls.search(rng, restarts=20, iters=40)
            res.append((f, name, S, None if v is None else v.tolist()))
res.sort(key=lambda r: r[0])
print(time.time() - t)
for r in res[:8]: print(r[:3], np.round(r[3], 4) if r[3] else None)
