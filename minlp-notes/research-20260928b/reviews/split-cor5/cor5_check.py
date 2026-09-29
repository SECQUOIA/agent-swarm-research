"""Independent exact recheck of Corollary 5 of side-results/split-separation-np-complete.md.

Claims checked, for X3C instances (A = incidence matrix, b = 1, gamma^2 = n+1):
  * closed-form entries of G used in the proof, and the displayed formula for Ghat;
  * (2.3) holds for every h;
  * with 4h^2 = max(3, n+1)*Ghat: X is PD, X00 = 1, the violated splits are those of Theorem 1(b),
    and X and D X D satisfy (4.1), (2.1)-(2.2), (2.3), (4.4), (4.5)-(4.8);
  * the proof's bound max |X_ij| < min(1/3, 1/(n+1)) for (i, j) != (0, 0);
  * invariance of all five families under every sign flip of the variables (small n);
  * checker liveness: probes that violate exactly one family.
Run: python3 research-20260928b/reviews/split-cor5/cor5_check.py
"""
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import (build_X, x3c_matrix, exact_covers, predicted_violators, all_violators, ldl,
                 slacks, satisfies_all, flip)

random.seed(20260929)
FAIL = []


def expect(cond, msg):
    if not cond:
        FAIL.append(msg)


def instances():
    out = []
    U1 = (0, 1, 2)
    for n in range(1, 6):  # q = 1: every set equals the universe
        out.append((1, [U1] * n, U1))
    for qq, count, nmax in ((2, 160, 7), (3, 90, 8)):
        U = tuple(range(3 * qq))
        triples = list(combinations(U, 3))
        for t in range(count):
            n = random.randint(1, nmax)
            sets = [random.choice(triples) for _ in range(n)]
            if t % 2 == 0 and n >= qq:  # plant a cover in half of them
                perm = list(U)
                random.shuffle(perm)
                pos = random.sample(range(n), qq)
                for k, p in enumerate(pos):
                    sets[p] = tuple(sorted(perm[3 * k:3 * k + 3]))
            out.append((qq, sets, U))
    return out


def ghat_true(G):
    return max(abs(G[i][j]) for i in range(len(G)) for j in range(len(G)) if (i, j) != (0, 0))


