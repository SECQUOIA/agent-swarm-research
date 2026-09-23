# Stage 4, round 1, independent review 1

**Verdict: no major or minor issues identified.** I independently checked all three new sections, including the exact optimized Gaussian phase-loss theorem and the optimization over arbitrary physical composite energies. The stated conclusions follow under their explicit assumptions. The new results should still be distinguished from an exhaustive literature-priority determination.

## Scope and checks performed

I read `sections/gaussian-geometry.tex`, `sections/boundary-and-smooth.tex`, and `sections/capillarity-diagnostics.tex` in full, their relevant earlier theorem dependencies, their integration in `main.tex`, and the bibliography changes. I inspected `code/check_stage4.py` and ran it successfully. I read the author record after working through the new proofs; its statements about prior coordinator checking were not treated as verification. I did not read other Stage 4 round 1 reports, edit the manuscript, or delegate.

I also inspected the retained Challa–Hetherington primary text. Its finite-bath Gaussian-ensemble construction supports the limited historical attribution made here. I did not conduct an exhaustive independent novelty search.

## Scalar Gaussian results

Completion of squares gives exactly the component means, common shrunken variance, and logistic phase weight displayed in the manuscript. The necessary scale follows from more than phase-population matching: because each transformed component has no larger width than a target component and the phase separation diverges in standardized units, the two target windows require two distinct transformed components. Their ordering fixes their identification. Convergence within the individual windows forces the common variance ratio to one and both standardized shifts to zero. Subtracting the shifts gives `k_N r_N -> 0`.

For a finite crossover, this scale product has a finite limit while `r_N` diverges, so the variance correction vanishes. If both transformed weights have positive subsequential limits, the logistic equation forces `b_N=O(1/r_N)` and hence preserves the two opposite limiting translations. The limiting weighted-normal TV objective is convex in the transformed weight and symmetric under reflection, so balance minimizes it. If one transformed weight vanishes, its surviving bounded-width Gaussian cannot recover both separated target phases; the error is at least one half. For a positive crossover parameter, the field `t_N=kappa_N m_N` exactly aligns the upper component and gives asymptotic complete selection of it. Thus both branches of the optimized formula are attained, and the changeover value is correct.

The untuned asymmetric prescription has the stated odds shift. Its extra `m_N^2` condition is necessary because its nonzero fixed factor `2w-1` changes the phase weights; it is also sufficient for the mean and covariance changes. The manuscript correctly specifies which reference mean defines that calibration.

## Multivariate classification and component matching

The covariance, transformed means, phase scores, and affine invariant agree with direct multivariate completion of squares. For the necessity proof, macroscopic covariance is at most `I/N`; every positive-weight target atom must therefore receive a distinct transformed component. A limiting bijective map of the finite phase set has the form `e -> s e+a`, with `0<=s<=1`. Comparing the finite set's positive diameter forces `s=1`, and comparing its arithmetic centroid forces `a=0`. This rules out an overlooked component permutation or a translating configuration that reproduces the same finite point set.

Once labels match, the isolated Gaussian shapes give the stated standardized mean-displacement condition. Subtracting the conditions for two different phase points yields the `N^(3/2)` necessary scale. Exact phase-weight restoration is equivalent to the affine representability of the squared radii, which is precisely the cosphere equation. If the equation fails, the nonzero affine dependence in the invariant forces `alpha_N -> 0`. This is equivalent to the stronger `kappa_N N^2 -> 0` condition. The choices of field used to establish both sufficiency directions are correct. The single-phase covariance criterion is also correct.

The anisotropic completion uses `B_N(I+N B_N)^(-1)` rather than the raw curvature as its effective metric. The discussion of a possible nullspace linear term correctly avoids claiming that every semidefinite restoration locus is a cylinder. No unsupported scalar exponent classification is exported to arbitrary anisotropic or unequal-covariance models.

## Exact optimized Gaussian phase loss

I checked the lower bound for unrestricted fields in detail.

