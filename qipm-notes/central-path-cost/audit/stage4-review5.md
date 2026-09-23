# Stage 4 independent review 5

Reviewed 2026-09-07. I read both new sections, the formulation appendix, the new verification script, bibliography/main integration, relevant earlier definitions, primary-source preparation, and the current literature ledger. I did not read any other review report or communicate with other reviewers. Final introduction, abstract, and figures are outside this stage's scope.

## Verdict

**No major issue identified in the Stage 4 mathematics or attribution.** The full feasible gap-set result is correctly identified as classical. The finite-start three-scale comparison preserves the same dyadic instance. The weighted exposed-minor scale, dimension argument, arbitrary PSD completion treatment, and root-dependent tree parameters withstand the checks below.

Two minor corrections are needed: one common-weight factor and one definition clarification.

## Required minor corrections

1. **Equal weights versus unit weights.** `sections/appendix-formulations.tex:223` says that “For equal weights” Delta_eff is exp(entropy). For equal weights lambda_a=lambda>0, its definition instead gives `Delta_eff=lambda exp(-sum p_a log p_a)`. For example, a single source with lambda=2 has Delta_eff=2, whereas the stated equal-weight specialization gives 1. Replace “equal weights” with “unit weights,” or retain the common factor lambda. The general formula and the subsequent weighted AM–GM equality condition are correct.

2. **Define the operational lift explicitly.** At the start of Theorem `thm:dimension-dictionary`, give the affine-lift contract as `C=pi(K intersect L)`, with L affine and pi affine, and explain “minimal operational face” as the smallest product face containing the feasible slice, considered in its linear span (with zero factors removed). The proof uses precisely this conventional lift representation and its reduced ambient dimension. The current word “operational” has no definition in the manuscript and could be confused with the dimension of the affine feasible slice or the projected body. No change to the dimension argument is needed under the intended meaning.

## Mathematical review

### Negative conjugate, speed split, and the feasible gap set

- With the negative-pairing conjugate, the maximizer defining F_*(s) at an eta-center is eta*x. This gives `F_*'(s)=-eta x`, `F_*''(s)=eta^2 H^(-1)`, and `F(x)+F_*(s)=nu log eta-nu`. The signs and scaling in the section are consistent.
- Differentiating in log eta gives `eta dot(s)=F'(x)-H dot(x)`. Whitened primal and dual velocities sum to g=H^(-1/2)F'(x), lie in orthogonal feasible tangent spaces, and hence have squared norms adding to nu. The full-row-rank Schur expression has the correct H inverses, and MHM=M yields the stated objective progress identities. Redundant equality rows do not change the tangent-space claim.
- At a central point of target gap epsilon, the supporting-hyperplane derivative of the product barrier toward any feasible smaller-gap point is nonnegative. Orthogonality of feasible differences is exactly what makes the bilinear complementarity gap reduce to the displayed affine expression. The center therefore minimizes the product barrier over the *entire* feasible target set. The ambient gradient dual norm sqrt(2nu) gives the lower distance, while constant product speed sqrt(nu) gives the upper route. Intermediate affine infeasibility is allowed by the ambient metric lower proof.
- The manuscript attributes this result to Nesterov–Todd's Theorem 5.1(c), Theorem 5.2, and Corollary 5.1; it does not repackage the target-set inference as new. Projection calculus is also expressly attributed to classical work.

### Optimal product-ball cone barrier and small primal activity

