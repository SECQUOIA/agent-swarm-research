"""Validate only this minor-fix handoff and its changed point metadata."""
from pathlib import Path as _PublicPath
_PUBLIC_HOME = str(_PublicPath.home())

from pathlib import Path
import ast,json,re,subprocess,hashlib
p=Path(__file__).resolve().parents[2];d=Path(__file__).resolve().parent
issues=json.loads((d/'issues.json').read_text());assert len(issues)==10 and sum(map(len,issues.values()))==57
entries=[]
for track,rows in issues.items():
 script='code/minor_review_check.py' if track=='primal/water-ann-kan' else 'checks/minor_review_check.py' if track.startswith('literature/') else 'minor_review_check.py'
 log='checks/minor_review_check.log' if track.startswith('literature/') else 'logs/minor_review_check.log'
 report=(p/track/'report.md').read_text();assert report.count('## Response to review')==1
 response=report.split('## Response to review')[1]
 for i,title,_,_ in rows:assert f'| {i}. {title} |' in response,(track,i,title)
 data=(p/track/log).read_text();assert 'PASS:' in data and 'Traceback' not in data
 ast.parse((p/track/script).read_text())
 entries.append((track,script,log))
 print(track,len(rows),'responses; final targeted check PASS')
for file in ['primal/dtoc5-lukvle10/gaps.py','primal/lnts/lnts_primal.py','primal/water-ann-kan/code/nn_exact.py','literature/control/checks/qplib_camshape_compare.py','literature/control/checks/dtoc5_reference_check.py']:
 ast.parse((p/file).read_text());print('syntax OK',file)
for file in sorted((p/'primal/water-ann-kan/points').glob('*.point.json')):
 rel=file.relative_to(p.parents[1]);old=json.loads(subprocess.check_output(['git','show',f'HEAD:{rel}'],text=True));new=json.loads(file.read_text())
 assert '(mid, rad)' in old['construction'] and '{lo, hi}' in new['construction']
 assert old['construction'].replace('(mid, rad)','{lo, hi}')==new['construction']
 del old['construction'];del new['construction'];assert old==new
 print('numerical fields unchanged',file.name)
for track in ['literature/control','literature/network','scip-bug']:
 manifest=(p/track/'sources/MANIFEST.md').read_text().split('## Minor-review revision (2026-10-03)')[1]
 for line in manifest.splitlines():
  m=re.match(r'\| `([^`]+)` \|.*\| `(\w{64})` \|',line)
  if m:
   file=p/track/'sources'/m[1];assert hashlib.sha256(file.read_bytes()).hexdigest()==m[2],file
 print('added-source hashes OK',track)
assert 'report.md was NOT written' not in (p/'primal/chain/report.md').read_text()
assert 'Status: partial.' not in (p/'audit-ir/report.md').read_text()
assert 'Status: partial.' not in (p/'primal/powerflow/report.md').read_text()
assert 'PDF page 112' in (p/'literature/network/checks/minor_review_check.log').read_text()
assert 'matches saved r2 hash' in (p/'literature/control/checks/dtoc5_reference_check.log').read_text()
# Record the exact final targeted commands. Historical main-track commands remain in reports.
prefix='OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 '
base='research-20260929/publication/'
text=('# Commands and results for the minor-fix revision\n\nAll commands below ran from `' + _PUBLIC_HOME + '/repo/minlp-notes`. Numerical checks used one thread per process. At most four independent small checks ran concurrently; the work never exceeded four CPU cores. No main construction, solver campaign, project-wide verification or CI inspection was performed. The older commands preserved in the reports belong to the original tracks, not this revision.\n\n## Targeted checks actually run\n\n')
checks=[]
for track,script,log in entries:
 cmd=prefix+f'python3 {base}{track}/{script} > {base}{track}/{log}'
 text+=f'### {track}\n\n```sh\n{cmd}\n```\n\nResult: exit 0; final PASS. Evidence: [log](../../{track}/{log}).\n\n'
 checks.append({'track':track,'command':cmd,'result':'exit 0; PASS'})
