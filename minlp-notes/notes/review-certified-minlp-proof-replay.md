**Independent review of the exact VIPR proof replay.**

Reviewed 2026-09-13. The reviewed implementation was `code/minlp_solver_lab/certify/vipr.py`, SHA-256 `835b3100513b51f1767fb4d23de4ac98b4affd35170808d56c850808468e2f95`. This review covered its parser, proof rules, assumption discharge, solution witnesses, final result, and row lifetimes. It also checked the solution-cutoff argument in [the soundness note](certified-minlp-soundness.md) and [the replay contract](certified-minlp-vipr-replay.md). No paper files were changed.

No unsound accepted inference was found in this review. The implementation provides a coherent exact checker for its stated restricted VIPR subset. This conclusion is a source review with adversarial regression tests, not a formal verification or an assertion that all conceivable malformed files have been tested. It does not independently establish nonlinear model identity, curvature, interval arithmetic, or correctness of every benchmark certificate.

**Rule and assumption checks.**

The linear-combination rule multiplies each source sense by the sign of its exact rational multiplier. Nonzero inequality terms must have a consistent resulting direction; equalities may join either direction. The sum must dominate the claimed row. Zero coefficients are removed before comparison, and a constant contradiction can imply any row. Assumptions from every nonzero term are retained. Zero-multiplier references still must be valid earlier row indices, but correctly contribute no mathematical assumption.

Rounding requires that each remaining nonzero term is an integer coefficient times a declared integer variable. Lower inequalities use the ceiling of the exact right-hand side; upper inequalities use its floor. Equalities are rejected for this rule. These checks prevent the continuous-variable rounding defect present in the inspected upstream source.

An assumption row records its own row index. Unsplit requires two actual assumption rows with a common integral linear form and complementary bounds `a*x <= k` and `a*x >= k+1`, where `k` is integral. Both branch conclusions must dominate the result. The discharged dependency set is exactly `(deps(c1) minus {a1}) union (deps(c2) minus {a2})`. In particular, a contradiction obtained by combining both incompatible branch assumptions cannot be reused as both branch conclusions to erase both dependencies. An unrelated common assumption also survives. The final finite dual bound or infeasibility conclusion must have no undischarged assumptions.

**Why solution cutoffs still prove an unconditional bound.**

For minimization, every stored solution is checked against the original rational master rows and variable integrality. Let `b` be the smallest verified solution value, and let `S` be the master-feasible points of objective at most `b`. Every accepted solution cutoff is valid throughout `S`. Induction over all remaining proof rules shows that every derived row holds at each point of `S` satisfying its recorded assumptions.

If the final assumption-free row proves objective at least `L`, then every point in `S` has objective at least `L`. The best checked witness itself belongs to `S`, so the same proof establishes `b >= L`. Every feasible point outside `S` has objective greater than `b`, and therefore also at least `L`. This explains why the implementation does not need a separate numerical guard `L <= b`: the checked witness and final derivation already establish that guard semantically. The argument uses a supplied witness, not existence or attainment of an optimizer.

Without a solution witness, no solution cutoff is accepted, and the invariant applies to all feasible master points. Infeasibility claims require an empty solution section, so a cutoff cannot manufacture infeasibility by excluding feasible points. Maximization reverses the cutoff and final-bound inequalities. The unsupported integer extension `best - 1` is correctly rejected; this review does not establish soundness of any future implementation of that extension.

**Parser, references, and final targets.**

Problem matching and replay share the same parser for the master section. Numeric tokens are exact integers or fractions with positive denominators. Duplicate or invalid variable, integer, and coefficient indices are rejected, including duplicate zero coefficients. Derivation references are row indices rather than labels. Objective abbreviations share a read-only coefficient dictionary; replay builds combination coefficients separately and does not mutate the objective.

