"""[Note, 2026-10-02: used for the family-(A) certificates of Section 9.2 of note.md. The family-(B)
sector search and the family-(BP) triangle search below did not finish (CLOSEOUT.md); they are
superseded by box_cert.py (B, BP at the Theorem 14 corner) and by the analytic proof of
Theorem 11(c) (BP at the W-corner).  References to "Lemma 7/8 of the note" below refer to an
earlier draft; the certificate argument is Lemma 16 of note.md.]

Exact certificate that a rational point lam_hat lies in the closure of the orbit family (A)
or of its maximal completion (B) at a rational bilinear corner (S = {w <= xy}).

Certificate (Lemma 7 of the note).  Let Pi be a polytope of cut vectors a in R^N_+.  Suppose
there are symmetric Y_1, ..., Y_N >= 0 (Y_j = 0 when lam_hat_j = 0) such that
    R := -M(sbar)^{-1} sum_j M0(p_j) Y_j  is symmetric, and
    Q(a) := R - sum_j a_j Y_j  is PSD with positive trace at every vertex a of Pi.
(A) Then no orbit set C_F with sbar in int C_F has cut vector a(F) in Pi:
    with A_0 = sym(F^T M(sbar)) > 0, A_j = sym(F^T M0(p_j)) one has a_j A_0 + A_j >= 0, so
    0 <= sum_j <a_j A_0 + A_j, Y_j> = <A_0, sum_j a_j Y_j - R> = -<A_0, Q(a)> < 0.
(B) For the completions B_F = cl(C_F + R_+ e_w) the same holds for every F whose first row
    (F_11, F_12) lies in a closed sector cone{u, u'} such that u.(Y_11, Y_12) >= 0 and
    u'.(Y_11, Y_12) >= 0 for every Y in {Y_j} and every Q(vertex): then <Z, Y> >= 0 with
    Z = sym(F^T E) (since <Z, Y> = F_11 Y_11 + F_12 Y_12), points s of B_F satisfy
    <A(s), Y> >= 0 for such Y, and sbar in int B_F gives A_0 - tau_0 Z > 0 for some tau_0 >= 0, so
    <A_0, Q> = <A_0 - tau_0 Z, Q> + tau_0 <Z, Q> > 0 for Q >= 0, Q != 0.
If the pieces cover Delta = {a >= 0 : lam_hat^T a <= 1} (for every sector in case (B)), every cut
of the family satisfies a^T lam_hat > 1, so lam_hat is in the closure.

Pieces are simplices in the coordinates j with lam_hat_j > 0 (coordinates with lam_hat_j = 0 do
not enter: a_j is free there and Y_j = 0), refined by bisecting the longest edge (squared lengths
compared exactly; first pair in lexicographic order on ties).  Each certificate is found with
Clarabel, rounded to rationals, the symmetry of R is restored exactly by solving for one entry,
and every condition is checked in exact rational arithmetic.

Usage:  python3 certify_closure_point.py INSTANCE FAMILY      (FAMILY = A or B)
Writes ../logs/closure_cert_INSTANCE_FAMILY.json (checked by the separate verify_closure_cert.py).
"""
import sys, json, time, itertools
from fractions import Fraction as Fr
import numpy as np
import cvxpy as cp

SECTORS4 = [(('1', '0'), ('0', '1')), (('0', '1'), ('-1', '0')), (('-1', '0'), ('0', '-1')), (('0', '-1'), ('1', '0'))]
# Lemma 8 of the note: if sbar in int B_F with det F > 0 then the first row f of F satisfies
# f . (1, -sbar_y) > 0, and every F with sbar in int B_F and f . (1, -sbar_y) > 0 has det F > 0.
# For sbar_y = 0 the sectors below cover the half-plane f_1 >= 0.
_DIRS = [('0', '-1'), ('1', '-2'), ('1', '-1'), ('2', '-1'), ('1', '0'), ('2', '1'), ('1', '1'), ('1', '2'), ('0', '1')]
SECTORS_HALF8 = [(_DIRS[i], _DIRS[i + 1]) for i in range(8)]

