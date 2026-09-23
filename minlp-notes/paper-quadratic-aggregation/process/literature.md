# Literature evidence and access record

Checked 2026-09-22. This record is not part of the submission. The manuscript
must distinguish journal metadata from the particular full-text versions
actually inspected. No managed literature file was changed. Downloads are
working copies outside the submission directory; exact retrieval URLs and
hashes below permit independent retrieval without redistributing papers.

## Direct predecessor and numbering

Blekherman, Dey, Sun, *Aggregations of Quadratic Inequalities and Hidden
Hyperplane Convexity*, SIAM Journal on Optimization 34(1):98–126 (2024),
DOI [10.1137/22M1528215](https://epubs.siam.org/doi/10.1137/22M1528215).
Publisher metadata checked: online January 5, 2024. Publisher full text was
not obtained. Local author copy is dated October 5, 2022:
`literature/papers/blekherman2024-aggregations-of-quadratic-inequalities-and/`.
The original PDF and extracted text were inspected at the conjecture and
background results. The extraction sometimes loses negation signs, so its
equations must not be copied without checking the PDF.

The current arXiv version is [2210.01722v2](https://arxiv.org/abs/2210.01722v2),
May 29, 2023 (history checked September 22, 2026). Downloaded full text:
`/tmp/quadratic-paper-literature/bdsv2.pdf`, with layout extraction `.txt`.
Theorem numbers in the notes generally refer to the older local copy.

| Content | Local 2022 copy | arXiv v2 used in manuscript | v2 PDF page |
|---|---|---|---|
| HHC definition | Definition 2.1 | Definition 2.1 | 4 |
| Two/three-form sufficient conditions | Corollary 2.6 | Corollary 2.7 | 6 |
| Proper open hull from good aggregations | Theorem 2.8 | Theorem 2.9 | 6 |
| Diagonal special case | Theorem 2.11 | Theorem 2.12 | 7–8 |
| Empty-set certificate | Proposition 2.12 | Proposition 2.13 | 8 |
| No PSD multiplier implies whole-space hull | Proposition 2.13 | Proposition 2.14 | 8 |
| Closed system interior hull | Theorem 2.23 | Theorem 2.24 | 12–13 |
| Nonzero Q aggregation qualification | Remark 2.24 | Remark 2.25 | 13 |
| Certificate conjecture | Conjecture 3.3 | Conjecture 3.3 | 14 |

The v2 conjecture asks for a PSD quadratic part with aggregate not a negative
constant; under strict feasibility this is equivalent to (Aλ,bλ)≠(0,0).
The proof in this paper must resolve exactly the case where nonzero PSD
multipliers exist but every associated aggregate is a negative constant.
The no-PSD-multiplier case and the diagonal case were already settled there.
Conjectures 3.1–3.2 concern finite good-aggregation descriptions. The concurrent
frontier note now makes Conjecture 3.1 a candidate for stage 4; it is not yet
an accepted manuscript claim. No resolution of Conjecture 3.2 is proposed.
Numbered citations explicitly identify v2, not the journal.

## Adjacent aggregation work

- Dey, Muñoz, Serrano, SIAM J. Optim. 32(2):659–686 (2022),
  [10.1137/21M1428583](https://doi.org/10.1137/21M1428583).
  Local original and extracted text:
  `literature/papers/dey2022-on-obtaining-the-convex-hull/`.
  Inspected local full text pp.3–5 (printed pp.661–663: PDLC, symmetric
  S-lemma, Theorem 2.4 and the comparison with Yildiran). This local copy
  carries journal pagination. The collection's existing reading record
  additionally points to pp.9–11 (limitations and closed extension) and
  pp.21–24 (finiteness example); those latter page ranges were not freshly
  checked in this stage.
  Its result is a hull description for three quadratics with additional
  hypotheses; it is not evidence of a new two-quadratic certificate theorem.
- Yildiran, *Convex hull of two quadratic constraints is an LMI set*,
  IMA J. Math. Control Inform. 26(4):417–450 (2009),
  [10.1093/imamci/dnp023](https://academic.oup.com/imamci/article-pdf/26/4/417/1876141/dnp023.pdf).
  Publisher abstract and bibliographic metadata inspected; accessible page
  states full content requires access. Full text was not obtained in this
  stage. The modest manuscript claim (at most two aggregate inequalities)
  is stated directly by the author's abstract and is also discussed in BDS
  and DMS full text. Do not invent theorem numbers for Yildiran.
- Blekherman, Dunbar, *A Topological Approach to Simple Descriptions of
  Convex Hulls of Sets Defined by Three Quadrics*, SIAM J. Applied Algebra
  and Geometry 9(2):310–342 (2025),
  [10.1137/24M1668445](https://epubs.siam.org/doi/10.1137/24M1668445).
  Publisher abstract and metadata checked, publication May 6, 2025.
  The repository's “2024 preprint” description is stale bibliographically.
  Accessible full text [arXiv:2405.18282v1](https://arxiv.org/abs/2405.18282v1),
  May 28, 2024, is `/tmp/quadratic-paper-literature/bd.pdf` and `.txt`.
  Inspected introduction and Theorems 1.1–1.4 (pp.1–3), and sections on
  hyperplane restrictions and finite aggregations (pp.9–16). Theorem 1.4
  addresses four aggregations with regularity assumptions, and explicitly
  relates to BDS Conjecture 3.2. The inspected preprint does not state or
  resolve the whole-space certificate conjecture. Publisher full text was
  not obtained during initial stage 1 authoring. A concurrent note supplies
  an accessible eprint lead, recorded below for stage 4 inspection; do not
  claim every published-version detail was checked by this paper process.

## Classical tools and SDP context

- Dines, *On the mapping of quadratic forms*, Bull. Amer. Math. Soc. 47
  (1941):494–498, DOI 10.1090/S0002-9904-1941-07494-X. AMS PDF request
  returned HTTP 403. The exact convex-image theorem is reproduced and used
  in BDS v2 Corollary 2.7's proof, and is classical, not a novelty claim.
  Omit issue number: the local BDS bibliography has an inconsistent one.
- Polyak, JOTA 99(3):553–583 (1998), DOI 10.1023/A:1021798932766.
  Author-uploaded full text is available at
  [ResearchGate](https://www.researchgate.net/publication/226667003_Convexity_of_Quadratic_Transformations_and_Its_Use_in_Control_and_Optimization).
  The exact three-real-form theorem and n≥3 boundary should be inspected
  by stage 3 before its use; BDS v2's proof of Corollary 2.7 also states
  the relevant classical result. No new convexity theorem is claimed here.
- Sheriff, Harvard dissertation (2013),
  [institutional record](https://dash.harvard.edu/entities/publication/73120378-b892-6bd4-e053-0100007fdf3b).
  Record and abstract inspected. A preexisting extraction is
  `/tmp/sherthesis.txt`; it loses many digits and is inadequate for exact
  theorem numbering. A fresh institutional PDF request returned HTTP 405.
  Stage 3 can use a precise self-contained definition of stable convexity
  and cite the thesis for terminology without importing unchecked
  roundness theorem details. Higher-dimensional roundness is context only.
- Fujie–Kojima, J. Global Optim. 10:367–380 (1997), DOI
  10.1023/A:1008282830093. Preexisting `/tmp/fk.pdf`, `/tmp/fk.txt` were
  inspected, particularly printed pp.372–373, Theorem 2.1 and its explicit
  Condition 1.2. That theorem gives inclusion and equality with the closure
  under its condition. Origin of the preexisting download is not recorded;
  retain as a reading aid, not a fresh retrieval claim.
- Kojima–Tunçel, SIAM J. Optim. 10(3):750–778 (2000), DOI
  10.1137/S1052623498336450. Fresh author-hosted published PDF retrieved:
  [nonconvex.pdf](https://www.math.uwaterloo.ca/~ltuncel/publications/nonconvex.pdf),
  `/tmp/quadratic-paper-literature/kt.pdf` and `.txt`. Printed pp.758–759,
  Theorem 4.2, claim exact equality without a constraint qualification.
  The coordinator independently inspected the PDF and found that its proof
  uses a dual-of-intersection identity without a closure. This is in tension
  with explicit nonclosed-projection examples developed in this project.
  Do not use Theorem 4.2 to justify equality or a universal closedness claim.
  Stage 3 should prove the precise needed closure relation independently
  under strict feasibility, and qualify historical attribution. No erratum
  search or published criticism has yet been verified.

## Broader search and limits of priority claims

Queries actually used included `"Blekherman" "Conjecture 3.3" quadratic`,
`"Aggregations of quadratic inequalities" "convex hull" 2025 2026`,
`"hidden hyperplane convexity"`, `"hidden hyperplane convexity" "certificate"`,
and author/title searches for the papers above. The first and combined
queries returned substantial irrelevant material; the exact HHC phrase
was more useful. Search results alone are not evidence of priority.

Additional primary records inspected:

- [Song–Xia arXiv:2108.08517v1](https://arxiv.org/abs/2108.08517v1),
  August 19, 2021: extensions of Polyak, Yuan and S-lemma for forms generated
  by three forms with PDLC. Stage 1 inspected abstract only, not its proofs.
- [Nguyen–Chu–Sheu arXiv:2503.01225v1](https://arxiv.org/abs/2503.01225v1):
  despite the 2025 upload, the record identifies the journal publication as
  JIMO 18(1):575–592 (2022), DOI 10.3934/jimo.2020169. It concerns convexity
  of the range of two inhomogeneous quadratics, not arbitrary-m proper-hull
  certificates. Abstract and metadata only inspected in this stage.
- [Huy et al., arXiv:2601.13511v1](https://arxiv.org/html/2601.13511v1),
  January 20, 2026: introduction and mathematical setting inspected in
  full HTML. It concerns convexity of image-plus-orthant, S-lemma and
  quadratic programming; in its main setting constraint quadratic parts
  are PSD. This is not a resolution of the arbitrary-m HHC certificate
  question. No assertion of exhaustive review of all its proofs is made.
- [Dymarsky arXiv:1410.2254](https://arxiv.org/abs/1410.2254): primary
  record and preexisting full text `/tmp/dym.txt`/`/tmp/sheriff.txt`
  identified. The latter is misleadingly named and is Dymarsky, not Sheriff.
  Its shifting-hyperplane technique concerns convexity of image subsets,
  rather than the certificate limit argument here. Detailed comparison can
  be made in synthesis if this source is used.

No subsequent resolution of BDS Conjecture 3.3 was found in this targeted
search. This is a bounded search conclusion, not proof of publication
priority. A justified eventual novelty statement is that the manuscript
proves the stated conjecture, with its weaker stated hypothesis; add
“To the best of our knowledge” to any priority assertion and give the
explicit scope. Do not call the two-quadratic case, classical SDP/aggregation
relationship, or compactness separation lemma original.

## Frontier literature leads and required stage 4 comparisons

The correction agent read the entire concurrent
`notes/research-20260922-aggregation-frontier.md`. The following records
distinguish inspection of a repository note from independent inspection
of an external primary source. No new external full-text inspection or online
search was performed in this correction step. Earlier stage 1 inspections
remain documented above; the note author's additional inspections below are
reported evidence and leads, not transferred primary-source verification.

| Source or lead | Evidence already inspected by this paper process | Remaining obligation before stage 4 claims |
|---|---|---|
| BDS Conjecture 3.1, finite-aggregation theorem, and HHC constructions | BDS v2 full text obtained; stage 1 reviewed the setting and certificate-related locators above. The frontier note reports inspection of the local 2022 source, including its Theorem 2.17 and Section 9. | Independently inspect the exact Conjecture 3.1 statement, finite-aggregation hypotheses, and listed HHC constructions in v2; do not copy old theorem numbering or assume novelty from differing notation. |
| Blekherman–Dunbar published eprint, [author link](https://epubs.siam.org/eprint/VRNXYR5GPAAPTF5RJHV3/full), DOI 10.1137/24M1668445 | Stage 1 inspected arXiv v1 as above. The frontier note reports reading published Theorems 1.4 and 3.9; the correction agent inspected that report only. | Obtain and inspect the published statements and assumptions: PDLC, no points at infinity, projective variety, smoothness/hyperbolicity, and open versus closed systems. Verify applicability against the candidate's common zeros and singular determinant before making exclusion claims. |
| Wang–Kılınç-Karzan, *On semidefinite descriptions for convex hulls of quadratic programs*, [arXiv:2403.04752v1, Appendix B.2](https://arxiv.org/html/2403.04752v1#A2.SS2) | Source note reports SDP hull exactness for a repeated-column quadratic matrix program with enough columns and a positive-definite convex quadratic combination. This external theorem has not yet been independently inspected for the paper. | Read the exact theorem, hypotheses, version/publication metadata, and proof context. Check `r>=3` and `A1+A2=I` against its conventions. If applicable, credit closed SDP exactness as prior work and separate it from HHC and necessity of infinitely many direct good aggregations. |
| Earlier Wang–Kılınç-Karzan work and Beck's quadratic matrix-programming results | General leads in the frontier note only; exact earlier articles and theorem locators not yet established by this paper process. | Identify and inspect relevant primary sources through the preceding paper's citations. Compare eigenvalue multiplicity, joint numerical ranges, convex hulls, and replicated-matrix constructions before any general-HHC novelty claim. |
| Dey–Han–Wang, *Aggregation of bilinear bipartite equality constraints and its application to structural model updating problem*, J. Global Optim. 94:1099–1135 (2026), [10.1007/s10898-026-01607-8](https://link.springer.com/article/10.1007/s10898-026-01607-8) | Frontier note reports Theorem 2 and its different closure; local full text is `literature/papers/dey2026-aggregation-of-bilinear-bipartite-equality/fulltext.md`. Correction agent read the report, not that primary text. | Inspect Theorem 2 and introductory comparison: signed aggregation of two bilinear equalities on a box, then convexification of each equality. Distinguish that closure from direct strict good quadratic sublevel sets. Never claim infinite aggregation necessity in nonlinear optimization is generally new. |
| Dunbar's 2025 thesis, [Emory PDF lead](https://etd.library.emory.edu/downloads/2j62s637x?locale=en) | Frontier note reports a search excerpt for Theorem 5.0.5 and a failed HTTP 403 download. No thesis theorem has been inspected in full context here. | Attempt primary-text access and check whether the four-aggregation bound removes the no-points-at-infinity assumption while retaining PDLC and other regularity. If inaccessible, record the limit and make no theorem attribution based only on the excerpt. |
| [Dunbar author homepage](https://alex-dunbar.github.io/) and subsequent aggregation literature | Frontier note reports a current publication listing and 2026 talk; initial paper searches above focused on Conjecture 3.3. | Perform a separate bounded search for Conjecture 3.1, HHC under repeated matrix blocks, uncountable strict descriptions, and later developments. A homepage without a newer manuscript is discovery evidence only. |

The candidate hull formula also has a proposed direct midpoint proof for
`r>=3`. A short self-contained proof does not by itself establish novelty;
its positive convexification content may already follow from matrix-programming
theory. The proposed new role to assess is an HHC example for Conjecture 3.1,
including the unique-active-ray obstruction to finite (and possibly countable)
strict good-aggregation descriptions. There is no claim that finite extended
SDP or SOCP formulations are impossible. The strict/open and non-strict/closed
versions require separate statements and comparisons.

## Supplementary access leads from the first five reviews

Reviewers 1 and 4 report readable author-uploaded Yildiran full text at
[ResearchGate](https://www.researchgate.net/publication/220386378_Convex_hull_of_two_quadratic_constraints_is_an_LMI_set),
corroborating the strict-inequality and at-most-two-aggregation account.
This augments the initial author's abstract-only access record without
rewriting that historical record. If a later section needs a theorem-level
qualification or locator, inspect the primary text directly at that stage.
Reviewer 5 identified a [Harvard thesis PDF endpoint](https://dash.harvard.edu/bitstreams/620ecf61-bf48-4b50-bbad-918a328d0930/download)
for Sheriff but did not inspect its theorem statements; this remains a
stage 3 access lead, not an imported stable-convexity theorem.

## Application appendix: prior-work obligations

The coordinator has included the proved conflict-repair construction in a
concise stage 3 application appendix; see `coverage.md`. The local exploratory
note cites Berthold–Witzig, *Conflict Analysis for MINLP* (2021), DOI
[10.1287/ijoc.2020.1050](https://doi.org/10.1287/ijoc.2020.1050), local package
`berthold2021-conflict-analysis-for-minlp`, and Hongbo Dong, *Relaxing nonconvex
quadratic functions by multiple adaptive diagonal perturbations*,
[author manuscript](https://optimization-online.org/wp-content/uploads/2014/03/4274.pdf).
The correction agent inspected the local note's comparison and the separate
correctness review, not these primary papers. Stage 3 must inspect the primary
statements actually used to situate the elementary construction. Do not claim
aggregation, reconstructed aggregates, diagonal-dominance convexification,
tangents, or the selection LP is new, and do not infer algorithmic performance
from its corrected exact example. The unrelated inexact OA/Benders exploration
and unimplemented benchmark proposals are excluded.

## Stage 3 primary-source followups (2026-09-22)

- Polyak: read the author-uploaded primary full-text extraction at the
  ResearchGate URL above, including the introductory three-real-form
  statement and Theorem 2.1. The web extraction loses displayed formulas
  and renders the n≥3 sign imperfectly. The exact n≥3, three-form,
  signed-positive-definite-combination implication is independently stated
  and applied in the retrieved BDS v2 Corollary 2.7 proof. A direct
  ResearchGate PDF click failed; no fresh visual PDF inspection is claimed.
  Only this classical implication is used, not Polyak's other assertions.
- Sheriff: read the stable-convexity definition and perturbation discussion
  in the preexisting institutional-thesis text `/tmp/sherraw.txt` (around
  lines 1368--1394), and cross-checked the title and institutional metadata
  online. Its open-neighborhood definition is exactly the one in the paper.
  Fresh institutional PDF attempts returned HTTP 405. No uncertain thesis
  theorem number or roundness classification is imported. The definite
  three-form case follows from Polyak and openness of positive definiteness.
- Fujie--Kojima: reread `/tmp/fk.txt`, printed pp.369--373, including
  Condition 1.2, its stronger strict-original-feasibility sufficient
  Condition 1.4, and Theorem 2.1. Their convex-aggregate intersection
  equals the closure of the SDP projection under that condition. Our
  self-contained proof verifies the relevant qualification directly.
- Kojima--Tunçel: see `stage03-root-closure-audit.md`. The original
  compactness convention is respected by the additional four-row example
  now proved in the paper; the two-row example alone would not suffice
  for that comparison. The coordinator's targeted erratum search found
  none, which does not prove none exists. The paper does not rely on
  Theorem 4.2's unqualified equality or universal projection closedness.
- Berthold--Witzig: read the local primary report extraction, especially
  physical pp.8--14: local linearizations, nonlinear proof/aggregation
  (19), and tangent discussion. The local version is ZIB Report 20-20
  (2020). Journal metadata freshly checked at
  [the publisher](https://pubsonline.informs.org/doi/10.1287/ijoc.2020.1050):
  INFORMS Journal on Computing 33(2):421--435 (2021). The appendix
  claims only that local affine proofs and convex nonlinear relaxation
  aggregations are prior work, not an unproved absence of a technique.
- Dong: read [the May 12, 2016 author manuscript](https://optimization-online.org/wp-content/uploads/2014/03/4274.pdf),
  physical pp.1--3, especially p.2. It allows aggregating original rows
  and lifted inequalities reconstructed as quadratic rows before
  convexification; effective aggregate selection is outside its scope.
  We do not infer novelty of the selection LP from that observation.
  Journal metadata checked at
  [the publisher](https://epubs.siam.org/doi/10.1137/140960657):
  SIAM J. Optim. 26(3):1962--1985, published September 27, 2016.

No priority claim is made for the elementary stage 3 consequences,
examples, or application. The certificate theorem is positioned against
the named conjecture rather than a claim of exhaustive literature search.

## SHA-256 source identifiers

| Source | SHA-256 |
|---|---|
| Local BDS original.pdf | `2aefd96d489ab9bf07dbb0dd2b70f799ff5538c25e8f6364ddf5b26fdede0ddd` |
| Local DMS original.pdf | `93179a8024d31f8219cfc1fc639803ffbf4c5fd048a0c76a535098331d9877b9` |
| BDS arXiv v2 PDF | `021c7553da8734f0a4f955b3b86db0cec51dd4976c8ee3d648d63e3f15331822` |
| BD arXiv v1 PDF | `951ef6553192aa1d138c70389b9c459237af18536d59c9f6f05057779be12c44` |
| Kojima–Tunçel PDF | `2e448c5689c386fb8891d92095b247c2f3c1cf913898829facf0e7865b4f043a` |
| Preexisting Fujie–Kojima PDF | `20061abc476413e600c2d5b98dec9c374803b2ba3cecd6a83b826396edf6c23f` |


## Stage 4 completed primary-source audit

The Gram-map and infinite-aggregation author completed the additional source
audit in [stage04-literature.md](stage04-literature.md). It verifies the
classical fidelity formula, the real rotation extremum, Beck's global QM
image theorems, the DMS comparison, the published DHW theorem, WKK's
versioned QMP hull criterion, and the related ball hypograph. The HHC
conjecture-resolution priority sentence is qualified. The old frontier
thresholds are superseded by the proved sharp Gram-map threshold in the
stage 4 draft. The five independent manuscript reviews are still required.
## Stage 5 approximation and duality additions

The complete audit is `stage05-literature.md`. The author read the local
primary Bronshteyn–Ivanov (1975) theorem/proof/remark, Arya–da Fonseca–Mount
arXiv:2306.15648v2 Introduction and Theorems 1–2, Rote's author-hosted
primary report corresponding to Computing 48 (1992), 337–361, and
Boyd–Vandenberghe Section 5.9 on generalized inequality duality. The
manuscript credits the classical exponent and conic duality explicitly.
Rote is the closest one-dimensional tangent/chord approximation comparison;
the present rate concerns prescribed quadratic sublevel sets and covers
arbitrary interior good multipliers. No broad first approximation theorem
or runtime claim is made. No managed literature package was modified.

## Stage 6 strict PDLC transfer

The complete independent audit is [stage06-literature.md](stage06-literature.md).
It checks BD's fully qualified four-bound and explicit low-dimensional
proofs, BDS v2's six-bound and four-necessary example, and the classical
two-bound. It corrects the half-ball locator to v2 Example 2.23. The
dissertation's stronger regular-nonstrict statement is acknowledged, with
retrieval and proof-dependency limits recorded separately from manuscript
claims. Originality is qualified and limited to the full arbitrary-strict
transfer; the four-bound, sharpness example, and fixed-set eigenvector
limit have credited antecedents.

## Stage 6b many constraints in a three-dimensional span

The source audit is [stage06b-literature.md](stage06b-literature.md).
It verifies BDS v2 Proposition 2.22 and Propositions 9.1 and 9.6, and the
specific three-generator scope of BD v1 Propositions 8.6 and 8.10. The
appendix gives a directional refinement of the existing facet argument,
an essential-ellipsoid family, and a new explicit obstruction to the
proposed general-cone two-bound. No broad priority or optimal-count claim
is made, and no conjectural improved bound is used.
