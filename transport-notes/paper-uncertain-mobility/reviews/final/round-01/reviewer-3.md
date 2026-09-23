# Independent final manuscript review — reviewer 3

Snapshot: `e5a8cd3e390d1b7afa16481b35bcd01944a8111bce55e2ffaf1570f40ebc899d`.

## Verdict

**No major issues and no remaining valid minor issues identified.** I recommend acceptance of this manuscript at this review round. This is a fresh assessment of the connected argument and final presentation, not an inference from stage approvals. It does not certify exhaustive priority against all literature or promise that an external referee will have no suggestions.

I checked the complete manuscript, its cross-section assumptions, the reproducibility implementation and its two repository dependencies, the supplied numerical evidence, and the scope of the literature comparisons. I did not read other reviewers' reports, coordinator checks, or prior adjudications, and did not delegate. All 28 files match the frozen manifest, including a second hash check during final numerical verification. I wrote no manuscript, figure, data, or implementation files.

## Whole-paper mathematical assessment

### Physical meaning, rough coefficients, and transfer of optimal values

Sections 1–2 and the discussion use the same physical problem: a fixed channel, positive fixed transverse diffusivity, fixed affinity, zero wall axial drift, a nonzero fixed mean speed, and a quenched exchange pattern. The invariant weights, the formula for the mean speed, and the factor `chi = K V^2/(A+KP)` are mutually consistent. Proportional adsorption and desorption preserve the stationary weights when the pattern changes. The dimensionless wall budget is correctly distinguished from its physical counterpart: diffusivity scales with rate times length squared, its wall integral with rate times length cubed, and the scalar response with length divided by rate. Multiplying the dimensional scalar response by the dimensional `chi` gives an axial diffusivity.

The paper does not identify an arbitrary nonnegative `L^1` coefficient with a well-defined diffusion without an additional condition. It explicitly separates the scalar smooth-test supremum from the minimal closed physical realization. This distinction matters for pathological weighted derivative forms. A positive floor supplies closability and the necessary coercivity even without an upper diffusivity bound. The weighted anchor on the reaction controls constants uniformly; it is not being replaced by an unjustified pointwise lower bound on the rate.

The spectral argument yields the stationary long-time variance coefficient as an extended nonnegative quantity. It handles spectral mass at zero and does not silently assume a central limit theorem or ergodicity for every degenerate design. Nonnegative, integrable molecular axial diffusivity contributes through the separate quadratic-variation term. The independence and stationarity assumptions used for this addition are stated.

I checked the Schur reduction with the signs of the wall forcing and the trace term. The lower bound is `D_flow >= chi J`. When the scalar source is bounded in the energy norm, completing that energy space justifies the response vector and square completion even if an `L^2` scalar inverse has not been established. In particular, there is no subtraction of two infinite energies. The boundary load has fixed mass, and the logarithmic remainder follows from its Fourier `H^{-1/2}` norm: low frequencies are bounded by the mass, high frequencies by the `L^2` estimate, with the cutoff proportional to the load's `L^infinity` bound. This gives logarithmic growth without requiring bounds on derivatives of the design.

The mixing argument preserves the exact budget and the observation used by a policy. The two treatments of moments, Minkowski for `q >= 1` and subadditivity for `0 < q < 1`, are appropriate. A root-bump lower bound on a fixed positive-probability part of the cosine ensemble applies to every field, including a field selected with information. It supplies the growth needed to make the logarithmic bulk correction negligible uniformly over observation laws and over budget-dependent binning. Thus later scalar sharp constants really transfer to the physical infima; the paper does not require a uniform bulk remainder for every unmixed degenerate competitor.

Measurability is also treated at the correct level. A countable family of smooth tests gives a Borel scalar response. Policies are Borel maps into `L^1` and use the full budget for every observation. Neither the oracle proof nor the bin proof relies on an unproved measurable selection from pointwise minimizers.

### Local response and the uniform-design baseline

The whole-line source problems are energy-dual problems, not formal inverses of a constant `L^2` source on the line. The quadratic and quartic coercivity and tail estimates justify exhaustion with both Dirichlet and Neumann endpoints. In particular, Neumann endpoint freedom does not introduce an uncontrolled source contribution at infinity. Compact parameter convergence and source tails are used together, rather than asserting an equivalent uniformly over an unbounded parameter set.

