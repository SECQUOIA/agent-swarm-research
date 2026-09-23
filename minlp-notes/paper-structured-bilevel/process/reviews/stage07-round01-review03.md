# Stage 7, round 1, independent review 03

Reviewer: stage07_review03. Date: 2026-09-09.

**Verdict: accept this synthesis stage. Major issues: none identified. Minor issues requiring correction: none identified.** This verdict is for the specified stage; it does not replace the subsequent full-manuscript review.

## Integrity and scope

I verified the frozen `stage07-round01/SHA256.json` hash as `8291e480da66a12a69a046e702818c268420be847c4af81b324baca6868ce1b6` and independently verified all 31 file hashes. I compared the stage 7 files against `stage06-accepted`, read the entire new abstract, Section 1 (including the unchanged definitions underlying its summaries), comparison table, roadmap, conclusion, bibliography additions, README and coverage record, and the Section 4/6 citation changes. I did not read other reviewers' reports or use the root literature assessment as authority. I read the user-supplied AGENTS instructions and the local literature instructions; no repository-root or manuscript-local AGENTS.md exists.

My additional mathematical review read Section 5 and Appendix D, including the dense and near-identity reductions, conditioned grid, growing-leader transfer and mixed-radix construction, bounded-core algorithm, both path constructions, padding and output obstructions. I checked the summaries against the exact, pessimistic and robustness theorem/corollary statements and the accuracy model and theorem. This stage did not include a complete new line-by-line audit of every proof in Sections 2–4 and Appendices A–C; that remains part of the separate whole-paper gate.

## Scientific assessment

The introduction states a coherent central question: whether fixed shared dimensions suffice despite a growing number of local follower choices. It explains the distinction between one jointly optimizing follower and independent agents. Its five contribution paragraphs identify complete guarantees rather than claiming the underlying arrangement, multiplier, quantifier-elimination or conjugacy tools as new. The table caption expressly avoids asserting that the cited models are subsumed. The qualified novelty sentence is limited to the combined theorem classes and outputs. I found no unsupported priority claim in the new synthesis.

The exact summary respects the important qualifications: numerical degree rather than binary exponent length, fixed structural dimensions rather than FPT, fixed-normal optimistic attainment versus general attainment decisions, and a selected common field rather than a compositum of unrelated adversarial witnesses. Its constant-Hessian refinement matches the fixed-normal corollary; the separate robust corollary does permit moving shared/measurement normals while the local KKT matrices remain constant. The approximation summary states exact base feasibility and conditional response-dependent upper feasibility separately. The abstract is compact, but the next sections supply the explicit assumptions it summarizes.

The boundary overview and conclusion match the proofs I checked:

- The constant-gap dense reduction has a positive weighted triangular Gram Hessian and conditional minority/shortfall readouts. The Boolean-witness gradient margin dominates both feedback terms, and rounding yields the zero-versus-two gap without upper response rows.
- The near-identity reduction needs coordinate-relative error. Its diagonal scaling, nilpotent inverse bound, feedback inequality, bounded upper coefficients and exponentially small polynomial-bit gap fit together. The resulting exact/accuracy-bit hardness does not imply a constant-gap or strong-hardness result; the text explicitly says so.
- The conditioned grid uses saturation slabs and a maximum-minor row basis to remove numerical incentive-magnitude dependence. Its error is normalized by the upper follower coefficient one-norm, and its polynomial dependence is on inverse accuracy and K. The projected-gradient and rational-reconstruction argument supplies the claimed exact follower output. This is consistent with the near-identity hardness result.
- The growing-leader classification is explicitly transferred from prior work. The independent mixed-radix construction uses a continuous rounding gap, so it does not rely on unsupported discretization of leader inputs. Polynomial duplication preserves the bounded-coefficient claims.
- Leader-interaction paths and follower-constraint paths are consistently distinguished. The leader-path message examples prove representation growth separately from the weak-hardness reduction. The follower-path reduction retains its essential nonconvex upper row. Padding preserves original cube vertices and the exposing response inequality while only fixing the local constraint alphabet; the slab and rescaled costs retain variable binary data.
- Appendix D attributes the sparse shadow, proves the particular exposure formula used, and separates full-representation lower bounds from pointwise O(n) evaluation. Equal-gain projection is correctly restricted to objectives in retained states. The arithmetic subsection distinguishes common-field degree from radical expression size and does not call Square Root Sum NP-hard.

