"""Independent checks of Lemma 2, Lemma 3 (via Theorem 1), Theorem 1 and Corollaries 1-3."""
import random
import sys
from fractions import Fraction as F
from itertools import product

from tools import (q, is_pd, violators_fp, violators_box, theorem1_G, theorem1_table,
                   normalize, zero_one_solutions, predicted)

random.seed(7)
fails = 0


def report(name, bad, total, extra=""):
    global fails
    fails += bad
    print(f"[{name}] {total} instances: {bad} failures {extra}")


# ---------------------------------------------------------------- oracle cross-check
def oracle_crosscheck():
    """The forward Fincke-Pohst enumerator must agree with the Cauchy-Schwarz box."""
    bad = cnt = 0
    for _ in range(150):
        N = random.randint(2, 4)
        V = [[random.randint(-3, 3) for _ in range(N)] for _ in range(N + 1)]
        G = [[F(sum(r[i] * r[j] for r in V)) for j in range(N)] for i in range(N)]
        if not is_pd(G):
            continue
        X = normalize(G)
        box = violators_box(X)
        if box is None:
            continue
        cnt += 1
        bad += box != violators_fp(X) or box != violators_fp(X, zero_first=True)
    report("oracle: Fincke-Pohst (both orders) == Cauchy-Schwarz box, random PD", bad, cnt)


# ---------------------------------------------------------------- Theorem 1
def check_instance(A, b, gamma2=None, h2=None, use_box=False):
    """Returns (ok, solvable, viol, X)."""
    n = len(A[0])
    G = theorem1_G(A, b, gamma2, h2)
    if gamma2 is None and h2 is None:
        assert G == [[F(x) for x in row] for row in theorem1_table(A, b)]
    X = normalize(G)
    ok = X[0][0] == 1 and is_pd(X)
    viol = violators_box(X) if use_box else violators_fp(X, zero_first=True)
    if viol is None:
        viol = violators_fp(X, zero_first=True)
    sols = zero_one_solutions(A, b)
    ok &= viol == predicted(sols)
    if sols and viol:
        hh = F(n + 1) if h2 is None else F(h2)
        g2 = F(n + 1) if gamma2 is None else F(gamma2)
        mq = min(q(X, v) for v in viol)
        ok &= mq == (n - g2) / (4 * (g2 + hh))
        ok &= all(q(X, v) == mq for v in viol)  # every violator has the same value
    return ok, bool(sols), viol, X


def subset_sum_random(k, nmax=5, lo=-6, hi=9):
    inst = []
    for _ in range(k):
        n = random.randint(1, nmax)
        a = [random.randint(lo, hi) for _ in range(n)]
        if random.random() < 0.5:
            x = [random.randint(0, 1) for _ in range(n)]
            s = sum(ai * xi for ai, xi in zip(a, x))
        else:
            s = random.randint(lo * n, hi * n)
        inst.append(([a], [s]))
    return inst


def multi_row_random(k):
    inst = []
    for _ in range(k):
        p, n = random.randint(1, 4), random.randint(1, 5)
        A = [[random.randint(-4, 4) for _ in range(n)] for _ in range(p)]
        if random.random() < 0.6:
            x = [random.randint(0, 1) for _ in range(n)]
            b = [sum(A[r][i] * x[i] for i in range(n)) for r in range(p)]
        else:
            b = [random.randint(-5, 5) for _ in range(p)]
        inst.append((A, b))
    return inst


def x3c_random(k, qs=(2, 3, 4), max_extra=5):
    inst = []
    for _ in range(k):
        qq = random.choice(qs)
        U = list(range(3 * qq))
        sets = [tuple(sorted(random.sample(U, 3))) for _ in range(random.randint(0, max_extra))]
        if random.random() < 0.3 and sets:
            sets.append(sets[0])  # repeated set
        if random.random() < 0.5:
            random.shuffle(U)
            sets += [tuple(sorted(U[3 * j:3 * j + 3])) for j in range(qq)]
        if not sets:
            sets = [tuple(U[:3])]
        random.shuffle(sets)
        A = [[int(e in S) for S in sets] for e in range(3 * qq)]
        inst.append((A, [1] * (3 * qq), qq))
    return inst


def run(name, inst, **kw):
    bad = yes = 0
    for A, b in inst:
        ok, y, _, _ = check_instance(A, b, **kw)
        bad += not ok
        yes += y
    report(name, bad, len(inst), f"({yes} solvable)")


def edge_cases():
    """Hand-picked: zeros and duplicates in a, s = 0, n = 1, all-solutions, negative targets."""
    inst = [([[0, 0, 1]], [0]), ([[0, 0, 1]], [1]), ([[1]], [0]), ([[1]], [1]), ([[1]], [2]),
            ([[2]], [1]), ([[-3, 3]], [0]), ([[1, 1, 1, 1]], [2]), ([[5, -5, 5]], [-5]),
            ([[0]], [0]), ([[0]], [1]), ([[1, 2], [3, 4]], [4, 6]), ([[1, 2], [3, 4]], [3, 7]),
            ([[1, 6]], [6]), ([[1, 6]], [7]), ([[2, 2, 2]], [3])]
    bad = 0
    for A, b in inst:
        ok, y, viol, _ = check_instance(A, b, use_box=True)
        bad += not ok
    report("edge cases (zeros, duplicates, n=1, s=0, b=0 columns) with box oracle", bad, len(inst))


