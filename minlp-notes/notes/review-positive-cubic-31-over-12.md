# Independent review of the cubic upper bound 31/12

Date: 2026-09-04. Target:
[`results/positive-cubic-rounding-upper-bound.md`](../results/positive-cubic-rounding-upper-bound.md).
This is an independent agent review, not external peer review.

**Verdict:** The universal bound `tbtgap≤(31/12)chgap` is correct for positive
multilinear polynomials of maximum degree three on finite nonnegative boxes. The
three distributions preserve all coordinate marginals, every monomial class satisfies
the required bound, and the fixed-mixture optimality certificate is valid within its
stated scope. Two minor proof-wording qualifications were requested and incorporated:
exclude zero-gap terms before division, and limit the optimality conclusion to uniform
termwise guarantees from fixed mixtures. No unresolved mathematical issue remains.

## Marginals and the common-distribution requirement

The proof uses a single global mixture with weights `18/31,6/31,7/31` on endpoint
orientation `O`, independent rounding `I`, and the threshold distribution `B`.
The weights are nonnegative and sum to one. Their definitions use the full marginal
vector but not monomial-specific parameters, so they can be applied simultaneously
to every term of a polynomial.

In `O`, either endpoint interval has length `x_i`; the independent orientation coin
therefore preserves its marginal. In `I` this is immediate. In `B`, low coordinates
`x_i≤1/2` equal `1[U≤x_i]`; high coordinates fail with conditional probability one-half
on an interval of length `2(1−x_i)<1`, so their unconditional failure probability is
`1−x_i`. Conditional high-coordinate failures are mutually independent. Values zero
and one cause no problem: they are deterministic up to null endpoint events.
The boundary `x_i=1/2` belongs to the low class throughout the argument.

For any binary distribution with the prescribed means, a monomial's deficiency
`u−E product` is nonnegative, since its product is bounded by its anchor variable.
Thus omitted contributions from other mixture components may safely be ignored.
Positive coefficients permit summing the individual guarantees. Zero termwise gaps
need no estimate. Affine terms affect neither full nor termwise gaps.

## At least two low coordinates

For a cubic term with `u≤v≤1/2`, its termwise gap is `T=u` because `1−v≥u`.
If the anchor and the second coordinate have opposite endpoint orientations, the
latter fails throughout the anchor interval. This event has probability one-half,
so `D_O≥u/2`. Independence gives `D_I=u(1−vw)≥u/2` because `v≤1/2` and `w≤1`.
Their weights sum to `24/31`, giving deficiency at least `12T/31`.
This includes all ties at one-half and the case where the third coordinate equals one.

## Exactly one low coordinate

Let `a=1−v≥b=1−w≥0`, so `T=min(u,a+b)`. Conditional on the anchor orientation,
the opposite-orientation exclusions are nested intervals. Under `B`, the low anchor
is active for `U≤u`, and the two high failure intervals have lengths `2a,2b` with
independent failure probability one-half. Integrating directly gives

```
D_O = (1/2)min(u,a)+(1/4)min(u,b),
D_B = (1/2)min(u,2a)+(1/4)min(u,2b).
```

The four cases in the written proof exhaust `a≥b≥0` and include shared boundaries.
For clarity, their weighted contributions and the decisive inequalities are:

- `a≤u/2`: `18D_O+7D_B=16a+8b≥12(a+b)=12T`, by `a≥b`.
- `b≥u/2`: `D_O≥3u/8` and `D_B=3u/4`; the weighted sum is at least `12u≥12T`.
- `b≤u/2≤a≤u`: the weighted sum is `9a+8b+7u/2`. If `a+b≤u`, then
  `3a+4b≤4u−a≤7u/2`, giving the required bound `12(a+b)`.
  If `a+b≥u`, then `9a+8b≥8u+a≥17u/2`, giving the bound `12u`.
- `b≤u/2` and `a≥u`: the weighted sum is `25u/2+8b≥12u≥12T`.

The case `u=0` is trivial. Independence contributes a nonnegative amount, so division
by the common mixture denominator 31 proves the desired termwise fraction.

## No low coordinates

Write `c=1−u≥a=1−v≥b=1−w≥0`, with `c<1/2`. In `B`, the probabilities of at least
one failure are `7/8`, `3/4`, and `1/2` on the nested intervals of lengths
`2b`, `2(a−b)`, and `2(c−a)`. Their total is `c+a/2+b/4`. Subtracting the anchor's
failure probability `c` gives the deficiency. Consequently

