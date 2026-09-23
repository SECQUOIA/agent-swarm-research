# Literature evidence and claim boundaries

Stage 1 inspection date: 2026-09-13. Local literature instructions were read at
`literature/AGENTS.md`. No local literature package or generated index was modified;
no literature original is redistributed in this paper folder. User-supplied PDFs
were read locally. Source access below describes this stage, not every historical
agent's work. Later authors must inspect the sources supporting their own theorems.

## Sources actually inspected for the foundations

- **Liu et al. (2016), Sensor Selection for Estimation with Correlated Measurement
  Noise**, IEEE TSP 64(13), 3509–3522, DOI
  [10.1109/TSP.2016.2550005](https://doi.org/10.1109/TSP.2016.2550005).
  Local `liu2016-sensor-selection-for-estimation-with` fulltext read at PDF p.3
  (Eqs. 5–11), pp.6–7 (Eqs. 29–32, Proposition 2 and criterion terminology),
  with context on model/greedy gains. Re-extracted original via `pdftotext -layout`
  to `/tmp/measurement-stage01/liu.txt`; visually inspected original PDF p.7.
  Original Eq. 7 selects covariance before inversion; Eq. 11 uses a scalar split;
  Eqs. 29–31 discuss full-inverse gating and the altered signal-gating experiment;
  Proposition 2 gives first-order agreement for weak correlation. The source's
  broad verbal “only” weak-correlation language must not be repeated as a
  necessary condition for exactness of every special subset/sensitivity pair.
  This paper derives the precise equality condition instead. Primary author PDF:
  https://ecs.syr.edu/faculty/fardad/Papers/LiuCheFarMasLeuVar16.pdf . Its existing
  SHA-256 is `462fc51fe3ed9608af9682d9cd35a099fd1a813b826146e0010826fd06954e22`.

- **Wang et al. (2024), Measure This, Not That**, C&CE 189, 108786,
  DOI [10.1016/j.compchemeng.2024.108786](https://doi.org/10.1016/j.compchemeng.2024.108786).
  Local `wang2024-measure-this-not-that-optimizing-2` is the accepted manuscript,
  DOI-linked OSTI record https://www.osti.gov/biblio/2447595 and manuscript
  https://www.osti.gov/servlets/purl/2447595 . Read printed pp.8–12 (PDF pp.9–13)
  for Eqs. 6–16 and implementation, and source-model/covariance passages using
  the extracted text. Visually inspected PDF p.10 (printed p.9), confirming that
  Eqs. 8–10 explicitly extract full inverse entries/blocks. `pdftotext -layout`
  independently confirms Eq. 11 pair gating and Eq. 12 trace objective. The
  historical audit compares these pages to arXiv:2406.09557v1 and visually checks
  the SI asymmetry; Stage 1 did not repeat that entire page-by-page comparison.
  Accepted-manuscript SHA-256:
  `7c6b6bb18044097ec4c6acb151db007a3c7831399a6c19ca819a5fcfd23ad6d0`.
  Publisher final typeset article remains uninspected; the paper states this
  boundary instead of asserting identity with it. The manuscript's statement
  that determinant is concave is not inherited: log determinant and determinant
  root are the relevant concave functions. The conventional A criterion is also
  distinguished from the source's maximized trace information.

- **Public measurement software**, immutable commit
  `430090e610446aab88328ce495ffb15b684c56c4` (2025-01-14):
  https://github.com/dowlinglab/measurement-opt/tree/430090e610446aab88328ce495ffb15b684c56c4 .
  Existing local source tree under `/tmp/minlp-measurement-source-audit-20260912/`
  was reused. `code/measurement_selection_source_audit.py` executed the unchanged
  author coefficient methods in this stage and checked exact witnesses and all
  64 six-channel patterns. Source locators from the repository audit:
  `measure_optimize.py` 757–841 computes a full pseudoinverse; 843–923 forms
  coefficients; 1157–1188 sums pair contributions; `kinetics_MO.py` 69–109 gives
  same-time covariance; `rotary_bed_MO.py` 101–108 gives diagonal covariance.
  No claim is made to deserialize/reproduce the source authors' stored designs.
  The public CSV's decimal values specify an as-stored statistical test problem;
  a complete generator/scaling provenance was not established. License evidence
  is file-specific; absence of a repository-wide license must not be replaced
  by an invented license in a supplement.

- **Patan and Bogacka (2007), Optimum experimental designs for dynamic systems
  in the presence of correlated errors**, CSDA 51, 5644–5661,
  DOI [10.1016/j.csda.2007.05.030](https://doi.org/10.1016/j.csda.2007.05.030).
  Local fulltext and original now available as a user-supplied Sep13 promotion,
  `patan2007-optimum-experimental-designs-for-dynamic`. Read PDF pp.1–5:
  multiresponse dynamic model, response- and time-correlated errors,
  parameter-dependent covariance contribution to Fisher information, local
  sensitivities, D criterion and efficiency, and exchange procedure context.
  Thus Sep12 audit statements that this source was abstract-only are stale.
  It directly precedes correlated-error kinetic sampling and must be discussed
  in the introduction/computational comparison. No global-certification absence
  is inferred just from its abstract.

- **Hainy, Müller and Pázman (2025), Practical aspects of the virtual noise
  convex optimum design approach for correlated responses**, arXiv:2504.17651v1,
  https://arxiv.org/abs/2504.17651 . Local fulltext inspected at PDF pp.1–2
  (correct covariance, D and conventional A criteria), pp.5–7 (Proposition 3,
  Liu/virtual-noise equivalence), and algorithm/criterion passages. Primary arXiv
  page checked online this stage: v1, 2025-04-24, 33 pages, no later version or
  journal reference listed at access. This already publishes the equivalence
  found independently in the repository; do not claim that equivalence new.
  Its simplicial decomposition and exchange methods are essential prior art.

- **Pázman, Hainy and Müller (2022), A convex approach to optimum design of
  experiments with correlated observations**, EJS 16(2), 5659–5691,
  DOI [10.1214/22-EJS2071](https://doi.org/10.1214/22-EJS2071).
  Read local source note and beginning of fulltext; the Stage 1 claim is only
  its established selected-covariance model. Detailed theorem reading is assigned
  to certification stage. The local retained original is a preprint, not the
  final EJS layout. Online Project Euclid opening returned an iframe-only page.
  Author-institution primary metadata confirms final pages **5659–5691**, fixing
  a draft bibliography transcription:
  https://research.jku.at/en/publications/a-convex-approach-to-optimum-design-of-experiments-with-correlate/ .

- **Sagnol and Harman (2015), Computing exact D-optimal designs by mixed integer
  second-order cone programming**, Annals of Statistics 43(5), 2198–2224,
  DOI [10.1214/15-AOS1339](https://doi.org/10.1214/15-AOS1339).
  Local original/fulltext first-page metadata and criterion description checked;
  source-grounded local note read for subsystem criteria and conic/side-constraint
  scope. Deeper theorem inspection is required in the separator/certification
  stage. Existing matrix-atom design/MISOCP criteria are not new here.

- **Moradi, Furuichi and Heydarbeygi (2019), New Refinement of the Operator
  Kantorovich Inequality**, Mathematics 7(2), 139,
  DOI [10.3390/math7020139](https://doi.org/10.3390/math7020139).
  Direct publisher page returned HTTP 429 this stage. An indexed publisher-hosted
  primary collected PDF exposes the article's first page and Eq. 1, explicitly
  stating inverse-compression bound and attributing it to prior work:
  https://mdpi-res.com/bookfiles/book/1955/Inequalities.pdf?v=1749949339 .
  This is the source for attribution, not a claim to read the whole collection.
  Our elementary proof is included; the sharp optimization consequences are
  described as consequences, with no first-inequality claim.

## Topic-level literature boundaries for remaining stages

The following is a source map from inspected research priority audits and present
KB status, not a claim that Stage 1 re-read all these full proofs.

| Source family | Relationship and next reading obligation |
|---|---|
| Lee–Gómez–Atamtürk, *Convexification of multi-period quadratic programs with indicators* | Primary Springer HTML confirmed online, published 2026-07-22, DOI https://doi.org/10.1007/s10107-026-02379-5 . Noiseless complete-block selected-inverse path hull is known. Stage 2 must reproduce affine sensitivity image, telescoping forward/reverse terms and singular-transition limit without claiming new hull. |
| Wei–Atamtürk–Gómez–Küçükyavuz principal-inverse polytope | General principal-inverse convexification antecedent, DOI 10.1007/s10107-023-01982-0; local source exists. |
| Vecchia 1988 | Full local source now user-supplied Sep13; first principles of truncated chronological conditionals inspected at extracted Section 3, PDF around pp.5–6. DOI 10.1111/j.2517-6161.1988.tb01729.x. Stage 2 must credit construction and compare the precise operator bound and optimization transfer; subset uniformity alone is not a novelty distinction because suitable class-uniform full-calendar results transfer by independent dummy-block padding. |
| Inverse decay, FSAI, Baxter and filter stability | Read covariance-decay/FSAI audits and actual cited primary theorems in Stage 2; old direct-sum proposal is unproved, whereas newer general-covariance proof is separate. Use actual local fulltext status rather than historic missing-source labels. Carry over the dummy-block padding and block-diagonal normalization reductions from `notes/research-20260912-general-covariance-memory-bound.md`, Section 8, and `notes/research-20260912-covariance-decay-priority-audit.md`, lines 34–55; removing an upper bound on original diagonal blocks alone does not defeat older bounded-spectrum theory. |
| Kaminetz thesis vs Kaminetz–Webber March 2026 | Distinct artifacts/statements. March paper arXiv:2603.05709v1, *Everything is Vecchia: Unifying low-rank and sparse inverse Cholesky approximations*, has no thesis supermodularity assertion. Repeated-pair Kaporin example separates metric scaling; it is not a counterexample to the paper. The global Gaussian KL eigenvalue identity already yields a relative precision and mean-Fisher sandwich (`notes/research-20260912-noisy-markov-fsai-priority-audit.md`, Section 5). Stage 2 must explain this implication and restrict the comparison to model hypotheses, constants, chronological calendar windows and horizon dependence. |
| Das–Kempe STOC2008; Mahalanabis–Štefankovič 2012 | Scalar noisy-chain FPTAS existence novelty is unsafe. The detailed target-node reduction includes theorem adaptations, polynomial conditioning, and avoidance of a printed local-cost inverse/block error. Stage 3 must check original recurrence, not merely quote source metadata. |
| Approximate Pareto sets, Berstein et al. nonlinear matroid/profile machinery, normalization by selected vectors | Critical spectral-cover antecedents. Stage 3 must state precisely what complete matrix sandwich/range preservation adds, fixed-p complexity and rational representation restriction; no generic Pareto/profile novelty. |
| Sagnol–Harman, generalized correlated-block information atoms, Holland-Letz/Dette and mixed-effects designs | Whole schedules as information atoms and nuisance/subsystem criteria are established. Stage 4 must read now-available full text for stronger comparisons. |
| Balas; Papageorgiou–Trespalacios disjunction grouping | Grouping patterns can tighten relaxations at exponential local cost; changing latent anchor representation additionally needs the explicit Schur/projection proof. |
| Wang–Yue2026 robust kinetic design, standardized maximin/D-efficiency antecedents | `wang2026-robust-sampling-time-design-for` is now supplied locally. Stage 4 must compare actual robust criterion/scenarios; maximin and normalization are not new. |
| Ahipaşaoğlu–Cipolla–Gondzio2026 | Root checked accessible primary https://link.springer.com/article/10.1007/s12532-026-00326-1 . Column generation for independent regression vectors; “correlated” generated vectors there are not correlated measurement errors. Generic column generation is prior art. |
| Filová2026 multiresponse exact design under linear/sparsity constraints | Root found https://onlinelibrary.wiley.com/doi/abs/10.1002/asmb.70072 ; later stages should inspect primary content for block/packet overlap. Not used as full-text evidence in foundations. |
| Uciński–Patan CDC2024 | DOI 10.1109/CDC56724.2024.10886743; root retry of primary PaperPlaza PDF returned 404. Indexed abstract mentions noise split/simplicial decomposition/A-optimality, insufficient to exclude a detailed result. Final pages reportedly 2703–2708 conflict with draft TOC; do not copy draft metadata. |

### Required locality and approximation handoff

Stage 2 must explain both reductions in the general-covariance note's Section 8:
independent covariance blocks placed at deleted calendar positions retain the
lower spectral and off-diagonal decay promises, while leaving selected local
conditionals unchanged; block-diagonal normalization gives bounded spectrum
under those promises even if the original marginal variances have no upper
bound. These arguments qualify novelty relative to suitable class-uniform
full-calendar and bounded-spectrum results. They do not establish that prior
work proves the entire specialized bound. The global-KL-to-Fisher implication
in the FSAI priority audit, Section 5, also belongs in the comparison: a global
Gaussian KL bound confines each relative-precision eigenvalue between two
positive scalar roots. Congruence then transfers the bound to mean Fisher
information. Fixed-window spectral control may still allow total KL to grow
with horizon, so the two guarantees differ in their quantifiers and scaling.

Stage 3 must include the inherited general-covariance weighted-trace FPTAS
from `notes/research-20260912-general-covariance-memory-bound.md`, Section 6.
Its explicitly encoded rational covariance, sensitivities, PSD prior and
PSD trace weight may have input-sized packet and parameter dimensions.
Decay rate and the decay-amplitude/lower-eigenvalue ratio have fixed bounds;
rational constants (and rational metrics if used) are supplied. Selection is
of complete packets with exact cardinality, optionally with mandatory or
forbidden times. The polynomial degree depends on those fixed promises.
This is not a uniform scheme over unrestricted decay/conditioning parameters,
and does not supply a trace-inverse or multivariate log-determinant FPTAS.

## Online search log

Queries used in Stage 1 (2026-09-13): exact-title searches for *Measure This, Not
That* plus 108786; *Sensor Selection for Estimation with Correlated Measurement
Noise* plus 2016; *New Refinement of the Operator Kantorovich Inequality* plus 2019;
*Convexification of multi-period quadratic programs with indicators* plus 2026;
exact DOI/title queries for Pázman et al. and its page range; publisher-hosted
Kantorovich article query. Opened primary arXiv 2504.17651, Project Euclid EJS2071,
and MDPI 7/2/139. Bibliography and theorem attributions rely on the primary
sources listed above, not search snippets from ResearchGate or aggregators.

Stage 1 makes no positive first-publication claim. The developing paper's candidate
contributions must be confined to precisely compared local-history guarantees
and their explicit constants, complete optimization/certificate integration,
and the proven specialized
separator hierarchy, with numerical comparisons and source correction clearly
separated from established mathematical components. A bounded negative search is
not proof of priority. Bibliographic inclusion alone is not full-text inspection.

## Stage 2 source inspection and attribution record (2026-09-13)

The author read `literature/AGENTS.md`; no KB package, generated index, or
historical research artifact was modified. Local primary fulltext was read for
the sections below. The thesis original was independently extracted with
`pdftotext -layout` to confirm its displayed formulas; the temporary full
extraction was removed, so the paper folder does not redistribute the source.
The manuscript's proofs use covariance algebra directly; these citations
identify prior work and are not substitutes for proof.

- **Lee, Gómez and Atamtürk (2026)**, local
  `atamturk2026-convexification-of-multi-period-quadratic`: inspected published
  model assumptions, Definition 1, principal-inverse formulation, and scalar
  reverse decomposition (PDF pp.5–7, 12–14), alongside the published primary
  HTML https://link.springer.com/article/10.1007/s10107-026-02379-5 . The
  original nonsingular transition/factor assumptions were retained when mapping
  to the factorized class. The paper gives its own continuity proof for singular
  transitions. Earlier **Wei et al.**, local `wei2023-on-the-convex-hull-of`,
  primary introduction/principal-inverse problem statement read; cited only as
  the general convexification antecedent, DOI 10.1007/s10107-023-01982-0.

- **Vecchia (1988)**, local fulltext PDF p.5, Eqs.11–12 and Section3.1 read:
  predecessor conditionals, actual local regression variances, nugget and
  ordering. This source was already user-supplied on Sep13; no missing-source
  qualification is retained. **Katzfuss–Guinness (2021)**, primary
  https://arxiv.org/html/1708.06302v5 Section2.1–2.3 read online: arbitrary
  selected noisy block vectors and general latent/observed conditionals.
  Primary final metadata https://doi.org/10.1214/19-STS755 confirms
  Statistical Science 36(1):124–141. This directly defeats any first-subset or
  first-block construction claim. **Pan et al. (2025)**, original published
  author PDF https://marcgenton.github.io/2025.PAGS.Technometrics.pdf pp.1–4
  inspected: block multivariate conditionals, clustering and GPU computation.
  First page confirms authors, Technometrics 67(3):546–558 and DOI
  10.1080/00401706.2025.2475784. Cited for established block computation only.

- **Schäfer–Katzfuss–Owhadi (2021)**, local fulltext Theorem2.1, Section3.3.2/
  Theorem3.4 and Section4.1 (PDF pp.4–5, 8–12) read. The primary arXiv record
  https://arxiv.org/abs/2004.14455 checked online. Fixed-pattern KL optimality,
  Green's-function/geometric hypotheses, log(n/epsilon) radius and separate
  noisy latent/incomplete-factor construction are distinguished. No categorical
  claim that KL fails to control mean Fisher is made.

- **Huan et al. (2025)**, local primary introduction, Section3 and Section7.1
  read: exact FSAI/Vecchia/Kaporin historical identification, conditional
  variance/ALC interpretation, and directed-inference neighborhood selection.
  Cited as direct approximation and experimental-design antecedent, DOI
  10.1137/23M1606253. No claim of new conditional selection is made.

- **Kozdoba et al. (2019)**, local Theorems1–2 and proof context (PDF pp.6–11)
  read. The process-noise/covariance-norm mechanism and limiting/burn-in
  assumptions were checked; online primary arXiv 1809.05870 and publisher
  https://ojs.aaai.org/index.php/AAAI/article/view/4307 checked, the latter
  confirms AAAI 33(1):4098–4105. The manuscript proves a separate finite-horizon
  time-varying local-history transport using direct covariance inequalities.

- **Benzi–Tůma (2000)**, local original first-page metadata and Theorem4.1
  (PDF pp.1,7–8) read: normalized SPD band matrix and inverse-Cholesky decay.
  Bibliography confirms SIAM JSC 21(5):1851–1868, DOI
  10.1137/S1064827598339372. **Krishtal–Strohmer–Wertz (2015)**, local
  Definition2.3/Theorem2.4 and Corollary5.1/proof (preprint pp.4–5,12)
  inspected: admissible inverse-closed decay algebras and Cholesky inheritance.
  The fixed exponential weight fails the required GRS condition, so no identical
  exponential rate is inferred. **Rubensson et al. (2021)**, published local
  Theorem5.6 and its hypotheses/proof (PDF pp.18–20, printed746–748) read:
  decay of both covariance and initial inverse factors plus uniformly bounded
  conditioning; the factor is not identified with a local Vecchia factor.
  The manuscript proves explicit local regression estimates instead and excludes
  the historical unproved direct-sum factorization-inheritance route.

- **Meyer–McMurry–Politis (2015)**, local fulltext assumptions and
  Theorem2.1 (PDF pp.3–8) inspected: stationary triangular arrays, finite past,
  spectral lower bound and weighted coefficient tails. **Inoue–Kasahara–
  Pourahmadi (2018)**, primary introduction and Theorem6.9/Corollary6.10
  (PDF pp.1–3,29) inspected: multivariate common-order FARIMA finite-predictor
  inequalities. These are credited as finite-predictor prior; the manuscript
  does not claim a new general localization principle.

- **Pagendam–Pollett (2010)**, local Section2 (PDF pp.2–4), log likelihood
  and Fisher-information expressions read. The paper uses this as an explicit
  non-Gaussian Markov sampling predecessor. Appendix `app:markov-scope` gives
  a full score-orthogonality proof and Gaussian mean/covariance derivative
  calculation with explicit regularity conditions. It does not claim those
  established identities new or transfer them to noisy finite-memory covariance
  parameters without a proof.

- **Kaminetz thesis (2025)**, original PDF printed pp.12–14 independently
  extracted and read, including Eqs.4.8–4.10, displayed objective scaling,
  pivot convention and exponential bound. The manuscript independently gives
  exact regression precisions, determinant ratios and the failed marginal
  identity for the 3-by-3 witness. Fixed-order-only final-bound contradiction
  remains distinct from the convention-independent supermodularity failure.
  **Kaminetz–Webber (2026)**, local Definition1.1, Theorem2.4 and Theorem3.1
  scope inspected with source note and primary https://arxiv.org/abs/2603.05709
  checked online (only v1, submitted 5 March2026, at access). The full-rank
  Kaporin normalization used is mean-eigenvalue raised to full dimension divided
  by determinant. The March2026 paper makes no thesis supermodularity claim;
  neither the thesis issue nor repeated-pair metric example is presented as its
  counterexample.

Stage2 online searches were exact-title/author metadata checks for Kozdoba's
page range, Katzfuss–Guinness's general framework, and Pan's block Vecchia
paper, plus the primary page openings above. The bibliography uses primary
metadata and contains no copied repository-note citation. The two priority
reductions requested at the Stage1 handoff are now proved in
`subsec:locality-prior`; the KL-to-relative-information implication is proved
in `app:locality-metrics`. No unqualified first-publication assertion is made.

## Stage 3 author source inspection (2026-09-13)

The author read the actual primary text portions below, alongside the repository
notes. Existing KB packages were not modified. Downloaded open PDFs used for
reading are temporary under `/tmp/correlated-stage03-sources`; no third-party
PDF is required or redistributed in the deliverable. Literature access status
is recorded precisely; abstracts and missing files are not full-text exclusions.

- Mahalanabis–Stefankovic, arXiv:1209.5991: local original PDF, exact pdftotext
  extraction of pp.14–17, Definition 18/Eqs37–43; local fulltext Section3.2,
  Observation33, Lemmas41–42 and Theorem43 pp.37–38. The private-principal-block
  inverse in Eq39 differs from the intended covariance block. Our singleton
  target bag avoids any positive cost in that form. Focused weights/candidate
  restrictions are transparent proof adaptations, not literal theorem wording.
- Berstein et al., primary Optimization Online author report
  https://optimization-online.org/wp-content/uploads/2007/07/1725.pdf:
  Theorem1.3; Section4 Proposition4.2/Lemmas4.3–4.4, printed pp.14–18, and
  deletion self-reduction. Cauchy–Binet squared coefficients/interpolation
  are established. Rational PSD normalization supplies bounded weights and
  singular-range coverage, not a new exact profile detector.
- Brown–Laddha–Singh2024, final NSF-hosted publisher PDF
  https://par.nsf.gov/servlets/purl/10548928: initial browser retrieval timed
  out, direct open HTTP download succeeded (266314 bytes). Theorem3 p.2 and
  guessed normalization/filter/forced-subset arguments pp.3–5 read. Broader
  independence-oracle matroid model and randomized accuracy-dependent exponent
  distinguished from this paper's deterministic rational representation.
- Papadimitriou–Yannakakis2000 author-hosted conference PDF and
  Tsaggouris–Zaroliagis author publisher PDF
  https://www.ceid.upatras.gr/webpages/faculty/zaro/pub/jou/J28-TOCS-mosp.pdf:
  approximate Pareto construction, nonnegative path costs, nonlinear monotonicity
  and growth conditions inspected. Mittal–Schulz2013 local primary fulltext
  Definitions2.1–2.2/Theorems2.3–2.4 and Section3 pp.4–6 inspected. These are
  the profile/Pareto antecedents, not direct signed-entry PSD guarantees.
- Filova, **Pal Somogyi**, Harman: primary full preprint
  https://arxiv.org/html/2507.04713v1, Sections3–4 Eq4 and Theorem1 read.
  General PSD multiresponse atoms and tied rank-one conversion already known.
  Final Wiley primary metadata verifies 2026,42(2),e70072,
  DOI10.1002/asmb.70072; no claim that final theorem numbering was checked.
- Mohar2001 author PDF, Theorem4.1(a), printed pp.10–11, and primary publisher
  metadata https://www.sciencedirect.com/science/article/pii/S0095895600920264:
  cubic Independent Set NP-hardness; DOI10.1006/jctb.2000.2026,
  JCTB82(1)102–117. The covariance/gap reduction is proved in our text.
- Liberty–Sviridenko2017 local fulltext Section5 Lemmas14–15 and Theorem5
  pp.3–7: arbitrary-accuracy multiple-regression guarantee enlarges support.
  No exact-k conclusion attributed to it.
- Vitus et al.2012 full author PDF
  https://engineering.purdue.edu/~jianghai/Publication/Automatica2012_sensor.pdf,
  Sections2/5 and Theorem6; Atanasov et al.2014 full author PDF
  https://www.georgejpappas.org/wp-content/uploads/2024/04/0528.pdf,
  SectionIV redundancy definitions/Theorem3: additive trajectory covariance/cost
  guarantees under process-noise assumptions, not the all-target relative cover.
- Alriksson–Rantzer2005 authorized thesis reprint local fulltext, printed
  pp.137–148 (PDF marker pp.139–150), especially Procedure2 at marker p.143:
  existence of a direction tests a quadratic lower envelope. The KB summary's
  simple pairwise-domination gloss is incomplete; manuscript follows actual
  procedure and retains explicit quantifier counterexample. Lincoln–Rantzer2006
  local fulltext SectionsII–III and Theorems1–3: multiplicative Bellman slack and
  quadratic representations already established.
- Indyk et al., arXiv:1807.11648v2 primary PDF: introduction,
  Proposition6.2/Section6.2 (printed pp.21ff), explicitly objective-independent
  fractional budgeted core-set and subsequent criterion rounding.
  Mahabadi–Vuong2026 PMLR300 primary full PDF downloaded from publisher-linked
  GitHub assets (415133 bytes), Theorem26 and AppendixC/Theorems33–36: spectral
  peeling gives distributions over retained vectors, then design rounding.
  These are antecedents with different feasible objects/accuracy guarantees.
- Onn–Rothblum2004 local fulltext introduction and Theorem2.6 pp.4–6:
  projected vertices for convex maximization; the manuscript provides a small
  exact interior-profile witness against substitution for D/E.
- De Loera et al.2008 local primary fulltext Theorem1 pp.2–3:
  fixed total decision dimension; fixed matrix/profile dimension does not imply
  that assumption. Bokler–Chimani–Jasper2026 local primary fulltext Definition3
  and Theorem6 pp.4–7: positive rational objectives and a relaxed-dual-restriction
  oracle; no automatic PSD-order oracle is supplied.

Onn2010 Chapter6 and Radovilsky et al.2006 were not available in full text
in this author stage; root's further retrieval attempts also failed. Neither
is used for a negative theorem claim. The contribution claim is qualified to
specific results and assumptions, and never infers priority from a missing
source or search absence. Stage3 resolves all theorem/proof obligations using
standalone derivations regardless of the qualified priority assessment.
- Berstein–Lee–Onn–Weismantel, arXiv:0807.3907 primary PDF Section3,
  Theorem4 and the element-indeterminate/random-substitution argument inspected
  during author final audit. Published2010 DOI10.1007/s10107-010-0358-6 is a
  separate randomized intersection result; the new appendix retains exact
  mixed-determinant cancellation, finite-field and unattainable-profile
  witnesses and the limitation of the older fixed-distinct-weight oracle route.
