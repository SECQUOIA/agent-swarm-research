# Stage 3 independent review 01, round 01

Reviewer: `/root/reviewer01`. Date: 19 September 2026.

## Verdict

**No major issue found. Two minor wording/specification fixes are required.** The generated models, witness constructions, domain and convexity arguments, and positive/zero-weight cone representations are mathematically sound. The comparative results retain their proper narrow, numerical interpretation. The data regeneration and narrative checks pass in an isolated copy, and all 47 frozen Stage 3 fingerprints match.

I reviewed the entire new stage, with particular attention to the mathematical model appendix and its consistency with the accepted theory. I did not read other current Stage 3 reviewer reports, edit manuscript sources, or spawn agents. Stage 4 packaging and remaining sections are not omissions in this review.

## Required minor corrections

1. **Restrict monotonicity to the nonnegative argument box.** `sections/appendix-formulations.tex:52` says “All laws are increasing, convex and differentiable on a neighborhood of the box.” Quadratic `phi(z)=4z^2` and trig have negative derivatives immediately to the left of zero, so they are not increasing on an open neighborhood of `[0,10/11]`. They are increasing on that interval and convex/differentiable on a sufficiently small open neighborhood. Separate those clauses explicitly. The domain, convexity, finite-gradient and epigraph-bound conclusions remain valid; no model or computational correction follows from this wording fix.

2. **State the exact two-dimensional representation transformation.** `sections/oracle-diagnostics.tex:75` calls the design “the base row and six exponential transformations” but does not explicitly write the transformed row or identify its six parameters in that paragraph. Add `q(x)=x^TQx-1`, `exp(a q(x))-1`, and `a in {1,2,4,8,16,32}` (or an exact cross-reference to a definition supplying all three). The scalar section and source make the intended interpretation inferable, but the full two-dimensional design should be unambiguous in the standalone paper. Source: `code/minlp_solver_lab/lbesh_oracle_diagnostic.py:26`, `:34`–`:52`, `:157`–`:165`. This is a specification improvement only; the reported 896-cut count agrees with that design.

## Mathematical reconstruction

### Generated models and witnesses

- The allocation objective, mode capacities, off-mode equality, demands, resource row and neighboring-unit congestion match `lbesh_research/instances.py`. The declared row and variable counts are correct when an original affine equality is counted as one model row.
- All three cost arguments remain in `[0,10/11]` using only individual variable bounds. Log and reciprocal arguments stay strictly within their domains. The displayed second derivatives are correct. Trig curvature remains positive since `15/11 < pi/2`. Convexity extends to an open neighborhood, notwithstanding the monotonicity wording correction above.
- Positive weights and nondecreasing costs on the actual box justify the finite `T_i` upper bound. Bounding a positively priced epigraph this way preserves every optimal production decision; the manuscript correctly does not claim preservation of arbitrarily large redundant epigraph values.
- The allocation witness uses total production `0.50 U_i`, strictly below the smallest standard capacity `0.58 U_i`, meets both demands exactly, and lies strictly within both inflated resource budgets. Its chosen cost values meet their epigraphs and finite bounds.
- The region formulation is a sum of positive affine exponentials, and its log-sum-exp interpretation is equivalent because each radius is positive. The global nonlinear rows are convex sums of affine squares. The maximum congestion component magnitude is three, giving `t <= 9n` without excluding a minimum-cost epigraph lift.
- Mode-1 centers satisfy the region inequalities with value four, demands with the stated positive margins, and variation at most `0.0512n`. The stated witness therefore works for every draw in the declared ranges. Compactness, continuity and finite alternatives establish attainment and finite optimal value for both designs.
- The sequential random draw order agrees with the generator, including paired coordinates before subsequent parameter groups. Reconstructing the 51 parameter streams in the isolated narrative check reproduced all coefficient digests.

### Conic formulations and interaction with the main theory

