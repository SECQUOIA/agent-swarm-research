#!/usr/bin/env python3
"""Exact diagnostics for new directional sensitivity bounds, not universal proofs."""
from fractions import Fraction as F
from itertools import product, combinations
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def law(x, plus, minus):
    return plus*x*x if x >= 0 else -minus*x*x


def solve(matrix, rhs):
    a = [list(row)+[b] for row, b in zip(matrix, rhs)]
    n = len(a)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        divisor = a[k][k]
        a[k] = [x/divisor for x in a[k]]
        for i in range(n):
            if i != k:
                factor = a[i][k]
                a[i] = [x-factor*y for x, y in zip(a[i], a[k])]
    return [row[-1] for row in a]


def main():
    scalar = 0
    coefficients = [F(1, 9), F(1), F(7, 3)]
    for x, h, bp, bm in product([F(i, 6) for i in range(-12, 13)],
                                [F(i, 7) for i in range(1, 15)],
                                coefficients, coefficients):
        low = min(bp, bm)
        increment = law(x+h, bp, bm)-law(x, bp, bm)
        require(increment >= low*h*abs(x)/2, 'directional scalar inequality')
        require(increment > 0, 'strict scalar increment')
        require(law(-x, bm, bp) == -law(x, bp, bm), 'orientation swaps coefficients')
        scalar += 1

    # Exactly physical states with common nomination (2,-1,-1); the last
    # edge crosses zero. Its directional coefficients are different.
    edges = [(0, 1), (0, 2), (1, 2)]
    states = []
    for s in [F(i, 40) for i in range(-10, 11)]:
        x = [1+s, 1-s, s]
        pi = [F(2), law(s, F(2), F(3)), F(0)]
        bp = [(pi[0]-pi[1])/x[0]**2, pi[0]/x[1]**2, F(2)]
        bm = [F(4)+s, F(5)-s, F(3)]
        require(min(bp+bm) > 0, 'positive directional coefficients')
        require([x[0]+x[1], -x[0]+x[2], -x[1]-x[2]] == [2,-1,-1], 'conservation')
        for e, (u, v) in enumerate(edges):
            require(law(x[e], bp[e], bm[e]) == pi[u]-pi[v], 'physical directional law')
        states.append((x, pi, bp, bm))
    physical = crossing = zero = 0
    for (x, pi, bp, bm), (y, pj, ap, am) in product(states, repeat=2):
        low = min(bp+bm+ap+am)
        q = [max(abs(a-b), abs(c-d)) for a,b,c,d in zip(bp,ap,bm,am)]
        difference = max(abs(a-b) for a,b in zip(x,y))
        require(difference <= F(2)*sum(q)/(2*low), 'sharper directional finite bound')
        require(difference <= 2*3*2*max(q)/low, 'elementary circulation bound')
        crossing += int(x[2]*y[2] < 0)
        zero += int(x[2] == 0 or y[2] == 0)
        physical += 1

    # Independent exact Laplacian solves check the differentiated equations,
    # each electrical response and simultaneous coefficient forcing. Tied
    # potentials supply zero-flow edges; rho remains positive on those edges.
    response = simultaneous = zero_edges = 0
    for n in range(3, 7):
        edges = list(combinations(range(n), 2))
        for rho in [F(1, 2), F(1, 16), F(1, 2**20)]:
            pi = [F(i//2) for i in range(n)]
            x = [pi[u]-pi[v] for u,v in edges]
            r = [2-rho if value else rho for value in x]
            b = [F(0)]*n
            for (u,v), value in zip(edges,x):
                b[u] += value; b[v] -= value
            mass = sum(map(abs,b))/2
            active = [(1-rho)/abs(value) if value else F(1) for value in x]
            low = min(active)
            lap = [[F(0) for _ in range(n-1)] for _ in range(n-1)]
            for (u,v), re in zip(edges,r):
                for a, sa in [(u,1),(v,-1)]:
                    for c, sc in [(u,1),(v,-1)]:
                        if a < n-1 and c < n-1:
                            lap[a][c] += F(sa*sc)/re
            slopes = [F((-1)**e*(e+1), len(edges)) for e in range(len(edges))]
            forcing = [s*v*abs(v) for s,v in zip(slopes,x)]
            total_h = [F(0)]*len(edges)
            for e, (u,v) in enumerate(edges):
                demand = [F(int(a==u)-int(a==v)) for a in range(n-1)]
                p = solve(lap,demand)+[F(0)]
                j = [(p[a]-p[c])/re for (a,c),re in zip(edges,r)]
                require(0 <= j[e] <= 1, 'driven electrical edge bound')
                require(max(map(abs,j)) <= 1, 'unit electrical flow bound')
                h = [forcing[e]/r[e]*(ja-int(a==e)) for a,ja in enumerate(j)]
                balance = [F(0)]*n
                for a, ((tail,head),value) in enumerate(zip(edges,h)):
                    balance[tail] += value; balance[head] -= value
                    residual = r[a]*value + (forcing[e] if a == e else 0)
                    require(residual == forcing[e]/r[e]*(p[tail]-p[head]), 'differentiated potential equation')
                    total_h[a] += value
                require(not any(balance), 'differentiated conservation')
                require(max(map(abs,h)) <= abs(slopes[e])*mass/(2*low), 'per-edge derivative bound')
                zero_edges += int(x[e] == 0)
                response += 1
            require(max(map(abs,total_h)) <= mass*sum(map(abs,slopes))/(2*low), 'simultaneous derivative bound')
            simultaneous += 1
    print(json.dumps(dict(passed=True, scalar_cases=scalar, physical_pairs=physical,
                          sign_reversal_pairs=crossing, zero_endpoint_pairs=zero,
                          electrical_responses=response, zero_flow_responses=zero_edges,
                          simultaneous_derivatives=simultaneous,
                          scope='Exact finite diagnostics; universal claims rely on manuscript proofs.'), sort_keys=True))


if __name__ == '__main__':
    main()
