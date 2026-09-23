# Independent audit: strong hardness with five contract exceptions

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: PASS.** I independently checked the complete refinement in
[the candidate](pooling-fixed-exception-hardness-refinement.md) against
the previously reviewed constant-data source reduction. I also inspected
the separate compiler and its original physical solver formulation.
The refined construction preserves feasibility, has the claimed five
exceptional nodes and fixed numerical data, and gives strong NP-
completeness in the stated model. Publication priority of the combined
restriction remains unestablished.

## Starting equivalence and exact comparisons

The reviewed starting circuit encodes the homogeneous source constraints,
the dyadic intake-quality expression, and the positive threshold within
its physical network. The threshold excludes zero total intake. Its
two-source pool interface and two unit-capacity primary outputs have
the same feasible radial throughput bound as before. None of the new
transformations changes that interface or adds an external threshold
constraint.

A comparison source on ports `u` and `2-v` with total supply at most two
imposes `u<=v`. Replacing it by exact supply two on `u`, `s`, and `2-v`
imposes `u+s=v`. Since both compared signals lie in `[0,2]`, its unique
slack belongs to `[0,2]` precisely for the original feasible comparisons.
A fresh copied signal supplies this slack using the same bounded
physical modules. The replacement is exact in both directions and
adds only a constant number of occurrences per comparison. Equality
comparisons retain the two-port exact source.

## Complement grouping is exact and noncircular

For a gate source requesting flows `f_h` on ports of capacities `c_h`,
the corresponding unused positive-quality ports have flows `c_h-f_h`.
This is true for full ports, whose paired total is two, and half ports,
whose paired total is one. Once the requested source has exact supply
`S`, the unused flows sum to the fixed quantity `sum_h c_h-S`.
Replacing their separate variable inputs by one same-quality exact
source of that quantity therefore loses no feasible port assignment.
Conversely, splitting that grouped source into separate fillers recovers
a feasible starting network for any refined feasible assignment.

The module identities do not require any chosen throughput on those
positive-quality fillers. They follow from the module's exact middle
supply, exact output demands, and its endpoint-quality relations;
closed zero-quality links identify repeated signal occurrences. In the
upper-quality-only starting construction the same relations are forced
by the reviewed closed-cycle equality argument. In the refined network
they can also be read directly from the imposed exact output qualities.
Grouping therefore does not assume the very gate equation it needs
to establish.

I checked every gate type in the table. Average and full/half coupling
use capacities `(2,1,1)`, supply two, and complement supply two.
Addition and slack comparison use `(2,2,2)`, supply two, and complement
supply four. Equality uses `(2,2)`, with both supplies two. Zero and
unit gates use one capacity-two port, with complementary supplies two
and one respectively. There is no negative, nonconstant, or oversized
exact supply hidden in this step.

## Three-port splitting

For any exact source with three requested ports, replace port `h` by
a same-quality source of exact supply `c_h`, feeding the old port and
a collector. Conservation makes the collector flow `c_h-f_h`, which
is nonnegative and at most its capacity. An exact collector demand
`sum_h c_h-S` is equivalent to the original total equation
`sum_h f_h=S`. Its exact quality is automatic because all its sources
have the same quality.

This argument covers both supply-two gates and their supply-four
complement sources. With capacities `(2,2,2)`, the collector demand
is respectively four or two. With `(2,1,1)` it is two. New source
supplies and arc capacities are one or two. Every new input has two
outgoing arcs and each collector has three inlets. Distinct occurrence
ports prevent parallel arcs, including when a signal is repeated in
one gate. Original copy outputs keep their prior inlet counts.

## Exact ordinary contracts and the five exceptions

All full and half module outputs, including the endpoint-one and
endpoint-33 converters, can have their quality specifications imposed
exactly: the original feasible extensions satisfy them and the refined
equations preserve the copy identities. Collectors have exact demand
and a single incoming source quality. Consequently every nonprimary
output has both exact demand and exact quality.

All gate, complement, split, middle, and zero-quality link inputs have
exact total supplies. Each converter's fixed-supply positive endpoint
source still feeds a bypass complement and the pool; its total remains
exactly two even though its pool intake varies. The only variable
inputs left are the converter's other positive-endpoint filler in each
of the two converters and the zero-quality anchor. Those are three
declared supply-interval inputs. Both primary outputs retain variable
demands and upper quality bounds, giving the other two exceptions.

This accounting includes the pool arcs in input degree. The converter
feed sources have one bypass and one pool arc. All inputs thus have
total out-degree at most two, and all outputs have total in-degree
at most three. The pool has exactly two feed and two outlet arcs.
Its two unit outlet capacities imply a total throughput bound of two,
so the stated common upper bound is redundant.

The unscaled quality alphabet is precisely the displayed seven-element
set. Scaling every quality by `1/33` preserves all homogeneous quality
equalities and inequalities and produces the claimed normalized
alphabet. Flow bounds and exact supplies/demands remain in
`{0,1,2,3,4}`. Zero supplies, unit gates, and zero intake in a particular
converter do not create additional exceptional nodes; exception status
here is determined by the declared contracts.

## Complexity, membership, and evidence

The starting binary arithmetic circuit has polynomial size in the
source instance. Each refinement is linear in its gate/port count;
in particular numerical magnitudes are not expanded into that many
copies. The resulting network has polynomial size and all numerical
data are from fixed finite sets. Encoding those data in unary therefore
still gives a polynomial reduction, proving strong NP-hardness.
The nonlinear positive-product threshold remains encoded by circuit
topology, not by an additional large flow bound or objective coefficient.

NP membership follows from the reviewed fixed-parameter linear-fiber
lemma with one scalar pool quality. At a fixed quality every physical
constraint is linear in the bounded arc flows. The active-basis
certificate and univariate algebraic verification do not require a
rational physical witness. This supplies NP membership for the precise
feasibility decision model used here.

I inspected
[the separate compiler](../code/pooling_bypass_copy/check_fixed_exception_hardness.py).
Its comparison replacement, gate-indexed unused-port grouping, and
source splitting implement the transformations above. The final solver
uses only original arc and node bounds, output quality rows, and actual
pool mass and quality balances. It receives no signal equations, source
polytope rows, or threshold comparison directly. The construction checks
the exception counts, degree bounds, distinct arcs, and numerical
palettes. The reported sixteen global numerical feasibility solves are
supporting checks, not exact symbolic certificates; I did not duplicate
them.

Together with the separately reviewed degree-two-bypass algorithm for
fixed contract exceptions, this gives the stated feasibility boundary
between maximum output degree two and three, while keeping input total
degree at most two, one scalar quality, two pool feeds/outlets, and
redundant common pool capacity. Positive exact contracts remain
essential. There is no claim of hardness for the all-lower-bounds-zero
feasibility model or of polynomial dense-cost optimization on degree two.