extra='literature/control/checks/dtoc5_reference_check'
cmd=prefix+f'python3 {base}{extra}.py > {base}{extra}.log'
text+=f'### dtoc5 reference-point scale\n\n```sh\n{cmd}\n```\n\nResult: exit 0; hash matches r2, maximum |x| = 8.057243524908399 < 100. No feasibility or optimality proof was repeated.\n\n'
checks.append({'track':'literature/control reference','command':cmd,'result':'exit 0; PASS'})
text+='''## Source preparation and report edits

```sh
pdftotext -layout research-20260929/publication/reviews/lit-network-r2/sources_r2/rwth820314_wayback20260128.pdf research-20260929/publication/literature/network/sources/schweidtmann2021_dissertation.txt
pdftotext -layout research-20260929/publication/literature/network/sources/oustry2022_pscc22.pdf research-20260929/publication/literature/network/sources/oustry2022_pscc22.txt
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/reviews/minor-fixes/prepare_sources.py > research-20260929/publication/reviews/minor-fixes/prepare_sources.log
python3 research-20260929/publication/reviews/minor-fixes/edit_reports.py
python3 research-20260929/publication/reviews/minor-fixes/edit_literature.py
python3 research-20260929/publication/reviews/minor-fixes/final_cleanup.py
python3 research-20260929/publication/reviews/minor-fixes/finish_handoff.py
```

Results: text extraction, saved-source copies and report edits succeeded. GitHub API issue/comment reads succeeded; nothing was submitted. Seven of the fifteen Crossref requests failed (six HTTP 429, one HTTP 404); the errors are retained in the metadata JSON, and paper headers were used where available. The metadata preparation script therefore completed with mixed lookup results, not universal success. Its log records every DOI outcome.

Final small inline edits updated the source-check references, the audit's repeated digit-count wording and the network summary table. Read-only inspections used `rg`, `cat`, `sed`, `head`, `tail`, scoped `git diff` and `git show`; the latter confirmed the historical eg second-pass commit and, in validation below, compared the seven point JSON files against HEAD. No Git mutation was performed.

## Development-check failures and resolution

Initial versions of the small check scripts exposed assumptions in the checks: the SCIP CSV omitted two later runs; the water-point check assumed a different JSON layout; the Waki check confused printed p. 31 with PDF p. 33; the QPLIB reference check initially expected zero entries to be listed. Each was corrected against raw logs, actual JSON or primary source bytes. The first report-edit helper also rejected an overlapping text replacement before being corrected. These were failures of the new checking/editing helpers, not failed main certificates. Final runs of the commands above all passed. Four checks (chain, dtoc5/lukvle10, SCIP and network) were repeated after strengthening their evidence; the dtoc5 reference-point command was repeated after its entry-count correction.

## Final handoff validation

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/reviews/minor-fixes/validate_handoff.py > research-20260929/publication/reviews/minor-fixes/validation.log
```

Checks: 57 response rows across ten reports; final PASS logs; syntax of the four minimally changed scripts and new check scripts; all numerical fields in the seven ANN/KAN JSON files unchanged against HEAD; added-source hashes; final reference-point evidence. This check is scoped to the authorized revision. CI was neither run nor inspected.
'''
# Count actual metadata failures rather than rely on prose.
meta=json.loads((p/'literature/network/sources/bibliography_metadata_20261003.json').read_text());failed=[v for v in meta.values() if 'error' in v]
assert len(failed)==7,len(failed)
(d/'commands.md').write_text(text)
files=[p/t/'report.md' for t in issues]
for track,script,log in entries:files.extend([p/track/script,p/track/log])
files.extend(p/f for f in ['primal/dtoc5-lukvle10/gaps.py','primal/lnts/lnts_primal.py','primal/water-ann-kan/code/nn_exact.py','literature/control/checks/qplib_camshape_compare.py','literature/control/checks/dtoc5_reference_check.py','literature/control/checks/dtoc5_reference_check.log'])
files.extend((p/'primal/water-ann-kan/points').glob('*.point.json'))
for track in ['literature/control','literature/network','scip-bug']:
 files.append(p/track/'sources/MANIFEST.md')
 manifest=(p/track/'sources/MANIFEST.md').read_text().split('## Minor-review revision (2026-10-03)')[1]
 for line in manifest.splitlines():
  m=re.match(r'\| `([^`]+)` \|',line)
  if m:files.append(p/track/'sources'/m[1])
files.extend(x for x in d.rglob('*') if x.is_file() and x.name!='FILES.json')
(d/'FILES.json').write_text(json.dumps(sorted(str(x.relative_to(p)) for x in set(files)),indent=2)+'\n')
progress=json.loads((d/'PROGRESS.json').read_text());progress.update(status='complete',remaining=[],background_jobs=[],checks=checks+[{'track':'handoff','command':prefix+f'python3 {base}reviews/minor-fixes/validate_handoff.py > {base}reviews/minor-fixes/validation.log','result':'PASS'}],open_issues=['Integration changes in summary.md remain for the integrating agent.','Source-access and model-equivalence limits remain documented in summary.md.']);(d/'PROGRESS.json').write_text(json.dumps(progress,indent=2)+'\n')
print('PASS: 57 review responses, targeted logs, syntax, metadata-only JSON changes and added-source hashes. Handoff complete; no background jobs.')
