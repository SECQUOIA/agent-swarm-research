# Publication readiness of the September 25 research batch

Completed 25 September 2026. This is the handoff for the current research
batch. It does not reassess every older project in this repository and is
not a manuscript.

The three main packages are ready for manuscript preparation on the scope
specified below. Their proofs, assumptions, source comparisons, exact
certificates, and limitations are documented. Fresh adversarial reviews
found no unresolved proof blocker. This is an assessment of the available
evidence, not a guarantee of correctness, priority, or journal acceptance.
Independent review here means review by another research agent, not external
peer review.

The supporting work is also closed at its proved scope. Some results are
classical consequences or modest examples; others preserve useful negative
findings. Publication preparation does not turn those records into separate
original contributions. Open extensions remain open and no new research
direction was started in this preparation.

## Three candidate publication packages

| Package and complete assessment | Contribution to develop | Why it matters and what is not yet established |
| --- | --- | --- |
| [Exact-penalty encoding and calibration](publication-penalty-assessment.md) | An explicit compact convex quadratic model with one binary needs a least optimized-dual penalty of `2^(2^n-1)`. General and fixed-quadratic-count upper bounds place this obstruction in context. A separate binary-box reduction proves polynomial-factor calibration hardness even when a conservative sufficient penalty is supplied. | Distinguishes finite exactness from manageable coefficient encoding and from finding a nearly smallest coefficient. It limits general penalty-based decomposition guarantees. It gives no practical penalty-selection algorithm or solver speedup. |
| [Missing quadratic cuts and their SDP formulation](publication-quadratic-assessment.md) | A rational three-variable example strictly separates two precisely identified recent relaxations. A valid parameter family contains exposed rays missed by the disjoint-support certificates; all its inequalities can be enforced with one PSD block of order five and six nonnegative auxiliaries. | Supplies a concrete selective strengthening for continuous quadratic subproblems in MINLP. Exact formulations for the entire three-variable hull already exist. The family is not claimed complete, minimal, or faster than those formulations. |
| [Quantitative limits of subset moments on indicator stars](publication-star-assessment.md) | For every `k`, rational, uniformly conditioned stars with `2k` leaves pass every specified `k`-subset compatibility test but retain additive and relative gaps of order at least `k^-2` in the original epigraph. A general transfer explains how moment incompatibility becomes an optimization gap. | Identifies a limitation of a concrete formulation design despite strong convexity and sparse structure. Prior quantum compatibility theory is an essential input. Stronger consistency schemes, arbitrary compact lifts, and optimization algorithms are outside the lower bound. |

These are candidate packages, not a recommendation to divide the work into
exactly three papers. The penalty package has the broadest complexity message;
the quadratic package has the most direct new relaxation component; the star
package is a focused formulation limitation. None currently establishes a
substantial computational improvement. Venue fit and external evaluation of
significance remain matters for manuscript development.

## Claim boundaries that must survive a manuscript rewrite

For penalties, the lower construction concerns the supremum over unrestricted
equality multipliers. Its threshold gives exact values; infeasible minimizers
can tie at the threshold. The upper bounds give the stronger conclusion of
zero-multiplier minimizer-set exactness under the stated refined slice Slater
assumptions. With input length `N` and continuous dimension `n`, the general
coefficient bit bound is `(N+1)2^{O(n)}`. With at most `k` nonlinear native
quadratic inequalities it is `N^{O(k+1)}`, allowing arbitrarily many affine
rows. The lower bound is exponential in dimension and superpolynomial in
ordinary sparse input length; a matching exponential lower bound in that
full input length is not asserted. The calibration theorem concerns proximity
to the least penalty, not difficulty of finding any sufficient penalty.

For quadratic cuts, the disjoint-support comparator includes all 27 maximal
localizing matrices without a degree cutoff. Diagonal caps are verified
separately. The Anstreicher–Puges comparison checks the specified SOC
inequalities under every required switch and permutation. The family block
strictly strengthens these systems when intersected with them; it need not
dominate either system by itself. Its six auxiliaries are sufficient, with
no minimality theorem. The supporting `K_5`-minor obstruction concerns the
joint moment hull with its specified diagonal slack, not an arbitrary
objective epigraph.

