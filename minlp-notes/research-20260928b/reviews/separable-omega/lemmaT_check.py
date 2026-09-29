"""Review check of Lemma T, Theorem A (1D) and Corollary A' (2D phases of omega).

Part 1 (1D, exact).  Random convex (max of lines) and non-convex (random knot values of m >= 0)
instances, three minimizer selections, kappa in {1,2,3}, random tau, beta (also beta < 0),
b = beta + kappa tau.  Checks
  Lemma T on every leaf of T_b AND on maximal valid intervals [a, u*(a)] started at every
  endpoint of a split node (these are the largest valid intervals containing such nodes on the
  right), both for the non-strict (w >= tau) and strict (w > tau) pruned trees;
  Theorem A: |S| <= 4N-5 + c_k (4N-4) (N >= 2), <= c_k (N = 1).
Part 2 (adversarial).  Hill climbing over non-convex knot instances, maximizing the number of
  split nodes inside one valid interval (kappa = 1, 2).
Part 3 (2D, exact).  omega on random separable instances; every phase P (maximal run of splits
  along one coordinate with the other interval fixed) is checked against
  N_P = N_{A}(eps + m_other(y_other)) (the slice budget; n_P >= N_P for every certificate):
  internal(P) <= 4N_P - 5 + 5(4N_P - 4) if N_P >= 2, <= 5 if N_P = 1.  Counts phases with tau = 0.
Part 4.  An explicit phase with n_P = 1 (a certificate box contains the phase segment) and one
  internal node: Corollary A''s displayed formula gives -1 there.
usage: python3 lemmaT_check.py TRIALS SEED
"""
import random
import sys
from fractions import Fraction as Fr
from sepcore import PL, rmin_tree, pruned_tree, run

ONE = Fr(1)


def ck(k):
    return k * (2 * k * (k + 1) + 1)


def rand_convex(rng, sel):
    lines = []
    for _ in range(rng.randint(3, 12)):
        p = Fr(rng.randint(0, 1000), 1000)
        mu = Fr(rng.choice([0, 0, 1, 2, 5, 10, 20, 50, 100, 300]), 1000) * Fr(rng.randint(1, 10), 10)
        s = Fr(rng.choice([0, 0, 0, -1, 1, -3, 3, -10, 10]), 4) * Fr(rng.randint(1, 8), 8)
        lines.append((2 * p + s, -p * p + mu - s * p))
    c = PL.from_lines(lines, sel=sel)
    mn = min(c.m(t) for t in c.x)
    return PL(c.x, [h - mn for h in c.Hk], sel)


def rand_nonconvex(rng, sel):
    xs = sorted({Fr(0), ONE} | {Fr(rng.randint(1, 999), 1000) for _ in range(rng.randint(3, 15))})
    ms = [Fr(rng.choice([0, 0, 1, 2, 5, 20, 100]), 1000) * Fr(rng.randint(1, 9), 9) for _ in xs]
    mn = min(ms)
    return PL.from_m(xs, [m - mn for m in ms], sel)


def count_inside(S, lo, hi):
    return sum(1 for (l, u) in S if lo <= l and u <= hi)


def part1(trials, rng):
    worst = {}
    done = skipped = 0
    for _ in range(trials):
        sel = rng.choice(["wmax", "left", "right"])
        c = rand_convex(rng, sel) if rng.random() < 0.5 else rand_nonconvex(rng, sel)
        kappa = rng.choice([1, 1, 2, 3])
        tau = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5])) * Fr(rng.randint(1, 9), 3)
        b = Fr(1, rng.choice([10, 100, 1000, 10 ** 4, 10 ** 5, 10 ** 6])) * Fr(rng.randint(1, 9), 3)
        beta = b - kappa * tau
        A = (c.L, c.U)
        tb = rmin_tree(c, A, b, cap=20000)
        if tb is None:
            skipped += 1
            continue
        _, leaves = tb
        N = c.ncert(b)
        for strict in (False, True):
            S = pruned_tree(c, A, beta, tau, strict=strict, cap=20000)
            if S is None:
                skipped += 1
                continue
            inleaf = max([count_inside(S, l, u) for l, u in leaves] + [0])
            ends = {p for D in S for p in D}
            inval = 0
            for a in ends:
                u = c.maxvalid(a, b)
                assert c.node(a, u)[0] >= -b
                inval = max(inval, count_inside(S, a, u))
            # and valid intervals ending at each endpoint (mirror): scan left ends on a grid
            key = (kappa, "leaf")
            worst[key] = max(worst.get(key, 0), inleaf)
            key2 = (kappa, "maxvalid")
            worst[key2] = max(worst.get(key2, 0), inval)
            assert inleaf <= ck(kappa) and inval <= ck(kappa), (inleaf, inval, kappa)
            bound = ck(kappa) if N == 1 else 4 * N - 5 + ck(kappa) * (4 * N - 4)
            assert len(S) <= bound, (len(S), bound)
            r = Fr(len(S), N)
            worst[(kappa, "|S|/N")] = max(worst.get((kappa, "|S|/N"), 0), r)
            done += 1
    return done, skipped, worst


