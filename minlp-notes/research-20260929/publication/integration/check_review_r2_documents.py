"""Targeted r2 document, Git-ignore boundary and label-only regression checks."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'research-20260929/publication'
OUT = Path(__file__).resolve().parent
MANIFESTS = {'MANIFEST.md', 'manifest.tsv'}


def ignored(paths):
    run = subprocess.run(['git', 'check-ignore', '--stdin'], cwd=ROOT,
                         input='\n'.join(paths) + '\n', capture_output=True, text=True)
    assert run.returncode in (0, 1), run.stderr
    return set(run.stdout.splitlines())


all_files = [p for p in (P / 'literature').rglob('*') if p.is_file() and '__pycache__' not in p.parts]
copies = [str(p.relative_to(ROOT)) for p in all_files if 'sources' in p.parts and p.name not in MANIFESTS]
track = [str(p.relative_to(ROOT)) for p in all_files if 'sources' not in p.parts or p.name in MANIFESTS]
assert ignored(copies) == set(copies)
assert not ignored(track), ignored(track)
print(f'PASS literature ignore boundaries: {len(copies)} local source copies ignored; {len(track)} reports/checks/logs/manifests visible')
assert (OUT / 'review-r2-root-literature-before.log').read_bytes() == (OUT / 'review-r2-root-literature-after.log').read_bytes()
assert subprocess.check_output(['git', 'status', '--short', '--ignored', '--', 'literature/'], cwd=ROOT) == (OUT / 'review-r2-root-literature-before.log').read_bytes()
print('PASS root literature/ status unchanged')

files = json.loads((P / 'reproduction/files-to-commit.json').read_text())
paths = [v for values in files.values() if isinstance(values, list) for v in values]
assert not ignored(paths)
assert not set(paths) & set(copies)
assert set(track) <= set(paths)
print(f'PASS {len(set(paths))} distinct commit dependencies visible, with no literature source copies')

summary = (P.parent / 'open-instances-summary.md').read_text()
ready = (P / 'READINESS.md').read_text()
small = (P / 'literature/small/report.md').read_text()
network = (P / 'literature/network/report.md').read_text()
control = (P / 'literature/control/report.md').read_text()
readme = (P / 'reproduction/README.md').read_text()
assert 'within 1.3e-6 (camshape100) and 3.9e-5 (lnts50)' in summary
assert '1.3e-6 for camshape100 and 3.9e-5 for lnts50' in ready
assert 'Martín' not in control
assert 'exactly feasible point 6.4531031593842274' not in small
assert 'exactly feasible point 5.7605396164535106' not in small
assert 'unless the separate full recheck has replaced it' not in small
for stale in ('2233.821, ours', '6963.795, ours', '914.012, ours (10.8%)'):
    assert stale not in network
assert 'total CPU' not in readme and '41,162 CPU' not in readme
assert 'wall s (summed over chunks)' in (P / 'eg-recheck/report.md').read_text()
assert 'as seen inside the WSL2 VM' in ready
assert 'excluded' not in ready.lower() and 'remain with the parallel owner' not in ready
for item in ('DOI', 'data/code-availability', 'QPLIB', 'MATPOWER', 'Göß–Burlacu–Martin', 'MINLPLib maintainers', 'BARON developers'):
    assert item in ready, item
for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', ready):
    if '#' not in target or '://' in target or target.startswith('#'):
        continue
    path, anchor = target.split('#', 1)
    text = (P / path).read_text()
    headings = [line.lstrip('#').strip() for line in text.splitlines() if line.startswith('#')]
    anchors = {re.sub(r'[^\w\- ]', '', heading.lower()).replace(' ', '-') for heading in headings}
    assert anchor in anchors, target
print('PASS r2 wording, decisions and response-section anchors')

path = 'research-20260929/publication/eg-recheck/summarize.py'
old = subprocess.check_output(['git', 'show', 'HEAD:' + path], cwd=ROOT, text=True)
new = (ROOT / path).read_text()
restored = new.replace('wall time {t:.0f}s (summed over chunks)', 'CPU time {t:.0f}s').replace("{tot['time']:.0f}s wall time summed over certification chunks", "{tot['time']:.0f}s CPU in the certification chunks")
assert ast.dump(ast.parse(old)) == ast.dump(ast.parse(restored))
print('PASS summarize.py differs only in the two timing labels; no scientific code executed')
for path in [OUT / 'check_review_r2_evidence.py', OUT / 'check_review_r2_documents.py'] + list((P / 'reproduction/tools').glob('*.py')):
    ast.parse(path.read_text(), filename=str(path))
print('PASS changed check and package-tool Python syntax')
for path in [P / 'READINESS.md', P / 'reproduction/README.md', P / 'reproduction/report.md']:
    assert path.read_bytes().endswith(b'\n')
    assert all(line.rstrip() == line for line in path.read_text().splitlines()), path
print('ALL REVIEW R2 DOCUMENT CHECKS PASSED')
