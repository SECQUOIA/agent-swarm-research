# Manuscript development and review record

The user requested a comprehensive LaTeX paper on physical finite reservoirs at coexistence. Each stage has one author, followed by five independent reviewers. The coordinating agent assesses every criticism. A different agent fixes all valid issues. Any major issue requires another five-reviewer round after correction. Minor issues must also be resolved before the next stage. The completed manuscript receives the same five-reviewer process.

## Sequential stages

1. **Physical framework and sharp reservoir theorems.** Exact bath law, full-state/energy TV identity, weak-support classification, unequal-scale necessity, two-phase sufficiency and its precise hypotheses. Establish the LaTeX project and notation.
2. **Microscopic realizations.** Mean-field Potts theorem and exact finite-system reduction; critically develop the short-range Potts argument, including the outstanding sufficiency question. Resolve what the source hypotheses actually prove.
3. **Shared-bath statistics.** Phase selection, full marginal and joint TV, full microscopic information, fixed-copy extension, balancing, and linear-capacity boundary.
4. **Related reservoir developments.** Exact Gaussian phase geometry and calibration crossover, smooth-bath extension, interfacial-tail/capillarity consequences, and diagnostic distinctions among full-law, histogram, and barrier accuracy. Treat model statements as such.
5. **Synthesis and complete draft.** Introduction, prior art with verified bibliography, physical interpretation, numerical evidence, coverage audit, cross-references, appendices, conclusion, and compiled PDF.
6. **Whole-manuscript review.** Five independent full readers; revise with a different agent and repeat after any major issue, until no major issue remains and all valid minor issues are fixed.

Scope: include all reservoir/coexistence developments relevant to the first proposed paper. Separate survival-conditioning, interfacial-response inverse problems, reactive capacity, and generic droplet stability are not part of this paper. Related Hamiltonian-uncertainty results will be assessed for direct relevance rather than included solely because they also concern coexistence.

Scientific rule: unresolved research questions cannot be declared solved by omitting an assumption or invoking an unproved tail estimate. Investigate them; publish only statements with complete proofs or clearly identified model assumptions. Record failed approaches and the grounds for any scope decision. Do not invent priority, authorship, affiliations, citations, or numerical evidence.

## Status

Stage 1: author completed a nine-page compiling draft; five independent reviewers dispatched for round 1.

### Stage 1 round 1 frozen files

- `main.tex`: SHA-256 `2f7e4b687830ac76f0e1e4c34c08b78092c482bf5f6a1e62439e3e8f277e37c5`
- `sections/framework.tex`: SHA-256 `bcffeec68e95b72992736943d9c169994066b1e9a11a7ea1defe449e43dccdb3`
- `sections/thresholds.tex`: SHA-256 `3965fa7ab64cb16eb9e40733567113be0790baac2ec376b6b115da88b9fd743c`

### Stage 1 round 1 assessment

Five reports received. All found no major issue. Five accepted local corrections (four merged reviewer findings and one coordinator terminology clarification) are assigned to the separate correction agent. See `reviews/stage-1-round-1-adjudication.md`. Stage 2 has not begun.

### Stage 1 closed

The separate correction agent implemented all accepted fixes. The coordinator checked each change and the clean LaTeX log. No major finding occurred, so the required five-reviewer round is complete without a repeat. Stage 1 is closed; Stage 2 may begin.

Stage 2: author assigned to microscopic realizations and the short-range sufficiency investigation.

### Stage 2 round 1

Author completed the microscopic section, including a new proposed short-range sufficiency proof and the pure-spin mean-field extension. Five independent reviewers are dispatched; the new short-range proof is not accepted until their findings are assessed. The combined draft compiles to 19 pages. Frozen files:

- `main.tex`: SHA-256 `9bcb57d5ff6d3e7eff1599595fbc096fdc4e8f337b9697f7d55bfdc52cea68e9`
- `sections/microscopic.tex`: SHA-256 `5d47521e17406672142efc7ee8a268865961455922da56a048fc38a67c0f736f`
- `refs.bib`: SHA-256 `c9c359fb9da4e68544984db032d21500ae184284080a471806c42e1d2ab9748a`

### Stage 2 round 1 assessment

All five reports received. The coordinator accepts one major source-convention issue: the 2012 and 2022 contour exterior definitions were incorrectly treated as identical. The derivative strategy itself passed all reviews. Three merged minor corrections concern the general matching-label derivative justification, log-partition wording, and geometric explanation. All are assigned to the separate correction agent. A second five-reviewer round is required after correction. See `reviews/stage-2-round-1-adjudication.md`.

### Stage 2 round 2

All round-1 corrections implemented by the separate agent. The coordinator checked the correction map and revised passages; the 20-page draft compiles cleanly. Five independent reviewers dispatched again, including review of the expanded original-source pressure and matching-label arguments. Frozen microscopic section SHA-256: `4f6cfab2a45063487df9a706731ca9a670f7231f4825410a72c518e3c9061fe2`.

