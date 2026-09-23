# Independent review: Stage 06, round 01, reviewer 1

Reviewer: `/root/paper_reviewer_1`. Date: 2026-09-07.

Snapshot: `fd49a0c7de991734f21f20428b8a74ba19e44a0ffa3204ed80a925056ab5fb2f`. All sixteen manifest hashes matched. I read the full new section, its handoff and relevant notation/claims, together with the accepted smooth-test, measure-relaxation, localization, placement, and policy-transfer dependencies. I did not read other reports or coordinator-checks, coordinate conclusions, delegate, or change manuscript sources.

## Verdict

**No major issue found. One minor incorrect cross-reference requires correction.** The intermediate crossover is justified by a genuine conditional variational localization theorem and global integrable bounds. The local value has a valid attainment and continuity proof, including possibly singular or non-tight weak limits. The simultaneous coarse limit is proved independently rather than inferred by taking the large-argument limit in a fixed-ratio theorem.

## Independent analytic checks

### 1. Definition and exact local scaling

The finite number of bin choices justifies decomposition of the global value into conditional infima. An arbitrarily close coefficient can be chosen separately in each bin, and the finite sum of its errors can be made arbitrarily small. Thus there is no measurable-selection or expectation–infimum issue at this step.

For potential `a(x-z)^2`, the length `(m/a)^(1/5)` and coefficient transformation `D=a ell^4 d` give mass `a ell^5=m`. With source amplitude `(a ell^2)^(-1)`, source, derivative, and reaction terms share factor `(a ell)^(-1)=a^(-4/5)m^(-1/5)`. The center width is divided by ell. This verifies the local scaling formula, including its curvature exponent and the convention that eta is the full width of a uniformly distributed center interval.

### 2. Quadratic weighted-form completion and expanding endpoints

I checked the quadratic version of the graded-background lemma separately from its quartic predecessor. On a fixed core, the positive mobility floor and an interval avoiding every possible center control the constant mode and local H1 norm. Outside it, the potential controls `int x^2 f^2`. Weighted Cauchy–Schwarz gives a source-tail bound proportional to `L^(-1/2)`, not the quartic `L^(-3/2)`. The manuscript uses the correct slower exponent.

Bounded-energy maximizing sequences therefore have local H1 weak limits and weak weighted derivatives. On compact sets the floor lets distributional differentiation identify the weighted derivative limit with the derivative of the limiting function. Lower semicontinuity controls energy, while the source-tail estimate promotes local source convergence to whole-interval source convergence. This applies to unequal growing endpoints as stated.

Membership in the actual smooth-test completion is not simply assumed. The local one-dimensional Sobolev inequality gives the squared pointwise bound by the sum of `|x|^(-2)` and `|x|^(alpha/2-1)` times the energy. Because alpha<2, this bounds the limiting function at infinity. The derivative cost introduced by a distant cutoff is at most `C R^(-2)||f||_infinity^2 int_annulus d`, which vanishes. The existing derivative and reaction tails vanish separately. On the resulting compact support, approximation of derivatives in L2 of the finite measure `d dx`, followed by an integral correction and integration, gives smooth approximation. The local floor makes that approximation uniform in the functions and hence also controls source and reaction terms. Unbounded d is allowed in this argument.

For continuity in z, the anchored energy controls `int(1+x^2) f^2` uniformly on compact center sets. The difference of the shifted quadratic potentials is bounded by `C|z-z'|(1+x^2)`. Nearby forms consequently bound each other with multiplicative factors approaching one. This proves continuity of the fixed-profile response and supplies the compact-center uniformity used later. A scalar derivative normalization tending to one obeys the same comparison.

### 3. Local value: bounds, relaxation, attainment, and continuity

The lower bound Cpl follows from the exact known-center theorem for each translated root. The independent moving-test bound is also correct for all eta>0: amplitude `eta^(1/2)` and width `eta^(-1/4)` give source and reaction scale `eta^(1/4)`. At a fixed spatial point the center-averaged squared derivative is bounded by `eta^(1/4) T_psi`. Its integral against any unit-mass coefficient is therefore bounded independently of spikes and zero sets. Taking the oscillator variational supremum yields `C0 eta^(1/4)`.

The padded constant-density upper trial has exactly mass one. Both endpoints stay at least one physical unit from every possible center. For large eta the harmonic length is of order `eta^(-1/4)`, so both endpoint distances in harmonic coordinates tend to infinity uniformly, including for centers at the extremes of their interval. The free-endpoint harmonic limit and the bounded reciprocal exterior give `C0 eta^(1/4)[1+o(1)]`. For bounded eta the same construction gives a uniform finite upper value.

The previously proved derivative-flattening construction applies to the shifted quadratic reaction because source and reaction remain continuous under uniform convergence on the common compact support of each approximating test. Thus singular mobility mass is indeed ineffective under this smooth-test definition. For each compact smooth test, simultaneous vague convergence of mobility measures and convergence of the center preserve its value. The supremum is jointly lower semicontinuous and can be taken over a common countable collection of tests; it is measurable.

