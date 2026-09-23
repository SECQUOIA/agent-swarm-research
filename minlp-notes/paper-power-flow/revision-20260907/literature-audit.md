# Stage 1 literature audit, 7 September 2026

This is a source audit, not a claim of exhaustive publication priority. No literature package was changed. Repository notes were used for discovery; the evidence below distinguishes primary text inspected during this stage from background notes. Search results alone were not used to establish detailed comparisons.

## Fresh online queries

- `"power flow" "existential theory of the reals"`
- `"resistive" "feasibility" "complete" complexity power`
- `power flow feasibility universality solution set algebraic winding complexity`
- `"power flow" "exists R"`
- `"power flow" "ETR" complexity`
- `"winding" "power flow" Jafarpour`
- `"resistive networks" "hardness" feasibility`
- `Farivar Low branch flow model angle recovery cycle condition 2013`
- `Jafarpour Huang Smith Bullo Flow Elastic Networks torus 2022 SIAM`
- `"power" "existential-real" completeness`
- `"power flow" "universality" algebraic`
- `Manik Timme Witthaut cycle flows multistability oscillator networks 2017`
- `Delabays Coletta Jacquod winding numbers power grids 2016`
- `"power flow" "existential" complexity -transportation -ETR`
- `"resistive power" "hard" complexity feasibility`
- `site.motion.me.ucsb.edu "18M1242056"`
- `site.epubs.siam.org "Flow and Elastic" "3.3"`
- `site.arxiv.org "power flow" "exists" "complete"`
- `"resistive" "existential" network feasibility`

The exact-complexity searches were noisy and did not locate a closer matching existential-real completeness theorem. That is a search outcome, not proof of absence. The manuscript makes a qualified model-specific comparison with named predecessors, without an unrestricted first-result claim. Searches can omit preprints, alternate terminology, and recent publications.

The main new literature finding was the importance of the cycle-angle recovery and winding predecessors. The other material addition was crediting the known general repeated-power separation example, while specifying that the electrical realization is the additional result.

## Primary evidence inspected

Local paths below are relative to the repository root. `fulltext.md` is primary-source extraction, not the secondary `paper.md` note. Original PDFs remain authoritative where formulas lose signs or exponents.

1. **Gan and Low, 2014.** Original-derived text `paper-power-flow/build/source-cache/gan-low-dc.txt`, PDF pp.1–4, especially Theorems 1–2 on PDF p.4 (journal p.2895). Author record: <https://authors.library.caltech.edu/records/zf7qf-8jb24>; DOI <https://doi.org/10.1109/TPWRS.2014.2313514>. The source gives sufficient SOCP exactness conditions involving nonbinding voltage upper bounds, or uniform upper bounds and negative injection lower bounds, with objective hypotheses. Intro reports sufficient conditions, not unconditional exact-Turing tractability. The construction permits simultaneous singleton voltage and injection bounds and does not assume their hypotheses.

2. **Jeeninga, De Persis, van der Schaft, Part I, 2023.** Primary text `literature/papers/jeeninga2023-dc-power-grids-with-constant/fulltext.md`, model pp.2–4 and Theorem 3.22 pp.12–13; open original <https://arxiv.org/pdf/2010.01076>. The theorem addresses both exact feasibility and interior feasibility, via positive definite and positive semidefinite matrix alternatives respectively. This passage was read directly, not inferred from the abstract. The source has fixed source voltages and constant-power demands, without the independent operating voltage and source-injection constraints used here. Signed demands are allowed: signedness is not the difference. Part II was screened only through its local note and is not newly cited.

3. **Bienstock and Verma, 2019.** Primary text `literature/papers/bienstock2019-strong-np-hardness-of-ac/fulltext.md`, p.1 model and strong-hardness statement; p.6 Section 1.3; <https://arxiv.org/abs/1512.07315v2>. The local artifact is the preprint: lossless active flows, fixed magnitudes, unconstrained reactive quantities. Its approximation question uses an unpromised relaxed sine system. The separate version-specific preprint citation remains necessary because journal numbering differs. The comparison does not claim that our theorem subsumes its physical restrictions.

4. **Lehmann, Grastien, Van Hentenryck, 2016.** Primary text `literature/papers/lehmann2016-ac-feasibility-on-tree-networks/fulltext.md`, p.1 Section II, pp.2–3 Theorem 1/star construction. DOI <https://doi.org/10.1109/TPWRS.2015.2407363>. Fixed unit magnitudes, active/reactive demands and variable dispatch are explicit. Star/tree hardness is credited. Our result does not assert resistive hardness on trees.

5. **Farivar and Low, Part I, 2013: new citation.** Primary published author-hosted PDF <https://smart.caltech.edu/papers/relaxconvex2parts.pdf>, downloaded to `paper-power-flow/revision-20260907/sources/farivar-low.pdf` with extracted text. Inspected model/introduction pp.2554–2556 and Theorem 2, equations (33)–(34), journal p.2561 (PDF p.8). Its recovery criterion uses cycle sums modulo 2π. Our selected real short differences must sum to zero as real numbers. This is a direct cycle-consistency predecessor, not a proof of the new polynomial input encoding. Metadata verified from the published PDF.

