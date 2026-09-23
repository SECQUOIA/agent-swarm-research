# Separable convex vector graphs with arbitrary unconditional oracle budgets

Date: 2026-09-05. Status: independently reviewed result; two full proof audits passed and
a focused primary-source assessment is complete.

The [oracle-body curvature-rank construction](../results/convex-vector-oracle-curvature-rank-precision.md)
and the [reviewed shared-basis product packing](../results/convex-separable-vector-curvature-rank-precision.md)
combine for multivariate separable outputs without a finite facet description.

Let `x in [0,1]^n` and

```
F_j(x)=ell_j(x)+sum_i phi_ji(x_i),
```

where each `phi_ji` is continuous and convex and each `ell_j` is affine. Let
`K` be a compact convex unconditional error body with zero in its interior.
For each coordinate subtract the straight chord between zero and one from its
vector summand, and let `S` be the span of all remaining vectors over all
coordinates and inputs. Put `r=dim S`. In the dense polynomial case this is
the rank of all nonlinear coefficient columns from all coordinate blocks.

After removing affine-only input coordinates, for `n,r>=1` the finite comparison
is

```
p_bin<=p_conv+8n+2n ceil(log2 r).                                  (1)
```

For dense rational convex coordinate polynomials, rational affine terms, and
an unconditional body with a polynomial rational strong separation oracle and
known positive rational inner/outer radii, there is a polynomial rational MILP
construction satisfying

```
p_out<=p_conv+21n+2n ceil(log2 r).                                 (2)
```

The benchmark permits all convex general-integer lifts of the original whole
vector graph. Both bounds are independent of output count, polynomial degree,
and any facet count. Construction size and time are polynomial in the supplied
dense separable representation, oracle description, and radius encodings.
Affine-only graphs need no integers.

## 1. Reuse the same two body spanners

Choose coordinates `V` for the shared nonlinear image, and write

```
F(x)=ell(x)+V sum_i q_i(x_i).
```

The effective body, positive-polar image, and two spanners are exactly those
of the one-input oracle-rank theorem: they depend on `K` and `S`, not on the
number of input coordinates. Let `P subset S` be its inner parallelotope,
and let `lambda_1,...,lambda_r` be its selected feasible nonnegative polar
normals. Define

```
Psi=sum_s lambda_s^T F = affine+sum_i psi_i(x_i).
```

Each `psi_i` is convex. With exact maximum-volume bases, the two conclusions
are

```
||g_i||_K<=g_(psi_i),       K intersect S subset rP.                (3)
```

Here `g_i` is the vector chord gap in coordinate `i`. With the reviewed
polynomial rational spanners, the safe constants are

```
||g_i||_K<=3g_(psi_i),      K intersect S subset 3rP.               (4)
```

Both versions also give `P subset K`. These inequalities hold on every
coordinate interval because the positive-polar coefficient relations use one
shared output basis across all coordinate blocks. Every vector chord gap is
nonnegative and belongs to `S`.

If a selected `psi_i` is affine, its scalar chord gaps vanish. Equation (3)
or (4) then forces every original component summand in that coordinate to be
affine. Removing it costs no integers and preserves the nonlinear image rank.
All retained `psi_i` are therefore nonaffine.

## 2. The original-vector product packing

Use the scalar maximal-packing construction from the reviewed separable theorem.
For each coordinate and chosen local tolerance `tau`, a finite maximal set of
`P_i` points has pairwise midpoint gaps greater than `tau`, and

```
N_tau(psi_i)<=6P_i.                                               (5)
```

Ordered midpoint-gap superadditivity implies that two points of its Cartesian
product, with index vectors `u,v`, satisfy

```
J_Psi(x(u),x(v))>tau ||u-v||_1
```

when distinct. Since every selected `lambda_s` belongs to the original polar,
`J_Psi>r` forces at least one `lambda_s^T J_F>1`, and hence an inadmissible
midpoint error for the original vector graph.

The same integer-lattice estimate used in the reviewed separable theorem gives

```
#{z in Z^n: ||z||_1<=qn} < [3(2q+1)]^n
```

for every positive integer `q`. It follows by weighting with
`t=q/(q+1)` and summing the geometric series. This estimate applies also to a
truncated product grid. A greedy separated code therefore preserves at least
the full product size divided by that bound. Its existence is used only for
the lower comparison; the algorithm never enumerates the grid or code.

## 3. Finite construction

