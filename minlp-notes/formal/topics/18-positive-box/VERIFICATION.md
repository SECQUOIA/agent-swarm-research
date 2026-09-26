# Positive-box multilinear gaps: verification record

Status: complete with the PB44 source corrections in [COVERAGE.md](COVERAGE.md).
All forty-six obligations are covered under those corrections. The package has
nineteen proof modules in `MultilinearGap`, with the radix family in
`MultilinearGap.Radix`. The targeted checks were last rerun on current sources
on 2026-09-25: warning-free build of all nineteen modules, 1,214 audited
declarations with standard axioms only, and kernel replay of all nineteen
modules. See [the 2026-09-25 section](#targeted-rerun-on-2026-09-25). No
project-wide verification or CI inspection was run for this follow-up.

| Module | Obligations |
|---|---|
| `PositiveBox.lean` | PB01-PB04 |
| `PhysicalEnvelope.lean` | PB05, PB06, PB10, PB11, PB12 |
| `SlabIntegrality.lean` | PB10 (geometric integrality) |
| `FairOrientationFolding.lean` | PB07 (equality of laws) |
| `OrientationMoments.lean` | PB05 (sorted form), PB07, PB08, PB09 |
| `CoefficientInequality.lean` | PB13-PB18 |
| `CommonAspectBound.lean` | PB19-PB22, PB25 |
| `OriginalBoxTransfer.lean` | PB23, PB24 |
| `TransferInterpretation.lean` | PB26 |
| `BalancedOrientation.lean` | PB27, PB28 |
| `BalancedMoments.lean` | PB29, and the non-inductive half of PB30 |
| `BalancedRefinement.lean` | PB30, PB31 |
| `RadixFamily.lean` | PB32 family definitions and partition nesting |
| `RadixIncidence.lean` | PB37 (upper direction) |
| `RadixAttainment.lean` | PB37 (matching attainment) |
| `RadixTermwise.lean` | PB32-PB35 |
| `RadixHullGap.lean` | PB36, PB38-PB41, PB42 (radix map), PB43 |
| `BilinearGraph.lean` | PB42 (bilinear map), PB44 |
| `PositiveBoxHeadline.lean` | PB45, PB46 |

## Targeted rerun on 2026-09-25

The previous targeted checks ran at `90eb77ce`. Commit `748a8b28` then added
the odd-dimensional PB44 results to `BilinearGraph.lean`, with a new import of
`PhysicalEnvelope`: `meanSum_halfPoint`, `countFloor_halfPoint_odd`,
`countFrac_halfPoint_odd`, the private `choose_two_convex`,
`bilinearGraph_minimum_odd`, `bilinearGraph_hullGap_odd`,
`bilinearGraph_termwiseGap_odd`, `bilinearGraph_cube_ratio_odd` and
`bilinearGraph_cube_ratio_odd_ne`. Commits `748a8b28` and `fa2a6f42` also
edited module docstrings in `BalancedMoments.lean`, `BalancedRefinement.lean`
and `CoefficientInequality.lean`; no definitions or proofs changed there.
The audit program now also prints axioms for the five public
`bilinearGraph_*_odd*` theorems by name.

The following checks ran on 2026-09-25 from `formal/` at `d85171b8`, with that
audit edit in the working tree and `$HOME/.elan/bin` on `PATH`. The build and
audit used `LEAN_NUM_THREADS=4`; each replay used `LEAN_NUM_THREADS=1` and ran
alone.

| Check | Result | Wall time |
|---|---|---|
| `lake build --wfail` with the nineteen explicit topic targets | Exit 0, no warnings, 8,743 jobs. Lake rebuilt only `PositiveBoxHeadline`; the other eighteen targets were already up to date with the current sources. | 26.9 s |
| `lake env lean topics/18-positive-box/verification/AuditPositiveBox.lean` | Exit 0. `PASS: audited 1214 topic-18 declarations across 19 modules.` All 125 named prints report only `propext`, `Classical.choice`, and `Quot.sound`. | 9.0 s |
| `lake env leanchecker` for each of the nineteen modules, one at a time | Exit 0 for every module, no output | 4.7-5.6 s each |

The count rose from 1,205 to 1,214 because of the nine declarations added by
`748a8b28`; the sweep covers all of them, including the private helper. The
full commands, output and wall times are in
[verification/run-2026-09-25.log](verification/run-2026-09-25.log).

The odd-dimensional theorems add no obligation; the count remains forty-six.
They are extra results that support the PB44 correction: frozen PB44 states the
ratio `2(n-1)/n`, which holds only in even dimension. The PB44 row of
[COVERAGE.md](COVERAGE.md) already lists these theorems and records the
correction. [CLAIMS.md](CLAIMS.md) is frozen and was not changed.

## Historical checks

The original sixteen-module package recorded warning-free targeted builds,
coexistence, a 104-name axiom audit, zero `sorry` occurrences, and three
independent reviews. Its historical import check reported 433 proof modules.
After PB07, PB10, and PB37 were closed, the nineteen-module axiom sweep recorded
1,200 declarations with only `propext`, `Classical.choice`, and `Quot.sound`,
and all nineteen modules passed individual kernel replay. The prior audit output
is retained in [verification/run.log](verification/run.log). These are historical
results; they are not claims that every earlier check was repeated now.

## Historical PB32 follow-up checks

The PB32 proof relates actual block indices across levels and proves unique
coarse-block containment. The shared index formula was moved from
`RadixAttainment.lean` into `RadixFamily.lean`. The following checks passed on 2026-09-20 from `formal/`, with
`$HOME/.elan/bin` on `PATH` and `LEAN_NUM_THREADS=1`:

- `lake build --wfail` with the nineteen explicit `Formal.MultilinearGap.*`
  targets imported by `AuditPositiveBox.lean`: exit 0, no warnings.
- `lake env lean topics/18-positive-box/verification/AuditPositiveBox.lean`:
  exit 0, 1,205 owned declarations, standard axioms only.
- `lake env leanchecker Formal.MultilinearGap.RadixFamily`: exit 0.
- `lake env leanchecker Formal.MultilinearGap.RadixAttainment`: exit 0.

The full target list, commands, and output are in
[verification/nesting-followup.log](verification/nesting-followup.log). These
checks and the 1,205-declaration count precede the new odd-dimensional theorems
in `BilinearGraph.lean`; they are not verification results for those additions.

The audit [verification/AuditPositiveBox.lean](verification/AuditPositiveBox.lean)
imports all nineteen topic modules, prints axioms for selected named declarations,
and sweeps every declaration owned by those modules, including private helpers.
Named prints establish that those declarations exist; matching their types to
obligations remains a source-review task. The sweep permits only `propext`,
`Classical.choice`, and `Quot.sound`.

Kernel replay checks the compiled proof terms using the installed Lean kernel
and pinned imports. It is not a fresh replay of all of Mathlib or an independently
implemented proof assistant. `--wfail` makes any build warning an error.

## What the proofs do and do not use

The package uses no `sorry`, custom `axiom`, `native_decide`, `partial def`, or
`@[implemented_by]`. Its explicit finite checks use ordinary kernel evaluation.
Lean 4.33.1 and Mathlib v4.33.1 remain pinned; no dependency was added.

The PB07 folding identity was initially checked by hand and numerically; it is
now an equality of laws in Lean. The PB44 unequal-width counterexamples remain
external source-review evidence: exact linear programs gave `13/9` for widths
`(1,1,2,2)` and `25/16` for `(1,1,1,1,1,3)`. No Lean theorem depends on those
computations. The common-box qualification and the distinct formulas for even
dimensions and odd dimensions `n ≥ 3` are explicit in the formal statements and
coverage map. At `n = 1` both bilinear gaps vanish.

## Scope of the guarantee

Verification applies to the definitions recorded in [COVERAGE.md](COVERAGE.md)
and to no others. It does not establish novelty, bibliographic priority,
external peer review or physical validity, and it verifies no numerical
producer, solver or checker. The exclusions frozen in [CLAIMS.md](CLAIMS.md)
remain outside the package and are each mapped, with a reason, in
[COVERAGE.md](COVERAGE.md).

On complexity, as in topics 3, 16 and 17: what is verified is correctness and
exact size recursions — the radix family's term count and degrees
(`Radix.support_card`, `Radix.support_injective`), the block recursion
(`Radix.blockCount_mul_blockSize`), the `binom(n,2)` term count of the bilinear
graph (`bilinearSupports_card`). What remains excluded is the counted bit-cost
model and the conversion of these sizes into a running time under an execution
model. No operation count is asserted as a machine-level claim anywhere.

No exact value of `C_box(rho)` is claimed at any fixed `rho`. The package proves
`max{2, rho} ≤ C_box(rho) ≤ rho + 2` and the asymptotic
`0 ≤ C_box(rho) - rho ≤ 2`, and nothing more.

Nor is `β_N` claimed minimal. PB27 defines it and PB31 asserts the bound
`rho + β_N`; whether `F_{S,j} ≥ 0` still holds ambiently for any smaller
constant is unverified in either direction, and the grid search at `β_N - 1/100`
that found no violation is not evidence of sharpness.

## Closure of the four previously recorded gaps

The earlier reviews recorded the following gaps. All four are now closed.

| Obligation | Previous state | Now |
|---|---|---|
| PB07 | Discharged by reusing the folded `CubicGap.orientationLaw`; the equivalence to the construction the obligation names was unformalized | `fairOrientationLaw_eq_orientationLaw`: an **equality of laws**, no cube hypothesis |
| PB10 | Route substitution; the named slab-integrality statement was absent from the tree | `convexHull_slabVertices_eq`: the slab is the convex hull of its binary vertices, with `extremePoints_slab_subset` the one-sided corollary that every extreme point is binary, plus `mem_slab_self`. An earlier version of this row said "integrality in both forms"; the converse of the extreme-point inclusion is not proved |
| PB32 | Blocks defined separately at each level, without a nesting theorem | `block_subset_unique`: each fine block lies in exactly one coarse block |
| PB37 | Upper direction only; attainment open | `isGreatest_incidenceValues_of_le_radix`: the equality under `2 <= L <= b`. An earlier version of this row said "at the obligation's `b >= L`", omitting the `2 <= L` the declaration also carries, so `L` of zero or one is not covered within that regime |

Historical exploratory checks included: 960 random LPs found no
fractional vertex of the slab; the folding identity was checked by hand in both
regimes and numerically; and selected attainment instances were checked by exact LP.

That last check **refuted a supplementary claim** made earlier in the package.
It had been reported that the incidence bound is tight "exactly in the `b >= L`
regime". Exact LP shows otherwise: `(L, b) = (3, 2)` and `(4, 2)` are tight with
`b < L`, consistent with sufficiency under `b >= 2` and `2 <= L <= b + 2`. The source's `b >= L` is
therefore **sufficient but not necessary**. The formalization proves attainment
under `b >= 2` and `2 <= L <= b + 2`, with `2 <= L <= b` as the corollary matching PB37 as written. The
necessity direction is not formalized, though the LP gap at `(5, 2)`
(`2.75 < 3.00`) shows the equality is genuinely false there, not merely unproved.
