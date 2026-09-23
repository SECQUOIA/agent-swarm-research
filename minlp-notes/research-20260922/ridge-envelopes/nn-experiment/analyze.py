"""Aggregate raw results into CSV files, a summary JSON and markdown tables.

Best-known value of (net, sense) = min over: multistart primal, B&B incumbents
(true network values) and SCIP/Gurobi solutions re-evaluated with numpy.
All values are in minimization units (sense * output).
"""
import csv
import glob
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
REL_GAP, ABS_GAP = 1e-4, 1e-6


def tol(v):
    return max(ABS_GAP, REL_GAP * abs(v))


def sgm(x, shift):
    x = np.asarray(x, float)
    return float(np.exp(np.mean(np.log(x + shift))) - shift)


def load():
    root = {}
    for f in glob.glob(str(RES / "root" / "*.json")):
        o = json.load(open(f))
        root[o["name"]] = o
    bnb = {}
    for f in glob.glob(str(RES / "bnb" / "*.json")):
        o = json.load(open(f))
        bnb[(o["name"], o["sense"], o["mode"])] = o
    solv = {}
    for f in glob.glob(str(RES / "solvers" / "*.json")):
        o = json.load(open(f))
        solv[(o["name"], o["sense"], o["solver"])] = o
    return root, bnb, solv


def best_known(root, bnb, solv):
    best = {}
    for name, o in root.items():
        for r in o["runs"]:
            k = (name, r["sense"])
            best[k] = min(best.get(k, np.inf), r["primal"])
    for (name, sense, _), o in bnb.items():
        best[(name, sense)] = min(best.get((name, sense), np.inf), o["UB"])
    for (name, sense, _), o in solv.items():
        if o.get("true_value") is not None:
            best[(name, sense)] = min(best.get((name, sense), np.inf), o["true_value"])
    return best


def root_table(root, best):
    rows = []
    for name, o in sorted(root.items()):
        R = {(r["sense"], r["bounds"], r["mode"]): r for r in o["runs"]}
        for sense in (1, -1):
            P = best[(name, sense)]
            for b in ("ibp", "obbt"):
                r0, r1 = R[(sense, b, "R0")], R[(sense, b, "R1")]
                g0 = P - r0["bound"]
                rows.append(dict(
                    net=name, act=o["act"], d=o["d"], depth=len(o["widths"]), widths="x".join(map(str, o["widths"])),
                    sense="min" if sense > 0 else "max", bounds=b, best_known=P, multistart=r0["primal"],
                    R0=r0["bound"], R1=r1["bound"], gap_R0=g0, gap_R1=P - r1["bound"],
                    gap_closed=(r1["bound"] - r0["bound"]) / g0 if g0 > 0 else 0.0,
                    rounds_R0=r0["rounds"], rounds_R1=r1["rounds"], status_R0=r0["status"], status_R1=r1["status"],
                    cuts_R0=r0["cuts_r0"], cuts_R1_r0=r1["cuts_r0"], cuts_R1_r1=r1["cuts_r1"],
                    tsep_R0=r0["t_sep"], tsep_R1=r1["t_sep"], time_R0=r0["time"], time_R1=r1["time"],
                    obbt_time=r0["obbt_time"], mean_z_width=r0["mean_z_width"]))
    return rows


def bnb_table(bnb, best):
    rows = []
    keys = sorted({(n, s) for (n, s, _) in bnb})
    for n, s in keys:
        if (n, s, "R0") not in bnb or (n, s, "R1") not in bnb:
            continue
        a, b = bnb[(n, s, "R0")], bnb[(n, s, "R1")]
        P = best[(n, s)]
        row = dict(net=n, act=a["act"], d=a["d"], depth=len(a["widths"]), widths="x".join(map(str, a["widths"])),
                   sense="min" if s > 0 else "max", best_known=P)
        for m, o in (("R0", a), ("R1", b)):
            row.update({"%s_%s" % (k, m): o[k] for k in ("status", "closed", "nodes", "time", "wall_time", "LB", "UB",
                                                          "gap", "root_bound", "rounds", "cuts_r0", "cuts_r1",
                                                          "t_lp", "t_sep", "max_depth")})
            row["relgap_%s" % m] = o["gap"] / max(1.0, abs(o["UB"]))
            row["lb_valid_%s" % m] = bool(o["LB"] <= P + tol(P))
        rows.append(row)
    return rows