### Stage 2 closed

All five round-2 reviewers found no major or minor issues. The coordinator accepts the corrected proof after inspecting its source conventions, derivative estimates, and probability transfers. See `reviews/stage-2-round-2-adjudication.md`. Stage 2 is closed.

Stage 3: author assigned to shared-bath statistics, with complete proofs of full-state TV and information limits and the boundary regime.

### Stage 3 round 1

Author completed the shared-bath section and coverage record. The combined manuscript compiles to 27 pages without warnings. Five independent reviewers are dispatched after the author handoff. Frozen files:

- `sections/shared-baths.tex`: SHA-256 `3320cb17b34a5b59fbfaf0b9c4eb9043fdc01eaedd1ad29c43a5346571b1178d`
- `main.tex`: SHA-256 `79568610816f779897bfdd98569111529f631b70676bca9ac939d0b42cdbb215`
- `refs.bib`: SHA-256 `83be162d3d61d1f4acbd3b5fa42ac964a9ae4a27b12f0fd6456f56c39e545504`

### Stage 3 round 1 assessment

Five reports received; none finds a major issue. The coordinator accepts two merged minor clarifications: identify the auxiliary bond measure under temperature balancing, and describe the linear-boundary restriction as positive variance rather than microscopic density. All are assigned to the separate fixer. See `reviews/stage-3-round-1-adjudication.md`.

### Stage 3 closed

The separate fixer completed both accepted corrections. The coordinator inspected the auxiliary-law construction, conditional moment and exceptional-mass transfer, terminology, and clean compilation log. No major issue arose, so no repeat round is required. Stage 3 is closed. Stage 4 may begin.

Stage 4 is in author development. Current investigations complete the earlier multivariate optimal phase-loss bound, extend physical boundary formulas to positive microscopic phase measures, and develop calibrated and optimized physical boundary errors. The author and coordinator independently checked these arguments; acceptance awaits the required five-reviewer stage round. Detailed coordinator derivations are retained in `reviews/stage-4-coordinator-investigation.md`.

### Stage 4 round 1

Author completed three new sections, the coverage record, and deterministic formula checks. The 39-page draft compiles cleanly. Five independent reviewers were dispatched after the author handoff, each assigned all new results with different emphasis. Frozen files:

- `sections/gaussian-geometry.tex`: SHA-256 `9ca4859886a47f5d78920a790f284015872b66c6893a7a4aa00139e7a8d6c390`
- `sections/boundary-and-smooth.tex`: SHA-256 `08cb6cc904d6a7a13a37bc74c4188fab519b082770bff077f9fa16a5f048d537`
- `sections/capillarity-diagnostics.tex`: SHA-256 `54bd3844cc8e6313343f8d02ed353be3698fdfde48426b0abd7c19554b39eb89`
- `refs.bib`: SHA-256 `db2afbf1839f98d47f4aad4a6b93958176665da0c3eccf6d2759ac0676663a29`
- `main.tex`: SHA-256 `3ba0937bc1059ba5955314d711ed2296326a0f3df329668bfdc063cd4476db83`

### Stage 4 round 1 assessment

All five reviews received; none identifies a major issue. Two accepted minor corrections concern the bounded offset in the corrected density-tail estimate and degenerate semidefinite geometric level sets. A separate agent is assigned to fix both. See `reviews/stage-4-round-1-adjudication.md`.

### Stage 4 closed

The separate fixer implemented both corrections. The coordinator inspected the corrected tail proof and all range/nullspace level-set cases, and confirmed the clean compilation. No major issue arose; no repeat round is required. Stage 4 is closed. The new optimum and boundary results have completed the required independent stage review. Literature priority remains a separate assessment.

Stage 5: author assigned to synthesis, complete manuscript presentation, literature positioning, reproducibility, and the repository coverage/status audit. No new research direction is to be started.

### Stage 5 round 1

The author completed the synthesis and standalone numerical bundle. The manuscript compiles cleanly to 47 pages. Five independent reviewers were dispatched after the author handoff. Each reviews all Stage 5 changes, with complementary emphasis. The full-manuscript review remains a separate subsequent stage.

Frozen files:

- `main.tex`: SHA-256 `02778449fc97978032e4fc6e162ee03979c49ae36d05339c7218209e5c65fd3c`.
- `refs.bib`: SHA-256 `ca74953b39bea47a6e37395ddfdb3a3cc3a1f2503aaa48f89f1fad1fad6b920c`.
- `sections/introduction.tex`: SHA-256 `bf35e1e2803f9ef00e26922ba8b445f31604eaf3025f5bbe64267fad8abac619`.
- `appendices/short-range-proof.tex`: SHA-256 `7646916834de9a542e63ed449dc276098725e900fff0adf59295909f43b06f9c`.

