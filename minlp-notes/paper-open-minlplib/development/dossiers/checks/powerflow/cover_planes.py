"""Exact checks on the stored leaf boxes: (1) coverage of the root box (grid of all breakpoints,
each elementary cell in exactly one leaf, by midpoint test); (2) every vertex plane of every leaf
satisfies H >= F at all 8 vertices, and passes through >= 4 of them (exact); (3) identity and cut
slack at the exactly feasible point (centre, 60 digits)."""
import json, sys, itertools
from fractions import Fraction as Fr
sys.path.insert(0, "/tmp/pfdossier/code")
import pf_model as pm, leafcut as lc
from decimal import Decimal, getcontext
getcontext().prec = 80

for name in sys.argv[1:]:
    M = pm.decode(name); info = lc.leaf_info(M)
    b = info["b"]
    print(name, "b =", b, "=", float(b), " 1/b =", 1/b, " Pg var", M["I"]["names"][info["Pg"]], "Qg var", M["I"]["names"][info["Qg"]],
          " root box", [(str(a), str(c)) for a, c in ((info['plo'], info['phi']), (info['qlo'], info['qhi']), info['WLL'])])
    root = ((info["plo"], info["phi"]), (info["qlo"], info["qhi"]), info["WLL"])
    for tag in ("bb3", "bb3t"):
        D = json.load(open(f"/tmp/pfdossier/data/{name}.{tag}.json"))
        boxes = [tuple((Fr(a), Fr(c)) for a, c in L["box"]) for L in D["leaves"]]
        for bx in boxes:
            for d in range(3):
                assert root[d][0] <= bx[d][0] < bx[d][1] <= root[d][1]
        cuts = [sorted({root[d][0], root[d][1]} | {bx[d][k] for bx in boxes for k in (0, 1)}) for d in range(3)]
        ncell = 0
        for cell in itertools.product(*[list(zip(c[:-1], c[1:])) for c in cuts]):
            mid = [(lo + hi) / 2 for lo, hi in cell]
            inside = [bx for bx in boxes if all(bx[d][0] <= mid[d] <= bx[d][1] for d in range(3))]
            assert len(inside) == 1, (cell, len(inside))
            # cell must lie inside that box entirely
            bx = inside[0]
            assert all(bx[d][0] <= cell[d][0] and cell[d][1] <= bx[d][1] for d in range(3))
            ncell += 1
        vol = sum((bx[0][1]-bx[0][0])*(bx[1][1]-bx[1][0])*(bx[2][1]-bx[2][0]) for bx in boxes)
        rv = (root[0][1]-root[0][0])*(root[1][1]-root[1][0])*(root[2][1]-root[2][0])
        # planes
        npl = 0; minslack = None
        for bx in boxes:
            V = [(p, q, s, lc.F(info, p, q, s)) for p in bx[0] for q in bx[1] for s in bx[2]]
            P = lc.planes3(info, bx)
            assert len(P) >= 1
            for (al, be, ga, de) in P:
                vals = [al*p + be*q + ga*s + de - f for p, q, s, f in V]
                assert all(v >= 0 for v in vals)
                assert sum(1 for v in vals if v == 0) >= 4
                npl += 1
        print(f"  {tag}: {len(boxes)} leaves, {ncell} grid cells each in exactly one leaf; volume sum == root: {vol == rv}; planes checked {npl}")
    # identity at the exactly feasible point (centre)
    P = json.load(open(f"/tmp/pfdossier/data/{name}.json"))
    val = {}
    for k, v in P["fixed"].items(): val[k] = Fr(v["value"])
    for k, v in P["free"].items(): val[k] = Fr(Decimal(v))
    nm = M["I"]["names"]
    Pg, Qg = val[nm[info["Pg"]]], val[nm[info["Qg"]]]
    if M["polar"]:
        (vN, tN), (vL, tL) = M["busmap"][info["N"]], M["busmap"][info["L"]]
        WNN, WLL = val[nm[vN]]**2, val[nm[vL]]**2
        print("  bus N vars", nm[vN], nm[tN], " bus L vars", nm[vL], nm[tL])
    else:
        # rectangular: find e,f pairs from volt rows order used by pf_model: pairs sorted by var index
        I = M["I"]; xset = set()
        for c in I["cons"]:
            if c["quad"] and c["lb"] == c["ub"]:
                for a, bb, _ in c["quad"]: xset |= {a, bb}
        keys = sorted({tuple(sorted(a for a, bb, _ in c["quad"])) for c in I["cons"]
                       if c["quad"] and not c["lin"] and {a for a, bb, _ in c["quad"]} <= xset})
        (eN, fN), (eL, fL) = keys[info["N"]], keys[info["L"]]
        print("  bus N vars", nm[eN], nm[fN], " bus L vars", nm[eL], nm[fL])
        WNN = val.get(nm[eN], 0)**2 + val.get(nm[fN], 0)**2
        WLL = val.get(nm[eL], 0)**2 + val.get(nm[fL], 0)**2
    Fv = lc.F(info, Pg, Qg, WLL)
    print(f"  exact point: Pg {float(Pg):.14f} Qg {float(Qg)} W_LL {float(WLL):.14f}; W_NN - F = {float(WNN - Fv):.3e}")
    D = json.load(open(f"/tmp/pfdossier/data/{name}.bb3t.json"))
    for L in D["leaves"]:
        bx = tuple((Fr(a), Fr(c)) for a, c in L["box"])
        if all(bx[0][0] <= Pg <= bx[0][1] for _ in [0]) and bx[1][0] <= Qg <= bx[1][1] and bx[2][0] <= WLL <= bx[2][1]:
            sl = [al*Pg + be*Qg + ga*WLL + de - Fv for al, be, ga, de in lc.planes3(info, bx)]
            print(f"  leaf with point {[[float(a), float(c)] for a, c in bx]}: envelope slack H - F at point per plane {[float(s) for s in sl]}")
