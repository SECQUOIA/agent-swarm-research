# Stage 2, round 1, independent review 5

Verdict: **no major findings; three minor corrections**.

I reviewed every statement and proof in `sections/04-lower-bounds.tex` and
`sections/05-composition.tex`, their Stage 1 access contracts, the Stage 2
author record, the active source notes, and the primary composition and
matrix-function sources identified below. I did not read any other review
report and did not edit the manuscript. The paper moved under `notes/`
during this review; the source line numbers below are unchanged.

## Numbered findings

1. **Minor — the advertised harmless rational sparsity loss has a degenerate
   boundary.** `04-lower-bounds.tex:166–169` and `:200–201` replace the base
   `(s-1)/2` by `(s-1)/8` while allowing `s=9`. At that boundary the new base
   is one, so the displayed rational-instance lower bound loses all its
   exponential dependence. The inequality remains true but does not justify
   describing the replacement as harmless on the entire stated range.
   The actual construction already repairs this: the largest admissible
   power-of-four gate has size at least both four and `(s-1)/8`. Use
   `max{4,(s-1)/8}`, or retain the original base while changing its absolute
   exponent constant. No new construction is needed.

2. **Minor — state the constant-success convention explicitly.**
   `04-lower-bounds.tex:1–7` does not establish a general success convention,
   while the statistical theorem at `:298`, coherent counting corollary at
   `:364`, conditional compiler at `05-composition.tex:36`, distributional
   theorem at `:99`, and path theorem at `:318` do not specify their default
   success probability. Their proofs use bounded error, with amplification
   from a fixed constant such as two thirds. Add a global sentence that every
   lower bound requires success at least two thirds on every promised input
   unless a different failure probability is displayed. This also prevents
   reading the bounds as uniform for success probabilities approaching one
   half, which the proofs do not establish.

3. **Minor — make the rational generator's coefficient test normalized.**
   `04-lower-bounds.tex:232–237` says to test an endpoint inverse coefficient
   against `9 tau/10`, then describes it as an entry of `(mI+h Jhat)^{-1}`.
   The coefficient whose lower bound is needed is
   `a [(mI+h Jhat)^{-1}]_{ij}`, namely an entry of `f_kappa(Jhat)`, not the
   unnormalized inverse entry. Write this exact test explicitly, and specify
   the second/penultimate indices in the even branch. Otherwise a literal
   implementation of the stated search can accept a clock with normalized
   signal smaller by a factor of kappa. The rounded witness already passes
   the correct test with slack, so the terminating-generator result and all
   substantive lower bounds survive this local correction.

## Checks on the lower-bound reductions

- The normalized reciprocal minimax formula is algebraically consistent
  with the cited reciprocal error, including degree zero. Its uniform
  degree range needs only the stated sufficiently small absolute accuracy.
- The Montanaro–Shao theorem has the degree parameters, exponent, and
  denominator reproduced in the manuscript. Its weighted-clock construction
  supports the real-sign/orthogonal-gate oracle simulation used here.
- Polarization introduces error at most epsilon for unit support-two right
  sides, and at most `25 epsilon/24` for the rational 3/5, 4/5 right sides.
  Constant amplification permits two calls to the single-form routine.
- Row and column norms and all magnitude sampling laws are public because
  clock transition supports lie in different clock blocks. Appending public
  scalar pads enforces exact condition number without revealing hidden data.
- The block bidiagonal factor has `BB^T=H`, and taking `C=B^T` is the correct
  orientation. The paired interval barrier has Hessian `2H` and the claimed
  squared decrement. No history-state product of hidden gates is exposed by
  the sparse factor oracle.
- Dyadic rounding preserves contraction, has the stated operator error, and
  retains sufficient Forrelation gap. The rational LDL/four-square factor
  preserves its Gram matrix and sparse, sign-independent metadata. The
  explicit refusal to claim efficient public preprocessing is necessary.
