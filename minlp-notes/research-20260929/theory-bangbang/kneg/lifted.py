"""Branch-and-bound certificates on the control of the switching stage, for the scalar toys (ktoy.py),
in exact rational arithmetic.

Node = {u_n in [l, r]} (other controls in U).  Two node bounds, both calibration bounds:

* fixed node family ("fixed"): the quadratic family with curvatures P (here the tangential P = -k) and
  the costates of the node's own KKT point z^A as slopes; bound = J(z^A) - sum of stage losses over
  D_t x U_t (stage n over [l, r]) - terminal loss.  Valid for every anchor.
* lifted family ("lifted"): u_n is treated as a parameter v in an interval V = [l', r'] of the node.  For
  each v, z(v) = z^A with u_n replaced by v (states re-simulated); the family has the curvatures P and the
  costates of z(v) (affine in v).  If every stage t != n is exact for every v in V (stage n has no control)
  and the terminal term is exact, the bound for {u_n in V} is min_{v in V} J(z(v)), an explicit 1-D
  quadratic.  Exactness for all v follows from exactness at the two ends of V, because sigma_t(v) is affine
  in v and the zero-loss set of a vertex stage is an interval (proof in kappa-negative.md, Lemma 3.2).
  The lifted bound is the calibration bound of the lifted problem with state (x, v), v in V.

Only families with beta_t = P_{t+1} + k_t = 0 at every stage are handled exactly (then the stage minimum
over d is at d = 0 whenever the anchor state lies in the box); this covers P = -k for constant k.
"""
from fractions import Fraction as Fr

from ktoy import kkt_refine, exact_kkt, stage_loss, terminal_loss, hess_exact


def _exact_anchor(toy, kk):
    """Exact anchor for a node.  Any feasible anchor gives a valid bound (the slopes need not be KKT
    costates); if the float active-set point is not an exact KKT point, the exact sign check is skipped
    and the record says so."""
    try:
        A = exact_kkt(toy, kk)
        A["kkt_exact"] = True
    except AssertionError:
        A = exact_kkt(toy, kk, check=False)
        A["kkt_exact"] = False
    return A


def _check_beta0(D, P):
    k = D["k"]
    assert all(P[t + 1] + k[t] == 0 for t in range(D["N"])), "lifted.py needs beta_t = 0"


def node_kkt(toy, N, u_start, n, l, r):
    kk = kkt_refine(toy, N, u_start, bnds={n: (float(l), float(r))})
    kk["bnds"] = {n: (l, r)}
    return _exact_anchor(toy, kk)


def fixed_bound(toy, A, P, n):
    """Calibration bound of node {u_n in [lo_n, hi_n]} with the family anchored at A (node KKT point)."""
    N = A["N"]
    D = dict(A)
    loss = Fr(0)
    worst = []
    for t in range(N):
        lt = stage_loss(toy, D, P, t, om_lo=A["lo"][t] - A["u"][t], om_hi=A["hi"][t] - A["u"][t])
        if lt > 0:
            worst.append((t, lt))
        loss += lt
    loss += terminal_loss(toy, D, P)
    return A["J"] - loss, worst


def lifted_interval(toy, A, P, n):
    """Largest interval V of v = u_n (inside A's node range) on which every stage t != n of the lifted
    family anchored at A is exact.  Returns (vlo, vhi) or None if even v = u^A_n fails.  Exact."""
    _check_beta0(A, P)
    N, h = A["N"], A["h"]
    un = A["u"][n]
    lo, hi = A["lo"][n] - un, A["hi"][n] - un          # delta range
    Hcol = hess_exact(toy, N, [n] + [t for t in range(N) if t != n])
    Htn = {t: Hcol[0][i + 1] for i, t in enumerate([t for t in range(N) if t != n])}
    dlo, dhi = lo, hi
    for t in range(N):
        if t == n:
            continue
        kap = P[t + 1]
        s, e = A["sig"][t], Htn[t] / h                 # sigma_t(delta) = s + e delta
        ut = A["u"][t]
        if A["lo"][t] < ut < A["hi"][t]:
            return None                                # another fractional stage: not handled here
        # zero loss: min over om in [0, om_f] of h sig om + h^2 kap om^2 / 2 >= 0, om_f the far end
        om_f = A["lo"][t] - ut if ut == A["hi"][t] else A["hi"][t] - ut
        # condition c0 + c1 delta >= 0 with c(delta) = h sig(delta) om_f + h^2 kap om_f^2 / 2 (kap < 0),
        # plus the sign condition sig(delta) om_f >= 0 (needed when kap >= 0)
        conds = [(h * s * om_f + h * h * kap * om_f * om_f / 2, h * e * om_f)]
        if kap >= 0:
            conds = [(s * om_f, e * om_f)]
        for c0, c1 in conds:
            if c1 == 0:
                if c0 < 0:
                    return None
                continue
            root = -c0 / c1
            if c1 > 0:
                dlo = max(dlo, root)
            else:
                dhi = min(dhi, root)
    if dlo > 0 or dhi < 0:
        return None
    # stage n (no control) and the terminal term must be exact; states must stay inside the box
    Kn = h + P[n + 1] - P[n]
    assert Kn >= 0
    assert terminal_loss(toy, A, P) == 0
    R = Fr(toy.R)
    for dl in (dlo, dhi):
        for t in range(n + 1, N + 1):
            assert abs(A["x"][t] + h * dl) <= R
    return un + dlo, un + dhi


