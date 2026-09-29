"""Proposition D numbers, redone after the review with the exact q(t) = t^2 (QuadCoord) and exact
product certificates for g x g.  For eps (or b) = 1e-3..1e-7 prints:
  N_g(b) (exact greedy), N_q(b) (certified bracket for the exact quadratic);
  g x g: product certificate min over 64 budget splits, exact-verified grid optimum, omega (both rules);
  q x q: the Whitney construction count 1 + 3 ceil(log2(1/sqrt(eps))), exact-verified grid optimum, omega."""
import math
from fractions import Fraction as Fr
from sepexact import Coord, QuadCoord, run, guill_grid
import fam
from exp5 import dyadic_caps

g = dyadic_caps(30)
q = QuadCoord(0)
for k in range(3, 8):
    eps = Fr(1, 10 ** k)
    Ng = len(g.greedy(eps)) - 1
    Nq = q.greedy_count_bracket(eps)
    prod = min((len(g.greedy(eps * Fr(j, 64))) - 1) * (len(g.greedy(eps * Fr(64 - j, 64))) - 1) for j in range(1, 64))
    # grid for g x g: all dyadic knots down to sqrt(eps)/64, plus greedy breakpoints at eps*j/64 and omega cuts
    Coord.sel = "knot"
    ro_g = run([g, g], eps, "omega", record=True)
    pts = {x for x in g.x if x == 0 or x >= Fr(1, 2 ** 40)}
    for j in (1, 8, 16, 24, 32, 40, 48, 56, 63, 64):
        pts |= set(g.greedy(eps * Fr(j, 64)))
    pts |= fam.cut_positions(ro_g)[0] | fam.cut_positions(ro_g)[1]
    pts = sorted(p for p in pts if p == 0 or p >= Fr(1, 10 ** 6) * 0 + p)
    gg = fam.thin(pts, 90)
    Ngg, _ = guill_grid(g, g, gg, gg, eps)
    Coord.sel = "proj"
    g.cache.clear()
    om_proj = run([g, g], eps, "omega")["leaves"]
    Coord.sel = "knot"
    g.cache.clear()
    # q x q exact
    ro_q = run([q, q], eps, "omega", record=True)
    qpts = {Fr(0), Fr(1)} | fam.cut_positions(ro_q)[0] | fam.cut_positions(ro_q)[1]
    rho = math.sqrt(float(eps))
    r = Fr(rho).limit_denominator(10 ** 12)
    while r < 1:
        qpts.add(r)
        r *= 2
    for j in (1, 16, 32, 48, 63, 64):
        qpts |= set(q.greedy(eps * Fr(j, 64)))
    qg = fam.thin(sorted(qpts), 60)
    Nqq, _ = guill_grid(q, q, qg, qg, eps)
    whitney = 1 + 3 * math.ceil(math.log2(1 / rho))
    print(f"eps=b=1e-{k}: N_g {Ng}, N_q in {Nq}; g x g: product {prod}, grid optimum {Ngg} (grid {len(gg)}), "
          f"omega knot {ro_g['leaves']}, omega proj {om_proj}; q x q: Whitney {whitney}, grid optimum {Nqq} "
          f"(grid {len(qg)}), omega {ro_q['leaves']}", flush=True)
