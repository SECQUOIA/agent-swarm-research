"""Exactly feasible points for ann_cumene_tanh (OSIL model) and points of the KAN
relaxation R for kan_r5_h1_n3/n5/n8, by forward construction (fwd.py).

ann_cumene_tanh: the free inputs x723..x727 are fixed at rationals; every other
variable is defined by one equality row (all 789 equality rows are used); the
single inequality row and all variable bounds are proved with interval
arithmetic.  The point is then exactly feasible for the OSIL model.

KAN: the relaxation R of wave 3 drops the partition-of-unity rows (sum of basis
values = 1), the bounds B >= 0 of basis and spline variables, and every
intermediate-variable bound except the input class and the hidden class.  The
inputs are fixed at rationals (the exact binary64 inputs of the wave-3 point);
interval binaries are chosen from the edge arguments; every other variable is
defined by one equality row.  Partition rows are never used.  All other rows
(one-hot rows exactly; big-M rows exactly or by intervals) and ALL variable
bounds are checked; a point satisfying them is in R (R drops constraints only).

usage: python3 nn_exact.py ann_cumene_tanh | kan_r5_h1_n3 | kan_r5_h1_n5 | kan_r5_h1_n8
"""
import os as _repro_os
_REPRO_ROOT = _repro_os.path.normpath(_repro_os.path.join(
    _repro_os.path.dirname(_repro_os.path.abspath(__file__)), '../../../../..'))
import json
import os
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp
from mpmath import iv

import fwd
import osil

HERE = os.path.dirname(os.path.abspath(__file__))
W3 = _REPRO_ROOT + "/research-20260929/open-instances-wave3"
DPS = 60

# our rigorous dual bounds (open-instances-summary.md; exact binary64 values as stored)
DUAL = {
    # ann: ann/extension.md, "-3386.5402291369187 ... exactly -3386.540229136918696895..."
    "ann_cumene_tanh": Fr(-3386.5402291369187),
    # KAN: logs/<name>.result.json "dual_bound" (bound for R)
    "kan_r5_h1_n3": None, "kan_r5_h1_n5": None, "kan_r5_h1_n8": None,
}


def fmt(q, d=30):
    with mp.workdps(d + 10):
        return mp.nstr(mp.mpf(q.numerator) / q.denominator, d)


def read_sol(path):
    d = {}
    for line in open(path):
        p = line.split()
        if len(p) == 2:
            d[p[0]] = p[1]
    return d


def partition_rows(M):
    isb = [t in ("B", "I") for t in M["vtype"]]
    out = []
    for c in M["cons"]:
        if c["lb"] is None or c["lb"] != c["ub"] or c["quad"] or c["nl"] is not None:
            continue
        if c["lb"] == 1 and c["const"] == 0 and c["lin"] and all(a == 1 for a in c["lin"].values()) \
                and not any(isb[j] for j in c["lin"]):
            out.append(c["name"])
    return out


def kan_inputs(name):
    """Indices of the input variables (class roots) from the wave-3 decoder; used as a hint
    only: the forward construction below must then determine every variable."""
    sys.path.insert(0, os.path.join(W3, "kan"))
    sys.path.insert(0, _REPRO_ROOT + "/research-20260929/open-instances-wave2/small")
    sys.path.insert(0, _REPRO_ROOT + "/research-20260929/reviews/open-instances-verification")
    import kan_model as km
    D = km.decode(name)
    return D["inputs"], [Hd["h"] for Hd in D["hidden"]]


