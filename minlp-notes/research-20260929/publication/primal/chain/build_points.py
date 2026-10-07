"""Construct exactly feasible points for chain50/100/200/400 (COPS hanging chain).

Model (cached OSIL, structure asserted by verify_points.py, not here):
  variables x_0..x_N, u_0..u_N, free except x_0 = 1 and x_N = 3;
  rows      x_{i+1} - x_i - eta*(u_i + u_{i+1}) = 0      (i = 0..N-1)
            eta * sum_{i<N} (s_i + s_{i+1}) = 4,  s_i = sqrt(u_i^2 + 1)
  objective eta * sum_{i<N} (s_i x_i + s_{i+1} x_{i+1}),  eta = 1/(2N).

With w_0 = w_N = 1 and w_i = 2 otherwise, a point satisfies all rows iff
  x is propagated from x_0 = 1 by the linear rows,
  sum_i w_i u_i = 4N   (this makes x_N = 3),
  sum_i w_i s_i = 8N   (the length row).
Write t_i = u_i + s_i > 0, so that 1/t_i = s_i - u_i, u_i = (t_i - 1/t_i)/2 and
s_i = (t_i + 1/t_i)/2. Every rational t_i gives rational u_i and s_i with
s_i = sqrt(1 + u_i^2) exactly. The two conditions become
  sum_i w_i t_i = 12N  and  sum_i w_i / t_i = 4N.

Construction: start from the saved double-precision point of the wave-2 run
(open-instances-wave2/cops/logs/chainN_primal.txt), compute t_i there, round
t_i to K decimal places for every i except two interior indices a < b, and
solve the remaining 2x2 system exactly:
  t_a + t_b = alpha,  1/t_a + 1/t_b = beta
  => t_a, t_b are the roots of T^2 - alpha*T + alpha/beta = 0.
The roots lie in the quadratic field Q(sqrt(R)) for an integer R, so the
whole point lies in Q(sqrt(R)) and every row can be checked exactly.

Outputs (points/):
  chainN_generator.json  the exact definition of the point (decimal t_i, a, b,
                         root choice) and the derived integer R;
  chainN_box.json        every OSIL variable as a 45-significant-digit decimal
                         centre with a common rigorous radius, plus the exact
                         objective enclosure.
The independent check is verify_points.py (shares no code with this file).
"""
import json
import math
import os
import sys
from fractions import Fraction as F

import mpmath as mp

sys.set_int_max_str_digits(0)
HERE = os.path.dirname(os.path.abspath(__file__))
R29 = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))  # research-20260929/
PRIMAL = os.path.join(R29, "open-instances-wave2/cops/logs/chain%d_primal.txt")
K = 20            # decimal places of the fixed t_i
DIGITS = 45       # significant digits of the box centres
RADIUS = F("1e-40")


class QR:
    """p + q*sqrt(R) with rational p, q and a fixed positive integer R."""
    R = None

    def __init__(self, p, q=0):
        self.p, self.q = F(p), F(q)

    def __add__(s, o):
        o = o if isinstance(o, QR) else QR(o)
        return QR(s.p + o.p, s.q + o.q)

    __radd__ = __add__

    def __sub__(s, o):
        o = o if isinstance(o, QR) else QR(o)
        return QR(s.p - o.p, s.q - o.q)

    def __mul__(s, o):
        o = o if isinstance(o, QR) else QR(o)
        return QR(s.p * o.p + s.q * o.q * QR.R, s.p * o.q + s.q * o.p)

    __rmul__ = __mul__

    def inv(s):
        n = s.p * s.p - s.q * s.q * QR.R
        assert n != 0
        return QR(s.p / n, -s.q / n)

    def sign(s):
        a, b = s.p, s.q
        if b == 0:
            return (a > 0) - (a < 0)
        if a == 0 or (a > 0) == (b > 0):
            return 1 if (a > 0 or (a == 0 and b > 0)) else -1
        # opposite signs: compare a^2 with b^2 R
        big = a * a > b * b * QR.R
        return (1 if a > 0 else -1) if big else (1 if b > 0 else -1)

    def enclose(s, k):
        """rational [lo, hi] containing the real value, sqrt(R) known to 10^-k."""
        r = math.isqrt(QR.R * 10 ** (2 * k))
        lo, hi = F(r, 10 ** k), F(r + 1, 10 ** k)
        a, b = s.p + s.q * lo, s.p + s.q * hi
        return min(a, b), max(a, b)