The coordinator inspected the new synthesis, figure rendering, coverage mapping, status corrections, bibliography, and clean build. The bounded source audit is retained in `reviews/stage-5-coordinator-literature-audit.md`.

### Stage 5 round 1 assessment

All five reports find no major issues. Five merged minor corrections are accepted: the TV comparison with unbounded summaries, logarithmic derivative terminology in the short-range guide, boundary assumptions in the early overview, historical review-status wording, and strict asymptotic growth wording. All are assigned to the separate fixer. See `reviews/stage-5-round-1-adjudication.md`.

### Stage 5 closed

The separate fixer corrected all five issues. The coordinator inspected each revised passage against the formal statements and checked the correction report and clean 47-page build. No major issue arose; a repeat Stage 5 round is not required. All five author stages are closed.

### Stage 6: whole-manuscript review, round 1

Five fresh independent agents are assigned the complete manuscript, including every proof and appendix, all cross-section dependencies, literature positioning, figures, and supporting records. Each reads the whole paper; complementary emphases do not replace that responsibility. They must not read other current-round reports or edit the manuscript. Corrections will be assigned to a separate agent, and any accepted major issue will require another five-reader round.

Frozen main source SHA-256: `eba0469ad1ba66ccf1c3f184fb0793f15bb700caff5219ec95949bc357a218e9`; PDF SHA-256: `b11e0df7e0b0be9e1bece38cd58bd6c008dfb9ca672041929dafb2e242f9c761`.

The coordinator additionally verified a clean fresh build in an isolated temporary directory containing only `main.tex`, `refs.bib`, and the `sections`, `appendices`, and `figures` folders. It produced the 47-page PDF with no warnings, independently of the repository literature and existing build intermediates.

### Whole-paper round 1 assessment

All five reports received. The coordinator accepts the nonnegative-curvature omission in the standalone smooth-necessity proposition as a major formal statement issue: a negative curvature scale supplies a literal counterexample, although the intended physical context and applications are nonnegative. This is a stricter classification than reviewer 5's minor assessment. Four further merged editorial/attribution improvements are accepted. All are assigned to the separate fixer; another five-reader full-paper round is required after correction. See `reviews/whole-round-1-adjudication.md`.

### Whole-paper round 2

The separate fixer implemented all five accepted issues. The coordinator inspected the corrected proposition and vector-model signs, cap wording, leading canonical heat-capacity calculation, and narrow primary-source attribution. The revised paper compiles cleanly to 48 pages with 25 cited references. The coordinator independently read the newly cited Biskup and Kim primary passages as well.

Five independent complete-paper reviewers were dispatched again after this handoff. They may use the correction map and their own earlier review, but must independently assess the current whole paper and must not read each other's reports. No accepted issue is considered closed merely because its textual correction has been made.

### Whole-paper round 2 assessment

All five reviews find no major issue. One minor notation clarification in the new introductory heat-capacity paragraph is accepted and assigned to the separate fixer. The coordinator independently agrees with the correction and the five assessments of the repaired statement and full proof chain. See `reviews/whole-round-2-adjudication.md`. No third round is required unless correction reveals a new major issue.

### Stage 6 closed; manuscript complete

The separate fixer defined the introductory phase probabilities and kinetic Gamma shape, including the no-kinetics convention. The coordinator inspected the exact revised passage and correction record. It changes no formula or theorem and reveals no new issue. Every accepted major and minor finding is resolved.

The required process is complete: five author stages, five independent reviewers after each stage, a second Stage 2 review after its major corrections, and two five-reader whole-paper rounds after the final formal statement correction. The folder retains **40 independent review reports**, their adjudications, and the separate correction records. No third whole-paper round is required because round 2 found no major issue and its sole valid minor issue is now corrected.

Final verification: the **48-page PDF**, with **25 cited references** and **two figures**, builds cleanly both in the repository and from an isolated source-only copy. No unresolved citations, reference labels, warnings, or box diagnostics remain. Numerical algorithms and data passed the independently documented enumeration, quadrature, formula, and archive checks. The large archival run was not unnecessarily repeated. `git diff --check` passes.

Final PDF SHA-256: `0b18c642eedd8d35ed9689592ee06d37dae47825bbdd711359b18abb5cc038ef`.

The paper, reproducibility bundle, coverage mapping, and source/negative-result records are complete within the explicitly stated theorem and model scopes. Internal review is not external peer review or a guarantee of historical priority. Authorship remains unassigned; nothing has been submitted or sent externally. Work stops here as requested.

## Post-completion revision after a referee-style review (2026-09-07)

