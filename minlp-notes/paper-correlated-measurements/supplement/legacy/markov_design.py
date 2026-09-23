"""Exact scalar AR(1) measurement selection, using two convex OA formulations.

Bounds and stopping decisions use floating-point Gurobi tolerances; they are not
formal arithmetic certificates. See README.md for the model and CLI examples.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from itertools import combinations
import json
import math
from time import perf_counter
from typing import Literal

import gurobipy as gp
import numpy as np
from numpy.typing import NDArray

Array = NDArray[np.float64]
Formulation = Literal["path", "dense"]


@dataclass(frozen=True)
class Chain:
    """Rows of F are scalar-observation sensitivities at consecutive times."""

    F: Array
    rho: float
    sigma: float = 1.0

    def __post_init__(self) -> None:
        F = np.array(self.F, dtype=float, copy=True)
        if F.ndim != 2 or min(F.shape) < 1 or not np.all(np.isfinite(F)):
            raise ValueError("F must be a finite, nonempty n-by-p matrix")
        if not math.isfinite(self.rho) or abs(self.rho) >= 1:
            raise ValueError("rho must satisfy abs(rho) < 1")
        if not math.isfinite(self.sigma) or self.sigma <= 0:
            raise ValueError("sigma must be positive and finite")
        F.setflags(write=False)
        object.__setattr__(self, "F", F)

    def covariance(self) -> Array:
        indices = np.arange(len(self.F))
        return self.sigma**2 * self.rho ** np.abs(indices[:, None] - indices)


@dataclass(frozen=True)
class Design:
    chains: tuple[Chain, ...]
    prior: Array
    k: int

    def __post_init__(self) -> None:
        chains = tuple(self.chains)
        prior = np.array(self.prior, dtype=float, copy=True)
        if not chains:
            raise ValueError("at least one chain is required")
        p = chains[0].F.shape[1]
        if any(chain.F.shape[1] != p for chain in chains):
            raise ValueError("all chains must have the same parameter dimension")
        if prior.shape != (p, p) or not np.all(np.isfinite(prior)):
            raise ValueError("prior must be a finite p-by-p matrix")
        if not np.allclose(prior, prior.T, rtol=1e-12, atol=1e-14):
            raise ValueError("prior must be symmetric")
        prior = (prior + prior.T) / 2
        np.linalg.cholesky(prior)
        n = sum(len(chain.F) for chain in chains)
        if not isinstance(self.k, (int, np.integer)) or not 0 <= self.k <= n:
            raise ValueError("k must be an integer between zero and n")
        prior.setflags(write=False)
        object.__setattr__(self, "chains", chains)
        object.__setattr__(self, "prior", prior)

    @property
    def n(self) -> int:
        return sum(len(chain.F) for chain in self.chains)

    @property
    def p(self) -> int:
        return len(self.prior)


def logdet(J: Array) -> float:
    """Use Cholesky so an indefinite matrix cannot masquerade as positive definite."""
    return float(2 * np.log(np.diag(np.linalg.cholesky((J + J.T) / 2))).sum())


def exact_information(design: Design, selected: tuple[int, ...]) -> Array:
    """Independent reference: invert each selected dense covariance submatrix.

    Indices are zero-based and flattened in chain order. Any subset size is
    allowed, including full selection for the initial upper bound.
    """
    if len(set(selected)) != len(selected) or any(
        not isinstance(i, (int, np.integer)) or not 0 <= i < design.n
        for i in selected
    ):
        raise ValueError("selected must contain distinct valid integer indices")
    J = design.prior.copy()
    offset = 0
    for chain in design.chains:
        indices = np.array(
            [i - offset for i in selected if offset <= i < offset + len(chain.F)],
            dtype=int,
        )
        if len(indices):
            F = chain.F[indices]
            R = chain.sigma**2 * chain.rho ** np.abs(indices[:, None] - indices)
            J += F.T @ np.linalg.solve(R, F)
        offset += len(chain.F)
    return (J + J.T) / 2


def exact_objective(design: Design, selected: tuple[int, ...]) -> float:
    return logdet(exact_information(design, selected))


class PathOracle:
    """Affine information on ordered DAG arcs; each chain has a unit flow."""

    def __init__(self, design: Design):
        self.design = design
        self.arcs: list[tuple[int, int, int]] = []
        self.chain_arcs: list[list[int]] = []
        self.arc_lookup: dict[tuple[int, int, int], int] = {}
        weights = []
        for g, chain in enumerate(design.chains):
            n = len(chain.F)
            local = []
            # Source is -1, observations are 0..n-1, and sink is n.
            for i in range(-1, n):
                for j in range(i + 1, n + 1):
                    arc = (g, i, j)
                    local.append(len(self.arcs))
                    self.arc_lookup[arc] = len(self.arcs)
                    self.arcs.append(arc)
                    if j == n:
                        W = np.zeros_like(design.prior)
                    elif i == -1:
                        W = np.outer(chain.F[j], chain.F[j]) / chain.sigma**2
                    else:
                        a = chain.rho ** (j - i)
                        v = chain.F[j] - a * chain.F[i]
                        W = np.outer(v, v) / (chain.sigma**2 * (1 - a**2))
                    weights.append(W)
            self.chain_arcs.append(local)
        self.weights = np.array(weights)

    def subset_point(self, selected: tuple[int, ...]) -> Array:
        point = np.zeros(len(self.arcs))
        offset = 0
        for g, chain in enumerate(self.design.chains):
            n = len(chain.F)
            visits = sorted(i - offset for i in selected if offset <= i < offset + n)
            sequence = [-1, *visits, n]
            for i, j in zip(sequence[:-1], sequence[1:]):
                point[self.arc_lookup[g, i, j]] = 1
            offset += n
        return point

    def information(self, point: Array) -> Array:
        return self.design.prior + np.einsum("a,aij->ij", point, self.weights)

    def value_gradient(self, point: Array) -> tuple[float, Array]:
        J = self.information(point)
        inverse = np.linalg.solve(J, np.eye(self.design.p))
        gradient = np.einsum("ij,aji->a", inverse, self.weights)
        return logdet(J), gradient


class DenseOracle:
    """Liu's binary-exact extension, with a fixed fraction of lambda_min(R)."""

    def __init__(self, design: Design, split_fraction: float = 0.5):
        if not math.isfinite(split_fraction) or not 0 < split_fraction < 1:
            raise ValueError("split_fraction must lie strictly between zero and one")
        self.design = design
        self.blocks = []
        offset = 0
        for chain in design.chains:
            R = chain.covariance()
            a = float(np.linalg.eigvalsh(R)[0]) * split_fraction
            if a <= 0:
                raise ValueError("covariance is not numerically positive definite")
            S = R - a * np.eye(len(R))
            self.blocks.append((slice(offset, offset + len(R)), S, a, chain.F))
            offset += len(R)

    def subset_point(self, selected: tuple[int, ...]) -> Array:
        point = np.zeros(self.design.n)
        point[list(selected)] = 1
        return point

    def _evaluate(self, point: Array) -> tuple[Array, list[tuple[slice, float, Array]]]:
        J = self.design.prior.copy()
        rows = []
        for indices, S, a, F in self.blocks:
            d = point[indices] / a
            V = np.linalg.solve(np.eye(len(S)) + S * d[None, :], F)
            J += F.T @ (d[:, None] * V)
            rows.append((indices, a, V))
        return (J + J.T) / 2, rows

    def information(self, point: Array) -> Array:
        return self._evaluate(point)[0]

    def value_gradient(self, point: Array) -> tuple[float, Array]:
        J, rows = self._evaluate(point)
        gradient = np.zeros(self.design.n)
        for indices, a, V in rows:
            gradient[indices] = np.einsum("ij,ji->i", V, np.linalg.solve(J, V.T)) / a
        return logdet(J), gradient


