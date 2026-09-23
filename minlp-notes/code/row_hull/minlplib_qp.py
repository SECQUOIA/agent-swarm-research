"""Row-hull root cuts on MINLPLib instances that are separable concave quadratic programs with linear
constraints (continuous, finite bounds, minimization, diagonal objective with no positive square).
python minlplib_qp.py out.jsonl [names...]   (no names: scan the whole local library)"""
import glob, json, math, os, sys, time
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "vertex_binarization"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "univariate_envelopes"))
from uenv.osil import read_osil
from sob.functions import X, Univariate, Piece
from sob.model import SeparableProblem, original_ir
from sob.backends import SOLVERS
from rowhull.strengthen import cut_loop, cut_ir

OSIL = os.path.expanduser("~/.cache/minlplib/minlplib/osil")


def load(name):
    path = f"{OSIL}/{name}.osil"
    if os.path.getsize(path) > 2_000_000:
        return None
    try:
        ins = read_osil(path)
    except Exception:  # noqa: BLE001
        return None
    n = len(ins.var_lb)
    if ins.obj_sense != "min" or any(t != "C" for t in ins.var_type) or n > 400:
        return None
    if any(not math.isfinite(a) or not math.isfinite(b) for a, b in zip(ins.var_lb, ins.var_ub)):
        return None
    obj, cons = ins.rows[0], ins.rows[1:]
    if obj["nl"] is not None or any(r["nl"] is not None or r["quad"] for r in cons) or not cons:
        return None
    c2 = np.zeros(n)
    for i, j, c in obj["quad"]:
        if i != j:
            return None
        c2[i] += c
    if (c2 > 0).any() or not (c2 < 0).any():
        return None
    funcs = []
    for i in range(n):
        expr = sp.Float(c2[i]) * X**2 + sp.Float(obj["lin"].get(i, 0.0)) * X
        lo, hi = ins.var_lb[i], ins.var_ub[i]
        if hi - lo < 1e-12:
            hi = lo + 1e-9
        funcs.append(Univariate(expr, lo, hi, pieces=[Piece(lo, hi, bool(c2[i] < 0), expr)]))
    A, sense, b = [], [], []
    for r in cons:
        row = np.zeros(n)
        for k, v in r["lin"].items():
            row[k] = v
        if r["lb"] == r["ub"]:
            A.append(row); sense.append("=="); b.append(r["ub"])
        else:
            if math.isfinite(r["ub"]):
                A.append(row); sense.append("<="); b.append(r["ub"])
            if math.isfinite(r["lb"]):
                A.append(row.copy()); sense.append(">="); b.append(r["lb"])
    return SeparableProblem(name, funcs, np.array(A), sense, np.array(b)), ins.obj_const


if __name__ == "__main__":
    out = sys.argv[1]
    names = sys.argv[2:] or sorted(Path(p).stem for p in glob.glob(f"{OSIL}/*.osil"))
    with open(out, "a") as fh:
        for name in names:
            got = load(name)
            if got is None:
                continue
            p, const = got
            t0 = time.time()
            try:
                cuts, extra, info = cut_loop(p, time_limit=60)
            except Exception as e:  # noqa: BLE001
                print(name, "cut loop failed", repr(e)); continue
            rec = {"name": name, "n": p.n, "rows": int(p.A.shape[0]), "cutinfo": info, "obj_const": const}
            for form, ir in (("orig", original_ir(p)), ("cuts", cut_ir(p, cuts, extra))):
                r = SOLVERS["gurobi"](ir, 60, threads=4); r.pop("x", None)
                rec[form] = r
            fh.write(json.dumps(rec) + "\n"); fh.flush()
            best = min(rec["orig"]["primal"], rec["cuts"]["primal"])
            b0, b1 = info["bound0"], info["bound"]
            clos = 100 * (b1 - b0) / max(best - b0, 1e-9) if b0 is not None else float("nan")
            print(f"{name:14s} n={p.n:3d} rows={p.A.shape[0]:3d} closed {clos:5.1f}%  cutloop {info['time']:.1f}s "
                  f"orig {rec['orig']['nodes']:.0f} nodes {rec['orig']['time']:.2f}s | cuts {rec['cuts']['nodes']:.0f} nodes {rec['cuts']['time']:.2f}s "
                  f"opt {best + const:.4f}", flush=True)
