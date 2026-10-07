# Kernel and sparse SOS citation verification

Status: final reader/citation verification for the 17 assigned manuscript
keys. This is a bounded citation audit, not a priority search or an independent
literature run. The two Tran–Toh keys identify versions of the same work.

## Metadata and source-content status

“Metadata verified” means the title, authors, and publication or preprint
record were checked against Crossref, arXiv, PMLR, the publisher, or the
retained slide title page. “Content read” is stated separately and identifies
the text or preserved original used for each claim. It does not certify
independent proof correctness. Lasserre and Waki are existing read packages
in the KB; Magron's set-products article is also an existing read package.
The remaining open-source contracts were read from primary sources or the
retained source audit, but their packages are absent from the KB.

| Current key | Canonical bibliography key | Metadata verification | Source-content verification and local KB state |
|---|---|---|---|
| baldi2024-putinar-hypercube | baldi2024-putinar-hypercube | Crossref DOI 10.1137/23M1555430; SIAM Journal on Applied Algebra and Geometry 8(1), 1–25 verified. | Read arXiv v3 primary HTML. Theorem 3 gives the dense cube ordinary-module degree upper bound (detailed statement with constants: Theorem 11); Theorem 4 gives a different dense-module lower-bound example. No KB package. |
| catala2024-singular-measures | catala2024-singular-measures | Crossref DOI 10.1007/s00365-024-09686-0; Constructive Approximation 60(3), 405–442 verified. | Read publisher primary HTML. Remark 3.7 is the equal-low-order-Fourier-moments/equal-Jackson-convolution statement; Theorem 3.3 supplies the Wasserstein smoothing bound. No KB package. |
| dklerk2017-improved-upper-bounds | dklerk2017-improved-upper-bounds | Crossref DOI 10.1137/16M1065264; SIAM Journal on Optimization 27(1), 347–367 verified. Author is Roxana Hess. | Primary author PDF and source audit read. The result concerns dense upper-bound hierarchies using polynomial densities and Schmüdgen-type box certificates, with order O(r^-2); its Jackson kernel is a precedent. It is not a lower hierarchy or a sparse overlap theorem. No KB package. |
| gamertsfelder2025-countable-gmp | gamertsfelder2025-countable-gmp | arXiv API metadata for v4, arXiv:2501.09385; title, authors and version verified. | Read primary HTML v4. Equation (3), Assumption 9, Theorem 13 and Corollary 14 give effective-positivity transfer conditional on an attained dual in the finitely-supported multiplier space. This does not give the manuscript's unconditional finite-order consistency construction. No KB package. |
| gribling2026-squared-kernels | gribling2026-squared-kernels | arXiv API metadata for v1, arXiv:2605.31496; title, authors and version verified. | Read primary HTML v1. Sections 3–4 and Theorem 7 give the dense ordinary box-module O(log^3(r)/r^2) rate under the theorem's stated parameter conditions. It supplies the squared-kernel/normalization precedent, not sparse marginal gluing. The source audit did not independently verify its main proof. No KB package. |
| grimm2007-structured-sparsity | grimm2007-structured-sparsity | Crossref title query and DOI 10.1007/s00013-007-2234-z; Archiv der Mathematik 89(5), 399–403 verified. | Read the open author manuscript. Lemma 3 and its proof use running intersection and strict positivity to approximate separator fiber minima and obtain sparse SOS representations. It is not a quantitative finite-rate or zero-margin result. No KB package. |
| han2018-local-moment-matching | han2018-local-moment-matching | Official PMLR record: volume 75, COLT 2018, pages 3189–3221; title and authors verified. | Read PMLR primary PDF. Lemma 25, printed pp. 23–24, identifies the largest discrepancy between probability laws sharing their first n moments as twice the degree-n best uniform approximation error. An affine interval change preserves the statement used here. No KB package. |
| korda2025-convergence-rates-sparsity | korda2025-convergence-rates-sparsity | Crossref DOI 10.1007/s10107-024-02071-6; Mathematical Programming 209(1–2), 435–473, online 25 March 2024, verified. | Read the published primary HTML/PDF and retained source audit. Theorem 6 gives sparse box-preordering rate O(r^(-2/(w+3))) for fixed data in the manuscript's width notation (the paper states degree O(epsilon^(-(J+3)/2)) using its largest-bag parameter and coordinatewise truncation). Theorem 8 covers sparse ordinary modules on general domains under running intersection, normalized local Archimedean certificates, and local Łojasiewicz assumptions. With local exponent 1, displayed eqs. (5)–(6) imply O(r^(-18/(238+55w))); the manuscript's weaker qualitative description is safe. No KB package. |
| lasserre2006-convergent-sdprelaxations-in-polynomial-optimization | lasserre2006-convergent-sdprelaxations-in-polynomial-optimization | Crossref DOI 10.1137/05064504X; SIAM Journal on Optimization 17(3), 822–843 verified. | Read local paper.md/fulltext.md and compared claims against the original PDF. Theorem 3.6 gives qualitative sparse SDP convergence under its boundedness/local-support assumptions; Appendix Lemma 6.4 and surrounding proof glue consistent local representing measures. It does not give the manuscript's finite-order rate for arbitrary truncated functionals. KB package present and read. |
| laurent2023-effective-schmudgen | laurent2023-effective-schmudgen | Crossref DOI 10.1007/s11590-022-01922-5; Optimization Letters 17(3), 515–530, online 2022, verified. | Read open CWI full text. The dense box full-preordering lower hierarchy has O(r^-2) convergence; Proposition 6 bounds the Jackson eigenvalue defect by a constant times k^2/(r+2)^2. This does not establish ordinary-module or sparse-overlap results. No KB package. |
| magron2025slides-lorentz | magron2025slides-lorentz | Retained primary slide title page: Victor Magron, Lorentz Center lecture, 7 July 2025; PDF title/date verified. | Visually read slide 23/44 (PDF p. 90). It defines full local preorderings for two overlapping bags, total-degree truncation 2d, and asserts a sparse gap O(d^-2), attributed to Korda, Ríos-Zertuche and Magron. This is a public slide assertion, not a peer-reviewed theorem proof. No KB package; retained PDF is present. |
| magron2026-convergence-rates-for-polynomial-optimization | magron2026-convergence-rates-for-polynomial-optimization | Crossref DOI 10.1137/25M1773416; SIAM Journal on Optimization 36(3), 1867–1886 verified. | Read local KB note/full text and compared the cited claims to the original. Theorem 11 and Corollary 12 give O(t^-2) for dense full preorderings on stated Cartesian products of spheres, balls, simplexes and hypercubes under the paper's factor-kernel assumptions. It does not prove sparse overlap consistency or ordinary-module transfer. KB package present and read. |
| magron2026slides-tenors | magron2026slides-tenors | Retained primary slide title page: Victor Magron, TENORS Learning Week 2, UiT The Arctic University of Norway, 16 February 2026; title/date verified. | Visually read slide 35/90 (PDF p. 121). It repeats the sparse two-bag full-preordering inverse-square assertion; its separate sparse Putinar mention gives no exponent. Neither slide resolves the difference from the published Korda Theorem 6. No KB package; retained PDF is present. |
| nie2026-sparse-tightness | nie2026-sparse-tightness | Crossref DOI 10.1007/s10107-025-02223-2; Mathematical Programming 215(1–2), 369–405, online 2 May 2025, verified. | Read open primary HTML. Theorem 3.1 characterizes finite tightness through polynomial bag separator multipliers/decompositions. Example 6.7 gives a quartic two-bag box problem whose fiber minima force a rational nonpolynomial separator and whose sparse hierarchy is not finitely tight, although the dense hierarchy is exact at order two. This is a qualitative precedent, not an inverse-square lower bound. No KB package. |
| tran2026-moment-sos-approximation | tran2026-truncated-moment-sequences | Crossref DOI 10.1007/s10107-026-02394-6; Mathematical Programming publication date 7 July 2026; title/authors verified. | This is the published version of the same work as arXiv:2507.00572v1, not a separate study. The published full text was not accessible; only its metadata and abstract are verified. The inspected preprint's Theorem 4.7/Corollary 4.8 support the manuscript's comparison to dense preordering bounds with the same global Hölder exponent. See the next row for version locators and caveat. |
| tran2026-truncated-moment-rates | tran2026-truncated-moment-sequences | arXiv API metadata for v1, arXiv:2507.00572; title, authors and version verified. Same work as the 2026 published article above. | Read primary preprint HTML/PDF. Theorem 3.5 gives fixed-degree moment approximation on products of balls/simplexes; Theorem 4.7 and Corollary 4.8 give a global Hölder rate for the dense reduced hierarchy, and the stated full-preordering rate has the same global exponent. This supports the §08 comparison. Independent local application does not make separator marginals agree, and the source's reduced cone still retains inequality-generator products. Keep these preprint locators distinct from any final published locators. No KB package. |
| waki2006-sparse-sos | waki2006-sums-of-squares-and-semidefinite | Crossref DOI 10.1137/050623802; SIAM Journal on Optimization 17(1), 218–242 verified. | Read existing KB note/full text. The paper introduces correlative sparsity patterns and chordal-clique sparse SOS/SDP relaxations; its order-one quadratic result preserves the dense SDP value for the stated class. It does not itself prove sparse hierarchy convergence in general. Existing canonical KB package is present and read. |

