# Independent audit: coupled separable convex-vector precision

Date: 2026-09-05. Reviewer: `graph_precision_second_review`.

**Status: PASS.** I independently checked the full
[candidate](convex-separable-vector-curvature-rank-precision.md), including
both its box and nonnegative-facet error-body statements. The verified
polynomial rational construction bounds are

```
p_out <= p_conv + n ceil(log2 r) + 17n       (box error),
p_out <= p_conv + n ceil(log2 r) + 18n       (facet error).
```

The comparison is with the original coupled vector problem and arbitrary
convex lifts with unrestricted integer ranges. The assumptions of dense
separated polynomial encoding, convex coordinate summands, positive
budgets, and the specified rank are essential. This is a proof audit,
not a literature-priority certification.

I requested one wording clarification in the facet proof, now applied:
the coordinate chord gaps sum to at most `13/32` **for every facet**.
The estimate is not a sum over all facets. No mathematical correction
or change of constants was needed.

## Shared curvature basis

The concatenated coefficient rows represent functions modulo affine
functions in the direct sum of the coordinate spaces. A row relation in
this matrix gives the same coefficients in every coordinate. Its remaining
difference is a sum of affine coordinate functions, hence an affine function
of the full input. This justifies the global functional relation and its
coordinatewise use.

The determinant-exchange algorithm chooses original normalized outputs
with representation coefficients bounded in absolute value by two. Its
polynomial bit argument from the reviewed one-input rank theorem applies
to the concatenated rational matrix without change; the larger matrix
still has polynomial encoding length. Independent bases for different
coordinates are not used.

Each selected basis output has convex coordinate summands. Consequently,
for every coordinate and every interval, all basis chord gaps are
nonnegative and affine differences cancel. This proves

```
0 <= g_ji <= 2 g_(psi_i),
```

even if some representation coefficients are negative. If `psi_i` is
affine, this inequality forces every original coordinate summand to be
affine. Removing such coordinates from the integer construction preserves
their affine dependence exactly. For lower bounds their values can simply
be fixed; their affine contribution has zero midpoint gap.

## Scalar packing and actual grid capacity

Uniform continuity bounds the cardinality of pairwise midpoint-incompatible
sets: sufficiently close inputs have gap at most the positive tolerance.
A finite maximal set therefore exists. For a selected anchor, the set of
inputs compatible with it is a closed interval, by monotonicity of a convex
function's Jensen gap under interval enlargement. Maximality makes these
compatibility intervals cover the domain.

Split each compatibility interval at its anchor. Each resulting interval
has endpoint midpoint gap at most `tau`, hence full chord gap at most
`2tau`. This yields a cover of at most `2P_i` intervals. Converting the
cover to a partition and applying the scalar three-piece refinement gives
`N_tau(psi_i)<=6P_i`.

The imported hybrid compiler's actual cell count satisfies
`K_i<=486N_tau(psi_i)` in both its greedy and curvature-splitting branches.
For `L_i=ceil(log2 K_i)`,

```
2^L_i <= 2K_i <= 5832P_i.
```

This is also valid for a single cell, where `L_i=0`. The proof uses actual
integer index capacities, so no further ceiling loss remains to be added
at the end. Neither the maximal packing nor an optimal partition has to
be found by the algorithm.

## Superadditivity and comparison with the vector lift

For a twice continuously differentiable convex univariate function,

```
J_phi(a,b) = (1/2) integral_a^b min(t-a,b-t) phi''(t) dt.
```

On each member of a partition of `[a,b]`, its local tent kernel is bounded
by the global tent kernel. The interiors are disjoint, and `phi''>=0`.
This proves the required superadditivity over consecutive subintervals.
The result also extends to continuous convex functions by convex
piecewise-linear approximation, though polynomial smoothness suffices here.

Ordered packing points have adjacent gaps strictly greater than `tau`.
A separation of `h` indices therefore has gap strictly greater than
`h*tau`. Since `Psi` is separable, its full midpoint gap is the sum of the
coordinate midpoint gaps. Thus distinct product-grid points satisfy

```
J_Psi(x(u),x(v)) > tau ||u-v||_1.
```

For box error, `tau=1/(2n)` and distance greater than `2nr` imply
`J_Psi>r`. Because `Psi` is the sum of `r` selected original normalized
outputs, some selected component has midpoint gap greater than one.
The corresponding vector graph midpoint violates the original box error.
This establishes incompatibility for the original vector lift; it does
not substitute a scalar integer minimum at the finer local tolerance.

For facet error, the selected outputs are normalized facet functions.
If an original nonnegative Jensen vector belongs to `K`, every normalized
facet gap is at most one. Thus `J_Psi>r` again contradicts the original
error body. The local tolerance `1/(4n)` gives the claimed distance
threshold `4nr`.

Only finitely many graph witnesses are needed for the product code.
Assigning a lift to each witness and grouping integer coordinates by
parity proves that a pairwise incompatible code has at most `2^p` points.
No closure, measurability, or bounded-integer assumption is required here.

## Lattice-ball constant

