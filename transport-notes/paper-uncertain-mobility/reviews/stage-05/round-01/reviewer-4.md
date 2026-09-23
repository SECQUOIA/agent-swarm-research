# Independent review: Stage 05, round 01, reviewer 4

Reviewer: `paper_reviewer_4`. Date: 2026-09-07.

**Verdict: no major issue found. Two minor mathematical-wording clarifications should be corrected.** The compact placement and exact-observation results, including the original degenerate trials' bulk-remainder convergence, survived this independent check.

## Snapshot and independence

Reviewed snapshot: `b10b05d41199399897fdd9cc7cc6eab8d0fe2ae90e96c6ff4fa8d7d2ef68b42c`. All fifteen hashes in the manifest matched when recomputed. I read the complete new section, handoff, and its accepted variational/localization/transfer prerequisites. I did not read other reviewer reports or coordinator checks, did not delegate, and did not edit manuscript sources. No build was needed.

## Exact whole-line solution and certificate

I independently expanded the profile polynomial and checked the identities. Its integral is 3/20; `p′+y²(9-8y)=1` holds identically. The flux on the positive half is `-R p(x/R)` and vanishes at both ends. Reflection supplies the negative half with continuous zero flux at the center. Consequently no point source is introduced by the source representative's corners.

Independent symbolic integration gave derivative energy coefficient 12/5, interior reaction coefficient 38/5, and total reaction coefficient 48/5, all in units 1/(aR). The inner source is 10/(aR), the exterior source is 2/(aR), and total mass is 3aR⁵/80. These verify the response 12/(aR), the local constant, and the sensitivity `dJmin/dm=-64/(a²R⁶)`.

The lower certificate genuinely applies to arbitrary L¹ coefficients. The source representative is globally Lipschitz, has integrable source and reaction terms, and its cutoff derivative on the far tail is O(L^(-3)). Mollified cutoffs retain a derivative bound tending to b*. Their derivatives converge almost everywhere, so dominated convergence against any finite mobility density is valid even for unbounded competitors. The strict slope inequality outside the support forces a minimizing competitor's mass inside it. First variation at the limiting test then yields an L¹ flux with an absolutely continuous representative, and zero exterior flux fixes the integration constants on both half-supports. This proves the claimed almost-everywhere uniqueness without assuming a classical inverse for the competitor.

## Compact-wall lower bound and direct-support upper bound

The lower proof uses the actual mass bj in each fixed disjoint neighborhood. Because bj≤M, every comparison support is eventually inside the region where the cutoff equals one, uniformly over all positive bj. The cutoff acts only on a tail independent of bj, so its source/reaction error is uniformly Oη(1). Its added slopes are bounded independently of bj, whereas the central optimal slope diverges at least as M^(-3/5); thus the arbitrary local mobility cost is bounded by bj times the central squared slope. The comparison k≤aj,+ x² has the correct direction for a lower variational test. Disjoint supports allow the resulting lower values to add. If bj=0, an auxiliary shrinking profile has zero mobility cost and diverging source-minus-reaction value, correctly giving an infinite response.

Minimizing the sum of weighted inverse fifth powers uses the full mass because the cost is decreasing. The stationary condition gives allocation proportional to `wj^(5/6)`, hence `aj^(-2/3)`, and strict convexity proves the minimum. No localization or concentration of the unknown competing design is assumed.

For the upper construction, the zero-flux interior equation proves the response bound 10/(aj,- Rj) directly for every smooth restricted test, with no endpoint values fixed. Using k≥aj,- x² reduces the response, as required. Outside supports, `2v-kv²≤1/k` provides the remaining 2/(aj,- Rj) term near each defect, up to a bounded fixed-neighborhood error. This is sufficient for the full upper bound, without identifying the global inverse or placing artificial Dirichlet conditions at the support edges. Since all aj,- share the same multiplicative factor, the allocation based on aj is also the minimizing allocation for this comparison family. The limit order in M and η is correct, and the text explicitly avoids an unsupported bounded additive error after that second limit.

## Physical realization and bulk remainder

For the explicit profiles, positivity on each open half-support and zero mobility elsewhere give the stated closability argument by exhaustion of compact positive-mobility subintervals. The central linear zero and outer quadratic zeros have the vanishing transition energies claimed in the proof. These justify a domain with no transmission matching requirement at those points; the wording about traces should be adjusted as in R4-01 below.

At fixed M, the reaction is bounded below away from the kinetic centers. Near a center, weighted Cauchy–Schwarz with D comparable to |x| gives a logarithmic pointwise bound in terms of the form energy and an anchored value. The logarithm is locally integrable, so the scalar L² coercivity argument is valid. This is a fixed-budget bound, not a uniform gap as M tends to zero.

The positive-part comparison with the lower-curvature source representative gives `0≤h≤h_j,-` on each support. Outside, the zero derivative coefficient leaves the multiplication solution `h=1/k`. I checked the bound `max y²(9-8y)=27/16`. Therefore kh is uniformly bounded at fixed η and differs from one only on supports of total length Oη(M^(1/5)), giving the stated L² rate Oη(M^(1/10)). This argument needs the fixed kinetic profile and separated support geometry; it is correctly not used uniformly near an offset fold.

