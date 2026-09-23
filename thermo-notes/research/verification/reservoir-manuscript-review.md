# Fresh-reader review of the reservoir coexistence manuscript

Reviewer: independent subagent `capacity_review`. Date: 2026-09-06.

Reviewed `research/reservoir-coexistence-manuscript.md` as a new reader, with a separate derivation of its main implications. After that derivation, consulted the earlier physical-bath and microscopic-Potts reviews to check that the manuscript retained their assumptions. This review did not repeat the established numerical calculations.

**Verdict:** no substantive mathematical error or omitted assumption invalidating either stated iff theorem was found. The arbitrary-total-energy necessity argument is sound for every positive bath exponent. The two-phase sufficiency proof controls potentially amplified valley mass, the three-phase proof needs no additional quantitative valley bound, and the boundary-scale formula correctly accounts for unequal phase variances. The microscopic Potts realization has the stated weights, variances, and sufficient density control. Priority and short-range physical applicability remain separate unresolved questions, as the manuscript says.

## 1. Exact reservoir model and scope

Equation (4) follows directly by multiplying the subsystem density of states by `(total_energy-E)^c` and dividing by the canonical Boltzmann factor. Its likelihood ratio depends only on subsystem energy. Thus full subsystem-state total variation equals energy-law total variation; no reduction error is hidden by studying energy alone. This exact equivalence uses the stated neglect of subsystem–bath interaction energy in the equilibrium measure.

The bath convention is consistent. A surface density proportional to `U^c` has surface inverse temperature `c/U` and surface-entropy heat capacity `k_B c`. A quadratic bath with `f` degrees of freedom has `c=f/2-1`, while its canonical heat capacity is `k_B(c+1)`. The manuscript keeps this finite offset explicit.

The asymptotic problem fixes positive `beta`. The statements are not uniform claims for a temperature that itself tends to zero, vanishing phase weights, vanishing within-phase variance, or changing phase separation scales. Those situations fall outside the explicit hypotheses.

## 2. Necessity under arbitrary tuning

The key local lemma is valid with the local L1 hypothesis in Equation (6); pointwise convergence of densities or likelihoods is unnecessary. On any fixed standardized interval, the limiting Gaussian density has a positive lower bound. If `TV(P_N,Q_N)` tends to zero, the likelihood ratio tends to one in canonical probability, and therefore its logarithm tends to zero in Lebesgue measure on that interval.

A cutoff cannot evade this conclusion. If the standardized bath cutoff remained bounded above along a subsequence, a fixed Gaussian interval above it would retain positive canonical probability but zero bath probability. Hence every fixed local interval is eventually inside the domain of the concave log likelihood.

For completeness, select four points with log-likelihood values tending to zero in separated intervals to the left and right of the origin. Concavity bounds the derivative at zero between the outer secant slopes, both tending to zero. A chord through points on opposite sides bounds the center value below; continuation of a left secant bounds it above. This establishes both parts of Equation (7).

Consequently the two bath inverse temperatures satisfy `beta_B,±=beta+o(N^(-1/2))`. Their reciprocal difference is exactly `Delta_N/c_N`. Since reciprocal is smooth near fixed positive `beta`, this difference is `o(N^(-1/2))`. Therefore `c_N/N^(3/2)` tends to infinity. This reasoning permits arbitrary positive `c_N` sequences and arbitrary total-energy tuning; it does not assume the secant calibration or a large bath before establishing necessity.

For three phases, the same derivative conclusion pins the bath inverse temperature uniformly near `beta` throughout the interval between extreme energies. The curvature is therefore `beta^2/c_N[1+o(1)]` uniformly. The concavity gap at the middle phase is bounded below by the product of its two extensive distances times `beta^2/(2c_N)`. The center-value part of Equation (7) forces that gap to zero, proving `c_N/N^2 -> infinity`. Normalization and every linear energy tilt cancel from the gap. There is no loophole from moving the common additive energy zero.

## 3. Sufficiency and what concentration supplies

The proposed total energy exactly balances the residual likelihood at the two chosen endpoints and keeps both endpoints below the bath cutoff. Under either sufficient capacity scaling, the cutoff is also far outside every fixed standardized phase window.

After subtracting the common endpoint value, concavity gives nonnegative residual log weight inside their interval and nonpositive weight outside it. Thus rare exterior canonical tails are never amplified. This sign is important because the subsystem kinetic energy is unbounded above.

For two phases, the pointwise valley envelope is genuinely needed. On the interior tail, the amplification is at most `C N x/c_N`. Its ratios to the Gaussian and stretched-exponential costs are bounded by the two expressions in Equation (13). Both vanish when `c_N >> N^(3/2)` and `alpha>=1/2`. The reweighted interior probability outside fixed standardized phase windows is consequently uniformly negligible after the window size is sent to infinity. The use of `exp[-min(a,b)] <= exp(-a)+exp(-b)` is in the correct direction and permits explicit tail integration.

