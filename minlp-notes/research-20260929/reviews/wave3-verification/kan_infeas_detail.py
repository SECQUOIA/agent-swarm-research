"""Detail of the exact partition-row infeasibility for one edge (verifier's own code).
   python3 kan_infeas_detail.py <name> <edge-arg-var-name>"""
import sys
from fractions import Fraction as Fr
import sympy
from kan_decode import decode
from kan_struct import poly, peval
name, zname = sys.argv[1], sys.argv[2]
D = decode(name)
e = [e for e in D["edges"] if D["names"][e["z"]] == zname][0]
box = [(inp["lo"], inp["hi"]) for inp in D["inputs"] if e in inp["edges"]] + \
      [(h["lo"], h["hi"]) for h in D["hiddens"] if e is h["edge2"]]
lo, hi = box[0]
print(name, zname, "box [%.17g, %.17g]" % (lo, hi))
for kk, (a, b) in enumerate(e["I"]):
    if not (a <= hi and lo <= b):
        continue
    a2, b2 = max(a, lo), min(b, hi)
    polys = []
    txt = []
    for r, c, n in e["resid"][kk]:
        txt.append("%s(%d terms): %s" % (D["rows"][r]["name"], n,
                   "0" if not any(c) else " ".join("%.3g" % float(x) for x in c)))
        if any(c):
            polys.append(poly(c))
    g = polys[0]
    for p in polys[1:]:
        g = sympy.gcd(g, p)
    roots = [((float(ra), float(rb))) for (ra, rb), _ in g.intervals()] if g.degree() > 0 else []
    print(" piece %2d z in [%.6f, %.6f]  gcd degree %d, real roots of gcd %s" % (kk, a2, b2, g.degree(), roots))
    for t in txt:
        print("     ", t)
