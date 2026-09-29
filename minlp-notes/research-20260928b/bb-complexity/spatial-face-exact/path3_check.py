"""Proposition 4.7: the star-forest hypothesis of Theorem 4.5 cannot be dropped, and transversality is
not the right invariant for p >= 2.  Instance instances.path3().
Checks: (1) the 4 orthant boxes around (a1, a2) are not valid (negative node bound);
(2) node counts of bisection and SCIP-type rules versus eps, against the Theorem 3.6 bound
    N >= tau (alpha/(9 eps)) H^2(S) = 0.707 * 1.300 / (9 eps) = 0.102/eps leaves."""
import itertools, math
import numpy as np
from face_bb import relax, run, RULES
import instances as I

P = I.path3()
a1, a2 = 1 / 3, math.sqrt(2) - 1
vals = []
for s1, s2 in itertools.product((0, 1), repeat=2):
    l = np.array([a1 if s1 else 0, a2 if s2 else 0, 0.]); u = np.array([1 if s1 else a1, 1 if s2 else a2, 1.])
    vals.append(relax(P, l, u)[0])
print("orthant boxes around (a1,a2): node bounds", [round(v, 4) for v in vals])
H2 = math.sqrt(2) * (min(1 - a1, 1 - a2) - max(-a1, -a2))   # area of S = {X1 = X2} in the box
for eps in (1e-2, 1e-3, 1e-4):
    lb = (1 / math.sqrt(2)) * H2 / (9 * eps)
    out = {r: run(P, eps, RULES[r], max_nodes=150000) for r in ("bisect", "SCIP(1,.2)w", "SCIP(1,.2)sp")}
    print(f"eps={eps:.0e}: Thm 3.6 bound {lb:8.1f} leaves; nodes {out}", flush=True)
