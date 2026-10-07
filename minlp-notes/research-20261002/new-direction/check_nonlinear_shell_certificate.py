"""Exact small-instance checks for nonlinear-shell-certificate.md.

This diagnostic implements finite shell/core tables and owned-variable OR
messages. It does not replace the general rounding or complexity proofs.
"""

from fractions import Fraction as F
from itertools import product
from math import comb


def clean(poly):
    return {a: c for a, c in poly.items() if c}


def value(poly, x):
    return sum(c * prod(xi**ai for xi, ai in zip(x, a))
               for a, c in poly.items())


def prod(items):
    out = F(1)
    for item in items:
        out *= item
    return out


def translate(poly, center):
    out = {}
    for a, c in poly.items():
        for b in product(*(range(ai + 1) for ai in a)):
            coefficient = c * prod(comb(ai, bi) * vi**(ai-bi)
                                   for ai, bi, vi in zip(a, b, center))
            out[b] = out.get(b, F(0)) + coefficient
    return clean(out)


def second(poly, i):
    out = {}
    for a, c in poly.items():
        if a[i] >= 2:
            b = list(a)
            b[i] -= 2
            out[tuple(b)] = c * a[i] * (a[i] - 1)
    return out


def interval_monomial(a, bounds):
    low = high = F(1)
    for ai, (left, right) in zip(a, bounds):
        choices = [left**ai, right**ai]
        if ai and ai % 2 == 0 and left <= 0 <= right:
            choices.append(F(0))
        vlow, vhigh = min(choices), max(choices)
        products = [low*vlow, low*vhigh, high*vlow, high*vhigh]
        low, high = min(products), max(products)
    return low, high


def curvature(poly, bounds):
    upper = []
    for i in range(len(bounds)):
        total = F(0)
        for a, c in second(poly, i).items():
            low, high = interval_monomial(a, bounds)
            total += max(c*low, c*high)
        upper.append(total)
    return max(upper) if max(upper) > 0 else F(1)


