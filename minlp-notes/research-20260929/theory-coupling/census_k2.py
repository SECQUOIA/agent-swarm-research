"""Bag-targeted greedy count of coupling rows (second heuristic).

Same graph and free rows as census_k.py. Repeat: run min-degree elimination,
take the bag (eliminated vertex plus neighbours) at which the width is first
attained, and remove the row node of largest degree in that bag. Stop when the
width upper bound is at most TARGET, after MAXR removals, or after TCAP
seconds. Records the width after every removal.

Usage: python3 census_k2.py OUT.jsonl [workers]
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[2])

import sys, os, json, time, heapq
from multiprocessing import Pool
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-coupling'))
from census_k import rowdata, fac_graph, read, OSIL_DIR, CENSUS, TARGET  # noqa: E402

MAXR = 64
TCAP = 240
ROWBASE = 2 * 10 ** 9


def width_and_bag(adj, tmax=30):
    adj = {v: set(nb) for v, nb in adj.items()}
    heap = [(len(nb), v) for v, nb in adj.items()]
    heapq.heapify(heap)
    width, bag = 0, []
    t0 = time.time()
    alive = set(adj)
    while heap:
        d, v = heapq.heappop(heap)
        if v not in alive or d != len(adj[v]):
            continue
        if d > width:
            width, bag = d, [v] + list(adj[v])
        if time.time() - t0 > tmax:
            return None, []
        nb = list(adj[v])
        for a in nb:
            adj[a].discard(v)
        for i, a in enumerate(nb):
            for b in nb[i + 1:]:
                if b not in adj[a]:
                    adj[a].add(b)
                    adj[b].add(a)
        for a in nb:
            heapq.heappush(heap, (len(adj[a]), a))
        alive.discard(v)
        del adj[v]
    return width, bag


def work(name):
    t0 = time.time()
    rec = {"name": name}
    try:
        I = read(os.path.join(OSIL_DIR, name + ".osil"))
    except Exception as e:  # pragma: no cover
        rec["error"] = str(e)[:100]
        return rec
    rows = rowdata(I)
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
    removed = set()
    trace = []
    k = None
    while True:
        adj = fac_graph(rows, free | removed)
        w, bag = width_and_bag(adj)
        trace.append((len(removed), w))
        if w is None:
            break
        if w <= TARGET:
            k = len(removed)
            break
        if len(removed) >= MAXR or time.time() - t0 > TCAP:
            break
        rnodes = [v for v in bag if isinstance(v, int) and v >= ROWBASE]
        if not rnodes:
            break  # width not caused by a row hub
        best = max(rnodes, key=lambda v: len(adj[v]))
        removed.add(best - ROWBASE - 1)
    rec["trace"] = trace
    rec["k_bag"] = k
    rec["removed_degrees"] = [len(rows[r][0]) + len(rows[r][1]) for r in removed]
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
    size = {r["name"]: r["n"] for r in sel}
    names = sorted((r["name"] for r in sel if r["name"] not in done), key=lambda s: size[s])
    with open(out, "a") as fo, Pool(workers) as pool:
        for rec in pool.imap_unordered(work, names):
            fo.write(json.dumps(rec) + "\n")
            fo.flush()


if __name__ == "__main__":
    main()
