"""Reviewer's independent numerical and exact checks for the ratio-bound note (review r1).
Written from the note's statements; does not import the stream's code.

Sections:
  1. Theorem A and Corollary A': random corners (N = 3, 5), own z_K (face enumeration + bisection),
     own cylinder step formula (checked against bisection on the definition), rho_par >= f(D) and the
     Corollary A' constant when the margin hypothesis holds.
  2. Lemma S and Theorem S: SCIP's Case-4 set implemented from the piecewise phi_lambda description
     (scip-rule-fidelity note, Section 1.3, kappa = 0), compared with the upward closure of
     {4N^2 q >= V(s - sbar)^2, trace >= 0}; Theorem S bound checked.
  3. Theorem B2(2): exact check of the explicit X.
  4. Proposition S3: exact rational checks at Pythagorean u (SCIP step via phi_lambda, z_K identity,
     orbit set slacks).
  5. Theorem B(2) cond(P), Theorem B3(1) z_K bounds.
  6. Proposition C3: interval disjointness on a fine grid of t, H_cyl >= 1 - 4d, min q over T*.
usage: python3 indep_checks.py SEED
"""
import sys
import itertools
import numpy as np
from fractions import Fraction as Fr

rng = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
ALL = {}


def q(s):
    return s[2] - s[0] * s[1]


# ---------- z_K by face enumeration of min q over a simplex ----------
def min_q_simplex(V):
    """min of q over conv(V) (V: list of 3-vectors) by enumerating faces and stationary points."""
    best = min(q(v) for v in V)
    n = len(V)
    for k in range(2, n + 1):
        for S in itertools.combinations(range(n), k):
            v0 = V[S[0]]
            E = np.array([V[i] - v0 for i in S[1:]]).T  # 3 x (k-1)
            # q(v0 + E a) = q(v0) + g^T E a + a^T H a with H = E^T Q E, Q = -[[0,1/2,0],[1/2,0,0],[0,0,0]]
            g = np.array([-v0[1], -v0[0], 1.0])
            Q = -np.array([[0, .5, 0], [.5, 0, 0], [0, 0, 0]])
            H = E.T @ Q @ E
            b = E.T @ g
            try:
                a = np.linalg.solve(2 * H, -b)
            except np.linalg.LinAlgError:
                continue
            if np.all(a >= -1e-12) and a.sum() <= 1 + 1e-12:
                best = min(best, q(v0 + E @ a))
    return best


def zK(sbar, P, c):
    """corner bound (finite case) by bisection on z with exact-ish face enumeration."""
    lo, hi = 0.0, 1.0
    while min_q_simplex([sbar] + [sbar + hi / c[j] * P[:, j] for j in range(P.shape[1])]) > 0:
        hi *= 2
        if hi > 1e8:
            return np.inf
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if min_q_simplex([sbar] + [sbar + m / c[j] * P[:, j] for j in range(P.shape[1])]) > 0:
            lo = m
        else:
            hi = m
    return hi


def cyl_step(sbar, p, t):
    qb = q(sbar)
    g = np.array([-sbar[1], -sbar[0], 1.0]) @ p
    b2 = (t * p[0] + p[1] / t) ** 2
    if b2 == 0:
        return np.inf if g >= 0 else qb / (-g)
    return 2 * qb / (np.sqrt(g * g + qb * b2) - g)


def in_cyl(s, sbar, t):
    return q(s) - (t * (s[0] - sbar[0]) - (s[1] - sbar[1]) / t) ** 2 / 4 >= 0


def rho_par(sbar, Pt):
    f = lambda lt: min(cyl_step(sbar, Pt[:, j], np.exp(lt)) for j in range(Pt.shape[1]))
    grid = np.linspace(-12, 12, 2401)
    vals = [f(x) for x in grid]
    k = int(np.argmax(vals))
    a, b = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    gr = (np.sqrt(5) - 1) / 2
    for _ in range(100):
        m1, m2 = b - gr * (b - a), a + gr * (b - a)
        if f(m1) >= f(m2):
            b = m2
        else:
            a = m1
    return max(max(vals), f(0.5 * (a + b)))


def fD(D):
    return 1 / (1 + 2 * D * D) if D <= 1 else 1 / ((1 + np.sqrt(2)) * D)


