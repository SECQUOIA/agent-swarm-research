# Stage 4, round 1: independent review 2

Verdict: **no major issues**. I found one minor bound-notation clarification in the alternative density-envelope argument. The new microscopic boundary extension, complete physical optimization, and Gaussian geometry proofs are supported under the stated assumptions.

I read all three new sections, the stage author record, relevant Stage 1–3 dependencies, and the integration in `main.tex` and `refs.bib`. I did not consult other current-round reports, edit the manuscript, or delegate work. The review was analytic, with the source checks described below; no numerical calculation was rerun.

## Minor issue and remedy

**Location:** `sections/boundary-and-smooth.tex`, final paragraph of the microscopic-applications subsection, around lines 340–351.

The paragraph treats both the secant calibration and its finite corrections, but writes the interior estimate as `h_N(E) <= C x/sqrt(N)`, where `x` is distance to the nearest phase center. This estimate is correct for the secant calibration. For a finite correction normalized at the lower center, the upper endpoint value can tend to a positive `D`, so the displayed estimate cannot hold there with `x=0`.

**Remedy:** Explicitly denote that first estimate by `h_N^sec`, and add that a bounded finite correction satisfies `h_N(E) <= C_0 + C_1 x/sqrt(N)` on the interior. The extra constant is harmless: in the tail region `x >= R sqrt(N)` its ratio to the Gaussian cost is at most `C_0/R^2`, and it can also simply be retained as a bounded prefactor in the weighted tail integral. The already stated exterior constant bound is correct. No theorem or limiting formula changes.

## Microscopic boundary extension

**Mean-field, including zero variance.** The global Gaussian occupation bound yields every fixed exponential moment of standardized phase energy after conditioning, since the canonical phase probabilities stay positive. The Gamma transform has the same property for each fixed parameter and all sufficiently large sizes. The qualification about the lower size cutoff is necessary and is present. There is no exceptional component. The ordered pure-spin variance is positive and the disordered one is zero; the measure formulation of the boundary theorem handles the latter correctly. In particular, a zero-variance phase contributes a point mass, its tilt does not change its conditional law, and its Gaussian-normalization factor is one.

**All fixed moments when spatial dimension exceeds two.** Stage 2 proves the restricted second derivative bound uniformly on `|beta-beta_c| <= eta_0/L`. If `d>2`, then for every fixed real transform parameter, the associated displacement of order `N^(-1/2)=L^(-d/2)` eventually lies in this window. The `O(N)` curvature bound and the `O(sqrt(N))` center error bound its logarithmic moment transform by a finite constant depending on that fixed parameter. The fugacity change has derivatives bounded above and away from zero on the fixed temperature interval, so the same statement applies to the bond count. The binomial-noise bound is available for every fixed parameter, and Cauchy–Schwarz transfers the resulting moments to the spin energy. This establishes the actual hypothesis required by the boundary theorem, not just a small-parameter moment.

**Contour and midpoint events.** The established contour-phase exponential moment makes the conditional probability of landing beyond the opposite spin-energy midpoint exponentially small on scale `sqrt(N)`. The tunneling event has vanishing probability. Hence the symmetric difference between a contour phase event and its corresponding midpoint event vanishes under the Edwards–Sokal reference. Since both phase probabilities have positive limits, their conditional spin laws approach one another in TV. The previously proved midpoint-conditioned weak CLTs therefore identify the contour-conditioned weak limits. No assumption that the finite-volume partitions coincide is used.

**Exceptional mass and spatial dimension.** At boundary capacity, the maximal secant gain has logarithm asymptotic to `beta^2 ell^2 sqrt(N)/(8 gamma)`. For `d>2`, the exceptional cost `tau L^(d-1)` dominates `sqrt(N)=L^(d/2)`. In `d=2`, both are proportional to `L`; the strict displayed inequalities ensure both a moment parameter beyond the tilt and a strictly negative residual exceptional exponent. Thus every fixed positive `gamma` is justified for `d>=3`, while only sufficiently large fixed `gamma` is justified for `d=2`. The manuscript does not overstate the latter range or claim microscopic droplet morphology there.

## Physical boundary law and optimization

- Direct expansion of the exact endpoint slopes gives standardized limits `b` and `−b`, with `b=beta^2 ell/(2 gamma)`. A total-energy correction `d sqrt(N)` changes the relative endpoint log weight by `D=beta^2 ell d/gamma`, while changing standardized slopes by a vanishing amount. The signs and coefficients agree.

- The strict exponential-moment condition `eta>b` permits a fixed power `p>1` of the tangent bound. This supplies uniform integrability of both the reweighting and the TV integrand. The exceptional bound is stable under bounded corrections because the normalized maximum changes by only `O(1)`. Thus the limiting normalization, phase weights, conditional Gaussian tilts, and full microscopic TV formula do not rely on weak convergence alone.

- The phase-population compensation has the correct positive correction when the lower phase has larger variance. It makes the two integrated reweighting factors equal. The remaining Gaussian translation gives the stated weighted TV error, including zero for a degenerate phase. It claims asymptotic, not finite-size, phase matching.

- For the upper bound in the complete optimization, bounded corrections attain every interior phase weight. Continuity supplies the endpoint infimum. A separately phase-centered bounded weight preserves the selected phase and eliminates the other, attaining its discarded reference weight.

