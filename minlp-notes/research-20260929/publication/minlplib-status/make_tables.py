"""Build the markdown tables of report.md from the data files.

Usage: python3 make_tables.py   (writes data/tables.md)
"""
import datetime
import json
import os

import instances as I

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))
A = json.load(open(os.path.join(HERE, "data", "part_a.json")))
BD = json.load(open(os.path.join(HERE, "data", "bounddates.json")))
W = json.load(open(os.path.join(HERE, "data", "wayback_files.json")))
S = json.load(open(os.path.join(HERE, "data", "stats_history.json")))
P = {r["name"]: r for r in json.load(open(os.path.join(R, "bound-audit", "pages.json")))}
FLAG = {"glider100": ["COUENNE", "LINDO"], "topopt-cantilever_60x40_50": ["LINDO"], "methanol50": ["LINDO"],
        "sssd20-04persp": ["LINDO"], "sssd22-08persp": ["LINDO"], "sssd25-04persp": ["LINDO"],
        "sssd25-08persp": ["LINDO"], "nuclear14": ["LINDO"], "ghg_3veh": ["ANTIGONE", "BARON"],
        "nd_netgen-2000-3-4-b-a-ns_7": ["CPLEX", "GUROBI"], "watercontamination0303": ["BONMIN", "LINDO"],
        "smallinvDAXr1b150-165": ["LINDO"], "smallinvDAXr2b150-165": ["LINDO"], "smallinvDAXr1b200-220": ["LINDO"],
        "smallinvDAXr2b200-220": ["LINDO"], "eniplac": ["COUENNE", "LINDO", "SCIP"], "lop97icx": ["ANTIGONE"],
        "spring": ["ANTIGONE", "BARON", "COUENNE", "LINDO", "SCIP"], "stockcycle": ["ANTIGONE", "BARON", "COUENNE"],
        "rocket100": ["LINDO"], "rocket200": ["LINDO"], "rocket400": ["LINDO"]}


def iso(d):
    return datetime.datetime.strptime(d, "%d %b %Y").strftime("%Y-%m-%d")


def lm(s):
    return datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d") if s else "?"


def short_verdict(v):
    if v.startswith("identical"):
        return "identical"
    if v.startswith("same up to double"):
        return "same up to rounding (" + v.split("max relative difference ")[1].split(";")[0] + ")"
    if v.startswith("same"):
        return "same"
    return v


def src_date(s):
    if s["tag"] == "jl2017":
        return "2017-11-23"
    d = s.get("date") or ""
    try:
        return datetime.datetime.strptime(d.split()[0], "%m/%d/%y").strftime("%Y-%m-%d")
    except ValueError:
        return d


def wb(n):
    out = []
    for k in ("gms", "osil"):
        for c in W[f"{n}:{k}"]["captures"]:
            tag = "=" if c["digest_matches_current"] else ("prefix" if c.get("proper_prefix_of_current") else "DIFF")
            out.append(f"{k} {c['timestamp'][:4]}-{c['timestamp'][4:6]}-{c['timestamp'][6:8]} {tag}")
    seen, res = set(), []
    for o in out:
        if o not in seen:
            seen.add(o)
            res.append(o)
    return "; ".join(res) if res else "none"


def table_a():
    rows = ["| instance | group | page head vs 09-30 copy | parsed vs pages.json | OSIL sha256 vs cache | "
            "OSIL Last-Modified | GMS Last-Modified | latest dated entry (bounddates.html) |",
            "|---|---|---|---|---|---|---|---|"]
    for n in I.ALL:
        r = A["instances"][n]
        c = [x for x in r["page_comparisons"] if x["copy"].startswith("bound-audit")][0]
        last = sorted(BD[n])[-1] if BD[n] else ["-", "", ""]
        rows.append(f"| {n} | {r['group']} | {'identical' if c['byte_identical'] else 'DIFFERENT'} | "
                    f"{'equal' if r['pages_json_match'] else 'DIFFERENT'} | "
                    f"{'identical' if r['osil']['identical_to_cache'] else 'DIFFERENT'} | "
                    f"{lm(r['osil']['last_modified'])} | {lm(r['gms']['last_modified'])} | "
                    f"{last[0]} {last[1]} {last[2]} |")
    return "\n".join(rows)


def table_b(names, with_flag=True):
    head = ("| instance | added | " + ("flagged listed duals (date) | " if with_flag else "best listed dual (date) | ")
            + "archived versions compared with the current OSIL | Internet Archive captures of the model files "
              "(= byte-identical, prefix = truncated capture equal to the start of the current file) | "
              "statistics snapshots equal to current |")
    rows = [head, "|---|---|---|---|---|---|"]
    for n in names:
        h = json.load(open(os.path.join(HERE, "data", "history", n + ".json")))
        p = P[n]
        if with_flag:
            du = "; ".join(f"{d['solver']} {d['value']} ({iso(d['date'])})" for d in p["duals"]
                           if d["solver"] in FLAG[n])
        else:
            vals = [(float(d["value"]), d) for d in p["duals"] if d["value"] not in (None, "", "inf", "-inf")]
            if vals:
                v, d = (max if p["sense"] == "min" else min)(vals, key=lambda t: t[0])
                du = f"{d['solver']} {d['value']} ({iso(d['date'])})"
            else:
                du = "none"
        srcs = []
        for s in h["sources"]:
            v = s.get("vs_minlplib_osil")
            lab = {"gamsworld-GlobalLib": "GLOBALLib", "gamsworld-MINLPLib": "MINLPLib 1",
                   "gamsworld-PrincetonLib": "PrincetonLib", "jl2017": "MINLPLib.jl"}[s["tag"]]
            txt = " (GAMS text identical)" if s.get("canonical_text_identical") else ""
            verdict = short_verdict(v["verdict"]) if v else "conversion failed"
            if lab == "PrincetonLib" and verdict == "DIFFERENT":
                verdict = (f"a different model ({v['nvars'][0]} vs {v['nvars'][1]} variables, "
                           f"{v['summary']['var_diffs']} bound differences), not a predecessor")
            srcs.append(f"{lab} {src_date(s)}: {verdict}{txt}")
        ch = S[n]["changes"]
        struct = [f for f in ch if f not in ("npolynomcons", "ngennlcons", "nsignomcons", "objtype", "adddate")]
        stats = ("no archived snapshot (instance too new)" if S[n]["present_in"] == ["current"] else
                 f"{S[n]['present_in'][0]} to current: " +
                 ("all equal" if not struct else "CHANGED: " + ", ".join(struct)) +
                 (" (only the constraint-class counts were reclassified)" if ch and not struct else ""))
        rows.append(f"| {n} | {iso(A['instances'][n]['page']['added_to_library'])} | {du} | "
                    f"{'; '.join(srcs) if srcs else 'none found'} | {wb(n)} | {stats} |")
    return "\n".join(rows)


if __name__ == "__main__":
    partb = I.AUDIT_I + I.AUDIT_IR + I.ROCKET
    rest = [n for n in I.ALL if n not in partb]
    txt = ("## Table A\n\n" + table_a() + "\n\n## Table B1 (audited)\n\n" + table_b(partb) +
           "\n\n## Table B2 (other)\n\n" + table_b(rest, with_flag=False) + "\n")
    open(os.path.join(HERE, "data", "tables.md"), "w").write(txt)
    print(txt[:3000])
