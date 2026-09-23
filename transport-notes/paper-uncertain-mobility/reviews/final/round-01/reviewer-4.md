# Final whole-manuscript review — reviewer 4, round 01

Snapshot: `e5a8cd3e390d1b7afa16481b35bcd01944a8111bce55e2ffaf1570f40ebc899d`.

## Verdict and independence

**No major issues identified. No mathematical or scientific correction is requested.** One minor repository-status inconsistency should be corrected before final delivery. Subject to that housekeeping change, I recommend acceptance of this manuscript in the final review process.

I verified all 28 manifest hashes both before and after the review; all matched. I read the complete manuscript, including every proof in Sections 01–06 and the introduction, numerical section, and discussion. I checked the bibliography, relevant source comparisons, code/data evidence, and the scope inventory. I did not read other reviewers' reports, coordinator checks, or prior adjudications, and did not use stage acceptance as evidence for a mathematical claim. I did not delegate or change manuscript files. The only repository file written by this review is this report.

This report identifies the checks supporting its verdict; it does not promise immunity from an unknown future peer-review objection.

## Findings requiring correction

### Minor — preparation status is stale in several live supporting files

Locations: `README.md:3`, `PLAN.md:3`, `claims-map.md:3`, and `notation.md:3`.

These live status paragraphs still say Stage 07 corrections await coordinator verification. The final-review assignment explicitly occurs after Stage 07 acceptance. The historical freeze should remain preserved, but the live documentation should describe the current state consistently.

Remedy: during final delivery, update these four paragraphs together to distinguish completed staged drafting from the final whole-manuscript review and its actual outcome. A simple pointer to the review ledger plus an accurate short current status is enough. Do not declare final acceptance before the coordinator completes the requested review/correction process. This does not affect the compiled scientific manuscript and does not require another five-reviewer major-issue cycle.

## 1. Physical model, dimensions, and variational transfer

I independently checked the exchange signs in the forward equations. The bulk boundary loss is exactly the wall gain; constant bulk concentration and wall concentration K times that constant give the stated stationary measure. The divergence-form tangential generator preserves that measure. The backward boundary condition obtained from the symmetric energy has the correct opposite-wall-trace coupling. The process construction on the disjoint union of closed bulk and wall uses a dense regular form core; the bulk trace coupling is continuous in the product form norm. For a positive floor the mean-zero coercivity proof controls both components, rather than assuming bulk connectedness alone controls a possibly isolated wall.

The stationary finite-time covariance formula and its nonnegative spectral measure prove the extended long-time coefficient directly. In particular, a zero spectral component contributes linear growth to variance divided by time, hence an infinite coefficient; it is not silently removed. The full variational formula has the correct factor Z. The independent axial Brownian driver has zero conditional mean, so its covariance with the advective displacement vanishes even though its local variance depends on the transverse path.

The dimensional accounting is consistent: M has units L^3/T; J has units LT; chi has units L/T^2; thus chi J has units L^2/T. The dimensionless response acquires the factor ell_ref/k_ref before multiplication by physical chi. All subsequent budget powers and logarithms use the fixed dimensionless units.

The scalar class and physical class remain distinct throughout. Positive-floor closability is proved without an upper bound on D. The source quotient, nonnegative inverse, constant-test identity, and measurability from countable smooth tests are sufficient for later optimization. The finite-response extension of the Schur calculation correctly uses an energy completion and the image sqrt(k) h in L2, not an assumed L2 corrector. Its load is bounded by the bulk gradient, so its remainder is finite.

Completing the surface square gives the signs `+K V^2 J`, `-2 K V int(kh)b`, and a nonpositive Schur penalty. The load kills common constants because `int(u-V)=KPV` and `int kh=P`. The logarithmic remainder follows from nonnegative w=kh of fixed mass, its O(1/m) supremum bound, and the one-dimensional H^(-1/2) Fourier split. Squaring the dual load bound produces one logarithm, not its square. The theorem explicitly excludes a joint vanishing-D_b uniform estimate.

As an independent normalization check, for a disk of radius R, constant bulk velocity U, and constant rate k, the constant surface solution has J=P/k and w=1. The radial bulk solution has derivative `f_0'(r)=-(U-V)r/(2D_b)` and satisfies the stated boundary flux because `V=UR/(R+2K)`. Its contribution is `R_0=(U-V)^2 pi R^4/(8 D_b Z)`, and its trace is constant, so the Schur penalty vanishes. The resulting `D_flow=chi P/k+R_0` has the expected positive exchange contribution and dimensions. In the perfectly mixed bulk reduction, its exchange term also agrees with the elementary two-state occupation-time calculation.

