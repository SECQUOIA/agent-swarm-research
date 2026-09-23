"""Independent exact finite checks for stage 5; no manuscript imports."""
from fractions import Fraction as F
from itertools import product, combinations
from random import Random
from pathlib import Path
import json
from math import factorial, lcm


def solve(a, b):
    n = len(b)
    a = [[F(v) for v in row] + [F(v)] for row, v in zip(a, b)]
    for j in range(n):
        p = next((i for i in range(j, n) if a[i][j]), None)
        if p is None:
            return None
        a[j], a[p] = a[p], a[j]
        q = a[j][j]
        a[j] = [v/q for v in a[j]]
        for i in range(n):
            if i != j:
                q = a[i][j]
                a[i] = [v-q*w for v, w in zip(a[i], a[j])]
    return [row[-1] for row in a]


def check_padding():
    certificates = targets = 0
    for weights in [(1,), (2, 3), (1, 2, 5), (2, 4, 7)]:
        W = sum(weights)
        r = 0
        while F(1, 4**(r+1)) > F(1, 8*W):
            r += 1
        n = len(weights) + (len(weights)-1)*r
        positions = [i*(r+1) for i in range(len(weights))]
        gamma = F(1, 4)
        delta = F(1, 4**(2*(n-1)))
        tau = delta/(2*n)
        c = [(1-gamma)*gamma**(2*(n-i-1)-1) for i in range(n-1)] + [F(0)]
        totals = []
        sums = set()
        for free in product((0, 1), repeat=len(weights)):
            bits = [0]*n
            for i, b in zip(positions, free):
                bits[i] = b
            v = []
            previous = F(0)
            for b in bits:
                previous = b + (1-2*b)*gamma*previous
                v.append(previous)
            assert all(v[i] <= F(1, 2) for i in range(n) if i not in positions)
            assert v[-1]-sum(a*b for a,b in zip(c,v))-v[-1]**2 == 0
            total = sum(a*v[i] for a,i in zip(weights,positions))
            exact = sum(a*b for a,b in zip(weights,free))
            assert abs(total-exact) <= F(1,8)
            totals.append(total)
            sums.add(exact)
            for h in [-delta/4, F(0), delta/4]:
                price = 2*v[-1]-1+h
                if not -1 <= price <= 1:
                    continue
                # KKT against the original full cube, after identity scaling.
                gradient = [v[i]-c[i]/tau for i in range(n)]
                gradient[-1] -= price/tau
                multipliers = [F(0)]*n
                for i in range(n-1,-1,-1):
                    after = gamma*multipliers[i+1] if i+1 < n else F(0)
                    multipliers[i] = (-gradient[i]-after)/(2*bits[i]-1)
                assert all(m > 0 for m in multipliers)
                certificates += 1
        for target in range(W+1):
            assert any(abs(total-target) <= F(1,4) for total in totals) == (target in sums)
            targets += 1
    return dict(strict_identity_hessian_full_cube_certificates=certificates,
                padded_subset_sum_target_comparisons=targets)


def vertex_feasible(n, bounds, edges):
    rows = []
    for i,(lo,hi) in enumerate(bounds):
        unit = [F(int(j==i)) for j in range(n)]
        rows += [(unit,hi), ([-v for v in unit],-lo)]
    for u,v,a,b,c in edges:
        row = [F(0)]*n
        row[v] = 1
        row[u] = -a
        rows += [(row,c), ([-q for q in row],-b)]
    for basis in combinations(rows,n):
        x = solve([a for a,b in basis],[b for a,b in basis])
        if x is not None and all(sum(a*v for a,v in zip(row,x)) <= b for row,b in rows):
            return True
    return False


