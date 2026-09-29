# Final audit of the September 25 publication preparation

Date: 2026-09-25. Scope: a fresh cross-package review of the completed
September 25 research batch. This is an independent research-agent audit,
not external peer review, a new proof of every theorem, or a certificate of
publication priority.

The package assessments support a qualified handoff for manuscript
preparation. I found no unresolved mathematical blocker in the accepted
claims examined here. This does not make every retained observation a new
standalone publication. The principal contribution claims, credited
supporting results, and open extensions are separated clearly.

## Material reviewed

I read the current assessments for
[penalties](publication-penalty-assessment.md),
[quadratic hulls](publication-quadratic-assessment.md),
[indicator stars](publication-star-assessment.md), and
[supporting investigations](publication-supporting-assessment.md), together
with the [reproduction index](publication-reproduction.md).
I then read the completed [central handoff](publication-readiness.md)
and the updated batch and repository introductions. Their scope agrees
with these assessments: current-batch manuscript preparation is complete,
while source priority, publication acceptance, and unresolved extensions
are not represented as settled.

For claims whose wording could conceal a scope or correctness issue, I
also read the relevant primary mathematical passages: the assumptions and
conclusion of [the penalty upper bound](penalty-upper-bound.md), the exact
decision and approximation reductions in
[the calibration note](minimum-penalty-hardness.md), the unrestricted
parameter domain and cone equivalence in
[the quadratic-family note](three-positive-family-sdp.md), and the complete
general transfer proof in [the indicator moment note](tree-indicator-moment-gluing.md).
The [fresh fixed-count proof audit](publication-penalty-fixed-k-audit.md)
and [source-version treewidth audit](publication-treewidth-review.md)
were also inspected for agreement with their package summaries.

## Conclusions that must remain qualified

| Package | Defensible main contribution | Boundary that must survive manuscript preparation |
| --- | --- | --- |
| Exact penalties | An explicit optimized-dual encoding obstruction, complemented by sufficient encoding upper bounds and restricted calibration hardness | The lower bound is exponential in continuous dimension and superpolynomial in sparse input length; those are different claims. The upper bounds require the stated slice assumptions. Smallest-penalty calibration is hard even though a conservative sufficient coefficient is easy in that construction. |
| Quadratic cuts | A strict exact gap for specified relaxations, a valid family including exposed rays, and a compact lift enforcing that family | Complete three-variable box hull formulations and separation predate this work. The new block supplies a selective strengthening. Completeness, minimum lift size, exact polynomial-time SDP decision, and practical speedup do not follow. |
| Indicator stars | Transfer of subset incompatibility to the original quadratic epigraph and a rational, uniformly conditioned quantitative obstruction | Different subsets share only the total and singleton moment matrices. The result does not cover stronger overlap consistency, every conic formulation, or optimization runtime. Its exponent has close prior geometric antecedents; the simultaneous optimization realization is the proposed addition. |
| Supporting material | Credited formulations, exact counterexamples, restricted lemmas, a source-specific correction, and useful negative findings | Close or classical antecedents prevent treating all items as cleared standalone novelties. Unresolved broad questions are explicit extensions, not silently assumed theorems. |

The proof scopes also agree across packages. Optimized-dual value exactness,
existence of a finite maximizing multiplier, and equality of minimizer sets
are distinguished. The quadratic family permits unrestricted real `h` and
nonnegative remaining parameters; the stronger contact assumptions apply
only to its exposed-ray subclass. The star transfer includes closedness,
control of the unbounded moment set, and passage to the closed epigraph
hull, rather than identifying auxiliary incompatibility with an
original-variable gap without proof.

The treewidth correction is now attributed by version. The August 19
revision directly assumes torso width in its main theorem. The false
graph bound remains relevant to its corollary's proof. The audit does not
infer that the corresponding optimization conclusions are false, and does
not represent the direct torso assumption as a new repair first introduced
here. That wording agrees with the separate source checks; this final
audit did not independently re-audit the entire external preprint.

## Correction found and resolved

The first reproduction-index version I read said the integer-structure
checks had no retained script. That had become stale after
`check_integer_structure.py` was added. I reported the contradiction;
the reproduction owner corrected the paragraph and added the script,
counts, dependencies, and verification limits to the supporting table.
I reread the corrected passages and confirmed their agreement with the
supporting assessment. No new theorem or proof repair was needed.

One further wording refinement separates construction of parent moment
matrices from explicit construction of scalar atom locations. The new
star checker builds positive definite rational pattern matrices and checks
their totals and marginals. The two-atom realization argument then certifies
actual local laws; the checker need not compute their possibly irrational
atom locations. The mathematical implication is sound, but the latter step
belongs to the proof rather than the exact program output.

## Verification limits and remaining work

This final audit did not rerun unchanged arithmetic suites, Lean, numerical
searches, project-wide verification, or CI. The result-specific runs and
source artifacts are recorded in the reproduction index and individual
audits. Those checks establish different kinds of evidence and are not
interchangeable: finite rational certificates establish their exact
instances, symbolic checks establish their displayed identities, Lean
covers its stated formal theorems, and literature comparisons constrain
priority claims.

No further extension is required to state the accepted theoretical results
accurately. Choosing a venue, writing manuscripts, obtaining external
review, and checking source revisions again at submission remain normal
publication steps. Solver experiments would be required for a practical
performance claim; none is part of the present mathematical conclusions.
Novelty remains qualified by the sources and formulations examined, even
where no equivalent statement was found.
