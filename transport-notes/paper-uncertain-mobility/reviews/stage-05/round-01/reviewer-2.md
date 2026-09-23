# Independent review: stage 05, round 01, reviewer 2

Date: 2026-09-07. Reviewed snapshot `b10b05d41199399897fdd9cc7cc6eab8d0fe2ae90e96c6ff4fa8d7d2ef68b42c`; independently recomputed every manifest hash and all matched. Read the whole new exact-observation section, its author handoff, accepted prerequisites, and supporting notation/bibliography changes. Did not read other reviewers' reports or coordinator checks. No source edits, delegation, or shared-output build was performed.

## Verdict

**Accept Stage 05. No major or minor issue found.** The arbitrary-placement lower bounds, exact local optimizer and uniqueness, explicit physical realization, and measurable oracle policy support the stated results. No future finite-precision theorem is included in this acceptance.

## Independent checks

### Exact polynomial solution, constants, flux, and global optimality

For `p(y)=y-3y³+2y⁴`, direct symbolic calculation independently gives `∫_0^1 p=3/20` and `p′+y²(9-8y)=1`. Thus the even mobility has mass `3aR⁵/80=m`. On the positive half-support the flux is `-Rp(x/R)`, so its negative derivative and the quadratic reaction sum to one. The flux is zero at 0 and R, and reflection gives zero flux at -R as well. The central cusp and slope change at the outer edges therefore produce no distributional source term.

The interior source integral is 10/(aR), with exterior integral 2/(aR). The derivative energy is `m[8/(aR³)]²=12/(5aR)`. Independent integration gives interior reaction energy 38/(5aR); adding the exterior 2/(aR) yields 48/(5aR), confirming all energy identities. Differentiating 12/(aR) with the mass-radius relation gives `-64/(a²R⁶)=-b_*²`.

The candidate is bounded and Lipschitz, has an integrable x⁻² tail, and finite reaction and derivative energies. Cutoff and corner mollification therefore justify its energy representative and the square completion. For a completely arbitrary integrable competitor D, the same approximants have uniformly bounded derivatives converging almost everywhere; dominated convergence against D is legitimate. Their tail derivative is O(L⁻³). This supplies a genuine global certificate, not only a stationary optimality condition.

The equality argument is sound. Strictly smaller slope magnitude outside [-R,R] forces any equality competitor to vanish there almost everywhere. The candidate then attains the extended functional for that competitor, and variations by compact smooth tests give the distributional equation. Since D h_*′ is locally integrable and its derivative is locally integrable, the flux has an absolutely continuous representative. Integrating from the zero exterior flux recovers D uniquely on each open half-support. Values at the isolated center and endpoints are irrelevant to almost-everywhere uniqueness.

### Compact-wall lower localization and budget allocation

The lower proof uses each competitor's actual neighborhood mass b_j. Once M is small, uniformly for all 0<b_j≤M, the cutoff lies entirely on the universal tail `1/(a_{j,+}x²)`. It therefore changes source/reaction terms by a fixed bounded amount independent of b_j. Cutoff slopes on the fixed transition region are bounded, while the central slope grows at least as M^(-3/5); the global slope bound used in the certificate is retained. Potential ordering has the correct direction: k≤a_{j,+}x² lowers reaction cost and improves the trial value. Disjoint supports allow adding tests without derivative cross terms. Zero neighborhood mass indeed gives infinite response by sending an auxiliary profile budget to zero.

Minimizing `∑w_j b_j^(-1/5)` exhausts the budget and gives `b_j∝w_j^(5/6)`; strict convexity proves the minimum. With `w_j=Cpl a_{j,+}^(-4/5)`, this gives the curvature exponent -2/3 and total coefficient `Cpl(∑a_j^(-2/3))^(6/5)` after η→0.

The upper construction has exact budget M. All lower comparison curvatures differ from the true curvatures by the same factor 1-η, so the proposed allocation is also the optimizing allocation for those comparison problems. Zero flux at the support endpoints permits completing the square for arbitrary restricted smooth traces, giving the interior value 10/(a_-R). The exterior reciprocal integral supplies 2/(a_-R), with only bounded fixed-neighborhood errors. This matches the local whole-line coefficient. The order of limits and the absence of a claimed bounded error relative to the exact leading coefficient are appropriate. The extension of uniform-mobility localization to these continuous rates is justified by the actual comparison proof, not by silently applying a C² theorem outside its assumptions.

### Degenerate physical trials and bulk correction

For these particular coefficients, closability follows by exhaustion of the open positive-mobility regions and the fact that the remaining exceptional boundary points have zero Lebesgue measure. The endpoint-capacity estimates are correct: an outer quadratic zero costs O(epsilon) for a unit transition, whereas the central linear zero costs O(1/|log epsilon|) with a logarithmic transition. Both transition L² costs vanish. This permits the domain decomposition used in the comparison argument; it does not impose transmission conditions by assumption.

