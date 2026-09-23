# Bilevel continuation: results and paper-readiness record

Date: 2026-09-07 (UTC). Status: completed. All current theorem, implementation,
source-comparison, and independent-review tasks are closed within their stated
scope. Final repository checks are recorded below.

The subsequent [nonconvex follow-up](bilevel-nonconvex-closeout.md) strengthens
classical positioning and implements a genuinely nonconvex aligned scalar
aggregate case. Its separate review and benchmark record updates the practical
evidence below. Both closeouts describe source material for paper writing,
not a submission-ready manuscript or established industrial solver advantage.

This continuation responds to the user's request to develop impactful and
practically important bilevel results, investigate their literature, verify them
independently, and bring the current ideas to a state suitable for paper writing.
It concerns bilevel work only. Unrelated pooling, integer-dimension,
relaxation-limit, and potential-flow work was preserved.

## Main results

| Result | New capability | Essential qualification |
| --- | --- | --- |
| [Near-optimal follower robustness](../results/bilevel-near-optimal-response-robustness.md) | Exact robust feasibility, infimum, attainment decision, and algebraic adversarial witnesses with many quadratic local blocks and possibly nonconvex aggregate cost | Leader, block, aggregate, resource, and per-criterion measurement dimensions are fixed. The number of upper criteria may grow. A common polynomial-degree field is promised for one recovered worst response, not every unrelated witness together. |
| [Exact dense-quadratic screening](../results/bilevel-surrogate-screening-exact-optimization.md) | Recover the exact dense-follower bilevel optimum using at most `M*3^t` LPs after sound screening on a surrogate response cover | `M` counts cover cells and `t` uncertified statuses per cell. A supplied low-rank surrogate need not have small `t`. A quantitative perturbation neighborhood gives `t<=(r+1)q` from bounded vertex transition multiplicity. |
| [Convex aggregate accuracy-bit algorithm](../results/bilevel-convex-aggregate-accuracy-bit-algorithm.md) | Global approximation polynomial in requested accuracy bits for strictly convex local polynomial costs coupled by convex polynomial aggregate penalties | Fixed leader, aggregate, and resource dimensions; numerical degree matters. No uniform positive curvature or Slater point is needed. Rational recovery crosses nonlinear branch boundaries while preserving exact feasible-leader membership. |
| [Response-dependent polynomial upper data](../results/bilevel-response-constraint-accuracy-bit-algorithm.md) | Polynomial upper objectives and constraints, unconditional objective/violation approximation, rigorous posterior value intervals, and exact rational feasible approximation under explicit tightening conditions | Exact safety needs a quantitative tightening modulus. Convex reduced constraints with a strict anchor, or reserve decisions with uniform safe headroom, give concrete sufficient conditions. An isolated feasible optimum can defeat inner convergence. |

The constraint result composes with the nonlinear aggregate result. Polynomial
upper objectives include actual tariff revenue and nonlinear performance costs;
this avoids restricting the application to an affine revenue proxy. The exact
near-optimal robustness theorem also supports a bounded follower-error budget as
a leader decision, allowing robustness-versus-cost design.

All four canonical results have two independent full proof reviews. Their new
refinements were included in the final reviews. The earlier resource and
monotone-inverse dependencies received a fresh
[independent core audit](review-bilevel-reopened-existing-core.md), which found
no substantive error within their existing scope.

## Practical algorithms and experiments

The [scalar quadratic algorithm note](bilevel-reopened-quadratic-algorithm.md)
describes the implemented methods and classical antecedents.

The general scalar-leader prototype proposes active sets numerically and checks
the resulting complete response path with exact rational KKT conditions. It
preserves singleton and disconnected upper-feasible sets. The path can be reused
with different affine response constraints and tariff objectives. Large-instance
proposal failure is explicit; it does not return an uncertified answer. A
separate exponential exhaustive oracle is complete on rational inputs.

For the aligned rank-one model `Q=D+h*u*u^T`, `C=gamma*u`, the complete exact
sweep avoids numerical proposals. It supports signed loadings and either sign
of `h` under positive definiteness, and uses
`O(N log N+N(m+1))` rational operations. This is a useful implementation of
classical breakpoint/parametric-QP structure, not a new general algorithmic
principle.

The [saved general experiments](../code/bilevel_reopened/quadratic_benchmark_results.json)
contain twenty synthetic paths with up to 120 followers, twelve exhaustive
small-instance comparisons, and eighteen independently formulated KKT MILP
comparisons. The latter reported optimality and agreed in objective within
`1.22e-13`; that numerical agreement is separate from the exact path certificate.
The [tariff experiments](../code/bilevel_reopened/quadratic_tariff_benchmark_results.json)
include 10,000 followers, 15,372 thresholds, and a recorded sweep time of 1.047
seconds plus input validation. These are reproducible synthetic demonstrations,
not calibrated industrial case studies or general speed comparisons.

The dense-screening proof of concept demonstrates exact original-Hessian
recovery, including signed costs, response constraints, shifted switching
points, and degeneracy. A constructed dense 20-follower case needs 285 recovery
LPs with at most two ambiguous statuses per cell. Comparing that count to `3^N`
only illustrates enumeration reduction; it is not a comparison with a modern
solver. A separate [MILP comparison](bilevel-reopened-screening-computation.md)
records timings and numerical tolerances, including unfavorable evidence for
the current screening prototype.

The [code guide](../code/bilevel_reopened/README.md) distinguishes implemented
algorithms from diagnostics. The general real-algebraic optimization procedures
in the theorems are not implemented production solvers.

