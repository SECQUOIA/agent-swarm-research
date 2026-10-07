# Independent Stage 4 review 2

## Verdict

**No major issue found.** The full primal–dual geometry, same-instance three-scale comparison, weighted exposed-minor bound, operational-dimension argument, and concrete formulation results are mathematically consistent. I found one minor error in the interpretation of the heterogeneous entropy scale: the displayed simplification requires unit weights, rather than merely equal weights.

Read all of `05-primal-dual.tex`, `06-formulation.tex`, `appendix-formulations.tex`, the new verification script, bibliography/main integration, and their earlier metric/movement dependencies. Consulted the Stage 4 literature ledger and relevant primary texts, not other reviewers' reports. Did not edit the manuscript or run a competing build. The existing final build log contains no warnings, undefined references/citations, or overfull/underfull boxes. The pending Stage 5 introduction, abstract, and figures are outside this review.

## Required minor repair

### MINOR 1 — “Equal weights” omits the common objective scale

Location: `sections/appendix-formulations.tex`, line 223, immediately after `eq:heterogeneous-formulation-distance`.

The assertion

“For equal weights, `Delta_eff=exp(-sum_a p_a log p_a)`”

is false for a common weight other than one. From the preceding definition, if every lambda_a=lambda, then

`Delta_eff=lambda exp(-sum_a p_a log p_a)`.

For example, two sources of equal size and weights lambda_1=lambda_2=2 have p_1=p_2=1/2 and Delta_eff=4; the sentence as written gives 2. The main weighted distance formula and the subsequent AM–GM statement are correct.

Suggested fix: replace “For equal weights” with “For unit weights”, or display the common-weight factor lambda explicitly. No proof change is required.

## Independent proof checks

### Negative-pairing conjugacy, speed, and the entire feasible gap set

At a center s=-eta^{-1}F'(x), the optimizer defining the negative-pairing conjugate is eta x. This gives exactly `F_*'(s)=-eta x`, `F_*''(s)=eta^2 H^{-1}`, and `F(x)+F_*(s)=nu log eta-nu`. Differentiation with respect to log eta yields `eta dot(s)=F'(x)-H dot(x)`. Therefore the two whitened tangents sum to g and belong to complementary Euclidean subspaces; the projection signs and the full-row-rank Schur expression are correct. The objective derivative identities have the correct eta factors and signs, and their integrated versions explicitly require convergence to the optimum.

For the gap-set result, primal–dual affine feasibility makes the cross difference pairing zero. The gradient at the terminal center is nonnegative toward every feasible smaller-gap point. Convexity of the barrier therefore gives a minimum over the entire target set, without requiring any particular final certificate. Its ambient gradient dual norm is sqrt(2 nu), which yields the printed lower constant sqrt(nu/2). Constant central speed gives the upper constant sqrt(nu). Intermediate affine infeasibility is harmless because the gradient bound holds on the ambient product cone. The chord conversion uses the starting local norm and the correct `-log(1-R)` constant.

The attribution is appropriately explicit: the entire feasible gap-set comparison, and permission for intermediate affine infeasibility, are already in Nesterov–Todd, not a new endpoint-set extension.

### Product-ball homogenization and small primal projections

The private-column embedding has k rows and at least k columns. Restricting the classical matrix-norm-cone barrier gives precisely `(k-1)log(t)-sum log(t^2-||y_a||^2)` and logarithmic degree k+1. The positive log term is justified by that prior barrier, not an invalid subtraction rule. The infinity-norm section gives the claimed optimal degree for k>=2, and the separate k=1 orthant argument supplies the missing low-dimensional case.

The t=1 restriction is the standard product-ball metric of parameter k. Its active radial speed formula and the dual complement k+1-q_eff are consistent with the full cone geometry. The all-positive small-weight example has a unique projected optimizer, while its weights explicitly depend on epsilon. Its activity upper bound and terminal gap are correct; the text preserves the distinction between a uniform objective-family counterexample and the eventual behavior of a fixed all-positive objective. The analytic-center eta=0 limit is used only for the primal projection, not as a finite full primal–dual starting point.

### Same dyadic input, finite starting point, and finite counts

The box objective signs imply beta-alpha=w, and complementarity gives the stated standard central coordinates. The full product speed is sqrt(2r) and the endpoint full gap is exactly 2 epsilon_r. The initial slack equation gives alpha_i^0>=1/sqrt(2). At any feasible final pair of gap at most 2 epsilon_r, every alpha_i<=epsilon_r, so projection onto their logarithms proves the lower bound to all feasible outputs. This does not prescribe the final dual solution.

The primal comparison genuinely starts at the finite center with log eta=0. The missing negative-parameter tail has uniformly bounded primal length because the exact dyadic weights have bounded l2 norm. The final interval from the first accurate label to T has length at most sqrt(r). These changes preserve both primal asymptotic orders. For the lower finite central count, prepending only O_R(1) sampled chords allows use of the earlier discrete potential theorem; the argument does not infer a lower count merely from arclength. It also handles fixed tubes and backward labels. The ordinary encoding B=Theta(r^2) gives all three printed B-scales.

### Weighted exposed support minors and arbitrary fibers

The quadratic-representation identity `P(c)P(x)P(c)=P(P(c)x)` gives an exact ambient squared dual norm q for the derivative of the negative log exposed minor. Positivity of the compressed element in its Peirce algebra is justified even when the certificate is singular in the full algebra. This argument includes arbitrary inactive eigenvalues and cross fibers, not just block-diagonal points.