The initial scan checks all references, including zero multipliers, against preceding rows and declared lifetimes. Replay releases rows only after their computed actual last use. Missing live rows cause rejection; a lifetime annotation never supplies replacement contents. Every declared derivation and all trailing input are checked. The last derivation, rather than an earlier successful prefix, must establish the requested finite dual target. A finite primal endpoint additionally requires an appropriate feasible solution witness.

The implementation deliberately rejects some semantically usable proofs, including unsupported syntax, equality rounding, nonconforming lifetime annotations, and objective cutoff extensions. Such rejection is not evidence that a claimed bound is false. The proof file must remain stable while it is parsed, replayed, matched, and optionally checked externally; protection against concurrent file replacement is outside this function's stated contract. Extremely large counts or rational tokens can exhaust resources; this is not a service hardened against denial of service.

The inspected upstream comparison source was `/home/sgusev/build-scip/vipr/code/viprchk.cpp`, checkout `30f2951d1e90e47afa821bdd1b12b82246656c42`. Its arithmetic and branch-rule implementations were used as a comparison, not as proof authority. The new kernel checks stronger prerequisites where that source omits necessary validation, notably integrality for rounding and an actual solution witness for a cutoff.

**Verification evidence.**

Added `code/minlp_solver_lab/certify/tests/test_vipr_independent_review.py` with 13 regression cases covering a valid split with an infeasible branch, the corresponding invalid continuous split, cross-branch and unrelated assumption retention, zero-multiplier dependencies, solution ordering, maximization cutoff direction and a forged maximization upper bound, infeasibility with a solution witness, and unsupported equality rounding. These supplement the kernel author's 44 cases. The combined run passed all 57 tests:

```sh
cd code/minlp_solver_lab
.venv/bin/python -m pytest certify/tests/test_vipr.py certify/tests/test_vipr_independent_review.py -q
```

No kernel changes were required by this independent review. Full artifact replay and the separate audits of the nonlinear-to-master interface remain necessary evidence for the complete certificate pipeline.

**Follow-up: SCIP's trailing global-bound annotation.**

A preliminary replay exposed an input-compatibility gap in the reviewed grammar: SCIP emits derivation lines ending `} -1 global`. The source at `scipoptsuite-10.0.3/scip/src/scip/certificate.cpp:3463` explicitly writes this suffix. The corresponding `viprcomp.cpp` function `processGlobalBoundChange` uses `global` as completion metadata for bound updates; upstream `viprchk.cpp` skips the remaining text after the lifetime field. It is not an incomplete or empty linear-combination reason.

The following unchanged original files were rejected by the initial strict grammar. Temporary copies passed complete exact proof replay after removing only each exact terminal ` global` token:

| Instance | First rejected derivation index | Number of annotations |
| --- | ---: | ---: |
| `cvxnonsep_nsig20r` | 260 | 40 |
| `cvxnonsep_nsig30r` | 374 | 60 |
| `cvxnonsep_nsig40r` | 481 | 80 |
| `cvxnonsep_psig20r` | 497 | 21 |
| `cvxnonsep_psig30r` | 734 | 31 |
| `ex1223a` | 43 | 5 |
| `fac1` | 82 | 3 |
| `fac2` | 192 | 2 |

These initial rejections mean unsupported producer metadata, not invalid proof arithmetic. The temporary-copy experiment checked the MILP proof alone; it does not establish that any of these historical certificates matches the corrected nonlinear master. No historical artifact was edited.

The compatibility correction was then independently reviewed at SHA-256 `f72deccd4e7d32710d0587a07bf9db9133a74a86a2a1eddb85611ef199f0daf9`. The shared record tokenizer removes exactly one optional terminal `global` token. Both scanning and replay still require a complete reason and valid lifetime; duplicate markers and other trailing text remain errors. After exact inference replay, a marked row is rejected if its independently computed assumption set is nonempty. The marker cannot discard assumptions or justify arithmetic. An empty assumption set has the same incumbent-conditioned interpretation described above for every other derived row.

