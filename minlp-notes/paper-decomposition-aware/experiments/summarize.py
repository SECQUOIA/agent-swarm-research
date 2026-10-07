"""Headline numbers from the saved results -> results/summary.json (and stdout).

Every number quoted in Section 11 of the paper is computed here from the CSV
files of run_all.py, chain/, recourse/ and qplib/.
"""
import csv
import json
import math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
from statistics import median

HERE = Path(__file__).resolve().parent
RES = HERE / 'results'


def read(path):
    with open(path) as fh:
        return list(csv.DictReader(fh))


def plateau(stage_rows, key, last=4):
    by = defaultdict(list)
    for r in stage_rows:
        by[r['key']].append((int(r['stage']), float(r[key])))
    return {k: median(x for _, x in sorted(v)[-last:]) for k, v in by.items()}


def last_stage(stage_rows):
    last = {}
    for r in stage_rows:
        if r['key'] not in last or int(r['stage']) > int(last[r['key']]['stage']):
            last[r['key']] = r
    return last


def rng(values, nd=3):
    values = [v for v in values if v is not None]
    return [round(min(values), nd), round(max(values), nd)] if values else None


def main():
    out = {}
    st = {e: read(RES / f'{e}_stages.csv') for e in ('E1', 'E2', 'E3')}
    runs = {e: read(RES / f'{e}_runs.csv') for e in ('E1', 'E2', 'E3')}

    # ---------------- E1
    e1 = {'runs': len(runs['E1']),
          'all_replays_valid': all(r['verify_valid'] == 'True' for r in runs['E1']),
          'all_enclose_fstar': all(r['fstar_enclosed'] == 'True' for r in runs['E1']),
          'optimizer_never_filtered': all(r['xstar_always_retained'] == 'True' for r in runs['E1'])}
    per = defaultdict(lambda: defaultdict(list))
    for r in st['E1']:
        per[(r['kind'], r['n'], r['method'])][int(r['stage'])].append(int(r['table_states']))
    e1['median_table_entries_by_stage'] = {f'{k[0]}{k[1]}:{k[2]}': [int(median(v[j])) for j in sorted(v)]
                                           for k, v in sorted(per.items())}
    out['E1'] = e1

    # ---------------- constants of lem:commonmesh over runs with 8 kappa theta^2 <= 1
    comp = ([('E1', r) for r in st['E1'] if r['method'] == 'geometric_pruned']
            + [('E2', r) for r in st['E2'] if r['method'] == 'geom_theorem']
            + [('E3', r) for r in st['E3'] if r['method'] == 'geom_theorem'])
    kub = {r['key']: float(r['kappa_ub']) for e in runs for r in runs[e]}
    assert all(8 * kub[r['key']] * float(r['theta']) ** 2 <= 1 for _, r in comp)
    lemma = {}
    for e in ('E1', 'E2', 'E3', 'all'):
        rows = [r for x, r in comp if e in (x, 'all')]
        lemma[e] = {'stage_rows': len(rows),
                    'max_D_over_Lnh2 (bound 9/16)': max(float(r['D_y_over_Lnh2']) for r in rows),
                    'max_dist2_over_kappa_n_h2 (bound 1)': max(float(r['y_dist_ratio_lemma']) for r in rows),
                    'max_radius_over_4.2sqrt(n kappa)h': max(float(r['radius_ratio_lemma']) for r in rows),
                    'max_nodes_over_cap_8/theta_log': max(int(r['max_nodes']) / int(r['cap_nodes_lemma'])
                                                          for r in rows),
                    'max_nodes_over_impl_cap_100/theta_log': max(int(r['max_nodes']) / int(r['cap_nodes_impl'])
                                                                  for r in rows)}
    out['lemma_constants_theorem_theta_runs'] = lemma

    # ---------------- off-grid minimizers: free coordinates of x* that are grid nodes
    offgrid = {}
    for e in ('E1', 'E2', 'E3'):
        last = last_stage(st[e])
        info = {r['key']: r for r in runs[e]}
        by = defaultdict(lambda: [0, 0, 0, 0])
        for key, r in last.items():
            k = info[key]
            tag = f"{e}:kappa{k['kappa_target']}:{r['method']}"
            by[tag][0] += int(r['xstar_nodes_free'])
            by[tag][1] += int(r['n_free'])
        for r in st[e]:
            k = info[r['key']]
            tag = f"{e}:kappa{k['kappa_target']}:{r['method']}"
            by[tag][2] += int(r['xstar_nodes_free'])
            by[tag][3] += int(r['n_free'])
        for tag, (a, b, c, d) in by.items():
            offgrid[tag] = {'final_stage_nodes': a, 'final_stage_free_coords': b,
                            'all_stages_nodes': c, 'all_stages_free_coords': d}
    out['xstar_free_coordinates_on_grid'] = offgrid
    tot = [0, 0]
    for e in ('E1', 'E2', 'E3'):
        last = last_stage(st[e])
        info = {r['key']: r for r in runs[e]}
        for key, r in last.items():
            if int(info[key]['kappa_target']) >= 4:
                tot[0] += int(r['xstar_nodes_free'])
                tot[1] += int(r['n_free'])
    out['xstar_free_on_last_grid_E1_E3_kappa_ge_4'] = {'nodes': tot[0], 'free_coordinates': tot[1],
                                                       'fraction': tot[0] / tot[1]}

    # ---------------- E2 and E3 plateaus
    for e, par in (('E2', 'kappa_target'), ('E3', 'n')):
        nodes, rad = plateau(st[e], 'max_nodes_free'), plateau(st[e], 'radius_over_h_free')
        last = last_stage(st[e])
        agg = defaultdict(lambda: defaultdict(list))
        for r in runs[e]:
            k = (r['method'], int(r['kappa_target']), int(r[par]))
            agg[k]['nodes'].append(nodes.get(r['key']))
            agg[k]['radius_over_h'].append(rad.get(r['key']))
            h = float(last[r['key']]['h'])
            agg[k]['gap_over_Lnh2_last'].append(float(last[r['key']]['gap_U_minus_beta']) / (2 * int(r['n']) * h * h))
            agg[k]['status'].append(r['status'])
            agg[k]['final_trial'].append(r['final_trial'])
            agg[k]['theta'].append(r['theta'])
            agg[k]['kappa'].append((float(r['kappa_lb']), float(r['kappa_ub'])))
            agg[k]['total_states'].append(int(r['total_states']))
        out[e] = {'runs': len(runs[e]), 'all_replays_valid': all(r['verify_valid'] == 'True' for r in runs[e]),
                  'all_enclose_fstar': all(r['fstar_enclosed'] == 'True' for r in runs[e]),
                  'kappa_ub_over_kappa_lb_max': max(float(r['kappa_ub']) / float(r['kappa_lb']) for r in runs[e]),
                  'kappa_lb_over_target_range': rng([float(r['kappa_lb']) / float(r['kappa_target']) for r in runs[e]], 4),
                  'kappa_ub_over_target_range': rng([float(r['kappa_ub']) / float(r['kappa_target']) for r in runs[e]], 4),
                  'by_method_kappa_' + par: {
                      f'{m}:k{kt}:{x}': {'median_plateau_nodes': median(v['nodes']),
                                         'median_plateau_radius_over_h': median(v['radius_over_h']),
                                         'median_last_gap_over_Lnh2': median(v['gap_over_Lnh2_last']),
                                         'theta': sorted(set(v['theta'])), 'final_trial': v['final_trial'],
                                         'status': sorted(set(v['status'])),
                                         'kappa_range': [min(a for a, _ in v['kappa']), max(b for _, b in v['kappa'])],
                                         'median_total_states': median(v['total_states'])}
                      for (m, kt, x), v in sorted(agg.items())}}

    # ---------------- CT runs: was any trial aborted by the cap?
    # A trial ends by success, by its stage limit, or by an abort before a
    # table is formed. Aborts show up as skipped trial indices, as a failed
    # trial with fewer stages than the others, or as attempted > completed.
    ct_runs = ([r for r in runs['E2'] if r['method'] == 'default_schedule'] + read(RES / 'E5_grid_runs.csv'))
    ct_stages = [r for r in st['E2'] if r['method'] == 'default_schedule'] + read(RES / 'E5_grid_stages.csv')
    by = defaultdict(list)
    for r in ct_stages:
        by[r['key']].append(int(r['trial']))
    suspicious, restarts = [], 0
    for r in ct_runs:
        counts = defaultdict(int)
        for t in by[r['key']]:
            counts[t] += 1
        ts = sorted(counts)
        restarts += len(ts) - 1
        if (ts != list(range(2, ts[-1] + 1)) or r['attempted_stages'] != r['completed_stages']
                or len({counts[t] for t in ts[:-1]}) > 1):
            suspicious.append(r['key'])
    out['CT_trial_aborts'] = {'runs_checked': len(ct_runs), 'restarts': restarts,
                              'runs_with_possible_abort': suspicious}

    # ---------------- E4
    rows = read(RES / 'E4_exact.csv')
    ex = [r for r in rows if r['status'] == 'exact']
    out['E4'] = {'runs': len(rows), 'exact': len(ex),
                 'exact_matches_oracle': sum(r['value_matches_oracle'] == 'True' for r in rows),
                 'exact_point_optimal': sum(r['point_is_optimal'] == 'True' for r in ex),
                 'all_replays_valid': all(r['verify_valid'] == 'True' for r in rows),
                 'not_exact': [(r['name'], r['status'], r['final_gap_bits'], r['required_gap_bits_code'],
                                r['required_gap_bits_lemma']) for r in rows if r['status'] != 'exact'],
                 'stages_bits_code_bits_lemma': sorted((int(r['stages']), round(float(r['required_gap_bits_code']), 1),
                                                        round(float(r['required_gap_bits_lemma']), 1), r['name'],
                                                        int(r['rounds'])) for r in rows),
                 'bits_code_range_exact': rng([float(r['required_gap_bits_code']) for r in ex], 1),
                 'bits_lemma_range_exact': rng([float(r['required_gap_bits_lemma']) for r in ex], 1),
                 'bits_code_range_all': rng([float(r['required_gap_bits_code']) for r in rows], 1),
                 'bits_lemma_range_all': rng([float(r['required_gap_bits_lemma']) for r in rows], 1),
                 'accepted_point_from_recovery_proposal': sum(r['point_from_recovery_proposal'] == 'True' for r in ex),
                 'replay_over_solve': rng([float(r['verify_wall_s']) / float(r['solve_wall_s'])
                                           for r in rows if float(r['solve_wall_s']) >= 0.1], 2)}

    # ---------------- E5 and E5V
    scip, grid = read(RES / 'E5_scip.csv'), read(RES / 'E5_grid_runs.csv')
    g = {(r['kind'], r['n'], r['seed']): r for r in grid}
    groups = defaultdict(list)
    for r in scip:
        gr = g[(r['kind'], r['n'], r['seed'])]
        groups[f"{r['kind']}{r['n']}"].append({
            'scip_status': r['status'], 'scip_wall_s': round(float(r['wall_s']), 2),
            'scip_dual_bound': float(r['dual_bound']), 'scip_primal_bound': float(r['primal_bound']),
            'scip_exact_gap': float(r['exact_gap']), 'scip_point_excess': float(r['scip_point_excess_over_fstar']),
            'interval_contains_fstar': r['interval_contains_fstar'],
            'grid_status': gr['status'], 'grid_gap': float(gr['gap']), 'grid_bag': int(gr['max_bag_size']),
            'grid_solve_s': round(float(gr['solve_wall_s']), 2),
            'grid_replay_s': round(float(gr['verify_wall_s']), 2), 'grid_trial': gr['final_trial']})
    table = {}
    for k, v in groups.items():
        table[k] = {'bag': max(x['grid_bag'] for x in v), 'max_solve': max(x['grid_solve_s'] for x in v),
                    'max_replay': max(x['grid_replay_s'] for x in v),
                    'scip_status': sorted({x['scip_status'] for x in v}),
                    'scip_max_time': max(x['scip_wall_s'] for x in v),
                    'scip_exact_gap_range': [min(x['scip_exact_gap'] for x in v), max(x['scip_exact_gap'] for x in v)],
                    'scip_dual_range': [min(x['scip_dual_bound'] for x in v), max(x['scip_dual_bound'] for x in v)],
                    'grid_trials': [x['grid_trial'] for x in v]}
    gapreached = [r for r in scip if r['status'] != 'timelimit']
    out['E5'] = {'table': table, 'groups': groups,
                 'scip_runs': len(scip),
                 'scip_reported_gap_reached': len(gapreached),
                 'scip_exact_gap_range_when_reported_reached': rng([float(r['exact_gap']) for r in gapreached], 9),
                 'scip_interval_contains_fstar': sum(r['interval_contains_fstar'] == 'True' for r in scip),
                 'scip_primal_bound_below_fstar': sum(r['primal_bound_below_fstar'] == 'True' for r in scip),
                 'scip_primal_shortfall_range': rng([-float(r['primal_bound']) for r in scip], 9),
                 'scip_incumbent_excess_range': rng([float(r['scip_point_excess_over_fstar']) for r in scip], 18),
                 'scip_dual_bound_valid': sum(r['dual_bound_le_fstar'] == 'True' for r in scip),
                 'objective_constant_range': rng([float(r['objective_constant']) for r in scip], 1),
                 'inward_gradient_mu_range': rng([float(F(r['mu'])) for r in scip], 1),
                 'grid_all_certified': all(r['status'] == 'certified' for r in grid),
                 'grid_replays_valid': all(r['verify_valid'] == 'True' for r in grid),
                 'grid_gap_max': max(float(r['gap']) for r in grid),
                 'grid_replay_over_solve': rng([float(r['verify_wall_s']) / float(r['solve_wall_s']) for r in grid], 2)}
    var = read(RES / 'E5V_scip_variants.csv')
    vs = defaultdict(lambda: defaultdict(list))
    for r in var:
        vs[r['variant']][f"{r['kind']}{r['n']}"].append(r['status'])
    out['E5V'] = {'statuses': {v: {k: sorted(set(x)) for k, x in d.items()} for v, d in vs.items()},
                  'interval_contains_fstar': {v: sum(r['interval_contains_fstar'] == 'True' for r in var
                                                     if r['variant'] == v) for v in vs},
                  'runs': {v: sum(1 for r in var if r['variant'] == v) for v in vs},
                  'dual_at_limit_range': {v: rng([float(r['dual_bound']) for r in var if r['variant'] == v
                                                  and r['status'] == 'timelimit'], 9) for v in vs}}

    # ---------------- S1
    rows = read(RES / 'S1_localized.csv')
    acc = [r for r in rows if r['status'] == 'accepted']
    hard = sorted(rows, key=lambda r: -int(r['height_rule_stages']))[:5]
    out['S1'] = {'runs': len(rows), 'accepted': len(acc),
                 'n_range': rng([int(r['n']) for r in rows], 0),
                 'integer_coordinates': sorted({int(r['n_integer']) for r in rows}),
                 'accepted_on_full_box': sum(r['local_accepted_on_full_box'] == 'True' for r in acc),
                 'max_first_stage_index_0based': max(int(r['local_first_stage']) for r in acc),
                 'disagreements_with_EX': sum(r['values_agree'] == 'False' for r in rows),
                 'agreements_with_EX': sum(r['values_agree'] == 'True' for r in rows),
                 'oracle_checked': sum(1 for r in rows if r.get('oracle_value')),
                 'oracle_mismatches': sum(r.get('local_matches_oracle') == 'False' for r in rows),
                 'EX_status': sorted({r['height_rule_status'] for r in rows}),
                 'EX_stages_range': rng([int(r['height_rule_stages']) for r in rows], 0),
                 'max_local_time_to_acceptance_s': max(float(r['local_time_to_acceptance_s']) for r in acc),
                 'face_candidate_accepted': sum(r['face_first_stage'] not in ('', 'None') for r in rows),
                 'face_candidate_max_stage_index_0based': max(int(r['face_first_stage']) for r in rows
                                                              if r['face_first_stage'] not in ('', 'None')),
                 'face_candidate_agrees_with_EX': sum(r['face_agrees_with_EX'] == 'True' for r in rows),
                 'face_and_incumbent_rules_accept_same_instances': all(
                     (r['face_first_stage'] in ('', 'None')) == (r['local_first_stage'] in ('', 'None'))
                     for r in rows),
                 'not_accepted': [r['name'] for r in rows if r['status'] != 'accepted'],
                 'five_most_EX_stages': [{k: r.get(k) for k in (
                     'name', 'height_rule_stages', 'height_rule_rounds', 'omega_bits_lemma', 'omega_bits_code',
                     'single_run_stages_lemma', 'single_run_stages_code', 'single_run_trials_lemma',
                     'single_run_trials_code', 'local_first_stage')} for r in hard],
                 'single_run_stages_lemma_range_top5': rng([int(r['single_run_stages_lemma']) for r in hard], 0),
                 'single_run_stages_code_range_top5': rng([int(r['single_run_stages_code']) for r in hard], 0),
                 'single_run_stages_lemma_range_all': rng([int(r['single_run_stages_lemma']) for r in rows
                                                           if r.get('single_run_stages_lemma')], 0),
                 'omega_bits_lemma_range': rng([float(r['omega_bits_lemma']) for r in rows if r.get('omega_bits_lemma')], 1),
                 'omega_bits_code_range': rng([float(r['omega_bits_code']) for r in rows if r.get('omega_bits_code')], 1)}

    # ---------------- E6
    rows = read(RES / 'E6_random_growth.csv')
    inst = {}
    for r in rows:
        inst.setdefault(r['name'], {'kind': r['kind'], 'n': int(r['n']), 'proof': r['optimality_proof'],
                                    'growth': r['growth_status'], 'kappa_lb': r['kappa_lb'],
                                    'kappa_ub': r['kappa_ub'], 'lambda_min_H': float(r['lambda_min_H']),
                                    'n_free': r['n_free'], 'oracle': r['matches_oracle'], 'q': {}})
        inst[r['name']]['q'][int(r['q'])] = {
            'status': r['status'], 'max_nodes': int(r['max_nodes']), 'stages': int(r['stages']),
            'final_trial': r['final_trial'], 'trials': int(r['trials']), 'replay_valid': r['replay_valid'],
            'solve_s': float(r['solve_s']), 'replay_s': float(r['replay_s']),
            'xhat_nodes_free_last_stage': r['xhat_nodes_free_last_stage'], 'table_states': int(r['table_states'])}
    grp = {}
    for kind in ('path', 'band2'):
        for n in (8, 12, 16, 24):
            sel = [v for v in inst.values() if v['kind'] == kind and v['n'] == n]
            if not sel:
                continue
            cert = [v for v in sel if v['growth'] == 'certified']
            grp[f'{kind}{n}'] = {
                'instances': len(sel), 'growth_certified': len(cert),
                'localized_proof': sum(v['proof'] == 'localized' for v in sel),
                'unproved': sum(v['proof'] in ('', 'None', None) for v in sel),
                'kappa_brackets': [(round(float(v['kappa_lb']), 2), round(float(v['kappa_ub']), 2)) for v in cert],
                'nonconvex': sum(v['lambda_min_H'] < 0 for v in sel),
                'max_nodes_by_q': {q: max(v['q'][q]['max_nodes'] for v in sel) for q in sorted(sel[0]['q'])},
                'median_max_nodes_by_q': {q: median(v['q'][q]['max_nodes'] for v in sel) for q in sorted(sel[0]['q'])},
                'stages_by_q': {q: rng([v['q'][q]['stages'] for v in sel], 0) for q in sorted(sel[0]['q'])},
                'trials_at_q50': [v['q'][50]['trials'] for v in sel],
                'all_certified_runs': all(x['status'] == 'certified' for v in sel for x in v['q'].values()),
                'all_replays_valid': all(x['replay_valid'] == 'True' for v in sel for x in v['q'].values()),
                'max_solve_s': max(x['solve_s'] for v in sel for x in v['q'].values()),
                'xhat_free_on_last_grid': sum(int(x['xhat_nodes_free_last_stage'] or 0) for v in sel
                                              for x in v['q'].values()),
                'free_coords_total_times_runs': sum(int(v['n_free'] or 0) * len(v['q']) for v in sel)}
    allinst = list(inst.values())
    q50_nodes = q50_free = 0
    for r in rows:
        if int(r['q']) == 50 and r['xhat_nodes_free_last_stage'] not in ('', 'None'):
            q50_nodes += int(r['xhat_nodes_free_last_stage'])
            q50_free += int(r['n_free'])
    out['E6'] = {'instances': len(allinst), 'groups': grp,
                 'growth_certified': sum(v['growth'] == 'certified' for v in allinst),
                 'localized_proof': sum(v['proof'] == 'localized' for v in allinst),
                 'growth_failure_reasons': sorted({v['growth'] for v in allinst if v['growth'] != 'certified'}),
                 'oracle_checked': sum(v['oracle'] in ('True', 'False') for v in allinst),
                 'oracle_matches': sum(v['oracle'] == 'True' for v in allinst),
                 'nonconvex': sum(v['lambda_min_H'] < 0 for v in allinst),
                 'kappa_brackets_certified_rounded_outward': sorted(
                     (math.floor(float(v['kappa_lb']) * 10) / 10, math.ceil(float(v['kappa_ub']) * 10) / 10)
                     for v in allinst if v['growth'] == 'certified'),
                 'xhat_free_on_last_grid_q50': [q50_nodes, q50_free],
                 'all_runs_first_trial': all(x['final_trial'] == '2' and x['trials'] == 1
                                             for v in allinst for x in v['q'].values()),
                 'max_nodes_range_by_q': {q: rng([v['q'][q]['max_nodes'] for v in allinst], 0)
                                          for q in sorted(allinst[0]['q'])},
                 'instances_with_same_max_nodes_for_all_q': sum(len({x['max_nodes'] for x in v['q'].values()}) == 1
                                                                for v in allinst),
                 'max_nodes_spread_over_q': max(max(x['max_nodes'] for x in v['q'].values())
                                                - min(x['max_nodes'] for x in v['q'].values()) for v in allinst),
                 'replay_over_solve': rng([x['replay_s'] / x['solve_s'] for v in allinst for x in v['q'].values()
                                           if x['solve_s'] >= 0.1], 2)}

    # ---------------- replay cost over all grid certificates with solve time >= 0.1 s
    ratios = {}
    for e in ('E1', 'E2', 'E3'):
        ratios[e] = rng([float(r['verify_wall_s']) / float(r['solve_wall_s']) for r in runs[e]
                         if float(r['solve_wall_s']) >= 0.1], 2)
    ratios['E4'] = out['E4']['replay_over_solve']
    ratios['E5'] = out['E5']['grid_replay_over_solve']
    ratios['E6'] = out['E6']['replay_over_solve']
    chain = read(HERE / 'chain' / 'results.csv')
    ratios['chain'] = rng([float(r['replay_s']) / float(r['solve_s']) for r in chain if float(r['solve_s']) >= 0.1], 2)
    rec = read(HERE / 'recourse' / 'results.csv')
    ratios['recourse_plain_grid'] = rng([float(r['replay_s']) / float(r['solve_s']) for r in rec
                                         if r['method'] == 'grid' and float(r['solve_s']) >= 0.1], 2)
    allr = [x for k, v in ratios.items() if v for x in v]
    out['replay_over_solve_time'] = {'by_experiment': ratios, 'overall': [min(allr), max(allr)],
                                     'note': 'main checker, runs with solve time >= 0.1 s'}

    # ---------------- chain warm start, QPLIB
    ws = HERE / 'chain' / 'results_warmstart.csv'
    if ws.exists():
        w = {r['m']: r for r in read(ws)}
        out['chain_warmstart'] = {m: {'stages': (int(r['stages']), int(w[m]['stages'])),
                                      'max_nodes': (int(r['max_grid_nodes']), int(w[m]['max_grid_nodes'])),
                                      'states_ratio': round(int(w[m]['table_states']) / int(r['table_states']), 3),
                                      'initial_upper_warm': w[m]['initial_upper'],
                                      'replay_ok': w[m]['replay_ok']}
                                  for m, r in ((r['m'], r) for r in chain) if m in w}
    qp = HERE / 'qplib' / 'results.json'
    if qp.exists():
        out['qplib'] = json.loads(qp.read_text())['instances']

    env = json.loads((RES / 'environment.json').read_text())
    out['environment'] = {k: env.get(k) for k in ('cpu_model', 'nproc', 'loadavg', 'loadavg_end', 'wall_s',
                                                  'sum_task_wall_s', 'jobs', 'n_tasks', 'failures', 'scip',
                                                  'pyscipopt', 'python', 'started', 'finished')}
    (RES / 'summary.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
    print(json.dumps(out, indent=1, default=str)[:30000])


if __name__ == '__main__':
    main()