def main():
    # ---- checker liveness
    def mat(x, Y):
        m = len(x)
        return [[F(1)] + list(x)] + [[x[i]] + list(Y[i]) for i in range(m)]
    probes = {
        "4.1": mat([F(1, 2)], [[F(2, 5)]]),
        "2.3": mat([F(0)] * 2, [[F(2, 5), F(1, 2)], [F(1, 2), F(1)]]),
        "4.5-4.8": mat([F(-3, 5)] * 2, [[F(3, 5), F(1, 10)], [F(1, 10), F(3, 5)]]),
        # 5 variables, unit diagonal, off-diagonal -6/25: PD, only (4.4) with |S| = 5 fails
        "4.4": mat([F(0)] * 5, [[F(1) if i == j else F(-6, 25) for j in range(5)] for i in range(5)]),
        "2.1-2.2": mat([F(0)] * 3, [[F(1) if i == j else F(-2, 5) for j in range(3)] for i in range(3)]),
    }
    for fam, P in probes.items():
        s = slacks(P)
        bad = {k for k, v in s.items() if v is not None and v < 0}
        want = {fam} if fam != "2.1-2.2" else {"2.1-2.2", "4.4"}  # triangles are (4.4) with |S| = 3
        expect(bad == want, f"liveness probe {fam}: flagged {bad}")
    expect(ldl(probes["4.4"]) is not None, "(4.4) probe should be PD")
    print(f"[liveness] 5 probes; each flags exactly its family ((2.1)-(2.2) also as (4.4), |S|=3); "
          f"the (4.4) probe is positive definite")

    insts = instances()
    stats = dict(n=0, cover=0, ghat_formula_mismatch=[], maxratio=F(0), weak44=0, flipped=0,
                 minslack={})
    for qq, sets, U in insts:
        A, b = x3c_matrix(sets, U)
        n = len(sets)
        sols = exact_covers(sets, U)
        pred = predicted_violators(sols)
        stats["n"] += 1
        stats["cover"] += bool(sols)

        # closed-form entries (proof of Corollary 5), at any h
        _, G = build_X(A, b, n + 1, n + 1)
        idx_g = n + 1
        for i in range(1, n + 1):
            expect(G[0][i] == 0, "G0i")
            expect(G[i][i] == 7, "Gii")
            expect(G[i][idx_g] == 5, "Gig")
            for j in range(1, n + 1):
                if i != j:
                    expect(G[i][j] == len(set(sets[i - 1]) & set(sets[j - 1])), "Gij")
        expect(G[idx_g][idx_g] == 3 * qq + 2 * n + 1, "Ggg")
        expect(G[0][idx_g] == -2 * (n + 1), "G0g")
        gt = ghat_true(G)
        gf = max(3 * qq + 2 * n + 1, 2 * (n + 1))
        if gt != gf:
            stats["ghat_formula_mismatch"].append((qq, n, gt, gf))

        # (2.3) for every h: several h^2 values, including below the Theorem 1 threshold
        for h2 in (F(0), F(1, 100), F(n + 1, 8), F(n + 1), F(10 ** 6)):
            X, _ = build_X(A, b, n + 1, h2)
            s = slacks(X)["2.3"]
            expect(s is None or s >= 0, f"(2.3) fails at h2={h2}, q={qq}, n={n}")

        # main claim with the true Ghat and with the displayed formula for Ghat
        eps = min(F(1, 3), F(1, n + 1))
        for gh in {gt, gf}:
            h2 = F(max(3, n + 1) * gh, 4)
            X, _ = build_X(A, b, n + 1, h2)
            expect(X[0][0] == 1 and ldl(X) is not None, "X not PD / X00 != 1")
            expect(all_violators(X) == pred, f"violated set differs, q={qq}, n={n}")
            mx = max(abs(X[i][j]) for i in range(n + 2) for j in range(n + 2) if (i, j) != (0, 0))
            expect(mx < eps, f"max |X_ij| = {mx} >= eps = {eps}, q={qq}, n={n}, Ghat={gh}")
            stats["maxratio"] = max(stats["maxratio"], mx / eps)
            D = [-1] * n + [1]
            for Z, name in ((X, "X"), (flip(X, D), "DXD")):
                ok, s = satisfies_all(Z)
                expect(ok, f"{name} fails {s}, q={qq}, n={n}")
                for k, v in s.items():
                    if v is not None:
                        stats["minslack"][k] = min(stats["minslack"].get(k, v), v)
            XD = flip(X, D)
            vd = all_violators(XD)
            expect({v for v in vd if set(v) <= {0, 1}} == {(0,) + tuple(x) + (1,) for x in sols},
                   "0/1 violators of DXD")
            if n + 1 <= 5 and gh == gt:  # all sign flips
                for sig in product((1, -1), repeat=n + 1):
                    ok, _ = satisfies_all(flip(X, sig))
                    expect(ok, f"flip {sig} breaks a family")
                    stats["flipped"] += 1

        # informational: is the factor max(3, n+1) needed for (4.4) on these instances?
        Xw, _ = build_X(A, b, n + 1, F(3 * gt, 4))
        stats["weak44"] += slacks(Xw)["4.4"] < 0

    print(f"[Corollary 5] {stats['n']} X3C instances (q in {{1,2,3}}, n <= 8; {stats['cover']} with a cover)")
    print(f"  closed-form G entries (G0i=0, Gii=7, Gig=5, Gij=|Si & Sj|, Ggg=3q+2n+1, G0g=-2(n+1)): "
          f"checked on all")
    print(f"  displayed formula Ghat = max(3q+2n+1, 2(n+1)) differs from the true max on "
          f"{len(stats['ghat_formula_mismatch'])} instance(s): {stats['ghat_formula_mismatch']} "
          f"(q, n, true, formula)")
    print(f"  (2.3) at h^2 in {{0, 1/100, (n+1)/8, n+1, 10^6}}: checked on all")
    print(f"  4h^2 = max(3,n+1)*Ghat (true Ghat and formula Ghat): PD, X00=1, violated set = Theorem 1(b), "
          f"X and DXD satisfy (4.1),(2.1)-(2.3),(4.4),(4.5)-(4.8), DXD 0/1 violators = (0,x,1)")
    print(f"  largest max|X_ij| / min(1/3, 1/(n+1)) over (i,j) != (0,0): {stats['maxratio']} "
          f"= {float(stats['maxratio']):.4f} (< 1 required)")
    print(f"  smallest slack per family: " +
          ", ".join(f"{k}: {float(v):.4f}" for k, v in sorted(stats["minslack"].items())))
    print(f"  sign-flip invariance: {stats['flipped']} flipped matrices (all sigma, n+1 <= 5) satisfy all families")
    print(f"  informational: with only 4h^2 = 3*Ghat, (4.4) fails on {stats['weak44']} of {stats['n']}")
    if FAIL:
        print(f"FAILURES ({len(FAIL)}):")
        for msg in FAIL[:30]:
            print("  ", msg)
        sys.exit(1)
    print("COR5 CHECKS PASSED")


if __name__ == "__main__":
    main()