- The stopped hypergeometric argument avoids divergent KL terms near an
  exhausted Hamming weight. Its stopping probability and divergence bounds
  support the finite-population minimum. The zero/one regime covers small
  populations, and the Bernoulli-product argument has the right separate
  population requirement for confidence amplification.
- The sign-block identity is exact, and its canonical coherent reduction
  permits the approximate-counting lower bound. The amplitude-estimation
  upper bound has the correct square-root dependence on the smallest success
  probability. It is not a general sparse inverse-form upper bound.

## Checks on composition and explicit clocks

- The conditional compiler obtains linear outer query complexity in its
  actual parameter range. It uses a theorem valid for partial outer and inner
  functions, and states the narrow-level conditions needed beyond exact
  levels.
- The fixed pair of inner hard distributions used in the distributional
  theorem is supported by the proof of Ben-David–Blais Theorem 35, not merely
  by its worst-case conclusion. The order of quantifiers, conditional
  independence, and subsequent outer hard distribution are correct.
- With `n>=200`, the two outer Hamming weights remain a fixed distance from
  both endpoints. Their separation is a constant times the square root of
  the population, so their randomized and noisy complexities are linear.
  The Hoeffding exponent, scalar separation, and amplified estimation error
  leave the claimed constant margin. No unproved pointwise two-level promise
  is used.
- The restricted-interval dual witness really annihilates the needed full
  domain polynomials. The positive spectral measure has the stated total
  mass and its second and penultimate orthogonal polynomials produce the
  claimed cross and diagonal entries. I checked the partial-fraction and
  derivative identities giving the diagonal, including their signs.
- The path determinant, cofactors, endpoint diagonal, and contrast formulas
  agree. Its three groups of Hadamard layers use increasing source width,
  and thus increasing genuine source hardness rather than padding. The
  maximum admissible length has the stated high-accuracy scale. The outer
  block count is of order kappa squared.
- Cyclic dilution uses normality correctly. The two-cluster identity and
  Schur-complement condition bound are valid under their stated hypotheses.
  The final scalar optimization is an endpoint maximum by convexity. These
  are expressly construction-specific obstructions, not universal no-go
  theorems.
- The final lower envelope is a maximum over parameter-selected dimensions.
  Nothing in the present proofs justifies multiplying the entire statistical
  factor by the entire accuracy-dependent exponential, and the manuscript
  correctly declines that claim.

## Primary-source checks and novelty boundary

I independently inspected the primary Montanaro–Shao PDF extraction at
`/tmp/qipm-ms.txt`, Theorem 1.8, Corollary 5.1, and Section 5.1. Its theorem
statement and gate construction support the quoted engine. Existing
matrix-function hardness is appropriately credited; the manuscript supplies
the additional positive-form and full-SQ/LP reductions explicitly.

I also checked [Ben-David–Blais, version 2](https://arxiv.org/html/2002.10809v2),
Definitions 33–34 and the proof of Theorem 35, including its fixed inner hard
pair, together with Theorem 24. The asserted product-distribution consequence
is supported. [Chakraborty et al.'s published paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol275-approx-random2023/LIPIcs.APPROX-RANDOM.2023.63/LIPIcs.APPROX-RANDOM.2023.63.pdf)
expressly permits partial functions in Theorem 2 and gives the quoted noisy
complexity inequality in Observation 23. No unsupported new general
composition theorem is being claimed.

The delivered text does not assert first priority for the approximation,
Forrelation, composition, or counting ingredients. Final novelty positioning
must continue to distinguish those ingredients from the paper's specific
access-model reductions and explicit contrast calculations.

## Numerical diagnostics

The supplied `checks/check_lower_identities.py` passed using the qipm
interpreter: 25 witness Jacobi realizations and 25 constant paths.

I additionally wrote and ran an independent in-memory calculation with random
positive path weights and alternating public Hadamard/hidden diagonal-sign
gates, checking the factor orientation, every lifted row-norm formula, and
the exact sign-block quadratic-form identity over several conditions and
dimensions. All passed. These are finite diagnostics; the proofs above are
the basis of the correctness assessment.
