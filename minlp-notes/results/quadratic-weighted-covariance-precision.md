# Unequal quadratic output accuracies: a finite covariance determinant law

Date: 2026-09-05. Status: independently reviewed by two agents; see the audit links below.
Publication priority is unestablished. This note extends the reviewed
[noncommutative-rank precision theorem](../results/quadratic-system-noncommutative-rank-complexity.md)
to finite, unequal output tolerances. The argument needs no noncommutative
rank machinery and gives constants depending only on the input dimension.

## Statement

Let `n>=1`, `m>=1`, and

```
f_j(x)=(1/2)x^T H_j x+a_j^T x+b_j,  x in [0,1]^n,
H_j real symmetric,  epsilon_j>0.
```

Define `p_conv` as the least number of unrestricted general integer
coordinates in an arbitrary finite-dimensional convex lift whose projection
contains the entire graph and, at each admitted input in the box, admits
only outputs satisfying `|w_j-f_j(x)|<=epsilon_j`. Neither closure of the
convex lift nor bounded integer ranges is assumed. Define `p_bin` similarly
using binary linear extended formulations. Continuous lift dimensions are
unrestricted in both definitions.

Set

```
D = max det P
    subject to 0 <= P <= I,
               tr(H_j P H_j P) <= epsilon_j^2   (j=1,...,m),
Phi = -(1/2) log2 D.
```

Matrix inequalities are in the positive semidefinite order. The maximum
exists by compactness. A sufficiently small positive multiple of `I` is
feasible, so `D>0`; consequently every determinant maximizer is positive
definite. Also `D<=1` and `Phi>=0`.

Let `omega_n` denote the volume of the Euclidean unit ball and define

```
c_n=max{4,n/4},
A_n=log2[omega_n (n+2)^(n/2)] +(n/2)log2 c_n,
B_n=n log2 n+n.
```

**Theorem.** For every such system and all positive tolerances,

```
max{0, Phi-A_n} <= p_conv <= p_bin <= Phi+B_n.             (1)
```

The upper formulation uses `p_grid<=Phi+B_n` binaries and at most
`O(n p_grid+n^2+mn^2)` rows and continuous variables. Coefficients can be
arbitrary real numbers. In particular, this is an existence and formulation
size theorem, not a polynomial-time algorithm or rational encoding theorem
for optimizing `D` or computing its eigenspaces.

For rational data, the separately reviewed
[polynomial construction theorem](quadratic-weighted-precision-polynomial-construction.md)
computes a rational formulation with the same additive-order guarantee.

Thus integer precision is determined to additive `O(n log(n+1))` by one
matrix optimization, uniformly over all Hessians, affine coefficients,
numbers of outputs, and positive, unequal tolerances. For another
full-dimensional box, first normalize the input coordinates to `[0,1]^n`
and use the transformed Hessians.

## Lower bound: covariance of parity supports

For each of the `2^p` parity classes of the integer coordinates, collect
the graph inputs admitting a graph lift in that class. Their union covers
the box. Two such graph lifts have an integer midpoint. Convexity and the
quadratic midpoint identity therefore give, within each support,

```
|(1/2)(x-y)^T H_j(x-y)| <= 4 epsilon_j.                  (2)
```

Taking the closure of each support in the compact box preserves (2) and
the cover. The resulting sets `S` are compact and measurable, whether or
not the initial projection or convex lift is closed.

Consider a support with positive volume. Let `X` be uniform on `S`,
center it, and let `Y` be an independent centered copy. Write `Sigma` for
the positive definite covariance. The exact fourth-moment identity is

```
E[((1/2)(X-Y)^T H_j(X-Y))^2]
 = (1/2)E[(X^T H_j X)^2]
   +(1/2)(E[X^T H_j X])^2 + tr(H_j Sigma H_j Sigma).
```

All three terms on the right are nonnegative. Equation (2) gives

```
tr(H_j Sigma H_j Sigma) <= 16 epsilon_j^2.               (3)
```

For any unit vector `v`, the range of `v^T x` on the unit cube has width
`||v||_1<=sqrt(n)`. A scalar variable supported in an interval of width
`w` has variance at most `w^2/4`: its squared distance from the interval
midpoint is at most that number, and centering at its mean minimizes
mean squared distance. Consequently `Sigma<=(n/4)I`.

It follows that `P=Sigma/c_n` is feasible for the determinant problem:
the matrix cap uses `c_n>=n/4`, and (3) uses `c_n>=4`. Hence

```
det Sigma <= c_n^n D.
```

The elementary volume-covariance inequality is

```
vol(S) <= omega_n (n+2)^(n/2) sqrt(det Sigma).
```

