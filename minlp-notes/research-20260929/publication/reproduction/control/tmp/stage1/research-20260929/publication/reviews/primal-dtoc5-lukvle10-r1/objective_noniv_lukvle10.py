"""Reviewer's second enclosure of f(x*) for lukvle10 that does not use mpmath at all.

x* is the point defined by the seeds in points/lukvle10_seed.txt and the rows
  x_{j+2} = (1 - x_j + 3 x_{j+1} - 2 x_{j+1}^2) / 2      (form checked against the OSIL by
                                                         check_lukvle10.py: report_row_form_matches_osil)
All arithmetic is on integers: a value v is held as an integer interval [L, U] with
L 2^-Q <= v <= U 2^-Q, and every operation rounds outward with exact floor/ceil.
ln and exp are bounded by series with explicit remainder bounds:
  ln(v) = 2 atanh(z) + e ln 2, z = (m-1)/(m+1) in [0, 1/3), m = v 2^-e in [1, 2),
          atanh(z) in [S_N(z), S_N(z) + z^(2N+1) / ((2N+1)(1-z^2))];
  exp(y) = exp(y 2^-s)^(2^s), |y 2^-s| < 2^-10, Taylor with K terms and remainder 2 t^(K+1)/(K+1)!;
          exp(t) = 1/exp(-t) for t < 0.
The only assumption is that Python integer arithmetic is correct.
Usage: python3 objective_noniv_lukvle10.py Q
"""
import json, os, sys, time
from fractions import Fraction

T0 = time.time()
Q = int(sys.argv[1]) if len(sys.argv) > 1 else 400
PP = Q + 2400  # propagation precision (bits); widths grow by about 10^488 along the chain
import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../../.."))
TRACK = _REPO + "/research-20260929/publication/primal/dtoc5-lukvle10"
ONE = 1 << Q


