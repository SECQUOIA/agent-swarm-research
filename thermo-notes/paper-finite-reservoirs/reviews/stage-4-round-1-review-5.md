# Stage 4, round 1: independent review 5

**Verdict: no major issues identified. Two minor corrections are needed.**

I reviewed all of `gaussian-geometry.tex`, `boundary-and-smooth.tex`, and `capillarity-diagnostics.tex`, including the earlier microscopic and general-threshold results used by the new arguments. I did not edit manuscript files, consult other current-round reviews, or delegate. In particular, I independently checked the two new global optimization proofs rather than assuming bounded calibrations or bounded sphere centers.

## Minor findings

### 1. Include degenerate level sets in the semidefinite classification

**Location:** final paragraph of `gaussian-geometry.tex`, the statement that a semidefinite effective metric gives an elliptic cylinder when its linear coefficient is in its range.

The algebraic effective metric is correct, but positive semidefiniteness permits zero-radius and rank-zero cases. For example, take `M=diag(1,0)`, zero linear coefficient, and phase points `(0,0)` and `(0,1)`. The restoration locus is `x_1^2=0`, namely an affine subspace rather than a nondegenerate elliptic cylinder. With `M=0`, a nonzero linear coefficient gives a hyperplane; a zero coefficient can give the whole space. These cases are allowed by the stated matrix assumptions.

**Fix:** Qualify the cylindrical classification as “possibly degenerate,” explain that zero-radius cases give affine subspaces, and briefly handle rank zero. The paraboloid statement can likewise mention flat directions if the nullspace has dimension greater than one. No exponent theorem or effective-metric formula needs changing.

### 2. Add the bounded endpoint constant in the density-envelope boundary argument

**Location:** final paragraph of `boundary-and-smooth.tex`, the interior estimate `h_N(E) <= C x/sqrt(N)` in the alternative continuous-density argument.

That estimate is valid for the secant residual normalized to zero at both endpoints. The paragraph also treats finite calibration corrections, for which the endpoint values approach `0` and `D`; if `D>0`, the displayed bound fails at the upper endpoint because `x=0` there.

**Fix:** State the general bound as `h_N(E) <= C_0 + C x/sqrt(N)` for bounded correction parameters, with `C_0=0` available in the secant case. The constant only multiplies the weighted tail bound by a fixed factor, so all conclusions and scale comparisons remain valid. The separately stated exterior constant bound is already sufficient.

## Verification of the exact Gaussian results

- Recomputed the scalar square completion, logistic phase weights, transformed means, and variance. All signs and scale factors agree.
- The scalar convergence criterion follows from component isolation in separated fluctuation windows. At finite crossover, any nondegenerate limiting pair of transformed weights forces the standardized field to vanish; convexity and reflection then minimize the two-phase error at equal weights. A vanishing transformed phase weight costs at least one half. The field `t=kappa m` exactly aligns the retained upper component and reaches the one-phase bound when the finite crossover parameter is positive. Thus the displayed infimum limit does address arbitrary approximate minimizers.
- The prescribed tangent-at-canonical-mean calibration with unequal phase weights changes the log odds by the stated amount. Shape matching followed by weight matching yields the stronger quadratic-gap criterion; its dependence on that specified calibration is explicit.
- In the vector model, the transformed means, covariance, weights, and affine invariants follow from exact square completion. Full convergence forces a bijection between target and transformed macroscopic components. A positive homothety carrying a finite set of positive diameter onto itself has scale one and zero translation, so a hidden label permutation cannot invalidate the subsequent shape and weight argument.
- The sphere equation is exactly the solvability condition for restoring all phase scores. Failure supplies the displayed nonzero affine invariant and forces the quadratic scale. The one-phase covariance criterion and the two-or-more-phase fluctuation criterion are consistent with the component formulas.

### Global Gaussian phase-loss optimum

I checked both potentially delicate cases in its lower bound.

1. If the field norm is bounded below on a subsequence, the linear score loss outside a shrinking exposed band is of order at least `N^(3/4)`, whereas the quadratic score differences are `o(sqrt(N))`. The surviving transformed means lie beyond every target mean in the field direction by a fixed positive macroscopic displacement. Projected Gaussian concentration then gives total variation tending to one, including for unbounded fields.
2. If the field tends to zero, the means still approach their own macroscopic phase points even when their fluctuation-scale displacements diverge. Missing target phases therefore give the stated lower bound. Positive limiting transformed weights imply approximate equal-score constraints and upper-score inequalities for a fixed finite linear system. Farkas' alternative rules out an infeasible limiting system with residuals tending to zero, without requiring the candidate centers to remain bounded. Hence every positive limiting support is contained in a finite empty-sphere contact set.

The fixed-center construction attains conditioned reference weights on each contact set while preserving component shapes. It matches the lower bound and proves the claimed equality. The three scalar-point example and the statement that the central phase cannot be the sole discarded phase follow correctly.

The anisotropic square completion uses `B_N(I+NB_N)^{-1}` in the score quadratic, not `B_N`; this is correct. The manuscript does not overextend the scalar exponent classification to arbitrary anisotropic sequences. Only minor finding 1 concerns its geometric wording.

