# Finite formulations for coupled separable continuous convex outputs

Date: 2026-09-05. Status: supporting consequence; an [independent full audit passes](review-convex-separable-vector-curvature-rank-precision-second.md) in that report's finite-companion addendum. This is the finite real-coefficient companion to the [reviewed compact polynomial theorem](../results/convex-separable-vector-curvature-rank-precision.md). The basis and packing arguments are inherited, with an exact basis and a direct finite disjunction replacing their polynomial implementations.

Let

```
F_j(x)=ell_j(x)+sum_i phi_ji(x_i),   x in [0,1]^n,
```

where the summands are continuous and convex, and the affine terms may have real coefficients. Let the positive box tolerances be `epsilon_j`. In the direct sum over coordinates of the function spaces modulo affine functions, take the rank `r` of the `m` normalized output rows. This finite rank is at most `m` even if the summands are not polynomials. Remove coordinates on which all outputs are affine; `n` below counts the remaining coordinates.

For `n,r>=1`, a finite real-coefficient binary linear lift satisfies

```
p_bin <= p_conv+n ceil(log2 r)+7n.                       (1)
```

For a compact unconditional body `K={e:A|e|<=b}`, with `A>=0` and `b>0`, define `r` using the normalized facet functions `(AF)_k/b_k`. Then

```
p_bin <= p_conv+n ceil(log2 r)+8n.                       (2)
```

The body and function coefficients may be real in these finite statements. If the rank is zero, the graph is affine and requires no integers. No effective representation, computability, or polynomial formulation-size claim is made for arbitrary continuous inputs.

## Proof for the box

Choose a maximum-volume basis of the finitely many normalized output rows in their `r`-dimensional span. Every original row has representation coefficients with absolute value at most one. The same representation holds in every coordinate modulo affine functions. Thus, for the sum `Psi` of the selected outputs and its coordinate summands `psi_i`, every original normalized coordinate chord gap is nonnegative and at most the corresponding gap of `psi_i`.

Take scalar midpoint packings at tolerance `tau=1/n`. Write their sizes as `P_i`. The scalar refinement argument in the compact theorem gives a partition with at most `N_i<=6P_i` intervals, each with `psi_i` chord gap at most `1/n`. Therefore the finite binary disjunction for this coordinate can use `L_i=ceil(log2 N_i)` bits, with

```
2^(L_i)<=2N_i<=12P_i.                                    (3)
```

Every selected original output uses these same coordinate intervals and interpolation weights. Its total chord gap is between zero and one. If `T_j` is the sum of its normalized exact chords and restored affine term, the band `T_j-1<=w_j<=T_j` contains its exact graph and admits only unit error. One finite disjunction per coordinate encodes its interval and all corresponding original-output chords. Thus only the `sum_i L_i` selector bits are declared integer; the band adds continuous variables and inequalities.

In the product packing, index distance greater than `nr` makes the midpoint gap of `Psi` greater than `r`, so at least one original selected output has midpoint gap greater than one. These contacts are incompatible for the original vector lift. The lattice-ball estimate in the compact theorem with `a=1` bounds a deleted ball by `(9r)^n`. Parity therefore yields

```
2^(p_conv)>=product_i P_i/(9r)^n.
```

Combining this with (3) gives

```
p_bin<=p_conv+n log2(108r)<p_conv+n log2 r+7n,
```

which implies (1).

## Proof for the coupled body

Use a maximum-volume basis of the normalized facet rows and sum its selected facet functions. Choose `tau=1/(2n)`. Every facet's coordinate chord gaps now sum to at most `1/2`. Since the original component gaps are nonnegative, the original vector chord error is in `K/2`. The band `w-T in K/2` therefore contains the graph and admits errors in `K`. Absolute-value auxiliary variables encode it with finitely many continuous linear inequalities.

The product-packing separation threshold is `2nr`; the lattice-ball bound with `a=2` is `(15r)^n`. Equation (3) is unchanged at the new tolerance. Hence

```
p_bin<=p_conv+n log2(180r)<p_conv+n log2 r+8n,
```

proving (2). Compactness of `K` and nonnegative facet weights ensure that a rank-zero facet system forces every original coordinate curvature to vanish, as in the reviewed facet theorem.

These bounds are existence statements for finite linear disjunctions, compared against arbitrary convex lifts with unrestricted general integer variables. They do not restrict the admissible lower-bound lift's continuous dimension, integer range, or convex-set description. The max-volume basis is the classical barycentric-spanner primitive credited in the main theorem; no new basis or scalar approximation algorithm is asserted here.
