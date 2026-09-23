"""Independent-reference checks for the exact block-input cactus solver."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
import json
import random
from exact_weighted_cactus import Quadratic as Q, solve_cycle, solve_cactus


def decimal(x):
    if isinstance(x, Q):
        return decimal(x.a)+decimal(x.b)*decimal(x.d).sqrt()
    x = F(x)
    return Decimal(x.numerator)/Decimal(x.denominator)


def physical(offsets, weights, beta):
    """Independent high-precision monotone solve for a fixed beta profile."""
    ell, w, beta = [list(map(decimal, a)) for a in (offsets, weights, beta)]
    left, right = min(-t for t in ell), max(-t for t in ell)
    for _ in range(180):
        q = (left+right)/2
        total = sum(b*(q+t)*abs(q+t) for b, t in zip(beta, ell))
        if total > 0:
            right = q
        else:
            left = q
    q = (left+right)/2
    value = sum(a*b*(q+t)*abs(q+t) for a, b, t in zip(w, beta, ell))
    return q, value


def run():
    rng = random.Random(690609)
    comparisons = 0
    with localcontext() as context:
        context.prec = 100
        for _ in range(1200):
            args = [[F(rng.randrange(-200,201),rng.randrange(1,50)),
                     F(rng.randrange(-200,201),rng.randrange(1,50)),
                     F(rng.randrange(0,300),rng.randrange(1,50))] for _ in range(2)]
            x, y = [Q(*a) for a in args]
            expected = (decimal(x)>decimal(y))-(decimal(x)<decimal(y))
            assert x.compare(y) == expected
            assert x.compare(y) == -y.compare(x)
            assert x.compare(x) == 0
            lo, hi = x.interval(60)
            assert lo <= x <= hi and hi-lo <= F(1,2**60)
            comparisons += 1
        assert Q(1,2,2) == Q(1,1,8)
        assert Q(0,1,F(9,25)) == F(3,5)
        assert Q(0,-1,2) < 0 < Q(0,1,2)
        # A rational optimum with a uniquely necessary interior resistance.
        interior = solve_cycle([0,0,3,0],[2,-1,-3,0],[1]*4,[4,3,4,5])
        assert interior['circulation'] == -1
        assert interior['objective'] == -12
        assert interior['resistances'] == (F(1),F(2),F(1),F(1))
        # Entire feasible cycle is the all-zero stratum.
        zero = solve_cycle([3,3,3],[2,-4,7],[1]*3,[2,3,4])
        assert zero['circulation'] == -3 and zero['objective'] == 0
        # A rational capacity endpoint forces a single nonzero profile.
        cap = solve_cycle([0,0,3,0],[2,-1,-3,0],[1]*4,[4,3,4,5],
                          flow_lower=[-1,None,None,None],flow_upper=[-1,None,None,None])
        assert cap['circulation'] == -1 and cap['objective'] == -12
        assert solve_cycle([0,1,-2],[1,-1,2],[1]*3,[3,4,2],
                           flow_lower=[10,None,None]) is None
        # Fixed resistances exercise irrational aggregate-boundary recovery.
        irrational = solve_cycle([0,1,-2],[1,-1,2],[3,1,1],[3,1,1])
        assert irrational['circulation'].b != 0
        assert irrational['resistances'] == (F(3),F(1),F(1))
        # Flat objective must still find a feasible physical boundary.
        flat = solve_cycle([0,1,-2],[4,4,4],[1]*3,[3,4,2])
        assert flat['objective'] == 0
        profiles = 0
        capacity_cases = 0
        for trial in range(45):
            n = rng.randrange(3,7)
            ell = [F(rng.randrange(-4,5)) for _ in range(n)]
            weights = [F(rng.randrange(-4,5)) for _ in range(n)]
            lower = [F(rng.randrange(1,4)) for _ in range(n)]
            upper = [a+rng.randrange(0,4) for a in lower]
            # Rational flow capacities; randomly cap just one edge on some runs.
            flo, fhi = [None]*n, [None]*n
            if trial % 3 == 0:
                flo[0], fhi[0] = F(-2), F(2)
                capacity_cases += 1
            maximum = solve_cycle(ell,weights,lower,upper,flo,fhi,'max')
            minimum = solve_cycle(ell,weights,lower,upper,flo,fhi,'min')
            scenarios = [[u if bit else l for l,u,bit in zip(lower,upper,bits)]
                         for bits in product((0,1),repeat=n)]
            scenarios += [[l+(u-l)*F(rng.randrange(0,101),100)
                           for l,u in zip(lower,upper)] for _ in range(10)]
            for beta in scenarios:
                q, value = physical(ell,weights,beta)
                if flo[0] is not None and not decimal(flo[0])-Decimal('1e-45') <= q+decimal(ell[0]) <= decimal(fhi[0])+Decimal('1e-45'):
                    continue
                assert maximum is not None and minimum is not None
                assert decimal(minimum['objective'])-Decimal('1e-40') <= value
                assert value <= decimal(maximum['objective'])+Decimal('1e-40')
                profiles += 1
        result = solve_cactus({'cycles':[
            {'offsets':[0,1,-2], 'weights':[1,-1,2], 'lower':[1,1,1], 'upper':[3,4,2]},
            {'offsets':[0,0,3,0], 'weights':[2,-1,-3,0], 'lower':[1]*4,'upper':[4,3,4,5]}],
            'bridges':[{'flow':'-3/2','weight':2,'lower':1,'upper':3}]},80)
        lo,hi = map(F,result['objective_interval'])
        assert hi-lo <= F(1,2**80)
        assert result['bridges'][0]['resistance'] == '1'
        for bad in (1.5, True):
            try:
                solve_cycle([0,bad,1],[1,2,3],[1]*3,[2]*3)
                raise AssertionError('Invalid numeric input accepted')
            except ValueError:
                pass
    print(json.dumps({'quadratic_comparisons_and_intervals':comparisons,
                      'random_network_cases':45,'capacity_cases':capacity_cases,
                      'independent_physical_profiles':profiles,
                      'interior_resistance_regression':'passed',
                      'zero_fixed_flat_and_singleton_capacity':'passed',
                      'multiblock_interval_bits':80},indent=2))


if __name__ == '__main__':
    run()
