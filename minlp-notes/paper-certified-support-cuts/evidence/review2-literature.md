# Review 2, lens: prior work, attribution and novelty

Date: 2026-10-03. Manuscript state: `sections/*.tex` and `main.pdf` of
2026-10-03 19:12. `development/draft-round2/` is byte-identical to the
current sources and PDF (checked with `diff -rq`), so the page numbers below
are those of `development/draft-round2/main.txt`.

## Summary

The attributions in the paper are mostly accurate, and the round-1 citation
audit (`review1-citation-audit.md`) has been acted on: Breen 1973,
Tawarmalani 2010 Ex. 3.8 and Cor. 3.10, Müller et al. 2022, Davarnia et al.
2017, Bao et al. 2009, Sherali–Adams, Shor, Grone et al., Waki et al.,
Laurent, Del Pia–Khajavirad Thm. 3, Bertelè–Brioschi, Bemporad et al.,
Bhathena et al., Margot 2009, the current MINLPLib and the journal version of
Dey–Khajavirad are now cited. All 94 DOI entries and all 13 arXiv entries of
`references.bib` agree with Crossref and arXiv. No cited result is misused
in a way that invalidates a theorem.

The remaining problems concern positioning, not correctness:

1. **Kojima–Kim–Arima 2026 is missing.** It is the closest recent work on
   gluing exact local relaxations along a sparsity pattern. Its bib entry is
   present, but no section cites it.
2. **SCIP's own cut cleanup is not acknowledged.** SCIP documents the
   stored-row rounding hazard and relaxes its own nonlinear cuts with
   variable bounds (SCIP 8 report, §4.2.10; `misc_rowprep.c`). The paper
   presents the hazard as a finding from reading `lp.c`.
3. **Proposition 3.5(ii) is uncredited.** It is the classical
   Lagrangian-decomposition duality (Guignard–Kim 1987), applied to pair
   hulls, but the paper lists it as a contribution without that credit.
4. **The SCIP separators used as baselines lack their original sources.**
   These separators (intersection, interminor, RLT with hidden products) are
   the comparators in a headline claim of the abstract.
5. **A cited theorem is used beyond its scope.** Burer–Natarajan–Willemsen,
   Thm. 1, holds for n ≤ 3, but the introduction and the conclusions
   generalize it. This overlaps referee finding F1 in `review2-referee.md`.

The two hedged novelty claims hold up within my search:
- exact support for nonconvex stars with center–leaf rows;
- the degree-two path example, the δ²/2 value and the use of the
  alternation criterion for κ-moment interfaces.

The claim "no published MINLP implementation certifies the exported rows" is
also supported, but it should acknowledge point 2.

## Method

- I read the paper as typeset (`development/draft-round2/main.txt`) and
  listed every `\cite` with `grep` over `sections/*.tex`. I also listed every
  novelty statement ("to our knowledge", "what we add", "new", "classical",
  "folklore", "established").
- I compared these with `evidence/literature-L1..L5.md`,
  `evidence/review1-citation-audit.md`, `evidence/coverage.md` and the local
  library `literature/papers/*/fulltext.md`.
- Sources I read in full text for this round:
  - Del Pia–Khajavirad arXiv 2609.35595v1: §1, Thm. 1–3, §2.5, refs.
  - Dey–Khajavirad arXiv 2508.18435v2, which I downloaded. Cor. 1, Thm. 1–2
    and Cor. 3–4 have the same numbering as v1, and v2 predates the journal
    version, which went online 2026-05-26.
  - Kojima–Kim–Arima arXiv 2606.21823: §2.1, §3.3.
  - Burer–Natarajan–Willemsen arXiv 2504.03996v3: Thm. 1 and the relaxation
    it covers, Ex. 4.
  - Lasserre 2006: Lemma 6.3, Lemma 6.4, Thm. 3.7.
  - Tawarmalani 2010: Ex. 3.8, Cor. 3.9, Cor. 3.10.
  - Xu–Pokutta arXiv 2608.03318: abstract, §1.
  - Anstreicher–Puges 2025: intro.
  - SCIP Optimization Suite 8.0 report (arXiv 2112.08872, downloaded): §4.2.7
    Presolve, §4.2.10 Cut cleanup, §4.3.3, §4.9, §4.11, refs [22], [44].
  - SCIP 10.0.2 source (GitHub tag v10.0.2): `src/scip/lp.c` and
    `src/scip/misc_rowprep.c`.
  - Szeider, VIPR from black-box ILP solvers (CP 2026).
- Bibliography: `verification/R9_literature_bibcheck.py` compares every DOI
  entry with Crossref, in title, author family names, journal, volume, issue,
  pages and year. It compares every arXiv entry with the arXiv API and
  searches Crossref for journal versions of the preprints. Output is in
  `verification/R9_literature_bibcheck.json`.
- Targeted web searches (2022–2026) covered:
  - simultaneous or joint convexification;
  - hulls of quadratic graphs on paths, trees and stars;
  - sparse vs dense Shor/moment/RLT relaxations, and gluing;
  - exact algorithms for box- and linearly-constrained QPs on trees and
    stars;
  - Lagrangian and aggregation cuts;
  - safe and certified cuts in MINLP/MILP (SCIP exact, VIPR);
  - SCIP nonlinear separators.
  I checked candidate references with the Crossref API.
- Numerical check: `verification/R9_literature_dense_star.py` (finding F5).

## What was verified and is fine

