# Second independent audit: marginal-floor multilinear gap

Date: 2026-09-04. Reviewer: `fbbt`, independently of the first reviewer. Target: [the marginal-floor theorem](../results/positive-multilinear-marginal-floor-gap.md).

**Verdict: the finite bound and sharp asymptotic pass mathematical review.** The clipping argument, exact marginal completion, simultaneous global coupling, normalized integral estimate, asymptotic constants, dyadic interpolation, and nonnegative-box extension are valid as written. No correction to the proof is required. This is a correctness review, not a novelty determination.

The nonvacuous parameter range is `0<delta<1`; the asymptotic and displayed finite bound concern `delta<=1/2`. At `delta=1` every coordinate is fixed at one and no positive hull-gap ratio remains, so that endpoint may simply be excluded from the supremum definition.

## Envelope representation and easy terms

A multiaffine function on a cube equals the expectation of its vertex values under independent Bernoulli rounding at each point. Consequently the graph's convex hull equals the convex hull of its binary vertices, and envelopes can be expressed through vertex distributions with fixed means. For positive monomials, a common threshold law simultaneously attains each upper value `min_i x_i`.

Choose a least-mean anchor for each term and write its mean as `u`. The lower single-monomial envelope is `max(0,u-S)`, where `S` is the sum of other failure means. Thus the individual gap is exactly `T=min(u,S)`. The pointwise deficiency `X_anchor-product_e X_i` is nonnegative. Its expectation is the term's upper value minus its expectation. Summing with positive coefficients gives the full hull-gap variational formula used in the proof.

For an all-high term, `u>1/2`, and independence gives at least `u(1-exp(-S))`. The inequality `1-exp(-S)>=(1-exp(-1)) min(1,S)` follows from concavity on `[0,1]` and monotonicity above one. Also `u min(1,S)>=min(u,S)/2`: if `S<=1`, use `u>=1/2` and `min(u,S)<=S`; otherwise use `min(u,S)<=u`. This verifies the constant `kappa=2/(1-exp(-1))`.

For a term with at least two low means, a nonanchor success probability is at most `1/2`, so independence gives deficiency at least `u/2>=T/2>=T/kappa`. The classification includes ties at `1/2` consistently. Fixed-one variables and zero-gap terms cause no problem. Affine terms can be removed before this reasoning.

## One global law with exact marginals

The density `h(t)=1/[L(t+tau)]` integrates to one by the definition of `L`. For each high-variable failure mean `p<1/2`, clipping gives `0<=q_p<=1` and

`0<=m_p=integral q_p<=integral p h=p<1/2`.

Hence the completion factor `(p-m_p)/(1-m_p)` is well-defined and belongs to `[0,1]`. The completed conditional probability lies in `[q_p,1]`, and its integral is exactly

`m_p+[(p-m_p)/(1-m_p)](1-m_p)=p`.

At `p=0`, both the clipped probability and correction are zero. Low variables share the threshold uniform `U`; conditional high-variable failures can be realized using mutually independent additional uniform variables. This explicitly produces a single finite-dimensional joint distribution with all prescribed means. It is not a set of incompatible term-specific constructions. Neither its density nor the completion depends on the monomial list or objective coefficients.

The conditional union bound has two exhaustive cases. If any `p h(t)>=1`, its clipped and completed failure probabilities equal one, so the union probability is one. Otherwise all probabilities are unclipped before completion, and conditional independence gives

`product(1-q'_p)<=exp(-sum q'_p)<=exp(-h(t) sum p)`.

Thus the claimed `1-exp(-S h(t))` lower bound holds even in the saturated region. Bounding the sum of clipped probabilities alone would be insufficient; the draft correctly handles saturation separately.

## Uniform hard-term guarantee

A hard term has one low anchor and only high other variables. Its deficiency is exactly the event that the anchor succeeds and at least one other variable fails. Conditioning on `U` gives equation (5).

For `S>0`, substituting `t=uz` produces exponent `y/[L(z+epsilon)]`, with `y=S/u` and `epsilon=tau/u`. Dividing by `u min(1,y)` gives the normalized integrand in the draft. For every `a>=0`,

`(1-exp(-ay))/min(1,y)>=1-exp(-a)`

