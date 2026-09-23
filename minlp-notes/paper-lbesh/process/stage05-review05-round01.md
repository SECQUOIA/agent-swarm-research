# Final whole-manuscript review 05, round 01

Reviewer: `/root/reviewer05`. Date: 19 September 2026.

Read `process/stage05-author.md`, verified its frozen source set, and reread the complete scientific manuscript: abstract, introduction, related work, model/cut results, guarantees overview, implementation, study, results, discussion, conclusion, all mathematical/oracle/model/reproducibility appendices, all 17 tables and all 27 bibliography entries. This was a new whole-manuscript assessment rather than an assumption that prior stage approvals were sufficient. I did not read other current final review reports, edit manuscript sources, or spawn agents.

## Definitive verdict

**Accept the manuscript in its stated computational and methodological scope. No actionable major or minor issue was identified in this final review.** No additional development or experimental campaign is needed to support the claims actually made. The evidence does not establish a major new algorithm or broad solver superiority, and the manuscript does not present it that way. Editorial judgments about fit and significance remain separate from the scientific and presentation checks reported here.

The abstract now distinguishes perspective cuts in hull masters from tangent deactivation in big-M masters, expands NLP, and qualifies conic comparisons by common-solved mean time. The conclusion preserves mixed external coverage and limits its error-bound statement to the absence of a general linear bound without additional joint regularity. I found no surviving overstatement from the earlier formulations of those passages.

## Mathematical and scientific assessment

1. **Model and hull construction.** The finite row sets, original integer coordinates, native indicators, affine logic and bounded domains are stated explicitly. The neighborhood assumption handles ambient gradients at fixed coordinates. I checked the perspective derivatives, vanishing-weight continuity, complete tangent identity, inactive-origin treatment of empty alternatives, and both directions of the separate-disjunction convex-hull proof. The manuscript does not silently replace the intersection of separate hulls by the full GDP hull. The big-M coefficients are valid box maxima, and the compact epigraph result preserves an optimal lift under the stated no-other-role condition.

2. **Separation and numerical contracts.** Reconstructed the anchor inequality, ESH margin and coefficient norm bound, integral rowwise packing, fractional packing in copied-variable/weight space, safe omission threshold and weaker fixed-cutoff guarantee. Constant rows and zero weights are handled without an unstated strict-feasibility requirement. The geometric repair proof preserves a term's affine rows, and the square-root intersection example correctly disproves the claimed linear error inference. The value argument uses a common compact domain, valid relaxations and vanishing residual/suboptimality. The single-tree result explicitly requires old-cut resolution and finite optional refinement. The coefficient-error relaxation correctly loses `2E` plus the stored-cut feasibility tolerance. These exact statements remain distinct from the observed numerical solver behavior.

3. **Representation diagnostics.** Checked the composition-chain-rule argument, positive scaling at the boundary, same-point ECP weakening, actual scalar master recurrence, strict transient bound and fixed-parameter quadratic Newton expansion. The centered ellipsoid formulas and off-center disk witnesses prove precisely the stated conditional dominance and general non-dominance. The empirical diagnostic specifies the transformed rows, common geometric stopping criterion, counted value/gradient operations, finite root stopping and timing exclusions. It does not impute those oracle counts to GDP runs that did not record them.

4. **Generated models and cones.** Rechecked the five laws and derivative/domain claims, allocation objective and explicit witness, regional demand/variation witness, and finite epigraph bounds. The parameter specification makes the 51 generated models reproducible without repository notes. Positive-weight cone algebra recovers the intended perspectives. At zero weight, scaled bounds and aggregate cost or radius rows exclude spurious copied points and force the relevant auxiliary values to zero. The quadratic slack lift and norm/reciprocal adapter scope are accurately qualified. The external model classification does not mistake successful structure extraction for satisfaction of all smoothness/compactness assumptions.

