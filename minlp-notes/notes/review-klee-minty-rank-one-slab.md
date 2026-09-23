# Independent review: rank-one concave quadratic on a path with one slab

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the identity and SUBSET SUM reduction pass this independent
audit.** I also checked the completed
[written draft](klee-minty-rank-one-slab-hardness.md), including its
fixed-core consequence and parabolic exposing certificate. The formulas
reviewed here are written explicitly below. The restricted family is ordinarily NP-complete;
neither strong hardness nor novelty of general rank-one quadratic
minimization follows from this audit.

Let `x_0=0`, `0<epsilon<1/2`, and impose

```
epsilon*x_(j-1) <= x_j <= 1-epsilon*x_(j-1), j=1,...,n.
```

These are the Klee-Minty scalar path inequalities. They imply
`0<=x_j<=1`. Define

```
L(x)=x_n-(1-epsilon)*sum_(i<n) epsilon^(2(n-i)-1)*x_i,
f(x)=L(x)-x_n^2.
```

The claimed identity is exact:

```
f(x)=sum_(j=1)^n epsilon^(2(n-j))
       *(x_j-epsilon*x_(j-1))*(1-epsilon*x_(j-1)-x_j).
```

Indeed each unweighted product expands to
`x_j-x_j^2-epsilon*x_(j-1)+epsilon^2*x_(j-1)^2`.
After weighting, every square except `-x_n^2` cancels. For `i<n`,
the remaining linear coefficient is
`epsilon^(2(n-i))-epsilon^(2(n-i)-1)`, exactly the coefficient in `L`.

Every summand is nonnegative on the path polytope and has positive
weight. The sum vanishes if and only if every variable takes one of its
two path bounds. Their gap is strictly positive, and every such bound
selection is the unique vertex indexed by a bit vector `u`, recursively
`x_j=u_j+(1-2u_j)epsilon*x_(j-1)`. Thus `f>=0`, with zero set exactly
the original cube vertices. The Hessian of `f` is `-2 e_n e_n^T`, so
it is a concave quadratic with precisely one negative eigenvalue.

For positive integer SUBSET SUM weights `w_i`, write `W=sum w_i`,
choose `epsilon=1/(8W)`, and add the single scalar aggregate interval

```
B-1/4 <= sum_i w_i*x_i <= B+1/4.
```

At a cube vertex, `|x_i-u_i|<=epsilon`, hence its weighted rounding
error is at most `1/8`. If the bits sum to target `B`, that vertex is
inside the slab and has objective zero. Conversely, if a slab-feasible
point has objective at most zero, nonnegativity forces it to be a cube
vertex. Its integer weighted bit sum differs from `B` by at most
`1/8+1/4=3/8`, and therefore equals `B`. This proves the exact decision
equivalence. A slab consists of two parallel dense inequalities; the
argument does not replace it by one one-sided dense inequality.

For targets `0<=B<=W`, the clipped polytope is always nonempty. The
zero vertex has weighted sum zero. The all-one-bit vertex has weighted
sum at least `W-1/8`. Convexity supplies every intermediate sum; for
the endpoint `B=W`, that all-one-bit vertex itself lies in the slab.
Thus the reduction can promise a nonempty compact feasible polytope,
including on no instances. Targets outside this interval are trivial
SUBSET SUM no cases and need not be part of the hard source family.

All data have polynomial binary size: powers of `epsilon` have exponents
at most `2n`, while `log W` is polynomial in the source input length.
A yes certificate can be the bit vector itself; its recursively defined
rational vertex has polynomial coordinate encoding length, and the slab
and quadratic objective can be checked exactly. More generally, a
concave quadratic over a bounded rational polytope attains a minimum at
a rational vertex of polynomial encoding length. Either argument gives
the required NP upper bound for this restricted decision family.

This result concerns a two-variable-per-row scalar path plus one dense
aggregate interval, and a linear objective term minus the square of a
single endpoint coordinate. The path alone has minimum zero trivially.
The global aggregate is essential in this reduction. Broad hardness of
rank-one concave quadratic minimization was already known; priority of
this precise structural restriction requires separate comparison. The
weight-dependent small coefficients do not establish strong hardness.

