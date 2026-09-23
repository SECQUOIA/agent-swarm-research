"""Fixed-design representation diagnostic using the actual LBESH cut oracle.

Run from this directory: .venv/bin/python lbesh_oracle_diagnostic.py
No optimization model or solver environment is created. Gurobi is imported by
LBESH, but this diagnostic does not request a license or solve a GDP.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path
import platform
import statistics
import time

import numpy as np

from lbesh.solver import LBESH, Stats
from lbesh.structure import NLRow


SCALES = (1, 2, 4, 8, 16, 32)
GEOMETRIC_TOL = 1e-8
REPEATS = 9


class CountedFunction:
    """Analytic row wrapper; all value/gradient calls from NLRow are counted."""

    def __init__(self, qdiag=None, scale=None):
        self.qdiag = None if qdiag is None else np.asarray(qdiag, dtype=float)
        self.scale = scale
        self.vars = [object() for _ in range(1 if qdiag is None else len(qdiag))]
        self.values = self.gradients = 0

    def base(self, x):
        x = np.asarray(x, dtype=float)
        return float(x[0] - 1) if self.qdiag is None else float(np.dot(self.qdiag * x, x) - 1)

    def value(self, x):
        self.values += 1
        q = self.base(x)
        return q if self.scale is None else math.expm1(self.scale * q)

    def grad(self, x):
        self.gradients += 1
        g = np.ones(1) if self.qdiag is None else 2 * self.qdiag * np.asarray(x)
        return g if self.scale is None else self.scale * math.exp(self.scale * self.base(x)) * g

    def value_grad(self, x):
        return self.value(x), self.grad(x)


def make_oracle(esh):
    oracle = LBESH.__new__(LBESH)
    oracle.esh = esh
    oracle.cut_tol = oracle.feas_tol = 1e-12
    oracle.stats = Stats()
    return oracle


def call_cut(oracle, func, candidate, anchor):
    row = NLRow("diagnostic", func)
    point = {id(v): float(x) for v, x in zip(func.vars, candidate)}
    interior = {id(v): float(x) for v, x in zip(func.vars, anchor)}
    cuts = oracle._esh_cuts([row], point, interior, ("diagnostic",))
    if len(cuts) != 1:
        raise AssertionError(f"Expected one separating cut, got {len(cuts)}")
    _, coef, const, z = cuts[0]
    if oracle.esh and all(z[id(v)] == point[id(v)] for v in func.vars):
        raise AssertionError("This diagnostic requires a boundary cut, not ECP fallback")
    normal = np.array([coef.get(id(v), 0.0) for v in func.vars])
    length = float(np.linalg.norm(normal))
    if not math.isfinite(length) or length <= 0:
        raise AssertionError("Invalid cut normal")
    return normal / length, float(const / length), np.array([z[id(v)] for v in func.vars])


def scalar_run(scale, esh):
    func, oracle = CountedFunction(scale=scale), make_oracle(esh)
    trajectory = [2.0]
    recurrence_error = 0.0
    started = time.perf_counter()
    while trajectory[-1] - 1 > GEOMETRIC_TOL:
        p = trajectory[-1]
        normal, const, z = call_cut(oracle, func, [p], [0.0])
        bound = -const / normal[0]
        if not 1 - 1e-12 <= bound < p:
            raise AssertionError("Scalar cut must retain x=1 and improve the master bound")
        if not esh:
            exact_update = 1.0 if scale is None else p + math.expm1(-scale * (p - 1)) / scale
            recurrence_error = max(recurrence_error, abs(bound - exact_update))
        trajectory.append(float(bound))
        if len(trajectory) > 100:
            raise AssertionError("Unexpected scalar iteration count")
    elapsed = time.perf_counter() - started
    return dict(scale=scale, policy="esh" if esh else "ecp", cuts=len(trajectory) - 1,
                function_calls=func.values, gradient_calls=func.gradients,
                root_searches=(len(trajectory) - 1) if esh else 0,
                root_function_calls=func.values - 3 * (len(trajectory) - 1) if esh else 0,
                trajectory=trajectory, geometric_error=max(0.0, trajectory[-1] - 1),
                recurrence_max_error=recurrence_error, elapsed_seconds=elapsed)


def repeated_scalar(scale, esh):
    runs = [scalar_run(scale, esh) for _ in range(REPEATS)]
    result = runs[0]
    for run in runs[1:]:
        for field in ("cuts", "function_calls", "gradient_calls", "trajectory"):
            assert result[field] == run[field], field
    result["elapsed_seconds_samples"] = [run["elapsed_seconds"] for run in runs]
    result["elapsed_seconds_median"] = statistics.median(result["elapsed_seconds_samples"])
    del result["elapsed_seconds"]
    return result


def quadratic_trial(qdiag, radius, angle, scale, esh):
    direction = np.array([math.cos(angle), math.sin(angle)])
    boundary = direction / np.sqrt(qdiag)
    candidate = radius * boundary
    expected_normal = qdiag * boundary
    expected_normal /= np.linalg.norm(expected_normal)
    expected_const = -1 / np.linalg.norm(qdiag * boundary)
    func, oracle = CountedFunction(qdiag, scale), make_oracle(esh)
    started = time.perf_counter()
    normal, const, z = call_cut(oracle, func, candidate, [0, 0])
    elapsed = time.perf_counter() - started
    # Exact ECP has the same normal for these centered radial candidates.
    q = radius**2 - 1
    decrement = q if scale is None else -math.expm1(-scale * q) / scale
    ecp_const = (-2 * radius**2 + decrement) / (2 * radius * np.linalg.norm(qdiag * boundary))
    analytical_const = expected_const if esh else ecp_const
    assert np.max(np.abs(normal - expected_normal)) < 1e-12
    assert abs(const - analytical_const) < 1e-9
    # The entire ellipsoid satisfies this affine cut: its support function is
    # sqrt(n^T Q^-1 n). This check is stronger than a boundary point sample.
    max_feasible_cut_value = float(np.sqrt(np.sum(normal**2 / qdiag)) + const)
    assert max_feasible_cut_value < 1e-10
    depth = float(normal @ candidate + const)
    assert depth > 0
    return dict(shape="disk" if np.all(qdiag == 1) else "ellipsoid", qdiag=qdiag.tolist(),
                radius=radius, angle_radians=angle, scale=scale, policy="esh" if esh else "ecp",
                candidate=candidate.tolist(), anchor=[0, 0], boundary=boundary.tolist(),
                tangent_point=z.tolist(), unit_normal=normal.tolist(), normalized_constant=const,
                exact_support_constant=expected_const, support_constant_error=abs(const - expected_const),
                analytical_cut_constant_error=abs(const - analytical_const),
                max_feasible_cut_value=max_feasible_cut_value, cut_depth=depth,
                function_calls=func.values, gradient_calls=func.gradients,
                root_searches=int(esh), root_function_calls=func.values - 3 if esh else 0,
                elapsed_seconds=elapsed)


def quadratic_runs():
    result = []
    for diag in ([1., 1.], [1., 4.]):
        for radius in (1.25, 1.75):
            for k in range(16):
                for scale in (None,) + SCALES:
                    for esh in (False, True):
                        runs = [quadratic_trial(np.array(diag), radius, 2 * math.pi * k / 16,
                                                scale, esh) for _ in range(REPEATS)]
                        row = runs[0]
                        row["elapsed_seconds_samples"] = [r["elapsed_seconds"] for r in runs]
                        row["elapsed_seconds_median"] = statistics.median(row["elapsed_seconds_samples"])
                        del row["elapsed_seconds"]
                        result.append(row)
    return result


def non_dominance():
    candidate, anchor = [2., 0.], [0., .9]
    witnesses = [[1.2, 1.], [1.3, -2.]]
    result = []
    for esh in (False, True):
        func, oracle = CountedFunction([1., 1.]), make_oracle(esh)
        normal, const, z = call_cut(oracle, func, candidate, anchor)
        violations = [float(normal @ witness + const) for witness in witnesses]
        assert max(float(np.linalg.norm(normal) + const), 0.0) < 1e-10
        assert (violations[0] > 0 and violations[1] < 0) if esh else (violations[0] < 0 and violations[1] > 0)
        result.append(dict(policy="esh" if esh else "ecp", candidate=candidate, anchor=anchor,
                           witnesses=witnesses, witness_cut_values=violations,
                           unit_normal=normal.tolist(), normalized_constant=const,
                           tangent_point=z.tolist(), cut_depth=float(normal @ candidate + const),
                           function_calls=func.values, gradient_calls=func.gradients,
                           root_searches=int(esh), root_function_calls=func.values - 3 if esh else 0))
    return result


def summarize(scalar, quadratic, nondominance):
    esh = [r for r in quadratic if r["policy"] == "esh"]
    ecp = [r for r in quadratic if r["policy"] == "ecp"]
    pairs = list(zip(ecp, esh))
    for a, b in pairs:
        assert all(a[k] == b[k] for k in ("shape", "radius", "angle_radians", "scale"))
        assert b["cut_depth"] >= a["cut_depth"] - 1e-10
    return dict(scalar_trials=len(scalar), quadratic_trials=len(quadratic),
                quadratic_esh_max_support_constant_error=max(r["support_constant_error"] for r in esh),
                quadratic_ecp_support_constant_error_range=[min(r["support_constant_error"] for r in ecp),
                                                            max(r["support_constant_error"] for r in ecp)],
                quadratic_min_esh_minus_ecp_depth=min(b["cut_depth"] - a["cut_depth"] for a, b in pairs),
                all_scalar_esh_cut_counts_one=all(r["cuts"] == 1 for r in scalar if r["policy"] == "esh"),
                max_scalar_recurrence_error=max(r["recurrence_max_error"] for r in scalar),
                nondominance_confirmed=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "results/lbesh_development/oracle_diagnostic.json")
    args = parser.parse_args()
    # Warm imports and the tiny oracle path before collecting descriptive times.
    scalar_run(1, True)
    scalar_run(1, False)
    scalar = [repeated_scalar(a, esh) for a in (None,) + SCALES for esh in (False, True)]
    quadratic, nondominance = quadratic_runs(), non_dominance()
    dependencies = {name: importlib.metadata.version(name) for name in ("numpy", "pyomo", "gurobipy")}
    root = Path(__file__).parent
    sources = [Path(__file__), root / "lbesh/solver.py", root / "lbesh/structure.py"]
    output = dict(schema_version=1, generated_utc=datetime.now(timezone.utc).isoformat(),
                  design=dict(scales=list(SCALES), scalar_initial_master=2, scalar_anchor=0,
                              scalar_stop="max(0,x-1) <= 1e-8", scalar_initial_cuts="box only",
                              cut_tol=1e-12, feas_tol=1e-12, timing_repeats=REPEATS,
                              quadratic_radii=[1.25, 1.75], quadratic_angles="2*pi*k/16, k=0,...,15",
                              quadratic_anchor="center (0,0)", normalized_cut="unit Euclidean normal, original x space",
                              none_scale_means="untransformed base row", timing_scope="oracle, Python bookkeeping, and scalar bound update; excludes imports and setup",
                              root_count_accounting="ESH total function calls minus one candidate, one anchor, and one tangent value per cut; ECP fallback is asserted absent",
                              scope="mechanistic diagnostic; no GDP solve or representative speedup claim"),
                  environment=dict(python=platform.python_version(), platform=platform.platform(), dependencies=dependencies),
                  source_sha256={str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
                  scalar=scalar, quadratic=quadratic, nondominance=nondominance,
                  summary=summarize(scalar, quadratic, nondominance))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps(output["summary"], indent=2))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
