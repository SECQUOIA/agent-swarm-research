# Bilevel research continuation

Date: 2026-09-07 (UTC). Status: completed development and independent verification.
The [closeout](bilevel-reopened-closeout.md) is the final result and paper-readiness
record for this continuation.

The user reopened the bilevel topic to obtain impactful, practically important,
paper-ready results. This continuation supersedes the earlier closed status only
for bilevel work. Existing unrelated manuscript and potential-flow changes are
outside this continuation and are being preserved.

## Work and ownership

| Direction | Current purpose | Record |
| --- | --- | --- |
| Quadratic algorithms | Exact scalar-leader response-path certificates, affine upper constraints, meaningful computational comparison | `bilevel-reopened-quadratic-algorithm.md` |
| Approximate structure | Use a low-rank surrogate to certify true variable statuses, and solve dense follower models with few uncertain statuses | `bilevel-reopened-approximate-structure.md` |
| Response constraints | Accuracy-bit approximation with explicit upper feasibility guarantees and honest margin assumptions | `bilevel-reopened-response-constraints.md` |
| Nonlinear aggregates | Extend polynomial-cost accuracy-bit algorithms to fixed-dimensional convex aggregate coupling | `bilevel-reopened-nonlinear-aggregate.md` |
| Near-optimal followers | Exact structural algorithms protecting the leader against every sufficiently good follower response | `bilevel-reopened-near-optimal-robustness.md` |
| Literature | Claim-by-claim comparison with open primary sources; distinguish known mechanisms from combined guarantees | `bilevel-reopened-literature-audit.md` |
| Existing core | Fresh independent proof audit of the accuracy-bit and inverse-approximation dependencies | `review-bilevel-reopened-existing-core.md` |

All directions in this table are complete within their stated scope. The four
new theorem documents have been promoted into `results/`, with the continuation
notes retained as redirects. Each theorem has two independent full proof audits.
The scalar implementation has an independent mathematical and code audit, and
the [dense screening comparison](bilevel-reopened-screening-computation.md)
records both exact certificate agreement and the numerical MILP's faster runtime
on the tested synthetic family. No unfinished proof or review task remains.

## Completion standard

The final statements, proofs and dependencies, scope, counterexamples, source
comparisons, computational evidence, and review dispositions are recorded in the
canonical results and closeout. Reviews produced incorporated corrections and
useful refinements. Publication priority remains qualified; generic mechanisms
and classical implementation techniques are attributed. No new direction is
active in this continuation.
