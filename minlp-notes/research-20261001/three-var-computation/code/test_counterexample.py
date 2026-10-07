"""Check the relaxations on the counterexample objective p of research-20260925."""
import sys; sys.path.insert(0, '.')
import numpy as np
from n3_study import build
# p = x^2+y^2+9z^2+6xy-12xz-12yz-x-y+9z+1/4
H = np.array([[1, 3, -6], [3, 1, -6], [-6, -6, 9]], float)
g = np.array([-1, -1, 9], float)
for parts in ['', 'K', 'A', 'KA', 'F', 'KAF', 'X']:
    R = build(H, g, parts)
    r = R.solve('clarabel', tol=1e-10)
    print('%-4s bound %.8f safe %.8f %s' % (parts or 'B', r['pobj'] + 0.25, r['safe'] + 0.25, r['status']))