The attainment proof correctly handles mass loss differently from the fixed-fold integrated problem. A vague limit of a minimizing sequence has mass at most one. Fatou gives cost at most the liminf on the fixed center parameter interval. After singular mass is removed, any missing mass can be filled with a nonnegative density. Monotonicity in mobility guarantees that this completion cannot increase cost. The resulting unit-mass density therefore attains the infimum. Tightness, strict mass monotonicity, and a prescribed scaling law at fixed eta are not required.

For eta_n tending to eta, the same simultaneous compact-test lower semicontinuity and mass completion give lower semicontinuity of the value. For the reverse inequality, the positive-tail regularization `(d+epsilon rho)/(1+epsilon)` has a response at most `(1+epsilon)` times the old one. Its response is finite and continuous on compact center sets by the preceding lemma, so its average is continuous in eta. It is a valid fixed competitor for nearby eta_n. Letting epsilon decrease to zero proves upper semicontinuity, including at eta=0. Reflection averaging gives an even minimizer without any asserted uniqueness or monotonicity of the width dependence.

### 4. Conditional arbitrary-design liminf

Reflection preserves each individual cosine rate, so symmetrization is valid for an arbitrary bin; symmetry of the bin in c is unnecessary. The two half-circles have equal mass M/2 after this averaging. For the first half, the scale `ell_I=((M/2)/a_I)^(1/5)` makes its normalized mobility measure have mass one. Vague subsequences are available even when the original coefficients oscillate or concentrate.

For `c=c_I+Delta v`, Taylor expansion about its midpoint root gives `(c+cos(r_I+ell_I x))/(sqrt(a_I)ell_I)=eta_I v-x+O_K(ell_I x^2)`, uniformly on compact x and v sets. A compact test and its reflected copy therefore have equal limiting source, derivative, and reaction contributions. The factor two in the normalized lower response is exactly the paired-half factor; no mobility allocation is assumed beyond the legitimate reflection reduction.

For each v, taking the supremum after the fixed-test lower limit gives the whole-line response of the limiting measure. Fatou then integrates over v. Removing singular mass and completing any missing density gives a lower value at least Fctr of the limiting eta. Continuity of Fctr converts this sequential statement into the stated uniform lower convergence on a compact regular offset set. This treats escaped mass and all competing integrable coefficients explicitly.

### 5. Uniform conditional recovery

The exact coordinate has derivative `dx/ds=sin(s)/(sqrt(a_I)ell_I)` and metric `w_I=sqrt(a_I)/sin(s)`. On a fixed regular-root neighborhood, this metric is uniformly bounded and tends locally to one in the rescaled coordinate. With `D=a_I ell_I^4 w_I d`, the metric factors in the derivative energy cancel exactly. Source and reaction carry one factor w_I, whereas mass carries `w_I^2`. This confirms both the canonical limiting form and the mass correction `m[1+o(1)]`.

A regularized local profile has an integrable positive tail. The quadratic free-endpoint lemma controls both growing sides of its neighborhood and all bin centers in a compact scaled range. Outside the two neighborhoods the rate has a uniform positive lower bound for all c in the bin, so the unscaled exterior response is bounded and disappears under the local response normalization. Multiplying the mobility by the total-mass correction changes responses only by a factor tending to one, through comparison of the complete quadratic forms.

The finite-profile cover is justified: continuity of each regularized profile's averaged response and continuity of Fctr provide neighborhoods in eta with a common arbitrarily small excess cost. A finite cover of the compact eta range then supplies finitely many profiles. Choosing the first qualifying profile for each bin gives deterministic choices and uniform errors. No continuously selected family of true minimizers is needed.

### 6. Global bin envelopes and the order law

For regular bins, possible-root span is of order `w=Delta/sqrt(t)` and the padding scale is `ell=(M/t)^(1/5)`. Uniform patches have mobility comparable to `M/(w+ell)`. Their harmonic length is at most a fixed multiple of ell, since `M/t=ell^5`. The condition `t>=C(Delta+M^(2/7))` keeps both patches disjoint and inside uniform quadratic neighborhoods. The reciprocal exterior term `1/(t ell)` is bounded by the harmonic response scale, and its further fold-scale term `t^(-3/2)` is also absorbed. Expanding `(w+ell)^(1/4)` produces exactly the two curvature exponents 4/5 and 7/8 in the regular-bin envelope.

