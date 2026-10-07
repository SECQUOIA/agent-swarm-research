"""Check the ex6_2_5 dual shown in open-instances-summary.md line 30 against the verifier's bound.

The verifier (reviews/wave2-small-verification/gibbs_bound.py) certifies
    bound = lambda.b + sum_p [ min(0, tmax * m_p) - max_i R_p,i / e ],
with phases 0 and 1 using m = -tau (tau from the stored B&B log) and phase 2 (ideal) using the
closed form m_2 = -ln sum_i exp(lambda_i - c). This script
  (1) evaluates lambda.b and the tau terms exactly in rationals, and bounds the other terms;
  (2) replays the verifier's 50-digit interval evaluation and takes the lower end lb.a exactly.
It calls gibbs_sym.analyse (read-only) and writes nothing."""
import json, os, sys
from fractions import Fraction as F
import mpmath
from mpmath import iv

V = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wave2-small-verification")
sys.dont_write_bytecode = True
sys.path.insert(0, V)
import gibbs_sym

name = "ex6_2_5"
A = gibbs_sym.analyse(name, verbose=False)
bb = json.load(open(os.path.join(V, "logs", "ex6_2_5_bb_type0_tau1e-17.json")))
assert bb["ok"] and bb["name"] == name and bb["ptype"] == 0
lam_s, tau = bb["lam"], bb["tau"]
slots = {0: 0, 1: 0, 2: 2}  # gibbs_bound.py: phase slot -> m_p used

# (1) exact rationals
lamF = [F(s) for s in lam_s]
bF = [F(s) for s in A["b"]]
tmaxF = sum(bF)
lamb = sum(l * b for l, b in zip(lamF, bF))
maxR = [max(F(int(r.p), int(r.q)) for r in A["R"][p]) for p in range(3)]
iv.dps = 50; mpmath.mp.dps = 50
cI = iv.mpf(".156969560191053")
lamI = [iv.mpf(s) for s in lam_s]
mI = -iv.log(sum(iv.exp(lamI[i] - cI) for i in range(3)))
assert mI.a > 0  # so min(0, tmax * m_2) = 0
exact_rational_part = lamb - 2 * tmaxF * F(tau)  # phases 0 and 1: tmax * (-tau)
print("tmax =", tmaxF, "; tau =", tau, "; max R_p =", [str(x) for x in maxR], "; m_2 lower end > 0:", mI.a > 0)
assert all(x == 0 for x in maxR)  # then the certified value is exactly lambda.b - 2 tmax tau

# (2) replay the verifier's interval evaluation (gibbs_bound.py lines 57-64)
b = [iv.mpf(v) for v in A["b"]]
mp_ = {0: -iv.mpf(tau), 2: mI}
lb = sum(lamI[i] * b[i] for i in range(3))
for slot, pt in slots.items():
    R = A["R"][slot]
    mR = max(iv.mpf(int(r.p)) / iv.mpf(int(r.q)) for r in R)
    lb = lb + (iv.mpf([min(0, mpmath.mpf(((b[0] + b[1] + b[2]) * mp_[pt]).a)), 0]) - mR / iv.e)
sg, man, ex, _ = mpmath.mpf(lb.a)._mpf_  # exact binary value of lb.a (sign kept)
lba = (-1) ** sg * F(int(man)) * F(2) ** int(ex)
assert mpmath.nstr(mpmath.mpf(lb.a), 20) == "-70.75207783344770758"  # the verifier's printed string
assert lba <= exact_rational_part

mpmath.mp.dps = 60
f = lambda q, n=30: mpmath.nstr(mpmath.mpf(q.numerator) / q.denominator, n)
print("certified value, exact (lambda.b - 2 tmax tau) =", f(exact_rational_part))
print("verifier lb.a (exact binary value)            =", f(lba))
for label, shown in (("old display", "-70.75207783344770758"), ("new display", "-70.75207783344770759")):
    x = F(shown)
    print(label, shown, ": minus exact =", f(x - exact_rational_part, 4), "; minus lb.a =", f(x - lba, 4), "; valid:", x <= lba)
primal = F("-70.75207783344770558")  # verifier's own exact primal, 20-digit print
print("gap cell: primal - new display =", f(primal - F("-70.75207783344770759"), 4))
print("displayed primal -70.752077833447706 - new display =", f(F("-70.752077833447706") - F("-70.75207783344770759"), 4))
