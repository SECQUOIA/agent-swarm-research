# Stage 6 corrections after round 1

Status: the five round-2 reviews found no major issue. Their one accepted minor
regression is now corrected and checked, as documented below. Root inspection
and Stage 6 acceptance remain pending; this record does not start Stage 7.

## Preservation before correction

Before editing measured sources or data, the correction agent copied all 82
files in the round-1 validation manifest plus the manifest itself into
[`round1-archive/`](../verification/stage06-corrections/round1-archive/).
Every file's original hash was checked before copying. Its `manifest.json`
records all 83 hashes. This includes the original optimization source, raw
measurements, generated tables, PDF, author record, tests, and validation logs.
The earlier pre-upgrade research snapshot remains unchanged as well.

## Accepted findings and corrections

| Finding | Correction |
|---|---|
| R5-S06-01, major | `strong_baselines.optimize_ef` now has a direct fixed-weight branch. It creates only positive-weight state-flow blocks, block balance equations, and native scaled variable bounds. It substitutes original x/z costs and rows, moves fixed y terms in additional rows to the RHS, restores the full original y objective constant, and reconstructs every original x/y/z coordinate, including zero observed states. Global merging occurs before zero-state removal. The existing free-weight representation remains available. |
| S06R01-R1-F01 / R2-S6-01 / S06-R1-R3-01 / R4-S06-01 | The printed benchmark command now has one continuation backslash. Its text was extracted from the final PDF and passed to Bash with a harmless argument-printing replacement for Python; the two intended argument lists were verified. |
| R2-S6-02 | The manuscript's implemented linear-in-length statement now explicitly excludes the constructor's observation sorting, whose comparison bound is `O(|O| log |O|)`. The accepted mathematical grouped-input bound is unchanged. |
| S06R01-R1-F02 | The manuscript now separates the 16-circuit three-label separation method from inverse-basis recovery, which starts at three observed labels. The corresponding author-record sentence was corrected; its header now identifies it as the historical round-1 record and directs readers here. Its old measurements were not silently replaced. |
| S06-R1-R3-02 / R5-S06-02 | The table generator now checks complete unique ordered flat-case keys, membership label counts, optimization names/order, required methods in warmups/summaries/every run, method rotations, expected statuses, and complete timing fields before recomputing all summaries. Thirteen isolated mutations test duplicate/missing cases, wrong labels/order, omitted methods, wrong rotation, and a corrupt timing summary. All are rejected before any table is written. |

The optimization builder retains one public entry point and uses a direct local
branch; no additional modeling abstraction or unrelated optimization was added.
Native variable bounds are excluded from the displayed row counts consistently
with the existing table convention.

## Repeated measurements and revised interpretation

All methods in the same three optimization cases received a fresh audited
warmup and five timed runs with the original method-order rotations. The rerun
reads the original objective vectors, fixed weights, and coupled rows directly
from the archive. It checks all input identities and reproduces every original
optimum within `1e-7`. It does not use reviewer timings or expand the grid.

| Case | Full | Global merge | Initial compression | Observed elimination |
|---|---:|---:|---:|---:|
| Sparse original: median total ms | 19.05 | 4.25 | 4.82 | 6.45 |
| Sparse original: variables | 5,547 | 516 | 255 | 222 |
| Aggregate budget: median total ms | 32.80 | 4.33 | 5.84 | 6.11 |
| All labels observed: median total ms | 30.36 | 30.38 | 10.16 | 18.39 |
| All labels observed: variables | 7,215 | 7,215 | 495 | 367 |

The revised discussion identifies global merging's lower median on the sparse
and budgeted examples. The sparse-case timing ranges overlap. The all-labels-
observed control still shows a substantial local-compression benefit. Repeated
cutting remains slower, and further observed elimination remains smaller but
slower than initial compression in these runs. No universal timing order,
industrial gain, persistent-solver advantage, or exact numerical optimality is
claimed.

All 16 flat cases, three many-label membership cases, and cold-library records
are unchanged, with equality checked against the archived JSON. Their algorithms
were not changed by this correction. The revised JSON records its mixed
measurement provenance explicitly. All five tables were regenerated from it;
membership/flat table contents change only in the data-hash header.

