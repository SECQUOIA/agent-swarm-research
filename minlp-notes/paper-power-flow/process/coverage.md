# Source coverage map

This map distinguishes manuscript coverage from repository history. All four writing stages and the separate whole-manuscript review are accepted. The integration supplies the literature comparison and verification appendix. Every relevant source below has a manuscript destination or an explicit duplicate/out-of-scope disposition; there are no pending coverage entries.
Repository source paths are relative to the repository root. Manuscript paths
beginning with `checks/`, `process/`, or `verification/` are relative to
`paper-power-flow/`; paths already beginning with `paper-power-flow/` remain
repository-relative.
References to sections 01–06 identify the corresponding files in
`paper-power-flow/sections/`, not the printed section numbers after integration.

| Repository source | Material relevant to this paper | Manuscript destination/status |
|---|---|---|
| `results/ac-power-flow-existential-reals.md`, Theorem 1, Sections 1 and 3 | Exact RPF model; membership; complement paths; addition and inversion; both reduction directions; degree and fixed numerical data | Covered in sections 01–02; exact counts and rational-homeomorphism statement made explicit |
| Same result, Theorem 2, Sections 1–2 | AC model; rational-cosine encoding; real-angle lift; winding count; zero reactive injections; rectangular angle box | Covered in section 03, with explicit series/shunt signs, all limits below pi, determinant crossing rule, and componentwise references |
| Same result, Corollary 3, Remarks 5–6 | Conditional NP obstruction; arbitrary algebraic degree; unique magnitudes | NP consequence covered in section 02; section 05 distinguishes rational universality for compact basic closed sets from general compact semialgebraic topology; unique voltages and designated-coordinate degree use a self-contained conjunction-only arithmetic lemma |
| Same result, Remarks 1–4 | Physical interpretation, loads-only comparison, angle range, lossless and tree distinctions | Covered in the introduction and sections 01 and 03: physical DC, fixed-source loads, lossless fixed-magnitude AC, and tree scope are distinguished |
| Same result, Section 5 | Legacy numerical checks and exact winding evidence | Verification appendix covers all eight examples analytically and identifies the old solver evidence precisely; four exact suites support the final construction |
| `notes/review-power-flow-existential-reals-A.md` | Initial angle-semantics failure; explicit cycle counterexample; rational input; repeated copies; free-injection bounds; degree; numerical timeout limitations | RPF corrections incorporated in sections 01–02; AC counterexamples and model distinctions covered in section 03; verification appendix states the old numerical evidence and its limitations |
| `notes/review-power-flow-existential-reals-B.md` | Independent original-network exact checks and reduction audit; angle issue and follow-up | RPF proof checked; AC real-lift distinction and corrected transfer covered in section 03 |
| `notes/review-power-flow-existential-reals-C.md` | Corrected AC membership; unequal magnitudes; half-open crossings; attribution; optional angle extension | Section 03 proves a scale-independent determinant rule and extends membership to every rational cosine in (-1,1]; independent geometric checks include long arcs and axis endpoints |
| `notes/review-existential-reals-closeout.md` | Final scope corrections; singleton/coordinate-degree dependence; finite-check limits | Sections 02–03 correct complexity and angle semantics; section 05 explains coordinate versus field generation and symbolic-certificate limits; finite checks remain supporting evidence |
| `notes/power-flow-existential-reals-novelty.md` | Detailed primary-literature comparison and search history | Introduction gives checked primary-source comparisons. Broad absence claims are omitted, and an LMI characterization is not treated as an exact Turing algorithm |
| `code/power_flow_existential_reals/dc_resistive_build_and_check.py` | Original construction; per-bus free bounds; numerical QCQP and rectangular AC experiments | Read and compared; paper-local checker independently builds fixed-85 version and has no Gurobi dependency; verification appendix supplies the analytic eight-example table and accurately identifies the historical AC bounds; licensed solver not rerun |
| `code/power_flow_existential_reals/check_winding_count_exact.py` | 360 scaled line pairs; 4,136 cycles; axis/reversal and winding regressions | New standalone `checks/check_ac_exact.py` covers determinant crossings, unequal scales, negative cosines, 177,168 cycles against a rotated cut, and 648 AC sign checks; verification appendix records both suites; actual rerun log is verification/root/legacy-winding.log |
| `results/pooling-existential-theory-of-reals.md`, algebraic-degree corollary | Shared ETR-INV rational-equivalence and coordinate-projection argument | Section 05 and Appendix A prove the power-flow consequence using verified conjunction-only gates; the broad source universality claim is corrected, and no pooling manuscript dependency is used |
| `notes/pooling-existential-reals-novelty.md` | Shared source/complexity survey and Bienstock–Verma discussion | Shared literature discussion covered in introduction; no separate power-flow theorem |
| `notes/open-problems-from-literature.md`, entry 11 | Bienstock–Verma approximate NP question | Section 06 distinguishes exact feasibility, a specified gap promise, and the lossless fixed-magnitude approximate-membership question; the latter is not claimed resolved |
| `notes/log.md`, power-flow entries near lines 1039–1092 | Chronology of authoring, failed angle semantics, corrections, audits | Historical duplicate; no additional result to promote |
| `notes/reopened-run-status.md`, power-flow entry | Summary of completed result | Historical duplicate |
| `notes/research-continuation-assessment.md` | Research-priority assessment | No additional theorem; paper need not reproduce prioritization |
| `notes/research-continuation-closeout.md` | Scope and evidence reconciliation | Historical duplicate of closeout; relevant checks covered by the verification appendix |
| `notes/potential-flow-global-correlation-novelty.md` | Incidental reference to stochastic power-flow literature | No exact power-flow-feasibility development; out of mathematical scope |