I found no contradiction between these statements and the new contribution/conclusion prose. The coverage map retains the distinct source developments rather than silently replacing the dense constant-gap theorem with the near-identity theorem, or replacing the original contact analysis with convexification. Its continuous-bilevel scope explains the excluded pooling and binary cut material.

## Primary-source checks and literature limits

I refreshed the following actual sources, independently of repository audit conclusions:

1. [Ketkov–Prokopyev, v2](https://arxiv.org/html/2511.15592v2): checked the current June 10, 2026 version, model, Assumption A1, Tables 1–2 and Theorem 4. Their optimistic convex-quadratic positive result fixes follower dimension and has the stated convex quadratic upper structure. Their universal pessimistic convention and total-row parameter do not invalidate the manuscript comparison.
2. Sugishita–Carvalho: read the local original v2 PDF's opening/model and theorem context, and checked the [published IPCO chapter metadata](https://link.springer.com/chapter/10.1007/978-3-032-28691-8_28). The single-leader unit-box/no-additional-upper-constraints comparison is accurate. The published chapter is dated June 13, 2026; the separate v2 citation retains the proof-version locator. I did not obtain the subscription chapter full text.
3. [Froese–Grillo–Hertrich–Stargalla, v3](https://arxiv.org/html/2509.22849v3): checked the actual continuous clique-gap argument in Proposition 4.1, Theorem 5.3 and Corollary 5.5. Its polynomially bounded spike locations and two-input neurons support the manuscript's capped-ReLU transfer. Attribution is explicit in both the theorem proof and new overview.
4. Gärtner–Helbling–Ota–Takahashi: converted and read the local original PDF, Section 4, especially Definition 11 and Lemma 12, and refreshed its [arXiv record](https://arxiv.org/abs/1308.2495). The coefficients and parity exposure formula in Appendix D match that source. The manuscript does not present this shadow as new.
5. Hochbaum–Shanthikumar: read the local original PDF Sections 1.2–1.3 and Theorem 1.1. It already approximates the solution vector, with numerical subdeterminant dependence and the stated oracle model. The revised Section 4 comparison correctly credits this stronger predecessor result.
6. Gardiner–Lucet: read the actual local original around Propositions 3.1 and 4.3. The quadratic and linear time statements cited in Section 6 are correct. Calling them arithmetic-time constructions is appropriate; the manuscript does not claim a faster convex-envelope algorithm.
7. Chen–Ji–Zhang: checked the local source's abstract/model and stated oracle task. The introduction's contrast between approximate stationarity and the manuscript's global bit task is appropriate.

I also ran independent web searches for near-identity scalar-leader quadratic hardness, fixed-rank/separable bilevel complexity with growing follower dimension, and accuracy-bit complexity for separable polynomial followers. I used primary sources for conclusions, not aggregators returned by those queries. These bounded searches did not uncover a theorem that contradicts the scoped comparison. They cannot prove absence of all prior work; the manuscript's qualified wording is therefore necessary and appropriate. I did not independently reread every publication cited in the bibliography, including all newly added Nie-family papers, in this focused review.

## Standalone and presentation verification

I copied exactly 17 manuscript inputs from the frozen snapshot into `verification/stage07-review03/standalone/`: the main source, seven section files, four appendices, bibliography, contact PDF and three table inputs. A clean independent latexmk/pdfLaTeX/BibTeX build succeeded and produced 77 pages. The final log contains no warnings, undefined references/citations, overfull boxes or underfull boxes. I inspected the rendered comparison-table page; the table is readable, fits the page, and its references and roadmap render correctly. The LaTeX build does not require process records, internal notes, code or literature originals.

Evidence, original-source text extractions and the standalone build are retained only in `verification/stage07-review03/`. No manuscript, bibliography, raw measurement or solver file was edited. I did not rerun or alter performance experiments; stage 7 changes neither their sources nor their data.

The stage should proceed to the required full-manuscript gate. This acceptance is a reasoned review conclusion, not a guarantee of journal acceptance or proof that future improvements are impossible.
