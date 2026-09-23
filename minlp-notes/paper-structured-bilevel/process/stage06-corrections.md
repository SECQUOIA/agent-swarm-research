# Stage 6 corrections

Correction agent: `correction_agent`, distinct from the stage author and five
reviewers. Date: 2026-09-07. Authority:
`process/assessments/stage06-round01.md`. Both accepted minor issues are fixed.
No accepted issue remains unresolved; root acceptance remains pending.

## Changes and verification

| Issue | Change | Verification |
| --- | --- | --- |
| S6-1 | `code/compressed_solver.py:340` now materializes `constraints = tuple(constraints)` once before checking dimensions. All later upper-row loops reuse that tuple. The false-convexification case in `code/check_full_task.py:61–63` now explicitly requires both list and one-shot iterator inputs to return infeasibility under optimistic and pessimistic semantics. | The new regression failed against the measured source before the fix, at the iterator assertion. After the fix, all 18 existing full-task cases pass with the additional assertions under both semantics, as do the existing singular-minor, flat-continuum, singleton-aggregate, fixed-box, and fast-path checks. |
| S6-2 | The README opening now identifies accepted stages 1–5 and authored stage 6, whose corrections await root verification. Its reproduction paragraph points to the existing commands and logs. The solver and provenance paragraphs distinguish the measured rational fast paths from the later iterator normalization. | Inspected the complete README diff. It does not claim stage 6 acceptance, future availability of existing reproduction commands, or that the corrected solver was used for the archived timings. Final synthesis and the whole-manuscript review remain separately pending without conflating their stage numbers. |

## Measured and corrected source versions

Before modifying the solver, I checked that its SHA-256 matched the measured
hash in `data/stage06-results.json`, then preserved that exact file as
`verification/correction-agent/stage06/measured-compressed-solver.py`:

```text
62afc7320fec870c9e4207933be3fa68a584b1d9749103a4643d8ddd66ca5671
```

The corrected live solver's hash is:

```text
43d52aee2b43a21940cbaa3d8c3854d6b5478c46e0577d9fef7161b465cd0001
```

Removing the single tuple-materialization line from the corrected solver
reproduces the preserved measured source byte for byte. The measured rational
sign and midpoint fast paths, atlas construction, algebraic fallbacks, and
contact logic are unchanged. Recorded calls supplied reusable lists or tuples,
so the iterator defect did not drop rows in those measurements. The corrected
entry-point normalization was not timed; no raw timing was replaced or
relabeled as a measurement of this version.

`verification/correction-agent/stage06/manifest.json` maps each measured source
to its preserved path and measured hash, together with the current hash. This
includes the already preserved measured driver and test helper. The helper's
new assertions extend correctness checks; the experiment inputs and worker
timing code are unchanged. The historical author report accurately describes
its own source versions and remains immutable; this report records the later
correction.

## Checks and isolated build

The regression was first added while the solver still matched the measured
source. Invoking the false-convexification case produced the expected
`('constraint iterator', 'optimistic')` assertion failure, recorded in
`regression-before-fix.log`. After the fix, the complete helper was run in
`verification/correction-agent/stage06/workspace/paper-structured-bilevel/`:

```sh
python code/check_full_task.py
latexmk -gg -pdf -interaction=nonstopmode -halt-on-error -outdir=../../build main.tex
```

All 18 cases compare the independent original-face baseline and compressed
solver under both semantics, verify exact values and attainment, and validate
attained witnesses and response sets. The new iterator assertions execute
within both semantic cases. The helper's final boundary and unchanged-solver
comparisons also pass. Logs and the resulting 18-case JSON are retained under
the correction directory. The isolated workspace uses a link to the existing
repository code for imports; its helper writes to its own isolated author-log
path, leaving the actual author's results untouched.

The isolated paper build succeeds with 73 pages and no final warnings,
undefined citations or references, overfull or underfull boxes, or fatal
errors. No LaTeX manuscript source changed. The verified PDF is
`verification/correction-agent/stage06/build/main.pdf`; the live build
directory was not rebuilt. A timing rerun was unnecessary and was not performed.

## Integrity and evidence

Before editing, all 30 live and frozen files matched the reviewed manifest,
whose SHA-256 remains
`b9c28c41440e7ea2e660731eac9023d900279ad1ebae7bf99866f32ffb3d4bc8`.
Every frozen file still matches its hash, and the isolated sources match the
corrected live files. I inspected the complete diff: only README,
`code/compressed_solver.py`, and `code/check_full_task.py` changed among the
manifest-listed files. Section 6 and all earlier proofs remain unchanged.

The raw measurement archive, prepared inputs, tables, figures, historical
author report, author manifest, and original full-task results retain their
hashes. Root status, assessments, and snapshots were not edited.

Evidence under `verification/correction-agent/stage06/` consists of
`pre-edit-manifest.json`, `manifest.json`, `measured-compressed-solver.py`,
`regression-before-fix.log`, `full-task-checks.log`, `full-task-checks.json`,
`build-command.log`, `final-main.log`, `rendered.txt`, `source.diff`, and the
isolated sources and PDF.

Remaining accepted issues: **none**. No later stage was started, and no work
was delegated.
