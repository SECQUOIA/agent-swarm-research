"""Targeted exact checks for the two-integer Pell output-size example.

These checks corroborate finite instances. The accompanying review proves
the parametrization, valuation identity, and asymptotic output bound.
"""

from math import isqrt


def multiply(left, right):
    x, b = left
    u, v = right
    return x * u + 5 * b * v, x * v + b * u


def pell_power(exponent):
    result = (1, 0)
    base = (9, 4)
    while exponent:
        if exponent & 1:
            result = multiply(result, base)
        base = multiply(base, base)
        exponent //= 2
    return result


def valuation_five(number):
    valuation = 0
    while number % 5 == 0:
        number //= 5
        valuation += 1
    return valuation


x, b = 1, 0
least_exponents = {}
for n in range(1, 3126):
    x, b = 9 * x + 20 * b, 4 * x + 9 * b
    assert x * x - 5 * b * b == 1
    assert valuation_five(b) == valuation_five(n)
    assert b % 5 == (4 * n * pow(9, n - 1, 5)) % 5
    for m in range(1, 5):
        if m not in least_exponents and b % (5**m) == 0:
            least_exponents[m] = n
    if n <= 40:
        x_five_n, b_five_n = pell_power(5 * n)
        bracket = x**4 + 10 * x * x * b * b + 5 * b**4
        assert b_five_n == 5 * b * bracket
        assert x_five_n == x**5 + 50 * x**3 * b**2 + 125 * x * b**4
        assert bracket % 5 == 1
assert least_exponents == {m: 5**m for m in range(1, 5)}
print("Recurrence and valuation: n = 1..3125 passed.")
print("Both fifth-power coefficient identities: n = 1..40 passed.")
print("Direct least divisible exponents: m = 1..4 passed.")

circuit_x, circuit_b = 9, 4
for m in range(1, 7):
    n = 5**m
    x, b = pell_power(n)
    circuit_x, circuit_b = (
        circuit_x**5 + 50 * circuit_x**3 * circuit_b**2
        + 125 * circuit_x * circuit_b**4,
        5 * circuit_x**4 * circuit_b + 50 * circuit_x**2 * circuit_b**3
        + 25 * circuit_b**5,
    )
    assert (x, b) == (circuit_x, circuit_b)
    coefficient = 5 ** (2 * m + 1)
    y, remainder = divmod(b, n)
    assert remainder == 0
    assert x * x - coefficient * y * y == 1
    assert x >= 2 and y >= 1
    assert 4 * n <= x.bit_length() <= 5 * n
    print(
        f"m = {m}: coefficient bits = {coefficient.bit_length()}, "
        f"optimal x bits = {x.bit_length()}, optimal y bits = {y.bit_length()}"
    )

solutions = []
for b in range(1, 200000):
    square = 1 + 5 * b * b
    x = isqrt(square)
    if x * x == square:
        solutions.append((x, b))
assert solutions == [pell_power(n) for n in range(1, len(solutions) + 1)]
print("Enumeration for B = 1..199999: all four solutions are consecutive powers.")
