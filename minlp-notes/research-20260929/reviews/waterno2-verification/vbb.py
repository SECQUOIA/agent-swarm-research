"""Verifier's rigorous branch and bound for one period subproblem of waterno2_T.

Independent of the authors' rbb.py.  Differences in method:
  * all certificate arithmetic is EXACT rational (fractions.Fraction):
    - bound propagation (FBBT) computes every new bound exactly and then rounds
      it outward to a double (checked with Fraction comparisons);
    - square and cube roots are rounded outward and checked by exact squaring /
      cubing;
    - relaxation rows have exact rational coefficients (tangent w >= 2p x - p^2,
      w >= 3p^2 x - 2p^3, secants through the exact box corners, McCormick);
    - the node bound is min_{box} (c + A^T y) z - y.b evaluated exactly for the
      LP dual vector y (y clamped to >= 0 on <= rows); HiGHS only supplies y.
  * tangent points: box ends and quartiles; branching point: LP value clipped
    to the middle half of the interval; no reduced-cost tightening; root OBBT
    without objective cutoff (optional).
A node is discarded only if (a) exact propagation proves it empty, or (b) its
exact bound is >= target.  Result: phi >= min(target, bounds of open nodes).

usage: python3 vbb.py T t multipliers.json target [node_limit] [time_limit] [extra_bounds.json]
"""
import heapq
import json
import math
import sys
import time
from fractions import Fraction as F

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

import vmodel

INF = math.inf


# ---------------------------------------------------------------- rounding
def fdn(q):
    f = float(q)
    if F(f) > q:
        f = math.nextafter(f, -INF)
    return f


def fup(q):
    f = float(q)
    if F(f) < q:
        f = math.nextafter(f, INF)
    return f


def sqrt_dn(q):
    if q <= 0:
        return 0.0
    s = math.sqrt(float(q))
    while s > 0 and F(s) ** 2 > q:
        s = math.nextafter(s, -INF)
    return s


def sqrt_up(q):
    if q <= 0:
        return 0.0
    s = math.sqrt(float(q))
    while F(s) ** 2 < q:
        s = math.nextafter(s, INF)
    return s


def cbrt_dn(q):
    if q < 0:
        return -cbrt_up(-q)
    s = float(q) ** (1.0 / 3.0)
    while s > 0 and F(s) ** 3 > q:
        s = math.nextafter(s, -INF)
    return s


def cbrt_up(q):
    if q < 0:
        return -cbrt_dn(-q)
    s = float(q) ** (1.0 / 3.0)
    while F(s) ** 3 < q:
        s = math.nextafter(s, INF)
    return s


def fin(x):
    return x not in (INF, -INF)


