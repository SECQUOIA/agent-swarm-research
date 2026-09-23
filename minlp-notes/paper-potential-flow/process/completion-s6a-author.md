# Stage 6a author report

Status: complete author draft, frozen for the five independent reviewers. This report does not mark the stage accepted. The lead will dispatch five reviewers after this freeze, adjudicate their findings, and assign valid corrections to a different agent under `completion-plan.md`.

## Coverage and mathematical development

The new `complexity/sections/11-certified-computation.tex` supplies a standalone treatment of all proved content in the two promoted certificate results, their supporting notes, the goal-oriented note, and the integrated original-instance pipeline. It supersedes the earlier coverage map's mention-only allocation for the two promoted certificate results. No result is deferred to a companion paper. The accepted global-design energy certificate remains in Section 9 and is cross-referenced without rewriting it.

| Manuscript label | Complete content |
| --- | --- |
| `prop:a-cert-energy` | Asymmetric cubic conjugate, rational primal-dual gap, scalar uniform-convexity proof, and common rational flow radius. |
| `eq:a-cert-root` and preceding construction | Exact conservation repair by chord rounding and tree elimination; cut-error bound; polynomial rational square/cube-root upper enclosures and verification model. |
| `prop:a-cert-bregman` | Reverse-Bregman energy decomposition, strict monotonicity in the unknown state despite a zero derivative at zero, outward endpoint inequalities and polynomial-bit bisection. |
| `prop:a-cert-signs` | Per-edge sign-error residuals and original-scenario flow bound; non-strict compatibility conditions proving exact rational endpoint optimality. |
| `thm:a-cert-support` | Conserved-energy support dual for positive multipliers; exact zero-multiplier cut goals; relative-Slater completeness of rational witnesses and support convergence as the trial energy approaches optimum. |
| `thm:a-cert-hessian` | Curvature bounds on intervals containing both trial and physical flows, conservation-aware Cauchy–Schwarz estimate, exact zero-edge residual conditions, and the physical zero-gap shortcut. |
| `prop:a-cert-projection` | Exact constrained Laplacian equations, consistency iff the goal annihilates zero-curvature circulations, singular gauge/redundancy handling, rational solvability, and sharpness over the conserved quadratic error set. |
| `eq:a-cert-effective` | All-positive weighted projection formula, effective-resistance interpretation and zero bridge factor. |
| `ex:a-cert-paths` | Full two-path energy/support/Bregman/Laplacian comparison; explicit rational dual data attaining both support endpoints; pointwise asymptotic scope and distinction between interval centers. |
| `eq:a-cert-direct-loss` | Original-instance verification, independently reconstructed envelope mapping, two physical-state witnesses, valid interval intersections, direct loss subtraction, and exact endpoint interpretation. |
| `eq:a-cert-scaling` | Exact covariance of energy/root/flow witnesses and curvature goal witnesses under common rational flow and resistance unit changes. |

The prose additionally proves deterministic edge-drop, path-pressure, and zero-sum weighted-potential enclosures on arbitrary graphs, without assigning them an unsupported uncertainty-envelope interpretation. It explains graph recognition, finite-set endpoints, exact unit-Laplacian adjoint signs including zero signs, the reversed target rule, and why reusing a conserved trial flow for the selected scenario requires no second physical optimization.

The principal completion beyond the supporting notes is the sharpness proof for the constrained quadratic constant. Given optimal KKT data, set `d_P=D(w_P-A_P^T v)` and `d_Z=-xi`. The KKT equations imply `Ad=0`, `w^T d=C_*`, and `d^T H d=C_*`. Scaling this circulation attains the quadratic-set support bound. If the zero-edge equations are inconsistent, an uncontrolled zero-curvature circulation makes that abstract set's goal unbounded. This assertion concerns the quadratic error set; it does not assert sharpness for actual physical errors or for its additional Bregman interval constraints. The theorem states sharpness for positive quadratic budgets. Separately, an actual verified energy gap zero gives the exact physical state irrespective of curvature.

The exact two-path dual construction is also explicit in the manuscript, including lower as well as upper support. The interval-center distinction is stated. A rational counterexample (`29/750 > 1/50`) shows that the conserved-energy support set need not satisfy the separate-edge Bregman constraints that are proved only for the physical state.

## Boundaries retained after code inspection

The mathematical certificate scope permits disconnected loopless multigraphs with componentwise feasible nominations. The numerical conservation-repair helper is restricted to connected simple loopless graphs. The complete original-instance pipeline is restricted further to graphs with no K4 minor, fixed nominations, independent interval/finite resistance choices, and no side constraints. Parallel edges and disconnected gauges are tested for the broader exact goal certificate but are not attributed to the narrower numerical helper or pipeline.

The basic energy JSON certifies its encoded deterministic instance. It does not validate original uncertainty data. The Bregman helper requires prior base verification; the goal verifier independently repeats that verification. The strict original-instance reader reconstructs the graph, original endpoints, target, direction, envelope coefficients, and target goal; it rejects unknown fields, duplicate keys, nonstring rational fields, and Boolean indices. These strict schema claims are not transferred to the simpler base reader.

