"""Count composite univariate subexpressions (>= 2 nonlinear operators in one variable) per MINLPLib instance."""
import glob, json, os, sys
from concurrent.futures import ProcessPoolExecutor
from uenv.osil import collapse, read_osil

def scan(path):
    if os.path.getsize(path) > 30e6:
        return {"name": os.path.basename(path)[:-5], "status": "too large"}
    try:
        inst = read_osil(path)
    except NotImplementedError as e:
        return {"name": os.path.basename(path)[:-5], "status": f"unsupported operator {e}"}
    nl_rows = [r for r in inst.rows if r["nl"] is not None]
    found, bounded = [], 0
    for r in nl_rows:
        collapse(r["nl"], found)
    for vi, _ in found:
        bounded += inst.var_lb[vi] > -1e20 and inst.var_ub[vi] < 1e20
    return {"name": inst.name, "status": "ok", "nl_rows": len(nl_rows), "composite": len(found), "declared_bounded": bounded}

if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(sys.argv[1], "*.osil")))
    with ProcessPoolExecutor(16) as ex:
        rs = list(ex.map(scan, files, chunksize=8))
    json.dump(rs, open(sys.argv[2], "w"), indent=0)
    ok = [r for r in rs if r["status"] == "ok"]
    gen = [r for r in ok if r["nl_rows"]]
    comp = [r for r in gen if r["composite"]]
    print(f"files {len(rs)}, parsed {len(ok)}, with general nonlinear rows {len(gen)}, with composite univariate {len(comp)}")
    print("not parsed:", {s: sum(r['status'] == s for r in rs) for s in {r['status'] for r in rs} - {'ok'}})