# ---------------------------------------------------------------- problem
class Period:
    def __init__(self, T, t, lam, mu, extra=None, full=False):
        """full=True: all variables and all rows except the horizon row
        (used for implied bounds); the objective is then zero."""
        I = vmodel.instance(T)
        m = I["m"]
        gv = I["per_vars"][t] if not full else sorted(v for vs in I["per_vars"] for v in vs)
        rowlist = I["per_rows"][t] if not full else sorted(
            [i for rs in I["per_rows"] for i in rs] + [i for lk in I["links"] for (i, a, b) in lk])
        loc = {v: k for k, v in enumerate(gv)}
        self.names = [m["names"][v] for v in gv]
        n0 = len(gv)
        lo, hi = [], []
        for v in gv:
            lo.append(-INF if m["lb"][v].upper() == "-INF" else fdn(F(m["lb"][v])))
            hi.append(INF if m["ub"][v].upper() in ("INF", "+INF") else fup(F(m["ub"][v])))
        isbin = [m["vt"][v] == "B" for v in gv]
        for name, (a, b) in (extra or {}).items():
            if name in self.names:
                k = self.names.index(name)
                lo[k] = max(lo[k], fdn(F(a)))
                hi[k] = min(hi[k], fup(F(b)))
        mons = {}
        rows = []
        for i in rowlist:
            c = m["cons"][i]
            p = vmodel.poly(c)
            cols, cf = [], []
            for mono, a in p.items():
                if len(mono) == 1:
                    col = loc[mono[0]]
                else:
                    key = tuple(sorted(loc[v] for v in mono))
                    if key not in mons:
                        mons[key] = n0 + len(mons)
                    col = mons[key]
                cols.append(col)
                cf.append(a)
            L = None if c["lb"].upper() == "-INF" else F(c["lb"])
            U = None if c["ub"].upper() in ("INF", "+INF") else F(c["ub"])
            rows.append((cols, cf, L, U, c["name"]))
        aux = []
        for key, w in sorted(mons.items(), key=lambda kv: kv[1]):
            if len(key) == 2 and key[0] == key[1]:
                aux.append(("sq", key[0], None, w))
            elif len(key) == 3 and len(set(key)) == 1:
                aux.append(("cube", key[0], None, w))
            elif len(key) == 2:
                aux.append(("bil", key[0], key[1], w))
            else:
                raise NotImplementedError(key)
        self.n0, self.n = n0, n0 + len(aux)
        self.aux, self.rows = aux, rows
        self.lo0 = lo + [-INF] * len(aux)
        self.hi0 = hi + [INF] * len(aux)
        self.isbin = isbin + [False] * len(aux)
        cobj = vmodel.period_objective(I, t, lam, mu) if not full else {}
        self.c = [F(0)] * self.n
        for v, a in cobj.items():
            self.c[loc[v]] = a
        self.cf = np.array([float(a) for a in self.c])
        assert all(float(a) == a for a in self.c)  # objective coefficients are doubles
        # static LP rows (exact):  a.z <= b  or  a.z = b
        st = []
        for (cols, cf, L, U, nm) in rows:
            if L is not None and U is not None and L == U:
                st.append((cols, cf, L, True))
            else:
                if U is not None:
                    st.append((cols, cf, U, False))
                if L is not None:
                    st.append((cols, [-a for a in cf], -L, False))
        self.static = st

    # ------------------------------------------------------------ FBBT
    def fbbt(self, lo, hi, maxrounds=30):
        lo, hi = list(lo), list(hi)
        for _ in range(maxrounds):
            olo, ohi = lo[:], hi[:]
            if not self._rows(lo, hi):
                return None
            if not self._mons(lo, hi):
                return None
            for j in range(self.n0):
                if self.isbin[j]:
                    if lo[j] > 0:
                        lo[j] = 1.0
                    if hi[j] < 1:
                        hi[j] = 0.0
                    if lo[j] > hi[j]:
                        return None
            big = False
            for j in range(self.n):
                w = hi[j] - lo[j] if fin(hi[j]) and fin(lo[j]) else INF
                d1 = lo[j] - olo[j] if fin(olo[j]) else (INF if fin(lo[j]) else 0.0)
                d2 = ohi[j] - hi[j] if fin(ohi[j]) else (INF if fin(hi[j]) else 0.0)
                if max(d1, d2) > 1e-3 * min(w, 1.0) + 1e-12:
                    big = True
                    break
            if not big:
                break
        return lo, hi

    def _rows(self, lo, hi):
        for (cols, cf, L, U, nm) in self.rows:
            tl, th = [], []
            nli = nhi = 0
            sl = sh = F(0)
            for col, a in zip(cols, cf):
                l, h = lo[col], hi[col]
                if a > 0:
                    x1 = a * F(l) if fin(l) else None
                    x2 = a * F(h) if fin(h) else None
                else:
                    x1 = a * F(h) if fin(h) else None
                    x2 = a * F(l) if fin(l) else None
                tl.append(x1)
                th.append(x2)
                if x1 is None:
                    nli += 1
                else:
                    sl += x1
                if x2 is None:
                    nhi += 1
                else:
                    sh += x2
            if U is not None and nli == 0 and sl > U:
                return False
            if L is not None and nhi == 0 and sh < L:
                return False
            for k, (col, a) in enumerate(zip(cols, cf)):
                # others' low/high
                if tl[k] is None:
                    ol = sl if nli == 1 else None
                else:
                    ol = sl - tl[k] if nli == 0 else None
                if th[k] is None:
                    oh = sh if nhi == 1 else None
                else:
                    oh = sh - th[k] if nhi == 0 else None
                # a*z in [L - oh, U - ol]
                qlo = (L - oh) if (L is not None and oh is not None) else None
                qhi = (U - ol) if (U is not None and ol is not None) else None
                if a > 0:
                    zl = qlo / a if qlo is not None else None
                    zh = qhi / a if qhi is not None else None
                else:
                    zl = qhi / a if qhi is not None else None
                    zh = qlo / a if qlo is not None else None
                if zl is not None:
                    f = fdn(zl)
                    if f > lo[col]:
                        lo[col] = f
                if zh is not None:
                    f = fup(zh)
                    if f < hi[col]:
                        hi[col] = f
                if lo[col] > hi[col]:
                    return False
        return True

    def _mons(self, lo, hi):
        for (kind, x, y, w) in self.aux:
            if kind == "sq":
                l, h = lo[x], hi[x]
                if fin(l) and fin(h):
                    L2, H2 = F(l) ** 2, F(h) ** 2
                    if l >= 0:
                        a, b = L2, H2
                    elif h <= 0:
                        a, b = H2, L2
                    else:
                        a, b = F(0), max(L2, H2)
                    lo[w] = max(lo[w], fdn(a))
                    hi[w] = min(hi[w], fup(b))
                else:
                    lo[w] = max(lo[w], 0.0)
                if lo[w] > hi[w]:
                    return False
                if fin(hi[w]):
                    r = sqrt_up(F(hi[w]))
                    lo[x] = max(lo[x], -r)
                    hi[x] = min(hi[x], r)
                if lo[w] > 0:
                    s = sqrt_dn(F(lo[w]))
                    if lo[x] > -s:
                        lo[x] = max(lo[x], s)
                    elif hi[x] < s:
                        hi[x] = min(hi[x], -s)
                if lo[x] > hi[x]:
                    return False
            elif kind == "cube":
                l, h = lo[x], hi[x]
                if fin(l):
                    lo[w] = max(lo[w], fdn(F(l) ** 3))
                if fin(h):
                    hi[w] = min(hi[w], fup(F(h) ** 3))
                if lo[w] > hi[w]:
                    return False
                if fin(lo[w]):
                    lo[x] = max(lo[x], cbrt_dn(F(lo[w])))
                if fin(hi[w]):
                    hi[x] = min(hi[x], cbrt_up(F(hi[w])))
                if lo[x] > hi[x]:
                    return False
            else:
                lx, hx, ly, hy = lo[x], hi[x], lo[y], hi[y]
                if fin(lx) and fin(hx) and fin(ly) and fin(hy):
                    p = [F(lx) * F(ly), F(lx) * F(hy), F(hx) * F(ly), F(hx) * F(hy)]
                    lo[w] = max(lo[w], fdn(min(p)))
                    hi[w] = min(hi[w], fup(max(p)))
                if lo[w] > hi[w]:
                    return False
                if fin(lo[w]) and fin(hi[w]):
                    for (p_, q_) in ((x, y), (y, x)):
                        ql, qh = lo[q_], hi[q_]
                        if fin(ql) and fin(qh) and (ql > 0 or qh < 0):
                            Wl, Wh = F(lo[w]), F(hi[w])
                            cand = [Wl / F(ql), Wl / F(qh), Wh / F(ql), Wh / F(qh)]
                            lo[p_] = max(lo[p_], fdn(min(cand)))
                            hi[p_] = min(hi[p_], fup(max(cand)))
                            if lo[p_] > hi[p_]:
                                return False
        return True

    # ------------------------------------------------------------ relaxation
    def relax_rows(self, lo, hi):
        """Exact rows a.z <= b valid for every point of the box satisfying the
        monomial definitions."""
        R = []
        for (kind, x, y, w) in self.aux:
            if kind in ("sq", "cube"):
                l, h = F(lo[x]), F(hi[x])
                pts = sorted({l, h, (3 * l + h) / 4, (l + h) / 2, (l + 3 * h) / 4})
                # snap interior points to doubles (keeps the numbers short)
                pts = sorted({F(float(p)) for p in pts} | {l, h})
                if kind == "sq":
                    for p in pts:  # w >= 2p x - p^2   ->  -w + 2p x <= p^2
                        R.append(([w, x], [F(-1), 2 * p], p * p))
                    # secant w <= (l+h) x - l h
                    R.append(([w, x], [F(1), -(l + h)], -l * h))
                else:
                    assert l >= 0, "cube argument must be >= 0"
                    for p in pts:  # w >= 3p^2 x - 2p^3 (valid for x >= -2p)
                        R.append(([w, x], [F(-1), 3 * p * p], 2 * p ** 3))
                    s = h * h + h * l + l * l
                    R.append(([w, x], [F(1), -s], -h * l * (h + l)))
            else:
                lx, hx, ly, hy = F(lo[x]), F(hi[x]), F(lo[y]), F(hi[y])
                # (x-lx)(y-ly) >= 0: -w + ly x + lx y <= lx ly
                R.append(([w, x, y], [F(-1), ly, lx], lx * ly))
                # (hx-x)(hy-y) >= 0: -w + hy x + hx y <= hx hy
                R.append(([w, x, y], [F(-1), hy, hx], hx * hy))
                # (x-lx)(hy-y) >= 0: w - hy x - lx y <= -lx hy
                R.append(([w, x, y], [F(1), -hy, -lx], -lx * hy))
                # (hx-x)(y-ly) >= 0: w - ly x - hx y <= -hx ly
                R.append(([w, x, y], [F(1), -ly, -hx], -hx * ly))
        return [(c, a, b, False) for (c, a, b) in R]

    def lp(self, obj, lo, hi, rows):
        ub = [r for r in rows if not r[3]]
        eq = [r for r in rows if r[3]]

        def mat(rs):
            ri, ci, v = [], [], []
            for k, (cols, cf, b, e) in enumerate(rs):
                ri += [k] * len(cols)
                ci += cols
                v += [float(a) for a in cf]
            return csr_matrix((v, (ri, ci)), shape=(len(rs), self.n))
        res = linprog(obj, A_ub=mat(ub), b_ub=[float(r[2]) for r in ub], A_eq=mat(eq),
                      b_eq=[float(r[2]) for r in eq], bounds=list(zip(lo, hi)), method="highs")
        y = [0.0] * len(rows)
        if res.status != 0:
            return None, None
        iu = ie = 0
        for k, r in enumerate(rows):
            if r[3]:
                y[k] = -float(res.eqlin.marginals[ie])
                ie += 1
            else:
                y[k] = -float(res.ineqlin.marginals[iu])
                iu += 1
        return res.x, y

    def lp_elastic(self, obj, lo, hi, rows, pen=1e4):
        """LP with a penalized slack on every row (always feasible); only its
        duals are used."""
        ub = [r for r in rows if not r[3]]
        eq = [r for r in rows if r[3]]
        nu, ne = len(ub), len(eq)
        N = self.n + nu + 2 * ne
        ri, ci, v = [], [], []
        for k, (cols, cf, b, e) in enumerate(ub):
            ri += [k] * len(cols) + [k]
            ci += cols + [self.n + k]
            v += [float(a) for a in cf] + [-1.0]
        Aub = csr_matrix((v, (ri, ci)), shape=(nu, N))
        ri, ci, v = [], [], []
        for k, (cols, cf, b, e) in enumerate(eq):
            ri += [k] * len(cols) + [k, k]
            ci += cols + [self.n + nu + k, self.n + nu + ne + k]
            v += [float(a) for a in cf] + [1.0, -1.0]
        Aeq = csr_matrix((v, (ri, ci)), shape=(ne, N))
        cc = np.concatenate([obj, np.full(nu + 2 * ne, pen)])
        bnds = list(zip(lo, hi)) + [(0, None)] * (nu + 2 * ne)
        res = linprog(cc, A_ub=Aub, b_ub=[float(r[2]) for r in ub], A_eq=Aeq,
                      b_eq=[float(r[2]) for r in eq], bounds=bnds, method="highs")
        if res.status != 0:
            return None, None
        y = [0.0] * len(rows)
        iu = ie = 0
        for k, r in enumerate(rows):
            if r[3]:
                y[k] = -float(res.eqlin.marginals[ie])
                ie += 1
            else:
                y[k] = -float(res.ineqlin.marginals[iu])
                iu += 1
        return res.x[:self.n], y

    def exact_bound(self, cexact, lo, hi, rows, y):
        """min over the box of (c + A^T y).z - y.b, exactly (Fraction)."""
        r = list(cexact)
        yb = F(0)
        for (cols, cf, b, e), yi in zip(rows, y):
            if yi == 0.0 or (not e and yi < 0):
                continue
            Y = F(yi)
            for col, a in zip(cols, cf):
                r[col] += Y * a
            yb += Y * b
        tot = -yb
        for j in range(self.n):
            rj = r[j]
            if rj > 0:
                if not fin(lo[j]):
                    return None
                tot += rj * F(lo[j])
            elif rj < 0:
                if not fin(hi[j]):
                    return None
                tot += rj * F(hi[j])
        return tot

    def node_bound(self, lo, hi, cexact=None, cfloat=None):
        cexact = self.c if cexact is None else cexact
        cfloat = self.cf if cfloat is None else cfloat
        rows = self.static + self.relax_rows(lo, hi)
        x, y = self.lp(cfloat, lo, hi, rows)
        if x is None:
            x, y = self.lp_elastic(cfloat, lo, hi, rows)
            if x is None:
                return None, None
        return self.exact_bound(cexact, lo, hi, rows, y), x

    def obbt(self, lo, hi, cand):
        for j in cand:
            for sgn in (1, -1):
                ce = [F(0)] * self.n
                ce[j] = F(sgn)
                cfl = np.zeros(self.n)
                cfl[j] = sgn
                b, _ = self.node_bound(lo, hi, ce, cfl)
                if b is None:
                    continue
                if sgn == 1:
                    lo[j] = max(lo[j], fdn(b))
                else:
                    hi[j] = min(hi[j], fup(-b))
                if lo[j] > hi[j]:
                    return None
            r = self.fbbt(lo, hi, 5)
            if r is None:
                return None
            lo, hi = r
        return lo, hi


