# Algorithms, effort, and evidence review — round 1

Review date: 2026-10-05 America/New_York (2026-10-06 UTC).
Snapshot hashes recorded at 2026-10-06T01:22:10 UTC:

- `sections/algorithms.tex`: `a142568512f3ddb0fab359416eca4a32e4cb63ff83033a6dd93f1fad30f02da5`
- `sections/effort.tex`: `25175e8b04ddf1f2741de1db849bc7a06d496d7155f67bb6db28a68295812081`
- `sections/experiments.tex`: `0971c59a886f6f0a6a3fbd762714724495c4f26a6a272f95ea3dab6ab09cf97f`

Read BRIEF, INTEGRATION-NOTES, the completed evidence audit, the three manuscript
sections, original September/October reports and frozen numerical/reference
sources, and saved JSON/CSV. Experiments was absent at first and immediately
after a bounded 30-second wait, then appeared before the review finished and
was reviewed in full. No manuscript file was edited.

## Overall assessment

The exact-closure theorem and proof match the declared rational implementation.
All six main reference-fixture rows match saved driver output, including the
fourth-round reconstruction failure after three committed Newton iterates.
The effort section correctly separates an enhanced-execution ledger from an
independent-baseline comparison, states serial admission/reservation, and treats
its interleaving and rescue results as ideal work guarantees. No material proof
error was found in those results.

The main October outcome table and most newly derived callback summaries agree
with the raw records. The sections clearly distinguish the numerical policy
from protected-box/matrix-tail theory and avoid statistical timing claims.
Several factual and interpretive corrections below are needed before integration.

## Corrections required

1. **Original unbounded public models: four, not two.**
   `experiments.tex`, cohort paragraph, says two public models have unbounded
   variables in their original formulations. The frozen JSON bounds contain
   infinity in `powerflow0009r`, `qp3`, `bayes2_50` (coordinate 0), and
   `pointpack08` (coordinate 16). Change the count to four, or explicitly say
   that two models have unbounded variables *occurring in quadratic terms* if
   that narrower count is what is intended. Preserve the separate observation
   that only `qp3` stays unsupported at every admitted callback.

2. **The September adaptive contraction statistic uses the moving subset.**
   `experiments.tex`, precursor paragraph, describes a ratio of total normalized
   widths. In `relax.py`, `rho` is the ratio of summed FBBT-normalized widths
   after/before the round **over variables whose width shrank by at least 0.1%**;
   it is one if that subset is empty. It is not the full-box normalized-width
   ratio and is not the paper's max-width `w(B)`. Define this distinction and
   include the adaptive 120-second cap (and no-changed-bound stop) if this
   paragraph is intended to give the actual stopping rules.

3. **The prospective overhead percentages are cohort aggregates.**
   `experiments.tex`, interpretation, says the direct propagator cost was at
   most about 7% of run time. The 6.2%/7.4% values divide the summed sidecar times
   by summed process times over all 40 runs. They are not per-run upper bounds:
   the largest saved per-run shares are approximately 40.58% fixed and 40.45%
   adaptive. Also, the sidecar timer excludes the admission-test cost, which
   `effort.tex` correctly calls an unbounded separate term J. Replace the claim
   with “recorded sidecar time was 6.2% and 7.4% of total cohort process time.”
   Any statement about direct savings must retain that aggregate scope and
   exclude the separately unmeasured admission overhead.

4. **The final “no changed search” assertion contradicts the results.**
   `experiments.tex`, interpretation, says the 308 accepted reductions did not
   produce a changed search within ten seconds. Earlier paragraphs report a
   better incumbent on `bayes2_50` and seven-node versus root-only completion
   on the small bilinear cycles. Change the conclusion to “did not produce
   additional solves or a demonstrated overall speedup.” The archive establishes
   associations between policies and search outcomes; it does not isolate
   causality of particular root reductions without an ablation.

5. **Distinguish recorded node-zero callbacks from proved probing provenance.**
   `experiments.tex`, work decomposition, calls all nonroot `node=0` events
   temporary probing nodes and asserts their origin. The archived records
   retain node number and depth, but no probing-mode flag. Their numeric split
   reproduces exactly; the probing interpretation was not independently
   established from the retained records/source. Use “nonroot callbacks with
   node number zero (consistent with temporary probing nodes)” and identify
   this as an interpretation, or provide a directly supporting SCIP source/API
   fact. Do not silently promote a classification inference into an observation.
   The at-most-three-callback behavior for a shared node-zero key is directly
   supported by `TriggerState` and can remain.

