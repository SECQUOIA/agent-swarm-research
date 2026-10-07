"""Numerical check (not a proof) that both Jacobian codes are right.

The Krawczyk test is only valid if the interval Jacobian encloses the true
derivatives; a wrong derivative formula would not make the test fail when
F(centre) is tiny. This script compares, at the stored box centre,
  (1) the forward-mode Jacobian of lnts_primal.py (recursion),
  (2) the hand-written closed-form Jacobian of crosscheck.py,
  (3) central finite differences of the recursion F (step 1e-30, 110 digits),
and reports the largest relative differences.

Usage: python3 jacobian_check.py 50 100 200 400
"""
import json
import sys
from fractions import Fraction as Q

from mpmath import iv, mp

import crosscheck
import lnts_primal

mp.dps = iv.dps = 110


def run(N):
    P = json.load(open(f"points/lnts{N}_point.json"))
    names = list(P["fixed_controls"])
    thfix = [mp.mpf(Q(P["fixed_controls"][nm]).numerator) / Q(P["fixed_controls"][nm]).denominator for nm in names]
    zc = [mp.mpf(Q(d["centre"]).numerator) / Q(d["centre"]).denominator for d in P["unknowns_box"].values()]
    # (1) forward mode on the recursion, plain mp numbers
    F0, J1 = lnts_primal.residual(thfix, zc, mp, True)
    # (3) central differences of the recursion F
    step = mp.mpf(10) ** -30
    J3 = [[None] * 3 for _ in range(3)]
    for k in range(3):
        zp, zm = list(zc), list(zc)
        zp[k] += step
        zm[k] -= step
        Fp, _ = lnts_primal.residual(thfix, zp, mp, False)
        Fm, _ = lnts_primal.residual(thfix, zm, mp, False)
        for i in range(3):
            J3[i][k] = (Fp[i] - Fm[i]) / (2 * step)
    # (2) closed form of crosscheck.py at the centre (thin intervals -> midpoints)
    w, c = crosscheck.weights(N)
    th = [iv.mpf(t) for t in thfix]
    Kc = sum((iv.mpf(w[j].numerator) / w[j].denominator * iv.cos(th[j - 1]) for j in range(1, N)), iv.mpf(0))
    Ks = sum((iv.mpf(w[j].numerator) / w[j].denominator * iv.sin(th[j - 1]) for j in range(1, N)), iv.mpf(0))
    Ls = sum((iv.mpf(c[j].numerator) / c[j].denominator * iv.sin(th[j - 1]) for j in range(1, N)), iv.mpf(0))
    I = crosscheck.I
    _, J2 = crosscheck.FJ(*[iv.mpf(z) for z in zc], Kc, Ks, Ls, I(w[0]), I(w[N]), I(c[0]), I(c[N]), I(100))
    J2 = [[mp.make_mpf(J2[i][j].mid._mpi_[0]) for j in range(3)] for i in range(3)]
    scale = max(abs(J1[i][j]) for i in range(3) for j in range(3))
    d12 = max(abs(J1[i][j] - J2[i][j]) for i in range(3) for j in range(3)) / scale
    d13 = max(abs(J1[i][j] - J3[i][j]) for i in range(3) for j in range(3)) / scale
    out = dict(instance=f"lnts{N}", max_abs_F_centre=mp.nstr(max(abs(f) for f in F0), 3),
               rel_diff_AD_vs_closed_form=mp.nstr(d12, 3), rel_diff_AD_vs_finite_diff=mp.nstr(d13, 3))
    print(json.dumps(out), flush=True)
    return out


if __name__ == "__main__":
    res = [run(int(a)) for a in sys.argv[1:]]
    with open("logs/jacobian_check_" + "_".join(sys.argv[1:]) + ".json", "w") as f:
        json.dump(res, f, indent=1)
