#!/usr/bin/env python3
"""Independent spot check of evidence/ablation-global-solve.json (Part 5U3).

For N random cuts (``random.Random(seed).sample`` over the stored ``cuts``
list) this script, in a fresh process and without importing
``ablation_global_solve`` or ``ablation_uncertified``:

1. reads the cut from its record file (``meta.parts[*].records``, line, cut)
   and recomputes the certified value Fraction(support_witness.lower_bound);
2. expands sum_k fl(c_k) g_k(u) exactly (``sympy.expand`` and
   ``as_coefficients_dict``, rational coefficients), checks the result against
   the certificate's stored problem, rounds each coefficient to binary64,
   builds the Gurobi model (box bounds, domain rows a.u <= rhs; NonConvex=2,
   Threads=1, Seed=0, TimeLimit=10, OutputFlag=0, other parameters default)
   and solves it;
3. compares ObjBound, ObjVal, status and node count with the stored values
   (bit for bit) and recomputes the stored exact excesses and the invalid and
   material flags of U3, U3p and U3s.

Usage::

    $PY ablation_global_solve_spotcheck.py --count 50 --seed 3
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import os  # noqa: E402

for _name in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_name] = "1"

import argparse  # noqa: E402
from fractions import Fraction as Q  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
from pathlib import Path  # noqa: E402
import random  # noqa: E402

HERE = Path(__file__).resolve().parent
PARAMS = {"NonConvex": 2, "Threads": 1, "Seed": 0, "TimeLimit": 10.0, "OutputFlag": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--data", type=Path, default=HERE.parent / "evidence" / "ablation-global-solve.json")
    parser.add_argument("--count", type=int, default=50)
    parser.add_argument("--seed", type=int, default=3)
    parser.add_argument("--out", type=Path,
                        default=HERE.parent / "evidence" / "ablation-global-solve-spotcheck.json")
    args = parser.parse_args()

    channel = os.fdopen(os.dup(1), "w")      # Gurobi's C library prints license lines to fd 1
    os.dup2(2, 1)
    import gurobipy as gp
    from gurobipy import GRB
    import sympy as sp

    data = json.loads(args.data.read_text())
    stored = data["cuts"]
    chosen = sorted(random.Random(args.seed).sample(range(len(stored)), args.count))
    records = {p["label"]: Path(p["records"]) for p in data["meta"]["parts"]}
    wanted = {}
    for i in chosen:
        wanted.setdefault(stored[i]["part"], {}).setdefault(stored[i]["line"], []).append(i)
    cuts = {}
    for label, lines in wanted.items():
        with open(records[label], "rb") as handle:
            for line_no, raw in enumerate(handle):
                if line_no in lines:
                    record = json.loads(raw)
                    for i in lines[line_no]:
                        cuts[i] = (record["name"], record["cuts"][stored[i]["cut"]])

    env = gp.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()
    checks = []
    for i in chosen:
        s = stored[i]
        name, cut = cuts[i]
        certified = Q(cut["support_witness"]["lower_bound"])
        syms = [sp.Symbol(t, real=True) for t in cut["symbols"]]
        local = {str(t): t for t in syms}
        d = len(syms)
        expression = sp.expand(sp.Add(*(
            sp.Rational(*Q(float(c)).as_integer_ratio()) * sp.sympify(f, locals=local)
            for c, f in zip(cut["coefficients"], cut["features"]))))
        constant, linear, quadratic = Q(0), [Q(0)] * d, {}
        for monomial, coefficient in expression.as_coefficients_dict().items():
            value = Q(int(coefficient.p), int(coefficient.q))
            powers = monomial.as_powers_dict() if monomial != 1 else {}
            index = [syms.index(t) for t, e in powers.items() for _ in range(int(e))]
            if not index:
                constant += value
            elif len(index) == 1:
                linear[index[0]] += value
            elif len(index) == 2:
                key = tuple(sorted(index))
                quadratic[key] = quadratic.get(key, Q(0)) + value
            else:
                raise ValueError(f"degree > 2 in cut {i}")
        pairs = [(a, b) for a in range(d) for b in range(a, d)]
        exact = [constant, *linear, *(quadratic.get(p, Q(0)) for p in pairs)]
        problem = cut["support_witness"]["proof"]["quadratic"]["problem"]
        matches_problem = [Q(c) for c in problem["coefficients"]] == exact
        rounded = [float(c) for c in exact]

        m = gp.Model(env=env)
        for key, value in PARAMS.items():
            m.setParam(key, value)
        x = [m.addVar(lb=float(Q(lo)), ub=float(Q(hi)), name=f"u{k}")
             for k, (lo, hi) in enumerate(cut["box"])]
        objective = gp.QuadExpr()
        objective.addConstant(rounded[0])
        for k in range(d):
            if rounded[1 + k] != 0:
                objective.addTerms(rounded[1 + k], x[k])
        for (a, b), c in zip(pairs, rounded[1 + d:]):
            if c != 0:
                objective.addTerms(c, x[a], x[b])
        m.setObjective(objective, GRB.MINIMIZE)
        for k, row in enumerate(cut["domain_rows"]):
            m.addLConstr(gp.LinExpr([float(Q(v)) for v in row["coefficients"]], x), GRB.LESS_EQUAL,
                         float(Q(row["rhs"])), name=f"row{k}")
        m.optimize()
        bound = float(m.ObjBound)
        value = float(m.ObjVal) if m.SolCount > 0 else None
        fresh = {"status": int(m.Status), "nodes": float(m.NodeCount),
                 "obj_bound": bound.hex(), "obj_val": None if value is None else value.hex()}
        m.dispose()

        gs = s["gurobi"]
        constants = {"u3": bound, "u3p": value,
                     "u3s": bound - 1e-6 * max(1.0, abs(bound)) if math.isfinite(bound) else None}
        scale = Q(1, 10**6) * max(Q(1), abs(certified))
        flags_match = True
        for v, u in constants.items():
            if u is None or not math.isfinite(u):
                flags_match &= bool(s.get(f"{v}_none"))
                continue
            excess = Q(u) - certified
            flags_match &= (s.get(v) == u.hex() and Q(s[f"{v}_excess"]) == excess
                            and s[f"{v}_invalid"] == (excess > 0)
                            and s[f"{v}_material"] == (excess > scale))
        checks.append({
            "index": i, "part": s["part"], "name": name, "line": s["line"], "cut": s["cut"],
            "name_matches": name == s["name"],
            "certified_matches": str(certified) == s["certified"],
            "expansion_matches_certificate_problem": matches_problem,
            "fresh": fresh,
            "stored": {k: gs[k] for k in ("status", "nodes", "obj_bound", "obj_val")},
            "obj_bound_identical": fresh["obj_bound"] == gs["obj_bound"],
            "obj_val_identical": fresh["obj_val"] == gs["obj_val"],
            "status_identical": fresh["status"] == gs["status"],
            "nodes_identical": fresh["nodes"] == gs["nodes"],
            "excess_and_flags_match": bool(flags_match),
        })
    env.dispose()
    keys = ("name_matches", "certified_matches", "expansion_matches_certificate_problem",
            "obj_bound_identical", "obj_val_identical", "status_identical", "nodes_identical",
            "excess_and_flags_match")
    summary = {"data": str(args.data), "count": args.count, "seed": args.seed,
               "call": f"random.Random({args.seed}).sample(range({len(stored)}), {args.count})",
               "parts": dict(sorted({c["part"]: sum(x["part"] == c["part"] for x in checks)
                                     for c in checks}.items())),
               **{k: sum(c[k] for c in checks) for k in keys}}
    args.out.write_text(json.dumps({"summary": summary, "checks": checks}, indent=1))
    json.dump(summary, channel, indent=1)
    channel.write("\n")
    channel.flush()


if __name__ == "__main__":
    main()
