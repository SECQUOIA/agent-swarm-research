# Review 1, reviewer R3-lit: citation and novelty audit

Date: 2026-10-03. Manuscript: `paper-certified-support-cuts/main.tex` and
`sections/*.tex` (state of 2026-10-03 11:48). Line numbers are file lines
in `sections/`.

## Method

- Every `\cite*` command in the compiled sections (117 occurrences, 91 keys)
  was listed with `grep` and checked against the source.
- Sources were read in this order: local KB full text
  (`literature/papers/<slug>/fulltext.md`); primary sources downloaded for
  this audit (arXiv PDFs of Nie–Demmel v3, Nie–Qu–Tang–Zhang v3,
  Fantuzzi–Fuentes v3; Murty's Chapter 2 PDF; the Konstanz report version of
  Garloff–Jansson–Smith 2003 JCAM; Anstreicher 2012 Optimization Online
  preprint; Boyd–Vandenberghe PDF; SCIP `src/scip/lp.c` at tags v10.0.0 and
  v10.0.2); and, where no full text was reachable, abstracts and the
  literature-lane reports L1–L5 (marked "lane").
- Bibliography: every entry with a DOI (76) was compared with Crossref
  (`verification/R3-lit_crossref.py`, output
  `verification/R3-lit_crossref.json`). The 12 arXiv-only or arXiv-linked
  entries were checked with the arXiv API. Preprints were searched in
  Crossref for later journal versions.
- Novelty statements were checked against lanes L1–L5 and targeted web
  searches (certified MINLP cuts; nonconvex star QPs with linear rows;
  gluing pair hulls; Radon partitions on the moment curve).
- `verification/R3-lit_radon_check.py` checks, on 3000 random finite
  instances, that the criterion of Theorem 6.3 (alternation) coincides with
  the classical Radon-partition criterion for points on the moment curve
  (0 mismatches).

Verdict codes: **OK** (source says what is attributed, locator correct);
**OK-lane** (verified by a lane report from full text, not re-read here);
**OK-abs** (abstract or metadata level only); **Imprecise** (support is
partial or wording overstates); **Wrong** (source does not say it).

## Summary of findings (most severe first)

No cited result was found to be misused in a way that invalidates a theorem.
The issues are attribution and novelty framing.

