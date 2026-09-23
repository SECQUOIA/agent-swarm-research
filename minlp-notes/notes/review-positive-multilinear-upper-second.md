# Second independent review: logarithmic degree upper bound

Date: 2026-09-04. Reviewer: `review_scaling_characterization`.
Reviewed: `results/positive-multilinear-degree-upper-bound.md`.

## Verdict

The unit-box theorem is correct as written. For nonnegative-coefficient multilinear
polynomials of maximum degree `d≥2`, it proves

```
tbtgap ≤ [2(K+1)/(1−e^(−1))] chgap,
K = 1+floor(log₂(d−1)).
```

The proof defines actual joint distributions for all coordinates, not separate
incompatible couplings for different monomials. All boundary cases are covered.
No numerical evidence is required for the theorem. This review does not establish
novelty of the upper bound in the open literature.

## Deficiency identity

For a monomial choose a coordinate with smallest marginal `u` and write the other
failure marginals as `y_j=1−x_j`. Its term-by-term gap is
`T=min(u,Σ_j y_j)`, from the exact unit-box monomial envelopes. In any joint binary
distribution with the prescribed means, its deficiency is the probability that
the chosen coordinate is one and at least one other coordinate is zero. It is
nonnegative and equals `u−E(product)`.

Positive coefficients imply that the full concave envelope is the sum of monomial
concave envelopes, attained by a common nested-threshold distribution. The
multilinear vertex interpolation identity gives the full convex envelope as the
minimum expected polynomial over binary distributions with the prescribed means.
Consequently the hull gap is exactly the largest expected weighted total deficiency.
These observations justify the central identity used in the draft.

## The independent distribution

The global classification calls a coordinate low when `x_i≤1/2`. A term with at
least two low coordinates has independent deficiency at least `u/2≥T/2`: after
choosing a minimum-marginal coordinate, another low coordinate remains in the product.

An all-high term has `u>1/2`. With `Y=Σ_j y_j` and `c=1−e^(−1)`, independence gives

```
u(1−∏_j(1−y_j)) ≥ c u min(1,Y) ≥ (c/2) min(u,Y).
```

The last inequality holds both for `Y≤u` and `Y>u`, using `u>1/2`. Thus the single
independent distribution handles every term except those with exactly one low
coordinate. Nonnegative deficiencies ensure that its contributions to the
remaining terms can be discarded safely.

## The dyadic distributions are globally feasible

At scale `B≥1`, use one common uniform random variable `U`. Low coordinates are
one exactly when `U≤x_i`. For a high coordinate with failure marginal `y_i>0`, put
`h_i=min(By_i,1)` and fail independently of other high coordinates, conditional
on `U`, with probability `y_i/h_i` if `U≤h_i`, and zero otherwise.

The failure probability integrates to `h_i(y_i/h_i)=y_i`. It lies in `[0,1]`:
if `By_i≤1`, it equals `1/B`; otherwise it equals `y_i`. A coordinate with `y_i=0`
is always one. The conditional independence is imposed once over the entire set
of high coordinates. Every monomial therefore sees the required conditional
independence as a restriction of one well-defined global distribution.

For a term with exactly one low coordinate, that coordinate is necessarily its
minimum-marginal coordinate and its deficiency is supported on `U≤u≤1/2`.
For `U=t` in this range, a high coordinate with `y_j≥t/B` is active and has failure
probability at least `1/B`. Thus, writing `N(s)=#{j:y_j≥s}`,

```
G_B ≥ ∫_0^u [1−(1−1/B)^N(t/B)]dt
    ≥ c ∫_0^(u/B) min(B,N(s)) ds.
```

The first inequality remains valid when `By_j>1`, because then the failure event
is active for every `U∈(0,1)` and its conditional probability is greater than
`1/B`. For `B=1`, active failures are deterministic; when `N=0` the integrand is
zero, as the draft explicitly states. There is no need to assign an ambiguous
meaning to `0^0`.

## The dyadic sum and tail integral

There are exactly `K=1+floor(log₂(d−1))` powers of two from one through the largest
power not exceeding `d−1`. For any `0<s≤u` with `N(s)>0`, choose the largest power
of two no greater than `min(N(s),u/s)`. It is present in the scale list and is at
least half that minimum. Its integral includes `s`, and its contribution at `s`
is precisely that scale. Hence

```
Σ_B G_B ≥ (c/2) ∫_0^u min(N(s),u/s) ds.
```

The integral is at least `min(u,Y)`, where `Y=Σ_j y_j`. If `Y≤u`, every failure
marginal is at most `u`, the integral of `N` on `[0,u]` is `Y`, and
`sN(s)≤∫_0^s N≤Y≤u`; the truncated integrand equals `N` throughout.

If `Y>u`, the integral of `N` on `[0,u]` is at least `u`. Indeed, one marginal
at least `u` already gives that much area; otherwise the area equals `Y`.
The cumulative integral is continuous, so choose `v≤u` with `∫_0^vN=u`.
On `(0,v)`, monotonicity gives `sN(s)≤∫_0^s N≤u`; therefore the truncated
integrand equals `N` on this prefix, contributing `u`. This proves the lemma.
When `u=0`, the term gap is zero and none of the divisions are needed.

## Combining all terms

Take a uniform mixture of the independent distribution and the `K` dyadic
distributions. It preserves every marginal. For every term, its summed deficiency
across the component distributions is at least `(c/2)T`: independence proves
this for the easy classes and the dyadic sum proves it for the one-low class.
The nonnegative coefficients permit summation, and every discarded contribution
is nonnegative. Dividing by the number `K+1` of distributions proves the claimed
constant. This establishes an existence bound, not a polynomial-time convex-envelope
algorithm or a polynomial support-size claim.

## Independently checked extension to all nonnegative boxes

During this audit I proposed the following extension. The first reviewer,
`audit_packing`, independently confirmed it. It requires only an inequality
between term-by-term relaxations, not their equality.

On a finite box `[l,u]` with `l≥0`, substitute `x_i=l_i+(u_i−l_i)y_i`. Each original
positive monomial becomes a sum of positive unit-box monomials of degree at most
its original degree. For any decomposition `g=Σ_h g_h`, independently of this
particular substitution,

```
cav(g) ≤ Σ_h cav(g_h),
vex(g) ≥ Σ_h vex(g_h).
```

The first sum is a concave majorant of `g`, and the second is a convex minorant.
Therefore the original monomial gap is no larger than the sum of gaps of its
expanded terms. Summing over original monomials gives

```
original tbtgap ≤ expanded tbtgap.
```

The full polynomial is unchanged by this affine reparametrization, so its full
hull gap is invariant. Applying the proved unit-box theorem to the expanded
positive polynomial therefore gives the same degree-dependent bound for the
original term-by-term gap on any nonnegative box. Coordinates with zero box
width are fixed and can be eliminated first. Expansion can be large, but this
argument asserts existence of a bound and does not claim an efficient expansion
algorithm or representation.
