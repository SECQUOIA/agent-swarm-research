"""Exact rational node counts on the McCormick kink family, widest-side selection with ties to x,
for the deterministic rules (revision after review): the clip C_0.2 at a = 1/6 (float runs give
19,541 because rounding breaks width ties w_x = w_y toward y) and the recentring clamp RC_0.2
(eps = 0 gives the supremum over eps, since a deterministic rule's tree only grows as eps falls)."""
from fractions import Fraction as F


def run(a, eps, rule, th=F(1, 5)):
    stack = [(F(0), F(1), F(0), F(1))]
    T = 0
    while stack:
        lx, ux, ly, uy = stack.pop()
        T += 1
        if not (lx < a < ux):
            continue
        wx, wy = ux - lx, uy - ly
        if wy * (a - lx) * (ux - a) / wx <= eps:
            continue
        rho = (a - lx) / wx
        i, l, u, p = (0, lx, ux, a) if wx >= wy else (1, ly, uy, ly + rho * wy)
        w = u - l
        if rule == "clip":
            s = min(max(p, l + th * w), u - th * w)
        elif p < l + th * w:
            s = l + max(th * w, 2 * (p - l))
        elif p > u - th * w:
            s = u - max(th * w, 2 * (u - p))
        else:
            s = p
        if i == 0:
            stack += [(s, ux, ly, uy), (lx, s, ly, uy)]
        else:
            stack += [(lx, ux, s, uy), (lx, ux, ly, s)]
    return T


if __name__ == "__main__":
    a = F(1, 6)
    print("clip 0.2, a = 1/6:", [run(a, F(1, 10 ** k), "clip") for k in range(2, 9)], "at eps = 1e-2..1e-8")
    for a in (F(1, 6), F(3, 238), F(1999, 10000), F(1, 4), F(1, 3)):
        print(f"recenter 0.2, a = {a}: eps = 0 -> {run(a, F(0), 'recenter')}; eps = 1e-8 -> "
              f"{run(a, F(1, 10 ** 8), 'recenter')}")
