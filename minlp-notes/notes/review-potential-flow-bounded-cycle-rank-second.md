# Second independent audit: bounded cycle rank in every block

Date: 2026-09-05.
Reviewer: independent agent `graph_precision_second_review`.
Source: `notes/potential-flow-block-cycle-rank-investigation.md`.

## Verdict

The quadratic-law candidate passes this second independent mathematical
audit. The positive-source objective perturbation resolves the flat-path
obstruction, including coincident endpoint adjoints and two-vertex peak
plateaus. The topology bounds, finite-face limit, fixed-dimensional
algebraic optimization, interval aggregation, and rational recovery are
valid. I found no substantive counterexample or proof gap.

I requested explicit treatment of bridge blocks and faces with no free
nomination coordinates; the author reports both clarifications have been
added. They bypass formulas intended for non-bridge blocks and do not
change the theorem. This review covers the quadratic-law theorem, not
the tentative extension to other piecewise polynomial laws, and makes no
literature-priority claim.

The polynomial-time statement is for each fixed bound on block cycle
rank. It does not prove fixed-parameter tractability when that bound is
part of the input. Independent interval nominations, balance, positive
resistances, and absence of additional physical bounds remain essential.

## Global localization to one block

For positive law smoothing, the adjoint of the unperturbed global
objective is an electrical unit `s-t` potential. After off-path
aggregation, each objective-path block transmits the unit current between
its entrance and exit. Within a non-bridge biconnected block, every
internal vertex has adjoint strictly between those two boundary values.
Indeed, an internal maximum at the entrance value would propagate along
a path to the exit that avoids the entrance, contradicting the distinct
boundary values; biconnectivity supplies such a path. The minimum case is
symmetric. Bridges have a strict decrease directly.

The open ranges of consecutive blocks are disjoint and ordered. The
linear-programming balance multiplier therefore localizes every possible
free load to one block, with the stated saturation outside it. If it
matches an articulation, that vertex is the only possible free core
vertex and can belong to either incident selected block. Terminal and
all-upper/all-lower cases use the first or last block.

The established joint smoothing/nomination compactness proof applies on
arbitrary connected graphs; it uses cubic energy and tree routings, not
cactus structure. It therefore passes this global one-block face
statement to the original law. Off-path aggregation and the fixed
outside nominations produce a local balanced interval problem by shifting
entrance and exit intervals by fixed rational totals. Changing the local
nomination while preserving its sum changes no outside block's effective
loads, so their drops remain constant.

## Suppression topology and parallel paths

In a non-bridge biconnected block every degree is at least two. Therefore
`sum_v(deg(v)-2)=2r_H-2` bounds the number of degree-at-least-three vertices
by `2r_H-2`. Including the two distinct local objective terminals gives
`|K|<=2r_H`, whether neither, one, or both terminals originally have
degree two.

Every remaining vertex has degree two. Its connected component after
removing `K` belongs to a path between marked vertices: a component that
closed into an isolated cycle could not connect to `K`, whereas the block
is connected and `K` contains the terminals. Suppressing these interiors
preserves cycle rank. The connected suppressed multigraph has `|K|`
vertices, so its number of edges/paths is exactly
`p=r_H+|K|-1<=3r_H-1`.

Parallel suppressed paths are legitimate and do not affect any count or
argument. A rank-one block has two terminal branches. Internal degree-two
paths are disjoint; their endpoints can be shared core vertices, which
are handled only once by the core-state enumeration. Direct edges
between marked vertices have no internal nomination to classify.

A bridge has `r_H=0` and two vertices. The expressions `8r_H-3` and
`9r_H-3` are not its dimensions. Its balanced local nomination leaves at
most one scalar, and its potential difference is the monotone quadratic
edge law evaluated at that scalar. Optimize at the corresponding feasible
endpoint, or use the trivial one-dimensional algebraic problem. Fixed-load
bridges have rational drops. The author's explicit bridge bypass handles
this case.

