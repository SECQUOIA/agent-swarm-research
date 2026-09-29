"""Toy spatial branch-and-bound on sphere- and ball-constrained problems.

Problem:  minimize f(y) = -sum_i c_i y_i^2 + sum_i e_i y_i^4  over  F = X0 ∩ {|y| = 1}  ("sphere")
          or F = X0 ∩ {|y| <= 1}  ("ball"),  X0 = [LO, HI]^n.
With e = 0: f* = -max_i c_i and the optimal set is the unit sphere of the
coordinates with c_i = max c, a manifold of dimension p = (multiplicity of max c) - 1.
Instance S2_quart (c = (1,1), e = (0,1)): f = -1 + y_2^4 on the circle, so the
optimal set is {(+-1, 0)} with quartic growth along the circle.

Node relaxation on a box B = [l, u] (objective-gap scheme, Section 2 of the note):
  objective   f_B(y) = f(y) - alpha q_B(y),  q_B(y) = sum_i (y_i - l_i)(u_i - y_i),
              alpha = 1.1 * max c  (convex, gap exactly alpha q_B);
  constraints |y|^2 <= 1 kept exactly (convex);
              for "sphere" also the secant relaxation of |y|^2 >= 1:
              sum_i ((l_i + u_i) y_i - l_i u_i) >= 1   (margin exactly q_B).
Lower bound: Lagrangian dual of the separable convex node problem,
  d(mu, nu) = sum_i min_{y_i in [l_i,u_i]} [(alpha - c_i + mu) y_i^2 - (alpha + nu)(l_i+u_i) y_i]
              + alpha sum_i l_i u_i - mu + nu (1 + sum_i l_i u_i),
maximized over mu, nu >= 0 by L-BFGS-B.  Any (mu, nu) >= 0 gives a valid bound,
so imperfect maximization can only add nodes.  Floating point, not certified.

Tree: binary widest-side bisection, incumbent fixed at f*, prune if bound >= f* - eps.
Usage: python3 sbb_sphere.py NAME [eps ...]   (NAME from INSTANCES below)
"""
import sys
import json
import math
import time
import numpy as np
from scipy.optimize import minimize

LO, HI = -1.2, 1.3

INSTANCES = {
    # name: (n, c, kind)
    "S2_iso": (2, [1.0, 0.5], "sphere"),        # circle, isolated minimizers, p = 0
    "S2_circ": (2, [1.0, 1.0], "sphere"),       # circle all optimal, p = 1
    "S3_iso": (3, [1.0, 0.5, 0.25], "sphere"),  # 2-sphere, isolated, p = 0
    "S3_circ": (3, [1.0, 1.0, 0.5], "sphere"),  # optimal great circle, p = 1
    "S3_all": (3, [1.0, 1.0, 1.0], "sphere"),   # whole 2-sphere optimal, p = 2
    "B2_circ": (2, [1.0, 1.0], "ball"),         # disk, optimal boundary circle, p = 1
    "B3_iso": (3, [1.0, 0.5, 0.25], "ball"),    # ball, isolated boundary minimizers, p = 0
    "B3_circ": (3, [1.0, 1.0, 0.5], "ball"),    # ball, optimal great circle on boundary, p = 1
    "B3_all": (3, [1.0, 1.0, 1.0], "ball"),     # ball, optimal boundary sphere, p = 2
    "S2_quart": (2, [1.0, 1.0], "sphere", [0.0, 1.0]),  # circle, quartic growth, eps^(-1/4)
}


class Relax:
    def __init__(self, n, c, kind, e=None):
        self.n = n
        self.c = np.array(c, float)
        self.e = np.zeros(n) if e is None else np.array(e, float)
        self.kind = kind
        self.alpha = 1.1 * self.c.max()
        self.fstar = -self.c.max()

    def dual(self, x, l, u):
        """Return (-d, -grad d) at x = (mu, nu)."""
        mu, nu = x[0], (x[1] if self.kind == "sphere" else 0.0)
        a = self.alpha
        A = a - self.c + mu
        b = l + u
        Bc = (a + nu) * b
        y = Bc / (2 * A)
        for i in np.nonzero(self.e)[0]:  # minimize e y^4 + A y^2 - B y: 4e y^3 + 2A y - B = 0
            p, q = 2 * A[i] / (4 * self.e[i]), -Bc[i] / (4 * self.e[i])
            r = math.sqrt(q * q / 4 + p ** 3 / 27)
            y[i] = np.cbrt(-q / 2 + r) + np.cbrt(-q / 2 - r)
        y = np.clip(y, l, u)
        val = np.sum(A * y * y - Bc * y + self.e * y ** 4) + a * np.sum(l * u) - mu
        g_mu = np.sum(y * y) - 1.0
        if self.kind == "sphere":
            rhs = 1.0 + np.sum(l * u)
            val += nu * rhs
            g_nu = rhs - np.sum(b * y)
            return -val, -np.array([g_mu, g_nu])
        return -val, -np.array([g_mu])

    def quick_infeasible(self, l, u):
        # B ∩ ball empty?
        dmin = np.where(l > 0, l, np.where(u < 0, u, 0.0))
        if np.sum(dmin * dmin) > 1.0 + 1e-12:
            return True
        if self.kind == "sphere":
            b = l + u
            if np.sum(np.maximum(b * l, b * u)) < 1.0 + np.sum(l * u) - 1e-12:
                return True
        return False

    def lower_bound(self, l, u, x0):
        if self.quick_infeasible(l, u):
            return math.inf, x0
        k = 2 if self.kind == "sphere" else 1
        x0 = np.asarray(x0[:k], float)
        r = minimize(self.dual, x0, args=(l, u), jac=True, method="L-BFGS-B",
                     bounds=[(0.0, 1e9)] * k,
                     options={"maxiter": 500, "ftol": 1e-15, "gtol": 1e-12})
        return -r.fun, r.x


def run(name, eps, max_nodes=3_000_000):
    n, c, kind = INSTANCES[name][:3]
    R = Relax(n, c, kind, *INSTANCES[name][3:])
    thr = R.fstar - eps
    stack = [(np.full(n, LO), np.full(n, HI), np.zeros(2))]
    nodes = 0
    while stack:
        l, u, x0 = stack.pop()
        nodes += 1
        if nodes > max_nodes:
            return None
        lb, x = R.lower_bound(l, u, x0)
        if lb >= thr:
            continue
        i = int(np.argmax(u - l))
        s = 0.5 * (l[i] + u[i])
        u1 = u.copy(); u1[i] = s
        l2 = l.copy(); l2[i] = s
        xs = np.zeros(2); xs[:len(x)] = x
        stack.append((l, u1, xs))
        stack.append((l2, u, xs))
    return nodes


def main():
    name = sys.argv[1]
    epss = [float(e) for e in sys.argv[2:]] or [10.0 ** (-k) for k in range(1, 6)]
    for eps in epss:
        t0 = time.time()
        nodes = run(name, eps)
        print(json.dumps({"inst": name, "alpha": 1.1 * max(INSTANCES[name][1]),
                          "eps": eps, "nodes": nodes,
                          "sec": round(time.time() - t0, 1)}), flush=True)


if __name__ == "__main__":
    main()
