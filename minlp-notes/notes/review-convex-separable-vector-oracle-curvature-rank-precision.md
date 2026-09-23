# Independent audit: separable convex outputs with an oracle error body

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`. Status: **PASS** for the complete [candidate extension](convex-separable-vector-oracle-curvature-rank-precision.md). This report verifies the mathematical transfer and its constants. The rational body-spanner algorithm is an explicitly imported, independently audited dependency of the [promoted one-input theorem](../results/convex-vector-oracle-curvature-rank-precision.md); this report does not repeat its oracle implementation audit or make a priority claim.

## Common image and scalarization

The nonlinear image must span every coordinate summand after subtracting its affine chord. The candidate uses exactly this joint image. A basis `V` and left inverse therefore represent all coordinate summands with the same output coordinates. Each positive-polar spanner relation is a relation in this common image and hence holds on every coordinate chord gap. There is no assumption that any single coordinate spans the entire image.

All selected polar normals are feasible for the original body and nonnegative. Thus their scalarizations and coordinate summands are convex. Exact spanner coefficient bound one gives `||g_i||_K<=g_(psi_i)`; the rational spanner bound three gives `||g_i||_K<=3g_(psi_i)`. The nonnegativity of the original chord vector permits the positive-polar norm formula, and the selected scalar gaps are nonnegative even when their representation coefficients have mixed signs. These are precisely the hypotheses needed by the inherited rank argument.

A selected coordinate scalar sum can be affine only if every original component summand there is affine, by either norm bound. Removing such coordinates preserves the common nonlinear image. The rank-zero case is the exact affine graph.

## Packing against the correct minimum

For each retained coordinate, the reviewed maximal midpoint packing at local tolerance `tau` has size `P_i` and satisfies `N_tau<=6P_i`. Ordered midpoint superadditivity makes the selected scalar sum's gap exceed `tau ||u-v||_1` for distinct product indices. A value greater than `r` forces one selected feasible polar normal to have original vector midpoint error greater than one. This compares to the original vector graph's unrestricted convex-lift integer minimum, not to the scalar surrogate's minimum.

For positive integer `q`, weighting the lattice sum with `t=q/(q+1)` bounds the ball of radius `qn` by `[3(2q+1)]^n`. With finite tolerance `1/(2rn)`, choose `q=2r^2`, obtaining the factor `(15r^2)^n`. With compact tolerance `1/(36rn)`, choose `q=36r^2`, obtaining `(219r^2)^n`. All thresholds are integers. Greedy deletion in a truncated product grid obeys the same bounds. Same-parity contacts in any convex general-integer lift have an integer midpoint, regardless of lift size, integer range, or other continuous coordinates. This gives both displayed lower comparisons.

## Finite representation

Exact body spanners give `K intersect S subset rP` and `P subset K`. The summed coordinate chord error is in `(1/(2r))K intersect S`, hence in `P/2`. The exact chord center with the symmetric `P/2` band contains the graph and admits errors only in `P`. A finite disjunction for each coordinate encodes all its component chords at common endpoints and a common interpolation weight. There are no products of interpolation weights from different coordinates. Its binary capacity is at most `12P_i`. The factor `12*15=180<256` proves the finite overhead `8n+2n ceil(log2 r)`.

The statement correctly permits real coefficients and nonconstructive finite knots for arbitrary continuous convex inputs. It does not make a polynomial algorithm claim for that representation class.

## Rational representation and error budget

The total scalar chord error is `13/(576r)`; multiplying by the polar factor three and the body factor `3r` puts the original vector gap in `(13/64)P`. Rounding each effective-coordinate polynomial endpoint with error at most `1/(16nr L_B)` gives effective error in `P_0/(16n)`. Convex interpolation preserves this membership, and summing over the `n` coordinates gives original output rounding error in `P/16`. The affine part is restored exactly. Central symmetry and Minkowski addition therefore give center error in `(17/64)P`.

The explicit half-parallelotope band contains the graph since `17/64<1/2`, and every admitted error is in `(49/64)P subset K`. This is a single simultaneous vector band with shared coordinate interpolation weights. All image and band variables are continuous.

The scalar circuit capacity bound is `5832P_i`, including a one-cell construction. Together with the lattice estimate it yields `5832*219=1277208<2^21`, proving the stated compact overhead. The common rational basis, its inverse, all affine-coordinate transformations, and the oracle-produced body spanners have polynomial encoding by the imported theorem. The factor `n` in local tolerances and rounding adds only logarithmic precision. Polynomial evaluations of the possibly nonconvex effective-coordinate functions are used only for endpoint arithmetic; they are not incorrectly passed to the convex scalar compiler. The actual compiler inputs `psi_i` are convex.

No correction is required. The scope excludes mixed multivariate nonlinear terms and keeps the body unconditional, exactly where the proof needs these assumptions.
