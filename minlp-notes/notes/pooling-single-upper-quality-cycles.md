# Candidate: one upper-bound quality through closed copy cycles

Date: 2026-09-05. Status: two independent reviews PASS, including the
input-degree-two refinement. The combined theorem is promoted in
[the final result](../results/pooling-one-pool-upper-bounds-np-completeness.md).

This construction removes every lower quality specification from the
[degree-three copy reduction](pooling-bypass-degree-three-hardness.md).
It uses one scalar quality and upper specifications only. Fixed flow
contracts remain at this stage. The separately proposed
[exact-penalty construction](pooling-upper-flow-only-penalty-hardness.md)
would then remove those contracts without introducing any quality row.
Both components have now passed their audits and are combined in the
linked result.

## 1. Full-copy cycles force their upper bounds tight

Use the full gadgets from the degree-three construction, including the
original quality-conversion gadgets. A gadget with endpoint qualities
`0,beta`, where `beta>0`, has two outputs of exact demand four and
upper quality `beta/2`. Its common middle input has quality `beta/2`
and exact supply four. Write the two endpoint flows at each output as
`alpha_j,b_j`, and its middle flow as `m_j`. The sole quality inequality is

```
beta b_j + (beta/2)m_j <= (beta/2)*4
iff b_j <= alpha_j,                alpha_j+b_j+m_j=4.
```

For a cycle of `r>=1` full gadgets belonging to one signal, connect the
second zero-quality endpoint of each gadget to the first zero-quality
endpoint of its successor using a quality-zero source with exact supply
two and exactly those two outgoing arcs. Indices are cyclic. For `r=1`,
these are the two distinct outputs of the same gadget, so no parallel
arc is introduced.

Summing these source equations gives total zero-endpoint flow `2r`.
Summing output demands and middle supplies gives total endpoint flow
`4r`; hence the total other-endpoint flow is also `2r`. Each inequality
`b_j<=alpha_j` must therefore be tight. Every gadget consequently has
the full-copy port formulas `x,2-x` on both endpoint sides. The zero-
quality links make its signal agree with its successor, so the whole
cycle represents one common `x in [0,2]`.

The values of `beta` may differ between gadgets: division by their own
positive `beta/2` gives the same inequality `b_j<=alpha_j`. Thus ordinary
gadgets with `beta=3` and intake-conversion gadgets with `beta=a_i>1`
can lie in the same full cycle. In every conversion gadget, its second
`a_i` port and actual pool intake still share their exact two-unit
source, so the intake equals this common signal.

Conversely, any common `x in [0,2]` extends to all full gadgets using
the original formulas. Every cyclic link then carries `2-x+x=2`.

## 2. Half-copy cycles

Half gadgets have endpoint qualities zero and three, common middle
quality one with exact supply three, and two outputs of exact demand
three and upper quality one. Their constraints give

```
3 b_j+m_j <= 3,
alpha_j+b_j+m_j=3,
therefore 2 b_j <= alpha_j.
```

Place the half gadgets for one signal in their own closed zero-port
cycle, again with two-unit zero-quality sources. Total zero-endpoint
flow is `2r`; total endpoint flow is `3r`; hence total other-endpoint
flow is `r`. All inequalities `2b_j<=alpha_j` are tight. The half-port
formulas follow: zero ports `x,2-x`, and quality-three ports
`x/2,1-x/2`. The cycle links impose one common half-cycle signal.
Every `x in [0,2]` extends to the cycle.

Full and half gadgets are not mixed in a single cycle: their endpoint
ratios differ. They are coupled explicitly as follows.

## 3. Couple the full and half versions of each signal

For every signal with a half-port occurrence, reserve one additional
full positive port and two additional, distinct complementary half
ports. Assign them to a quality-three source with exact supply two.
If the two cycles' signals are `x_f,x_h`, its supply equation is

```
x_f+(1-x_h/2)+(1-x_h/2)=2 iff x_f=x_h.
```

Allocate one gadget per reserved port occurrence, just as for all other
port occurrences. In particular the two half ports go to distinct
outputs. This source has degree three. If the signal previously had no
full gadget, the newly reserved full port creates one. Signals without
half occurrences need no coupling source or half cycle.

