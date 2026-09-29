"""Clique (Midpoint Lemma) versus chromatic (parity-colouring) lower bounds on
MICP rank for random finite sets S of integers.

G_S: vertices S, edge {x,y} iff (x+y)/2 is not in S.
Any MICP formulation with d integer variables maps x -> z_x in Z^d; if z_x and z_y
have the same parity then (x+y)/2 is in S.  Hence the parity map properly
colours G_S with 2^d colours:  d >= log2 chi(G_S) >= log2 omega(G_S).
The Midpoint Lemma of Lubin-Zadik-Vielma is the omega version.
chi >= |S| / alpha(G_S), where alpha(G_S) = largest subset whose pairwise
midpoints all lie in S.  Binary formulations give d <= ceil(log2 |S|).
Exact max clique by a small bitset branch-and-bound with greedy-colouring bounds.
"""
import math, random, sys, time


def build(S, want_edge):
    n = len(S)
    adj = [0] * n
    for i in range(n):
        for j in range(n):
            if i != j and want_edge(S[i], S[j]):
                adj[i] |= 1 << j
    return adj


def max_clique(adj):
    n = len(adj)
    best = [0]

    def colour_order(P):
        # greedy colouring of candidate set P; returns vertices with colour bounds
        order, bounds = [], []
        U = P
        c = 0
        while U:
            c += 1
            Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~(1 << v)
                Q &= ~adj[v]
                U &= ~(1 << v)
                order.append(v)
                bounds.append(c)
        return order, bounds

    def expand(R_size, P):
        order, bounds = colour_order(P)
        for k in range(len(order) - 1, -1, -1):
            if R_size + bounds[k] <= best[0]:
                return
            v = order[k]
            newP = P & adj[v]
            if newP:
                expand(R_size + 1, newP)
            elif R_size + 1 > best[0]:
                best[0] = R_size + 1
            P &= ~(1 << v)

    expand(0, (1 << n) - 1)
    return best[0]


def dsatur_colours(adj):
    n = len(adj)
    colour = [-1] * n
    for _ in range(n):
        v = max((u for u in range(n) if colour[u] < 0),
                key=lambda u: (len({colour[w] for w in range(n) if adj[u] >> w & 1 and colour[w] >= 0}),
                               bin(adj[u]).count("1")))
        used = {colour[w] for w in range(n) if adj[v] >> w & 1}
        c = 0
        while c in used:
            c += 1
        colour[v] = c
    return max(colour) + 1


if __name__ == "__main__":
    random.seed(1)
    for N in [40, 80, 120]:
        for trial in range(2):
            S = sorted(x for x in range(N) if random.random() < 0.5)
            Sset = set(S)
            out = lambda x, y: (x + y) % 2 == 1 or (x + y) // 2 not in Sset
            inside = lambda x, y: not out(x, y)
            t0 = time.time()
            omega = max_clique(build(S, out))
            alpha = max_clique(build(S, inside))
            chi_ub = dsatur_colours(build(S, out))
            chi_lb = math.ceil(len(S) / alpha)
            print(f"N={N} |S|={len(S)} omega={omega} alpha={alpha} chi in [{chi_lb},{chi_ub}] | "
                  f"d >= {math.ceil(math.log2(omega))} (midpoint), d >= {math.ceil(math.log2(chi_lb))} (colouring), "
                  f"d <= {math.ceil(math.log2(len(S)))} (binary)  [{time.time()-t0:.1f}s]")
            sys.stdout.flush()
