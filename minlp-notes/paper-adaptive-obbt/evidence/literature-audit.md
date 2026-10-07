# Literature and novelty audit: adaptive and iterated OBBT

**Final bounded audit, 2026-10-05.** This review checked the manuscript's cited
sources and the exact antecedents named in its theorem claims. It is a
source-based novelty assessment, not a publication-priority clearance. Three
claim-driven discovery rounds were completed; round three yielded no new
citation-worthy source under the recorded scope. Three sequential
identified-source batches then checked remaining named sources and version
records. The full run record, including round artifacts and retrieval gaps, is
in [`literature/runs/2026-10-05-adaptive-obbt-literature-audit/run.md`](../../literature/runs/2026-10-05-adaptive-obbt-literature-audit/run.md).

## Contribution boundary

Prior work already establishes repeated domain reduction, incumbent-cutoff
OBBT, selective and learned tightening, fixed-point and limit-box arguments,
generic McCormick convergence orders, recursive factor composition rules,
and examples where repeated reduction stalls. The paper should make no
priority claim for any of those general ideas.

The supported contribution is more specific: for the stated rebuilt
relaxation family, the paper gives an explicit second-order tangent model
indexed by box shape and position, the induced homogeneous box-to-box OBBT
map, and sufficient local contraction and stall tests. The quadratic examples
give exact model-specific rates and conditions. The composite result concerns
the ordinary clipped McCormick construction; it computes a shape- and
position-dependent second-order coefficient. This distinction leaves the
recursive composition and convergence-order rules credited to earlier work.
The scalar threshold is connected to the established cluster-prefactor
thresholds of Wechsung–Schaber–Barton and Kannan–Barton, rather than presented
as a new general threshold.

The finite-pool result is an OBBT-specific certificate: the retained points
must be feasible in the relaxation rebuilt on their own hull. Compact support
attainment gives at most `2n` face witnesses for a box; after the rebuilt
feasibility and hull check, monotonicity protects that box under later rounds
at the stated cutoff. This is distinct from filtering witnesses in the
current relaxation, which certifies only a frozen round. The sharp finite-pool
cutoff threshold and the full-relaxation face threshold follow from face
coverage and attained support values; present them as exact formulas, not new
polyhedral principles. The residual, LP-sensitivity, and feasible-repair
results likewise use established contraction, parametric LP, and error-bound
tools under explicit OBBT-specific validity regions and constants.

## Disposition of every approved bibliography key

The approved supplement contains 37 entries, all now cited in the manuscript.
“Full text” below means source text was consulted; “metadata/abstract” means
the claim must remain at that level. The corrected and additional records are
in [`literature-references.bib`](literature-references.bib); the generated KB
bibliography was not edited.