INSTANCES = {
    # W-corner: sbar in the interior of the McCormick wedge W = {x >= 0, y <= 0, w >= 0}; rays e_x, -e_y, e_w, -e_w.
    # D = {lam >= 0 : lam_4 >= 2}; the point (t, t, t, 0) is not in any scaling of D.
    'wcorner_A': dict(sbar=['1', '-1', '1'], rays=[['1', '0', '0'], ['0', '-1', '0'], ['0', '0', '1'], ['0', '0', '-1']],
                      lam=['20', '20', '20', '0']),
    'wcorner_BP': dict(sbar=['1', '-1', '1'], rays=[['1', '0', '0'], ['0', '-1', '0'], ['0', '0', '1'], ['0', '0', '-1']],
                       lam=['6', '6', '0', '0']),
    # Proposition 16 corner of the sfree note (support-one minimizer lam* = e_1, z_K(1,1,1) = 1)
    'prop16': dict(sbar=['-2', '3', '2'], verts=[['0', '0', '0'], ['6', '-2', '1/4'], ['1', '-5/2', '1/2']],
                   lam=['24/25', '1/100', '29/1000'], xpoints=[['1', '0', '0']], sectors=None),
    # Theorem 14 corner of the sfree note; lam_hat = (27, 41, 30)/99, sum 98/99 < 1 = z_K(1,1,1)
    'thm14': dict(sbar=['-9/2', '0', '3/2'],
                  verts=[['-1', '-6', '18'], ['-5', '6', '-18'], ['0', '5/2', '5/2']],
                  lam=['3/11', '41/99', '10/33'], xpoints=[['1/2', '1/2', '0']], sectors=SECTORS_HALF8),
}


def half_plane_sectors(sy, k=8):
    """k consecutive sectors covering the closed half-plane {f : f . (1, -sy) >= 0} (Lemma 8)."""
    n = (Fr(1), -Fr(sy))
    t = (Fr(sy), Fr(1))                 # tangent direction (n rotated by +90 degrees)
    # directions -t, then n*c + t*s for a rational parametrization of the half circle, then +t
    dirs = [(-t[0], -t[1])]
    for i in range(1, k):
        # rational point on the half circle: angle phi_i in (-pi/2, pi/2); use tan(phi/2) = r
        r = Fr(2 * i - k, k + 1)        # in (-1, 1), increasing
        c, s_ = (1 - r * r) / (1 + r * r), 2 * r / (1 + r * r)
        dirs.append((c * n[0] + s_ * t[0], c * n[1] + s_ * t[1]))
    dirs.append(t)
    return [((str(dirs[i][0]), str(dirs[i][1])), (str(dirs[i + 1][0]), str(dirs[i + 1][1]))) for i in range(k)]


