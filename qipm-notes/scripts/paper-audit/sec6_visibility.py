# Section 6, remark after thm:cond-visibility:
#   "In the usual lower-cost-winner case p >= 1/G, the trace-distance bounds
#    reduce to p - 1/G <= Dtr <= p."
# Read as an implication ("a lower-cost winner gives p >= 1/G") this is false
# under the section's own two-cost hypotheses: a strictly lower spectral EDGE
# does not control the resolvent trace.  Section 7 says as much for its own
# family ("This implication is special to the present spectra and is not part
# of the general two-cost model of Sec 6.1").  Explicit instance below.
import numpy as np
from scipy.optimize import brentq

d, m, G = 2, 1, 3
gam = [10.0]                 # winner shifted spectrum: {0} u {gam}, edge = 0
delt = [0.1, 0.1]            # loser  shifted spectrum, edge = 0.1 > 0
A = lambda x: m/x + sum(1.0/(x+g) for g in gam)
B = lambda x: sum(1.0/(x+dd) for dd in delt)

for tau in (0.2116, 0.15, 0.05, 0.01):
    x = brentq(lambda x: tau*(A(x) + (G-1)*B(x)) - 1.0, 1e-14, 1e6)
    p = tau*A(x)
    print(f"tau={tau:<7g} x={x:.6f}  p={p:.6f}  1/G={1/G:.6f}  "
          f"{'p < 1/G  <-- lower-edge winner, LESS than uniform mass' if p < 1/G else 'p >= 1/G'}")