def cdiv(a, b):
    return -((-a) // b)


# ---------- propagation at PP bits ----------
SP = 1 << PP
seeds = {}
for line in open(TRACK + "/points/lukvle10_seed.txt"):
    if line.startswith("#") or not line.strip():
        continue
    k, v = line.split()
    seeds[k] = Fraction(v)


def civ(q):
    return (q.numerator * SP // q.denominator, cdiv(q.numerator * SP, q.denominator))


def sq(a, S):
    lo, hi = a
    if lo >= 0:
        return (lo * lo // S, cdiv(hi * hi, S))
    if hi <= 0:
        return (hi * hi // S, cdiv(lo * lo, S))
    return (0, cdiv(max(lo * lo, hi * hi), S))


X = [civ(seeds["x1"]), civ(seeds["x2"])]
for j in range(998):
    a, b = X[j], X[j + 1]
    s = sq(b, SP)
    lo = SP - a[1] + 3 * b[0] - 2 * s[1]
    hi = SP - a[0] + 3 * b[1] - 2 * s[0]
    X.append((lo // 2, cdiv(hi, 2)))
# round to Q bits outward
sh = PP - Q
XQ = [(lo >> sh, -((-hi) >> sh)) for lo, hi in X]
wmax = max(hi - lo for lo, hi in XQ)
print("propagated; max width in units of 2^-Q:", wmax, flush=True)

# ---------- ln and exp bounds (fixed point, scale 2^-Q) ----------
NAT = 2 * Q // 3 + 20  # atanh terms: (1/3)^(2N+1) < 2^-Q needs N > Q/3.17


def atanh_bounds(z_num, z_den):
    """bounds of atanh(z) for rational 0 <= z < 1/3 (exact numerator/denominator)"""
    zl = z_num * ONE // z_den
    zh = cdiv(z_num * ONE, z_den)
    # lower: terms rounded down
    z2l = zl * zl // ONE
    p = zl
    lo = 0
    for i in range(NAT):
        lo += p // (2 * i + 1)
        p = p * z2l // ONE
    # upper: terms rounded up, plus remainder
    z2h = cdiv(zh * zh, ONE)
    p = zh
    hi = 0
    for i in range(NAT):
        hi += cdiv(p, 2 * i + 1)
        p = cdiv(p * z2h, ONE)
    # p >= z^(2N+1) now; remainder <= p / ((2N+1)(1 - z^2)), 1 - z^2 >= 8/9
    hi += cdiv(p * 9, (2 * NAT + 1) * 8) + 1
    return lo, hi


L2 = atanh_bounds(1, 3)
LN2 = (2 * L2[0], 2 * L2[1])


def ln_bounds(N):
    """bounds of ln(N 2^-Q) for integer N > 0"""
    assert N > 0
    b = N.bit_length()
    e = b - 1 - Q  # N 2^-Q = m 2^e, m = N / 2^(b-1) in [1, 2)
    base = 1 << (b - 1)
    lo, hi = atanh_bounds(N - base, N + base)
    lo, hi = 2 * lo, 2 * hi
    if e >= 0:
        return lo + e * LN2[0], hi + e * LN2[1]
    return lo + e * LN2[1], hi + e * LN2[0]


KT = 2 * Q // 10 + 10  # Taylor terms for |t| < 2^-10


def exp_small_pos(T):
    """bounds of exp(T 2^-Q) for 0 <= T < 2^(Q-10)"""
    lo, term = 0, ONE
    for k in range(KT):
        lo += term
        term = term * T // (ONE * (k + 1))
    hi, term = 0, ONE
    for k in range(KT):
        hi += term
        term = cdiv(term * T, ONE * (k + 1))
    hi += 2 * term + 1  # term >= t^KT/KT!; remainder <= 2 t^KT / KT!
    return lo, hi


def exp_bounds_point(Y, upper):
    """lower (upper=False) or upper (upper=True) bound of exp(Y 2^-Q)"""
    s = max(0, abs(Y).bit_length() - Q + 10)
    T = (-((-Y) >> s)) if upper else (Y >> s)  # ceil / floor of Y / 2^s
    if T >= 0:
        lo, hi = exp_small_pos(T)
        v = hi if upper else lo
    else:
        lo, hi = exp_small_pos(-T)
        v = cdiv(ONE * ONE, lo) if upper else (ONE * ONE) // hi
    for _ in range(s):
        v = cdiv(v * v, ONE) if upper else v * v // ONE
    return v


def mul_iv(a, b):
    ps = [a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1]]
    return (min(ps) // ONE, cdiv(max(ps), ONE))


assert LN2[0] < LN2[1] and LN2[1] - LN2[0] < 10 ** 6

F = (0, 0)
for i in range(500):
    for a, b in ((2 * i, 2 * i + 1), (2 * i + 1, 2 * i)):
        A = sq(XQ[a], ONE)  # base x_a^2
        B = sq(XQ[b], ONE)
        assert A[0] > 0
        E = (B[0] + ONE, B[1] + ONE)  # exponent x_b^2 + 1
        lnA = (ln_bounds(A[0])[0], ln_bounds(A[1])[1])  # ln increasing
        Y = mul_iv(E, lnA)
        term = (exp_bounds_point(Y[0], False), exp_bounds_point(Y[1], True))
        F = (F[0] + term[0], F[1] + term[1])
flo, fhi = Fraction(F[0], ONE), Fraction(F[1], ONE)


def dec(q, k, up):
    v = q.numerator * 10 ** k
    i = cdiv(v, q.denominator) if up else v // q.denominator
    s = str(abs(i)).rjust(k + 1, "0")
    return ("-" if i < 0 else "") + s[:-k] + "." + s[-k:]


track_lo = Fraction("352.2380254064956226308712710293664647979978")
track_hi = Fraction("352.2380254064956226308712710293664647979979")
out = dict(Q_bits=Q, objective_lo_45=dec(flo, 45, False), objective_hi_45=dec(fhi, 45, True),
           inside_track_enclosure=track_lo <= flo and fhi <= track_hi,
           seconds=round(time.time() - T0, 1))
out["width_log2"] = (F[1] - F[0]).bit_length() - Q
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", f"objective_noniv_lukvle10_Q{Q}.json"), "w"), indent=1)
