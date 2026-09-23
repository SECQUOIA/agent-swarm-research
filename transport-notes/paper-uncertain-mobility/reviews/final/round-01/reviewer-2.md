# Final whole-manuscript review — reviewer 2, round 01

Frozen snapshot: `e5a8cd3e390d1b7afa16481b35bcd01944a8111bce55e2ffaf1570f40ebc899d`.

**Verdict: no major issues. One minor scope clarification in the introduction should be made before completion.** I found no incorrect theorem, missing proof dependency, unsupported sharp constant, or unresolved limit interchange in the mathematical results. The numerical evidence is appropriately separated from the continuum theorems.

I verified all 28 manifest hashes, reread the entire manuscript source, and checked the proofs afresh rather than treating earlier stage approvals as evidence. I also examined the numerical driver, its imported routines, saved data, figures, bibliography, and scope inventory. I did not read other final reviews, coordinator checks, or prior adjudications. The manuscript sources were not changed.

A fresh private build in `/tmp/transport-final-reviewer2-Zx22Pa` produced a 54-page PDF. The final log contains no warnings, undefined references, or overfull/underfull boxes. I checked the extracted text and page progression against the source. The blank author field is an intentional submission-detail placeholder, not a mathematical omission.

## Required minor correction

### M1 — qualify the introductory physical correction statement

**Location:** `sections/00-introduction.tex:74–79`, immediately after the explanation that the scalar definition permits arbitrary integrable coefficients.

The sentence beginning “The physical dispersion coefficient has a nonnegative bulk correction to…” omits two qualifications that the later model section correctly makes: the derivative preform must be closable to assign the physical process, and the additive finite-response identity is stated when `J_c(D)<∞`. The immediate transition from the larger scalar coefficient class can give a reader the impression that every scalar competitor already has this physical identity. The manuscript explicitly explains later why that inference is not valid.

**Remedy:** state, for example, “For physically admissible designs with finite response, the flow-induced dispersion coefficient equals `χJ_c` plus a nonnegative bulk correction.” Keep the following positive-background construction and, if useful, refer to Proposition `prop:schur`. The general physical lower bound with extended values remains valid as proved. This is a minor summary-scope clarification: the theorem, proof, and optimal-value transfer already use the correct classes and need no change.

## Model, stationary dispersion, and physical transfer

I independently checked the forward boundary signs, backward generator, equilibrium weights, and source normalization. The exchange contribution in the symmetric energy is `K∫k(v−fΓ)^2`, so its integration by parts gives `Db ∂n f=Kk(v−fΓ)` and the wall generator `∂s(Dv′)+k(fΓ−v)`. The forward equations have matching bulk loss and surface gain. The equilibrium measure has unnormalized masses `A` and `KP`; consequently `V=∫u/Z` and the wall component of the centered velocity is `−V`. The scalar prefactor is therefore `KV²/Z`, with no extra factor of two from the variance convention.

The separate treatment of scalar test values and physical closed forms is mathematically important and is respected in the proofs. For a positive floor, an energy-Cauchy sequence has its ordinary derivative identified in `L²`, and then its weighted derivative identified almost everywhere; this proves closability even without an upper bound on `D`. The anchored inequality follows from periodic Poincaré and the lower bound on `∫k`. The coupled energy is closed in the product form norm. Normal contractions control the exchange term as well as the individual derivative terms. Constants, regularity of the core, and the finite invariant measure justify the conservative stationary Markov realization. A positive floor supplies the stated spectral gap; a gap is not silently assumed for every degenerate design.

The stationary covariance formula yields

\[
\frac{\operatorname{Var}X_t^{\rm adv}}{2t}
=\int\!\left[\int_0^t(1-r/t)e^{-\lambda r}\,dr\right]d\nu_g(\lambda).
\]

Its integrand is increasing in `t`, with limit `1/λ` on the positive spectrum and `t/2` at zero. Thus the extended stationary coefficient is actually identified from displacement, not defined by a desired variational formula. The variational formula follows by spectral truncation, including both kinds of infinite response. The independent axial Brownian driver contributes its stationary expected diffusivity without cross covariance.

