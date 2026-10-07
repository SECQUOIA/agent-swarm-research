"""Reviewer r1: independent depth of the deepest audit triples (six-tetrahedron primal lift)."""
import json, os, sys, warnings
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lift_depth import lift_depth
warnings.filterwarnings('ignore')
L = 'logs/spar_audit/'
cases = {'spar090-075-1': [35, 79, 84], 'spar100-050-1': [26, 34, 91], 'spar100-050-2': [38, 60, 91],
         'spar125-050-1': [22, 40, 48]}
for name, T in cases.items():
    z = np.load(L + name + '.json.base.npz'); x, Y = z['x'], z['Y']
    d = np.load(L + name + '.json.depth.npz')['depths']
    M = np.empty((4, 4)); M[0, 0] = 1; M[0, 1:] = M[1:, 0] = x[T]; M[1:, 1:] = Y[np.ix_(T, T)]
    i, j, k = T
    tv = max(Y[i, j] + Y[i, k] - x[i] - Y[j, k], Y[i, j] + Y[j, k] - x[j] - Y[i, k],
             Y[i, k] + Y[j, k] - x[k] - Y[i, j], x[i] + x[j] + x[k] - Y[i, j] - Y[i, k] - Y[j, k] - 1)
    ld, st = lift_depth(M)
    print(json.dumps({'name': name, 'triple': T, 'stream_min_depth': float(d.min()), 'lift_depth': ld,
                      'status': st, 'minus_4x_triangle_violation': -4 * tv}))
