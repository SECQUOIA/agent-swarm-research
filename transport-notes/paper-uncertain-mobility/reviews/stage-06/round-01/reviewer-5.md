# Independent review: Stage 06, round 01, reviewer 5

Reviewer: `paper_reviewer_5`. Date: 2026-09-07.

**Verdict: no major issue found; correct one minor cross-reference.** The new finite-ratio crossover is proved through conditional variational localization and global domination. It is not inferred merely from agreement of endpoint formulas. I found its mathematical content, including the local existence and continuity arguments, justified under the stated assumptions.

## Snapshot and independence

I verified every file hash in snapshot `fd49a0c7de991734f21f20428b8a74ba19e44a0ffa3204ed80a925056ab5fb2f`. I read the entire new section, handoff, and the accepted measure-relaxation, natural-endpoint, exact-placement, and physical-transfer prerequisites. I did not consult other reviewer reports or coordinator checks and did not delegate or edit manuscript source.

## Independent derivations and proof checks

### Local uncertain-center problem

The scaling `ell=(m/a)^(1/5)` gives mobility mass `a ell^5=m` and response factor `(a ell)^(−1)=a^(−4/5)m^(−1/5)`. Its normalized uncertainty is exactly `w/ell`.

For the universal large-width lower certificate, the trial amplitude is `eta^(1/2)` and width `eta^(−1/4)`. Source and quadratic reaction both scale as `eta^(1/4)`. Averaging the squared derivative over a center interval of width eta gives at most `eta^(1/4)T_psi` at each spatial point. This bound can be integrated against any unit-mass mobility, proving the exact lower bound `C0 eta^(1/4)` without requiring smoothness or exclusion of concentrated designs. The known-center lower bound is independently supplied by the accepted quadratic placement theorem.

The padded constant-mobility upper trial has mass one. Its minimum root-to-endpoint distance is one, which is arbitrarily large in harmonic units as eta grows. An interior Dirichlet bracket and a Neumann bracket with reciprocal-potential tails therefore give the uniform harmonic coefficient; the exterior cost remains bounded. This proves the local large-width equivalent.

The quadratic source-tail bound is correctly weakened from the previous quartic case to `L^(−1/2)`. For the natural-endpoint limit, local energy controls the H¹ norm, while the potential controls the source outside the core. Locally weak weighted derivatives are identified with the distributional derivative using the positive compact lower bound on d. The pointwise Sobolev bound gives a bounded limiting representative because `alpha<2`. Its cutoff derivative cost is bounded by `R^(−2)||f||_infty²∫_(R<|x|<2R)d`, and the original energy tails vanish. Smooth derivative approximation on compact intervals is valid even for unbounded integrable d. These steps establish membership in the minimal energy completion, which is needed for the Neumann upper limit.

For attainment of the local value, vague compactness, joint compact-test lower semicontinuity, and Fatou give a finite-cost measure limit. Singular mass can be removed by the accepted derivative-flattening proof because the quadratic reaction is bounded on each fixed test support. Any missing density mass can then be added without increasing the response. The resulting unit-mass density has value at most the infimum and hence attains it; unlike the earlier supercritical argument, this proof does not require strict mass scaling or tightness of the original minimizing sequence. The same construction gives lower semicontinuity in eta. Positive-tail regularization gives the upper semicontinuity: form ordering yields the factor `1+epsilon`, and the fixed regularized response is continuous uniformly on compact center sets. These arguments include eta=0.

### Conditional localization and its uniformity

Reflection preserves each individual cosine rate. Thus it can symmetrize every conditional competitor without assuming that the bin is symmetric in c. The resulting two half-circle masses are exactly M/2. Rescaling one half around its midpoint root gives probability measures of mass one before taking vague limits. The local potential expansion is uniform for bounded center parameter and compact rescaled position. Reflected compact tests supply the factor of two in the response lower bound. Fatou, singular-mass removal, and completion of missing mass then give the local value as a lower bound for every competing sequence, including one with escaping or concentrated mass.

I independently checked the exact recovery coordinate. Its derivative is `sin(s)/(sqrt(a_I)ell_I)`, so `ds=ell_I w_I dx`. The mobility `a_I ell_I^4 w_I d` cancels the derivative metric in the rescaled energy; the source and potential retain precisely one factor w_I. Its mass is `(M/2)∫w_I²d`, converging to M/2 because the metric is uniformly bounded and tends locally to one. One scalar normalization restores the exact total budget. The gapped exterior is uniformly bounded on each retained compact offset set. The natural-endpoint lemma, with its compact-center uniformity, justifies conditional averaging of recovery responses.

Continuity of the local value and of each regularized trial permits finitely many profiles to cover the compact range of normalized uncertainties. This turns the sequential recovery into a uniform bin policy. There are only finitely many bins for each problem, so no unproved measurable-selection assertion is needed. The finite conditional-infimum decomposition is also valid without existence of a circle optimizer.