The same-budget mixture preserves measurability, total mass, and information timing. Form ordering gives J(D_theta) <= J(D)/(1-theta), including for the larger scalar class. Minkowski for q>=1 and subadditivity for q<1 yield the stated comparisons. The pointwise bump on a positive-probability regular-root event justifies the observation-uniform M^(-q/5) lower bound and both relative-error rates.

## 2. Local defects and the undesigned baseline

The expanding-interval proof controls the source tails as well as energy, which is essential because the constant source is not in L2 on the line. Neumann bracketing is consistently used as an upper bound; compact zero-trace trials give the lower bound. The weighted version only uses uniform comparability plus local convergence, with a confining potential anchor.

I checked the double Gaussian integral of the oscillator kernel and the beta substitution, recovering `C0=pi Gamma(1/4)/(2 Gamma(3/4))`. Quadratic localization gives the integrated response scale epsilon^(-1/4) a^(-3/4). The quartic local operator scale is epsilon^(2/3) b^(2/3), while its integrated inverse scale is epsilon^(-1/2)/b; these are not confused. The separated positive pair tail contains two roots of curvature 4 mu, giving C0/sqrt(2), and the negative tail is the reciprocal integral pi/2 times |mu|^(-3/2).

The cosine bounds cover compact fold parameters, separated roots, rootless offsets, and their overlap. The shrinking root neighborhoods in the sharp matching statement are large in oscillator units and small relative to separation. This separate argument avoids improperly using a compact-parameter interval limit at diverging parameters.

The moment coefficients correctly include the offset density 1/4, two folds, paired roots, and fold Jacobian `(epsilon/2)^(1/3)`. The critical inside logarithm is justified by an explicit cutoff argument. The second moment dominates the squared mean, yielding the stated variance order; neither is confused with a particle displacement moment. The exact limiting law has the correct half-mass atom at zero.

For the stronger uniform bulk limit I checked `k''=2(1-c^2)+6c(c+cos s)-4(c+cos s)^2` and the flux identity. The response and spectral-gap bounds give `||kh-1||_2^2=O(epsilon^(1/6))`, hence the stated exponent 1/12. The limiting Neumann problem has the correct compatibility condition. Its H2 regularity is used only where warranted, and the Schur comparison gives the claimed uniform remainder limit.

The Gaussian counterexample is a global-amplitude obstruction: the constant trial gives J>=2P/R^2 for every design, so mobility cannot cure its infinite mean. The local zero sum's finite first moment does not contradict this. The marked Kac–Rice calculation uses first-root weighting, including for the diagonal lower bound on the second moment, and does not assume independence of zeros. The mean-rate replacement inequality follows immediately by discarding derivative energy and accurately illustrates a different failure of averaging.

## 3. Sharp predetermined moments and generic folds

Convexity for every q>0 follows from the quotient supremum of convex negative powers, not from the false general claim that raising an arbitrary convex positive function to q<1 preserves convexity. The two cosine symmetries preserve the ensemble and the budget.

The elementary shell lower bound uses only local mass and the averaged translated derivative kernel. Its critical sum has N~log(1/M) disjoint shells and gives N^(7/5) M^(-2/5). The whole-budget fold bump gives M^((2-3q)/7). Both apply to arbitrary L1 competitors, including zero local mass.

For the sharp moving-root certificate I checked the paired-root probability factor `2^(q-3)`, the derivative-kernel scaling M^(-1-q/4), and the cancellation after integration against the total mass M. The reference density makes the spatial coefficient constant. Truncation at arc ends only reduces the nonnegative kernel. At criticality the shrinking arcs have an explicitly vanishing relative test width, so the relative reaction and Jacobian errors are controlled uniformly against concentrated competitors.

The graded upper estimates protect ordinary roots as well as the fold core and rootless side. The identity

`2 - 3q/2 + alpha_q q/4 = (8-5q)/(q+4)`

is correct. The subcritical dominating exponent is `7q/[2(q+4)]<1`. At criticality the four one-sided fold approaches give `Z_R~(4/7) log(1/M)`; the omitted inner annuli cost only log log, and the core/rootless terms lack the leading logarithm. As a separate limiting check, alpha_(2/3)=0, and K_(2/3) reduces to the corresponding uniform-mobility coefficient after epsilon=M/(2pi).

