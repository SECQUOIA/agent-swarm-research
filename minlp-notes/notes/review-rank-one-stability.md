# Independent audit of correlation-face stability

Date: 2026-09-04. Reviewer: independent `review_extension` agent.

Reviewed result: [Quantitative stability of the correlation face and
approximate LP lower bounds](../results/rank-one-correlation-face-stability.md).

Verdict: the original rounding proof, its constant `136m+10`, exact-penalty
consequence, outer-approximation transfer, and approximate LP lower bound
are mathematically correct. No required correction was found. The proof
also yields the sharper outer-approximation factor `m(184m+6)` derived below,
improving the original order `m^3` to order `m^2`.

## Rounding proof

All matrix norms in the result are entrywise l1 norms. This convention is
essential for both the outer-product estimates and the later objective
duality. For nonnegative vectors, `||uv^T||_1=||u||_1||v||_1`.

The atom is `W=rc^T/S`, with both marginal sums equal to `S`. The bound
`||r-c||_1<=2SD` follows from the scalar inequality
`|a-b|<=a(1-b)+b(1-a)` on the unit square. The binary rounding estimates
are valid even at rounding ties:

```
sum_i r_i(1-r_i) <= SD+||r-c||_1 <= 3SD,
u=||r-a||_1 <= 6SD,
v=||c-a||_1 <= u+||r-c||_1 <= 8SD.
```

The pair product estimate charges each coordinate discrepancy exactly once,
so the number `h` of full pairs satisfies `h<=SB+8SD`. With `k=sum a` and
`z` empty pairs, `k=m+h-z`, hence

```
||a-b||_1=h+z=2h+m-k <= 2SB+22SD+|S-m|.
```

Here the repaired vector `b` has exactly one selected entry per pair.
The rescaled comparison vector `b_tilde=(S/m)b` has total `S`, just like
`r,c`. It need not belong to the unit cube; that is harmless because the
following estimates require only nonnegativity and its total. Splitting
the outer-product difference into two terms and dividing by `S` gives
`||rc^T/S-b_tilde b_tilde^T/S||_1<=||r-b_tilde||_1+||c-b_tilde||_1`.
The remaining normalization discrepancy has norm exactly `|S-m|`.
Thus the claimed total atom estimate is

```
||W-bb^T/m||_1 <= 4SB+58SD+5|S-m|.
```

No error term is divided by a small total. The separate zero-atom case is
valid. Substituting `S<=2m`, the definition of `g`, and `B+D<=g` gives
the stated coefficient `136m+10`: the intermediate coefficients are
`18m+5` on `B`, `136m+5` on `D`, and `5` on `g`.

Finite convex decomposition, convexity of the norm, and affinity of `g`
give the error bound on the whole compact hull. The proof is an existence
argument for a general hull point; it does not provide an efficient method
to find its rank-one decomposition. The result correctly says this.

## Penalty and approximation consequences

The exact-penalty corollary uses the dual estimate
`|<H,W-V>|<=||H||_infinity ||W-V||_1`. The strict condition on its penalty
coefficient is necessary for the stated claim that every minimizer lies
on the face; equality of the threshold would only ensure that at least
one face minimizer is optimal.

The exposing functional has maximum absolute coefficient `4m+2`, not
`4m+1`, because its diagonal coefficient includes the total-sum term.
The draft uses the correct constant. A point of the outer set on the
three face equations has `g=0`, so an entrywise distance `epsilon` to the
hull gives `g(W)<=(4m+2)epsilon`. The triangle inequality and the linear
projection then give the original factor
`m[1+(4m+2)(136m+10)]` exactly. Neither symmetry of the outer approximation
nor attainment of an optimization problem over it is needed. Membership
in the stated Minkowski sum already supplies the required nearby hull point.

The LP source was opened and read independently:
[Braun, Fiorini, Pokutta and Steurer, *Approximation Limits of Linear
Programs (Beyond Hierarchies)*](https://www.bayesianestimation.org/paper/approxlp.pdf).
Theorem 6(i), PDF page 18, applies to the minimum number of inequalities
in any polyhedron between `COR(m)` and a fixed dilation of their explicitly
defined outer polyhedron in `R^(m x m)`. Their definition permits arbitrary
auxiliary dimension and does not count affine equations. The dilation
factor two used here satisfies its hypothesis.

The coefficient matrix `2diag(a)-aa^T` has entrywise infinity norm at most
one. Thus entrywise l1 error at most one relaxes each of its valid bounds
from one to two. This works on nonsymmetric matrices as well, agreeing
with the ambient space of the cited theorem. Section 4.3, Lemma 9 of the
same source provides a small PSD lift for a set in this sandwich, so the
note correctly declines to infer approximate SDP hardness from this
particular family of inequalities.

These source-derived assertions concern only a transferred established
lower bound. They do not certify novelty of the quantitative rank-one result.

## Sharper residual averaging

The atom calculation yields a stronger global affine bound than the original
single-slack estimate:

```
dist_1(W,F) <= 28m B(W)+156m D(W)+5[m-T(W)]    for every W in K.
```

To prove it, first replace `S` by its upper bound `2m` in the atom estimate:

```
||W-V||_1 <= 8m B+116m D+5|S-m|.
```

The earlier exposing-inequality proof gives
`S-m<=2mB+4mD`. Since its right side is nonnegative, it also bounds
`(S-m)_+`. Consequently

```
|S-m|=2(S-m)_++m-S <= 4mB+8mD+m-S.
```

Substitution proves the displayed affine bound for a nonzero atom. The zero
atom also satisfies it: its chosen face point has distance `m`, while the
right side is `161m`. Because the entire right side is affine, the same
convex-decomposition argument proves it on `K`. The signed term `m-T(W)`
must be kept during this averaging step; replacing an average of absolute
values by the absolute value of the average would be invalid.

For `Y` satisfying the three face equations and `||Y-W||_1<=epsilon`,
the coefficient infinity norms of `B`, `D`, and `T` are each at most one.
Therefore

```
0<=B(W)<=epsilon,  0<=D(W)<=epsilon,  |m-T(W)|<=epsilon,
dist_1(Y,F) <= (184m+6)epsilon.
```

The principal-block projection multiplies distance by at most `m`. Thus
the outer-approximation theorem holds with

```
A'_m=m(184m+6).
```

The identical LP sandwich argument now applies whenever
`epsilon_m<=1/[m(184m+6)]`, an order `m^-2` accuracy threshold. This
improvement was independently rechecked by the author, who confirmed all
steps and adopted it in the outer-approximation theorem.

## Exact arithmetic verification

[audit_face_stability.py](../code/rank_one_hardness/audit_face_stability.py)
exhausts equal-total marginal pairs on the grid `{0,1/4,1/2,3/4,1}` for
`m=1,2`. It checks the mismatch, rounding, pair-repair, normalization,
original error bound, and sharper affine residual bound with rational
arithmetic. The test supplements the proof and covers nonsymmetric atoms,
zero marginals, rounding ties, and totals on both sides of `m`.
All checks passed: 85 pairs for `m=1` and 38,165 pairs for `m=2`.
