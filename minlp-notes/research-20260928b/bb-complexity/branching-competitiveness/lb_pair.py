"""Exact-arithmetic check of the two-instance adversary (Theorem 3, 1D).

alpha = 1, root [0,1].  Each instance is H = m + y^2 = max of lines (slope, intercept).
Instance A has the unique two-piece certificate {1/3}; instance B has the unique
two-piece certificate {3/5}.  Both have min m = eps, the same root relaxation
value, the same unique root relaxation minimizer y1 = 3/5, and f_A = f_B on a
neighbourhood [p, q] of y1.  Hence every node-local rule that sees only data
from [p, q] (box, relaxation minimizer and value, incumbent, eps, values and
derivatives of f there) splits the root at the same point on both, and on at
least one of them some child is invalid: T >= 5 while the optimum is 3.
"""
from fractions import Fraction as Fr

EPS = Fr(1, 10000)
Y1 = Fr(3, 5)
S_A = Fr(1, 3)
DELTA = Fr(1, 100)


def chord(a, b):
    # chord of y^2 over [a,b]: y -> (a+b) y - a b
    return (a + b, -a * b)


def through(x, h, slope):
    return (slope, h - slope * x)


def envelope(lines):
    """Knots of max of lines on [0,1] (exact), as sorted list of (x, H(x), active line)."""
    def H(x):
        return max(s * x + b for s, b in lines)
    xs = {Fr(0), Fr(1)}
    for i, (s1, b1) in enumerate(lines):
        for s2, b2 in lines[i + 1:]:
            if s1 != s2:
                x = (b2 - b1) / (s1 - s2)
                if 0 < x < 1 and s1 * x + b1 == H(x):
                    xs.add(x)
    xs = sorted(xs)
    return xs, [H(x) for x in xs], H


def active(lines, x):
    Hx = max(s * x + b for s, b in lines)
    return sorted((s, b) for s, b in lines if s * x + b == Hx)


def analyse(name, lines, expect_s):
    xs, Hs, H = envelope(lines)
    ms = [h - x * x for x, h in zip(xs, Hs)]
    mmin = min(ms)
    print(f"== {name}: {len(xs)} knots; min m = {mmin} (eps = {EPS}); argmin m at "
          f"{[str(x) for x, m in zip(xs, ms) if m == mmin]}")
    assert mmin == EPS
    # root relaxation: phi = m - y(1-y) = H - y; minimum over knots (H - y convex piecewise linear)
    vals = [h - x for x, h in zip(xs, Hs)]
    v = min(vals)
    arg = [x for x, w in zip(xs, vals) if w == v]
    print(f"   root LB (min of m - q) = {v} = {float(v):.6f}; minimizers {[str(a) for a in arg]}")
    assert v < 0 and arg == [Y1]
    # greedy from the left: largest b with [0,b] valid; from the right: smallest a with [a,1] valid
    R0 = Fr(1)
    for x, m in zip(xs, ms):
        if 0 < x < R0:
            R0 = min(R0, x + m / x)
    L1 = Fr(0)
    for x, m in reversed(list(zip(xs, ms))):
        if L1 < x < 1:
            L1 = max(L1, x - m / (1 - x))
    print(f"   [0,b] valid iff b <= {R0}; [a,1] valid iff a >= {L1}")
    assert R0 == L1 == expect_s, "two-piece certificate not unique"
    return xs, H


def main():
    HA_y1 = Fr(4, 3) * Y1 - Fr(1, 3) + DELTA      # chord of y^2 over [1/3,1] at y1, lifted by DELTA
    g_left = through(Y1, HA_y1, Fr(4, 5))
    g_right = through(Y1, HA_y1, Fr(6, 5))
    end0 = (Fr(1, 6), EPS)                          # m = eps + y/6 - y^2 near 0
    end1 = through(Fr(1), 1 + EPS, 2 - Fr(1, 3))     # m = eps + (1-y)(1/3 - (1-y)) near 1
    A = [chord(Fr(0), S_A), chord(S_A, Fr(1)), g_left, g_right, end0, end1]
    B = [chord(Fr(0), Y1), chord(Y1, Fr(1)), g_left, g_right, end0, end1]
    xA, HA = analyse("A (rigid at 1/3)", A, S_A)
    xB, HB = analyse("B (rigid at 3/5)", B, Y1)
    # both envelopes are linear on [p, y1] and [y1, q] (adjacent knots); equality at p, y1, q gives equality on [p, q]
    pA = max(x for x in xA if x < Y1); qA = min(x for x in xA if x > Y1)
    pB = max(x for x in xB if x < Y1); qB = min(x for x in xB if x > Y1)
    p, q = max(pA, pB), min(qA, qB)
    for x in (p, Y1, q):
        assert HA(x) == HB(x)
    assert active(A, Y1) == active(B, Y1) == sorted([g_left, g_right])
    print(f"f_A = f_B on [{p}, {q}] = [{float(p):.4f}, {float(q):.4f}]; both equal max(g_left, g_right) there")
    # consequences at the root split point sigma: on A, sigma != 1/3 leaves an invalid child; on B, sigma != 3/5
    print("any root split sigma: sigma != 1/3 => A has an invalid child; sigma != 3/5 => B has an invalid child;")
    print("so max(T_A, T_B) >= 5 = (5/3) * (2 N_opt - 1) with N_opt = 2 for both.")


if __name__ == "__main__":
    main()
