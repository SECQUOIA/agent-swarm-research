"""Independent recomputation of the optcdeg2 quadratic-calibration lower bound (reviewer code).

Certificate data (any values give a valid bound): py_t, pv_t, q_t, c_t (t = 1..N) from
theory-bangbang/logs/optcdeg2_qcal_data.npz, used as exact rationals; S_t(y, v) = py y + pv v
+ (q/2)(v - c)^2. Model constants are the exact OSIL decimals (checked by v_model.py):
  h = 4e-4 (coefficient of v in Y-rows and of u in V-rows), a = 8e-6, b = 8e-5, w = 2e-4 (objective),
  U = [-1/5, 1/5] exactly, V_t = reviewer enclosures (v_states.py), y free, y_0 = 10, v_0 = 0, v_N = 0.

Bound:  f* >= min_{u in U} [w*100 + S_1(10, h u - 10 a)] + sum_{t=1}^{N-1} inf_{R x V_t x U} rho_t
               + inf_y [w y^2 - S_N(y, 0)],
  rho_t(y, v, u) = w y^2 + S_{t+1}(y + h v, v + h u - a y - b v^2) - S_t(y, v).

All arithmetic is exact (Fractions). Per stage:
 * y is eliminated exactly: rho_t = A2 y^2 + (B0 - Q1 a e) y + const, A2 = w + Q1 a^2/2 > 0 (checked),
   with e = g(v) + h u - c_{t+1}, g(v) = v - b v^2. The reduced residual is
   G(v, e) = F(v) + K2 e^2 + K1' e (derived by hand; spot-checked against the definition).
 * u enters only through e (affine, e in [e_-(v), e_+(v)]). Hence, exactly,
     inf_{v,u} = min( inf_V G(v, e_-(v)), inf_V G(v, e_+(v)), [K2 > 0] inf_{R*} G*(v) ),
   G* = F - K1'^2/(4 K2), R* = {v in V : e_-(v) <= -K1'/(2K2) <= e_+(v)} (an enclosure is used).
 * Each univariate polynomial (degree <= 4) is minimized over an interval rigorously: endpoints
   plus local minima of G, which are isolated with an exact Sturm sequence of G' and bracketed by
   exact sign changes; on a bracket of width w, G >= G(l) - M2 w^2 with M2 >= max|G''|.
Stage minima are rounded down to the grid 2^-200 and summed exactly.
"""
import json
import math
import sys
import time
from fractions import Fraction as Fr

import numpy as np

import os as _os  # repository root, from this file's location (no absolute paths)
_REPO = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../.."))
TB = _REPO + "/research-20260929/theory-bangbang/"
N = 50000
H = Fr(4, 10000)
AY = Fr(8, 10 ** 6)
BV = Fr(8, 10 ** 5)
W = Fr(2, 10 ** 4)
UL, UH = Fr(-1, 5), Fr(1, 5)
GRID = 1 << 200


# ----------------------------------------------------------------------------- exact polynomials
def trim(p):
    p = list(p)
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    n = max(len(p), len(q))
    return trim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def pscale(p, s):
    return trim([s * c for c in p])


def pmul(p, q):
    r = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        if a:
            for j, b in enumerate(q):
                r[i + j] += a * b
    return trim(r)


def peval(p, x):
    s = Fr(0)
    for c in reversed(p):
        s = s * x + c
    return s


def pder(p):
    return trim([i * p[i] for i in range(1, len(p))]) if len(p) > 1 else [Fr(0)]


def prem(a, b):
    a = list(a)
    db = len(b) - 1
    lb = b[-1]
    while len(a) - 1 >= db and any(a):
        if a[-1] == 0:
            a.pop(); continue
        f = a[-1] / lb
        k = len(a) - 1 - db
        for i in range(len(b)):
            a[k + i] -= f * b[i]
        a.pop()
    return trim(a) if a else [Fr(0)]


def sgn(x):
    return (x > 0) - (x < 0)


