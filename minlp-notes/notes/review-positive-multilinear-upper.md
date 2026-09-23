# Independent audit of the logarithmic degree upper bound

Date: 2026-09-04. Reviewed result:
`results/positive-multilinear-degree-upper-bound.md`.

**Outcome:** the claimed bound is mathematically correct:

```
K=1+floor(log₂(d−1)),  c=1−exp(−1),
tbtgap ≤ [2(K+1)/c] chgap.
```

I checked the argument independently of its author and the second reviewer, including
the common coupling, all monomial classes, dyadic scale selection, integral lemma,
and boundary cases. I also independently confirmed the second reviewer's extension
to arbitrary nonnegative boxes, detailed below. No unresolved mathematical issue was
found. This is an independent agent audit, not journal peer review, formal theorem
verification, or certification that the result is absent from the literature.

## Deficiency representation and scope

For a monomial choose any coordinate attaining its smallest mean `u`. Its exact
term-by-term gap on the unit cube is

```
T=min(u, Σ_{j≠anchor}(1−x_j)).
```

This follows directly by subtracting its lower envelope
`max(0,Σ_j x_j−|e|+1)` from its upper envelope `u`. At a binary vertex the
nonnegative deficiency `D=X_anchor−∏_j X_j` equals the stated anchored failure
indicator. Under a distribution with the required coordinate means,
`E D=u−E∏_j X_j`.

A common comonotone distribution attains the monomial upper envelopes simultaneously
for nonnegative coefficients. The multilinear graph hull equals its vertex graph
hull. Consequently the maximum weighted expected deficiency is exactly the full
convex-hull gap. This establishes the optimization direction: constructing any one
feasible common distribution supplies a lower bound on the hull gap.

Affine terms have zero gap under both relaxations and can be removed. Zero coefficients
can be removed as well. If no nonlinear terms remain, the conclusion is immediate.
Nonnegative coefficients are essential when summing the per-monomial inequalities.
The theorem is stated as an inequality, so it also covers zero hull gaps without
forming an undefined ratio.

## Independent distribution and the three classes

The classification is global: a coordinate is low exactly when `x_i≤1/2`.

- With at least two low coordinates, a minimum coordinate can serve as anchor and
  another low coordinate remains. Under independence, the monomial deficiency is
  at least `u/2≥T/2`.
- With no low coordinates, `u>1/2`. If `S=Σ_{j≠anchor}(1−x_j)`, independence gives
  deficiency at least `c u min(1,S)`. Since `min(1,S)≥min(u,S)=T` and `u>1/2`,
  this is at least `cT/2`.
- With exactly one low coordinate, that coordinate is a minimum and can serve as
  the unique anchor. Its mean is at most `1/2`. The remaining coordinates are all
  high, which is the class handled by the dyadic construction.

Ties at `1/2` belong to the low class. A monomial with several such coordinates is
therefore in the first class. No monomial is omitted or counted as needing two
incompatible anchor choices.

## Common dyadic coupling and its marginals

For each scale `B=1,2,…,2^(K−1)` restricted to powers of two, the construction
uses one uniform variable `U` for every coordinate. Low coordinates take their
success event to be `[0,x_i]`. A high coordinate with failure mean `y_i=1−x_i>0`
uses support length `h_i=min(B y_i,1)` and conditional failure probability
`y_i/h_i` on `[0,h_i]`, zero elsewhere. The high coordinates are mutually
independent conditional on `U`.

This defines a single distribution for the whole polynomial, not a separate
incompatible coupling for each monomial. Conditional Bernoulli coins can be assigned
to every high coordinate once and reused in all its monomials. Its marginal failure
probability is exactly `h_i(y_i/h_i)=y_i`; moreover `h_i≥y_i`, so the conditional
probability lies in `[0,1]`. Coordinates with `y_i=0` are fixed at one, avoiding
`0/0`. Saturation at `h_i=1` causes no problem.

For a one-low monomial and `U=t≤u`, any leaf with `B y_j≥t` is active. Its
conditional failure probability is at least `1/B`: it equals `1/B` before
saturation, and after saturation it is `y_j≥1/B`. Conditional independence gives
union probability at least `1−(1−1/B)^N`, where `N=N(t/B)` counts active leaves.
This is at least `c min(1,N/B)` for `B>1` by the exponential inequality. At `B=1`
it is exactly one when `N>0` and zero when `N=0`, so the same lower bound holds
without relying on a convention for `0^0`.

The substitution `t=B s` therefore gives

```
G_B ≥ c ∫₀^(u/B) min(B,N(s)) ds.
```

Failure means equal to zero affect neither the integral nor its count for `s>0`.
Endpoint inclusions at `s=y_j` have measure zero and do not affect the proof.

## Dyadic summation and the tail integral

