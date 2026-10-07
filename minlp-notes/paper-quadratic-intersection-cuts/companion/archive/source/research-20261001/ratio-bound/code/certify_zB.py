"""Branch-and-bound search for an infeasibility proof (Theorem B2 of the note): in the normalized frame of
the Theorem B family, no family-(B) set contains sbar = (0, 0, 1), P1 = (rho, -rho, 1), P2 = (rho, -2 rho, 1)
and meets the vertical line {(rho, rho, h)}.

Family (B) set of X (2x2, det X > 0): B_X = cl(C_X + R_+ e_w), C_X = {s : sym(X M(s)) >= 0},
M(x, y, w) = [[w, x], [y, 1]].  A point s with q(s) = w - x y >= 0 lies in B_X iff some lowered point
s - tau e_w with 0 <= tau <= q(s) lies in C_X (lowered points of C_X have q >= 0 when det X > 0).

Necessary conditions used (all hold for every valid set that contains the simplex; sbar in the
interior of B_X is relaxed to sbar in B_X):
  point conditions for sbar, P1, P2 and the midpoints m01, m02, m12 (convexity),
  line condition: sym(X M(rho, rho, h)) >= 0 for some h (then h >= rho^2 automatically),
  det X > 0.

Certificates for a box of X (one entry of X fixed to +-1, the other three in a box; X is defined up
to a positive factor, so the 8 facets of the cube max|x_ij| = 1 cover all X):
  'det'  : det X < 0 at every vertex of the box (det is multilinear in the free entries);
  'pt'   : a vector v with v^T X M(s) v < 0 and v^T X M(s - q(s) e_w) v < 0 on the whole box (both forms
           are linear in X).  Then for every tau in [0, q(s)] the matrix sym(X M(s - tau e_w)) has a
           negative quadratic form at v (convex combination), so s is not in B_X;
  'psi'  : an interval upper bound of Psi(X) = rho x21 (x11 - x22) + x11 x22 - rho^2 x21^2 is < 0.  For
           det X > 0 and x21 != 0, max_h det sym(X M(rho, rho, h)) = (det X / x21^2) Psi(X); for x21 = 0,
           Psi = det X > 0.  So Psi < 0 excludes the line condition for every X of the box with det X > 0;
  'a22'  : rho x21 + x22 < 0 on the box (the (2,2) entry of sym(X M(rho, rho, h)), independent of h).
The search uses floats with a safety margin; verify_zB.py re-checks every leaf in exact rational
arithmetic and checks that the leaves cover all 8 facets.

usage: python3 certify_zB.py RHO OUTFILE [TIMEOUT_SECONDS] [MAXDEPTH] [FAMILY]
  RHO may be a fraction such as 7/5; FAMILY is 'B' (default) or 'tan:ETA:K' (see family_points_exact).
Checkpointing: leaves are appended to OUTFILE as they are certified (one JSON line each, with the
facet and the bisection path); a rerun skips facets marked done in OUTFILE.
"""
import sys
import json
import time
from fractions import Fraction
from math import sqrt

E = ((1.0, 0.0), (0.0, 0.0))
FACETS = [(i, j, s) for i in range(2) for j in range(2) for s in (1, -1)]


def Mmat(s):
    x, y, w = s
    return ((w, x), (y, 1.0))


def symXN(X, N):
    a = X[0][0] * N[0][0] + X[0][1] * N[1][0]
    b = X[0][0] * N[0][1] + X[0][1] * N[1][1]
    c = X[1][0] * N[0][0] + X[1][1] * N[1][0]
    d = X[1][0] * N[0][1] + X[1][1] * N[1][1]
    return (a, 0.5 * (b + c), d)


def lmin_vec(S):
    a, b, d = S
    tr = 0.5 * (a + d)
    r = sqrt(0.25 * (a - d) ** 2 + b * b)
    lam = tr - r
    if abs(b) > 1e-300:
        v = (lam - d, b) if abs(lam - d) > abs(lam - a) else (b, lam - a)
    else:
        v = (1.0, 0.0) if a <= d else (0.0, 1.0)
    n = sqrt(v[0] ** 2 + v[1] ** 2)
    return lam, (v[0] / n, v[1] / n)


def comb(S, T, t):
    return (S[0] + t * T[0], S[1] + t * T[1], S[2] + t * T[2])


def maxconc(f, lo, hi, it=90):
    gr = (sqrt(5) - 1) / 2
    a, b = lo, hi
    for _ in range(it):
        m1, m2 = b - gr * (b - a), a + gr * (b - a)
        if f(m1) >= f(m2):
            b = m2
        else:
            a = m1
    cands = [lo, hi, 0.5 * (a + b)]
    vals = [f(c) for c in cands]
    k = max(range(3), key=lambda i: vals[i])
    return vals[k], cands[k]


