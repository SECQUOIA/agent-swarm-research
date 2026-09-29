# Closing record for the current research directions

Date: 2026-09-28. The user requested completion of the directions already
underway and no new directions. This record distinguishes independently
reviewed results from unfinished questions. Independent review here means
review by other research agents, not journal peer review. Publication
priority and practical solver improvements remain unestablished.
All directions in this closing scope are finished. Unresolved questions
below are recorded as limitations, not further work being pursued.

## Exact arithmetic with rational optimizers

The [rational-optimizer coordinate theorem](rational-optimizer-posslp-coordinate-comparison.md)
strengthens the earlier PosSLP lower bound: exact comparison of an
optimizer coordinate remains PosSLP-hard when the unique optimizer is
rational and bounded, the minimum is the known number zero, and short
rational square factors and a strict rational Hessian certificate are
supplied. The matching general upper bound makes the specified coordinate
problem PosSLP-complete. This does not prove NP-hardness or exclusion
from polynomial time, and it does not promise a rational optimizer for
the separate minimum-value perturbation construction.

The two substantive new dependencies are the
[rational quaternion sign compiler](quaternion-circuit-posslp-reduction.md)
and [quartic circuit realization](unit-quaternion-circuit-quartic-realization.md).
The compiler has two fresh independent proof reviews; the realization
has its own fresh review. The root read the full proofs and reviews and
checked the final composition. The root authored the realization, so
that composition check is not described as a fresh independent review.
Exact symbolic and rational computations challenge gate identities,
cancellation, tiny signals, shared parents, and rounding. They supplement
the all-input proofs.

The [literature comparison](quaternion-circuit-posslp-prior.md) credits
matrix-circuit simulations and Solovay--Kitaev commutator methods.
Solovay--Kitaev already uses shared computation; sharing alone is not
an additional contribution. The distinctions concern exact rational
sign encoding and its restricted convex optimization realization.

Separately, the [circle family](rational-convex-quartic-minimizer-height.md)
has bounded rational optimizers requiring exponentially many fraction
bits in the dimension. The [conditioning refinement](rational-circle-minimizer-local-conditioning.md)
preserves this obstruction with a polynomial Hessian condition number
at the optimizer. The [certificate consequence](rational-circle-optimal-gram-height.md)
forces long expanded entries in optimal moment matrices, maximal-rank
rational optimal Grams, and nonzero rational PSD matrices exposing
the optimal Gram face.
Short lower-rank Grams remain available. Existing large-output SDP
examples are credited; the claim is the restricted quartic realization.

## Integer search and exact continuous comparison

The reviewed [candidate-list theorem](fixed-integer-strong-quartic-fpt.md)
constructs a list containing every optimal integer block of a globally
strongly convex quartic with unrestricted continuous fibers and a
rational polyhedron on the integer block. Ordinary deterministic time
and total output length are \(2^{O(k\log(k+1))}L^C\), with
absolute \(C\). Exact comparisons are needed only to select the
optimal members. Nonadaptive PosSLP queries suffice for that selection.
There are at most \(2^k\) optimal integer blocks.

The [mixed-linear extension](mixed-linear-strong-quartic-candidate-list.md)
has also passed fresh proof and source reviews. With arbitrary mixed
linear constraints, it constructs a candidate list containing every
optimal integer block in ordinary deterministic \(a(k)L^C\) time.
Its approximate primal-dual cut
handles degenerate fibers without Slater or a multiplier-size bound.
Complementary slackness controls the error through the primal gradient
instead. The author and root independently rechecked the review's
zero-integer-variable dispatch and residual-QP attainment clarification.
Exact constrained-fiber selection remains separate.

The already proposed
[constraint-rank composition](mixed-quartic-integer-constraint-rank-oracle.md)
combines that list with exact continuous comparison when the continuous
constraint matrix has small rank. Its fresh reviews and final
reconciliation passed. It gives a Las Vegas PosSLP-oracle algorithm
with expected time \(F(k,\operatorname{rank}B)L^C\), absolute
\(C\), for exact optimization under \(Az+By\le c\).
It returns the lexicographically smallest optimal integer block and an
exact implicit continuous optimizer. It does not claim deterministic
optimization, short expanded algebraic coordinates, or an ordinary
algorithm eliminating the oracle.

