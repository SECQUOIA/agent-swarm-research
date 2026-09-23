"""Paper Stage 6: strong baselines, five rotated repetitions, exact audits.

Run from the repository root with PYTHONPATH=code:
python -m network_simplex_benchmarks.paper_stage06 --output PATH
Use --quick only for a smoke run; publication tables require the default grid.
"""
from fractions import Fraction as F
import argparse
import importlib.util
import json
import os
from pathlib import Path
import platform
from statistics import median
import sys
from time import perf_counter

import numpy as np
import scipy
from scipy.optimize import OptimizeResult

from .baselines import Instance, OriginalLP, block_chain
from .strong_baselines import optimize_ef, optimize_independent_states, membership_ef
from network_simplex import Point, NetworkSimplex
from network_simplex.flat_chain import FlatChainSimplex, reduced_library, _reduced_bases
from network_simplex_compressed import CompressedNetworkSimplex

# Reuse the unchanged historical instance generator and exact audit adapters.
# Its script-style imports expect the benchmark directory on sys.path.
sys.path.insert(0, str(Path(__file__).parent))
from .run import membership_data, point as rational_point, check_decomposition, cut_terms

ROOT = Path(__file__).resolve().parents[2]


def timed(function):
    start = perf_counter(); result = function()
    return result, perf_counter()-start


def historical_flat():
    path = ROOT/'paper-network-simplex/verification/reference/stage06/flat_chain.py'
    name = 'network_simplex._stage06_unreduced'
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def flat_instance(length, feasible, interior):
    arcs = [(i, i+1, 1.) for i in range(length) for _ in range(2)]+[(0, length, 1.)]
    balances = np.zeros(length+1); balances[0] = 1.; balances[-1] = -1.
    obs = [(2*i, i % 2) for i in range(length)]
    y = [F(1, 3) if interior else F(1, 2)]*2
    if feasible:
        x = [F(1, 4)]*(2*length)+[F(1, 2)]
        z = {key: (F(1, 12)+F(i % 3-1, 48) if interior else
                   F(1, 8)+(-1 if i % 2 else 1)*F(i % 3-1, 16))
             for i, key in enumerate(obs)}
    else:
        x = [F(3, 10), F(1, 5)]*length+[F(1, 2)]
        z = {key: F(3, 10) for key in obs}
    p = Point(x, y, z)
    assert all(max(0, p.x[e]+p.y[j]-1) <= v <= min(p.x[e], p.y[j]) for (e, j), v in z.items())
    return Instance(arcs, balances, 2, obs, np.asarray(x, float)), p


def global_flat_cut(instance, cut):
    length, m = (instance.edge_count-1)//2, instance.simplex_size
    maximum = None
    for state in range(m+1):
        coefficients = [F(0)]*instance.edge_count
        constant = cut.constant
        for key, value in cut.coefficients.items():
            if key[0] == 'x': coefficients[key[1]] += value
            elif key[0] == 'y' and key[1] == state: constant += value
            elif key[0] == 'z' and key[2] == state: coefficients[key[1]] += value
        value = constant+max(coefficients[-1], sum(max(coefficients[2*i], coefficients[2*i+1]) for i in range(length)))
        maximum = value if maximum is None else max(maximum, value)
    assert maximum <= 0
    return str(maximum)


def lp_record(result, total, setup=0.):
    if result.status not in (0, 2):
        raise RuntimeError(f'LP status {result.status}: {result.message}')
    return dict(status=int(result.status), build_seconds=setup+result.assembly_seconds,
                solve_seconds=result.solve_seconds, total_seconds=setup+total,
                symbolic_seconds=setup, matrix_seconds=result.assembly_seconds,
                stats=result.model_stats,
                **({'objective':float(result.fun)} if result.success and getattr(result, 'fun', None) is not None else {}))