def M_ex(s, h=1):
    x, y, w = s
    return [[w, x], [y, Fr(h)]]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def inv2(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def psd2(X):
    """exact: symmetric 2x2 PSD"""
    assert X[0][1] == X[1][0]
    return X[0][0] >= 0 and X[1][1] >= 0 and X[0][0] * X[1][1] - X[0][1] ** 2 >= 0


def setup(inst):
    sbar = [Fr(v) for v in inst['sbar']]
    if 'verts' in inst:
        P = [[Fr(vv[i]) - sbar[i] for i in range(3)] for vv in inst['verts']]
    else:
        P = [[Fr(v) for v in p] for p in inst['rays']]
    lam = [Fr(v) for v in inst['lam']]
    Msi = inv2(M_ex(sbar))
    Nj = [matmul(Msi, M_ex(p, 0)) for p in P]                     # M(sbar)^{-1} M0(p_j)
    return sbar, P, lam, Nj


def R_of(Nj, Ys):
    R = [[0, 0], [0, 0]]
    for N, Y in zip(Nj, Ys):
        NY = matmul(N, Y)
        for i in range(2):
            for k in range(2):
                R[i][k] -= NY[i][k]
    return R


def sdp_cert(Nj_f, act, verts_a, sector=None, solver='CLARABEL', NE_f=None):
    """Y_j (j in act) >= 0, R symmetric, Q(vertex) >= t I, sector constraints; maximize t.
    NE_f = (N_E, [S^(k)]) given (family BP): also <S^(k), sym(N_E Y_j)> >= 0 for the vertices S^(k)
    of the current triangle of point-rule matrices S, N_E = M(sbar)^{-1} E."""
    Y = {j: cp.Variable((2, 2), symmetric=True) for j in act}
    t = cp.Variable()
    R = -sum(Nj_f[j] @ Y[j] for j in act)
    # point-rule families (BP): F^T M(sbar) = S is symmetric, so only sym(R) matters (Lemma 7(c))
    cons = [] if NE_f is not None else [R[0, 1] == R[1, 0]]
    Rs = (R + R.T) / 2
    mats = []
    for j in act:
        cons.append(Y[j] >> 0.02 * t * np.eye(2))      # keep Y_j PD so that rounding cannot break PSD
        mats.append(Y[j])
    for a in verts_a:
        Q = Rs - sum(a[j] * Y[j] for j in act)
        cons.append(Q >> t * np.eye(2))
        mats.append(Q)
    if sector is not None:
        for u in sector:
            for X in mats:
                cons.append(u[0] * X[0, 0] + u[1] * X[0, 1] >= 0.02 * t)
    if NE_f is not None:
        NEm, Svs = NE_f
        for j in act:
            W = NEm @ Y[j]
            for Sk in Svs:
                cons.append(cp.trace(Sk @ (W + W.T) / 2) >= 0.02 * t)
    cons.append(cp.trace(Rs) + sum(cp.trace(Y[j]) for j in act) == 1)
    pr = cp.Problem(cp.Maximize(t), cons)
    try:
        pr.solve(solver=solver)
    except Exception:
        return None, None
    if pr.status not in ('optimal', 'optimal_inaccurate') or t.value is None:
        return None, None
    return {j: Y[j].value for j in act}, t.value


def exact_check(Nj, act, Ys_f, verts_a_ex, sector_ex=None, den=10 ** 9, NE=None):
    """Round, restore symmetry of R exactly, check all conditions exactly."""
    n = len(Nj)
    Ys = []
    for j in range(n):
        if j in act:
            Yf = Ys_f[j]
            a = Fr(Yf[0, 0]).limit_denominator(den); b = Fr(Yf[0, 1]).limit_denominator(den)
            c = Fr(Yf[1, 1]).limit_denominator(den)
            Ys.append([[a, b], [b, c]])
        else:
            Ys.append([[Fr(0), Fr(0)], [Fr(0), Fr(0)]])

    def asym(Ys_):
        R = R_of(Nj, Ys_)
        return R[0][1] - R[1][0]
    if NE is not None:
        R = R_of(Nj, Ys)
        R = [[R[0][0], (R[0][1] + R[1][0]) / 2], [(R[0][1] + R[1][0]) / 2, R[1][1]]]
        return _finish_check(Ys, R, act, verts_a_ex, sector_ex, NE)
    best = None
    for j in act:
        for (r, s) in ((0, 0), (0, 1), (1, 1)):
            Yt = [[row[:] for row in Y] for Y in Ys]
            Yt[j][r][s] += 1
            if (r, s) == (0, 1):
                Yt[j][1][0] += 1
            coef = asym(Yt) - asym(Ys)
            if coef != 0 and (best is None or abs(coef) > abs(best[0])):
                best = (coef, j, r, s)
    coef, j, r, s = best
    delta = -asym(Ys) / coef
    Ys[j][r][s] += delta
    if (r, s) == (0, 1):
        Ys[j][1][0] += delta
    R = R_of(Nj, Ys)
    if R[0][1] != R[1][0]:
        return False, None
    return _finish_check(Ys, R, act, verts_a_ex, sector_ex, NE)


def _finish_check(Ys, R, act, verts_a_ex, sector_ex, NE):
    ok = all(psd2(Y) for Y in Ys)
    mats = [Ys[j] for j in act]
    for a in verts_a_ex:
        Q = [[R[i][k] - sum(a[jj] * Ys[jj][i][k] for jj in act) for k in range(2)] for i in range(2)]
        ok &= psd2(Q) and (Q[0][0] + Q[1][1] > 0)
        mats.append(Q)
    if sector_ex is not None:
        for u in sector_ex:
            for X in mats:
                ok &= (u[0] * X[0][0] + u[1] * X[0][1] >= 0)
    if NE is not None:
        NEm, Svs = NE
        for j in act:
            W = matmul(NEm, Ys[j])
            Ws = [[W[0][0], (W[0][1] + W[1][0]) / 2], [(W[0][1] + W[1][0]) / 2, W[1][1]]]
            for Sk in Svs:
                ok &= sum(Sk[i][k] * Ws[k][i] for i in range(2) for k in range(2)) >= 0
    return ok, Ys


def split(piece, act):
    """Bisect the longest edge (exact squared lengths over the active coordinates)."""
    best = None
    for i, k in itertools.combinations(range(len(piece)), 2):
        d = sum((piece[i][m] - piece[k][m]) ** 2 for m in act)
        if best is None or d > best[0]:
            best = (d, i, k)
    _, i, k = best
    n = len(piece[0])
    mid = [(piece[i][m] + piece[k][m]) / 2 for m in range(n)]
    p1 = [v if idx != i else mid for idx, v in enumerate(piece)]
    p2 = [v if idx != k else mid for idx, v in enumerate(piece)]
    return p1, p2


def initial_simplex(lam, act):
    n = len(lam)
    return [[Fr(0)] * n] + [[(Fr(1) / lam[j] if k == j else Fr(0)) for k in range(n)] for j in act]


def x_points(sbar, P, ngrid=12, include=()):
    """Exact rational points of X = {lam >= 0 : q(sbar + P lam) <= 0}: for grid directions d in the
    simplex, a rational point slightly beyond the first hit of the ray {t d}; q <= 0 checked exactly."""
    n = len(P)
    q = lambda s: s[2] - s[0] * s[1]
    pts = [[Fr(v) for v in p] for p in include]
    for p in pts:
        s_ = [sbar[i] + sum(p[j] * P[j][i] for j in range(n)) for i in range(3)]
        assert q(s_) <= 0
    for comb in itertools.product(range(ngrid + 1), repeat=n):
        if sum(comb) != ngrid:
            continue
        d = [Fr(c, ngrid) for c in comb]
        # q(sbar + t P d) = g0 + g1 t + g2 t^2
        Pd = [sum(d[j] * P[j][i] for j in range(n)) for i in range(3)]
        g0 = q(sbar); g1 = Pd[2] - sbar[0] * Pd[1] - sbar[1] * Pd[0]; g2 = -Pd[0] * Pd[1]
        ts = np.roots([float(g2), float(g1), float(g0)]) if g2 != 0 else ([-float(g0) / float(g1)] if g1 != 0 else [])
        ts = sorted(t.real for t in ts if abs(np.imag(t)) < 1e-12 and t.real > 0)
        if not ts:
            continue
        for fac in (Fr(1000001, 1000000), Fr(10001, 10000), Fr(101, 100)):
            t = Fr(ts[0]).limit_denominator(10 ** 8) * fac
            lamx = [t * dj for dj in d]
            s_ = [sbar[i] + sum(lamx[j] * P[j][i] for j in range(n)) for i in range(3)]
            if q(s_) <= 0:
                pts.append(lamx)
                break
    return pts


def outside_V(piece, xpts, act):
    """index k such that every vertex a of the piece has a^T x_k < 1 (piece misses the valid set)"""
    for k, x in enumerate(xpts):
        if any(x[j] != 0 for j in range(len(x)) if j not in act):
            continue  # inactive cut coordinates are unbounded on this piece
        if all(sum(a[j] * x[j] for j in range(len(x))) < 1 for a in piece):
            return k
    return None


def cover(Nj, lam, sector=None, max_sdp=200000, label='', xpts=None, NE=None, zero=()):
    """zero: indices j with a_j(F) = 0 for every member of the family (rays along +e_w for (B)
    families); they get a multiplier Y_j but do not enter Q(a) (a_j = 0 on every piece)."""
    n = len(lam)
    act = [j for j in range(n) if lam[j] > 0]
    yidx = act + [j for j in zero if j not in act]
    Nj_f = [np.array([[float(v) for v in row] for row in N]) for N in Nj]
    sector_f = None if sector is None else [[float(v) for v in u] for u in sector]
    NE_f = None if NE is None else (np.array([[float(v) for v in row] for row in NE[0]]),
                                     [np.array([[float(v) for v in row] for row in Sk]) for Sk in NE[1]])
    queue = [initial_simplex(lam, act)]
    certified = []
    t0 = time.time(); nsdp = 0
    while queue:
        piece = queue.pop(0)
        nsdp += 1
        if nsdp % 500 == 0:
            print('  %s %d SDPs, %d certified, %d open (%.0f s)' % (label, nsdp, len(certified), len(queue), time.time() - t0), flush=True)
        if nsdp > max_sdp:
            print('  %s budget of %d SDPs exhausted' % (label, max_sdp), flush=True)
            return False, certified
        if xpts is not None:
            k = outside_V(piece, xpts, act)
            if k is not None:
                certified.append((piece, ('outside', k)))
                continue
        vf = [np.array([float(v) for v in a]) for a in piece]
        Ys_f, tval = sdp_cert(Nj_f, yidx, vf, sector_f, NE_f=NE_f)
        ok = False
        if Ys_f is not None and tval > 0:
            ok, Ys = exact_check(Nj, yidx, Ys_f, piece, sector, NE=NE)
        if ok:
            certified.append((piece, Ys))
            continue
        queue += list(split(piece, act))
    print('  %s certified: %d pieces cover Delta (%d SDPs, %.1f s)' % (label, len(certified), nsdp, time.time() - t0), flush=True)
    return True, certified


def S_of_u(u):
    """trace-one symmetric matrix of the point-rule parametrization (PD iff u1^2 + u2^2 < 1)"""
    return [[Fr(1, 2) + u[0] / 2, u[1] / 2], [u[1] / 2, Fr(1, 2) - u[0] / 2]]


def tri_meets_open_disk(T):
    """exact: min over the triangle of u1^2 + u2^2 < 1"""
    (a, b, c) = T
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    O = (Fr(0), Fr(0))
    d1, d2, d3 = cross(a, b, O), cross(b, c, O), cross(c, a, O)
    if (d1 >= 0 and d2 >= 0 and d3 >= 0) or (d1 <= 0 and d2 <= 0 and d3 <= 0):
        return True
    best = None
    for p, q in ((a, b), (b, c), (c, a)):
        dx, dy = q[0] - p[0], q[1] - p[1]
        tt = -(p[0] * dx + p[1] * dy) / (dx * dx + dy * dy)
        tt = min(Fr(1), max(Fr(0), tt))
        x, y = p[0] + tt * dx, p[1] + tt * dy
        v = x * x + y * y
        best = v if best is None else min(best, v)
    return best < 1


def split_tri(T):
    best = None
    for i, k in ((0, 1), (1, 2), (0, 2)):
        d = (T[i][0] - T[k][0]) ** 2 + (T[i][1] - T[k][1]) ** 2
        if best is None or d > best[0]:
            best = (d, i, k)
    _, i, k = best
    m = ((T[i][0] + T[k][0]) / 2, (T[i][1] + T[k][1]) / 2)
    return (tuple(v if idx != i else m for idx, v in enumerate(T)),
            tuple(v if idx != k else m for idx, v in enumerate(T)))


TRI_ROOTS = [((Fr(-1), Fr(-1)), (Fr(1), Fr(-1)), (Fr(1), Fr(1))), ((Fr(-1), Fr(-1)), (Fr(1), Fr(1)), (Fr(-1), Fr(1)))]


def zero_idx(P):
    """rays that are positive multiples of e_w (recession directions of every (B) set)"""
    return [j for j, p in enumerate(P) if p[0] == 0 and p[1] == 0 and p[2] > 0]


def run_BP(name, inst, sbar, P, lam, Nj, budget=80):
    NEm = matmul(inv2(M_ex(sbar)), [[Fr(1), Fr(0)], [Fr(0), Fr(0)]])
    result = dict(instance=inst, family='BP', tri_roots=[[[str(v) for v in p] for p in T] for T in TRI_ROOTS], blocks=[])
    stack = list(TRI_ROOTS)
    allok = True
    while stack:
        T = stack.pop(0)
        if not tri_meets_open_disk(T):
            result['blocks'].append(dict(triangle=[[str(v) for v in p] for p in T], skip=True))
            continue
        Svs = [S_of_u(p) for p in T]
        ok, cert = cover(Nj, lam, None, max_sdp=budget, label='triangle %s' % [[float(v) for v in p] for p in T],
                         NE=(NEm, Svs), zero=zero_idx(P))
        if not ok:
            if max(abs(T[0][0] - T[1][0]), abs(T[0][1] - T[1][1]), abs(T[1][0] - T[2][0])) < Fr(1, 2 ** 12):
                allok = False
                result['blocks'].append(dict(triangle=[[str(v) for v in p] for p in T], ok=False))
                continue
            stack += list(split_tri(T))
            continue
        result['blocks'].append(dict(triangle=[[str(v) for v in p] for p in T], ok=True,
                                     pieces=[dict(vertices=[[str(v) for v in a] for a in piece],
                                                  Y=[[[str(v) for v in row] for row in Y] for Y in Ys])
                                             for piece, Ys in cert]))
    result['ok'] = allok
    return result


def run(name, fam, sector_ids=None):
    inst = INSTANCES[name]
    sbar, P, lam, Nj = setup(inst)
    print('instance %s family %s: sbar=%s lam_hat=%s, sum lam_hat = %s' % (name, fam, inst['sbar'], inst['lam'], sum(lam)), flush=True)
    if fam == 'BP':
        return run_BP(name, inst, sbar, P, lam, Nj)
    result = dict(instance=dict(inst), family=fam, blocks=[])
    if fam in ('A', 'BP'):
        sectors = [None]
    else:
        secs = inst.get('sectors', SECTORS4)
        if secs is None:
            secs = half_plane_sectors(sbar[1])
        sectors = [tuple(tuple(Fr(v) for v in u) for u in s) for s in secs]
    NE = None
    if fam == 'B' and sector_ids is not None:
        sectors = [sectors[i] for i in sector_ids]
    xpts = None
    if fam == 'B':
        # (B) sets with det F > 0 are S-free, so their cut vectors are valid for X: a^T x >= 1 for x in X
        xpts = x_points(sbar, P, include=inst.get('xpoints', ()))
        result['instance']['xpoints'] = [[str(v) for v in x] for x in xpts]
        print('  %d exact points of X used for pruning' % len(xpts), flush=True)
    allok = True
    for sec in sectors:
        ok, cert = cover(Nj, lam, sec, label='sector %s' % (None if sec is None else [[str(v) for v in u] for u in sec]),
                         xpts=xpts, NE=NE, zero=zero_idx(P) if fam == 'B' else ())
        allok &= ok
        result['blocks'].append(dict(sector=None if sec is None else [[str(v) for v in u] for u in sec], ok=ok,
                                     pieces=[dict(vertices=[[str(v) for v in a] for a in piece],
                                                  outside=Ys[1]) if isinstance(Ys, tuple) else
                                             dict(vertices=[[str(v) for v in a] for a in piece],
                                                  Y=[[[str(v) for v in row] for row in Y] for Y in Ys])
                                             for piece, Ys in cert]))
    result['ok'] = allok
    return result


if __name__ == '__main__':
    name = sys.argv[1] if len(sys.argv) > 1 else 'thm14'
    fam = sys.argv[2] if len(sys.argv) > 2 else 'A'
    sector_ids = [int(v) for v in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
    res = run(name, fam, sector_ids)
    res['sector_ids'] = sector_ids
    tag = '' if sector_ids is None else '_s' + '-'.join(str(i) for i in sector_ids)
    out = '../logs/closure_cert_%s_%s%s.json' % (name, fam, tag)
    with open(out, 'w') as fh:
        json.dump(res, fh)
    print('ALL PASS' if res['ok'] else 'FAILED', '; certificate written to', out)
