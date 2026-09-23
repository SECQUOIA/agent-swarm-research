#!/usr/bin/env python3
"""Independent numerical checks for primal--dual and formulation results.

This is a diagnostic, not a proof certificate. Uses only NumPy
and the standard library already present in the qipm environment.
"""
from fractions import Fraction
from math import isqrt, log, sqrt

import numpy as np
from numpy.testing import assert_allclose

rng = np.random.default_rng(731904)


def check_projection():
    """Differentiate random feasible orthant central KKT systems."""
    for _ in range(80):
        n, m = 8, 3
        x = np.exp(rng.uniform(-2, 2, n))
        A = rng.normal(size=(m, n))
        eta = np.exp(rng.uniform(-1, 1))
        y = rng.normal(size=m)
        slack = 1 / (eta * x)
        cost = A.T @ y + slack
        # Solve the full differentiated saddle system, not the projector formula.
        Hess = np.diag(1 / x**2)
        KKT = np.block([[Hess, -eta * A.T], [A, np.zeros((m, m))]])
        sol = np.linalg.solve(KKT, np.r_[-eta * slack, np.zeros(m)])
        dx, dy = sol[:n], sol[n:]
        ds = -A.T @ dy
        primal = dx @ Hess @ dx
        dual = np.sum((ds / slack)**2)
        assert_allclose(primal + dual, n, rtol=2e-12)
        assert_allclose(dx @ ds, 0, atol=2e-12)
        assert_allclose(-eta * cost @ dx, primal, rtol=2e-11)
        assert_allclose(eta * (A @ x) @ dy, dual, rtol=2e-11)
        Hinv = np.diag(x**2)
        M = Hinv - Hinv @ A.T @ np.linalg.solve(A @ Hinv @ A.T, A @ Hinv)
        assert_allclose(eta**2 * cost @ M @ cost, primal, rtol=3e-10)
    print("80 random full KKT projection/progress checks passed")


def check_box():
    for rank in (4, 16, 64, 256):
        cumulative = Fraction(0)
        exponents = []
        for j in range(1, rank + 1):
            exponents.append((4 * rank * cumulative).__floor__())
            cumulative += Fraction(1, j * (isqrt(j - 1) + 1))
        a = np.array(exponents) * log(2)
        T = a[-1]
        for s in np.linspace(0, T, 17):
            z = s - a
            L = np.logaddexp(0, 2*z) / 2
            # Stable central primal logarithms: x=tanh(asinh(exp(z))/2).
            asinh_exp = np.logaddexp(z, L)
            logu = log(2) - np.logaddexp(0, -asinh_exp)
            logv = log(2) - np.logaddexp(0, asinh_exp)
            logalpha, logbeta = -s-logu, -s-logv
            x = np.tanh(asinh_exp / 2)
            # Derivatives from the complementarity quadratic.
            du_over_u = x * (1-x) / (1+x*x)
            dv_over_v = -x * (1+x) / (1+x*x)
            dalpha = -1-du_over_u
            dbeta = -1-dv_over_v
            activity = np.sum(-np.expm1(-L))
            assert_allclose(np.sum(du_over_u**2 + dv_over_v**2), activity, atol=2e-12)
            assert_allclose(np.sum(dalpha**2 + dbeta**2), 2*rank-activity, atol=2e-12)
            assert_allclose(logu+logalpha, -s, atol=1e-12)
            assert_allclose(logv+logbeta, -s, atol=1e-12)
            # beta-alpha=w in logarithms, using beta/alpha=u/v.
            # At tiny weights the difference cannot be formed accurately; use active coordinates.
            active = z > -15
            assert_allclose(np.exp(logbeta[active]) - np.exp(logalpha[active]),
                            np.exp(-a[active]), atol=1e-13, rtol=2e-9)
        initial_alpha = (1-np.exp(-a)+np.sqrt(1+np.exp(-2*a))) / 2
        assert np.min(initial_alpha) >= 1/sqrt(2)-1e-14
        log_primal_error = np.logaddexp.reduce(-a + logv)
        assert log_primal_error <= log(rank)-T+1e-12
        pd_lower = sqrt(rank)*max(0, T-log(rank)-log(2)/2)
        pd_length = sqrt(2*rank)*T
        assert pd_lower <= pd_length
        print(f"dyadic rank={rank}: product length={pd_length:.6g}, whole-gap lower={pd_lower:.6g}")


