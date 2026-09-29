#!/usr/bin/env python3
"""Exact finite challenges for Sections 5--6 and the star appendix.

Only the Python standard library is needed. Quadratics are assembled from
the original residual rows, then optimized by rational linear algebra. The
tests challenge the stated formulas; they do not prove asymptotic results.
"""

from fractions import Fraction as F
from itertools import permutations, product


def solve(matrix, rhs):
    """Solve a nonsingular rational system, including the empty system."""
    n = len(rhs)
    a = [[F(v) for v in row] + [F(rhs[i])] for i, row in enumerate(matrix)]
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        div = a[k][k]
        a[k] = [v / div for v in a[k]]
        for i in range(n):
            if i != k:
                mul = a[i][k]
                a[i] = [v - mul * u for v, u in zip(a[i], a[k])]
    return [row[-1] for row in a]


def inverse(matrix):
    n = len(matrix)
    cols = [solve(matrix, [F(i == j) for i in range(n)]) for j in range(n)]
    return [[cols[j][i] for j in range(n)] for i in range(n)]


class Quadratic:
    """A residual-built objective x'Qx+c'x+constant+penalty'z."""

    def __init__(self, n):
        self.n = n
        self.q = [[F(0) for _ in range(n)] for _ in range(n)]
        self.c = [F(0)] * n
        self.penalty = [F(0)] * n
        self.constant = F(0)

    def square(self, row, target=0):
        target = F(target)
        self.constant += target * target
        for i, vi in row.items():
            self.c[i] -= 2 * vi * target
            for j, vj in row.items():
                self.q[i][j] += vi * vj

    def optimum(self, bits, fixed=None):
        fixed = {} if fixed is None else fixed
        assert all(bits[i] or value == 0 for i, value in fixed.items())
        x = [F(fixed.get(i, 0)) for i in range(self.n)]
        free = [i for i in range(self.n) if bits[i] and i not in fixed]
        rhs = [-self.c[i] / 2 - sum(self.q[i][j] * x[j] for j in fixed)
               for i in free]
        answer = solve([[self.q[i][j] for j in free] for i in free], rhs)
        for i, value in zip(free, answer):
            x[i] = value
        value = (self.constant + sum(a * b for a, b in zip(self.penalty, bits))
                 + sum(a * b for a, b in zip(self.c, x))
                 + sum(x[i] * self.q[i][j] * x[j]
                       for i in range(self.n) for j in range(self.n)))
        return value, x


def all_bits(n):
    return product((0, 1), repeat=n)


def chain(amplitudes, controls, theta, target=None, state_penalty=0, shift=0):
    """Build original expanded residual model, before choosing any bits."""
    n = len(amplitudes)
    obj = Quadratic(2 * n)
    for i, amplitude in enumerate(amplitudes):
        x, state = 2 * i, 2 * i + 1
        obj.square({x: F(1)})
        obj.c[x] -= 2 * amplitude
        obj.penalty[x] = amplitude * amplitude
        obj.penalty[state] = state_penalty
        row = {state: F(1), x: -controls[i]}
        if i:
            row[state - 2] = -theta
        intercept = F(shift) if i == 0 else shift * (1 - theta)
        obj.square(row, intercept)
    if target is not None:
        obj.square({2 * n - 1: theta}, theta * (shift + target))
    return obj


def check_matrix(obj, theta):
    for i, row in enumerate(obj.q):
        radius = sum(abs(v) for j, v in enumerate(row) if i != j)
        assert row[i] - radius >= 1 - 3 * theta
        assert row[i] + radius <= 1 + 3 * theta + 2 * theta * theta
        assert sum(v != 0 for j, v in enumerate(row) if i != j) <= 4
        assert all(v == 0 for j, v in enumerate(row) if abs(i - j) > 2)