My independent scaling checks give:

- Quadratic reaction `a x^2`: response `C_0 epsilon^(-1/4) a^(-3/4)`.
- Quartic pair `(b x^2-t)^2`: length `(epsilon/b^2)^(1/6)`, parameter `t/(epsilon b)^(1/3)`, response `epsilon^(-1/2) b^(-1) C_pair`.
- Positive pair tail: `(C_0/sqrt(2)) mu^(-3/4)`; negative pair tail: `(pi/2)|mu|^(-3/2)`.

These agree with the operator, source, and probability Jacobians in the text. The harmonic constant agrees with the integrated Mehler kernel and gamma-function expression.

The separated-root statement allows the root separation to shrink with diffusivity. Its condition is the necessary relative separation `epsilon/t^3 -> 0`; the proof chooses a shrinking relative neighborhood whose rescaled extent nevertheless diverges. This resolves a potentially important joint-limit failure of fixed-neighborhood arguments. The compact fold limit and the global envelopes are kept distinct. The critical logarithmic coefficient is extracted by a retained region with exponent less than `1/3`, followed by an estimate uniform in that exponent for the omitted region. The exact factor `t(2-t)` is retained where needed. There is no unsupported interchange of the fold cutoff with the small-diffusivity limit.

The uniform thresholds, beta-function constant, critical coefficient, and supercritical pair integral have the correct factors for two folds and the uniform density `1/4`. The limiting random response has an atom from root-free samples, while the finite-diffusivity responses have finite moments. The distinction between disorder fluctuations and displacement statistics in a fixed channel is maintained throughout.

The refined flux identity also has the correct reaction-derivative sign. Its uniform bounds lead to convergence of the boundary forcing, and hence to the finite bulk correction, without asserting uniform convergence of the scalar corrector itself. The fixed-profile Neumann problem has the correct compatibility condition.

Finally, the Gaussian amplitude-collapse example is a real obstruction to extrapolating the local root statistics: the constant trial produces an inverse squared-amplitude lower bound whose mean diverges. It lies outside the uniform anchor assumption. The Rice discussion does not turn a one-point Palm tail into independence of zeros or a stable-sum assertion.

### Predetermined design: arbitrary competitors and all three regimes

The convexity needed for symmetry reduction holds for every positive moment order. It follows from the smooth-test quotient representation and negative powers of the affine energy; it does not require `q >= 1`.

The moving-root shell lower bound averages local gradient costs before applying the negative-power inequality. Consequently it applies to concentrated, rapidly oscillating, or partially vanishing `L^1` designs. At criticality, the shell resource sum gives the additional power of the logarithm. A fold bump gives the supercritical power independently of any proposed profile.

For the sharp subcritical coefficient, I checked the tangent construction's source, reaction, derivative, and root-density factors. The two roots contribute twice to the response but are counted correctly when the parameter integral is converted to an arclength integral. The averaged gradient kernel is bounded in supremum norm, so an arbitrary competitor cannot defeat the certificate by placing its mass on a small set. The equality of the limiting kernel weight is exactly the allocation condition yielding

`alpha_q = (6q-4)/(q+4)`.

The integrability threshold `alpha_q = 1` is `q = 8/5`. The rounded recovery profile has an integrable parameter envelope throughout the stated subcritical range, including `4/3 <= q < 8/5`, where the uniform-design envelope would fail.

At criticality the lower certificate is uniform on retained root positions down to `M^b`, `b < 1/7`. The upper construction resolves the inner radius and the additional logarithmic normalization separately. The core and omitted annuli are smaller than the leading logarithmic term. Independent balancing gives `r^7 log(1/r)` of order `M`, and the resulting moment is `M^(-2/5) log(1/M)^(7/5)`, consistent with the exact coefficient in the theorem.

The supercritical coefficient requires more than order bounds, and the measure-relaxation argument addresses this. Singular mobility measures are removable in this one-dimensional smooth-test problem: flattening test derivatives near a singular set can eliminate their derivative penalty with vanishing effect on source and absolutely continuous energy. This argument does not assume atoms only. Vague compactness, lower semicontinuity against compact tests, and Fatou then apply to possible escaped mass. The mass scaling is strictly decreasing for this integrated fold objective, excluding wasted or singular limiting mass at the minimum. The argument does not incorrectly extend that strict conclusion to merely order-optimal sequences.

