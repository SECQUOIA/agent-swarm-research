# Completion assessment

The follow-up research program is developed into a report with proofs, checked
reference implementations, an integrated SCIP policy, a prospective comparison,
and independent reviews. Its central mathematical result is a finite way to
certify limits on future tightening for a specified relaxation family. Its
computational result supports retaining native SCIP as the default on the
tested cohort.

This is a completed study, not evidence that the entire subject is exhausted.
The remaining questions below need additional structural assumptions or new
performance evidence. Labeling those questions solved would overstate the work.

## What each recommended workstream produced

| Workstream | Developed result | Scope |
|---|---|---|
| Decide whether to start or continue | Feasible witnesses give current-round improvement ceilings; the solver rechecks cached witnesses and uses a short pilot. | A supplied witness may screen before a directional LP. The first solver callback has no cached LP witnesses and can still pay for its pilot. No universal free predictor of worthwhile OBBT is claimed. |
| Selective tightening in the search tree | A working local propagator with node-scoped triggers, incumbent reconsideration, bounded LP work, and validated bound proposals. | Tested against native SCIP and fixed-order additional OBBT. Numerical incumbent feasibility remains part of the cutoff contract. |
| Certified remaining benefit | Protected boxes, objective ceilings, cutoff frontiers, conditional matrix residual bounds, and a rational primal/dual driver. | Same monotone relaxation family and verified reuse premises. The measured SCIP policy does not deploy the all-future certificate machinery. |
| Coupled and nonlinear constraints | Verified parametric LP regions, uniform sensitivity under explicit coverage, and a feasible-repair contraction theorem with an explicit nonlinear example. | Changing McCormick coefficients need separate control. Repair, residual, and growth constants are substantive premises. |
| Allocation among solver actions | Correct cost accounting, independent-baseline scheduling bounds, counterexamples, and a common validity/cost contract. | These do not predict which action saves the most search time. Current component evidence does not justify a larger deployed controller. |

The [report](document/main.pdf) brings the results together. The
[claim map](document/COVERAGE.md) and [verification record](VERIFICATION.md)
identify which claims are proved, checked arithmetically, implemented, or tested
empirically. The [literature ledger](literature/source-ledger.md) attributes
classical ingredients and avoids an unsubstantiated publication-priority claim.

## What the experiment establishes

The frozen comparison contains 120 runs: twenty models, two seeds, and three
policies. Each arm solved the same 14 of 40 model–seed cases, including 2 of 24
public cases and 12 of 16 synthetic cases. There were no process failures or
invalid returned incumbents; each arm had one run without an incumbent.

| Policy | Solved | Mean penalized process time (PAR-2) | Additional directional LPs |
|---|---:|---:|---:|
| Native SCIP | 14/40 | 13.855 s | 0 |
| Fixed-order additional OBBT | 14/40 | 13.988 s | 2,172 |
| Adaptive additional OBBT | 14/40 | 13.997 s | 1,719 |

Adaptive selection reduced auxiliary LP calls by 20.9% relative to the fixed
policy, but it produced no additional solves or demonstrated overall speedup.
Its total sidecar time actually rose from 19.530 to 23.123 seconds as it made
more callbacks and performed screening. Fewer LP solves therefore did not mean
less total enhancement work.
Only two directions were screened by cached feasible witnesses in the adaptive
arm. The combined policy comparison does not isolate each feature's effect or
demonstrate practical savings from the stronger future-round certificates.
Both additional policies improved the public cohort's mean final-gap score;
the adaptive improvement was concentrated in the two seeds of `bayes2_50`.
Against native SCIP, adaptive OBBT won four and lost twelve of the 39 comparable
final-gap pairs. The mean improvement did not translate into a solve-count
advantage within the budget.
Small timing differences on this shared machine do not support a claim of a
reliable slowdown either. The defensible recommendation is to keep native SCIP
as the default and treat the added policy as an experimental implementation.

This is a small selected cohort with ten-second budgets, not a comprehensive
solver benchmark. The [experiment report](experiments/RESULTS.md) preserves all
outcomes, uncapped elapsed costs, exclusions from gap comparisons, and the
separate pilot. Nothing was tuned on these holdout outcomes. Negative or
inconclusive outcomes are part of the result.

## Remaining research questions

Three extensions remain scientifically meaningful, but they are not established
by this study:

1. Obtain future-round certificates cheaply from information already produced
   by native search, with a measured net saving. The exact checker and automatic
   proposal fixtures establish validity, not this cost advantage.
2. Automatically verify useful uniform sensitivity or feasible-repair constants
   for broad nonlinear model classes. The conditional theorems and worked
   examples explain what must be verified; they are not a general discovery
   algorithm.
3. Connect bounds on coordinate movement or relaxation quality to expected
   search time well enough to choose among OBBT, cuts, branching, and other
   actions. Neither past progress nor a work budget supplies that connection.

These are new research tasks, not missing proof steps in the stated results.
The present evidence gives no reason to add a more complex controller merely
to enlarge the implementation. A broader or longer campaign would need a
specific new hypothesis, such as a supported model class or lower-overhead
certificate reuse. The appropriate completion claim is therefore that the
recommended follow-up has been developed and tested within its stated scope;
adaptive solver effort allocation as a whole remains open.
