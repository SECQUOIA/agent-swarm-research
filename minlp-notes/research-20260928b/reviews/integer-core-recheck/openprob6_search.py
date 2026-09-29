"""Small random search related to Open problem 6 (not a claim of the note): can iterated
incumbent bound tightening at the root of a 3-D box prune the root (N = 1) while the
midpoint clique number is 8 = 2n + 2 > 2n + 1?  That would violate N >= kappa/(2n+1).
Exact arithmetic; model as in thm18c_counting.py (UB = OPT, early stop)."""
import itertools
import random
import sys
import time
from fractions import Fraction as Fr

from exact import phi
from thm18c_counting import Run, rand_A


def max_clique(adj, nv):
    best = 0

    def rec(R, Pset):
        nonlocal best
        if not Pset:
            best = max(best, len(R))
            return
        if len(R) + len(Pset) <= best:
            return
        for v in list(Pset):
            rec(R + [v], [u for u in Pset if u in adj[v]])
            Pset = [u for u in Pset if u != v]
            if len(R) + len(Pset) <= best:
                return
    rec([], list(range(nv)))
    return best


rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
trials = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
lo0, hi0 = (0, 0, 0), (2, 2, 2)
n = 3
P = [tuple(Fr(v) for v in p) for p in itertools.product(range(3), repeat=3)]
stats = dict(inst=0, root_pruned=0, clique_hist={}, pruned_clique_hist={}, max_steps=0)
t0 = time.time()
for t in range(trials):
    A = rand_A(rng, n)
    c = [Fr(rng.choice([1, 3])) / 2 + Fr(rng.randint(-2, 2), 16) for _ in range(n)]
    y = [sum(A[i][j] * c[j] for j in range(n)) + Fr(rng.randint(-2, 2), 20) for i in range(n)]
    OPT = min(phi(A, y, p) for p in P)
    eps = rng.choice([Fr(0), OPT / 100, OPT / 20])
    tau = OPT - eps
    run = Run(A, y, lo0, hi0, tau, 'iter', rng.sample(range(n), n))
    steps, rl, rh = run.reduce(lo0, hi0)
    pruned = any(l > h for l, h in zip(rl, rh)) or run.certified(rl, rh)
    adj = {i: set() for i in range(len(P))}
    for i, j in itertools.combinations(range(len(P)), 2):
        m = [(a + b) / 2 for a, b in zip(P[i], P[j])]
        if phi(A, y, m) < tau:
            adj[i].add(j)
            adj[j].add(i)
    w = max_clique(adj, len(P))
    stats['inst'] += 1
    stats['clique_hist'][w] = stats['clique_hist'].get(w, 0) + 1
    stats['max_steps'] = max(stats['max_steps'], len(steps))
    if pruned:
        stats['root_pruned'] += 1
        stats['pruned_clique_hist'][w] = stats['pruned_clique_hist'].get(w, 0) + 1
        if w > 2 * n + 1:
            print("VIOLATION CANDIDATE", A, y, eps, steps)
print(f"{stats['inst']} instances on [0,2]^3 ({time.time() - t0:.0f}s): midpoint clique histogram {dict(sorted(stats['clique_hist'].items()))}")
print(f"   root pruned by iterated tightening: {stats['root_pruned']}; clique histogram among those {dict(sorted(stats['pruned_clique_hist'].items()))}")
print(f"   max bound changes at the root: {stats['max_steps']} (2n = {2 * n})")
