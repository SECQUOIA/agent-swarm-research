"""Independent checks of Theorem A (robust-branching.md, Section 2).

Written for the review; does not import the author's code.

[A1] Alternating (L,R,L,R,...) trap points of five deterministic clamp schedules, built by nested
     intervals in 400-digit arithmetic (the fixed-1/5 point is also checked to equal 1/6 exactly).
     Replay the clip rule for 150 steps: the kink must lie strictly inside a clamp zone at every
     step. Check rho_k (1 - rho_k) >= theta0/4 along the chain and the 1D count T >= 2K+1 of
     Theorem A(ii), with theta0 the smallest value the schedule can take.
[A2] McCormick family with x-only selection: the open test is |c| w_y rho (1-rho) w_x with
     w_y = 1, i.e. linear in w_x (the proof's step 5 writes w_k^2). Report both counts.
[A3] Theorem A(ii) says "(in fact uncountably many)" points satisfy the bound with the stated K.
     For the fixed clamp 1/5, test itineraries with one run of length 2.
[A4] Theorem A(iii): widest-side selection on the McCormick family, exact rational arithmetic for
     the fixed clamp 1/5 at a = 1/6 (y-splits clip 1/5), and 60-digit arithmetic for the
     width-dependent schedule 1/10 + w_x/5 at its trap point; compare with the proved bound
     theta0^2 |c|^(1/2) / (2 eps^(1/2)).
"""
import math
import sys
from fractions import Fraction as Fr

import mpmath as mp

mp.mp.dps = 400

# schedules: theta as a function of (l, u, k, sides) where sides = tuple of earlier zone sides
SCHED = {
    "fixed 1/5": (lambda l, u, k, s: mp.mpf(1) / 5, 0.2),
    "depth 1/5,1/4 alternating": (lambda l, u, k, s: mp.mpf(1) / 5 if k % 2 == 0 else mp.mpf(1) / 4, 0.2),
    "width 1/10 + w/5": (lambda l, u, k, s: mp.mpf(1) / 10 + (u - l) / 5, 0.1),
    "position 1/8 + l/4": (lambda l, u, k, s: mp.mpf(1) / 8 + l / 4, 0.125),
    "history: 0.15 if #L even else 0.3": (lambda l, u, k, s: mp.mpf("0.15") if s.count("L") % 2 == 0
                                          else mp.mpf("0.3"), 0.15),
}


def build(sched, itinerary):
    l, u, sides = mp.mpf(0), mp.mpf(1), ()
    for k, side in enumerate(itinerary):
        th = sched(l, u, k, sides)
        w = u - l
        if side == "L":
            u = l + th * w
        else:
            l = u - th * w
        sides += (side,)
    return (l + u) / 2


def replay(sched, a, steps):
    """Chain of the clip rule; returns list of (l, u, theta, side) or stops at a split on a."""
    l, u, sides, out = mp.mpf(0), mp.mpf(1), (), []
    for k in range(steps):
        th = sched(l, u, k, sides)
        w = u - l
        lo, hi = l + th * w, u - th * w
        if lo <= a <= hi:
            out.append((l, u, th, "HIT"))
            return out
        side = "L" if a < lo else "R"
        out.append((l, u, th, side))
        if side == "L":
            u = lo
        else:
            l = hi
        sides += (side,)
    return out


def T1d(chain, a, eps, alpha=1):
    T = 1
    for l, u, th, side in chain:
        if alpha * (a - l) * (u - a) <= eps:
            break
        T += 2
        if side == "HIT":
            break
    return T


def Tmc_xonly(chain, a, eps, c=1):
    T = 1
    for l, u, th, side in chain:
        if c * (a - l) * (u - a) / (u - l) <= eps:   # w_y = 1
            break
        T += 2
        if side == "HIT":
            break
    return T


def Kbound(th0, eps, alpha=1.0):
    return math.ceil(math.log(alpha * th0 / (4 * eps)) / (2 * math.log(1 / th0)))


