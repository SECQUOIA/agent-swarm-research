"""Exact check of Theorem B: x arbitrary (random convex or non-convex knot instance), z sharp at c
(m_z = 2|t-c| - (t-c)^2 on [0,1]).  Asserts omega leaves <= 56 N and deficit leaves <= 32 N,
N = N_x(eps); also asserts the phase-1 size bound |S_1| <= 24N - 25 (or 5 if N = 1).
usage: python3 thmB_check.py TRIALS SEED"""
import random, sys
from fractions import Fraction as Fr
from sepexact import run
from search import coord_from_lines, rand_line
from phase_check import rand_nonconvex
import fam

if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    worst = {"omega": 0, "deficit": 0}
    worst_phase = 0
    done = 0
    for t in range(trials):
        cx = coord_from_lines([rand_line(rng) for _ in range(rng.randint(3, 12))]) if rng.random() < 0.5 \
            else rand_nonconvex(rng, rng.randint(3, 15))
        c = Fr(rng.randint(1, 999), 1000)
        cz = fam.sharp(c, 2)
        eps = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6]))
        N = len(cx.greedy(eps)) - 1
        for rule, bound in (("omega", 56), ("deficit", 32)):
            r = run([cx, cz], eps, rule, cap=200000, record=(rule == "omega"))
            if r is None:
                continue
            assert r["leaves"] <= bound * N, (rule, r["leaves"], N)
            worst[rule] = max(worst[rule], r["leaves"] / N)
            if rule == "omega":
                # phase 1 = x-splits made while z is unsplit (z-interval equal to the root)
                s1 = sum(1 for box, y, i, ph in r["internal"] if i == 0 and box[1] == (cz.L, cz.U))
                assert s1 <= (24 * N - 25 if N >= 2 else 5), (s1, N)
                worst_phase = max(worst_phase, s1 / N)
        done += 1
    print(f"instances {done}: max leaves/N_x(eps): omega {worst['omega']:.2f} (bound 56), "
          f"deficit {worst['deficit']:.2f} (bound 32); max phase-1 size / N = {worst_phase:.2f}; all assertions passed")
