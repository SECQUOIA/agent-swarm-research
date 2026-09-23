# Independent audit of the convex two-output box-error gap

Date: 2026-09-05. Verdict: PASS on
[the full note](convex-vector-one-bit-box-gap-investigation.md), including
the piecewise-linear model, degree-32 polynomial model, and optional
Bernstein transfer.

## Exact degree-32 construction

The stated rational range constants satisfy `1/2<L<3/4` and `0<d<1/4`.
I checked these as exact fractions. The first two inequalities equivalently
compare `3*31^32` and `2*31^32` with `32^32`, without relying on decimals.
Monotonicity of the two powers places their graph pieces inside the listed
three boxes. Their individual coordinate range widths are strictly below one.

For the convex hull of the three labeled boxes, integer labels zero and
two restrict to their respective boxes. Label one forces equal outer
weights `t`, with middle weight `1-2t`. Conditional points in each box can
be consolidated by convexity. The minimum possible input is
`c(1-2t)+(1-c)t=c+t(1-3c)>=c`, and the symmetric maximum is at most `1-c`.
Every output coordinate is at most
`L+t(A+d-2L)<=max(L,(A+d)/2)<1`, while the true graph coordinates there
lie in `[0,L]`. Both are nonnegative, so their absolute difference is below
one. This proves validity of every integer fiber, not just selected chords.

The exact graph witnesses at zero, one half, and one are pairwise incompatible
with a fixed binary assignment. For the first pair, the indicated gap is
strictly above one; equivalently,
`8^32+3*4^32>12*7^32`, also checked as an exact integer inequality.
The second pair is symmetric and the outer pair has a larger chord value
at the same test input. Thus three binary assignments are necessary and
two binary variables suffice by the explicit three-box union.
The same incompatibility excludes a zero-integer convex formulation.
Consequently the exact counts are one general integer and two binaries.

The convex hull of finitely many rational bounded boxes has a rational
extended formulation using continuous disaggregated box coordinates and
weights; their weighted label is the sole declared general integer.
There is no hidden binary requirement in that construction. Adding `48x`
to the first polynomial makes its derivative nonnegative and is an affine
graph-output transformation, preserving all error and count arguments.

## Supporting variants

The piecewise-linear construction has the same valid label-one input geometry
and output bound `3/4`. Its three pairwise chord obstructions `9/8,9/8,21/16`
are correct. In the Bernstein variant, nonnegative sampled second differences
preserve convexity, and the binomial Lipschitz estimate is `3/256<1/64`.
Output thickening preserves complete polynomial graph coverage and keeps
error below one; chord gaps change by at most twice the uniform approximation
error. Both exact integer counts are therefore preserved. No correction
to either variant was required.

## Independent direct-product consequence

Taking `n` independent inputs and the `2n` degree-32 outputs obtained by
applying the pair to each coordinate gives a general-integer formulation
with `n` integers, by taking the product of the reviewed formulations.
The Cartesian grid `{0,1/2,1}^n` has `3^n` exact graph witnesses. Any two
distinct grid inputs differ in at least one coordinate, where the same
pairwise chord obstruction applies to an output of that coordinate.
Thus all `3^n` witnesses require distinct binary assignments and

```
p_bin>=ceil(n log2 3),
p_bin-p_conv>=ceil(n log2 3)-n.
```

A product of the three-box unions has `3^n` pieces and realizes the same
binary count, so the binary lower bound is exact for finite formulations.
This is a growing gap with growing input dimension, fixed degree 32,
and unit box error. It does not resolve the one-input growing-output
question, and it makes no assertion that `p_conv=n` is the exact minimum.

## Improved constants give both exact product counts

The subsequent choice `A=7/4`, `c=1/48`, still at degree 32, also passes.
Exact fraction checks give `A-1<L=A(1-c)^32<1`, `d=A c^32<1/4`, and
`max(L,(A+d)/2)<1`. Thus the same three-box integer-hull upper proof is
unchanged. For inputs zero and one half, the first-component chord at
`1/6` has error

```
(2/3)A+(1/3)A/2^32-A(5/6)^32>1.
```

The symmetric pair uses input `5/6`. For inputs zero and one, the
first-component chord at `1/3` has error
`(2/3)A-A(2/3)^32>1`. I checked both strict inequalities as exact fractions.
All three obstructions now use weights with denominator three.

For the `n`-fold product, choose exact lifts at the `3^n` grid points.
If two of their integer vectors have equal residues modulo three, both
their one-third and two-thirds convex combinations have integer coordinates.
A coordinate where the grid points differ provides one of the preceding
forbidden chord combinations, contradicting feasibility. Hence the `3^n`
contacts have distinct residues in `F_3^p`, so `p>=n`. Together with the
explicit product upper formulation this gives exactly

```
p_conv=n,        p_bin=ceil(n log2 3).
```

This strengthened conclusion is proved for the improved constants. The
earlier `A=3/2` example and its weaker product estimate remain valid.