def gamma_window():
    """Lemma 2 with M = 1 needs n < gamma^2 <= n+1. Boundary values inside must work; values
    outside must fail on some instance (gamma^2 = n: solutions not strictly closer;
    gamma^2 > n+1: 0/1 points with |Ax-b|^2 = 1 become strictly closer)."""
    inst = subset_sum_random(250, nmax=4, lo=0, hi=6)
    for label, g2f, expect_ok in [("gamma^2 = n+1", lambda n: n + 1, True),
                                  ("gamma^2 = n+1/1000", lambda n: F(n) + F(1, 1000), True),
                                  ("gamma^2 = n+1/2", lambda n: F(n) + F(1, 2), True),
                                  ("gamma^2 = n (outside)", lambda n: F(n), False),
                                  ("gamma^2 = n+1+1/1000 (outside)", lambda n: F(n + 1) + F(1, 1000), False)]:
        bad = 0
        for A, b in inst:
            n = len(A[0])
            g2 = F(g2f(n))
            h2 = g2  # 8 h^2 >= gamma^2
            ok, _, _, _ = check_instance(A, b, gamma2=g2, h2=h2)
            bad += not ok
        good = (bad == 0) if expect_ok else (bad > 0)
        global fails
        fails += not good
        print(f"[gamma window: {label}] {len(inst)} instances: {bad} mismatches "
              f"({'expected 0' if expect_ok else 'expected > 0'}) -> {'OK' if good else 'UNEXPECTED'}")


def h_threshold():
    inst = subset_sum_random(250, nmax=4, lo=0, hi=6)
    for label, h2f, expect_ok in [("h^2 = (n+1)/8 (boundary)", lambda n: F(n + 1, 8), True),
                                  ("h^2 = 7/3 (n+1)", lambda n: F(7 * (n + 1), 3), True),
                                  ("h^2 = 10^6 (n+1)", lambda n: F(10 ** 6 * (n + 1)), True),
                                  ("h^2 = (n+1)/9 (below)", lambda n: F(n + 1, 9), None),
                                  ("h^2 = (n+1)/200 (below)", lambda n: F(n + 1, 200), False)]:
        bad = 0
        for A, b in inst:
            n = len(A[0])
            ok, _, _, _ = check_instance(A, b, h2=h2f(n))
            bad += not ok
        if expect_ok is None:
            print(f"[h threshold: {label}] {bad} mismatches (informational: the condition is only sufficient)")
            continue
        good = (bad == 0) if expect_ok else (bad > 0)
        global fails
        fails += not good
        print(f"[h threshold: {label}] {len(inst)} instances: {bad} mismatches -> {'OK' if good else 'UNEXPECTED'}")


def x3c_checks():
    bad = yes = 0
    maxent = 0
    for A, b, qq in x3c_random(150):
        n = len(A[0])
        ok, y, viol, X = check_instance(A, b)
        G = theorem1_table(A, b)
        ent = max(abs(x) for row in G for x in row)
        maxent = max(maxent, ent)
        ok &= ent <= max(8 * (n + 1), 3 * qq + 2 * n + 1)
        ok &= all(sum(t != 0 for t in v[1:]) == qq + 1 for v in viol)  # |supp w| = q+1
        # Corollary 2: flipped matrix, restricted families
        D = [1] + [-1] * n + [1]
        Xf = [[D[i] * D[j] * X[i][j] for j in range(n + 2)] for i in range(n + 2)]
        vf = violators_fp(Xf, zero_first=True)
        ok &= vf == {tuple(D[i] * v[i] for i in range(n + 2)) for v in viol}
        sols = zero_one_solutions(A, b)
        ok &= {v for v in vf if set(v) <= {0, 1}} == {(0,) + x + (1,) for x in sols}
        ok &= any(v[0] == 0 and set(v) <= {-1, 0, 1} for v in vf) == bool(sols)
        # Corollary 3: mu
        mu = max([F(0)] + [-q(X, v) for v in viol])
        ok &= mu == (F(1, 8 * (n + 1)) if sols else 0)
        bad += not ok
        yes += y
    report("X3C q in {2,3,4}, repeated sets allowed: Thm 1, Cor 1(ii),(iii), Cor 2, Cor 3", bad, 150,
           f"({yes} with a cover; largest |G entry| {maxent})")


def best_additive_gap():
    """Observation: over the admissible window gamma^2 in (n, n+1], 8h^2 >= gamma^2, the violation
    (gamma^2 - n)/(4(gamma^2 + h^2)) is maximal at gamma^2 = n+1, h^2 = (n+1)/8: 2/(9(n+1))."""
    bad = 0
    for A, b in subset_sum_random(100, nmax=4, lo=0, hi=5):
        n = len(A[0])
        ok, y, viol, X = check_instance(A, b, h2=F(n + 1, 8))
        if y:
            bad += min(q(X, v) for v in viol) != -F(2, 9 * (n + 1))
        bad += not ok
    report("gap 2/(9(n+1)) at h^2 = (n+1)/8", bad, 100)


if __name__ == "__main__":
    oracle_crosscheck()
    edge_cases()
    run("subset sum, a in -6..9 (zeros, negatives), n <= 5, h^2 = n+1", subset_sum_random(400))
    run("0/1 equations, 1-4 rows, entries -4..4, n <= 5", multi_row_random(300))
    run("subset sum, box oracle (provably complete)", subset_sum_random(120, nmax=3, lo=0, hi=5), use_box=True)
    gamma_window()
    h_threshold()
    x3c_checks()
    best_additive_gap()
    print("ALL OK" if fails == 0 else f"FAILURES: {fails}")
    sys.exit(0 if fails == 0 else 1)
