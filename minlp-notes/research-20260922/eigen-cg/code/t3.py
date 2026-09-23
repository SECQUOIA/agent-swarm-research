import numpy as np, sympy as sp
from bh import *
from facets import *
P = PBH(6, W0=1)
for s in (F13, F14, F15):
    a, c = parse(s)
    val, z = P.minimize(a)
    z6 = np.round(z*6).astype(int)
    print("6z =", z6.tolist())
    M = sp.Matrix(moment_matrix(6, z6/6.0)*6).applyfunc(lambda t: sp.Integer(round(t)))/6
    print(" eig", np.round(np.linalg.eigvalsh(np.array(M, dtype=float)),4), "rank", M.rank())
    print(" kernel", [list(k) for k in M.nullspace()])
