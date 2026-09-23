# Stage 6, round 1 — independent review 08

**Verdict: PASS.** No demonstrable major or minor defect identified. This is a stage review, subject to the reading and verification limits below; it does not replace the separate final whole-paper review.

## Coverage

I reviewed the frozen manuscript in `process/snapshots/stage06-round01`. I independently computed the SHA256 of its 111-page `main.pdf`: `343b29156e275df970236babbab1077b3a53261317e0995a6a7ea0398b583916`.

I read `main.tex`, `macros.tex`, and `references.bib`; every main source file, namely `01-foundations.tex`, `02-universal-positive.tex`, `03-cubic-equal-means.tex`, `04-incidence-interiority.tex`, `05-feedback-frequency.tex`, `06-treewidth-two.tex`, `07-positive-boxes.tex`, `08-exact-complexity.tex`, `09-cardinality-spatial.tex`, `10-cardinality-preordering.tex`, `11-coordinate-domains-lifts.tex`, `12-relative-blocks-cuts.tex`, `13-xor-quadratic-hulls.tex`, `14-monomial-reformulations.tex`, `15-finite-certificates-affine.tex`, `16-supporting-comparisons.tex`, and `17-synthesis.tex`; and all eleven appendices: `appendix-cubic-certificates.tex`, `appendix-fbbt.tex`, `appendix-finite-signings.tex`, `appendix-integer-comparison.tex`, `appendix-p-split.tex`, `appendix-point-packing.tex`, `appendix-positive-box-predecessors.tex`, `appendix-positive-couplings.tex`, `appendix-rank-one.tex`, `appendix-scaling.tex`, and `appendix-structural-auxiliary.tex`. These paths are under the frozen `sections/` directory.

I read the frozen review protocol, Stage 6 review and author assignments, author record, scope proposal and claim-coverage ledger, README and PROCESS, and consulted the frozen build report. I also read the three canonical notes `notes/common-factor-p-split-correction.md`, `notes/common-factor-p-split-balls.md`, and `notes/common-factor-p-split-rotation-gap.md`. I did not read other reports from this round or use prior verdicts as evidence. I read `literature/AGENTS.md` before opening local originals.

The full manuscript reading was of the TeX, including proofs and bibliography. Visual PDF inspection was targeted: manuscript pages 1, 4, 97–100 and 105–111, and published P-split PDF pages 15–16. The inspected pages were readable, without clipped formulas or broken cross-references. I did not visually inspect every PDF page or rerun LaTeX.

Primary-source checks were as follows. Page numbers are PDF pages unless explicitly marked printed.

