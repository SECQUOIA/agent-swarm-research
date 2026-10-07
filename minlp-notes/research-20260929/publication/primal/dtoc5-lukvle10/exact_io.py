"""Exact decimal I/O for rational points (Fraction <-> terminating decimal string)."""
import gzip
from fractions import Fraction


def to_decimal(q):
    """Exact decimal string of a Fraction whose denominator is 2^a 5^b (raises otherwise)."""
    q = Fraction(q)
    d, a, b = q.denominator, 0, 0
    while d % 2 == 0:
        d //= 2
        a += 1
    while d % 5 == 0:
        d //= 5
        b += 1
    assert d == 1, "denominator is not of the form 2^a 5^b"
    k = max(a, b)
    num = q.numerator * (10 ** k // q.denominator)  # exact, since q.denominator divides 10^k
    sign = "-" if num < 0 else ""
    s = str(abs(num)).rjust(k + 1, "0")
    out = sign + (s[:-k] + "." + s[-k:] if k > 0 else s)
    assert Fraction(out) == q
    return out


def dec_floor(q, k):
    """largest k-decimal number <= q, as a string"""
    q = Fraction(q)
    return _fmt((q.numerator * 10 ** k) // q.denominator, k)


def dec_ceil(q, k):
    """smallest k-decimal number >= q, as a string"""
    q = Fraction(q)
    return _fmt(-((-q.numerator * 10 ** k) // q.denominator), k)


def _fmt(n, k):
    sign = "-" if n < 0 else ""
    s = str(abs(n)).rjust(k + 1, "0")
    return sign + s[:-k] + "." + s[-k:]


def write_point(path, names, values, header):
    with gzip.open(path, "wt") as f:
        for line in header:
            f.write("# " + line + "\n")
        for nm, v in zip(names, values):
            f.write(f"{nm} {to_decimal(v)}\n")


def read_point(path):
    """Returns {name: Fraction}. Lines starting with '#' are comments."""
    opener = gzip.open if path.endswith(".gz") else open
    out = {}
    with opener(path, "rt") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            nm, val = line.split()
            assert nm not in out
            out[nm] = Fraction(val)
    return out
