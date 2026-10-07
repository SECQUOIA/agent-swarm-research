"""Verify one listed point: route A (exact check as listed), else route B
(polish + Krawczyk, verify.verify_point). Writes logs/verify/<tag>.json.

Usage: python3 verify_one.py <name>.<pk> [--held v1,v2,...] [--max-n N] [--route-c-only]
"""
import json
import os
import sys
import time

import mpmath

import audit_eval as A
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))


def jsonable(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, mpmath.mpf):
            out[k] = mpmath.nstr(v, 25)
        elif isinstance(v, (list, tuple)) and len(v) > 40:
            out[k] = list(v[:40]) + ["..."]
        else:
            out[k] = v
    return out


def main(tag, held=(), max_n=4000):
    t0 = time.time()
    name = tag.rsplit(".", 1)[0]
    m = A.load(name)
    vals = A.read_sol(os.path.join(HERE, "sol", tag + ".sol"))
    res = V.exact_check(m, vals)
    if res["ok"]:
        res.update(status="proved", route="A (exactly feasible as listed)")
    else:
        why_a = res["reason"]
        if ROUTE_C_ONLY:
            res = V.verify_point_shift(m, vals, extra_fix=held, max_n=max_n, log=lambda s: print(s, flush=True))
            res["attempt"] = "shift (route C)"
        else:
            res = V.verify_point(m, vals, extra_fix=held, max_n=max_n, log=lambda s: print(s, flush=True))
        res["route"] = "B (polish + Krawczyk)"
        res["route_A_failure"] = why_a
    res["sec"] = round(time.time() - t0, 1)
    cen = res.pop("_center", None)
    if cen is not None:  # centre of the proof box (numerical cross-check only)
        with open(os.path.join(HERE, "logs", "verify", tag + ".center.sol"), "w") as f:
            for n, v in zip(m["names"], cen):
                f.write(f"{n} {v}\n")
    out = jsonable(res)
    os.makedirs(os.path.join(HERE, "logs", "verify"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "logs", "verify", tag + ".json"), "w"), indent=1)
    print(tag, out.get("status"), out.get("route"), out.get("obj_lo"), out.get("obj_hi"),
          out.get("reason", ""), out["sec"], flush=True)


ROUTE_C_ONLY = "--route-c-only" in sys.argv

if __name__ == "__main__":
    held = ()
    if "--held" in sys.argv:
        held = tuple(sys.argv[sys.argv.index("--held") + 1].split(","))
    max_n = int(sys.argv[sys.argv.index("--max-n") + 1]) if "--max-n" in sys.argv else 4000
    main(sys.argv[1], held, max_n)
