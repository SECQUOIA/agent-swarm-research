"""Recheck of Proposition 4' (SCIP 10's default branching point) in exact rationals.

Written for this recheck.  The rule is transcribed from SCIPbranchGetBranchingPoint in
SCIP v10.0.2 src/scip/branch.c (lines 2393-2519 of scip-src/v10.0.2_branch.c), called by
cons_nonlinear with suggestion = SCIP_INVALID (cons_nonlinear.c line 7478):

    mp  = midpull (0.75);  rel = (ub - lb) / (gub - glb)   [global bounds]
    if rel < midpullreldomtrig (0.5): mp *= rel
    bp  = mp * (lb + ub)/2 + (1 - mp) * lpval ;  bp = clip(bp, lb, ub)
    bp  = clip(bp, (1-c) lb + c ub, c lb + (1-c) ub)      [c = clamp = 0.2, LOCAL bounds]

The absolute epsilon guards (1.01*epsilon*scale; midpoint if reldiff <= 2.02*epsilon) are
omitted in the exact model; `guard_width` reports where they would start to matter.

Instance: f(y) = 2 alpha |y - a| on [0, 1], a = 3/238, exact gap alpha*q_B, incumbent f* = 0.
Nothing about minimizers or pruning is assumed: every node's relaxation is minimized exactly
(phi_B is convex piecewise quadratic, candidates = ends, kink, stationary points) and every node
of the tree is simulated.
Usage: python3 scip_prop4prime.py
"""
from fractions import Fraction as Fr
import math

A = Fr(3, 238)


def relax(l, u, a, alpha, eps):
    """min over [l,u] of phi(y) = eps + 2 alpha |y-a| - alpha (y-l)(u-y); returns (min, argmins)."""
    def phi(y):
        return eps + 2 * alpha * abs(y - a) - alpha * (y - l) * (u - y)
    cands = {l, u}
    if l < a < u:
        cands.add(a)
    for s in (1, -1):               # piece where sign(y - a) = s: stationary at (l+u)/2 - s
        y = (l + u) / 2 - s
        if l <= y <= u and (y - a) * s >= 0:
            cands.add(y)
    vals = {y: phi(y) for y in cands}
    mn = min(vals.values())
    return mn, sorted(y for y, v in vals.items() if v == mn)


def scip_point(l, u, y, glb=Fr(0), gub=Fr(1), midpull=Fr(3, 4), trig=Fr(1, 2), clamp=Fr(1, 5)):
    mp = midpull
    rel = (u - l) / (gub - glb)
    if rel < trig:
        mp *= rel
    bp = mp * (l + u) / 2 + (1 - mp) * y
    bp = max(l, min(bp, u))
    unclamped = bp
    lo = (1 - clamp) * l + clamp * u
    hi = clamp * l + (1 - clamp) * u
    bp = max(lo, min(bp, hi))
    return bp, unclamped, mp


def run(rule, a, alpha, eps, trace=False, cap=10 ** 6):
    """Full tree. rule in {'scip', 'noclamp', 'min'}. Returns (T, chain records)."""
    T, stack, chain = 0, [(Fr(0), Fr(1))], []
    while stack:
        l, u = stack.pop()
        T += 1
        assert T < cap
        mn, argm = relax(l, u, a, alpha, eps)
        if mn >= 0:
            continue
        assert len(argm) == 1, "non-unique minimizer"
        y = argm[0]
        assert l < a < u and y == a, "an invalid node without the kink inside, or minimizer != kink"
        if rule == "min":
            s, unc, mp = y, y, Fr(0)
        elif rule == "scip":
            s, unc, mp = scip_point(l, u, y)
        else:
            s, unc, mp = scip_point(l, u, y, clamp=Fr(0))
        assert l < s < u
        if trace:
            chain.append(dict(l=l, u=u, w=u - l, pos=(a - l) / (u - l), mp=mp,
                              unclamped=unc, split=s, clamped=(s != unc)))
        stack += [(l, s), (s, u)]
    return T, chain


def K_formula(alpha, eps):
    c = alpha * Fr(5, 36) * Fr(9, 119) ** 2
    assert eps < c
    k = 2
    while c / Fr(25) ** (k - 2) > eps:
        k += 1
    return k                         # = 2 + #{k >= 2 : c 25^-(k-2) > eps}


