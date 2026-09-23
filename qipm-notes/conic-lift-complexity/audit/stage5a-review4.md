# Stage 5A independent review 4

I personally read all of `11a-exposed-movement.tex`,
`11b-primal-dual-movement.tex`, `11c-concrete-movement.tex`, and
`11d-tree-distance.tex`, together with the author record. I did not delegate,
read other reviewers' reports, edit the manuscript, or rebuild its shared
artifacts. I checked the relevant earlier tree, packing, balance-slice,
spectral-cone, and chordal-star statements and the companion's formulation
appendix. I also checked the original grouped-ball tube argument.

**Recommendation: accept after one minor correction. No major issue found.**

## Required minor correction

1. **Common objective-weight normalization:**
   `sections/11c-concrete-movement.tex:315` says that *equal* objective
   weights give `Delta_eff = exp(H(p))`. With the immediately preceding
   definition, common weight `lambda > 0` instead gives
   `Delta_eff = lambda exp(H(p))`. For example, one tree with objective
   weight two has `p=1` and `Delta_eff=2`, not one. Change “equal objective
   weights” to “unit objective weights,” or include the common factor
   lambda. The general theorem, its proof, and the following inequality
   `Delta_eff <= sum lambda_a` are correct. This is a local normalization
   slip, not a problem with the entropy-scale result.

## Mathematical checks

- **Weighted exposed minors (11a):** The Peirce-compression fundamental
  identity gives squared dual norm `q_i` with the stated Jordan trace
  normalization. Weighting both potential and metric contributes
  `alpha_i q_i`, and restriction decreases the dual norm. Maximizing the
  weighted determinant product allocates gap
  `epsilon alpha_i q_i / Q_alpha`; this reproduces every factor of
  `Delta_alpha`, including its powers of alpha. The full-cone upper curve
  gives the stated leading coefficient; its explicit restriction to the
  full cone avoids an unsupported assertion about arbitrary affine slices.
  The dictionary corollary retains the same genuine certificate and the
  correct generic/existential/global quantifiers.

- **PSD contraction and exposure profiles (11a):** Schur-complement
  concavity and monotone convex composition justify the Hessian
  contraction. QR reduction handles nonisometric injective compressions.
  The chosen compressed trace is bounded by the target trace, and the
  reference spectrum includes the reference slack rather than only the
  exposing matrix. I differentiated both continuous optimization
  expressions: the geometric maximizer is asymptotic to
  `2 log(1/epsilon)/(3a)`; the polynomial maximizer is
  `exp((2-beta)/(beta-1)) epsilon^(-1/(beta-1))`. The leading constants,
  integer rounding, growing-rank conditions, and fixed-rank crossover are
  correct. The diagonal-box upper paths prove matching orders only where
  stated, without asserting matching arbitrary-pencil distances.

- **Primal--dual geometry (11b):** Differentiating the central relation
  gives `H^(1/2) xdot + eta H^(-1/2) sdot = H^(-1/2) F'`.
  Feasibility makes the two summands orthogonal, proving the speed split
  and the objective-progress identities. Convexity at the center of gap
  epsilon gives the minimum product-barrier value over the entire feasible
  gap sublevel. Its ambient gradient norm is `sqrt(2 nu)`, yielding the
  stated lower constant; constant central speed gives the upper constant.
  Strict feasibility, endpoint feasibility, and the distinction between
  ambient intermediate motion and primal-only motion are explicit.

- **Dimension envelope (11b):** Each nonray proper factor has a planar
  interior section, and the product section meets the ambient interior.
  Thus its orthant lower bound applies even to coupled barriers. Minimizing
  `r+2q` subject to `r+dq >= D+1` gives exactly the displayed integer
  envelope, including `d=2` and zero remainder. Its status as a charge
  envelope, rather than an attainable frontier for every body, is clear.

- **Product-ball distribution calculations (11b):** The radial solution,
  logarithmic speed, Q1/Q2 constants, and their equality cases at scalar
  argument one check directly. The head-tail bounds use different first
  and second moments as claimed. The unique-exposure example changes the
  instance with requested accuracy and says so. The geometric-weight
  interval estimate and the remaining logarithmic interval yield the
  stated central-arc order, without implying an unrestricted shortest-path
  theorem. The pointwise metric example is explicitly not claimed to
  integrate to a barrier.

- **Grouped and packed distances (11c):** Free completion entries make
  the residual inverse diagonal at the center, but the endpoint proof uses
  Hadamard for arbitrary residuals. It therefore does not inadvertently
  restrict fibers along a competing path. Allocation stationarity and
  leaf stationarity give `h q + r^2=1`, `2r/q=tau`. The residual product
  bound and parameter H give `sqrt(H) log(H q0/(2 epsilon))`. The
  blockwise logarithmic determinant-vector inequality follows from trace
  Cauchy--Schwarz in the full affine Hessian; the positive quadratic W
  term has correctly been retained. The Hermitian one-column extension
  uses real traces and Jordan determinants consistently.