def family_points_exact(spec, rho):
    """Exact test points [sbar, P1, P2, m01, m02, m12] for a family spec and rho (Fraction).
    spec 'B'           : Theorem B family, P1 = (rho, -rho, 1), P2 = (rho, -2 rho, 1);
    spec 'tan:ETA:K'   : near-tangent family (Section 3.3), P1 = (rho, -rho, 1 - 2 rho (1 - ETA)),
                         P2 = (rho, -K rho, 1 - 2 sqrt(K) rho (1 - ETA)); K must be the square of a rational.
    The third vertex lies on the vertical line over (rho, rho) in both families."""
    r = Fraction(rho)
    one = Fraction(1)
    sb = (Fraction(0), Fraction(0), one)
    if spec == 'B':
        p1, p2 = (r, -r, one), (r, -2 * r, one)
    elif spec.startswith('tan:'):
        _, eta, k = spec.split(':')
        eta, k = Fraction(eta), Fraction(k)
        sk = Fraction(int(round(float(k.numerator) ** 0.5)), int(round(float(k.denominator) ** 0.5)))
        assert sk * sk == k, 'K must be a rational square'
        p1 = (r, -r, 1 - 2 * r * (1 - eta))
        p2 = (r, -k * r, 1 - 2 * sk * r * (1 - eta))
    else:
        raise ValueError(spec)
    mid = lambda a, b: tuple((a[i] + b[i]) / 2 for i in range(3))
    return [sb, p1, p2, mid(sb, p1), mid(sb, p2), mid(p1, p2)]


def points(rho, spec='B'):
    return [tuple(float(t) for t in p) for p in family_points_exact(spec, Fraction(rho))]


def lin_coef(v, N):
    Nv = (N[0][0] * v[0] + N[0][1] * v[1], N[1][0] * v[0] + N[1][1] * v[1])
    return ((v[0] * Nv[0], v[0] * Nv[1]), (v[1] * Nv[0], v[1] * Nv[1]))


def box_max_lin(c, lo, hi):
    m = 0.0
    for i in range(2):
        for j in range(2):
            m += c[i][j] * (hi[i][j] if c[i][j] > 0 else lo[i][j])
    return m


def box_of(facet, path):
    """Box (lo, hi as 2x2 lists of Fractions) for a facet and a bisection path ('0'/'1' string).
    The split coordinate is the free coordinate with the longest edge (ties: lowest index)."""
    fi, fj, fs = facet
    lo = [[Fraction(-1), Fraction(-1)], [Fraction(-1), Fraction(-1)]]
    hi = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(1)]]
    lo[fi][fj] = hi[fi][fj] = Fraction(fs)
    free = [(i, j) for i in range(2) for j in range(2) if (i, j) != (fi, fj)]
    for ch in path:
        i, j = max(free, key=lambda ij: (hi[ij[0]][ij[1]] - lo[ij[0]][ij[1]], -free.index(ij)))
        mid = (lo[i][j] + hi[i][j]) / 2
        if ch == '0':
            hi[i][j] = mid
        else:
            lo[i][j] = mid
    return lo, hi


def det_max_vertices(lo, hi):
    best = None
    for a in (lo[0][0], hi[0][0]):
        for b in (lo[0][1], hi[0][1]):
            for c in (lo[1][0], hi[1][0]):
                for d in (lo[1][1], hi[1][1]):
                    v = a * d - b * c
                    best = v if best is None or v > best else best
    return best


def iv_mul(a, b):
    ps = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (min(ps), max(ps))


def psi_upper(lo, hi, rho):
    """Interval upper bound of Psi = rho x21 x11 - rho x21 x22 + x11 x22 - rho^2 x21^2
    (indices 0-based in code: x11 = X[0][0], x12 = X[0][1], x21 = X[1][0], x22 = X[1][1])."""
    I = lambda i, j: (lo[i][j], hi[i][j])
    x21 = I(1, 0)
    t1 = iv_mul(x21, I(0, 0))[1] * rho
    t2 = iv_mul(x21, I(1, 1))[0] * rho        # minus rho x21 x22: use the minimum of the product
    t3 = iv_mul(I(0, 0), I(1, 1))[1]
    sq = Fraction(0) if (x21[0] <= 0 <= x21[1]) else min(x21[0] * x21[0], x21[1] * x21[1])
    return t1 - t2 + t3 - rho * rho * sq


def rat(v, den=2 ** 24):
    return (Fraction(round(v[0] * den), den), Fraction(round(v[1] * den), den))