def sturm(p):
    s = [p, pder(p)]
    while len(s[-1]) > 1:
        r = prem(s[-2], s[-1])
        if len(r) == 1 and r[0] == 0:
            break
        s.append([-c for c in r])
    return s


def variations(seq, x):
    sg = [sgn(peval(q, x)) for q in seq]
    sg = [z for z in sg if z != 0]
    return sum(1 for i in range(len(sg) - 1) if sg[i] != sg[i + 1])


STATS = dict(quartic_calls=0, sturm_bisections=0, seeded_brackets=0, bisection_brackets=0,
             even_roots=0, max_bracket_slack=0.0)


def min_poly(G, a, b):
    """exact-arithmetic rigorous lower bound of min_{a<=x<=b} G(x); returns (lb, argmin-ish)."""
    assert a <= b
    G = trim(G)
    cands = [(peval(G, a), a), (peval(G, b), b)]
    deg = len(G) - 1
    if deg <= 1 or a == b:
        return min(cands)
    if deg == 2:
        if G[2] > 0:
            x = -G[1] / (2 * G[2])
            if a < x < b:
                cands.append((peval(G, x), x))
        return min(cands)
    STATS["quartic_calls"] += 1
    P = pder(G)
    P2 = pder(P)
    assert peval(P, a) != 0 and peval(P, b) != 0, "critical point at an endpoint (not handled)"
    S = sturm(P)
    stack = [(a, b, variations(S, a) - variations(S, b))]
    iso = []
    guard = 0
    while stack:
        l, r, k = stack.pop()
        if k == 0:
            continue
        if k == 1:
            iso.append((l, r)); continue
        guard += 1; assert guard < 2000
        STATS["sturm_bisections"] += 1
        mid = (l + r) / 2
        if peval(P, mid) == 0:
            mid = l + (r - l) / 3
            assert peval(P, mid) != 0
        vm = variations(S, mid)
        stack.append((l, mid, variations(S, l) - vm))
        stack.append((mid, r, vm - variations(S, r)))
    seeds = None
    for l, r in iso:
        sl, sr = sgn(peval(P, l)), sgn(peval(P, r))
        if sl == sr:
            STATS["even_roots"] += 1
            continue
        if sl > 0:          # local maximum of G
            continue
        if seeds is None:
            fc = [float(c) for c in reversed(P)]
            seeds = [z.real for z in np.roots(fc) if abs(z.imag) <= 1e-9 * (1 + abs(z))]
        br = None
        for s in seeds:
            fs = Fr(s)
            if not (l < fs < r):
                continue
            dl = Fr(1e-13) * (1 + abs(fs))
            ll, rr = max(l, fs - dl), min(r, fs + dl)
            if peval(P, ll) < 0 < peval(P, rr):
                br = (ll, rr); STATS["seeded_brackets"] += 1
                break
        if br is None:
            ll, rr = l, r
            while rr - ll > Fr(1, 1 << 60):
                mid = (ll + rr) / 2
                pm = peval(P, mid)
                if pm == 0:
                    ll = rr = mid; break
                if pm < 0:
                    ll = mid
                else:
                    rr = mid
            br = (ll, rr); STATS["bisection_brackets"] += 1
        ll, rr = br
        R = max(abs(ll), abs(rr))
        M2 = sum(abs(c) * R ** i for i, c in enumerate(P2))
        slack = M2 * (rr - ll) ** 2
        STATS["max_bracket_slack"] = max(STATS["max_bracket_slack"], float(slack))
        cands.append((min(peval(G, ll), peval(G, rr)) - slack, ll))
    return min(cands)


# ----------------------------------------------------------------------------- g^{-1} enclosures
def g(v):
    return v - BV * v * v


def ginv_dn(w):
    """rational x <= g^{-1}(w) on the branch v < 6250: one exact Newton step (g concave => below root)."""
    wf = float(w)
    x = Fr(2 * wf / (1 + math.sqrt(1 - 4 * float(BV) * wf)))
    x = x - (g(x) - w) / (1 - 2 * BV * x)
    assert g(x) <= w and x < 6000
    return x


