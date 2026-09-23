# Exact structural optimization against near-optimal follower responses

Date: 2026-09-07 (UTC). Status: two independent full proof audits passed,
including the positive-budget nonattainment and upper-criterion hardness
boundaries below. Publication priority remains qualified by the source search.

Near-optimal-response robustness is an established bilevel model. The proposed
contribution here is an exact polynomial bit-time algorithm for many follower
variables with fixed-dimensional quadratic blocks, aggregate coupling, and shared
resources. The aggregate cost may be nonconvex. The proof uses the repository's
existing response compression on affine measurement fibers. It does not assume
that a near-optimal response is stationary.

## 1. Model and statement

Use the follower model of the [quadratic block theorem](bilevel-fixed-block-response-algorithm.md)
and its [moving-normal extension](bilevel-compressed-response-infimum-semantics.md).
The leader `x` ranges over a compact rational semialgebraic set `X` of fixed
dimension `r`. The follower vector consists of arbitrarily many local blocks of
dimension at most fixed `d`, with polynomially specified local polyhedral sets,
uniform polynomial coordinate bounds, and a fixed number `k` of shared linear
equalities/inequalities. All local and shared constraint normals may depend
polynomially on `x`. Denote this compact, possibly empty fiber by `P(x)`.

The follower cost is

```
f(x,z) = sum_b [z_b^T Q_b(x) z_b / 2 + c_b(x)^T z_b]
           + phi(x,U(x)z),
```

where each local symmetric matrix `Q_b(x)` is positive definite, `U(x)` has a
fixed number `s` of rows, and `phi` is a polynomial, not necessarily convex.
Rational polynomials use explicit monomial lists and degrees polynomially bounded
by the encoding length, as in the existing theorem. Dense or unary-degree data
are included; sparse binary degrees of exponential numerical size are excluded.

For every feasible leader define

```
v(x) = min {f(x,z): z in P(x)},
Z_delta(x) = {z in P(x): f(x,z) <= v(x)+delta(x)},
```

where `delta(x)>=0` is a rational polynomial supplied with the input. The budget
may itself be a bounded leader coordinate. A leader with `P(x)` empty is never
admissible. For a feasible leader, `Z_delta(x)` is nonempty and compact.

Each upper criterion `j`, including the objective `j=0`, has the form

```
G_j(x,z) = p_j(x,T_j(x)z),
```

where `p_j` and the matrix `T_j` are rational polynomials, and `T_j` has at most
fixed `h` rows. Different criteria may use different matrices; the total number
of criteria is unrestricted. Every affine upper criterion is included with
`h=1`. Fixed-rank quadratic or polynomial measurement criteria are also included.

The robust leader problem is

```
D = {x in X: P(x) nonempty,
             G_j(x,z)<=0 for all z in Z_delta(x), all j>=1},
inf_(x in D) max_(z in Z_delta(x)) G_0(x,z).
```

Upper constraints do not filter the follower's choices before the adversary
selects a response. The budget is measured above the true global follower
minimum, including when its aggregate cost is nonconvex.

**Theorem.** For fixed `r,d,s,k,h`, robust feasibility, the exact finite infimum
when feasible, and attainment decision are computable in polynomial rational
input bit time. If the infimum is attained, an optimal leader and a worst-case
near-optimal follower response can be returned in one real-algebraic field of
polynomial degree and total encoding length. At any supplied rational feasible
leader, exact worst-case criterion values and witnessing near-optimal responses
are also computable in polynomial bit time. No bound on the number of follower
variables, local polyhedral rows, or upper criteria is required.

The polynomial exponent depends on the fixed dimensions. This is a structural
complexity result, not an implemented scalable global optimization algorithm.

## 2. Affine measurement fibers compress near-optimality

Fix one matrix `T(x)` with at most `h` rows and write `t=T(x)z`. For a nonempty
fiber define

```
m_T(x,t) = min {f(x,z): z in P(x), T(x)z=t}.
```

The measurement equation adds only `h` shared resource rows. Treat `(x,t)` as
the leader parameters. The local block dimension and aggregate count do not
increase. The added row normals are polynomial in `x`, so the moving-normal
compression applies. The parameter dimension increases only from `r` to `r+h`.

Uniform polynomial coordinate bounds on `z`, compactness of `X`, and polynomial
entries of `T` give a computable rational box containing every possible `t` with
polynomial bit length. One can obtain bounds for the polynomial data by fixed-
dimensional real algebraic optimization on `X`, then round outwards to rational
integers. No enumeration over the growing follower coordinates is needed beyond
their explicit input lists. The enlarged parameter domain is compact.

