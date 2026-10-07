"""Exact infeasibility certificate for the KAN OSIL models (verifier's own code).

Single-edge certificate (valid whatever pieces the other edges choose, and at
overlap points of neighbouring knot intervals): for an edge e with argument z
in its box, and for EVERY knot piece k whose admissible interval I_k meets the
box, give either
  (i)  a partition row of e whose residual polynomial Sum_m B_m(z) - 1 (piece k,
       exact, from kan_decode) has no real root in I_k cap box
       (sympy count_roots: exact Sturm sequences over QQ), or
  (ii) two partition rows of e whose residual polynomials have a nonzero
       resultant (no common root at all).
Then no value of z satisfies the rows of e exactly, so the OSIL model is
infeasible in exact arithmetic.
   python3 kan_infeas_cert.py <name>
"""
import sys
import sympy
from kan_decode import decode
from kan_struct import poly

Z = sympy.Symbol("z")


def cert_edge(D, e, lo, hi):
    out = []
    for kk, (a0, b0) in enumerate(e["I"]):
        a, b = max(a0, lo), min(b0, hi)
        if a > b:
            continue
        A_, B_ = sympy.Rational(a.numerator, a.denominator), sympy.Rational(b.numerator, b.denominator)
        ps = [(D["rows"][r]["name"], poly(c)) for r, c, n in e["resid"][kk] if any(c)]
        how = None
        for nm, p in ps:
            if p.count_roots(A_, B_) == 0:
                how = ("root-free", nm)
                break
        if how is None:
            for x in range(len(ps)):
                for y in range(x + 1, len(ps)):
                    p, q = ps[x][1], ps[y][1]
                    if p.degree() >= 1 and q.degree() >= 1 and sympy.resultant(p.as_expr(), q.as_expr(), Z) != 0:
                        how = ("resultant", ps[x][0], ps[y][0])
                        break
                if how:
                    break
        out.append((kk, how))
    return out


name = sys.argv[1]
D = decode(name)
boxes = []
for inp in D["inputs"]:
    for e in inp["edges"]:
        boxes.append((e, inp["lo"], inp["hi"], "layer1"))
for h in D["hiddens"]:
    boxes.append((h["edge2"], h["lo"], h["hi"], "layer2"))
ncert = {"layer1": 0, "layer2": 0}
first = None
for e, lo, hi, lay in boxes:
    c = cert_edge(D, e, lo, hi)
    if all(how is not None for kk, how in c):
        ncert[lay] += 1
        if first is None:
            first = (D["names"][e["z"]], c)
print("%s: edges with a complete single-edge infeasibility certificate: layer-1 %d of %d, layer-2 %d of %d"
      % (name, ncert["layer1"], sum(1 for b in boxes if b[3] == "layer1"),
         ncert["layer2"], sum(1 for b in boxes if b[3] == "layer2")))
if first:
    print("  example: edge argument %s:" % first[0])
    for kk, how in first[1]:
        print("    piece %2d: %s" % (kk, how))
    print("  => the OSIL model %s has no exactly feasible point" % name)
