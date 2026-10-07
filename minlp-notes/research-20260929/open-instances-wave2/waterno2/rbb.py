"""Rigorous LP-based spatial branch and bound for window subproblems of waterno2_T.

Problem (window W of consecutive periods, Lagrangian objective c):
    min c.x  s.t. the OSIL rows of W (polynomial, degree <= 3), the OSIL
    variable bounds, x_b in {0,1} for binaries.
Every nonlinear monomial (x^2, x^3, x*y) gets an auxiliary variable w = m(x);
all OSIL rows become linear in (x, w).

Rigour (what the certified bound rests on):
  * Data: decimal constants from the OSIL file are enclosed in floating-point
    intervals [dn(v), up(v)] (one ulp outward); variable bounds are widened
    outward by one ulp.  The objective coefficients c are exact floats (the
    Lagrange multipliers are taken to be exactly those floats).
  * Bound propagation (FBBT) uses outward-rounded interval arithmetic; the
    rounding error of every float sum of n terms is covered by an explicit
    margin 4e-14 * sum|terms| (>= (n-1) * 2^-53 * sum|terms| for n <= 300).
  * Node relaxation: McCormick inequalities for x*y, tangents and secants for
    x^2 and x^3 (x >= 0), with rigorously computed constants; the OSIL rows
    with interval coefficients.  Any dual vector (nu >= 0 for <= rows, eta
    free for = rows) gives the lower bound
        min_{x in box} (c + A^T nu + A_eq^T eta).x - nu.b - eta.b_eq,
    evaluated with interval coefficients and outward rounding (Neumaier and
    Shcherbina 2004).  The LP solver (HiGHS) only supplies the dual vector; its
    optimality is not relied on.
  * A node is discarded only if its rigorous bound is >= the target value or
    if FBBT proves it empty.  The certified bound is min(target, min of the
    rigorous bounds of all open nodes).
"""
import heapq
import math
import time
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

INF = math.inf
MARG = 1e-12


def dn(x):
    return np.nextafter(x, -np.inf)


def up(x):
    return np.nextafter(x, np.inf)


def dec_iv(s):
    """Interval enclosure of a decimal string."""
    f = float(s)
    if Fraction(s) == Fraction(f):
        return f, f
    return float(dn(f)), float(up(f))


def imul(al, ah, bl, bh):
    p = np.array([al * bl, al * bh, ah * bl, ah * bh])
    with np.errstate(invalid="ignore"):
        p = np.where(np.isnan(p), 0.0, p)  # 0*inf -> 0 (interval convention)
    return dn(p.min(axis=0)), up(p.max(axis=0))


