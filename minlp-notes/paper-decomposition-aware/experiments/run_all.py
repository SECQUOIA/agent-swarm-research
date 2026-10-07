"""Reproduce experiments E1-E6 and S1 of the computational section.

    python3 run_all.py            # all experiments, 4 worker processes
    python3 run_all.py --jobs 2   # fewer workers
    python3 run_all.py --only E4  # one experiment
    python3 run_all.py --figures  # rebuild figures from saved CSV files

The solver is imported unchanged from the research solver directory.
Every task runs in a worker process with one numerical thread. Raw per-task
records go to results/raw/, plot-ready tables to results/*.csv, and figures
to figures/*.pdf. Machine data and load are recorded in results/environment.json.
"""
from __future__ import annotations

import os
for _var in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[_var] = '1'

import argparse
import csv
import gzip
import hashlib
import json
import math
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from instances import (SOLVER, flat_segment, planted, random_continuous,  # noqa: E402
                       random_small, tied_isolated)
from certified_grid import BoxQP, solve  # noqa: E402
from verify_certificate import verify_certificate  # noqa: E402
from exact_output import rational_heights, solve_exact  # noqa: E402
from analysis import growth_certificate, lemma_heights  # noqa: E402

RESULTS = HERE / 'results'
RAW = RESULTS / 'raw'
CERTS = RESULTS / 'certificates'
L_CONST = F(2)
SEEDS = (101, 202, 303)


def theorem_theta(kappa_ub: float) -> F:
    """Largest 2^-mu (mu >= 2) with theta^2 <= 1/(8 kappa)."""
    mu = 2
    while F(1, 4 ** mu) > F(1) / (8 * F(kappa_ub).limit_denominator(10**9)):
        mu += 1
    return F(1, 2 ** mu)


def stage_rows(problem, cert, info):
    """Per-stage quantities for the common-mesh lemma (lem:commonmesh).

    Constants of the lemma: |y_j - x*|^2 <= kappa n h_j^2, D(y_j) <= (9/16) L n h_j^2,
    retained radius <= 4.2 sqrt(n kappa) h_j, nodes per coordinate <=
    8 theta^-1 ceil(log2(n+2)). Ratios use kappa_lb, the lower end of the
    certified kappa interval, so they over-estimate the true ratios.
    """
    n = len(problem.b)
    xstar = [F(v) for v in info['xstar']] if info else None
    active = set(info['active']) if info else set()
    free = [i for i in range(n) if i not in active]
    kappa_lb = info['kappa_lb'] if info else None
    log_cap = (n + 1).bit_length()  # ceil(log2(n+2))
    rows = []
    for st in cert['stages']:
        h = F(st['h'])
        theta = F(st['theta'])
        grids = st['grids']
        y = [F(v) for v in st['grid_point']]
        beta = F(st['grid_lower'])
        nb = [(F(a), F(b)) for a, b in st['next_bounds']]
        nodes = [len(g) for g in grids]
        radius = [max(abs(lo - yi), abs(hi - yi)) for (lo, hi), yi in zip(nb, y)]
        dy = problem.value(tuple(y)) - beta  # = D(y_j) because Q(y_j) = beta_j
        row = {'stage': st['stage'], 'trial': st.get('trial'), 'trial_stage': st.get('trial_stage'),
               'h': float(h), 'theta': float(theta), 'table_states': st['table_states'],
               'max_nodes': max(nodes), 'removed_intervals': st['removed_intervals'],
               'max_nodes_free': max((nodes[i] for i in free), default=0),
               'mean_nodes_free': (sum(nodes[i] for i in free) / len(free)) if free else 0.0,
               'radius_over_h_free': float(max((radius[i] for i in free), default=F(0)) / h),
               'radius_over_h': float(max(radius) / h),
               'gap_U_minus_beta': float(F(st['upper']) - beta),
               'D_y_over_Lnh2': float(dy / (L_CONST * n * h * h)),
               'cap_nodes_impl': int(100 * (1 / theta) * log_cap) if theta else None,
               'cap_nodes_lemma': int(8 * (1 / theta) * log_cap) if theta else None}
        if xstar is not None:
            err = sum((a - b) ** 2 for a, b in zip(y, xstar))
            row.update({'E_over_nh2': float(err / (n * h * h)),
                        'y_dist_ratio_lemma': float(err / (n * h * h)) / kappa_lb,
                        'radius_ratio_lemma': float(max(radius) / h) / (4.2 * math.sqrt(n * kappa_lb)),
                        'xstar_retained': all(lo <= x <= hi for (lo, hi), x in zip(nb, xstar)),
                        'xstar_nodes_free': sum(1 for i in free if xstar[i] in set(map(F, grids[i]))),
                        'n_free': len(free),
                        'beta_le_fstar': beta <= F(info['fstar'])})
        rows.append(row)
    return rows


