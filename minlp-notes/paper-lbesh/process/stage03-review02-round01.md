# Stage 3 independent review 02, round 1

Reviewer: `/root/reviewer02`. Date: 19 September 2026. Reviewed the Stage 3 author record and frozen fingerprint, experimental design, results, model/cone appendix, computational appendix, appended empirical oracle text, compact data and regeneration/checking scripts. No other current Stage 3 review was read. No manuscript, solver, raw record or generated table was changed.

## Verdict

**Pass after two minor corrections; no major issue identified.** The principal counts, timing ratios, work summaries, numerical acceptance and reference accounting reconcile with original records. The paper keeps the modest controlled benefit, external nontransfer, exact-conic advantage and dependence on integer-point NLP recovery visible. Its conclusions are narrower than the supplied measurements and do not turn solver statuses or conic dual estimates into exact certificates.

## Major findings

None. In particular, I found no hidden change of denominator, exclusion of failed original runs, replacement of originals by improved follow-ups, pooling of repetitions, or overstatement of the cone reference scope. The unfinished abstract/discussion and archival packaging are Stage 4 work, not Stage 3 defects.

## Minor findings requiring correction

1. **Restrict monotonicity to the model box.** Location: `sections/appendix-formulations.tex:52`, “All laws are increasing, convex and differentiable on a neighborhood of the box.” Quadratic `4z^2` and trigonometric `(1-cos(1.5z))/(1-cos(.75))` are not increasing on any open neighborhood of the box `[0,10/11]`: their derivatives are negative immediately to the left of zero. They are nondecreasing on the box and convex/smooth on a sufficiently small open neighborhood. State those two facts separately. The bound on epigraph costs uses monotonicity only on the box, so this wording correction preserves the model, feasibility and boundedness arguments.

2. **State the cross-witness/reference comparison tolerance explicitly.** Locations: `sections/experimental-design.tex:35` and `sections/results.tex:52`. The gap gate is defined precisely, but “comparison tolerance” and “declared objective comparison tolerance” do not explicitly say which objective scales that tolerance. The source uses `T(w)=1e-6+1e-4*max(1,abs(w))` at the *comparison witness objective*. In the minimizing sense, a reported bound contradicts a validated witness when `B > w+T(w)` (reverse sense for maximization). An infeasibility report contradicts existence of any accepted witness. Enumeration agreement uses `abs(f-f_ref)<=T(f_ref)`. Add this concise definition or cross-reference an explicitly defined `T`; do not leave readers to infer that it is the feasibility-check tolerance or the own-incumbent gap scale. This is a standalone-method description issue, not a numerical discrepancy. Source: `lbesh_study_analysis.py:245–259`, `lbesh_results_independent_audit.py:31–32,121–131`, and `results/lbesh_development/analysis_v1/derive_ablations_references.py:60–65`.

## Independent raw-record and arithmetic checks

I wrote and ran `/tmp/lbesh_stage03_review02_check.py`, a separate standard-library checker, without importing the manuscript regeneration script or repository study analyzer. It verifies:

- Every file hash in the Stage 3 author fingerprint, all listed source-input/raw-record hashes, and all compact input hashes.
- All **1,464** compact benchmark records against the original JSONL records: run/instance/method uniqueness, outcome, raw status, wall time, objective, global bound, all inspected cut/LP/NLP/node/timing fields, LP exit and residual diagnostics.
- The acceptance calculation directly from original saved validation, completed-worker state, usable-bound flag and `abs(f-B)<=1e-6+1e-4*max(1,abs(f))`. Every compact accepted/not-accepted classification agrees. This checks aggregation and the gap gate; it deliberately does not pretend to be a new implementation of primal model evaluation.
- Batch cardinalities **663, 132, 132, 9, 351, 144, 9, 24**, summing to 1,464. Original and follow-up cohorts remain distinct.
- Every primary accepted-count and PAR10 cell; all primary ESH/ECP paired count, shifted-mean, ratio and faster-case cells.
- Paired work arithmetic means and medians, family/size timing ratios and denominators, formulation/tree contrasts, pilot ablation rows, external no-norm paired timing rows, and fixed-cohort repetition cells.
- The actual original **42** cone-root records: **40 optimal and two optimal-inaccurate**. Directly recomputed all reported 40-root precision-table entries from original cone dual estimates and original prototype LP bounds.
- The actual **14 × 27 = 378** fixed-assignment records: **174 optimal, 204 infeasible**, with no unresolved assignment status. Together with the roots this is **420** calls.
- All **182** accepted primary comparisons against the best enumeration objective, using the reference-scaled tolerance. Largest discrepancy/tolerance is **0.01321185162206496**, consistent with the manuscript's approximately 1.32% statement.

All these assertions passed. The source fingerprint stayed unchanged during the review.

## Other reviewed content and interpretation

Read the complete original-model validator and numerical assessment functions. The paper accurately distinguishes scaled primal tolerances from the prototype's internal absolute test, requires all original numerical variables, recomputes the original objective, and distinguishes valid points from usable global bounds. The explicit statement that the independent arithmetic audit reuses the original-model checker is accurate and should remain.

Inspected the baseline adapter, including native GAMS status/bound handling, SHOT tolerance options, hull initialization, and generated-only declared-convex option. The text distinguishes transformed-model and interface failures from solver search performance, and keeps the missing exported batch bound despite the native closed-gap log visible.

Read the generator formulas and draw order against `lbesh_research/instances.py`. Independently checked the derivative, box-domain, production-witness, geometric-witness and epigraph-bound arguments in the appendix. The monotonicity-neighborhood wording above is the sole mathematical correction found. The zero-weight cone reasoning and the distinction between a formulation's exactness and floating-point certification are sound. The optional positive auxiliary epigraph values at zero weight are removed by the positively weighted zero budget, as stated.

Reviewed the cone-adapter description, external expression/scope classes, table-generation formulas, and empirical oracle reporting. The excerpted data retain all six norm models in the stress stratum, distinguish 25 cone-supported models from all 27, and use the 19-model supported/no-norm intersection for cone timing. The fixed-anchor diagnostic, function-evaluation accounting, analytic support tests and tiny-duration timing caveat do not purport to explain every GDP runtime.

The same-seed repetitions, common-solved conditioning, concurrent workers, shared ECP initialization, large hard-case contributions to arithmetic work means, and absent full candidate/cut histories are all material limitations; the current Stage 3 text states them appropriately. No independence-based inference or universal separator dominance is claimed.

## Verification limits

No optimizer or full experiment rerun, project-wide verification, CI inspection, or LaTeX build was performed. I read the recorded fresh 174-witness/full-study audit but did not duplicate that evaluation. My independent checks use saved original validation outcomes and independently reconstruct acceptance arithmetic; that scope is distinct from revalidating nonlinear expressions. Abstract, integrated discussion and archival packaging remain for Stage 4.
