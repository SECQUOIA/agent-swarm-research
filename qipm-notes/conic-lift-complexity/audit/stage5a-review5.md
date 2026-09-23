# Independent Stage 5A review 5

Reviewer: `/root/stage5a_review5`.

## Scope and verdict

I personally read all of `11a-exposed-movement.tex`,
`11b-primal-dual-movement.tex`, `11c-concrete-movement.tex`, and
`11d-tree-distance.tex`, together with `audit/stage5a-author.md`. I did not
read another formal review, delegate this review, edit the manuscript, or
run a shared build. I checked the relevant balance-slice, matrix-packing,
shared-spectral, and rank/metric dependencies and compared the original
principal-minor and norm-tree workbench notes and the companion's
formulation, primal--dual, and distribution sections.

**No major issue found. One minor correction is required.** The new
weighted active/inactive tree coefficient is supported by the proof as
written; the restriction to the specified metric and fixed objective is
essential and is stated clearly.

## Minor correction

1. **Common objective scale omitted in the entropy specialization.**
   Location: `sections/11c-concrete-movement.tex:315`.
   The sentence “For equal objective weights,
   Delta_eff = exp(H(p))” is false for equal weights other than one.
   Under the immediately preceding definition, if every lambda_a equals
   a common lambda > 0, then

       Delta_eff = lambda exp(H(p)).

   The general theorem and its proof have the correct scale; this is only
   an incorrectly stated specialization. For example, one tree of objective
   weight 2 has p = 1 and Delta_eff = 2, whereas the displayed specialization
   gives 1. Change “equal objective weights” to “unit objective weights,”
   or give the general common-lambda identity. No other theorem or bound
   needs changing.

## Mathematical checks

### Weighted exposed minors and affine pencils (`11a`)

- Recomputed the Peirce-compression dual norm using
  P(c)P(x)P(c) = P(P(c)x). The resulting squared norm is the support rank,
  including for the exceptional Jordan algebra. Weighting the potential
  and Hessian contributes alpha_i q_i, rather than alpha_i squared q_i.
  Affine restriction can only decrease the covector norm.
- Reoptimized the determinant bound over positive gap allocations. The
  optimizer is g_i = epsilon alpha_i q_i / Q_alpha and gives precisely the
  alpha_i powers in Delta_alpha. The theorem does not assume bounded
  completion fibers or strict complementarity, and its proof does not
  introduce either assumption.
- Checked the full-cone matching curve and the limits of transferring it
  to an affine slice. The certificate is transformed together with the
  reference, and the manuscript correctly refrains from asserting a
  matching upper bound on arbitrary slices.
- The dictionary corollary uses the same selected or existential genuine
  certificate supplied by the earlier rank theorem. It does not exchange
  support/certificate quantifiers or infer movement from a larger barrier
  parameter. Fixed-instance dependence of Delta is explicitly retained.
- Checked Schur-complement concavity and composition with negative log
  determinant, injective-compression invariance, and the trace-gradient
  estimate. The matrix-ball example legitimately uses its restricted
  parameter r, rather than its unreduced pencil order r + q. Inactive
  null directions in the compressed Hessian do not invalidate the
  covector inequality.
- Recomputed both continuous spectral-profile maxima. The geometric
  stationary equation gives m = (2/(3a)) Lambda + O(log Lambda), and the
  polynomial maximum has m = exp((2-beta)/(beta-1))
  epsilon^(-1/(beta-1)). The constants in both displayed asymptotics
  follow. The margin delta ensures that truncation contains the
  maximizer. Fixed rank correctly returns the logarithmic regime.
- The diagonal-box endpoints have each weighted gap at most epsilon/r.
  Their scalar metric coordinates give the stated matching upper orders.
  These are correctly described as particular growing-rank examples,
  not universal tightness of the profile or central-path upper bounds.

### Primal--dual geometry and distribution calculations (`11b`)

- Recomputed the orthogonal central-velocity decomposition, the scaling
  F_*''(s) = eta^2 H^(-1), and both objective derivative identities.
  The definitions consistently distinguish eta derivatives from
  derivatives in log eta.
- The gap-set minimization proof uses affine-feasibility orthogonality at
  its endpoints only. The gradient norm sqrt(2 nu) is ambient, so the
  lower distance bound permits intermediate affine infeasibility, as
  claimed. The upper route has speed sqrt(nu). The bounded-chord
  consequence has the correct starting-local-norm logarithm.
- The dimension envelope uses M >= D + 1 and an interior orthant section.
  Restriction is legitimate for coupled logarithmically homogeneous
  barriers. I checked the integer minimization, including d = 2 and
  remainders zero and one; the theorem makes no unsupported attainability
  claim.
- Recomputed the shared-product-ball primal activity and its complementary
  dual activity. The unique-optimizer example depends on requested
  accuracy; the manuscript expressly distinguishes it from fixed-instance
  asymptotics with all weights positive.
- Checked the sharp scalar Q1/Q2 constants, the head/tail integrations,
  the full-gap tail estimate, and the bounded-chord sampling direction.
  The dyadic geometric example counts j visible channels on the stated
  interval and gives the claimed central-arc order when rank grows. It
  does not identify that arc with shortest distance.
- The final pointwise matrix example has the stated inverse diagonal,
  determinant, diagonal-direction norm, and covector norm. It is clearly
  labeled as nonintegrated pointwise data, not a constructed barrier.

