"""Closing audit (b), item 3: exact replay of the kink-family node counts and of the
incumbent-branching remark (Proposition 5.4(d)) of face-exact-node-complexity.md.

Written from the note's definitions only (no code from the note or the reviews):
  f_{a,b}(x,y) = L|x-a| + c (x-a)(y-b) on [0,1]^2, c = -1, L = 2, b = sqrt(2) - 1,
  termwise McCormick on the product, fixed incumbent UBD = f* = 0, prune iff LB >= -eps.
Node bounds are computed exactly in Q(sqrt 2) by enumerating the vertices of the
subdivision of the box by the line x = a and the McCormick switching diagonal
(f_B is convex piecewise linear on that subdivision).  No closed form is assumed.
Rules: LP(1,beta) (relaxation point, clamped), SCIPdef (midpull 0.75, times the relative
width below 0.5, clamp 0.2), bisection, INC (bisection with the incumbent coordinate,
coordinate test or point test), product-score strong branching with the LP(1,.2) point.
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
from fractions import Fraction as Fr


class Q2:
    """p + q sqrt(2), p, q rational; exact order."""
    __slots__ = ("p", "q")

    def __init__(self, p, q=0):
        self.p = Fr(p); self.q = Fr(q)

    def __add__(self, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(self.p + o.p, self.q + o.q)
    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.p, -self.q)

    def __sub__(self, o):
        return self + (-(o if isinstance(o, Q2) else Q2(o)))

    def __rsub__(self, o):
        return Q2(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Q2) else Q2(o)
        return Q2(self.p * o.p + 2 * self.q * o.q, self.p * o.q + self.q * o.p)
    __rmul__ = __mul__

    def sign(self):
        p, q = self.p, self.q
        if p >= 0 and q >= 0:
            return 0 if (p == 0 and q == 0) else 1
        if p <= 0 and q <= 0:
            return -1
        # opposite signs: compare p^2 and 2 q^2
        if p > 0:
            return 1 if p * p > 2 * q * q else (-1 if p * p < 2 * q * q else 0)
        return 1 if 2 * q * q > p * p else (-1 if 2 * q * q < p * p else 0)

    def __lt__(self, o):
        return (self - o).sign() < 0

    def __le__(self, o):
        return (self - o).sign() <= 0

    def __gt__(self, o):
        return (self - o).sign() > 0

    def __ge__(self, o):
        return (self - o).sign() >= 0

    def __float__(self):
        return float(self.p) + float(self.q) * 2 ** 0.5


B = Q2(-1, 1)   # b = sqrt(2) - 1
L = 2
C = -1


def fB(box, X, Y):
    """Relaxation value at (x, y) = (a + X, b + Y) on box given in shifted coords."""
    Xl, Xu, Yl, Yu = box
    # termwise McCormick convex envelope of C*X*Y (C = -1): -cave(XY)
    cave = min(Xu * Y + X * Yl - Xu * Yl, Xl * Y + X * Yu - Xl * Yu)
    absX = X if X >= 0 else -X
    return L * absX + C * cave


def node_lb(a, lx, ux, ly, uy):
    """Exact min of f_B over the box, by vertex enumeration."""
    Xl, Xu = lx - a, ux - a
    Yl, Yu = Q2(ly) - B, Q2(uy) - B
    box = (Q2(Xl), Q2(Xu), Yl, Yu)
    cand = [(Q2(Xl), Yl), (Q2(Xl), Yu), (Q2(Xu), Yl), (Q2(Xu), Yu)]
    if Xl < 0 < Xu:
        # x = a meets the bottom/top edges and the switching diagonal (Xl,Yl)-(Xu,Yu)
        t = Fr(-Xl, Xu - Xl)
        cand += [(Q2(0), Yl), (Q2(0), Yu), (Q2(0), Yl + t * (Yu - Yl))]
    vals = [fB(box, X, Y) for X, Y in cand]
    best = min(vals)
    return best


def relax_point(a, lx, ux, ly, uy):
    """Minimizer of f_B for a straddling box, found by checking the vertex candidates;
    asserts uniqueness among candidates (the note's Proposition 5.4(a))."""
    Xl, Xu = lx - a, ux - a
    Yl, Yu = Q2(ly) - B, Q2(uy) - B
    box = (Q2(Xl), Q2(Xu), Yl, Yu)
    t = Fr(-Xl, Xu - Xl)
    cands = [(Q2(Xl), Yl, lx, ly), (Q2(Xl), Yu, lx, uy), (Q2(Xu), Yl, ux, ly), (Q2(Xu), Yu, ux, uy),
             (Q2(0), Yl, a, ly), (Q2(0), Yu, a, uy), (Q2(0), Yl + t * (Yu - Yl), a, ly + t * (uy - ly))]
    vals = [(fB(box, X, Y), xx, yy) for X, Y, xx, yy in cands]
    m = min(v[0] for v in vals)
    arg = [(xx, yy) for v, xx, yy in vals if v <= m]
    assert len(set(arg)) == 1, arg
    return arg[0]


def clamp(p, l, u, beta):
    return min(max(p, l + beta * (u - l)), u - beta * (u - l))


def run(a, eps, rule, beta=Fr(1, 5), tie="x", inc=None, test="coord", cap=2 * 10 ** 6):
    a = Fr(a); eps = Fr(eps)
    stack = [(Fr(0), Fr(1), Fr(0), Fr(1), None)]
    n = 0
    while stack:
        lx, ux, ly, uy, lb = stack.pop()
        n += 1
        if n > cap:
            return None
        if lb is None:
            lb = node_lb(a, lx, ux, ly, uy)
        if lb >= Q2(-eps):
            continue
        assert lx < a < ux    # only straddling boxes can have negative bounds
        wx, wy = ux - lx, uy - ly
        if rule == "SB":
            # product-score strong branching over {x, y} with the LP(1,beta) point
            xh, yh = relax_point(a, lx, ux, ly, uy)
            best = None
            for i in (0, 1):
                if i == 0:
                    p = clamp(xh, lx, ux, beta)
                    kids = [(lx, p, ly, uy), (p, ux, ly, uy)]
                else:
                    p = clamp(yh, ly, uy, beta)
                    kids = [(lx, ux, ly, p), (lx, ux, p, uy)]
                lbs = [node_lb(a, *k) for k in kids]
                d = [max(v - lb, Q2(Fr(1, 10 ** 9))) for v in lbs]
                sc = d[0] * d[1]
                if best is None or sc > best[0]:      # ties keep x
                    best = (sc, kids, lbs)
            _, kids, lbs = best
            stack += [(k[0], k[1], k[2], k[3], v) for k, v in zip(kids[::-1], lbs[::-1])]
            continue
        if rule == "xonly":
            i = 0
        else:
            i = 0 if (wx > wy or (wx == wy and tie == "x")) else 1
        l, u = (lx, ux) if i == 0 else (ly, uy)
        w = u - l
        if rule == "LP":
            xh, yh = relax_point(a, lx, ux, ly, uy)
            p = clamp((xh, yh)[i], l, u, beta)
        elif rule == "xonly":
            xh, yh = relax_point(a, lx, ux, ly, uy)
            p = clamp(xh, l, u, beta)
        elif rule == "SCIPdef":
            xh, yh = relax_point(a, lx, ux, ly, uy)
            mp = Fr(3, 4) if w >= Fr(1, 2) else Fr(3, 4) * w     # relative width = w (global [0,1])
            p = clamp(mp * (l + u) / 2 + (1 - mp) * (xh, yh)[i], l, u, Fr(1, 5))
        elif rule == "bisect":
            p = (l + u) / 2
        elif rule == "INC":
            xs = Fr(inc[i])
            ok = l < xs < u
            if test == "point":
                ok = ok and (lx <= inc[0] <= ux and ly <= inc[1] <= uy)
            p = xs if ok else (l + u) / 2
        if i == 0:
            stack += [(p, ux, ly, uy, None), (lx, p, ly, uy, None)]
        else:
            stack += [(lx, ux, p, uy, None), (lx, ux, ly, p, None)]
    return n


if __name__ == "__main__":
    E = [Fr(1, 10 ** k) for k in range(2, 9)]
    a = Fr(1, 6)
    # sanity: closed-form straddling bound -w_y (a-l)(u-a)/w_x against vertex enumeration
    import random
    random.seed(1)
    bad = 0
    for _ in range(300):
        lx = Fr(random.randint(0, 50), 300); ux = Fr(random.randint(51, 300), 300)
        ly = Fr(random.randint(0, 150), 300); uy = Fr(random.randint(151, 300), 300)
        lb = node_lb(a, lx, ux, ly, uy)
        cf = -(uy - ly) * (a - lx) * (ux - a) / (ux - lx)
        bad += (lb - Q2(cf)).sign() != 0
    print("closed-form straddling bound vs exact vertex enumeration: mismatches", bad, "of 300")
    print("[1] a = 1/6, LP(1,1/5), widest, ties x :", [run(a, e, "LP") for e in E])
    print("    a = 1/6, LP(1,1/5), widest, ties y :", [run(a, e, "LP", tie="y") for e in E[:6]])
    print("    a = 1/6, LP(1,1/5), x only         :", [run(a, e, "xonly") for e in E])
    print("    a = 1/6, LP(1,0), widest, ties x   :", [run(a, e, "LP", beta=Fr(0)) for e in E])
    print("    a = 1/6, LP(1,1/10), widest, ties x:", [run(a, e, "LP", beta=Fr(1, 10)) for e in E])
    print("    a = 1/6, INC (1/6,1/2), ties x     :", [run(a, e, "INC", inc=(a, Fr(1, 2))) for e in E])
    print("    a = 1/6, SCIPdef, widest, ties x   :", [run(a, e, "SCIPdef") for e in E])
    print("    a = 1/6, bisection, widest, ties x :", [run(a, e, "bisect") for e in E])
    print("    a = 1/6, product-score SB, LP(1,.2):", [run(a, e, "SB") for e in E])
    a2 = Fr(1999, 10000)
    print("[2] a = 0.1999, LP(1,1/5), ties x, eps 1e-4,1e-6,1e-8:", [run(a2, e, "LP") for e in (E[2], E[4], E[6])])
    print("[3] incumbent branching, eps = 1e-2 .. 1e-6")
    for aa in (Fr(1, 3), Fr(1, 6)):
        for tie in ("x", "y"):
            for inc in ((aa, Fr(1, 2)), (aa, Fr(0))):
                for test in ("coord", "point"):
                    print(f"    a={aa} ties {tie} inc=({inc[0]},{inc[1]}) {test:5s}:",
                          [run(aa, e, "INC", tie=tie, inc=inc, test=test) for e in E[:5]])
