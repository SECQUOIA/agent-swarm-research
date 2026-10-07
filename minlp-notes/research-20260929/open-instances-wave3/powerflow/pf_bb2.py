"""Spatial branch and bound with SDP-Lagrangian node bounds and envelope cuts for the
power-flow relaxation R (pf_model; angle rows dropped, they are replaced by cones).

Node data
  vbox[k] = (l_k, u_k) rational bounds on |V_k| (rows l_k^2 <= e_k^2 + f_k^2 <= u_k^2);
  cone[(p,q)] = directions d1, d2 (exact rationals) bounding the angle of W_pq = V_p conj(V_q):
      angle >= dir(d1):  s1 w_R - c1 w_I <= 0 ;  angle <= dir(d2):  c2 w_I - s2 w_R <= 0.
Envelope cut for a pair with a cone narrower than pi and a direction u = (c, s) inside it:
  every rank-one point satisfies  c w_R + s w_I = |W_pq| |u| cos(angle - angle(u))
      >= kappa |W_pq|,   kappa <= |u| cos(h'),  h' = max angular distance of u to the cone ends,
  and |W_pq| = sqrt(W_pp W_qq) >= P(W_pp, W_qq) for any affine P lying below the concave
  function sqrt(a b) at the four corners of [l_p^2, u_p^2] x [l_q^2, u_q^2] (concavity).
  Row:  kappa P(W_pp, W_qq) - (c w_R + s w_I) <= 0.
Children partition the parent: magnitude splits at a rational m (|V| <= m / |V| >= m), angle
splits along one exact rational direction (complementary halfplanes).
Node bound = rigorous pf_cert certificate for R + node rows (valid for the node's region;
children inherit max(parent, own) bounds).

    python3 pf_bb2.py <name> <time_limit_s> <UB>
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import heapq
import math
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp
import numpy as np

import pf_cert as pc
import pf_model as pm
import pf_sdp as ps
from pf_bb import half_row, wRI


def vrow(k, lo2, hi2, name):
    Q = {(2 * k, 2 * k): Fr(1), (2 * k + 1, 2 * k + 1): Fr(1)}
    return dict(name=name, lin={}, Q=Q, qy={}, lb=lo2, ub=hi2, kind="volt")


def ang(d):
    with mp.workdps(40):
        return mp.atan2(mp.mpf(d[1].numerator) / d[1].denominator, mp.mpf(d[0].numerator) / d[0].denominator)


def rat_unit(phi):
    return (Fr(math.cos(phi)).limit_denominator(10**9), Fr(math.sin(phi)).limit_denominator(10**9))


def envelope_plane(lp, up_, lq, uq):
    """affine P(a,b) = al*a + be*b + ga below sqrt(ab) at the 4 corners (exact rationals);
    returns the plane through three corners that is valid at the fourth (best of 4 choices)."""
    A = [lp * lp, up_ * up_]
    B = [lq * lq, uq * uq]
    pts = [(A[i], B[j], [lp, up_][i] * [lq, uq][j]) for i in range(2) for j in range(2)]  # exact sqrt values
    best = None
    for drop in range(4):
        tri = [pts[k] for k in range(4) if k != drop]
        (a1, b1, g1), (a2, b2, g2), (a3, b3, g3) = tri
        M = [[a1, b1, 1], [a2, b2, 1], [a3, b3, 1]]
        det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
               + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
        if det == 0:
            continue
        # Cramer
        def sub(col, vals):
            Mm = [row[:] for row in M]
            for r in range(3):
                Mm[r][col] = vals[r]
            return (Mm[0][0] * (Mm[1][1] * Mm[2][2] - Mm[1][2] * Mm[2][1]) - Mm[0][1] * (Mm[1][0] * Mm[2][2] - Mm[1][2] * Mm[2][0])
                    + Mm[0][2] * (Mm[1][0] * Mm[2][1] - Mm[1][1] * Mm[2][0]))
        g = [g1, g2, g3]
        al, be, ga = sub(0, g) / det, sub(1, g) / det, sub(2, g) / det
        a4, b4, g4 = pts[drop]
        if al * a4 + be * b4 + ga <= g4:
            # score: value at the center
            ac, bc = (A[0] + A[1]) / 2, (B[0] + B[1]) / 2
            val = al * ac + be * bc + ga
            if best is None or val > best[0]:
                best = (val, al, be, ga)
    return best[1:]


def cone_kappa(d1, d2, u):
    """rational kappa <= |u| cos(h'), h' = max angle distance from u to d1, d2 (all in the cone)."""
    with mp.workdps(40):
        a1, a2, au = ang(d1), ang(d2), ang(u)
        # unwrap into [a1, a1 + 2 pi)
        def unwrap(x):
            while x < a1:
                x += 2 * mp.pi
            return x
        a2u, auu = unwrap(a2), unwrap(au)
        assert a2u - a1 < mp.pi and a1 <= auu <= a2u
        h = max(auu - a1, a2u - auu)
        nu = mp.sqrt((mp.mpf(u[0].numerator) / u[0].denominator) ** 2 + (mp.mpf(u[1].numerator) / u[1].denominator) ** 2)
        k = nu * mp.cos(h) * (1 - mp.mpf(10) ** -25)
        q = Fr(mp.nstr(k, 30))
        return q if q > 0 else Fr(0)


def node_rows(node):
    rows = []
    for k, (l, u) in node["vbox"].items():
        rows.append(vrow(k, l * l, u * u, f"VB{k}"))
    for (p, q), (d1, d2) in node["cone"].items():
        if d1 is not None:
            c1, s1 = d1
            rows.append(half_row(p, q, s1, -c1, f"C{p}_{q}lo"))
        if d2 is not None:
            c2, s2 = d2
            rows.append(half_row(p, q, -s2, c2, f"C{p}_{q}hi"))
        if d1 is not None and d2 is not None:
            # direction inside the cone: normalized bisector (rational approximation)
            with mp.workdps(30):
                a1 = ang(d1); a2 = ang(d2)
                while a2 < a1:
                    a2 += 2 * mp.pi
                if a2 - a1 >= mp.pi:
                    continue
                mid = float((a1 + a2) / 2)
            u = rat_unit(mid)
            kap = cone_kappa(d1, d2, u)
            if kap <= 0:
                continue
            lp, up_ = node["vbox"].get(p, node["vdef"][p])
            lq, uq = node["vbox"].get(q, node["vdef"][q])
            al, be, ga = envelope_plane(lp, up_, lq, uq)
            WR, WI = wRI(p, q)
            Q = {}
            for kk, v in WR.items():
                Q[kk] = Q.get(kk, 0) - u[0] * v
            for kk, v in WI.items():
                Q[kk] = Q.get(kk, 0) - u[1] * v
            Q[(2 * p, 2 * p)] = Q.get((2 * p, 2 * p), 0) + kap * al
            Q[(2 * p + 1, 2 * p + 1)] = Q.get((2 * p + 1, 2 * p + 1), 0) + kap * al
            Q[(2 * q, 2 * q)] = Q.get((2 * q, 2 * q), 0) + kap * be
            Q[(2 * q + 1, 2 * q + 1)] = Q.get((2 * q + 1, 2 * q + 1), 0) + kap * be
            Q = {kk: v for kk, v in Q.items() if v != 0}
            rows.append(dict(name=f"E{p}_{q}", lin={}, Q=Q, qy={}, lb=None, ub=-kap * ga, kind="cut"))
    return rows


def recover_primal(M0, W, log=print):
    """rank-one extraction V = sqrt(lambda_max) v_max from W; build the full OSIL point (polar or
    rectangular), evaluate it at 50 digits.  Returns (objective, max row viol, max bound viol, x)."""
    sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
    import ev
    n = M0["n"]
    Wc = np.zeros((n, n), complex)
    for a in range(n):
        for b in range(n):
            Wc[a, b] = (W[2 * a, 2 * b] + W[2 * a + 1, 2 * b + 1]) + 1j * (W[2 * a + 1, 2 * b] - W[2 * a, 2 * b + 1])
    w, V = np.linalg.eigh(Wc)
    v = V[:, -1] * np.sqrt(max(w[-1], 0))
    # rotate so that bus 0 has zero angle
    v = v * np.exp(-1j * np.angle(v[0]))
    I = M0["I"]
    names = I["names"]
    with mp.workdps(50):
        x = [None] * len(names)
        if M0["polar"]:
            for k, (vv, tt) in enumerate(M0["busmap"]):
                x[vv] = mp.mpf(abs(v[k])); x[tt] = mp.mpf(float(np.angle(v[k])))
        else:
            xset = {}
            for r in M0["rows"]:
                pass
            # rectangular: variables e,f are the voltage-row pairs (same order as pf_model)
            keys = []
            for c in I["cons"]:
                if c["quad"] and not c["lin"] and all(a == b for a, b, _ in c["quad"]):
                    keys.append(tuple(sorted(a for a, b, _ in c["quad"])))
            keys = sorted(set(k for k in keys if len(k) == 2))
            eq_quad = set()
            for c in I["cons"]:
                if c["quad"] and c["lb"] == c["ub"]:
                    for a, b, _ in c["quad"]:
                        eq_quad |= {a, b}
            keys = [k for k in keys if set(k) <= eq_quad]
            for k, (a, b) in enumerate(keys):
                x[a] = mp.mpf(float(v[k].real)); x[b] = mp.mpf(float(v[k].imag))
        # remaining variables by forward propagation of equality rows with one unknown (linear in it)
        rows = [c for c in I["cons"] if c["lb"] == c["ub"]]
        import osilx
        def vars_of(t):
            if t is None:
                return set()
            if t[0] == "var":
                return {t[1]}
            if t[0] == "num":
                return set()
            return set().union(*[vars_of(z) for z in t[1:]])
        prog = True
        while prog:
            prog = False
            for c in rows:
                unk = [j for j in c["lin"] if x[j] is None]
                allv = set(c["lin"]) | vars_of(c["nl"]) | {a for a, b, _ in c["quad"]} | {b for a, b, _ in c["quad"]}
                if len(unk) != 1 or any(x[j] is None for j in allv if j != unk[0]):
                    continue
                j = unk[0]
                if j in vars_of(c["nl"]) or any(j in (a, b) for a, b, _ in c["quad"]):
                    continue
                rest = dict(c, lin={k: a for k, a in c["lin"].items() if k != j})
                s_ = osilx.ev_row(rest, x, mp.mpf, ev.MPFNS)
                x[j] = (mp.mpf(c["lb"]) - s_) / mp.mpf(c["lin"][j])
                prog = True
        miss = [names[j] for j in range(len(names)) if x[j] is None]
        if miss:
            log(f"    primal recovery: undetermined {miss[:5]}")
            return None
        r = ev.evaluate(I, x, 50)
        import os
        outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", f"{M0['name']}.recovered.sol")
        with open(outp, "w") as fh:
            for nm, vv in zip(names, x):
                fh.write(f"{nm} {mp.nstr(vv, 25)}\n")
        # top violated rows
        vio = []
        for c in I["cons"]:
            val = osilx.ev_row(c, x, mp.mpf, ev.MPFNS)
            vv = mp.mpf(0)
            if not osilx.isinf(c["lb"]):
                vv = max(vv, mp.mpf(c["lb"]) - val)
            if not osilx.isinf(c["ub"]):
                vv = max(vv, val - mp.mpf(c["ub"]))
            if vv > 1e-6:
                vio.append((float(vv), c["name"], sorted(names[j] for j in c["lin"])[:3]))
        vio.sort(reverse=True)
        log(f"    violated rows (>1e-6): {len(vio)}; top: {vio[:4]}")
        return float(r["obj"]), float(r["row_viol"]), float(r["bound_viol"]), r["worst_row"]


def solve_node(M0, node):
    M = dict(M0)
    M["rows"] = list(M0["rows"]) + node_rows(node)      # angle rows (polar model) kept: valid for every node
    try:
        val, st, raw = ps.solve_dual_vec(M, chordal_decomposition_enable=False)
    except Exception as e:
        return None
    W = ps.solve_dual_vec.W
    res = pc.certify(M, raw, log=lambda s: None)
    if res is None:
        return None
    return res[0], W, val, st


def pair_stats(W, p, q):
    Wpp = W[2 * p, 2 * p] + W[2 * p + 1, 2 * p + 1]
    Wqq = W[2 * q, 2 * q] + W[2 * q + 1, 2 * q + 1]
    wr = W[2 * p, 2 * q] + W[2 * p + 1, 2 * q + 1]
    wi = W[2 * p + 1, 2 * q] - W[2 * p, 2 * q + 1]
    return Wpp, Wqq, wr, wi


def worst_pair(M0, W):
    from pf_bb import lines_of
    best = (-1, None)
    for (p, q) in lines_of(M0):
        if True:
            Wpp, Wqq, wr, wi = pair_stats(W, p, q)
            if abs(wr) + abs(wi) < 1e-9:
                continue
            v = (Wpp * Wqq - wr * wr - wi * wi) / (Wpp * Wqq)
            if v > best[0]:
                best = (v, (p, q))
    return best


def run(name, tlim, UB, rel_tol=1e-6, log=print):
    t0 = time.time()
    M0 = pm.decode(name)
    n = M0["n"]
    vdef = {}
    for r in M0["rows"]:
        if r["kind"] == "volt":
            (i, j), = [k for k in r["Q"] if k[0] == k[1] and k[0] % 2 == 0]
            k = i // 2
            lo2, hi2 = vdef.get(k, (None, None))
            if r["lb"] is not None:
                lo2 = r["lb"] if lo2 is None else max(lo2, r["lb"])
            if r["ub"] is not None:
                hi2 = r["ub"] if hi2 is None else min(hi2, r["ub"])
            vdef[k] = (lo2, hi2)
    # magnitudes: need rational square roots of the bounds (0.94^2 etc. are exact squares)
    vmag = {}
    for k, (a, b) in vdef.items():
        def rsqrt(x):
            num, den = x.numerator, x.denominator
            rn, rd = math.isqrt(num), math.isqrt(den)
            assert rn * rn == num and rd * rd == den, "bound not a rational square"
            return Fr(rn, rd)
        vmag[k] = (rsqrt(a), rsqrt(b))
    root = dict(vbox={}, cone={}, vdef=vmag)
    # polar model: the angle limits of a line give its initial cone when the line is first branched on
    angle0 = {(p, q): ((Fr(1), ta), (Fr(1), tb)) for (p, q), (A0, B0, ta, tb) in M0["angle"].items()}
    r = solve_node(M0, root)
    b, W, val, st = r
    log(f"root: bound {float(b)!r} ({st})  UB {UB}  gap {UB - float(b):.4g}")
    heap = [(float(b), 0, root, b, W)]
    cnt = 0
    closed = []
    nodes = 1
    tol = rel_tol * abs(UB)
    while heap and time.time() - t0 < tlim:
        fb, _, node, b, W = heapq.heappop(heap)
        if fb >= UB - tol:
            closed.append(b)
            continue
        viol, (p, q) = worst_pair(M0, W)
        if viol < 1e-6:
            rec = recover_primal(M0, W, log)
            if rec is not None:
                log(f"    near rank-one node (bound {fb!r}): recovered point obj {rec[0]!r} row viol {rec[1]:.2e} ({rec[3]}) bound viol {rec[2]:.2e}")
        Wpp, Wqq, wr, wi = pair_stats(W, p, q)
        cone = node["cone"].get((p, q), angle0.get((p, q), (None, None)))
        lp, up_ = node["vbox"].get(p, vmag[p])
        lq, uq = node["vbox"].get(q, vmag[q])
        # decide: angle split if the cone is wide, else split the wider magnitude range
        d1, d2 = cone
        width = None
        if d1 is not None and d2 is not None:
            a1, a2 = float(ang(d1)), float(ang(d2))
            while a2 < a1:
                a2 += 2 * math.pi
            width = a2 - a1
        kids = []
        if width is None or width > 0.02:
            if d1 is None and d2 is None:
                mid = math.atan2(wi, wr) if False else 0.0
                dm = (Fr(1), Fr(0))
                kids = [dict(node, cone={**node["cone"], (p, q): (None, dm)}), dict(node, cone={**node["cone"], (p, q): (dm, None)})]
            elif d1 is None or d2 is None:
                base = float(ang(d1 if d1 is not None else d2))
                mid = base + (math.pi / 2 if d1 is not None else -math.pi / 2)
                dm = rat_unit(mid)
                neg = lambda dd: (-dd[0], -dd[1])     # the half-plane "angle >= d" ends at direction -d
                if d1 is not None:
                    kids = [dict(node, cone={**node["cone"], (p, q): (d1, dm)}), dict(node, cone={**node["cone"], (p, q): (dm, neg(d1))})]
                else:
                    kids = [dict(node, cone={**node["cone"], (p, q): (neg(d2), dm)}), dict(node, cone={**node["cone"], (p, q): (dm, d2)})]
            else:
                dm = rat_unit(0.5 * (a1 + a2))
                kids = [dict(node, cone={**node["cone"], (p, q): (d1, dm)}), dict(node, cone={**node["cone"], (p, q): (dm, d2)})]
            what = f"angle {p}-{q}"
        else:
            k, (l, u) = (p, (lp, up_)) if (up_ - lp) >= (uq - lq) else (q, (lq, uq))
            m = ((l + u) / 2).limit_denominator(10**6)
            kids = [dict(node, vbox={**node["vbox"], k: (l, m)}), dict(node, vbox={**node["vbox"], k: (m, u)})]
            what = f"|V_{k}| at {float(m):.5f}"
        for kd in kids:
            rr = solve_node(M0, kd)
            nodes += 1
            if rr is None:
                cb, cW = b, W
            else:
                cb, cW = max(rr[0], b), rr[1]
            cnt += 1
            heapq.heappush(heap, (float(cb), cnt, kd, cb, cW))
        glb = min([h[0] for h in heap] + [float(x) for x in closed]) if (heap or closed) else float(b)
        log(f"  nodes {nodes}: split {what} (pair viol {viol:.2e}); LB {glb!r} gap {UB-glb:.4g} open {len(heap)} t {time.time()-t0:.0f}s")
    allb = [h[3] for h in heap] + closed
    return min(allb), nodes, len(heap)


if __name__ == "__main__":
    name = sys.argv[1]
    tl = float(sys.argv[2])
    UB = float(sys.argv[3])
    LB, nodes, nopen = run(name, tl, UB)
    print(f"FINAL {name}: certified LB {float(LB)!r} (exact {LB}) nodes {nodes} open {nopen}")
