# Closure of the continued research program

Later update: the user reopened the potential-flow topic on 2026-09-06.
The [new continuation record](potential-flow-reopened-status.md) supersedes
this historical closeout for that topic, including its weighted-cactus boundary.
Other directions remain outside that follow-up.

Date: 2026-09-05. This record responds to the instruction to finish the
directions already started, verify them, and stop without opening new
directions. It supersedes historical running, pending, and unfinished labels
in the research log and earlier status notes. All existing proof and review
tasks in this closing batch are complete. The remaining mathematical
questions are explicitly documented as unresolved boundaries. Research has
stopped; no further directions were started.

Independent reviews are checks by separate research agents, not external
peer review or formal proof-assistant certification. Literature searches
support qualified comparisons; they cannot establish publication priority.

## Final developments and proof records

| Existing direction | Closing outcome |
| --- | --- |
| Polynomial inverse approximation | The [signed-coefficient inverse lemma](certified-monotone-polynomial-inverse-approximation.md) is complete with two full audits. It constructs a uniform rational piecewise-polynomial approximation in polynomial time in dense degree, coefficient encoding, and accuracy bits, including interior derivative zeros. The positive-coefficient version retains sharper bounds. |
| Bilevel resource coupling | The [fixed-resource algorithm](../results/bilevel-fixed-resource-accuracy-bit-algorithm.md) and sharper [one-resource result](../results/bilevel-one-resource-accuracy-bit-algorithm.md) are promoted. Both final-scope audits cover arbitrary dense strictly convex polynomial local costs, signed coefficients, and interior derivative zeros. Fixed leader and resource dimensions permit polynomial dependence on accuracy bits with exactly feasible rational leader output. No response-dependent upper constraints are allowed. |
| Two-quality pooling | The [convex-feasibility result](../results/pooling-two-source-qualities-convex-feasibility.md) has two final-scope audits. It permits arbitrary bypass topology, source supply intervals, exact product contracts, and restrictive upper pool capacities. A shared convex quadratic lift gives exact rational feasibility. |
| Contracted degree-two pooling with a common capacity | The [common-capacity theorem](../results/pooling-contracted-common-capacity-algorithm.md) passed two full audits. Exactly contracted scalar or affine-rank-one pooling with bypass degree two permits arbitrary common lower/upper throughput bounds and individual arc lower bounds. Exact witnesses have polynomial algebraic degree. The prior missing symbolic-cut and support-function argument is complete; its submodular identities are classical and attributed. |
| Global energy design | The [any-graph energy maximization result](../results/potential-flow-global-energy-maximization.md) is complete with two mathematical audits and an independent exact-certificate code audit. Its positive conclusion uses classical energy concavity and conic duality. The opposite globally correlated minimization problem retains its reviewed strong hardness. |
| Weighted flow path signs | The [signed-path corollary](potential-flow-weighted-sign-path-decomposition.md) passed a closing independent audit and exact checks. Fixed global cycle rank and a fixed marked path decomposition allow exact joint optimization with unbounded objective support. It is retained as a supporting refinement. |
| Pooling and power-flow real algebraic complexity | The [closing audit](review-existential-reals-closeout.md) reconciles the three `∃R` results and bounded-data pooling variant with their earlier two or three audits. It corrects scope, approximation, and novelty wording and saves exact winding-count and bounded-gadget checks. |

The strongest earlier completed contributions remain indexed in the
[README](../README.md): integer-precision construction and separation laws,
structural pooling and bilevel algorithms with matching restricted hardness,
potential-flow complexity boundaries, and spatial certificate lower bounds.
This closeout does not replace their assumptions with a blanket theorem.

## Corrections and verification limits

The [full thread inventory](research-open-thread-audit.md) checked review
records and outstanding investigations across integer precision, spatial
branch-and-bound, Benders, FBBT, and supporting elimination lemmas. It found
an actual omission in an older positive-polynomial feature note: affine
terms must be removed before its lower Jensen-distance comparison. The
restriction `k>=2` is now explicit and was independently checked by root.
The promoted separable theorem uses a different, already-reviewed direct
Jensen argument and is unaffected.

The power-flow result retains real angle-difference constraints or the
specified reference-angle boxes. Principal angle differences alone permit
nonzero winding and do not justify the equal-angle reduction. Its original
audits found and repaired that flaw; the closing check confirms the
restriction and tests the winding encoding exactly. The introductory
wording and numerical verification claims now respect this scope.

