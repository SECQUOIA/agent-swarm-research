"""Explore 3-variable gadgets f(x,y,z) = ux(x) + b x y + c y^2 + [uz(z) + coupling(y,z)] on [-1,1]^3.
Class-(a) symmetric fooling gap: exact = min_s K(s), relaxed = min_p vex k1(p) + vex k2(p) + c p,
where k_i(s) = h_i(sqrt s), h_i(y) = min over the end variable.
"""
import numpy as np, sys, itertools

S = np.linspace(0, 1, 4001)          # s = y^2 grid
Zg = np.linspace(-1, 1, 20001)

def h_bilinear_quad(a, b, y):        # min_x x^2/(2a) + b x y over [-1,1]
    x = np.clip(-a * b * y, -1, 1)
    return x * x / (2 * a) + b * x * y

def h_quartic(beta, bp, y):          # min_z z^2/2 - beta z^4 + bp y z over [-1,1]
    uz = Zg ** 2 / 2 - beta * Zg ** 4
    return np.array([np.min(uz + bp * yy * Zg) for yy in np.atleast_1d(y)])

def h_zy2(bp, y):                    # min_z z^2 - bp z y^2 over [-1,1]
    z = np.clip(bp * y * y / 2, -1, 1)
    return z * z - bp * z * y * y

def vex(vals):                       # lower convex envelope on grid S
    hull = []
    for i in range(len(S)):
        while len(hull) >= 2:
            i1, i2 = hull[-2], hull[-1]
            if (vals[i2] - vals[i1]) * (S[i] - S[i1]) >= (vals[i] - vals[i1]) * (S[i2] - S[i1]):
                hull.pop()
            else:
                break
        hull.append(i)
    return np.interp(S, S[hull], vals[hull])

def analyse(k1, k2, c):
    K = k1 + k2 + c * S
    exact = K.min(); argex = S[K.argmin()]
    R = vex(k1) + vex(k2) + c * S
    rel = R.min(); argrel = S[R.argmin()]
    pos = np.all(K[1:] > 0)
    return exact, argex, rel, argrel, pos, K

if __name__ == "__main__":
    y = np.sqrt(S)
    best = []
    # design Q: bilinear couplings, quartic uz
    for ab in [1.5, 2.0, 3.0]:
        for b in [0.5, 1.0, 1.5, 2.0]:
            a = ab / b
            k1 = h_bilinear_quad(a, b, y)
            for beta in [0.05, 0.08, 0.15, 0.25, 0.35, 0.45]:
                for bp in [0.3, 0.6, 1.0, 1.5]:
                    k2 = h_quartic(beta, bp, y)
                    # choose c: smallest c with K>0 on (0,1] (bisection), then add small margin
                    lo, hi = 0.0, 20.0
                    for _ in range(50):
                        mid = (lo + hi) / 2
                        K = k1 + k2 + mid * S
                        if np.all(K[1:] > 0) and (K[1] - K[0]) > 0: hi = mid
                        else: lo = mid
                    c = hi * 1.02 + 1e-3
                    exact, ae, rel, ar, pos, K = analyse(k1, k2, c)
                    gap = exact - rel
                    # Lipschitz sup |grad| on the box (x,y,z in [-1,1])
                    Lx = 1 / a + b
                    Ly = b + 2 * c + bp
                    Lz = max(abs(1 - 4 * beta), 1.0) + bp   # |z - 4 beta z^3| max over [-1,1] + bp
                    Lz = np.max(np.abs(Zg - 4 * beta * Zg ** 3)) + bp
                    Lam = 2 * max(Lx, Ly, Lz)
                    best.append((gap / Lam, gap, Lam, ab, b, beta, bp, c, ar))
    best.sort(reverse=True)
    print("design Q (bilinear, quartic uz): top")
    for r in best[:8]:
        print("gap/Lam=%.5f gap=%.5f Lam=%.3f ab=%.2f b=%.2f beta=%.2f bp=%.2f c=%.4f argrel=%.3f" % r)
    best = []
    for ab in [1.5, 2.0, 3.0, 4.0]:
        for b in [0.5, 1.0, 2.0, 3.0, 4.0]:
            a = ab / b
            k1 = h_bilinear_quad(a, b, y)
            for bp in [0.5, 1.0, 1.5, 2.0]:
                k2 = h_zy2(bp, y)
                lo, hi = 0.0, 40.0
                for _ in range(50):
                    mid = (lo + hi) / 2
                    K = k1 + k2 + mid * S
                    if np.all(K[1:] > 0) and (K[1] - K[0]) > 0: hi = mid
                    else: lo = mid
                c = hi * 1.02 + 1e-3
                exact, ae, rel, ar, pos, K = analyse(k1, k2, c)
                gap = exact - rel
                Lx = 1 / a + b; Ly = b + 2 * c + 2 * bp; Lz = 2 + bp
                Lam = 2 * max(Lx, Ly, Lz)
                best.append((gap / Lam, gap, Lam, ab, b, bp, c, ar))
    best.sort(reverse=True)
    print("design P (z y^2 coupling): top")
    for r in best[:8]:
        print("gap/Lam=%.5f gap=%.5f Lam=%.3f ab=%.2f b=%.2f bp=%.2f c=%.4f argrel=%.3f" % r)
