# Independent review: Stage 06, round 01, reviewer 4

Reviewer: `paper_reviewer_4`. Date: 7 September 2026.

**Verdict: no major mathematical or scientific issue found. One minor incorrect cross-reference should be fixed.** The conditional localization proof and fold envelopes support the new exact finite-ratio crossover, rather than merely checking its endpoint consistency.

## Snapshot and independence

Reviewed snapshot: `fd49a0c7de991734f21f20428b8a74ba19e44a0ffa3204ed80a925056ab5fb2f`. I independently recomputed all sixteen hashes in the manifest; all matched. I reviewed the entire finite-precision section, its handoff, notation and claim updates, and the accepted model, local-limit, measure, placement, and transfer prerequisites. I did not read other reviewer reports or coordinator checks, did not delegate, and did not edit manuscript sources. No build was needed.

## Information structure and exact budgets

The optimization is correctly defined over one coefficient per observed bin. There are finitely many choices at each M and Δ, so the sum of conditional infima equals the infimum of the sum by choosing a separate near-minimizer in each bin. This is valid without a measurable selection theorem. The policy space does not pool mass across observations. Reusing a single budget-M coefficient across a group of fold bins still gives mass M for every bin; it does not charge that mass repeatedly to one shared budget or grant extra information.

Reflection in arclength preserves every cosine rate individually. Therefore symmetrizing within a bin is legitimate even when the bin is not symmetric under changing c to -c. A reflected design has exactly half of its mass on each half-circle because the endpoints are Lebesgue-null for L¹ fields. This justifies the half-budget scale in the conditional local problem. Later regularization and scalar normalization use only the bin, preserve reflection, and impose the exact total mass M.

## Local uncertain-center value

The local scaling is correct: with ell=(m/a)^(1/5), coefficient `D=a ell⁴ d`, and source field `h=(a ell²)^(-1)f`, the source, derivative energy, and reaction energy have common response factor `1/(a ell)=a^(-4/5)m^(-1/5)`. Center uncertainty width is divided by ell, as displayed.

The expanding-interval lemma retains the correct quadratic source-tail decay L^(-1/2), rather than the faster quartic estimate from the preceding stage. On the compact core the positive mobility background and a positive-potential interval anchor the H¹ norm. Outside, the reaction controls x²f². Local weighted derivative compactness identifies the limit distributionally because d is bounded below on compact intervals. The Sobolev estimate combines local squared norms of orders |x|^(-2) and |x|^α, producing the cross term |x|^(α/2-1). Since α<2, the resulting boundedness of the limit makes the extra cutoff derivative energy vanish against integrable d. Weighted derivative approximation on compact intervals, with its integral correction where required, completes the density argument. This supplies both the free-endpoint upper limit and the compact-test lower limit even for unbounded d and asymmetric expanding intervals.

The fixed-profile continuity argument also has the needed global control: on compact center ranges, the energy controls `∫(1+x²)f²`, while changing the center changes the potential by at most a constant times the center displacement times `(1+x²)`. Nearby forms therefore compare multiplicatively and their inverse responses are continuous.

For the local lower bound, exact observation gives Tz(d)≥Cpl at every center for mass one. I separately checked the translated-oscillator calculation. The test amplitude is η^(1/2) and its width η^(-1/4); source and reaction each scale as η^(1/4). Averaging its squared derivative over a center interval of width η gives a pointwise kernel bounded by η^(1/4)Tψ. Integrating against arbitrary unit mass then yields the exact lower bound C0η^(1/4), with no smooth-design assumption.

The padded constant-mobility trial proves finiteness and the claimed large-width constant. Every center is at least unit physical distance from each patch endpoint, while the harmonic length tends to zero. Thus both endpoint distances diverge in harmonic units, uniformly in the center, and the interior response has coefficient C0. The exterior reciprocal-potential contribution stays bounded and is lower order.

The local existence proof does not improperly use the strict mass scaling of the different quartic problem. Vague lower semicontinuity of compact-test responses remains valid under simultaneous center convergence. Removing singular measure mass has the same derivative-flattening proof, since the new potential is still locally bounded. Any missing absolutely continuous mass can then be replaced by a nonnegative density, decreasing the response. This yields a unit-mass minimizer with cost no larger than the liminf. It also proves lower semicontinuity of the optimum as η varies. Upper semicontinuity follows from a fixed positive-tail regularization and form ordering; its uniformly continuous response on compact center ranges justifies averaging. The claims of attainment, continuity, and an even minimizer therefore follow without a uniqueness or width-monotonicity assumption.

