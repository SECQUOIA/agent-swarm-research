"""Vector-quality physical LPs versus exact scalar-chart cut conditions.

The LP retains every original pool arc and every quality coordinate. The
cut side uses rational arithmetic. This checks fixed parameter fibers,
not the global real-algebraic optimization algorithm.
"""
from fractions import Fraction as F
from random import Random

from check_all_product_contracts import LP
from check_quality_scaled_cuts import cuts_hold


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def physical(net, q):
    C, a, B, b, edges, feeds, outlets = net
    t = len(q)
    lp = LP({**{('z', i, j): (0, 2) for i, j in edges},
             **{('y', i): (0, cap) for i, cap in feeds.items()},
             **{('v', j): (0, cap) for j, cap in outlets.items()}})
    for i in range(len(C)):
        row = {('z', i, j): F(1) for ii, j in edges if ii == i}
        if i in feeds:
            row['y', i] = F(1)
        lp.add(row, a[i], True)
    for j in range(len(B)):
        row = {('z', i, j): F(1) for i, jj in edges if jj == j}
        if j in outlets:
            row['v', j] = F(1)
        lp.add(row, b[j], True)
        for h in range(t):
            row = {('z', i, j): C[i][h] for i, jj in edges if jj == j}
            if j in outlets:
                row['v', j] = q[h]
            lp.add(row, b[j]*B[j][h], True)
    lp.add({**{('y', i): F(1) for i in feeds},
            **{('v', j): F(-1) for j in outlets}}, 0, True)
    for h in range(t):
        lp.add({**{('y', i): C[i][h] for i in feeds},
                **{('v', j): -q[h] for j in outlets}}, 0, True)
    return lp.feasible()


def transformed(net, q, beta, vector_rows=True):
    C, a, B, b, edges, feeds, outlets = net
    t = len(q)
    c = [dot(beta, ci) for ci in C]
    gamma = [ci-dot(beta, q) for ci in c]
    assert all(gamma)
    if sum(a) != sum(b) or any(sum(C[i][h]*a[i] for i in range(len(C))) !=
                               sum(B[j][h]*b[j] for j in range(len(B))) for h in range(t)):
        return False
    nodes = [('i', i) for i in range(len(C))] + [('o', j) for j in range(len(B))]
    arcs = [(('i', i), ('o', j)) for i, j in edges]
    nb, eb = {}, {}
    for i in range(len(C)):
        ends = [gamma[i]*(a[i]-feeds.get(i, 0)), gamma[i]*a[i]]
        nb['i', i] = min(ends), max(ends)
    for i, j in edges:
        eb[(('i', i), ('o', j))] = [min(0, 2*gamma[i]), max(0, 2*gamma[i])]

    def intersect(i, j, lo, hi):
        e = (('i', i), ('o', j))
        eb[e] = [max(eb[e][0], lo), min(eb[e][1], hi)]

    for j in range(len(B)):
        R = b[j]*(dot(beta, B[j])-dot(beta, q))
        nb['o', j] = -R, -R
        ins = [i for i, jj in edges if jj == j]
        lo, hi = b[j]-outlets.get(j, 0), b[j]
        if len(ins) == 2:
            i, k = ins
            if c[i] != c[k]:
                ends = [gamma[i]*(R-gamma[k]*s)/(c[i]-c[k]) for s in (lo, hi)]
                intersect(i, j, min(ends), max(ends))
            else:
                ends = [gamma[i]*lo, gamma[i]*hi]
                if not min(ends) <= R <= max(ends):
                    return False
            for h in range(t) if vector_rows else []:
                ah = (C[i][h]-q[h])*gamma[k]-(C[k][h]-q[h])*gamma[i]
                fh = gamma[i]*(b[j]*(B[j][h]-q[h])*gamma[k]-(C[k][h]-q[h])*R)
                if ah:
                    intersect(i, j, fh/ah, fh/ah)
                elif fh:
                    return False
        elif len(ins) == 1:
            i = ins[0]
            ends = [gamma[i]*lo, gamma[i]*hi]
            intersect(i, j, min(ends), max(ends))
            if vector_rows and any((C[i][h]-q[h])*R != b[j]*(B[j][h]-q[h])*gamma[i]
                                   for h in range(t)):
                return False
        else:
            if not lo <= 0 <= hi:
                return False
            if vector_rows and any(b[j]*(B[j][h]-q[h]) for h in range(t)):
                return False
    return cuts_hold(nodes, arcs, nb, eb)


