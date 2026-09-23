# Topic coverage map

Inventory begun at stage 1 on 2026-09-22; current status updated after
stage 3 corrections. This is a development record, not part of the
submission manuscript. Stages 1, 2, and 3 are accepted. Stage 3 completed
five independent reviews and all accepted corrections before coordinator
acceptance.
Later planned material is not yet accepted mathematics. The initial
destination table records the development plan; the authored-destination
tables below identify the current manuscript coverage.

## Repository sources inspected

The canonical source is `results/quadratic-aggregation-trivial-hull-certificate.md`.
Its complete mathematical content is mapped below. Concurrent frontier and
formal sources, discovered during the first review round, are inventoried
separately below. Their inclusion is not an acceptance of their claims. Topic searches across the
repository also identified `notes/review-quadratic-aggregation-certificate.md`,
the aggregation portions of `notes/review-minlp-developments-20260922.md`,
`notes/log.md` (entry beginning line 1156 and the September 22 audit entry),
the README topic entry, and `code/quadratic_aggregation/`.
Other notes about quadratic precision, rank, clustering, or bilevel optimization
are separate topics and supply no additional result for this paper.

| Development | Canonical location | Planned destination and treatment |
|---|---|---|
| Open system, homogenization, HHC, nontrivial certificate | §§1–2 | Stage 1 notation and original question; stage 2 theorem |
| Asymptotic hyperplane convexity | §1, proof remarks | Stage 2 definition, proof, normal-specific scope |
| No strict negative quadratic direction | Lemma 1 | Stage 2 proof; avoid confusing this with general recession-cone characterization |
| Hyperplanes disjoint from homogeneous strict system | Lemma 2 | Stage 2 proof, including t=0 and open-hull separation |
| Closed finitely generated cone separated from PSD cone | Lemma 3 | Stage 2 elementary lemma; no novelty claim for compactness itself |
| Exclusion of trivial limit certificates | §3.3 Steps 1–3 | Stage 2 retain the argument as supporting development; the shorter proof below can carry the main exposition |
| Direct nonzero PSD limit from strict-feasibility elimination of the constant | Concurrent §3.4, formal SOURCE-REVIEW.md, and contributed formal section | Stage 2 develop the shorter main proof: normalize `(A,b)`, use compactness in the closed finitely generated cone, and recover actual nonnegative weights; preserve Lemma 3 independently and avoid duplicating the proof in the formal account |
| No restrictions n≥3 or m≥2 in main theorem | Proof remark 3 | Stage 2; explain known m=1 and m=2 cases |
| Closed inequalities under strict feasibility | Corollary 1 | Stage 3, ordinary convex hull throughout |
| Closed system without strict feasibility | Corollary 1 example | Stage 3 exact proof of proper hull with interior, HHC, trivial certificates |
| Necessity of nonzero homogenized aggregations in BDS closed theorem | Same example | Stage 3 verify inertia and empty good-aggregation set; cite v2 Theorem 2.24 and Remark 2.25 |
| Three regimes under HHC | Corollary 2 | Stage 3 with n≥3 hull description; n≥2 emptiness certificate scope |
| Finite SDP characterization | Corollary 3 | Stage 3 improve 2[n(n+1)/2+n] objectives if possible; exact values, no complexity or solver-certification claim |
| Shor projection is whole space iff hull is | Corollary 4 | Stage 3; existence guarantee only |
| Without HHC, Shor projection whole iff certificates trivial | Lemma 4 | Stage 3 cone argument with midpoint identity; handle nonclosed cone |
| Classical convex aggregation/Shor relation | Corollary 4 discussion | Stage 3 own proof of needed closure relation; do not inherit unchecked KT equality claim |
| Two forms and three forms with PDLC of A blocks | Corollary 5 | Stage 3, attribute Dines/Polyak and known two-constraint case |
| Stable convexity of A tuple | Corollary 5 | Stage 3 sufficient condition, no conflation with HHC |
| PDLC of A versus Q when trivial certificate exists | Corollary 5 scope | Stage 3 preserve Schur-complement qualification; avoid claiming genuinely broader unresolved case |
| HHC without stable convexity | Corollary 5 scope, corrected audit | Stage 3 exact arbitrarily small perturbation and midpoint obstruction |
| Ordinary hidden convexity insufficient, also on E | §5 four-form example | Stage 3 complete image, trace, boundedness and midpoint proofs |
| Three-form version of preceding obstruction | §5 final paragraph | Stage 3 concise reduction with bounded linear functional |
| Convex aggregations and Shor need not describe hull even under HHC | §7 strip example | Stage 3 exact witness at zero, preserved from corrective audit |
| Original note leaves finite good-aggregation questions and HHC verification open | §§6–7 | Stage 4 revisit Conjecture 3.1 using the concurrent candidate below; the synthesis stage retain the limitation that no general HHC verification algorithm is supplied |
| Numerical consistency trials | `check_examples.py`, README | Historical only: known two-form case, paired forms, three-form PDLC; no main-proof evidence and no need to rerun expensive solver trials |
| Closed example sampled eigenvalue check | `check_closed_example.py` | Replace sampling with exact proof and standalone exact checks in stage 3 |
| Corrected strip/stability witnesses | `check_scope_counterexamples.py` | Reproduce as exact standalone checks in stage 3 |

