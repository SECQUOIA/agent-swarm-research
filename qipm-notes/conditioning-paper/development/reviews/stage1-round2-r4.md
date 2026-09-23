# Stage 1, round 2 — independent reviewer 4

Decision: **No major issues remain in the Stage 1 deliverables.** One minor literature-map refinement is identified below. The planned mathematics still requires the scheduled authoring and full proof review.

## Correction assessment

I read the updated scope/literature audit, bibliography, correction log, progress record, and first-round reviewer 5 report. My first-round numerical-reproduction finding is fully addressed: Stage 5 now requires commands, versions, seeds, data provenance/checksums, transformations, output mapping, declared dependencies, and machine-readable failure/cutoff records.

The major missing-literature finding is substantively corrected. I independently accessed the public author-uploaded [Peña manuscript](https://www.researchgate.net/publication/220588878_Two_properties_of_condition_numbers_for_convex_programs_via_implicitly_defined_barrier_functions), revised May 9, 2001. Its Proposition 2.3 identifies the implicit Hessian inverse; Proposition 3.2 gives the stated primal-gap reparameterization bounds; and Proposition 3.7, Corollary 3.8, and Remark 3.9 give the reported Schur-system conditioning bounds and attribution. The audit distinguishes those matrices from the proposed reduced primal Hessians, credits the old use of objective gap, and expressly withholds generic-upper-bound novelty claims. It does not infer absence of overlap from unavailable sources.

I also reopened [Renegar's publisher page](https://epubs.siam.org/doi/10.1137/S105262349427532X). Its abstract supports the conditioning/approximate-CG description. The corresponding full-text access limitation is honestly stated. This limitation need not block self-contained development with the currently restrained originality language.

The updated common-gap interval, uniformly bounded barrier-family qualification, coordinate-change quantifiers, weak-subspace distinction, and norm-versus-squared-mass wording address the other first-round concerns. The direct approximate-containment lead in the progress record is plausible: the residual bound controls the initial line derivative, the integrated self-concordant inequality controls its later value, and semiboundedness controls the remaining feasible distance. These remain candidate proof steps, as labeled.

The scope is coherent and no additional mandatory repository result was found. The all-barrier comparison, attained geometric examples, LP endpoint limits, and solver/formulation implications form a reasonable standalone package.

## MINOR R4-2: record the SDP spectral-cluster antecedent exposed by the new source

**Location:** Scope audit subsections 2a and 3, and Stage 3/4 literature obligations.

**Evidence:** Immediately before its Proposition 3.7, Peña's manuscript discusses prior SDP Schur-matrix eigenvalue clustering and presents Proposition 3.6 attributed to Alizadeh and collaborators. Its reference [1] is Alizadeh–Haeberly–Overton, *Primal-Dual Interior-Point Methods for Semidefinite Programming: Convergence Rates, Stability and Numerical Results*, SIOPT 8 (1998), 746–768. A local package already exists at `literature/papers/alizadeh1998-primal-dual-interior-point-methods/paper.md`. Peña's second reference for that proposition is a private communication, so the displayed full classification must not automatically be attributed verbatim to the published article.

**Suggested fix:** Add this as a concrete primary-source screening obligation for the SDP spectral discussion and fractional example. Inspect the local primary material before assigning exact results or theorem locators, and preserve the Schur-versus-reduced-Hessian distinction. The final paper should credit established SDP spectral clustering where relevant, while identifying precisely what its non-strictly-complementary fractional example adds. This is minor at the planning stage because the current novelty language is already restrained and no unverified SDP comparison appears in the manuscript.

## Outcome

Address the small literature-map refinement and proceed to Stage 2. This review does not require another five-reviewer round on Stage 1. Final priority wording must still be judged against the actual proved results and the planned source comparisons.