Not repeated as findings.

- Theorem 3.3 and Breen 1973: the finite-set criterion is the Radon-partition
  characterization for the moment curve. The text now attributes it, and
  claims only "its reading as a criterion for gluing interfaces"
  (03-composition.tex:199–208).
- Tawarmalani 2010, Ex. 3.8 (pp. 14–15) and Cor. 3.10 (p. 16) say what
  03-composition.tex:9–11 and 329–331 attribute to them.
- Lasserre 2006: Lemma 6.3 is the two-block gluing lemma (03:257), Lemma 6.4
  is the p-block version, and Thm. 3.7 is the rank condition (03:267).
- Dey–Khajavirad:
  - Cor. 1 is decomposability across a complete separator without plus
    loops.
  - Thm. 2 is the stable-set theorem for PP(G), and Cor. 4 is its QP(G)
    form. Its proof adds the products among N′(i).
  - The paper does not show that the no-plus-loop hypothesis is necessary.
    DK v2 has no such example either, and §7 lists open questions only.
  So "Proposition 3.1 shows that the hypothesis cannot be dropped" is a
  legitimate new remark.
- Del Pia–Khajavirad 2609.35595:
  - O(n²) operations and comparisons on forests (Thm. 1, p. 4);
  - strong NP-hardness at treewidth two (Thm. 3, p. 20);
  - quartic minimization on paths (Thm. 2, p. 18);
  - concave piecewise-quadratic value functions;
  - no linear constraints in the model.
  This matches 04-quadratic.tex:188–203, but see F7 on the order of
  "Theorems 2 and 3".
- Burer–Natarajan–Willemsen Thm. 1: the relaxation is Shor plus the RLT upper
  bounds, n ≤ 3, submodular data, and any signs of c. This is as stated at
  03-composition.tex:309–312. The problem is its extension in the
  introduction and conclusions (F5).
- SCIP 10.0.2 `lp.c` rounds near-integral coefficients when `!exact_enable`:
  - `rowAddCoef`, l. 2223–2225;
  - `rowChgCoefPos`, l. 2402–2403;
  - `rowMerge`, l. 6320–6321.
  This confirms 06-certification.tex:38–41.
- SCIP defaults (PySCIPOpt 6.2.1 / SCIP 10.0):
  - `separating/rlt/freq` = 0, but `hiddenrlt` and `detecthidden` are
    FALSE;
  - `separating/minor/freq` = 10;
  - `separating/interminor/freq` = −1;
  - `separating/eccuts/freq` = −1;
  - `nlhdlr/quadratic/useintersectioncuts` = FALSE.
  This is consistent with "separates RLT and semidefinite minor cuts" and
  with the list of disabled separators (02-setting.tex:153–165).
- Novelty claim on stars (01-introduction.tex:68–70; 04-quadratic.tex:212–213):
  - Web and library searches found no exact algorithm for nonconvex star
    QPs with rows that couple the center with one leaf.
  - DK, DK-SOC and Khajavirad (2601.18545, 2604.25033) are box-only.
  - Bienstock–Muñoz is approximate.
  - SDP-exactness results need sign conditions.
  The claim is adequately hedged, and the ingredients (nonserial DP,
  parametric QP) are credited.
- Novelty claim on certification (02-setting.tex:135–137): searches found
  only MILP certification work:
  - Eifler–Gleixner 2023/2024;
  - VIPR;
  - SCIP 10 exact mode;
  - Szeider, CP 2026 (VIPR certificates from floating-point ILP solvers);
  and whole-problem certificates for convex MINLP (Halbig et al. 2024). The
  claim stands, but see F2 and F8.
- Bibliography (R9_literature_bibcheck): all 94 DOI entries match Crossref.
  The flagged differences are encoding artifacts: "&amp;", "Van Hentenryck"
  vs "Hentenryck", "Kelley, Jr.", and a page range of "520–520". All 13 arXiv
  entries match title and authors. No preprint in the bibliography has a
  journal version that Crossref can find.

## Findings

Severity: critical / major / minor / suggestion. Locations are source
`file:line` and PDF page or section.

### F1 [major] The closest recent work on gluing local exact relaxations is not cited

- Location: sections/03-composition.tex:262–285 and 287–293 (Section 3.4,
  pp. 9–10). The bib entry `KojimaKimArima2026` (references.bib:851) is
  present but uncited.
- Issue. Section 3.4 positions the 1/128 path example against the
  sparse-moment and gluing literature. It omits Kojima, Kim and Arima,
  "Local-to-global exactness of SDP relaxations for sparse QCQPs"
  (arXiv:2606.21823, 2026). That paper assembles exactness of a sparse SDP
  relaxation from exact clique-wise sub-SDPs, which is the question the
  section studies. Its key restriction is directly relevant:
  - If two maximal cliques share more than one node, the shared off-diagonal
    entries impose product relations on local rank-one solutions. These
    relations "cannot be verified in advance".
  - The authors therefore assume a block-clique structure (cliques meet in at
    most one node) [KKA, §3.3, pp. 12–13].
  - Linear terms are handled by homogenization (§2.1). In the path example
    the homogenized cliques {1,x,y} and {1,y,z} share both m_y, an
    off-diagonal entry, and s_y.
  Proposition 3.1 is thus an explicit instance of the obstruction that KKA
  exclude by assumption, and it fails even with exact local hulls. KKA give
  no such example. A referee in this area will expect the comparison, and
  will notice the dropped citation.
