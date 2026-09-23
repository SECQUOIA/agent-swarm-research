# Stage 4 author completion record

Status: author complete; ready for the required first full-stage 15-reviewer
round. This is not coordinator acceptance or a frozen review record.

The replacement sole author audited all four saved drafts after the prior
author was interrupted. The completed stage is in
`sections/09-cardinality-spatial.tex`,
`sections/10-cardinality-preordering.tex`,
`sections/11-coordinate-domains-lifts.tex`, and
`sections/12-relative-blocks-cuts.tex`. They are Sections 12--15 in the
current cumulative PDF. `main.tex` inputs all four, and `references.bib`
contains the five added Stage 4 citations. No later-stage text was authored.

All six canonical source files in the seven-row scope matrix below were
read, together with the paper-local lift candidate, the relevant correction
notes, the certificate definitions in `sections/01-foundations.tex`, the
assignment, and the coordinator's provisional proof/source records.
The proofs were reconstructed directly; historical PASS labels were not
used as mathematical premises. The 14 accepted section and macro files
match `process/snapshots/stage03-accepted` byte for byte. Accepted snapshots,
other paper folders, repository source notes, and literature were not edited.

## Complete source-to-claim coverage

Paths beginning with `results/` or `notes/` are relative to the repository
root. All labels below occur in the current manuscript.

| Stage 4 scope source | Claims retained or completed | Manuscript labels |
| --- | --- | --- |
| `results/spatial-bb-exponential-lower-bound.md` | Exact optimum, arbitrary real coordinate splits and overlapping covers, endpoint witnesses, domination of all separable convex underestimators, exact separable McCormick/minimal-alphaBB interpretation, exponential upper certificate, polynomial fixed-demand exact certificate, charged discarded slabs, small feasibility tolerance, quadratic chord error. The older claim leaving SDP spatial behavior open is superseded explicitly. | `sec:cardinality-spatial`, `eq:cardinality-problem`, `eq:cardinality-optimum`, `eq:cardinality-chord`, `eq:cardinality-witness`, `lem:endpoint-count`, `thm:chord-cover`, `prop:chord-upper`, `eq:second-order-chord`, `prop:charged-tolerance`, `thm:sdp-cover` |
| `results/spatial-bb-sdp-rlt-exponential-lower-bound.md` | Complete augmented PSD and all pairwise box inequalities, including repeated/diagonal indices and degenerate intervals; equality products, exact restricted moment objective, cover lower bound, chord domination and original-space affine-product closure. | `eq:sdp-model`, `eq:box-rlt`, `lem:sdp-witness`, `thm:sdp-cover`; closure paragraph at the end of `sec:cardinality-spatial` |
| `results/spatial-bb-higher-sos-exponential-lower-bound.md` | Exact order-one equivalence, classical moments with fresh homogeneous/Gram proof, degree-correct balance identities, every repeated slack product with every allowed global square, restriction/order tradeoff, positive distinct perturbations, unique optimizer and symmetry on the balance slice, increasing concave costs with the absolute/relative distinction. | `sec:cardinality-preordering`, `eq:preorder-normalization`, `eq:preorder-equality`, `eq:preorder-positivity`, `eq:fractional-moments`, `lem:fractional-positive`, `eq:fractional-homogenization`, `eq:fractional-gram`, `lem:assignment-localizer`, `thm:preordering-cover`, `eq:qr`, `cor:unique-cardinality`, `eq:perturbed-qr`, `eq:increasing-allocation` |
| `results/spatial-bb-product-domain-exponential-lower-bound.md` | Arbitrary nonempty coordinate sets, including disconnected/nonclosed sets; every valid univariate polynomial equality/inequality through degree; products with global squares; scalar-function branching and exact charging of removed sets; literal polynomial substitution with effective order rD retained as a coarser comparison. | `sec:coordinate-domains`, `eq:product-domain-oracle`, `eq:product-domain-equalities`, `thm:product-domain-cover`, `eq:local-endpoint-interpolation`, `prop:literal-lift` |
| `process/univariate-lift-refinement.md` | Candidate proved by affine endpoint interpolation with no loss of order, even for nonpolynomial auxiliaries finite on all of [0,1]. Originals remain available, balances remain affine, local graph restrictions are independent, and the available polynomial objective agrees on the full graph. Every balance product, local equality product, localizer and objective transfer is proved. Relative-block transfer includes a globally coupled written objective. | `eq:local-graph-map`, `eq:lifted-local-oracle`, `thm:local-graph-lift`, `eq:graph-interpolation-map`, `lem:tensor-preordering`, `thm:relative-cover` |
| `results/spatial-bb-relative-gap-exponential-lower-bound.md` | Fixed-size blocks under one global total-degree oracle, full tensor positivity, explicit relative exponent and positive-tau regime, r=1/t=2 example, strictly increasing/concave costs, unique optimizer, squared-index coefficients excluding permutations modulo balances, and the short alternative component certificate. | `sec:relative-blocks`, `eq:relative-problem`, `eq:relative-optimum`, `eq:relative-target`, `lem:tensor-preordering`, `thm:relative-cover`, `eq:relative-cover-bound`, `eq:relative-example`, `prop:relative-asymmetry`, `eq:squared-perturbation`; final subsection of `sec:relative-blocks` |
| `notes/spatial-bb-known-clique-cut.md` | Classical Boolean-quadric clique inequality, direct continuous-graph validity, root exactness for base/perturbed/increasing costs and one cut per relative block; the cuts and component certificates limit the claim to the specified certificate system. The signed cubic XOR motivation remains distinct from positive multilinear gaps. | `prop:clique-escape`, `eq:clique-cut`; closing paragraphs of `sec:relative-blocks` |

