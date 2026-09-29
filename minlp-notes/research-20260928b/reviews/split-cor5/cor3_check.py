"""Independent exact recheck of the sharpened Corollary 3 of side-results/split-separation-np-complete.md.

Checks:
  A. enumerator sanity: Fincke-Pohst list == brute box search (box from (X^-1)_ii);
  B. padded X3C (n >= 3q), h^2 = (n+1)/8: violated set, gap 2/(9(n+1)) = 2/(9(N-1)), all |X_ij| <= 1;
     unpadded instances where some |X_ij| > 1 (so padding matters);
  C. gap formula (gamma^2 - n)/(4(gamma^2 + h^2)) over several admissible (gamma^2, h^2);
  D. "largest gap within this construction": the |u0| >= 3 case only needs 8h^2 >= gamma^2 - n for this
     lattice (not 8h^2 >= gamma^2), and the M-scaled variant of Lemma 2 allows gamma^2 = n + 8.
     Checks violated sets and gaps for (M=1, gamma^2=n+1, h^2=1/8) and (M=3, gamma^2=n+8, h^2=1),
     plus negative controls just below the refined threshold.
Run: python3 research-20260928b/reviews/split-cor5/cor3_check.py
"""
import random
import sys
from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt, floor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib import (build_X, x3c_matrix, exact_covers, predicted_violators, all_violators, brute_violators,
                 inverse_diag, ldl, qval)

random.seed(28979)
FAIL = []


def expect(cond, msg):
    if not cond:
        FAIL.append(msg)


def random_x3c(qq, nmin, nmax, plant):
    U = tuple(range(3 * qq))
    triples = list(combinations(U, 3))
    n = random.randint(max(nmin, qq if plant else 1), nmax)
    sets = [random.choice(triples) for _ in range(n)]
    if plant:
        perm = list(U)
        random.shuffle(perm)
        for k, p in enumerate(random.sample(range(n), qq)):
            sets[p] = tuple(sorted(perm[3 * k:3 * k + 3]))
    return sets, U


def pad(sets, qq):
    """Repeat the first set until n >= 3q (does not change whether a cover exists)."""
    sets = list(sets)
    while len(sets) < 3 * qq:
        sets.append(sets[0])
    return sets


def gap_of(X, viol):
    return -min(qval(X, v) for v in viol) if viol else F(0)


def check_case(sets, U, gamma2, h2, M, want_gap):
    """Violated set equals Theorem 1(b) and the gap equals want_gap (or 0 without a cover)."""
    A, b = x3c_matrix(sets, U)
    X, G = build_X(A, b, gamma2, h2, M)
    sols = exact_covers(sets, U)
    viol = all_violators(X)
    ok = X[0][0] == 1 and ldl(X) is not None and viol == predicted_violators(sols)
    ok &= gap_of(X, viol) == (want_gap if sols else 0)
    return ok, bool(sols), X