For three phases, the maximum interior amplification is already `exp[O(N^2/c_N)]=1+o(1)`. No quantitative valley envelope is then necessary. Equation (6), **including the condition that the positive phase weights sum to one**, supplies all the remaining concentration. This is a real concentration assumption, but it is already stated; the manuscript does not incorrectly infer sufficiency from unrelated local peaks carrying less than the full limiting mass.

Each argument establishes `integral p_N |exp(h_N)-1| -> 0` for the endpoint-normalized residual, which implies that its normalizer tends to one and that normalized total variation tends to zero. Thus the claimed existence iff conditions are correct. The secant construction proves existence; the manuscript does not claim to optimize finite nonzero TV errors.

For maximum formal clarity, Theorem 1 could say “assume exactly two energy phases in (6)” in its first sentence. Its present section title, notation, and preceding discussion already make that scope clear, so this is an editorial clarification rather than a mathematical correction.

## 4. Boundary-scale local law

At `c_N/N^(3/2) -> gamma`, set `delta_N=beta Delta_N/c_N`. Secant calibration gives

\[
\beta_{B,-}=\frac{c_N}{\Delta_N}(1-e^{-\delta_N}),
\qquad
\beta_{B,+}=\frac{c_N}{\Delta_N}(e^{\delta_N}-1).
\]

Taylor expansion yields

\[
\sqrt N h_N'(E_{-,N})\to\frac{\beta^2\ell}{2\gamma},
\qquad
\sqrt N h_N'(E_{+,N})\to-\frac{\beta^2\ell}{2\gamma}.
\]

The local quadratic term is of order `N/c_N` and vanishes. Thus the local limiting tilt is linear, with the signs and coefficient in Equation (14).

For `alpha>1/2`, the stretched-exponential valley term dominates the bath gain asymptotically; the Gaussian tail is controlled by choosing a sufficiently large standardized window. The stronger Gaussian envelope in the Potts example also suffices. At `alpha=1/2`, that domination can fail at boundary scale. The manuscript correctly excludes this case from the conclusion based on Equation (9) alone.

Tilting a centered normal density of variance `v_i` by `exp(b_i z)` multiplies its mass by `exp(b_i^2 v_i/2)`, shifts its conditional mean by `b_i v_i`, and retains conditional variance `v_i`. Therefore the normalization, phase probabilities, means, and TV expression in Equation (14) are correct. In particular, equal endpoint likelihoods do not fix integrated phase probabilities when the two variances differ. No missing variance correction was found.

## 5. Independent Potts calculation

For simplex coordinates `(p_1,p_2)` with `p_3=1-p_1-p_2`, write `b=beta J`. At the disordered minimum the Hessian of the rate potential is

\[
H_d=(3-b)\begin{pmatrix}2&1\\1&2\end{pmatrix},
\qquad \det H_d=3(3-b)^2.
\]

At an ordered minimum `(2/3,1/6,1/6)`, it is

\[
H_o=\begin{pmatrix}15/2-2b&6-b\\6-b&12-2b\end{pmatrix},
\qquad\det H_o=3(6-b)(3-b).
\]

Combining the multinomial Stirling factor `(p_1p_2p_3)^(-1/2)` with the inverse square root determinant gives the single-ordered/disordered weight ratio

\[
r=\sqrt{\frac{2(3-b)}{6-b}}.
\]

There are three ordered colors, so the combined low-energy weight is `3r/(1+3r)` and the disordered weight is `1/(1+3r)`, as in Equation (18).

The ordered potential-energy gradient in these coordinates is `(-J/2,0)`. Its Gaussian variance is

\[
\frac{J^2}{4}(H_o^{-1})_{11}
=\frac{J^2}{6(3-b)}.
\]

The disordered tangent gradient is zero, so its potential-energy fluctuations disappear on the `sqrt N` scale. Independent kinetic energy contributes `a/beta^2` to both phase variances. This reproduces every quantity in Equation (18), including the energy-density gap `J/12`.

The global occupation estimate is justified by local nondegenerate minima and compactness. Away from those minima, a positive rate gap absorbs polynomial errors in Stirling's formula, including boundary lattice points. The partition sum is of order `exp(-N I_min)`: each local lattice neighborhood contributes order `N` points with weights of order `N^(-1) exp(-N I_min)`. Thus no normalization power of `N` is missing in Equation (19).

