"""Evaluate all constraints and the objective of a Pyomo model at a point in float and in mpmath (50 digits)."""
import mpmath
import sympy
import pyomo.environ as pe
from pyomo.core.expr.sympy_tools import sympyify_expression


def _lambdify(expr):
    bimap, sexpr = sympyify_expression(expr)
    syms = sorted(sexpr.free_symbols, key=lambda s: s.name)
    pvars = [bimap.sympy2pyomo[s] for s in syms]
    f = sympy.lambdify(syms, sexpr, modules="mpmath")
    return pvars, f


def _mp(v):
    # exact binary value of the double (no decimal re-rounding)
    return mpmath.mpf(float(v))


def check_point(m, vals, dps=50):
    """vals: {var name: float}. Returns dict with per-constraint float/mp violations and objectives."""
    mpmath.mp.dps = dps
    for v in m.component_data_objects(pe.Var):
        v.set_value(vals[v.name], skip_validation=True)
    out = {"con": {}}
    for c in m.component_data_objects(pe.Constraint, active=True):
        body_f = pe.value(c.body)
        pvars, f = _lambdify(c.body)
        body_mp = f(*[_mp(vals[v.name]) for v in pvars])
        lb = c.lower() if c.has_lb() else None
        ub = c.upper() if c.has_ub() else None
        def viol(b):
            r = 0
            if lb is not None:
                r = max(r, _mp(lb) - b)
            if ub is not None:
                r = max(r, b - _mp(ub))
            return r
        out["con"][c.name] = (float(viol(mpmath.mpf(body_f))), float(viol(body_mp)))
    bviol = 0.0
    for v in m.component_data_objects(pe.Var):
        x = vals[v.name]
        if v.lb is not None:
            bviol = max(bviol, v.lb - x)
        if v.ub is not None:
            bviol = max(bviol, x - v.ub)
        if v.is_binary():
            bviol = max(bviol, abs(x - round(x)))
    out["max_viol_float"] = max(r[0] for r in out["con"].values())
    out["max_viol_mp"] = max(r[1] for r in out["con"].values())
    out["argmax_mp"] = max(out["con"], key=lambda k: out["con"][k][1])
    out["max_bound_viol"] = bviol
    out["obj_float"] = pe.value(m.obj)
    pvars, f = _lambdify(m.obj.expr)
    out["obj_mp"] = float(f(*[_mp(vals[v.name]) for v in pvars]))
    return out