def try_certify(lo, hi, X, rho, pts, qs):
    """Float search for a certificate on the box; returns (kind, data) or None, plus a flag 'feasible'
    if all conditions hold at the center X."""
    flo = [[float(lo[i][j]) for j in range(2)] for i in range(2)]
    fhi = [[float(hi[i][j]) for j in range(2)] for i in range(2)]
    if float(det_max_vertices(lo, hi)) < -1e-12:
        return ('det', None), False
    Z = symXN(X, E)
    fails = []
    for k, s in enumerate(pts):
        A = symXN(X, Mmat(s))
        f = lambda t: lmin_vec(comb(A, Z, -t))[0]
        val, ts = maxconc(f, 0.0, qs[k])
        cands = [ts, 0.0, qs[k]]
        fails.append((val, k, cands, A))
    ok_all = all(f[0] >= 0 for f in fails)
    if float(psi_upper(lo, hi, rho)) < -1e-9:
        return ('psi', None), False
    if rho * fhi[1][0] + fhi[1][1] < -1e-12:
        return ('a22', None), False
    for val, k, cands, A in sorted(fails, key=lambda t: t[0]):
        if val >= 0:
            break
        s = pts[k]
        N1, N2 = Mmat(s), Mmat((s[0], s[1], s[2] - qs[k]))
        for ts in cands:
            v = lmin_vec(comb(A, Z, -ts))[1]
            vr = rat(v)
            vf = (float(vr[0]), float(vr[1]))
            c1, c2 = lin_coef(vf, N1), lin_coef(vf, N2)
            sc = 1.0 + sum(abs(c1[i][j]) + abs(c2[i][j]) for i in range(2) for j in range(2))
            if box_max_lin(c1, flo, fhi) < -1e-9 * sc and box_max_lin(c2, flo, fhi) < -1e-9 * sc:
                return ('pt', (k, [str(vr[0]), str(vr[1])])), False
    # line condition at the center (only for the feasibility flag)
    r = rho
    A0 = symXN(X, Mmat((r, r, r * r)))
    fl = lambda t: lmin_vec(comb(A0, Z, t))[0]
    T = 1.0
    while fl(2 * T) > fl(T) and T < 1e30:
        T *= 2
    lv, _ = maxconc(fl, 0.0, 2 * T)
    detc = X[0][0] * X[1][1] - X[0][1] * X[1][0]
    return None, (ok_all and lv >= 0 and detc > 0)


def run(rho_str, outfile, timeout, maxdepth, spec='B'):
    t0 = time.time()
    rho = float(Fraction(rho_str))
    pts = points(Fraction(rho_str), spec)
    qs = [s[2] - s[0] * s[1] for s in pts]
    done = set()
    try:
        for line in open(outfile):
            d = json.loads(line)
            if d.get('facet_done'):
                done.add(tuple(d['facet']))
    except FileNotFoundError:
        pass
    out = open(outfile, 'a')
    stats = {}
    for facet in FACETS:
        if facet in done:
            continue
        # restart the facet from scratch (leaves of an unfinished facet are discarded by the verifier)
        out.write(json.dumps({'facet_start': list(facet), 'rho': str(Fraction(rho_str)), 'family': spec}) + '\n')
        stack = ['']
        nleaf = 0
        while stack:
            if time.time() - t0 > timeout:
                out.write(json.dumps({'timeout': True, 'facet': list(facet)}) + '\n')
                out.close()
                print('TIMEOUT in facet', facet, 'leaves so far', nleaf, flush=True)
                return False
            path = stack.pop()
            lo, hi = box_of(facet, path)
            X = [[float((lo[i][j] + hi[i][j]) / 2) for j in range(2)] for i in range(2)]
            cert, feas = try_certify(lo, hi, X, rho, pts, qs)
            if cert is not None:
                out.write(json.dumps({'facet': list(facet), 'path': path, 'cert': cert[0], 'data': cert[1]}) + '\n')
                nleaf += 1
                continue
            if feas:
                out.write(json.dumps({'feasible_point': X, 'facet': list(facet), 'path': path}) + '\n')
                out.close()
                print('FEASIBLE POINT FOUND', X, flush=True)
                return False
            if len(path) >= maxdepth:
                out.write(json.dumps({'maxdepth': True, 'facet': list(facet), 'path': path}) + '\n')
                out.close()
                print('MAXDEPTH reached at', facet, path, X, flush=True)
                return False
            stack.append(path + '1')
            stack.append(path + '0')
        out.write(json.dumps({'facet_done': True, 'facet': list(facet), 'leaves': nleaf}) + '\n')
        out.flush()
        stats[facet] = nleaf
        print('facet', facet, 'done, leaves', nleaf, 'elapsed %.0fs' % (time.time() - t0), flush=True)
    out.close()
    print('ALL FACETS DONE', stats, flush=True)
    return True


if __name__ == '__main__':
    rho_str = sys.argv[1]
    outfile = sys.argv[2]
    timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 3600
    maxdepth = int(sys.argv[4]) if len(sys.argv) > 4 else 60
    spec = sys.argv[5] if len(sys.argv) > 5 else 'B'
    run(rho_str, outfile, timeout, maxdepth, spec)
