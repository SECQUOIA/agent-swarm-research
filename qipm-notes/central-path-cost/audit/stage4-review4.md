# Stage 4 independent review 4

**Verdict: no major issues found.** All new theorem proofs are valid in their stated settings. One minor scaling error in the heterogeneous-weights interpretation should be corrected.

Reviewed all new text in `sections/05-primal-dual.tex`, `sections/06-formulation.tex`, and `sections/appendix-formulations.tex`, the new diagnostic script, bibliography/main integration, and relevant Stage 1–3 interfaces. I did not read other reviewers' reports, communicate with other reviewers, or edit manuscript files. Pending Stage 5 front matter and synthesis are outside this review.

## Minor finding

**The entropy specialization needs unit weights, or a common-weight multiplier.** Location: the final paragraph of `sections/appendix-formulations.tex`, immediately after `eq:heterogeneous-formulation-distance`.

The text states “For equal weights, `Delta_eff=exp(-sum p_a log p_a)`.” With the subsection's general positive weights, equality of the weights means `lambda_a=lambda`, and the definition instead gives

`Delta_eff=lambda exp(-sum p_a log p_a)`.

For example, with one source and weight two, the defined scale is two, while the printed specialization is one. **Repair:** replace “For equal weights” with “For unit weights,” or retain the general common factor in the formula. The heterogeneous theorem, its proof, and the following weighted AM–GM bound are correct; only this interpretive specialization is affected.

## Mathematical checks

### Classical primal–dual geometry and little-primal-movement examples

- The negative-pairing conjugate convention is consistent throughout. At an exact center, `F_*''(s)=eta^2 H^{-1}`, `F_*'(s)=-eta x`, and the sum of barrier values is `nu log(eta)-nu`; there is no missing additive normalization constant.
- The differentiated central relation gives `g=v+d_0` with the stated orthogonal tangent spaces. The projector formulation handles rank-deficient equalities. The inverse Schur formula is explicitly restricted to full row rank, and removing redundant equations does not change either objective-progress identity.
- The primal and dual speed signs agree with minimization and maximization respectively. Integrating the objective derivatives uses exactly the convergence assumption stated in the proposition.
- The gap-set proof uses feasible endpoint orthogonality to make the central supporting hyperplane nonnegative on the entire smaller-gap set. Integrating the ambient gradient norm then proves the lower bound for paths whose intermediate points may be affinely infeasible. The central upper route has the claimed constant product speed. No same-endpoint theorem is being incorrectly substituted for a target-set statement.
- The product-ball cone is a valid sparse row restriction of the cited spectral-norm-cone barrier. The logarithmic degree is `k+1`; the positive log term is justified by that restriction, not by a subtraction rule. The infinity-norm section gives the matching lower bound, with the two-dimensional case treated separately.
- The rank-one objective and all-positive perturbation examples use the restricted primal barrier parameter `k` and full logarithmic parameter `k+1` consistently. The weights in the all-positive example really depend on requested accuracy, which is explicitly acknowledged. The unique projected optimizer does not prevent small primal activity on the stated finite parameter interval.

### Same-data completion theorem and actual finite counts

- Checked the standard-form cost signs and the relation `beta_i-alpha_i=w_i`. Complementarity gives precisely the earlier dyadic central coordinates and full gap `2r exp(-s)`.
- The initial smaller slack satisfies `alpha_i^0>=1/sqrt(2)`. Feasibility at an arbitrary final certificate yields `gap=sum(2alpha_i+v_i w_i)` and hence `alpha_i<=epsilon_r`. The dual logarithmic coordinate contraction therefore supplies the stated lower bound regardless of the unprescribed final certificate or intermediate affine feasibility.
- The full product length is `sqrt(2r) T`, while the full target-set lower bound is of order `sqrt(r) T`. Combining lengths/distances with the starting-norm chord estimates gives both full rows of the table.
- The negative-log-parameter primal tail has uniformly bounded length on the dyadic weights. The last segment after first accuracy has length at most `sqrt(r)`. These errors preserve the endpoint-distance and central-length orders.
- The central-iterate lower bound correctly invokes the discrete potential theorem after prepending a bounded number of tail chords. It does not incorrectly infer a chord lower bound solely from central arclength. This transfer also covers the stated fixed tubes with arbitrary label order.
- The bit-length conversion and the factor comparing optimal full completion with optimal primal movement are correct. The text explicitly states the slightly different primal and full target accuracies and the finite full-central initialization.

### Exposed minors, weighted scales, and auxiliary fibers