The existing compression constructs a polynomial-size fixed-variable formula
`M_T(x,t,u)` for the graph of the attained fiber minimum. To make the dependency
explicit, local KKT solutions are rational functions of the compressed leader,
aggregate, and multiplier coordinates on polynomially many sign regimes. Every
global fiber minimizer has such a representation. Compare its objective against
all feasible fiber KKT candidates using one universal compressed copy. KKT points
that are not globally optimal are thereby excluded. Quantifier elimination
leaves a quantifier-free polynomial-size graph in free variables `(x,t,u)`.
Empty fibers contribute no point to this graph.

The central identity is

```
exists z in Z_delta(x) with T(x)z=t
   iff exists u: M_T(x,t,u) and u<=v(x)+delta(x).       (1)
```

The forward implication follows by minimizing over that fiber. Conversely, the
compact fiber has a minimizer; its cost meets the near-optimality budget and its
measurement is exactly `t`. The selected representative can be a fiber minimizer
even if the original near-optimal response was not a stationary point of the
unrestricted follower problem. This distinction is essential.

This is a general value-function projection identity. No novelty is claimed for
the identity alone; the structural compression and bit guarantee are the point.

**Simpler implementation of the threshold predicate.** Global comparison need
not be repeated for each measurement. Let `K_T(x,t,u)` describe feasible
measurement-fiber KKT candidates and their objective values, using the same
rational block response regimes. The right side of (1) is also equivalent to

```
exists u: K_T(x,t,u) and u<=v(x)+delta(x).                 (2)
```

If a near-optimal point exists on the fiber, a global fiber minimizer supplies
such a KKT candidate. Conversely, every candidate is feasible on the fiber, so
its own cost bound makes it near-optimal. Global optimality is still required
when computing the nominal value `v(x)`; (2) does not replace that comparison.
Either version gives the theorem, and the subsequent formulas may use (2).

## 3. Robust criteria without a growing quantified dimension

Let `M_0(x,v)` be the already eliminated graph of the nominal minimum, obtained
with no measurement rows. For each criterion `j`, eliminate the variables in

```
E_j(x,v,q) := exists t,u:
  M_(T_j)(x,t,u) and u<=v+delta(x) and q=p_j(x,t).
```

At `v=v(x)`, this is exactly the set of attainable values of the criterion on
the near-optimal set. Its degree and formula size remain polynomial since the
number of real variables in each elimination is fixed. Perform these eliminations
**separately for each criterion before conjoining the resulting formulas**.
Introducing one simultaneous quantified block for every criterion would destroy
the fixed-variable argument and is not the proposed algorithm.

Likewise eliminate the scalar in each predicate

```
B_j(x,v) := exists q: E_j(x,v,q) and q>0.
```

Then an admissible leader is described by

```
D(x) := x in X and exists v:
  M_0(x,v) and not B_1(x,v) and ... and not B_m(x,v).
```

Only one nominal-value variable is needed. There are polynomially many separate
eliminations and their quantifier-free outputs have polynomial total size. The
nominal value is unique, so the `v` shared by every constraint is the true value.

Define the worst objective graph by

```
W(x,q) := D(x) and exists v:
  M_0(x,v) and E_0(x,v,q)
  and not exists q': E_0(x,v,q') and q'>q.
```

Compactness of `Z_delta(x)` and continuity of each criterion ensure that its
maximum is attained at every admissible leader. The set of attainable worst
values `{q: exists x W(x,q)}` is a bounded semialgebraic set with a polynomial
fixed-variable description. Its emptiness, infimum endpoint, and membership of
that endpoint are decided by fixed-dimensional real algebraic algorithms.
Membership determines whether an optimal leader exists. If the leader domain is
empty or no follower is feasible, report infeasibility instead of a value.

## 4. Exact witness recovery

When an optimal leader exists, sample it simultaneously with its nominal value,
worst criterion value, measurement `t`, and the compressed global minimizer of
the corresponding measurement fiber. There are only fixed-dimensional copies
of the response engine. Common-field algebraic sampling gives polynomial degree
and total bit length. Recover all local coordinates from their rational response
formulas in that same field. By (1), the resulting follower is within the budget
and attains the worst criterion value. It need not maximize or minimize the
original follower cost among all near-optimal points.

The same argument at a rational feasible leader returns a counterexample to any
violated upper criterion, or its exact worst value. Exact rational follower output
is not claimed: an irrational worst response can be forced even by a scalar
quadratic cost and a rational positive budget.