def membership(method, instance, p, old=None):
    if method in ('full', 'global', 'two_state'):
        result, total = timed(lambda: membership_ef(instance, p.x, p.y, [p.z[o] for o in instance.observations],
                                                   merge=method == 'global', two_state=method == 'two_state'))
        return lp_record(result, total), result
    if method in ('initial', 'eliminated'):
        model, setup = timed(lambda: CompressedNetworkSimplex(instance.arcs, -instance.balances,
                             instance.simplex_size, instance.observations, eliminate_observed=method == 'eliminated'))
        result, total = timed(lambda: model.membership(p))
        return lp_record(result, total, setup), result
    constructor = old.FlatChainSimplex if method == 'unreduced' else FlatChainSimplex if method == 'flat' else NetworkSimplex
    if method in ('flat', 'unreduced'):
        model, setup = timed(lambda: constructor((instance.edge_count-1)//2, instance.simplex_size, instance.observations))
    else:
        model, setup = timed(lambda: constructor(instance.arcs, -instance.balances, instance.simplex_size, instance.observations))
    result, online = timed(lambda: model.separate(p, decompose=False))
    record = dict(status=0 if result.feasible else 2, build_seconds=setup,
                  solve_seconds=online, total_seconds=setup+online)
    if result.feasible:
        recovered, recovery = timed(lambda: model.separate(p, decompose=True))
        assert recovered.feasible
        record.update(with_recovery_seconds=recovery, total_with_recovery_seconds=setup+recovery)
        return record, recovered
    record['cut_reason'] = result.cut.reason
    return record, result


def audit_membership(instance, p, result, flat):
    start = perf_counter()
    if result.feasible:
        check_decomposition(instance, p, result.decomposition)
        audit = dict(exact_decomposition=True, positive_global_states=sum(w > 0 for w in result.decomposition.weights))
    else:
        assert result.cut.evaluate(p) > 0
        assert flat
        audit = dict(exact_cut_violation=str(result.cut.evaluate(p)),
                     exact_global_path_cut_maximum=global_flat_cut(instance, result.cut),
                     cut={'constant':str(result.cut.constant),
                          'terms':[[list(k), str(v)] for k, v in sorted(result.cut.coefficients.items())]})
    audit['outside_timing_seconds'] = perf_counter()-start
    return audit


def summarize(runs):
    methods = runs[0]['measurements']
    out = {}
    for method in methods:
        out[method] = {}
        for key in runs[0]['measurements'][method]:
            if key.endswith('_seconds'):
                values = [run['measurements'][method][key] for run in runs]
                out[method][key] = {'minimum':min(values), 'median':median(values), 'maximum':max(values)}
    return out


def member_case(instance, p, expected, methods, repetitions, old=None):
    warmup, audits = {}, {}
    for method in methods:
        record, result = membership(method, instance, p, old)
        assert record['status'] == (0 if expected else 2), (method, record)
        warmup[method] = record
        if method in ('flat', 'unreduced', 'separator'):
            audits[method] = audit_membership(instance, p, result, method != 'separator')
    runs = []
    for repeat in range(repetitions):
        shift = repeat % len(methods)
        order = methods[shift:]+methods[:shift]
        measurements = {}
        for method in order:
            measurements[method], _ = membership(method, instance, p, old)
            assert measurements[method]['status'] == (0 if expected else 2)
        runs.append(dict(order=order, measurements=measurements))
    return dict(edges=instance.edge_count, states=instance.simplex_size,
                observed_labels=len({j for _, j in instance.observations}), observations=len(instance.observations),
                feasible=expected, warmup=warmup, audits=audits, runs=runs, summary=summarize(runs))


def add_original_rows(model, rows):
    for coefficients, rhs in rows:
        model.ub.append(({i:F(str(v)) for i, v in enumerate(coefficients) if v}, F(rhs)))


def cutting_plane(instance, objective, y, extra_rows):
    started = perf_counter()
    model = NetworkSimplex(instance.arcs, -instance.balances, instance.simplex_size, instance.observations)
    relaxation = OriginalLP(instance, y_fixed=y)
    for coefficients, rhs in extra_rows:
        relaxation.add_cut([(i, float(v)) for i, v in enumerate(coefficients) if v], float(rhs))
    construction = perf_counter()-started
    solver = matrix = separator = reconstruction = 0.
    cuts = []
    first_objective = None
    for iteration in range(1001):
        answer = relaxation.solve(objective)
        assert answer.status == 0
        solver += answer.solve_seconds; matrix += answer.assembly_seconds
        if first_objective is None: first_objective = float(answer.fun)
        p, elapsed = timed(lambda: rational_point(instance, answer.x)); reconstruction += elapsed
        separated, elapsed = timed(lambda: model.separate(p)); separator += elapsed
        if separated.feasible:
            record = dict(status=0, objective=float(answer.fun), mccormick_objective=first_objective,
                          cuts=len(cuts), build_seconds=construction+matrix, solve_seconds=solver,
                          separator_seconds=separator, reconstruction_seconds=reconstruction,
                          total_seconds=perf_counter()-started, stats=answer.model_stats)
            return record, (p, separated, cuts)
        cuts.append(separated.cut)
        relaxation.add_cut(cut_terms(instance, separated.cut), -float(separated.cut.constant))
    raise AssertionError('Cutting-plane iteration cap reached')


def optimize(method, instance, objective, y, extra_rows):
    if method in ('full', 'global'):
        result, total = timed(lambda: optimize_ef(instance, objective, y_fixed=y, merge=method == 'global', extra_rows=extra_rows))
        return lp_record(result, total), result
    if method == 'network_states':
        assert not extra_rows
        result, total = timed(lambda: optimize_independent_states(instance, objective, y))
        return lp_record(result, total), result
    if method == 'cuts':
        return cutting_plane(instance, objective, y, extra_rows)
    model, setup = timed(lambda: CompressedNetworkSimplex(instance.arcs, -instance.balances, instance.simplex_size,
                         instance.observations, eliminate_observed=method == 'eliminated'))
    _, extra_time = timed(lambda: add_original_rows(model, extra_rows)); setup += extra_time
    result, total = timed(lambda: model.optimize(objective, y_fixed=y))
    return lp_record(result, total, setup), result


def opt_case(instance, objective, y, extra_rows, methods, repetitions):
    warmup, audits, optimum = {}, {}, None
    for method in methods:
        record, result = optimize(method, instance, objective, y, extra_rows)
        assert record['status'] == 0
        if optimum is None: optimum = record['objective']
        assert abs(record['objective']-optimum) < 1e-7, (method, record['objective'], optimum)
        warmup[method] = record
        audit_start = perf_counter()
        if method == 'cuts':
            p, separated, cuts = result
            check_decomposition(instance, p, separated.decomposition)
            for cut in cuts:
                cost = np.zeros(len(objective))
                for i, value in cut_terms(instance, cut): cost[i] = value
                support = optimize_ef(instance, -cost, merge=True)
                assert support.status == 0 and -support.fun+float(cut.constant) <= 1e-7
            audits[method] = dict(exact_final_decomposition=True, numerical_global_cut_support_audits=len(cuts))
        else:
            p = rational_point(instance, result.original_point)
            separated = NetworkSimplex(instance.arcs, -instance.balances, instance.simplex_size, instance.observations).separate(p)
            assert separated.feasible
            check_decomposition(instance, p, separated.decomposition)
            audits[method] = dict(exact_reconstructed_component_decomposition=True)
        for coefficients, rhs in extra_rows:
            vector = p.x+p.y+tuple(p.z[o] for o in instance.observations)
            assert sum(F(str(c))*v for c, v in zip(coefficients, vector)) <= F(rhs)
        audits[method]['outside_timing_seconds'] = perf_counter()-audit_start
    runs = []
    for repeat in range(repetitions):
        shift = repeat % len(methods); order = methods[shift:]+methods[:shift]
        measurements = {}
        for method in order:
            measurements[method], _ = optimize(method, instance, objective, y, extra_rows)
            assert measurements[method]['status'] == 0
            assert abs(measurements[method]['objective']-optimum) < 1e-7
        runs.append(dict(order=order, measurements=measurements))
    return dict(edges=instance.edge_count, states=instance.simplex_size, observations=len(instance.observations),
                observed_labels=len({j for _, j in instance.observations}), objective=optimum,
                y=[str(v) for v in y], objective_vector=list(map(float, objective)),
                extra_rows=[{'coefficients':list(map(float, c)), 'rhs':str(rhs)} for c, rhs in extra_rows],
                warmup=warmup, audits=audits, runs=runs, summary=summarize(runs))


def local_labels_instance():
    instance = block_chain(seed=73, blocks=16, paths=3, length=2, states=64, observed_states=0)
    instance.observations = [(path[0][0], j) for block, paths in enumerate(instance.blocks)
                             for j in range(4*block, 4*block+4) for path in paths]
    instance.observations.sort()
    assert instance.edge_count == 111 and len(instance.observations) == 192
    assert {j for _, j in instance.observations} == set(range(64))
    return instance


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repetitions', type=int, default=5)
    parser.add_argument('--quick', action='store_true')
    args = parser.parse_args()
    assert args.repetitions >= 1
    old = historical_flat()
    old.circuit_library.cache_clear(); old._profile_bases.cache_clear()
    _, old_circuit_time = timed(lambda: old.circuit_library(3))
    _, old_basis_time = timed(lambda: old._profile_bases(3))
    reduced_library.cache_clear(); _reduced_bases.cache_clear()
    _, circuit3_time = timed(lambda: reduced_library(3))
    _, basis3_time = timed(lambda: _reduced_bases(3))
    output = dict(versions={'python':platform.python_version(), 'numpy':np.__version__, 'scipy':scipy.__version__},
                  host={'platform':platform.platform(), 'processor':platform.processor(), 'logical_cpus':os.cpu_count(),
                        'thread_environment':{key:os.environ.get(key) for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS')}},
                  repetitions=args.repetitions, quick=args.quick,
                  protocol='One full recorded warmup per case; then repeated model construction with rotating method order. Exact audits and numerical cut-support audits run outside timed components. Host is not isolated; no persistent solver callback experiment.',
                  storage='Rows exclude variable bounds. Matrix bytes count input CSR arrays only; not Python objects, solver workspaces, or process peak memory.',
                  cold={'unreduced_three_coordinate_circuits_seconds':old_circuit_time,
                        'unreduced_three_coordinate_bases_seconds':old_basis_time,
                        'reduced_three_observed_label_circuits_seconds':circuit3_time,
                        'reduced_three_observed_label_bases_seconds':basis3_time,
                        'new_two_label_library':'No library construction or enumeration is called.'},
                  flat=[], membership=[], optimization=[])
    def save():
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, indent=2)+'\n')
    lengths = [8] if args.quick else [8, 32, 128, 512]
    for length in lengths:
        for interior in (False, True):
            for feasible in (True, False):
                instance, p = flat_instance(length, feasible, interior)
                methods = ['full', 'unreduced', 'flat']
                if not interior: methods.append('two_state')
                if length <= 32: methods += ['initial', 'eliminated']
                case = member_case(instance, p, feasible, methods, args.repetitions, old)
                case.update(gadgets=length, weights='interior' if interior else 'boundary')
                output['flat'].append(case); save()
                print(json.dumps({'flat':(length, interior, feasible), 'total_medians':
                      {method:values['total_seconds']['median'] for method, values in case['summary'].items()}}), flush=True)
    for m in ([16] if args.quick else [16, 128, 1024]):
        instance, p = membership_data(41, 4, 6, m)
        case = member_case(instance, p, True, ['full','global','initial','eliminated','separator'], args.repetitions)
        output['membership'].append(case); save()
        print(json.dumps({'membership_states':m, 'total_medians':
              {method:values['total_seconds']['median'] for method, values in case['summary'].items()}}), flush=True)
    instance = block_chain(seed=33, blocks=4, paths=5, states=128)
    rng = np.random.default_rng(1033)
    objective = np.r_[rng.normal(scale=.15, size=instance.edge_count), np.zeros(128), rng.normal(size=len(instance.observations))]
    y = [F(9, 10*128)]*128
    methods = ['full','global','initial','eliminated','network_states','cuts']
    case = opt_case(instance, objective, y, [], methods, args.repetitions)
    case['name'] = 'sparse_global_and_local_labels'; output['optimization'].append(case); save()
    print(json.dumps({'optimization':case['name'], 'total_medians':
          {method:values['total_seconds']['median'] for method, values in case['summary'].items()}}), flush=True)
    if not args.quick:
        unconstrained = optimize_ef(instance, objective, y_fixed=y, merge=True)
        p = rational_point(instance, unconstrained.original_point)
        resource = np.asarray([int(value > F(str(reference))) for value, reference in zip(p.x, instance.reference)])
        current = sum(int(d)*value for d, value in zip(resource, p.x))
        reference = sum(int(d)*F(str(value)) for d, value in zip(resource, instance.reference))
        assert current > reference
        budget = (current+reference)/2
        coefficients = np.r_[resource, np.zeros(instance.simplex_size+len(instance.observations))]
        case = opt_case(instance, objective, y, [(coefficients,budget)],
                        ['full','global','initial','eliminated','cuts'], args.repetitions)
        case.update(name='same_instance_aggregate_budget', unconstrained_resource=str(current),
                    reference_resource=str(reference), scope='H intersect one aggregate budget; exact-component relaxation, not a claim about convexifying the additionally constrained product graph')
        output['optimization'].append(case); save()
        print(json.dumps({'optimization':case['name'], 'total_medians':
              {method:values['total_seconds']['median'] for method, values in case['summary'].items()}}), flush=True)
        instance = local_labels_instance()
        rng = np.random.default_rng(1073)
        objective = np.r_[rng.normal(scale=.15, size=instance.edge_count), rng.normal(scale=.02, size=64), rng.normal(size=len(instance.observations))]
        case = opt_case(instance, objective, [F(9, 640)]*64, [],
                        ['full','global','initial','eliminated','network_states'], args.repetitions)
        case['name'] = 'all_labels_global_but_few_per_block'
        assert case['warmup']['full']['stats']['variables'] == case['warmup']['global']['stats']['variables'] == 7215
        assert case['warmup']['initial']['stats']['variables'] == 495
        assert case['warmup']['eliminated']['stats']['variables'] == 367
        output['optimization'].append(case); save()
        print(json.dumps({'optimization':case['name'], 'total_medians':
              {method:values['total_seconds']['median'] for method, values in case['summary'].items()}}), flush=True)


if __name__ == '__main__':
    main()