I independently recover the supercritical mass exponent `(2-3q)/7` and the two-fold coefficient `2^((11q-12)/7) S_q`. Equal mass allocation follows from minimizing the sum of the two strictly convex negative powers. The recovery construction uses the exact sine coordinate, includes its Jacobian in both mobility and budget, and normalizes to the exact budget. Its positive graded floor permits Neumann exhaustion and an integrable envelope over the entire rescaled parameter range. Thus the lower localization result and the upper construction close the same variational problem.

### Generic folds and exact observation

The generic theorem explicitly requires finitely many transverse folds, distinct fold locations and parameters, and two-sided positive sampling density near each fold. The compact zero set and the simple-root condition outside the fold neighborhoods provide a finite uniform cover; ordinary roots are not omitted. The moving critical point in the normal form shifts by order `t`, which is smaller than the root distance on the separated-root scale. Parameter Jacobians are bounded in both directions where used.

The generic upper construction supplies a floor sufficient for ordinary roots, including a stationary simple root at the location of a fold occurring at another parameter. There is no use of cosine reflection symmetry in this theorem. Endpoint parameters can contain simple roots, while folds are interior by hypothesis. The conclusion is appropriately limited to orders, not universal cosine constants.

For exact observation, I checked the explicit local solution by differentiating its polynomial flux. The zero flux at the center and support endpoints prevents spurious delta sources. The prescribed mass and response are respectively `3 a R^5/80` and `12/(a R)`. The squared derivative saturates the budget multiplier on the support and is smaller outside, giving a global certificate for arbitrary nonnegative `L^1` coefficients. The bounded Lipschitz response can be approximated by smooth tests against an arbitrary such coefficient, so the certificate is not restricted to smooth competitors. The claimed uniqueness follows from the equality conditions and the flux equation.

The compact multi-root result handles zero local budgets by a limiting lower certificate. Its allocation weights are `a_j^(-2/3)`, consistent with minimizing the sum of `a_j^(-4/5) m_j^(-1/5)`.

The exact-observation upper bound uses an explicit Borel policy with separate separated-root, fold-layer, and root-free pieces. The moving cutoff leaves the local support inside a region where the actual reaction dominates the chosen quadratic reaction. The fold layer has width `M^(2/7)` in parameter and response at most order `M^(-3/7)`, hence is lower order for the mean. The global normalized envelope is integrable. Dominated convergence establishes the upper coefficient; Fatou and the fixed-profile placement lower bound establish the lower coefficient for arbitrary nearly optimal measurable policies. This avoids an interchange of expectation and pointwise minimization.

### Finite precision and the two distinct sharp limits

For finitely many bins, choices decouple directly and preserve the per-observation budget. The local uncertain-center problem is formulated for all `L^1` designs. Its lower bounds come both from exact placement and from an averaged translated harmonic test. The latter gives `C_0 eta^(1/4)` even for nonuniform and concentrated coefficients. The positive graded floor and quadratic weighted Neumann exhaustion justify recovery and continuity; mass completion after vague convergence is sufficient for existence here and does not rely on the stronger strict mass argument used for the integrated quartic problem.

The conditional local length is `(m/a)^(1/5)` with root budget `m=M/2`. Dividing the root displacement by this length gives `eta = 2^(1/5) tau a^(-3/10)`. Combined with the two-root response and probability density `1/4`, this yields exactly the stated integral defining `H(tau)`.

The lower localization allows singular or escaped rescaled mass and completes any missing mass before comparing with the local value. The recovery uses an exact coordinate for the cosine reaction, not a Taylor approximation over an uncontrolled uncertainty interval. A finite cover of compact local uncertainty widths supplies uniform conditional recovery for moving bins.

The global fold treatment uses `W = Delta + M^(2/7)`, so it includes bins that cross a fold and bins whose edge approaches it at any rate. The integrated fold bound

`O(M^(-1/7) + M^(-1/4) Delta^(3/8))`

is negligible relative to `M^(-1/5) + M^(-1/4) Delta^(1/4)` in every stated joint limit. The regular-root envelopes have parameter powers `4/5` and `7/8`, both integrable. These facts justify extending the compact conditional result to the complete ensemble.