A full referee-style read of the completed manuscript, with four independent verification passes (short-range contour proof; shared-bath and boundary sections; Gaussian and capillarity appendices; numerical bundle), found no mathematical error and recommended a major revision for presentation, plus a list of minor proof gaps and missing citations. All recommendations were implemented. Per instruction, no result was removed: peripheral material was moved into appendices.

Structure and framing:

- Introduction rewritten: a "mechanism in two lines" subsection states the slope/curvature heuristic behind both thresholds; a physical-context paragraph names finite-bath Monte Carlo, nanoscale calorimetry, and finite-bath thermalization; a "calibration sensitivity" subsection shows the secant energy needs relative precision of order 1/N, the same sensitivity the canonical ensemble has at coexistence; the relation-to-earlier-work subsection is consolidated and ends with a single explicit list of the five contributions, replacing the repeated novelty disclaimers.
- The fixed-phase-count proposition and the linear-capacity subsection moved from Section 5 to the new Appendix D (appendices/shared-extensions.tex). Section 5 gains a short subsection naming the phase partitions used for each microscopic model (Voronoi cells for mean field; midpoint energy events for short range).
- The exact secant interior-gain subsection moved from Appendix C into Section 6, where eq. boundary-maximal-gain is used.

Proof and statement fixes:

- Appendix A: the color threshold q_0(d) is now fixed once at the start (it exceeds 2d, covers the cited contour results, and absorbs the extra exponential slack); the identification of the BKMS free-energy crossing with the BCT magnetization onset is now argued and cited (Kotecký–Shlosman 1982; Laanait et al. 1991); the bound on internal contour intersections M(Γ) is proved rather than asserted; the cluster sum is anchored as in BCT Lemma A.2; the Lipschitz constant for a_i is corrected to 2C; the BKMS error is noted as O(q^{-bL}).
- Theorem positive-sufficiency now states its moment bound for N ≥ N_0, matching the microscopic lemmas.
- Proposition smooth-necessity requires κ_N > 0 (previously κ_N ≥ 0 made it vacuous).
- Theorem physical-boundary states up front that the phase probabilities are defined on the auxiliary decomposition; Theorem physical-boundary-optimum's proof records that the limit exists.
- Section 5: the energy centers are defined as any deterministic sequences satisfying the tightness hypothesis.
- Appendix B: the scalar necessity proof is written out via the label-matching argument; "lie on one sphere" replaced by "cospherical" with the d = 1 caveat at the theorem; the constant clash c N^{3/4} renamed c_1; bounded transformed centers justified where asserted.
- Appendix C: the LDP speed is stated as the d = 2 surface scale; t_γ² positivity noted in Appendix D.

Citations and numerics:

- Added: Hilbert–Hänggi–Dunkel 2014 and Dunkel–Hilbert 2014 (entropy convention); Leung–Zia 1990 and Neuhaus–Hager 2003 (droplet-to-strip crossover on a square torus); Kotecký–Shlosman 1982 and Laanait–Messager–Miracle-Solé–Ruiz–Shlosman 1991 (large-q transition point). All DOIs verified against publisher pages. Kim–Keyes–Straub was checked and does exhibit droplet and strip regions.
- Appendix C now cites the specific Griffin–Matty–Swendsen norm (their eq. 23) that the histogram example contrasts.
- Section 7 notes that the mean-field saddle lies on the Voronoi boundary with rate excess log 3 − (19/12) log 2 ≈ 1.1e-3, and reports exact finite-N ordered-phase variances and weights (N = 3000, 12000) against their limits.

Housekeeping: compiled Python bytecode removed from version control and ignored; README describes the underflow guard in the standalone enumeration script. The revised paper builds cleanly (50 pages, 31 references) from an isolated source-only copy.

## Commit-review corrections (2026-09-07)

Review of commit `0d0d39f` identified an incorrect variance-detection step in the rewritten scalar Gaussian proof. The proof now obtains convergence of the variance ratio from the separation of the matched means, then uses probabilities above the target means to establish vanishing displacements. No theorem statement changed.

The calibration discussion now distinguishes relative errors of order 1/N, which change phase odds by order one, from the o(1/N) errors needed for vanishing changes. Relative energy errors are measured against the reservoir energy at a phase center.

`code/potts_phase_statistics.py` and `data/potts-phase-statistics.json` reproduce the pure-spin statistics in Section 7. The manuscript, script, and README specify Euclidean Voronoi distance in all three occupation fractions and assign ordered–disordered ties to the ordered phase. The existing independent spin enumeration now checks the phase probabilities and conditional variances by computing distances to the four minima directly.

Validation: the phase calculation reproduces the quoted values at N=3000 and N=12000. Explicit enumeration through N=8, direct density quadrature at N=12, and the Stage 4 formula checks pass. The updated manuscript builds without LaTeX warnings and remains 50 pages with 31 references. Trailing whitespace in the generated log is removed after the build, and `git diff --check` passes.