def rel_disc(sbar, p):
    A = -p[0] * p[1]
    B = np.array([-sbar[1], -sbar[0], 1.0]) @ p
    g0 = q(sbar)
    return (B * B - 4 * A * g0) / (B * B + abs(4 * A * g0))


def random_corner(N):
    while True:
        sbar = rng.normal(size=3) * rng.choice([0.3, 1, 3])
        sbar[2] = sbar[0] * sbar[1] + abs(rng.normal()) * rng.choice([1e-3, 1e-2, 0.1, 1])
        P = rng.normal(size=(3, N))
        c = rng.uniform(0.2, 2, size=N)
        z = zK(sbar, P, c)
        if np.isfinite(z) and z > 1e-6:
            return sbar, P, c, z


def section1(n=120):
    bad_formula = 0
    viol = 0
    viol_cor = 0
    ncor = 0
    minratio = np.inf
    for it in range(n):
        N = 3 if it % 2 == 0 else 5
        sbar, P, c, z = random_corner(N)
        Pt = P * (z / c)
        X, Y = np.max(np.abs(Pt[0])), np.max(np.abs(Pt[1]))
        D = np.sqrt(X * Y / q(sbar))
        # formula (1) vs bisection on the definition
        t = np.exp(rng.normal())
        for j in range(N):
            a = cyl_step(sbar, Pt[:, j], t)
            if np.isfinite(a):
                lo, hi = 0.0, a * 1.5 + 1
                for _ in range(100):
                    m = 0.5 * (lo + hi)
                    if in_cyl(sbar + m * Pt[:, j], sbar, t):
                        lo = m
                    else:
                        hi = m
                if abs(lo - a) > 1e-7 * max(1, a):
                    bad_formula += 1
        rp = rho_par(sbar, Pt)
        if rp < fD(D) * (1 - 1e-9):
            viol += 1
        minratio = min(minratio, rp / fD(D))
        # Corollary A': margin of rays that miss S and along which q initially decreases
        mus = []
        for j in range(N):
            p = Pt[:, j]
            A = -p[0] * p[1]
            B = np.array([-sbar[1], -sbar[0], 1.0]) @ p
            g0 = q(sbar)
            misses = (A > 0 and B * B < 4 * A * g0) or (A >= 0 and B >= 0)
            if misses and B < 0:
                mus.append(-rel_disc(sbar, p))
        mu = min(mus) if mus else 1.0
        if mu > 0 and D >= 1:
            ncor += 1
            gam = np.sqrt((1 - mu) / (1 + mu))
            gD = max(gam, 1 / D)
            bound = 1 / (D * (gD + np.sqrt(1 + gD * gD)))
            if rp < bound * (1 - 1e-9):
                viol_cor += 1
    ok = bad_formula == 0 and viol == 0 and viol_cor == 0
    print('S1 Theorem A: %d corners, formula (1) mismatches %d, violations of rho_par >= f(D): %d, '
          'min rho_par/f(D) = %.4f; Corollary A\' applicable %d, violations %d -> %s'
          % (n, bad_formula, viol, minratio, ncor, viol_cor, 'PASS' if ok else 'FAIL'), flush=True)
    ALL['S1'] = ok


# ---------- SCIP Case 4 (kappa = 0) from the piecewise description ----------
def scip_member(s, sbar):
    xh = lambda u: np.array([(u[0] - u[1]) / 2, (u[2] + 1) / 2])
    yh = lambda u: np.array([(u[0] + u[1]) / 2, (u[2] - 1) / 2])
    lam = xh(sbar) / np.linalg.norm(xh(sbar))
    le = lam[1]
    y = yh(s)
    ny = np.linalg.norm(y)
    if y[1] <= le * ny:
        phi = ny
    else:
        phi = np.sqrt(max((1 - le * le) * (ny * ny - y[1] ** 2), 0)) + le * y[1]
    return phi <= lam @ xh(s)


def scip_member_uncompleted(s, sbar):
    xh = lambda u: np.array([(u[0] - u[1]) / 2, (u[2] + 1) / 2])
    yh = lambda u: np.array([(u[0] + u[1]) / 2, (u[2] - 1) / 2])
    lam = xh(sbar) / np.linalg.norm(xh(sbar))
    return np.linalg.norm(yh(s)) <= lam @ xh(s)


