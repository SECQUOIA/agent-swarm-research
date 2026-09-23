"""Independent root checks of the actual submission exports."""
from pathlib import Path
from zipfile import ZipFile
import concurrent.futures
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

OUT = Path(__file__).resolve().parent
PAPER = OUT.parents[1]
WORK = Path(tempfile.mkdtemp(prefix='bilevel-final-root-'))
ENV = os.environ.copy()
ENV.pop('PYTHONPATH', None)
ENV['PATH'] = str(Path(sys.executable).parent) + os.pathsep + ENV['PATH']
for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    ENV[key] = '1'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(name, command, cwd, timeout=600):
    result = subprocess.run(command, cwd=cwd, env=ENV, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=timeout)
    (OUT / (name + '.log')).write_text(result.stdout)
    assert result.returncode == 0, (name, result.returncode)
    return {'command': command, 'cwd': str(cwd), 'exit_code': result.returncode}

artifacts = {}
roots = {}
for name in ('structured-bilevel-latex-source', 'structured-bilevel-computational-supplement'):
    path = PAPER / (name + '.zip')
    artifacts[path.name] = digest(path)
    with ZipFile(path) as archive:
        for member in archive.namelist():
            rel = Path(member)
            assert not rel.is_absolute() and '..' not in rel.parts
        archive.extractall(WORK)
    root = WORK / name
    manifest = json.loads((root / 'SHA256.json').read_text())
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    assert actual == set(manifest) | {'SHA256.json'}
    for relative, expected in manifest.items():
        assert digest(root / relative) == expected, relative
        assert not any(part in ('process', 'literature') for part in Path(relative).parts)
    roots[name] = root

SOURCE = roots['structured-bilevel-latex-source']
SUPPLEMENT = roots['structured-bilevel-computational-supplement']
SP = SUPPLEMENT / 'paper-structured-bilevel'
for path in SOURCE.rglob('*'):
    if path.is_file() and path.name not in ('README.md', 'SHA256.json'):
        assert path.read_bytes() == (PAPER / path.relative_to(SOURCE)).read_bytes()
assert r'\author{}' in (SOURCE / 'main.tex').read_text()

snapshot = PAPER / 'process/snapshots/stage08-round01'
frozen = json.loads((snapshot / 'SHA256.json').read_text())
changed = [name for name, expected in frozen.items() if digest(PAPER/name) != expected]
assert set(changed) == {'README.md', 'sections/01-foundations.tex', 'sections/04-accuracy.tex', 'references.bib'}, changed
diff = []
for name in changed:
    diff.extend(difflib.unified_diff((snapshot/name).read_text().splitlines(True),
                (PAPER/name).read_text().splitlines(True), fromfile='reviewed/'+name, tofile='final/'+name))
(OUT / 'changes.diff').write_text(''.join(diff))

provenance = json.loads((SUPPLEMENT/'measurement-provenance.json').read_text())
record = json.loads((SP/'data/stage06-results.json').read_text())
assert len(record['records']) == 60
assert len({(r['name'], r['method'], r['repetition']) for r in record['records']}) == 60
assert all(r['exit_code'] == 0 for r in record['records'])
assert digest(SP/'data/stage06-results.json') == '29d0bf7b85001b96f50fcd220164bd019238a2132ea866daba73d5863bc8af7f'
assert set(record['input_hashes']) == set(provenance['input_mapping'])
for name, expected in record['input_hashes'].items():
    mapping = provenance['input_mapping'][name]
    assert digest(SUPPLEMENT/mapping['measured_path']) == expected
    assert digest(SUPPLEMENT/name) == mapping['current_sha256']

def check_source():
    result = run('source-build', ['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error', '-outdir=build', 'main.tex'], SOURCE)
    log = (SOURCE/'build/main.log').read_text()
    assert not re.search(r'Warning|Overfull|Underfull|undefined', log)
    shutil.copy2(SOURCE/'build/main.log', OUT/'final-main.log')
    run('source-text', ['pdftotext', 'build/main.pdf', str(OUT/'source-paper.txt')], SOURCE)
    run('delivered-text', ['pdftotext', str(PAPER/'paper.pdf'), str(OUT/'delivered-paper.txt')], SOURCE)
    assert (OUT/'source-paper.txt').read_bytes() == (OUT/'delivered-paper.txt').read_bytes()
    run('pdf-info', ['pdfinfo', str(PAPER/'paper.pdf')], SOURCE)
    result['pages'] = int(re.search(r'Output written on .*\((\d+) pages', log).group(1))
    return result

def check_computations():
    checks = [run('supplement-integrity', [sys.executable, 'verify_archive.py'], SUPPLEMENT)]
    tables = {p.name: p.read_bytes() for p in (SP/'data').glob('table-*.tex')}
    checks.append(run('tables', [sys.executable, 'paper-structured-bilevel/code/summarize_experiments.py'], SUPPLEMENT))
    assert len(tables) == 3
    assert all((SP/'data'/name).read_bytes() == data for name, data in tables.items())
    checks.append(run('diagnostics', [sys.executable, 'paper-structured-bilevel/code/run_diagnostics.py'], SUPPLEMENT, timeout=1000))
    diagnostics = json.loads((SP/'verification/stage06-author/diagnostics.json').read_text())
    assert len(diagnostics) == 5 and all(r['exit_code'] == 0 for r in diagnostics)
    shutil.copy2(SP/'verification/stage06-author/diagnostics.json', OUT/'diagnostic-outcomes.json')
    assert digest(SP/'data/stage06-results.json') == provenance['record_sha256']
    return checks

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    a = pool.submit(check_source)
    b = pool.submit(check_computations)
    source_result = a.result()
    computation_result = b.result()

for name, expected in artifacts.items():
    assert digest(PAPER/name) == expected, ('archive changed during verification', name)
artifacts['paper.pdf'] = digest(PAPER/'paper.pdf')
report = {'workspace': str(WORK), 'artifacts': artifacts, 'changed_reviewed_files': changed,
          'unchanged_reviewed_files': len(frozen)-len(changed), 'source': source_result,
          'computations': computation_result, 'measured_inputs': len(record['input_hashes']),
          'records': 60, 'tables_byte_identical': 3, 'status': 'passed'}
(OUT/'manifest.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report, indent=2))
