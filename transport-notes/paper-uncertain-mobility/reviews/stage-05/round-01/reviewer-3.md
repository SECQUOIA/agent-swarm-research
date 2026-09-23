# Independent review: Stage 05, round 01, reviewer 3

Reviewer: `/root/paper_reviewer_3`. Date: 2026-09-07.

Snapshot: `b10b05d41199399897fdd9cc7cc6eab8d0fe2ae90e96c6ff4fa8d7d2ef68b42c`.

I reviewed the complete `sections/05-exact-observation.tex`, the author handoff, and the relevant accepted form, bracketing, physical-transfer, and predetermined-mean results. I did not read other reviewer reports or coordinator checks, edit manuscript sources, or delegate review work. The checks below are independent analytical checks, not reliance on the author's sampled potential tests.

## Local profile, global certificate, and uniqueness

I independently expanded the profile polynomial as `p(y)=y-3y^3+2y^4`. Its integral is 3/20, and `p'(y)+y^2(9-8y)=1`. With the prescribed R these give mass m and the weak source equation. The flux is zero at the center and both support boundaries, so the finite slope jumps do not create distributional sources. The interior source integral is `10/(aR)`, the exterior integral is `2/(aR)`, and their sum agrees with the derivative and reaction energies displayed in the manuscript.

For an arbitrary integrable competitor, the Lipschitz source representative is a valid limiting test: its far cutoff changes the derivative by only O(L^(-3)), while mollification does not increase the Lipschitz constant. Bounded derivatives converging almost everywhere allow dominated convergence against an arbitrary L1 mobility, even one concentrated near the corners. The global slope certificate therefore excludes all such competitors; it does not assume their smoothness or a minimum spatial scale.

Equality forces all mass into the saturated-slope interval. The first variation is legitimate for the approximated source plus any compact smooth perturbation. Its flux has a locally absolutely continuous representative, because its distributional derivative is locally integrable. Zero exterior flux and the nonzero constant source slopes on each open half-support uniquely recover D there. This proves the asserted almost-everywhere uniqueness without imposing an additional transmission condition at the center. Differentiating `12/(aR)` using `m=3aR^5/80` gives `-64/(a^2R^6)`, matching the negative squared optimal slope.

## Arbitrary local masses on a compact wall

The cutoff in the lower certificate acts only on the fixed-distance reciprocal tail once M is small. Its source/reaction alteration is uniformly bounded over all local masses between zero and M; the cutoff's bounded slopes are eventually smaller than the diverging central certificate slope. Mollification preserves that bound. Thus the lower estimate depends on each competitor's actual local mass, with a constant independent of whether that mass is much smaller than M.

If a neighborhood has zero mobility mass, the auxiliary-budget source test has no derivative penalty there and its source-minus-reaction value diverges as that auxiliary budget tends to zero. The stated infinite lower bound is therefore valid. For positive masses, minimizing a sum of terms `w_j b_j^(-1/5)` under total mass at most M gives masses proportional to `w_j^(5/6)`. Substitution of `w_j=Cpl a_j^(-4/5)` yields the curvature power -2/3 and the total power 6/5.

The upper support estimate uses a zero-flux square completion, so it remains valid for restrictions of arbitrary wall tests with unrestricted endpoint traces. On each support the source integral is `10/(a_- R)`; the reciprocal tail contributes at most `2/(a_- R)` plus a fixed error. Together these recover the whole-line constant. The fixed-eta lower and upper errors do not justify an additive bounded error at exact curvature, and the manuscript explicitly avoids that claim.

## Physical domain and finite-bulk correction

For the explicit localized field, the proposed closability check covers the whole wall: on each compact subset where D is positive the weighted derivative limit must vanish, and on the zero-D set it vanishes identically. Only finitely many interface points remain. The quadratic outer zeros have vanishing transition energy of order the transition width; the central linear zero admits logarithmic transitions with vanishing energy. Thus the minimal closure permits the independent half-support and exterior domains used in the comparison proof.

For each fixed M, reaction controls the domain away from centers. Near a center, anchoring in a strictly positive interior interval and integrating `1/D` gives at most logarithmic growth of pointwise test values; that logarithm is integrable. This supplies the asserted fixed-M L2 coercivity and inverse. Testing the difference from the lower-potential source with its positive part proves `0<=h<=h_-` on each support. Outside, the zero derivative coefficient gives `h=1/k` almost everywhere.