def lifted_check_ends(toy, A, P, n, V):
    """Independent exact check: at both ends v of V, rebuild z(v) from scratch and verify that every
    stage t != n has zero loss for the family with the costates of z(v)."""
    from ktoy import exact_traj
    out = []
    for v in V:
        u = list(A["u"])
        u[n] = v
        Z = exact_traj(toy, A["N"], u, A["nu"])
        Z["lo"], Z["hi"] = A["lo"], A["hi"]
        mx = Fr(0)
        for t in range(A["N"]):
            if t == n:
                continue
            mx = max(mx, stage_loss(toy, Z, P, t, om_lo=A["lo"][t] - u[t], om_hi=A["hi"][t] - u[t]))
        out.append(mx)
    return out


def lifted_min(A, n, V, toy):
    """min over v in V of J(z(v)) = J(A) + h sig_n (v - u_n) + H_nn (v - u_n)^2 / 2 (exact quadratic)."""
    h = A["h"]
    Hnn = hess_exact(toy, A["N"], [n])[0][0]
    g = h * A["sig"][n]
    un = A["u"][n]
    cands = [V[0], V[1]]
    if Hnn > 0:
        vs = un - g / Hnn
        if V[0] <= vs <= V[1]:
            cands.append(vs)
    vals = [A["J"] + g * (v - un) + Hnn * (v - un) ** 2 / 2 for v in cands]
    i = min(range(len(vals)), key=lambda j: vals[j])
    return vals[i], cands[i]


def certify(toy, Z, P, n, target, eps=Fr(0), max_nodes=60, use_lifted=True, log=None):
    """Prove min over {u_n in U} of J >= target - eps by a 1-D branch and bound on u_n.  Z: exact KKT point
    (the anchor of the root).  Node bounds: lifted (if use_lifted) on the margin interval around the
    anchor, fixed elsewhere; nodes that fail are bisected.  Returns a record."""
    N = Z["N"]
    stack = [(Fr(-1), Fr(1))]
    nodes = []
    ok = True
    while stack:
        if len(nodes) >= max_nodes:
            ok = False
            break
        l, r = stack.pop()
        A = node_kkt(toy, N, [float(v) for v in Z["u"]], n, l, r)
        rec = dict(l=float(l), r=float(r), anchor_un=float(A["u"][n]), J_anchor_minus_target=float(A["J"] - target))
        V = lifted_interval(toy, A, P, n) if use_lifted else None
        if V is not None and (V[1] > V[0] or (l == r)):
            val, vmin = lifted_min(A, n, V, toy)
            rec.update(kind="lifted", V=[float(V[0]), float(V[1])], bound_minus_target=float(val - target))
            if val >= target - eps:
                nodes.append(rec)
                for (a, b) in ((l, V[0]), (V[1], r)):
                    if b > a:
                        stack.append((a, b))
                continue
        Bf, worst = fixed_bound(toy, A, P, n)
        rec.update(kind="fixed", bound_minus_target=float(Bf - target),
                   worst=[(t, float(v / Z["h"] ** 2)) for t, v in sorted(worst, key=lambda q: -q[1])[:3]])
        nodes.append(rec)
        if Bf >= target - eps:
            continue
        m = (l + r) / 2
        nodes[-1]["kind"] += "-split"
        stack += [(l, m), (m, r)]
    return dict(ok=ok, nodes=nodes, n_nodes=len(nodes), n_lifted=sum(1 for q in nodes if q["kind"] == "lifted"))


