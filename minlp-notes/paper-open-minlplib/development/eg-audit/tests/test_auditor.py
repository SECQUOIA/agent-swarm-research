"""Unit tests of cert/auditor.py.

  python3 test_auditor.py [n]      (n random arguments per range for the speed/acceptance part)

1. Constants: auditor.self_test() (runs at import; exact rational arithmetic).
2. Enclosure: lo <= e^x <= hi checked against mpmath at 300 bits on random arguments and on
   edge cases (reduction half-points (m+1/2) ln2/64 and their neighbours, multiples of ln2/64,
   -708, 709, 0, +-subnormals, -700, 600).  Maximum relative width reported.
3. Acceptance: np.exp and x ** k as numpy computes them pass the audit on the certifier's argument
   ranges (exp: [-745, 1e-10], [0, 17], x < -708; powers: [0, 3.2], [0, 40], tiny x).
   Measured errors of np.exp and np.power against mpmath / exact rationals are reported.
4. Soundness (negative tests): values whose exact relative error exceeds eps (1.0001, 1.5, 10 and
   1e4 times eps, both signs), NaN, inf, negative results, x < -708 with y < 0 or y > 2^-1020,
   x > 709, powers of negative or NaN x, x = 0 with y != 0, tiny x on the exact path: all must
   fail.  Errors well below eps (0.3 eps) must pass (the audit is not over-strict).
"""
import os
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cert"))
import auditor as A  # noqa: E402

mp.mp.prec = 300
EPS = float(A.EPS_EXP)
fails = 0


def check(cond, msg):
    global fails
    print(f"  {'ok  ' if cond else 'FAIL'} {msg}")
    fails += not cond


def exact_exp(x):
    return mp.exp(mp.mpf(float(x)))


