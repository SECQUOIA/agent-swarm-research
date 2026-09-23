# Independent audit: conditioned fixed-box follower approximation

Date: 2026-09-05. Reviewer: `benders_property`.

**PASS.** I independently checked
[the conditioned-box additive algorithm](bilevel-conditioned-box-additive-algorithm.md),
including the subsequently added elementary exact follower solver. The
algorithm returns a rational feasible leader and its exact rational
follower response within the stated normalized additive error. The
enumeration bound is independent of numerical magnitudes of `c,D,b`;
their binary encoding lengths still enter arithmetic complexity. This
audit verifies correctness and encoding, not literature novelty.

## Norm bounds and saturation

For symmetric matrices, the spectral norm is at most the infinity norm.
Applied to `Q^(-1)`, this gives
`mu=1/||Q^(-1)||_infinity<=lambda_min(Q)`. Also
`||Q||_infinity<=sqrt(N)||Q||_2`, and the same inequality holds for its
inverse, proving `K<=N*kappa_2(Q)`. Both `mu` and `K` are positive
rational numbers computable by exact linear algebra in polynomial bit
time. No eigenvalue oracle is required.

The saturation thresholds have the correct signs and include equality.
When coordinate `i` is positive, its gradient is bounded below by
`Q_ii z_i+m_i^-+c_i+D_i x`. Thus a cost at least `-m_i^-` gives a
strictly positive derivative and excludes a positive optimal coordinate.
When the coordinate is below one, its gradient is bounded above by
`Q_ii(z_i-1)+m_i^++c_i+D_i x`. A cost at most `-m_i^+` therefore forces
it to one. These arguments use `Q_ii>0` and permit arbitrary off-diagonal
signs.

The intervening slab has width
`R_i=sum_j |Q_ij|`, so `R_i/mu<=K`. The bounds are conservative rather
than exact active-set thresholds; this is sufficient. A coordinate with
zero row in `D` cannot be removed merely because its direct cost is
constant, since coupling may change its response. The candidate correctly
keeps such coordinates in `J` unless the saturation test freezes them.

## Closed cells and degeneracies

The threshold arrangement has polynomially many realizable sign
conditions for fixed leader dimension. Intersecting with a rational
polytope does not increase that count. Constant tests and lower-dimensional
leader domains can be treated by the same affine feasibility machinery.

For each nonempty sign condition, replacing its strict inequalities by
weak inequalities while retaining its equality tests and membership in
`X` gives its closure. To prove the reverse inclusion, mix a point of
that weak system with any point realizing the original strict signs.
Convexity preserves membership and all equalities, while every strict
sign holds for positive mixing weight. This handles cells lying on faces
of `X` and cells consisting of single points.

Coordinates labeled at or beyond a threshold have the asserted constant
response on the whole closed cell. The remaining coordinates stay within
their weak cost slabs, including any saturation endpoints reached on the
boundary. Overlap between closures is harmless. At least one enumerated
cell covers every leader, including an optimum.

## Response sensitivity and the row basis

On a cell, frozen coordinates agree at every leader. The remaining
problem has a fixed box and principal Hessian `Q_JJ`. Its smallest
eigenvalue is at least `lambda_min(Q)>=mu`. Adding the two follower
variational inequalities gives precisely

```
mu ||z(x)-z(x')||_2^2
 <= -(D_J(x-x'))^T(z_J(x)-z_J(x')).
```

Cauchy--Schwarz yields the displayed response bound. This argument
requires neither differentiability of the response nor a fixed active
set within the saturation cell.

Let `E=D_J/mu` have rank `q`. Once `q` independent columns have been
chosen, enumerate the `q`-row minors in those columns and select a
maximum absolute determinant. This is polynomial for fixed `r` because
`q<=r`. Cramer's rule shows that every row of `E` is a combination of
the selected full rows with coefficients bounded in absolute value by
one. The representation first holds on the selected columns. It then
holds on all columns, because the selected columns span the full column
space. This is a linear-algebra argument, not an assumption about the
conditioning of the selected basis.

Consequently a displacement of at most `delta` in each basis-row
coordinate changes every row of `E x` by at most `q delta`. The response
distance is at most `sqrt(N)q delta`. If `q=0`, the parameter-dependent
cost of the unfrozen subproblem is constant; its unique response is
constant, so one LP minimizing the direct leader cost suffices. A leader
domain with dimension below `q` merely creates empty grid intersections;
it does not invalidate these bounds. A zero-dimensional leader is also
covered by this constant-response case.

## Cover and approximation guarantee