6. **Jafarpour, Huang, Smith, Bullo, 2022: new citation.** Primary preprint <https://arxiv.org/abs/1901.11189v4>, downloaded to `paper-power-flow/revision-20260907/sources/jafarpour.pdf` with extracted text. Inspected Definition 3.1/Theorem 3.3 (PDF pp.12–13), Theorem 3.6 (p.15), Theorem 4.1 (p.17). These give winding numbers/cells, potential representations, and at-most uniqueness for monotone flow maps. Intro credits those established concepts. SIAM Review 64(1):59–104, DOI 10.1137/18M1242056 was corroborated by author Kevin Smith's UCSB dissertation bibliography <https://motion.me.ucsb.edu/pdf/phd-kds-dec22.pdf>. Direct DOI opening failed in the web tool; journal theorem numbering was not assumed. The bibliography identifies the inspected preprint; the intro avoids version-sensitive theorem locators for this source.

7. **Delabays, Coletta, Jacquod, 2016: new citation.** Primary published author-hosted PDF <https://delabays.xyz/docs/articles/Delabays16a.pdf>, inspected via web: pp.2–4 and pp.7–8, loop currents and winding discussion. The source credits earlier winding work and explains circulating solutions and their connection to power grids. The manuscript credits this established phenomenon. First page verifies Journal of Mathematical Physics 57, 032701, DOI 10.1063/1.4943296. No local download was made.

8. **Lavaei–Low, 2012; Dörfler–Chertkov–Bullo, 2013.** Original-derived Lavaei–Low text `paper-power-flow/build/source-cache/lavaei-low.txt`, Appendix B Case 2 on PDF p.13, checked for the resistive-AC/zero-reactive connection. DOI <https://doi.org/10.1109/TPWRS.2011.2160974>. This does not justify an unrestricted torus uniqueness assertion. The Dörfler source was screened through its repository note and existing citation; no fresh theorem-level claim is made about it. It remains background for weighted sine equilibria.

9. **Mareček, McCoy, Mevissen, 2016 version: new citation.** Primary text `literature/papers/marecek2014-power-flow-as-an-algebraic/fulltext.md`, pp.6–8 Theorem 1/Corollary 2 and p.12 discussion. Version date verified at <https://arxiv.org/abs/1412.8054v2>: 15 November 2016. It analyzes multihomogeneous equations, generic complex root counts, and positive-dimensional sets. Realization of prescribed compact real sets with operating inequalities is different. We do not claim to originate algebraic power-flow analysis. Citation explicitly uses the inspected preprint version.

10. **Abrahamsen and Miltzow, 2019.** Primary text `literature/papers/abrahamsen2019-dynamic-toolbox-for-etrinv/fulltext.md`: Theorem 1 p.3, rational equivalence p.4, Boolean preprocessing Lemma A pp.5–7; conjunction arithmetic Lemmas C–G pp.8–18. <https://arxiv.org/abs/1912.08674v1> confirms only v1 is posted. Integer versus rational coefficients do not change rational functions. Theorem 1 states universality for arbitrary compact semialgebraic sets. The manuscript's basic-closed invariant and three-quadrant example limit that claim under the same globally defined rational-coordinate interpretation. Intro now identifies the version and relies on the self-contained conjunction arithmetic instead of Boolean preprocessing. This does not challenge separately established ETR-INV decision hardness.

11. **Abrahamsen, Adamaszek, Miltzow.** Primary local text `literature/papers/abrahamsen2022-the-art-gallery-problem-is/fulltext.md`, p.11 Definition 5/Theorem 7, pp.12–15 reduction. <https://arxiv.org/abs/1704.06969>. The local artifact uses STOC/arXiv numbering despite the package's journal year, so preserve the qualification already in Section 2. The bounded arithmetic source problem is imported.

12. **Dobbins, Kleist, Miltzow, Rzążewski, 2023.** Primary published text `paper-power-flow/build/source-cache/dobbins-area.txt`, journal p.163, Theorem 2.1 and Figure 3. DOI <https://doi.org/10.1007/s00454-022-00381-0>. Its three-addition crossover copies the crossing variables via their sum, which lies up to 4. The source formulates a promise problem; this manuscript uses explicit bounds and supplies its own electrical realization. Stage 2 should verify that bounded solution-set argument rather than importing the stronger property from promise hardness alone.

13. **Ohmoto and Shiota, 2017 version.** Primary original-derived text `paper-power-flow/build/source-cache/ohmoto-shiota-triangulation.txt`, PDF p.2 Theorem 1.1 and Section 1.2; <https://arxiv.org/abs/1505.03970v2>. Compact semialgebraic sets have finite semialgebraic triangulations. No rationality of the triangulation is required for our separate topological conclusion.