holds by concavity through zero for `y<=1` and monotonicity for `y>=1`. Since `u>=delta`, `epsilon<=B^-2`. Increasing this denominator offset decreases the integrand, yielding the common lower bound `I`. The case `S=0` has zero term gap and requires no division.

Mix the constructed law and independence with probabilities

`(1/I)/(1/I+kappa)` and `kappa/(1/I+kappa)`.

Every hard term then gets deficiency at least `T/(1/I+kappa)` from the first law; every other term gets the same guarantee from independence. The remaining contribution is nonnegative. Positive coefficients permit summation, proving the finite bound. Both mixed components have the same exact marginals, so the mixture preserves them.

## Integral asymptotics

For small `delta`, `B=ln(1/delta)` and `tau=exp(-B)/B^2`; hence

`L=B+2 ln B+ln(1+tau)=B+2 ln B+o(1)`.

In particular `L/B^2->0`, `L~B`, and `ln L~ln B`. The upper bound follows from replacing `z+B^-2` by `z`, then applying `1-exp(-a)<=min(1,a)`. Integration over `[0,1/L]` and `[1/L,1]` gives `(1+ln L)/L`.

For the lower bound on `[1/L,1]`, the inequalities

`a>=1/[Lz(1+L/B^2)]`, and `a^2<=1/(L^2 z^2)`

combine with `1-exp(-a)>=a-a^2/2`. Integrating yields exactly the stated lower estimate. Its main term is `(ln L)/L` times `1+o(1)`, while the subtracted term is `O(1/L)`. Therefore `I~ln L/L`. The additive constant `kappa` is negligible compared with `1/I`, giving the claimed upper leading constant one.

## Dyadic lower bound and interpolation

In the cited dyadic family with `ell` levels, every leaf mean is `1-2^-ell`, anchor means range from `1/2` down to `2^-ell`, and the term gap is `ell`. The exact hull formula gives `H_ell=log_2 ell+O(1)` and therefore ratio asymptotic to `ell/log_2 ell`.

The exact attainment formula is stronger than needed here. The separate elementary estimate in the same result,

`H_ell<=5+log_2(1+(ell-1) ln 2)`,

already gives the matching asymptotic lower ratio with leading constant one. Thus this marginal-floor theorem need not depend on the more intricate exact dyadic attainment construction for its lower-bound direction.

Choosing `ell=floor(log_2(1/delta))` makes `2^-ell>=delta`, with the correct direction of rounding. For sufficiently small `delta`, all leaf and anchor means satisfy the floor. If `B=ln(1/delta)`, then `ell=B/ln 2+O(1)`, so

`ell/log_2 ell=(B+O(1))/(ln B-ln ln 2+o(1))~B/ln B`.

This checks the base conversion, leading constant, and interpolation between dyadic parameter values. The construction has positive hull gap and unit coefficients. Monotonicity of the supremum handles `1/2<delta<1` using the finite bound at `1/2`.

## Nonnegative-box extension

Substitute fixed coordinates first. For every remaining coordinate, the affine map from its box to `[0,1]` is invertible. It preserves the full polynomial's envelope values at the corresponding point and hence its hull gap. Each original positive monomial expands into nonnegative multiples of normalized monomials because all lower endpoints and widths are nonnegative.

For each original term, the minimum expectation of a sum is at least the sum of minimum expectations, and the maximum is at most the sum of maxima. Its exact gap is therefore at most the sum of the expanded subterm gaps. Summing over original terms gives `T_original<=T_expanded`, while `H_original=H_expanded`. Every normalized coordinate still has mean at least `delta`, and the theorem imposes no degree or incidence restriction on the expansion. Applying the cube result proves the extension. Zero expansion coefficients can be discarded; repeated subterms can be combined. This reasoning would not justify a frequency-preserving extension, which the draft appropriately avoids.

## Supporting numerical checks

Using 45-digit arithmetic, I checked 75 instances of the normalized integral inequality at five floors from `delta=1/2` to `10^-200`, three anchor means per floor, and five ratios `S/u` ranging from `10^-4` to `100`. All passed. Twenty clipped-marginal completions, including zero failure probability and probabilities near `1/2`, integrated to the specified failure mean. Both analytic integral bounds held for every tested floor. These checks support the algebra but are not assumptions of the proof.
