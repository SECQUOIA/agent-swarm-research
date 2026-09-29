"""Exact non-separable 2D exact-gap instances (alpha = 1).

H(y) = max_k (a_k . y + b_k) (convex, polyhedral), m = H - |y|^2 (so m + |y|^2
is convex: exact alphaBB with alpha = 1).  For a box B = [l1,u1] x [l2,u2]
    phi_B(y) = m(y) - q_B(y) = H(y) - (l1+u1) y1 - (l2+u2) y2 + l1 u1 + l2 u2,
a convex piecewise-linear function, minimized at a vertex of the arrangement of
H's breaklines restricted to B: a corner of B, a breakline/edge crossing, or a
triple point inside B.  All candidates are enumerated (a superset is harmless),
so node values and minimizers are exact up to floating point.
The instance is shifted so that min over [0,1]^2 of m equals eps (m is concave
on each linear piece of H, so its minimum is also at such a vertex).
"""
import itertools
import math
import numpy as np

TOL = 1e-12


class Poly2:
    def __init__(self, A, b, eps):
        self.A = np.asarray(A, float)          # K x 2 slopes
        self.b = np.asarray(b, float)          # K intercepts
        K = len(self.b)
        # breaklines between pairs: (a_j - a_k) . y = b_k - b_j
        self.pairs = [(j, k) for j in range(K) for k in range(j + 1, K)]
        # triple points
        tri = []
        for j, k, l in itertools.combinations(range(K), 3):
            M = np.array([self.A[j] - self.A[k], self.A[j] - self.A[l]])
            if abs(np.linalg.det(M)) < 1e-14:
                continue
            y = np.linalg.solve(M, [self.b[k] - self.b[j], self.b[l] - self.b[j]])
            tri.append(y)
        self.tri = np.array(tri).reshape(-1, 2)
        # shift so that min over the unit square of m is eps
        pts = self._candidates(0.0, 1.0, 0.0, 1.0)
        mv = self.H(pts) - (pts ** 2).sum(1)
        self.b = self.b - mv.min() + eps
        self.eps = eps

    def H(self, P):
        return (P @ self.A.T + self.b).max(1)

    def _candidates(self, l1, u1, l2, u2):
        pts = [np.array([[l1, l2], [l1, u2], [u1, l2], [u1, u2]])]
        for j, k in self.pairs:
            d = self.A[j] - self.A[k]
            r = self.b[k] - self.b[j]
            for x in (l1, u1):          # vertical edges: solve for y2
                if abs(d[1]) > 1e-15:
                    y2 = (r - d[0] * x) / d[1]
                    if l2 <= y2 <= u2:
                        pts.append(np.array([[x, y2]]))
            for y in (l2, u2):
                if abs(d[0]) > 1e-15:
                    y1 = (r - d[1] * y) / d[0]
                    if l1 <= y1 <= u1:
                        pts.append(np.array([[y1, y]]))
        if len(self.tri):
            T = self.tri
            ins = (T[:, 0] >= l1) & (T[:, 0] <= u1) & (T[:, 1] >= l2) & (T[:, 1] <= u2)
            if ins.any():
                pts.append(T[ins])
        return np.vstack(pts)

    def node(self, box):
        (l1, u1), (l2, u2) = box
        P = self._candidates(l1, u1, l2, u2)
        phi = self.H(P) - (l1 + u1) * P[:, 0] - (l2 + u2) * P[:, 1] + l1 * u1 + l2 * u2
        k = int(np.argmin(phi))
        return float(phi[k]), P[k]


def run(inst, rule, cap=200_000):
    stack = [((0.0, 1.0), (0.0, 1.0))]
    nodes = leaves = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > cap:
            return None, None
        v, y = inst.node(box)
        if v >= -TOL:
            leaves += 1
            continue
        a = [(y[i] - box[i][0]) * (box[i][1] - y[i]) for i in range(2)]
        w = [box[i][1] - box[i][0] for i in range(2)]
        if rule == "bis":
            cuts = [(int(np.argmax(w)), None)]
        elif rule == "omega":
            cuts = [(int(np.argmax(a)), y)]
        elif rule == "multi":
            cuts = [(i, y) for i in range(2) if a[i] > 0]
        else:
            raise ValueError(rule)
        boxes = [box]
        for i, yy in cuts:
            s = 0.5 * (box[i][0] + box[i][1]) if yy is None else float(yy[i])
            nb = []
            for b in boxes:
                l, u = b[i]
                if not (l < s < u):
                    raise RuntimeError("degenerate split")
                b1 = list(b); b1[i] = (l, s)
                b2 = list(b); b2[i] = (s, u)
                nb += [tuple(b1), tuple(b2)]
            boxes = nb
        stack.extend(boxes)
    return nodes, leaves


def valid_table(inst, g1, g2):
    G1, G2 = len(g1), len(g2)
    V = np.zeros((G1, G1, G2, G2), np.uint8)
    for a in range(G1):
        for b in range(a + 1, G1):
            for c in range(G2):
                for d in range(c + 1, G2):
                    V[a, b, c, d] = inst.node(((g1[a], g1[b]), (g2[c], g2[d])))[0] >= -TOL
    return V


def guill(inst, g1, g2):
    import ctypes
    from nd_sep import _lib
    V = np.ascontiguousarray(valid_table(inst, g1, g2))
    out = ctypes.c_int(0)
    _lib.guillotine_dp(len(g1), len(g2), V.ctypes.data, ctypes.byref(out))
    return out.value, V


def opt_ilp(V, time_limit=120):
    """Exact min partition (not necessarily guillotine) into valid grid boxes, via MILP."""
    from scipy.optimize import milp, LinearConstraint, Bounds
    from scipy.sparse import lil_matrix
    G1, G2 = V.shape[0], V.shape[2]
    boxes = [(a, b, c, d) for a in range(G1) for b in range(a + 1, G1)
             for c in range(G2) for d in range(c + 1, G2) if V[a, b, c, d]]
    A = lil_matrix(((G1 - 1) * (G2 - 1), len(boxes)))
    for k, (a, b, c, d) in enumerate(boxes):
        for i in range(a, b):
            for j in range(c, d):
                A[i * (G2 - 1) + j, k] = 1
    res = milp(c=np.ones(len(boxes)), constraints=[LinearConstraint(A.tocsr(), 1, 1)],
               integrality=np.ones(len(boxes)), bounds=Bounds(0, 1), options={"time_limit": time_limit})
    return (None if res.x is None else int(round(res.fun))), res.status
