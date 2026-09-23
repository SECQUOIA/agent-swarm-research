# Independent review of the scalar nonconvex aggregate solver

Date: 2026-09-07. Reviewer: independent subagent `nonconvex_review_one`.

Scope: [algorithm and proof](bilevel-nonconvex-scalar-algorithm.md),
[implementation](../code/bilevel_nonconvex/scalar_solver.py), and the exact
adversarial checks in [review_one.py](../code/bilevel_nonconvex/review_one.py).
This review concerns the stated scalar aligned-tariff specialization, not the
full generality of the existing fixed-aggregate theorem or a novelty claim.

## Conclusion

The reviewed reduction, global-response enumeration, and leader optimization
are sound for the stated rational-data model. The implementation preserves
all tied global responses, including flat intervals. Its optimistic and robust
pessimistic conventions are clearly distinguished. No unresolved correctness
issue was found after the corrections below.

The independent script passes **86 exact checks**. Run it with
`python code/bilevel_nonconvex/review_one.py` in an environment with SymPy and
NumPy. It uses symbolic identities and exact inequalities, not tolerance-based
acceptance. The independent benchmark review separately checks original-space
active-face enumeration; this review deliberately concentrates on degeneracy,
semantics, and exact output.

## Proof audit

1. **Fiber compression is complete.** Strict convexity of the local diagonal
   objective makes the resource-constrained fiber minimizer unique. Replacing
   any other point on the same fiber improves the full follower objective,
   because the aggregate terms stay fixed. Signed aggregate weights retain
   monotonicity of the multiplier response: its slope is a sum of squares
   divided by positive diagonal coefficients. Zero-weight coordinates and
   fixed coordinates are treated separately. Zero-slope multiplier intervals
   contribute only a point, already covered by adjacent pieces; the globally
   constant aggregate has an explicit singleton representation.
2. **The candidates contain every global response.** A scalar quadratic on a
   closed piece is minimized at an endpoint, at its interior stationary point
   when its curvature is positive, or throughout the piece when it is flat.
   These cases exhaust the possibilities. The comparison uses follower
   objective values, so indefinite follower KKT points do not acquire a false
   global certificate.
3. **The envelope partition is sufficient.** Candidate domains have rational
   endpoints, and two candidate values differ by a polynomial of degree at
   most two. Between all their roots and domain boundaries, the ordering is
   constant. If two candidates win on an open interval, equality of their
   value derivatives gives `gamma*w_1=gamma*w_2`; since `gamma!=0`, they have
   the same aggregate and hence the same unique fiber minimizer. At partition
   points the code explicitly restores all distinct responses and flat pieces.
4. **Upper constraints and response semantics are handled correctly.** On an
   open cell, affine upper rows restrict the tariff to an interval and the
   objective is quadratic. At a tie tariff, optimistic feasibility intersects
   each minimizing fiber interval with all upper rows before maximizing
   revenue. Robust pessimistic feasibility checks every minimizing interval's
   endpoints, and its revenue takes the minimum over all responses. These
   endpoint tests are exact because both the rows and revenue are affine on
   a fixed fiber piece.
5. **Attainment is not conflated with a supremum.** Limits from open cells are
   initially recorded as unattained unless the selected tariff is interior to
   that cell. Actual tie tariffs are separately evaluated under the requested
   semantics. A constant objective receives a feasible interior sample. Thus
   pessimistic downward jumps or failure of universal feasibility at a limit
   do not produce a spurious optimizer. Optimistic feasibility is a closed
   subset of a compact response graph and therefore attains its maximum when
   nonempty, consistently with the examples checked.
6. **Exact output has the claimed bounded degree after correction.** Crossing
   tariffs have degree at most two; stationary tariffs and upper-row crossings
   inside an open cell are rational. Flat-piece tariffs are rational. The
   chosen affine response, revenue, and limit pair therefore remain rational
   or in a single quadratic field. The corrected interior sampler is rational,
   avoiding the degree-four midpoint issue described below.

The polynomial-bit argument applies to the explicit algorithm with exact
bounded-degree algebraic operations. It is not a practical speed guarantee for
SymPy. The implementation now inserts candidates into an incremental lower envelope
and retains earlier contact points for final global checks. It still does
repeated exact comparisons; its polynomial worst-case bound should not be
confused with an efficient large-instance implementation.

## Corrections identified and verified

- The initial rational-input guard rejected Python floats but silently accepted
  SymPy and some NumPy floating-point values by converting their already
  rounded values to rationals. The author now requires a genuinely rational
  symbolic value for non-string inputs. Regression cases include Python float,
  SymPy Float, NumPy float32, and NumPy float64. Exact decimal strings remain
  explicitly allowed as exact rational specifications.
- I independently identified a potential violation of the degree-two output
  claim: an arithmetic midpoint of two different quadratic endpoints can have
  degree four. A zero-revenue branch could retain this midpoint as its attained
  optimizer. The other independent reviewer had also identified this issue.
  The author replaced interior midpoints with exact dyadic rational samples.
  Checks cover independent radicals, negative intervals, and an interval of
  width `10^-30`.

