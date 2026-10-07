"""Primal box certificate that a rational point lam_hat lies in the closure of the completion
family (B) or of SCIP's point-rule completion family (BP) at a rational corner of S = {w <= xy}.

Notation (Sections 1 and 3 of note.md).  M(s) = [[w, x], [y, 1]], q(s) = det M(s) = w - xy.  A set of
the family is B_F = cl(C_F + R_+ e_w) with C_F = {s : sym(F^T M(s)) >= 0}, det F > 0, and it is
used only if sbar lies in int B_F.  Put X = F^T M(sbar) (any 2x2 matrix; F is recovered as
F^T = X M(sbar)^{-1}, and positive multiples of X give the same set).  Then

    A(s) := sym(F^T M(s)) = sym(X N(s)),  N(s) = M(sbar)^{-1} M(s),
    A(sbar + mu p) = sym(X) + mu sym(X N_p),  N_p = M(sbar)^{-1} M0(p),
    Z := sym(F^T E) = sym(X N_E),  N_E = M(sbar)^{-1} E,  E = [[1, 0], [0, 0]].

Fact 1 (Lemma 6(a) of the note).  If s is in B_F and v^T Z v >= 0 ("v is kept"), then
v^T A(s) v >= 0.  [s = lim (c_n + t_n e_w), c_n in C_F, t_n >= 0, A(c_n + t e_w) = A(c_n) + t Z.]

Box certificate (Lemma 15 of note.md).  A box is an axis-parallel box of parameters t; X(t) is affine in t.  For a ray
j with lam_hat_j > 0 and a rational vector v: if v^T Z v >= 0 and n := -v^T X N_j v > 0 at every
vertex of the box, put mu_j = max over the vertices of d / n with d := v^T X v.  For every X in
the box and every mu > mu_j, v^T A(sbar + mu p_j) v = d - mu n is affine in X and negative at all
vertices, hence negative on the box; by Fact 1, sbar + mu p_j is not in B_F.  So every member of
the family in the box has alpha_j <= mu_j, i.e. a_j >= 1/mu_j (if mu_j > 0).  The box is
certified ('cut') if sum_j lam_hat_j / mu_j >= 1 over the rays with such a certificate (other
rays contribute a_j >= 0).  A box is excluded ('excl') if some v is kept and has d < 0 at every
vertex: then sbar is not in B_F for any X in the box.  If every box of a cover of the parameter
domain is certified or excluded, every member of the family has a^T lam_hat >= 1, so lam_hat is
in the closure.

Kept-boundary bound (family BP only; Lemma 8 of the note).  For S > 0 the vector v = J S m,
m = M(sbar)^{-1} e_1, J = [[0, 1], [-1, 0]], satisfies v^T Z v = 0 (kept), v^T S v = det(S) m^T S m > 0,
and n_j(v) = -v^T S N_j v = det(S) L_j(S) with a linear form L_j (exact polynomial division, done
at setup).  Hence a_j >= L_j(S) / (m^T S m) for every S > 0; on a box with m^T S m > 0 at all
vertices the minimum of this linear-fractional function is attained at a vertex.  Unlike the
fixed-vector bound, this one is valid only for S > 0, which is exactly the family; it is what
makes boxes that straddle the boundary of the disk certifiable.

Parameter domains.
  BP (point rule, the transformations SCIP's rule can produce): X = S symmetric positive definite
     (F^T M(sbar) symmetric, sbar in int C_F); normalized to trace 1:
     S(u) = [[(1 + u1)/2, u2/2], [u2/2, (1 - u1)/2]], u in the open unit disk.  One chart
     [-1, 1]^2; boxes that do not meet the open disk are skipped ('skip', checked exactly).
  B  (all completions): by Lemma 7 of the note, det F > 0 and sbar in int B_F imply
     u^T S u > 0 for S = sym(X) and u = (1, -sbar_y).  With U = [u, e_2] (det U = 1) write
     U^T X U = [[t1, t2 + t4], [t2 - t4, t3]], so that t1 = u^T S u > 0.  Projectively,
     max_i |t_i| = 1; the charts are the facets t_i = +-1 of the cube [-1, 1]^4 intersected with
     t1 >= 0 (7 charts, each a 3-dimensional box; t1 in [0, 1] on the charts i != 1).

Search.  Boxes are processed first-in first-out; a box that is neither certified nor excluded is
bisected along its longest side (exact widths; ties to the lowest index).  Test vectors are
chosen in floating point (analytic candidates at the box centre, small rotations of them, and an
angular grid) and every condition is then checked in exact rational arithmetic.

Process hygiene: --time is an overall wall-clock limit; the state (queue, leaves) is saved
atomically to the checkpoint file every --ckpt seconds and at exit; --resume continues from it.

Usage:
  python3 box_cert.py INSTANCE FAMILY OUT.json [--time SEC] [--ckpt SEC] [--resume] [--charts i,j]
                      [--bpchart pq|u]
  (FAMILY = B or BP; OUT.json is the checkpoint and, when complete, the certificate)
Exit status 0 if the cover is complete (all leaves certified, excluded or skipped), 3 if the
time limit was reached (state saved), 4 if some box hit the depth limit.
"""
import sys, os, json, time, math, argparse
from fractions import Fraction as Fr
import numpy as np

