"""Lane M1: exact randomized check of the closure theorem on finite domains.

A finite D is compact and every function on it is continuous, so the
closure theorem of development/M1.md applies.  For random rational data with
  * inequality rows   g(Sw) + A w <= b   (A also acts on block coordinates),
  * an equality row   h(Sw) + C w  = e,
  * an epigraph-style row with coefficient -1 on a free variable t,
we compare, with exact rational LPs (M1_exactlp, Bland's rule):
  (i)  membership of w in R = {w : T(w) in K + ({0} x R^m_+ x {0})};
  (ii) the maximum violation of a cut over the normalized direction box
       -1 <= a <= 1, 0 <= lambda <= 1, -1 <= mu <= 1.
The theorem predicts: w in R  <=>  maximum violation <= 0.  Each violated
cut found in (ii) is also re-checked exactly for validity on the graph.
Run: code/minlp_solver_lab/.venv/bin/python paper-certified-support-cuts/verification/M1_closure_random.py
"""
import os
import random
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M1_exactlp import solve_lp  # noqa: E402

random.seed(7)


def rnd(lo=-3, hi=3, den=4):
    return Fr(random.randint(lo * den, hi * den), den)


def instance(npts=5, d=2, N=4, m=2, r=1):
    pts = [[rnd(0, 2) for _ in range(d)] for _ in range(npts)]
    gvals = [[rnd() + (p[0] * p[1] if i == 0 else -p[0] ** 2) for i in range(m)] for p in pts]
    hvals = [[p[0] ** 2 - p[1] + rnd(-1, 1)] for p in pts]
    A = [[rnd() for _ in range(N)] for _ in range(m)]
    A[0][N - 1] = Fr(-1)          # row 0: epigraph row in the free t = w[N-1]
    C = [[rnd() for _ in range(N)] for _ in range(r)]
    return pts, gvals, hvals, A, C


def T(w, A, C, b, e, d):
    x = list(w[:d])
    q = [b[i] - sum(A[i][j] * w[j] for j in range(len(w))) for i in range(len(b))]
    s = [e[k] - sum(C[k][j] * w[j] for j in range(len(w))) for k in range(len(e))]
    return x, q, s


def member(w, data, d):
    pts, gvals, hvals, A, C, b, e = data
    x, q, s = T(w, A, C, b, e, d)
    n = len(pts)
    A_eq = [[Fr(1)] * n] + [[pts[j][i] for j in range(n)] for i in range(d)] \
        + [[hvals[j][k] for j in range(n)] for k in range(len(s))]
    b_eq = [Fr(1)] + x + s
    A_ub = [[gvals[j][i] for j in range(n)] for i in range(len(q))]
    st, _, th = solve_lp([0] * n, A_ub, q, A_eq, b_eq, [(Fr(0), None)] * n)
    if st == "optimal":
        # exact re-check of the certificate of membership
        assert all(t >= 0 for t in th) and sum(th) == 1
        for i in range(d):
            assert sum(th[j] * pts[j][i] for j in range(n)) == x[i]
        for k in range(len(s)):
            assert sum(th[j] * hvals[j][k] for j in range(n)) == s[k]
        for i in range(len(q)):
            assert sum(th[j] * gvals[j][i] for j in range(n)) <= q[i]
        return True
    assert st == "infeasible"
    return False


