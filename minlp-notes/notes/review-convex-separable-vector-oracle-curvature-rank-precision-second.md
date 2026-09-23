# Second audit of the separable oracle-body curvature-rank extension

Date: 2026-09-05. Reviewer: `binary_formulation_review`. Verdict: PASS on
[the full companion](convex-separable-vector-oracle-curvature-rank-precision.md).

The reviewed one-input oracle-body theorem, its separately audited rational
spanner lemma, the scalar compiler, and the promoted shared-basis packing
result are explicit dependencies. This audit checks their multivariate
combination, every count constant, and the accumulated output error.

## Shared image and scalarization

The span of all coordinate deviations is exactly the space needed for a
single rational image matrix `V`. The positive-polar representation coefficients
therefore work on each coordinate block with the same values. Since original
coordinate summands are convex, every coordinate vector gap is nonnegative.
The imported positive-polar argument gives the coordinate inequalities (3)
or (4) without selecting unrelated scalarizations for different coordinates.

If a coordinate sum `psi_i` is affine, the gauge domination forces every
component's chord gaps in that coordinate to vanish. Removing that coordinate
from the integer construction is valid; its remaining dependence is affine.
The rank-zero and affine-only branches are consistent.

## Product packing against the original vector lift

The scalar maximal midpoint packing gives `N_tau<=6P_i`, as in the linked
reviewed theorem. For ordered selected points, Jensen superadditivity across
adjacent subintervals makes an index separation of `h` yield a gap strictly
greater than `h tau`. Separability adds these coordinate gaps exactly, so
the product-grid lower inequality applies to the shared scalarization.

If its midpoint gap exceeds `r`, one of the `r` selected feasible positive
polar normals pairs with the original vector Jensen gap above one. This is
an error outside the original body, not just outside a separately chosen
scalar tolerance. Thus the parity lower comparison uses the original vector
integer minimum correctly.

For local tolerance `1/(2rn)`, the conservative deleted index-ball radius is
`2nr^2`; substituting `q=2r^2` in the exact geometric-series lattice bound
gives fewer than `(15r^2)^n` points. For tolerance `1/(36rn)`, substitute
`q=36r^2` to obtain fewer than `(219r^2)^n`. Both `q` values are positive
integers. Truncating to the finite product grid cannot increase a deleted
ball size. Greedy selection and parity therefore give both displayed product
packing inequalities, including when some scalar packing has only one point.

## Finite formulation and count

A scalar chord partition has at most `6P_i` cells; binary rounding of its
index count uses capacity at most `12P_i`. The finite exact-spanner coordinate
gauge bounds add to at most `1/(2r)`. The total vector gap belongs to the
shared image, and the effective body's outer dilation therefore puts it in
`P/2`. Centering a symmetric `P/2` band at the vector chord contains the
whole graph and admits errors only in `P subset K`.

Multiplying the coordinate capacities and using the product packing gives
overhead `n log2(180r^2)<8n+2n log2 r`. The stated integer upper bound with
`ceil(log2 r)` is consequently valid. Finite real-coordinate polyline and
band encodings require no additional discrete output selectors.

## Rational construction and accumulated error

The scalar compiler's capacity estimate is exactly
`2^L_i<=2K_i<=972N_tau<=5832P_i`. Summing its coordinate exact chord errors
at tolerance `1/(36rn)` gives `13/(576r)`. The factor-three scalarization
bound, followed by the effective-body factor `3r`, gives total vector gap
in `13P/64`.

The rounding depth `1/(16nrL_B)` bounds each effective coordinate error in
`P_0/(16n)`. Each interpolation error remains in that body by convexity;
adding the `n` errors gives `P_0/16`, or `P/16` in original outputs.
Thus the rounded center differs from the graph by a vector in `17P/64`.
The symmetric `P/2` band contains the exact graph and admits only `49P/64`
error. Keeping all rounding in the shared nonlinear image is essential and
is explicitly done.

Each input coordinate has its own interpolation weight, consistently shared
by every output summand depending on that input. Summing coordinate polynomial
interpolants is exact for the assumed separable representation; no mixed-input
product is left unmodeled. Affine terms are restored exactly. Additional
output arithmetic, coordinate variables, and band variables are continuous.
The extra factors `n` in tolerances add only logarithmic numerical precision
to the already polynomial oracle and scalar-compiler encoding bounds.

Finally, `5832*219=1277208<2^21`. The capacity product and original-vector
packing inequality yield the claimed
`p_out<=p_conv+21n+2n ceil(log2 r)`. No correction was required. The theorem
does not extend to mixed-coordinate nonlinear terms or claim that its rank
overhead is necessary, and these scope limits are correctly stated.
