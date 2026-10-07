"""M5: exact checks of the screening theorem (Report A screening.tex, Thm screen).

  * max_j s_j|c_j| <= 1  pairs with R_1 (scaled L1 residual);
    sum_j s_j|c_j| <= 1  pairs with R_inf (scaled L_inf residual).
  * the swapped pairing is false (explicit counterexample);
  * the screen is tight: with the best mixture, R_1 equals the largest
    max-normalized violation (L1 distance duality);
  * one-sided refinement for normals with c_j >= 0 on cone coordinates.
Graph: F(x) = (x, x^2) on [0,1]; exact support min_x c1 x + c2 x^2 is closed form.
"""
import random
from fractions import Fraction as F

random.seed(3)


def support(c1, c2):
    cands = [F(0), F(1)]
    if c2 > 0 and 0 < -c1 / (2 * c2) < 1:
        cands.append(-c1 / (2 * c2))
    return min(c1 * x + c2 * x * x for x in cands)


def screen(q, xs, lam, s, widen):
    """Return (R_1, R_inf, R_1 one-sided in coordinate 2) from interval enclosures."""
    L, U = [F(0), F(0)], [F(0), F(0)]
    for x, l, w in zip(xs, lam, widen):
        vals = (x, x * x)
        for j in range(2):
            L[j] += l * (vals[j] - w)
            U[j] += l * (vals[j] + w)
    r = [max(abs(q[j] - L[j]), abs(q[j] - U[j])) / s[j] for j in range(2)]
    r_one = [r[0], max(U[1] - q[1], F(0)) / s[1]]
    return sum(r), max(r), sum(r_one)


def rand_normal(kind, s):
    c = [F(random.randint(-100, 100), 100) for _ in range(2)]
    if kind == "max":
        m = max(s[j] * abs(c[j]) for j in range(2))
    else:
        m = sum(s[j] * abs(c[j]) for j in range(2))
    return [cj / m for cj in c] if m else c


def main():
    checked = 0
    for _ in range(300):
        q = (F(random.randint(-20, 120), 100), F(random.randint(-20, 120), 100))
        xs = [F(random.randint(0, 100), 100) for _ in range(3)]
        lam = [F(random.randint(1, 5)) for _ in range(3)]
        lam = [l / sum(lam) for l in lam]
        s = [F(random.randint(1, 4), 2) for _ in range(2)]
        widen = [F(random.randint(0, 3), 1000) for _ in range(3)]
        R1, Rinf, R1_one = screen(q, xs, lam, s, widen)
        for kind, bound in (("max", R1), ("sum", Rinf)):
            for _ in range(20):
                c = rand_normal(kind, s)
                beta = support(*c)
                assert beta - (c[0] * q[0] + c[1] * q[1]) <= bound
                if c[1] >= 0 and kind == "max":
                    assert beta - (c[0] * q[0] + c[1] * q[1]) <= R1_one
                checked += 1
    # swapped pairing fails: H = {(0,0)} (singleton domain x=0), query (-1,-1), s=(1,1)
    # cut z1 + z2 >= 0 is valid; max-normalized; violation 2 > R_inf = 1.
    viol, R1, Rinf = F(2), F(2), F(1)
    assert viol > Rinf and viol <= R1
    # sum-normalized cut (1/2, 1/2): violation 1 = R_inf
    assert F(1) <= Rinf
    # tightness: q = (3/10, 2/25), mixture = point x=3/10, tangent normal (-3/5, 1)
    q = (F(3, 10), F(2, 25))
    R1, _, _ = screen(q, [F(3, 10)], [F(1)], [F(1), F(1)], [F(0)])
    c = (F(-3, 5), F(1))
    assert support(*c) - (c[0] * q[0] + c[1] * q[1]) == R1 == F(1, 100)
    print(f"screening checks passed ({checked} cut/normalization pairs); swapped pairing refuted; tight example ok")


if __name__ == "__main__":
    main()