For `t=ar/(ar+1)` and integer radius `anr`, summing
`t^(||z||_1-anr)` over `Z^n` gives

```
|B_1(anr) intersect Z^n|
 <= (1+1/(ar))^(anr) (2ar+1)^n
 < [3(2a+1)r]^n.
```

The geometric series is `(1+t)/(1-t)=2ar+1`. The strict final bound follows
from `(1+1/q)^q<3` for `q=ar>=1` and
`2ar+1<=(2a+1)r`. It holds for `n=1` and `r=1` as well.

Greedy deletion from the finite product grid removes at most the full
integer lattice-ball count per selected point, including at grid boundaries.
The resulting code therefore has size at least the product cardinality
divided by `(15r)^n` for `a=2`, or `(27r)^n` for `a=4`.
This gives precisely the claimed parity inequalities. No code or product
grid enumeration enters the construction.

## Box bands and simultaneous graph containment

At local tolerance `1/(2n)`, the scalar chord error is at most
`13/(32n)`. The shared basis bound and summation over coordinates give
normalized component chord gap at most `13/16`. Downward rounding of each
coordinate summand's endpoint values by at most `1/(8n)` gives total
rounding error at most `1/8`.

Writing `T_j` for the sum of exact coordinate chords, and `y_j` for the
rounded sum including the exact affine part,

```
0 <= T_j-G_j <= 13/16,
0 <= T_j-y_j <= 1/8.
```

Hence the band `[y_j-13/16,y_j+1/8]` contains the exact graph and admits
normalized absolute error at most `15/16`. Every output uses the same
selected knots and the same interpolation weight for each coordinate.
The coordinate paths cover their entire intervals, so their independent
choices cover the full input cube. Repeated or reversed coordinate cells
remain valid. No combinations at inconsistent input values are admitted.

## Facet bands, rounding, and degenerate cases

Write `B_kj=A_kj/b_k`. The facet functions have convex coordinate summands
because these weights are nonnegative. The same shared-basis argument
at tolerance `1/(4n)` gives, for each facet,

```
sum_i g_(H_k,i) <= 2n * 13/(64n) = 13/32.
```

The original vector's exact chord gap is nonnegative, so this says
`T-F in (13/32)K`. Compactness of `K` implies that every column of `A`
has a positive entry, and in particular `M_A=max_k sum_j B_kj>0`.
With endpoint error at most `min(1,1/(16nM_A))`, the sum of coordinate
rounding errors obeys each facet budget `1/16`. Convex interpolation
preserves this bound. Therefore

```
y-F in (15/32)K.
```

The half-body band `w-y in K/2` contains the graph and has total error
in `(31/32)K`. Continuous auxiliaries `s>=|w-y|` and `As<=b/2`
project exactly to that band because `A>=0`. No facet selectors are needed.

If the concatenated facet rank is zero, all facet coordinate gaps vanish.
Each original component has a positive coefficient in some facet, so its
nonnegative coordinate gaps must vanish too. The entire graph is affine.
The same argument handles affine-only input coordinates. A weighted
`l_1` body with positive weights has one nonaffine facet function and rank
one whenever the graph is nonaffine, proving the stated `18n` corollary.

## Rational size and final counts

The input includes the full dense separated polynomial arrays and, in the
facet case, the rational matrix and budgets. Normalization, sums, rational
basis computation, local tolerances, and row sums have polynomial bit
length. Every scalar compiler has polynomial-time indexed rational knots
with a polynomial-bit common denominator. Evaluating the original dense
summands at these knots has polynomial complexity even when degrees grow.
Fixed output precision and offsets encode signed endpoint numerators.

Only the `L_i` index bits per coordinate are declared integer. Internal
Boolean gate wires are continuous and forced to their Boolean values by
those index bits; their products with coordinate interpolation weights use
exact binary-product hulls. Forming the output sums and affine terms adds
linear rows. The construction does not enumerate the Cartesian product
of coordinate cells or introduce output-specific integer selectors.

Multiplying the capacity inequalities and applying the original-lift code
bound gives

```
p_out <= p_conv + n log2(5832*15r)
      <  p_conv + n log2 r + 17n,
```

or the same calculation with `27r` and `18n`. The integer statements with
`n ceil(log2 r)` follow immediately. There is no missing additional unit
from rounding the total count.

## Independent exact checks

I ran checks separate from the author's code:

- 96 exact integer lattice-ball counts across `n=1,...,8`, `r=1,...,6`,
  and both thresholds, using the closed count
  `sum_k 2^k binom(n,k) binom(anr,k)`;
- 16 systems of nine coupled polynomial outputs in three inputs, with
  one shared concatenated curvature basis of rank three;
- 3,456 exact coordinate gap inequalities and 1,152 exact assembled
  component graph-band checks with rational endpoint rounding.

All passed. The checks supplement the continuum packing proof and the
variable-dimension bit analysis. No claim is made here for mixed
multivariate monomials, arbitrary tilted error bodies, sparse huge-degree
encoding, or necessity of the stated overheads.
