"""Independent re-bounding of certification records of a separator-branching
certificate (waterno2_06) with the recheck's vbb2 (not the authors' rbb.py).

Own driver; nothing from the authors' sepbranch/ code is imported:
  * model, period split, link order and Lagrangian objective: first verifier's
    vmodel / vbb.Period (links in row order; x_end(t,k) = x_start(t+1,k));
  * variable bounds: OSIL bounds and the FIRST VERIFIER'S implied bounds
    (reviews/waterno2-verification/logs/my_implied_06.json), intersected with the
    record's stored entry / exit cell boxes (entry box on the start copies of
    period t, exit box on the end copies);
  * last period: the terminal row 1/2 x253 + 1/5 x265 + 4/9 x277 >= 3913/900
    as derived independently in ind_verify.py;
  * slopes: the record's lam_in / lam_out (checked equal to the plan's slopes by
    ind_verify.py), mu = 0.
Target: the record's rbb bound (finite records); for records with rbb bound
+inf, the smallest value that keeps the DP value unchanged ("required"), and
infeasibility is reported if vbb2 proves it.

usage: python3 rebound.py cert.pkl selection.json out.jsonl workers time_limit
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import contextlib
import io
import json
import math
import sys
import time
import multiprocessing as mp
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-recheck")
sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vbb  # noqa: E402
import vbb2  # noqa: E402
import vmodel  # noqa: E402

T = 6
IMPLIED = _RESEARCH + "/reviews/waterno2-verification/logs/my_implied_06.json"
TERM = ({"x253": F(1, 2), "x265": F(1, 5), "x277": F(4, 9)}, F(3913, 900))


class _TermBase(vbb.Period):
    def __init__(self, T_, t, lam, mu, extra=None, term=None):
        super().__init__(T_, t, lam, mu, extra)
        if term is not None:
            coef, lb = term
            cols = [self.names.index(n) for n in coef]
            cf = [coef[n] for n in coef]
            self.rows.append((cols, cf, lb, None, "terminal"))
            self.static.append((cols, [-a for a in cf], -lb, False))


class Pair(vbb2.PeriodF, _TermBase):
    """vbb2's float-interval FBBT (built from self.rows, which now include the
    terminal row) on top of vbb's exact relaxation / node bound."""


def run(task):
    rid, rec, target, tl = task
    I = vmodel.instance(T)
    names = I["m"]["names"]
    t = rec["t"]
    imp = json.load(open(IMPLIED))
    extra = {n: (F(a), F(b)) for n, (a, b) in imp.items()}

    def put(n, lo, hi):
        lo, hi = F(lo), F(hi)
        if n in extra:
            lo, hi = max(lo, extra[n][0]), min(hi, extra[n][1])
        extra[n] = (lo, hi)
    if t > 0:
        for k, (i, a, b) in enumerate(I["links"][t - 1]):
            put(names[b], rec["cin_box"][0][k], rec["cin_box"][1][k])
    if t < T - 1:
        for k, (i, a, b) in enumerate(I["links"][t]):
            put(names[a], rec["cout_box"][0][k], rec["cout_box"][1][k])
    tic = time.time()
    if any(lo > hi for lo, hi in extra.values()):
        return rid, dict(status="empty box", nodes=0, time=0.0, target=target)
    lam = [[0.0, 0.0, 0.0] for _ in range(T - 1)]
    if t > 0:
        lam[t - 1] = [float(v) for v in rec["lam_in"]]
    if t < T - 1:
        lam[t] = [float(v) for v in rec["lam_out"]]
    P = Pair(T, t, lam, 0.0, extra, term=TERM if t == T - 1 else None)
    with contextlib.redirect_stdout(io.StringIO()):
        res = vbb.solve(P, target, 10**6, tl, True, False)
    res["time"] = time.time() - tic
    res["target"] = target
    return rid, res


def main():
    pkl, selp, out, workers, tl = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
    import load_cert
    P = load_cert.load(pkl).__dict__
    sel = json.load(open(selp))
    byid = {s["rid"]: s for s in sel}
    done = set()
    try:
        for line in open(out):
            done.add(json.loads(line)["rid"])
    except FileNotFoundError:
        pass
    tasks = []
    for item in sel:
        rid = item["rid"]
        if rid in done:
            continue
        rec = P["crecs"][rid]
        target = rec["bound"] if math.isfinite(rec["bound"]) else item["required"]
        tasks.append((rid, rec, target, tl))
    print(f"{len(tasks)} tasks", flush=True)
    fh = open(out, "a")
    with mp.Pool(workers) as pool:
        for rid, res in pool.imap_unordered(run, tasks):
            rec = P["crecs"][rid]
            item = byid[rid]
            line = dict(rid=rid, t=rec["t"], group=item["group"], rbb_bound=rec["bound"], rbb_status=rec["status"],
                        rbb_nodes=rec["nodes"], required=item["required"], vbb2_status=res.get("status"),
                        vbb2_bound=res.get("bound"), vbb2_nodes=res.get("nodes"), time=round(res["time"], 1),
                        target=res["target"])
            fh.write(json.dumps(line) + "\n")
            fh.flush()
            print(json.dumps(line), flush=True)


if __name__ == "__main__":
    main()
