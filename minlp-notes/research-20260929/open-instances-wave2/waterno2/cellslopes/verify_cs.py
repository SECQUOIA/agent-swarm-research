"""Exact recomputation of a cell-slope separator-branching certificate.

Checks (no planning code is used; the state is read as plain data):
  1. terminal row re-derived exactly (sepbranch/terminal.derive), printed;
  2. for every link the cells form a binary split tree whose root is the link's
     level box (sepbranch/core.level_box) and whose leaves are the state's
     leaves; each split replaces [lo, hi] by [lo, m], [m, hi] in one coordinate
     with lo < m < hi, so the leaves cover the level box;
  3. every leaf has ONE slope vector (st.lam[link][leaf]); it is used for the
     exit term of period `link` and the entry term of period `link + 1`;
  4. for every leaf pair (D, D') of period t a record r of period t is chosen
     (largest float value) among the records whose stored entry / exit boxes
     CONTAIN D and D' (float comparisons, exact); mu = 0; its bound B_r is
     finite or +inf with status infeasible/empty.  The pair bound is, exactly,
        B_r + sum_k min(d_k lo_k, d_k hi_k) + sum_k min(-d'_k lo'_k, -d'_k hi'_k),
     d = l_D - a_in(r), d' = l_D' - a_out(r), [lo, hi] = D, [lo', hi'] = D'
     (+inf if B_r = +inf);
  5. exact shortest path over these pair bounds, rounded down to 9 decimals.
Optional: 6. at known feasible points (MINLPLib .sol files) the period
Lagrangian value with the leaf slopes is >= the pair bound of the leaves that
contain the point's link levels (a necessary condition; catches sign errors).

usage: python3 verify_cs.py state.pkl implied.json out.json [point.sol ...]
"""
import json
import math
import os
import pickle
import sys
from fractions import Fraction as F

import numpy as np

import gzip
import cs  # noqa: F401  (unpickling the state)
import core
import terminal

INF = math.inf


