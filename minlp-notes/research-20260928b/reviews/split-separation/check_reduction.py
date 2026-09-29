"""Independent exact checks of Lemmas A, B, C (subset sum -> CLOSER -> split separation).

Y is built directly as a rational Gram matrix, parameterized by gamma^2 and h^2, so gamma
and h need not be rational. For every instance the complete set of violated splits is
computed by exact enumeration (exact_lattice.violators_pd), not by a box search.
"""
import random, sys
from fractions import Fraction as F
from itertools import product, combinations
from exact_lattice import violators_pd, split_q, qform, enum_below, gram, mat_inv
from math import isqrt, floor

random.seed(20260928)


def Y_subset_sum(a, s, M=3, g2=None, h2=None):
    """Index 0 = b0, 1..n = b_i, n+1 = g. Coordinates (sum, parity_1..n, gamma, h)."""
    n = len(a)
    g2 = F(n + 1) if g2 is None else F(g2)
    h2 = g2 if h2 is None else F(h2)
    N = n + 2
    G = [[F(0)] * N for _ in range(N)]
    G[0][0] = 4 * g2 + 4 * h2
    G[0][n + 1] = G[n + 1][0] = -2 * g2
    for i in range(n):
        for j in range(n):
            G[1 + i][1 + j] = F(M * M * a[i] * a[j] + (4 if i == j else 0))
        G[1 + i][n + 1] = G[n + 1][1 + i] = F(M * M * a[i] * s + 2)
    G[n + 1][n + 1] = F(M * M * s * s + n) + g2
    nb = G[0][0]
    return [[x / nb for x in row] for row in G]


def solutions(a, s):
    n = len(a)
    return [x for x in product((0, 1), repeat=n) if sum(ai * xi for ai, xi in zip(a, x)) == s]


def predicted_violators(a, s):
    out = set()
    for x in solutions(a, s):
        out.add((-1,) + x + (-1,))
        out.add((0,) + tuple(-xi for xi in x) + (1,))
    return out


def check_identities(trials=300):
    for _ in range(trials):
        N = random.randint(2, 5)
        Y = [[F(0)] * N for _ in range(N)]
        for i in range(N):
            for j in range(i, N):
                Y[i][j] = Y[j][i] = F(random.randint(-20, 20), random.randint(1, 6))
        Y[0][0] = F(1)
        v = [random.randint(-4, 4) for _ in range(N)]
        e0 = [1] + [0] * (N - 1)
        u = [2 * v[i] + e0[i] for i in range(N)]
        inner = sum(v[i] * (v[j] + e0[j]) * Y[i][j] for i in range(N) for j in range(N))
        q = split_q(Y, v)
        assert q == inner
        assert q == (qform(Y, u) - Y[0][0]) / 4
        w = [-v[i] - e0[i] for i in range(N)]
        assert split_q(Y, w) == q
        # Lemma A with an explicit rational factor B (Y = B^T B)
        d = random.randint(N, N + 2)
        B = [[F(random.randint(-3, 3), random.randint(1, 3)) for _ in range(N)] for _ in range(d)]
        cols = [[B[r][c] for r in range(d)] for c in range(N)]
        YB = gram(cols)
        Bv = [sum(B[r][c] * v[c] for c in range(N)) for r in range(d)]
        lhs = split_q(YB, v)
        rhs = sum((Bv[r] + B[r][0] / 2) ** 2 for r in range(d)) - sum((B[r][0] / 2) ** 2 for r in range(d))
        assert lhs == rhs
    print(f"[identities] {trials} random cases: q(v) = <v(v+e0)^T,Y> = ((2v+e0)^T Y (2v+e0) - Y00)/4 = q(-v-e0); Lemma A norm identity: OK")


