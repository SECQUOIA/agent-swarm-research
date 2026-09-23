# Stage 7, round 1, independent review 04

Date: 2026-09-09. Reviewer: stage07_review04.

## Verdict

**Accept stage 7. No major or minor findings.** This verdict concerns the completed synthesis and the dependencies checked below. It does not replace the separately required whole-manuscript review or certify that no future improvement or unidentified error is possible.

I used no delegation, edited no manuscript or scientific artifact, and read no other reviewer report. I read the supplied global instructions and `literature/AGENTS.md`. The author report was an inventory of assertions to verify, not evidence that they were correct.

## Frozen version and actual scope

I independently verified all 31 files in `process/snapshots/stage07-round01/SHA256.json`; its SHA256 is `8291e480da66a12a69a046e702818c268420be847c4af81b324baca6868ce1b6`. There were no mismatches. I read the complete 504-line recursive diff against `stage06-accepted`, including the abstract, new introduction/contributions, related-work paragraphs, comparison table, roadmap, Section 4 attribution revision, Section 6 attribution revisions, bibliography additions, README changes, coverage changes and new conclusion. I also read the full bibliography, README and coverage map, the model/selection/encoding definitions, all of Section 6, both scalar implementations' relevant construction and upper-solve logic, and the complete full-task comparison test.

I checked the overview against the actual exact theorem, moving-normal/pessimistic theorem, constant-field corollaries, robustness statement and measurement-fiber proof, accuracy theorem/model, and near-identity/condition-dependent theorem statements. The review emphasis was complete scalar response sets, original contacts, upper selection, classical attribution, performance evidence and reproducibility. I have not repeated a complete line-by-line proof audit of all four mathematical appendices in this synthesis review.

## Mathematical and scientific checks

1. **Scope in the introduction and abstract.** The text distinguishes growing total follower dimension from fixed leader, local block, resource and aggregate dimensions; numerical degree from binary degree encoding; and XP-type dependence from fixed-parameter tractability. Constant algebraic degree is limited to the stated constant-local-matrix subclass and a selected output field. The accuracy overview explicitly separates exact base-domain recovery from conditional response-row feasibility. The model paragraph correctly describes one jointly optimizing follower and does not misidentify the nonconvex aggregate as a Nash equilibrium among independent players.

2. **Scalar compression and contact reconstruction.** Strict convexity on a fixed aggregate fiber gives a unique original-coordinate recovery. The multiplier partition has at most `2N-1` nondegenerate aggregate pieces; zero loadings, fixed coordinates and plateau intervals have appropriate separate treatment. Piece endpoints, convex stationary points and flat intervals exhaust tilted minima. All-pair comparisons and the incremental-contact argument retain true ties, including tangencies and isolated domains. Equal winner value polynomials on an open interval have derivatives `gamma*w`, so their recovered responses agree. The proof uses `gamma != 0` where needed.

3. **Convexification.** The supporting-affine-function proof of value equality is sound. The additional equality between original cost and convex envelope is necessary for recovering responses; it is not replaced by mixing exposed endpoints. Both false-convexification and capacity-jump examples are consistent with the actual objective and the implementation. No new convex-envelope construction is claimed.

4. **Both upper problems.** Open response cells are clipped by upper rows while tracking endpoint inclusion. Isolated prices retain all response components. Optimism can select an upper-feasible response, whereas pessimism requires every original response to satisfy all rows and takes least revenue. Affineness of recovery on each flat fiber piece justifies endpoint checks. The compact optimistic graph gives attainment; the pessimistic examples correctly give an unattained supremum. Selected outputs lie in the field of one cut, and the paper does not incorrectly combine unrelated quadratic fields.

5. **Independent baseline.** I checked the minimal-face completeness proof against `original_faces.py`: every nonempty principal minor is validated; only positive-definite free faces are retained; free stationarity and fixed-coordinate gradient signs are imposed correctly, with no gradient sign on a fixed box coordinate. Original dense quadratic substitution supplies candidate values. The full-price partition, all ties and separate upper optimizer are independent of the compressed solver. The nonzero-minor restriction is strong but explicit and sufficient; the code rejects singular cases instead of silently claiming completeness. The exponential enumeration is not presented as scalable.

6. **Conclusion.** It accurately connects response-description dimension, arithmetic output, exact versus approximate feasibility, and path representation versus pointwise evaluation. Its discussion of experiments is consistent with the recorded unfavorable screening outcomes and does not claim industrial superiority or implementation of the general quantifier-elimination algorithms.

## Primary-source checks and novelty