| Key | Source basis and disposition |
|---|---|
| `applegate2007-exact-solutions-to-linear-programming` | Full source read, [[applegate2007-exact-solutions-to-linear-programming]]: exact LP solution and certification context for the numerical validation. It does not make the paper's outward-rounding implementation a new exact-LP method. |
| `badilla2024tradeoffs` | arXiv v2 text read: OBBT cost/quality tradeoffs in ReLU verification. Application-specific evidence; it does not establish the local-rate results. |
| `belotti2010-feasibility-based-bounds-tightening-via-fixed-points` | Published-chapter metadata verified; chapter text unavailable. Cite jointly with the read 2012 manuscript `belotti2012fbbt` for the FBBT fixed-point and linear-LP statements; the 2010 entry is a published-version record, not an independently checked text. |
| `belotti2012fbbt` | Full author manuscript read, [[belotti2012-on-feasibility-based-bounds-tightening]]: monotone feasibility propagation, greatest fixed point, possibly infinite iteration, and an LP characterization for linear constraints. This is FBBT, not incumbent-cutoff OBBT. |
| `bompadre2012-convergence-rate-of-mccormick-relaxations` | Metadata, abstract, and limited theorem-level excerpts checked; KB package remains `access: none`, `status: unread`. Credit generic pointwise/Hausdorff convergence-order analysis under its hypotheses only. Do not make detailed negative claims about its coefficient recursion or use it to assert priority. |
| `borrelli2003parametric` | Full author-hosted source read: critical regions for multiparametric LP support the basis-region attribution. |
| `caprara2010-global-optimization-problems-and-domain` | Full source read, [[caprara2010-global-optimization-problems-and-domain]] pp. 4–9, 13–14: iterated domain-reduction limits and order independence. It is direct prior art for limit behavior, not the manuscript's local tangent map. |
| `caprara2016-theoretical-and-computational-results-about` | Full source read, [[caprara2016-theoretical-and-computational-results-about]] pp. 2–11: a lower-limit result for optimality-based reductions, a result for a restricted class, and stall counterexamples. Stalling itself is not new; the manuscript's row and face criteria are tied to its specified termwise McCormick construction. |
| `cengil2025learning` | Published source text read: learned variable selection for tightening AC-OPF relaxations. Supports the statement that learned direction selection is established; it is not a repeated-map rate analysis. |
| `chmiela2023scheduling` | Full arXiv v1 text read; published CPAIOR 2023 metadata and DOI verified. Supports online scheduling of MIP heuristics, not an OBBT novelty claim. The BibTeX entry uses the published proceedings record and notes the consulted preprint. |
| `coramin2023filters` | Pinned software source read: feasible-point and aggregate-objective filtering in the current relaxation. This is a frozen-round screening precedent, not a rebuilt-hull persistence check. |
| `gleixner2017-three-enhancements-for-optimization-based` | Full source read, pp. 1–3, 9–11: direction filtering, auxiliary-LP ordering/warm starts, and dual-derived reusable variable bounds. The manuscript correctly credits current-round screening and dual reuse. |
| `gomezcasares2025domain` | arXiv v2 source text read: per-instance selection among domain-reduction configurations in polynomial optimization. It establishes learned configuration selection. |
| `gonzalezdiaz2025lifted` | arXiv v1 source text read: lifted-variable bounds can help or hurt end-to-end solver performance. Supports the cost/performance caveat, not a rate theorem. |
| `hay2012computations` | Full UAI source read: value-of-computation and stopping in a probabilistic decision model. It supplies decision-theoretic context, not OBBT-specific guarantees. |
| `hendel2018adaptive` | Full 2018 manuscript source read; publication metadata checked against the 2019 proceedings chapter (pp. 513–519, DOI `10.1007/978-3-030-18500-8_64`). The legacy key retains “2018,” while the supplement gives the published year and venue. Credit adaptive bandit control of solver components. |
| `hoffman1952-on-approximate-solutions-of-systems` | Original source read, [[hoffman1952-on-approximate-solutions-of-systems]]: classical linear-inequality error bound. The manuscript uses it as a tool, not as a new theorem. |
| `jachymski2016perov` | Full source read: vector-valued contraction framework. The manuscript's positive-eigenvector comparison is elementary; it does not need or claim a nonlinear Perron–Frobenius theorem. |
| `kannan2017-the-cluster-problem-in-constrained` | Full source read, pp. 13–22, 34–41: constrained cluster analysis and scalar prefactor threshold. Credit the matching numerical threshold; do not identify the manuscript's shape map with their scalar worst-case prefactor. |
| `mccormick1976-computability-of-global-solutions-to` | Original source read: factorable convex/concave relaxations and bilinear envelopes. Foundational attribution only. |
| `mitsos2009-mccormick-based-relaxations-of-algorithms` | Full source read: product and univariate-composition rules for McCormick relaxations. Credit these recursive construction rules. |
| `najman2016-convergence-analysis-of-multivariate-mccormick-relaxations` | Direct journal text not retrieved; metadata and abstract checked. Relevant generic order results are also restated in the officially hosted 2020 thesis, Chapter 3, viewed through the public record. Keep attribution at the generic convergence-order level; do not assert detailed comparison to inaccessible article contents. |
| `neumaier2004-safe-bounds-in-linear-and` | Full source read, [[neumaier2004-safe-bounds-in-linear-and]]: safe lower bounds for LP/MILP over bounded domains. It supports the established safe-bound foundation, not a new rounding principle. |
| `pineda2025sweetspot` | arXiv v1 source text read: topology-optimization tightening-subproblem tradeoffs. Application context only. |
| `robinson1973-bounds-for-error-in-the-solution-set` | Metadata and abstract checked; KB package remains `access: none`, `status: unread`. Use only for the broad classical error-bound attribution in the related-work text; no manuscript constant or theorem depends on a detailed reading of Robinson's result. |
| `ryoo1995-global-optimization-of-nonconvex-nlps` | Full source read: marginal-based range reduction and stopping/cap mechanisms. The scalar OBBT comparison is an adaptation of established range-reduction logic, not a general new principle. |
| `scip1002tree` | Pinned official SCIP 10.0.2 `src/scip/tree.c` source read. The archived records contain node number zero, not an explicit probing flag; the probing interpretation is inferred from source behavior. Keep the manuscript's safer phrase “number-zero callbacks.” |
| `scip2026obbt` | Pinned SCIP source/documentation for the current OBBT implementation read: root-focused OBBT, work budget, stored dual bounds, and reevaluation after incumbent change. Cite for this version's behavior only. |
| `scott2011-generalized-mccormick-relaxations` | Full source read, pp. 3–13. Definition 9 Step 6 gives clipping; Remark 2 discusses omission; Theorem 4 proves partition monotonicity under the stated nested-interval, scalar-domain, and Lipschitz assumptions. Do not generalize it to unclipped or solver-strengthened relaxations. |
| `tarski1955fixpoint` | Original source read; DOI verified. The greatest-fixed-point attribution is a standard consequence of monotonicity, not a contribution claim. |
| `walker2011anderson` | Full source read: Anderson acceleration proposes iterates/candidates; validity must be checked by the OBBT operator or a certificate. |
| `wechsung2014-the-cluster-problem-revisited` | Full source read, pp. 5, 8–9: scalar second-order prefactor and cluster-size threshold. Credit the shared threshold and distinguish the shape-dependent tangent map. |
| `coffrin2015-strengthening-convex-relaxations-with-bound` | Full chapter source read, [[coffrin2015-strengthening-convex-relaxations-with-bound]] pp. 10–12: repeated feasibility-based bound consistency strengthens power-network convex relaxations. It is an application precedent for iterated rebuilding/tightening, not incumbent-cutoff OBBT. |
| `bompadre2013-convergence-analysis-of-taylor-models` | Journal metadata verified; local author-upload retrieval failed (HTTP 403), package remains unread. A prior September review records reading an author version, §§1–2 and Appendix A; this final audit does not rely on that unavailable copy for a negative claim. Credit the abstract-supported convergence-order rules for Taylor and McCormick–Taylor arithmetic/composition. Recursive order propagation itself is established. |
| `nagarajan2019-an-adaptive-multivariate-partitioning-algorithm` | Full source read, [[nagarajan2019-an-adaptive-multivariate-partitioning-algorithm]]: adaptive multivariate partitioning includes sequential OBBT/PBT and repeats tightening to a bound-change tolerance. Generic repeated OBBT is therefore prior art; the paper's comparison is limited to rates and certificates for its specified rebuilt map. |
| `puranik2017-domain-reduction-techniques-for-global` | Full survey source read, [[puranik2017-domain-reduction-techniques-for-global]]: reviews OBBT/FBBT and repeated domain-reduction practices. Use for field context, not a detailed priority claim. |
| `sundar2023-optimization-based-bound-tightening-using` | Published CDC 2023 DOI/pages verified, but that proceedings copy remains unavailable. The distinct arXiv v3 preprint, [[sundar2018-optimization-based-bound-tightening-using]] pp. 13–14, was read and supports rebuilding the strengthened QC relaxation between incumbent-cutoff OBBT rounds. Attribute those details to the consulted arXiv version; do not describe the published text as independently read. |

