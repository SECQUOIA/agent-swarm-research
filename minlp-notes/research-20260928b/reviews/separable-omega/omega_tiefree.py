"""omega on a tie-free variant of Theorem C's instances (review check).

N as in the note (root minimizer 1/2, w = 1/4).  R' has root minimizer y = 1/2 + delta
(w = 1/4 - delta^2 < 1/4), the same root value -c, and lines y t + phi, (1+y) t - y + phi, so that
cutting R' at y gives two valid children.  Every labelling has R' in some coordinate; omega
strictly prefers every uncut N coordinate, so it cuts all n-1 of them first.
Checks exactly: root minimizers and values, N_opt = 2 (the R'-cut is valid), and omega's node
count on every labelling (expected 2^(n+1) - 1), for n = 2..5.
"""
from fractions import Fraction as Fr
from sepcore import PL, run
from thmC_check import lines, EPS

H2 = Fr(1, 2)


def rprime(n, r0, delta):
    c = Fr(1, 4) - r0
    phi = (n - 1) * c - EPS / 2
    y = H2 + delta
    h = y - c                      # H(y) - y = -c
    s = EPS / (4 * (n - 1))
    L = [(1 - s, h - (1 - s) * y), (1 + s, h - (1 + s) * y), (y, phi), (1 + y, -y + phi)]
    return PL.from_lines(L), y


if __name__ == "__main__":
    for n in range(2, 6):
        r0 = Fr(1, 4) - Fr(1, 5 * n)
        _, LN, _ = lines(n, EPS, r0)
        N = PL.from_lines(LN)
        R, y = rprime(n, r0, Fr(1, 50))
        FR, yR, wR = R.node(Fr(0), Fr(1))
        FN, yN, wN = N.node(Fr(0), Fr(1))
        assert yR == y and yN == H2 and FR == FN and wR < wN, (yR, FR, FN, wR, wN)
        mR, mN = min(R.m(t) for t in R.x), min(N.m(t) for t in N.x)
        assert R.convex() and N.convex()
        shift = mR + (n - 1) * mN          # f* shift: validity is sum F + eps >= shift
        cut = [R.node(Fr(0), y)[0] + (n - 1) * FN + EPS - shift, R.node(y, Fr(1))[0] + (n - 1) * FN + EPS - shift]
        root = FR + (n - 1) * FN + EPS - shift
        counts = []
        for i in range(n):
            cs = [N] * n
            cs[i] = R
            counts.append(run(cs, EPS - shift, "omega")["nodes"])
        print(f"n={n}: min m_R' + (n-1) min m_N = {shift}; root value+eps = {root} (<0); R'-cut margins {cut} (>=0, N_opt = 2); "
              f"w_R' = {wR} < w_N = {wN}; omega nodes on each labelling {counts}; 2^(n+1)-1 = {2 ** (n + 1) - 1}")
        assert root < 0 and min(cut) >= 0 and all(t == 2 ** (n + 1) - 1 for t in counts)
    print("all assertions passed")
