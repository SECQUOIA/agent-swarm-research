"""Theorem 3 instances and the scope statements, in exact rationals (engine pl1d.py, written for
this recheck).  Checks: f* = 0 in both; same unique root minimizer and value; the maximal
agreement intervals of H_A and H_B (so every finite one-sided jet at 0, 1 and 3/5 agrees);
validity thresholds 1/3 and 3/5; R_min's tree on each instance (T = 5 on A, T = 3 on B), which
shows Proposition 2's bound 5 is attained with N_opt = 2.  Also cross-checks the review's
11/5 instance for R_min.
Usage: python3 thm3_scope_check.py
"""
from fractions import Fraction as Fr

from pl1d import PL1D, upper_envelope

eps = Fr(1, 10000)


def chord(a, b):
    return (a + b, -a * b)                       # (slope, intercept) of chord of y^2


h1 = Fr(143, 300)
g_minus = (Fr(4, 5), h1 - Fr(4, 5) * Fr(3, 5))
g_plus = (Fr(6, 5), h1 - Fr(6, 5) * Fr(3, 5))
e0 = (Fr(1, 6), eps)
e1 = (Fr(5, 3), -Fr(2, 3) + eps)
LA = [chord(Fr(0), Fr(1, 3)), chord(Fr(1, 3), Fr(1)), g_minus, g_plus, e0, e1]
LB = [chord(Fr(0), Fr(3, 5)), chord(Fr(3, 5), Fr(1)), g_minus, g_plus, e0, e1]


def build(lines):
    xs, Hs = upper_envelope(lines, Fr(0), Fr(1))
    return PL1D(xs, [h - x * x for h, x in zip(Hs, xs)])


def agreement(P, Q):
    xs = sorted(set(P.xs) | set(Q.xs))
    eq = [P.H(x) == Q.H(x) for x in xs]
    ivs, cur = [], None
    for i, x in enumerate(xs):
        if eq[i] and cur is None:
            cur = x
        seg_eq = i + 1 < len(xs) and eq[i] and eq[i + 1]
        if cur is not None and not seg_eq:
            ivs.append((cur, x))
            cur = None
    return ivs


def rmin_splits(P):
    out = []

    def rec(l, u):
        if P.valid(l, u):
            return 1
        ch = P.minimizer_choices(l, u)
        assert len(ch) == 1
        out.append(ch[0])
        return 1 + rec(l, ch[0]) + rec(ch[0], u)
    return rec(P.L, P.U), out


def main():
    A, B = build(LA), build(LB)
    for name, P, s in (("A", A, Fr(1, 3)), ("B", B, Fr(3, 5))):
        ms = [P.m(x) for x in P.xs]
        mn = min(ms)
        argm = [x for x, v in zip(P.xs, ms) if v == mn]
        p, v = P.profile(P.L, P.U)
        root = min(v)
        rootmin = [y for y, w in zip(p, v) if w == root]
        N, bps = P.greedy()
        T, splits = rmin_splits(P)
        print(f"{name}: min m = {mn} at {argm}; root LB value {root} at {rootmin}; N_opt = {N}, "
              f"greedy breakpoint {bps}; R_min T = {T}, splits {splits}")
        assert mn == eps and argm == [0, 1] and root == Fr(-37, 300) and rootmin == [Fr(3, 5)]
        assert N == 2 and bps == [s]
        # [0,b] valid iff b <= s; [c,1] valid iff c >= s (probe just beyond s)
        tiny = Fr(1, 10 ** 9)
        assert P.valid(Fr(0), s) and not P.valid(Fr(0), s + tiny)
        assert P.valid(s, Fr(1)) and not P.valid(s - tiny, Fr(1))
    ivs = agreement(A, B)
    print("maximal agreement intervals of H_A, H_B:", [(str(a), str(b)) for a, b in ivs])
    assert ivs == [(Fr(0), 30 * eps / 13), (Fr(1, 60), Fr(27, 40)), (1 - 3 * eps, Fr(1))]
    print("=> any finite one-sided jet at 0 and 1, and any jet at 3/5 (interior of [1/60, 27/40]), agree")

    # the review's 11/5 instance (convex H, eps = 1/100)
    xs = [Fr(0), Fr(1, 16), Fr(3, 16), Fr(7, 16), Fr(1, 2), Fr(9, 16), Fr(13, 16), Fr(15, 16), Fr(1)]
    m = [Fr(41, 1600), Fr(41, 1600), Fr(823, 20000), Fr(1, 100), Fr(1, 100), Fr(1, 100), Fr(823, 20000),
         Fr(41, 1600), Fr(41, 1600)]
    P = PL1D(xs, m)
    N, bps = P.greedy()
    T, splits = rmin_splits(P)
    Tw = P.worst_tree(P.minimizer_choices)
    print(f"review 11/5 instance: N_opt = {N} (breakpoints {[str(b) for b in bps]}), R_min T = {T}, "
          f"worst over ties {Tw}, splits {[str(s) for s in splits]}")
    assert N == 3 and T == 11


if __name__ == "__main__":
    main()