## Primary-source dependencies

The local `literature/AGENTS.md` was read. Literature files were not changed.
Page locators refer to page markers in archived full text and, where indicated,
the original PDF. Preprint and journal numbering must not be silently conflated.

| Source | Verified material / intended use | Status |
|---|---|---|
| `literature/papers/abrahamsen2022-the-art-gallery-problem-is/` | Archived STOC/arXiv copy, Definition 5 and Theorem 7, p.11; ETR-INV variable interval and all three equation forms | Text read; original PDF p.11 visually checked; stage 1 cited explicitly with version qualification |
| `literature/papers/abrahamsen2019-dynamic-toolbox-for-etrinv/` | Complexity conventions p.1–2; Theorem 1 p.3; rational equivalence and linear extension, Definitions 4–5 p.4 | Independent review found the general Boolean Lemma A and its unrestricted rational-universality conclusion false. Section 05 gives the sharp basic-closed scope and an explicit obstruction; Appendix A verifies conjunction-only arithmetic gates and affine replacement-coordinate recovery without importing the failed step or printed range-lemma errors |
| `literature/papers/schaefer2024-the-existential-theory-of-the/` | Complexity definitions, current broader comparison, ETR-INV | Introduction and section 01 use its class definitions and complexity context; no literature-absence claim is made |
| `literature/papers/bienstock2019-strong-np-hardness-of-ac/` | Lossless fixed-magnitude model p.1; approximate NP discussion p.6 | Section 06 discusses the arXiv-version approximation question precisely; introduction compares the physical model; the approximation question cites arXiv:1512.07315v2 (2019) separately from the journal article |
| Gan–Low 2014, *Optimal power flow in direct current networks* | Provenance of resistive model; exactness regimes | Cached primary publisher PDF read, including its distinction from linear DC approximation and its two sufficient exactness regimes; introduction cites the scoped conclusions |
| Lavaei–Low 2012, *Zero duality gap in optimal power flow problem* | Appendix B, Case 2; scope of zero-reactive reasoning | Cached primary PDF text inspected, Appendix B Case 2; section 03 uses a self-contained counterexample and does not import its discrete-phase assertion. Introduction credits the zero-reactive connection without importing an unrestricted phase assertion |
| Dörfler–Chertkov–Bullo 2013, *Synchronization in complex oscillator networks and smart grids* | Oscillator equilibrium equation and cohesive-angle analysis | Cached primary full text read, Eq. (1) and supplementary Lemma 2; section 03 cites the equation/background only, not its global uniqueness assertion. Our real-lift lemma is proved independently |
| Jeeninga–De Persis–van der Schaft, DC power grids with constant-power loads, Part I | Fixed-source loads-only feasibility characterization; precise relation to this model | Cached primary Theorem 3.22 read in full: BOTH exact and interior feasibility; introduction states the distinct model and does not infer exact Turing P. Part II supplies no additional theorem needed here |
| Lehmann–Grastien–Van Hentenryck, AC-feasibility on tree networks | Different hardness regime; input encoding distinctions | Primary full text read: fixed unit magnitudes and star construction; introduction gives precisely the tree/star hardness comparison |
| Bienstock–Muñoz, LP formulations for polynomial optimization | Approximation with bounded structure and irrational exact solutions | Primary arXiv:1501.00288v15 (19 October 2016), Theorem 7 and Corollary 8 read: scaled feasibility/optimality approximation; introduction identifies that version and distinguishes this from exact decision |

New independent results developed during manuscript preparation belong in this
map as they are proved and reviewed. Stage 1 adds the explicit size bound,
exact rational homeomorphism (including unused variables), and license-free
original-network checker. Stage 2 develops and proves: membership for all
rational cosines greater than -1; an exact determinant crossing count;
the fundamental-cycle angle-budget criterion; strictly positive principal-only
windows with size-dependent polynomial-bit cosines; and the positive-width
one-sided reactive-interval corollary. These results passed the stage-2 independent review process. Stage 3 adds the
structural and numerical developments listed below. Its first five-reviewer round exposed a false general universality dependency, now repaired with the sharp basic-closed characterization and a separate triangulation argument; the repaired developments passed a second five-reviewer round, with its remaining coefficient-field qualifier corrected and checked before stage 3 closed.


## Stage 3 developments and additional primary dependencies