## Degree, boundary, and model audit

- `lem:endpoint-count` uses the minimum of the two reciprocal avoidance
  bounds, not the incorrect historical maximum. Neither avoidance-event
  independence nor disjoint regions is assumed. Empty endpoint classes,
  zero exclusion counts, impossible avoidance events and q=0 are covered.
- `prop:chord-upper` counts intermediate upper children, giving
  2^(n+2)-3 nodes and 2^(n+1)-1 leaves for positive tolerance. The exact
  midpoint tree has binomial(n+1,k+1) leaves and polynomial exponent
  min{k+1,n-k} when that exponent is fixed. Strict positive-tolerance
  pruning can use a slightly higher chord target.
- `prop:charged-tolerance` explicitly charges certified discarded boxes
  and assumes certification of a closed slab before using it as a box.
  Product domains later charge the exact removed set. The tolerance
  optimum 1/4-delta^2 is proved only for 0<=delta<1/2, and the lower bound
  requires epsilon+delta^2<1/4. Integer demand sums outside that range
  defeat the unrestricted old formula.
- `lem:sdp-witness` establishes the full covariance projection, including
  deterministic restricted rows. All four RLT expressions are checked for
  two free indices, for a repeated free index, and whenever either index is
  restricted. Every row balance product and the objective are calculated.
- At order one the full preordering is exactly the stated SDP--RLT model.
  Original-space affine Farkas representations grant all allowed products
  of valid affine inequalities on the box/balance polytope, at order one
  and at higher order. Constants and degenerate boxes are included. This
  does not grant lifted affine clique cuts or objective-cutoff localizers.
- `lem:fractional-positive` proves normalization, Boolean reduction,
  cardinality products through multiplier degree 2d-1, homogeneous
  replacement with an ideal multiplier of degree at most d-1, and the
  exact incidence Gram decomposition. Vandermonde is used without
  division by a possibly zero numerator. Coefficients are nonnegative
  under the stated sufficient hypotheses.
- `lem:assignment-localizer` proves the uncancelled indicator identity,
  the positive-weight conditional identity when needed, and the separate
  constant/zero-weight/all-assigned cases. Repeated or conflicting slacks
  and arbitrary globally coupled square multipliers are included. The
  following negative-indicator argument shows why stronger classical
  moment-matrix positivity alone does not improve the noninteger full
  preordering range; integer cardinalities are a distinct boundary case.
- `thm:preordering-cover` uses the integer exclusion count to retain
  2r-1 witness coordinates of both endpoint types. It handles r=1
  separately in the remaining-dimension check. The constructed value is
  strictly below the non-strict pruning target. Positive q_r, linear q_r
  and the exact epsilon=1/8 order regime are distinguished. No zero
  threshold is divided by.
