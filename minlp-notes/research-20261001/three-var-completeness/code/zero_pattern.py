import numpy as np
from cube3 import *

def zeros(pvec, tol=1e-6):
    p = quad_from_vector(pvec)
    res = []
    for status, x, v in face_minimizers(p, tol=1e-9):
        if abs(v) < tol:
            res.append((status, np.round(x, 4).tolist()))
    return res

def pattern(pvec, tol=1e-6):
    z = zeros(pvec, tol)
    dims = [sum(1 for s in st if s == -1) for st, _ in z]
    return tuple(sorted(dims)), z

def rank_info(pvec):
    P = hom_matrix(quad_from_vector(pvec))
    ev = np.linalg.eigvalsh(P)
    return ev
