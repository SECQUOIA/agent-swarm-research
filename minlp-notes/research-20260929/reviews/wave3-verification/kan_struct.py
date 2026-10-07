"""Structure checks for the kan_* instances (verifier's own code, exact arithmetic).

  python3 kan_struct.py <name>

Reports
  * the bounds that the relaxation R drops (by variable category),
  * knot ambiguity: gaps/overlaps between the admissible intervals I_k, I_{k+1},
  * the value jump |P_{k+1} - P_k| over each overlap / at each knot,
  * partition-of-unity residuals Sum_m B_{m,p}(z) - 1 on each admissible piece,
    and whether ANY z in the edge's box satisfies all partition rows and the
    B >= 0 bounds exactly (exact gcd of the residual polynomials + exact real
    root isolation with sympy).  An edge whose argument box contains no such z
    makes the OSIL model exactly infeasible.
"""
import sys
from fractions import Fraction as Fr

import sympy

from kan_decode import decode

Z = sympy.Symbol("z")


def poly(c):
    return sympy.Poly(sum(sympy.Rational(x.numerator, x.denominator) * Z ** d for d, x in enumerate(c)), Z)


def peval(c, z):
    return sum(x * z ** d for d, x in enumerate(c))


def analyse(name, verbose=False):
    D = decode(name)
    names = D["names"]
    out = {}
    # ---------------- dropped bounds by category
    cat = {}
    for e in D["edges"]:
        for v in e["solved_vars"]:
            cat[v] = "basis/spline"
        cat[e["out"]] = "edge-output"
        cat[e["s"]] = "silu"
    cat[D["yv"]] = "output-sum"
    dropped = {}
    for v, c in cat.items():
        if D["lb"][v] is not None or D["ub"][v] is not None:
            key = (c, None if D["lb"][v] is None else float(D["lb"][v]) if c in ("silu",) else "lb" if D["lb"][v] is not None else None,
                   "ub" if D["ub"][v] is not None else None)
            dropped[key] = dropped.get(key, 0) + 1
    print("bounds dropped in R (category, lb, ub): count")
    for k, v in sorted(dropped.items(), key=str):
        print("   ", k, v)

    # boxes of edge arguments
    def edge_box(e):
        for inp in D["inputs"]:
            if e in inp["edges"]:
                return inp["lo"], inp["hi"]
        for h in D["hiddens"]:
            if e is h["edge2"]:
                return h["lo"], h["hi"]
        raise KeyError
    maxgap, maxover, maxjump = Fr(0), Fr(0), Fr(0)
    n_infeasible_edges = 0
    edge_feas = []
    maxres = 0.0
    nonzero_levels = {1: 0, 2: 0, 3: 0}
    tot_levels = {1: 0, 2: 0, 3: 0}
    for ei, e in enumerate(D["edges"]):
        lo, hi = edge_box(e)
        adm = [kk for kk, (a, b) in enumerate(e["I"]) if a <= hi and lo <= b and a <= b]
        e["adm"] = adm
        for kk in range(len(e["I"]) - 1):
            a0, b0 = e["I"][kk]
            a1, b1 = e["I"][kk + 1]
            d = a1 - b0            # >0 gap, <0 overlap
            if d > 0:
                maxgap = max(maxgap, d)
            else:
                maxover = max(maxover, -d)
            if kk in adm and kk + 1 in adm:
                # jump on the overlap (or at the knot b0 if gap)
                pts = [b0, a1]
                for t in pts:
                    maxjump = max(maxjump, abs(peval(e["P"][kk + 1], t) - peval(e["P"][kk], t)))
        # partition residuals & exact feasibility
        feas_pts = []
        for kk in adm:
            a, b = max(e["I"][kk][0], lo), min(e["I"][kk][1], hi)
            res = e["resid"][kk]
            polys = []
            for (r, c, nterms) in res:
                lev = {17: 1, 16: 2, 15: 3, 11: 1, 10: 2, 9: 3}.get(nterms, nterms)
                tot_levels[lev] = tot_levels.get(lev, 0) + 1
                if any(c):
                    nonzero_levels[lev] = nonzero_levels.get(lev, 0) + 1
                    polys.append(poly(c))
                    m = max(abs(float(peval(c, t))) for t in (a, b))
                    maxres = max(maxres, m)
            if not polys:
                feas_pts.append(("interval", kk, a, b))
                continue
            g = polys[0]
            for p in polys[1:]:
                g = sympy.gcd(g, p)
            if g.degree() <= 0:
                continue
            for (ra, rb), _mult in g.intervals(eps=sympy.Rational(1, 10 ** 45)):
                # exact rational isolating intervals of width < 1e-45
                ra, rb = Fr(ra.p, ra.q), Fr(rb.p, rb.q)
                if a <= ra and rb <= b:
                    feas_pts.append(("root", kk, ra, rb))
                elif rb >= a and ra <= b:
                    feas_pts.append(("root-boundary", kk, ra, rb))
        edge_feas.append(feas_pts)
        if not feas_pts:
            n_infeasible_edges += 1
        if verbose:
            print("edge", ei, names[e["z"]], "adm pieces", adm, "exact partition-feasible:", feas_pts[:4])
    print("max gap between admissible intervals %.3g, max overlap %.3g, max |P_k+1 - P_k| at knots/overlaps %.3g"
          % (maxgap, maxover, maxjump))
    print("partition rows: nonzero residual polynomials by level (nonzero/total over admissible pieces):",
          {k: "%d/%d" % (nonzero_levels[k], tot_levels[k]) for k in tot_levels})
    print("max |residual| at piece endpoints %.3g" % maxres)
    print("edges with NO z in their box satisfying all partition rows exactly: %d of %d"
          % (n_infeasible_edges, len(D["edges"])))
    l1_inf = [ei for ei, e in enumerate(D["edges"]) if not edge_feas[ei]
              and any(e in inp["edges"] for inp in D["inputs"])]
    print("   of which layer-1 edges:", len(l1_inf))
    return D, edge_feas


if __name__ == "__main__":
    analyse(sys.argv[1], verbose=len(sys.argv) > 2)
