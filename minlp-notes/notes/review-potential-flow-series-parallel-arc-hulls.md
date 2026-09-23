# Independent audit: series-parallel arc-flow uncertainty hulls

Date: 2026-09-05. Reviewer: `constant_rank_review`.
Reviewed candidate: `notes/potential-flow-series-parallel-arc-hulls.md`.

## Verdict

**PASS.** The edge-flow separate-monotonicity theorem, compact-set hull
equality, joint nomination extension, and exact polynomial validation
consequence at fixed block cycle rank are correct. In particular, the
positive result covers every graph with maximum block cycle rank at most
two. Combined with the separately reviewed rank-three hardness theorem,
this gives the stated complexity boundary.

The precise adjacent-terminal graph lemma is available in an openly
accessible primary source. Applying it to the target edge's block
resolves the main source and terminology issue in the initial draft.
No substantive correction to either parameter derivative was needed.

This audit does not establish novelty. The electrical current-direction
mechanism is classical; possible overlap with nonlinear tolerance
literature remains a separate source-review question.

## Graph conventions and the adjacent-terminal lemma

The graph class in this candidate means `K4`-minor-free graphs, allowing
an arbitrary tree of biconnected blocks. It should not be confused with
the narrower convention that the whole graph already has two specified
terminals and a series-parallel decomposition.

The equivalence between `K4`-minor exclusion and series-parallel
biconnected components is stated explicitly in the primary abstract of
Cosme Llópez and Pous, *K4-free Graphs as a Free Algebra*.
[MFCS 2017 publication](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2017.76).

