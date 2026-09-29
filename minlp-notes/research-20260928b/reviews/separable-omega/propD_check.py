"""Review check of Proposition D (q = t^2 vs dyadic caps g) and Lemma 3.2 (budget halving).

Part 1: 1D sizes.  N_q(b) for the EXACT q (certified bracket by monotone bisection; the note's
  table used a knot interpolant of q) and N_g(b) exact (g truncated at 2^-60, which changes F by
  at most 2^-122); the bounds of (a).
Part 2: (b) the explicit guillotine certificate of q + q, every box verified exactly, count vs
  1 + 3 ceil((1/2) log2(1/eps)).
Part 3: (c) the lower bound (1/2) sum_{j<=J*} ceil((K-j+1)/2) vs the note's grid optima, and a
  randomized exact check of Claim 1 and of the three-point bound.
Part 4: omega (and deficit) leaves on q+q (exact q) and g+g.
Part 5: Lemma 3.2 on random 1D instances: N(b/2) <= 3 N(b); largest ratio found.
usage: python3 propD_check.py TRIALS SEED
"""
import math
import random
import sys
from fractions import Fraction as Fr
from sepcore import PL, Quad, run, dyadic_caps
from lemmaT_check import rand_convex, rand_nonconvex

ONE = Fr(1)


def clog(x, base):
    return math.log(float(x)) / math.log(base)


def part1(q, g):
    print("Part 1: b, N_q(b) bracket [lo, hi], N_g(b), (a)-bounds for q: upper 1+ceil(log3(1/sqrt(8b))), "
          "lower 1+log7(1/sqrt(56b)); for g: upper K+1 (4^-K/4 <= b), lower (K_b+2)/2")
    for k in range(2, 11):
        b = Fr(1, 10 ** k)
        lo, hi = q.ncert_bounds(b)
        Ng = g.ncert(b)
        uq = 1 + math.ceil(clog(1 / math.sqrt(8 * float(b)), 3))
        lq = 1 + clog(1 / math.sqrt(56 * float(b)), 7)
        K = 0
        while Fr(1, 4 ** K) / 4 > b:
            K += 1
        Kb = max(kk for kk in range(0, 80) if Fr(1, 2 ** (2 * kk + 1)) > b)
        ok = lq <= lo and hi <= uq and (Kb + 2) / 2 <= Ng <= K + 1
        print(f"  b=1e-{k}: N_q in [{lo},{hi}], N_g={Ng}; q-bounds [{lq:.2f}, {uq}], g-bounds [{(Kb + 2) / 2}, {K + 1}]  ok={ok}")
        assert ok


def qq_cert(eps, rho0):
    """1 + 3L boxes: [0,rho0]^2 and shells [rho,2rho]x[0,rho], [0,rho]x[rho,2rho], [rho,2rho]^2,
    clipped to [0,1]^2."""
    boxes = [((Fr(0), rho0), (Fr(0), rho0))]
    rho = rho0
    while rho < 1:
        r2 = min(2 * rho, ONE)
        boxes += [((rho, r2), (Fr(0), rho)), ((Fr(0), rho), (rho, r2)), ((rho, r2), (rho, r2))]
        rho = 2 * rho
    return boxes