At fixed M, reaction controls the region away from kinetic centers. On each half-support near a center, weighted Cauchy–Schwarz with D comparable to |x| yields the stated logarithmic pointwise bound after anchoring in a regular subinterval. The logarithm is integrable, so fixed-M coercivity and an L² source inverse follow. Positivity and the comparison k≥a_-x² then give h≤h_- on each support; outside all supports, h=1/k. The endpoint domain facts justify these as local weak comparisons.

Independent maximization of `y²(9-8y)` gives 27/16 at y=3/4. Thus kh is uniformly bounded on each support and equals one elsewhere. The support length is O_eta(M^(1/5)), giving exactly `||kh-1||₂=O_eta(M^(1/10))`. The resulting load convergence in the bulk energy dual supplies the remainder upper limit. For the lower limit, every fixed smooth trace has penalty at most `M||∂s trace||∞²`; smooth bulk tests are dense in the mean-zero energy space. This proves convergence to R0 without requiring a bounded derivative of the bulk maximizer. The text correctly limits this stronger assertion to a fixed kinetic profile and fixed η.

### Separated-root oracle policy and scale separation

For the cosine pair, both curvatures are a=1-c² and each receives mass M/2, so the placement radius is `(40M/(3b))^(1/5)`. In the separated regime, a≥t≥L M^(2/7), hence z=M/a^(7/2)≤L^(-7/2). With η=z^(1/10), delta=η sqrt(a)/2, and b=a(1-η), direct calculation gives

`R/delta=2(40/3)^(1/5) z^(1/10)(1-η)^(-1/5)`.

A sufficiently large fixed L therefore enforces all stated support constraints uniformly. The two comparison neighborhoods are disjoint because delta is a sufficiently small multiple of sqrt(a), which is no larger than the root-to-fold distance. Taylor's inequality gives `|g(r_j+x)|≥sqrt(a)|x|(1-η/4)` on these neighborhoods. Squaring is stronger than the required `k≥a(1-η)x²`.

The reciprocal tail estimate follows by integrating inverse quadratics from R near each root and by quartic fold scaling on the complement. The complementary fold term is O(a^(-3/2)), and R≤c sqrt(a) makes it no larger than C/(aR). Combined with the zero-flux interior bound, this proves `J≤CM^(-1/5)t^(-4/5)` uniformly.

At each fixed interior offset, η→0, b/a→1, and R/delta→0. The sharper exterior contribution within each comparison neighborhood is at most 2/(bR), while the remaining O_c(delta⁻¹) is only O_c(M^(-1/10)), smaller than M^(-1/5). Thus each root contributes the full local 12/(bR), and the two-root coefficient is `2^(6/5)Cpl a^(-4/5)`. The compact-wall lower theorem supplies the reverse pointwise bound.

### Fold and rootless policies, measurability, and averaging

For the fold patch, r=M^(1/7) gives D=r⁶/(2B), operator scale r⁴, and response scale r⁻³. The finite-interval limiting potential `(x²/2-μ)²` cannot vanish identically at any μ in the compact parameter range. Together with the fixed positive derivative coefficient, this gives uniform Neumann coercivity by the stated contradiction argument. Enlarging B provides a fixed scaled margin beyond all roots, and the outside reciprocal integral is O(r⁻³). The middle policy bound is therefore valid on the entire two-sided fold layer.

For rootless offsets, dropping derivative energy gives the correct |t|^(-3/2) bound and a bounded response at fixed exterior offsets. The separated profiles depend continuously in L¹ on their positive widths, amplitudes, and translations. The finite branch partition, fold choices, and null threshold assignments therefore define an actual Borel policy with the exact budget at every offset.

The proposed common dominating function has exponent 4/5 and is integrable. In the fold layer, `M^(1/5-3/7)=M^(-8/35)` is bounded by a constant times |t|^(-4/5) because |t|≤L M^(2/7). On the rootless side, `M^(1/5)|t|^(-7/10)` is uniformly bounded when |t|≥L M^(2/7). This verifies domination in every regime. Density 1/4 and the two-root coefficient therefore produce `Kobs=(2^(6/5)Cpl/4)B(1/2,1/5)`.

For the oracle lower bound, near-optimal Borel policies exist by the definition of the finite infimum. The fixed-offset compact theorem bounds each sequence pointwise; Fatou then integrates those lower limits. No measurable pointwise minimizer or interchange of infimum and expectation is needed. The additional +1 approximation error vanishes after multiplication by M^(1/5). The fold layer contributes M^(2/7)M^(-3/7)=M^(-1/7), correctly smaller than the leading mean. The oracle/blind exponent is `-1/5+1/4=1/20`, and the paired-root coefficient and physical χ cancellation are correct.

### Attribution and presentation

The section distinguishes the local source problem from a stationary infinite-wall process and a proven asymptotic policy from a finite-budget optimum. I checked the cited [Alexandersen–Sigmund accepted manuscript](https://findresearcher.sdu.dk/ws/portalfiles/portal/191660127/ITherm2021_revised.pdf): its metadata and its fixed-volume, constant-optimal-gradient precedent support the limited attribution here. The paper does not claim that general method as new.

No proof-essential gap, unsupported constant, missing physical restriction, or actionable clarity issue was identified. Finite-precision crossover work remains a separate later stage.