The September 22 corrective audit governs over older positive verdicts.
It withdraws claims that globally convex aggregations recover all valid
linear inequalities, treats near-zero SDP values as inconclusive, and
supplies a valid stability example. Historical logs still contain wording
such as “separable example” and “SDP decision procedure”; these are not
accepted scientific claims for the manuscript.

## New investigations proposed by the coordinator

`process/root-investigation.md` records candidate refinements: a strict
separation between asymptotic HHC and HHC using three forms with A1=I;
a reduction to 2n+1 SDP objectives using trace(A) and ±b coordinates; and
an independent closure argument for the Shor projection. Stage 3 has now
developed and reviewed these refinements. Its strict-feasible nonclosed
Shor examples include a compact original feasible set and replace reliance
on the unqualified equality claim in Kojima–Tunçel (see `literature.md`).


## Concurrent frontier note: candidate stage 4 mathematics

Read `notes/research-20260922-aggregation-frontier.md`, including its later
primary-source comparisons, independent derivations, symbolic-check record,
and stronger consequence. Its status explicitly requires adversarial review
and deeper novelty comparison. None of the following is an accepted paper
result at stage 1; stage 4 must supply self-contained proofs and the full
five-reviewer process. The note uses older BDS numbering: any manuscript
citation must be checked against the v2 numbering used here.

| Candidate development | Note location | Planned destination and treatment |
|---|---|---|
| General HHC for `phi_i(X,t)=tr(A_i XX^T)+c_i t²`, `X` of size `k` by `r`, `r>=3k` | General HHC construction | Stage 4 check the Gram completion, common nullspace dimension, zero-mixing/zero-`s` cases; compare matrix-programming and joint-image literature; do not claim a sharp dimension threshold |
| Three inequalities `norm(u)²<1`, `norm(v)²<1`, `u·v>1/2`, with `r>=6` | Main claim; Applying the lemma | Stage 4 prove HHC, nonemptiness, boundedness, and proper hull; candidate affirmative answer to BDS Conjecture 3.1 |
| Exact good-multiplier cone `lambda>=0`, `lambda3²<=4 lambda1 lambda2`, excluding zero | Exact identification of good aggregations | Stage 4 prove replicated inertia and strict convex-hull validity; distinguish the 2 by 2 block from the full quadratic matrix |
| Continuum of positive-definite Gram witnesses with uniquely active rays `(tau,1/tau,2)` | Infinite necessity | Stage 4 verify realizability, strict slack for every different ray, and the quantifier over every finite good-aggregation family |
| Exact open-hull formula `p>0`, `q>0`, `1/2-u·v<sqrt(pq)` | Optional hull formula from BDS | Stage 4 derive from the cone and verify use of the BDS v2 theorem; no automatic novelty claim for convexification |
| Direct midpoint construction for the same hull formula when `r>=3`, with covariance Cauchy–Schwarz converse | Independent derivations received | Stage 4 develop a self-contained proof independent of HHC/BDS; compare known matrix-programming exactness |
| No signed positive-definite combination of the homogenized matrices, despite `A1+A2=I` for the quadratic parts | PDLC fails; Additional primary-source comparisons | Stage 4 prove the obstruction and distinguish PDLC on `Q_i` from PDLC on quadratic blocks |
| Nonempty common projective zero set and singular spectral determinant | Additional primary-source comparisons | Stage 4 verify the witness and determinant factorization before using them to delimit spectral finiteness theorems |
| Every exact strict good-aggregation description must contain uncountably many rays | Stronger consequence awaiting independent review | Stage 4 verify the stronger quantification using the unique-ray witnesses; state that the claim concerns the ordinary open hull and strict inequalities |
| Closed-hull distinctions: a dense countable family suffices for all non-strict aggregates; no finite family can suffice if the proposed perturbation argument works | Stronger consequence awaiting independent review | Stage 4 develop the closed-hull identification and finite-family perturbation proof; the note gives an argument sketch, not an accepted closed-hull theorem |
| Exact multiplier determinant, witness constraint vector, distinct-ray slack identity, and Gram determinant | Targeted verification performed | Stage 4 reproduce in a standalone exact-check script; historical SymPy assertions do not prove HHC or novelty |
| Finite extended conic formulations are not ruled out | Main claim; Additional primary-source comparisons | Stages 4–5 explicitly distinguish direct good-aggregation necessity from SDP/SOCP extended formulations; credit prior closed SDP exactness |

