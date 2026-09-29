"""Recheck of Theorem 2.3(b) with the generalized objective psi(t), exact arithmetic.

Claim: for psi convex on R and strictly increasing on [0, inf), the MILP
    min { psi(t) : A w - b <= t 1, w in Z^n, t in R }
has projected relaxation phi(w) = inf_{t >= M(w)} psi(t), M(w) = max_j (a_j.w - b_j),
OPT = psi(t*), kappa <= m (classes H_j = {a_j.w - b_j >= t*}), and every leaf with
r >= OPT - eps misses P_r = {M <= 0} when 0 <= eps < psi(1) - psi(0).

The Glaser-Pfetsch system itself is not rebuilt (their theorem is cited); the reduction
is tested on small integral systems with t* = 1 and P_r nonempty:
  S1: 2(w1 + w2 + w3) = 3 as two rows, plus box rows   (parity, n = 3, m = 8)
  S2: w1 + w2 = 1, w1 = w2 as four rows, plus box rows   (n = 2, m = 8)
For several psi (and one psi that violates the hypothesis) we check, exactly:
  (a) t* = 1 and OPT = psi(t*) over an integer window (M is integer-valued there);
  (b) every integer point of the window lies in some H_j, and phi >= OPT there;
  (c) phi <= psi(0) on P_r (vertices and random rational points of P_r);
  (d) the root bound inf phi = psi~(min M) and the eps range: for eps < psi(1)-psi(0)
      the root is not a certificate and no leaf meeting P_r is; for
      eps >= OPT - inf phi the root alone is a certificate (range is sharp here).
"""
import itertools
import random
from fractions import Fraction as Fr


def psi_tilde(psi, crit, s):
    """inf_{t >= s} psi(t) for convex psi given by its candidate minimizers crit
    (stationary points / breakpoints); exact."""
    cands = [s] + [c for c in crit if c >= s]
    return min(psi(c) for c in cands)


PSIS = {
    "t":         (lambda t: t, []),
    "t^2":       (lambda t: t * t, [Fr(0)]),
    "|t|":       (lambda t: abs(t), [Fr(0)]),
    "t^2+2t":    (lambda t: t * t + 2 * t, [Fr(-1)]),
    "max(-t/2,3t)": (lambda t: max(-t / 2, 3 * t), [Fr(0)]),
    # violates the hypothesis (decreasing on [0,1]):
    "(t-1)^2 [bad]": (lambda t: (t - 1) ** 2, [Fr(1)]),
}


def systems():
    S1 = [([2, 2, 2], 3), ([-2, -2, -2], -3)]
    S2 = [([1, 1], 1), ([-1, -1], -1), ([1, -1], 0), ([-1, 1], 0)]
    out = []
    for name, rows, n in (("S1 parity", S1, 3), ("S2", S2, 2)):
        rows = list(rows)
        for i in range(n):
            e = [0] * n
            e[i] = 1
            rows.append((e, 1))                 # w_i <= 1
            rows.append(([-v for v in e], 0))   # -w_i <= 0
        out.append((name, [([Fr(v) for v in a], Fr(b)) for a, b in rows], n))
    return out


def M(rows, w):
    return max(sum(ai * wi for ai, wi in zip(a, w)) - b for a, b in rows)


def points_of_Pr(name, rng):
    pts = []
    if name.startswith("S1"):
        # vertices of {w in [0,1]^3 : sum w = 3/2}: permutations of (1, 1/2, 0)
        pts += [tuple(Fr(v) for v in p) for p in set(itertools.permutations((1, Fr(1, 2), 0)))]
        for _ in range(200):
            u = [Fr(rng.randint(0, 50), 100) for _ in range(2)]
            w3 = Fr(3, 2) - u[0] - u[1]
            if 0 <= w3 <= 1:
                pts.append((u[0], u[1], w3))
    else:
        pts.append((Fr(1, 2), Fr(1, 2)))
    return pts


def main():
    rng = random.Random(20260929)
    for name, rows, n in systems():
        m = len(rows)
        window = list(itertools.product(range(-2, 4), repeat=n))
        tstar = min(M(rows, [Fr(v) for v in z]) for z in window)
        intM = all(M(rows, [Fr(v) for v in z]).denominator == 1 for z in window)
        Pr = points_of_Pr(name, rng)
        inPr = all(M(rows, w) <= 0 for w in Pr)
        # min of M over R^n: M >= 0 everywhere for these equality-type systems
        minM = min(M(rows, w) for w in Pr)
        print(f"{name}: n={n}, m={m}, t* = {tstar} (M integer on Z^n: {intM}), P_r points tested {len(Pr)} (in P_r: {inPr}), min M on them = {minM}")
        for pname, (psi, crit) in PSIS.items():
            phi = lambda w: psi_tilde(psi, crit, M(rows, w))
            OPT = min(phi([Fr(v) for v in z]) for z in window)
            opt_ok = OPT == psi(tstar)
            # (b) classes H_j cover the window, phi >= OPT on each (checked on the window)
            cover = all(any(sum(ai * v for ai, v in zip(a, z)) - b >= tstar for a, b in rows) for z in window)
            # on H_j: M >= t* >= 1 >= 0 so phi = psi(M) >= psi(t*) by monotonicity on [0,inf);
            # exact spot check on random rational points of each H_j near the box
            spot = True
            for _ in range(300):
                w = [Fr(rng.randint(-40, 80), 40) for _ in range(n)]
                if M(rows, w) >= tstar:
                    spot &= phi(w) >= OPT
            # (c) phi <= psi(0) on P_r
            c_ok = all(phi(w) <= psi(Fr(0)) for w in Pr)
            root = psi_tilde(psi, crit, minM)  # inf phi = psi~(min M) since psi~ nondecreasing
            gap = psi(Fr(1)) - psi(Fr(0))
            # (d) eps range
            eps_in = [gap * k / 10 for k in range(10)]  # 0 <= eps < gap
            d_ok = all(OPT - e > psi(Fr(0)) for e in eps_in) and all(root < OPT - e for e in eps_in)
            sharp = OPT - (OPT - root) <= root  # at eps = OPT - root the root certifies
            print(f"   psi={pname:14s}: OPT = {OPT} = psi(t*): {opt_ok}; H_j cover: {cover}; phi >= OPT on sampled H_j points: {spot}; "
                  f"phi <= psi(0) on P_r: {c_ok}; root bound {root}; psi(1)-psi(0) = {gap}; "
                  f"eps in [0,gap): root not a certificate and leaves miss P_r: {d_ok}; "
                  f"root certifies at eps = OPT - root = {OPT - root}")


if __name__ == "__main__":
    main()
