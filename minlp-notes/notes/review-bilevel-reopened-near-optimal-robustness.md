# Independent review: near-optimal response robustness

Date: 2026-09-07. Reviewer: independent subagent `nearoptimal_review1`.
Author of reviewed draft: root agent. Disposition: **the structural theorem and
attainment subclass are correct under the stated encoding and fixed-dimension
assumptions**. No substantive proof defect found. This is a proof review, not a
claim of novelty or a fresh independent audit of every previously promoted
dependency.

Reviewed the full [draft](bilevel-reopened-near-optimal-robustness.md), the full
[block response theorem](../results/bilevel-fixed-block-response-algorithm.md),
the full [moving-normal and pessimistic extension](../results/bilevel-compressed-response-infimum-semantics.md),
and the full [scalar response theorem](../results/bilevel-fixed-aggregate-response-algorithm.md).

## Proof judgment

The essential projection argument is sound. Fixing `t=T(x)z` adds at most `h`
shared equality rows. The enlarged leader parameter `(x,t)` has fixed dimension,
the local positive-definite quadratic matrices retain their positivity, and all
new coefficients are explicit polynomials of polynomial actual degree. Existing
compression therefore applies to the measurement fibers, including dependent
measurement rows, rank-changing rows, and empty fibers. An empty fiber has no
feasible KKT candidate and contributes no point to its minimum graph; there is no
vacuous universal comparison admitting an empty fiber because a candidate is
required before the comparison.

The distinction between a measurement-fiber optimum and an unrestricted follower
stationary point is crucial and handled correctly. A near-optimal adversary need
not be unrestricted-stationary. Its measurement can nevertheless be reproduced
by a global minimum on that measurement fiber, whose cost is no greater. The
converse follows from feasibility of the reconstructed fiber minimum. Nonconvex
aggregate costs cause no gap: polyhedral KKT necessity holds at global minima,
and comparing against all feasible KKT candidates excludes nonglobal candidates
when a minimum graph is needed. Degeneracy and failure of constraint qualification
do not invalidate the polyhedral normal-cone argument.

In fact the fiber construction can be simplified: if `K_T(x,t,u)` denotes the
graph of objective values of feasible fiber KKT candidates, then

```
exists z in Z_delta(x) with T(x)z=t
  iff exists u: K_T(x,t,u) and u<=v(x)+delta(x).
```

The forward direction chooses a global fiber minimum, and the reverse direction
only needs the represented KKT candidate to be feasible. Thus a global comparison
is required for the nominal value `v(x)`, but not for each measurement fiber.
Using the stronger `M_T` minimum graph in the reviewed draft remains correct.
This optional simplification was sent to the author.

The bit-complexity statement survives the extension. A rational bounding box for
the measurement parameters has polynomial encoding length by fixed-dimensional
polynomial optimization/root bounds on the compact leader set and the supplied
polynomial coordinate bounds. There are polynomially many local active subsets
and response regimes. Products of their polynomial denominators and substitution
of the explicit upper polynomials have polynomial degree, coefficient bit length,
and expanded size because the ambient compressed dimension is fixed. This would
fail for unrestricted binary-encoded exponential degree, which the draft excludes.

Independently varying measurement matrices across a growing number of criteria
cause no dimension leak. The draft eliminates each criterion separately, yielding
quantifier-free formulas in the same fixed tuple `(x,v,q)` before combining them.
Consequently all criteria share the unique true nominal value, and the final
formula has polynomial length with fixed total variable count. Their collective
measurement rank need not be bounded. Nonemptiness of the nominal graph prevents
vacuous robust feasibility when no follower is feasible.

The exact infimum and attainment logic is valid even when response graphs are
discontinuous. Worst values exist at each feasible leader by compactness of the
near-optimal set; they are bounded over all leaders by the uniform boxes. A
bounded nonempty univariate semialgebraic value set has an algebraic infimum,
and membership decides attainment. For common-field witness recovery, sample the
leader, nominal value, worst criterion value, measurement, and compressed fiber
response simultaneously with the infimum condition. The number of copies is
fixed. Rational reconstruction of all local blocks stays in that one field and
does not form a compositum of independently generated algebraic responses.

The unconditional-attainment subclass is also correct. With fixed full constraint
normals, Hoffman's bound gives lower semicontinuity of feasible fibers relative
to the closed feasible-leader set; uniform boxes give upper semicontinuity. A
convex aggregate plus the positive-definite local quadratic terms gives strict
convexity of the full follower objective. Hence its unique minimizer and value
are continuous. For positive budgets, a small convex mixture toward that minimizer
has strict budget slack and survives nearby feasible-fiber repairs. At zero
budgets the singleton minimizer itself supplies the lower-continuity sequence,
including when nearby budgets are positive. Closed graph supplies upper
continuity. Thus each robust criterion maximum is continuous; robust feasibility
is closed and minimization on the compact feasible set attains its optimum.