For indicator stars, subsets share only the center and singleton moment
matrices. Larger overlapping pattern marginals need not agree. The rational
theorem gives `I/39 < Q < 12I`, polynomial data encoding, bounded prescribed
means, hull height below 122, additive gap at least `1/(466560 k^2)`, and
relative gap at least `1/(56920320 k^2)`. These constants concern the pure
quadratic epigraph at the constructed original coordinates. They do not
give hardness of optimizing trees, a fixed positive gap at every order,
or a lower bound for stronger hierarchies. The center degree grows with `k`.

## Proof, source, and reproduction record

Each package assessment is a claim-to-proof map with exact assumptions,
primary-source comparisons, completed independent reviews, and commands
actually run. The [reproduction index](publication-reproduction.md) adds
dependencies, finite check counts, shared checker components, formal coverage,
and an integrity check for the retained
[source manifest](publication-sources/source-manifest.json). An independent
[final assessment](publication-final-audit.md) reviews consistency across
the packages and this handoff.

The evidence has different roles:

- Exact rational calculations certify the displayed finite counterexamples,
  matrix inequalities, and numerical constants. Symbolic calculations check
  identities. The all-order theorems still depend on the written proofs.
- New star checks independently construct parent moment matrices certifying
  actual local laws, rather than only testing the perimeter criterion. The
  two-atom realization argument supplies the laws; their possibly irrational
  atom locations are not computed by the checker. The durable integer-structure
  checker replaces previously unretained exploratory calculations as a
  reproducible supporting artifact.
- The penalty lower-bound native models and optimized dual formulas have
  targeted Lean coverage. The unchanged source matches its independently
  reviewed hash. Encoding complexity, Slater regularity, upper bounds,
  hardness, and novelty are outside that formal coverage.
- Literature audits compare assumptions and conclusions with the strongest
  located antecedents. Retained PDFs, HTML, extracted text, and hashes identify
  the inspected artifacts. An unsuccessful search is not evidence of absence.

No project-wide verification or CI inspection was performed. Numerical
discovery searches are kept separate from exact certificates. Unchanged Lean
proofs were not rebuilt solely to repeat already successful checks. The
[root record](root-research-log.md) distinguishes root checks from the other
agents' checks.

## Corrections and stronger comparisons made during preparation

The current August revision of the treewidth preprint assumes residual torso
width directly in Theorem 1. The false elimination bound is used in its
Corollary 1. The [versioned correction](treewidth-elimination-review.md) now
states that distinction; the latest main theorem is not challenged by this
counterexample. The source was checked independently by the reviewer and root.

The fixed-quadratic-count penalty comparison now includes Kamminga–Rudolph's
explicit QCQP application and its relation to the affine-face reduction.
No priority claim is based on an unavailable older proof. The quadratic
comparison includes Burer–Dong's existing complete separation method as well
as the classical exact tetrahedral lift. The star comparison now explicitly
includes established subset-compatibility terminology, related approximation
rates, global compatibility approximation, earlier star gaps for other
relaxations, and exact tree algorithms. These comparisons narrow the novelty
claims without changing the proved main results.

The Anstreicher–Puges HTML and PDF carrying the same apparent version label
have different displayed manuscript dates. Both are retained; the comparator
is tied to the checked equations, whose equivalence was audited. No source
version is silently inferred from its filename.

## Supporting material and excluded claims

The [supporting assessment](publication-supporting-assessment.md) gives the
full disposition. The common-denominator pooling reduction is classical;
its formulation is available as an attributed lemma. Signed low-rank
structure has close algorithmic and hardness antecedents. The continuous
five-variable star is a reproducible translation of a known copositive
obstruction. The treewidth correction is source-specific. The bounded-face
result for indicator stars rules out one route to a lower bound and does
not settle the full hull. These records are suitable supporting material,
not independent claims of major originality.

The unrestricted four-variable continuous-star question is unresolved.
Failure of the saved numerical searches to find a counterexample is not
evidence of exactness. Older exploratory conjectures and superseded reviews
remain in the folder as research history; the final result notes and the
assessments linked here control their current status.

## Work remaining after this handoff

No additional theorem or computational experiment is required for the
specified theoretical claims. Manuscript writing, selection of a coherent
presentation and venue, external expert review, and a source-version refresh
at submission time remain. A claim of practical solver improvement would
require implementation and comparative experiments, which are not supplied.

Symmetry completeness of the quadratic family, constructive penalty choice,
compact indicator-star lifts, matching approximation upper bounds, and
stronger consistency schemes are possible future research. They are not
missing steps in the accepted results. They were not pursued as new projects
in this publication-preparation pass.