6. **Correct two fixed-arm rounded values and the literal maximum bound.**
   The solved-run fixed process total is `39.52471000405785` seconds, which
   rounds to **39.52**, not 39.53. Fixed sidecar time on those solved runs is
   `5.2345126020372845`, which rounds to **5.23**, not 5.24.
   The largest adaptive sidecar total is `1.0050050349236699` seconds. Thus
   “no run more than 1.005 seconds” is a literal underbound. Say “the largest
   total rounded to 1.005 seconds,” give 1.00501, or use the true rounded-up
   bound 1.006 seconds.

7. **Match the actual directional-LP time-limit floor.**
   `algorithms.tex`, directions/limits paragraph, gives
   `min(0.25 s, remaining sidecar time)`. Frozen `Relaxation.bound` requests
   `max(0.001 s, min(0.25 s, remaining allowance and global deadline))`.
   State the one-millisecond floor, which is another reason that the callback
   deadline is not an interruptible hard bound. The effort section's no-fixed-
   delta caveat is correct.

8. **Define the pilot gain before integer rounding.**
   `algorithms.tex`, pilot paragraph, describes accepted reductions divided by
   initial widths. The saved source accumulates the improvement of each
   *accepted outward-margin proposal* relative to the current SCIP bound,
   divided by the callback-start width. This is measured **before integer
   rounding**; actual integer-domain reduction can be larger. Clarify this
   definition rather than suggesting that the pilot sums actual domain changes.

9. **Avoid unsupported necessity/cost claims for protected-box discovery.**
   `algorithms.tex`, final paragraph, says finding a protected box costs up to
   2n LPs and exceeds callback limits. A support-based discovery pass can
   require 2n support proposals plus an optional objective proposal, but a
   supplied finite witness pool can be checked without any LP. Also, 2n does
   not exceed every possible root limit; n=5 gives 10 below the root limit 12.
   Say that the measured policy does not attempt such discovery/checks and
   that a full support-based pass *can exceed* its allowance. Its row history
   and node scope need additional protection checks which are not implemented.
   Change “the tangent pool breaks lifted order” to “the history-dependent
   tangent construction can break lifted order”; the earlier paragraph already
   uses the correct conditional language. SCIP cuts are not imported into the
   sidecar, so do not suggest that they directly change its rows.

10. **Unresolved precursor appendix reference in this snapshot.**
    The reference to `sec:precursor-details` has no corresponding label/file
    in the current manuscript sources. Complete the appendix or remove the
    reference. Ensure any precursor solver table uses SCIP control/r5 counts
    573/563, and identifies the historical time/node summaries as uncorrected
    with respect to wrong-success classification.

## Smaller clarifications that improve interpretation

- The claimed 17 ms “callback cost outside LP solves” divides all non-LP
  sidecar time by the number of admitted callbacks. That numerator includes
  timed trigger visits that admitted no callback (2.0693375277/3.6232640795 s).
  It is an allocation per admitted callback, not the observed average duration
  of one recorded callback. Name it “non-LP sidecar time per admitted callback,
  including rejected trigger visits.” The approximately 6 ms per LP and
  2.43-second LP-time saving are supported.
- “LP solve and validation” in the work table should say “LP solve and dual-bound
  validation”: `lp_time` includes `linprog` and `dual_box_bound`, while proposal
  margins, SCIP application, and witness checks remain outside that timer.
- All-future theory is correctly excluded from interpretation. Retain this
  clean separation without saying the certificate mechanisms are inherently
  inapplicable to every future implementation of the sidecar.
- The one-round-late example should explicitly choose the constant objective
  and compatible cutoff, such as objective zero and cutoff zero. Its mathematical
  example is otherwise correct.
- The data-availability paragraph can now name the complete precursor results,
  including all boxes/vectors and retained metadata/cache inputs. State the
  weaker September input/source lineage succinctly if distinguishing frozen
  sources is important to the paper; the companion already documents it.
- Local POSIX `subprocess.Popen._wait(timeout)` does use a polling interval
  capped at 0.05 s, consistent with the recorded time clusters. This current
  runtime-source observation is not itself a frozen campaign artifact. Treat
  the explanation as an implementation observation, not a calibrated 50 ms
  timing-error bound or proof that actual overhead is a constant.

## Numerical checks that passed

Direct reads and sums of saved records, without importing an archived analyzer:

- All nine October table rows agree with `summary.json` to their stated
  precision: solved counts, mean PAR-2, uncapped shifted means, and gap scores.
