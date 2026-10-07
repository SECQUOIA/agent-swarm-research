# Integration commands and results

Date: 2026-10-03. Working directory: /workspace/minlp-notes.
All numerical commands used one process, with OMP_NUM_THREADS=1,
OPENBLAS_NUM_THREADS=1 and MKL_NUM_THREADS=1. No solver or scientific search
was rerun. No project-wide verification or CI inspection was performed.
Nothing was committed, pushed or sent outside the repository.

The checks below are this implementation's checks, not new independent
review rounds. Scripts read saved evidence without importing scientific
modules. The audit checker runs only in an automatically removed disposable
copy. It opens neither a scientific module nor an output log in the main
tree.

```sh
python3 research-20260929/publication/integration/apply_replacements.py > research-20260929/publication/integration/replacements.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_numbers.py > research-20260929/publication/integration/numbers.log
python3 research-20260929/publication/integration/integrate_documents.py > research-20260929/publication/integration/integration.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/recompute_objectives.py > research-20260929/publication/integration/objectives.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_audit_displays.py > research-20260929/publication/integration/audit-displays.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_publication_counts.py > research-20260929/publication/integration/publication-counts.log
python3 research-20260929/publication/integration/check_integration.py > research-20260929/publication/integration/document-checks.log
python3 -m py_compile research-20260929/publication/integration/*.py

git diff --check -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/integration/
git diff --stat -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md
git status --short -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/integration/
```

| command/check | result and retained output |
|---|---|
| apply_replacements.py | All 40 old strings match in order, including all occurrences. The 33 owned replacements were applied; seven protected replacements were validated on disposable copies only. replacements.log/.json, before/ and ordered-validation/ retain the exact record. Do not rerun this script on already edited originals. |
| check_numbers.py | Exact Fraction checks passed: all numerical summary gap cells, corrected primal directions, saved dual directions, campaign comparisons/counts, run-G leaf totals and emfl lower displays. numbers.log and number-checks.json retain results and source hashes; gap-values.json retains every rational upper gap. It was rerun after fixing percentage formatting and adding the named memory-stop check. The first post-integration rerun failed because the new literature rows reused instance names; the checker was corrected to select the first numeric-table occurrence, then passed. This was a check-parser issue, not a numerical discrepancy. |
| integrate_documents.py | Both owned main documents written. Later small editorial edits and the readiness record were written directly; this script is the initial integration record, not an idempotent current-document rewrite. |
| recompute_objectives.py | dtoc5 and all five water objectives independently recomputed from saved exact points and OSIL; all equal their stored rational objectives. objectives.log. |
| check_audit_displays.py | Existing audit checker run in a disposable copy: ok 84, failed 8, skipped 1. All eight are the known historical quotations; no new failure. audit-displays.log and audit-display-command.json retain output and exact subprocess argv. |
| check_integration.py | Current table gaps cover their exact saved quantities; literature table names every campaign instance exactly once; local links and Markdown table shapes pass; stale current claims absent; open-decision run lists agree with the saved table. document-checks.log. |
| check_publication_counts.py | Exact saved-page counts 35/38/46, slack floor (0 screened changes; 17 tie changes), and SCIP 14-row/15-run and three-of-five scope pass. After the parent handoff, read-only inspection confirms six protected replacements applied by the round-3 owner; one historical solver-runs/report.prev.md display remains. publication-counts.log and protected-handoff.json. The first tie recount included three feasibility-only models without an objective; applying the audit’s min/max-sense restriction reproduced the published counts. |
| py_compile and scoped git diff --check | Targeted syntax and whitespace checks only. verification.log records their exits. |

Read-only inspection used pwd, rg --files, rg -n, cat, sed -n, head, tail,
git status --short, and short Python snippets on the supplied reports,
latest reviews, saved JSON/CSV and exact logs. AGENTS.md was read. The
initial `find .. -name AGENTS.md -print` finished; it found no additional
instructions under research-20260929. No background process remains.

The final package commands are **pending, not run by this task** because
reproduction/ is protected and edits are not frozen:

```sh
python3 research-20260929/publication/reproduction/tools/build_result_maps.py
python3 research-20260929/publication/reproduction/tools/rebuild_manifest.py
python3 research-20260929/publication/reproduction/tools/check_package.py
```

The parent’s round-3 handoff was checked read-only; no older-document
replacement was applied or reapplied after that handoff.

After all integration and track edits finish, the package owner
must rebuild the maps, then rebuild the manifest and run the default
package checker immediately before the user-authorized commit. This
integration did not duplicate the package smoke suite or inspect CI.

## Response to integration review r1 (2026-10-04)

Scope: items 1, 3–14 in the two main documents and READINESS.md;
items 2 and 15 are assigned to the parallel package/track owner.
Only those documents and integration/ were written. The before-edit
copies are in review-r1-before/. All numerical work read saved evidence
and used exact Fraction/Decimal arithmetic; NumPy was used only for
environment introspection and loading saved non-pickled timing scalars.
No scientific script was imported or executed in the main tree. At most
three single-thread checks ran concurrently. No certificate or solver
was rerun. No commit, push, message to an outside party, project-wide
verification or CI inspection was performed.

| targeted check | actual result |
|---|---|
| check_numbers.py | Passed all 142 exact checks; review-r1-numbers.log. Existing check code re-read saved source evidence, not the reviewer's numerical output. |
| recompute_objectives.py | All six exact OSIL objectives agreed with saved points; review-r1-objectives.log. |
| check_publication_counts.py | Saved-page counts, floor/ties, SCIP scope and protected handoff passed; review-r1-counts.log. |
| collect_environment_r1.py | Current /proc/uname/OS/BLAS/SIMD/libc captured; 443-command index and selected successful log hashes checked. environment-r1.json/.log and runtime-evidence-r1.json retain the evidence. |
| check_review_r1_evidence.py | Fresh exact checks passed for decimal versus binary64, both retry leaf totals/targets, historical closeness, campaign point, spring bisection, methanol precision/date, eg elapsed times, nine archive-gap instances, source PARA percentages, review counts, requirements and solver versions. review-r1-evidence.log/.json. |
| check_integration.py | All gaps and links passed. All 19 tables across the three documents parse with their rows attached to headers; the original 43 orphan literature rows are rejected by the negative control. review-r1-document-checks.log. |
| verify_review_r1_documents.py | Rendered HTML checked: 5 summary tables, 10 audit tables, 4 readiness tables; literature has 43 attached body rows. All 15 issues are accounted for, items 2/15 excluded, numeric result rows unchanged, timing values checked. review-r1-render-checks.log and rendered-tables-r1.json. |
| changed-script py_compile; scoped git diff --check | Passed; targeted syntax/whitespace only, not CI. |

Disagreement: eg-recheck labels its chunk times CPU seconds, but the
saved code uses time.time(). Exact summation of npz scalar times rounds
to 41,162 aggregate chunk wall seconds; summing independently rounded
log integers gives 41,151. Scheduler elapsed wall time is 5,372 seconds.
READINESS uses the actual elapsed-time meaning. Original per-run
environments and CPU times remain explicitly incomplete.

