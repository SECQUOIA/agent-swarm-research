"""Independent exact finite checks. These supplement, not replace, proof review."""
from itertools import product
from random import Random
import json
from pathlib import Path
import sympy as sp

rng = Random(202609092)
counts = {}

def divergence(n, edges, w):
    d = [0] * n
    for (u, v), value in zip(edges, w):
        d[u] += value
        d[v] -= value
    return tuple(d)

def flow_checks():
    feasible_count = 0
    for test in range(160):
        n = rng.randrange(1, 7)
        # Both degree-two graphs and small unrestricted directed graphs.
        edges = [(i, i + 1) for i in range(n - 1)]
        if n > 2 and test % 3 == 0:
            edges.append((n - 1, 0))
        elif n > 3 and test % 3 == 1:
            edges.append((0, 2))
        edges = [(u, v) if rng.randrange(2) else (v, u) for u, v in edges]
        lo = [rng.randrange(-2, 2) for _ in edges]
        hi = [v + rng.randrange(3) for v in lo]
        all_d = {divergence(n, edges, w) for w in product(*[range(l, u + 1) for l, u in zip(lo, hi)])}
        if test % 2 == 0:
            base = rng.choice(sorted(all_d))
            alpha = [v - rng.randrange(3) for v in base]
            beta = [v + rng.randrange(3) for v in base]
        else:
            alpha = [rng.randrange(-3, 4) for _ in range(n)]
            beta = [v + rng.randrange(3) for v in alpha]
        feasible = {d for d in all_d if all(a <= v <= b for a, v, b in zip(alpha, d, beta))}
        sets = [set(i for i in range(n) if mask & (1 << i)) for mask in range(1 << n)]
        def f(S):
            return sum(u for (tail, head), u in zip(edges, hi) if tail in S and head not in S) - sum(l for (tail, head), l in zip(edges, lo) if tail not in S and head in S)
        def low_cut(S):
            return sum(l for (tail, head), l in zip(edges, lo) if tail in S and head not in S) - sum(u for (tail, head), u in zip(edges, hi) if tail not in S and head in S)
        def cut_ok(S):
            return sum(alpha[v] for v in S) <= f(S) and sum(beta[v] for v in S) >= low_cut(S)
        assert all(map(cut_ok, sets)) == bool(feasible)
        def connected(S):
            if not S:
                return False
            reached = {min(S)}
            while True:
                new = reached | {v for u, v in edges if u in reached and v in S} | {u for u, v in edges if v in reached and u in S}
                if new == reached:
                    return reached == S
                reached = new
        assert all(cut_ok(S) for S in sets if connected(S)) == bool(feasible)
        if not feasible:
            continue
        feasible_count += 1
        g = {frozenset(S): min(f(T) + sum(beta[v] for v in S - T) - sum(alpha[v] for v in T - S) for T in sets) for S in sets}
        assert g[frozenset()] == g[frozenset(range(n))] == 0
        for S in sets:
            # Integral bounded network polytope: integer enumeration contains
            # every vertex, so these are exact real support extrema too.
            assert g[frozenset(S)] == max(sum(d[v] for v in S) for d in feasible)
            for T in sets:
                assert g[frozenset(S)] + g[frozenset(T)] >= g[frozenset(S | T)] + g[frozenset(S & T)]
        for _ in range(4):
            costs = [rng.randrange(-4, 5) for _ in range(n)]
            order = sorted(range(n), key=lambda v: -costs[v])
            dstar = [0] * n
            S = frozenset()
            for v in order:
                nxt = S | {v}
                dstar[v] = g[nxt] - g[S]
                S = nxt
            assert tuple(dstar) in feasible
            assert sum(c * d for c, d in zip(costs, dstar)) == max(sum(c * v for c, v in zip(costs, d)) for d in feasible)
    counts['signed_cut_instances'] = 160
    counts['nonempty_box_rank_instances'] = feasible_count
    counts['greedy_cost_vectors'] = feasible_count * 4

def clamp_checks():
    for test in range(300):
        n = rng.randrange(1, 10)
        unary = [[rng.randrange(-6, 7), rng.randrange(-6, 7)] for _ in range(n)]
        a = [rng.randrange(6) for _ in range(n)]
        b = [rng.randrange(6) for _ in range(n)]
        E0 = unary[0][0]
        D = unary[0][1] - unary[0][0]
        P = D
        Z = 0
        endpoints = {0}
        for i in range(1, n):
            u = unary[i][1] - unary[i][0]
            E0 += unary[i][0] + min(0, D + b[i])
            low, high = -b[i] - P, a[i] - P
            endpoints.update([low, high])
            Z = max(low, min(Z, high))
            D = u + max(-b[i], min(D, a[i]))
            P += u
            assert D - P == Z and Z in endpoints
        dp_value = E0 + min(0, D)
        def energy(x):
            return sum(unary[i][x[i]] for i in range(n)) + sum(a[i] * (x[i-1] == 0 and x[i] == 1) + b[i] * (x[i-1] == 1 and x[i] == 0) for i in range(1, n))
        assert dp_value == min(map(energy, product([0, 1], repeat=n)))
    counts['clamp_path_instances'] = 300

def symbolic_checks():
    q, c1, c2, B, b, z1, z2 = sp.symbols('q c1 c2 B b z1 z2')
    R = b * (B-q)
    w1 = (c1-q)*(R-(c2-q)*(z1+z2))/(c1-c2)
    residual = (c1-q)*z1+(c2-q)*z2-R
    assert sp.factor(w1-(c1-q)*z1) == sp.factor(-(c1-q)*residual/(c1-c2))
    C1h,C2h,qh,Bh,g1,g2 = sp.symbols('C1h C2h qh Bh g1 g2')
    # gamma_i=projected C_i - projected q, projected B=B.
    ah = (C1h-qh)*(c2-q)-(C2h-qh)*(c1-q)
    fh = (c1-q)*(b*(Bh-qh)*(c2-q)-(C2h-qh)*R)
    assert sp.Poly(ah,q,qh).total_degree() <= 1
    assert sp.Poly(fh,q,qh).total_degree() <= 2
    w = sp.symbols('w')
    ambient = (C1h-qh)*w/(c1-q) + (C2h-qh)*(R-w)/(c2-q)-b*(Bh-qh)
    assert sp.cancel(ambient*(c1-q)*(c2-q)-(ah*w-fh)) == 0
    W0,W1 = sp.symbols('W0 W1')
    v = b + W0/q - W1/(1-q)
    assert sp.factor(W0-q*b*(B-1)-q*(1-q)*v) == sp.factor(q*(W0+W1-b*(B-q)))
    rho = sp.symbols('rho', positive=True)
    lam = rho/(2*(rho+1))
    assert sp.simplify(-rho+lam*(rho+1)+rho/2) == 0
    counts['symbolic_identity_groups'] = 5

flow_checks()
clamp_checks()
symbolic_checks()
result = {'status':'all checks passed', 'seed':202609092, 'counts':counts, 'limits':'Finite exact diagnostics and symbolic identities; not a proof of asymptotic complexity or a full algorithm implementation.'}
Path(__file__).with_name('results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
