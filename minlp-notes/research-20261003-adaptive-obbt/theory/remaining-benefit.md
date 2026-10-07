# Finite certificates for screening and remaining OBBT benefit

This note develops three different statements that must not be conflated:

1. A feasible relaxation point bounds the possible coordinate improvement in
   the **current frozen relaxation**.
2. Feasible endpoint points on a **self-consistent protected box** bound the
   coordinate and objective-bound improvement of every subsequent round of the
   specified isotone OBBT procedure.
3. A **verified uniform sensitivity bound** converts an exact residual, or a
   certified upper bound on that residual, into an upper bound on the remaining
   movement of exact Jacobi OBBT.

These are mathematical bounds on specified strengthening operations. They do
not establish that skipping those operations minimizes solving time. A skipped
coordinate solve may also forgo useful dual information for later Lagrangian
variable bounds even when its immediate coordinate improvement is zero.

Current-round primal filtering is established in Gleixner et al.,
[Section 3.2](https://optimization-online.org/wp-content/uploads/2016/03/5356.pdf).
The order arguments below specialize classical fixed-point reasoning; matrix
contraction bounds specialize the classical Perov/Banach framework, for
example [Jachymski and Klima, Theorems 3.2–3.4](https://www.math.ubbcluj.ro/~nodeacj/download.php?f=162-ja-kl-1396-final.pdf).
The contribution developed here is an explicit OBBT certificate contract,
computable finite constructions, cutoff reuse, exact checks, and scope limits.
Publication priority for these OBBT formulations is not asserted.

## R1. The relaxation family and the operation being certified

Write a nonempty box as `B=[l,u]`. All relaxations use the same lifted variables
`z=(x,w)` and the same affine objective `v(z)=c^T z+c0`. Let `R(B)` be the
compact convex relaxation on `B`, and

```
R_U(B) = {z in R(B): v(z) <= U},
T_U(B) = box hull of projection_x R_U(B).
```

The central hypothesis is **lifted isotonicity**:

```
P subset B  implies  R(P) subset R(B).                         (R1)
```

Validity additionally requires every original feasible point in `B` to have
its valid lift in `R(B)`, with the original objective represented by `v`.
Validity preserves original sublevel points; isotonicity proves the repeated
relaxation statements. These are separate requirements. Witnesses below need
only be relaxation feasible and may violate the original nonlinear model.

The implementation fixes rational linear rows and adds all four McCormick
inequalities for each product `w_k=x_i*x_j`, including square products with
`i=j`. This family satisfies (R1): the convex hull relaxation of each product
over a smaller rectangle lies in the one over a larger rectangle. Intersecting
with common linear rows and original-variable bounds preserves inclusion.
For a repeated index, restricting both product coordinates to the same `x_i`
also preserves inclusion. This finite LP square relaxation has endpoint
tangents and the secant; it does not use the exact convex square epigraph.

The default scope is continuous LP OBBT, including selecting individual
coordinate directions and rebuilding between them. A certified, conservative
coordinate update also preserves every box that exact OBBT preserves. New cuts,
changed row families, arbitrary native propagation and integer rounding are
additional operations and are not covered automatically. Integer rounding
preserves a protected box if its endpoints are integral on every integer
coordinate; otherwise even valid rounding can remove its fractional faces.

## R2. Current-round screening from primal points

**Proposition R2.** Let `W` be a nonempty collection of points in `R_U(B)`.
Define

```
a_i = min_{z in W} x_i,       b_i = max_{z in W} x_i.
```

The exact lower-bound increase in this frozen relaxation is at most `a_i-l_i`;
the exact upper-bound decrease is at most `u_i-b_i`.

**Proof.** The relaxed coordinate minimum is no greater than `a_i`, and its
maximum is no less than `b_i`. Subtract the current bound. These are bounds on
possible benefit, not valid new variable bounds. In particular, a primal
witness does not justify replacing the lower bound by its coordinate. QED.

Screening can begin before the first new endpoint LP if the solver already has
usable primal points. Checking `k` rational points in `m` rows costs a finite
row evaluation for each point and row. Finding good points may cost as much as
OBBT itself. The construction is therefore not an unconditional cheap test.

**Counterexample to indefinite reuse.** Relax `w=x^2`, `x in [0,u]`, with the
four square McCormick rows and cutoff `w<=0`. Then `max x=u/2`, attained by
`(x,w)=(u/2,0)`. That point certifies only the present round. After rebuilding
on `[0,u/2]` it violates the new upper-endpoint tangent. Exact rounds give
`u_k=2^{-k}u_0`, so the eventual upper-bound reduction is the entire `u_0`.
Freezing the first point would incorrectly cap it at `u_0/2`.

## R3. Protected boxes and all-future-round ceilings

**Theorem R3 (finite protected-box certificate).** Let `P=[a,b] subset B`.
For every coordinate, suppose there is a point in `R_U(P)` with `x_i=a_i`
and a point in `R_U(P)` with `x_i=b_i`. The points may differ and one point
may cover multiple endpoints. Then:

1. `T_U(P)=P`.
2. Every exact OBBT iterate from `B` contains `P`.
3. The same conclusion holds for any sequence of selected coordinate OBBT
   updates, with optional rebuilding after each update.
4. The total possible lower-bound increase is at most `a_i-l_i`; the total
   possible upper-bound decrease is at most `u_i-b_i`.

**Proof.** Since every projected point belongs to `P`, the hull is contained
in `P`. The endpoint witnesses attain all its faces, proving equality. If
`P subset B_k`, isotonicity gives `R_U(P) subset R_U(B_k)`, so every endpoint
witness is available to each coordinate support problem on `B_k`. None of
those support problems can move a bound past a face of `P`. Thus any selected
coordinate update retains `P`; induction proves both the Jacobi and sequential
claims. The distance from each current bound to the corresponding face of `P`
gives the stated ceilings. No continuity or asymptotic convergence assumption
is required. QED.

The phrase "protected" refers to this relaxation procedure. `P` need not be
an inner approximation of the original feasible set; it can contain no
original feasible points except one, or even none if the cutoff is infeasible.
Existence of this certificate proves neither original feasibility nor the
existence of a useful incumbent.

**Corollary R3a (objective-bound ceiling).** Let `P` have the certificate above,
and let `z0 in R_U(P)` have objective `v0`. For every subsequent retained box,
the relaxed objective bound `L(B_k)=min_{z in R(B_k)} v(z)` satisfies

```
L(B_k) <= v0.
```

If `Lcert <= L(B)` is a certified current lower bound, then the remaining
improvement is at most `v0-Lcert`. This upper bound remains safe when `Lcert`
is weaker than the exact current relaxation bound.

**Proof.** Isotonicity puts `z0` in every `R(B_k)`, so each minimization value
is no greater than `v0`. Also `L(B)>=Lcert`. QED.

One can minimize the affine objective over `R_U(P)` to propose a stronger
objective witness. Exact primal feasibility suffices for the ceiling; proving
that this proposal is optimal is unnecessary. A relaxation-feasible point with
objective below the true optimum supplies a gap floor, not a feasible solution.

**Corollary R3b (original sublevel points).** If `S` is a nonempty finite set of
original feasible points with objective at most `U`, then `P=box hull S` is
protected whenever their exact lifts are available. Each endpoint of `P` is
attained by a point of `S`, and validity supplies its lift in `R_U(P)`.
Unlike generic relaxation witnesses, these original feasible points survive
all additional cuts valid for the original sublevel set. Obtaining exact
original feasible lifts, particularly for nonlinear equalities, can be hard.

**A concrete objective gap certificate.** On `[-1,1]^3`, consider

```
f(x) = x1^2+x2^2+x3^2+x1*x2+x1*x3+x2*x3
     = (||x||_2^2 + (x1+x2+x3)^2)/2.
```

The unique original optimum is `x=0`, with value zero. Use square variables
`s_i`, product variables `w_ij`, the McCormick rows, the fixed rows `s_i>=0`,
and cutoff `sum s_i+sum w_ij<=0`. At the face `x_i=+1` or `-1`, set the other
original variables to zero, `s_i=1`, the other squares to zero, the two products
involving `i` to zero, and the opposite product to `-1`. This is a feasible
endpoint witness with objective zero. All six faces are protected. At `x=0`,
set all squares to zero and all three products to `-1`; the objective is `-3`.
Every subsequent OBBT relaxation therefore has objective bound at most `-3`.
The bound is exactly `-3`: every square is nonnegative and every product is at
least `-1`. These same points satisfy exact convex square epigraphs, so the
stall is not caused by allowing negative square variables. This instantiates
the existing iterated-OBBT study's row-stall mechanism; it is not a new stall
example claimed against that study.

## R4. Reuse after a cutoff or domain change

A finite witness pool `W` for a protected `P` has the exact cutoff threshold

```
U_required = max_{z in W} v(z).
```

The same certificate remains valid for any cutoff `U' >= U_required` and any
current box `B'` containing `P`, provided the relaxation family and fixed rows
are unchanged. This includes genuine improvements of the incumbent. It also
includes node boxes that still contain `P`; arbitrary children need not do so.
The threshold applies to the retained pool. Removing a redundant high-objective
witness and rechecking endpoint coverage can lower it.

If `U'<U_required`, loss of the certificate does not prove tightening is useful.
If a new box excludes part of `P`, intersecting `P` with that box does not
automatically produce a protected box. Rebuild the candidate relaxation and
recheck its endpoint witnesses. Adding valid cuts can eliminate relaxation-only
witnesses; model identity and locality must therefore be part of cache keys.

**Proposition R4a (mixing within the current relaxation).** Let `z,a in R(B)`
with `v(a)<=U<v(z)`. Then

```
theta = (U-v(a))/(v(z)-v(a)),
z_U   = a + theta*(z-a)
```

belongs to `R_U(B)`. If `v(z)<=U`, use `z` itself.

**Proof.** `0<=theta<1`; convexity gives feasibility in `R(B)`, and the affine
objective of the mixture is exactly `U`. QED.

The anchor may be a lifted incumbent, but any relaxation-feasible anchor below
the cutoff suffices. This operation gives current-round screening points. It
does not justify rebuilding their coordinate hull without another check. For
example, on `[-1,1]` the square graph points `(x,w)=(+1,1),(-1,1)` mixed with
`(0,0)` to cutoff `1/4` give `(+1/4,1/4),(-1/4,1/4)`. Both are feasible in the
old relaxation, but violate the square secant `w<=1/16` on their new hull.

**Proposition R4b (exact frontier of a cached convex pool).** Let
`W={z1,...,zk} subset R(B)` be finite. To attain every coordinate minimum and
maximum over `conv(W) intersect {v<=U}`, it suffices to examine:

- original points `zj` with `v(zj)<=U`;
- the mixtures at objective exactly `U` of each pair with one objective
  strictly below `U` and one strictly above it.

**Proof.** Write a pooled point as `sum_j lambda_j z_j`, with `lambda>=0`,
`sum lambda=1`, and `sum lambda_j v(z_j)<=U`. Every extreme point of this
coefficient polytope either has one positive coefficient or has two positive
coefficients and an active cutoff. Otherwise a nonzero perturbation preserving
the one or two active affine equations keeps both signs feasible, contradicting
extremality. Linear coordinate objectives attain their extrema at such points.
Their images are precisely the listed originals and pair mixtures. QED.

This yields all coordinate-optimal pooled witnesses with at most quadratic
many candidate mixtures and no new LP. It optimizes over the cached convex
hull, not over the whole relaxation. An empty hull intersection means that the
cache cannot help, not that the relaxation is infeasible. On a new node box,
check cached points against the rebuilt rows before applying this proposition.

## R5. Uniform sensitivity and the remaining residual tail

Use outward endpoint coordinates `p=(u,-l)` and let `F_U(p)` be the same
coordinates of `T_U(B(p))`. Then `F_U(p)<=p` and `F_U` is order preserving.
The protected-box theorem supplies an invariant order interval
`D=[p_protected,p_current]` when its assumptions hold.

**Theorem R5 (finite matrix majorant).** On an invariant region `D`, suppose
the exact Jacobi map satisfies the verified, componentwise inequality

```
|F_U(p)-F_U(q)| <= M |p-q|       for all p,q in D,              (R5)
```

where `M>=0` is fixed. Let `p1=F_U(p0)` and `d=p0-p1`. If `e>=0` satisfies

```
d + M e <= e,                                                   (R6)
```

then every remaining total endpoint displacement from `p0` is at most `e`;
the total displacement after completing the first round is at most `e-d`.
If `rho(M)<1`, one valid choice is `e=(I-M)^(-1)d`.

**Proof.** Put `d_k=p_k-p_{k+1}>=0`. Applying (R5) to consecutive iterates
gives `d_{k+1}<=M d_k`, hence `d_k<=M^k d`. From (R6), induction gives
`sum_{j=0}^{N-1} M^j d <= e-M^N e <= e`. Taking the increasing limit of the
partial displacement sums proves the result. Subtracting the exact first
displacement proves the after-round bound. If `rho(M)<1`, the nonnegative
Neumann series gives `(I-M)^(-1)d` and equality in (R6). QED.

The supermajorant form (R6) can succeed even with a noncontracting inactive
coordinate: `M=diag(1,1/2)`, `d=(0,1/2)`, `e=(0,1)` satisfy it. Thus a global
spectral-radius test is sufficient, not necessary for a finite tail bound.
If a certified upper bound `dbar>=d` is available, replacing `d` by `dbar` in
(R6) still bounds total movement. The after-round bound is then `e-d_actual`
if the actual exact first displacement is known. It is not `e-dbar`.

An observed displacement from a selective, interrupted, or inaccurate round
is not generally an upper bound on the exact Jacobi residual. It may be zero
while unprocessed directions admit large changes. R5 must not be applied to
such a displacement merely because the code labels it a round.

A rational `v>0` and rational `q<1` with `Mv<=qv` provide a checkable sufficient
condition for `rho(M)<1` in the weighted maximum norm. Alternatively, one can
verify a rational candidate `e` directly by (R6), avoiding a numerical spectral
radius. Neither arithmetic check establishes the uniform sensitivity hypothesis
(R5). A fitted observed ratio or a derivative at one active LP basis is
insufficient. [The constrained note](constrained-obbt.md) develops finite
verified sensitivity constructions under explicit basis-cover assumptions.

**A finite rebuilt-McCormick example.** Use `x in [0,u]`, square McCormick
rows, and cutoff `w<=r^2`, where `u>=r>0`. Then

```
F(u) = (u^2+r^2)/(2u),
F'(u) = (1-r^2/u^2)/2.
```

The upper-endpoint tangent gives the upper bound; `(F(u),r^2)` is a feasible
lift, proving attainment. The lower endpoint remains zero. On the invariant
interval `[r,u0]`, a verified uniform constant is
`q=(1-r^2/u0^2)/2<1/2`. Thus the residual divided by `1-q` bounds all future
upper-bound movement. For `r=1,u0=2`, the residual is `3/4`, `q=3/8`, and the
ceiling is `6/5`, compared with the actual total movement `1`. This explicit
result concerns a finite LP approximation of a square and remains valid while
the endpoint tangents are rebuilt.

**Counterexample to using a fitted residual ratio.** The scalar map

```
F(s) = 3s/4                 for 0<=s<=1/2,
F(s) = s/4+1/4              for 1/2<=s<=1
```

is continuous, monotone, and contractive in the order sense `F(s)<=s`. Starting
at `1`, the first two iterates are `1/2` and `3/8`. Successive observed
displacements have ratio `1/4`. Extrapolating that ratio would bound movement
from `1/2` by `(1/8)/(1-1/4)=1/6`, but the actual limit is zero and the remaining
movement is `1/2`. The valid uniform Lipschitz constant is `3/4`. Order
monotonicity alone does not justify an empirical geometric tail certificate.

**Cutoff perturbation.** If, on a common invariant region and cutoff interval,
one has the stronger uniform estimate

```
|F_U(p)-F_V(q)| <= M|p-q| + h|U-V|,
```

with `h>=0` and `rho(M)<1`, then fixed points in that region satisfy
`|p_U-p_V| <= (I-M)^(-1)h|U-V|`. Apply the estimate at the fixed points,
iterate the resulting nonnegative inequality, and use `M^k -> 0`.
Without this uniform cutoff estimate, a previous residual certificate cannot
be transferred to a tighter cutoff. Recompute it or use the explicit witness
thresholds and same-domain mixing above.

## R6. Implemented construction, checks, and limitations

[`certificates.py`](certificates.py) contains a reusable exact checker for
rational fixed linear rows and McCormick product lifts. It provides:

- `current_round_ceilings`: feasible primal points bound one frozen LP round;
- `verify_protected_box`: exact row and endpoint-support verification;
- `ProtectedBox.reusable` and `.ceilings`: same-model, containing-domain, and
  cutoff checks before reusing an all-future certificate;
- `mix_for_cutoff` and `cutoff_frontier`: exact reuse of a finite convex pool;
- `discover_protected_box`: floating endpoint LP proposals, rational recovery,
  hull construction, and exact checking on the rebuilt hull;
- `check_tail_majorant`: arithmetic verification of (R6), with the residual
  and uniform sensitivity matrix explicitly supplied hypotheses.

`ProtectedBox` verifies its invariant on direct construction too; an unchecked
instance is not accepted merely because it has the expected Python type.
Exact input coefficients use integers, rational strings, or `Fraction` values.
Floating coefficients must first be given an explicit intended rational model.
The model object compares row data; it does not carry or prove node-local row
provenance. The caller must establish that every fixed row is valid for the
original sublevel set on the domain being considered. Equal row arrays alone
do not establish this validity or authorize moving a local row to another
node. Without it, the checker still describes the supplied LP family but makes
no valid-domain-reduction claim for the original problem.
The discovery procedure rationalizes floating proposals, but the verifier
accepts only exact row satisfaction, exact endpoint attainment, and exact
cutoff satisfaction. Failure is inconclusive. In particular, a tolerance-based
feasibility status from an LP solver is never itself a certificate.

Discovery needs up to `2n` endpoint LP proposals. The optional objective proposal
adds one LP after a protected box is found. This cost is comparable to one
OBBT round, so the procedure does not solve the general cheap-starting problem.
It can also consume already available proposals through its callback. Certificates
can amortize their cost across later rounds and compatible cutoff/node states,
but the present small checks do not demonstrate a net solver speedup.

Targeted command:

```
python3 research-20261003-adaptive-obbt/theory/check_remaining_benefit.py --with-lp-proposals
```

The checks cover exact graph-row validity, frozen versus rebuilt witnesses,
coordinate and objective ceilings, fixed coupling rows, direct-construction
validation, cutoff/domain/model invalidation, genuine compatible cutoff reuse,
mixture frontiers, degenerate boxes, matrix tails, and the misleading-ratio
counterexample. Automatic discovery finds exact certificates on six of eight
fixed fixtures: three simple square-stall fixtures, the three-variable example
with nonnegative squares, and two linear models. On both strictly contracting
square examples it correctly returns inconclusive; it does not round a small
residual into a false fixed point. Each automatic result is
replayed through the exact verifier and reports all proposal LP calls and
elapsed time, including the checks. These are correctness demonstrations,
not held-out computational-performance evidence or CI results.

[`certified_driver.py`](certified_driver.py) makes the stopping certificate
operational in a standalone closure procedure. For each directional LP, the
numerical solver proposes both a primal point and inequality dual multipliers.
For `min c^T z` subject to `A z<=b`, the checker verifies exactly

```
A z<=b,  lambda<=0,  A^T lambda=c,  c^T z=lambda^T b.
```

Weak duality then proves the proposed endpoint optimum. All variable bounds
are explicit rows, and the numerical LP variables are otherwise free. Only
after every endpoint proof in a Jacobi round passes does the driver replace
the box by their coordinate hull. It then checks those witnesses on the
rebuilt hull. A successful check stops with a protected fixed box. A failed
fixed-box check continues safely; failed primal/dual reconstruction discards
the incomplete round and returns `inconclusive`. A round limit returns
`unfinished`, never `fixed`. Prior certified rounds remain available in either
case. The driver retains proofs and counts all proposal LP calls and total
elapsed time, including rational verification.

Targeted workflow command:

```
python3 research-20261003-adaptive-obbt/theory/check_certified_driver.py
```

The three-variable stall stops after six endpoint LPs plus one objective LP,
with ceiling `-3`. The coupled linear fixture reaches its fixed box
`[1/2,2]^2` after four endpoint LPs. The zero-cutoff square example is correctly
unfinished after five rounds and ten LPs, at upper bound `1/32`. The positive
cutoff example starting at upper bound `2` has upper bound `3281/3280` after
three certified rounds. When asked to continue, numerical rational recovery
fails exact primal replay at a later endpoint; the driver reports
`inconclusive` and preserves that last certified box. This is a useful limit
of the implementation, not a mathematical stall. The workflow checks also
cover negative variable bounds, a zero round budget, invalid dual proofs,
incomplete-round rollback, preservation of previous rounds, and a failed
optional objective proposal. Exact dual residuals are never silently rounded
away.

The protected-box procedure certifies the specified relaxation family. It is
not wired into the native solver's all-future stopping decision, because native
cut generation and additional domain reductions do not satisfy this fixed-family
contract automatically. The native experiment and these exact demonstrations
therefore have different certification scopes.