- Kronqvist–Misener–Tsay, package `literature/papers/kronqvist2026-p-split-formulations-a-class/original.pdf`, SHA256 `0122c8371b2d7114dddc6e01de3408295438864b94970fbb65d71857b5aaf46d`: original pp. 4–7 for assumptions, global bounds and retained-domain formulation, and pp. 15–16 for Corollary 3, Definition 4, Theorem 6 and its proof. Also consulted package fulltext at the relevant statements, including Theorem 4.
- Fawzi–Parrilo, local original p. 3, Theorem 1 and the Lorentz-cone discussion; Lee–Raghavendra–Steurer author full version `/tmp/minlp-relaxation-limits-sources/lrs-sdpsize.pdf`, p. 23, Theorem 3.8/equation (3.11), and pp. 32–34, pseudodensity construction and Theorems 5.3–5.4; Braun et al. author version `braun2013-approxlp.pdf` in that same temporary source directory, p. 18, Section 4.1 and Theorem 6(i).
- Balas, local original PDF pp. 5–7, printed pp. 7–9, Theorem 2.1 and proof; Starr, temporary author source `starr1969.pdf`, PDF pp. 12–13, printed pp. 35–36, Appendix 2, Lemma 2, corollary and proof; Wu et al., local original p. 12, Lemma 3 and Theorem 3. Wu's supplemental proof was not inspected.
- Etessami–Yannakakis, temporary author source `ey-rmc.pdf`, relevant circuit normalization and amplification argument on pp. 26–28; Esparza–Kiefer–Luttenberger, local original p. 34, Section 7, equation (14), Theorem 7.1 and proof; Stewart et al., local original pp. 21–22, Section 4.1, equation (18) and its convergence discussion.
- Schoenebeck, temporary author full version `schoenebeck-full.pdf`, statements of Theorems 11–12 and Lemma 13 and the main local vector construction around pp. 7–11; Cornuejols, temporary author manuscript `cornuejols-packing-covering.pdf`, Theorems 6.5 and 6.13, printed pp. 76 and 82. These were targeted dependency checks, not complete external proof audits.
- Khajavirad, [arXiv:2404.03091v1](https://arxiv.org/html/2404.03091v1), formulation/domain definitions and Propositions 1 and 3: the statement values and applicable sizes agree with the manuscript. I reconstructed the manuscript's supplied certificates separately.

## Findings

None. In particular, the source correction is supported by an example satisfying the published retained-box formulation, and the replacement proposition states sufficient assumptions rather than claiming an unwarranted equivalence.

## Independent verification

### P-split correction and local repair

In `appendix-p-split.tex`, Example `ex:psplit-exact-box` (PDF p. 98), I checked the box `[0,3] × [-1,1]` and disjuncts `t²+w² ≤ 1` and `(t−3)²+w² ≤ 1`. The defining quadratics are strictly convex, and the retained disjuncts are disjoint because their first-coordinate ranges are `[0,1]` and `[2,3]`. Together they contain all four box vertices, so their convex hull is exactly the retained box. Consequently, any valid convex relaxation contained in that box is already exact. The explicit shared lift `(a,b,c)=(3t,9−3t,1)` is a convex combination of the two valid endpoint lifts; its epigraph inequalities follow from `t(3−t) ≥ 0`. The weighted transverse-square extension preserves strict convexity and the same vertex argument in every stated dimension.

The published Theorem 6 proof uses strict Jensen improvement at a component even when the two endpoints have the same argument for that component. Strict convexity does not supply that improvement. Its subsequent neighborhood argument also needs feasibility in the retained domain. These are real gaps in the published proof, and the manuscript's example additionally disproves the stated universal conclusion; it is not merely an objection to one proof. The manuscript correctly distinguishes strictly convex defining functions from strictly convex truncated sets.

For Proposition `prop:psplit-repair`, I reconstructed both requirements: convexity plus inclusion of all original feasible points gives inclusion of the entire hull, while the support direction produces a strict exterior point. Every zero-slack link is explicitly protected by the directional assumption. Each positive-slack link remains feasible for a sufficiently small step by continuity, and finiteness of the link family gives one common positive step. The separate retained-domain condition prevents the published boundary failure. No differentiability assumption is being used implicitly.

### Exact translated-ball geometry

For Proposition `prop:psplit-balls` (PDF pp. 98–99), write `U=(d+r)²` and `c=Σc_i`. At fixed `c`, the two auxiliary boxes have residual budget `h=r²−c`; their convex hull is the square `0≤a,b≤U` cut by `a+b≤U+h`. This gives the displayed full auxiliary hull with `c≤r²`. Its downward closure permits replacement of all auxiliary variables by the actual coordinate squares. Completing the square gives exactly

`||w||² ≤ r²`, and `2(t−d/2)²+||w||² ≤ 2(d/2+r)²`.

These inequalities also imply the retained longitudinal interval, so dropping its redundant display does not enlarge the projection. Grouping all transverse coordinates produces the same residual-budget calculation even though its original box upper bound differs. The hierarchy application is restricted to the original box and its additive bounds.

I independently maximized distance to the capsule. With `s=||w||²`, the left endpoint is `t=−e(s)`, where `e(s)=sqrt((d/2+r)²−s/2)−d/2`. The squared distance to the center is `e(s)²+s`, whose derivative is `1/2+d/(4sqrt((d/2+r)²−s/2))>0`. The maximum is therefore at `s=r²`, giving exactly the stated Hausdorff error; the limiting factor is `sqrt(2)−1`. This also checks the geometric endpoint used in the proof.

For Proposition `prop:psplit-rational` (PDF p. 100), I checked the orthogonal rational matrix with rows `(3,4)/5` and `(4,−3)/5` and the witness `(2D,4D/3)`. Its aligned coordinates are `(34D/15,4D/5)`. The original-coordinate auxiliary midpoint dominates all true-square links, giving the stated growing lower bound. The aligned retained-domain relaxation has transverse radius at most one and the claimed uniform upper bound. The transformed diamond/parallelogram is retained; no invalid box hierarchy is invoked after rotation.

For Proposition `prop:psplit-exact-image`, every convex auxiliary set containing both center images contains their midpoint, so the same witness survives even exact auxiliary-image convexification in the original coordinates. In aligned coordinates, the concave decreasing function `d²+1−c+2d sqrt(1−c)` gives the two valid hypographs. Combining them with the actual epigraph links yields precisely the capsule cross-section. The converse follows from validity and convexity. I also checked the displayed second-order-cone representation and the distinction between the auxiliary image and the full graph.

### Whole-manuscript checks

I reconstructed the main chains outside the assigned focus rather than treating them as accepted prerequisites. Checks included the signed induced-cut cell vertices and polarization/Khinchine loss; positive harmonic normalization with inactive mass; dyadic cutoff and coefficient-removal concentration; the cubic scalar minorant and mixtures; the width-two elimination invariant and Camion application; positive-box scaling and ambient coefficient spreading; the narrow-box PARTITION reduction and accuracy scale; fractional-cardinality Gram coefficients, indicator localizers and tensorized spatial certificates; XOR parity closure, degree budgets `4r` and `4rD`, and the separate order-one upper identity; and the midpoint/parity-class integer comparison and its constants.

For the Stage 6 additions, I reconstructed the point-packing certificates; the compact rectangular-fibre criterion for scaling and its zero-scale cases; the perspective product-weight construction with its stated block assumptions; correlation rounding constants `136m+10` and section-transfer constant `m(184m+6)`; the differing exact LP, fine-accuracy PSD and fixed-cone consequences; and both FBBT constructions. In the latter, the least-fixed-point argument uses fairness and soundness, the detector distinguishes the two arithmetic-circuit cases, and the stronger-initialized primitive invariant prevents inverse updates from bypassing the repeated affine increments. The specified directed component bounds and distinction from undirected treewidth are preserved.

### Independent computations

The standalone checker is `verification/reviewer08/stage06-round01/check.py`; its output is `check-results.json` in the same directory. It passed.

- Exact rational vertex enumeration checked nine auxiliary polytopes, with one, two and three transverse components and three choices of `(U,r²)`. The respective vertex counts were 8, 11 and 14 for each parameter choice; every enumerated vertex belonged to one of the two defining disjunctive pieces.
- Exact rational arithmetic checked 651 retained-box lift points and the rational rotation witness at `D=2,7/3,10,100`.
- Numerical sampling at 1,001 radii for each of `(d,r)=(3,1),(10,2),(100,1)` agreed with the monotonicity and endpoint Hausdorff formulas. These samples supplement the analytic derivative above.
- I replayed the complete printed cubic-certificate program and complete-signing program directly from the frozen appendices. The cubic checks passed and the signing maxima were `[1,2,4,4,5,8]`.

These computations test finite instances and executable assertions; they do not establish any universal theorem.

## Remaining limits

This was a complete reading of the integrated manuscript, with targeted fresh checks of primary sources. It was not a fresh reading of every cited work in its entirety. In particular, the full external proofs of the rank lower bounds, random-XOR width input and balanced-matrix theorems were not re-proved. The manuscript's reductions from their stated inputs were checked. An attempted text search in the available Hassin–Tamir PDF returned no searchable match, so I do not claim a fresh original-source verification of its cited theorem. The Coniglio review-version/published-version identity remains explicitly unverified, as the manuscript already states. I did not independently reopen every older classical source or complete a bibliographic priority audit.

The manuscript's listed open questions remain open; I found no place where the reviewed text silently promotes one to a theorem. The scope ledger and the new supporting appendices are consistent about the limits of pointwise widths, spatial certificates, lift size, propagation work and integer precision. Finite checker success, the existing build report and earlier stage status are not substitutes for proof. No manuscript or frozen snapshot was edited.
