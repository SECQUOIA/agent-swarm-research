# Literature, novelty, and citation review — round 1

**Verdict: minor revision in this review area.** I found no novelty blocker and no demonstrated false attribution in the citation sample. The contribution is credible as certificates and exact feasibility results for specific stored models, together with an audit that resolves bound conflicts by proved existence. It should not be described as the first benchmark-bound audit, the first MINLPLib certification effort, or a new general certification mechanism. The manuscript mostly observes these distinctions already.

The six issues below concern the scope of negative statements, the numerical standard of a close precedent, recent related work, and citation precision. They do not require changing the reported numerical results. This review does not assess the correctness of the new mathematical proofs or checking programs.

Reviewed `main.tex`, `supplement.tex`, their included sections, the existing rendered PDFs, `references.bib`, the three L1–L3 literature syntheses, and the source passages in the 53-entry ledger below. Paths in issue locations are relative to `paper-open-minlplib/`. Source page numbers are physical PDF pages represented by `<!-- page N -->` in local `fulltext.md`, unless a printed page is explicitly identified. This matters for author manuscripts with different pagination from the final publication.

## Numbered issues

1. **minor — Bound two categorical negative statements to the evidence.**

   **Locations:** `sections/01-introduction.tex:157`; `sections/D-literature.tex:171`.

   **Problem:** “None of these libraries certifies nonlinear dual bounds” is a current, library-wide negative assertion supported mainly by historical library descriptions. “No source treats the model without taps” is also broader than the documented search. The global search disclaimer helps, but these sentences should carry the qualification themselves. This is an evidential scope problem; I did not establish a counterexample to either statement.

   **Evidence:** Shcherbina et al., `shcherbina2003-benchmarking-global-optimization-and-constraint/fulltext.md`, p. 6, distinguish approximate from verified results and explicitly plan updates using verifying global solvers. Gleixner et al., `gleixner2021-miplib-2017-data-driven-compilation/fulltext.md`, pp. 22–25, describe solution checking and comparison of inconsistent solver results; that does not establish the present contents of every nonlinear benchmark library. The manuscript itself distinguishes the tapped and tap-free stored models at `sections/D-literature.tex:165–174` and acknowledges unavailable older power-system work at line 226.

   **Concrete fix:** Replace the first sentence with “The benchmark records inspected in our search do not supply independently checkable nonlinear dual-bound certificates.” Replace the second with “In the search described in this supplement, we found no source treating this exact tap-free stored model.” Preserve the distinctions between benchmark records, rigorous results obtained by research solvers, and the exact model variant.

2. **minor — State the numerical verification standard of the closest MINLPLib certificate precedent.**

   **Location:** `sections/01-introduction.tex:159`.

   **Problem:** The 17-of-67 statement and the convex/nonconvex distinction are correct. Because this paper uses “certificate” for exact or outward-rounded verification, the comparison would be clearer if it also stated how Halbig et al. constructed and checked their certificates. A reader should not have to infer that their computational verification has the same arithmetic standard as this paper.

   **Evidence:** Halbig et al., `halbig2024-computing-optimality-certificates-for-convex/fulltext.md`, p. 18, §4.3 and Algorithm 3, verify planes through optimization and check integer freeness of a polyhedron. Page 32, §8.1, says the underlying optimization problems are solved using Gurobi 10.0.2; p. 33 reports 17 certificates for 67 selected convex instances. The mathematical certificate framework is a genuine precedent and should retain full credit.

   **Concrete fix:** Add one sentence: “Their computational construction and verification solve the auxiliary optimization problems with Gurobi; here we require exact or outward-rounded verification on the stored nonconvex models.” Do not replace the accurate 17-of-67 claim or suggest that the earlier mathematical certificates are invalid.

