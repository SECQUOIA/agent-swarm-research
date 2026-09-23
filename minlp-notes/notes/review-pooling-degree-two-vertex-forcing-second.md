# Second review: degree-two physical vertex forcing

Date: 2026-09-05. Verdict: PASS for
[the physical construction](pooling-degree-two-vertex-forcing.md).
It has the stated exponentially many isolated optimal physical flow
vectors. It does not establish a pooling hardness classification.

## Projection and physical interface

The modified terminal output must have upper quality one; retaining its
former upper bound of zero would destroy the intended interface. The
completed draft explicitly makes this replacement. Its original path
inlet has quality zero and the added bypass has quality one, so the new
quality row is redundant. The waste output's upper quality two is also
redundant, since both its bypass and pool feeds have quality at most two.

Let `t` be the original terminal flow. Terminal demand and source A's
exact supply give A-bypass `1-t` and A-pool feed `t`. The exact pool
throughput then gives B-pool feed `1-t`. B's exact supply and the waste
output's exact demand give B-bypass `t` and pool-waste flow `1-t`.
Pool balance makes its primary outflow `t`. These equations determine
all added flows except the clean flow, and all are within their unit
capacities for `t in [0,1]`.

The always-active pool has quality `2-t`. The primary upper quality row
is exactly `z>=t-t^2`; its other constraint is `t+z<=2`. Choosing
`z=t-t^2 in [0,1/4]` gives a valid extension of every original path
point. Thus the interface does not exclude any Klee–Minty point. At
`t=0` and `t=1` the same equations remain valid without division by
zero, because the pool still has throughput one.

## Ordinary economics

The proposed source costs and output revenues are correct. Subtracting
one from all source costs and output revenues leaves profit unchanged
by total external mass balance. In the resulting algebra, inputs A and
B and all newly added outputs have zero price, while the clean input
has unit cost. The terminal output has zero adjusted revenue, so its
new bypass inflow causes no missing term.

On the original path, adjusted cost at source `j` equals the adjusted
revenue of its left output. Consequently only its right flow contributes,
with coefficient `3s_j` for `j<n` and zero for `j=n`. Since
`t_j=s_j x_j`, this gives coefficient
`3s_j^2=(1-epsilon)epsilon^(2(n-j)-1)` in normalized coordinates.
Total profit is therefore exactly `c^T x-z`, with no omitted constant.
The actual, unshifted economics are nonnegative and satisfy the stated
bounds on costs and revenues.

## Optimum count and topology

The reviewed identity gives `F=t-c^T x-t^2>=0` on the path.
Primary dilution therefore implies
`profit<=c^T x-(t-t^2)=-F<=0`. Equality requires a Klee–Minty
vertex and the unique clean flow `z=t-t^2`. Every such vertex extends
and attains equality. All original path flows, all new flows, and the
active pool's quality are then determined. Hence there are exactly
`2^n` optimal physical arc-flow vectors, each isolated in this finite
optimal set. This count concerns physical flows and the active pool
quality, not redundant auxiliary variables that a different formulation
might introduce at inactive outputs.

All external inputs have at most two arcs, and all outputs at most two
incoming arcs. The pool has two incoming and two outgoing arcs. Deleting
pool-incident arcs leaves the original path extended by input A, plus
the separate B–waste and clean–primary edges, so the bypass graph is a
union of paths. In the full undirected graph, the only cycle is the
triangle B–pool–waste; the remaining edges form attached trees. It is
connected and unicyclic. The pool itself has undirected degree four,
which does not contradict the stated separate input/output degree bounds.

The geometric result does not implement the dense weighted slab from
the abstract subset-sum reduction. Exponentially many isolated optima
alone do not imply NP-hardness, and a zero-profit point is easy to exhibit
in this family. The draft states these limits correctly.

## Exact-throughput negative control

The pool's positive throughput lower bound is essential to this proof.
If only that lower bound is removed, retaining its upper bound of one
and every external supply/demand contract, the claimed zero-profit
upper bound fails. Set all normalized path coordinates before `n-1`
to zero, set `x_(n-1)=1`, and set `x_n=1/4`. This is a valid path
point. Choose

```
A-pool=1/4, A-bypass=3/4,
B-pool=0, B-bypass=1,
pool-waste=0, pool-primary=1/4, clean=0.
```

The pool has quality one and throughput one quarter, and all remaining
physical constraints hold. The profit is `c_(n-1)=3/16>0`. This does
not contradict the proposed result, which explicitly retains the exact
throughput contract and makes no contract-removal claim.

## Separate physical-network implementation

