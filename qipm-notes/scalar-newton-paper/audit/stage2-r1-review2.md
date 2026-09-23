# Stage 2, round 1 — independent reviewer 2

Reviewed Sections `04-lower-bounds.tex` and `05-composition.tex`, the Stage 1 access model, `audit/stage2-author.md`, the Stage 2 source-map entries, and the diagnostic script. I did not consult other reviewers' reports. The manuscript was relocated from the repository root into `notes/scalar-newton-paper/` during this review; references below are relative to its new location.

## Findings

1. **Minor — state the default success and cost conventions for lower bounds.** The exponential theorem explicitly requires success probability 2/3, but the first assertion of `thm:statistical-lower`, `cor:coherent-counting`, `prop:contrast`, `thm:distributional-product`, and `thm:path-product` do not explicitly state their success requirement. Section 1 currently introduces a failure parameter but no default bounded-error convention. Their proofs establish the intended bounded-error statements, so this is not a mathematical counterexample. **Fix:** state once in the access-model section that lower bounds, unless otherwise specified, require success at least 2/3 on every promised input and charge worst-case query count; retain the explicit distributional expected-cost convention where used. The high-confidence theorem then overrides the default. It would also help to explicitly inherit the preceding theorem's kappa and epsilon range in the coherent counting corollary.

No major findings. I found no invalid result or proof gap in the statistical, oracle-simulation, composition, witness, or path calculations.

## Statistical and coherent lower bounds

- For the two-Hamming-sphere lemma, adaptive addresses do not affect the hypergeometric fresh-bit probabilities. Stopping before the observed one count reaches t/2 avoids the support singularities that otherwise invalidate a direct global KL argument. The stopping probabilities, per-query KL bound, Pinsker estimate, and restoration of the stopped suffix yield the claimed minimum of M and t M / Delta squared.
- In the large-population branch, the chosen floor and ceiling obey all lemma hypotheses, including at epsilon=1/128 and the population threshold. The scalar gap is at least 6 epsilon while the lower scalar is below two, so the relative intervals are disjoint. In the complementary branch, zero versus one marked input gives the stated linear-in-M lower bound.
- The high-confidence proof is valid for the explicit large-population regime. The two Bernoulli populations concentrate into separated relative-error scalar bands; adaptive bit queries have fresh Bernoulli laws; each KL contribution is O(epsilon squared / kappa). Binary data processing gives the logarithmic confidence factor. The stated population condition keeps the lower bound below the total input size.
- The sign-block form identity and its exact two-sparse square root are correct. The eigenvalues, row and column norms, Frobenius norm, and all squared-magnitude sample distributions are independent of the hidden signs. A queried value uses one hidden bit, including for the constraint factor.
- The coherent lower bound uses the standard two-weight consequence of Nayak–Wu in a population regime where its second term is Omega(sqrt(kappa)/epsilon). The common-eigenbasis success-ancilla construction has mean q/kappa, so relative amplitude estimation supplies the matching upper bound. Restricting the coherent oracle completion is necessary and is correctly done.

## Exponential lower bound and rational implementation

- Checked Montanaro–Shao Theorem 1.8 and Corollary 5.1 directly in the primary full-text extraction `/tmp/qipm-ms.txt`. The degree parameters, sparsity exponent, and denominator agree. The real orthogonal gauge proves that the diagonal data and transition magnitudes are public.
- Affine shifting and padding give the exact spectral promise. Polarization converts two relative estimates to the stated additive matrix-entry error. Hadamard supports, sign supports, diagonal masses, and global row/column norm samples are all simulable at constant hidden-query cost.
- The sparse factor is a block Cholesky factor with public scalar pivots; no hidden circuit product is needed. Its Gram matrix, barrier Hessian, analytic center, and objective-perturbation decrement have the claimed factors of two.
- The dyadic rounding, Perron monotonicity, tridiagonal norm bound, and resolvent stability leave adequate promise-gap slack. The rational 3/5, 4/5 polarization coefficient is 25a/48, with propagated error 25epsilon/24. The four-square block LDL construction gives an exactly rational sparse constraint factor. The text appropriately distinguishes computability from efficient public preparation and does not claim a uniform bit-complexity bound.

## Composition and explicit clocks

- Checked the fixed-inner-distribution statement against Ben-David–Blais Definitions 33–34, Theorems 24 and 35, and the full proof in `/tmp/qipm-bdb.txt`. The manuscript's quantifier order is supported: the hard pair of distributions is chosen for the inner function first, and the proof establishes the required lower bound for that pair.
- Independently checked Chakraborty et al. Theorem 2 and Observation 23 in the [primary published PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol275-approx-random2023/LIPIcs.APPROX-RANDOM.2023.63/LIPIcs.APPROX-RANDOM.2023.63.pdf), page 63:11. These permit a partial outer function and give the asserted noisy-query consequence when outer randomized complexity is linear in its arity.
- The conditional high-contrast compiler meets the two-sphere hypotheses for sufficiently small epsilon. The stated level-width restrictions are correct; no unjustified perfect-composition theorem is used.
- In the unconditional distributional product, n>=200 keeps the two outer Hamming spheres away from the endpoints. The Hoeffding exponent is correct: the threshold is one eighth of the scalar mean gap and the tail is below 0.004. The gap exceeds 14epsilon d, leaving room for concentration and relative estimator error. Median amplification and thresholding therefore produce the required composed decision algorithm.
- Re-derived the explicit Jacobi witness. The signed barycentric measure annihilates the claimed polynomial degrees; the added zero mass makes the second and penultimate orthogonal polynomials have matching diagonal spectral masses. Partial fractions give both S0 and S1 and hence the exact diagonal formula. The circuit-depth interpretation uses growing source width, not padding of a fixed source instance.
- Re-derived the constant-path determinant recurrence and cofactors. The endpoint coefficient, diagonal, signal ratio, kappa powers, admissible circuit lengths, and high-accuracy regime are consistent. Direct sums then yield the kappa-squared outer factor without claiming the full product of the main upper bound.
- The cyclic dilution, two-cluster obstruction, Schur-complement condition bound, and condition-budget endpoint maximization are valid under their stated assumptions. They are appropriately qualified as limitations of specific constructions.

## Diagnostics and presentation

`checks/check_lower_identities.py` passed under the qipm interpreter, checking 25 Jacobi realizations and 25 constant paths. I additionally checked the statistical floor/ceiling choices and disjoint relative-error intervals across representative condition, accuracy, and population thresholds. These diagnostics supplement the algebra above.

The stage carefully attributes the approximation, matrix-function hardness, counting, and composition engines. It does not claim that separately sharp factors imply a fully sharp joint complexity, and it distinguishes numerical quantum estimation from promise decision. I found no unsupported novelty assertion in these two sections.
