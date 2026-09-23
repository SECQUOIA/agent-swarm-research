# Stage 5A independent review 2

## Scope and verdict

I personally read all four new sections, `11a-exposed-movement.tex`,
`11b-primal-dual-movement.tex`, `11c-concrete-movement.tex`, and
`11d-tree-distance.tex`, and the stage author record. I checked the relevant
norm-tree, grouped/packed barrier, balance-slice, and shared-spectral
dependencies in Sections 7 and 9, the companion's actual formulation
section, the Stage 5A source dispositions, and the principal primary
literature cited below. I did not delegate this review, read other review
reports, edit the manuscript, or run a shared build.

**No major or minor issue requiring correction was found.** This verdict
concerns the frozen Stage 5A material and its stated contracts; it does not
replace the later whole-manuscript review.

## Independent verification of the weighted tree theorem

I rederived the principal new theorem rather than relying on the author
record's verification.

1. For `f=-log(x^T J x)`, direct multiplication gives
   `H_f^{-1}=xx^T-(q/2)J`. A nonzero null dual vector therefore gives
   squared dual norm exactly one for `d log(s^T x)`. The determinant
   logarithm has squared dual norm two. Scaling the metric by `omega`
   and its active potential by `omega`, or its inactive potential by
   `omega/2`, gives precisely `omega` and `omega/2`, respectively.
   There is no missing Jordan-trace normalization factor.
2. The support vectors are genuine nonnegative Lorentz duals. Their
   pairings telescope to the entire objective gap even when internal
   support norms vanish. Inactive nodes are complete descendant subtrees.
   For a maximal inactive subtree, its child-axis coordinate is perpendicular
   to the active parent's normalized support direction. The displayed
   perpendicular-component inequality consequently gives
   `t_child^2 <= 2 gap/alpha_parent`. Positivity of all axes propagates
   this bound down the subtree, and `q_z <= t_z^2` completes the needed
   estimate. Finiteness of the fixed tree makes its constant finite.
3. The resulting potential has ambient squared dual norm `K_c`; affine
   restriction can only decrease that norm. Every target of gap at most
   epsilon increases this potential by at least
   `K_c log(1/epsilon)-O(1)`. Thus the lower bound concerns all endpoints
   and all feasible completion paths, rather than a particular route.
4. In the proposed upper curve, recursively subtracting child-axis
   squares leaves exactly the prescribed `q_v`; at the root the sum
   of all determinants is `A h+Z h/lambda^2`, so the root really is one.
   Every positive square root is on the correct Lorentz sheet. The root
   is active, hence `A>=1`, and the objective gap is asymptotic to `A h/2`.
5. Differentiating `q=x^T Jx` gives the displayed metric-speed identity.
   Active axial and supported leaf derivatives are `O(h)`, while inactive
   child derivatives are `O(sqrt(h)/lambda)`. Active blocks therefore
   have squared speed `1+O(h+lambda^{-2})`. Each inactive block is a
   fixed interior vector times `sqrt(h)/lambda`, so its exact squared
   speed is `2(1/2+1/lambda)^2`. Weighting and summing gives
   `K_c+O(1/lambda)`. Its square root integrates to
   `sqrt(K_c) lambda+O(log lambda)`; connecting the starting reference
   by a fixed interior segment costs only a fixed finite length.
6. The weighted central path has `q_v/omega_v` constant and speed tending
   to `sqrt(W)`. Its exact scalar arc shows an `O(1)` remainder in gap
   coordinates. Hence the ratio and its equality condition are correct.
   For independent products, the combined lower potential and synchronized
   upper curves both add squared coefficients. Fixed positive objective
   weights change constants only; wholly zero-weight independent factors
   may stay at the reference. The statement correctly distinguishes this
   from an inactive subtree inside a positively weighted tree.

