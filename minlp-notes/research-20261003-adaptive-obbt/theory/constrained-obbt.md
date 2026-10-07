# Constraints, active-set changes, and incumbent-triggered OBBT

This note develops checkable sensitivity statements for constrained OBBT.
It does not infer a convergence certificate from observed contraction rates.
The exact checker is [check_constrained_obbt.py](check_constrained_obbt.py).

The LP facts below are classical parametric programming. In particular,
Borrelli, Bemporad, and Morari, *Geometric Algorithm for Multiparametric
Linear Programming*, JOTA 118 (2003), Sections 2–4, derive affine optimizers
and critical regions for fixed-matrix LPs with affine right-hand sides
([author-hosted paper](https://cse.lab.imtlucca.it/~bemporad/publications/papers/jota-mplp.pdf)).
Our use is an OBBT certificate contract: distinguish safe reuse, guaranteed
new tightening, and bounds on possible benefit, and supply the uniform
sensitivity assumption needed by a remaining-benefit certificate. These
facts alone establish neither publication priority nor a runtime improvement.

## 1. A relaxation family and its signed supports

Let

```text
R(theta) = {z : A z <= b + E theta},
h_c(theta) = max {c^T z : z in R(theta)}.                     (C1)
```

The original variables are selected coordinates of the lifted vector `z`.
Every parameter under consideration has a nonempty relaxation, and the
support values used below are finite and attained. All data in an exact
certificate are rational. A node's signed box endpoints are `p=(u,-l)`;
the signed coordinate objectives are `c=e_i` and `c=-e_i`. The parameter
`theta` can contain `p` and an objective cutoff `U`.

Validity of `R(theta)` as an outer relaxation is a separate obligation.
An LP basis certificate does not prove that a generated nonlinear row is
valid. If the family is monotone under smaller boxes and cutoffs, the
corresponding signed support map `F(p,U)` is monotone, and `F(p,U)<=p`
when all current box bounds are present.

**Fixed matrix means fixed matrix.** The rows of a rebuilt McCormick
relaxation ordinarily change their coefficients when bounds change. They
do not satisfy (C1) merely because their coefficients are easy to evaluate.
For those rows, the certificate below applies to cutoff changes with the
box frozen. For a varying box one must derive a valid normalization, verify
the parameter-dependent basis algebra and derivative bounds separately, or
use a different remaining-benefit certificate. A numerical active set is
only a proposal for these checks.

## 2. Dual envelopes remain valid across active-set changes

**Proposition C1 (global dual upper envelope).** If `y>=0` and `A^T y=c`,
then, for every parameter with nonempty relaxation,

```text
h_c(theta) <= y^T b + y^T E theta.                          (C2)
```

For a stored finite collection of dual feasible vectors, the minimum of
their affine bounds is also an upper bound. This conclusion does not
require the stored basis to remain optimal or primal feasible.

*Proof.* For every feasible `z`, `c^T z=y^T Az<=y^T(b+E theta)`.
Taking the maximum and then the minimum over stored vectors proves both
claims. QED.

Suppose the only changing row is the objective cutoff `a^T z<=U`, and a
stored primal-dual pair is exactly optimal at `U0`. Let `eta` be the
nonnegative dual multiplier of that row. Then for `U<=U0`,

```text
h_c(U) <= h_c(U0) - eta (U0-U).                            (C3)
```

Thus `eta (U0-U)` is a **guaranteed support reduction**, provided the new
relaxation is nonempty. It is not an upper bound on the amount of new
tightening. A zero old multiplier gives no such guaranteed reduction; it
does not prove that a later cutoff change has no effect.

If exact optimality was not proved, the stored affine expression still
bounds the new support, but subtracting it from an unverified old optimum
does not certify (C3). A previously certified signed endpoint can always
be compared directly with the new affine upper bound.

## 3. Exact basis cells and finite cutoff validity intervals

For `d=dim(z)`, choose `d` linearly independent rows indexed by `I`. Define

```text
z_I(theta) = A_I^{-1}(b_I+E_I theta),
y_I       = A_I^{-T} c,      y_j=0 for j outside I,
C_I       = {theta : A z_I(theta) <= b+E theta}.            (C4)
```

**Proposition C2 (basis cell certificate).** If `y_I>=0`, then for every
`theta in C_I`, `z_I(theta)` is an optimal support point and

```text
h_c(theta)=c^T A_I^{-1}(b_I+E_I theta).                     (C5)
```

*Proof.* The proposed point is feasible by the definition of `C_I`.
The vector `y` is dual feasible and is supported on tight rows, so
`c^T z_I=y^T(b+E theta)`. Proposition C1 supplies the matching upper bound.
QED.

The cell is a closed rational polyhedron. For a proposed bounded parameter
polytope given as a convex hull, checking all residual inequalities at its
vertices proves containment in `C_I`. This tests a proposed cell, not the
completeness of a collection of cells. Coverage must also be verified.
In one parameter, exact interval endpoints and adjacency suffice. In more
parameters, coverage is an additional geometric verification problem.

Degeneracy does not invalidate C2: zero dual multipliers and ties between
bases are allowed. A singular proposed basis is rejected. A degenerate
support may need a different independent basis; this certificate format
does not promise that a solver's first proposed basis works.

For a cutoff interval, write `z_I(U)=v+wU`. Each primal constraint becomes
one scalar affine inequality in `U`. Their exact intersection gives the
interval on which (C5) is valid. Inside that interval, the cutoff slope
`eta` gives the exact support change. Outside it, the same dual vector
continues to give C2, but the affine expression need not be exact.

### Exact example: a zero cutoff multiplier before a useful tightening

Consider the LP with objective `min y`, box `0<=x<=3`, `0<=y<=4`, and

```text
x-y <= 1,       4x-y <= 7,       x <= 5/2.
```

The objective cutoff adds `y<=U`, where `0<=U<=4`. Maximizing `x` gives

```text
h_x(U) = min(1+U, 7/4+U/4, 5/2)
       = 1+U          for 0<=U<=1,
         7/4+U/4      for 1<=U<=3,
         5/2          for 3<=U<=4.                         (C6)
```

In each interval, choose `y=U` and let `x` equal the displayed support.
These points are feasible and meet their corresponding dual upper bound.
The cutoff multipliers are `1`, `1/4`, and `0`, respectively. The checker
verifies all three basis cells, their coverage, and their exact values.

At `U0=4`, the multiplier is zero. Tightening to `U=2` nevertheless reduces
the support from `5/2` to `9/4`. The validity interval, or the support
witness `(5/2,3)`, certifies no reduction only as far down as `U=3`.
At `U0=2`, the old dual gives the valid bound `15/8` after a change to
`U=1/2`; the new support is `3/2`. Extrapolation remains safe as an upper
bound and understates the actual improvement.

This example is a constrained LP, not a claimed difficult MINLP instance.
It isolates the active-set and reuse issue without numerical ambiguity.

## 4. Witnesses bound the possible benefit of retriggering

**Proposition C3 (retained support witnesses).** Fix the box and all rows
except the objective cutoff. Let `p_i` be a currently valid signed bound.
Store any finite set of exactly feasible relaxed points `W_i`. At a new
cutoff `U`, retain only points satisfying `a^T z<=U`. If the retained set is
nonempty, then

```text
L_i(U) = max {c_i^T z : z in W_i, a^T z<=U} <= F_i(U),
0 <= p_i-F_i(U) <= p_i-L_i(U).                             (C7)
```

The nonnegative lower inequality assumes the current box is part of the
relaxation. Combining C7 with a dual envelope `D_i(U)` brackets the new
support by `L_i(U)<=F_i(U)<=min(p_i,D_i(U))`.

*Proof.* Every retained point is feasible for the new support problem,
which proves the lower support bound. Subtracting it from `p_i` proves
the upper improvement bound. QED.

If a witness attained the old exact support, it proves that support does
not change until its own objective value is excluded. Among several old
optimal witnesses, the one with least objective value gives the widest
such reuse interval. Finding that witness can itself require another LP;
the policy must account for that cost.

These are certificates for **one support problem on a fixed relaxation**.
They do not bound all later improvements after rebuilding nonlinear
relaxations. If the box or local rows change, every retained witness must
be rechecked against the changed rows. A witness excluded by a new cutoff
does not prove that tightening will occur: there may be another support
point. A missing witness is not an infeasibility certificate.

For a whole OBBT round, C7 must cover every direction whose possible benefit
is being bounded. One favorable direction does not screen an entire round.
For certified bounds on all future rounds use the protected-region or
uniform-contraction statements in
[remaining-benefit.md](remaining-benefit.md).

## 5. From active-set cells to a uniform comparison matrix

Fix a cutoff. Let `P` be a convex parameter region for signed endpoints,
with nonempty relaxations. Suppose that, for every support coordinate `i`,
a verified finite collection of closed basis cells covers `P`, and on
each such cell

```text
F_i(p)=alpha_i+g_i^T p.
```

**Proposition C4 (uniform sensitivity across switches).** If `M>=0` and
`|g_ij|<=M_ij` for every certified cell, then for every `p,q in P`,

```text
|F(p)-F(q)| <= M |p-q|                                  (C8)
```

componentwise.

*Proof.* The segment from `p` to `q` stays in `P`. Its intersections with
the finitely many polyhedral cells partition it into finitely many
intervals. On each interval the relevant support is affine, with
`|dF_i/dt|<=sum_j M_ij |p_j-q_j|`. At a cell boundary both valid basis
expressions equal the same support by C2, so there is no jump. Integrate
over the segment. QED.

This supplies an input to the matrix residual-tail theorem; it does not
by itself imply contraction. That theorem also requires the subsequent
OBBT trajectory to remain in the certified region and an appropriate
finite tail majorant, such as `rho(M)<1`. Frozen coordinates and persistent
feasible continua commonly prevent strict contraction.

For an order interval `[p_protected,p_current]`, monotonicity and a
verified fixed protected box ensure invariance. Certifying derivatives
only at the current parameter or only on its present basis cell is
insufficient when later iterates can cross a cell boundary.

### A complete changing-cell contraction certificate

For a transparent algebraic test, take the problem `x^2<=0`, `0<=x<=r`.
For `r>0`, retain just the tangents to `x^2` at

```text
t1=r/2,       t2=r/8+3/4.
```

Each necessary inequality `2t x-t^2<=0` becomes `x<=t/2`. Their LP
relaxation, including `x<=r`, has upper-support map

```text
F(r)=min(r/4,r/16+3/8),       0<=r<=8.                    (C9)
```

At `r=0` the box fixes `x=0`; no division by a zero tangent coefficient is
used. Both normalized rows are valid for the original feasible point.
The basis cells are `[0,2]` and `[2,8]`; their derivatives are `1/4` and
`1/16`. They cover the invariant region `[0,8]`, so `M=[1/4]` certifies C8
across the switch. Starting at `r=8` gives

```text
8 -> 7/8 -> 7/32 -> 7/128 -> ...
```

The active tangent changes after the first round. The ratio `7/64` in
that round is not a valid uniform contraction factor: the next ratio is
`1/4`. The exact checker verifies both cells and the trajectory. Direct
propagation would solve this deliberately simple problem immediately;
C9 tests the mathematical certificate, not solver performance.

## 6. A constrained quadratic example with an exact rate and floor

Consider `f(x,y)=(x-y)^2`, expanded as `x^2+y^2-2xy`, on `[-r,r]^2`.
Keep the square terms exact and replace `xy` by its McCormick
overestimator. The resulting convex objective is

```text
phi_r(x,y)=x^2+y^2-2r^2+2r|x-y|.                         (C10)
```

Without further constraints, the feasible minimizers `(r,r)` and `(-r,-r)`
retain every box endpoint at cutoff zero. OBBT stalls at the entire box.

Now impose the exact affine equality `y=-x`. It reduces C10 to

```text
phi_r(t,-t)=2t^2+4r|t|-2r^2.
```

For cutoff `U>=0`, a Jacobi OBBT round returns a symmetric box of radius

```text
G_U(r)=min(r, sqrt(2r^2+U/2)-r).                          (C11)
```

At `U=0`, this gives the exact linear rate `sqrt(2)-1`. At `U>0`, starting
from any `r0>=sqrt(U)/2`, the radii decrease to exactly `sqrt(U)/2`.

*Proof.* The relaxed cutoff on the equality is
`2|t|^2+4r|t|-2r^2<=U`. Its nonnegative root is the second term in C11.
It is smaller than `r` precisely when `r>sqrt(U)/2`. It is at least
`sqrt(U)/2` for all such `r`, since, with `a=sqrt(U)/2`,
`2r^2+2a^2-(r+a)^2=(r-a)^2>=0`. The sequence therefore has a limit at
least `a`. Continuity and the fixed-point equation force that limit to
be `a`. The case `U=0` follows by factoring out `r`. QED.

This gives a complete constrained instance of the tangent-map result:
an equality removes the directions responsible for stalling, and a better
incumbent lowers the attainable width floor. An interval `[0,U0]` of
possible cutoffs does not justify assuming the rate at `U0` is unchanged.

If the equality is eliminated before relaxing, the objective becomes
`4x^2`. Its exact convex cutoff gives `|x|<=sqrt(U)/2` in one round.
Thus the contraction rate depends on the formulation and the chosen
relaxation. There is no rate determined just by the original constrained
optimization problem.

The general affine-equality extension is direct when the original tangent
expansion has no first-order objective term and the equality is retained
exactly: restrict the tangent support problems to `C xi=0`. A verified
strict contraction for these restricted problems gives the same local
upper-rate argument as the old theory. General nonlinear active constraints
also need uniform residual and remainder control; simply imposing their
first-order tangent cone does not prove such a result. The repository's
[constrained growth bound](../../results/cluster-free-branch-and-bound-constrained-minima.md)
provides one route to a coarser bound, with its stated assumptions, rather
than a solver-independent exact rate.

## 7. Nonlinear constraints through a certified feasible repair

The following extension does not need a guessed active set. It uses a
uniform constraint error bound, feasible growth, and a relaxation error
bound. These are substantive assumptions; an optimizer's numerical KKT
residual does not establish them. The repair argument is an application of
classical error-bound transfer, also developed in the repository's
[projection proof](../../notes/research-20260922-error-bound-transfer.md).

Let `S` be the original feasible set, let `x* in S`, and write `f*=f(x*)`.
All boxes under consideration contain `x*` and lie in a fixed neighborhood.
Let `v(x)>=0` be a constraint residual, zero on `S`. For each relaxed point
`x in R(B)`, with `w=w(B)`, assume:

1. The objective estimator satisfies `phi_B(x)>=f(x)-a w^2` and the
   residual satisfies `v(x)<=b w^2`, for uniform `a,b>=0`.
2. There is a feasible repair `y in S` with
   `||x-y||_inf<=kappa v(x)^theta`, where `kappa>=0` and `0<theta<=1`.
   Both `x` and `y` lie in the neighborhoods on which the following two
   assumptions hold. The repair need not stay in `B`, but it must stay in
   the feasible-growth neighborhood; this is part of the assumption.
3. The objective change obeys `f(y)<=f(x)+L||x-y||_inf`, for uniform `L>=0`.
   A certified Lipschitz bound on a neighborhood containing both points
   suffices; a one-sided bound just on repair pairs also suffices.
4. Feasible growth holds at every such repair:
   `f(y)>=f*+mu||y-x*||_inf^2`, for uniform `mu>0`.

Relaxation validity at `x*` and a cutoff `U=f*+epsilon`, `epsilon>=0`, ensure
that the retained set is nonempty. The assumptions concern every point
in the relaxed set, including infeasible points, not just its minimizers.

**Proposition C5 (repair-based constrained width bound).** Define
`r=kappa(b w^2)^theta`. Then

```text
w(T_U(B)) <= 2r + 2 sqrt((epsilon+a w^2+Lr)/mu).           (C12)
```

For linear repair (`theta=1`), let `K=kappa b` and
`q=2 sqrt((a+LK)/mu)`. If `q<1`, choose a width limit `wbar>0` with
`lambda=q+2K wbar<1`. Throughout a neighborhood where the assumptions
hold and for all such boxes of width at most `wbar`,

```text
w(T_U(B)) <= lambda w(B) + 2 sqrt(epsilon/mu).             (C13)
```

At zero cutoff slack, iterated OBBT contracts with ratio at most `lambda`.
At positive slack, nested iterates remain in the original neighborhood
and satisfy

```text
limsup_k w(B_k) <= 2 sqrt(epsilon/mu)/(1-lambda).          (C14)
```

If `K=0`, choose any `wbar` on which the other assumptions hold and take
`lambda=q`. C14 is an upper bound, not an exact limiting width.

*Proof.* If a relaxed point is retained by the cutoff,
`f(x)<=f*+epsilon+a w^2`. Its repair satisfies
`f(y)<=f*+epsilon+a w^2+Lr`. Feasible growth therefore gives
`||y-x*||_inf<=sqrt((epsilon+a w^2+Lr)/mu)`. The triangle inequality
gives the same bound on `||x-x*||_inf` plus `r`. Taking the box hull gives
C12. For `theta=1`, split the square root using `sqrt(s+t)<=sqrt(s)+sqrt(t)`
and bound `2K w^2<=2K wbar w`; this proves C13. Nesting keeps later
widths at most `wbar`. Iteration of C13 gives C14 by summing a geometric
series. QED.

For `theta<1` and fixed positive `L*kappa*b`, C12 has an `O(w^theta)`
term. Its ratio to `w` need not be bounded near zero, so this argument
does not certify linear contraction. It does not prove that OBBT fails
to contract. If a local repair-pair Lipschitz bound `L_B` is available,
it can replace `L` in C12. The adverse square-root term then has order
`sqrt(L_B) w^theta`; recovering an `O(w)` bound requires
`L_B=O(w^(2-2theta))`, and the separate repair term `O(w^(2theta))`
must also be `O(w)`. Additional structure is needed when `theta<1/2`.

### A nonlinear equality with explicit rational constants

Consider

```text
S = {(x,y) : y=x^2} intersect ([-1/4,1/4] x [0,1/16]),
f(x,y)=x^2+y^2-xy/16,       (x*,y*)=(0,0), f*=0.
```

For any subbox `B=[ell,u] x [0,v]` containing the origin, use the graph
relaxation and objective estimator

```text
x^2 <= y <= (ell+u)x-ell*u,
phi_B(x,y)=x^2+y^2-m_B^U(x,y)/16,
m_B^U(x,y)=min(u*y, ell*y+v*x-ell*v).                    (C15)
```

The objective is convex after this McCormick replacement. The equality's
relaxation is convex and monotone under nested boxes. Bounds with zero
width are interpreted directly; no division by a width is needed.

Every relaxed point has the exact feasible repair `(x,y)->(x,x^2)`.
It stays in the same box because `0<=x^2<=y<=v`. Its infinity-norm repair
distance is precisely the residual `y-x^2`, bounded by
`(u-ell)^2/4<=w(B)^2/4`. Thus `theta=1`, `kappa=1`, `b=1/4`.

The bilinear envelope error is at most `(u-ell)v/4<=w(B)^2/4`, so
`a=1/64`. On the outer box,

```text
|partial_x f|+|partial_y f| <= (2+1/16)(1/4+1/16)=165/256,
```

which gives `L=165/256`. On the feasible graph,

```text
f(x,x^2)=x^2(1-x/16+x^2) >= (63/64)x^2
         = (63/64)||(x,x^2)||_inf^2.
```

Hence `mu=63/64`, `K=1/4`, and

```text
q^2 = 4(a+LK)/mu = 181/252 < 49/64 = (7/8)^2.
```

For `w(B)<=1/8`, C13 therefore gives the rational bound

```text
w(T_U(B)) <= (15/16) w(B) + 2 sqrt(64 epsilon/63).        (C16)
```

At cutoff zero this certifies uniform linear contraction for all nested
box shapes in that neighborhood, without knowing which inequality will
be active at the next support solution. The constants are conservative;
the claim is a sufficient rate bound, not an exact rate or a performance
advantage over recognizing convex structure. The checker verifies the
rational constants and the graph-repair and envelope identities. The
inequalities above prove them over the full boxes, not just at sampled
points.

## 8. Finite histories cannot certify an eventual stall

Here is a precise limit on observed-rate stopping rules under validity and
monotonicity alone. Fix an integer `N>=2`, set
`a=1/2`, `delta=1/(2N)`, `b=a-delta`, and `q=1/4`. Define two maps on `[0,1]`:

```text
F_stall(s) = min(s, max(b,s-delta)),

F_shrink(s) = q s                                      if s<=b,
              q b + (b-q b)(s-b)/(a-b)                 if b<=s<=a,
              s-delta                                 if s>=a.
```

Both maps are continuous, nondecreasing, and satisfy `0<=F(s)<=s`.
Consequently `R_s=[0,F(s)]` is a valid isotone outer relaxation family
for the original feasible set `{0}`. From `s0=1`, both trajectories agree
through `s_{N+1}=b`: they successively subtract `delta`. After that,
`F_stall` stays at `b`, while `F_shrink` converges geometrically to zero.
For `N=8`, the common history ends at `7/16`; the next values are
`7/16` and `7/64`.

*Verification.* On each piece the slopes are nonnegative, values match at
the boundaries, and `F(s)<=s` follows by checking the endpoints of each
affine piece. The common history remains at or above `a` until the step
from `a` to `b`. The two different continuations then follow from their
definitions. QED.

The example permits arbitrarily many initial ratios close to one while
leaving two incompatible eventual outcomes. It does not assert that these
families are standard McCormick relaxations. It proves that validity,
monotonicity, and a finite observed history cannot establish a general
remaining-benefit guarantee. A uniform derivative bound, protected box,
or additional relaxation-specific structure supplies information absent
from that history.

## 9. Interface to a solver policy

A certificate record must include the node/local-row scope, original and
current box, cutoff, signed direction, rational row data, and either a
verified dual vector, a retained primal witness, or a verified basis cell.
Changing any scoped row invalidates reuse until it is rechecked. Ancestor
row validity can survive at descendants, but descendant-local rows cannot
be used at siblings merely because their numerical coefficients match.

For a fixed-box cutoff improvement, C2/C3 yield bounds without a new LP
solve. A feasible witness that nearly reaches the current signed bound
can certify little one-round benefit. A dual envelope substantially below
that bound can certify useful available tightening. The unclassified gap
is an appropriate place for a budgeted LP probe, not a correctness claim.

The exact checks supplied here certify the stated small examples and the
basis-verification procedure. They do not certify the floating-point
relaxations produced by an external solver. Benchmark policies using
numerical duals or basis predictions must label those decisions as
heuristics unless they perform the rational or interval validation above.

## 10. Targeted verification

The following commands were run successfully from the repository root:

```bash
python research-20261003-adaptive-obbt/theory/check_constrained_obbt.py
python -m py_compile research-20261003-adaptive-obbt/theory/check_constrained_obbt.py
```

The first checks exact basis cells, their interval coverage, safe dual and
witness reuse, rejection of invalid certificates including floating-point
inputs, the active-tangent transition, the quadratic equality example,
the nonlinear graph constants and 141 rational graph cases, and the
finite-history counterexample. The second checks Python syntax. Neither
command is a project-wide check or a CI result.

The [independent theory review](../reviews/theory-review.md) checked the
propositions and supplied a floating-point false-acceptance example. The
verifier now rejects non-integer, non-`Fraction` numerical data at entry;
the supplied example and its exact-integer counterpart are regression
checks. Arithmetic tests support the proofs; they do not replace the
uniform assumptions of the general statements.