INSTANCES = {
    # W-corner: sbar in the interior of the McCormick wedge {x >= 0, y <= 0, w >= 0}; rays e_x, -e_y,
    # e_w, -e_w (projections of the rays of a simplicial cone in R^4, Section 6 of the note).
    'wcorner': dict(sbar=['1', '-1', '1'], rays=[['1', '0', '0'], ['0', '-1', '0'], ['0', '0', '1'], ['0', '0', '-1']],
                    lam={'BP': ['6', '6', '0', '0']}),
    # Theorem 14 corner of the sfree note
    'thm14': dict(sbar=['-9/2', '0', '3/2'], verts=[['-1', '-6', '18'], ['-5', '6', '-18'], ['0', '5/2', '5/2']],
                  lam={'B': ['3/11', '41/99', '10/33'], 'BP': ['1/5', '0', '1/6']}),
    # Theorem 14 corner, points close to the numerical closure minimizers (tighter upper bounds)
    'thm14t': dict(sbar=['-9/2', '0', '3/2'], verts=[['-1', '-6', '18'], ['-5', '6', '-18'], ['0', '5/2', '5/2']],
                   lam={'B': ['67/250', '41/100', '151/500'], 'BP': ['51/350', '0', '17/150']}),
    # Theorem 14 corner, point near the closure minimizer for w = (11/20, 10^-6, 9/20) (factor estimate)
    'thm14w': dict(sbar=['-9/2', '0', '3/2'], verts=[['-1', '-6', '18'], ['-5', '6', '-18'], ['0', '5/2', '5/2']],
                   lam={'B': ['2211/10000', '8805/10000', '2464/10000']}),
    # Proposition 16 corner of the sfree note
    'prop16': dict(sbar=['-2', '3', '2'], verts=[['0', '0', '0'], ['6', '-2', '1/4'], ['1', '-5/2', '1/2']],
                   lam={'B': ['24/25', '1/100', '29/1000']}),
}

MAXDEPTH = 48


# ------------------------------------------------------------------ exact 2x2 helpers
def mm(A, B):
    return [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]


def inv2(A):
    d = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return [[A[1][1] / d, -A[0][1] / d], [-A[1][0] / d, A[0][0] / d]]


def Mex(s, h=1):
    x, y, w = s
    return [[w, x], [y, Fr(h)]]


def qf(v, X, W=None):
    """v^T X W v (W = I if None)"""
    Y = X if W is None else mm(X, W)
    return v[0] * (Y[0][0] * v[0] + Y[0][1] * v[1]) + v[1] * (Y[1][0] * v[0] + Y[1][1] * v[1])


