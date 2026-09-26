# Flat-chain threshold verification

Status: complete. The original 2026-09-19 delivery passed warning-free builds
of 144 topic modules and an axiom audit of 4,197 declarations. The package now
contains 145 modules, including `ThreeCircuitForms` for FC38's named
seven/five/three/one classification. Checks of that addition are recorded
separately below; the delivery logs and fingerprint manifest remain unchanged.
The pinned toolchain is `leanprover/lean4:v4.33.1`; dependency revisions are
recorded in `formal/lake-manifest.json` and included in the source fingerprints.

The following commands reproduce the checks against the current sources from
`formal/`; the module list now includes the added module:

```sh
lake build --wfail $(cat topics/15-flat-chain-threshold/verification/modules.txt)
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/Audit.lean
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewAlgorithms.lean
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewObserved.lean
python3 topics/15-flat-chain-threshold/verification/ReviewGeneratedCalls.py
```

All five commands passed at delivery, when the module list had 144 entries.
The following table records that historical run:

| Check | Result | Saved evidence |
|---|---|---|
| Targeted module build | 144 explicit topic targets; build completed successfully (8,886 jobs, including dependencies) | [build.log](verification/build.log), [modules.txt](verification/modules.txt) |
| Transitive axiom audit | 4,197 declarations in 144 extension modules; only the three allowed axioms | [axioms.log](verification/axioms.log), [Audit.lean](verification/Audit.lean) |
| Algorithm boundary examples | Nine kernel-checked examples passed | [ReviewAlgorithms.lean](verification/ReviewAlgorithms.lean), [review-algorithms.log](verification/review-algorithms.log) |
| Observed-label boundary examples | Four kernel-checked examples passed | [ReviewObserved.lean](verification/ReviewObserved.lean), [review-observed.log](verification/review-observed.log) |
| Generated-code regression | All four cache/query entry-point checks passed | [ReviewGeneratedCalls.py](verification/ReviewGeneratedCalls.py), [review-generated-calls.log](verification/review-generated-calls.log) |

Successful Lean example checks produce no output, so their saved logs are empty.
The generated-code check inspects the C output of the targeted build for the
specific repeated-label-deduplication regression. It does not prove general
compiler correctness or machine-runtime bounds.

The first command names only the topic-owned modules. It checks their required
dependencies and treats warnings as failures; it does not build the whole
project. The audit imports exactly those modules, enumerates their declarations
including private and generated declarations, and checks transitive axiom
usage. Only `propext`, `Classical.choice`, and `Quot.sound` are allowed. A
`sorryAx`, custom axiom, or native-computation axiom fails the audit.

The [source fingerprints](verification/SOURCES.sha256) identify the delivery-time proof
sources and their local import dependencies, manuscript sections, topic
documentation, review records, verification programs and logs, import registry,
and toolchain files. [Delivery metadata](verification/delivery.json) records the
counts, commands and scope, and the fingerprint manifest's own digest. From the
repository root, run:

```sh
sha256sum -c formal/topics/15-flat-chain-threshold/verification/SOURCES.sha256
```

**This manifest is a delivery-time snapshot and is not expected to match the
current tree.** It is retained unchanged so that its evidence remains tied to
the delivery. The comparison made during the 2026-09-20 follow-up found 206
matching entries and 12 mismatches. A rerun of the same command on 2026-09-25
at `d85171b8` found 199 matching entries and 19 mismatches; the last seven rows
below are the new ones, and the `Audit.lean` row gained a second reason. The
reasons come from `git log` on each file since the manifest was added in
`c75d5321`.

| File | Reason for the mismatch |
|---|---|
| `formal/Formal/NetworkSimplex/ThresholdObservedRecovery.lean` | The payload-size docstring changed; its executable definitions and proofs did not. |
| `formal/Formal.lean` | The import registry includes later topics and the new `ThreeCircuitForms` module. |
| `formal/topics/15-flat-chain-threshold/{ALGORITHMS,COVERAGE,README,REVIEW,VERIFICATION}.md` | Topic documentation was corrected after delivery. |
| `formal/topics/15-flat-chain-threshold/verification/{Audit.lean,modules.txt}` | The audit and module list now include `ThreeCircuitForms` (`748a8b28`). Commit `fa2a6f42` also split the audit's final `PASS` message across two source lines. |
| `README.md`, `formal/topics/README.md`, `formal/RECOMMENDED-TOPICS-PLAN.md` | Repository indexes were updated as later topics completed. |
| `formal/topics/15-flat-chain-threshold/verification/ReviewObserved.lean` | Commit `fa2a6f42` wrapped two long `example` statements across lines. The four examples and their `decide +kernel` proofs are unchanged. |
| `formal/README.md` | The formal index was updated as later topics completed (`367fcbc8`, `c716f120`, `17ac3204`, `6816f8b3`, `2cd1bf23`). |
| `paper-network-simplex/sections/{01-foundations,04-bounded-rank,06-series-parallel,07-fixed-state-chains}.tex` | Manuscript prose was revised in the 2026-09-24 repository audit (`aee2afbf`). |
| `results/network-simplex-flat-chain-fixed-states.md` | Commit `367fcbc8` added a paragraph relating this note's unreduced formulation to the sharper results in the current manuscript. |