def lemmaS_member_up(s, sbar):
    a = sbar[0] - sbar[1]
    b = sbar[2] + 1
    N2 = a * a + b * b
    N = np.sqrt(N2)
    V0 = a * (s[2] - sbar[2]) - b * ((s[0] - s[1]) - a)
    qq = q(s)
    # tau >= 0 with 4N^2 (q - tau) >= (V0 - a tau)^2 and trace(tau) = (b (s_w - tau + 1) + a (s_x - s_y))/N >= 0
    A2, B1, C0 = a * a, 4 * N2 - 2 * a * V0, V0 * V0 - 4 * N2 * qq
    if A2 < 1e-300:
        if B1 <= 0:
            taus = [0.0] if C0 <= 0 else []
        else:
            taus = [0.0] if C0 <= 0 else []
    else:
        disc = B1 * B1 - 4 * A2 * C0
        if disc < 0:
            return False
        r1 = (-B1 - np.sqrt(disc)) / (2 * A2)
        r2 = (-B1 + np.sqrt(disc)) / (2 * A2)
        if r2 < 0:
            return False
        taus = [max(r1, 0.0)]
    if not taus:
        return False
    tau = taus[0]
    return b * (s[2] - tau + 1) + a * (s[0] - s[1]) >= -1e-12


def step_by_bisection(member, sbar, p, cap=1e7):
    if not member(sbar, sbar):
        return np.nan
    hi = 1.0
    while member(sbar + hi * p, sbar):
        hi *= 2
        if hi > cap:
            return np.inf
    lo = 0.0
    # membership along a ray from an interior point of a convex set is an interval
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if member(sbar + m * p, sbar):
            lo = m
        else:
            hi = m
    return lo


def section2(n=150):
    mism = 0
    mism_unc = 0
    viol = 0
    minr = np.inf
    for it in range(n):
        sbar, P, c, z = random_corner(3)
        Pt = P * (z / c)
        st_phi = [step_by_bisection(scip_member, sbar, Pt[:, j]) for j in range(3)]
        st_up = [step_by_bisection(lemmaS_member_up, sbar, Pt[:, j]) for j in range(3)]
        # Lemma S closed form for the uncompleted set: first s>0 with 4N^2 q(sbar+sp) = s^2 V(p)^2
        a = sbar[0] - sbar[1]
        b = sbar[2] + 1
        N2 = a * a + b * b
        st_cf = []
        for j in range(3):
            p = Pt[:, j]
            V = a * p[2] - b * (p[0] - p[1])
            g = np.array([-sbar[1], -sbar[0], 1.0]) @ p
            # 4N^2 (qbar + g s - p_x p_y s^2) - V^2 s^2 = 0
            cq = [-4 * N2 * p[0] * p[1] - V * V, 4 * N2 * g, 4 * N2 * q(sbar)]
            rts = [r.real for r in np.roots(cq) if abs(r.imag) < 1e-12 and r.real > 0]
            st_cf.append(min(rts) if rts else np.inf)
        st_unc = [step_by_bisection(scip_member_uncompleted, sbar, Pt[:, j]) for j in range(3)]
        for x1, x2 in zip(st_phi, st_up):
            if not (np.isinf(x1) and np.isinf(x2)) and abs(x1 - x2) > 1e-6 * max(1, abs(x1)):
                mism += 1
        for x1, x2 in zip(st_unc, st_cf):
            if not (np.isinf(x1) and np.isinf(x2)) and abs(x1 - x2) > 1e-6 * max(1, abs(x1)):
                mism_unc += 1
        ratio = min(1.0, min(st_phi))
        X, Y = np.max(np.abs(Pt[0])), np.max(np.abs(Pt[1]))
        D = np.sqrt(X * Y / q(sbar))
        kap = np.linalg.cond(Pt)
        b1 = min(0.5, 1 / (2 * D), np.sqrt(q(sbar)) / max(np.hypot(Pt[0, j] - Pt[1, j], Pt[2, j]) for j in range(3)))
        b2 = min(0.5, 1 / (np.sqrt(6) * kap * D))
        if ratio < b1 * (1 - 1e-7) or b1 < b2 * (1 - 1e-12):
            viol += 1
        minr = min(minr, ratio / b1)
    ok = mism == 0 and mism_unc == 0 and viol == 0
    print('S2 Lemma S / Theorem S: %d corners; phi-lambda Case-4 steps vs upward closure of Lemma S set: %d mismatches; '
          'uncompleted MS set vs closed form: %d mismatches; Theorem S violations %d; min ratio/first bound %.4f -> %s'
          % (n, mism, mism_unc, viol, minr, 'PASS' if ok else 'FAIL'), flush=True)
    ALL['S2'] = ok


