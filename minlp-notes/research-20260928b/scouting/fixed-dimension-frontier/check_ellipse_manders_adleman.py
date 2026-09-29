"""Scratch check: concave quadratic minimization over the integer points of one
ellipse in Z^2 decides Manders-Adleman quadratic congruences.

Instance (a,b,c), b not dividing a: is there x in [1,c-1] with x^2 = a mod b?
Put c'=c-1, u=ceil((a-c'^2)/b), Y=max(1,ceil((a/b-u)/2)), t=-Y-u, N=a+b t.
Ellipse E: X^2 + b y + y^2/(2Y^2) <= N + 1/2   (Hessian diag(2, 1/Y^2) > 0).
Objective f = N - X^2 - b y (Hessian diag(-2,0), concave).
Claim: f >= 0 on E cap Z^2, and min f = 0 iff the congruence instance is YES.
"""
from math import ceil, isqrt
from fractions import Fraction as F

def ma_truth(a, b, c):
    return any((x * x - a) % b == 0 for x in range(1, c))

def reduce(a, b, c):
    cp = c - 1
    u = -((-(a - cp * cp)) // b)          # ceil((a-cp^2)/b)
    Y = max(1, ceil(F(F(a, b) - u, 2)))
    t = -Y - u
    N = a + b * t
    return N, Y

def min_f(a, b, c):
    N, Y = reduce(a, b, c)
    # 2Y^2 X^2 + 2Y^2 b y + y^2 <= 2Y^2 N + Y^2 ; complete square in y
    # (y + bY^2)^2 <= 2Y^2 N + Y^2 + b^2 Y^4 - 2Y^2 X^2
    R = 2 * Y * Y * N + Y * Y + b * b * Y ** 4
    best = None
    Xmax = isqrt(max(R, 0) // (2 * Y * Y)) + 1
    for X in range(-Xmax, Xmax + 1):
        rhs = R - 2 * Y * Y * X * X
        if rhs < 0:
            continue
        s = isqrt(rhs)
        # feasible y: |y + bY^2| <= sqrt(rhs); f decreases in y, so take the largest feasible y
        y = -b * Y * Y + s
        while 2 * Y * Y * X * X + 2 * Y * Y * b * y + y * y > 2 * Y * Y * N + Y * Y:
            y -= 1
        assert 2 * Y * Y * X * X + 2 * Y * Y * b * (y + 1) + (y + 1) ** 2 > 2 * Y * Y * N + Y * Y
        f = N - X * X - b * y
        assert f >= 0, (a, b, c, X, y, f)
        if best is None or f < best:
            best = f
    return best

cnt = yes = 0
for b in range(2, 36):
    for a in range(1, b):
        for c in range(2, b + 3):
            truth = ma_truth(a, b, c)
            m = min_f(a, b, c)
            assert m is not None and ((m == 0) == truth), (a, b, c, m, truth)
            cnt += 1; yes += truth
print(f'checked {cnt} instances ({yes} YES): min f == 0 exactly on YES instances')