The needed terminal selection is Eppstein's Lemma 9, printed page 9
(PDF page 9): a biconnected series-parallel graph can use the endpoints
of any existing edge as its two terminals. I read both the statement
and its proof, which reroots the series-parallel composition around the
selected edge. The lemma applies directly to the target block.
[Eppstein, *Parallel Recognition of Series-Parallel Graphs*](https://www.ics.uci.edu/~eppstein/pubs/Epp-IC-92.pdf).

In Eppstein's convention, a graph with a two-terminal decomposition has
a path of blocks; an arbitrary branching block tree need not have such
a decomposition. Restricting to the target edge's block is therefore
necessary when using that source. An attached component meets this
block at only one articulation and has no electrical source, so its
adjoint potential is constant and its adjoint currents vanish. A bridge
target is handled separately as a one-edge block.

For completeness, the current-sign conclusion follows directly by
induction on the block's two-terminal decomposition. Under positive
terminal voltage, a single positive resistor carries positive current.
A series composition has the same positive terminal current through
both pieces and positive voltage across each. A parallel composition
has the same positive voltage across its two pieces, each with positive
current. Induction therefore assigns a consistent source-to-sink
direction to every constituent edge, independently of positive resistance
values. Scaling to unit terminal current changes no signs. Fixed input
edge orientations merely attach fixed plus or minus signs to these
directions.

Adjacency is essential because it supplies this rooted decomposition.
The theorem is not claiming current-direction independence for all
pairs of nonadjacent vertices of a series-parallel block.

## Physical states and both derivative formulas

As in the previously audited cactus theorem, a continuous strictly
increasing law that vanishes at zero has a strictly convex coercive
primitive, including when the law has bounded range. Its energy on
the balanced affine flow space has a unique minimizer. Potentials are
unique after fixing a reference. There is no need to add a surjectivity
assumption on edge laws.

For smooth positive-derivative laws, use tail-positive incidence `A`
and `D=diag(g'_e(x_e))>0`. The derivative of a pressure difference
between the endpoints `u,v` of target edge `a`, when a parameter
changes only edge `e`, is

```
partial(pi_u-pi_v)/partial theta = j_e f_e(x_e),
```

where `j=D^(-1)A^T h` and
`A D^(-1)A^T h=e_u-e_v`. This follows by differentiating the
physical equations and testing with the adjoint. The effective
electrical resistances are precisely the positive derivatives in
`D`, so the graph lemma applies even when the original physical laws
are nonlinear or asymmetric.

If `e!=a`, differentiating the unchanged target law gives

```
partial x_a/partial theta = j_e f_e(x_e)/g'_a(x_a).
```

If `e=a`, the direct parameter term in the target law must be
subtracted, yielding

```
partial x_a/partial theta = (j_a-1)f_a(x_a)/g'_a(x_a).
```

Both formulas in the candidate have the correct signs and denominators.
The own-edge term cannot be replaced by the other-edge formula.

The unit adjoint is an acyclic flow from `u` to `v`, with every
actual edge current at most one in magnitude. The target edge's own
direction agrees with the positive terminal drop, so `0<j_a<=1`
for an ordinary nonloop target. A bridge has `j_a=1`; conservation
indeed fixes its physical flow independently of every parameter.
Thus `j_a-1` always has a fixed weak negative sign. If loops are
allowed, their physical flow is identically zero and they can be
discarded or treated separately.

## Affine parameters, sign preservation, and nonsmooth laws

For any one parameter, hold every other parameter and the nominations
fixed. If its basis value `f_e(x_e)` vanishes at any parameter value,
the entire state there satisfies the physical equations at all other
values: the only changing constitutive term is zero. Uniqueness makes
the entire state constant. Otherwise continuity makes that basis value
retain one sign throughout the interval. This handles multiple independent
parameters on the same edge as well, by fixing the other ones.

For another-edge parameter, the graph lemma fixes the sign of `j_e`;
for an own-edge parameter, the preceding bound fixes the sign of
`j_a-1`. The positive denominator cannot change either sign. Each
smooth physical edge-flow objective is therefore separately monotone.

Centered convolution of the complete laws, followed by a positive
linear term, preserves their zero at zero and affine one-edge parameter
dependence. Each complete admissible law remains increasing and becomes
smooth with positive derivative. The derivative sign theorem applies
uniformly over the same parameter box.

Physical flows are bounded by total positive nomination: their oriented
support strictly decreases in potential and has no directed cycle.
With compact nominations, this bound is uniform. Uniform convergence
of the smoothed laws on the resulting compact flow interval bounds
their potential drops; a spanning tree bounds normalized potentials.
Every convergent subsequence satisfies the limiting physical equations,
and uniqueness identifies its limit. The compactness contradiction
therefore gives uniform convergence of the physical objectives over
compact parameter and nomination sets.

On any fixed coordinate interval, choose a subsequence of surrogates
with one common weak monotonicity direction. Its limit inherits that
direction. This proves the continuous-law theorem without differentiating
at zero derivatives or kinks. The direction may differ on different
coordinate fibers.

## Hull equality and uncertainty scope

A compact parameter box has an objective optimizer by physical-state
continuity. Move its coordinates successively to suitable endpoints.
Separate monotonicity prevents worsening, and global optimality forces
each move to preserve the optimum. This does not require the direction
to remain unchanged after another coordinate is moved.

The product of arbitrary compact scalar sets is contained in its interval
hull and contains every hull vertex because the endpoints are attained.
The endpoint optimizer proves equality of maxima and minima over the
two products. For joint optimization over a compact nomination set,
hold an optimal nomination fixed throughout endpoint movement. It is
not necessary, and generally not valid, to assert that the value already
optimized over nominations is separately monotone.

There are no extra scenario feasibility restrictions. Capacity validation
compares all unrestricted physical scenarios against bounds afterwards;
it does not discard scenarios violating some other capacity first.
Coupled parameter sets or one parameter affecting several edges are
outside this proof.

## Exact algorithm and optional endpoint recovery

For explicitly listed positive rational resistance sets, reading the
minimum and maximum of each list is polynomial in the input size.
Their interval hulls are positive rational boxes, so the twice-reviewed
exact arc-extremum theorem applies on a series-parallel graph with
fixed maximum block cycle rank. Equality of hull and discrete extrema
transfers its exact algebraic values and polynomial bit complexity.
Comparing every signed extremum with rational arc capacities is exact,
including equality cases. No enumeration of endpoint combinations occurs.

The imported algorithm permits arbitrary shifted rational nomination
boxes with a nonempty balanced part. Its exact algebraic outputs can
be compared in polynomial time at fixed block rank. This audit uses
that already reviewed theorem; it does not replace it by a numerical
flow solver or by an additive approximation.

If an extremizing finite resistance scenario is desired, it can also be
recovered in polynomial time. Compute the exact optimum `V`. Fix one
resistance to its rational lower endpoint and recompute the optimum
over the remaining box and original nomination box. If the value is
`V`, retain that endpoint; otherwise retain the upper endpoint. At
least one endpoint retains `V`, by applying separate monotonicity at
an optimizer of the current restricted problem. Repeat for all coordinates.
This takes only a linear number of calls to the same fixed-rank exact
algorithm, with polynomial algebraic equality comparisons. Every selected
resistance is rational and belongs to its original finite set. Exact
optimizing nominations may still be algebraic; rational endpoint recovery
does not imply rational physical flows or exact rational nominations.

## The block-rank boundary

A `K4` minor must occur within a biconnected block. One justification
is to split at an articulation: at most one branch set of a `K4`
model can contain that articulation, and all other branch sets must
lie on the same side, since they are pairwise adjacent. Any parts on
other sides can be discarded from the model. Repeating localizes the
minor to one block.

The cycle rank of `K4` is three, and cycle rank cannot increase under
edge or vertex deletions and contractions. Hence a graph whose every
block has cycle rank at most two is `K4`-minor-free. The exact positive
algorithm consequently covers the entire rank-at-most-two class.

The separately audited hardness construction has one biconnected block
of rank three and a polynomially encoded strict capacity gap; its
coNP-membership argument is likewise already supplied. Combining it
with this positive theorem yields the claimed rank boundary for finite
resistance uncertainty. This does not say that every rank-three instance
is hard: series-parallel instances of any fixed rank retain the positive
guarantee. Nor does it give a polynomial-time algorithm for series-parallel
graphs with unbounded block cycle rank.