## Uniform conditional variational localization

For the unrestricted lower bound, the normalized half-circle mobility measures have mass one and vaguely converge, after a subsequence, to a measure of mass at most one. The ordinary-root expansion has sign `eta_I v-x` and the correct normalization `sqrt(a_I) ell_I`; squaring gives the local uncertain-center potential. Reflection creates two identical test contributions with disjoint supports. Their shared integrated-inverse factor is `2/(a_I ell_I)`, equal to `2 a_I^(-4/5)(M/2)^(-1/5)`.

At each fixed parameter v, compact-test insertion proves the local liminf before taking a supremum. Fatou then gives the conditional integrated lower bound. Completing any lost mass to a unit density decreases the limiting cost and therefore compares it in the correct direction with Fctr. Continuity of Fctr and subsequence compactness turn this into uniformity on a fixed regular offset set. The proof makes no restriction on the competing field's fine structure or concentration.

For recovery I independently checked the exact coordinate and metric factors. Since `dx/ds=sin(s)/(sqrt(a_I)ell_I)`, the Jacobian is `ds=ell_I w_I dx`. The rate is exactly `a_I ell_I²(x-eta_I v)²`. Choosing mobility `a_I ell_I⁴ w_I d` cancels the metric in the derivative energy, while the source and reaction carry the bounded factor w_I. Its mass is `m∫w_I²d`, tending to m; normalizing the two reflected patches restores the exact budget and changes response only by a factor tending to one.

All possible roots in a regular bin eventually lie strictly inside the fixed neighborhoods. The exterior reciprocal-potential integral is consequently uniformly bounded and vanishes after response normalization. The quadratic free-endpoint lemma controls each interior response, including integration over the compact center range. A finite cover by fixed regularized profiles is enough to make recovery uniform. It introduces no hidden pointwise optimizer selection and respects the available information.

## Global envelopes and fold-bin control

For a regular bin at distance t from a fold, possible roots span an arc of length comparable to `w=Δ/sqrt(t)`. With placement padding `ell=(M/t)^(1/5)`, the patch mobility is comparable to M/(w+ell). The condition `t≥C(Δ+M^(2/7))` makes the patches disjoint and keeps them in quadratic neighborhoods. The harmonic width is no greater than a constant times ell, so all roots have enough endpoint margin. The interior response is bounded by `e^(-1/4)t^(-3/4)`. Its scale dominates both exterior terms `1/(t ell)` and t^(-3/2). Expanding `(w+ell)^(1/4)` gives exactly the two exponents t^(-4/5) and t^(-7/8) in the regular envelope.

For the fold groups, taking patch radius of order sqrt(W), W=Δ+M^(2/7), gives constant mobility e comparable to M/sqrt(W). The inequality W≥M^(2/7) implies W≥c e^(1/3), so the parameter group contains the quartic layer at its appropriate scale. The integrated inner and rootless contributions are O(e^(-1/6)); the separated-root contribution is O(e^(-1/4)W^(1/4)). The latter absorbs the former under that inequality. Substitution of e gives M^(-1/4)W^(3/8). The fixed scaled endpoint margin permits the finite-interval Neumann estimates even when the quartic-scaled patch radius is merely bounded below rather than tending to infinity. The text explicitly relies on the bracketing proof for this reason.

The exterior patch response and all remaining rootless bins cost O(W^(-1/2)). They are absorbed because `M^(1/4)W^(-7/8)≤1`. Enlarging the fold groups by whole bins changes their widths only by fixed factors, since Δ≤W. This is the needed grid-alignment control for bins containing or adjoining a fold.

The unrestricted coarse-order lower test is also correctly normalized. Its width is b=(M/Δ)^(1/4), amplitude γb^(-2), source-minus-reaction of order `(γ-Cγ²)b^(-1)`, and averaged derivative kernel at most `Cγ²/(Δ b⁵)`. Multiplication by arbitrary mass M gives a cost of order γ²b^(-1), so a fixed small γ gives the claimed lower bound. A regular collection of bins has probability bounded below. The oracle bound handles the remaining precision range. Thus the maximum of the two lower bounds is comparable to the claimed sum.