See `literature.md` for which external sources were actually inspected in
stage 1 and which are source leads requiring stage 4 followup.

## Core formal package: accepted stage 2 integration, pending packaging

Initially inspected `formal/topics/27-quadratic-aggregation/README.md`,
`CLAIMS.md`, `SOURCE-REVIEW.md`, and `COVERAGE.md` while the package reported
in-progress status. During stage 1 corrections the README changed to complete,
and `REVIEW.md`, `VERIFICATION.md`, and `verification/manifest.json` became
available. Those updated records and the contributed
`sections/90-formal-verification.tex` were then read. The exact source hashes
and inspection time are frozen in `stage01-formal-source-snapshot.json`.

At stage 1, the package reported warning-free targeted builds of 11 modules,
an axiom audit of 178 owned declarations, and 11 successful module kernel
replays; that stage recorded the claim without rerunning Lean. Stage 2 then
reviewed the actual theorem interfaces and semantic correspondence, and the
coordinator independently reran all these targeted checks successfully.
The exact evidence and limits are recorded in `stage02-root-formal-check.md`.
The pinned toolchain is Lean 4.33.1. These checks do not certify later
mathematics, and no CI result is inferred.

The frozen obligations Q01–Q12 cover the strict-system definitions, main
Theorem 1, its supporting Lemmas 1–3, and the HHC specialization (Conjecture
3.3). They exclude Corollaries 1–5, Lemma 4, example classifications, SDP or
complexity guarantees, and novelty claims. They do not cover the frontier
note or certify the manuscript as a whole. The integrated formal account
states this bounded scope and the actual reviewed evidence.

The contributed formal section was deferred from the main build during
stage 1. Stage 2 integrated and reviewed the shorter main proof and bounded
formal account, without repeating the proof in two sections. The paper's
five-reviewer requirements remain independent of the formal package's reviews.
The contributed wrappers `FORMAL-VERIFICATION.md` and `formal-verification.tex`
are preserved and use the accepted core sections. Portable source/supplement
packaging remains an obligation of the synthesis stage.

The canonical result now includes §3.4. It and `SOURCE-REVIEW.md` give the
shorter proof: strict feasibility bounds the constant coefficient above by
a continuous function of the quadratic/linear pair; normalize that pair,
then use compactness in the actual closed finitely generated cone. A norm-one
PSD limit directly supplies actual nonnegative aggregation weights. No bound
on the original constant divided by the pair norm is assumed. Stage 2
independently checked this proof and preserved the older uniform-distance
cone-separation lemma as supporting mathematics. The intermediate simplex
limit is a proof device, not a separate conclusion every proof must reproduce.

## Older conflict-repair exploration: concise stage 3 application appendix

Inspected the aggregation proposal in
`notes/research-20260912-algorithm-opportunities.md` and its linked
`notes/review-20260912-quadratic-conflict-example.md`. The exploratory note
is closed; no conflict-repair integration or solver benchmark was implemented.
The coordinator includes its proved mathematical construction and corrected
example in a concise stage 3 application appendix to cover the relevant
repository developments. These are elementary/classical applications, with
no algorithm novelty or performance claim. Their historical correctness
review does not replace the paper's required author and reviewer process.

