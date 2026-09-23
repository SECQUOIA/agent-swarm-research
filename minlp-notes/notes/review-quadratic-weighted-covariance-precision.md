# Independent audit: finite weighted covariance precision law

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Source: `notes/quadratic-weighted-covariance-precision.md`, including
its subsequently added geodesic-convexity observation.

## Verdict and correction made

The determinant characterization, explicit dimension-only constants,
arbitrary convex integer-lift lower bound, rotated compact binary upper,
weighted graph reduction, and geodesic-convexity observation pass this
independent mathematical audit. No outstanding substantive gap was found.

One formulation-size statement initially used the *minimum* binary count
`p_bin` where its proof counted the *constructed* number of bits. I flagged
this, and the author corrected the statement to `p_grid<=Phi+B_n` and
size `O(n p_grid+n^2+mn^2)`. The original size notation was not justified:
the finite bounds would only give `p_grid<=p_bin+A_n+B_n`, potentially
adding `O(n^2 log(n+1))` to a size expression in terms of the minimum.
The current statement is correct.

This is a proof audit, not a novelty assessment or certification of a
numerical algorithm for the determinant problem. I did not rerun the
author's numerical suite; the findings below come from separate algebraic
and geometric derivations.

## Feasibility, attainment, and degenerate data

The optimization is over the closed bounded set `0<=P<=I`, intersected
with finitely many continuous energy sublevel sets. It is compact. For
symmetric `H` and positive semidefinite `P`, the energy is nonnegative:

```
tr(H P H P)=||P^(1/2) H P^(1/2)||_F^2.
```

A sufficiently small positive scalar multiple of the identity satisfies
every positive tolerance. A zero Hessian imposes no restriction and
must simply be skipped in any formula dividing by its norm. Therefore
the optimum determinant is positive. Every determinant maximizer is
positive definite, because a singular positive semidefinite matrix has
zero determinant. The maximum is thus attained in the positive definite
part even though the definition correctly uses the closed semidefinite
feasible set.

All eigenvalues are at most one, so `0<D<=1` and `Phi>=0`. If every
Hessian vanishes, `D=1`; the actual graph is affine and both minimum
integer counts are zero. The finite inequality remains valid in this
case. No assumption that the tolerances are small is needed anywhere
in the theorem. Unequal tolerances, repeated outputs, zero Hessians,
and very large tolerances are all included.

## Parity covariance lower bound

Same-parity integer graph lifts have an integral midpoint inside the
original convex lifting set. The quadratic midpoint identity gives
`|q_j(x-y)|<=4 epsilon_j` for `q_j(v)=v^T H_j v/2`. Closing the parity
supports in the compact unit cube preserves these pair inequalities and
coverage. This avoids any regularity assumption on the projection or
on the original lifting set.

For a positive-volume support, its centered uniform covariance `Sigma`
is positive definite. The fourth-moment identity has the factors in
the draft and gives
`tr(H_j Sigma H_j Sigma)<=16 epsilon_j^2` separately for every output.
There is no summation over the number of outputs in this step, which
is why the final additive constant can be independent of `m`.

For any unit vector `v`, the scalar projection of the unit cube has
width `||v||_1<=sqrt(n)`. Its variance is at most one quarter of that
width squared. Hence `Sigma<=(n/4)I`, even though the coordinatewise
variance bound alone would not justify `Sigma<=I` in arbitrary dimension.
Scaling by exactly `c_n=max(4,n/4)` simultaneously enforces the matrix
cap and all weighted energy constraints. Thus
`det Sigma<=c_n^n D`.

The volume-covariance inequality gives

```
vol(S)<=omega_n(n+2)^(n/2)c_n^(n/2) sqrt(D)
      =2^A_n sqrt(D).
```

Zero-volume supports need no covariance argument. Summing over at most
`2^p` closed supports covering the unit-volume cube proves
`p>=Phi-A_n`. Combining with the trivial nonnegative integer count
gives the stated maximum with zero. The exact powers in `A_n` are
correct, and its size is `O(n log(n+1))` with no dependence on Hessians,
affine terms, tolerances, or the number of outputs.

## Rotated grid, endpoints, and error constant

An optimal `P` has an orthogonal eigendecomposition with
`0<lambda_i<=1`. The width of a unit-cube projection on a unit vector
is its l1 norm, which lies between 1 and `sqrt(n)`. These bounds ensure
that every displayed depth
`L_i=ceil(log2(w_i sqrt(n/lambda_i)))` is nonnegative. In dimension one,
`lambda_1=1` gives an empty prefix, as intended.

The expansion with residual width `h_i=w_i 2^(-L_i)` covers the entire
rotated bounding interval. Its upper endpoint is attained using an
all-ones prefix plus the full residual. Retaining the original box
through affine identities and its original inequalities is sufficient;
extra points in the bounding box do not affect graph containment or
the error guarantee on the original domain.