def kept_boundary_forms(sbar, N):
    """[(L_j as dict over a, b, c), (m^T S m as dict)] with S = [[a, b], [b, c]] (exact, via sympy)"""
    import sympy as sp
    a, b, c = sp.symbols('a b c')
    S = sp.Matrix([[a, b], [b, c]]); J = sp.Matrix([[0, 1], [-1, 0]])
    Ms = sp.Matrix([[sp.Rational(str(sbar[2])), sp.Rational(str(sbar[0]))], [sp.Rational(str(sbar[1])), 1]])
    m = Ms.inv() * sp.Matrix([1, 0])
    v = J * S * m
    forms = []
    for Nj in N:
        Njs = sp.Matrix([[sp.Rational(str(x)) for x in row] for row in Nj])
        n = sp.expand(-(v.T * S * Njs * v)[0])
        q, r = sp.div(sp.Poly(n, a, b, c), sp.Poly(a * c - b ** 2, a, b, c))
        assert r.as_expr() == 0
        qq = sp.Poly(q.as_expr(), a, b, c)
        forms.append({k: Fr(str(qq.coeff_monomial(sym))) for k, sym in (('a', a), ('b', b), ('c', c))})
    den = sp.Poly(sp.expand((m.T * S * m)[0]), a, b, c)
    dform = {k: Fr(str(den.coeff_monomial(sym))) for k, sym in (('a', a), ('b', b), ('c', c))}
    return forms, dform


def lin(form, X):
    return form['a'] * X[0][0] + form['b'] * X[0][1] + form['c'] * X[1][1]


def setup(name, fam):
    inst = INSTANCES[name]
    sbar = [Fr(v) for v in inst['sbar']]
    if 'verts' in inst:
        P = [[Fr(vv[i]) - sbar[i] for i in range(3)] for vv in inst['verts']]
    else:
        P = [[Fr(v) for v in p] for p in inst['rays']]
    lam = [Fr(v) for v in inst['lam'][fam]]
    Msi = inv2(Mex(sbar))
    N = [mm(Msi, Mex(p, 0)) for p in P]
    NE = mm(Msi, [[Fr(1), Fr(0)], [Fr(0), Fr(0)]])
    return sbar, P, lam, N, NE


# ------------------------------------------------------------------ charts: t -> X (affine)
def charts(fam, sbar, bpchart='pq'):
    """List of charts: dict(id, dim, lo, hi, X0, Xi) with X(t) = X0 + sum_i t_i Xi (exact).
    BP, bpchart='u': one chart, S(u) = [[(1 + u1)/2, u2/2], [u2/2, (1 - u1)/2]], u in [-1, 1]^2;
        S(u) > 0 iff u1^2 + u2^2 < 1.
    BP, bpchart='pq': one chart, S(t) = [[(1 + t1 - t2)/2, (t1 + t2 - 1)/2], [(t1 + t2 - 1)/2, (1 - t1 + t2)/2]] (trace 1),
        t in [-1/2, 3/2]^2; S(t) > 0 iff (t1 - t2)^2 + (t1 + t2 - 1)^2 < 1.  (The coordinates
        t1 = S_11 + S_12, t2 = S_12 + S_22 make the planes S(1, 1)^T = 0 coordinate planes.)
    B:  U^T X U = [[t1, t2], [t3, t4]] with U = [[1, 0], [-sbar_y, 1]]; charts are the facets
        t_i = +-1 of [-1, 1]^4 with t1 >= 0 (t1 = u^T sym(X) u)."""
    h = Fr(1, 2)
    if fam == 'BP' and bpchart == 'u':
        X0 = [[h, Fr(0)], [Fr(0), h]]
        X1 = [[h, Fr(0)], [Fr(0), -h]]
        X2 = [[Fr(0), h], [h, Fr(0)]]
        return [dict(id='disk', dim=2, lo=[Fr(-1)] * 2, hi=[Fr(1)] * 2, X0=X0, Xi=[X1, X2])]
    if fam == 'BP':
        X0 = [[h, -h], [-h, h]]
        X1 = [[h, h], [h, -h]]
        X2 = [[-h, h], [h, h]]
        return [dict(id='trace1', dim=2, lo=[Fr(-1, 2)] * 2, hi=[Fr(3, 2)] * 2, X0=X0, Xi=[X1, X2])]
    sy = sbar[1]
    Ui = inv2([[Fr(1), Fr(0)], [-sy, Fr(1)]])
    UiT = [[Ui[0][0], Ui[1][0]], [Ui[0][1], Ui[1][1]]]
    E = [[[1, 0], [0, 0]], [[0, 1], [0, 0]], [[0, 0], [1, 0]], [[0, 0], [0, 1]]]
    basis = [mm(mm(UiT, [[Fr(a) for a in r] for r in Bm]), Ui) for Bm in E]
    out = []
    for i in range(4):
        for sg in ((1,) if i == 0 else (1, -1)):
            free = [k for k in range(4) if k != i]
            X0 = [[sg * basis[i][r][c] for c in range(2)] for r in range(2)]
            lo = [Fr(0) if k == 0 else Fr(-1) for k in free]
            hi = [Fr(1)] * 3
            out.append(dict(id='t%d=%+d' % (i + 1, sg), dim=3, lo=lo, hi=hi, X0=X0, Xi=[basis[k] for k in free]))
    return out