For the Schur calculation I expanded the surface maximum at fixed bulk trace. Its constant term is `KV²J`, its cross term is `−2KV∫kh fΓ`, and its residual trace quadratic form is nonpositive in the objective. The compatibility identities `∫Ω(u−V)=KPV` and `∫kh=P` validate the common-constant gauge. The extension when `J` is finite but an `L²` corrector need not exist uses the energy completion and its continuous map into `L²(k ds)`; it does not subtract infinite quantities. The resulting `w∈L²` makes the bulk remainder finite.

The uniform remainder proof uses both positivity and exact mass of `w`. The Fourier bounds `|ŵn|≤1` and `Σ|ŵn|²≤||w||∞` give an `H^(−1/2)` squared norm bounded by a logarithm after splitting at `N≈||w||∞`. The floor estimate `||w||∞≤C/m` then produces `R≤C(1+log(1/m))` through the trace dual norm. This step is specific to the stated one-dimensional wall and fixed positive bulk diffusivity.

Finally the mixture has exactly the original budget and observation dependence. Its full scalar form dominates `(1−θ)` times the original form, including the reaction. Minkowski for `q≥1` and subadditivity for `q<1` give the stated comparison without selecting a pointwise optimizer. Taking `θ=M` proves the asymptotic ratio, and the moving bump of width `M^(1/5)` proves the observation-uniform cosine lower bound. All later physical transfers satisfy the required growth condition. The dimensional conversion also checks: `Jphys=(ℓref/kref)J′`, so dimensional coefficients require that factor before multiplication by physical `χ`.

## Uniform mobility, fold tails, and averaged moments

The interval lemma provides the ingredient needed on both sides of every bracketing argument: a positive-potential anchor controls constants even with free endpoints, and the weighted source tails tend to zero. Its proof permits bounded comparable metric weights converging only locally. This suffices for compact unfolding parameters; the manuscript separately proves, rather than assumes, the estimates needed when those parameters diverge.

I integrated the oscillator heat kernel and checked

\[
C_0=\frac{\pi\Gamma(1/4)}{2\Gamma(3/4)}.
\]

A quadratic defect with coefficient `a` has length `(ε/a)^(1/4)` and response `C0 ε^(−1/4)a^(−3/4)`. A quartic fold `(bx²−t)²` has length `(ε/b²)^(1/6)`, parameter `μ=t/(εb)^(1/3)`, and response `ε^(−1/2)b^(−1) Cpair(μ)`. For the positive pair tail, the two roots each have quadratic coefficient `4μ`, giving `C0/√2`; the omitted reciprocal potential is smaller on the selected shrinking relative neighborhoods. On the negative side, scaling by `√|μ|` and testing with the reciprocal potential gives the exact `π/2` coefficient.

For the cosine family, `b=1/2`, two folds, and density `1/4` give the supercritical uniform coefficient `2^(q−4/3)∫Cpair^q`. The inside tail is integrable precisely for `q<4/3`. At the critical order the explicit logarithmic cutoff yields `(2C0)^(4/3)/12`, which equals the coefficient displayed in the theorem. The squared mean is lower order than the second moment, so the variance formula follows. The limiting distribution has the claimed half-mass atom and `4/3` tail.

I also rederived `k_c''=2(1−c²)+6c(c+cos s)−4(c+cos s)²`. The integrated flux identity and the uniform response/gap bounds imply `||kh−1||²≤Cε^(1/6)`. The Neumann bulk load and Schur penalty then yield the stated uniform remainder limit. The stronger correction is proved for uniform mobility and is not imported into arbitrary design families.