- All twenty cohort rows agree with the frozen manifest; 41 eligible public
  names, three public models containing binaries, selected historical times,
  12 public/eight synthetic models, seeds, dimensions, and software/resource
  metadata agree. The only cohort-count mismatch found is the unbounded count
  described above.
- The complete callback table reproduces when the classes are defined as root,
  nonroot node-zero, other nonroot, and unsupported: fixed counts 100/90/166/48;
  adaptive 98/90/505/48, with all displayed LP/accepted/time totals matching.
  The residual timer totals 2.0693375277/3.6232640795 seconds reproduce.
- LP/dual-validation times 12.8179189367/10.3928326039 seconds, proposals
  200/470, maximum totals, over-budget counts 7/11, no-cutoff callbacks 124/120,
  64-LP counts 27/5, and adaptive callback-cap count 20 excluding qp3 agree.
- Solved native/adaptive process totals 34.2051009040/39.8771319880 seconds
  round to the displayed 34.21/39.88. Adaptive solved sidecar time
  5.7164011429 rounds to 5.72. The fixed rounding issues are listed above.
- Excluding bayes2_50 yields public mean gap scores
  0.2735378939/0.2822599888/0.2886894266 for native/fixed/adaptive, matching
  0.274/0.282/0.289. Bayes incumbents and near-zero duals match. Eleven of each
  arm's twelve gap losses have weaker duals; qp3 seed 1 has a changed fixed
  dual bound even though it is unsupported.
- Both small bilinear-cycle seeds have seven native nodes and one node in each
  added arm. Both adaptive process times are about 0.1 s below native. Fixed
  seed zero, however, has almost no process-time reduction; avoid suggesting
  that every root-only completion produces the same observed time reduction.
- The six displayed closure fixtures, optional objective count, all statuses,
  returned rational boxes, five invalid LP certificate cases, and cancellation
  example agree with stored reference sources/results. No fixture was executed.
- September unaffected diagnostic values agree with the original records and
  review: 339/85 cohort, 678 pairs, pipeline solve ranges, root-gap closures,
  4,573 boxes with a reference, and 109/25 integer-only counts. Historical
  ratio values reproduce their archived summaries, but remain the old-rule
  metrics, as already explained in `audit-evidence.md`.

## Verification actually performed

Targeted read-only `cat`, `sed`, `rg`, and `nl` commands inspected the three
sections, relevant source functions, saved reports and outputs. Standard-library
Python heredocs read JSON/CSV, counted or summed their stored fields, computed
snapshot hashes, and inspected the local standard-library subprocess wait
implementation. This was transcription and interpretation checking of existing
results; no archived analyzer, LP solver, numerical experiment, reference fixture,
project-wide check, or CI status/log was executed or inspected.

## Addendum: precursor appendix

Reviewed `appendices/precursor-study.tex` as it existed at
2026-10-06T01:27:18 UTC; SHA-256
`8f411c6cb826d34e34b4d6ad9be93a313e8774182eb88ddf6164a4b5ff74dc98`.
The previously unresolved appendix reference is now resolved. The snapshot
already removes the sentence combining 104, 100, and seven trajectories, but
still says 23 trajectories reached a fixed point after one tightening round.
Direct inspection of the saved histories supplies a more precise correction
than the archived independent review, and supersedes that review's “23” claim.

### Trajectory definitions and correction

There are 339 successful known-cutoff records with a `full` trajectory.
Exactly 104 of those full trajectories have **one saved history entry**. Their
first-round outcomes partition as follows:

| First-round status | Count |
|---|---:|
| Completed, no bound changed | 97 |
| Capped, no bound changed before stopping | 3 |
| Capped, at least one bound changed before stopping | 4 |

Thus 100 of the one-entry trajectories changed nothing, and seven were capped,
but those two groups **overlap in three**. Neither number counts convergence
after one productive round.

Another 23 records have a productive first round and a zero-change second
history entry. Of these, **22** have a completed second round. The remaining
record, `qspp_0_10_0_1_10_1`, has `capped=True` in round two, with 64 LPs for
180 candidate variables and cumulative round time 401.282701253891 seconds.
Round one changed four bounds. No conclusion about completion of its second
round follows from the zero-change counter.

Recommended manuscript wording:

> Among the 339 known-cutoff trajectories, 97 completed their first round
> without a bound change and seven were interrupted in that round. A further
> 22 trajectories changed a bound in the first round and then completed a
> second round with no accepted change. One additional trajectory had no change
> recorded in its second round, but that round was interrupted by the time cap.