def part_A1_A2():
    print("[A1/A2] alternating trap points, 150-step replay, 1D and McCormick x-only counts")
    for name, (sched, th0) in SCHED.items():
        a = build(sched, "LR" * 120)
        ch = replay(sched, a, 150)
        hit = any(s == "HIT" for *_, s in ch)
        alt = all(ch[k][3] == "LR"[k % 2] for k in range(len(ch)))
        pr = min((a - l) * (u - a) / (u - l) ** 2 for l, u, _, _ in ch)
        print(f"  {name}: a = {mp.nstr(a, 20)}; hit within 150 steps: {hit}; itinerary alternating: {alt}; "
              f"min rho(1-rho) = {mp.nstr(pr, 6)} (theta0/4 = {th0 / 4})")
        if name == "fixed 1/5":
            print(f"    |a - 1/6| = {mp.nstr(abs(a - mp.mpf(1) / 6), 3)}")
        for k in (4, 8, 16, 24, 32, 48):
            eps = mp.mpf(10) ** (-k)
            T = T1d(ch, a, eps)
            K = Kbound(th0, 10.0 ** -k)
            Tm = Tmc_xonly(ch, a, eps)
            print(f"    eps=1e-{k}: 1D T = {T} (Theorem A(ii) bound 2K+1 = {2 * K + 1}, ok={T >= 2 * K + 1}); "
                  f"McCormick x-only T = {Tm}")


def part_A3():
    print("[A3] fixed clamp 1/5: itineraries with one run of length 2, against the stated K of A(ii)")
    sched, th0 = SCHED["fixed 1/5"]
    for pre in ("", "LR", "LRLR", "LRLRLR"):
        # exactly one run of length 2, alternating otherwise
        itin = "LL" + "RL" * 100 if not pre else pre + "R" + "LR" * 100
        a = build(sched, itin)
        ch = replay(sched, a, 120)
        worst = None
        for j in range(1, 400):
            eps = 10.0 ** (-j / 20)
            if eps >= th0 / 4:
                continue
            T = T1d(ch, a, mp.mpf(eps))
            K = Kbound(th0, eps)
            if T < 2 * K + 1:
                worst = (eps, T, 2 * K + 1)
                break
        print(f"  itinerary {itin[:12]}...: a = {mp.nstr(a, 12)}; first violation of T >= 2K+1: "
              + (f"eps = {worst[0]:.3g}, T = {worst[1]} < {worst[2]}" if worst else "none found"))


def mc_widest(a, eps, xrule, yclamp=Fr(1, 5), cap=2_000_000):
    """McCormick kink family c=-1, widest side (ties to x); boxes as exact numbers.
    xrule(lx, ux) -> theta for x (depends only on the x-interval). Returns processed nodes."""
    stack = [(0, 1, 0, 1)]
    T = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        T += 1
        if T > cap:
            return None
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        if wx >= wy:
            th = xrule(lx, ux)
            s = min(max(a, lx + th * wx), ux - th * wx)
            if s == a:
                T += 2  # both children pruned (not straddling)
                continue
            stack += [(lx, s, ly, uy), (s, ux, ly, uy)]
        else:
            s = ly + min(max(rho, yclamp), 1 - yclamp) * wy
            stack += [(lx, ux, ly, s), (lx, ux, s, uy)]
    return T


def part_A4():
    print("[A4] Theorem A(iii): widest-side selection on the McCormick family")
    a = Fr(1, 6)
    for k in range(2, 9):
        eps = Fr(1, 10 ** k)
        T = mc_widest(a, eps, lambda lx, ux: Fr(1, 5))
        bound = 0.2 ** 2 / (2 * math.sqrt(10.0 ** -k))
        print(f"  fixed 1/5, a = 1/6, eps = 1e-{k}: T = {T} (exact rationals); bound {bound:.1f}")
        sys.stdout.flush()
    mp.mp.dps = 60
    sched, th0 = SCHED["width 1/10 + w/5"]
    mp.mp.dps = 400
    aw = build(sched, "LR" * 120)
    mp.mp.dps = 60
    aw = +aw
    for k in range(2, 9):
        eps = mp.mpf(10) ** (-k)
        T = mc_widest(aw, eps, lambda lx, ux: mp.mpf(1) / 10 + (ux - lx) / 5, yclamp=mp.mpf(1) / 5)
        bound = 0.1 ** 2 / (2 * math.sqrt(10.0 ** -k))
        print(f"  width schedule, a = {mp.nstr(aw, 12)}, eps = 1e-{k}: T = {T} (60 digits); bound {bound:.1f}")
        sys.stdout.flush()
    mp.mp.dps = 400


if __name__ == "__main__":
    parts = sys.argv[1:] or ["A1", "A3", "A4"]
    for p in parts:
        {"A1": part_A1_A2, "A3": part_A3, "A4": part_A4}[p]()
        sys.stdout.flush()
