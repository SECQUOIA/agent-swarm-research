"""Independent-parameter and C0 constitutive checks; not a certified optimizer."""
from fractions import Fraction as F

import numpy as np
from scipy.optimize import least_squares

from pbflow import Graph
from block_rank_checks import subdivided_core


def basis(x):
    return np.array([x, x * np.abs(x), x**3, np.maximum(x - 1, 0)]).T


def basis_derivative(x):
    return np.array([np.ones_like(x), 2*np.abs(x), 3*x*x, (x > 1).astype(float)]).T


def physical(G, b, theta):
    tree, chords = G.spanning_forest()
    x0 = G.tree_flow(b, tree)
    Z = np.array([G.cycle_vector(tree, e) for e in chords])
    def residual(c):
        return Z @ np.sum(theta*basis(x0+Z.T@c), axis=1)
    def jacobian(c):
        resistance = np.sum(theta*basis_derivative(x0+Z.T@c), axis=1)
        return (Z*resistance)@Z.T
    sol = least_squares(residual, np.zeros(len(chords)), jac=jacobian,
                        xtol=1e-13, ftol=1e-13, gtol=1e-13, max_nfev=200)
    x = x0+Z.T@sol.x
    drop = np.sum(theta*basis(x), axis=1)
    A = np.zeros((G.n, G.m))
    for e, (u, v, _) in enumerate(G.arcs):
        A[u, e], A[v, e] = 1, -1
    pi = np.zeros(G.n)
    pi[1:] = np.linalg.lstsq(A[1:].T, drop, rcond=None)[0]
    error = max(np.max(np.abs(A@x-b)), np.max(np.abs(A.T@pi-drop)))
    assert error < 1e-8, error
    return x, pi, A, error


def run():
    rng = np.random.default_rng(590527)
    derivative_error = physical_error = 0.
    exact_cycles = derivative_checks = 0
    crossed_hinge = False
    for trial in range(16):
        graph = subdivided_core('theta' if trial % 2 == 0 else 'k4', rng)
        arcs = list(graph.edges())
        G = Graph(len(graph), [(u, v, 1.) for u, v in arcs])
        # Exact rational physical states, with independently chosen nonlinear
        # coefficients and a recovered positive linear coefficient.
        potential = [100*int(v) for v in rng.permutation(G.n)]
        exact_drops = []
        for u, v in arcs:
            x = F(int(rng.integers(1, 5)), 2)
            if potential[u] < potential[v]:
                x = -x
            fs = [x, x*abs(x), x**3, max(x-1, 0)]
            theta = [F(1, 3), F(1, 5), F(1, 7)]
            a = (potential[u]-potential[v]-sum(c*f for c, f in zip(theta, fs[1:])))/x
            assert a > 0
            exact_drops.append(sum(c*f for c, f in zip([a]+theta, fs)))
        tree, chords = G.spanning_forest()
        for e in chords:
            z = list(map(int, G.cycle_vector(tree, e)))
            assert sum(c*f for c, f in zip(z, exact_drops)) == 0
            exact_cycles += 1
        # Positive linear part makes every coefficient-box law increasing,
        # including the genuinely C0 hinge at flow 1.
        theta = rng.uniform(.03, .4, (G.m, 4))
        theta[:, 0] += 1
        b = rng.uniform(-2.5, 2.5, G.n)
        b[-1] = -sum(b[:-1])
        x, pi, A, error = physical(G, b, theta)
        crossed_hinge |= bool(np.any(x > 1) and np.any(x < 1))
        physical_error = max(physical_error, error)
        R = np.sum(theta*basis_derivative(x), axis=1)
        q = np.zeros(G.n)
        q[0], q[1] = 1, -1
        L = (A/R)@A.T
        h = np.zeros(G.n)
        h[1:] = np.linalg.solve(L[1:, 1:], q[1:])
        jh = A.T@h/R
        assert np.max(np.abs(jh)) <= 1+1e-10
        for e, k in zip(rng.choice(G.m, 4, replace=False), range(4)):
            step = 1e-5
            plus, minus = theta.copy(), theta.copy()
            plus[e, k] += step
            minus[e, k] -= step
            pp = physical(G, b, plus)[1]
            pm = physical(G, b, minus)[1]
            fd = ((pp[0]-pp[1])-(pm[0]-pm[1]))/(2*step)
            error = abs(fd-jh[e]*basis(x)[e, k])
            derivative_error = max(derivative_error, error)
            assert error < 2e-6, (trial, e, k, error)
            derivative_checks += 1
    assert crossed_hinge
    print(f'{exact_cycles} exact affine-law cycle identities and {derivative_checks} independent coefficient derivatives passed.')
    print(f'Max derivative error {derivative_error:.3g}; physical residual {physical_error:.3g}.')


if __name__ == '__main__':
    run()
