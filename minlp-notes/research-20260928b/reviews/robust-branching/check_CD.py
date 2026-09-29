"""Independent checks of Propositions C and D (robust-branching.md, Sections 4-5). Review code only.
Exact rational arithmetic throughout.

[C1] 1D chain, kink at a < theta: S of the recentring clamp RC_theta and of the clip C_theta,
     against J = min{j >= 0 : a >= theta^(j+1)} (= ceil(log(theta/a)/log(1/theta))) and
     m = min{j >= 0 : a >= theta^(j+1)/2}. Checks S_RC <= m + 2 <= J + 2 (Proposition D(i)) and
     tests the sharper S_RC = J + 1 (the Proposition C lower bound).
[C2] Proposition C: T >= 2J + 1 when alpha a^2 (1-theta)/theta > eps, for RC and C at alpha = 1.
[D2] Proposition D(ii): McCormick family (c = -1), widest side, ties to x, RC_theta on both
     coordinates. T is non-increasing in eps for a deterministic rule, so eps = 0 (open iff the box
     straddles a) gives sup_eps T. Compared with 1 + 4 theta^-(m+2)/(1-theta) and
     1 + 2/(theta^2 (1-theta) d0).
"""
import random
import sys
from fractions import Fraction as Fr


def rc_point(p, l, u, th):
    w = u - l
    if p < l + th * w:
        return l + max(th * w, 2 * (p - l))
    if p > u - th * w:
        return u - max(th * w, 2 * (u - p))
    return p


def clip_point(p, l, u, th):
    w = u - l
    return min(max(p, l + th * w), u - th * w)


def chain(a, th, rule, eps=None, cap=400):
    """Returns (S, T): splits until a split lands on a (eps None), or T at tolerance eps."""
    l, u = Fr(0), Fr(1)
    S, T = 0, 1
    for _ in range(cap):
        if eps is not None and (a - l) * (u - a) <= eps:
            return S, T
        s = rule(a, l, u, th)
        S += 1
        T += 2
        if s == a:
            return S, T
        if a < s:
            u = s
        else:
            l = s
    return None, None  # no split on a within cap steps (clip trap)


def J_of(a, th):
    j = 0
    while a < th ** (j + 1):
        j += 1
    return j


def m_of(a, th):
    j = 0
    while a < th ** (j + 1) / 2:
        j += 1
    return j


def part_C1():
    print("[C1] 1D: S of RC_theta and C_theta against J + 1 (lower bound of Proposition C)")
    rng = random.Random(2026)
    for th in (Fr(1, 10), Fr(1, 5), Fr(1, 4), Fr(3, 10), Fr(1, 3)):
        As = [Fr(1, 10 ** k) for k in range(1, 31)]
        As += [th ** j * f for j in range(1, 12) for f in (Fr(1, 2), Fr(1, 2) + Fr(1, 10 ** 9), Fr(999, 1000),
                                                             Fr(1001, 1000), Fr(1, 1))]
        As += [Fr(rng.randrange(1, 10 ** 12), 10 ** 12) * th ** rng.randrange(0, 15) for _ in range(3000)]
        As = [a for a in As if 0 < a < th]
        n = len(As)
        viol_D = viol_eq = 0
        worst_clip = 0
        traps = 0
        hist = {}
        for a in As:
            J, m = J_of(a, th), m_of(a, th)
            S_rc, _ = chain(a, th, rc_point)
            S_cl, _ = chain(a, th, clip_point)
            if S_cl is None:
                traps += 1
                S_cl = 0
            if not (S_rc <= m + 2 <= J + 2):
                viol_D += 1
            if S_rc != J + 1:
                viol_eq += 1
            worst_clip = max(worst_clip, S_cl - (J + 1))
            hist[S_rc - J - 1] = hist.get(S_rc - J - 1, 0) + 1
        print(f"  theta = {th}: {n} kinks; violations of S_RC <= m+2 <= J+2: {viol_D}; "
              f"S_RC - (J+1) histogram {hist}; max S_clip - (J+1) = {worst_clip}; clip never hits a in 400 steps: {traps}")
    a = Fr(1, 10 ** 8)
    print(f"  a = 1e-8, theta = 1/5: J+1 = {J_of(a, Fr(1, 5)) + 1}, S_RC = {chain(a, Fr(1, 5), rc_point)[0]}, "
          f"S_clip = {chain(a, Fr(1, 5), clip_point)[0]}")