Take the exact spanners and `tau=1/(2rn)`. Deleting index balls of radius
`2nr^2` leaves pairwise inadmissible graph midpoints. The lattice-ball factor
is at most `(15r^2)^n`, so parity gives

```
2^(p_conv)>=product_i P_i/(15r^2)^n.                              (6)
```

Choose coordinate chord partitions at tolerance `tau`. Equation (5) and finite
binary encoding give index capacities at most `12P_i`. Interpolate all vector
coordinate summands at the same selected coordinate endpoints. The total
vector chord gap has `K` norm at most `sum_i tau=1/(2r)` by (3), and lies in
`S`; hence it belongs to `P/2`.

The exact vector chord center with band `P/2` contains the graph and admits
only errors in `P subset K`. This band is linear. All coordinate polylines
have finite real-coefficient encodings with only their own index bits.
Combining with (6),

```
p_bin<=p_conv+n log2(12*15r^2)
     <p_conv+8n+2n log2 r,
```

which proves (1). No rational or efficient-knot claim is made in this finite
continuous-function statement.

## 4. Compact rational construction

Use the rational factor-three spanners and `tau=1/(36rn)`. The product code
now deletes index balls of radius `36nr^2`. Their count is at most
`(219r^2)^n`, since `3(72r^2+1)<=219r^2`. Thus

```
2^(p_conv)>=product_i P_i/(219r^2)^n.                              (7)
```

The dense scalar compiler has actual count `K_i<=486N_tau(psi_i)`, so its
binary index capacity satisfies

```
2^(L_i)<=2K_i<=5832P_i.                                           (8)
```

Compile the coordinate scalar functions at that tolerance. Their total exact
scalar chord error is at most `13/(576r)`. By (4), the total vector chord gap
belongs to `(13/(192r))K intersect S subset (13/64)P`.

Write `P=V(1/r)B[-1,1]^r` as in the one-input theorem. Evaluate each coordinate
vector polynomial `q_i` at its selected scalar knots and round every entry
with error at most

```
delta=1/(16nr L_B),       L_B=1+sum_(j,k)|(B^(-1))_jk|.
```

Each coordinate rounding error belongs to `P_0/(16n)` in effective coordinates,
so their sum and interpolation error belong to `P/16` in the original output
image. Restore the affine part exactly. The resulting center `y` has

```
y-F(x) in (17/64)P.
```

The explicit rational band `w-y=VB u/(2r)`, `-1<=u<=1`, contains the exact graph
and admits error only in `(49/64)P subset K`. Each input coordinate has one
index and one continuous interpolation weight shared by all outputs.
All additional output arithmetic, image-coordinate variables, and band variables
are continuous. The spanner and scalar compiler bit bounds apply uniformly;
the extra factor `n` in tolerances and rounding costs only logarithmic precision.

Combining (7),(8),

```
p_out<=p_conv+n log2(5832*219r^2)
     <p_conv+21n+2n log2 r,
```

since `5832*219=1277208<2^21`. This proves (2). The entire construction uses the
input representation and body oracle; no optimal lift or scalar packing is
needed computationally.

## Scope and dependencies

The common nonlinear image and positive-polar basis are shared across all
coordinates. Choosing unrelated output bases per coordinate would not justify
the same original-vector packing comparison. Separability and componentwise
convexity are retained; no mixed-coordinate nonlinear terms are claimed.

The result is the body transfer with an inner band in the nonlinear image.
The spanner oracle, scalar compiler, and product-code estimate are reviewed
supporting ingredients. Two independent full audits passed. The bounded source
assessment found no matching combined theorem in the checked literature; it
does not establish unrestricted publication priority.

The [exact checker](../code/quadratic_rank/check_separable_oracle_rank_precision.py)
passes 96 integer-lattice ball bounds and 1,536 coupled separable rounding/band
checks. The latter use a rank-two, three-output example with up to eight input
coordinates. They supplement the geometric proof and do not implement the
inherited convex-body or quadrature oracles.


* [First full proof audit](../notes/review-convex-separable-vector-oracle-curvature-rank-precision.md).
* [Second full proof audit](../notes/review-convex-separable-vector-oracle-curvature-rank-precision-second.md).
* [Focused source assessment](../notes/convex-separable-vector-oracle-curvature-rank-novelty.md).

The arbitrary-body oracle interface is broader than an explicit-facet input;
the explicit-facet theorem can have a smaller integer bound when that
representation is available. Separable interpolation error composition is
classical and is credited in the source assessment, alongside the inherited
spanner, packing, and scalar compilation tools.