def perturbed_exp(x, rel):
    """nearest float to e^x (1 + rel), computed in 300-bit arithmetic."""
    return np.array([float(exact_exp(v) * (1 + mp.mpf(rel))) for v in x])


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    rng = np.random.default_rng(2026)
    print("== 1. constants")
    check(A.self_test(), f"self_test (L1 {A.L1!r}, L2 {A.L2!r}, DL {float(A.DL):.2e}, DR {float(A.DR):.2e}, "
                         f"rho_H {float(A.RHO_H):.3e}, CLO {A.CLO!r}, CHI {A.CHI!r})")
    print("== 2. enclosure vs mpmath (300 bits)")
    L = float(mp.log(2) / 64)
    ms = rng.integers(-65371, 65460, 3000)
    half = (ms + 0.5) * L
    x = np.concatenate([rng.uniform(-708, 0, 15000), rng.uniform(0, 17, 3000),
                        rng.uniform(-1, 1, 2000) * 10.0 ** rng.uniform(-300, 0, 2000),
                        half, np.nextafter(half, np.inf), np.nextafter(half, -np.inf), ms * L,
                        [-708.0, 709.0, 0.0, -0.0, 5e-324, -5e-324, -700.0, 600.0, 1e-10, -707.9999999999]])
    x = x[(x >= -708) & (x <= 709)]
    lo, hi, valid = A.exp_enclosure(x)
    check(bool(valid.all()), f"reduction valid on all {len(x)} arguments")
    bad, worst = 0, 0.0
    for xi, l, h in zip(x, lo, hi):
        e = exact_exp(xi)
        bad += not (mp.mpf(float(l)) <= e <= mp.mpf(float(h)))
        worst = max(worst, float((mp.mpf(float(h)) - mp.mpf(float(l))) / e))
    check(bad == 0, f"lo <= e^x <= hi on all {len(x)} arguments; max relative width {worst:.3e}")
    print("== 3. acceptance of numpy's results")
    xe = np.concatenate([rng.uniform(-745, 1e-10, n), rng.uniform(0, 17, n // 4), rng.uniform(-5000, -708, 1000),
                         -10.0 ** rng.uniform(-20, 0, 1000), [-708.0, -708.0000001, 0.0, 700.0]])
    t0 = time.perf_counter()
    ok = A.exp_ok(xe, np.exp(xe))
    dt = time.perf_counter() - t0
    check(bool(ok.all()), f"np.exp passes on {len(xe)} arguments ({1e9 * dt / len(xe):.0f} ns/argument)")
    sub = rng.choice(len(xe), 3000, replace=False)
    err = max(float(abs(mp.mpf(float(np.exp(xe[i]))) / exact_exp(xe[i]) - 1)) for i in sub if xe[i] >= -708)
    print(f"  (measured: max relative error of np.exp on 3000 sampled arguments {err:.3e} = {err / 2 ** -53:.2f} u)")
    for k in (2, 3, 4):
        xp = np.concatenate([rng.uniform(0, 3.2, n), rng.uniform(0, 40, n // 4), 10.0 ** rng.uniform(-75, 1.5, 2000),
                             [0.0, 1.0, 0.1, 2.0 ** -250, 2.0 ** -251, 3e-77]])
        y = xp ** k
        t0 = time.perf_counter()
        ok = A.pow_ok(xp, k, y)
        dt = time.perf_counter() - t0
        check(bool(ok.all()), f"x ** {k} passes on {len(xp)} values ({1e9 * dt / len(xp):.0f} ns/value)")
        w = 0.0
        for i in rng.choice(len(xp), 3000, replace=False):
            ex = Fr(float(xp[i])) ** k
            if ex:
                w = max(w, float(abs(Fr(float(y[i])) - ex) / ex))
        print(f"  (measured: max relative error of x ** {k} on 3000 sampled values {w:.3e} = {w / 2 ** -53:.2f} u)")
    print("== 4. soundness: errors above eps must fail, errors well below eps must pass")
    xs = np.concatenate([rng.uniform(-708, 0, 300), rng.uniform(0, 17, 100), [0.0, -708.0, 709.0]])
    for rel in (1.0001, 1.5, 10.0, 1e4):
        for sgn in (1, -1):
            yb = perturbed_exp(xs, sgn * rel * EPS)
            check(not A.exp_ok(xs, yb).any(), f"exp: relative error {sgn * rel:g} eps flagged on all {len(xs)} arguments")
    yg = perturbed_exp(xs, 0.3 * EPS)
    check(bool(A.exp_ok(xs, yg).all()), "exp: relative error 0.3 eps accepted")
    yg = perturbed_exp(xs, -0.3 * EPS)
    check(bool(A.exp_ok(xs, yg).all()), "exp: relative error -0.3 eps accepted")
    special = [(0.0, np.nan), (0.0, np.inf), (-1.0, -np.exp(-1.0)), (np.nan, 1.0), (710.0, np.exp(710.0)),
               (-800.0, -1e-320), (-800.0, 2.0 ** -1019), (-708.5, 1e-300), (-1.0, 0.0)]
    for xv, yv in special:
        with np.errstate(over="ignore"):
            check(not A.exp_ok(np.array([xv]), np.array([yv]))[0], f"exp: (x, y) = ({xv}, {yv}) flagged")
    check(bool(A.exp_ok(np.array([-800.0, -745.0, -709.0]), np.array([0.0, 5e-324, np.exp(-709.0)])).all()),
          "exp: x < -708 with 0 <= y <= 2^-1020 accepted")
    for k in (2, 3, 4):
        xp = np.concatenate([rng.uniform(1e-3, 40, 300), [3e-77, 2.0 ** -250, 1.0]])
        for rel in (1.0001, 1.5, 10.0):
            for sgn in (1, -1):
                yb = np.array([float(Fr(float(v)) ** k * (1 + sgn * Fr(rel) * A.EPS_POW)) for v in xp])
                exact_bad = np.array([abs(Fr(float(b)) - Fr(float(v)) ** k) > A.EPS_POW * Fr(float(v)) ** k
                                      for b, v in zip(yb, xp)])
                flagged = ~A.pow_ok(xp, k, yb)
                check(bool(np.all(flagged[exact_bad])) and exact_bad.any(),
                      f"pow k={k}: relative error {sgn * rel:g} eps: all {int(exact_bad.sum())} values whose rounded "
                      f"result still has exact error > eps are flagged ({int(flagged.sum())} flagged)")
        yg = np.array([float(Fr(float(v)) ** k * (1 + Fr(3, 10) * A.EPS_POW)) for v in xp])
        check(bool(A.pow_ok(xp, k, yg).all()), f"pow k={k}: relative error 0.3 eps accepted")
        for xv, yv in ((-1.0, (-1.0) ** k), (np.nan, 1.0), (0.0, 1e-300), (2.0 ** 251, 2.0 ** (251 * k) if k < 4 else np.inf),
                       (1e-100, 1e-100 ** k * 1.5), (1.0, np.nan)):
            with np.errstate(over="ignore", invalid="ignore"):
                check(not A.pow_ok(np.array([xv]), k, np.array([yv]))[0], f"pow k={k}: (x, y) = ({xv}, {yv}) flagged")
        check(bool(A.pow_ok(np.array([0.0, 3e-77]), k, np.array([0.0, 3e-77]) ** k).all()),
              f"pow k={k}: x = 0 and the exact path (x = 3e-77 < 2^-250) accepted")
        xu = {2: np.array([1e-160, 1e-200, 1e-300]), 3: np.array([1e-110, 1e-120, 1e-160, 1e-200, 1e-300]),
              4: np.array([1e-80, 1e-120, 1e-160, 1e-200, 1e-300])}[k]          # x^k underflows
        with np.errstate(under="ignore"):
            yu = xu ** k
        ex_bad = np.array([abs(Fr(float(b)) - Fr(float(v)) ** k) > A.EPS_POW * Fr(float(v)) ** k for b, v in zip(yu, xu)])
        check(bool(np.all(~A.pow_ok(xu, k, yu)[ex_bad])) and ex_bad.all(),
              f"pow k={k}: underflowed powers (relative error > eps) flagged, x = {xu.tolist()}")
    print("ALL AUDITOR TESTS PASSED" if not fails else f"AUDITOR TESTS FAILED: {fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
