"""Validate only round-2 artifacts and ordered edits; never apply integration changes."""
import ast
import hashlib
import json
from pathlib import Path
import re

W = Path(__file__).resolve().parent
P = W.parents[1]
R = P.parent
ROOT = R.parent
tracks = ['primal/chain','primal/dtoc5-lukvle10','primal/lnts','primal/powerflow',
          'primal/water-ann-kan','audit-ir','eg-recheck','scip-bug','literature/control','literature/network']
for path,h in json.loads((W/'protected-r2.json').read_text()).items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == h, path
print('Protected main summary and audit report unchanged.')
summary = (W/'summary.md').read_text()
edits = json.loads((W/'integration-r2.json').read_text())
for target in dict.fromkeys(v['target'] for v in edits):
    content = (R/target).read_text()
    for v in (v for v in edits if v['target'] == target):
        assert v['old'] in content, (target,v['reason'])
        assert v['old'] in summary and v['new'] in summary
        content = content.replace(v['old'],v['new'])
print('All',len(edits),'ordered old -> new edits apply in memory and appear in summary.md.')
response = (W/'response-r2.md').read_text()
numbers = [int(s) for s in re.findall(r'^\| (\d+)\.',response,re.M)]
assert numbers == list(range(1,23))
for track in tracks:
    f = P/track/'report.md'; text = f.read_text()
    assert text.count('### Round 2: independent minor-fixes review') == 1
    section = text.split('### Round 2: independent minor-fixes review')[1]
    for target in re.findall(r'\]\(([^)]+)\)',section):
        assert (f.parent/target).resolve().is_file(), (track,target)
print('All 22 response rows and ten report response sections present; new links resolve.')
assert 'PASS:' in (W/'check_r2.log').read_text().splitlines()[-1]
assert 'PASS:' in (P/'primal/water-ann-kan/logs/minor_review_check.log').read_text().splitlines()[-1]
assert 'PASS:' in (P/'primal/lnts/logs/review_r2_check.log').read_text().splitlines()[-1]
assert 'PASS:' in (P/'scip-bug/logs/review_r2_check.log').read_text().splitlines()[-1]
assert 'PASS:' in (P/'literature/control/checks/dtoc5_reference_check.log').read_text().splitlines()[-1]
text = (P/'literature/control/checks/qplib_camshape_compare.log').read_text()
assert text.count('MINLPLib rows without a QPLIB row') == 4
assert '4.708e-10' in text and '2.497e-10' in text and 'x1.up' in text
for f in [*W.glob('*r2.py'),P/'primal/water-ann-kan/code/minor_review_check.py',
          P/'primal/water-ann-kan/code/nn_exact.py',P/'literature/control/checks/dtoc5_reference_check.py']:
    ast.parse(f.read_text(),filename=str(f))
print('Final targeted logs and changed-script syntax pass.')
draft = (P/'scip-bug/report.md').read_text().split('## upstream-report-draft.md (content)')[1].split('## Response to review')[0]
assert not any(s in draft for s in ['logs/minor_review_check.log','../reviews/','Review r1','review r1'])
assert 'not submitted' in draft
for phrase in ['none of this has been independently reviewed','6.89%']:
    assert phrase not in (P/'primal/water-ann-kan/report.md').read_text()
control = (P/'literature/control/report.md').read_text()
assert 'largest applicable finite bound magnitude' not in control
assert 'implies [−100' not in control
assert '5.9096%' in control and '13.3380%' in control and '20.8425%' in control
network = (P/'literature/network/report.md').read_text()
assert 'Göß et al. 2026' not in network and '42,48,56,59,69,72' not in network
print('Draft stays internal; corrected mechanism, default-rule and citation wording checked.')
assert all(v['exit_code'] == 0 for v in json.loads((W/'commands-r2.json').read_text()))
print('PASS: targeted round-2 handoff validation; no project-wide or CI checks.')