- **Weighted trees and central arcs (11c):** Internal stationarity
  forces `q_v/omega_v` constant; telescoping gives `W q+r^2=1`.
  This remains valid when leaf and subtree coefficients vanish. The
  speed identity follows from differentiated full affine stationarity,
  not an unjustified Hessian of a nonlinear pullback. Integrating its
  radial expression gives the stated artanh primitive and leading
  logarithm. Weighted AM--GM gives the entropy formula correctly; only
  the prose specialization listed above needs correction. The lower
  finite-accuracy distance and bounded-chord upper construction have
  constants uniform in the unweighted tree as claimed.

- **Tube constants (11c):** Let `a_R=(1-R)^(-1)`. Summing transported
  gradient changes gives `a_R^m-1`, and the two endpoint centrality
  residuals contribute `B_rho(1+a_R^m)`. The center-to-iterate Hessian
  comparison gives the factor `1-rho` in the denominator. The final gap
  bound uses `rho sqrt(L_omega)/tau <= rho L_omega/tau`, which is valid
  because `L_omega>=1`. The hypotheses `rho<gamma_a` and
  `tau_j>=aW` supply the needed positivity and uniform central speed.

- **Balance slices (11c):** For the proposed diagonal point,
  `gradient Phi + tau S = -e/a` is the full trace normal. The balance
  moment is zero because the moments are off-diagonal in the selected
  frames. Consequently this is full-slice stationarity even in the Albert
  case, not merely stationarity in a diagonal subspace. With
  `Q=rho-1`, the metric along the curve is
  `Q dg^2/g^2 + dg^2/(1-g)^2`. Integration gives exactly the stated
  upper additive term `log(rho(1-epsilon))`; the lower scale is
  `Q/rho`. The argument properly confines the metric conclusion to the
  displayed standard barrier.

- **Spectral and chordal invariance (11c):** Von Neumann's inequality
  gives `sum(1-sigma) <= R0-ell`, in the direction needed for AM--GM.
  The reduced parameter is R0, and full gradient stationarity at
  `X_a=r C_a` gives the same scalar arc. Earlier fixed-identity
  clique--separator elimination gives literally the same barrier, so
  equality of the reduced distances follows. The text does not infer a
  Newton-system or query-cost identity.

- **New all-objective distance coefficient (11d):** I independently
  checked both halves of the proof. The Euclidean Lorentz null duals
  telescope to the true objective gap. Every maximal inactive subtree is
  attached to an active node; orthogonal projection at that node bounds
  its root axis squared by `2g/alpha_parent`, and descendant monotonicity
  bounds all its determinants. In the product metric the active logarithm
  has squared dual norm one and half the determinant logarithm has
  squared dual norm one-half; with weights, their sum is exactly K_c.
  This proves a lower bound for every endpoint and every feasible path.
  In the upper curve all determinant assignments telescope to the root
  equation and the correct positive sheets. Active block squared speeds
  are `1+O(h+lambda^(-2))`; every inactive block is a fixed interior
  vector scaled by `sqrt(h)/lambda`, giving exactly
  `2(1/2+1/lambda)^2`. Weighted summation and integration prove the
  logarithmic-logarithmic remainder. The gap is a positive fixed
  multiple of `exp(-lambda)` to leading order. The arbitrary reference
  connection has finite length on an interior segment. Product potentials
  and synchronized curves give the summed coefficient, while independent
  zero-objective factors can indeed remain fixed. The discontinuity as
  objective support vanishes is correctly explained by the fixed-instance
  order of limits.

## Literature, overlap, and presentation

I opened the primary Nesterov--Todd paper at
<https://people.orie.cornell.edu/miketodd/NTRiemann.pdf> and checked its
Section 3 and Theorem 5.1(c)/5.2. The manuscript correctly attributes the
feasible gap-sublevel minimization and primal--dual distance argument to
this prior work. I opened Hauser--Guler's primary preprint at
<https://arxiv.org/pdf/math/0103196> and checked Theorem 5.5, including
the irreducible coefficients being at least one. I also opened the primary
Nesterov--Nemirovski text at
<https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf> for its
general primal-distance context. These references are used within their
proper scope.

The companion's `appendix-formulations.tex` explicitly contains the
unweighted grouped/packed/tree central paths, unrestricted completion
distance, tree parameter, and heterogeneous entropy scale. The new text
acknowledges this overlap and provides its own proofs. The new weighted
active/inactive coefficient is precisely delimited; no general geodesic
mechanism is claimed as novel, and no priority conclusion is drawn from
unread Duistermaat material. The source dispositions retain the distinct
tube refinement and the deferred balance/spectral movement applications.
I found no additional omission in the assigned stage's stated coverage.

The four sections distinguish ambient parameter, restricted parameter,
objective-sensitive certificate rank, target distance, central arclength,
and bounded-step count consistently. Their local proofs are readable
without the companion. I found no unresolved major mathematical or
scientific issue in this stage.
