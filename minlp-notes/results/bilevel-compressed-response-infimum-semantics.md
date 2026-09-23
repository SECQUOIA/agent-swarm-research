# Compressed bilevel responses: pessimistic semantics and unattained infima

Date: 2026-09-05. Status: independently reviewed corollaries.
[First independent audit](../notes/review-bilevel-infimum-semantics.md) and
[second independent audit](../notes/review-bilevel-infimum-semantics-second.md).
The starting point is the reviewed
[scalar compressed-response theorem](bilevel-fixed-aggregate-response-algorithm.md)
and its [quadratic block extension](bilevel-fixed-block-response-algorithm.md).
This note separates exact semialgebraic optimization from the extra
continuity needed to guarantee attainment.

## 1. Polynomially varying shared and local constraint normals

In the scalar theorem, replace the constant resource matrices by polynomial
matrices `A(x),H(x)`, still with fixed row counts. Keep compact `C`, finite
polynomial bounds, positive local quadratic coefficients, fixed aggregate
and leader dimensions, and the original polynomial encoding condition.

The rational response construction is unchanged except that

```
B_i(v)=c_i(x)+(U(x)^T grad_w phi(x,w))_i
               +(A(x)^T lambda)_i+(H(x)^T mu)_i.
```

For each fixed leader, the follower set remains a compact polyhedron.
Polyhedral KKT necessity still applies at that fixed leader, regardless of
whether the normals vary across leaders. The clipping tests remain
polynomials in the same fixed number of variables; their actual degrees
are polynomially bounded. Shared feasibility, complementarity, and value
equations also remain polynomial after positive denominator clearing.
Thus the complete globally optimal response graph still has a
polynomial-size first-order description using a fixed total number of
variables. The common-field encoding argument remains unchanged.

For the block theorem, allow both shared resource matrices and all local
constraint matrices to depend polynomially on the leader:

```
P_b(x)={y: E_b(x)y=e_b(x), G_b(x)y<=h_b(x)}.
```

Keep fixed leader, aggregate, shared-row, and maximum block dimensions;
positive-definite local polynomial quadratic matrices `Q_b(x)`; compact
`C`; and polynomial coordinate bounds ensuring uniform boundedness. Local
row counts may grow. The following argument replaces the constant
local-equality-basis step in the original block proof.

### Local response branches when equality ranks change

At fixed compressed coordinates `v=(x,w,lambda,mu)`, the local quadratic
response is still unique when feasible. Its stationarity problem has
polynomial positive-definite matrix `Q_b(x)` and polynomial effective
linear coefficient `q_b(v)` exactly as in the earlier block proof.

Instead of choosing a single constant row basis of `E_b`, enumerate every
pair `(I,J)` where `I` is a subset of equality rows, `J` a subset of
inequality rows, and `|I|+|J|<=d_b`. There are polynomially many pairs for
fixed `d`, even when their row counts grow. Include the empty pair.
Put

```
V_(I,J)(x)=[(E_b(x))_I; (G_b(x))_J],
M_(I,J)(x)=[Q_b(x)  V_(I,J)(x)^T;
             V_(I,J)(x)     0].
```

Use a branch only where `Delta_(I,J)(x)=det M_(I,J)(x)` is nonzero.
For positive-definite `Q_b(x)`, this is equivalent to row independence of
`V_(I,J)(x)`, by the same nullspace argument as in the original block
proof. Cramer's rule solves its KKT equations rationally. As before, use
`Delta^2` as a positive denominator, multiplying all Cramer numerators by
`Delta`. This denominator is now positive only on the branch's declared
validity region, which is sufficient for every clearing operation.

A branch is valid when `Delta^2>0`, the candidate satisfies **all** original
local equality and inequality rows, and the multipliers belonging to `J`
are nonnegative. No condition that `I` span all equality rows is needed for
soundness: multipliers on omitted equality and inequality rows can be set
to zero, yielding sufficient KKT conditions for the local strictly convex
quadratic program. Hence every valid branch returns its unique minimizer.

For completeness, at any fixed `x` with a feasible local polytope choose
`I` to be a basis of the full equality row space at that leader. The
polyhedral normal-cone representation of the negative local minimizer gradient,
followed by conic support reduction modulo that equality row space,
provides active inequality rows `J` independent together with `I` and
`|I|+|J|<=d_b`. This pair is enumerated and has nonzero KKT determinant.
Its branch is valid and returns the minimizer. Rank changes of `E_b(x)`
cause no missing cases because all possible bases, including the empty
one, were enumerated.

