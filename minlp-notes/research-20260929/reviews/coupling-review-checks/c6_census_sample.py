"""Rerun the coupling-row census heuristics on a sample and classify the
removed rows.

1. Reruns census_k.work and census_k2.work (the author's code) on a sample
   and compares k_heur, k_bag and traces with logs/census_k*.jsonl.
2. For the bag-targeted rule, replays the removal loop (same code path as
   census_k2.work) but records the removed row ids, and classifies each as
   linear/nonlinear and equality/inequality, and counts integer variables.
   The note's theory (Sections 2-4) is for linear rows; Theorems 3.1 and 4.5
   for linear equality rows.

Usage: python3 c6_census_sample.py
"""
from pathlib import Path as _PublicPath
_PUBLIC_REPO = str(_PublicPath(__file__).resolve().parents[3])

import sys, json, os, time
sys.path.insert(0, (_PUBLIC_REPO + '/research-20260929/theory-coupling'))
import census_k as ck  # noqa: E402
import census_k2 as ck2  # noqa: E402

LOGD = (_PUBLIC_REPO + '/research-20260929/theory-coupling/logs')
SAMPLE = ["ann_cumene_tanh", "powerflow0030p", "transswitch0030r", "sfacloc1_4_95",
          "sfacloc1_3_90", "wastepaper6", "waterno1_03", "waterno1_04", "tln12",
          "kall_ellipsoids_tc03c", "waternd_pescara", "waternd_fossiron", "waterful2",
          "casctanks", "waterno2_03", "kriging_peaks-full100"]


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


def replay_bag(name):
    I = ck.read(os.path.join(ck.OSIL_DIR, name + ".osil"))
    rows = ck.rowdata(I)
    free = free_rows(I, rows)
    removed = []
    t0 = time.time()
    while True:
        adj = ck.fac_graph(rows, free | set(removed))
        w, bag = ck2.width_and_bag(adj)
        if w is None or w <= ck.TARGET or len(removed) >= ck2.MAXR or time.time() - t0 > ck2.TCAP:
            break
        rnodes = [v for v in bag if isinstance(v, int) and v >= ck2.ROWBASE]
        if not rnodes:
            break
        best = max(rnodes, key=lambda v: len(adj[v]))
        removed.append(best - ck2.ROWBASE - 1)
    cls = []
    for r in removed:
        row = I["rows"][r]
        nonlin = bool(row["quad"]) or row["nl"] is not None
        eq = row["lb"] == row["ub"]
        ints = sum(1 for v in row["lin"] if I["vt"][v] in "BI")
        cls.append(("NL" if nonlin else "L") + ("=" if eq else "<>") + (f"/int{ints}" if ints else ""))
    return w, removed, cls


if __name__ == "__main__":
    L1 = {json.loads(l)["name"]: json.loads(l) for l in open(os.path.join(LOGD, "census_k.jsonl"))}
    L2 = {json.loads(l)["name"]: json.loads(l) for l in open(os.path.join(LOGD, "census_k2.jsonl"))}
    for nm in SAMPLE:
        a = ck.work(nm)
        b = ck2.work(nm)
        same1 = (a.get("k_heur"), a.get("trace")) == (L1[nm].get("k_heur"), [list(x) for x in L1[nm]["trace"]]) or \
                (a.get("k_heur"), [list(x) for x in a.get("trace", [])]) == (L1[nm].get("k_heur"), L1[nm]["trace"])
        same2 = b.get("k_bag") == L2[nm].get("k_bag") and [list(x) for x in b["trace"]] == L2[nm]["trace"]
        w, removed, cls = replay_bag(nm)
        print(f"{nm}: k_heur={a.get('k_heur')} (log {L1[nm].get('k_heur')}, match={same1}) "
              f"k_bag={b.get('k_bag')} (log {L2[nm].get('k_bag')}, match={same2}) "
              f"w_free={a.get('w_free')} final_w={w} removed rows: {cls}", flush=True)
