"""Closing audit A, item 3: robust-branching.md, Section 11 changes.
Independent code, exact rationals.

(A) Theorem A(ii): clip schedules, alternating points and itineraries with runs
    of length <= 2; 1D kink (alpha = 1) and McCormick x-only chain (|c| = 1).
    Node I_k of the chain is open iff  1D:  rho_k (1 - rho_k) w_k^2 > eps
                                       McC: rho_k (1 - rho_k) w_k   > eps
    and T = 2 #open + 1 (children not containing the kink are closed).
(B) Midpoint fallback: S = ceil(log2(theta/d0)) + 1 for theta <= 1/3.
(C) Proposition D(i): recentring clamp RC_theta uses exactly S = J + 1 splits.
Run: python3 robust_audit.py > robust_audit.log
"""
import random
from fractions import Fraction as Fr


# ---------------------------------------------------------------- helpers
def ceil_pow(base, target):
    """least integer k >= 0 with base^k >= target (base > 1), for exact rationals."""
    k, v = 0, Fr(1)
    while v < target:
        v *= base
        k += 1
    return k


def K_general(C, eps, th0, expo):
    """ceil( log(C/eps) / (expo * log(1/th0)) ) computed exactly, as an integer >= 0
    when C/eps >= 1; returns the least k >= 0 with (1/th0)^(expo k) >= C/eps."""
    if C / eps <= 1:
        return 0
    return ceil_pow((1 / th0) ** expo, C / eps)


# ---------------------------------------------------------------- (A) clip schedules
def schedule_fixed(th):
    return lambda k, l, u: th


def schedule_depth_alt(th_a, th_b):
    return lambda k, l, u: th_a if k % 2 == 0 else th_b


def _rnd(x):
    """round to the dyadic grid 2^-30 (keeps rationals small; the schedule is still a
    deterministic function of the box)."""
    return Fr(int(x * 2 ** 30), 2 ** 30)


def schedule_width(k, l, u):
    return Fr(1, 10) + _rnd(u - l) / 5


def schedule_pos(k, l, u):
    return Fr(1, 8) + _rnd(l) / 4


def itinerary_point(sched, itin):
    """Nested closed zones; return the final interval (a lies in it)."""
    l, u = Fr(0), Fr(1)
    for k, side in enumerate(itin):
        th = sched(k, l, u)
        w = u - l
        if side == 'L':
            u = l + th * w
        else:
            l = u - th * w
    return l, u


def clip_chain(sched, a, eps, model, kmax=10 ** 6):
    """Follow the clip schedule on the kink a; count open chain nodes."""
    l, u = Fr(0), Fr(1)
    k = 0
    opened = 0
    while k < kmax:
        w = u - l
        if not (l < a < u):
            break
        rho = (a - l) / w
        bnd = rho * (1 - rho) * (w * w if model == '1d' else w)
        if bnd <= eps:
            break
        opened += 1
        th = sched(k, l, u)
        if rho < th:
            s = l + th * w
        elif rho > 1 - th:
            s = u - th * w
        else:
            break  # split at a: chain ends
        if a < s:
            u = s
        else:
            l = s
        k += 1
    return 2 * opened + 1


