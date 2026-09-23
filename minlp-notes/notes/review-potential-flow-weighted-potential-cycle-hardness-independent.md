# Independent audit of weighted-potential hardness on one cycle

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`, independent of
the author and the other reviewer.

Reviewed: [the weighted-potential cycle investigation](potential-flow-weighted-potential-cycle-hardness.md),
including the exact one-scenario verifier and continuous-interval companion.

**Verdict: PASS after the incorporated scaling correction.** The reduction,
membership proof, and positive companion are correct. Fixed absolute
accuracy hardness also follows when arbitrary resistance scaling is allowed.
The other reviewer identified this strengthening; I independently verified
it below, and the author incorporated it. Strong hardness and relative
approximation hardness do not follow.

## Triangle identities

For the consistently oriented triangle, conservation with nominations
`(2,-3,1)` gives exactly `(q+2,q-1,q)`. On `-1/2<q<0`, the first flow is
positive and the other two are negative. The cycle drop is

```
(q+2)^2-(q-1)^2-theta*q^2=6q+3-theta*q^2.
```

It is negative at `-1/2` and positive at zero. The global signed cycle
equation is strictly increasing, so its root in this interval is the unique
physical circulation. Solving the quadratic and rationalizing the negative
root gives the stated `q=-6/(6+sqrt(36+12theta))`.

The objective coefficients sum to zero, so the functional is invariant
under a common potential shift. Its exact form is

```
-5*(pi_0-pi_1)+7*(pi_1-pi_2)
 =-5*(q+2)^2-7*(q-1)^2
 =-105/4-12*(q+1/4)^2.