- Section 04 reproduces the bounded crossover while retaining every original
  and transmitted interval. Its generalized complement 9/2 construction is
  planar by an occurrence-aware disk-and-corridor embedding. Free-injection
  connectors and harmonic even subdivisions prove all graph restrictions
  simultaneously, preserving rational solution-set equivalence.
- Section 05 proves rational universality precisely for compact basic closed
  sets, proves that scope is sharp via compact denominator bounds and the
  three-quadrant obstruction, and retains arbitrary compact semialgebraic
  topology by finite triangulation and standard-simplex nonface equations.
  Appendix A proves the conjunction-only bounded arithmetic lemma with unique
  rational extension and scalar-affine recovery, using explicit verified gates.
  This supplies unique voltages of any designated coordinate degree. The
  corresponding AC statement fixes its reference-phase convention. No
  complexity bound is asserted for arbitrary scaling or triangulation.
- Section 06 proves two-sided residual transfer for the ordinary gadgets,
  gives an explicit infeasible recurrence family with doubly exponentially
  small residuals in the original network, and applies a general polynomial
  minimum theorem to give the matching separation scale. It proves short
  rational certificates for a defined promise problem and quantitative
  reactive stability, including component and singleton cases, then combines
  these bounds for approximate AC states. It makes no tolerance-hardness or
  general exact-algorithm lower-bound assertion.
- `checks/check_developments_exact.py` checks 49 generalized crossover
  profiles, 8 generalized inversion profiles including repeated names,
  connection of three components, three even-subdivision scales on an
  independently specified triangle with a pendant bus and unequal
  conductances, 360 perturbed original-network profiles, the
  tiny-residual family for k=0,...,10, and 100 exact graph-Poincare and
  voltage-Lipschitz samples. It uses original edge-current aggregation
  and only the standard library. It does not claim numerical planarity
  tests or finite samples prove the general results.

| Additional primary source | Verified material / use | Evidence |
|---|---|---|
| Dobbins–Kleist–Miltzow–Rzążewski, DCG70(2023),154–188 | Theorem 2.1 and Figure 3, printed p.163; crossover equations and bounded-witness promise | Cached publisher PDF and extracted text read; section 04 states its own bounded solution-set version and includes a fresh incidence drawing |
| Ohmoto–Shiota, arXiv:1505.03970v2 (2017) | Theorem 1.1 and Section 1.2, p.2: semialgebraic triangulation, finite for compact sets | Cached primary PDF and extracted text checked; only topological/semialgebraic homeomorphism is used, not rational equivalence or triangulation-size bounds |
| Jeronimo–Perrucci–Tsigaridas, SIAM J Optim23(2013),241–255 | Journal Theorem 1.1; same explicit polynomial-minimum bound as cached arXiv Theorem 1, p.2 | Root verified journal numbering; stage 3 checked cached primary formula and all application hypotheses, including even degree, integer coefficients, and compact connected set |

Stage 3 build and actual exact-check output are retained in
`paper-power-flow/verification/stage03-build.log` and
`paper-power-flow/verification/stage03-exact-check.log`.

Stage 3 round-1 corrections are documented in `process/stage03-corrections.md`.
The additional standard-library `checks/check_arithmetic_exact.py` checks
1,681 composed product/reciprocal profiles, a full disk circuit with 332
variables and 330 actual addition/inversion equations on 49 valid, 72 outside,
and 49 altered profiles, nine dyadic constant-chain configurations, and
35 standard-simplex support profiles. These checks support the analytic
proof and do not replace its quantified or topological arguments.

## Integration and worktree closure

- The introduction compares every power-flow model used in the source notes
  against the relevant primary literature, without promoting search absence
  to a novelty theorem. The conclusion collects only proved conclusions.
- The verification appendix records all four paper-local suites and their
  actual scope, the rerun legacy winding counts, and exact solutions or
  contradictions for every legacy numerical source case. It states the four
  historical AC instance sizes and the reported bound on the sum of squared
  imaginary voltages; it does not use numerical solver output as proof.
- The relevant result, all three power-flow reviews, novelty/closeout notes,
  and both source programs are byte-identical in the other worktree
  `/home/sgusev/repo/minlp-notes-potential-flow`. Evidence is retained in
  `process/worktree-coverage-audit.json` and the refreshed
  `verification/root/worktree-coverage-final-check.json`. The other
  worktree therefore contributes no unaccounted power-flow development.
- Potential-flow papers concern a different model and already have their own
  manuscript folders; they remain outside this paper's scope. The shared
  pooling arithmetic dependency is proved locally, without importing a
  pooling paper or broad universality claim.
- Failed historical angle and Boolean-universality assertions are represented
  by their corrected mathematical substance and explicit scope boundaries.
  Author/reviewer chronology and numerical time-limit details remain process
  evidence rather than separate final theorems.
- Stage-4 execution logs use `verification/stage04-*.log`. Bibliographic
  metadata and version-specific citation choices are recorded in the
  stage-4 author report.