## Distinct adversarial cases

The script includes a follower `f_x(z)=(x-1)z`, `z in [0,1]`, which has a whole
interval of responses at tariff one. Its optimistic optimum is one, whereas
its robust pessimistic supremum is one and is not attained. Additional upper
rows restrict the sole feasible optimistic response set at that tariff to an
interior interval or an interior singleton; robust pessimistic feasibility is
then empty. These cases exercise quantifiers that checking only an arbitrary
follower minimizer would get wrong.

A genuinely nonconvex follower `f_x(z)=-z^2/2+xz` has a two-endpoint global tie
at tariff one half. Optimistic revenue one half is attained; robust pessimistic
revenue has the same unattained supremum. Further cases reverse the revenue
ordering with negative tariffs, reverse the sign of `gamma`, flip a coordinate
and its aggregate coefficient, and handle zero aggregate weights, singleton
boxes, and a singleton leader domain. Close-radical sign checks ensure that the
review itself does not replace exact comparisons by a fixed tolerance.

This evidence supports correctness of this implementation. It establishes
neither priority over the resource-allocation and lower-envelope literature nor
superiority to a global optimization solver on applications.

## Incremental-envelope revision

The author replaced all-pair overpartitioning during this review. I audited the
revised `_insert_envelope` logic and reran the full suite. Inductively, each open
cell stores one true minimizer among the candidates already inserted. Adding a
candidate splits a cell at its domain endpoints and every equality with that
cell's winner; a rational interior comparison selects the new winner. Adjacent
cells with the same winner may merge, but the separate contact registry retains
all equality points. Thus a tangency that never wins on either adjacent open
interval is not lost. Singleton candidate domains are also added to the registry
even though they have no effect on open cells. Later candidates can make such
contacts obsolete; the final all-candidate scan at every registered tariff
correctly decides whether they are still globally relevant.

Twelve additional exact checks cover an isolated quadratic tangency, a
singleton-domain branch strictly below the neighboring envelope, later dominance
of both events, and a two-crossing branch combined with a bounded-domain
insertion. These checks use artificial branch polynomials to test the envelope
routine independently of the follower candidate generator. The final suite has
86 checks.

## Benchmark integration review

I independently checked [the computation note](bilevel-nonconvex-computation.md)
against `benchmarks.py`, `benchmarks.json`, and the retained pairwise-baseline
JSON. No new timing runs were needed. Recomputing every stored median from its
three samples reproduced the reported medians; the four old/new table rows
match their JSON entries. Exact symbolic comparison confirms that all four
baseline/revised revenue values agree. The verification counts sum to 340
response checks and 136 tariff query entries, as stated. These are explicitly
finite checks, with duplicate query entries acknowledged.

The grouped population reduction is valid. Jensen's inequality applied within
each identical coordinate type makes the local quadratic cost minimal only at
a uniform type response. If the two type responses are `a,b`, then the original
objective divided by `m` is exactly

`a^2/2-a+b^2/2-b/2-(3/10)*(a+b)^2+x*(a+b)`.

The original aggregate is `W=m*(a+b)` and capacity becomes `a+b<=1`. Thus the
reduction is exact for arbitrary positive integer `m`, including follower ties
and the robust pessimistic quantifier; it does not merely approximate a large
population by representative coordinates. I reran the two-coordinate
original-space oracle at `x=17/20` and verified the two global responses
`(3/8,0)` and `(1,5/8)`, each with normalized follower value `-9/320`.
The unnormalized population follower value is `-9m/320`.

On the capacity-feasible low-response branch near this switch,
`a+b=(5/2)*(1-x)`. Its revenue per copy is `(5/2)*x*(1-x)`, strictly decreasing
for `x>=17/20`. The high-response branch violates capacity. Consequently the
optimistic maximum is `51m/160`, attained at the switch with `W=3m/8`;
robust pessimistic feasibility excludes the switch and has that same
unattained supremum. The deterministic two-coordinate solver check reproduces
these formulas and the three fiber pieces/seven atlas points. Replication
preserves the fixed number of event types; the note correctly does not present
its 1000-variable timing as evidence for 1000 distinct response events.

The singular-face argument for the original-space value oracle is sound. The
same argument also captures extreme linear revenue among global minimizers:
start with a global minimizer having extreme revenue. Any feasible null
direction on its minimal face must have zero revenue derivative, since both
small signs are feasible and remain global minimizers. Moving to the boundary
therefore preserves both follower value and extreme revenue. Iteration reaches
one of the enumerated nonsingular stationary faces or a vertex.

The computational comparisons are appropriately limited. Old versus new atlas
construction compares the same task and instances, with historical baseline
provenance and cache/concurrency qualifications stated. The original-space
oracle's nine-price query time performs a smaller task than continuous-tariff
bilevel optimization; the note explicitly avoids treating it as a competing
complete solve. The distinct-event scaling limitations and absence of
application data or general-solver superiority are reported clearly. No
unresolved issue was found in this benchmark integration review.
