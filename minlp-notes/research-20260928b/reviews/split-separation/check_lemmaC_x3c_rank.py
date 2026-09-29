"""Exact checks of Lemma C on random CLOSER instances, of a strongly NP-hard (X3C)
variant of Lemma B, and of the fixed-rank reduction (rank-r lattice CVP)."""
import random
from fractions import Fraction as F
from itertools import product, combinations
from math import gcd
from exact_lattice import (violators_pd, split_q, qform, enum_below, gram, mat_inv,
                           matmul, transpose)

random.seed(7)


def closer_truth(C, t):
    """Exact: exists z in Z^m with |t - Cz|^2 < |t|^2 ? (C columns = lattice basis)."""
    G = gram(C)
    w = [sum(F(ci) * F(ti) for ci, ti in zip(c, t)) for c in C]
    Gi = mat_inv(G)
    zstar = [sum(Gi[i][j] * w[j] for j in range(len(C))) for i in range(len(C))]
    R = sum(zstar[i] * w[i] for i in range(len(C)))  # |t|^2 - |t|^2 + w^T G^-1 w
    # |t-Cz|^2 - |t|^2 = (z-z*)^T G (z-z*) - w^T G^-1 w
    pts = enum_below(G, R, center=zstar)
    return [p for p in pts if any(p)]


def Y_lemmaC(C, t, h2):
    """b0 = (2t, 2h), b_j = (c_j, 0); Y = Gram/|b0|^2, parameterized by h^2."""
    m = len(C)
    N = m + 1
    G = [[F(0)] * N for _ in range(N)]
    tt = sum(F(x) ** 2 for x in t)
    G[0][0] = 4 * tt + 4 * F(h2)
    for j in range(m):
        G[0][1 + j] = G[1 + j][0] = 2 * sum(F(a) * F(b) for a, b in zip(t, C[j]))
        for k in range(m):
            G[1 + j][1 + k] = sum(F(a) * F(b) for a, b in zip(C[j], C[k]))
    return [[x / G[0][0] for x in row] for row in G]


def random_instance():
    d = random.randint(1, 3)
    m = random.randint(1, d)
    while True:
        C = [[random.randint(-4, 4) for _ in range(d)] for _ in range(m)]
        try:
            mat_inv(gram(C))
            break
        except StopIteration:
            pass
    t = [F(random.randint(-12, 12), random.choice([1, 2, 3, 4])) for _ in range(d)]
    if not any(t):
        t[0] = F(1, 3)
    return C, t


def check_lemmaC(trials=1500):
    stats = {"yes": 0, "no": 0}
    bad = {"l1": 0, "boundary": 0}
    neg = 0
    negex = None
    for _ in range(trials):
        C, t = random_instance()
        truth = bool(closer_truth(C, t))
        stats["yes" if truth else "no"] += 1
        tt = sum(x * x for x in t)
        h_l1 = sum(abs(x) for x in t)
        for key, h2 in (("l1", h_l1 ** 2), ("boundary", tt / 8)):
            Y = Y_lemmaC(C, t, h2)
            assert Y[0][0] == 1
            viol = violators_pd(Y)
            if bool(viol) != truth:
                bad[key] += 1
            # every violator has v0 in {0,-1}
            assert all(v[0] in (0, -1) for v in viol)
        # negative control: h too small
        Y = Y_lemmaC(C, t, tt / 80)
        if bool(violators_pd(Y)) != truth:
            neg += 1
            negex = negex or (C, t)
    print(f"[Lemma C] {trials} random CLOSER instances ({stats['yes']} yes / {stats['no']} no): "
          f"mismatches with h=|t|_1: {bad['l1']}, with 8h^2=|t|^2: {bad['boundary']}; "
          f"all violators have v0 in {{0,-1}}")
    print(f"  negative control h^2=|t|^2/80: {neg} mismatches, e.g. {negex}")
    # the 1-D example from the review: L = Z, t = 1/3
    C, t = [[1]], [F(1, 3)]
    print(f"  L=Z, t=1/3: CLOSER={bool(closer_truth(C, t))}; h^2=|t|^2/8 violated={bool(violators_pd(Y_lemmaC(C, t, F(1, 72))))}; "
          f"h^2=|t|^2/9 violated={bool(violators_pd(Y_lemmaC(C, t, F(1, 81))))}")


def Y_x3c(q, sets, M=3, g2=None, h2=None):
    """Exact cover by 3-sets: b_j = (M chi_{S_j}, 2 e_j, 0, 0), g = (M 1_U, 1_m, gamma, 0),
    b0 = (0, 0, -2 gamma, 2h). Integer Gram entries bounded by a polynomial in m and q."""
    m = len(sets)
    g2 = F(m + 1) if g2 is None else F(g2)
    h2 = g2 if h2 is None else F(h2)
    N = m + 2
    G = [[F(0)] * N for _ in range(N)]
    G[0][0] = 4 * g2 + 4 * h2
    G[0][m + 1] = G[m + 1][0] = -2 * g2
    for i in range(m):
        for j in range(m):
            G[1 + i][1 + j] = F(M * M * len(set(sets[i]) & set(sets[j])) + (4 if i == j else 0))
        G[1 + i][m + 1] = G[m + 1][1 + i] = F(M * M * 3 + 2)
    G[m + 1][m + 1] = F(M * M * 3 * q + m) + g2
    return [[x / G[0][0] for x in row] for row in G], G


def has_exact_cover(q, sets):
    U = set(range(3 * q))
    for r in range(len(sets) + 1):
        for comb in combinations(range(len(sets)), r):
            cov = [e for i in comb for e in sets[i]]
            if len(cov) == len(set(cov)) and set(cov) == U:
                return True
    return False