14. **Jeronimo, Perrucci, Tsigaridas, 2013.** Primary local original `literature/papers/jeronimo2013-on-the-minimum-of-a/original.pdf`; cached extracted text `paper-power-flow/build/source-cache/jeronimo-minimum.txt`; <https://arxiv.org/abs/1112.0544>. Inspected Theorem 1 PDF p.2 and Example 13 p.12. Example 13 was rendered from the original and visually checked because exponent extraction is fragile. It uses repeated powers to generate two points with doubly exponential separation. The intro now credits that known scale and claims the fixed-data bounded-degree electrical realization. The local theorem is numbered 1; root has been alerted that the numerical section's journal Theorem 1.1 locator needs verification or explicit preprint qualification.

15. **Bienstock, Del Pia, Hildebrand, 2023: new citation.** Primary text `literature/papers/bienstock2023-complexity-exactness-and-rationality-in/fulltext.md`, overview pp.3–4, theorem statement discussions, and Theorem 3.6 pp.18–19; <https://arxiv.org/abs/2011.08347>. It distinguishes rational certificate size from real feasibility and proves a fixed-dimension near-feasible certificate result. Our variable-dimension gap promise is proved by its own bounded-quadratic rounding argument. The intro cites the broader issues without overstating that theorem.

16. **Bienstock and Muñoz, 2018.** Local package and previous audit were screened. The revised intro retains the existing expressly version-specific Theorem 7/Corollary 8 reference <https://arxiv.org/abs/1501.00288v15>. No new quantitative algorithm claim was added. This stage did not freshly read its full theorem proof; a final reviewer should verify the locator if treating this audit as the sole evidence source.

## Access and verification limits

The five newly cited sources were inspected in primary form. Where the primary text was a preprint, no publisher theorem number was silently inferred. The Jafarpour DOI open failed; the author preprint download succeeded and supplied all substantive comparison evidence. The attempt to render local PDFs with Python `fitz` failed because that package was absent; the standard `pdftoppm` tool succeeded and the JPT example was visually checked. Neither failure altered a literature package.

No all-model electrical universality is claimed. Independent singleton voltage and injection constraints remain essential assumptions. The residual example belongs to the ordinary fixed-data bounded-degree class: no quantitative transfer through planarization is claimed. A complete independent proof audit of the core is the next stage, not something certified by this literature stage.

## Review and correction follow-up

The five independent Stage 1 reviews and the separate correction pass supplied the following additional primary-source checks. These resolve the initial audit's open locator questions; the initial inspection record above is retained.

- **Jeeninga et al.** Theorem 3.18 establishes closedness and convexity of the feasible demand set; Theorem 3.22 supplies the exact/interior matrix alternatives. The introduction now cites both locators.
- **Bienstock–Muñoz.** Reviewers and the corrector inspected Theorem 7 and Corollary 8 directly in the primary local extraction listed above. The version-specific locators are correct. Theorem 7 bounds the formulation size using the treewidth and the number of local variables and constraints; the introduction now makes both structural qualifications explicit.
- **Dynamic Toolbox.** Definition 4 requires rational coordinate maps in both directions, defined on their respective sets. Integer versus rational coefficients gives the same notion. The introduction now explicitly identifies that agreement; it does not require nonvanishing denominators throughout the ambient Euclidean spaces.
- **Jafarpour et al.** Section 2.1 takes angles modulo a common rotation, and the proof of Theorem 4.1 concludes equality modulo rotations. The introduction now includes this qualification. Reviewer 4 also directly confirmed the journal metadata at <https://epubs.siam.org/doi/10.1137/18M1242056>.
- **Ohmoto–Shiota: published metadata added; inspected version retained.** The corrector independently opened the [publisher record](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/topo.12024) and [Ohmoto's publication page](https://www.math.sci.hokudai.ac.jp/~ohmoto/activity.html). Both confirm *Journal of Topology* 10 (2017), 765–775, DOI `10.1112/topo.12024`; the publisher confirms issue 3. The version-specific [arXiv record](https://arxiv.org/abs/1505.03970v2) was also opened, and the cached primary v2 text was reread at Theorem 1.1 and Section 1.2. Those are the manuscript's precise triangulation and compact-finiteness locators. The bibliography now supplies the journal metadata and expressly states that theorem and section numbering follows v2, retaining its URL. The publisher full-text link returned its abstract page, so published theorem numbering was not inferred from that response.
- **Jeronimo–Perrucci–Tsigaridas: journal locator confirmed.** Reviewer 4 located the [published SIAM PDF at CONICET](https://ri.conicet.gov.ar/bitstream/handle/11336/14866/CONICET_Digital_Nro.18274.pdf?isAllowed=y&sequence=1), independently opened by root. The corrector downloaded the same primary PDF to `paper-power-flow/revision-20260907/sources/jeronimo-published.pdf` and extracted `jeronimo-published.txt`. Journal page 242 explicitly labels the relevant result **Theorem 1.1** and states the compact-connected-component, even-degree, coefficient-height minimum bound. The first page confirms *SIAM Journal on Optimization* 23(1), 241–255 (2013), DOI `10.1137/110857751`. The numerical section's journal locator is correct and remains unchanged. The web opener returned an internal error in the correction pass, but the ordinary HTTPS download succeeded. This resolves the initial audit's numbering uncertainty.
