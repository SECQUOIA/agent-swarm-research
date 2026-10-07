"""Exact recomputation of a separator-branching certificate (certify_dp.py state).

Checks:
  1. the terminal row is re-derived exactly (terminal.derive) and printed;
  2. for every link the cells form a binary tree rooted at the level box of the
     link (core.level_box); each split replaces [lo, hi] by [lo, m] and [m, hi]
     in one coordinate with lo < m < hi, so the leaves cover the box;
  3. for every period and every pair of current leaves, the bound used comes
     from a certification record of that period whose entry and exit cells are
     ancestors of (or equal to) the pair's cells, whose stored boxes equal those
     cells, and whose slopes are the plan's slopes of links t-1 and t, mu >= 0;
  4. the shortest path  mu*c + min over leaf sequences of sum_t bound_t  is
     recomputed in exact rational arithmetic and rounded down to 9 decimals.

The pair bounds are rbb.solve results; they are not recomputed here
(crosscheck_pairs.py re-bounds a sample with independent code).

usage: python3 verify.py cert_config.json
"""
import json
import pickle
import sys
from fractions import Fraction

import numpy as np

import core
import terminal
from dpcells import CellPlan  # noqa: F401  (unpickling)


def main():
    cfg = json.load(open(sys.argv[1]))
    T = cfg["T"]
    P = pickle.load(open(cfg["out"] + ".pkl", "rb"))
    D = core.setup(T, cfg["implied"])
    coef, const = terminal.derive(D)
    print("terminal row (exact):", {D["M"]["names"][j]: str(v) for j, v in coef.items()}, ">=", const)
    assert P.mu >= 0
    # 2. cell trees
    for link in range(T - 1):
        lo, hi = core.level_box(D, link)
        cells = P.cells[link]
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
        assert sorted(leaves) == sorted(P.leaves[link]) and len(set(leaves)) == len(leaves), link
    print("cell trees ok; leaves per link:", [len(l) for l in P.leaves])

    def anc(link, cid):
        out = set()
        while cid is not None:
            out.add(cid)
            cid = P.cells[link][cid]["parent"]
        return out

    # 3. bounds of all leaf pairs
    Bq = []
    used = set()
    stat = dict(finite=0, inf=0)
    for t in range(T):
        rows = [-1] if t == 0 else P.leaves[t - 1]
        cols = [-1] if t == T - 1 else P.leaves[t]
        assert P.tables["CB"][t].shape == (len(rows), len(cols))
        ar = [{-1} if t == 0 else anc(t - 1, cid) for cid in rows]
        ac = [{-1} if t == T - 1 else anc(t, cid) for cid in cols]
        lin, lout = P.slopes(t)
        Mt = []
        for r in range(len(rows)):
            row = []
            for c in range(len(cols)):
                rid = int(P.tables["CSRC"][t][r, c])
                assert rid >= 0, ("pair without certificate", t, r, c)
                rec = P.crecs[rid]
                used.add(rid)
                assert rec["t"] == t and rec["cin"] in ar[r] and rec["cout"] in ac[c]
                if t > 0:
                    assert rec["lam_in"] == lin
                    cc = P.cells[t - 1][rec["cin"]]
                    assert [list(rec["cin_box"][0]), list(rec["cin_box"][1])] == [cc["lo"], cc["hi"]]
                else:
                    assert rec["cin_box"] is None
                if t < T - 1:
                    assert rec["lam_out"] == lout
                    cc = P.cells[t][rec["cout"]]
                    assert [list(rec["cout_box"][0]), list(rec["cout_box"][1])] == [cc["lo"], cc["hi"]]
                else:
                    assert rec["cout_box"] is None
                assert rec["mu"] == P.mu
                assert float(P.tables["CB"][t][r, c]) == rec["bound"]
                b = rec["bound"]
                assert b != -np.inf
                if np.isfinite(b):
                    row.append(Fraction(b))
                    stat["finite"] += 1
                else:
                    assert b == np.inf and rec["status"] in ("infeasible", "empty")
                    row.append(None)
                    stat["inf"] += 1
            Mt.append(row)
        Bq.append(Mt)
    print(f"pair bounds ok: {stat['finite']} finite, {stat['inf']} proved empty; "
          f"{len(used)} certification records used of {len(P.crecs)}")

    # 4. exact shortest path (None = +inf)
    def add(a, b):
        return None if a is None or b is None else a + b

    def mn(vals):
        v = [x for x in vals if x is not None]
        return min(v) if v else None
    f = list(Bq[0][0])
    for t in range(1, T - 1):
        f = [mn(add(f[r], Bq[t][r][c]) for r in range(len(f))) for c in range(len(Bq[t][0]))]
    V = mn(add(f[r], Bq[T - 1][r][0]) for r in range(len(f)))
    total = Fraction(P.mu) * D["hor_rhs"] + V
    down = Fraction(int(total * 10**9 // 1), 10**9)
    print("CERTIFIED separator-branching bound (exact):", total)
    print(f"rounded down to 9 decimals: {float(down):.9f}")
    json.dump(dict(bound_exact=str(total), bound_rounded_down=str(down), leaves=[len(l) for l in P.leaves],
                   records_used=len(used), records=len(P.crecs)),
              open(cfg["out"] + "_verify.json", "w"), indent=1)


if __name__ == "__main__":
    main()
