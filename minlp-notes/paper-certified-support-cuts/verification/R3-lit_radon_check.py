"""R3-lit: sanity check that Theorem alternation (finite case) coincides with the
classical Radon-partition criterion for points on the moment curve:
conv(gamma_k(A)) and conv(gamma_k(C)) intersect  <=>  alt(A,C) >= k+1.
Exact LP feasibility via scipy (floating point, small integer data, generic)."""
import itertools, random
import numpy as np
from scipy.optimize import linprog

def alt(A, C):
    pts = sorted([(a, 0) for a in A] + [(c, 1) for c in C])
    # longest alternating subsequence length minus 1
    r, last = 0, pts[0][1]
    for _, lab in pts[1:]:
        if lab != last:
            r += 1; last = lab
    return r

def hulls_meet(A, C, k):
    # variables: lambda (|A|), mu (|C|) >= 0; sum lambda = sum mu = 1; moments 1..k equal
    nA, nC = len(A), len(C)
    Aeq, beq = [], []
    Aeq.append([1]*nA + [0]*nC); beq.append(1)
    Aeq.append([0]*nA + [1]*nC); beq.append(1)
    for j in range(1, k+1):
        Aeq.append([a**j for a in A] + [-(c**j) for c in C]); beq.append(0)
    res = linprog(np.zeros(nA+nC), A_eq=np.array(Aeq, float), b_eq=np.array(beq, float),
                  bounds=[(0, None)]*(nA+nC), method="highs")
    return res.status == 0

random.seed(1)
bad = 0; total = 0
for trial in range(3000):
    k = random.randint(1, 4)
    pool = random.sample(range(0, 12), random.randint(2, 8))
    split = random.randint(1, len(pool)-1)
    A, C = pool[:split], pool[split:]
    lhs = hulls_meet(A, C, k); rhs = alt(A, C) >= k+1
    total += 1
    if lhs != rhs:
        bad += 1
        print("MISMATCH", k, sorted(A), sorted(C), lhs, rhs)
print("checked", total, "mismatches", bad)
