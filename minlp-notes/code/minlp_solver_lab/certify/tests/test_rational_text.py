"""Large report values preserve exact arithmetic and decimal references."""
from fractions import Fraction
import sys

import pytest

from certify.rational_text import parse_rational_text, format_rational_text
from certify.recheck import exact_comparison
from certify.summarize import reference_comparison


@pytest.mark.parametrize("sign", ["", "-"])
def test_long_rational_parse_format_comparison_and_reference_distance(sign):
    guard = sys.get_int_max_str_digits()
    numerator = "1" + "0" * 5000
    text = sign + numerator + "/3"
    value = parse_rational_text(text)
    assert value == (1 if not sign else -1) * Fraction(10**5000, 3)
    assert format_rational_text(value) == text
    assert exact_comparison(text, text) == "equal"
    assert exact_comparison(text, "0") == "changed"
    comparison = reference_comparison(text, "0.1", 1)
    assert parse_rational_text(comparison["signed_difference"]) == Fraction(1, 10) - value
    assert comparison["normalized_difference"] == comparison["signed_difference"]
    assert sys.get_int_max_str_digits() == guard


def test_decimal_references_remain_exact_including_long_mantissas():
    assert parse_rational_text("0.1") == Fraction(1, 10)
    assert parse_rational_text("-12.50e-2") == Fraction(-1, 8)
    assert reference_comparison("1/10", "0.1", 1)["signed_difference"] == "0"
    text = "0." + "0" * 5000 + "1"
    value = parse_rational_text(text)
    assert value == Fraction(1, 10**5001)
    assert format_rational_text(value) == "1/1" + "0" * 5001
    for invalid in ("NaN", "Infinity", "not a number"):
        with pytest.raises(ValueError):
            parse_rational_text(invalid)
    with pytest.raises(ZeroDivisionError):
        parse_rational_text("1/0")
