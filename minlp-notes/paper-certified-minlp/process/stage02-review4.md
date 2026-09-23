# Stage 2 independent review 4

Reviewed 2026-09-13. Scope: Sections 3–4, their integration with Sections 1–2, the Stage 2 author report and analytic validation record, and a bounded adversarial inspection of the executable checking boundary. No manuscript or checker source was edited.

## Verdict

**No major issue or required minor correction found in Stage 2.** The mathematical statements are conditional in the right places, their proofs are sound under the stated assumptions, and the inspected implementation agrees with the described acceptance conditions. This is a bounded review, not a formal correctness proof of the Python implementation.

## Mathematical checks

- The box correction has the correct signs on both half-lines, and its finite-interval upper enclosure uses the upper residual endpoint with `z-L` and the lower residual endpoint with `z-U`. The free-coordinate condition correctly requires exact residual zero. The worked quadratic example's residual, safe intercept, and positive square-completion remainder agree algebraically.
- Propagation preserves mixed-integer feasible points even when integer rounding removes continuously feasible points. Requiring cuts on the entire resulting box is stronger than required for transfer and is logically compatible with this propagation.
- The discrete invariant is stated on the incumbent sublevel set `S`. It does not falsely assert that a solution-cutoff row holds throughout the master. The supplied best feasible witness belongs to `S`, which supplies exactly the inequality needed to lift a derived lower bound to points outside `S`. Neither this proof nor nonlinear transfer assumes an attained master or nonlinear optimum.
- Unsplit disjunctions are exhaustive for the checked integral linear form. The displayed assumption-set formula retains cross-branch and unrelated dependencies. The proof works even if a branch conclusion did not depend on its named branch assumption; it does not rely on an unjustified assumption-discharge convention.
- The quadratic Schur-complement test, homogenized-norm recognition, monomial Hessian congruence and Schur-complement calculation, and one-variable fractional second derivative are correct. Their sufficient-domain restrictions match the intended scope. Boundary extension of convexity is separated from existence of usable derivatives.
- The derivative-along-segments bridge is materially important and correctly stated. The text acknowledges that arbitrary finite coordinate one-sided derivatives are insufficient and does not mistake interval finiteness for proof of that bridge. Symbolic differentiation and supported boundary chain rules remain within the explicitly trusted implementation, rather than an advertised mechanized theorem.
- The objective-preserving extension handles affine constants, objective-sense normalization, and a free epigraph coordinate. Primal completion requires original feasibility and a rigorous objective bound; it does not promote master incumbents to nonlinear witnesses.

## Executable boundary inspected

I inspected `vipr.py` end to end through parsing, solution validation, reference/lifetime scanning, rule evaluation, proving-derivation selection, and external-verdict corroboration. In particular:

- Original rows check every supplied solution, including implicit zero coordinates and integrality. A finite primal range endpoint requires an adequate feasible witness.
- The solution inference requires that witness and checks ordinary cutoff domination. It does not silently apply an integer objective decrement.
- Rational linear combination signs, integral rounding coefficients and variables, exact domination, actual assumption-row identities, split adjacency, and dependency propagation agree with Proposition 3. The support for contradictory constant rows is logically valid.
- The first pass checks every reference, including zero-multiplier references. The second pass retains referenced rows until the computed last use. Zero multipliers omit semantic assumptions but do not bypass reference validity.
- Earlier proving derivations do not bypass suffix validation. Repeated or forged `global` metadata cannot erase dependencies. The common problem parser is used for master matching and full proof replay.
- The master comparison checks objective sense and exact coefficients, integrality, variable bijection, and a positively normalized multiset of all expected rows and bounds. The manuscript correctly avoids claiming arbitrary algebraic or negative-scaling equivalence. Stable-file assumptions are now explicit, so separate reads do not carry an unstated adversarial integrity guarantee.

I also inspected exact expression reconstruction, `_verify_given_cut`, safe interval conversion/enclosure, domain checks, scalar curvature rules, quadratic elimination, monomial decomposition/recognition, and the linear-fractional recognizer. I found no accepted class whose curvature was demonstrably misclassified in this bounded review. The exact representation import used by the quadratic helpers is indeed `exact_repn`, despite the legacy local alias `generate_standard_repn`; those helpers do not revert to Pyomo floating coefficient aggregation.

## Independent test execution

Executed the focused adversarial suites in the existing solver-lab environment:

```text
.venv/bin/python -m pytest -q \
  certify/tests/test_vipr_independent_review.py \
  certify/tests/test_independent_semantics.py \
  certify/tests/test_review_convexity.py -p no:cacheprovider
58 passed in 0.68s
```

The inspected cases include cross-branch dependencies, invalid continuous splits, omitted slopes on half-lines/free coordinates, singular norm support, nonlinear composition signs, fixed-variable behavior, and quadratic zero pivots. These checks provide distinct empirical confidence; I did not treat the existing 152-test author run as a guarantee of soundness and did not repeat the large historical replay.

## Continuity requirements, already acknowledged by this draft

Later sections must keep the restricted API and trusted symbolic/interval/kernel boundary visible. Focused Lean results must not be described as verifying all these executable components. Replaying historical artifacts after changes to trusted checker code would require new source identifiers and appropriately regenerated evidence. No such source change was identified as necessary by this review. Missing later-stage experiments and formalization are not Stage 2 defects.
