"""Independent re-check of a separator-branching certificate for waterno2_06.

Uses only the first verifier's model reader (vmodel / osilx) and my own code.
The authors' code (core, dpcells, verify, terminal) is NOT imported; the pickle
is read through a stub class (load_cert.py).

A. Terminal row: derived by structure in exact arithmetic (per period, sum of
   the three balance rows / 3600, reduced with the in-period copy rows and the
   fixed demand), then summed over periods with the link rows and the horizon
   row.
B. Certificate:
   1. level box of each link from OSIL bounds and implied bounds (exact);
      the root cell of the plan must contain it;
   2. the leaves of each link cover the root box (elementary-cell sweep over
      all leaf breakpoints; independent of the split tree);
   3. every leaf pair (r, c) of period t uses a record of period t whose stored
      entry/exit boxes CONTAIN the leaf boxes, whose slopes equal the single
      slope vector of the link (the same vector for both periods adjacent to
      the link), and mu = 0;
   4. shortest path in exact rational arithmetic over the record bounds.
usage: python3 ind_verify.py cert.pkl implied.json
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
from fractions import Fraction as F

import numpy as np

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel  # noqa: E402
import load_cert  # noqa: E402

T = 6
INF = float("inf")


def is_inf(s):
    return s.upper() in ("INF", "+INF", "-INF")


# ---------------------------------------------------------------- A
def terminal_row(I):
    m = I["m"]
    names = m["names"]
    cons = m["cons"]
    total_d = F(0)
    levs = []
    for t in range(T):
        polys = {i: vmodel.poly(cons[i]) for i in I["per_rows"][t]}
        # union-find over in-period copy rows  x_a - x_b = 0
        par = {}

        def find(v):
            par.setdefault(v, v)
            while par[v] != v:
                v = par[v]
            return v
        fixed = {}
        for i, p in polys.items():
            c = cons[i]
            if is_inf(c["lb"]) or is_inf(c["ub"]) or F(c["lb"]) != F(c["ub"]):
                continue
            if len(p) == 2 and all(len(k) == 1 for k in p) and sorted(p.values()) == [-1, 1] and F(c["lb"]) == 0:
                a, b = [k[0] for k in p]
                ra, rb = find(a), find(b)
                if ra != rb:
                    par[ra] = rb
            if len(p) == 1 and list(p)[0].__len__() == 1 and list(p.values())[0] == 1:
                fixed[list(p)[0][0]] = F(c["lb"])
        bal = [i for i, p in polys.items() if any(abs(a) == 3600 for a in p.values())]
        assert len(bal) == 3
        # sum of balance rows / 3600, flows mapped to class representatives
        comb = {}
        lev = {}
        for i in bal:
            c = cons[i]
            assert F(c["lb"]) == F(c["ub"]) == 0
            for k, a in polys[i].items():
                assert len(k) == 1
                v = k[0]
                if abs(a) == 3600:
                    r = find(v)
                    comb[r] = comb.get(r, 0) + a / 3600
                else:
                    lev[v] = lev.get(v, 0) + a / 3600
        comb = {r: a for r, a in comb.items() if a != 0}
        # expected: +1 on the class of the horizon variable, -1 on the class of the fixed demand
        h = I["hvar"][t]
        assert comb.pop(find(h)) == 1, (t, comb)
        (rd, ad), = comb.items()
        assert ad == -1
        dvars = [v for v in fixed if find(v) == rd]
        assert len(dvars) == 1
        d = fixed[dvars[0]]
        total_d += d
        # so  h_t - d_t + sum lev_v x_v = 0  with lev: +A/3600 on start, -A/3600 on end
        print(f"  period {t}: h = {names[h]} = d + sum_k A_k (e_k - s_k)/3600, d = {d}, "
              f"levels {{{', '.join(f'{names[v]}: {a}' for v, a in lev.items())}}}")
        if t == 0:
            start = {v: a for v, a in lev.items() if a > 0}    # +A/3600 * s
            L0 = {v: F(m["lb"][v]) for v in start}
            assert all(m["lb"][v] == m["ub"][v] for v in start)
        if t == T - 1:
            end = {v: -a for v, a in lev.items() if a < 0}     # coefficient A/3600 of e
        levs.append(lev)
    # link rows x_end(t,k) = x_start(t+1,k) must join an end and a start of equal area
    for t in range(T - 1):
        for (i, a, b) in I["links"][t]:
            assert levs[t][a] < 0 and levs[t + 1][b] == -levs[t][a], (t, names[a], names[b])
    # telescoping over links: sum_t (e_t - s_t) = E - L0 per tank (links s_{t+1} = e_t)
    # horizon: sum h >= c  ->  sum_k A_k (E_k - L0_k)/3600 >= c - sum d
    c = I["hrhs"]
    rhs = c - total_d + sum(start[v] * L0[v] for v in start)
    print(f"  sum_t d_t = {total_d} ({float(total_d)}); horizon rhs c = {c}; c - sum d = {c - total_d}")
    print("  terminal row:", {names[v]: str(a) for v, a in end.items()}, ">=", rhs, "=", float(rhs))
    return end, rhs


# ---------------------------------------------------------------- B
def level_box(I, link, implied):
    m = I["m"]
    names = m["names"]
    lo, hi = [], []
    for (i, a, b) in I["links"][link]:
        l, h = None, None
        for v in (a, b):
            lv = F(m["lb"][v])
            hv = F(m["ub"][v])
            if names[v] in implied:
                lv = max(lv, F(implied[names[v]][0]))
                hv = min(hv, F(implied[names[v]][1]))
            l = lv if l is None else max(l, lv)
            h = hv if h is None else min(h, hv)
        lo.append(l)
        hi.append(h)
    return lo, hi


def covers(root_lo, root_hi, leaves):
    """Leaves (closed boxes, float) cover the closed root box: all leaves in the
    root; every elementary cell of the breakpoint grid lies in some leaf."""
    for lo, hi in leaves:
        for k in range(3):
            assert root_lo[k] <= lo[k] <= hi[k] <= root_hi[k], (lo, hi)
    bps = []
    for k in range(3):
        s = sorted({root_lo[k], root_hi[k]} | {l[0][k] for l in leaves} | {l[1][k] for l in leaves})
        assert s[0] == root_lo[k] and s[-1] == root_hi[k]
        bps.append(s)
    shape = tuple(len(s) - 1 for s in bps)
    assert all(n >= 1 for n in shape)
    hit = np.zeros(shape, dtype=np.int32)
    idx = [{v: j for j, v in enumerate(s)} for s in bps]
    for lo, hi in leaves:
        sl = tuple(slice(idx[k][lo[k]], idx[k][hi[k]]) for k in range(3))
        hit[sl] += 1
    return int(hit.min()), int(hit.max()), shape


def main():
    pkl, implied_path = sys.argv[1], sys.argv[2]
    I = vmodel.instance(T)
    names = I["m"]["names"]
    print("A. terminal row (independent derivation)")
    end, rhs = terminal_row(I)
    implied = json.load(open(implied_path))
    implied = implied.get("bounds", implied)
    P = load_cert.load(pkl)
    d = P.__dict__
    assert d["T"] == T and d["mu"] == 0.0
    cells, leaves, crecs, tabs = d["cells"], d["leaves"], d["crecs"], d["tables"]
    lam = d["lam"]
    print("B. certificate", pkl)
    # 1-2 coverage
    for link in range(T - 1):
        lo, hi = level_box(I, link, implied)
        root = cells[link][0]
        ok = all(F(root["lo"][k]) <= lo[k] and F(root["hi"][k]) >= hi[k] for k in range(3))
        assert ok, (link, root, lo, hi)
        lv = [(cells[link][c]["lo"], cells[link][c]["hi"]) for c in leaves[link]]
        mn, mx, shape = covers(root["lo"], root["hi"], lv)
        assert mn >= 1, ("uncovered elementary cell", link)
        print(f"  link {link}: exact level box lo={[float(v) for v in lo]} hi={[float(v) for v in hi]} "
              f"inside root cell; {len(lv)} leaves cover it (grid {shape}, coverage multiplicity {mn}..{mx})")
    # 3 records
    Bq = []
    used = set()
    nfin = ninf = 0
    for t in range(T):
        rows = [None] if t == 0 else [cells[t - 1][c] for c in leaves[t - 1]]
        cols = [None] if t == T - 1 else [cells[t][c] for c in leaves[t]]
        lin = lam[t - 1] if t > 0 else [0.0, 0.0, 0.0]
        lout = lam[t] if t < T - 1 else [0.0, 0.0, 0.0]
        CS, CB = tabs["CSRC"][t], tabs["CB"][t]
        assert CS.shape == (len(rows), len(cols))
        M = []
        for r, rc in enumerate(rows):
            row = []
            for c, cc in enumerate(cols):
                rid = int(CS[r, c])
                assert rid >= 0
                rec = crecs[rid]
                used.add(rid)
                assert rec["t"] == t and rec["mu"] == 0.0
                assert list(rec["lam_in"]) == list(lin) and list(rec["lam_out"]) == list(lout), (t, rid)
                for cell, box in ((rc, rec["cin_box"]), (cc, rec["cout_box"])):
                    if cell is None:
                        assert box is None
                    else:
                        blo, bhi = box
                        assert all(blo[k] <= cell["lo"][k] and cell["hi"][k] <= bhi[k] for k in range(3)), \
                            ("record box does not contain the leaf", t, rid)
                b = rec["bound"]
                assert float(CB[r, c]) == b
                assert not (b != b) and b != -INF
                if b == INF:
                    assert rec["status"] in ("infeasible", "empty")
                    row.append(None)
                    ninf += 1
                else:
                    row.append(F(b))
                    nfin += 1
            M.append(row)
        Bq.append(M)
    print(f"  leaf pairs: {nfin} finite bounds, {ninf} +inf; records used {len(used)} of {len(crecs)}; "
          f"slopes per link identical in all used records; mu = 0")

    # 4 exact DP (None = +inf), with argmin path
    def add(a, b):
        return None if a is None or b is None else a + b

    f = [(Bq[0][0][c], [c]) for c in range(len(Bq[0][0]))]
    for t in range(1, T):
        nc = len(Bq[t][0])
        g = []
        for c in range(nc):
            best = (None, None)
            for r in range(len(f)):
                v = add(f[r][0], Bq[t][r][c])
                if v is not None and (best[0] is None or v < best[0]):
                    best = (v, f[r][1] + [c])
            g.append(best)
        f = g
    V, path = f[0]
    down = F(V.numerator * 10**9 // V.denominator, 10**9)
    print(f"  exact DP value: {V}  = {float(V)!r}; rounded down 9 dp: {float(down):.9f}")
    print(f"  minimizing path (leaf positions per link): {path[:T-1]}")
    for t in range(T):
        r = 0 if t == 0 else path[t - 1]
        c = 0 if t == T - 1 else path[t]
        rid = int(tabs["CSRC"][t][r, c])
        print(f"    period {t}: record {rid}, bound {crecs[rid]['bound']!r}")
    json.dump(dict(value=str(V), rounded_down=f"{float(down):.9f}", path=path[:T - 1],
                   terminal={names[v]: str(a) for v, a in end.items()}, terminal_rhs=str(rhs)),
              open(sys.argv[3], "w"), indent=1)


if __name__ == "__main__":
    main()