def solver_table(solv, bnb, best):
    rows = []
    for (n, s, sv), o in sorted(solv.items()):
        P = best[(n, s)]
        st = str(o.get("status"))
        LB, UB = o.get("LB"), o.get("UB")
        closed = LB is not None and UB is not None and np.isfinite(UB) and UB - LB <= tol(UB) * 1.0000001
        r = dict(net=n, act=o["act"], d=o["d"], sense="min" if s > 0 else "max", solver=sv, status=st,
                 time=o.get("time"), wall_time=o.get("wall_time"), nodes=o.get("nodes"), LB=LB, UB=UB,
                 true_value=o.get("true_value"), best_known=P, closed=bool(closed),
                 lb_valid=bool(LB is None or LB <= P + tol(P)))
        for m in ("R0", "R1"):
            k = (n, s, m)
            if k in bnb:
                r["bnb_%s_closed" % m] = bnb[k]["closed"]
                r["bnb_%s_time" % m] = bnb[k]["time"]
        rows.append(r)
    return rows


def write_csv(rows, path):
    if not rows:
        return
    keys = list(rows[0].keys())
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(rows)


def q(x):
    x = np.asarray(x, float)
    return "%.1f / %.1f / %.1f / %.1f" % tuple(100 * np.percentile(x, [25, 50, 75, 100]))


