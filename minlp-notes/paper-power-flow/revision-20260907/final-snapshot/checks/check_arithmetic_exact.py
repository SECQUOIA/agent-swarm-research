#!/usr/bin/env python3
"""Exact checks of Appendix A's actual bounded addition/inversion equations.

The checker composes all gates into a circuit for a compact basic closed disk,
checks original final equations and every variable bound, and rejects altered
values and outside points. Finite checks do not prove universality, global
range existence, triangulation, or the basic-closed obstruction.
"""
from fractions import Fraction as F
from itertools import product


class Bounded:
    def __init__(self):
        self.values = []
        self.equations = []
        self.one = self.new(F(1))
        self.equations.append(('inv', self.one, self.one))
        self.half = self.halve(self.one)
        self.threehalves = self.add(self.one, self.half)
        self.threequarters = self.halve(self.threehalves)
        self.two = self.add(self.one, self.one)
        self.twothirds = self.inv(self.threehalves)

    def new(self, value):
        self.values.append(F(value))
        return len(self.values) - 1

    def add(self, a, b, out=None):
        if out is None:
            out = self.new(self.values[a] + self.values[b])
        self.equations.append(('add', a, b, out))
        return out

    def sub(self, a, b, out=None):
        if out is None:
            out = self.new(self.values[a] - self.values[b])
        self.add(out, b, a)
        return out

    def halve(self, a):
        out = self.new(self.values[a] / 2)
        self.add(out, out, a)
        return out

    def inv(self, a):
        out = self.new(1 / self.values[a])
        self.equations.append(('inv', a, out))
        return out

    def square(self, a, out=None):
        b = self.add(a, self.half)
        bp, ap = self.inv(b), self.inv(a)
        c = self.add(ap, self.half)
        d = self.sub(c, self.twothirds)
        e = self.add(d, self.half)
        f = self.sub(e, bp)
        g = self.add(f, f)
        h = self.sub(g, self.twothirds)
        i = self.inv(h)
        assert self.values[h] == 1 / (self.values[a] * self.values[b])
        j = self.sub(i, self.half)
        k = self.add(j, self.threequarters)
        l = self.halve(b)
        return self.sub(k, l, out)

    def multiply(self, a, b, out=None):
        ap, bp = self.add(a, self.half), self.add(b, self.half)
        ha, hb = self.halve(ap), self.halve(bp)
        t = self.add(ha, hb)
        r = self.sub(t, self.half)
        s = self.square(r)
        u = self.add(s, self.half)
        a2, b2 = self.square(a), self.square(b)
        a3, b3 = self.add(a2, self.half), self.add(b2, self.half)
        a4, b4 = self.halve(a3), self.halve(b3)
        c = self.add(a4, b4)
        d = self.halve(c)
        e = self.sub(u, d)
        f = self.add(e, e)
        return self.sub(f, self.half, out)

    def violations(self):
        bad = []
        for i, v in enumerate(self.values):
            if not F(1, 2) <= v <= 2:
                bad.append(('bound', i))
        for i, eq in enumerate(self.equations):
            if eq[0] == 'add':
                _, a, b, c = eq
                ok = self.values[a] + self.values[b] == self.values[c]
            else:
                _, a, b = eq
                ok = self.values[a] * self.values[b] == 1
            if not ok:
                bad.append(('equation', i))
        return bad