# ---------------------------------------------------------------- float screening: epsilon-certificates
def fixed_bound_float(toy, N, u_start, n, l, r, kconst):
    """Float node bound with the tangential family P = -k (beta = 0): node KKT point by active-set
    Newton, then closed-form stage losses max(0, -min_{om in ends} (h sig om + h^2 kap om^2 / 2))."""
    import numpy as np
    kk = kkt_refine(toy, N, u_start, bnds={n: (float(l), float(r))})
    h = kk["h"]
    lo = np.full(N, -1.0)
    hi = np.full(N, 1.0)
    lo[n], hi[n] = float(l), float(r)
    om_lo, om_hi = lo - kk["u"], hi - kk["u"]
    kap = -kconst
    f = lambda om: h * kk["sig"] * om + h * h * kap * om * om / 2
    loss = np.maximum(0.0, -np.minimum(f(om_lo), f(om_hi)))
    return kk["J"] - loss.sum(), kk, loss


def greedy_partition(toy, N, u_bar, n, target, eps, kconst, h2scale, safety=1.0):
    """Outward greedy partition of [-1, 1] for u_n: a central node [ub - w0, ub + w0] (anchor zbar,
    deficit k h^2 w0^2 / 2 <= eps), then nodes as wide as possible (bisection on the width) whose fixed
    bound is >= target - eps.  Returns the list of nodes (l, r, bound - target)."""
    import math
    eps = eps * safety                  # safety < 1: leave room for float rounding (exact re-check)
    ub = float(u_bar[n])
    h = toy.T / N
    w0 = math.sqrt(2 * eps / (h * h * kconst))
    nodes = []
    l0, r0 = max(-1.0, ub - w0), min(1.0, ub + w0)
    B, _, _ = fixed_bound_float(toy, N, u_bar, n, l0, r0, kconst)
    nodes.append((l0, r0, (B - target) / h2scale))
    for side in (+1, -1):
        edge = r0 if side > 0 else l0
        far = 1.0 if side > 0 else -1.0

        def ok(e, w):
            a, b = (e, e + w) if side > 0 else (e - w, e)
            Bn, _, _ = fixed_bound_float(toy, N, u_bar, n, a, b, kconst)
            return Bn >= target - eps, Bn

        def widest(e):
            wmax = abs(far - e)
            if ok(e, wmax)[0]:
                return wmax
            lo_w, hi_w = 0.0, wmax
            for _ in range(40):
                mid = (lo_w + hi_w) / 2
                if ok(e, mid)[0]:
                    lo_w = mid
                else:
                    hi_w = mid
            return lo_w
        side_nodes = []
        backtracks = 0
        while abs(far - edge) > 1e-12:
            w = widest(edge)
            if w <= 1e-12:
                # stalled: shorten the previous node of this side (sub-intervals of prunable nodes stay
                # prunable in these runs; checked by recomputing its bound) and retry from its new end
                if not side_nodes or backtracks > 60:
                    nodes.append(("stuck", edge))
                    break
                a, b, _ = side_nodes.pop()
                start = a if side > 0 else b
                old_w = abs(b - a)
                nw = old_w * 0.7
                good, Bn = ok(start, nw)
                if not good:
                    nodes.append(("stuck", edge))
                    break
                backtracks += 1
                na, nb = (start, start + nw) if side > 0 else (start - nw, start)
                side_nodes.append((na, nb, (Bn - target) / h2scale))
                edge = nb if side > 0 else na
                continue
            Bn = ok(edge, w)[1]
            a, b = (edge, edge + w) if side > 0 else (edge - w, edge)
            side_nodes.append((a, b, (Bn - target) / h2scale))
            edge = b if side > 0 else a
        nodes += side_nodes
    return nodes


# ---------------------------------------------------------------- multi-stage branch and bound (boxes)
def _node_kkt_box(toy, N, u_start, bn):
    kk = kkt_refine(toy, N, u_start, bnds={t: (float(l), float(r)) for t, (l, r) in bn.items()})
    kk["bnds"] = dict(bn)
    return _exact_anchor(toy, kk)