def run_grid(problem, info, *, epsilon, theta, pruning, grid_mode, schedule, max_stages,
             time_limit, max_table_states, convex_presolve=False, verify=True):
    t0, c0 = time.perf_counter(), time.process_time()
    kwargs = dict(epsilon=epsilon, max_stages=max_stages, time_limit=time_limit,
                  max_table_states=max_table_states, pruning=pruning, grid_mode=grid_mode,
                  schedule=schedule, convex_presolve=convex_presolve)
    if schedule == 'adaptive':
        kwargs.update(theta=theta, slope_decay_period=0)
    cert = solve(problem, **kwargs)
    solve_wall, solve_cpu = time.perf_counter() - t0, time.process_time() - c0
    rec = {'status': cert['status'], 'lower': cert['lower'], 'upper': cert['upper'],
           'gap': cert['gap'], 'gap_float': float(F(cert['gap'])),
           'stats': cert['stats'], 'solve_wall_s': solve_wall, 'solve_cpu_s': solve_cpu,
           'stages': stage_rows(problem, cert, info)}
    if verify:
        t1, c1 = time.perf_counter(), time.process_time()
        try:
            check = verify_certificate(cert, max_table_states=10**7)
            rec['verify'] = {'valid': check['valid'], 'lower': check['lower'], 'upper': check['upper']}
        except Exception as exc:  # record, never hide, a failed replay
            rec['verify'] = {'valid': False, 'error': repr(exc)}
        rec['verify_wall_s'] = time.perf_counter() - t1
        rec['verify_cpu_s'] = time.process_time() - c1
    if info is not None:
        rec['fstar_enclosed'] = F(cert['lower']) <= F(info['fstar']) <= F(cert['upper'])
    return rec, cert


# ---------------------------------------------------------------- tasks
def task_grid(spec):
    problem, info = planted(spec['kind'], spec['n'], spec['kappa_target'], spec['seed'])
    theta = F(spec['theta']) if spec.get('theta') is not None else theorem_theta(info['kappa_ub'])
    rec, _ = run_grid(problem, info, epsilon=F(spec.get('epsilon', '1/1208925819614629174706176')),
                      theta=theta, pruning=spec['pruning'], grid_mode=spec['grid_mode'],
                      schedule=spec.get('schedule', 'adaptive'), max_stages=spec['max_stages'],
                      time_limit=spec['time_limit'], max_table_states=spec['max_table_states'],
                      convex_presolve=spec.get('convex_presolve', False))
    rec.update({'spec': spec, 'instance': {k: v for k, v in info.items() if k != 'edges'},
                'theta_used': str(theta) if spec.get('schedule', 'adaptive') == 'adaptive' else None})
    return rec


def task_exact(spec):
    if spec['family'] == 'random':
        problem = random_small(spec['n'], spec['kind'], spec['n_int'], spec['seed'])
        info = None
    elif spec['family'] == 'tied':
        problem = tied_isolated(spec['seed'])
        info = None
    elif spec['family'] == 'flat':
        problem = flat_segment(spec['seed'])
        info = None
    else:
        problem, info = planted(spec['kind'], spec['n'], spec['kappa_target'], spec['seed'])
    from oracle import exact_minimum
    t0 = time.perf_counter()
    ref, ref_points = exact_minimum([list(r) for r in problem.A], list(problem.b), problem.constant,
                                    list(problem.bounds), set(problem.integers))
    oracle_s = time.perf_counter() - t0
    t0, c0 = time.perf_counter(), time.process_time()
    cert = solve_exact(problem, time_limit=spec['time_limit'], max_rounds=12, max_stages=3000,
                       max_table_states=200000)
    solve_wall, solve_cpu = time.perf_counter() - t0, time.process_time() - c0
    t1 = time.perf_counter()
    try:
        check = verify_certificate(cert, max_table_states=10**7)
        verify = {'valid': check['valid'], 'exact': check['exact'], 'lower': check['lower'],
                  'upper': check['upper']}
    except Exception as exc:
        verify = {'valid': False, 'error': repr(exc)}
    verify_s = time.perf_counter() - t1
    CERTS.mkdir(parents=True, exist_ok=True)
    with gzip.open(CERTS / f"E4_{problem.name}.certificate.json.gz", 'wt') as fh:
        json.dump(cert, fh)
    point = tuple(F(v) for v in cert['point'])
    rec = {'spec': spec, 'name': problem.name, 'n': len(problem.b),
           'n_integer': len(problem.integers), 'max_bag_size': max(map(len, problem.bags)),
           'status': cert['status'], 'value': cert['upper'], 'lower': cert['lower'],
           'proof_kind': cert.get('proof', {}).get('kind'),
           'proof_source': cert.get('proof', {}).get('source'),
           'n_feasible_proposals': len(cert.get('feasible_proposals', [])),
           'point_from_recovery_proposal': any(prop['point'] == cert['point']
                                               for prop in cert.get('feasible_proposals', [])),
           'rounds': cert['stats']['rounds'], 'stages': cert['stats']['completed_stages'],
           'table_states': cert['stats']['completed_table_states'],
           'solve_wall_s': solve_wall, 'solve_cpu_s': solve_cpu, 'verify_wall_s': verify_s,
           'verify': verify, 'oracle_value': str(ref), 'oracle_s': oracle_s,
           'oracle_optimal_candidates': len(ref_points),
           'value_matches_oracle': cert['status'] == 'exact' and F(cert['upper']) == ref,
           'point_is_optimal': problem.feasible(point) and problem.value(point) == ref,
           'value_denominator': F(cert['upper']).denominator,
           'height_value_bound_bits': int(F(cert['heights']['value'])).bit_length(),
           'required_gap_bits': math.log2(int(F(cert['heights']['value'])) * F(cert['upper']).denominator),
           # Bits log2(Omega W) at the optimum (W = denominator of the optimal value),
           # with the solver's row-sum constant (Remark rem:heights) and with
           # the constant of (eq:exact-constants).
           'required_gap_bits_code': math.log2(int(F(cert['heights']['value'])) * ref.denominator),
           'required_gap_bits_lemma': math.log2(lemma_heights(problem)['Omega'] * ref.denominator),
           'final_gap': float(F(cert['upper']) - F(cert['lower'])),
           'final_gap_bits': (-math.log2(F(cert['upper']) - F(cert['lower']))
                              if F(cert['upper']) > F(cert['lower']) else None)}
    if info is not None:
        rec['planted_point_recovered'] = list(map(str, point)) == info['xstar']
    return rec


