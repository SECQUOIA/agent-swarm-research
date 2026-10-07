"""Rigorous gaps between the constructed points and our dual bounds, in exact arithmetic.

Gap = (upper end of the primal objective enclosure) - (dual bound), rounded up; relative gaps
(primal - dual)/|dual| and /|primal| are rounded up as well (|primal| taken at the lower end of
its magnitude).  Dual bounds are the exact certified values:
  waterno2_06: open-instances-wave2/waterno2/cellslopes/logs/certB_verify.json bound_exact
  waterno2_09..24: open-instances-wave2/waterno2/logs/cert_TT_w1_impl.json certified_bound_exact
  ann_cumene_tanh: -3386.5402291369187 (binary64, open-instances-wave3/ann/extension.md)
  kan_*: open-instances-wave3/logs/<name>.result.json dual_bound (binary64; a bound for R)

usage: python3 gaps.py
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../../..'))
import json
import os
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
PTS = os.path.join(HERE, "..", "points")
WAT = _REPRO_ROOT + "/research-20260929/open-instances-wave2/waterno2"
W3 = _REPRO_ROOT + "/research-20260929/open-instances-wave3"


def up(q, d):
    """Decimal string of q rounded up at d decimals."""
    t = q * 10 ** d
    n = -((-t.numerator) // t.denominator)
    s = str(abs(n)).rjust(d + 1, "0")
    return ("-" if n < 0 else "") + s[:-d] + "." + s[-d:]


def down(q, d):
    return "-" + up(-q, d) if q < 0 else _down_pos(q, d)


def _down_pos(q, d):
    t = q * 10 ** d
    n = t.numerator // t.denominator
    s = str(n).rjust(d + 1, "0")
    return s[:-d] + "." + s[-d:]


def sci_up(q, digits=3):
    """Positive q rounded up to `digits` significant digits, scientific notation."""
    assert q > 0
    e = 0
    while q >= 10:
        q /= 10
        e += 1
    while q < 1:
        q *= 10
        e -= 1
    t = q * 10 ** (digits - 1)
    n = -((-t.numerator) // t.denominator)
    if n >= 10 ** digits:
        n //= 10
        e += 1
        n += 1
    s = str(n)
    return f"{s[0]}.{s[1:]}e{e:+d}"


def rows():
    out = []
    d06 = Fr(json.load(open(os.path.join(WAT, "cellslopes/logs/certB_verify.json")))["bound_exact"])
    for T in ("06", "09", "12", "18", "24"):
        P = json.load(open(os.path.join(PTS, f"waterno2_{T}.exact.json")))
        p = Fr(P["objective"])
        d = d06 if T == "06" else Fr(json.load(open(os.path.join(WAT, f"logs/cert_{T}_w1_impl.json")))["certified_bound_exact"])
        out.append((f"waterno2_{T}", p, p, d))
    for name in ("ann_cumene_tanh", "kan_r5_h1_n3", "kan_r5_h1_n5", "kan_r5_h1_n8",
                 "kan_r3_h1_n4", "kan_r3_h1_n5", "kan_r3_h1_n9"):
        f = os.path.join(PTS, f"{name}.point.json")
        if not os.path.exists(f):
            continue
        P = json.load(open(f))
        lo, hi = Fr(P["objective_lo"]), Fr(P["objective_hi"])
        d = Fr(P["dual_bound"])
        out.append((name, lo, hi, d))
    return out


def main():
    print("| instance | primal objective enclosure [lo, hi] | dual bound (exact value, shown rounded down) | gap = hi - dual (rounded up) | gap / abs(dual) | gap / abs(primal) |")
    print("|---|---|---|---|---|---|")
    for name, lo, hi, d in rows():
        g = hi - d
        assert g > 0
        pr = f"{down(lo, 15)} (exact rational)" if lo == hi else f"[{down(lo, 15)}, {up(hi, 15)}]"
        absp = min(abs(lo), abs(hi))
        print(f"| {name} | {pr} | {down(d, 12)} | {sci_up(g, 6)} | {sci_up(g / abs(d), 4)} | {sci_up(g / absp, 4)} |")


if __name__ == "__main__":
    main()