The [monotone zero theorem](strong-monotone-cubic-posslp-upper.md)
extends exact observable comparison to strongly monotone cubic maps
that need not be gradients. The reviewed
[polyhedral variational-inequality extension](polyhedral-strong-monotone-vi-upper.md)
gives an unambiguous oracle classification, including degenerate
polyhedra. The [constraint-rank algorithm](constraint-rank-strong-monotone-oracle.md)
uses classical violator-space sampling and an exact small-subproblem
primitive. Its parameter is the rank of all constraint normals, not
the size of one final active support.

The general integer-query framework, no-bisection optimization idea,
and violator-space algorithms are established prior. Del Pia's exact
convex mixed-integer quadratic theorem is the strongest direct quadratic
comparison and allows weaker assumptions. The quartic results do not
subsume it. The potential solver capability is to separate discrete
search using moderate precision from a limited number of exact
continuous comparisons. No implemented speedup is established.

## Arithmetic costs of sparse SOS certificates

The reviewed [quartic lifting theorem](rational-block-sos-splitting-obstruction.md)
constructs a short rational SOS of a sum of two disjoint-variable
polynomials for which no rational SOS can respect those two blocks.
Real block certificates still exist. A growing family changes the
least coefficient field from the rationals for a joint certificate
to \(\mathbb Q(2^{1/5^k})\) for separated certificates.

The reviewed [strong-convexity supplement](strongly-sos-convex-block-splitting-obstruction.md)
makes both blocks strongly SOS-convex in the fixed-field construction.
After a positive perturbation, rational block certificates exist but
every pair of local rational PSD Grams has an entry needing
\(\Omega(k2^k)\) denominator bits, while a short joint rational SOS
is supplied. Every explicit separated SOS has the corresponding total
coefficient-size lower bound. This is a cost of enforcing that exact
certificate format; it is not an unrestricted SOS lower bound or a
lower bound on optimization time.

Fresh review corrected the padding lemma's input specification: its
polynomial-size output guarantee counts the supplied baseline SOS
certificate. The concrete construction already supplies it. The root
independently rechecked the correction and its application. The
[prior audit](rational-block-sos-splitting-prior.md) distinguishes this
arithmetic obstruction from known real sparse-relaxation gaps and
from coordinate projections that preserve short rational certificates.

The [quadratic-graph theorem](quadratic-graph-quartic-realization.md)
has now passed fresh proof and source reviews. From a zero-minimum
quartic with a supplied full positive definite rational Hessian Gram,
it constructs in polynomial time a rational SOS quartic whose unique
zero records the original optimizer and all its quadratic products.
It supplies a short full positive definite rational Hessian Gram,
without expanding the optimizer or its minimal polynomial. The
zero-minimum promise is assumed, not tested.

This completes the growing-field extension: both disjoint blocks can
be strongly SOS-convex while the least field for separated certificates
is still \(\mathbb Q(2^{1/5^k})\), despite a short joint rational
SOS. The individual coefficient-degree lower bound is \(5^k\) in
\(\Theta(k^2)\) total variables. The joint polynomial has a short
rational Hessian SOS certificate, but additive separation forces
every positive semidefinite Gram on its full joint Hessian basis to be
singular. The
fixed-field and positive-family theorems above do not depend on this
extension.

## Remaining limits

The [interior-Gram size bounds](interior-gram-single-exponential-upper.md)
and their [lower construction](interior-gram-bit-lower-bound.md) remain
verified: strict Hessian certification and strict positivity give a
\(\operatorname{poly}(L)2^{O(n)}\)-size interior rational Gram,
and some short inputs force exponential size in every interior Gram.
Those inputs still have short singular certificates. The stronger
unrestricted all-PSD certificate-size question remains open in this
work; the sparse result must not be substituted for it.

Novelty searches do not establish priority. Practical value still
requires algorithm design and computational assessment. Exact checks
cover specific identities and finite edge cases; the universal proofs
and imported primary theorems carry the asymptotic claims. No new Lean
formalization was used for these closing directions, and no project-wide
verification or CI inspection was performed.

Final mathematical reviews and source reconciliations passed. The
root read the closing proofs and review records, independently
rechecked substantive corrections, and recorded the exact targeted
commands and their scope in the [research log](root-research-log.md).
The final [scope audit](closing-research-scope-review.md) caught and
reconciled two missing qualifications: rational matrix output in the
height consequence and positive semidefiniteness in the separated
Hessian-Gram singularity statement. No unresolved correctness finding
remains in these closing results.
