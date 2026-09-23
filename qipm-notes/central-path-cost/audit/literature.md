# Literature evidence for the standalone paper

Stage 1 screening date: 2026-09-07. Read `literature/README.md` before consulting packages. The manuscript bibliography is independent of the repository-generated bibliography. This ledger records evidence and limitations; it is not a systematic-review or priority certificate. No local package with missing full text has been marked read.

## Primary texts checked

### Nesterov–Todd (2002)

- Verified bibliographic metadata from local package `literature/papers/nesterov2002-on-the-riemannian-geometry-defined/paper.md`: *Foundations of Computational Mathematics* 2(4), 333–361, DOI [10.1007/s102080010032](https://doi.org/10.1007/s102080010032).
- Local primary extraction read at [[nesterov2002-on-the-riemannian-geometry-defined]] p.8-9, p.11-16, p.20-22; author PDF also opened online: https://people.orie.cornell.edu/miketodd/NTRiemann.pdf . These are manuscript PDF page numbers, not printed journal pages.
- §3 Lemmas 3.1–3.2 and Corollary 3.2: local norm/distance comparison and distance divided by `-log(1-R)` as a lower bound for the number of short steps. Generic Dikin counting is prior art.
- §4 Lemma 4.1: product distance adds in squares. Theorem 4.1: orthogonality plus logarithmic homogeneity gives central-product arc length `sqrt(nu)|log(omega1/omega0)|` and sqrt(2)-geodesicity. Theorem 5.2 specializes this to feasible primal–dual central paths. Attribute these results explicitly.
- §6.2 treats the cube with the scalar `-log cos` barrier on a rescaled interval and integrates its local norm to produce a Euclidean isometry. Thus scalar flattening and its product use are classical even though the manuscript uses another scalar barrier.
- §6.3 gives classical PSD logdet distance using relative eigenvalues. That cone metric is different from the bounded matrix-ball real Hessian metric used here.

### Nesterov–Nemirovski (2008)

- Primary published PDF opened: https://www2.isye.gatech.edu/~nemirovs/FCM_Riem_2008.pdf . Title, authors, journal 8(5), 533–560 and DOI [10.1007/s10208-007-9019-4](https://doi.org/10.1007/s10208-007-9019-4) verified on its first page.
- [[nesterov2008-primal-central-paths-and-riemannian]] p.3-4: distance to a target set and Example 1.1's primal orthant shortcut. Neither comparing with a target set nor demonstrating a shortcut is new here.
- [[nesterov2008-primal-central-paths-and-riemannian]] p.18, Theorem 4.1 / printed p.550: fixed-endpoint bound `L <= log 2 + nu^(1/4) sqrt(D(D+log 12))`. It applies to a nondegenerate nu-self-concordant barrier and the stated central path. The later same-accuracy theorem must not be confused with this one.
- [[nesterov2008-primal-central-paths-and-riemannian]] p.26, Theorem 5.3 / printed p.558: when the starting radius-1/10 Dikin ellipsoid misses the target sublevel, `L <= O(1) nu^(1/4) sqrt(D_set(D_set+log nu))`. The small-distance case is discussed separately. Online PDF extraction explicitly displays this equation and separation assumption.
- Novelty boundary: the possible new statement is the specified spectral distance/allocation formula and sharp logarithmic-rank centrality comparison, not a generic central-path/geodesic comparison.

### Lewis–Sendov (2001)

- Local package has no full text; did not use its unread note as evidence of the theorem.
- Open primary author PDF read: https://people.orie.cornell.edu/aslewis/publications/01-twice.pdf . First page confirms *SIAM Journal on Matrix Analysis and Applications* 23(2), 368–386 (2001), DOI [10.1137/S089547980036838X](https://doi.org/10.1137/S089547980036838X). Publisher metadata independently confirms this information.
- PDF p.14 / printed p.381, Theorem 3.3: equivalence of twice differentiability of a symmetric function and its real-symmetric spectral lift, with the Hessian formula. PDF p.18 / printed p.385 derives the second directional derivative specialization.
- Scope: the original theorem is stated on real symmetric matrices. Our complex-Hermitian trace-separable formula is derived directly by differentiating an analytic power series, not attributed as a verbatim complex theorem of this source. The nonnegative divided differences and repeated-eigenvalue convention are classical.

### Baes (2007)

- Title, author, journal and pages independently verified against the author's publication list https://sites.google.com/view/michelbaes/ and the local metadata package. DOI [10.1016/j.laa.2006.11.025](https://doi.org/10.1016/j.laa.2006.11.025); *Linear Algebra and its Applications* 422(2–3), 664–700.
- Open full text was not located in this stage; local package is unread with `access: none`. No theorem number or page claim is cited in the paper. Its citation identifies the subject's prior literature only. The needed Jordan logdet Hessian is derived in the manuscript using inversion and the Peirce decomposition. If a later stage invokes a stronger Baes theorem, retrieve and read the actual text first.

### Permenter (2023)

- Local full text read for the introduction and §2: [[permenter2023-a-geodesic-interior-point-method]] p.1-5. Author preprint landing page verified at https://arxiv.org/abs/2008.08047 . Local metadata: *SIAM Journal on Optimization* 33(2), 1006–1034, DOI [10.1137/20M1385019](https://doi.org/10.1137/20M1385019).
- Uses geodesic updates on symmetric cones and establishes a rank-dependent short-step guarantee. The paper's update geometry is a comparator; it does not supply the bounded spectral-interval target allocation computed here.
- Primary corpus version is the 2020 preprint. Citation uses verified published metadata while stage-one prose makes only claims supported by that primary text.

### Hirai–Nieuwboer–Walter (2026)

- Primary preprint https://arxiv.org/abs/2303.04771 opened; abstract states the generalization of self-concordance to Riemannian manifolds and Newton/path-following guarantees. The published title and DOI [10.1007/s10208-026-09756-8](https://doi.org/10.1007/s10208-026-09756-8) were checked against the coauthor institution's University of Copenhagen research portal. The publisher DOI redirect failed in the browser during this stage; do not invent volume or page numbers. Entry says published online.
- Stage-one comparison concerns only the verified subject matter and distinction of base metric, not an unexamined technical theorem.

## Targeted search and novelty limits

In addition to the repository's September-4 `2026-09-04-targeted-literature-screen-sparse-conic-qipm.md`, searched the open web for:

- `"central path" "sqrt" "log" "hypercube" geodesic`;
- `"spectral norm ball" "Riemannian" distance barrier`;
- `"central path" "water filling" barrier distance`;
- exact titles for Lewis–Sendov, Baes, and Hirai–Nieuwboer–Walter.

The first three did not locate a direct matching theorem. Results ranged from the known Nesterov–Todd source to unrelated manifold algorithms and communications water filling. This absence supports no unqualified first/novel claim. Stage 5 must extend the review to LP path/neighborhood lower bounds, scalar/canonical barriers, and primal–dual completion, then state novelty narrowly. Good candidate language: "To the best of our knowledge, the combination of the following explicit formulas and sharp comparisons has not appeared in the cited literature." Enumerate the actual theorem and its hypotheses; never use that phrase as a substitute for evidence.

## Stage-one mathematical/build verification

- `make -C central-path-cost` completed through latexmk, BibTeX and PDFLaTeX; the final output is eight pages.
- Final LaTeX log contains no undefined references/citations, overfull boxes, or package warnings.
- All LaTeX inputs and bibliography are contained inside the new folder. Audit/source-map links to historical sources are provenance, not build dependencies.
- Proof checks: Hermitian dilation factor `2g''=b''`; off-diagonal norm normalization in the Jordan Peirce formula; starting-norm direction of chord inequalities; scales >0 for metric formulas versus >=1 for self-concordance; active coordinates and positive multiplier in both allocation problems; extraneous gamma=0 root excluded in the multiplied Lambert equation.
- Five independent reviewers have not yet reviewed this author stage; the root coordinates that required next step.

## Stage 2 literature and verification

- Read Lorentz's local primary extraction [[lorentz1951-on-the-theory-of-spaces]] p.2-4. The definition and triangle-property theorem concern decreasing-rearrangement norms. The manuscript credits the weighted-prefix inequality as a finite weighted version of this classical norm idea; it does not attribute the central-path sharpness theorem to Lorentz. Published metadata confirmed on primary printed p.411: *Pacific Journal of Mathematics* 1(3), 411–429 (1951), DOI 10.2140/pjm.1951.1.411. Direct browser access to publisher DOI/page returned a safe-open/internal error during this stage; the local retrieved primary PDF/extraction provided the evidence instead.
- Existing Nesterov–Todd and Nesterov–Nemirovski comparisons and source limits remain as recorded above. Stage 2 makes no broad first-result claim, and treats the special prefix sharpness, scalar KKT dilation, and explicit sequence model as the actual theorem statements. Root's expanded priority screen is separately recorded in `audit/root-additional-literature.md` for final synthesis.
- The two new scripts ran under `/home/sgusev/miniconda3/envs/qipm/bin/python` without installing packages. Exact Fraction certificates passed; the independent floating-point geometry checks also passed and are explicitly distinguished from proof certificates.
- Author final LaTeX build completed with 20 pages and no undefined references/citations, overfull boxes, or warnings (subsequent reviewer edits require their own final rebuild).

## Stage 3 primary literature checks (2026-09-07)

- Read the local primary Chewi preprint [[chewi2023-the-entropic-barrier-is-n]] p.1-4 and its tensorization discussion p.10-11. Theorem2 gives the n parameter on general convex bodies; dimensionone supplies the precise standard self-concordance used for the entropic interval. The manuscript derives the scalar gradient norm and exact cube parameter directly. The published chapter metadata were verified on https://link.springer.com/chapter/10.1007/978-3-031-26300-2_6 : Geometric Aspects of Functional Analysis, LNM2327,209–222 (2023), DOI10.1007/978-3-031-26300-2_6. The local primary artifact is the2021 preprint; published metadata do not change the theorem use.
- Lee–Yue primary author PDF https://manchungyue.com/nSC.pdf inspected pp.1-6. Definition3 defines polar-volume universal barrier; Theorem2 proves n-self-concordance; Remark2 identifies simple-vertex lower bound and NN1994 Proposition2.3.6. Published metadata verified through authorinstitution repository https://ira.lib.polyu.edu.hk/handle/10397/95502?mode=full : MathOR46(3)1129–1148 (2021), DOI10.1287/moor.2020.1113. The cube factorization here is directly calculated and explicitly not claimed novel.
- Read the one-page local original Bubeck–Eldan abstract [[bubeck2015-the-entropic-barrier-a-simple]] p.1; it supports historical introduction of the entropic barrier, not proof details. The full preprint landing page https://arxiv.org/abs/1412.1587 and final publisher https://pubsonline.informs.org/doi/10.1287/moor.2017.0923 verified the final title, MathOR44(1)264–276 (2019 issue; online2018), DOI10.1287/moor.2017.0923. The final title is *The Entropic Barrier: Exponential Families, Log-Concave Geometry, and Self-Concordance*. The exact-n step in this manuscript cites Chewi, not the asymptotic Bubeck–Eldan theorem.
- The explicit cube entropic log-partition, its separability, and Langevin gradient appear in Lévy–Valeau–Akhavan–Rebeschini, *Self-Concordant Perturbations for Linear Bandits*, arXiv2510.24187v3 (26June2026), section6.1/Proposition6. Open primary HTML inspected at https://arxiv.org/html/2510.24187v3 , including displayed product-integral calculation. Added a direct citation beside our cube factorization to remove any suggestion that this formula itself is new. Their problem is bandit regret; our consequence concerns fixed-objective centrality ratios and bounded-movement sequences.
- Papa Quiroz–Oliveira local package has no fulltext and remains unread. Open primary preprint retrieved in browser at https://carmamaths.org/resources/jon/Preprints/Books/CUP/CUPold/MaterialII/hypercube.pdf (dated6April2005), pp.1-2: explicitly introduces sum(2x_i-1)(logx_i-log(1-x_i)), parameter3r/2, and Hessian-geometric algorithms. Author-deposited OptimizationOnline record https://optimization-online.org/2004/08/932/ and authorinstitution metadata https://research.upn.edu.pe/en/publications/new-self-concordant-barrier-for-the-hypercube/ corroborate the published2007 JOTA135(3)475–490, DOI10.1007/s10957-007-9220-2. Manuscript makes only this supported historical comparison, not a claimed application of the normalized theorem to their different parameter3/2 scalar barrier.
- Read primary Castro–Cuesta [[castro2011-quadratic-regularizations-in-an-interior]] p.18-21, section4.1, Lemmas2–4. Its diagonal quadratic regularizations on a box preserve parametern when each coefficient is at most1/u_i². The paper explicitly contrasts this with non-diagonal augmented functions on cones. Our manuscript credits diagonal parameter-preserving regularization and claims only its own proved dense/radial constructions plus centrality comparisons. Metadata from its primary/local record: MathProgram130(2)415–445 (2011), DOI10.1007/s10107-010-0341-2. The citation is section4.1 (section4.2 is computational).
- General trace-separable spectral Hessian formula is derived in the text by polynomial Jordan calculus and uniform second-derivative approximation. Lewis–Sendov/Baes are background credit; no uninspected Baes theoremnumber is invoked. No statement transfers arbitrary scalar self-concordance to a matrix/Jordan lift without separate verification.
- Root supplied additional curvature/strong-linear-programming sources in `root-additional-literature.md` for stage5 synthesis. They remain outside this stage's narrow novelty statements.

### Stage 3 verification boundary

The C_sc envelope has a complete analytic bound and uniqueness proof; its printed decimal is expressly numerical. The c_star appendix has a separate exact Fraction certificate for every displayed rational localization claim. The radial theorem has a complete analytic proof plus independent numeric checks from nested center solves. The author build is34pages and clean. Required five-reviewer assessment is still pending at author handoff.

## Stage 4 writing screen and attribution

Author consulted all relevant workbench sources listed in `source-map.md`, root primary-source preparation, and the local literature README. These unpublished notes are derivation sources, not evidence of novelty or replacements for public citations.

- Nesterov–Todd2002: precise prior gap-set scope is retained, including Theorem5.1(c)/Corollary5.1. The manuscript's self-contained central supporting-hyperplane proof reproduces that classical consequence. No new metric projection, constant-speed, or whole-gap-set claim is made.
- Ohara–Ishi–Tsuchiya2024 primary publisher opened during writing: https://link.springer.com/article/10.1007/s41884-023-00116-x. Publisher says volume7,555–586(2024), first online27July2023; an institutional record says2023, so bibliography follows publisher issue year2024. Sections4–5 support the prior metric projection/conjugacy discussion.
- Hauser–Güler2002 primary publisher opened: https://link.springer.com/article/10.1007/s102080010022; Oxford author publication record https://www.maths.ox.ac.uk/node/19735 confirms FoCM2,121–143,2002. Root directly verified arxivmath/0103196 Theorem5.5 for the complete self-scaled classification with every coefficient>=1. The manuscript uses precisely its weighted consequence.
- Hildebrand2013 author publication list https://membres-ljk.imag.fr/Roland.Hildebrand/publications.htm verifies final title *A lower bound on the barrier parameter of barriers for convex cones*, MathProg142,311–329,2013. Root directly inspected https://optimization-online.org/wp-content/uploads/2011/06/3068.pdf Corollary6.2. This preprint's title differs; final journal title used. The k=1 two-dimensional orthant case is separated from Corollary6.2's dimension>=3 range.
- Product-ball barrier is an elementary restriction of NN1994 Proposition5.4.6(i), printedp199, exactly as root checked from the local original via `/tmp/central-path-nn1994.txt`. No claim of new barrier construction is made.
- Faraut–Korányi1994 local Peirce chapter package has no full text; no invented page citation is used. Oxford primary book record https://academic.oup.com/book/54470 verifies authors/title/year and DOI10.1093/oso/9780198534778.001.0001. The book is cited for standard quadratic-representation background; the metric contraction and optimization consequences needed here are derived explicitly. The chapter DOI request failed; no inaccessible specific chapter theorem is quoted.
- Gouveia–Parrilo–Thomas2013 metadata and proper-lift framework were checked by root at primary publisher DOI10.1287/moor.1120.0575. The manuscript cites this as background only; it uses an elementary compactness argument for operational dimension instead of requiring a factorization theorem or smooth certificate selection.
- Root's additional screen found published Allamigeon–Dadush–Loho–Natura–Végh2025 SICOMP54(5),FOCS22-178–FOCS22-264, DOI10.1137/23M1554588. Final synthesis should cite the journal version, replacing preprint-only metadata. Its straight-line wide-neighborhood complexity differs from bounded local Hessian movement.

The stage4 additions make no broad priority claim. The exact same-sparse-instance three-scale comparison, explicit weighted activity allocation, and fixed-metric formulation consequences are candidates for qualified contribution statements after the full-manuscript literature synthesis. The standard Busemann/principal-minor metric identity, AM–GM, barrier restriction, and NT gap-set theorem are prior ingredients.

## Stage 5 synthesis and primary-source checks (2026-09-07)

The final introduction consolidates the previously verified geometric
literature and distinguishes precise original comparisons from prior
ingredients. The qualified novelty paragraph is limited to the exact
active-rank supremum plus allocation, the explicit dyadic arbitrary-label
sequence separation, the specified radial-family comparison, and the
same-instance three-scale completion comparison. No exhaustive priority
claim, generic first central-path inefficiency claim, or new classical
gap-set theorem is made.

Additional sources opened during synthesis:

- Allamigeon–Dadush–Loho–Natura–Végh, primary full HTML
  https://arxiv.org/html/2206.08810v4 and primary publisher
  https://epubs.siam.org/doi/abs/10.1137/23M1554588. The introduction's
  comparison is limited to affine-segment straight-line complexity in a
  wide neighborhood, explicitly distinct from fixed-radius local-Hessian
  moves. Bibliography uses the published SICOMP54(5),FOCS22-178--FOCS22-264,
  2025, DOI10.1137/23M1554588. It does not equate that source's wide
  neighborhood with every Newton-decrement neighborhood.
- Allamigeon–Gaubert–Vandame, https://arxiv.org/abs/2201.02186 and the
  official STOC program https://acm-stoc.org/stoc2022/toc.html. The latter
  directly confirms the author is Nicolas Vandame (corrected during
  authorship). Proceedings metadata: STOC2022,515–528,
  DOI10.1145/3519935.3519997. The brief historical statement refers to its
  specified self-concordant-barrier neighborhood framework.
- Deza–Nematollahi–Terlaky, primary author PDF
  https://www.cas.mcmaster.ca/~deza/mp2008.pdf and author-deposited record
  https://optimization-online.org/2004/12/1034/ verify authors including
  Eissa Nematollahi, published MathProg113,1–14,2008,
  DOI10.1007/s10107-006-0044-x. Used only for Klee–Minty path-following
  lower-bound context.
- Allamigeon–Benchimol–Gaubert–Joswig, primary published author PDF
  https://www.cmap.polytechnique.fr/~gaubert/PAPERS/LogBarrier.pdf,
  SIAM J Applied Algebra and Geometry2(1),140–178,2018,
  DOI10.1137/17M1142132. Root inspected opening theorems and synthesis
  author opened the same primary PDF. The manuscript gives proportionate
  credit for long-winding logarithmic paths and exponential neighborhood
  iteration lower bounds; it does not confuse their numerical scale or
  input encoding with the present dyadic cube family.

All other primary-source scope qualifications from earlier stages remain
in effect. The newly added bibliography entries were checked against
primary records; no inaccessible source is used for a theorem claim.

## Final-review current-literature update (2026-09-08)

Dadush, Daniel; Ma, Haoyuan; Natura, Bento; and Végh, László A.,
“Trust Region Interior Point Methods: Optimal ℓ₂- and Faster
Wide-Neighborhood Path Following,” Proceedings of the 58th Annual ACM
Symposium on Theory of Computing (STOC 2026), pp. 755–766,
DOI 10.1145/3798129.3800790, published June 9, 2026.

- Primary full manuscript: https://homepages.cwi.nl/~dadush/papers/trust-region.pdf.
  Root and final reviewer5 independently read the abstract/introduction;
  the final repair agent reopened and inspected the primary PDF abstract.
- Primary publication record: https://dl.acm.org/doi/10.1145/3798129.3800790.
  Root and reviewer5 verified the ACM metadata. The repair agent's separate
  web opening of this record failed; the bibliographic metadata uses those
  already completed primary checks, not a claim of successful fresh access.
- Supported scope: improved wide-neighborhood running-time and iteration
  guarantees parameterized by straight-line complexity, and approximately
  instance-optimal trust-region following in the narrow ℓ₂ neighborhood.
  The abstract defines straight-line complexity through affine segments
  traversing a central neighborhood and states constant-factor iteration
  optimality in the narrow neighborhood.
- Manuscript use: a brief comparison adjacent to the ADLNV2025 discussion.
  It explicitly distinguishes affine-segment/algorithmic iteration resources
  from fixed-radius Hessian moves. No theorem from the new source is used
  in a proof, and no broader novelty or priority claim is introduced.
