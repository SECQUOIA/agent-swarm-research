"""Exact algebraic enclosure checks for stage3 reviewer10.

Exercise existing algorithm implementations, but validate rational exponent
answers without logarithms, exponentials, or floating-point reference values.
For alpha=m/n, r approximates t**(2*n/m) iff its error interval brackets
the root, which can be checked by integer powers of exact fractions.
"""
from contextlib import redirect_stdout
from fractions import Fraction as F
from io import StringIO
from pathlib import Path
import runpy

root = Path(__file__).resolve().parents[2]
with redirect_stdout(StringIO()):
    routines = runpy.run_path(str(root / "code/quadratic_rank/check_compiled_power_knots.py"))

count = 0
for depth in range(5):
    for alpha in (F(129,128), F(4,3), F(7,4), F(2), F(17,5), F(31,2)):
        for delta in (F(1,16), F(3,1024)):
            for index in range(2**depth + 1):
                r = routines["rational_knot"](index, depth, alpha, delta)
                t = F(index, 2**depth)
                assert 0 <= r <= 1
                assert max(F(0), r-delta)**alpha.numerator <= t**(2*alpha.denominator)
                assert t**(2*alpha.denominator) <= min(F(1), r+delta)**alpha.numerator
                if index in (0, 2**depth):
                    assert r == t
                count += 1

integer_count = 0
for depth in range(5):
    for degree in (2,3,4,7,16,31):
        for index in range(2**depth + 1):
            delta = F(3,1024)
            r = routines["integer_knot"](index, depth, degree, delta)
            target = F(index, 2**depth)**2
            assert max(F(0), r-delta)**degree <= target <= min(F(1), r+delta)**degree
            integer_count += 1
print(f"PASS: {count} exact rational-exponent enclosures and {integer_count} exact integer-exponent enclosures, including depth zero and all endpoint indices.")
