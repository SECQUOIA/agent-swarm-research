import time, numpy as np
from bh import *
from facets import *
t=time.time()
P = PBH(6, W0=1)
print(len(P.keys), time.time()-t)
for s in (F13, F14, F15):
    a, c = parse(s)
    val, z = P.minimize(a, verbose=True)
    print("min", val + c, "z=", np.round(z, 4), time.time()-t)
