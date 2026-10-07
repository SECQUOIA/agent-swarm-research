"""lukvle10: an exactly feasible point defined by two rational seeds, with a rigorous enclosure of
every coordinate and of the objective (mpmath interval arithmetic, outward rounded).

Argument.
1. From the OSIL (exact constants) we assert that the 998 rows are equalities that can be solved
   one after another: row r is linear in its largest-index variable p(r) (exact nonzero
   coefficient, p(r) absent from the quadratic and nonlinear parts), the p(r) are distinct, and
   every other variable of row r has a smaller index. The variables that are no pivot are the
   seeds (here x1, x2 = x_0, x_1). All variables are continuous and free (checked generically
   below: the bounds are tested over the enclosure).
2. Fix the seeds at exact rationals (points/lukvle10_seed.txt). Then x_{p(r)} := (rhs - rest) / coef,
   in pivot order, defines a unique real point x* (rational, since the rows are polynomial with
   rational coefficients) that satisfies every row exactly.
3. The same recursion evaluated in outward-rounded interval arithmetic gives intervals X_k with
   x*_k in X_k (inclusion property). Evaluating the objective expression tree over the X_k
   encloses f(x*); real powers a^e with a > 0 are evaluated as exp(e log a).
Assumption: mpmath.iv rounds +, -, *, /, integer powers, exp and log outward (encloses the exact
result). The seeds are chosen from the high-precision KKT point of lukvle10_kkt.py, but the
argument does not depend on that computation.

Outputs: points/lukvle10_seed.txt (exact seeds, written once from the KKT file),
points/lukvle10_box.txt.gz (for each variable a 60-digit decimal centre and a radius such that
the closed box contains x*), logs/lukvle10_enclose.json.
"""
import gzip
import json
import os
import sys
import time
from fractions import Fraction

from mpmath import iv, mp
from mpmath.libmp import to_rational

import osil_exact
from exact_io import dec_ceil, dec_floor, read_point, to_decimal

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil/lukvle10.osil")
SEED = "points/lukvle10_seed.txt"
BOX = "points/lukvle10_box.txt.gz"
DPS = 750           # interval working precision (decimal digits)
SEED_DIGITS = 640   # decimals kept in the rational seeds
CENTRE_DIGITS = 60  # decimals of the box centres in the saved box
DUAL = Fraction("352.2380254050784")  # our rigorous dual bound (open-instances-summary.md)


def tree_vars(t, out):
    if t[0] == "var":
        out.add(t[1])
    elif t[0] != "num":
        for c in t[1:]:
            tree_vars(c, out)


def triangular_order(I):
    """Return [(row index, pivot)] in pivot order and the seed variables; assert the structure."""
    n = len(I["names"])
    piv = []
    for r, row in enumerate(I["cons"]):
        assert row["lb"] is not None and row["lb"] == row["ub"], "only equality rows supported"
        qv, nv = set(), set()
        for i, j, _ in row["quad"]:
            qv |= {i, j}
        if row["nl"] is not None:
            tree_vars(row["nl"], nv)
        allv = set(row["lin"]) | qv | nv
        p = max(allv)
        assert row["lin"].get(p, 0) != 0 and p not in qv and p not in nv
        piv.append((r, p))
    piv.sort(key=lambda rp: rp[1])
    pivots = [p for _, p in piv]
    assert len(set(pivots)) == len(pivots)
    seeds = sorted(set(range(n)) - set(pivots))
    return piv, seeds


def write_seeds(I, seeds):
    """Round the KKT point's seed coordinates to SEED_DIGITS decimals (done once)."""
    kkt = {}
    for line in open("logs/lukvle10_kkt_x.txt"):
        nm, val = line.split()
        kkt[nm] = val
    with open(SEED, "w") as f:
        f.write(f"# lukvle10 exact rational seeds (decimals), rounded from the KKT point to {SEED_DIGITS} digits\n")
        for k in seeds:
            nm = I["names"][k]
            mp.dps = DPS
            q = Fraction(int(mp.nint(mp.mpf(kkt[nm]) * 10 ** SEED_DIGITS)), 10 ** SEED_DIGITS)
            f.write(f"{nm} {to_decimal(q)}\n")


def lo(v):
    """exact lower end of an mpmath interval, as a Fraction"""
    return Fraction(*to_rational(v._mpi_[0]))


def hi(v):
    """exact upper end of an mpmath interval, as a Fraction"""
    return Fraction(*to_rational(v._mpi_[1]))