For supercritical attainment, compact-test lower semicontinuity has the correct direction under vague convergence. Derivative flattening on small neighborhoods of compact null sets removes the singular measure while preserving the source and reaction and the absolutely continuous derivative energy. The correction restoring zero derivative integral also has vanishing singular energy. The mass scaling exponent `(3q-2)/7` is positive and strictly decreases cost with usable mass. Therefore the minimizing-sequence argument rules out both escaped and singular mass; the attained object is genuinely an L1 density.

The two-fold lower blowup includes no hidden regularity hypothesis. Minimization of the sum of negative mass powers enforces half the total mass at each fold for sharp asymptotic optimality. The exact sine-coordinate recovery cancels the derivative metric through the chosen factor w, while its mass contains w^2; the common normalization tends to one. The graded positive tail supplies both natural-endpoint convergence for a possibly unbounded density and an integrable global parameter envelope. The resulting coefficient is `2^((11q-12)/7) S_q`, independently confirmed by algebra. A named infimum is therefore not being substituted for a missing sharp-limit proof.

The generic-family theorem explicitly assumes transverse, positively sampled, finitely many distinct fold sites and values. Compactness supplies the uniform root count and rate anchor. The normal form has enough regularity under C4, and ordinary roots are not assumed to move with c. Choosing a nonnegative grading exponent when q<=2/3 is necessary to protect an ordinary root that happens to occupy another parameter's fold site. The partition upper bounds, extra ordinary-root contribution, and exponent integration establish all three orders. The full-bulk ratio is stronger than an order comparison but follows from the general transfer theorem without claiming generic cosine constants.

## 4. Exact observation and finite precision

I directly verified the polynomial identity, mass, flux, and energies of quadratic placement: `int_0^1 p=3/20`, `p'+y^2(9-8y)=1`, integrated derivative energy `12/(5aR)`, reaction energy `48/(5aR)`, and total response `12/(aR)`. The saturated slope controls all competing L1 coefficients. Equality forces exterior zero mobility and the distributional flux equation, which gives the claimed almost-everywhere uniqueness. Corners and cutoffs are handled with bounded derivatives, so no extra regularity of a competitor is assumed.

Compact-wall localization uses actual masses in disjoint fixed neighborhoods, with uniform bounded cutoff errors before sending the curvature tolerance to zero. The local upper bound uses the support equation with free traces and then adds the reciprocal exterior response. Minimizing the sum of negative mass powers yields `m_j proportional to a_j^(-2/3)`. The physical corollary treats the linear central and quadratic outer zeros through their zero capacity rather than assuming transmission or finite endpoint traces. The L2 flux estimate follows from bounded kh-1 on total support O(M^(1/5)); the limiting remainder follows by smooth bulk tests without an unnecessary regularity assumption on the bulk maximizer.

The oracle proof defines a Borel policy and then proves its expectation, rather than interchanging an uncountable infimum with expectation. The separated branch has an explicitly smaller support than its quadratic-comparison neighborhood. The fold patch has enough margin beyond all roots, with coercive free-endpoint forms and a controlled reciprocal exterior. Its O(M^(-1/7)) ensemble cost is smaller than the leading M^(-1/5). The uniform exponent 4/5 is integrable, and Fatou supplies the unrestricted lower bound. The factors in K_obs and the M^(1/20) ratio are consistent.

For uncertain centers, the exact change of variables gives `a^(-4/5)m^(-1/5) F_ctr(w/(m/a)^(1/5))`. The translated oscillator certificate gives C0 eta^(1/4) for every eta, not only asymptotically. The padded constant design gives its sharp large-eta endpoint. Attainment of F_ctr correctly uses a different argument from S_q: after vague convergence and singular-mass removal, any missing mass can be added without raising cost. Strict tightness of the original sequence is not claimed. A positive-tail regularization and quadratic source-tail control prove upper semicontinuity, including at eta=0.

Conditional localization first uses reflection valid within each individual bin to fix half-wall masses. Its scaled potential converges uniformly on compact sets, with the correct eta_I and factor `2 a_I^(-1) ell_I^(-1)`. The exact-coordinate recovery has the correct metric and exact total mass after normalization. Compact parameter continuity allows finitely many regularized profiles, so the upper statement is a genuine bin-based policy.

The global bin envelope is essential and sufficient. Regular patches cover every root location with a margin in harmonic units. Fold-bin groups have total width controlled by W=Delta+M^(2/7) independently of alignment, and their integrated response is `O(M^(-1/4) W^(3/8))`. The remaining rootless integral is absorbed using W>=M^(2/7). These terms are negligible relative to the sum in the joint order law. On compact regular offsets the conditional values give Riemann sums; the exponents 4/5 and 7/8 make the omitted fold approaches integrable. Thus the finite-ratio crossover is proved globally, including tau=0.