- The private-column-block matrix construction has YY*=diag(||y_a||^2). Restricting the classical spectral-norm-cone barrier therefore gives exactly the displayed sum of log quadratics plus (k-1)log t. Its logarithmic degree is k+1. The argument correctly avoids an invalid subtraction rule for self-concordance.
- A one-direction section in each block produces the (k+1)-dimensional infinity-norm cone. Hildebrand's lower bound supplies k+1 for k>=2; k=1 is separately handled by the two-dimensional orthant. Thus “optimal over logarithmically homogeneous barriers” has the appropriate scope.
- On t=1 the restricted metric is the sum of rank-one ball metrics, and the effective primal activity is the displayed sum. The dual activity is the complement k+1-q_eff. With a single active objective, the large dual length and small primal length follow directly.
- In the positive-weight perturbation, `(eta w_a)^2<=epsilon^2/nu^2` for a>=2 and eta<=nu/epsilon. Summing gives the stated upper primal activity and lower dual activity. The optimizer is unique because every weight is positive. The text correctly says that the objective depends on the requested accuracy and that fixed positive weights eventually activate all k channels.

### Finite-start dyadic three-scale comparison

- The standard-form objective gives beta_i-alpha_i=w_i. Central complementarity is `u_i alpha_i=v_i beta_i=exp(-s)`, yielding x_i=q(exp(s-a_i)), the primal activity profile, and full squared speed 2r. The finite start s=0 means eta=1, not the primal analytic-center limit.
- The initial alpha bound is correct: the equation `1/alpha+1/(alpha+w)=2`, with w<=1, gives alpha>=1/sqrt(2). At an arbitrary strictly feasible target, `gap=sum(2alpha_i+v_i w_i)`, so every alpha_i<=epsilon_r when the gap is at most 2epsilon_r. Projecting an arbitrary full curve onto these logarithmic dual slacks gives the claimed lower distance without fixing a final dual certificate.
- The full central route has exact length sqrt(2r)*T, so the upper and lower full movement orders match. The classical whole-gap theorem gives the same order and is cited as an alternative lower proof.
- Passing from the earlier analytic-center primal start to the finite start removes only O(1) central length, since sum w_i^2=O(1). Passing from first accuracy to s=T adds at most sqrt(r). These changes preserve both primal endpoint distance and central length orders. For the lower central *chord count*, the proof correctly prepends a bounded number of sampled initial chords and invokes the discrete potential theorem; it does not infer chord counts from central arclength alone.
- The same argument covers fixed tubes and backward labels. The comparisons use the exact same dyadic weights and tolerance, with the full target gap explicitly 2epsilon_r. The bit-length substitutions are correct, and the final scope statement does not turn movement into an unrestricted runtime or query lower bound.

### Weighted exposed support minor and arbitrary fibers

- For a rank-q support idempotent c, the fundamental quadratic-representation identity gives `P(c)P(x)P(c)=P(P(c)x)`. Therefore the squared ambient dual norm of the principal-minor log-determinant covector is exactly q, independent of unexposed coordinates and cross fibers. The proof uses the correct trace and Peirce normalizations and extends to the exceptional algebra.
- Scaling the barrier and covector by alpha_i gives contribution alpha_i q_i to the squared dual norm, so the total coefficient is sqrt(Q_alpha). Affine restriction can only reduce this dual norm.
- Within each exposed Peirce algebra, the transformed certificate gives trace g_i and determinant det(s_i)det(P(c_i)y_i). Spectral AM–GM followed by the weighted optimization over g_i yields `g_i=epsilon alpha_i q_i/Q_alpha`, including the factors alpha_i^(alpha_i q_i). Thus the weighted Delta scale is correct; it is not the unweighted scale with Q merely renamed.
- The positive-part distance and approximate-start/round estimates follow from integrating the covector and applying the triangle inequality. No bound on inactive eigenvalues or auxiliary variables is used. The full-cone support-scaling path proves the stated leading coefficient; the text explicitly does not infer the same upper path on an arbitrary affine slice.
- Hauser–Güler's classification applies to irreducible symmetric-cone factors with coefficients at least one, exactly as stated. The paper does not extend this classification to arbitrary barriers or hide a cone-dictionary rank lower bound inside the distance theorem.

### Arbitrary-cone dimension bound