def task_scip(spec):
    problem, info = planted(spec['kind'], spec['n'], spec['kappa_target'], spec['seed'])
    import pyscipopt
    from pyscipopt import Model, quicksum
    n = len(problem.b)
    m = Model()
    m.hideOutput()
    m.setParam('limits/time', float(spec['time_limit']))
    # Same absolute target as the certified grid runs; SCIP's default relative
    # gap limit (0) is kept. Parameters that do not exist are recorded as skipped.
    m.setParam('limits/absgap', float(spec['absgap']))
    params = {'limits/time': float(spec['time_limit']), 'limits/absgap': float(spec['absgap'])}
    if spec.get('feastol'):
        for name in ('numerics/feastol', 'numerics/dualfeastol'):
            m.setParam(name, float(spec['feastol']))
            params[name] = float(spec['feastol'])
    for name, val in (('parallel/maxnthreads', 1), ('lp/threads', 1), ('randomization/randomseedshift', 0)):
        try:
            m.setParam(name, val)
            params[name] = val
        except Exception:
            params[name] = 'skipped (not available)'
    x = [m.addVar(f'x{i}', lb=float(lo), ub=float(hi),
                  vtype='I' if i in problem.integers else 'C') for i, (lo, hi) in enumerate(problem.bounds)]
    t = m.addVar('t', lb=None, ub=None)
    quad = quicksum(float(problem.b[i]) * x[i] for i in range(n)) \
        + quicksum(float(problem.A[i][i]) / 2 * x[i] * x[i] for i in range(n)) \
        + quicksum(float(a) * x[i] * x[j] for i, j, a in problem.interactions)
    if spec.get('offset'):  # constant as an objective offset instead of inside t >= F(x)
        m.addCons(t >= quad)
        m.setObjective(t, 'minimize')
        m.addObjoffset(float(problem.constant))
    else:
        m.addCons(t >= float(problem.constant) + quad)
        m.setObjective(t, 'minimize')
    t0, c0 = time.perf_counter(), time.process_time()
    m.optimize()
    wall, cpu = time.perf_counter() - t0, time.process_time() - c0
    rec = {'spec': spec, 'instance': {k: v for k, v in info.items() if k != 'edges'},
           'scip_version': str(m.version()), 'pyscipopt_version': pyscipopt.__version__,
           'status': m.getStatus(), 'scip_solving_time_s': m.getSolvingTime(),
           'wall_s': wall, 'cpu_s': cpu, 'nodes': m.getNTotalNodes(),
           'primal_bound': m.getPrimalbound(), 'dual_bound': m.getDualbound(), 'gap': m.getGap(),
           'params': params, 'objective_constant': float(problem.constant)}
    if m.getNSols() > 0:
        sol = m.getBestSol()
        pt = []
        for i, (lo, hi) in enumerate(problem.bounds):
            v = F(sol[x[i]])  # exact binary value of the double
            v = min(max(v, lo), hi)
            if i in problem.integers:
                v = F(round(v))
            pt.append(v)
        exact_val = problem.value(tuple(pt))
        rec['exact_value_of_scip_point'] = float(exact_val)
        # Positive values mean that SCIP's epigraph variable lies below the exact
        # objective of its own (clipped) point, i.e. a tolerated constraint violation.
        rec['epigraph_shortfall'] = float(exact_val - F(sol[t])
                                          - (F(float(problem.constant)) if spec.get('offset') else 0))
        rec['primal_bound_below_fstar'] = m.getPrimalbound() < float(F(info['fstar']))
        rec['scip_point_excess_over_fstar'] = float(exact_val - F(info['fstar']))
        rec['scip_dist_to_xstar'] = math.sqrt(float(sum((a - F(b)) ** 2 for a, b in zip(pt, info['xstar']))))
        # Gap of SCIP's own interval with its incumbent evaluated exactly:
        # exact value of the (clipped) incumbent minus the dual bound (a double, read exactly).
        rec['exact_gap'] = float(exact_val - F(m.getDualbound()))
        rec['interval_contains_fstar'] = m.getDualbound() <= float(F(info['fstar'])) <= m.getPrimalbound()
    rec['dual_bound_le_fstar'] = rec['dual_bound'] <= float(F(info['fstar'])) + 1e-9
    return rec