| Development | Stage 3 treatment |
|---|---|
| Nonnegative aggregation of original globally active inequalities and validity of local affine underestimators | State and prove the certificate contract, including a positive box margin and the distinction between local underestimator validity and global aggregate validity |
| Convex aggregate and tangent cuts | Prove global validity; distinguish separation of the expansion point from exclusion of a whole box, which needs a minimizer or a separate support check |
| Diagonally dominant multiplier-repair LP | Give the inequality-row simplex normalization, absolute-value lifting, exact affine box-minimum lifting, and rational sum-of-squares PSD certificate; a feasible positive margin suffices, without optimality |
| Signed equality multipliers | Retain the corrected normalization of nonnegative positive/negative parts together with inequality weights, including equality-only certificates; explain why normalizing only inequality weights can leave the margin objective unbounded |
| Conditional GDP rows | Retain the conjunction of supporting activation conditions; do not present the resulting cut as globally unconditional |
| Corrected two-row exact example | Independently check estimator validity, root lifted witness and envelopes, PSD aggregate, tangent, feasible activation witnesses, and node exclusion |
| Exact repair optimum | Verify DD range `1/5<=a<=5/7`, both affine-margin pieces and their common breakpoint, and optimum `(5/7,2/7)` with normalized margin `1/35`; do not compare it to an unnormalized margin |
| Pure-bilinear limitation | Prove that a PSD matrix with zero diagonal vanishes; cancellation may yield affine aggregates but supplies no quadratic curvature |
| Shor implication | Link to the stage 3 general inclusion: all PSD aggregate inequalities follow from a common Shor lift; the toy example shows room beyond its termwise relaxation, not beyond the full Shor relaxation |
| Exact script `code/research_20260912/verify_quadratic_conflict_example.py` | Reproduce needed identities in the standalone exact checks; no need for solver benchmarks |

The unrelated inexact OA/Benders candidate and unimplemented repair-selection
experiments are excluded. They are historical proposals, not unfinished
obligations for this paper. Literature comparisons for the application are
recorded separately in `literature.md`.

## Stage 3 accepted destinations

| Development | Current manuscript destination |
|---|---|
| Closed-system properness and strict-feasibility qualification | `cor:closed`, `ex:closed` |
| Three regimes with separate n≥2 and n≥3 bounds | `cor:regimes` |
| Improved finite SDP characterization, using 2n+1 objectives | `eq:sdp-objectives`, `cor:finite-sdp` |
| Shor inclusion, cone dual, closure equality with strict feasibility | `eq:shor-aggregation`, `prop:shor-closure` |
| Hypothesis-free whole-Shor equivalence given S nonempty | `eq:shor-whole`, second half of `prop:shor-closure` |
| Shor/hull whole-space equivalence under AHC | `cor:shor-hull` |
| Strict-feasible nonclosed projection, including compact original T | `ex:nonclosed-shor`; independently proved two-/four-row formulas |
| Stable parts, two forms, three forms with real PDLC | `prop:stable`, `eq:perturbed-parts` |
| A versus Q PDLC qualification in trivial-certificate case | Paragraph after `prop:stable` |
| Strict AHC versus HHC, stable does not imply HHC | `ex:ahc-not-hhc` |
| HHC does not imply stable convexity of parts | `ex:hhc-not-stable` |
| Ordinary HC on full space and E insufficient, four-/three-row variants | `ex:ordinary-hc` |
| Exact closed example, interior and no good multipliers, BDS nonzero-Q condition | `ex:closed` |
| Convex aggregations/Shor fail to describe hull even under HHC | `ex:strip` |
| Local/global validity, tangents, whole-box qualification | `prop:local-certificate` in `app:application` |
| Exact DD repair LP, affine minimum lift, PSD identity | `eq:repair-lp`, `eq:box-minimum`, `eq:dd-sos` |
| Equality normalization and activation-condition preservation | Application validity subsection |
| Rational original example, lifted witness, estimators, tangent and activations | `eq:repair-example`, `eq:repair-tangent` and surrounding proof |
| Exact repair optimum, normalized margin comparison | Final paragraphs of application rational-example subsection |
| Pure-bilinear and Shor limitations | Application final subsection |
| Standalone exact reproducibility checks | `supplement/check_examples.py` |

