# Independent whole-manuscript review — reviewer 5

Date: 2026-09-07. Reviewed snapshot `e5a8cd3e390d1b7afa16481b35bcd01944a8111bce55e2ffaf1570f40ebc899d`.

**Verdict: no major mathematical, scientific, numerical, or manuscript-presentation issue identified. One minor auxiliary-document status correction is needed.** This verdict follows a fresh reading of every included section and reconsideration of the proof dependencies, rather than an aggregation of earlier stage approvals. I did not read other reviewers' reports or coordinator checks/adjudications, delegate review work, or change manuscript sources or numerical artifacts.

## Snapshot and scope

I recomputed the SHA-256 hash of every file in the final manifest: all 28 hashes match. I read `main.tex`, every included section from the abstract through the discussion, the bibliography, numerical driver and its two imported solver/design files, data and table definitions, and the scope/notation documentation. I also compared the manuscript's coverage with the uncertainty working draft and the contents of the relevant risk, generic-fold, observation, precision, and placement notes. Historical claims of verification were not premises of this review.

The manuscript covers the uncertainty paper's full mathematical chain: the physical reduction, uniform baseline, unrestricted predetermined moments, generic fold orders, exact placement and observation, and finite observation precision. It goes beyond the historical working draft by proving the supercritical variational coefficient and the finite-ratio crossover. General power-law deterministic placement, finite rate floors, varying surface velocity observables, and joint flow/budget optimization are separate questions; their exclusion does not omit a premise needed by the uncertainty results. The necessary quadratic placement result is included and proved.

## Independent mathematical audit

### Physical model, closed forms, dispersion, and transfer

The forward boundary sign gives bulk loss equal to surface gain. Constant bulk concentration and wall concentration multiplied by `K` yield the stated equilibrium and mean velocity. The symmetric exchange energy gives the backward boundary condition `Db ∂n f = Kk(v−fΓ)`, with the correct wall weight `K`; the coefficient multiplying the scalar response is consequently `KV²/(A+KP)`. The dimensional budget is a length cubed divided by time, and the response conversion is a length multiplied by time. The stated nondimensionalization and the factor `χphys ℓref/kref` are consistent.

The scalar and physical admissible classes remain distinct throughout the paper. For a positive floor, closability follows because energy convergence implies ordinary derivative convergence, and multiplication by finite-a.e. `sqrt(D)` identifies the weighted derivative limit. No upper bound on `D` is needed. The anchor controls the surface constant mode; bulk Poincaré, trace continuity, and exchange then give the coupled gap in the common-constant gauge. The closed form on the disjoint union of the bulk closure and the separate wall component has the required continuous core, finite invariant measure, and constant zero-energy function. Thus using a stationary reversible transverse process is justified for the stated physical class.

I checked the dispersion derivation independently: stationarity produces the covariance integral, and spectral positivity gives a monotonically increasing finite-time response with limit `∫λ⁻¹ dνg`. The explicit kernel-projection trial covers nonzero mass at zero; restricting the proof to positive spectral intervals would not suffice, but the present proof does not make that omission. The axial Brownian contribution has the right expectation and vanishing covariance conditional on the transverse path. It is not combined with the optimized advective coefficient without the stated boundedness assumption.

The Schur completion has the correct negative cross term and nonnegative penalty. For finite scalar response without an `L²` corrector, the separate energy completion is sufficient: `sqrt(k)h` is an `L²` image, the resulting `w` gives a finite trace load, and the surface supremum can be completed without subtracting infinite terms. The mean-zero gauge follows from `∫w=P` and `∫Ω(u−V)=KPV`.

The logarithmic remainder bound uses the properties that actually remain uniform: `w≥0`, `∫w=P`, and `||w||∞≤C/m`. Low Fourier modes contribute a harmonic sum; high modes contribute `||w||∞/N`. Choosing `N` comparable to the latter norm gives an `H⁻¹/²` squared norm of logarithmic size. The trace-dual bulk maximization then preserves that order. This is consistent with a connected one-dimensional wall and fixed positive bulk diffusivity; the later results do not invoke it outside those assumptions.

