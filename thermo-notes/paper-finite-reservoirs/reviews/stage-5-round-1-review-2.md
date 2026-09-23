# Stage 5, round 1: independent review 2

Verdict: **no major issues**. The synthesis preserves the proved microscopic claims, and the proof relocation is exact. I identified two minor qualifications to make in the overview/status prose.

I reviewed the Stage 5 author record, abstract, introduction, numerical section, conclusions, appendix relocation, bibliography integration, README and coverage files, and the changed current research notes. I inspected the numerical source transfer and both figure images. I did not read another current-round review or the coordinator's current literature report, edit the manuscript, or delegate work.

## Minor findings

### R2.1 — Qualify the boundary result when first summarizing it

**Location:** `sections/introduction.tex`, paragraph beginning “At the boundary ...”, and the corresponding abstract sentence in `main.tex`.

The introduction discusses both microscopic realizations and then presents the boundary optimization without naming its additional integrability restrictions. Those restrictions are explicit in the theorem and conclusions, so this is not an unsupported theorem. Nevertheless, the early summary can suggest that every positive boundary coefficient is covered in the two-dimensional short-range example.

**Remedy:** Add “under the stated moment and exceptional-mass bounds” to the introductory boundary summary. A short following sentence can identify the application range: every positive coefficient for mean field and short-range spatial dimension greater than two, and sufficiently large coefficients for short-range dimension two. In the abstract, “Under suitable phase-tail bounds, at the ... boundary ...” is sufficient. The separate `c_N >> N^(3/2)` microscopic iff theorem remains unrestricted by this boundary-coefficient caveat.

### R2.2 — Distinguish the historical review completion from the pending full LaTeX review

**Location:** `research/results-summary.md`, Section 5: “The final manuscript and linear-capacity appendix passed their last reviews.”

After this file's new introduction and manuscript links, “the final manuscript” reads as the new LaTeX paper. Stage 5 and the later full-manuscript cycle are still in progress according to the author handoff and workflow. The sentence appears to be an inherited statement about the older Markdown manuscript and its appendix.

**Remedy:** State explicitly that the earlier Markdown manuscript and centered linear-capacity note completed their reviews, and that the LaTeX manuscript's current staged/full-review status is recorded in `WORKFLOW.md`. Alternatively replace the sentence with the currently accurate Stage 1–4 completion statement. Once the final full cycle is actually complete, the coordinator can record that new completion separately.

## Proof preservation and microscopic scope

I independently reconstructed the pre-relocation microscopic section by removing its new main-text proof guide, appending the contour appendix without its new introduction, and restoring the original heading levels. Its SHA-256 is exactly:

`4f6cfab2a45063487df9a706731ca9a670f7231f4825410a72c518e3c9061fe2`

This matches the accepted Stage 2 round-2 file. Thus the BCT convention, both-side pressure identification, cutoff-removal proof, derivative estimates, midpoint/contour distinction, and bond-to-spin transfer have not been lost or altered in the move. The main-text proof guide accurately describes their roles and points to the complete appendix.

The principal overview claims match the proved statements: sufficiently large fixed `q`, each fixed spatial dimension `d>=2`, optional kinetic coordinates, and exactly two distinct phase energies despite ordered-color degeneracy. The conclusions correctly preserve the narrower boundary range in dimension two. They do not promote the square-torus rate model to microscopic morphology, infer kinetics from barrier heights, or infer microscopic information from TV alone.

The repository status changes correctly identify the old short-range sufficiency gap and the pure-spin mean-field restriction as resolved. The older route's remaining tasks are explicitly marked historical. The anisotropic effective metric and semidefinite qualifications agree with the corrected Gaussian appendix. The newly completed optimal-loss equality is linked to its proof and distinguished from its established geometric mechanism.

## Coverage and organization