3. **minor — Bring rigorous interval global optimization coverage up to date.**

   **Locations:** `sections/01-introduction.tex:166`, `sections/01-introduction.tex:173`; `sections/B9-ann-kan.tex:116`.

   **Problem:** The classical provenance is covered well, including Ninin et al. (2015). The discussion largely stops before recent developments directly relevant to reliable affine/Taylor relaxations, transcendental operations, and certified per-box LP bounds. An MPC reader should see how the present instance certificates relate to current rigorous solvers as well as their historical ingredients.

   **Evidence:** Araya, Messine, Ninin, and Trombettoni, *Hybridizing two linear relaxation techniques in interval-based solvers*, printed pp. 437–442, especially §§2.1 and 2.4, combine ART and X-Taylor in interval solvers and certify LP-derived bounds by post-processing. Section 2.1 explicitly relaxes equality constraints for the IBBA/IbexOpt runs. This provides relevant context without establishing an earlier exact-feasibility certificate for any of the 43 stored models. [Publisher full text](https://link.springer.com/article/10.1007/s10898-024-01449-2).

   **Concrete fix:** Add two or three sentences about this recent work near the existing affine/Taylor discussion. Explain that reliable lower-bound machinery is established, while the present contribution combines instance-specific bounds with proofs of exact feasibility on the stored models. Keep the equality-relaxation distinction explicit. No additional solver campaign is needed for this literature correction.

   ```bibtex
   @article{araya2025-hybridizing-two-linear-relaxation-techniques,
     author = {Araya, Ignacio and Messine, Fr{\'e}d{\'e}ric and
               Ninin, Jordan and Trombettoni, Gilles},
     title = {Hybridizing two linear relaxation techniques in interval-based solvers},
     journal = {Journal of Global Optimization},
     year = {2025},
     volume = {91},
     number = {2},
     pages = {437--456},
     doi = {10.1007/s10898-024-01449-2}
   }
   ```

4. **minor — Connect the audit to recent exact MIP certification and numerical-correctness work.**

   **Locations:** `sections/01-introduction.tex:160–167`; `sections/02-semantics.tex:44`; `sections/06-points.tex:46`.

   **Problem:** VIPR and the exact rational MIP lineage are credited correctly. However, recent work on safe propagation and certification from floating-point solver output is especially relevant to the paper's contrast between finding a result and checking it. Hoen et al. (2025) is already cited for input semantics and point repair, but its broader numerical-correctness investigation belongs in the reliability discussion too.

   **Evidence:** Hoen et al., `hoen2025-analyzing-the-numerical-correctness-of/fulltext.md`, pp. 4–6, §§2.2–2.3, discuss repairing solutions and checking numerical decisions after solving. Borst, Eifler, and Gleixner (2024), pp. 6–8, §3, treat certified constraint propagation and dual proof analysis in exact MIP. [Author manuscript](https://optimization-online.org/wp-content/uploads/2024/03/complete-1.pdf). Szeider (2026), pp. 52:1–52:2, constructs VIPR certificates using black-box floating-point ILP solvers, separating the solver oracle from rational certificate construction. [Publisher record and paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2026.52).

   **Concrete fix:** Add a compact paragraph referencing Hoen et al. and the two works below. Distinguish exact linear MIP/ILP certification from the present nonlinear, sometimes transcendental, certificate obligations. These sources do not establish an earlier report of the specific SCIP nonlinear propagation defect, nor a prior rigorous closure of these stored MINLP models. Do not broaden the paper's novelty claim to “first independent solver verification.”

   ```bibtex
   @misc{borst2024-certified-constraint-propagation-and-dual-proof-analysis,
     author = {Borst, Sander and Eifler, Leon and Gleixner, Ambros},
     title = {Certified Constraint Propagation and Dual Proof Analysis
              in a Numerically Exact {MIP} Solver},
     year = {2024},
     eprint = {2403.13567},
     archivePrefix = {arXiv},
     primaryClass = {math.OC},
     doi = {10.48550/arXiv.2403.13567},
     url = {https://arxiv.org/abs/2403.13567}
   }

   @inproceedings{szeider2026-vipr-certificate-construction-from-black-box-ilp-solvers,
     author = {Szeider, Stefan},
     title = {{VIPR} Certificate Construction from Black-Box {ILP} Solvers},
     booktitle = {32nd International Conference on Principles and Practice
                  of Constraint Programming (CP 2026)},
     series = {Leibniz International Proceedings in Informatics (LIPIcs)},
     volume = {379},
     pages = {52:1--52:14},
     year = {2026},
     publisher = {Schloss Dagstuhl -- Leibniz-Zentrum f{\"u}r Informatik},
     doi = {10.4230/LIPIcs.CP.2026.52}
   }
   ```

5. **minor — Identify source versions in page-specific citations.**

   **Locations:** `sections/01-introduction.tex:23`; `sections/01-introduction.tex:153`; `sections/D-literature.tex:229`.

   **Problem:** The statements are supported, but their locators are ambiguous when the bibliography describes the published article and the checked text is an author manuscript. The Vigerske citation uses a physical PDF page, whereas the slides display another number.

   **Evidence:** Vigerske, `vigerske2014-towards-minlplib-2-0/fulltext.md`, physical p. 38, displays slide 23/26 and contains the quoted warning about bound correctness. Bestuzheva et al., `bestuzheva2025-global-optimization-of-mixed-integer/fulltext.md`, p. 23, §3.3, supports the failed-run comparison with MINLPLib; the final journal article has printed pages 287–310. The supplement already discloses that author manuscripts were used, but readers following a particular page citation still need its version.

   **Concrete fix:** Use “slide 23 (PDF p. 38)” for Vigerske. Use “§3.3, author manuscript p. 23” for Bestuzheva, or substitute the verified page in the final journal version. Apply the same convention to other page-specific citations based on preprints. Section and table numbers are preferable where stable across versions.

6. **minor — Make the seminar report's editorial role and the relevant contribution explicit.**

   **Locations:** `references.bib:213–221`; `sections/01-introduction.tex:163`.

   **Problem:** The four people stored in the report's `author` field are identified as editors in the source. The specific discussion supporting the feasibility-tolerance statement is Timo Berthold's contribution. Citing the whole report is defensible, but the present metadata and unlocated citation hide that attribution.

   **Evidence:** `bonami2018-designing-and-implementing-algorithms-for/fulltext.md`, p. 1, labels Bonami, Gleixner, Linderoth, and Misener “Edited by”; p. 8, printed p. 71, §3.6, attributes *Numerical Challenges in MINLP solvers* to Berthold and discusses stopping outer approximation at the allowed feasibility violation. Title, report number, venue, year, page range, and DOI agree with the source.

   **Concrete fix:** Record the editorial role in the BibTeX entry using the project's supported style, and cite “Berthold's contribution, §3.6, p. 71” in the text or citation locator. If the bibliography style requires an `author` field for an edited journal report, retain its rendering convention but add an explicit note identifying the editors and the contribution. This is an attribution refinement, not a claim that the reported observation is wrong.

## Novelty and priority audit

The following register covers the substantive novelty and absence-of-prior-work claims, grouping repeated formulations. Ordinary uses of “first” for an algorithm step, “new variable,” and chronological descriptions of the authors' own implementations are not priority claims.

| Location | Claim and finding |
|---|---|
| `sections/01-introduction.tex:80`; `sections/03-results.tex:76` | No earlier rigorous certificate for the 31 stored models, explicitly limited to the documented search. No counterexample found. This is a search result, not proof of historical priority. Retain the qualification. |
| `sections/01-introduction.tex:91–92`; `sections/06-points.tex:74` | Classical existence tests; new exact points and separately written re-proofs. Supported as a claim about the present exact definitions and verification artifacts. Some numerical candidates come from earlier listed points: do not rephrase this as first discovery of the approximate trajectories or first implementation of these existence tests. |
| `sections/01-introduction.tex:97`; `sections/03-results.tex:91` | No retrievable waterno2 closure, with three unread sources and no priority claim for period decomposition. Appropriately cautious. The unread computational results prevent a categorical first-result assertion. |
| `sections/01-introduction.tex:99`; `sections/D-literature.tex:196–199` | Earlier floating-point closures of ann_cumene_exp are acknowledged; the paper's own lower bound is weaker. This prevents an inappropriate new-closure claim. |
| `sections/01-introduction.tex:117`; `sections/D-literature.tex:39` | First systematic screen of listed per-solver bounds **settled by proving exact feasibility**, within the search. Vigerske already cross-checked solver bounds (slides, physical pp. 38–39); Neumaier et al. already studied incorrect solver answers (pp. 12–14). The added exact-existence criterion is essential. No earlier screen meeting that criterion was identified. |
| `sections/01-introduction.tex:124`; `sections/08-solvers.tex:98` | Specific nonlinear propagation defect not previously reported, dated issue-tracker search. No matching prior report identified in the public material inspected. This is narrower than a claim of the first numerical SCIP defect. Retain “to our knowledge” and the date; a public tracker search cannot exclude private reports. |
| `sections/01-introduction.tex:157` | Library-wide absence claim: qualification needed; issue 1. |
| `sections/01-introduction.tex:159` | Halbig et al.'s 17 convex certificates credited correctly. Clarify computational verification standard; issue 2. |
| `sections/01-introduction.tex:164` | Contrast with the enumerated earlier benchmark/reliability studies is supported by the inspected passages. Read “these studies” as those just cited, not all existing work on verification. Hoen et al. would improve this discussion; issue 4. |
| `sections/01-introduction.tex:170–177`; `sections/04-split.tex:122` | Explicitly classical mechanisms and instance-specific novelty. Supported by the decomposition, sufficiency, discrete comparison, safe LP/SDP, interval, and SOS sources in the ledger. Exact arithmetic and outward rounding themselves are not novel. |
| `sections/03-results.tex:48`; `sections/B3-camshape.tex:302–303` | Exact camshape value/proof for four stored models distinguished from floating-point closures and related copies. No earlier exact certificate found. The qualification and stored-model identity are necessary; missing Octeract logs remain a limitation. |
| `sections/05-other.tex:179` | Cut mechanism expressly not new. No unsupported general method claim. |
| `sections/05-other.tex:251` | Hessian and safe LP tools classical; per-period construction is the application contribution. Consistent with the decomposition and safe-bound sources. |
| `sections/05-other.tex:290` | HVYCRASH: no prior source establishing the same model/global result or feasible point found. The literature table and unavailable original references limit this claim. A SIF comment/reference value is not a rigorous feasibility or global-optimality proof. |
| `sections/05-other.tex:326` | Taylor methods classical; kernel moments, minimax LP, and checked leaves are specific constructions. Acceptable; recent ART/X-Taylor work should be discussed (issue 3). |
| `sections/B1-lnts-lukvle10.tex:136–137`; `sections/B1-lnts-lukvle10.tex:321` | Classical sufficiency; attaining-control construction and scalar-root enclosure specific to the stored models; no earlier rigorous result found in the search. Earlier floating-point lnts closures are acknowledged. |
| `sections/B2-dtoc5-optcdeg2.tex:88`; `sections/B2-dtoc5-optcdeg2.tex:353` | No earlier rigorous stored-model certificate found. Waki et al.'s numerical sparse-SDP results and listed Gurobi/MINOTAUR results do not establish such a certificate. The local Waki extraction drops the equations, so this review did not independently establish exact DTOC5 model identity from that text. Retain unread original-source and model-copy limitations. |
| `sections/B7-eg.tex:75` | No earlier rigorous dual certificate found, bounded search. Go et al.'s floating-point eg_int_s closure is explicitly credited. No conflict identified. |
| `sections/B8-waterno2.tex:141–143` | Priority waived for period decomposition and cellwise slopes. Correct treatment of Ghaddar et al. and other pump-scheduling work. Full computational results of the unread sources remain unresolved. |
| `sections/B9-ann-kan.tex:116` | Reliable affine relaxation/weak-duality method expressly credited to Ninin et al. Ninin pp. 15–16 support it. Karia et al.'s floating-point KAN results are separately credited; they do not certify exact feasibility of the stored decimal model. |
| `sections/D-literature.tex:47–60` | Explicit bounded-search rule, no priority assertion for unread sources, and distinction between rigor and prior floating-point closure. Appropriate and important. “No earlier rigorous result found” remains compatible with “earlier epsilon-global result possible but unconfirmed.” |
| `sections/D-literature.tex:127` | No camshape800 global result found, read under the supplement's stated search scope. No counterexample identified. |
| `sections/D-literature.tex:171` | Tap-free-model absence claim: qualify locally; issue 1. |
| `sections/F-eg-rounding.tex:282` | “New code” describes the checking artifact, not a claim of a new mathematical certification method. No literature objection. |
| `sections/11-conclusion.tex:63` | Conclusion retains priority limits and unread-source qualifications. Consistent with the evidence. |

## Coverage and online search

The existing coverage is adequate in breadth: MINLPLib, MIPLIB, QPLIB, COCONUT, PAVER, COPS/CUTEst; solver reliability studies; interval verification; exact LP/MIP and VIPR; safe LP/SDP post-processing; and the relevant instance families. The main gap is current work that connects these traditions, addressed by issues 3 and 4. I do not recommend inflating the bibliography with every interval package or general global-optimization survey.

Online searches included recent verified global optimization and interval linear relaxations; exact MIP/VIPR certificates and certified propagation; MINLP numerical correctness; benchmark curation; and combinations of rigorous/certified/verified with camshape, lnts, lukvle10, dtoc5, optcdeg2, hvycrash, ex6_2_5, ex6_2_7, waterno2, and the ANN/KAN model families. The three recommended additions have primary-source links and metadata above. None of the inspected online hits established a prior rigorous certificate for the exact stored models claimed here. Search non-results cannot establish nonexistence.

Two further relevant works were screened: Elloumi et al., *Global solution of quadratic problems using interval methods and convex relaxations*, JGO 91 (2025), 331–353, DOI 10.1007/s10898-024-01370-8; and Eifler and Gleixner, *Safe and Verified Gomory Mixed-Integer Cuts in a Rational Mixed-Integer Program Framework*, SIAM J. Optim. 34 (2024), 742–763, DOI 10.1137/23M156046X. They reinforce the requested coverage update but are not necessary additional citations if the concise revisions above are made. Their full texts were not included in the 53-source local full-text sample. [Elloumi publisher abstract](https://link.springer.com/article/10.1007/s10898-024-01370-8), [Eifler institutional publication record](https://www.htw-berlin.de/forschung/online-forschungskatalog/publikationen/publikation/?eid=15459).

The Ghaddar pump-scheduling paper has an indexed institutional PDF and an indexed publisher introduction. Direct full-PDF retrieval timed out; publisher access was inconsistent. Its computational results were not read and it is not counted in the full-text sample. An indexed document is not evidence that every result has been examined. The manuscript's waiver of decomposition priority and its unresolved instance-level status should therefore remain. I also did not resolve the unread GLOPEQ/handbook results for ex6_2_5 and ex6_2_7.

## Citation and bibliography check ledger

Each of the following 53 cited sources was opened as local `fulltext.md`, and the listed source passages were compared with the manuscript claim. This is a passage-level check, not a claim to have read every page of every source. “Supported” concerns the statement identified in the row; it does not validate the new paper's results or infer rigor from a numerical benchmark table.

For all 53 bibliography entries, I inspected author names, title, venue or source type, year, and DOI when present against local source material and publication information. Metadata status **R** means an additional successful DOI-registry lookup (38 entries); **S** means no DOI is supplied in the bibliography and source/preprint/thesis metadata was used (7 entries); **L** means the local comparison was completed but independent DOI retrieval failed or was rate-limited (8 entries). Thus 45 entries have the additional registry/source check, and 53 have the local check. An L does not assert that the DOI is wrong. The editorial-role refinement in issue 6 is the only concrete metadata concern found in this sample.

Physical PDF pagination is used below; DOI links use the spellings in `references.bib` so the checked entries can be identified exactly.

| # | Cited source and local full text | Manuscript location checked | Source pages | Passage check | Bibliography check |
|---:|---|---|---|---|---|
| 1 | [bussieck2003-minlpliba-collection-of-test-models](../../../../literature/papers/bussieck2003-minlpliba-collection-of-test-models/fulltext.md) | `sections/01-introduction.tex:5` | 2–4 | Model collection, sources, and benchmark purpose: supported. | R; 2003; [DOI](https://doi.org/10.1287/ijoc.15.1.114.15159) |
| 2 | [vigerske2014-towards-minlplib-2-0](../../../../literature/papers/vigerske2014-towards-minlplib-2-0/fulltext.md) | `sections/01-introduction.tex:153` | 38–39 | Non-verified dual bounds and corroboration by other solvers: supported; locator refinement in issue 5. | S; 2014; no DOI supplied |
| 3 | [koch2011-miplib-2010-mixed-integer-programming](../../../../literature/papers/koch2011-miplib-2010-mixed-integer-programming/fulltext.md) | `sections/01-introduction.tex:155` | 8–11 | Arbitrary-precision rational solution checking with tolerances and input-data interpretation: supported. | R; 2011; [DOI](https://doi.org/10.1007/s12532-011-0025-9) |
| 4 | [gleixner2021-miplib-2017-data-driven-compilation](../../../../literature/papers/gleixner2021-miplib-2017-data-driven-compilation/fulltext.md) | `sections/01-introduction.tex:155` | 22–25 | Point checking, numerical inconsistencies, and curation: supported; no inference of nonlinear certificate availability. | R; 2021; [DOI](https://doi.org/10.1007/s12532-020-00194-3) |
| 5 | [bussieck2014-paver-2-0-an-open](../../../../literature/papers/bussieck2014-paver-2-0-an-open/fulltext.md) | `sections/01-introduction.tex:155` | 5, §3.3 | Automatic detection/analysis of inconsistent benchmark bounds: supported. | R; 2014; [DOI](https://doi.org/10.1007/s10898-013-0131-5) |
| 6 | [gould2015-cutest-a-constrained-and-unconstrained](../../../../literature/papers/gould2015-cutest-a-constrained-and-unconstrained/fulltext.md) | `sections/01-introduction.tex:156` | 1–2, 7–8 | Testing environment and reference/residual information: supported. | R; 2015; [DOI](https://doi.org/10.1007/s10589-014-9687-3) |
| 7 | [furini2018-qplib-a-library-of-quadratic](../../../../literature/papers/furini2018-qplib-a-library-of-quadratic/fulltext.md) | `sections/01-introduction.tex:156` | 17–20, 28–29 | Quadratic model library, formats, provenance, and solution checks: supported. PDF includes preceding referee replies. | R; 2019; [DOI](https://doi.org/10.1007/s12532-018-0147-4) |
| 8 | [shcherbina2003-benchmarking-global-optimization-and-constraint](../../../../literature/papers/shcherbina2003-benchmarking-global-optimization-and-constraint/fulltext.md) | `sections/01-introduction.tex:156` | 4, 6–8 | COCONUT collection and approximate/verified status: supported; current universal absence claim needs qualification (issue 1). | L; 2003; [DOI](https://doi.org/10.1007/978-3-540-39901-8_16) |
| 9 | [halbig2024-computing-optimality-certificates-for-convex](../../../../literature/papers/halbig2024-computing-optimality-certificates-for-convex/fulltext.md) | `sections/01-introduction.tex:159` | 18, 32–33 | Convex certificates for 17 of 67 instances: supported; Gurobi-based computational verification noted (issue 2). | R; 2024; [DOI](https://doi.org/10.1287/ijoc.2022.0099) |
| 10 | [neumaier2005-a-comparison-of-complete-global](../../../../literature/papers/neumaier2005-a-comparison-of-complete-global/fulltext.md) | `sections/01-introduction.tex:161` | 12–14 | False global/infeasibility answers and need for proved feasibility: supported. | R; 2005; [DOI](https://doi.org/10.1007/s10107-005-0585-4) |
| 11 | [nowak2008-lago-a-heuristic-branch-and](../../../../literature/papers/nowak2008-lago-a-heuristic-branch-and/fulltext.md) | `sections/01-introduction.tex:116` | 8 | Wrong BARON root bound on bayes2_10: supported. | R; 2008; [DOI](https://doi.org/10.1007/s10100-007-0051-x) |
| 12 | [vigerske2017-scip-global-optimization-of-mixed](../../../../literature/papers/vigerske2017-scip-global-optimization-of-mixed/fulltext.md) | `sections/01-introduction.tex:116` | 20 | Exclusion of runs with wrong dual bounds: supported. | R; 2018; [DOI](https://doi.org/10.1080/10556788.2017.1335312) |
| 13 | [montanher2018-a-computational-study-of-global](../../../../literature/papers/montanher2018-a-computational-study-of-global/fulltext.md) | `sections/01-introduction.tex:162` | 6, 12, 17 | Benchmark classification/counting of incorrect global-solver claims: supported. | R; 2018; [DOI](https://doi.org/10.1007/s10898-018-0649-7) |
| 14 | [bestuzheva2025-global-optimization-of-mixed-integer](../../../../literature/papers/bestuzheva2025-global-optimization-of-mixed-integer/fulltext.md) | `sections/01-introduction.tex:23` | 23–24, §3.3 | Failures judged against MINLPLib bounds/reference results: supported; author-manuscript locator (issue 5). | R; 2025; [DOI](https://doi.org/10.1007/s10898-023-01345-1) |
| 15 | [bonami2018-designing-and-implementing-algorithms-for](../../../../literature/papers/bonami2018-designing-and-implementing-algorithms-for/fulltext.md) | `sections/01-introduction.tex:163` | 1, 8 (printed 71) | Numerical/tolerance concerns: supported by Berthold §3.6; editorial-role refinement (issue 6). | L; 2018; [DOI](https://doi.org/10.4230/DagRep.8.2.64) |
| 16 | [kearfott2003-globsol-history-composition-and-advice](../../../../literature/papers/kearfott2003-globsol-history-composition-and-advice/fulltext.md) | `sections/01-introduction.tex:166` | 1, 4, 7, 10–13 | GlobSol, rigorous interval computations, and existence tests: supported. | R; 2003; [DOI](https://doi.org/10.1007/978-3-540-39901-8_2) |
| 17 | [kearfott2011-interval-computations-rigour-and-non](../../../../literature/papers/kearfott2011-interval-computations-rigour-and-non/fulltext.md) | `sections/01-introduction.tex:166` | 1, 5, 9, 14 | Rigorous interval methods distinguished from non-rigorous optimization: supported. | R; 2011; [DOI](https://doi.org/10.1080/10556781003636851) |
| 18 | [neumaier2004-complete-search-in-continuous-global](../../../../literature/papers/neumaier2004-complete-search-in-continuous-global/fulltext.md) | `sections/01-introduction.tex:166` | 33–35, 63–68 | Complete-search/interval global-optimization provenance: supported. | L; 2004; [DOI](https://doi.org/10.1017/s0962492904000194) |
| 19 | [neumaier2004-safe-bounds-in-linear-and](../../../../literature/papers/neumaier2004-safe-bounds-in-linear-and/fulltext.md) | `sections/01-introduction.tex:166` | 1, 12 | Directed-rounding safe LP and integer-programming bounds: supported. | R; 2004; [DOI](https://doi.org/10.1007/s10107-003-0433-3) |
| 20 | [jansson2006-vsdp-verified-semidefinite-programming](../../../../literature/papers/jansson2006-vsdp-verified-semidefinite-programming/fulltext.md) | `sections/01-introduction.tex:166` | 1, 4–5, 8–12 | Verified semidefinite-programming bounds from numerical candidates: supported. | S; 2006; no DOI supplied |
| 21 | [jansson2007-rigorous-error-bounds-for-the](../../../../literature/papers/jansson2007-rigorous-error-bounds-for-the/fulltext.md) | `sections/01-introduction.tex:166` | 1–3, 6, 12 | Rigorous SDP error/bound post-processing: supported. | R; 2007; [DOI](https://doi.org/10.1137/050622870) |
| 22 | [domes2009-gloptlab-a-configurable-framework-for](../../../../literature/papers/domes2009-gloptlab-a-configurable-framework-for/fulltext.md) | `sections/01-introduction.tex:166` | 1–2, 18–19 | Configurable rigorous quadratic constraint-satisfaction framework: supported. | R; 2009; [DOI](https://doi.org/10.1080/10556780902917701) |
| 23 | [vanaret2014-certified-global-minima-for-a](../../../../literature/papers/vanaret2014-certified-global-minima-for-a/fulltext.md) | `sections/01-introduction.tex:166` | 1–3, 5–7 | Certified minima of difficult nonlinear test functions: supported; not a general MINLPLib audit. | S; 2014; no DOI supplied |
| 24 | [applegate2007-exact-solutions-to-linear-programming](../../../../literature/papers/applegate2007-exact-solutions-to-linear-programming/fulltext.md) | `sections/01-introduction.tex:167` | 1, 3–6 | Exact rational linear programming: supported. | R; 2007; [DOI](https://doi.org/10.1016/j.orl.2006.12.010) |
| 25 | [cook2011-an-exact-rational-mixed-integer](../../../../literature/papers/cook2011-an-exact-rational-mixed-integer/fulltext.md) | `sections/01-introduction.tex:52` | 1, 3 | Exact rational MIP and rational input interpretation: supported. | R; 2011; [DOI](https://doi.org/10.1007/978-3-642-20807-2_9) |
| 26 | [cook2013-a-hybrid-branch-and-bound](../../../../literature/papers/cook2013-a-hybrid-branch-and-bound/fulltext.md) | `sections/01-introduction.tex:167` | 1, 5, 38 | Hybrid branch-and-bound with safe/exact verification procedures: supported. | R; 2013; [DOI](https://doi.org/10.1007/s12532-013-0055-6) |
| 27 | [cheung2017-verifying-integer-programming-results](../../../../literature/papers/cheung2017-verifying-integer-programming-results/fulltext.md) | `sections/01-introduction.tex:167` | 3–4, 7–10 | VIPR sequential proof format and independent checking: supported. | R; 2017; [DOI](https://doi.org/10.1007/978-3-319-59250-3_13) |
| 28 | [eifler2023-a-computational-status-update-for](../../../../literature/papers/eifler2023-a-computational-status-update-for/fulltext.md) | `sections/01-introduction.tex:52` | 3–4 | Exact MIP computational update, rational-data repair, and VIPR: supported in local conference manuscript. | R; 2023; [DOI](https://doi.org/10.1007/s10107-021-01749-5) |
| 29 | [kuznetsov2024-convexification-and-global-optimization-of](../../../../literature/papers/kuznetsov2024-convexification-and-global-optimization-of/fulltext.md) | `sections/01-introduction.tex:168` | 85–87, 101–102 | Seven-electron Thomson closure by BARON-solved subproblems: supported; not an exact arithmetic certificate. | S; 2024; no DOI supplied |
| 30 | [geoffrion1972-generalized-benders-decomposition](../../../../literature/papers/geoffrion1972-generalized-benders-decomposition/fulltext.md) | `sections/01-introduction.tex:171` | 1, 4–5 | Classical generalized Benders decomposition: supported within its stated assumptions; not evidence of unrestricted nonconvex validity. | R; 1972; [DOI](https://doi.org/10.1007/bf00934810) |
| 31 | [karuppiah2008-a-lagrangean-based-branch-and](../../../../literature/papers/karuppiah2008-a-lagrangean-based-branch-and/fulltext.md) | `sections/01-introduction.tex:171` | 1, 8–12, 16–18 | Lagrangian bounds and decomposition in nonconvex global optimization: supported. | R; 2008; [DOI](https://doi.org/10.1007/s10898-007-9203-8) |
| 32 | [khajavirad2009-a-deterministic-lagrangian-based-global](../../../../literature/papers/khajavirad2009-a-deterministic-lagrangian-based-global/fulltext.md) | `sections/01-introduction.tex:171` | 1–4 | Deterministic Lagrangian-based global optimization: supported. | R; 2009; [DOI](https://doi.org/10.1115/1.3087559) |
| 33 | [cao2019-a-scalable-global-optimization-algorithm](../../../../literature/papers/cao2019-a-scalable-global-optimization-algorithm/fulltext.md) | `sections/01-introduction.tex:171` | 1–6 | Scalable global optimization using decomposition/nonanticipativity relaxation: supported. | R; 2019; [DOI](https://doi.org/10.1007/s10898-019-00769-y) |
| 34 | [krotov1967-sufficient-conditions-for-the-optimality](../../../../literature/papers/krotov1967-sufficient-conditions-for-the-optimality/fulltext.md) | `sections/01-introduction.tex:171` | 1–4 | Classical global sufficiency via an auxiliary-function argument: supported; Russian OCR limits fine wording. | S; 1967; no DOI supplied |
| 35 | [mangasarian1966-sufficient-conditions-for-the-optimal](../../../../literature/papers/mangasarian1966-sufficient-conditions-for-the-optimal/fulltext.md) | `sections/01-introduction.tex:171` | 1–5, 7–8 | Classical optimal-control sufficiency under specified convexity/sign assumptions: supported. | L; 1966; [DOI](https://doi.org/10.1137/0304013) |
| 36 | [lincoln2006-relaxing-dynamic-programming](../../../../literature/papers/lincoln2006-relaxing-dynamic-programming/fulltext.md) | `sections/01-introduction.tex:171` | 1–3 | Relaxed dynamic programming/value-function bounds: supported. | R; 2006; [DOI](https://doi.org/10.1109/tac.2006.878720) |
| 37 | [bienstock2018-lp-formulations-for-polynomial-optimization](../../../../literature/papers/bienstock2018-lp-formulations-for-polynomial-optimization/fulltext.md) | `sections/01-introduction.tex:171` | 1–3, 10–17 | LP formulations for polynomial optimization with bounded treewidth: supported with bounded-domain/approximation assumptions. | R; 2018; [DOI](https://doi.org/10.1137/15m1054079) |
| 38 | [bohner1996-linear-hamiltonian-difference-systems-disconjugacy](../../../../literature/papers/bohner1996-linear-hamiltonian-difference-systems-disconjugacy/fulltext.md) | `sections/01-introduction.tex:172` | 1–3, 10–16, 19–21 | Discrete disconjugacy and positivity/comparison results: supported. | L; 1996; [DOI](https://doi.org/10.1006/jmaa.1996.0177) |
| 39 | [mcdonald1995-global-optimization-for-the-phase-2](../../../../literature/papers/mcdonald1995-global-optimization-for-the-phase-2/fulltext.md) | `sections/01-introduction.tex:172` | 1–4, 9–14, 31–37 | Gibbs tangent-plane/global phase methods and NRTL examples: supported; does not resolve unread results for the target UNIQUAC instances. | L; 1995; [DOI](https://doi.org/10.1016/0098-1354(94)00106-5) |
| 40 | [tessier2000-reliable-phase-stability-analysis-for](../../../../literature/papers/tessier2000-reliable-phase-stability-analysis-for/fulltext.md) | `sections/01-introduction.tex:172` | 3–6, 8, 12–17 | Reliable phase-stability/interval methods including UNIQUAC: supported; no same-instance closure established. | L; 2000; [DOI](https://doi.org/10.1016/s0009-2509(99)00442-x) |
| 41 | [xia2020-a-survey-of-hidden-convex](../../../../literature/papers/xia2020-a-survey-of-hidden-convex/fulltext.md) | `sections/01-introduction.tex:172` | 1–2, 10–11, 15–17 | Hidden convexity and reformulations: supported. | R; 2020; [DOI](https://doi.org/10.1007/s40305-019-00286-5) |
| 42 | [lavaei2012-zero-duality-gap-in-optimal](../../../../literature/papers/lavaei2012-zero-duality-gap-in-optimal/fulltext.md) | `sections/01-introduction.tex:172` | 1–2, 10–12 | OPF SDP exactness under conditions and numerical cases: supported; not a rigorous certificate for the modified stored cases. | R; 2012; [DOI](https://doi.org/10.1109/tpwrs.2011.2160974) |
| 43 | [molzahn2019-a-survey-of-relaxations-and](../../../../literature/papers/molzahn2019-a-survey-of-relaxations-and/fulltext.md) | `sections/01-introduction.tex:172` | 1–6, 29–42 | Survey of OPF relaxations: supported. | R; 2019; [DOI](https://doi.org/10.1561/3100000012) |
| 44 | [ninin2015-a-reliable-affine-relaxation-method](../../../../literature/papers/ninin2015-a-reliable-affine-relaxation-method/fulltext.md) | `sections/01-introduction.tex:173` | 1, 15–16, 19, 21, 23 | Reliable affine relaxations and safe LP duality: supported. Reported failures do not establish earlier rigorous ex6_2_5/ex6_2_7 closures. | R; 2015; [DOI](https://doi.org/10.1007/s10288-014-0269-0) |
| 45 | [peyrl2008-computing-sum-of-squares-decompositions](../../../../literature/papers/peyrl2008-computing-sum-of-squares-decompositions/fulltext.md) | `sections/01-introduction.tex:173` | 1–4, 7–10 | Conversion of approximate SOS decompositions to rational certificates: supported. | R; 2008; [DOI](https://doi.org/10.1016/j.tcs.2008.09.025) |
| 46 | [hoen2025-analyzing-the-numerical-correctness-of](../../../../literature/papers/hoen2025-analyzing-the-numerical-correctness-of/fulltext.md) | `sections/02-semantics.tex:44` | 1, 4–6, §§2.2–2.3 | Numerical-correctness analysis, point repair, and checking solver decisions: supported; related-work use recommended in issue 4. | R; 2025; [DOI](https://doi.org/10.1007/978-3-031-95976-9_3) |
| 47 | [go2026-parabolic-approximation-relaxation-for-minlp](../../../../literature/papers/go2026-parabolic-approximation-relaxation-for-minlp/fulltext.md) | `sections/D-literature.tex:89` | 38, Table 17 | SCIP floating-point eg_int_s closure at 9085.1 seconds: supported; no rigorous certificate asserted. | L; 2026; [DOI](https://doi.org/10.1007/s10898-026-01591-z) |
| 48 | [go2026-clash-of-minlp-relaxations-piecewise](../../../../literature/papers/go2026-clash-of-minlp-relaxations-piecewise/fulltext.md) | `sections/D-literature.tex:90` | 32, Table 4 | Floating-point gaps for the lnts models: supported; does not supply exact feasible points. | S; 2026; no DOI supplied |
| 49 | [oustry2022-certified-and-accurate-sdp-bounds](../../../../literature/papers/oustry2022-certified-and-accurate-sdp-bounds/fulltext.md) | `sections/B6-powerflow.tex:117` | 2, 4–8 | Certified SDP post-processing for OPF on other benchmark cases: supported. | R; 2022; [DOI](https://doi.org/10.1016/j.epsr.2022.108278) |
| 50 | [waki2006-sums-of-squares-and-semidefinite](../../../../literature/papers/waki2006-sums-of-squares-and-semidefinite/fulltext.md) | `sections/B2-dtoc5-optcdeg2.tex:80` | 23, 32–33, Table 12 | Numerical sparse-SDP optimal-control results with perturbation: supported; not an exact certificate. The extracted equations are blank, so exact DTOC5 model identity was not independently checked from this full text. | R; 2006; [DOI](https://doi.org/10.1137/050623802) |
| 51 | [fullner2024-feasibility-verification-and-upper-bound](../../../../literature/papers/fullner2024-feasibility-verification-and-upper-bound/fulltext.md) | `sections/06-points.tex:44` | 3–7, §3.2 | Verification/upper bounds and fixing coordinates for an approximately active system: supported. | R; 2024; [DOI](https://doi.org/10.1287/ijoc.2023.0162) |
| 52 | [schweidtmann2019-deterministic-global-optimization-with-artificial](../../../../literature/papers/schweidtmann2019-deterministic-global-optimization-with-artificial/fulltext.md) | `sections/B9-ann-kan.tex:14` | 20–23, Table 4 | Cumene-network models, reduced dimensions, and non-convergence at 100000 seconds: supported. | R; 2019; [DOI](https://doi.org/10.1007/s10957-018-1396-0) |
| 53 | [karia2025-deterministic-global-optimization-over-trained](../../../../literature/papers/karia2025-deterministic-global-optimization-over-trained/fulltext.md) | `sections/D-literature.tex:201` | 15–16, 19, 22 | SCIP settings, zero-gap KAN solves and computation-time tables: supported. Archived per-instance primal/dual data were not independently checked in this source passage audit. | S; 2025; no DOI supplied |

Additional metadata observations:

- The bibliography correctly uses the published years 2019 for QPLIB and 2018 for Vigerske's SCIP paper despite 2018/2017 in their slug names. Earlier online publication dates in DOI records are not evidence of an erroneous print year.
- Jansson et al., DOI 10.1137/050622870, has an online publication date in December 2007 and a final issue commonly identified as 2007–2008/2008. The existing 2007 entry is defensible; this is a date-convention issue, not an established metadata error.
- The local Eifler full text is a conference manuscript; the bibliography identifies the later 2023 Mathematical Programming article. The checked rational-input/VIPR statements occur in the local manuscript. A final-version page locator should not be inferred from it.
- The bibliography correctly identifies Helfried Peyrl, Antoine Oustry and Manuel Ruiz, and Artur M. Schweidtmann. Some local knowledge-base summaries contain different given names; those summaries should not override the source front matter. No change to the literature folder was made.
- Registry title formatting differs in two benign cases: MIPLIB 2010 stores its subtitle separately, and GloptLab uses styled capitals/markup. These do not indicate wrong titles in the bibliography.

## Verification record and limits

Targeted work actually performed: `rg` searches for novelty phrases and citation commands in the two documents' included sections; Python inventories of citation keys and balanced BibTeX entries; opening and extracting page-marked passages from the 53 local `fulltext.md` files; title/author/publication comparisons against the bibliography; DOI metadata requests through Crossref (38 successful, eight unresolved requests); and `pdftotext -layout` inspection of the existing main and supplement PDFs. Online primary-source searches and PDF/text inspection supplied the recent-work checks above. These were review checks, not a build or computational reproduction of the certificates.

No project-wide verification was run, no CI status or logs were inspected, no paper or literature file was edited, and no commit was made. The deliverable is this review only. Unread source results, unavailable solver logs, exact stored-model identity across older publications, and the absence of private defect reports remain explicit limits. No stronger historical priority conclusion follows from this review.
