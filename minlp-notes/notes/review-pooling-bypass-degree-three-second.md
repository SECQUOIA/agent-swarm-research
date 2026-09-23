# Review of the degree-three half-port construction

Date: 2026-09-05. Verdict: the reduction in
[the degree-three draft](pooling-bypass-degree-three-hardness.md) is correct,
conditional on the already reviewed source reduction and bounded-flow NP
membership lemma. I proposed the half-port refinement while independently
auditing the degree-four construction. The author independently checked its
algebra and wrote the draft. The implementation described below is separate
from the author's implementation; a further proof review should be read as
the fully independent review of this refinement.

## Half ports and chain composition

For the half gadget, an output has exact demand three and quality one.
Its endpoint qualities are zero and three, with middle quality one.
Writing its endpoint flows as `u,v`, subtraction of mass from quality gives
`u=2v`. Its middle flow is `3-3u/2`. The common middle source has exact
supply three across the two outputs, hence the two zero-quality endpoint
flows sum to two. Thus the four endpoint flows are exactly

```
x, 2-x, x/2, 1-x/2,      0<=x<=2.
```

Conversely these values fill both outputs, and their middle flows lie in
`[0,3]`. The endpoint capacities two and one are valid, including at both
signal endpoints. The zero-quality ports agree with the full midpoint
gadget and the original quality-conversion gadget. An exact two-unit
zero-quality source linking a previous complementary port to the next
positive port therefore forces equality of their signals, even when the
gadget types differ.

The averaging source has quality three, exact supply two, and flows
`v,1-u/2,1-w/2`. Its supply equation is exactly `2v=u+w`.
If a child is `2-x`, its required half-complement is `x/2`, which is
the positive half port. Each occurrence has a separate gadget and output;
repeated children neither merge ports nor create parallel arcs. Unused
ports have separate sources with the corresponding capacity.

## Full reduction and boundary cases

The padded binary tree remains an exact arithmetic implementation of the
average of the original full leaves. Its auxiliary values lie in `[0,2]`
by induction. The zero signal is forced by an ordinary full positive
port of upper supply zero. Padding by copies of that signal is valid;
its complementary half ports carry one and do not cause an infeasibility.
The root bound `B/N` is in `[0,2]`. A one-leaf row uses the appropriate
full port directly, and a zero row is omitted.

Both projection directions hold. A feasible original intake assignment
extends by computing the averages and filling each gadget. Conversely,
the exact supplies recover the copy equations and every averaging
equation, after which the root bounds imply the original rows. At zero
original intakes, auxiliary averages can be nonzero because complementary
leaves equal two. This causes no problem: the original homogeneous rows
are satisfied, and the calculated averages provide the required extension.

Every requested port costs one constant-size gadget and a bounded number
of chain links. Each row uses fewer than twice its original number of
coefficient occurrences as leaves. The polynomial total coefficient sum
of the particular Matsui source system is essential: this argument does
not claim a polynomial unary expansion for arbitrary binary matrices.

The averaging sources have three arcs; every other input has at most two
except private sources, which have one. Each gadget output has three
incoming arcs. The original pool still has two outgoing arcs and can have
unbounded incoming degree. Every upper flow bound is at most four. The
primary objective and its production-cost realization are preserved
because each actual intake is still its original signal and each rewarded
private conversion flow is still that signal. New ports and averaging
sources carry no additional base objective.

The theorem retains exact supply and demand contracts. It gives one
physical quality with lower and upper specifications, or two upper-bound
quality coordinates after negation and affine normalization. It does not
establish strong NP-completeness, hardness with bypass degree two, or a
priority claim relative to the literature.

## Separate full-network implementation

[independent_degree_three_review.py](../code/pooling_bypass_copy/independent_degree_three_review.py)
constructs inputs, outputs, physical arcs, exact supplies, exact demands,
and quality equations directly. Its LP contains no source-cone rows,
copy equalities, or averaging equations. It uses the earlier independent
LP backend, extended to distinguish demand-three half gadgets from
demand-four full gadgets. It does not import the author's constructor.

The checker passed:

- 120 projection LPs, compared with optimization over the explicit source
  cone and total intake bound;
- 114 complete pooling LPs at fixed compositions, including 56 excluded
  compositions;
- degree, capacity, and distinct-arc assertions on every constructed
  network.

Instances cover zero rows, one-leaf rows, repeated variables, padding,
empty simplex sections, and both original and shifted qualities. The
negative control relaxes only the lower bounds of the averaging supplies;
with every midpoint contract intact, the maximum of `x0-x1` in a cone
requiring equality changes from zero to two. This separately confirms
that the new three-port sources enforce the intended coupling.

These numerical tests support the explicit proof above. They are not
substitutes for the proof or for the source-complexity review.