def check_minor_and_packing():
    for _ in range(80):
        n, q = 7, 3
        U = rng.normal(size=(n, n))
        X = U @ U.T + np.eye(n)
        # Arbitrary large inactive diagonal and dense cross fiber.
        scale = np.diag(np.r_[np.ones(q), np.exp(rng.uniform(0, 4, n-q))])
        X = scale @ X @ scale
        A = X[:q, :q]
        covector = np.zeros((n, n))
        covector[:q, :q] = np.linalg.inv(A)
        assert_allclose(np.trace(covector @ X @ covector @ X), q, atol=1e-11)
        W = rng.normal(size=(4, 3))
        Q = rng.normal(size=(3, 3))
        D = Q @ Q.T + np.eye(3)
        S = D + W.T @ W
        dW = rng.normal(size=W.shape)
        dS = rng.normal(size=S.shape)
        dS = (dS+dS.T)/2
        dD = dS-dW.T@W-W.T@dW
        Di = np.linalg.inv(D)
        expected = np.trace(Di@dD@Di@dD)+2*np.trace(Di@dW.T@dW)
        def deriv(t):
            Wt, St = W+t*dW, S+t*dS
            Dt = St-Wt.T@Wt
            dDt = dS-dW.T@Wt-Wt.T@dW
            return -np.trace(np.linalg.solve(Dt, dDt))
        eps = 1e-6
        numerical = (deriv(eps)-deriv(-eps))/(2*eps)
        assert_allclose(numerical, expected, rtol=2e-8, atol=2e-8)
        assert expected >= np.trace(Di@dD)**2/3-1e-11
    for d in range(2, 13):
        for h in range(1, 101):
            target = 2*(h//d)+min(h%d, 2)
            actual = min(2*q+max(0, h-d*q) for q in range(h+1))
            assert actual == target
    print("80 arbitrary-fiber minor/packing checks and 1100 integer envelope checks passed")


def tree_hessian(children, point):
    H = np.zeros((len(point), len(point)))
    gradient = np.zeros(len(point))
    for v, kids in children.items():
        gradq = np.zeros(len(point)); gradq[v] = 2*point[v]
        diagq = np.zeros(len(point)); diagq[v] = 2
        for child in kids:
            gradq[child] = -2*point[child]; diagq[child] = -2
        q = point[v]**2-sum(point[j]**2 for j in kids)
        assert q > 0 and point[v] > 0
        H += np.outer(gradq, gradq)/q**2-np.diag(diagq)/q
        gradient -= gradq/q
    return H, gradient


def check_trees():
    # Index0 is root; dictionary keys are all internal vertices.
    shapes = [({0: [1, 2]}, 3),
              ({0: [1, 2], 1: [3, 4]}, 5),
              ({0: [1, 2], 1: [3, 4], 2: [5, 6]}, 7),
              ({0: [1, 2, 3], 1: [4, 5], 2: [6, 7], 3: [8, 9]}, 10)]
    for children, size in shapes:
        internal = set(children)
        leaves = [i for i in range(size) if i not in internal]
        b = len(internal)
        c = rng.uniform(.2, 1, len(leaves)); c /= np.linalg.norm(c)
        leaf_weight = dict(zip(leaves, c*c))
        def counts(v):
            if v not in internal:
                return 0, leaf_weight[v]
            parts = [counts(j) for j in children[v]]
            return 1+sum(t[0] for t in parts), sum(t[1] for t in parts)
        stats = {v: counts(v) for v in internal}
        target_nu = 2*b-(2 if all(j in internal for j in children[0]) else 1)
        for tau in (.0, .1, 1., 10., 100.):
            D = np.hypot(b, tau); q = 2/(D+b); radial = tau/(D+b)
            point = np.zeros(size)
            for v, (number, mass) in stats.items():
                point[v] = sqrt(number*q+radial*radial*mass)
            point[leaves] = radial*c
            H, grad = tree_hessian(children, point)
            objective = np.zeros(size); objective[leaves] = c
            assert_allclose(grad[1:], tau*objective[1:], atol=3e-10)
            tangent = np.zeros(size)
            tangent[1:] = np.linalg.solve(H[1:, 1:], tau*objective[1:])
            assert_allclose(tangent@H@tangent, b*(1-b/D), atol=2e-10)
            parameter_at_point = grad[1:]@np.linalg.solve(H[1:, 1:], grad[1:])
            leverage = np.linalg.inv(H)[0, 0]/point[0]**2
            assert_allclose(parameter_at_point, 2*b-1/leverage, atol=2e-10)
            assert parameter_at_point <= target_nu+1e-10
        print(f"tree {children}: center, speed, and exact-parameter upper checks passed")
    for _ in range(100):
        arity = int(rng.integers(2, 8))
        mass = rng.dirichlet(np.ones(arity))*rng.uniform(.001, .999)
        r = mass.sum(); q = 1-r
        Z = np.sum(mass**2/(q+2*mass))
        S = (2*(1+r)-16*Z/(q+4*Z))/q**2
        assert S >= 2-1e-9
    print("100 root Schur-complement inequalities passed")


if __name__ == '__main__':
    check_projection()
    check_box()
    check_minor_and_packing()
    check_trees()
    print("All stage4 numerical diagnostics passed (not a proof certificate).")
