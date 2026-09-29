"""Reviewer's independent branch-and-bound on the kink family (Sections 5.2-5.3 of the note).

f_{a,b}(x,y) = L|x-a| + c (x-a)(y-b) on [0,1]^2, termwise McCormick on c X Y (X = x-a, Y = y-b).
Node bound: exact minimum of the convex piecewise-linear relaxation over the box, computed by
enumerating the vertices of the arrangement {box edges, X = 0, crease of the McCormick max/min}
(the minimum of a convex PL function over a rectangle is attained at such a vertex).  This is
independent of the author's LP code and of the closed form used by the note; the closed form
LB = -|c| w_y (a-l_x)(u_x-a)/w_x for straddling boxes is cross-checked against it.

Incumbent fixed at f* = 0; a node is pruned iff LB >= -eps; processed = generated nodes.

Parts:
  [1] closed form vs enumeration on random boxes
  [2] scout instance (L=2, c=-1, a=1/3, b=sqrt2-1): bisection and R(alpha,beta) rules, widest side
      (ties -> x), min-score and product-score strong branching; SCIP's actual default point rule
      (midpull 0.75, reduced by relative domain width below 0.5, clamp 0.2)
  [3] Prop 5.4(b) clamp count: R(1,0.2) with a close to a clamp point
  [4] Prop 5.5(b): x-only selection with alpha < 1 (log growth)
"""
import math
import random
import sys

L0, C0 = 2.0, -1.0
A0, B0 = 1.0 / 3.0, math.sqrt(2.0) - 1.0


def relax(box, L=L0, c=C0, a=A0, b=B0):
    lx, ux, ly, uy = box
    Xl, Xu, Yl, Yu = lx - a, ux - a, ly - b, uy - b
    if c > 0:
        p1 = (c * Yl, c * Xl, -c * Xl * Yl)      # c*(Yl X + Xl Y - Xl Yl)
        p2 = (c * Yu, c * Xu, -c * Xu * Yu)
        env = lambda X, Y: max(p1[0] * X + p1[1] * Y + p1[2], p2[0] * X + p2[1] * Y + p2[2])
    else:
        p1 = (c * Yu, c * Xl, -c * Xl * Yu)      # c*(Yu X + Xl Y - Xl Yu)  (c<0: min of overestimators)
        p2 = (c * Yl, c * Xu, -c * Xu * Yl)
        env = lambda X, Y: max(p1[0] * X + p1[1] * Y + p1[2], p2[0] * X + p2[1] * Y + p2[2])
    fB = lambda X, Y: L * abs(X) + env(X, Y)
    # crease of env: (p1-p2).(X,Y,1) = 0 ; crease of |X|: X = 0
    d = (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])
    cand = [(Xl, Yl), (Xl, Yu), (Xu, Yl), (Xu, Yu)]
    if Xl < 0 < Xu:
        cand += [(0.0, Yl), (0.0, Yu)]
        if abs(d[1]) > 0:
            cand.append((0.0, -d[2] / d[1]))
    if abs(d[1]) > 0:
        for X in (Xl, Xu):
            cand.append((X, -(d[0] * X + d[2]) / d[1]))
    if abs(d[0]) > 0:
        for Y in (Yl, Yu):
            cand.append((-(d[1] * Y + d[2]) / d[0], Y))
    tol = 1e-15
    best = None
    for (X, Y) in cand:
        if Xl - tol <= X <= Xu + tol and Yl - tol <= Y <= Yu + tol:
            X = min(max(X, Xl), Xu)
            Y = min(max(Y, Yl), Yu)
            v = fB(X, Y)
            if best is None or v < best[0] - 1e-15:
                best = (v, X + a, Y + b)
    return best


def closed_form(box, c=C0, a=A0):
    lx, ux, ly, uy = box
    return -abs(c) * (uy - ly) * (a - lx) * (ux - a) / (ux - lx)


def point_R(alpha, beta, l, u, xh):
    w = u - l
    p = alpha * xh + (1 - alpha) * 0.5 * (l + u)
    return min(max(p, l + beta * w), u - beta * w)


def point_scip(l, u, xh, gl=0.0, gu=1.0, midpull=0.75, trig=0.5, clamp=0.2):
    rel = (u - l) / (gu - gl)
    mp = midpull * rel if rel < trig else midpull
    p = mp * 0.5 * (l + u) + (1 - mp) * xh
    w = u - l
    return min(max(p, l + clamp * w), u - clamp * w)


def children(box, var, p):
    lx, ux, ly, uy = box
    if var == 0:
        return (lx, p, ly, uy), (p, ux, ly, uy)
    return (lx, ux, ly, p), (lx, ux, p, uy)