def main():
    print("== Prop 4' chain, a = 3/238, alpha = 1, eps = 1e-16 (exact, full tree)")
    alpha, eps = Fr(1), Fr(1, 10 ** 16)
    T, ch = run("scip", A, alpha, eps, trace=True)
    for i, r in enumerate(ch[:6]):
        print(f"  N_{i}: [{r['l']}, {r['u']}] w={float(r['w']):.6g} pos(a)={r['pos']} mu={r['mp']} "
              f"unclamped={r['unclamped']} (~{float(r['unclamped']):.5f}) split={r['split']} clamped={r['clamped']}")
    # the stated facts
    assert ch[0]["split"] == Fr(45, 119) and not ch[0]["clamped"] and ch[0]["mp"] == Fr(3, 4)
    assert ch[1]["l"] == 0 and ch[1]["u"] == Fr(45, 119) and ch[1]["pos"] == Fr(1, 30)
    assert ch[1]["mp"] == Fr(135, 476) and ch[1]["unclamped"] == A * (1 + 14 * Fr(135, 476))
    assert ch[1]["clamped"] and ch[1]["split"] == Fr(9, 119)
    assert (ch[2]["l"], ch[2]["u"], ch[2]["pos"]) == (0, Fr(9, 119), Fr(1, 6))
    for i in range(2, len(ch)):
        r = ch[i]
        assert r["pos"] == (Fr(1, 6) if i % 2 == 0 else Fr(5, 6))
        assert r["w"] == Fr(9, 119) / 5 ** (i - 2)
        assert r["mp"] < Fr(1, 10) and r["mp"] <= Fr(27, 476)
        assert r["clamped"]
        exp_unc = r["l"] + r["w"] * (r["pos"] + r["mp"] * (Fr(1, 2) - r["pos"]))
        assert r["unclamped"] == exp_unc
    print(f"  chain length {len(ch)}: positions alternate 1/6, 5/6 from N_2; widths (9/119) 5^-(k-2);"
          f" clamp binds at every level from N_1; max mu from N_2 = {max(r['mp'] for r in ch[2:])} (< 1/10)")

    print("== node counts (full exact trees) vs 2K+1 and R_min")
    for alpha in (Fr(1), Fr(7, 3)):
        for k in (4, 6, 8, 12, 16, 24, 32):
            eps = alpha * Fr(1, 10 ** k)
            Ts = {r: run(r, A, alpha, eps)[0] for r in ("scip", "noclamp", "min")}
            K = K_formula(alpha, eps)
            print(f"  alpha={alpha} eps=alpha*1e-{k}: T_scip={Ts['scip']} (2K+1={2*K+1}) "
                  f"T_noclamp={Ts['noclamp']} T_min={Ts['min']}")
            assert Ts["min"] == 3 and Ts["scip"] >= 2 * K + 1
            assert Ts["scip"] == 2 * K + 1            # off-chain children are all pruned
    print("== N_opt = 2: [0,a] and [a,1] valid, root invalid (exact, eps = 1e-8)")
    eps = Fr(1, 10 ** 8)
    assert relax(Fr(0), A, A, Fr(1), eps)[0] >= 0 and relax(A, Fr(1), A, Fr(1), eps)[0] >= 0
    assert relax(Fr(0), Fr(1), A, Fr(1), eps)[0] < 0
    print("  ok")
    print("== eps bound: N_0, N_1 invalid whenever eps < (5/36)(9/119)^2")
    c = Fr(5, 36) * Fr(9, 119) ** 2
    print(f"  a(1-a) = {float(A*(1-A)):.6g}, a(45/119-a) = {float(A*(Fr(45,119)-A)):.6g}, (5/36)(9/119)^2 = {float(c):.6g}")
    assert A * (1 - A) > c and A * (Fr(45, 119) - A) > c

    print("== no-clamp growth per doubling of log(1/eps)")
    Tn = {k: run("noclamp", A, Fr(1), Fr(1, 10 ** k))[0] for k in (8, 12, 16, 24, 32, 48, 64)}
    print("  ", Tn)
    for k in (8, 12, 16):
        if 2 * k in Tn:
            print(f"   eps 1e-{k} -> 1e-{2*k}: T {Tn[k]} -> {Tn[2*k]} (+{Tn[2*k]-Tn[k]})")

    print("== where SCIP's absolute epsilon guard (1.01e-9 * max(|lb|,|ub|,1)) would exceed the 0.2 clamp")
    w_guard = Fr(101, 100) * Fr(1, 10 ** 9) / Fr(1, 5)
    k = 2
    while Fr(9, 119) / 5 ** (k - 2) >= w_guard:
        k += 1
    wk = Fr(9, 119) / 5 ** (k - 2)
    print(f"  first chain node with w < {float(w_guard):.3g}: N_{k}, w = {float(wk):.3g}; it is invalid only if "
          f"eps < alpha*(5/36) w^2 = alpha*{float(Fr(5,36)*wk*wk):.3g}")


if __name__ == "__main__":
    main()
