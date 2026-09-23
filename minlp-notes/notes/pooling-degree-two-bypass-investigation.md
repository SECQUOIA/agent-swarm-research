# Degree-two bypass paths: an exponential price-response obstruction

Date: 2026-09-05. Status: physical embedding, uniform penalty, output-price
representation and algebraic lower bound independently reviewed. No
pooling hardness or polynomial-time classification is claimed.

The degree-two bypass question remains open. The current structural
algorithm handles bounded vertex integrity, which excludes arbitrarily
long paths. A general polynomial-size symbolic support formula for path
components cannot fill that gap: even a physical blending path with one
upper quality has exponentially many optimal price regimes. This note
records the exact embedding and a way to remove fixed source contracts.

Later work records an actual one-pool endpoint interface in
[pooling-degree-two-vertex-forcing.md](pooling-degree-two-vertex-forcing.md).
It has exponentially many isolated optimizers but also an explicit
polynomial-size LP convex hull. The weighted aggregate needed for the
abstract path/slab hardness result is still not physically realized.

## 1. A primary-source obstruction to the generic path argument

Gärtner, Helbling, Ota and Takahashi prove that the Klee–Minty cube has
an exponential two-dimensional shadow even though each inequality uses
at most two variables. Their [open paper](https://arxiv.org/pdf/1308.2495),
Section 4, uses the scalar path constraints

```
0<=z_1<=1,
epsilon z_(j-1)<=z_j<=1-epsilon z_(j-1),  j=2,...,n.
```

Fix `epsilon=1/4`. With `c_j=epsilon^(3(n-j))` for `j<n` and `c_n=0`,
the objective `c^T z+lambda z_n` uniquely exposes every one of the `2^n`
vertices for suitable `lambda` in `[-1/15,1/15]`. Consequently its value
has `2^n` distinct affine pieces on that interval. The explicit rational
exposing parameters and independent checks are preserved in
[the obstruction audit](parametric-path-lp-obstructions.md).
This is an established shadow result, not a new combinatorial theorem.

The pointwise LP remains polynomial-time solvable. In fact backward
elimination uses a short nested absolute-value recurrence, recorded in
[the path-LP investigation](parametric-path-lp-investigation.md). Thus a
large explicit response curve does not prove optimization is hard.

## 2. Exact realization by a physical blending path

Use `n>=2` inputs and `n+1` outputs numbered `0,...,n`. Input `j`
has quality `C_j=n-j` and exact supply `D_j=4^(j-1)`. Its only outgoing
arcs go left to output `j-1` and right to output `j`, each with capacity
`D_j`. Write the rightward flow as `x_j`; the leftward flow is then
`D_j-x_j`.

For `j=2,...,n`, internal output `j-1` has upper throughput `D_j`
and upper quality `(C_(j-1)+C_j)/2`. It receives
`x_(j-1)+D_j-x_j`. Its capacity gives `x_j>=x_(j-1)`. Since consecutive
input qualities differ by one, its upper quality condition is equivalent
to `x_(j-1)<=D_j-x_j`. Thus its two constraints are exactly

```
x_(j-1)<=x_j<=D_j-x_(j-1).
```

The two endpoint outputs have capacities `D_1,D_n` and upper qualities
`C_1,C_n`; their quality rows are redundant. Nonnegativity supplies the
remaining endpoint bounds. With `z_j=x_j/D_j`, these are precisely the
Klee–Minty inequalities at `epsilon=1/4`.

Conversely, every Klee–Minty point gives these physical flows, satisfying
all supplies, capacities and upper quality specifications. The mapping is
affine and bijective. The bypass graph is a single path; every input and
output has degree at most two. There are no pools in this LP component.
It can occur as a bypass component in a larger fixed-pool instance, but
this embedding makes no claim that an active pool is needed.

Divide all flows and capacities by `D_n`. Put

```
s_j=D_j/D_n=4^(j-n),
t_j=x_j/D_n=s_j z_j.
```

Every upper capacity is now at most one. Divide all quality values and
bounds by `n-1` to put them in `[0,1]`. The same constraints and mapping
hold. All rational data have polynomial encoding length. The source
shadow objective becomes

```
sum_(j<n) w_j t_j + lambda t_n,
w_j=c_j/s_j=16^(j-n).
```

In particular its physical coefficients are bounded; the example does
not rely on large base reward values.

## 3. A single varying output price and nonnegative economics

Define `w_n=lambda` and output base revenues

```
R_0=1,
R_j=1+sum_(h=1)^j w_h,       j=1,...,n.
```

All revenues lie in `[0,2]` uniformly for
`lambda in [-1/15,1/15]`. Only the final output's revenue depends on
`lambda`; every other price is constant. Set input production costs to
zero. On the exact-supply network, total revenue is

```
sum_j [ R_(j-1)(s_j-t_j)+R_j t_j ]
  = C0 + sum_j w_j t_j,
C0=sum_j R_(j-1) s_j.
```

The constant `C0` is independent of `lambda`, because it excludes `R_n`.
Thus varying one terminal price already exposes all `2^n` operating
regimes with ordinary nonnegative output revenues.

## 4. Remove the input supply lower bounds uniformly in price

Let `Q` be the exact-supply physical path polytope in its `N=2n`
individual arc flows. Let `A` contain nonnegativity, all arc/output/input
upper capacities and all upper quality rows. Let `Ew=s` give the exact
input supplies. Dropping those equalities while retaining their upper
bounds gives deficits `Delta=s-Ew>=0` and `delta=sum Delta`.

All coefficient rows can be scaled to integer entries in `{-1,0,1}`:
internal upper quality rows reduce to right-predecessor flow minus left-
current flow at most zero, and all other rows are ordinary mass bounds.
The contract rows are unscaled zero-one rows. The reviewed explicit
[polyhedral error bound](../results/pooling-one-pool-upper-bounds-np-completeness.md#2-explicit-rational-error-bound-for-restoring-contracts)
therefore gives a point `w' in Q` with

```
||w'-w||_1 <= H delta,       H=N^N.
```

The unpenalized physical revenue vector has every entry in `[0,2]`
uniformly in the price parameter. Therefore the loss in base revenue on
repair is at most `2H delta`. Choose `M=2H+1` and add `M` to every
output's unit revenue. By total mass conservation, this rewards total
input throughput by `M`; no input cost or additional arc is needed.
For every feasible upper-only flow,

```
new_revenue-M sum_j s_j
 = base_revenue-M delta
 <= base_revenue(w')-(M-2H)delta.
```

Every exact-supply point attains deficit zero. Consequently, uniformly
throughout the price interval,

```
V_upper(lambda) = M sum_j s_j + C0 + h_KM(lambda).
```

This formula is exact. All positive lower flow bounds have been removed;
all remaining quality constraints are upper bounds on one scalar quality.
Capacities remain at most one, the graph remains a path of maximum degree
two, all production costs are zero, and every output revenue is positive.
Only the final output price varies. The penalty `M` has `O(n log n)`
bits. This is a useful lower bound on explicit response-curve complexity,
not an NP-hardness proof: every fixed-price instance is still an LP.

## 5. Consequence for symbolic elimination

An exact piecewise-affine price-response table needs at least `2^n`
pieces. More generally, a quantifier-free formula in `(lambda,v)` using
polynomials and Boolean operations, defining either its graph or its
epigraph on the price interval, needs total polynomial degree at least
`2^n`. At an interior point of each open graph segment, some defining
polynomial must vanish; otherwise all polynomial signs would be locally
constant and could not define that boundary. On each segment, the product
of all nonzero defining polynomials therefore vanishes identically on a
nonempty line interval, so its distinct affine supporting line divides
that product. There are `2^n` distinct supporting lines. Their product's
degree cannot exceed the sum of defining degrees. Zero polynomials can
be removed as constant truth values. This establishes the bound.

This does not exclude a compact arithmetic circuit, an existential
extended formulation, implicit evaluation, or a polynomial algorithm that
avoids constructing the whole response curve. The remaining degree-two
pooling classification needs a different argument.

## 6. Verification and remaining scope

The [author checker](../code/pooling_bypass_paths/check_shadow.py) builds
physical input equations and output capacity/quality rows. For every
vertex witness through `n=6`, it solves the original active network rows
exactly and constructs an exact dual certificate with strictly positive
multipliers on the chosen inequality rows. Full row rank and positive
multipliers certify the unique original-network maximizer, without
inserting Klee–Minty constraints into that LP. It also checks every other
physical inequality, distinct terminal flows, bounded nonnegative prices
and the revenue identity. All 126 exact primal/dual certificates passed;
its [log](../code/pooling_bypass_paths/shadow_output.txt) is retained.

Both independent reviewers checked the physical embedding. Their generic
source audit checks 8,190 exposing witnesses and 8,178 exact breakpoints
through dimension twelve. The
[first final review](review-pooling-degree-two-price-response.md) and
[second final review](review-pooling-degree-two-price-response-second.md)
both pass the all-upper-flow terminal-price packaging and quantifier-free
consequence. The second reviewer additionally built the upper-only
physical LP with the actual theoretical `M=2(2n)^(2n)+1` and certified
252 exposed optima through dimension seven by exact primal/dual
arithmetic, including feasibility, nonsingularity, strictly positive
dual multipliers and the exact objective offset. Its
[checker](../code/parametric_path_lp/exact_physical_penalty_check.py)
is retained. The
embedding is recorded as an application of established shadow theory;
its separate literature priority is unclaimed.

## 7. A separate limit on coordinate-port universality

There is a simple structural obstruction to replacing every degree-three
node in the new LP representation by a degree-two bypass gadget. In a
pool-free network of maximum degree two, every supply, demand, arc bound
and output quality constraint contains at most two arc-flow variables.
This remains true with arbitrarily many quality coordinates and with
either upper or lower bounds. No additional global objective-threshold
row or nonphysical side constraints are included in this statement.
Its physical feasible set is therefore a system
with at most two variables per inequality.

Such systems are closed under coordinate projection. Fourier–Motzkin
elimination pairs an inequality involving the eliminated variable and
at most one other coordinate with another such inequality; the resulting
row contains at most two remaining coordinates. Repeating elimination
gives an exact finite two-variable-per-inequality description of any
coordinate projection. The number of resulting rows need not be
polynomial; no efficient elimination claim follows.

Consequently a degree-two bypass network cannot represent every linear
polytope by designating single arc flows as its original variables. For
example, the full-dimensional simplex
`{x in R^3: x>=0, x_1+x_2+x_3<=1}` cannot have a two-variable inequality
description. The point `(1/2,1/2,1/2)` satisfies every valid inequality
involving at most two coordinates: its coordinates on any such pair
extend to a simplex point by setting the third coordinate to zero.
Yet the point is outside the simplex. Equivalently, its non-coordinate
facet has three nonzero normal entries.
This does not exclude arbitrary linear-image representations, which is
why it does not conflict with the exponential two-dimensional shadow.

The independently reviewed degree-three construction does represent
arbitrary rational linear systems on bounded signals in `[0,2]` by
designated port coordinates. Thus
degree three is sufficient and degree two is insufficient for this
specific LP representation property. The obstruction is an application
of elementary elimination, with separate novelty unclaimed. Both current
reviewers passed this argument and identified the explicit bounded-signal
and no-global-side-row qualifications now stated here.

## 8. A fixed-alphabet route and its limitation

The physical path constructions above use `n` distinct input qualities
in strict descending order. Fixing the number of distinct input-quality
values, in addition to pool count and bypass degree two, may therefore
be a different structural boundary. This means the number of distinct
vectors, not their affine rank; the displayed path already has rank one.

A simple attempted reuse of the path gadget with alternating qualities
0 and 1 fails to preserve its interval recursion. At a high-to-low
boundary with upper specification `1/2`, the quality row is
`t_(j-1)<=s_j-t_j`; at a low-to-high boundary it reverses to
`s_j-t_j<=t_(j-1)`. The ordinary output upper capacity always gives
a lower bound on `t_j`, so the second case supplies two lower bounds
instead of the two opposing Klee–Minty bounds. This observation only
rejects that direct embedding. It proves neither a polynomial algorithm
nor hardness for a bounded quality alphabet. The fixed-alphabet hardness
result elsewhere in the repository uses output degree three.

The subsequent [quality-reset construction](degree-two-fixed-quality-alphabet-investigation.md)
resolves this particular representability question: exact-demand relays
copy the signal while resetting quality zero to one. Two input-quality
values already suffice for the exponential linear price response, even
with all lower flow bounds removed by a uniform exact penalty. Three
values suffice for the reviewed nonlinear vertex-forcing geometry with
its explicit contracts. Thus bounded quality alphabet alone does not
remove that response-complexity obstruction.

The independent [boundary-projection result](pooling-degree-two-boundary-projection.md)
instead gives polynomial feasibility, and optimization on a fixed number
of retained arc coordinates, with arbitrary many qualities. Its key
restriction is the absence of a dense eliminated cost coordinate, not
the quality alphabet. Dense-profit classification remains unresolved.
