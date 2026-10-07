"""Native-preserving root cuts obtained by aggregating original row sides.

All modes submit the same model. Discovery is lazy: models solved in presolve
pay no block-discovery cost. Numerical LPs propose directions only. Support
and final-row arithmetic are independently replayable certificates.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import time
import warnings
import xml.etree.ElementTree as ET

import numpy as np
import pyscipopt as ps
from scipy.optimize import linprog, OptimizeWarning
import sympy as sp

from .model import Instance, ModelAdmissionError, build_model, read_osil
from .row_certificate import AffineSide, certify_row_combination

Q = Fraction


class DiscoveryBudgetExhausted(Exception):
    """Incomplete discovery; it provides no statement about supported blocks."""


def _check_discovery_deadline(deadline):
    if deadline is not None and time.perf_counter() >= deadline:
        raise DiscoveryBudgetExhausted


@dataclass(frozen=True)
class Config:
    max_dimensions: int = 4
    max_blocks: int = 32
    max_rows_per_block: int = 6
    max_domain_rows: int = 16
    max_faces: int = 2000
    max_rounds: int = 3
    max_cuts: int = 12
    max_cuts_per_round: int = 4
    max_support_calls: int = 24
    max_exchange_rounds: int = 3
    max_cells: int = 128
    max_depth: int = 16
    max_separation_seconds: float = 1.0
    separation_budget_fraction: float = .05
    min_violation: float = 1e-5
    auto_min_violation: float = 5e-4
    grid_1d: int = 33
    grid_2d: int = 7
    gap_limit: float = 1e-4
    # Campaign 4: exact whole-row support directions first (post hoc v3d variant).
    row_directions: bool = False

    def __post_init__(self):
        integers = ('max_dimensions', 'max_blocks', 'max_rows_per_block',
                    'max_domain_rows', 'max_faces', 'max_rounds', 'max_cuts',
                    'max_cuts_per_round', 'max_support_calls',
                    'max_exchange_rounds', 'max_cells', 'grid_1d', 'grid_2d')
        if any(type(getattr(self, key)) is not int or getattr(self, key) < 1 for key in integers):
            raise ValueError('work limits must be positive integers')
        if type(self.row_directions) is not bool:
            raise ValueError('row_directions must be a bool')
        if self.max_dimensions > 4 or not 0 <= self.max_depth <= 256:
            raise ValueError('dimension cap is four and depth must lie in [0,256]')
        if (not 0 <= self.separation_budget_fraction <= 1 or
                not math.isfinite(self.max_separation_seconds) or self.max_separation_seconds < 0 or
                not all(math.isfinite(x) and x > 0 for x in (self.min_violation, self.auto_min_violation)) or
                not math.isfinite(self.gap_limit) or self.gap_limit < 0):
            raise ValueError('invalid time, gap, or violation limit')


@dataclass(frozen=True)
class Side:
    row_index: int
    sign: int
    side: str
    nonlinear: sp.Expr
    affine: tuple[tuple[str, Q], ...]
    rhs: Q
    variables: tuple[int, ...]

    @property
    def source_id(self):
        return f'row{self.row_index}:{self.side}'

    def record(self):
        return {'row_index': self.row_index, 'sign': self.sign, 'side': self.side,
                'source_id': self.source_id, 'nonlinear': str(self.nonlinear),
                'affine_terms': [[v, str(c)] for v, c in self.affine], 'rhs': str(self.rhs)}


@dataclass
class Block:
    variables: tuple[int, ...]
    sides: tuple[Side, ...]
    symbols: tuple[sp.Symbol, ...]
    box: tuple
    rows: tuple
    domain_records: tuple
    quadratic: bool
    auto_eligible: bool
    sample: np.ndarray | None = None
    sample_points: list = field(default_factory=list)
    scale: np.ndarray | None = None
    previous_point: tuple | None = None
    failures: int = 0

    @property
    def features(self):
        return self.symbols + tuple(side.nonlinear for side in self.sides)


@dataclass
class Detected:
    blocks: list[Block]
    stats: dict


def split_affine(expression, symbols, *, deadline=None):
    """Split exact additive affine terms; do not expand powers multinomially."""
    _check_discovery_deadline(deadline)
    if not symbols:
        return (sp.S.Zero, (), Q(expression)) if expression.is_Rational else (expression, (), Q(0))
    expanded = sp.expand(expression, mul=True, multinomial=False,
                         power_base=False, power_exp=False)
    affine = {str(s): Q(0) for s in symbols}
    symbol_order = {s: i for i, s in enumerate(symbols)}
    constant, nonlinear = Q(0), []
    for term in sp.Add.make_args(expanded):
        _check_discovery_deadline(deadline)
        if term.is_Rational:
            constant += Q(term)
            continue
        # Dense polynomial storage recurses once per generator, even when
        # almost all global model coordinates are absent from this term.
        # Restricting generators preserves the exact affine decomposition.
        used_symbols = tuple(sorted(term.free_symbols, key=symbol_order.__getitem__))
        if not used_symbols:
            nonlinear.append(term)
            continue
        try:
            polynomial = sp.Poly(term, *used_symbols, domain=sp.QQ)
        except (sp.PolynomialError, sp.polys.polyerrors.CoercionFailed, ValueError, TypeError, RecursionError):
            nonlinear.append(term)
            continue
        if polynomial.total_degree() > 1:
            nonlinear.append(term)
            continue
        constant += Q(polynomial.coeff_monomial(1))
        for symbol in used_symbols:
            affine[str(symbol)] += Q(polynomial.coeff_monomial(symbol))
    return sp.Add(*nonlinear), tuple((v, c) for v, c in affine.items() if c), constant


def signed_sides(inst, built, *, deadline=None):
    sides = []
    indices = {symbol: i for i, symbol in enumerate(built.source_symbols)}
    for ri, expression in enumerate(built.source_rows):
        _check_discovery_deadline(deadline)
        nonlinear, affine, constant = split_affine(expression, built.source_symbols, deadline=deadline)
        if ri == 0:
            if built.objective_var is None:
                continue
            sign = 1 if inst.obj_sense == 'min' else -1
            variants = [(sign, 'objective', Q(0))]
        else:
            row = inst.rows[ri]
            variants = []
            if math.isfinite(row['ub']): variants.append((1, 'upper', Q(row['ub'])))
            if math.isfinite(row['lb']): variants.append((-1, 'lower', -Q(row['lb'])))
        for sign, side, bound in variants:
            linear = [(v, sign*c) for v, c in affine]
            if ri == 0:
                linear.append((built.objective_var.name, Q(-sign)))
            sides.append(Side(ri, sign, side, sign*nonlinear, tuple(linear),
                              bound-sign*constant,
                              tuple(sorted(indices[s] for s in nonlinear.free_symbols))))
    return sides


def discover(inst, built, config=Config(), *, deadline=None):
    """Group original nonlinear rows, retaining original-row affine domains."""
    _check_discovery_deadline(deadline)
    sides = signed_sides(inst, built, deadline=deadline)
    stats = {'nonlinear_sides': 0, 'unsupported_sides': 0, 'blocks': 0,
             'auto_eligible': 0, 'block_cap_reached': False}
    admissible = []
    for side in sides:
        _check_discovery_deadline(deadline)
        if side.nonlinear == 0:
            continue
        stats['nonlinear_sides'] += 1
        if (not side.variables or len(side.variables) > config.max_dimensions or
                not all(math.isfinite(v) for i in side.variables for v in built.bounds[i])):
            stats['unsupported_sides'] += 1
            continue
        symbols = tuple(built.source_symbols[i] for i in side.variables)
        polynomial = side.nonlinear.is_polynomial(*symbols)
        if not polynomial and len(symbols) != 1:
            stats['unsupported_sides'] += 1
            continue
        if polynomial and sp.Poly(side.nonlinear, *symbols).total_degree() > 8:
            stats['unsupported_sides'] += 1
            continue
        admissible.append(side)
    # Each row is covered individually. Extra groups join existing overlaps;
    # unrelated pairs are never enumerated. Larger unions precede subblocks.
    groups = {tuple(side.variables) for side in admissible}
    for side in admissible:
        _check_discovery_deadline(deadline)
        union = set(side.variables)
        for other in admissible:
            _check_discovery_deadline(deadline)
            combined = union.union(other.variables)
            if union.intersection(other.variables) and len(combined) <= config.max_dimensions:
                union = combined
        groups.add(tuple(sorted(union)))
    blocks = []
    affine_sides = [s for s in sides if s.nonlinear == 0]
    for variables in sorted(groups, key=lambda v: (-len(v), v)):
        _check_discovery_deadline(deadline)
        chosen_list = []
        for side in admissible:
            _check_discovery_deadline(deadline)
            if set(side.variables).issubset(variables):
                chosen_list.append(side)
                if len(chosen_list) >= config.max_rows_per_block:
                    break
        chosen = tuple(chosen_list)
        if not chosen:
            continue
        syms = tuple(built.source_symbols[i] for i in variables)
        names = tuple(str(s) for s in syms)
        rows, records = [], []
        for side in affine_sides:
            _check_discovery_deadline(deadline)
            if not side.affine or not {v for v, c in side.affine}.issubset(names):
                continue
            coefficients = tuple(dict(side.affine).get(name, Q(0)) for name in names)
            rows.append((coefficients, side.rhs))
            records.append({'row_index': side.row_index, 'sign': side.sign,
                            'coefficients': [str(c) for c in coefficients], 'rhs': str(side.rhs)})
            if len(rows) >= config.max_domain_rows:
                break
        quadratic = True
        for side in chosen:
            _check_discovery_deadline(deadline)
            if not side.nonlinear.is_polynomial(*syms) or sp.Poly(side.nonlinear, *syms).total_degree() > 2:
                quadratic = False
                break
        nonconvex = False
        if quadratic:
            for side in chosen:
                _check_discovery_deadline(deadline)
                if sp.hessian(side.nonlinear, syms).is_positive_semidefinite is not True:
                    nonconvex = True
                    break
        coupling = any(sum(c != 0 for c in a) > 1 for a, rhs in rows)
        auto = bool(nonconvex and (coupling or len({s.row_index for s in chosen}) >= 2))
        blocks.append(Block(variables, chosen, syms, tuple(built.bounds[i] for i in variables),
                            tuple(rows), tuple(records), quadratic, auto))
        if len(blocks) >= config.max_blocks:
            stats['block_cap_reached'] = len(groups) > len(blocks)
            break
    stats.update(blocks=len(blocks), auto_eligible=sum(b.auto_eligible for b in blocks))
    return Detected(blocks, stats)


def _evaluate(block, points):
    fs = [sp.lambdify(block.symbols, feature, 'numpy') for feature in block.features]
    with np.errstate(all='ignore'):
        values = np.column_stack([np.broadcast_to(f(*points.T), (len(points),)) for f in fs])
    if not np.isfinite(values).all():
        raise ValueError('nonfinite heuristic samples')
    return values


def _sample(block, config):
    if block.sample is not None:
        return
    dimension = len(block.variables)
    count = config.grid_1d if dimension == 1 else config.grid_2d if dimension == 2 else 3
    points = np.asarray(list(itertools.product(*(np.linspace(lo, hi, count) for lo, hi in block.box))))
    # Floating filtering only shapes a proposal; it is not a feasibility proof.
    if block.rows:
        mask = np.ones(len(points), dtype=bool)
        for a, rhs in block.rows:
            aa = np.asarray(a, dtype=float)
            mask &= points @ aa <= float(rhs) + 1e-12*max(1., abs(float(rhs)))
        points = points[mask]
    exact = []
    if block.quadratic:
        from theory.quadratic_polytope import polytope_vertices
        count_faces = sum(math.comb(len(block.rows)+2*dimension, k) for k in range(dimension+1))
        if count_faces <= config.max_faces:
            exact = polytope_vertices(block.box, tuple((*a, b) for a, b in block.rows))
    if exact:
        vertices = [tuple(Q(v) for v in point) for point in exact]
        centroid = tuple(sum(p[j] for p in vertices)/len(vertices) for j in range(dimension))
        exact = vertices + [centroid]
        points = np.vstack((points.reshape((-1, dimension)), np.asarray(exact, dtype=float)))
    if not len(points):
        raise ValueError('no finite domain samples')
    block.sample_points = [tuple(Q(float(v)) for v in p) for p in points]
    block.sample = _evaluate(block, points)
    span = np.ptp(block.sample, axis=0)
    block.scale = np.maximum(span, np.maximum(1., np.max(abs(block.sample), axis=0))*1e-8)


def propose_direction(block, point, config=Config()):
    """Sample LP with nonnegative multipliers for all signed source rows."""
    _sample(block, config)
    point = np.asarray(point, float)
    scaled_samples = block.sample/block.scale
    scaled_point = point/block.scale
    d = len(block.variables)
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', message='Unrecognized options detected.*', category=OptimizeWarning)
        result = linprog(np.r_[-1., scaled_point],
                         A_ub=np.column_stack((np.ones(len(block.sample)), -scaled_samples)),
                         b_ub=np.zeros(len(block.sample)),
                         bounds=[(None,None)]+[(-1.,1.)]*d+[(0.,1.)]*len(block.sides),
                         method='highs', options={'time_limit': .05, 'threads': 1, 'parallel': False})
    if not result.success or result.fun >= -config.min_violation:
        return None
    coefficients = np.asarray(result.x[1:]/block.scale, float)
    if not np.isfinite(coefficients).all():
        return None
    coefficients[d:] = np.maximum(0., coefficients[d:])
    return tuple(float(c) for c in coefficients)


def _audit_inserted_row(model, row, variables, coefficients, rhs):
    """Reject substitutions not proved by this original-coordinate certificate."""
    actual = {column.getVar().name: Q(float(c))
              for column, c in zip(row.getCols(), row.getVals()) if c}
    expected, mapping = {}, []
    for variable, coefficient in zip(variables, coefficients):
        if not coefficient:
            continue
        transformed = model.getTransformedVar(variable)
        name, value = transformed.name, Q(float(coefficient))
        # No aggregation identity is part of this certificate. Distinct
        # source variables must not silently alias one transformed column.
        if name in expected:
            return None
        expected[name] = expected.get(name, Q(0))+value
        mapping.append({'source': variable.name, 'transformed': name})
    expected = {name:value for name,value in expected.items() if value}
    lhs, upper, constant = float(row.getLhs()), float(row.getRhs()), float(row.getConstant())
    if (actual != expected or not math.isfinite(lhs) or abs(lhs) >= model.infinity() or
            not math.isfinite(constant) or
            Q(lhs)-Q(constant) != Q(float(rhs)) or not upper >= model.infinity() or row.isLocal()):
        return None
    return {'local': False, 'columns': {name:float(c) for name,c in actual.items()},
            'lhs': lhs, 'rhs': upper, 'constant': constant, 'scip_infinity': model.infinity(),
            'source_to_transformed': mapping}


class RowSeparator(ps.Sepa):
    def __init__(self, inst, built, mode, config, budget):
        self.inst, self.built, self.mode, self.config, self.budget = inst, built, mode, config, budget
        self.detected = None
        self.discovery_stopped = False
        self.records, self.seen = [], set()
        self.names = tuple(str(s) for s in built.source_symbols)
        self.variables = list(built.xs)
        self.bounds = dict(zip(self.names, built.bounds))
        if built.objective_var is not None:
            self.names += (built.objective_var.name,)
            self.variables.append(built.objective_var)
            self.bounds[built.objective_var.name] = (-math.inf, math.inf)
        self.stats = {'calls':0, 'cuts':0, 'candidate_lps':0, 'certification_calls':0,
                      'certification_failures':0, 'sampling_failures':0, 'selection_skips':0,
                      'row_binding_rejections':0, 'row_rounding_rejections':0, 'repeat_skips':0,
                      'exchange_samples':0, 'callback_seconds':0., 'discovery_seconds':0.,
                      'discovery_incomplete':False,
                      'candidate_seconds':0., 'certification_seconds':0., 'row_seconds':0.,
                      'budget_exhausted':False}

    def _expired(self, started):
        exhausted = (self.stats['callback_seconds']+time.perf_counter()-started >= self.budget or
                     self.stats['certification_calls'] >= self.config.max_support_calls or
                     self.stats['cuts'] >= self.config.max_cuts)
        self.stats['budget_exhausted'] |= exhausted
        return exhausted

    def _query(self, block, values):
        mapping = dict(zip(self.names, values))
        return tuple(values[i] for i in block.variables)+tuple(
            float(side.rhs)-sum(float(c)*mapping[v] for v,c in side.affine) for side in block.sides)

    def _directions(self, block, query, started):
        d = len(block.variables)
        # Unmixed original rows include exact objective support as a first
        # inexpensive direction. No sample LP is needed for these directions.
        for j in range(len(block.sides)):
            if self._expired(started): return
            if self.config.row_directions:
                # Campaign 4 (post hoc variant of v3d): first the exact support of
                # the whole source row, including its affine terms in the block
                # variables; then the support of the nonlinear remainder alone.
                names = [self.names[i] for i in block.variables]
                affine = dict(block.sides[j].affine)
                direction = [float(affine.get(name, 0)) for name in names]+[0.]*len(block.sides)
                direction[d+j] = 1.
                if any(direction[:d]):
                    yield tuple(direction)
            direction = [0.]*(d+len(block.sides))
            direction[d+j] = 1.
            yield tuple(direction)
        for _ in range(self.config.max_exchange_rounds):
            if self._expired(started): return
            proposal_start = time.perf_counter()
            try:
                self.stats['candidate_lps'] += 1
                direction = propose_direction(block, query, self.config)
            except (ValueError, TypeError, ArithmeticError, NotImplementedError):
                self.stats['sampling_failures'] += 1
                return
            finally:
                self.stats['candidate_seconds'] += time.perf_counter()-proposal_start
            if direction is None: return
            yield direction

    def sepaexeclp(self):
        if self.discovery_stopped or self.model.getDepth() != 0 or self.stats['calls'] >= self.config.max_rounds:
            return {'result':ps.SCIP_RESULT.DIDNOTRUN}
        started = time.perf_counter()
        if self._expired(started):
            return {'result':ps.SCIP_RESULT.DIDNOTRUN}
        self.stats['calls'] += 1
        added = 0
        try:
            if self.detected is None:
                discovery_start = time.perf_counter()
                try:
                    self.detected = discover(self.inst, self.built, self.config,
                        deadline=started+self.budget-self.stats['callback_seconds'])
                except DiscoveryBudgetExhausted:
                    self.discovery_stopped = True
                    self.stats['discovery_incomplete'] = True
                    self.stats['budget_exhausted'] = True
                    return {'result':ps.SCIP_RESULT.DIDNOTFIND}
                finally:
                    self.stats['discovery_seconds'] += time.perf_counter()-discovery_start
            values = tuple(float(self.model.getSolVal(None, v)) for v in self.variables)
            if not all(math.isfinite(v) for v in values):
                return {'result':ps.SCIP_RESULT.DIDNOTFIND}
            from .support import certify_support
            for bi, block in enumerate(self.detected.blocks):
                if self._expired(started) or added >= self.config.max_cuts_per_round:
                    break
                if self.mode == 'auto' and (not block.auto_eligible or block.failures >= 2):
                    self.stats['selection_skips'] += 1
                    continue
                query = self._query(block, values)
                if query == block.previous_point:
                    self.stats['repeat_skips'] += 1
                    continue
                block.previous_point = query
                threshold = self.config.auto_min_violation if self.mode == 'auto' else self.config.min_violation
                for coefficients in self._directions(block, query, started):
                    if self._expired(started) or added >= self.config.max_cuts_per_round: break
                    key = (bi, coefficients)
                    if key in self.seen: continue
                    self.seen.add(key)
                    certification_start = time.perf_counter()
                    self.stats['certification_calls'] += 1
                    activity = float(np.dot(coefficients, query))
                    result = certify_support(block.features, block.symbols, block.box, coefficients,
                                             rows=block.rows, target=None if block.quadratic else activity+threshold,
                                             max_cells=self.config.max_cells, max_depth=self.config.max_depth,
                                             max_polytope_faces=self.config.max_faces)
                    self.stats['certification_seconds'] += time.perf_counter()-certification_start
                    minimizer = result.stats.get('minimizer')
                    if minimizer is not None and block.sample is not None:
                        point = tuple(Q(v) for v in minimizer)
                        if point not in block.sample_points:
                            try:
                                sample = _evaluate(block, np.asarray([point], dtype=float))
                                block.sample = np.vstack((block.sample, sample))
                                block.sample_points.append(point)
                                self.stats['exchange_samples'] += 1
                            except (ValueError, TypeError, ArithmeticError):
                                # A heuristic evaluation failure does not affect
                                # a support certificate already obtained.
                                self.stats['sampling_failures'] += 1
                    if result.cut is None:
                        self.stats['certification_failures'] += 1
                        block.failures += 1
                        continue
                    try:
                        digest = hashlib.sha256(json.dumps(result.witness, sort_keys=True,
                                                           separators=(',',':'), allow_nan=False).encode()).hexdigest()
                        converted = certify_row_combination(variables=self.names, bounds=self.bounds,
                            linear_terms=dict(zip((str(s) for s in block.symbols), coefficients[:len(block.variables)])),
                            multipliers=coefficients[len(block.variables):], support_rhs=result.cut.rhs,
                            sides=[AffineSide(s.source_id, s.affine, s.rhs) for s in block.sides],
                            support_id=digest)
                    except (ValueError, OverflowError):
                        self.stats['row_rounding_rejections'] += 1
                        continue
                    if abs(converted.rhs) >= self.model.infinity():
                        self.stats['row_rounding_rejections'] += 1
                        continue
                    final_activity = sum(c*v for c,v in zip(converted.coefficients, values))
                    violation = converted.rhs-final_activity
                    normalization = max(1., sum(abs(c) for c in converted.coefficients))
                    if not math.isfinite(violation) or violation <= threshold*normalization:
                        continue
                    row_start = time.perf_counter()
                    row = self.model.createEmptyRowSepa(self, f'certified_row_aggregate_{len(self.records)}',
                              lhs=converted.rhs, rhs=None, local=False, removable=True)
                    self.model.cacheRowExtensions(row)
                    for variable, coefficient in zip(self.variables, converted.coefficients):
                        if coefficient:
                            self.model.addVarToRow(row, self.model.getTransformedVar(variable), coefficient)
                    self.model.flushRowExtensions(row)
                    actual = _audit_inserted_row(self.model, row, self.variables,
                                                 converted.coefficients, converted.rhs)
                    if actual is None:
                        self.model.releaseRow(row)
                        self.stats['row_binding_rejections'] += 1
                        self.stats['row_seconds'] += time.perf_counter()-row_start
                        continue
                    infeasible = self.model.addCut(row, forcecut=True)
                    self.model.releaseRow(row)
                    self.stats['row_seconds'] += time.perf_counter()-row_start
                    self.records.append({'block':bi, 'variables':list(block.variables),
                        'symbols':[str(s) for s in block.symbols], 'features':[str(f) for f in block.features],
                        'signed_sides':[s.record() for s in block.sides],
                        'box':[[str(Q(lo)),str(Q(hi))] for lo,hi in block.box],
                        'domain_rows':list(block.domain_records), 'coefficients':list(coefficients),
                        'support_witness':result.witness, 'support_stats':result.stats,
                        'row_certificate':converted.to_dict(), 'actual_row':actual,
                        'activity_at_separation':final_activity, 'rhs':converted.rhs,
                        'column_names':[v.name for v in self.variables], 'local':False})
                    self.stats['cuts'] += 1
                    added += 1
                    if infeasible:
                        return {'result':ps.SCIP_RESULT.CUTOFF}
            return {'result':ps.SCIP_RESULT.SEPARATED if added else ps.SCIP_RESULT.DIDNOTFIND}
        finally:
            self.stats['callback_seconds'] += time.perf_counter()-started


RUN_INSTANCE_PARAMS = ('parallel/maxnthreads', 'randomization/randomseedshift', 'limits/gap',
                       'limits/nodes', 'limits/time')


def run_instance(instance_or_path, mode='baseline', time_limit=30., seed=0,
                 node_limit=None, config=None, quiet=True, scip_params=None):
    """Run one model; setup and lazy discovery count against total time budget.

    scip_params (campaign 4): SCIP parameters set on the model before solving,
    in every mode alike; recorded in the result.
    """
    if mode == 'control': mode = 'baseline'
    if mode not in ('baseline','all','auto'):
        raise ValueError('mode must be baseline, all, or auto')
    if not math.isfinite(time_limit) or time_limit <= 0:
        raise ValueError('time_limit must be finite and positive')
    config = config or Config()
    scip_params = dict(scip_params or {})
    if any(not isinstance(key, str) or key in RUN_INSTANCE_PARAMS for key in scip_params):
        raise ValueError('scip_params must have string names not set by run_instance itself')
    started = time.perf_counter()
    try:
        inst = read_osil(str(instance_or_path)) if isinstance(instance_or_path,(str,Path)) else instance_or_path
    except (OSError, ET.ParseError, ValueError, TypeError, KeyError, IndexError, NotImplementedError, RecursionError) as error:
        return {'name':Path(instance_or_path).stem,'mode':mode,'sense':None,
                'status':'unsupported_input','diagnostic':str(error),
                'primal':None,'dual':None,'root_dual':None,'original_values':None,
                'nodes':0,'time_limit':time_limit,'node_limit':node_limit,'seed':seed,
                'read_seconds':time.perf_counter()-started,'build_seconds':0.,'discovery_seconds':0.,
                'solve_wall_seconds':0.,'scip_solve_seconds':0.,'total_seconds':time.perf_counter()-started,
                'remaining_solve_budget':0.,'discovery':None,'coverage':None,'separation':None,
                'cuts':[],'model_metadata':None,'config':asdict(config),'scip_params':scip_params,'scip_version':None,
                'bound_status':'Input not admitted; no solver bound reported'}
    read_seconds = time.perf_counter()-started
    build_start = time.perf_counter()
    try:
        built = build_model(inst)
    except ModelAdmissionError as error:
        return {'name':inst.name,'mode':mode,'sense':inst.obj_sense,'status':error.status,
                'diagnostic':str(error),'primal':None,'dual':None,'root_dual':None,
                'original_values':None,'nodes':0,'time_limit':time_limit,'node_limit':node_limit,'seed':seed,
                'read_seconds':read_seconds,'build_seconds':time.perf_counter()-build_start,
                'discovery_seconds':0.,'solve_wall_seconds':0.,'scip_solve_seconds':0.,
                'total_seconds':time.perf_counter()-started,'remaining_solve_budget':0.,
                'discovery':None,'coverage':None,'separation':None,'cuts':[],
                'model_metadata':None,'config':asdict(config),'scip_params':scip_params,'scip_version':None,
                'bound_status':'Model not admitted; no solver bound reported'}
    build_seconds = time.perf_counter()-build_start
    model = built.model
    try:
        if quiet: model.hideOutput()
        model.setParam('parallel/maxnthreads',1)
        model.setParam('randomization/randomseedshift',seed)
        model.setParam('limits/gap',config.gap_limit)
        if node_limit is not None: model.setParam('limits/nodes',int(node_limit))
        for key, value in scip_params.items():
            model.setParam(key, value)
        separator = None
        if mode != 'baseline':
            separator = RowSeparator(inst,built,mode,config,min(config.max_separation_seconds,
                                                     config.separation_budget_fraction*time_limit))
            model.includeSepa(separator,'certified_row_aggregation',
                              'certified native-preserving original-row aggregate cuts',
                              priority=100000,freq=0,maxbounddist=1.,delay=False)
        remaining = max(0.,time_limit-(time.perf_counter()-started))
        model.setParam('limits/time',remaining)
        solve_start = time.perf_counter()
        model.optimize()
        solve_wall = time.perf_counter()-solve_start
        primal = float(model.getObjVal()) if model.getNSols() else None
        values = [float(model.getSolVal(model.getBestSol(),v)) for v in built.xs] if model.getNSols() else None
        def finite_bound(value):
            value = float(value)
            return value if math.isfinite(value) and abs(value)<1e19 else None
        detected = separator.detected if separator else None
        return {'name':inst.name,'mode':mode,'sense':inst.obj_sense,'status':str(model.getStatus()),
                'primal':primal,'dual':finite_bound(model.getDualbound()),
                'root_dual':finite_bound(model.getDualboundRoot()),'original_values':values,
                'nodes':int(model.getNNodes()),'time_limit':time_limit,'node_limit':node_limit,'seed':seed,
                'read_seconds':read_seconds,'build_seconds':build_seconds,
                'discovery_seconds':separator.stats['discovery_seconds'] if separator else 0.,
                'solve_wall_seconds':solve_wall,'scip_solve_seconds':float(model.getSolvingTime()),
                'total_seconds':time.perf_counter()-started,'remaining_solve_budget':remaining,
                'discovery':detected.stats if detected else None,'coverage':detected.stats if detected else None,
                'separation':separator.stats if separator else None,'cuts':separator.records if separator else [],
                'model_metadata':built.metadata,'config':asdict(config),'scip_params':scip_params,
                'scip_version':f'{model.getMajorVersion()}.{model.getMinorVersion()}.{model.getTechVersion()}',
                'bound_status':'SCIP numerical bounds; only added rows have exact support/rounding certificates'}
    finally:
        model.freeProb()