If witnesses are requested for many unrelated criteria, provide separate
polynomial-size algebraic encodings for each. The common-field guarantee covers
the sampled optimal leader and one worst response; combining independently
requested witnesses into a single polynomial-degree field is not promised.

## 5. A useful unconditional-attainment subclass

Suppose all local and shared constraint normals are independent of the leader,
and `phi(x,.)` is convex for each `x`. Keep positive-definite local quadratic
costs and all previous compactness assumptions. Then the robust problem attains
its optimum whenever feasible, for every continuous polynomial budget
`delta(x)>=0`, including budgets equal to zero.

Here is the continuity argument, which is separate from the algebraic algorithm.
The feasible-leader set `X_F={x in X:P(x) nonempty}` is compact. The common
constraint matrix and Hoffman's error bound give lower semicontinuity of `P`
relative to `X_F`: a point feasible at `x` can be repaired to a nearby point
feasible at any nearby feasible leader, with distance bounded by a constant times
the change in polynomial right-hand sides. Upper semicontinuity follows from
closed constraints and uniform bounds. Strict convexity gives a unique nominal
minimizer, continuous on `X_F`, and its value `v` is continuous.

The near-optimal correspondence is upper semicontinuous by its closed graph and
uniform bounds. To prove lower semicontinuity at `(x,z)` with positive budget,
mix `z` with the unique nominal minimizer by any positive weight. Convexity makes
the mixture's cost strictly less than `v(x)+delta(x)` unless `z` was already
strictly below it, in which case mixing is unnecessary. The mixture can be made
arbitrarily close to `z`; repair it into nearby feasible fibers and use continuity
of the cost, value, and positive budget. This yields near-optimal points for every
sufficiently close feasible leader. At a zero budget, the near-optimal set is the
singleton nominal minimizer, and the continuous nearby nominal minimizers give
the required approximations even if nearby budgets are positive.

Thus `Z_delta` is a continuous compact-valued correspondence on `X_F`. Its
continuous-criterion maxima are continuous. The robust feasible set is closed
in compact `X_F`, and its worst objective attains a minimum whenever nonempty.
These are classical maximum-theorem and error-bound arguments; the new candidate
claim remains the combined structural exact algorithm.

## 6. Scope, practical uses, and limits

- Affine performance criteria permit arbitrarily many response-dependent upper
  constraints without fixing their collective rank.
- The same theorem can maximize an explicitly bounded tolerated follower-cost
  loss by treating the loss budget as an additional leader coordinate. This is
  an exact robustness-versus-cost design problem within fixed leader dimension.
- Polynomial criteria in a fixed number of measurements include nonlinear risk
  or performance measures, but arbitrary dense polynomial criteria in all follower
  coordinates are not covered by this projection proof.
- With moving constraint normals or nonconvex aggregate costs, compact leader and
  follower sets do not guarantee leader attainment. The existing zero-budget
  counterexamples remain valid special cases, so the general theorem retains an
  attainment decision rather than promising a nonexistent optimizer.
- This does not extend exact common-field output to general convex polynomial
  local costs. Independent cubic local costs already create the documented
  sum-of-square-roots representation and comparison boundary.
- No unit-cost real arithmetic, rational worst response, general fixed-parameter
  tractability, or practical polynomial exponent is claimed.

## 7. Explicit boundaries

### A positive budget does not restore attainment for nonconvex followers

Let `delta=1/16`, `z in [0,1]`, and `h(z)=3z^2-2z^3`. For a parameter
`c in [delta,1/8]`, put

```
f_c(z)=z^2(1-z)^2+c h(z).
```

Its unique global minimizer is zero with value zero: both summands are
nonnegative and `h(z)>0` for every `z>0`. This fits the theorem by separating
off the positive local quadratic `z^2/2` and putting the remainder in the
one-dimensional polynomial aggregate cost. The box normals are constant.

At `c=delta`, direct factorization gives

```
f_delta(z)-delta=(z-1)^2(z^2-z/8-1/16).
```

Thus `Z_delta=[0,a] union {1}`, where `a=(1+sqrt(17))/16<1/3`. For `c>delta`,
the cost is strictly larger at every positive `z`, and its delta-sublevel is
`[0,a_c]`, with `0<a_c<a`. Indeed
`f_c'(z)=2z(1-z)(1-2z+3c)` is positive up to its unique interior maximum and
negative afterwards; the endpoint value `f_c(1)=c` exceeds the budget.

Two distinct consequences follow.

