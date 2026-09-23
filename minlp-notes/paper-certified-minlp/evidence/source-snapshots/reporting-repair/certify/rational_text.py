"""Exact rational report text without Python's decimal-int digit limit.

This module handles textual report boundaries, not model extraction or proof
inference. Decimal and exponent strings retain their exact decimal value.
"""
from decimal import Decimal, InvalidOperation
from fractions import Fraction

from flint import fmpq


def parse_rational_text(text: str) -> Fraction:
    """Parse an integer/fraction or finite decimal string exactly."""
    text = text.strip()
    try:
        value = fmpq(text)
    except ValueError:
        try:
            numerator, denominator = Decimal(text).as_integer_ratio()
        except (InvalidOperation, ValueError, OverflowError) as error:
            raise ValueError("not finite rational text") from error
        return Fraction(numerator, denominator)
    return Fraction(int(value.numerator), int(value.denominator))


def format_rational_text(value: Fraction) -> str:
    """Print a canonical rational without converting large Python ints to str."""
    return str(fmpq(value.numerator, value.denominator))