All averaging inputs, signed leaves, zero padding, root bounds, original
conversion sources and primary outputs are otherwise unchanged. The
full/half equality restores exactly the previous averaging formulas,
so the projection onto original intakes is the same homogeneous cone.
The original objective identity and polynomial source reduction carry
over unchanged. Zero original intakes remain feasible even when the
source polytope is empty; auxiliary averages may be nonzero.

## 4. Size and model restrictions

Each signal gains at most three gadgets and one degree-three coupling
source. Closing a chain uses at most one additional two-arc source.
The total construction is polynomial. All input total out-degrees and
output total in-degrees remain at most three. Pool out-degree is two;
pool in-degree is unrestricted. Upper flow bounds remain at most four.
The two primary output bounds were upper-only already. All quality
lower bounds can therefore be deleted: there is just one scalar quality
with upper output specifications. Its nonnegative rational input values
and bounds can be scaled into `[0,1]` with polynomial encoding length.

The corresponding NP upper bound uses one pool-quality parameter.
The candidate conclusion is ordinary NP-completeness for this precise
one-pool, one-upper-quality, degree-three, fixed-flow-contract model.
The penalty proof, if independently verified for this base, would further
remove all positive lower flow bounds. No strong-hardness or priority
claim is made. The published broad one-pool capacity hardness assertion
still limits novelty claims; the precise restrictions need their own
source comparison.

## 5. Original-network experiments

**Reviewed additional degree refinement.** The input out-degree
bound can be reduced to two. Every degree-three input above has quality
three, exact supply two, and outgoing port capacities `c=(2,1,1)`.
Replace it by three distinct quality-three inputs with exact supplies
`c_h`. Input `h` feeds its original port, with capacity `c_h`, and a
new common collector output, also with arc capacity `c_h`. Give the
collector exact demand `sum_h c_h-2=2`; its upper quality three is
redundant. If the original port flow is `f_h`, its collector flow is
`c_h-f_h`, so collector demand is equivalent to `sum_h f_h=2`.
Conversely every original feasible port assignment extends this way.
Each new input has out-degree two, and the collector has in-degree
three. All other inputs already have out-degree at most two. Original
pool intakes, profits and upper capacities are unchanged; every new upper
capacity is at most two. This elementary complement-flow substitution
also applies before the penalty: its new exact contracts are simply added
to `Ew=e`. It does not reduce the output in-degree bound of three.

The [checker](../code/pooling_bypass_copy/check_upper_quality.py) builds
only original arcs, node supplies/demands, and scalar upper quality
constraints. It adds no lower quality inequalities, copy equations or
source-cone equations. It passed 26 original-network global solves,
including shifted qualities, empty source polytope, singleton rows,
repeated leaves, padding and zero reward. It checks degrees, capacities
and distinct arcs. The [log](../code/pooling_bypass_copy/upper_quality_output.txt)
is retained. Relaxing the cyclic sources' upper bounds changes a control
optimum from 10 to 20.

A first attempted negative control removed only cyclic sources' lower
bounds and caused no change. This is consistent with the proof: their
upper bounds give total alpha at most `2r`, while exact demands/middle
supplies and upper quality imply alpha at least `2r`, so the cyclic
source equalities are already implied. This observation is not needed
for the broader exact-penalty construction.

The [first review](review-pooling-single-upper-quality-cycles.md) and
[second review](review-pooling-single-upper-quality-cycles-second.md)
both PASS, including the input-degree-two substitution. The second
reviewer independently implemented that substitution and passed eight
projection comparisons and sixteen penalized comparisons, with degree-two
input assertions. The author also passed 26 global solves and 12 penalty
solves on the final substitution; logs are
[here](../code/pooling_bypass_copy/upper_quality_split_inputs_output.txt)
and [here](../code/pooling_bypass_copy/upper_quality_split_inputs_penalty_output.txt).

The penalty checker also accepts `--upper-quality` to use this cyclic
network. It passed 12 additional original-network solves with every
positive lower flow bound deleted and no lower quality rows, testing
intake rewards and private-input production rewards. The experimental
`M=100` matched the contracted reference and restored every contract;
the zero-penalty control doubled profit from `15/2` to 15. Its
[log](../code/pooling_bypass_copy/upper_quality_penalty_output.txt) is
retained. These numerical tests use a moderate penalty and do not verify
the explicit theoretical error-bound constant.
