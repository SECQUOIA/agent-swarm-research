# Algebraic frontiers for exact convex MINLP

Date: 2026-09-28. This directory records a focused follow-up to the
September 27 exact convex-quartic work. No publication-priority claim
has been established.

The strongest supporting result found here is an explicit compilation
of exact sign logic into one arithmetic-circuit sign test. Its numerical
ingredients are classical scaled inverse-Newton sign iteration; the
precise closure formulation has received a
[deeper primary-source audit](posslp-prior-deep.md), but publication
priority remains unestablished.

| Note | What is established | Main limit |
| --- | --- | --- |
| [Boolean closure](posslp-boolean-closure-audit.md) | A polynomial-size Boolean DAG of PosSLP tests compiles into one PosSLP instance. | This removes oracle composition from the reduction format, not the arithmetic sign problem. |
| [Adaptive compilation](adaptive-integer-sign-circuit-compilation.md) | An S-gate integer arithmetic-and-threshold circuit compiles into an O(S^2)-size arithmetic sign circuit; a polynomial-size universal SLP evaluator extends this to polynomial-time adaptive PosSLP computations. | Exact integer separation and Boolean inputs are essential; arbitrary real branching inputs are outside the statement. |
| [Binary extraction](binary-extraction-known-value.md) | A unique optimal binary decision remains PosSLP-hard with a known rational optimum, rational bounded optimizer, and continuous constraint rank one; a refinement retains a full positive definite Hessian Gram. | This is a short corollary of the earlier coordinate realization, not a main independent advance. |
| [Degeneracy frontier](degeneracy-frontier.md) | Entirely zero Hessian at a convex-quartic minimizer permits rational linear algebra; partial degeneracy can have irrational kernels and discontinuous Newton maps. | The general convex-quartic PosSLP upper bound remains unresolved here. |

The [Boolean review](posslp-boolean-closure-independent-review.md) independently
reconstructs the exact range and Boolean-gate argument. An additional
independent agent checked the adaptive global error bound, denominator
clearing, and padded interpreter; its findings are recorded in the adaptive
note. The coordinating author independently derived the adaptive error
argument before reading that proof. The
[binary review](binary-extraction-review.md) distinguishes the base
construction from the full-Gram refinement it suggested; the coordinating
author independently checked that refinement's Hessian identity and Schur
complement. These are research-agent reviews, not journal peer review or
formal verification of the complete compiler. A
[fresh noncontributor review](binary-joint-gram-fresh-review.md) now also
checks the full-Gram refinement independently and reports no defect. A
[fresh cross-branch review](adaptive-closure-fresh-review.md) also checked
the entire adaptive argument. Subsequent [Lean verification](formal-coverage.md)
covers local algebraic lemmas and explicitly excludes the circuit and
complexity conclusions.

Only targeted checks were used. The adaptive checker
`python research-20260928/algebra/check_adaptive_sign_compilation.py`
passed 3,003 exact rational compressor samples, 100 error-budget instances,
and 25 refinement steps. The Boolean reviewer reports 5,882 exact rational
cases. Those finite checks support identities and edge cases; they do not
verify every input. A later
[reference DAG compiler](sign-compiler-reference-verification.md) has
separate targeted tests, including exact full-schedule examples and a
counterexample to shortened diagnostic schedules. The degeneracy note
records its separate symbolic checks. No project-wide checks or CI
inspection were performed.

The compiler theorem applies to deterministic adaptive sign computations.
No separate composed complexity theorem for the earlier FPT candidate-list
algorithm is claimed here. The Las Vegas constraint-rank algorithm does not
become deterministic merely from this closure statement. No ordinary
polynomial-time algorithm eliminating PosSLP has been obtained. This branch
is complete at the scope of its stated results; no further work is active.