@dataclass
class OAResult:
    formulation: str
    integer: bool
    status: str
    n: int
    p: int
    k: int
    wall_seconds: float
    oa_rounds: int
    master_nodes: float
    master_status: int | None
    cuts: int
    lower_bound: float | None
    upper_bound: float
    relaxation_value: float | None
    absolute_gap: float
    selected: tuple[int, ...] | None
    objective_residual: float | None
    fractional_visits: tuple[float, ...] | None
    root_oa_rounds: int = 0
    dense_split_fraction: float | None = None


def _solve_oa(
    design: Design,
    formulation: Formulation,
    *,
    integer: bool,
    absolute_gap: float,
    time_limit: float,
    max_rounds: int,
    root_rounds: int = 0,
    split_fraction: float = 0.5,
) -> OAResult:
    if formulation not in ("path", "dense"):
        raise ValueError("formulation must be 'path' or 'dense'")
    if not math.isfinite(absolute_gap) or absolute_gap <= 0:
        raise ValueError("absolute_gap must be positive and finite")
    if not 0 < time_limit <= 30:
        raise ValueError("each experiment must have a time limit in (0, 30] seconds")
    if max_rounds < 0:
        raise ValueError("max_rounds must be nonnegative")
    if not isinstance(root_rounds, int) or root_rounds < 0:
        raise ValueError("root_rounds must be a nonnegative integer")
    started = perf_counter()
    deadline = started + time_limit
    oracle = (PathOracle(design) if formulation == "path"
              else DenseOracle(design, split_fraction))
    all_selected = tuple(range(design.n))
    full_point = oracle.subset_point(all_selected)
    full_value = exact_objective(design, all_selected)
    # A deterministic, feasible seed makes a time-limited run useful as well.
    seed = tuple(int(i) for i in np.linspace(0, design.n - 1, design.k))
    seed_point = oracle.subset_point(seed)
    incumbent = exact_objective(design, seed)
    best_selected = seed if integer else None
    best_relaxation_visits = None
    best_point = seed_point
    if not integer:
        # This mixture is feasible for either relaxation and has total visits k.
        fraction = design.k / design.n
        best_point = fraction * full_point + (1 - fraction) * oracle.subset_point(())
        incumbent = oracle.value_gradient(best_point)[0]
        best_relaxation_visits = tuple([fraction] * design.n)
    upper = full_value
    rounds, nodes, cut_count = 0, 0.0, 0
    root_count = 0
    status, master_status = "iteration_limit", None

    with gp.Env(empty=True) as env:
        env.setParam("OutputFlag", 0)
        env.start()
        with gp.Model("markov_design_" + formulation, env=env) as model:
            model.Params.Threads = 1
            model.Params.Seed = 0
            model.Params.FeasibilityTol = 1e-9
            model.Params.OptimalityTol = 1e-9
            model.Params.IntFeasTol = 1e-9
            model.Params.MIPGap = 0
            model.Params.MIPGapAbs = min(1e-9, absolute_gap / 10)
            z = list(model.addVars(design.n, lb=0, ub=1,
                                  vtype=gp.GRB.BINARY if integer else gp.GRB.CONTINUOUS,
                                  name="z").values())
            model.addConstr(gp.quicksum(z) == design.k, name="cardinality")
            if isinstance(oracle, PathOracle):
                variables = list(model.addVars(len(oracle.arcs), lb=0, ub=1,
                                               name="y").values())
                offset = 0
                for g, chain in enumerate(design.chains):
                    n = len(chain.F)
                    incoming = {j: [] for j in range(n + 1)}
                    outgoing = {i: [] for i in range(-1, n)}
                    for a in oracle.chain_arcs[g]:
                        _, i, j = oracle.arcs[a]
                        outgoing[i].append(variables[a])
                        incoming[j].append(variables[a])
                    model.addConstr(gp.quicksum(outgoing[-1]) == 1)
                    model.addConstr(gp.quicksum(incoming[n]) == 1)
                    for j in range(n):
                        model.addConstr(gp.quicksum(incoming[j]) == z[offset + j])
                        model.addConstr(gp.quicksum(outgoing[j]) == z[offset + j])
                    offset += n
            else:
                variables = z
            t = model.addVar(lb=logdet(design.prior), ub=full_value, name="logdet")
            model.setObjective(t, gp.GRB.MAXIMIZE)

            def add_cut(point: Array) -> None:
                nonlocal cut_count
                value, gradient = oracle.value_gradient(point)
                tangent = gp.LinExpr(gradient.tolist(), variables)
                model.addConstr(t <= value - float(gradient @ point) + tangent)
                cut_count += 1

            add_cut(full_point)
            add_cut(best_point)
            if integer and root_rounds:
                for variable in z:
                    variable.VType = gp.GRB.CONTINUOUS
                for _ in range(root_rounds):
                    remaining = deadline - perf_counter()
                    if remaining <= 0:
                        break
                    model.Params.TimeLimit = remaining
                    model.optimize()
                    root_count += 1
                    if model.Status != gp.GRB.OPTIMAL:
                        break
                    upper = min(upper, float(model.ObjVal))
                    point = np.clip(np.array([v.X for v in variables]), 0, 1)
                    root_value = oracle.value_gradient(point)[0]
                    visits = np.array([v.X for v in z])
                    candidate = tuple(sorted(int(i) for i in
                                      np.argsort(-visits, kind="stable")[:design.k]))
                    candidate_value = exact_objective(design, candidate)
                    if candidate_value > incumbent:
                        incumbent, best_selected = candidate_value, candidate
                        best_point = oracle.subset_point(candidate)
                    add_cut(point)
                    if upper - root_value <= max(absolute_gap, 1e-5):
                        break
                for variable in z:
                    variable.VType = gp.GRB.BINARY
            if integer:
                for j, variable in enumerate(z):
                    variable.Start = int(j in best_selected)
                for variable, value in zip(variables, best_point):
                    variable.Start = float(value)
                t.Start = incumbent

            for _ in range(max_rounds):
                remaining = deadline - perf_counter()
                if remaining <= 0:
                    status = "time_limit"
                    break
                model.Params.TimeLimit = remaining
                model.optimize()
                rounds += 1
                master_status = model.Status
                nodes += model.NodeCount
                if integer:
                    candidate_upper = model.ObjBound
                    if math.isfinite(candidate_upper):
                        upper = min(upper, float(candidate_upper))
                elif master_status == gp.GRB.OPTIMAL:
                    upper = min(upper, float(model.ObjVal))

                point = None
                if model.SolCount:
                    visits = np.array([variable.X for variable in z])
                    if integer:
                        rounded = np.rint(visits)
                        if (np.max(np.abs(visits - rounded)) > 1e-6
                                or int(rounded.sum()) != design.k):
                            status = "invalid_integer_incumbent"
                            break
                        selected = tuple(int(i) for i in np.flatnonzero(rounded))
                        point = oracle.subset_point(selected)
                        # Only the independently evaluated binary subset updates LB.
                        value = exact_objective(design, selected)
                        if value > incumbent:
                            incumbent, best_selected, best_point = value, selected, point
                    else:
                        point = np.array([variable.X for variable in variables])
                        point = np.clip(point, 0, 1)
                        value = oracle.value_gradient(point)[0]
                        if value > incumbent:
                            incumbent, best_point = value, point
                            best_relaxation_visits = tuple(float(v) for v in visits)

                if upper < incumbent - 1e-7 * (1 + abs(incumbent)):
                    status = "numerical_bound_inconsistency"
                    break
                if upper - incumbent <= absolute_gap:
                    status = "optimal_tolerance"
                    break
                if master_status == gp.GRB.TIME_LIMIT or perf_counter() >= deadline:
                    status = "time_limit"
                    break
                if master_status != gp.GRB.OPTIMAL:
                    status = "master_status_" + str(master_status)
                    break
                if point is None:
                    status = "no_master_solution"
                    break
                add_cut(point)

    residual = None
    if integer:
        residual = abs(oracle.value_gradient(best_point)[0]
                       - exact_objective(design, best_selected))
    return OAResult(
        formulation=formulation, integer=integer, status=status,
        n=design.n, p=design.p, k=design.k,
        wall_seconds=perf_counter() - started,
        oa_rounds=rounds, master_nodes=nodes, master_status=master_status,
        cuts=cut_count, lower_bound=incumbent if integer else None,
        upper_bound=upper, relaxation_value=None if integer else incumbent,
        absolute_gap=max(0.0, upper - incumbent), selected=best_selected,
        objective_residual=residual, fractional_visits=best_relaxation_visits,
        root_oa_rounds=root_count,
        dense_split_fraction=split_fraction if formulation == "dense" else None,
    )


