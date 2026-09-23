# Independent review: degree-three bypass construction

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the fresh degree-three refinement passes.** This reviews
[the candidate](pooling-bypass-degree-three-hardness.md), independently of
the reviewer who proposed the half-port idea. It strengthens the previously
[reviewed degree-four construction](review-pooling-bypass-degree-four.md).

The half gadget's mass and quality equations imply `u=2v` at each output.
Its exact middle supply and two exact demands then give total zero-port
flow 2. Thus its zero ports are `x,2-x` and its quality-three ports are
`x/2,1-x/2`, with nonnegative middle flows for every `x in [0,2]`. Full
gadgets have the same zero-port formulas. Consequently exact two-unit
zero-quality chain links can join any sequence of full, half, and final
conversion gadgets while preserving one common signal.

The averaging source's three distinct arcs carry
`v,1-u/2,1-w/2`; exact supply 2 is equivalent to `2v=u+w`.
Complemented children correctly request positive half ports. Allocating a
separate gadget to each occurrence avoids parallel arcs even when both
children are the same signal. Global zero padding, full root ports, and
the empty-row and single-literal cases preserve the previous row-tree
equivalence. Auxiliary signals can be nonzero at zero original intake,
which the construction and draft correctly allow.

The number of gadgets and links is linear in the source row's literal
count. The source-specific polynomial coefficient-sum argument therefore
still gives polynomial size. Every averaging source has three arcs; every
other input has at most two except private one-arc sources. Each gadget
output has three incoming arcs. Conversion input degree includes its pool
arc. The primary outputs and sole pool retain their stated degrees. Flow
upper bounds are at most 4, including the half gadgets' demand and middle
supply 3 and half-port capacity 1.

The exact source-cone projection, intake reward, production-cost variant,
and NP upper bound carry over without modification. This statement still
uses exact flow contracts and lower/upper quality specifications, or a
negative duplicate as a second upper-only coordinate. Removing either
type of lower bound requires the separate audited extensions.

I independently ran the assembled original-network checker with seed 41
and eight trials. All 22 global solves passed: 16 randomized/shifted
cases and six boundary cases. The checker verifies input/output degree
at most three, finite flow bounds at most four, and unique physical arcs.
A negative control relaxing an averaging supply changes the optimum from
10 to 20. The
[independent log](../code/pooling_bypass_copy/degree_three_independent_review_output.txt)
is retained. These tests corroborate the exact projection proof; they do
not establish literature priority or strong NP-hardness.