Run the exact optimization-only update from the repository root:

```sh
PYTHONPATH=code python paper-network-simplex/verification/stage06-corrections/rerun_optimization.py
python paper-network-simplex/verification/stage06-tables.py
```

The default full-grid runner remains available and its all-labels-observed
variable-count assertion now matches the fixed-weight model.

## Verification and evidence

The combined suite passed **22 tests**. The new test independently enumerates
four path/loop vertices and all simplex vertices: 48 fixed-weight original-hull
vertex LPs agree with 96 full/global joint LP results, including exact zero
weights, a zero residual weight, a single unused positive state, dense coupled
x/y/z rows, and nonzero costs on every original y coordinate. It verifies the
objective constant, full original-point reconstruction, native state bounds,
state balances, and independent legacy hull membership. An infeasible y-only
row and injected solver failures are also checked. Existing free-weight and
varied-multigraph tests pass, and the independent root's 60 free-weight dense
coupled-row comparisons were rerun successfully.

The complete table generator passed; all **13 private mutations** were rejected.
The official optimization rerun also performs its existing exact reconstructed
decomposition and budget checks and numerical global-cut support audits outside
the timings. Floating-point optimum agreement remains numerical evidence.

A clean build produced a **45-page PDF** with no final warnings, unresolved
references/citations, or overfull/underfull boxes. Rendered pages 40, 41, and 43
were inspected, including the revised tables, interpretation, and command.
All accepted mathematical sections 01–07 remain byte-identical to the frozen
round-1 snapshot. The unrelated manuscript folders were not edited.

Commands used the existing `/workspace/local-home/miniconda3/envs/minlp-notes/bin/python`
interpreter; their complete logs, the source diff, source/data/build hashes,
shell argument check, mutation records, and current validation manifest are
under [`verification/stage06-corrections/`](../verification/stage06-corrections/).
One attempted clean-build redirection used the repository directory rather
than the manuscript directory and failed before `latexmk` ran; it was corrected
and the clean build was rerun successfully. No code or numerical failure was
hidden by that command-path correction.

## Round 2: zero-arc fixed-weight regression

Reviewers 2 and 3 independently identified the same minor issue
(`R2-S6R2-01` / `S06-R2-R3-01`): with no arcs, the fixed-weight formulation
has no flow columns, and SciPy rejects an empty objective. The root accepted
this issue after reading all five reports; no major issue remained.

The separate correction agent preserved the reviewed baseline source, tests,
correction record, and validation records with hashes under
`verification/stage06-corrections/round2/reviewed-source/`. All 100 current
round-2 dependency hashes were verified before this local edit.

`optimize_ef` now checks the zero-column constant model directly. It tests the
scaled balance right-hand sides and substituted constant inequalities at
numerical tolerance `1e-9`, consistent with the existing membership precheck.
Nonfinite constant RHS values raise `ValueError`. A feasible result has empty
internal flow coordinates, the complete original fixed y vector, and the
original objective constant; an infeasible result has status 2 and no purported
original solution. Metadata records zero variables/nonzeros and identifies the
direct check. No call to `linprog` occurs on this branch. Ordinary nonempty-flow
LP execution and solver-failure handling are unchanged.

The combined suite now passes **23 tests**. The focused new test checks feasible
constant problems, inconsistent balances, and infeasible y-only rows in both
merge modes, for `m=0` and `m=2`. It verifies original points, objective values,
empty internal solutions, metadata, timing fields, and absence of solver calls.
It also confirms the stated tolerance behavior and rejects nonfinite constants.
The prior fixed/free-weight, coupled-row, and injected-solver-failure tests pass.

No measured case has zero arcs. No benchmark was rerun, no measurement changed,
and no manuscript source or generated table changed. The existing PDF and its
hash are unchanged, so another LaTeX build is unnecessary. The round-2 source
diff, test log, preserved source identities, and validation record are under
`verification/stage06-corrections/round2/`; the current Stage 6 manifest has been
refreshed. As adjudicated by the root, this minor repair alone does not require
a third five-reviewer round.
