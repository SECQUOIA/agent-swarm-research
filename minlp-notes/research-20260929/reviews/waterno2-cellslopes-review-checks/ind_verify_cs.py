"""Independent re-check of a cell-slope certificate for waterno2_06 (own code).

The pickle is read through a stub class (load_cs.py); no author code is
imported.  The model comes from the first verifier's vmodel; the implied
bounds from the first verifier's my_implied_06.json.

Checks
  1. records: period, mu = 0, boxes present exactly on the sides that exist,
     lo <= hi, bound not NaN / -inf, +inf only with status infeasible/empty,
     slopes finite floats (lam_in unused for t = 0, lam_out unused for t = 5;
     reported if nonzero);
  2. level box of each link (OSIL bounds of both copies and the first
     verifier's implied bounds, exact) lies inside the root cell; the leaves
     lie in the root and partition it (elementary-cell sweep over all leaf
     breakpoints; independent of the split tree); every leaf has positive width;
  3. one finite slope vector per leaf; the SAME array LAM[l] is used for the
     exit term of period l and the entry term of period l+1 (by construction
     below);
  4. every leaf pair (D, D') of period t: among ALL records of period t whose
     stored boxes contain D and D' (box comparison, not the tree), the one with
     the largest float value of  B_r + corr  is chosen (ties: smallest rid); the
     pair bound is then evaluated EXACTLY:
        B_r + sum_k min(d_k lo_k, d_k hi_k) + sum_k min(-d'_k lo'_k, -d'_k hi'_k),
        d = l_D - a_in(r),  d' = l_D' - a_out(r);  +inf if B_r = +inf;
  5. shortest path in Fraction arithmetic; path; records used; leaf pairs and
     records on paths within 0.05 and 0.5 of the optimum.

usage: python3 ind_verify_cs.py cert.pkl.gz out.json [authors_verify.json]
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import math
import sys
import time
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel  # noqa: E402
import load_cs  # noqa: E402

T = 6
INF = math.inf
IMPLIED = _RESEARCH + "/reviews/waterno2-verification/logs/my_implied_06.json"


def level_box(I, link, implied):
    m = I["m"]
    names = m["names"]
    lo, hi = [], []
    for (i, a, b) in I["links"][link]:
        l, h = None, None
        for v in (a, b):
            lv, hv = F(m["lb"][v]), F(m["ub"][v])
            if names[v] in implied:
                lv = max(lv, F(implied[names[v]][0]))
                hv = min(hv, F(implied[names[v]][1]))
            l = lv if l is None else max(l, lv)
            h = hv if h is None else min(h, hv)
        lo.append(l)
        hi.append(h)
    return lo, hi


def sweep(root_lo, root_hi, leaves):
    for lo, hi in leaves:
        for k in range(3):
            assert root_lo[k] <= lo[k] < hi[k] <= root_hi[k], ("leaf outside root or degenerate", lo, hi)
    bps = []
    for k in range(3):
        s = sorted({root_lo[k], root_hi[k]} | {l[0][k] for l in leaves} | {l[1][k] for l in leaves})
        bps.append(s)
    shape = tuple(len(s) - 1 for s in bps)
    hit = np.zeros(shape, dtype=np.int32)
    idx = [{v: j for j, v in enumerate(s)} for s in bps]
    for lo, hi in leaves:
        hit[tuple(slice(idx[k][lo[k]], idx[k][hi[k]]) for k in range(3))] += 1
    return int(hit.min()), int(hit.max()), shape


def corr_exact(lam_leaf, a, lo, hi, sign):
    """exact min over the box [lo, hi] of sign * (lam_leaf - a) . y"""
    v = F(0)
    for k in range(3):
        d = sign * (F(lam_leaf[k]) - F(a[k]))
        v += min(d * F(lo[k]), d * F(hi[k]))
    return v


def main():
    pkl, outp = sys.argv[1], sys.argv[2]
    tic = time.time()
    d = load_cs.load(pkl)
    assert d["T"] == T
    I = vmodel.instance(T)
    implied = json.load(open(IMPLIED))
    implied = implied.get("bounds", implied)
    cells, leaves, lamd, recs = d["cells"], d["leaves"], d["lam"], d["recs"]
    rep = {}
    # ---------------------------------------------------------------- 1 records
    nz_unused = 0
    for rid, r in enumerate(recs):
        t = r["t"]
        assert 0 <= t < T
        assert r["mu"] == 0.0
        b = r["bound"]
        assert isinstance(b, float) and b == b and b != -INF, rid
        if b == INF:
            assert r["status"] in ("infeasible", "empty"), rid
        assert (r["cin_box"] is None) == (t == 0), rid
        assert (r["cout_box"] is None) == (t == T - 1), rid
        for box in (r["cin_box"], r["cout_box"]):
            if box is not None:
                assert len(box[0]) == 3 and len(box[1]) == 3
                assert all(float(box[0][k]) <= float(box[1][k]) for k in range(3)), rid
        for v in list(r["lam_in"]) + list(r["lam_out"]):
            assert math.isfinite(float(v))
        if (t == 0 and any(float(v) != 0.0 for v in r["lam_in"])) or \
                (t == T - 1 and any(float(v) != 0.0 for v in r["lam_out"])):
            nz_unused += 1
    print(f"1. {len(recs)} records: fields ok; records with a nonzero unused slope side: {nz_unused}")
    rep["records"] = len(recs)
    rep["nonzero_unused_side"] = nz_unused
    # ---------------------------------------------------------------- 2 coverage
    LO, HI, LAM = [], [], []
    for l in range(T - 1):
        lo, hi = level_box(I, l, implied)
        root = cells[l][0]
        assert root["parent"] is None
        assert all(F(root["lo"][k]) <= lo[k] and hi[k] <= F(root["hi"][k]) for k in range(3)), (l, root, lo, hi)
        lv = [(cells[l][c]["lo"], cells[l][c]["hi"]) for c in leaves[l]]
        assert len(set(leaves[l])) == len(leaves[l])
        mn, mx, shape = sweep(root["lo"], root["hi"], lv)
        assert mn == 1 and mx == 1, (l, mn, mx)
        print(f"2. link {l}: level box lo={[float(v) for v in lo]} hi={[float(v) for v in hi]} inside root "
              f"lo={root['lo']} hi={root['hi']}; {len(lv)} leaves partition the root (grid {shape})")
        LO.append(np.array([cells[l][c]["lo"] for c in leaves[l]], float))
        HI.append(np.array([cells[l][c]["hi"] for c in leaves[l]], float))
        # ------------------------------------------------------------ 3 slopes
        vs = [lamd[l][c] for c in leaves[l]]
        for v in vs:
            assert len(v) == 3 and all(isinstance(x, float) and math.isfinite(x) for x in v)
        LAM.append(np.array(vs, float))
    rep["leaves"] = [len(l) for l in leaves]
    rep["distinct_slopes"] = [len({tuple(v) for v in LAM[l].tolist()}) for l in range(T - 1)]
    print("3. one slope vector per leaf; distinct per link:", rep["distinct_slopes"])
    # ---------------------------------------------------------------- 4 records per leaf pair
    nr = [1] + [len(leaves[t - 1]) for t in range(1, T)]
    nc = [len(leaves[t]) for t in range(T - 1)] + [1]
    best = [np.full((nr[t], nc[t]), -INF) for t in range(T)]
    brid = [np.full((nr[t], nc[t]), -1, int) for t in range(T)]
    for rid, r in enumerate(recs):
        t = r["t"]
        if t > 0:
            blo, bhi = np.array(r["cin_box"][0], float), np.array(r["cin_box"][1], float)
            rows = np.nonzero(np.all((LO[t - 1] >= blo) & (HI[t - 1] <= bhi), axis=1))[0]
        else:
            rows = np.array([0])
        if t < T - 1:
            blo, bhi = np.array(r["cout_box"][0], float), np.array(r["cout_box"][1], float)
            cols = np.nonzero(np.all((LO[t] >= blo) & (HI[t] <= bhi), axis=1))[0]
        else:
            cols = np.array([0])
        if len(rows) == 0 or len(cols) == 0:
            continue
        b = r["bound"]
        if b == INF:
            val = np.full((len(rows), len(cols)), INF)
        else:
            ci = np.zeros(len(rows))
            co = np.zeros(len(cols))
            if t > 0:
                dd = LAM[t - 1][rows] - np.array(r["lam_in"], float)
                ci = np.minimum(dd * LO[t - 1][rows], dd * HI[t - 1][rows]).sum(1)
            if t < T - 1:
                dd = LAM[t][cols] - np.array(r["lam_out"], float)
                co = np.minimum(-dd * LO[t][cols], -dd * HI[t][cols]).sum(1)
            val = b + ci[:, None] + co[None, :]
        sub = best[t][np.ix_(rows, cols)]
        better = val > sub
        if better.any():
            ri, cj = np.nonzero(better)
            best[t][rows[ri], cols[cj]] = val[ri, cj]
            brid[t][rows[ri], cols[cj]] = rid
    Bq = []
    used = set()
    nfin = ninf = ncorr = 0
    for t in range(T):
        M = []
        for rr in range(nr[t]):
            row = []
            for cc in range(nc[t]):
                rid = int(brid[t][rr, cc])
                assert rid >= 0, ("leaf pair without a containing record", t, rr, cc)
                used.add(rid)
                r = recs[rid]
                if r["bound"] == INF:
                    row.append(None)
                    ninf += 1
                    continue
                v = F(r["bound"])
                if t > 0:
                    v += corr_exact(LAM[t - 1][rr].tolist(), r["lam_in"], LO[t - 1][rr].tolist(),
                                    HI[t - 1][rr].tolist(), 1)
                if t < T - 1:
                    v += corr_exact(LAM[t][cc].tolist(), r["lam_out"], LO[t][cc].tolist(),
                                    HI[t][cc].tolist(), -1)
                if v != F(r["bound"]):
                    ncorr += 1
                row.append(v)
                nfin += 1
            M.append(row)
        Bq.append(M)
    print(f"4. leaf pairs: {nfin} finite, {ninf} +inf; {ncorr} finite pair bounds differ from their record bound "
          f"(Lemma-2 correction); records used {len(used)} of {len(recs)}  [{time.time()-tic:.0f}s]")
    rep.update(finite=nfin, infinite=ninf, corrected=ncorr, used=len(used))

    # ---------------------------------------------------------------- 5 exact DP
    def add(a, b):
        return None if a is None or b is None else a + b
    f = [(Bq[0][0][c], [c]) for c in range(nc[0])]
    for t in range(1, T):
        g = []
        for c in range(nc[t]):
            bv, bp = None, None
            for r_ in range(nr[t]):
                v = add(f[r_][0], Bq[t][r_][c])
                if v is not None and (bv is None or v < bv):
                    bv, bp = v, f[r_][1] + [c]
            g.append((bv, bp))
        f = g
    V, path = f[0]
    down = F(V.numerator * 10**9 // V.denominator, 10**9)
    path = path[:T - 1]
    print(f"5. exact DP value {V} = {float(V)!r}; rounded down {float(down):.9f}; path {path}")
    rep.update(value=str(V), rounded_down=f"{float(down):.9f}", path=path)
    prow = []
    for t in range(T):
        rr = 0 if t == 0 else path[t - 1]
        cc = 0 if t == T - 1 else path[t]
        rid = int(brid[t][rr, cc])
        prow.append(dict(t=t, r=rr, c=cc, rid=rid, bound=str(Bq[t][rr][cc]), rec_bound=recs[rid]["bound"],
                         src=str(recs[rid]["src"]),
                         exit_cell=None if t == T - 1 else [LO[t][cc].tolist(), HI[t][cc].tolist()],
                         exit_slope=None if t == T - 1 else LAM[t][cc].tolist()))
        print(f"   period {t}: pair bound {float(Bq[t][rr][cc]):.4f}, record {rid} {recs[rid]['src']} "
              f"rec bound {recs[rid]['bound']:.4f}")
    rep["path_rows"] = prow
    # near-optimal leaf pairs (float through-values)
    Bf = [np.array([[INF if v is None else float(v) for v in row] for row in M]) for M in Bq]
    ff = [None] * T
    ff[0] = Bf[0][0, :]
    for t in range(1, T - 1):
        ff[t] = (ff[t - 1][:, None] + Bf[t]).min(axis=0)
    gg = [None] * T
    gg[T - 2] = Bf[T - 1][:, 0]
    for t in range(T - 2, 0, -1):
        gg[t - 1] = (Bf[t] + gg[t][None, :]).min(axis=1)
    near = {}
    crit = {}
    for t in range(T):
        fin_ = np.zeros(1) if t == 0 else ff[t - 1]
        go = np.zeros(1) if t == T - 1 else gg[t]
        Pi = fin_[:, None] + Bf[t] + go[None, :]
        for (rr, cc), v in np.ndenumerate(Pi):
            rid = int(brid[t][rr, cc])
            crit[rid] = min(crit.get(rid, INF), float(v) - float(V))
            if v <= float(V) + 0.5:
                near[(t, rr, cc)] = float(v) - float(V)
    rep["near_pairs_0.5"] = [dict(t=t, r=rr, c=cc, rid=int(brid[t][rr, cc]), excess=e,
                                  bound=str(Bq[t][rr][cc])) for (t, rr, cc), e in sorted(near.items())]
    rep["used_records"] = sorted(used)
    rep["crit"] = {str(k): v for k, v in crit.items()}
    n005 = {int(brid[t][rr, cc]) for (t, rr, cc), e in near.items() if e <= 0.05}
    n05 = {int(brid[t][rr, cc]) for (t, rr, cc), e in near.items()}
    print(f"   leaf pairs within 0.05: {sum(1 for e in near.values() if e <= 0.05)} ({len(n005)} records); "
          f"within 0.5: {len(near)} ({len(n05)} records)")
    rep["brid"] = [b.tolist() for b in brid]
    if len(sys.argv) > 3:
        A = json.load(open(sys.argv[3]))
        same_val = A["bound_exact"] == str(V)
        au = set(A["used_records"])
        print(f"   authors' exact value {A['bound_exact']}: {'identical' if same_val else 'DIFFERENT'}; "
              f"used-record sets: authors {len(au)}, mine {len(used)}, common {len(au & used)}")
        rep["authors_same_value"] = same_val
        rep["authors_used_diff"] = [sorted(au - used), sorted(used - au)]
    json.dump(rep, open(outp, "w"))
    print(f"done in {time.time()-tic:.0f}s")


if __name__ == "__main__":
    main()
