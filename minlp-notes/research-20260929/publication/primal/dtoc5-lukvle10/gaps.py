"""Rigorous gaps (exact rational arithmetic, results rounded up) between the primal values of this
track and the dual bounds of open-instances-summary.md (and the verifier's sharper dtoc5 value)."""
import json
from fractions import Fraction


def sci_up(q, digits=4):
    """upper bound of q > 0 in scientific notation with `digits` significant digits"""
    e = len(str(q.numerator)) - len(str(q.denominator))
    while Fraction(10) ** e > q:
        e -= 1
    while Fraction(10) ** (e + 1) <= q:
        e += 1
    m = q / Fraction(10) ** e
    d = -((-m.numerator * 10 ** (digits - 1)) // m.denominator)
    if d == 10 ** digits:
        d //= 10
        e += 1
    s = str(d)
    return f"{s[0]}.{s[1:]}e{e}"


out = {}
# dtoc5: exact objective of the rational point (logs/dtoc5_check_objective_exact.txt)
P = Fraction(open("logs/dtoc5_check_objective_exact.txt").read().strip())
for label, D in [("summary dual 5.38967211918114", Fraction("5.38967211918114")),
                 ("verifier dual (truncated) 5.38967211918114046742396472386",
                  Fraction("5.38967211918114046742396472386"))]:
    g = P - D
    assert g > 0
    out[f"dtoc5 vs {label}"] = dict(abs_gap_upper=sci_up(g), rel_gap_upper=sci_up(g / D))
# lukvle10: upper end of the box objective enclosure (rounded up to 40 decimals)
U = Fraction(json.load(open("logs/lukvle10_enclose.json"))["objective_box"][1])
D = Fraction("352.2380254050784")
out["lukvle10 vs summary dual 352.2380254050784"] = dict(abs_gap_upper=sci_up(U - D), rel_gap_upper=sci_up((U - D) / D))
print(json.dumps(out, indent=1))
json.dump(out, open("logs/gaps.json", "w"), indent=1)
