"""Exact finite checks of the proposed lossless coordinatewise lift transfer.

Checks high-degree power and nonpolynomial square-root auxiliaries at the
original hierarchy order. These cases support, and do not replace, the proof.
Polynomials below are stored after Boolean reduction as mask/coefficient maps.
"""
from fractions import Fraction as Q
from math import prod
from pathlib import Path
import json
import random


def add(*polys):
    out = {}
    for poly in polys:
        for mask, coefficient in poly.items():
            out[mask] = out.get(mask, Q(0)) + coefficient
    return {mask: coefficient for mask, coefficient in out.items() if coefficient}


def scale(poly, value):
    return {mask: coefficient*value for mask, coefficient in poly.items() if coefficient*value}


def multiply(left, right):
    return add(*({a | b: x*y} for a, x in left.items() for b, y in right.items()))


def power(poly, degree):
    out = {0: Q(1)}
    for _ in range(degree):
        out = multiply(out, poly)
    return out


def falling(value, degree):
    return prod(value-j for j in range(degree))


def run_case(order, fixed_middle, power_degree):
    # k endpoint ones, eight middle coordinates of value 1/16, z zeros.
    # sqrt(1/16)=1/4 permits exact checking of nonpolynomial auxiliaries.
    k = z = 2*order-1
    m = 8
    n = k+m+z
    restricted = set(range(k, k+fixed_middle))
    remaining = [i for i in range(n) if i not in restricted]
    index = {i: j for j, i in enumerate(remaining)}
    s = len(remaining)
    t = Q(k) + Q(m-fixed_middle, 16)
    assert s >= 2*order and t >= 2*order-1 and s-t >= 2*order-1
    moments = [Q(falling(t, a), falling(s, a)) for a in range(2*order+1)]

    def expectation(poly):
        assert all(mask.bit_count() <= 2*order for mask in poly)
        return sum(coefficient*moments[mask.bit_count()] for mask, coefficient in poly.items())

    xs, ys, zs = [], [], []
    one = {0: Q(1)}
    for i in range(n):
        if i in restricted:
            xs.append({0: Q(1,16)})
            ys.append({0: Q(1,16)**power_degree})
            zs.append({0: Q(1,4)})
        else:
            u = {1 << index[i]: Q(1)}
            xs.append(u)
            ys.append(u)  # Endpoint interpolation of x**D.
            zs.append(u)  # Endpoint interpolation of sqrt(x).
    variables = xs+ys+zs
    demand = add(*xs, {0: -Q(2*k+1, 2)})
    graph = [add(power(zs[i],2), scale(xs[i],-1)) for i in range(n)]
    if power_degree <= 2*order:
        graph += [add(ys[i], scale(power(xs[i],power_degree),-1)) for i in range(n)]
    assert all(not identity for identity in graph)

    # These local polynomials are valid on the full individual graph:
    # 0<=x,y,sqrt(x)<=1, x**D<=x, x**D<=x**2, and the tangent at x=1.
    generators = []
    for x,y,sqrt_x in zip(xs,ys,zs):
        for variable in [x,y,sqrt_x]:
            generators.extend([(variable,1),(add(one,scale(variable,-1)),1)])
        generators.extend([(add(x,scale(y,-1)),1),
                           (add(power(x,2),scale(y,-1)),2),
                           (add(y,scale(x,-power_degree),{0:Q(power_degree-1)}),1)])

    rng = random.Random(500+order*17+fixed_middle*3+power_degree)
    equalities = localizers = 0
    for _ in range(80):
        multiplier = one
        for _ in range(rng.randrange(2*order)):
            multiplier = multiply(multiplier, rng.choice(variables))
        assert expectation(multiply(demand,multiplier)) == 0
        equalities += 1
    for _ in range(160):
        g, degree = one, 0
        for _ in range(rng.randrange(2*order+1)):
            candidate, cost = rng.choice(generators)
            if degree+cost <= 2*order:
                g, degree = multiply(g,candidate), degree+cost
        max_square_degree = (2*order-degree)//2
        terms = []
        for _ in range(6):
            monomial = {0: Q(rng.randrange(-3,4))}
            for _ in range(rng.randrange(max_square_degree+1)):
                monomial = multiply(monomial,rng.choice(variables))
            terms.append(monomial)
        p = add(*terms)
        assert expectation(multiply(g,power(p,2))) >= 0
        localizers += 1
    penalty = add(*(add(x,scale(power(x,2),-1)) for x in xs))
    assert expectation(penalty) == fixed_middle*Q(15,256)
    return dict(order=order, power_degree=power_degree,
                fixed_middle=fixed_middle, original_dimension=n,
                lifted_dimension=3*n, demand_checks=equalities,
                localizer_checks=localizers, graph_identities=len(graph),
                objective=str(expectation(penalty)))


def main():
    records = [run_case(r,f,D) for r in [1,2,3] for f in [0,1,2] for D in [2,3,7,21]]
    output = Path(__file__).with_suffix('.json')
    output.write_text(json.dumps({'status':'PASS', 'arithmetic':'Exact Fraction',
        'interpretation':'Finite evidence for a candidate theorem; not a universal proof.',
        'cases':records},indent=2)+'\n')
    print(f'PASS {len(records)} lifted cases, '
          f'{sum(v["demand_checks"] for v in records)} equality checks, '
          f'{sum(v["localizer_checks"] for v in records)} localizers. {output}')


if __name__ == '__main__':
    main()
