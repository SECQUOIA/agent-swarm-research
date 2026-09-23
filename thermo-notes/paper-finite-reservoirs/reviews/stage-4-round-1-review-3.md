# Stage 4, round 1 — independent review 3

## Verdict

**No major issues found.** The physical finite-boundary theorem, its optimization over arbitrary composite energies, and its degenerate-Gaussian cases are valid. The Gaussian phase-geometry and capillarity statements are also sound under their explicit model assumptions. I found one minor clarification in the alternative density-envelope argument.

I reviewed all of `sections/gaussian-geometry.tex`, `sections/boundary-and-smooth.tex`, and `sections/capillarity-diagnostics.tex`, together with the stage-1 likelihood/tail tools and the microscopic moment inputs on which the applications depend. I did not read another current-round report, edit the manuscript, or delegate.

## Minor issue

**Include the bounded endpoint offset for finite calibration corrections in the density-envelope argument.** Near the end of `boundary-and-smooth.tex`, the argument states `h_N(E) <= C x/sqrt(N)` after saying that the density assumptions cover both the secant calibration and finite corrections. The displayed inequality applies directly to the secant case. For a finite correction with limiting upper endpoint value `D>0`, it fails at the upper endpoint, where `x=0` but `h_N(e_+) -> D`.

The conclusion is unaffected: explicitly distinguish the secant estimate from the corrected estimate `h_N(E) <= C_0 + C x/sqrt(N)`, where `C_0` is bounded along a fixed correction sequence. The factor `exp(C_0)` does not change weighted-tail convergence. The subsequent exterior bound by a constant is already correct for finite corrections. This is a local clarification of an estimate, not a defect in the boundary theorem or its proof.

## Independent verification of the physical boundary results

### Finite tilts and uniform integrability

For secant calibration with `c_N/N^(3/2) -> gamma`, the endpoint derivatives times `sqrt(N)` tend to `+b` and `-b`, with `b=beta^2 ell/(2 gamma)`. The second-derivative contribution over a fixed standardized window vanishes because `N/c_N -> 0`. A total-energy increment `d_N sqrt(N)` changes the upper-minus-lower endpoint value by `beta^2 ell d/gamma + o(1)`, while changing the standardized endpoint slopes by `o(1)`. This verifies both the sign and scale of the local correction.

The exponential-moment requirement `eta>b` is sufficient. The global tangent inequality bounds the reweighting by a fixed multiple of `exp[(b+epsilon)|X_i,N|]`; choosing a power greater than one below the available moment exponent proves uniform integrability. This controls normalization, conditional weak limits, and the absolute-likelihood integral for full-state TV. It is stronger than merely knowing local Gaussian limits, as needed at a nonvanishing tilt.

The exceptional-mass assumption is sufficient for every bounded correction sequence. With normalization at the lower center, differentiating the maximal log weight with respect to total energy gives `beta_N-c_N/(cal E_N-e_-,N)`, which is `O(N^(-1/2))` in this range. An `O(sqrt(N))` total-energy shift therefore changes the maximal amplification by only an `O(1)` logarithmic amount. The exceptional contribution vanishes under the stated secant assumption.

For a zero variance, the Gaussian limit is a point mass at zero, its exponential tilt has normalizer one and remains the same point mass. Every integral statement continues to be meaningful. No positive density is implicitly required by this proof.

### Compensation and the objective function

The finite correction restoring phase probabilities satisfies

`D = b^2(v_- - v_+)/2`,

so its coefficient of `sqrt(N)` is `beta^2 ell(v_- - v_+)/(8 gamma)`, as stated. The remaining componentwise translation gives the weighted sum of Gaussian TV distances, including zero contribution from a zero variance.

Writing the finite-boundary TV as `F(r)` uses a sum of signed-measure norms on the two asymptotically separate phases. It is correct even though the positive decomposition need not be an exact disjoint partition: the physical likelihood depends only on the actual energy, its absolute integral is linear in the positive decomposition, and macroscopic separation identifies the limiting sectors. Convexity and continuity of `F` follow directly from the norm.

The positive-part CDF formula is correct for either sign of the phase tilt after reflection. Its derivative in the retained mass is the first displayed normal CDF. Thus the derivative of `F` is strictly increasing when both variances are positive, and it has opposite signs at the endpoints. For equal variances, its zero is `r=w_-`; the result does not require equal target phase weights. The separate zero-variance prescription is correct.

### Arbitrary-calibration lower bound

The overlap argument supplies the needed compactness rather than assuming that an optimizer lies near secant calibration. If total TV stays strictly below both phase weights, each phase has a fixed positive overlap with the reweighted law. Removing a sufficiently large fixed standardized tail, very small likelihood values, and very large likelihood values leaves positive overlap in each phase. The large-likelihood removal uses `P(R>M) <= 1/M`, since the normalized likelihood integrates to one. This justifies selecting feasible phase-window points with likelihoods in a common interval `[epsilon,M]`.

At the two selected points, their log-likelihood difference is bounded. Solving the exact endpoint equation gives the stated total-energy formula. Its sensitivity to this bounded log difference is `O(c_N/D_N)=O(sqrt(N))`. The secant expansion

