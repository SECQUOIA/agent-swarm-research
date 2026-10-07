"""Negative control for the re-bounding driver (own code).

For the leaf pairs that contain a known feasible point x (MINLPLib .sol), the
pair value is at most x's exact period Lagrangian value at the LEAF slopes
(x restricted to the period is feasible for the pair up to its row violation,
< 1e-9).  A driver that over-constrains the pair problem (wrong copy, wrong
slope sign, wrong box) could certify more.  Here vbb2 is asked to certify
value + 0.01; it must NOT succeed.

usage: python3 control_cs.py cert.pkl.gz sol out.jsonl time_limit
"""
import os as _os  # path of research-20260929 relative to this file (clean-checkout fix)
_RESEARCH = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '../..'))
import json
import multiprocessing as mp
import sys
from fractions import Fraction as F

sys.path.insert(0, _RESEARCH + "/reviews/waterno2-verification")
import vmodel  # noqa: E402
import load_cs  # noqa: E402
import vrebound_cs  # noqa: E402
from point_check_cs import read_sol  # noqa: E402

T = 6


def main():
    d = load_cs.load(sys.argv[1])
    cells, leaves, lam = d["cells"], d["leaves"], d["lam"]
    tl = float(sys.argv[4])
    I = vmodel.instance(T)
    m = I["m"]
    names = m["names"]
    x = read_sol(sys.argv[2], names)
    obj = {v: F(a) for v, a in m["obj"]["lin"].items()}
    lev = [[x[a] for (i, a, b) in I["links"][t]] for t in range(T - 1)]

    def leaf_of(link):
        out = [p for p, cid in enumerate(leaves[link])
               if all(F(cells[link][cid]["lo"][k]) <= lev[link][k] <= F(cells[link][cid]["hi"][k]) for k in range(3))]
        assert len(out) == 1
        return out[0]
    path = [leaf_of(l) for l in range(T - 1)]
    tasks = []
    for t in range(T):
        r = None if t == 0 else leaves[t - 1][path[t - 1]]
        c = None if t == T - 1 else leaves[t][path[t]]
        val = sum(obj.get(v, 0) * x[v] for v in I["per_vars"][t])
        lin = [0.0] * 3 if t == 0 else list(lam[t - 1][r])
        lout = [0.0] * 3 if t == T - 1 else list(lam[t][c])
        if t > 0:
            val += sum(F(lin[k]) * lev[t - 1][k] for k in range(3))
        if t < T - 1:
            val -= sum(F(lout[k]) * lev[t][k] for k in range(3))
        tasks.append(dict(key=f"control_t{t}", t=t,
                          cin_box=None if t == 0 else (cells[t - 1][r]["lo"], cells[t - 1][r]["hi"]),
                          cout_box=None if t == T - 1 else (cells[t][c]["lo"], cells[t][c]["hi"]),
                          lam_in=lin, lam_out=lout, target=float(val + F(1, 100)), tl=tl, value=float(val)))
    with mp.Pool(len(tasks), initializer=vrebound_cs._init) as pool:
        res = dict(pool.map(vrebound_cs.run, tasks))
    with open(sys.argv[3], "w") as fh:
        for tk in tasks:
            r = res[tk["key"]]
            b = r.get("bound")
            line = dict(t=tk["t"], point_value=tk["value"], target=tk["target"], vbb2_status=r.get("status"),
                        vbb2_bound=None if b is None else float(F(b)), nodes=r.get("nodes"),
                        time=round(r["time"], 1))
            print(json.dumps(line), flush=True)
            fh.write(json.dumps(line) + "\n")


if __name__ == "__main__":
    main()