def max_violation(w, data, d):
    """max phi - c.T(w) over normalized c, with phi <= c.G_j for all j."""
    pts, gvals, hvals, A, C, b, e = data
    x, q, s = T(w, A, C, b, e, d)
    m, r, n = len(q), len(s), len(pts)
    nv = d + m + r + 1                    # (a, lam, mu, phi)
    cobj = [Fr(0)] * nv                   # minimize c.T(w) - phi
    for i in range(d):
        cobj[i] = x[i]
    for i in range(m):
        cobj[d + i] = q[i]
    for k in range(r):
        cobj[d + m + k] = s[k]
    cobj[-1] = Fr(-1)
    A_ub = []
    for j in range(n):                    # phi - c.G_j <= 0
        row = [-pts[j][i] for i in range(d)] + [-gvals[j][i] for i in range(m)] \
            + [-hvals[j][k] for k in range(r)] + [Fr(1)]
        A_ub.append(row)
    bounds = [(Fr(-1), Fr(1))] * d + [(Fr(0), Fr(1))] * m + [(Fr(-1), Fr(1))] * r + [(None, None)]
    st, val, sol = solve_lp(cobj, A_ub, [Fr(0)] * n, (), (), bounds)
    assert st == "optimal"
    viol = -val
    if viol > 0:                          # exact re-check of the violated cut
        a, lam, mu = sol[:d], sol[d:d + m], sol[d + m:d + m + r]
        phi = min(sum(a[i] * p[i] for i in range(d)) + sum(lam[i] * gvals[j][i] for i in range(m))
                  + sum(mu[k] * hvals[j][k] for k in range(r)) for j, p in enumerate(pts))
        # cut in original variables: (S^T a - A^T lam - C^T mu).w >= phi - lam.b - mu.e
        N = len(w)
        coef = [(a[j] if j < d else Fr(0)) - sum(lam[i] * A[i][j] for i in range(m))
                - sum(mu[k] * C[k][j] for k in range(r)) for j in range(N)]
        rhs = phi - sum(lam[i] * b[i] for i in range(m)) - sum(mu[k] * e[k] for k in range(r))
        assert sum(coef[j] * w[j] for j in range(N)) - rhs == -viol
    return viol


def main(trials=60):
    d, N, m, r = 2, 4, 2, 1
    stats = {"in_R": 0, "out_R": 0}
    for t in range(trials):
        pts, gvals, hvals, A, C = instance(d=d, N=N, m=m, r=r)
        # build b, e so that a constructed w0 lies in R (some slacks zero)
        wts = [Fr(random.randint(0, 4)) for _ in pts]
        if sum(wts) == 0:
            wts[0] = Fr(1)
        wts = [v / sum(wts) for v in wts]
        x0 = [sum(wts[j] * pts[j][i] for j in range(len(pts))) for i in range(d)]
        y0 = [sum(wts[j] * gvals[j][i] for j in range(len(pts))) for i in range(m)]
        h0 = [sum(wts[j] * hvals[j][k] for j in range(len(pts))) for k in range(r)]
        w0 = x0 + [rnd(-2, 2) for _ in range(N - d)]
        slack = [Fr(random.randint(0, 1), 4) for _ in range(m)]
        b = [y0[i] + sum(A[i][j] * w0[j] for j in range(N)) + slack[i] for i in range(m)]
        e = [h0[k] + sum(C[k][j] * w0[j] for j in range(N)) for k in range(r)]
        data = (pts, gvals, hvals, A, C, b, e)
        cands = [w0]
        for _ in range(3):                # small perturbations of w0
            cands.append([w0[j] + Fr(random.randint(-2, 2), 16) for j in range(N)])
        cands.append([rnd(0, 2) for _ in range(d)] + [rnd(-4, 4) for _ in range(N - d)])
        for k, w in enumerate(cands):
            inside = member(w, data, d)
            viol = max_violation(w, data, d)
            assert inside == (viol <= 0), (t, w, inside, viol)
            if k == 0:
                assert inside
            stats["in_R" if inside else "out_R"] += 1
    print("closure theorem on finite D: membership <=> no violated cut;", stats)


if __name__ == "__main__":
    main()
    print("M1_closure_random: all checks passed")


# ---------------------------------------------------------------------------
# Free-remainder proposition: if the remainder block M = [A_z; C_z] has full
# row rank and z is unconstrained, then R_D = conv(Sigma_D), where
# Sigma_D = {(x,z): x in D, g(x) + A w <= b, h(x) + C w = e}.
# conv(Sigma_D) for finite D is tested with Balas' disjunctive LP (all pieces
# share the recession cone {A_z zeta <= 0, C_z zeta = 0}, so it is exact).

