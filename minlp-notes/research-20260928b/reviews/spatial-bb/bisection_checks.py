"""Reviewer checks of Theorems A and C and of the (QD) remarks (independent code).

1. 1D exact alphaBB: dyadic bisection tree size T (incumbent f*), exact N_opt
   (greedy), J_eps, Theorem A bound, ratio T/(J N_opt); grid estimate of the
   (QD) constant K and Theorem C bound.
2. 2D separable exact alphaBB: 4-ary dyadic refinement with exact node bounds,
   grid estimate of K (sup-norm), Theorem B and Theorem C bounds.
3. (QD) sufficient-condition counterexamples.
4. Sharp 1D minimum at a point with very sparse binary digits: bisection level
   count computed in exact rational arithmetic.
"""
import math
from fractions import Fraction
import numpy as np
from numpy.polynomial import Polynomial as Poly
import mpmath as mp
from scipy import integrate

import thm_b_1d as T

A = 1.0 / 3.0


# ---------------------------------------------------------------- 1D
def lb_box(F, alpha, l, u):
    extra = Poly([alpha * l * u, -alpha * (l + u), alpha])   # -alpha (y-l)(u-y)
    return F.min_on(l, u, extra)


def bisect_1d(F, fstar, alpha, eps):
    stack, nodes = [(0.0, 1.0)], 0
    while stack:
        l, u = stack.pop()
        nodes += 1
        if lb_box(F, alpha, l, u) >= fstar - eps:
            continue
        m = 0.5 * (l + u)
        stack += [(l, m), (m, u)]
    return nodes


def qd_constant_1d(F, fstar, grid):
    y = np.linspace(0, 1, grid)
    m = np.array([F(t) for t in y]) - fstar
    m = np.maximum(m, 0.0)
    K = 0.0
    for i in range(grid):
        d2 = (y - y[i]) ** 2
        den = m + d2
        mask = den > 0
        K = max(K, np.max(m[i] / den[mask]))
    return K


def one_d():
    left = Poly([2 * A, -2]) - Poly([-A, 1]) ** 2
    right = Poly([-2 * A, 2]) - Poly([-A, 1]) ** 2
    inst = []
    F, p = T.poly_instance([0, 0, 1, 0, -2], A)
    inst.append(("nondeg t^2-2t^4", F, -(2 - 24 * (2 / 3) ** 2) / 2))
    F, p = T.poly_instance([0, 0, 0, 0, 1, 0, -1], A)
    inst.append(("quartic t^4(1-t^2)", F, T.alpha_for(p)))
    inst.append(("sharp 2|t|-t^2", T.PWPoly([(0.0, A, left), (A, 1.0, right)]), 1.0))
    for name, F, alpha in inst:
        fstar, arg = T.fmin(F)
        Ks = [qd_constant_1d(F, fstar, g) for g in (401, 1601, 6401)]
        K = Ks[-1]
        n, ap = 1, alpha
        Lam = K * (ap * n / 4 + 1) + ap * n / 4
        print(f"== {name}: alpha=alpha'={alpha:.4g}; grid K estimates {['%.3g' % k for k in Ks]}")
        for eps in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
            Tn = bisect_1d(F, fstar, alpha, eps)
            nopt = T.opt_cover(F, fstar, alpha, eps)
            J = max(0, math.ceil(math.log2(math.sqrt(ap * n / (4 * eps)))))
            thmA = 1 + 4 ** n * (math.sqrt(n) + 4) ** n * J * nopt
            I = T.bound(F, fstar, alpha, eps, [arg]) / (math.sqrt(alpha) / math.pi)   # raw integral
            thmC = 1 + 2 ** (n + 1) * Lam ** (n / 2) * I
            print(f"  eps={eps:.0e} T_bis={Tn:4d} N_opt={nopt:4d} J={J:2d} T/(J*N_opt)={Tn/(J*nopt):.3f} "
                  f"ThmA={thmA:.0f} ThmC={thmC:.1f} T/integral={Tn/I:.3f}")


# ---------------------------------------------------------------- 2D separable
def sep_instance(kind):
    c = np.array([1 / 3, math.sqrt(2) - 1])
    if kind == "nondeg":
        hs = [T.poly_instance([0, 0, 1, 0, -2], ci)[1] for ci in c]
    elif kind == "mixed":
        hs = [T.poly_instance([0, 0, 1], c[0])[1], T.poly_instance([0, 0, 0, 0, 1, 0, -2.5], c[1])[1]]
    else:
        raise ValueError
    alpha = max(T.alpha_for(h) for h in hs)
    return [T.PWPoly([(0.0, 1.0, h)]) for h in hs], alpha, c


def bisect_2d(Fs, fstars, alpha, eps):
    fstar = sum(fstars)
    stack, nodes, leaves = [((0.0, 1.0), (0.0, 1.0))], 0, 0
    while stack:
        box = stack.pop()
        nodes += 1
        lb = sum(lb_box(F, alpha, l, u) for F, (l, u) in zip(Fs, box))
        if lb >= fstar - eps:
            leaves += 1
            continue
        (l1, u1), (l2, u2) = box
        m1, m2 = 0.5 * (l1 + u1), 0.5 * (l2 + u2)
        for b1 in ((l1, m1), (m1, u1)):
            for b2 in ((l2, m2), (m2, u2)):
                stack.append((b1, b2))
    return nodes, leaves


