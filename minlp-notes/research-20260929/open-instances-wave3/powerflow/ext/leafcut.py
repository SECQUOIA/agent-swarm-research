"""Exact valid cuts for the leaf generator bus L of powerflow0039p/0039r (bus index 29,
reached only through line N-L, N = 1).

Notation (exact, from the model rows; checked by leaf_info):
  W_NN = e_N^2 + f_N^2,  W_LL = e_L^2 + f_L^2,  w_R = e_N e_L + f_N f_L,  w_I = e_N f_L - f_N e_L,
  Pg = the cost-carrying generator output at L, Pg = s b w_I  (s = +-1),
  Qg = the reactive output at L,                Qg = b (W_LL - w_R),       b > 0.
For every real point, W_NN W_LL = w_R^2 + w_I^2 (Lagrange identity).  With
w_R = W_LL - Qg/b, w_I^2 = Pg^2/b^2 and W_LL >= vmin_L^2 > 0 this gives, at every point of
the relaxation R,
    W_NN = F(Pg, Qg, W_LL) := W_LL - 2 Qg/b + (Qg^2 + Pg^2) / (b^2 W_LL).
F is convex on W_LL > 0 ((q^2 + p^2)/s is a perspective).  On a box of (Pg, Qg, W_LL),
every affine H with H >= F at the eight vertices satisfies H >= F on the whole box, so
    W_NN - al Pg - be Qg - ga W_LL <= de                                       (cut)
holds at every point of R whose (Pg, Qg, W_LL) lies in the box.  planes3 enumerates the
planes through four vertices that are valid at all eight (exact rationals).
(An earlier variant that used only Qg >= q_lo, W_NN <= G(Pg, W_LL), was too weak and has
been removed; the assertion vmin_L^2 > q_hi / b in leaf_info is left from it and is not
needed for F.)
"""
from fractions import Fraction as Fr


def leaf_info(M, N=1, L=29):
    rows = M["rows"]
    eN, fN, eL, fL = 2 * N, 2 * N + 1, 2 * L, 2 * L + 1

    def key(i, j):
        return (i, j) if i <= j else (j, i)
    # rows touching bus L
    touch = [r for r in rows if any(i in (eL, fL) or j in (eL, fL) for (i, j) in r["Q"])]
    flows = [r for r in touch if r["kind"] == "flow"]
    assert len(flows) == 4, len(flows)
    b = None
    wI = {key(eN, fL): Fr(1), key(fN, eL): Fr(-1)}
    qg_form = None
    pg_flow = qg_flow = None
    for r in flows:
        (y,) = r["lin"]
        Qneg = {k: -v for k, v in r["Q"].items()}           # y = -<Q, x x^T>
        # P from L to N:  y = s b w_I
        if set(Qneg) == set(wI):
            c = Qneg[key(eN, fL)]
            assert Qneg[key(fN, eL)] == -c
            # the end at L: flow row whose y enters a linear row with a cost-carrying variable
            pg_flow = pg_flow or []
            pg_flow.append((y, c))
        elif key(eL, eL) in Qneg:
            # y = b (W_LL - w_R)
            bb = Qneg[key(eL, eL)]
            assert Qneg == {key(eL, eL): bb, key(fL, fL): bb, key(eN, eL): -bb, key(fN, fL): -bb}, Qneg
            qg_flow = (y, bb)
            b = bb
    assert b is not None and b > 0 and len(pg_flow) == 2
    # generator variables: linear rows  flow_y - g = 0  with g in the objective (Pg) / not (Qg)
    obj = M["obj"]
    Pg = Qg = None
    for r in rows:
        if r["kind"] == "linear" and len(r["lin"]) == 2 and r["lb"] == r["ub"] == 0 and not r["qy"]:
            (y1, c1), (y2, c2) = r["lin"].items()
            for (yf, cf), (yg, cg) in (((y1, c1), (y2, c2)), ((y2, c2), (y1, c1))):
                if cf == 1 and cg == -1:
                    if qg_flow and yf == qg_flow[0]:
                        Qg = yg
                    for (yp, c) in pg_flow:
                        if yf == yp and yg in obj["lin"]:
                            Pg = (yg, c)
    assert Pg is not None and Qg is not None
    (pg, c) = Pg
    assert abs(c) == b, (c, b)
    # the Pg and Qg variables appear only in their defining row (+ objective, + box)
    for r in rows:
        for yv in (pg, Qg):
            if yv in r["lin"] or yv in r["qy"]:
                assert r["kind"] == "linear" and len(r["lin"]) == 2, r["name"]
    qlo, qhi = M["ybox"][Qg]
    plo, phi = M["ybox"][pg]
    # voltage bounds of L (from the volt rows)
    vlo2 = max(r["lb"] for r in touch if r["kind"] == "volt" and r["lb"] is not None)
    vhi2 = min(r["ub"] for r in touch if r["kind"] == "volt" and r["ub"] is not None)
    assert vlo2 > qhi / b > 0
    return dict(N=N, L=L, b=b, Pg=pg, Qg=Qg, qlo=qlo, qhi=qhi, plo=plo, phi=phi, WLL=(vlo2, vhi2))


