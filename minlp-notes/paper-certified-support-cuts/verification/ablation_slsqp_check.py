#!/usr/bin/env python3
"""Why SLSQP leaves materially invalid U2 constants (Part U diagnostic; offline, no solver).

Reads ``evidence/ablation-uncertified.json`` (output of ``ablation_uncertified.py``) and, for
every exact-certificate cut whose U2 constant is materially invalid, the cut's block (features,
box, binary64 direction) from its record file. For each recorded SLSQP start x0 it computes,
in binary64 with the same SymPy lambdify objective and gradient as ``ablation_uncertified.py``:

- ``pg``: the infinity norm of the projected gradient at x0 on the block box (the first-order
  optimality residual; every such cut has no domain rows, so the box is the feasible set);
- ``gs``: |g^T s| for s = clip(-g, lo - x0, hi - x0), the first search direction of SLSQP
  (its first quadratic subproblem uses the identity as Hessian; with box constraints only, its
  solution is this s). SLSQP stops with "Optimization terminated successfully" before any
  line search when this quantity (plus multiplier terms, zero here) is below ftol;
- the SLSQP result with the settings of ``ablation_uncertified.py`` (ftol 1e-6, maxiter 200),
  as a reproduction check of the recorded value and iteration count;
- the SLSQP result with ftol 1e-14 and maxiter 1000.

Each cut is classified by its best tight-tolerance value (exact rational comparison with the
certified value, same material tolerance 1e-6*max(1,|value|)): ``tight_reaches`` if the excess
becomes immaterial, else ``tight_local``. A start is called ``stationary`` if pg <= 1e-12.

    ablation_slsqp_check.py [--in-json PATH] [--out-json PATH]
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import os  # noqa: E402

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "1"

import argparse  # noqa: E402
import collections  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402
import warnings  # noqa: E402

import numpy as np  # noqa: E402
from scipy.optimize import minimize  # noqa: E402
import sympy as sp  # noqa: E402

HERE = Path(__file__).resolve().parent
MATERIAL = Q(1, 10**6)
STATIONARY = 1e-12


def load_cuts(records, wanted):
    """Cuts {(line, k): cut} of one record file, reading it once."""
    lines = {line for line, _ in wanted}
    found = {}
    with open(records, "rb") as handle:
        for i, raw in enumerate(handle):
            if i in lines:
                cuts = json.loads(raw)["cuts"]
                found.update({(i, k): cuts[k] for line, k in wanted if line == i})
    return found


def block_functions(cut):
    syms = tuple(sp.Symbol(s, real=True) for s in cut["symbols"])
    local = {str(s): s for s in syms}
    feats = [sp.sympify(f, locals=local) for f in cut["features"]]
    c = np.asarray([float(x) for x in cut["coefficients"]], dtype=float)
    fs = [sp.lambdify(syms, f, "numpy") for f in feats]
    gs = [[sp.lambdify(syms, sp.diff(f, s), "numpy") for s in syms] for f in feats]

    def fun(u):
        return float(c @ np.array([float(f(*u)) for f in fs]))

    def jac(u):
        return c @ np.array([[float(g(*u)) for g in row] for row in gs])

    box = [(float(Q(lo)), float(Q(hi))) for lo, hi in cut["box"]]
    return fun, jac, box


def projected_gradient(g, x, box):
    out = []
    for gi, xi, (lo, hi) in zip(g, x, box):
        if xi <= lo:
            out.append(min(gi, 0.0))
        elif xi >= hi:
            out.append(max(gi, 0.0))
        else:
            out.append(gi)
    return np.asarray(out)


def first_directional_derivative(g, x, box):
    """|g.s| for s = argmin g.s + |s|^2/2 over the box shifted to x."""
    return abs(sum(gi * min(max(-gi, lo - xi), hi - xi) for gi, xi, (lo, hi) in zip(g, x, box)))


def run_slsqp(fun, jac, x0, box, ftol, maxiter):
    with warnings.catch_warnings(), np.errstate(all="ignore"):
        warnings.simplefilter("ignore")
        res = minimize(fun, x0, jac=jac, method="SLSQP", bounds=box,
                       options={"ftol": ftol, "maxiter": maxiter})
    x = np.clip(np.asarray(res.x, dtype=float), [b[0] for b in box], [b[1] for b in box])
    return {"value": fun(x), "nit": int(res.nit), "status": int(res.status),
            "moved": float(np.max(np.abs(x - x0)))}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--in-json", type=Path, default=HERE.parent / "evidence" / "ablation-uncertified.json")
    ap.add_argument("--out-json", type=Path, default=HERE.parent / "evidence" / "ablation-slsqp-check.json")
    args = ap.parse_args()
    data = json.loads(args.in_json.read_text())
    records = {p["label"]: p["records"] for p in data["meta"]["parts"]}
    rows = [r for r in data["cuts"] if r["exact_certificate"] and r.get("u2_material")]
    wanted = collections.defaultdict(set)
    for r in rows:
        wanted[r["part"]].add((r["line"], r["cut"]))
    cuts = {(part, line, k): cut for part, pairs in wanted.items()
            for (line, k), cut in load_cuts(records[part], pairs).items()}
    out = []
    for r in rows:
        if r["domain_rows"]:
            raise SystemExit("cut with domain rows: the box-only analysis does not apply")
        cut = cuts[(r["part"], r["line"], r["cut"])]
        if cut["coefficients"] != r["coefficients"]:
            raise SystemExit(f"record/JSON mismatch at {r['part']} line {r['line']}")
        fun, jac, box = block_functions(cut)
        certified = Q(r["certified"])
        scale = MATERIAL * max(Q(1), abs(certified))
        starts = []
        for rec in r["slsqp"]:
            x0 = np.asarray(rec["start"], dtype=float)
            g = jac(x0)
            default = run_slsqp(fun, jac, x0, box, 1e-6, 200)
            tight = run_slsqp(fun, jac, x0, box, 1e-14, 1000)
            starts.append({
                "f0": fun(x0), "pg": float(np.max(np.abs(projected_gradient(g, x0, box)))),
                "gs": first_directional_derivative(g, x0, box),
                "default": default, "tight": tight,
                "default_reproduces": (default["nit"] == rec.get("nit") and
                                       rec.get("value") is not None and
                                       abs(default["value"] - float.fromhex(rec["value"])) <=
                                       1e-12 * max(1.0, abs(default["value"])))})
        best_tight = min(s["tight"]["value"] for s in starts)
        tight_excess = Q(best_tight) - certified
        group = r["name"] if r["family"] == "minlplib" else "path family"
        out.append({"group": group, "part": r["part"], "line": r["line"], "cut": r["cut"],
                    "certified": float(certified), "u2": r["u2_float"],
                    "box_width_max": max(hi - lo for lo, hi in box),
                    "best_tight": best_tight, "tight_excess": float(tight_excess),
                    "class": "tight_reaches" if tight_excess <= scale else "tight_local",
                    "starts": starts})
    summary = {}
    for group in sorted({o["group"] for o in out}):
        mine = [o for o in out if o["group"] == group]
        st = [s for o in mine for s in o["starts"]]
        summary[group] = {
            "cuts": len(mine),
            "classes": dict(collections.Counter(o["class"] for o in mine)),
            "starts": len(st),
            "default_reproduces": sum(s["default_reproduces"] for s in st),
            "starts_stationary": sum(s["pg"] <= STATIONARY for s in st),
            "starts_default_nit_le_1": sum(s["default"]["nit"] <= 1 for s in st),
            "starts_default_not_moved": sum(s["default"]["moved"] == 0.0 for s in st),
            "max_pg_nonstationary": max((s["pg"] for s in st if s["pg"] > STATIONARY), default=None),
            "max_gs": max(s["gs"] for s in st),
            "max_gs_default_nit_le_1": max((s["gs"] for s in st if s["default"]["nit"] <= 1),
                                           default=None),
            "max_abs_certified": max(abs(o["certified"]) for o in mine),
            "box_width_max": max(o["box_width_max"] for o in mine),
            "max_tight_excess": max(o["tight_excess"] for o in mine),
            "max_tight_nit": max(s["tight"]["nit"] for s in st),
        }
    args.out_json.write_text(json.dumps({"summary": summary, "cuts": out}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
