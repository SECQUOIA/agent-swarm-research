# Stage 4, round 1 — independent review 4

## Verdict

**No major or minor issues identified.** The exact Gaussian results, physical boundary law and its optimization, and the stated capillarity and accuracy diagnostics are mathematically consistent under their written hypotheses. The distinctions between exact probability models, microscopic theorems, specified calibrations, and conditional capillarity conclusions are maintained.

I independently reviewed `sections/gaussian-geometry.tex`, `sections/boundary-and-smooth.tex`, and `sections/capillarity-diagnostics.tex`, along with their earlier theorem dependencies, the manuscript inclusion and reference entries, and `code/check_stage4.py`. I did not read other current-round reports, edit the manuscript, or delegate. The numerical checks described below were performed separately from the author's checker.

## Gaussian calculations and calibration geometry

### Scalar crossover

Completion of squares gives the displayed means, variance, and logistic weight. At finite `kappa_N m_N s_N -> a`, the within-phase variance correction vanishes because `m_N/s_N -> infinity`. Both surviving phases can have positive limiting weights only when the rescaled field is of order `s_N/m_N`. Their standardized translations therefore remain the opposite shifts of magnitude `a`. The limiting TV is convex in the surviving upper-phase weight and reflection-symmetric, so balance minimizes it in that class.

If one phase loses all weight, a single component of bounded standardized width cannot cover both separated target windows, giving error at least one half. The field `t_N=kappa_N m_N` aligns one component exactly and selects it when `a>0`, attaining that bound. Thus the optimized crossover and the switch at `2 Phi^{-1}(3/4)` are correct. The necessity argument also covers large curvature or escaping fields through component-window mismatch.

For unequal phase weights, the specified tangent-at-reference-mean prescription gives the stated additional odds term. Its stronger `kappa_N m_N^2 -> 0` requirement follows once the necessary variance condition has been established. The comparison does not silently replace the specified reference mean by a self-consistent modified mean.

### Several quantities and empty-sphere geometry

The multivariate completion-of-squares formulas and affine weight invariant are correct. TV convergence requires a bijection between separated macroscopic components. A limiting homothety mapping a finite positive-diameter set onto itself has scale one and translation zero, so a hidden permutation cannot evade the shape argument. Subtracting the standardized mean displacements gives the `N^(3/2)` curvature condition. Exact weight restoration is equivalent to the printed cosphere equation; when it is insoluble an affine dependence detects the nonzero squared-norm discrepancy and forces the stronger `N^2` condition.

The phase-loss upper bound follows by fixing an empty-sphere center and retaining its contact set. For the lower bound, fields bounded away from zero push the selected macroscopic mass beyond a supporting hyperplane of the target set, and the resulting TV tends to one. For fields tending to zero, only their own phase neighborhoods can receive components. The limiting positive-weight set satisfies the approximate finite linear equality/inequality system displayed in the proof.

The appeal to Farkas' alternative is legitimate even for unbounded candidate centers: an infeasible fixed linear system has a strict separating certificate with fixed multipliers, which is incompatible with errors tending to zero. Consequently that positive-weight set is contained in an actual finite empty-sphere contact set. This supplies the needed lower bound and does not assume bounded optimizing centers.

The anisotropic formulas use the correct effective matrix `B_N(I+NB_N)^{-1}`. The discussion only asserts finite-size algebra and explicitly withholds an unsupported general anisotropic exponent classification.

## Physical boundary law and optimized error

### Curvature and finite calibration

The smooth-reservoir curvature has the correct entropy and heat-capacity sign. In the necessary result, the selected three feasible energies lie inside the center interval, and the quadratic chord defect has magnitude proportional to `kappa_N N^(3/2)`. The comparison with sufficient criteria retains the endpoint-calibration and tail/feasible-neighborhood hypotheses.

At `c_N/N^(3/2) -> gamma`, the physical endpoint slopes times `sqrt(N)` tend to `+b,-b`, with `b=beta^2 ell/(2 gamma)`. The correction `d sqrt(N)` changes the endpoint log-likelihood difference by `beta^2 ell d/gamma`, while its effect on the standardized slopes vanishes. The required exponential moment has coefficient strictly greater than `b`; this is sufficient to bound a power greater than one of the reweighting factor. The exceptional-mass hypothesis is applied to the actual secant maximum, and a bounded calibration correction changes that maximum by only a bounded amount.

The resulting phase probabilities and tilted Gaussian means follow, including a phase variance equal to zero. The full microscopic TV formula is a likelihood integral obtained through uniform integrability, not an unsupported inference from weak convergence.

### Compensation coefficient

Equating the two integrated phase factors requires

`D = b^2(v_- - v_+)/2`.

Since `D=beta^2 ell d/gamma`, this gives exactly

`d=beta^2 ell(v_- - v_+)/(8 gamma)`.

The remaining conditional translations yield the weighted Gaussian TV sum. Matching integrated phase weights is correctly distinguished from matching the phase fluctuations and from exact finite-size calibration.

### Arbitrary-calibration compactness

The optimized physical boundary proof covers every admissible composite energy, rather than just bounded secant corrections. If TV stays strictly below both target phase weights, each positive phase component retains positive overlap. Tightness and lower/upper likelihood cuts produce two feasible energies in fixed standardized phase windows, with their normalized likelihoods bounded above and below. This selection remains valid for positive overlapping phase decompositions.