The contributed `sections/91-formal-consequences.tex` and topic-28 package
were identified during this stage. Their portable integration and actual
formal-source review are deferred to synthesis at the coordinator's
direction. The fragment is preserved but is not input by stage 3; its older
signed-coordinate SDP count differs from the 2n+1 trace reduction above.
The main-proof formal account does not silently acquire this broader scope.

## Stage 2 accepted destinations

The main build now includes `sections/02-certificate.tex` and the revised
`sections/90-formal-verification.tex`. This supersedes the stage 1 deferral
above. Stage 2 is accepted after its five independent reviews.
Stage 3 is accepted after its reviews and corrections;
frontier material remains outside these stages' acceptance.

| Covered development | Current manuscript destination |
|---|---|
| AHC in unbounded-level and increasing-sequence forms; HHC implication | Definition `def:ahc` and its following equivalence argument |
| Complete nonempty AHC theorem and Conjecture 3.3 specialization | `thm:certificate`, `cor:hhc-certificate` |
| Common negative leading direction and all-target midpoint proof | `lem:negative-direction` |
| Strict supporting halfspace, exclusion at t=0 and either sign of t | `lem:sweeping` |
| Separation of nonclosed convex image from open negative orthant and simplex normalization | `lem:hyperplane-certificate` |
| Actual coefficient cone, closedness via independent-support reduction | `eq:coefficient-cone`, `lem:finite-cone` |
| Strict-point constant elimination, nonzero pair, compact unit limit and actual final weights | Proof of `thm:certificate`, `eq:constant-elimination`, `eq:eliminated-sweep`, `rem:limit-scope` |
| Both easy-direction cases, no nonemptiness/AHC needed | First paragraph of the theorem proof |
| One supporting normal suffices; dimensions n,m>=1; old one/two-form cases | `rem:one-normal` |
| Original uniform cone separation and full quantitative alternative | `lem:uniform-cones`, `eq:distance-psd`, `prop:sweep-bound`, final subsection paragraph |
| Precise formal statement correspondence, equivalent norms, actual checked scope and exclusions | `sec:formal-verification` |
| Standalone wrapper without duplicating proof text | `formal-verification.tex` reuses setting, main proof and formal account |

The author read all eleven actual Lean modules and the declaration interfaces,
not merely the reported coverage. Their correspondence and proof-route details
are recorded in `stage02-author.md`. The coordinator independently reran the
explicit module build, all-owned-declaration axiom audit, and eleven kernel
replays; all passed. Its exact command, result, and boundaries are in
`stage02-root-formal-check.md`, with logs under
`verification/stage02-root-formal/`. This is local topic-specific verification,
not CI or project-wide verification. The author did not duplicate that run.

The formal sources and reproducibility records still need a portable supplement
at the synthesis stage. `FORMAL-VERIFICATION.md` explicitly records this
packaging obligation.
The final source/PDF snapshot is `stage02-author-snapshot.json`.


## Stage 4 authored destinations (reviewed and strengthened; awaiting acceptance)

The initial frontier table above records the earlier candidate, not the
final theorem's dimensions. Five independent reviews found no major or
minor correctness issue. The accepted strict-description strengthening is
incorporated, pending coordinator acceptance. The sharp source and integrated result now
supersede its r>=3k/r>=6 construction. No additional novelty claim is made
for that earlier, weaker proof.

| Development | Authored destination |
|---|---|
| Full Gram map plus scalar square: HHC iff r>=k | Section 5, Theorem `thm:gram-hhc`; full exact image except k=r=1 |
| Singular Gram factors and real orthogonal trace interval | Lemma `lem:gram-range`; explicit pair rotations, including odd square dimensions |
| Classical squared-fidelity infimum and concavity | Lemma `lem:fidelity-concavity`; Uhlmann credited, boundary proof supplied |
| Arbitrary number of repeated-block forms | Corollary `cor:gram-family`; no mixed tX terms or codimension-two claim |
| Three inequalities in 2r variables for every r>=2 | Section 6, Proposition `prop:ball-good-cone`; HHC, boundedness, exact good cone |
| Indispensable continuum of strict rays | Theorem `thm:indispensable-rays`; every ray in tau in [1,2] must occur |
| No finite nonstrict good family; dense countable suffices closed | Theorems `thm:indispensable-rays` and `thm:ball-hulls` |
| Open/closed formulas, closed original-system hull, finite SDP lift | Theorem `thm:ball-hulls`; direct midpoint sufficiency for r>=3 and covariance necessity also supplied |
| No countable strict quadratic conjunction in the original variables | Theorem `thm:no-finite-quadratics`; each nonzero quadratic has finitely many zeros on an uncountable analytic boundary arc, so every exact strict description requires uncountably many inequalities |
| No finite nonstrict quadratic conjunction in the original variables | Same theorem; identically zero planar restrictions discarded before the finite-family neighborhood argument; countable nonstrict good descriptions remain possible |
| No homogeneous PDLC, repeated spectral determinant, common projective zero | Final subsection of Section 6; precise limits of spectral/definiteness comparisons |
| Earlier DMS infinite example, different DHW architecture, QMP and hypograph convexification | Section 6 literature subsection, with exact HHC/inertia distinction and primary-source locators |
| Exact rational witness identities and finite-family perturbations | `supplement/check_infinite_aggregation.py`, standard library only |

