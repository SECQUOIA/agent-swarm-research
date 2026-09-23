# Stage 7, round 1, independent review 5

Reviewer: `/root/stage07_review05`  
Date: 2026-09-09  
Snapshot: `process/snapshots/stage07-round01`  
Manifest SHA-256: `8291e480da66a12a69a046e702818c268420be847c4af81b324baca6868ce1b6`

## Verdict

**Accept stage 7 after one minor terminology correction. No major issue found.**

The synthesis presents a coherent research contribution for an optimization-journal readership. It explains why tractability of an individual follower solve does not settle global upper optimization, distinguishes the growing primal dimension from the fixed dimension of its response description, and separates exact algebraic output from approximation in accuracy bits. The abstract, contribution paragraphs, comparison table and conclusions agree with the theorem statements and proof interfaces I checked. The paper does not claim that established multiplier arrangements, value comparisons, inverse approximation, convex conjugation or real-algebraic algorithms are new.

This is the stage 7 synthesis gate, not a substitute for the separately required whole-manuscript review. The latter must still review every proof and the complete computational material.

## Findings

### R5-1 — Minor: use “follower variables” in the arithmetic contribution

**Location:** `sections/01-foundations.tex:53`, the exact-global-responses contribution paragraph; compiled page 2.

The phrase “independent of the number of followers” should read “independent of the number of follower variables” (or explicitly name the number of local blocks). The introduction has correctly specified one jointly optimizing follower, and Corollary 2.9 states independence from the number of follower variables. Referring to the number of strategic followers here is inconsistent with that model and can obscure what grows in the theorem.

**Required fix:** replace this occurrence of “number of followers” with “number of follower variables.” No theorem or proof change is needed. References to independent scalar followers in explicitly decoupled examples need not be changed on this basis.

**Major findings:** none.  
**Other minor findings:** none.

## Manuscript and scientific integration checked

I read the entire stage 6 accepted to stage 7 round 1 diff, all new abstract/introduction/contribution/related-work/table/roadmap/conclusion prose, the complete bibliography, README and coverage record. I read the surrounding model, semantics and encoding definitions and traced the important summary claims into the actual manuscript, rather than relying on the author’s report or past reviews. In particular:

- **Exact compression:** Theorem 2.1, the local-branch and polynomial-size arguments, the common denominator, the two-copy global comparison, joint optimal sampling, the fixed-normal compactness proof, Theorem 2.7 and Corollary 2.9. The claimed polynomial regime bound is in fixed compressed dimension; the construction does not enumerate a Cartesian product of independent statuses. The universal comparison tests actual feasible costs and retains global ties. Constant-degree output needs constant local KKT matrices, exactly as the introduction qualifies it.
- **Robustness:** Theorem 3.1 and its complete measurement-fiber and separate-criterion proof, and Corollary 3.3. The nominal value is global; a threshold-feasible fiber candidate is sufficient without treating every near-optimal point as stationary. Separate elimination of each criterion avoids a growing collection of quantified adversaries. The one-witness/common-field qualification survives the synthesis. The screening summary says that `M 3^t` counts recovery LPs after screening, not total running time.
- **Accuracy:** Theorem 4.1 and its model, polynomial substitution and final proof; the candidate/recovery interface and its true-response comparison across nonlinear branch boundaries; the outer/inner theorem and tightening/anchor statements; and the complete Appendix C response-modulus proof. The summary does not import the more general exact model’s moving normals or nonconvex aggregate into the convex accuracy theorem. Rational recovery preserves the base polytope, whereas response-dependent upper feasibility is qualified. The sharpness assertion is about the exponent for the class and is witnessed by `x^(1/P)`; it is not a universal priority claim about Hölder regularity.
- **Boundaries:** The near-identity theorem and complete scaling/error proof, the conditioned-grid theorem and its initial saturation argument, and the specific restrictions named by the synthesis. The exact-hardness and inverse-accuracy statements are compatible. The introduction retains the nonconvex upper quadratic row in the path result and credits the growing-leader and sparse-shadow classifications. It does not infer pointwise hardness from representation size.
- **Computation and conclusion:** The changed envelope and stationary-face attribution paragraphs, their surrounding algorithm specifications, and the scope of the reported experiments. The conclusion preserves original contact reconstruction, attained versus unattained upper values, separate heterogeneous versus repeated-type scaling, and the unfavorable screening comparison. It explicitly distinguishes proof-based general complexity from finite implementation evidence.

The paper is long, but that length is consistent with the user’s comprehensive scope and the substantial supporting proofs. The opening supplies a useful organizing question and the contribution overview has theorem references. The table identifies differences without claiming that this manuscript subsumes every cited model. The conclusions explain what the results establish and where the mathematical assumptions matter, without asserting that all broader research questions are solved. I found no need for a structural rewrite at this gate.

## Independent primary-source checks

I read `literature/AGENTS.md` and used originals as the authority. I did not read other stage 7 reviewer reports or use an author audit as a substitute for these checks.