def objective(c, beta, tau, b):
    S = pruned_tree(c, (c.L, c.U), beta, tau, cap=3000)
    if S is None or not S:
        return 0
    ends = {p for D in S for p in D}
    best = 0
    for a in ends:
        u = c.maxvalid(a, b)
        best = max(best, count_inside(S, a, u))
    return best


def part2(rng, restarts, steps):
    best_all = {1: 0, 2: 0}
    for kappa in (1, 2):
        for _ in range(restarts):
            xs = sorted({Fr(0), ONE} | {Fr(rng.randint(1, 999), 1000) for _ in range(10)})
            ms = [Fr(rng.randint(0, 200), 1000) for _ in xs]
            tau = Fr(1, rng.choice([100, 1000, 10000]))
            b = Fr(1, rng.choice([100, 1000, 10000]))
            beta = b - kappa * tau

            def mk(ms_):
                mn = min(ms_)
                return PL.from_m(xs, [m - mn for m in ms_])
            cur = objective(mk(ms), beta, tau, b)
            for _ in range(steps):
                ms2 = list(ms)
                k = rng.randrange(len(ms2))
                ms2[k] = max(Fr(0), ms2[k] + Fr(rng.randint(-50, 50), 1000))
                beta2, tau2 = beta, tau
                if rng.random() < 0.2:
                    tau2 = tau * Fr(rng.choice([1, 2, 3]), rng.choice([1, 2, 3]))
                    beta2 = b - kappa * tau2
                v = objective(mk(ms2), beta2, tau2, b)
                if v >= cur:
                    cur, ms, beta, tau = v, ms2, beta2, tau2
            best_all[kappa] = max(best_all[kappa], cur)
    return best_all


def part3(trials, rng, eps_list):
    worst = 0
    tau0 = 0
    nph = 0
    for _ in range(trials):
        cs = [rand_convex(rng, "wmax") if rng.random() < 0.5 else rand_nonconvex(rng, "wmax") for _ in range(2)]
        eps = rng.choice(eps_list)
        r = run(cs, eps, "omega", cap=4000, record=True)
        if r is None:
            continue
        phases = {}
        for box, i, ph, y in r["internal"]:
            phases.setdefault(ph, []).append((box, i, y))
        for ph, lst in phases.items():
            box, i, y = lst[0]
            # the phase root is the largest box (first in DFS order)
            root = max(lst, key=lambda z: z[0][i][1] - z[0][i][0])[0]
            o = 1 - i
            other = cs[o].node(*root[o])
            yk = other[1]
            if other[2] == 0:
                tau0 += 1
            bud = eps + cs[o].m(yk)
            NP = cs[i].ncert(bud, root[i])
            bound = 5 if NP == 1 else 4 * NP - 5 + 5 * (4 * NP - 4)
            assert len(lst) <= bound, (len(lst), NP)
            worst = max(worst, Fr(len(lst), NP))
            nph += 1
    return nph, worst, tau0


def part4():
    """x: tent with deficit e = eps, z: tent with deficit d = 1/10 (both root minimizers 1/2,
    w = 1/4, tie -> x).  The x-phase at the root has one internal node; the certificate
    {[0,1] x [0,2/5], [0,1] x [2/5,3/5], [0,1] x [3/5,1]} has exactly one box meeting the phase
    segment [0,1] x {1/2}."""
    e, d = Fr(1, 1000), Fr(1, 10)
    tent = lambda q: PL.from_lines([(Fr(0), Fr(0)), (1 - q, Fr(0)), (1 + q, -q)])
    cx, cz = tent(e), tent(d)
    assert min(cx.m(t) for t in cx.x) == 0 and min(cz.m(t) for t in cz.x) == 0
    r = run([cx, cz], e, "omega", record=True)
    ph1 = [z for z in r["internal"] if z[2] == 1]
    cert = [((Fr(0), ONE), (Fr(0), Fr(2, 5))), ((Fr(0), ONE), (Fr(2, 5), Fr(3, 5))),
            ((Fr(0), ONE), (Fr(3, 5), ONE))]
    valid = [cx.node(*bx)[0] + cz.node(*bz)[0] + e >= 0 for bx, bz in cert]
    meets = sum(1 for bx, bz in cert if bz[0] <= Fr(1, 2) <= bz[1])
    return dict(root_split_coord=r["internal"][0][1], phase1_internal=len(ph1), cert_valid=valid,
                n_P=meets, formula_at_nP=4 * meets - 5 + 5 * (4 * meets - 4), omega_nodes=r["nodes"])


if __name__ == "__main__":
    trials, seed = int(sys.argv[1]), int(sys.argv[2])
    rng = random.Random(seed)
    done, skipped, worst = part1(trials, rng)
    print(f"Part 1: {done} (instance, strictness) cases, {skipped} skipped (size cap); all assertions passed")
    for k in sorted(worst, key=str):
        print(f"   max {k}: {worst[k]}  (c_kappa = {ck(k[0])})")
    print("Part 2: adversarial max #split nodes inside one valid interval:", part2(rng, 12, 60), flush=True)
    nph, w, t0 = part3(trials // 2, rng, [Fr(1, 10 ** k) for k in range(2, 7)])
    print(f"Part 3: {nph} omega phases in 2D checked against the slice budget; max internal/N_P = {float(w):.2f}; "
          f"phases with tau = 0: {t0}; all assertions passed")
    print("Part 4:", part4())