| # | Severity | Location | Issue |
|---|---|---|---|
| 1 | major | 06-composition.tex:236–239 (and 06:183–186) | The novelty claim includes "the exact characterizations of Theorems interleave and alternation". The combinatorial core of Theorem 6.3 is the classical description of Radon partitions of points on the moment curve: two finite sets have intersecting moment-curve hulls iff they alternate at least k+1 times (Breen 1973; alternating oriented matroids). Theorem 6.2(ii)'s zero case is the k=2 instance (crossing chords of a parabola). Only the application to gluing interfaces and the exact value δ²/2 are new. |
| 2 | major | 06-composition.tex:6–9, 219–239, 271–284 | Section 6 omits the closest MINLP precedent, Tawarmalani (2010), which is already in the bibliography. Its Example 3.8 (pp. 14–15) shows that separate envelopes are weaker because they use two different convex-combination representations of the same point. Its Corollary 3.10 (p. 16) glues two functions that share u when their inclusion certificates have equal marginals of u. That is the full-marginal gluing statement of Section 6.5, stated for MINLP hulls. |
| 3 | major | 04-original-variables.tex:223–238; 02b-related.tex:79–91 | Müller, Muñoz, Gasse, Gleixner, Lodi, Serrano (2022, Math. Program. 192:89–118) is missing. It studies the surrogate relaxation of MINLPs obtained by aggregating nonlinear constraints, inside SCIP. The hierarchy conv Σ ⊆ ∩_λ conv Σ_λ ⊆ C and the "aggregated sets versus aggregated functions" remark are its subject. |
| 4 | major | 02b-related.tex:55–77; 01-introduction.tex:23 | Two references on joint relaxation of several terms are missing. Davarnia, Richard, Tawarmalani (2017, SIAM J. Optim. 27(3):1801–1833) give simultaneous convexification of bilinear functions over polytopes, i.e. joint graphs with linear rows. Bao, Sahinidis, Tawarmalani (2009, OMS 24(4–5):485–504) give multiterm relaxations, the BARON reference for grouping quadratic terms. |
| 5 | minor | 04-original-variables.tex:211–213 | Misattribution. Liers et al. (2021) do not study "the objective alone". Their problem (OP) is the hull of the graph {(x,z): z=g(x), x∈D} of a vector of constraint functions, each with its own variable z_j. That is the free-remainder case of Proposition 4.6. |
| 6 | minor | 08-implementation.tex:249–251 | Over-attribution. Schichl–Neumaier (2005, §3.1) say that constant folding in DAG simplification must not introduce roundoff. Only Neumaier (2004, §20) observes that modeling systems introduce uncontrolled rounding. |
| 7 | minor | 02b-related.tex:94–95 | "because their overall effect is negative" is overstated for SCIP 8. Bestuzheva et al. (2025) disable intersection cuts ("not clear yet ... when it will be beneficial"), edge-concave cuts ("has not shown to be particularly useful") and gradient-cut tightening ("require more tuning"). SCIP 10 disables flower cuts on continuous products "because of a performance loss". |
| 8 | minor | 05-quadratic-support.tex:104–122 | Proposition 5.3 (MAX CUT, coNP) is folklore and is presented without saying so. Burer–Letchford (2009, §2.3, p. 4) state it as a folklore result, citing Garey–Johnson–Stockmeyer. Del Pia–Khajavirad (2026), Theorem 3, give the stronger, quadratic-specific result: box QP is strongly NP-hard at treewidth two. Lines 132–134 cite only the quartic path result (Theorem 2). |
| 9 | minor | 05-quadratic-support.tex:152–154 | Rikun (1997) is weak support for "convexifying over the constrained domain repairs this". Anstreicher (2012, Thm. 1, Cor. 1), already in the bibliography, is the direct source. |
| 10 | minor | 02b-related.tex:43–45 | The n=3 box counterexample is due to Anstreicher–Burer (2010, p. 8 of the preprint). Burer–Letchford (2009, p. 4) and Anstreicher (2012, p. 8) only report it. Also, for triangulated polytopes AB2010 give a disjunctive extended formulation over the simplices, not SDP+RLT on the polytope. |
| 11 | minor | 01-introduction.tex:76–78 | "to our knowledge, the case with center–leaf rows has not been solved exactly before" is stronger than the hedged 05b-star.tex:276–279. The proof is nonserial dynamic programming (Bertelè–Brioschi 1972) with parametric scalar minimization; cite these as the ingredients. |
| 12 | minor | 04-original-variables.tex:47 | Locator. Boyd–Vandenberghe §5.1(.3) gives the lower-bound property; "weak duality" is named and stated in §5.2.2 (verified in the PDF). |
| 13 | minor | 06-composition.tex:219–227; 02b-related.tex:104–107 | The standard sparse-SDP references are missing: Waki–Kim–Kojima–Muramatsu (2006); Grimm–Netzer–Schweighofer (2007); and Laurent (2009, Cor. 8.7) / Grone et al. (1984), which show that sparse equals dense for quadratics through PSD completion. Kojima–Kim–Arima (2026, §3.3) on overlaps that carry off-diagonal entries is also missing. RLT is used throughout with no citation (Sherali–Adams 1990; Sherali–Tuncbilek 1992), and the SDP relaxation is used without citing Shor. |
| 14 | minor | 05b-star.tex:19 | Moré–Vavasis (1990) is verified only at abstract level: "separable concave ... bounds and one equality ... NP-hard". The paper says "concave separable quadratic". Add the one-line subset-sum reduction, or cite a source that proves the quadratic case. |
| 15 | minor | references.bib `DeyKhajavirad2025` | Now published in Mathematical Programming (online 2026-05-26), DOI 10.1007/s10107-026-02364-y. Cite the journal version and recheck "Corollary 1" against it. |
| 16 | minor | references.bib `SCIPsource10`; 03-certification.tex:45–48 | The source tag is v10.0.0, but the runs use 10.0.2. The rounding lines are identical in both tags (rowAddCoef l. 2223–2225, rowChgCoefPos l. 2401–2403). Cite the version that was run. |
| 17 | minor | references.bib, rendering | (a) `SCIP10` renders as "Technical Report 2511.18580, arXiv". (b) `DelPiaKhajavirad2026`, `Khajavirad2026` and `ZhuHeTawarmalani2026` render with no arXiv number, because plainnat ignores `eprint` and prints only an HTML URL. (c) `Ballerstein2013` loses its DOI and Diss. number. (d) Issue numbers are missing in 8 entries (Table C). |
| 18 | minor | 09-computations.tex:21 | The runs use the current MINLPLib (OSiL files, library metadata), but the citation is the 2003 MINLPLib paper. Also cite the current library (S. Vigerske, MINLPLib, https://www.minlplib.org, with access date). |
| 19 | minor | 02b-related.tex:12; 04:182 | Ballerstein (2013) was not accessed by any lane. The attribution is secondary, via Liers et al. (2021, Prop. 1) and Mertens (2019, Prop. 3.13: "Cor. 5.25"). Add the locator once it is checked, or cite it "as stated in Liers et al." |
| 20 | suggestion | 00-abstract.tex:16 | "We show that exact pair hulls glued on shared moments do not compose" reads as a discovery claim. Section 6 states that the phenomenon is known. Suggested: "We quantify how exact pair hulls glued on shared moments fail to compose:". |
| 21 | suggestion | various | Optional references: Bemporad et al. (2002) and Bhathena et al. (2026) for parametric/tree DP (05b); Margot (2009, testing cut generators) for the replay validity test (09); Xu–Pokutta (2026, joint-range inequalities for QCQPs; arXiv) and Khajavirad (2026, Optimization Online, polynomial-time sparse box POP) as very recent related work; a standard numerical-analysis source for the interpolation remainder in Lemma 3.4; Rockafellar (1970, Cor. 11.5.1) for Proposition 2.1. |
| 22 | suggestion | 04-original-variables.tex:80–83; 03-certification.tex:132–134 | Wording. "equals the dual of its convexification" should be "equals the optimal value of its convexification (under a constraint qualification)". The αBB quantity is the maximal separation of the αBB underestimator of −p (equivalently the concave overestimator of p) with α=M/2. |

## Table A: every citation

| Location | Key(s) | Attributed claim (paraphrase) | Locator | Checked against | Verdict / note |
|---|---|---|---|---|---|
| 01:7 | McCormick1976, SmithPantelides1999, TawarmalaniSahinidis2004 | factorable relaxation with auxiliary variables | – | standard; KB (McCormick, TS2004) | OK |
| 01:23 | Tawarmalani2010, Ballerstein2013, LiersEtAl2021, HeTawarmalani2021, ZhuHeTawarmalani2026 | simultaneous convexification of vectors of univariate, multilinear and composite functions, applications | – | KB (Tawarmalani, Liers, Zhu); HT2021 abstract; Ballerstein via Liers Prop. 1 and Mertens (lane L1) | OK (Ballerstein secondary; finding 19). Missing DRT2017 (finding 4) |
| 01:42 | BestuzhevaEtAl2025 | SCIP detects quadratic/bilinear/convex structure, uses row projections | – | KB SCIP 8 paper | OK |
| 01:77 | DelPiaKhajavirad2026 | box case of star = special case of forest algorithm | – | KB, Thm. 1, p. 4 | OK; novelty wording see finding 11 |
| 02b:6 | McCormick1976, SmithPantelides1999, TawarmalaniSahinidis2004, BelottiEtAl2009, BestuzhevaEtAl2025 | factorable relaxations in global solvers | – | standard | OK |
| 02b:9 | ZhuHeTawarmalani2026 | factorable relaxations ignore linking linear constraints | – | KB p. 2 ("ignoring interdependencies ... induced by linking constraints") | OK |
| 02b:10 | Tawarmalani2010 | inclusion certificates for the hull of several functions | – | KB abstract, Def. 3.4 | OK |
| 02b:12 | Ballerstein2013 | hull of a vector of functions by linear combinations | – | Liers Prop. 1 (secondary) | OK (secondary; finding 19) |
| 02b:13 | LiersEtAl2021 | separation over it in a gas network application | – | KB §3, §5 | OK |
| 02b:14 | HeTawarmalani2021/2022/2024 | composite relaxations with vectors of outer functions | – | HT2021 abstract ("generalize to simultaneous convexification of a vector of outer-functions"); HT2024 KB §4 | OK |
| 02b:16 | ZhuHeTawarmalani2026 | simultaneous factorable graphs with coupling constraints | – | KB §3 ("multilinear compositions with linking constraints") | OK |
| 02b:19 | Rikun1997, LuedtkeNamazifarLinderoth2012, BolandEtAl2017, BaoKhajaviradSahinidisTawarmalani2015 | termwise vs joint gap for multilinear/bilinear terms | – | KB (Rikun, Luedtke, Boland) | OK |
| 02b:21 | MisenerFloudas2012 | solvers group quadratic terms before relaxing | – | title/abstract (edge-concave aggregation) | OK-abs; add BaoSahinidisTawarmalani2009 (finding 4) |
| 02b:22 | TsoukalasMitsos2014, BongartzMitsos2017, NajmanBongartzMitsos2021 | reduced-space relaxations avoid auxiliary variables | – | KB (Tsoukalas–Mitsos); titles | OK |
| 02b:30 | Nowak2005, KaruppiahGrossmann2008, WuMutsNowakHendrix2025 | Lagrangian cuts in block decomposition | – | lane L1/L4 (Nowak habilitation §7.1; book Ch. 7 pp. 83–97 per Crossref); KB Wu | OK-lane |
| 02b:31 | TawarmalaniSahinidis2004, GleixnerEtAl2017 | Lagrangian/duality range reduction | – | KB; lane L1 (§4 pp. 15–17) | OK |
| 02b:32 | DomesNeumaier2016 | rigorous filtering with aggregated constraints | – | lane L3/L4 (§3.1, eqs. (31)–(34)) | OK-lane |
| 02b:35 | Falk1969, Geoffrion1974, FeltenmarkKiwiel2000, LemarechalRenaud2001 | primal form of the Lagrangian dual | – | lanes (Geoffrion IP form; others abstract) | OK-abs/lane |
| 02b:37 | ChenLuedtke2022 | set version for Lagrangian cuts | – | KB Thm. 3 and proof (U^s = P_s via separation, v ≥ 0) | OK |
| 02b:39 | DeyMunozSerrano2022, BlekhermanDeySun2024 | aggregation hulls of quadratic constraints | – | KB | OK |
| 02b:44 | AnstreicherBurer2010 | hull over simplex, 2-D box, small triangulated polytopes via SDP+RLT | – | KB (Thm. 3, Cor. 4, Thm. 6, Thm. 7) | Imprecise (finding 10): triangulated case is a disjunctive extended formulation |
| 02b:45 | BurerLetchford2009, Anstreicher2012 | not so for boxes in higher dimension | – | BL2009 p. 4 and Anstreicher 2012 p. 8 both report AB2010's n=3 example | OK as secondary; add AB2010 (finding 10) |
| 02b:47 | Murty1997 | face enumeration for QP is classical | §2.9 | Murty Ch. 2 PDF, printed pp. 163–165 ("The Method", ≤ 2^m candidate problems) | OK |
| 02b:48 | Vavasis1990 | QP is in NP | – | title/abstract | OK-abs (only NP membership is used) |
| 02b:49 | DelPiaKhajavirad2026 | box QP on forests strongly polynomial | – | KB Thm. 1 | OK |
| 02b:50–51 | DeyKhajavirad2025, Khajavirad2026 | explicit hulls for star-shaped sign patterns | – | KB (DK Thm. 1, Thm. 2; K Thm. 5–6) | OK; DK now published (finding 15) |
| 02b:53 | Vorobev1962, Lasserre2006 | gluing exact with full marginals | – | Vorob'ev abstract (lane); Lasserre KB Lemmas 6.3–6.4 | OK; add Tawarmalani2010 Cor. 3.10 (finding 2) |
| 02b:54 | FantuzziFuentes2025 | finite truncations need extra conditions | – | arXiv v3, Thm. 1.1 (overlap flatness) | OK |
| 02b:55 | NieDemmel2009, NieQuTangZhang2026 | sparse path relaxations can be strictly weaker | – | arXiv v3 of both (Ex. 3.5; Ex. 6.7) | OK |
| 02b:61 | NeumaierShcherbina2004, CookEtAl2009SafeCuts, EiflerGleixner2024 | safe bounds/cuts with bounds and directed rounding | – | KB NS §§3, 6–7; KB EG2024 | OK |
| 02b:63 | CookKochSteffyWolter2013, CheungGleixnerSteffy2017, EiflerGleixner2023 | exact MIP and VIPR certify complete solves | – | titles; KB EG2023 | OK |
| 02b:64 | SCIP10 | SCIP 10 exact mode for MILP | – | KB §3.1 ("restricted to mixed-integer linear programs") | OK |
| 02b:66 | BorradaileVanHentenryck2005, Kearfott2011, DomesNeumaier2012, NininMessineHansen2015 | rigorous linear relaxations, safe estimators | – | lane L3 | OK-lane |
| 02b:67 | GarloffJanssonSmith2003JCAM, GarloffSmith2008, MunozNarkawicz2013 | verified Bernstein bounds | – | Konstanz report §5; lane L3 (GS2008 §5); KB MN2013 | OK |
| 02b:68 | Johansson2017arb | ball arithmetic | – | title | OK |
| 02b:70 | Neumaier2004 | rounding in the problem formulation must be controlled | §20 | KB §20 "Rounding in the problem definition" | OK |
| 02b:70 | SchichlNeumaier2005 | same | – | KB §3.1 (constant folding must avoid roundoff) | OK in this wording; see finding 6 for 08:251 |
| 02b:71 | LiersEtAl2021 | safe rounding of coefficients mentioned without details | – | KB p. 25 ("safe rounding of coefficients") | OK |
| 02b:78 | GrotschelLovaszSchrijver1981, GrotschelLovaszSchrijver1988 | weak separation ⇔ weak optimization for convex bodies | – | KB GLS book Thm. 4.4.7, §4 overview | OK |
| 02b:81 | Gilbert1966, BrierleyNavascuesVertesi2016 | Gilbert: nearby point or separating hyperplane | – | BNV abstract (arXiv v2) | OK |
| 02b:83 | Boyd1994, ChvatalCookEspinoza2013 | Fenchel/local cuts by column generation over an optimization oracle, exact arithmetic | – | titles; lane L5 | OK-lane |
| 02b:85 | BienstockChenMunoz2020 | oracle-based cuts for polynomial optimization | – | title | OK |
| 02b:91 | MullerSerranoGleixner2020 | projections of linear rows for bilinear terms | – | title/abstract | OK |
| 02b:93 | BestuzhevaEtAl2025, SCIP8report | SCIP detects structures, RLT and minor cuts, concave-only variables to binaries | – | KB §2.2 (l. 206–214), §2.3.3–2.3.4 | OK |
| 02b:95 | BestuzhevaEtAl2025, SCIP10 | valid cut families disabled because overall effect is negative | – | KB SCIP 8 l. 323, 335, 391; SCIP 10 l. 495 | Imprecise (finding 7) |
| 02:3–41 | (none) | Proposition 2.1 | – | – | suggestion: cite Rockafellar Cor. 11.5.1 (finding 21) |
| 03:33 | GarloffJanssonSmith2003JCAM | numerically chosen affine bound, rigorous final shift only | §5 | Konstanz report §5 ("not necessary to verify the feasibility or optimality ... We have only to add the constant δ") | OK |
| 03:33 | GarloffSmith2008 | same | – | lane L3 (§5 of author PDF) | OK-lane |
| 03:35 | NeumaierShcherbina2004 | cut parameters chosen in floating point, derivation repeated rigorously | p. 294 | KB p. 294, §7 (quoted) | OK |
| 03:37 | BorradaileVanHentenryck2005 | safe estimators in terms of machine coefficients | – | lane L3 (TR §§2–3) | OK-lane |
| 03:48 | SCIPsource10 | SCIP 10 rounds near-integral row coefficients without adjusting sides | rowAddCoef, rowChgCoefPos in lp.c | lp.c at v10.0.0 and v10.0.2, l. 2223–2225 and 2401–2403 | OK; version mismatch (finding 16) |
| 03:57 | NeumaierShcherbina2004, EiflerGleixner2024 | bound-corrected rounding (eq. 3.1) | – | KB NS §6 (residual enclosure with bounds); lane L3 (EG Lemma 1/Cor. 2) | OK |
| 03:81 | GarloffSmith2008 | Bernstein enclosure | – | lane L3 | OK (classical property) |
| 03:96 | GarloffJanssonSmith2003 | enclosures shrink monotonically with the box | – | abstract (inclusion isotonicity of the control-point hull; multivariate boxes) | OK-abs |
| 03:97 | MunozNarkawicz2013 | Bernstein subdivision formalized in a proof assistant | – | KB (PVS) | OK |
| 03:121 | Johansson2017arb | outward-rounded ball arithmetic | – | title | OK |
| 03:134 | AdjimanEtAl1998 | max separation of αBB with α=M/2 | – | KB l. 201 (d_max formula, from Maranas–Floudas) | OK; wording (finding 22) |
| 03:196 | Mangasarian1999 | dual-norm bound on violation of a hyperplane | – | lane L3 (Thm. 2.2) | OK-lane |
| 03:198 | Tawarmalani2010 | inclusion certificate | – | KB Def. 3.4 | OK |
| 04:47 | BoydVandenberghe2004 | weak Lagrangian duality | §5.1 | BV PDF: §5.1.3 lower bounds; §5.2.2 "Weak duality" | Imprecise locator (finding 12) |
| 04:50 | Nowak2005 | Lagrangian cut of a block in the extended block-separable reformulation | §7.1 | lane L1/L4 (habilitation §7.1.3, eq. (7.9)); book Ch. 7 "Cuts, Lower Bounds and Box Reduction" (Crossref) | OK-lane |
| 04:53 | TawarmalaniSahinidis2004, KaruppiahGrossmann2008 | related cuts and range reductions | – | KB TS2004; KG title | OK |
| 04:54 | DomesNeumaier2016 | related | – | lane | OK-lane |
| 04:83 | Falk1969, Geoffrion1974, FeltenmarkKiwiel2000, LemarechalRenaud2001 | Lagrangian dual = dual of convexification in joint space | – | lanes | OK; wording (finding 22) |
| 04:84 | ChenLuedtke2022 | separation argument | Thm. 3 | KB Thm. 3 proof | OK |
| 04:121 | Nowak2005, WuMutsNowakHendrix2025 | block convex-hull relaxations keep rows inside the block | §3 | lane (Nowak (3.12)–(3.14)); Wu abstract (CHR) | OK |
| 04:125 | TawarmalaniSahinidis2005 | lifted OA tighter than OA in original space for the same points | – | lane L1 (Thm. 1, p. 227) | OK-lane |
| 04:182 | Nowak2005 | joint relaxations dominate separate envelopes | Lemma 3.4 | lane L1 (habilitation pp. 31–32) | OK-lane |
| 04:182 | Tawarmalani2010, LiersEtAl2021 | same | – | KB (Tawarmalani p. 1 example; Liers abstract) | OK |
| 04:213 | LiersEtAl2021 | "the objective alone ... is the case studied by Liers et al." | – | KB §2 (OP): min c^T(x,z) s.t. z = g(x), x ∈ D | **Wrong** (finding 5) |
| 04:223 | Geoffrion1974, Nowak2005 | x²=1/4 gap is a Lagrangian duality gap | – | lanes | OK |
| 04:228 | DeyMunozSerrano2022 | aggregation closure of sets | – | KB | OK (illustrative) |
| 04:224–238 | (none) | hierarchy conv Σ ⊆ ∩ conv Σ_λ ⊆ C | – | – | missing Müller et al. 2022 (finding 3) |
| 04:260 | NeumaierShcherbina2004, CookEtAl2009SafeCuts, EiflerGleixner2024 | bound-corrected rounding of safe LP bounds/cuts | – | as above | OK |
| 05:99 | Vavasis1990 | QP in NP | – | abstract | OK-abs |
| 05:100 | Murty1997 | total enumeration of faces | §2.9 | Murty Ch. 2 PDF pp. 163–165 | OK |
| 05:104–122 | Karp1972, GareyJohnsonStockmeyer1976 | unweighted MAX CUT NP-hard | – | Report B source ledger (Karp p. 97); GJS title | OK; folklore not acknowledged (finding 8) |
| 05:134 | DelPiaKhajavirad2026 | box quartic strongly NP-hard on paths | – | KB Thm. 2, p. 18 | OK; add Thm. 3 (finding 8) |
| 05:154 | Rikun1997, ZhuHeTawarmalani2026, WuMutsNowakHendrix2025 | convexifying over the constrained domain repairs factorable weakness | – | Zhu p. 2/Thm. 8; Wu Prop. 1 (lane); Rikun only on polytope envelopes | Imprecise for Rikun (finding 9) |
| 05:156 | (none) | "reformulation–linearization products" | – | – | missing Sherali–Adams (finding 13) |
| 05:158 | AnstreicherBurer2010 | SDP+RLT describes hull on a triangle | – | KB Cor. 4 (DNN on simplex, n ≤ 3) | OK |
| 05:163 | MullerSerranoGleixner2020 | projection-based envelopes for bilinear terms | – | abstract | OK |
| 05b:19 | MoreVavasis1990 | concave separable quadratic over box + one row NP-hard | – | abstract (separable concave, bounds, one equality, NP-hard) | OK-abs; "quadratic" unverified (finding 14) |
| 05b:92 | DelPiaKhajavirad2026 | forests in O(n²); root merge O(k²) on a star | – | KB Thm. 1 proof (merge costs O(d_v m_v)) | OK |
| 05b:108 | DeyKhajavirad2025 | SOC star hulls assume sign patterns and box | – | KB (QP(G) on [0,1], plus/minus loops) | OK |
| 05b:109 | BienstockMunoz2018 | LP approximations allow constraints, approximate | – | lane L2 (Thm. 4) | OK-lane |
| 05b:124 | DelPiaKhajavirad2026 (citeauthor) | irrational breakpoints handled exactly via algebraic representation | – | KB l. 69 (τ0+τ1√D), Lemma 16 | OK |
| 06:9 | Lasserre2006, NieDemmel2009, FantuzziFuentes2025 | finitely many shared moments do not determine the shared distribution | – | KB Lasserre proof of Thm. 3.6; FF p. 3 | OK; add Tawarmalani2010 (finding 2) |
| 06:26 | AnstreicherBurer2010 | 2-D box hull = SDP+RLT | – | KB Thm. 6 (preprint numbering; journal Thm. 2 per BNW) | OK (no locator given) |
| 06:185 | KarlinStudden1966 | signed measure annihilating degree ≤ k has ≥ k+1 sign changes | – | not accessed (book) | Standard; add Breen 1973 (finding 1) |
| 06:216 | Lasserre2006 | measures with equal marginals glue | Lemma 6.3 | KB Lemma 6.3 (two blocks); FF cite the journal with the same numbering ("[11, Lemma 6.4]") | OK |
| 06:222 | NieDemmel2009 | numerical quartic path example | Example 3.5 | arXiv v3 p. 8 (f_Δ ≈ 5e-5 < f_sos ≈ 0.8499) | OK (arXiv numbering) |
| 06:223 | NieQuTangZhang2026 | box quartic, sparse hierarchy never tight | Example 6.7 | arXiv v3 (x ∈ [−1,1]³, p1 = −(x2²+1)^(−1) not polynomial; dense tight) | OK (arXiv numbering; recheck in journal) |
| 06:226 | Lasserre2006 | finite gluing needs rank conditions on overlaps | Thm. 3.7 | KB Thm. 3.7 (rank M_s0(y,I_jk)=1) | OK |
| 06:227 | FantuzziFuentes2025 | same | – | arXiv v3 Thm. 1.1 | OK |
| 06:228 | DeyKhajavirad2025 | decomposition across complete separator with no plus loop | Corollary 1 | KB Cor. 1 (arXiv) | OK (recheck in journal version) |
| 06:230 | Khajavirad2026 | builds on this decomposition | – | lane L2 (Lemma 4) | OK-lane |
| 06:257 | BurerNatarajanWillemsen2025 | n ≤ 3, nonpositive off-diagonals: SDP + part of RLT exact | Theorem 1 | KB Thm. 1 (SDP + RLT upper bounds, submodular, n ≤ 3) | OK |
| 06:274 | Vorobev1962, Lasserre2006 | running-intersection gluing with full marginals | – | as above | OK |
| 06:279 | Padberg1989 | McCormick exact on forests (unit box) | Proposition 8 | KB Prop. 8 (QP^G = QP^G_LP iff G acyclic, binary) | OK; continuous case uses vertex property (argued in text) |
| 07:75 | Boyd1994, ChvatalCookEspinoza2013 | Fenchel/local cut separation scheme | – | lane L5 | OK-lane |
| 07:123 | Gilbert1966, BrierleyNavascuesVertesi2016 | Gilbert variant, calls independent of k | – | BNV abstract | OK |
| 07:126–131 | GrotschelLovaszSchrijver1988 | WSEP from WOPT without radius; convex bodies full-dimensional; WSEP almost valid on S(K,−δ) | – | KB Thm. 4.4.7; GLS definitions | OK |
| 07:173 | DelPiaKhajavirad2026 | quartic path hardness | – | KB Thm. 2 | OK |
| 08:3, 08:144 | SCIP10 | SCIP 10; exact mode MILP only | – | KB | OK |
| 08:4 | PySCIPOpt | PySCIPOpt | – | Crossref | OK |
| 08:249 | PnueliSiegelSingerman1998, Necula2000 | translation validation | – | titles | OK |
| 08:250 | Neumaier2004 | modeling systems introduce uncontrolled rounding | §20 | KB §20 | OK |
| 08:250 | SchichlNeumaier2005 | same | – | KB §3.1, §8.2 | Imprecise (finding 6) |
| 08:266 | Rabinowitsch1930 | d≠0 ⇔ ∃u: du=1 | – | standard | OK |
| 08:268 | BestuzhevaEtAl2025 | positive tolerance for strict domains in benchmark setups | – | KB §3.2.1 ("bounded away from zero by 10^-9") | OK |
| 08:270 | BelottiEtAl2009 | x^y = exp(y log x) needs x>0 | compare | lane L3 (§2: "Otherwise, all solutions x such that x_j = 0 are excluded") | OK-lane |
| 09:21 | BussieckDrudMeeraus2003 | MINLPLib | – | Crossref | OK; current library (finding 18) |
| 09:303 | LodiTramontani2013 | performance variability | – | abstract | OK |
| A:151 | GrotschelLovaszSchrijver1988 | central-cut ellipsoid method | Theorem 3.2.1 | KB (3.2.1) | OK |
| A2:24 | BenOr1983 | depth Ω(log N − n) for N components | – | standard statement | OK |

## Table B: novelty and priority statements

| Location | Statement | Evidence | Verdict |
|---|---|---|---|
| 00:16–20 | "We show that exact pair hulls glued on shared moments do not compose ..." | Section 6 itself says the phenomenon is known | Reframe (finding 20) |
| 01:55–59; 02b:72–74 | "to our knowledge, no published MINLP implementation combines them to certify joint support cuts against the source model [and the stored row]" | L3 found no such implementation. Web search (certified/verified cuts, nonconvex MINLP, 2023–2026) found only MILP work (Eifler–Gleixner, VIPR, SCIP 10 exact mode) and convex-MINLP certificates (Halbig et al. 2024). Liers et al. mention safe rounding without detail. | Supported as hedged |
| 01:64–66; 04:12–14, 80–88 | closure = set version of classical primal characterization | lanes L1/L4 | Properly hedged |
| 01:70–72; 05:100–102 | "classical face enumeration, made precise for certificates" | Murty §2.9 | Properly hedged |
| 01:76–78 | "to our knowledge, the case with center–leaf rows has not been solved exactly before" | L2 and own search found no exact algorithm. Bienstock–Muñoz is approximate; DK, DK-SOC and Khajavirad (Aug 2026, OO) are box-only. | Supported, but align with 05b wording and credit the DP ingredients (finding 11) |
| 05b:276–279 | "We know of no earlier exact algorithm for nonconvex stars with center–leaf rows; the construction ... is elementary" | as above | Supported |
| 05:248–255 | Ω((m+k) log(m+k)) optimality by Ben-Or | standard technique | Fine |
| 06:6–9 | failure of gluing and its reason are known | Lasserre, ND, FF; also Tawarmalani 2010 Ex. 3.8 / Cor. 3.10 | Properly hedged; add Tawarmalani (finding 2) |
| 06:183–187 | criterion is a consequence of the classical sign-change fact | Karlin–Studden; also Breen 1973 | Correct, but attribution incomplete (finding 1) |
| 06:236–239 | "To our knowledge, a degree-two example with exact pair hulls, an exact rational gap, a separating cut in the existing coordinates, and the exact characterizations of Theorems 6.2 and 6.3 have not been given before." | Example/witness/cut/δ²/2 family: no precedent found (L1, L2, own search). The characterization in Thm. 6.3 (finite case) equals the Radon-partition criterion for the moment curve (Breen 1973, Israel J. Math. 15:156–157, DOI 10.1007/BF02764601; alternating oriented matroids, Björner et al. 1999, DOI 10.1017/CBO9780511586507); checked numerically, 0/3000 mismatches. | **Overstated** (finding 1) |
| 07:9–13; 01:96–98 | "The tools are classical, and we do not claim the principle as new" | lanes L5 | Properly hedged |
| 01:128 | no new convexification principle | – | Fine |
| 03:30–37 | the principle of the exported-row proposition is established | GJS §5, NS p. 294, BVH | Properly hedged |
| 05:104–122 | Proposition 5.3 stated without "well known" | Burer–Letchford 2009 §2.3 p. 4 ("folklore"), GJS 1976 | Add attribution (finding 8) |
| 03:132 | chord bound is "the classical remainder of linear interpolation" | standard | Fine; add a citation (finding 21) |

## Table C: bibliography check (88 entries)

Crossref comparison of title, authors (family names and count), journal,
volume, issue, pages and print year, for every entry with a DOI. Name
differences that come only from TeX accent macros (for example `M{\"u}ller`)
are not listed.

| Key | DOI | Result |
|---|---|---|
| AdjimanEtAl1998 | 10.1016/S0098-1354(98)00027-1 | match |
| AnstreicherBurer2010 | 10.1007/s10107-010-0355-9 | match; issue 1–2 missing |
| Ballerstein2013 | 10.3929/ethz-a-009959194 | DataCite DOI; resolves to ETH Research Collection; DOI and Diss. No. not printed by plainnat |
| BelottiEtAl2009 | 10.1080/10556780903087124 | match (Crossref title has a typo, bib is correct) |
| BestuzhevaEtAl2025 | 10.1007/s10898-023-01345-1 | match (91(2):287–310, 2025) |
| BienstockChenMunoz2020 | 10.1007/s10107-020-01484-3 | match |
| BlekhermanDeySun2024 | 10.1137/22M1528215 | match |
| BorradaileVanHentenryck2005 | 10.1007/s10107-004-0533-8 | match |
| Boyd1994 | 10.1287/opre.42.1.53 | match |
| BussieckDrudMeeraus2003 | 10.1287/ijoc.15.1.114.15159 | match |
| ChenLuedtke2022 | 10.1287/ijoc.2022.1185 | match; arXiv 2106.04023 matches |
| CheungGleixnerSteffy2017 | 10.1007/978-3-319-59250-3_13 | match; arXiv 1611.08832 matches |
| ChvatalCookEspinoza2013 | 10.1007/s12532-013-0052-9 | match |
| CookEtAl2009SafeCuts | 10.1287/ijoc.1090.0324 | match |
| CookKochSteffyWolter2013 | 10.1007/s12532-013-0055-6 | match |
| DeyMunozSerrano2022 | 10.1137/21M1428583 | match |
| DomesNeumaier2012 | 10.1007/s10898-011-9722-1 | match |
| DomesNeumaier2016 | 10.1007/s10107-014-0851-4 | match |
| EiflerGleixner2023 | 10.1007/s10107-021-01749-5 | match |
| EiflerGleixner2024 | 10.1137/23M156046X | match |
| Falk1969 | 10.1137/0307039 | match |
| FeltenmarkKiwiel2000 | 10.1137/S1052623498332336 | match |
| GarloffJanssonSmith2003 | 10.1007/s00607-003-1471-7 | match |
| GarloffJanssonSmith2003JCAM | 10.1016/S0377-0427(03)00422-9 | match |
| Geoffrion1974 | 10.1007/BFb0120690 | match |
| Gilbert1966 | 10.1137/0304007 | match |
| GleixnerEtAl2017 | 10.1007/s10898-016-0450-4 | match; issue 4 missing |
| GrotschelLovaszSchrijver1981 | 10.1007/BF02579273 | match |
| GrotschelLovaszSchrijver1988 | 10.1007/978-3-642-97881-4 | match |
| HeTawarmalani2021 | 10.1007/s10107-020-01541-x | match; issue 1–2 missing |
| HeTawarmalani2022 | 10.1287/moor.2021.1162 | match |
| HeTawarmalani2024 | 10.1137/22M1515537 | match |
| Johansson2017arb | 10.1109/TC.2017.2690633 | match |
| Karp1972 | 10.1007/978-1-4684-2001-2_9 | match |
| KaruppiahGrossmann2008 | 10.1007/s10898-007-9203-8 | match |
| Kearfott2011 | 10.1080/10556781003636851 | match |
| Lasserre2006 | 10.1137/05064504X | match |
| LemarechalRenaud2001 | 10.1007/PL00011429 | match |
| LiersEtAl2021 | 10.1007/s10898-020-00974-0 | match |
| LodiTramontani2013 | 10.1287/educ.2013.0112 | match |
| Mangasarian1999 | 10.1016/S0167-6377(98)00049-2 | match |
| MisenerFloudas2012 | 10.1007/s10107-012-0555-6 | match; issue 1 missing |
| MullerSerranoGleixner2020 | 10.1137/19M1249825 | match |
| MunozNarkawicz2013 | 10.1007/s10817-012-9256-3 | match |
| Necula2000 | 10.1145/349299.349314 | match |
| Neumaier2004 | 10.1017/S0962492904000194 | match |
| NeumaierShcherbina2004 | 10.1007/s10107-003-0433-3 | match |
| NininMessineHansen2015 | 10.1007/s10288-014-0269-0 | match |
| Nowak2005 | 10.1007/3-7643-7374-1 | match (Ch. 3 pp. 21–31, Ch. 7 pp. 83–97) |
| PnueliSiegelSingerman1998 | 10.1007/BFb0054170 | match |
| Rabinowitsch1930 | 10.1007/BF01782361 | match; issue 1 missing |
| SchichlNeumaier2005 | 10.1007/s10898-005-0937-x | match |
| SmithPantelides1999 | 10.1016/S0098-1354(98)00286-5 | match |
| TawarmalaniSahinidis2004 | 10.1007/s10107-003-0467-6 | match |
| TawarmalaniSahinidis2005 | 10.1007/s10107-005-0581-8 | match |
| Vavasis1990 | 10.1016/0020-0190(90)90100-C | match |
| WuMutsNowakHendrix2025 | 10.1007/s10898-024-01376-2 | match; issue 2 missing |
| Anstreicher2012 | 10.1007/s10107-012-0602-3 | match |
| BaoKhajaviradSahinidisTawarmalani2015 | 10.1007/s12532-014-0073-z | match |
| BenOr1983 | 10.1145/800061.808735 | match |
| BienstockMunoz2018 | 10.1137/15M1054079 | match |
| BolandEtAl2017 | 10.1007/s10107-016-1031-5 | match |
| BongartzMitsos2017 | 10.1007/s10898-017-0547-4 | match |
| BurerLetchford2009 | 10.1137/080729529 | match |
| GareyJohnsonStockmeyer1976 | 10.1016/0304-3975(76)90059-1 | match |
| LuedtkeNamazifarLinderoth2012 | 10.1007/s10107-012-0606-z | match |
| McCormick1976 | 10.1007/BF01580665 | match |
| MoreVavasis1990 | 10.1007/BF01588800 | match; issue 1–3 missing |
| NajmanBongartzMitsos2021 | 10.1007/s10898-020-00977-x | match |
| NieDemmel2009 | 10.1137/060668791 | match |
| NieQuTangZhang2026 | 10.1007/s10107-025-02223-2 | match; issue 1–2 missing |
| Padberg1989 | 10.1007/BF01589101 | match |
| PySCIPOpt | 10.1007/978-3-319-42432-3_37 | match |
| Rikun1997 | 10.1023/A:1008217604285 | match |
| TsoukalasMitsos2014 | 10.1007/s10898-014-0176-0 | match |
| Vorobev1962 | 10.1137/1107014 | match |
| DelPiaKhajavirad2026 | arXiv 2609.35595 | arXiv: title/authors match (v1, 2026-09-28); arXiv number not printed (bib uses `eprint`, ignored by plainnat) |
| Khajavirad2026 | arXiv 2601.18545 | match (v2, 2026-02-12); arXiv number not printed |
| ZhuHeTawarmalani2026 | arXiv 2603.18458 | match (v1); arXiv number not printed |
| BurerNatarajanWillemsen2025 | arXiv 2504.03996 | match (v3, 2026-08-31); no journal version found |
| DeyKhajavirad2025 | arXiv 2508.18435 | **published**: Math. Program. (online 2026-05-26), DOI 10.1007/s10107-026-02364-y |
| FantuzziFuentes2025 | arXiv 2502.01410 | match (v3, 2026-07-06); no journal version found |
| SCIP10 | arXiv 2511.18580 | authors (34) and title match; renders as "Technical Report 2511.18580, arXiv" |
| BrierleyNavascuesVertesi2016 | arXiv 1609.05011 | match (v2, 2017-01-05) |
| EiflerGleixner2024 / EiflerGleixner2023 / HeTawarmalani2024 | arXiv 2303.12365 / 2101.09141 / 2310.07168 | match |
| Tawarmalani2010 | Optimization Online 2722 | KB copy dated 2010-09-05; no journal version found |
| GarloffSmith2008 | no DOI | lane L3 (author PDF hash recorded) |
| SCIPsource10 | GitHub tag v10.0.0 | exists; runs used v10.0.2 (finding 16) |

Not checked for lack of an identifier: BoydVandenberghe2004 (URL works,
TOC verified), Murty1997 (author PDF works), KarlinStudden1966 (book),
SCIP8report (ZIB-Report 21-41).

## Missing references an expert referee would ask for

Major (see findings 2–4):
- Tawarmalani 2010, Ex. 3.8 and Cor. 3.10 (already in the bibliography), in Section 6.
- Breen, M. (1973). Primitive Radon partitions for cyclic polytopes. Israel J. Math. 15:156–157. DOI 10.1007/BF02764601. Also Björner, Las Vergnas, Sturmfels, White, Ziegler, *Oriented Matroids*, 2nd ed., CUP 1999 (alternating matroids). In Section 6.3.
- Müller, Muñoz, Gasse, Gleixner, Lodi, Serrano (2022). On generalized surrogate duality in mixed-integer nonlinear programming. Math. Program. 192:89–118. DOI 10.1007/s10107-021-01691-6. In Section 4.3.
- Davarnia, Richard, Tawarmalani (2017). Simultaneous convexification of bilinear functions over polytopes with application to network interdiction. SIAM J. Optim. 27(3):1801–1833. DOI 10.1137/16M1066166.
- Bao, Sahinidis, Tawarmalani (2009). Multiterm polyhedral relaxations for nonconvex, quadratically constrained quadratic programs. Optim. Methods Softw. 24(4–5):485–504.

Minor:
- Sherali–Adams (1990), SIAM J. Discrete Math. 3(3):411–430, and Sherali–Tuncbilek (1992), J. Global Optim. 2:101–112, for RLT. Shor (1987) for the SDP relaxation.
- Waki, Kim, Kojima, Muramatsu (2006), SIAM J. Optim. 17(1):218–242. Grimm, Netzer, Schweighofer (2007), Arch. Math. 89:399–403. Laurent (2009), IMA Vol. 149, §8.1. Grone, Johnson, Sá, Wolkowicz (1984). Kojima, Kim, Arima (2026, arXiv 2606.21823).
- Del Pia–Khajavirad 2026, Theorem 3 (already cited paper; add the locator).
- Bertelè–Brioschi (1972), *Nonserial Dynamic Programming*; Bemporad et al. (2002), Automatica 38(1):3–20; Bhathena et al. (2026), Math. Program. 218:291–336.
- Margot (2009), Math. Program. Comput. 1(1):69–95, on testing cut generators.
- Current MINLPLib (minlplib.org).

Suggestions: Xu–Pokutta (2026), joint-range inequalities for QCQPs
(arXiv); Khajavirad (Aug 2026, Optimization Online), "A polynomial-time
solvable class of sparse box-constrained polynomial optimization
problems"; Hong–Stahl (1995) for the original inclusion-isotonicity proof
(credited in the GJS 2003 abstract); Rockafellar (1970).

## Scratch files written by R3-lit

- `verification/R3-lit_crossref.py`, `verification/R3-lit_crossref.json`
- `verification/R3-lit_radon_check.py`

Downloaded sources used for checks are in `/tmp/r3lit/` and are not part
of the repository.
