# Candidate refinement: bounded bypass degree does not restore tractability

Date: 2026-09-05. Status: two independent mathematical reviews PASS; retained milestone.

The [reviewed one-pool bypass reduction](../results/pooling-one-pool-bypass-np-completeness.md)
can apparently be modified so that every input has total out-degree at
most four and every output has total in-degree at most three. The sole
pool still has two outgoing arcs; its in-degree is unrestricted. Thus the
bypass graph has maximum degree four. Exact supply and demand contracts
remain essential. There is one physical quality with lower and upper
bounds, or two upper-bound quality coordinates.

The modification uses the already reviewed copy gadget and a bounded
averaging tree. It does not use the separate binary-coefficient
universality extension.

## Reviewed primitive and port convention

For distinct quality labels `alpha,beta`, two gadget outputs have exact
demand four and exact midpoint quality `(alpha+beta)/2`. A private
midpoint-quality input supplies exactly four units to these two outputs.
Each output also has one `alpha` and one `beta` input port, with capacity
two on each port. The four port flows are exactly

```
A-alpha = x,       A-beta = x,
B-alpha = 2-x,     B-beta = 2-x,        0<=x<=2.
```

A source of quality `alpha`, exact supply two, and exactly two outgoing
arcs joins `B-alpha` of one gadget to `A-alpha` of the next. This forces
their signal values to agree. Chains using `(alpha,beta)=(0,2)` therefore
provide as many distinct quality-two ports carrying `x` or `2-x` as
required. Unused ports have private sources with upper supply two and
no lower bound.

For clarity, allocate a separate chain gadget for every requested port
occurrence, using only its requested `A-beta` or `B-beta` port and
privately supplying the other. This creates polynomially many gadgets
and guarantees that repeated occurrences are distinct physical arcs to
distinct output nodes. Two equal-quality source nodes are never merged
unless their common supply equation is explicitly part of the construction.

Original signal chains still end with the reviewed `(0,a_i)` conversion
gadget: its `B-beta` port and the pool intake share one source with exact
supply two. The actual pool intake is `x_i`. New auxiliary signal chains
need no conversion gadget and have private sources at their unused chain
endpoints.

## Degree-four implementation of an averaging equation

For signals `u,w,v in [0,2]`, the equation `2v=u+w` is equivalent to

```
v + v + (2-u) + (2-w) = 4.                              (A)
```

Use a new quality-two input with exact supply four, whose only outgoing
arcs are two distinct ports carrying `v`, one carrying `2-u`, and one
carrying `2-w`. It has out-degree four. Its ordinary supply equation is
exactly (A); no additional quality coordinate or nonlinear constraint is
introduced. Conversely any values satisfying `2v=u+w` fill these four
arcs within their capacities of two.

A child can be a complemented original signal. If `u=2-x_i`, the needed
port `2-u` is simply a positive `x_i` port. If `u=x_i`, it is a
complementary `2-x_i` port. All such ports have quality two regardless of
the actual pool input quality used by the conversion gadget.

Create one additional signal `zeta` and force it to zero by assigning one
positive `zeta` port to an input with upper supply zero. Its other copies
are available for zero padding. Complementary `2-zeta` ports then carry
two units. The copy gadgets at `zeta=0` remain feasible: their `A`
endpoint flows are zero, their `B` endpoint flows are two, and their
middle flows are four and zero. This adds only a degree-one capacity
input; it does not require a positive-flow assumption.

## Replacing a row input by a balanced tree

In the reviewed reduction, a homogeneous row `sum_i c_i x_i<=0`
uses a quality-two input whose `m=sum_i |c_i|` outgoing ports carry
the list

```
f_1,...,f_m in [0,2],
```

containing `c_i` copies of `x_i` when `c_i>0` and `-c_i` copies of
`2-x_i` when `c_i<0`. Its upper supply is

```
B=2 sum_{c_i<0}(-c_i).
```

The sum of these port flows is `sum_i c_i x_i+B`, so their capacity
condition `sum_j f_j<=B` is the required row.

If `m=0`, the row is the identity `0<=0` and needs no node. Otherwise
put `N=2^ceil(log2 m)`, pad the leaf list by `N-m` copies of `zeta`,
and arrange the `N` leaves in a complete binary tree. Associate a new
auxiliary signal with every internal node and enforce that it is the
average of its two children, using (A). Induction from the leaves gives

```
v_root = (sum_{j=1}^m f_j)/N,
0<=v<=2 at every internal node.
```

