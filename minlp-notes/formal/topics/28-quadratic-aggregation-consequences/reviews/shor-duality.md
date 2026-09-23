# Independent semantic review of the Shor converse

Reviewer: the topic 28 source-inventory agent. Date: 2026-09-22.

Reviewed the final reported interfaces and proof bodies in
`ShorConeSeparation.lean` and `ShorDuality.lean`, together with their
`ShorModel.lean` and `ShorBlock.lean` definitions. No mathematical or
statement-fidelity defect was found in these files. Whole-package
completion, the assembled iff declaration, and machine-check results
remain the coordinator's separate obligations.

`exists_nonnegative_separator` separates an arbitrary nonempty convex
subset of real coordinate space from the open strict negative orthant.
It assumes neither closedness nor that the convex set contains the origin.
The nonnegative coordinates of the separator are derived by taking each
negative-orthant coordinate arbitrarily negative. Nonzero weights follow
from strict separation and nonemptiness. Approaching the origin inside
the orthant proves that the separator is nonnegative on the convex set.
These steps supply exactly the separation fact required by the application.

`System.strict_shor_alternative` applies this result to the actual affine
image `f(x)+(trace(A_i Y))_i` with `Y` PSD. Convexity follows from PSD convexity
and linearity of the trace; `Y=0` supplies a point in that image. The
separating aggregate is nonnegative at `Y=0`. Scaling `vv^T` by an explicit
nonnegative scalar rules out a negative quadratic value in any direction,
so symmetry of the aggregate yields PSD. Thus neither SDP dual attainment
nor closedness of a linear PSD image is being assumed.

`System.exists_strict_shor_slack` uses absence of a nontrivial certificate
to force the separating quadratic and linear aggregates to vanish.
Topic 27's strict-feasibility lemma then makes its constant strictly
negative, contradicting the nonnegative aggregate value at `x`. Its only
mathematical premises are nonempty strict feasibility and absence of a
certificate. No HHC, AHC, cone-closure, Slater-lift, or witness premise is
introduced. The conclusion is stronger than the source's required weak
Shor feasibility: every `x` has a PSD covariance slack with all residuals
strictly negative.

`System.shorProjection_eq_univ_of_no_certificate` passes from those strict
residuals to the actual weak Shor projection. The underlying definition
uses a covariance matrix; `System.mem_shorProjection_iff` proves its
equivalence to the standard `[1 x^T; x X]` PSD matrix and lifted affine
inequalities. `shorBlock_posSemidef_iff` is a Schur-complement theorem with
the invertible scalar block equal to one. It does not require an extra
symmetry premise on `X`: the PSD predicates supply symmetry themselves.

The trace pairing is `trace(A Y)`. For the symmetric matrices in these
interfaces this is the usual Frobenius pairing. `tracePair_outer` verifies
the quadratic evaluation identity, and `tracePair_nonneg` proves PSD
pairing nonnegativity by a matrix square factorization. Consequently the
covariance implementation preserves the source's lifted inequalities.

This proof replaces the source's closure/interior argument without
weakening Lemma 4. Documentation should describe that simplification and
should not list the unused source cone-closure identity as a separately
formalized theorem. No additional local Lean command was run for this
semantic review; author compilation reports and the coordinator's final
targeted audit must be recorded under verification rather than attributed
to this review.