def task_localized(spec):
    """S1: localized exact acceptance (proposed test) versus the height rule."""
    from localized import first_acceptance
    problem = random_small(spec['n'], spec['kind'], spec['n_int'], spec['seed'])
    t0 = time.perf_counter()
    cert = solve(problem, epsilon=F(1, 2**60), max_stages=spec['max_stages'], time_limit=60,
                 max_table_states=300000, convex_presolve=False)
    solve_s = time.perf_counter() - t0
    check = verify_certificate(cert, max_table_states=10**7)
    stage, xhat, full = first_acceptance(problem, cert)
    rec = {'spec': spec, 'name': problem.name, 'n': len(problem.b), 'n_integer': len(problem.integers),
           'n_concave': sum(1 for i in range(len(problem.b)) if problem.A[i][i] <= 0),
           'max_bag_size': max(map(len, problem.bags)), 'history_valid': check['valid'],
           'local_first_stage': stage, 'local_accepted_on_full_box': full,
           'local_time_to_acceptance_s': (cert['stages'][stage]['elapsed_seconds']
                                          if stage is not None else None),
           'local_value': str(problem.value(xhat)) if xhat is not None else None,
           'grid_run_s': solve_s}
    t0 = time.perf_counter()
    ex = solve_exact(problem, time_limit=60, max_rounds=12, max_stages=3000, max_table_states=300000)
    rec.update({'height_rule_status': ex['status'], 'height_rule_value': ex['upper'],
                'height_rule_stages': ex['stats']['completed_stages'],
                'height_rule_rounds': ex['stats']['rounds'],
                'height_rule_s': time.perf_counter() - t0,
                'height_value_bound_bits': int(F(ex['heights']['value'])).bit_length()})
    rec['values_agree'] = (None if stage is None or ex['status'] != 'exact'
                           else F(rec['local_value']) == F(ex['upper']))
    # One grid run (CT) and the threshold of Proposition prop:accept: the first
    # stage after which the certified gap U - beta is below 1/(Omega W), where W
    # is the denominator of the optimal value (found by EX), with Omega of
    # (eq:exact-constants) ('lemma') and the solver's row-sum constant ('code').
    # From then on an optimal candidate (for example from REC) passes the test.
    # The run targets 1/(2 Omega W), so it does not stop earlier.
    if ex['status'] == 'exact':
        opt = F(ex['upper'])
        w_opt = opt.denominator
        for label, omega in (('lemma', lemma_heights(problem)['Omega']),
                             ('code', int(F(rational_heights(problem)['value'])))):
            rec[f'omega_bits_{label}'] = math.log2(omega * w_opt)
            t0 = time.perf_counter()
            run = solve(problem, epsilon=F(1, 2 * omega * w_opt), max_stages=3000, time_limit=120,
                        max_table_states=300000, convex_presolve=False)
            threshold = F(1, omega * w_opt)
            first, incumbent_optimal = None, None
            if F(run['initial']['upper']) - F(run['initial']['lower']) < threshold:
                first, incumbent_optimal = 0, F(run['initial']['upper']) == opt
            for st in ([] if first == 0 else run['stages']):
                if F(st['upper']) - F(st['lower']) < threshold:
                    first = st['stage'] + 1  # stages completed when the gap first passes
                    incumbent_optimal = F(st['upper']) == opt
                    break
            rec[f'single_run_stages_{label}'] = first
            rec[f'single_run_incumbent_optimal_{label}'] = incumbent_optimal
            rec[f'single_run_status_{label}'] = run['status']
            rec[f'single_run_trials_{label}'] = len({st['trial'] for st in run['stages']})
            rec[f'single_run_s_{label}'] = time.perf_counter() - t0
    if len(problem.b) <= 6:
        from oracle import exact_minimum
        ref, _ = exact_minimum([list(r) for r in problem.A], list(problem.b), problem.constant,
                               list(problem.bounds), set(problem.integers))
        rec['oracle_value'] = str(ref)
        rec['local_matches_oracle'] = None if stage is None else F(rec['local_value']) == ref
    from localized import first_face_acceptance
    fstage, fx = first_face_acceptance(problem, cert)
    rec['face_first_stage'] = fstage
    rec['face_value'] = str(problem.value(fx)) if fx is not None else None
    rec['face_agrees_with_EX'] = (None if fx is None or ex['status'] != 'exact'
                                  else problem.value(fx) == F(ex['upper']))
    rec['status'] = 'accepted' if stage is not None else 'not_accepted'
    return rec