def check_x3c(trials=400):
    mism = 0
    nyes = 0
    maxnum = 0
    for _ in range(trials):
        q = random.choice([2, 3])
        m = random.randint(q, 7)
        U = list(range(3 * q))
        sets = [tuple(sorted(random.sample(U, 3))) for _ in range(m)]
        Y, G = Y_x3c(q, sets)
        truth = has_exact_cover(q, sets)
        nyes += truth
        maxnum = max(maxnum, max(abs(x) for row in G for x in row))
        if bool(violators_pd(Y)) != truth:
            mism += 1
    print(f"[X3C variant] {trials} random instances ({nyes} with exact cover): {mism} mismatches; "
          f"largest |Gram entry| = {maxnum} (polynomial in m, q -> strong NP-hardness)")


def check_rank(trials=300):
    """Y = P^T G P with integer P (r x N) of rank r, G rational PD. Reduced test: CVP in
    Lambda = P Z^N under form G with target -w0/2. Compared with a box search in Z^N."""
    import sympy
    agree = 0
    found = 0
    for _ in range(trials):
        r = random.choice([1, 2])
        N = random.randint(r + 1, 4)
        while True:
            P = [[random.randint(-3, 3) for _ in range(N)] for _ in range(r)]
            if sympy.Matrix(P).rank() == r and any(P[i][0] for i in range(r)):
                break
        A = [[F(random.randint(-3, 3), random.randint(1, 2)) for _ in range(r)] for _ in range(r)]
        G = matmul(transpose(A), A)
        for i in range(r):
            G[i][i] += F(1, random.randint(1, 3))
        w0 = [F(P[i][0]) for i in range(r)]
        s = sum(w0[i] * G[i][j] * w0[j] for i in range(r) for j in range(r))
        G = [[x / s for x in row] for row in G]  # makes Y00 = 1
        Y = matmul(matmul(transpose([[F(x) for x in row] for row in P]), G), [[F(x) for x in row] for row in P])
        assert Y[0][0] == 1
        # basis of Lambda = P Z^N via Hermite normal form of the r x N matrix
        from sympy.matrices.normalforms import hermite_normal_form
        H = hermite_normal_form(sympy.Matrix(P))
        assert H.shape == (r, r)
        # H's columns generate P Z^N: P = H * (integer matrix), and |det H| = gcd of r x r minors
        X = H.inv() * sympy.Matrix(P)
        assert all(x.is_integer for x in X)
        minors = [sympy.Matrix(P).extract(list(range(r)), list(c)).det() for c in combinations(range(N), r)]
        gm = 0
        for x in minors:
            gm = gcd(gm, abs(int(x)))
        assert abs(H.det()) == gm
        W = [[int(H[i, j]) for j in range(H.shape[1])] for i in range(r)]  # columns = basis
        k = len(W[0])
        # (Wz + w0/2)^T G (Wz + w0/2) < w0^T G w0 / 4, enumerated in z
        GW = matmul(matmul(transpose([[F(x) for x in row] for row in W]), G), [[F(x) for x in row] for row in W])
        # center z* solves W z* = -w0/2 (W square, invertible)
        Wi = mat_inv([[F(x) for x in row] for row in W])
        zstar = [sum(Wi[i][j] * (-w0[j] / 2) for j in range(r)) for i in range(k)]
        reduced = bool(enum_below(GW, F(1, 4), center=zstar))  # w0^T G w0 = 1
        # direct box search on v in Z^N
        box = any(split_q(Y, v) < 0 for v in product(range(-4, 5), repeat=N))
        # rank 1 closed form: violated iff |p0| >= 2 gcd(p)
        if r == 1:
            p = P[0]
            gg = 0
            for x in p:
                gg = gcd(gg, abs(x))
            closed = abs(p[0]) >= 2 * gg
            assert closed == reduced, (P, closed, reduced)
        if box:
            assert reduced, (P, G)
        found += reduced
        agree += (reduced == box)
    print(f"[fixed rank] {trials} random PSD Y of rank 1-2: rank-r CVP decision agrees with box search in "
          f"{agree} cases ({found} violated); box-found violations always found by the reduced test; "
          f"rank-1 closed form |p0| >= 2 gcd(p) confirmed")


def check_factorization(trials=100):
    """For PSD rational Y of rank r: P = r independent rows of Y, G = (PP^T)^-1 P Y P^T (PP^T)^-1."""
    import sympy
    for _ in range(trials):
        N = random.randint(2, 5)
        r = random.randint(1, N - 1)
        Bm = [[F(random.randint(-3, 3), random.randint(1, 3)) for _ in range(N)] for _ in range(r)]
        Y = matmul(transpose(Bm), Bm)
        rk = sympy.Matrix(Y).rank()
        if rk == 0:  # Y = 0 cannot have Y00 = 1
            continue
        rows = []
        for i in range(N):
            cand = rows + [Y[i]]
            if sympy.Matrix(cand).rank() == len(cand):
                rows = cand
        P = rows
        assert len(P) == rk
        PPt = matmul(P, transpose(P))
        Pi = mat_inv(PPt)
        G = matmul(matmul(Pi, matmul(matmul(P, Y), transpose(P))), Pi)
        assert matmul(matmul(transpose(P), G), P) == Y
        assert sympy.Matrix(G).is_positive_definite
    print(f"[fixed rank] {trials} random rational PSD Y: Y = P^T G P with G rational positive definite: OK")


if __name__ == "__main__":
    check_lemmaC()
    check_x3c()
    check_factorization()
    check_rank()
