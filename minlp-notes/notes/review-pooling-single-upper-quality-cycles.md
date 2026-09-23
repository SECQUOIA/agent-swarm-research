# Independent review: scalar upper-quality copy cycles

Date: 2026-09-05. Reviewer: `benders_review`.

**Verdict: the closed-cycle construction passes, and it composes with the
reviewed exact penalty.** This reviews
[the candidate](pooling-single-upper-quality-cycles.md), independently of
the other cycle reviewer. The final combined model needs only one scalar
upper quality specification per output, upper flow bounds, and nonnegative
flows. It retains one pool, input total out-degree at most three, output
total in-degree at most three, and pool out-degree two.

For a full gadget, exact output mass and its single upper quality bound
give `b_j<=alpha_j`, after dividing by its own positive endpoint quality.
Summing all zero-port cycle source equations gives total `alpha=2r`.
Exact demands minus exact middle supplies give total endpoint mass `4r`,
hence total `b=2r`. Every individual nonnegative slack `alpha_j-b_j`
must therefore vanish. This works even when different full gadgets have
different positive endpoint qualities, so intake-conversion gadgets can
join the same cycle. Individual full-copy formulas then follow, and the
links equate successive signals. A one-gadget cycle has two distinct
output endpoints and does not introduce a parallel arc.

For the separate half cycle, the quality slack is `alpha_j-2b_j>=0`.
Its zero-port total is `2r`, while exact demands and middle supplies
give endpoint total `3r`. Thus total `b=r`, and again every local slack
vanishes. Its half-copy formulas and common signal follow. Keeping full
and half cycles separate is essential to this simple summation proof;
the draft does so explicitly.

The coupling source uses one full positive port and two distinct half
complement ports. Its exact supply 2 gives `x_f=x_h`. The full port is
allocated to an ordinary quality-three gadget, even when the signal also
has a conversion gadget of another quality. All three source ports
therefore have matching quality. A new full gadget is created when needed.
Distinct occurrence gadgets prevent parallel arcs for the repeated half
signal. This proves exact compatibility with averaging equations, signed
leaves, root bounds, and the zero signal.

The cycle closure and at most three extra occurrence gadgets per signal
add only polynomial size. Every new source has degree at most three and
each output still has three incoming arcs. Original conversion sources,
pool intakes, costs, and primary outlet constraints are unchanged. All
quality data are nonnegative and can be scaled into `[0,1]`. Both primary
outputs already use upper quality bounds only.

The exact-contract copy polyhedron is nonempty at zero original intake,
including when the source product polytope is empty. Its projection onto
intakes is the same homogeneous cone as before. Its constraints remain
linear in copy flows, and its contracts retain zero-one coefficient
rows. These are exactly the properties used by the
[independently reviewed penalty](review-pooling-upper-flow-only-penalty.md).
The penalty can therefore remove all positive lower flow bounds without
reintroducing any lower quality constraint or changing degrees and upper
capacities. The fixed-one-parameter LP certificate supplies NP membership.

I inspected the assembled checker, including its explicit deletion of
all lower quality specifications, and ran seed 43 with eight trials.
All 22 original-network global solves passed: 16 randomized/shifted
cases and six boundary cases. Degree, capacity, and distinct-arc checks
also passed. Relaxing cycle upper supplies changes the negative-control
profit from 10 to 20. The
[independent log](../code/pooling_bypass_copy/upper_quality_independent_review_output.txt)
is retained. The separate penalty review records 16 further independently
run global solves using this cycle model with all lower flow bounds removed.

This supports ordinary NP-completeness under the precise combined
restrictions. The proof does not establish strong NP-hardness, bounded
pool in-degree, or literature priority.

## Added input-degree-two refinement

The final source-splitting paragraph also passes a fresh independent check.
For a degree-three quality-three input with exact supply 2 and port
capacities `(2,1,1)`, replace it by three distinct sources of the same
quality and exact supplies `c_h`. Each source supplies its original port
and a new common collector. Conservation forces the latter flow to be
`c_h-f_h`, which is nonnegative and within its capacity whenever the
original port is within `[0,c_h]`. The collector's exact demand
`sum c_h-2=2` is equivalent to the original equation `sum f_h=2`.
Its upper quality bound is redundant because all incoming qualities
coincide. This proves both extension and projection without extra routes.

The splitter adds a constant number of nodes and arcs per averaging or
full/half coupling source. Every new input has two arcs; every collector
has three. Existing output incoming degrees and all pool flows are
unchanged. Thus input total out-degree can indeed be reduced to two,
while output in-degree remains at most three and the pool out-degree
remains two. No lower quality constraint is introduced.

For the penalty, include the new source supplies and collector demand
among the contract rows. Their coefficients remain zero or one and the
right-hand sides remain integers, now including 1. The copy polytope
is still bounded and nonempty with exactly the same intake projection,
so the proved error-bound and radial-repair argument applies unchanged
after recomputing its explicit dimension and coefficient bound. The
production-cost reward inputs are not among the split sources, and the
uniform cost/revenue offset still cancels by mass conservation.

I independently ran the split checker with seed 59 and six trials:
18 exact-contract original-network solves passed, including its boundary
cases and a negative control changing profit 10 to 20. I also ran the
all-upper-flow split penalty checker with seed 61 and six trials:
12 global solves passed for both reward conventions, with the zero-penalty
control profit 15 restored to `15/2` at experimental penalty 100.
The [split log](../code/pooling_bypass_copy/split_inputs_independent_review_output.txt)
and [split penalty log](../code/pooling_bypass_copy/split_inputs_penalty_independent_review_output.txt)
are retained. These checks support the stronger input-degree-two version;
the previous warnings about strong hardness and priority still apply.
