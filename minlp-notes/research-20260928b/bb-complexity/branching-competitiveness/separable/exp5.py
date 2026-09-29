"""N_opt is not a function of the 1D certificate functions: dyadic caps (g) vs quadratic (q).
g: m = 0 at 0 and at 2^-k (k = 0..K), concave caps (curvature -2) in between (H linear on cells).
q: m = (t - 0)^2 on [0,1] (minimum at the end 0, knot interpolant).
Prints 1D N_g(b), N_q(b) (exact greedy) and 2D grid-optimal guillotine N for g x g and q x q,
plus omega leaves.  The grid contains all knots of g (or geometric points for q) and greedy points."""
from fractions import Fraction as Fr
from sepexact import Coord, run, guill_grid
import fam

def dyadic_caps(K):
    xs = [Fr(0)] + [Fr(1, 2 ** k) for k in range(K, -1, -1)]
    return Coord.from_m(xs, [0] * len(xs), shift=False)

def quad0(rmin=Fr(1, 10 ** 6)):
    pts = {Fr(0), Fr(1)}
    r = Fr(1)
    while r > rmin:
        pts.add(r); r = r * Fr(4, 5); r = r.limit_denominator(10 ** 12)
    xs = sorted(pts)
    return Coord.from_m(xs, [x * x for x in xs])

if __name__ == "__main__":
    g = dyadic_caps(30); q = quad0()
    print("1D certificate sizes N(b):")
    for k in range(2, 11):
        b = Fr(1, 10 ** k)
        print(f"  b=1e-{k}: N_g={len(g.greedy(b)) - 1} N_q={len(q.greedy(b)) - 1}")
    for name, c in (("g x g", g), ("q x q", q)):
        for k in range(2, 8):
            eps = Fr(1, 10 ** k)
            ro = run([c, c], eps, "omega", record=True)
            cuts = fam.cut_positions(ro)
            grids = []
            for cu in cuts:
                pts = set(fam.thin(sorted(set(c.x)), 30)) | set(fam.thin(sorted(cu | {c.L, c.U}), 25)) | \
                    set(fam.thin(sorted(fam.greedy_multi(c, eps, K=10)), 25))
                grids.append(sorted(pts))
            N, _ = guill_grid(c, c, grids[0], grids[1], eps)
            print(f"{name} eps=1e-{k} grid={len(grids[0])} N_grid={N} omega={ro['leaves']} slice={len(c.greedy(eps)) - 1}", flush=True)