For sufficiently large `N`, `aN>1`. The Gamma density's log curvature on the bounded feasible kinetic-energy-density interval is at most `-c/N`; the curvature becomes more negative near zero. Expansion around its mode, followed by the bounded mode-to-mean shift, proves Equation (20) uniformly even at arbitrarily small positive kinetic energy. Values outside its positive support have zero density.

To obtain Equation (21), partition occupation space by a nearest minimum and retain a fixed fraction of the Gaussian occupation exponent. The remaining occupation and kinetic exponents jointly control `(E-Ne_i)^2/N` by Lipschitz continuity of the potential-energy density. The retained exponent sums over the two-dimensional occupation lattice to `O(N)`, canceling the occupation prefactor. This supplies the claimed energy envelope without losing an extra power of `N`.

Finally, the Gamma local density limit provides continuous smoothing of conditional occupation CLTs. It yields local L1 energy-density limits even in the disordered phase, where the potential-energy limit is a point mass. Fixed positive `a` is essential to this argument and is explicitly assumed. This validates the microscopic theorem's inputs without requiring a discrete occupation local limit theorem.

## 6. Probability formulas and numerical scope

The kinetic integral is proportional to `(total_energy-U)^(A+c) B(A,c+1)`, yielding Equation (22)'s occupation exponent and conditional Beta parameters. The canonical kinetic law is Gamma with shape `A`. No off-by-one bath exponent was found.

Strict concavity of the scalar log likelihood makes its positive superlevel set an interval, so the Beta/Gamma CDF formula in Equation (23) computes TV exactly in exact arithmetic. Physical support may truncate that interval, as the manuscript already states. The global scalar crossing problem is compatible with this truncation.

This review did not recompute the numerical table or the already verified limiting numerical values. The manuscript labels its calibration, finite-size scope, floating-point implementation, and lack of interval-arithmetic certification appropriately. Those calculations support the illustrations; the iff results rest on the proofs rather than on the observed numerical trends.

## Overall assessment

The manuscript has preserved the important qualifications from the earlier notes: explicit interior-tail control for two-phase sufficiency, positive full phase weights, local variances supplied by a fixed kinetic sector, unrestricted tuning in necessity, and surface-versus-canonical bath capacities. The title and abstract should continue to be read with the exact power-law bath model and specified phase hypotheses; they are not universal claims for every thermal reservoir or every first-order transition. No mathematical correction is required on the basis of this audit. Novelty, practical short-range hypotheses, and possible finite-nonzero-error optimization remain outside the verified claims.

## Final bounded audit of the expanded manuscript, 2026-09-07

Re-read the expanded manuscript together with `reservoir-support-classification.md` and the spin-only upgrade in `short-range-potts-route.md`. The generalized support theorem, unequal-spacing two-scale corollary, microscopic spin-only necessity statement, and shared-bath statements are consistent with their independently reviewed hypotheses. No substantive mathematical error was found.

The support theorem correctly assumes a diverging energy scale and a weak probability limit with at least three support points. Its necessity selects good likelihood points from positive-probability intervals and uses the exact logarithmic chord gap; it does not retain the obsolete Gaussian assumptions. Its sufficiency uses the global weight bound and tightness. The two-scale corollary correctly requires a diverging nondegenerate within-phase scale smaller than the phase gap and concentration of the other phase on a smaller-than-gap scale.

The short-range spin variance argument is valid: an independent set has at least `N/5` vertices; for `q>4`, at least one neighbor-color count is zero and another is positive; every conditional color probability is at least `exp(-4 beta_max)/q`. Conditional independence and the pairwise variance identity give the stated uniform extensive variance lower bound. Passing the resulting strong-convexity inequality to the thermodynamic pressure and then restricting to each open stable branch proves positive branch curvatures. C2 continuity extends them to coexistence. This avoids the invalid shortcut of reading a within-phase variance directly from the extensive coexistence mixture variance.

Combined with the previously reviewed one-sided-transform deduction, that positivity makes the spin-only conditional Gaussian limits nondegenerate and justifies the microscopic necessary `N^(3/2)` scale. The manuscript continues to distinguish this necessity corollary from the unproved isolated short-range sufficiency theorem. Its composite short-range iff statement needs only the macroscopic three-point support theorem and does not silently use that missing sufficiency estimate.

One notation issue arose because the manuscript now includes discrete spin energies and no-density theorems: the original introductory TV formula used a Lebesgue density. The root has corrected it to a generic dominating-measure expression and changed the reservoir law to a Radon–Nikodym formula. The later density assumptions are now explicitly confined to the local-density lemma and Theorem 1. With that correction, the expanded manuscript's scope is coherent.

This closes the requested fresh mathematical audit. No additional numerical calculations or research directions were opened.
