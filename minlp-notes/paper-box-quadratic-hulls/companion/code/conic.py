"""Small conic modeling layer with Clarabel and SCS back ends and a safe dual bound.

A model has scalar variables x (all with known valid bounds lo <= x <= hi) and
cone constraints on affine expressions.  An affine expression is a pair
(dict var->coef, constant).  Supported cones: zero (equalities), nonnegative,
second-order (t, u) with ||u|| <= t, and PSD blocks given as symmetric matrices
of affine expressions.

Both solvers use the form  min q'x  s.t.  A x + s = b,  s in K.
For an expression e(x) = c + a'x that must lie in K we store the row
A = -a, b = c, so that s = b - A x = e(x).

Safe bound (Jansson style).  For any z' in K* and any feasible x,
    q'x = (q + A'z')'x - b'z' + z''s >= -b'z' + sum_i min(r_i lo_i, r_i hi_i),
with r = q + A'z'.  We project the solver dual onto K* (all cones here are
self-dual), shift PSD blocks slightly to absorb eigen-decomposition error, and
subtract a priori floating-point error bounds.  The bound is valid for every
feasible point of the model as built, provided lo/hi are valid bounds for all
feasible points (callers must ensure this; see relax.py).
"""

import time
import numpy as np
import scipy.sparse as sp

SQ2 = np.sqrt(2.0)


def aff(d=None, c=0.0):
    return (dict(d) if d else {}, float(c))


def add_aff(*terms):
    """Linear combination: terms are (coef, expr)."""
    out = {}
    const = 0.0
    for coef, (d, c) in terms:
        if coef == 0:
            continue
        const += coef * c
        for k, v in d.items():
            out[k] = out.get(k, 0.0) + coef * v
    return (out, const)