def X_at(ch, t):
    X = [[ch['X0'][r][c] for c in range(2)] for r in range(2)]
    for ti, Xi in zip(t, ch['Xi']):
        if ti != 0:
            for r in range(2):
                for c in range(2):
                    X[r][c] += ti * Xi[r][c]
    return X


def vertices(lo, hi):
    d = len(lo)
    for mask in range(1 << d):
        yield [hi[k] if (mask >> k) & 1 else lo[k] for k in range(d)]


def box_meets_open_disk_u(lo, hi):
    """exact: min over the box of u1^2 + u2^2 < 1"""
    x = [min(max(Fr(0), lo[i]), hi[i]) for i in range(2)]
    return x[0] ** 2 + x[1] ** 2 < 1


def box_meets_open_disk(lo, hi):
    """exact: min over the box of F(t) = (t1 - t2)^2 + (t1 + t2 - 1)^2 < 1 (BP trace-one chart).
    F = 2 (t1 - 1/2)^2 + 2 (t2 - 1/2)^2 is separable, so the minimizer over the box clamps each
    coordinate to [lo_i, hi_i] separately."""
    x = [min(max(Fr(1, 2), lo[i]), hi[i]) for i in range(2)]
    return 2 * (x[0] - Fr(1, 2)) ** 2 + 2 * (x[1] - Fr(1, 2)) ** 2 < 1


# ------------------------------------------------------------------ floating-point candidates
def fl(X):
    return np.array([[float(X[0][0]), float(X[0][1])], [float(X[1][0]), float(X[1][1])]])


ANG = np.linspace(0, np.pi, 181)[:-1]
GRID = np.stack([np.cos(ANG), np.sin(ANG)], axis=1)


def candidates(Xc, Nj, NEf):
    """unit vectors: generalized eigenvectors of (S, A_j), isotropic directions of Z, small rotations,
    and an angular grid"""
    S = 0.5 * (Xc + Xc.T)
    A = Xc @ Nj; A = 0.5 * (A + A.T)
    Z = Xc @ NEf; Z = 0.5 * (Z + Z.T)
    base = []
    try:
        w, V = np.linalg.eig(np.linalg.solve(S, -A)) if abs(np.linalg.det(S)) > 1e-14 else (None, None)
        if V is not None:
            for k in range(2):
                if abs(np.imag(w[k])) < 1e-12:
                    base.append(np.real(V[:, k]))
    except np.linalg.LinAlgError:
        pass
    a, b, c = Z[0, 0], Z[0, 1], Z[1, 1]
    if abs(a) > 1e-15:
        disc = b * b - a * c
        if disc >= 0:
            for sg in (1, -1):
                base.append(np.array([(-b + sg * math.sqrt(disc)) / a, 1.0]))
    else:
        base.append(np.array([1.0, 0.0]))
        if abs(c) > 1e-15:
            base.append(np.array([c, -2 * b]))
    out = []
    for v in base:
        nv = np.linalg.norm(v)
        if nv == 0:
            continue
        th = math.atan2(v[1], v[0])
        for dth in (0.0, 1e-4, -1e-4, 1e-3, -1e-3, 1e-2, -1e-2, 3e-2, -3e-2):
            out.append(np.array([math.cos(th + dth), math.sin(th + dth)]))
    return np.vstack(out + [GRID]) if out else GRID


def best_float(Xv, Nj, NEf, cand):
    """per candidate: float lower bound 1/mu over the box (0 if invalid)"""
    V = cand
    best = (0.0, None)
    nvert = len(Xv)
    ok = np.ones(len(V), bool)
    mu = np.full(len(V), -np.inf)
    for X in Xv:
        K = np.einsum('ki,ij,kj->k', V, X @ NEf, V)
        d = np.einsum('ki,ij,kj->k', V, X, V)
        n = -np.einsum('ki,ij,kj->k', V, X @ Nj, V)
        ok &= (K >= -1e-12) & (n > 1e-15)
        with np.errstate(divide='ignore', invalid='ignore'):
            mu = np.maximum(mu, np.where(n > 0, d / n, np.inf))
    val = np.where(ok & (mu > 0), 1.0 / np.where(mu > 0, mu, 1), 0.0)
    k = int(np.argmax(val))
    return val[k], V[k]


