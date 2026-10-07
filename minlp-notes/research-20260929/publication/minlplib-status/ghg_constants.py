"""Revision after review round 1, ghg_3veh: the constants that differ between
the old model text (2010 MINLPLib 1 file, 2017 MINLPLib.jl copy) and the
current .gms/OSIL.

The old text writes factored products such as
  150000*(0.0181052631578947/x44 + 0.03458*x47 - 0.03458*x48)
  11.34*(33.1610917987189 - x95)/x81
  0.854659090909091*(33.1610917987189 - x95)/x80
the current text writes the expanded products as rounded decimals. This
script counts the occurrences in both files and computes, exactly with
Fractions, the difference between each exact product and the decimal now
written (and the IEEE double that GAMS computes for the product).

Usage: python3 ghg_constants.py
"""
import os
import re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = os.path.join(HERE, "pages", "sources", "gamsworld", "MINLPLib", "Scalar_models", "ghg_3veh.gms")
JL = os.path.join(HERE, "pages", "sources", "jl2017", "ghg_3veh.jl")
CUR = os.path.join(HERE, "pages", "models", "gms", "ghg_3veh.gms")

CASES = [  # (factor a, factor b, decimal written now)
    ("150000", "0.0181052631578947", "2715.7894736842"),
    ("11.34", "33.1610917987189", "376.046780997472"),
    ("0.854659090909091", "33.1610917987189", "28.341428570246"),
]


def rows_with(path, needle):
    text = open(path).read()
    out = []
    for m in re.finditer(r"(?m)^(e\d+)\.\.(.*?);", text, re.S):
        k = m.group(2).replace("\n", "").replace(" ", "").count(needle)
        if k:
            out.append((m.group(1), k))
    return out


def main():
    for a, b, now in CASES:
        exact = F(a) * F(b)
        dbl = float(a) * float(b)
        d = F(now) - exact
        print(f"{a} * {b} = {exact} (exact) = {float(exact)!r}; GAMS double {dbl!r}")
        print(f"  current decimal {now}: diff {float(d):.3e}, relative {float(abs(d) / exact):.3e}; "
              f"double vs current relative {abs(dbl - float(now)) / dbl:.3e}")
        print(f"  current .gms rows/occurrences: {rows_with(CUR, now)}")
    for f in (OLD, JL):
        t = open(f).read().replace(" ", "").replace("\n", "")
        print(os.path.basename(os.path.dirname(f)), os.path.basename(f), "factored forms:",
              {s: t.count(s) for s in ["150000*(0.0181052631578947/", "11.34*(33.1610917987189-",
                                       "0.854659090909091*(33.1610917987189-", "2715.78", "376.04", "28.341"]})


if __name__ == "__main__":
    main()