def part_C2():
    print("[C2] Proposition C: T >= 2J+1 when a^2 (1-theta)/theta > eps (alpha = 1)")
    th = Fr(1, 5)
    bad = 0
    tot = 0
    rng = random.Random(7)
    for _ in range(3000):
        a = Fr(rng.randrange(1, 10 ** 9), 10 ** 9) * th ** rng.randrange(0, 10)
        if not 0 < a < th:
            continue
        J = J_of(a, th)
        for k in range(2, 30, 3):
            eps = Fr(1, 10 ** k)
            if a * a * (1 - th) / th <= eps:
                continue
            tot += 1
            for rule in (rc_point, clip_point):
                _, T = chain(a, th, rule, eps=eps)
                if T < 2 * J + 1:
                    bad += 1
    print(f"  {tot} (a, eps) pairs x 2 rules: violations {bad}")


def mc_widest(a, eps, th, cap=3_000_000):
    stack = [(Fr(0), Fr(1), Fr(0), Fr(1))]
    T = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        T += 1
        if T > cap:
            return None
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if eps and wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        if wx >= wy:
            s = rc_point(a, lx, ux, th)
            if s == a:
                T += 2
                continue
            stack += [(lx, s, ly, uy), (s, ux, ly, uy)]
        else:
            s = rc_point(ly + rho * wy, ly, uy, th)
            stack += [(lx, ux, ly, s), (lx, ux, s, uy)]
    return T


def part_D2():
    print("[D2] Proposition D(ii): RC_theta, widest side, eps = 0 (sup over eps)")
    rng = random.Random(11)
    th = Fr(1, 5)
    As = [Fr(1, 6), Fr(3, 238), Fr(102, 10000), Fr(1999, 10000), Fr(2001, 10000), Fr(999, 10000),
          Fr(1, 4), Fr(1, 3), Fr(8252, 10000), Fr(1, 100), Fr(1, 1000), Fr(1, 10 ** 4)]
    As += [Fr(rng.randrange(1, 10 ** 6), 10 ** 6) for _ in range(40)]
    worst = 0
    for a in As:
        d0 = min(a, 1 - a)
        T = mc_widest(a, 0, th)
        if d0 >= th:
            m = None
            b1 = b2 = 3
        else:
            m = m_of(d0, th)
            b1 = 1 + 4 * th ** (-(m + 2)) / (1 - th)
            b2 = 1 + 2 / (th ** 2 * (1 - th) * d0)
        ok = T <= b1 <= b2 + Fr(1, 10 ** 12)
        worst = max(worst, float(T / b2))
        if a in As[:12] or not ok:
            print(f"  a = {float(a):.6g}: T(eps=0) = {T}; bound1 = {float(b1):.1f}; bound2 = {float(b2):.1f}; ok = {ok}")
        sys.stdout.flush()
    print(f"  max T / bound2 over {len(As)} kinks: {worst:.4f}")
    th = Fr(1, 3)
    for a in (Fr(1, 6), Fr(1, 10), Fr(3, 238), Fr(1, 50)):
        d0 = min(a, 1 - a)
        T = mc_widest(a, 0, th)
        b2 = 1 + 2 / (th ** 2 * (1 - th) * d0) if d0 < th else 3
        print(f"  theta = 1/3, a = {float(a):.6g}: T(eps=0) = {T}; bound2 = {float(b2):.1f}")


if __name__ == "__main__":
    parts = sys.argv[1:] or ["C1", "C2", "D2"]
    for p in parts:
        {"C1": part_C1, "C2": part_C2, "D2": part_D2}[p]()
        sys.stdout.flush()