def solve_oa(
    design: Design,
    formulation: Formulation,
    *,
    absolute_gap: float = 1e-6,
    time_limit: float = 30,
    max_rounds: int = 500,
    root_rounds: int = 0,
    split_fraction: float = 0.5,
) -> OAResult:
    """Globally solve successive linear MIP masters and add concave tangents."""
    return _solve_oa(design, formulation, integer=True, absolute_gap=absolute_gap,
                     time_limit=time_limit, max_rounds=max_rounds,
                     root_rounds=root_rounds, split_fraction=split_fraction)


def solve_relaxation(
    design: Design,
    formulation: Formulation,
    *,
    absolute_gap: float = 1e-6,
    time_limit: float = 30,
    max_rounds: int = 500,
    split_fraction: float = 0.5,
) -> OAResult:
    """Optimize the continuous relaxation; its feasible value is NOT a MIP LB."""
    return _solve_oa(design, formulation, integer=False, absolute_gap=absolute_gap,
                     time_limit=time_limit, max_rounds=max_rounds,
                     split_fraction=split_fraction)


def enumerate_optimum(design: Design) -> tuple[float, tuple[int, ...]]:
    """Tiny-instance reference. Refuse accidental exponential large runs."""
    if math.comb(design.n, design.k) > 100_000:
        raise ValueError("enumeration is limited to 100,000 subsets")
    return max((exact_objective(design, selected), selected)
               for selected in combinations(range(design.n), design.k))


