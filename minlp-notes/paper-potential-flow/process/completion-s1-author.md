# Completion stage S1: foundations and corpus audit

Date: 2026-09-10. Author implementation complete; five independent manuscript reviews and lead assessment remain required. No claim of external peer review is made. No commit or staging operation was performed, and the pre-existing uncommitted A1–A3 work was preserved.

## Scope and concrete changes

- Critically read all three existing foundation sections, approximately 2,270 lines before this stage: general passive-state existence and block structure; cactus nomination-face localization, rational recovery, and both SRS encoders; bounded-block localization, perturbation, real-algebraic optimization, parametric box elimination and recovery, joint sensitivity, and exact arc validation.
- Replaced the long introductory symbol inventories in A02 and A03 with short mathematical roadmaps. Those inventories interrupted the argument before the main results and contained internal stage names such as “A1.” The symbols remain defined where used. A03 now explains why pressure uses interval sums while a single arc admits one polynomial-size algebraic output. A01 now opens with the model/structure/arithmetic purpose and closes with the role of block rank, rather than a list of internal dependency labels.
- Clarified that the joint Lipschitz statement concerns the stated unfiltered product domains.
- Resolved the Canny bibliography issue left in the older A2 record. The paper now cites the exact report version whose Theorem 3.3 was used, with verified UC Berkeley institutional metadata, report number UCB/CSD-88-439, August 1988, and author John F. Canny. The entry no longer mixes report theorem numbering with a disputed STOC page range.
- Created `completion-coverage.md`, mapping all 43 promoted potential-flow results to proposed standalone Paper A uses. The map explicitly includes weighted-cactus, correlated-performance, and output-boundary results previously assigned to Paper B; it distinguishes certificate implementation detail from a missing complexity theorem. It also identifies the supporting approximation and fixed-core notes outside the result glob.

No theorem was weakened to bypass a discovered error. No mathematical flaw requiring a new hypothesis or repaired proof was identified in this author pass. That is an assessment to be tested by the five independent reviewers, not a certification of the full manuscript.

## Corpus and source examination

Read the README, conventions, PROCESS, coverage inventory, and A1–A3 implementation/review records. Compared all 43 result files, 173 matching investigation/review notes, and 73 research Python scripts byte for byte between the worktree and main checkout: all corresponding files were identical, with no main-only or worktree-only item. This is a complete version reconciliation of those sets, not a claim to have audited every later theorem's proof in S1.

For later scope, examined the complexity map and paper-readiness record, result headings throughout the promoted corpus, the general weighted bounded-block obstruction note, the reopened weighted-face reduction, and the rational-witness boundary. Their mathematical claims must be independently developed and reviewed in their writing stages. The coverage table is a proposal, not a completed-coverage declaration.