## Perturbed adjoints and the plateau case

The local perturbed objective is a linear combination of normalized
physical potentials. Differentiating under positive smoothing gives the
same grounded electrical inverse as before, now with a source of exactly
`delta>0` at every unmarked degree-two vertex. Marked vertices have no
need for a restricted adjoint pattern because their total number is
bounded.

For a path oriented from `v_0` to `v_k`, outward electrical current at
an internal vertex is `j_i-j_(i-1)`. Thus its source equation is exactly

```
j_i-j_(i-1)=delta.
```

The sign is correct. Positive edge resistances imply
`h_(i+1)-h_i=-R_i j_i`. As the currents strictly increase, the adjoint
sequence first strictly increases and then strictly decreases. Either
part can be absent. A zero current occurs on at most one edge, producing
at most two adjacent equal vertices at the peak.

This remains true when the two marked endpoints have equal adjoints:
the sequence can arch above that common value, but cannot be a long
constant path. A level below the peak has at most one occurrence on each
strict branch; the peak has one vertex or its two-vertex plateau; a level
above the peak has none. Consequently every level has at most two
occurrences, and every strict upper-level set is an interval in the
vertex ordering. Removing the marked endpoints preserves these
properties for the internal-vertex sequence.

The nomination pattern follows from linear-programming optimality:
lower bounds outside the upper interval, upper bounds inside, and
optional free vertices at the two boundaries. A peak plateau equal to
the multiplier is specifically represented by two adjacent free pivots
and an empty upper interval. Empty intervals, all-upper paths, all-lower
paths, a single free peak, and purely monotone paths must be included.
These are all boundary/gap choices, so each path contributes only a
quadratic number of candidate patterns.

As a separate finite check, I generated 6,772 exact rational current/path
instances with one to nine edges, initial currents spanning negative,
zero, and positive values, unit positive source increments, and varied
positive resistances 1 and 3. Every attained level occurred at most twice,
and every strict upper-level set was an interval. This corroborates the
sign/plateau analysis but does not replace its proof. The author's
separate network experiment is not part of this independent count.

## Face count, dimensions, and perturbation limits

Each of the `p` paths contributes at most two internal free nominations,
and each core vertex has three possible states. Hence the number of
faces is at most `3^|K|` times a product of quadratic path-size bounds,
which is `n^{O(r)}` for fixed `r`. The number of free nominations is at
most `|K|+2p<=8r_H-2`. Every enumerated face has rational interval bounds
and the exact balance equation. Extra feasible patterns that do not arise
from any actual perturbed adjoint cannot hurt: they remain subsets of
the original nomination polytope.

If there are `f>=1` free coordinates, eliminate one using balance; this
gives at most `f-1<=8r_H-3` independent nomination coordinates. If there
are none, simply test the fixed vector's balance and omit nomination
variables. Collapsed intervals and fixed coordinates reduce dimension
further. Adding `r_H` circulation coordinates gives the stated upper
bound `9r_H-3` in the non-bridge case.

Uniform convergence of the perturbed objectives needs no quantitative
choice of either perturbation. For `rho<=1`, all physical flows are
uniformly bounded and each normalized smoothed potential has a common
bound obtained from a path sum. Thus the extra objective term is bounded
uniformly by `delta` times a fixed finite constant. The already established
uniform convergence as `rho` tends to zero completes the two-parameter
argument for arbitrary joint sequences `delta,rho -> 0`.

The local nomination polytope is compact. Any limit of corresponding
maximizers is therefore an original maximizer. Only finitely many closed
faces occur, and their defining bounds are independent of both
perturbations. Taking a subsequence in one face preserves its saturation
in the limit. There is no hidden assumption that perturbed pivots or their
adjoint levels converge with a prescribed ordering, and no perturbation
size must be computed by the algorithm.

## Flow equations and fixed-dimensional algebraic computation