The response measurability follows from a common countable smooth-test family. Uniform-background mixing is continuous in `L¹`, preserves exact per-observation mass and available information, and produces a physical field. The two separate moment estimates correctly use Minkowski for `q≥1` and subadditivity for `q<1`. The pointwise cosine bump gives `J≥cM⁻¹/⁵` on a parameter event of probability `1/4`, for every selected design. It therefore supports the observation-uniform ratio estimates, including observation laws changing with `M`.

### Local source problems, moments, and counterexamples

The whole-line source is handled in the energy dual, rather than as an `L²` constant. The core anchor and the source-tail bounds are sufficient for both Dirichlet and free-endpoint expanding intervals. In particular, the upper limit retains source convergence, not only energy lower semicontinuity. Locally convergent weights preserve these arguments through uniform comparability.

Direct Gaussian integration of the displayed oscillator kernel gives `sqrt(2π/sinh(2t))`; the substitution `r=exp(−4t)` gives the beta expression and `C0`. The isolated-zero rescaling gives the factor `ε⁻¹/⁴ a⁻³/⁴`. For the quartic pair, the positive-parameter roots have curvature `4μ`, giving `2C0(4μ)⁻³/⁴`; on the negative side the reciprocal-potential integral gives `(π/2)|μ|⁻³/²`. These tails give precisely the `q>4/3` integrability condition.

The exact sine coordinate preserves the local squared-rate structure at each cosine fold. I checked the oscillator lengths, spectral-gap powers, complement estimates, and the distinct compact-fold and separated-root limits. The argument does not use a whole-line rootless coefficient on an interval whose scaled endpoint stays comparable to the offset scale.

The disorder-moment factors include the uniform density `1/4`, both folds, and the paired roots correctly. At criticality, retaining `t≥ε^b` gives a coefficient proportional to `b`; the omitted contribution is bounded by a constant times `1/3−b`, so the subsequent `b↑1/3` limit supplies an upper as well as a lower coefficient. The squared mean is lower order than the second moment. The atom and positive tail of the samplewise limiting variable also agree with direct inversion of the cosine expression.

For the stronger uniform bulk limit, I checked the identity obtained by multiplying the source equation by `kh`. The two interior error terms are bounded by `Cε¹/⁶`, as is the exterior term, giving the stated `L²` flux error `Cε¹/¹²`. The regular Neumann bulk problem has the correct compatibility condition. Its `H²` regularity permits the uniform-mobility Schur trial, and the moment/variance consequences follow from the uniform bounded remainder. No additive bounded error for the singular scalar equivalent is inferred.

The Gaussian example uses a constant test and hence survives every mobility choice, including observation-dependent choices. The Rayleigh inverse-square expectation diverges, while the inverse-three-halves mean is finite. The marked Kac–Rice discussion is explicitly an application of established zero-intensity weighting and makes no independence, stable-law, or annealed-limit claim. Averaging the rate before inversion indeed produces a uniformly bounded response and cannot replace the quenched average.

### Unrestricted predetermined design and generic folds

The quotient supremum proves convexity for every positive `q`, including values below one. The symmetry reduction uses the actual cosine law and is not later transferred to nonsymmetric families. In the shell certificate, averaging derivative energy gives `m/(rℓ)`, while reaction energy is `r²ℓ³`; balancing them gives the stated shell power. At criticality, disjoint shells and the total-mass inequality give the power `7/5` of the shell count. The fold test of width `M¹/⁷` supplies the supercritical exponent against arbitrary competitors.

I rechecked the sharp moving-root certificate with its probability normalization. The spatial factor in the averaged derivative penalty is proportional to

`ρ d_E^(−1−q/4) a^(−3q/4) = Z_E^(1+q/4)/4`.