- Related omissions:
  - Kim, Kojima, Toh (2020): exact gluing of DNN relaxations on block-clique
    graphs.
  - The SDP-exactness results on forests and bipartite graphs under sign
    conditions: Kim–Kojima 2003; Sojoudi–Lavaei 2014; Azuma, Fukuda, Kim,
    Yamashita 2022. Del Pia–Khajavirad (p. 2) cite these as the
    SDP-tightness literature for sparse box QPs. They are relevant to the
    paragraph on dense versus sparse Shor relaxations, but they do not cover
    the inhomogeneous family (6). With linear terms, the homogenizing
    variable closes cycles in the aggregate sparsity graph.
- Evidence: `literature/papers/kojima2026-local-to-global-exactness-of/fulltext.md`
  l. 45, 302–336. `grep KojimaKimArima2026 sections/*.tex` returns nothing.
  R9_literature_bibcheck reports it as an uncited entry. L2 lists KKA as
  must-cite (literature-L2.md:806).
- Fix. After "Finite gluing results require rank or flatness conditions on the
  overlaps [67, Theorem 3.7], [43]." (03:266–267) insert:
  > For sparse QCQPs, \citet{KojimaKimArima2026} assemble exactness of the
  > SDP relaxation from exact clique-wise subproblems. They assume that maximal
  > cliques meet in at most one node, because shared off-diagonal entries
  > impose product conditions that local exactness cannot control
  > \citep[Section~3.3]{KojimaKimArima2026}; block-clique structure also makes
  > doubly nonnegative relaxations exact \citep{KimKojimaToh2020}. In our path,
  > the homogenized cliques $\{1,x,y\}$ and $\{1,y,z\}$ share the off-diagonal
  > entry $m_y$ as well as $s_y$, and Proposition~\ref{prop:path-gap} shows that
  > this obstruction occurs even when the local relaxations are exact hulls.

  In the paragraph at 03:287–293, after the Grone/Waki/Laurent sentence, add:
  > Exactness of Shor relaxations on forests and bipartite graphs under sign
  > conditions \citep{KimKojima2003,SojoudiLavaei2014,AzumaEtAl2022} concerns
  > homogeneous formulations; the linear terms of \eqref{eq:family} add the
  > homogenizing variable to every clique, so these results do not apply here.

  Bib:
  - Kim, Kojima, Toh, J. Global Optim. 77(3):513–541, 2020,
    doi:10.1007/s10898-020-00879-y;
  - Kim, Kojima, Comput. Optim. Appl. 26(2):143–154, 2003,
    doi:10.1023/A:1025794313696;
  - Sojoudi, Lavaei, SIAM J. Optim. 24(4):1746–1778, 2014,
    doi:10.1137/130915261;
  - Azuma, Fukuda, Kim, Yamashita, J. Global Optim. 82(2):243–262, 2022,
    doi:10.1007/s10898-021-01071-6.

### F2 [major] SCIP's documented cleanup of its own nonlinear cuts is not acknowledged

- Location: sections/06-certification.tex:28–41 (Section 6.1, p. 18) and
  :56–66 (after Proposition 6.1). sections/02-setting.tex:132–137 (p. 5).
- Issue. The paper says: "What is specific to support cuts is that ... the
  stored row must be checked: outside its exact mode, SCIP 10 rounds a row
  coefficient that is integral within its tolerance to that integer, without
  adjusting the sides (functions rowAddCoef, rowChgCoefPos and rowMerge in
  src/scip/lp.c of [105])." This reads as a finding from the source code.
  SCIP documents both the hazard and a remedy:
  - The SCIP Optimization Suite 8.0 report, §4.2.10 "Cut cleanup" (pp. 35–36
    of arXiv 2112.08872), step 3, relaxes coefficients within 1e-9 of an
    integer with variable bounds. Its motivation is "to prevent the
    replacement of a_j by ⌊a_j⌉ that would occur when the cut is stored in a
    SCIP ROW, since that could make the cut invalid".
  - Step 4 handles right-hand sides near 0.
  - Step 1 removes terms by aggregating with bounds.
  - The cuts are discarded if the needed bounds are infinite or if
    violation is lost.
  - In SCIP 10.0.2, `misc_rowprep.c` `rowprepCleanupIntegralCoefs`
    (l. 419–500) implements this in floating point. When the needed bound is
    infinite, it rounds the coefficient anyway, "even though this will
    introduce an error".
  Prop. 6.1 and its rules (correct after merging, scaling and removal of tiny
  coefficients; discard when a bound is missing or violation is lost) are the
  exact-arithmetic counterpart of this cleanup. A SCIP-familiar referee will
  ask for it to be cited. The comparison helps the paper:
  - SCIP's remedy is floating point and only for its own cuts;
  - it has an unsafe fallback;
  - it does not check the stored row.
  L3 flagged "SCIP's own coefficient rounding (lp.c, misc_rowprep.c)"
  (literature-L3.md:767). Only lp.c made it into the paper.
- Evidence: /tmp download of arXiv 2112.08872, `scip8.txt` l. 1963–1996.
  GitHub `scipopt/scip` v10.0.2 `src/scip/misc_rowprep.c` l. 433–495.