Each basis coordinate has an explicit rational interval of width at
most `K`. Its offset can be arbitrarily large, but its bit length is
polynomial. Subdividing by
`delta=epsilon/(Nr)` uses at most `2+KNr/epsilon` intervals per selected
row. The grid has dimension `q<=r`; it is not a grid in follower
dimension. Empty grid intersections are rejected by LP, and all nonempty
ones are compact rational polytopes.

Minimizing `b^T x` exactly on each intersection is essential and correct.
For an optimal leader `xstar`, the retained leader in any covering grid
intersection has direct leader cost no greater than `b^T xstar`.
The response term changes by at most

```
||a||_2 sqrt(N) q delta
 <= ||a||_1 sqrt(N) r delta
 <= epsilon ||a||_1.
```

Thus the direct term cannot consume the approximation allowance even
when `b` is numerically large. Choosing the best evaluated retained
leader proves the theorem. The optimum exists because a strictly convex
fixed-box follower has a continuous unique response and `X` is compact.

The candidate count is
`N^{O(r)}(2+KNr/epsilon)^r`. No numerical bound on `c,D,b` is used in
this count. Their bit lengths affect rational LPs and follower
evaluations, as they should. If `a=0`, exact LP is sufficient; the
absolute-error conversion must retain the stated possible dependence on
`||a||_1/epsilon_abs`.

## Exact rational follower output

At a rational retained leader, every strictly interior follower
coordinate has zero gradient. The corresponding principal matrix of
`Q` is nonsingular. Fixing all other coordinates to zero or one therefore
gives a rational solution whose numerator and denominator lengths are
polynomial in the sampled input. Rationality alone would not identify
the correct active set efficiently, but classical polynomial-bit convex
QP algorithms provide that computation. The primary attribution is
[Kozlov, Tarasov, and Khachiyan's convex-QP result](https://www.mathnet.ru/eng/zvmmf5189).

The candidate's additional elementary method also suffices under its
allowed polynomial dependence on `K`. Set `L=||Q||_infinity` and
iterate the exact rational map

```
z_next=clip_[0,1](z-(Qz+t)/L),  t=c+D x.
```

Projection is nonexpansive and the linear part has Euclidean operator
norm at most `1-1/K`. Starting at zero gives distance at most `sqrt(N)`.
Clear a common denominator from `Q,t` and bound the absolute integer
entries by `H>=1`. Every free principal determinant is at most
`f!H^f<=N!H^N=B`, so every exact optimal coordinate has reduced
denominator at most `B`. Contributions from fixed-one coordinates affect
the right-hand side, not this determinant bound.

The proposed iteration count is valid. With

```
S=2 ceil(log_2 B)+ceil(log_2 N)+4,
k=ceil(K) S,
```

the error is at most
`sqrt(N)exp(-S)<=sqrt(N)2^(-S)<=1/(16 B^2 sqrt(N))`, strictly below
`1/(4B^2)`. The case `K=1` already contracts to zero in one step.
Distinct rationals of denominator at most `B` differ by at least
`1/B^2`, so continued-fraction reconstruction identifies the exact
coordinate. Exact box KKT checks verify the result.

For explicit iterate-size control, clear a common denominator `T` from
the fixed affine update coefficients. Starting at zero, every coordinate
at iteration `k` has denominator dividing `T^k`; clipping to zero or
one preserves this property. Since iterates stay in the unit box, their
numerators need no more bits than that denominator. Thus bit length is
polynomial in `K` and sampled input length. This independently closes
the exact-inner-output argument without an active-set search.

The optional solver introduces additional polynomial numerical
dependence on `K`. The sentence saying that enumeration is the only
such dependence should therefore be understood as applying to the
classical polynomial-bit QP implementation; either implementation gives
the stated overall theorem. I requested this small qualification.

## Diagnostics and scope

Two exact symbolic diagnostics passed during this audit. A two-column
matrix with rows `(1,0),(0,1),(10,1),(-2,3),(0,0)` has a selected maximum
minor whose row expansion coefficients all lie in `[-1,1]`. Also, for

```
Q=[[2,-1],[-1,2]],  c=(0,-1/2),  D=(-1,0)^T,
```

the interior response on `x in [0,1]` is
`((2x+1/2)/3,(x+1)/3)`. Its second coordinate varies even though its row
of `D` is zero, illustrating why the algorithm's handling of such rows
is necessary. Here `mu=1` and `K=3`, consistent with the stated bounds.
These checks supplement the proofs; they are not an implementation of
the entire approximation algorithm.

The guarantee depends on a fixed unit-box follower and no follower-based
upper constraints. It does not silently guarantee exact preservation of
arbitrary upper feasibility conditions by a nearby response. It is
polynomial in inverse tolerance, not in accuracy bits, and it does not
contradict exact or high-precision hardness. No substantive defect remains
under the stated hypotheses.
