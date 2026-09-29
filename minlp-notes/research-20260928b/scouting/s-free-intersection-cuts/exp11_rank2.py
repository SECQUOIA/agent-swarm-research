"""E11: rank of the (Balas cone-based) intersection closure.  P = triangle a=(0,2), u=(-.5,0), u'=(.5,0),
S = {x : ||x|| >= 1} (reverse convex; unique maximal S-free set = unit disk).  Rank-1 closure
(cuts at the two vertices inside the disk) strictly contains conv(P cap S); rank 2 equals it."""
import numpy as np
a, u, up = np.array([0, 2.]), np.array([-.5, 0]), np.array([.5, 0])
def exit_disk(p, d):  # largest t with ||p + t d|| <= 1 (p inside disk)
    A, B, C = d @ d, 2 * p @ d, p @ p - 1
    return (-B + np.sqrt(B * B - 4 * A * C)) / (2 * A)
p1 = u + exit_disk(u, a - u) * (a - u); e1 = u + exit_disk(u, up - u) * (up - u)
p2 = up + exit_disk(up, a - up) * (a - up); e2 = up + exit_disk(up, u - up) * (u - up)
# intersection X of line p1-e1 and line p2-e2
M = np.array([e1 - p1, -(e2 - p2)]).T; st = np.linalg.solve(M, p2 - p1); X = p1 + st[0] * (e1 - p1)
print('p1', p1.round(4), 'p2', p2.round(4), 'X', X.round(4), '|X|', round(np.linalg.norm(X), 4))
print('chord p1p2 height', round(p1[1], 4), '-> X below chord, so X in rank-1 closure but not in conv(P cap S):', X[1] < p1[1])
# rank 2: at X the two edges point to p1 and p2, both on the unit circle -> cut is the chord p1p2
print('X->p1 exit param', round(exit_disk(X, p1 - X), 6), ' X->p2 exit param', round(exit_disk(X, p2 - X), 6), '(1 means exits exactly at p_i)')
