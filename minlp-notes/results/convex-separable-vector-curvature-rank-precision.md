# Coupled separable convex outputs: a compact near-minimum integer formulation

Date: 2026-09-05. Status: verified result with two independent full proof audits and a qualified source assessment. Author: `noncommutative_rank_review`. Dependencies are the reviewed [scalar polynomial compiler](convex-polynomial-compiled-integer-precision.md), [separable packing theorem](separable-convex-graph-linear-dimension-precision.md), and [output curvature-rank basis theorem](convex-vector-curvature-rank-precision.md).

## 1. Main statement for box error

Let `x in [0,1]^n` and let

```
F_j(x)=ell_j(x)+sum_(i=1)^n phi_ji(x_i),   j=1,...,m,
```

where each `ell_j` is rational affine and each `phi_ji` is a densely encoded rational univariate polynomial convex on `[0,1]`. Every component may depend on every input coordinate. Positive rational component tolerances are `epsilon_j`.

Normalize by `epsilon_j` and form one coefficient row for each output by concatenating all coefficients of degrees at least two in all its coordinate summands. Let `r` be the rank of this single matrix. This is rank in the direct sum of the coordinate function spaces modulo affine functions. It is not a sum of independently selected coordinate ranks.

After removing affine-only input coordinates, suppose `n,r>=1`. There is a deterministic polynomial-time rational MILP construction containing the exact vector graph, with component errors at most `epsilon_j`, whose declared integer count satisfies

```
p_out <= p_conv+n ceil(log2 r)+17n.                       (1)
```

Here `p_conv` minimizes integer dimension over every admissible convex lift, with unrestricted general integers and continuous size. All dimensions, degrees, and output counts may grow; the running time and encoding length are polynomial in the supplied dense separated polynomial representation and tolerance encodings. If `r=0`, the graph is affine and needs no integers.

## 2. One shared basis across all coordinate curvatures

Use the polynomial 2-approximate barycentric-spanner construction from the output-rank theorem on the concatenated rows. It selects original normalized outputs `G_(j_1),...,G_(j_r)`, where `G_j=F_j/epsilon_j`, such that

```
G_j = affine_j + sum_s c_js G_(j_s),   |c_js|<=2.
```

The same coefficients work in every coordinate. Define

```
Psi=sum_s G_(j_s)=affine+sum_i psi_i(x_i),
psi_i=sum_s phi_(j_s,i)/epsilon_(j_s).
```

Every `psi_i` is convex. On any univariate interval in coordinate `i`, let `g_ji` and `g_(psi_i)` be the corresponding normalized summand chord gaps. Affine parts cancel and all original summand gaps are nonnegative, so

```
0<=g_ji<=2g_(psi_i).                                    (2)
```

If `psi_i` is affine, (2) forces every output summand in that coordinate to be affine. These coordinates can therefore be removed from the integer construction. From now on `n` counts the remaining active coordinates.

## 3. A scalar packing at the finer local tolerance

Set `tau=1/(2n)`. For each active coordinate, let `P_i` be the size of a finite maximal set of pairwise midpoint-incompatible points for `psi_i` at tolerance `tau`:

```
J_(psi_i)(a,b)>tau    for every distinct selected pair.
```

Such a finite maximal set exists by uniform continuity and is used only for the lower-bound argument. The reviewed scalar packing proof gives

```
N_tau(psi_i)<=6P_i.
```

For clarity, a maximal set has compatibility intervals covering the domain; splitting each interval at its selected point yields at most `2P_i` intervals of chord error at most `2tau`, and the three-piece scalar refinement gives the displayed bound.

The dense scalar compiler has actual cell count `K_i<=486N_tau(psi_i)`. Its binary index capacity therefore obeys

```
2^(L_i)<=2K_i<=5832P_i,   L_i=ceil(log2 K_i).              (3)
```

This holds also when `K_i=1`. The compiler applies to signed polynomial coefficients because only convexity is required by the reviewed result.

## 4. Product packing against the original vector lift

Order every scalar packing set. Midpoint Jensen gaps of a continuous convex function are superadditive across consecutive subintervals. Hence an index separation of `h>0` in coordinate `i` gives midpoint gap strictly greater than `h*tau`.

For two distinct points in the product grid with index vectors `u,v`,

```
J_Psi(x(u),x(v))>tau ||u-v||_1.
```

If `||u-v||_1>2nr`, this gap exceeds `r`. Since `Psi` is the sum of `r` original normalized outputs, at least one of those outputs then has midpoint gap greater than one. Thus the two vector graph points are incompatible in the original error box. This comparison uses the original vector lift, not an independently optimized scalar lift at a different tolerance.

Select a separated product subcollection greedily, deleting after each choice all grid indices within l1 distance `2nr`. Its size is at least the full product size divided by the corresponding integer lattice-ball count.

Here is an explicit bound. For positive integers `a,r,n`, put `t=ar/(ar+1)`. Then

```
#{z in Z^n: ||z||_1<=anr}
<=t^(-anr) (sum_(k in Z)t^|k|)^n
=(1+1/(ar))^(anr) (2ar+1)^n
< [3(2a+1)r]^n.                                        (4)
```

The first inequality bounds the indicator by `t^(||z||_1-anr)` and sums the geometric series. The last uses `(1+1/q)^q<3` for a positive integer `q`, and `2ar+1<=(2a+1)r`. Taking `a=2` bounds the deleted ball by `(15r)^n`.

The separated subcollection therefore has at least `product_i P_i/(15r)^n` points. Any two have an inadmissible graph midpoint. The parity principle for an arbitrary convex lift gives

