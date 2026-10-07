"""Independent leaf counts for gadget chains (delta = 0, theorem base split), without the authors' code.

With delta = 0 and all unary terms in the gadget factors, the connecting factors are zero, so the
class bound of a chain box is the sum of the gadget class bounds (the connecting factor can take the
product of the neighbouring marginals).  Only y is shared inside a gadget; class (a) gives S_y = P_2
(u_y = c y^2 is quadratic), class b_d gives S_y = P_d.

Gadget bound on C = Cx x Cy x Cz (Lemma 1.2 reduced to y):
    V(C) = sup_{rho in P_d} [ min_{Cy} (A + rho) + min_{Cy} (B - rho) ],
    A(y) = min_{x in Cx} (y1^2 x^2 + b x y) + c y^2,   B(y) = min_{z in Cz} (u(z) + b' y z).
A and B are quadratic between explicit breakpoints.  Exchange method: grid LP (upper bound on V),
and the grid-optimal rho evaluated exactly on every piece (lower bound on V).
B&B: widest-side bisection at midpoints, first index on ties, fstar = 0; prune if the lower bound
>= -eps, split if the upper bound < -eps, otherwise count as ambiguous.
Usage: python3 check_bb.py d eps G1 G2 ...
"""
import sys
import time
import numpy as np
from numpy.polynomial import chebyshev as C, polynomial as P
from scipy.optimize import linprog

y1, eta, epsv = 0.38, 0.05, 0.02
b, bp, c = 2 * y1, 2 * eta + 2 * (1 - eta) * (1 - y1), 1 + eta + epsv
z1, k = 2 * eta * y1 / bp, 2 * (1 - eta) * y1


def u(z):
    a = np.abs(z)
    return np.where(a <= z1, bp ** 2 * z ** 2 / (4 * eta), (bp * a + k) ** 2 / 4 - (1 - eta) * y1 ** 2)


def zu(y):  # unconstrained minimiser of u(z) + bp y z (u convex, u'(zu) = -bp y)
    a = np.abs(y)
    return np.where(a <= y1, -2 * eta * y / bp, -np.sign(y) * (2 * a - k) / bp)


def zu_inv(z):
    if abs(z) <= z1:
        return -bp * z / (2 * eta)
    return (k - bp * z) / 2 if z < 0 else -(k + bp * z) / 2


def make_AB(lx, ux, lz, uz):
    def A(y):
        x = np.clip(-y / y1, lx, ux)
        return y1 * y1 * x * x + b * x * y + c * y * y

    def B(y):
        z = np.clip(zu(y), lz, uz)
        return u(z) + bp * y * z
    return A, B


def pieces(lx, ux, ly, uy, lz, uz):
    bps = {ly, uy, -y1 * ux, -y1 * lx, y1, -y1, zu_inv(lz), zu_inv(uz)}
    return sorted(t for t in bps if ly <= t <= uy)


def piece_min(f_on, rho, pts):
    """min over [pts[0], pts[-1]] of f + rho, f quadratic on each [pts[i], pts[i+1]]."""
    best, arg = np.inf, None
    for a, bb in zip(pts[:-1], pts[1:]):
        if bb - a < 1e-15:
            continue
        s = np.array([a, 0.5 * (a + bb), bb])
        q = P.Polynomial(P.polyfit(s, f_on(s), 2))
        p = q + rho
        cands = [a, bb] + [r.real for r in p.deriv().roots() if abs(r.imag) < 1e-9 and a < r.real < bb]
        cands = np.array(cands)
        vals = f_on(cands) + rho(cands)
        j = int(np.argmin(vals))
        if vals[j] < best:
            best, arg = float(vals[j]), float(cands[j])
    return best, arg


def V(box, d, rounds=40, tol=1e-10):
    lx, ux, ly, uy, lz, uz = box
    A, B = make_AB(lx, ux, lz, uz)
    pts = pieces(lx, ux, ly, uy, lz, uz)
    mid, half = 0.5 * (ly + uy), 0.5 * (uy - ly)
    grid = set((mid + half * np.cos(np.linspace(0, np.pi, 201))).tolist()) | set(pts)
    for it in range(rounds):
        y = np.array(sorted(grid)); m = len(y)
        T = C.chebvander((y - mid) / half, d)[:, 1:]
        # vars: coeffs (d), s1, s2; max s1 + s2;  s1 - T coef <= A,  s2 + T coef <= B
        Aub = np.vstack([np.hstack([-T, np.ones((m, 1)), np.zeros((m, 1))]),
                         np.hstack([T, np.zeros((m, 1)), np.ones((m, 1))])])
        rhs = np.concatenate([A(y), B(y)])
        cc = np.zeros(d + 2); cc[-2:] = -1
        res = linprog(cc, A_ub=Aub, b_ub=rhs, bounds=[(None, None)] * (d + 2), method="highs")
        up = -res.fun
        coef = np.concatenate([[0.0], res.x[:d]])
        rho = C.Chebyshev(coef, domain=[ly, uy]).convert(kind=P.Polynomial)
        m1, a1 = piece_min(A, rho, pts)
        m2, a2 = piece_min(B, -rho, pts)
        lo = m1 + m2
        if up - lo <= tol:
            break
        grid |= {a1, a2}
    return lo, up


def bb(d, eps, G):
    n = 3 * G
    memo = {}
    stack = [(np.full(n, -1.0), np.full(n, 1.0))]
    leaves = nodes = amb = 0
    pm, sm, wid = np.inf, np.inf, 0.0
    while stack:
        l, uu = stack.pop(); nodes += 1
        lo = up = 0.0
        for g in range(G):
            key = (l[3 * g], uu[3 * g], l[3 * g + 1], uu[3 * g + 1], l[3 * g + 2], uu[3 * g + 2])
            if key not in memo:
                memo[key] = V(key, d)
            lo += memo[key][0]; up += memo[key][1]
            wid = max(wid, memo[key][1] - memo[key][0])
        if lo >= -eps:
            leaves += 1; pm = min(pm, lo + eps); continue
        if up >= -eps:
            amb += 1
        else:
            sm = min(sm, -eps - up)
        j = int(np.argmax(uu - l)); mdp = 0.5 * (l[j] + uu[j])
        u1 = uu.copy(); u1[j] = mdp; l2 = l.copy(); l2[j] = mdp
        stack.append((l, u1)); stack.append((l2, uu))
    return dict(leaves=leaves, nodes=nodes, ambiguous=amb, min_prune_margin=pm, min_split_margin=sm,
                max_bracket_width=wid, distinct_gadget_boxes=len(memo))


if __name__ == "__main__":
    d, eps = int(sys.argv[1]), float(sys.argv[2])
    for G in map(int, sys.argv[3:]):
        t0 = time.time()
        r = bb(d, eps, G)
        print("S_y = P_%d (%s) eps=%g G=%d n=%d: %s (%.1fs)" % (d, "class a" if d == 2 else "b%d" % d, eps, G, 3 * G,
                                                               r, time.time() - t0), flush=True)
