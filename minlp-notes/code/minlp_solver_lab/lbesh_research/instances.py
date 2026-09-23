"""Deterministic bounded convex GDPs for controlled LB-ESH experiments.

``build(name)`` returns a fresh Pyomo model initialized at a feasible witness.
``MANIFEST`` and ``manifest()`` expose the predeclared experiment split.  No
instance parameters depend on a solver result.  See the accompanying research
note for convexity, domain, witness, and experiment-design arguments.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import math
import random

import pyomo.environ as pyo
from pyomo.gdp import Disjunct, Disjunction


SEEDS = (104729, 130363, 155921)
SIZES = {"small": 3, "medium": 8, "large": 16}
LAWS = ("exp", "log", "reciprocal", "quadratic", "trig")


def _phi(z, law, symbolic=False):
    if law == "exp":
        return ((pyo.exp if symbolic else math.exp)(3 * z) - 1) / (math.exp(1.5) - 1)
    if law == "log":
        return -(pyo.log if symbolic else math.log)(1 - z) / math.log(2)
    if law == "reciprocal":
        return 1 / (1 - z) - 1
    if law == "quadratic":
        return 4 * z**2
    if law == "trig":
        return (1 - (pyo.cos if symbolic else math.cos)(1.5 * z)) / (1 - math.cos(0.75))
    raise ValueError(law)


def _allocation_data(n, seed):
    rng = random.Random(seed)
    data = []
    for i in range(n):
        capacity = rng.uniform(0.8, 1.2)
        data.append({
            "capacity": capacity,
            "weight": [rng.uniform(0.75, 1.25) for _ in range(2)],
            "cross": rng.uniform(0.2, 0.5),
            "fixed": [0.0, rng.uniform(0.08, 0.12), rng.uniform(0.25, 0.35)],
            "operating": [0.0, rng.uniform(1.05, 1.25), rng.uniform(0.65, 0.85)],
            "mode_capacity": [0.0, rng.uniform(0.58, 0.68), 1.0],
            "resource": [rng.uniform(0.7, 1.3) for _ in range(2)],
        })
    return data


def _cost(x0, x1, datum, mode, law, symbolic=False):
    # The variable box alone puts every argument at or below 1/1.1.
    domain = 1.1 * datum["capacity"]
    return datum["capacity"] * datum["operating"][mode] * (
        datum["weight"][0] * _phi(x0 / domain, law, symbolic)
        + datum["weight"][1] * _phi(x1 / domain, law, symbolic)
        + datum["cross"] * _phi((x0 + x1) / (2 * domain), law, symbolic)
    )


def _allocation(law, n, seed):
    data = _allocation_data(n, seed)
    m = pyo.ConcreteModel()
    m.I = pyo.RangeSet(0, n - 1)
    m.P = pyo.RangeSet(0, 1)
    m.J = pyo.RangeSet(0, 2)
    witness = {(i, p): (0.28 if p == 0 else 0.22) * data[i]["capacity"]
               for i in m.I for p in m.P}
    m.x = pyo.Var(m.I, m.P, bounds=lambda _, i, p: (0, data[i]["capacity"]),
                  initialize=lambda _, i, p: witness[i, p])
    # Individual box bounds, not the sum constraint, suffice for these bounds.
    upper = {i: 1.05 * max(_cost(data[i]["capacity"], data[i]["capacity"],
                                      data[i], j, law) for j in (1, 2)) for i in m.I}
    cost_witness = {i: _cost(witness[i, 0], witness[i, 1], data[i], 1, law)
                    for i in m.I}
    m.t = pyo.Var(m.I, bounds=lambda _, i: (0, upper[i]),
                  initialize=lambda _, i: cost_witness[i])
    m.total_capacity = pyo.Constraint(m.I, rule=lambda _, i:
                                     m.x[i, 0] + m.x[i, 1] <= data[i]["capacity"])
    m.demand = pyo.Constraint(m.P, rule=lambda _, p:
                             sum(m.x[i, p] for i in m.I) >= sum(witness[i, p] for i in m.I))
    resource = sum(data[i]["resource"][p] * witness[i, p] for i in m.I for p in m.P)
    m.resource = pyo.Constraint(expr=sum(data[i]["resource"][p] * m.x[i, p]
                                          for i in m.I for p in m.P) <= 1.08 * resource)
    congestion_witness = sum(((witness[i, 0] + 0.35 * witness[(i + 1) % n, 1])
                              / data[i]["capacity"])**2 for i in m.I)
    m.congestion = pyo.Constraint(expr=sum(((m.x[i, 0] + 0.35 * m.x[(i + 1) % n, 1])
                                           / data[i]["capacity"])**2 for i in m.I)
                                 <= 1.08 * congestion_witness)

    def mode_rule(d, i, j):
        d.capacity = pyo.Constraint(expr=m.x[i, 0] + m.x[i, 1]
                                    <= data[i]["capacity"] * data[i]["mode_capacity"][j])
        if j == 0:
            d.off_cost = pyo.Constraint(expr=m.t[i] == 0)
        else:
            d.cost = pyo.Constraint(expr=_cost(m.x[i, 0], m.x[i, 1], data[i], j, law, True)
                                   <= m.t[i])

    m.mode = Disjunct(m.I, m.J, rule=mode_rule)
    m.choose = Disjunction(m.I, rule=lambda _, i: [m.mode[i, j] for j in m.J], xor=True)
    for i in m.I:
        for j in m.J:
            m.mode[i, j].indicator_var.set_value(j == 1)
    m.objective = pyo.Objective(expr=sum(m.t[i] + sum(
        data[i]["capacity"] * data[i]["fixed"][j] * m.mode[i, j].binary_indicator_var
        for j in m.J) for i in m.I))
    m._research_data = {"parameters": data, "witness_modes": [1] * n}
    return m


def _geometry_data(n, seed):
    rng = random.Random(seed)
    centers = ((-0.75, -0.35), (0.25, 0.7), (0.8, -0.45))
    return [{"centers": [[a + rng.uniform(-0.08, 0.08), b + rng.uniform(-0.08, 0.08)]
                         for a, b in centers],
             "scale": [[rng.uniform(1.7, 2.3), rng.uniform(1.7, 2.3)] for _ in centers],
             "radius": [rng.uniform(4.8, 5.6) for _ in centers],
             "price": [rng.uniform(0.8, 1.2), rng.uniform(0.15, 0.35)],
             "fixed": [rng.uniform(0.02, 0.08) for _ in centers]}
            for _ in range(n)]


def _geometry(n, seed):
    data = _geometry_data(n, seed)
    m = pyo.ConcreteModel()
    m.I = pyo.RangeSet(0, n - 1)
    m.P = pyo.RangeSet(0, 1)
    m.J = pyo.RangeSet(0, 2)
    m.x = pyo.Var(m.I, m.P, bounds=(-2, 2),
                  initialize=lambda _, i, p: data[i]["centers"][1][p])
    witness_t = sum((data[i]["centers"][1][0]
                     - 0.5 * data[(i + 1) % n]["centers"][1][1])**2 for i in m.I)
    m.t = pyo.Var(bounds=(0, 9 * n), initialize=witness_t)
    m.demand0 = pyo.Constraint(expr=sum(m.x[i, 0] for i in m.I) >= 0)
    m.demand1 = pyo.Constraint(expr=sum(m.x[i, 1] for i in m.I) >= 0.1 * n)
    m.congestion = pyo.Constraint(expr=sum((m.x[i, 0] - 0.5 * m.x[(i + 1) % n, 1])**2
                                          for i in m.I) <= m.t)
    m.variation = pyo.Constraint(expr=sum((m.x[i, p] - m.x[(i + 1) % n, p])**2
                                         for i in m.I for p in m.P) <= 0.55 * n)

    def mode_rule(d, i, j):
        d.region = pyo.Constraint(expr=sum(
            pyo.exp(sign * data[i]["scale"][j][p] * (m.x[i, p] - data[i]["centers"][j][p]))
            for p in m.P for sign in (-1, 1)) <= data[i]["radius"][j])

    m.mode = Disjunct(m.I, m.J, rule=mode_rule)
    m.choose = Disjunction(m.I, rule=lambda _, i: [m.mode[i, j] for j in m.J], xor=True)
    for i in m.I:
        for j in m.J:
            m.mode[i, j].indicator_var.set_value(j == 1)
    m.objective = pyo.Objective(expr=sum(data[i]["price"][p] * m.x[i, p]
                                       for i in m.I for p in m.P) + 0.1 * m.t + sum(
        data[i]["fixed"][j] * m.mode[i, j].binary_indicator_var for i in m.I for j in m.J))
    m._research_data = {"parameters": data, "witness_modes": [1] * n}
    return m


MANIFEST = {}
for _law in LAWS + ("logsumexp",):
    for _size, _n in SIZES.items():
        for _seed in (SEEDS[:2] if _law == "logsumexp" else SEEDS):
            _name = f"lbesh.{_law}.{_size}.s{_seed}"
            MANIFEST[_name] = {
                "name": _name, "family": _law, "size": _size, "seed": _seed,
                "split": "pilot" if _seed == SEEDS[0] else "held_out",
                "generator_version": 1, "units": _n, "n_disjunctions": _n,
                "n_disjuncts": 3 * _n, "n_binary": 3 * _n,
                "n_continuous": 2 * _n + 1 if _law == "logsumexp" else 3 * _n,
                "n_nonlinear_disjunct_rows": 3 * _n if _law == "logsumexp" else 2 * _n,
                "n_nonlinear_global_rows": 2 if _law == "logsumexp" else 1,
                "n_global_constraints": 4 if _law == "logsumexp" else _n + 4,
                "n_disjunct_constraints": 3 * _n if _law == "logsumexp" else 6 * _n,
                "quadratic_control": _law == "quadratic", "known_optimum": None,
                "witness_modes": [1] * _n,
                "mechanism": "coupled_regions" if _law == "logsumexp" else "technology_allocation",
            }
            _parameters = (_geometry_data(_n, _seed) if _law == "logsumexp"
                           else _allocation_data(_n, _seed))
            MANIFEST[_name]["parameters_sha256"] = hashlib.sha256(json.dumps(
                _parameters, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def manifest():
    """Return independent metadata; the declared held-out seeds are not tuned."""
    return deepcopy(MANIFEST)


def parameters(name):
    """Return all generated coefficients in a JSON-serializable structure."""
    info = MANIFEST[name]
    return (_geometry_data(info["units"], info["seed"]) if info["family"] == "logsumexp"
            else _allocation_data(info["units"], info["seed"]))


def build(name):
    """Build a named model with a feasible initialization, without solving it."""
    info = MANIFEST[name]
    model = (_geometry(info["units"], info["seed"]) if info["family"] == "logsumexp"
             else _allocation(info["family"], info["units"], info["seed"]))
    model.name = name
    model._research_metadata = deepcopy(info)
    return model


def witness(name):
    """Return the explicit primal witness, including GDP indicator values."""
    model = build(name)
    return {
        "variables": {v.name: pyo.value(v) for v in model.component_data_objects(
            pyo.Var, descend_into=(pyo.Block, Disjunct))},
        "modes": list(model._research_data["witness_modes"]),
        "objective": pyo.value(model.objective),
    }