The kernel author added five focused cases for valid metadata, a forged global assertion on a dependent row, duplicate markers, and other trailing text. The independent reviewer reran both proof test files: all 62 tests passed. The correction was approved for the subsequent frozen replay; the earlier incomplete campaign is not the authoritative result.

**Follow-up: an earlier closed derivation can establish the requested bound.**

A fresh affine maximization example produced two valid derivations: the first proved the exact normalized bound `-17/3`, while the last proved a slightly weaker rational approximation. Requiring the last row to prove the target rejected this evidence despite a complete valid proof already appearing earlier. This was another conservative compatibility restriction, not an invalid bound.

The corrected kernel was independently reviewed at SHA-256 `3e92d397ca30d9e77bf5439cabdd45e3cb0a6a304a57abcb291eab86aed567eb`. It records the first assumption-free derivation dominating the requested target as `proving_derivation`. It still checks every subsequent derivation, all counts, and the end of the file. Invalid arithmetic, cutoffs, references, or global assertions in a suffix still cause rejection. A later valid row need not strengthen the result or discharge its own unused assumptions: it cannot invalidate the implication already established by the earlier closed proof.

This change preserves the mathematical invariant and solution-witness argument above. For an infeasibility request, dominating the fixed contradiction `0 >= 1` is equivalent to deriving a contradiction; a later tautology cannot undo it. This acceptance contract supersedes the initial review's last-row requirement.

Seven additional independent regression cases cover valid weaker and unused-assumption tails; invalid arithmetic, solution-cutoff, global-marker, and reference tails; and an earlier infeasibility proof followed by a valid tautology. The reviewer reran both proof test files: all 69 tests passed. The exact motivating artifact also passed independently, reporting bound `-17/3`, two checked derivations, and proving index 5. This change was approved for the subsequent frozen replay.

**Final follow-up: classification of twelve exact proof rejections.**

The final frozen replay reported twelve failures inside exact inference replay. The reviewer independently recomputed each first rejected linear combination using standard-library `Fraction` arithmetic. This read only the proof prefix through the rejected row and used the same exact row parser; it did not rerun the complete large proofs or change source files or historical artifacts. The [machine-readable evidence](../code/minlp_solver_lab/results/cert_proof_failure_audit_20260913.json) records each instance, proof hash from the authoritative replay, derivation index, exact combined and claimed right-hand sides, rational residual, coefficient comparison, and incompatible multiplier where present.

Eleven cases are historical `crash` results: `rsyn0820m03m`, `rsyn0830m02m`, `rsyn0830m03m`, `rsyn0830m04m`, `rsyn0840m02m`, `rsyn0840m03m`, `rsyn0840m04m`, `syn20m04m`, `syn30m03m`, `syn40m03m`, and `syn40m04m`. In every case the recombined coefficients exactly match the claimed row, and all nonzero inequality terms have the required upper-bound direction. However, the exact combined right-hand side is strictly greater than the claimed upper bound. The positive residuals range approximately from `1.55e-12` to `1.93e-10`. Therefore the stated `lin` justification does not dominate the claimed row. These are invalid recorded inference steps, not unsupported cutoff rules or a syntax restriction; their small numerical size does not justify accepting them in an exact checker.

The remaining case, historically accepted `smallinvDAXr5b200-220`, fails at derivation 84794. Its proposed lower-bound combination includes row 84789 (`A84789`, an upper inequality with right-hand side 39) with the strictly positive multiplier recorded in the evidence. That term remains an upper inequality while the other nonzero inequality terms are lower inequalities. Such opposing directions cannot be combined by this `lin` rule. The independent rational sum also falls below the claimed right-hand side by approximately `0.0201374`.

No additional checker implementation defect or missing supported proof rule was found in these twelve failures. Their rejection is required by the exact proof contract. An invalid recorded inference does not establish that its claimed row or the final optimization bound is false: another valid proof may exist, and this bounded diagnostic did not adjudicate that separate question. Recovering these certificates requires corrected evidence, not relaxing the checker.
