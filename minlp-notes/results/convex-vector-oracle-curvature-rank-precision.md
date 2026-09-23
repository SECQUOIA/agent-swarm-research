# Oracle error bodies: convex vector graph precision controlled by curvature rank

Date: 2026-09-05. Status: independently reviewed result. Full proof and oracle audits passed;
a focused primary-source assessment is complete.

Let `F:[0,1]->R^m` be continuous and componentwise convex. Let `K` be a compact
convex unconditional body with zero in its interior. Define the nonlinear
output image

```
S=span{F(x)-(1-x)F(0)-xF(1): 0<=x<=1},        r=dim S.
```

For polynomials, `S` is the span of the coefficient columns of degrees at least
two; its dimension is the usual curvature rank. Let `p_conv` compare with every
convex lift containing the entire vector graph and admitting only errors in
`K`, with general integers and unrestricted continuous size.

If `r=0`, the exact graph is affine and needs no integers. For `r>=1`, the
finite real-coefficient comparison is

```
p_bin<=p_conv+ceil(log2(8r^2-1)).                                  (1)
```

For densely encoded rational polynomial outputs, suppose `K` has a rational
strong separation oracle with polynomial query/output complexity and known
positive rational bounds

```
rho B_2^m subset K subset R B_infinity^m.
```

There is a polynomial-time rational MILP construction satisfying

```
p_out<=p_conv+17+2ceil(log2 r).                                    (2)
```

The final MILP has no oracle constraints and does not need a polyhedral
representation of `K`. Its error band is an explicit rational parallelotope
inside the effective error body. Complexity includes the total dense input,
oracle description, and radius encodings. Neither output dimension, polynomial
degree, nor an unknown facet count occurs in the additive bound.

## 1. Effective output coordinates and body geometry

Choose a full-column-rank matrix `V` spanning `S`. Write

```
F(x)=a+bx+V q(x),            a=F(0), b=F(1)-F(0).
```

The coordinate functions `q_i` are independent modulo affine functions:
`q(0)=q(1)=0`, and their values span `R^r` by the definition of `S`.
For dense rational polynomials choose independent nonlinear coefficient columns
for rational `V`, and compute the rational left inverse
`L=(V^T V)^(-1)V^T`. Then `q=L(F-a-bx)` is a dense rational polynomial vector
of polynomial encoding length.

Put `C={z in R^r: Vz in K}`. This is a centrally symmetric compact convex body
with interior. It need not be unconditional in these coordinates. With rational
bounds

```
C_V=1+sum_(i,j)|V_ij|,
C_L=1+sum_(i,j)|L_ij|,
```

it has known radii

```
(rho/C_V) B_2^r subset C subset (m R C_L) B_2^r.                    (3)
```

A strong separator for `K` pulls back by `V^T` to a strong separator for `C`.
If the query is outside `C`, the pulled-back normal cannot vanish, since zero
belongs to `C`. All maps, normals, and radius values have polynomial bit length.

## 2. Positive polar scalarizations

Let

```
P_+={lambda>=0: h_K(lambda)<=1},
T={V^T lambda: lambda in P_+} subset R^r.
```

The body `P_+` is compact, convex, and has nonempty interior in `R^m`.
The set `T` spans `R^r`, because sufficiently small positive coordinate-axis
vectors belong to `P_+` and the rows of `V` span `R^r`.

For each feasible `lambda`, the scalar function `H_lambda=lambda^T F` is convex.
Its nonlinear coefficient row in coordinates `q` is `V^T lambda`. If a basis
of `r` projected points represents every point of `T` with coefficients of
magnitude at most `c`, choose their feasible preimages `lambda_s` and put

```
Psi=sum_(s=1)^r lambda_s^T F.
```

All selected functions are original convex positive scalarizations. For `r>0`,
`Psi` is nonaffine: if its sum were affine, nonnegativity of the summands'
chord gaps would force every summand affine, contradicting their projected
linear independence. For every
input interval their nonnegative chord gaps imply

```
0<=g_(H_lambda)<=c g_Psi,       lambda in P_+.                      (4)
```

Indeed the projected coefficient relation leaves only an affine function,
which has zero chord gap. Signed basis coefficients are harmless because the
selected scalar chord gaps are nonnegative.

For any nonnegative vector `e`, unconditionality gives the polar identity

```
||e||_K=sup_(lambda in P_+) lambda^T e.                             (5)
```

