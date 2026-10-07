# Completion record

All five required deliverables and their documented extensions are complete,
including the large-model discovery repairs, matched validation, and the
reviewed 25-page report. No required work remains within this stated program.
The completion standard is the five-item [program](PROGRAM.md), fixed before
the new evaluation outcomes.

| Required work | Delivered result | Evidence |
| --- | --- | --- |
| Preserve native model structure | Direct original-variable cuts from nonnegative combinations of source row sides; identical common models and presolve; lazy discovery; a fixed bounded activation policy | [Integration contract](implementation/integration.md), [independent review](reviews/integration-review.md) |
| Broaden safe model support | Exact original-affine bound propagation, source-domain witnesses, positive-base variable powers, and exact submitted-expression checks; all seven historical importer failures admitted | [Model contract](numerics/model-contract.md), [admission records](numerics/model-admission.json), [independent review](reviews/model-review.md) |
| Complete separation contract | Implemented finite positive-tolerance separation for rational polynomial graphs on compact rational polytopes, including coordinate cones; rational cut or proved L1 distance bound; explicit bounded exhaustion | [Proof and API](theory/separation.md), [independent review](reviews/separation-review.md) |
| Support beyond pairs and stars | Exact quadratic support over bounded rational polytopes, with lower-dimensional and singular cases; fixed-dimension polynomial bit complexity and an unrestricted-dimension MaxCut hardness boundary | [Proof and implementation contract](theory/exact-support.md), [independent review](theory/polytope-review.md) |
| Prospective evaluation and integrated report | All 282 prospective jobs and 75 matched repair-validation jobs complete and independently audited; integrated 25-page report built and reviewed | [Protocol](experiments/protocol.md), [report](document/main.pdf), [claim map](document/COVERAGE.md) |

The direct-row theorem also establishes exactly what exhaustive cuts recover:
the projection of the joint graph hull with the original affine row remainders.
It does not generally recover the original feasible-set hull. The one-variable
example `x^2 = 1/4` on `[0,1]` proves that distinction. This is a limitation of
the specified relaxation, not a missing normal-search implementation.

The separation result is constructive. Complete mode has a finite exhaustive
fallback, including a feasible rational domain net for higher-degree
polynomials. Its potentially large enumeration costs are stated. The practical
SCIP callback has separate fixed work limits and never claims hull membership
because it failed to find a cut.

The integrated report retains the earlier exact constrained-star result and
the explicit `1/128` overlap obstruction, with their original evidence and
attribution. It also retains the earlier unfavorable 316-run campaign. The new
experiment does not replace or relabel that historical result.

Verification is recorded in [VERIFICATION.md](VERIFICATION.md). The combined
targeted suite passed 250 tests and eight subtests. Independent analytic checks
and component reviews supplement those tests; their overlapping counts are not
summed. The post-repair focused run passed 81 tests and three subtests. No
project-wide local checks or CI inspection were performed.

The prospective experiment solved the same 25 of 30 new holdout models in
baseline, all-cut, and automatic modes. All 123 recorded cuts passed replay;
all 271 returned incumbents passed the numerical original-model checks.
Four large-diagnostic worker failures have unknown cut logs. Those failures
and measured discovery-budget overruns motivated the matched repair validation;
neither failed records nor original runtimes are replaced by corrected runs.

The corrected cohort completed all 75 jobs without worker errors or missing
cut logs. All 42 recorded cuts passed replay and all 67 returned incumbents
passed their numerical checks. Each mode solved the same 4 of 8 affected
holdout models and 4 of 7 historical models. Discovery deadlines now stop
sequential work and explicitly discard incomplete analysis; individual
symbolic operations can still exceed a soft deadline. The selected repair
cohort is not a second prospective population sample.

Across the two separate datasets, all 165 recorded cuts and 338 returned
incumbents passed their respective checks. The four original unknown cut
logs remain outside that certification claim. The tested methods produced
no additional full solves relative to their matched native baselines.
**Keep native SCIP as the default; use the certified cut component
experimentally.**

The certificates establish recorded support inequalities, their source-model
premises, and the final exported SCIP rows. They do not certify the complete
numerical SCIP solve. Internal independent review is not external peer review
or formal verification. The report credits the classical convex-analysis,
duality, quadratic-programming, and safe-rounding ingredients and makes no
publication-priority claim.

General efficient support at unrestricted block dimension, the hull of an
arbitrary nonlinear feasible set, and an end-to-end exact MINLP solver are
different research objectives. The report explains their boundaries instead
of treating them as unfinished steps in this implementation.