### Concrete formulations (`11c`)

- The height and concave-log-slack lemmas bound every feasible path to the
  accurate set. The concavity assumption is not incorrectly applied to
  Lorentz quadratic determinants later.
- Grouped and packed stationary equations give the common residual
  q and radial profile r. Free completion variables are retained both
  in the stationary calculation and in the Hadamard endpoint bound.
  The block determinant-vector inequality has the correct 1/c_j weights.
- The heterogeneous AM--GM calculation correctly preserves objective
  scales in the theorem; the sole erroneous specialization is reported
  above. Hermitian one-column packing is stated within the earlier
  real-subspace and real-trace/Jordan-determinant conventions.
- Recomputed weighted tree stationarity q_v/omega_v = q and the subtree
  recursion. All zero-support subtrees remain feasible and smooth at
  finite positive central parameter. The speed follows from differentiated
  restricted stationarity and equals W(1-W/sqrt(W^2+tau^2)).
- Differentiated the scalar arc primitive. Its derivative is
  sqrt(2) sqrt(1+r^2)/(1-r^2), and its leading logarithm is correct.
  Arc partitioning produces the stated feasible Dikin chords.
- Checked the entropy bound, exact unweighted root-parameter substitution,
  and its uniform chord-order conclusion. These are distinguished from
  the sharper fixed-objective leading coefficient in the next section.
- Recomputed the tube residual estimate, backward transport factors, and
  geometric sum. They give the stated A_{rho,R,m}; the bound on final
  objective displacement is valid since L_omega >= 1. The condition
  rho < gamma_a ensures a positive terminal scale.
- In the balance slice, the diagonal candidate has zero balance moment,
  and the entire gradient plus objective is a total-trace normal.
  The exposed rank is rho - 1, the reference scale is (rho - 1)/rho,
  and the integral gives the displayed upper additive logarithm.
  The equality with the body's intrinsic parameter is not misused as a
  claim about every barrier metric.
- For spectral sharing, von Neumann's trace inequality has the required
  direction, determinant AM--GM gives the factor 2 epsilon/R_0, and
  the common reduced barrier gives identical metrics after the stated
  elimination. The stationary radial path supplies the matching leading
  coefficient only for this displayed metric.

### New weighted tree coefficient (`11d`)

- The block support vectors are genuine Lorentz boundary duals when
  alpha_v > 0; their pairings are strictly positive and telescope to the
  whole objective gap. Inactive dual blocks are zero, so support-rank
  arguments alone would indeed omit their cost.
- Checked the inactive-subtree bound: an inactive child axis is orthogonal
  to the active support direction; Lorentz feasibility bounds its square
  by 2g/alpha_parent. Positivity and tree monotonicity propagate the bound
  to all descendants. All constants are finite for a fixed objective.
- Independently inverted the Lorentz Hessian. For a null dual s,
  D log(s^T x) has squared dual norm one; half of the barrier gradient
  has squared dual norm one-half. Thus the chosen weighted potential
  has precisely squared norm K_c before restriction. Its increase at
  every accurate endpoint is K_c log(1/epsilon) - O(1), proving the
  path-independent lower bound.
- The upper construction's prescribed determinants telescope exactly,
  root one is satisfied, and positive square roots put every block on
  the correct sheet. Active block squared speed is
  1 + O(h + lambda^(-2)); a whole inactive subtree is a fixed interior
  vector scaled by sqrt(h)/lambda, giving block speed
  2(1/2 + 1/lambda)^2. Summation and integration yield the stated
  O(log log(1/epsilon)) remainder. This argument does not assume every
  leaf coefficient is nonzero.
- Checked the central/distance ratio, the two-node example, the product
  construction, and independent zero-objective factors. The discontinuity
  as an objective component vanishes is correctly explained as a
  nonuniform fixed-objective limit. No all-barrier or unrestricted
  iteration conclusion is attached to this coefficient.

## Source coverage and attribution

The workbench principal-minor and norm-tree developments are represented
with their operative hypotheses and finite-rank limitations. The source
map explicitly routes integer ledgers and query/work questions to Stage5B;
I found no missing Stage5A result that must be inserted before closing this
stage. The companion actually contains the overlapping exposed-minor,
primal--dual, distribution, grouped/packed, and uniform tree material, and
this draft attributes those results rather than advertising the general
mechanisms as new. Its specific new tree claim is narrowly stated.

I opened and checked the primary online texts:

- Nesterov--Todd, [full text](https://people.orie.cornell.edu/miketodd/NTRiemann.pdf),
  especially Theorem 5.1(c), Theorem 5.2, and Corollary 5.1. These already
  cover the feasible gap set and allow intermediate affine infeasibility;
  the draft's classical attribution is appropriate.
- Hauser--Guler, [full text](https://arxiv.org/pdf/math/0103196), for the
  classification context of self-scaled barriers. The manuscript restricts
  its use to the cone and does not extend it to arbitrary coupled barriers
  on a slice.
- Nesterov--Nemirovski,
  [full text](https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf),
  for the general primal-distance comparison context.

Targeted searches on norm-tree Riemannian/barrier distances did not identify
an earlier explicit active/inactive weighted coefficient. This is limited
negative evidence, not proof of priority; the manuscript does not turn it
into an exhaustive novelty assertion.
