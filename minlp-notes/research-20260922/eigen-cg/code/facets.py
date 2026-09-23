"""Non-Eigen-CG facets of BQP_6 quoted in arXiv:2604.00932v1 (Props. 3-5, eqs. (13)-(15))."""
import re
from bh import pairs

F13 = "2 - 2x1 - x2 + x3 - 2x4 + 3x5 - x6 + 2X12 - X13 - X23 + 2X14 + X24 - 2X15 - X25 - X45 + X16 + X36 + X46 - X56"
F14 = ("5 - 4x1 - 4x2 + 4x3 - 5x4 + 4x5 - 3x6 + 3X12 - 2X13 - 2X23 + 5X14 + 5X24 - 3X34 - 2X15 - 2X25"
       " + 1X35 - 3X45 + 2X16 + 2X26 - 1X36 + 3X46 - 1X56")
F15 = ("1 - x1 + 2x3 + x5 + 2X12 - X13 - 3X23 + X14 + 2X24 - 2X34"
       " - X15 - 2X25 + 2X35 - X45 + X16 + 2X26 - 2X36 + X46 - X56")


def parse(s, n=6):
    P = pairs(n)
    a = [0] * (n + len(P))
    c = 0
    for sign, coef, var, idx in re.findall(r"([+-]?)\s*(\d*)\s*([xX]?)(\d*)", s.replace(" ", "")):
        if not (coef or var):
            continue
        k = int(coef) if coef else 1
        if sign == "-":
            k = -k
        if not var:
            c += k
        elif var == "x":
            a[int(idx) - 1] += k
        else:
            i, j = int(idx[0]) - 1, int(idx[1]) - 1
            a[n + P.index((min(i, j), max(i, j)))] += k
    return a, c