- `cor:unique-cardinality` proves strict-concavity reduction to vertices,
  the unique sorted optimizer, and absence of a permutation preserving
  the objective on the balance slice. A fresh sentence explicitly proves
  uniqueness of the linear-cost LP by transferring positive mass from a
  higher-cost coordinate to a lower-cost one; the clique-cut proof uses
  this LP conclusion. First moments lie in [0,1] by the node constraints.
- `thm:product-domain-cover` uses only actual witness and endpoint
  membership. Every local nonnegative polynomial reduces to nonnegative
  endpoint indicators. Distinct nonconstant coordinates consume at least
  one degree each, so expansion preserves the localizer budget even for
  repeated factors. No compactness or hull theorem for coordinate sets is
  invoked.
- `lem:tensor-preordering` constructs full block Gram matrices, tensors
  them, then keeps the principal submatrix of indices with permitted
  total degree. Unused tensor entries need not be global moments. This
  proves positivity for squares coupling every block; equality products
  factor one monomial at a time.
- `thm:relative-cover` treats lightly restricted blocks by fractional
  moments and heavily restricted blocks by actual witness evaluation.
  Its exact bound uses tau>0. Tau<=0 gives only one region. The explicit
  example has tau=17/128 and exponent 17n/384. Fixed order permits fixed
  positive relative tolerance after choosing the block size; there is no
  uniform relative tolerance claimed as order grows without bound.
- `prop:relative-asymmetry` first shows a feasible-set permutation maps
  entire blocks to blocks. Squared-index successive differences then
  exclude translation equivalence of coefficient lists. Distinctness
  alone is explicitly insufficient modulo several balances.
- `prop:clique-escape` proves continuous validity by multiaffinity,
  uses equality products to bound the trace, and combines the resulting
  1/4 penalty bound with the separately attained linear-cost minimum.
  Exact moment evaluation gives attainment. PSD is unnecessary for this
  deduction. The k=0 boundary is treated directly after the cited range.

## Bounded development of the local-lift candidate

The sole author independently validates `thm:local-graph-lift`; it is
promoted into the manuscript for review, not accepted by the coordinator.
The new bound uses order r, independent of polynomial degree D and the
finite number of auxiliaries. The older literal-substitution rD proof
remains in `prop:literal-lift` as a valid weaker comparison.

For every unrestricted coordinate, affine interpolation maps each lifted
variable to its two actual endpoint graph values. Restricted coordinates
are fixed at their actual witness graph values. Thus lifted degree cannot
increase. The original affine balance maps to the same fractional
cardinality relation. A valid local inequality has nonnegative endpoint
values, and a valid local equality vanishes there, so Boolean reduction
proves every permitted localizer and equality product, including global
multipliers. The full-graph objective assumption makes its substituted
polynomial agree on every Boolean assignment with the intended original
objective. Uniqueness of multilinear reduction gives equality of their
moment values through the available degree. This is a construction of a
functional, not a continuous identity between a nonlinear function and
its chord.

Functions must be finite at every point of [0,1], including every witness
value. They may be discontinuous and the resulting graph may be noncompact;
covering is defined by preimages of the original compact feasible set,
whose optimum and attainment are preserved. Original coordinates remain
in the model. Coupled auxiliary functions, coupled valid inequalities,
nonlinear elimination of the originals and an exact hull of the coupled
feasible graph are outside the theorem. The exponent counts original
dimension, not an arbitrarily enlarged lifted dimension.

The relative extension uses these substitutions blockwise and the full
tensor argument. A written lifted objective can couple blocks: agreement
on every substituted Boolean assignment still gives the same reduction
as the original separable objective. This proves the objective estimate
without adding an unjustified written-separability assumption.

No bounded Stage 4 derivation remains unfinished. The sharper local-lift
result and its relative consequence are completed mathematical claims
pending independent review. Publication priority, the optimal tradeoff
over other functionals or stronger oracles, and the later XOR program
are not resolved by this stage. No claim of inherent optimization
hardness is made for the explicit easy-to-optimize families.

## Primary-source checks and access limits

The following are replacement-author checks, separate from the earlier
coordinator checks in `verification/primary-source-checks.md` and
`verification/stage04-root-provisional-review.md`. Original local PDF
hashes and locators are in `verification/stage04-author-validation.json`.