The fold error is uniformly lower order at all relative rates: its two upper components are M^(-1/7) and M^(-1/4)Δ^(3/8), compared respectively with M^(-1/5) and M^(-1/4)Δ^(1/4). The separate fixed-N exponent statement also follows: a positive-length regular part of one bin gives the moving-root lower bound, while a predetermined design supplies the upper bound. It does not assert the small-Δ coefficient for a fixed partition.

## Exact crossover and simultaneous coarse limit

On a compact regular offset interval, uniform conditional localization and continuity supply the stated Riemann-sum limit. The coefficient `2^(6/5)/4` comes from two half-budget root problems and density 1/4. The local uncertainty argument is `2^(1/5)tau a^(-3/10)`. Discarding all other bins gives the lower global limit. For the upper limit, the omitted regular contribution is controlled by the integrable powers t^(-4/5) and t^(-7/8), and the normalized fold contribution tends to zero. I independently checked its powers: M^(2/35) and, for bounded Δ/M^(1/5), M^(1/40). Sending the compact interval to the root-containing region then proves the finite-ratio theorem, including tau=0.

The separate coarse argument avoids the invalid inference that an iterated large-tau limit proves a simultaneous one. On compact regular sets, each root arc has width `w=Δ/sqrt(a)[1+o(1)]`; with e=M/(2w), the harmonic width b=(e/a)^(1/4) satisfies b/w→0. Paired translated harmonic tests give the source/reaction factor 2z0 and a derivative kernel whose multiplication by total mass M=2ew yields 2z0Tψ. Edge truncation cannot increase that kernel. Taking the oscillator supremum therefore gives the unrestricted coefficient 2C0z0.

For the upper construction, padding with p=sqrt(bw) makes both p/b tend to infinity and p/w tend to zero. Hence endpoint localization is uniform while the patch mobility remains e[1+o(1)]. The exterior reciprocal response has relative size b/p→0. The resulting conditional coefficient is `2^(5/4)C0 a^(-7/8)M^(-1/4)Δ^(1/4)`. Integrable omitted-root bounds and the normalized fold estimate O(Δ^(1/8)) allow integration over the ensemble. Multiplication by density 1/4 yields `2^(-3/4)C0 B(1/2,1/8)`.

I independently checked the crossover-integral curvature exponent -7/8 and the power of two -3/4. The large-tau behavior of H follows from the local endpoint theorem and the same integrable bound, and is correctly presented as additional consistency rather than as the simultaneous-limit proof.

## Physical scope, dimensions, and interpretation

The full-bulk comparison applies to the bin observation law at every M and N, including laws changing with M. It preserves each bin's mass and information by the same uniform-background mixture, giving the accepted observation-uniform relative error `CM^(1/5)log(1/M)` for the mean. It compares optimized values rather than asserting a small remainder for arbitrary original rough local minimizers. The local whole-line measure problems remain scalar compactness devices and are not assigned stationary particle processes.

Physical coefficients require the response conversion `ell_ref/k_ref` in addition to the physical χ and the dimensionless-budget substitution established earlier. The stated local criterion `Δ∼m^(1/5)a^(3/10)` follows from equating root-span uncertainty Δ/sqrt(a) with placement width (m/a)^(1/5). The binary-resolution formula includes the fixed interval-length factor in its O(1) term. A further binary digit gives the claimed factor only within the sharp coarse regime, as stated. The nested-partition comparison is valid by policy inclusion; no ordering of arbitrary nonnested partitions is inferred. The final paragraph correctly limits the model to noiseless quantization before a static design, without optimizing the observation channel or introducing a measurement cost.

## Finding

### R4-01 — Minor: incorrect reference for the exact sine coordinate

Location: `sections/06-finite-precision.tex`, lines 448–450.

The sentence refers to “the exact sine coordinate of `eq:fold-scaling`.” That label in Section 02 contains the generic whole-line fold rescaling `(ell,mu,x=ell y)`, not the sine-coordinate identity. The sine coordinate `z=2sin((s-sj)/2)` is introduced in the proof of the uniform cosine localization lemma.

Remedy: refer to the proof of `lem:cosine-uniform`, or explicitly state the sine coordinate in this sentence. The estimate itself is correct; this is a navigation/reference correction.

## Overall assessment

No major issue was found. The local existence and continuity argument, arbitrary-design conditional liminf, exact-budget recovery, fold envelopes, and independent simultaneous coarse proof together resolve the previous interior-crossover gap at the stated scope. Correct and verify the one minor cross-reference before acceptance. Numerical evaluation of the attained continuum value and the full manuscript's literature positioning remain later-stage work.