- For the lower bound, error strictly below both phase weights forces a fixed positive likelihood overlap in each phase. Tightness and the likelihood Markov bound produce two feasible energies within `O(sqrt(N))` of their centers, with likelihoods bounded above and away from zero. Their exact likelihood-ratio equation forces the total energy to lie within `O(sqrt(N))` of the secant calibration. The asymptotic expansion and its response to endpoint perturbations have the stated orders. A convergent correction subsequence then falls under the proved boundary theorem. This argument covers arbitrary approximate minimizers; it does not assume that a global minimizing calibration exists or silently restrict the original infimum.

- The signed-measure objective has the correct factor one-half. Its normal-CDF expression sums the positive parts of the two weighted phase differences, whose total positive and negative masses agree. Differentiation cancels the Gaussian-density terms and gives the stated strictly increasing derivative when both variances are positive. Equal positive variances give the target phase weight as the unique interior minimizer. Abandonment must still be compared separately, as the theorem does.

- Smooth-reservoir necessity follows from the strong-concavity chord at three good likelihood points inside the feasible phase interval. The entropy-curvature/heat-capacity conversion has the correct sign and units. The smooth converse explicitly requires endpoint calibration and the tail assumptions, rather than asserting that arbitrary reservoir entropy can be calibrated by total energy alone.

## Exact Gaussian geometry

The scalar completion of squares, transformed weight odds, standardized displacements, finite crossover, and phase-abandonment optimization are consistent. A single bounded-width Gaussian cannot cover both separated target windows. In the finite-crossover regime, retaining both component weights forces the additional standardized field to vanish, giving the symmetric convex objective; choosing a field that centers one component attains the one-half alternative. The specified canonical-mean calibration with unequal weights has the stronger weight-error condition claimed.

For the vector model, matching full-law TV forces a bijection between components and target phase neighborhoods. A limiting homothety of a finite distinct point set onto itself must have unit scale, by its diameter, and zero translation, by its centroid. Hence the original component labels and weights are recovered. Shape comparison gives the `N^(3/2)` obstruction, and the affine score invariant supplies the additional `N^2` obstruction exactly when the squared phase norms do not lie in the affine span of the phase coordinates. This is equivalent to the sphere condition. The one-phase covariance criterion is also correct.

The phase-loss theorem handles the potentially problematic unbounded fields. If the field stays away from zero, score concentration occurs near a supporting face, while the transformed mean moves beyond the reference support in that direction; the scale comparison makes the TV tend to one. If the field tends to zero, missing positive limiting component weights give the reference-mass lower bound. The fixed finite linear equality/inequality system for surviving phases is approximately feasible. Farkas' alternative rules out approximate feasibility of an infeasible fixed system with vanishing errors, even when the approximate centers diverge. Therefore a finite empty-sphere contact set contains the surviving indices. This proves the lower bound matching the constructive upper bound.

The anisotropic completion of squares correctly uses `B_N(I+N B_N)^(-1)` as the effective quadratic metric. The nullspace qualification avoids incorrectly describing every semidefinite restoration locus as a cylinder. No unsupported anisotropic scaling classification is asserted.

## Capillarity and diagnostics

The exact physical interior formula and the cubic sign follow from the Bernoulli log transform. The maximum has the leading coefficient used in the microscopic exceptional estimate; its cubic correction can be order one at boundary capacity and is not used to infer tied weights.

The compact-support large-deviation model is explicitly assumed. Uniform convergence of the rescaled physical tilt on its fixed compact support justifies the normalized tilted rate. Below the stated threshold the minimizing set is separated from the two canonical endpoints, giving TV tending to one. Above it the statement is only about rate minimizers. The explanation that subexponential factors prevent determination of tied weights is correct and distinguishes this model from a microscopic Potts Wulff theorem.

For the prescribed square-torus rate, each of its three branches bounds `8 tau theta(1-theta)` from below, with joint equality only at the two endpoints and the midpoint. Subtracting the midpoint value proves the claimed unique minimizer below the capacity threshold; equality yields precisely three minimizers.

The histogram Gaussian integrals and TV crossing formula have the correct normalization. Fixed-width-bin squared errors scale like the bin width times the density squared error; this explains the vanishing Euclidean norm without changing TV. The fixed-energy barrier identity cancels normalization exactly. The midpoint gain is `c log cosh(beta Delta/(2c))`; its lower and upper bounds imply the claimed absolute-accuracy equivalence without a prior large-capacity assumption. The relative-barrier scale is stated in its large-capacity regime and is not presented as a kinetic-rate or relocated-saddle result.

## Source and scope checks

The retained primary Challa–Hetherington 1988 text defines the Gaussian reservoir through quadratic entropy and discusses ensemble-dependent fluctuations. Its use here is appropriately narrow. The primary publisher abstract for [Challa, Landau, and Binder 1986](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.34.1841), inspected during this review, explicitly describes weighted Gaussian energy peaks and confirms the cited authors, year, journal volume, and starting page. These references support the acknowledged established models; the manuscript does not use them to substitute Gaussian tails for the microscopic phase laws.

The section ordering and references make the required dependencies available. A broader novelty audit and final synthesis remain outside this stage. No conclusion of literature priority follows from this report.
