"""Exact identities for Section 3's corrected nearby-point counterexample.

This checks the displayed algebra, not every quantifier in the proof or any
numerical branch-and-bound run. Requires SymPy; checked with version 1.14.0.
"""

import sympy as sp


def main():
    b, w = sp.symbols("b w", positive=True)
    t, s, q = sp.symbols("t s q", real=True)
    x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
    g = x3 + x1**2 - x2**2 + x1 * x2
    f = -x3 + 2 * x1**2 + 2 * x2**2
    shifted = {x1: b + t, x2: -2 * b + s, x3: 5 * b**2 + q}
    gs = sp.expand(g.subs(shifted))
    fs = sp.expand(f.subs(shifted))
    assert sp.expand(gs - (q + t**2 + s * (5 * b + t - s))) == 0

    # The old box included a distinct feasible point, disproving F(Z)={y_b}.
    assert sp.expand(gs.subs({t: 0, s: -w, q: 0})) == -5 * b * w - w**2

    alpha = sp.sqrt(5) / 2
    k = sp.sqrt(alpha / (1 + alpha))
    correction = alpha * (w**2 / 4 - t**2 + s * (w - s) + q * (w - q))
    witness = {t: -k * w / 2, s: 0, q: 0}
    assert sp.simplify((gs - correction).subs(witness)) == 0
    gap = 5 * b**2 - fs.subs(witness)
    assert sp.simplify(gap - (2 * b * k * w - k**2 * w**2 / 2)) == 0

    # alphaBB convexity: eigenvalues of Hessian(g) + 2 alpha I are
    # 0, sqrt(5), 2 sqrt(5). The critical-space Lagrangian Hessian
    # has eigenvalues 4 +/- sqrt(5), both positive.
    hcv = sp.hessian(g, (x1, x2, x3)) + 2 * alpha * sp.eye(3)
    assert hcv.eigenvals() == {0: 1, sp.sqrt(5): 1, 2 * sp.sqrt(5): 1}
    hlag = sp.hessian(f + g, (x1, x2, x3))[:2, :2]
    assert hlag.eigenvals() == {4 - sp.sqrt(5): 1, 4 + sp.sqrt(5): 1}
    print("Exact counterexample identities, convexity, and critical-space curvature passed.")


if __name__ == "__main__":
    main()
