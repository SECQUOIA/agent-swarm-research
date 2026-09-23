# Stage 2 corrections

Author: `/root/stage02_corrections`. Date: 19 September 2026.

Read the lead disposition and all five independent round-1 review reports. Implemented every accepted finding in the three affected manuscript sections. The oracle diagnostic section did not require correction. No agent was spawned. All writes were confined to `paper-lbesh`; frozen solver sources and experimental records were unchanged.

## Item-by-item resolution

1. **Finite row sets and common compact containment — resolved.** The model explicitly declares the global nonlinear row index set `H` and every term row index set `J_ik` finite. Proposition `prop:value` now requires the lifted candidate sequence to be contained in one common compact domain. The proof's common compactness premise is therefore explicit.
2. **Actual finiteness guards — resolved.** The common routine now specifies its actual radial-anchor condition: all row variables must be present and the row value must compare below `-1e-9`. It no longer calls this a separately certified finite anchor. The error description names nonfinite candidate row values and fallback coefficients. The following explanation states that anchor values, midpoint values, and the scalar radial violation lack separate finiteness guards; returned nonfinite values take ordinary comparison paths, while thrown evaluation exceptions propagate. This wording was checked against `_esh_cuts` in the frozen source.
3. **Exact root versus approximate endpoint — resolved.** The row-boundary statement now concerns the exact boundary target. A separate sentence describes the actual exterior bracket endpoint used for linearization. The distinction between an individual row boundary and feasibility of the full disjunct is preserved.
4. **Exhaustive old-cut callback accounting — resolved.** Contract 1 of Theorem `thm:single-tree` now explicitly requires old-cut-infeasible callbacks to re-enforce an existing cut without adding fresh cuts. Each old-cut resolution episode must finish in finite time. Fresh nonlinear rejection iterations occur only at old-cut-feasible points. The existing finite optional-refinement contract and the express limitation that the frozen callback implementation is not proved to satisfy these contracts remain.
5. **Normalized-point domain risk — resolved.** A new paragraph explains how scaled-bound errors may be amplified by division by a small positive weight. It states that the frozen routine neither projects onto the original box nor separately verifies normalized domain membership, and that finite row values and derivatives outside the assumed convexity domain do not establish support validity. Exact results require in-domain evaluation points. The text explicitly treats this as a potential numerical risk, not an observed experimental failure. `_separate_point` was inspected to confirm the normalization behavior.
6. **Positive division constants — resolved.** Example `ex:intersection` now quantifies `K>0` before the threshold `1/K^2`. Proposition `prop:arithmetic` explicitly requires the chosen coefficient-norm bound `K-tilde>0` before dividing by it. A positive upper bound is permissible even for a zero normal, so no unnecessary separate constant-cut case was added.

These corrections clarify assumptions and match numerical descriptions to the source. They do not alter the substantive mathematical conclusions, create a new priority claim, or establish any invalid recorded run. No new experiment or source change was warranted.

## Targeted commands and results

From the repository root:

```sh
python paper-lbesh/evidence/check_stage02.py > paper-lbesh/evidence/stage02-corrections-checks.json
```

Passed. The checker reports the same two source cutoff paths, disk boundary and opposing witnesses, scalar counts 3/5/10/91 at parameters 2/4/10/100, and intersection error/residual ratios 10/100/1000. This is algebraic/example corroboration, not a replacement for the general proofs. The checker's existing repository-source dependency is unchanged, as standalone packaging is a later stage.

From `paper-lbesh`:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex > process/stage02-corrections-build.log 2>&1
```

Passed. The corrected interim manuscript has 19 pages.

From the repository root:

```sh
rg -n 'Warning|Overfull|Underfull|undefined|Output written' paper-lbesh/main.log
pdfinfo paper-lbesh/main.pdf
pdftotext -layout paper-lbesh/main.pdf paper-lbesh/process/stage02-corrections-rendered.txt
cat paper-lbesh/evidence/stage02-corrections-checks.json
git diff --check -- paper-lbesh
rg -n -A 18 -B 6 'common compact|re-enforced|Hull normalization|Anchor values|exact boundary target|finite. Here|K > 0' paper-lbesh/process/stage02-corrections-rendered.txt
```

The log query returned only the successful PDF output line: no warnings, undefined references/citations, or overfull/underfull boxes. `pdfinfo` confirmed 19 pages. The extracted corrected passages, equations, and references were inspected for reading order and layout; no issue was found. Git whitespace checking was clean. Because manuscript files may still be untracked, the additional inline check below independently checked the four Stage 2 sections and recorded their hashes:

```sh
python - <<'PY'
from pathlib import Path
import hashlib, json, re
root=Path('paper-lbesh')
paths=[root/'sections'/name for name in ('model-and-cuts.tex','separation-theory.tex','algorithm-and-implementation.tex','oracle-diagnostics.tex')]
for p in paths:
    assert all(line==line.rstrip() for line in p.read_text().splitlines()), p
log=(root/'main.log').read_text()
assert not re.search(r'Warning|Overfull|Underfull|undefined',log)
text=(root/'process/stage02-corrections-rendered.txt').read_text()
assert '??' not in text
(root/'process/stage02-corrections-source-sha256.json').write_text(json.dumps({str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},indent=2)+'\n')
print('PASS: four section whitespace checks, clean LaTeX log, and no unresolved rendered references; section hashes recorded.')
PY
```

Passed. No project-wide verification, optimizer benchmark, CI status inspection, or CI log inspection occurred. All accepted Stage 2 minor findings are resolved; no unresolved issue was introduced by these corrections.
