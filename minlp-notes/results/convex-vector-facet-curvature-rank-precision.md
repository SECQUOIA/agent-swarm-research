# Coupled unconditional error budgets: precision controlled by facet curvature rank

Date: 2026-09-05. Status: independently reviewed result; two full audits passed. Author: `noncommutative_rank_review`; the constants were independently derived by root. The [box curvature-rank theorem](../notes/convex-vector-curvature-rank-precision.md) and its two audits are dependencies.

## 1. Statement

Let `F:[0,1]->R^m` be continuous and componentwise convex. Let the permitted output error body be

```
K={e in R^m: A|e|<=b},   A>=0,   b>0,
```

with finitely many rows and compact `K`. Define normalized facet functions

```
H_k(x)=sum_j (A_kj/b_k)F_j(x),
r=dim span{H_k} modulo affine functions of x.
```

The functions `H_k` are convex. This rank may be smaller than the curvature rank of the original vector; it also depends on the chosen error body.

Write `p_conv` for the minimum integer dimension over arbitrary convex lifts containing the exact graph and admitting only errors in `K`. General integers and unrestricted continuous formulation size are allowed. For `r>=1`, a finite binary linear formulation satisfies

```
p_bin <= p_conv+ceil(log2(8r-1)).                         (1)
```

For densely encoded rational polynomial outputs and rational `A,b`, there is a deterministic polynomial-time rational MILP construction satisfying

```
p_out <= p_conv+ceil(log2 r)+13.                          (2)
```

Input length includes the entire polynomial and error-body descriptions. Rank, degree, number of outputs, and number of rows may all grow. The construction uses one global binary index and is polynomial in tolerance encoding through `A,b`.

If `r=0`, the whole vector is affine and its graph needs no integers. To verify this, compactness and nonnegativity of `A` imply that every column has a positive entry. If all facet functions are affine, then their nonnegative weighted sums of component chord gaps vanish on every interval. Every component gap must vanish, so every component is affine.

## 2. Finite theorem

Apply the exact barycentric-spanner basis from the box theorem to the original convex functions `H_k` in their quotient by affine terms. Select `r` facet functions and define their sum `Psi`. For every interval, their nonnegative chord gaps imply

```
0<=g_(H_k)<=g_Psi    for every k.                         (3)
```

For any admissible lift with `p` integer variables, group exact graph contacts by integer parity and take the closures and interval hulls. The projected midpoint error on a hull belongs to `K`, and componentwise convexity makes it nonnegative. Thus the midpoint Jensen gap of each `H_k` is at most one. The midpoint gap of `Psi` is at most `r`, and its maximum chord gap on that hull is at most `2r`.

Use the direct scalar level-refinement lemma from the box theorem with target error `1/2` and integer factor `4r`. There are at most `8r-1` subintervals per parity hull with `g_Psi<=1/2`. Equation (3) gives

```
A g_F <= b/2,
```

so `g_F` belongs to `K/2`. If `T` is the exact vector chord on one such interval, use the polyhedral band

```
w-T(x) in K/2.                                          (4)
```

It contains the graph because `F-T=-g_F` belongs to `K/2`. Every admitted error is `(w-T)+g_F`, in `K/2+K/2=K`. This symmetric half-body construction is essential: an arbitrary box-style downward band need not respect the coupled budget.

There are at most `(8r-1)2^p` bands. Finite binary disjunction proves (1). The body is polyhedral because absolute values can be represented by continuous auxiliary variables.

## 3. Polynomial rational construction

Compute the densely encoded rational facet polynomials `H_k`. Use the polynomial determinant-exchange algorithm from the box theorem to select a 2-approximate barycentric spanner of their nonaffine coefficient rows. Let `Psi` be the sum of the selected original facet polynomials. Its chord gaps obey

```
0<=g_(H_k)<=2g_Psi.                                      (5)
```

The variable-rank polynomial termination and coefficient-bit bounds are unchanged: a row exchange multiplies an original rational row minor by more than two, and those minors have polynomial upper and nonzero lower bit bounds. No maximum-volume optimization oracle is required.

Every parity hull still has `g_Psi<=2r`. Refining to scalar tolerance `1/4` now uses at most `16r-1` subintervals. The finite-cover-to-partition argument from the box theorem gives

