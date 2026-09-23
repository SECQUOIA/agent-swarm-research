"""Root IEP bound (B3 with B2) for F1 instances: no pattern information, K_1 = [KF - (A_max) a c (T-1), KF].
usage: rootiep.py names..."""
import sys, json
from nucsim import Data
from nodebounds import iep_partial, b2
from iep import rho
out = {}
for nm in sys.argv[1:]:
    D = Data(nm); Kl, Kh = iep_partial(D, [None] * D.N)
    out[nm] = dict(B1=rho(D.G, Kh[D.T - 1]), B2=b2(D, Kh[D.T - 1]))
    print(nm, out[nm], flush=True)
json.dump(out, open("../runs/rootiep.json", "w"), default=float)
