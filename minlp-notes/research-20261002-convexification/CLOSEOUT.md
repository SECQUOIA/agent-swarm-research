# Joint-convexification continuation: completed work and decision

The [authorized development program](PROGRAM.md) is complete for the stated
supported classes. The outcome is a checked experimental solver component,
exact coupled-block support results, and a reproducible comparison. It is not
a finding that automatic joint cuts should be enabled by default.

Use the integrated [report](document/main.pdf) and
[claim-to-evidence map](document/COVERAGE.md) as the main document. The
[literature assessment](literature/README.md) distinguishes the contribution
from established simultaneous convexification, Bernstein bounds, quadratic
hulls, forest-box optimization, and measure-consistency results.

## What was finished

| Development need | Completed result | Evidence |
| --- | --- | --- |
| Rigorous cuts after numerical direction selection | Exact binary64 coefficient interpretation, outward right-hand-side rounding, complete-domain Bernstein/Arb bounds, typed model binding, and replay | [Numerical contract](numerics/contract.md), kernel and independent analytic tests |
| Selective automatic integration | Source-based discovery, matched reformulation, cached proposals, certified polynomial screening, bounded exact-support exchange, root-global SCIP rows, and actual row auditing | [Integration](implementation/integration.md), [independent review](reviews/integration-review.md) |
| Coupled two-variable blocks | Exact rational quadratic support on a bounded rational polygon, including degenerate and empty domains | [Theory](theory/README.md), exact oracle and tests |
| A larger useful structured extension | Exact support for constrained quadratic stars with arbitrary center–leaf affine rows; sharp gain from merging specified pair directions | Full proof, implemented oracle, independent KKT and whole-interval audits |
| Limits of overlapping hulls | Explicit exact-pair-hull obstruction with joint minimum `1/128`; full-marginal gluing conditions and positive special cases | [Overlap analysis](theory/overlap-review.md), [exact mechanism artifact](experiments/star-mechanism.json) |
| Implementation-cost investigation | Automatic work selection, a combined reuse-policy ablation, and an optional C sampling kernel with measured crossover limits | Retained solver comparisons and [native-kernel benchmark](implementation/native-kernel.md) |
| Credible comparative evidence | Frozen selection, baseline/control/all/auto comparisons, root runs, ablations, seed repeats, raw inputs and sources, original-model residual checks, and fresh-process replay | [Experiment records](experiments/campaign-v1/results.md), [verification](VERIFICATION.md) |

The importer now refuses source expressions whose domains cannot be proved
throughout their declared boxes, whole rows changed by binary64 assembly, and
invalid or unrepresentable sides. Rewritten rows are checked after substituting
the exact auxiliary features. This conservative contract was necessary:
review found actual model changes caused by coefficient cancellation and by
domains lost from cancelled logarithms or square roots. The correction narrows
applicability; it is not a complete nonlinear-model compiler.

## Computational outcome

The campaign completed all **316 scheduled runs** in **443.6 seconds**, with
no hard process timeouts or omitted jobs. Full runs used a six-second soft
integration budget; root runs used two seconds and one node. Other jobs shared
the host, so small timing differences are descriptive.

For the deterministically selected 24-model application sample:

| Mode | Numerically solved / selected | Submitted to SCIP | Recorded new cuts | Summed recorded integration seconds |
| --- | ---: | ---: | ---: | ---: |
| Baseline | 19/24 | 20 | 0 | 17.40 |
| Reformulation control | 19/24 | 20 | 0 | 20.66 |
| All eligible blocks | 18/24 | 20 | 230 | 25.41 |
| Automatic selection | 18/24 | 20 | 106 | 23.01 |

Three models failed the common source-domain admission check; one used
unsupported variable exponents. These are importer limitations, not native
SCIP failures. The latter generated eight retained construction-error records
across full/root runs and four modes. Those records have no saved model/cut
log; their cut counts are recorded as unknown, even though the retained
trace identifies the failure before optimization.

Automatic selection reduced application-sample direction LPs from 1,073 to
323 and callback time from 5.59 to 3.05 seconds relative to unconditional
activation. This did not recover the baseline solve count. On the 13 synthetic
cases, control and both cut modes solved all 13, versus 12 for baseline;
the reformulation control therefore prevents attributing that gain to cuts.
The star case also failed to establish a runtime benefit: native SCIP already
handled it well, and automatic star merging added cost. The exact pair-hull
obstruction remains a mathematical result, separate from this solver outcome.

All **1,082 recorded added cuts** passed original-model-bound replay, including
their actual stored SCIP rows. All **270 returned incumbents** passed the
independent numerical residual checks at the specified tolerance; there were
no reference-bound conflicts. Replay rejected all 12 tamper controls and
verified 101 frozen source/input hashes. These results certify the recorded
cut inequalities within the documented trust base. They do not certify SCIP's
presolve, numerical feasibility decisions, node bounds, or final optimality.

## Decision and remaining research boundaries

Keep native SCIP as the default and the new separator experimental. The
reusable support oracles and cut-checking interface are concrete deliverables;
the campaign does not establish a generally beneficial activation policy.
The optional native kernel speeds selected repeated sampling workloads, but
it was not loaded by the main solver workers and does not justify a claim
about full-solve acceleration. A full native SCIP handler was not built;
the current evidence does not justify treating that port as the missing
routine step to a proven performance improvement.

The supported program is finished. Wider overlapping nonlinear hulls,
multivariate elementary functions, arbitrary nonlinear block domains,
complete normal separation, permissive domain-preserving model compilation,
and end-to-end solver certification remain outside its results. They require
new mathematics or substantial solver engineering. A broad performance claim
would also require a new, longer, independently selected experiment after
an algorithm change; retuning on this completed sample would not provide it.

Internal research-agent reviews, precise source attribution, retained
negative outcomes, and the final claim map make these boundaries explicit.
No project-wide checks, CI inspection, commit, pull request, or publication
was part of this continuation.
