# Independent audit of the implicit convex-vector knot overlay

Date: 2026-09-05. Reviewer: `quadratic_weighted_precision`.
Status: PASS after a full independent read of
[the candidate](compiled-convex-vector-knot-overlay.md).

The deterministic bisection implementation does return nondecreasing knots.
At a fixed node its oracle value and tolerance are independent of the target;
its left/return/right target regions are ordered. The geometrically ordered
search subtrees therefore prove monotonicity by induction, even if oracle
values at different nodes are inconsistent with monotonicity. Fixed depth,
exact forced endpoints, and dyadic zero padding preserve the conclusion.
Reversing reflected-piece indices and concatenating rational pieces gives
one sorted scalar array without enumerating it.

The right-endpoints-only merge is correct. Prepending one zero yields exactly
`sum_j K_j` cells, including repeated endpoints. Any positive-width merged
cell lies inside a source cell of every array: otherwise an intervening source
knot would also appear in the merged multiset. Repeated entries cause only
zero-width cells and preserve the coverage and error arguments.

The exact implicit order-statistic algorithm has polynomial bit complexity.
A product of the polynomially many rational piece-endpoint denominators,
multiplied by the largest required dyadic factor, represents every input knot.
Its value can be exponential, but its bit length is polynomial. Searching
an array for its count at a proposed numerator uses `O(log(K_j+1))` exact
indexed calls. Searching numerators uses `O(log(H+1))` count queries. The
number of outputs and all nested search depths are polynomial, so this does
not hide enumeration of either the grid or the possible denominators.

Exact dense-polynomial evaluation at a rational knot has polynomial bit
length: powers multiply the knot bit length by at most the dense degree.
Directed dyadic rounding then supplies the stated downward `epsilon_j/8`
error. A known fixed offset handles signed output values. This does not need
a positive-coefficient arithmetic primitive. All affine terms may be evaluated
with the polynomial or restored exactly.

Restriction preserves the exact convex chord bound `13epsilon_j/16` on each
merged cell. Interpolating the downward endpoint approximations changes the
true chord by a value in `[-epsilon_j/8,0]`. The displayed band therefore
contains every exact graph point and gives absolute admitted error at most
`15epsilon_j/16` simultaneously in all outputs. One common interpolation
weight is essential and is explicitly used.

Projection of a vector lift onto any scalar output gives a valid scalar lift
without new integers. Thus `K_j<1458*2^(p_conv)` follows from the reviewed
scalar hybrid's actual cell count, not from an independently optimized sum
of integer counts. Summing counts, rather than independently encoding output
cells, yields `K<1458m*2^(p_conv)` and hence the claimed
`p_out<=p_conv+11+ceil(log2 m)`. The compiler only declares its global index
bits integer; all gates and endpoint products are forced by them.

The proof correctly limits itself to dense input and box output error. It
does not establish that the logarithmic output-count term is necessary, and
it does not settle the separate output-independent compact-gap question.
No mathematical or bit-complexity correction is required.

Supporting exact checks in
[the shared checker](../code/quadratic_rank/check_implicit_knot_overlay.py)
passed 2,304 ordered-search comparisons (including deliberately nonmonotone
oracle values), 60 multiset order statistics, 180 source-cell containments,
eight implicit rank queries on arrays with `2^40` cells, and 99 directed-band
checks. These verify the combinatorial and band mechanisms; they do not
implement the inherited quadrature oracle.