`c_N/beta_N + (x_N+y_N)/2 + beta_N(y_N-x_N)^2/(12c_N) + O(D_N^4/c_N^3)`

is uniform on the selected windows. Moving the endpoints by `O(sqrt(N))` changes it by `O(sqrt(N))`; the remainder here is smaller. Thus every such low-error sequence has a bounded correction parameter and a subsequence covered by the boundary theorem.

The upper bounds obtained by centering the reservoir maximum at one phase are also valid under the same positive decomposition: the selected phase sees a weight tending to one, the opposite phase a weight tending to zero, and the exceptional mass cannot be amplified because the centered weight is at most one. The retained phase is reproduced in the limit and the error is exactly the discarded phase weight. Combining these bounds with the overlap compactness proves the optimization over all admissible total energies, including choices near a cutoff or very far from secant calibration. Approximate minimizers suffice; existence of a finite-size minimizer is not assumed.

### Microscopic boundary applications

The mean-field lattice-Gaussian bound gives every fixed absolute exponential moment on the standardized energy scale, and the Gamma contribution has the same property. Thus every positive gamma is allowed, including the pure-spin degenerate disordered phase.

For fixed spatial dimension greater than two, every fixed multiple of `N^(-1/2)` eventually lies in the cutoff-free contour window of width proportional to `L^(-1)`. The established restricted second-derivative estimate therefore gives bond moments at every fixed standardized parameter; the already proved binomial transfer gives spin-energy moments. The exponentially small mismatch with the midpoint phase events identifies the contour conditional weak limits. The exceptional surface cost dominates `sqrt(N)` for all these dimensions.

In dimension two the manuscript correctly requires both a sufficient moment coefficient and a sufficient exceptional surface constant. The strict inequalities displayed in the paper imply the boundary theorem for all sufficiently large gamma, but do not imply it for all gamma. No unsupported all-gamma short-range claim is made.

## Other stage claims checked

### Smooth entropy curvature

The curvature/heat-capacity relation has the correct units and sign. The good-point proof selects three feasible energies entirely between the phase centers, so its curvature lower bound is used only where assumed. Strong concavity gives the quadratic chord defect with factor `(y-x)(z-y)/2`, forcing `kappa_N N^(3/2) -> 0`. The sufficiency comparison correctly adds endpoint calibration, global concavity, and tail control rather than treating positive heat capacity alone as sufficient.

### Exact Gaussian geometry

I checked the scalar completion of squares, logistic weights, balanced crossover, and the alternative pure-phase calibration. In the finite-crossover regime, retaining two positive weights forces the field on the inverse-separation scale, while a disappearing component cannot cover both separated target windows. This gives the stated optimized minimum. The untuned asymmetric calibration requires the stronger squared-gap scale through its exact phase odds.

The vector completion of squares and affine invariant are correct. Any limiting bijection of the finite phase set by a positive scalar contraction plus translation must have contraction one and translation zero. The component shapes then impose the `N^(3/2)` condition. The phase-weight restoration equations are precisely the cosphere equations, and a violated affine relation forces the stronger `N^2` condition.

For optimal phase loss, nonvanishing or unbounded fields push the dominant components beyond a supporting plane of the original phase set, so their TV tends to one. If the field tends to zero, the positive limiting weight set satisfies a limiting finite system of affine equalities and inequalities. Farkas' alternative justifies exact feasibility even if the inferred sphere centers escape. Therefore that set lies in an empty-sphere contact set, proving the claimed lower bound. The common effective metric for the anisotropic algebra is `B_N(I+NB_N)^(-1)`, as stated; no unwarranted general exponent classification is inferred from it.

### Capillarity and diagnostics

The exact interior physical gain and its cubic expansion have the correct signs. At the boundary scale the quadratic term is of order `sqrt(N)` and the cubic term may remain order one, as stated. The capillarity proposition assumes its rate function rather than deriving it for the microscopic Potts model. On the fixed compact support, the cutoff eventually lies outside the support and the scaled log likelihood converges uniformly to the bounded quadratic tilt. The exponential-tilting proof of the new rate function is valid. Below the threshold its minimizing set stays away from the original endpoint minimizers, giving TV tending to one. The text correctly declines to infer tied-minimizer weights from a rate function.

For the square-torus model, the inequality `I(theta) >= 8 tau theta(1-theta)` is sharp exactly at the two endpoints and the midpoint. It gives the stated threshold and minimizer classifications. The model's isotropic circular branch is not represented as a derived lattice Wulff law.

The Gaussian density `L^2` norm, scale-invariant TV expression, and fixed-width histogram scaling agree with direct Gaussian integration. The fixed-energy barrier shift cancels normalization exactly. The physical midpoint gain is `c log cosh(beta Delta/(2c))`; its vanishing is equivalent to `c >> Delta^2`, including sequences outside the local quadratic regime. The relative barrier comparison explicitly assumes `c >> Delta` and distinguishes a fixed density ratio from a dynamical transition rate.

## Verification scope

The review used analytic rederivations and stage-dependency checks. I did not use numerical agreement as evidence for the arbitrary-calibration compactness or uniform-integrability arguments. Apart from the bounded additive constant in the alternative density proof, I found no substantive gap, hidden positivity requirement, degenerate-measure error, or unsupported microscopic application in this stage.