The maximum of `y^2(9-8y)` occurs at y=3/4 and is 27/16. Therefore kh is bounded uniformly for fixed eta, and kh-1 is supported on total length of order `M^(1/5)`. Its L2 norm is of order at most `M^(1/10)`. Load convergence and the nonnegative Schur penalty give the bulk limsup; fixed smooth bulk trials with penalty at most `M||partial_s f_trace||_infinity^2` give the liminf by density. This justifies the fixed-profile remainder limit without extending it into a coalescing-defect regime.

## Explicit observed-offset policy and moving comparison region

In the separated regime, `a=t(2-t)>=t`, so `z=M/a^(7/2)<=L^(-7/2)`. The support-to-comparison radius ratio is indeed

`R/delta = 2(40/3)^(1/5) z^(1/10)(1-eta)^(-1/5)`.

A fixed sufficiently large L therefore enforces both eta at most 1/2 and R at most delta/2 uniformly in the entire separated regime. The root neighborhoods are disjoint at this scale.

Taylor's inequality is strong enough for the chosen reduced curvature: for `|x|<=delta=eta sqrt(a)/2`,

`|cos(r+x)-cos r|^2 >= a x^2 (1-eta/4)^2 >= a(1-eta)x^2`.

Thus the support comparison is valid; its curvature loss does not shrink faster than the spatial comparison error. The uniform reciprocal tail is obtained from inverse-square singularities near each root plus an O(a^(-3/2)) fold complement. The latter is absorbed by `1/(aR)` when R is at most a fixed multiple of sqrt(a). At a fixed interior offset, the sharper truncated tail gives `2/(bR)` per root and the remaining `O_c(delta^(-1))` term is lower order because delta is proportional to `M^(1/10)`. Combined with the two interior values this gives `2^(6/5)Cpl a^(-4/5)M^(-1/5)`.

The fold patch has exactly mass M, contains all roots with a fixed scaled margin, and its rescaled potential has uniformly positive integral on the fixed interval. Together with the positive derivative coefficient this gives uniform free-endpoint coercivity. Outside the patch the reciprocal potential costs O(r^(-3)). The rootless branch is also bounded by its reciprocal potential. These establish a valid global scalar policy, subject only to the minor terminology correction about operator versus integrated-energy scale recorded below.

Translations and dilations of the compact profiles are continuous in L1 within the separated branch. The regime sets, fold choices, and uniform branch are Borel. Assigning a prescription at every threshold and fold point yields exact mass for every observation, including null exceptional offsets. No minimizing selection is being assumed.

## Averaging and sharp constants

The normalized response in the fold core is `M^(-8/35)`, bounded by a fixed multiple of `|t|^(-4/5)` when `|t|<=L M^(2/7)`. On the outer rootless branch, the required inequality reduces to `M^(1/5)|t|^(-7/10)<=C`, which follows from its threshold. The resulting envelope is integrable near both folds and is independent of M. Dominated convergence therefore gives the sharp upper mean; rootless fixed offsets contribute zero to the normalized limit.

For the lower bound, a sequence of globally near-optimal Borel policies exists by the finite infimum definition. The compact-wall theorem bounds every coefficient at each fixed interior offset. Fatou then supplies the lower mean without needing measurability of a pointwise infimum over designs. The beta integral, density 1/4, and paired-root factor give the stated Kobs. Dividing by the accepted predetermined mean gives exponent 1/20 and the stated ratio of constants. The fold window contributes only `M^(2/7)M^(-3/7)=M^(-1/7)`, consistent with its being necessary for the global policy but lower order in the mean.

## Finding

### R3-01 — Minor: distinguish the operator scale from the integrated energy scale

Location: `sections/05-exact-observation.tex:405–420`, especially lines 411–412.

The sentence says the “derivative energy has the same scale r^4.” Under `s-s0=rx` and an unscaled test `v(s)=v_tilde(x)`, the derivative **operator** and killing coefficient have common scale r^4, but the two terms of the integrated quadratic energy have common scale r^5 because `ds=r dx`. Specifically, `D=r^6/(2B)` gives `integral D|v'|^2 ds = r^5/(2B) integral |v_tilde'|^2 dx`. The subsequent response factor `r/r^4=r^(-3)` is correct, so this is terminology rather than a wrong bound.

Remedy: replace “derivative energy” by the rescaled differential-operator term, or explicitly state that the operator factors by r^4 and the integrated energy by r^5. Keep the correct response factor. This small correction makes the scaling explanation unambiguous to readers following the variational normalization.

## Verdict

No major issue found. Correct the minor operator/energy wording before stage acceptance. The unrestricted placement theorem, physical realization of the explicit trials, measurable oracle policy, and sharp averaging argument withstand the checks above. This review does not certify the subsequent finite-precision problem or literature priority beyond the distinctions stated in this section.
