"""Lane M1: exact check of bound-corrected binary64 export (Prop. elimination-round).

For random exact rational rows c.v >= r and bounds L <= v <= U (some one-sided
infinite), export c_hat = binary64 round-to-nearest of c, compute
  E = sum_j inf_{s in [L_j, U_j]} (c_hat_j - c_j) s       (exact),
  r_hat = largest binary64 <= r + E,
and verify with an exact LP that  min { c_hat.v : c.v >= r, L <= v <= U } >= r_hat.
Also exhibits that the uncorrected export (r_hat = RD(r)) can be invalid.
Run: code/minlp_solver_lab/.venv/bin/python paper-certified-support-cuts/verification/M1_rounding.py
"""
import math
import os
import random
import sys
from fractions import Fraction as Fr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from M1_exactlp import solve_lp  # noqa: E402

random.seed(11)


def round_down64(q):
    f = float(q)
    if Fr(f) > q:
        f = math.nextafter(f, -math.inf)
    assert Fr(f) <= q
    return f


def correction(delta, L, U):
    """Exact E, or None if a needed bound is infinite (zero delta needs none)."""
    E = Fr(0)
    for dj, lj, uj in zip(delta, L, U):
        if dj > 0:
            if lj is None:
                return None
            E += dj * lj
        elif dj < 0:
            if uj is None:
                return None
            E += dj * uj
    return E


def lp_min(chat, c, r, L, U):
    n = len(c)
    st, val, _ = solve_lp(list(chat), A_ub=[[-v for v in c]], b_ub=[-r], bounds=list(zip(L, U)))
    return st, val


def main(trials=400):
    accepted = refused = 0
    uncorrected_invalid = 0
    for _ in range(trials):
        n = random.randint(1, 4)
        c = [Fr(random.randint(-30, 30), random.choice([3, 7, 10, 1])) * Fr(1, random.choice([1, 10**9]))
             for _ in range(n)]
        if random.random() < 0.3:
            c[0] = Fr(1, 2)              # exactly representable: delta = 0
        r = Fr(random.randint(-50, 50), random.choice([3, 7, 1]))
        chat = [Fr(float(cj)) for cj in c]
        delta = [ch - cj for ch, cj in zip(chat, c)]
        L, U = [], []
        for dj in delta:
            lo = Fr(random.randint(-5, 0)) if random.random() < 0.8 else None
            hi = Fr(random.randint(1, 5)) if random.random() < 0.8 else None
            if dj == 0 and random.random() < 0.5:
                lo, hi = None, None      # unbounded coordinate with exact coefficient
            L.append(lo); U.append(hi)
        st, val = lp_min(chat, c, r, L, U)
        if st == "infeasible":
            continue
        E = correction(delta, L, U)
        if E is None:
            refused += 1
            continue
        assert st == "optimal", st       # bounded below by r + E, so finite
        rhat = round_down64(r + E)
        assert val >= r + E >= Fr(rhat)
        accepted += 1
        if val < Fr(round_down64(r)):
            uncorrected_invalid += 1
    # a deterministic instance where the uncorrected export is invalid
    c = [Fr(1, 3), Fr(1, 7)]   # both round down in binary64
    r = Fr(1)
    chat = [Fr(float(v)) for v in c]
    L, U = [Fr(0), Fr(0)], [Fr(10**6), Fr(10**6)]
    st, val = lp_min(chat, c, r, L, U)
    assert st == "optimal" and val < Fr(round_down64(r))  # c_hat.v >= 1 is NOT valid
    E = correction([a - b for a, b in zip(chat, c)], L, U)
    assert val >= r + E
    print(f"rounding: {accepted} corrected exports verified exactly, {refused} refused "
          f"(needed bound infinite), {uncorrected_invalid} random uncorrected exports invalid; "
          f"deterministic counterexample: min c_hat.v - 1 = {float(val - 1):.3e} < 0 for uncorrected row")


if __name__ == "__main__":
    main()
    print("M1_rounding: all checks passed")