### Global regimes and bit complexity

Collect every determinant and cleared branch-feasibility polynomial from
all blocks. The KKT matrices have size at most `2d`; their entries have
polynomial degree in the fixed-dimensional leader/compressed variables.
Determinants and numerators therefore have polynomial degree and expanded
bit length. There are polynomially many branches and tests for fixed `d`.

Realizable sign conditions of this family in the fixed-dimensional
compressed space can be enumerated in polynomial bit time. Within each
condition, determinant nonvanishing and all branch-validity tests are
fixed. Discard a condition if any block has no valid branch; otherwise
choose its first valid branch. Uniqueness of the local quadratic response
makes overlapping branches agree, so this selection is lossless.

The selected squared determinants have positive product on that regime.
Clearing this common denominator gives a polynomial-size fixed-dimensional
formula for all follower KKT points. Pointwise polyhedral KKT necessity
still covers every global follower minimizer. Comparing all compressed
KKT values therefore gives the exact globally optimal reaction graph.

All quantifier formulas for optimistic and pessimistic values, infima,
and attainment now apply unchanged. Uniform box boundedness on compact
`C` bounds all upper values. At each fixed feasible leader the follower
argmin set is compact, so a pessimistic worst response exists there. The
reaction graph need not be closed as the leader varies; hence the result
retains an attainment test and does not promise an optimizer when the
infimum is unattained.

What fails is the fixed-normal Hoffman argument for a closed reaction
graph. For example,

```
x,z in [0,1],  xz=0,
follower minimizes (z-1)^2,
leader minimizes x+z.
```

For `x>0` the sole response is `z=0`; for `x=0` it is `z=1`. The optimistic
objective has infimum zero, but no optimizer attains it. This example has
a positive local quadratic coefficient and only one shared equality.

**Corollary 1.** With polynomial shared and local constraint normals, exact
optimistic bilevel feasibility, infimum computation, and attainment
decision remain polynomial in rational input bit length for the same fixed
dimensions and encoding. If the infimum is attained, an exact optimizer
can be returned in polynomial-size common-field form. A feasible problem
has a finite infimum because the upper objective is continuous on the
compact leader set and uniformly bounded follower boxes. Fixed-normal
attainment is a separate stronger conclusion of the original theorem.

## 2. Pessimistic semantics, including robust upper constraints

Let

```
S(x)=argmin{f(x,z): z in P(x)}.
```

Here the following pessimistic convention is explicit: upper constraints
must hold for **every** globally optimal follower response, and the leader
minimizes the worst upper objective among those responses. Thus admissible
leaders form

```
D={x in C: S(x) is nonempty,
            g_j(x,z)<=0 for every z in S(x) and every j},
```

and the objective at `x in D` is

```
W(x)=max{F(x,z): z in S(x)}.
```

The follower optimizes over `P(x)`, without upper constraints. Upper
constraints do not remove unwanted follower optima before the worst-case
selection. This convention avoids ambiguity between different formulations
called pessimistic bilevel optimization.

For each feasible leader, `S(x)` is nonempty and compact, so the maximum
in `W(x)` is attained. The admissible leader set need not be closed, and
its worst-case objective need not attain its infimum.

**Corollary 2.** Pessimistic feasibility under this convention,
exact infimum computation, and attainment decision are polynomial for the
scalar and block classes above, including polynomial shared and local constraint normals.
When an optimal leader exists it can be returned exactly; one of its
worst-case globally optimal follower responses can also be returned. All
returned algebraic coordinates have polynomial total encoding length in
one common field. No unconditional attainment claim is made even when all
constraint normals are fixed.

### Fixed-dimensional formulas

Write `R(x;xi)` for the globally optimal compressed follower-response
formula, where `xi=(w,lambda,mu,tau)`. It includes the original fixed-size
universal copy that compares all follower KKT values. For each response
regime the follower vector is a known rational function `z=Z/Q`, with
`Q>0`. Define

```
T(x,eta) := exists xi:
   R(x;xi) AND [eta=F(x,Z/Q) in its regime],

Bad(x) := exists xi:
   R(x;xi) AND [some g_j(x,Z/Q)>0 in its regime].
```