This cancellation makes its upper bound uniform in position, so integrating against an arbitrary concentrated `D` is legitimate. Arc endpoints only remove nonnegative kernel mass. The supporting-line error comes from the potential and reference geometry, independently of the competing field. Expanding fixed arcs gives the subcritical beta coefficient. The rounded upper fields have an integrable fold envelope with exponent `7q/[2(q+4)]`, including the range where the uniform-mobility envelope fails.

At criticality, the test width divided by distance from the fold tends uniformly to zero on the moving retained arcs. The four one-sided fold approaches give the normalization `4 log(1/R)`. The upper argument retains harmonic intervals much larger than the oscillator length, and both the discarded inner annuli and rootless contributions lose a logarithmic factor. These checks give the same `Kcrit` from both sides.

The supercritical measure argument does not presume that a weak limit is a density. Flattening the test derivative near compact null sets, followed by the integral correction needed for a compact primitive, removes singular mobility mass with vanishing source/reaction error. Vague lower semicontinuity holds for each compact test, then for the supremum, and Fatou handles the parameter integral. The admissible tail range `1<α<min(2,6−8/q)` is nonempty precisely in the required supercritical range. Spatial mass scaling gives the exponent `(3q−2)/7`; positivity and its strict decrease rule out lost or singular mass in a minimizing sequence. Thus the asserted attained density follows without a profile regularity claim.

The rough-density natural-endpoint lemma supplies the missing upper-limit ingredient for recovery. Its positive lower tail gives local `H¹` compactness and weighted derivative identification. The point bound and integrable coefficient make whole-line cutoff energy vanish. Exact sine-coordinate transplantation produces the derivative coefficient intended in the local problem; the extra metric occurs twice in mass, and the manuscript includes both factors before its exact-budget normalization. The parameter envelope covers the full offset half-range and is integrable to power `q`.

Independently combining the parameter Jacobian, response scale, density, and equal-fold allocation gives

`(1/4) b0^((3−8q)/7) × 2 × (1/2)^(-(3q−2)/7) = 2^((11q−12)/7)`

for `b0=1/2`. The concentration statement is restricted to sequences attaining the sharp value; the explicit half-budget-plus-uniform counterexample correctly excludes the stronger statement for merely order-optimal sequences.

For generic folds, compactness and the nondegenerate fold/simple-root cover give the necessary uniform root count, root separation outside folds, slope bounds, and rate anchor. The Taylor-factor coordinate has sufficient regularity under `C⁴`; its Jacobian and the parameter Jacobian are bounded as needed. The lower shell argument uses positive sampling near only one fold. The upper field protects all fold sites and uses a nonnegative exponent, which is necessary to protect ordinary roots that can occupy another fold site. Ordinary, central, and rootless terms have the stated lower or equal orders. The generic conclusion remains an order theorem and the physical transfer remains an optimal-value ratio, not a claim of generic cosine coefficients.

### Exact placement and exact observation

I differentiated and integrated the local polynomial independently. Its integral is `3/20`, and `p′+y²(9−8y)=1`. The flux is zero at the center and support edges. The reaction integral is `48/(5aR)`, the derivative integral `12/(5aR)`, and the total source `12/(aR)`. In particular, the exterior source contribution `2/(aR)` is retained; omitting it would give a wrong placement constant.

The saturated global slope bounds derivative cost by the full competing mass even for unbounded `L¹` fields. The specified cutoff/mollification preserves the needed slope control. Equality forces zero exterior mobility, and the distributional first variation fixes the flux and then the coefficient on both half-supports. This proves the advertised a.e. uniqueness rather than only stationarity.