The coverage map accounts for the relevant reservoir notes through the stronger support theorem, two-phase positive-tail criteria, microscopic models, shared-bath results, exact Gaussian geometry, boundary optimization, capillarity model, and probability/barrier diagnostics. The older three-phase physical theorem is indeed subsumed by the weak-support result; it does not contain an omitted separate boundary law. The separate survival, kinetic, reactive-capacity, inverse-interface, and generic Hamiltonian-uncertainty projects do not supply a missing lemma for this manuscript and are reasonably excluded.

The main route now emphasizes the physical problem and microscopic consequences. Moving the lengthy positive-contour proof and exact auxiliary models to appendices improves readability while retaining all proofs in the same PDF. Stable labels remain intact. The table distinguishes one fluctuation window, two distinct energies, and three or more macroscopic energy support points. It does not mistake ordered-color multiplicity for three energy phases.

## Literature checks

The comparisons are narrow enough to be supported by the primary material I checked:

- Griffin–Matty–Swendsen's retained primary equation (23) is the Euclidean norm of energy-probability differences; their Section VI explicitly optimizes the comparison inverse temperature. The introduction accurately identifies both distinctions from the prescribed-target TV problem.
- Riera–Gogolin–Eisert's retained Appendices A–B bound trace distance by the bath entropy remainder and give a sufficient bath-size dependence involving the squared subsystem Hamiltonian norm. The text properly credits the strong-distance squared-range sufficient scale and claims a different optimized necessity/two-phase refinement.
- The retained Diaconis–Freedman primary report states the regular exponential-family growing-block conditional variation theorem. Its reference is pertinent and is not treated as a microscopic coexistence theorem.
- The retained Challa–Hetherington texts support Gaussian finite-reservoir ensembles and fluctuation changes. The previously checked Challa–Landau–Binder 1986 primary publisher abstract supports weighted Gaussian phase peaks. The Gaussian valley/surface-cost distinction is also directly justified by the manuscript's own scale calculation.
- Cohen–Rittenberg–Sadhu Section 4.3 explicitly identifies order-one information changes from phase degeneracy, consistent with the limited introduction claim. The opposite-phase precedent is also retained and credited rather than presented as an unprecedented mechanism.
- The local primary Corti–Ohadi–Fariello–Uline 2023 paper discusses isolated contact between small ideal-gas subsystems and the finite-system consequences of surface versus volume entropy. The conclusion uses it for that context and does not import its broader entropy-definition position as a theorem of this paper.
- The primary arXiv records for [Mishin 2015](https://arxiv.org/abs/1507.05662) and [Yoneta–Shimizu 2019](https://arxiv.org/abs/1903.04111) confirm the cited publication metadata and their finite-reservoir fluctuation and finite-size ensemble-conversion scope. The introduction's distinction from preserving a full canonical phase mixture is appropriate.

The attempt to independently reopen the 1990 review publisher page returned HTTP 403. I therefore do not claim a fresh full-text verification of that review; its access limitation remains explicit in the bundle. No theorem in the manuscript relies on an unavailable derivation from it. I performed no new exhaustive priority search, and this report does not certify novelty.

## Numerical and reproduction checks

The copied archival data hash independently equals the README value:

`93fed9507ceaf9126feb93e79ae5bbb295be185a56f9a84dabe0608e55aab2c1`

An AST comparison finds `canonical_energies` and `finite_bath` identical to the previously independently checked source functions. The new command-line layer keeps the archival file separate, exposes modest and full reproduction plans, and defaults to a separate recomputation output.

The plotting code uses the full energy/full-state TV field, not the spin-configuration marginal. Its phase weights, variances, and boundary slope agree with the proved microscopic formulas. Both figure images are readable. The captions correctly distinguish exact finite-system occupation/CDF evaluations from evaluations of a limiting formula, identify the shorter size range for the nonboundary sequences, and disclaim a short-range numerical test. The README explains the historical capacity-field convention and the ordinary floating-point nature of the checks. It does not claim rigorous interval validation or a repeated large-size run.

This Stage 5 review is separate from the still-required whole-manuscript review.
