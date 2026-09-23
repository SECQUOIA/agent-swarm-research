"""Exact clipping and physical capacity recovery, including frozen intervals."""
from fractions import Fraction as F
from random import Random
from cactus_convex_design_checks import profiles, value, root_box


def rational_profile(q, low, up):
    lo, hi = profiles(q, low, up)
    hlo, hhi = value(q, lo), value(q, hi)
    assert hlo <= 0 <= hhi
    lam = -hlo / (hhi - hlo) if hhi != hlo else F(0)
    beta = [a + lam * (b - a) for a, b in zip(lo, hi)]
    assert value(q, beta) == 0
    return beta


def run():
    rng = Random(502311)
    cases = []
    for _ in range(400):
        low = [F(rng.randrange(1, 9), 3) for _ in range(3)]
        up = [b + F(rng.randrange(0, 8), 5) for b in low]
        a, b = sorted([F(-rng.randrange(0, 33), 32) for _ in range(2)])
        cases.append((low, up, a, b))
    # Irrational singleton physical interval; rational singleton clipping;
    # narrow irrational interval forces endpoint recovery from a frozen proxy.
    cases += [([F(1)] * 3, [F(1)] * 3, F(-1), F(0)),
              ([F(1)] * 3, [F(4)] * 3, F(-1, 2), F(-1, 2)),
              ([F(1)] * 3, [F(1) + F(1, 2**100)] * 3, F(-1), F(0))]
    feasible = infeasible = frozen = rational = 0
    eta = F(1, 2**22)
    for low, up, a, b in cases:
        # H_max has the lower attainable root, H_min the upper root.
        hmax_a = value(a, profiles(a, low, up)[1])
        hmin_b = value(b, profiles(b, low, up)[0])
        lower_rational = hmax_a > 0
        upper_rational = hmin_b < 0
        if lower_rational and upper_rational:
            possible = a <= b
        elif lower_rational:
            possible = value(a, profiles(a, low, up)[0]) <= 0
        elif upper_rational:
            possible = value(b, profiles(b, low, up)[1]) >= 0
        else:
            possible = True
        if not possible:
            infeasible += 1
            continue
        feasible += 1
        lower_beta = rational_profile(a, low, up) if lower_rational else [up[0], up[1], low[2]]
        upper_beta = rational_profile(b, low, up) if upper_rational else [low[0], low[1], up[2]]
        for beta in (lower_beta, upper_beta):
            # Strictly increasing constitutive sum makes these exact root
            # comparisons, with no numerical evaluation of irrational flow.
            assert value(a, beta) <= 0 <= value(b, beta)
            assert all(l <= x <= u for l, x, u in zip(low, beta, up))
        lb = (a, a) if lower_rational else root_box(low, up, False, eta)
        ub = (b, b) if upper_rational else root_box(low, up, True, eta)
        if lb[1] <= ub[0]:
            q = (lb[1] + ub[0]) / 2
            beta = rational_profile(q, low, up)
            assert a <= q <= b
            rational += 1
        else:
            beta = lower_beta
            frozen += 1
        assert value(a, beta) <= 0 <= value(b, beta)
        assert all(l <= x <= u for l, x, u in zip(low, beta, up))
    assert frozen >= 2 and rational > 0 and infeasible > 0
    print(f'PASS: {len(cases)} exact cases; {feasible} feasible, {infeasible} infeasible; '
          f'{rational} retained rational recoveries and {frozen} frozen endpoint recoveries')


if __name__ == '__main__':
    run()