def symXN(X, N):
    a = X[0][0] * N[0][0] + X[0][1] * N[1][0]
    b = X[0][0] * N[0][1] + X[0][1] * N[1][1]
    c = X[1][0] * N[0][0] + X[1][1] * N[1][0]
    d = X[1][0] * N[0][1] + X[1][1] * N[1][1]
    return a, (b + c) / 2, d


def psd(S, strict=False):
    a, b, d = S
    if strict:
        return a > 0 and a * d - b * b > 0
    return a >= 0 and d >= 0 and a * d - b * b >= 0


def Mx(s):
    return ((s[2], s[0]), (s[1], Fr(1)))


def section3():
    X = ((Fr(1), Fr(-1678587, 10 ** 6)), (Fr(1463, 200000), Fr(174583, 250000)))
    rho = Fr(273, 2)
    h0 = Fr(255361, 8)
    ok = psd(symXN(X, Mx((Fr(0), Fr(0), Fr(1)))), strict=True)
    ok &= psd(symXN(X, Mx((rho, -rho, Fr(1)))))
    ok &= psd(symXN(X, Mx((rho, -2 * rho, Fr(1)))))
    ok &= psd(symXN(X, Mx((rho, rho, h0))))
    detX = X[0][0] * X[1][1] - X[0][1] * X[1][0]
    eps0 = (rho / (h0 - 1)) ** 2
    ok &= detX > 0 and eps0 == Fr(24336, 1330717441)
    # midpoints and the segment to (rho, rho, h) for h >= h0 are implied by convexity; also check a point
    # slightly above h0 and P3 for eps = eps0 exactly: 1 + rho/sqrt(eps0) = h0
    print('S3 Theorem B2(2): sym(X) > 0, P1, P2, (rho, rho, h0) in C_X, eps0 = %s -> %s' % (eps0, 'PASS' if ok else 'FAIL'))
    ALL['S3'] = ok


def section4():
    ok = True
    for m in (3, 7, 20):
        u = Fr(m * m + 1, 2 * m)
        v = Fr(m * m - 1, 2 * m)
        for D in (Fr(1, 2), Fr(1), v):
            sbar = (u, -u, Fr(-1))
            P = [(v * D, Fr(0), Fr(0)), (Fr(0), -v * D, Fr(0)), (Fr(0), Fr(0), -v * v)]
            # q along ray 3 and the SCIP (phi-lambda) set: lambda = (1, 0) exactly since wbar + 1 = 0
            s3 = Fr(2) / (u + 1)
            pt = tuple(sbar[i] + s3 * P[2][i] for i in range(3))
            # exact: on ray 3, x+y = 0, yhat = (0, (w-1)/2), xhat = (u, 0): phi = |w-1|/2 (yhat_e <= 0 since w < 1)
            w = pt[2]
            ok &= (w < 1) and (abs(w - 1) / 2 == u)  # boundary point exactly at s3
            # orbit set C_{1,beta} in centred coordinates contains the vertices
            beta_f = float(D) / (float(u) * float(D) + float(v))
            for vert in [sbar] + [tuple(sbar[i] + P[j][i] for i in range(3)) for j in range(3)]:
                x, y, ww = (float(vert[0] - u), float(vert[1] + u), float(vert[2] + u * vert[0] - u * vert[1] - u * u))
                slack = 4 * (ww - x * y) - (x - y - beta_f * ww) ** 2
                tr = ww + beta_f * x + 1
                ok &= slack >= -1e-9 * (1 + abs(ww)) and tr > 0
            # z_K identity at random lambda
            for _ in range(5):
                lam = [Fr(int(rng.integers(0, 50)), 17) for _ in range(3)]
                pt = tuple(sbar[i] + sum(lam[j] * P[j][i] for j in range(3)) for i in range(3))
                lhs = pt[2] - pt[0] * pt[1]
                rhs = v * v * (1 - lam[2]) + u * v * D * (lam[0] + lam[1]) + v * v * D * D * lam[0] * lam[1]
                ok &= lhs == rhs
            # float cross-check of SCIP steps by bisection with the phi-lambda set
            sb = np.array([float(t) for t in sbar])
            Pm = np.array([[float(t) for t in p] for p in P]).T
            st = [step_by_bisection(scip_member, sb, Pm[:, j]) for j in range(3)]
            ok &= np.isinf(st[0]) and np.isinf(st[1]) and abs(st[2] - float(s3)) < 1e-9
    print('S4 Proposition S3: exact boundary point on ray 3, z_K identity, orbit-set slacks, phi-lambda steps -> %s'
          % ('PASS' if ok else 'FAIL'))
    ALL['S4'] = ok