A spanning-tree routing is affine in the retained nomination coordinates.
Choose fundamental cycle columns with unit coefficient on their own
non-tree edge and zero on other non-tree edges. Adding their linear
combination parameterizes every flow satisfying conservation. Because
the tree routing vanishes on non-tree edges, each circulation coefficient
is exactly the corresponding physical non-tree-edge flow, up to an
immaterial chosen orientation.

Acyclic physical-flow orientation bounds every edge by total positive
injection, so the rational original-input bound `B` is valid for all
circulations and all physical blocks. Effective active-block injections
are formed by grouping original loads; they do not require a larger
physical-flow bound. A compact rational box therefore contains every
physical solution.

Each flow is affine in a constant number of variables. Its zero set
defines a hyperplane; repeated hyperplanes and lower-dimensional
arrangement faces are harmless. On each sign cell the edge law and
objective are degree-two polynomials. The fundamental-cycle equations
are sufficient for potential consistency: a drop vector annihilating
the entire cycle space is a potential gradient. Together with exact
conservation and the sign-specific physical laws this is precisely the
passive physical solution. Strict convexity of the flow energy gives
uniqueness for every nomination, preventing spurious physical solutions.
Zero flows agree across sign pieces, including on cell boundaries.

In fixed dimension an arrangement of polynomially many rational
hyperplanes has polynomially many faces and can be enumerated with
polynomial bit work. The resulting semialgebraic systems have fixed
dimension and degree and polynomial-size rational data. The decision
and algebraic sample-point subroutines cited and checked in the cactus
audit apply unchanged. Rational coefficient sums, denominator clearing,
and objective bisection have polynomial bit growth. The polynomial
exponent may depend on the fixed rank bound.

For a fixed-load non-bridge block, only its at-most-`r` circulation
variables remain. The same system has a unique physical solution.
Fixed-dimensional bounded-degree real algebraic sampling gives a
representation of that solution with algebraic degree bounded in terms
of the fixed rank and polynomial coefficient bit length. One may also
obtain its drop interval directly by objective feasibility queries.
Either method avoids constructing or comparing an exact sum of the
drops over an unbounded number of blocks.

## Higher-dimensional rational nomination recovery

The retained active face has only `O(r)` free loads. An algebraic
near-optimal sample can be refined to rational enclosing intervals for
each of these coordinates, each of any prescribed small width. Intersect
those intervals with the original rational face bounds and exact rational
balance equation. This rational polytope is nonempty because it contains
the sampled algebraic nomination. Rational linear programming returns
an exactly feasible rational point with polynomial encoding length.

If there are `f` free coordinates and every enclosing interval has width
at most `eta`, the rational point differs from the sample in l1 distance
at most `f eta`. Taking, for example,
`eta<=epsilon/(4 C f)` for positive Lipschitz constant `C` limits the
rounding loss to `epsilon/4`. Fixed coordinates remain fixed, and the
balance equation is imposed exactly. This argument covers samples on
several simultaneous active bounds, degenerate faces, and irrational
samples whose feasible rational neighborhood is one-sided. It does not
rely on independent coordinate rounding, which could violate balance.
Zero free coordinates need no rounding. Zero Lipschitz constant needs
no precision-driven division.

Changing the local shifted loads changes the original core loads by the
same differences, so the connected-graph Lipschitz estimate applies with
a rational global bound. Disaggregating each rational group total inside
its original rational intervals preserves balance and the core objective.
No claim that the physical flows or potentials are rational is needed.

Finally, compute each fixed-block constant interval finely enough that
their summed width is below the chosen per-face error budget. Add the
active optimum interval. Taking maxima of lower and upper endpoints over
all global block choices and local faces contains MPD and preserves the
largest individual interval width. Selecting a greatest-lower-endpoint
face, sampling near its local optimum, and reserving a rounding budget
proves the rational epsilon-optimal output just as in the cactus audit.
The polynomial number of faces introduces no extra additive error.