## Priority-critical contract and required manuscript wording

The two retained Magron slide PDFs make the inverse-square sparse
preordering rate a prior public assertion: Lorentz 2025 slide 23/44
(physical PDF p. 90) and TENORS 2026 slide 35/90 (physical PDF p. 121).
Both show two overlapping bags, local full preorderings and total-degree
truncation, and both attribute the inverse-square statement to Korda,
Ríos-Zertuche and Magron. The published Korda Theorem 6 instead gives
O(r^(-2/(w+3))) for fixed data (its parameter is largest bag size; its
degree bounds are coordinatewise). Width-dependent conversion to total
degree changes constants, not the exponent. The discrepancy is unresolved:
do not dismiss the slides as a typo, infer a hidden hypothesis, or cite
published Theorem 6 as proving inverse-square. The manuscript's explicit
statement that the rate is not new and that the discrepancy remains open is
supported.

The dense ordinary-module rate O(log^3(r)/r^2) is prior to Gribling,
de Klerk and Vera, Theorem 7. The sparse ordinary overlap transfer is the
distinct candidate result. Korda Theorem 8 is a broader-domain ordinary
module comparison under additional local assumptions. Gamertsfelder–Mourrain
also requires dual attainment in the finitely-supported multiplier space;
that assumption is different from finite-SDP dual attainment. Do not say
their framework proves the manuscript's unconditional construction.

