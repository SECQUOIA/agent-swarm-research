# Independent mathematical referee report: algorithms and gap-zero separation

Reviewed `sections/05-algorithms.tex` and `sections/06-gap-zero.tex`, with the shared definitions in `sections/02-preliminaries.tex` and `macros.tex`. Review was analytical. No computational experiments, project-wide checks, CI inspection, or literature searches were performed. The quoted primary-source exact-CVP time bound was treated as separately verified, as requested.

## Verdict

No theorem-threatening mathematical error was found. The short-certificate arguments, rational lattice quotient, fixed-rank reduction, normalized-threshold enumeration, rank-one formulas, restricted-direction reduction, and gap-zero construction are sound. The three formulation corrections and one encoding clarification below were communicated to the authors and have all been applied. No unresolved mathematical objection remains from this review.

## Corrections requested

All four items in this subsection are resolved in the revised sources.

1. **Minor, but important for mathematical accuracy: rational Gram factors.** `05-algorithms.tex`, opening paragraph, currently says that a rational positive semidefinite matrix “need not have a rational Gram factor.” The subsequent proof correctly constructs a rectangular rational factor. The intended statement must specify a factor **with a number of rows equal to its rank**, or a factor **in its intrinsic dimension**. A rational matrix such as `[3]` has no one-row rational Gram factor, but does have a three-row rational factor. The present opening sentence, without the dimensional qualification, conflicts with the valid sum-of-squares construction later in the section.

2. **Minor formulation ambiguity: existential restricted separation.** In `prop:restricted-rank-one-hardness`, replace “deciding whether a split vector ... is violated” by “deciding whether there exists a violated split vector ...”. Evaluating a supplied split vector is polynomial. The proof establishes the stated existential decision problem, not difficult evaluation of a supplied vector.

3. **Minor terminology inconsistency: arbitrary input distance vectors.** The opening paragraph and `thm:gap-zero-hardness` in `06-gap-zero.tex` refer to a “rational cut vector.” Section 02 has already defined a cut vector as a particular `0/1` cut incidence vector, which satisfies every valid gap inequality. Use “rational distance vector” or “rational point in the cut-coordinate space” for the arbitrary input. This is a wording correction; the constructed rational inputs and reduction are correct.

4. **Optional encoding clarification.** In the paragraph following `thm:gap-zero-hardness`, specify that the construction has polynomial encoding length **in the source instance and the prescribed rational epsilon**. Taking the minimum of the original positive nu and epsilon has this encoding bound. The spectral distance to the positive semidefinite cone is in fact exactly nu, because the matrix has one negative eigenvalue equal to minus nu.

## Verification details

### Rational elimination and certificates

- The zero-diagonal/off-diagonal negative direction has value exactly `-1`: the choice of its first coordinate cancels the remaining diagonal term. Positive-pivot Schur-complement lifting preserves quadratic value.
- Schur-complement entries and the lifted negative direction have polynomial bit length by determinant bounds after clearing denominators. The selected positive pivots define a positive definite principal submatrix of order equal to rank in the positive semidefinite case.
- For the quotient, `A = P^T G P` follows from the zero Schur complement. Clearing denominators before column Hermite normal form gives a full-rank integer lattice. Computing preimages of basis columns and solving a feasible integral system give polynomial-size lifts; no integer inequality constraints are being imposed.
- A hypermetric violator in the positive semidefinite/range case lies in the open ball of radius `||t||_G` about `t`, hence has norm less than `2||t||_G`. Its coordinates have exponential magnitude bounds with polynomial bit length, and denominators dividing a fixed common denominator of `P`. The preimage obtained by integer linear algebra preserves the exact value of the objective.
- The non-positive-semidefinite and out-of-range cases both give immediate polynomial-size hypermetric witnesses by sign selection. No extra large scaling multiplier is necessary.
- The split certificate uses the correct parity coset. A bounded image `P(e_0+2v)` is lifted by the feasible system `2Pv' = y-Pe_0`, so parity is preserved rather than discarded by quotienting.

### Fixed-rank separation

- The hypermetric problem is exactly closest vector to `delta_K/2` in `P Z^m` under the rational metric `G`, with a strict radius comparison.
- The split problem is exactly closest vector to `-Pe_0/2` with squared threshold `1/4`. No parity restriction remains on the coefficient vector `v`; parity was absorbed by the affine target.
- The rational Euclidean embedding is valid: each positive rational `p/q` is a sum of rational squares obtained from the binary expansion of `pq`. An odd-position bit becomes two equal integer squares and an even-position bit one integer square; dividing their integer roots by `q` gives the required rational squares. Rational LDL factorization then gives a rectangular rational matrix with the desired Gram matrix, with polynomial size.
- The embedding adds ambient coordinates but not lattice generators. The lattice has rank `r`; inner products and projections can be computed from its `r`-by-`r` rational Gram matrix. Thus the separately verified rank-dimensional CVP bound applies without placing the larger ambient dimension in the exponential term.
- A closest lattice point has norm at most twice the target norm because zero is feasible. Its rational quotient coordinates and its integer basis coordinates therefore have polynomial encoding length. The returned point can be lifted with `T` without increasing the bit length beyond a polynomial.
- The support corollary correctly applies rank separation to induced vertex sets, allowing a new root inside each support. This avoids unsupported facet-coefficient bounds. Split support includes the moment root separately. Gonality enumeration is finite and the text correctly distinguishes fixed-parameter polynomiality from an FPT claim.