def check_hardness():
    instances = [([1, 3], 2), ([1, 3], 3), ([2, 3, 6], 4),
                 ([2, 3, 6], 5), ([2, 2, 5], 8), ([2, 2, 5], 9)]
    count = 0
    scales = 0
    for theta in (F(1, 10), F(1, 20)):
        delta = theta**2 * (1 - theta**2) / (1 + theta**4)
        for a, target in instances:
            n = len(a)
            yes = any(sum(ai * zi for ai, zi in zip(a, z)) == target
                      for z in all_bits(n))
            amplitudes = [F(ai) * theta**(-(n - i)) for i, ai in enumerate(a)]
            eta = delta / (4 * n)
            fixed = chain(amplitudes, [theta] * n, theta, target, eta)
            bound = 1 + target + sum(amplitudes)
            normalized = chain([v / bound for v in amplitudes], [theta] * n,
                               theta, F(target) / bound, eta / bound**2)
            controls = [F(ai, sum(a)) * theta**(i + 1)
                        for i, ai in enumerate(a)]
            terminal = F(target, sum(a)) * theta**n
            unit = chain([F(1)] * n, controls, theta, terminal, F(1), F(4))
            for obj in (fixed, normalized, unit):
                check_matrix(obj, theta)
            assert fixed.q == normalized.q
            assert all(abs(v) <= 2 for v in normalized.c)
            assert all(0 < v <= 1 for v in normalized.penalty)
            assert unit.penalty == [1] * (2 * n)
            assert all(abs(v) <= 9 for v in unit.c)
            best = [None] * 3
            unit_argmins = []
            for bits in all_bits(2 * n):
                vals = [obj.optimum(bits)[0] for obj in (fixed, normalized, unit)]
                assert vals[1] * bound**2 == vals[0]
                for j, value in enumerate(vals):
                    if best[j] is None or value < best[j]:
                        best[j] = value
                        if j == 2:
                            unit_argmins = [bits]
                    elif j == 2 and value == best[j]:
                        unit_argmins.append(bits)
                count += 3
            assert (best[0] <= delta / 4) if yes else (best[0] > delta)
            assert (best[2] == n) if yes else (best[2] > n)
            assert all(all(bits[1::2]) for bits in unit_argmins)
            if not yes:
                gap = (theta**(2*n) / sum(a)**2
                       / (theta**(2*n) * sum(ai*ai for ai in a) / sum(a)**2
                          + sum(theta**(2*j) for j in range(n)) + theta**(-2)))
                assert best[2] - n >= gap
            # Scaling is checked by rebuilding residuals and independently solving.
            sigma = F(1, 3)
            scale = 1 + int(8 * (2 * n) * (1 + sigma) / delta) + 1
            scaled = chain([scale * v for v in amplitudes], [theta] * n,
                           theta, scale * target, scale**2 * eta)
            lower = scale**2 * delta / 4 + 2 * n * sigma
            upper = scale**2 * delta - 2 * n * sigma
            assert lower < upper
            for noise in ([sigma] * (2 * n), [-sigma] * (2 * n),
                          [sigma * (-1)**i for i in range(2 * n)]):
                assert all(p + xi > 0 for p, xi in zip(scaled.penalty, noise))
                noisy = min(scaled.optimum(bits)[0]
                            + sum(xi * zi for xi, zi in zip(noise, bits))
                            for bits in all_bits(2 * n))
                assert (noisy <= lower) if yes else (noisy > upper)
                scales += 1
    return count, scales


def branches(n, theta, controls=None):
    controls = [theta] * n if controls is None else controls
    weight = [theta**(n - i - 1) for i in range(n)]
    w = sum(v * v for v in weight)
    return {z: (sum(v * b * bit for v, b, bit in zip(weight, controls, z)),
                w + sum(v * v * b * b * bit
                        for v, b, bit in zip(weight, controls, z)))
            for z in all_bits(n)}


def value(branch, t):
    center, denominator = branch
    return (t - center)**2 / denominator