The bracketed predicates are quantifier-free polynomial-size disjunctions
over the already enumerated regimes, with positive denominator clearing.
Each formula keeps its single copy of `R` outside that regime disjunction;
it does not repeat quantified response variables once per regime or per
upper constraint. Equivalently, eliminate the internal quantifiers of `R`
once before building these formulas. The response
formula returns only feasible global follower optima; conversely it covers
every such optimum. A response may have several multiplier encodings,
which does not change either predicate. Multiple valid regime formulas at
the same compressed point agree on the follower vector.

Then

```
D(x) := x in C AND [exists xi: R(x;xi)] AND NOT Bad(x),

Worst(x,eta) := D(x) AND T(x,eta)
                 AND forall eta': [T(x,eta') implies eta'<=eta].
```

Every copy of `R` or `T` uses fresh internal variables. The number of
copies is a fixed constant, so the total number of real variables remains
fixed. Formula length remains polynomial even if there are many upper
constraints, because these appear in an explicit disjunction inside
`Bad`, not as separate quantified variable blocks.

Fixed-dimensional quantifier elimination gives the exact semialgebraic
set

```
V={eta: exists x Worst(x,eta)}.
```

It also decides if `D` is empty. If nonempty, `V` is nonempty and bounded;
its infimum is an endpoint of a univariate semialgebraic set and can be
computed exactly by univariate real algebra. Membership of that endpoint
in `V` decides attainment.

For simultaneous common-field recovery one can instead add a free `eta0`
and encode the infimum property as

```
[forall eta: eta in V implies eta0<=eta]
AND [forall epsilon>0: exists eta in V with eta<eta0+epsilon].
```

Substituting the fixed-variable description of `V` gives only a fixed
number of additional quantified copies. When attainment holds, append
`Worst(x,eta0)` and the compressed response equation realizing `F=eta0`.
Quantifier elimination and simultaneous algebraic sampling produce the
leader and its worst-case response in one polynomial-degree extension.
The same infimum construction proves Corollary 1 using optimistic
attainable values instead of `Worst`.

## 3. Fixed normals do not ensure pessimistic attainment

Take `x,z in [0,1]`, no resource constraints, and follower objective

```
f(x,z)=z^2(1-z)^2+xz.
```

This fits the positive-local-quadratic model with `a=1`, aggregate `w=z`,
and

```
phi(x,w)=w^2(1-w)^2-w^2/2+xw.
```

For `x>0`, both terms in `f` are nonnegative and only `z=0` has value zero.
At `x=0`, exactly `z=0,1` are global optima. Set `F(x,z)=x+z` and impose no
upper constraints. Then

```
W(x)=x for x>0,  W(0)=1.
```

The pessimistic infimum is zero and is not attained, despite fixed normals,
compact boxes, and a positive local quadratic coefficient. The aggregate
term is nonconvex, as the theorem permits.

The same example shows why robust upper feasibility can be nonclosed.
Adding the upper constraint `z<=1/2` makes every `x>0` admissible but excludes
`x=0` because one of its globally optimal responses violates the constraint.
Optimistic feasibility would retain `x=0` by selecting `z=0`; the two
semantics differ on this instance.

## 4. Attribution, validation, and boundaries

The additional moving-local-normal proof is preserved in
[its investigation note](../notes/bilevel-moving-local-normal-extension.md).
The exact boundary checker
[check_response_boundaries.py](../code/bilevel_response/check_response_boundaries.py)
passed. It checks the singular equality-active branch for `xz=0`, the
necessary switch to an empty equality basis at `x=0`, and exclusion of the
quartic follower's nonglobal stationary point `z=1/2` by value comparison.
These examples support, but do not replace, the independent proof audits.

These are consequences of the newly derived response compression, not new
general quantifier-elimination or pessimistic-bilevel principles. General
bilevel distinctions and fixed-dimension complexity are compared in
[the source audit](../notes/bilevel-fixed-aggregate-response-novelty.md), particularly
[Ketkov and Prokopyev (2026)](https://arxiv.org/html/2511.15592v2).
Their pessimistic hardness results allow structures or dimensions excluded
here. This note does not resolve their general fixed-follower-constraint
case or promise attainment where it fails.

The exact arithmetic restrictions of the scalar theorem remain: general
convex cubic local response functions embed sum-of-square-roots comparison,
and unrestricted sparse-binary degrees can force exponentially large
minimal-polynomial output. No complexity claim is made for arbitrary
integer followers or unbounded local block dimensions.
