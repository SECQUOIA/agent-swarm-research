#!/usr/bin/env python3
"""Copy the targeted artifact to a fresh /tmp tree, then run short checks there."""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo-root', required=True, type=Path)
    ap.add_argument('--logs', required=True, type=Path)
    ap.add_argument('--eg-int', action='store_true', help='Also regenerate and audit eg_int_s (about five minutes).')
    a = ap.parse_args()
    repo = a.repo_root.resolve()
    logs = a.logs.resolve()
    logs.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='minlp-artifact-', dir='/tmp'))
    p = work / 'paper-open-minlplib'
    r = work / 'research-20260929'
    roots = ['paper-open-minlplib/development/reviews/code/' + d for d in
             ('sol-lnts-review', 'sol-dtoc5-review', 'sol-kan-review', 'sol-eg-audit-review')]
    roots += ['paper-open-minlplib/development/eg-audit',
              'paper-open-minlplib/development/dossiers/ann-kan-checks/logs',
              'research-20260929/reviews/eg-retry-review-checks',
              'research-20260929/publication/eg-recheck',
              'research-20260929/publication/primal/lnts',
              'research-20260929/reviews/wave3-verification/logs',
              'research-20260929/open-instances-wave3/logs']
    for rel in roots:
        shutil.copytree(repo / rel, work / rel, ignore=shutil.ignore_patterns('__pycache__'))
    files = ['paper-open-minlplib/development/dossiers/checks/lnts-lukvle10/lnts_exact_opt.json',
             'paper-open-minlplib/development/reviews/sol-dtoc5-exact.md']
    files += ['research-20260929/open-instances-wave3/eg/retry/logs/' + f for f in
              ('int9_final.log', 'disc9_p0.log', 'disc9_p1.log')]
    for rel in files:
        target = work / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(repo / rel, target)
    # The copy checker also reads each original recording module as data.
    for src in (p / 'development/eg-audit/record/research-20260929').rglob('*'):
        if src.is_file():
            rel = src.relative_to(p / 'development/eg-audit/record/research-20260929')
            target = r / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(repo / 'research-20260929' / rel, target)
    numbers = json.loads((repo / 'paper-open-minlplib/data/numbers.json').read_text())
    osil = work / 'osil'
    osil.mkdir()
    for name in ['lnts50', 'lnts100', 'lnts200', 'lnts400', 'eg_int_s', 'eg_disc_s', 'eg_disc2_s']:
        item = numbers['instances'][name]['size']
        src = repo / item['osil']
        assert hashlib.sha256(src.read_bytes()).hexdigest() == item['osil_sha256'], name
        shutil.copy2(src, osil / (name + '.osil'))
    env = dict(os.environ, MINLP_REPO_ROOT=str(work), EG_AUDIT_R=str(r), MINLPLIB_OSIL_ROOT=str(osil),
               OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
               NUMEXPR_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    cpus = sorted(os.sched_getaffinity(0))[:4]
    os.sched_setaffinity(0, cpus)
    review = p / 'development/reviews/code'
    jobs = [('lnts', [str(review / 'sol-lnts-review/verify.py')]),
            ('dtoc5', [str(review / 'sol-dtoc5-review/review.py')])]
    jobs += [(name, [str(review / 'sol-kan-review/run_review.py'), name])
             for name in ('kan_r3_h1_n4', 'kan_r3_h1_n5', 'kan_r3_h1_n9')]
    jobs += [(name, [str(p / 'development/eg-audit/tests' / (name + '.py'))])
             for name in ('test_auditor', 'test_negative', 'boundary_check', 'check_copies')]
    jobs = [(name, args + [str(r / 'publication/eg-recheck/rec/rec_disc2_p1.npz'),
                          str(work / 'negative-tests')] if name == 'test_negative' else args)
            for name, args in jobs]
    def run(job):
        name, args = job
        cmd = ['python3'] + args
        t = time.monotonic()
        with (logs / (name + '.log')).open('w') as out:
            result = subprocess.run(cmd, cwd=work, env=env, stdout=out, stderr=subprocess.STDOUT, timeout=900)
        record = {'name': name, 'command': cmd, 'cwd': str(work), 'exit_code': result.returncode,
                  'wall_seconds': round(time.monotonic() - t, 3), 'log': name + '.log'}
        print(json.dumps(record), flush=True)
        return record
    egjob = ('eg_int', [str(p / 'development/eg-audit/run_audit.py'), '--only', 'int', '--workers', '1',
                        '--out', str(work / 'fresh-eg-int'), '--timeout', '600'])
    # Three concurrent single-threaded jobs; the driver spawns only one worker.
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(run, job) for job in ([egjob] if a.eg_int else []) + jobs]
        results = [f.result() for f in futures]
    failed = [x['name'] for x in results if x['exit_code']]
    comparisons = {}
    def compare_json(rel, ignored=()):
        old = json.loads((repo / rel).read_text())
        new = json.loads((work / rel).read_text())
        for key in ignored:
            old.pop(key, None); new.pop(key, None)
        assert old == new, rel
        comparisons[rel] = 'all fields equal except ' + ', '.join(ignored) if ignored else 'all fields equal'
    compare_json('paper-open-minlplib/development/reviews/code/sol-lnts-review/certificate.json')
    compare_json('paper-open-minlplib/development/reviews/code/sol-dtoc5-review/result.json', ('elapsed_seconds', 'affinity'))
    for name in ('kan_r3_h1_n4', 'kan_r3_h1_n5', 'kan_r3_h1_n9'):
        compare_json('paper-open-minlplib/development/reviews/code/sol-kan-review/evidence/' + name + '.result.json', ('time',))
    if a.eg_int and not failed:
        # Import only installed numpy; the numerical scripts ran from the disposable tree.
        import numpy as np
        for newpath, oldrel, ignored in [
            (work / 'fresh-eg-int/rec/rec_int.npz', 'paper-open-minlplib/development/eg-audit/out/rec/rec_int.npz', ()),
            (work / 'fresh-eg-int/res/int.npz', 'paper-open-minlplib/development/eg-audit/out/res/int.npz', ('time',))]:
            with np.load(newpath) as new, np.load(repo / oldrel) as old:
                assert set(new.files) == set(old.files)
                assert all(new[k].dtype == old[k].dtype and new[k].shape == old[k].shape and
                           new[k].tobytes() == old[k].tobytes() for k in old.files if k not in ignored), oldrel
            comparisons[oldrel] = 'byte-identical arrays except ' + ', '.join(ignored) if ignored else 'byte-identical arrays'
        shutil.copy2(work / 'fresh-eg-int/compare.log', logs / 'eg_int_compare.log')
    followups = [('dtoc5_displays', [str(review / 'sol-dtoc5-review/check_displays.py')]),
                 ('dtoc5_boundaries', [str(review / 'sol-dtoc5-review/boundary_checks.py')]),
                 ('kan_audit', [str(review / 'sol-kan-review/audit.py')])]
    followups += [(name, [str(review / 'sol-eg-audit-review' / (name + '.py'))]) for name in
                  ('independent_numeric', 'source_and_range', 'verify_artifacts')]
    for job in followups:
        result = run(job); results.append(result)
        if result['exit_code']: failed.append(result['name'])
    summary = {'work_root': str(work), 'cpu_affinity': cpus, 'commands': results,
               'comparisons': comparisons, 'failed': failed, 'scope': 'Targeted packaging checks only; no CI or project-wide checks.'}
    (logs / 'short-checks.json').write_text(json.dumps(summary, indent=2) + '\n')
    print('PASS' if not failed else 'FAIL', 'targeted relocated checks;', work, flush=True)
    return bool(failed)


if __name__ == '__main__':
    raise SystemExit(main())
