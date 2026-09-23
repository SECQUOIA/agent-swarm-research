"""Validate the delivered archives after extraction outside the repository."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from zipfile import ZipFile

PAPER = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
WORK = Path(tempfile.mkdtemp(prefix='structured-bilevel-export-'))
ENV = os.environ.copy()
ENV.pop('PYTHONPATH', None)
ENV['PATH'] = str(Path(sys.executable).parent) + os.pathsep + ENV['PATH']
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    ENV[key] = '1'
(OUT/'extracted-workspace.txt').write_text(str(WORK)+'\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def extract(stem):
    with ZipFile(PAPER/(stem+'.zip')) as archive:
        archive.extractall(WORK)
    root = WORK/stem
    manifest = json.loads((root/'SHA256.json').read_text())
    for name, expected in manifest.items():
        assert sha(root/name) == expected, name
    return root

SOURCE = extract('structured-bilevel-latex-source')
SUPPLEMENT = extract('structured-bilevel-computational-supplement')
records = []

def run(name, args, cwd, timeout=300):
    started = time.monotonic()
    result = subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True, timeout=timeout)
    (OUT/(name+'.log')).write_text(result.stdout+result.stderr)
    entry = dict(name=name, command=args, cwd=str(cwd), exit_code=result.returncode,
                 seconds=round(time.monotonic()-started, 3))
    records.append(entry)
    print(name, result.returncode, entry['seconds'], flush=True)
    assert result.returncode == 0, name
    return result.stdout

def build():
    run('source-build', ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error', '-outdir=build', 'main.tex'], SOURCE)
    log = (SOURCE/'build/main.log').read_text()
    warnings = [line for line in log.splitlines() if any(word in line for word in ('Warning', 'Overfull', 'Underfull', 'undefined'))]
    assert not warnings, warnings
    shutil.copy2(SOURCE/'build/main.pdf', PAPER/'paper.pdf')
    shutil.copy2(SOURCE/'build/main.log', OUT/'final-main.log')
    run('pdf-info', ['pdfinfo', str(PAPER/'paper.pdf')], SOURCE)
    run('pdf-text', ['pdftotext', str(PAPER/'paper.pdf'), str(OUT/'paper.txt')], SOURCE)

def check():
    run('integrity', [sys.executable, 'verify_archive.py'], SUPPLEMENT)
    paper = SUPPLEMENT/'paper-structured-bilevel'
    tables = {str(p.relative_to(SUPPLEMENT)): sha(p) for p in (paper/'data').glob('table-*.tex')}
    raw = sha(paper/'data/stage06-results.json')
    commands = [
        ('tables', 'paper-structured-bilevel/code/summarize_experiments.py'),
        ('diagnostics', 'paper-structured-bilevel/code/run_diagnostics.py'),
        ('support-recovery', 'paper-structured-bilevel/verification/stage02-author/check_support_recovery.py'),
        ('near-optimal', 'code/bilevel_reopened/nearoptimal_second_review.py'),
        ('screening', 'code/bilevel_reopened/screening_review_checks.py'),
        ('modulus', 'paper-structured-bilevel/verification/stage04-author/check_sharp_modulus.py'),
        ('boundaries', 'paper-structured-bilevel/verification/stage05-author/run_checks.py'),
        ('padding-recovery', 'paper-structured-bilevel/verification/stage05-author/check_padding_and_recovery.py'),
        ('figure', 'paper-structured-bilevel/code/plot_contacts.py'),
    ]
    for name, path in commands:
        run(name, [sys.executable, path], SUPPLEMENT, timeout=1000 if name == 'diagnostics' else 300)
    assert all(sha(SUPPLEMENT/name) == expected for name, expected in tables.items())
    assert sha(paper/'data/stage06-results.json') == raw
    result = dict(tables_byte_identical=tables, raw_record_unchanged=raw,
                  diagnostics=json.loads((paper/'verification/stage06-author/diagnostics.json').read_text()),
                  full_task_cases=len(json.loads((paper/'verification/stage06-author/full-task-checks.json').read_text())))
    (OUT/'computational-validation.json').write_text(json.dumps(result, indent=2)+'\n')

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = [pool.submit(build), pool.submit(check)]
    errors = []
    for future in futures:
        try:
            future.result()
        except Exception as error:
            errors.append(repr(error))
(OUT/'commands.json').write_text(json.dumps(records, indent=2)+'\n')
(OUT/'validation-result.json').write_text(json.dumps(dict(workspace=str(WORK), errors=errors), indent=2)+'\n')
assert not errors, errors
print('PASS: isolated source build and all documented non-timing commands', flush=True)
