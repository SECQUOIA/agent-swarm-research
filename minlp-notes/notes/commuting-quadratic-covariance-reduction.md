# Commuting Hessians reduce the covariance problem to scalar allocation

Date: 2026-09-05. Status: independently reviewed support result.

If the symmetric Hessians commute pairwise, the reviewed determinant
benchmark has an optimizer diagonal in their common orthonormal
eigenbasis. This remains true for indefinite Hessians. Averaging the
covariances arithmetically would not justify the claim; the midpoint
of an affine-invariant matrix geodesic does.

## A determinant-preserving symmetry operation

Work in a common eigenbasis and let `S` be any diagonal sign matrix.
Then `S H_j=H_j S`, so replacing `P` by `SPS` preserves every energy
`tr(H_j P H_j P)`, the cap `P<=I`, and the determinant. For positive
definite `P`, define

```
M=P#(SPS)
 =P^(1/2)[P^(-1/2)(SPS)P^(-1/2)]^(1/2)P^(1/2).
```

This is the midpoint of the geodesic used in the
[covariance theorem](../results/quadratic-weighted-covariance-precision.md).
Its established geodesic convexity proof shows that `M` is feasible
whenever `P` is feasible. The determinant identity gives
`det M=sqrt(det P det(SPS))=det P`.

The geometric mean is symmetric in its two arguments and is invariant
under simultaneous orthogonal congruence. These identities follow from
the unique positive definite solution of `M P^(-1) M=Q`, namely
`P#Q`. In particular,

```
S M S=(SPS)#P=M.
```

Thus `M` commutes with `S`. If `P` already commutes with another
commuting sign matrix `S'`, then both mean arguments and their matrix
functions commute with `S'`, so this previous symmetry is preserved.

Starting from a positive definite determinant optimizer, apply this
operation successively to the `n` coordinate sign flips. The final
matrix is diagonal, feasible, and has exactly the same determinant.
A positive definite optimizer exists because small scalar multiples
of the identity are feasible and the original feasible set is compact.

## A convex program with only linear constraints

Write `H_j=diag(h_j1,...,h_jn)` and `P=diag(p_1,...,p_n)` in that basis.
The covariance problem becomes

```
maximize   sum_i log t_i
subject to sum_i h_ji^2 t_i<=epsilon_j^2,   every j,
           0<t_i<=1,                       every i,
```

where `t_i=p_i^2`. Its optimum objective is `2 log D`. This is an
ordinary concave maximization with linear constraints. In particular,
indefinite signs cause no residual nonconvexity in this commuting case.

For a correlated positive semidefinite output budget `W_l`, simply
replace the coefficient `h_ji^2` in each row by

```
a_li=h_:i^T W_l h_:i>=0.
```

The same symmetry proof applies because all Hessians commute with each
sign flip. When the common eigenbasis and eigenvalues are rationally
given, the allocation problem has rational linear constraints; the
rational grid construction can then be applied without the general
Riemannian optimization stage. This note does not claim a fast exact
rational common eigenbasis algorithm for arbitrary rational inputs.

## One Hessian has an explicit solution

For a single Hessian with eigenvalues `lambda_i`, put `a_i=lambda_i^2`.
If `epsilon^2>=sum_i a_i`, then `D=1` and every `p_i=1` is optimal.
Otherwise there is a unique positive number `s<max_i a_i` satisfying

```
sum_i min(a_i,s)=epsilon^2.
```

The optimizer is

```
t_i=min(1,s/a_i)   if a_i>0,
t_i=1             if a_i=0,
p_i=sqrt(t_i).
```

The equality constraint uses the entire budget. To check optimality,
set the multiplier for it to `1/s`. For every unsaturated coordinate,
`1/t_i=a_i/s`; for a saturated positive coordinate, `a_i<=s`, so the
nonnegative upper-bound multiplier is `1-a_i/s`. For a zero coefficient,
that multiplier is one. These equations certify optimality in the
strictly concave scalar program. Sorting the `a_i` gives `s` by solving
a linear equation on the appropriate interval.

For `H=I` and unit tolerance this gives `p_i=n^(-1/2)`, recovering the
exact benchmark in the [dimension-gap example](covariance-benchmark-dimension-gap.md).

The support result combines standard matrix-geometric-mean symmetries
with the already proved geodesic feasibility. It does not claim that
scalar resource allocation or geometric-mean symmetrization is new.
Its purpose is to identify a simpler exact benchmark for a structured
quadratic family and to rule out the need for a matrix optimization
stage when a rational common diagonalization is already available.

The [independent proof audit](review-commuting-quadratic-covariance-reduction.md)
passed, including symmetry preservation, correlated budgets, objective
normalization, and every water-filling boundary case.