The completed draft's fixed-core consequence is correctly qualified.
Fixing `x_n` leaves a linear system, but its local path variables are
coupled. The slab and dense linear part of the objective use a fixed
number of global aggregates. The resulting hard family therefore rules
out replacing independent blocks in the constructive theorem by general
scalar path-coupled blocks while retaining a generic polynomial guarantee.
It does not call the entire constraint graph a path.

The additional parabolic exposing proof also passes. At every cube
vertex, `L=x_n^2`. Distinct vertices have distinct endpoint coordinates:
the two endpoint branches occupy disjoint intervals, and within a branch
the recurrence is invertible, so induction recovers every previous bit.
For a vertex endpoint `t`, the objective `2t*x_n-L` is at most
`t^2-(x_n-t)^2` throughout the polytope. Equality forces both zero
certificate slack and the same endpoint, hence the unique vertex.
This proves the stated exponential shadow with the displayed alternate
projection coefficients and parameter interval. It is a correct
alternative certificate for an already established shadow phenomenon;
separate novelty is not asserted by this review.

## Independent exact validation

I wrote [an exact checker](../code/quadratic_rank/check_klee_minty_slab_review.py).
It verifies the polynomial identity symbolically for dimensions one
through six. It also solves 72 independently generated clipped-cube
quadratic programs exactly, through dimension seven, using rational
arithmetic.

The continuous optimization check enumerates every original cube vertex
inside the slab and every original cube edge's intersections with the
two slab boundaries. These are all vertices of the clipped polytope:
a new vertex on one cutting hyperplane must lie on an original edge,
and the two distinct parallel slab boundaries cannot both be active.
The concave objective reaches its minimum among these candidates.
All 2,784 candidate vertices gave nonnegative objective, and the exact
minimum was zero if and only if independent enumeration found a subset
of the source weights summing to the target. All checks passed.

## Fixed local coefficients by padding

The author's additional padding corollary also passes this independent
audit. Fix `epsilon=1/4`. Between consecutive free coordinates insert
`L` padding coordinates, choosing `4^(-(L+1))<=1/(8W)`, and bound each
padding coordinate above by `1/2`. Use the same telescoping objective
on all `N=n+(n-1)L` coordinates, and apply the source slab only to the
free coordinates.

The objective remains nonnegative on the unrestricted path polytope.
If it vanishes, every coordinate chooses a path endpoint. An upper
endpoint is at least `3/4`, since the preceding coordinate is at most
one. Thus a padding coordinate cannot use its upper endpoint; it must
equal one quarter of its predecessor. After `L` such steps, a free
coordinate has recurrence

```
y_i=u_i+(1-2u_i)*4^(-(L+1))*y_(i-1).
```

The first free coordinate is its bit exactly. Therefore every free
coordinate differs from its bit by at most `4^(-(L+1))`, and the
weighted error is at most `1/8`. Every free bit vector extends by
choosing all padding endpoints low; each padding value is at most
`1/4`, so its added bound is satisfied. Both directions of the previous
slab reduction follow unchanged.

The feasible local polytope is convex and contains zero and the vertex
with every free bit one and every padding branch low. Its weighted
free sum at the latter point is at least `W-1/8`, preserving the
nonempty-slab proof for every target in `[0,W]`. Choosing minimal `L`
uses `O(log W)` padding coordinates per gap. The resulting dimension
and all objective coefficient bit lengths are polynomial in the source
encoding; the final coordinate is free, so the Hessian still has rank
one in that endpoint.

Local inequality coefficients now belong to
`{0,1,-1,1/4,-1/4}` and their right-hand sides to `{0,1/2,1}`.
The global slab weights and the small coefficients of the linear
objective part remain encoded in binary. This is an ordinary
NP-completeness refinement fixing local path data; it does not establish
strong hardness or remove the global aggregate.