## Independent verification and corrections

| Family | Independent proof records | Distinct verification evidence |
| --- | --- | --- |
| Existing resource/inverse core | [Audit](review-bilevel-reopened-existing-core.md) | Signed quintic, inverse-modulus, critical-point, and analytic-panel exact checks. |
| Near-optimal robustness | [First](review-bilevel-reopened-near-optimal-robustness.md), [second](review-bilevel-reopened-near-optimal-robustness-second.md) | Measurement-fiber identities, nonstationary adversarial witnesses, positive-budget nonattainment, and exact Max-Cut boundary checks. |
| Dense screening | [First](review-bilevel-reopened-approximate-structure.md), [second](review-bilevel-reopened-approximate-structure-second.md) | Independently written exact full-active-set comparisons, dense indefinite residuals, singleton cells, and quantitative neighborhood checks. |
| Nonlinear aggregate | [First](review-bilevel-reopened-nonlinear-aggregate.md), [second](review-bilevel-reopened-nonlinear-aggregate-second.md) | Irrational branch boundaries, rational recovery on opposite sides, inactive negative resource slack, and vanishing curvature. |
| Response constraints | [First](review-bilevel-reopened-response-constraints.md), [second](review-bilevel-reopened-response-constraints-second.md) | 4,553 author cases and 10,091 independent exact cases, including polynomial upper functions and posterior bound signs. |
| Scalar implementation | [Review](review-bilevel-reopened-quadratic-algorithm.md) | 33 affine and 24 quadratic independently formulated dense-face comparisons, five hand objective cases, and five extreme sweep cases. |

Important corrections and improvements from review were incorporated:

- Reject floating coefficients in exact response-path certificates; otherwise
  rounded arithmetic could be mistaken for exact KKT verification.
- Distinguish a finite exact exhaustive algorithm from a numerical proposal
  loop whose input conversion can fail on enormous coefficients.
- Count screening preprocessing separately from the `M*3^t` recovery LPs.
- Certify free-coordinate gradients on cell closures by continuity, avoiding
  artificial ambiguity when a surrogate cell touches a clipping boundary.
- Keep nominal global optimality in the near-optimal theorem, while simplifying
  measurement-fiber projection to feasible KKT candidates below the budget.
- Clarify separate algebraic encodings for independently requested adversaries,
  zero-follower cases, polynomial-cost normalization, and the upper-constraint
  case where an objective-only LP shortcut would be invalid.
- Restrict the illustrative positive-budget derivative argument to its actual
  parameter interval; the unrestricted parameter wording was too broad.

The reviewers found no unresolved substantive defect in the final theorem
statements. Independent agent reviews and finite diagnostics are not journal
peer review or formal proof-assistant certification.

## Literature and publication positioning

The [open-primary-source audit](bilevel-reopened-literature-audit.md) records
sources, inspected theorem/page locations, queries, access limits, and
claim-by-claim distinctions. No matching complete theorem was found for the
structural exact near-optimal robustness, ambiguity-parameter dense recovery,
or nonlinear aggregate accuracy-bit guarantees in the sources checked.

Near-optimal robustness, rowwise adversaries, safe screening from structured
approximations, parametric QP, response margins, value-function projection,
resource-allocation inverses, and fixed-dimensional real algebraic methods all
have established precedents. They are explicitly credited. The proposed
contribution is the complete structural complexity guarantee and its verified
scope, not renaming those ingredients. Absence of a matching result in an open
search does not establish priority.

A coherent paper can build around the number of shared interactions controlling
global bilevel optimization despite many local follower decisions. The exact
quadratic, near-optimal robust, and nonlinear accuracy-bit results give distinct
guarantees; screening connects the exact model to some dense perturbations.
The tariff algorithms and exact certificates provide computational support.
The theorem documents, proof dependencies, source comparisons, review records,
and code are ready as the source material for that paper. The general screening
method's empirical advantage and industrial relevance are not established.

## Retained negative findings and stopping boundary

Strictly positive follower-error budgets do not ensure leader attainment for
nonconvex followers, even with fixed normals and a unique nominal optimum.
Arbitrary growing-rank quadratic upper criteria make adversarial optimization
NP-hard even for a diagonal quadratic follower. A strict feasible leader alone
does not imply convergence of tightened upper problems. Exact response-dependent
equalities may force irrational leaders, and small Hessian error alone need not
give useful screening. These limitations are proved or checked in the linked
canonical results rather than hidden behind algorithmic promises.

The current directions have been developed through their useful immediate
extensions: general polynomial upper data, convex aggregate coupling, explicit
safe-output conditions, robustness-budget design, quantitative dense-model
neighborhoods, and complete scalar tariff computation. General dense exact
optimization, arbitrary exact nonlinear response equalities, finding a uniformly
good surrogate, and production-scale evaluation are not unfinished premises of
these results. They require different assumptions or additional empirical work;
existing hardness and counterexamples rule out several blanket extensions.
No further theorem direction is opened as part of this closeout.

## Repository verification

Final integration checked local links across 26 Markdown documents with no
missing targets, parsed all 15 Python files in `code/bilevel_reopened/`, read
all five experiment JSON records, and found no trailing whitespace in the new
artifacts. The tracked README and scope-map changes also passed `git diff
--check`. The [machine-readable verification record](../code/bilevel_reopened/verification_summary.json)
records the counts, scope, and final canonical-document hashes. Link existence
checks do not validate Markdown anchors or external websites.

Previous unrelated working-tree edits were preserved. No files were committed,
and the validation does not attribute other concurrent changes to this work.