- Fix. Replace 06-certification.tex:35–41, from "What is specific to support
  cuts" to "of \citealp{SCIPsource10}).", with:
  > SCIP's developers know the rounding hazard of the stored row: outside
  > its exact mode, SCIP~10 rounds a row coefficient that is integral within
  > its tolerance to that integer and drops coefficients below its epsilon,
  > without adjusting the sides (\code{rowAddCoef}, \code{rowChgCoefPos} and
  > \code{rowMerge} in \code{src/scip/lp.c} of \citealp{SCIPsource10}).
  > SCIP's nonlinear constraint handler therefore relaxes its own cuts with
  > variable bounds before storing them, in floating point, and rounds without
  > correction when the needed bound is infinite \citep[Section~4.2.10]{SCIP8report}.
  > Cuts added by an external separator receive no such treatment. What is
  > specific to support cuts is that the bound must be certified for the final
  > direction on the whole block domain, which is a global nonconvex
  > minimization, that the rounding correction is exact, and that the row SCIP
  > stores is compared with the certified row.

  Add `misc_rowprep.c` to the `SCIPsource10` entry or as a second software
  reference.

### F3 [major] Proposition 3.5(ii) is classical Lagrangian-decomposition duality, presented without credit

- Location: sections/03-composition.tex:343–366 and 384–393 (Prop. 3.5,
  pp. 10–11). sections/01-introduction.tex:61–62 ("We also relate the gain
  from merging pairs into a star to the glued relaxation", contribution 1,
  p. 2).
