# How accurately must kinetic defects be measured before placing mobility?

Research note, 2026-09-07. This extends the blind/adaptive distinction in [robust-mobility-design.md](robust-mobility-design.md) to an observation with finite resolution. The parent proposed the measurement question; the derivation below is independent. Independent mathematical review has verified the uniform order law and both sharp endpoint limits; see [review-finite-precision-mobility.md](review-finite-precision-mobility.md). The targeted [literature audit](finite-precision-mobility-prior-art.md) found no exact match, while identifying established observation-channel and stochastic-design frameworks. The derivation uses the scalar surface functional. The independently verified transfer below extends its optimal-value laws to finite transverse bulk diffusion under fixed bulk data and nonzero mean tracer velocity.

## Decision problem and resolution law

On a circle of length `2π`, let `k_c(s)=(c+cos s)²`, with `c` uniform on `[-2,2]`. For `D≥0`, define

\[
J_c(D)=\sup_{f\in C^\infty_{\rm per}}
\left\{2\int f-\int[D|f'|^2+k_cf^2]\right\}.
\]

The designer observes only the bin containing `c`, then chooses a nonnegative mobility with total mass `M` for that bin. Take the deterministic partition `I_j=[−2+jΔ,−2+(j+1)Δ)`, with the final interval closed at its right endpoint and common width `Δ=4/N`. Equivalent bounds hold for partitions whose cell widths lie between fixed positive multiples of `Δ`. Exact asymptotic constants below use equal widths. Define

\[
\Phi(M,\Delta)=\inf_{\{D_I:\int D_I=M\}}
\sum_I\frac{|I|}{4}\,\mathbb E[J_c(D_I)\mid c\in I].
\tag{1}
\]

The budget is available separately for each manufactured wall. It is not pooled across bins. There is no pointwise mobility cap, prescribed fabrication length, or measurement cost. The observation is noiseless quantization; additive measurement noise is a different model. If partitions are nested, refinement cannot worsen the optimum because it preserves every coarse policy. Bin width alone does not order arbitrary nonnested partitions by information.

The principal theorem is the uniform two-parameter estimate

\[
\boxed{\Phi(M,\Delta)\asymp
M^{-1/5}+M^{-1/4}\Delta^{1/4},\qquad M\to0,\ \Delta\to0.}
\tag{2}
\]

The comparison constants are independent of the relative rate at which `M` and `Δ` vanish. Thus resolution substantially finer than `M^{1/5}` attains the adaptive order. Coarser resolution leaves an additional factor of order `(Δ/M^{1/5})^{1/4}`. A fixed nonzero bin width retains the blind budget exponent `−1/4`; the displayed small-`Δ` coefficient law additionally requires `Δ→0`.

## Local uncertain-zero problem

Let one quadratic defect have curvature `a>0`, with its center `r` uniform in an interval of spatial width `w`. If its allocated budget is `m`, scale

\[
\ell=(m/a)^{1/5},\quad x=\ell y,\quad
D(x)=(m/\ell)d(y),\quad \int d=1.
\]

The whole-line conditional optimum is exactly

\[
a^{-4/5}m^{-1/5}\,F(w/\ell),
\]

where

\[
F(\eta)=\inf_{d\ge0,\int d=1}
\frac1\eta\int_{-\eta/2}^{\eta/2}
\sup_f\left\{2\int f-\int[d|f'|^2+(y-u)^2f^2]\right\}du.
\tag{3}
\]

At `η=0`, use the single known center. The exact placement theorem gives

\[
F(0)=C_*,\qquad C_*=12(3/80)^{1/5}.
\]

The expected compliance functional is convex in the mobility. Reflection symmetrization therefore permits an even design in (3). Translation covariance and local root averaging suggest, and the elementary bounds below establish at the level of orders,

\[
F(\eta)\asymp1+\eta^{1/4}.
\tag{4}
\]

In the cosine model `a=sin²r=1-c²`, while offset uncertainty `Δ` moves the root a spatial distance approximately `w=Δ/√a`. Hence the local transition is

\[
\boxed{\Delta\sim m^{1/5}a^{3/10}.}
\tag{5}
\]

If slope magnitude `v=√a` is used instead of curvature, the last factor is `v^{3/5}`. Confusing slope and curvature changes this exponent.

For `η≫1`, approximately uniform mobility on the possible-root interval, padded by its much smaller diffusion layers, gives

\[
F(\eta)\sim C_0\eta^{1/4},\qquad
C_0=\Gamma(1/4)^2/(2\sqrt2).
\tag{6}
\]

A root-averaged dual test proves the matching lower bound, as described below. For `η→0`, a smooth positive approximation to the known-center optimal design, followed by continuous dependence on the center and a diagonal limit, gives `F(η)→C_*`; the reverse inequality follows by allowing exact knowledge of the center.

## Lower bound valid for arbitrary mobility fields

First, more information cannot worsen the optimum. The already verified adaptive theorem therefore gives

\[
\Phi(M,\Delta)\ge cM^{-1/5}.
\tag{7}
\]

It remains to prove the coarse term for `Δ≥L M^{1/5}`, where `L` is a sufficiently large fixed number. Restrict to bins wholly inside a fixed regular offset interval, for example `[-1/2,1/2]`, and to the middle half of each bin. The root locations then range over arcs of length comparable to `Δ`; their curvatures and the conditional root densities, after multiplication by `Δ`, are bounded above and below.

Use for every retained center `r` a bump

\[
h_r(s)=A\,\psi((s-r)/\ell),\qquad
\ell=(M/\Delta)^{1/4},\quad A=\alpha\ell^{-2},
\]

with fixed nonnegative compact smooth `ψ` and small fixed `α>0`. The two root supports are disjoint. Choose `L` so large that `ℓ/Δ` is small; if desired, a fixed small multiplier in `ℓ` can enforce this at the initial threshold. The averaged source minus potential term has order `αℓ^{-1}−Cα²ℓ^{-1}`. Meanwhile

\[
\sup_s\mathbb E[|h'_r(s)|^2\mid c\in I]
\le C A^2/(\Delta\ell),
\]

because only a center interval of length `O(ℓ)` contributes at each `s`. Its cost against any mobility placement is at most

\[
M\sup_s\mathbb E|h'_r(s)|^2
\le C\alpha^2 M/(\Delta\ell^5)
=C\alpha^2\ell^{-1}.
\]

Choosing `α` small gives `E[J_c(D_I)|I]≥cℓ^{-1}=cM^{-1/4}Δ^{1/4}` for every admissible `D_I`, including rapidly oscillating fields, spikes, and zero regions. The total probability of retained bins is bounded below. This proves the second lower bound. When `Δ<L M^{1/5}`, that term is already bounded by a constant multiple of (7). Taking the larger bound is equivalent, up to a factor two, to their sum in (2).

For the sharp large-`η` coefficient in (6), use the harmonic inverse profile as the bump after smooth truncation. Apart from a negligible edge fraction, the averaged squared derivative is constant over the uncertain-center interval to leading order. This is the constant-curvature specialization of the unrestricted dual certificate in [robust-mobility-design.md](robust-mobility-design.md). It excludes improvement by unresolved mobility microstructure.

## Constructive upper bound, including bins crossing a fold

Write `t=1−|c|`. Put

\[
W=\Delta+M^{2/7}.
\]

Use one shared design for all bins within a fixed multiple of `W` of each fold. Outside these bins, `t` and the curvature remain comparable throughout each bin.

For a regular zero-containing bin, its two possible-root arcs have width at most `Cw`, with `w=Δ/√t`. Pad each arc by

\[
\ell=(M/t)^{1/5}.
\]

Place uniform mobility on the padded arcs, dividing the budget equally. Its size is comparable to `M/(w+ℓ)`. For `t≥CW`, each support lies within a quadratic neighborhood and remains separated from the other root. The harmonic layer has width

\[
r_H\asymp\left[\frac{M}{t(w+\ell)}\right]^{1/4}\le C\ell,
\]

so the padding contains the diffusion layer with a fixed margin. Neumann bracketing and quadratic potential comparison, together with the reciprocal-potential integral outside the support, give the uniform conditional bound

\[
J_c(D_I)\le C\left[
M^{-1/5}t^{-4/5}
+M^{-1/4}\Delta^{1/4}t^{-7/8}\right].
\tag{8}
\]

Both singularities are integrable over `c`. The estimate is uniform for all offsets in the bin. The requirement `t≥CM^{2/7}` is exactly what keeps an adaptive-width patch smaller than the separation of the roots.

For the fold bins, use constant mobility on a single interval of radius `R=K√W` around the fold center, with `K` fixed sufficiently large; it contains every possible zero in those bins with a margin. Put zero mobility elsewhere. Its size is `d\asymp M/√W`. The local coordinate `z=2sin(x/2)` converts the potential exactly to `(z²/2-t)²`, with bounded metric factors.

The previously verified quartic interval bounds, applied with this constant local mobility, show

\[
\int_{|t|\le CW}J_c(D_I)\,dt
\le C d^{-1/4}W^{1/4}+CW^{-1/2}
\le C M^{-1/4}W^{3/8}.
\tag{9}
\]

The first term comes from integrating the quartic response over `t`; the second is the reciprocal-potential contribution outside the mobility support. The last inequality uses `W≥M^{2/7}`. More explicitly the quartic response has amplitude `d^{-1/2}`, parameter scale `d^{1/3}`, and positive-parameter integral growing as `(W/d^{1/3})^{1/4}`. The scaled interval boundary remains farther from the roots by a fixed factor, as required by the uniform interval estimates.

There are only two groups of fold bins, and the same trial mobility is used for every bin in a group; the integrals in (9) therefore directly bound their unconditional contribution. Bins on the no-zero side outside these groups need no special design: `J_c(D)≤∫1/k_c`, whose integral from `|t|=CW` outward is at most `CW^{-1/2}` and is absorbed in (9).

Finally,

\[
M^{-1/4}W^{3/8}
\le C\left[M^{-1/7}+M^{-1/4}\Delta^{3/8}\right]
\le C\left[M^{-1/5}+M^{-1/4}\Delta^{1/4}\right].
\]

Combining this with the integrals of (8) proves the upper half of (2). The fold bins do not change the global resolution exponent.

## Sharp limits away from the crossover

The same local comparison and dual-certificate arguments give the following sharper equivalents. Independent review verified their constants, the uniform conditional lower certificate, and the matching constructions.

If `Δ/M^{1/5}→0`,

\[
\Phi(M,\Delta)\sim K_{\rm adaptive}M^{-1/5},\qquad
K_{\rm adaptive}=\frac{2^{6/5}C_*}{4}B(1/2,1/5).
\tag{10}
\]

On compact regular offset sets, root uncertainty is negligible on the optimal patch scale. Smooth regularizations of the exact adaptive design converge uniformly under the vanishing scaled shifts. The coarse term in (8), after multiplication by `M^{1/5}`, tends to zero and has an integrable `t^{-7/8}` factor; the adaptive term has integrable factor `t^{-4/5}`. The fold bound (9) is lower order. Shrinking a fixed omitted fold neighborhood then yields the same coefficient as exact observation.

If `Δ→0` and `Δ/M^{1/5}→∞`,

\[
\Phi(M,\Delta)\sim K_{\rm coarse}M^{-1/4}\Delta^{1/4},\qquad
K_{\rm coarse}=2^{-3/4}C_0 B(1/2,1/8)=25.7238273888\ldots.
\tag{11}
\]

On compact regular offset sets each bin has nearly constant curvature. Its two root arcs have width `Δ/√a`, and symmetry plus convexity allocates half the budget to each. Formula (6) gives the conditional coefficient `2^{5/4}C₀ a^{-7/8}`. Parameter Riemann sums yield (11). The harmonic layer divided by the root-uncertainty width tends to zero uniformly on each fixed regular offset set, which is the uniformity needed by the dual lower certificate. The bound (8) controls the omitted folds. In the coarse regime `W\simΔ`, and (9) divided by the leading scale is `O(Δ^{1/8})→0`.

At `Δ/M^{1/5}→τ∈(0,∞)`, a natural candidate for the exact crossover is

\[
M^{1/5}\Phi(M,\Delta)\longrightarrow
\frac{2^{6/5}}4\int_{-1}^1(1-c^2)^{-4/5}
F\left(2^{1/5}\tau(1-c^2)^{-3/10}\right)dc.
\tag{12}
\]

This formula is not proved here. It would require a uniform variational localization theorem for the conditional optimization problem, rather than localization for a fixed chosen design. Its integral converges by (4). It has the correct limits (10)–(11), but that consistency is not a proof.

## Transfer to finite transverse bulk diffusion

Let `Φ_bulk(M,Δ)` be the expected flow-dispersion optimum over exactly the same bin-dependent policies and budgets in the full bulk–surface model. Assume a fixed smooth bounded cross-section with a one-dimensional periodic wall, fixed positive bulk diffusivity, fixed bulk velocity `u∈L²`, constant affinity `K>0`, and nonzero mean tracer velocity `V`. Write `Z=A+KP` and `B=KV²/Z>0`. The cosine rate family satisfies the uniform hypotheses `0≤k_c≤9` and `∫k_c≥P/2`.

The independently checked [scalar-to-bulk transfer theorem](scalar-to-bulk-design-transfer.md) gives

\[
\boxed{\Phi_{\rm bulk}(M,\Delta)\sim B\Phi(M,\Delta)}
\]

uniformly in the observation rule, including every varying bin width considered here. More quantitatively, for sufficiently small dimensionless `M`,

\[
1\le\frac{\Phi_{\rm bulk}(M,\Delta)}{B\Phi(M,\Delta)}
\le1+C M^{1/5}\log(1/M),
\]

with `C` independent of `Δ`. Consequently the order theorem (2) and both sharp endpoint equivalents (10)–(11) hold for the full-bulk optimum after multiplication by `B`.

The transfer preserves the information and the budget: mix any near-optimal bin policy with a uniform floor as `D_I^θ=(1−θ)D_I+θM/P`. Quadratic-form ordering gives `J_c(D_I^θ)≤J_c(D_I)/(1−θ)`, while the bulk remainder is at most `C[1+log(P/(θM))]`. Choosing `θ=M` and using the uniform adaptive lower bound `Φ≥cM^{−1/5}` proves the ratio. This argument transfers optimized values; it does not assert a uniform remainder for each original, unmixed design. It also does not establish the unproved intermediate scalar crossover (12). Vanishing bulk diffusivity, zero mean velocity, and fabrication constraints that exclude the mixture require separate treatment.

## Interpretation and novelty boundary

For `N=2^B` equal bins, the observation has `B` binary digits of resolution and `Δ=4·2^{−B}`. The order threshold becomes `B=(1/5)log₂(1/M)+O(1)`. In the sharp coarse regime (11), one additional binary digit multiplies the leading response by `2^{−1/4}≈0.8409`. This is a consequence for the specified deterministic quantizer, not an information-capacity theorem for arbitrary measurements.

The measurement resolves the kinetic offset, rather than directly resolving spatial position. The needed spatial precision depends on the local slope, as in (5). The dominant average contribution comes from ordinary zeros, and their characteristic scale is `Δ\sim M^{1/5}`. Improving precision past this scale cannot improve the budget exponent already available with perfect observation; coarser precision spreads the mobility over a root-uncertainty arc and raises the response.

The result is an idealized information-versus-resource law. It does not price measurement, constrain fabrication, or establish the benefit at a particular finite experimental budget. Its slow fractional powers should be retained when interpreting practical gains. It also does not assert that a uniform patch is the exact finite-resolution optimizer; the patch supplies an upper bound and the root-averaged dual test supplies the matching order.

Conditional and adaptive design under partial information are established decision frameworks, and the source functional is a compliance. The specific scaling law for singular kinetic defects is the candidate contribution. The targeted [literature audit](finite-precision-mobility-prior-art.md) found no exact match for the uniform two-parameter law. [Yüksel and Linder (2012)](https://arxiv.org/pdf/1009.3824) study expected-cost continuity under changes of observation channels, including quantizers. [Saldi, Yüksel and Linder (2015)](https://arxiv.org/pdf/1511.04657) establish asymptotic optimality of quantized models under their assumptions. These works establish the broader decision framework but do not provide this singular PDE budget rate. The broad prior-art boundaries recorded in [optimal-mobility-placement-prior-art.md](optimal-mobility-placement-prior-art.md) and [random-barrier-prior-art.md](random-barrier-prior-art.md) continue to apply.