def shifted_system(values, equations, nonnegative, ell=16, k=5):
    """Encode the actual AMI circuit using only final add/inv constraints."""
    delta, eps = F(1, 2**ell), F(1, 2**(ell + k))
    small = {'delta': delta, 'zero': F(0)}
    small_eq = [('add', 'zero', 'delta', 'delta')]
    previous = 'delta'
    for j in range(k):
        nxt = f'halving{j}'
        small[nxt] = small[previous] / 2
        small_eq.append(('add', nxt, nxt, previous))
        previous = nxt
    epsilon_name = previous
    for name, value in values.items():
        small['w_' + name] = eps * value
    for i, eq in enumerate(equations):
        if eq[0] == 'one':
            small_eq.append(('add', 'w_' + eq[1], 'zero', epsilon_name))
        else:
            op, x, y, z = eq
            wx, wy, wz = ['w_' + name for name in (x, y, z)]
            if op == 'add':
                small_eq.append(('add', wx, wy, wz))
            else:
                q = f'q{i}'
                small[q] = eps * eps * values[z]
                small_eq += [('mul', wx, wy, q), ('mul', epsilon_name, wz, q)]
    net = Bounded()
    a, b, c = {}, {}, {}
    for name, value in small.items():
        a[name] = net.new(1 + value)
        c[name] = net.add(a[name], net.half)
        b[name] = net.sub(c[name], net.threequarters)
    midpoint = net.half
    for _ in range(1, ell):
        midpoint = net.halve(net.add(midpoint, net.one))
    assert net.values[midpoint] == 1 - delta
    net.add(a['delta'], midpoint, net.two)
    for op, s, t, u in small_eq:
        if op == 'add':
            net.add(b[s], b[t], c[u])
        else:
            m = net.multiply(a[s], a[t])
            f = net.add(m, net.half)
            g = net.sub(f, b[t])
            h = net.add(g, net.threequarters)
            net.add(b[u], b[s], h)
    for name in nonnegative:
        net.sub(a['w_' + name], net.half)
    for name, value in values.items():
        assert (net.values[a['w_' + name]] - 1) / eps == value
    return net


def main():
    samples = [F(i, 100000) for i in range(-20, 21)]
    for x, y in product(samples, repeat=2):
        net = Bounded()
        a, b = net.new(1 + x), net.new(1 + y)
        out = net.multiply(a, b)
        assert net.values[out] == (1 + x) * (1 + y)
        assert not net.violations()
    print(f'PASS: {len(samples)**2} composed multiplication/reciprocal gate profiles.')

    equations = [('one', 'one'), ('add', 'zero', 'one', 'one'),
                 ('mul', 'x', 'x', 'xx'), ('mul', 'y', 'y', 'yy'),
                 ('add', 'xx', 'yy', 'sum'), ('add', 'sum', 'slack', 'one')]
    inside = outside = altered = 0
    maximum = (0, 0)
    for x, y in product([F(i, 4) for i in range(-5, 6)], repeat=2):
        values = dict(one=F(1), zero=F(0), x=x, y=y,
                      xx=x*x, yy=y*y, sum=x*x+y*y, slack=1-x*x-y*y)
        net = shifted_system(values, equations, ['slack'])
        bad = net.violations()
        if x*x + y*y <= 1:
            assert not bad
            inside += 1
        else:
            assert bad and all(kind == 'bound' for kind, _ in bad)
            outside += 1
        maximum = max(maximum, (len(net.values), len(net.equations)))
        if x*x + y*y <= 1:
            values['xx'] += F(1, 16)
            modified = shifted_system(values, equations, ['slack'])
            assert any(kind == 'equation' for kind, _ in modified.violations())
            altered += 1
    print(f'PASS: full disk circuit: {inside} feasible profiles, {outside} outside points, '
          f'{altered} inconsistent circuit profiles; {maximum[0]} variables, '
          f'{maximum[1]} original final equations per profile.')

    for ell, k in product((4, 12, 32), (0, 1, 20)):
        net = shifted_system({'one': F(1)}, [('one', 'one')], [], ell, k)
        assert not net.violations()
    print('PASS: nine exact delta/midpoint/epsilon/halving configurations, including k=0.')

    # A cycle's standard-simplex nonfaces are its two diagonals (and supersets).
    faces = [set(), {0}, {1}, {2}, {3}, {0, 1}, {1, 2}, {2, 3}, {0, 3}]
    count = 0
    for numerators in product(range(5), repeat=4):
        if sum(numerators) != 4:
            continue
        z = [F(v, 4) for v in numerators]
        constraints = z[0] * z[2] == 0 and z[1] * z[3] == 0
        assert constraints == ({i for i, v in enumerate(z) if v} in faces)
        count += 1
    print(f'PASS: {count} simplex grid profiles agree with nonface/support membership.')
    print('Finite exact checks supplement the proofs; no quantified universality claim is inferred from samples.')


if __name__ == '__main__':
    main()