```
D_O=D_B=a/2+b/4 ≥ 3(a+b)/8 ≥ 3T/8.
```

For independence, put `s=a+b≤1` and use `ab≤s²/4`. When `T>0`:

- If `s≤u`, then `D_I/T≥u(1−s/4)≥u(1−u/4)≥7/16`.
- If `s≥u`, then `D_I/T≥s−s²/4≥u−u²/4≥7/16`.

The functions in these comparisons are increasing on the relevant unit intervals,
and `u>1/2`. The common expression at `u=1/2` is `7/16`; it remains a valid lower
bound in the open high class. Thus the mixture has deficiency at least

```
[(18+7)/31](3/8)T+(6/31)(7/16)T = (12/31)T.
```

All-high terms with zero gap, including all coordinates equal to one, are explicitly
excluded before division by `T`. The conclusion is trivial for them.

## Quadratic terms and general boxes

For two marginals `u≤v`, the endpoint deficiency is exactly `T/2`, where
`T=min(u,1−v)`. If both coordinates are low, `T=u` and independence gives at least
`T/2`; their two weights produce `12T/31`. With exactly one low coordinate,
`D_B=min(u,2(1−v))/2≥T/2`; the `O` and `B` weights produce `25T/62>12T/31`.
If both are high, `D_B=T/2` and independence gives `uT≥T/2`, so all three together
produce at least `T/2`. Therefore every quadratic term is covered as well.

The transfer to nonnegative boxes uses the already reviewed positive-expansion
argument. Fix zero-width coordinates and apply the invertible affine scaling on the
remaining coordinates. Expanded coefficients are nonnegative and degrees do not
increase. Subadditivity of concave envelopes and superadditivity of convex envelopes
show that the original termwise gap is at most the expanded one. The full hull gap
is invariant under the coordinate transformation. Zero coefficients produced by the
expansion may simply be omitted. This gives the claimed bound on the original
termwise relaxation of the full box.

## Optimality within the stated fixed-mixture class

For arbitrary fixed weights `(w,r,v)` on `(O,I,B)`, the three test configurations
in the result have these exact or limiting normalized deficiencies:

| Test marginals | `(D_O/T,D_I/T,D_B/T)` |
|---|---|
| `(u,1/2)`, `0<u≤1/2` | `(1/2,1/2,0)` |
| `(ε,1−ε²,1−ε²)`, `ε↓0` | limit `(3/8,0,3/4)` |
| `(u,1−u/2,1−u/2)`, `u↓1/2` from above | limit `(3/8,7/16,3/8)` |

In the second row, for sufficiently small positive `ε`, the term gap is `2ε²`.
The endpoint and threshold deficiencies are exactly `3ε²/4` and `3ε²/2`, while
independence has normalized value `ε−ε³/2→0`. In the third row, for `1/2<u<2/3`,
the gap is `u`; the endpoint and threshold fractions are `3/8` and the independent
fraction is `u−u²/4→7/16`. These checks ensure the limiting configurations stay in
the classes used by their respective formulas.

Accordingly any universal termwise fraction satisfies

```
α≤1/2−v/2,
α≤3/8+(3/8)v−(3/8)r,
α≤3/8+r/16.
```

Averaging these inequalities with weights `3/31,4/31,24/31` cancels both `r` and `v`
and gives `α≤12/31`. The proposed mixture attains that guarantee by the complete
proof above. This certifies optimality among fixed mixtures for a uniform termwise
bound. It neither proves that `R(3)=31/12` nor rules out a stronger coefficient-aware
or nontermwise argument using the same component distributions.

## Independent exact numerical replay

A separate implementation evaluated `O` by enumerating all orientation choices and
intersecting their intervals. It evaluated `B` by partitioning `[0,1]` at every low
threshold and every doubled high failure threshold, then integrating the actual
conditional product probabilities. This did not use the closed-form deficiency
expressions being audited.

Using exact rational arithmetic, all 2,002 sorted quadratic and cubic marginal tuples
with coordinates in `{0,1/20,...,1}` satisfied the `12/31` guarantee. Six further
near-boundary cases used the two limiting cubic configurations with parameters
`1/10`, `1/100`, and `1/1000`; all passed. The smallest observed normalized mixture
deficiency was exactly `12/31`, at the quadratic tuple `(1/20,1/2)`. Single-coordinate
integrations also confirmed all three distributions' marginals. These finite checks
support the proof and do not replace its complete case analysis.
