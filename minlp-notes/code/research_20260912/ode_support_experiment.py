"""Small reproducible experiments for rational extended-RPD support cuts."""

import argparse
from dataclasses import asdict, replace
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
from time import perf_counter

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import expm

from extended_rpd import dimerization, shift_methanation, rational
from rational_affine_flow import Slab, certify_affine_flow
from polynomial_tubes import certify_tubes


def round_physical_supports(rows, model, denominator):
    """Round slopes and compensate exactly on p in P, z=(x,-x), x in X.

    The result need not minorize the entire extended-RPD field off the physical
    state manifold. It minorizes each signed physical derivative, which suffices
    for comparison with the cooperative linear flow.
    """
    if isinstance(denominator,bool) or not isinstance(denominator,int) or denominator<1:
        raise ValueError("Support denominator must be a positive integer")
    n, m = len(model.state_box), len(model.parameter_box)
    result=[]
    def nearest(value):
        scaled=value*denominator+Q(1,2)
        return Q(scaled.numerator//scaled.denominator,denominator)
    for row in rows:
        slopes=tuple(nearest(value) for value in row[:-1])
        error=Q(0)
        for j,(lo,hi) in enumerate(model.parameter_box):
            delta=slopes[j]-row[j]
            error+=max(delta*lo,delta*hi)
        for j,(lo,hi) in enumerate(model.state_box):
            delta=(slopes[m+j]-row[m+j])-(slopes[m+n+j]-row[m+n+j])
            error+=max(delta*lo,delta*hi)
        constant=(row[-1]-error)*denominator
        result.append(slopes+(Q(constant.numerator//constant.denominator,denominator),))
    return result


def compile_slabs(model, nominal, horizon, steps, *, tubes=None, support_denominator=None, **options):
    """An unvalidated floating reference chooses exact globally valid pieces.

    Supplied tube data must be valid for this RHS; metadata and grid checks
    reject accidental mismatches but do not authenticate arbitrary callables.
    """
    horizon = rational(horizon)
    if isinstance(steps,bool) or not isinstance(steps,int) or steps<1 or horizon<=0:
        raise ValueError("Positive exact horizon and integer steps required")
    n, m = 2*len(model.state_box), len(model.parameter_box)
    if tubes is not None:
        if (tubes.duration != horizon or tubes.steps != steps or len(tubes.slabs) != steps
                or tubes.parameter_box != model.parameter_box
                or tubes.physical_box != model.state_box
                or tubes.initial_coefficients != model.initial
                or tubes.invariant_A != model.invariant_A
                or tubes.invariant_b != model.invariant_b
                or tubes.invariant_D != model.invariant_D
                or any(slab.start != j*horizon/steps or slab.duration != horizon/steps
                       for j,slab in enumerate(tubes.slabs))):
            raise ValueError("Tube certificate grid or model metadata mismatch")
    coefficients = np.array(model.initial_signed_coefficients(), dtype=float)
    bottom = np.eye(m+1)
    point = np.r_[nominal, 1.0]
    h = horizon/steps
    slabs = []
    for index in range(steps):
        reference = coefficients @ point
        slab_model = model if tubes is None else replace(model, state_box=tubes.slabs[index].refined_box)
        rows = slab_model.supports(nominal, reference, **options)
        if support_denominator is not None:
            rows = round_physical_supports(rows, slab_model, support_denominator)
        a = [row[:m] for row in rows]
        b = [row[m:-1] for row in rows]
        d = [row[-1] for row in rows]
        slab = Slab(h, b, a, d)
        slabs.append(slab)
        matrix = np.zeros((n+m+1, n+m+1))
        matrix[:n, :n] = b
        matrix[:n, n:n+m] = a
        matrix[:n, -1] = d
        coefficients = (expm(float(h)*matrix) @ np.vstack([coefficients,bottom]))[:n]
    return slabs


def run_case(model, name, steps, sweeps, horizon, *, validated_tubes=False, parameter_factor=Q(1), support_denominator=None):
    model = replace(model, parameter_box=tuple(
        ((lo+hi)/2-parameter_factor*(hi-lo)/2,
         (lo+hi)/2+parameter_factor*(hi-lo)/2) for lo,hi in model.parameter_box))
    nominal = [sum(pair)/2 for pair in model.parameter_box]
    options = {"row_sweeps": sweeps}
    started = perf_counter()
    tubes = certify_tubes(model, horizon, steps) if validated_tubes else None
    tube_seconds = perf_counter()-started
    started = perf_counter()
    slabs = compile_slabs(model, nominal, horizon, steps, tubes=tubes,
                          support_denominator=support_denominator, **options)
    compilation_seconds = perf_counter()-started
    started = perf_counter()
    cert = certify_affine_flow(slabs, model.initial_signed_coefficients(), model.parameter_box)
    certificate_seconds = perf_counter()-started
    x0 = model.initial_state(nominal)
    nominal_cut = np.array(cert.evaluate(nominal), dtype=float)
    nominal_reference = None
    nominal_deficit = None
    if tubes is None and support_denominator is None:
        reference = solve_ivp(lambda t,v:model.relaxation_rhs(nominal,v,**options),
                              [0,float(horizon)], np.r_[x0,-x0], rtol=1e-8,atol=1e-10)
        if not reference.success:
            raise RuntimeError(reference.message)
        nominal_reference = reference.y[:,-1].tolist()
        nominal_deficit = float(np.max(reference.y[:,-1]-nominal_cut))
    # Grid comparisons diagnose implementation, not certify nonlinear solutions.
    parameter_points = np.array(np.meshgrid(*[
        np.linspace(float(lo),float(hi),1 if lo==hi else 9) for lo,hi in model.parameter_box])).reshape(len(nominal),-1).T
    max_diagnostic_violation = -np.inf
    min_diagnostic_slack = np.inf
    for p in parameter_points:
        physical = solve_ivp(lambda t,x:model.physical_rhs(p,x),[0,float(horizon)],
                             model.initial_state(p),rtol=1e-10,atol=1e-12)
        if not physical.success:
            raise RuntimeError(physical.message)
        true_signed = np.r_[physical.y[:,-1],-physical.y[:,-1]]
        cut = np.asarray(cert.lower,dtype=float) @ np.r_[p,1]
        max_diagnostic_violation = max(max_diagnostic_violation,float(np.max(cut-true_signed)))
        min_diagnostic_slack = min(min_diagnostic_slack,float(np.min(true_signed-cut)))
    return {"model":name,"steps":steps,"row_sweeps":sweeps,"horizon":str(horizon),
            "validated_tubes":validated_tubes,"parameter_factor":str(parameter_factor),
            "support_denominator":support_denominator,
            "parameter_box":model.parameter_box,"state_box":model.state_box,
            "initial_coefficients":model.initial_signed_coefficients(),
            "nominal_parameter":nominal,"certified_lower_coefficients":cert.lower,
            "coefficient_error":str(cert.coefficient_error),
            "evaluation_error":str(cert.evaluation_error),
            "nominal_cut":nominal_cut.tolist(),
            "numerical_relaxation":nominal_reference,
            "max_nominal_support_deficit":nominal_deficit,
            "nominal_cut_state_widths":(-nominal_cut[:len(x0)]-nominal_cut[len(x0):]).tolist(),
            "final_interval_state_widths":None if tubes is None else [float(hi-lo) for lo,hi in tubes.slabs[-1].endpoint],
            "diagnostic_physical_grid_points":len(parameter_points),
            "diagnostic_max_violation":max_diagnostic_violation,
            "diagnostic_min_slack":min_diagnostic_slack,
            "compilation_seconds":compilation_seconds,"certificate_seconds":certificate_seconds,
            "tube_seconds":tube_seconds,"tubes":None if tubes is None else asdict(tubes),
            "slabs":[asdict(slab) for slab in slabs],
            "note":"Exact certificates conditional on reviewed model/support algebra; nonlinear reference and grid are numerical diagnostics."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    parser.add_argument("--models",nargs="+",choices=["dimerization","shift_methanation"],default=["dimerization"])
    parser.add_argument("--steps",nargs="+",type=int,default=[10,30])
    parser.add_argument("--sweeps",nargs="+",type=int,default=[0,1])
    parser.add_argument("--horizon",type=Q,default=Q(1,2))
    parser.add_argument("--validated-tubes",action="store_true")
    parser.add_argument("--parameter-factor",type=Q,default=Q(1))
    parser.add_argument("--support-denominator",type=int)
    args = parser.parse_args()
    if any(k<1 for k in args.steps) or args.horizon<=0:
        parser.error("Positive steps and horizon required")
    if not 0<=args.parameter_factor<=1:
        parser.error("Parameter factor must lie in [0,1]")
    report={"cases":[],"source_sha256":{
        name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
        for name in ("extended_rpd.py","rational_affine_flow.py","polynomial_tubes.py","ode_support_experiment.py")}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    models={"dimerization":dimerization,"shift_methanation":shift_methanation}
    for name in args.models:
        for steps in args.steps:
            for sweeps in args.sweeps:
                result=run_case(models[name](),name,steps,sweeps,args.horizon,
                                validated_tubes=args.validated_tubes,parameter_factor=args.parameter_factor,
                                support_denominator=args.support_denominator)
                report["cases"].append(result)
                args.output.write_text(json.dumps(report,indent=2,default=str)+"\n")
                print(json.dumps({key:result[key] for key in (
                    "model","steps","row_sweeps","max_nominal_support_deficit",
                    "evaluation_error","diagnostic_max_violation",
                    "nominal_cut_state_widths","final_interval_state_widths",
                    "compilation_seconds","certificate_seconds","tube_seconds")}),flush=True)


if __name__=="__main__":
    main()
