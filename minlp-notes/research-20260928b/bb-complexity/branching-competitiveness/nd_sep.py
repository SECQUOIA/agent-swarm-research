"""Separable n-dimensional exact-gap instances: rules versus exact guillotine optimum on a grid.

m(y) = sum_i m_i(y_i) with each m_i a 1D polyhedral instance (poly1d.Inst,
alpha = 1).  Box validity: sum_i F_i(B_i) >= -TOL with
F_i(I) = min_{t in I} (m_i(t) - (t-l)(u-t)) computed exactly (knots and endpoints).

Rules (each splits one coordinate at the relaxation minimizer unless noted):
  omega    coordinate maximizing a_i(y) = (y_i - l_i)(u_i - y_i)
  deficit  coordinate with the most negative F_i(B_i) among those with a_i(y) > 0
  multi    every coordinate with a_i(y) > 0 (2^k-ary)
  bis      widest coordinate, midpoint
N_guill is bounded above by the exact guillotine optimum with cuts restricted
to a candidate grid (gdp.c); N_grid_opt (non-guillotine, same grid) by an ILP.
"""
import ctypes
import math
import os
import numpy as np
from poly1d import Inst, from_lines
from sep2d import node1

TOL = 1e-12
_lib = ctypes.CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), "libgdp.so"))
_lib.guillotine_dp.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)]


def run(Is, rule, cap=500_000):
    """Return (nodes, leaves) of the rule's tree, or (None, None) past cap."""
    n = len(Is)
    stack = [tuple((0.0, 1.0) for _ in range(n))]
    nodes = leaves = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > cap:
            return None, None
        vals, ys = zip(*[node1(I, l, u) for I, (l, u) in zip(Is, box)])
        if sum(vals) >= -TOL:
            leaves += 1
            continue
        a = [(y - l) * (u - y) for (l, u), y in zip(box, ys)]
        w = [u - l for (l, u) in box]
        cand = [j for j in range(n) if a[j] > 0]
        if rule == "bis":
            i = int(np.argmax(w)); cuts = [(i, 0.5 * (box[i][0] + box[i][1]))]
        elif rule == "omega":
            i = int(np.argmax(a)); cuts = [(i, ys[i])]
        elif rule == "deficit":
            i = min(cand, key=lambda j: vals[j]); cuts = [(i, ys[i])]
        elif rule == "multi":
            cuts = [(j, ys[j]) for j in cand]
        else:
            raise ValueError(rule)
        boxes = [box]
        for i, s in cuts:
            nb = []
            for b in boxes:
                l, u = b[i]
                b1 = list(b); b1[i] = (l, s)
                b2 = list(b); b2[i] = (s, u)
                nb += [tuple(b1), tuple(b2)]
            boxes = nb
        stack.extend(boxes)
    return nodes, leaves


def Ftable(I, xs):
    G = len(xs)
    F = np.full((G, G), np.inf)
    for a in range(G):
        for b in range(a + 1, G):
            F[a, b] = node1(I, xs[a], xs[b])[0]
    return F


def guill_grid(Is, grids):
    """Exact min guillotine certificate on the product grid (2D)."""
    assert len(Is) == 2
    F1, F2 = Ftable(Is[0], grids[0]), Ftable(Is[1], grids[1])
    G1, G2 = len(grids[0]), len(grids[1])
    V = (F1[:, :, None, None] + F2[None, None, :, :] >= -TOL).astype(np.uint8)
    V = np.ascontiguousarray(V)
    out = ctypes.c_int(0)
    rc = _lib.guillotine_dp(G1, G2, V.ctypes.data, ctypes.byref(out))
    assert rc == 0
    return out.value


def grid_opt_ilp(Is, grids, time_limit=120):
    """Exact min (not necessarily guillotine) partition into valid grid boxes (2D), via MILP."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    F1, F2 = Ftable(Is[0], grids[0]), Ftable(Is[1], grids[1])
    G1, G2 = len(grids[0]), len(grids[1])
    boxes = [(a, b, c, d) for a in range(G1) for b in range(a + 1, G1)
             for c in range(G2) for d in range(c + 1, G2) if F1[a, b] + F2[c, d] >= -TOL]
    ncell = (G1 - 1) * (G2 - 1)
    A = lil_matrix((ncell, len(boxes)))
    for k, (a, b, c, d) in enumerate(boxes):
        for i in range(a, b):
            for j in range(c, d):
                A[i * (G2 - 1) + j, k] = 1
    res = milp(c=np.ones(len(boxes)), constraints=[LinearConstraint(A.tocsr(), 1, 1)],
               integrality=np.ones(len(boxes)), bounds=Bounds(0, 1),
               options={"time_limit": time_limit})
    if res.x is None:
        return None, res.status
    return int(round(res.fun)), res.status


def random_coord(rng, eps_i, k):
    """1D polyhedral m_i = max of k random lines (H-space) minus t^2, shifted to min eps_i."""
    lines = []
    for _ in range(k):
        p = rng.uniform(0, 1)
        mu = np.exp(rng.uniform(np.log(1e-4), np.log(0.5)))
        slope_extra = rng.normal(0, 1.0) * rng.choice([0.0, 1.0])
        lines.append((2 * p + slope_extra, -p * p + mu - slope_extra * p))
    lines.append((0.0, 0.3)); lines.append((2.0, -1.0 + 0.3))
    xs, ms = from_lines(lines)
    ms = ms - ms.min() + eps_i
    return Inst(xs, ms)


def default_grid(I, G):
    pts = set(np.linspace(0, 1, G)) | set(float(x) for x in I.x if len(I.x) <= 60)
    return np.array(sorted(pts))