## Additional exact boundary: a positive budget does not cure nonattainment

The draft invokes zero-budget examples to show the necessity of its general
attainment decision. The following example strengthens that warning to a constant
strictly positive budget, with fixed normals and a unique nominal follower.
It is a diagnostic example; no novelty claim is made for this mechanism.

Let `x in [0,1/16]`, `z in [0,1]`, `delta=1/16`, and set

```
h(z)=3z^2-2z^3,
f(x,z)=z^2(1-z)^2+(delta+x)h(z),
G(x,z)=4x+z.
```

Both summands of `f` are nonnegative, and for `z>0` the second is positive,
so the unique nominal minimizer is `z=0`, of value zero. This cost fits the
theorem with one scalar quadratic block, aggregate `w=z`, and
`phi(x,w)=f(x,w)-w^2/2`.

Writing `f0(z)=f(0,z)`, exact factorization gives

```
f0(z)-delta=(z-1)^2(16z^2-2z-1)/16.
```

For `a=(1+sqrt(17))/16<1/3`, the near-optimal set at zero is `[0,a] union {1}`.
For each `x>0`, adding `x h(z)>0` excludes every `z in (a,1]`. On `[0,a]`,

```
f0'(z)=z(4z^2-51z/8+19/8)>z/4       for z>0,
h'(z)=6z(1-z)>=0.
```

Thus there is a unique `a_x in (0,a)` with `f(x,a_x)=delta`, and the near-optimal
set is exactly `[0,a_x]`. Continuity and uniqueness give `a_x -> a` as `x -> 0+`.
Since `h(a_x)<a_x`,

```
x h(a_x)=f0(a)-f0(a_x)>(a-a_x)a_x/4,
```

so `a-a_x<4x`. The worst objective therefore satisfies `W(0)=1` and
`W(x)=4x+a_x>a` for all positive `x`, while `W(x)->a` as `x->0+`.
The infimum `a` is unattained. A strictly positive budget alone does not repair
the loss of lower semicontinuity caused by a secondary local minimum entering
the cost sublevel set at its exact boundary.

## Executable checks and disposition

[Independent exact checks](../code/bilevel_reopened/nearoptimal_review_checks.py)
verify the positive-budget factorization and inequalities, a two-coordinate
quadratic measurement fiber whose worst response is not unrestricted-stationary,
exclusion of a nonglobal stationary nominal candidate, an empty measurement fiber
at a rank-changing constraint, and a zero-budget convex limiting example.
The checks support the proof and do not substitute for it.

Run outcome: all five checks passed with exact SymPy arithmetic. Minor editorial issue sent to the author:
`shared linear inequalities/inequalities` should read `equalities/inequalities`.
No theorem correction is required. Promotion should additionally wait for the
separate literature comparison and the author's integration of independent reviews.

Cross-check of reviewer 2's simpler feasibility example: replacing the parameter
by `x in [delta,1/8]`, the cost by `z^2(1-z)^2+x h(z)`, and imposing the robust
upper row `z<=1/2` gives exactly `D=(delta,1/8]`. At `x=delta`, the admissible
response `z=1` violates the row. For every `x>delta`, all near-optimal responses
lie in `[0,a]` by the same factorization and strict positivity of `h` on `(0,1]`,
so the row holds. Minimizing `x` therefore has unattained infimum `delta`.
This confirms the second reviewer's example independently.

## Integration reread

Reread the integrated KKT threshold simplification, both positive-budget examples,
and the Max-Cut boundary. All arguments are valid. One local wording correction
was sent to the author: the claim that `f_c` has a unique interior maximum
requires `c<1/3`, whereas the surrounding introductory sentence allowed all
`c>=delta`. Both applications use only `c in [delta,1/8]`, so restricting that
introductory parameter range fixes the sentence without changing either example.
For larger `c`, monotonicity can replace the interior-maximum argument.

The Max-Cut transfer is correct: budget `N/2` includes the whole unit cube for
the diagonal quadratic follower; the stated convex quadratic upper objective
has a vertex maximizer, and at vertices it is the cut size. Threshold `K-1`
correctly makes universal feasibility the complement of `MaxCut>=K`. This
establishes the need for a structural upper-criterion restriction and does not
conflict with the polynomially many separately checked affine rows.