## Claim cautions and remaining citation limits

- Do not claim that no repeated-OBBT method, incumbent cutoff, convergence-order
  analysis, scalar contraction threshold, or stall example existed. Sundar et
  al. give repeated incumbent-cutoff OBBT; Nagarajan et al. repeat sequential
  OBBT/PBT; Caprara et al. give stall examples; Bompadre–Mitsos and
  Najman–Mitsos establish generic order results; and the cluster papers give
  scalar prefactor thresholds.
- Zamora and Grossmann report observed per-round width ratios in Table 3.
  Those data are empirical, not a theorem giving this paper's local tangent
  map. The manuscript should not say that prior observed ratios do not exist.
- The full BM2012 and Najman2016 texts were not retrieved. Accordingly, do not
  make source-specific negative claims about their coefficient recursions or
  detailed theorem scope. The defensible contrast is the paper's explicit
  shape/position-dependent tangent expansion and OBBT map, qualified as a
  contribution of this manuscript rather than an absolute first.
- BM–Mitsos–Chachuat (2013) studies Taylor and McCormick–Taylor models; it is
  not the same construction as ordinary clipped composite McCormick. Its
  arithmetic/composition order rules are explicitly credited.
- The BM2012, Najman2016, Robinson1973, Jansson2004, Zamora1999, and closed
  book/report source limitations are itemized below. No result requiring an
  unverified detailed theorem from these sources should be added.