def main():
    # ---- A. enumerator sanity
    nA = 0
    for _ in range(60):
        N = random.randint(2, 4)
        B = [[F(random.randint(-3, 3)) for _ in range(N)] for _ in range(N + 1)]
        X = [[sum(B[k][i] * B[k][j] for k in range(N + 1)) for j in range(N)] for i in range(N)]
        if X[0][0] == 0 or ldl(X) is None:
            continue
        X = [[e / X[0][0] for e in row] for row in X]
        vol = 1
        for d in inverse_diag(X):
            vol *= 2 * isqrt(floor(d)) + 3
        if vol > 200000:  # keep the brute box search small
            continue
        expect(all_violators(X) == brute_violators(X), "enumerator != brute (random)")
        nA += 1
    for sets, U in (([(0, 1, 2)], (0, 1, 2)), ([(0, 1, 2)] * 2, (0, 1, 2)),
                    ([(0, 1, 2), (3, 4, 5)], tuple(range(6))), ([(0, 1, 2), (0, 3, 4)], tuple(range(6)))):
        A, b = x3c_matrix(sets, U)
        n = len(sets)
        for h2 in (F(n + 1, 8), F(1, 8)):
            X, _ = build_X(A, b, n + 1, h2)
            expect(all_violators(X) == brute_violators(X), "enumerator != brute (X3C)")
            nA += 1
    print(f"[A enumerator] Fincke-Pohst list equals brute box search on {nA} PD matrices")

    # ---- B. padded X3C at h^2 = (n+1)/8
    nB = yB = 0
    maxabs = F(0)
    for t in range(45):
        qq = (1, 2, 2, 3)[t % 4]
        sets, U = random_x3c(qq, 1, 3 * qq + 1, plant=(t % 2 == 0))
        sets = pad(sets, qq)
        n = len(sets)
        ok, y, X = check_case(sets, U, n + 1, F(n + 1, 8), 1, F(2, 9 * (n + 1)))
        expect(ok, f"B: q={qq}, n={n}")
        N = len(X)
        expect(F(2, 9 * (n + 1)) == F(2, 9 * (N - 1)), "N-1 = n+1")
        m = max(abs(e) for row in X for e in row)
        expect(m <= 1, f"B: |X_ij| > 1 at q={qq}, n={n}")
        maxabs = max(maxabs, max(abs(X[i][j]) for i in range(N) for j in range(N) if (i, j) != (0, 0)))
        nB += 1
        yB += y
    print(f"[B Corollary 3] {nB} padded X3C instances (q in 1..3, n >= 3q; {yB} with a cover), h^2 = (n+1)/8: "
          f"violated set = Theorem 1(b), gap = 2/(9(n+1)) = 2/(9(N-1)), all |X_ij| <= 1; "
          f"largest off-(0,0) |X_ij| = {maxabs} = {float(maxabs):.4f}")
    # where padding matters: n < 3q
    for qq, n in ((3, 2), (3, 3), (4, 4), (5, 5)):
        sets = [tuple(range(3 * k, 3 * k + 3)) for k in range(min(n, qq))][:n]
        A, b = x3c_matrix(sets, tuple(range(3 * qq)))
        X, _ = build_X(A, b, n + 1, F(n + 1, 8))
        print(f"    unpadded q={qq}, n={n}: X_gg = {X[n + 1][n + 1]} = {float(X[n + 1][n + 1]):.4f}")

    # ---- C. gap formula over admissible (gamma^2, h^2)
    nC = 0
    for sets, U in (([(0, 1, 2), (3, 4, 5), (0, 1, 3)], tuple(range(6))),
                    ([(0, 1, 2)] * 3, (0, 1, 2)),
                    ([(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6)], tuple(range(9)))):
        n = len(sets)
        for gamma2 in (n + F(1, 4), n + F(1, 2), F(n + 1)):
            for h2 in (gamma2 / 8, gamma2, 3 * gamma2):
                ok, _, _ = check_case(sets, U, gamma2, h2, 1, (gamma2 - n) / (4 * (gamma2 + h2)))
                expect(ok, f"C: gamma2={gamma2}, h2={h2}")
                nC += 1
    print(f"[C gap formula] (gamma^2-n)/(4(gamma^2+h^2)) confirmed in {nC} cases "
          f"(gamma^2 in {{n+1/4, n+1/2, n+1}}, h^2 in {{gamma^2/8, gamma^2, 3gamma^2}})")

    # ---- D. larger gaps from the same construction
    # D1: M = 1, gamma^2 = n+1, h^2 = 1/8 (8h^2 = gamma^2 - n)
    nD1 = yD1 = 0
    for t in range(40):
        qq = (1, 2, 2, 3)[t % 4]
        sets, U = random_x3c(qq, 1, 6, plant=(t % 2 == 0))
        n = len(sets)
        ok, y, _ = check_case(sets, U, n + 1, F(1, 8), 1, F(2, 8 * n + 9))
        expect(ok, f"D1: q={qq}, n={n}")
        nD1 += 1
        yD1 += y
    print(f"[D1 M=1, gamma^2=n+1, h^2=1/8] {nD1} X3C ({yD1} with a cover): violated set = Theorem 1(b), "
          f"gap = 2/(8n+9) = 2/(8N-7)")
    # D2: M = 3, gamma^2 = n+8, h^2 = 1 (8h^2 = gamma^2 - n), and the generic h^2 = (n+8)/8
    nD2 = yD2 = 0
    for t in range(40):
        qq = (1, 2, 2, 3)[t % 4]
        sets, U = random_x3c(qq, 1, 6, plant=(t % 2 == 0))
        n = len(sets)
        ok, y, _ = check_case(sets, U, n + 8, F(1), 3, F(2, n + 9))
        expect(ok, f"D2: q={qq}, n={n}")
        ok, _, _ = check_case(sets, U, n + 8, F(n + 8, 8), 3, F(16, 9 * (n + 8)))
        expect(ok, f"D2 generic h: q={qq}, n={n}")
        nD2 += 1
        yD2 += y
    print(f"[D2 M=3, gamma^2=n+8] {nD2} X3C ({yD2} with a cover): violated set = Theorem 1(b); "
          f"gap = 2/(n+9) = 2/(N+7) at h^2 = 1, and 16/(9(n+8)) at h^2 = (n+8)/8")
    # D2 padded so that all |X_ij| <= 1.  Entries: G00 = 4n+36, Ggg = 27q+2n+8, Gii = 31, Gig = 29,
    # Gij <= 27, |G0g| = 2(n+8); so the condition is 27q <= 2n + 28 (n >= 14q suffices).
    for qq, plant, enumerate_ in ((1, True, True), (2, True, True), (2, False, True), (3, True, False)):
        sets, U = random_x3c(qq, 1, 3 * qq, plant)
        while 27 * qq > 2 * len(sets) + 28:
            sets.append(sets[0])
        n = len(sets)
        A, b = x3c_matrix(sets, U)
        X, _ = build_X(A, b, n + 8, F(1), 3)
        m = max(abs(X[i][j]) for i in range(n + 2) for j in range(n + 2) if (i, j) != (0, 0))
        expect(m <= 1, f"D2 padded |X| > 1")
        msg = ""
        if enumerate_:
            ok, y, _ = check_case(sets, U, n + 8, F(1), 3, F(2, n + 9))
            expect(ok, f"D2 padded: q={qq}, n={n}")
            msg = f"cover: {y}, violated set and gap 2/(n+9) ok: {ok}, "
        print(f"    padded M=3, q={qq}, n={n} (27q <= 2n+28): {msg}max off-(0,0) |X_ij| = {m} = {float(m):.4f}")
    # D3: negative controls just below the refined threshold on A 1 = 3*1 (three copies of the universe)
    sets, U = [(0, 1, 2)] * 3, (0, 1, 2)
    A, b = x3c_matrix(sets, U)
    for gamma2, h2, M in ((F(4), F(1, 9), 1), (F(11), F(9, 10), 3)):
        X, _ = build_X(A, b, gamma2, h2, M)
        viol = all_violators(X)
        extra = viol - predicted_violators(exact_covers(sets, U))
        expect(bool(extra) and all(abs(2 * v[0] + 1) == 3 for v in extra), "D3 control")
        print(f"[D3 control] q=1, three copies of U, M={M}, gamma^2={gamma2}, h^2={h2} "
              f"(8h^2 < gamma^2 - n): spurious violators {sorted(extra)} (all with |u0| = 3)")
        X, _ = build_X(A, b, gamma2, (gamma2 - 3) / 8, M)
        expect(all_violators(X) == predicted_violators(exact_covers(sets, U)), "D3 at threshold")
    print("    at 8h^2 = gamma^2 - n the same instance has exactly the Theorem 1(b) violators")
    # D4: the refined threshold for general 0/1 equations (subset sum and 2-row systems)
    nD4 = 0
    for _ in range(80):
        p, n = random.choice([(1, 1), (1, 2), (1, 3), (2, 2), (2, 3)])
        A = [[random.randint(-3, 4) for _ in range(n)] for _ in range(p)]
        if random.random() < 0.5:
            x0 = [random.randint(0, 1) for _ in range(n)]
            b = [sum(A[r][i] * x0[i] for i in range(n)) for r in range(p)]
        else:
            b = [random.randint(-3, 5) for _ in range(p)]
        sols = [x for x in product((0, 1), repeat=n)
                if all(sum(A[r][i] * x[i] for i in range(n)) == b[r] for r in range(p))]
        for gamma2, h2, M in ((F(n + 1), F(1, 8), 1), (F(n + 8), F(1), 3)):
            X, _ = build_X(A, b, gamma2, h2, M)
            viol = all_violators(X)
            ok = viol == predicted_violators(sols)
            ok &= gap_of(X, viol) == ((gamma2 - n) / (4 * (gamma2 + h2)) if sols else 0)
            expect(ok, f"D4: A={A}, b={b}, M={M}")
        nD4 += 1
    print(f"[D4] refined threshold 8h^2 = gamma^2 - n on {nD4} general 0/1-equation instances "
          f"(M=1 and M=3): violated set = Theorem 1(b), gap = (gamma^2-n)/(4(gamma^2+h^2))")

    if FAIL:
        print(f"FAILURES ({len(FAIL)}):")
        for msg in FAIL[:30]:
            print("  ", msg)
        sys.exit(1)
    print("COR3 CHECKS PASSED")


if __name__ == "__main__":
    main()
