"""Review check of Theorem B, the n-1 sharp-coordinates sketch, and the claim (Answers, item 2)
that the deficit rule is 'competitive within a phase (Theorem A)'.

Part 1: x random (convex / non-convex knot instance, random minimizer selection), z sharp:
  m_z = sigma |t - c| - (t - c)^2, sigma in {2, 3, 10} (>= 2 * width), random c.  Both
  coordinate orders (= both tie orders).  Asserts: (S1)/(S2) on random intervals; omega leaves
  <= 56N - 56 (N >= 2) or 14; deficit leaves <= 32N; phase-1 size <= 24N - 25 (or 5);
  phase-1 nodes of deficit have F_x < -eps/2.
Part 2: n = 3, x random, two sharp coordinates: max leaves / N_x(eps) for omega and deficit.
Part 3: deficit's phase vs n_P.  x: m = t^2 (exact), z: tent with root deficit eps/2 and
  m_z(1/2) = 1/4 - eps/2.  The deficit rule's first x-phase (z = [0,1]) is the R_min tree of x at
  budget eps/2, while an explicit certificate has exactly one box meeting the phase segment
  [0,1] x {1/2}.  omega's phases on the same instance are listed for comparison.
usage: python3 thmB_review.py TRIALS SEED
"""
import random
import sys
from fractions import Fraction as Fr
from sepcore import PL, Quad, run, sharp
from lemmaT_check import rand_convex, rand_nonconvex

ONE = Fr(1)


def check_sharp(cz, c, rng):
    for _ in range(40):
        l = Fr(rng.randint(0, 999), 1000)
        u = Fr(rng.randint(int(l * 1000) + 1, 1000), 1000)
        F, y, w = cz.node(l, u)
        if l < c < u:
            assert y == c and F == -(c - l) * (u - c) and w == (c - l) * (u - c)
        else:
            assert w == 0 and F >= 0


def part1(trials, rng):
    worst = {"omega": Fr(0), "deficit": Fr(0), "phase1": Fr(0)}
    done = 0
    for _ in range(trials):
        sel = rng.choice(["wmax", "left", "right"])
        cx = rand_convex(rng, sel) if rng.random() < 0.5 else rand_nonconvex(rng, sel)
        c = Fr(rng.randint(1, 999), 1000)
        sigma = rng.choice([2, 3, 10])
        cz = sharp(c, sigma)
        check_sharp(cz, c, rng)
        eps = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6])) * Fr(rng.randint(1, 9), 3)
        N = cx.ncert(eps)
        for order in ((0, 1), (1, 0)):
            cs = [cx, cz] if order == (0, 1) else [cz, cx]
            ix = order.index(0)
            for rule in ("omega", "deficit"):
                r = run(cs, eps, rule, cap=100000, record=True)
                assert r is not None
                if rule == "omega":
                    assert r["leaves"] <= (56 * N - 56 if N >= 2 else 14), (r["leaves"], N)
                else:
                    assert r["leaves"] <= 32 * N, (r["leaves"], N)
                worst[rule] = max(worst[rule], Fr(r["leaves"], N))
                ph1 = [bx for bx, i, ph, y in r["internal"] if i == ix and bx[1 - ix] == (cz.L, cz.U)]
                if rule == "omega":
                    assert len(ph1) <= (24 * N - 25 if N >= 2 else 5), (len(ph1), N)
                    worst["phase1"] = max(worst["phase1"], Fr(len(ph1), N))
                else:
                    assert all(cx.node(*bx[ix])[0] < -eps / 2 for bx in ph1)
        done += 1
    return done, worst


def part2(trials, rng):
    worst = {"omega": Fr(0), "deficit": Fr(0)}
    for _ in range(trials):
        cx = rand_convex(rng, "wmax") if rng.random() < 0.5 else rand_nonconvex(rng, "wmax")
        zs = [sharp(Fr(rng.randint(1, 999), 1000), 2) for _ in range(2)]
        eps = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5]))
        N = cx.ncert(eps)
        cs = [cx] + zs
        rng.shuffle(cs)
        for rule in ("omega", "deficit"):
            r = run(cs, eps, rule, cap=200000)
            worst[rule] = max(worst[rule], Fr(r["leaves"], N))
    return worst


def part3():
    rows = []
    for k in range(3, 11):
        eps = Fr(1, 10 ** k)
        cx = Quad(0, 1)
        cz = PL.from_lines([(Fr(0), Fr(0)), (1 - eps, Fr(0)), (1 + eps, -eps)])
        assert min(cz.m(t) for t in cz.x) == 0 and cz.node(Fr(0), ONE) == (-eps / 2, Fr(1, 2), Fr(1, 4))
        rd = run([cx, cz], eps, "deficit", record=True)
        ph = [bx for bx, i, p, y in rd["internal"] if p == 1]
        assert all(i == 0 for bx, i, p, y in rd["internal"] if p == 1) and all(bx[1] == (0, 1) for bx in ph)
        # certificate: strip [0,1] x [2/5,3/5]; below/above: x-pieces valid at budget eps
        # (F_z = 0 on [0,2/5] and on [3/5,1]), built from valid (lower) greedy pieces.
        pieces, a = [], Fr(0)
        while True:
            if cx.valid(a, ONE, eps):
                pieces.append((a, ONE)); break
            lo, hi = a, ONE
            for _ in range(60):
                md = (lo + hi) / 2
                if cx.valid(a, md, eps):
                    lo = md
                else:
                    hi = md
            pieces.append((a, lo)); a = lo
        cert = [((Fr(0), ONE), (Fr(2, 5), Fr(3, 5)))]
        cert += [(p, (Fr(0), Fr(2, 5))) for p in pieces] + [(p, (Fr(3, 5), ONE)) for p in pieces]
        assert all(cx.node(*bx)[0] + cz.node(*bz)[0] + eps >= 0 for bx, bz in cert)
        nP = sum(1 for bx, bz in cert if bz[0] <= Fr(1, 2) <= bz[1])
        ro = run([cx, cz], eps, "omega", record=True)
        phs = {}
        for bx, i, p, y in ro["internal"]:
            phs[p] = phs.get(p, 0) + 1
        lo_, hi_ = cx.ncert_bounds(eps)
        rows.append((k, len(ph), nP, len(cert), rd["nodes"], ro["nodes"], max(phs.values()), (lo_, hi_)))
    return rows


if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    done, w = part1(trials, rng)
    print(f"Part 1: {done} instances x 2 orders x 2 rules; all assertions passed; max leaves/N: "
          f"omega {float(w['omega']):.2f} (bound 56), deficit {float(w['deficit']):.2f} (bound 32); "
          f"max phase-1/N {float(w['phase1']):.2f}", flush=True)
    w2 = part2(trials // 4, rng)
    print(f"Part 2 (n = 3, two sharp): max leaves/N_x(eps): omega {float(w2['omega']):.2f}, "
          f"deficit {float(w2['deficit']):.2f}", flush=True)
    print("Part 3: eps, deficit first-phase internal nodes, n_P of the explicit certificate, "
          "certificate size, deficit nodes, omega nodes, omega's largest phase, N_q(eps) bracket")
    for row in part3():
        print("  eps=1e-%d: deficit phase %d, n_P %d, cert %d, deficit T %d, omega T %d, omega max phase %d, N_x(eps) in %s"
              % row)