def qd_constant_2d(Fs, fstars, G=81):
    y = np.linspace(0, 1, G)
    m1 = np.array([Fs[0](t) for t in y]) - fstars[0]
    m2 = np.array([Fs[1](t) for t in y]) - fstars[1]
    M = np.maximum(m1[:, None] + m2[None, :], 0).ravel()
    Y1, Y2 = np.meshgrid(y, y, indexing="ij")
    P = np.stack([Y1.ravel(), Y2.ravel()], 1)
    K = 0.0
    for i in range(len(P)):
        d = np.max(np.abs(P - P[i]), axis=1) ** 2
        den = M + d
        mask = den > 0
        K = max(K, np.max(M[i] / den[mask]))
    return K


def two_d():
    for kind in ("nondeg", "mixed"):
        Fs, alpha, c = sep_instance(kind)
        fstars = [T.fmin(F)[0] for F in Fs]
        K = qd_constant_2d(Fs, fstars)
        n = 2
        Lam = K * (alpha * n / 4 + 1) + alpha * n / 4
        print(f"== 2D separable {kind}: alpha=alpha'={alpha:.4g}, grid K={K:.3g}")
        for eps in (1e-2, 1e-4, 1e-6):
            nodes, leaves = bisect_2d(Fs, fstars, alpha, eps)
            g = lambda y2, y1: 1.0 / (Fs[0](y1) - fstars[0] + Fs[1](y2) - fstars[1] + eps)
            I, _ = integrate.nquad(g, [[0, 1], [0, 1]],
                                   opts=[{"points": [c[1]], "limit": 200}, {"points": [c[0]], "limit": 200}])
            thmB = (alpha * n / math.pi ** 2) ** (n / 2) * I
            thmC = 1 + 2 ** (n + 1) * Lam ** (n / 2) * I
            print(f"  eps={eps:.0e} nodes={nodes:5d} leaves={leaves:5d} ThmB={thmB:8.2f} leaves/ThmB={leaves/thmB:.2f} "
                  f"ThmC={thmC:10.1f} nodes/integral={nodes/I:.3f}")


# ---------------------------------------------------------------- (QD) counterexamples
def qd_counterexamples():
    print("== (QD) sufficient condition")
    for n in (2, 5, 10, 50):
        # m = |x|^2/2 on [-1,1]^n, gradient 1-Lipschitz (Euclidean); x=(t,..,t), y=0
        print(f"  m=|x|^2/2, n={n}: M=1, claimed K=max(2,M)=2, needed K >= n/2 = {n/2}")
    print("  1D m(t)=4(t-1/2)^2 (t+rho)(1+rho-t) on [0,1]; m>=0 on [-rho,1+rho]")
    for rho in (1e-1, 1e-2, 1e-3, 1e-4):
        p = Poly([-0.5, 1.0]) ** 2 * Poly([rho, 1.0]) * Poly([1 + rho, -1.0]) * 4
        d2 = p.deriv(2)
        tt = np.linspace(-rho, 1 + rho, 20001)
        M = np.max(np.abs(d2(tt)))
        # (QD) constant with y = 0 and x in (0, 0.5]
        x = np.concatenate([np.geomspace(1e-7, 0.5, 20000)])
        K0 = np.max(p(x) / (p(0.0) + x ** 2))
        g0, m0 = p.deriv()(0.0), p(0.0)
        print(f"   rho={rho:.0e}: M={M:.2f}, m(0)={m0:.2e}, m'(0)^2={g0**2:.3f} vs 2 M m(0)={2*M*m0:.2e}; "
              f"K >= {K0:.1f} (claimed max(2,M)={max(2,M):.2f})")


# ---------------------------------------------------------------- sparse-digit sharp minimum
def sparse_digit_levels():
    print("== sharp 1D f=2|y-z|-(y-z)^2, exact alphaBB alpha=1: node LB of the dyadic cell [l,u] containing z is -(z-l)(u-z)")
    P = [2, 4, 16, 256, 65536]
    z_sparse = sum(Fraction(1, 2 ** p) for p in P)
    z_third = Fraction(1, 3)
    for Lexp in (16, 60, 100, 200, 256, 257, 300, 400, 511, 600, 1000):
        eps = Fraction(1, 2 ** Lexp)
        out = []
        for z in (z_third, z_sparse):
            cnt, j = 0, 0
            while j < 4000:
                s = Fraction(1, 2 ** j)
                l = Fraction(math.floor(z * 2 ** j), 2 ** j)
                if (z - l) * (l + s - z) > eps:
                    cnt += 1
                else:
                    break    # bounds are monotone along the path, so deeper cells are never generated
                j += 1
            out.append(cnt)
        print(f"  eps=2^-{Lexp:<5d} non-pruned levels: z=1/3 -> {out[0]:4d} (nodes {1+2*out[0]}),  "
              f"z=sum 2^-2^2^k -> {out[1]:4d} (nodes {1+2*out[1]})")


if __name__ == "__main__":
    one_d()
    two_d()
    qd_counterexamples()
    sparse_digit_levels()
