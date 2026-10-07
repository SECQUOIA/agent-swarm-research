"""Referee check (round 2 confirmation) of Section 4.6 / Proposition C.5 of robust-chains.md.

Own moment-side implementation of the order-2 sparse relaxation (pair cliques) of the chiral chain
  f_n = a sum x_i^2 + b sum x_i x_{i+1} + (g/2) sum x_i x_{i+1} (x_{i+1} - x_i),  a = b + ev,  on [-1,1]^n,
written independently of chains/revision2_*.py: one global moment dictionary (univariate moments are shared
automatically, no equality constraints), PSD constraints on affine matrices.

Placements (box constraint 1 -/+ x_i, or 1 - x_i^2):
  every   : localized (clique basis 1, x, y) in every clique containing x_i
  match   : 1 - x_i in clique (i, i+1), 1 + x_i in clique (i-1, i) (ends: only clique)
  opp     : 1 - x_i in clique (i-1, i), 1 + x_i in clique (i, i+1) (ends: only clique)
  uni     : univariate multiplier basis (1, x_i)  [Waki et al. (20)]
  *_quad  : the same with 1 - x_i^2
Options: ball M (2M^2 - x^2 - y^2 per clique, clique basis); ybound (|y_alpha| <= 1 on all clique moments);
  zbound (Waki et al.'s actual technique: scale x = 2z - 1 to [0,1] and add 0 <= L(z^alpha) <= 1 for all clique
  monomials alpha of degree <= 4).
Usage: python3 d2_sdp.py n1 n2 ...      (floating point, Clarabel; SCS for a few rows)
"""
import sys
import json
import itertools
import cvxpy as cp

B_, G_, EV_ = 0.6, 0.3, 0.05
A_ = B_ + EV_


class Relax:
    def __init__(self, n):
        self.n = n
        self.mom = {}
        self.cons = []

    def key(self, k, i, j):  # monomial x_k^i x_{k+1}^j (0-based clique k)
        if i == 0 and j == 0:
            return ("1",)
        if j == 0:
            return ("u", k, i)
        if i == 0:
            return ("u", k + 1, j)
        return ("m", k, i, j)

    def y(self, k, i, j):
        kk = self.key(k, i, j)
        if kk == ("1",):
            return 1.0
        if kk not in self.mom:
            self.mom[kk] = cp.Variable()
        return self.mom[kk]

    def lin(self, k, poly):  # poly: list of (coef, (i, j)) on clique k
        return sum(cf * self.y(k, i, j) for cf, (i, j) in poly)

    def psd(self, k, basis, poly):
        rows = []
        for p in basis:
            rows.append([self.lin(k, [(cf, (p[0] + q[0] + m[0], p[1] + q[1] + m[1])) for cf, m in poly]) for q in basis])
        Mx = cp.bmat([[e if isinstance(e, cp.Expression) else cp.Constant(e) for e in row] for row in rows])
        self.cons.append((Mx + Mx.T) / 2 >> 0)


BASIS2 = [(0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2)]
BASIS1 = [(0, 0), (1, 0), (0, 1)]


