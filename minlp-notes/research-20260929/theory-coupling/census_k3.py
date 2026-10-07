"""Coupling-row counts restricted to the rows the theory covers (revision).

Reruns both greedy rules of census_k.py / census_k2.py with only eligible rows
removable:
  'lin'   : linear rows (no quadratic or nonlinear terms), equality or inequality
            (inequalities are covered through slack variables);
  'lineq' : linear equality rows (lb == ub).
Free rows (objective, objective-defining rows) are dropped as before, and the
starting width is min(w_full, w_free), because the min-degree bound is not
monotone under row removal. k is the smallest number of removed eligible rows
after which the bound is at most 12 (densest-first schedule as in census_k.py;
bag-targeted rule as in census_k2.py, capped at 64 rows or 240 s).

Run only on the instances where the unrestricted rules reached width 12 with
1..64 rows (restricting the eligible rows is expected to make the greedy rules
worse, not better; other instances keep their unrestricted status).

Usage: python3 census_k3.py OUT.jsonl [workers]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys, os, json, time
from multiprocessing import Pool
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-coupling'))
from census_k import rowdata, fac_graph, read, OSIL_DIR, CENSUS, TARGET, SCHEDULE  # noqa: E402
from census_k2 import width_and_bag, ROWBASE, MAXR, TCAP  # noqa: E402
from census import min_degree_width  # noqa: E402


def row_types(I):
    t = {}
    for r, row in I["rows"].items():
        if r == -1:
            continue
        lin = not row["quad"] and row["nl"] is None
        eq = row["lb"] is not None and row["ub"] is not None and row["lb"] == row["ub"]
        t[r] = (lin, eq)
    return t


def free_rows(I, rows):
    obj_lin = set(I["rows"][-1]["lin"]) if -1 in I["rows"] else set()
    occ = {}
    for r, (lin, terms) in rows.items():
        if r == -1:
            continue
        vs = set(lin)
        for s in terms:
            vs |= s
        for v in vs:
            occ.setdefault(v, []).append(r)
    free = {-1}
    for v in obj_lin:
        if len(occ.get(v, [])) == 1:
            free.add(occ[v][0])
    return free


def work(name):
    t0 = time.time()
    rec = {"name": name}
    I = read(os.path.join(OSIL_DIR, name + ".osil"))
    rows = rowdata(I)
    types = row_types(I)
    free = free_rows(I, rows)
    w_full = min_degree_width(fac_graph(rows, set()), tmax=30)
    w_free = min_degree_width(fac_graph(rows, free), tmax=30)
    base = min(w for w in (w_full, w_free) if w is not None) if (w_full or w_free) else None
    rec["w_full"], rec["w_free"], rec["w0"] = w_full, w_free, base
    for mode in ("lin", "lineq"):
        ok = {r for r, (lin, eq) in types.items() if r in rows and r not in free
              and lin and (eq or mode == "lin")}
        if base is not None and base <= TARGET:
            rec[f"k_dense_{mode}"] = rec[f"k_bag_{mode}"] = 0
            continue
        # densest first
        cand = sorted(ok, key=lambda r: -(len(rows[r][0]) + len(rows[r][1])))
        kd = None
        for r in SCHEDULE:
            if r > len(cand):
                break
            w = min_degree_width(fac_graph(rows, free | set(cand[:r])), tmax=30)
            if w is not None and w <= TARGET:
                kd = r
                break
        rec[f"k_dense_{mode}"] = kd
        # bag targeted
        removed, kb, t1 = set(), None, time.time()
        while True:
            adj = fac_graph(rows, free | removed)
            w, bag = width_and_bag(adj)
            if w is None:
                break
            if w <= TARGET:
                kb = len(removed)
                break
            if len(removed) >= MAXR or time.time() - t1 > TCAP:
                break
            rn = [v for v in bag if isinstance(v, int) and v >= ROWBASE and (v - ROWBASE - 1) in ok]
            if not rn:
                break
            best = max(rn, key=lambda v: len(adj[v]))
            removed.add(best - ROWBASE - 1)
        rec[f"k_bag_{mode}"] = kb
    rec["secs"] = round(time.time() - t0, 1)
    return rec


def main():
    out = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    base = (_PUBLIC_REPO + '/research-20260929/theory-coupling/logs/')
    r1 = {json.loads(l)["name"]: json.loads(l) for l in open(base + "census_k.jsonl")}
    r2 = {json.loads(l)["name"]: json.loads(l) for l in open(base + "census_k2.jsonl")}
    names = []
    for n in set(r1) | set(r2):
        ks = [v for v in (r1.get(n, {}).get("k_heur"), r2.get(n, {}).get("k_bag")) if v is not None]
        if ks and 1 <= min(ks) <= 64:
            names.append(n)
    names.sort()
    with open(out, "w") as fo, Pool(workers) as pool:
        for rec in pool.imap_unordered(work, names):
            fo.write(json.dumps(rec) + "\n")
            fo.flush()


if __name__ == "__main__":
    main()
