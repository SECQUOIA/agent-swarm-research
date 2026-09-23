"""Task 1(a),(b): the guarded LMTD f(d1,d2) = (d1-d2)/log(d1/(d2+eps)) in heatexch_gen1 is unbounded above.

(a) tabulate f(d2+eps+delta, d2) with mpmath;
(b) fix binaries to BARON's 120 s incumbent, force dt1 - dt2 = eps + delta on each active
    process exchanger, solve the NLP (Ipopt; CONOPT check), verify all constraints in float and
    mpmath (50 digits), then polish LMTD/area variables with mpmath and re-verify.
"""
import json
import math
import mpmath
from common import *
from mpcheck import check_point

EPS = 1e-6
mpmath.mp.dps = 50


def f_mp(d1, d2):
    d1, d2 = mpmath.mpf(d1), mpmath.mpf(d2)
    return (d1 - d2) / mpmath.log(d1 / (d2 + mpmath.mpf(EPS)))


# ---- (a) numeric illustration -----------------------------------------------------------
table_a = []
for d2 in (10.0, 50.0):
    for delta in (1e-3, 1e-5, 1e-7, 1e-8, 1e-9, 1e-12, -1e-8, -2e-6, -1e-3):
        d1 = float(mpmath.mpf(d2) + EPS + delta)
        val = f_mp(d1, d2)
        approx = (EPS + delta) * (d2 + EPS) / delta if delta > 0 else None
        table_a.append({"d2": d2, "delta": delta, "d1": d1, "f": float(val),
                        "f_float": (d1 - d2) / math.log(d1 / (EPS + d2)),
                        "asymptotic": approx})
for r in table_a:
    r["f_float"] = (r["d1"] - r["d2"]) / math.log(r["d1"] / (EPS + r["d2"]))
    print(r)

# ---- (b) explicit near-singular feasible points -------------------------------------------
# match k -> (dt_hot_end, dt_cold_end, lmtd, area, q, binary) in heatexch_gen1
MATCH = {
    "b1": ("x37", "x38", "x85", "x97", "x25"), "b2": ("x38", "x39", "x86", "x98", "x26"),
    "b3": ("x40", "x41", "x87", "x100", "x27"), "b4": ("x41", "x42", "x88", "x101", "x28"),
    "b5": ("x43", "x44", "x89", "x103", "x29"), "b6": ("x44", "x45", "x90", "x104", "x30"),
    "b7": ("x46", "x47", "x91", "x106", "x31"), "b8": ("x47", "x48", "x92", "x107", "x32"),
}
inc = json.load(open(RES / "baron120_gen1_point.json"))
xinc = inc["x"]
active = [k for k in MATCH if round(xinc[k]) == 1]
print("active process exchangers:", active)

results = {"table_a": table_a, "incumbent_obj": inc["obj"], "runs": []}


def build(delta, mode):
    """mode='fix': fix dt2=10, dt1=10+eps+delta.  mode='eq': add dt1-dt2 = eps+delta as a constraint."""
    m = load_minlplib("heatexch_gen1")
    for v in m.component_data_objects(pe.Var):
        v.set_value(xinc[v.name])
        if v.is_binary():
            v.fix(round(xinc[v.name]))
    m.extra = pe.ConstraintList()
    for k in active:
        d1, d2 = (getattr(m, n) for n in MATCH[k][:2])
        if mode == "fix":
            d2.fix(10.0)
            d1.fix(10.0 + EPS + delta)
        else:
            m.extra.add(d1 - d2 == EPS + delta)
    return m


def polish(m, vals):
    """Recompute LMTD and area variables exactly (mpmath) from the dt and q values, round to double."""
    vals = dict(vals)
    for k, (n1, n2, nl, na, nq) in MATCH.items():
        lm = f_mp(vals[n1], vals[n2])
        vals[nl] = float(lm)
        vals[na] = float(2 * mpmath.mpf(vals[nq]) / (mpmath.mpf(0.01) + mpmath.mpf(vals[nl])))
    return vals


def run(delta, mode, solver):
    m = build(delta, mode)
    if solver == "ipopt":
        opt = pe.SolverFactory("ipopt")
        opt.options["tol"] = 1e-12
        opt.options["constr_viol_tol"] = 1e-12
        opt.options["acceptable_tol"] = 1e-10
        opt.options["max_iter"] = 5000
        opt.options["bound_relax_factor"] = 0
        opt.options["honor_original_bounds"] = "yes"
        res = opt.solve(m, tee=False)
        term = str(res.solver.termination_condition)
    else:
        res, _ = solve_gams(m, "conopt", 60, threads=1, extra=["option optca=0;"])
        term = str(res.solver.termination_condition)
    vals = {v.name: pe.value(v) for v in m.component_data_objects(pe.Var)}
    mo = load_minlplib("heatexch_gen1")  # original model (no fixing) for verification
    raw = check_point(mo, vals)
    pol = check_point(mo, polish(m, vals))
    rec = {"delta": delta, "mode": mode, "solver": solver, "term": term,
           "obj_raw_float": raw["obj_float"], "obj_raw_mp": raw["obj_mp"],
           "maxviol_raw_float": raw["max_viol_float"], "maxviol_raw_mp": raw["max_viol_mp"],
           "argmax_raw_mp": raw["argmax_mp"],
           "obj_pol_float": pol["obj_float"], "obj_pol_mp": pol["obj_mp"],
           "maxviol_pol_float": pol["max_viol_float"], "maxviol_pol_mp": pol["max_viol_mp"],
           "argmax_pol_mp": pol["argmax_mp"], "bound_viol": max(raw["max_bound_viol"], pol["max_bound_viol"]),
           "lmtd": {k: vals[MATCH[k][2]] for k in active}, "area": {k: vals[MATCH[k][3]] for k in active},
           "q": {k: vals[MATCH[k][4]] for k in active},
           "util": {n: vals[n] for n in ("x33", "x34", "x35", "x36")},
           "dt": {k: (vals[MATCH[k][0]], vals[MATCH[k][1]]) for k in active}}
    print(json.dumps(rec, indent=None, default=float), flush=True)
    results["runs"].append(rec)
    return rec


for delta in (1e-7, 1e-8, 1e-9):
    run(delta, "fix", "ipopt")
for delta in (1e-7, 1e-8, 1e-9):
    run(delta, "eq", "ipopt")
run(1e-8, "fix", "conopt")
run(1e-8, "eq", "conopt")
# also: the incumbent itself (sanity check of the verifier)
mo = load_minlplib("heatexch_gen1")
chk = check_point(mo, xinc)
results["incumbent_check"] = {k: chk[k] for k in ("max_viol_float", "max_viol_mp", "argmax_mp", "obj_float", "obj_mp")}
print("incumbent check", results["incumbent_check"])
dump("singularity_audit.json", results)