Sources read: `notes/research-20260922-gram-hyperplane.md`, its independent
review, `results/infinite-quadratic-aggregation-hhc.md`, the novelty and
integrated reviews, and the earlier frontier provenance. The resulting
proofs are self-contained apart from explicitly cited published background
(the BDS full aggregation theorem for the r=2 hull). Quantitative accuracy
and objective-specific exactness are stage 5; the four-aggregation PDLC
development is stage 6; concurrent formal wrappers remain for stage 7.
## Stage 5 authored destinations (awaiting independent reviews)

| Development | Authored destination |
|---|---|
| Extended Euclidean Hausdorff objective over at most N arbitrary good cuts | Section 7 opening; `thm:approximation-rate` |
| Dimension-independent rate, improved lower constant sqrt(2)/2000 | `eq:approximation-rate`; finite-grid proof |
| All-point angle-mesh estimate and radial repair | `lem:angle-mesh`, `eq:angle-defect` |
| Coordinate endpoints, N=2, arbitrary nonuniform angular meshes | `lem:angle-mesh` and its application |
| Exact integer coefficient construction and 2m+1 cut count | `cor:rational-mesh`, `eq:rational-mesh` |
| O(log N) bits per multiplier coefficient, not full formulation or numerical complexity | Paragraph following `cor:rational-mesh` |
| Explicit necessary/sufficient epsilon cut counts without infimum attainment | Paragraph after `thm:approximation-rate` |
| N+1 rational Gram witnesses, arbitrary interior multipliers, finite pigeonhole proof | `eq:accuracy-gram`, `eq:accuracy-values`, `eq:grid-exclusion` |
| Uniform linear-objective interpretation | `eq:hausdorff-support` and proof |
| One objective-dependent exact good aggregation | `prop:one-objective`, self-contained strict-feasibility separation proof |
| Comparison with Rote, local Bronshteyn–Ivanov, Arya–da Fonseca–Mount, classical conic duality | Section 7 final paragraphs and `stage05-literature.md` |
| Reproducible quartic slice illustration, N=3,5,9 | `fig:finite-aggregation`, PDF and plotting source |
| Exact finite mesh/witness/radial checks | `supplement/check_approximation.py` |

Read `notes/research-20260922-aggregation-accuracy.md` and its independent
review, plus the newly contributed finite-grid argument in
`sections/94-formal-aggregation-accuracy.tex`. The main proof replaces the
older logarithmic covering proof with the simpler finite-grid construction
and improves its distance constant using the sharper 5 sqrt(2) gradient
bound. This is a stronger manuscript statement than the concurrent formal
fragment's reported 1/(2000 N^2) lower bound; formal coverage is deferred
to stage 7 and not presumed here. The old logarithmic proof remains source
provenance, rather than a duplicate weaker proof in the paper.

The rate concerns good cuts only. No rate for arbitrary quadratics,
algorithmic iteration lower bound, solver improvement, or new general
approximation/duality principle is claimed. The figure is a planar
illustration; the Hausdorff proof controls all original coordinates.

## Stage 6 authored destinations (awaiting independent reviews)

