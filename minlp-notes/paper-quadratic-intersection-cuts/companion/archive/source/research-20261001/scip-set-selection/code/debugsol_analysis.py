"""Audit archived debug-solution logs without launching SCIP.

Usage: python3 code/debugsol_analysis.py > logs/debugsol_analysis.md
Writes per-run diagnostics and corrected row activities to a JSON companion.
Count the explicit row-violation message, not parse_logs.debugsol_violation:
that field also matches unrelated diagnostics anywhere in a log.
"""
from collections import Counter
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

from parse_logs import parse
from root_analysis import load_ref
from full_analysis import reference_flags

BASE = Path(__file__).resolve().parent.parent
RUNNAME = re.compile(r'.+\.[^.]+\.s\d+\.log(?:\.gz)?$')
ROW = re.compile(r'debug: row <([^>]+)> violates debugging solution '
                 r'\(lhs=([^,]+), rhs=([^,]+), activity=\[([^,]+),([^]]+)\], '
                 r'local=(\d+), lpfeastol=([^)]*)\)')


def objective_components(inst):
    """Read only the quadratic/linear OSiL objectives diagnosed below."""
    cache = Path.home() / '.cache/minlplib/minlplib/osil'
    root = ET.parse(cache / (inst + '.osil')).getroot()
    ns = {'o': root.tag.split('}')[0][1:]}
    obj = root.find('.//o:obj', ns)
    names = [v.get('name') for v in root.find('.//o:variables', ns)]
    values = {p[0]: float(p[1]) for l in (BASE / 'sources/sol' / (inst + '.p1.sol')).read_text().splitlines()
              if len(p := l.split()) == 2}
    assert root.find('.//o:nonlinearExpressions', ns) is None
    linear = sum(float(c.text) * values.get(names[int(c.get('idx'))], 0)
                 for c in obj.findall('o:coef', ns))
    quad = sum(float(q.get('coef')) * values.get(names[int(q.get('idxOne'))], 0)
               * values.get(names[int(q.get('idxTwo'))], 0)
               for q in root.findall('.//o:qTerm', ns) if q.get('idx') == '-1')
    constant = float(obj.get('constant', '0'))
    return dict(linear=linear, quadratic=quad, constant=constant,
                actual_objective=linear + quad + constant, sol_objvar=values.get('objvar'))