def main():
    path, implied, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    sols = sys.argv[4:]
    st = pickle.load(gzip.open(path, "rb") if path.endswith(".gz") else open(path, "rb"))
    T = st.T
    D = core.setup(T, implied)
    coef, const = terminal.derive(D)
    print("terminal row (exact):", {D["M"]["names"][j]: str(v) for j, v in coef.items()}, ">=", const)
    # 2. trees
    for link in range(T - 1):
        lo, hi = core.level_box(D, link)
        cells = st.cells[link]
        assert cells[0]["lo"] == list(map(float, lo)) and cells[0]["hi"] == list(map(float, hi)), link
        assert cells[0]["parent"] is None
        leaves, stack = [], [0]
        while stack:
            cid = stack.pop()
            c = cells[cid]
            if c["split"] is None:
                leaves.append(cid)
                continue
            k, m, c1, c2 = c["split"]
            assert c["lo"][k] < m < c["hi"][k]
            a, b = cells[c1], cells[c2]
            assert a["parent"] == cid and b["parent"] == cid
            for j in range(3):
                if j == k:
                    assert a["lo"][j] == c["lo"][j] and a["hi"][j] == m
                    assert b["lo"][j] == m and b["hi"][j] == c["hi"][j]
                else:
                    assert a["lo"][j] == b["lo"][j] == c["lo"][j]
                    assert a["hi"][j] == b["hi"][j] == c["hi"][j]
            stack += [c1, c2]
        assert sorted(leaves) == sorted(st.leaves[link]) and len(set(leaves)) == len(leaves), link
    print("cell trees ok; leaves per link:", [len(l) for l in st.leaves])
    # 3. slopes: one finite vector per leaf
    for link in range(T - 1):
        for cid in st.leaves[link]:
            v = st.lam[link][cid]
            assert len(v) == 3 and all(isinstance(x, float) and math.isfinite(x) for x in v)
    nslopes = [len({tuple(st.lam[l][c]) for c in st.leaves[l]}) for l in range(T - 1)]
    print("distinct slope vectors per link:", nslopes)

    # leaves under each tree node
    def under(link):
        pos = {cid: i for i, cid in enumerate(st.leaves[link])}
        out = {}

        def rec(cid):
            c = st.cells[link][cid]
            r = [pos[cid]] if c["split"] is None else rec(c["split"][2]) + rec(c["split"][3])
            out[cid] = r
            return r
        rec(0)
        return out
    U = [under(l) for l in range(T - 1)]
    box = [(np.array([st.cells[l][c]["lo"] for c in st.leaves[l]]), np.array([st.cells[l][c]["hi"] for c in st.leaves[l]]))
           for l in range(T - 1)]
    lam = [np.array([st.lam[l][c] for c in st.leaves[l]]) for l in range(T - 1)]
    # 4. choose a record per leaf pair (float), then exact value
    best = [np.full((1 if t == 0 else len(st.leaves[t - 1]), 1 if t == T - 1 else len(st.leaves[t])), -INF)
            for t in range(T)]
    brid = [np.full(b.shape, -1, int) for b in best]
    for rid, rec in enumerate(st.recs):
        t = rec["t"]
        assert rec.get("mu", 0.0) == 0.0
        b = rec["bound"]
        assert not (b != b) and b != -INF
        if b == INF:
            assert rec["status"] in ("infeasible", "empty")
        rows = [0] if t == 0 else U[t - 1][rec["cin"]]
        cols = [0] if t == T - 1 else U[t][rec["cout"]]
        # containment of leaf boxes in the record's boxes
        if t > 0:
            blo, bhi = np.array(rec["cin_box"][0]), np.array(rec["cin_box"][1])
            ok = np.all((box[t - 1][0][rows] >= blo) & (box[t - 1][1][rows] <= bhi), axis=1)
            rows = [r for r, o in zip(rows, ok) if o]
        else:
            assert rec["cin_box"] is None
        if t < T - 1:
            blo, bhi = np.array(rec["cout_box"][0]), np.array(rec["cout_box"][1])
            ok = np.all((box[t][0][cols] >= blo) & (box[t][1][cols] <= bhi), axis=1)
            cols = [c for c, o in zip(cols, ok) if o]
        else:
            assert rec["cout_box"] is None
        if not rows or not cols:
            continue
        if b == INF:
            val = np.full((len(rows), len(cols)), INF)
        else:
            ci = np.zeros(len(rows))
            co = np.zeros(len(cols))
            if t > 0:
                d = lam[t - 1][rows] - np.array(rec["lam_in"])
                ci = np.minimum(d * box[t - 1][0][rows], d * box[t - 1][1][rows]).sum(1)
            if t < T - 1:
                d = lam[t][cols] - np.array(rec["lam_out"])
                co = np.minimum(-d * box[t][0][cols], -d * box[t][1][cols]).sum(1)
            val = b + ci[:, None] + co[None, :]
        sub = best[t][np.ix_(rows, cols)]
        better = val > sub
        if better.any():
            ri, cj = np.nonzero(better)
            best[t][np.array(rows)[ri], np.array(cols)[cj]] = val[ri, cj]
            brid[t][np.array(rows)[ri], np.array(cols)[cj]] = rid
    Bq = []
    corrected = []
    nfin = ninf = 0
    used = set()
    for t in range(T):
        Mt = []
        for r in range(best[t].shape[0]):
            row = []
            for c in range(best[t].shape[1]):
                rid = int(brid[t][r, c])
                assert rid >= 0, ("leaf pair without a record", t, r, c)
                used.add(rid)
                rec = st.recs[rid]
                b = rec["bound"]
                if b == INF:
                    row.append(None)
                    ninf += 1
                    continue
                v = F(b)
                if t > 0:
                    for k in range(3):
                        d = F(float(lam[t - 1][r, k])) - F(rec["lam_in"][k])
                        v += min(d * F(float(box[t - 1][0][r, k])), d * F(float(box[t - 1][1][r, k])))
                if t < T - 1:
                    for k in range(3):
                        d = F(float(lam[t][c, k])) - F(rec["lam_out"][k])
                        v += min(-d * F(float(box[t][0][c, k])), -d * F(float(box[t][1][c, k])))
                row.append(v)
                nfin += 1
                if v != F(b):
                    corrected.append((t, r, c, rid))
            Mt.append(row)
        Bq.append(Mt)
    print(f"leaf pairs: {nfin} finite bounds, {ninf} proved empty; records used {len(used)} of {len(st.recs)}; "
          f"{len(corrected)} finite pair bounds use a slope correction")

    # 5. exact DP with path
    def add(a, b):
        return None if a is None or b is None else a + b
    f = [(Bq[0][0][c], [c]) for c in range(len(Bq[0][0]))]
    for t in range(1, T):
        nc = len(Bq[t][0])
        g = []
        for c in range(nc):
            bv, bp = None, None
            for r in range(len(f)):
                v = add(f[r][0], Bq[t][r][c])
                if v is not None and (bv is None or v < bv):
                    bv, bp = v, f[r][1] + [c]
            g.append((bv, bp))
        f = g
    V, path = f[0]
    down = F(V.numerator * 10**9 // V.denominator, 10**9)
    print("CERTIFIED cell-slope separator-branching bound (exact):", V)
    print(f"rounded down to 9 decimals: {float(down):.9f}")
    path = path[:T - 1]
    print("minimizing path (leaf positions):", path)
    rows_out = []
    for t in range(T):
        r = 0 if t == 0 else path[t - 1]
        c = 0 if t == T - 1 else path[t]
        rid = int(brid[t][r, c])
        rec = st.recs[rid]
        ex = None if t == T - 1 else [st.cells[t][st.leaves[t][c]]["lo"], st.cells[t][st.leaves[t][c]]["hi"]]
        sl = None if t == T - 1 else st.lam[t][st.leaves[t][c]]
        print(f"  period {t}: bound {float(Bq[t][r][c]):.4f} record {rid} ({rec.get('src', 'cert3')}) "
              f"exit cell {ex and [[round(v, 3) for v in ex[0]], [round(v, 3) for v in ex[1]]]} "
              f"exit slope {sl and [round(v, 3) for v in sl]}")
        rows_out.append(dict(t=t, bound=str(Bq[t][r][c]), rid=rid, exit_cell=ex, exit_slope=sl))
    # records used by leaf pairs on paths within 0.05 of the optimum (float through-values)
    Bf = [np.array([[np.inf if v is None else float(v) for v in row] for row in Mt]) for Mt in Bq]
    ff = [None] * T
    ff[0] = Bf[0][0, :]
    for t in range(1, T - 1):
        ff[t] = (ff[t - 1][:, None] + Bf[t]).min(axis=0)
    gg = [None] * T
    gg[T - 2] = Bf[T - 1][:, 0]
    for t in range(T - 2, 0, -1):
        gg[t - 1] = (Bf[t] + gg[t][None, :]).min(axis=1)
    near = set()
    nnear = 0
    for t in range(T):
        fin = np.zeros(1) if t == 0 else ff[t - 1]
        gout = np.zeros(1) if t == T - 1 else gg[t]
        Pi = fin[:, None] + Bf[t] + gout[None, :]
        for r, c in zip(*np.nonzero(Pi <= float(V) + 0.05)):
            near.add(int(brid[t][r, c]))
            nnear += 1
    print(f"{nnear} leaf pairs lie on paths within 0.05 of the optimum; they use {len(near)} records")
    import random
    random.seed(7)

    def leafrec(t, r, c):
        rid = int(brid[t][r, c])
        return dict(t=t, r=r, c=c, rid=rid, bound=str(Bq[t][r][c]),
                    cin_box=None if t == 0 else [st.cells[t - 1][st.leaves[t - 1][r]]["lo"], st.cells[t - 1][st.leaves[t - 1][r]]["hi"]],
                    cout_box=None if t == T - 1 else [st.cells[t][st.leaves[t][c]]["lo"], st.cells[t][st.leaves[t][c]]["hi"]],
                    lam_in=[0.0, 0.0, 0.0] if t == 0 else list(st.lam[t - 1][st.leaves[t - 1][r]]),
                    lam_out=[0.0, 0.0, 0.0] if t == T - 1 else list(st.lam[t][st.leaves[t][c]]))
    leaf_checks = [dict(leafrec(t, 0 if t == 0 else path[t - 1], 0 if t == T - 1 else path[t]), group="path")
                   for t in range(T)]
    leaf_checks += [dict(leafrec(t, r, c), group="corrected") for (t, r, c, rid) in
                    random.sample(corrected, min(40, len(corrected)))]
    # 6. feasible points
    pts = []
    if sols:
        import evalpt
        M_, S_ = D["M"], D["S"]
        for sp in sols:
            x, obj = evalpt.read_sol(sp, M_["names"])
            lev = [[F(x[a]) for (i, a, b) in S_["link"][l]] for l in range(T - 1)]
            minmargin = None
            total = F(0)
            for t in range(T):
                cost = sum(F(x[v]) * F(M_["obj"][v]) for v in S_["per_vars"][t] if v in M_["obj"])
                # leaves containing the levels (any one of them; check all)
                rr = [0] if t == 0 else [i for i, cid in enumerate(st.leaves[t - 1])
                                         if all(F(st.cells[t - 1][cid]["lo"][k]) <= lev[t - 1][k] <= F(st.cells[t - 1][cid]["hi"][k]) for k in range(3))]
                cc = [0] if t == T - 1 else [i for i, cid in enumerate(st.leaves[t])
                                             if all(F(st.cells[t][cid]["lo"][k]) <= lev[t][k] <= F(st.cells[t][cid]["hi"][k]) for k in range(3))]
                assert rr and cc, ("point outside all leaves", sp, t)
                for r in rr:
                    for c in cc:
                        val = cost
                        if t > 0:
                            val += sum(F(float(lam[t - 1][r, k])) * lev[t - 1][k] for k in range(3))
                        if t < T - 1:
                            val -= sum(F(float(lam[t][c, k])) * lev[t][k] for k in range(3))
                        b = Bq[t][r][c]
                        assert b is not None, ("pair of a feasible point proved empty", sp, t)
                        m = val - b
                        assert m >= 0, ("bound above the point's period value", sp, t, float(m))
                        minmargin = m if minmargin is None else min(minmargin, m)
                total += Bq[t][rr[0]][cc[0]]
            print(f"point {os.path.basename(sp)}: f = {float(obj):.6f}; sum of pair bounds along its cells "
                  f"{float(total):.6f}; smallest margin {float(minmargin):.4f}")
            pts.append(dict(sol=os.path.basename(sp), f=float(obj), path_sum=float(total), min_margin=float(minmargin)))
    json.dump(dict(bound_exact=str(V), bound_rounded_down=f"{float(down):.9f}", leaves=[len(l) for l in st.leaves],
                   records_used=len(used), records=len(st.recs), path=path, path_rows=rows_out, points=pts,
                   distinct_slopes=nslopes, used_records=sorted(used), n_corrected=len(corrected),
                   leaf_checks=leaf_checks, near_records=sorted(near)),
              open(outp, "w"), indent=1)


if __name__ == "__main__":
    main()