def check_messages():
    qps = pruning = lower_tests = lifts = short = 0
    for theta in (F(1, 10), F(1, 20)):
        ctheta = (1 + theta**2) / (1 - theta**2)
        for n in range(1, 7):
            formulas = branches(n, theta)
            centers = sorted(c for c, _ in formulas.values())
            assert min(b - a for a, b in zip(centers, centers[1:])) == theta**n
            assert all(1 <= den <= ctheta for _, den in formulas.values())
            probes = sorted(set([F(0), F(1), F(1, 2)] + centers
                                + [(a + b) / 2 for a, b in zip(centers, centers[1:])]))
            if n <= 4:
                obj = chain([F(1)] * n, [theta] * n, theta)
                check_matrix(obj, theta)
                for z, branch in formulas.items():
                    bits = tuple(item for bit in z for item in (bit, 1))
                    for t in (F(0), F(1, 3), F(1)):
                        result, _ = obj.optimum(bits, {2 * n - 1: t})
                        assert result == value(branch, t)
                        qps += 1
            for z, branch in formulas.items():
                center = branch[0]
                for t in (max(F(0), center - theta**n / 3),
                          min(F(1), center + theta**n / 3)):
                    assert all(value(branch, t) < value(other, t)
                               for other_z, other in formulas.items() if other_z != z)
            for m in range(n + 1):
                delta = sum(theta**j for j in range(m + 1, n + 1))
                beta = sum(theta**(2 * j) for j in range(m + 1, n + 1))
                zeros = [v for z, v in formulas.items() if not any(z[:n - m])]
                extremes = [v for z, v in formulas.items()
                            if not any(z[:n - m]) or all(z[:n - m])]
                for t in probes:
                    exact = min(value(v, t) for v in formulas.values())
                    error0 = min(value(v, t) for v in zeros) - exact
                    error = min(value(v, t) for v in extremes) - exact
                    assert 0 <= error0 <= 2 * delta + beta
                    assert 0 <= error <= delta**2 / 4 + beta
                    pruning += 2
                if m:
                    zero_centers = [v[0] for v in zeros]
                    eps = theta**(2 * m) / (8 * ctheta)
                    for branch in formulas.values():
                        assert sum(value(branch, t) <= eps for t in zero_centers) <= 1
                        lower_tests += 1
            if n <= 3:
                lifted = chain([F(1)] * n, [theta] * n, theta,
                               state_penalty=F(1), shift=F(4))
                for t in (F(0), F(1, 2), F(1)):
                    candidates = [(lifted.optimum(bits, {2 * n - 1: 4 + t})[0], bits)
                                  for bits in all_bits(2 * n) if bits[-1]]
                    optimum = min(v for v, _ in candidates)
                    assert optimum == n + min(value(v, t) for v in formulas.values())
                    assert all(all(bits[1::2]) for v, bits in candidates if v == optimum)
                    lifts += len(candidates)
            controls = [F(2**i, 2**n - 1) * theta**(i + 1) for i in range(n)]
            varying = branches(n, theta, controls)
            h = theta**n / (2**n - 1)
            for k in range(2 * (2**n - 1) + 1):
                t = k * h / 2
                optimum = min(value(v, t) for v in varying.values())
                assert 0 <= optimum <= h*h / 4
                assert 0 <= value(varying[(1,) * n], t) - optimum <= theta**(2*n)
                short += 1
            for t in (theta**n, F(1, 2), F(1)):
                assert min(value(v, t) for v in varying.values()) == value(varying[(1,) * n], t)
                short += 1
            if n <= 3:
                obj = chain([F(1)] * n, controls, theta)
                for z, branch in varying.items():
                    bits = tuple(item for bit in z for item in (bit, 1))
                    result, _ = obj.optimum(bits, {2 * n - 1: F(1, 7)})
                    assert result == value(branch, F(1, 7))
                    qps += 1
    return qps, pruning, lower_tests, lifts, short


def star(weights):
    n = len(weights)
    q = [[F(i == j) for j in range(n + 1)] for i in range(n + 1)]
    for i, b in enumerate(weights, 1):
        q[0][i] = q[i][0] = b
    return q


def padded_inverse(q, support):
    out = [[F(0) for _ in q] for _ in q]
    block = inverse([[q[i][j] for j in support] for i in support])
    for a, i in enumerate(support):
        for b, j in enumerate(support):
            out[i][j] = block[a][b]
    return out


