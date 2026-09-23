# R3 final independent whole-manuscript review — reviewer 1

## Verdict

**No major issues and no valid minor issues identified.** The complete revised manuscript is mathematically coherent, scientifically complete for its stated method-and-reliability contribution, and substantially clearer in how it connects the research problem to the results. I request no further correction. This judgment concerns the actual scoped claims and evidence; it does not predict journal acceptance or preclude useful future research.

I independently reread the current `main.tex`, all nine section files, all five tables in their manuscript context, and the five generated TeX inputs under `tables/`. I also consulted the current literature map, formal coverage map, and the primary evidence already examined in the preceding independent reviews. This is a whole-paper review of the combined R1 and R2 result, not an approval based only on their diffs. I did not consult another R3 review, delegate, edit the manuscript, or rerun unchanged campaigns, proof archives, tests, or Lean builds.

## Mathematical scrutiny

**The model and the guarantee agree.** Section 2 specifies exact loaded-tree rational semantics, definedness and normalized convexity on the declared box, affine equalities, original integrality, and objective-sense normalization. It does not promise source-decimal equivalence or reverse earlier floating aggregation. The introductory pointwise bound is exactly the conclusion established in Section 3. Empty feasible sets and lack of attainment are handled without using an inappropriate real-infimum convention. The actual primal witness restores nonemptiness when the paper makes a finite gap or optimality claim.

**The safe-cut argument is correct under its explicit premises.** I rechecked sign reversal in affine propagation and the preservation of mixed-integer feasible points under integer endpoint rounding. For the residual correction, finite intervals use the correct endpoint maximum; lower half-lines require nonnegative residual slope, upper half-lines nonpositive residual slope, and free coordinates exact zero. The enclosing endpoint choices correctly account for the negative displacement at an upper endpoint. Fixed coordinates contribute zero, and sparse omitted slopes do not remove affine-only residual terms. Adding and summing these inequalities yields the stated intercept condition. The rounded-tangent counterexample, corrected intercept, squared-polynomial identity, and half-line alternative are consistent. The text never identifies this sufficient correction with the strongest possible cut.

**The discrete invariant is strong enough for the claimed master bound.** The incumbent cutoff is explicitly relative to a restricted feasible set. Exact feasibility of the supplied incumbent, rather than an optimality assumption, supplies the comparison needed to extend its bound to the whole master. Strictly backward references justify induction. Sign-compatible combinations, integer-variable/coefficient checks for rounding, and complementary integral branch assumptions support the admitted rules. The unsplit dependency union retains cross-branch assumptions. A sufficient earlier bound does not excuse an invalid suffix. The master infeasibility implication and the public finite-bound API are consistently distinguished.

**Transfer and primal completion use the required premises.** The feasible extension preserves original variables and integrality, supplies the true normalized objective as the epigraph coordinate, and includes the affine constant once through the fixed constant coordinate. Original affine rows, justified bounds, and safe nonlinear cuts all hold at that extension. Checked master identity therefore connects the bound to the intended nonlinear model. The primal corollary requires an actual original-model point, including bounds and integrality; a master point or recorded objective cannot replace it. Matching finite primal and dual evidence gives attainment as claimed.

**Curvature, boundary derivatives, and formal coverage remain appropriately limited.** Section 4's global quadratic PSD criterion, homogenized norm argument, monomial Hessian/Schur test, integer even-power condition, and one-variable fractional second derivative have the correct assumptions and signs. Boundary support is justified through derivatives along feasible segments, not inferred solely from finite coordinate partials. The derivative and interval implementations remain trusted. Section 5 and `formal/COVERAGE.md` accurately identify genuine coordinate and finite-sum proofs, semantic graph/transfer and cutoff-lifting results, and primal-infimum hypotheses. They explicitly exclude the concrete parser, curvature/support computation, interval implementation, VIPR invariant, and executable replay. No claim of fully mechanized benchmark certification has appeared in the revised framing.

## Scientific contribution, empirical evidence, and readability