- Issue. Part (ii) states that the glued bound equals
  sup Σ_i min_{P_i} q_i′ over re-splittings with Σα_i = Σγ_i = 0. This is
  the Lagrangian-decomposition theorem of Guignard and Kim (1987; see also
  Geoffrion 1974), applied to the pair hulls with the shared coordinates
  (m_y, s_y) as copied variables:
  - optimizing over the intersection of the convex hulls equals the
    Lagrangian-decomposition dual;
  - the re-splittings are exactly the multipliers of the copy constraints.
  In sparse-moment language it is the degree-two case of the
  "interface polynomial" decomposition of sparse SOS certificates:
  Grimm–Netzer–Schweighofer 2007; Nie–Qu–Tang–Zhang 2026, Thm. 3.1 (L2,
  literature-L2.md:697–700, 721–733). The proof via Sion's minimax theorem is
  correct, but the paper lists the result as a contribution. L2 recorded that
  "the overlap gap is a Lagrangian-decomposition gap" (literature-L2.md:607–613,
  citing Khajavirad's thesis, Ch. 5, and Guignard–Kim). No section cites
  Guignard–Kim.
- Fix. Before Proposition 3.5 add:
  > Part~(ii) below is the Lagrangian-decomposition duality of
  > \citet{GuignardKim1987} applied to the pair hulls, with the shared moments
  > $(m_y,s_y)$ as copied variables; in the terminology of sparse moment
  > relaxations it says that the glued bound is the best split of the
  > objective with an interface polynomial of degree two in $y$
  > \citep{GrimmNetzerSchweighofer2007}, \citep[Theorem~3.1]{NieQuTangZhang2026}.
  > What is new is the use of exact pair and star minima to evaluate it.

  In the introduction replace "We also relate the gain from merging pairs
  into a star to the glued relaxation." with:
  > Through Lagrangian decomposition we also relate the gain from merging
  > pairs into a star, which the exact star algorithm computes, to the glued
  > relaxation.

  Bib:
  - Guignard, Kim, Math. Program. 39(2):215–228, 1987,
    doi:10.1007/BF02592954;
  - Grimm, Netzer, Schweighofer, Arch. Math. 89(5):399–403, 2007,
    doi:10.1007/s00013-007-2234-z.

### F4 [major] The SCIP separators used as baselines are cited only through SCIP overview papers

- Location: sections/02-setting.tex:153–167 ("Native SCIP", p. 5);
  sections/08c-minlplib.tex:102–112 (Section 8.3, p. 26); Section 8.5, p. 28.
- Issue. A headline claim of the abstract is that "SCIP's
  disabled-by-default separators were stronger". Those separators are
  intersection cuts for quadratic constraints, interminor cuts, RLT cuts with
  hidden products and edge-concave cuts. They are cited only as
  [BestuzhevaEtAl2025, SCIP10]. Their original sources are missing, although
  L5 listed them (literature-L5.md:637–700):
  - Intersection cuts from maximal quadratic-free sets: Muñoz–Serrano 2022.
    Their implementation and strengthening in SCIP: Chmiela–Muñoz–Serrano
    2023. The SCIP 8 report, §4.3.3, points to both.
  - Interminor cuts: intersection cuts from 2×2 minors of X = xxᵀ, based on
    outer-product-free sets (Bienstock–Chen–Muñoz 2020, already in the
    bibliography as [15]) and implemented with the Chmiela et al. machinery
    (SCIP 8 report, §4.11). The paper describes [15] only as "oracle-based
    cuts".
  - RLT cuts for implicit and explicit products, including hidden products:
    Bestuzheva–Gleixner–Achterberg 2025 (SCIP 8 report, §4.9; ref. [6]
    there).
  - Edge-concave cuts: Misener–Floudas 2012, already cited for the relaxation
    itself.
- Fix. Replace 02-setting.tex:160–165, from "Several cut families" to "with
  hidden products.", with:
  > Several cut families that target the same joint quadratic structure as
  > our cuts are implemented but disabled by default, because they have not
  > been found to pay off in general \citep{BestuzhevaEtAl2025,SCIP10}:
  > edge-concave cuts on aggregated quadratic terms \citep{MisenerFloudas2012},
  > intersection cuts for quadratic constraints from maximal quadratic-free sets
  > \citep{MunozSerrano2022,ChmielaMunozSerrano2023}, interminor cuts from
  > outer-product-free sets \citep{BienstockChenMunoz2020,ChmielaMunozSerrano2023},
  > and RLT cuts with hidden products \citep{BestuzhevaGleixnerAchterberg2025}.

  Bib:
  - Muñoz, Serrano, Maximal quadratic-free sets, Math. Program.
    192(1–2):229–270, 2022, doi:10.1007/s10107-021-01738-8;
  - Chmiela, Muñoz, Serrano, On the implementation and strengthening of
    intersection cuts for QCQPs, Math. Program. 197(2):549–586, 2023,
    doi:10.1007/s10107-022-01808-5;
  - Bestuzheva, Gleixner, Achterberg, Efficient separation of RLT cuts for
    implicit and explicit bilinear terms, Math. Program. 210(1–2):47–74,
    2025, doi:10.1007/s10107-024-02104-0.

### F5 [major] Burer–Natarajan–Willemsen Thm. 1 (n ≤ 3) is generalized in the introduction and the conclusions

- Location: sections/01-introduction.tex:56–61 (p. 2);
  sections/09-conclusions.tex:6–13 (p. 31); sections/03-composition.tex:287.
- Issue. The introduction says: "A dense semidefinite relaxation with the
  McCormick inequalities of the missing product closes every three-variable
  path, by a theorem of Burer et al. [25]; the advantage of joint blocks over
  their pairs is therefore one of representation". The conclusions state the
  same without the restriction to three variables. The cited theorem covers
  n ≤ 3. Its own Example 4 shows failure for n = 4. According to
  `review2-referee.md` F1, which re-ran BNW's data in
  `verification/R9_referee_path4.py`, that example is a four-variable path:
  - Q is tridiagonal;
  - the minimum is 0;
  - dense Shor with the McCormick inequalities of all products gives
    −0.12206.
  Four-variable blocks are the size the separator uses.
- My own check (`verification/R9_literature_dense_star.py`, Clarabel):
  - the dense relaxation is exact on the paper's three-leaf star of
    Section 3.5 (value 0.6666667 vs 2/3) and on Proposition 3.1 (0.0078125);
  - it is exact on 300 random three-leaf stars and 300 random four-variable
    paths with small integer data (worst gap 6e-8).
  So the "representation" reading often holds for small trees, but it is not
  a theorem beyond n = 3. The attribution "by a theorem of Burer et al."
  must not carry the general conclusion. The introduction also says "of the
  missing product", whereas the argument needs the McCormick inequalities of
  all products after complementation (03:312–318).
- Fix. Use the restricted wording proposed in `review2-referee.md` F1 for
  01-introduction.tex:56–61, 03-composition.tex:287 and
  09-conclusions.tex:6–13. Add after 03:323:
  > For four variables this is no longer true: on the path of
  > \citet[Example~4]{BurerNatarajanWillemsen2025} the dense relaxation with the
  > McCormick inequalities of all products has value about $-0.122$, whereas the
  > minimum, and hence the support value of the block in that direction, is $0$.

### F6 [minor] The related-work sentence credits the low-dimensional hull results to Shor and Sherali–Adams

- Location: sections/02-setting.tex:100–105 (Section 2.1, p. 4).
- Issue. "The convex hull of {(x,xxᵀ)} is described by semidefinite and RLT
  constraints [Shor1987, SheraliAdams1990] over a simplex of dimension at most
  three and over a box in dimension two, and polytopes of dimension at most
  three admit an extended formulation built from a triangulation
  [AnstreicherBurer2010]". Citation placement attributes the simplex and box
  results to Shor and Sherali–Adams. These results are Anstreicher–Burer 2010
  (preprint Thm. 3, Cor. 4, Thm. 6). Shor and Sherali–Adams are only the
  sources of the constraint families.
- Fix:
  > \citet{AnstreicherBurer2010} show that the convex hull of $\{(x,xx\T)\}$ is
  > described by the semidefinite and RLT constraints \citep{Shor1987,SheraliAdams1990}
  > over a simplex of dimension at most three and over a box in dimension two, and
  > that polytopes of dimension at most three admit an extended formulation built
  > from a triangulation; for the box in dimension three these constraints, even
  > with the triangle inequalities, are not enough
  > \citep{AnstreicherBurer2010,BurerLetchford2009,Anstreicher2012}.

  Anstreicher–Puges 2025 (arXiv 2501.09150), intro, confirms the last
  clause.

### F7 [minor] Fixed-dimension strong polynomiality is unattributed, and the Del Pia–Khajavirad theorem numbers are swapped

- Location: sections/04-quadratic.tex:66–72 and 91–93 (Section 4.1, p. 12).
- Issue 1. "For fixed d the algorithm is therefore strongly polynomial ... in
  line with the result that quadratic programming is in NP [Vavasis1990]. ...
  what we add is the treatment of the degenerate cases that a certificate must
  cover." Del Pia–Khajavirad (2609.35595, p. 1) state: "If the number of
  variables is fixed, then the problem can be solved in strongly polynomial
  time using a simple face enumeration argument [40, 10]", where [40] is
  Vavasis 1990 and [10] is Del Pia–Dey–Molinaro 2017. The core of the proof of
  Theorem 4.1 is the usual way to show that an optimum has polynomial size:
  - a minimizer in the relative interior of a minimal face;
  - H positive definite on that face;
  - hence a unique solution of a nonsingular system.
  Compare Vavasis 1990; I could not access its full text, so this is my
  reading of the standard argument. "What we add" should name the parts that
  are new:
  - enumerating independent row sets;
  - redundant, opposite and implied-equality rows;
  - the emptiness test;
  - the explicit encoding bounds;
  - use as a replayable certificate.
- Issue 2. The sentence at 04:91–93 says "strongly NP-hard already at
  treewidth two, and quartic minimization already on paths [34, Theorems 2
  and 3]". In DK, Theorem 3 is treewidth two and Theorem 2 is the quartic
  path result.
- Fix 1. Replace 04:68–72 with:
  > For fixed $d$ the algorithm is therefore strongly polynomial, as known for
  > face enumeration \citep{Vavasis1990,DelPiaDeyMolinaro2017}, and the minimum
  > has polynomial encoding length. The method is total enumeration of faces
  > \citep[Section~2.9]{Murty1997}; what we add is a statement that covers every
  > degenerate case a certificate meets (redundant, opposite and implied-equality
  > rows, empty polytopes, singular faces) and explicit size bounds.

  Bib: Del Pia, Dey, Molinaro, Mixed-integer quadratic programming is in NP,
  Math. Program. 162(1–2):225–240, 2017, doi:10.1007/s10107-016-1036-0.
- Fix 2: "already at treewidth two \citep[Theorem~3]{DelPiaKhajavirad2026},
  and quartic minimization already on paths \citep[Theorem~2]{DelPiaKhajavirad2026}".

### F8 [minor] Recent and directly related work is missing

- Location:
  - sections/02-setting.tex:93–97 (aggregations of quadratic constraints,
    p. 4);
  - sections/01-introduction.tex:21–23 ("vectors of univariate functions",
    p. 1);
  - sections/02-setting.tex:118–137 (rigorous relaxations, p. 5);
  - sections/05-original.tex:125–135 (Section 5.2, p. 16).
- Issue. A referee would expect four more works:
  1. **Xu and Pokutta, Joint-range inequalities for nonconvex QCQPs**
     (arXiv:2608.03318, Aug 2026, ZIB). It convexifies the joint range of two
     quadratic functions, takes closed-form hulls in the nonconvex cases, and
     lifts the support inequalities back to sparse cuts for MINLP. This is
     joint convexification of several quadratic functions for solver cuts, as
     in this paper. It belongs next to Dey–Muñoz–Serrano and
     Blekherman–Dey–Sun. Round 1 and L1 (literature-L1.md:59, 360) flagged it,
     and it is still not cited.
  2. **He, Liu, Tawarmalani, Convexification techniques for fractional
     programs**, Math. Program. 213(1–2):107–149, 2025,
     doi:10.1007/s10107-024-02131-x. It gives exact simultaneous hulls of
     vectors of univariate functions (powers, reciprocals) through moment
     hulls. The introduction claims "vectors of univariate functions" but
     cites no paper that does exactly this. It is on L1's must-cite list
     (literature-L1.md:305–316, 1068).
  3. **Saxena, Bonami, Lee, Convex relaxations of non-convex mixed integer
     quadratically constrained programs: projected formulations**, Math.
     Program. 130(2):359–413, 2011, doi:10.1007/s10107-010-0340-3. It
     generates cuts in the original variable space from projected lifted
     (x, X) relaxations for MIQCPs. This is the closest QCQP precedent for
     Section 5's motivation: cuts in original variables, without auxiliary
     variables.
  4. **Halbig, Hümbs, Rösel, Schewe, Weninger, Computing optimality
     certificates for convex mixed-integer nonlinear problems**, INFORMS J.
     Comput. 36(6):1579–1610, 2024, doi:10.1287/ijoc.2022.0099. It is the
     MINLP counterpart of the VIPR line. Citing it shows that the paper knows
     MINLP certification work, and it sharpens the claim at 02:135–137,
     because Halbig et al. certify whole convex solves, not cuts.
- Fix. At 02:96–97 add "and the joint-range inequalities of
  \citet{XuPokutta2026}, which convexify the joint range of two quadratic
  functions and lift the result to sparse cuts,". At 01:23 and 02:66 add
  \citet{HeLiuTawarmalani2025}. At 05:130–135 add "Cuts in the original space
  derived from lifted quadratic relaxations by projection are studied by
  \citet{SaxenaBonamiLee2011}." At 02:124 add "certificates of optimality for
  convex MINLPs are computed by \citet{HalbigEtAl2024};".
- Optional, as suggestions:
  - Khademnia–Davarnia, Math. Oper. Res. 50(2):1019–1041, 2025,
    doi:10.1287/moor.2023.0001 (bilinear terms over network polytopes);
  - Kuznetsov–Sahinidis, J. Global Optim. 92(1):1–20, 2025,
    doi:10.1007/s10898-025-01464-x (an application of simultaneous
    convexification);
  - Khajavirad, arXiv:2604.25033, 2026 (polynomial-time sparse box POPs). DK
    call it the work most closely related to theirs.

### F9 [minor] The abstract and the conclusions present known facts as findings of the paper

- Location: sections/00-abstract.tex:5–6 (p. 1); sections/09-conclusions.tex:3–6
  (p. 31).
- Issue 1. Abstract: "Exact pair hulls glued on shared moments do not
  compose:". Section 3 says that the phenomenon is known (03:5–11, citing
  Lasserre, Nie–Demmel, Fantuzzi–Fuentes and Tawarmalani Ex. 3.8). The new
  parts are the quantification and the criteria. Round 1 raised this as
  finding 20, and the sentence is unchanged.