class Window:
    def __init__(self, D, t0, t1, box=None):
        M, S = D["M"], D["S"]
        self.D, self.t0, self.t1 = D, t0, t1
        gv = [v for t in range(t0, t1) for v in S["per_vars"][t]]
        self.gv = gv
        loc = {v: k for k, v in enumerate(gv)}
        self.loc = loc
        n0 = len(gv)
        lo, hi, isbin = [], [], []
        for v in gv:
            l, h = M["lb"][v], M["ub"][v]
            lo.append(-INF if l.upper() == "-INF" else dec_iv(l)[0])
            hi.append(INF if h.upper() in ("INF", "+INF") else dec_iv(h)[1])
            isbin.append(M["vt"][v] == "B")
        rows = [i for t in range(t0, t1) for i in S["per_rows"][t]]
        rows += [i for t in range(t0, t1 - 1) for (i, a, b) in S["link"][t]]
        aux = {}      # monomial (sorted local tuple) -> aux index
        auxdef = []   # (kind, args)
        R = []        # rows: (cols, coef_lo, coef_hi, rlo, rhi)
        for i in rows:
            r = M["rows"][i]
            cols, cl, ch = [], [], []
            for mono, a in r["poly"].items():
                al, ah = dec_iv(a)
                if len(mono) == 1:
                    cols.append(loc[mono[0]])
                else:
                    key = tuple(sorted(loc[v] for v in mono))
                    if key not in aux:
                        if len(key) == 2 and key[0] == key[1]:
                            kind = "sq"
                        elif len(key) == 3 and key[0] == key[1] == key[2]:
                            kind = "cube"
                        elif len(key) == 2:
                            kind = "bil"
                        else:
                            raise NotImplementedError(key)
                        aux[key] = n0 + len(auxdef)
                        auxdef.append((kind, key))
                    cols.append(aux[key])
                cl.append(al)
                ch.append(ah)
            rl = -INF if r["lb"].upper() == "-INF" else dec_iv(r["lb"])[0]
            rh = INF if r["ub"].upper() in ("INF", "+INF") else dec_iv(r["ub"])[1]
            R.append((np.array(cols), np.array(cl), np.array(ch), rl, rh, (r["name"], r["lb"] == r["ub"])))
        # no-good rows excluding pump configurations: sum_{v on}(1 - b_v) + sum_{v off} b_v >= 1,
        # i.e.  - sum_{v on} b_v + sum_{v off} b_v >= 1 - |on|   (integer data, exact)
        for t in range(t0, t1):
            for box in D.get("nogood", {}).get(t, []):
                cols, cl = [], []
                non = 0
                for v, (a, b) in box.items():
                    cols.append(loc[v])
                    if a == 1.0:
                        cl.append(-1.0)
                        non += 1
                    else:
                        cl.append(1.0)
                cl = np.array(cl)
                R.append((np.array(cols), cl, cl.copy(), float(1 - non), INF, ("nogood", False)))
        self.n0, self.naux = n0, len(auxdef)
        self.n = n0 + len(auxdef)
        self.auxdef = auxdef
        self.rows = R
        # implied bounds (rigorously derived for the full problem, implied.py)
        for k, v in enumerate(gv):
            for src in (D.get("extra", {}), box or {}):
                if v in src:
                    el, eu = src[v]
                    lo[k], hi[k] = max(lo[k], el), min(hi[k], eu)
        self.lo0 = np.array(lo + [-INF] * len(auxdef))
        self.hi0 = np.array(hi + [INF] * len(auxdef))
        self.isbin = np.array(isbin + [False] * len(auxdef))
        # sparse row structure for vectorized FBBT
        ri, ci, al, ah = [], [], [], []
        for k, (cols, cl, ch, rl, rh, nm) in enumerate(R):
            ri += [k] * len(cols)
            ci += list(cols)
            al += list(cl)
            ah += list(ch)
        self.nz_r = np.array(ri)
        self.nz_c = np.array(ci)
        self.nz_al = np.array(al)
        self.nz_ah = np.array(ah)
        self.r_lo = np.array([r[3] for r in R])
        self.r_hi = np.array([r[4] for r in R])
        self.nrows = len(R)
        assert np.all((self.nz_al > 0) | (self.nz_ah < 0)), "coefficient interval contains 0"

    # ------------------------------------------------------------------
    def objective(self, lam, mu):
        """Exact-float objective of the window; asserts that no variable
        collects two Lagrangian contributions (so no float sums occur)."""
        D, S, M = self.D, self.D["S"], self.D["M"]
        T = D["T"]
        c = np.zeros(self.n)
        seen = set()

        def put(v, val):
            assert v not in seen, "variable with two objective contributions"
            seen.add(v)
            c[self.loc[v]] = val
        for v in self.gv:
            if v in M["obj"]:
                assert Fraction(M["obj"][v]) == 1
                put(v, 1.0)
        for t in range(max(self.t0 - 1, 0), min(self.t1, T - 1)):
            ia = self.t0 <= t < self.t1
            ib = self.t0 <= t + 1 < self.t1
            if ia and ib:
                continue
            for k, (i, a, b) in enumerate(S["link"][t]):
                if ia:
                    put(a, -float(lam[t][k]))
                if ib:
                    put(b, float(lam[t][k]))
        for v, a in D["hor"].items():
            if self.t0 <= D["per_of"][v] < self.t1:
                assert a == 1
                put(v, -float(mu))
        return c

    # ------------------------------------------------------------------
    def fbbt(self, lo, hi, rounds=8):
        lo, hi = lo.copy(), hi.copy()
        for _ in range(rounds):
            olo, ohi = lo.copy(), hi.copy()
            if not self._aux_prop(lo, hi):
                return None
            if not self._row_prop(lo, hi):
                return None
            # binaries: round inward
            b = self.isbin
            lo[b] = np.ceil(lo[b] - 1e-9)
            hi[b] = np.floor(hi[b] + 1e-9)
            if np.any(lo > hi):
                return None
            with np.errstate(invalid="ignore"):
                d1 = np.where(np.isfinite(lo), lo - np.where(np.isfinite(olo), olo, -1e300), 0.0)
                d2 = np.where(np.isfinite(hi), np.where(np.isfinite(ohi), ohi, 1e300) - hi, 0.0)
            width = np.where(np.isfinite(hi - lo), hi - lo, 1.0) + 1e-9
            if max(np.max(d1 / width), np.max(d2 / width)) < 1e-4:
                break
        return lo, hi

    def _aux_index(self):
        if not hasattr(self, "_ai"):
            n0 = self.n0
            sq = [(n0 + k, a[0]) for k, (kind, a) in enumerate(self.auxdef) if kind == "sq"]
            cu = [(n0 + k, a[0]) for k, (kind, a) in enumerate(self.auxdef) if kind == "cube"]
            bi = [(n0 + k, a[0], a[1]) for k, (kind, a) in enumerate(self.auxdef) if kind == "bil"]
            self._ai = (np.array(sq, dtype=int).reshape(-1, 2), np.array(cu, dtype=int).reshape(-1, 2),
                        np.array(bi, dtype=int).reshape(-1, 3))
        return self._ai

    def _aux_prop(self, lo, hi):
        """Vectorized interval propagation through w = x^2, w = x^3, w = x*y
        (forward and backward), outward rounded."""
        sq, cu, bi = self._aux_index()
        with np.errstate(invalid="ignore", over="ignore"):
            # ---- squares
            if len(sq):
                w, x = sq[:, 0], sq[:, 1]
                l, h = lo[x], hi[x]
                a, b = imul(l, h, l, h)
                a = np.where((l <= 0) & (h >= 0), 0.0, np.maximum(a, 0.0))
                lo[w] = np.maximum(lo[w], a)
                hi[w] = np.minimum(hi[w], b)
                if np.any(lo[w] > hi[w]):
                    return False
                wl, wh = np.maximum(lo[w], 0.0), hi[w]
                sl = dn(np.sqrt(wl))
                sh = np.where(np.isfinite(wh), up(np.sqrt(wh)), np.inf)
                pos, neg = l >= 0, h <= 0
                nlo = np.where(pos, sl, np.where(neg, -sh, -sh))
                nhi = np.where(pos, sh, np.where(neg, -sl, sh))
                np.maximum.at(lo, x, nlo)
                np.minimum.at(hi, x, nhi)
            # ---- cubes (arguments >= 0)
            if len(cu):
                w, x = cu[:, 0], cu[:, 1]
                l, h = lo[x], hi[x]
                assert np.all(l >= 0), "cube of a possibly negative variable"
                a = dn(dn(l * l) * l)
                b = np.where(np.isfinite(h), up(up(h * h) * h), np.inf)
                lo[w] = np.maximum(lo[w], np.maximum(a, 0.0))
                hi[w] = np.minimum(hi[w], b)
                if np.any(lo[w] > hi[w]):
                    return False
                wl, wh = lo[w], hi[w]
                xl = dn(dn(dn(dn(np.cbrt(np.maximum(wl, 0.0))))))
                okl = (wl > 0) & (up(up(xl * xl) * xl) <= wl)
                np.maximum.at(lo, x[okl], xl[okl])
                xh = up(up(up(up(np.cbrt(np.where(np.isfinite(wh), wh, 0.0))))))
                okh = np.isfinite(wh) & (dn(dn(xh * xh) * xh) >= wh)
                np.minimum.at(hi, x[okh], xh[okh])
            # ---- bilinear (arguments >= 0 in this model; backward only for positive divisors)
            if len(bi):
                w, x, y = bi[:, 0], bi[:, 1], bi[:, 2]
                a, b = imul(lo[x], hi[x], lo[y], hi[y])
                lo[w] = np.maximum(lo[w], a)
                hi[w] = np.minimum(hi[w], b)
                if np.any(lo[w] > hi[w]):
                    return False
                for p, q in ((x, y), (y, x)):
                    ok = (lo[q] > 0) & np.isfinite(hi[q]) & np.isfinite(lo[w]) & np.isfinite(hi[w])
                    if not np.any(ok):
                        continue
                    ql = np.where(ok, lo[q], 1.0)
                    qh = np.where(ok, hi[q], 1.0)
                    wl = np.where(ok, lo[w], 0.0)
                    wh = np.where(ok, hi[w], 0.0)
                    cand = np.array([wl / ql, wl / qh, wh / ql, wh / qh])
                    pl, ph = dn(cand.min(axis=0)), up(cand.max(axis=0))
                    # several monomials may share an argument: apply sequentially
                    np.maximum.at(lo, p[ok], pl[ok])
                    np.minimum.at(hi, p[ok], ph[ok])
        return not np.any(lo > hi)

    def _row_prop(self, lo, hi):
        c = self.nz_c
        al, ah = self.nz_al, self.nz_ah
        tl, th = imul(al, ah, lo[c], hi[c])
        r = self.nz_r
        nr = self.nrows
        # lower sums (finite part and count of -inf)
        finl = np.where(np.isfinite(tl), tl, 0.0)
        finh = np.where(np.isfinite(th), th, 0.0)
        ninfl = np.bincount(r, weights=(~np.isfinite(tl)).astype(float), minlength=nr)
        ninfh = np.bincount(r, weights=(~np.isfinite(th)).astype(float), minlength=nr)
        sl = np.bincount(r, weights=finl, minlength=nr)
        sh = np.bincount(r, weights=finh, minlength=nr)
        absl = np.bincount(r, weights=np.abs(finl), minlength=nr)
        absh = np.bincount(r, weights=np.abs(finh), minlength=nr)
        # others' sums for each nonzero
        ol = sl[r] - finl
        oh = sh[r] - finh
        ol = dn(ol - MARG * (absl[r] + np.abs(finl)))
        oh = up(oh + MARG * (absh[r] + np.abs(finh)))
        ol = np.where(ninfl[r] - (~np.isfinite(tl)) > 0, -np.inf, ol)
        oh = np.where(ninfh[r] - (~np.isfinite(th)) > 0, np.inf, oh)
        # term in [rlo - oh, rhi - ol]
        with np.errstate(invalid="ignore"):
            ql = dn(self.r_lo[r] - oh)
            qh = up(self.r_hi[r] - ol)
        ql = np.where(np.isnan(ql), -np.inf, ql)
        qh = np.where(np.isnan(qh), np.inf, qh)
        # feasibility of the row itself
        tot_l = np.where(ninfl > 0, -np.inf, dn(sl - MARG * absl))
        tot_h = np.where(ninfh > 0, np.inf, up(sh + MARG * absh))
        if np.any(tot_l > self.r_hi) or np.any(tot_h < self.r_lo):
            return False
        # x = term / a, a interval not containing 0
        with np.errstate(divide="ignore", invalid="ignore"):
            cands = np.array([ql / al, ql / ah, qh / al, qh / ah])
        cands = np.where(np.isnan(cands), 0.0, cands)
        # if the term interval is unbounded on one side, the quotient is unbounded
        xl = dn(cands.min(axis=0))
        xh = up(cands.max(axis=0))
        unb_l = ~np.isfinite(ql)
        unb_h = ~np.isfinite(qh)
        pos = al > 0
        xl = np.where((pos & unb_l) | (~pos & unb_h), -np.inf, xl)
        xh = np.where((pos & unb_h) | (~pos & unb_l), np.inf, xh)
        np.maximum.at(lo, c, xl)
        np.minimum.at(hi, c, xh)
        return not np.any(lo > hi)

    # ------------------------------------------------------------------
    def _static_rows(self):
        """OSIL rows in LP form (nonzero arrays); equality rows keep their
        decimal rhs enclosure, range rows are split into two <= rows."""
        if hasattr(self, "_st"):
            return self._st
        ri, ci, am, al, ah, sense, bl, bh = [], [], [], [], [], [], [], []
        k = 0

        def add(cols, mid, cl, ch, sn, b1, b2):
            nonlocal k
            ri.extend([k] * len(cols))
            ci.extend(cols)
            am.extend(mid)
            al.extend(cl)
            ah.extend(ch)
            sense.append(sn)
            bl.append(b1)
            bh.append(b2)
            k += 1
        for (cols, cl, ch, rl, rh, nm) in self.rows:
            mid = np.where(cl == ch, cl, 0.5 * (cl + ch))
            if nm[1]:
                add(cols, mid, cl, ch, 1, rl, rh)
            else:
                if np.isfinite(rh):
                    add(cols, mid, cl, ch, 0, rh, rh)
                if np.isfinite(rl):
                    add(cols, -mid, -ch, -cl, 0, -rl, -rl)
        self._st = dict(ri=np.array(ri), ci=np.array(ci), am=np.array(am), al=np.array(al),
                        ah=np.array(ah), sense=np.array(sense), bl=np.array(bl), bh=np.array(bh), m=k)
        return self._st

    def relaxation(self, lo, hi, extra=None):
        """Node LP rows (arrays): static OSIL rows plus the relaxations of the
        auxiliary monomials on the box.  Row i reads  a_i.x <= b_i  (sense 0)
        or a_i.x = b_i (sense 1) with the exact coefficients in [al, ah] and the
        exact rhs in [bl, bh].  extra: optional (cols, coefs, rhs) cutoff row."""
        st = self._static_rows()
        sq, cu, bi = self._aux_index()
        R = [(st["ri"], st["ci"], st["am"], st["al"], st["ah"], st["sense"], st["bl"], st["bh"])]
        m = st["m"]
        parts = []
        # ---- squares: tangents at l, h, mid:  -w + 2a x <= a^2 ; secant w - s x <= C
        if len(sq):
            w, x = sq[:, 0], sq[:, 1]
            l, h = lo[x], hi[x]
            for a in (l, h, 0.5 * (l + h)):
                g = 2.0 * a
                parts.append((w, x, np.full(len(w), -1.0), g, up(a * a)))
            sl = np.where(h > l, (h * h - l * l) / np.where(h > l, h - l, 1.0), 0.0)
            C = np.maximum(self._up_pow_minus(l, sl, 2), self._up_pow_minus(h, sl, 2))
            parts.append((w, x, np.full(len(w), 1.0), -sl, C))
        # ---- cubes (x >= 0): tangents and secant
        if len(cu):
            w, x = cu[:, 0], cu[:, 1]
            l, h = lo[x], hi[x]
            for a in (l, h, 0.5 * (l + h)):
                g = 3.0 * a * a
                cst = self._cube_tangent_const_v(g, l, h)
                parts.append((w, x, np.full(len(w), -1.0), g, -cst))
            sl = np.where(h > l, (h * h * h - l * l * l) / np.where(h > l, h - l, 1.0), 0.0)
            C = np.maximum(self._up_pow_minus(l, sl, 3), self._up_pow_minus(h, sl, 3))
            parts.append((w, x, np.full(len(w), 1.0), -sl, C))
        rows2 = []
        for (w, x, cw, cx, rhs) in parts:
            rows2.append((w, x, None, cw, cx, None, rhs))
        # ---- bilinear McCormick
        if len(bi):
            w, x, y = bi[:, 0], bi[:, 1], bi[:, 2]
            lx, hx, ly, hy = lo[x], hi[x], lo[y], hi[y]
            ones = np.ones(len(w))
            # under: -w + ly x + lx y <= lx ly ; -w + hy x + hx y <= hx hy
            for (a1, a2, p_, q_) in ((ly, lx, lx, ly), (hy, hx, hx, hy)):
                pl, ph = imul(p_, p_, q_, q_)
                rows2.append((w, x, y, -ones, a1, a2, ph))
            # over: w - hy x - lx y <= -lx hy ; w - ly x - hx y <= -hx ly
            for (a1, a2, p_, q_) in ((hy, lx, lx, hy), (ly, hx, hx, ly)):
                pl, ph = imul(p_, p_, q_, q_)
                rows2.append((w, x, y, ones, -a1, -a2, -pl))
        for (w, x, y, cw, cx, cy, rhs) in rows2:
            nr = len(w)
            idx = m + np.arange(nr)
            if y is None:
                rr = np.concatenate([idx, idx])
                cc = np.concatenate([w, x])
                aa = np.concatenate([cw, cx])
            else:
                rr = np.concatenate([idx, idx, idx])
                cc = np.concatenate([w, x, y])
                aa = np.concatenate([cw, cx, cy])
            R.append((rr, cc, aa, aa, aa, np.zeros(nr, dtype=int), rhs, rhs))
            m += nr
        if extra is not None:
            cols, coefs, rhs = extra
            R.append((np.full(len(cols), m), cols, coefs, coefs, coefs, np.zeros(1, dtype=int),
                      np.array([rhs]), np.array([rhs])))
            m += 1
        L = dict(ri=np.concatenate([r[0] for r in R]), ci=np.concatenate([r[1] for r in R]),
                 am=np.concatenate([r[2] for r in R]), al=np.concatenate([r[3] for r in R]),
                 ah=np.concatenate([r[4] for r in R]), sense=np.concatenate([r[5] for r in R]),
                 bl=np.concatenate([r[6] for r in R]), bh=np.concatenate([r[7] for r in R]), m=m)
        return L

    @staticmethod
    def _up_pow_minus(x, s, p):
        """Upper bound of x^p - s x at float points x (vectorized, x >= 0 for p = 3)."""
        a, b = imul(x, x, x, x)
        if p == 2:
            a = np.where((x <= 0) & (x >= 0), 0.0, a)
        if p == 3:
            a, b = imul(a, b, x, x)
        c, d = imul(s, s, x, x)
        return up(b - c)

    @staticmethod
    def _cube_tangent_const_v(g, l, h):
        """Lower bound of min_{x in [l,h]} x^3 - g x (x >= 0, convex), vectorized."""
        s_lo = dn(np.sqrt(np.maximum(dn(g / 3.0), 0.0)))
        s_hi = up(np.sqrt(up(g / 3.0)))
        xl, xh = np.maximum(l, s_lo), np.minimum(h, s_hi)
        out = xl > xh
        endpoint = np.where(s_hi < l, l, h)
        xl = np.where(out, endpoint, xl)
        xh = np.where(out, endpoint, xh)
        a, b = imul(xl, xh, xl, xh)
        a, b = imul(a, b, xl, xh)
        c, d = imul(g, g, xl, xh)
        return dn(a - d)

    # ------------------------------------------------------------------
    def safe_bound(self, c, lo, hi, L, nu, full=False):
        """Rigorous lower bound  min_{box}(c + A^T y).x - y.b  for the dual
        vector y (y_i >= 0 enforced on <= rows), with interval coefficients."""
        y = nu.copy()
        le = L["sense"] == 0
        y[le] = np.maximum(y[le], 0.0)
        yr = y[L["ri"]]
        # per-nonzero product y*a with a in [al, ah]
        p1, p2 = yr * L["al"], yr * L["ah"]
        plo = np.minimum(p1, p2)
        phi = np.maximum(p1, p2)
        n = self.n
        rlo = c + np.bincount(L["ci"], weights=plo, minlength=n)
        rhi = c + np.bincount(L["ci"], weights=phi, minlength=n)
        mag = np.abs(c) + np.bincount(L["ci"], weights=np.abs(plo) + np.abs(phi), minlength=n)
        rlo = dn(rlo - MARG * mag - 1e-300)
        rhi = up(rhi + MARG * mag + 1e-300)
        # - y.b (lower end): for y >= 0 use bh, for y < 0 use bl
        yb = np.where(y >= 0, y * L["bh"], y * L["bl"])
        yb = np.where(y == 0, 0.0, yb)
        rhs_sum = yb.sum()
        rhs_abs = np.abs(yb).sum()
        with np.errstate(invalid="ignore"):
            pp = np.array([rlo * lo, rlo * hi, rhi * lo, rhi * hi])
        pp = np.where(np.isnan(pp), 0.0, pp)
        terms = dn(pp.min(axis=0))
        if np.any(np.isneginf(terms)):
            return (-INF, None, None, None) if full else -INF
        tot = terms.sum() - rhs_sum
        err = MARG * (np.abs(terms).sum() + rhs_abs) + 1e-300
        B = float(dn(tot - err))
        if full:
            return B, rlo, rhi, terms
        return B

    def rc_tighten(self, lo, hi, target, B, rlo, rhi, terms):
        """Reduced-cost tightening (rigorous): for x in the box with c.x < target,
        r_j x_j < G_j := target - (B - term_j)."""
        if not np.isfinite(target) or not np.isfinite(B):
            return lo, hi
        G = up(up(target - B) + terms)
        lo, hi = lo.copy(), hi.copy()
        with np.errstate(divide="ignore", invalid="ignore"):
            pos = rlo > 0
            ub = np.where(G >= 0, up(G / rlo), up(G / rhi))
            hi = np.where(pos & np.isfinite(ub), np.minimum(hi, ub), hi)
            neg = rhi < 0
            lb = np.where(G >= 0, dn(G / rhi), dn(G / rlo))
            lo = np.where(neg & np.isfinite(lb), np.maximum(lo, lb), lo)
        return lo, hi

    def obbt(self, c, target, lo, hi, cand, rounds=1):
        """Rigorous optimization-based bound tightening over the LP relaxation plus
        the objective cutoff c.x <= target (points with c.x >= target are not needed)."""
        for _ in range(rounds):
            for j in cand:
                for sgn in (1.0, -1.0):
                    extra = None
                    if np.isfinite(target):
                        nz = np.nonzero(c)[0]
                        extra = (nz, c[nz], float(target))
                    L = self.relaxation(lo, hi, extra)
                    e = np.zeros(self.n)
                    e[j] = sgn
                    x, nu, val = self.node_lp(e, lo, hi, L)
                    if x is None:
                        x, nu = self.node_lp_elastic(e, lo, hi, L)
                        if x is None:
                            continue
                    b = self.safe_bound(e, lo, hi, L, nu)
                    if sgn > 0:
                        lo[j] = max(lo[j], b)
                    else:
                        hi[j] = min(hi[j], -b)
                    if lo[j] > hi[j]:
                        return None
                r = self.fbbt(lo, hi)
                if r is None:
                    return None
                lo, hi = r
        return lo, hi

    # ------------------------------------------------------------------
    def node_lp(self, c, lo, hi, L):
        le = L["sense"] == 0
        m = L["m"]
        # row renumbering within the le and eq blocks
        pos = np.zeros(m, dtype=int)
        pos[le] = np.arange(le.sum())
        pos[~le] = np.arange((~le).sum())
        nzle = le[L["ri"]]
        n = self.n
        Aub = csr_matrix((L["am"][nzle], (pos[L["ri"][nzle]], L["ci"][nzle])), shape=(le.sum(), n))
        Aeq = csr_matrix((L["am"][~nzle], (pos[L["ri"][~nzle]], L["ci"][~nzle])), shape=((~le).sum(), n))
        b_ub = L["bh"][le]
        b_eq = 0.5 * (L["bl"][~le] + L["bh"][~le])
        bounds = np.column_stack([lo, hi])
        res = linprog(c, A_ub=Aub, b_ub=b_ub, A_eq=Aeq, b_eq=b_eq, bounds=bounds, method="highs")
        nu = np.zeros(m)
        if res.status == 0:
            nu[le] = -res.ineqlin.marginals
            nu[~le] = -res.eqlin.marginals
            return res.x, nu, res.fun
        return None, None, None

    def node_lp_elastic(self, c, lo, hi, L, pen=1e4):
        """Elastic LP (always feasible): a slack on every row with cost pen.
        Only its row duals are used (in safe_bound)."""
        le = L["sense"] == 0
        m = L["m"]
        n = self.n
        nle, neq = int(le.sum()), int((~le).sum())
        pos = np.zeros(m, dtype=int)
        pos[le] = np.arange(nle)
        pos[~le] = np.arange(neq)
        nzle = le[L["ri"]]
        # le rows: a x - s <= b ; eq rows: a x + s+ - s- = b
        r1 = np.concatenate([pos[L["ri"][nzle]], np.arange(nle)])
        c1 = np.concatenate([L["ci"][nzle], n + np.arange(nle)])
        v1 = np.concatenate([L["am"][nzle], -np.ones(nle)])
        N = n + nle + 2 * neq
        r2 = np.concatenate([pos[L["ri"][~nzle]], np.arange(neq), np.arange(neq)])
        c2 = np.concatenate([L["ci"][~nzle], n + nle + np.arange(neq), n + nle + neq + np.arange(neq)])
        v2 = np.concatenate([L["am"][~nzle], np.ones(neq), -np.ones(neq)])
        Aub = csr_matrix((v1, (r1, c1)), shape=(nle, N))
        Aeq = csr_matrix((v2, (r2, c2)), shape=(neq, N))
        cc = np.concatenate([c, np.full(nle + 2 * neq, pen)])
        bounds = np.vstack([np.column_stack([lo, hi]), np.column_stack([np.zeros(nle + 2 * neq),
                                                                        np.full(nle + 2 * neq, np.inf)])])
        res = linprog(cc, A_ub=Aub, b_ub=L["bh"][le], A_eq=Aeq, b_eq=0.5 * (L["bl"][~le] + L["bh"][~le]),
                      bounds=bounds, method="highs")
        nu = np.zeros(m)
        if res.status == 0:
            nu[le] = -res.ineqlin.marginals
            nu[~le] = -res.eqlin.marginals
            return res.x[:n], nu
        return None, None