- Under the lift representation identified in Minor 2, M>=D follows from affine-span dimension. If M=D, the affine projection is invertible and the affine slice must have full ambient affine hull, hence no effective affine restriction; its image is an affine image of the whole proper cone and is unbounded. Compactness therefore forces M>=D+1.
- A two-dimensional linear section through an interior point of any nonray proper factor is a proper wedge isomorphic to R_+^2. Its relative interior is interior to the factor: a supporting hyperplane at an interior point of the section would otherwise contain an ambient interior point. Taking the product with ray factors gives an orthant section of dimension r_0+2q_0, even when the barrier couples factors. Restriction preserves the logarithmic degree and self-concordance, so the classical orthant lower bound applies.
- The integer minimization of r_0+2q_0 under r_0+d q_0>=D+1 is exactly Psi_d(D+1). The remainder inequality gives Psi_d>=2(D+1)/d. Applying the classical product gap-set theorem yields the stated round bound. This is correctly described as a synthesis, not a sharp general lift frontier or a parameter-only primal lower bound.

### Grouped and packed formulations

- The Hessian formulas retain the second derivative of the quadratic residual. In particular, `tr((D^(-1) dot(D))^2)+2 tr(D^(-1) dot(W)^T dot(W))` is the correct affine-coordinate Hessian; treating D as independently affine would be wrong. The formulas imply positive definite metrics on free coordinates, standard self-concordance via the fixed-identity PSD restriction, and gradient parameter at most the number of columns H.
- Residual diagonal sums equal 1-||w_a||^2. The support inequality gives at most 2delta_a per source. Hadamard applies to arbitrary positive definite completion residuals, so no diagonal-fiber assumption enters the lower bound. Sourcewise and global AM–GM then give the displayed determinant collapse and distance scale.
- At a center, off-diagonal S variables can exactly cancel W^T W off-diagonals. Hadamard shows this is the minimizing residual completion. The remaining scalar equations give common q within each source and w=(tau q/2)c. The source equation `hq+(tau q/2)^2=1` has exactly the displayed solution.
- Differentiated stationarity gives the activity/gradient norm `H(1-h/sqrt(h^2+tau^2))`; its limit proves exact restricted parameter H. Changing from tau to source radius gives the exact length sqrt(H)rho(radius). The lower and upper counts match uniformly for epsilon<=k/4, including growing h or k.

### Norm-tree domains, centers, and exact root parameters

- Positive axial coordinates are explicitly required, selecting convex Lorentz sheets. The linked cone map is injective on free coordinates, so the restricted Hessian is positive definite. Telescoping cancels every nonroot axial square and gives the residual sum 1-||w||^2.
- Internal stationarity forces equal neighboring residuals, since every internal axial variable is positive. Leaf stationarity and telescoping give the same scalar center as the grouped case with h=b. The formula `t_v^2=n_v q+radius^2 C_v` proves both feasibility and uniqueness of positive internal coordinates. The speed follows from differentiated stationarity, not a boundary-regularity assumption.
- Before fixing the root, the linked barrier has degree 2b. Restricting the gradient to the root-fixed tangent space subtracts `t^2/(e_t^T H^(-1)e_t)` from the full squared gradient norm. The leverage beta_T is scale invariant. Dikin containment in the halfspace t>0 gives beta_T<=1.
- With a root leaf, the displayed limiting family remains on the positive sheet. Its trial direction changes only root and leaf, has zero second residual derivative, and norm tending to one. This proves sup beta_T=1 and exact parameter 2b-1.
- With only internal root children, descendant elimination gives effective axial curvature at least a_i^(-2). Replacing it by this lower curvature gives the stated comparison Schur complement. I independently re-derived its factor `16Z/(q+4Z)` and the equivalence `S>=2 iff r(3-r)>=4(2-r)Z`. The bound Z<=r^2/(1+r) leaves `3r(1-r)^2/(1+r)>=0`. Thus beta_T<=1/2. Shrinking all subtrees gives the matching limit and exact parameter 2b-2.
- Product parameters add. Barrier-height integration with the exact parameter proves the sharper tree lower distance; the common center path provides the matching upper order. The proof does not incorrectly subtract a fixed root block's nominal parameter without considering its restricted metric.

