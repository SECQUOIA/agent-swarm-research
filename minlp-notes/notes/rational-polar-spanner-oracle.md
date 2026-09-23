# Exact-feasible rational spanners from weak optimization and polar separation

Date: 2026-09-05. Status: independently reviewed supporting oracle lemma.
The [first full audit](review-rational-polar-spanner-oracle.md) and
[second full audit](review-rational-polar-spanner-oracle-second.md) passed.

This note supplies a fixed-bit implementation of a classical approximate
barycentric-spanner construction. It covers both a linear image of the
positive part of a polar body and an effective lower-dimensional primal
body. Its purpose is to prevent precision growth across successive oracle
calls and ensure that every returned vector is exactly feasible.

The imported optimization result is Grötschel, Lovász and Schrijver,
[*The ellipsoid method and its consequences in combinatorial optimization*](https://ir.cwi.nl/pub/10046/10046D.pdf),
Definition (5) on printed page 172 and Theorem (3.1) on page 177. For a body
with a rational weak separation oracle and explicit rational inner and
outer balls, it returns a rational `z` with

```
dist(z,P)<=eta,       d^T z>=max_(x in P) d^T x-eta.       (A)
```

The comparison is with all of `P`, as stated in that definition. Known
inner balls will turn its approximate feasibility into exact feasibility.
The source states its body convention for dimension at least two. In
dimension one, apply it to `P times [-1,1]` with objective `(d,0)`, center
`(c,0)`, inner radius `min(sigma,1)`, and outer radius `R_0+1`.
Projecting the returned point preserves (A) and polynomial complexity.

## 1. Generic spanner theorem

Let `P subset R^n` be a compact convex body with a rational weak separation
oracle of polynomial query and output complexity. Suppose the input gives
rational `c,sigma,R_0`, with `0<sigma<=R_0`, such that

```
B_2(c,sigma) subset P subset B_2(c,R_0).
```

Let `V` be rational `n by r`, with `r>=1`. The desired image is
`T={lambda^T V: lambda in P} subset R^r`. Assume explicit rational seeds
`lambda_1,...,lambda_r in P` are supplied such that their image rows form
an invertible matrix `B_0`. Write `Delta_0=|det B_0|>0`.

There is a deterministic polynomial-time algorithm returning rational
`lambda_1,...,lambda_r in P` such that their image-row matrix `B` is
invertible and every `t in T` has

```
t=sum_i alpha_i B_i,       |alpha_i|<=9/4<3.              (B)
```

Every output is exactly feasible. Total running time and output encoding
are polynomial in the body-oracle encoding, balls, `V`, and seeds. No exact
linear-optimization oracle or rational-polytope assumption is required.

### Uniform bounds before starting the exchanges

Choose the following positive rational bounds, all computable from the input:

```
Z=1+sum_i |c_i|+R_0,
M=1+sum_(i,j) |V_ij|,
W=1+n M Z,
U=1+r! W^(r-1)/Delta_0,
L=1+n M U.
```

Every image coordinate has magnitude at most `W`. During determinant-increasing
exchanges, the absolute determinant never falls below `Delta_0`. Cofactor
bounds therefore imply that every entry of the inverse image-row matrix has
magnitude at most `U`.

To optimize the `i`-th representation coefficient, the relevant linear
objective in the original body is

```
d_i=V B^(-1)e_i.
```

Its `l_1` norm is at most `L`, for every exchange stage; the same holds for
its negative. All displayed bounds have polynomial bit length, even when
`r` varies. They depend only on the initial input, not on denominators
generated later by the oracle.

### One fixed rational grid for all returned vectors

Choose one positive dyadic number `delta` so small that

```
2n delta<=1,
n delta [1+L+2L(R_0+1)/sigma]<=1/4.                      (C)
```

The necessary dyadic precision is polynomial in the input bit length.
For any objective `d` with `||d||_1<=L`, run (A) with `eta=n delta`.
Round every coordinate of its output `z` to a multiple of `delta`, producing
`q` with coordinate errors at most `delta`. Set

```
epsilon=2n delta,
lambda=(sigma q+epsilon c)/(sigma+epsilon).              (D)
```

Since `dist(q,P)<=epsilon`, choose `x in P` with `||q-x||<=epsilon`.
Formula (D) is the convex combination

```
sigma/(sigma+epsilon) * x
+epsilon/(sigma+epsilon) * [c+(sigma/epsilon)(q-x)].
```

The bracket lies in the known inner ball, so `lambda in P` exactly. Also
`||c-q||<=R_0+epsilon<=R_0+1`. Hence

```
||lambda-z||_2
 <=n delta+2n delta(R_0+1)/sigma,

max_(x in P)d^T x-d^T lambda
 <=n delta+L[n delta+2n delta(R_0+1)/sigma]
 <=1/4.                                                  (E)
```

Thus (D) is an exact-feasible additive-`1/4` linear optimizer.

The grid and repair weight are fixed before any exchange. Every `q` has
denominator `1/delta` and bounded coordinates, and (D) uses only the fixed
rational data `c,sigma,epsilon`. All possible returned `lambda` therefore
have a common rational denominator of polynomial encoding and uniformly
bounded numerators. Include the finitely many seed denominators when making
this statement about all possible bases. This avoids a recursive increase
of arithmetic precision across successive optimization calls.

### Exchange and termination

For every basis position `i`, optimize both `d_i` and `-d_i` using (D).
If any returned vector has representation coefficient of magnitude greater
than two in that position, replace that basis row by its image. A row
replacement multiplies the absolute determinant by that coefficient, so
the determinant more than doubles.

If no replacement is found, (E) implies that both the maximum positive and
negative values of every representation coefficient are at most `2+1/4`.
This proves (B). A returned vector is not merely approximately feasible;
the final basis vectors belong to `T` themselves.

Hadamard's elementary permutation bound gives `|det B|<=r! W^r`. Thus the
number of exchanges is at most

```
1+ceil(log2(r! W^r/Delta_0)).
```

This is polynomial in the input length. Every current basis entry has
polynomial bit length because of the fixed output denominator; its exact
inverse and every subsequent objective also do. All weak-optimization calls,
rounding steps, comparisons, and row exchanges consequently have a uniform
polynomial bit bound. It would not suffice merely to assert that each oracle
call is polynomial in its current input without this precision control.

## 2. Exactly feasible support optimization on a strongly separated body

Let `K subset R^m` have a rational strong separation oracle and known rational
radii `0<rho<=R` such that

```
rho B_2^m subset K subset R B_2^m.
```

No symmetry is needed in this section. Given a rational direction `a` and
positive rational error `tau`, we can return a rational `x in K` satisfying

```
a^T x<=h_K(a)<=a^T x+tau.                                (F)
```

Indeed, choose positive rational `eta<=1` with

```
eta[1+||a||_1(R+1)/rho]<=tau.
```

Apply (A) to `K` and direction `a`, and repair its output by
`x=rho z/(rho+eta)`. The same inner-ball convex combination as above proves
exact feasibility. Since `||z||<=R+eta<=R+1`, the loss relative to the
support optimum is at most `eta+||a||_1 eta(R+1)/rho`. This proves (F)
with polynomial rational encoding and running time. The zero direction can
return zero immediately.

## 3. A weak separator for the positive polar

Define

```
P=K^circ intersect R_+^m
 ={lambda>=0: h_K(lambda)<=1}.
```

Choose a positive dyadic `a<=min(1,1/(8Rm))` and put

```
c=a 1,     sigma=a/2,     R_0=1/rho+m a.
```

These are an explicit inner and outer ball for `P`. Nonnegativity has a
margin of at least `a/2` on `B(c,a/2)`, and every point there has norm less
than `1/R`, so its `K` support is at most one. Conversely `P subset
(1/rho)B_2`, giving the outer ball centered at `c`.

Here is a rational weak separation oracle for `P` at a rational query
`lambda` and requested distance accuracy `eta>0`.

1. If a coordinate is outside `[0,1/rho]`, return the corresponding exact
   coordinate separator, which is valid for `P`.
2. Otherwise `||lambda||_2<=m/rho`. Set
   `tau=eta/[2(1+m/rho)]` and use (F) to find `x in K` with
   `h_K(lambda)<=lambda^T x+tau`.
3. If `lambda^T x>1`, return the valid separating inequality
   `x^T mu<=1`. Its normal is nonzero and rational. Rescale by its nonzero
   infinity norm if the weak-separation convention requires norm at least
   one.
4. Otherwise `h_K(lambda)<=1+tau`, and
   `lambda/(1+tau)` belongs to `P`. Its distance from the query is at most
   `tau||lambda||<=eta/2`. Return the corresponding weak-membership answer.

Every separation branch is valid on the entire exact body. Every membership
branch certifies a genuine nearby feasible point. The support oracle is
invoked at polynomial-bit accuracy, so this weak separator has polynomial
query and output complexity. It requires no strong separation oracle for
the polar itself.

## 4. Positive scalarizations of a rational image

Let `V` be rational `m by r` of full column rank. Select `r` independent
rows with indices `j_1,...,j_r` by rational elimination. For the positive
polar above, the exact rational vectors

```
lambda_s=2a e_(j_s)
```

are feasible: their norms are at most `1/R`, so their `K` support is at
most one. Their image rows are `2a` times the independent rows of `V`.
They give explicit seeds with nonzero rational determinant and polynomial
bit encoding.

Apply the generic theorem to the weak separator from section 3. It returns
positive scalarization weights `lambda_s>=0`, all satisfying
`h_K(lambda_s)<=1` exactly, whose projected rows form a `9/4`-approximate
barycentric spanner of

```
{lambda^T V: lambda>=0, h_K(lambda)<=1}.
```

Their coefficients, feasibility, and running-time guarantees are uniform
and rational. The image need not contain a neighborhood of zero: the
algorithm works in the full-dimensional original positive-polar body, while
the explicit seeds certify the image span.

## 5. Application to an effective primal body

With the same full-column-rank `V`, let

```
K_eff={z in R^r: Vz in K}.
```

A rational left inverse `J` of `V` is computable by elimination. Set

```
sigma_eff=rho/(1+sum|V_ij|),
R_eff=R(1+sum|J_ij|).
```

Then `sigma_eff B_2^r subset K_eff subset R_eff B_2^r` by the elementary
operator-norm bounds. A strong separator for `K_eff` is obtained by querying
the `K` oracle at `Vz` and pulling its separating normal back through `V`.
A violated pulled-back normal cannot vanish because zero belongs to `K_eff`.

The generic theorem applies with original body `K_eff`, image matrix `I`,
center zero, and exact seeds `sigma_eff e_i`. It therefore constructs an
exact-feasible rational `9/4`-approximate barycentric spanner of `K_eff` in
polynomial time and bit complexity. If `K` is centrally symmetric, so is
`K_eff`; in that case a basis matrix with these vectors as columns gives
the usual contained crosspolytope and outer parallelotope used in geometric
approximations.

## Attribution and limits

The determinant-exchange barycentric-spanner mechanism is established;
see Awerbuch and Kleinberg, section 2.3, especially Propositions 2.2 and 2.4
in the [primary author manuscript](https://www.cs.cornell.edu/~rdk/papers/OLSP.pdf).
Weak separation and optimization equivalence is the cited GLS theorem.
Central-ball feasibility repair is already used in the repository's
[reviewed rational log-product oracle](rational-log-product-convex-body-oracle.md).

This note assembles those ingredients with explicit positive-polar access
and a fixed output grid for use in graph-precision constructions. It does
not claim a new general spanner algorithm, a strongly polynomial running
time, exact linear optimization, or an implicit strong oracle for the polar.

The [second reviewer's exact checker](../code/quadratic_rank/check_rational_polar_spanner_second.py)
checks 16 generic systems, 93 repaired calls, 11 determinant exchanges,
120 full-image vertex bounds, and 347 positive-polar cases. These tests
supplement the general oracle and conditioning proofs.