def projected_recover(n,bounds,edges):
    lows = [[lo] for lo,hi in bounds]
    ups = [[hi] for lo,hi in bounds]
    adjacent = [[] for _ in range(n)]
    for u,v,a,b,c in edges:
        if not a:
            lows[v].append(b)
            ups[v].append(c)
        else:
            adjacent[u].append((v,a))
            adjacent[v].append((u,1/a))
    A = [None]*n
    components = []
    for root in range(n):
        if A[root] is not None:
            continue
        A[root] = F(1)
        nodes = [root]
        for u in nodes:
            for v,a in adjacent[u]:
                if A[v] is None:
                    A[v] = a*A[u]
                    nodes.append(v)
        components.append(nodes)
    lo,hi = [],[]
    for i in range(n):
        left,right = lows[i],ups[i]
        if A[i] < 0:
            left,right = right,left
        lo.append(max(v/A[i] for v in left))
        hi.append(min(v/A[i] for v in right))
    distance = [[None]*n for _ in range(n)]
    for i in range(n):
        distance[i][i] = F(0)
    for u,v,a,b,c in edges:
        if a:
            alpha,beta = sorted([b/A[v],c/A[v]])
            distance[u][v] = beta
            distance[v][u] = -alpha
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if distance[i][k] is not None and distance[k][j] is not None:
                    value = distance[i][k]+distance[k][j]
                    if distance[i][j] is None or value < distance[i][j]:
                        distance[i][j] = value
    if any(lo[i] > hi[j]+distance[j][i] for nodes in components for i in nodes for j in nodes):
        return None
    x = [None]*n
    for nodes in components:
        for i in nodes:
            x[i] = A[i]*min(hi[j]+distance[j][i] for j in nodes)
    assert all(lo <= v <= hi for v,(lo,hi) in zip(x,bounds))
    assert all(a*x[u]+b <= x[v] <= a*x[u]+c for u,v,a,b,c in edges)
    return x


def check_strips():
    rng = Random(504)
    feasible = 0
    for trial in range(120):
        n = 3
        bounds = [(F(-1),F(2)) for _ in range(n)]
        if trial % 3 == 0:
            value = F(rng.randrange(-2,5),2)
            bounds[trial % n] = (value,value)
        edges = []
        for child in range(1,n):
            u,v = rng.randrange(child),child
            if rng.randrange(2):
                u,v = v,u
            a = rng.choice([F(-2),F(-1,2),F(0),F(1,3),F(2)])
            b = F(rng.randrange(-6,7),2)
            c = b+F(rng.randrange(4),2)
            edges.append((u,v,a,b,c))
        witness = projected_recover(n,bounds,edges)
        assert (witness is not None) == vertex_feasible(n,bounds,edges)
        feasible += witness is not None
    return dict(oriented_tree_zero_negative_gain_projection_cases=120,
                original_coordinate_rational_witnesses=feasible)


def check_exact_oracle():
    rng = Random(505)
    cases = 30
    iterations = 0
    for _ in range(cases):
        q = F(rng.randrange(-2,3),2)
        Q = [[F(rng.randrange(2,6)),q],[q,F(rng.randrange(2,6))]]
        t = [F(rng.randrange(-15,5),3) for _ in range(2)]
        optimum = None
        for statuses in product((0,1,2),repeat=2):
            z = [F(int(s==2)) for s in statuses]
            free = [i for i,s in enumerate(statuses) if s==1]
            if free:
                values = solve([[Q[i][j] for j in free] for i in free],
                               [-t[i]-sum(Q[i][j]*z[j] for j in range(2) if j not in free) for i in free])
                for i,v in zip(free,values):
                    z[i] = v
            g = [sum(Q[i][j]*z[j] for j in range(2))+t[i] for i in range(2)]
            if all(0<=v<=1 for v in z) and all((s==0 and g[i]>=0) or (s==1 and g[i]==0) or (s==2 and g[i]<=0) for i,s in enumerate(statuses)):
                optimum = z
                break
        assert optimum is not None
        det = Q[0][0]*Q[1][1]-q*q
        inv = [[Q[1][1]/det,-q/det],[-q/det,Q[0][0]/det]]
        L = max(sum(map(abs,row)) for row in Q)
        K = L*max(sum(map(abs,row)) for row in inv)
        coeff = [v for row in Q for v in row]+t
        common = lcm(*(v.denominator for v in coeff))
        H = max(1,*(abs(v*common) for v in coeff))
        B = int(factorial(2)*H**2)
        ceil_log_B = (B-1).bit_length()
        j = -(-(K*(2*ceil_log_B+1+4)).numerator//(K*(2*ceil_log_B+1+4)).denominator)
        z = [F(0),F(0)]
        for _ in range(j):
            z = [min(F(1),max(F(0),z[i]-(sum(Q[i][h]*z[h] for h in range(2))+t[i])/L)) for i in range(2)]
        assert all(abs(a-b)<F(1,4*B*B) for a,b in zip(z,optimum))
        assert [v.limit_denominator(B) for v in z] == optimum
        iterations += j
    return dict(exact_projected_gradient_rational_recoveries=cases,
                rational_gradient_iterations=iterations)


if __name__ == '__main__':
    result = {**check_padding(), **check_strips(), **check_exact_oracle()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