For fold groups, a patch radius of order sqrt(W), `W=Delta+M^(2/7)`, covers all roots with a fixed relative margin. Its constant mobility is of order `e=M/sqrt(W)`. The condition W>=M^(2/7) implies `e^(1/3)<=C W`, so the local integrated response is bounded by its quartic core term `e^(-1/6)` plus root-side integral `e^(-1/4) int t^(-3/4) dt`. Both are bounded by `e^(-1/4)W^(1/4)=M^(-1/4)W^(3/8)`. Finite endpoint effects are controlled by the fixed margin and the same interval bracketing, rather than an invalid all-parameter whole-line equivalent. Exterior and remaining rootless costs are of order W inverse-square-root and are absorbed because `M^(1/4)W^(-7/8)<=1`. Grouping bins by whether they meet a fold neighborhood enlarges the total parameter region by at most one bin width, so alignment changes only constants.

The oracle lower bound supplies `M^(-1/5)`. The coarse lower bound on fixed regular offset bins uses width `b=(M/Delta)^(1/4)` and amplitude `gamma b^(-2)`. Its mean source-minus-reaction is of order `(gamma-C gamma^2)/b`; averaging the squared derivative kernel gives cost at most `C gamma^2 M/(Delta b^5)=C gamma^2/b`. A small fixed gamma gives the other lower order for arbitrary designs. When the coarse scale is smaller, it is already covered by the oracle lower bound.

Both regular curvature powers are integrable. The fold contribution is bounded by `C[M^(-1/7)+M^(-1/4)Delta^(3/8)]`, which is little-o of the sum of the two main scales along every joint limit. This proves the joint order without a relation between M and Delta. The separate fixed-N statement also follows from a positive-length regular portion of a bin and the predetermined upper design.

### 7. Exact crossover and separate sharp coarse limit

On compact regular offsets, the conditional normalization is `2 a_I^(-4/5)(M/2)^(-1/5)`, giving factor `2^(6/5)/4` after multiplying by the bin probability. The local uncertainty argument is `2^(1/5) tau a_I^(-3/10)`. Uniform conditional convergence therefore gives the displayed Riemann-sum density.

For bounded tau, the omitted regular regions are dominated by `C t^(-4/5)+C tau^(1/4)t^(-7/8)`, integrable at a fold. The normalized fold contributions vanish with powers 2/35 and 1/40, as stated. Artificial edges of the retained offset interval affect only bins of total vanishing width and are covered by the same envelope. This proves matching global liminf and limsup, including tau=0. The upper bound on Fctr gives the same integrable domination for H itself and hence its continuity.

In the separate coarse limit, the harmonic length/root-arc length ratio tends to zero. A paired moving-root certificate uses conditional density `(1+o(1))/w`, with edge truncation decreasing its nonnegative derivative kernel. Multiplying its pointwise derivative bound by arbitrary mass `M=2ew` gives exactly the paired reference derivative cost. Thus the sharp conditional lower constant does not presume an allocation by the competitor. Uniformly padded root arcs with `b<<p<<w` give the matching upper constant and make their exterior reciprocal response smaller by factor b/p. The conditional coefficient is `2^(5/4) C0 a_I^(-7/8)`.

After integration with density 1/4 this becomes `2^(-3/4) C0 B(1/2,1/8)`. The fold contribution normalized by the coarse scale is O(`Delta^(1/8)`), and the omitted oracle term has coefficient `(M^(1/5)/Delta)^(1/4)` tending to zero. Consequently the proof is uniform in the simultaneous coarse limit; it is not merely a consistency check of H at infinity.

I independently evaluated the coarse coefficient as `25.7238273887632910360585246214` and checked the powers 2/35, 1/40, and the factor `2^(-3/4)` algebraically. The asymptote of H follows separately by dominated convergence using the local large-width limit, and agrees with this constant.

The physical comparison applies uniformly over these observation laws by the accepted theorem. The bits interpretation retains the factor four in Delta as an O(1) shift in B. The distinction between nested and arbitrary nonnested partitions is correct, as is the restriction to noiseless quantization and per-observation budgets.

## Minor finding

### R1-01 — Incorrect reference for the exact sine coordinate

- **Severity:** minor cross-reference error.
- **Location:** `sections/06-finite-precision.tex`, lines 448–449, the sentence beginning “In the exact sine coordinate of ...”.
- **Issue:** `eq:fold-scaling` in Section 02 displays the whole-line scaling length and parameter for `(b x^2-t)^2`; it does not define the sine coordinate. The sine coordinate occurs in the proof of `lem:cosine-uniform`. A reader following the current reference will not find the transformation being invoked.
- **Remedy:** Write the coordinate explicitly, for example `z=2 sin((s-s_j)/2)`, and refer to `lem:cosine-uniform` for its metric and localization argument, or give the sine-coordinate display a dedicated label and cite that label. The subsequent local potential and estimates are correct.

## Disposition

No new external theorem beyond the accepted dependencies is needed for the arguments checked here. No scientific numerical experiment is used to justify the new limit, and this review did not alter frozen build outputs. The local value and crossover coefficient are legitimate attained variational characterizations; an elementary formula or uniqueness proof is not required for the theorem actually stated.

**Accept after the separate fixer corrects R1-01 and the coordinator verifies it. No major issue found.**