def summarize(root_rows, bnb_rows, solv_rows, root):
    out, md = {}, []
    # ---------------- root
    md.append("### Root gap closed by R1 over R0, (R1 - R0) / (best - R0), in percent\n")
    md.append("| group | bounds | n | mean | 25% / median / 75% / max | #>1% | #>10% | R1 < R0 - 1e-6 |")
    md.append("|---|---|---|---|---|---|---|---|")
    groups = [("all", lambda r: True)]
    groups += [("act=" + a, (lambda a: lambda r: r["act"] == a)(a)) for a in ("tanh", "sigmoid", "silu", "gelu", "sin")]
    groups += [("d=%d" % d, (lambda d: lambda r: r["d"] == d)(d)) for d in (2, 3, 5)]
    groups += [("hidden layers=%d" % k, (lambda k: lambda r: r["depth"] == k)(k)) for k in (1, 2, 3)]
    for gname, gf in groups:
        for b in ("ibp", "obbt"):
            rs = [r for r in root_rows if r["bounds"] == b and gf(r)]
            gc = [r["gap_closed"] for r in rs]
            worse = sum(r["R1"] < r["R0"] - 1e-6 for r in rs)
            md.append("| %s | %s | %d | %.1f | %s | %d | %d | %d |" % (gname, b, len(rs), 100 * np.mean(gc), q(gc),
                                                                  sum(g > 0.01 for g in gc), sum(g > 0.10 for g in gc), worse))
            out["root_%s_%s" % (gname, b)] = dict(n=len(rs), mean=float(np.mean(gc)), median=float(np.median(gc)),
                                                  worse=int(worse))
    md.append("")
    # R1 with IBP vs R0 with OBBT
    pairs = defaultdict(dict)
    for r in root_rows:
        pairs[(r["net"], r["sense"])][r["bounds"]] = r
    better = sum(p["ibp"]["R1"] > p["obbt"]["R0"] + 1e-6 for p in pairs.values())
    md.append("R1 with IBP bounds beats R0 with OBBT bounds in %d of %d (net, sense) pairs.\n" % (better, len(pairs)))
    out["r1ibp_beats_r0obbt"] = [better, len(pairs)]
    # cost
    md.append("| bounds | mean rounds R0 / R1 | mean cuts R0 | mean cuts R1 (1-D + Thm 1) | mean sep. time R0 / R1 (s) | mean total time R0 / R1 (s) |")
    md.append("|---|---|---|---|---|---|")
    for b in ("ibp", "obbt"):
        rs = [r for r in root_rows if r["bounds"] == b]
        md.append("| %s | %.1f / %.1f | %.0f | %.0f + %.0f | %.2f / %.2f | %.2f / %.2f |" % (
            b, np.mean([r["rounds_R0"] for r in rs]), np.mean([r["rounds_R1"] for r in rs]),
            np.mean([r["cuts_R0"] for r in rs]), np.mean([r["cuts_R1_r0"] for r in rs]),
            np.mean([r["cuts_R1_r1"] for r in rs]), np.mean([r["tsep_R0"] for r in rs]),
            np.mean([r["tsep_R1"] for r in rs]), np.mean([r["time_R0"] for r in rs]), np.mean([r["time_R1"] for r in rs])))
    st = defaultdict(int)
    for r in root_rows:
        st[(r["status_R0"], r["status_R1"])] += 1
    md.append("\nCut-loop termination (R0 status, R1 status): %s\n" % dict(st))
    # cut checks
    cc = [o["cut_check"] for o in root.values()]
    out["cut_check"] = dict(cuts=int(sum(c["cuts"] for c in cc)), max_violation=float(max(c["max_violation"] for c in cc)),
                            mean_outside=float(np.mean([c["mean_fraction_outside_simplex"] for c in cc])))
    # ---------------- bnb
    if bnb_rows:
        md.append("### Python B&B, R0 vs R1 (600 s CPU limit)\n")
        md.append("| group | runs | closed R0 | closed R1 | both closed | SGM time R0 / R1 (s, shift 1) | SGM nodes R0 / R1 (shift 10) | median node ratio R1/R0 | median time ratio R1/R0 | R1 faster / slower (>10%) | open both: median rel. gap R0 / R1 |")
        md.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for gname, gf in groups:
            rs = [r for r in bnb_rows if gf(r)]
            if not rs:
                continue
            both = [r for r in rs if r["closed_R0"] and r["closed_R1"]]
            neither = [r for r in rs if not r["closed_R0"] and not r["closed_R1"]]
            nr = [r["nodes_R1"] / r["nodes_R0"] for r in both]
            tr = [r["time_R1"] / r["time_R0"] for r in both]
            faster = sum(t < 0.9 for t in tr)
            slower = sum(t > 1.1 for t in tr)
            md.append("| %s | %d | %d | %d | %d | %s | %s | %s | %s | %d / %d | %s |" % (
                gname, len(rs), sum(r["closed_R0"] for r in rs), sum(r["closed_R1"] for r in rs), len(both),
                "%.1f / %.1f" % (sgm([r["time_R0"] for r in both], 1), sgm([r["time_R1"] for r in both], 1)) if both else "-",
                "%.0f / %.0f" % (sgm([r["nodes_R0"] for r in both], 10), sgm([r["nodes_R1"] for r in both], 10)) if both else "-",
                "%.2f" % np.median(nr) if both else "-", "%.2f" % np.median(tr) if both else "-", faster, slower,
                "%.2e / %.2e" % (np.median([r["relgap_R0"] for r in neither]), np.median([r["relgap_R1"] for r in neither])) if neither else "-"))
            out["bnb_%s" % gname] = dict(runs=len(rs), closed_R0=sum(r["closed_R0"] for r in rs),
                                         closed_R1=sum(r["closed_R1"] for r in rs), both=len(both),
                                         median_node_ratio=float(np.median(nr)) if both else None,
                                         median_time_ratio=float(np.median(tr)) if both else None)
        md.append("")
        out["bnb_lb_invalid"] = [(r["net"], r["sense"]) for r in bnb_rows if not (r["lb_valid_R0"] and r["lb_valid_R1"])]
        # open in both: which has the smaller final gap
        neither = [r for r in bnb_rows if not r["closed_R0"] and not r["closed_R1"]]
        if neither:
            smaller = sum(r["gap_R1"] < r["gap_R0"] * 0.99 for r in neither)
            larger = sum(r["gap_R1"] > r["gap_R0"] * 1.01 for r in neither)
            md.append("Runs open in both modes at the limit: %d; final gap smaller with R1 in %d, larger in %d.\n" % (len(neither), smaller, larger))
    # ---------------- solvers
    if solv_rows:
        md.append("### SCIP 10 and Gurobi 13 (context; GELU skipped)\n")
        md.append("| solver | runs | closed (gap <= max(1e-6, 1e-4 abs(UB))) | SGM time on closed (s) | Python B&B R0 / R1 closed on the same runs |")
        md.append("|---|---|---|---|---|")
        for sv in ("scip", "gurobi"):
            rs = [r for r in solv_rows if r["solver"] == sv]
            cl = [r for r in rs if r["closed"]]
            md.append("| %s | %d | %d | %.1f | %d / %d |" % (sv, len(rs), len(cl), sgm([r["time"] for r in cl], 1) if cl else float("nan"),
                                                        sum(bool(r.get("bnb_R0_closed")) for r in rs), sum(bool(r.get("bnb_R1_closed")) for r in rs)))
        out["solver_lb_invalid"] = [(r["net"], r["sense"], r["solver"]) for r in solv_rows if not r["lb_valid"]]
        md.append("")
    return out, md


if __name__ == "__main__":
    root, bnb, solv = load()
    best = best_known(root, bnb, solv)
    rr, br, sr = root_table(root, best), bnb_table(bnb, best), solver_table(solv, bnb, best)
    write_csv(rr, RES / "root.csv")
    write_csv(br, RES / "bnb.csv")
    write_csv(sr, RES / "solvers.csv")
    out, md = summarize(rr, br, sr, root)
    (RES / "summary.json").write_text(json.dumps(out, indent=1))
    (RES / "summary_tables.md").write_text("\n".join(md))
    print("\n".join(md))
    print(json.dumps({k: v for k, v in out.items() if "invalid" in k or k == "cut_check"}, indent=1))