def mono_val(kind, x, y, z):
    if kind == "sq":
        return z[x] ** 2
    if kind == "cube":
        return z[x] ** 3
    return z[x] * z[y]


def choose(P, lo, hi, z, rootw):
    fr = [(abs(z[j] - 0.5), j) for j in range(P.n0) if P.isbin[j] and hi[j] > lo[j] and 1e-6 < z[j] < 1 - 1e-6]
    if fr:
        return min(fr)[1], None
    best, bv = 0.0, None
    for (kind, x, y, w) in P.aux:
        v = abs(z[w] - mono_val(kind, x, y, z))
        if v <= 1e-9:
            continue
        for a in ((x,) if y is None else (x, y)):
            if P.isbin[a]:
                continue
            wd = hi[a] - lo[a]
            if wd <= 1e-7:
                continue
            s = v * wd / rootw[a]
            if s > best:
                best, bv = s, a
    if bv is None:
        ub = [j for j in range(P.n0) if P.isbin[j] and hi[j] > lo[j]]
        return (ub[0], None) if ub else (None, None)
    wd = hi[bv] - lo[bv]
    sp = min(max(z[bv], lo[bv] + 0.25 * wd), hi[bv] - 0.25 * wd)
    return bv, sp


def solve(P, target, node_limit=100000, time_limit=1800.0, root_obbt=True, verbose=True):
    tic = time.time()
    tF = F(target)
    r = P.fbbt(P.lo0, P.hi0)
    if r is None:
        return dict(bound="inf", status="infeasible", nodes=0)
    lo, hi = r
    if root_obbt:
        cand = sorted({a for (k, x, y, w) in P.aux for a in ((x,) if y is None else (x, y)) if not P.isbin[a]})
        r = P.obbt(lo, hi, cand)
        if r is None:
            return dict(bound="inf", status="infeasible", nodes=0)
        lo, hi = r
    rootw = [max(h - l, 1e-9) if fin(h) and fin(l) else 1.0 for l, h in zip(lo, hi)]
    heap = [(-INF, 0, lo, hi)]
    cnt, nodes, leaf_min, infeas = 0, 0, None, 0
    status = "certified"
    while heap:
        if nodes >= node_limit or time.time() - tic > time_limit:
            status = "limit"
            break
        pb, _, lo, hi = heapq.heappop(heap)
        nodes += 1
        r = P.fbbt(lo, hi, 8)
        if r is None:
            infeas += 1
            continue
        lo, hi = r
        b, z = P.node_bound(lo, hi)
        if b is not None and b >= tF:
            continue
        if z is None:
            raise RuntimeError("LP failed")
        bf = fdn(b) if b is not None else -INF
        var, sp = choose(P, lo, hi, z, rootw)
        if var is None:
            leaf_min = bf if leaf_min is None else min(leaf_min, bf)
            continue
        l2, h2, l3, h3 = lo[:], hi[:], lo[:], hi[:]
        if P.isbin[var]:
            h2[var], l3[var] = 0.0, 1.0
        else:
            h2[var], l3[var] = sp, sp
        cnt += 1
        heapq.heappush(heap, (bf, cnt, l2, h2))
        cnt += 1
        heapq.heappush(heap, (bf, cnt, l3, h3))
        if verbose and nodes % 200 == 0:
            print(f"  nodes {nodes} open {len(heap)} min open {heap[0][0]:.6f} target {target:.6f} "
                  f"t {time.time()-tic:.0f}s", flush=True)
    cands = [F(h[0]) if fin(h[0]) else None for h in heap]
    if leaf_min is not None:
        cands.append(F(leaf_min))
    if any(c is None for c in cands):
        bound = None
    else:
        bound = min([tF] + cands)
    return dict(bound=None if bound is None else str(bound), bound_float=None if bound is None else fdn(bound),
                status=status if bound == tF else "limit", nodes=nodes, open=len(heap),
                infeasible_nodes=infeas, time=time.time() - tic)


if __name__ == "__main__":
    T, t = int(sys.argv[1]), int(sys.argv[2])
    mult = json.load(open(sys.argv[3]))
    target = float(sys.argv[4])
    nl = int(sys.argv[5]) if len(sys.argv) > 5 else 100000
    tl = float(sys.argv[6]) if len(sys.argv) > 6 else 1800.0
    extra = json.load(open(sys.argv[7])) if len(sys.argv) > 7 else None
    lam = [[float(v) for v in l] for l in mult["lam"]]
    mu = float(mult["mu"])
    P = Period(T, t, lam, mu, extra)
    print(f"T={T} period {t}: {P.n0} vars, {len(P.aux)} monomials, {len(P.rows)} rows, target {target!r}", flush=True)
    res = solve(P, target, nl, tl)
    print("RESULT", json.dumps(res), flush=True)
