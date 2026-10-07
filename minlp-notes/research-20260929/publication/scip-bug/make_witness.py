"""Turn a nearly feasible floating-point solution of a CIP model into an exactly
feasible rational point (the witness).  SCIP is only used to supply the
floating-point solution; the result is checked by exact_check.py.

Method (as reviews/waterno2-verification/vrepair.py, re-implemented on the
CIP file): fix the binaries at their rounded values and fixed variables at
their bounds; repeatedly solve equality rows that have exactly one unknown
appearing linearly, in exact rational arithmetic; when no such row exists,
seed one unknown (arguments of nonlinear terms first) with its value rounded
to DIGITS decimals and clipped to the exact interval implied by the rows in
which it is the only unknown.  Pairs of inequality rows that bound the same
linear form from both sides with equal values (big-M rows of a running pump)
are used as equalities.

usage: python3 make_witness.py MODEL.cip OUT.json [SETTING] [DIGITS] [TIES]
SETTING is a run_scip.py setting used to get the float point (default
'default'); TIES is a comma list a:b:r meaning seed a := r * value(b).
"""
import json
import sys
from fractions import Fraction as F

import pyscipopt as ps

import exact_check as ec
import run_scip


def scip_point(path, setting):
    m = ps.Model()
    m.hideOutput()
    m.readProblem(path)
    for k, v in run_scip.parse(setting).items():
        m.setParam(k, v)
    m.setParam("limits/time", 600)
    m.optimize()
    sol = m.getBestSol()
    x = {v.name: m.getSolVal(sol, v) for v in m.getVars()}
    print(f"SCIP ({setting}): status {m.getStatus()} claimed {m.getDualbound()!r} primal {m.getPrimalbound()!r}")
    return x, m.getPrimalbound()


def main():
    path, out = sys.argv[1], sys.argv[2]
    setting = sys.argv[3] if len(sys.argv) > 3 else "default"
    digits = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    ties = {}
    if len(sys.argv) > 5 and sys.argv[5]:
        for tie in sys.argv[5].split(","):
            a, b, r = tie.split(":")
            ties[a] = (b, F(r))
    x0, pval = scip_point(path, setting)
    vars_, rows = ec.parse_cip(path)
    # parser cross-check against SCIP's reading of the file: objective of SCIP's point
    obj0 = sum(float(v["obj"]) * x0[v["name"]] for v in vars_)
    print(f"objective of SCIP's point by our parser {obj0!r} (SCIP {pval!r})")
    assert abs(obj0 - pval) <= 1e-6 * max(1.0, abs(pval))
    V = {v["name"]: v for v in vars_}
    known = {}
    for v in vars_:
        if v["type"] == "binary":
            known[v["name"]] = F(round(x0[v["name"]]))
        elif v["lb"] is not None and v["lb"] == v["ub"]:
            known[v["name"]] = v["lb"]
    eqrows = [(r["name"], r["terms"], r["rhs"]) for r in rows if r["op"] == "=="]
    # implied equalities from two-sided inequality pairs after fixing binaries
    groups = {}
    for r in rows:
        if r["op"] == "==":
            continue
        const, rest = F(0), []
        for a, vs in r["terms"]:
            if all(n in known for n in vs):
                val = a
                for n in vs:
                    val *= known[n]
                const += val
            else:
                rest.append((tuple(sorted(vs)), a))
        if not rest:
            continue
        rest.sort()
        lead = rest[0][1]
        key = tuple((vs, a / lead) for vs, a in rest)
        bound = (r["rhs"] - const) / lead
        is_lo = (r["op"] == ">=") == (lead > 0)
        g = groups.setdefault(key, [None, None, []])
        if is_lo:
            g[0] = bound if g[0] is None else max(g[0], bound)
        else:
            g[1] = bound if g[1] is None else min(g[1], bound)
        g[2].append(r["name"])
    for key, (lo, hi, nm) in groups.items():
        if lo is not None and lo == hi:
            eqrows.append(("+".join(nm), [(a, list(vs)) for vs, a in key], lo))
            print("implied equality from rows", nm)
    used = set()

    def solve_rows():
        progress = True
        while progress:
            progress = False
            for name, terms, rhs in eqrows:
                if name in used:
                    continue
                unk = {n for a, vs in terms for n in vs if n not in known}
                if len(unk) != 1:
                    continue
                u = unk.pop()
                const, coef, ok = F(0), F(0), True
                for a, vs in terms:
                    k = vs.count(u)
                    val = a
                    for n in vs:
                        if n != u:
                            val *= known[n]
                    if k == 0:
                        const += val
                    elif k == 1:
                        coef += val
                    else:
                        ok = False
                if not ok or coef == 0:
                    continue
                known[u] = (rhs - const) / coef
                used.add(name)
                progress = True

    nl = {n for r in rows for a, vs in r["terms"] if len(vs) > 1 for n in vs}

    def interval(u):
        lo, hi = V[u]["lb"], V[u]["ub"]
        for r in rows:
            if not any(u in vs for a, vs in r["terms"]):
                continue
            if any(n not in known and n != u for a, vs in r["terms"] for n in vs):
                continue
            const, coef, lin = F(0), F(0), True
            for a, vs in r["terms"]:
                k = vs.count(u)
                val = a
                for n in vs:
                    if n != u:
                        val *= known[n]
                if k == 0:
                    const += val
                elif k == 1:
                    coef += val
                else:
                    lin = False
            if not lin or coef == 0:
                continue
            Lo = (r["rhs"] - const) / coef if r["op"] in ("==", ">=") else None
            Hi = (r["rhs"] - const) / coef if r["op"] in ("==", "<=") else None
            if coef < 0:
                Lo, Hi = Hi, Lo
            if Lo is not None:
                lo = Lo if lo is None else max(lo, Lo)
            if Hi is not None:
                hi = Hi if hi is None else min(hi, Hi)
        return lo, hi

    seeded = []
    solve_rows()
    order = [v["name"] for v in vars_]
    while len(known) < len(vars_):
        u = min((n for n in order if n not in known), key=lambda n: (0 if n in nl else 1, order.index(n)))
        val = F(format(x0[u], f".{digits}f"))
        if u in ties:
            b, r = ties[u]
            val = r * known[b]
        lo, hi = interval(u)
        if lo is not None:
            val = max(val, lo)
        if hi is not None:
            val = min(val, hi)
        known[u] = val
        seeded.append(u)
        solve_rows()
    print(f"seeded {len(seeded)} variables: {seeded}")
    json.dump({n: str(known[n]) for n in order}, open(out, "w"), indent=0)
    ec.check(path, {n: str(known[n]) for n in order})


if __name__ == "__main__":
    main()