### Thresholds and rank-one examples

- The best-offset identity is exact, including integer fractional part zero. Positive semidefiniteness implies the universal raw upper bound `1/4`.
- The strict threshold condition is `||w||^2 < 1/(4 rho)`. The largest allowed integer squared norm is exactly `ceil(1/(4 rho))-1`, including the equality boundary. The finite enumeration and XP running-time claim are correct.
- The added `prop:raw-quarter` is valid. For rational input, parity-coset quadratic values form a nonempty subset of a discrete nonnegative rational grid, so the minimum is attained. Equality of the raw violation to `1/4` is equivalent to a zero image in the positive semidefinite form, and the integer system preserves the parity coset exactly. Integer linear algebra decides it in polynomial time.
- The added `lem:primitive-split-domination` is valid. Direct coefficient matching gives `a+b=k^2` and the correct linear coefficient; the remaining constant is exactly the stated consecutive-integer product. The floor definition gives `0<=b<k^2`, and negation followed by normalization gives the convex-combination domination precisely under `Y_{00}>=0`. Primitive directions therefore suffice for detecting a violation and for the normalized objective. No claim about maximizing the raw objective over primitive directions is made.
- A rational rank-one matrix with root entry one is necessarily the stated outer product. The least common denominator makes the integer vector `p` primitive; Bezout therefore permits every integer scalar product. The raw maximum and polynomial-size maximizer follow.
- The example with `x=1-1/D` gives the displayed raw and normalized violations. For `D>=4`, the larger raw violation has a strictly smaller normalized value than the elementary direction.
- All four cases of the restricted `0/1` SUBSET SUM reduction have the stated strict bounds. The construction is for general moments, not Boolean-diagonal moments, and the text correctly limits its hardness claim.

### Gap-zero separation

This portion was also independently checked by a second focused mathematical referee.

- The basis `e_i-s_i s_n e_n` spans the signed hyperplane exactly. Non-positive-semidefiniteness on that rational restriction gives a polynomial-size integer zero-gap witness.
- Padding by zeros correctly converts ordinary PARTITION to its balanced-cardinality version. Adding the large common shift `K` prevents cancellation between a nonzero cardinality imbalance and the original weighted sum.
- The edge weights have degree exactly `rho_i`. They are strictly positive and bounded below by `theta_*`. Consequently the constructed matrix has unit diagonal and maps `a` to `-nu a`.
- The weighted-to-unweighted variance comparison gives the claimed lower bound on `a`'s orthogonal complement. Symmetry then gives exactly one negative eigenvalue.
- The signed-hyperplane converse gives `|s^T a| < 1` with the precise chosen constant. Integer-valuedness forces zero, so no extra gap-zero violator can appear in a no instance.
- Every fractional metric bound checks. In particular, the final scalar inequality factors as `(n-6)(13n-11) >= 0`. The coordinates lie strictly between `1/2` and `127/200`, which implies all strict triangle and perimeter inequalities.
- Decreasing positive nu preserves the weight, metric, and converse estimates. The matrix remains non-positive-semidefinite with precisely one negative eigenvalue and can be made arbitrarily close to the positive semidefinite cone.
- The concluding scope limitation is correct: non-positive-semidefinite inputs trivially violate some unrestricted gap inequality, whereas the positive semidefinite all-gap problem is not settled by the reductions in this paper.

## Targeted commands run

Only source reads and line-number searches were used: `cat AGENTS.md`, `cat paper-binary-separation/macros.tex`, `sed`/`nl` reads of sections 02, 05 and 06, and a targeted `rg` over the abstract, introduction and discussion for algorithmic claims. No numerical result was rerun.

## Follow-up: raw approximation and lattice-basis notation

The added `cor:raw-approximation` is mathematically sound. The complete split classification in `thm:relaxation-hardness` makes the attained raw optimum exactly zero in a no instance and exactly `1/(2N)` in a yes instance. The zero optimum is legitimate because the zero split vector has zero slack and every other slack is nonnegative in a no instance.

- A two-sided multiplicative guarantee with any finite factor forces the reported value to be exactly zero when the optimum is zero, and strictly positive when it is positive. Exact rational output therefore decides the source instance by its sign. No bound on the finite factor is needed for this implication.
- An absolute error **strictly** smaller than `1/(4N)` puts a no-instance report strictly below `1/(4N)` and a yes-instance report strictly above it. The strict inequality is necessary: an error bound with equality allowed could give the same midpoint in both cases. The requested tolerance has polynomial encoding length, as does the reduced input.
- The corollary concerns the raw value and a tolerance depending on the reduction. It correctly makes no claim about fixed additive tolerances or normalized-threshold approximation.

The replacement of the lattice-basis name `W` by `R_Lambda` is consistent throughout Section 05. The basis relation, lattice representation, Gram matrix and target coordinates now read respectively `R_Lambda=PT`, `Lambda=R_Lambda Z^r`, `F=R_Lambda^T G R_Lambda`, and `xi=R_Lambda^{-1}t`. The lifts by `T` remain correct, and no stale lattice-basis use of `W` remains. The change also avoids confusion with the vertex set `W` in the preliminaries.

This follow-up used only targeted `sed` and `rg` reads of Sections 03 and 05. No computational experiment or literature search was performed. No further correction is requested.