5. **Literature and contribution.** The paper identifies established perspective, logic-based OA, radial supporting-plane, SHOT, disjunctive-strengthening and conic precedents, and distinguishes this implementation's procedure from stronger or differently represented relaxations. I revisited the local primary SHOT fulltext, including its abstract, Section 2 conditions and fixed-integer heuristic discussion; these support the corresponding attribution. The manuscript's contribution is the matched GDP evidence and its interpretable diagnostics/contracts, with no first-ever priority claim based on search absence.

6. **Study and results.** The eight benchmark batches, separate reference calls, 18/33 split and related parameter streams are accounted for. Same-seed repetitions, concurrent work, shared initialization, conditional timing cohorts and failure-penalized PAR10 are explained. Every unfavorable result remains visible: equal external counts, supported conic timing advantage with mixed coverage, weak user-cut benefit, severe no-recovery ablation, invalid witnesses, failed exports and missing bounds. Outcome-triggered follow-ups remain separate. The numerical acceptance, cross-witness tolerance and reference-agreement formulas are explicit. Arithmetic means, medians, shifted means, total cut time and per-cut cost are not conflated.

## Reader flow and standalone completeness

The abstract and introduction make the question and limited positive finding easy to locate. The model and concise guarantees overview explain the intervention before the implementation and study. Full proofs follow in appendices with resolved references. The detailed model specifications and tables make the experimental meaning recoverable without internal notes. The interpretation consistently separates exact mathematical conditions from finite-tolerance implementation behavior.

The source and frozen research supplement have different, clearly described purposes. A reader can build from the local bibliography and supplied graphics, regenerate numerical presentation, or audit saved witnesses without mistaking these tasks for optimization reruns. Required environments, separate conic lockfile, native solver dependencies, GDPlib import-path selection and fresh audit-output requirement are documented. The paper does not invent authorship, funding or a public data identifier.

The sampled final pages show readable equations, proof structure, references and appendix formulations. No missing cross-reference or clipped content was found. The remaining bibliography underfull-box diagnostic is harmless and is not a requested correction.

## Checks actually executed for this final review

- Verified all **68** entries in `process/stage05-round01-source-sha256.json` against the current files.
- Extracted the delivered source archive into `/tmp/lbesh-stage05-review05-ffq3g4zk/paper-lbesh`; independently verified all **62** embedded-manifest payload hashes/sizes and compared each payload byte-for-byte with the current repository source. Confirmed `main.pdf` and `dist/paper-lbesh.pdf` are identical.
- Independently scanned LaTeX labels/references and citations: **83 unique labels**, all reference targets resolved, and all **27** bibliography keys cited with no missing keys.
- Ran a forced clean build in the extracted source directory: `latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex`. It passed with **42 pages**, no undefined citations/references, no overfull boxes, and only the inherited bibliography underfull line.
- Used `pdftotext -layout` and newly rendered/viewed pages **8, 27 and 35**, covering the overview-to-algorithm transition, error/value results and conditional solver contract, and conic adapter/model scope.
- Independently counted all eight compact-data batches, totaling **1,464** records. Recomputed every held-out single-tree ESH/ECP common-solved ratio across the three schedules without importing the manuscript scripts: hull `0.9405887162`, `0.9505880886`, `0.9405393662`; big-M `0.9574286262`, `0.9460339820`, `0.9376460042`. Accepted counts are `[33,32]` for each hull schedule and `[33,31]` for each big-M schedule. These support the abstract's rounded 4–6% statement.
- Reread the current table fragments, bibliography and relevant local primary SHOT passages. Mathematical conclusions above were checked by reconstructing the arguments, not by treating numerical examples as proofs.

No complete saved-witness audit, figure regeneration, fresh environment installation, optimizer benchmark, project-wide test or CI inspection was repeated in this final review. Existing fresh-witness and relocation records remain identified evidence; I do not claim this final round supplied an independent second feasibility-checker implementation or an exhaustive proof of absence of every possible future reviewer concern.

## Required actions

None from this reviewer. The lead should evaluate the five independent final reports before declaring the overall process complete.