def section5():
    P = np.array([[1, 1, 1], [-1, -2, 1], [0, 0, 1]], dtype=float)
    cP = np.linalg.cond(P)
    ok = abs(cP - 12.01) < 0.01
    msg = 'cond(P) = %.4f' % cP
    for eta, k in ((1e-3, 4.0), (1e-2, 4.0), (1e-3, 2.25), (1e-3, 1.96)):
        for L in (0.5, 3.0, 30.0):
            sbar = np.array([0, 0, 1.0])
            P3 = np.array([[1, 1, 1], [-1, -k, 1], [-2 * (1 - eta), -2 * np.sqrt(k) * (1 - eta), L]])
            z = zK(sbar, P3, np.ones(3))
            ok &= L < z < L + 1 / L
    print('S5 Theorem B(2) %s; Theorem B3(1) L < z_K < L + 1/L on 12 cases -> %s' % (msg, 'PASS' if ok else 'FAIL'))
    ALL['S5'] = ok


def section6():
    ok = True
    for d in (1e-2, 1e-3, 1e-4):
        sbar = np.array([1.5, -0.5, 0.25 - d])
        v2 = np.array([0.5, 1.5, 1 - d])
        v3 = np.array([3.0, 1.0, 4 - d])
        verts = {'s': sbar, '2': v2, '3': v3}
        H = min(4 * v[2] / (v[0] + v[1]) ** 2 for v in verts.values())
        ok &= H >= 1 - 4 * d - 1e-12

        def iv(v, al):
            qq = v[2] - v[0] * v[1]
            c = al * v[0] - v[1]
            r = 2 * np.sqrt(al * qq)
            return (c - r) / v[2], (c + r) / v[2]
        gaps = []
        for t in np.exp(np.linspace(-8, 8, 40001)):
            I = [iv(v, t * t) for v in verts.values()]
            gaps.append(max(i[0] for i in I) - min(i[1] for i in I))
        ok &= min(gaps) > 0
        # min q over T* (t* = 0 is a vertex); expect min 0 attained only at t*
        V = [np.zeros(3), sbar, v2, v3]
        mq = min_q_simplex(V)
        # also sample: q > 0 away from t*
        W = rng.dirichlet(np.ones(4), size=200000)
        pts = W @ np.array(V)
        qq = pts[:, 2] - pts[:, 0] * pts[:, 1]
        far = W[:, 0] < 0.999
        ok &= abs(mq) < 1e-12 and qq[far].min() > 0
        print('   d = %g: H_cyl(t=1) = %.6f, min interval gap over t = %.3e, min_T* q = %.2e, min sampled q away from t* = %.3e'
              % (d, H, min(gaps), mq, qq[far].min()))
    print('S6 Proposition C3 (numerical) -> %s' % ('PASS' if ok else 'FAIL'))
    ALL['S6'] = ok


if __name__ == '__main__':
    section3()
    section4()
    section5()
    section6()
    section1()
    section2()
    print('ALL PASS' if all(ALL.values()) else 'SOME FAIL', ALL)
