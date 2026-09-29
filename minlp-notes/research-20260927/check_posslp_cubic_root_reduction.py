"""Exact structural checks for the candidate PosSLP cubic-root reduction.

These checks do not prove the universal analytic error estimate. They verify
the gadget expansion, projective annotations, and actual signed box arithmetic
for source circuits with positive, zero, and negative outputs.
"""

from fractions import Fraction as Q

import sympy as sp


x, y = sp.symbols("x y")
DEG = 6


def trunc(expr):
    return sp.Add(*(c * x**e[0] * y**e[1]
                    for e, c in sp.Poly(sp.expand(expr), x, y).terms()
                    if sum(e) <= DEG))


def A_series(expr):
    result, power = 0, 1
    for j in range(1, DEG + 1):
        power = trunc(power * expr)
        result += sp.binomial(sp.Rational(1, 3), j) * 3**j * power
    return trunc(result)


def H_series(z):
    ap, am = A_series(z), A_series(-z)
    return trunc((A_series(trunc(ap**2)) + A_series(trunc(am**2))) / 2)


H = H_series(x)
P = A_series(trunc((H_series(x + y) - H_series(x - y)) / 4))
assert sp.expand(H - H.xreplace({x: -x})) == 0
assert sp.Poly(H, x, y).coeff_monomial(x**2) == 1
assert sp.expand(P.subs(x, 0)) == 0 and sp.expand(P.subs(y, 0)) == 0
assert sp.Poly(P, x, y).coeff_monomial(x * y) == 1
assert all(e[0] >= 1 and e[1] >= 1 for e, c in sp.Poly(P, x, y).terms())
assert all(sum(e) >= 4 for e, c in sp.Poly(P - x * y, x, y).terms())


class MacroCircuit:
    def __init__(self):
        self.nodes = [("delta",)]
        self.annotation = [(1, 1)]  # (assigned degree, integer coefficient)

    def gate(self, kind, a, b, sign=1):
        da, ca = self.annotation[a]
        db, cb = self.annotation[b]
        if kind == "A":
            assert da == db
            anno = (da, ca + sign * cb)
        else:
            assert kind == "P"
            anno = (da + db, ca * cb)
        self.nodes.append((kind, a, b, sign))
        self.annotation.append(anno)
        return len(self.nodes) - 1

    def compile_integer(self, source):
        pairs = []
        values = []  # Only a check; not part of the reduction algorithm.
        for node in source:
            kind = node[0]
            if kind == "one":
                pair, value = (0, 0), 1
            elif kind == "zero":
                pair, value = (self.gate("A", 0, 0, -1), 0), 0
            else:
                ia, ib = node[1:]
                fa, ga = pairs[ia]
                fb, gb = pairs[ib]
                if kind in ("+", "-"):
                    sign = 1 if kind == "+" else -1
                    numerator = self.gate("A", self.gate("P", fa, gb),
                                          self.gate("P", fb, ga), sign)
                    value = values[ia] + sign * values[ib]
                else:
                    assert kind == "*"
                    numerator = self.gate("P", fa, fb)
                    value = values[ia] * values[ib]
                pair = (numerator, self.gate("P", ga, gb))
            f, g = pair
            assert self.annotation[f][0] == self.annotation[g][0]
            assert self.annotation[f][1] == value and self.annotation[g][1] == 1
            pairs.append(pair)
            values.append(value)
        return pairs[-1][0], values[-1]


class RawCircuit:
    def __init__(self):
        self.gates = []

    def append(self, c, linear=None, square=None):
        self.gates.append((Q(c), linear or {}, square or {}))
        return len(self.gates) - 1

    def A(self, terms):
        linear = {}
        for predecessor, coefficient in terms:
            linear[predecessor] = linear.get(predecessor, Q(0)) + 3 * Q(coefficient)
        return self.append(1 - sum(linear.values()), linear)

    def S(self, predecessor):
        return self.append(4, {predecessor: Q(-6)}, {predecessor: Q(3)})

    def P(self, a, b):
        branches = [self.A([(a, sa), (b, sb)])
                    for sa, sb in [(1, 1), (-1, -1), (1, -1), (-1, 1)]]
        squares = [self.S(t) for t in branches]
        return self.A([(t, Q(sign, 8)) for t, sign in zip(squares, [1, 1, -1, -1])])

    def check_boxes(self, initial, upper_gate_count):
        boxes = []
        for i, (c, linear, square) in enumerate(self.gates, 1):
            w = 1000**i * initial
            lo, hi = 1 - w, 1 + w
            il, iu = c, c
            for coefficients, exponent in [(linear, 1), (square, 2)]:
                for predecessor, coefficient in coefficients.items():
                    l, h = boxes[predecessor]
                    l, h = l**exponent, h**exponent
                    if coefficient < 0:
                        l, h = h, l
                    il += coefficient * l
                    iu += coefficient * h
            assert 0 < lo < hi
            assert lo**3 <= il <= iu <= hi**3, (i, lo**3 - il, iu - hi**3)
            assert w <= Q(1, 1000**3)
            boxes.append((lo, hi))
        assert len(self.gates) <= upper_gate_count
        return boxes


def run_case(source):
    # Append 2V-1; all test sources start with one.
    out = len(source) - 1
    full_source = source + [("+", out, out), ("-", out + 1, 0)]
    macro = MacroCircuit()
    output, integer_value = macro.compile_integer(full_source)
    T = len(macro.nodes) - 1
    q, bound = 2 * T + 5, 11 * T + 6
    assert bound == q + 9 * T + 1
    delta0 = Q(1, 1000 ** (bound + 3))
    raw = RawCircuit()
    delta = raw.append(1 + 3 * delta0**2)
    for _ in range(q - 1):
        delta = raw.S(delta)
    mapping = [delta]
    for kind, a, b, sign in macro.nodes[1:]:
        if kind == "A":
            mapping.append(raw.A([(mapping[a], 1), (mapping[b], sign)]))
        else:
            mapping.append(raw.P(mapping[a], mapping[b]))
    assert integer_value != 0
    assert macro.annotation[output][1] == integer_value
    raw.check_boxes(delta0, bound)
    bT = 16 * 3**T - 15
    assert 4 * 2**q > bT + 30
    assert 2**24 > 2 * 100**3
    return T, len(raw.gates), integer_value


cases = [
    [("one",)],
    [("one",), ("zero",)],
    [("one",), ("-", 0, 0), ("-", 1, 0)],
    [("one",), ("+", 0, 0), ("*", 1, 1), ("+", 1, 1), ("-", 2, 3)],
    [("one",), ("+", 0, 0), ("*", 1, 1), ("*", 2, 2), ("-", 3, 2)],
]
results = [run_case(case) for case in cases]
print("P through degree six:", P)
print("PASS: exact leading coefficients and signed interval boxes", results)
