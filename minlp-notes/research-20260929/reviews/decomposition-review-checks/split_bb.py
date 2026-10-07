"""Toy single-tree spatial B&B on the path family with per-factor alphaBB, for several factorizations
of the SAME objective F = sum (x_i^2 - kappa x_i^4 + c_i x_i) + b sum x_i x_{i+1} on [-1,1]^n.

Relaxations (all per-factor alphaBB; node relaxation F - sum_j A_j (x_j - l_j)(u_j - x_j), convex):
  note  unary terms exact, each bilinear factor b x_i x_{i+1} alone: alpha = |b|/2 on every box
        (the relaxation of Corollary 2.1 / Theorem 4.1(a));
  balS  balanced split f_i = s_i g_i + b x_i x_{i+1} + t_{i+1} g_{i+1} (g_1, g_n wholly in the end factors,
        interior g_i split 1/2:1/2), alpha computed on each box from the interval Hessian (exact for 2x2);
  balR  balanced split with the root-box alpha on every box (a constant-alpha rule).
Node bound: L-BFGS-B minimizer, then the Frank-Wolfe lower bound F_B(x) + min_box grad.(y - x) (valid
for convex F_B).  Incumbent fixed at f*; prune iff bound >= f* - eps; widest-side bisection at the midpoint.
Floating-point illustration, not a certified count.

Usage: python3 split_bb.py rel[+cvx] cmode eps n1 n2 ...   (cmode: zero | seedS  with c ~ U(-0.2, 0.2))
       "+cvx": split the widest side at -0.5 or 0.5 when the interval contains it, else at the midpoint.
"""
import math
import sys
import time
import numpy as np
from scipy import optimize

KAPPA, B = 0.1, 0.8


class Inst:
    def __init__(self, n, cmode):
        self.n = n
        self.c = np.zeros(n) if cmode == "zero" else np.random.default_rng(int(cmode[4:])).uniform(-0.2, 0.2, n)
        best = None
        rng = np.random.default_rng(7)
        for x0 in [np.zeros(n)] + [rng.uniform(-1, 1, n) for _ in range(20)]:
            r = optimize.minimize(self.F, x0, jac=self.G, method="L-BFGS-B", bounds=[(-1, 1)] * n,
                                  options={"ftol": 1e-16, "gtol": 1e-13})
            if best is None or r.fun < best.fun:
                best = r
        self.xs, self.fs = best.x, float(best.fun)

    def F(self, x):
        return float(np.sum(x * x - KAPPA * x ** 4 + self.c * x) + B * np.sum(x[:-1] * x[1:]))

    def G(self, x):
        g = 2 * x - 4 * KAPPA * x ** 3 + self.c
        g[:-1] += B * x[1:]; g[1:] += B * x[:-1]
        return g


def lmin2(p, q):
    return (p + q) / 2 - np.sqrt(((p - q) / 2) ** 2 + B * B)


def weights(I, rel, l, u):
    n = I.n
    if rel == "note":
        A = np.full(n, abs(B)); A[0] = A[-1] = abs(B) / 2
        return A
    sb = np.full(n, 0.5); ta = np.full(n, 0.5)
    sb[0], ta[0], sb[-1], ta[-1] = 1.0, 0.0, 0.0, 1.0
    if n == 2:
        sb[0], ta[1] = 1.0, 1.0
    if rel == "balR":
        l, u = -np.ones(n), np.ones(n)
    gmin = 2 - 12 * KAPPA * np.maximum(l * l, u * u)
    alf = np.maximum(0.0, -lmin2(sb[:-1] * gmin[:-1], ta[1:] * gmin[1:])) / 2
    A = np.zeros(n); A[:-1] += alf; A[1:] += alf
    return A


def bound(I, rel, l, u, thr):
    A = weights(I, rel, l, u)
    def Fg(x):
        v = I.F(x) - float(np.sum(A * (x - l) * (u - x)))
        g = I.G(x) - A * (l + u - 2 * x)
        return v, g
    def fw(x):
        v, g = Fg(x)
        return v + float(np.sum(np.minimum(g * (l - x), g * (u - x)))), v
    if not np.any(A > 0) and np.all(l <= I.xs) and np.all(I.xs <= u):
        return I.fs, I.fs                      # relaxation exact and x* in the box
    r = optimize.minimize(Fg, np.clip(I.xs, l, u), jac=True, method="L-BFGS-B", bounds=list(zip(l, u)),
                          options={"ftol": 1e-15, "gtol": 1e-12, "maxiter": 3000})
    lb, ub = fw(np.clip(r.x, l, u))
    if lb < thr <= ub:
        r = optimize.minimize(Fg, np.clip(r.x, l, u), jac=True, method="L-BFGS-B", bounds=list(zip(l, u)),
                              options={"ftol": 0.0, "gtol": 1e-15, "maxiter": 20000, "maxcor": 30})
        lb = max(lb, fw(np.clip(r.x, l, u))[0])
    return lb, ub


def run(I, rel, eps, node_limit=600_000, tlim=1500, rule="bisect"):
    stack = [(-np.ones(I.n), np.ones(I.n))]
    nodes = leaves = 0
    t0 = time.time()
    thr = I.fs - eps
    near = 0
    while stack:
        l, u = stack.pop()
        nodes += 1
        lb, _ = bound(I, rel, l, u, thr)
        if lb >= thr:
            leaves += 1
            if np.max(np.maximum(0, np.maximum(l - I.xs, I.xs - u))) < 0.05:
                near += 1
            continue
        if nodes >= node_limit or time.time() - t0 > tlim:
            return nodes, leaves, near, "limit", time.time() - t0
        i = int(np.argmax(u - l)); p = 0.5 * (l[i] + u[i])
        if rule == "cvx":                      # split at +-0.5 (inside the convexity cube of balS) when possible
            for q in (-0.5, 0.5):
                if l[i] < q < u[i]:
                    p = q
                    break
        u1 = u.copy(); u1[i] = p; l2 = l.copy(); l2[i] = p
        stack.append((l2, u)); stack.append((l, u1))
    return nodes, leaves, near, "done", time.time() - t0


def main():
    rel, cmode, eps = sys.argv[1], sys.argv[2], float(sys.argv[3])
    rule = "bisect"
    if rel.endswith("+cvx"):
        rel, rule = rel[:-4], "cvx"
    for n in map(int, sys.argv[4:]):
        I = Inst(n, cmode)
        nodes, leaves, near, st, dt = run(I, rel, eps, rule=rule)
        print("%s/%s %s eps=%.0e n=%d: leaves=%d (within 0.05 of x*: %d) nodes=%d %s %.1fs |x*|inf=%.3f" % (
            rel, rule, cmode, eps, n, leaves, near, nodes, st, dt, np.abs(I.xs).max()), flush=True)


if __name__ == "__main__":
    main()