def certify_box(toy, Z, P, target, eps=Fr(0), max_nodes=200, use_lifted=True):
    """Branch and bound over boxes in the controls (exact).  Node = {u_t in [l_t, r_t] for t in its
    dictionary}.  Bound: lifted on the worst stage n of the anchor (if every other stage of the anchor
    is a vertex of the node box and exact on an interval V of u_n), else fixed.  A failing node is split
    on its worst stage: around V (lifted), or at the anchor value / midpoint."""
    N = Z["N"]
    stack = [dict()]
    nodes = []
    while stack:
        if len(nodes) >= max_nodes:
            return dict(ok=False, nodes=nodes, n_nodes=len(nodes))
        bn = stack.pop()
        A = _node_kkt_box(toy, N, [float(v) for v in Z["u"]], bn)
        Bf, worst = fixed_bound(toy, A, P, None)
        rec = dict(box={t: (float(l), float(r)) for t, (l, r) in bn.items()}, J_anchor_minus_target=float(A["J"] - target),
                   fixed_bound_minus_target=float(Bf - target))
        if Bf >= target - eps:
            rec["kind"] = "fixed"
            nodes.append(rec)
            continue
        n = max(worst, key=lambda q: q[1])[0]
        l, r = bn.get(n, (Fr(-1), Fr(1)))
        if use_lifted:
            V = lifted_interval(toy, A, P, n)
            if V is not None and V[1] > V[0]:
                val, _ = lifted_min(A, n, V, toy)
                if val >= target - eps:
                    rec.update(kind="lifted", stage=n, V=(float(V[0]), float(V[1])),
                               bound_minus_target=float(val - target))
                    nodes.append(rec)
                    for (a, b) in ((l, V[0]), (V[1], r)):
                        if b > a:
                            stack.append({**bn, n: (a, b)})
                    continue
        un = A["u"][n]
        m = un if l < un < r else (l + r) / 2
        rec.update(kind="split", stage=n, at=float(m))
        nodes.append(rec)
        stack += [{**bn, n: (l, m)}, {**bn, n: (m, r)}]
    return dict(ok=True, nodes=nodes, n_nodes=len(nodes),
                n_leaves=sum(1 for q in nodes if q["kind"] in ("fixed", "lifted")))


# ---------------------------------------------------------------- lifting several stages (boxes)
def lifted_box(toy, A, P, E):
    """Lift the controls of the stages in E (the anchor's other stages must be vertices of the node box).
    z(v) = A with u_E = v.  Every stage t not in E has a zero-loss condition c0_t + sum_e c_te delta_e >= 0
    (affine in delta = v - u^A_E; derivation as in lifted_interval).  Returns the largest box
    {delta_e in [lam lo_e, lam hi_e]} (one factor lam in [0, 1] for all e, lo/hi the node range minus the
    anchor) on which all conditions hold at every corner (hence everywhere, by affinity), or None."""
    _check_beta0(A, P)
    N, h = A["N"], A["h"]
    E = list(E)
    from ktoy import hess_exact as _he
    cols = {}
    others = [t for t in range(N) if t not in E]
    for e in E:
        Hc = _he(toy, N, [e] + others)
        cols[e] = {t: Hc[0][i + 1] for i, t in enumerate(others)}
    lo = {e: A["lo"][e] - A["u"][e] for e in E}
    hi = {e: A["hi"][e] - A["u"][e] for e in E}
    conds = []
    for t in others:
        ut = A["u"][t]
        if A["lo"][t] < ut < A["hi"][t]:
            return None
        kap = P[t + 1]
        om_f = A["lo"][t] - ut if ut == A["hi"][t] else A["hi"][t] - ut
        s = A["sig"][t]
        if kap >= 0:
            c0, cs = s * om_f, {e: cols[e][t] / h * om_f for e in E}
        else:
            c0 = h * s * om_f + h * h * kap * om_f * om_f / 2
            cs = {e: cols[e][t] * om_f for e in E}       # h * (H_te / h) * om_f
        if c0 < 0:
            return None
        conds.append((c0, cs))
    lam = Fr(1)
    import itertools as _it
    for corner in _it.product((0, 1), repeat=len(E)):
        for c0, cs in conds:
            slope = sum(cs[e] * (lo[e] if c else hi[e]) for e, c in zip(E, corner))
            if slope < 0:
                lam = min(lam, c0 / (-slope))
    if lam <= 0:
        return None
    assert terminal_loss(toy, A, P) == 0
    for e in E:
        assert h + P[e + 1] - P[e] >= 0
    return {e: (A["u"][e] + lam * lo[e], A["u"][e] + lam * hi[e]) for e in E}, lam