The pooling `∃R` threshold theorem does not imply ordinary feasibility is
nontrivial when all lower flow bounds vanish. Its fixed-data variant also
has an instance-dependent objective threshold. The one-pool theorem needs
unbounded quality count. These distinctions remain explicit in the results.

Several apparent pending tasks were stale labels. The cactus restoration
bound, power-law region extension, FBBT source assessment, fixed-condition
vector addendum, and exact ternary-count family already had completed
reviews. Their status records are reconciled. The
[supporting source closeout](supporting-results-source-closeout.md) covers
facial pooling integrality and the relative-gap spatial result without
claiming exhaustive novelty clearance.

## Questions closed as unresolved, not assumed results

- A dimension-independent binary overhead for one input and arbitrarily
  many convex outputs under box error: individual output violation regions
  do not supply the needed simultaneous lattice argument. The growing-input
  degree-32 separation does not resolve this question.
- Weighted nomination optimization with fixed rank per block, rather than
  fixed global rank: intermediate blocks contribute varying algebraic
  functions of shared decisions. The existing fixed-value summation method
  does not optimize those functions.
- General degree-two pooling with unrestricted contracts or dense arc
  economics: the closed restricted algorithms do not cover those models.
  Generic continuous path elimination retains its recorded large explicit
  representation obstruction.
- One-quality, upper-quality-bounds-only pooling `∃R`-hardness: the attempted
  gadget route remains incomplete. A connection to concave-only constraint
  systems is not a reduction equivalence or an impossibility proof.
- Arbitrary affine spatial branching: the established lower bounds use
  specified branching and node-relaxation systems. Known cuts or
  decomposition solve some constructed instances; there is no general
  optimization-hardness claim for them.
- Earlier CIA, positive-multilinear, incidence-width, common-factor, and
  rank-one questions were already closed with explicit unresolved limits
  in the [previous closeout](research-closeout.md). They were not restarted.

The [flow closure inventory](potential-flow-energy-closure.md) and
[general thread inventory](research-open-thread-audit.md) give the detailed
dispositions. Brainstorm-only alternatives were not started projects and
were not investigated during this closure. Open mathematics and missing
historical literature are retained as limitations, not presented as solved.

## Reproducible verification

The theorem proofs justify the universal claims. Exact arithmetic and
independently formulated numerical checks supplement them. The final notes
link scripts and record their model and precision limits. The algebraic
and oracle-based complexity results are not represented as implemented
production solvers.

Significant closing checks include:

- Polynomial inverse: 15,504 exact panel checks, 20 rational centers, 236
  coefficient/Cauchy checks, 60 inverse enclosures, 80 modulus checks, and
  three complex-critical pairs.
- Bilevel: 7,200 one-resource checks and 11,424 fixed-resource checks,
  including signed marginals, degenerate follower faces, nonzero repairs,
  and resource-projection identities.
- Two-quality pooling: 160 original-physical versus convex-QP numerical
  comparisons and 240 independent exact rational network checks.
- Contracted common-capacity pooling: 360 exact symbolic-path cases; the
  two independent support checkers covered 128 and 36 networks, including
  support extrema and capacity-intersection reconstruction.
- Global energy: exact cone and physical-state checks, the zero-gap `3/4`
  triangle certificate, 99 certificate and 99 gauge checks, and rejection
  of 151 malformed direct inputs and 294 corrupt CLI inputs.
- Power-flow angle encoding: 360 exact scaled angle pairs and 4,136 cycle
  checks, including 256 nonzero windings. Bounded pooling gadgets: seven
  exact physical witnesses and 300 structural instances.
- Signed weighted paths: 192 exact paths, 32 returning paths, 275 zero
  source coefficients before perturbation, and 3,394 threshold checks.

These are the completed owners' recorded reruns, not a claim that every
historical program was rerun or that numerical solver tolerances prove
universal statements. The final repository hygiene check is recorded below.


The final repository check examined 2,650 local artifact links across 880 authored Markdown documents, with no missing targets, and parsed all 246 Python files under `code/` without syntax errors. `git diff --check` passed. The check excludes imported literature full-text markup and does not validate remote URLs or Markdown anchors. All research and review agents completed their assigned work.