```
N_(1/4)(Psi)<=(16r-1)2^p.                                (6)
```

Compile `Psi` at tolerance `1/4` using the reviewed dense scalar compiler. Its actual cell count and exact chord error satisfy

```
K_cells<=486N_(1/4)(Psi),
g_Psi<=13/64 on each compiled cell.
```

Equation (5) yields `A g_F<=13b/32`, that is, `g_F in (13/32)K`.

To round original vector endpoints, compute the positive rational number

```
M_A=max_k sum_j A_kj/b_k,
rho=min(1,1/(16M_A)).
```

Compactness ensures `M_A>0`. Choose a dyadic downward rounding precision of absolute error at most `rho` for every original output coordinate. Then each endpoint rounding vector `v` satisfies `A|v|<=b/16`, so `v in K/16`. Interpolating the rounded endpoint values gives a rational chord `y`; its difference from the exact chord also belongs to `K/16` by convexity.

Consequently, on the entire cell,

```
y-F=(y-T)+(T-F) in K/16+(13/32)K=(15/32)K.
```

Use the band

```
w-y in K/2.                                             (7)
```

This contains the exact graph, since `F-y in (15/32)K subset K/2`. Every admitted error lies in

```
K/2+(15/32)K=(31/32)K subset K.
```

The rounded values, all outputs, and the absolute-value auxiliaries use the same input index and interpolation weight. Thus this is one vector approximation with the coupled budget enforced jointly.

For an explicit linear encoding of (7), add continuous `s_j` with `s_j>=w_j-y_j`, `s_j>=y_j-w_j`, and `A s<=b/2`. This projects exactly to (7), because `A>=0` and `s_j>=|w_j-y_j|`; choosing equality gives the reverse implication. It introduces no integer coordinates.

The row sums, dyadic precision, circuit output offsets, endpoint polynomial evaluations, and all body coefficients have polynomial bit length in the rational input. The scalar circuit supplies the same rational knots; extra output arithmetic and band constraints introduce only continuous wires and auxiliaries. The endpoint evaluation time is polynomial even for growing dense polynomial degree.

By (6),

```
K_cells<=486(16r-1)2^p<7776r 2^p<8192r 2^p.
```

The single binary index therefore uses at most `p+ceil(log2 r)+13` bits, proving (2). As before, the algorithm does not know or compute an optimal unrestricted-integer lift.

## 4. Weighted l1 error has constant overhead

For

```
K={e: sum_j omega_j |e_j|<=epsilon},
omega_j>0, epsilon>0,
```

there is only one facet function `H=sum_j omega_j F_j/epsilon`. If any component is nonaffine, this function is convex and nonaffine, so `r=1`. Thus (1) gives `p_bin<=p_conv+3`, and (2) gives a polynomial rational construction with `p_out<=p_conv+13`, independently of output count and polynomial degree.

The scalarization is not an arbitrary fixed direction under an unrelated tolerance. It is the defining coupled error budget applied to a nonnegative vector of Jensen gaps. This is why it controls all component chord errors jointly.

## Scope and source credit

The result retains one input and componentwise convexity. Nonnegative facet weights ensure convex scalar facet functions and nonnegative gap identities. The proof does not apply without further work to a tilted parallelogram with signed facet coefficients or an arbitrary centrally symmetric body.

The approximate barycentric spanner is a classical primitive credited in the [box theorem's bounded source assessment](../notes/convex-vector-curvature-rank-novelty.md), including Awerbuch and Kleinberg, section 2.3. Half-body Minkowski sums and binary disjunctions are also standard. The proposed extension is their rank-dependent graph-precision guarantee and compact rational implementation for a coupled unconditional budget. No necessity of the logarithmic rank term or exhaustive novelty is claimed.

Both complete audits passed without required corrections: [first audit](../notes/review-convex-vector-facet-curvature-rank-precision.md) and [second audit](../notes/review-convex-vector-facet-curvature-rank-precision-second.md). They checked the rational basis dependency, nonnegative facet scalarization, rank-zero case, parity transfer, rounding precision, common band, integer count, and weighted-l1 specialization.
