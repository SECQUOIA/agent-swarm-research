# Claim and evidence map

The scope of a result includes its assumptions. An implementation of its
arithmetic checks does not establish missing assumptions about a native solver.

| Claim | Mathematical basis | Implementation and evidence | Limit |
|---|---|---|---|
| A feasible relaxation witness bounds one direction's improvement in the current frozen round. | `certificates.tex`, current-round proposition | `../theory/certificates.py`, `current_round_ceilings` | Does not bound rebuilt future relaxations. |
| A finite witness pool can protect an inner box in every later round. | `certificates.tex`, finite protection theorem | `verify_protected_box` with exact rational row checks | Same monotone relaxation family, containing domains, adequate cutoffs; additional cuts and integer rounding need separate validity arguments. |
| Witnesses can survive a tighter cutoff by convex mixing. | `certificates.tex`, cutoff adaptation | `mix_for_cutoff` | Current convex relaxation only; the hull must be checked again for future-round protection. |
| All coordinate supports of a cached convex witness pool after a cutoff change can be obtained without a new LP. | `certificates.tex`, cutoff-frontier proposition | `cutoff_frontier`, exact pair-mixture checks | Optimizes over the cached hull, not the full relaxation; all points must be rechecked on a changed domain. |
| A protected witness bounds the objective improvement of that relaxation. | `certificates.tex`, objective ceiling | `ProtectedBox.objective_ceiling` | No original-model incumbent or bound on stronger native relaxations. |
| A residual plus a uniform matrix bound can bound all future endpoint motion. | `certificates.tex`, remaining-motion theorem | `check_tail_majorant` checks the rational supersolution inequality | The implementation does not infer or certify the uniform matrix bound for arbitrary models. |
| An exact OBBT round can be committed and then stopped using a protected-box certificate. | `implementation.tex`, certified stopping workflow; LP weak duality and protected-box theorem | `../theory/certified_driver.py`; `remaining-benefit-driver-checks.json` | Rational primal/dual reconstruction may fail. Failed incomplete rounds are discarded; budget exhaustion is `unfinished`, not `fixed`. |
| Stored LP dual vectors remain valid through active-set changes. | `constraints.tex`, dual-envelope proposition (C1) | `../theory/check_constrained_obbt.py` | Fixed matrix and affine right-hand side; a cutoff multiplier gives a guaranteed reduction, not an upper limit on possible reduction. |
| Exact basis regions certify support values and cutoff intervals. | `constraints.tex`, basis-region proposition (C2) | Exact basis and interval checks | A checked region is not proof of complete coverage. Rebuilt McCormick coefficients usually violate the fixed-matrix premise. |
| Retained support witnesses bound one-round retriggering benefit. | `constraints.tex`, primal/dual bracket (C3) | Exact cutoff support examples | Witness exclusion does not prove tightening will occur. Changed rows need rechecking. |
| A complete basis-region cover supplies a uniform comparison matrix. | `constraints.tex`, comparison-matrix proposition (C4) | Exact changing-cell example on an invariant interval | Invariance and a finite residual majorant remain separate premises. |
| Nonlinear constraints can yield a uniform contraction estimate through feasible repair. | `constraints.tex`, feasible-repair theorem (C5) and explicit graph example | Analytic proof plus exact constants and identities checked by `check_constrained_obbt.py` | Requires uniform residual, repair, objective-error and growth bounds; not an automatic recognizer for general MINLP. The graph example uses exact convex square epigraphs. |
| A cost ledger bounds optional work on the enhanced trajectory. | `allocation.tex`, ledger proposition | `../theory/check_effort_allocation.py` | This is not a runtime guarantee against an independent baseline. |
| Independent scheduling or serial rescue protects a baseline in an ideal work model. | `allocation.tex`, protected-baseline proposition | Exact finite trace checks in `check_effort_allocation.py` | No deployed portfolio or shared-machine wall-clock guarantee. |
| The numerical sidecar supplies conservative local coordinate bounds for its declared relaxation and cutoff. | `implementation.tex`, dual-residual and outward row-rounding formulas | `../solver/adaptive_obbt.py`, author and independent targeted tests | Validity is conditional on the cutoff. A numerically accepted incumbent is not an exact feasibility certificate, and native SCIP is not independently replayed. |
| The measured adaptive policy combines ordering, current-round screening, pilot stopping, and limited reconsideration during search. | `implementation.tex`, frozen policy; `evidence.tex`, prospective protocol and outcomes | `../experiments/runs/campaign-01`, immutable source snapshot and raw records | Protected-box and matrix-tail APIs do not control this policy. Short selected cohort, two seeds, native OBBT enabled in all arms. |

The empirical comparison and constrained-theory evidence are described in the
corresponding report sections. Proofs, arithmetic checks, numerical regression
tests, and solver experiments provide different kinds of confidence. Internal
review is neither formal verification nor external peer review. No CI results
are represented as local verification.