```
2^(p_conv)>=product_i P_i/(15r)^n.                      (5)
```

No enumeration of this product or code is part of the construction.

## 5. Shared coordinate grids and simultaneous graph containment

Compile every `psi_i` at tolerance `tau=1/(2n)`. Its exact chord error is at most `13/(32n)` on each compiled cell. Evaluate every normalized original summand `phi_ji/epsilon_j` at those same two coordinate knots, with downward rounding error at most `1/(8n)` per endpoint.

Let `T_ji` be its exact chord, and let `y_ji` interpolate its rounded values using the same coordinate interpolation weight as all other outputs. For an arbitrary combination of selected coordinate cells, put

```
T_j=ell_j/epsilon_j+sum_i T_ji,
y_j=ell_j/epsilon_j+sum_i y_ji.
```

Separation across input coordinates makes these sums affine in the continuous interpolation variables after the index bits have fixed the knots. By (2),

```
0<=T_j-G_j<=sum_i 2g_(psi_i)<=13/16,
0<=T_j-y_j<=1/8.
```

Impose the shared vector band

```
y_j-13/16<=w_j<=y_j+1/8   for all j,
```

and rescale output `j` by `epsilon_j`. The exact graph is contained, and every admitted component error is at most `15epsilon_j/16`. Every output uses the same coordinate input and interpolation weight, so independently compatible scalar pieces are not incorrectly combined at different input points.

Only the `L_i` input index bits per coordinate are declared integer. All additional original-output evaluations, Boolean circuit wires, and binary-times-continuous products use the reviewed scalar compilation mechanism. The number of outputs and coordinates increases formulation size polynomially without adding selector bits for each output.

Combining (3) and (5) gives

```
p_out=sum_i L_i
<=p_conv+n log2(5832*15r)
<p_conv+n log2 r+17n,
```

because `5832*15=87480<2^17`. This implies (1). The input normalization, concatenated rational basis, polynomial evaluations, local tolerances, and rounding precisions all have polynomial encoding length. The construction never requires `P_i`, the separated code, or the unknown optimal lift.

## 6. Coupled unconditional error bodies

The same proof has a useful extension. Let

```
K={e:A|e|<=b},   A>=0, b>0, K compact,
```

with rational data. Form convex facet functions `H_k=(AF)_k/b_k` and let `r` be their concatenated curvature rank across all input coordinates. The polynomial construction obeys

```
p_out<=p_conv+n ceil(log2 r)+18n.                       (6)
```

Use a shared 2-approximate barycentric spanner of the facet functions and their separable sum `Psi`. Compile its active coordinate summands at `tau=1/(4n)`. The product-packing threshold is now `4nr`; (4) with `a=4` bounds its lattice ball by `(27r)^n`. Equation (3) still holds at this new local tolerance, so the count factor is `5832*27r=157464r<2^18 r` per active coordinate.

For every facet, its coordinate chord gaps sum to at most `13/32`, as in the reviewed [single-input facet-rank construction](convex-vector-facet-curvature-rank-precision.md). Round each original coordinate summand's endpoints with absolute error at most `min(1,1/(16nM_A))`, where `M_A=max_k sum_j A_kj/b_k`. Summing over the `n` coordinates puts the total rounding vector in `K/16`. Hence the rounded center differs from the true vector graph by an element of `(15/32)K`. The band `w-y in K/2` contains the exact graph and admits only errors in `(31/32)K`.

The half-body band is encoded with continuous absolute-value auxiliaries, exactly as in the single-input result. Compactness and nonnegative weights handle the rank-zero and affine-only-coordinate cases. In particular, weighted l1 error has one facet and rank one, giving `p_out<=p_conv+18n` independently of output count, degree, and the number of distinct coordinate curvatures.

## Scope and source credit

The outputs may be arbitrarily coupled through convex separable summands with arbitrary coefficient signs. This extends beyond independent outputs and beyond positive monomial coefficients. It does not cover arbitrary mixed multivariate polynomial terms: the exact shared interpolation construction relies on summing univariate chord contributions. Replacing it by multilinear corner interpolation would require a separate compact linear encoding argument.

Barycentric spanners and their determinant exchange are classical, as credited to Awerbuch and Kleinberg in the single-input theorem. The product packing, Jensen superadditivity, and scalar compiler are reviewed local dependencies. The proposed new step is the shared output basis together with a rank-scaled product code, producing a comparison with the original coupled vector integer minimum. The [source assessment](../notes/convex-separable-vector-curvature-rank-novelty.md) did not locate this combined theorem in the checked open literature; this is a qualified search finding, not proof of priority.

## Independent verification

Both the [first full audit](../notes/review-convex-separable-vector-curvature-rank-precision.md) and [second full audit](../notes/review-convex-separable-vector-curvature-rank-precision-second.md) pass. They check the original-vector lower-bound comparison, the common signed basis across every coordinate, both lattice-ball constants, simultaneous graph containment, and polynomial rational encoding. A wording clarification makes explicit that the facet gap bound holds separately for every facet; no proof correction was required.

The [second review's exact checker](../code/quadratic_rank/check_coupled_separable_rank_review.py) verifies 24 shared bases, 31 determinant exchanges, 39 negative representation coefficients, 540 gap dominations, 300 box bands, and 600 coupled-body error checks. The first review also records exact lattice-ball and gap checks. These calculations supplement the proofs; they do not establish the theorem by themselves.


The [separable oracle-body theorem](convex-separable-vector-oracle-curvature-rank-precision.md)
combines the shared-coordinate packing with an explicit inner band in the
nonlinear output image. It handles unconditional bodies given by strong
separation, with compact overhead `21n+2nceil(log2 r)`.