- Issue 2. Conclusions: "Two consequences of the theory matter for solver
  design. First, certification does not constrain how directions are found".
  Section 6.1 credits this principle to Garloff–Jansson–Smith §5,
  Neumaier–Shcherbina p. 294 and Borradaile–Van Hentenryck. It is not a
  consequence of this paper's theory.
- Fix 1, abstract:
  > Exact pair hulls glued on shared moments are known not to compose; we
  > quantify this: for a family ...
- Fix 2, conclusions:
  > Two points matter for solver design. First, as in safe-cut practice,
  > certification does not constrain how directions are found: ...

### F10 [minor] Unsupported claims that merged blocks are mostly stars

- Location: sections/04-quadratic.tex:97–98 (Section 4.2, p. 12);
  sections/09-conclusions.tex:13 (p. 31).
- Issue:
  - "Section 3 shows that the blocks worth merging are often stars" — Section
    3 studies three-variable paths and one diagnostic proposition for stars.
    It shows nothing about frequency.
  - "For stars, the most common merged blocks" — there is no evidence: in
    Section 8 no block had more than four variables, and "the star algorithm
    ... was not needed there" (08f-star.tex; p. 30).
- Fix. 04:97–98:
  > The merged blocks of Section~\ref{sec:composition} are stars: several
  > pairs that share one variable.

  09:13:
  > For stars, the merged blocks of Section~\ref{sec:composition}, ...