- The Jordan fundamental identity gives `P(c)P(x)P(c)=P(P(c)x)`. It yields the exact ambient covector norm squared `q` for the negative log exposed minor, including noncommuting auxiliary components. The proof does not need their boundedness or strict complementarity.
- Positive definiteness of the compressed element follows from order positivity of `P(c)`, as stated. The determinant/trace transformation inside the Peirce algebra has the right scale and rank normalization.
- With barrier coefficients `alpha_i`, the covector norm squared is `sum alpha_i q_i`. Maximizing the determinant product assigns error mass in proportion to `alpha_i q_i`; this produces exactly the alpha factors in `Delta_{c,alpha}`. The weighted scale is not silently replaced by its unweighted version.
- Affine restriction can only reduce the covector dual norm and restrict admissible curves. The proof therefore handles arbitrary feasible auxiliary motion. The reference-point and per-round triangle inequalities are correct.
- The full-cone asymptotic sharpness construction preserves the certificate rank under the reference-normalizing cone automorphism. Shrinking its support eigenvalues produces the leading coefficient `sqrt(Q_alpha)`. The text correctly warns that an affine slice can exclude that upper route.

### Arbitrary operational cone factors

- Compactness and full-dimensional projection imply operational dimension at least `D+1`: equality with `D` would make the projection invertible and force the slice to have no effective equations, giving an unbounded affine image of the whole cone.
- A two-dimensional linear section through an interior point of each nonray proper cone is a proper wedge. Its relative interior belongs to the original interior and its boundary to the original boundary, so barrier restriction is legitimate. This supplies an orthant section even when the original barrier couples factors.
- The dimension-cap integer minimization is correct for rays, nonray factors, divisible and remainder cases, including `d=2`. The resulting lower bound concerns a barrier on the operational product cone, exactly as stated; it is not transferred to an arbitrary barrier on the body.
- The movement conclusion follows from the full primal–dual gap-set theorem and its actual endpoint assumptions. No primal parameter-only inference appears.

### Grouping, packing, trees, and heterogeneity

- The affine-coordinate Hessians include the additional positive `W`/`w` derivative terms. Treating the nonlinear residual as an affine variable would give a wrong metric; the manuscript explicitly avoids that error.
- Positive definiteness and standard self-concordance follow from the actual affine PSD restrictions. The gradient estimate charges only the free residual column count. The center-limit calculation proves the exact restricted parameter, so fixed identity blocks are not mistakenly charged.
- Hadamard's inequality handles unrestricted off-diagonal completion variables. Partial minimization over those variables makes the residual diagonal and leaves the grouped equations. The stated common residual, radial coordinate, speed, and path length follow correctly.
- The support deficit inequalities remain valid even when an accurate endpoint is not aligned with the objective. The source residual sums, product collapse, and target-set lower bound therefore control the entire feasible accurate set.
- The positive-sheet norm-tree domain is convex, and its linked Hessian is positive definite. Telescoping gives the exact residual budget. Stationarity forces equal residuals because nonroot axial coordinates are positive. The reconstructed internal coordinates are feasible and give the stated shape-independent central path.
- Independently checked the root-leverage formula and both exact-parameter limits. For a root leaf, the supplied trial direction has zero residual second derivative and norm tending to one. For an all-internal root, eliminating descendants and using their axial halfspace bounds gives the displayed root Schur complement. Its scalar estimate is valid and bounds the leverage by one half; shrinking the child subtrees supplies the matching limit.
- The exact restricted tree parameter is used in the barrier-height lower bound. Its universal comparison with `2L` produces the stated matching orders uniformly for `0<epsilon<=k/4`.
- In the heterogeneous version, terminal error is allocated with weights `m_a/M_0`, while the objective coefficients enter the scale separately. The product ratio and exact grouped/packed parameter are correct. Only the final equal-weight specialization needs the minor correction above.

## Verification and primary-source assessment

Ran `scripts/verify_primal_dual_formulations.py` with the existing qipm interpreter. All full KKT/progress checks, dyadic complementarity checks, arbitrary-fiber minor and packing tests, integer envelope checks, tree center/speed checks, and root Schur inequalities passed.

Also independently evaluated the two noncentral limiting tree configurations used to prove exactness. For a two-node tree with a root leaf, the restricted gradient squared norm increased from approximately `2.94521` to `2.99850` as the limiting parameter decreased from `0.1` to `0.003`, approaching the claimed value three. For a three-node tree with only internal root children it increased from `3.87760` to `3.99989`, approaching four. These diagnostics test the supremum witnesses rather than only the central path.

Read the relevant local Nesterov–Todd statements, including Theorem 5.1(c) and Corollary 5.1. The manuscript's explicit classical attribution matches their gap-set and intermediate-infeasibility scope. Independently opened [Hildebrand's primary preprint](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf), Corollary 6.2: it gives the infinity-norm cone lower bound and has the stated dimension restriction. Independently opened [Hauser–Güler's primary preprint](https://arxiv.org/pdf/math/0103196), Theorem 5.5: the classification uses Jordan log determinants with coefficients at least one, as the manuscript states.

The novelty language within this stage is appropriately limited: classical projection and gap-set geometry, barrier constructions, and the self-scaled classification receive credit. The formulation results are presented with their actual metric/certificate contracts. No unsupported lift-rank frontier or unconditional runtime claim is made.

No additional mandatory finding was identified. Final introduction, manuscript-level contribution prioritization, and concluding interpretation remain the explicitly planned Stage 5 work.
