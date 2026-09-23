import time, numpy as np
from bh import *
from facets import *
from ecgsep import separate_ecg
P = PBH(6, W0=1)
for s in (F13, F14, F15):
    a, c = parse(s)
    val, z = P.minimize(a)
    z = np.round(z*6)/6
    t=time.time()
    ob, bd, sols = separate_ecg(6, z, V=4, timelimit=120)
    print("facet min", val+c, "ECG sep obj", ob, "bound", bd, time.time()-t)
    if sols: print(sols[0])