### Heterogeneous counts

The weighted source residual-product calculation, e_a allocation proportional to m_a, entropy scale Delta_eff, and distance coefficient M_0/sqrt(nu) are correct. In arbitrary PSD packing, nonuniform central diagonal residuals still separate by source, and the central gradient parameter tends to sum m_a. The only correction is the omitted common factor in the equal-weight specialization noted above.

## Executed checks

Used the qipm Python interpreter and installed NumPy/SciPy only; no packages were installed.

- The supplied script passed 80 full differentiated KKT projection/progress checks, dyadic logarithmic complementarity checks at ranks 4/16/64/256, 80 arbitrary-fiber minor/packing checks, 1,100 integer-envelope checks, four tree-shape center/speed/parameter checks, and 100 root Schur inequalities.
- Independently checked the *limiting noncentral* tree families used for exact parameter attainment. Root-leaf examples approached parameter 3 with values `2.91132918, 2.97409928, 2.99243650, 2.99749348`; all-internal-root examples approached parameter 4 with values `3.77180960, 3.97531450, 3.99778531, 3.99975399` as the scale decreased from 0.15 to 0.005. These tests cover the lower-attainment argument beyond the author's central-path tests.
- Independently tested the weighted exposed determinant scale at ranks (1,2,3), scales (1,2.5,4), and epsilon=0.03. The weighted rank was 18, Delta was `6.724309078442606`, and the equality-case AM–GM endpoint had exact gap 0.03 to numerical precision. The barrier increase `97.42116740876648` agreed with Q_alpha log(Delta/epsilon).
- Independently formed first, second, and third directional derivatives of the homogeneous product-ball barrier for 180 random points/directions over k=1,2,5 with heterogeneous block dimensions. The maximum normalized third derivative was `0.9999494686861216`, below one; the maximum discrepancy in inverse-Hessian gradient degree k+1 was `4.44e-14`. This checks the nontrivial positive log(t) term numerically while the primary restriction theorem supplies the proof.
- The integrated log reports 45 pages and no warnings, undefined references/citations, or overfull/underfull boxes. I did not launch a conflicting shared build.

## Primary literature and novelty

I checked Nesterov–Todd's local primary Section 5.1, including its explicit feasible gap-set corollary and allowance for intermediate affine infeasibility. I checked the local original-derived NN1994 text at printed page 199, Proposition 5.4.6(i): its spectral-norm-cone formula is algebraically exactly the barrier used here.

I opened and checked [Hildebrand's primary preprint, Corollary 6.2](https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf), which gives the infinity-norm epigraph lower degree n for n>=3 and displays the same scalar homogenized barrier. I also checked [Hauser–Güler's primary Theorem 5.5](https://arxiv.org/pdf/math/0103196), whose coefficients are explicitly at least one. These match the manuscript's hypotheses and attribution. The Faraut–Korányi reference is used for classical algebraic identities that are written explicitly in the proof; the Gouveia–Parrilo–Thomas reference is contextual rather than a substitute for the dimension proof.

The stage is careful about what is classical: projection geometry, constant full speed, the feasible gap-set bound, the product-ball cone barrier, principal-minor algebra, and self-scaled classification. Its potentially original value lies in the exact same-instance comparison and the specified weighted/formulation consequences, rather than rebranding those ingredients. No unsupported broad first-result claim appears in this stage. Final synthesis should preserve these distinctions.

The two sections fit the preceding centrality analysis: primal shortcuts are first separated from feasible dual completion, then the formulation section explains the dependence on the metric and representation. The concrete-formulation proofs are appropriately kept in the appendix. Apart from the two minor corrections above, I found no required correctness, completeness, or readability change for Stage 4.
