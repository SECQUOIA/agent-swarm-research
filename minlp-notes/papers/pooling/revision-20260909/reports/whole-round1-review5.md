# Independent whole-manuscript review 5

**Manuscript:** *The Complexity of Pooling: Algebraic Barriers and Structural Algorithms*.  
**Version reviewed:** frozen `revision-20260909/whole-round1/`, including all material in the 104-page PDF.  
**Verdict:** ready on mathematical substance, with optional editorial improvements. I found no fatal, major, or minor mathematical defect and no required repair. This is a referee assessment, not a formal correctness certificate or a guarantee of acceptance by an unspecified journal.

## Scope and method

I read the complete introduction, Sections 1–6, Appendices A–C, every proof and construction, all figures, `main.tex`, the entire bibliography, and `submission-README.md`. This includes the unnumbered discussion of matrix parameters at the end of Appendix A, the synthesis's open questions and counterexamples, and all assumptions in the two scope tables. The review did not use author, reviewer, or adjudication reports and did not delegate any part of the review. No manuscript file was changed.

The statement-level ledger is [claim-coverage.csv](../checks/whole-review5/claim-coverage.csv): 95 formal theorem, lemma, proposition, corollary, and example environments, each identified by frozen-source file, line, and label. This ledger complements the substantive discussion below; it is not a substitute for proof review. All prose outside those environments was also read.

I independently built a copy of the frozen source using its documented build procedure. It produces 104 pages, with no undefined references or citations and no LaTeX overfull/underfull warnings. Extracted text is identical to the supplied `stage4-corrections-build/source/main.pdf`. The evidence is in [build-summary.json](../checks/whole-review5/build-summary.json), [build-output.txt](../checks/whole-review5/build-output.txt), and the `build/` directory. I inspected the source of all figures and visually inspected the dense scope table on PDF page 62. I did not visually inspect every PDF page.

I checked reduction identities, reconstruction arguments, degeneracies, and complexity bounds directly. One additional independent exact computation checks the signed divergence support machinery; its purpose and limits appear below. Literature verification used original articles, original author preprints, and publisher or author sources. The source ledger distinguishes inspected passages from claims whose complete external proof was not rederived.

## Findings and optional improvements

There are **no required findings**. In particular, I found no unsupported step that changes a theorem's scope, no omitted physical balance needed by a reduction, and no conflation of a real-arithmetic algorithm with the stated bit model.

### WR5-O1 — Optional: add the published Grothey–McKinnon citation

**Locator:** `bibliography.bib:334`, entry `s6:grothey2020`; use at `appendices/A-response-geometry.tex:434`.