- In the stated regime, `s_N -> 1` and `alpha_N=o(sqrt(N))`, while `alpha_N -> infinity`. If `|t_N|` stays bounded below along a subsequence, phase indices whose projection is more than `N^(-1/4)` below the maximizing projection lose a score of at least a fixed multiple of `N^(3/4)`. Their quadratic score differences are only `o(sqrt(N))`, so their weight vanishes. Every remaining transformed center lies beyond the target supporting hyperplane by a fixed positive amount, including when the field norm diverges. Projected Gaussian fluctuations have vanishing macroscopic variance, giving TV tending to one.
- Thus only fields tending to zero can do better. Their transformed components remain near their own macroscopic phase points. If `I` indexes the positive limiting transformed weights, the missing target neighborhoods give error at least `1-sum_(i in I) w_i` independently of any remaining fluctuation distortion.
- Dividing the exact score differences by `alpha_N` gives approximate equalities on `I` and approximate inequalities on every phase index. These form one fixed finite linear feasibility problem. Even with unbounded sphere centers, infeasibility would give fixed Farkas multipliers that contradict the errors tending to zero. The resulting finite feasible center has an empty-sphere contact set containing `I`. Hence its retained target mass bounds the mass of `I` by `W_*`.
- Conversely, fixing any contact-set center and taking the prescribed field preserves all component shapes in TV and conditions the limiting phase weights exactly on that contact set. The maximum retained mass is attained among finitely many possible contact subsets.

These arguments prove equality, not merely the fixed-center upper bound. The three-collinear-point example and the impossibility of discarding only the central point are consistent with the exact affine invariant.

## Physical boundary theorem and compensation

At capacity proportional to `N^(3/2)`, the secant slopes times `sqrt(N)` have limits `+b` and `-b`, and the local curvature times `N` vanishes. An order-`sqrt(N)` change in composite energy changes the endpoint log-weight difference by `D=beta^2 ell d/gamma` and changes neither limiting local slope. The sign and coefficient are correct.

The exponential moment strictly beyond `b` provides the necessary uniform integrability through the concavity tangent bound. It does not infer weighted-integral convergence from weak convergence alone. The secant exceptional-mass hypothesis also controls bounded finite corrections because the maximum log-weight changes by only order one. These controls give both the tilted Gaussian phase laws and the full microscopic likelihood-integral TV formula, including a variance-zero phase.

The stated compensation coefficient makes `D=b^2(v_--v_+)/2`, equalizing the integrated phase factors and restoring the reference phase probabilities. The residual within-phase translations have the stated weighted Gaussian TV loss. Equal variances give the unweighted common translation loss independently of the target phase weights.

## Optimization over arbitrary physical calibrations

The overlap compactness argument rules out a hidden calibration that beats both abandonment and the finite-correction family:

1. A TV limit strictly below both target phase weights implies strictly positive overlap with each positive phase component.
2. Tightness removes fixed-width-window tails from the overlap. The regions where the normalized likelihood is below a sufficiently small fixed number or above a sufficiently large fixed number contribute arbitrarily little overlap; the latter uses `P(R>M)<=1/M`. Hence two feasible selected energies can be chosen within order `sqrt(N)` of their respective centers, with log-likelihood difference bounded by a constant.
3. Solving their exact physical likelihood difference gives the displayed composite-energy formula. The bounded log-ratio changes it by `O(c_N/Delta_N)=O(sqrt(N))` from the secant calibration for those selected points. The Bernoulli-function expansion of that secant calibration has the stated sign and coefficient, and perturbing its endpoints by order `sqrt(N)` perturbs its value by no more than that order.
4. Thus every calibration beating abandonment has a bounded standardized displacement from the original secant calibration. On a further subsequence the boundary theorem applies, giving the convex objective `F(r)`.

For the upper bound, fixed finite corrections realize every interior mixture weight, continuity supplies endpoint infima, and phase-centered globally bounded reservoir weights realize abandonment. The proof correctly applies these bounds to approximate minimizers rather than assuming existence of finite-system minimizers.