def main(name):
    iv.dps = DPS
    mp.mp.dps = DPS
    t0 = time.time()
    M = osil.load(name)
    N = M["names"]
    idx = {n: i for i, n in enumerate(N)}
    log = []
    P = lambda s: (print(s), log.append(s))
    if name == "ann_cumene_tanh":
        sol = read_sol(os.path.join(W3, "sol", "ann_cumene_tanh.wave3.sol"))
        inputs = [idx[n] for n in ("x723", "x724", "x725", "x726", "x727")]
        u = [Fr(sol[N[j]]) for j in inputs]
        skip = []
        dual = DUAL[name]
        src = "open-instances-wave3/sol/ann_cumene_tanh.wave3.sol (input values, decimal)"
    else:
        res = json.load(open(os.path.join(W3, "logs", f"{name}.result.json")))
        inputs, hidden = kan_inputs(name)
        u = [Fr(v) for v in res["u"]]  # exact binary64 values of the wave-3 inputs
        skip = partition_rows(M)
        dual = Fr(res["dual_bound"])
        src = f"open-instances-wave3/logs/{name}.result.json (input vector u, binary64)"
    P(f"{name}: {len(N)} variables, {len(M['cons'])} rows; inputs {[N[j] for j in inputs]}")
    P(f"inputs (exact rationals): {[str(q) for q in u]}")
    if skip:
        P(f"partition rows dropped (relaxation R): {len(skip)}")
    Fw = fwd.Forward(M, skip_rows=skip)
    P(f"binary groups (one-hot rows with an edge argument): {len(Fw.groups)}")
    fixed = dict(zip(inputs, u))
    res = Fw.run(fixed, "iv")
    nd = sum(1 for v in res["X"] if v is not None)
    P(f"forward construction: {nd} of {len(N)} variables determined; {len(res['used'])} equality rows used as definitions")
    rep = Fw.check(res)
    P(f"rows not used as definitions: {len(rep['unused_eq_exact'])} equality rows checked exactly "
      f"(e.g. {rep['unused_eq_exact'][:3]}), {len(rep['unused_eq_uncertified'])} equality rows NOT certifiable "
      f"{rep['unused_eq_uncertified'][:5]}, {len(rep['skipped'])} skipped (dropped by R); "
      f"inequality rows: {rep['ineq_exact']} exact, {rep['ineq_iv']} by intervals; "
      f"smallest interval margin {float(rep['min_margin'][0]) if rep['min_margin'] else None:.3e} "
      f"({rep['min_margin'][1] if rep['min_margin'] else ''})")
    assert not rep["unused_eq_uncertified"]
    bad, minm = Fw.check_bounds(res)
    P(f"variable bounds: {len(bad)} not proved {bad[:10]}; smallest proved margin of an interval value "
      f"{float(minm[0]):.3e} ({minm[1]})")
    nbin = sum(1 for j in range(len(N)) if M["vtype"][j] in ("B", "I"))
    assert all(res["Q"][j] is not None and res["Q"][j].denominator == 1
               for j in range(len(N)) if M["vtype"][j] in ("B", "I"))
    P(f"integrality: {nbin} binaries exact 0/1")
    O = Fw.objective(res)
    olo, ohi = fwd.lo_frac(O), fwd.hi_frac(O)
    P(f"objective enclosure: [{fmt(olo)}, {fmt(ohi)}] (width {float(ohi - olo):.2e})")
    gap = ohi - dual
    P(f"dual bound {float(dual)!r} (exact {dual}); rigorous gap = upper end - dual = {float(gap):.12e}"
      f" (relative to |primal|: {float(gap / abs(olo)):.6e}; to |dual|: {float(gap / abs(dual)):.6e})")
    if name != "ann_cumene_tanh":
        hid = set(hidden)
        hb = [b for b in bad if idx[b[0]] in hid]
        P(f"hidden-neuron variables {[N[j] for j in hidden]}: bound problems {hb}")
    # Point file: inputs exactly; other variables as rationals or outward intervals {lo, hi}.
    pts = {}
    for j in range(len(N)):
        if res["Q"][j] is not None:
            pts[N[j]] = str(res["Q"][j])
        else:
            X = res["X"][j]
            lo, hi = fwd.lo_frac(X), fwd.hi_frac(X)
            pts[N[j]] = dict(lo=fwd.dec_out(lo, 45), hi=fwd.dec_out(hi, 45, up=True), defined_by=res["defrow"].get(j))
    out = dict(instance=name, source=src,
               construction=("inputs fixed at the given rationals; every other variable is the exact real value "
                             "defined by its row 'defined_by' (that row solved for the variable, which appears "
                             "linearly with a nonzero coefficient), in the order of the rows' use; values given "
                             "as rationals or as enclosing intervals {lo, hi}"),
               inputs={N[j]: str(q) for j, q in zip(inputs, u)},
               dropped_rows=skip,
               objective_lo=fwd.dec_out(olo, 45), objective_hi=fwd.dec_out(ohi, 45, up=True),
               objective=fmt((olo + ohi) / 2, 40), dual_bound=str(dual), gap_upper=fwd.dec_out(gap, 30, up=True),
               unproved_bounds=bad, log=log, x=pts)
    path = os.path.join(HERE, "..", "points", f"{name}.point.json")
    json.dump(out, open(path, "w"), indent=0)
    P(f"wrote {os.path.relpath(path, HERE)}; time {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1])
