"""Independent exact regressions for reopened operating-constraint arguments.

Standard library only. No imports from the investigated implementation.
Assertions deliberately use explicit exceptions, including under python -O.
"""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from random import Random
import subprocess
import sys
from pathlib import Path


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


# Work in Q[t]/(t^2-12t+4), using the root t in (1/3,3/8).
def plus(p, q):
    return p[0] + q[0], p[1] + q[1]


def scale(c, p):
    return c * p[0], c * p[1]


def times(p, q):
    return (p[0]*q[0]-4*p[1]*q[1],
            p[0]*q[1]+p[1]*q[0]+12*p[1]*q[1])


def check_irrational_example():
    zero, one, theta = (F(0), F(0)), (F(1), F(0)), (F(0), F(1))
    q = (F(1, 2), F(1, 4))
    r = (F(1, 2), F(-1, 4))
    check(plus(q, r) == one, 'branch conservation')
    check(times(q, q) == theta, 'first branch pressure')
    check(scale(2, times(r, r)) == theta, 'second branch pressure')
    # A continuous strictly decreasing polynomial changes sign once here.
    polynomial = lambda t: t*t-12*t+4
    lo, hi = F(1, 3), F(3, 8)
    check(polynomial(lo) > 0 > polynomial(hi), 'isolating interval')
    check(2*hi-12 < 0, 'strictly decreasing on interval')
    check(isqrt(128)**2 != 128, 'no rational roots')
    # Interval arithmetic proves both branch flows positive and below one.
    check(0 < F(1, 2)+lo/4 < F(1, 2)+hi/4 < 1, 'q bounds')
    check(0 < F(1, 2)-hi/4 < F(1, 2)-lo/4 < 1, 'r bounds')
    potential = [theta, zero, scale(F(1, 2), theta), scale(F(1, 2), theta)]
    edges = [(0, 1), (0, 2), (2, 1), (0, 3), (3, 1)]
    flow = [one, q, q, r, r]
    beta = [theta, scale(F(1, 2), one), scale(F(1, 2), one), one, one]
    balance = [zero]*4
    for (u, v), x, coefficient in zip(edges, flow, beta):
        check(times(coefficient, times(x, x)) == plus(potential[u], scale(-1, potential[v])), 'individual edge law')
        balance[u] = plus(balance[u], x)
        balance[v] = plus(balance[v], scale(-1, x))
    check(balance == [scale(2, one), scale(-2, one), zero, zero], 'original nominations')

    # Strengthened instance: two upper capacities force a saturated cut.
    upper_theta = plus(theta, one)
    potential = [upper_theta, zero, theta, scale(F(1, 2), theta), scale(F(1, 2), theta)]
    edges = [(0, 1), (0, 2), (2, 3), (3, 1), (2, 4), (4, 1)]
    flow = [one, one, q, q, r, r]
    beta = [upper_theta, one, scale(F(1, 2), one), scale(F(1, 2), one), one, one]
    balance = [zero]*5
    for (u, v), x, coefficient in zip(edges, flow, beta):
        check(times(coefficient, times(x, x)) == plus(potential[u], scale(-1, potential[v])), 'upper-capacity edge law')
        balance[u] = plus(balance[u], x)
        balance[v] = plus(balance[v], scale(-1, x))
    check(balance == [scale(2, one), scale(-2, one), zero, zero, zero], 'upper-capacity nominations')
    check(plus(plus(times(upper_theta, upper_theta), scale(-14, upper_theta)), scale(17, one)) == zero, 'shifted minimal polynomial')
    check(lo+1 == F(4, 3) and hi+1 == F(11, 8), 'shifted parameter interval')
    check(flow[:2] == [one, one] and plus(flow[0], flow[1]) == scale(2, one), 'saturated cut')
    check(len(edges)-len(potential)+1 == 2, 'strengthened cycle rank')