[physical_vertex_forcing_check.py](../code/parametric_path_lp/physical_vertex_forcing_check.py)
constructs original left/right path arcs, the seven added physical arcs,
all exact source and output contracts, pool balances, and homogeneous
upper quality rows. Only the actual pool quality is fixed for each LP;
no intended flow-copy or nonlinear vertex-certificate equation is inserted
into the LP. Its objective comes directly from the stated source costs
and output revenues on actual arcs.

For every vertex in dimensions two through seven, the LP recovers the
predicted path vertex, all interface flows, minimum clean dilution, and
zero economic profit. All 252 cases pass. Eighteen interior terminal
values give strictly negative optimal physical profit, as predicted by
the telescoping identity. These tests complement the exact algebra above
and do not constitute an exhaustive nonlinear solver proof.

## Exact convex-lift integer dimension of the optimal set

The subsequent Section 5 passes. Normalized path coordinates are linear
functions of physical arc flows, so taking a physical midpoint takes
their coordinatewise midpoint as well. At optimizers, `L(x)=t^2`;
linearity of `L` therefore gives

```
F((x+x')/2)=(t-t')^2/4>0
```

for distinct optimizers. Distinct terminal coordinates were proved in
the original vertex audit. Thus every pair of distinct optimal flow
vectors has its midpoint outside the optimal set.

Choose one feasible lift for each optimal point in any proposed exact
convex lift with `k` integer coordinates and arbitrary continuous
auxiliaries. If `k<n`, two of the `2^n` chosen integer vectors have
the same parity. Their midpoint is integral; convexity makes it a
feasible lifted point, whose physical projection is the forbidden
midpoint. This proves `k>=n`, regardless of bounds on the integer
variables and without a polyhedral assumption.

The matching upper construction is also exact. The convex hull of
`(s(u),u)` lies over `[0,1]^n`. Any integral label in this cube is a
binary vector. A convex combination producing that label can place
positive weight only on vertices with precisely that label, coordinate
by coordinate. There is exactly one assigned physical point for each
label, so the integer-restricted projection is exactly the desired set.
This proves minimum integer dimension `n`; it does not bound formulation
size polynomially. The hull is a finite rational polytope in this family.

