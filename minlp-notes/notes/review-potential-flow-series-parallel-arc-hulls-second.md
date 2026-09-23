# Second independent audit of series-parallel arc-flow uncertainty hulls

Date: 2026-09-05. Reviewer: `noncommutative_rank_review`, independent of
the author and first reviewer.

Reviewed: [the series-parallel arc-hull investigation](potential-flow-series-parallel-arc-hulls.md),
including the final primary-source paragraph and exact discrete recovery
by successive endpoint restrictions.

**Verdict: PASS.** Separate monotonicity, interval-hull equality, the joint
nomination extension, exact fixed-rank computation, and discrete optimizer
recovery follow under the stated assumptions. Combined with the reviewed
rank-three hardness theorem, this proves the proposed rank-two versus
rank-three complexity boundary. The graph and electrical sign mechanisms
are established prior theory; this mathematical review does not clear the
nonlinear tolerance theorem's novelty.

## Physical existence and continuity

For a continuous strictly increasing law `g` with `g(0)=0`, its primitive
`G(x)=integral_0^x g(s) ds` is nonnegative and strictly convex. With
`c=min(g(1),-g(-1))>0`, the inequality
`G(x)>=c*(|x|-1)` holds for `|x|>=1`. The sum of edge energies is therefore
coercive in the full flow vector, even if the constitutive laws are bounded.
Balanced nominations have a nonempty conservation space on a connected
graph. The energy attains a unique minimizer there, and stationarity supplies
potentials satisfying every edge law.

The sign of an edge's drop agrees with the sign of its flow. Hence the
orientation induced by positive physical flows is acyclic. Flow decomposition
bounds every magnitude by the total nomination magnitude. On a compact
nomination set this bound is uniform, independently of coefficients.
Normalize one potential. A spanning-tree path sum then bounds all potentials
using the laws on this compact flow interval. For convergent nominations
and coefficients, subsequential state limits satisfy the limiting equations;
uniqueness identifies the limit. This proves the required continuity and
attainment of extrema on compact uncertainty sets.

## Primary graph and electrical sources