For a distinct-index monomial, both prefix terms in
`y_i y_k=A_i y_k+rho_i A_k+rho_i rho_k` are exact sums of
binary-times-bounded-continuous products. Residual McCormick error is
at most `h_i h_k/4`. For a square the same identity reduces correctly
to a binary-prefix expression plus `rho_i^2`, and the stated triangle
has two-sided error at most `h_i^2/4`.

The output is written as one half of the ordered double sum of its
symmetric Hessian entries. Therefore the combined absolute error is
exactly bounded by

```
(1/8) sum_(i,k) |G_(j,ik)| h_i h_k.
```

This counts off-diagonal coefficients twice and diagonal coefficients
once, matching the Hessian convention. Since
`h_i h_k<=sqrt(lambda_i lambda_k)/n`, entrywise l1-to-Frobenius
Cauchy-Schwarz gives the bound

```
error_j <= (1/8)||diag(sqrt(lambda)) G_j diag(sqrt(lambda))||_F
        = (1/8)sqrt(tr(H_j P H_j P))
        <= epsilon_j/8.
```

Thus the constant is deliberately slack but valid for every dimension.
There is no cancellation assumption. Sharing approximate monomial
variables across outputs cannot defeat the bound, and exact graph
points have simultaneous lifts using actual residual products.

## Binary count and compact formulation size

Summing the ceilings gives

```
p_grid <= -(1/2)sum_i log2 lambda_i
          +sum_i log2 w_i +(n/2)log2 n+n
       <= Phi+n log2 n+n.
```

The coefficient of `Phi`, the two half-dimension logarithmic terms,
and the rounding term are all correct. Every coordinate bit participates
in at most a linear number of monomial prefix products. There are
quadratically many possible residual monomials, and output assembly
has at most `mn^2` coefficients. This proves the corrected size bound
in terms of `p_grid` without enumerating grid cells.

All coordinate changes and coefficients may be real. The note correctly
does not infer polynomial bit complexity from attainment, eigendecomposition,
or the number of variables. The dimension-only additive guarantee concerns
existence and binary/row counts, not an already implemented global optimizer.

## Exact graph special case

For an edge Hessian, direct multiplication yields
`2(P_ii P_kk+P_ik^2)`. Replacing a feasible positive semidefinite matrix
by its diagonal keeps its entries between zero and one, reduces each
such energy, and weakly increases the determinant by Hadamard's
inequality. A diagonal optimum therefore exists.

Writing `P_ii=2^(-2s_i)` transforms the edge constraint to

```
2*2^(-2(s_i+s_k))<=epsilon_(ik)^2,
s_i+s_k>=log2(sqrt(2)/epsilon_(ik)).
```

Thus the stated weighted fractional vertex-cover LP is exactly the
value `Phi`, not just an upper bound on it. Negative demands are
redundant because `s_i>=0`, and isolated vertices choose `s_i=0`.
The diagonal replacement argument depends on this special edge energy;
it does not justify diagonal restriction for arbitrary quadratic tuples.

## Added geodesic-convexity observation

The new observation also passes independent review. For
`P(t)=P_0^(1/2)exp(tA)P_0^(1/2)`, diagonalizing the symmetric generator
and using Hessian symmetry gives

```
tr(H_j P(t) H_j P(t))
 =sum_(i,k) C_(j,ik)^2 exp(t(a_i+a_k)).
```

Every coefficient is nonnegative. Therefore the energy is convex in
`t`, and its logarithm is convex when the Hessian is nonzero. For a
zero Hessian the energy is identically zero and no logarithm is needed.
The determinant logarithm is affine along this path.

For the path joining two positive definite feasible endpoints, the
inequality `d^t<=1-t+td` for positive eigenvalues and `0<=t<=1` gives
`P(t)<=(1-t)P_0+tP_1<=I`. Hence both the matrix cap and every energy
sublevel set are geodesically convex. A geodesic to a point of larger
determinant would increase the affine log determinant immediately,
contradicting any local maximum in the positive definite feasible set.
The statement is therefore correct with its explicit positive definite
scope. It does not by itself supply an iteration, conditioning, or
finite-precision complexity guarantee.

The claim that the feasible set need not be Euclidean convex is
compatible with this observation. For example, diagonal matrices
`diag(1,1/10)` and `diag(1/10,1)` each have off-diagonal-Hessian energy
`1/5`, whereas their arithmetic midpoint has energy `121/200>1/5`.
Both endpoints obey the matrix cap.

## Norm-equivalence interpretation

The ellipsoid interpretation is valid because the Frobenius energy
bound dominates the operator norm. More explicitly, if `D_F` and
`D_op` use the corresponding Frobenius and operator constraints, then

```
D_F <= D_op <= n^(n/2) D_F.
```

The first inequality follows from norm ordering. For the second, any
operator-feasible `P` becomes Frobenius-feasible after scaling by
`1/sqrt(n)`, which preserves `P<=I` and changes determinant by
`n^(-n/2)`. This makes the draft's dimension-only comparison precise.
It does not alter or weaken the proven weighted Frobenius theorem.
