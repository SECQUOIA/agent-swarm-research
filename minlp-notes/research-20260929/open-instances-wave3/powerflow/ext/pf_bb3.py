"""Leaf branch and bound for powerflow0039p / 0039r: Shor SDP node bounds (pf_cert exact
Lagrangian certificate) plus exact envelope cuts of the leaf identity

    W_NN = F(Pg, Qg, W_LL) = W_LL - 2 Qg / b + (Qg^2 + Pg^2) / (b^2 W_LL)     (leafcut.py)

Node = box [p1,p2] x [q1,q2] x [s1,s2] for (Pg, Qg, W_LL) (bus L = 29, N = 1).  Node rows:
the Pg and Qg boxes (y boxes), s1 <= W_LL <= s2 (a voltage row), and the vertex planes
W_NN <= H(Pg, Qg, W_LL).  Children split one coordinate at an exact rational m and cover
the parent.  Node bound = max(parent bound, pf_cert certificate of the node relaxation).
The final bound is the minimum over all leaves (open and fathomed).

    python3 pf_bb3.py <name> <time_limit_s> <UB> [abs_tol] [clarabel_tol] [tag]
"""
import heapq
import json
import os
import sys
import time
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pf_cert as pc  # noqa: E402
import pf_model as pm  # noqa: E402
import leafcut as lc  # noqa: E402
from pf_primal import solve_primal, complex_W  # noqa: E402


def node_model(M, info, box):
    (p1, p2), (q1, q2), (s1, s2) = box
    MM = dict(M, ybox=dict(M["ybox"]))
    MM["ybox"][info["Pg"]] = (p1, p2)
    MM["ybox"][info["Qg"]] = (q1, q2)
    L = info["L"]
    extra = [dict(name="VBL", lin={}, Q={(2 * L, 2 * L): Fr(1), (2 * L + 1, 2 * L + 1): Fr(1)}, qy={},
                  lb=s1, ub=s2, kind="volt")]
    extra += lc.cut_rows3(info, box)
    return MM, extra


def solve_node(M, info, box, solver_kw=None):
    MM, extra = node_model(M, info, box)
    try:
        res = solve_primal(MM, None, extra, solver_kw=solver_kw)
    except Exception as e:  # solver failure: caller keeps the parent bound
        return None
    if res["W"] is None or res["status"] not in ("optimal", "optimal_inaccurate"):
        return dict(status=res["status"], bound=None)
    cert = pc.certify(dict(MM, rows=res["rows"]), res["raw"], log=lambda s: None)
    yi = {y: q for q, y in enumerate(M["ys"])}
    Wc = complex_W(M, res["W"])
    N, L = info["N"], info["L"]
    pt = dict(W_NN=Wc[N, N].real, W_LL=Wc[L, L].real, Pg=res["y"][yi[info["Pg"]]], Qg=res["y"][yi[info["Qg"]]])
    ev = np.linalg.eigvalsh(Wc)
    return dict(status=res["status"], value=res["value"], bound=None if cert is None else cert[0],
                eps=None if cert is None else cert[1], pt=pt, eig2=ev[-2], raw=res["raw"])


def choose_split(info, box, pt):
    b = float(info["b"])
    (p1, p2), (q1, q2), (s1, s2) = [(float(a), float(c)) for a, c in box]
    P = min(max(pt["Pg"], p1), p2); Q = min(max(pt["Qg"], q1), q2); S = min(max(pt["W_LL"], s1), s2)
    e = [(P - p1) * (p2 - P) / (b * b * S), (Q - q1) * (q2 - Q) / (b * b * S),
         (Q * Q + P * P) / (b * b * S ** 3) * (S - s1) * (s2 - S)]
    # also consider pure widths (in case the point sits on a face)
    w = [(p2 - p1) ** 2 / (4 * b * b * S), (q2 - q1) ** 2 / (4 * b * b * S), (Q * Q + P * P) / (b * b * S ** 3) * (s2 - s1) ** 2 / 4]
    score = [ei + 0.1 * wi for ei, wi in zip(e, w)]
    d = int(np.argmax(score))
    lo, hi = box[d]
    val = Fr([P, Q, S][d]).limit_denominator(10 ** 6)
    width = hi - lo
    m = min(max(val, lo + width / 10), hi - width / 10)
    m = Fr(m).limit_denominator(10 ** 8)
    if not lo < m < hi:
        m = (lo + hi) / 2
    return d, m