The entry accurately identifies the 2020 preprint and its version. A published version is now available: *Annals of Operations Research* 322, 691–711 (2023), DOI `10.1007/s10479-022-05156-7`. Updating the bibliographic record would improve the submission's presentation while preserving a note that the Section 3 locator refers to arXiv version 1. This is not a citation error or a novelty defect: the predecessor is already credited for a small example with many local solutions. The publication metadata and the scope of that predecessor are supported by the [publisher's article](https://link.springer.com/article/10.1007/s10479-022-05156-7).

**Suggested repair:** use the journal entry, DOI, volume, and pages, retaining the explicit preprint-version locator if it is still needed. No proof changes follow.

### WR5-O2 — Optional: make the independent reading routes more explicit

**Locators:** `sections/00-introduction.tex:164–204`; `sections/05-contract-algorithms.tex:102–301`; `sections/06-synthesis.tex:1–14`; `appendices/A-response-geometry.tex:500–553`.

The existing tables, introduction roadmap, and synthesis are useful. The remaining presentation cost is breadth: the article combines algebraic universality, sharply restricted physical hardness, several distinct elimination algorithms, and a substantial independent rank-one convexification contribution. A reader primarily interested in one of these may have difficulty identifying which auxiliary results must be read first.

**Suggested improvement:** add a short dependency-oriented reading guide identifying the main physical classification route and the independently readable Appendix B–C route, and identify the general parametric-path and matrix-parameter discussions as supporting limits on elimination. This could be a few sentences, rather than another large table. Splitting the paper is not necessary to establish correctness, and I do not recommend removing proof detail merely to reduce length. This is optional editorial advice, not an objection to the existing organization.

## Complete mathematical coverage

### Introduction, model definitions, and Section 1

The abstract, headline table, and body distinguish feasibility, rational threshold decision, exact optimization, and uniform convexification. Claims about the number of pools, quality rank, local degrees, bypasses, lower bounds, and objective support are consistent with the cited theorems. The paper does not treat variable quality coordinates at an unused pool as physically meaningful flow witnesses.

I checked destination decomposition, the single-product projection, the physical-flow sign test, the shortest-path extension, conic-hull equality, cyclic reconstruction, and the recognition characterization for universal flow integrality. The treatment of unsupported circulation is substantive: the cyclic physical convention is stated, and circulation terms are not silently identified with source-to-product deliveries. The zero-flow and zero-capacity cases do not break the scaling or reconstruction arguments. The sign theorem is correctly credited as a development of an existing polynomial zero-optimum test, not claimed as a new resolution after Xiang et al.

The facial integrality characterization appropriately concerns universal integrality under the specified flow bounds, rather than asserting integrality for arbitrary pooling sets. Its recognition and bounded-pool algorithm use the characterization at the stated scope.

### Section 2: algebraic complexity and witnesses

I checked the reciprocal emission gadget, every algebraic operation in the conversion, and the forward and reverse physical reconstruction. The saturation argument forces the intended equalities; the emission budget is large enough for the attached uses; and the bounded-data refinement uses explicit polynomial-size replication and conversion. The one-pool construction retains the distinct-summand normalization and handles pins without losing the claimed equivalence.

The witness-field result is more delicate than a generic ETR reduction. The argument uses a compact singleton and retains its original coordinate through rational, uniquely determined auxiliary operations. It does not use an arbitrary compactification or a square-root slack that could invalidate the claimed field preservation. The quadratic irrational example is consistent with this distinction between a threshold witness and an optimizer.

For the basis-index certificate I checked that only a polynomial number of basis indices is guessed, that determinant substitutions yield a fixed-dimensional semialgebraic decision problem, and that degrees and coefficient lengths remain polynomial when the linear fiber dimension grows. The certificate does not require writing an arbitrary high-degree algebraic solution as an NP witness. The bounded pool-count-times-rank and pool-count-times-product-count specializations, and the separate one-pool no-bypass statement, preserve their differing hypotheses.

### Section 3: restricted hardness

I checked the pure-mode construction and its continuous cleanup, including the value-preserving relationship with independent set; the all-four-degrees-two refinement; and the edge-coloring assumption used for the approximation gap. The weighted extension and positive-concentration perturbation explicitly distinguish exact integral behavior from approximation control. The counterexample correctly shows why a strictly positive tolerance is not an exact binary forcing device.

The positive-product reduction is self-contained where the older Matsui statement needs care. The proof bounds the full auxiliary dimension and uses the determinant gap before transferring to positive affine factors. The two-pool realization preserves the exact product comparison. Its approximation algorithm is restricted to the represented subfamily and does not imply an approximation scheme for the strongly hard neighboring families.

I checked the one-pool copy/conversion construction, bounded-coefficient rows, full and half ports, directed cycles with a single upper quality bound, and the source splitting needed for degree control. Exact supplies remain private where the proof requires them. The upper-only reduction pays for constraint violations through a rational error bound with polynomial encoding; it does not assume a numerically constant penalty. The constant-data circuit and two-feed implementation represent the required rational quantities with polynomially many gates. The final five-exception family preserves the exact-contract restrictions outside the explicitly exceptional nodes.

No gate quietly creates an extra attribute, an unbounded supply, an extra pool, or a degree violation that would invalidate the associated theorem. The contrasts between strong NP-hardness, ETR-completeness, and NP membership are maintained.

### Section 4: structural algorithms

The fixed-core theorem retains the necessary pool mass, attribute mass, and objective aggregates in its local support construction. Support enumeration is polynomial for the fixed local and aggregate dimensions. Polynomial degrees are allowed to grow with the instance, but the number of real variables in the subsequent algebraic computation remains fixed. The proof supplies both decision/optimization and a physical lift from the common algebraic field, rather than only an objective value.

The fixed-input, fixed-quality/no-bypass, and bounded bypass vertex-integrity corollaries follow with their advertised parameters. In the latter, small residual components, the retained separator, and the global pool data play different roles; the proof does not pretend that bounding only the number of pools bounds the bypass coupling.

I checked the two planar relation formulas, degenerate and unbounded-slope cases within their bounded feasible domains, balanced path composition, endpoint projection, and reconstruction. The attachment theorem retains only a fixed number of necessary boundary variables. Its optimization extensions explicitly retain objective support or reduce the objective by exact equalities. They do not claim unrestricted dense-profit optimization from an endpoint projection that has forgotten the corresponding flow contributions. The degree-two versus degree-three comparison consequently has a matched and meaningful feasibility scope.

### Section 5: contract and exceptional-node algorithms

I read the entire general one-parameter recursion and affine-strip/tree/cycle-rank results. The first theorem claims quasipolynomial symbolic complexity, not polynomial complexity. The second uses its additional strip structure. Their use in the physical discussion is appropriately qualified.

For exact contracts I independently followed the elimination to signed divergence intervals and the connected-cut conditions, including signs, lower bounds, cycles, isolated components, zero interval widths, and quality endpoints. The quadratic-field feasibility result retains all relevant conservation equations. The common-capacity counterexample is valid and explains why a shared throughput bound cannot be dropped.

The fixed-dimensional quality chart for arbitrary attributes uses the affine relations contributed by contracted nodes and exposes only the stated exceptional dimensions. Empty or degenerate charts are handled through the algebraic formulation. The arbitrary-quality exception theorem requires the stipulated redundant common bounds; later throughput results are not implicitly combined with it.

I checked the symbolic binary path/cycle minimization, the box-truncated base rank, greedy support evaluation, and throughput reconstruction. Signed edge lower bounds and signed node intervals are legitimate throughout. Ties in a supporting cost order and disconnected components do not change the validity of the support test. The rank formula involves all subsets before its efficient path/cycle implementation; it is not an unjustified restriction to connected sets after box truncation.

The two-full-quality-vector theorem is a distinct convex reduction. The transformed quadratic upper bounds have nonnegative capacity multipliers, making the auxiliary `r >= q^2` substitution valid in the required direction. The rational convex QP is a decision and recovery tool, not a generic claim of polynomial exact conic feasibility. The separate endpoint LPs and exact interior test address spurious points of the closed transformed polytope. The zero lower-bound assumptions at outlets and the common resource are essential and appear in the statement. The rational KKT argument supports polynomial-size rational recovery. The extensions retain their exact-supply and resource qualifications.

### Section 6 and Appendix A: response geometry

The synthesis accurately states the implications and the open degree-two bypass question. The shared-helper example exposes a real loss of private source equations. The paper does not infer numerical-solver performance or hardness from a large number of local optima.

I checked the telescoping vertex certificate and its physical path realization; the one-price family and exact penalties; the exponential response and explicit-elimination conclusions; the coordinate-port obstruction; the single-pool vertex-forcing extension; the perturbation producing distinct strict local values; the exact integer-coordinate lower and upper bounds for the finite optimal set; and the compact LP hull. The hull's optimization conclusion follows because the relevant vertices are physically feasible. A compact hull and many isolated physical optima therefore do not contradict each other.

The three-quality/general-supply extension keeps the physical balances. The dense-slab hardness proposition is explicitly an abstract additional coupling result, and the text does not claim an unproved degree-two physical realization. The final discussion of matrix parameters separately treats rank-one signed perturbations and rank-two product constructions. Its elementary exact arguments do not require accepting a broader external hardness assertion without proof.

### Appendix B: isolated rank-one margin costs

I checked the decomposition of a general cost into additive row/column terms plus fixed interaction rank, the chamber/vertex enumeration, the remaining scalar optimization, and quadratic-field recovery. The parameter concerns interaction rank after removing additive terms, which is the economically relevant distinction for the proposed Lagrangian oracle.

The general-cost hardness reduction uses the exact rank-one interval-margin set from the earlier conjecture. The unit-margin repair preserves the threshold implication with the stated coefficient scale. The proof of rational yes witnesses correctly separates stationary optima from boundary points and shows why the existence of an irrational exact optimum need not prevent a short rational threshold witness. The fixed-margin-dimension algorithm handles the remaining scalar parameter without promoting this to an algorithm when both dimensions grow.

These results are not a physical-pooling hardness proof for ordinary additive operating costs. Both the appendix and the synthesis explicitly preserve that distinction. The fixed-attribute Lagrangian result is an isolated-block oracle and does not assert zero duality gap or solve the coupled primal problem.

### Appendix C: exact and approximate convexification

I checked the exposed face and affine correlation-polytope identification, including the unit margins and normalization. The exact LP, fixed-order PSD-block, SOC-dimension, and unrestricted PSD-order consequences use different source bounds and are stated with the appropriate measures of size.

The exposure-and-rounding estimate is applied to convex combinations before the approximation transfer. The total entrywise error convention is explicit; it is not interchangeable with a fixed per-entry error. The outer LP transfer uses the correct correlation relaxation sandwich. For the SDP transfer, I checked the valid-slack factorization step and the quantitative pseudo-density substitution, including the positive shift needed for a strict source hypothesis, the dependence on the odd parameter, and the resulting exponent. The approximate SDP conclusion is weaker than the exact lower bound in the required way. It is not obtained by merely invoking exact extension complexity for a perturbed set.

The lower bounds allow arbitrary real coefficients and concern a representation serving all bounded linear costs. They remain compatible with an exponential exact SOC representation and with useful compact relaxations for particular objectives.

## Primary-source and novelty assessment

The strongest contributions appear substantial and distinct from the inspected predecessors: physical ETR encodings and witness-field consequences; simultaneous degree, alphabet, and contract restrictions in the physical hardness results; exact algorithms that retain the otherwise lost global flow aggregates; the resolution of the isolated rank-one simultaneous-margin conjecture; and the explicit correlation face with a quantitative approximate-conic transfer. The paper's importance does not depend on treating established tools as new theorems.

The following are the principal verified comparisons. Original local PDF paths are recorded in [sources/index.json](../checks/whole-review5/sources/index.json); the extracted passages and independently obtained PDFs are in `checks/whole-review5/sources/`. Source inspection concerned the relevant original passages, not complete reproofs of every external article.

| Primary source and inspected locator | Assessment of the manuscript's use |
| --- | --- |
| Abrahamsen et al., *The Art Gallery Problem is ETR-complete*, Definition 5 and Theorem 7; original PDF | Supplies the bounded ETR-INV source problem with the stated operations and interval. |
| Abrahamsen et al., *A Dynamic Toolbox for ETRINV*, Theorem 1/Corollary 2 and conversion Lemmas C–G | The manuscript's restricted compact-singleton use avoids importing the full compactification step into a field-preservation claim. |
| Haugland, *The Computational Complexity of the Pooling Problem*, Proposition 3, Theorems 1–5 and conclusion; Haugland–Hendrix, *Pooling Problems with Polynomial-Time Algorithms*, Section 4.5/Theorem 4.1 and bypass discussion | The earlier pool-count, input/output-count, and scalar restrictions differ materially from the new simultaneous restrictions. |
| Boland et al., *A Polynomially Solvable Case of the Pooling Problem*, theorem and Section 4 questions | Fixed inputs and omitted bypass coupling are credited. The historical questions are described with their original qualifications. |
| Baltean-Lugojan and Misener, *Piecewise Parametric Structure in the Pooling Problem*, Assumption 2.2 and Remark 4.6 | Broad one-pool capacity hardness was already stated. The manuscript acknowledges it and bases its stronger claim on simultaneous physical restrictions. |
| Gupte et al., *Relaxations and Discretizations for the Pooling Problem*, Section 2.1.1, especially Remark 2.2 | Confirms the historical zero-optimum question; it does not establish novelty after the later Xiang result. |
| Xiang et al., original 2026 proceedings PDF, Proposition 4 and Theorem 2 on PDF page 8 | Confirms one-LP-per-product zero-optimum testing, including pool-to-pool arcs and general arc costs. The manuscript credits it. The source PDF was inspected independently and copied to this review's evidence; [official proceedings](https://ios2026.isye.gatech.edu/refereed-proceedings) confirm the contribution. |
| Chlebík–Chlebíková, Section 5(A), Theorem 19 proof | The source explicitly preserves the needed edge-three-colored cubic restriction in the approximation reduction. |
| Matsui, METR 95-13 original, pages 2–5 | Checked the printed estimate and the manuscript's counterexample to its unrestricted form. The replacement proof in Section 3 supplies the needed determinant gap. |
| Basu–Pollack–Roy, *On the Combinatorial and Algebraic Complexity of Quantifier Elimination*, Section 1.3, Theorems 1.3.1 and 1.3.3 | Supports the fixed-variable polynomial dependence on degree and coefficient length. |
| Adler–Beling, *Polynomial Algorithms for Linear Programming over the Algebraic Numbers*, Section 5, Remark 1 | The manuscript accurately characterizes the rational-machine discussion as an outline and keeps the common extension degree polynomial. |
| Schrijver, *Combinatorial Optimization*, Corollaries 11.2i and 11.3a, printed pages 175–176 | Confirms signed arc/node interval feasibility, integrality, and max-flow recovery. I extracted these pages directly from an original book PDF, without reading any accompanying review. |
| Shioura–Shakhlevich–Strusevich, Theorems 1–2, printed page 192 | Confirms the box-truncated submodular rank and greedy support framework. The manuscript proves its base-total specialization. [Original article PDF](https://eprints.whiterose.ac.uk/id/eprint/78189/10/shakhlevich1.pdf). |
| Kozlov–Tarasov–Khachiyan | The original publication and translation metadata were verified at [MathNet](https://www.mathnet.ru/eng/zvmmf5189), and exact polynomial binary complexity is stated by the [publisher's abstract](https://www.sciencedirect.com/science/article/pii/0041555380900981). The full Russian PDF was not obtained in this review; its numbered paragraph locators were not independently verified. The manuscript's rational KKT recovery argument was checked directly. |
| Gärtner et al., *Large Shadows from Sparse Inequalities*, Section 4 | The shadow is established prior work; the manuscript supplies and appropriately claims the physical realization. |
| Boveroux et al., Section 3.1 and Section 3.3 | The original preprint's positive-product and one-column parameter observations are relevant; the manuscript gives its own signed rank-one two-LP reasoning. [Original PDF](https://orbi.uliege.be/bitstream/2268/345162/1/OntheComplexityofLinearProgramswithparametricConstraintMatrices.pdf). |
| Dey–Kocuk–Santana, Section 3.1 after Theorem 4 | The conjecture is indeed linear optimization over rank-one matrices with simultaneous row and column bounds. Appendix B addresses that exact set. |
| Jalilian–Kocuk, published Theorem 2 and Lemma 1; corresponding local preprint theorem | The exact SOC construction is generally exponential, so the new lower bounds are compatible. The version-sensitive theorem numbering in the bibliography is appropriate. [Published original PDF](https://research.sabanciuniv.edu/id/eprint/52174/1/Improved.pdf). |
| Fawzi–Parrilo, Theorem 1 | Supports exponential correlation-polytope lower bounds for products of PSD blocks of fixed order. |
| Lee–Raghavendra–Steurer, full original, Theorem 1.1, Theorem 3.8/equation (3.11), and Theorem 5.3 | Supports the exact unrestricted PSD bound and the quantitative machinery used in the separate robust bound. |
| Braun–Fiorini–Pokutta–Steurer, Section 4.1, Theorem 6(i) | Supports the fixed-factor correlation-relaxation sandwich used for the approximate LP transfer. |

The local file named for Dey–Gupte's *Analysis of MILP Techniques for the Pooling Problem* contains presentation slides, not the journal article. I treated it as contextual material and did not use it as original-article proof verification. Other local formulation and algorithm articles were used for context; their entire external proofs were not audited. This limitation does not leave an unproved essential step in the manuscript: its relevant physical constructions are supplied in full, and the principal novelty comparisons above were verified in original articles.

The targeted search did not identify an earlier physical ETR-completeness result contradicting the manuscript's novelty positioning. This is not an exhaustive certification against all unpublished or obscure work. The assessment rests on the specific primary comparisons above and the manuscript's appropriately qualified language. In particular, the 2026 Xiang and Jalilian sources were not ignored because they postdate the older local literature.

## Independent computational evidence and limits

[check_divergence_support.py](../checks/whole-review5/check_divergence_support.py) is one coherent independent check of the signed incidence/box-rank/greedy/DP chain, not a collection of duplicate test counts. It generates 60 small path and cycle systems with signed integral edge and node bounds, enumerates every feasible integral edge flow, evaluates the rank formula for every vertex subset, and compares exact rational-cost support values and greedy attainment. A separate binary dynamic program checks the subset-minimization value, including directed-edge orientation and cycle closure. All comparisons pass; see [check_divergence_support.json](../checks/whole-review5/check_divergence_support.json).

Because the incidence systems with these integral interval bounds are integral, enumeration determines their linear support values exactly. The cases include collapsed intervals, negative lower bounds, cost ties, and both path and cycle components. They corroborate the algebraic signs and implementation-independent identities on the tested systems. They do not prove the symbolic piece-count bounds, cover every degenerate physical instance, or replace the mathematical proof.

The build evidence establishes a complete, reproducible submission source independent of the external literature repository. No solver benchmark or implemented general algorithm is claimed by the article, and I do not regard their absence as a defect in this theoretical contribution. Exact arithmetic claims were reviewed at the proof and encoding-bound level; the manuscript has not been formally verified in a proof assistant.

## Journal readiness

The article has a coherent thesis: physical pooling complexity depends on both algebraic mixing and the linear network information that can be eliminated without loss. The detailed constructions support that thesis, and the appendix results explain why description size, local geometry, cost structure, and uniform convexification must be separated. The writing is careful about theorem boundaries and supplies counterexamples at several tempting but invalid extensions.

Its principal editorial risk is the 104-page breadth, not a missing technical foundation. A theoretical optimization journal willing to consider a long article could review the present manuscript on its substance. No venue was specified, so I have not inferred a page-limit, anonymity, or formatting violation from a generic article-class submission. The optional citation update and reading-guide improvement would make the submission easier to assess, but this review identifies no mandatory mathematical or expository repair before submission.
