# Primary-literature review and novelty boundary

Initially reconciled on 2026-09-13 and integrated with additional primary sources on 2026-09-14 for the completed manuscript. Local literature instructions were read; no literature database packages, generated index, or generated bibliography were changed. The paper bibliography is a selected copy plus manually verified primary-source records. Local user-supplied PDFs are citation material and will not be redistributed.

## Review method

Searches included exact-title and concept searches for `Computing optimality certificates convex`, `convex mixed-integer certificates rational verification`, `convex MINLP verified cuts certificate`, `VIPR formally verified`, `formal nonlinear optimization`, and `outer approximation conic certificates`. The closest source's reference discussion was followed to Baes et al., Basu et al., and VIPR. CvxLean's related-work section was followed to formal nonlinear inequality and global-optimization work. Current primary pages were checked for VIPR, Magron et al., Wood et al., and MINLPLib. This is a focused novelty search, not evidence that no unpublished or differently indexed system exists.

## Direct comparisons

| Primary work and checked location | Established result relevant here | Boundary on this paper |
|---|---|---|
| Baes, Oertel, Weismantel (2016), `[[baes2016-duality-for-mixed-integer-convex]] p.3-8` | Mixed-integer convex certificates using subgradients and integer-free polyhedra; constrained version under mixed-integer Slater | Neither finite convex-MINLP certificates nor generalized KKT/duality is new here. Our lower-bound soundness does not need Slater, but it does not prove complete optimality certification. |
| Basu et al. (2017), `[[basu2017-optimality-certificates-for-convex-minimization]] p.2-4` | Strong optimality certificates bounded by Helly numbers under substantive attainment/interiority conditions | No smaller certificate-size or general existence claim is supported here. |
| Halbig et al. (2024), `[[halbig2024-computing-optimality-certificates-for-convex]] p.3-8`, `p.16-18`, `p.31-35` | Constructive generalized convex-MINLP certificates, reduction, verification, and computational study | Closest prior work; must appear prominently. Algorithm 3 checks each plane through a continuous convex solve; integer-freeness requires a MILP solve. The proposed distinction is replay of rigorous local nonlinear evidence plus a discrete proof, not first certificate format or independent verifier. |
| Duran and Grossmann (1986), `[[duran1986-an-outer-approximation-algorithm-for]] p.1-7` | Convex MINLP solved by nonlinear subproblems and supporting-hyperplane MILP masters | Outer approximation and bound transfer are classical. |
| Coey, Lubin, Vielma (2020), `[[coey2020-outer-approximation-with-conic-certificates]] p.3-8`, `p.15-16` | Conic dual certificates generate OA cuts; scaling accounts for MILP feasibility tolerances | Certificate-based decomposition and tolerance safeguards already exist; our contribution must specify exact expression/cut/proof replay. |
| Neumaier and Shcherbina (2004), `[[neumaier2004-safe-bounds-in-linear-and]] p.1`, `p.12` | Directed rounding and interval methods for safe MILP bounds and cuts; choose heuristically then repeat derivation rigorously | Safe rounding and untrusted heuristic proposals are established principles. |
| Eifler and Gleixner (2024), `[[eifler2024-safe-and-verified-gomory-mixed]] p.14-20` | Safe rational GMI cuts, encoding control, and VIPR derivations | Rational-cut safety and MILP certification are inherited infrastructure. |
| Borst, Eifler, Gleixner (2024), `[[borst2024-certified-constraint-propagation-and-dual]] p.3-8` | Certified linear propagation and dual proof analysis | Rational bound propagation is not a new standalone contribution. |
| Cheung, Gleixner, Steffy (2017), [primary report](https://optimization-online.org/wp-content/uploads/2016/11/5740.pdf), report printed p.1 and introduction | VIPR proof format and independent rational MILP checking | This paper extends the input-justification layer; it does not originate discrete proof replay. |
| Wood et al. (2026), [journal record](https://doi.org/10.1016/j.jsc.2025.102543), [open manuscript v4](https://arxiv.org/html/2312.10420v4), Sections 3 and 4.2 | Why3 proves the logical encoding; the implementation translates it to SMT. | Updated citation: Journal of Symbolic Computation 135, article 102543 (2026). The logical theorem does not automatically verify the C++ implementation. |
| CakeML project, [pinned README](https://raw.githubusercontent.com/CakeML/cakeml/8a32c2e8a6a3cfc7495ed13c8de9865df0c15510/examples/vipr/README.md), [program proof](https://raw.githubusercontent.com/CakeML/cakeml/8a32c2e8a6a3cfc7495ed13c8de9865df0c15510/examples/vipr/viprProgScript.sml) | Pure VIPR checker, translation into a CakeML program, and file/stdin semantics theorems. | Executable VIPR verification predates this implementation. No build or artifact compatibility assessment is claimed. |
| Szeider (2026), [primary CP paper record](https://doi.org/10.4230/LIPIcs.CP.2026.52), abstract and publisher metadata | Converts black-box ILP solver answers into rational VIPR derivations. | Recent adjacent discrete-proof construction; no nonlinear input interface is described in the inspected abstract. No performance comparison claimed. |
| Solovyev and Hales (2013), `[[solovyev2013-formal-verification-of-nonlinear-inequalities]] p.1`, `p.5-10` | HOL Light Taylor/interval nonlinear inequality proofs | Neither verified nonlinear interval arithmetic nor formal nonlinear bounds is new. |
| Narkawicz and Muñoz (2014), `[[narkawicz2014-a-formally-verified-generic-branching]] p.10-14` | PVS soundness of generic global-optimization branching under component contracts | Conditional formal correctness of optimization control flow is established. |
| Magron, Allamigeon, Gaubert, Werner (2015), [journal source](https://jfr.unibo.it/article/view/4319), abstract and bibliographic record | Coq-checked semialgebraic/transcendental lower bounds using quadratic approximations and SOS witnesses | Broad claims of first nonlinear lower-bound certificates or first formal optimization verification are false. Full detailed comparison beyond this verified abstract-level scope should use the open original in a later stage if needed. |
| Bentkamp, Fernández Mir, Avigad (2023), `[[bentkamp2023-verified-reductions-for-optimization]] p.3-8`, `p.14-15` | Lean-verified optimization reductions, with the numerical back-end solve outside formal coverage | Formalizing safe-cut/transfer theorems is distinct from verifying the Python checker or every benchmark artifact. |
| Kronqvist, Bernal, Lundell, Grossmann (2019), `[[kronqvist2019-a-review-and-comparison-of]] p.21-25`, `p.40-42` | Convex-MINLP algorithm review and controlled solver comparison | Avoid claiming a new solver class or drawing efficiency rankings from heterogeneous historical budgets. |
| MINLPLib [official page](https://www.minlplib.org/), accessed 2026-09-13 | GAMS scalar is the primary format; conversions and reported bound records have defined limitations | Pyomo interpretation is not automatically identical to GAMS input; library recorded bounds are not independently checked primal certificates. |

The source locators above use the repository's actual fulltext page markers. For Halbig et al., the locally stored accepted manuscript has a cover sheet, so these are artifact pages, not the final journal's page numbers. The current author rendered and visually inspected `original.pdf` page 18 (printed page 17): Algorithm 3 removes integrality, adds the certificate-plane halfspace, and solves the continuous problem; Section 4.3 separately invokes linear (M)IP (7). The temporary image was removed to avoid adding literature reproductions to the paper bundle. The Stage 1 paper does not reproduce such missing equations or numerical prior-work performance tables.

## Current refresh and contribution wording

Current queries were `"Computing optimality certificates" Halbig verification Algorithm 3`, `"Satisfiability Modulo Theories for Verifying MILP Certificates" 2026`, `"Formalisation of VIPR in CakeML"`, and `"convex MINLP" "proof" certificate rational verification`. The closest original and publisher record were checked again, and the Wood journal publication and Szeider CP 2026 paper were newly identified. This remains a focused review rather than proof of absence of competing systems.

The manuscript describes the implemented combination directly: exact loaded-tree semantics, conservative rational underestimators on bounded/one-sided/free coordinates, checked master identity, complete rational proof replay in a restricted subset of VIPR, and measured reliability. It omits the former qualified priority sentence because a concrete contribution description is better supported than a priority claim. Elementary support inequalities, propagation, and feasible-set inclusion are explanatory results. Section 5 and formal/COVERAGE.md identify the actual Lean theorems, their premises, and executable exclusions.

The empirical contribution has complementary parts: the frozen uniform
protocol yields 203 accepted artifacts among all 289 attempts in separate
replay, while historical replay accepts 188 with 92 rejections and nine missing
artifacts. Exact local audits distinguish invalid submitted inferences and
infeasible returned points from sufficient cut/curvature failures. Section 6
presents capability, failure mechanisms, and costs in that order; Appendix B
retains the protocols and separately versioned repair accounting. This is
software evidence, not a theorem for every execution or a comparative claim
against the prior certificate methods above.

## Adjacent software and search limits

The earlier `discopt` inspection covered documentation and reformulation/LP certificate components at commit `66d341df0ab8da383f97207f9f3f4145d9789b4b`; see `notes/certified-minlp-literature-audit.md` for the primary URLs. Its documented interval curvature and safe bounds are adjacent. Limited inspection does not prove absence of another replay interface elsewhere in that project; the paper makes no claim about such absence or project correctness.

A fresh GitHub API query for CakeML VIPR path history returned commit `c58a1b9184ca08819e7eeba61be4fd9fd1088228`, dated 2026-08-05 (merge). The paper cites the earlier immutable tree actually inspected, not an audit of the newest build. Corporate project attribution avoids assigning incomplete individual software credits.

## Claims excluded by the evidence

- First convex MINLP certificate, its computation, or independent verification of convex MINLP optimality.
- First formally verified MILP/nonlinear checking, safe cuts, or directed rounding.
- Complete solution of all convex MINLPs, universal curvature recognition, polynomial proof size, or finite termination in general.
- No trusted software or end-to-end Lean verification of the executable and artifacts.
- 269 current certified instances or optimality from reference-objective proximity.
- Performance superiority over prior certificate methods or solvers from historical heterogeneous budgets.

## Integrated comparison

Sections 3–4 state the admitted VIPR rules in relation to Cheung and Wood; Section 5 distinguishes the actual formal coverage from CvxLean and CakeML. No inspected source invalidates the scoped integration/reliability contribution or justifies a broad priority claim.


## Stage 2 monomial attribution check

On 2026-09-13, independently retrieved Lundell and Westerlund, *Convex
underestimation strategies for signomial functions*, Optimization Methods &
Software 24(4–5), 505–522 (2009), DOI
[10.1080/10556780802702278](https://doi.org/10.1080/10556780802702278), from the
[author-hosted published PDF](https://users.abo.fi/twesterl/some-selected-papers/26.%20OMS-AL-TW-2009.pdf).
The web-tool fetch timed out; direct HTTPS retrieval succeeded. The first page
confirms the publication metadata. Read the extracted text and rendered and
visually inspected printed page 507 (PDF page 3), Theorems 2.1–2.2. The first
gives convexity of a positive monomial for all nonpositive exponents, or one
positive exponent with negative remaining exponents and total at least one.
Zero exponents can be omitted. The second gives convexity of a negative
monomial for nonnegative exponents totaling at most one, hence concavity of
the corresponding positive monomial. The surrounding text attributes these
conditions to earlier work. Section 4 cites this published statement, retains
its direct Hessian proof, and makes no first-discovery claim. The downloaded
original and page image were used only as temporary research inputs, not added
to the distributable supplement or the local literature database.


## Added rigorous-bounding precedents (Stage 5)

The coordinator's primary-source followup was independently checked before
integration. Publisher-deposited Crossref metadata for all four works is saved
in `process/stage05-literature-metadata.json`. Direct source locators:

| Source | Verified material | Consequence for the manuscript |
|---|---|---|
| Jansson (2004), Journal of Global Optimization 28(1), 121–137, [DOI](https://doi.org/10.1023/B:JOGO.0000006720.68398.8c) | TUHH institutional bibliographic/abstract record and publisher-deposited metadata; no assertion of reading unavailable full text | Attribute rigorous convex lower bounds as established; no novelty for rigorous nonlinear bounding. |
| Jansson (2009), Japan Journal of Industrial and Applied Mathematics 26(2–3), 337–363, [DOI](https://doi.org/10.1007/BF03186539) | [Full author manuscript](https://www.tuhh.de/ti3/paper/jansson/ConvexPshort081117.pdf), introduction and convex/conic relaxation context; institutional and Crossref metadata | Verified convex/conic bounds have existing global and combinatorial uses. |
| Messine and Trombettoni (2019), AIP Conference Proceedings 2070, 020050, [DOI](https://doi.org/10.1063/1.5090017) | [Four-page author workshop version](https://www.lirmm.fr/~trombetton/publis/reliableconvexrelaxation_gow_2018.pdf), Theorems 1–2; final 2019 record from Crossref | Finite-box correction is support minimization applied to the affine residual, not a new general bounding principle. |
| Elloumi, Lambert, Neveu and Trombettoni (2025), Journal of Global Optimization 91(2), 331–353, [DOI](https://doi.org/10.1007/s10898-024-01370-8) | [Author manuscript](https://hal.science/hal-04016716v2/document), Section 5; final issue metadata checked against Crossref | QIBEX-R describes interval branch-and-bound with curvature correction and rigorous convex-relaxation bounds. Comparison is to its reported method, not independent validation of all proofs/software or evidence of absent export features. Use 2025 issue year despite 2024 online publication. |

Baes et al.'s local full text, Theorems 1 and 3, was checked again: the bound is
on the **number of certificate points**, at most 2 to the integer dimension
under the respective assumptions. It is not a bit-complexity bound on real
certificate data. Section 1 now states that distinction explicitly.

The Lean/mathlib references added during Stage 3 cite the theorem prover and
library directly. That earlier formalization mechanized rational coordinate
enclosures and their sum, semantic bound/cutoff transfer, and primal completion.
The extension completed on 2026-09-17 covers all 49 mathematical obligations,
including propagation, curvature, typed discrete checking, and master matching;
the current [coverage map](../formal/COVERAGE.md) records its precise scope.
Neither development originates verified optimization or verifies this Python
artifact checker.

The final experimental contribution comprises frozen historical replay
188/92/9, primary replay 203/19/67, the separately versioned twelve-case
producer repair and two-proof reporting repair, and a matching-model catalogue
with 222 entries from 405 accepted records. These empirical findings supplement
the certificate-interface contribution; none proves universal soundness of
the executable or comparative solver superiority.