def task_random_growth(spec):
    """E6: unplanted random continuous box QP; CT at several accuracies.

    The candidate is the stationary point of the face of the final incumbent of
    the most accurate run. Its optimality is proved by Lemma lem:growthcert(a)
    when that sufficient condition holds (which also brackets kappa), otherwise
    by the localized test of Proposition prop:local on the same certificate.
    """
    from localized import candidate, first_acceptance
    problem = random_continuous(spec['kind'], spec['n'], spec['seed'])
    n = len(problem.b)
    rec = {'spec': spec, 'name': problem.name, 'n': n, 'max_bag_size': max(map(len, problem.bags)),
           'lambda_min_H': float(__import__('numpy').linalg.eigvalsh(
               [[float(v) for v in row] for row in problem.A])[0]),
           'runs': {}}
    certs = {}
    for q in sorted(spec['q_list'], reverse=True):
        t0 = time.perf_counter()
        cert = solve(problem, epsilon=F(1, 2 ** q), max_stages=600, time_limit=120,
                     max_table_states=10 ** 6, convex_presolve=False)
        solve_s = time.perf_counter() - t0
        t1 = time.perf_counter()
        try:
            valid = verify_certificate(cert, max_table_states=10 ** 7)['valid']
        except Exception as exc:
            valid = repr(exc)
        replay_s = time.perf_counter() - t1
        st = cert['stages']
        final_trial = st[-1]['trial'] if st else None
        rec['runs'][q] = {'status': cert['status'], 'gap': float(F(cert['gap'])), 'stages': len(st),
                          'trials': len({x['trial'] for x in st}), 'final_trial': final_trial,
                          'max_nodes': max((len(g) for x in st for g in x['grids']), default=0),
                          'max_nodes_final_trial': max((len(g) for x in st if x['trial'] == final_trial
                                                        for g in x['grids']), default=0),
                          'table_states': cert['stats']['completed_table_states'],
                          'solve_s': solve_s, 'replay_s': replay_s, 'replay_valid': valid}
        certs[q] = cert
    best = certs[max(spec['q_list'])]
    xhat = candidate(problem, tuple(F(v) for v in best['point']))
    growth = growth_certificate(problem, xhat) if xhat is not None else {'status': 'no candidate'}
    rec['growth'] = growth
    proof = 'growth' if growth['status'] == 'certified' else None
    if proof is None:
        stage, xloc, _ = first_acceptance(problem, best)
        if stage is not None:
            xhat, proof = xloc, 'localized'
    rec['optimality_proof'] = proof
    if xhat is not None:
        rec['xhat'] = list(map(str, xhat))
        rec['value'] = str(problem.value(xhat))
        free = [i for i, (lo, hi) in enumerate(problem.bounds) if lo < xhat[i] < hi]
        rec['n_free'] = len(free)
        rec['free_denominators'] = sorted({xhat[i].denominator for i in free})
        for q, cert in certs.items():
            last = cert['stages'][-1] if cert['stages'] else None
            rec['runs'][q]['xhat_nodes_free_last_stage'] = (
                None if last is None else
                sum(1 for i in free if xhat[i] in set(map(F, last['grids'][i]))))
            rec['runs'][q]['upper_equals_value'] = F(cert['upper']) == problem.value(xhat)
    if n <= 8:
        from oracle import exact_minimum
        ref, _ = exact_minimum([list(r) for r in problem.A], list(problem.b), problem.constant,
                               list(problem.bounds), set())
        rec['oracle_value'] = str(ref)
        rec['matches_oracle'] = xhat is not None and problem.value(xhat) == ref
    rec['status'] = proof or 'unproved'
    return rec


TASKS = {'grid': task_grid, 'exact': task_exact, 'scip': task_scip, 'localized': task_localized,
         'random_growth': task_random_growth}


def run_task(item):
    key, kind, spec = item
    t0 = time.perf_counter()
    try:
        rec = TASKS[kind](spec)
        rec['ok'] = True
    except Exception as exc:
        rec = {'spec': spec, 'ok': False, 'error': repr(exc)}
    rec['key'] = key
    rec['task_wall_s'] = time.perf_counter() - t0
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / f'{key}.json').write_text(json.dumps(rec, indent=1, default=str) + '\n')
    return key, rec


