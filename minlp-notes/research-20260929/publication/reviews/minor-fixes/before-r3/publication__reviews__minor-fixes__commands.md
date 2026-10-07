# Commands and results for the minor-fix revision

All commands below ran from `/workspace/minlp-notes`. Numerical checks used one thread per process. At most four independent small checks ran concurrently; the work never exceeded four CPU cores. No main construction, solver campaign, project-wide verification or CI inspection was performed. The older commands preserved in the reports belong to the original tracks, not this revision.

## Targeted checks actually run

### primal/chain

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/chain/minor_review_check.py > research-20260929/publication/primal/chain/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../primal/chain/logs/minor_review_check.log).

### primal/dtoc5-lukvle10

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/dtoc5-lukvle10/minor_review_check.py > research-20260929/publication/primal/dtoc5-lukvle10/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../primal/dtoc5-lukvle10/logs/minor_review_check.log).

### primal/lnts

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/lnts/minor_review_check.py > research-20260929/publication/primal/lnts/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../primal/lnts/logs/minor_review_check.log).

### primal/powerflow

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/powerflow/minor_review_check.py > research-20260929/publication/primal/powerflow/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../primal/powerflow/logs/minor_review_check.log).

### primal/water-ann-kan

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/water-ann-kan/code/minor_review_check.py > research-20260929/publication/primal/water-ann-kan/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../primal/water-ann-kan/logs/minor_review_check.log).

### audit-ir

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/audit-ir/minor_review_check.py > research-20260929/publication/audit-ir/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../audit-ir/logs/minor_review_check.log).

### eg-recheck

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/eg-recheck/minor_review_check.py > research-20260929/publication/eg-recheck/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../eg-recheck/logs/minor_review_check.log).

### scip-bug

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/scip-bug/minor_review_check.py > research-20260929/publication/scip-bug/logs/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../scip-bug/logs/minor_review_check.log).

### literature/control

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/minor_review_check.py > research-20260929/publication/literature/control/checks/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../literature/control/checks/minor_review_check.log).

### literature/network

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/network/checks/minor_review_check.py > research-20260929/publication/literature/network/checks/minor_review_check.log
```

Result: exit 0; final PASS. Evidence: [log](../../literature/network/checks/minor_review_check.log).

### dtoc5 reference-point scale

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/dtoc5_reference_check.py > research-20260929/publication/literature/control/checks/dtoc5_reference_check.log
```

Result: exit 0; hash matches r2, maximum |x| = 8.057243524908399 < 100. No feasibility or optimality proof was repeated.

## Source preparation and report edits

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

## Round 2 (2026-10-03)

The preceding four-core statement describes round 1 only. Round 2 ran serially with one numerical thread per process and at most two CPU cores. No main construction, solver campaign, project-wide check or CI inspection was run. No commit, push or outside contact occurred.

From the repository root, these preparation/edit commands were run:

```sh
python3 research-20260929/publication/reviews/minor-fixes/edit_r2.py
python3 research-20260929/publication/reviews/minor-fixes/build_integration_r2.py
python3 research-20260929/publication/reviews/minor-fixes/run_checks_r2.py
python3 research-20260929/publication/reviews/minor-fixes/finish_r2.py
```

