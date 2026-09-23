# Independent review: Klee–Minty rank-one identity and one aggregate slab

Date: 2026-09-05. Verdict: PASS for the identity and reduction in
[the completed source draft](klee-minty-rank-one-slab-hardness.md).
The exact audited statement is recorded below.
Broad rank-one concave quadratic hardness and exponential Klee–Minty
shadows are known; this review establishes correctness, not priority of
the more restricted construction.

## Telescoping identity and its zero set

Let `0<epsilon<1/2`, set `x_0=0`, and impose

```
epsilon x_(j-1) <= x_j <= 1-epsilon x_(j-1), j=1,...,n.
```

Define

```
L(x)=x_n-(1-epsilon) sum_(i<n) epsilon^(2(n-i)-1) x_i,
F(x)=L(x)-x_n^2.
```

The claimed identity is exact:

```
F(x)=sum_(j=1)^n epsilon^(2(n-j))
       (x_j-epsilon x_(j-1)) (1-epsilon x_(j-1)-x_j).
```

Expand one product as
`x_j-x_j^2-epsilon x_(j-1)+epsilon^2 x_(j-1)^2`.
The weighted square terms telescope, leaving only `-x_n^2`.
The coefficient of `x_i` for `i<n` is
`epsilon^(2(n-i))-epsilon^(2(n-i)-1)`, which is exactly the
coefficient in `L`. The terminal linear coefficient is one.

Every factor is nonnegative on the Klee–Minty polytope, and every weight
is positive. Thus `F>=0`, with equality exactly when each variable
chooses one of its two local endpoint bounds. The bounds are distinct,
because every coordinate is in `[0,1]` and `epsilon<1/2`. Every endpoint
pattern yields a nonsingular triangular active system and a vertex;
conversely every vertex chooses one endpoint in every pair. Therefore
`F<=0` on this polytope selects exactly its vertices.

## Subset-sum reduction

Take positive integer weights `w_i` and integer target `B`, and let
`W=sum_i w_i>=1`. Choose `epsilon=1/(8W)` and add the single
aggregate slab

```
B-1/4 <= sum_i w_i x_i <= B+1/4.
```

At the vertex with bits `u_i`,
`x_i=u_i+(1-2u_i)epsilon x_(i-1)`, hence
`|x_i-u_i|<=epsilon`. The weighted sum differs from the corresponding
integer subset sum by at most `epsilon W=1/8`.

A subset summing to `B` therefore gives a vertex inside the slab. In the
other direction, `F<=0` forces a vertex, and membership in the slab gives

```
|sum_i w_i u_i-B| <= 1/8+1/4 = 3/8 < 1.
```

The expression inside the absolute value is an integer and must be zero.
This proves the exact equivalence. An empty slab intersection would
correctly remain a no-instance. The final draft strengthens the reduction
by restricting the source target to `0<=B<=W` and proving its slab
intersection is always nonempty. This proof passes: the all-one endpoint
pattern has weighted sum at least `W-1/8`; its segment with the feasible
zero point reaches each integer `B<W`, while for `B=W` that vertex
already lies in the slab. Thus every constructed minimum is attained
on a nonempty compact set and is positive, possibly extremely small,
for no-instances.

The objective Hessian has only one nonzero entry, `-2` in the last
coordinate, so it is negative semidefinite of rank one. Its linear
coefficients have `O(n log W)` bits each. The local linear polytope has
a 2VPI path description, with two opposing inequalities on one global
aggregate added. The quadratic condition has its own dense linear part.
Consequently the complete constraint graph must not be described as a
path. The final draft makes both qualifications explicit.
All construction lengths are polynomial in the subset-sum input.
This proves ordinary NP-hardness for this structured concave quadratic
class. It does not establish strong hardness, since the reduction uses
binary subset-sum weights and weight-dependent rational coefficients.

