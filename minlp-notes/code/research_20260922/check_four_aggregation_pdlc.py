"""Exact checks for the credited BDS four-aggregation sharpness example.

These checks verify finite algebraic identities and witness signs. They do
not verify the universal perturbation/limit theorem or its novelty.
"""

import sympy as sp

s, rho = sp.symbols("s rho", real=True)
f = sp.Matrix([-s**2 + 1 + rho, s**2 + 5 * s - 4 + rho, -s - rho])
rays = sp.Matrix([[1, 0, 0], [0, 1, 0], [1, 0, 1], [0, 1, 1]])

assert sp.expand(-7 * f[0] - 3 * f[1] - 15 * f[2]) == 4 * s**2 + 5 * rho + 5
assert all(value.is_negative for value in f.subs({s: -3, rho: 4}))

witnesses = [
    (-2, 3),
    (-4, 8),
    ((-1 - sp.sqrt(5)) / 2, 0),
    (-2 - 2 * sp.sqrt(2), 0),
]
for designated, (s_value, rho_value) in enumerate(witnesses):
    slacks = (rays * f.subs({s: s_value, rho: rho_value})).applyfunc(sp.simplify)
    assert slacks[designated] == 0
    assert all(slacks[j].is_negative for j in range(4) if j != designated)
    print(f"Witness {designated + 1}: {list(slacks)}")

print("PASS: PDLC identity, strict feasibility, four uniquely active rays.")