def ginv_up(w):
    x = ginv_dn(w)
    d = Fr(1, 1 << 80)
    while g(x) < w:
        x += d; d *= 2
    return x


# ----------------------------------------------------------------------------- stage computations
def stage(t, D, Vb, check=False):
    P0y, P0v, Q0, C0 = (Fr(float(D[k][t])) for k in ("py", "pv", "q", "c"))
    P1y, P1v, Q1, C1 = (Fr(float(D[k][t + 1])) for k in ("py", "pv", "q", "c"))
    vs, us = Fr(float(D["v"][t])), Fr(float(D["u"][t]))
    A2 = W + Q1 * AY * AY / 2
    assert A2 > 0
    B0 = P1y - P0y - AY * P1v
    K2 = Q1 * W / (2 * A2)
    K1p = P1v + B0 * Q1 * AY / (2 * A2)
    K0 = -B0 * B0 / (4 * A2)
    vp = [vs, Fr(1)]                                   # v = vs + d
    F = padd(padd(pscale(vp, P1y * H - P0v), [P1v * C1 + K0]),
             pscale(pmul(padd(vp, [-C0]), padd(vp, [-C0])), -Q0 / 2))
    gp = padd(vp, pscale(pmul(vp, vp), -BV))

    def Gu(u):
        e = padd(gp, [H * u - C1])
        return padd(F, padd(pscale(pmul(e, e), K2), pscale(e, K1p)))

    vlo, vhi = Fr(float(Vb[t, 0])), Fr(float(Vb[t, 1]))
    a, b = vlo - vs, vhi - vs
    Gm, Gp = Gu(UL), Gu(UH)
    cands = [min_poly(Gm, a, b), min_poly(Gp, a, b)]
    star = None
    if K2 > 0:
        es = -K1p / (2 * K2)
        w1, w2 = es + C1 - H * UH, es + C1 - H * UL      # need g(v) in [w1, w2]
        if not (g(vhi) < w1 or g(vlo) > w2):
            lo = vlo if g(vlo) >= w1 else ginv_dn(w1)
            hi = vhi if g(vhi) <= w2 else ginv_up(w2)
            lo, hi = max(lo, vlo), min(hi, vhi)
            if lo <= hi:
                Gs = padd(F, [-K1p * K1p / (4 * K2)])
                star = min_poly(Gs, lo - vs, hi - vs)
                cands.append(star)
    m = min(cands)[0]
    # value of the reduced residual at the stored trajectory point (d = 0, u = u_t)
    e0 = g(vs) + H * us - C1
    c00 = peval(F, Fr(0)) + K2 * e0 * e0 + K1p * e0
    if check:   # spot-check the y-elimination against the definition, exactly
        for (v, u) in ((vs, us), (vs + (b - a) / 3 + a, UL), (vhi, UH)):
            e = g(v) + H * u - C1
            ystar = -(B0 - Q1 * AY * e) / (2 * A2)

            def rho(y):
                y1, v1 = y + H * v, v + H * u - AY * y - BV * v * v
                S1 = P1y * y1 + P1v * v1 + Q1 / 2 * (v1 - C1) ** 2
                S0 = P0y * y + P0v * v + Q0 / 2 * (v - C0) ** 2
                return W * y * y + S1 - S0
            Gv = peval(Gu(u), v - vs) if u in (UL, UH) else None
            red = peval(F, v - vs) + K2 * e * e + K1p * e
            assert rho(ystar) == red, ("y-elimination mismatch", t)
            assert Gv is None or Gv == red
            assert rho(ystar + 1) > red and rho(ystar - 1) > red
    return m, c00, (star is not None), float(K2)