The load then converges in the bulk energy dual norm. Dropping the nonnegative Schur penalty yields the upper limit R0. For a fixed smooth bulk test, using its wall trace as a surface trial bounds that penalty by M times a fixed squared derivative norm. Density of smooth mean-zero bulk tests therefore gives the matching lower limit. This does not assume extra trace regularity of the limiting bulk maximizer. The optimized leading value itself follows separately from the accepted same-budget mixture theorem, so it does not rely on the sharper remainder statement for these particular degenerate trials.

## Exact-observation policy and all parameter regimes

For separated cosine roots, `a=1-c²`, `z=M/a^(7/2)`, and `eta=z^(1/10)` give the displayed support-to-neighborhood ratio. Since a≥t≥LM^(2/7), z≤L^(-7/2). A sufficiently large fixed L therefore ensures eta≤1/2 and R≤delta/2 uniformly. Taylor's inequality gives `|cos(r+x)-cos r|≥sqrt(a)|x|-x²/2`; on the chosen delta-neighborhood its square is at least `a(1-eta)x²`. The two mass-M/2 polynomial profiles thus fit in disjoint valid comparison neighborhoods and have exact total mass M.

The reciprocal integral outside their supports is O(1/(aR)): immediately around each root this is the truncated inverse-square integral, and outside fixed-relative root neighborhoods the fold coordinate gives O(a^(-3/2)), which is smaller since R≤c sqrt(a). The direct-support upper response supplies the remaining same-order term. At a fixed interior offset, the sharper exterior estimate gives 2/(bR) per root, while the part beyond delta is O_c(delta^(-1))=O_c(M^(-1/10)), below the leading M^(-1/5). Together with the interior 10/(bR), and b/a→1, this yields exactly the paired coefficient `2^(6/5) Cpl a^(-4/5)`.

For the fold patch, D=r⁶/(2B), spatial scale is r=M^(1/7), and the rescaled operator has scale r⁴. The potential converges uniformly on the fixed patch to `(x²/2-mu)²` for mu in a compact set. Uniform positive diffusion plus the nonzero integral of every limiting potential proves free-endpoint coercivity by the contradiction argument stated. The integrated inverse scale is r^(-3). The text calls r⁴ an energy scale; this is the small terminology correction R4-02 below, and does not change the correct response calculation.

After increasing B, the patch extends a fixed scaled distance beyond every root in the layer. Its exterior reciprocal integral is then controlled by the x^(-4) tail, giving another O(r^(-3)) term. On the rootless branch, the uniform field and reciprocal-potential bound give |t|^(-3/2). Thus all three response estimates hold over their full assigned regimes.

Translations/dilations of the compact profiles depend continuously in L¹ on the separated-regime parameters, and the remaining branches and thresholds are Borel. The policy is consequently defined measurably with exact mass at every offset, including ±1. Its normalized response has the integrable envelope |t|^(-4/5): the central scale is M^(-8/35), and the rootless comparison reduces to `M^(1/5)|t|^(-7/10)≤C` at |t|≥LM^(2/7). Dominated convergence proves the sharp upper mean. The lower proof uses near-optimal policies and the compact theorem pointwise before Fatou, avoiding an expectation–infimum interchange. The fold layer contributes only O(M^(-1/7)), below the leading mean order, but is correctly retained to make the policy globally admissible.

Independent high-precision evaluation gave `Cpl=6.2228237360198886`, `Kobs=22.4046282307491383`, and `Kobs/K1=1.2185657929346874`, consistent with the displayed constants. These values follow from the analytic formulas, not numerical optimization. The full-bulk factors and oracle/blind exponent difference 1/20 agree with the accepted transfer theorem and predetermined mean result.

## Findings

### R4-01 — Minor: zero-capacity interfaces do not generally have traces

Location: `sections/05-exact-observation.tex`, lines 252–255, especially “permits independent traces of the half-supports and exterior.”

The intended conclusion, that the closure imposes no matching constraint between components, is correct. However, general form-domain functions need not possess finite endpoint traces here. On the exterior the domain is L² with zero derivative energy. Near a central linear zero, a cutoff version of `log log(e/x)` has finite L², reaction, and weighted derivative energy but diverges at the endpoint. Thus literal trace language can suggest more regularity than the proof provides.

Remedy: say that the closure allows the half-support and exterior components to vary independently, with no trace-matching/transmission condition at these zero-capacity points. Add that finite endpoint traces need not exist if helpful. The subsequent weak comparison uses this component separation, not finite traces, so no result needs changing.

### R4-02 — Minor: distinguish the fold operator scale from the integrated energy scale

Location: `sections/05-exact-observation.tex`, lines 411–412.

After `s-s0=rx`, the differential operator has scale r⁴, but for a test `v(s)=phi(x)` the derivative and reaction integrals each have scale r⁵ because ds=r dx. Calling r⁴ the “derivative energy” scale is inconsistent with the integrated-energy terminology in the preceding stages. The subsequent response factor r/r⁴=r^(-3) is correct.

Remedy: replace that sentence by the precise rescaled operator statement, or display the form as `r⁵∫[(1/(2B))|phi′|²+V phi²]dx` and source as `r∫phi dx`. This makes the response scale transparent without changing any bound.

## Overall assessment

No major mathematical or scientific issue was found. The local-mass lower bound, direct-support upper certificate, degenerate-trial bulk corollary, measurable oracle policy, and averaging argument are complete at the claimed scope. Correct and verify the two minor wording points before acceptance. No later-stage finite-precision claim or broad novelty conclusion is certified by this review.
