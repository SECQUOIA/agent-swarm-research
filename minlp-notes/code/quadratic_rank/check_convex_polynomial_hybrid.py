"""Exact checks for the convex-polynomial hybrid proof.

Uses Sturm root counts on odd-multiplicity factors as an independent chord
predicate. Does not implement the certified quadrature or Boolean compiler.
"""
import sympy as sp

x = sp.Symbol('x')
R = sp.Rational


def chord_good(f, a, b, epsilon):
    if a == b:
        return True
    fa, fb = f.eval(a), f.eval(b)
    q = sp.Poly(fa + (fb-fa)*(x-a)/(b-a) - f.as_expr() - epsilon, x)
    assert q.eval(a) == -epsilon and q.eval(b) == -epsilon
    # A polynomial negative at both endpoints becomes positive iff it crosses
    # zero with odd multiplicity somewhere inside the interval.
    for fac, multiplicity in sp.sqf_list(q)[1]:
        if multiplicity % 2 and fac.count_roots(a, b):
            return False
    return True


curvatures = [
    sp.Integer(2),
    (x-R(1,2))**2,
    1+100*(x-R(1,4))**2,
    (x-R(1,4))**2*(x-R(3,4))**2,
    1+100*x*(1-x),
]
fs = [sp.Poly(sp.integrate(sp.integrate(g, x), x), x) for g in curvatures]
rounding_checks = greedy_checks = grid_queries = 0
for f in fs:
    coeffs = f.all_coeffs()[::-1]
    M = max(R(1), sum(k*abs(c) for k,c in enumerate(coeffs)))
    M2 = sum(k*(k-1)*abs(c) for k,c in enumerate(coeffs))
    h = R(1,128)
    for j in range(7):
        a, b = R(j,7), R(j+1,7)
        eta = M2*(b-a)**2/8
        lo, hi = max(R(0), a-h), min(R(1), b+h)
        assert chord_good(f, lo, hi, eta+2*M*h)
        ar, br = sp.floor(a/h)*h, sp.floor(b/h)*h
        assert chord_good(f, ar, br, eta+2*M*h)
        rounding_checks += 2
    # Exhaustive grid dynamic programming versus farthest-endpoint greedy.
    n = 16
    for epsilon in [R(1,64), R(1,16), R(1,4)]:
        good = {}
        for a in range(n):
            for b in range(a+1,n+1):
                good[a,b] = chord_good(f,R(a,n),R(b,n),epsilon)
                grid_queries += 1
        if not all(good[j,j+1] for j in range(n)):
            continue
        dist = [n+1]*(n+1)
        dist[0] = 0
        for b in range(1,n+1):
            dist[b] = min(dist[a]+1 for a in range(b) if good[a,b])
        a = 0
        count = 0
        while a < n:
            feasible = [b for b in range(a+1,n+1) if good[a,b]]
            # Feasibility is an initial interval, as required by binary search.
            assert feasible == list(range(a+1,max(feasible)+1))
            a = max(feasible)
            count += 1
        assert count == dist[n]
        greedy_checks += 1

counts = [1, 8, 2**40, 1, 4]
prefix = [0]
for k in counts:
    prefix.append(prefix[-1]+k)
index_checks = 0
for j,k in enumerate(counts):
    for local in sorted({0,k//2,k-1}):
        global_index = prefix[j]+local
        selected = next(i for i in range(len(counts)) if global_index < prefix[i+1])
        assert selected == j
        assert global_index-prefix[selected] == local
        index_checks += 1
print(f'PASS: {rounding_checks} exact expansion/rounding bounds; '
      f'{greedy_checks} greedy-vs-optimal grid comparisons using '
      f'{grid_queries} exact chord decisions; {index_checks} global-index checks')