### F11 [minor] SCIP's implicit-discreteness presolve is described imprecisely, and its source is not credited

- Location: sections/02-setting.tex:157–160 (p. 5); sections/08e-path.tex:86–90
  (Section 8.5, p. 28).
- Issue. "Its presolve fixes a variable that occurs in a single nonlinear
  constraint, in which the constraint function is concave in that variable,
  to one of its bounds". SCIP 8 report §4.2.7 "Implicit Discreteness"
  (pp. 29–30) restricts x to {lb, ub}; it does not fix x. The conditions it
  states are:
  - a non-binary variable with finite bounds;
  - no objective coefficient;
  - occurrence in exactly one constraint;
  - a polynomial constraint in which x appears only as c_k x^{2k} or with
    exponent 1;
  - all c_k of one sign;
  - g concave with an infinite left side, or g convex with an infinite right
    side.
  If the bounds are [0, 1] the type becomes binary; otherwise a bound
  disjunction is added. The report credits the idea to Hansen, Jaumard, Ruiz
  and Xiong (1993), the same observation that Del Pia–Khajavirad use (p. 2).
  The paper's wording follows the SCIP parameter docstring, but its condition
  list is incomplete: it omits the objective condition and the convex case.
- Fix. 02:157–160:
  > Its presolve restricts a variable to its two bounds if the variable has no
  > objective coefficient and occurs in a single polynomial constraint that is
  > concave (convex) in it with an infinite left-hand (right-hand) side, and makes
  > it binary when its bounds are $[0,1]$ \citep[Section~4.2.7]{SCIP8report};
  > the idea goes back to \citet{HansenEtAl1993}.

  Bib: Hansen, Jaumard, Ruiz, Xiong, Global minimization of indefinite
  quadratic functions subject to box constraints, Naval Res. Logist.
  40(3):373–392, 1993, doi:10.1002/1520-6750(199304)40:3<373::AID-NAV3220400307>3.0.CO;2-A.

### F12 [suggestion] Bibliography hygiene and locator versions

- Location: references.bib; sections/03-composition.tex:263–264.
- Points:
  - Remove or cite the uncited entries `FuriniEtAl2018` and
    `KojimaKimArima2026`; F1 cites the latter.
  - Add arXiv:2112.08872 to `SCIP8report`; it is the accessible version and
    the source of the section numbers.
  - Nie–Demmel Ex. 3.5 and Nie–Qu–Tang–Zhang Ex. 6.7 were verified only on
    arXiv math/0606476v3 and 2406.06882v3 (round 1, L2), while the
    bibliography cites the journal versions. Check the numbering in the
    journal versions or write "Example 3.5 of the arXiv version".
  - Dey–Khajavirad numbering is stable between v1 and v2. The QP(G) form of
    the stable-set theorem is Cor. 4, so "[35, Theorem 2 and Corollary 4]" is
    more precise at 03:277.
  - Keys `DeyKhajavirad2025` and `BhathenaEtAl2025` carry 2026 entries. This
    is harmless for readers but confusing for coauthors.

### F13 [suggestion] Lemma D.1 cites a secondary source for the Bernstein enclosure property

- Location: sections/A-bounds.tex:17 (Appendix D, p. 44).
- Issue. "Bernstein enclosure; see Garloff–Smith 2008". The range-enclosure
  property of Bernstein coefficients is classical: Cargo and Shisha 1966 for
  the univariate case, Garloff 1986 for the multivariate case. Garloff–Smith
  2008 is an application paper.
- Fix: "see, e.g., \citealp{GarloffSmith2008} and the references therein", or
  cite Cargo–Shisha (J. Res. Nat. Bur. Standards 70B:79–81, 1966).

## Novelty statements: verdicts