def check_scalar_and_triangle():
    phi = lambda x: x*abs(x)
    values = [F(i, 9) for i in range(-36, 37)]
    count = 0
    for x in values:
        for y in values:
            h = y-x
            check((phi(y)-phi(x))*h >= abs(h)**3/2, 'cubic monotonicity')
            check(abs(phi(y)-phi(x)) <= 8*abs(h), 'Lipschitz law')
            if h > 0:
                check(phi(y)-phi(x) >= h*abs(x)/2, 'linear-bound scalar ingredient')
            count += 1
    for A, B, q in [(F(1), F(9), F(3, 4)), (F(9), F(1), F(1, 4)), (F(5), F(5), F(1, 2))]:
        check(A*q*q == B*(1-q)**2, 'triangle equilibrium')
        check((A*q*q <= 1) == (A != 5), 'pressure filter')
    return count


def check_cycle_lemma():
    random = Random(9046)
    cases = 0
    for n in range(3, 10):
        edges = list(combinations(range(n), 2))
        indices = {e: i for i, e in enumerate(edges)}
        for _ in range(50):
            circulation = [F(0)]*len(edges)
            for _ in range(2*n):
                cycle = random.sample(range(n), random.randrange(3, n+1))
                amount = F(random.randrange(1, 10), random.randrange(1, 10))
                for u, v in zip(cycle, cycle[1:]+cycle[:1]):
                    edge = (min(u, v), max(u, v))
                    circulation[indices[edge]] += amount if u < v else -amount
            H = max(map(abs, circulation))
            check(H > 0, 'nonzero random circulation')
            threshold = H/len(edges)
            for i, value in enumerate(circulation):
                if abs(value) != H:
                    continue
                u, v = edges[i] if value > 0 else edges[i][::-1]
                reached = {v}
                while True:
                    previous = set(reached)
                    for (a, b), flow in zip(edges, circulation):
                        if flow < 0:
                            a, b = b, a
                        if abs(flow) >= threshold and a in reached:
                            reached.add(b)
                    if reached == previous:
                        break
                check(u in reached, 'max edge has a high-flow return path')
            cases += 1
    return cases


def check_physical_perturbations():
    # Triangle (0,1),(0,2),(1,2), with a zero-flow third edge at s=0.
    # The conserved perturbation changes that edge's sign through zero.
    phi = lambda x: x*abs(x)
    samples = []
    for s in [F(i, 40) for i in range(-10, 11)]:
        flow = [1+s, 1-s, s]
        potential = [F(2), phi(s), F(0)]
        beta = [(potential[0]-potential[1])/phi(flow[0]),
                (potential[0]-potential[2])/phi(flow[1]), F(1)]
        check(all(x > 0 for x in beta), 'positive resistances')
        check([flow[0]+flow[1], -flow[0]+flow[2], -flow[1]-flow[2]] == [2, -1, -1], 'fixed nominations')
        for (u, v), x, coefficient in zip([(0, 1), (0, 2), (1, 2)], flow, beta):
            check(coefficient*phi(x) == potential[u]-potential[v], 'perturbation physical edge law')
        samples.append((flow, potential, beta))
    cases = 0
    for x, pi, beta in samples:
        for y, pj, alpha in samples:
            M, m = F(2), 3
            delta = max(abs(a-b) for a, b in zip(alpha, beta))
            low, high = min(alpha+beta), max(alpha+beta)
            H = max(abs(a-b) for a, b in zip(x, y))
            check(H*H <= M*M*2*m*delta/low, 'original Holder bound')
            check(H <= 2*m*M*delta/low, 'stronger linear bound')
            check(abs((pi[0]-pi[2])-(pj[0]-pj[2])) <= delta*M*M+2*high*M*H, 'one-edge pressure bound')
            check(abs((pi[1]-pi[2])-(pj[1]-pj[2])) <= delta*M*M+2*high*M*H, 'zero-flow edge pressure bound')
            cases += 1
    return cases


def main():
    check_irrational_example()
    scalar = check_scalar_and_triangle()
    cycle = check_cycle_lemma()
    physical = check_physical_perturbations()
    author = Path(__file__).with_name('reopened_constraints_exact_checks.py')
    for optimized in (False, True):
        subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(author)], check=True)
    print(f'Independent PASS: irrational witness; {scalar} scalar pairs; {cycle} circulations; {physical} physical perturbation pairs, including zero and reversing flows.')


if __name__ == '__main__':
    main()
