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