As a secondary arithmetic check, I evaluated the analytic speed formula
using Python's standard-library Decimal arithmetic at 80-digit precision
for a three-node unbalanced tree with barrier weights `(1.3,4.2,2.7)`.
Objectives supported on its root leaf, middle leaf, and deepest leaf give
`K_c=4.75,6.85,8.2`, respectively. Evaluations at increasing lambda
converged to those squared speeds. This is supporting arithmetic only;
the preceding argument supplies the proof. No packages were installed.

## Checks of the other sections

- **Exposed-minor movement:** the Peirce quadratic-representation identity
  gives the claimed constant for every Jordan family, including Albert.
  Weighted AM--GM gives the stated powers of `alpha_i` in the reference
  scale. Restriction and inactive completions do not invalidate the
  covector argument. The full-cone upper construction transforms the
  certificate together with the reference. The dictionary consequences
  retain the required certificate and the distinction between generic,
  existential aggregate, and selected smooth ranks.
- **Affine pencils:** Schur-complement concavity proves convexity of the
  difference of the two negative log determinants. QR changes a compressed
  determinant by a constant only. The exposure-profile compression is
  positive and its trace is bounded by the full exposed trace. Independent
  maximization reproduces the geometric constant
  `(2/3)sqrt(2/(3a))` and the polynomial optimizer
  `exp((2-beta)/(beta-1)) epsilon^{-1/(beta-1)}`. The growing-rank
  assumptions and the specially constructed matching-order boxes are
  explicitly separated from arbitrary-pencils and fixed-rank assertions.
- **Primal--dual geometry:** differentiating central stationarity gives
  the stated orthogonal velocity allocation and objective derivatives.
  The barrier-height argument on the feasible gap sublevel has the
  correct `sqrt(nu/2)` constant even when intermediate paths are not
  affine feasible. The integer dimension charge includes rays and
  arbitrary coupled barriers. I checked the scalar Q1/Q2 constants,
  head/tail bounds, geometric-weight arc order, and fixed-instance caveat.
  None asserts a parameter-only primal or unrestricted-query lower bound.
- **Concrete formulations:** free PSD completion variables are retained
  in both stationarity and Hadamard's endpoint bound. The barrier-height
  and determinant-vector inequalities have the correct normalizations.
  Weighted tree stationarity and the scalar arc primitive agree on
  differentiation. Entropy scales account for the reference residuals.
  For the tube estimate, transporting each chord's gradient change and
  the endpoint residual gives the stated geometric sum, and the objective
  error in the tube yields the stated terminal-parameter lower bound.
- **Deferred movement applications:** on the balance slice the proposed
  frame-diagonal path satisfies the full affine stationary equations,
  including the balance normal, and its trace relation gives the claimed
  gap integral. For shared spectral cones, von Neumann's inequality has
  the required direction, AM--GM bounds the determinant product, and
  the reduced barrier has exactly the referenced parameter. Grouping and
  the fixed-identity block-star realization preserve that same function,
  which is what permits the movement conclusion.

## Literature and coverage

I opened the primary Nesterov--Todd paper at
<https://people.orie.cornell.edu/miketodd/NTRiemann.pdf>, including
Theorem 5.1(c), Theorem 5.2, and the following discussion. The manuscript
correctly treats feasible-gap minimization and product-metric geometry
as classical results. I also checked Theorem 5.5 of Hauser--Guler at
<https://arxiv.org/pdf/math/0103196>; its irreducible-factor coefficients
are indeed at least one.

Reading the companion's actual formulation section confirms the substantial
overlap in exposed-minor movement, dimension-only charges, grouped and
packed movement, uniform tree bounds, and exact unweighted central paths.
The new sections explicitly attribute those results and give standalone
proofs. The precise weighted active/inactive distance coefficient is
distinguished from that overlap, while its final paragraph does not claim
an exhaustive priority classification or optimality over all barriers.
The Stage 5A source dispositions account for the movement developments and
identify the integer-resource, query, and compiler material deferred to
later stages; I found no omitted movement result requiring a correction
to this stage.