| Location | Statement | Verdict |
|---|---|---|
| 00:5–6 | "Exact pair hulls ... do not compose:" | Reframe (F9) |
| 01:52–56, 03:199–208 | alternation = Radon partitions on the moment curve; "what the theorem adds is its reading as a criterion for gluing interfaces" | Correctly attributed and hedged |
| 01:56–61, 09:6–13 | "advantage ... is therefore one of representation" | Overgeneralized from BNW n ≤ 3 (F5) |
| 01:61–62 | gain from merging related to glued relaxation | Classical duality, needs credit (F3) |
| 01:67–70, 04:212–213 | no exact algorithm for stars with center–leaf rows | Supported within search; hedged |
| 03:283–291 | example, δ²/2, alternation use "have not been given before" | Supported within search; position against KKA 2026 (F1) |
| 04:70–72 | "what we add is the treatment of the degenerate cases" | Narrow and attribute fixed-d strong polynomiality (F7) |
| 02:135–137 | no MINLP implementation certifies exported rows | Supported; acknowledge SCIP cleanup (F2) and Halbig et al. (F8) |
| 06:28–41 | "What is specific to support cuts ... stored row must be checked" | Acknowledge SCIP 8 §4.2.10 (F2) |
| 09:3–6 | certification independent of direction search as a consequence of the theory | Established principle (F9) |
| 01:100–101 | no new convexification principle, no general speedup | Fine |

## Bibliography check (R9_literature_bibcheck)

- 114 entries. 94 have a Crossref DOI, and 13 arXiv identifiers were
  checked. Two entries are uncited (`FuriniEtAl2018`, `KojimaKimArima2026`).
  No key is cited without an entry.
- DOI entries: title, author family names, journal, volume, issue, pages and
  year agree with Crossref for all 94. The script flags 6 entries, all
  encoding or parsing artifacts: `AdjimanEtAl1998`, `SmithPantelides1999` and
  `Vorobev1962` ("&amp;"); `BorradaileVanHentenryck2005` ("Van Hentenryck");
  `Kelley1960` ("Jr."); and `Rabinowitsch1930` (page range "520–520"). The 40
  most important cited items are among the 94 and match, including:
  - Tawarmalani–Sahinidis 2004/2005, Liers et al. 2021, He–Tawarmalani ×3,
    Davarnia et al. 2017, Bao et al. ×2, Misener–Floudas 2012;
  - Anstreicher–Burer 2010, Anstreicher 2012, Burer–Letchford 2009,
    Lasserre 2006, Nie–Demmel 2009, Nie et al. 2026, Waki et al. 2006,
    Grone et al. 1984, Padberg 1989, Vorob'ev 1962, Breen 1973;
  - Chen–Luedtke 2022, Müller et al. 2022, Dey–Muñoz–Serrano 2022,
    Blekherman–Dey–Sun 2024;
  - Neumaier–Shcherbina 2004, Cook et al. 2009, Eifler–Gleixner 2023/2024,
    Cheung–Gleixner–Steffy 2017, Cook–Koch–Steffy–Wolter 2013;
  - Borradaile–Van Hentenryck 2005, Domes–Neumaier 2012/2016,
    Bestuzheva et al. 2025, Müller–Serrano–Gleixner 2020,
    Bienstock–Chen–Muñoz 2020, Bienstock–Muñoz 2018;
  - Bhathena et al. 2026, Dey–Khajavirad 2026 (online first; Crossref has no
    volume or pages yet), Sion 1958, Vavasis 1990, Moré–Vavasis 1990.
- arXiv entries: all titles and authors match. The script's "DelPia" vs "Pia"
  and SCIP 10 author-name differences are parse artifacts. Versions:
  - Del Pia–Khajavirad v1, 2026-09-28. It is five days old and unrefereed;
    the paper relies on it only for the box case and for hardness.
  - Khajavirad 2601.18545 v2; Zhu–He–Tawarmalani v1;
    Burer–Natarajan–Willemsen v3 (2026-08-31); Fantuzzi–Fuentes v3
    (2026-07-06); SCIP 10 2511.18580 v1; KKA v1.
  - No journal versions were found.
- `SCIP8report`: 35 authors and title match arXiv 2112.08872.

## Targeted commands run (this lens)

All checks are local and targeted. No SCIP or Gurobi solve was run, and no
project-wide tests or CI were used.

- `diff -rq development/draft-round2/sections sections` (identical).
- `verification/R9_literature_bibcheck.py` (Crossref + arXiv;
  `OMP_NUM_THREADS=1` etc.; output `R9_literature_bibcheck.json`). The first
  run crashed on an accent-map bug, which I fixed; the second run completed.
- `verification/R9_literature_dense_star.py`, and the same script with the
  `random` argument (cvxpy + Clarabel, single thread). Outputs are
  `R9_literature_dense_star.json` and `R9_literature_dense_star_random.json`.
- PySCIPOpt parameter query for separator defaults (`getParam`, no solve).
- Downloads to `/tmp/r9lit/`, not kept in the repository:
  - SCIP 8 report (arXiv 2112.08872);
  - SCIP v10.0.2 `lp.c` and `misc_rowprep.c`;
  - Dey–Khajavirad arXiv 2508.18435v2;
  - Del Pia–Dey–Molinaro arXiv 1407.4798;
  - CP 2026 paper 52.
- Crossref queries for the candidate references listed in F1, F3, F4, F7,
  F8 and F11.

These checks do not replace CI. CI handles project-wide verification.
