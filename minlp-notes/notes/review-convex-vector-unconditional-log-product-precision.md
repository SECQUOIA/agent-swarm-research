# Independent audit of unconditional convex-vector graph precision

Date: 2026-09-05. Reviewer: `quadratic_weighted_precision`.
Status: PASS after full independent inspection of
[the candidate](convex-vector-unconditional-log-product-precision.md).

The exact maximum-product point exists in the nonnegative part of the compact
body and is positive because an interior ball supplies positive feasible
points. Convexity and coordinate-sign invariance put its whole coordinate box
inside the body. Differentiating the feasible segment toward any nonnegative
body point gives the stated supporting inequality `sum v_i/b_i<=m`.
The parity midpoint vector is nonnegative because every component is convex;
it belongs to the closed error body by the projected midpoint limit argument.
Thus the selected scalar sum has midpoint gap at most `m`, and full gap at
most `2m`. The level-cut refinement and common chord bands prove the finite
`ceil(log2(4m-1))` overhead without a closure assumption on the lift.

The approximate-product functional estimate is valid. Write `s=1-1/m`.
For `m>=2`, all discarded product-expansion terms are nonnegative, and
`s^(m-1)>=exp(-1)`. The near-optimal product guarantee bounds the product
ratio by `exp(1)`, giving
`sum v_i/b_i<=m(exp(2)-1)+1<7m`. For `m=1`, the direct scalar ratio bound
is less than `exp(1)<7`, as separately stated. No approximate gradient or
unproved optimality certificate is substituted for the product guarantee.

The rational oracle import fits the reviewed log-product solver exactly.
Use the variables `p=b/R`, the nonnegative matrix `C=R I`, the original body,
and cap `p<=1`. The outer coordinate bound makes that cap redundant for
positive body points. The known inner Euclidean ball provides a strictly
positive feasible vector of polynomial bit length. The returned loss at
most one in log product transfers unchanged when multiplying coordinates
by `R`. Rational output encoding and positivity imply polynomial bit lengths
for all reciprocals `1/b_i`; no inverse condition number appears as a numerical
iteration count. A Euclidean outer radius, if the imported oracle interface
needs one, follows from the given coordinate radius by the rational bound
`mR`. All calls remain within the stated strong-separation model.

The scalarized dense polynomial is convex and nonaffine if any component is
nonaffine: its second derivative is a positive weighted sum of nonnegative
second derivatives. The factor `7m` gives full gap `14m` per parity hull and
at most `28m-1` refined intervals. The inherited actual scalar cell count is
therefore less than `486*28m*2^p=13608m*2^p`, which gives the compact
`14+ceil(log2 m)` overhead.

Every component normalized by `b_i` has nonnegative chord gap bounded by that
of the scalar sum. Downward endpoint error at most `1/8` and the displayed
bands give absolute normalized error at most `15/16`. The same interpolation
weight admits all exact output values simultaneously. The resulting coordinate
error box lies in the original unconditional body, so the final MILP requires
neither facets of that body nor an oracle constraint. All additional arithmetic,
gate variables, and products are continuous once the single index is fixed.

The finite statement permits real coefficients; the compact statement requires
dense rational polynomial data and a polynomial strong-separation oracle with
known rational radii. The proof retains this distinction. No mathematical or
bit-complexity correction is required.