The Gaussian amplitude-collapse counterexample is sound: its constant test gives `J≥2P/R²` for every field, whereas the samplewise harmonic zero sum has finite mean. This does not conflict with the anchored cosine results. The Kac–Rice paragraph is presented as a classical marked-root calculation, not a new annealed transport theorem. Averaging the rate before solving gives a bounded response and is correctly distinguished from averaging the realized inverse response.

## Predetermined optimization, including critical and supercritical sharpness

The quotient representation proves convexity of `J^q` for every positive `q`, including orders below one. The four cosine symmetries reduce the value without imposing regularity on competitors.

The moving-shell test gives a conditional derivative cost controlled by local mass through Fubini. Negative-power Jensen then gives `r^(2−5q/4)m^(−q/4)`. Disjoint shells supply the critical logarithmic lower order. The fold bump uses the full budget and gives `M^((2−3q)/7)` without any concentration assumption. The graded construction balances `a_R≈R^(6+α)` and has the necessary root, core, and rootless bounds. I checked the identity

\[
2-\frac{3q}{2}+\frac{q\alpha_q}{4}
=\frac{8-5q}{q+4},
\]

which identifies the optimized threshold and all three upper orders.

For the sharp subcritical certificate, the paired-test source factor, the `1/4` root density, and the division by two when both root arcs are counted agree. The moving derivative kernel is spatially constant to leading order because `d_E` has exponent `1/(1+q/4)`. Its supremum can be integrated against any concentrated competing field. The supporting-line derivative penalty cancels the excess reference term after the resource constraint is applied. Truncation at arc endpoints reduces the nonnegative kernel and cannot invalidate its upper bound. This proves a genuinely unrestricted lower coefficient, not just optimization among fixed limiting shapes.

At criticality the same calculation remains uniform since the oscillator width divided by root-to-fold distance tends to zero on the moving arcs. For recovery, the four one-sided fold approaches give `Z_R~(4/7)log(1/M)`. The retained `RL` annuli have large oscillator-scaled radius, the reciprocal-potential complement is negligible, and omitted inner annuli cost only an additional `log L`. These estimates produce precisely `Kcrit=(2C0)^(8/5)(4/7)^(7/5)/8`.

For the supercritical variational value, derivative flattening near a null support correctly removes singular measure mass while preserving the source and potential integrals. Vague lower semicontinuity is available test by test and then through Fatou. The mass scaling is

\[
\mathscr I_q(d_m)=m^{-(3q-2)/7}\mathscr I_q(d),
\qquad d_m(x)=m^{6/7}d(x/m^{1/7}).
\]

A positive integrable tail with `1<α<min(2,6−8/q)` gives finite cost for every fixed `q>8/5`. Strict mass scaling rules out lost and singular mass in a minimizing sequence and proves attainment by a density. No unproved uniqueness is asserted.

The common-scale lower bound has geometric factor `(1/4)b0^((3−8q)/7)` and two limiting masses of total at most one. Minimizing the strictly convex decreasing mass costs gives equal halves. With `b0=1/2`, the net factor is `2^((11q−12)/7)`. I independently checked that exponent algebraically.

Recovery uses an exact sine coordinate, not a Taylor approximation across the entire cell. The choice `D=b0²ℓ⁶wℓ d` cancels the metric in the derivative integral; the actual mass is `m∫wℓ²d=m(1+o(1))`. The normalization multiplier therefore tends to one. The free-endpoint lemma establishes the correct whole-line limit even for unbounded locally positive densities. Its boundedness and cutoff argument closes a possible weighted-domain gap. The global graded background supplies an integrable parameter envelope on the entire offset half-range, so pointwise fold localization legitimately passes to the moment. Thus both recovery and attainment concern the same unrestricted constant `Sq`.

## Generic fold families

The hypotheses exclude identically vanishing realizations and imply uniform anchoring by compactness. The constructed normal coordinate uses `gss≠0` and `gc≠0`; its critical-point shift is `O(t)` and its bounded Jacobian preserves the root scales. Compactness supplies a uniform ordinary-root cover and a finite bound on the number of roots. No ordinary-root parameter transversality is silently assumed.

