"""Independent finite arithmetic checks, not a proof of the universal claims.

Run with a Python providing NumPy. All identities and localizer entries use
Fraction; only the final eigenvalue checks use floating point.
"""
from fractions import Fraction as F
from functools import cache
from itertools import combinations, product
from math import comb
import json
import numpy as np


def fall(x, n):
    ans = F(1)
    for j in range(n):
        ans *= x - j
    return ans


def moment(s, t, n):
    return fall(t, n) / fall(s, n)


def subsets(mask):
    sub = mask
    while True:
        yield sub
        if not sub:
            break
        sub = (sub - 1) & mask


@cache
def local(s, t, a, b, c):
    # Direct expansion of u_A (1-u)_B u_C in the Boolean quotient.
    if (a | c) & b:
        return F(0)
    return sum((-1) ** j.bit_count() * moment(s, t, (a | c | j).bit_count())
               for j in subsets(b))


gram_count = balance_count = conditional_count = 0
for d in range(1, 5):
    for s in range(max(2*d, 4*d-2), max(2*d, 4*d-2)+5):
        for t2 in range(2*(2*d-1), 2*(s-(2*d-1))+1):
            t = F(t2, 2)
            for overlap in range(d+1):
                lhs = moment(s, t, 2*d-overlap)
                rhs = sum(fall(t, 2*d-j)*fall(s-t, j)/fall(s, 2*d)
                          * comb(overlap, j) for j in range(overlap+1))
                assert lhs == rhs
                gram_count += 1
            for a in range(2*d):
                assert a*moment(s, t, a)+(s-a)*moment(s, t, a+1) == t*moment(s, t, a)
                balance_count += 1
            for a in range(2*d+1):
                for b in range(2*d+1-a):
                    amask = (1 << a)-1
                    bmask = ((1 << b)-1) << a
                    pi = fall(t,a)*fall(s-t,b)/fall(s,a+b)
                    assert pi >= 0
                    for c in range(2*d+1-a-b):
                        cmask = ((1 << c)-1) << (a+b)
                        rhs = pi * (moment(s-a-b,t-a,c) if c else 1)
                        assert local(s,t,amask,bmask,cmask) == rhs
                        conditional_count += 1


def mons(n, d):
    return [sum(1 << i for i in inds)
            for k in range(d+1) for inds in combinations(range(n),k)]


eigen_count = 0
worst_eigenvalue = 0.0
largest_matrix = 0
for r, s, t in [(1, 2, F(1)), (1, 4, F(3,2)),
                (2, 6, F(3)), (2, 8, F(7,2))]:
    blockmask = (1 << s)-1
    for a1,b1,a2,b2 in product(range(2*r+1),repeat=4):
        v = a1+b1+a2+b2
        if v > 2*r or a1+b1>s or a2+b2>s:
            continue
        d = (2*r-v)//2
        indices = mons(2*s,d)
        assignments = [((1 << a)-1, ((1 << b)-1) << a)
                       for a,b in [(a1,b1),(a2,b2)]]
        matrix = np.empty((len(indices),len(indices)))
        for i, alpha in enumerate(indices):
            for j in range(i+1):
                union = alpha | indices[j]
                entry = (local(s,t,*assignments[0],union & blockmask)
                         * local(s,t,*assignments[1],union >> s))
                matrix[i,j] = matrix[j,i] = float(entry)
        minimum = float(np.linalg.eigvalsh(matrix)[0])
        assert minimum >= -1e-10, (r,s,t,assignments,minimum)
        eigen_count += 1
        largest_matrix = max(largest_matrix,len(indices))
        worst_eigenvalue = min(worst_eigenvalue,minimum)

# The full preordering really needs more than square positivity alone.
negative_assignment = local(8,F(5,2),15,0,0)
assert negative_assignment == F(-1,1792)

print(json.dumps({
    "exact_gram_entry_identities":gram_count,
    "exact_balance_identities":balance_count,
    "exact_conditional_moment_identities":conditional_count,
    "two_block_localizer_psd_checks":eigen_count,
    "largest_total_degree_matrix":largest_matrix,
    "minimum_floating_eigenvalue":worst_eigenvalue,
    "negative_four_slack_boundary_example":str(negative_assignment),
    "note":"Finite diagnostics only; PSD eigenvalues are numerical."
},indent=2))
