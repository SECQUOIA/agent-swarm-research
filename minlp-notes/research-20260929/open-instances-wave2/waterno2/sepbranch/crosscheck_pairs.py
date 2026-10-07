"""Independent re-bounding of certified pair records with the recheck's B&B
(reviews/waterno2-recheck/vbb2.py: exact-rational node bounds, outward-rounded
propagation, shares no code with rbb.py).

For a record (period t, entry cell, exit cell, slopes, bound b), vbb2 is run on
the verifier's own period model with
  * the verifier's Lagrangian objective (vmodel.period_objective) for the
    record's slopes (zero multipliers on all other links, mu = record mu);
  * the authors' implied bounds (confirmed by the first verifier) intersected
    with the record's cell boxes (exact floats);
  * for the last period, the terminal row (terminal.py, derived exactly);
and target b.  "certified" means vbb2 proved phi >= b.

usage: python3 crosscheck_pairs.py cert_config.json selection out.json [time_limit] [workers]
  selection: "path" (records on the certified best path), "random:N:seed", or
             "path+random:N:seed"
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../../..'))
import json
import pickle
import random
import sys
import time
import multiprocessing as mp
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-recheck")
sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vbb  # noqa: E402
import vbb2  # noqa: E402
import vmodel  # noqa: E402

import core  # noqa: E402
import terminal  # noqa: E402
from dpcells import CellPlan  # noqa: E402,F401


class TermPeriod(vbb.Period):
    def __init__(self, T, t, lam, mu, extra=None, term=None):
        super().__init__(T, t, lam, mu, extra)
        if term is not None:
            names, coefs, lb = term
            cols = [self.names.index(n) for n in names]
            cf = [F(a) for a in coefs]
            self.rows.append((cols, cf, F(lb), None, "terminal"))
            self.static.append((cols, [-a for a in cf], -F(lb), False))


class PairF(vbb2.PeriodF, TermPeriod):
    pass


_G = {}


def _init(cfg):
    T = cfg["T"]
    D = core.setup(T, None)
    coef, const = terminal.derive(D)
    names = [D["M"]["names"][j] for j in coef]
    _G["term"] = (names, [coef[j] for j in coef], const)
    _G["implied"] = json.load(open(cfg["implied"]))["bounds"]
    _G["D"] = D
    _G["T"] = T


def _run(a):
    rid, rec, tl = a
    T, D = _G["T"], _G["D"]
    t = rec["t"]
    S = D["S"]
    names = D["M"]["names"]
    extra = {n: (F(lo), F(hi)) for n, (lo, hi) in _G["implied"].items()}

    def put(n, lo, hi):
        if n in extra:
            lo, hi = max(extra[n][0], F(lo)), min(extra[n][1], F(hi))
        extra[n] = (F(lo), F(hi))
    if t > 0:
        for k, (i, va, vb) in enumerate(S["link"][t - 1]):
            put(names[vb], rec["cin_box"][0][k], rec["cin_box"][1][k])
    if t < T - 1:
        for k, (i, va, vb) in enumerate(S["link"][t]):
            put(names[va], rec["cout_box"][0][k], rec["cout_box"][1][k])
    lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = rec["lam_in"]
    if t < T - 1:
        lam[t] = rec["lam_out"]
    if any(extra[n][0] > extra[n][1] for n in extra):
        return rid, dict(status="empty box", nodes=0, time=0.0)
    P = PairF(T, t, lam, rec["mu"], {n: (lo, hi) for n, (lo, hi) in extra.items()},
              term=_G["term"] if t == T - 1 else None)
    tic = time.time()
    import io
    import contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        res = vbb2.solve(P, rec["bound"], 10**7, tl)
    res["time"] = time.time() - tic
    return rid, res


def main():
    cfg = json.load(open(sys.argv[1]))
    sel = sys.argv[2]
    out = sys.argv[3]
    tl = float(sys.argv[4]) if len(sys.argv) > 4 else 1200.0
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 8
    P = pickle.load(open(cfg["out"] + ".pkl", "rb"))
    T = P.T
    ids = []
    if "path" in sel:
        V, f, g = P.dp("CB")
        path = P.best_path(f, g, "CB")
        for t in range(T):
            r = 0 if t == 0 else path[t - 1]
            c = 0 if t == T - 1 else path[t]
            ids.append(int(P.tables["CSRC"][t][r, c]))
    if "random" in sel:
        n, seed = sel.split("random:")[1].split(":")
        used = sorted({int(v) for t in range(T) for v in P.tables["CSRC"][t].ravel()} - set(ids))
        used = [i for i in used if P.crecs[i]["bound"] not in (float("inf"),)]
        random.seed(int(seed))
        ids += random.sample(used, min(int(n), len(used)))
    pool = mp.Pool(workers, initializer=_init, initargs=(cfg,))
    tasks = [(i, P.crecs[i], tl) for i in ids]
    res = {}
    for rid, r in pool.imap_unordered(_run, tasks):
        rec = P.crecs[rid]
        res[rid] = dict(t=rec["t"], rbb_bound=rec["bound"], rbb_status=rec["status"], vbb2=r)
        print(f"record {rid} period {rec['t']}: rbb bound {rec['bound']!r} -> vbb2 {r.get('status')} "
              f"bound {r.get('bound')} nodes {r.get('nodes')} {r['time']:.0f}s", flush=True)
    pool.close()
    json.dump(res, open(out, "w"), indent=1)
    ok = sum(1 for v in res.values() if v["vbb2"].get("status") in ("certified", "infeasible"))
    print(f"{ok}/{len(res)} records re-certified by vbb2")


if __name__ == "__main__":
    main()