One sampled fold suffices for all lower orders. The upper construction protects every site and takes a nonnegative grading exponent. That last choice avoids reducing mobility at a stationary ordinary root that happens to occupy another fold's spatial site. I checked central Neumann coercivity and the integrals in every range, including `q≤2/3`, the critical logarithm, and the supercritical comparison with ordinary-root contributions. Only orders are transferred from this theorem; cosine sharp coefficients are not assigned to generic families.

## Exact placement and observation

I checked the polynomial identity with `p(y)=y−3y³+2y⁴`:
`∫₀¹p=3/20` and `p′+y²(9−8y)=1`. The flux vanishes at the center and outer edges, so there is no hidden delta source. The integrated response, derivative energy, and reaction energy are `12/(aR)`, `12/(5aR)`, and `48/(5aR)`. The saturated slope has square `64/(a²R⁶)`, matching the derivative of the optimized value with respect to mass. The Lipschitz certificate is admissible against arbitrary integrable coefficients by cutoff and dominated convergence. Equality forces the exterior mobility to vanish and the weak flux equation uniquely recovers the interior profile.

The compact-wall lower theorem uses each competitor's actual local mass and has an error uniform over masses between zero and `M`. Its auxiliary-mass argument handles a zero local budget. Minimization of the resulting negative-power sum yields `m_j∝a_j^(−2/3)` and the `6/5` power. The upper bound includes both the interior value and the reciprocal-potential exterior, retaining the essential extra `2/(aR)` per defect.

For the explicit degenerate physical trials, the proof checks closability, zero endpoint capacity, and coercivity instead of silently imposing transmission. Potential comparison bounds `kh`, and its nonconstant part is supported on length `O(M^(1/5))`. This proves the stated fixed-profile correction limit.

The observed cosine policy keeps `R≪δ≪√a` uniformly in the separated regime after choosing the fixed threshold large enough. The curvature loss tends to zero at every fixed regular offset. The fold patch has mass `M` and response `O(M^(−3/7))`; its parameter width is `O(M^(2/7))`, so its mean contribution is lower order. Together with the rootless reciprocal bound, this gives the integrable `|1−|c||^(−4/5)` envelope. The pointwise lower theorem plus Fatou proves the lower mean without interchanging expectation and an uncountable pointwise infimum. The Borel recovery policy establishes the upper mean with the required per-realization budget.

## Finite precision and the two distinct joint limits

The uncertain-center scaling is `a^(−4/5)m^(−1/5)Fctr(w/(m/a)^(1/5))`. The translated oscillator certificate gives `Fctr(η)≥C0η^(1/4)` for arbitrary unit-mass fields. Uniform mobility on a padded uncertainty interval gives the matching large-width limit. Vague compactness, singular removal, and completion of missing mass prove attainment; positive-tail regularization proves upper semicontinuity. The expanding-interval lemma includes the slower quadratic source tail and justifies the necessary energy completion.

Reflection symmetry in each bin splits the budget into two exact halves even though an individual bin need not be symmetric under `c→−c`. The resulting uncertainty parameter is

\[
\eta_I=2^{1/5}\Delta M^{-1/5}(1-c_I^2)^{-3/10}.
\]

The compact-test liminf permits escaped and singular masses; the exact cosine-coordinate recovery preserves the same local response and restores the exact budget. Continuity and compactness justify uniform conditional limits, not just limits for a fixed bin.

The bin envelope controls regular bins, bins straddling folds, and rootless bins. With `W=Δ+M^(2/7)`, the integrated fold cost is `O(M^(−1/4)W^(3/8))`. It is negligible compared with the sum of the two mean scales along every joint limit. The fixed-compact-bin Riemann sums therefore extend through the folds using integrable exponents `4/5` and `7/8`. They give the displayed function `H` with the correct probability and half-budget factors.

