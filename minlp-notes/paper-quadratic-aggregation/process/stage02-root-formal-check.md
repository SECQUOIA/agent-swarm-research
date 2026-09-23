# Coordinator's independent topic-27 check

The coordinator runs the existing topic-specific runner via Python `runpy`,
redirecting its `OUT` global to
`paper-quadratic-aggregation/verification/stage02-root-formal/`. The runner's
audit input and explicit module list are copied there. The original formal
verification records are preserved. Source files remain in the existing
`formal/` project, whose pinned toolchain and dependencies are used.

This checks only the 11 named quadratic-aggregation modules, their owned
declarations, and individual kernel replays. It does not invoke the full
project verification or inspect CI. The runner fingerprints sources before
and after checking. Final logs and its manifest supply the outcome; a process
start by itself is not successful verification.

The check concerns the existing Lean theorem and stated supporting lemmas.
Correspondence to the manuscript and the mathematical claims outside the
formal package still require the prescribed paper reviews.

Outcome: PASS. The explicit 11-module warning-free build, 178-declaration
transitive axiom audit, all 11 kernel replays, and source-stability checks
completed with exit code zero. See the manifest and individual logs in the
output directory. No project-wide verification or CI inspection was run.

Exact coordinator command, from the repository root:

```sh
python3 - <<'PY'
from pathlib import Path
import runpy, shutil
repo = Path.cwd()
out = repo / 'paper-quadratic-aggregation/verification/stage02-root-formal'
out.mkdir(parents=True, exist_ok=True)
source = repo / 'formal/topics/27-quadratic-aggregation/verification'
for name in ('AuditAggregation.lean', 'modules.json'):
    shutil.copy2(source / name, out / name)
ns = runpy.run_path(str(source / 'run_checks.py'))
ns['main'].__globals__['OUT'] = out
ns['main']()
PY
```
