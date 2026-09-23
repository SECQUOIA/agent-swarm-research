# Stage 5A independent review 1

## Scope and conclusion

I personally read all four frozen Stage 5A sections (`11a` through `11d`),
the author record, and the earlier results used for dictionary rank,
selected rank, product certificates, tree parameters, column packing,
balance slices, and shared spectral barriers. I did not delegate, edit the
manuscript, or consult any other review.

**No major issue found. Two minor domain qualifications should be made
explicit.** Neither affects the substantive results or their proofs.

## Minor issues

1. **Require a positive compression parameter.** In
   `sections/11a-exposed-movement.tex:236–243`, the optional sharper
   gradient inequality permits `vartheta = 0` as written, whereas the
   following distance formula divides by its square root. This is an
   actual permitted edge case: take `L(x) = diag(1,x)`, `x > 0`, and
   compress to the first coordinate. The ambient Hessian is positive
   definite and the compression is constant. Require `vartheta > 0`
   when giving the ratio bound (and, for complete explicitness, specify
   `r >= 1` for the compression). Any positive bound works for a
   constant compression; the resulting lower bound is simply zero.

2. **State the accuracy range of the explicit central chord schedule.**
   In `sections/11c-concrete-movement.tex:260–271`, the expression
   `A(1-epsilon/k)` is used without stating `0 < epsilon <= k`, although
   `A` was defined only for `0 <= r < 1`. Add this accuracy condition to
   the sentence introducing the route. If desired, say that an accuracy
   target `epsilon >= k` is already met at the analytic center and needs
   no chords. The later application `epsilon <= k/4` is already within
   the correct range, so this is a local statement clarification.

## Substantive mathematical checks

### Weighted exposed minors and certificate quantifiers

- The fundamental identity with an idempotent gives
  `P(c) P(x) P(c) = P(P(c)x)`. Combining this with the inverse Hessian
  `P(x)` gives squared covector norm exactly `rank(c)` in the full
  Jordan metric, including the exceptional algebra. The proof does not
  rely on associative matrix multiplication.
- Scaling the block metric by `alpha_i` and its potential by `alpha_i`
  gives the squared norm `sum alpha_i q_i`. Affine restriction decreases
  the dual norm. No completion coordinate has been fixed silently.
- I independently optimized the weighted determinant product under
  `sum g_i <= epsilon`: the maximizing allocations are
  `g_i = epsilon alpha_i q_i / Q_alpha`. This recovers both the powers
  of `alpha_i` in the scale and the coefficient `sqrt(Q_alpha)`.
- The full-cone upper curve retains the transformed certificate and
  contracts only its positive-support eigenvalues; its metric length
  and objective gap have the claimed rates. No matching upper bound is
  inferred for an arbitrary affine slice.
- The product dictionary application uses precisely the high-rank
  aggregate whose existence was proved earlier. It does not reverse the
  certificate quantifiers or substitute a restricted barrier parameter
  for exposed rank. The fixed-instance qualifications on the scale are
  essential and are present.

### Affine PSD compression and profile asymptotics

- The Schur-complement proof of Hessian domination is valid over both
  stated fields. Negative log determinant is convex and order reversing;
  the Schur complement is matrix concave. QR reduction changes the
  compressed logarithm only by a constant.
- For the spectral profile, `R_m = Q D^(1/2) U_m` is injective and
  `R_m R_m^* <= W`. This verifies the endpoint trace inequality even
  though the chosen compression need not be orthogonal.
- I differentiated the geometric continuous maximum. Its maximizing
  scale is `2 Lambda/(3a) + O(log Lambda)` and the leading coefficient
  is `(2/3) sqrt(2/(3a))`, as printed.
- Stirling's formula gives the polynomial maximizing scale
  `exp((2-beta)/(beta-1)) epsilon^(-1/(beta-1))`; the bracket there is
  `2(beta-1)`. The error after multiplication by `sqrt(m)` is uniformly
  bounded. Integer rounding and the specified rank cutoffs preserve both
  asymptotics.
- The box-pencil upper paths stay in the feasible domain, since straight
  segments in the nonnegative transformed distance coordinates correspond
  to `0 < q_i <= 1`. The sum of positive logarithm squares has the stated
  orders. The manuscript appropriately claims matching orders only for
  these examples, not equality of constants or arbitrary pencils.

### Primal–dual geometry and activity distribution

