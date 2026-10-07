"""Independent frozen-study arithmetic audit; no optimization or analysis imports."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import re
import statistics
import tarfile

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
DEFAULT = LAB / 'results/lbesh_development'


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def artifact_directory(root, recorded):
    """Locate frozen run artifacts below the selected exported result root."""
    _, separator, suffix = str(recorded).partition('/results/lbesh_development/')
    assert separator and suffix, ('Unexpected recorded artifact path', recorded)
    relative = Path(suffix)
    assert not relative.is_absolute() and '..' not in relative.parts, recorded
    return Path(root) / relative


def verify_source_archive(root, manifest):
    """Check the exported source bytes independently of original run metadata."""
    archive = root / manifest['source_archive']
    assert digest(archive) == manifest['archive_sha256'], 'Source archive hash mismatch'
    with tarfile.open(archive, 'r:gz') as stream:
        members = stream.getmembers()
        names = [item.name for item in members]
        assert len(names) == len(set(names)), 'Duplicate source archive members'
        assert set(names) == set(manifest['files']), 'Source archive member mismatch'
        for item in members:
            assert item.isfile() and not Path(item.name).is_absolute(), item.name
            assert all(part not in ('', '.', '..') for part in item.name.split('/')), item.name
            data = stream.extractfile(item).read()
            assert hashlib.sha256(data).hexdigest() == manifest['files'][item.name], item.name


def finite(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def tolerance(x):
    return 1e-6 + 1e-4 * max(1, abs(x))


def shifted(values):
    return math.expm1(statistics.fmean(math.log1p(x) for x in values)) if values else None


def dimensions(name):
    if name.startswith('lbesh.'):
        _, family, size, seed = name.split('.')
        return family, size, 'pilot' if seed == 's104729' else 'held_out'
    return 'legacy', 'legacy', 'legacy'


def cohorts(names):
    yield 'all', 'all', names
    for pos, label in enumerate(('family', 'size', 'split')):
        for val in sorted({dimensions(n)[pos] for n in names}):
            yield label, val, [n for n in names if dimensions(n)[pos] == val]


def check_metadata(meta, freeze):
    assert meta and meta['source_sha256'], 'Missing source metadata'
    for path, value in meta['source_sha256'].items():
        assert freeze['code/minlp_solver_lab/' + path] == value, ('Source differs from freeze', path)
    assert meta['uv_lock_sha256'] == freeze['code/minlp_solver_lab/uv.lock']


def load_batch(path, expected, freeze):
    schedule = read(Path(str(path) + '.runs/schedule.json'))
    assert schedule['instances'] == expected['instances'], ('Instance schedule', path)
    assert schedule['methods'] == expected['methods'], ('Method schedule', path)
    assert (schedule['time_limit'], schedule['wall_limit'], schedule['threads']) == (120, 150, 1)
    assert 1 <= schedule['parallel'] <= 6
    seed = expected.get('order_seed')
    if seed is None:
        cmd = expected['command']; seed = int(cmd[cmd.index('--order-seed') + 1])
    assert schedule['order_seed'] == seed
    ordered = list(itertools.product(schedule['instances'], schedule['methods']))
    random.Random(seed).shuffle(ordered)
    assert list(map(tuple, schedule['ordered_jobs'])) == ordered, 'Randomized order differs'
    records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    pairs = [(r['instance'], r['method']) for r in records]
    assert Counter(pairs) == Counter(ordered), f'{path.name}: incomplete/duplicate/unscheduled ({len(records)}/{len(ordered)})'
    check_metadata(schedule['metadata'], freeze)
    for row in records:
        if row.get('metadata'):
            check_metadata(row['metadata'], freeze)
            assert row['metadata'] == schedule['metadata'], ('Worker environment changed', row['instance'], row['method'])
        else:
            assert row.get('outcome') != 'completed', 'Completed worker has no metadata'
        assert row['wall_limit'] == 150 and row['threads'] == 1
        assert row['solver_time_limit'] == 120
        if row['instance'].startswith('lbesh.') and row.get('instance_metadata'):
            meta = row['instance_metadata']
            assert tuple(meta[k] for k in ('family', 'size', 'split')) == dimensions(row['instance'])
        row['_file'] = path.stem
    return schedule, records


def revalidate(row):
    from gdp_instances import build as legacy_build
    from lbesh_research.instances import build
    from lbesh_research.validation import validate_witness
    name = row['instance']
    model = build(name) if name.startswith('lbesh.') else legacy_build(name)
    result = validate_witness(model, row['witness'], reported_objective=row.get('reported_objective'))
    assert result['feasible'] == row['validation']['feasible'], ('Revalidation disagreement', name, row['method'])
    if result['feasible']:
        assert math.isclose(result['objective'], row['validation']['objective'], abs_tol=1e-9, rel_tol=1e-12)
    return result


def classify(records, references, fresh):
    best = {}
    senses = {}
    for row in records:
        val = revalidate(row) if fresh and row.get('witness') else (row.get('validation') or {})
        obj = val.get('objective')
        row['_feasible'] = val.get('feasible') is True and finite(obj)
        row['_objective'] = obj
        sense = row.get('objective_sense', val.get('objective_sense'))
        if row['_feasible']:
            assert sense in ('minimize', 'maximize')
            assert senses.setdefault(row['instance'], sense) == sense
            sign = 1 if sense == 'minimize' else -1
            best[row['instance']] = min(best.get(row['instance'], math.inf), sign * obj)
    for name, obj in references:
        best[name] = min(best.get(name, math.inf), obj)
    contradictions = []
    for row in records:
        name = row['instance']; bound = row.get('dual_bound')
        sign = 1 if senses.get(name, row.get('objective_sense')) == 'minimize' else -1
        inconsistent = row.get('bound_valid') is True and finite(bound) and name in best and sign * bound > best[name] + tolerance(best[name])
        infeasible = 'infeasible' in str(row.get('raw_status', '')).lower() and name in best
        if inconsistent or infeasible:
            contradictions.append([row['_file'], name, row['method'], 'bound' if inconsistent else 'infeasible'])
        row['_solved'] = (row['_feasible'] and row.get('outcome') == 'completed' and row.get('bound_valid') is True
                          and finite(bound) and abs(row['_objective'] - bound) <= tolerance(row['_objective'])
                          and not inconsistent and not infeasible)
    return contradictions


def tables(batches):
    summaries, pairs = [], []
    for label, schedule, records in batches:
        lookup = {(r['instance'], r['method']): r for r in records}
        def time(row):
            assert finite(row.get('wall_time')) and row['wall_time'] >= 0
            return min(row['wall_time'], 150)
        for dim, group, names in cohorts(schedule['instances']):
            base = dict(run=label, dimension=dim, group=group)
            for method in schedule['methods']:
                rows = [lookup[n, method] for n in names]
                penalized = [time(r) if r['_solved'] else 1500 for r in rows]
                summaries.append(dict(**base, method=method, scheduled=len(rows), numerical_solved=sum(r['_solved'] for r in rows),
                    validated_feasible=sum(r['_feasible'] for r in rows), par10_mean=statistics.fmean(penalized), par10_shifted_geomean=shifted(penalized)))
            for esh in schedule['methods']:
                if not esh.startswith('lbesh-esh-'): continue
                ecp = esh.replace('-esh-', '-ecp-', 1)
                if ecp not in schedule['methods']: continue
                common = [n for n in names if lookup[n, esh]['_solved'] and lookup[n, ecp]['_solved']]
                a, b = [[time(lookup[n, m]) for n in common] for m in (esh, ecp)]
                ga, gb = shifted(a), shifted(b)
                bits = esh.split('-')
                pairs.append(dict(**base, formulation=bits[2], tree=bits[3], variant='-'.join(bits[4:]) or 'default',
                    scheduled=len(names), common_solved=len(common), common_instances=common,
                    esh_solved=sum(lookup[n, esh]['_solved'] for n in names), ecp_solved=sum(lookup[n, ecp]['_solved'] for n in names),
                    esh_shifted_geomean=ga, ecp_shifted_geomean=gb, esh_over_ecp_shifted_geomean=ga/gb if gb else None,
                    esh_faster=sum(x < y for x,y in zip(a,b)), ecp_faster=sum(y < x for x,y in zip(a,b))))
    return summaries, pairs


def audit_references(root, primary, freeze, fresh):
    roots_path = root / 'general_conic_roots_frozen_v1.jsonl'
    enum_path = root / 'general_conic_enumeration_frozen_v1.jsonl'
    roots, enums = [[json.loads(s) for s in p.read_text().splitlines() if s.strip()] for p in (roots_path, enum_path)]
    supported = [n for n in primary['instances'] if '.trig.' not in n]
    small = [n for n in supported if '.small.' in n]
    assert Counter(r['name'] for r in roots) == Counter(supported)
    assert Counter(r['name'] for r in enums) == Counter(small)
    fixed = []
    for group in enums:
        assert group['assignments'] == 27 and len(group['rows']) == 27
        assert Counter(tuple(r['modes']) for r in group['rows']) == Counter(itertools.product(range(3), repeat=3))
        assert all(r['name'] == group['name'] for r in group['rows'])
        unresolved = sum(r['status'] not in ('optimal','infeasible') for r in group['rows'])
        assert unresolved == group['unresolved_assignments']
        feasible = [r for r in group['rows'] if r['status'] == 'optimal']
        if feasible: assert group['obj'] == min(r['obj'] for r in feasible)
        fixed.extend(group['rows'])
    feasible_refs = []
    invalid_refs = []
    missing_optimal_witnesses = []
    for row in roots + fixed:
        assert row['bound_certified'] is False
        assert row['bound_kind'] == 'floating_point_conic_dual_estimate'
        assert row['threads'] == 1
        assert row['versions']['cvxpy'] == '1.7.3' and row['versions']['clarabel'] == '0.11.1'
        for filename in ('conic_reference.py','instances.py'):
            assert row['source_sha256'][filename] == freeze['code/minlp_solver_lab/lbesh_research/' + filename]
        assert row['environment_lock_sha256'] == freeze['code/minlp_solver_lab/lbesh_research/conic_reference_env/uv.lock']
        if row['modes'] is not None and row['status'] in ('optimal','optimal_inaccurate') and not row.get('witness'):
            missing_optimal_witnesses.append(dict(name=row['name'],modes=row['modes'],status=row['status']))
        if row['modes'] is not None and row.get('witness') and fresh:
            from lbesh_research.instances import build
            from lbesh_research.validation import validate_witness
            variables = row['witness']
            booleans = {k.replace('.binary_indicator_var','.indicator_var'): bool(round(v)) for k,v in variables.items() if k.endswith('.binary_indicator_var')}
            result = validate_witness(build(row['name']), dict(variables=variables, booleans=booleans), reported_objective=row['obj'])
            if result['feasible']: feasible_refs.append((row['name'], result['objective']))
            else: invalid_refs.append(dict(name=row['name'], modes=row['modes'], status=row['status'], issues=result['issues']))
    return dict(roots=len(roots), enumerations=len(enums), assignments=len(fixed),
                root_statuses=dict(Counter(r['status'] for r in roots)), fixed_statuses=dict(Counter(r['status'] for r in fixed)),
                validated_fixed_witnesses=len(feasible_refs), invalid_fixed_witnesses=len(invalid_refs),
                invalid_fixed_witness_details=invalid_refs, missing_optimal_witnesses=missing_optimal_witnesses,
                fixed_validation_performed=fresh), feasible_refs


def audit_sensitivity(path, root, freeze):
    plan = read(root/'gurobi_trig_sensitivity_plan_v1.json')
    expected = {f'lbesh.trig.{size}.s{seed}' for size in ('small','medium','large') for seed in (104729,130363,155921)}
    assert set(plan['instances']) == expected and len(plan['instances']) == 9
    assert plan['methods'] == ['gams-gurobi-bigm-feas1e8']
    assert plan['solver_options'] == {'feasibilitytol': 1e-8}
    assert plan['validator_tolerances'] == {'absolute':1e-6,'relative':1e-7,'integrality':1e-6}
    assert plan['primary_results_unchanged'] is True
    assert digest(LAB/'lbesh_gurobi_sensitivity.py') == plan['metadata']['supplementary_wrapper_sha256']
    assert plan['metadata']['copied_adapter_source_sha256'] == freeze['code/minlp_solver_lab/lbesh_research/benchmark.py']
    schedule, records = load_batch(path, plan, freeze)
    for key in ('metadata','solver_options','validator_tolerances','primary_results_unchanged'):
        assert schedule[key] == plan[key], ('Sensitivity plan mismatch',key)
    versions = read(root/'runtime_versions.json')
    for row in records:
        assert row.get('metadata') == plan['metadata'], 'Sensitivity must retain wrapper provenance for every outcome'
        if row.get('outcome') != 'completed': continue
        assert row['options']['solver_options'] == plan['solver_options']
        assert row['effective_feasibilitytol'] == 1e-8
        assert row['native_versions'] == {'gams':versions['gams_executable'],'gurobi':versions['gams_gurobi']}
        assert row['option_file_sha256'] == hashlib.sha256(b'feasibilitytol 1e-8\n').hexdigest()
        artifacts = artifact_directory(root, row['artifacts'])
        log = (artifacts/'gams.log').read_text()
        match = re.search(r'(?m)^\s*FeasibilityTol\s+([0-9.eE+-]+)\s*$',log)
        assert match and float(match.group(1)) == 1e-8
        assert f"GAMS {versions['gams_executable']}" in log
        assert f"Gurobi Optimizer version {versions['gams_gurobi']}" in log
        assert row['dual_bound'] == row['native_gams']['OBJEST']
    return path.stem, schedule, records


def audit_initialization(path, root, freeze):
    plan = read(root/'legacy_initialization_plan_v2.json')
    farms = ['pyomo.farm_layout.'+s for s in ('FLay02','FLay03','FLay03_alt_1','FLay03_alt_2','FLay04','FLay05','FLay06')]
    assert plan['instances'] == farms + ['gdplib.batch_processing']
    assert plan['methods'] == ['gams-'+s+'-bigm-initialized' for s in ('shot','gurobi','scip')]
    assert digest(LAB/'lbesh_legacy_initialization.py') == plan['metadata']['supplementary_wrapper_sha256']
    source_manifest = read(root/'source_v1_manifest.json')
    historical_manifest_sha256 = source_manifest.get('original_manifest_sha256', digest(root/'source_v1_manifest.json'))
    assert historical_manifest_sha256 == plan['metadata']['source_manifest_sha256']
    assert freeze['code/minlp_solver_lab/lbesh_research/benchmark.py'] == plan['metadata']['copied_adapter_source_sha256']
    assert plan['validator_tolerances'] == {'absolute':1e-6,'relative':1e-7,'integrality':1e-6}
    schedule, records = load_batch(path, plan, freeze)
    for key in ('metadata','initialization','unchanged','validator_tolerances'):
        assert schedule[key] == plan[key], ('Initialization schedule changed',key)
    versions = read(root/'runtime_versions.json')
    from gdp_instances import build
    import pyomo.environ as pe
    from pyomo.gdp import Disjunct
    from pyomo.core.expr.visitor import identify_variables
    for name, changes in plan['initialization_by_instance'].items():
        model=build(name)
        expected_names = {f'plot_width[{i}]' for i in model.plots} if name in farms else {f'storageTankSize_log[{model.STAGES.last()}]'}
        assert {c['variable'] for c in changes} == expected_names
        for change in changes:
            var=model.find_component(change['variable'])
            assert var.value == change['old_value'] and list(var.bounds) == change['original_variable_bounds'] and not var.fixed
            if name in farms:
                row=model.find_component(change['source_constraint'])
                assert row.active and row.body is var and pe.value(row.lower) == change['new_value'] > 0
            else:
                assert change['source_constraint'] is None and change['new_value'] == var.lb
                for kind in (pe.Constraint,pe.Objective,pe.Expression,pe.LogicalConstraint):
                    for component in model.component_data_objects(kind,active=None,descend_into=(pe.Block,Disjunct)):
                        assert all(v is not var for v in identify_variables(component.expr,include_fixed=True))
            assert change['new_value'] == change['source_lower_bound']
    for row in records:
        assert row.get('metadata') == plan['metadata']
        if 'initialization_changes' in row:
            assert row['initialization_changes'] == plan['initialization_by_instance'][row['instance']]
        if row['outcome'] != 'completed': continue
        assert row['options'] == plan['unchanged_primary_options'][row['method']]
        solver=row['method'].split('-')[1]
        assert row['native_versions']['gams'] == versions['gams_executable']
        expected_version=versions['shot' if solver=='shot' else 'gams_'+solver]
        if solver == 'shot':
            assert row['native_versions'][solver] in (None,expected_version)  # Known frozen metadata-parser limitation.
        else:
            assert row['native_versions'][solver] == expected_version
        log=(artifact_directory(root, row['artifacts'])/'gams.log').read_text()
        assert f"GAMS {versions['gams_executable']}" in log
        patterns={'shot':r'SHOT[^\n]*?version[: ]+(\d+\.\d+(?:\.\d+)?)','gurobi':r'Gurobi Optimizer version (\d+\.\d+\.\d+)','scip':r'SCIP version (\d+\.\d+\.\d+)'}
        match=re.search(patterns[solver],log,re.I)
        if solver == 'shot' and match is None:
            match=re.search(r'(?m)^\s*Version:\s*(\d+\.\d+(?:\.\d+)?)\.\s*Git hash:\s*a81275b4',log)
        assert match and match.group(1)==expected_version
        assert row['dual_bound'] == row['native_gams']['OBJEST']
    return path.stem,schedule,records


def compare(analysis_path, summary, pairs):
    analysis = read(analysis_path)
    checked = 0
    for label, ours, key in [('summary', summary, ('run','dimension','group','method')),
                             ('esh_ecp_pairs', pairs, ('run','dimension','group','formulation','tree','variant'))]:
        theirs = {tuple(r[k] for k in key): r for r in analysis[label]}
        for row in ours:
            match = theirs[tuple(row[k] for k in key)]
            for field, expected in row.items():
                actual = match[field]
                if isinstance(expected, float): assert math.isclose(expected, actual, abs_tol=1e-10, rel_tol=1e-10), (label, key, field, expected, actual)
                else: assert expected == actual, (label, key, field, expected, actual)
                checked += 1
    return checked


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT)
    parser.add_argument('--batches', nargs='+', help='Explicit complete declared benchmark subsets; not full-study acceptance')
    parser.add_argument('--legacy-initialization', type=Path)
    parser.add_argument('--main-only', action='store_true', help='Audits only complete primary; not full-study acceptance')
    parser.add_argument('--fresh-validation', action='store_true')
    parser.add_argument('--compare-analysis', type=Path)
    parser.add_argument('--sensitivity', type=Path, help='Additional declared all-nine-trig sensitivity; never replaces primary rows')
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists(), 'Use a new audit output file'
    root = args.root
    manifest = read(root/'source_v1_manifest.json')
    # Recorded workers bind the original frozen sources, not privacy edits.
    freeze = dict(manifest['files'])
    freeze.update(manifest.get('original_file_sha256', {}))
    verify_source_archive(root, manifest)
    primary = read(root/'study_plan_v1.json')['primary_schedule']
    expected_names = {f'lbesh.{family}.{size}.s{seed}' for family in ('exp','log','reciprocal','quadratic','trig','logsumexp')
                      for size in ('small','medium','large') for seed in (104729,130363,155921)
                      if family != 'logsumexp' or seed != 155921}
    assert set(primary['instances']) == expected_names and len(primary['instances']) == 51
    assert len(primary['methods']) == 13
    specs = [('main_generated_v1', primary)]
    if not args.main_only or args.batches:
        specs.extend((j['name'],j) for j in read(root/'supplementary_plan_v1.json')['jobs'] if 'instances' in j)
    if args.batches:
        assert set(args.batches) <= {label for label,_ in specs}
        specs = [(label,spec) for label,spec in specs if label in args.batches]
    batches = [(label, *load_batch(root/(label+'.jsonl'), spec, freeze)) for label,spec in specs]
    if args.sensitivity:
        batches.append(audit_sensitivity(args.sensitivity, root, freeze))
    if args.legacy_initialization:
        batches.append(audit_initialization(args.legacy_initialization,root,freeze))
    if args.fresh_validation:
        # Fresh checks require the exact exported frozen source bytes.
        for path, value in manifest['files'].items():
            if path.endswith('.py') and ('/lbesh/' in path or '/lbesh_research/' in path or path.endswith('/gdp_instances.py')):
                assert digest(REPO/path) == value, ('Current validation/model source not frozen', path)
    ref_info, refs = ({}, []) if args.main_only or args.batches else audit_references(root, primary, freeze, args.fresh_validation)
    contradictions = classify([r for _,_,rs in batches for r in rs], refs, args.fresh_validation)
    summaries, pairs = tables(batches)
    compared = compare(args.compare_analysis, summaries, pairs) if args.compare_analysis else 0
    payload = dict(scope='selected_complete_batches' if args.batches else 'primary_only' if args.main_only else 'full_declared_study',
        source_archive_sha256=manifest['archive_sha256'], audit_source_sha256=digest(Path(__file__)),
        original_model_validator_reused=args.fresh_validation, independent_arithmetic=True,
        inputs={name:dict(rows=len(rs),sha256=digest(root/(name+'.jsonl'))) for name,_,rs in batches},
        references=ref_info, contradictions=contradictions, analysis_fields_compared=compared, summary=summaries, esh_ecp_pairs=pairs)
    args.out.write_text(json.dumps(payload, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in payload.items() if k not in ('summary','esh_ecp_pairs')},indent=2))
    return 2 if contradictions or ref_info.get('invalid_fixed_witnesses') or ref_info.get('missing_optimal_witnesses') else 0


if __name__ == '__main__':
    raise SystemExit(main())
