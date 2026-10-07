"""M2: cross-check Report B's quadratic_polytope.support_quadratic and Report A's
quadratic_polygon.support_quadratic against the independent flint enumeration in
M2_polytope_checks.py (imported read-only; bytecode writing disabled).

Run: code/minlp_solver_lab/.venv/bin/python -B \
        paper-certified-support-cuts/verification/M2_crosscheck_impl.py
"""

import importlib.util
import os
import random
import sys
from fractions import Fraction as Fr

sys.dont_write_bytecode = True
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


polytope = load("rb_polytope", os.path.join(ROOT, "research-20261003-convexification/theory/quadratic_polytope.py"))
polygon = load("ra_polygon", os.path.join(ROOT, "research-20261002-convexification/theory/quadratic_polygon.py"))

# reuse the independent enumeration without re-running its checks
src = open(os.path.join(os.path.dirname(__file__), "M2_polytope_checks.py")).read()
src = src.split("# ---------------------------------------------------------------- random cross-checks")[0]
ns = {}
exec(compile(src, "M2_polytope_checks_head", "exec"), ns)
enumerate_support, box_rows = ns["enumerate_support"], ns["box_rows"]

random.seed(11)
mismatch = 0
total = 0
for _ in range(120):
    d = random.choice([1, 2, 2, 3])
    lo = [Fr(random.randint(-3, 0), random.randint(1, 2)) for _ in range(d)]
    hi = [Fr(random.randint(0, 3), random.randint(1, 2)) for _ in range(d)]
    extra = [tuple(random.randint(-3, 3) for _ in range(d)) + (Fr(random.randint(-2, 3), random.randint(1, 3)),)
             for _ in range(random.randint(0, 3))]
    if random.random() < 0.2 and extra:
        extra.append(tuple(-v for v in extra[-1]))        # equality pair
    pairs = [(i, j) for i in range(d) for j in range(i, d)]
    mono = [random.randint(-3, 3) for _ in pairs]
    lin = [Fr(random.randint(-4, 4), random.randint(1, 2)) for _ in range(d)]
    c0 = Fr(random.randint(-2, 2))
    H = [[0] * d for _ in range(d)]
    for v, (i, j) in zip(mono, pairs):
        if i == j:
            H[i][i] = 2 * v
        else:
            H[i][j] = H[j][i] = v
    rows = [(tuple(r[:-1]), Fr(r[-1])) for r in extra] + box_rows(lo, hi)
    mine = enumerate_support(H, lin, c0, rows)[0]
    rb = polytope.support_quadratic(list(zip(lo, hi)), extra, [c0] + lin + mono)
    rb_val = None if rb["status"] == "empty" else Fr(rb["bound"])
    total += 1
    if (mine is None) != (rb_val is None) or (mine is not None and mine[0] != rb_val):
        mismatch += 1
    if d == 2:
        ra = polygon.support_quadratic(list(zip(lo, hi)), [tuple(r) for r in extra],
                                       [c0, lin[0], lin[1], mono[0], mono[1], mono[2]])
        ra_val = None if ra["status"] == "empty" else Fr(ra["bound"])
        total += 1
        if (mine is None) != (ra_val is None) or (mine is not None and mine[0] != ra_val):
            mismatch += 1
print(f"implementation cross-checks: {total - mismatch}/{total} agree")
raise SystemExit(0 if mismatch == 0 else 1)