def build(n, place, ball=None, ybound=False, zbound=False):
    R = Relax(n)
    for k in range(n - 1):
        R.psd(k, BASIS2, [(1.0, (0, 0))])
        if ball is not None:
            R.psd(k, BASIS1, [(2 * ball**2, (0, 0)), (-1.0, (2, 0)), (-1.0, (0, 2))])

    def cliques_of(i):  # 0-based variable i -> list of (clique, coord)
        out = []
        if i >= 1:
            out.append((i - 1, 1))
        if i <= n - 2:
            out.append((i, 0))
        return out

    def con(sign, coord, quad):
        if quad:
            return [(1.0, (0, 0)), (-1.0, (2, 0) if coord == 0 else (0, 2))]
        return [(1.0, (0, 0)), (sign, (1, 0) if coord == 0 else (0, 1))]
    quad = place.endswith("_quad")
    base = place.replace("_quad", "")
    for i in range(n):
        cl = cliques_of(i)
        left = cl[0]            # clique (i-1, i) if it exists, else (i, i+1)
        right = cl[-1]          # clique (i, i+1) if it exists, else (i-1, i)
        signs = [None] if quad else [-1.0, +1.0]
        for s in signs:
            if base == "every":
                for (k, co) in cl:
                    R.psd(k, BASIS1, con(s, co, quad))
            elif base == "match":   # 1 - x_i on the right clique, 1 + x_i on the left clique
                (k, co) = right if s == -1.0 else left
                R.psd(k, BASIS1, con(s, co, quad))
            elif base == "opp":
                (k, co) = left if s == -1.0 else right
                R.psd(k, BASIS1, con(s, co, quad))
            elif base == "oneL":
                (k, co) = left
                R.psd(k, BASIS1, con(s, co, quad))
            elif base == "oneR":
                (k, co) = right
                R.psd(k, BASIS1, con(s, co, quad))
            elif base == "uni":
                (k, co) = right
                ub = [(0, 0), (1, 0)] if co == 0 else [(0, 0), (0, 1)]
                R.psd(k, ub, con(s, co, quad))
            else:
                raise ValueError(place)
    obj = 0
    for k in range(n - 1):
        obj += A_ / 2 * (R.y(k, 2, 0) + R.y(k, 0, 2)) + B_ * R.y(k, 1, 1) + G_ / 2 * (R.y(k, 1, 2) - R.y(k, 2, 1))
    obj += A_ / 2 * R.y(0, 2, 0) + A_ / 2 * R.y(n - 2, 0, 2)
    allm = [(i, j) for i in range(5) for j in range(5 - i) if (i, j) != (0, 0)]
    if ybound:
        for k in range(n - 1):
            for (i, j) in allm:
                R.cons += [R.y(k, i, j) <= 1, R.y(k, i, j) >= -1]
    if zbound:
        # z = (1 + x)/2; L(z1^i z2^j) = 2^{-(i+j)} sum_{p<=i, q<=j} C(i,p) C(j,q) L(x1^p x2^q)
        from math import comb
        for k in range(n - 1):
            for (i, j) in allm:
                e = sum(comb(i, p) * comb(j, q) * R.y(k, p, q) for p in range(i + 1) for q in range(j + 1)) / 2 ** (i + j)
                R.cons += [e >= 0, e <= 1]
    return cp.Problem(cp.Minimize(obj), R.cons), R


RUNS = [
    ("every", None, False, False),
    ("match", None, False, False),
    ("opp", None, False, False),
    ("opp", 1.0, False, False),
    ("opp", 1.01, False, False),
    ("opp", 1.04, False, False),
    ("opp", 1.1, False, False),
    ("opp", 1.5, False, False),
    ("opp", 2.0, False, False),
    ("opp", 10.0, False, False),
    ("match", 10.0, False, False),
    ("uni", None, False, False),
    ("uni", None, True, False),
    ("uni", None, False, True),
    ("uni", 1.0, False, False),
    ("uni", 2.0, False, False),
    ("every_quad", None, False, False),
    ("oneL_quad", None, False, False),
    ("oneR_quad", None, False, False),
    ("uni_quad", None, False, False),
    ("uni_quad", None, True, False),
]


if __name__ == "__main__":
    ns = [int(v) for v in sys.argv[1:]] or [5, 8]
    for n in ns:
        for place, ball, yb, zb in RUNS:
            out = dict(n=n, place=place, ball=ball, ybound=yb, zbound=zb)
            for solver in ("CLARABEL", "SCS") if (place in ("opp", "uni") and ball in (None, 2.0)) else ("CLARABEL",):
                prob, _ = build(n, place, ball, yb, zb)
                kw = dict(eps=1e-9, max_iters=100000) if solver == "SCS" else {}
                try:
                    prob.solve(solver=solver, **kw)
                    out[solver] = [prob.status, None if prob.value is None else float(f"{prob.value:.7g}")]
                except Exception as exc:  # noqa: BLE001
                    out[solver] = ["error", str(exc)[:80]]
            print(json.dumps(out), flush=True)
