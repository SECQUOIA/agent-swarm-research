"""Exact check of the multicolored-clique encoding used for the
kappa^{Omega(p)} lower bound.

Variables (all integer): x_c in [1,N] (c=1..k); for each pair c<d with edge
list R_cd = ((a_1,b_1),...,(a_m,b_m)): zeta_l, S_l in {0,1}, A_l, B_l in [0,N]
(l=1..m), S_0=A_0=B_0=0.
Phi = sum_pairs [ sum_l (S_l-S_{l-1}-zeta_l)^2 + (A_l-A_{l-1}-a_l zeta_l)^2
                  + (B_l-B_{l-1}-b_l zeta_l)^2 + (S_m-1)^2 + (A_m-x_c)^2
                  + (B_m-x_d)^2 ]
Psi = W Phi + sum_pairs sum_l w(e_l) zeta_l,  W = 1 + C(k,2) max w.
Claims checked by an exact min-sum DP with minimizer counting on the stated
tree decomposition:  min Phi = 0 iff a multicolored clique exists; the number
of minimizers of Psi equals the number of minimum-weight cliques; if a clique
exists then Psi* < W, else Psi* >= W; maximum bag size max(k,7).
"""

import random
from itertools import product, combinations


def solve_count(domains, bags, edges, factors):
    """Min-sum with counts.  factors: list of (scope, fn).  Returns (min, count)."""
    nb = len(bags)
    nbr = [[] for _ in range(nb)]
    for u, v in edges:
        nbr[u].append(v)
        nbr[v].append(u)
    home = []
    for scope, fn in factors:
        home.append(next(t for t, bag in enumerate(bags) if set(scope) <= set(bag)))
    parent, order = [-1] * nb, [0]
    seen = {0}
    for u in order:
        for v in nbr[u]:
            if v not in seen:
                seen.add(v)
                parent[v] = u
                order.append(v)
    msgs = {}
    for u in reversed(order):
        bag = bags[u]
        children = [v for v in nbr[u] if parent[v] == u]
        sep = tuple(i for i in bag if parent[u] >= 0 and i in bags[parent[u]])
        out = {}
        for vals in product(*(domains[i] for i in bag)):
            asg = dict(zip(bag, vals))
            cost, cnt = 0, 1
            for (scope, fn), h in zip(factors, home):
                if h == u:
                    cost += fn(*(asg[i] for i in scope))
            for v in children:
                key = tuple(asg[i] for i in bags[v] if i in bag)
                mc, mn = msgs[v][key]
                cost += mc
                cnt *= mn
            key = tuple(asg[i] for i in sep)
            if key not in out or cost < out[key][0]:
                out[key] = (cost, cnt)
            elif cost == out[key][0]:
                out[key] = (cost, out[key][1] + cnt)
        # separator key ordering must match parent lookup: order of bags[u] restricted
        msgs[u] = out
    return msgs[0][()]


def build(k, N, E, w):
    """E: dict (c,d) -> list of (a,b) edges; w: dict ((c,d),(a,b)) -> weight."""
    names = {}
    domains = []

    def var(name, dom):
        names[name] = len(domains)
        domains.append(list(dom))
        return names[name]

    xs = [var(("x", c), range(1, N + 1)) for c in range(k)]
    wmax = max(w.values()) if w else 1
    W = 1 + (k * (k - 1) // 2) * wmax
    bags = [tuple(xs)]
    edges = []
    factorsPhi, factorsTau = [], []
    for (c, d), R in E.items():
        m = len(R)
        S = [None] + [var(("S", c, d, l), (0, 1)) for l in range(1, m + 1)]
        A = [None] + [var(("A", c, d, l), range(N + 1)) for l in range(1, m + 1)]
        B = [None] + [var(("B", c, d, l), range(N + 1)) for l in range(1, m + 1)]
        Z = [None] + [var(("Z", c, d, l), (0, 1)) for l in range(1, m + 1)]
        end = len(bags)
        bags.append((xs[c], xs[d], S[m], A[m], B[m]))
        edges.append((0, end))
        prev = end
        for l in range(m, 0, -1):
            a, b = R[l - 1]
            if l == 1:
                bag = (Z[1], S[1], A[1], B[1])
                factorsPhi.append(((S[1], Z[1]), lambda s, z: (s - z) ** 2))
                factorsPhi.append(((A[1], Z[1]), lambda s, z, a=a: (s - a * z) ** 2))
                factorsPhi.append(((B[1], Z[1]), lambda s, z, b=b: (s - b * z) ** 2))
            else:
                bag = (S[l - 1], A[l - 1], B[l - 1], Z[l], S[l], A[l], B[l])
                factorsPhi.append(((S[l], S[l - 1], Z[l]), lambda s, t, z: (s - t - z) ** 2))
                factorsPhi.append(((A[l], A[l - 1], Z[l]), lambda s, t, z, a=a: (s - t - a * z) ** 2))
                factorsPhi.append(((B[l], B[l - 1], Z[l]), lambda s, t, z, b=b: (s - t - b * z) ** 2))
            factorsTau.append(((Z[l],), lambda z, ww=w[((c, d), (a, b))]: ww * z))
            idx = len(bags)
            bags.append(bag)
            edges.append((prev, idx))
            prev = idx
        factorsPhi.append(((S[m],), lambda s: (s - 1) ** 2))
        factorsPhi.append(((A[m], xs[c]), lambda s, x: (s - x) ** 2))
        factorsPhi.append(((B[m], xs[d]), lambda s, x: (s - x) ** 2))
    return domains, bags, edges, factorsPhi, factorsTau, W


def main():
    rng = random.Random(5)
    checked = {"instances": 0, "yes": 0, "no": 0, "unique_cases": 0}
    for trial in range(14):
        k, N = 3, rng.choice([2, 3])
        E = {}
        for c, d in combinations(range(k), 2):
            E[(c, d)] = [(a, b) for a in range(1, N + 1) for b in range(1, N + 1) if rng.random() < 0.4]
            if not E[(c, d)]:
                E[(c, d)] = [(1, 1)]
        allE = [(cd, ab) for cd, R in E.items() for ab in R]
        R_w = 2 * len(allE)
        w = {e: rng.randint(1, R_w) for e in allE}
        domains, bags, edges, fP, fT, W = build(k, N, E, w)
        assert max(len(b) for b in bags) <= max(k, 7)
        phi_min, _ = solve_count(domains, bags, edges, fP)
        psi_f = [(s, (lambda f: (lambda *a: W * f(*a)))(f)) for s, f in fP] + fT
        psi_min, psi_cnt = solve_count(domains, bags, edges, psi_f)
        cliques = [xs for xs in product(range(1, N + 1), repeat=k)
                   if all((xs[c], xs[d]) in E[(c, d)] for c, d in combinations(range(k), 2))]
        assert (phi_min == 0) == bool(cliques)
        if cliques:
            weights = [sum(w[((c, d), (xs[c], xs[d]))] for c, d in combinations(range(k), 2)) for xs in cliques]
            best = min(weights)
            assert psi_min == best < W
            assert psi_cnt == weights.count(best)
            checked["yes"] += 1
            checked["unique_cases"] += int(psi_cnt == 1)
        else:
            assert psi_min >= W
            checked["no"] += 1
        checked["instances"] += 1
    print(checked)


if __name__ == "__main__":
    main()