- The exponential cone's closed zero-scale slice is correctly stated and agrees with the cited CVXPY documentation. The scalar rotated-SOC identity has the correct factor two and side conditions.
- For positive weight, the exponential row yields `(e^1.5-1) q + y >= y exp(3z/y)`; the log row yields `q >= -y log(1-z/y)/log 2`; the reciprocal product yields `q >= y[(1-z/y)^(-1)-1]`; and the quadratic product yields `q >= 4z^2/y`. These are exactly the intended perspective epigraphs.
- At zero weight, copied box bounds force the original copied argument to zero. Allowing positive auxiliary q in an individual zero-scale cone would not alone force a zero lifted auxiliary; the manuscript correctly supplies the missing aggregate argument: the copied cost variable is zero and every cost coefficient is strictly positive for the drawn operating alternatives, forcing all q to zero. Off modes have their own copied cost equality. No spurious positive-weight or zero-weight restriction is introduced.
- The region cone construction similarly forces all four exponential auxiliaries to zero at zero weight. For positive weight, summing their lower bounds recovers the exact perspective inequality. It describes individual hull intersections with global constraints, not the full GDP convex hull, consistently with the earlier theory.
- The quadratic adapter's equality definition of s is equivalent to the quadratic perspective at positive weight. Scaled bounds and that equality force both the copied vector and s to zero at zero weight. Preserving affine-square terms with `z_k=A_k nu+b_k lambda` gives the correct homogeneous perspective. The exact-rational PSD check really operates on represented float coefficients and does not clip eigenvalues.
- The norm and positive-reciprocal epigraph descriptions match the adapter. For positive numerator, `a <= t d` with nonnegative t,d excludes d=0 and preserves the division domain. The restriction to convex monotone positions is necessary and present.
- The appendix does not claim the external stress models all satisfy the compact smooth oracle hypotheses. Its A/B/C grouping, unbounded automatic epigraph discussion, norm nondifferentiability at zero, positive farm-width deductions and distinction between original model feasibility and raw initial-value failures are consistent with the scoped theory. The no-norm stratum is expressly weaker than a theorem-assumption stratum.

## Empirical, provenance and writing assessment

The design keeps the related generated controls, pilot chronology, preliminary root inspection, unchanged search seeds, concurrent-worker variation, common ECP initialization, numerical acceptance, and outcome-triggered followups visible. This supports a controlled policy comparison, not an independent solver-superiority claim.

The results and generated tables keep failures in their declared schedules, use identical common-solved cohorts for paired time/work comparisons, distinguish shifted geometric means from arithmetic work means, and report medians that reverse some mean effects. The exact quadratic conic comparison, external lack of accepted-count gains, failed no-integer-NLP ablation, and unsuccessful fractional-cut ablation remain explicit. The root/enumeration evidence is not upgraded into a certified dual or infeasibility proof. The additional oracle experiment carefully separates measured function counts from GDP runtime and uses a common geometric stopping criterion.

All new citation keys resolve. The added references provide solver/model-source context without introducing an unsupported novelty assertion. I checked the newly used exponential-cone definition against the primary documentation and Clarabel metadata against its primary arXiv page. The manuscript's direct mathematical derivations do not depend on a solver documentation claim alone.

I found no reason to request further benchmark campaigns, a new baseline, new theoretical priority claims, or changes to frozen evidence for this stage. The two local fixes above are sufficient for my findings.

## Checks actually performed

1. Read `process/stage03-author.md`, the 47-file fingerprint record, all four new Stage 3 section files, the appended empirical oracle subsection, the new bibliography entries, both scripts, compact-data README/provenance, and the generated-table construction logic.
2. Ran an inline Python SHA-256 check of `process/stage03-author-source-sha256.json`: **47 files, zero mismatches**.
3. Created an isolated copy at `/tmp/lbesh-r01-stage03-9blhjcq1/paper`, then ran:
   - `python /tmp/lbesh-r01-stage03-9blhjcq1/paper/scripts/check_evidence.py`: **passed**, including 51 independently reconstructed parameter streams, cohort/narrative statistics and oracle checks.
   - `python /tmp/lbesh-r01-stage03-9blhjcq1/paper/scripts/regenerate.py --no-figures`: **passed**, producing 17 tables and all 1464 CSV records.
   - Compared the 17 regenerated table files, CSV and table-values JSON against the frozen source copies: **19 byte-identical outputs, zero mismatches**.
4. Used targeted `sed`/`rg` reads of `lbesh_research/instances.py`, `conic_reference.py`, `conic.py`, `validation.py` and `lbesh_oracle_diagnostic.py`. Reconstructed the cone and witness proofs independently rather than treating the scripts as proof.
5. Ran a citation-key check over all section files and `references.bib`: **no missing keys**.
6. Opened [CVXPY solver/cone documentation](https://www.cvxpy.org/tutorial/solvers/index.html) and [Clarabel's primary manuscript record](https://arxiv.org/abs/2405.12762). The exponential-cone zero-scale slice and Clarabel title/authors are supported. An attempted direct open of the Gurobi constraint documentation returned a tool internal error; I do not claim that page was verified in this review.
7. One initial guessed generator filename did not exist; the subsequent directory inspection located and read `lbesh_research/instances.py`. That failed read changed nothing.

No shared manuscript/data files were rewritten by the checks. I did not rebuild the PDF, regenerate figures, rerun solver benchmarks, rerun the full raw-data audit, inspect CI, or execute project-wide tests. The author's fresh raw-audit results and the lead's targeted generator/conic test results are recorded evidence, not executions claimed by this reviewer.
