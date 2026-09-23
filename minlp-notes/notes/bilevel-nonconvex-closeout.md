# Bilevel follow-up: classical positioning and nonconvex computation

Date: 2026-09-07. This follow-up addresses the useful remaining work identified
in the comments on the [previous continuation](bilevel-reopened-closeout.md).
It adds a verified executable nonconvex specialization and a systematic
classical comparison. It does not claim a new general complexity theorem or
publication priority for classical envelope algorithms.

## Results

The [exact scalar algorithm](bilevel-nonconvex-scalar-algorithm.md) now optimizes
a tariff against a box follower with positive diagonal local quadratic costs
and a concave rank-one quadratic aggregate. The complete follower Hessian and
its reduced aggregate cost may be nonconvex. The leader enters through the
aligned term `gamma*x*(u^T*z)`. This restriction is essential to the implemented
specialization and is narrower than the general fixed-aggregate theorem.

The algorithm constructs the complete global response graph, including isolated
ties and flat intervals. It handles affine upper constraints, optimistic and
universally feasible pessimistic semantics, infeasibility, and attainment.
It returns exact algebraic values and witnesses of degree at most two.
Globality follows from comparing all scalar candidates after exact convex
fiber elimination. It is not inferred from follower stationarity.

A two-variable capacity example gives an optimistic maximum `51/160` at tariff
`17/20` and aggregate `3/8`. The pessimistic problem has the same supremum but
no optimizer: the second response tied at the limiting tariff violates capacity.
The solver correctly distinguishes these outcomes. This is a useful exact
example and regression, not a claim that pessimistic nonattainment is new.

The [source comparison](bilevel-nonconvex-source-positioning.md) connects the
scalar value computation to classical nonconvex piecewise quadratic conjugates.
It also proves and illustrates why convexifying the follower can preserve all
optimal values while adding false response choices. A one-variable example
makes an actually infeasible upper equality appear feasible after convexifying
the reaction graph. Exact reconstruction must keep contact with the original
objective. A [figure](../code/bilevel_nonconvex/figures/convex_envelope_false_choices.pdf)
and reproduction script are included.

## Practical evidence and limits

The [computational report](bilevel-nonconvex-computation.md) and
[raw data](../code/bilevel_nonconvex/benchmarks.json) retain three-run timings,
multiple heterogeneous seeds, original-coordinate verification, and the slower
initial implementation.

| Experiment | Measured result | Interpretation |
| --- | --- | --- |
| Same heterogeneous 12-variable case before/after incremental envelope insertion | Build median falls from 15.882 s to 3.079 s | Avoiding inactive pairwise crossings materially improves this implementation |
| Heterogeneous 48-variable case | Build 18.699 s; upper optimization 2.922 s | Exact symbolic processing remains costly as distinct response events grow |
| Two repeated coordinate types, 1,000 variables | Build 0.255 s; constrained upper optimization 1.261 s | A genuinely nonconvex large population is tractable when it has few response types |

The repeated-type family has exactly three fiber pieces and seven atlas points.
Its reduction to the two-variable model follows from strict local convexity
within each type, and its exact optimum scales by the replication factor.
It is deliberately distinguished from heterogeneous-event scaling.

The independent active-face oracle answers fixed-price follower queries, a
smaller task than solving the continuous leader problem. Its timings are not
presented as an equivalent competing bilevel solve. Local-solver failures are
illustrated by an exact one-variable example. No superiority over a production
global solver, or performance on calibrated application data, is established.
The unfavorable earlier screening-versus-MILP result remains in the record.

## Classical positioning and paper organization

The [classical comparison](bilevel-classical-positioning.md) now supplies a
related-work draft, parameter/semantics/output table, precise locators, and
explicit source-access limits for Deng, Liu–Spencer, Jeroslow,
Hansen–Jaumard–Savard, Vicente–Savard–Júdice, Buchheim, the Kleinert and Beck
surveys, Ketkov–Prokopyev, and Sugishita–Carvalho.

It confirms several corrections to the supplied comments:

- Deng's classical positive result fixes **follower** dimension. The fixed
  structural dimensions here permit growing follower dimension. Neither
  comparison should be described as fixed leader dimension alone.
- The existing polynomial-bit small gap already excludes polynomial runtime
  in accuracy bits unless `P=NP`. Strong hardness is not needed for that claim.
- An inverse-polynomial absolute gap in the same bounded-coefficient,
  uniformly conditioned dense-box class would contradict its existing
  polynomial-in-`1/epsilon` approximation algorithm unless `P=NP`.
- The positive fixed-dimension bounds are XP-type. They are not formal FPT
  bounds. The available boundaries do not prove the necessity of each fixed
  parameter separately in every theorem.

The [paper scope](bilevel-paper-scope.md) selects the fixed-normal optimistic
quadratic-block model as primary and puts response semantics, robustness, and
accuracy/output variants in a separate table. Screening is a secondary result
with conditional guarantees and unfavorable current performance evidence.
Integer followers and new graph-parameter classifications are different
research directions, not missing premises of the current continuous results.

## Independent verification and corrections

The scalar proof and code passed two independent full reviews:
[first](review-bilevel-nonconvex-one.md) and
[second](review-bilevel-nonconvex-two.md). Their checks include 86 adversarial
exact cases; 350 original-coordinate face comparisons; 72 atlas point/cell
comparisons; 30 independent all-pair-partition comparisons; and 11 additional
edge cases. The separate benchmark oracle passed 340 response checks at 136
query entries across eight cases. Counts include the repetitions and endpoint
representations described in the reports; they are not counts of independent
theorems or randomly sampled applications.

Review corrected floating-point inputs slipping into the rational API and
algebraic midpoint witnesses potentially exceeding the promised degree two.
Exact rational interior samples now preserve the output guarantee. The proof
also distinguishes polynomial bit cost from abstract branch-processing counts.
The revised incremental envelope, all ties, singular/fixed coordinates, signed
weights, reversed tariff coupling, and nonattainment were included in review.

The classical comparison received a separate
[independent source audit](review-bilevel-classical-positioning.md). The
convex-envelope contact identity and false-feasibility example received
independent mathematical review. The proposed paper scope received a read-only
consistency check; its accuracy-bit wording was corrected to describe runtime,
not the error itself.

## Stopping decision

This closes the bounded follow-up. The main computational omission has a
concrete, globally exact implementation with independent checks and honest
scale measurements; the classical-positioning omission has an audited source
comparison. The current theorem packages and this evidence are ready to use
when writing a theory paper. This does not mean that a submission-ready
manuscript or an industrial solver has been produced.

General polynomial aggregates, unaligned leader perturbations, more leader
coordinates, and large heterogeneous populations would require materially
broader implementation work. They are not unresolved correctness conditions
of this specialization. Existing exact theorem proofs already cover their
stated broader models. No new hardness or integer-follower program is opened
as part of this follow-up.

The [code guide](../code/bilevel_nonconvex/README.md) gives reproduction commands.
The final [verification record](../code/bilevel_nonconvex/verification_summary.json)
records checked artifacts, command outcomes, and hashes. Historical verification
records from the first continuation remain historical; unrelated concurrent
repository work was preserved.