The serial runner executed these exact targeted commands; all exited 0:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/reviews/minor-fixes/check_r2.py > research-20260929/publication/reviews/minor-fixes/check_r2.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/water-ann-kan/code/minor_review_check.py > research-20260929/publication/primal/water-ann-kan/logs/minor_review_check.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/primal/lnts/minor_review_check.py > research-20260929/publication/primal/lnts/logs/review_r2_check.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/scip-bug/minor_review_check.py > research-20260929/publication/scip-bug/logs/review_r2_check.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/dtoc5_reference_check.py > research-20260929/publication/literature/control/checks/dtoc5_reference_check.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/qplib_camshape_compare.py research-20260929/publication/literature/control/sources/qplib/camshape_copies/camshape100.gms research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_2738.gms research-20260929/open-instances/minlplib_sol/camshape100.p1.sol research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_2738.sol > research-20260929/publication/literature/control/checks/qplib_camshape_compare.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/qplib_camshape_compare.py research-20260929/publication/literature/control/sources/qplib/camshape_copies/camshape200.gms research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_2480.gms research-20260929/open-instances/minlplib_sol/camshape200.p1.sol research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_2480.sol >> research-20260929/publication/literature/control/checks/qplib_camshape_compare.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/qplib_camshape_compare.py research-20260929/publication/literature/control/sources/qplib/camshape_copies/camshape400.gms research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_2703.gms research-20260929/open-instances/minlplib_sol/camshape400.p1.sol research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_2703.sol >> research-20260929/publication/literature/control/checks/qplib_camshape_compare.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/literature/control/checks/qplib_camshape_compare.py research-20260929/publication/literature/control/sources/qplib/camshape_copies/camshape800.gms research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_3177.gms research-20260929/open-instances/minlplib_sol/camshape800.p1.sol research-20260929/publication/literature/control/sources/qplib/camshape_copies/QPLIB_3177.sol >> research-20260929/publication/literature/control/checks/qplib_camshape_compare.log
```

Results: independent rational display/gap/bound/slack checks, audit-page recount, eg saved-array counts, lnts byte comparisons, current stored-box Krawczyk check, SCIP raw-log recount and exact small-model comparisons all passed. The four comparison outputs refresh `literature/control/checks/qplib_camshape_compare.log`; the QPLIB_2703 maximum is now 4.708e-10 at x1.up, not the stale lower-bound-only result. The saved dtoc5 reference-point check passed with the corrected default-rule qualification.

The independent checker was also run directly during development, with the same environment and redirection shown above. Early runs exposed mistakes in that new checker: waterno2_06 was incorrectly assumed to lie below 282.888; waterno2_09 was incorrectly expected to need a correction; Unicode minus signs had not yet been normalized. Those assertions/input errors were fixed before the final successful run. These failures did not concern a main certificate. The checker was strengthened afterward to cover remaining duals and powerflow slacks, then rerun successfully.

Read-only evidence inspection used `rg`, `cat`, `sed`, `head`, `tail`, scoped `git status`, and small Python reads of saved JSON, XML and page text. No new downloads were needed. Inline Python writes made scoped snapshots/progress records and small prose follow-ups; their final edits are retained in `report_changes_r2.patch`. All independent numerical checks are saved in `check_r2.py`; none were hidden in an inline numerical command.

### Additional small arithmetic inspections and final validation

The following read-only exact arithmetic commands were also run during evidence discovery; their comparisons are now included in the saved independent checker:

```sh
python3 - <<'PY_CHECK'
from fractions import Fraction as Q
for s in ['6.4531031529331155','5.760539610694994','5.642100574331458','576.8934122988004','41869.05148485014','41869.05148327243','352.2380254050784']:
 print(s,'decimal - float',float(Q(s)-Q(float(s))))
PY_CHECK
python3 - <<'PY_CHECK'
import json
from fractions import Fraction as Q
from pathlib import Path
v=json.loads(Path('research-20260929/open-instances-wave3/logs/powerflow0030p.sdpcert.json').read_text());b=Q(v['bound_exact']);print('0030p display - certified exact',float(Q('576.8934122988004')-b));print(v.keys())
PY_CHECK
python3 - <<'PY_CHECK'
from fractions import Fraction as Q
import json
from pathlib import Path
v=json.loads(Path('research-20260929/reviews/wave2-small-verification/logs/pricing050.json').read_text());m=v['multipliers'];muR=Q(m['e5'])*Q('-788')+Q(m['e6'])*Q('-984');UB=muR-Q(v['certificate']['sum_minF_certified']);print('display - UB saved sum',float(Q('-1813.8290784519730577')-UB),'uncertainty sum print',5e-22)
PY_CHECK
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/reviews/minor-fixes/check_r2.py > research-20260929/publication/reviews/minor-fixes/check_r2.log
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python3 research-20260929/publication/reviews/minor-fixes/validate_r2.py > research-20260929/publication/reviews/minor-fixes/validation_r2.log
```

Results: all exited 0. The decimal-versus-binary64 inspection was exploratory: the final checker uses exact rational powerflow certificates and eg decimal targets, rather than assuming every stored dual is binary64. Final validation passed all 22 response rows, ten round-2 report sections, new local links, 40 ordered integration replacements in memory, changed-script syntax and final logs. Hash checks confirmed the main summary and audit report were unchanged. No CI checks were run or inspected. Final bookkeeping updated only summary links, this command record, the scoped patch, FILES.json / FILES-r2.json and PROGRESS.json; it launched no jobs.

Scoped whitespace check also ran (exit 0):

```sh
git diff --check -- research-20260929/publication/primal/chain/report.md research-20260929/publication/primal/dtoc5-lukvle10/report.md research-20260929/publication/primal/lnts/report.md research-20260929/publication/primal/powerflow/report.md research-20260929/publication/primal/water-ann-kan/report.md research-20260929/publication/audit-ir/report.md research-20260929/publication/eg-recheck/report.md
```