I inspected the primary manuscript of
[Lubin, Vielma, and Zadik](https://optimization-online.org/wp-content/uploads/2017/06/6082.pdf),
whose Lemma 4.1 on PDF page 12 states this midpoint lower bound on MICP
rank. The attribution is appropriate. The corollary applies to an exact
representation of the full optimal set, rather than a representation of
its value or of one selected optimizer.

A separate consequence for possible future use concerns the entire
feasible set. For each `t in [0,1]`, take all normalized path coordinates
before the last to be zero, set the last to `t`, and extend the interface
with clean flow `z=t-t^2`. These are feasible physical points. For any
distinct `t,t'`, the midpoint's clean flow falls below its required
minimum by `(t-t')^2/4`, while its other interface flows still determine
the midpoint terminal value. Its midpoint is therefore infeasible.
This infinite pairwise midpoint-excluded family invokes the same known
lemma to rule out every exact finite-integer convex lift of the entire
feasible set. This is distinct from the finite optimal-set statement
and does not imply computational hardness.

## Exact convex hull and recovery of a physical optimizer

The subsequent Section 6 also passes. Every physical arc flow and the
active pool quality is affine in the path coordinates and clean flow
`(x,z)`, and the converse map is affine as well. The remaining primary
throughput inequality is redundant because `x_n,z<=1`. Thus the full
physical feasible set is affinely equivalent to
`T={(x,z):x in P_epsilon, x_n-x_n^2<=z<=1}`.

The inequality `c^T x<=x_n-x_n^2` holds everywhere on the path
polytope, with equality at every vertex. A vertex decomposition of `x`
therefore represents `(x,c^T x)` as a convex combination of points of
`T`. The upper point `(x,1)` is in `T`, and interpolation gives every
point with `c^T x<=z<=1`. This proves the stated convex hull exactly.
There is no closure or limiting argument: all decompositions are finite.

The vertex characterization is valid because the lower and upper affine
boundaries are disjoint: `c^T x<=1/4<1`. An interior vertical point
is not extreme, and a point on either boundary with nonvertex `x`
inherits a nontrivial convex decomposition from the base polytope.
Thus every hull vertex has a Klee–Minty vertex as its path coordinate
and either lower or upper `z`. Both choices are physically feasible.
The resulting rational LP has polynomial size and coefficient length.
Recovering an optimal vertex, rather than an arbitrary point on an
optimal face, gives an exact feasible optimizer for every linear physical
objective. Standard bounded LP vertex recovery suffices.

For minimization on the bare Klee–Minty polytope, the additional rank-one
quadratic statement also holds. With `b>=0`, the objective
`a^T x-b x_n^2` is concave and attains a minimum at a vertex. At every
such vertex it equals `a^T x-b L(x)`, so the two minimum values agree,
and an optimal vertex of the latter LP attains the former minimum.
The slab extension cannot inherit this conclusion: it can create new
vertices at which `L(x)>x_n^2`. For the particular hardness objective
`F=L-x_n^2`, its proposed linearization is identically zero, whereas
a constructed subset-sum no-instance has a positive minimum over its
nonempty clipped polytope.

These conclusions are compatible with the exact-set representability
obstructions. A compact convex hull can support optimization while
containing infeasible convex combinations, and therefore need not be an
exact convex lift of the original feasible set or its optimal set.

## Direct physical-flow identity and nonuniform supplies

The author's additional simplification also passes. With `t_0=0` and
`s_n=1`, expansion and cancellation give

```
sum_(j=1)^n (t_j-t_(j-1))(s_j-t_(j-1)-t_j)
  = t_n-t_n^2-sum_(j<n)(s_(j+1)-s_j)t_j.
```

Each summand expands to
`s_j t_j-t_j^2-s_j t_(j-1)+t_(j-1)^2`. This yields a proof
directly in the physical rightward flows, without normalizing them or
introducing geometric weights.

The construction extends to positive rational supplies ending in
`s_n=1` and satisfying `s_(j+1)>2s_j`. Induction gives
`0<=t_j<=s_j`; the two conditional bounds
`t_(j-1)<=t_j<=s_j-t_(j-1)` are distinct because
`2t_(j-1)<=2s_(j-1)<s_j`. All endpoint patterns are feasible
vertices. Their terminal coordinates are distinct: lower endpoint values
lie in `[0,s_(n-1)]`, upper endpoint values in
`[s_n-s_(n-1),s_n]`; these intervals are disjoint, and each branch
recovers the preceding coordinate. Apply the same argument recursively.

The standard economics still produces the linear coefficients
`s_(j+1)-s_j`. Consequently the same vertex-forcing and isolated-optimum
proof applies. For the convex hull, replace `c^T x` by
`sum_(j<n)(s_(j+1)-s_j)t_j`; the identity bounds this affine function
by `t_n-t_n^2<=1/4` and gives equality at every path vertex. The
previous finite convex-decomposition argument then applies verbatim.
All source costs and the path output revenues remain at most one.

## Strict local maxima with distinct objective values

The later price-perturbation subsection passes for the geometric supplies.
Increasing the primary revenue and clean-input cost by the same
`delta=4^(-n)` adds exactly `delta*t` to physical profit. On the
least-clean-flow boundary the reduced objective is `H=-F+delta*x_n`.
Along an incident edge from terminal value `t` to `t'`, its outward
derivative is `-(t'-t)^2+delta*(t'-t)`. Every vertex terminal value
has denominator dividing `4^(n-1)`, so every nonzero terminal difference
has magnitude at least `4^(-(n-1))`, strictly larger than `delta`.
The derivative is therefore negative for either sign of the difference.

Strict negativity on finitely many edge rays does imply a strict local
maximum here. Those rays generate the tangent cone at the vertex. After
normalizing directions, their negativity bounds the first-order change
above by `-m||d||` for some positive `m` depending on that vertex.
The quadratic remainder is at most `||d||^2`, so sufficiently small
nonzero feasible displacements decrease the objective. In physical
coordinates use clean slack `h=z-(t-t^2)>=0`: profit is `H(x)-h`.
The affine physical parameterization and continuity of this change of
slack variable preserve strict local optimality.

The constructed local values are `delta*t` and are all distinct.
Every feasible profit is at most `delta*t<=delta`. Equality forces
the unique path point with `t=1`, whose preceding coordinates are all
zero, and the least clean flow. Thus exactly one constructed local
maximum is global. The new actual prices remain nonnegative and below
three. The dimension-dependent perturbation gives no fixed numerical
robustness radius, attraction-basin size, or local-solver runtime bound.

The optimal-set integer-dimension statement must continue to refer to
the original unperturbed economics; its perturbed global optimal set is
a singleton. This scope clarification was sent to the author.

[exact_strict_local_check.py](../code/parametric_path_lp/exact_strict_local_check.py)
passed 2,044 distinct local-value checks and 18,432 exact negative
directed-edge derivative checks through dimension ten, including the
edge interpolation identity and uniqueness of the terminal-one vertex.