def ceil(q):
    return -(-q.numerator // q.denominator)


def coord_grid(left, right, spacing, radius, delta, n, core=False):
    nodes = {F(0)}
    for sign, width in ((-1, -left), (1, right)):
        cap = min(width, radius if core else 2*radius)
        if spacing is not None:
            if core:
                continue
            cap = spacing * (cap // spacing)
        if cap <= 0:
            continue
        initial = delta * radius / (2*n)
        if spacing is not None:
            initial = spacing * ceil(initial / spacing)
        a = min(cap, initial)
        nodes.add(sign*a)
        while a < cap:
            step = delta*a if spacing is None else spacing*max(
                1, (delta*a)//spacing)
            a = min(cap, a+step)
            nodes.add(sign*a)
        threshold = radius if spacing is None else spacing*ceil(radius/spacing)
        if threshold <= cap:
            nodes.add(sign*threshold)
    return sorted(nodes)


def corrected(poly, n, correction):
    out = dict(poly)
    for i in range(n):
        a = tuple(2 if i == j else 0 for j in range(n))
        out[a] = out.get(a, F(0)) - correction
    return clean(out)


def table_min(poly, grids, radius, bags, parents):
    n = len(grids)
    children = [[] for _ in bags]
    depth = [0] * len(bags)
    for t in range(1, len(bags)):
        children[parents[t]].append(t)
        depth[t] = depth[parents[t]] + 1
    owners = [min((t for t, bag in enumerate(bags) if i in bag),
                  key=lambda t: depth[t]) for i in range(n)]
    for i in range(n):
        for t, bag in enumerate(bags):
            if i in bag and t != owners[i]:
                assert i in bags[parents[t]]
    local = [[] for _ in bags]
    for a, c in poly.items():
        support = {i for i, ai in enumerate(a) if ai}
        t = next(t for t, bag in enumerate(bags) if support <= set(bag))
        local[t].append((tuple(a[i] for i in bags[t]), c))
    separators = [()] + [tuple(i for i in bags[t] if i in bags[parents[t]])
                         for t in range(1, len(bags))]
    messages = {}
    rows = 0
    for t in reversed(range(len(bags))):
        bag = bags[t]
        msg = {}
        for assignment in product(*(grids[i] for i in bag)):
            rows += 1
            cost = sum(c*prod(xi**ai for xi, ai in zip(assignment, a))
                       for a, c in local[t])
            flag = any(abs(assignment[j]) >= radius
                       for j, i in enumerate(bag) if owners[i] == t)
            costs = {flag: cost}
            for child in children[t]:
                key = tuple(assignment[bag.index(i)] for i in separators[child])
                new = {}
                for f1, c1 in costs.items():
                    for f2 in (False, True):
                        if (key, f2) in messages[child]:
                            f = f1 or f2
                            z = c1 + messages[child][key, f2]
                            new[f] = min(new.get(f, z), z)
                costs = new
            key = tuple(assignment[bag.index(i)] for i in separators[t])
            for flag, cost in costs.items():
                msg[key, flag] = min(msg.get((key, flag), cost), cost)
        messages[t] = msg
    got = messages[0].get(((), True))
    candidates = [value(poly, x) for x in product(*grids)
                  if max(map(abs, x)) >= radius]
    expected = min(candidates) if candidates else None
    assert got == expected
    return got, rows


def round_coordinate(x, nodes):
    if x in nodes:
        return [(x, F(1))]
    left = max(y for y in nodes if y < x)
    right = min(y for y in nodes if y > x)
    return [(left, (right-x)/(right-left)),
            (right, (x-left)/(right-left))]


def rounding_checks(poly, grids, radius, delta, ell, sigma, spacing):
    n = len(grids)
    targets = []
    for nodes, step in zip(grids, spacing):
        values = {nodes[0], F(0), nodes[-1]}
        if step is None:
            for a, b in zip(nodes, nodes[1:]):
                values.add((2*a+b)/3)
                break
        else:
            for a, b in zip(nodes, nodes[1:]):
                if b-a > step:
                    values.add(a+step)
                    break
        targets.append(sorted(values))
    count = 0
    for x in product(*targets):
        if max(map(abs, x)) < radius:
            continue
        laws = [round_coordinate(xi, nodes) for xi, nodes in zip(x, grids)]
        expectation = norm_expectation = variance = F(0)
        for xi, law in zip(x, laws):
            mean = sum(y*p for y, p in law)
            moment = sum(y*y*p for y, p in law)
            assert mean == xi
            var = moment-xi*xi
            assert 4*var <= delta**2*moment + delta**2*radius**2/n**2
            variance += var
        for atom in product(*laws):
            y = tuple(t[0] for t in atom)
            probability = prod(t[1] for t in atom)
            assert max(map(abs, y)) >= radius
            expectation += probability*value(poly, y)
            norm_expectation += probability*sum(yi*yi for yi in y)
        fx = value(poly, x)
        assert expectation-fx <= ell*variance/2
        assert expectation-sigma*norm_expectation - (
            fx-sigma*sum(xi*xi for xi in x)) <= (
                sigma*norm_expectation + sigma*radius**2/n)
        count += 1
    return count


def trial(poly, bounds, v, spacing, bags, parents, delta, counters):
    n = len(v)
    shift = translate(poly, v)
    shift.pop((0,)*n, None)
    sides = [(left-vi, right-vi) for (left, right), vi in zip(bounds, v)]
    for i, step in enumerate(spacing):
        if step is None:
            unit = tuple(int(i == j) for j in range(n))
            c = shift.get(unit, F(0))
            assert sides[i][0] == 0 or c <= 0
            assert sides[i][1] == 0 or c >= 0
    ell = curvature(poly, bounds)
    sigma = ell*delta**2/8
    r0 = min([step/2 for step in spacing if step is not None] +
             [abs(a) for i, pair in enumerate(sides) if spacing[i] is None
              for a in pair if a])
    slice_poly = {a: c for a, c in shift.items()
                  if all(not ai or spacing[i] is None for i, ai in enumerate(a))}
    q = {a: c for a, c in slice_poly.items() if sum(a) <= 2}
    tail = {a: c for a, c in slice_poly.items() if sum(a) >= 3}
    bound = max(F(1), sum(map(abs, tail.values())))
    rho = min(F(1), r0, sigma/bound)
    core_ok = True
    if any(step is None for step in spacing):
        grids = [coord_grid(*sides[i], spacing[i], rho, delta, n, core=True)
                 for i in range(n)]
        m, rows = table_min(corrected(q, n, 3*sigma), grids, rho, bags, parents)
        counters["rows"] += rows
        counters["tables"] += 1
        assert m is not None
        core_ok = m >= sigma*rho**2/n
        for x in product(*[(F(0), nodes[0]/2, nodes[-1]/2)
                           for nodes in grids]):
            norm = sum(xi*xi for xi in x)
            assert abs(value(slice_poly, x)-value(q, x)) <= bound*rho*norm
            if core_ok:
                assert value(q, x) >= 2*sigma*norm
                assert value(slice_poly, x) >= sigma*norm
            counters["core"] += 1
    outer_ok = True
    radius = rho
    diameter = max(abs(a) for pair in sides for a in pair)
    while radius <= diameter:
        grids = [coord_grid(*sides[i], spacing[i], radius, delta, n)
                 for i in range(n)]
        m, rows = table_min(corrected(shift, n, 2*sigma),
                            grids, radius, bags, parents)
        counters["rows"] += rows
        counters["tables"] += 1
        outer_ok &= m is None or m >= sigma*radius**2/n
        counters["rounding"] += rounding_checks(
            shift, grids, radius, delta, ell, sigma, spacing)
        radius *= 2
    return core_ok, outer_ok, sigma


def main():
    counters = dict(rows=0, tables=0, core=0, rounding=0)
    fixtures = [
        ("quartic interaction",
         {(2, 0): F(1), (0, 2): F(1), (2, 2): F(1)},
         [(F(0), F(1))]*2, (F(0),)*2, [None, None],
         [(0, 1)], [-1], F(1)),
        ("Taylor quadratic negative away from core",
         {(1,): F(1), (2,): F(-1), (3,): F(1)},
         [(F(0), F(2))], (F(0),), [None], [(0,)], [-1], F(1)),
        ("mixed negative lattice derivative",
         {(2, 0): F(1), (1, 0): F(-1, 2), (0, 2): F(1),
          (2, 2): F(1, 4), (0, 4): F(1, 8)},
         [(F(0), F(2)), (F(0), F(1))], (F(0),)*2, [F(1), None],
         [(0, 1)], [-1], F(1, 2)),
        ("pure integer quartic",
         {(2,): F(1), (1,): F(-1, 2), (4,): F(1, 8)},
         [(F(0), F(3))], (F(0),), [F(1)], [(0,)], [-1], F(5, 8)),
    ]
    # A nonzero rational candidate and a nonunit rational lattice.
    center = (F(1, 3), F(0))
    displacement_poly = {(2, 0): F(1), (1, 0): F(-1, 6),
                         (0, 2): F(1), (2, 2): F(1), (0, 4): F(1, 4)}
    fixtures.append(("rational lattice and signed continuous core",
                     translate(displacement_poly, tuple(-z for z in center)),
                     [(F(0), F(1)), (F(-1, 2), F(1, 2))],
                     center, [F(1, 3), None], [(0, 1)], [-1], F(1, 2)))
    fixtures.append(("sparse polynomial path",
                     {(2, 0, 0): F(1), (0, 2, 0): F(1),
                      (0, 0, 2): F(1), (2, 2, 0): F(1),
                      (0, 2, 2): F(1)},
                     [(F(0), F(1))]*3, (F(0),)*3, [None]*3,
                     [(0, 1), (1, 2)], [-1, 0], F(1)))
    total_trials = 0
    for name, poly, bounds, v, spacing, bags, parents, g in fixtures:
        delta = F(1, 2)
        while True:
            total_trials += 1
            core, outer, sigma = trial(poly, bounds, v, spacing,
                                       bags, parents, delta, counters)
            if sigma <= g/5:
                assert core and outer, name
            if core and outer:
                assert sigma <= g, name
                print(f"PASS {name}: delta={delta}, sigma={sigma}")
                break
            delta /= 2
            assert delta >= F(1, 128)
    # Positive local quadratic and valid first-order signs do not suffice.
    wrong = {(2,): F(1), (3,): F(-3), (4,): F(2)}
    wrong_checks = 0
    for delta in (F(1, 2), F(1, 4), F(1, 8)):
        core, outer, _ = trial(wrong, [(F(0), F(1))], (F(0),),
                                [None], [(0,)], [-1], delta, counters)
        assert not outer
        if delta <= F(1, 4):
            assert core
        wrong_checks += 1
    assert value(wrong, (F(3, 4),)) < 0
    # Curvature only at lattice points does not justify the chord bound.
    h = translate({(4,): F(5, 3), (6,): F(-2, 3)}, (F(-1),))
    assert [value(h, (F(i),)) for i in range(3)] == [F(1), F(0), F(1)]
    assert all(value(second(h, 0), (F(i),)) == 0 for i in range(3))
    print(f"PASS {len(fixtures)} positive fixtures, {total_trials} trials, "
          f"{wrong_checks} rejected wrong-candidate trials; {counters}")


if __name__ == "__main__":
    main()
