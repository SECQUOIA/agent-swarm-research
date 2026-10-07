# Conditional recourse continuation

The completed result is an explicit way to remove all outside grid error
when a supplied small core leaves a tractable signed residual. It does
not solve the general bounded-treewidth conditional-message question.

Read [the main note](note.md) for assumptions, proofs, cost bounds,
literature comparisons, and implementation limits. Read the
[mixed convex/concave supplement](mixed-submodular-recourse.md) for the
broader exact oracle and its polynomial certificate construction.

The [completed recourse pipeline](../completion/recourse.md) now discovers
cores and performs original-model transformations automatically. The
[mixed submodular implementation](../completion/submodular-recourse.md)
constructs greedy-base mixtures with exact cutting planes and convex QP
queries. Its finite worst-case runtime is not the theorem's polynomial
oracle bound. The diagnostic counts below describe the first release.

| Component | Status |
| --- | --- |
| Recognize separately concave, sign-switchable quadratic residuals | Implemented by graph traversal for a supplied core |
| Exact residual min-cut values and rational flow certificates | Implemented and independently checked |
| Adaptive core cells, additive bounds, full trace verification | Implemented and tested against exact small global optima |
| Exact rational output by value separation and core face reconstruction | Implemented; explicit level limit may return an unfinished enclosure |
| Expected query count without residual dimension in its exponential factor | Proved under stated independent core noise |
| Exact finite-noise optimization with the existing base-cutoff closure/fallback | Proved corollary; that full closure/fallback is not implemented here |
| Concave polynomial unaries and certified signed core-dependent couplings | Proved oracle extension; quadratic code only |
| Coupled convex/concave submodular residual with greedy-base/KKT certificate | Proved; exact finite cutting-plane backend implemented in the second phase; no polynomial implementation bound |
| General treewidth-only improvement for arbitrary indefinite or polynomial residuals | Open |

The [reference module](mincut_recourse.py) uses only the Python standard
library and exact `Fraction` arithmetic. Supply `Quadratic`, core indices,
and box bounds. `detect_flips` either returns a valid residual switching
or rejects this sufficient class. `adaptive_core` returns an additive
enclosure and its evidence; `verify_search` checks the whole evidence
without solving optimization problems. `exact_core` adds rational exact
output, and `verify_exact` checks that output without face enumeration.
The small execution defaults are safeguards against unlimited runs, not
the theorem's full stopping-depth claim.

The commands actually run during this work were:

```text
python research-20261002-decomposition/conditional-messages/check_recourse.py --examples --output research-20261002-decomposition/conditional-messages/check-results.json
python3 -B research-20261002-decomposition/conditional-messages/check_mixed_submodular.py
python research-20261002-decomposition/conditional-messages/reviews/check_independent.py
```

The first was run by the main author, the second by the supplement author,
and the third by the independent reviewer. All passed. The exact command
spelling for reviewer checks is also recorded in the
[independent review](reviews/independent-review.md).

Author checks cover 100 residual oracle and automatic-recognition cases,
20 exact global comparisons, 105 optimizer-preserving levels, 508 cut
certificates, four exact-output cases, and adversarial certificate/domain
inputs. Eight bounded search examples reached their requested certified
accuracy, including dense mode-switching residuals with two interior
optimal core projections. The supplement covers 60 full QP comparisons,
560 conditional values, 6,720 submodularity inequalities, singular convex
blocks, integer residual cases, and a nontrivial certificate mixture.
The independent review adds coupled and nonconvex cores, exact-output
reconstruction, and coupled convex-block checks.

The review found and the implementation fixed loss of one-pass integer
index inputs, and admission of floating point flow/sign data into exact
verification. Regressions now reject those false certificates. These
checks establish the stated reference behavior and supplement the proofs;
they do not demonstrate competitive performance against established
MINLP solvers. No project-wide verification or CI inspection was run.
