"""Discover small nonlinear blocks and add certified global cuts at SCIP's root.

Native SCIP constraints always enforce the original expressions and auxiliary
definitions. Floating point sampling and LPs only propose directions; certified
support bounds determine every added right-hand side. No custom propagation,
branching, presolve-bound inference, or local cuts are used.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from functools import lru_cache
from fractions import Fraction
import itertools
import math
from pathlib import Path
import sys
import time
import warnings

import numpy as np
from scipy.optimize import linprog, OptimizeWarning
import sympy as sp
import pyscipopt as ps

from .model_binding import (assert_source_domains, native_expression,
                            normalize_constant_trees, same_expression)

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "code" / "univariate_envelopes"))
from uenv.osil import Instance, read_osil, _scip_expr


class SourceModelMismatch(ValueError):
    """Refuse a numerical construction that is unequal to its exact source."""


@dataclass(frozen=True)
class Config:
    """Fixed, deliberately small experimental work limits."""

    max_atoms: int = 256
    max_blocks: int = 64
    max_features: int = 8
    max_degree_1d: int = 8
    max_degree_2d: int = 4
    grid_1d: int = 65
    grid_2d: int = 13
    max_rounds: int = 5
    max_cuts: int = 24
    max_cuts_per_round: int = 6
    max_cells: int = 128
    max_depth: int = 16
    max_separation_seconds: float = 2.0
    separation_budget_fraction: float = 0.15
    min_violation: float = 1e-5
    auto_min_violation: float = 5e-4
    cache_samples: bool = True
    merge_stars: bool = True
    gap_limit: float = 1e-4
    max_exchange_rounds: int = 3

    def __post_init__(self):
        positive = ("max_atoms", "max_blocks", "max_features", "max_degree_1d", "max_degree_2d",
                    "grid_1d", "grid_2d", "max_rounds", "max_cuts", "max_cuts_per_round",
                    "max_cells", "max_exchange_rounds")
        if any(getattr(self, name) < 1 for name in positive) or self.max_features < 3:
            raise ValueError("work limits must be positive and max_features at least three")
        if self.max_depth < 0 or self.max_separation_seconds < 0 or not 0 <= self.separation_budget_fraction <= 1:
            raise ValueError("invalid separation budget")
        if self.min_violation <= 0 or self.auto_min_violation <= 0 or self.gap_limit < 0:
            raise ValueError("invalid violation or gap threshold")


@dataclass
class Atom:
    index: int
    tree: tuple
    expr: sp.Expr
    variables: tuple[int, ...]
    nonlinear_ops: int
    admitted: bool = True


@dataclass
class Block:
    variables: tuple[int, ...]
    atoms: tuple[int, ...]
    features: tuple[sp.Expr, ...]
    symbols: tuple[sp.Symbol, ...]
    box: tuple[tuple[float, float], ...]
    rows: tuple = ()
    auto_eligible: bool = False
    sample: np.ndarray | None = None
    scale: np.ndarray | None = None
    offset: np.ndarray | None = None
    previous_point: np.ndarray | None = None
    failures: int = 0
    cuts: int = 0
    sample_points: np.ndarray | None = None
    screening_cache: object = None
    screening_samples: object = None
    screening_weights: tuple | None = None
    last_screen: object = None
    exact_quadratic: bool = False


@dataclass
class Detected:
    atoms: list[Atom]
    rewritten_rows: list[tuple | None]
    quadratic_atoms: dict[tuple[int, int], int]
    blocks: list[Block]
    stats: dict


@lru_cache(maxsize=32768)
def _variables(tree):
    if tree[0] == "var":
        return frozenset((tree[1],))
    if tree[0] == "num":
        return frozenset()
    return frozenset().union(*(_variables(c) for c in tree[1:]))


@lru_cache(maxsize=32768)
def _nonlinear_ops(tree):
    op = tree[0]
    if op in ("num", "var"):
        return 0
    own = int(op not in ("sum", "negate", "times", "divide"))
    if op == "times":
        own = int(sum(bool(_variables(c)) for c in tree[1:]) >= 2)
    if op == "divide":
        own = int(bool(_variables(tree[2])))
    return own + sum(_nonlinear_ops(c) for c in tree[1:])


def exact_expression(tree, symbols):
    """Real interpretation of the binary64 constants in the loaded OSiL tree."""
    op = tree[0]
    if op == "num":
        if not math.isfinite(tree[1]):
            raise ValueError("nonfinite expression constant")
        return sp.Rational(float(tree[1]))
    if op == "var":
        return symbols[tree[1]]
    args = [exact_expression(c, symbols) for c in tree[1:]]
    if op == "sum":
        return sp.Add(*args)
    if op == "times":
        return sp.Mul(*args)
    if op == "negate":
        return -args[0]
    if op == "divide":
        return args[0] / args[1]
    if op == "power":
        return args[0] ** args[1]
    if op == "square":
        return args[0] ** 2
    return {"log": sp.log, "exp": sp.exp, "sqrt": sp.sqrt,
            "sin": sp.sin, "cos": sp.cos, "abs": sp.Abs}[op](args[0])


def discover(inst: Instance, config: Config = Config()) -> Detected:
    """Extract bounded atoms; group shared coordinates and row-coupled pairs.

    Sums are split before atom extraction, so different functions of the same
    coordinate remain visible. Native expression trees, including domain
    restrictions, remain the source of every auxiliary definition.
    """
    started = time.perf_counter()
    _variables.cache_clear()
    _nonlinear_ops.cache_clear()
    syms = tuple(sp.Symbol(f"x{i}", real=True) for i in range(len(inst.var_lb)))
    atoms, keys = [], {}
    stats = {"unsupported_atoms": 0, "atom_cap_reached": False,
             "block_cap_reached": False}

    def atom(tree):
        variables = tuple(sorted(_variables(tree)))
        if not 1 <= len(variables) <= 2 or not _nonlinear_ops(tree):
            return None
        if not all(math.isfinite(inst.var_lb[i]) and math.isfinite(inst.var_ub[i])
                   and inst.var_lb[i] < inst.var_ub[i] for i in variables):
            return None
        try:
            expr = exact_expression(tree, syms)
            if not expr.free_symbols:
                return None
            if expr.is_polynomial(*(syms[i] for i in variables)):
                degree = sp.Poly(expr, *(syms[i] for i in variables)).total_degree()
                cap = config.max_degree_1d if len(variables) == 1 else config.max_degree_2d
                if degree < 2 or degree > cap:
                    return None
            elif len(variables) != 1:
                return None
        except (ValueError, TypeError, KeyError, sp.PolynomialError):
            stats["unsupported_atoms"] += 1
            return None
        # Equal simplified expressions can have different source domains:
        # sqrt(x)^4 and x^2 agree only where the former is defined. Sharing by
        # exact source tree preserves every native domain restriction.
        key = (variables, tree)
        if key in keys:
            return keys[key]
        if len(atoms) >= config.max_atoms:
            stats["atom_cap_reached"] = True
            return None
        idx = len(atoms)
        atoms.append(Atom(idx, tree, expr, variables, _nonlinear_ops(tree)))
        keys[key] = idx
        return idx

    def rewrite(tree):
        if tree[0] in ("num", "var"):
            return tree
        # Keep additive features and constant multipliers separate. A factor
        # belongs to its original model row; it need not create a duplicate aux.
        if tree[0] in ("sum", "negate"):
            return (tree[0], *(rewrite(c) for c in tree[1:]))
        if tree[0] == "times":
            varying = [c for c in tree[1:] if _variables(c)]
            if len(varying) == 1 and len(tree) > 2:
                return ("times", *(rewrite(c) for c in tree[1:]))
        idx = atom(tree)
        if idx is not None:
            return ("uni", idx)
        return (tree[0], *(rewrite(c) for c in tree[1:]))

    rewritten, quadratic_atoms = [], {}
    for ri, row in enumerate(inst.rows):
        rewritten.append(rewrite(row["nl"]) if row["nl"] is not None else None)
        for qi, (i, j, coefficient) in enumerate(row["quad"]):
            if coefficient:
                idx = atom(("times", ("var", i), ("var", j)))
                if idx is not None:
                    quadratic_atoms[(ri, qi)] = idx

    # A pair is proposed only if an existing atom or original linear row
    # connects it. This avoids enumerating all variable pairs.
    candidates = {(i,) for a in atoms for i in a.variables if len(a.variables) == 1}
    candidates.update(a.variables for a in atoms if len(a.variables) == 2)
    linear_rows = []
    for row in inst.rows[1:]:
        if row["quad"] or row["nl"] is not None:
            continue
        support = tuple(sorted(i for i, c in row["lin"].items() if c))
        if not 1 <= len(support) <= 2:
            continue
        linear_rows.append((support, row))
        if len(support) == 2:
            candidates.add(support)

    # Merge a genuinely overlapping quadratic star, when its leaves have no
    # leaf-leaf quadratic term. Exact support is delegated to the star oracle.
    # Restricting the feature count bounds work and avoids a tensor grid.
    if config.merge_stars:
        neighbors = {}
        for a in atoms:
            if len(a.variables) == 2 and a.expr.is_polynomial(*(syms[i] for i in a.variables)):
                if sp.Poly(a.expr, *(syms[i] for i in a.variables)).total_degree() <= 2:
                    i, j = a.variables
                    neighbors.setdefault(i, set()).add(j)
                    neighbors.setdefault(j, set()).add(i)
        for center, leaves in sorted(neighbors.items()):
            if not 2 <= len(leaves) <= 4:
                continue
            variables = tuple(sorted({center} | leaves))
            matching = [a for a in atoms if set(a.variables) <= set(variables)]
            if (len(variables) + len(matching) <= config.max_features and
                    all(a.expr.is_polynomial(*(syms[i] for i in variables)) and
                        sp.Poly(a.expr, *(syms[i] for i in variables)).total_degree() <= 2 and
                        (len(a.variables) == 1 or center in a.variables) for a in matching)):
                candidates.add(variables)

    blocks = []
    for variables in sorted(candidates, key=lambda v: (len(v), v)):
        ids = tuple(a.index for a in atoms if set(a.variables) <= set(variables))
        if not ids:
            continue
        # Keeping the first features is explicit bounded support, not a claim
        # that every expression in an arbitrarily large block is included.
        ids = ids[:max(1, config.max_features - len(variables))]
        rows = []
        for support, row in linear_rows:
            if set(support) <= set(variables):
                coeff = tuple(float(row["lin"].get(i, 0)) for i in variables)
                if math.isfinite(row["ub"]):
                    rows.append((coeff, float(row["ub"])))
                if math.isfinite(row["lb"]):
                    rows.append((tuple(-c for c in coeff), float(-row["lb"])))
        features = tuple(syms[i] for i in variables) + tuple(atoms[i].expr for i in ids)
        nonlinear = len(ids)
        eligible = ((len(variables) == 1 and
                     (nonlinear >= 2 or atoms[ids[0]].nonlinear_ops >= 2)) or
                    (len(variables) == 2 and bool(rows) and nonlinear >= 1) or
                    len(variables) >= 3)
        blocks.append(Block(variables, ids, features, tuple(syms[i] for i in variables),
                            tuple((inst.var_lb[i], inst.var_ub[i]) for i in variables),
                            tuple(rows), eligible))
        blocks[-1].exact_quadratic = len(variables) >= 2 and all(
            f.is_polynomial(*(syms[i] for i in variables)) and
            sp.Poly(f, *(syms[i] for i in variables)).total_degree() <= 2 for f in features)
        if len(blocks) >= config.max_blocks:
            stats["block_cap_reached"] = len(candidates) > len(blocks)
            break
    stats.update(atoms=len(atoms), blocks=len(blocks),
                 auto_eligible=sum(b.auto_eligible for b in blocks),
                 discovery_seconds=time.perf_counter() - started)
    return Detected(atoms, rewritten, quadratic_atoms, blocks, stats)


def _sample(block: Block, config: Config):
    if config.cache_samples and block.sample is not None:
        return
    n = config.grid_1d if len(block.symbols) == 1 else config.grid_2d
    axes = [np.linspace(lo, hi, n) for lo, hi in block.box]
    if len(block.symbols) <= 2:
        points = np.asarray(list(itertools.product(*axes)))
    else:
        # Deterministic low-discrepancy samples plus all box corners. Sampling
        # only proposes a normal, so it does not restrict the certified domain.
        from scipy.stats import qmc
        unit = qmc.Halton(len(block.symbols), scramble=False).random(128)
        lower, upper = np.asarray(block.box).T
        points = np.vstack((lower + unit * (upper - lower),
                            list(itertools.product(*[(lo, hi) for lo, hi in block.box]))))
    if block.rows:
        # Infeasible sample points would weaken the candidate problem. A small
        # admission tolerance is harmless: samples have no validity authority.
        mask = np.ones(len(points), dtype=bool)
        for a, rhs in block.rows:
            mask &= points @ np.asarray(a) <= rhs + 1e-12 * max(1, abs(rhs))
        points = points[mask]
    exact_seeds = []
    if len(block.symbols) == 2 and block.rows:
        from theory.quadratic_polygon import polygon_vertices
        vertices = polygon_vertices(block.box, [(*a, rhs) for a, rhs in block.rows])
        exact_seeds.extend(vertices)
        if vertices:
            exact_seeds.append(tuple(sum(p[j] for p in vertices) / len(vertices) for j in range(2)))
            exact_seeds.extend(tuple((a + b) / 2 for a, b in zip(v, w))
                               for v, w in zip(vertices, vertices[1:] + vertices[:1]))
    elif len(block.symbols) >= 3 and block.exact_quadratic:
        from theory.quadratic_star import support_star
        for center in range(len(block.symbols)):
            try:
                # Exact coordinate extrema supply feasible seeds even when
                # affine equalities make every box-grid point infeasible.
                for j in range(len(block.symbols)):
                    powers = tuple(int(i == j) for i in range(len(block.symbols)))
                    for sign in (-1, 1):
                        witness = support_star(block.box, block.rows, {powers: sign}, center)
                        if witness["status"] == "complete":
                            exact_seeds.append(tuple(Fraction(x) for x in witness["minimizer"]))
                break
            except ValueError:
                exact_seeds.clear()
    parameter_points = np.asarray([tuple(Fraction(float(x)) for x in p) for p in points]
                                  + exact_seeds, dtype=object)
    if len(exact_seeds):
        points = np.vstack((points, np.asarray(exact_seeds, dtype=float)))
    if not len(points):
        raise ValueError("grid has no domain samples")
    try:
        from .native_sampling import sampled_features
        values = sampled_features(block.features, block.symbols, points)
    except (ImportError, ValueError, TypeError, sp.PolynomialError):
        fs = [sp.lambdify(block.symbols, f, "numpy") for f in block.features]
        with np.errstate(all="ignore"):
            values = np.column_stack([np.broadcast_to(f(*points.T), (len(points),)) for f in fs])
    if not np.isfinite(values).all():
        raise ValueError("nonfinite sample values")
    lo, hi = np.min(values, axis=0), np.max(values, axis=0)
    block.offset = lo
    block.scale = np.maximum(hi - lo, 1e-10 * np.maximum(1, np.maximum(abs(lo), abs(hi))))
    block.sample = values
    block.sample_points = parameter_points


def propose_direction(block: Block, point, config: Config = Config(), min_violation=None):
    """LP over cached graph samples; returns an uncertified float direction."""
    _sample(block, config)
    p = np.asarray(point, float)
    threshold = config.min_violation if min_violation is None else min_violation
    normalized = (block.sample - block.offset) / block.scale
    pnorm = (p - block.offset) / block.scale
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="Unrecognized options detected.*", category=OptimizeWarning)
        result = linprog(np.r_[1.0, pnorm],
                         A_ub=np.column_stack((-np.ones(len(normalized)), -normalized)),
                         b_ub=np.zeros(len(normalized)),
                         bounds=[(None, None)] + [(-1, 1)] * len(p), method="highs",
                         options={"presolve": True, "time_limit": 0.1,
                                  "threads": 1, "parallel": False})
    if result.success and block.screening_cache is not None:
        # HiGHS row duals supply a convex-combination proposal at no second LP
        # cost. Only its nonzero support is evaluated with exact arithmetic.
        weights = -np.asarray(result.ineqlin.marginals)
        selected = np.flatnonzero(weights > 0)
        if len(selected):
            try:
                block.screening_samples = block.screening_cache.bind(block.sample_points[selected])
                block.screening_weights = tuple(float(w) for w in weights[selected])
            except (ValueError, TypeError, OverflowError):
                # Grid row feasibility was floating point. Exact binding may
                # correctly reject points on a numerically admitted boundary.
                block.screening_samples = None
                block.screening_weights = None
    if not result.success or result.fun >= -threshold:
        return None
    coeff = np.asarray(np.clip(result.x[1:], -1, 1) / block.scale, dtype=float)
    if not np.isfinite(coeff).all() or not np.any(coeff):
        return None
    # These exact floats are passed unchanged to the checker and to SCIP.
    coeff[np.abs(coeff) < 1e-12 * max(1, float(np.max(abs(coeff))))] = 0.0
    for j, value in enumerate(coeff):
        # Preserve max_j scale_j*|c_j| <= 1 after coefficient rounding, matching
        # the exact L1-distance screening guarantee.
        while Fraction(float(block.scale[j])) * abs(Fraction(float(value))) > 1:
            value = np.nextafter(value, 0.0)
        coeff[j] = value
    point_value = float(np.dot(coeff, p))
    sampled_support = float(np.min(block.sample @ coeff))
    if sampled_support - point_value <= threshold:
        return None
    return tuple(float(c) for c in coeff), point_value, sampled_support


def _exchange_sample(block, minimizer):
    """Append an exact support minimizer as heuristic graph-LP information."""
    parameter = tuple(Fraction(v) for v in minimizer)
    if any(tuple(p) == parameter for p in block.sample_points):
        return False
    point = np.asarray([[float(v) for v in parameter]])
    fs = [sp.lambdify(block.symbols, f, "numpy") for f in block.features]
    with np.errstate(all="ignore"):
        value = np.asarray([float(f(*point[0])) for f in fs])
    if not np.isfinite(value).all():
        return False
    block.sample = np.vstack((block.sample, value))
    block.sample_points = np.vstack((block.sample_points, np.asarray(parameter, dtype=object)))
    return True


def _polynomial_source(tree):
    op = tree[0]
    if op in ("num", "var"):
        return True
    if op in ("sum", "times", "negate", "square"):
        return all(_polynomial_source(c) for c in tree[1:])
    if op == "power":
        return (tree[2][0] == "num" and float(tree[2][1]).is_integer()
                and 0 <= tree[2][1] <= 32 and _polynomial_source(tree[1]))
    return False


def _initialize_screen(block, detected):
    """Bind only source polynomials, which have no hidden domain exclusions."""
    from .screening import SampleCache
    if not all(_polynomial_source(detected.atoms[i].tree) for i in block.atoms):
        return
    polynomials = [tuple((powers, Fraction(int(c.p), int(c.q)))
                         for powers, c in sp.Poly(f, *block.symbols, domain=sp.QQ).terms())
                   for f in block.features]

    def evaluate(point):
        return [sum((coefficient * math.prod(x ** power for x, power in zip(point, powers))
                     for powers, coefficient in terms), Fraction(0)) for terms in polynomials]

    block.screening_cache = SampleCache(bounds=block.box, evaluate=evaluate,
                                       rows=[(*a, rhs) for a, rhs in block.rows])


def _audit_inserted_row(model, row, variables, coefficients, rhs):
    """Check exact source-row equivalence after SCIP's row construction.

    Aggregation is disabled for these variables. Any substitution, including a
    numerical presolve fixing, or rounded coefficient/bound change causes the
    proposed row to be discarded. No presolve proof is assumed.
    """
    actual = {c.getVar().name: Fraction(float(a))
              for c, a in zip(row.getCols(), row.getVals()) if a}
    expected, mapping = {}, []
    for variable, coefficient in zip(variables, coefficients):
        if not coefficient:
            continue
        transformed = model.getTransformedVar(variable)
        name, value = transformed.name, Fraction(float(coefficient))
        if name not in actual:
            return None
        expected[name] = expected.get(name, Fraction(0)) + value
        mapping.append({"source": variable.name, "transformed": name})
    expected = {name: value for name, value in expected.items() if value}
    if actual != expected:
        return None
    lhs, constant, upper = float(row.getLhs()), float(row.getConstant()), float(row.getRhs())
    if (not math.isfinite(lhs) or not math.isfinite(constant) or
            upper < model.infinity() or
            row.isLocal() or Fraction(lhs) - Fraction(constant) != Fraction(float(rhs))):
        return None
    return {"local": bool(row.isLocal()), "columns": {name: float(v) for name, v in actual.items()},
            "lhs": lhs, "rhs": upper, "constant": constant,
            "scip_infinity": float(model.infinity()),
            "source_to_transformed": mapping}


def _build(inst, detected, mode):
    m = ps.Model(inst.name)
    if not len(inst.var_lb) == len(inst.var_ub) == len(inst.var_type):
        m.freeProb()
        raise SourceModelMismatch("source variable bound/type lengths differ")
    intervals = [*zip(inst.var_lb, inst.var_ub),
                 *((r["lb"], r["ub"]) for r in inst.rows[1:])]
    if any(math.isnan(lo) or math.isnan(hi) or lo == math.inf or hi == -math.inf or lo > hi
           for lo, hi in intervals):
        m.freeProb()
        raise SourceModelMismatch("source bounds or row sides have NaN, reversed order, or wrong-signed infinity")
    finite_sides = [*inst.var_lb, *inst.var_ub,
                    *(r[side] for r in inst.rows[1:] for side in ("lb", "ub"))]
    if any(math.isfinite(v) and abs(v) >= m.infinity() for v in finite_sides):
        m.freeProb()
        raise SourceModelMismatch("finite source bound or row side reaches SCIP's infinity sentinel")
    for ri, row in enumerate(inst.rows):
        if row["nl"] is not None:
            try:
                assert_source_domains(row["nl"], tuple(zip(inst.var_lb, inst.var_ub)))
            except ValueError as error:
                m.freeProb()
                raise SourceModelMismatch(f"row {ri} source domain is not proved on declared box: {error}") from error
    xs = [m.addVar(name=f"v{i}", lb=None if math.isinf(lo) else lo,
                   ub=None if math.isinf(hi) else hi,
                   vtype={"C": "C", "I": "I", "B": "B"}[kind])
          for i, (lo, hi, kind) in enumerate(zip(inst.var_lb, inst.var_ub, inst.var_type))]
    source_symbols = tuple(sp.Symbol(f"x{i}", real=True) for i in range(len(xs)))
    native_symbols = {v.name: source_symbols[i] for i, v in enumerate(xs)}
    source_rows, native_rows = [], []
    for ri, row in enumerate(inst.rows):
        source = sum(sp.Rational(float(c)) * source_symbols[i] for i, c in row["lin"].items())
        original = sum(c * xs[i] for i, c in row["lin"].items())
        for i, j, c in row["quad"]:
            source += sp.Rational(float(c)) * source_symbols[i] * source_symbols[j]
            original += c * xs[i] * xs[j]
        if row["nl"] is not None:
            source += exact_expression(row["nl"], source_symbols)
            original += _scip_expr(normalize_constant_trees(row["nl"]), xs, {})
        if ri == 0:
            source += sp.Rational(float(inst.obj_const))
            original += inst.obj_const
        if not same_expression(source, native_expression(original, native_symbols)):
            m.freeProb()
            raise SourceModelMismatch(f"row {ri} differs after native binary64 expression assembly")
        source_rows.append(source)
        native_rows.append(original)
    aux = {}
    if mode != "baseline":
        rejected = []
        for a in detected.atoms:
            expression = _scip_expr(normalize_constant_trees(a.tree), xs, {})
            try:
                a.admitted = same_expression(a.expr, native_expression(expression, native_symbols))
            except (ValueError, TypeError, OverflowError):
                a.admitted = False
            if not a.admitted:
                # The native occurrence remains; an exact source certificate
                # is never attached to a rounded, different auxiliary graph.
                rejected.append(a.index)
                aux[a.index] = expression
                continue
            w = m.addVar(name=f"block_aux_{a.index}", lb=None, ub=None)
            m.addCons(w == expression, name=f"block_def_{a.index}")
            aux[a.index] = w
        retained = []
        for block in detected.blocks:
            block.atoms = tuple(i for i in block.atoms if detected.atoms[i].admitted)
            if not block.atoms:
                continue
            block.features = block.symbols + tuple(detected.atoms[i].expr for i in block.atoms)
            if len(block.variables) == 1:
                block.auto_eligible = len(block.atoms) >= 2 or detected.atoms[block.atoms[0]].nonlinear_ops >= 2
            retained.append(block)
        detected.blocks = retained
        detected.stats.update(semantic_mismatch_rejections=rejected,
                              admitted_atoms=sum(a.admitted for a in detected.atoms),
                              blocks=len(retained), auto_eligible=sum(b.auto_eligible for b in retained))
        # Identical presolve treatment in control/all/auto. Native definitions
        # remain enabled, so SCIP owns graph feasibility and branching.
        used = {i for b in detected.blocks for i in b.variables}
        for v in [*(xs[i] for i in sorted(used)), *(aux[a.index] for a in detected.atoms if a.admitted)]:
            m.markDoNotAggrVar(v)
            m.markDoNotMultaggrVar(v)
    for ri, row in enumerate(inst.rows):
        expr = sum(c * xs[i] for i, c in row["lin"].items())
        for qi, (i, j, c) in enumerate(row["quad"]):
            ai = detected.quadratic_atoms.get((ri, qi)) if detected is not None else None
            expr += c * (aux[ai] if mode != "baseline" and ai is not None else xs[i] * xs[j])
        tree = row["nl"] if mode == "baseline" else detected.rewritten_rows[ri]
        if tree is not None:
            expr += _scip_expr(normalize_constant_trees(tree), xs, aux)
        if ri == 0:
            expr += inst.obj_const
        if mode != "baseline":
            rewrite_symbols = dict(native_symbols)
            rewrite_symbols.update({aux[a.index].name: a.expr for a in detected.atoms if a.admitted})
            if not same_expression(source_rows[ri], native_expression(expr, rewrite_symbols)):
                # Native admission succeeded, but a surrounding rewritten sum
                # can still round differently. Keep the original whole row.
                expr = native_rows[ri]
                detected.rewritten_rows[ri] = row["nl"]
                detected.quadratic_atoms = {key: value for key, value in detected.quadratic_atoms.items()
                                            if key[0] != ri}
                detected.stats.setdefault("rewritten_row_rejections", []).append(ri)
        if ri == 0:
            sense = "minimize" if inst.obj_sense == "min" else "maximize"
            if row["quad"] or tree is not None:
                z = m.addVar(name="objective_aux", lb=None, ub=None)
                m.addCons(z >= expr if sense == "minimize" else z <= expr)
                m.setObjective(z, sense)
            else:
                m.setObjective(expr, sense)
        else:
            # A constant infeasible row must remain infeasible. SCIP requires
            # an expression rather than Python's eagerly evaluated bool.
            if isinstance(expr, (int, float)):
                if not row["lb"] <= expr <= row["ub"]:
                    dummy = m.addVar(name=f"constant_infeas_{ri}", lb=0, ub=0)
                    m.addCons(dummy >= 1)
                continue
            if row["lb"] == row["ub"]:
                m.addCons(expr == row["lb"])
            else:
                if math.isfinite(row["lb"]):
                    m.addCons(expr >= row["lb"])
                if math.isfinite(row["ub"]):
                    m.addCons(expr <= row["ub"])
    return m, xs, aux


class BlockSeparator(ps.Sepa):
    def __init__(self, detected, xs, aux, mode, config, budget):
        self.detected, self.xs, self.aux = detected, xs, aux
        self.mode, self.config, self.budget = mode, config, budget
        self.records = []
        self.seen = set()
        self.stats = {"calls": 0, "cuts": 0, "candidate_lps": 0,
                      "certification_calls": 0, "certification_failures": 0,
                      "sampling_failures": 0, "selection_skips": 0,
                      "screen_queries": 0, "screen_skips": 0,
                      "screening_seconds": 0.0,
                      "exchange_samples": 0,
                      "row_binding_rejections": 0,
                      "repeat_skips": 0, "callback_seconds": 0.0,
                      "candidate_seconds": 0.0, "certification_seconds": 0.0,
                      "row_seconds": 0.0, "budget_exhausted": False}

    def _find_support(self, block, point, bi, threshold, round_start):
        from .certified import certify_support
        for _ in range(self.config.max_exchange_rounds):
            candidate_start = time.perf_counter()
            try:
                self.stats["candidate_lps"] += 1
                proposal = propose_direction(block, point, self.config, threshold)
            except (ValueError, TypeError, OverflowError, ZeroDivisionError, NotImplementedError):
                self.stats["sampling_failures"] += 1
                block.failures += 1
                return None
            finally:
                self.stats["candidate_seconds"] += time.perf_counter() - candidate_start
            if proposal is None:
                return None
            coefficients, activity, sampled_support = proposal
            key = (bi, coefficients)
            if key in self.seen:
                return None
            self.seen.add(key)
            cert_start = time.perf_counter()
            self.stats["certification_calls"] += 1
            result = certify_support(block.features, block.symbols, block.box, coefficients,
                                     rows=block.rows,
                                     target=None if block.exact_quadratic else
                                     activity + max(threshold, 0.8 * (sampled_support - activity)),
                                     max_cells=self.config.max_cells,
                                     max_depth=self.config.max_depth)
            self.stats["certification_seconds"] += time.perf_counter() - cert_start
            if (result.cut is not None and math.isfinite(result.cut.rhs)
                    and result.cut.rhs - activity > threshold):
                return result, coefficients, activity
            self.stats["certification_failures"] += 1
            minimizer = result.stats.get("minimizer")
            if (minimizer is None or not self.config.cache_samples or
                    self.stats["callback_seconds"] + time.perf_counter() - round_start >= self.budget or
                    not _exchange_sample(block, minimizer)):
                block.failures += 1
                return None
            self.stats["exchange_samples"] += 1
        return None

    def sepaexeclp(self):
        if self.model.getDepth() != 0 or self.stats["calls"] >= self.config.max_rounds:
            return {"result": ps.SCIP_RESULT.DIDNOTRUN}
        if self.stats["callback_seconds"] >= self.budget or self.stats["cuts"] >= self.config.max_cuts:
            self.stats["budget_exhausted"] = True
            return {"result": ps.SCIP_RESULT.DIDNOTRUN}
        start = time.perf_counter()
        self.stats["calls"] += 1
        added = 0
        try:
            for bi, block in enumerate(self.detected.blocks):
                if (self.stats["callback_seconds"] + time.perf_counter() - start >= self.budget
                        or self.stats["cuts"] >= self.config.max_cuts
                        or added >= self.config.max_cuts_per_round):
                    self.stats["budget_exhausted"] = True
                    break
                if self.mode == "auto" and (not block.auto_eligible or block.failures >= 2):
                    self.stats["selection_skips"] += 1
                    continue
                variables = [self.xs[i] for i in block.variables] + [self.aux[i] for i in block.atoms]
                point = np.asarray([self.model.getSolVal(None, v) for v in variables])
                if not np.isfinite(point).all():
                    continue
                if (self.config.cache_samples and block.previous_point is not None and block.scale is not None and
                        np.max(abs(point - block.previous_point) / block.scale) < 1e-7):
                    self.stats["repeat_skips"] += 1
                    continue
                block.previous_point = point.copy()
                if self.mode == "auto" and self.config.cache_samples:
                    screen_start = time.perf_counter()
                    if block.screening_cache is None:
                        _initialize_screen(block, self.detected)
                    if block.screening_samples is not None:
                        from .screening import screen_convex_combination
                        block.last_screen = screen_convex_combination(
                            point, block.screening_samples, block.screening_weights,
                            scales=block.scale, threshold=self.config.auto_min_violation, norm="1")
                        self.stats["screen_queries"] += 1
                        if block.last_screen.can_skip:
                            self.stats["screen_skips"] += 1
                            self.stats["screening_seconds"] += time.perf_counter() - screen_start
                            continue
                    self.stats["screening_seconds"] += time.perf_counter() - screen_start
                threshold = (self.config.auto_min_violation if self.mode == "auto"
                             else self.config.min_violation)
                supported = self._find_support(block, point, bi, threshold, start)
                if supported is None:
                    continue
                result, coefficients, activity = supported
                rhs = result.cut.rhs
                row_start = time.perf_counter()
                row = self.model.createEmptyRowSepa(self, f"certified_block_{len(self.records)}",
                                                     lhs=rhs, rhs=None, local=False, removable=True)
                self.model.cacheRowExtensions(row)
                for v, c in zip(variables, coefficients):
                    if c:
                        self.model.addVarToRow(row, self.model.getTransformedVar(v), c)
                self.model.flushRowExtensions(row)
                actual_row = _audit_inserted_row(self.model, row, variables, coefficients, rhs)
                if actual_row is None:
                    self.model.releaseRow(row)
                    self.stats["row_binding_rejections"] += 1
                    self.stats["row_seconds"] += time.perf_counter() - row_start
                    continue
                infeasible = self.model.addCut(row, forcecut=True)
                self.model.releaseRow(row)
                self.stats["row_seconds"] += time.perf_counter() - row_start
                self.records.append({"block": bi, "variables": list(block.variables),
                                     "atoms": list(block.atoms), "features": [str(f) for f in block.features],
                                     "symbols": [str(s) for s in block.symbols],
                                     "box": [list(b) for b in block.box],
                                     "rows": [[list(a), rhs] for a, rhs in block.rows],
                                     "column_names": [v.name for v in variables],
                                     "local": False, "actual_row": actual_row,
                                     "atom_trees": [self.detected.atoms[i].tree for i in block.atoms],
                                     "coefficients": list(coefficients), "rhs": rhs,
                                     "activity_at_separation": activity,
                                     "certificate": result.witness,
                                     "certificate_stats": result.stats})
                added += 1
                block.cuts += 1
                self.stats["cuts"] += 1
                if infeasible:
                    return {"result": ps.SCIP_RESULT.CUTOFF}
            return {"result": ps.SCIP_RESULT.SEPARATED if added else ps.SCIP_RESULT.DIDNOTFIND}
        finally:
            self.stats["callback_seconds"] += time.perf_counter() - start


def run_instance(instance_or_path, mode="baseline", time_limit=30.0, seed=0,
                 node_limit=None, config=None, quiet=True):
    """Run one cold model; all in-process setup counts against its wall budget.

    Imports and interpreter startup precede this function. External callers
    should measure process wall time as well when reporting end-to-end costs.
    The solver's time limit is the remainder after read/discovery/model setup;
    callbacks are included in SCIP solve time, not added to it a second time.
    """
    if mode == "reformulation":
        mode = "control"
    if mode not in ("baseline", "control", "all", "auto"):
        raise ValueError("mode must be baseline, control, all, or auto")
    if time_limit <= 0:
        raise ValueError("time_limit must be positive")
    config = Config() if config is None else config
    start = time.perf_counter()
    inst = read_osil(str(instance_or_path)) if isinstance(instance_or_path, (str, Path)) else instance_or_path
    read_seconds = time.perf_counter() - start
    discovery_start = time.perf_counter()
    detected = discover(inst, config) if mode != "baseline" else None
    discovery_seconds = time.perf_counter() - discovery_start
    build_start = time.perf_counter()
    try:
        m, xs, aux = _build(inst, detected, mode)
    except SourceModelMismatch as error:
        return {"name": inst.name, "mode": mode, "sense": inst.obj_sense,
                "status": "source_model_mismatch", "diagnostic": str(error),
                "primal": None, "dual": None, "root_dual": None,
                "original_values": None, "nodes": 0,
                "time_limit": time_limit, "node_limit": node_limit, "seed": seed,
                "read_seconds": read_seconds, "discovery_seconds": discovery_seconds,
                "build_seconds": time.perf_counter() - build_start,
                "solve_wall_seconds": 0.0, "scip_solve_seconds": 0.0,
                "total_seconds": time.perf_counter() - start,
                "remaining_solve_budget": max(0.0, time_limit - (time.perf_counter() - start)),
                "discovery": detected.stats if detected else None,
                "detected_atoms": [], "rewritten_rows": None, "quadratic_atoms": [],
                "separation": None, "cuts": [], "config": asdict(config),
                "scip_version": None, "bound_status": "Source model refused; no solver bound reported"}
    build_seconds = time.perf_counter() - build_start
    if quiet:
        m.hideOutput()
    m.setParam("parallel/maxnthreads", 1)
    m.setParam("randomization/randomseedshift", seed)
    m.setParam("limits/gap", config.gap_limit)
    if node_limit is not None:
        m.setParam("limits/nodes", int(node_limit))
    separator = None
    if mode in ("all", "auto") and detected.blocks:
        separator = BlockSeparator(detected, xs, aux, mode, config,
                                   min(config.max_separation_seconds,
                                       config.separation_budget_fraction * time_limit))
        m.includeSepa(separator, "certified_blocks", "certified small-block global root cuts",
                      priority=100000, freq=0, maxbounddist=1.0, delay=False)
    remaining = max(0.0, time_limit - (time.perf_counter() - start))
    m.setParam("limits/time", remaining)
    solve_start = time.perf_counter()
    m.optimize()
    solve_wall_seconds = time.perf_counter() - solve_start
    primal = float(m.getObjVal()) if m.getNSols() else None
    values = [float(m.getSolVal(m.getBestSol(), v)) for v in xs] if m.getNSols() else None
    dual = float(m.getDualbound())
    root_dual = float(m.getDualboundRoot())
    result = {"name": inst.name, "mode": mode, "sense": inst.obj_sense,
              "status": str(m.getStatus()), "primal": primal,
              "dual": dual if math.isfinite(dual) and abs(dual) < 1e19 else None,
              "root_dual": root_dual if math.isfinite(root_dual) and abs(root_dual) < 1e19 else None,
              "original_values": values, "nodes": int(m.getNNodes()),
              "time_limit": time_limit, "node_limit": node_limit, "seed": seed,
              "read_seconds": read_seconds, "discovery_seconds": discovery_seconds,
              "build_seconds": build_seconds, "solve_wall_seconds": solve_wall_seconds,
              "scip_solve_seconds": float(m.getSolvingTime()),
              "total_seconds": time.perf_counter() - start,
              "remaining_solve_budget": remaining,
              "discovery": detected.stats if detected else None,
              "detected_atoms": [{"index": a.index, "tree": a.tree,
                                  "variables": list(a.variables), "admitted": a.admitted}
                                 for a in detected.atoms] if detected else [],
              "rewritten_rows": detected.rewritten_rows if detected else None,
              "quadratic_atoms": [[ri, qi, ai] for (ri, qi), ai in detected.quadratic_atoms.items()] if detected else [],
              "separation": separator.stats if separator else None,
              "cuts": separator.records if separator else [],
              "config": asdict(config),
              "scip_version": f"{m.getMajorVersion()}.{m.getMinorVersion()}.{m.getTechVersion()}",
              "bound_status": "SCIP numerical bounds; only added rows have exact support certificates"}
    m.freeProb()
    return result
