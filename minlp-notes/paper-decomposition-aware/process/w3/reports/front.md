# W3 report: front group (abstract, intro, related, conclusion)

Files edited: `sections/abstract.tex`, `sections/intro.tex`, `sections/related.tex`,
`sections/conclusion.tex`. No other file was touched.

Before writing, I read the current versions of all other sections, including the
revisions that other agents made during this round: thm:approx, lem:states, thm:exact,
thm:certificate, thm:transfer, thm:valuefn, thm:cv, thm:cr-oracle, thm:cr-search,
thm:cr-exact, thm:balanced, thm:tu-approx, sec:tu-limits, thm:cells, thm:endpointset,
cor:facecsp, thm:diagdiscovery, lim:prop:unique, lim:cor:nopolylog, prop:lbwidth,
prop:lbproduct, lim:prop:oracle, lim:rem:oracle and lim:prop:setgrowth. Every summary
statement in my files was checked against these statements. The results table follows
the revised bounds of thm:cv and thm:valuefn (extra factor kappa^C, growth of V), of
thm:cr-exact (8^k(1+sqrt(k kappa_K))^k poly(I)) and of thm:tu-approx (K_Z, s), as they
stood at 02:15.

## What changed

* **Abstract.** Rewritten from R6 Rewrite 1, about 230 words of prose. It covers the
  certificate (valid without growth), the accuracy-independent grid bound, the
  approximation bound f(p, kappa-bar)(I+q+1)^5, exact output under point growth with
  kappa >= kappa-bar, and the lower bounds with their assumptions. It has one sentence
  for the extensions and one for the implementation. Corrections to Rewrite 1:
  - Growth is not called "checkable", because it is not.
  - "must grow linearly" became "cannot be o(p)".
  - "(I+q+1)^{O(1)}" became "(I+q+1)^5".
  - Exact output is qualified by point growth and the Euclidean kappa.
  - The abstract makes no complexity claim for the TU extension.
* **Introduction.** Sections 1.1 and 1.2 are merged into one subsection, "Results"
  (label `sec:intro-results`). It contains, in order:
  - the setup;
  - the certificate paragraph, which carries the new contribution (i) of R7: the
    node-separable form of the Bajaj-Hasan vertex bound, called an observation;
    min-marginals as interval bounds for OBBT; a certificate checked by recomputation;
  - Theorem 1.1 (`thm:intro-main`, parts a-c), combining thm:certificate,
    lem:states/thm:approx and thm:exact with their exact hypotheses;
  - a novelty statement and the snapping sentence (Rewrite 8);
  - the "Parameterized form" paragraph, with the FPT wording of CONVENTIONS section 5;
  - the "Scope of the growth hypothesis" paragraph, with the CONVENTIONS text plus a
    sentence on the size of kappa;
  - the exact-messages example;
  - the ETH and rETH definitions;
  - Theorem 1.2 (`thm:intro-lower`, parts a-d), with explicit assumptions, followed by
    the CONVENTIONS lower-bound sentence and a summary of the further limits, with
    credits;
  - one paragraph each on recourse (opens with the definition, Rewrite 8b), TU coupling
    (CONVENTIONS wording) and several minimizers (with the Rosenberg/WJW/Werner credit),
    each with its novelty statement;
  - Table 1 (`tab:results`; booktabs, `\small`, float `[tbp]`), with 14 rows;
  - the organization paragraph for the new structure.

  The six-item contributions list was removed.
* **Related work.** Reorganized around the three questions of R6 m33:
  1. tractability of sparse nonconvex QP;
  2. grid and vertex bounds, filtering and certificates;
  3. accuracy-independent work under growth, with adaptive discretization in its own
     paragraph.

  Then come exact output, value functions, cuts and submodularity, and
  constraints/optimal sets/limits. Changes:
  - All R7 minor fixes (m3-m6, m11).
  - The AMP and Gupte-Koster-Kuhnke sentence (M4).
  - Cook-Koch-Steffy-Wolter next to Cheung-Gleixner-Steffy.
  - The extra point from the deleted rem:cluster (the condition 8 kappa-bar theta^2 <= 1
    plays the role of the second-order prefactor bound).
  - The full Burer-Natarajan-Willemsen and balanced-QP comparison, which formerly sat
    also in an in-section remark.
  - The smoothed-analysis sentence was removed (its appendix is deleted).
