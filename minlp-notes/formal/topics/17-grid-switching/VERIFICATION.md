# Arbitrary-grid one-switch minimax and sharp grid transfer: verification record

Status: complete. All checks below were run locally on 2026-09-20 from `formal/`
and are the checks actually performed, re-run after the independent reviews and
the fixes they prompted. Project-wide verification is CI's responsibility and
was **not** run locally; no CI status or log was inspected. Nothing here asserts
an unobserved CI result.

The package adds twenty-three proof modules to the canonical project, 15,432
lines, in the new namespace `GridSwitching`.

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
| Targeted module builds, `lake build --wfail` | PASS: all 23, zero errors and zero warnings |
| Coexistence: the 23 modules imported together | PASS: no conflicting declarations |
| Import coverage, `python3 scripts/check_imports.py` | PASS at delivery: 417 proof modules. A later recorded run reported 436 after subsequent topics were added. These are historical counts, not a count of the current tree; this documentation correction did not rerun the project-wide import check. |
| Axiom audit over every `Formal.GridSwitching` declaration, including private helpers | PASS: **1,921** declarations. (This row read 1,869 at delivery; the count rose when the audit findings below were closed by adding proofs. Re-run today it is 1,921.) |
| Allowed axioms | Only `propext`, `Classical.choice`, `Quot.sound` |
| Kernel replay, `LEAN_NUM_THREADS=1 lake env leanchecker` per module | PASS: all 23, zero failures |
| Independent review | PASS: four reviewers, no incorrect theorem found; see [REVIEW.md](REVIEW.md) |

The [run log](verification/run.log) records the invocations and their output.
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