def stage0(D):
    P1y, P1v, Q1, C1 = (Fr(float(D[k][1])) for k in ("py", "pv", "q", "c"))
    # y_1 = 10 + h*0 = 10, v_1 = 0 + h u - a*10 - b*0
    val = lambda u: W * 100 + P1y * 10 + P1v * (H * u - AY * 10) + Q1 / 2 * (H * u - AY * 10 - C1) ** 2  # noqa
    c2 = Q1 / 2 * H * H
    c1 = P1v * H + Q1 * (-AY * 10 - C1) * H
    cands = [val(UL), val(UH)]
    if c2 > 0 and UL < -c1 / (2 * c2) < UH:
        cands.append(val(-c1 / (2 * c2)))
    return min(cands), val(Fr(float(D["u"][0])))


def terminal(D):
    PNy, PNv, QN, CN = (Fr(float(D[k][N])) for k in ("py", "pv", "q", "c"))
    # inf_y  w y^2 - (PNy y + PNv*0 + QN/2 (0 - CN)^2)
    return -PNy * PNy / (4 * W) - QN / 2 * CN * CN


def main():
    t0 = time.time()
    D = dict(np.load(TB + "logs/optcdeg2_qcal_data.npz"))
    Vb = np.load("logs/vt_reviewer.npy")
    lb_auth = np.load(TB + "logs/optcdeg2_qcal_stage_lb.npy")          # LB[t-1], t = 1..N-1
    ts = range(1, N) if len(sys.argv) < 2 else range(int(sys.argv[1]), int(sys.argv[2]))
    s0, s0_traj = stage0(D)
    te = terminal(D)
    total_int = (s0.numerator * GRID) // s0.denominator + (te.numerator * GRID) // te.denominator
    loss_int = 0
    worst = (-1.0, None); worst_auth = (-math.inf, None); n_star = 0; n_auth_viol = 0
    head = mid = tail = 0.0
    s1 = int(np.where(np.abs(np.abs(D["u"]) - 0.2) > 1e-12)[0][0])
    s2 = int(np.where(np.abs(np.abs(D["u"]) - 0.2) > 1e-12)[0][1])
    per = np.empty(N + 1)
    for t in ts:
        chk = (t % 500 == 0) or abs(t - s1) <= 3 or abs(t - s2) <= 3 or t in (1, N - 1)
        m, c00, st, K2 = stage(t, D, Vb, check=chk)
        n_star += st
        mi = (m.numerator * GRID) // m.denominator
        total_int += mi
        loss = c00 - m
        loss_int += ((loss.numerator * GRID) // loss.denominator)
        lf = float(loss); per[t] = float(m)
        if t <= s1:
            head += lf
        elif t <= s2:
            mid += lf
        else:
            tail += lf
        if lf > worst[0]:
            worst = (lf, t)
        excess = Fr(float(lb_auth[t - 1])) - m          # > 0 would mean the author's stage bound is invalid
        if excess > 0:
            n_auth_viol += 1
        if float(excess) > worst_auth[0]:
            worst_auth = (float(excess), t)
        if t % 5000 == 0:
            print(json.dumps(dict(t=t, sec=round(time.time() - t0, 1), **STATS)), flush=True)
    total = Fr(total_int, GRID)
    rec = dict(stages=[ts.start, ts.stop], stage0=float(s0), stage0_at_traj=float(s0_traj), terminal=float(te),
               bound=float(total), bound_str=str(total.numerator * 10 ** 20 // total.denominator),
               bound_rounded_down_double=math.nextafter(float(total), -math.inf) if Fr(float(total)) > total else float(total),
               loss_total=float(Fr(loss_int, GRID)), loss_head=head, loss_mid=mid, loss_tail=tail,
               worst_stage=worst[1], worst_loss=worst[0], stages_with_interior_u_piece=n_star,
               author_stage_lb_minus_exact_min_max=worst_auth[0], at=worst_auth[1],
               author_stages_above_exact_min=n_auth_viol, seconds=time.time() - t0, **STATS)
    print(json.dumps(rec, indent=1), flush=True)
    tag = "" if len(sys.argv) < 2 else f"_{sys.argv[1]}_{sys.argv[2]}"
    json.dump(rec, open(f"logs/qcal_exact{tag}.json", "w"), indent=1)
    np.save(f"logs/qcal_exact_stage_min{tag}.npy", per)


if __name__ == "__main__":
    main()