Sharpness language must keep Nie et al.'s rational-separator, no-finite-
tightness example qualitative. Han Lemma 25 is the established
moment-matching/best-approximation identity. Baldi–Slot's dense
ordinary-module obstruction is different from the sparse overlap example.
None of these sources establishes the manuscript's new quantitative sparse
quadratic lower bound.

Catala et al.'s exact Jackson smoothing statement is for trigonometric
polynomials on the torus. Its use after a cosine/even pushforward to
Chebyshev moments is an inference in the manuscript's setting, not a
separate sparse SDP theorem.

## Exact manuscript uses and cautious corrections

- sections/01-introduction.tex, lines 18–29, 143–190 and 192–202, distinguishes
  dense preordering, dense ordinary module, published Korda sparse exponent,
  earlier slides, no attainment requirement and the qualitative Nie
  precedent. Keep that distinction and the explicit unresolved slide/article
  discrepancy.
- sections/02-setting.tex, lines 387–392, correctly assigns qualitative
  convergence and local-measure gluing to Lasserre; it should not describe
  that gluing as the new quantitative theorem.
- sections/03-kernels.tex, lines 117–124 and 418–459, credits Jackson-kernel
  precedents, records the Korda/slide discrepancy, distinguishes dense lower
  and upper hierarchies, and calls out conditional generalized-moment
  transfer. Catala's Chebyshev application should remain identified as the
  cosine/even-map inference.
- sections/04-ordinary.tex, lines 621–640, correctly identifies Gribling's
  dense ordinary-module rate and Korda's broader sparse result. Its
  description of Korda Theorem 8 as a small negative power decreasing with
  width is safe; for local error exponent 1, the displayed equations yield
  exponent 18/(238+55w) after the box normalization recorded in the source
  audit.
- sections/05-sharpness.tex, lines 465–477, should continue to distinguish
  Nie's qualitative rational-separator obstruction, Grimm's strict-positivity
  representation, Han's moment-matching identity and Baldi–Slot's dense
  module lower bound from the manuscript's quantitative sparse example.
- sections/08-extensions.tex, lines 383–398, cites the 2026 publication.
  The same-work 2025 preprint was read, and its Theorem 4.7/Corollary 4.8
  support the global Hölder comparison. The final journal-version theorem
  locator was not checked; preserve the version note in the unified BibTeX
  entry or cite the inspected preprint explicitly if theorem-level wording
  is added.
- Baldi–Slot metadata is a critical correction: DOI 10.1137/23M1555430 is
  correct. DOI 10.1137/23M157257X resolves to an unrelated conjugate-gradient
  paper. The assigned manuscript key is retained; only its canonical
  metadata is fixed here.