I directly inspected [Eppstein's author manuscript](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf),
Lemma 9, printed page 9 (PDF index 8), including its decomposition-rerooting
proof. It states that the endpoints of any existing edge of a biconnected
series-parallel graph can be used as its two terminals. The result is applied
only to the target edge's block. Eppstein's broader graph conventions must
not be substituted for an arbitrary connected block assembly.

[Cosme Llópez and Pous (2017)](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2017.76)
explicitly state the equivalence between excluding a `K4` minor and having
series-parallel biconnected components. This connects the candidate's graph
convention to the rooted lemma.

The elementary electrical induction is valid. Under a positive terminal
drop, a series composition carries the same positive current through its
components; a parallel composition sends positive current through each
component. Recursing fixes the orientation of each edge independently of
all positive resistances. For a unit terminal injection, the same currents
are multiplied by a positive normalization factor. Components off the target
block attach through one articulation and have no adjoint sources, so their
potentials are constant and their adjoint currents vanish. Bridges are
handled directly.

I also directly inspected [Duffin (1965)](https://sites.math.washington.edu/~reu/papers/current/jim/duffin.pdf),
Theorems 0 and 1, printed pages 306–307. His obstruction called the Wheatstone
bridge is explicitly the complete four-graph. Adding a positive-resistance
battery branch parallel to the existing target edge creates no new simple
`K4` minor. The augmented graph is therefore confluent. Battery-driven
currents in the original network are a positive multiple of the unit
endpoint adjoint, which proves the same sign statement. No claim about
arbitrary, nonadjacent terminal pairs follows from this argument.

## Parameter derivatives, including the target edge

For smooth laws with positive derivatives, the linearized resistances are
`R_e=g'_e(x_e)>0`. Grounding a potential makes the corresponding Laplacian
invertible. The standard electrical adjoint calculation gives

```
partial(pi_u-pi_v)/partial theta=j_e*f_e(x_e)
```

when the affine parameter changes only edge `e`. If `e` differs from the
target `a`, differentiating the target law therefore gives exactly
`partial x_a/partial theta=j_e*f_e(x_e)/g'_a(x_a)`.

If the parameter acts on the target itself, its direct constitutive
derivative must also be included. The correct formula is

```
partial x_a/partial theta=(j_a-1)*f_a(x_a)/g'_a(x_a).
```

The candidate includes this essential subtraction. The unit adjoint has
source `u` and sink `v`, so the maximum principle and conservation at the
source give `0<=j_a<=1` for the edge oriented `u->v`. Its factor `j_a-1`
has a fixed weak sign. If the target is a bridge, `j_a=1`, consistent with
its flow being fixed by nominations. On every other edge, the rooted graph
lemma fixes the sign of `j_e`.

For one parameter coordinate, with every other input fixed, suppose
`f_e(x_e(theta_0))=0` at some parameter value. The entire state at that value
satisfies the laws at every other value of this coordinate: its only changed
constitutive term is zero. Physical uniqueness makes the state constant
throughout the interval. Otherwise the continuous scalar function
`f_e(x_e(theta))` never vanishes and has one sign on the connected interval.
Thus each displayed derivative has a fixed weak sign throughout the
coordinate interval. The direction may depend on the fixed nominations
and on other parameters; no uniform choice of an optimal corner is asserted.

## Smoothing continuous laws

One explicit centered smoothing operator is

```
S_rho f(x)=integral eta(z)*[f(x-rho*z)-f(-rho*z)] dz,
```

where `eta` is a nonnegative smooth compactly supported unit-mass kernel.
Apply it linearly to the base law and every affine basis, and add `rho*x`
to the complete law. Linearity preserves affine parameter dependence.
Centering gives zero at zero. Convolution preserves strict increase, and
the added term makes every derivative positive. Individual basis functions
need not be increasing; admissibility is required of every complete law.

The smoothed complete laws converge uniformly on the common compact flow
interval. Their physical flows have the same acyclic bound, and the
continuity/uniqueness argument gives convergence to the original physical
states. For any fixed coordinate problem, every smoothed response is weakly
increasing or weakly decreasing. An infinite subsequence has the same
direction. Taking pointwise limits along that subsequence preserves the
corresponding inequalities for every pair of coordinate values. This proves
monotonicity without imposing differentiability, nonzero physical flows,
or a lower bound on the unsmoothed derivative.

## Hull replacement and joint nominations

For fixed nominations, start at a global optimizer on the product of
parameter intervals. Monotonicity permits moving the first coordinate to
an endpoint without worsening the objective. Since the starting value is
already globally optimal, that endpoint still attains the optimum. Repeat
for every coordinate, using the possibly changed monotonicity direction
appropriate to the current fixed data. Both endpoints belong to each
original compact scalar set, so the resulting point is feasible for the
original product set. Inclusion in the hull supplies the reverse bound.
The minimum follows by the same argument with reversed objective sign.

For a joint optimizer over nominations and parameters, hold its attained
nomination fixed throughout these endpoint moves. That proves joint equality
for any compact nomination set independent of the parameter product.
It neither requires the optimized response to be separately monotone after
eliminating nominations nor assumes a common corner works for all
nominations. Correlated scalar parameter sets or extra operating constraints
would invalidate this endpoint argument and remain outside the theorem.

## Exact computation and discrete recovery

For explicitly listed finite positive rational quadratic resistances, the
interval endpoints are rational and computable from the input. At fixed
maximum block cycle rank, the reviewed continuous-box arc theorem returns
exact extremum values and performs equality-sensitive rational-capacity
comparisons in polynomial bit time. Hull equality transfers those values
and decisions to the finite sets. An unbounded number of graph blocks
causes no sum-of-independent-radicals comparison: the objective edge lies
in one block, and the exact arc algorithm reduces to that block.

The added self-reduction also passes. Let `V` be the current exact maximum
with some coordinates already fixed to endpoints. Let `V_L,V_U` be the
maxima after fixing the next coordinate to its lower or upper endpoint.
The same endpoint proof gives `V=max(V_L,V_U)`, while neither restricted
value can exceed `V`. Therefore equality `V_L=V` justifies selecting the
lower endpoint; otherwise the upper endpoint must preserve `V`.

Each new optimization instance has only rational coefficients and rational
endpoint restrictions. There are at most linearly many extra calls in the
number of uncertain coefficients. Their algebraic extremum values have
polynomial degree and encoding length, and each pairwise equality/order
comparison is polynomial. They are not successively adjoined to a growing
number field and no multi-block physical pressure is evaluated.

At the end, the selected endpoint vector belongs to the original finite
resistance sets and admits the global optimal nomination value. One final
fixed-resistance call supplies an algebraic local nomination optimizer.
Disaggregating outside nomination sums can use interval allocation with
arithmetic and comparisons over that one local optimizer field. It does not
introduce independent algebraic physical states from other blocks. Thus a
global algebraic nomination vector of polynomial encoding length can also
be returned. No rational exact physical-state witness is implied.

## Rank boundary and limitations

A `K4` minor is contained in a biconnected block; a cut vertex cannot join
separate pieces of a biconnected minor. Cycle rank cannot increase under
deletion or contraction, while `K4` has rank three. Hence every graph with
maximum block cycle rank at most two is `K4`-minor-free. The positive
algorithm therefore applies to all such graphs.

The reviewed discrete arc-capacity reduction uses a `K4` subdivision with
rank three and proves coNP-completeness even for fixed nominations and
two options per uncertain edge. Together these statements give the proposed
boundary by maximum block rank. They do not claim that every rank-three
graph is hard; some are still series-parallel and covered by the positive
algorithm. Nor do they give polynomial bit complexity on series-parallel
graphs with unbounded block rank.

The positive structural proof applies established confluence theory.
Potential overlap with the unread Hasler–Wang nonlinear tolerance paper
remains a material novelty qualification. The verified computational
boundary should be distinguished from any claim that the electrical sign
mechanism or endpoint consequence was previously unknown.