def excl_float(Xv, NEf, cand):
    """candidate kept at all vertices with v^T X v < 0 at all vertices (float pre-check)"""
    ok = np.ones(len(cand), bool)
    for X in Xv:
        K = np.einsum('ki,ij,kj->k', cand, X @ NEf, cand)
        d = np.einsum('ki,ij,kj->k', cand, X, cand)
        ok &= (K >= -1e-12) & (d < -1e-15)
    idx = np.nonzero(ok)[0]
    return cand[idx[0]] if len(idx) else None


def rat(v, den=10 ** 6):
    s = max(abs(v[0]), abs(v[1]))
    return [Fr(float(v[0] / s)).limit_denominator(den), Fr(float(v[1] / s)).limit_denominator(den)]


# ------------------------------------------------------------------ exact checks
def exact_ray(Xv_ex, Nj, NE, v):
    """mu_j (Fraction) if v is a valid certificate for the ray on the box, else None"""
    mu = None
    for X in Xv_ex:
        if qf(v, X, NE) < 0:
            return None
        n = -qf(v, X, Nj)
        if n <= 0:
            return None
        r = qf(v, X) / n
        mu = r if mu is None or r > mu else mu
    return mu


def exact_excl(Xv_ex, NE, v):
    return all(qf(v, X, NE) >= 0 and qf(v, X) < 0 for X in Xv_ex)


def process_box(ch, lo, hi, lam, N, NE, Nf, NEf, act, kb=None):
    """returns a leaf record or None (split)"""
    if ch['id'] == 'trace1' and not box_meets_open_disk(lo, hi):
        return dict(type='skip')
    if ch['id'] == 'disk' and not box_meets_open_disk_u(lo, hi):
        return dict(type='skip')
    Xv_ex = [X_at(ch, t) for t in vertices(lo, hi)]
    Xv = [fl(X) for X in Xv_ex]
    tc = [(a + b) / 2 for a, b in zip(lo, hi)]
    Xc = fl(X_at(ch, tc))
    # exclusion first (cheap)
    cand_e = candidates(Xc, Nf[act[0]], NEf)
    ve = excl_float(Xv, NEf, cand_e)
    if ve is not None:
        v = rat(ve)
        if exact_excl(Xv_ex, NE, v):
            return dict(type='excl', v=[str(x) for x in v])
    # kept-boundary bounds (exact; BP only)
    kbval = {}
    if kb is not None:
        forms, dform = kb
        dens = [lin(dform, X) for X in Xv_ex]
        if all(d > 0 for d in dens):
            for j in act:
                vals = [lin(forms[j], X) / d for X, d in zip(Xv_ex, dens)]
                mn = min(vals)
                if mn > 0:
                    kbval[j] = mn
    total_f = 0.0
    picks = {}
    for j in act:
        cand = candidates(Xc, Nf[j], NEf)
        val, v = best_float(Xv, Nf[j], NEf, cand)
        kv = float(kbval.get(j, 0))
        if val > kv:
            picks[j] = v
        total_f += float(lam[j]) * max(val, kv)
    if total_f < 1 - 1e-9:
        return None
    total = Fr(0)
    vs = {}
    used_kb = []
    for j in act:
        best = kbval.get(j, Fr(0)); how = 'kb' if j in kbval else None
        if j in picks:
            v = rat(picks[j])
            mu = exact_ray(Xv_ex, N[j], NE, v)
            if mu is not None and mu > 0 and 1 / mu > best:
                best = 1 / mu; how = v
        if how is not None:
            total += lam[j] * best
            if how == 'kb':
                used_kb.append(j)
            else:
                vs[j] = how
    if total >= 1:
        return dict(type='cut', v={str(j): [str(x) for x in v] for j, v in vs.items()}, kb=[str(j) for j in used_kb])
    return None