The weighted-normal positive-part CDF expression agrees with direct half-line integration. Its derivative is the difference of the two displayed CDFs, is strictly increasing when both limiting variances are positive, and has opposite signs at the endpoints. Equal variances give the target phase weight as the unique interior minimizer. Variance-zero contributions are handled by their positive masses rather than an undefined Gaussian density.

## Microscopic applicability and smooth reservoirs

The mean-field occupation estimate and Gamma transform give every fixed standardized exponential moment for all sufficiently large sizes. The pure-spin disordered variance may vanish, and the measure-form boundary theorem permits this.

For short-range systems with fixed spatial dimension greater than two, every fixed multiple of `N^(-1/2)` eventually lies in the already established cutoff-free `1/L` window. The same second derivative bound and centering estimate therefore give every fixed bond moment, and the binomial transfer gives every fixed spin-energy moment. The small moment already proved also identifies the positive contour phase laws with the midpoint phase laws up to a vanishing conditional TV discrepancy. The surface exceptional exponent dominates `sqrt(N)` precisely in these dimensions. In two dimensions the two explicit sufficient inequalities impose the appropriate large-`gamma` restriction; the manuscript does not claim the boundary law at arbitrary small fixed `gamma` there.

For continuous density envelopes with exponent above one half, the stated tail absorption works after taking a sufficiently large fixed phase-window radius and then large size. Finite corrections have bounded exterior weight because the endpoint slopes retain their signs. At exponent one half, the second absorption ratio need not vanish, as correctly stated.

The smooth-reservoir necessity follows from the strong-concavity chord inequality at three selected good points inside the phase-center interval. Their adjacent distances are order `sqrt(N)` and `N`, giving the mixed scale. The converse is correctly conditional on an attainable endpoint calibration and the previously stated upper curvature and tail assumptions; it is not asserted for arbitrary reservoir entropies solely from their local heat capacity.

## Capillarity and diagnostics

The exact interior formula is the Bernoulli log transform with its linear part removed. Its quadratic and cubic coefficients, signs, and uniform remainder on bounded fractions are correct. Maximizing its leading quadratic part gives the displayed boundary maximal gain.

The capillarity proposition explicitly assumes a compactly supported large-deviation model, so the uniform physical tilt and compact-space Laplace principle apply. When the tilted rate has a strictly negative interior minimum, its minimizing set is separated from both canonical endpoint minima, which yields full TV tending to one. The endpoint-only conclusion above the threshold is correctly limited to macroscopic concentration. At equality, the inability of a rate function to determine tied weights is real and is explained accurately.

The square-torus prescribed rate obeys the stated perimeter lower bound, with equality only at the two endpoints and the midpoint. This proves the threshold and all three minimizer cases, including uniqueness below the threshold. It is not represented as a microscopic Potts Wulff theorem.

The Gaussian density-norm integral, positive fixed TV value, and fixed-bin scaling agree with direct Gaussian integration. The fixed-energy barrier identity cancels normalization exactly. Its physical midpoint value is `c log cosh(beta Delta/(2c))`; the lower and upper bounds on `log cosh` establish the stronger absolute-barrier scale without assuming small curvature first. Relative barrier accuracy is correctly distinguished from full-state TV and from a dynamical transition-rate claim.

## Numerical validation actually performed

`python paper-finite-reservoirs/code/check_stage4.py` passed. The weighted-normal CDF objectives and independent absolute-density quadratures agree to approximately `1e-10` or better in the three supplied cases. The equal-variance root matches the target phase weight. Direct exact-power-law quadrature approaches the predicted unequal-variance compensation and TV limits across the supplied sizes. The square-model inequalities also pass the grid check. These computations support the explicit formulas; the unrestricted-field and arbitrary-calibration theorems were assessed by the analytic arguments above.

No required correction remains from this independent review.