The particular constructed decision family is also in NP directly:
guess the endpoint bits, compute their rational vertex recursively, and
check the slab exactly. Its coordinates have polynomial encoding length.
For a broader bounded class with arbitrary rational linear rows and a
single nonlinear coordinate in the objective, the reviewed fixed-
parameter linear-fiber NP lemma gives the corresponding upper bound.
The NP-hardness argument alone should not be presented as a claim that
all rank-one nonlinear formulations automatically have the same encoding.

## A direct parabolic shadow consequence

Put `c_i=(1-epsilon)epsilon^(2(n-i)-1)` for `i<n` and `c_n=0`.
At a vertex with terminal coordinate `t`, the identity gives
`c^T x=t-t^2`. At every feasible point, it gives `L(x)>=x_n^2`.
Thus for the objective with parameter `lambda=2t-1`,

```
c^T x+lambda x_n = 2t x_n-L(x)
                 <= t^2-(x_n-t)^2 <= t^2.
```

Equality requires both `F=0` and `x_n=t`. Distinct endpoint patterns
have distinct terminal coordinates: the final bit is distinguished by
the disjoint intervals `[0,epsilon]` and `[1-epsilon,1]`, after which
the previous coordinate is recovered recursively. Hence this objective
uniquely exposes the chosen vertex. This supplies an elementary proof
that all `2^n` vertices survive a two-dimensional shadow, with explicit
parameter witnesses in `[-1,1]`. It is an alternative proof and a changed
projection vector, not a claim that exponential shadows themselves are
new. The earlier primary source is
[Gärtner et al., Section 4](https://arxiv.org/pdf/1308.2495).

## Exact checks

[exact_rank_one_slab_check.py](../code/parametric_path_lp/exact_rank_one_slab_check.py)
uses rational arithmetic. It passed 2,246 identity, strict-interior
positivity, and unique tangent-objective checks through dimension ten.
It also checked 661 subset-sum targets on 28 weighted instances through
dimension seven, including targets at zero, at total weight, and outside
the feasible sum range. These checks agree with the proof above; no
floating-point tolerance is used.

## Fixed local coefficients by padding

The subsequent Section 2.1 passes as well. Fix `epsilon=1/4` and
choose the least nonnegative integer `r` with `4^(r+1)>=8W`.
Then `r=O(log W)`. Put `r` padding variables between consecutive
free variables and bound each padding variable above by `1/2`.
The entire path has `N=n+(n-1)r` variables and ends at a free variable.

The same telescoping identity on all `N` variables still gives `F>=0`
and forces endpoint choices at every zero. An upper endpoint is at
least `1-epsilon=3/4`, so a padding coordinate's singleton upper bound
excludes that choice. Its flow is therefore exactly one quarter of its
predecessor. The next free variable has recurrence

```
x_free = u + (1-2u) 4^(-(r+1)) x_previous_free.
```

The first free variable equals its bit exactly. Every subsequent free
coordinate differs from its bit by at most `4^(-(r+1))<=1/(8W)`.
Conversely every free-bit pattern extends by choosing the lower branch
on all padding positions, whose values are at most `1/4` and hence
satisfy their singleton bounds. Thus the same weighted rounding proof
establishes equivalence with subset sum.

For the nonempty-feasible-set promise, the all-free-one, all-padding-zero
endpoint pattern has weighted free-coordinate sum at least `W-1/8`.
Its segment to zero remains feasible for every local path and singleton
bound. This is exactly the convex interpolation needed for targets
`B<W`; the endpoint itself covers `B=W`.

All local coefficients are now from `{0,+/-1,+/-1/4}` and local
right-hand sides from `{0,1/2,1}`. Padding does not add edges to the
local path graph. Its size and all objective encodings are polynomial:
the objective's largest denominator exponent is linear in `N`.
The dense aggregate weights and objective coefficients still depend on
the instance, so ordinary NP-completeness remains the justified claim.
The original free bits are a polynomial certificate; padding choices
are determined and need not be guessed.

The exact checker was extended with 1,016 padded endpoint-pattern
identities and 661 fixed-coefficient slab target comparisons on the
same 28 weighted instances. It also checks that choosing an upper branch
at a padding position violates its singleton bound. All checks pass.