def split(lo, hi):
    w = [b - a for a, b in zip(lo, hi)]
    k = max(range(len(w)), key=lambda i: (w[i], -i))
    mid = (lo[k] + hi[k]) / 2
    lo2 = list(lo); lo2[k] = mid
    hi1 = list(hi); hi1[k] = mid
    return (lo, hi1), (lo2, hi)


# ------------------------------------------------------------------ driver with checkpoints
def save(path, state):
    tmp = path + '.tmp'
    with open(tmp, 'w') as fh:
        json.dump(state, fh)
    os.replace(tmp, path)


def enc(b):
    return [str(x) for x in b]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('instance'); ap.add_argument('family'); ap.add_argument('out')
    ap.add_argument('--time', type=float, default=3600.0)
    ap.add_argument('--ckpt', type=float, default=60.0)
    ap.add_argument('--resume', action='store_true')
    ap.add_argument('--charts', default=None)
    ap.add_argument('--bpchart', default='pq', choices=['pq', 'u'])
    args = ap.parse_args()
    sbar, P, lam, N, NE = setup(args.instance, args.family)
    act = [j for j in range(len(lam)) if lam[j] > 0]
    Nf = [fl(M) for M in N]; NEf = fl(NE)
    chs = charts(args.family, sbar, args.bpchart)
    kb = kept_boundary_forms(sbar, N) if args.family == 'BP' else None
    use = list(range(len(chs))) if args.charts is None else [int(c) for c in args.charts.split(',')]
    t0 = time.time()
    if args.resume and os.path.exists(args.out):
        st = json.load(open(args.out))
        assert st['instance'] == args.instance and st['family'] == args.family
        queue = [(q[0], [Fr(x) for x in q[1]], [Fr(x) for x in q[2]], q[3]) for q in st['queue']]
        leaves = st['leaves']
        elapsed0 = st.get('elapsed', 0.0)
        stats = st['stats']
        print('resumed: %d queued, %d leaves, %.0f s used before' % (len(queue), len(leaves), elapsed0), flush=True)
    else:
        queue = [(c, list(chs[c]['lo']), list(chs[c]['hi']), 0) for c in use]
        leaves = []
        elapsed0 = 0.0
        stats = dict(cut=0, excl=0, skip=0, unresolved=0, processed=0)
    st = dict(instance=args.instance, family=args.family, sbar=enc(sbar), rays=[enc(p) for p in P], lam=enc(lam),
              charts=[c['id'] for c in chs], used_charts=use, maxdepth=MAXDEPTH, bpchart=args.bpchart,
              code='box_cert.py')
    last = time.time()

    def dump(status):
        st.update(queue=[(q[0], enc(q[1]), enc(q[2]), q[3]) for q in queue], leaves=leaves, stats=stats,
                  elapsed=elapsed0 + time.time() - t0, status=status)
        save(args.out, st)

    status = 'complete'
    while queue:
        if elapsed0 + time.time() - t0 > args.time:
            status = 'incomplete: time limit'
            break
        c, lo, hi, depth = queue.pop(0)
        rec = process_box(chs[c], lo, hi, lam, N, NE, Nf, NEf, act, kb)
        stats['processed'] += 1
        if rec is not None:
            rec.update(chart=c, lo=enc(lo), hi=enc(hi), depth=depth)
            leaves.append(rec)
            stats[rec['type']] += 1
        elif depth >= MAXDEPTH:
            leaves.append(dict(type='unresolved', chart=c, lo=enc(lo), hi=enc(hi), depth=depth))
            stats['unresolved'] += 1
        else:
            for (a, b) in split(lo, hi):
                queue.append((c, a, b, depth + 1))
        if time.time() - last > args.ckpt:
            dump('running')
            last = time.time()
            print('  %.0f s: processed %d, queue %d, %s' % (elapsed0 + time.time() - t0, stats['processed'],
                                                            len(queue), {k: v for k, v in stats.items() if k != 'processed'}), flush=True)
    if status == 'complete' and stats['unresolved'] > 0:
        status = 'incomplete: depth limit'
    dump(status)
    print('status: %s; %s; %.1f s' % (status, stats, elapsed0 + time.time() - t0), flush=True)
    sys.exit(0 if status == 'complete' else (3 if 'time' in status else 4))


if __name__ == '__main__':
    main()