def run(rule, eps, cap=200000, **kw):
    """rule(box, lb, xhat, yhat, kw) -> (var, point)."""
    root = (0.0, 1.0, 0.0, 1.0)
    stack = [root]
    nodes = 0
    while stack:
        box = stack.pop()
        nodes += 1
        if nodes > cap:
            return None
        lb, xh, yh = relax(box, **kw)
        if lb >= -eps:
            continue
        var, p = rule(box, lb, xh, yh, kw)
        stack.extend(children(box, var, p))
    return nodes


def widest(box):
    return 0 if box[1] - box[0] >= box[3] - box[2] else 1


def mk_R(alpha, beta, sel="w"):
    def rule(box, lb, xh, yh, kw):
        if sel == "w":
            var = widest(box)
            return (var, point_R(alpha, beta, box[0], box[1], xh) if var == 0
                    else point_R(alpha, beta, box[2], box[3], yh))
        if sel == "x":
            return 0, point_R(alpha, beta, box[0], box[1], xh)
        cands = []
        for var in (0, 1):
            p = point_R(alpha, beta, box[0], box[1], xh) if var == 0 else point_R(alpha, beta, box[2], box[3], yh)
            c1, c2 = children(box, var, p)
            l1, l2 = relax(c1, **kw)[0], relax(c2, **kw)[0]
            if sel == "s":
                score = min(l1, l2)
            else:
                score = max(l1 - lb, 1e-9) * max(l2 - lb, 1e-9)
            cands.append((score, -var, var, p))
        cands.sort(reverse=True)
        return cands[0][2], cands[0][3]
    return rule


def rule_bisect(box, lb, xh, yh, kw):
    var = widest(box)
    return var, (0.5 * (box[0] + box[1]) if var == 0 else 0.5 * (box[2] + box[3]))


def rule_scip(sel="w"):
    def rule(box, lb, xh, yh, kw):
        var = widest(box) if sel == "w" else 0
        return (var, point_scip(box[0], box[1], xh) if var == 0 else point_scip(box[2], box[3], yh))
    return rule


def part1():
    rng = random.Random(1)
    worst = 0.0
    for _ in range(3000):
        lx = rng.uniform(0, A0 - 1e-3); ux = rng.uniform(A0 + 1e-3, 1)
        ly = rng.uniform(0, 0.99); uy = rng.uniform(ly + 1e-3, 1)
        box = (lx, ux, ly, uy)
        v, xh, yh = relax(box)
        worst = max(worst, abs(v - closed_form(box)))
        assert abs(xh - A0) < 1e-12
    print(f"[1] straddling boxes: max |enumeration - closed form| = {worst:.2e} over 3000 boxes; xhat = a in all")


def part2():
    eps_list = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
    rules = [("bisect", rule_bisect), ("R(1,.2)w", mk_R(1, .2)), ("R(.75,.1)w", mk_R(.75, .1)),
             ("R(.7,.01)w", mk_R(.7, .01)), ("R(.25,.2)w", mk_R(.25, .2)), ("R(.25,.2)sp", mk_R(.25, .2, "p")),
             ("R(.25,.2)s", mk_R(.25, .2, "s")), ("SCIPactual w", rule_scip("w")), ("SCIPactual x", rule_scip("x"))]
    print("[2] scout kink instance, processed nodes for eps =", eps_list)
    for name, r in rules:
        row = []
        for e in eps_list:
            n = run(r, e, cap=100000)
            row.append("cap" if n is None else str(n))
        print(f"    {name:14s} " + " ".join(f"{s:>7s}" for s in row))
        sys.stdout.flush()


def part3():
    print("[3] Prop 5.4(b): R(1,0.2), widest side (ties->x), a near the clamp point 0.2; nodes at eps=1e-4,1e-6,1e-8")
    for a in (0.2 - 1e-2, 0.2 - 1e-3, 0.2 - 1e-4, 0.2 - 1e-5, 0.2 - 1e-6, 0.3, 1 / 3):
        row = [run(mk_R(1, .2), e, cap=400000, a=a) for e in (1e-4, 1e-6, 1e-8)]
        note_bound = 1 + math.log(1 / min(a, 1 - a)) / math.log(1 / 0.2)
        print(f"    a={a:.7f}: nodes {row}   (note's clamp bound 1+log(1/min(a,1-a))/log5 = {note_bound:.2f})")


def part4():
    print("[4] Prop 5.5(b): x-only selection, nodes vs note bound 1+2ceil(log(|c|/(4eps))/log(1/(1-beta')))")
    for (al, be) in ((.75, .1), (.25, .2), (.7, .01)):
        bp = max(be, (1 - al) / 2)
        out = []
        for e in (1e-3, 1e-4, 1e-5, 1e-6, 1e-8):
            n = run(mk_R(al, be, "x"), e)
            bnd = 1 + 2 * math.ceil(math.log(1 / (4 * e)) / math.log(1 / (1 - bp)))
            out.append(f"{n}<={bnd}")
        print(f"    R({al},{be}) x-only: " + ", ".join(out))


if __name__ == "__main__":
    part1()
    part2()
    part3()
    part4()