Source terms were read through web__run from the sources' own sites:
[MINLPLib download](https://www.minlplib.org/download.html),
[QPLIB documentation](https://qplib.zib.de/doc.html),
[CUTEst LICENSE](https://github.com/ralna/CUTEst/blob/master/LICENSE),
[SIF LICENSE](https://github.com/ralna/SIF/blob/master/LICENSE),
[MATPOWER software licence](https://matpower.org/license/) and
[MATPOWER manual Section 1.2](https://matpower.org/docs/MATPOWER-manual-8.0b1.pdf).
MINLPLib and QPLIB state CC BY 4.0; QPLIB reserves website copyright
separately. CUTEst and SIF each state three-clause BSD terms. MATPOWER
software uses BSD from 5.1; its manual excludes case data from that licence.
No licence was selected for our original data or code. The QPLIB root
timed out and /about/license/ was unavailable; the corrected primary
URLs above were accessible. No secondary source was relied on for terms.

Edits used apply_patch for the integration helpers/checker and final prose
cleanup; fix_review_r1.py made the initial three-document edit and saved
before-edit copies. It is a one-time edit, not an idempotent rewrite.

Exact terminal commands, in execution order (repeated checks are retained;
git diff --no-index exits 1 when it finds the intended changes):

```sh
pwd; git status --short; cat AGENTS.md; cat research-20260929/publication/reviews/integration-review-r1.md
sed -n '1,220p' research-20260929/publication/reviews/integration-review-r1.md; cat research-20260929/publication/READINESS.md; cat research-20260929/publication/integration/commands.md; rg --files -g AGENTS.md research-20260929
cat research-20260929/publication/integration/check_integration.py; sed -n '1,215p' research-20260929/open-instances-summary.md; sed -n '247,360p' research-20260929/open-instances-summary.md; sed -n '1,55p' research-20260929/publication/READINESS.md
sed -n '163,214p' research-20260929/open-instances-summary.md; sed -n '250,310p' research-20260929/open-instances-summary.md; sed -n '275,291p' research-20260929/bound-audit/audit-report.md; sed -n '655,682p' research-20260929/bound-audit/audit-report.md; sed -n '737,756p' research-20260929/bound-audit/audit-report.md; sed -n '903,940p' research-20260929/bound-audit/audit-report.md; sed -n '1350,1380p' research-20260929/bound-audit/audit-report.md
cat research-20260929/publication/reproduction/environment.json; cat research-20260929/publication/reproduction/requirements.txt; python3 - <<'PY'
import json
from pathlib import Path
p=Path('research-20260929/publication/reproduction/commands.json')
x=json.loads(p.read_text());print(type(x).__name__)
if isinstance(x,dict):
 print(x.keys())
 for k,v in x.items():
  print(k, type(v).__name__,len(v) if hasattr(v,'__len__') else '');print(str(v)[:5000])
else:print(len(x));print(x[:4])
PY
uname -a; lscpu; cat /proc/meminfo; python3 --version; ldd --version
cat research-20260929/publication/reviews/integration-r1/agent-lit/findings.md; cat research-20260929/publication/reviews/integration-r1/scratch/my_gaps.py; cat research-20260929/publication/reviews/integration-r1/scratch/my_gaps2.py; sed -n '1,70p' research-20260929/publication/integration/check_numbers.py
sed -n '75,110p' research-20260929/publication/minlplib-status/report.md; sed -n '78,105p' research-20260929/publication/scip-bug/report.md; cat research-20260929/publication/audit-ir/logs/xcheck_scip.log; cat research-20260929/publication/reviews/solver-campaign-r2/PROGRESS.json; sed -n '1,110p' research-20260929/publication/reviews/solver-analysis-review-r1.md; sed -n '365,410p' research-20260929/publication/solver-runs/report.md; sed -n '1,115p' research-20260929/publication/reviews/minor-fixes-review-r2.md
python3 - <<'PY'
import json
from collections import Counter
from pathlib import Path
x=json.loads(Path('research-20260929/publication/reproduction/commands.json').read_text())
print('families',Counter(v['id'].split('/')[0] for v in x))
for v in x:
 if v['id'].split('/')[0] in ('control','small','cops','powerflow','water','ann','kan','eg') or any(s in v['id'] for s in ('lnts','dtoc5','lukvle','bound','certify','verify','pindyck','audit')):
  print(v['id'],v['wall_s'],v['exit'],v['command'],v['output'])
PY
cat /etc/os-release; rg -n 'GAMS Release|GAMS [0-9]|Version|version' research-20260929/publication/solver-runs/runs/camshape100__{BARON,GUROBI,SCIP}/gams.log research-20260929/publication/solver-runs/report.md; rg -n 'wall|CPU|seconds|41151' research-20260929/publication/eg-recheck/report.md research-20260929/open-instances-wave3/eg/retry.md; rg --files research-20260929/publication/literature | rg '(qplib|license|goss|correction|matpower|sif)'
python3 - <<'PY'
import json, importlib.util
from pathlib import Path
x=json.loads(Path('research-20260929/publication/reproduction/commands.json').read_text())
for v in x:
 if v['id'].startswith(('network/','water-audit/')) and not any(s in v['id'] for s in ('primal','vbb','verify_exact','crosscheck','rbb','rebound','samples')):
  print(v['id'],v['wall_s'],v['exit'])
for m in ('markdown_it','mistune','markdown'):
 print('PARSER',m,importlib.util.find_spec(m))
PY
sed -n '85,105p' research-20260929/publication/minlplib-status/report.md; sed -n '82,103p' research-20260929/publication/scip-bug/report.md; cat research-20260929/publication/audit-ir/logs/xcheck_scip.log; sed -n '420,431p' research-20260929/publication/literature/small/report.md; sed -n '165,180p' research-20260929/publication/literature/small/report.md; sed -n '409,419p' research-20260929/publication/literature/control/report.md; cat research-20260929/publication/solver-runs/point_checks.log
sed -n '1,45p' research-20260929/publication/integration/check_publication_counts.py; sed -n '160,175p' research-20260929/publication/eg-recheck/report.md; rg --files research-20260929/publication/eg-recheck/res | head -8; head -35 research-20260929/reviews/eg-retry-review-checks/logs/verify_disc_p0.log; head -35 research-20260929/reviews/eg-retry-review-checks/logs/verify_disc_p1.log; rg -n 'argv|theta|Fraction|Q\(' research-20260929/reviews/eg-retry-review-checks/verify_tree.py; sed -n '77,90p' research-20260929/publication/literature/control/report.md; sed -n '257,274p' research-20260929/publication/literature/control/report.md; sed -n '299,314p' research-20260929/publication/literature/control/report.md; sed -n '525,539p' research-20260929/publication/literature/control/report.md; sed -n '140,148p' research-20260929/publication/literature/network/report.md; sed -n '174,193p' research-20260929/publication/literature/network/report.md; sed -n '1,24p' research-20260929/publication/minlplib-status/report.md; sed -n '1,10p' research-20260929/open-instances-wave3/eg/retry/logs/disc9_p1.log; sed -n '442,455p' research-20260929/reviews/closing-audit-a.md
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/collect_environment_r1.py > research-20260929/publication/integration/environment-r1.log
cat research-20260929/publication/integration/environment-r1.log; cat research-20260929/publication/integration/runtime-table-r1.md; python3 - <<'PY'
from markdown_it import MarkdownIt
from pathlib import Path
p=MarkdownIt('commonmark').enable('table')
for rel in ('open-instances-summary.md','bound-audit/audit-report.md','publication/READINESS.md'):
 t=Path('research-20260929')/rel;s=t.read_text(); ts=p.parse(s)
 covered=set();fences=set()
 for x in ts:
  if x.type=='table_open': covered.update(range(*x.map));print(rel,x.map)
  if x.type=='fence':fences.update(range(*x.map))
 print('ORPHANS',[(i+1,l[:90]) for i,l in enumerate(s.splitlines()) if l.startswith('|') and i not in covered and i not in fences])
PY
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_numbers.py > research-20260929/publication/integration/review-r1-numbers.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/recompute_objectives.py > research-20260929/publication/integration/review-r1-objectives.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_publication_counts.py > research-20260929/publication/integration/review-r1-counts.log
rg -n 'CPU|cpu|time|wall' research-20260929/publication/eg-recheck/logs/p0_c0.log research-20260929/publication/eg-recheck/logs/run_cert.log; rg --files research-20260929/publication/eg-recheck/logs | head -18; cat research-20260929/publication/integration/gap-values.json | head -20; rg -n 'camshape100|camshape_opt' research-20260929/publication/integration/check_numbers.py; rg -n 'pair2236|65\.12|56\.49|55\.6898' research-20260929/publication/scip-bug/report.md; head -25 research-20260929/publication/literature/network/sources/matpower_case{30,39}.m; sed -n '1,35p' research-20260929/reviews/eg-retry-review-checks/indep_cert.py
tail -5 research-20260929/publication/eg-recheck/logs/cert_p0_c0.log; rg -n 'wall|5372|scheduler|411' research-20260929/publication/eg-recheck/logs/* | head -20; rg -n 'self.theta|Fr\(theta' research-20260929/reviews/eg-retry-review-checks/indep_cert.py; rg --files research-20260929/publication/literature/control/sources | rg 'goss|goess|2603'; cat research-20260929/publication/reviews/solver-campaign-r2/PROGRESS.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 - <<'PY'
import numpy as np
from pathlib import Path
p=Path('research-20260929/publication/eg-recheck/res/p0_c0.npz')
with np.load(p,allow_pickle=False) as x:
 print(x.files)
 for k in x.files:
  if x[k].size<10:print(k,x[k])
PY
pdftotext -layout research-20260929/publication/literature/control/sources/goess2026_clash_arXiv2603.16505v1.pdf research-20260929/publication/integration/goess2026-r1.txt
rg -n 'lnts(50|100|200|400)|Alexander Martin' research-20260929/publication/integration/goess2026-r1.txt | head -15
rg -n 'time\.|\btime=' research-20260929/publication/eg-recheck/recheck_leaves.py research-20260929/publication/eg-recheck/summarize.py research-20260929/publication/eg-recheck/run_cert.py; python3 - <<'PY'
from pathlib import Path
from fractions import Fraction as Q
import re
files=list(Path('research-20260929/publication/eg-recheck/logs').glob('cert_p*_c*.log'))
print('chunks',len(files));print('sum printed times',sum(int(re.search(r'; time (\d+)s',p.read_text())[1]) for p in files))
PY
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_review_r1_evidence.py > research-20260929/publication/integration/review-r1-evidence.log
python3 research-20260929/publication/integration/fix_review_r1.py > research-20260929/publication/integration/review-r1-edits.log
python3 - <<'PY'
import re
from markdown_it import MarkdownIt
from pathlib import Path
p=MarkdownIt('commonmark').enable('table')
for rel in ('open-instances-summary.md','bound-audit/audit-report.md','publication/READINESS.md'):
 f=Path('research-20260929')/rel;s=f.read_text().splitlines()
 for t in p.parse('\n'.join(s)):
  if t.type!='table_open':continue
  start,end=t.map;w=len(re.split(r'(?<!\\)\|',s[start]))
  for n in range(start,end):
   row=re.split(r'(?<!\\)\|',s[n])
   if len(row)!=w:print('WIDTH',rel,n+1,w,len(row),s[n][:200])
PY
cat research-20260929/publication/integration/review-r1-evidence.log; tail -8 research-20260929/publication/integration/review-r1-numbers.log; sed -n '905,949p' research-20260929/bound-audit/audit-report.md; tail -25 research-20260929/publication/READINESS.md
python3 research-20260929/publication/integration/check_integration.py > research-20260929/publication/integration/review-r1-document-checks.log
git diff --no-index -- research-20260929/publication/integration/review-r1-before/open-instances-summary.md research-20260929/open-instances-summary.md
git diff --no-index -- research-20260929/publication/integration/review-r1-before/audit-report.md research-20260929/bound-audit/audit-report.md
git diff --no-index -- research-20260929/publication/integration/review-r1-before/READINESS.md research-20260929/publication/READINESS.md
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_review_r1_evidence.py > research-20260929/publication/integration/review-r1-evidence.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 research-20260929/publication/integration/check_review_r1_evidence.py > research-20260929/publication/integration/review-r1-evidence.log
python3 research-20260929/publication/integration/check_integration.py > research-20260929/publication/integration/review-r1-document-checks.log
python3 research-20260929/publication/integration/verify_review_r1_documents.py > research-20260929/publication/integration/review-r1-render-checks.log
cat research-20260929/publication/integration/PROGRESS.json; cat research-20260929/publication/integration/review-r1-render-checks.log; tail -12 research-20260929/publication/integration/review-r1-document-checks.log; sed -n '47,57p' research-20260929/publication/READINESS.md; sed -n '670,686p' research-20260929/bound-audit/audit-report.md; sed -n '1380,1400p' research-20260929/bound-audit/audit-report.md; git diff --check -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/integration/; python3 -m py_compile research-20260929/publication/integration/check_integration.py research-20260929/publication/integration/collect_environment_r1.py research-20260929/publication/integration/check_review_r1_evidence.py research-20260929/publication/integration/fix_review_r1.py research-20260929/publication/integration/verify_review_r1_documents.py
```

Final progress/hash update and checks (all exited 0):

```sh
python3 - <<'PY'
import hashlib,json
from pathlib import Path
root=Path('/workspace/minlp-notes')
out=root/'research-20260929/publication/integration'
p=out/'PROGRESS.json';x=json.loads(p.read_text())
x['date']='2026-10-04'
x['phase']='integration review r1 response complete for owned issues; targeted checks passed'
x['review_r1']={'verdict':'issues','blockers':0,'major':3,'minor':12,'fixed_items':[1]+list(range(3,15)),'excluded_items':[2,15],'excluded_owner':'parallel package/track agent','second_independent_review':False,'runtime_disagreement':'eg chunk timings use time.time(): aggregate wall time, not CPU time'}
x['verification']['rendered_tables']={'summary':5,'audit':10,'readiness':4,'literature_body_rows':43,'original_broken_table_rejected':True}
x['verification']['fresh_review_evidence']='passed'
x['cores_used']='at most three concurrent single-thread checks; no solver runs'
x['pending_user_decisions'].append('choose licence(s) for original paper data/code; include applicable source notices')
x['final_document_sha256']={rel:hashlib.sha256((root/rel).read_bytes()).hexdigest() for rel in x['final_document_sha256']}
newfiles=[str(f.relative_to(root)) for f in out.rglob('*') if f.is_file() and '__pycache__' not in f.parts]
x['files_written']=sorted(set(x['files_written']+newfiles))
p.write_text(json.dumps(x,indent=2)+'\n')
print('Updated integration progress and final document hashes')
PY
python3 research-20260929/publication/integration/check_integration.py > research-20260929/publication/integration/review-r1-document-checks.log
python3 research-20260929/publication/integration/verify_review_r1_documents.py > research-20260929/publication/integration/review-r1-render-checks.log
python3 -m py_compile research-20260929/publication/integration/check_integration.py research-20260929/publication/integration/collect_environment_r1.py research-20260929/publication/integration/check_review_r1_evidence.py research-20260929/publication/integration/fix_review_r1.py research-20260929/publication/integration/verify_review_r1_documents.py
git diff --check -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/integration/
git status --short -- research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/integration/
python3 - <<'PY'
import hashlib,json
from pathlib import Path
root=Path('/workspace/minlp-notes');out=root/'research-20260929/publication/integration'
x=json.loads((out/'PROGRESS.json').read_text())
for rel,digest in x['final_document_sha256'].items():
 p=root/rel;raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==digest
 assert raw.endswith(b'\n')
 assert all(line.rstrip()==line for line in p.read_text().splitlines()),rel
print('PASS final document hashes, final newline and whitespace (including untracked READINESS.md)')
assert 'ALL DOCUMENT CHECKS PASSED' in (out/'review-r1-document-checks.log').read_text()
assert 'PASS all 15 issues accounted for' in (out/'review-r1-render-checks.log').read_text()
print('PASS retained final verification outputs')
PY
head -4 research-20260929/publication/integration/commands.md; tail -4 research-20260929/publication/integration/commands.md
```

The final whitespace check explicitly included untracked READINESS.md;
git diff --check by itself does not cover untracked files. Final document
hashes match PROGRESS.json. No subsequent main-document edit was made.

## Implementation response to integration review r2 (2026-10-04)

All nine findings were checked and accepted. Numerical corrections use
this task's own exact Fraction arithmetic on saved objectives and bounds.
The source terms were read from saved primary documents; the full local
MATPOWER 8.1 manual was extracted to check its citation section, and the
saved QPLIB primary page was checked. No outside contact was made.

| targeted command / check | final result |
|---|---|
| check_review_r2_evidence.py | 35 evidence checks passed; review-r2-evidence.log/.json. Historical gaps are 1.2157e-6 and 3.8248e-5, bounded upward by 1.3e-6 and 3.9e-5. All replacement primal/gap directions passed. |
| git check-ignore -v; git status --short --ignored; check_review_r2_documents.py | 363 literature source copies ignored; 65 reports/checks/logs/manifests visible; 343 distinct commit dependencies visible, excluding source copies. Root literature/ status unchanged. Labels-only AST comparison, response-section anchors, decisions and Python syntax passed. |
| check_integration.py | All final gap cells, counts, local links and Markdown table checks passed, including the negative control for the old broken literature table. Link inspection uses parsed Markdown, so literal Markdown in the exact command transcript is treated as code. |
| build_result_maps.py | 43 summary instances / 46 audit instances; 54 EG command records; binding eg_disc_s part 1 and required command inputs checked. |
| rebuild_manifest.py | 2,542 files inventoried; experiments_run = 0; rebuilt on 2026-10-04. All-leaf scopes populated; literature source copies excluded. |
| default check_package.py | All five groups passed: manifest/maps/syntax/patches/smoke. No stale hashes. 2,425 mapped numeric references; 150 Python and 6 shell checks, 23 EG scripts; 12 patch replays, 154 identical outputs; the two previously inspected non-packaging differences preserved. 25 prior smoke records and 3 prior EG records revalidated. |
| check_eg_relocated.py | Three fresh sequential scientific smoke checks passed in disposable copies: summary 1,114,361 leaves / zero failures; subset 29/29; unchanged certifier 64/64. Zero successful source-tree opens. New output and scientific trees cleaned after retaining logs; original 8 evidence hashes unchanged. The old leaked tree named by the reviewer was also removed. |
| scoped git diff --check and explicit authored-file whitespace checks | Passed, including untracked readiness/package prose. |

The corrected reports label chunk timings as summed wall times.
The exact stored sum is 41162.1982879638671875 seconds; scheduler elapsed
time is 5,372 seconds. No full all-leaf recheck, tree generation or solver
campaign was rerun. Scientific scripts ran only in disposable copies,
with at most four CPU cores and one BLAS/OpenMP thread. The retained
25 package smoke commands were revalidated, not rerun.

During development the evidence helper's initial assertions exposed an
incomplete licence excerpt and manifest entries marked “not saved”.
The helper now reads the full saved manual and verifies available primary
files, including the earlier local download cache. Its final 35 checks
all pass. These were evidence-fixture corrections, not scientific failures.

Edits through apply_patch and the recorded one-time edit script covered
.gitignore; the summary/audit/readiness and requested track/package reports;
EG timing label strings; package map, command-evidence and smoke tooling;
and integration evidence/check records. No mathematical code in summarize.py
changed: comparison with HEAD confirms only its two timing labels differ.

Exact terminal commands follow. Heredoc stdin is preserved, including
the one-time document/dependency edits. The initial reads preceded the
implementation command recorder. The final sequence was repeated after
the last integration-checker edit and completed in the required order;
covered scientific/package files did not change afterwards. Source copies
stay local with hashes in tracked manifests. No staging, commit, push,
CI inspection, project-wide verification or outside contact occurred.
There is no disagreement with the review.

```sh
pwd; git status --short; rg --files -g 'AGENTS.md' -g '.gitignore' -g '*integration-review-r2*' -g '*files-to-commit*' -g '*commands.md'

cat research-20260929/publication/reviews/integration-review-r2.md

cat AGENTS.md; cat .gitignore; cat research-20260929/publication/READINESS.md

cat research-20260929/publication/reproduction/tools/eg_evidence.py; cat research-20260929/publication/reproduction/tools/check_eg_relocated.py; cat research-20260929/publication/integration/commands.md

sed -n '85,285p' research-20260929/publication/READINESS.md

cat research-20260929/publication/reproduction/tools/eg_evidence.py

cat research-20260929/publication/reproduction/tools/check_eg_relocated.py

cat research-20260929/publication/reviews/integration-r2/agent-repro/findings.md; cat research-20260929/publication/reviews/integration-r2/agent-licence/findings.md; cat research-20260929/publication/reviews/integration-r2/scratch/new_numbers.py

cat research-20260929/publication/reproduction/tools/build_result_maps.py

cat research-20260929/publication/reproduction/tools/rebuild_manifest.py; cat research-20260929/publication/reproduction/tools/check_package.py; cat research-20260929/publication/reproduction/tools/finish_paths.py

sed -n '150,225p' research-20260929/publication/reproduction/report.md; sed -n '335,405p' research-20260929/publication/reproduction/report.md; sed -n '230,310p' research-20260929/publication/reproduction/README.md; head -45 research-20260929/publication/reproduction/files-to-commit.json

rg -n 'Response|response|parent|orchestrat' research-20260929/publication/{minlplib-status,literature/small,solver-runs,reproduction}/report.md; rg --files research-20260929/publication/literature | rg '(manifest|MANIFEST|SHA|sources/)'

cat research-20260929/publication/reproduction/tools/check_package.py

cat research-20260929/publication/reproduction/tools/finish_paths.py; head -28 research-20260929/publication/reproduction/files-to-commit.json; tail -25 research-20260929/publication/reproduction/files-to-commit.json

sed -n '165,225p' research-20260929/publication/reproduction/report.md; sed -n '343,397p' research-20260929/publication/reproduction/report.md; sed -n '235,309p' research-20260929/publication/reproduction/README.md

rg -n 'Response|response|parent|orchestrat' research-20260929/publication/{minlplib-status,literature/small,solver-runs,reproduction}/report.md; rg --files research-20260929/publication/literature | rg '/sources/(MANIFEST.md|manifest.tsv|SHA256SUMS)$'; sed -n '80,103p' research-20260929/publication/scip-bug/report.md; sed -n '295,306p' research-20260929/open-instances-summary.md; sed -n '187,196p' research-20260929/open-instances-summary.md; sed -n '350,357p' research-20260929/open-instances-summary.md

sed -n '1,65p' research-20260929/publication/reviews/integration-r2/agent-licence/sources/optrove-sif-LICENSE; rg --files research-20260929/publication/reviews/integration-r2/agent-licence/sources

sed -n '1,150p' research-20260929/publication/integration/check_numbers.py; sed -n '1,100p' research-20260929/publication/reviews/integration-r2/agent-repro/check_eg_displays.py; sed -n '270,283p' research-20260929/publication/literature/network/report.md; sed -n '385,396p' research-20260929/publication/literature/small/report.md; sed -n '461,474p' research-20260929/publication/literature/small/report.md; sed -n '508,521p' research-20260929/publication/literature/small/report.md

cat research-20260929/publication/reviews/integration-r2/agent-licence/sources/{bitbucket_optrove_sif_LICENSE,matpower_LICENSE,MATPOWER-manual-8.1_sec1.2.txt}; sed -n '1,65p' research-20260929/publication/literature/control/sources/MANIFEST.md; head -15 research-20260929/publication/literature/network/sources/MANIFEST.md; head -3 research-20260929/publication/literature/small/sources/manifest.tsv

cat research-20260929/reviews/eg-retry-review-checks/record_run.py; head -65 research-20260929/open-instances-wave3/eg/retry/egbb.py; head -60 research-20260929/publication/reviews/eg-recheck-r1/own_sample.py; rg -n 'minF|osil|ev|egfast|egtm|\.sol' research-20260929/{reviews/eg-retry-review-checks/indep_cert.py,open-instances-wave3/eg/retry/egbb.py,publication/reviews/eg-recheck-r1/own_sample.py}; sed -n '30,55p' research-20260929/publication/eg-recheck/report.md; sed -n '155,168p' research-20260929/publication/eg-recheck/report.md; rg -n CPU research-20260929/publication/eg-recheck/summarize.py

head -12 research-20260929/publication/literature/{control,network}/sources/MANIFEST.md; head -3 research-20260929/publication/literature/small/sources/manifest.tsv; rg -n 'CPU|cpu|41,162' research-20260929/publication/eg-recheck/report.md; sed -n '320,327p' research-20260929/publication/reproduction/report.md; head -100 research-20260929/publication/reproduction/tools/smoke.py; sed -n '910,944p' research-20260929/publication/literature/small/report.md; cat research-20260929/publication/scip-bug/logs/scan_summary.csv | head -5

head -25 research-20260929/publication/scip-bug/logs/binary_p4.log; rg -n '10.1.0|GAMS|p4|optimal' research-20260929/publication/scip-bug/logs/scan_summary.csv | head -18; head -15 research-20260929/publication/primal/water-ann-kan/points/waterno2_09.exact.json; sed -n '80,96p' research-20260929/open-instances-summary.md; rg -n 'time.time' research-20260929/publication/eg-recheck/recheck_leaves.py; sed -n '934,944p' research-20260929/bound-audit/audit-report.md; sed -n '48,58p' research-20260929/publication/reviews/eg-recheck-review-r1.md; sed -n '76,85p' research-20260929/publication/READINESS.md

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/integration/check_review_r2_evidence.py > research-20260929/publication/integration/review-r2-evidence.log

cat research-20260929/publication/reviews/integration-r2/agent-licence/sources/MATPOWER-manual-8.1_sec1.2.txt; rg --files /tmp research-20260929/publication/reviews/integration-r2 | rg -i '(matpower.*(8.1|pdf)|qplib.*(index|html)|gams.*p4)' | head -20; tail -12 research-20260929/publication/integration/review-r2-evidence.log; rg --files research-20260929/publication/scip-bug/logs | rg '(gams|gscan)'

git status --short --ignored -- literature/ > research-20260929/publication/integration/review-r2-root-literature-before.log; git status --short --ignored -- research-20260929/publication/literature/ > research-20260929/publication/integration/review-r2-literature-before.log; git check-ignore -v research-20260929/publication/literature/small/report.md research-20260929/publication/literature/small/sources/manifest.tsv literature/ > research-20260929/publication/integration/review-r2-ignore-before.log

pdftotext -layout /tmp/lic/MATPOWER-manual-8.1.pdf research-20260929/publication/literature/network/sources/MATPOWER-manual-8.1.txt; cp /tmp/lic/qplib_index.html research-20260929/publication/literature/control/sources/qplib_index.html; cat research-20260929/publication/scip-bug/gams/logs/scan_p4.txt; rg -n -A 8 '1.3    Citing' research-20260929/publication/literature/network/sources/MATPOWER-manual-8.1.txt; rg -n 'please cite' research-20260929/publication/literature/control/sources/qplib_index.html

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/integration/check_review_r2_evidence.py > research-20260929/publication/integration/review-r2-evidence.log

cat research-20260929/publication/reviews/integration-r2/agent-licence/sources/SHA256SUMS; python3 - <<'PY'
import json
from pathlib import Path
p=Path('research-20260929/publication/reproduction/files-to-commit.json'); x=json.loads(p.read_text())
for k,v in x.items():
 print(k, len(v) if isinstance(v,list) else str(v)[:250])
 if isinstance(v,list):
  print('\n'.join(i for i in v if '/literature/' in i))
PY

python3 -B research-20260929/publication/integration/fix_review_r2.py > research-20260929/publication/integration/review-r2-edits.log; OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/integration/check_review_r2_evidence.py > research-20260929/publication/integration/review-r2-evidence.log

head -50 research-20260929/open-instances-wave3/eg/retry/{egfast,egtm}.py; head -50 research-20260929/publication/reviews/eg-recheck-r1/{own_ia,own_model}.py; rg -n 'check_eg_relocated|summarize.py|CPU' research-20260929/publication/reproduction/tools/check_review_response.py; rg -n 'summarize.py' research-20260929/publication/reproduction/patches/*.patch; git status --short --ignored -- literature/ > research-20260929/publication/integration/review-r2-root-literature-after.log; git status --short --ignored -- research-20260929/publication/literature/ > research-20260929/publication/integration/review-r2-literature-after.log; git check-ignore -v research-20260929/publication/literature/{small,control,network}/report.md research-20260929/publication/literature/{control,network}/sources/MANIFEST.md research-20260929/publication/literature/small/sources/manifest.tsv research-20260929/publication/literature/small/sources/eg/camino_ghezzi_et_al_arxiv2404.11786v2.pdf literature/ > research-20260929/publication/integration/review-r2-ignore-after.log; cat research-20260929/publication/integration/review-r2-ignore-after.log

test -f research-20260929/research_path.py; rg -n '^import |^from |sys.path|osil' research-20260929/open-instances-wave3/eg/retry/egdata.py research-20260929/open-instances-wave2/small/ev.py; rg -n '^import |^from ' research-20260929/open-instances-wave3/eg/retry/egfast.py; rg -n 'manifest|EXTRA|pending|rebuild' research-20260929/publication/reproduction/PROGRESS.json | head -20; sed -n '1,12p' research-20260929/bound-audit/audit-report.md

sed -n '47,57p' research-20260929/publication/READINESS.md; sed -n '312,327p' research-20260929/publication/reproduction/report.md; tail -18 research-20260929/publication/reproduction/report.md; sed -n '297,307p' research-20260929/publication/minlplib-status/report.md; cat research-20260929/publication/reproduction/PROGRESS.json

tail -9 research-20260929/publication/literature/{control,network}/sources/MANIFEST.md; tail -5 research-20260929/publication/integration/review-r2-evidence.log

python3 - <<'PY'
from pathlib import Path
p=Path('research-20260929/publication/READINESS.md')
s=p.read_text()
replacements=[
('Updated 2026-10-04: response to integration review r1.', 'Updated 2026-10-04: responses to integration reviews r1 and r2; final package rebuilt.'),
('explicitly. Final packaging remains pending.', 'explicitly. The final package rebuild and default package check passed on\n2026-10-04; release decisions and a user-authorized commit remain pending.'),
('closure; For eg_disc_s', 'closure; for eg_disc_s'),
('The current host was captured on 2026-10-04 from /proc, uname and\n/etc/os-release:', 'The current computing environment, as seen inside the WSL2 VM, was\ncaptured on 2026-10-04 from /proc, uname and /etc/os-release:'),
('Although the track report calls the chunk total CPU time, recheck_leaves.py\nmeasures time.time(), so it is a sum of chunk wall times, not measured CPU\ntime.', 'The corrected track report and summarize.py label this sum as chunk wall\ntime: recheck_leaves.py measures time.time().'),
('Final packaging is deferred\nbecause integration changed summary rows and concurrent track edits can\ninvalidate hashes. It must be done after all those edits stop.', 'This implementation task owns the final map and manifest rebuild. It ran\nbuild_result_maps.py, rebuild_manifest.py and the default check_package.py\non 2026-10-04 after all covered edits were final; all passed. Covered edits\nafter that date require another rebuild and default check.'),
('checked by the parent orchestrator against the reviews.', 'checked by the parent orchestrator against the reviews; see the [saved response](minlplib-status/report.md#response-to-review-round-2).'),
('the parent checked the final small-literature minor fixes against its reviews.', 'the parent checked the final small-literature minor fixes against its reviews; see the [saved response and checks](literature/small/report.md#18-response-to-review-round-3-2026-10-03).'),
('collect.py diff additive only, per-row flags and report wording.', 'collect.py diff additive only, per-row flags and report wording; see the [saved response](solver-runs/report.md#response-to-review-round-1).'),
('the parent spot-checked those fixes. No second independent package review round was performed. Final manifest intentionally awaits integration.', 'the parent spot-checked those fixes; see the [saved package response](reproduction/report.md#response-to-review-round-1) and [integration response](reproduction/report.md#response-to-integration-review-r1). No second independent package review round was performed. Maps and manifest were rebuilt and the default package check passed on 2026-10-04.'),
('Final map/manifest synchronization and commit dependencies remain to be checked.', 'eg_disc2_s all-leaf evidence is mapped; manifest scopes include eg-recheck/ and reviews/eg-recheck-r1/. Final map/manifest synchronization and commit dependencies passed targeted checks; copied copyrighted literature stays local, with hashes in tracked manifests.'),
('The parent spot-checked those fixes, and integration review r1 covers them;', 'The parent spot-checked those fixes, recorded in the [round-3 response](reviews/minor-fixes/response-r3.md), and integration review r1 covers them;'),
('the parent spot-checked those fixes, and integration review r1 covers them.', 'the parent spot-checked those fixes, recorded in the [round-3 response](reviews/minor-fixes/response-r3.md), and integration review r1 covers them.'),
('Items 2 and 15 belong to the parallel owner.', 'Items 2 and 15 were resolved by the package owner; this r2 response closes\nthe remaining track displays and the final manifest rebuild.'),
('| 2, major: eg_disc2_s package coverage | Excluded from this implementation as instructed; the parallel package owner handles the all-leaf evidence and package descriptions. No package file was changed here. |', '| 2, major: eg_disc2_s package coverage | Resolved by the package owner; see [reproduction/report.md, Response to integration review r1](reproduction/report.md#response-to-integration-review-r1): README, result map, 54 EG command records and relocated smoke checks. This task completed the manifest rebuild on 2026-10-04. |'),
('Restored 1.2e-6 for camshape100 and 3.8e-5 for lnts50', 'Restored 1.3e-6 for camshape100 and 3.9e-5 for lnts50 (upward bounds corrected in r2)'),
('| 15: stale track/package displays | Excluded as instructed; handled by the parallel track/package owner. The summary\'s checked displays remain authoritative. |', '| 15: stale track/package displays | Resolved by the package owner; see [reproduction/report.md, Response to integration review r1](reproduction/report.md#response-to-integration-review-r1). The remaining track displays identified in integration review r2 issue 7 are corrected below. |'),
('For item 10, the parent\'s checks are recorded as the user specified, not\nmislabelled as a second independent review.', 'For item 10, the parent\'s checks link to the saved response sections above;\nthey are not a second independent review.'),
]
for old,new in replacements:
 assert old in s, old
 s=s.replace(old,new)
# Licence rows use the terms of the source actually obtained.
s=s.replace('terms: retain copyright, conditions and disclaimer;', 'terms: retain or reproduce copyright, conditions and disclaimer;')
s=s.replace('Preserve problem-source credits in the SIF files. |', 'Preserve problem-source credits in the SIF files. HVYCRASH.SIF came from ralna/SIF. The four control SIF files came from [bitbucket.org/optrove/sif](https://bitbucket.org/optrove/sif/src/master/LICENSE) (MIT, © 2022 Nick Gould, Dominique Orban and Philippe Toint); they are byte-identical to the ralna/SIF copies. Include the notice of the source actually redistributed. |')
s=s.replace('[manual, Section 1.2](https://matpower.org/docs/MATPOWER-manual-8.0b1.pdf)', '[manual 8.1, Section 1.2](https://matpower.org/docs/MATPOWER-manual-8.1.pdf)')
s=s.replace('data were included by permission or converted from public sources.', 'data were "in most cases" included by permission or converted from public sources.')
s=s.replace('These source terms do not choose a licence', 'MATPOWER (manual 8.1, Section 1.3) and [QPLIB](https://qplib.zib.de/) request\ncitation when their data are used. Saved primary-source licence evidence\nand verified hashes are in [review-r2-evidence.log](integration/review-r2-evidence.log).\n\nThese source terms do not choose a licence')
start=s.index('3. **Commit the publication work and final package refresh:**')
end=s.index('4. **Release licence:**', start)
s=s[:start]+'''3. **Commit the publication work:** when authorized, commit the untracked
   publication files with all modified dependencies in
   [files-to-commit.json](reproduction/files-to-commit.json) and the
   minor-fixes lists. Include .gitignore, literature reports, checks, logs
   and source SHA-256 manifests. Copied sources in each literature sources/
   folder stay local and untracked; their hashes are in the tracked
   manifests. The paper's data release must not redistribute copyrighted
   sources. The root literature/ collection remains ignored. No staging,
   commit or push was performed. The protected historical
   solver-runs/report.prev.md cleanup remains with its owner.

   This implementation task completed the final package refresh on
   2026-10-04, after all covered edits: build_result_maps.py, then
   rebuild_manifest.py, then the default check_package.py, all passed.
   Repeat those commands if covered files change before committing; require
   the default package check to pass. Exact commands and outputs are in
   [commands.md](integration/commands.md).

'''+s[end:]
start=s.index('**Release preparation still pending:**')
end=s.index('Upstream filing and additional solver reruns', start)
s=s[:start]+'''**Release preparation still pending:** the protected historical
solver-runs/report.prev.md display cleanup; choosing the data/code release
licence and preparing third-party notices; publishing a persistent public
archive with a DOI and a data/code-availability statement; adding the
required MINLPLib, QPLIB, MATPOWER and Göß–Burlacu–Martin publisher-correction
citations; presenting timings as wall times from reproduction runs on a
shared machine; and committing the complete dependency set when authorized.
Source copies stay local and untracked, with hashes in tracked manifests;
the public data release must not redistribute copyrighted sources.

**Open user decisions:** file the drafted SCIP report; optionally notify
MINLPLib maintainers about invalid listed bounds and BARON developers about
the two contradicted optimality claims; rerun the 10 overloaded or 3
memory-limited solver runs; and choose the release licence. No outside
contact or solver rerun was performed by this task.

The independent integration review r2 found issues (0 blockers, 1 major,
8 minor). This response resolves all nine findings. Items 2 and 15 of r1
were resolved by the package owner; the residual displays in r2 issue 7
are now corrected. The maps and manifest were rebuilt on 2026-10-04 and
the default package check passed. These are implementation checks, not a
new independent review verdict.
'''+s[end:]
s+='''

## Response to integration review r2

The [review](reviews/integration-review-r2.md) returned **issues**: 0 blockers,
1 major and 8 minor. I checked the review evidence before changing each
claim, using my own exact Fraction arithmetic for the numbers. The
[exact evidence](integration/review-r2-evidence.log) and
[commands/results](integration/commands.md) record this implementation.

| issue | resolution |
|---|---|
| 1, major: ignored literature | Negation rules expose the literature reports, checks, logs and source manifests while keeping all copied sources local and ignored. files-to-commit.json excludes those copies. git check-ignore and status checks confirm the policy and unchanged root literature/ status. Copyrighted sources must not be redistributed in the paper data release. |
| 2: historical closeness | Exact checks give 1.2157e-6 and 3.8248e-5; upward bounds are 1.3e-6 and 3.9e-5 in the summary, this record and the control report. |
| 3: SCIP seeds | Summary and audit now state seed and version dependence; p4 failed for all 10 tried seeds on 10.1.0 and GAMS/SCIP. Raw scan logs were checked. |
| 4: timing labels | EG report, summarize.py and reproduction README now say wall time summed over chunks. The original independent review has an appended clarification. Timing data are unchanged; no full recheck was rerun. |
| 5: readiness and rebuild ownership | r1 items 2 and 15 are resolved. This implementation task owns and completed the final map/manifest rebuild and default package check on 2026-10-04. The all-leaf scopes are explicit above. |
| 6: source terms | optrove/sif is MIT; ralna/SIF is BSD. MATPOWER data terms retain "in most cases" and cite manual 8.1. MATPOWER and QPLIB citation requests are recorded. |
| 7: displays and prose | EG and water primal displays round upward from saved exact objectives; the water gaps round upward. Martin is spelled consistently. All 13 former tolerance-only closures now have exactly feasible points. The all-leaf EG status is current. |
| 8: package evidence and smoke tool | Recorded-tree inputs include the pinned OSIL, listed point and producer modules; interval samples include OSIL and sample C's minF inputs. eg_disc_s maps the binding part-1 bound and documents its binary64 caveat. The smoke tool writes fresh output, cleans its temporary scientific copy and documents bwrap/strace. |
| 9: wording and records | Fixed the case typo, Gurobi 13.0.0/status caveat, audit date and WSL2 VM scope. Parent-check statements link to saved response sections and retain the distinction from an independent review. |

Final commands ran in the required order: build_result_maps.py,
rebuild_manifest.py, default check_package.py, then the targeted relocated
EG smoke checks. All passed. Scientific scripts ran only in disposable
copies, sequentially with one BLAS/OpenMP thread and at most four CPU cores.
The existing 25 package smoke records were revalidated by the default
check; the three EG smoke checks were executed afresh. No project-wide
verification, CI inspection, staging, commit, push or outside contact occurred.

There is no disagreement with the review. Publishing an archive, release
licence choice, citations, upstream filing, optional notifications and solver
reruns remain the paper-preparation decisions listed above.
'''
p.write_text(s)
PY

python3 - <<'PY'
import json
from pathlib import Path
p=Path('research-20260929/publication/reproduction/PROGRESS.json'); x=json.loads(p.read_text())
x['remaining']=[]
x['done'].append('Integration review r2: all nine issues addressed; final maps and manifest rebuilt on 2026-10-04; default package check and targeted relocated EG smoke checks passed')
x['open_issues']=[s for s in x['open_issues'] if not s.startswith('Default package check intentionally fails')]
x['integration_review_r2']={'date':'2026-10-04','owner':'this integration implementation task','review':'research-20260929/publication/reviews/integration-review-r2.md','status':'resolved_final_package_checked','fixed_items':list(range(1,10)),'agreement':'all nine findings accepted','main_manifest_rebuilt':True,'default_package_check':'publication/integration/review-r2-package-check.log','eg_smoke_checks':3,'full_recheck_repeated':False,'commands':'publication/integration/commands.md'}
p.write_text(json.dumps(x,indent=2)+'\n')
p=Path('research-20260929/publication/reproduction/report.md')
with p.open('a') as f:
 f.write('''\n\n## Response to integration review r2\n\nAll nine findings in integration-review-r2.md were checked against saved\nevidence and accepted. Exact Fraction checks confirm the upward EG and\nwater primal displays and historical closeness bounds. The original\nclosures used tolerance-feasible points; exactly feasible points now\ncover all 13 in publication/primal/.\n\nThe command index now names the recorded-tree OSIL, listed point and\nproducer modules, plus OSIL and sample C minF inputs for the interval\nsamples. The result map selects eg_disc_s part 1, the smaller bound. The\nREADME retains its exact-decimal-versus-binary64 qualification and labels\nEG timing totals as summed wall time. The relocated smoke tool writes\nfresh output, requires bwrap/strace and removes its scientific copy.\nIt preserves the original integration-r1 smoke records.\n\nLiterature reports, checks, logs and SHA-256 source manifests are commit\ndependencies. Source copies stay local and untracked; the paper data\nrelease must not redistribute copyrighted sources. No release licence\nwas chosen, and no staging, commit, push or outside contact occurred.\n\nThis integration implementation task owns the final rebuild. On\n**2026-10-04**, after all covered edits were final, it ran\n**build_result_maps.py**, then **rebuild_manifest.py**, then the\n**default check_package.py**, followed by the three targeted relocated\nEG smoke checks; all passed. The 25 earlier smoke records were\nrevalidated by the default check. Scientific execution was confined to\ndisposable copies with at most four CPU cores and one BLAS/OpenMP thread.\nExact commands and outputs are recorded in\n[publication/integration/commands.md](../integration/commands.md) and\n[review-r2-package-check.log](../integration/review-r2-package-check.log).\nThese are targeted local checks; no CI or project-wide verification ran.\nThere is no disagreement with the review.\n''')
# Keep appended primary-source manifest entries inside their own tables.
for family in ('control','network'):
 p=Path('research-20260929/publication/literature')/family/'sources/MANIFEST.md'
 s=p.read_text(); marker='\n| '+('qplib_index.html' if family=='control' else 'MATPOWER-manual-8.1.txt')+' |'
 assert marker in s
 header='\n## Integration review r2 source check (2026-10-04)\n\n'+('| file | source URL / origin | sha256 |\n|---|---|---|\n' if family=='control' else '| file | URL / origin | bytes | sha256 |\n|---|---|---|---|\n')
 s=s.replace(marker,header+marker.lstrip('\n'));p.write_text(s)
PY

cat research-20260929/publication/integration/check_integration.py; sed -n '1,55p' research-20260929/publication/reproduction/tools/check_integration_displays.py; rg -n 'manifest|CPU|sif|1.2e-6|3.8e-5|parallel|Excluded' research-20260929/publication/{READINESS.md,reproduction/README.md,reproduction/report.md} | tail -25; sed -n '1,55p' research-20260929/publication/scip-bug/witness* 2>/dev/null

rg --files /tmp/lic | head -30; git ls-files -- research-20260929/publication/eg-recheck/summarize.py; rg -n 'mart|Mart|sha|SIF' research-20260929/publication/reviews/integration-r2/agent-licence/* 2>/dev/null | head -12; rg --files research-20260929/publication/literature/network/checks | head -4

rg --files --hidden --no-ignore research-20260929/publication/reviews research-20260929/literature | rg '(DTOC5|LUKVLE10|OPTCDEG2|OPTCNTRL)\.SIF$'; git diff -- research-20260929/publication/eg-recheck/summarize.py; git diff --numstat -- .gitignore research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/eg-recheck/report.md; rg -n 'minF' research-20260929/publication/reproduction/inputs/saved-inputs.json | head -4

rg --files research-20260929/publication/scip-bug | rg '(witness|p4).*json$' | head -12; rg -n 'ralna|bitbucket|DTOC5' research-20260929/publication/reviews/lit-control-r2/web/*md research-20260929/publication/reviews/lit-control-r2/*md 2>/dev/null | head -8; git diff -- research-20260929/publication/eg-recheck/summarize.py > research-20260929/publication/integration/review-r2-summarize-label.diff

head -15 research-20260929/publication/scip-bug/witness/p4.json; tail -n 4 research-20260929/publication/scip-bug/witness/p4.json; rg -n '^def |gaps|BOUND|float|num' research-20260929/publication/reproduction/tools/eg_evidence.py | tail -3; git diff -- .gitignore

python3 - <<'PY'
from pathlib import Path
p=Path('research-20260929/publication/READINESS.md');s=p.read_text();s=s.replace('The only numerical interpretation disagreement found here concerns the eg\nruntime label: the saved timing fields measure wall time, despite the track\nreport\'s CPU label. The environment section uses the actual measurement.', 'At r1 the only numerical interpretation disagreement concerned the eg\nruntime label: the saved timing fields measured wall time despite the then\nCPU label. This r2 response agrees with the reviewer and corrects that label.')
p.write_text(s)
PY

python3 -B research-20260929/publication/integration/check_review_r2_documents.py > research-20260929/publication/integration/review-r2-document-policy.log

python3 -B research-20260929/publication/integration/check_integration.py > research-20260929/publication/integration/review-r2-document-checks.log

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/build_result_maps.py > research-20260929/publication/integration/review-r2-map-build.log

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/rebuild_manifest.py > research-20260929/publication/integration/review-r2-manifest-build.log

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/check_package.py > research-20260929/publication/integration/review-r2-package-check.log

python3 - <<'PY'
import hashlib,json
from pathlib import Path
p=Path('research-20260929/publication/reproduction/logs')
files=list((p/'integration-r1-eg').rglob('*'))+[p/'integration-r1-eg-smoke.json']
x={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in files if f.is_file()}
Path('research-20260929/publication/integration/review-r2-smoke-original-hashes.json').write_text(json.dumps(x,indent=2)+'\n')
print('Recorded',len(x),'original smoke-evidence hashes')
PY

OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/check_eg_relocated.py > research-20260929/publication/integration/review-r2-eg-run.log

python3 - <<'PY'
import hashlib,json,re,shutil
from pathlib import Path
P=Path('research-20260929/publication');out=P/'integration'
log=(out/'review-r2-eg-run.log').read_text();print(log)
source=Path(re.search(r'outputs: (.+)',log)[1])
r=json.loads((source/'results.json').read_text())
assert not Path(r['tree']).exists(),'temporary scientific tree leaked'
assert len(r['cpus'])<=4
assert all(v['exit']==0 and v['successful_main_tree_opens']==0 for v in r['checks'])
old=json.loads((out/'review-r2-smoke-original-hashes.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in old.items())
shutil.copytree(source,out/'review-r2-eg-smoke')
shutil.rmtree(source)
assert not source.exists()
print('PASS fresh default output directory; scientific tree and /tmp output cleaned; 8 original smoke records unchanged')
result=json.loads((P/'reproduction/result-map.json').read_text())
row=next(r for r in result if r['instance']=='eg_disc_s')
lb=next(r for r in row['numeric_evidence'] if r['quantity']=='lower bound')
assert lb['path'].endswith('disc9_p1.log') and lb['value']=='5.760539610694994'
x=json.loads((P/'reproduction/commands.json').read_text())
for v in x:
 if v['id'].startswith('eg-recheck/record-p'):
  assert any(p.endswith('eg_disc2_s.osil') for p in v['inputs'])
  assert any(p.endswith('eg_disc2_s.p1.sol') for p in v['inputs'])
  assert all(any(p.endswith(n+'.py') for p in v['inputs']) for n in ('egbb','egfast','egtm','ev'))
 if v['id'].startswith('eg-recheck/interval-sample-'):
  assert any(p.endswith('eg_disc2_s.osil') for p in v['inputs'])
  if v['id'].endswith('-C'): assert sum('minF_' in p for p in v['inputs'])==7
print('PASS binding part-1 bound and required command inputs; 54 EG command records')
manifest=json.loads((P/'reproduction/manifest.json').read_text())
assert any('/eg-recheck/' in v['path'] for v in manifest['files'])
assert any('/reviews/eg-recheck-r1/' in v['path'] for v in manifest['files'])
assert not any('/literature/' in v['path'] and '/sources/' in v['path'] and Path(v['path']).name not in ('MANIFEST.md','manifest.tsv') for v in manifest['files'])
print('PASS all-leaf manifest scopes and literature source exclusion')
PY

cat research-20260929/publication/integration/review-r2-map-build.log research-20260929/publication/integration/review-r2-manifest-build.log research-20260929/publication/integration/review-r2-package-check.log research-20260929/publication/integration/review-r2-document-policy.log

python3 - <<'PY'
import hashlib,json
from pathlib import Path
root=Path.cwd();out=root/'research-20260929/publication/integration'
p=out/'PROGRESS.json';x=json.loads(p.read_text())
x['date']='2026-10-04';x['phase']='integration review r2 resolved; final package rebuild and targeted checks passed'
x['review_r2']={'verdict':'issues','blockers':0,'major':1,'minor':8,'fixed_items':list(range(1,10)),'agreement':'all nine issues accepted','independent_review_after_response':False,'manifest_owner':'this integration implementation task','manifest_rebuilt':'2026-10-04','package_check':'review-r2-package-check.log','evidence_checks':35,'literature_local_source_copies':363,'literature_visible_files':65,'commit_dependencies':343,'eg_smoke_checks':3,'full_recheck_repeated':False}
x['verification']['review_r2_default_package']=json.loads((out/'review-r2-package-check.log').read_text())
x['cores_used']='at most four CPU cores; sequential scientific smoke checks with one BLAS/OpenMP thread'
x['final_document_sha256']={rel:hashlib.sha256((root/rel).read_bytes()).hexdigest() for rel in x['final_document_sha256']}
x['files_written']=sorted(set(x['files_written']+[str(f.relative_to(root)) for f in out.rglob('*') if f.is_file() and '__pycache__' not in f.parts]))
p.write_text(json.dumps(x,indent=2)+'\n')
print('PASS integration progress and current main-document hashes updated; package-covered files unchanged')
PY

git diff --check -- .gitignore research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/literature research-20260929/publication/eg-recheck/report.md research-20260929/publication/eg-recheck/summarize.py research-20260929/publication/reviews/eg-recheck-review-r1.md research-20260929/publication/reproduction research-20260929/publication/integration > research-20260929/publication/integration/review-r2-diff-check.log

python3 - <<'PY'
import json,shutil
from pathlib import Path
p=Path('research-20260929/publication/reproduction/logs/integration-r1-eg-smoke.json')
old=Path(json.loads(p.read_text())['tree'])
assert old == Path('/tmp/repro-eg-integration-r1-81qsbigg')
if old.exists():
 assert (old/'research-20260929/publication/eg-recheck').is_dir()
 shutil.rmtree(old)
 print('PASS removed the old disposable tree identified by review r2:',old)
else:
 print('PASS old disposable tree already absent:',old)
PY
```

Final closeout commands:

```sh
python3 -B research-20260929/publication/integration/check_review_r2_documents.py > research-20260929/publication/integration/review-r2-document-policy.log
python3 -B research-20260929/publication/integration/check_integration.py > research-20260929/publication/integration/review-r2-document-checks.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/build_result_maps.py > research-20260929/publication/integration/review-r2-map-build.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/rebuild_manifest.py > research-20260929/publication/integration/review-r2-manifest-build.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/check_package.py > research-20260929/publication/integration/review-r2-package-check.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B research-20260929/publication/reproduction/tools/check_eg_relocated.py > research-20260929/publication/integration/review-r2-eg-final-run.log
git diff --check -- .gitignore research-20260929/open-instances-summary.md research-20260929/bound-audit/audit-report.md research-20260929/publication/READINESS.md research-20260929/publication/literature research-20260929/publication/eg-recheck/report.md research-20260929/publication/eg-recheck/summarize.py research-20260929/publication/reviews/eg-recheck-review-r1.md research-20260929/publication/reproduction research-20260929/publication/integration > research-20260929/publication/integration/review-r2-diff-check.log
```

Final smoke retention, cleanup and read-only hash/whitespace validation:

```sh
python3 - <<'PY'
import hashlib,json,re,shutil
from pathlib import Path
P=Path('research-20260929/publication');out=P/'integration'
log=(out/'review-r2-eg-final-run.log').read_text();source=Path(re.search(r'outputs: (.+)',log)[1])
r=json.loads((source/'results.json').read_text())
assert not Path(r['tree']).exists() and len(r['cpus'])<=4
assert len(r['checks'])==3 and all(v['exit']==0 and v['successful_main_tree_opens']==0 for v in r['checks'])
old=json.loads((out/'review-r2-smoke-original-hashes.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in old.items())
shutil.copytree(source,out/'review-r2-eg-smoke-final');shutil.rmtree(source)
assert not source.exists() and not Path('/tmp/repro-eg-integration-r1-81qsbigg').exists()
manifest=json.loads((P/'reproduction/manifest.json').read_text())
assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in manifest['files'])
check=json.loads((out/'review-r2-package-check.log').read_text())
assert check['all_passed'] and not check['stale_manifest'] and check['checked_groups']==['manifest','maps','syntax','patches','smoke']
paths=[P/'READINESS.md',P/'reproduction/README.md',P/'reproduction/report.md',out/'commands.md',out/'check_review_r2_evidence.py',out/'check_review_r2_documents.py',out/'fix_review_r2.py']
for p in paths:
 assert p.read_bytes().endswith(b'\n') and all(line.rstrip()==line for line in p.read_text().splitlines()),p
progress=json.loads((out/'PROGRESS.json').read_text())
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in progress['final_document_sha256'].items())
report=['PASS final manifest hashes unchanged after smoke and command recording','PASS all five default package groups; no stale hashes','PASS three fresh EG checks, zero source opens, at most four CPUs','PASS original smoke hashes unchanged; all new and identified old /tmp trees cleaned','PASS final main-document hashes and authored-file whitespace']
(out/'review-r2-final-validation.log').write_text('\n'.join(report)+'\n')
print(log+'\n'.join(report))
PY
```

Fresh final smoke argv, output hashes and timings are retained in
review-r2-eg-smoke-final/results.json; lifecycle checks are in
review-r2-final-validation.log. The original and final successful rebuild
outputs have identical counts. The final default package output is
review-r2-package-check.log.
