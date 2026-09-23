# Independent whole-paper review 05

**Verdict: PASS.** No major or minor finding. This is an independent review of the frozen whole-paper target, not a confirmation of previous verdicts.

## Coverage

The reviewed target is `process/snapshots/whole-round01/main.pdf`, 111 pages, with independently checked SHA256 `912de166731f56368a8ee4db21294aa348b85364e85cd444e31265b29828d084`. All manuscript paths below refer to this snapshot.

I read the complete `main.tex`, `macros.tex`, and `references.bib`, including the abstract, introduction, roadmap, every proof and every bibliography entry. I read all of these files in full:

- `sections/01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`;
- `sections/07-positive-boxes.tex`, `08-exact-complexity.tex`, `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`;
- `sections/13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, `17-synthesis.tex`;
- `sections/appendix-finite-signings.tex`, `appendix-positive-couplings.tex`, `appendix-cubic-certificates.tex`, `appendix-structural-auxiliary.tex`, `appendix-positive-box-predecessors.tex`, `appendix-point-packing.tex`, `appendix-scaling.tex`, `appendix-p-split.tex`, `appendix-rank-one.tex`, `appendix-fbbt.tex`, `appendix-integer-comparison.tex`.

I also read the frozen `README.md`, `process/review-protocol.md`, `process/whole-paper-review-assignment.md`, `process/stage06-reviewer-focus.json`, `process/scope-proposal.md`, `process/claim-coverage.md`, `process/stage-06-author.md`, and `process/stage06-corrections.md`. I checked the ledger against the manuscript, including the scaling catalogue restriction, ownership of high coordinates, and the FBBT nonempty-limit qualifier. I found no omitted required scope item. I did not read another report from this final round, delegate work, or edit the manuscript or snapshot.

After reading `literature/AGENTS.md`, I consulted these primary-source originals at the passages relevant to the manuscript:

- Schoenebeck, *Linear Level Lasserre Lower Bounds for Certain k-CSPs*: the random-instance model, width definition, Theorems 11–12, complete signed-vector construction in Lemma 13, and the random-width argument in the appendix. The freshly downloaded [author PDF](https://schoeneb.people.si.umich.edu/papers/LasserreNew.pdf) has SHA256 `b909449375ade807c55f4992b08ea9c4c57e412605edf947b56a199226c15413`, matching the recorded source. I also inspected the rendered source pages containing the relevant statements and construction.
- Cornuéjols, *Combinatorial Optimization: Packing and Covering*: Theorems 6.5 and 6.13, for the distinct total-unimodularity and balanced-matrix dependencies.
- Davidson–Donsig, *Norms of Schur Multipliers*: Theorems 1.2 and 2.4 and the continuous weighted-density definition in the local author manuscript.
- Potechin, *Sum of Squares Lower Bounds from Symmetry and a Good Story*: Theorem 1, Example 18, and Theorem 44, including the falling-factorial moment convention and source attribution.
- Hassin–Tamir, [*Efficient Algorithms for Optimization and Selection on Series-Parallel Graphs*](https://www.math.tau.ac.il/~hassin/sp.pdf): scanned original pages containing the series-parallel definitions and Theorem 3.1. Text extraction was unusable, so this check was visual.
- Luedtke–Namazifar–Linderoth, *Some Results on the Strength of Relaxations of Multilinear Functions*: the stated scope and the concluding conjecture in the author manuscript.
- Kronqvist and coauthors, *P-split Formulations*: Assumptions 1–4, Remark 1, Definition 4, and Theorem 6 with its proof. The manuscript correctly identifies the shared-domain assumption relevant to its counterexample and repair.
- Lee–Raghavendra–Steurer, *Lower Bounds on the Size of Semidefinite Programming Relaxations*: Theorems 3.8, 5.3, and 5.4 and the relevant displayed quantitative bound.
- Fawzi–Parrilo, *Exponential Lower Bounds on Fixed-Size PSD Rank and Semidefinite Extension Complexity*: Theorem 1 and its fixed-block interpretation.
- Ahmadi–Dash–Hua–Stellato, *Disjunctive Sum of Squares*: Theorem 1 and the finite-tolerance termination statement and Algorithm 2. Beame and coauthors, *Stabbing Planes*: Theorems 1–2 and the split/slab definition. Fleming and coauthors, *On the Power and Limitations of Branch and Cut*: Theorems 1.3–1.4 and the coefficient restriction.

These were targeted source checks, not complete rereadings of every cited paper. No source needed for the additional XOR focus was inaccessible. Limits on the remaining external dependencies are stated below.

## Findings

None. I found no demonstrable error requiring repair.

## Independent verification

### Mathematical reconstruction across the paper

I reconstructed the envelope representation by vertex laws, cell interpolation, signed-cut reduction, and fractional-orientation identities. I checked normalization and inactive mass in the harmonic construction, the tangent mixture, the finite Lambert inequality, and the dyadic/radix constructions. The limiting sharp constant is distinguished from finite attainment. The coefficient-removal argument preserves the relevant normalized quantities.

For the structural results, I checked the high-coordinate ownership argument, the feedback repair distribution, the frequency-two half-integral slab argument and baseline, and the cardinality matching construction. I followed all series and parallel cases of the width-two active/blocking invariant. The positive-box coupling handles restrictions to the ambient box correctly, and the complexity claims distinguish fixed-dimensional evaluation, rational input size, and varying graph size.

For the cardinality lower bounds, I checked the Vandermonde/homogenization positivity argument and the degree available to every product of slacks. Endpoint substitutions in coordinate graph lifts preserve the asserted degree. Tensor positivity uses a principal submatrix indexed by total degree, so it does not silently grant additional degree to each block. The relative-error and explicit-cut statements preserve their stated qualifications.

I checked the supplementary derivations for point packing, scaling, P-splits, rank-one/correlation faces, FBBT, and integer split comparisons. In particular, the scaling proof retains the catalogue and zero-weight restrictions; the P-split counterexample concerns the actual shared domain; exact fixed-block conic lower bounds are not substituted for approximate arbitrary-size SDP bounds; and the FBBT statement does not infer a feasible point from an empty limit. The geometric area/width and parity arguments use the stated disjunction model.

### Additional focus: XOR, quadratic hulls, rank, and order one

The source construction uses signed character moments in `{0, +1, -1}` with support through width `w`, and positivity for squares through degree `floor(w/2)`. I reconstructed the signed equivalence classes rather than relying on the source's typography. The manuscript's normalization and parameter choice are correct despite typographical problems in the source presentation.

The restriction argument is deterministic substitution, not probabilistic conditioning. The product of endpoint indicators is idempotent, and the degree charged to the indicator times the test polynomial is accounted for. This explains the `4r` and `4rD` budgets, including repeated slack localizers.

For the quadratic hull, a PSD Gram matrix with unit diagonal and entries in `{0, +1, -1}` has equal or opposite vectors within a nonorthogonal class and orthogonal vectors between classes. Independent fair signs for the nonconstant classes, with the constant class fixed, reproduce every required first and second moment. This is an actual law on the coordinate box. It need not be a law on the monomial graph, and neither lower nor upper proof assumes that stronger property.

I checked the random-instance deletion arithmetic and quantifiers: deleting clauses incident to overly frequent coordinates preserves the original functional and yields the stated occurrence bound, retained-clause count, and objective gap. The rank argument counts consistent parity restrictions by binary rank, not by the number of restrictions. A basis covers the support of every row, giving `|C| <= Dq`; the witness fraction is exactly `2^(-q)`. The conversion from original variables and clauses to the total lifted coordinate count preserves the exponent `7N/52224` in the order-one corollary.

The order-two grid upper certificate uses cubic corner bounds and graph identities at the available degree. The distinct order-one argument uses the full-box quadratic law and expectation-level graph equations. I checked its nonnegative quadratic polynomial and degree-two certificate identity. The affine-halfspace obstruction preserves all moments tested by the proposed cut, and its final localizer bound is explicitly a limitation of that method.

### Exact computations and build

All independent artifacts are in `verification/reviewer05/whole-round01/`.

- `focus_checks.py` and `focus-checks.json`: exact binary linear algebra and enumeration for all 32,768 families of nonzero rows in dimension four. For every family, enumeration checks the number and sizes of consistent parity fibres and the support/rank bound.
- The same checker verifies the order-one quadratic inequality and identity at 24,256 rational corner/sign cases, using grid counts 1, 2, 3, and 7. It also checks 420 seeded signed-class constructions on 1–14 coordinates by exact enumeration of their sign laws.
- The deletion estimate is checked with integers: `384 * 3^24 = 108452942008704 < 2^64 = 18446744073709551616`.
- I extracted and executed the printed finite-signing and cubic-certificate programs. They passed. The signing counts for dimensions 2–7 were `1, 2, 4, 4, 5, 8`; the cubic program verified the displayed exact rational bounds, including the finite cases and the dimension-16 certificate.
- I copied only the build inputs into `verification/reviewer05/whole-round01/build/` and ran `latexmk` there with an explicit working directory. The build completed with 111 pages and no warning, undefined-reference, or overfull-box matches in the final log. The complete layout-text extraction agrees byte for byte with the frozen PDF's extraction. I do not claim the rebuilt PDF has the same binary hash.

I rendered all 111 frozen pages and visually inspected six contact sheets covering every page. I additionally inspected full-page higher-resolution renders of manuscript pages 70, 73, 74, and 76, covering the additional focus. I saw no clipping, missing material, or layout defect.

## Remaining limits

The finite computations check finite cases and implementations; they do not establish the general theorems. The general arguments above were reviewed mathematically. The signed-class examples are generated valid class patterns, not an exhaustive test of all PSD matrices. The rational corner checks complement, rather than replace, the polynomial proof. I did not run a floating-point optimizer or construct and certify a large random XOR instance.

The all-page contact sheets check gross layout, not every symbol at reading resolution. Source checks establish the relevant statements, conventions, and selected derivations; I did not independently reprove all inherited results, including the complete external SDP-size, fixed-block conic, and proof-complexity lower bounds. I did not authenticate every bibliographic publication detail or the equivalence of anonymous and public Coniglio versions, and I make no comprehensive novelty or priority claim. These limitations do not expose a defect in the paper's stated scope or its locally proved conclusions.