Polynomial verification and rational elimination count expanded numerator/denominator bit lengths. Exact-string scientific notation accepted by `Fraction` is not treated as a raw-JSON-length polynomial input model. The theoretical additive algorithms remain distinct from practical CVXPY/Clarabel proposals. No generic support-dual optimization producer, requested-tolerance numerical guarantee, scalable sparse exact solver, or polynomial support-certificate size guarantee is asserted. The existing exact dense Hessian producer is accurately described. A zero-curvature obstruction is never regularized away; the full pipeline can omit that optional witness and retain its valid Bregman enclosure.

No existing code validity bug was found by the author or lead. No existing implementation was edited. Numerical comparisons use verified interval widths and loss upper bounds, not actual errors. The physical state can remain irrational when a rational endpoint scenario is proved exactly optimal.

## Corpus and source inspection

Read the completion plan, coverage map and literature screen; both promoted rational/Bregman results and supporting notes; the complete goal-oriented and original-instance pipeline notes; accepted Section 5's envelope, confluence, energy modulus and recovery proofs; Section 9's global certificate and parser qualification; and the relevant main/bibliography/build conventions.

Read the actual full implementations of `envelope_rational_certificates.py`, `envelope_bregman_bounds.py`, `goal_flow_certificate.py`, `certified_envelope.py`, `certified_envelope_benchmarks.py`, and `envelope_socp_checks.py`. Also read the four independent review scripts in full: base certificate, Bregman certificate, goal certificate, and complete pipeline. The author did not spawn agents. The lead independently checked the main proofs, code and source context in parallel under the user-authorized stage process.

Primary literature checked directly:

- Boyd and Vandenberghe, *Convex Optimization* (2004): downloaded the open author PDF and inspected Sections 3.3, 5.1.6, and 5.2.3, especially the conjugate definition/Fenchel inequality and strong duality plus dual attainment under relative Slater feasibility. The existing bibliography entry is reused. [Author PDF](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf).
- Bregman, *The relaxation method of finding the common point of convex sets and its application to the solution of problems in convex programming*, *USSR Computational Mathematics and Mathematical Physics* 7(3), 200–217 (1967), DOI 10.1016/0041-5553(67)90040-7. The openly hosted original English translation is image-only. The author rendered and visually inspected printed pp. 201, 204, and 206; p. 206 equation (1.4) is precisely the divergence definition used here. Publisher/MathNet metadata distinguish the article's 1967 date from its 1966 receipt date and the host filename. [Original translation](https://www.lix.polytechnique.fr/~nielsen/Bregman1966.pdf), [publisher record](https://www.sciencedirect.com/science/article/pii/0041555367900407).
- Bartels and Milicevic, *Primal-dual gap estimators for a posteriori error analysis of nonsmooth minimization problems*, *ESAIM: M2AN* 54(5), 1635–1660 (2020), DOI 10.1051/m2an/2019074. Downloaded and read Section 3, especially Proposition 3.1 and its complete proof on printed p. 1641: a feasible primal-dual gap bounds the energy error and the supplied uniformly convex error measure. The manuscript credits this general tradition, without claiming a new a posteriori principle. [Open original and metadata](https://numdam.org/articles/10.1051/m2an/2019074/).
- Lyons and Peres, *Probability on Trees and Networks* (2016), author-hosted corrected paperback version dated 19 August 2026. Read Chapter 2 Section 4, printed pp. 33–35: energy/effective-resistance identity, weighted star/cycle orthogonality, current as projection, Pythagorean identity and Thomson's principle. Copyright pages verify first publication in 2016 and corrected paperback publication in 2021. The bibliography explicitly names the inspected 2026 corrected text. [Author text](https://rdlyons.pages.iu.edu/prbtree/book_pb.pdf).
- Vrachimis, Eliades and Polycarpou, *Real-time hydraulic interval state estimation for water transport networks: a case study*, *Drinking Water Engineering and Science* 11, 19–24 (2018), DOI 10.5194/dwes-11-19-2018. Read the official original model, Section 2, and data-availability statement: the actual law has Hazen–Williams exponent 1.852, demand measurement intervals and known external heads. [Original article](https://dwes.copernicus.org/articles/11/19/2018/). The article directly identifies [dataset DOI 10.5281/zenodo.1185136](https://doi.org/10.5281/zenodo.1185136). Fresh Zenodo browser requests failed; no access barrier was bypassed. The already downloaded original `/tmp/Vrachimis2018NetDWES.inp` was inspected, including its copyright/license header and complete node/pipe geometry sections. An exact transformation audit checks all 13 oriented edges and every rational proxy interval against the retained adaptation JSON. Its source SHA is retained. The manuscript makes the synthetic nominations, quadratic proxy, target mapping and non-hydraulic interpretation explicit.

Four primary bibliography entries were appended; the old bibliography remains an unchanged prefix. No managed literature package, index, generated bibliography, or read status was changed. The source PDFs were downloaded only under `/tmp`; their hashes are retained. Classical duality, divergence, and electrical projection are explicitly attributed. No general first-result claim or inference from an inaccessible nonlinear-tolerance paper is made.

## Verification and evidence

`verification/check_s6a_certificates.py` adds distinct exact checks in a supplied circulation basis, rather than duplicating the implementation's potential-system solve. Its two fixtures are a rank-two graph of overlapping cycles and a disconnected parallel-edge graph with a bridge and isolated vertex. Across all curvature assignments in `{0,1,2}` and three goals, 810 cases agree with the independently formed cycle Gram problem: 774 finite factors and 36 zero-curvature obstructions. In each finite case the test checks exact factor equality and a circulation attaining both `w^T d=C` and `d^T H d=C`.

The diagnostic checks 16 exact rational upper/lower support witnesses for path lengths 1, 2, 8 and 32 and two positive rational perturbations. It checks the support/Bregman counterexample and rechecks the saved six-edge certificate, every Bregman interval, and every optimal Laplacian edge bound. Every printed strict bound on that saved case is tested against its exact rational value.

The normal diagnostic additionally produces a fresh ambiguous-sign original-instance witness, verifies it both with and without optional goal bounds, and retains its complete exact payload and both reports. The verified target-width improvement is about 114.1197; the verified loss-bound improvement is about 131.0812. The selected endpoint scenario remains uncertified as exactly optimal. The optimized `-S -O` diagnostic runs all exact mathematics without site/scientific packages. Both commands passed.

Fourteen existing audit/demo/producer commands were also replayed in an isolated copy of `code/potential_flow_mpd`, so the benchmark's automatic saved-JSON writes did not modify distributed data. They cover normal and `-S -O` runs of all four independent audits and the goal demonstration; the six-case numerical energy producer; the ten-case original-instance benchmark; the optional scale producer audit; and the saved six-edge goal comparison. Every command returned zero. The manifest retains all stdout/stderr, including numerical inaccurate-solution warnings, full commands and elapsed times.

Specific replay evidence includes 800 root-minimality checks; 50 exact signed/zero-gap Bregman states, 339 malformed intervals and 60 physical residual inequalities; 9 asymmetric/zero-edge goal cases, 732 conserved sublevel samples and 161 malformed goal witnesses; 771 graph/minor comparisons, 24 exact original-instance physical fixtures, four independent closed-form loss checks, 66 malformed CLI cases and 22 malformed integrated goals. The ten-case numerical suite again obtained ten valid certificates and nine exactly optimal endpoint scenarios. Its two small cases compare against 128 endpoint scenarios combined. Unit covariance is checked under scales `10^400` and `10^-400`. These finite checks support implementation confidence and do not replace the manuscript's universal proofs.

The checks manifest records the scientific interpreter and NumPy, SciPy, NetworkX, CVXPY and Clarabel versions, all existing Python source hashes, saved JSON hashes, the new diagnostic hash, exact diagnostic outputs, benchmark rows, dataset transformation evidence, primary-PDF hashes and preservation checks.

## Build and preservation

Paper A alone was built by importing `verification/build_and_check.py` and calling `build('complexity')`. The two-paper CLI was not used. The manifest's passed condition additionally requires zero overfull boxes. The final PDF has 188 pages, compared with 172 before S6a. The final build has zero errors, undefined references, undefined citations, duplicate labels and overfull boxes. A rendered implementation/reproducibility page was visually inspected. Reading-order and appendix reorganization remain for S6b; this author did not start that stage.

All 18 final `.tex`/`.bib` inputs appear in the SHA-256 build manifest. The 17 pre-author inputs match the accepted S5c build manifest exactly. All 15 prior inputs other than `main.tex` and `references.bib` remain byte-identical. Removing the single Section 11 input line reproduces the prior main file, and the old bibliography remains an exact prefix. Every existing Python source matches its pre-edit isolated copy. No accepted section, Paper B input, research result/note, managed literature file, or existing implementation was edited. No commits were made.

The files are now frozen pending review. Exact hashes follow.

- `complexity/sections/11-certified-computation.tex`: `0730038a9098898f45ce72c4373ae64101fd1fdc74b4f6d92d8ae093ecf0f09e`

- `complexity/main.tex`: `487331965e56acee0c8c8eee3c2bd9061e0b0a81a25450ad20c2acb218a9877e`

- `complexity/references.bib`: `852c66955257391ff1b2c4720e1a61b570f0ba97782ab4e60dcae3762a6ae3f5`

- `verification/check_s6a_certificates.py`: `72d595b543c6b50247c0d7ac23540a6aebf1e0164f78f93d07f077f97822d341`

- `process/completion-s6a-build.json`: `9ce091afe60f07072f0fddba250a46318b21ac6c6b79310f191d1d09f78ac939`

- `process/completion-s6a-checks.json`: `0d21e00759ff803b4b34e453f7c50572f2b2b64a320e52ce330257e7e1cab81e`