def instances():
    rng = Random(950631)
    for t in (2, 3):
        for case in range(24):
            n = 3+case % 4
            C = [tuple(F(rng.randrange(4)) for _ in range(t)) for _ in range(n)]
            # Force equal projected first coordinates, and sometimes full equality.
            if case % 3 == 0:
                C[1] = (C[0][0], *C[1][1:])
            if case % 7 == 0:
                C[1] = C[0]
            all_edges = [(i, i) for i in range(n)]+[(i, (i+1) % n) for i in range(n)]
            edges = [e for e in all_edges if case % 2 == 0 or rng.random() > .25]
            z = {e: F(rng.randrange(1, 5), 4) for e in edges}
            y = {i: F(rng.randrange(1, 5), 4) for i in range(n) if i == 0 or rng.random() > .2}
            T = sum(y.values())
            q = tuple(sum(C[i][h]*yi for i, yi in y.items())/T for h in range(t))
            out_set = [j for j in range(n) if j == 0 or rng.random() > .2]
            v = {j: T/len(out_set) for j in out_set}
            a = [y.get(i, 0)+sum(zz for (ii, j), zz in z.items() if ii == i) for i in range(n)]
            b = [v.get(j, 0)+sum(zz for (i, jj), zz in z.items() if jj == j) for j in range(n)]
            B = [tuple((q[h]*v.get(j, 0)+sum(C[i][h]*zz for (i, jj), zz in z.items() if jj == j))/b[j]
                       if b[j] else F(0) for h in range(t)) for j in range(n)]
            yield (C, a, B, b, edges, {i: F(2) for i in y},
                   {j: max(F(2), 2*vj) for j, vj in v.items()}), q


def main():
    checked = feasible = singular = charts = omitted_detected = 0
    for net, known in instances():
        C = net[0]
        t = len(known)
        targets = {known, *C}
        targets.update(tuple(qh+(F(1, 3) if h == k else 0) for h, qh in enumerate(known)) for k in range(t))
        assert physical(net, known)
        for q in targets:
            original = physical(net, q)
            if q in C:
                singular += 1
                continue
            good = []
            for k in range(1, len(C)*(t-1)+2):
                beta = tuple(F(k**h) for h in range(t))
                if all(dot(beta, ci) != dot(beta, q) for ci in C):
                    good.append(beta)
            assert good, ('chart coverage', C, q)
            # Include beta=(1,0,..), which often has equal projected input qualities.
            beta0 = (F(1),)+(F(0),)*(t-1)
            if all(ci[0] != q[0] for ci in C):
                good.append(beta0)
            for beta in good:
                actual = transformed(net, q, beta)
                assert actual == original, (q, beta, actual, original)
                omitted_detected += transformed(net, q, beta, False) and not actual
                charts += 1
            checked += 1
            feasible += original
    assert omitted_detected > 0
    print(f'PASS: {checked} vector-quality fibers ({feasible} feasible), {charts} nonsingular chart comparisons.')
    print(f'PASS: {singular} source-vector singular cases use original physical LPs.')
    print(f'PASS: dropping extra vector-quality rows gives {omitted_detected} false-positive chart cases.')
    print('Cut arithmetic is exact rational; original feasibility uses numerical HiGHS.')


if __name__ == '__main__':
    main()
