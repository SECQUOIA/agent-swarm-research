# Compressed bilevel responses: pessimistic semantics and unattained infima

Date: 2026-09-05. Status: promoted after independent review to
[the result](../results/bilevel-compressed-response-infimum-semantics.md).
The starting point is the reviewed
[scalar compressed-response theorem](../results/bilevel-fixed-aggregate-response-algorithm.md)
and its [quadratic block extension](../results/bilevel-fixed-block-response-algorithm.md).
This note separates exact semialgebraic optimization from the extra
continuity needed to guarantee attainment.

## 1. Leader-dependent resource normals

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

The same extension is valid for the block theorem if only the **shared**
resource matrices `A(x),H(x)` vary; local matrices `E_b,G_b` stay constant.
The independent local active-normal lists and local KKT matrices remain
as proved there, and the shared-multiplier contribution to `q_b(v)` merely
acquires polynomial leader dependence. Varying local normals is outside
this note.

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

**Candidate corollary 1.** With polynomial shared resource normals, exact
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

**Candidate corollary 2.** Pessimistic feasibility under this convention,
exact infimum computation, and attainment decision are polynomial for the
scalar and block classes above, including polynomial shared normals.
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

## Attribution and boundaries

These are consequences of the newly derived response compression, not new
general quantifier-elimination or pessimistic-bilevel principles. General
bilevel distinctions and fixed-dimension complexity are compared in
[the source audit](bilevel-fixed-aggregate-response-novelty.md), particularly
[Ketkov and Prokopyev (2026)](https://arxiv.org/html/2511.15592v2).
Their pessimistic hardness results allow structures or dimensions excluded
here. This note does not resolve their general fixed-follower-constraint
case or promise attainment where it fails.

The exact arithmetic restrictions of the scalar theorem remain: general
convex cubic local response functions embed sum-of-square-roots comparison,
and unrestricted sparse-binary degrees can force exponentially large
minimal-polynomial output. No complexity claim is made for arbitrary
integer followers or unbounded local block dimensions.
