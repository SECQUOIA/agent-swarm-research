"""Final dual bound from the reviewer's own pieces (exact rational arithmetic):
  J(p) <= J(p*) + sum_t |dJ/dp_t(p*)| max(p*_t, pmax_t - p*_t)   for p in F (subset of G),
valid once Psi <= -mu I on a box containing theta(G) (own_concavity.py). Uses the interval
enclosures from primal_check.py (logs/primal_enclosure.txt) and pmax from own G' and from the
author's G. Also checks the report's printed statements."""
import os
import pickle
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
RG = pickle.load(open(os.path.join(HERE, "ranges.pkl"), "rb"))
AD = pickle.load(open(os.path.join(HERE, "author_data.pkl"), "rb"))
enc = {}
for line in open(os.path.join(HERE, "logs", "primal_enclosure.txt")):
    k, a, b = line.split()
    enc[k] = (Fr(a), Fr(b))
Jlo, Jhi = enc["J"]
gmag = [max(abs(enc[f"g{t}"][0]), abs(enc[f"g{t}"][1])) for t in range(1, 17)]
PRIM = os.path.join(HERE, "..", "..", "open-instances-wave2", "small", "logs", "pindyck_primal.txt")
vals = dict(line.split() for line in open(PRIM))
pstar = [Fr(vals[f"x{t}"]) for t in range(1, 17)]
out = open(os.path.join(HERE, "logs", "final_bound.log"), "w")


def say(*a):
    s = " ".join(str(v) for v in a)
    print(s)
    out.write(s + "\n")


def dec(q, k=25):
    """decimal string of q rounded toward -inf with k digits after the point"""
    f = (q * 10 ** k).__floor__()
    sgn = "-" if f < 0 else ""
    f = abs(f)
    return f"{sgn}{f // 10 ** k}.{f % 10 ** k:0{k}d}"


for label, pmax in [("own G'", RG["pmaxq"]), ("author's G", [Fr(float(v)) for v in AD["pmax"]])]:
    UB = Jhi + sum(g * max(ps, pm - ps) for g, ps, pm in zip(gmag, pstar, pmax))
    say(f"[{label}] every feasible point has objective >= -UB = {dec(-UB)} (rounded down)")
    say(f"[{label}] gap UB - J(p*) <= {float(UB - Jlo):.6e}")
claimed = Fr("-1170.4862854360886163932")
UBown = Jhi + sum(g * max(ps, pm - ps) for g, ps, pm in zip(gmag, pstar, RG["pmaxq"]))
say(f"claimed bound -1170.4862854360886163932 <= own bound -UB: {claimed <= -UBown} (difference {float(-UBown - claimed):.3e})")
primal_claim = Fr("-1170.486285436088562087577")
say(f"objective at p* lies in [{dec(-Jhi, 30)}, {dec(-Jlo, 30)}]; claim '<= -1170.486285436088562087577': {-Jlo <= primal_claim}")
say(f"difference between the two printed numbers: {float(primal_claim - claimed):.6e} (report: 'gap <= 5.43e-14')")
say(f"exact gap between the claimed dual bound and the objective at p*: {float(-Jlo - claimed):.6e}")