1. **Megiddo–Tamir (1993):** extracted the local `original.pdf` and read the block/multiplier construction, especially original manuscript pages 7–8. The text explicitly bounds each local hyperplane family using fixed local variable and row counts and obtains polynomially many intersections in fixed multiplier dimension. This supports the attribution of the arrangement principle. The present introduction appropriately frames its contribution as the complete primal-elimination/global-bilevel guarantee, not the first polynomial arrangement count. The original PDF extraction has damaged mathematical glyphs; I relied on the readable prose for this limited comparison, not on a reconstruction of unreadable formulas.
2. **Hochbaum–Shanthikumar (1990):** read the local original’s Sections 1.2–1.3 and Theorem 1.1, printed pages 846–847, with the subsequent explanation of oracle accuracy. They expressly approximate the solution vector and give logarithmic accuracy dependence with numerical subdeterminant dependence. The revised Section 4 and related-work paragraph now describe this accurately. No unsupported claim that response approximation is new remains in those paragraphs.
3. **Gardiner–Lucet (2010):** read the local original around Propositions 3.1 and 4.3, printed pages 471 and 478. They supply quadratic-time and linear-time envelope constructions, respectively, with linear space. Section 6 credits those results and does not claim an asymptotic improvement. The additional bilevel obligation is to preserve the original contact set and upper selection/feasibility, not simply the tilted value.
4. **Nie–Ye–Zhong (2026):** independently opened the primary [arXiv v2 manuscript](https://arxiv.org/html/2304.00695v2), read Sections 1.1–1.2 and 2.2–2.3, including formula (2.9), Proposition 2.3 and Theorem 2.4. Their support size uses the rank of the whole constraint matrix and their retained variables include the primal follower. This directly supports the paper’s distinction between global-rank multiplier support and fixed local-block primal elimination. I also verified the journal volume, issue and pages against [Jane Ye’s publication list](https://janeye.ca/publications/). I did not inspect the paywalled published article against the open version.
5. **Ketkov–Prokopyev (2026):** independently read [v2 Theorem 4 and its setup](https://arxiv.org/html/2511.15592v2). Its optimistic convex-quadratic result fixes follower dimension and assumes the stated positive-semidefinite upper/follower matrices. The introduction describes that result accurately and does not confuse a fixed total row count with a fixed shared row count plus growing local bounds.
6. **Recent adjacent work:** checked the primary [Chen–Ji–Zhang v4 abstract and version history](https://arxiv.org/abs/2511.22331v4) and the author-submitted [Flocco–Schiewe–Gabriel entry](https://optimization-online.org/2026/06/nested-benders-decomposition-for-large-scale-multi-follower-bilevel-optimization/). The former studies approximate stationarity/oracle complexity; the latter has linear followers decoupling at a fixed leader. These primary descriptions support the narrow comparisons made in Section 1. I did not re-review their full algorithmic proofs.

I also searched online for fixed/separable quadratic bilevel complexity and the named PLME/envelope predecessors. That bounded search found no evidence contradicting the precisely scoped novelty statement, but it cannot prove literature-wide absence. The manuscript’s “To the best of our knowledge” language and explicit restriction to combined theorem classes are appropriate. The other bibliography entries were read for consistency and rendering; they were not all independently re-retrieved in this stage 7 review.

## Reproducibility, build and visual checks

Evidence is in `verification/stage07-review05/`.

- Independently verified every one of the **31** snapshot manifest entries. There were **zero mismatches**; the manifest hash matches the assigned snapshot. `hash-check.json` records the result.
- Copied only the **17 manuscript build inputs** into `isolated/`: `main.tex`, bibliography, seven sections, four appendices, one PDF figure and three generated table inputs. No repository notes, process records, review files or external literature were available as relative build dependencies.
- Ran a fresh `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex`. It completed successfully, yielding **77 pages**. The final TeX log has no warnings, overfull boxes, undefined citations or undefined references. Build output is retained in `isolated/build-run.log` and `isolated/build/`.
- Rendered and visually inspected pages **1, 2, 5, 58, 59, 75 and 77**, covering title/abstract, contributions, complete comparison table, conclusion, transition to appendices and representative bibliography pages. Text, rules, citations and mathematical symbols were legible; no clipping or layout defect was found.
- Read the README’s source-version and timing provenance distinctions. No solver or raw experiment data changed in stage 7; the diff confirms the preserved code/data hashes. I did not rerun timing experiments or numerical tests for prose-only changes.

The clean manuscript build independently substantiates the claim that the mathematical paper and LaTeX sources stand alone. Reproduction of some computational diagnostics still intentionally uses repository code, as the README says; the conclusion does not misrepresent those diagnostics as an independent general quantifier-elimination implementation.

## Scope limits

This review checks the synthesis and selected mathematical dependencies in depth. It is not a fresh line-by-line review of all 77 pages, every reduction, the whole inverse-approximation appendix, or every solver branch. I make no claim of formal verification, exhaustive novelty proof, or guaranteed journal acceptance. The required stage 8 whole-manuscript review remains necessary. Within the stage 7 scope, R5-1 is the only correction I request.
