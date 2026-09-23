"""Independent exact checks of the joint weighted cycle elimination.

No import from author or first-review implementations; standard library only.
The mathematical review separately covers the global approximation compiler.
"""
from fractions import Fraction as F
from itertools import product
from random import Random


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def vertex_optimum(f, weights, lower, upper):
    candidates = []
    n = len(f)
    for pivot in range(n):
        other = [i for i in range(n) if i != pivot]
        for endpoints in product((0, 1), repeat=n-1):
            beta = list(lower)
            for i, endpoint in zip(other, endpoints):
                beta[i] = upper[i] if endpoint else lower[i]
            remaining = -sum((f[i]*beta[i] for i in other), F(0))
            if f[pivot]:
                beta[pivot] = remaining/f[pivot]
                if not lower[pivot] <= beta[pivot] <= upper[pivot]:
                    continue
            elif remaining:
                continue
            require(dot(f, beta) == 0, 'enumerated vertex equality')
            candidates.append(dot([w*x for w, x in zip(weights, f)], beta))
    return max(candidates) if candidates else None


def threshold_optima(f, weights, lower, upper):
    values = []
    for multiplier in set(weights):
        beta = [None]*len(f)
        tied = []
        fixed_total = F(0)
        expression = F(0)
        for i, (x, w) in enumerate(zip(f, weights)):
            if w == multiplier:
                tied.append(i)
            else:
                beta[i] = upper[i] if (w-multiplier)*x > 0 else lower[i]
                fixed_total += x*beta[i]
                expression += (w-multiplier)*x*beta[i]
        low = sum((min(lower[i]*f[i], upper[i]*f[i]) for i in tied), F(0))
        high = sum((max(lower[i]*f[i], upper[i]*f[i]) for i in tied), F(0))
        if not fixed_total+low <= 0 <= fixed_total+high:
            continue
        remaining = -fixed_total-low
        interiors = 0
        for i in tied:
            if not f[i]:
                beta[i] = lower[i]
                continue
            contribution = min(lower[i]*f[i], upper[i]*f[i])
            width = abs(f[i])*(upper[i]-lower[i])
            increment = min(width, remaining)
            beta[i] = (contribution+increment)/f[i]
            remaining -= increment
            interiors += lower[i] < beta[i] < upper[i]
        require(remaining == 0, 'greedy residual exhausted')
        require(interiors <= 1, 'at most one interior tied resistance')
        require(all(a <= b <= c for a, b, c in zip(lower, beta, upper)), 'recovered box')
        require(dot(f, beta) == 0, 'recovered circulation law')
        objective = dot([w*x for w, x in zip(weights, f)], beta)
        require(objective == expression, 'threshold value identity')
        values.append(objective)
    return values


def test_lp():
    random = Random(6409)
    totals = dict(cases=0, infeasible=0, zero=0, tied=0)
    for n in range(3, 8):
        for index in range(80):
            f = [F(random.randrange(-4, 5)) for _ in range(n)]
            if index % 20 == 0:
                f = [F(0)]*n
            weights = [F(random.randrange(-2, 3)) for _ in range(n)]
            if index % 10 == 0:
                weights = [F(1)]*n
            lower = [F(random.randrange(1, 5), 3) for _ in range(n)]
            upper = [a+F(random.randrange(4), 2) for a in lower]
            expected = vertex_optimum(f, weights, lower, upper)
            actual = threshold_optima(f, weights, lower, upper)
            require((expected is None) == (not actual), 'threshold feasibility coverage')
            require(all(value == expected for value in actual), 'all feasible thresholds achieve LP optimum')
            totals['cases'] += 1
            totals['infeasible'] += expected is None
            totals['zero'] += not any(f)
            totals['tied'] += len(set(weights)) < n
    return totals


def test_root_values():
    random = Random(4690)
    cases = 0
    for _ in range(500):
        # General quadratic boundary a*q²+b*q+c=0 with rational roots.
        a = F(random.choice([-4, -3, -2, -1, 1, 2, 3, 4]), 3)
        b = F(random.randrange(-6, 7), 4)
        radical = F(random.randrange(7), 3)
        c = (b*b-radical*radical)/(4*a)
        A, B, C = [F(random.randrange(-5, 6), 3) for _ in range(3)]
        for sign in (-1, 1):
            q = (-b+sign*radical)/(2*a)
            require(a*q*q+b*q+c == 0, 'quadratic boundary')
            require(sign*(2*a*q+b) >= 0, 'root selector including double roots')
            # Substitute q²=(-b*q-c)/a then substitute q explicitly.
            linear = B-A*b/a
            polynomial = C-A*c/a-linear*b/(2*a)
            coefficient = sign*linear/(2*a)
            require(A*q*q+B*q+C == polynomial+coefficient*radical, 'polynomial plus radical value')
            cases += 1
    return cases


if __name__ == '__main__':
    print('PASS:', test_lp(), 'LP cases;', test_root_values(), 'quadratic-root identities.')