### Global estimates and limit exchanges

In regular bins, possible-root span has order `w=Delta/sqrt(t)` and padding has order `ell=(M/t)^(1/5)`. The condition `t≥C(Delta+M^(2/7))` makes both small relative to root separation. The padded constant coefficient has harmonic length no greater than a constant times ell. The reciprocal-potential complement is bounded by `1/(t ell)+t^(−3/2)`, which is absorbed by the harmonic scale. Expanding `(w+ell)^(1/4)` gives exactly the two exponents `t^(−4/5)` and `t^(−7/8)`.

For fold groups, radius of order `sqrt(W)` and mobility of order `M/sqrt(W)` give integrated local cost `e^(−1/4)W^(1/4)=M^(−1/4)W^(3/8)`. The quartic core and negative unfolding tail contribute `e^(−1/6)`, which is smaller because `W≥c e^(1/3)`. The finite patch endpoints remain outside all possible roots with a fixed relative margin. The local bracketing arguments therefore provide the needed order bounds even when the rescaled interval does not tend to the whole line in a compact parameter regime. No prohibited large-parameter finite-interval equivalent is used. The exterior and remaining rootless cost `W^(−1/2)` is absorbed because `M^(1/4)W^(−7/8)≤1`. A bin crossing a fold enlarges its parameter group by at most Delta≤W, so grid alignment does not alter the estimate.

The unrestricted coarse lower bound uses actual-root tests and a spatial derivative-kernel supremum, rather than assuming a competitor's allocation. Its width `(M/Delta)^(1/4)` makes the derivative cost have the same order as the source and reaction after averaging. Together with the oracle lower bound, this proves the joint order law at every relative rate. The extra fold terms are smaller by factors bounded by `M^(2/35)` and `Delta^(1/8)` relative to the two main scales.

For finite `tau=lim Delta/M^(1/5)`, uniform conditional localization gives Riemann sums on a compact regular offset interval. The omitted normalized envelope is bounded by an integrable combination of `t^(−4/5)` and `t^(−7/8)`. Its integral near a fold tends to zero as the retained interval expands. Independently, normalized fold costs vanish as `M^(2/35)` and at most `M^(1/40)` when the ratio is bounded. This justifies taking the small-budget limit first and then removing the offset cutoff. The crossover argument `2^(1/5)tau a^(−3/10)` and prefactor `2^(6/5)/4` include both roots, the half budgets, and density 1/4.

The simultaneous coarse limit is proved separately. Conditional root density is `(1+o(1))/w`; the two derivative kernels have disjoint spatial neighborhoods. Their uniform maximum times arbitrary mass M gives exactly the harmonic derivative cost `2z_0T_psi`. For recovery, padding `sqrt(bw)` satisfies `b≪padding≪w`, so endpoint and exterior errors vanish relative to the main coefficient. This yields conditional factor `2^(5/4)C0 a^(−7/8)`. The same omitted-bin bounds extend it to the ensemble. I independently recovered the power of two `−3/4`, curvature exponent `−7/8`, and coefficient `K_coarse=25.72382738876329103605852...`. The large-tau asymptote of the crossover integral then follows separately by dominated convergence and is correctly presented as a consistency statement.

## Finding

### R5-01 — Minor: incorrect reference for the exact sine coordinate

**Location:** `sections/06-finite-precision.tex`, lines 448–450, “In the exact sine coordinate of `eq:fold-scaling`”.

**Reason:** `eq:fold-scaling` in Section 02 defines the generic quartic scaling length and unfolding parameter; it does not define the exact sine coordinate. The coordinate used here is correct and appears in the proof of the uniform cosine localization lemma, but the present reference sends the reader to a different change of variables.

**Remedy:** Write the coordinate explicitly, for example `z=2 sin((s−s_j)/2)`, or refer to the proof of `lem:cosine-uniform` with an appropriate precise coordinate label. Preserve the subsequent bounded-metric argument.

## Physical interpretation, completeness, and build

The section distinguishes a local uncertain-center value from the global ensemble crossover, and it proves the necessary connection. The physical conclusion invokes the accepted observation-uniform transfer at the same per-bin budget. The fixed-N statement is kept separate from the small-bin sharp coefficient. Binary-digit interpretation refers to the specified noiseless quantizer; no noisy-channel, information-cost, fabrication-cap, monotone-width local-value, or unique-profile claim is made. The unresolved elementary form of a minimizing profile does not undermine the attained variational characterization or exact crossover theorem. Broad novelty comparison remains for the manuscript's literature stage.

A fresh isolated build used `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=<temporary directory> main.tex`. It exited with status 0, produced 45 pages, and left no warning, overfull-box, or underfull-box notice in the final log. Independent symbolic simplifications verified the normalized fold exponents `2/35` and `1/40` and the curvature and prefactor exponents quoted above.