Rechecked the actual local four-author single-cycle primary manuscript, `literature/papers/labbe2021-deciding-feasibility-of-a-booking/fulltext.md`: rational-data Assumption 6.1; Theorem 6.4's nine variables and 42 constraints; Theorem 6.5; and Corollary 6.6. They support the current A2 comparison. The [author's publication list](https://martin-schmidt.science/publications/) corroborates the final 2021 Networks 78(2):128–152 metadata and four-author attribution. The separate three-author 2020 booking paper must not be substituted for that theorem.

The [official Berkeley report record](https://www2.eecs.berkeley.edu/Pubs/TechRpts/1988/6041.html) verifies Canny's report title, author, institution, number, date, and existential-real PSPACE claim, and supplies the institutional BibTeX entry. The old direct digital-library record returned 403 during this pass. The previously inspected report theorem remains correctly identified in A02. The author's own publication list also lists STOC pages 460–467, but changing to the verified report avoids carrying a version mismatch at all.

The lead independently corroborated the current open SRS status against Ajdarów, Main, Novotný, and Randour, ICALP 2025, DOI 10.4230/LIPIcs.ICALP.2025.138, whose introduction and Section 5 explicitly state no known polynomial-time algorithm and no known NP membership. The foundational SRS citations remain appropriate. The lead is assessing the newly retrieved 2026 literature and final novelty framing separately; no unverified current-priority claim was inserted here.

## Mathematical audit points

- General existence uses a uniform coercive primitive-energy bound, including bounded strictly increasing laws; it does not rely on surjectivity or coercivity only along selected rays.
- Aggregation partitions nominations correctly at articulations, preserves shifted interval boxes, and permits rational disaggregation. Flow or potential filters are not silently included.
- Smoothed KKT/exchange arguments have positive derivative resistances; compactness and uniform convergence remove smoothing without a genericity assumption or an algorithmically chosen perturbation size.
- Cactus threshold faces cover gaps, one/two equal-level vertices, fixed bounds, and lower-dimensional domains. Other block contributions become constants because active pivots have fixed total nomination in one cycle.
- Bounded-block suppression counts and strict internal-source forcing correctly yield at most two level hits per path, including the two-vertex maximum plateau. The two limiting steps are applied to a fixed coarse face before local perturbation.
- Closed sign-cell covers include zero flows and lower-dimensional feasible regions. Algebraic sampling and quantifier elimination remain in fixed dimension; the degree/output bounds depend on fixed rank.
- The box lemma constructs a polynomial formula by enumerating realized signs in fixed dimension, then uses support separation. It recovers many resistance coordinates using fixed-dimensional zonotope vertices and Carathéodory combinations, rather than exponentially enumerating endpoint assignments.
- Joint rounding maintains nomination balance and resistance bounds exactly. Its physical state can leave the original sign cell, which is allowed by the uniform objective estimate. Inactive block fields are not merged.
- Exact arc extrema optimize the arc after using pressure monotonicity only at fixed target resistance. They do not incorrectly substitute a jointly pressure-maximizing resistance for an arc optimizer.
- SRS encoders preserve weak inequalities, exact ties, integer bit lengths, and maximum-degree-three simple cactus structure. SRS-hardness is not presented as NP-hardness. The broader graph-parameter limitation credits the original Thürauf reduction and uses its explicitly encoded gap.

## Verification

All commands ran successfully in the worktree after the manuscript edits:

- `python3 paper-potential-flow/verification/check_a1_preliminaries.py`: 22,236 checks; maximum numerical error 1.103e-28.
- `python3 paper-potential-flow/verification/check_a2_cactus.py`: 47,356 A2 assertions, 75,826 imported A1 assertions; 273 exact/separated encoder comparisons including 55 ties; 28 cactus cases and 168 feasible faces; maximum passive residual 1.075e-30.
- `python3 paper-potential-flow/verification/check_a3_block_rank.py`: 22,417 A3 assertions and 7,354 imported A1 assertions; 200 exact support/LP comparisons, 108 exact Carathéodory recoveries, 17,576 arc-grid scenarios, and 24 capacity decisions including three ties. Maximum finite-difference derivative error 8.778e-16.
- `python3 paper-potential-flow/verification/check_coverage.py`: 308 inventory files and 18 original planned sections. This checker validates the original inventory, not completion of the expanded coverage plan.
- A separate exact filename check confirms every one of the 43 promoted result files occurs in `completion-coverage.md`.
- From `paper-potential-flow/complexity/`: `latexmk -g -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`: successful 50-page partial Paper A PDF. No undefined references/citations, duplicate labels, errors, or overfull boxes. Input hashes and diagnostics are in `completion-s1-build.json`. Paper B was not rebuilt or edited by this stage.
- `git diff --check`: passed.

The numerical searches and finite differences are regression evidence, not implementations of the certified global real-algebraic algorithm. Exact arithmetic tests exercise their specified finite identities and recovery procedures; neither class of check replaces proof review.

## Remaining scope

S1 leaves no identified major foundation issue unresolved. Later sections, abstract, introduction, final bibliography coverage, and whole-manuscript review remain outstanding. The old general weighted bounded-block summation route requires a separate development decision; the cactus case is already resolved by the repository and must be fully written. An unproved Wronskian proposal must not be promoted into a theorem. The known unread nonlinear-tolerance source limits envelope priority claims, and old internal source reviews are not external publication-priority certification.
