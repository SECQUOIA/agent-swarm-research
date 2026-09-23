"""Original-network versus local-only LP fibers for the all-contract theorem.

The original LP includes every actual pool arc and both pool balances.
The local LP includes only bypass arcs and node rows. Tests check the
elimination mapping, not the quasipolynomial symbolic projection algorithm.
"""
from fractions import Fraction as F
from random import Random

import numpy as np
from scipy.optimize import linprog


class LP:
    def __init__(self, bounds):
        self.names = list(bounds)
        self.index = {name: i for i, name in enumerate(self.names)}
        self.bounds = [bounds[name] for name in self.names]
        self.eq, self.beq, self.ub, self.bub = [], [], [], []

    def add(self, terms, rhs, equal=False):
        row = [F(0)] * len(self.names)
        for name, coef in terms.items():
            row[self.index[name]] += coef
        rows, bounds = (self.eq, self.beq) if equal else (self.ub, self.bub)
        rows.append(row)
        bounds.append(F(rhs))

    def feasible(self):
        if not self.names:
            return all(v == 0 for v in self.beq) and all(v >= 0 for v in self.bub)
        result = linprog(np.zeros(len(self.names)),
                         A_ub=np.asarray(self.ub, dtype=float) if self.ub else None,
                         b_ub=np.asarray(self.bub, dtype=float) if self.ub else None,
                         A_eq=np.asarray(self.eq, dtype=float) if self.eq else None,
                         b_eq=np.asarray(self.beq, dtype=float) if self.eq else None,
                         bounds=self.bounds, method='highs')
        assert result.status in (0, 2), result.message
        return result.status == 0


def compare(net, q, enforce_constants=True, pool_cap=None):
    C, a, B, b, edges, feeds, outlets = net
    n, m = len(C), len(B)
    z_bounds = {('z', i, j): (0, 2) for i, j in edges}
    original = LP({**z_bounds,
                   **{('y', i): (0, cap) for i, cap in feeds.items()},
                   **{('v', j): (0, cap) for j, cap in outlets.items()}})
    local = LP(z_bounds)
    for i in range(n):
        terms = {('z', ii, j): F(1) for ii, j in edges if ii == i}
        original.add({**terms, **({('y', i): F(1)} if i in feeds else {})}, a[i], True)
        if i in feeds:
            local.add(terms, a[i])
            local.add({key: -val for key, val in terms.items()}, feeds[i]-a[i])
        else:
            local.add(terms, a[i], True)
    for j in range(m):
        terms = {('z', i, jj): F(1) for i, jj in edges if jj == j}
        original.add({**terms, **({('v', j): F(1)} if j in outlets else {})}, b[j], True)
        if j in outlets:
            local.add(terms, b[j])
            local.add({key: -val for key, val in terms.items()}, outlets[j]-b[j])
        else:
            local.add(terms, b[j], True)
        quality = {('z', i, jj): C[i] for i, jj in edges if jj == j}
        original.add({**quality, **({('v', j): q} if j in outlets else {})}, B[j]*b[j], True)
        local.add({('z', i, jj): C[i]-q for i, jj in edges if jj == j},
                  b[j]*(B[j]-q), True)
    original.add({**{('y', i): F(1) for i in feeds},
                  **{('v', j): F(-1) for j in outlets}}, 0, True)
    original.add({**{('y', i): C[i] for i in feeds},
                  **{('v', j): -q for j in outlets}}, 0, True)
    if pool_cap is not None:
        original.add({('y', i): F(1) for i in feeds}, pool_cap)
    constants = (sum(a) == sum(b) and
                 sum(ci*ai for ci, ai in zip(C, a)) == sum(bj*dj for bj, dj in zip(B, b)))
    return original.feasible(), local.feasible() and (constants or not enforce_constants)


def instances():
    rng = Random(90713)
    for case in range(24):
        n = 3 + case % 6
        C = [F(rng.randrange(5)) for _ in range(n)]
        # A full alternating cycle, or paths/isolated nodes obtained by cuts.
        all_edges = [(i, i) for i in range(n)] + [(i, (i+1) % n) for i in range(n)]
        edges = [edge for edge in all_edges if case % 3 == 0 or rng.random() > .3]
        z = {edge: F(rng.randrange(5), 4) for edge in edges}
        feed_set = {i for i in range(n) if rng.random() > .25} | {0}
        outlet_set = {j for j in range(n) if rng.random() > .25} | {0}
        y = {i: F(rng.randrange(1, 5), 4) for i in feed_set}
        T = sum(y.values())
        q = sum(C[i]*flow for i, flow in y.items()) / T
        shares = {j: rng.randrange(1, 5) for j in outlet_set}
        v = {j: T*weight/sum(shares.values()) for j, weight in shares.items()}
        a = [y.get(i, F(0)) + sum(flow for (ii, _), flow in z.items() if ii == i)
             for i in range(n)]
        b = [v.get(j, F(0)) + sum(flow for (_, jj), flow in z.items() if jj == j)
             for j in range(n)]
        B = [(q*v.get(j, F(0)) + sum(C[i]*flow for (i, jj), flow in z.items() if jj == j))/b[j]
             if b[j] else F(0) for j in range(n)]
        feeds = {i: max(F(2), 2*flow) for i, flow in y.items()}
        outlets = {j: max(F(2), 2*flow) for j, flow in v.items()}
        yield (C, a, B, b, edges, feeds, outlets), q


def main():
    checks = feasible = 0
    for case, (net, q) in enumerate(instances()):
        for test_q in sorted({q, *(F(j, 2) for j in range(9))}):
            full, reduced = compare(net, test_q)
            assert full == reduced, (case, test_q, full, reduced)
            checks += 1
            feasible += full
        assert compare(net, q) == (True, True)
    # Exact, small controls: omitting either global constant admits fake pooling.
    mass_bad = [F(1)], [F(1)], [F(1)], [F(2)], [], {0: F(2)}, {0: F(2)}
    quality_bad = [F(0)], [F(1)], [F(1)], [F(1)], [], {0: F(1)}, {0: F(1)}
    for net in (mass_bad, quality_bad):
        assert compare(net, F(1), enforce_constants=False) == (False, True)
        assert compare(net, F(1)) == (False, False)
    # The proof excludes a restrictive common pool capacity for a reason.
    cap_net = ([F(0), F(2)], [F(1), F(1)], [F(1, 2), F(3, 2)],
               [F(1), F(1)], [(0, 0), (1, 1)], {0: F(1), 1: F(1)}, {0: F(1), 1: F(1)})
    assert compare(cap_net, F(1)) == (True, True)
    assert compare(cap_net, F(1), pool_cap=F(3, 4)) == (False, True)
    print(f'PASS: {checks} original-pool/local-only fixed-quality comparisons; {feasible} feasible.')
    print('PASS: global mass, global quality, and common-capacity negative controls.')
    print('Checks validate elimination; no symbolic parameter-projection implementation is tested.')


if __name__ == '__main__':
    main()
