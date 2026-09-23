# Independent review: degree-two physical vertex certificate

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the physical interface, economics, and exact optimizer count
in [the draft](pooling-degree-two-vertex-forcing.md) pass this independent
mathematical audit.** The statement retains exact flow contracts and
does not establish NP-hardness.

Replacing the former terminal output's quality bound is necessary: its
new redundant upper bound must be 1, as the completed draft states.
The exact terminal demand then gives source A bypass `1-t` and pool
intake `t`. Exact pool throughput and source B supply give B intake
`1-t` and bypass `t`. Exact waste demand gives pool waste `1-t`, so
the pool's other output is `t`. Its positive fixed throughput makes its
quality uniquely `2-t`.

The waste upper quality 2 is redundant, while primary upper quality 1
with a zero-quality clean source gives exactly `z>=t-t^2`. Every
`t in [0,1]` admits this choice with `0<=z<=1/4`, within every arc
and output bound. Thus the interface introduces no extra restriction
on the original Klee-Minty path coordinates. There is no division at
zero endpoint flow: the pool itself always carries one unit.

The completed nonnegative production-cost/output-revenue formula also
checks out without any objective offset. Subtracting one from every
input cost and output revenue cancels by mass conservation. New outputs
then have zero revenue, A and B have zero cost, and clean source Z has
cost one. Path source `j` has cost `R_(j-1)=s_j-1`, while adjacent
output revenue difference is `3s_j` for `j<n` and zero at the last
source. The extra terminal inflow has zero revenue after the shift.
Hence profit is exactly `sum_(j<n)3s_j*t_j-z`, and
`3s_j^2=(1-epsilon)epsilon^(2(n-j)-1)` at `epsilon=1/4`.

The reviewed nonnegative telescoping certificate implies that profit
is at most zero. Equality forces a path vertex and the minimal clean
flow `z=t-t^2`. Conversely every path vertex extends with those values
to zero profit. All original path flows, all added flows, and the sole
pool quality are then unique. Consequently the original physical
decision variables have exactly `2^n` isolated global optimizers.

Every input and output has degree at most two, and the pool has two
incoming and two outgoing arcs. Removing the pool leaves one extended
original path and two isolated bypass edges. The full graph is connected
with `2n+7` nodes and `2n+7` edges, hence has one undirected cycle,
namely the pool/B/waste triangle. The topology statements are accurate.

Common positive quality scaling preserves every constraint; bounds
remain finite with polynomial binary encoding length. The statement
does not remove lower flow contracts, realize the dense weighted slab,
or establish hardness merely from the large finite optimizer set.
This review concerns the complete proof. An original-model numerical
checker, if added, should be reported separately and cannot establish
the exact optimizer count by finite sampling.

## Exact integer dimension of the optimal set

The added Section 5 corollary passes this independent check. For distinct
path vertices, their endpoint coordinates differ. Since `F` is linear
minus the endpoint square and is zero at both vertices,
`F((x+x')/2)=(t-t')^2/4>0`. Thus the midpoint of any two distinct
optimal physical states is absent from the optimal set, whether or not
the uniquely determined active pool quality is retained as a coordinate.

Choosing one lift of each of the `2^n` optimal states, fewer than `n`
integer coordinates give fewer than `2^n` parity classes. Two lifts
would have an integral midpoint inside the convex lift, contradicting
the physical midpoint exclusion. Arbitrary continuous auxiliaries,
unbounded integer ranges, and nonpolyhedral convex lifts do not change
this argument.

For the upper bound, in `conv{(s(u),u):u in {0,1}^n}` an integral
last-coordinate vector must be binary. A convex combination attaining
that binary vector can use only vertices with exactly that same label,
because each label coordinate is already at an endpoint of `[0,1]`.
Thus requiring the last `n` coordinates to be integer selects precisely
the original optimal states. This proves equality at `n` for both
integer and binary dimension, without a polynomial-size representation
claim. The draft correctly attributes the lower-bound method to the
established parity argument and restricts its conclusion to representing
the complete optimal set, not merely its value or one optimizer.

