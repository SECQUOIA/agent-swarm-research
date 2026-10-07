"""Validate only round-3 write scope, records and patch replay."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent
os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:2])
inventory = json.loads((W / 'FILES-r3.json').read_text())
assert inventory['base'] == 'research-20260929'
files = inventory['files']
assert len(files) == len(set(files))
older = {'open-instances-wave2/cops/report.md', 'reviews/cops-verification/verification-report.md',
         'reviews/open-instances-verification/verification-report.md', 'reviews/closing-audit-a.md',
         'publication/reviews/solver-campaign-review-r1.md'}
tracks = ['primal/chain', 'primal/lnts', 'primal/powerflow', 'primal/water-ann-kan',
          'audit-ir', 'scip-bug', 'literature/control']
allowed = older | {f'publication/{track}/report.md' for track in tracks}
allowed |= {'publication/literature/control/checks/dtoc5_reference_check.py',
            'publication/literature/control/checks/dtoc5_reference_check.log'}
for rel in files:
    assert rel in allowed or rel.startswith('publication/reviews/minor-fixes/'), rel
    assert (R / rel).is_file(), rel
cumulative = set(json.loads((W / 'FILES.json').read_text()))
for rel in files:
    assert (rel[len('publication/'):] if rel.startswith('publication/') else '../'+rel) in cumulative
print('Write inventory is complete for snapshots and artifacts; every path is in the assigned scope.')
assert 'PASS:' in (W / 'check_r3.log').read_text().splitlines()[-1]
commands = json.loads((W / 'commands-r3.json').read_text())
assert any(c['exit_code'] == 1 and 'check_r3.py' in c['command'] for c in commands)
assert any(c['exit_code'] == 0 and 'check_r3.py' in c['command'] for c in commands)
print('Exact command records retain both the initial patch-check failure and successful correction.')

patch = W / 'report_changes_r3.patch'
targets = re.findall(r'^\+\+\+ (.+)$', patch.read_text(), re.M)
assert all(target in files for target in targets)
with tempfile.TemporaryDirectory(prefix='minor-fixes-r3-replay-') as directory:
    dest = Path(directory)
    for before in sorted((W / 'before-r3').iterdir()):
        rel = before.name.replace('__', '/')
        copy = dest / rel
        copy.parent.mkdir(parents=True, exist_ok=True)
        copy.write_bytes(before.read_bytes())
    result = subprocess.run(['patch', '--batch', '--fuzz=0', '-p0', '-i', str(patch)],
                            cwd=dest, text=True, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    for target in targets:
        assert (dest / target).read_bytes() == (R / target).read_bytes(), target
    print('Round-3 GNU patch --batch --fuzz=0 -p0 replay reproduces all', len(targets), 'patch targets byte for byte.')
print('PASS: targeted round-3 artifact validation; no project-wide or CI checks.')
