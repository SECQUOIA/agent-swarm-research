"""Exact checks for the diagonal (box-Lagrangian) certificate.

F(x) = 1/2 x^T H x + b^T x + c on a continuous box [l,u].  For a box KKT point s,
lambda_i(s) = 2 dF_i(s)/(u_i-l_i) at a lower bound, -2 dF_i(s)/(u_i-l_i) at an
upper bound, 0 in the interior.  Checks:
  * the identity F(x)-F(s) = 1/2 (x-s)^T (H+Lam)(x-s) + 1/2 sum lam_i (x_i-l_i)(u_i-x_i);
  * invariance lambda(t) = lambda(s) at other optimizers t (constructed by kernel moves);
  * the full-set description against brute force on rational test grids;
  * rejection of the nonglobal KKT point of the invalid-growth trap;
  * the subset-sum instance (bag size 3) lies in the class, and its optimizers are
    exactly the subset-sum solutions.
Run: python3 -B check_diagonal.py
"""
import random
from fractions import Fraction as Fr
from itertools import product

random.seed(7)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fr(0))


def mv(A, x):
    return [dot(row, x) for row in A]


def psd(a):
    a = [row[:] for row in a]
    while a:
        if any(a[i][i] < 0 for i in range(len(a))):
            return False
        piv = next((i for i in range(len(a)) if a[i][i] > 0), None)
        if piv is None:
            return all(v == 0 for row in a for v in row)
        others = [i for i in range(len(a)) if i != piv]
        a = [[a[i][j] - a[i][piv] * a[piv][j] / a[piv][piv] for j in others] for i in others]
    return True


def Fval(H, b, c, x):
    return dot(x, mv(H, x)) / 2 + dot(b, x) + c


def grad(H, b, x):
    return [u + v for u, v in zip(mv(H, x), b)]


def multipliers(H, b, box, s):
    """Return lambda(s) if s is a box KKT point, else None."""
    g = grad(H, b, s)
    lam = []
    for (lo, hi), si, gi in zip(box, s, g):
        if si == lo and gi >= 0:
            lam.append(2 * gi / (hi - lo))
        elif si == hi and gi <= 0:
            lam.append(-2 * gi / (hi - lo))
        elif lo < si < hi and gi == 0:
            lam.append(Fr(0))
        elif lo < si < hi:
            return None
        else:
            return None
    return lam


def certificate(H, b, box, s):
    lam = multipliers(H, b, box, s)
    if lam is None:
        return None
    n = len(s)
    M = [[H[i][j] + (lam[i] if i == j else 0) for j in range(n)] for i in range(n)]
    return (lam, M) if psd(M) else None


def in_set(H, b, box, s, lam, M, x):
    n = len(x)
    if any(not (lo <= xi <= hi) for (lo, hi), xi in zip(box, x)):
        return False
    d = [xi - si for xi, si in zip(x, s)]
    if any(v != 0 for v in mv(M, d)):
        return False
    return all(lam[i] * (x[i] - box[i][0]) * (box[i][1] - x[i]) == 0 for i in range(n))


def random_class_instance(n):
    box = []
    for _ in range(n):
        lo = Fr(random.randint(-2, 1), random.choice([1, 2]))
        box.append((lo, lo + Fr(random.randint(1, 3), random.choice([1, 2]))))
    # kernel move k between endpoints on some coordinates
    s = []
    k = []
    status = []
    for (lo, hi) in box:
        st = random.choice(["l", "u", "i"])
        status.append(st)
        if st == "l":
            s.append(lo)
            k.append(random.choice([Fr(0), hi - lo]))
        elif st == "u":
            s.append(hi)
            k.append(random.choice([Fr(0), lo - hi]))
        else:
            s.append(lo + (hi - lo) * Fr(random.randint(1, 3), 4))
            k.append(Fr(random.randint(-1, 1), 8))
    # PSD M with k in kernel: sum of rank one a a^T, a orthogonal to k
    M = [[Fr(0)] * n for _ in range(n)]
    kk = dot(k, k)
    for _ in range(random.randint(1, n)):
        a = [Fr(random.randint(-2, 2)) for _ in range(n)]
        if kk:
            a = [ai - dot(a, k) / kk * ki for ai, ki in zip(a, k)]
        for i in range(n):
            for j in range(n):
                M[i][j] += a[i] * a[j]
    lam = []
    for st, (lo, hi) in zip(status, box):
        lam.append(Fr(random.randint(0, 3)) if st != "i" else Fr(0))
    H = [[M[i][j] - (lam[i] if i == j else 0) for j in range(n)] for i in range(n)]
    gs = []
    for st, (lo, hi), li in zip(status, box, lam):
        gs.append(li * (hi - lo) / 2 if st == "l" else (-li * (hi - lo) / 2 if st == "u" else Fr(0)))
    Hs = mv(H, s)
    b = [g - h for g, h in zip(gs, Hs)]
    c = Fr(random.randint(-3, 3))
    t = [si + ki for si, ki in zip(s, k)]
    return H, b, c, box, s, lam, t