- The current direct citation to Robinson supports a general classical
  attribution only. If the final text is revised to depend on a specific
  Robinson constant or theorem, retrieve and check the full article first.

## Complete in-scope source-content access gaps

This is the deduplicated list of all in-scope materials identified in this
review whose full source artifact remains unavailable in the KB or whose
published version has not been retrieved. “Unavailable” does not imply the
work is irrelevant: the manuscript uses only the qualified claims described
above. Direct landing pages below are lawful; no access control was bypassed.

1. Bompadre and Mitsos, “Convergence Rate of McCormick Relaxations” (2012),
   DOI `10.1007/s10898-011-9685-2`,
   [Springer landing page](https://link.springer.com/article/10.1007/s10898-011-9685-2)
   and [author-upload page](https://www.researchgate.net/publication/220249483_Convergence_rate_of_McCormick_relaxations).
   The journal article is closed; the public author-page PDF attempt returned
   HTTP 403. Abstract and limited theorem text were visible, but no lawful
   full-text artifact was obtained. KB: `bompadre2012-convergence-rate-of-mccormick-relaxations`.
2. Najman and Mitsos, “Convergence Analysis of Multivariate McCormick
   Relaxations” (2016), DOI `10.1007/s10898-016-0408-6`,
   [Springer landing page](https://link.springer.com/article/10.1007/s10898-016-0408-6).
   The direct journal text is closed. Generic results were checked through
   the thesis entry below; the article itself remains unavailable. KB:
   `najman2016-convergence-analysis-of-multivariate-mccormick`.
3. Najman, “McCormick-based Efficient Global Optimization in the Space of
   Degrees of Freedom” (2020 PhD thesis), DOI `10.18154/RWTH-2020-10531`,
   [official RWTH record](https://publications.rwth-aachen.de/record/804786).
   The downloaded PDF was a 248-byte anti-bot response. Chapter 3 §§3.1–3.4
   were visible through the official browser record and support only the
   generic order rules cited above; the thesis PDF is still unavailable to
   the KB. KB: `najman2020-mccormick-based-efficient-global-optimization`.
4. Najman and Mitsos, “On Tightness and Anchoring of McCormick and Other
   Relaxations” (2019), DOI `10.1007/s10898-017-0598-6`,
   [Springer landing page](https://link.springer.com/article/10.1007/s10898-017-0598-6).
   The direct article source was not retrieved; only an adjacent thesis
   discussion was viewed. It was not used for a manuscript claim.
5. Robinson, “Bounds for Error in the Solution Set of a Perturbed Linear
   Program” (1973), DOI `10.1016/0024-3795(73)90007-4`,
   [publisher DOI page](https://doi.org/10.1016/0024-3795(73)90007-4).
   Only metadata and abstract were available. KB:
   `robinson1973-bounds-for-error-in-the`.
6. Jansson, “Rigorous Lower and Upper Bounds in Linear Programming” (2004),
   DOI `10.1137/S1052623402416839`,
   [SIAM DOI page](https://doi.org/10.1137/S1052623402416839).
   Crossref metadata and abstract were checked; no local full text was
   retrieved, and this uncited candidate is not needed because Neumaier and
   Applegate support the manuscript's numerical-validation statements. KB:
   `jansson2004-rigorous-lower-and-upper-bounds`.
7. Zamora and Grossmann, “A Branch and Contract Algorithm for Problems with
   Concave Univariate, Bilinear and Linear Fractional Terms” (1999), DOI
   `10.1023/A:1008312714792`,
   [publisher DOI page](https://doi.org/10.1023/A:1008312714792).
   A prior project report records reading pp. 226–228 and Table 3 p. 235, but
   no source file is available in this KB run. The table reports observed
   ratios only; do not turn that into a theorem or a priority contrast. KB:
   `zamora1999-a-branch-and-contract-algorithm`.
8. Locatelli and Schoen, *Global Optimization: Theory, Algorithms, and
   Applications*, Chapter 5 (2013), DOI `10.1137/1.9781611972672.ch5`,
   [SIAM chapter page](https://epubs.siam.org/doi/10.1137/1.9781611972672.ch5).
   The full book chapter is not open; only bibliographic/preview information
   was available. No manuscript claim relies on its text. KB:
   `locatelli2013-chapter-5-branch-and-bound`.
9. Caprara and Locatelli, “Global Optimization Problems and Domain Reduction
   Strategies,” Research Report OR/07/3 DEIS (2007, reported submitted to
   *Mathematical Programming*),
   [official Caprara CV](https://archiviostorico.unibo.it/it/patrimonio-documentario/ritratti-di-docenti/139595/caparara_alberto.pdf/%40%40download/file/caparara_alberto.pdf).
   The CV verifies this title, report number, year, and submission note; the
   report itself was not retrieved. An alternate 2008 Torino identity was
   not verified. The published 2010 article was read and is the claim basis.
   No DOI or stable report landing page was found.
10. Belotti, Cafieri, Lee, and Liberti, “Feasibility-Based Bounds Tightening
    via Fixed Points” (2010 published chapter), DOI
    `10.1007/978-3-642-17458-2_7`,
    [Springer chapter page](https://link.springer.com/chapter/10.1007/978-3-642-17458-2_7).
    The published chapter text was not retrieved. The related 2012 author
    manuscript was read in full and is the source-text basis for the shared
    FBBT claims. The 2010 entry is retained only as the published-version
    citation. No separate KB package was created for it.
11. Bompadre, Mitsos, and Chachuat, “Convergence Analysis of Taylor Models
    and McCormick-Taylor Models” (2013), DOI `10.1007/s10898-012-9998-9`,
    [Springer landing page](https://link.springer.com/article/10.1007/s10898-012-9998-9)
    and [author-upload page](https://www.researchgate.net/publication/257588944_Convergence_analysis_of_Taylor_models_and_McCormick-Taylor_models).
    Current full-text retrieval from the public author page returned HTTP
    403. A September project note says an author version was read (§§1–2 and
    Appendix A), but the artifact is not available for this audit. The
    manuscript uses only the generic order results stated in the abstract and
    makes no negative-content claim. KB:
    `bompadre2013-convergence-analysis-of-taylor-models`.
12. Sundar et al., “Optimization-Based Bound Tightening Using a Strengthened
    QC-Relaxation of the Optimal Power Flow Problem” (CDC 2023 published
    version), DOI `10.1109/CDC49753.2023.10384116`,
    [IEEE landing page](https://doi.org/10.1109/CDC49753.2023.10384116).
    The published proceedings text was not retrieved. The separate arXiv
    v3 (2019) source was read in full and supports the cited repeated
    incumbent-cutoff OBBT details; the manuscript/BibTeX must identify that
    version as the text consulted. KB published-version package:
    `sundar2023-optimization-based-bound-tightening-using`; consulted
    preprint: `sundar2018-optimization-based-bound-tightening-using`.
13. Ryoo and Sahinidis, “A Branch-and-Reduce Approach to Global
    Optimization” (1996), DOI
    `10.1007/BF00138689`,
    [Springer landing page](https://link.springer.com/article/10.1007/BF00138689).
    A prior project report records reading pp. 116–117, but no local full-text
    artifact is present. The manuscript cites and relies on the read 1995
    paper, not a distinct claim from this follow-up.

## Bibliography and verification record

The supplement has 37 verified entries. Corrections include published
metadata for Borrelli (DOI `10.1023/B:JOTA.0000004869.66331.5C`), Tarski (DOI
`10.2140/pjm.1955.5.285`), Hay (official UAI proceedings record), Hendel
(published 2019 chapter metadata under the established legacy key), and
Chmiela (published 2023 LNCS metadata with the consulted arXiv v1 noted).
The Sundar published 2023 record is separate from its read 2019 arXiv v3.
Neumaier (DOI `10.1007/s10107-003-0433-3`) and Applegate et al. (DOI
`10.1016/j.orl.2006.12.010`) have full source texts and verified entries.
No generated KB bibliography was changed.

Three discovery rounds were run; the third was empty, so stopping is
operational saturation under this claim-driven scope, not evidence of
completeness. Three identified-source batches checked the remaining named
works and source versions. Packages added or promoted in this audit are the
full-text Coffrin 2015 chapter and Sundar arXiv v3 preprint, plus metadata
records for Bompadre–Mitsos–Chachuat 2013 and the published Sundar 2023
proceedings version. Existing metadata packages for Bompadre–Mitsos 2012,
Najman–Mitsos 2016, Robinson 1973, Jansson 2004, Zamora–Grossmann 1999, and
the Najman thesis remain unread where identified above. The run account
records the final `lit.py check` counts and status.
