from fractions import Fraction as F
from math import lcm

def paper_omega(p):
    n = len(p.b)
    dens = [p.constant.denominator] + [v.denominator for v in p.b]
    dens += [(p.A[i][i] / 2).denominator for i in range(n)]
    dens += [p.A[i][j].denominator for i in range(n) for j in range(i + 1, n)]
    dens += [v.denominator for pair in p.bounds for v in pair]
    D = lcm(*dens)
    R = D
    for i in range(n):
        lo, hi = p.bounds[i]
        if i not in p.integers and p.A[i][i] > 0:   # I_C^+ (paper: i in I_C with H_ii > 0)
            R *= int(D * p.A[i][i])
    return D * R * R

