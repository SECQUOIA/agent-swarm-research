# Arbitrary-grid one-switch minimax and sharp grid transfer: verification record

Status: complete. The checks below were first run locally on 2026-09-20 from
`formal/` at two recorded revisions, and all machine checks were rerun on 2026-09-25 at
`549a5786` (see [Targeted rerun, 2026-09-25](#targeted-rerun-2026-09-25)).
Each row names the revision it checked.
Project-wide verification is CI's responsibility and was **not** run locally; no
CI status or log was inspected. Nothing here asserts an unobserved CI result.

The package adds twenty-three proof modules to the canonical project, 15,481
lines at `549a5786` (`wc -l`; an earlier record gave 15,432, which matches no
recorded revision), in the new namespace `GridSwitching`.

| Module | Obligations |
|---|---|
| `Model.lean`, `Cumulative.lean` | SC01-SC04 |
| `Endpoint.lean` | SC05, SC06 |
| `Compactness.lean` | SC07-SC09 |
| `OneSwitch.lean` | SC10, SC11 |
| `LinearPrograms.lean` | SC12, SC13 |
| `Coverage.lean` | SC14, SC15 |
| `TwoLarge.lean` | SC16, SC17 |
| `Symmetrize.lean` | SC18 |
| `Elimination.lean` | SC19 |
| `FiniteOne.lean` | SC20 |
| `ThreeMode.lean` | SC21 |
| `Examples.lean` | SC22, SC23 |
| `Rounding.lean`, `UniformTransfer.lean` | SC24 |
| `Transfer.lean` | SC25, SC26 |
| `BinaryTransfer.lean` | SC27 |
| `Sharpness.lean` | SC28, SC29 |
| `Coarsening.lean`, `Refinement.lean` | SC30, SC32 |
| `Dwell.lean` | SC31 |
| `InstanceAlgorithms.lean` | SC33-SC35 |
| `SubsetDP.lean` | SC36, SC37 |

## Checks performed

| Check | Result |
|---|---|
| Targeted module builds, `lake build --wfail` | PASS at `549a5786`: all 23 recompiled from source, zero errors and zero warnings. Earlier: PASS at `fa3ed328`. |
| Coexistence: the 23 modules imported together | PASS at `549a5786`: no conflicting declarations. Earlier: PASS at `fa3ed328`; the `80f36418` axiom audit also imported all 23 together. |
| Import coverage, `python3 scripts/check_imports.py` | PASS at `549a5786`: 813 proof modules, including all 23 of this package. This static script reads the whole `Formal/` tree and builds nothing. Historical counts: 417 at delivery (`fa3ed328`) and 436 in a later recorded run. |
| Axiom audit over every `Formal.GridSwitching` declaration, including private helpers | PASS at `549a5786`: **1,921** declarations, the same count as at `80f36418`. (This row read 1,869 at delivery, `fa3ed328`; the count rose when the audit findings below were closed by adding proofs.) |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay, `LEAN_NUM_THREADS=1 lake env leanchecker` per module | PASS at `549a5786`: all 23, zero failures. Earlier: PASS at `fa3ed328`. |
| Independent review | PASS: four reviewers, no incorrect theorem found; see [REVIEW.md](REVIEW.md) |

The [2026-09-25 run log](verification/run-2026-09-25.log) records every command
and its output at `549a5786`. The earlier [run log](verification/run.log)
records the `80f36418` axiom audit and its output. The delivery log, with the
build, coexistence, import-coverage, audit and replay invocations at
`fa3ed328`, was replaced in `80f36418` and is retained in git history:

```sh
git show fa3ed328:formal/topics/17-grid-switching/verification/run.log
```

Commit `80f36418` changed the proofs in six modules: `Coarsening`, `Examples`,
`InstanceAlgorithms`, `Model`, `Rounding` and `SubsetDP`. Its axiom audit covered
them, but no record from that time shows a warning-free build or kernel replay
after the change. The 2026-09-25 rerun closes that gap: it rebuilt and replayed
all 23 modules at `549a5786`, which includes those proofs and the later
comment-only edits in `90eb77ce` and in the comment correction below.
The audit is [`verification/AuditGridSwitching.lean`](verification/AuditGridSwitching.lean),
the project audit of `Verify.lean` restricted to this namespace, so it covers
module-owned private and auxiliary declarations rather than only the public API.
Reproduce it with:

```sh
lake env lean topics/17-grid-switching/verification/AuditGridSwitching.lean
```

## What the proofs do and do not use

There is no `sorry`, no custom `axiom`, no `native_decide`, no `partial def` and
no `@[implemented_by]` in any of the twenty-three modules. The explicit finite
checks use ordinary kernel evaluation, not native compilation.

Kernel replay uses the installed Lean kernel and the pinned imported Mathlib
base. It is not an independently implemented proof assistant, and it is not a
fresh replay of all of Mathlib. Lean 4.33.1 and Mathlib v4.33.1 remain pinned
and are shared with the existing project.

## Two dependencies worth recording

- **The cumulative-class converse (SC02)** rests on
  `AbsolutelyContinuousOnInterval.integral_deriv_eq_sub`, a 2025 Mathlib
  addition. The older fundamental-theorem variants require a derivative at
  *every* point of the interval and would not suffice, since a Lipschitz
  function is differentiable only almost everywhere.
- **The transfer rounding (SC24)** does not follow the sources. They derive it
  from integral network-flow feasibility; the pinned Mathlib has no max-flow, no
  circulation theorem, and only the *definition* of total unimodularity without
  the Hoffman-Kruskal integrality consequence. The proof here uses Hall's
  marriage theorem instead. Support feasibility alone does not imply the
  prefix bounds (`exists_supported_not_prefix_bounded`), so the statement is
  genuinely global; no particular greedy algorithm is refuted.

## Scope of the guarantee

Verification applies to the definitions recorded in [COVERAGE.md](COVERAGE.md)
and to no others. It does not establish novelty, bibliographic priority,
external peer review, or physical validity, and it verifies no numerical
producer, solver or checker. The exclusions frozen in [CLAIMS.md](CLAIMS.md)
remain outside the package.

On complexity, the boundary that the reviews sharpened is this: what is verified
is correctness, termination, and **exact arithmetic-operation or size
recursions** — the three-candidate bound independent of the mode count, the
`O(N^2)` candidate set, the `2^k` states and `3^k` transitions of the dynamic
program, the exact cardinality of the block-partition enumeration, and the
`N + M - 1` bound on a common refinement. What remains excluded is only the
counted bit-cost model and the conversion of these sizes into a running time
under an execution model. No operation count is asserted as a machine-level
claim anywhere.

This package does not extend the three-mode unit-grid model of topic 1; it
builds a general one. No part of that package is reused: no module here references
`SwitchingControl`, so nothing is inherited and `CLAIMS.md`'s identification
requirement is met vacuously. Its 27,641 lines are specific to three modes and
unit cells.

## Documentation correction check, 2026-09-20

The source review recorded in [REVIEW.md](REVIEW.md) changed documentation and
one comment in `Coarsening.lean`; no theorem statement or proof changed. No
new Lean build, axiom audit, kernel replay, or CI inspection was performed.
The earlier results above are historical and were not rerun for these edits.

The targeted whitespace check passed:

```sh
git diff --check -- formal/topics/17-grid-switching/README.md formal/topics/17-grid-switching/COVERAGE.md formal/topics/17-grid-switching/REVIEW.md formal/topics/17-grid-switching/VERIFICATION.md formal/Formal/GridSwitching/Coarsening.lean
```

## Comment correction check, 2026-09-25

Two comments in `UniformTransfer.lean` said that grid uniformity is used only
once. They now say that `exists_blockMap_uniform` uses it twice: in `hcellsum`,
to normalize each occupation row to the simplex, and in `hVnode`, to convert
selected-cell counts into node values, as [COVERAGE.md](COVERAGE.md) already
records under SC24. Only comments changed; no theorem statement or proof
changed. No new Lean build, axiom audit, kernel replay, or CI inspection was
performed, and the earlier results above were not rerun for this edit.

The targeted whitespace check passed:

```sh
git diff --check -- formal/topics/17-grid-switching/README.md formal/topics/17-grid-switching/VERIFICATION.md formal/Formal/GridSwitching/UniformTransfer.lean
```

## Targeted rerun, 2026-09-25

All machine checks in the table were rerun (the independent review was not repeated) from `formal/` at `549a5786`. No `.lean` file
under `formal/` had uncommitted changes; the only uncommitted `formal/` changes
at the time were two topic-14 Markdown files. Toolchain: Lean 4.33.1 with the
pinned Mathlib v4.33.1. Every Lean process ran one at a time. The full commands
and output are in [`verification/run-2026-09-25.log`](verification/run-2026-09-25.log).

- **Builds.** The existing `Formal/GridSwitching` build outputs were first moved
  out of `.lake/build`, so each module was recompiled rather than taken from
  cache. Then, in dependency order, one call per module:
  `LEAN_NUM_THREADS=4 lake build --wfail Formal.GridSwitching.<M>`. All 23
  exited 0 with no warnings; 240 s in total.
- **Coexistence.** `lake env lean` on a file importing all 23 modules: exit 0.
- **Import coverage.** `python3 scripts/check_imports.py`: PASS, 813 proof modules.
- **Axiom audit.** `lake env lean topics/17-grid-switching/verification/AuditGridSwitching.lean`:
  `PASS: audited 1921 GridSwitching declarations`; every named declaration
  depends only on `propext`, `Classical.choice` and `Quot.sound`.
- **Kernel replay.** `LEAN_NUM_THREADS=1 lake env leanchecker Formal.GridSwitching.<M>`
  for each of the 23 modules: all exited 0 with no output, which is
  `leanchecker`'s success behavior; 112 s in total.

Project-wide verification was not run, and no CI status or log was inspected.