The polar of an unconditional body is unconditional; replacing a polar normal
by its coordinatewise absolute value cannot decrease its pairing with `e`.
Thus, for the nonnegative vector chord gap `e=T_F-F`, (4) implies

```
||e||_K<=c g_Psi.                                                 (6)
```

This argument uses the whole positive polar, not an assumed finite facet list.

## 3. A parallelotope band in the nonlinear image

Choose `r` independent points of `C` as the columns of a matrix `B`. Suppose
every point of `C` has coefficients in this basis of magnitude at most `d`.
Then

```
B {u: ||u||_1<=1} subset C subset B[-d,d]^r.
```

The first inclusion follows from central symmetry and convexity, since all
columns and their negatives lie in `C`. Define

```
P_0=(1/r) B[-1,1]^r,      P=V P_0 subset S.
```

Consequently,

```
P subset K intersect S subset dr P.                               (7)
```

The band `w-y in P/2` is explicitly linear: set
`w-y=V B u/(2r)` with continuous `-1<=u_i<=1`. It adds no integers.

## 4. The finite comparison

Choose maximum-absolute-determinant bases in the compact spanning sets `T`
and `C`. Cramer's rule gives coefficients bounded by one for both, so `c=d=1`
in (6),(7). These finite bases may be real and need not be computed.

Take an admissible `p`-integer lift and the interval hull of each parity class
of exact graph contacts. The projected midpoint error belongs to `K`, by
continuity and closedness of the error body. For each selected feasible polar
normal, its midpoint gap is at most one. Hence `Psi` has midpoint gap at most
`r` and full chord gap at most `2r` on that hull.

The reviewed direct level-cut lemma refines such an interval to scalar chord
error at most `1/(2r)` using at most `8r^2-1` subintervals. By (6),(7), the
vector chord gap on each subinterval belongs to `P/2`. The exact chord center
therefore admits the exact vector graph through the symmetric band `P/2`, and
every admitted error lies in `P subset K`.

These bands are finite polyhedra, despite a possibly nonpolyhedral original
body. There are at most `(8r^2-1)2^p` bands. A finite binary disjunction proves
(1). Arbitrary lift errors outside `S` cause no difficulty: the midpoint
Jensen vectors used in the lower comparison automatically belong to `S`.

## 5. Rational bases from the oracle

The [fixed-grid barycentric-spanner lemma](../notes/rational-polar-spanner-oracle.md)
supplies the constructive replacement for the two maximum-volume bases. It
provides:

* Feasible rational `lambda_1,...,lambda_r` in `P_+` whose projected points span
  `R^r` and represent every projected point with coefficient magnitudes at most
  three.
* Feasible rational columns of `B` in `C` whose coefficient bound is at most
  three.
* Polynomially bounded output encoding, iteration count, and construction time
  in the original data, radii, and rank, with no accumulating precision growth.

For the supporting lemma's Euclidean outer-radius convention, replace the
given coordinate radius by the rational Euclidean bound `mR`. The effective
body `C` has the strong separator and radii in (3). The positive
polar is accessed through a weak separation oracle derived from support
optimization over `K`; approximate support values alone are not treated as
exact membership tests. Feasible polar optimization and the spanner selection
must use the supporting lemma's exact rational repair and fixed denominator.

Spanning seeds are explicit. For `C`, sufficiently small coordinate-axis
vectors from its inner ball suffice. For `P_+`, sufficiently small coordinate
vectors whose corresponding rows of `V` are independent have feasible projected
images spanning `R^r`. Uniform determinant and radius bounds control all inverse
basis norms. Fixed-grid rounding and central-ball repair prevent iterative
oracle output denominators from growing beyond a uniform polynomial bound.

The lemma therefore makes equations (6),(7) hold with `c=d=3`, giving

```
||e||_K<=3g_Psi,       K intersect S subset 3r P.                   (8)
```

## 6. Compile the scalar grid and a rational inner band

Set `tau=1/(36r)` and apply the reviewed dense convex scalar compiler to `Psi`.
Each original parity hull still has scalar full gap at most `2r`, so direct
level refinement and the cover-to-partition argument give

```
N_tau(Psi)<=(144r^2-1)2^p.
```

The scalar compiler has actual cell count at most `486N_tau` and exact chord
gap at most `13tau/16`. Combining with (8), each vector chord gap belongs to

```
(13/(192r))K intersect S subset (13/64)P.                          (9)
```