def part_A(rng):
    print('== (A) Theorem A(ii)')
    scheds = [('fixed 1/5', schedule_fixed(Fr(1, 5)), Fr(1, 5)),
              ('depth-alt 1/5,1/4', schedule_depth_alt(Fr(1, 5), Fr(1, 4)), Fr(1, 5)),
              ('width 1/10+w/5', schedule_width, Fr(1, 10)),
              ('position 1/8+l/4', schedule_pos, Fr(1, 8)),
              ('fixed 2/5', schedule_fixed(Fr(2, 5)), Fr(2, 5)),
              ('fixed 1/10', schedule_fixed(Fr(1, 10)), Fr(1, 10))]
    epss = [Fr(1, 10 ** e) for e in (2, 3, 4, 6, 8, 12, 16, 24, 32, 48)]
    depth = 200
    tot = {'alt_1d': [0, 0], 'alt_mcc_Kp': [0, 0], 'r2_1d': [0, 0], 'r2_mcc_Kp': [0, 0], 'r2_mcc_Kp2': [0, 0]}
    for name, sch, th0 in scheds:
        # alternating points
        for itin0 in ('LR', 'RL'):
            itin = (itin0 * depth)[:depth]
            l, u = itinerary_point(sch, itin)
            a = (l + u) / 2
            for eps in epss:
                if eps >= th0 / 4:
                    continue
                T1 = clip_chain(sch, a, eps, '1d')
                K = K_general(th0 / 4, eps, th0, 2)
                tot['alt_1d'][0] += 1; tot['alt_1d'][1] += T1 < 2 * K + 1
                T2 = clip_chain(sch, a, eps, 'mcc')
                Kp = K_general(th0 / 4, eps, th0, 1)
                tot['alt_mcc_Kp'][0] += 1; tot['alt_mcc_Kp'][1] += T2 < 2 * Kp + 1
                if name == 'fixed 1/5' and itin0 == 'LR' and eps in (Fr(1, 10 ** 4), Fr(1, 10 ** 16), Fr(1, 10 ** 48)):
                    print(f'  fixed 1/5 alternating a={float(a):.12f}: eps={float(eps):.0e}: 1D T={T1} >= 2K+1={2 * K + 1}; '
                          f'McCormick x-only T={T2} >= 2K\'+1={2 * Kp + 1}')
        # runs of length <= 2
        for _ in range(12):
            itin = []
            side = rng.choice('LR')
            while len(itin) < depth:
                itin += [side] * rng.choice((1, 2))
                side = 'R' if side == 'L' else 'L'
            itin = itin[:depth]
            l, u = itinerary_point(sch, itin)
            a = (l + u) / 2
            for eps in epss:
                if eps >= th0 / 4:
                    continue
                T1 = clip_chain(sch, a, eps, '1d')
                K2 = K_general(th0 ** 2 / 4, eps, th0, 2)
                tot['r2_1d'][0] += 1; tot['r2_1d'][1] += T1 < 2 * K2 + 1
                T2 = clip_chain(sch, a, eps, 'mcc')
                Kp = K_general(th0 / 4, eps, th0, 1)
                Kp2 = K_general(th0 ** 2 / 4, eps, th0, 1)
                tot['r2_mcc_Kp'][0] += 1; tot['r2_mcc_Kp'][1] += T2 < 2 * Kp + 1
                tot['r2_mcc_Kp2'][0] += 1; tot['r2_mcc_Kp2'][1] += T2 < 2 * Kp2 + 1
    for k, (n, v) in tot.items():
        print(f'  {k}: {n} cases, violations {v}')
    # explicit violation of K' (theta0/4) at a runs-<=2 point: fixed 1/5, itinerary L L R L R ...
    sch = schedule_fixed(Fr(1, 5))
    l, u = itinerary_point(sch, ['L', 'L'] + list('RL' * depth)[:depth])
    a = (l + u) / 2
    for eps in (Fr(1, 25), Fr(3, 100), Fr(1, 100), Fr(9, 1000)):
        T2 = clip_chain(sch, a, eps, 'mcc')
        Kp = K_general(Fr(1, 20), eps, Fr(1, 5), 1)
        Kp2 = K_general(Fr(1, 100), eps, Fr(1, 5), 1)
        print(f'  fixed 1/5, itinerary LLRLR..., a={float(a):.6f}, eps={eps}: McCormick x-only T={T2}; '
              f'2K\'+1 with theta0/4: {2 * Kp + 1}; with theta0^2/4: {2 * Kp2 + 1}')
    # the step-4 inequality rho_k > theta^r/2 along random itineraries with runs <= 3
    viol = checked = 0
    for name, sch, th0 in scheds[:4]:
        for _ in range(20):
            itin = []
            side = rng.choice('LR')
            while len(itin) < 80:
                itin += [side] * rng.choice((1, 2, 3))
                side = 'R' if side == 'L' else 'L'
            itin = itin[:80]
            l0, u0 = itinerary_point(sch, itin)
            a = (l0 + u0) / 2
            l, u = Fr(0), Fr(1)
            for k in range(60):
                w = u - l
                rho = (a - l) / w
                r = 1
                while itin[k + r] == itin[k]:
                    r += 1
                d = min(rho, 1 - rho)
                checked += 1
                if not (d > th0 ** r / 2 and rho * (1 - rho) >= th0 ** r / 4):
                    viol += 1
                th = sch(k, l, u)
                if itin[k] == 'L':
                    u = l + th * w
                else:
                    l = u - th * w
    print(f'  step 4: d_k > theta0^r/2 and rho(1-rho) >= theta0^r/4 along runs <= 3: {checked} steps, violations {viol}')


# ---------------------------------------------------------------- (B) midpoint fallback
def S_rule(a, rule, th, kmax=100000):
    """Number of splits until the split point is the kink (eps = 0)."""
    l, u = Fr(0), Fr(1)
    for s_count in range(1, kmax):
        w = u - l
        rho = (a - l) / w
        if th <= rho <= 1 - th:
            return s_count
        if rule == 'mid':
            s = l + w / 2
        elif rule == 'rc':
            if rho < th:
                s = l + max(th * w, 2 * (a - l))
            else:
                s = u - max(th * w, 2 * (u - a))
            assert l + th * w <= s <= u - th * w
        elif rule == 'clip':
            s = l + th * w if rho < th else u - th * w
        if s == a:
            return s_count
        if a < s:
            u = s
        else:
            l = s
    return None