- [Jarre (2018), Sections 2--3](https://optimization-online.org/wp-content/uploads/2018/07/6729.pdf):
  directly read the binary fixing framework and max-cut SDP comparison.
  This supports the limited predecessor sentence; it is not used as a
  premise of the continuous spatial proof.
- [Grigoriev (2001), author manuscript](https://logic.pdmi.ras.ru/~grigorev/pub/square_knapsack_journal.pdf):
  visually inspected original PDF page 7, including the falling-factorial
  functional and Lemmas 1.3--1.4. The cardinality identity and classical
  positivity provenance match the text. The subsequent full positivity
  proof was not audited or imported; the manuscript proves its own
  sufficient Gram positivity and full localizer result.
- [Potechin (2019)](https://drops.dagstuhl.de/storage/00lipics/lipics-vol124-itcs2019/LIPIcs.ITCS.2019.61/LIPIcs.ITCS.2019.61.pdf):
  read Theorem 1 and the knapsack parts of Theorem 44/Corollary 45 via the
  primary PDF; visually inspected Example 18 on original page 61:8.
  This confirms the moment formula and attribution to Grigoriev. No
  audit of the full general symmetry theorem is claimed.
- [Padberg (1989)](https://doi.org/10.1007/BF01589101): visually inspected
  the local original, printed page 149 / PDF page 11, Lemma 2 equation
  (17). Its parameter alpha=k and whole-coordinate set give the exact
  cited cut after changing sides and multiplying by two. The manuscript
  supplies its own continuous extension and root-exactness argument.
- [Coniglio, anonymous review version](https://openreview.net/pdf/369974754b073802afab412ee5f715561c39adbc.pdf):
  a fresh author access returned an OpenReview browser-verification
  challenge. No bypass or successful author read is claimed. The
  coordinator's earlier successful reading of Assumption 1,
  Propositions 2--4 and Appendix C is explicitly recorded in the shared
  source log. The manuscript identifies the review version and restricts
  its comparison to that checked midpoint-branching model. Identity with
  the published version remains unverified. This source is contextual;
  no new theorem depends on it, and no exhaustive priority claim is made.

## Verification and build evidence

All listed commands completed successfully from the paper directory.

| Command | Evidence and scope |
| --- | --- |
| `python verification/check_stage04_author.py` | New exact checks: 27 symbolic Gram-entry identities through d=6; 48 boundary cases including negative noninteger slack products; nine three-block lifted cases through r=3 with 774 equality-product checks and 360 allowed localizer/square checks; discontinuous local functions and coupled graph-identity objective representations; 1,792 vertex checks of clique equality and the unique perturbed optimizer; exact relative example arithmetic. These are finite supplemental checks, not universal positivity proofs. |
| `python verification/check_univariate_lift_refinement.py` | Replayed all 36 exact power/square-root lift cases: 2,880 demand products, 5,760 localizers, available graph identities and objective values. This does not substitute for the full graph-lift proof. |
| `python verification/check_spatial_tolerance_and_tree.py` | Replayed 140 exact tolerance-slab cases with 15,813 enumerated vertices, 1,770 recursive tree counts and three out-of-range tolerance regressions. |
| `python verification/build_and_check.py` | Successful cumulative 80-page PDF; no warnings, duplicate labels, unresolved references or citations. Printed Stage 2 checker still matches its verified file. `verification/build-report.json` records source hashes and PDF SHA-256 `acc8e083b7a3aa985d71e686a73d90405ea005928416a39e0bee05c338206339`. |

Rendered current PDF pages 47, 53, 59, 61 and 64 were visually inspected:
section transition, moment definitions/homogenization, lifted theorem and
substitution, relative model/tensor lemma, and clique-cut statement/algebra
are readable, with no visible clipping. Renders used `/tmp` and did not
change literature or snapshots. The author validation JSON independently
checks that all 14 earlier accepted section/macro files are unchanged.

The only replacement-author manuscript edit after the saved drafts was
the explicit mass-transfer proof of the linear-cost minimum in
`cor:unique-cardinality`. The previously requested infimum clarification
in Section 12 and perturbation parameter quantifiers in Section 13 were
already present and were checked. Bibliography entries and all four main
inputs were already saved, were verified, and required no further change.