I separately checked the simultaneous coarse proof. Its condition is b/w->0, so padded constant mobility and the unrestricted moving-root certificate have the same coefficient. The exterior error is o of the root response. Integration gives `2^(-3/4) C0 B(1/2,1/8)`. The coarse limit is not obtained merely by taking tau large after a finite-tau theorem. The binary-digit interpretation, nested-partition monotonicity statement, and physical relative-error transfer all retain the exact per-observation budget.

## 5. Numerical evidence, literature, and presentation

I reevaluated all nine saved uncertain-center designs, including the refinements and deliberately underresolved quadrature case, from their stored mobility vectors. All were nonnegative and had unit mass to roundoff. Maximum relative objective and validation errors against the saved values were about 3e-15; absolute gap discrepancies were below 8e-15. I also reran the full q=3, M=10^(-12), 32768-cell, 48-node-per-subinterval circle computation: both raw moments reproduced exactly, including the ratio `0.03481435853950191`. This is verification of the stored evidence, not a new continuum convergence certificate.

The finite-volume conductance, integral response normalization, exact discrete budget, averaged exterior tail, analytical objective gradient, and convex tangent gap all agree. The current numerical discussion explicitly acknowledges when spatial/domain changes lie below optimization uncertainty. It does not call a discrete tangent interval a continuum interval, or a trial a finite-budget optimum. The two small new trial arguments justify the unrounded mean and distance-based critical profiles with the correct leading constants.

Independent symbolic/numerical checks recover:

- C0 = 4.647476009400967;
- Cpl = 6.222823736019888;
- K1 = 18.386063650114284;
- Kcrit = 2.0223307639693906;
- Kobs = 22.40462823074913;
- Kcoarse = 25.723827388763294;
- Kobs/K1 = 1.2185657929346865.

I inspected the source comparisons and bibliography without treating search failure as proof of novelty. The general transport precedent is accurately credited to [Levesque et al.](https://arxiv.org/abs/1211.5224) and [Alexandre et al.](https://arxiv.org/abs/2105.06212). The specific distinction from positive-conductivity stochastic designs agrees with [Buttazzo–Maestre](https://arxiv.org/abs/1002.2770) and the explicit `0<alpha<beta` model in [Alphonse–Kunštek–Vrdoljak](https://arxiv.org/html/2602.19869v1). It is not incorrectly applied to the degenerate mass-design literature. I inspected [Buttazzo–Oudet–Velichkov, Proposition 4.1 in the preprint](https://arxiv.org/pdf/1506.00141), which supports the credited measure-relaxation and gradient-constraint methods. The manuscript proves its additional line, singular-mass, and parameter-integration arguments itself.

I checked the first and weighted Rice hypotheses against [Azaïs–Wschebor, Theorems 6.2 and 6.4](https://www.math.univ-toulouse.fr/~azais/styles/other/student/level.pdf), including the bounded continuous mark approximation. The contextual rare-bifurcation comparison agrees with the moments described in [Berry–Keating–Schomerus](https://michaelberryphysics.wordpress.com/wp-content/uploads/2013/07/berry320.pdf). Additional searches for uncertain surface-diffusion optimization and vanishing-reaction design produced no identified exact prior statement of these laws; that limited search is not an absolute novelty guarantee. No unsupported broad priority claim is made in the manuscript.

The paper's physical question and assumptions are understandable to transport researchers: it optimizes variability of spreading among fixed channels with fixed equilibrium speed. It clearly states the independent-control idealization, fixed bulk diffusion, known fold geometry, static noiseless quantization, and unrestricted fabrication class. The proofs are long, but the introduction, regime table, section progression, and discussion explain why each layer is needed. The scope inventory covers the uncertainty, moment, observation, and finite-bulk developments; unrelated deterministic phase diagrams and traveling-channel questions are not prerequisites. I found no promised theorem left as an unresolved argument.

I built the current frozen draft in the private directory `/tmp/final-r4-RL0Zn2`. The build produced the complete 54-page PDF with no final warnings, undefined references/citations, or overfull/underfull boxes. The bibliography contains the expected 16 entries. The two figures and their labels distinguish numerical trials and discrete values from proved continuum coefficients. No scientific rewrite or further mathematical investigation is required by this review.
