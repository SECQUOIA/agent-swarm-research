"""Exact algorithm for one core coordinate with sign-consistent couplings.

F(v, y) = q(v) + E0(y) + v * beta . y, v in [0,1], y binary, E0 submodular
(pairwise w_ij <= 0), beta <= 0.  The recursion over minimal minimizers
(nested by Topkis' monotonicity) needs at most 2r+1 cut queries; here a
brute-force 'cut' returns the minimal minimizer.  Compared with brute force.
"""
import random
from fractions import Fraction as Fr
from itertools import product

def make(rng, r):
    mu = [Fr(rng.randint(-12, 12), rng.randint(1, 4)) for _ in range(r)]
    beta = [-Fr(rng.randint(0, 12), rng.randint(1, 4)) for _ in range(r)]
    w = {(i, j): -Fr(rng.randint(0, 8), rng.randint(1, 3)) for i in range(r) for j in range(i + 1, r) if rng.random() < 0.6}
    qa, qb = Fr(rng.randint(-6, 12), rng.randint(1, 3)), Fr(rng.randint(-12, 12), rng.randint(1, 3))
    return mu, beta, w, qa, qb

def E0(inst, S):
    mu, beta, w, qa, qb = inst
    return sum(mu[i] for i in S) + sum(wij for (i, j), wij in w.items() if i in S and j in S)

def B(inst, S):
    return sum(inst[1][i] for i in S)

def min_minimizer(inst, v, r):
    vals = {}
    for y in product((0, 1), repeat=r):
        S = frozenset(i for i in range(r) if y[i])
        vals[S] = E0(inst, S) + v * B(inst, S)
    m = min(vals.values())
    opt = [S for S, x in vals.items() if x == m]
    inter = frozenset.intersection(*opt)
    assert inter in opt
    return inter, m

def explore(inst, r, a, b, P, Q, found, calls):
    lP = lambda v: E0(inst, P) + v * B(inst, P)
    lQ = lambda v: E0(inst, Q) + v * B(inst, Q)
    if P == Q:
        return
    dB = B(inst, P) - B(inst, Q)
    if dB == 0:
        return  # parallel lines; both optimal on [a,b]
    vm = (E0(inst, Q) - E0(inst, P)) / dB
    if not (a < vm < b):
        return
    Sm, phi = min_minimizer(inst, vm, r); calls[0] += 1
    if phi == lP(vm):
        return
    assert P <= Sm <= Q and Sm not in (P, Q)
    found.add(Sm)
    explore(inst, r, a, vm, P, Sm, found, calls)
    explore(inst, r, vm, b, Sm, Q, found, calls)

def quad_min(qa, qb, c0, c1):
    # min over v in [0,1] of qa v^2 + qb v + c0 + c1 v
    cands = [Fr(0), Fr(1)]
    lin = qb + c1
    if qa > 0:
        v = -lin / (2 * qa)
        if 0 <= v <= 1:
            cands.append(v)
    return min(qa * v * v + lin * v + c0 for v in cands)

def run(rng, trials=200):
    worst_calls = 0
    for _ in range(trials):
        r = rng.randint(1, 6)
        inst = make(rng, r)
        mu, beta, w, qa, qb = inst
        calls = [2]
        S0, _ = min_minimizer(inst, Fr(0), r); S1, _ = min_minimizer(inst, Fr(1), r)
        found = {S0, S1}
        explore(inst, r, Fr(0), Fr(1), S0, S1, found, calls)
        assert len(found) <= r + 1 and calls[0] <= 2 * r + 1
        alg = min(quad_min(qa, qb, E0(inst, S), B(inst, S)) for S in found)
        brute = min(quad_min(qa, qb, E0(inst, frozenset(i for i in range(r) if y[i])),
                             B(inst, frozenset(i for i in range(r) if y[i])))
                    for y in product((0, 1), repeat=r))
        assert alg == brute, (alg, brute)
        worst_calls = max(worst_calls, calls[0] / (2 * r + 1))
    return worst_calls

if __name__ == "__main__":
    rng = random.Random(31)
    wc = run(rng)
    print("k=1 sign-consistent exact recursion matched brute force on 200 instances; max calls/(2r+1) = %.3f" % wc)
    print("ALL K1 CHECKS PASSED")
