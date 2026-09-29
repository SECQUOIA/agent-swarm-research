"""Exp 14: linear edge costs, crossing gadget at a square vertex: basic REL < OPT = REL_hull."""
import numpy as np
from gcs import *
sets = {'s': ('point', [0., 0.]), 'u1': ('point', [0., 0.]), 'u2': ('point', [0., 0.]),
        'v': ('box', [-1., -1.], [1., 1.]), 'w1': ('point', [0., 0.]), 'w2': ('point', [0., 0.]), 't': ('point', [0., 0.])}
E = [('s','u1'), ('s','u2'), ('u1','v'), ('u2','v'), ('v','w1'), ('v','w2'), ('w1','t'), ('w2','t')]
I = Inst(sets, E, 's', 't', 2); I.norm = 'lin'
Z = np.zeros(2)
I.lin = {e: (Z, Z) for e in E}
I.lin[('u1','v')] = (Z, -np.array([1., 1.])); I.lin[('u2','v')] = (Z, np.array([1., 1.]))
I.lin[('v','w1')] = (-np.array([1., -1.]), Z); I.lin[('v','w2')] = (np.array([1., -1.]), Z)
print("REL", relax(I), "REL_hull", relax(I, hull=True), "OPT", exact(I))