def sig_ceil(q, digits=2):
    """a number with `digits` significant decimal digits that is > q (exact Fraction); 0 for q = 0"""
    if q == 0:
        return Fraction(0)
    e = len(str(q.numerator // q.denominator)) if q >= 1 else -len(str(q.denominator // q.numerator))
    while Fraction(10) ** e <= q:
        e += 1
    while Fraction(10) ** (e - 1) > q:
        e -= 1
    unit = Fraction(10) ** (e - digits)  # 10^(e-1) <= q < 10^e
    return (q // unit + 1) * unit


def main():
    t0 = time.time()
    I = osil_exact.read(OSIL)
    n = len(I["names"])
    assert all(t == "C" for t in I["vtype"])
    piv, seeds = triangular_order(I)
    print(f"{len(piv)} pivot rows, seeds {[I['names'][k] for k in seeds]}", flush=True)
    if not os.path.exists(SEED):
        write_seeds(I, seeds)
    S = read_point(SEED)
    assert set(S) == {I["names"][k] for k in seeds}

    iv.dps = DPS
    A = osil_exact.IntervalArith(iv)
    X = [None] * n
    for k in seeds:
        X[k] = A.const(S[I["names"][k]])
    for r, p in piv:
        row = I["cons"][r]
        rest = dict(row, lin={j: c for j, c in row["lin"].items() if j != p})
        X[p] = (A.const(row["lb"]) - osil_exact.eval_row(rest, X, A)) / A.const(row["lin"][p])
    L = [lo(v) for v in X]
    H = [hi(v) for v in X]
    maxrad = max(H[k] - L[k] for k in range(n)) / 2
    # bounds over the enclosure (all variables are free here; checked generically)
    for k in range(n):
        assert I["lb"][k] is None or L[k] >= I["lb"][k]
        assert I["ub"][k] is None or H[k] <= I["ub"][k]
    # sanity: every row evaluated over the enclosure must contain its right-hand side
    worst = Fraction(0)
    for row in I["cons"]:
        v = osil_exact.eval_row(row, X, A)
        assert lo(v) <= row["lb"] <= hi(v)
        worst = max(worst, hi(v) - lo(v))
    obj = osil_exact.eval_row(I["obj"], X, A)
    print(f"tight enclosure: max coordinate radius {float(maxrad):.3e}, objective width "
          f"{float(hi(obj) - lo(obj)):.3e} ({time.time() - t0:.0f} s)", flush=True)

    # saved box: decimal centres with CENTRE_DIGITS digits and radii rounded up to 2 significant digits
    scale = 10 ** CENTRE_DIGITS
    centres, radii, boxX = [], [], []
    for k in range(n):
        c = Fraction(round((L[k] + H[k]) / 2 * scale), scale)
        rq = sig_ceil(max(H[k] - c, c - L[k]))
        assert c - rq <= L[k] and H[k] <= c + rq
        centres.append(c)
        radii.append(rq)
        boxX.append(iv.mpf([A.const(c - rq).a, A.const(c + rq).b]))
        assert lo(boxX[k]) <= c - rq and hi(boxX[k]) >= c + rq
    obj_box = osil_exact.eval_row(I["obj"], boxX, A)
    with gzip.open(BOX, "wt") as f:
        f.write("# lukvle10: the exactly feasible point x* (seeds in lukvle10_seed.txt, other coordinates\n")
        f.write("# defined by the rows) lies in the closed box  centre +- radius  given per variable below.\n")
        f.write("# name centre radius (both exact decimals)\n")
        for k in range(n):
            f.write(f"{I['names'][k]} {to_decimal(centres[k])} {to_decimal(radii[k])}\n")

    rec = dict(
        dps=DPS, seed_digits=SEED_DIGITS, seeds=[I["names"][k] for k in seeds],
        n_vars=n, n_rows=len(I["cons"]), max_coordinate_radius=f"{float(maxrad):.3e}",
        max_row_enclosure_width=f"{float(worst):.3e}",
        min_abs_coordinate=dec_floor(min(min(abs(L[k]), abs(H[k])) for k in range(n)), 12),
        objective_tight=[dec_floor(lo(obj), 40), dec_ceil(hi(obj), 40)],
        objective_tight_width=f"{float(hi(obj) - lo(obj)):.3e}",
        box_max_radius=to_decimal(max(radii)),
        objective_box=[dec_floor(lo(obj_box), 40), dec_ceil(hi(obj_box), 40)],
        objective_box_width=f"{float(hi(obj_box) - lo(obj_box)):.3e}",
        dual_bound=to_decimal(DUAL),
        gap_upper_tight=dec_ceil(hi(obj) - DUAL, 25),
        gap_upper_box=dec_ceil(hi(obj_box) - DUAL, 25),
        rel_gap_upper_box=f"{float(hi(obj_box) - DUAL) / float(DUAL):.4e}",
        seconds=round(time.time() - t0, 1))
    print(json.dumps(rec, indent=1))
    json.dump(rec, open("logs/lukvle10_enclose.json", "w"), indent=1)


if __name__ == "__main__":
    main()