def test_points(th, rng, count):
    pts = []
    for _ in range(count):
        e = rng.uniform(0, 12)
        pts.append(Fr(rng.randint(1, 10 ** 6), 10 ** 6) * Fr(1, 10 ** int(e)) * Fr(rng.randint(1, 9), 10))
    for j in range(0, 30):
        for base in (th ** j, th ** j / 2, Fr(1, 2 ** j), th / 2 ** j):
            for pert in (0, Fr(1, 10 ** 6), -Fr(1, 10 ** 6), Fr(1, 100), -Fr(1, 100)):
                pts.append(base * (1 + pert))
    return [d for d in pts if 0 < d < Fr(1, 2)]


def part_B(rng):
    print('== (B) midpoint fallback: S = ceil(log2(theta/d0)) + 1 for d0 < theta <= 1/3')
    for th in (Fr(1, 10), Fr(1, 5), Fr(1, 4), Fr(3, 10), Fr(1, 3)):
        bad = n = 0
        for d0 in test_points(th, rng, 1500):
            if d0 >= th:
                continue
            for a in (d0, 1 - d0):
                S = S_rule(a, 'mid', th)
                pred = ceil_pow(2, th / d0) + 1
                n += 1
                bad += S != pred
        print(f'  theta={th}: {n} kinks, mismatches {bad}')
    # beyond 1/3 the midpoint fallback traps at 1/3 (doubling map orbit 1/3, 2/3, ...)
    th = Fr(2, 5)
    print(f'  theta=2/5, a=1/3: splits before landing (limit 2000): {S_rule(Fr(1, 3), "mid", th, kmax=2000)} (None = trapped)')


# ---------------------------------------------------------------- (C) recentring clamp
def J_of(d0, th):
    j = 0
    while d0 < th ** (j + 1):
        j += 1
    return j


def best_safe_S(d0, th):
    """Least number of theta-safe splits that land on the kink at distance d0 (offline
    optimum, exhaustive over the relevant choices): a split at relative s in [th, 1-th];
    while the kink is in a zone, the best continuation keeps the smallest child with
    the kink, and the kink can be hit once its distance is >= th^2 (split first at
    s in [d/(1-th), d/th] ∩ [th, 1-th] ...)."""
    # independent brute force over a grid of safe split points, depth-limited BFS on distances
    from collections import deque
    grid = [th + (1 - 2 * th) * Fr(k, 40) for k in range(41)]
    start = min(d0, 1 - d0)
    q = deque([(start, 0)])
    seen = {start}
    while q:
        d, k = q.popleft()
        if th <= d <= 1 - th:
            return k + 1
        if k > 60:
            return None
        for s in grid:
            # kink at relative d; split at s; child containing kink
            if d < s:
                nd = d / s
            else:
                nd = (d - s) / (1 - s)
            nd = min(nd, 1 - nd)
            if nd not in seen and len(seen) < 20000:
                seen.add(nd)
                q.append((nd, k + 1))
    return None


def part_C(rng):
    print('== (C) Proposition D(i): RC_theta uses exactly J + 1 splits')
    for th in (Fr(1, 10), Fr(1, 5), Fr(1, 4), Fr(3, 10), Fr(1, 3)):
        bad = n = 0
        worst_clip = 0
        for d0 in test_points(th, rng, 1500):
            for a in (d0, 1 - d0):
                S = S_rule(a, 'rc', th)
                J = J_of(d0, th)
                n += 1
                bad += S != J + 1
                Sc = S_rule(a, 'clip', th, kmax=5000)
                if Sc is not None:
                    worst_clip = max(worst_clip, Sc - (J + 1))
        print(f'  theta={th}: {n} kinks, S_RC != J+1: {bad}; clip exceeds J+1 by up to {worst_clip}')
    # grid brute force of the offline optimum on a few kinks (sanity check of Prop. C's bound)
    th = Fr(1, 5)
    rows = []
    for d0 in (Fr(1, 6), Fr(1, 100), Fr(3, 1000), Fr(1, 26), Fr(1, 24), Fr(1, 10 ** 5)):
        rows.append((d0, J_of(d0, th) + 1, best_safe_S(d0, th), S_rule(d0, 'rc', th)))
    print('  theta=1/5: (d0, J+1, grid-optimal safe S, S_RC):', [(str(r[0]), r[1], r[2], r[3]) for r in rows])


def main():
    rng = random.Random(11)
    part_A(rng)
    part_B(rng)
    part_C(rng)


if __name__ == '__main__':
    main()