The coarse limit has its own uniform moving-root lower certificate and padded-arc recovery. It is not inferred by exchanging the finite-ratio and large-ratio limits. The conditional leading value is `2^(5/4)C0 a^(−7/8)M^(−1/4)Δ^(1/4)`; division by four and integration gives `Kcoarse=2^(−3/4)C0 B(1/2,1/8)`. The omitted fold cost becomes `O(Δ^(1/8))` relative to that scale. This proves the claimed grid-alignment independence. Statements about binary digits and nested partitions remain within the specified noiseless quantizer model.

## Independent constants and numerical checks

I recalculated the principal constants at high precision:

| Constant | Independent value |
|---|---:|
| `C0` | 4.64747600940096692 |
| `Cpl` | 6.22282373601988861 |
| `K1` | 18.3860636501142786 |
| `Kobs` | 22.4046282307491383 |
| `Kcrit` | 2.02233076396938973 |
| `Kcoarse` | 25.723827388763291 |
| `Kobs/K1` | 1.21856579293468737 |

These agree with the manuscript. The numerical unrounded-mean shape is squeezed by the rounded shape and the sharp lower bound. The critical distance profile has the same logarithmic coefficient by local comparison on retained annuli. The third-moment trial is only labeled order optimal.

The circle matrix, reflected source integral, offset density, and sampled mobility normalization agree with the prose. For the center calculation, independent differentiation of `h·1ᵀA⁻¹1` with face masses gives the displayed negative squared-gradient derivative. Convexity then gives `F−g·p+min g` as a lower value for that discrete simplex problem. The exterior response is the exact average of `1/(L−z)+1/(L+z)`.

For this final review I recomputed all nine stored center fields with separately assembled sparse matrices and a sparse linear solver. Every field is feasible to floating-point precision. The largest relative objective discrepancy was `7.99×10^(−15)` and the largest absolute tangent-gap discrepancy was `2.60×10^(−14)`. This checks the derivative and objective independently of the optimization implementation. The corrected mean-refinement percentage agrees with the data. The disclosed underresolved quadrature example and the separate optimization/discretization limitations prevent the numerical values from being misrepresented as continuum certificates.

## Literature, completeness, and readability

The manuscript contains the proof dependencies needed for its claims and does not send a reader to unpublished repository notes for missing arguments. The progression from the physical coefficient to local models, predetermined optimization, exact observation, and finite precision is coherent. The order/equivalent distinction, admissible classes, independent observation budgets, and dimensionless constants remain consistent across the technical sections and conclusions, subject to M1 in the introduction.

The literature comparisons are appropriately limited. I checked the primary [reinforcement formulation](https://arxiv.org/pdf/1506.00141), the [random-load conductivity formulation](https://arxiv.org/pdf/1002.2770), the [risk-averse two-conductor formulation](https://arxiv.org/html/2602.19869v1), and the [adsorption/desorption transport context](https://arxiv.org/abs/1211.5224). They support the described precedents without establishing the present vanishing-reaction, small-resource laws. The manuscript also credits the broad risk-allocation, bifurcation-moment, and observation-channel ideas instead of claiming those methods as inventions. The weighted-form warning is consistent with the established Hamza criterion, as also discussed in the primary [one-dimensional diffusion analysis](https://arxiv.org/abs/1701.02411).

Additional targeted searches did not identify a prior source giving the particular thresholds, critical coefficient, unrestricted fold variational limit, or joint resolution law. That negative search result is not a proof of absolute novelty, and I do not treat it as one. The paper's positive comparisons and stated access limits are a defensible way to present the literature position.

No further substantive development is necessary for the theorems as stated. Explicit formulas for the two attained variational minimizers, arbitrary noisy measurements, simultaneous generic folds, mobility caps, and fabricated-surface realization are expressly outside the claimed results rather than gaps in their proofs.

## Final disposition

Make the minor introductory qualification M1, check the resulting build, and update administrative completion status after the coordinator's final decision. My review finds no major issue requiring another five-reviewer round. This conclusion follows from the whole-manuscript audit above, not from earlier stage approvals.
