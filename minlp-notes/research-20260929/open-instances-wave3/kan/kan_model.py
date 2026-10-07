"""Exact decoding of the MINLPLib KAN instances (kan_r3_h1_n*, kan_r5_h1_n*).

Reads the OSIL file with the decimal-preserving reader osilx.py and recovers the
Kolmogorov-Arnold network  obj = A*(beta0 + sum_j psi_j(h_j)) + B,
h_j = beta_j + sum_i phi_ij(u_i), where every edge function is
    phi(z) = w_s * S(z) + w_b * silu(z),   S(z) = sum_m c_m B_m(z)
and the B-spline basis B_m is encoded by binaries (one per knot interval,
big-M rows) and the Cox-de Boor recursion (bilinear rows).

Everything is decoded by explicit pattern checks against the parsed rows; every
row and every variable must be accounted for (asserted).  All constants are kept
as Fractions of the OSIL decimal strings.

Main entry points
    decode(name)            -> model dict (exact)
    piece_polys(edge)       -> model's own spline polynomial on each knot interval
                               (exact, obtained by propagating the recursion rows
                               with the binaries fixed)
    ideal_pieces(edge)      -> the exact C^2 cubic spline on the decoded knots
    full_point(M, u, ...)   -> all OSIL variables from the inputs (mpmath)
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import os
import sys
from fractions import Fraction as Fr

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
import osilx  # noqa: E402

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def F(s):
    return Fr(s)


# ----------------------------------------------------------------------------
# polynomials with Fraction coefficients (list, lowest degree first)
def padd(a, b):
    n = max(len(a), len(b))
    return ptrim([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])


def pscale(a, c):
    return ptrim([c * x for x in a])


def pmul(a, b):
    if not a or not b:
        return []
    r = [Fr(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return ptrim(r)


def ptrim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def peval(a, x):
    s = 0
    for c in reversed(a):
        s = s * x + c
    return s


def pder(a):
    return ptrim([i * a[i] for i in range(1, len(a))])


def pshift(a, x0):
    """coefficients of q(s) = a(x0 + s)"""
    r = []
    for c in reversed(a):  # Horner with polynomials
        r = padd(pmul(r, [x0, Fr(1)]), [c])
    return r


def pabsbound(a, lo, hi):
    """exact rational upper bound of |a(x)| on [lo, hi] (Taylor at lo)."""
    q = pshift(a, lo)
    w = hi - lo
    assert w >= 0
    return sum(abs(c) * w ** k for k, c in enumerate(q))


# ----------------------------------------------------------------------------
SILU_TREE = lambda z: ("negate", ("divide", ("var", z, "1"), ("sum", ("exp", ("var", z, "-1")), ("num", "1"))))


def decode(name):
    I = osilx.read(os.path.join(OSIL, name + ".osil"))
    N, cons = I["names"], I["cons"]
    nv = len(N)
    vt = I["vt"]
    isbin = [t == "B" for t in vt]
    assert all(t in ("B", "C") for t in vt)
    for j in range(nv):
        if isbin[j]:
            assert I["lb"][j] == "0" and I["ub"][j] == "1"
    lb = [None if osilx.isinf(s) else F(s) for s in I["lb"]]
    ub = [None if osilx.isinf(s) else F(s) for s in I["ub"]]
    used = [False] * len(cons)
    for c in cons:
        assert c["constant"] == "0", c["name"]

    def eq(c):
        return c["lb"] == c["ub"] and not osilx.isinf(c["lb"])

    # ---- objective: min obj var
    o = I["obj"]
    assert o["sense"] == "min" and o["constant"] == "0" and not o["quad"] and o["nl"] is None
    assert len(o["lin"]) == 1 and list(o["lin"].values()) == ["1"]
    objv = list(o["lin"])[0]

    # ---- SiLU rows
    silu = {}  # s var -> z var
    for r, c in enumerate(cons):
        if c["nl"] is not None:
            assert eq(c) and c["lb"] == "0" and not c["quad"] and len(c["lin"]) == 1
            (s, cs), = c["lin"].items()
            assert cs == "1"
            z = c["nl"][1][1][1]
            assert c["nl"] == SILU_TREE(z), c["nl"]
            silu[s] = z
            used[r] = True
    zargs = sorted(set(silu.values()))
    assert len(zargs) == len(silu), "each edge argument has its own SiLU row"

    # ---- rows grouped by the edge argument z
    edges = []
    for s, z in silu.items():
        E = dict(z=z, s=s)
        # big-M rows
        lows, ups = {}, {}
        M1 = M2 = None
        for r, c in enumerate(cons):
            if used[r] or c["quad"] or c["nl"] is not None or z not in c["lin"]:
                continue
            if not (osilx.isinf(c["lb"]) and not osilx.isinf(c["ub"])):
                continue
            others = [v for v in c["lin"] if v != z]
            assert len(others) <= 1 and all(isbin[v] for v in others), c["name"]
            cz = c["lin"][z]
            if cz == "-1":
                M1 = F(c["ub"]) if M1 is None else M1
                assert F(c["ub"]) == M1
                lows[others[0] if others else None] = F(c["lin"][others[0]]) if others else Fr(0)
            else:
                assert cz == "1"
                M2 = F(c["ub"]) if M2 is None else M2
                assert F(c["ub"]) == M2
                ups[others[0] if others else None] = F(c["lin"][others[0]]) if others else Fr(0)
            used[r] = True
        bins = [b for b in lows if b is not None] + [b for b in ups if b is not None]
        bins = sorted(set(bins))
        # order binaries by their interval: lower bound c_k - M1
        # (the first interval has no 'low' row with a binary; the last no 'up' row)
        assert None in lows and None in ups
        K = len(bins)
        lo_of = {b: (lows[b] - M1 if b in lows else -M1) for b in bins}
        hi_of = {b: (M2 - ups[b] if b in ups else M2) for b in bins}
        order = sorted(bins, key=lambda b: lo_of[b])
        assert [b for b in bins if b not in lows] == [order[0]] and [b for b in bins if b not in ups] == [order[-1]]
        E["bins"] = order
        E["lo"] = [lo_of[b] for b in order]
        E["hi"] = [hi_of[b] for b in order]
        E["M1"], E["M2"] = M1, M2
        # one-hot row
        oh = [r for r, c in enumerate(cons) if not used[r] and eq(c) and c["lb"] == "1" and not c["quad"]
              and set(c["lin"]) == set(order) and all(v == "1" for v in c["lin"].values())]
        assert len(oh) == 1
        used[oh[0]] = True
        # recursion rows: quad terms (v, z) with v binary or basis var
        level = {b: 0 for b in order}
        rec = []
        for r, c in enumerate(cons):
            if used[r] or not c["quad"]:
                continue
            if not all(q[1] == z for q in c["quad"]):
                continue
            assert eq(c) and c["lb"] == "0" and len(c["quad"]) == 2 and len(c["lin"]) == 3
            rec.append(r)
            used[r] = True
        # determine the basis var of each rec row (the lin var with coef 1 not in quad)
        basis_rows = {}
        for r in rec:
            c = cons[r]
            qv = [q[0] for q in c["quad"]]
            new = [v for v in c["lin"] if v not in qv]
            assert len(new) == 1 and c["lin"][new[0]] == "1"
            assert set(qv) == set(v for v in c["lin"] if v != new[0])
            basis_rows[new[0]] = r
        # levels
        changed = True
        while changed:
            changed = False
            for B, r in basis_rows.items():
                if B in level:
                    continue
                qv = [q[0] for q in cons[r]["quad"]]
                if all(v in level for v in qv):
                    lv = {level[v] for v in qv}
                    assert len(lv) == 1
                    level[B] = lv.pop() + 1
                    changed = True
        assert all(B in level for B in basis_rows)
        deg = max(level.values())
        E["deg"] = deg
        E["rec"] = basis_rows
        E["level"] = level
        top = sorted([B for B in basis_rows if level[B] == deg])
        # partition rows sum_{level p} B = 1, p = 1..deg
        for p in range(1, deg + 1):
            Bp = {B for B in basis_rows if level[B] == p}
            pr = [r for r, c in enumerate(cons) if not used[r] and eq(c) and c["lb"] == "1" and not c["quad"]
                  and set(c["lin"]) == Bp and all(v == "1" for v in c["lin"].values())]
            assert len(pr) == 1, (p, pr)
            used[pr[0]] = True
            E.setdefault("partition_rows", []).append(cons[pr[0]]["name"])
        # spline-sum row: {B_m: c_m (top level), S: -1} = 0
        sr = [r for r, c in enumerate(cons) if not used[r] and eq(c) and c["lb"] == "0" and not c["quad"]
              and c["nl"] is None and set(top) <= set(c["lin"]) and len(c["lin"]) == len(top) + 1]
        assert len(sr) == 1
        c = cons[sr[0]]
        used[sr[0]] = True
        (S,) = [v for v in c["lin"] if v not in top]
        assert c["lin"][S] == "-1"
        E["S"] = S
        E["coef"] = {B: F(c["lin"][B]) for B in top}
        # edge-combination row {e: 1, S: -ws, s: -wb} = 0
        cr = [r for r, c in enumerate(cons) if not used[r] and eq(c) and c["lb"] == "0" and not c["quad"]
              and c["nl"] is None and S in c["lin"] and s in c["lin"] and len(c["lin"]) == 3]
        assert len(cr) == 1
        c = cons[cr[0]]
        used[cr[0]] = True
        (e,) = [v for v in c["lin"] if v not in (S, s)]
        assert c["lin"][e] == "1"
        E["e"] = e
        E["ws"] = -F(c["lin"][S])
        E["wb"] = -F(c["lin"][s])
        edges.append(E)

    # ---- remaining rows: neuron sums, copies/scalings, output, objective
    evars = {E["e"]: k for k, E in enumerate(edges)}
    sums = []
    aff = []   # (v1, a1, v2, a2, rhs): a1 v1 + a2 v2 = rhs
    for r, c in enumerate(cons):
        if used[r]:
            continue
        assert eq(c) and not c["quad"] and c["nl"] is None, c["name"]
        ev = [v for v in c["lin"] if v in evars]
        if ev:
            (h,) = [v for v in c["lin"] if v not in evars]
            assert c["lin"][h] == "1" and all(c["lin"][v] == "-1" for v in ev)
            sums.append(dict(h=h, bias=F(c["lb"]), edges=[evars[v] for v in ev]))
        else:
            assert len(c["lin"]) == 2, c["name"]
            (v1, a1), (v2, a2) = c["lin"].items()
            aff.append((v1, F(a1), v2, F(a2), F(c["lb"])))
        used[r] = True
    assert all(used)

    # affine closure: express every var in an affine class as a*root + b
    rep = {}

    def find(v):
        # returns (root, a, b) with v = a*root + b
        if v not in rep:
            return (v, Fr(1), Fr(0))
        r0, a, b = rep[v]
        R, a2, b2 = find(r0)
        rep[v] = (R, a * a2, a * b2 + b)
        return rep[v]

    # roots preference: SiLU arguments of first-layer edges and neuron-sum vars
    pref = set(zargs) | {sm["h"] for sm in sums}
    for (v1, a1, v2, a2, rhs) in aff:
        R1, p1, q1 = find(v1)
        R2, p2, q2 = find(v2)
        assert R1 != R2
        # a1 (p1 R1 + q1) + a2 (p2 R2 + q2) = rhs
        # attach the non-preferred root to the other one
        if R1 in pref and R2 in pref:
            # both preferred: must be a copy between a neuron sum and a 2nd-layer argument, or two args
            pass
        if R2 in pref and R1 not in pref:
            R1, p1, q1, a1, R2, p2, q2, a2 = R2, p2, q2, a2, R1, p1, q1, a1
        # now express R2 in terms of R1: R2 = (rhs - a1 p1 R1 - a1 q1 - a2 q2)/(a2 p2)
        den = a2 * p2
        rep[R2] = (R1, -a1 * p1 / den, (rhs - a1 * q1 - a2 * q2) / den)
    classes = {}
    for v in range(nv):
        if isbin[v]:
            continue
        R, a, b = find(v)
        classes.setdefault(R, []).append((v, a, b))
    # ---- network: layer-1 edges have argument in an input class, layer-2 in a neuron class
    hvars = {sm["h"] for sm in sums}
    hroot = {}
    for sm in sums:
        R, a, b = find(sm["h"])
        assert (a, b) == (1, 0) or R == sm["h"]
        hroot[find(sm["h"])[0]] = sm
    # the output sum is the neuron sum whose edges' arguments are in neuron classes
    inputs, hidden, out = [], [], None
    for sm in sums:
        zr = {find(edges[k]["z"])[0] for k in sm["edges"]}
        if all(R in hroot for R in zr):
            assert out is None
            out = sm
        else:
            hidden.append(sm)
    assert out is not None
    in_roots = sorted({find(edges[k]["z"])[0] for sm in hidden for k in sm["edges"]})
    # every layer-1 edge argument is an exact copy (a=1,b=0) of its class root
    for sm in hidden:
        for k in sm["edges"]:
            R, a, b = find(edges[k]["z"])
            assert a == 1 and b == 0 and R in in_roots
            edges[k]["layer"] = 1
            edges[k]["src"] = in_roots.index(R)
    hidden_ids = {id(sm): j for j, sm in enumerate(hidden)}
    for k in out["edges"]:
        R, a, b = find(edges[k]["z"])
        (j,) = [jj for jj, sm in enumerate(hidden) if find(sm["h"])[0] == R]
        Rh, ah, bh = find(hidden[j]["h"])
        assert (a, b) == (ah, bh) == (1, 0)
        edges[k]["layer"] = 2
        edges[k]["src"] = j
    for sm in hidden:
        srcs = sorted(edges[k]["src"] for k in sm["edges"])
        assert srcs == list(range(len(in_roots)))
    assert sorted(edges[k]["src"] for k in out["edges"]) == list(range(len(hidden)))

    # ---- bounds of a class root from all members (exact)
    def root_box(R):
        L, U = None, None
        for (v, a, b) in classes[R]:
            for bound, isup in ((lb[v], False), (ub[v], True)):
                if bound is None:
                    continue
                # a*R + b <= bound (isup) or >= bound
                t = (bound - b) / a
                upper = (isup and a > 0) or (not isup and a < 0)
                if upper:
                    U = t if U is None else min(U, t)
                else:
                    L = t if L is None else max(L, t)
        return L, U

    # ---- output: obj = A*y + B, y = out sum
    y = out["h"]
    Ry, ay, by = find(y)
    Ro, ao, bo = find(objv)
    assert Ry == Ro
    # objv = ao*R + bo, y = ay*R + by -> objv = (ao/ay) (y - by) + bo
    A = ao / ay
    Bc = bo - A * by
    M = dict(name=name, I=I, edges=edges, inputs=in_roots, input_box=[root_box(R) for R in in_roots],
             hidden=[dict(h=sm["h"], bias=sm["bias"], edges=sm["edges"], box=root_box(find(sm["h"])[0]),
                          root=find(sm["h"])[0]) for sm in hidden],
             out=dict(y=y, bias=out["bias"], edges=out["edges"], box=root_box(Ry)),
             A=A, B=Bc, objv=objv, classes=classes, lb=lb, ub=ub, isbin=isbin)
    # sanity: the hidden sum var is the class root (so 'box' is its bound set)
    for Hd in M["hidden"]:
        assert Hd["root"] == Hd["h"] or find(Hd["h"])[1:] == (1, 0)
    return M


# ----------------------------------------------------------------------------
def piece_polys(M, E):
    """Model's own spline S and basis polynomials on each knot interval k,
    obtained by propagating the recursion rows with b_k = 1, other binaries 0.
    Returns list over k of dict(S=poly, B={var: poly})."""
    cons = M["I"]["cons"]
    z = E["z"]
    res = []
    for k, bk in enumerate(E["bins"]):
        val = {b: ([Fr(1)] if b == bk else []) for b in E["bins"]}
        todo = sorted(E["rec"], key=lambda B: E["level"][B])
        for B in todo:
            c = cons[E["rec"][B]]
            s = []
            for v, a in c["lin"].items():
                if v == B:
                    continue
                s = padd(s, pscale(val[v], F(a)))
            for (v, w, a) in c["quad"]:
                assert w == z
                s = padd(s, pmul(pscale(val[v], F(a)), [Fr(0), Fr(1)]))
            val[B] = pscale(s, Fr(-1))   # B + s = 0
        S = []
        for B, cm in E["coef"].items():
            S = padd(S, pscale(val[B], cm))
        res.append(dict(S=S, B=val))
    return res


def ideal_knots(E):
    """t_0 = -M1, t_K = M2, interior t_k = lo_{k+1} (exact decimals of the big-M rows)."""
    K = len(E["bins"])
    t = [E["lo"][0]] + [E["lo"][k] for k in range(1, K)] + [E["hi"][K - 1]]
    return t


def ideal_basis(t, deg):
    """Exact Cox-de Boor on knots t_0..t_K: returns dict (m, p) -> list over pieces
    k=0..K-1 of polynomials; basis (m,p) (m = 1-based like the model's order-p var
    index) is supported on [t_{m-1}, t_{m+p}]."""
    K = len(t) - 1
    Bp = {}
    for m in range(1, K + 1):
        Bp[(m, 0)] = [([Fr(1)] if k == m - 1 else []) for k in range(K)]
    for p in range(1, deg + 1):
        for m in range(1, K - p + 1):
            d1 = t[m + p - 1] - t[m - 1]
            d2 = t[m + p] - t[m]
            f1 = [-t[m - 1] / d1, 1 / d1]          # (z - t_{m-1})/d1
            f2 = [t[m + p] / d2, -1 / d2]          # (t_{m+p} - z)/d2
            Bp[(m, p)] = [padd(pmul(f1, Bp[(m, p - 1)][k]), pmul(f2, Bp[(m + 1, p - 1)][k])) for k in range(K)]
    return Bp


def support(polys):
    return tuple(k for k, q in enumerate(polys) if q)


def ideal_pieces(M, E, model_pieces=None):
    """Ideal spline S~ = sum_m c_m B~_m on the decoded knots.  The model's
    top-level basis vars are matched to ideal bases by support.
    Returns (t, list over pieces of S~ polynomial, match info)."""
    if model_pieces is None:
        model_pieces = piece_polys(M, E)
    t = ideal_knots(E)
    K = len(t) - 1
    Bp = ideal_basis(t, E["deg"])
    ideal_by_support = {support(Bp[(m, E["deg"])]): m for m in range(1, K - E["deg"] + 1)}
    St = [[] for _ in range(K)]
    match = {}
    for B, cm in E["coef"].items():
        sup = tuple(k for k in range(K) if model_pieces[k]["B"][B])
        m = ideal_by_support[sup]
        match[B] = m
        for k in range(K):
            St[k] = padd(St[k], pscale(Bp[(m, E["deg"])][k], cm))
    assert len(set(match.values())) == len(match)
    return t, St, match


def spline_error(M, E, zlo, zhi):
    """Rigorous (exact rational) bound  max |S_model(z) - S~(z)|  over every
    z in [zlo, zhi] and every knot interval k allowed by the big-M rows at z,
    i.e. z in [lo_k, hi_k].  Also returns the allowed piece range."""
    mp_ = piece_polys(M, E)
    t, St, _ = ideal_pieces(M, E, mp_)
    K = len(t) - 1
    worst = Fr(0)
    allowed = []
    for k in range(K):
        a, b = max(E["lo"][k], zlo), min(E["hi"][k], zhi)
        if a > b:
            continue
        allowed.append(k)
        for k2 in range(K):   # ideal pieces overlapping [a, b]
            a2, b2 = max(a, t[k2]), min(b, t[k2 + 1])
            if a2 > b2:
                continue
            d = padd(mp_[k]["S"], pscale(St[k2], Fr(-1)))
            worst = max(worst, pabsbound(d, a2, b2))
    return worst, allowed, t, St