def main():
    ref, tag, sense = load_ref()
    report = dict(groups={}, objective_diagnosis={})
    for inst in ('st_glmp_fp2', 'ex5_2_5', 'nvs17', 'nvs24', 'gasprod_sarawak01'):
        report['objective_diagnosis'][inst] = objective_components(inst)
    print('# Archived debug-solution audit\n')
    print('Reference-bound threshold: 1e-6 max(1, |MINLPLib reference|), with objective sense accounted for. '
          'Row counts count explicit diagnostic messages, including any repeated row. '
          'Final/root bounds use statistics in the original objective; internal debug warnings '
          'use the objective of the point actually loaded by the checker.\n')
    for directory in ('debugsol', 'debugsol_withsym'):
        folder = BASE / 'logs' / directory
        fs = sorted(folder.glob('*.log'))
        records = []
        artifacts = [f.name for f in fs if not RUNNAME.fullmatch(f.name)]
        for f in fs:
            if not RUNNAME.fullmatch(f.name):
                continue
            r = parse(str(f))
            lines = f.read_text(errors='replace').splitlines()
            counts = Counter()
            examples = {}
            rows = []
            corrected_rows = []
            for k, line in enumerate(lines):
                m = ROW.search(line)
                if m:
                    name, lhs, rhs, lo, hi, local, feastol = m.groups()
                    kind = 'intersection_row' if 'intersection_quadratic' in name else 'other_row'
                    counts[kind] += 1
                    rows.append(dict(name=name, kind=kind, message=line))
                    # All intersection-row warnings in this archive concern this
                    # model, whose nonlinear objective helper was loaded as 0.
                    if r['inst'] == 'st_glmp_fp2' and kind == 'intersection_row':
                        coef = re.search(r'([+-][0-9.eE+-]+)<t_nlobjvar>', lines[k + 1])
                        assert coef is not None
                        value = report['objective_diagnosis'][r['inst']]['quadratic']
                        shift = float(coef[1]) * value
                        corrected = dict(name=name, lhs=float(lhs), rhs=float(rhs),
                                         activity_lo=float(lo) + shift, activity_hi=float(hi) + shift,
                                         nlobjvar=value, coefficient=float(coef[1]), feastol=float(feastol))
                        corrected['violation'] = max(corrected['lhs'] - corrected['activity_lo'],
                                                     corrected['activity_hi'] - corrected['rhs'])
                        corrected_rows.append(corrected)
                elif 'ERROR:' in line:
                    if 'global lower bound' in line and 'larger than' in line:
                        kind = 'global_objective_bound'
                    elif 'local lower bound' in line and 'larger than' in line:
                        kind = 'local_objective_bound'
                    elif 'cut off in local node' in line:
                        kind = 'node_cutoff'
                    elif 'invalid global lower bound:' in line or 'invalid global upper bound:' in line:
                        kind = 'variable_bound'
                    else:
                        kind = 'other_error'
                    counts[kind] += 1
                    examples.setdefault(kind, line)
            r.update(diagnostic_counts=dict(counts), examples=examples, rows=rows, corrected_rows=corrected_rows)
            r['final_reference_flags'] = reference_flags(r, ref, tag, sense)
            sign = -1 if sense[r['inst']] == 'max' else 1
            r['root_excludes_reference'] = (r['rootdual'] is not None and
                sign * (r['rootdual'] - ref[r['inst']]) > 1e-6 * max(1, abs(ref[r['inst']])))
            r['limit'] = next(l.split(' = ')[1] for l in lines if l.startswith('limits/time = '))
            r['symmetry_disabled'] = 'misc/usesymmetry = 0' in lines
            r['unknown_variable_warning'] = any('unknown variable <' in l for l in lines)
            records.append(r)
        report['groups'][directory] = dict(records=records, artifacts=artifacts)
        if directory == 'debugsol':
            insts = [l.strip() for l in (BASE / 'logs/testset_full.txt').read_text().splitlines() if l.strip()]
            assert len(records) == 300
            assert {(r['inst'], r['setting'], r['seed']) for r in records} == {
                (i, s, 0) for i in insts for s in ('scip', 'corner', 'eff', 'cornerS', 'effS')}
            assert all(r['symmetry_disabled'] for r in records)
        print(f'## {directory}\n')
        print(f'{len(records)} runs; limits {dict(Counter(r["limit"] for r in records))}; '
              f'return codes {dict(Counter(r["returncode"] for r in records))}.')
        print('Non-run artifacts:', ', '.join(artifacts))
        print('Statuses:', dict(Counter(r['status'] for r in records)))
        print('\n| setting | runs | intersection row messages / runs | other row messages / runs | global objective warnings / runs | local objective warnings / runs | node cutoff messages / runs | any ERROR runs | rc not 0 | final dual excludes reference | root dual excludes reference |')
        print('|---|---|---|---|---|---|---|---|---|---|---|')
        for s in ('scip', 'corner', 'eff', 'cornerS', 'effS'):
            rs = [r for r in records if r['setting'] == s]
            if not rs:
                continue
            cells = []
            for kind in ('intersection_row', 'other_row', 'global_objective_bound', 'local_objective_bound', 'node_cutoff'):
                values = [r['diagnostic_counts'].get(kind, 0) for r in rs]
                cells.append(f'{sum(values)} / {sum(v > 0 for v in values)}')
            print(f'| {s} | {len(rs)} | ' + ' | '.join(cells) +
                  f" | {sum(r['error'] for r in rs)} | {sum(r['returncode'] != '0' for r in rs)} | "
                  f"{sum('dual excludes feasible reference' in r['final_reference_flags'] for r in rs)} | "
                  f"{sum(r['root_excludes_reference'] for r in rs)} |")
        print('\n### Runs with diagnostics or reference flags\n')
        print('| log | diagnostic message counts | reference flags | rc |')
        print('|---|---|---|---|')
        for r in records:
            if r['diagnostic_counts'] or r['final_reference_flags'] or r['returncode'] != '0':
                print(f"| {r['log']} | {r['diagnostic_counts']} | {r['final_reference_flags']} | {r['returncode']} |")
        print('\nUnknown-variable warnings in', sum(r['unknown_variable_warning'] for r in records), 'runs.')
        print('Final dual exclusions of MINLPLib:', sum('dual excludes feasible reference' in r['final_reference_flags'] for r in records))
        print('Root dual exclusions of MINLPLib:', sum(r['root_excludes_reference'] for r in records))
        print('Global objective-warning runs:', sum(r['diagnostic_counts'].get('global_objective_bound', 0) > 0 for r in records))
        print('Global objective-warning instances:', sorted({r['inst'] for r in records if r['diagnostic_counts'].get('global_objective_bound', 0)}))
        print('\n### Intersection rows after correcting st_glmp_fp2 nlobjvar\n')
        print('| log | raw intersection messages | re-evaluated | still violates by > LP feastol | largest corrected violation (negative = slack) |')
        print('|---|---|---|---|---|')
        for r in records:
            if r['corrected_rows']:
                rows = r['corrected_rows']
                print(f"| {r['log']} | {r['diagnostic_counts']['intersection_row']} | {len(rows)} | "
                      f"{sum(c['violation'] > c['feastol'] for c in rows)} | {max(c['violation'] for c in rows):.12g} |")
    print('\n## Objective mapping diagnosis\n')
    print('| instance | original linear part at solution | quadratic part | constant | actual solution objective | objvar in solution file |')
    print('|---|---|---|---|---|---|')
    for i, c in report['objective_diagnosis'].items():
        print(f'| {i} | {c["linear"]:.14g} | {c["quadratic"]:.14g} | {c["constant"]:.14g} | {c["actual_objective"]:.14g} | {c["sol_objvar"]:.14g} |')
    print('\nSCIP reader_osil.c names generated helpers nlobjvar and objconstvar. '
          'debug.c ignores unknown names in solution files, defaults missing original values to 0, '
          'and computes its reference objective from loaded linear objective coefficients. '
          'Thus these files do not supply the nonlinear/constant helper values. '
          'st_glmp_fp2 rows are re-evaluated above with nlobjvar=7.6275; '
          'other row, variable-bound and node diagnostics are not certified harmless by this analysis. '
          'A clean whole-run validity check would require correctly mapped helper values.\n')
    inventory = Counter()
    seed0_full = []
    for f in sorted((BASE / 'logs').rglob('*.s0.log')):
        txt = f.read_text(errors='replace')
        if 'set misc debugsol' in txt or 'misc/debugsol =' in txt:
            inventory['debug-solution'] += 1
        elif re.search(r'^limits/nodes = 1$', txt, re.M):
            inventory['root only'] += 1
        elif 'SCIP version' in txt:
            inventory['ordinary full solve'] += 1
            seed0_full.append(str(f.relative_to(BASE)))
    report['seed0_inventory'] = dict(counts=dict(inventory), ordinary_full_logs=seed0_full)
    print('Seed-0 archived run-log inventory:', dict(inventory))
    print('Ordinary full-solve seed-0 logs:', seed0_full)
    def clean(v):
        if isinstance(v, dict):
            return {k: clean(x) for k, x in v.items()}
        if isinstance(v, list):
            return [clean(x) for x in v]
        if isinstance(v, float) and (v == float('inf') or v == -float('inf')):
            return str(v)
        return v
    (BASE / 'logs/debugsol_analysis.json').write_text(json.dumps(clean(report), indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
