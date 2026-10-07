"""Reviewer's independent re-evaluation of the pf_bb3 leaf certificates.

For one stored run (ext/logs/<name>.<tag>.json):
 1. Coverage: all leaf-box breakpoints define a grid of elementary cells; every cell must lie
    in exactly one leaf box, and the leaf boxes must lie in the root box.  The root box is
    read from the reviewer's own relaxation (y boxes of Pg, Qg; voltage bounds of bus L).
 2. Node rows: own relaxation rows (own_relax, content checked equal to pf_model in
    cmp_rows.py) in the author's row order, plus VBL (s1 <= W_LL <= s2) and the cut rows,
    whose planes are enumerated here independently and must equal the author's list (for the
    multiplier alignment).  Every plane is checked H >= F at all 8 box vertices exactly.
 3. Lagrangian: exact rationals.  obj + sum_eq w (h - rhs) + sum_ineq [m+ (h - ub) + m- (lb - h)]
    = const + sum_y (sig y^2 + kap y) + x^T A x.  The y part is minimized exactly over the node
    y boxes (unboxed y: sig > 0 required, else failure).
 4. PSD proof (different method from the author's interval Cholesky and exact LDL^T):
    lam = smallest eigenvalue of A at 50 digits (mpmath); eps = max(0, -lam) + 1e-30;
    Cholesky R of A + eps I at 60 digits, rounded to exact binary rationals; exact residual
    E = A + eps I - R R^T; Gershgorin g = min_i (E_ii - sum_{j!=i} |E_ij|) is a rigorous lower
    bound on lam_min(E).  Then A = R R^T + E - eps I >= (g - eps) I, and on R
    x^T A x >= min(0, g - eps) * sum_k vmax_k^2.
    Bound = const + inner + min(0, g - eps) * sum vmax^2  (exact rational).
    python3 verify_leaves.py <name> <tag>
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../..'))
import itertools
import json
import os
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp

sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow")
sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow/ext")
import pf_model as pm  # noqa: E402  (row order only)
import leafcut as lc  # noqa: E402   (plane list only, compared with the own enumeration)
import own_relax as orl  # noqa: E402

LOGS = _REPRO_ROOT + "/research-20260929/open-instances-wave3/powerflow/ext/logs"
N, L = 1, 29


def leaf_data(R):
    """b, Pg, Qg (OSIL indices) from the own rows of line N-L and the bus-L balance rows"""
    rows = R["rows"]
    eN, fN, eL, fL = 2 * N, 2 * N + 1, 2 * L, 2 * L + 1
    touchL = {nm: r for nm, r in rows.items() if any(eL in ij or fL in ij for ij in r["Q"])}
    flows = {nm: r for nm, r in touchL.items() if r["lin"] and r["lb"] == r["ub"] == 0}
    assert len(flows) == 4
    b = qflow = None
    pflows = []
    for nm, r in flows.items():
        (y, cy), = r["lin"].items()
        assert cy == 1
        Q = r["Q"]                                     # y = -x^T Q x
        if (eL, eL) in Q:
            if Q.get((eL, eL)) is not None and set(Q) == {(eL, eL), (fL, fL), (eN, eL), (fN, fL)}:
                bb = -Q[(eL, eL)]
                assert Q == {(eL, eL): -bb, (fL, fL): -bb, (eN, eL): bb, (fN, fL): bb}
                b, qflow = bb, y                       # y = b (W_LL - w_R)
        elif set(Q) == {(eN, fL), (fN, eL)}:
            c = -Q[(eN, fL)]
            assert -Q[(fN, eL)] == -c                   # y = c (e_N f_L - f_N e_L) = c w_I
            pflows.append((y, c))
    assert b is not None and b > 0 and len(pflows) == 2
    Pg = Qg = None
    for nm, r in rows.items():
        if not r["Q"] and not r["qy"] and len(r["lin"]) == 2 and r["lb"] == r["ub"] == 0:
            (y1, c1), (y2, c2) = r["lin"].items()
            for (yf, cf), (yg, cg) in (((y1, c1), (y2, c2)), ((y2, c2), (y1, c1))):
                if cf == 1 and cg == -1:
                    if yf == qflow:
                        Qg = yg
                    for yp, c in pflows:
                        if yf == yp and yg in R["obj"]["lin"]:
                            assert abs(c) == b
                            Pg = yg
    assert Pg is not None and Qg is not None
    # voltage bounds of bus L
    if R["info"]["polar"]:
        vr = rows[f"V{L}"]
        s_lo, s_hi = vr["lb"], vr["ub"]
    else:
        vrs = [r for r in touchL.values() if not r["lin"] and set(r["Q"]) == {(eL, eL), (fL, fL)}]
        s_lo = max(r["lb"] for r in vrs if r["lb"] is not None)
        s_hi = min(r["ub"] for r in vrs if r["ub"] is not None)
    return dict(b=b, Pg=Pg, Qg=Qg, root=(R["ybox"][Pg], R["ybox"][Qg], (s_lo, s_hi)))


def Fval(b, p, q, s):
    return s - 2 * q / b + (q * q + p * p) / (b * b * s)


def own_planes(b, box):
    """all planes through 4 affinely independent vertices with H >= F at all 8 vertices"""
    (p1, p2), (q1, q2), (s1, s2) = box
    V = [(p, q, s, Fval(b, p, q, s)) for p in (p1, p2) for q in (q1, q2) for s in (s1, s2)]
    out = set()
    for quad in itertools.combinations(V, 4):
        # solve [p q s 1] (al be ga de)^T = F by Cramer's rule (exact)
        Mx = [[t[0], t[1], t[2], Fr(1)] for t in quad]
        d = det4(Mx)
        if d == 0:
            continue
        sol = []
        for c in range(4):
            Mc = [row[:c] + [t[3]] + row[c + 1:] for row, t in zip(Mx, quad)]
            sol.append(det4(Mc) / d)
        H = tuple(sol)
        if all(H[0] * p + H[1] * q + H[2] * s + H[3] >= f for (p, q, s, f) in V):
            out.add(H)
    return sorted(out)


def det4(M):
    # Laplace expansion (exact)
    def det(m):
        if len(m) == 1:
            return m[0][0]
        return sum((-1) ** c * m[0][c] * det([r[:c] + r[c + 1:] for r in m[1:]]) for c in range(len(m)))
    return det(M)


def node_rows(R, M, ld, box):
    base = [R["rows"][r["name"]] if r["kind"] != "angle" else
            dict(lin={}, Q=dict(r["Q"]), qy={}, lb=r["lb"], ub=r["ub"]) for r in M["rows"]]
    (p1, p2), (q1, q2), (s1, s2) = box
    extra = [dict(lin={}, Q={(2 * L, 2 * L): Fr(1), (2 * L + 1, 2 * L + 1): Fr(1)}, qy={}, lb=s1, ub=s2)]
    planes = own_planes(ld["b"], box)
    info = lc.leaf_info(M)
    assert info["b"] == ld["b"] and info["Pg"] == ld["Pg"] and info["Qg"] == ld["Qg"]
    theirs = lc.planes3(info, box)
    assert planes == theirs, "plane lists differ"
    # validity: H >= F at all 8 vertices (exact); F convex on s > 0 (perspective), box = hull(vertices)
    assert s1 > 0
    for (al, be, ga, de) in planes:
        for p in (p1, p2):
            for q in (q1, q2):
                for s in (s1, s2):
                    assert al * p + be * q + ga * s + de >= Fval(ld["b"], p, q, s)
        Q = {(2 * N, 2 * N): Fr(1), (2 * N + 1, 2 * N + 1): Fr(1)}
        if ga != 0:
            Q[(2 * L, 2 * L)] = -ga
            Q[(2 * L + 1, 2 * L + 1)] = -ga
        lin = {}
        if al != 0:
            lin[ld["Pg"]] = -al
        if be != 0:
            lin[ld["Qg"]] = -be
        extra.append(dict(lin=lin, Q=Q, qy={}, lb=None, ub=de))
    ybox = dict(R["ybox"])
    ybox[ld["Pg"]] = (p1, p2)
    ybox[ld["Qg"]] = (q1, q2)
    return base + extra, ybox, len(planes)


def lagrangian(R, rows, ybox, raw):
    assert len(rows) == len(raw)
    const = R["obj"]["const"]
    kap = {y: R["obj"]["lin"].get(y, Fr(0)) for y in R["ys"]}
    sig = {y: R["obj"]["qy"].get(y, Fr(0)) for y in R["ys"]}
    n2 = 2 * R["n"]
    A = [[Fr(0)] * n2 for _ in range(n2)]
    clipped = 0
    for r, rv in zip(rows, raw):
        if rv[0] == "eq":
            assert r["lb"] is not None and r["lb"] == r["ub"]
            w = Fr(rv[1])
            const -= w * r["lb"]
        else:
            assert rv[0] == "ineq"
            mp_ = Fr(rv[1]) if rv[1] is not None else Fr(0)
            mm_ = Fr(rv[2]) if rv[2] is not None else Fr(0)
            clipped += (mp_ < 0) + (mm_ < 0)
            mp_, mm_ = max(mp_, Fr(0)), max(mm_, Fr(0))
            assert mp_ == 0 or r["ub"] is not None
            assert mm_ == 0 or r["lb"] is not None
            if mp_:
                const -= mp_ * r["ub"]
            if mm_:
                const += mm_ * r["lb"]
            w = mp_ - mm_
        if w == 0:
            continue
        for y, c in r["lin"].items():
            kap[y] += w * c
        for y, c in r["qy"].items():
            sig[y] += w * c
        for (i, j), c in r["Q"].items():
            if i == j:
                A[i][i] += w * c
            else:
                A[i][j] += w * c / 2
                A[j][i] += w * c / 2
    inner = Fr(0)
    for y in R["ys"]:
        s, k = sig[y], kap[y]
        assert s >= 0, ("negative sigma", y)
        bx = ybox.get(y)
        if bx is not None:
            l, u = bx
            assert l is not None and u is not None
            cands = [l, u]
            if s > 0:
                t = -k / (2 * s)
                if l < t < u:
                    cands.append(t)
            inner += min(s * t * t + k * t for t in cands)
        else:
            if s == 0:
                assert k == 0, ("unbounded y", y)
            else:
                inner += -k * k / (4 * s)
    return const, inner, A, clipped


def mpf_to_fr(x):
    sign, man, exp, bc = x._mpf_
    v = Fr(int(man)) * (Fr(2) ** exp)
    return -v if sign else v


def psd_shift(A):
    """rigorous lower bound (exact rational, <= 0 reported as is) on lambda_min(A)"""
    n = len(A)
    with mp.workdps(50):
        Am = mp.matrix([[mp.mpf(a.numerator) / a.denominator for a in row] for row in A])
        ev = mp.eigsy(Am, eigvals_only=True)
        lam = min(ev)
    eps = max(Fr(0), -mpf_to_fr(lam)) + Fr(1, 10 ** 30)
    with mp.workdps(60):
        B = mp.matrix([[mp.mpf(A[i][j].numerator) / A[i][j].denominator + (mp.mpf(eps.numerator) / eps.denominator if i == j else 0)
                        for j in range(n)] for i in range(n)])
        Rm = mp.cholesky(B)
        Rf = [[mpf_to_fr(Rm[i, j]) if j <= i else Fr(0) for j in range(n)] for i in range(n)]
    g = None
    for i in range(n):
        Ei = []
        for j in range(n):
            s = A[i][j] + (eps if i == j else 0)
            s -= sum(Rf[i][k] * Rf[j][k] for k in range(min(i, j) + 1))
            Ei.append(s)
        gi = Ei[i] - sum(abs(Ei[j]) for j in range(n) if j != i)
        g = gi if g is None else min(g, gi)
    return g - eps, float(lam), eps


def cover(root, boxes):
    for bx in boxes:
        for d in range(3):
            assert root[d][0] <= bx[d][0] < bx[d][1] <= root[d][1]
    cuts = [sorted({root[d][0], root[d][1]} | {bx[d][e] for bx in boxes for e in (0, 1)}) for d in range(3)]
    ncell = 0
    for i0 in range(len(cuts[0]) - 1):
        for i1 in range(len(cuts[1]) - 1):
            for i2 in range(len(cuts[2]) - 1):
                cell = [(cuts[0][i0], cuts[0][i0 + 1]), (cuts[1][i1], cuts[1][i1 + 1]), (cuts[2][i2], cuts[2][i2 + 1])]
                k = sum(all(bx[d][0] <= cell[d][0] and cell[d][1] <= bx[d][1] for d in range(3)) for bx in boxes)
                assert k == 1, (cell, k)
                ncell += 1
    return ncell


def main(name, tag):
    t0 = time.time()
    D = json.load(open(os.path.join(LOGS, f"{name}.{tag}.json")))
    R = orl.build(name)
    M = pm.decode(name)
    ld = leaf_data(R)
    root = ld["root"]
    print(f"== {name} [{tag}]: b = {ld['b']} ({float(ld['b'])}); Pg x{ld['Pg']+1} Qg x{ld['Qg']+1}; root box "
          f"{[(str(a), str(c)) for a, c in root]}")
    boxes = [tuple((Fr(a), Fr(c)) for a, c in lf["box"]) for lf in D["leaves"]]
    nc = cover(root, boxes)
    print(f"  coverage: {len(boxes)} leaves, {nc} grid cells, each in exactly one leaf box: ok")
    vm2 = sum(R["vmax2"])
    results = []
    for lf, bx in zip(D["leaves"], boxes):
        t = time.time()
        assert lf["raw"] is not None, "leaf without stored multipliers"
        rows, ybox, npl = node_rows(R, M, ld, bx)
        const, inner, A, clipped = lagrangian(R, rows, ybox, lf["raw"])
        shift, lam, eps = psd_shift(A)
        bound = const + inner + min(Fr(0), shift) * vm2
        stored = Fr(lf["bound"])
        results.append((bx, bound, stored))
        print(f"  leaf {[[round(float(a), 6), round(float(c), 6)] for a, c in bx]} planes {npl}: lam_min(A) {lam:.3e}, "
              f"rigorous shift {float(shift):.3e}; own bound {float(bound)!r}; stored {float(stored)!r}; "
              f"own - stored {float(bound - stored):.2e}; clipped negative ineq duals {clipped}; {time.time()-t:.0f}s")
    LB = min(b for _, b, _ in results)
    LBs = min(s for _, _, s in results)
    print(f"  own minimum over leaves {float(LB)!r}; stored LB {float(Fr(D['LB_exact'])) if 'LB_exact' in D else D['LB']!r}; "
          f"own - stored minimum {float(LB - LBs):.2e}")
    k12 = LB.numerator * 10 ** 12 // LB.denominator
    print(f"  floor(own minimum * 1e12) = {k12}; stored minimum floor = {LBs.numerator * 10**12 // LBs.denominator}")
    print(f"  total {time.time()-t0:.0f}s")
    return LB, results


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
