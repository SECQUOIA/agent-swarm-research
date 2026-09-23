# Stage 1 author audit

Written: models and classical algorithms, manuscript skeleton, source inventory, numerical diagnostics.

## Verified statements

- Relative Chebyshev residual degree is O(sqrt(kappa) log(1/epsilon)); no extra log(kappa) is needed for a relative positive quadratic form.
- The complex-coordinate estimator is unbiased; its second moment sums only over the support of the sampling vector. The manuscript preserves the inequality when zero coordinates exist.
- The Kantorovich bound follows from a scalar quadratic inequality and gives the required O(kappa) relative variance. Its sharp example only proves estimator-specific tightness.
- Median of means needs no a priori value of the unknown quadratic form. The full proof handles failure probability, deterministic bias, and spare constants for perturbation.
- The bilinear variance is energy-normalized, and relative bilinear error needs a noncancellation promise.
- The normal-equation residual identity works for nonnormal complex matrices. It gives relative vector error before sampling; no unjustified spectral-radius contraction is used.
- The rejection sampler's complete raw output law is written explicitly. Singular-value lower bounds make it terminate in finite expectation. Row and column sparsity are both required.
- The general inverse-overlap theorem retains the supplied solution-norm bound R_e and charges log(R_e/epsilon) in polynomial degree.

## Corrections and developments

The source upper note suggests guard precision polynomial in walk depth, log sparsity, log condition, and log accuracy in addition to input bits. This is not an adequate complete finite-precision theorem: evaluating a polynomial bounded on the interval does not control the later division by an arbitrarily small sampled b_i. The manuscript replaces that suggestion with a proved deterministic estimator-perturbation and total-variation sampling transfer proposition. Rational input implementation exists via finite local exact sums or certified refinement, but the paper does not infer a dimension-independent bit bound from ideal arithmetic.

The sampling complexity uses log(d+1), including diagonal sparsity d=1, so the exponent does not spuriously vanish. The K=1 boundary is handled separately as identity (SPD) or unitary (general).

No general 'tight joint frontier' is claimed from the upper bound alone. Necessary logarithmic/squared-logarithmic condition growth is proved; matching hard instances belong to later stages.

## Literature evidence and attribution

Read the repository literature instructions and the local Gharibian–Le Gall full text, including its sampling definitions and Theorem 1.3/4.1 context. The coordinate identity and exponential-in-degree local algorithm are attributed to prior work. Root independently checks the source metadata, which are erroneous for Gharibian–Le Gall in the local catalog, and owns the external literature review.

## Verification

`scripts/verify_classical.py` checks spectral residuals, complex expectations with zero coordinates, Kantorovich equality, full rejection output probabilities, and deterministic median perturbation. These are diagnostic examples, not substitutes for proofs.

## Remaining stage scope

Lower-bound parameter uniformity, all composition variants, coherent-query bounds, finite rational hard instances, and optimization/structured-cone transfers are routed in source-map.md. No theorem from those stages is currently assumed by the Stage 1 proofs. Five independent reviews are required before this stage is accepted.