For alpha_i weights, the covector is also multiplied by alpha_i, while the inverse metric divides by alpha_i. Thus its squared norm is exactly `Q_alpha=sum alpha_i q_i` before restriction and at most that afterwards. Maximizing the determinant product under the objective-gap sum allocates `g_i=epsilon alpha_i q_i/Q_alpha`. This produces exactly the printed alpha-dependent Delta scale, including its denominator. The positive-part and initial-offset round bounds are consistent in both signs of the logarithm. The full-cone path proves only a leading coefficient, and the manuscript correctly declines to infer the same upper bound on an arbitrary affine slice.

Hauser–Güler's classification has coefficients at least one, matching the chosen standard self-concordance normalization. The text correctly retains the weighted scale rather than changing only the rank coefficient.

### Operational dimension and arbitrary coupled cone barriers

The compact full-dimensional projected body requires operational dimension at least D+1: if the dimension were D, the full-rank affine projection would be invertible and the feasible affine slice would have to span the entire operational space, leaving an unbounded affine image of the cone. The argument applies to the declared affine-cone-lift model and uses no certificate selections.

A plane through an interior point of a proper nonray factor yields a proper two-dimensional wedge. Its relative interior is inside the factor's interior and its boundary inside the factor's boundary. The product of these sections and all ray factors is therefore an interior orthant section to which the barrier restriction applies, even for a coupled original barrier. Its dimension is r_0+2q_0. Minimizing this charge subject to r_0+dq_0>=D+1 gives the stated exact integer envelope Psi_d. The extra full primal–dual assumptions are made explicit before applying the classical gap-set result.

### Grouped and packed formulations

The affine Hessian formulas retain the necessary quadratic W term. Positive definiteness on the free coordinates follows directly, and affine PSD restriction gives standard self-concordance. Trace Cauchy–Schwarz bounds the gradient parameter by the number of residual columns H, without charging the fixed identity block.

Hadamard's inequality permits every packed off-diagonal completion to move. Minimizing over them makes residual D diagonal, reducing the center calculation to the grouped problem. The source equation hq+(tau q/2)^2=1 yields the displayed q and radius, and differentiated stationarity gives the claimed speed. The limiting central gradient norm proves that parameter H is exact. The target residual-product collapse follows from the full source norm, so arbitrary completion variables cannot evade the distance estimate.

### Norm trees and the exact root-slice parameter

Telescoping gives sum_v q_v=1-||w||^2, and every positive nonroot axial stationarity equation forces its two adjacent residuals to agree. The stated central internal coordinates are feasible and unique. The common center speed therefore agrees with that of grouped sources with h=b, although the full restricted parameter may be larger.

For the parameter proof, homogeneity and projection give `||DF||_*^2=2b-1/beta_T` with `beta_T=(H^{-1})_(tt)/t^2`. The Dikin halfspace argument gives beta_T<=1. If a root leaf exists, the trial direction has exactly zero residual second derivative, and its norm tends to one while all subtree directions remain fixed. This proves the matching supremum beta_T=1.

When all root children are internal, eliminating strict descendants leaves axial curvature at least a_i^{-2}. The monotonicity of a minimizing quadratic form justifies replacing each such curvature by this lower bound. I independently expanded the rank-one inverse calculation: its Schur complement is the displayed expression with Z. The inequality Z<=r^2/(1+r) reduces S>=2 to `3r(1-r)^2/(1+r)>=0`. Shrinking all child subtrees and using the root-only trial direction gives the matching limit two. Hence the two exact parameters are 2b-1 and 2b-2, respectively. Product parameter suprema add.

The barrier-height lower bound, exact central route length, and uniform `0<epsilon<=k/4` chord comparison follow with the stated constants. The heterogeneous residual-product optimization is also correct; only the common-weight simplification identified above needs repair.

## Independent verification

Ran `scripts/verify_primal_dual_formulations.py` under `/workspace/local-home/miniconda3/envs/qipm/bin/python`, without installing packages. Every diagnostic passed: full KKT/progress checks, exact dyadic data at four ranks, arbitrary-fiber minors, affine packed Hessians, integer envelopes, four tree shapes, and root Schur inequalities.

Added independent checks in a temporary inline Python process, without editing files:

- Generated 300 noncentral feasible points across three linked-tree shapes by selecting residuals and leaves first, then reconstructing internal radii and normalizing the root. Direct restricted-Hessian inversion respected the claimed parameter in every case.
- Evaluated the root-leaf boundary sequence at delta=0.1,0.03,0.01; its squared gradient norms were approximately 2.940900, 2.984606, 2.994969, approaching the exact parameter 3.
- Evaluated the all-internal-root boundary sequence at the same deltas; its norms were approximately 3.629725, 3.967504, 3.996399, approaching the exact parameter 4.

These diagnostics support the analytical proofs and do not certify unsampled cases.

## Primary-literature and integration check

Revisited Nesterov–Todd's local primary Theorem 5.1/5.2 and Corollary 5.1, including the explicit sentence permitting affine-infeasible intermediate sequences. Read the relevant local primary text of Hildebrand Corollary 6.2 (n>=3) and Hauser–Güler Theorem 5.5 (all coefficients>=1). Inspected NN1994 Proposition 5.4.6(i), printed p.199, in the local book extraction; its spectral-cone formula agrees with the homogenization used here. These support the manuscript's narrow attributions. The new sections avoid claiming novelty for the classical product speed, whole-gap-set comparison, cone barrier, classification, or quadratic-representation identity.

All Stage 4 source-map themes are represented with their necessary distinctions: full product versus primal restricted metrics, exact finite central start, actual output accuracy versus full gap, weighted certificate scale, arbitrary auxiliary motion, and specified-formulation versus arbitrary-lift claims. No major integration or unsupported scope claim was found.