def member_conv_sigma(w, data, d):
    pts, gvals, hvals, A, C, b, e = data
    n, N, m, r = len(pts), len(w), len(b), len(e)
    p = N - d
    # variables: theta_j (n), zeta_{j,k} (n*p, free)
    nv = n + n * p
    th = lambda j: j
    ze = lambda j, k: n + j * p + k
    A_eq, b_eq, A_ub, b_ub = [], [], [], []
    row = [Fr(0)] * nv
    for j in range(n):
        row[th(j)] = Fr(1)
    A_eq.append(row); b_eq.append(Fr(1))
    for i in range(d):
        row = [Fr(0)] * nv
        for j in range(n):
            row[th(j)] = pts[j][i]
        A_eq.append(row); b_eq.append(w[i])
    for k in range(p):
        row = [Fr(0)] * nv
        for j in range(n):
            row[ze(j, k)] = Fr(1)
        A_eq.append(row); b_eq.append(w[d + k])
    for j in range(n):
        for i in range(m):    # theta_j (g_j + A_x u_j - b_i) + A_z zeta_j <= 0
            row = [Fr(0)] * nv
            row[th(j)] = gvals[j][i] + sum(A[i][q] * pts[j][q] for q in range(d)) - b[i]
            for k in range(p):
                row[ze(j, k)] = A[i][d + k]
            A_ub.append(row); b_ub.append(Fr(0))
        for kk in range(r):
            row = [Fr(0)] * nv
            row[th(j)] = hvals[j][kk] + sum(C[kk][q] * pts[j][q] for q in range(d)) - e[kk]
            for k in range(p):
                row[ze(j, k)] = C[kk][d + k]
            A_eq.append(row); b_eq.append(Fr(0))
    bounds = [(Fr(0), None)] * n + [(None, None)] * (n * p)
    st, _, _ = solve_lp([0] * nv, A_ub, b_ub, A_eq, b_eq, bounds)
    return st == "optimal"


def free_remainder_test(trials=25):
    d, m, r = 2, 2, 1
    gaps = {"full_rank": 0, "deficient": 0}
    tested = {"full_rank": 0, "deficient": 0}
    for t in range(trials):
        for kind, N in (("full_rank", d + m + r), ("deficient", d + m + r - 1)):
            pts, gvals, hvals, A, C = instance(d=d, N=N, m=m, r=r)
            A[0][N - 1] = Fr(-1)
            wts = [Fr(random.randint(0, 4)) for _ in pts]
            if sum(wts) == 0:
                wts[0] = Fr(1)
            wts = [v / sum(wts) for v in wts]
            x0 = [sum(wts[j] * pts[j][i] for j in range(len(pts))) for i in range(d)]
            y0 = [sum(wts[j] * gvals[j][i] for j in range(len(pts))) for i in range(m)]
            h0 = [sum(wts[j] * hvals[j][k] for j in range(len(pts))) for k in range(r)]
            w0 = x0 + [rnd(-2, 2) for _ in range(N - d)]
            b = [y0[i] + sum(A[i][j] * w0[j] for j in range(N)) for i in range(m)]
            e = [h0[k] + sum(C[k][j] * w0[j] for j in range(N)) for k in range(r)]
            data = (pts, gvals, hvals, A, C, b, e)
            assert member(w0, data, d)
            inside_conv = member_conv_sigma(w0, data, d)
            tested[kind] += 1
            if kind == "full_rank":
                import sympy as _sp
                Mz = _sp.Matrix([[A[i][j] for j in range(d, N)] for i in range(m)]
                                + [[C[k][j] for j in range(d, N)] for k in range(r)])
                if Mz.rank() == m + r:
                    assert inside_conv, (t, w0)
            if not inside_conv:
                gaps[kind] += 1
            # sanity: a point of Sigma_D itself (Dirac mixture) lies in conv(Sigma_D)
            j0 = random.randrange(len(pts))
            wd = list(pts[j0]) + [rnd(-2, 2) for _ in range(N - d)]
            bd = [gvals[j0][i] + sum(A[i][j] * wd[j] for j in range(N)) + Fr(1, 8) for i in range(m)]
            ed = [hvals[j0][k] + sum(C[k][j] * wd[j] for j in range(N)) for k in range(r)]
            assert member_conv_sigma(wd, (pts, gvals, hvals, A, C, bd, ed), d)
    print("free-remainder test: points of R_D outside conv(Sigma_D):", gaps, "of", tested)


if __name__ == "__main__":
    free_remainder_test()
    print("M1_closure_random (free remainder): all checks passed")