1. Let the leader be `c in [delta,1/8]`, minimize `c`, and require `z<=1/2`
   for every near-optimal response. The robust feasible set is exactly
   `(delta,1/8]`. Its infimum is `delta` and is not attained.
2. Even without upper constraints, let `x in [0,delta]`, set `c=delta+x`,
   and minimize the worst value of `4x+z`. At zero the value is one. For
   positive `x` it is `4x+a_(delta+x)>a` and tends to `a` as `x` decreases
   to zero. To see the strict inequality, on `0<z<=a<1/3` one has
   `f_delta'(z)=z(4z^2-51z/8+19/8)>z/4` and `h(z)<z`.
   Since `x h(a_c)=f_delta(a)-f_delta(a_c)`, integration gives
   `x a_c>(a-a_c)a_c/4`, hence `a-a_c<4x`. The infimum `a` is unattained.

Both examples were independently derived and cross-checked in the two reviews.
They show why the theorem retains an attainment decision despite compactness,
unique nominal responses, fixed normals, and a strictly positive budget. No
new general nonattainment mechanism is claimed.

### Arbitrary quadratic upper criteria cross a hardness boundary

With no leader, shared resources, or aggregate coupling, take the positive
diagonal quadratic follower `f(z)=sum_i z_i^2/2` on the unit cube and budget
`delta=N/2`. The near-optimal set is the whole cube. For an input graph, the
quadratic upper criterion

```
G(z)=sum_{ij in E}(z_i-z_j)^2
```

is convex, so its maximum on the cube is attained at a vertex. At binary
vertices it is exactly the cut size. Exact worst-value computation is therefore
NP-hard, and universal upper-threshold feasibility is coNP-hard by the classical
Max-Cut problem (using threshold `K-1` to complement `MaxCut>=K`). A violating
binary vertex also gives NP membership of the complement on this family.
This is an elementary transfer of classical hardness, not a new Max-Cut result.
The fixed per-criterion measurement restriction is substantive; permitting
unboundedly many separately checked affine rows does not imply tractability of
an arbitrary growing-rank quadratic criterion.

## 8. Open primary-source comparison

Besançon, Anjos and Brotcorne, *Robust bilevel optimization for near-optimal
lower-level solutions*, J. Global Optimization 90 (2024), 813–842,
[open published version](https://publications.polymtl.ca/65063/1/2024_Besancon_Robust_Bilevel_Optimization_Near-optimal_Lower-level.pdf),
introduce and develop the near-optimal robustness model and convex-duality
reformulations. Their robustification principle is prior work.

The same authors' *Complexity of near-optimal robust versions of multilevel
optimization problems*, Optimization Letters 15 (2021), 2597–2610,
[open manuscript](https://arxiv.org/pdf/2011.00824), Lemma 1 and Theorems 1–2,
study preservation of complexity-class membership under adversarial response
optimization. They do not state the present polynomial-time global algorithm
with growing follower dimension and fixed block/aggregate/resource dimensions.
The exact source locators and comparison boundaries are recorded in the
[continuation literature audit](../notes/bilevel-reopened-literature-audit.md).

The near-optimal model, fixed-variable elimination, and value-function fiber
identity are not separately new claims. With the proof audits complete and no
matching combined theorem found in the inspected sources, the proposed contribution is their exact
structural composition, including nonconvex aggregate followers, independently
varying measurement criteria, and algebraic adversarial witnesses.

## 9. Verification record

The [first full audit](../notes/review-bilevel-reopened-near-optimal-robustness.md) and
[second full audit](../notes/review-bilevel-reopened-near-optimal-robustness-second.md)
passed. They independently checked the full block/scalar compression dependencies,
empty fibers, changing constraint ranks, polynomial degree and bit complexity,
separate elimination for growing criterion counts, common-field witness recovery,
and the fixed-normal convex attainment proof. The first review proposed the
simpler thresholded fiber-KKT predicate; both verified it. Each reviewer derived
a positive-budget nonattainment example and cross-checked the other's. The
second review checked the Max-Cut boundary and clarified the multiple-witness
encoding limit.

The independent [first exact checker](../code/bilevel_reopened/nearoptimal_review_checks.py)
passed five symbolic identities and boundary checks. The [second exact checker](../code/bilevel_reopened/nearoptimal_second_review.py)
passed 24,603 fiber identities across 35 measurement models, two nonstationary
adversarial-witness examples, the positive-budget factorization and 2,048 exclusion
checks, and 75 graph cases with 5,421 cube-point comparisons. These are exact
diagnostics supplementing the general proof, not an implementation of the
fixed-dimensional elimination algorithm. No substantive theorem defect was found.
