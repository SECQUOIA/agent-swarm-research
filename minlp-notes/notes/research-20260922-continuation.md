# Research continuation, September 22

Status: completed the topics already underway, then stopped at the user's
request. No further research directions were started after that instruction.
This closeout distinguishes completed results from documented open questions.

## Main results

One principal positive result is the
[universal four-aggregation theorem](../results/four-aggregation-strict-pdlc.md).
For three strict quadratic inequalities under homogeneous PDLC, four good
aggregations suffice in every positive dimension, including dependent
triples. Four is necessary in dimensions at least three, by an independently
checked existing BDS example. The proof removes regularity and infinity
assumptions from the published Blekherman–Dunbar bound using positive
definite inward perturbations and a strict limit. Several independent reviews
checked the substantive simplifications and final version. A primary-source
audit found no explicit universal strict theorem, while documenting an
unresolved dependency in a stronger displayed dissertation statement.
Novelty remains provisional; the proof relies on the published theorem.

The complementary
[explicit infinite-aggregation example](../results/infinite-quadratic-aggregation-hhc.md)
satisfies hidden hyperplane convexity in four variables but requires a
continuum of distinct good aggregation rays for an exact strict hull
description. Finite aggregation also fails for its closed hull. This answers
the mathematical assertion of BDS Conjecture 3.1 in the inspected preprint.
The result carefully distinguishes original-space quadratic descriptions
from finite SDP lifts and does not claim the underlying SDP convexification
is new. Two proof reviews, a separate novelty comparison, and a fresh
integrated review checked the important arguments and corrected source
version numbering. Priority remains provisional.

A separate result concerns
[bandwidth-two indicator quadratic optimization](../results/indicator-quadratic-treewidth-two-hardness.md).
Exact NP-completeness persists for arbitrarily well-conditioned Hessians,
including a fixed matrix family with positive penalties, or unit penalties
and bounded linear terms with an instance-dependent matrix. The different
accuracy and coefficient tradeoffs are explicit. The construction uses an
established SUBSET SUM accumulation idea; its combined restrictions and
structural boundary are the candidate contribution. A fresh reviewer checked
both reductions, and the coordinator independently derived the stronger
conditioning and unit-penalty versions.

Its [fixed-data message follow-up](research-20260922-constant-data-messages.md)
proves that a scalar conditional value function can need `2^n` distinct
polynomial formulas with a fixed rational stage cost and a near-identity
Hessian. A matching horizon-independent accuracy law holds for pruning
original support quadratics. Fresh review confirmed both bounds and identified
classical quadratic-pruning and covering antecedents. The unconditioned
objective is easy, so this does not replace the separate hardness reduction.

The strongest solver-oriented result is
[exact smoothed message construction under spectral bounds](../results/smoothed-spectral-indicator-messages.md).
For fixed-treewidth positive definite indicator QPs with polynomial numerical
bounds, independent rational penalty noise permits exact construction of
every subtree message on a prescribed bounded separator box and an exact
global optimizer in polynomial expected bit time. A grid of at least `2n`
points suffices, requiring `O(log n)` random bits per penalty. The proof
combines a classical shattered-set inequality, a near-optimal-support count,
certified approximate partition enumeration, and a parameter net. Two fresh
reviews checked the complete argument, including spectral conditional bounds
and bit complexity. The construction requires neither diagonal dominance nor
an invariant box for recursive messages. It does not establish a practical
speedup or definitive publication priority.

The [earlier scalar algorithm](../results/smoothed-indicator-block-dp.md)
retains sharper explicit operation bounds on bounded blocks. The
[direct treewidth algorithm](../results/smoothed-fixed-treewidth-indicator-dp.md)
and [higher-moment theorem](research-20260922-envelope-higher-moments.md)
are independently reviewed alternatives. The final construction needs only
first moments. Its additive certificate is useful but not a new approximation
frontier: ordinary grid dynamic programming already gives additive
approximation under these bounds. A
[reviewed magnitude obstruction](research-20260922-smoothing-magnitude-obstruction.md)
shows why arbitrary encoded coefficient magnitudes cannot be covered by a
uniform bit-polynomial smoothing claim merely from fixed conditioning and
width two.

## Corrections and directions not promoted as major contributions

- The [error-bound transfer](research-20260922-error-bound-transfer.md)
  gives a shorter and more general proof of the existing clustering result.
  Its core is classical exact-penalty growth, explicitly stated by Anitescu.
  The coordinator inspected that source and an independent reviewer
  confirmed the comparison. The result note, README, and historical review
  now narrow the novelty claim. Sound application results were retained.
- [Moment-based control decomposition](research-20260922-moment-control.md)
  includes a fixed two-stage example with exact gap `2E_k(|x|)=Theta(1/k)`
  and a dynamics-preserving repair argument. The
  [novelty screen](research-20260922-separator-novelty.md) found strong
  antecedents in approximate linear programming and marginal moment
  transport. A [fresh proof review](review-20260922-moment-control.md)
  confirmed the repair and exact gap, clarified normalization and measurable
  action domains, and identified the precise earlier duality theorem. This
  remains supporting work.
- The [oracle investigation](research-20260922-oracle-conjectures.md)
  records a newer derivative-free lower-bound source and a candidate
  full-information separation transfer. It does not settle the general
  binary-oracle conjecture. Its
  [fresh review](review-20260922-oracle-transfer.md) confirmed the proof
  under its assumptions but located the core geometric mechanism in Basu's
  earlier work. The source note now narrows attribution and makes chart
  quantifiers explicit.