- Differentiating `s = -F'(x)/eta` in `log eta` yields the stated
  orthogonal velocity decomposition. The conjugate Hessian scaling is
  `eta^2 H^(-1)`, so both the total speed and the signs of the objective
  derivatives are correct.
- The feasible gap-sublevel proof correctly uses affine feasibility only
  at the target and center. Its lower potential bound therefore remains
  valid along ambient product-interior curves. Its classical attribution
  is accurate.
- I checked the ray/nonray integer minimization for the dimension
  envelope, the arbitrary-coupling restriction argument, the scalar
  product-ball speed, the two threshold constants, and the head/tail
  inequalities. The unique-optimizer example explicitly varies its
  weights with accuracy, avoiding an incorrect fixed-instance claim.
- The dyadic visible-weight counts include the threshold endpoints and
  truncated finite list correctly. The pointwise Hessian counterexample
  has the asserted diagonal inverse entries and gradient norm, and is
  explicitly not claimed to integrate to a barrier.

### Concrete movement and weighted tree theorem

- Free packing completion variables are handled by determinant
  inequalities and the full restricted metric, rather than being fixed
  along competing paths. Heterogeneous entropy scales follow from
  sourcewise weighted AM–GM with the correct center determinants.
- Internal-axis stationarity gives `q_v / omega_v` constant. Telescoping
  then gives `W q + r^2 = 1`; differentiating central stationarity gives
  the printed speed. The exact scalar arc and its logarithmic leading
  term agree with direct differentiation.
- The tube estimate uses dual-norm transport in the correct direction.
  A single chord changes the gradient by at most `R/(1-R)` in the
  starting dual norm; summing transported changes gives the printed
  geometric factor. The terminal gap estimate uses the central gradient
  norm upper bound and `L_omega >= 1` legitimately.
- The balance-slice certificate has rank `rho-1`, scale
  `(rho-1)/rho`, and a central path satisfying every balance equation.
  The central metric integral and its additive upper remainder are
  correct. The shared spectral argument uses the appropriate direction
  of von Neumann's trace inequality and the reduced parameter `R_0`.
- For the new tree result I independently inverted the Lorentz Hessian:
  `H^(-1) = x x^T - (q/2) J`. Hence a null dual logarithm has squared
  covector norm one, whereas the determinant logarithm has squared norm
  two. This verifies the crucial half weight on inactive blocks.
- The active pairings telescope to the full objective gap. Every maximal
  inactive subtree begins in a coordinate perpendicular to the active
  parent's support direction; its axis squared is bounded by a fixed
  multiple of that gap. Positivity of all internal axes propagates the
  bound throughout the inactive subtree. This covers all inactive nodes,
  including ones arbitrarily far below an active node.
- The upper curve's subtree sums produce exactly its prescribed
  determinants and root value. Active blocks have squared speed
  `1 + O(h + lambda^(-2))`; inactive blocks are fixed interior vectors
  scaled by `sqrt(h)/lambda`, giving exactly
  `2(1/2 + 1/lambda)^2`. Thus the weighted sum is `K_c + O(1/lambda)`
  and integrates to the asserted remainder. A fixed interior segment
  connects any prescribed reference at finite cost.
- Summed potentials and synchronized upper curves prove the independent
  product version. Zero-objective independent factors can stay fixed;
  zero-objective subtrees of an active tree cannot. The manuscript keeps
  this important distinction. The central excess ratio and its
  discontinuity as objective support vanishes follow correctly.

## Literature, overlap, and presentation

I compared the actual companion formulation, distribution, and
primal–dual sections with the new manuscript. The overlapping exposed
minor theorem, dimension envelope, central calculations, and
distribution laws are attributed. The explicitly identified new tree
coefficient is stated for its fixed weighted barrier; it is not promoted
to an all-barrier or unrestricted-algorithm theorem.

I opened the primary Hauser–Guler text at
`https://arxiv.org/pdf/math/0103196` and checked Theorem 5.5, including
the coefficient threshold of one. I opened the primary Nesterov–Todd
text at `https://people.orie.cornell.edu/miketodd/NTRiemann.pdf` and
checked Theorem 5.1(c), Theorem 5.2, and the allowance for intermediate
affine infeasibility. I also read the local Boyd–Vandenberghe Example 3.4
supporting the matrix-fractional convexity attribution.

The four sections explain which metric, endpoint set, and algorithmic
restriction each conclusion uses. Beyond the two small domain
qualifications above, I found no unsupported novelty claim, missing
essential hypothesis, or proof gap in this stage.
