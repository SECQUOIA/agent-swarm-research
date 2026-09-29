"""Independent exact check of Theorem 3's two instances (alpha = 1, [0,1]).

Rebuilds H_A, H_B from the lines as written in the note (not from lb_pair.py),
and checks in exact rationals:
  1. min m = eps, attained only at y = 0 and y = 1 (so f* = 0 in both);
  2. root relaxation min(H - y): value -37/300, unique minimizer 3/5, in both;
  3. H_A = H_B on [0, 30eps/13], [1/60, 27/40], [1-3eps, 1], and these are the
     maximal intervals of agreement around 0, 3/5 and 1;
  4. [0,b] valid iff b <= s*, [c,1] valid iff c >= s*, with s* = 1/3 (A) and
     3/5 (B), via exact maximal-valid-interval computations; N_opt = 2 and
     the 2-piece certificate is unique;
  5. the tight-chord segments claimed in the proof.
"""
from fractions import Fraction as Fr

from exact1d import Inst

eps = Fr(1, 10000)
h1 = Fr(143, 300)


def chord(a, b):
    return (a + b, -a * b)


gm = (Fr(4, 5), h1 - Fr(4, 5) * Fr(3, 5))
gp = (Fr(6, 5), h1 - Fr(6, 5) * Fr(3, 5))
e0 = (Fr(1, 6), eps)
e1 = (Fr(5, 3), -Fr(2, 3) + eps)
LA = [chord(Fr(0), Fr(1, 3)), chord(Fr(1, 3), Fr(1)), gm, gp, e0, e1]
LB = [chord(Fr(0), Fr(3, 5)), chord(Fr(3, 5), Fr(1)), gm, gp, e0, e1]


def env(lines):
    H = lambda y: max(s * y + b for s, b in lines)
    xs = {Fr(0), Fr(1)}
    for i, (s1, b1) in enumerate(lines):
        for s2, b2 in lines[i + 1:]:
            if s1 != s2:
                x = (b2 - b1) / (s1 - s2)
                if 0 < x < 1 and s1 * x + b1 == H(x):
                    xs.add(x)
    xs = sorted(xs)
    return xs, H


def active_on(lines, line, a, b):
    """is `line` the maximum on all of [a,b]? (PL convex: check endpoints)"""
    H = lambda y: max(s * y + c for s, c in lines)
    return all(line[0] * y + line[1] == H(y) for y in (a, b))


def main():
    res = {}
    for name, lines, sstar in (("A", LA, Fr(1, 3)), ("B", LB, Fr(3, 5))):
        xs, H = env(lines)
        I = Inst(xs, [H(x) - x * x for x in xs])
        ms = I.m
        mmin = min(ms)
        argm = [x for x, m in zip(xs, ms) if m == mmin]
        assert mmin == eps and argm == [0, 1], (name, mmin, argm)
        assert I.convex()
        vals = [H(x) - x for x in xs]
        v = min(vals)
        arg = [x for x, w in zip(xs, vals) if w == v]
        assert v == Fr(-37, 300) and arg == [Fr(3, 5)], (name, v, arg)
        b0 = I.bmax(Fr(0))
        a1 = I.amin(Fr(1))
        assert b0 == sstar and a1 == sstar, (name, b0, a1)
        N = len(I.greedy()) - 1
        assert N == 2
        print(f"{name}: knots {[str(x) for x in xs]}")
        print(f"   min m = {mmin} at {[str(a) for a in argm]}; root LB (m-q) = {v}, unique minimizer {arg[0]}; "
              f"max valid [0,b]: b = {b0}; min valid [c,1]: c = {a1}; N_opt = {N} (unique breakpoint {sstar})")
        res[name] = (xs, H)
    (xa, HA), (xb, HB) = res["A"], res["B"]
    kn = sorted(set(xa) | set(xb))
    # agreement intervals: maximal runs of consecutive knots (of the union) where HA == HB,
    # and on which neither function has a knot where the other differs (PL: equality at
    # consecutive union knots implies equality between them)
    eq = [HA(x) == HB(x) for x in kn]
    runs, start = [], None
    for x, e in zip(kn, eq):
        if e and start is None:
            start = x
        if e:
            last = x
        if not e and start is not None:
            runs.append((start, last)); start = None
    if start is not None:
        runs.append((start, last))
    print("maximal intervals where H_A = H_B (between union knots):", [(str(a), str(b)) for a, b in runs])
    claimed = [(Fr(0), 30 * eps / 13), (Fr(1, 60), Fr(27, 40)), (1 - 3 * eps, Fr(1))]
    for a, b in claimed:
        assert any(r0 <= a and b <= r1 for r0, r1 in runs), (a, b)
    print("claimed agreement sets", [(str(a), str(b)) for a, b in claimed], "are contained in them")
    # tight chord segments
    assert active_on(LA, chord(Fr(0), Fr(1, 3)), 6 * eps, Fr(1, 140))
    assert active_on(LA, chord(Fr(1, 3), Fr(1)), Fr(27, 40), 1 - 3 * eps)
    assert active_on(LB, chord(Fr(0), Fr(3, 5)), 30 * eps / 13, Fr(1, 60))
    assert active_on(LB, chord(Fr(3, 5), Fr(1)), Fr(107, 120), 1 - 15 * eps)
    print("tight chord segments of step 4 confirmed")
    # the minimizer 3/5 is interior to the agreement interval; any root split sigma
    for sigma in (Fr(1, 3), Fr(3, 5), Fr(1, 2), Fr(1, 60), Fr(9, 10)):
        IA = Inst(xa, [HA(x) - x * x for x in xa]); IB = Inst(xb, [HB(x) - x * x for x in xb])
        badA = not (IA.valid(Fr(0), sigma) and IA.valid(sigma, Fr(1)))
        badB = not (IB.valid(Fr(0), sigma) and IB.valid(sigma, Fr(1)))
        assert badA or badB
        print(f"   root split {sigma}: A has invalid child {badA}, B has invalid child {badB}")
    print("all Theorem 3 checks passed")


if __name__ == "__main__":
    main()