## Physical-flow identity and general supplies

The added unweighted telescope is correct. Expanding its `j`th product
gives `s_j*t_j-t_j^2-s_j*t_(j-1)+t_(j-1)^2`. Summation cancels
all intermediate squares and gives the displayed linear coefficients;
`s_n=1` supplies the final `t_n-t_n^2` term.

The extension to positive rational supplies with `s_(j+1)>2s_j` also
passes. The lower endpoint for coordinate `j` lies in `[0,s_(j-1)]`,
while its upper endpoint lies in `[s_j-s_(j-1),s_j]`. Those ranges
are disjoint, and every endpoint interval has positive length. Each
pattern of lower/upper choices therefore gives a distinct vertex and
terminal value. The same physical capacity and midpoint-quality rows
produce these intervals, and the stated costs/revenues give coefficient
`s_(j+1)-s_j` in the objective. The two-feed interface needs only
`s_n=1`, so the rest of the proof carries over.

## Exact convex hull and recovery by linear programming

Section 6 passes. Every physical arc and the active pool quality is
affine in `(x,z)`, and the only remaining nonlinear restriction is
`g(x_n)<=z<=1`, where `g(t)=t-t^2`. The vertex certificate implies
`c^T x<=g(x_n)` everywhere on the path polytope and equality at every
path vertex. Decomposing `x` into those vertices shows that
`(x,c^T x)` belongs to the convex hull of the physical set. Since
`(x,1)` is itself physical, vertical interpolation yields every point
of the claimed hull. This proves both inclusions without assuming a
polynomial-size vertex enumeration.

The lower and upper affine boundaries are disjoint because
`c^T x<=1/4<1`. A hull vertex must lie on one of them, and its `x`
must be a path vertex: otherwise a nontrivial convex decomposition
on the same affine boundary would contradict extremality. Both lifted
boundary points over a path vertex are physical. Thus an optimal basic
feasible solution of the polynomial-size rational LP recovers an exact
physical optimizer for every linear objective. An arbitrary optimum
in the relative interior of the optimal LP face need not be physical;
the draft correctly requires a vertex solution.

The bare-path concave-quadratic observation is also correct. For
`b>=0`, the objective `a^T x-b*x_n^2` has a vertex minimizer, and it
equals `a^T x-b*L(x)` at every path vertex. The two optimization
problems therefore share their minimum and a vertex optimizer. A
dense slab may create new vertices where `L>x_n^2`, which is exactly
why this argument cannot remove the slab from the hardness reduction.

## Distinct strict local optima after price perturbation

Section 4.1 passes. Increasing the primary revenue and clean-input cost
by the same positive `delta` adds exactly `delta*t`. Along an incident
edge from a path vertex to a neighboring one, the outward derivative
is `-(t'-t)^2+delta*(t'-t)`. With geometric supplies, distinct terminal
values differ by at least `4^(-(n-1))`, whereas `delta=4^(-n)` is
strictly smaller. The derivative is therefore negative in both signs
of `t'-t`.

Incident edge rays generate the pointed tangent cone. Strict negativity
on these finitely many generators implies a uniformly negative first
derivative on its unit directions. The smooth quadratic remainder is
of second order, so a sufficiently small feasible neighborhood has
strictly smaller objective away from that vertex. Additional clean
flow only decreases profit. This establishes strict local maximality
in the original physical variables as well.

All constructed local values `delta*t` are distinct. The global bound
`profit<=delta*t<=delta` is attained only at the unique endpoint-one
vertex with minimal clean flow. Thus one is globally optimal and the
other `2^n-1` constructed strict local optima are suboptimal. The small
perturbation has polynomial binary length and keeps the stated costs
and revenues nonnegative. No dimension-independent perturbation size,
attraction basin, or local-algorithm runtime conclusion is justified.