def check_enumerator(trials=150):
    """Cross-check the exact enumerator against a box search whose box is provably
    sufficient: u^T Y u < Y00 implies |u_i| <= sqrt(Y00 * (Y^-1)_ii)."""
    tested = skipped = 0
    for _ in range(trials):
        N = random.randint(2, 4)
        d = N + random.randint(0, 1)
        while True:
            vecs = [[random.randint(-3, 3) for _ in range(d)] for _ in range(N)]
            G = gram(vecs)
            try:
                Gi = mat_inv(G)
                break
            except StopIteration:
                continue
        Y = [[x / G[0][0] for x in row] for row in G] if G[0][0] != 0 else None
        if Y is None:
            continue
        Yi = mat_inv(Y)
        rad = [isqrt(floor(Y[0][0] * Yi[i][i])) + 1 for i in range(N)]
        ranges = [range(-rad[0] - (rad[0] % 2 == 0), rad[0] + 2, 2)] + [range(-r - (r % 2), r + 1, 2) for r in rad[1:]]
        size = 1
        for rg in ranges:
            size *= len(rg)
        if size > 200000:
            skipped += 1
            continue
        tested += 1
        box = set()
        for u in product(*ranges):
            if qform(Y, u) < Y[0][0]:
                box.add(tuple((u[i] - (i == 0)) // 2 for i in range(N)))
        assert box == set(violators_pd(Y)), (Y, box)
    print(f"[enumerator] {tested} random positive definite Gram matrices (skipped {skipped} with box > 2e5 points): "
          f"exact enumeration = provably sufficient box search")


def run_family(label, instances, **kw):
    mism = []
    nyes = 0
    for a, s in instances:
        Y = Y_subset_sum(a, s, **kw)
        viol = set(violators_pd(Y))
        yes = bool(solutions(a, s))
        nyes += yes
        if (len(viol) > 0) != yes:
            mism.append((a, s, sorted(viol)[:3]))
        elif yes and viol != predicted_violators(a, s):
            mism.append((a, s, "violator set differs", sorted(viol)[:4]))
        if yes and not mism:
            n = len(a)
            g2 = F(n + 1) if kw.get("g2") is None else F(kw["g2"])
            h2 = g2 if kw.get("h2") is None else F(kw["h2"])
            mq = min(split_q(Y, v) for v in viol)
            assert mq == (n - g2) / (4 * g2 + 4 * h2), (a, s, mq)
    print(f"[{label}] {len(instances)} instances ({nyes} solvable): {len(mism)} mismatches")
    for m in mism[:4]:
        print("    e.g.", m)
    return mism


def instances_small():
    inst = []
    for n in (1, 2, 3):
        for a in product(range(1, 6), repeat=n):
            if list(a) != sorted(a):
                continue
            for s in range(0, sum(a) + 2):
                inst.append((a, s))
    for _ in range(60):
        a = tuple(random.randint(1, 9) for _ in range(4))
        inst.append((a, random.randint(0, sum(a) + 1)))
    return inst


if __name__ == "__main__":
    check_identities()
    check_enumerator()
    inst = instances_small()
    # The scout's eight instances (a = (3,5,7), gamma = 2, h = gamma), now with a complete search
    for s_ in (4, 8, 9, 10, 11, 13, 15, 16):
        Y = Y_subset_sum((3, 5, 7), s_, M=3, g2=4, h2=4)
        viol = violators_pd(Y)
        mq = min((split_q(Y, v) for v in viol), default=None)
        print(f"[scout instance] a=(3,5,7) s={s_:2d}: solvable={bool(solutions((3,5,7), s_))!s:5} "
              f"violated={bool(viol)!s:5} min violating q={mq} violators={sorted(viol)}")
    # Correct parameter ranges (expect 0 mismatches)
    run_family("M=3, g^2=n+1, h^2=g^2", inst)
    print("Further correct parameter choices (expect 0 mismatches):")
    for a_label, g2fun, h2fun, M in [
        ("M=3, g^2=n+8, h^2=g^2", lambda n: F(n + 8), lambda g2: g2, 3),
        ("M=3, g^2=n+1/7, h^2=g^2/8 (boundary 8h^2=|t|^2)", lambda n: n + F(1, 7), lambda g2: g2 / 8, 3),
        ("M=3, g^2=n+1, h^2=1000 g^2 (large h)", lambda n: F(n + 1), lambda g2: 1000 * g2, 3),
        ("M=2, g^2=n+4, h^2=g^2 (M^2 >= g^2-n suffices)", lambda n: F(n + 4), lambda g2: g2, 2),
        ("M=1, g^2=n+1, h^2=g^2 (M^2 >= g^2-n suffices)", lambda n: F(n + 1), lambda g2: g2, 1),
    ]:
        mism = []
        tot = 0
        for a, s in inst:
            n = len(a)
            g2 = g2fun(n)
            h2 = h2fun(g2)
            Y = Y_subset_sum(a, s, M=M, g2=g2, h2=h2)
            viol = set(violators_pd(Y))
            yes = bool(solutions(a, s))
            tot += 1
            if (len(viol) > 0) != yes or (yes and viol != predicted_violators(a, s)):
                mism.append((a, s))
        print(f"[{a_label}] {tot} instances: {len(mism)} mismatches {mism[:3]}")
    print("Negative controls (conditions violated; mismatches expected):")
    for a_label, g2fun, h2fun, M in [
        ("g^2=n (not > n)", lambda n: F(n), lambda g2: g2, 3),
        ("g^2=n+9 > n+8, M=3", lambda n: F(n + 9), lambda g2: g2, 3),
        ("M=2, g^2=n+8 (M^2 < g^2-n)", lambda n: F(n + 8), lambda g2: g2, 2),
        ("h^2 = g^2/9 (8h^2 < |t|^2)", lambda n: F(n + 1), lambda g2: g2 / 9, 3),
        ("h^2 = g^2/100", lambda n: F(n + 1), lambda g2: g2 / 100, 3),
    ]:
        mism = []
        for a, s in inst:
            n = len(a)
            g2 = g2fun(n)
            Y = Y_subset_sum(a, s, M=M, g2=g2, h2=h2fun(g2))
            viol = set(violators_pd(Y))
            yes = bool(solutions(a, s))
            if (len(viol) > 0) != yes:
                mism.append((a, s, yes, sorted(viol)[:1]))
        print(f"  [{a_label}] {len(mism)} mismatches, e.g. {mism[:2]}")