Evaluate the coordinate polynomials `q` at the two rational scalar knots and
round them with coordinate error at most

```
delta=1/(16r L_B),       L_B=1+sum_(i,j)|(B^(-1))_ij|.
```

Then each coordinate rounding error belongs to `P_0/16`, since its image under
`B^(-1)` has infinity norm at most `1/(16r)`. Interpolation preserves this
membership. Let `y=a+bx+V y_q`, where `y_q` interpolates the rounded coordinate
values and the affine part is restored exactly. By (9),

```
y-F(x) in (17/64)P.
```

Use the explicit band `w-y in P/2`. It contains every exact graph point and
admits only errors in `(49/64)P subset K`. All outputs share the scalar input
index and interpolation weight. Rounding coordinate functions rather than
arbitrary original output coordinates keeps the error exactly in `S`.

The scalar knot circuit, rational coordinate evaluations, fixed output offsets,
and the band equation use polynomially many continuous variables and rows.
Only its global index is declared binary. The rational spanner guarantee bounds
`B^(-1)`, all coordinate coefficients, and all precision lengths polynomially.
The count is

```
K_cells<=486(144r^2-1)2^p<69984r^2 2^p<131072r^2 2^p.
```

Therefore

```
ceil(log2 K_cells)<=p+17+2ceil(log2 r),
```

proving (2) with the stated rational spanner primitive. The algorithm
uses only input data and oracle calls; it does not know the comparator lift or
its optimal integer count.

## Scope

This replaces output-dimension or explicit-facet dependence by curvature rank
for arbitrary unconditional strong-oracle budgets. The proof retains one input
and componentwise convexity. Its final band is a rational parallelotope in the
nonlinear image, so no nonpolyhedral error constraint remains in the MILP.

Componentwise convexity cannot simply be removed: the
[nonconvex polynomial family](../results/polynomial-graph-binary-integer-degree-gap.md)
has one output, hence nonlinear-image rank one, while its binary-versus-general-
integer gap grows without bound at fixed error tolerance.

Maximum-volume bases, approximate barycentric spanners, positive-polar duality,
inner crosspolytopes, convex-body optimization, and circuit compilation are
established tools. The proposed new conclusion is their whole-formulation
rank-dependent comparison and uniform rational construction. Both the oracle lemma and this transfer have passed independent full proof
audits. The bounded source assessment found no matching complete theorem in
the checked literature; it does not establish unrestricted publication priority.

## Reproducible supporting checks

The [exact rational band checker](../code/quadratic_rank/check_oracle_curvature_rank_bands.py)
uses a rank-two, three-output convex polynomial graph with a nontrivial
nonlinear image. It passes 289 inner-parallelotope checks, 576 vector-chord
comparisons, and 9,216 admissible band-error checks. It tests the geometric
transfer and shared-coordinate band; it does not implement or certify the
black-box GLS optimization theorem or the full spanner construction.


Independent proof reports:

* [First main-transfer audit](../notes/review-convex-vector-oracle-curvature-rank-precision.md),
  whose author also wrote the oracle dependency and explicitly records that distinction.
* [Second main audit](../notes/review-convex-vector-oracle-curvature-rank-precision-second.md).
* [Third main audit](../notes/review-convex-vector-oracle-curvature-rank-precision-third.md).
* [First independent oracle audit](../notes/review-rational-polar-spanner-oracle.md).
* [Second independent oracle audit](../notes/review-rational-polar-spanner-oracle-second.md).

All reports passed. The separate independent oracle checks are essential to the
complete construction; the main author's and oracle author's reciprocal reviews
alone are not used as the only evidence.


The [focused source assessment](../notes/convex-vector-oracle-curvature-rank-novelty.md)
credits Awerbuch--Kleinberg's barycentric spanners, GLS's polar and nonnegative
anti-blocker oracle equivalences, and approximate-optimization spanner
constructions such as [Plevrakis--Hazan, Section 3.2](https://arxiv.org/abs/2010.13178).
These are established supporting methods. The result here concerns the complete
rank-dependent graph-formulation comparison and its rational implementation.


The [separable oracle-body theorem](convex-separable-vector-oracle-curvature-rank-precision.md)
combines the shared-coordinate packing with an explicit inner band in the
nonlinear output image. It handles unconditional bodies given by strong
separation, with compact overhead `21n+2nceil(log2 r)`.
