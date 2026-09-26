# Independent review of CM04 and CM34

Date: 2026-09-25. Reviewer: independent review agent.

## Scope

This review covers CM04 and CM34. The three earlier reviews
(`REVIEW-ANALYSIS.md`, `REVIEW-DISCRETE.md`, and `REVIEW-INTEGRATION.md`)
name the other 47 of the 49 obligations but not these two. The review
compares the obligation text in [CLAIMS.md](CLAIMS.md), the mapping in
[COVERAGE.md](COVERAGE.md), and the manuscript claims with the Lean
statements in [Examples.lean](CertifiedMinlp/Examples.lean).

Manuscript sources:

- CM04: [Section 2](../sections/02-model.tex), equation `folding-example`
  and the following sentence in "Expressions and model identity".
- CM34: [Section 4](../sections/04-implementation.tex), the two
  counterexamples at the end of the checker discussion, and the sentence on
  adjacent branch right-hand sides.

This review does not cover the Python extractor, Pyomo, or the behavior of the
inspected external `viprchk` checkout. CLAIMS.md and COVERAGE.md exclude
these explicitly. This review did not run project-wide verification or inspect
CI.

## Method

- The reviewer read each Lean statement and proof in `Examples.lean` and
  checked it against the CLAIMS.md text and the manuscript sentence. The
  checks covered quantifiers, domains, constants, and whether each hypothesis
  can be satisfied.
- `grep` for `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by`,
  `extern`, `unsafe`, and `set_option` in `Examples.lean` and its direct
  import `ExactCorrections.lean` found no matches.
- The reviewer ran `lake env lean` once, without a build, on a scratch file
  that imports `CertifiedMinlp.Examples`. The file contains `#print axioms`
  and `#check` for the seven declarations below. Every declaration
  depends only on `propext`, `Classical.choice`, and `Quot.sound`. The
  printed types match the source statements. The `.olean` files used were
  built on 2026-09-17. `Examples.lean` has not changed since commit `875a71ab`.
- Python `fractions.Fraction` independently checked the three binary64
  values: `Fraction(0.1)`, `Fraction(0.2)`, and
  `Fraction(0.30000000000000004)`. The same check confirmed the exact sum
  `-1/2^55` and that binary64 evaluation of
  `(0.1 + 0.2) - 0.30000000000000004` gives `0.0`.

## Verdicts

| Claim | Verdict | Reasons |
|---|---|---|
| CM04 | PASS | `exact_binary_leaf_difference` proves the displayed identity for every real `x`. The coefficients are `3602879701896397/2^55`, `3602879701896397/2^54`, and `1351079888211149/2^52`. These are exactly the binary64 values of `0.1`, `0.2`, and `0.30000000000000004`, as checked independently. The result is `-(1/2^55) x^2`, matching the manuscript's `-2^-55 x^2`. `exact_binary_leaf_concave` proves concavity on all of `ℝ`. `exact_binary_leaf_not_convex` proves non-convexity on every interval `[L, U]` with `L < U`. This is stronger than the claim's "a nontrivial interval", and its hypothesis can be satisfied. The proof in `negative_quadratic_not_convex` uses a genuine midpoint violation with strictly positive `c` and `U - L`, so it is not vacuous. The Lean docstring says that treating the rationals as software-parsed values happens outside Lean. The manuscript's remark that floating-point aggregation "can instead produce zero" is outside CM04 and is not formalized; the Python check above is consistent with it. |
| CM34 | PASS | `false_million_lower_bound` takes the manuscript model `min x` subject to `x >= 1`. It proves that `x = 1` is feasible, that its objective value is below `10^6`, and that the lower-bound assertion `∀ x, 1 ≤ x → 10^6 ≤ x` is false. That assertion is exactly the Section 2 bound `β ≤ f(x)` for all `x ∈ F` with `β = 10^6`. The variable is real; the same witness would refute the bound if `x` were integer. `continuous_rounding_invalid` refutes the real implication `x ≥ 1/2 → x ≥ 1` at `x = 3/4`. `continuous_adjacent_branches_not_exhaustive` refutes `x ≤ 0 ∨ x ≥ 1` over the reals at `x = 1/2`, matching the Section 4 sentence about adjacent right-hand sides. The integral-form positive case belongs to CM24, reviewed in `REVIEW-DISCRETE.md`. The first two conjuncts of the first two theorems are closed numeral facts that record the witness; each theorem's substantive content is its third conjunct, which is proved. The historical `viprchk` acceptance is correctly left as an empirical or source-audit assertion. |

No correction to CLAIMS.md, COVERAGE.md, or the Lean sources is required for
these two obligations.