Compact-wall localization uses actual local masses and handles zero local mass separately. Optimizing the inverse-fifth-power allocation gives weights `a_j⁻²/³` and the power `6/5`. The two limits in neighborhood accuracy and budget do not justify an additive bounded scalar error, and the manuscript correctly avoids that assertion. For the explicit degenerate trials, the zero-capacity transitions and fixed-budget coercivity justify independent component restrictions and comparison with the local source. The flux error is supported on length `O(M¹/⁵)`, giving its `L²` rate. The bulk remainder limit uses fixed smooth bulk tests and does not require a bounded derivative of the bulk maximizer.

The oracle proof uses an explicit Borel recovery policy and Fatou on near-minimizing policies, not an unjustified expectation/infimum interchange. The separated-root curvature comparison, the scale separation `R/δ→0` at fixed offset, and the fold patch energy/source powers are consistent. The global integrable envelope has exponent `4/5`. The fold contribution `M⁻¹/⁷` is strictly lower order than the mean scale, and all probability and two-root factors give the stated beta coefficient.

### Finite precision and global crossover

The local uncertain-center scaling has both the correct response factor and uncertainty argument. Its moving harmonic tests give the lower bound `C0 η¹/⁴` against arbitrary unit mass. The padded interval upper trial gives the same large-width coefficient. The quadratic-tail free-endpoint lemma retains the slower source tail `L⁻¹/²`; its point estimate is sufficient for boundedness and cutoff approximation when `α<2`.

Existence and continuity of the local value are proved separately from the endpoint formula. In the compactness argument, filling missing absolutely continuous mass can only improve the response, so tightness need not be assumed. Lower semicontinuity permits simultaneous center and measure limits. Upper semicontinuity uses a fixed regularized positive-tail profile, so it does not assume uniform continuity of arbitrary optimizing densities.

Conditional reflection symmetry is valid for each offset in a bin. It therefore permits half the budget on each half-circle even for a nonsymmetric bin. Compact-test localization and Fatou give the unrestricted conditional lower bound. The exact cosine coordinate and scalar normalization give a matching per-bin recovery, with bounded exterior response. Compactness/continuity or a finite profile cover supplies the uniformity required by the changing Riemann sums.

The fold-bin treatment uses `W=Δ+M²/⁷`, keeps roots a fixed relative distance from patch endpoints, and bounds the integrated cost by `M⁻¹/⁴W³/⁸`. It does not substitute an invalid unbounded-parameter whole-line equivalent for finite-interval control. I checked both absorptions: the rootless contribution `W⁻¹/²` is within this bound, and the complete fold contribution is lower order than the two-term global scale for every relative limit rate.

For finite scaled resolution, the two omitted regular-fold envelopes have exponents `4/5` and `7/8`, both integrable. Their coefficients remain bounded when `Δ/M¹/⁵` remains bounded. The normalized fold error tends to zero, including the endpoint `τ=0`. The resulting `H` is finite and continuous. For the simultaneous coarse limit, the manuscript supplies a separate uniform moving-root certificate and padded recovery; it does not exchange the joint limit with a later `τ→∞` limit. The conditional coefficient `2^(5/4)C0 a⁻⁷/⁸` integrates with density `1/4` to the displayed `Kcoarse`. Fixed partitions, noiseless equal-bin policies, nested refinements, and physical optimal-value transfer are all distinguished correctly.

## Numerical, build, and presentation checks

I built the exact frozen source in `/tmp/transport-final-review5-6tbm8cry` with a fresh `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error` invocation. It returned success and produced 54 pages. The final log contains no warnings, undefined references/citations, or overfull/underfull boxes. I inspected contact sheets covering all 54 pages for clipping, misplaced material, broken equations/tables, and figure/caption layout. No such defect was visible. Source reading supplied the detailed equation and prose review that thumbnail inspection cannot provide.

I independently assembled a dense incidence-matrix version of the uncertain-center discretization on 21 cells, with random positive simplex masses and 17 center nodes. Its objective agreed exactly with the band solver in floating point; the maximum gradient difference was `1.33e−15`. A centered mass-preserving directional finite difference differed from the analytic derivative by `6.48e−9` at step `1e−7`.

