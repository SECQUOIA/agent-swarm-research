import numpy as np, json
from screen2 import analyze
from fractions import Fraction as Fr
I = {'8459': ([-4.5, 0, 1.5], [-1, -6, 18], [-5, 6, -18], [0, 2.5, 2.5]),
     'bigA': ([-.5, .5, 1], [.5, -4, -.5], [-10, 3, 24], [4.5, .5, 7.5])}
for k, (sb, a, b, c) in I.items():
    sb = np.array(sb, float); P = np.stack([np.array(v, float) - sb for v in (a, b, c)], 1)
    print(k, end=' ', flush=True)
    analyze('+', sb, P, np.ones(3), nm_restarts=30, seed=1)
