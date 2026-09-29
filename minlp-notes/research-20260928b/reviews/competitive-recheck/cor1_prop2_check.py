"""Exact checks of Proposition 2 (T <= 5 when N_opt = 2), Theorem 1 (T <= 8 N_opt - 9) and the
corrected Corollary 1 (T_eps <= 8 N_opt(eps - 2 delta) - 9 for delta < eps/2; and
T_eps <= 8 N_opt(eps - delta) - 9 when split points have phi < 0), plus the symbolic identities.

Written for this recheck (engine pl1d.py).  Worst case over choices: at every node the adversary
may pick any listed split point; the tree size is maximized by memoized recursion.
 - R_min choices: every exact minimizer among breakpoints plus the midpoint of each flat minimal
   segment (exercises ties).
 - delta-minimizer choices: every breakpoint in {phi <= min + delta} and both ends of every
   sublevel interval (level crossings, generally not knots).  This is a finite subset of the
   adversary's continuum of choices.
Instance families (alpha = 1, m = H - y^2 with H piecewise linear, min m = eps at a knot):
 convex H, non-convex H, dyadic knots with small-integer values (ties), and chord-rigid
 instances (H >= chords of y^2 with a unique breakpoint).
Usage: python3 cor1_prop2_check.py N_INSTANCES SEED
"""
import random
import sys
from fractions import Fraction as Fr

import sympy as sp

from pl1d import PL1D


def identities():
    w, y1, y2, L, U, t1, t2, d, e = sp.symbols("w y1 y2 L U t1 t2 d e")
    ok1 = sp.expand((w - y2) * (y1 - w) + (y2 - L) * (y1 - y2) - (w - L) * (y1 - w) - (y2 - L) * (w - y2)) == 0
    ok2 = sp.expand((w - y2) * (y1 - w) + (y1 - L) * (U - y1) - (w - L) * (U - w)
                    - (y1 - w) * ((U - y1) - (y2 - L))) == 0
    ok3 = sp.expand((t1 + d) * (e - t1) - (t2 + d) * (e - t2) - (t1 - t2) * (e - t1 - t2 - d)) == 0
    ok4 = sp.expand((t2 + d) * (t1 - t2) + (t1 - t2) * (e - t1 - t2 - d) - (t1 - t2) * (e - t1)) == 0
    return ok1, ok2, ok3, ok4


def rand_frac(rng, den=64, lo=0, hi=1):
    return Fr(rng.randint(int(lo * den), int(hi * den)), den)


def instance(rng, fam, eps):
    if fam == "dyadic":
        K = rng.choice([4, 8])
        xs = [Fr(i, K) for i in range(K + 1)]
        ms = [eps * rng.choice([1, 1, 2, 3, 5, 9, 17, 33]) for _ in xs]
        ms[rng.randrange(len(ms))] = eps
        return PL1D(xs, ms)
    k = rng.randint(3, 8)
    xs = sorted(set([Fr(0), Fr(1)] + [Fr(rng.randint(1, 999), 1000) for _ in range(k)]))
    if fam == "nonconvex":
        ms = [eps + rand_frac(rng, 1000, 0, 1) ** 3 / 4 for _ in xs]
        ms[rng.randrange(len(ms))] = eps
        return PL1D(xs, ms)
    if fam == "convex":
        # H convex piecewise linear: increasing slopes
        slopes = sorted(Fr(rng.randint(-3000, 3000), 1000) for _ in range(len(xs) - 1))
        H = [Fr(0)]
        for a, b, s in zip(xs, xs[1:], slopes):
            H.append(H[-1] + s * (b - a))
        ms = [h - x * x for h, x in zip(H, xs)]
        sh = eps - min(ms)
        return PL1D(xs, [m + sh for m in ms])
    if fam == "rigid":
        # H = max(chord(0,s), chord(s,1), extra lines) + eps-type end lines -> breakpoint s rigid
        s = Fr(rng.randint(100, 900), 1000)
        lines = [(s, Fr(0)), (s + 1, -s)]
        for _ in range(rng.randint(1, 4)):
            c = Fr(rng.randint(50, 950), 1000)
            h = c * c + Fr(rng.randint(0, 200), 1000)       # line through (c, h) with random slope
            sl = Fr(rng.randint(-1000, 3000), 1000)
            lines.append((sl, h - sl * c))
        from pl1d import upper_envelope
        xs, Hs = upper_envelope(lines, Fr(0), Fr(1))
        ms = [h - x * x for h, x in zip(Hs, xs)]
        sh = eps - min(ms)
        return PL1D(xs, [m + sh for m in ms])
    raise ValueError(fam)


def main(n, seed):
    rng = random.Random(seed)
    print("symbolic identities (Prop 2 step 4, step 5, Lemma 2 step 4, combination):", identities())
    fams = ["convex", "nonconvex", "dyadic", "rigid"]
    stats = dict(inst=0, n2=0, n2_T5=0, maxT_n2=0, thm1_max_ratio=Fr(0), cor_runs=0, cor_a_viol=0,
                 cor_b_viol=0, strong_viol=0, strong_tight=0, cap=0)
    for it in range(n):
        fam = fams[it % len(fams)]
        eps = Fr(1, rng.choice([100, 1000, 10000]))
        P = instance(rng, fam, eps)
        N, _ = P.greedy()
        if N < 2:
            continue
        stats["inst"] += 1
        try:
            T = P.worst_tree(P.minimizer_choices)
        except RuntimeError:
            stats["cap"] += 1
            continue
        assert T <= 8 * N - 9, ("Thm 1", fam, it)
        stats["thm1_max_ratio"] = max(stats["thm1_max_ratio"], Fr(T, 2 * N - 1))
        if N == 2:
            stats["n2"] += 1
            stats["maxT_n2"] = max(stats["maxT_n2"], T)
            stats["n2_T5"] += (T == 5)
            assert T <= 5, ("Prop 2", fam, it)
        # Corollary 1 with delta-minimizers
        for frac in (Fr(1, 4), Fr(9, 20)):
            delta = frac * eps
            try:
                Td = P.worst_tree(lambda l, u: P.delta_choices(l, u, delta))
                Tb = P.worst_tree(lambda l, u: P.delta_choices(l, u, delta, require_negative=True))
            except RuntimeError:
                stats["cap"] += 1
                continue
            stats["cor_runs"] += 1
            N2 = P.greedy(2 * delta)[0]
            N1 = P.greedy(delta)[0]
            bound_a = 8 * N2 - 9 if N2 >= 2 else 1
            bound_b = 8 * N1 - 9 if N1 >= 2 else 1
            stats["cor_a_viol"] += Td > bound_a
            stats["cor_b_viol"] += Tb > bound_b
            stats["strong_viol"] += Td > bound_b         # the open stronger form, all delta-minimizers
            stats["strong_tight"] += Td == bound_b
    print(stats)
    assert stats["cor_a_viol"] == 0 and stats["cor_b_viol"] == 0


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