def mono_val(kind, args, x):
    if kind == "sq":
        return x[args[0]] ** 2
    if kind == "cube":
        return x[args[0]] ** 3
    return x[args[0]] * x[args[1]]


def solve(W, c, target, node_limit=200000, time_limit=600.0, verbose=False, gap_abs=1e-9,
          rc=True, obbt_vars=None, obbt_rounds=1):
    """Certify min c.x >= target over the window (or return the best certified bound).

    Returns dict(bound=certified lower bound, nodes, open, status, best_lp_point)."""
    tic = time.time()
    root = W.fbbt(W.lo0, W.hi0)
    if root is None:
        return dict(bound=INF, nodes=0, open=0, status="infeasible")
    heap = []
    cnt = 0
    nodes = 0
    pruned_infeas = 0
    min_open = INF
    lo, hi = root
    if obbt_vars is not None:
        r = W.obbt(c, target, lo, hi, obbt_vars, obbt_rounds)
        if r is None:
            return dict(bound=target, nodes=0, open=0, status="certified", time=time.time() - tic)
        lo, hi = r
    W.root_width = np.maximum(hi - lo, 1e-9)
    heapq.heappush(heap, (-INF, cnt, lo, hi))
    closed_min = INF  # min bound among nodes closed by bound (for reporting)
    status = "certified"
    while heap:
        if nodes >= node_limit or time.time() - tic > time_limit:
            status = "limit"
            break
        pb, _, lo, hi = heapq.heappop(heap)
        if pb >= target:
            closed_min = min(closed_min, pb)
            continue
        nodes += 1
        r = W.fbbt(lo, hi)
        if r is None:
            pruned_infeas += 1
            continue
        lo, hi = r
        if not (np.all(np.isfinite(lo)) and np.all(np.isfinite(hi))):
            raise RuntimeError("unbounded variable after FBBT")
        L = W.relaxation(lo, hi)
        x, nu, val = W.node_lp(c, lo, hi, L)
        if x is None:
            x, nu = W.node_lp_elastic(c, lo, hi, L)
            if x is None:
                raise RuntimeError("elastic LP failed")
        b, rlo, rhi, terms = W.safe_bound(c, lo, hi, L, nu, full=True)
        if b >= target:
            closed_min = min(closed_min, b)
            continue
        if rc and rlo is not None:
            lo2, hi2 = W.rc_tighten(lo, hi, target, b, rlo, rhi, terms)
            if np.any(lo2 > hi2):
                closed_min = min(closed_min, target)
                continue
            if np.any(lo2 > lo + 1e-7 * (1 + np.abs(lo))) or np.any(hi2 < hi - 1e-7 * (1 + np.abs(hi))):
                r2 = W.fbbt(lo2, hi2)
                if r2 is None:
                    pruned_infeas += 1
                    continue
                lo, hi = r2
        # branching
        var, split = choose_branch(W, lo, hi, x)
        if var is None:
            # nothing left to branch on: box is tiny; keep its bound as final
            min_open = min(min_open, b)
            continue
        l2, h2 = lo.copy(), hi.copy()
        if W.isbin[var]:
            h2[var] = 0.0
            l3, h3 = lo.copy(), hi.copy()
            l3[var] = 1.0
        else:
            h2[var] = split
            l3, h3 = lo.copy(), hi.copy()
            l3[var] = split
        cnt += 1
        heapq.heappush(heap, (b, cnt, l2, h2))
        cnt += 1
        heapq.heappush(heap, (b, cnt, l3, h3))
        if verbose and nodes % 500 == 0:
            print(f"  nodes={nodes} open={len(heap)} minbound={heap[0][0]:.6f} target={target:.6f} "
                  f"t={time.time()-tic:.1f}", flush=True)
    open_min = min([h[0] for h in heap] + [min_open])
    bound = min(target, open_min)
    return dict(bound=bound, nodes=nodes, open=len(heap), status=status if bound >= target else "limit",
                infeasible_nodes=pruned_infeas, time=time.time() - tic)


def choose_branch(W, lo, hi, x, minwidth=1e-7):
    # binaries first
    fb = [(abs(x[j] - 0.5), j) for j in np.nonzero(W.isbin & (hi > lo))[0]
          if 1e-6 < x[j] < 1 - 1e-6]
    if fb:
        return min(fb)[1], None
    best, bv = 0.0, None
    for k, (kind, args) in enumerate(W.auxdef):
        w = W.n0 + k
        v = abs(x[w] - mono_val(kind, args, x))
        if v <= 1e-9:
            continue
        for a in set(args):
            if W.isbin[a]:
                continue
            width = hi[a] - lo[a]
            if width <= minwidth:
                continue
            score = v * width / (W.root_width[a] if hasattr(W, "root_width") else 1.0)
            if score > best:
                best, bv = score, a
    if bv is None:
        # fall back: unfixed binaries, then widest nonlinear argument
        ub = [j for j in np.nonzero(W.isbin & (hi > lo))[0]]
        if ub:
            return ub[0], None
        return None, None
    split = 0.5 * (lo[bv] + hi[bv])
    return bv, split