def check_faces():
    atoms = faces = 0
    for m in range(1, 5):
        b = F(1, 2 * m)
        q = star([b] * (2 * m))
        tau = 1 / (1 - m * b * b)
        for bits in all_bits(2 * m + 1):
            z = bits[1:]
            w = padded_inverse(q, [i for i, bit in enumerate(bits) if bit])
            t = 1 / (1 - b*b*sum(z)) if bits[0] else F(0)
            assert w[0][0] == t
            assert all(w[0][i+1] == -b*t*z[i] for i in range(2*m))
            assert all(w[i+1][j+1] == F(i == j)*z[i] + b*b*t*z[i]*z[j]
                       for i in range(2*m) for j in range(2*m))
            g = ((m+1)*(1-bits[0]) + m - sum(z)
                 + sum(w[i+1][m+i+1] for i in range(m)) / (b*b))
            on_face = bool(bits[0] and all(z[i] + z[m+i] == 1 for i in range(m)))
            assert (g == 0) == on_face
            if not on_face:
                assert g >= b*b
            else:
                x = [[F(z[i]) if i == j else w[i+1][j+1]/(b*b*tau)
                      for j in range(m)] for i in range(m)]
                a = [x[i][i] for i in range(m)]
                recovered = a + [1-v for v in a]
                assert tuple(recovered) == z
                r = [[x[i][j] for j in range(m)]
                     + [a[i]-x[i][j] for j in range(m)] for i in range(m)]
                r += [[a[j]-x[i][j] for j in range(m)]
                      + [1-a[i]-a[j]+x[i][j] for j in range(m)] for i in range(m)]
                assert all(w[i+1][j+1] == F(i == j)*recovered[i] + b*b*tau*r[i][j]
                           for i in range(2*m) for j in range(2*m))
                faces += 1
            flipped = [[v * (-1 if (i == 0) != (j == 0) else 1)
                        for j, v in enumerate(row)] for i, row in enumerate(q)]
            wf = padded_inverse(flipped, [i for i, bit in enumerate(bits) if bit])
            assert all(wf[i][j] == w[i][j] * (-1 if (i == 0) != (j == 0) else 1)
                       for i in range(2*m+1) for j in range(2*m+1))
            atoms += 1
    return atoms, faces


def project_row(q, index, selected):
    """Residual coordinates in the original independent factor-row basis."""
    row = [F(i == index) for i in range(len(q))]
    coeff = solve([[q[i][j] for j in selected] for i in selected],
                  [q[i][index] for i in selected])
    for i, c in zip(selected, coeff):
        row[i] -= c
    return tuple(row)


def projective_signature(row):
    first = next(v for v in row if v)
    return tuple(v / first for v in row)


def check_diagrams():
    orders = states = 0
    for n in range(1, 5):
        b = F(1, 2*n)
        q = star([b] * n)
        for order in permutations(range(n+1)):
            last_position = max(i for i, vertex in enumerate(order) if vertex)
            last = order[last_position]
            past = order[:last_position]
            leaves = [i for i in past if i]
            assert len(leaves) == n - 1
            signatures = set()
            for bits in all_bits(n-1):
                selected_leaves = [i for i, bit in zip(leaves, bits) if bit]
                root_past = 0 in past
                selected = selected_leaves + ([0] if root_past else [])
                index = last if root_past else 0
                row = project_row(q, index, selected)
                residual_root = [F(i == 0) - (b if i in selected_leaves else 0)
                                 for i in range(n+1)]
                d = 1 - len(selected_leaves)*b*b
                expected = (tuple(F(i == last) - b/d*residual_root[i]
                                  for i in range(n+1)) if root_past else tuple(residual_root))
                assert row == expected
                signatures.add(projective_signature(row))
                states += 1
            assert len(signatures) == 2**(n-1)
            orders += 1
    return orders, states


if __name__ == "__main__":
    hardness, scales = check_hardness()
    qps, pruning, lower, lifts, short = check_messages()
    atoms, faces = check_faces()
    orders, states = check_diagrams()
    print(f"PASS: {hardness} hardness support QPs; {scales} bounded-noise scaling cases")
    print(f"PASS: {qps} message support QPs; {pruning} pruning inequalities; "
          f"{lower} separated-center checks; {lifts} state-lift supports; "
          f"{short} short-approximation probes")
    print(f"PASS: {atoms} star atoms; {faces} face inverses; "
          f"{orders} variable orders; {states} projective residual states")