def main():
    nid = ninv = nset = 0
    for trial in range(200):
        n = random.choice([2, 3, 4])
        H, b, c, box, s, lam0, t = random_class_instance(n)
        cert = certificate(H, b, box, s)
        assert cert is not None
        lam, M = cert
        assert lam == lam0
        for _ in range(20):
            x = [lo + (hi - lo) * Fr(random.randint(-4, 16), 12) for lo, hi in box]  # also outside box
            d = [xi - si for xi, si in zip(x, s)]
            rhs = dot(d, mv(M, d)) / 2 + sum(lam[i] * (x[i] - box[i][0]) * (box[i][1] - x[i]) for i in range(n)) / 2
            assert Fval(H, b, c, x) - Fval(H, b, c, s) == rhs
            nid += 1
        # second optimizer by kernel move (if it lies in the box)
        if all(lo <= ti <= hi for (lo, hi), ti in zip(box, t)) and t != s:
            assert Fval(H, b, c, t) == Fval(H, b, c, s)
            cert_t = certificate(H, b, box, t)
            assert cert_t is not None and cert_t[0] == lam
            ninv += 1
        # full set vs brute force on a rational grid
        fs = Fval(H, b, c, s)
        steps = 8 if n <= 3 else 4
        grids = [[lo + (hi - lo) * Fr(j, steps) for j in range(steps + 1)] for lo, hi in box]
        for x in product(*grids):
            x = list(x)
            v = Fval(H, b, c, x)
            assert v >= fs
            assert (v == fs) == in_set(H, b, box, s, lam, M, x)
            nset += 1
    # trap: nonglobal KKT (0,0) rejected, global (1,1) accepted
    H = [[Fr(2), Fr(-3)], [Fr(-3), Fr(2)]]
    b = [Fr(63, 128)] * 2
    box = [(Fr(0), Fr(1))] * 2
    assert multipliers(H, b, box, [Fr(0), Fr(0)]) is not None
    assert certificate(H, b, box, [Fr(0), Fr(0)]) is None
    assert certificate(H, b, box, [Fr(1), Fr(1)]) is not None
    # two tilted segments example: F = (x-y+t/2)^2 + t(1-t)/8 on [0,1]^3
    v = [Fr(1), Fr(-1), Fr(1, 2)]
    H = [[2 * a * bb for bb in v] for a in v]
    H[2][2] -= Fr(1, 4)
    b = [Fr(0), Fr(0), Fr(1, 8)]
    box = [(Fr(0), Fr(1))] * 3
    for s in ([Fr(0), Fr(0), Fr(0)], [Fr(1, 3), Fr(1, 3), Fr(0)], [Fr(0), Fr(1, 2), Fr(1)], [Fr(1, 2), Fr(1), Fr(1)]):
        cert = certificate(H, b, box, s)
        assert cert is not None and cert[0] == [0, 0, Fr(1, 4)]
    # x + y - 2xy on [0,1]^2: endpoint class but also check diagonal class rejects/accepts
    # subset-sum instance in the class: variables x_1..x_m in [0,1], sigma_1..sigma_m in [0,A]
    a = [3, -5, 2, 4, -4]  # zero-sum target 0 with signed integers (T = 0)
    m = len(a)
    A = sum(abs(ai) for ai in a)
    # order: x_1..x_m, sigma_1..sigma_m ; F = sum (sigma_i - sigma_{i-1} - a_i x_i)^2 + sigma_m^2 + sum x_i(1-x_i)
    nvar = 2 * m
    H = [[Fr(0)] * nvar for _ in range(nvar)]
    bvec = [Fr(0)] * nvar
    rows = []
    for i in range(m):
        row = [Fr(0)] * nvar
        row[m + i] = Fr(1)
        if i > 0:
            row[m + i - 1] = Fr(-1)
        row[i] = Fr(-a[i])
        rows.append(row)
    last = [Fr(0)] * nvar
    last[2 * m - 1] = Fr(1)
    rows.append(last)
    for row in rows:
        for p in range(nvar):
            for q in range(nvar):
                H[p][q] += 2 * row[p] * row[q]
    for i in range(m):
        H[i][i] -= 2
        bvec[i] += 1
    box = [(Fr(0), Fr(1))] * m + [(Fr(-A), Fr(A))] * m
    # bag structure: each square couples sigma_{i-1}, sigma_i, x_i -> bags of size 3
    for p in range(nvar):
        for q in range(nvar):
            if H[p][q] != 0 and p != q:
                # allowed pairs: (x_i, sigma_i), (x_i, sigma_{i-1}), (sigma_i, sigma_{i-1})
                P, Qq = sorted((p, q))
                ok = (P < m and Qq >= m and (Qq - m == P or Qq - m == P - 1)) or (P >= m and Qq == P + 1)
                assert ok, (p, q)
    sols = []
    for xs in product([0, 1], repeat=m):
        sig = []
        acc = 0
        for i in range(m):
            acc += a[i] * xs[i]
            sig.append(Fr(acc))
        pt = [Fr(v) for v in xs] + sig
        val = Fval(H, bvec, Fr(0), pt)
        assert val >= 0
        if acc == 0:
            assert val == 0
            cert = certificate(H, bvec, box, pt)
            assert cert is not None, xs
            assert cert[0][:m] == [2] * m and all(v == 0 for v in cert[0][m:])
            sols.append(xs)
        else:
            assert val > 0
    print(f"diagonal checks passed: {nid} identities, {ninv} invariance moves, {nset} full-set grid points; "
          f"trap rejected; subset-sum instance has {len(sols)} certified optimal vertices (incl. zero)")


if __name__ == "__main__":
    main()