To see this, whiten the centered set. Its covariance is the identity
and its mean squared radius is `n`. Among measurable sets of prescribed
volume, a centered ball minimizes the integral of squared radius, as
can be proved by exchanging exterior points with missing interior
points. A ball of radius `R` has mean squared radius `n R^2/(n+2)`.
Thus the whitened set has volume at most `omega_n(n+2)^(n/2)`.

Every parity support therefore has volume at most `2^A_n sqrt(D)`.
Zero-volume supports satisfy the same bound. Summing over the cover of
the unit-volume cube gives `1<=2^p 2^A_n sqrt(D)`, proving the lower
bound in (1).

This is a quantitative application of the established parity method in
Lubin, Vielma, and Zadik, *Mixed-integer convex representability*,
[open paper](https://arxiv.org/abs/1706.05135). The parity method itself
is not a new contribution.

## Upper bound: a rotated dyadic grid

Take a determinant maximizer `P=U diag(lambda_i) U^T`, where `U` is
orthogonal and `0<lambda_i<=1`. Rotate the input by `U^T`. The exact
width of coordinate `i` of the rotated cube is

```
w_i=sum_k |U_ki|,       1<=w_i<=sqrt(n).
```

Translate its bounding box to `0<=y_i<=w_i`. Retain the original unit
cube through the affine coordinate identities and its original linear
inequalities. Translation changes only affine terms; the new Hessians
are `G_j=U^T H_j U`.

Choose

```
L_i=ceil(log2(w_i sqrt(n/lambda_i))),
h_i=w_i 2^(-L_i) <= sqrt(lambda_i/n),
y_i=A_i+rho_i,
A_i=w_i sum_(ell=1,...,L_i) 2^(-ell) beta_(i,ell),
beta_(i,ell) binary,      0<=rho_i<=h_i.
```

Every point of the bounding box is represented, including its upper
boundary via the all-one prefix and residual `h_i`. Empty prefixes
are allowed. Approximate each needed monomial using

```
y_i y_k = A_i y_k + rho_i A_k + rho_i rho_k.
```

The prefix products are sums of binary-times-bounded-continuous products;
each has its exact four-inequality linear formulation. For `i!=k`, use
the McCormick envelope for the residual product on
`[0,h_i] times [0,h_k]`. Its greatest absolute graph error is
`h_i h_k/4`. For a residual square use

```
t>=0,       t>=2h_i rho_i-h_i^2,       t<=h_i rho_i,
```

which contains its graph with greatest absolute error `h_i^2/4`.
Share one approximate value of each monomial across all outputs.

Because each output is `(1/2)sum_(i,k) G_(j,ik)y_i y_k` plus its
exact affine part, its total absolute error is at most

```
(1/8) sum_(i,k) |G_(j,ik)| h_i h_k
 <= (1/(8n)) sum_(i,k) |G_(j,ik)| sqrt(lambda_i lambda_k)
 <= (1/8) ||diag(sqrt(lambda)) G_j diag(sqrt(lambda))||_F
 =  (1/8) sqrt(tr(H_j P H_j P))
 <= epsilon_j/8 <= epsilon_j.                           (4)
```

The penultimate inequality uses the Cauchy-Schwarz estimate that the
entrywise absolute sum of an `n` by `n` matrix is at most `n` times
its Frobenius norm. The error margin is intentional and avoids special
cases in dimension one. Exact graph points remain feasible by setting
the residual monomials to their exact values.

Finally,

```
p=sum_i L_i
 <= -(1/2)sum_i log2 lambda_i
    +sum_i log2 w_i +(n/2)log2 n+n
 <= Phi+n log2 n+n.
```

Each coordinate bit participates in at most `O(n)` exact binary
products; residual monomials use `O(n^2)` rows and output equations
use at most `O(mn^2)` coefficients. This proves the stated compactness
and the upper bound. No explicit enumeration of all grid cells occurs.

## Weighted graph precision is an exact special case of the determinant problem

For a graph with one output `x_i x_k` on each edge, the Hessian has
ones in entries `(i,k)` and `(k,i)`. Direct multiplication gives

```
tr(H_(ik) P H_(ik) P)=2(P_ii P_kk+P_ik^2).
```

Replacing a feasible `P` by its diagonal preserves the matrix cap,
does not increase any energy, and does not decrease its determinant
by Hadamard's inequality. Thus a diagonal maximizer exists. Writing
`P_ii=2^(-2s_i)` gives precisely

```
Phi = min sum_i s_i
      subject to s_i>=0,
                 s_i+s_k>=log2(sqrt(2)/epsilon_(ik))
                 for every edge (i,k).
```

Negative edge right-hand sides are redundant. This is the same weighted
fractional vertex-cover allocation that occurs in the separate
[graph precision result](../results/bilinear-graph-binary-complexity.md),
with different dimension-only tolerance constants in the finite bounds.
For arbitrary quadratic systems the maximizing covariance can use a
rotation, so restricting to the original-coordinate diagonal is not
justified.

## What is and is not claimed

The determinant optimization need not be a convex optimization problem.
For example, with the off-diagonal two by two Hessian, diagonal positive
matrices have energy `2ab`; its sublevel sets are nonconvex. We claim
neither efficient global solution nor a rational construction for this
finite characterization. An arbitrary feasible positive definite `P`
still gives a certified binary upper bound by the displayed construction.

There is nevertheless useful convexity in the natural geometry of positive
definite matrices. If

```
P(t)=P_0^(1/2) exp(tA) P_0^(1/2),  A real symmetric,
```

then `log det P(t)` is affine in `t`. Diagonalize `A=V diag(a_i)V^T`
and put `C_j=V^T P_0^(1/2)H_jP_0^(1/2)V`. Direct multiplication gives

```
tr(H_j P(t) H_j P(t))
 = sum_(i,k) C_(j,ik)^2 exp[t(a_i+a_k)].                 (5)
```

Thus the energy is convex along each such geodesic; its logarithm is
also convex when `H_j!=0`, by the scalar log-sum-exp inequality. The
geodesic between `P_0` and `P_1` satisfies
`P(t)<= (1-t)P_0+tP_1`: conjugating reduces this to the scalar inequality
`d^t<=1-t+td` for the eigenvalues of `P_0^(-1/2)P_1P_0^(-1/2)`.
Consequently the cap `P<=I` and all energy sublevel sets are geodesically
convex. Every local maximizer of the determinant over the positive
definite feasible set is therefore a global maximizer, because a geodesic
to a better point would improve the affine log determinant immediately.

This is an elementary instance of established geodesic convex optimization
on positive definite matrices, not a claim that the geometry itself is
new; see Sra and Hosseini,
[Geometric optimisation on positive definite matrices](https://proceedings.neurips.cc/paper/2013/file/3948ead63a9f2944218de038d8934305-Paper.pdf).
Conditioning, finite precision, and iteration complexity still require
separate analysis before making an efficient algorithm claim.

The Frobenius constraint also has an ellipsoid interpretation: for
`d=P^(1/2)u`, `||u||_2<=1`,
`|d^T H_j d|<=||P^(1/2)H_jP^(1/2)||_F<=epsilon_j`.
Replacing Frobenius norm by operator norm changes the associated
determinant optimum by at most a dimension-dependent factor, using
`||M||_op<=||M||_F<=sqrt(n)||M||_op` and scalar rescaling of `P`.
Ellipsoid selection and Hessian-based anisotropic approximation are
established themes. Cao's 2007 paper derives interpolation metrics from
large ellipsoids in directional-derivative level sets
([primary publication](https://doi.org/10.1137/060667992)); Chen, Sun,
and Xu study optimal anisotropic interpolation and Hessian metrics
([open primary paper](https://www.math.uci.edu/~chenlong/Papers/Chen.L%3BSun.P%3BXu.J2006.pdf)).

The candidate contribution is the uniform finite equivalence between
this simultaneous quadratic geometry and the number of unrestricted
integer coordinates in arbitrary convex lifts, together with a compact
binary linear formulation. The initial bounded search did not locate
that equivalence. A broader novelty audit is still needed, particularly
against vector-valued anisotropic interpolation and entropy bounds.

## Verification

The independent audits are [first review](../notes/review-quadratic-weighted-covariance-precision.md)
and [second review](../notes/review-quadratic-weighted-covariance-precision-second.md).
Both passed after correcting the formulation-size notation to distinguish
the constructed binary count from its unknown minimum. The companion checker
`code/quadratic_rank/check_weighted_covariance.py` passed 576 projected
residual LP extrema, 216 rotated-cube representations, and 80 unequal
accuracy graph LP reductions. It also checks the covariance-energy
rotation identity and the constructed binary-count bound. Such finite
tests supplement the proof and do not establish novelty.

The [dimension-gap example](../notes/covariance-benchmark-dimension-gap.md)
shows that the `O(n log(n+1))` additive order is necessary for this
Frobenius determinant benchmark: one convex quadratic at unit tolerance
has `Phi=(n/4)log2 n` but `p_conv=(n/2)log2 n+O(n)`.

For [commuting Hessians](../notes/commuting-quadratic-covariance-reduction.md),
a determinant-preserving geodesic symmetry argument reduces the benchmark
to concave scalar allocation with linear constraints. A single Hessian
admits an explicit water-filling solution.
