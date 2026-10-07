# Research record

## 2026-10-03: scope and baseline

The user authorized completing topic 2 and its promising extensions. The
completion contract is in [PROGRAM.md](PROGRAM.md). The working tree already
contained unrelated manuscript work and active experiment logs; their status
was saved in [baseline-status.txt](baseline-status.txt). No unrelated work was
changed or stopped.

Parallel workstreams investigate the primary literature, global-convex point
output, residual-convex cubic completion, constrained exact comparison, and
independent audits of the two historical theorem families. A separate narrow
implementation workstream develops exact-rational output-contract examples.

Initial source reconciliation confirms that the September 27 unconstrained
exact upper bound already cites *Hesse's Redemption*. The October 2 focused
point-output audit needs an explicit comparison. The distinction is between
the prior value-gap guarantee and the proposed effective point-distance and
fixed-selector guarantees; different stated outputs alone do not establish
novelty.

The initial independent point-core reconstruction found no correctness
blocker. It checked the global Bregman extrapolation, rational optimizer
slice, Hoffman estimate, original-coordinate minimum-norm selector, and cubic
polytope reduction. These findings will be recorded in the final review files;
they are not external peer review.

New extensions are in development. No draft claim is accepted solely because
an author or an earlier review labels it complete. The final result map will
identify each reviewed theorem and each remaining general question.

## Completed mathematics and independent reviews

The global point work now covers sparse explicit polynomials, numerical
degree dependence, and arbitrary rational polyhedra. The proof constructs a
rational radius and a global error bound without circularly assuming
attainment. Sparse gradient coefficient rows avoid an exponential sampling
grid; affine substitutions remain evaluation circuits rather than dense
expanded polynomials. Two independent reconstructions passed.

The residual-convex cubic work now removes the joint core convexifier on
product boxes. The proof combines neighboring-tilt endpoint certificates,
an LLL certificate for quadratic minor margins, a contact-gradient volume
bound, and a finite-grid transfer. One base event pays for exact fallback;
the law, selected optimizer, and random work factor work for every requested
precision. Separate reviews reconstructed the lattice and probability
arguments and the integrated theorem. No cubic-box proof gap remains in the
stated result.

The constrained comparison investigation produced ordinary deterministic
FPT in nonlinear dimension over arbitrary polyhedra, and `P^PosSLP`
extensions for structured boxes and separable polynomial flows. The
constrained Newton recurrence is prior work and does not require identifying
the optimal face first. The unrestricted case still needs a verified exact
QP interface for circuit Hessians or a different argument; smooth penalties
and a generic barrier accuracy bound do not establish it. This question is
recorded as open, not relabeled complete.

The exact-core audit found no substantive defect in the historical
quartic reductions or witness-size results. Two additional reviewed
consequences were developed: a unary-degree exact upper reduction and
polynomial-size rational-circuit interior Grams. The latter construction
needs no sign oracle but makes no inexpensive-validation claim. The
historical bivariate irrational zero example answers the version-specific
rational-witness question identified in *Hesse's Redemption* v1.

The reference implementation has ten passing focused tests and a separate
review. A discovered constant-objective row bug was fixed. The checker
validates supplied witnesses for a certified convex subclass; it does not
claim to implement the theoretical solvers. Its incomplete tangent bounds
for additional constraints are documented and tested.

## Integration and source reconciliation

The integrated report contains the output contracts, global point proof,
domain-convex degree boundary, exact arithmetic, constrained extensions,
cubic recourse, and certificate representations. Existing theorem families
and new extensions are identified separately. Section-level integration
reviews preserve the exact hypotheses and complexity models. Minor
notation and exposition corrections were incorporated.

The source audit credits prior value/radius theorems, error-bound theory,
essential-variable extraction, Newton convergence, and the specialized QP
algorithms. The inspected external manuscript is Hesse v1. The full Yang
primary text and Hesse proceedings version were unavailable; no priority
claim is made. A scoped ignore exception preserves the authored literature
audit, since the repository otherwise ignores directories named literature.

Extension discovery is closed for this program. No unrelated research or
running experiment was changed, and no public submission or commit was made.

## Final closeout

The integrated `latexmk` build passed and produced `document/main.pdf`,
29 pages. Its final log has no warnings, unresolved references/citations,
or overfull/underfull boxes. The first build caught one math-mode typo,
which was corrected. A rendered first-page inspection confirmed readable
title, abstract, and contents layout.

The final scoped document command passed 53 authored documents, 263 local
link targets, 55 LaTeX labels, and 12 cited bibliography keys. The complete
bibliography contains 22 validated entries. The scoped `git diff --check`
also passed. [VERIFICATION.md](VERIFICATION.md) records commands and outcomes
from all workstreams, including the ten passing implementation tests and
the exact mathematical diagnostics. Passing checks were not rerun merely
to duplicate their records.

All new claims in the result map have completed proofs and internal
independent reviews. The main remaining mathematical question is the
unrestricted polyhedral exact-comparison classification; the cubic
coupled-domain/degree-four and succinct-input boundaries are also explicit.
The full topic is therefore not declared mathematically exhausted. The
deliverable contains the completed positive results and a precise account
of these unresolved questions. Source-access limits and unestablished
publication priority remain visible.