# ---------------------------------------------------------------- designs
def design():
    tasks = []
    # E1: accuracy dependence of per-stage states, kappa ~ 4, theorem theta.
    for kind, n in (('path', 16), ('tree', 16), ('band2', 12), ('band3', 8)):
        for seed in SEEDS:
            for grid_mode in ('geometric', 'uniform'):
                for pruning in (True, False):
                    tag = f"{grid_mode[:4]}_{'pruned' if pruning else 'full'}"
                    tasks.append((f'E1_{kind}{n}_s{seed}_{tag}', 'grid',
                                  dict(exp='E1', kind=kind, n=n, kappa_target=4, seed=seed,
                                       grid_mode=grid_mode, pruning=pruning, theta=None,
                                       max_stages=16, time_limit=40, max_table_states=100000)))
    # E2: dependence on kappa (path, n = 16).
    for kt in (2, 4, 8, 16, 32, 64, 128, 256):
        for seed in SEEDS:
            for tag, grid_mode, theta in (('geom_theorem', 'geometric', None),
                                          ('geom_quarter', 'geometric', '1/4'),
                                          ('unif', 'uniform', None)):
                tasks.append((f'E2_k{kt}_s{seed}_{tag}', 'grid',
                              dict(exp='E2', kind='path', n=16, kappa_target=kt, seed=seed,
                                   grid_mode=grid_mode, pruning=True, theta=theta, method=tag,
                                   max_stages=12, time_limit=60, max_table_states=200000)))
            tasks.append((f'E2_k{kt}_s{seed}_default', 'grid',
                          dict(exp='E2', kind='path', n=16, kappa_target=kt, seed=seed,
                               grid_mode='geometric', pruning=True, schedule='conditioning',
                               epsilon='1/1048576', method='default_schedule', convex_presolve=True,
                               max_stages=200, time_limit=60, max_table_states=200000)))
    # E3: dependence on n (paths). kappa_target = 4 has a coupled free block;
    # for kappa_target = 2 the generator sets the free-free couplings to zero
    # (H_SS = 2I), so the free coordinates are separable.
    for kt in (2, 4):
        for n in (4, 8, 16, 32, 64, 128):
            for seed in SEEDS:
                for tag, grid_mode, theta in (('geom_theorem', 'geometric', None),
                                              ('geom_quarter', 'geometric', '1/4'),
                                              ('unif', 'uniform', None)):
                    tasks.append((f'E3_k{kt}_n{n}_s{seed}_{tag}', 'grid',
                                  dict(exp='E3', kind='path', n=n, kappa_target=kt, seed=seed,
                                       grid_mode=grid_mode, pruning=True, theta=theta, method=tag,
                                       max_stages=11, time_limit=60, max_table_states=200000)))
    # E4: exact rational output against an independent enumeration.
    seed = 4000
    for n in (3, 4, 5, 6):
        for kind in ('path', 'tree', 'band2'):
            seed += 1
            tasks.append((f'E4_random_{kind}_n{n}_s{seed}', 'exact',
                          dict(exp='E4', family='random', kind=kind, n=n, n_int=1 + (n >= 5),
                               seed=seed, time_limit=30)))
    for s in (1, 2, 3):
        tasks.append((f'E4_tied_s{s}', 'exact', dict(exp='E4', family='tied', seed=s, time_limit=30)))
    for s in (1, 2):
        tasks.append((f'E4_flat_s{s}', 'exact', dict(exp='E4', family='flat', seed=s, time_limit=5)))
    for kind, n in (('path', 6), ('tree', 6), ('band2', 6)):
        tasks.append((f'E4_planted_{kind}_n{n}', 'exact',
                      dict(exp='E4', family='planted', kind=kind, n=n, kappa_target=4,
                           seed=4100, time_limit=30)))
    # E5: SCIP (numerical, single thread) and the default certified grid solver.
    e5 = [('path', 16), ('tree', 16), ('band2', 12), ('band3', 8), ('path', 32), ('path', 64),
          ('path', 128)]
    for kind, n in e5:
        for seed in SEEDS:
            base = dict(exp='E5', kind=kind, n=n, kappa_target=4, seed=seed)
            tasks.append((f'E5_{kind}{n}_s{seed}_scip', 'scip', dict(base, time_limit=20, absgap=1e-6)))
            tasks.append((f'E5_{kind}{n}_s{seed}_grid', 'grid',
                          dict(base, grid_mode='geometric', pruning=True, schedule='conditioning',
                               epsilon='1/1000000', method='default_schedule', convex_presolve=True,
                               max_stages=200,
                               time_limit=60, max_table_states=200000)))
    # E5V: robustness of the SCIP outcome (time limit 60 s; feasibility and dual
    # feasibility tolerances 1e-9; objective constant as an offset).
    for kind, n in e5:
        for seed in SEEDS:
            base = dict(exp='E5V', kind=kind, n=n, kappa_target=4, seed=seed, absgap=1e-6)
            tasks.append((f'E5V_{kind}{n}_s{seed}_offset', 'scip',
                          dict(base, variant='offset', time_limit=20, offset=True)))
            if n >= 32:
                tasks.append((f'E5V_{kind}{n}_s{seed}_t60', 'scip',
                              dict(base, variant='t60', time_limit=60)))
                tasks.append((f'E5V_{kind}{n}_s{seed}_feastol', 'scip',
                              dict(base, variant='feastol', time_limit=20, feastol=1e-9)))
    # E6: unplanted random continuous instances, CT at several accuracies.
    for kind in ('path', 'band2'):
        for n in (8, 12, 16, 24):
            for rep in range(1, 6):
                seed = 1000 * n + rep + (0 if kind == 'path' else 500)
                tasks.append((f'E6_{kind}_n{n}_s{seed}', 'random_growth',
                              dict(exp='E6', kind=kind, n=n, seed=seed, q_list=[10, 20, 30, 40, 50])))
    # S1 (supplementary): localized exact acceptance on unplanted random instances.
    seed = 7000
    for n in (4, 6, 8, 12, 16):
        for kind in ('path', 'tree', 'band2'):
            for rep in range(2):
                seed += 1
                tasks.append((f'S1_{kind}_n{n}_s{seed}', 'localized',
                              dict(exp='S1', kind=kind, n=n, n_int=1 + (n >= 8), seed=seed,
                                   max_stages=60)))
    return tasks


