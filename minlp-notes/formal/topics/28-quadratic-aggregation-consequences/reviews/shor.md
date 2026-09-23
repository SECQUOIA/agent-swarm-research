# Independent review of the Shor consequences

Date: 2026-09-22. Reviewer: the hyperplane-geometry agent, independently of
these Shor modules' implementation.

Reviewed `ShorConeSeparation.lean`, `ShorDuality.lean`, `ShorBlock.lean`,
`ShorModel.lean`, `ShorAlgebra.lean`, and `Consequences.lean` against
Corollary 4 and Lemma 4 in
`results/quadratic-aggregation-trivial-hull-certificate.md`. Also inspected
the closed-hull equivalence used by the final statement and the definitions
of the imported matrix PSD predicates. No correctness defect, hidden
mathematical premise, or mismatch with those source statements was found.

## Statement fidelity

`System.shorProjection_eq_univ_iff_no_certificate` proves exactly the
Lemma 4 equivalence: under nonempty strict feasibility, the actual Shor
projection fills the ambient space if and only if there is no nontrivial
convex aggregation certificate. The certificate definition requires
nonnegative nonzero weights, a PSD quadratic aggregate, and at least one
nonzero quadratic or linear aggregate. Its negated existence therefore
means every convex certificate is trivial, as in the source. No hidden
hyperplane convexity assumption enters this equivalence.

`System.shor_and_hulls_eq_univ` proves both equivalences in Corollary 4
under nonempty strict feasibility and asymptotic hyperplane convexity.
`System.shor_and_hulls_eq_univ_of_hhc` supplies the HHC specialization.
The strict and closed hulls are ordinary convex hulls, not their closures.
The properness direction for a certified Shor projection requires neither
strict feasibility nor a hyperplane convexity assumption, as expected.

## PSD and lifting semantics

`shorBlock` is the standard matrix with first row `(1,xᵀ)` and remaining
blocks `(x,X)`, indexed by `Unit ⊕ Fin n`. The Schur-complement equivalence
identifies its PSD condition with `X - xxᵀ` PSD. Matrix `PosSemidef`
includes the Hermitian condition; over the reals this supplies the required
symmetry. Arbitrary matrix witnesses do not omit a symmetry restriction.

`System.mem_shorProjection_iff` proves exact equivalence of the covariance
slack definition with the source's lifted block-matrix formulation.
`tracePair A Y = trace(A Y)` agrees with the Frobenius pairing for the
symmetric matrices involved. The rank-one identity and nonnegative pairing
of PSD matrices are proved, rather than postulated. The aggregate
inequality is established for actual feasible lifted witnesses.

## Closure and strictness

The strict semidefinite alternative separates the actual affine image
`f(x) + (trace(A_i Y))_i`, for PSD `Y`, from the open negative orthant.
That image is proved convex and nonempty. Neither it nor the Shor
projection is assumed closed. The separating functional has nonnegative,
nonzero weights; testing arbitrarily scaled rank-one PSD matrices proves
PSD of the quadratic aggregate.

Absence of a nontrivial certificate forces the aggregate quadratic and
linear terms to vanish. Evaluating the remaining constant at a strictly
feasible point makes it strictly negative, contradicting separation.
This proves the stronger intermediate fact that every fiber admits a PSD
covariance slack with every lifted residual strictly negative. The final
Shor projection uses weak inequalities, exactly as in the source.

This route replaces the source's cone-closure and interior argument. It
does not assume that a linear image of the PSD cone is closed, or identify
an arbitrary Shor projection with the intersection of convex aggregations.
The source's auxiliary closure/interior identities are not separately
formalized by these modules; completion claims should concern Lemma 4 and
Corollary 4 themselves and describe the changed proof route.

## Verification boundary

This was a source and semantic review. A targeted text scan of the six
modules found no `sorry`, `admit`, custom `axiom`, or `unsafe` declaration.
No additional Lean build, project-wide check, or CI inspection was run.
Machine-check results belong to the authors' targeted builds and the
coordinator's final package audit; this review does not replace them.