* **Conclusion.** Changes:
  - Lower-bound wording follows CONVENTIONS.
  - Explicit bounds replace the "FPT" label.
  - Branch-and-bound use is marked as a possible use ("whether either pays off inside a
    solver is untested").
  - R8 wording for the floating-point incumbent and for the QPLIB limit.
  - Open problem (1) uses Corollary cor:cv-nu.
  - Open problem (2) discusses where the p^p factor comes from.
  - Open problem (3) names Proposition tu-misaligned and Example tu-sum, plus the
    TU-hybrid outline in one sentence (rem:tu-hybrid is deleted).
  - Open problem (4) uses the corrected lim:prop:setgrowth.

## (1) Adjudication

| id | verdict | reason | change made (front files) |
|---|---|---|---|
| F0 | ACCEPTED | The TU summary claims contradicted lim:prop:constraints. | The abstract makes no TU complexity claim. The intro TU paragraph uses the CONVENTIONS wording: polynomial for fixed width when kappa_c, s/eta and r are polynomially bounded; not FPT in (p, kappa_c) (sec:tu-limits); the level-0 grid cannot be removed unless P=NP. |
| F1 | MODIFIED | Rewrite 1 still had "two checkable quantities" (growth is not checkable), "must grow linearly", "(I+q+1)^{O(1)}" and an unqualified exact claim. | New abstract of about 230 words; corrections listed above. |
| F2 | ACCEPTED | The paper had no headline theorem and the contributions list repeated the results. | Theorem 1.1 (a: certificate, b: grid bound + approx, c: exact) and Theorem 1.2 (lower bounds). Novelty statements moved into paragraphs; contributions list removed. |
| F3 | ACCEPTED | Correct; Lemma growthcert(b). | "Scope of the growth hypothesis" paragraph with the exact CONVENTIONS text. |
| F4 | ACCEPTED | K_S = 12r(2 sqrt(n kappa_S)+1). | "O(r sqrt(n kappa_S)) nodes per coordinate ...; for fixed p the work is polynomial in n, r, kappa_S and I+q". |
| F5 | ACCEPTED | Only polylogarithmic dependence is excluded. | Conclusion uses the CONVENTIONS lower-bound sentence. |
| F6 | MODIFIED | Rewrite 21 kept the "answers this" phrasing, but the theorem only covers a subclass. | Open problem (1) asks for time f(p, kappa_nu) poly(I+q) with kappa_nu = max{1, nu/g}. "Theorem cv and Corollary cv-nu give such a bound when certified responses of private convex blocks reduce every coordinate curvature to at most C_0 nu"; Prop cv-limit and Prop lim:prop:moments are cited as obstructions. |
| F11 | ACCEPTED (front part) | Comparisons were duplicated. | Related work keeps the full comparisons: cluster problem (plus the extra point from rem:cluster), cuts/BNW/balanced, OBBT/VIPR. It points to rem:tu-bm and rem:np, which keep the technical comparisons. Other owners have already done their part: growth.tex has a one-line pointer instead of rem:cluster, grids.tex no longer repeats the OBBT/VIPR text, and the balanced "Position" remark is gone. |
| F16 | ACCEPTED | Width two, not three. | Thm 1.2(a) says "maximum bag size three". |
| F17 | ACCEPTED | Hard to parse. | Rewrite 7. |
| F18 | ACCEPTED | "Within k bits" was undefined; recourse was undefined. | Rewrite 8 (certified gap at most 2^{-k}) and Rewrite 8b (definition of recourse). Added: "the growth hypothesis of part (c) serves only to bound the time". |
| F23 | ACCEPTED | Plural with one reference. | "Proposition prop:tu-misaligned and Example ex:tu-sum". |
| F26 | ACCEPTED (front part) | British spelling. | related.tex "neighbours" -> "neighbors"; the other occurrences are in other owners' files. |
| F27 | ACCEPTED (front part) | Idiom. | "does real work" removed from the intro. |
| F31 | ACCEPTED (front part) | The appendices also contain results. | Organization paragraph: "The appendices follow the order of the sections. Besides longer proofs, they contain secondary results: ...". Appendix order and titles belong to the coordinator and the owners. |
| F33 | MODIFIED | The catalogue structure was valid criticism, but the peripheral items cannot be moved into other owners' files, and no other section discusses Benders, MPC condensing, DEE or cascades. | Related work reorganized around the three questions, plus extension paragraphs. Smoothed analysis removed. Benders/MPC and DEE/cascades are reduced to one clause each inside the relevant paragraphs. |
| F36 | ACCEPTED | Same as F0; "forced" overclaims. | As F0. "Forced" replaced by "two natural non-uniform alternatives ... give invalid bounds with curvature-only corrections". |
| F37 | ACCEPTED | Correct. | Scope paragraph. Added: "The condition number can be large: on the hard instances of Theorem 1.2(a), log kappa = O(I), and unless P=NP it is not polynomially bounded there. We do not claim that it is moderate for the application models mentioned above. The certificates are valid in every case." The application paragraph motivates treewidth only and is kept. |
| F38 | ACCEPTED | kappa-bar is real, not an input, and not computed. | The abstract and conclusion state explicit bounds and avoid the FPT label. The intro "Parameterized form" paragraph: bound <= f(p, ceil(kappa-bar))(I+q+1)^5 because f is increasing; "a fixed-parameter bound in the parameters p and ceil(kappa-bar), which the algorithm does not need to know". |
| F40 | ACCEPTED | Correct. | Abstract of about 230 words; 1.1 and 1.2 merged; no TOC (main.tex has none). |
| F43 | ACCEPTED (front part) | Correct. | Intro: the cellwise identity is called an "observation" and Bajaj-Hasan is credited. The several-minimizers paragraph credits Rosenberg, WJW and Werner and states what is new. The §9.2 and §7.3 parts belong to optsets/recourse; recourse already contrasts with Khajavirad in rem:cv-instances. |
| F44 | ACCEPTED | Overstatement. | "cannot be o(p)" and "cannot be polylogarithmic unless P=NP" in the abstract, intro and conclusion. |
| F48 | ACCEPTED (front part) | Duplicate. | Related keeps the paragraph; core replaced the remark by a pointer. |
| F49 | ACCEPTED (d only) | (d) is in the conclusion; (a), (b), (c), (e) are in other files. | Conclusion (3) fixed. |
| F50 | ACCEPTED | As F0. | As F0 and F36. |
| F51 | ACCEPTED (front part) | Assumptions were dropped. | Conclusion paragraph 1 and open problem (2) rewritten; "must grow" removed. Remark 5.8 (rem:fpt) was already fixed by core. |
| F52 | ACCEPTED (front part) | The proposition assumes rETH and integer instances. | Abstract and intro: "under rETH the exponent ... cannot be o(p), already for integer box quadratics"; Thm 1.2(c) states the proposition exactly. |
| F54 | MODIFIED | Same content as F6 and F114. | See F6. |
| F55 | ACCEPTED (front part) | kappa_S and continuous variables. | Intro: "for continuous box quadratics certified by a diagonal Lagrangian multiplier ... f(p, kappa_S) poly(I) ... without knowledge of g_S". Table row uses kappa_S. Request to optsets below. |
| F68 | ACCEPTED (part e) | rem:cluster is deleted, so related.tex is the single place. | Related keeps the cluster comparison. The other parts are in other files. |
| F73 | ACCEPTED | Width two. | See F16. |
| F74 | ACCEPTED (MODIFIED) | The abstract list was redundant. | The abstract has one extension sentence. The intro recourse paragraph uses the corrected description: value factors certified by piecewise-affine responses; residuals evaluated by one minimum cut; for balanced quadratics the grid problem is a minimum cut, which removes the width parameter. |
| F80 | ACCEPTED | As F23. | As F23. |
| F96 | ACCEPTED (front part) | "Forced" overclaims. | Intro uses the CONVENTIONS wording; constraints.tex is the TU agent's (already changed). |
| F97 | ACCEPTED | As F0. | As F0. |
| F105 | ACCEPTED | The output is one optimizer plus a description. | "an exact optimizer and an exact description of the optimal set by linear equations and complementarity conditions". |
| F106 | ACCEPTED (front part) | kappa_S can be exponential. | See F4. |
| F109 | ACCEPTED (conclusion part) | The other items are in other files. | Conclusion (3). |
| F114 | MODIFIED | See F6. | See F6. |
| F134 | MODIFIED | Item (v) no longer exists (list removed). The credit and novelty statement were placed in the intro's limits summary. | "... a path of local affine equalities makes the problem NP-hard at bag size three and kappa = 1, by the running-sum encoding of Subset Sum of Bienstock and Muñoz [BM, App. A]; ... As far as we know, the expanding-box chain, the unique-minimizer hardness with explicit growth (a refinement of [DPK, Remark 2]), the rETH bound and the moment obstruction are new; the other statements adapt standard constructions." The Cifuentes-Parrilo credit stays in limits.tex (one place). |
| F135 | ACCEPTED (front part) | Correct. | The abstract no longer mentions the endpoint program. The intro credits Rosenberg/WJW/Werner and states the new part. optsets.tex is the optsets agent's. |
| F136 | ACCEPTED | Correct. | Contribution (i) text placed in the certificate paragraph (node-separable form; OBBT from one pair of message passes; certificate checked by recomputation). |
| F137 | MODIFIED | R7's sentence calls both methods "without a bound on the number of partition points". Gupte-Koster-Kuhnke use discretizations of fixed size (KB p. 5-8; DataCite abstract), so that is false for them, and the closing sentence "none ... comes with a state count independent of the accuracy" is literally false for a fixed-size heuristic. | Added to "Adaptive discretization": AMP "refines piecewise relaxations around the current relaxation solution and combines them with OBBT, with no bound on the number of partition points needed for a given accuracy", and "a primal heuristic re-centers discretizations of fixed size on the previous solution". Closing sentence: "None of these methods certifies a given accuracy with a number of states independent of that accuracy." |
| F138 | ACCEPTED | Waki and Lasserre give no rates. | "...; the known bounds on their size are polynomial in the inverse accuracy [BM, KMRZ2025]" (KMRZ abstract checked: polynomial rate depending on the clique size). |
| F139 | MODIFIED | The Bajaj-Hasan full text is not reachable (Springer blocks scripted access; Semantic Scholar elides the abstract), so whether they use one global bound or per-coordinate bounds cannot be confirmed. | related.tex makes no theorem-number or constant claim ("using an upper bound on the diagonal Hessian entries"). The intro says "the best of these bounds, with per-coordinate curvature bounds", which describes our use without asserting theirs. grids.tex keeps "[Theorem 1]" (core's file): unresolved. |
| F141 | ACCEPTED | Verified in the KB (trees O(n^2); graphs linear in n for fixed treewidth, margin, volume growth, kappa_2, kappa_inf; Cor. 1 discussion). | R7 wording. |
| F142 | ACCEPTED | Eiben: FPT by treewidth plus maximum domain (KB p. 4-6). Herrmann verified on arXiv (2608.17818v1, 2026-08-18). | R7 wording. |
| F143 | ACCEPTED | KB: Del Pia 2023 fixes rank and number of integer variables. | R7 wording. |
| F144 | ACCEPTED | Correct. | R7 wording. |
| F147 | ACCEPTED (front part) | — | Cited in related/intro: KordaMagronRiosZertuche2025, KolmogorovPockRolinek2016 and KuricAhmetspahicPock2024 (with DPK's remark on nonconvex terms; DPK fulltext p. 433 region), SojoudiLavaei2014, HladikCernyRada2021, Vorobev1962, DeLoeraEtAl2008, HildebrandWeismantelZemmer2016, PardalosVavasis1991 (Vavasis 1992 and Del Pia 2026 use it for the polylog argument, checked in KB), BreimanCutler1993, NeumaierShcherbina2004, Hansen1980 and HansenWalster2004 (instead of Kearfott 1996), CookKochSteffyWolter2013 and BurgisserCucker2013. Not in my files: CifuentesParrilo2016 (limits), SCIP 10 (computation). Not added: Füllner-Rebennack (optional; Benders is peripheral per F33). |
| F148 | ACCEPTED | Correct. | See F44. |
| F153 | ACCEPTED (no change needed in front files) | The finding concerns exact.tex. | The organization paragraph describes the new Section 6. |
| F157 | ACCEPTED (front part) | Weighted growth allows several minimizers. | Abstract: "quadratic growth", "under growth in the norm weighted by the L_i", "under growth at a unique minimizer" only for exact output. setting.tex belongs to core. |
| F178 | ACCEPTED (front part) | Counterexample confirmed by limits' revised Prop lim:prop:setgrowth. | Intro: "does not bound the grids produced by filtering". Conclusion (4): "the grids produced by filtering can need a number of nodes that grows with the accuracy". |
| F181 | ACCEPTED (front part) | Correct. | Abstract, intro and conclusion use "cannot be o(p)" under rETH and "cannot be polylogarithmic" unless P=NP. |
| F195 | ACCEPTED (front part) | Idiom. | "Does real work" removed from the intro. |
| F200 | ACCEPTED (conclusion part) | QPLIB_3852 is solvable with a larger cap. | "on binary QPLIB instances the width of the available decomposition, not the accuracy, is the binding limit". This stays true for the revised §11.9 (3852 solved exactly; 5881 needs about 10^29 entries). |
| F221 | ACCEPTED (conclusion part) | The experiments evaluate an incumbent exactly; they do not check SCIP's bounds. | "A replayable certificate also allows a floating-point incumbent to be certified: its exact value together with a grid certificate gives a rigorous gap." |

## (2) Labels deleted or renamed

None were deleted or renamed. The old intro, related and conclusion had only `sec:intro`,
`sec:related` and `sec:conclusion`, which are kept.

New labels:
* `sec:intro-results`: subsection "Results" of the introduction.
* `thm:intro-main`: Theorem 1.1, the headline theorem (certificate, grid bound and
  approximation, exact output).
* `thm:intro-lower`: Theorem 1.2, the lower bounds with their assumptions.
* `tab:results`: Table 1, the main results with their setting, parameters, bounds and
  outputs.

## (3) Requests for other files

1. **recourse:** keep the label `cor:cv-nu` (moved to appendix-recourse-convex.tex);
   conclusion open problem (1) cites it. It resolves in the current build. The
   conclusion uses the condition "every coordinate curvature at most C_0 nu", which
   matches "L^+ <= C_0 nu". If the bounds of thm:cv or thm:valuefn change again, the two
   corresponding rows of Table 1 in intro.tex must be updated (they currently read
   f(p,kappa) kappa^C (I+q+1)^C and f(p,kappa) kappa^{C_1}(I+1)^{C_1}).
2. **optsets:** Theorem thm:diagdiscovery(b),(c) and the remark after it still write
   kappa and g. The intro and Table 1 use kappa_S = max{1, L/g_S} (F55). Please change
   the theorem to kappa_S and g_S so that they match.
3. **core:** keep the labels `rem:fpt`, `cor:uniformgrid`, `lem:growthcert`,
   `ex:family`, `eq:logabsorb`, `alg:ct` and `lem:states`, all cited from the intro or
   conclusion. The notation table promised by the organization paragraph ("closes with a
   table of notation") is assumed to be at the end of Section 3 (CONVENTIONS section 1).
4. **exact:** keep `alg:ex`, `cor:poly`, `ex:polylimits`, `thm:transfer` and `rem:np`
   (related.tex cites rem:np for the NP-membership discussion).
5. **tu:** keep `rem:tu-bm` (related.tex and the intro point to it for the technical
   comparison with Bienstock-Muñoz) and `sec:tu-limits`. Table 1 uses `K_Z` and `s`
   as in the revised thm:tu-approx.
6. **bib (coordinator):** do NOT delete these entries; they are now cited in my files
   and were uncited before W3: BreimanCutler1993, DeLoeraEtAl2008,
   HildebrandWeismantelZemmer2016, PardalosVavasis1991, SojoudiLavaei2014,
   HladikCernyRada2021, Hansen1980, HansenWalster2004. These entries, newly added by the
   bib agent, are cited by my files: KordaMagronRiosZertuche2025, Herrmann2026,
   KolmogorovPockRolinek2016, KuricAhmetspahicPock2024, Vorobev1962,
   NeumaierShcherbina2004, CookKochSteffyWolter2013, BurgisserCucker2013,
   NagarajanEtAl2019 and GupteKosterKuhnke2022. Now unused, because the smoothed-analysis
   sentence was removed and appendix-smoothed is deleted: SpielmanTeng2004,
   BeierVocking2006, and RoglinVocking2007/BeierVocking2004 once appendix-smoothed.tex
   is gone.

## (4) New BibTeX entries

None needed. All keys I cite already exist in references.bib, added by the bib agent. I
checked them against primary metadata independently:
* Crossref: NagarajanEtAl2019 (JOGO 74(4):639-675), KordaMagronRiosZertuche2025
  (MP 209(1-2):435-473), Vorobev1962 (TPA 7(2):147-163), NeumaierShcherbina2004
  (MP 99(2):283-296), CookKochSteffyWolter2013 (MPC 5(3):305-344),
  KolmogorovPockRolinek2016 (SIIMS 9(2):605-636, 10.1137/15M1010257),
  KuricAhmetspahicPock2024 (SIIMS 17(2):1040-1077, 10.1137/23M1556915),
  CifuentesParrilo2016 (SIDMA 30(3):1534-1570) and BurgisserCucker2013
  (Grundlehren 349, 10.1007/978-3-642-38896-5).
* DataCite: GupteKosterKuhnke2022 (LIPIcs 233, 24:1-24:14; editors Schulz and Uçar).
* arXiv API: Herrmann2026 (2608.17818v1, 2026-08-18, sole author Anton Herrmann).

All matched the bib entries.

## (5) Checks run

* `latexmk -pdf -interaction=nonstopmode -outdir=build/front main.tex`. latexmk's bibtex
  step read a stray root-level `main.aux` from another build ("I found no \bibdata
  command"). I therefore ran the sequence manually: `pdflatex -output-directory=build/front`,
  then `cd build/front && BIBINPUTS=../..: bibtex main`, then pdflatex twice. Result:
  - 0 LaTeX errors;
  - 119 pages;
  - no undefined references or citations from abstract, intro, related or conclusion;
  - no overfull boxes in my files;
  - the remaining overfull boxes are in recourse-local (14.5pt), recourse-convex (12.8pt
    and 4.2pt), optsets (5.2pt) and appendix-moments (0.2pt);
  - the one remaining bibtex warning is a missing `HornJohnson2013`, cited by another
    group.
* I removed two overfull boxes in conclusion.tex (38.9pt and 18.9pt) and fixed the
  table width (originally 9.5pt too wide).
* Table 1 initially floated to the last page because it exceeded the top-float
  fraction. Placement changed to `[tbp]`; it now sits on page 6.
* I rendered pages 1-7 and 78-79 to PNG (`pdftoppm`) and inspected the abstract,
  Theorem 1.1, Theorem 1.2, the paragraphs, Table 1, related work and the conclusion.
* Word count of the abstract: 247 tokens counting each math expression as one word,
  about 230 prose words.
* Literature checks: local KB full texts for Bhathena (trees and graphs), Eiben 2019,
  Del Pia 2023 and 2026, Vavasis 1992, DPK (Kuric remark), Hladík-Černý-Rada,
  Gupte-Koster-Kuhnke and Nagarajan. Crossref, DataCite and arXiv queries as in (4).
  Semantic Scholar for the KMRZ abstract.
* Scan of my files for banned or deprecated wording: "must grow", "must be polynomial",
  "forced", "Algorithm 1/2", "geometric grid", "labels per", British spellings, "really",
  "actually", "crucial" and similar. No hits.

These are targeted checks only. No project-wide verification was run and CI was not
consulted.

## (6) Unresolved

* **Bajaj-Hasan 2020.** Theorem 1 and its constant convention, and whether they use a
  single diagonal bound or per-coordinate bounds, are still unverified (paywalled; F139).
  My files make no claim about either. grids.tex (core) still cites "[Theorem 1]".
* **Table 1 depends on statements that other agents are still revising** (thm:cv,
  thm:valuefn, thm:cr-exact, thm:tu-approx, thm:diagdiscovery). The rows match the
  versions current at 02:15. A final consistency pass after all groups finish is
  advisable.
* **The organization paragraph names Appendices C (app:boundary) and E (app:proximal)
  by label.** The recourse and TU appendices are mentioned without labels, because their
  final labels were not fixed when I wrote this.

## Verification (front-verify)

Files re-checked and edited: `sections/abstract.tex`, `sections/intro.tex`,
`sections/related.tex`, `sections/conclusion.tex`. No other file was touched.

### What was checked

* **Adjudications.** All 58 findings in `assign/front.json` against the diffs
  with `sections-before-w3/`. Every ACCEPTED fix is present in the files. The
  MODIFIED decisions (F1, F6/F54/F114, F33, F134, F137, F139, F74) are
  justified: Rewrite 1 did contain "checkable" and "must grow linearly"; Gupte,
  Koster and Kuhnke do use fixed-size discretizations, so R7's closing sentence
  would have been false for them; the contributions list no longer exists, so
  F134's item (v) became the novelty sentence after Theorem 1.2. No finding was
  rejected, and I found none that should have been.
* **Every summary statement against its source**, read in the current files:
  def:growth, lem:growthcert/rem:nonconvex, prop:cellwise, prop:filter,
  thm:certificate, alg:ct, thm:approx, lem:states, rem:fpt, lem:commonmesh,
  cor:uniformgrid, ex:family, ex:chain, prop:accept, thm:transfer,
  rem:setgrowth, rem:np, thm:exact, cor:poly, ex:polylimits,
  lem:valuefunction, thm:valuefn, thm:cr-filter, prop:star, prop:vf-curv,
  thm:cv, cor:cv-nu, rem:cv-unstable, prop:cv-limit, thm:cr-oracle,
  thm:cr-search, prop:cr-growth, thm:cr-exact, thm:balanced, thm:tu-approx and
  the paragraph after it, sec:tu-limits, prop:tu-misaligned, ex:tu-sum,
  rem:tu-bm, prop:twocenters, thm:cells, thm:endpointset, cor:facecsp,
  thm:diagdiscovery, prop:sshard, lim:prop:unique, lim:cor:nopolylog,
  lim:prop:oracle, lim:rem:oracle, prop:lbwidth, prop:lbproduct,
  lim:prop:messages, lim:prop:setgrowth, prop:oraclebarrier,
  lim:prop:constraints, lim:prop:moments, and the computation section
  (chain table, SCIP comparison, QPLIB limits). Theorem 1.1(a)-(c), Theorem
  1.2(a)-(d) and all 14 rows of Table 1 match these statements (for the TU row,
  K_0 <= max{K_Z, s/eta+1} and K_j <= max{K_Z, r(5+floor(2 sqrt(n_c kappa_c)))},
  so the combined K is a valid per-level bound; J = O(I+q)).
* **Derived claims re-derived:** "kbar <= kappa" (point growth gives weighted
  growth with gamma = g/L, or every gamma if L = 0); the transfer from lower
  bounds in kappa to kbar (an algorithm polynomial in kbar would be polynomial
  in kappa); "unless P=NP, no polynomial in I bounds kappa on the hard
  instances" (otherwise CT with p = 3 and q = ceil(log2(4m)) decides Subset
  Sum); Theorem 1.2(d) as stated (success on the whole class implies success on
  the family F_c); open problem (1) via thm:cv(iii) and cor:cv-nu.
* **CONVENTIONS:** claim wording for growth scope, FPT, lower bounds, TU,
  uniform cells, endpoint credits and the Subset Sum credit; algorithm names
  and first-use form; reserved symbols; banned words; British spellings; and
  undefined abbreviations.

### What was fixed

* **Intro, setup paragraph.** "kbar = max{1,1/gamma} for the largest such
  gamma" is undefined when L = 0 (every gamma is valid) and disagrees with
  def:growth, which allows any valid constant. Replaced with "Point growth
  implies weighted growth with kbar <= kappa". OPT is now defined before use,
  and w is described as a length.
* **Intro, scope paragraph.** "growth forces the Hessian block ... to be
  positive definite" is false for weighted growth, the hypothesis of Theorem
  1.1(b), which only gives positive semidefiniteness (lem:growthcert(b),
  rem:nonconvex). The paragraph now says: point growth gives positive definite,
  weighted growth gives positive semidefinite. The vague "it is not polynomially
  bounded there" now reads "no polynomial in I bounds kappa on all of them,
  since CT would then solve them in polynomial time".
* **Intro, snapping sentence.** k = poly(I) + log2(1/g_S) became
  k = poly(I) + max{0, log2(1/g_S)}, as in rem:setgrowth; the old form is wrong
  when g_S is large.
* **Intro, polynomial factors.** cor:poly assumes point growth; the sentence
  now says so.
* **Intro, chain.** The box widths are 2^t - 1 (lim:prop:messages, ex:chain),
  not 2^t.
* **Theorem 1.2.** In (c), the bag size p, on which the bound depends, is now
  part of the statement. In (d), "upper coordinate curvature".
* **Limits summary.** The sentence was ungrammatical. It now gives the list
  after "the following:". Prop:oraclebarrier concerns smooth functions and
  algorithms that query values and derivatives, so "no value-oracle algorithm
  certifies ..." became "for smooth functions with growth towards an unknown
  optimal set, an algorithm that queries only values and derivatives needs a
  number of queries that grows with the accuracy".
* **Notation clashes.** f is the specific function of Theorem 1.1(b). The intro,
  Table 1 and conclusion used f(p,kappa_S) for thm:diagdiscovery, whose function
  is f'; also f(p,kappa_nu) in open problem (1) and f(p,kappa_S,r) in open
  problem (4). All are now f' "for a computable function f'", as in
  thm:diagdiscovery and rem:grading. h was avoided because it is the mesh.
* **Table 1 caption.** "All upper bounds count bit operations" was false for the
  rows that count table entries, nodes, maximum flows or evaluations. It now
  reads "unless stated otherwise", and defines f' and n_c.
* **Undefined abbreviations.** QP (intro: "box QP"), TU (intro TU paragraph;
  used in Table 1), MIQP and MIP (related) are now defined at first use. A
  one-line gloss of kappa_c was added in the TU paragraph.
* **Duplicated comparisons (F11, CONVENTIONS section 1).**
  - The related-work sentences on exact piecewise-quadratic messages (DPK
    forests; Kolmogorov-Pock-Rolinek; Kuric-Ahmetspahic-Pock, nonconvex
    worst case) repeated sec:limits-messages almost word for word. They are now
    one sentence that keeps the citations and points to
    Section~\ref{sec:limits-messages}.
  - The Bienstock-Munoz constrained-approximation comparison appeared in the
    intro, in related and in rem:tu-bm. Related now only points to rem:tu-bm.
* **Related, balanced quadratics.** "polynomial in log(1/eps) and in kappa"
  became "polynomial in n, kappa and log(1/eps)", as in thm:balanced.
* **Conclusion.** CT now appears as "CT (Algorithm~\ref{alg:ct})" at its first
  use in the section. Open problem (1) says "point-growth constant" and that
  thm:cv measures p after elimination. Open problem (2) is qualified "under
  weighted growth".
* **Organization paragraph.** The recourse and TU appendices are now referenced
  by label (app:recourse-convex, app:recourse-cuts, app:tu). These labels exist
  in the current files. The appendices do follow section order (checked
  against appendix.tex).
* **Abstract.** "discard intervals without improving points" became "discard
  intervals that contain no improving point".

### Requests resolved since the front report

* optsets: thm:diagdiscovery now uses kappa_S and g_S, so request (2) is
  satisfied. The intro and Table 1 match it, with f'.

### Labels

None deleted or renamed. New labels are as listed in section (2) of the front
report.

### Checks run (targeted only; no project-wide verification, CI not consulted)

* `python3 process/w3/checks/front-verify-claims.py`, all checks pass. It checks
  in exact arithmetic:
  - f is increasing in kappa;
  - 8 kbar theta^2 <= 1 and 2^{mu*} <= 6 sqrt(kbar), which gives the
    O(sqrt(kbar) log(n+2)) cap of Theorem 1.1(b);
  - kbar <= kappa <= 2 for prop:lbwidth;
  - gamma = g/L gives kbar = kappa;
  - the kappa bound of lim:prop:unique.
* `pdflatex -output-directory=build/front-verify main.tex`, with bibtex run in
  the outdir (`BIBINPUTS=../..: bibtex main`), then pdflatex twice. Result:
  - 0 LaTeX errors;
  - no undefined references or citations in the whole document after the
    final bibtex run;
  - no overfull boxes in any file;
  - 123 pages.
* Rendered pages 2-6 (`pdftoppm -r 70`) and inspected Theorem 1.1, Theorem 1.2
  and Table 1 (page 6).
* Scans of the four files: all cited keys exist in references.bib (138 keys);
  no banned wording, British spellings, "Algorithm 1/2", "must grow" or
  "forced".

### Remaining

* F139 (Bajaj-Hasan Theorem 1 and its constant convention) is still
  unverified. The front files make no claim that depends on it.
* Table 1 and the extension paragraphs match the theorem statements as of this
  verification. If another group changes thm:cv, thm:valuefn, thm:cr-exact,
  thm:tu-approx, thm:cells or thm:diagdiscovery again, the corresponding rows
  must be rechecked.
* Theorem 1.2 starts at the foot of page 3 and its list continues on page 4.
  This is cosmetic, and final float and page placement belongs to the
  coordinator.

## Verification (front-verify, second pass)

A second, independent verification pass over `sections/abstract.tex`,
`sections/intro.tex`, `sections/related.tex` and `sections/conclusion.tex`,
run after all other groups had stopped editing (last change to any other
section file: 02:36). Only these four files were edited.

### What was checked

* **Adjudications.** All 58 findings in `assign/front.json` were checked
  against the diffs with `sections-before-w3/`. Every ACCEPTED fix is present.
  The MODIFIED decisions (F1, F6/F54/F114, F33, F74, F134, F137, F139) are
  justified. For F137, the Gupte-Koster-Kuhnke abstract (local KB) confirms
  that their discretization sizes are fixed, so R7's closing sentence would
  have been false. No finding should have been rejected.
* **Every summary statement against the current source**, re-read after the
  other groups finished: def:growth, lem:growthcert, rem:nonconvex,
  prop:cellwise, prop:filter, def:cert, thm:certificate, def:graded, alg:trial,
  lem:inv, lem:states, alg:ct, thm:approx, eq:logabsorb, rem:fpt, prop:sharp,
  cor:uniformgrid, ex:family, ex:chain, thm:transfer, rem:setgrowth, rem:np,
  alg:ex, thm:exact, cor:poly, ex:polylimits, lem:valuefunction, thm:valuefn,
  thm:cr-filter, prop:star, prop:vf-curv, thm:cv, rem:cv-instances,
  prop:cv-limit, cor:cv-nu, thm:cr-oracle, thm:cr-search, prop:cr-growth,
  thm:cr-exact, thm:balanced, thm:tu-approx and the paragraphs after it,
  sec:tu-limits, prop:tu-misaligned, ex:tu-sum, rem:tu-bm, prop:twocenters,
  thm:cells, thm:endpointset, cor:facecsp, thm:diagdiscovery, lim:prop:unique,
  lim:cor:nopolylog, lim:prop:oracle, lim:rem:oracle, prop:lbwidth,
  prop:lbproduct, lim:prop:messages, lim:prop:setgrowth, prop:oraclebarrier,
  lim:prop:constraints, and the computation results that are cited (chain
  table: 11 nodes at m=64; SCIP tolerances; QPLIB limits). Theorem 1.1(a)-(c),
  Theorem 1.2(a)-(d), the extension paragraphs and all 14 rows of Table 1
  match these statements, with the exceptions fixed below.
* **Re-derived:** Theorem 1.1(b) node bound (K_mu <= 60 sqrt(kbar)
  ceil(log2(n+2)) for every trial that runs); "no polynomial in I bounds kappa
  on the hard instances" (otherwise CT with p=3, q=ceil(log2(4m)) decides
  Subset Sum); the transfer of every lower bound from kappa to kbar <= kappa;
  open problem (1) from thm:cv(iii) and cor:cv-nu (kappa <=
  max{1,C_0} kappa_nu, so f(p,kappa)kappa^C(I+q+1)^C is of the form
  f'(p,kappa_nu)poly(I+q)); the weighted-growth block bound
  (H_{J0J0} >= 2 gamma diag(L_i)); the snapping exponent
  log2(1/eps_S) <= poly(I) + max{0, log2(1/g_S)}.
* **Literature spot checks (local KB):** Hladik-Cerny-Rada (fixed rank, any Q
  and q, polynomial: confirmed); Gupte-Koster-Kuhnke (fixed discretization
  sizes: confirmed).
* **CONVENTIONS:** claim wording (growth scope, FPT, lower bounds, TU, uniform
  cells, endpoint credits, Subset Sum credit), algorithm names and first-use
  form (CT, EX), reserved symbols, banned words, British spellings, and
  abbreviations (QP, MIQP, MIP, TU, ETH, rETH are defined at first use).

### What was fixed

* **Abstract.** "w is the largest adjacent grid interval" became "w is the
  length of the longest adjacent grid interval". "discard intervals that
  contain no improving point" became "discard intervals that cannot contain an
  improving point": the test is sufficient, and it does not remove every such
  interval. O(sqrt(kbar) log n) became O(sqrt(kbar) log(n+2)), as in Theorem
  1.1(b); the old form is false for n = 1.
* **Intro, setup.** kbar is invariant under rescaling of *continuous*
  coordinates only (Definition growth); the text now says so.
* **Intro, graded grids.** The sentence claimed O(sqrt(kbar) log n) nodes for
  every grading with 8 kbar theta^2 <= 1. For a small theta, Lemma states gives
  only 10 theta^{-1} ceil(log2(n_P+2)). The sentence now gives
  O(theta^{-1} log(n+2)) under the grading condition, and
  O(sqrt(kbar) log(n+2)) for theta of order 1/sqrt(kbar).
* **Intro, snapping sentence.** "the growth constant towards the optimal set"
  became "a growth constant g_S > 0 towards the optimal set; such a constant
  exists for every instance (Theorem transfer and Remark setgrowth)". Growth
  constants are not unique, and the sentence claims exactness without
  uniqueness.
* **Intro, scope paragraph.** Under weighted growth the paragraph claimed
  only positive semidefiniteness of the interior Hessian block. That holds at
  every minimizer, so it showed no restriction from growth. Lemma
  growthcert(b) gives H_{J0J0} >= 2 gamma diag(L_i), and the paragraph now
  states this bound. The "condition number can be large" sentence was
  reordered so that the claim (no polynomial bound unless P=NP) comes first
  and the upper bound log kappa = O(I) second. "We do not claim that it is
  moderate" now names kappa and kbar.
* **Intro, limits summary.** Cifuentes-Parrilo [Example 1.1] added next to
  Bienstock-Munoz for the running-sum encoding (CONVENTIONS section 5). This is
  the locator that limits.tex and the bib agent verified.
* **Intro, organization.** The list of "secondary results" in the appendices
  named Appendix proximal and Appendix tu. These appendices contain only
  proofs of main-text results (and the auxiliary Lemma tu-uniform). The list
  now names the boundary output (app:boundary), further recourse results
  including exact output with a cut residual (app:recourse-convex,
  app:recourse-cuts; thm:cr-exact is stated there) and the moment obstruction
  (app:moments, where lim:prop:moments is stated).
* **Table 1.**
  - The caption now says that f and f_1 are those of Theorem 1.1 and that C
    and C_1 are absolute constants unless stated otherwise. The rows for
    thm:exact and thm:cv used them without definition.
  - Row thm:valuefn: the recourse owner revised thm:valuefn during this pass
    (point growth; constants depend on the polynomial time bounds of the
    hypotheses; exact output needs a rational quadratic F). The row now reads
    "point growth of V (exact output: quadratic F with point growth)" and
    "C, C_1 depend on the polynomial time bounds".
  - Row thm:cells: added the exact-output bound K_S^p poly(I + log kappa_S).
    The row listed "exact minimizer" as output without a bound.
  - Row prop:lbproduct: the generic f(p) clashed with the specific f of
    Theorem 1.1 and is now f'(p).
* **Related work.**
  - Theorem balanced was described as "polynomial in n, kappa and
    log(1/eps)". Its bound (n kappa (I+q+1))^{O(1)} also depends on the input
    length, so the text now says "polynomial in the input length, kappa and
    log(1/eps)".
  - The Bhathena sentence had two semicolons in a row and was split into two
    sentences.
* **Conclusion.**
  - Open problem (1) said "A positive answer would need curvature measured
    only where near-optimal points can lie, or inequalities that couple both
    sides of a separator". This necessity is not proved. It now reads "These
    obstructions suggest ...".
  - Open problem (2) said "the factor p^p arises only when ... is bounded by
    ...", which was hard to parse. It now reads "comes only from the bound
    ceil(log2(n+2))^p <= 2p^p(n+2), which moves the logarithmic factor into
    the polynomial part". This inequality with n in place of n_P was checked
    exactly (see the checks below).

### Requests for other files (not edited)

1. **optsets** (optsets.tex, opening paragraph). "exactness itself costs only
   $\poly(I)+\log_2(1/g_S)$ bits of accuracy" should read
   "$\poly(I)+\max\{0,\log_2(1/g_S)\}$ bits", as in rem:setgrowth.
   Resolved: the optsets verifier made this change while this pass was
   running.
2. **core** (optional consistency). growth.tex (section opening) and
   growth-sharp.tex write $O(\sqrt{\bar\kappa}\log n)$. Theorem 1.1(b) and
   the abstract now use $\log(n+2)$, which is also correct for n = 1. The same
   applies to optsets.tex rem:grading and constraints.tex sec:tu-limits.

### Labels

None deleted or renamed. No new labels in this pass.

### Checks run (targeted; no project-wide verification; CI not consulted)

* `python3 process/w3/checks/front-verify-claims2.py` (new; exact
  arithmetic). All three checks pass:
  1. ceil(log2(n+2))^p <= 2p^p(n+2) for p <= 14 and every n with
     ceil(log2(n+2)) <= 60, checked at the extremal n for each value of the
     ceiling;
  2. Prop. cellwise(b) as summarized in the intro: the corrected grid minimum
     equals the best cell vertex bound, including the effective width 0 of
     integer unit intervals, on 300 random mixed instances with n = 2, 3;
  3. the snapping exponent bound.
* `python3 process/w3/checks/front-verify-claims.py` (from the first pass):
  all five checks pass.
* `latexmk -pdf -interaction=nonstopmode -outdir=build/front-verify main.tex`
  (exit 0; run after the last edit at 11:53). bibtex ran inside the outdir. Result: 0 LaTeX errors, no undefined
  references or citations, no overfull boxes in any file, 123 pages.
  A separate full pdflatex/bibtex/pdflatex x2 build in `build/front-verify2`
  before editing gave the same result.
* Rendered page 6 (Table 1) with `pdftoppm -r 80` and checked the layout after
  the row changes. Checked the abstract text on page 1 with `pdftotext`.
* Grep scans of the four files: no banned wording, British spellings,
  "Algorithm 1/2", "must grow" or "forced"; every all-caps abbreviation is
  defined at first use or standard (NP, SAT, QPLIB with citation in Section
  11).

### Remaining

* Other verifiers were still editing setting, grids, constraints, exact,
  limits and recourse files during this pass (changes up to 11:52). After
  their edits, the statements summarized in the front files were re-read:
  def:growth, lem:growthcert, rem:nonconvex, thm:certificate, thm:tu-approx,
  sec:tu-limits, rem:tu-bm, lim:prop:unique, lim:cor:nopolylog,
  lim:prop:oracle, prop:lbwidth, prop:lbproduct, lim:prop:messages,
  lim:prop:constraints, thm:exact, rem:setgrowth, thm:valuefn, thm:cv,
  cor:cv-nu and thm:cells. Only thm:valuefn had changed in a way that
  affected a front file (Table 1, fixed above). Any later change to these
  statements needs a recheck of Theorem 1.1, Theorem 1.2 and Table 1.
* F139 (Bajaj-Hasan Theorem 1 and its constant convention) is still
  unverified, because the full text is paywalled. The front files make no
  claim that depends on it. grids.tex (core) does not cite a theorem number
  either.
* Request (2) above is for other owners.
