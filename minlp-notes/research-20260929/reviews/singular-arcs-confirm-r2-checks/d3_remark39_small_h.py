"""Confirmation check d3.  Uses the independent symbol code of the round-1
confirmation (c1_symbol_independent.py, which imports nothing from the note)
for the one Remark 3.9 number not recomputed independently before: the exact
flow at N = 200.  Also evaluates the note's small-h form
tr(Phi)/2 ~ -(K + 4 phi)/(K - 4 phi), phi = f(pi)/h^3, against the transfer
map half-trace, for the trapezoidal rule at N = 100 and the exact flow at
N = 200."""
import sys
sys.path.insert(0, "../singular-arcs-confirm-r1-checks")
import mpmath as mp
import c1_symbol_independent as c1

K = 2 * mp.sqrt(10)
for name, N in (("trapezoid", 100), ("exact flow", 200)):
    r = c1.analyse(name, N)
    phi = r["fpi_over_h3"]
    small = -(K + 4 * phi) / (K - 4 * phi)
    print("%s N=%d: m+/h^3=%.5f m-/h^3=%.5f trPhi/2=%.10f small-h form=%.10f diff=%.2e det-1=%.1e"
          % (name, N, float(r["m_plus_over_h3"]), float(r["m_minus_over_h3"]), float(r["halftrace_Phi"]),
             float(small), float(small - r["halftrace_Phi"]), float(r["det_Phi"] - 1)), flush=True)