- The [star inverse-polytope investigation](research-20260922-frontier-scout.md)
  embeds a correlation-polytope face in the inverse-principal polytope of
  a well-conditioned star. It targets a standard intermediate formulation,
  not the original epigraph hull. A
  [fresh review](review-20260922-star-polytope.md) confirmed the face and
  lower-bound transfers. The hard coordinates are leaf-to-leaf inverse
  entries, so this is not a lower bound for the sparse epigraph projection.
- The [general Gram-map theorem](research-20260922-gram-hyperplane.md)
  sharpens the HHC construction to the threshold `r>=k`. Its key matrix
  concavity is established fidelity theory. A
  [fresh review](review-20260922-gram-hyperplane.md) confirmed the exact
  image argument and sharp threshold. Its strongest current role is a
  reusable structural certificate supporting the aggregation example;
  novelty of the general formulation remains provisional.
- The [many-constraint span-three investigation](research-20260922-span-three-many.md)
  extends a known facet-elimination argument in one coefficient-cone case
  and gives a linear lower bound. A
  [fresh review](review-20260922-span-three-many.md) confirmed the proofs,
  source versions, and exact witnesses. It remains supporting work; the
  unresolved general-cone case cannot be filled by combining triple hulls.

## Targeted checks run by the coordinator

- `python3 code/research_20260922/check_treewidth_two.py`: passed 24 rational
  instances and 3,072 exact support QPs, including both hardness constructions,
  state activation, spectral row bounds, coefficient bounds and bandwidth.
  The final run includes the reviewer's tighter `|c|<=9` assertion.
- `python3 code/research_20260922/check_infinite_aggregation.py`: passed
  2,601 rational multiplier-ray identities and six finite-family outside
  witnesses. It uses exact Gram entries, not floating-point square roots.
- `python3 code/research_20260922/check_four_aggregation_pdlc.py`: passed
  the exact PDLC identity, strict feasible point, and four uniquely active
  aggregation-ray witnesses, including radical signs.
- `python3 code/research_20260922/check_constant_data_messages.py`: passed
  180 exact support QPs, 252 centers, 504 active-neighborhood endpoints,
  and 6,252 approximation checks.
- `python3 code/research_20260922/check_smoothed_block_dp.py`: passed
  nine instances, 66 whole-interval message comparisons, 892 support QPs,
  3,580 coordinate bounds, 864 derivative bounds, and 48 inactive atoms.
  Thirty-two checks exercised full quadratics outside their active regions.
- `python3 code/research_20260922/check_envelope_higher_moments.py`: passed
  2,295 exact distribution cases, 61,965 noise states, 48,813 conditional
  interval checks, and 6,885 moment inequalities.
- `python3 code/research_20260922/check_nearopt_enumeration.py`: passed
  3,276 near-optimal-count cases over 18,270 exact noise outcomes and
  12,420 adversarial enumeration runs, including complete near-optimal-set
  coverage, exact ties, and empty child cells.
- `python3 code/research_20260922/check_oracle_all_messages.py`: passed
  80 exact affine parameter families, 1,132 net points, and 200 active
  supports, including a support active only at one tie.
- `python3 code/research_20260922/check_moment_control.py`: passed the
  exact degree-one, degree-two, and degree-three matching-moment witnesses
  and the quadratic approximation-error identity.
- A topic-only Markdown scan passed local-link and trailing-whitespace
  checks on 65 result, research, and review files.

These finite checks establish the tested identities and cases. They do not
prove all-dimensional hardness, HHC, irreducibility, or novelty. Those claims
rest on the displayed mathematical arguments and qualified source comparisons.
No project-wide verification, CI inspection, or Lean formalization was run.

## Final reassessment and unresolved limits

The aggregation results remain the strongest geometric contributions. The
[accuracy analysis](research-20260922-aggregation-accuracy.md) gives a sharp
`Theta(N^-2)` uniform finite-aggregation rate, while a single
objective-dependent aggregation remains exact for each fixed linear
objective. Exact representational impossibility therefore does not itself
imply poor solver performance at a specified tolerance.

The indicator investigation progressed from exact hardness and exponential
messages to constructive smoothed tractability. Its final
[spectral-bound theorem](../results/smoothed-spectral-indicator-messages.md)
constructs all bounded-parameter message dictionaries using only a first
moment. The earlier [planar region theorem](research-20260922-higher-dimensional-smoothing.md)
and [higher-moment theorem](research-20260922-envelope-higher-moments.md)
remain useful independent results; the final algorithm does not require
planar curvature or algebraic envelope decomposition. The
[priority audit](review-20260922-fixed-treewidth-priority.md) compares the
final theorem with exact margin-based message methods, classical smoothed
conversion, and parametric enumeration. It does not establish publication
priority.

All existing proof-review requests in this continuation were completed.
Reviews prompted explicit measurability assumptions, numerical and bit-cost
qualifications, source-version corrections, and narrower significance
claims. Useful earlier arguments are preserved and linked to the stronger
results rather than represented as unresolved active work.

Unresolved questions are documented, not assigned as further work: the
many-constraint complementary-cone bound, definitive publication priority,
practical solver implementation and performance, and generalizations beyond
the stated assumptions. The current mathematical results do not claim to
settle those questions. Research stopped here as instructed.
