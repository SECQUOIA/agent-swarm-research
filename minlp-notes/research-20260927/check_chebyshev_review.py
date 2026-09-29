"""Independent exact checks for the Chebyshev adversarial review."""

import sympy as sp


a, b, c, e, u, v, delta = sp.symbols("a b c e u v delta")


def q(t):
    return 2 * t**2 - 1


d = a - b
h = c - q(a)
k = e - q(b)
g = v - (1 - delta) * u
objective = (u - 1) ** 2 + (v + 1) ** 2

identities = {
    "A": 4 * d**2 - d**2 * (a + b) ** 2
    - 2 * d**2 * (1 - a**2) - 2 * d**2 * (1 - b**2) - d**4,
    "B": (c - q(b)) ** 2 - 4 * d**2 * (a + b) ** 2
    - h * (h + 4 * d * (a + b)),
    "C": (c - e) ** 2 - (c - q(b)) ** 2 - k * (k - 2 * (c - q(b))),
    "D": delta**2 - (u - v) ** 2 - delta**2 * (1 - u**2)
    - g * (2 * delta * u - g),
    "E": 16 * d**2 - (c - e) ** 2
    - (8 * d**2 * (1 - a**2) + 8 * d**2 * (1 - b**2) + 4 * d**4
       - h * (h + 4 * d * (a + b)) - k * (k - 2 * (c - q(b)))),
    "G": objective - sp.Rational(49, 32) - sp.Rational(1, 2) * (u + v) ** 2
    - 4 * (u - v - sp.Rational(1, 4)) ** 2
    - sp.Rational(7, 2) * (sp.Rational(1, 16) - (u - v) ** 2),
}
for label, residual in identities.items():
    assert sp.expand(residual) == 0, label

for m in range(1, 21):
    bags = [{"x", "u1", "v1"}]
    for j in range(2, m + 1):
        bags.extend([
            {f"u{j - 1}", f"v{j - 1}", f"u{j}"},
            {f"v{j - 1}", f"u{j}", f"v{j}"},
        ])
    seen = set()
    for i, bag in enumerate(bags):
        if i:
            assert bag & seen <= bags[i - 1]
        seen |= bag
    assert len(seen) == 2 * m + 1
    assert max(map(len, bags)) == 3
    assert len(bags) == 2 * m - 1

    differences = sp.symbols(f"d1:{m + 1}")
    perturbation = sp.Rational(1, 4**m)
    certificate = 16 ** (m - 1) * (perturbation**2 - differences[0] ** 2)
    certificate += sum(
        16 ** (m - j) * (16 * differences[j - 2] ** 2 - differences[j - 1] ** 2)
        for j in range(2, m + 1)
    )
    assert sp.expand(certificate - (sp.Rational(1, 16) - differences[-1] ** 2)) == 0

assert sp.Rational(49, 32) - sp.Rational(1, 16) == sp.Rational(47, 32)
print("PASS: 6 exact identities; width-two RIP and weighted telescope m=1,...,20; gap=47/32")