The abstract and early introduction state a concrete research problem: exact discrete evidence needs valid nonlinear cuts and a justified identity between the proved master and the nonlinear relaxation. The method, empirical findings, validation, and reusable artifacts then answer different parts of that problem. The theorem section supplies the complete implications; the implementation section identifies the concrete checks and trust boundary; the experiments measure capability and expose failures. The revised conclusion draws lessons from those results. This is a consistent scientific argument rather than a collection of development reports.

The novelty boundary is precise. Outer approximation, supporting-plane minimization, geometric convex-MINLP certificates, and rational discrete proof checking retain primary attribution. Halbig is identified as the closest computational comparison; the different checking procedures are described without a first-system claim. Baes's supporting-point bound remains distinct from serialized bit length and conditional on the cited hypotheses. The absence of a Slater or attainment assumption in a conditional bound-transfer theorem is not presented as a general certificate-existence result. Selected Lean proofs and software tests are validation, not claims to originate verified optimization.

The capability/failure/cost organization preserves the distinctions that make the empirical claims assessable:

- The 299-name selection and ten earlier exclusions yield the complete 289-name attempted population. The frozen 203 accepted replay artifacts are distinct from 198 successful producer returns and from the strongest-bound union of 222 models.
- Reference comparisons use exact signed rational differences and remain unverified-reference comparisons. The quadratic and `clay0204m` optimality completions have separate original-model witnesses.
- Invalid supplied inference steps, conservative nonlinear rejection, an unreportable already-checked rational bound, and infeasible saved solver points are different findings. Local invalid steps are not claimed to prove false final bounds.
- The returned-point violations retain printed-precision bounds and source-formula semantics. The paper neither upgrades SBB's Integer Solution status to global optimality nor attributes an unobserved internal solver defect.
- V1, V2, and V3 counts remain separate. The anticipated full V3 total is explicitly not a completed additional uniform experiment. Appendix B preserves the protocols and repair accounting behind the main section.
- Timing populations, concurrency, solver thread requests, additional tool work, hashing, historical external checking, proof bytes, and memory dependence retain their qualifications. No performance ranking follows from these observations.

The two appendices provide a useful division between reproduction commands and full experimental accounting. Their cross-references and the introductory roadmap are correct. Required evidence has been moved to a clearly identified supporting location rather than dropped. The source/formal/core/bulk distinction is consistent across the paper and delivered documentation.

## Verification basis and current identity

The mathematical proofs, formal modules, and numerical evidence are unchanged from the earlier independent checks. I reuse those accepted checks, including the actual Lean source/axiom audit and exact cohort/reference calculations, rather than treating author assertions as new validation. During R2 I independently confirmed the 18 proof-related plus one reporting rejection, all generation status counts, equality of the 67 admission-error and missing-bundle identity sets, and the updated source archive contents/hash.

For this final review, `sha256sum -c PAPER-SHA256SUMS` again passes for all 49 current content files. In particular, the reviewed soundness, implementation, and formalization hashes remain respectively:

- `ad1a631d74bf26afee4b2b12ae25d877d2364ab09b3dfa98d1acd565ec1f8b92`;
- `31e59d55944642060baeecb3d4b1a78c836820fbaa1c10c113d1f82de93c66e5`;
- `99b57b196d5317350bc7a60dba837caf7c810fa5c3b36fc90d2c7b92d19c00e0`.

The current integrated `main.tex` hash is `a0974eb5a94f9a93b0403fa0a315221605f5828135165548a50c75f3ec769fe9`. Section 6 is `a0c484168ad499becbcc9a8c4e82539b508eeac1bfb7b2603f70c476351688f5`, and Appendix B is `e748fa24d66ce28fb8133c669983ac81ab8dd26f7061c7526e95f2178b66f61f`. The accepted fresh 33-page build and source extraction checks therefore apply to the manuscript reviewed here.

I found no unresolved mathematical, empirical, originality, or presentation issue requiring another correction or development stage.
