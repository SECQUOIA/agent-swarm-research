"""Heuristic count of dense coupling rows for MINLPLib instances.

For each instance, build the factor-incidence graph of the treewidth census
(variables, row nodes, nonlinear-term nodes), then:

1. remove "free" rows: the objective row and objective-defining rows (a row
   that is the only constraint containing a variable with a linear objective
   coefficient). Their terms are summed by any DP, so they are not coupling
   rows;
2. sort the remaining constraint rows by degree in the factor-incidence graph
   (densest first) and remove the r densest rows for r in SCHEDULE, recomputing
   the min-degree width upper bound, until it is at most TARGET.

k_heur = smallest r in SCHEDULE with width <= TARGET (None if not reached).
Widths are heuristic upper bounds (min-degree elimination), as in the census.

Usage: python3 census_k.py OUT.jsonl [workers]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys, os, json, time
from multiprocessing import Pool
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/treewidth-census'))
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260922/scouting/minlplib-open-data'))
from census import min_degree_width, split_terms  # noqa: E402
from osil import read, V  # noqa: E402

OSIL_DIR = os.path.expanduser("~/.cache/minlplib/minlplib/osil")
CENSUS = (_PUBLIC_REPO + '/research-20260929/treewidth-census/census_merged.json')
SCHEDULE = [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64]
TARGET = 12
TMAX = 30


def rowdata(I):
    """Per row id: (linear variable set, list of nonlinear-term variable sets)."""
    out = {}
    for r, row in I["rows"].items():
        lin = set(row["lin"])
        terms = [{a, b} for (a, b, c) in row["quad"]]
        if row["nl"] is not None:
            for tt in split_terms(row["nl"]):
                s = V(tt)
                if s:
                    terms.append(set(s))
        if lin or terms:
            out[r] = (lin, terms)
    return out


def fac_graph(rows, skip):
    adj = {}
    nxt = [10 ** 9]

    def add(a, b):
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    for r, (lin, terms) in rows.items():
        if r in skip:
            # a removed row: keep its nonlinear terms as factors (they still
            # need a bag), drop the row hub that couples them
            for s in terms:
                if len(s) >= 2:
                    tn = nxt[0]; nxt[0] += 1
                    for v in s:
                        add(tn, v)
                else:
                    adj.setdefault(next(iter(s)), set())
            for v in lin:
                adj.setdefault(v, set())
            continue
        rn = 2 * 10 ** 9 + r + 1
        adj.setdefault(rn, set())
        for v in lin:
            add(rn, v)
        for s in terms:
            if len(s) == 1:
                add(rn, next(iter(s)))
            else:
                tn = nxt[0]; nxt[0] += 1
                add(rn, tn)
                for v in s:
                    add(tn, v)
    return adj


def degree(lin, terms):
    return len(lin) + len(terms)


def work(name):
    t0 = time.time()
    p = os.path.join(OSIL_DIR, name + ".osil")
    rec = {"name": name}
    try:
        I = read(p)
    except Exception as e:  # pragma: no cover
        rec["error"] = str(e)[:100]
        return rec
    rows = rowdata(I)
    # free rows
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
    rec["n_free"] = len(free) - 1
    rec["w_full"] = min_degree_width(fac_graph(rows, set()), tmax=TMAX)
    w0 = min_degree_width(fac_graph(rows, free), tmax=TMAX)
    rec["w_free"] = w0
    cand = sorted((r for r in rows if r not in free),
                  key=lambda r: -degree(*rows[r]))
    rec["top_degrees"] = [degree(*rows[r]) for r in cand[:8]]
    trace = [(0, w0)]
    k = 0 if (w0 is not None and w0 <= TARGET) else None
    if k is None:
        for r in SCHEDULE:
            if r > len(cand):
                break
            w = min_degree_width(fac_graph(rows, free | set(cand[:r])), tmax=TMAX)
            trace.append((r, w))
            if w is not None and w <= TARGET:
                k = r
                break
            if time.time() - t0 > 600:
                break
    rec["trace"] = trace
    rec["k_heur"] = k
    rec["deg_kth"] = degree(*rows[cand[k - 1]]) if k else None
    rec["secs"] = round(time.time() - t0, 1)
    return rec


def main():
    out = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    d = json.load(open(CENSUS))
    sel = [r for r in d if not r["convex"] and r["n_nl"] >= 100]
    done = set()
    if os.path.exists(out):
        for line in open(out):
            done.add(json.loads(line)["name"])
    names = [r["name"] for r in sel if r["name"] not in done]
    # small instances first so partial results are useful
    size = {r["name"]: r["n"] for r in sel}
    names.sort(key=lambda s: size[s])
    with open(out, "a") as fo, Pool(workers) as pool:
        for rec in pool.imap_unordered(work, names):
            fo.write(json.dumps(rec) + "\n")
            fo.flush()


if __name__ == "__main__":
    main()
