"""Bounded LP checks of continuous circuit wires and signed interpolation.

Only index bits are fixed to integers. HiGHS optimizes every internal wire
and product both ways; this checks uniqueness, rather than only inserting
the intended witness. This numerical check supplements the exact induction.
"""
from fractions import Fraction
from itertools import product

import numpy as np
from scipy.optimize import linprog


class Circuit:
    def __init__(self):
        self.bounds, self.ub, self.eq = [], [], []
        self.expected = []

    def var(self, value, bounds=(0, 1)):
        i = len(self.bounds)
        self.bounds.append(bounds)
        self.expected.append(value)
        return i

    def not_(self, a):
        v = self.var(1-self.expected[a])
        self.eq.append(({v: 1, a: 1}, 1))
        return v

    def and_(self, a, b):
        v = self.var(self.expected[a]*self.expected[b])
        self.ub.extend([({v: 1, a: -1}, 0), ({v: 1, b: -1}, 0),
                        ({a: 1, b: 1, v: -1}, 1)])
        return v

    def or_(self, a, b):
        return self.not_(self.and_(self.not_(a), self.not_(b)))

    def combine(self, entries, op, neutral):
        if not entries:
            return self.var(neutral, (neutral, neutral))
        value = entries[0]
        for other in entries[1:]:
            value = op(value, other)
        return value

    def matrices(self, rows):
        a, b = [], []
        for coefficients, rhs in rows:
            row = np.zeros(len(self.bounds))
            for i, c in coefficients.items():
                row[i] += c
            a.append(row)
            b.append(rhs)
        return np.array(a), np.array(b)


checks = invalid = 0
for length, cells in [(0, 1), (2, 3), (3, 5)]:
    # Signed coordinates, a duplicate input knot and a reversed segment.
    knots = [(Fraction(x, 7), Fraction(y, 11)) for x, y in
             [(-4, 3), (2, -5), (2, -2), (1, 7), (5, -9), (7, 4)]]
    for digits in product([0, 1], repeat=length):
        index = sum(v*2**i for i, v in enumerate(digits))
        for theta in [0, Fraction(1, 7), Fraction(1, 2), 1]:
            c = Circuit()
            bits = [c.var(v, (v, v)) for v in digits]
            neg = [c.not_(v) for v in bits]
            selectors = [c.combine([bits[i] if k >> i & 1 else neg[i]
                                    for i in range(length)], c.and_, 1)
                         for k in range(cells)]
            valid = c.combine(selectors, c.or_, 0)
            c.eq.append(({valid: 1}, 1))
            weight = c.var(theta, (float(theta), float(theta)))
            # Fixed offset -16 and 6 numerator bits cover both signed axes.
            decoded = []
            for side, denominator in product([0, 1], [7, 11]):
                axis = 0 if denominator == 7 else 1
                terms = []
                for place in range(6):
                    selected = [selectors[k] for k in range(cells)
                                if int(knots[k+side][axis]*denominator+16) >> place & 1]
                    wire = c.combine(selected, c.or_, 0)
                    p = c.and_(wire, weight)
                    terms.append((wire, p, Fraction(2**place, denominator)))
                decoded.append(terms)
            au, bu = c.matrices(c.ub)
            ae, be = c.matrices(c.eq)
            if index >= cells:
                result = linprog(np.zeros(len(c.bounds)), A_ub=au, b_ub=bu,
                                 A_eq=ae, b_eq=be, bounds=c.bounds, method='highs')
                assert result.status == 2
                invalid += 1
                continue
            for i, expected in enumerate(c.expected):
                for sign in [-1, 1]:
                    objective = np.zeros(len(c.bounds))
                    objective[i] = sign
                    result = linprog(objective, A_ub=au, b_ub=bu,
                                     A_eq=ae, b_eq=be, bounds=c.bounds, method='highs')
                    assert result.success, result.message
                    assert abs(result.fun-sign*float(expected)) < 1e-8
                    checks += 1
            for axis, denominator in enumerate([7, 11]):
                left, right = decoded[axis], decoded[2+axis]
                actual = -Fraction(16, denominator)
                actual += sum(scale*(c.expected[w]-c.expected[p]) for w, p, scale in left)
                actual += sum(scale*c.expected[p] for w, p, scale in right)
                assert actual == (1-theta)*knots[index][axis]+theta*knots[index+1][axis]
print(f'PASS: {checks} LP extrema of continuous wires/products; {invalid} invalid-code infeasibilities; signed shared-weight decoding, zero-bit, duplicate and reversed cases.')
