"""Section 5.5 claim: SCIP reports 'optimal' at 55.69 and at 65.12 on the same
pair subproblem (cert2 record 2236, period 3), depending on the seed.

SCIP models are built with the authors' period.solve_window (read-only import;
this only reproduces their SCIP runs).  Every returned point is then evaluated
EXACTLY with my own code on the first verifier's model: objective, max
violation of the period rows, of the OSIL bounds, of the implied bounds and of
the cell boxes.
usage: python3 scip_claim.py cert2.pkl rid
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import sys
from fractions import Fraction as F

W2 = _RESEARCH + "/open-instances-wave2/waterno2"
sys.path.insert(0, W2 + "/sepbranch")
sys.path.insert(0, W2)
sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel  # noqa: E402
import load_cert  # noqa: E402

T = 6


def main():
    P = load_cert.load(sys.argv[1]).__dict__
    for rid in [int(a) for a in sys.argv[2].split(",")]:
        one(P, rid, sys.argv[3] if len(sys.argv) > 3 else "claim")


def one(P, rid, mode):
    rec = P["crecs"][rid]
    t = rec["t"]
    import period
    import bundle
    D = period.setup(T, W2 + "/logs/implied_06.json")
    I = vmodel.instance(T)
    m = I["m"]
    names = m["names"]
    box = {}
    if t > 0:
        for k, (i, a, b) in enumerate(I["links"][t - 1]):
            box[b] = (rec["cin_box"][0][k], rec["cin_box"][1][k])
    if t < T - 1:
        for k, (i, a, b) in enumerate(I["links"][t]):
            box[a] = (rec["cout_box"][0][k], rec["cout_box"][1][k])
    lam = [[0.0] * 3 for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = rec["lam_in"]
    if t < T - 1:
        lam[t] = rec["lam_out"]
    imp = json.load(open(W2 + "/logs/implied_06.json"))["bounds"]
    cobj = vmodel.period_objective(I, t, lam, 0.0)
    print("record", rid, "period", t, "rbb bound", rec["bound"], "target", rec["target"])
    if t == T - 1:
        import terminal
        terminal.add_terminal_row(D)
    runs = (("noprop", bundle.NOPROP), ("default", {}), ("default seed7", {"randomization/randomseedshift": 7}))
    if mode == "tight":
        runs = (("default feastol 1e-9", {"numerics/feastol": 1e-9}),)
    for name, prm in runs:
        r = period.solve_window(D, t, t + 1, lam, 0.0, 60, prm, box)
        x = r["x"]
        if x is None:
            print(f"  SCIP {name}: {r['status']} (no point)")
            continue
        X = {v: F(val) for v, val in x.items()}
        obj = sum(a * X[v] for v, a in cobj.items())
        rowv = F(0)
        rowlist = [m["cons"][i] for i in I["per_rows"][t]]
        if t == T - 1:   # terminal row (my derivation), checked like a row
            rowlist.append(dict(lin={names.index("x253"): "1/2", names.index("x265"): "1/5",
                                     names.index("x277"): "4/9"}, quad=[], nl=None, lb="3913/900", ub="INF"))
        for c in rowlist:
            s = F(0)
            for mono, a in vmodel.poly(c).items():
                term = a
                for v in mono:
                    term *= X[v]
                s += term
            if c["lb"].upper() != "-INF":
                rowv = max(rowv, F(c["lb"]) - s)
            if c["ub"].upper() not in ("INF", "+INF"):
                rowv = max(rowv, s - F(c["ub"]))
        bv = F(0)
        for v in X:
            lo = None if m["lb"][v].upper() == "-INF" else F(m["lb"][v])
            hi = None if m["ub"][v].upper() in ("INF", "+INF") else F(m["ub"][v])
            for src in ([imp[names[v]]] if names[v] in imp else []) + ([box[v]] if v in box else []):
                a, b = F(src[0]), F(src[1])
                lo = a if lo is None else max(lo, a)
                hi = b if hi is None else min(hi, b)
            if lo is not None:
                bv = max(bv, lo - X[v])
            if hi is not None:
                bv = max(bv, X[v] - hi)
            if m["vt"][v] == "B":
                bv = max(bv, min(abs(X[v]), abs(X[v] - 1)))
        print(f"  SCIP {name}: status {r['status']}, primal {r['primal']:.6f}, dual {r['dual']:.6f}; "
              f"exact objective of its point {float(obj):.6f}, max row violation {float(rowv):.2e}, "
              f"max bound/box/integrality violation {float(bv):.2e}", flush=True)


if __name__ == "__main__":
    main()
