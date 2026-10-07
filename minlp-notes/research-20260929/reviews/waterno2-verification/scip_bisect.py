"""Additional SCIP settings to localize the wrong answers (period t, cheaper point x*).
usage: python3 scip_bisect.py t"""
import sys
import scip_check as sc
from scip_diag import load_point

EXTRA = {
    "pscost_branching(no strong br.)": dict(params={"branching/pscost/priority": 10**8}),
    "no_node_sepa": dict(params={"separating/maxrounds": 0}),
    "no_root_sepa": dict(params={"separating/maxroundsroot": 0}),
    "no_node_prop": dict(params={"propagating/maxrounds": 0}),
    "no_root_prop": dict(params={"propagating/maxroundsroot": 0}),
    "nonlinear_no_node_prop": dict(params={"constraints/nonlinear/propfreq": 0}),
    "nonlinear_prop_never(propfreq=-1)": dict(params={"constraints/nonlinear/propfreq": -1}),
    "nonlinear_maxprerounds0": dict(params={"constraints/nonlinear/maxprerounds": 0}),
    "nonlinear_propauxvars_off": dict(params={"constraints/nonlinear/propauxvars": False}),
    "nonlinear_varboundrelax_none": dict(params={"constraints/nonlinear/varboundrelax": "n"}),
    "nonlinear_varboundrelax_abs": dict(params={"constraints/nonlinear/varboundrelax": "a"}),
    "nonlinear_reformbinprods_off": dict(params={"constraints/nonlinear/reformbinprods": False}),
    "nonlinear_tightenlpfeastol_off": dict(params={"constraints/nonlinear/tightenlpfeastol": False}),
    "no_obbt_genvbounds": dict(params={"propagating/obbt/creategenvbounds": False}),
    "obbt_no_sepa": dict(params={"propagating/obbt/separatesol": False}),
    "no_nlp_sepa(convexity)": dict(params={"constraints/nonlinear/linearizeheursol": "o"}),
    "no_restarts": dict(params={"presolving/maxrestarts": 0}),
    "no_symmetry": dict(params={"misc/usesymmetry": 0}),
    "no_bilinear_nlhdlr": dict(params={"nlhdlr/bilinear/enabled": False}),
    "no_quadratic_nlhdlr": dict(params={"nlhdlr/quadratic/enabled": False}),
    "no_convex_nlhdlr": dict(params={"nlhdlr/convex/enabled": False, "nlhdlr/concave/enabled": False}),
    "no_perspective_nlhdlr": dict(params={"nlhdlr/perspective/enabled": False}),
    "no_quotient_soc": dict(params={"nlhdlr/quotient/enabled": False, "nlhdlr/soc/enabled": False}),
    "no_rlt_sepa": dict(params={"separating/rlt/freq": -1}),
    "no_intersection_cuts": dict(params={"nlhdlr/quadratic/useintersectioncuts": False}),
    "all_propagator_plugins_off": dict(params={f"propagating/{p}/freq": -1 for p in (
        "dualfix", "genvbounds", "nlobbt", "obbt", "probing", "pseudoobj", "redcost", "rootredcost", "symmetry", "vbounds")}),
    "all_propagator_plugins_off+nonlinear_propfreq-1": dict(params=dict({f"propagating/{p}/freq": -1 for p in (
        "dualfix", "genvbounds", "nlobbt", "obbt", "probing", "pseudoobj", "redcost", "rootredcost", "symmetry", "vbounds")},
        **{"constraints/nonlinear/propfreq": -1})),
    "linear_propfreq-1": dict(params={"constraints/linear/propfreq": -1}),
    "varbound_and_setppc_propfreq-1": dict(params={"constraints/varbound/propfreq": -1, "constraints/setppc/propfreq": -1}),
}
t = int(sys.argv[1])
x = load_point(t)
M, X, obj = sc.build(t)
vstar = float(sum(a * sc.F(x[v]) for v, a in obj.items()))
M.freeProb()
names = sys.argv[2].split(",") if len(sys.argv) > 2 else list(EXTRA)
for name in names:
    sc.SETTINGS[name] = EXTRA[name]
    try:
        sc.run_setting(t, name, EXTRA[name], vstar)
    except Exception as e:
        print(f"period {t} {name}: ERROR {e}", flush=True)