class Model:
    def __init__(self):
        self.nvar = 0
        self.lo = []
        self.hi = []
        self.names = []
        self.zero = []      # list of expressions
        self.nonneg = []    # list of expressions
        self.soc = []       # list of lists of expressions (t first)
        self.psd = []       # list of (k, list of upper-triangular entries by (i,j))
        self.q = {}         # objective coefficients
        self.qconst = 0.0
        self.tags = {}      # counts by tag for size reporting

    def var(self, lo, hi, name=None):
        i = self.nvar
        self.nvar += 1
        self.lo.append(float(lo))
        self.hi.append(float(hi))
        self.names.append(name)
        return i

    def _tag(self, tag, key, k=1):
        if tag is None:
            return
        d = self.tags.setdefault(tag, {})
        d[key] = d.get(key, 0) + k

    def add_eq(self, e, tag=None):
        self.zero.append(e)
        self._tag(tag, 'eq')

    def add_ge(self, e, tag=None):
        """e(x) >= 0"""
        self.nonneg.append(e)
        self._tag(tag, 'lin')

    def add_soc(self, exprs, tag=None):
        self.soc.append(list(exprs))
        self._tag(tag, 'soc%d' % len(exprs))

    def add_rsoc(self, u, v, w, tag=None):
        """u*v >= w^2, u, v >= 0  as  ||(u-v, 2w)|| <= u+v."""
        self.add_soc([add_aff((1, u), (1, v)), add_aff((1, u), (-1, v)), add_aff((2, w))], tag)

    def add_psd(self, mat, tag=None):
        """mat: k x k nested list of expressions (only upper triangle read)."""
        k = len(mat)
        if k == 1:
            self.add_ge(mat[0][0], tag)
            return
        self.psd.append((k, [[mat[i][j] if i <= j else None for j in range(k)] for i in range(k)]))
        self._tag(tag, 'psd%d' % k)

    def set_obj(self, d, c=0.0):
        self.q = dict(d)
        self.qconst = float(c)

    # ------------------------------------------------------------------
    def size_summary(self):
        s = {'vars': self.nvar, 'eq': len(self.zero), 'lin': len(self.nonneg), 'soc': len(self.soc)}
        orders = {}
        for k, _ in self.psd:
            orders[k] = orders.get(k, 0) + 1
        s['psd'] = {str(k): v for k, v in sorted(orders.items())}
        s['psd_svec'] = sum(k * (k + 1) // 2 for k, _ in self.psd)
        return s

    def build(self, solver):
        """Return (A csc, b, q, cone spec list, psd order list)."""
        rows, cols, vals, b = [], [], [], []
        r = 0

        def put(e, scale=1.0):
            nonlocal r
            d, c = e
            for k, v in d.items():
                if v != 0.0:
                    rows.append(r)
                    cols.append(k)
                    vals.append(-v * scale)
            b.append(c * scale)
            r += 1

        cones = []
        for e in self.zero:
            put(e)
        cones.append(('z', len(self.zero)))
        for e in self.nonneg:
            put(e)
        cones.append(('l', len(self.nonneg)))
        for es in self.soc:
            for e in es:
                put(e)
            cones.append(('q', len(es)))
        for k, mat in self.psd:
            for (i, j) in _orders(k, solver):
                put(mat[i][j], 1.0 if i == j else SQ2)
            cones.append(('s', k))
        A = sp.csc_matrix((vals, (rows, cols)), shape=(r, self.nvar))
        q = np.zeros(self.nvar)
        for k, v in self.q.items():
            q[k] += v
        return A, np.array(b), q, cones

    # ------------------------------------------------------------------
    def solve(self, solver='clarabel', tol=1e-8, max_iter=200, verbose=False, scs_eps=1e-6,
              time_limit=None, scs_max_iters=200000):
        t0 = time.time()
        A, b, q, cones = self.build(solver)
        tbuild = time.time() - t0
        t1 = time.time()
        if solver == 'clarabel':
            import clarabel
            ccones = []
            for kind, k in cones:
                if kind == 'z':
                    if k:
                        ccones.append(clarabel.ZeroConeT(k))
                elif kind == 'l':
                    if k:
                        ccones.append(clarabel.NonnegativeConeT(k))
                elif kind == 'q':
                    ccones.append(clarabel.SecondOrderConeT(k))
                elif kind == 's':
                    ccones.append(clarabel.PSDTriangleConeT(k))
            st = clarabel.DefaultSettings()
            st.verbose = verbose
            st.tol_gap_abs = tol
            st.tol_gap_rel = tol
            st.tol_feas = tol
            st.max_iter = max_iter
            st.max_threads = 1
            if time_limit:
                st.time_limit = time_limit
            P = sp.csc_matrix((self.nvar, self.nvar))
            solver_obj = clarabel.DefaultSolver(P, q, A, b, ccones, st)
            sol = solver_obj.solve()
            x = np.array(sol.x)
            z = np.array(sol.z)
            status = str(sol.status)
            iters = sol.iterations
            pobj = sol.obj_val
            dobj = sol.obj_val_dual
        else:
            import scs
            dims = {'z': 0, 'l': 0, 'q': [], 's': []}
            for kind, k in cones:
                if kind == 'z':
                    dims['z'] = k
                elif kind == 'l':
                    dims['l'] = k
                elif kind == 'q':
                    dims['q'].append(k)
                elif kind == 's':
                    dims['s'].append(k)
            data = {'A': A, 'b': b, 'c': q}
            solver_obj = scs.SCS(data, dims, eps_abs=scs_eps, eps_rel=scs_eps, verbose=verbose,
                                 max_iters=scs_max_iters, acceleration_lookback=10,
                                 **({'time_limit_secs': time_limit} if time_limit else {}))
            sol = solver_obj.solve()
            x = sol['x']
            z = sol['y']
            status = sol['info']['status']
            iters = sol['info']['iter']
            pobj = sol['info']['pobj']
            dobj = sol['info']['dobj']
        tsolve = time.time() - t1
        res = {
            'solver': solver, 'status': status, 'iters': int(iters),
            'pobj': float(pobj) + self.qconst, 'dobj': float(dobj) + self.qconst,
            'time_build': tbuild, 'time_solve': tsolve, 'x': x, 'z': z,
        }
        res['safe'] = safe_bound(A, b, q, cones, z, np.array(self.lo), np.array(self.hi), solver) + self.qconst
        # primal residual of cone constraints at x (max violation, scaled)
        res['pinf'] = primal_violation(A, b, cones, x, solver)
        return res


# ----------------------------------------------------------------------
def _svec_to_mat(v, k, solver_order):
    M = np.zeros((k, k))
    for t, (i, j) in enumerate(solver_order):
        if i == j:
            M[i, i] = v[t]
        else:
            M[i, j] = M[j, i] = v[t] / SQ2
    return M


def _mat_to_svec(M, solver_order):
    return np.array([M[i, j] if i == j else M[i, j] * SQ2 for (i, j) in solver_order])


def _orders(k, solver):
    if solver == 'clarabel':   # upper triangle, column-wise
        return [(i, j) for j in range(k) for i in range(j + 1)]
    return [(i, j) for i in range(k) for j in range(i, k)]   # SCS lower column-wise


def project_dual(z, cones, solver, shift=True):
    """Project z onto K* blockwise (cones are self-dual; zero-cone dual is free)."""
    zp = z.copy()
    pos = 0
    for kind, k in cones:
        if kind == 'z':
            pos += k
        elif kind == 'l':
            zp[pos:pos + k] = np.maximum(z[pos:pos + k], 0.0)
            pos += k
        elif kind == 'q':
            t, u = z[pos], z[pos + 1:pos + k]
            nu = np.linalg.norm(u)
            if nu <= t:
                pass
            elif nu <= -t:
                zp[pos:pos + k] = 0.0
            else:
                a = (t + nu) / 2.0
                zp[pos] = a
                zp[pos + 1:pos + k] = a * u / nu
            # make strictly inside by a tiny margin to absorb rounding
            zp[pos] += 4e-16 * (abs(zp[pos]) + np.linalg.norm(zp[pos + 1:pos + k])) * k
            pos += k
        elif kind == 's':
            n = k * (k + 1) // 2
            order = _orders(k, solver)
            M = _svec_to_mat(z[pos:pos + n], k, order)
            w, V = np.linalg.eigh(M)
            wp = np.maximum(w, 0.0)
            Mp = (V * wp) @ V.T
            if shift:
                # Weyl: eigh backward error and reconstruction error are O(k*u*||M||).
                Mp += np.eye(k) * (64 * k * 2.2e-16 * max(1.0, np.abs(w).max()))
            zp[pos:pos + n] = _mat_to_svec(Mp, order)
            pos += n
    return zp


def safe_bound(A, b, q, cones, z, lo, hi, solver):
    zp = project_dual(z, cones, solver)
    r = q + A.T @ zp
    # a priori rounding error for r and b'z' (generous constant)
    absA = abs(A)
    err_r = 1e-14 * (absA.T @ np.abs(zp) + np.abs(q))
    val = -float(b @ zp) - 1e-14 * float(np.abs(b) @ np.abs(zp))
    lo_r = np.minimum(r * lo, r * hi)
    width = np.maximum(np.abs(lo), np.abs(hi))
    val += float(lo_r.sum()) - float((err_r * width).sum()) - 1e-14 * float(np.abs(lo_r).sum())
    return val


def primal_violation(A, b, cones, x, solver):
    s = b - A @ x
    worst = 0.0
    pos = 0
    for kind, k in cones:
        if kind == 'z':
            if k:
                worst = max(worst, np.abs(s[pos:pos + k]).max())
            pos += k
        elif kind == 'l':
            if k:
                worst = max(worst, max(0.0, -s[pos:pos + k].min()))
            pos += k
        elif kind == 'q':
            worst = max(worst, max(0.0, np.linalg.norm(s[pos + 1:pos + k]) - s[pos]))
            pos += k
        elif kind == 's':
            n = k * (k + 1) // 2
            M = _svec_to_mat(s[pos:pos + n], k, _orders(k, solver))
            worst = max(worst, max(0.0, -np.linalg.eigvalsh(M)[0]))
            pos += n
    return worst
