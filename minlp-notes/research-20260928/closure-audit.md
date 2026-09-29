# Final closure audit of the September 28 research

Date: 2026-09-28. This audit covers `research-20260928/` and
`formal/topics/32-integer-sign-core/` after the user requested completion
of current ideas and no new ideas. The
[closing record](closing-research-results.md) is consistent with the
saved theorem statements, review boundaries, and source qualifications.
No remaining proof or review task is identified within the stated scope.
This is not a certificate of publication priority or an independent
verification of every mathematical proof.

## Closing synthesis

The synthesis correctly distinguishes ordinary quadratic modules from
full preorderings, total-degree from fixed-private-degree hierarchies,
and local geometric assumptions from global feasible repair. Its rates
refer to the specified relaxations. It does not claim a general MINLP
running-time improvement, practical numerical conditioning, or efficient
global projection.

Two precision corrections were identified and incorporated. The
order-one quadratic example uses a truncated moment witness represented
by an atom outside the box; only its order-two witness is a feasible
local measure. The rational-certificate consequence explicitly requires
rational input data. Neither correction changes the corresponding
proved theorem.

The main novelty assessment remains qualified. The kernel notes now
credit the July 2025 and February 2026 author slides that already assert
the inverse-square sparse preordering rate. Both early proof reviews
identify this later discovery. The ordinary-module, recourse, and
constrained results have their own comparisons; they do not inherit a
novelty claim from the printed paper's weaker exponent. The discrepancy
between the slides and printed theorem is recorded without inventing a
resolution.

The index and final root-log entry close the current scope. Earlier log
entries are explicitly historical. Open questions in the notes are
excluded from the completed claims, rather than assumed in their proofs
or retained as active assignments. The abstract product-domain screening
produced no saved theorem and is correctly closed without claiming one.

## Verification and source records

The following documentation or review gaps were identified during the
initial audit and are now closed.

- The [ordinary Putinar note](solver/sparse-putinar-kernel.md) links its
  completed proof and prior reviews. The
  [exact-consistency strengthening](solver/sparse-putinar-exact-consistency.md)
  links its [fresh final audit](solver/signed-kernel-final-audit.md).
- The [private-block prior audit](solver/partial-kernel-prior.md) uses
  the corrected matrix-Jensen reference and links the completed fresh
  review. The [affine-recourse upper note](solver/affine-recourse-kernel-upper.md)
  links its dedicated prior audit and verification record.
- The binary full joint Hessian-Gram refinement now has a
  [fresh noncontributor review](algebra/binary-joint-gram-fresh-review.md).
  Its original reviewer proposed the refinement; the new reviewer
  independently reconstructed it and ran separate exact checks. The
  main note and original review now identify both review scopes.
- The [regular-recourse note](solver/active-region-rates.md) links a
  [fresh proof review](solver/active-region-fresh-review.md) and
  [verification record](solver/active-region-verification.md). These
  cover both stated regularity conditions, the frequency-degree repair,
  and the sharp example. Arbitrary multivariate Lipschitz projections
  remain outside the theorem.
- The [general-constraints note](solver/general-constraints-kernel.md)
  links its [fresh review](solver/general-constraints-fresh-review.md)
  and records both exact checker commands and their coverage. The
  sharpened ordinary rate, required degree reserve, global error bound,
  and primal-only conclusion agree with the review.
- The [curvature literature audit](solver/branching-curvature-prior.md)
  is complete and linked from both existing theorem notes. It qualifies
  priority, distinguishes convex-cover complexity from solver time,
  and adds no theorem beyond the previously reviewed scope.
- The [structural overview](structural/README.md) accurately records the
  supporting repair theorem and its separate proof and source reviews.

The [Lean package](../formal/topics/32-integer-sign-core/README.md)
accurately limits its scope to local lemmas and a 53-declaration axiom
audit. Its [coverage record](algebra/formal-coverage.md) excludes the
complete compiler, interpreter, global error induction, and complexity
theorem. Numerical hierarchy comparisons likewise preserve their solver
residuals and finite-grid limitations. The closure audit did not rerun
those mathematical scripts, numerical experiments, or Lean checks.

## Separate review of the small source-audit example

One final status search found a subsidiary example still marked as needing
independent review in the
[submodular source audit](submodular/near-stieltjes-literature-audit.md).
Its three-variable matrix is distinct from the four-variable examples
covered by the existing obstruction review. The closure auditor
`/root/close_scope_audit`, who did not author this example, checked its
written argument separately by hand.

The matrix has diagonal entries three and off-diagonal entries
`Q_12=1`, `Q_13=-1`, `Q_23=-1/10`, with `b=(3,2,0)`.
The leading minors are `3`, `8`, and `2117/100`, proving positive
definiteness. For each of its four displayed supports, the stated
minimizer is nonnegative and satisfies `Q_A x_A=b_A`; positive
definiteness therefore makes it the global minimum on that support.
The objective value is `-b_A^T x_A`, giving exactly
`-3`, `-27/8`, `-27/8`, and `-107/29`. Their submodularity defect is
`-7/116`. The positive edge and two negative edges give the stated
sign-switching obstruction. The Schur-complement coefficient is
`-1/10+1/3=7/30`.

No mathematical error was found. This review establishes the finite
counterexample and its stated failure of indicator-only branching to
restore submodularity. It does not establish hardness, solve the broader
one-positive-edge problem, or determine novelty. No computational rerun
was used or needed for this small independent check.
This was the only new mathematical hand check in the closure audit;
the rest of the final pass compared documentation and review scopes.

## Documentation checks actually performed

The initial inline Python path audit read 76 Markdown files in the two
authorized directories and checked 272 local path references found by an
inline-link regular expression. Its two nonexistent-path reports were
false positives inside displayed LaTeX, not Markdown links. Three links
contained anchors. Manual inspection matched them to the actual section
headings: the explicit kernel, private quadratic-bound obstruction, and
sparse certificate consequence. Renderer-specific anchor generation was
not tested.

A second inline Python scan constructed the Markdown-link graph rooted
at the continuation index. It identified several completed but
undiscoverable results and reviews. The final index and closing record
now make every Markdown file in the continuation reachable, including
the curvature results, exact finite-order gaps, multiplier obstruction,
and final proof reviews. A later targeted scan was justified by these
new files and links; no actual broken local file path was found.

Targeted `rg` searches checked pending-review, active-work, and source
comparison wording. Each substantive hit was inspected in context.
Historical log entries and explicitly excluded future questions are
not current proof obligations. External URL availability was not
rechecked, and the path scanner is not a full CommonMark parser.

The first audit version was checked with
`git diff --no-index --check /dev/null research-20260928/closure-audit.md`.
It produced no whitespace diagnostics; exit status 1 was the expected
no-index difference status against `/dev/null`. The final rewrite received
a targeted local path and formatting check. No project-wide verification,
CI inspection, new research direction, or unrelated-directory audit was
performed.
