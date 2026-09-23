# Independent review: spectral criteria and singular costs

Reviewed `Determinant`, `Inverse`, `Pseudoinverse`, `CriteriaBasic`,
`CriteriaEigen`, `Criteria`, `CriteriaCost`, and `PseudoinverseOrder`. The reviewer did not implement
these modules. Existing theorem statements and proofs passed mathematical
review. The follow-up review closes the weighted-contrast, full ambient
pseudoinverse, and cover-reuse obligations identified in the initial review.

`IsRelativeCover` asserts that representatives are feasible and that every
feasible object has a representative satisfying both matrix inequalities.
The representative may depend on the feasible object. Finite maximization or
minimization subsequently supplies one criterion-specific optimum on the
representative set and compares it against every feasible object. The proof
does not incorrectly interchange these quantifiers or assume that one path
simultaneously optimizes different criteria. Nonempty-feasible hypotheses
provide actual representatives; the empty equivalence is proved separately.

The homogeneous criterion interface requires nonnegativity, PSD monotonicity,
and homogeneity, with positive degree. It does not assume concavity. Its finite
maximizer theorem is mathematical existence, not an arbitrary-function
comparison oracle or a complexity theorem. The lower scale is nonnegative
under its stated `eta<=1` hypothesis.

Determinant monotonicity handles a singular smaller matrix by its zero
determinant and nonnegativity of the larger determinant. In the nonsingular
case, congruence by an inverse factor reduces the comparison to eigenvalues
at least one. No inverse of a singular matrix is used in that branch. Scaling
and Bernoulli's inequality give the exact determinant and D-optimality factors;
the determinant-root theorem assumes positive dimension. Singular/all-zero
optima are handled without dividing by the optimum or taking its logarithm.
Exact rational determinant comparison is a separate computational obligation.

The E criterion is the minimum of the actual Hermitian eigenvalue list, not
a surrogate or a supplied monotone function. Its scalar-identity Loewner
characterization proves monotonicity and positive homogeneity. The zero scalar
case is handled separately. The minimum is attained, is nonnegative for PSD
matrices, and equals zero exactly when a PSD matrix is singular. Positive input
dimension is explicit for a minimum over eigenvalues. These results establish
the mathematical E guarantee; exact algebraic comparison and its bit work are
separate obligations.

Inverse order is proved for positive definite matrices using a quadratic
completion and actual inverse identities. The relative sandwich itself
transfers positive definiteness. The trace bound uses nonnegative PSD diagonal
entries. `inverseTraceCost` assigns infinity to non-positive-definite matrices,
so singular information is not misrepresented by Mathlib's totalized matrix
inverse. The finite minimization theorem uses extended nonnegative reals and
the strictly positive approximation factor. The substitution
`eta=eps/(1+eps)` gives exactly `1+eps` for every nonnegative `eps`. Existence
of a positive-definite feasible object is preserved by the cover.

The spectral pseudoinverse reciprocates nonzero eigenvalues and leaves zero
ones zero. The code proves all four Moore–Penrose equations. Estimability is
actual membership in the matrix range. Kernel equality from the two-sided PSD
sandwich is used to prove equivalent estimability; the proof does not assume
inverse monotonicity for matrices with different kernels. On each estimable
contrast the quadratic-completion argument gives both inverse factors. Zero
contrast and zero variance require no division by the contrast variance.
`contrastCost` assigns infinity to non-estimable contrasts and preserves actual
finite-cost existence in the cover.

The follow-up review checked `RelativeSandwich.pseudoInverse` in
`PseudoinverseOrder`. For an arbitrary ambient vector, the proof projects onto
the actual matrix range using `A * A⁺`. The removed component lies in the
kernel of both matrices, and both pseudoinverses annihilate it. Applying the
estimable-contrast inequalities to that projection proves the full ambient
Loewner sandwich. It does not assume that every ambient vector is estimable.

`weightedContrastCost` uses a finite sum with nonnegative weights in extended
nonnegative reals. The sandwich bound distributes over the sum, including the
standard `0 * infinity = 0` convention for a zero-weight non-estimable contrast.
`weightedContrast_minimum_eps` chooses an actual representative minimum and
obtains the exact `1+eps` factor. No division by a positive optimum is needed.

The `IsRelativeCover.congruence` and `IsRelativeCover.add_prior` wrappers in
`CriteriaBasic` use the same feasible and representative sets. Their proofs
reuse the same representative selected for each target and apply the pairwise
PSD transformation lemmas. They do not recompute the path set.

O02/O03/O04 computational comparison and bit-complexity claims are outside
this semantic review. In particular, finite real maximization is not an
implementation of exact E comparison. The same distinction applies to the
rational implementation of weighted contrast evaluation.

Targeted checks run from `formal/`, with `~/.elan/bin` on `PATH`:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.DAGSpectral.Determinant Formal.DAGSpectral.Inverse Formal.DAGSpectral.Pseudoinverse Formal.DAGSpectral.CriteriaBasic Formal.DAGSpectral.CriteriaEigen Formal.DAGSpectral.Criteria Formal.DAGSpectral.CriteriaCost
LEAN_NUM_THREADS=1 lake env lean topics/21-dag-spectral/verification/CriteriaReview.lean
```

Both passed. The second command inspected nine principal declarations and
reported only `propext`, `Classical.choice`, and `Quot.sound`. Its exact input
is preserved as `verification/CriteriaReview.lean`. This sampled dependency
audit is not the final whole-topic axiom audit or kernel replay. No
project-wide verification or CI inspection was run.

Follow-up targeted checks:

```text
LEAN_NUM_THREADS=1 lake build --wfail Formal.DAGSpectral.PseudoinverseOrder Formal.DAGSpectral.CriteriaBasic Formal.DAGSpectral.CriteriaCost
LEAN_NUM_THREADS=1 lake env lean topics/21-dag-spectral/verification/CriteriaReview.lean
```

Both follow-up commands passed. The preserved axiom audit now samples thirteen
declarations, including the ambient pseudoinverse, weighted-contrast minimum,
congruence and prior-addition wrappers. Every sampled declaration reports only
`propext`, `Classical.choice`, and `Quot.sound`.