def lifted_box_min(toy, A, E, box):
    """min over v in box of J(z(v)) = J(A) + sum_e h sig_e delta_e + delta^T H_EE delta / 2 (exact)."""
    from ktoy import hess_exact as _he, box_qp_min
    h = A["h"]
    HE = _he(toy, A["N"], E)
    g = [h * A["sig"][e] for e in E]
    lo = [box[e][0] - A["u"][e] for e in E]
    hi = [box[e][1] - A["u"][e] for e in E]
    return A["J"] + box_qp_min(g, HE, lo, hi)


def certify_multi(toy, Z, P, target, eps=Fr(0), max_nodes=300):
    """Branch and bound over boxes in the controls of a few stages (exact).  At each node: fixed bound;
    if it fails, lift E = (fractional stages of the anchor) + (the stage with the largest loss) on the
    largest admissible sub-box; the rest of the node box is split into boxes around the sub-box.  If
    lifting is impossible, bisect the worst stage at the anchor value (or midpoint)."""
    N = Z["N"]
    stack = [dict()]
    nodes = []
    best = dict(J=target, u=list(Z["u"]), frac=list(Z["frac"]), improved=False)
    while stack:
        if len(nodes) >= max_nodes:
            return dict(ok=False, nodes=nodes, n_nodes=len(nodes), incumbent=best)
        bn = stack.pop()
        A = _node_kkt_box(toy, N, [float(v) for v in Z["u"]], bn)
        if A["J"] < best["J"]:
            # a better feasible point (exact KKT point of the node problem): new incumbent.  Nodes pruned
            # earlier against the larger target stay pruned.
            best = dict(J=A["J"], u=list(A["u"]), frac=list(A["frac"]), improved=True)
            target = A["J"]
        Bf, worst = fixed_bound(toy, A, P, None)
        rec = dict(box={t: (float(l), float(r)) for t, (l, r) in bn.items()},
                   J_anchor_minus_target=float(A["J"] - target), fixed_bound_minus_target=float(Bf - target))
        if Bf >= target - eps:
            rec["kind"] = "fixed"
            nodes.append(rec)
            continue
        wst = max(worst, key=lambda q: q[1])[0]
        E = sorted(set(A["frac"]) | {wst})
        lb = lifted_box(toy, A, P, E) if len(E) <= 3 else None
        if lb is not None:
            sub, lam = lb
            val = lifted_box_min(toy, A, E, sub)
            if val >= target - eps:
                rec.update(kind="lifted", stages=E, sub={e: (float(a), float(b)) for e, (a, b) in sub.items()},
                           lam=float(lam), bound_minus_target=float(val - target))
                nodes.append(rec)
                # cover node box minus sub-box by boxes: for each e, the pieces below / above the sub-range
                import itertools as _it
                ranges = {e: [] for e in E}
                for e in E:
                    l, r = bn.get(e, (Fr(-1), Fr(1)))
                    a, b = sub[e]
                    ranges[e] = [(l, a), (a, b), (b, r)]
                for combo in _it.product(range(3), repeat=len(E)):
                    if all(c == 1 for c in combo):
                        continue
                    piece = dict(bn)
                    empty = False
                    for e, c in zip(E, combo):
                        a, b = ranges[e][c]
                        if b <= a:
                            empty = True
                            break
                        piece[e] = (a, b)
                    if not empty:
                        stack.append(piece)
                continue
        l, r = bn.get(wst, (Fr(-1), Fr(1)))
        un = A["u"][wst]
        m = un if l < un < r else (l + r) / 2
        rec.update(kind="split", stage=wst, at=float(m))
        nodes.append(rec)
        stack += [{**bn, wst: (l, m)}, {**bn, wst: (m, r)}]
    return dict(ok=True, nodes=nodes, n_nodes=len(nodes), incumbent=best,
                n_leaves=sum(1 for q in nodes if q["kind"] in ("fixed", "lifted")))
