"""Exact rational branch-and-bound on the kink family (second revision, after the recheck).

f_a = L|x-a| + c (x-a)(y-b), c = -1, L > max(b, 1-b) (e.g. L = 2, b = sqrt2 - 1).  All node data used
by the rules are rational (they do not involve b):
  straddling box (a in (l_x,u_x)):  LB = -w_y (a-l_x)(u_x-a)/w_x,  xhat = a,  yhat = l_y + rho w_y,
                                    rho = (a-l_x)/w_x   (c < 0; see Propositions 5.4(a), 5.7);
  non-straddling box: valid (sub-box of the Theorem 4.4 certificate), pruned.
Width ties w_x = w_y are therefore decided exactly (the floating-point runs of clamp_cantor.py break some
ties toward y by rounding, which adds a few nodes).
Rules: LP(1,beta) with widest side (ties to x or to y) or x only; INC = bisection with the branching point
set to the incumbent (a, y*) when (i) the incumbent's coordinate is strictly inside the interval
('coordinate test', as in face_bb.py) or (ii) additionally the incumbent point lies in the node box
('point test', the rule quoted from Tawarmalani-Sahinidis p.243)."""
from fractions import Fraction as Fr


def run(a, eps, rule, beta=Fr(1, 5), tie="x", inc=None, test="coord", cap=10 ** 7):
    stack = [(Fr(0), Fr(1), Fr(0), Fr(1))]
    n = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        n += 1
        if n > cap:
            return None
        if not (lx < a < ux):
            continue                      # non-straddling: valid, pruned
        wx, wy = ux - lx, uy - ly
        if wy * (a - lx) * (ux - a) / wx <= eps:
            continue                      # LB >= -eps
        rho = (a - lx) / wx
        if rule == "x":
            i = 0
        else:
            i = 0 if (wx > wy or (wx == wy and tie == "x")) else 1
        l, u = (lx, ux) if i == 0 else (ly, uy)
        w = u - l
        if rule == "INC":
            xs = inc[i]
            inside = (lx <= inc[0] <= ux and ly <= inc[1] <= uy) if test == "point" else True
            p = xs if (inside and l < xs < u) else (l + u) / 2
        else:
            xhat = a if i == 0 else ly + rho * wy
            p = min(max(xhat, l + beta * w), u - beta * w)
        if i == 0:
            stack += [(p, ux, ly, uy), (lx, p, ly, uy)]
        else:
            stack += [(lx, ux, p, uy), (lx, ux, ly, p)]
    return n


if __name__ == "__main__":
    E = [Fr(1, 10 ** k) for k in range(2, 9)]
    a = Fr(1, 6)
    print("[1] a = 1/6, LP(1,1/5), widest side, ties to x, exact:", [run(a, e, "LP") for e in E])
    print("    same, ties to y:", [run(a, e, "LP", tie="y") for e in E[:6]])
    print("    same, x only:", [run(a, e, "x") for e in E])
    a2 = Fr(1999, 10000)
    print("[2] a = 0.1999, LP(1,1/5), widest side, ties to x, eps = 1e-4, 1e-6, 1e-8:",
          [run(a2, e, "LP") for e in (E[2], E[4], E[6])])
    a3 = Fr(1, 3)
    E5 = E[:5]
    print("[3] a = 1/3, incumbent branching (INC), eps = 1e-2 .. 1e-6:")
    for tie in ("x", "y"):
        for inc in ((a3, Fr(1, 2)), (a3, Fr(0))):
            for test in ("coord", "point"):
                print(f"    ties to {tie}, incumbent {tuple(str(v) for v in inc)}, {test} test:",
                      [run(a3, e, "INC", tie=tie, inc=inc, test=test) for e in E5])