The simultaneous coarse regime is proved separately by a root arc much wider than its harmonic diffusion length. Its averaged-gradient certificate again handles arbitrary allocations, and padding the constant-mobility recovery interval makes the endpoint correction negligible. Thus the large-`tau` asymptotic of `H` is a consistency check, not an invalid substitute for a uniform theorem. Fixed nonvanishing bin width is not assigned the small-bin sharp coefficient. The information and bit-resolution interpretations respect the equal-bin, noiseless model and the distinction between nested and nonnested observations.

## Independent numerical and document checks

I built the frozen source from scratch with `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -file-line-error`, using only `/tmp/transport-final-review3-vbo7a6kd` for generated output. The build succeeded, produced **54 pages**, and reported no undefined references, overfull/underfull boxes, or other warnings. PDF text extraction contained no unresolved `??` references and found the expected two figure and three table captions.

For a fresh numerical check I independently assembled sparse tridiagonal matrices with `scipy.sparse.diags` and solved with `spsolve`, rather than using the manuscript's banded solver. I reconstructed all nine stored uncertain-center fields, their discrete objectives, gradients, tangent gaps, and independent center-quadrature re-evaluations. Maximum relative discrepancy in an objective was `7.99e-15`; maximum absolute tangent-gap discrepancy was `2.60e-14`; maximum relative discrepancy in a validation objective was `7.99e-15`. All fields were nonnegative with mass equal to one to floating-point precision.

The four main independently reconstructed values were:

| Center width | Cells | Objective | Tangent gap |
|---|---:|---:|---:|
| 0 | 400 | 6.222654786720648 | 0.001684106772552374 |
| 2 | 400 | 6.633099511133640 | 0.002194983985823740 |
| 8 | 400 | 8.082211246731587 | 0.000437168422001033 |
| 32 | 400 | 11.138582160438464 | 0.000143303275224049 |

The deliberately underresolved width-32, 200-cell field gives `10.840532642493397` on its 24-node objective and `12.094818219837410` on independent 384-node quadrature. This confirms the paper's interpretation of quadrature overfitting despite a small optimization gap.

I checked the circle solver's full-wall factor, half-wall Neumann endpoints, mass normalization, and ensemble quadrature weights against the formulas in the numerical section. Uniform and nonuniform fields receive the same discrete budget. The unrounded mean and distance-based critical trials have the stated leading constants by the comparison arguments given in the text; the supercritical trial is correctly described only as order optimal.

The paper consistently distinguishes a computed trial value, a global bound for a finite-dimensional quadrature objective, a continuum asymptotic optimum, and a finite-budget continuum optimum. In particular, the value below the exact continuum placement constant at zero uncertainty is disclosed as discretization error, and neither the spatial nor domain differences are called rigorous error bounds. No computed value is falsely assigned to `S_q` or the full crossover function.

## Completeness, sources, and presentation

The introduction's results table, abstract, theorem statements, later constants, and discussion agree on thresholds, powers, information assumptions, and physical scope. The paper's length comes mainly from proving unrestricted lower bounds and uniform recovery, including the rough-coefficient and endpoint issues those arguments require. The progression from physical reduction through local models, design, and observation is coherent. Local lemmas precede their use, and the two different whole-line value functions are kept distinct.

The literature presentation credits compliance and reinforcement methods, stochastic coefficient design, rare-degeneracy moment arguments, and quantized-policy theory. The distinction from positive-conductivity stochastic models is restricted to the two specifically cited models; it is not asserted for every reinforcement paper. The claimed new contribution is the particular sharp singular transport laws and their uniform proofs, not the general principles behind risk-dependent allocation or information-dependent decisions. The references and literature discussion do not support an exhaustive novelty guarantee, and the manuscript does not claim one.

The limitations in the discussion are mathematically substantive and sufficient: no mobility cap or fabrication length, independent idealized diffusivity control, fixed positive bulk transport, a uniform kinetic anchor, transverse isolated folds, and noiseless equal bins. No unfinished conjecture, unsupported physical extrapolation, numerical optimization assertion, or hidden future proof obligation remains within the stated results.

## Findings requiring action

- **Major:** none.
- **Minor:** none.
- **Required correction before acceptance:** none identified.

This independent report supplies one of the five required final reviews. I did not use the other reports to assess whether the complete five-review process has been satisfied. The coordinator should evaluate all five independently and use a different fixing agent for any valid issue found elsewhere, repeating the five-review round if a major correction is needed.
