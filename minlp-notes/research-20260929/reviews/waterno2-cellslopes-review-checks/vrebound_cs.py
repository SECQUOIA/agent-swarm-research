"""Re-bound the pair records of a cell-slope certificate (waterno2_06) with the
recheck's vbb2.py through my own driver.

Nothing from the authors' code (cellslopes/, sepbranch/, rbb.py) is imported,
and the earlier review's rebound.py is not used either.
  * model, period split, link order, Lagrangian objective: first verifier's
    vmodel / vbb.Period, with vbb2's outward-rounded float propagation;
    objective of period t: cost_t + lam_in . x_start(t) - lam_out . x_end(t)
    (vmodel.period_objective with lam[t-1] = lam_in, lam[t] = lam_out, mu = 0);
  * variable bounds: OSIL bounds and the first verifier's implied bounds
    (my_implied_06.json), intersected with the task's entry box (on the start
    copies x_start(t,k) = link t-1, k) and exit box (on the end copies
    x_end(t,k) = link t, k);
  * last period: terminal row 1/2 x253 + 1/5 x265 + 4/9 x277 >= 3913/900
    (derived independently by the earlier review; re-derived in
    terminal_check.py), added to the exact LP rows and to the float FBBT rows.

Tasks (selection file, list of dicts):
  kind "rec":  a record: its own stored boxes, its own slopes, target = its rbb
               bound (records with bound +inf: target 1e4);
  kind "leaf": a leaf pair: the leaf boxes, the LEAF slopes and target = the
               exact pair bound of the DP rounded down to a float (checks the
               record and the Lemma-2 correction together).
vbb.solve returns status "infeasible" only if FBBT / OBBT WITHOUT objective
cutoff prove the box empty; "certified" iff the bound equals the target.

usage: python3 vrebound_cs.py cert.pkl.gz selection.json out.jsonl workers time_limit
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import contextlib
import io
import json
import math
import multiprocessing as mp
import sys
import time
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-recheck")
sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vbb  # noqa: E402
import vbb2  # noqa: E402
import vmodel  # noqa: E402

T = 6
IMPLIED = _RESEARCH + "/reviews/waterno2-verification/logs/my_implied_06.json"
TERM_COEF = (("x253", F(1, 2)), ("x265", F(1, 5)), ("x277", F(4, 9)))
TERM_RHS = F(3913, 900)
_G = {}


def _init():
    I = vmodel.instance(T)
    imp = json.load(open(IMPLIED))
    imp = imp.get("bounds", imp)
    _G["I"] = I
    _G["imp"] = {n: (F(a), F(b)) for n, (a, b) in imp.items()}


def build(t, cin, cout, lam_in, lam_out):
    I = _G["I"]
    names = I["m"]["names"]
    extra = dict(_G["imp"])

    def clip(v, lo, hi):
        n = names[v]
        lo, hi = F(float(lo)), F(float(hi))
        if n in extra:
            lo, hi = max(lo, extra[n][0]), min(hi, extra[n][1])
        extra[n] = (lo, hi)
    if t > 0:
        for k, (i, a, b) in enumerate(I["links"][t - 1]):   # b = x_start(t, k)
            clip(b, cin[0][k], cin[1][k])
    if t < T - 1:
        for k, (i, a, b) in enumerate(I["links"][t]):       # a = x_end(t, k)
            clip(a, cout[0][k], cout[1][k])
    if any(lo > hi for lo, hi in extra.values()):
        return None
    lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = [float(v) for v in lam_in]
    if t < T - 1:
        lam[t] = [float(v) for v in lam_out]
    P = vbb2.PeriodF(T, t, lam, 0.0, extra)
    if t == T - 1:
        cols = [P.names.index(n) for n, _ in TERM_COEF]
        cf = [a for _, a in TERM_COEF]
        P.rows.append((cols, cf, TERM_RHS, None, "terminal"))
        P.static.append((cols, [-a for a in cf], -TERM_RHS, False))
        P.frows.append((cols, [vbb2.fdn(a) for a in cf], [vbb2.fup(a) for a in cf], [True] * 3,
                        vbb2.fdn(TERM_RHS), None))
    return P


def run(task):
    if not _G:
        _init()
    tic = time.time()
    P = build(task["t"], task["cin_box"], task["cout_box"], task["lam_in"], task["lam_out"])
    if P is None:
        return task["key"], dict(status="infeasible", bound="inf", nodes=0, time=time.time() - tic, note="empty box")
    with contextlib.redirect_stdout(io.StringIO()):
        res = vbb.solve(P, task["target"], 10**6, task["tl"], True, False)
    res["time"] = time.time() - tic
    return task["key"], res


def main():
    pkl, selp, outp, workers, tl = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
    import load_cs
    d = load_cs.load(pkl)
    recs, cells, leaves, lamd = d["recs"], d["cells"], d["leaves"], d["lam"]
    sel = json.load(open(selp))
    done = set()
    try:
        for line in open(outp):
            done.add(json.loads(line)["key"])
    except FileNotFoundError:
        pass
    tasks = []
    for s in sel:
        key = s["key"]
        if key in done:
            continue
        if s["kind"] == "rec":
            r = recs[s["rid"]]
            target = r["bound"] if math.isfinite(r["bound"]) else 1e4
            tasks.append(dict(key=key, t=r["t"], cin_box=r["cin_box"], cout_box=r["cout_box"],
                              lam_in=list(r["lam_in"]), lam_out=list(r["lam_out"]), target=target, tl=tl))
        else:
            t, rr, cc = s["t"], s["r"], s["c"]
            b = F(s["bound"])
            tf = float(b)
            if F(tf) > b:
                tf = math.nextafter(tf, -math.inf)
            cin = None if t == 0 else (cells[t - 1][leaves[t - 1][rr]]["lo"], cells[t - 1][leaves[t - 1][rr]]["hi"])
            cout = None if t == T - 1 else (cells[t][leaves[t][cc]]["lo"], cells[t][leaves[t][cc]]["hi"])
            lin = [0.0, 0.0, 0.0] if t == 0 else list(lamd[t - 1][leaves[t - 1][rr]])
            lout = [0.0, 0.0, 0.0] if t == T - 1 else list(lamd[t][leaves[t][cc]])
            tasks.append(dict(key=key, t=t, cin_box=cin, cout_box=cout, lam_in=lin, lam_out=lout, target=tf, tl=tl))
    print(f"{len(tasks)} tasks to run ({len(done)} already done)", flush=True)
    info = {s["key"]: s for s in sel}
    targets = {tk["key"]: tk["target"] for tk in tasks}
    fh = open(outp, "a")
    tic = time.time()
    n = 0
    with mp.Pool(workers, initializer=_init) as pool:
        for key, res in pool.imap_unordered(run, tasks, chunksize=1):
            s = info[key]
            line = dict(key=key, kind=s["kind"], group=s["group"], rid=s.get("rid"),
                        t=s["t"] if s["kind"] == "leaf" else recs[s["rid"]]["t"],
                        vbb2_status=res.get("status"), vbb2_bound=str(res.get("bound")), nodes=res.get("nodes"),
                        time=round(res["time"], 2), target=targets[key])
            fh.write(json.dumps(line) + "\n")
            fh.flush()
            n += 1
            if n % 500 == 0:
                print(f"{n}/{len(tasks)} done, {time.time()-tic:.0f}s", flush=True)
    print(f"all {n} done in {time.time()-tic:.0f}s", flush=True)


if __name__ == "__main__":
    main()
