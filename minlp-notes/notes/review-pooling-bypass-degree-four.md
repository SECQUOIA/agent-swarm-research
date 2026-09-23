# Independent review: degree-four bypass hardness

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the bounded-degree refinement is correct.** This reviews
[the candidate](pooling-bypass-degree-four-hardness.md), building on the
[reviewed copy reduction](review-pooling-one-pool-bypass-copy.md). It preserves
NP-completeness with one pool and one physical quality allowing lower and upper
bounds, or two upper-only quality coordinates. Input total out-degree is at
most four, output total in-degree at most three, and pool out-degree two. The
pool in-degree remains unrestricted. Exact flow contracts remain essential.

The new source has four distinct physical ports with flows
`v,v,2-u,2-w`, exact supply 4, and no other outgoing arc. Its conservation
equation is precisely `2v=u+w`. The two occurrences of `v` are assigned to
different copy gadgets and different outputs, so they do not require parallel
arcs. A complemented leaf correctly reverses the requested signal-port sign.
All ports have quality two, preserving source-quality consistency.

The zero signal is forced to zero by a single positive port with zero supply
capacity. Its other copies and complement ports remain feasible, and its
source identities do not acquire high degree when copies are added.

For a row with `m` literal occurrences, pad to a power of two `N` with the
zero signal. The arithmetic-mean tree forces the root to equal the literal
sum divided by `N`. A root capacity `B/N` therefore enforces the original
row exactly. Every auxiliary value lies in `[0,2]` because it averages values
in this interval. Conversely every feasible tree satisfies the intended
root identity, so the projection onto original signals is unchanged. The
`m=0` row is tautological and the `m=1` root can be a literal, including a
complement, without an averaging gadget.

There are `N-1` averaging equations and `4(N-1)+1` requested ports for a
nontrivial row. Separate copy gadgets per occurrence therefore use `O(m)`
nodes and arcs. Since `N<2m` and the reviewed source family has polynomial
total coefficient sum, construction size remains polynomial. The new root
capacity is rational with polynomial encoding length and lies in `[0,2]`.

All new sources have at most four arcs. Chain and midpoint sources have
two, while unused-port and root sources have one. Conversion sources retain
their two arcs including the pool intake. Gadget outputs retain exactly
three incoming arcs; the primary outputs have two and one. Thus deleting
the sole pool leaves a bypass graph of maximum degree at most four. The
construction does not bound its vertex integrity, component size, treewidth,
or the pool in-degree.

The original pool intakes, feasible source mixtures, and rewards are unchanged.
The production-cost offset also remains valid because all newly added source
and output flows enter total mass conservation. The reviewed fixed-parameter
linear-fiber NP upper bound supplies membership. The large source coefficients
still preclude a strong-hardness conclusion from this proof.

I inspected the assembled original-network checker and independently ran
`check_degree_four.py --seed 23 --trials 8` with the project Python. All 22
global solves passed: 16 randomized/shifted cases and six boundary cases for
empty rows, single-literal roots of both signs, padding, empty source polytope,
and zero reward. The checker verifies actual input/output degrees and absence
of duplicate arcs. It imposes only physical network constraints, without
directly adding the intended averaging or source-cone equations. Relaxing a
binding averaging source's exact supply changes the negative-control optimum
from 10 to 20, detecting the role of that contract.

The [independent log](../code/pooling_bypass_copy/degree_four_independent_review_output.txt)
is retained. These computations supplement the proof; they do not establish
priority. Novelty of the bounded-degree restriction needs a separate search.