def run(name, tlim, UB, abs_tol=Fr(1, 1000), log=print, out=None, solver_kw=None):
    t0 = time.time()
    M = pm.decode(name)
    info = lc.leaf_info(M)
    box0 = ((info["plo"], info["phi"]), (info["qlo"], info["qhi"]), info["WLL"])
    r = solve_node(M, info, box0, solver_kw)
    b0 = r["bound"]
    log(f"root: bound {float(b0)!r} value {r['value']!r} ({r['status']}) pt {r['pt']} eig2 {r['eig2']:.2e}  UB {UB}")
    cnt = 0
    heap = [(float(b0), cnt, box0, b0, r)]
    done = []            # fathomed leaves: (box, bound)
    nodes = 1
    UBf = Fr(UB)
    while heap and time.time() - t0 < tlim:
        fb, _, box, bnd, rr = heapq.heappop(heap)
        if bnd >= UBf - abs_tol:
            done.append((box, bnd, rr.get("raw")))
            continue
        d, m = choose_split(info, box, rr["pt"])
        kids = []
        for part in ((box[d][0], m), (m, box[d][1])):
            kb = list(box); kb[d] = part; kb = tuple(kb)
            kr = solve_node(M, info, kb, solver_kw)
            nodes += 1
            if kr is None or kr["bound"] is None:
                st = None if kr is None else kr["status"]
                if st in ("infeasible", "infeasible_inaccurate"):
                    log(f"    child {['Pg','Qg','W_LL'][d]} {[float(x) for x in part]}: SDP {st}; kept with parent bound")
                kr = dict(rr, raw=None) if kr is None or kr.get("pt") is None else kr
                kb_bound = bnd
            else:
                kb_bound = max(bnd, kr["bound"])
            cnt += 1
            heapq.heappush(heap, (float(kb_bound), cnt, kb, kb_bound, kr))
            kids.append((part, kb_bound, kr.get("value")))
        glb = min([h[0] for h in heap] + [float(x[1]) for x in done])
        log(f"  nodes {nodes}: split {['Pg','Qg','W_LL'][d]} at {float(m):.6f} of [{float(box[d][0]):.6f},{float(box[d][1]):.6f}]"
            f" -> {[(round(float(k[1]), 5)) for k in kids]}; LB {glb!r} gap {UB-glb:.4g} open {len(heap)} t {time.time()-t0:.0f}s")
    leaves = [(h[2], h[3], h[4].get("raw")) for h in heap] + done
    LB = min(l[1] for l in leaves)
    if out:
        json.dump(dict(name=name, UB=UB, LB=float(LB), LB_exact=str(LB), nodes=nodes,
                       leaves=[dict(box=[[str(a), str(c)] for a, c in bx], bound=str(bd), raw=raw) for bx, bd, raw in leaves]),
                  open(out, "w"))
    return LB, nodes, len(heap)


if __name__ == "__main__":
    name = sys.argv[1]
    tl = float(sys.argv[2])
    UB = float(sys.argv[3])
    tol = Fr(sys.argv[4]) if len(sys.argv) > 4 else Fr(1, 1000)
    kw = None
    if len(sys.argv) > 5:
        t_ = float(sys.argv[5])
        kw = dict(tol_gap_abs=t_, tol_gap_rel=t_, tol_feas=t_, tol_ktratio=t_, max_iter=500)
    tag = sys.argv[6] if len(sys.argv) > 6 else "bb3"
    out = os.path.join(HERE, "logs", f"{name}.{tag}.json")
    os.makedirs(os.path.join(HERE, "logs"), exist_ok=True)
    LB, nodes, nopen = run(name, tl, UB, tol, out=out, solver_kw=kw)
    k12 = int(LB * 10**12)                          # floor: LB >= k12 / 10^12
    assert Fr(k12, 10**12) <= LB
    print(f"FINAL {name}: certified LB {float(LB)!r} (rational bound {k12}/10^12 <= LB) nodes {nodes} open {nopen}")