def environment():
    info = {'python': sys.version, 'platform': platform.platform(), 'nproc': os.cpu_count(),
            'loadavg': Path('/proc/loadavg').read_text().split()[:3]}
    try:
        cpu = [l for l in Path('/proc/cpuinfo').read_text().splitlines() if l.startswith('model name')]
        info['cpu_model'] = cpu[0].split(':', 1)[1].strip() if cpu else None
    except OSError:
        pass
    import numpy, matplotlib
    info['numpy'], info['matplotlib'] = numpy.__version__, matplotlib.__version__
    try:
        import pyscipopt
        info['pyscipopt'] = pyscipopt.__version__
        info['scip'] = str(pyscipopt.Model().version())
    except Exception as exc:
        info['pyscipopt'] = repr(exc)
    info['solver_dir'] = str(SOLVER)
    info['solver_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(SOLVER.glob('*.py'))
                             if p.name in ('certified_grid.py', 'finite_dp.py', 'decomposition.py',
                                           'exact_output.py', 'verify_certificate.py',
                                           'rational_optimization.py')}
    info['experiment_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                 for p in sorted(HERE.glob('*.py'))}
    return info


def write_csvs():
    recs = [json.loads(p.read_text()) for p in sorted(RAW.glob('*.json'))]
    by = lambda e: [r for r in recs if r.get('spec', {}).get('exp') == e]

    def dump(name, rows):
        if not rows:
            return
        keys = []
        for r in rows:
            for k in r:
                if k not in keys:
                    keys.append(k)
        with open(RESULTS / name, 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(rows)

    stage_rows_all, run_rows = [], []
    for r in by('E1') + by('E2') + by('E3') + [x for x in by('E5') if x['key'].endswith('_grid')]:
        s = r['spec']
        method = s.get('method') or f"{s['grid_mode']}_{'pruned' if s['pruning'] else 'unpruned'}"
        base = {'exp': s['exp'], 'key': r['key'], 'kind': s['kind'], 'n': s['n'],
                'seed': s['seed'], 'kappa_target': s['kappa_target'], 'method': method}
        if not r.get('ok'):
            run_rows.append(dict(base, status='error', error=r.get('error')))
            continue
        inst = r['instance']
        run_rows.append(dict(base, status=r['status'], gap=r['gap_float'],
                             kappa_lb=inst['kappa_lb'], kappa_ub=inst['kappa_ub'], nu=inst['nu'],
                             max_bag_size=inst['max_bag_size'], theta=r.get('theta_used'),
                             completed_stages=r['stats']['completed_stages'],
                             attempted_stages=r['stats'].get('attempted_stages'),
                             total_states=r['stats']['completed_table_states'],
                             max_stage_states=max((x['table_states'] for x in r['stages']), default=0),
                             solve_wall_s=r['solve_wall_s'], solve_cpu_s=r['solve_cpu_s'],
                             verify_wall_s=r.get('verify_wall_s'),
                             verify_valid=r.get('verify', {}).get('valid'),
                             fstar_enclosed=r.get('fstar_enclosed'),
                             final_trial=(r['stages'][-1]['trial'] if r['stages'] else None),
                             xstar_always_retained=all(x.get('xstar_retained', True) for x in r['stages'])))
        for row in r['stages']:
            stage_rows_all.append(dict(base, **row))
    for e in ('E1', 'E2', 'E3', 'E5'):
        dump(f'{e}_runs.csv' if e != 'E5' else 'E5_grid_runs.csv', [x for x in run_rows if x['exp'] == e])
        dump(f'{e}_stages.csv' if e != 'E5' else 'E5_grid_stages.csv',
             [x for x in stage_rows_all if x['exp'] == e])
    e4 = []
    for r in by('E4'):
        row = {k: v for k, v in r.items() if k not in ('spec', 'verify')}
        row['family'] = r['spec']['family']
        row['verify_valid'] = r.get('verify', {}).get('valid')
        row['verify_exact'] = r.get('verify', {}).get('exact')
        e4.append(row)
    dump('E4_exact.csv', e4)
    def scip_rows(recs):
        out = []
        for r in recs:
            s = r['spec']
            row = {'key': r['key'], 'kind': s['kind'], 'n': s['n'], 'seed': s['seed'],
                   'variant': s.get('variant', 'default'), 'time_limit': s['time_limit'], 'ok': r.get('ok')}
            if r.get('ok'):
                row.update({k: r.get(k) for k in (
                    'status', 'scip_solving_time_s', 'wall_s', 'cpu_s', 'nodes', 'primal_bound',
                    'dual_bound', 'gap', 'exact_value_of_scip_point', 'exact_gap',
                    'interval_contains_fstar', 'scip_point_excess_over_fstar', 'scip_dist_to_xstar',
                    'dual_bound_le_fstar', 'epigraph_shortfall', 'primal_bound_below_fstar',
                    'scip_version', 'pyscipopt_version')})
                row['objective_constant'] = r.get('objective_constant')
                row['mu'] = r['instance'].get('mu')
            else:
                row['error'] = r.get('error')
            out.append(row)
        return out
    dump('E5_scip.csv', scip_rows([r for r in by('E5') if r['key'].endswith('_scip')]))
    dump('E5V_scip_variants.csv', scip_rows(by('E5V')))
    e6 = []
    for r in by('E6'):
        if not r.get('ok'):
            e6.append({'key': r['key'], 'error': r.get('error')})
            continue
        g = r['growth']
        for q, run in sorted(r['runs'].items(), key=lambda kv: int(kv[0])):
            e6.append({'key': r['key'], 'name': r['name'], 'kind': r['spec']['kind'], 'n': r['n'],
                       'seed': r['spec']['seed'], 'max_bag_size': r['max_bag_size'],
                       'lambda_min_H': r['lambda_min_H'], 'optimality_proof': r['optimality_proof'],
                       'growth_status': g['status'], 'kappa_lb': g.get('kappa_lb'),
                       'kappa_ub': g.get('kappa_ub'), 'n_free': r.get('n_free'),
                       'matches_oracle': r.get('matches_oracle'), 'q': int(q), **run})
    dump('E6_random_growth.csv', e6)
    s1 = []
    for r in by('S1'):
        row = {k: v for k, v in r.items() if k != 'spec'}
        row['kind'] = r['spec']['kind']
        s1.append(row)
    dump('S1_localized.csv', s1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--only', default=None, help='comma-separated experiment ids, e.g. E1,E4')
    ap.add_argument('--figures', action='store_true', help='only rebuild CSV files and figures')
    args = ap.parse_args()
    jobs = max(1, min(4, args.jobs))
    RESULTS.mkdir(exist_ok=True)
    if not args.figures:
        tasks = design()
        if args.only:
            keep = set(args.only.split(','))
            tasks = [t for t in tasks if t[2]['exp'] in keep]
        env = environment()
        env['started'] = time.strftime('%Y-%m-%d %H:%M:%S')
        env['jobs'] = jobs
        env['n_tasks'] = len(tasks)
        t0, c0 = time.perf_counter(), time.process_time()
        # Longest tasks first keeps the four workers busy until the end.
        order = sorted(tasks, key=lambda t: (t[2].get('n', 0) * (2 if t[2].get('grid_mode') == 'uniform' else 1)), reverse=True)
        failures = []
        with ProcessPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(run_task, t) for t in order]
            for k, fut in enumerate(as_completed(futures), 1):
                key, rec = fut.result()
                if not rec.get('ok'):
                    failures.append({'key': key, 'error': rec.get('error')})
                print(f"[{k}/{len(futures)}] {key}: {rec.get('status', rec.get('error'))} "
                      f"({rec['task_wall_s']:.1f}s)", flush=True)
        env['finished'] = time.strftime('%Y-%m-%d %H:%M:%S')
        env['wall_s'] = time.perf_counter() - t0
        env['loadavg_end'] = Path('/proc/loadavg').read_text().split()[:3]
        recs = [json.loads((RAW / f'{t[0]}.json').read_text()) for t in tasks]
        env['sum_task_wall_s'] = sum(r['task_wall_s'] for r in recs)
        env['failures'] = failures
        name = 'environment.json' if not args.only else f"environment_{args.only.replace(',', '_')}.json"
        (RESULTS / name).write_text(json.dumps(env, indent=1) + '\n')
    write_csvs()
    from figures import make_all
    make_all(RESULTS, HERE / 'figures')


if __name__ == '__main__':
    main()
