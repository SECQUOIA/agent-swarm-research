"""Exact supplemental checks for Stage 4 boundaries and lifted tensor transfer.

The universal results are proved in the Stage 4 sections. This checks symbolic
Gram entries, negative preordering boundary cases, globally coupled lifted
squares in three blocks, and the clique-cut algebra with rational arithmetic.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import comb, prod
from pathlib import Path
import json
import random

import sympy as sp

from check_univariate_lift_refinement import add, scale, multiply, power, falling


def gram_and_boundaries():
    s, t = sp.symbols("s t")
    count = 0
    for d in range(1, 7):
        for overlap in range(d + 1):
            numerator = sum(comb(overlap, j) * falling(t, 2*d-j)
                            * falling(s-t, j) for j in range(overlap+1))
            target = falling(t, 2*d-overlap)*falling(s-2*d+overlap, overlap)
            assert sp.expand(numerator-target) == 0
            count += 1
    boundary_cases = 0
    for r in range(1, 7):
        s = 4*r
        for endpoint in (Q(2*r-1), Q(2*r-1, 1)+Q(1, 2)):
            coefficients = [Q(falling(endpoint, 2*r-j)*falling(s-endpoint, j),
                              falling(s, 2*r)) for j in range(r+1)]
            assert min(coefficients) >= 0
            boundary_cases += 1
        for a in range(2*r-1):
            t = Q(2*a+1, 2)
            assert Q(falling(t, a+2), falling(s, a+2)) < 0
            boundary_cases += 1
    return dict(symbolic_gram_entries=count, boundary_cases=boundary_cases)


def tensor_case(r, kinds):
    rng = random.Random(10400+100*r+sum((j+1)*v for j, v in enumerate(kinds)))
    one = {0: Q(1)}
    xs, ys, penalties, demands, masks, parameters = [], [], [], [], [], []
    graph_equalities, local_slacks = [], []
    next_bit = 0
    expected_penalty = Q(0)
    k = 2*r-1
    m = 8
    nblock = 2*k+m
    for kind in kinds:
        # kind 0: no restriction; 1: one middle fixed; 2: full witness evaluation.
        block_x, block_y, block_z = [], [], []
        restricted_middle = m if kind == 2 else kind
        free = 0 if kind == 2 else nblock-restricted_middle
        mask = 0
        for i in range(nblock):
            value = Q(1) if i < k else (Q(1, 16) if i < k+m else Q(0))
            fixed = kind == 2 or (kind == 1 and i == k)
            if fixed:
                x = {0: value} if value else {}
                # Nonpolynomial function: 2 at zero, -3 at one, 7 elsewhere.
                y = {0: Q(2) if value == 0 else (Q(-3) if value == 1 else Q(7))}
                z = {0: value*(1-value)} if value*(1-value) else {}
            else:
                x = {1 << next_bit: Q(1)}
                mask |= 1 << next_bit
                next_bit += 1
                y = add({0: Q(2)}, scale(x, -5))
                z = {}
            block_x.append(x); block_y.append(y); block_z.append(z)
            lower = add(y, {0: Q(3)})
            upper = add({0: Q(7)}, scale(y, -1))
            local_slacks.extend([(x, 1), (add(one, scale(x, -1)), 1),
                                 (lower, 1), (upper, 1),
                                 (multiply(lower, upper), 2)])
            graph_equalities.extend([
                (add(z, scale(x, -1), power(x, 2)), 2),
                (multiply(multiply(add(y, {0: Q(-2)}), lower), upper), 3),
            ])
        xs.extend(block_x); ys.extend(block_y); penalties.extend(block_z)
        demands.append(add(*block_x, {0: -Q(2*k+1, 2)}))
        masks.append(mask)
        parameters.append((free, Q(k)+Q(m-restricted_middle, 16)))
        expected_penalty += restricted_middle*Q(15, 256)

    def expectation(poly):
        assert all(mask.bit_count() <= 2*r for mask in poly)
        return sum(coefficient*prod(
            Q(falling(t, (mask & blockmask).bit_count()),
              falling(s, (mask & blockmask).bit_count()))
            for blockmask, (s, t) in zip(masks, parameters))
            for mask, coefficient in poly.items())

    variables = xs+ys+penalties
    equality_checks = localizer_checks = 0
    assert expectation(one) == 1
    for degree in range(2*r):
        multiplier = one
        for _ in range(degree):
            multiplier = multiply(multiplier, rng.choice(variables))
        for demand in demands:
            assert expectation(multiply(demand, multiplier)) == 0
            equality_checks += 1
    for h, degree in graph_equalities:
        if degree <= 2*r:
            multiplier = one
            for _ in range(2*r-degree):
                multiplier = multiply(multiplier, rng.choice(variables))
            assert expectation(multiply(h, multiplier)) == 0
            equality_checks += 1
    for cost in range(2*r+1):
        for repeat in range(8):
            g = one
            # Repeat a chosen factor explicitly in half of these cases.
            choice = rng.choice(local_slacks[:4])
            used = 0
            while used < cost:
                h, degree = choice if repeat % 2 else rng.choice(local_slacks)
                if used+degree <= cost:
                    g = multiply(g, h); used += degree
            square_degree = (2*r-cost)//2
            terms = []
            for block in range(3):
                term = {0: Q(block+1)}
                for step in range(square_degree):
                    # Every nonconstant square couples all three blocks.
                    source_block = (block+step) % 3
                    term = multiply(term, xs[source_block*nblock+rng.randrange(nblock)])
                terms.append(term)
            p = add(*terms)
            assert expectation(multiply(g, power(p, 2))) >= 0
            localizer_checks += 1
    objective = add(*penalties)
    if r >= 2:
        # A written lifted objective can couple blocks via graph identities.
        h = graph_equalities[0][0]
        objective = add(objective, multiply(h, ys[nblock]))
    assert expectation(objective) == expected_penalty
    return dict(order=r, block_types=kinds, equality_checks=equality_checks,
                localizer_checks=localizer_checks, objective=str(expected_penalty))


def clique_and_example():
    vertices = 0
    for n in range(2, 9):
        for k in range(n):
            K = Q(2*k+1, 2)
            assert K*K-2*k*K+k*(k+1) == k+Q(1, 4)
            coefficients = [Q(2*(i+1), n*(n+1)) for i in range(n)]
            optimum = Q(1, 4)+sum(coefficients[:k])+coefficients[k]/2
            minimizers = 0
            for half in range(n):
                for ones in combinations([i for i in range(n) if i != half], k):
                    x = [Q(int(i in ones)) for i in range(n)]; x[half] = Q(1, 2)
                    cut = 2*sum(x[i]*x[j] for i in range(n) for j in range(i+1, n))-2*k*K+k*(k+1)
                    assert cut == 0
                    objective = sum(v*(1-v)+d*v for v, d in zip(x, coefficients))
                    assert objective >= optimum
                    minimizers += objective == optimum
                    vertices += 1
            assert minimizers == 1
    tau = Q(1, 4)-Q(1, 32)*(Q(5, 2)+Q(1, 4))-Q(1, 32)
    assert tau == Q(17, 128) and 2*tau/6 == Q(17, 384)
    return dict(clique_and_unique_optimizer_vertices=vertices,
                relative_tau=str(tau), relative_exponent_per_coordinate=str(2*tau/6))


def main():
    report = dict(status="PASS", arithmetic="exact rational and symbolic polynomial",
                  scope="Finite supplemental checks; universal proofs are in the Stage 4 sections.")
    report.update(gram_and_boundaries())
    report["lifted_tensor_cases"] = [tensor_case(r, kinds) for r in (1, 2, 3)
                                      for kinds in ((0, 0, 0), (0, 1, 2), (2, 2, 2))]
    report.update(clique_and_example())
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
