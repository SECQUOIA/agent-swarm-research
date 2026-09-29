"""Corollary 1 on the rigid instance tight at tolerance eps - delta (exact).

H(z) = max(eps + z^2, s z + delta, (1+s) z - s + delta) on [0,1], alpha = 1,
so m = H - z^2 = max(eps, q_{[0,s]}(z) + delta, q_{[s,1]}(z) + delta):
  * H is convex, min m = eps,
  * {[0,s], [s,1]} is a certificate at tolerance eps - delta, so
    N_opt(eps - delta) = 2 and the note's Corollary 1 claims T <= 7.
H is replaced by its piecewise-linear interpolant on a dense knot set (the
interpolant lies above H, so m stays >= eps and the certificate stays valid;
min m = eps is kept at knots where eps + z^2 is active).
The worst tree over ALL delta-minimizer choices is computed exactly.

Usage: python3 cor1_rigid.py
"""
from fractions import Fraction as Fr

from exact1d import Inst
from thm1_check import worst_tree


def instance(s, eps, delta, n_geo=40, n_uni=40):
    def H(z):
        return max(eps + z * z, s * z + delta, (1 + s) * z - s + delta)
    pts = {Fr(0), Fr(1), s}
    for i in range(1, n_uni):
        pts.add(Fr(i, n_uni))
    r = Fr(1, 2)
    for _ in range(n_geo):
        for c in (s, Fr(0), Fr(1)):
            for z in (c - r, c + r):
                if 0 < z < 1:
                    pts.add(z)
        r = r * Fr(2, 3)
    xs = sorted(pts)
    return Inst(xs, [H(z) - z * z for z in xs])


def main():
    print("s, eps, delta/eps : N(eps-delta)  N(eps-2delta)  worst T over delta-minimizers  (Cor. 1 bound 8N-9)")
    for s in (Fr(1, 2), Fr(1, 3), Fr(1, 5)):
        for eps in (Fr(1, 10 ** 3), Fr(1, 10 ** 5)):
            for rho in (Fr(1, 2), Fr(9, 10), Fr(99, 100), Fr(999, 1000)):
                d = eps * rho
                I = instance(s, eps, d)
                assert I.eps == eps and I.convex()
                N1 = len(I.greedy(shift=d)) - 1
                N2 = len(I.greedy(shift=2 * d)) - 1 if 2 * d < eps else None
                T = 2 * worst_tree(I, delta=d, cap=10 ** 6) + 1
                flag = "VIOLATES Cor. 1" if T > 8 * N1 - 9 else ""
                print(f"s={s} eps={float(eps):.0e} delta/eps={float(rho)}: N1={N1} N2={N2} T={T} bound={8*N1-9} {flag}", flush=True)


if __name__ == "__main__":
    main()
