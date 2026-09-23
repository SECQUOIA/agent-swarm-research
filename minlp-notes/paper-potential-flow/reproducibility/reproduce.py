#!/usr/bin/env python3
"""Replay exact witnesses, with optional scientific diagnostics in an isolated copy."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
CODE = 'code/potential_flow_mpd/'
VERIFY = 'paper-potential-flow/verification/'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numerical', action='store_true',
                        help='also run scientific diagnostics and numerical producers')
    parser.add_argument('--output', type=Path, default=Path('reproduction-report.json'))
    args = parser.parse_args()
    commands = []
    for mode in ([], ['-S', '-O']):
        for name in ('check_envelope_certificate_review', 'check_envelope_bregman_review',
                     'check_goal_flow_certificate_review', 'check_certified_envelope_review'):
            commands.append(mode + [CODE + name + '.py'])
        commands.append(mode + [VERIFY + 'check_s6a_certificates.py'])
    commands += [
        ['-S', '-O', CODE+'certified_envelope.py', 'verify', CODE+'certified_envelope_example.json'],
        ['-S', '-O', CODE+'envelope_rational_certificates.py', '--verify', CODE+'envelope_certificate_example.json'],
        ['-S', '-O', CODE+'energy_design_certificate.py', '--verify', CODE+'energy_design_certificate_example.json'],
        ['-S', '-O', CODE+'goal_flow_certificate.py'],
        ['-S', '-O', CODE+'goal_flow_certificate.py', '--certificate', CODE+'envelope_certificate_example.json'],
        ['-S', CODE+'exact_weighted_cactus.py', CODE+'exact_weighted_cactus_example.json'],
        ['-S', VERIFY+'check_a7_weighted_asymmetric.py'],
        ['-S', VERIFY+'check_s5b_sensitivity.py'],
    ]
    if args.numerical:
        commands += [[VERIFY+name+'.py'] for name in (
            'check_a1_preliminaries', 'check_a2_cactus', 'check_a3_block_rank',
            'check_a4_laws', 'check_s5a_design', 'check_s5c_scalar_approximation')]
        commands += [[VERIFY+'check_s6a_certificates.py', '--numerical'],
                     [CODE+'envelope_rational_certificates.py'],
                     [CODE+'certified_envelope_benchmarks.py'],
                     [CODE+'check_certified_envelope_review.py', '--producer']]
    report = {'python': sys.version, 'numerical': args.numerical, 'runs': [],
              'scope': 'Finite diagnostics and exact saved-witness verification; not proofs of universal theorems.'}
    if args.numerical:
        report['packages'] = {name: importlib.metadata.version(name) for name in
                              ('numpy', 'scipy', 'sympy', 'networkx', 'cvxpy', 'clarabel')}
    with tempfile.TemporaryDirectory(prefix='potential-flow-replay-') as temp:
        replay = Path(temp)
        shutil.copytree(ROOT/'code/potential_flow_mpd', replay/'code/potential_flow_mpd',
                        ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copytree(PAPER/'verification', replay/'paper-potential-flow/verification',
                        ignore=shutil.ignore_patterns('__pycache__'))
        for command in commands:
            start = time.monotonic()
            run = subprocess.run([sys.executable, *command], cwd=replay, capture_output=True,
                                 text=True, encoding='utf-8', errors='replace')
            def portable(text):
                return text.replace(str(replay), '<replay-root>').replace(str(ROOT), '<source-root>')
            report['runs'].append({'command': ['python', *command], 'returncode': run.returncode,
                                   'seconds': time.monotonic()-start,
                                   'stdout': portable(run.stdout), 'stderr': portable(run.stderr)})
            print(('PASS' if run.returncode == 0 else 'FAIL') + ': ' + ' '.join(command), flush=True)
    report['passed'] = all(run['returncode'] == 0 for run in report['runs'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())