def F(info, p, q, s):
    """W_NN as a function of (Pg, Qg, W_LL) at every real point satisfying the leaf rows:
    W_NN W_LL = w_R^2 + w_I^2 with w_R = W_LL - Qg/b and w_I^2 = Pg^2/b^2."""
    b = info["b"]
    return s - 2 * q / b + (q * q + p * p) / (b * b * s)


def planes3(info, box):
    """all affine H(p, q, s) = al p + be q + ga s + de through four vertices of the box
    [p1,p2]x[q1,q2]x[s1,s2] with H >= F at all eight vertices (exact rationals).  By
    convexity of F (s > 0), each such H satisfies H >= F on the whole box."""
    (p1, p2), (q1, q2), (s1, s2) = box
    assert 0 < s1 and p1 <= p2 and q1 <= q2 and s1 <= s2
    V = []
    for p in sorted({p1, p2}):
        for q in sorted({q1, q2}):
            for s in sorted({s1, s2}):
                V.append((p, q, s, F(info, p, q, s)))
    out = set()
    from itertools import combinations
    free = [i for i, (a, c) in enumerate(((p1, p2), (q1, q2), (s1, s2))) if a != c]
    if len(free) < 3:
        # degenerate box: planes in the free coordinates only, through len(free)+1 vertices
        k = len(free)
        for tri in combinations(V, k + 1):
            A = [[t[i] for i in free] + [Fr(1)] for t in tri]
            z = [t[3] for t in tri]
            sol = _solve(A, z)
            if sol is None:
                continue
            coef = [Fr(0), Fr(0), Fr(0)]
            for i, c in zip(free, sol[:-1]):
                coef[i] = c
            H = (coef[0], coef[1], coef[2], sol[-1])
            if all(H[0] * p + H[1] * q + H[2] * s + H[3] >= f for (p, q, s, f) in V):
                out.add(H)
        return sorted(out)
    for quad in combinations(V, 4):
        A = [[t[0], t[1], t[2], Fr(1)] for t in quad]
        z = [t[3] for t in quad]
        sol = _solve(A, z)
        if sol is None:
            continue
        H = tuple(sol)
        if all(H[0] * p + H[1] * q + H[2] * s + H[3] >= f for (p, q, s, f) in V):
            out.add(H)
    return sorted(out)


def _solve(A, z):
    """exact Gaussian elimination; None if singular"""
    n = len(A)
    M = [list(r) + [zz] for r, zz in zip(A, z)]
    for c in range(n):
        piv = next((r for r in range(c, n) if M[r][c] != 0), None)
        if piv is None:
            return None
        M[c], M[piv] = M[piv], M[c]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c] / M[c][c]
                M[r] = [a - f * bb for a, bb in zip(M[r], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def cut_rows3(info, box, tag=""):
    """rows  W_NN - al Pg - be Qg - ga W_LL <= de  for each valid vertex plane of the box."""
    N, L = info["N"], info["L"]
    rows = []
    for t, (al, be, ga, de) in enumerate(planes3(info, box)):
        Q = {(2 * N, 2 * N): Fr(1), (2 * N + 1, 2 * N + 1): Fr(1)}
        if ga != 0:
            Q[(2 * L, 2 * L)] = -ga
            Q[(2 * L + 1, 2 * L + 1)] = -ga
        lin = {}
        if al != 0:
            lin[info["Pg"]] = -al
        if be != 0:
            lin[info["Qg"]] = -be
        rows.append(dict(name=f"LC{tag}_{t}", lin=lin, Q=Q, qy={}, lb=None, ub=de, kind="cut"))
    return rows