## Verification of smooth and exact physical boundary results

- Differentiating the stated entropy convention gives `-h''=beta_B^2/(C_B/k_B)`. The curvature necessity proof selects good feasible energies wholly inside the center interval and uses a strong-concavity chord with the correct sign and product of gaps. Its necessity is independent of an endpoint calibration. The converse explicitly retains the required upper-curvature, concavity, feasibility, and tail assumptions.
- At `c_N ~ gamma N^(3/2)`, the secant endpoint slopes multiplied by `sqrt(N)` converge to the two signed finite tilts. A correction of order `sqrt(N)` in total energy produces the displayed finite difference between endpoint log weights and does not change those limiting slopes.
- The strict exponential-moment margin above the tilt coefficient provides an actual `L^p` bound for some `p>1`, not just tightness. This justifies normalizer, tilted weak-law, and full total-variation limits. The exceptional-mass condition remains valid under bounded corrections because the normalized maximal log gain changes by only order one.
- The formulas allow zero Gaussian variance as a point mass. The phase-population compensation coefficient has the correct sign and factor, and compensation leaves exactly the weighted Gaussian translation error stated in the corollary.

### Optimization over every physical composite energy

The proof does not merely optimize finite secant corrections. If an arbitrary calibration has limiting TV strictly smaller than either discarded phase weight, both phases retain positive overlap with the target. Removing the small-likelihood set, the large-likelihood set, and fluctuation tails still leaves good feasible points in both phase windows. The exact ratio at these two points constrains the calibration to within order `sqrt(N)` of their secant calibration. Expanding the latter and moving its endpoints shows that it is also within order `sqrt(N)` of the prescribed secant calibration. A bounded-correction subsequence then falls under the boundary theorem. All other subsequences already obey the one-phase lower bound.

The one-phase centered choices attain the two discarded-mass upper bounds using their global bounded weights. Finite corrections realize every strictly positive limiting phase-weight pair; continuity supplies the endpoints in the optimization without exchanging uncontrolled limits. These bounds establish the stated global infimum limit. The proof does not assume existence of finite-size minimizers.

I also rederived the scalar CDF expression for the two weighted Gaussian positive parts and its derivative. When both variances are positive the derivative is strictly increasing and changes sign, so the minimizer is unique. Equal variances yield `r=w_-`, including unequal canonical phase weights. The zero-variance conventions are consistent with the finite-measure objective.

### Microscopic applicability

The mean-field bounds provide every fixed exponential moment and have no exceptional component, including for pure spins. For fixed spatial dimension greater than two, every fixed multiple of `N^(-1/2)` eventually fits into the proved cutoff-free `1/L` window. The restricted log-partition derivative bounds and binomial transfer then supply every fixed physical-energy moment coefficient. The positive contour and midpoint phase laws have vanishing symmetric-difference probability through their small exponential moments and the tunneling bound, so they share the weak Gaussian limits. Surface suppression dominates the boundary gain for these dimensions. In dimension two the two explicit strict inequalities correctly retain both the moment and exceptional-mass margins; the manuscript makes no unsupported assertion for smaller capacity coefficients.

The continuous-density alternative also works after minor correction 2: a large fixed fluctuation cutoff absorbs the linear gain into the Gaussian cost, and `alpha>1/2` absorbs it into the interfacial cost. The order of limits is appropriate.

## Verification of capillarity and diagnostics

- Expanding the exact Bernoulli log transform gives the stated quadratic and cubic terms, including the sign of the cubic term. The uniform expansion gives the normalized maximal gain and the competing surface scale.
- The capillarity proposition expressly assumes a compactly supported large-deviation model. The normalized log tilt converges uniformly on that compact set and its cutoff is eventually beyond the set. Bounded continuous exponential tilting therefore gives the displayed rate function. Below the proposed threshold the minimizing set is separated from both canonical endpoints, yielding TV tending to one; above it the statement correctly stops at macroscopic rate minimizers.
- The discussion of tied minimizers identifies a real limitation of a rate function: subexponential factors can affect their weights while preserving the same rate. It does not claim fluctuation or phase-probability conclusions from the LDP alone.
- The square-torus perimeter inequality, its equality points, the threshold factor, and the unique midpoint minimizer below threshold are correct for the explicitly defined isotropic variational model. That model is not attributed to a derived lattice Wulff law.
- Direct Gaussian integration gives the displayed density `L^2` expression and the fixed positive TV expression. The fixed-bin-width Riemann-sum scaling is consistent with these formulas.
- The fixed-energy barrier ratio cancels the normalizer exactly. At the midpoint the physical residual is exactly `c log cosh(beta Delta/(2c))`. Its vanishing is equivalent to the stated quadratic-gap capacity condition, including arbitrary positive capacity sequences. The relative-barrier comparison retains its stated large-capacity assumption and does not claim dynamical-rate accuracy or identify a shifted saddle.

No numerical calculations or new source searches were necessary for these analytic checks. Planned introduction, figures, and final prior-art synthesis are not treated as omissions in this stage review.
