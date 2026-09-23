# Quadratic aggregation certificates

Status: complete within the scope below. All 12 frozen obligations have
Lean proofs and independent statement reviews. The targeted verification
passed warning-free builds of 11 modules, an axiom audit of 178 owned
declarations, and all 11 module kernel replays.

The target is Theorem 1, its three supporting lemmas, and its hidden
hyperplane convexity (HHC) specialization in the
[source note](../../../results/quadratic-aggregation-trivial-hull-certificate.md).
For a nonempty strict quadratic system with asymptotic hyperplane convexity,
the convex hull is proper exactly when some nonzero nonnegative aggregation
has a positive semidefinite quadratic part and a nonzero quadratic or linear
part. The certificate-to-proper-hull direction needs no hyperplane convexity.

- [Frozen claims](CLAIMS.md).
- [Independent source inventory](SOURCE-REVIEW.md).
- [Claim-to-declaration coverage](COVERAGE.md).
- [Independent review record](REVIEW.md).
- [Targeted verification and source fingerprints](VERIFICATION.md).

The proofs live in [Formal/QuadraticAggregation](../../Formal/QuadraticAggregation/).
The final [headline](../../Formal/QuadraticAggregation/Headline.lean) gives
`System.proper_hull_iff_certificate`, its source-sequence variant, and
`System.proper_hull_iff_certificate_of_hhc`. They take the original
coefficients and stated hypotheses. Hyperplane certificates, coefficient-cone
closedness, and a nonzero PSD limit are all proved, not supplied as premises.

The proof uses strict feasibility to bound the constant term before
normalizing the quadratic and linear coefficients. One compact subsequence
then yields a nonzero PSD aggregate. This avoids the source's eigenvalue
estimates; Lemma 3's uniform cone separation is also proved independently.

The certificate is an existence result. It does not assert that globally
convex aggregations recover the entire hull or every valid linear inequality.
The source note's corollaries, SDP interpretation, stable-convexity hypotheses,
and counterexamples remain separate mathematical claims unless explicitly
included in a later scope extension.

[Topic 28](../28-quadratic-aggregation-consequences/README.md) now verifies
Corollaries 1, 3 and 4, Lemma 4, and the two recommended boundary examples.
That separate extension leaves this core package's frozen scope and
verification history unchanged.

The related paper has a contributed
[formal-verification section](../../../paper-quadratic-aggregation/sections/90-formal-verification.tex)
with the precise theorem, simplified proof, and scope boundaries. The
[standalone supplement](../../../paper-quadratic-aggregation/FORMAL-VERIFICATION.md)
builds it independently while the manuscript's separate staged review
defers its inclusion in the main draft. The paper's
[development stages](../../../paper-quadratic-aggregation/PROCESS.md)
remain separate from this package's completion.

Topic 27 records the user's choice of the newly recommended topic. The
existing identifiers 22–26 and their queued scopes are preserved. Only
targeted checks for this package are run locally; CI results are not inferred.