For `0<s≤u` with `N(s)>0`, the number
`q=min(N(s),u/s)` satisfies `1≤q≤d−1`. The largest power of two `B≤q` lies
in the selected scale set and satisfies `B>q/2`. This is why the draft's
**floor logarithm is sufficient**; a ceiling is unnecessary. This scale also has
`s≤u/B` and `min(B,N(s))=B`. It follows pointwise that

```
Σ_B 1[s≤u/B] min(B,N(s)) ≥ min(N(s),u/s)/2.
```

All summands are nonnegative and there are finitely many scales, so interchanging
the sum and integral is justified. The intervals `(0,u/B)` are subsets of `(0,u)`.
Thus the summed deficiencies are at least
`(c/2) ∫₀^u min(N(s),u/s) ds`.

I checked the claimed integral lemma directly. Let `S=Σ_j y_j`.

- If `S≤u`, then every `y_j≤u`, `∫₀^u N=S`, and monotonicity gives
  `sN(s)≤∫₀^s N≤S≤u`. The minimum is therefore `N(s)` throughout the interval.
- If `S>u`, then `∫₀^u N≥u`. Indeed a leaf with `y_j≥u` suffices; otherwise
  this integral equals `S`. The indefinite integral is continuous, so choose
  `v≤u` with `∫₀^v N=u`. For `s≤v`, monotonicity gives
  `sN(s)≤∫₀^s N≤u`. Integrating the minimum through `v` therefore gives exactly
  `u`, and the remaining contribution is nonnegative.

This proves the lower bound `min(u,S)=T`. If `u=0` or `S=0`, the target is zero
and no division or integral argument is required. The proof uses only a finite,
nonincreasing step function `N`, so there is no hidden regularity assumption.

## Final mixture, constant, and degree two

There are exactly `K` dyadic distributions and one independent distribution.
Their uniform mixture preserves every coordinate mean. The summed deficiency is
at least `cT/2` for every monomial, using its appropriate class. Deficiencies in
the other distributions are nonnegative, so they cannot undo that bound. Weighting
by nonnegative coefficients and dividing by `K+1` proves the stated theorem.

For `d=2`, `K=1` and the sole scale is `B=1`. The one-low class has one high
leaf, and this scale actually attains its full term gap `min(u,y)`. The advertised
constant reduces to `4/(1−e^(−1))`, which is conservative but valid. The theorem
makes no claim to recover the sharper known bilinear constant.

## Extension to every nonnegative box

The second reviewer proposed this extension and I checked it independently. Suppose
`0≤l≤v` and the original multilinear polynomial has nonnegative coefficients and
maximum degree at most `d`. Remove fixed coordinates first. The affine map
`x_i=l_i+(v_i−l_i)y_i` is then a bijection from the unit cube to the remaining
box. Expanding an original monomial produces a sum of nonnegative-coefficient
unit-cube monomials of degree at most `d`.

For any sum of functions `g=Σ_h g_h` on a common domain,

```
cav(g) ≤ Σ_h cav(g_h),    vex(g) ≥ Σ_h vex(g_h).
```

Hence the exact gap of the original individual term, after rescaling, is at most
the sum of the gaps of its expanded monomials. Summing over the original terms gives

```
T_original ≤ T_expanded.
```

Combining repeated positive monomials leaves this summed term gap unchanged, and
affine contributions have zero gap. The degree bound still holds. The full
polynomial's hull gap is invariant under the affine change of coordinates, giving

```
T_original ≤ T_expanded ≤ [2(K+1)/c] H_expanded
           = [2(K+1)/c] H_original.
```

Thus the same constant applies to the original, unexpanded term-by-term relaxation
on any nonnegative box. The needed inequality goes in the correct direction:
expansion may weaken the term-by-term relaxation, which is harmless when proving
an upper bound on the original term-by-term gap. Zero-width coordinates and zero
lower bounds are both covered by the preliminary reduction and nonnegative expansion.

## Supplementary exact finite checks

I evaluated the global coupling formulas in exact rational arithmetic on all sorted
marginal tuples of monomial degrees `2,…,8` drawn from

```
{0, 1/16, 1/4, 1/2, 3/4, 15/16, 1}.
```

This covers 6,427 tuples, including endpoints, ties at the low/high threshold,
zero failure means, and saturated supports. For every dyadic scale I integrated
the conditional product exactly over its rational breakpoints, verified the high
coordinate marginal equations and valid conditional probabilities, and checked
nonnegative deficiencies. The sum of the independent and dyadic deficiencies
was at least `T/3` in every case, which is stronger than the claimed `cT/2`
for those cases. The smallest observed exact ratio of that summed deficiency to
`T` was `1/2`, attained at the bilinear means `(1/16,1/2)`.

These are supplementary checks, not an all-input certificate. The analytic proof
above establishes the stated constant for every degree and every allowed point.