The exact two-point likelihood equation gives the stated composite-energy formula. A bounded log-ratio changes the associated secant total energy by `O(c_N/Delta_N)=O(sqrt(N))`. The secant expansion and its response to endpoint movements show that these arbitrary calibrations are bounded corrections to the original secant calibration. A subsequence therefore falls under the proved finite-correction boundary law. The complementary sequences already have at least the discarded-phase error. Single-phase centered calibrations attain the two additional bounds using globally bounded weights, independently of the exceptional-tail amplification issue. This establishes the printed minimum formula without assuming finite-size minimizers exist.

### Normal CDF and root calculation

For one phase with standardized shift magnitude `d_i>0`, solving the weighted-density crossing gives the positive-part mass

`r_i Phi(log(r_i/w_i)/d_i + d_i/2) - w_i Phi(log(r_i/w_i)/d_i - d_i/2)`.

This holds for either sign of the Gaussian translation. The two phase contributions sum to `F(r)` because their total signed mass is zero. The limits at zero assigned phase weight and at zero variance are handled correctly. Differentiation cancels the crossing-density terms and gives the stated difference of CDFs. It is strictly increasing when both variances are positive, with opposite endpoint signs. Equality of the CDF arguments is therefore the unique root condition. Equal variances give `r=w_-`, including unequal target weights, and the simplified global optimum follows.

### Microscopic range of the boundary theorem

The mean-field occupation estimate supplies every fixed standardized exponential moment, so arbitrary fixed boundary tilts are allowed. In short-range dimension greater than two, every fixed `1/sqrt(N)` temperature shift eventually lies inside the established `1/L` cutoff-free interval, and the existing second-derivative and bond-to-spin estimates give every fixed moment parameter. The contour and energy-midpoint conditional laws agree asymptotically because the small moment already suppresses opposite macro-phase contamination.

The interfacial exceptional exponent dominates `sqrt(N)` for dimension greater than two. In dimension two the manuscript retains the two strict coefficient inequalities needed for moment control and exceptional-mass suppression. It does not claim the boundary law for all small fixed capacities there. The alternative density-envelope argument at exponent greater than one half controls the actual weighted tails; finite corrections preserve bounded exterior weights by the endpoint slope signs.

## Capillarity and diagnostics

The exact interior physical weight is correct. Expanding its logarithm gives the cubic coefficient `theta(1-theta)(2theta-1)/6`, with the correct sign. The expansion is uniform on fixed bounded phase-fraction sets when the physical cutoff moves beyond them. The maximal leading gain and the surface-balance scale follow.

The capillarity proposition uses an explicit compact-space LDP and a uniformly convergent bounded tilt. Its reweighted rate and normalization shift follow from the Laplace principle. Above the threshold only endpoint rate minimizers remain; below it the minimizing set lies strictly away from the endpoints and gives TV tending to one. The lack of tied-minimum weights at equality is correctly described as nonidentifiability from an LDP, rather than asserted to be determined.

For the square-torus model, I checked `I(theta)>=8 tau theta(1-theta)` for all three prescribed branches. The droplet inequality is strict away from its endpoint because `16/(3 sqrt(3)) < 2 sqrt(pi)`; the slab gives equality only at one half. This proves the listed critical coefficient and all three minimizer regimes, including uniqueness below the capacity threshold. The model is explicitly not claimed as a derived lattice Wulff law.

The Gaussian density `L2` norm and fixed-bin histogram scaling have the correct normalization factors. The midpoint physical gain is exactly `c log cosh(beta Delta/(2c))`. Its global lower bound by a constant times `min(Delta^2/c,Delta)` proves the absolute-accuracy equivalence, including capacities outside the Taylor regime. Relative accuracy uses the stipulated barrier size and `c >> Delta`. The statements concern fixed-energy density or mass ratios, and do not claim saddle relocation or dynamical rate accuracy.

## Additional numerical checks

1. With 70-digit arithmetic, I evaluated the exact interior gain at phase fractions `0.2` and `0.7`. After subtracting both displayed quadratic and cubic terms, division by the fourth power of the small bath-gap parameter stayed bounded and approached finite values as the parameter decreased through `0.1,0.03,0.01`. This independently checks the cubic sign and remainder order.
2. The midpoint expression from the exact interior formula agreed with `log cosh(q/2)` at `q=0.1,1,10` to approximately `1e-71` or better before multiplication by capacity.
3. Using `beta=2.3`, `ell=0.8`, `gamma=1.7`, and phase variances `0.2,0.8`, I evaluated the exact power-law endpoint log ratio under the printed compensation. Its values at `N=100,10000,1000000` were approximately `-0.46642224,-0.46480410,-0.46478798`, approaching the predicted `-0.46478782`. The standardized endpoint slopes simultaneously approached `+/-1.24470588`. This checks the compensation with non-unit inverse temperature and non-unit latent heat.

The author's checker separately contains direct Gaussian CDF/quadrature comparisons and finite physical-weight integrations. I inspected that implementation and found its formulas and stated checks consistent with the manuscript. Numerical checks were not used to replace the proof of the optimized infimum or the geometric lower bound.

## Scope

This report verifies the stated mathematics and its use of earlier results. It does not certify bibliographic priority for the Gaussian geometric classification or other new claims. The final whole-paper review should assess how much of this material belongs in the main text versus appendices, but that editorial choice is not a mathematical defect in this completed stage.