`ThreeCircuitForms.lean` and the follow-up log are new files and therefore have
no entry in the delivery manifest. The old manifest is evidence for the original
snapshot, not verification of these additions. The targeted checks below provide
separate evidence for the new module.

The delivery-time documentation check also verified the 60 coverage identifiers, module
manifest and root-import agreement, declaration references, and local topic links.
`git diff --check` passed. Earlier failed finishing checks prompted corrections
to incomplete proofs, a combined-import local-instance name collision, and the
runtime dimension calculation. Those failures are not passing completion evidence;
the independent reports distinguish earlier findings from the final reruns.

The executable examples cover missing groups, violated scalar rows, actual
three-label coefficient-repair examples that pass separate McCormick checks,
invalid simplex normalization despite profile feasibility, zero-weight output
filtering, dimension-zero recovery, duplicate observation labels, and
structurally observed zero-weight labels. The audit checks their kernel proofs;
it does not certify unrelated Python implementations or historical timings.

The cost results retain their stated models. Basis scans count multiply-add
steps, with the factor-two conversion to primitive arithmetic explicit. Recovery
counts rational arithmetic and output entries; it does not count every structural
lookup or allocation of nested finite functions. The packed oracle uses indexed
word operations, with enough address bits and linear-width normal keys. Operand
and bit bounds do not refine the compiled rational backend.

Coefficient bounds concern flow and observed-product coordinates, not constants
or simplex coefficients. Main expressions evaluate under gadget balance, and
`ThresholdAmbientDescription` treats independent b-flow coordinates under the
actual balance equations. The manuscript assumes at least one gadget; the
zero-gadget algebraic extension is recorded separately. These scope boundaries
are part of the completed claim, not unresolved proof obligations.

No project-wide local verification was run. CI status and logs were not inspected.

## Follow-up: compact payload description

Source review on 2026-09-20 confirmed that `observedWitness_compact_flow_size`
bounds the normalized decomposition payload formula. It does not count the full
`ObservedRecovery`, which retains additional cache, profile, and flow data.
The algorithm description, coverage row, and theorem comment now state that
distinction. No executable definition or proof changed, so no build or test was
run for this documentation correction. Earlier execution results remain historical.

## Follow-up: named three-label circuit forms

`ThreeCircuitForms.lean` gives the geometric definitions, counts, realization,
and exclusivity of the seven subset, five partition, three overlap, and one
half-cover forms, and connects them to the real support-minimal classification.
Source review also corrected FC30's definition attribution, FC59's distinction
between formula bounds, type cardinalities, and emitted-object sizes, and the
existence-only description of `supportMinimal_four_forms`.

The following targeted commands passed on 2026-09-20 from `formal/`, with
`$HOME/.elan/bin` on `PATH` and `LEAN_NUM_THREADS=1`:

```sh
lake build --wfail Formal.NetworkSimplex.ThreeCircuitForms
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/Audit.lean
lake env leanchecker Formal.NetworkSimplex.ThreeCircuitForms
```

The build exited 0 without warnings. The audit exited 0 and covered 4,261
declarations in 145 extension modules, with only `propext`, `Classical.choice`,
and `Quot.sound`. Kernel replay exited 0. The commands and output are saved in
[verification/circuit-forms-followup.log](verification/circuit-forms-followup.log).
This is separate from the unchanged delivery log of 4,197 declarations in 144
modules. The earlier algorithm examples and generated-code checks were not
rerun for this addition. No project-wide verification or CI inspection was run.

## Audit rerun on 2026-09-25

Commit `fa2a6f42` changed `Audit.lean` and `ReviewObserved.lean` only by line
wrapping, as described in the fingerprint table above. For consistency both
programs were run once more from `formal/` at `d85171b8`, with
`$HOME/.elan/bin` on `PATH` and `LEAN_NUM_THREADS=4`:

```sh
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/Audit.lean
lake env lean -DwarningAsError=true topics/15-flat-chain-threshold/verification/ReviewObserved.lean
```

The audit exited 0 in 30.6 s and printed
`PASS: audited 4261 declarations in 145 extension modules; only propext, Classical.choice, Quot.sound are allowed.`,
matching the 2026-09-20 follow-up. `ReviewObserved.lean` exited 0 in 4.0 s with
no output, so its four examples passed. Beforehand, `lake build --no-build` on
the 145 listed modules reported all targets up to date, so both programs read
outputs built from the current sources. The build, the other review programs,
the generated-code check and kernel replay were not rerun. No project-wide
verification or CI inspection was run.
