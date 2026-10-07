"""coreA verifier (second pass): exact check of Lemma lem:dp (grids.tex).

Random factor graphs with random tree decompositions (running intersection by
construction), random grids, random unary corrections d_i, Q = F - D.
Messages are computed as in the text: upward pass with eq:messages, then at
each bag A_t = q_t + sum of all incoming messages, and every downward message
M_{t->u} = min over y_{B_t \\ S_tu} of (A_t - M_{u->t}).
Asserts:
  A_t(y_B) = min{Q(z) : z in G, z_B = y_B} for every bag and every y_B;
  beta = min A_t for every t; m_i(v) = min of A_t over y_i = v for every bag t
  containing i; a minimizer recovered from the root outward attains beta.
Usage: python3 coreA-verify-dp.py [seed] [count]
"""
import itertools
import random
import sys
from fractions import Fraction as Fr


def rand_td(rng, n):
    N = rng.randint(1, 5)
    parent = [None] + [rng.randrange(t) for t in range(1, N)]
    adj = {t: set() for t in range(N)}
    for t in range(1, N):
        adj[t].add(parent[t])
        adj[parent[t]].add(t)
    bags = [set() for _ in range(N)]
    for i in range(n):
        # random connected subtree: grow from a random node
        start = rng.randrange(N)
        sub = {start}
        for _ in range(rng.randint(0, N - 1)):
            cand = [u for t in sub for u in adj[t] if u not in sub]
            if not cand:
                break
            sub.add(rng.choice(cand))
        for t in sub:
            bags[t].add(i)
    return N, adj, [sorted(b) for b in bags]


def run(rng):
    n = rng.randint(1, 5)
    N, adj, bags = rand_td(rng, n)
    # factors: scopes inside random bags; each assigned to a bag containing it
    factors = []
    for _ in range(rng.randint(0, 6)):
        t = rng.randrange(N)
        if not bags[t]:
            continue
        k = rng.randint(1, min(3, len(bags[t])))
        scope = sorted(rng.sample(bags[t], k))
        table = {}
        factors.append((t, scope, table))
    G = [sorted(set(Fr(rng.randint(-4, 4), rng.randint(1, 3)) for _ in range(rng.randint(1, 3)))) for _ in range(n)]
    for (t, scope, table) in factors:
        for y in itertools.product(*[G[i] for i in scope]):
            table[y] = Fr(rng.randint(-9, 9), rng.randint(1, 4))
    d = [{v: Fr(rng.randint(0, 6), rng.randint(1, 4)) for v in G[i]} for i in range(n)]
    home = []
    for i in range(n):
        ts = [t for t in range(N) if i in bags[t]]
        home.append(rng.choice(ts))

    def Q(z):
        s = Fr(0)
        for (t, scope, table) in factors:
            s += table[tuple(z[i] for i in scope)]
        return s - sum(d[i][z[i]] for i in range(n))

    def q(t, yB):  # yB: dict i -> value for i in bags[t]
        s = Fr(0)
        for (tt, scope, table) in factors:
            if tt == t:
                s += table[tuple(yB[i] for i in scope)]
        return s - sum(d[i][yB[i]] for i in range(n) if home[i] == t)

    def assignments(var):
        for vals in itertools.product(*[G[i] for i in var]):
            yield dict(zip(var, vals))

    M = {}

    def sep(t, u):
        return sorted(set(bags[t]) & set(bags[u]))

    def key(var, y):
        return tuple(y[i] for i in var)

    # upward pass (root 0), postorder
    order, stack, par = [], [(0, None)], {0: None}
    while stack:
        t, p = stack.pop()
        order.append(t)
        for u in adj[t]:
            if u != p:
                par[u] = t
                stack.append((u, t))
    for t in reversed(order):
        u = par[t]
        if u is None:
            continue
        S = sep(t, u)
        msg = {}
        for yB in assignments(bags[t]):
            val = q(t, yB) + sum(M[(v, t)][key(sep(v, t), yB)] for v in adj[t] if v != u)
            k = key(S, yB)
            if k not in msg or val < msg[k]:
                msg[k] = val
        M[(t, u)] = msg
    # downward pass: A_t then M_{t->c} from A_t - M_{c->t}
    A = {}
    for t in order:
        A[t] = {}
        for yB in assignments(bags[t]):
            A[t][key(bags[t], yB)] = q(t, yB) + sum(M[(v, t)][key(sep(v, t), yB)] for v in adj[t])
        for c in adj[t]:
            if c == par[t]:
                continue
            S = sep(t, c)
            msg = {}
            for yB in assignments(bags[t]):
                val = A[t][key(bags[t], yB)] - M[(c, t)][key(S, yB)]
                k = key(S, yB)
                if k not in msg or val < msg[k]:
                    msg[k] = val
            M[(t, c)] = msg
    # brute force
    allQ = {z: Q(z) for z in itertools.product(*G)}
    beta = min(allQ.values())
    for t in range(N):
        for yB in assignments(bags[t]):
            bf = min(qq for z, qq in allQ.items() if all(z[i] == yB[i] for i in bags[t]))
            assert A[t][key(bags[t], yB)] == bf, ("A_t", t, yB)
        assert min(A[t].values()) == beta
        for i in bags[t]:
            for v in G[i]:
                mi = min(qq for z, qq in allQ.items() if z[i] == v)
                at = min(val for kk, val in A[t].items() if kk[bags[t].index(i)] == v)
                assert mi == at, ("m_i", i, v)
    # minimizer recovered from the root outward
    z = {}
    for t in order:
        free = [i for i in bags[t] if i not in z]
        best = None
        for vals in itertools.product(*[G[i] for i in free]):
            y = dict(z)
            y.update(zip(free, vals))
            val = A[t][key(bags[t], y)]
            if best is None or val < best[0]:
                best = (val, dict(zip(free, vals)))
        z.update(best[1])
    zz = tuple(z[i] if i in z else G[i][0] for i in range(n))
    # coordinates in no bag do not occur; every coordinate is in some bag here
    assert all(i in z for i in range(n))
    assert allQ[zz] == beta, ("recovered minimizer", allQ[zz], beta)
    return N


if __name__ == "__main__":
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)
    bags_total = 0
    for _ in range(count):
        bags_total += run(rng)
    print(f"lem:dp check passed: {count} instances, {bags_total} bags, seed {seed}")
