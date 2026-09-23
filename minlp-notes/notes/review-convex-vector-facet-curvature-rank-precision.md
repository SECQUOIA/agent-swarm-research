# Independent audit of facet-curvature-rank precision

Date: 2026-09-05. Reviewer: `quadratic_weighted_precision`.
Status: PASS after full independent reads of
[the facet extension](convex-vector-facet-curvature-rank-precision.md)
and its [box-rank dependency](convex-vector-curvature-rank-precision.md).

The rank is correctly taken for the normalized facet functions, modulo affine
terms. Nonnegative facet coefficients preserve convexity. Compactness of the
error body implies every output column has a positive coefficient somewhere,
so rank zero forces all component chord gaps, and hence all nonlinear parts,
to vanish. This verifies the exact affine exception.

For the finite result, a maximum-determinant basis of original facet functions
has coefficient magnitudes at most one by a row-replacement determinant
identity. Original convex basis functions have nonnegative chord gaps, so
signed representation coefficients still give the displayed dominance by their
positive sum. The parity midpoint vector belongs to the body, and its normalized
facet gaps are at most one. Therefore the selected scalar sum has midpoint gap
at most `r` and full gap at most `2r`. The direct level refinement to tolerance
`1/2` gives exactly the stated `8r-1` factor. All component gap vectors on the
refined intervals lie in `K/2`; the symmetric half-body band contains the graph
and admits only error in `K`. This proves the finite count without confusing a
coupled body with independent downward component bands.

I checked the polynomial basis computation in the dependency. Choosing
independent columns preserves all row relations. Every row exchange with a
coefficient larger than two doubles a determinant of an original row minor.
The nonzero lower bound and upper bound on those rational minors have polynomial
bit length, so the number of exchanges is polynomial even at variable rank.
Every intermediate basis is an original submatrix, preventing accumulating
coefficient growth. Its inverse and all exact comparisons have polynomial
encoding. This is a valid polynomial 2-barycentric-spanner computation.

The resulting factor-two chord dominance, scalar tolerance `1/4`, and level
refinement give `N_(1/4)<= (16r-1)2^p`. The scalar compiler's actual count
`486N` and chord bound `13/64` imply the vector chord belongs to `(13/32)K`.
The chosen rational rounding precision
`rho=min(1,1/(16 max_k sum_j A_kj/b_k))`
places each coordinate rounding vector in `K/16`, including the case where
the minimum is attained at one. Its encoding is polynomial in the rational
input. Interpolation preserves that bound, so the rounded center differs from
the exact graph by a vector in `(15/32)K`.

The band `w-y in K/2` consequently contains the exact graph and admits only
error in `(31/32)K`. The explicit absolute-value auxiliary formulation is
exact: nonnegative `A` gives one implication from `s>=|w-y|`, and choosing
`s=|w-y|` gives the reverse. These variables are continuous. The common index
and interpolation weight are retained across all outputs, so containment is
simultaneous, not merely coordinatewise existential.

The cell count is less than `7776r*2^p<8192r*2^p`, giving the claimed
`13+ceil(log2 r)` binary overhead. Dense endpoint polynomial evaluation,
rational output offsets, row sums, and the extra band rows have polynomial
encoding. No maximum-volume oracle, comparator lift, facet enumeration beyond
the input description, or extra integer product variables are needed.

Finally, the weighted-l1 specialization has one nonaffine normalized facet
function whenever any convex component is nonaffine. Its rank is exactly one,
so the finite `+3` and polynomial `+13` bounds follow independently of the
number and degrees of the output components. The stated one-input,
componentwise-convex and nonnegative-facet scope is essential and is preserved.
No mathematical or bit-complexity correction is required.