| Development | Authored destination |
|---|---|
| Four strict-good aggregations for signed PDLC, every n>=1 | Section 8, `thm:strict-four` |
| All hypotheses of the external BD theorem, including independence and no infinity | `thm:bd-four-input`; explicit preprint low-dimensional proof locators |
| Countable exceptional levels for any continuous function on a second-countable space | `lem:regular-levels`, elementary countable-base proof |
| Proper hull excludes common negative leading direction | Reuses accepted `lem:negative-direction` |
| Independent positive definite perturbations even for dependent original triples | `lem:inward-pdlc`, explicit matrices and nonzero cubic coordinate minor |
| Boundedness and absence of nonstrict points at infinity in every inward system | `lem:inward-pdlc`, normalized-sequence proof |
| Regular selected levels and eventual inclusion of every fixed finite feasible subset | `lem:inward-pdlc`, ratios with positive denominators |
| Deletion of globally nonpositive polynomials before strictification | `lem:strictification`, exact quadratic local-maximum argument |
| Fixed four-tuple limit, nonzero simplex multipliers, exactly one negative eigenvalue | Upper-bound proof, `eq:four-matrix-limit` |
| Preservation of strict goodness and singular negative components | `eq:negative-components` and pointwise eventual-inclusion eigenvector argument |
| Exact strict hull equality, with no final closure interchange | Final paragraph of the upper-bound proof |
| Dependent triples reduce to at most two original rows and known two-bound | `rem:dependent-four`, attributed to Yildiran |
| Credited BDS sharpness, independent four indispensable-ray witnesses | `ex:four-sharp`, `eq:four-ray-cone`; n>=3 only |
| At most four oriented SOC constraints for the closed strict hull | `cor:four-soc`, mixing proof |
| Naive nonstrict replacement and hull of original nonstrict set can differ | PDLC half-ball example following the SOC corollary; correct v2 Example 2.23 |
| Qualified priority compared with BD and Dunbar's stronger dissertation statement | Section 8 opening and `stage06-literature.md` |
| Exact polynomial, rational/radical witness, and cone decomposition checks | `supplement/check_four_aggregation.py`, standard library only |

Read the complete current `results/four-aggregation-strict-pdlc.md`, the
frontier note and its transfer, second, compact, and priority reviews. The
current direct inward proof supersedes the older projective-chart route;
the latter remains provenance and is not duplicated in the manuscript.
The finite-check script does not certify the universal proof, the external
topological theorem, or novelty. Concurrent formal sections and their
packaging remain stage 7 work.

## Stage 6b authored destinations (awaiting independent reviews)

| Development | Authored destination |
|---|---|
| Matrix span of dimension three, signed PDLC, k extreme rays/facets | Appendix `app:three-span`, pointed cone and polygon section |
| Known unconditional 2k bound | Explicitly credited to BDS v2 Proposition 2.22 |
| HHC for the entire many-form family | Proof of `prop:facet-bound`, restriction of a basis triple and linear image |
| Directional exit and at most 2 times the number of negative facets | `prop:facet-bound`; PSD improvement and full-system pair reduction credited |
| Conditional 2k−2 when PSD in the span is not contained in the negative matrix cone | `eq:conditional-facet-bound` |
| Minimization over positive definite directions | Paragraph following the proposition; existence, not algorithm, claim |
| Centered ellipsoids with exactly k necessary aggregation rays | `ex:many-ellipsoids`; Vandermonde and exact boundary witness identities |
| Every infinite strict family must contain all original rays | Same example; no extension of indispensability to infinite weak families |
| Exactly k inequalities for finite weak descriptions | Same example, local continuity and radial dilation |
| New resolution of the proposed general-cone two-bound shortcut | `prop:complementary-many`: augmented ellipsoid family, exact count m=k−2 |
| Complementary PSD cone inclusion with arbitrarily many necessary rays | `eq:negative-orthant-contained`, exposed original rays and two added extreme rays |
| Strict set changes but ordinary hull is preserved | Generic small midpoint perturbations in the proof |
| Counterexample retains compact regular weak set, nonempty interior, no infinity | Final paragraph of `prop:complementary-many` |
| Why triangulation/intersection and arbitrary addition do not supply missing bounds | Appendix ending; no unconditional 2k−2 or optimal-count assertion |
| Exact symbolic identities and 1,235 rational witness evaluations | `supplement/check_three_dimensional_span.py` |

Read `notes/research-20260922-span-three-many.md` and its independent
review, plus `process/stage06b-root-development.md`. The previously proposed
general-cone analogue of the two-bound is now disproved explicitly; it is
not left as a plausible unproved input. This is distinct from determining
an optimal universal many-generator bound, for which no claim is made.