I re-evaluated all four saved 400-cell profiles from their stored mobility arrays. Their masses equal one to floating precision, their coefficients are nonnegative, their objective discrepancies are at most `1.87e−14`, and their tangent-gap discrepancies at most `7.55e−15`. Re-evaluation on 384 center nodes changes these objective values by at most `5.78e−15` relatively. I also reran the full main circle computation at `M=10⁻³`, `q=1`, 32768 half-wall cells and 48 nodes per subinterval; uniform, predetermined, and observed trial values match the saved values exactly in this environment.

Independent special-function evaluation gives `C0=4.647476009400967`, `Cpl=6.222823736019888`, `K1=18.386063650114284`, `Kobs=22.40462823074913`, `Kcrit=2.0223307639693906`, and `Kcoarse=25.723827388763294`. The oracle/predetermined coefficient ratio is `1.2185657929346865`. The recorded circle spatial refinement percentages recompute as `0.0158412%`, `0.00839274%`, and `0.118360%`, agreeing with the final rounded prose.

The two new trial-asymptotic statements are justified: the unrounded integrable mean shape dominates the rounded one by a factor tending to one, while the critical distance/sine comparison is asymptotically exact on the logarithmically dominant fold approaches. The third-moment graded trial is not assigned the unknown numerical value of the variational optimum.

The discrete tangent bound follows from convexity and linear minimization on the simplex; the derivative includes the correct powers of cell width. The paper clearly restricts that bound to the finite-dimensional quadrature objective and floating arithmetic. It retains the sparse-quadrature failure example and separates optimization, spatial, parameter, and domain uncertainties. It does not infer a continuum upper bound from the plotted markers or claim to have computed `S_q` or the global crossover.

The introduction gives the transport motivation, distinction between information policies, a useful regime table, and a reading map before the long proof sequence. Local rescalings are introduced where used. The discussion maintains the fixed-geometry, constant-affinity, nonzero-speed and stationary interpretation; it explains why whole-line source models are not infinite-wall equilibria. I found no unresolved manuscript placeholder or unsupported extrapolation to noise, fabrication limits, caps, vanishing bulk diffusivity, simultaneous folds, or anomalous displacement statistics.

## Literature positioning

I freshly inspected the primary [2026 risk-design paper](https://arxiv.org/html/2602.19869v1), particularly its introduction and two-positive-conductor formulation, and the primary [Buttazzo–Maestre preprint](https://arxiv.org/pdf/1002.2770), whose setup has positive lower and upper conductivity constraints and random forcing. These support the manuscript's specific comparison; it does not incorrectly apply that positivity statement to all reinforcement literature. I also reopened the [reinforcement preprint](https://arxiv.org/pdf/1506.00141) and the primary records for [Levesque et al.](https://arxiv.org/abs/1211.5224) and [Alexandre et al.](https://arxiv.org/abs/2105.06212).

The manuscript attributes the general compliance, measure, gradient, stochastic-design, rare-bifurcation, and quantization methods rather than asserting that those principles are new. Its mathematical contribution is stated through the specific sharp laws and their hypotheses. The supporting literature record discloses access limits, and neither it nor the paper treats search failure as proof of universal originality. I did not identify a literature-based contradiction to the claimed results. This is a scoped literature assessment, not a claim that every potentially related historical paper has been excluded.

## Required correction

**Minor M1 — stale stage status in auxiliary documents.** Locations: `README.md:3`, `PLAN.md:3`, `notation.md:3`, and `claims-map.md:3,59`. These frozen files still describe Stage 07 as awaiting coordinator verification, whereas this review was commissioned after Stage 07 acceptance. The full-manuscript review should of course remain marked pending until its actual adjudication; the Stage 07 status is the stale part. Update the four documents consistently to record Stage 07 acceptance and the actual final-review status when closing this cycle. This changes no theorem or proof and does not justify a further major-issue review round.

No other valid correction emerged from this independent whole-manuscript audit.
