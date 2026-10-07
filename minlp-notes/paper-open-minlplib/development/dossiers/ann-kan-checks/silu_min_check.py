"""Exact rational check of the SiLU-minimum constants used by the KAN bounds (dossier author).
silu(z) = z/(1+e^-z); silu'(z) = s(z)(1 + z(1 - s(z))), s = logistic.  Uses the primal reviewer's
rational interval exp (rint.exp_bounds: Taylor + Lagrange remainder, no floating point)."""
import sys
from fractions import Fraction as F
sys.path.insert(0, "/tmp/annkan_dossier")
import rint

def sig_bounds(z):           # logistic(z) = 1/(1+e^-z), rational z
    lo_e, hi_e = rint.exp_bounds(-z)
    return 1 / (1 + hi_e), 1 / (1 + lo_e)

def g_bounds(z):              # g(z) = 1 + z(1 - s(z)); sign of silu'(z)
    slo, shi = sig_bounds(z)
    vals = [1 + z * (1 - slo), 1 + z * (1 - shi)]
    return min(vals), max(vals)

# authors' bracket (kan_iv) and claimed lower bound of min silu
for name, zl, zr, smin in [("authors kan_iv", F(-1.27846454277), F(-1.27846454275), F(-0.27846454276108)),
                           ("verifier kan_bnb (approx.)", F("-1.27846454276107380910e0") - F(1, 10**15) - F(1, 10**20),
                            F("-1.27846454276107380910e0") + F(1, 10**15) + F(1, 10**20), None)]:
    gl, gr = g_bounds(zl), g_bounds(zr)
    print(name, ": silu'(zl) sign interval", float(gl[0]), float(gl[1]), "; silu'(zr)", float(gr[0]), float(gr[1]))
    assert gl[1] < 0 < gr[0]
    # lower bound of silu on [zl, zr]: numerator in [zl, zr] (negative), denominator >= 1 + e^{-zr}
    lo_e, _ = rint.exp_bounds(-zr)
    lb = zl / (1 + lo_e)
    print("   rigorous lower bound of min silu on the bracket:", float(lb))
    if smin is not None:
        print("   claimed bound", float(smin), "valid:", smin <= lb)
# outside the bracket silu is monotone (sign of g fixed): g is increasing? check g at a few points
for z in [F(-10), F(-3), F(-2), F(-1.3), F(-1.27), F(-1), F(0), F(2)]:
    print("g(", float(z), ") in", [float(x) for x in g_bounds(z)])

# tighter: mean-value form on the authors' bracket, exact rationals
zl, zr = F(-1.27846454277), F(-1.27846454275)
zm = (zl + zr) / 2
lo_e, hi_e = rint.exp_bounds(-zm)
silu_zm_lo = zm / (1 + lo_e)          # zm < 0: smallest value uses smallest denominator
# |silu'| on the bracket <= max |s(1 + z(1-s))| <= 1 * max(|g(zl)|, |g(zr)|) (g monotone increasing there)
gmax = max(abs(g_bounds(zl)[0]), abs(g_bounds(zr)[1]))
mv_lb = silu_zm_lo - gmax * (zr - zl) / 2
print("authors' bracket: rigorous mean-value lower bound of min silu:", mv_lb, float(mv_lb))
for c in [F(-0.27846454276108), F(-0.278464542761075)]:
    print("   constant", float(c), "<= rigorous lower bound:", c <= mv_lb)