## Old-key map and version handling

The accompanying kernels-map.json maps each of the 17 supplied keys to a
canonical bibliography key. All are identity mappings except Waki, whose
existing KB slug is waki2006-sums-of-squares-and-semidefinite, and the two
Tran–Toh citation keys, which both map to the single published-work entry
tran2026-truncated-moment-sequences. Tran–Toh is one work with a 2025
arXiv preprint and a 2026 journal version. The canonical BibTeX entry records
the DOI and arXiv version; this ledger keeps content locators and access
status version-specific. Do not invent separate work identities or reuse a
preprint locator as though it were checked in the inaccessible final text.

## KB package gaps and ingestion requests

Only these assigned items already have usable KB packages: Lasserre 2006,
Magron's 2026 set-products article, and Waki 2006. The following 14 source
packages are absent and may be ingested sequentially by the shared literature
owner. The URLs below are lawful publisher, author, arXiv, PMLR or retained
slide sources; “absent” means absent from the KB, not that this lane failed to
read every source.

1. Baldi and Slot (2024), DOI 10.1137/23M1555430; arXiv v3:
   https://arxiv.org/html/2302.12558v3
2. Catala, Hockmann, Kunis and Wageringel (2024), DOI
   10.1007/s00365-024-09686-0:
   https://link.springer.com/article/10.1007/s00365-024-09686-0
3. de Klerk, Hess and Laurent (2017), DOI 10.1137/16M1065264; free author
   PDF: https://ir.cwi.nl/pub/25758/M106526.pdf
4. Gamertsfelder and Mourrain (2025), arXiv:2501.09385v4:
   https://arxiv.org/html/2501.09385v4
5. Gribling, de Klerk and Vera (2026), arXiv:2605.31496v1:
   https://arxiv.org/html/2605.31496v1
6. Grimm, Netzer and Schweighofer (2007), DOI
   10.1007/s00013-007-2234-z; open author manuscript:
   https://www.math.uni-konstanz.de/~grimm/sparse.pdf
7. Han, Jiao and Weissman (2018), PMLR PDF:
   https://proceedings.mlr.press/v75/han18b/han18b.pdf
8. Korda, Magron and Ríos-Zertuche (2025), DOI
   10.1007/s10107-024-02071-6; free author/repository PDF:
   https://d-nb.info/1330825241/34
9. Laurent and Slot (2023), DOI 10.1007/s11590-022-01922-5; CWI full-text
   landing page: https://ir.cwi.nl/pub/32153
10. Magron, Lorentz Center slides (2025):
    https://homepages.laas.fr/vmagron/slides/lorentz25.pdf
11. Magron, TENORS slides (2026):
    https://homepages.laas.fr/vmagron/nlmoment.pdf
12. Nie, Qu, Tang and Zhang (2026), DOI 10.1007/s10107-025-02223-2:
    https://link.springer.com/article/10.1007/s10107-025-02223-2
13. Tran and Toh (2025 arXiv version), arXiv:2507.00572v1:
    https://arxiv.org/html/2507.00572v1
14. Tran and Toh (2026 published version), DOI 10.1007/s10107-026-02394-6:
    https://link.springer.com/article/10.1007/s10107-026-02394-6 . This is
    the same work as item 13; keep its version relation in the KB package
    metadata and note that the final article text was not accessible.

## Complete source-content retrieval gaps

One assigned source's full text remains inaccessible: the final 2026
Mathematical Programming version of Tran and Toh, DOI
10.1007/s10107-026-02394-6,
https://link.springer.com/article/10.1007/s10107-026-02394-6 . The publisher
page exposes subscription content only. The 2025 preprint
arXiv:2507.00572v1 was retrieved and read and supports the cited global
Hölder-rate comparison; no final-version theorem locator is claimed here.
All other assigned source contracts listed above were read from lawful
primary text or visually inspected retained slide PDFs. The 14 missing KB
packages are listed separately because KB absence is not the same as
unretrieved source content.

## Targeted checks performed

Read the assigned scope/brief and literature instructions; inspected the
manuscript citation sites and prior-source notes; checked metadata records
and source locators; compared local Lasserre, Waki and Magron texts to their
originals where a local full-text package was available; and checked that the
JSON old-key map contains all 17 input keys. No KB write, ingest, shared
index/check, TeX edit, experiment rerun, project-wide verification, or CI
inspection was performed.