def part2(q):
    print("Part 2: q+q certificate of (b)")
    for k in range(2, 13):
        eps = Fr(1, 10 ** k)
        if k % 2 == 0:
            rho0 = Fr(1, 10 ** (k // 2))
            exact = True
        else:
            s = math.isqrt(10 ** 40 // 10 ** k)          # floor(sqrt(eps) * 10^20)
            rho0 = Fr(s, 10 ** 20)
            exact = False
        assert rho0 * rho0 <= eps
        boxes = qq_cert(eps, rho0)
        # partition check: total area 1 and pairwise interior-disjoint by construction
        area = sum((bx[1] - bx[0]) * (bz[1] - bz[0]) for bx, bz in boxes)
        margins = [q.node(*bx)[0] + q.node(*bz)[0] + eps for bx, bz in boxes]
        bound = 1 + 3 * math.ceil(0.5 * math.log2(10 ** k))
        print(f"  eps=1e-{k}: rho0={'sqrt(eps)' if exact else '<sqrt(eps)'} boxes={len(boxes)} bound={bound} "
              f"area={area} min margin={float(min(margins)):.3g}")
        assert area == 1 and min(margins) >= 0 and len(boxes) <= bound


def part3(g, rng):
    print("Part 3: (c) lower bound vs the note's grid optima for g+g")
    note = {3: 27, 4: 50, 5: 81, 6: 102, 7: 145}
    for k in range(2, 11):
        eps = Fr(1, 10 ** k)
        K = max(kk for kk in range(80) if Fr(1, 2 ** (2 * kk + 1)) > eps)
        Js = max(j for j in range(80) if Fr(1, 4 ** (j + 2)) >= eps)
        tot = sum(math.ceil(Fr(K - j + 1, 2)) for j in range(Js + 1))
        lb = math.ceil(Fr(tot, 2))
        print(f"  eps=1e-{k}: K={K} J*={Js} lower bound N_opt >= {lb}; N_g(eps)^2 = {g.ncert(eps) ** 2}; "
              f"note grid optimum {note.get(k, '-')}")
    s = [Fr(1, 2 ** k) for k in range(0, 40)]
    bad = 0
    for _ in range(3000):
        k = rng.randint(1, 30)
        l = s[k + 1] - (s[k + 1] - s[k + 2]) * Fr(rng.randint(0, 1000), 1000)
        u = s[k - 1] + (1 - s[k - 1]) * Fr(rng.randint(0, 1000), 1000) * Fr(1, 2 ** rng.randint(0, 20))
        if g.node(l, u)[0] > -Fr(1, 2 ** (2 * k + 1)):
            bad += 1
    print(f"  three-point bound F_g(I) <= -2^(-2k-1) on 3000 random I containing s_(k+1), s_k, s_(k-1): violations {bad}")
    # Claim 1: valid box C = I x J meeting z = s_j and z = s_j' (j' >= j+2), j <= J*: I in a cell C_k, k <= j
    viol = checked = 0
    for _ in range(4000):
        eps = Fr(1, 10 ** rng.randint(2, 8))
        Js = max(j for j in range(80) if Fr(1, 4 ** (j + 2)) >= eps)
        j = rng.randint(0, Js)
        J = (s[j + 2] * Fr(rng.randint(0, 1000), 1000), s[j] + (1 - s[j]) * Fr(rng.randint(0, 1000), 1000) / 7)
        FJ = g.node(*J)[0]
        # sample I: random interval, keep if box valid
        a = Fr(rng.randint(0, 10 ** 6), 10 ** 6) ** rng.randint(1, 4)
        b = min(ONE, a + Fr(rng.randint(1, 10 ** 6), 10 ** 6) ** rng.randint(1, 6))
        if not a < b:
            continue
        if g.node(a, b)[0] + FJ + eps < 0:
            continue
        checked += 1
        cell = [kk for kk in range(0, 39) if s[kk + 1] <= a and b <= s[kk]]
        if not cell or cell[0] > j:
            viol += 1
    print(f"  Claim 1 on {checked} random valid boxes meeting two lines two apart: violations {viol}")


def part4(q, g):
    print("Part 4: omega / deficit leaves on q+q (exact q) and g+g; note's table: g+g 27/50/81/102/145, q+q 8/10/13/16/18")
    for k in range(3, 8):
        eps = Fr(1, 10 ** k)
        rq = run([q, Quad(0, 1)], eps, "omega")["leaves"]
        rqd = run([q, Quad(0, 1)], eps, "deficit")["leaves"]
        rg = run([g, dyadic_caps(60)], eps, "omega")["leaves"]
        print(f"  eps=1e-{k}: q+q omega {rq} deficit {rqd}; g+g omega {rg}")


def part5(trials, rng):
    worst = Fr(0)
    for _ in range(trials):
        c = rand_convex(rng, "wmax") if rng.random() < 0.5 else rand_nonconvex(rng, "wmax")
        b = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6])) * Fr(rng.randint(1, 9), 3)
        n1, n2 = c.ncert(b), c.ncert(b / 2)
        assert n2 <= 3 * n1
        worst = max(worst, Fr(n2, n1))
    print(f"Part 5: Lemma 3.2 on {trials} random instances: all N(b/2) <= 3 N(b); largest ratio {worst} "
          f"({float(worst):.2f}); structured instances in propD_extra.py")


if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    q, g = Quad(0, 1), dyadic_caps(60)
    part1(q, g)
    part2(q)
    part3(g, rng)
    part4(q, g)
    part5(trials, rng)