I extracted text directly from local original PDFs and read the relevant original passages, rather than relying on repository source summaries:

- **Gardiner and Lucet (2010), printed p. 471, Proposition 3.1, and p. 478, Proposition 4.3, with surrounding derivations/proof:** quadratic-time/linear-space `plq_coSplit` and linear-time/linear-space `plq_coDirect` are indeed stated for the piecewise linear-quadratic envelope task. The paper's new locators are correct. It calls these arithmetic-time constructions and imports no unproved rational-bit improvement. The direct candidate proof in Section 6 does not depend on the predecessor's tangent formulas.
- **Hladík, Černý and Rada, arXiv:1911.10877v1, pp. 1–3:** the fixed quantity is the rank of the whole quadratic matrix. Section 2 explicitly describes stationary-face enumeration, constancy of the objective on a stationary polyhedron and `3^n` faces. Both the fixed-total-rank comparison and classical-principle attribution are supported. Publication metadata was independently checked on the author's page: [published reference](https://kam.mff.cuni.cz/~hladik/publ/b2hd-HlaCer2021c.html). I did not claim to read the subscription publication in addition to the actual open original.
- **Moehle et al. (2023), Section 6.3 and Appendix B:** the text gives recursive piecewise quadratic envelope construction and attributes its lineage to Gardiner–Lucet. It supports the manuscript's narrow constructive-account citation and comparison-table row. The present proof is self-contained and does not import a source formula without verification.
- **Hochbaum and Shanthikumar (1990), printed pp. 846–847, Sections 1.2–1.3 and Theorem 1.1:** the source explicitly approximates the solution vector, not merely objective value. Its bound depends logarithmically on requested precision and numerically on a subdeterminant bound, in its stated oracle model. The revised introduction and Section 4 give that predecessor proper credit. Global optimization of an independent signed upper objective across all leaders remains a different combined task.

I also made fresh online searches for the Gardiner–Lucet envelope result and the Hladík–Černý–Rada box result, using the primary arXiv record and author metadata to confirm the latter. No search result from a secondary aggregator was used as mathematical authority.

The novelty sentence is qualified and restricted to the exact quadratic-block and global accuracy-bit theorem classes with their specified outputs. It expressly disclaims priority for global comparison, rational multipliers, sparse support reduction, polynomial inversion and real algebraic tools. The comparison table explicitly avoids a general model-subsumption claim. I found no unsupported priority claim within the scalar and computational scope I audited. This is not an exhaustive independent re-search of every mathematical lineage in the 77-page paper; in particular the new Nie-series bibliographic lineage was read as manuscript text and checked for its stated structural distinction, but I did not independently re-read all three full original articles in this review.

## Independent execution and provenance

All new checks and build output are under `verification/stage07-review04/`; existing raw data and historical logs were not overwritten.

- All 31 frozen hashes verified, recorded in `hash-check.json`.
- An isolated build from the 17 actual LaTeX/bibliography/table/figure inputs succeeded: **77 pages**, no undefined references/citations, LaTeX warnings, overfull boxes or underfull boxes. I visually inspected rendered pages 4 and 5, including the new related-work paragraphs and comparison table. Both are readable and fit their pages.
- I reran all **18 full-task comparison cases** via `compare_case`, avoiding the test main's historical-log output path. All passed: exact upper values/attainment, independently partitioned response sets and direct attained-output original-cost/row/witness checks for both methods. Results are in `full-task.log` and `full-task.json`.
- An additional independent invocation checked rejection of a singular principal minor and the compressed solver's flat response at zero price. Equality rows selecting aggregate `1/2` are optimistically attained there and pessimistically infeasible, as required.
- I checked all **60** raw worker records, their success statuses, exactly three repetitions in each of **20** method/instance groups, and relevant median quantities. The displayed heterogeneous and repeated-type counts/timings and qualitative comparisons agree with those records. No timing campaign was run.
- I independently verified all **11 recorded input hashes**, substituting the explicitly preserved measured driver/test/solver versions where documented. Removing exactly the later `constraints = tuple(constraints)` line from the current compressed solver recovers the measured source byte for byte. Thus the README's measured-version qualification is accurate; the current file is not falsely relabeled as the measured version. The data audit is in `data-audit.json`.
- The scripts' repository dependencies are described in the README, while the mathematical manuscript and its build are genuinely standalone. A final submission bundle still belongs to the later completion gate; this draft does not claim that the remaining review gate or packaging is complete.

## Findings requiring correction

**None.** No valid major or minor correction request arose from this review. I do not recommend expanding the manuscript merely to manufacture an additional comparison or a performance claim unsupported by the present evidence.