These are numerical stopping events under margins, filtering and improvement
thresholds. Do not call them exact fixed-point certificates. Likewise, name
`fp` as the study's no-change-or-limit rule when saying that the Gauss–Seidel
and Jacobi trajectories “reached their fixed points”; some were capped.
`audit-evidence.md` now explicitly supersedes its earlier transcription of 23.

### The two post hoc timing adjustments

The proposed ratio adjustments are arithmetically correct if—and only if—the
stated operation replaces each wrong run's recorded time by 600 seconds while
leaving every other recorded time unchanged. This is a saved-record adjustment,
not a rerun of the solver or archived analyzer.

For shifted geometric mean `s`, shift one, `n=678`, and replaced old time `t`,
that operation gives

`new_s = (s + 1) * (601 / (t + 1))**(1 / 678) - 1`.

The native SCIP mean remains `7.179200023594989` seconds. Substitution gives:

| Arm | Original shifted mean | Replacement shifted mean | Original ratio | Replacement ratio |
|---|---:|---:|---:|---:|
| Control | 8.304075119435538 | 8.34448851048594 | 1.1566852981033486 | 1.1623145312933394 |
| r5 | 8.839713569076535 | 8.864921955269544 | 1.2312950663060147 | 1.2348063748236993 |

The replaced raw totals are `30.816858053207397` for control and
`105.04316854476929` for r5. Therefore 1.157→1.162 and 1.231→1.235 are correct
three-decimal ratios, and their two-decimal **ratios** remain 1.16/1.23. Their
two-decimal **time columns** change to **8.34/8.86**, so the statement that
“the two-decimal values in the table are unaffected” is false unless explicitly
limited to the ratio column.

Recommendation: retain the consistently **original descriptive timing
convention** in the table and remove this post hoc adjustment paragraph; state
clearly that solved counts exclude flagged wrong answers but recorded time and
node summaries are the archived originals. This avoids expanding the appendix's
analysis scope. If the root instead retains the narrow adjustment, update the
two time cells to 8.34/8.86 and explicitly label both affected time/ratio entries
as replacements computed from saved records using the displayed formula.
Do not imply that this corrects node ratios or all other comparative tables.

The saved node summaries use the original `solved=True` selection, including
the two wrong rows. The current text acknowledges archived node ratios only
near the first table; the same caveat must also cover the pipeline/control and
gap-closure subgroup summaries. If that qualification obscures the exposition,
remove the affected comparative node/solve-time summaries instead of treating
them as corrected. No exhaustive corrected node reanalysis was performed here.

### Control-subset counts are correct

The corrected SCIP control count **441**, rather than 442, in the OBBT-ran
subset is correct. It should not be changed to 440. There are 546 model–seed
pairs on the 273 SCIP instances whose root did not report optimality:

- Control: 442 original `solved=True`, **441** after excluding `wrong=True`.
- r1: **438**; ad0.8: **439**; fp: **429**, all unchanged.

The Gurobi subset has 476 pairs on 238 instances and corrected control **440**,
with 435 for r1/ad0.8/fp. This follows directly by excluding names with an
optimal root record and reading the saved `solved`/`wrong` flags. Corrected
all-cohort control/r5 counts remain 573/563.

### Other appendix issues

- The hard-SCIP node maximum **1.27** is the correct two-decimal rounding of
  1.2653834682852336 for `ad0.5`; the prior report's range ending 1.26 was
  rounded inconsistently. The appendix's 1.06–1.27 is supported.
- The statement that large node reductions occurred *only on pairs* whose
  control solved in a few seconds overstates the reported **group means**.
  Replace it with “the largest mean node reductions occurred in groups whose
  mean control time was only a few seconds.” A group mean does not bound every
  pair's runtime.
- “The final solves were no faster” is too categorical when the table includes
  final-solve ratios 0.96 and 0.98. Say that the final-solve savings did not
  offset preprocessing cost in the total-time summaries.
- The new rho definition, delayed first-round adaptive cap, corrected solve
  counts, reference coverage, conditional contraction histogram, and OBBT-level
  tables otherwise agree with the saved sources and prior evidence review.
- All 4,573 numerical reference-containment checks retain their tolerance and
  numerical scope; do not reinterpret them as an exact proof of validity.

Additional verification actually performed: read-only source/table inspection,
and a standard-library Python heredoc that classified saved trajectory flags,
read solved/wrong flags in the saved subset, and applied the single-record
shifted-mean replacement formula above. No solver, archived analyzer, numerical
fixture, project-wide check, or CI inspection occurred.
