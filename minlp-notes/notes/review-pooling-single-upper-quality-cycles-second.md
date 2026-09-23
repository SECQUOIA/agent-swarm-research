# Second review: copy cycles with one upper quality

Date: 2026-09-05. Verdict: PASS for
[the cyclic construction](pooling-single-upper-quality-cycles.md).
Its combination with the exact-penalty proof also passes; see
[the separate penalty review](review-pooling-upper-flow-only-penalty-second.md).

In a full/conversion cycle of `r` gadgets, exact demands and middle
supplies give total endpoint flow `4r`, while cyclic zero-quality inputs
give total zero-quality endpoint flow `2r`. Each upper quality constraint
implies that the other endpoint flow is no larger than its zero-quality
partner. The sum of these nonnegative slacks is zero, so every inequality
is tight. Different positive endpoint qualities cause no problem: divide
each output row by that gadget's own positive midpoint quality before
summing. Once tightness is established, each gadget has its previous
full port formulas, and the cyclic links equate the signals.

For a separate half cycle, the corresponding endpoint totals are `3r`
and `2r`. Its upper rows say `2b<=alpha`, so again the total slack
is zero. Each half gadget recovers exactly its half-port formulas.
Mixing the two gadget types in one cycle would not justify this argument;
the draft correctly uses separate cycles.

The coupling input has one full positive port and two distinct half
complementary ports. Its exact supply of two forces
`x_full+2(1-x_half/2)=2`, hence equality of the cycle signals. All
three ports are at quality three, all are distinct physical arcs, and
the source degree is three. A cycle with only one gadget uses the two
different outputs of that gadget and is valid.

Every previous averaging equation, signed leaf, padded zero, and root
bound is therefore restored without adding a lower quality row. The
reverse construction fills the cycles for any valid signal, including
signal endpoints. The zero original-intake case remains feasible, with
possibly nonzero complementary leaves and auxiliary averages. Each
signal gains only a constant number of gadgets for coupling, so size and
the previous polynomial coefficient-occurrence argument are preserved.
The degree-three and upper-flow-at-most-four claims remain valid. Input
quality values remain distinct data values even when numerically equal;
they do not identify nodes or create alternative routes.

The observation about cyclic source lower bounds is correct. If only
their lower bounds are dropped, their upper bounds still force total
zero-quality endpoint flow at most `2r`. Exact demands/middle supplies
and upper quality force at least `2r`; equality and all individual source
contracts follow. This is not used to delete the other flow contracts;
that requires the separately reviewed penalty.

The independent constructor and checker
[independent_upper_quality_review.py](../code/pooling_bypass_copy/independent_upper_quality_review.py)
uses only original input/output arcs, supplies, demands, and homogeneous
upper quality inequalities. It contains no lower quality rows or hidden
copy, cycle-signal, averaging, or source-cone equations. It passed:

- 100 network projection LPs against the explicit source cones;
- 94 complete fixed-composition pooling LPs, including 46 excluded
  compositions;
- degree, upper-capacity, and distinct-arc assertions on every network.

The tests include zero and one-leaf rows, repeated occurrences, padded
trees, empty simplex sections, and shifted qualities. Increasing only
cyclic source upper bounds from two to four changes the maximum of
`x0-x1` from zero to two for a cone requiring equality. This provides
a direct negative control for the mechanism that forces quality
tightness. Eight additional penalty LPs restored all contracts under both
intake and private-source rewards.

This establishes correctness of the refinement, not its priority in the
literature. The unrestricted pool in-degree and ordinary binary-encoded
hardness qualification must remain explicit.

## Further refinement: input out-degree two

The subsequent splitter proposed by the author also passes. A degree-three
quality-three input of exact supply two feeds ports with capacities
`c=(2,1,1)`. Replace it by three separate quality-three inputs of exact
supplies `c_h`. Each feeds its original port and one new common collector
output, of exact demand two and upper quality three. Its residual flow
is necessarily `c_h-f_h`. The collector equation gives
`sum f_h=sum c_h-2=2`, exactly the original supply equation. Conversely,
every original feasible port assignment has nonnegative residuals within
their capacities and fills the collector. Its quality row is automatic.

Each new input has two arcs, and the collector has three. All other
inputs already had degree at most two. Upper bounds remain at most four,
and all added contract values are integral. The added sources have no base
reward; the original rewarded conversion sources are unchanged. Thus the
same exact penalty proof applies after adding these contracts and
recomputing its explicit constants and objective offset.

The independent checker now implements this splitter directly on its own
node/arc representation. It passed 24 additional checks: eight projection
comparisons and sixteen penalized fixed-composition comparisons, covering
both quality shifts and both reward realizations. It asserts input
out-degree at most two and output in-degree three after splitting. The
combined upper-only theorem can therefore claim input out-degree at most
two, while retaining output in-degree at most three and unrestricted pool
in-degree.