```

The signs in the second potential difference are essential and correct.
The unique peak occurs at `q=-1/4`, which gives `theta=24`. Direct rational
substitution verifies the endpoints `theta=16/3,144`, the respective roots
`q=-3/8,-1/8`, and their common value `-423/16`. The interior advantage
is exactly `3/16`. A symbolic check independently verified all three
balances, the objective identity, and these three states.

## Series encoding and separation

With zero internal nominations, every edge of the substituted path carries
the same signed flow `q`; its resistances add even though that flow is
negative. Thus the two-point options give the exact effective coefficient

```
theta=12+(12/K)*sum_i(a_i*sigma_i).
```

The graph has `n+2` vertices and `n+2` edges and is a single simple cycle,
including the case `n=1`. Its maximum degree is two. Only the three
original vertices have nonzero nominations or objective coefficients.
The value can reach `-105/4` exactly when the selected subset sums to `K`.
All rational options have polynomial encoding length.

Subtracting the circulation polynomial at `q_0=-1/4` yields exactly

```
(q+1/4)*(6+theta*(1/4-q))=(theta-24)/16.
```

The second factor is positive. For any non-target subset,
`|theta-24|>=12/K`. Using `1/4-q<3/4` and
`theta<=12+12S/K` gives

```
16*(6+theta*(1/4-q))<240+144S/K,
|q+1/4|>=1/(20K+12S).
```

Therefore every non-target selection, including those in a yes instance,
has objective at most the peak minus

```
Delta=12/(20K+12S)^2=3/[4(5K+3S)^2].
```

The robust threshold at the midpoint of this gap has the correct strict
violation direction. Absolute error below `Delta/4` distinguishes the
optimum values. An additive near-optimal discrete selection with error
below `Delta` must be a target subset on a yes instance; its selected
sum can be checked without evaluating its physical state.

## Integer data and fixed absolute accuracy

Multiplication of every resistance by `4nK` preserves the unique flow,
scales every potential and the objective by `4nK`, and gives the stated
integer options and threshold `-105nK`. The nominations and objective
coefficients stay fixed.

There is an additional valid scaling consequence. Write
`L=(5K+3S)^2` and instead scale by `lambda=4nK*L`. The peak becomes the
integer `P=-105nK*L`, all resistance values remain positive integers of
polynomial bit length, and the no-target gap is

```
lambda*Delta=3nK>=3.
```

An absolute-error-one maximum-value estimate is therefore NP-hard to
compute on this unrestricted-scale integer class: a yes estimate is at
least `P-1`, while a no estimate is at most `P-2`, so comparison with
`P-3/2` decides the source instance. A certified interval of width one
works as well. This corrects the draft's denial of a fixed-accuracy
consequence.

The amplification changes numerical magnitudes, not their polynomial
binary encoding lengths. It does not establish strong NP-hardness or
hardness under normalized bounded resistance magnitudes. It also does
not amplify the relative objective gap, so no relative approximation
or FPTAS impossibility conclusion follows from it.

## Exact evaluation of one resistance scenario

On a cycle with fixed balanced rational nominations, choose a rational
particular conserved flow and add a consistently oriented circulation.
Every edge flow is `q+d_e`, with rational `d_e` of polynomial bit length.
The scalar cycle equation is globally strictly increasing and has limits
of opposite sign at infinity. Its breakpoints are the rational numbers
`-d_e`.

Sorting these breakpoints and evaluating the equation there uses rational
arithmetic of polynomial bit complexity. The root is between the extreme
breakpoints: at the smallest one all edge terms are nonpositive, while
at the largest all are nonnegative. A breakpoint root is rational and
can be returned directly. Otherwise exactly one interval contains it.

On that interval the equation has rational degree at most two. Strict
increase excludes an identically constant polynomial on a nonempty
interval. A linear piece is solved rationally; a quadratic piece has an
algebraic root with polynomial encoding length, selected by its interval.
The all-zero-nomination case is included by its common breakpoint.

Every edge pressure drop is a degree-at-most-two polynomial in this same
root. Summing along paths and forming any rational zero-sum weighted
objective keeps all quantities in the single field of degree at most two.
Arithmetic and exact rational threshold comparison remain polynomial in
the number and bit lengths of input coefficients. There is no sum of
independent quadratic radicals from separately optimized blocks.

Guessing a listed resistance option on each edge therefore gives a
polynomial certificate whose weighted objective can be checked exactly.
Both weak threshold attainment and strict upper-bound violation belong
to NP. Robust upper-bound satisfaction belongs to coNP. Combined with
the separated reduction, the stated restricted problems are NP-complete
and coNP-complete.

## Continuous intervals at fixed global rank

The positive companion maps correctly to the reviewed
[fixed-core theorem](../results/fixed-core-block-polyhedral-optimization.md).
Choose a spanning-tree particular flow with zero chord flows and use the
`r` chord flows themselves as coordinates. Every flow is then rational
affine in this fixed-dimensional core. The bound `|z_i|<=B=sum|b_v|`
is valid because each coordinate is an actual physical edge flow.

The affine flow-zero hyperplanes have polynomially many sign cells for
fixed `r`, including lower-dimensional cells. Within a closed sign cell,
every signed-quadratic drop has form `beta_e*p_e(z)` with quadratic
`p_e`. These expressions agree at zero-flow boundaries, so closed-cell
optimization creates no false physical states.

The `r` independent cycle equations are necessary and sufficient for
these drops to be potential differences. Recovering potentials on the
spanning tree expresses the zero-sum objective as
`sum_e w_e*beta_e*p_e(z)`, with rational weights. Each resistance interval
is a scalar bounded polyhedral leaf. The aggregate dimension is `r`,
the leaf dimension is one, and all core degrees are at most two.

The existing theorem already permits this leaf-linear objective with
polynomial core coefficients. Adding a bounded objective coordinate and
one aggregate equality would also be valid but is unnecessary. The
proposed rational bound `B^2*||c||_1*sum_e beta_e^upper` follows from
normalized spanning-tree path sums and has polynomial encoding length.
The case `B=0` is trivial. Hence exact optimization and algebraic witnesses
have polynomial bit complexity at fixed global rank.

This mapping uses fixed nominations; it does not apply the pairwise
pressure nomination-face theorem to a weighted objective. Nor does fixed
maximum block rank suffice for this mapping when global rank is unbounded.

On a tree, fixed nominations determine every edge flow. The weighted
objective is a rational linear function of independent resistance
coefficients, so its finite-set optimum follows by choosing a maximizing
endpoint on each edge. One cycle is therefore the first rank at which
this discrete weighted objective can be hard.

## Scope

I also reran the author's existing mechanism checker. It passed three
symbolic identities, three exact triangle states, and 1,776 resistance
scenarios across 44 instances, including 68 target subsets. Its largest
cycle-law residual was approximately `1.76e-90`. These checks support the
reduction formulas; the membership and positive complexity claims rest
on the arguments above.

The theorem concerns a general weighted potential functional, not a
single pair difference or an arc flow. It is consistent with the positive
cactus results for those narrower objectives. Passive energy, series
aggregation, elementary subset encoding, and the continuous fixed-core
algorithm remain credited ingredients. Whether the specific one-cycle,
fixed-vector obstruction is absent from earlier circuit optimization
literature requires a separate novelty review.