Finally assign one positive root port to a fresh input whose only
outgoing arc is that port and whose upper supply is `B/N`. This
degree-one source enforces `sum f_j<=B` exactly. The capacity is a
nonnegative rational number with polynomial encoding length. In fact
`0<=B/N<=2` because `B<=2m<=2N`. If `m=1`, there are no internal
nodes: use the single leaf itself as the root, assigning its positive
or complementary port directly to the capacity input as appropriate.

Remove the original high-degree row input. Every leaf occurrence now
appears through the appropriate child-complement port in an averaging
equation, or directly in the root inequality when `m=1`. It has no
additional outgoing supply constraint inherited from the removed input.

**Equivalence.** Given any original feasible signal assignment, compute
each tree node as the arithmetic mean of its children. These values lie
in `[0,2]`, satisfy every exact four-unit supply equation, and obey the
root capacity. Fill all copy gadgets at their assigned values. Conversely,
any feasible modified physical network defines its chain signals; each
averaging input forces (A), and induction recovers the displayed root
identity. Its final capacity therefore implies the original row. The
projection onto original signals and pool intakes is unchanged.

## Encoding size, degrees, and costs

For a row with `m>=1`, `m<=N<2m`. It has `N-1` averaging equations,
at most `N-1` new signals, and `4(N-1)+1` requested equation/root ports,
plus padding occurrences already counted as children. The construction
has size `O(m)` per row. The source-specific Matsui system used by the
reviewed theorem has polynomial total coefficient sum after homogenizing;
therefore total network size stays polynomial. The only new denominators
are powers of two of size at most twice a row's original port count.
Every flow upper bound is now at most four. Root bounds are dyadic
rationals in `[0,2]`; the other bounds come from the existing zero-,
one-, two-, and four-unit gadgets. This does not imply strong hardness,
because the source quality and cost coefficients still have large
numerical magnitudes or, after normalization, large denominators.

Every input is one of the following:

| Input type | Maximum total out-degree |
|---|---:|
| Averaging equation | 4 |
| Private midpoint of a copy gadget | 2 |
| Chain link | 2 |
| Original conversion source, including its pool intake | 2 |
| Private unused port | 1 |
| Root bound or zero-signal bound | 1 |
| Anchor into the first primary output | 1 |

Every gadget output retains exactly three incoming arcs. The first
primary output has two incoming arcs, from the pool and anchor; the
second has just the pool arc. Thus all outputs have in-degree at most
three. All arcs are either input-pool, pool-output, or input-output arcs;
there are no pool-to-pool arcs. The sole pool retains out-degree two
and unrestricted in-degree. Deleting it leaves the bypass graph with
maximum degree at most four.

All new arcs have zero cost in the arc-cost version. The original signal
intakes and their rewards are unchanged, so the exact profit identity and
NP-hardness reduction remain valid. The reviewed production-cost version
also works: only private conversion inputs are rewarded according to
their original signal flows, and auxiliary sources have zero cost before
the uniform production-cost/output-revenue offset.

Quality conversion to two upper-bound coordinates and normalization into
`[0,1]` work exactly as in the reviewed theorem. Fixed-parameter LP
membership places this precise rational finite-flow model in NP.

## Candidate conclusion and verification required

The proposed conclusion is NP-completeness with one pool, two upper-bound
quality coordinates, arbitrary direct arcs of maximum bypass degree four,
input total out-degree at most four, output total in-degree at most three,
and pool out-degree two. Fixed supplies and demands are permitted and
used. No strong NP-completeness, zero lower-flow-bound, or bounded pool
in-degree claim is made.

This would show that bounded bypass degree alone does not replace the
stronger bypass decomposition assumptions in the constructive results.
The arithmetic equations and projection argument are explicit above,
and a first independent reviewer has approved the mathematical argument.
The [assembled-network checker](../code/pooling_bypass_copy/check_degree_four.py)
passed 26 original-model global solves: ten generated source cones,
each with original and shifted quality data, and six boundary cases.
It checks the actual input and output degrees, excludes parallel arcs,
and verifies every upper flow bound is at most four. Its model contains
ordinary node/arc bounds and blending/quality constraints, with no hidden
copy equations or source-cone constraints. Weakening an averaging source's
exact supply to an upper bound changes a deliberately selected optimum
from 10 to 20. The
[log](../code/pooling_bypass_copy/degree_four_output.txt) is retained.
Independent reviews: [first](review-pooling-bypass-degree-four.md),
[second](review-pooling-bypass-degree-four-second.md), both PASS. A later
[degree-three refinement](pooling-bypass-degree-three-hardness.md) is being
checked before selecting the final result to promote. Novelty of this degree refinement has not been
established by a separate search.