def dec_centre(v, k=90):
    """45-significant-digit decimal string within 1e-40 of v (rigorous)."""
    lo, hi = v.enclose(k)
    mid = (lo + hi) / 2
    mp.mp.dps = 120
    m = mp.mpf(mid.numerator) / mid.denominator
    c = mp.nstr(m, DIGITS, min_fixed=-10**9, max_fixed=10**9, strip_zeros=False)
    cf = F(c)
    assert max(hi - cf, cf - lo) <= RADIUS, (c, float(hi - cf), float(cf - lo))
    # exact containment: |v - c| <= RADIUS
    assert (v - (cf + RADIUS)).sign() <= 0 and (v - (cf - RADIUS)).sign() >= 0
    return c


def build(N):
    vals = [float(s) for s in open(PRIMAL % N).read().split()]
    assert len(vals) == 2 * N + 2
    u_dbl = vals[N + 1:]
    x_dbl = vals[:N + 1]
    mp.mp.dps = 50
    tstar = [mp.mpf(u) + mp.sqrt(1 + mp.mpf(u) ** 2) for u in u_dbl]
    a = min(range(1, N), key=lambda i: tstar[i])
    b = max(range(1, N), key=lambda i: tstar[i])
    assert 0 < a < b < N or 0 < b < a < N
    a, b = min(a, b), max(a, b)
    w = [1] + [2] * (N - 1) + [1]
    t = [None] * (N + 1)
    tdec = [None] * (N + 1)
    for i in range(N + 1):
        if i in (a, b):
            continue
        q = F(round(F(mp.nstr(tstar[i], 40, min_fixed=-10**9, max_fixed=10**9)) * 10 ** K), 10 ** K)
        tdec[i] = format_decimal(q, K)
        t[i] = F(tdec[i])
        assert t[i] == q and t[i] > 0
    alpha = (12 * N - sum(w[i] * t[i] for i in range(N + 1) if i not in (a, b))) / 2
    beta = (4 * N - sum(F(w[i]) / t[i] for i in range(N + 1) if i not in (a, b))) / 2
    disc = alpha * alpha - 4 * alpha / beta
    assert disc > 0 and alpha > 0 and beta > 0
    R = disc.numerator * disc.denominator           # sqrt(disc) = sqrt(R)/den
    assert math.isqrt(R) ** 2 != R, "R is a perfect square: the point is rational"
    QR.R = R
    sq = QR(0, F(1, disc.denominator))              # = sqrt(disc)
    lo_root = QR(alpha / 2) - F(1, 2) * sq
    hi_root = QR(alpha / 2) + F(1, 2) * sq
    # a has the smaller optimal t (a = 1 for the saved points), b the larger
    ta, tb = (lo_root, hi_root) if tstar[a] < tstar[b] else (hi_root, lo_root)
    root_a = "smaller" if tstar[a] < tstar[b] else "larger"
    assert ta.sign() > 0 and tb.sign() > 0
    T = [QR(t[i]) if i not in (a, b) else (ta if i == a else tb) for i in range(N + 1)]
    u = [(Ti - Ti.inv()) * F(1, 2) for Ti in T]
    s = [(Ti + Ti.inv()) * F(1, 2) for Ti in T]
    eta = F(1, 2 * N)
    x = [QR(1)]
    for i in range(N):
        x.append(x[i] + eta * (u[i] + u[i + 1]))
    # exact checks of the reformulated conditions (the OSIL check is separate)
    assert (x[N] - 3).sign() == 0
    length = eta * sum((s[i] + s[i + 1] for i in range(N)), QR(0))
    assert (length - 4).sign() == 0
    for i in range(N + 1):
        assert (s[i] * s[i] - (u[i] * u[i] + 1)).sign() == 0 and s[i].sign() > 0
    obj = eta * sum((s[i] * x[i] + s[i + 1] * x[i + 1] for i in range(N)), QR(0))
    olo, ohi = obj.enclose(80)
    # distance to the saved double point (information only)
    mp.mp.dps = 40
    dx = max(abs(float(x[i].enclose(40)[0] - F(x_dbl[i]))) for i in range(N + 1))
    du = max(abs(float(u[i].enclose(40)[0] - F(u_dbl[i]))) for i in range(N + 1))
    gen = dict(
        instance="chain%d" % N, N=N, eta="1/(2N) = %s" % str(eta),
        definition=(
            "w_0 = w_N = 1, w_i = 2 otherwise. For i not in {a, b}, t_i is the decimal given. "
            "alpha = (12N - sum_{i not in {a,b}} w_i t_i)/2, beta = (4N - sum_{i not in {a,b}} w_i/t_i)/2; "
            "t_a, t_b are the two roots of T^2 - alpha T + alpha/beta = 0 (t_a the '%s' one). "
            "u_i = (t_i - 1/t_i)/2 for all i (OSIL variable index N+1+i); "
            "x_0 = 1, x_{i+1} = x_i + eta (u_i + u_{i+1}) (OSIL variable index i)." % root_a),
        a=a, b=b, root_a=root_a, decimal_places=K,
        t=tdec,
        R=str(R), disc_denominator=str(disc.denominator),
        t_a_approx=mp.nstr(mp.mpf(ta.enclose(60)[0].numerator) / ta.enclose(60)[0].denominator, 30),
        t_b_approx=mp.nstr(mp.mpf(tb.enclose(60)[0].numerator) / tb.enclose(60)[0].denominator, 30),
        R_digits=len(str(R)),
        source_point=PRIMAL % N,
        max_abs_diff_to_source=dict(x=dx, u=du),
    )
    names = ["x%d" % (i + 1) for i in range(2 * N + 2)]  # OSIL names x1..x(2N+2)
    coords = x + u
    box = dict(
        instance="chain%d" % N,
        note=("The exactly feasible point of chainN_generator.json lies in the box "
              "[centre - radius, centre + radius] in every coordinate (checked exactly)."),
        radius="1e-40",
        variables=[dict(index=j, name=names[j], centre=dec_centre(coords[j])) for j in range(2 * N + 2)],
        objective_enclosure=[str(olo), str(ohi)],
        objective_enclosure_decimal=[fmt_down(olo, 40), fmt_up(ohi, 40)],
    )
    with open("%s/points/chain%d_generator.json" % (HERE, N), "w") as f:
        json.dump(gen, f, indent=1)
    with open("%s/points/chain%d_box.json" % (HERE, N), "w") as f:
        json.dump(box, f, indent=1)
    print("chain%d a=%d b=%d R digits=%d obj in [%s, %s] max|dx|=%.2e max|du|=%.2e"
          % (N, a, b, len(str(R)), fmt_down(olo, 30), fmt_up(ohi, 30), dx, du), flush=True)


def format_decimal(q, k):
    """exact decimal string of q = n / 10^k."""
    n = q * 10 ** k
    assert n.denominator == 1
    n = n.numerator
    sgn = "-" if n < 0 else ""
    n = abs(n)
    return "%s%d.%0*d" % (sgn, n // 10 ** k, k, n % 10 ** k)


def fmt_down(q, k):
    return format_decimal(F(math.floor(q * 10 ** k), 10 ** k), k)


def fmt_up(q, k):
    return format_decimal(F(math.ceil(q * 10 ** k), 10 ** k), k)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        build(int(arg))