def generic_design(n: int = 12, p: int = 3, k: int = 4,
                   rho: float = 0.8, seed: int = 0) -> Design:
    rng = np.random.default_rng(seed)
    return Design((Chain(rng.normal(size=(n, p)), rho),), 0.1 * np.eye(p), k)


def reaction_design(n: int = 16, k: int = 5, rho: float = 0.8) -> Design:
    """B-concentration sensitivities for A -> B -> C at nominal rates .7, .2.

    Parameters are log(k1), log(k2), and log(initial A concentration). The time
    grid is uniform on [.1, 12]; AR(1) rho is correlation per grid interval.
    """
    t = np.linspace(0.1, 12.0, n)
    k1, k2 = 0.7, 0.2
    d = k2 - k1
    e1, e2 = np.exp(-k1 * t), np.exp(-k2 * t)
    B = k1 / d * (e1 - e2)
    d1 = k2 / d**2 * (e1 - e2) - k1 / d * t * e1
    d2 = -k1 / d**2 * (e1 - e2) + k1 / d * t * e2
    F = np.column_stack((k1 * d1, k2 * d2, B))
    return Design((Chain(F, rho, sigma=0.05),), 0.01 * np.eye(3), k)


def validate() -> dict:
    """Exhaustive identities, derivative checks, and tiny global solves."""
    rng = np.random.default_rng(91)
    identity_error, gradient_error = 0.0, 0.0
    solves = []
    cases = [generic_design(n=7, p=3, k=3, rho=rho, seed=6)
             for rho in (0.0, 0.6, 0.95, -0.4)]
    cases.append(Design((Chain(rng.normal(size=(3, 2)), 0.8),
                         Chain(rng.normal(size=(4, 2)), -0.3, 0.7)),
                        0.2 * np.eye(2), 3))
    for design in cases:
        for oracle in (PathOracle(design), DenseOracle(design)):
            for size in range(design.n + 1):
                for selected in combinations(range(design.n), size):
                    expected = exact_information(design, selected)
                    actual = oracle.information(oracle.subset_point(selected))
                    error = np.linalg.norm(actual - expected) / max(1, np.linalg.norm(expected))
                    identity_error = max(identity_error, float(error))
                    assert error < 1e-10, (type(oracle).__name__, selected, error)
            x0 = oracle.subset_point(tuple(range(0, design.n, 2)))
            x1 = oracle.subset_point(tuple(range(1, design.n, 2)))
            x = 0.43 * x0 + 0.57 * x1
            direction = x1 - x0
            value, gradient = oracle.value_gradient(x)
            h = 1e-5
            observed = (oracle.value_gradient(x + h * direction)[0]
                        - oracle.value_gradient(x - h * direction)[0]) / (2 * h)
            expected = float(gradient @ direction)
            error = abs(observed - expected) / max(1, abs(expected))
            gradient_error = max(gradient_error, error)
            assert error < 1e-7, (type(oracle).__name__, error)
            for y in (x0, x1):
                assert oracle.value_gradient(y)[0] <= value + gradient @ (y - x) + 1e-9

        optimum, _ = enumerate_optimum(design)
        for formulation in ("path", "dense"):
            result = solve_oa(design, formulation, time_limit=10)
            assert result.status == "optimal_tolerance", result
            assert abs(result.lower_bound - optimum) < 1e-7, result
            assert result.upper_bound >= optimum - 1e-7, result
            assert result.objective_residual < 1e-8, result
            root = solve_relaxation(design, formulation, time_limit=10)
            assert root.upper_bound >= optimum - 1e-7, root
            assert root.lower_bound is None and root.selected is None, root
            solves.append({"rho": design.chains[0].rho,
                           "chains": len(design.chains), "formulation": formulation,
                           "integer": asdict(result), "relaxation": asdict(root)})

    for k in (0, 1, 5):
        design = generic_design(n=5, p=2, k=k)
        optimum, _ = enumerate_optimum(design)
        for formulation in ("path", "dense"):
            result = solve_oa(design, formulation, time_limit=5)
            assert result.status == "optimal_tolerance", result
            assert abs(result.lower_bound - optimum) < 1e-7, result
    for formulation in ("path", "dense"):
        limited = solve_oa(generic_design(), formulation, max_rounds=0)
        assert limited.status == "iteration_limit", limited
        assert limited.selected is not None and limited.lower_bound is not None

    reaction = reaction_design()
    times = np.linspace(0.1, 12.0, reaction.n)
    theta = np.log([0.7, 0.2, 1.0])

    def response(parameters: Array) -> Array:
        k1, k2, amplitude = np.exp(parameters)
        return amplitude * k1 / (k2 - k1) * (np.exp(-k1 * times) - np.exp(-k2 * times))

    for j in range(3):
        step = np.zeros(3)
        step[j] = 1e-5
        numeric = (response(theta + step) - response(theta - step)) / 2e-5
        assert np.max(np.abs(numeric - reaction.chains[0].F[:, j])) < 1e-8
    return {"status": "passed", "max_relative_information_error": identity_error,
            "max_relative_directional_derivative_error": gradient_error, "solves": solves}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "solve"))
    parser.add_argument("--family", choices=("generic", "reaction"), default="reaction")
    parser.add_argument("--formulation", choices=("path", "dense", "both"), default="both")
    parser.add_argument("--n", type=int, default=16)
    parser.add_argument("--p", type=int, default=3)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--rho", type=float, default=0.8)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--time-limit", type=float, default=30)
    parser.add_argument("--max-rounds", type=int, default=500)
    parser.add_argument("--absolute-gap", type=float, default=1e-6)
    parser.add_argument("--relaxation", action="store_true")
    args = parser.parse_args()
    if args.command == "validate":
        print(json.dumps(validate(), indent=2))
        return
    design = (reaction_design(args.n, args.k, args.rho) if args.family == "reaction"
              else generic_design(args.n, args.p, args.k, args.rho, args.seed))
    formulations = ("path", "dense") if args.formulation == "both" else (args.formulation,)
    solve = solve_relaxation if args.relaxation else solve_oa
    for formulation in formulations:
        result = solve(design, formulation, absolute_gap=args.absolute_gap,
                       time_limit=args.time_limit, max_rounds=args.max_rounds)
        print(json.dumps(asdict(result)), flush=True)


if __name__ == "__main__":
    main()
