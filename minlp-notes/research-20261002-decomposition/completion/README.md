# Completed solver implementations and further results

This phase follows the user's renewed instruction to finish the remaining
recommended work. It closes implementation gaps identified after the first
technical report and investigates concrete further extensions. The earlier
74-run benchmark records and their source snapshots remain historical evidence.
New results are recorded separately here.

Start with the updated [integrated report](../document/main.pdf), its
[claim and evidence map](../document/COVERAGE.md), and the
[solver interfaces](../solver/README.md). The entries below link the detailed
assumptions, algorithms, certificates, tests, and independent reviews.

| Former gap or extension | Completed result | Scope |
| --- | --- | --- |
| [Exact rational output](exact-output.md) | Rational reconstruction, singular stationary-face LP recovery, original-data value separation, and independent proof replay | Eventual exact recovery for every bounded rational mixed box QP as all limits increase; no efficient arbitrary-optimal-set bound |
| [Reusable exact optimization](rational-oracles.md) | Rational LP and convex box-QP with checked optimality, infeasibility, and unboundedness evidence | Capped simplex and active-face enumeration; no polynomial runtime claim for these implementations |
| [Finite trees and decomposition](finite-tree.md) | Shared branching-tree DP, every unary margin, infeasible states, and deterministic scope-preserving elimination heuristics | Full finite tables; heuristic width bounds and explicit state caps |
| [Integrated recourse](recourse.md) | Automatic affine recognition, exact substitution and lifting, minimum-cut core discovery, and changing-active-set convex factors | Independently checked original-model transformations; partition discovery remains heuristic |
| [Mixed submodular recourse](submodular-recourse.md) | Actual greedy-base mixture construction through exact convex queries and Lovasz-extension cutting planes | Supported signed concave/convex partition; finite but potentially factorial cut count |
| [Coupled constraints](constrained-solver.md) | Reusable TU-fiber models, full or equality-direction curvature, exactly feasible filtering, and nonunique exact recovery | Verified TU matrix, explicit native integer labels, and width-XP costs |
| [Optimal sets](optimal-sets.md) | Unknown-growth diagonal-class discovery and compact full-set endpoint certificates with membership checking | Specified certificate classes; a failed discovery trial is inconclusive |
| [Polynomial factors](polynomial-solver.md) | Explicit rational polynomial model, verified curvature bounds, sparse corrected grids, filtering, and replay | Fixed-degree theory; arbitrary-degree inputs expose their actual evaluation and encoding costs |
| [Polynomial boundary output](polynomial-boundary.md) | Discovered monotone face reductions and exact rational or implicit strongly convex optimizer descriptors | Sufficient interval tests and bounded restart search; no implementation-level FPT bound |
| [New theory](theory/README.md) | Nonunique TU union filtering and curvature cancellation across piecewise convex responses | Explicit projection/partition assumptions; neither gives the unrestricted parameterized theorem |

Shared finite-table operations belong to one module. Checkers recompute the
model-specific bounds and history; several independently implement the
Bellman arithmetic, while the convex-factor checker reuses the finite DP
engine. Component and integration reviews record that assurance boundary.
These are exact-arithmetic reference implementations, not formally verified
software or demonstrated replacements for production MINLP solvers.

The proofs establish the stated universal claims. Finite tests check code,
examples, adversarial inputs, and regressions. A resource-limited solve returns
valid partial bounds or an explicit inconclusive/unsupported result; it does
not report unproved optimality or class nonmembership.

Only targeted checks and bounded experiments are run. Other research topics,
their dirty files, and their background jobs are outside this phase. No commit,
submission, upload, or external message is part of this request.

## Verification and experiments

The [validation record](../solver/VALIDATION.md) lists the targeted commands.
The final combined suite passed **158 tests**. Its
[output](targeted-tests.txt) and [source hashes](targeted-tests-manifest.json)
are saved.
Each completion note links its component review. The
[integration review](reviews/integration/REVIEW.md) checks shared interfaces,
JSON round trips, original-model binding, and certificate replay across
backends. These are internal research-agent reviews, not external peer review.

The [new benchmark results](benchmarks/RESULTS.md) and
[findings](benchmarks/FINDINGS.md) retain exact references, successful proofs,
resource failures, rejected inputs, separate solve/replay costs, and frozen
source snapshots. The first release's 74 runs remain in
[the original benchmark directory](../solver/extra-benchmarks/README.md).
Measured results do not imply a general solver speedup.

The new experiments contain **84 configurations**: 68 completed mathematical
requests, 14 checked partial or unsupported-class bound intervals, one
rejected invalid TU input, and one inconclusive boundary search. All **82
available certificates replayed successfully**. Independent checks cover 62
numerical reference enclosures and two implicit-optimizer containments.
The [combined summary](benchmarks/combined-summary.json) and
[verification record](benchmarks/VERIFICATION.md) reconcile these counts.

## Remaining research boundaries

The completed implementations and proofs close the concrete gaps above.
They do not settle the unrestricted width-plus-negative-curvature/growth
algorithm, general certified local-message error bounds, width-FPT coupled
constraints, efficient arbitrary unknown optimal-set descriptions, polynomial
boundary output from point growth alone, or the one-draw exact smoothed TU
extension. These require new mathematical results. Finite exact quadratic
recovery without uniqueness is now established and implemented; efficient
general recovery and full-set representation are different questions.

Potential production work includes smaller proof histories, faster exact
or verified inexact arithmetic, and stronger decomposition heuristics. The
present bounded evidence does not justify a performance claim for those
unimplemented methods. They are distinct from correctness or proof gaps in
the delivered scoped algorithms.
