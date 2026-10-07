"""Rerun of the review's validity check quoted in decomposition-certificates.md, Section 5.2
(reviews/decomposition-review-checks/indep_dp.py valid 5 0 3 6 and valid 6 1 2 5), with the two
closed leaf-cell intersection tests of indep_dp.certificate widened by TOL.

The review's file is not modified: its source is read, the two tests are replaced in memory
(each replacement is asserted to match exactly once), and the result is executed as a module.
TOL = 0 reproduces the original code.

  python3 review_valid_tol.py TOL     e.g. 0 or 1e-12
"""
import os
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "decomposition-review-checks", "indep_dp.py")

REPL = [
    ("(clo[None, :] <= u2[:, None]) & (chi[None, :] >= l2[:, None])",
     "(clo[None, :] <= u2[:, None] + TOL) & (chi[None, :] >= l2[:, None] - TOL)"),
    ("(plo[None, :] <= u1[:, None]) & (phi_[None, :] >= l1[:, None])",
     "(plo[None, :] <= u1[:, None] + TOL) & (phi_[None, :] >= l1[:, None] - TOL)"),
]


def load(tol):
    src = open(SRC).read()
    for old, new in REPL:
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    src = src.replace('if __name__ == "__main__":', "if False:")
    mod = types.ModuleType("indep_dp_tol")
    mod.TOL = tol
    exec(compile(src, SRC + " (patched)", "exec"), mod.__dict__)
    return mod


if __name__ == "__main__":
    tol = float(sys.argv[1])
    m = load(tol)
    print("# review code indep_dp.py, leaf-cell tests widened by TOL = %g" % tol)
    for n, seed, mu, j in [(5, 0, 3, 6), (6, 1, 2, 5)]:
        m.valid(n, seed, mu, j)
        import numpy as np
        c = np.random.default_rng(seed).uniform(-0.2, 0.2, n)
        xs = m.xstar_and_values(n, 0.8, c)[0]
        lam = np.zeros(n)
        for t in range(1, n - 1):
            lam[t] = m.dphi(xs[t]) + c[t] + 0.8 * xs[t + 1]
        _, size, pairs, _ = m.certificate(n, 0.8, c, xs, 2.0 ** -j, mu, lam)
        print("#   size %d, (leaf, cell) pairs of non-root bags %d" % (size, pairs), flush=True)
