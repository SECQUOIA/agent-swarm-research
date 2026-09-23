# S4b author report: weighted cactus algorithms

Status: authored and frozen for the required five independent reviews. This report does not mark the stage accepted. The correction agent and lead must adjudicate the review findings before S5 begins.

## Delivered scope

Created `complexity/sections/07-weighted-cactus.tex` and changed only the section-7 input in `complexity/main.tex`. The old `sec:a-open-problems` label remains as an alias on the new section, preserving existing references. The unused placeholder file remains on disk; the manuscript no longer inputs it. Added two verified primary bibliography entries, reused the established Aßmann and Vigneron entries, and left accepted sections 1–6 and Paper B unchanged. Updated `completion-coverage.md` as authored pending review.

The new section gives the following standalone statements and proofs:

| Coverage | Main labels and treatment |
| --- | --- |
| General weighted nomination faces | `thm:a-wcac-faces`: fixed maximum block rank r and support p, O(rp) unfixed coordinates and n^{O(rp)} faces; objective-free pruning, zero-induced-objective block contraction, rational disaggregation, resistance independence, strict chain ordering, and two separate smoothing/perturbation limits. |
| Fixed-law affine nominations | `thm:a-wcac-affine`, `lem:a-wcac-local`: arbitrary weighted support, fixed parameter dimension, fixed asymmetric quadratic laws; correct radical root even for negative leading coefficient, exact rational branch with possibly vanishing denominator, and explicit all-zero stratum. |
| Accuracy-bit summation | `lem:a-wcac-panels` and the common-partition subsection: constructive rational binomial panels including the zero region, coefficient/degree bounds after dense expansion, common sign partition, rational summation before optimization, open-part suprema, strict-threshold algebraic sampling, explicit 5ε/16 sample loss, and rational original-parameter recovery. |
| Joint coefficient elimination | `lem:a-wcac-threshold`, `lem:a-wcac-candidates`: one-equality LP, exact threshold duality, full tied aggregates, all boundary/stationary/flat circulation cases, both quadratic roots, zero leading/linear coefficients, and exact eligibility projection. |
| Joint summation and recovery | Local surrogate comparisons precede summation; no Cartesian product of cycle choices or comparison of exact radical sums. Recover tied original coefficients separately over each local extension. `lem:a-wcac-coefficient-continuity` proves the original-coefficient sensitivity needed for rounding. |
| Full balanced nomination boxes | `cor:a-wcac-box`: compose the resistance-independent face family with fixed-dimensional optimization, compare certified face values, and rationally lift the winning scenario. No operating filters are added to this corollary. |
| Exact local filters | `thm:a-wcac-capacities`: exact feasibility and algebraic near-optimal output with local arc capacities. Fixed laws additionally allow bounded-degree closed local polynomial constraints involving one cycle/bridge and shared parameters. Joint coefficients retain only arc capacities. |
| Rational output under slack | `eq:a-wcac-resistance-flow`: a proved weaker square-root flow perturbation bound suffices for polynomial-bit rounding with a supplied positive capacity tightening. The comparison is only to the tightened optimum. `ex:a-wcac-irrational` proves the rational-data four-cycle with sole feasible parameter sqrt(2). |
| Exact fixed nominations | `thm:a-wcac-exact-profile`: polynomial-time exact rational optimizing coefficient profiles, optional rational signed arc bounds, irrational aggregate-boundary recovery by rational endpoints, exact local comparison across two radicals, and separately represented global sums. `ex:a-wcac-interior` proves the unique profile (1,2,1,1), so an interior resistance is necessary. |
| Implementation scope | The existing supplied-block symmetric solver is described accurately. It neither accepts/validates a graph decomposition nor implements varying-nomination QE or independent directional intervals. Its internal witness checks are not advertised as an untrusted optimality-certificate checker. |

## New mathematical development requiring explicit review

The stage strengthens the source results' joint **symmetric** interval theorem to a second model with **independent positive and negative quadratic coefficient intervals**. This is not merely a change in wording and should be reviewed explicitly.

The lead proposed examining this extension; the author independently checked and incorporated it:

1. On each closed sign cell, exactly one coefficient per nonzero edge flow is active. Use that directional interval in the original one-row LP. Inactive coefficients are unconstrained by the local physics and may be chosen rationally; both branches give zero at zero flow.
2. The leading circulation coefficients remain fixed rationals on each sign cell. Threshold elimination, both-root candidates, flat cases, and all approximation encoding bounds therefore remain unchanged.
3. The symmetric model is stated separately: a shared coefficient is a diagonal constraint, not two independent intervals. Recovery assigns the active value to the shared original coefficient before rounding. This prevents inadvertently relaxing the original model.
4. Coherent cycle reorientation swaps directional coefficient intervals. Bridges maximize with the active directional bounds.
5. Smooth by g+ρx with ρ independent of the coefficients. Unit terminal adjoint currents have absolute value at most one. The parameter derivatives are x_+² and −x_-², so each original-coordinate terminal sensitivity is bounded by B². Integration and uniform smoothing limits yield the L1 bound even across flow-sign changes.
6. For capacity recovery, the asymmetric law satisfies |g(u)−g(v)|≥β_L|u−v|²/2. Combined with the terminal sensitivity, the squared flow change is at most 2B²(k+1)δ/β_L, where k is the actual number of independent original coefficient coordinates (m or 2m). Polynomial-bit widths depending on σ² preserve original capacities.
7. Fixed rational nominations still admit exact rational original coefficient profiles: active aggregate boundaries force endpoints, rational circulation cases fill a rational one-row LP, and inactive directional coefficients can be any rational allowed values.

This extension applies to the affine, unrestricted-box fixed-support, local-capacity, and exact-profile statements. It does not change the public solver's implementation scope. No general bounded-block compiler, globally correlated coefficient theorem, or higher-degree local-candidate theorem is inferred.

## Critical proof and output choices

- Zero-induced-objective block contraction is proved by translating the exterior components and using their zero coefficient sums. It is stronger than pendant pruning and essential for nonzero currents on every ordinary chain.
- The coarse face is fixed before introducing positive path-interior adjoint sources. A single global perturbation would spoil the chain argument.
- Exact local formulas need no uniform lower bound on their rational denominators. Nonzero domains are retained, the rational formulas are optimized exactly on their strata, and original-parameter rounding uses physical continuity across stratum boundaries.
- The two errors in choosing a local winner by surrogate comparison are included: max values differ by at most the local approximation error; the selected candidate can be twice that error below the exact local winner. The global sample loss calculation uses the selected candidate's error relative to its selected surrogate.
- Algebraic output uses separate local extensions over one common nomination sample. It never constructs a primitive element containing all cycle radicals.
- General local polynomial filters are included only for fixed laws, where the objective state formula stays unchanged. Joint polynomial filters could create higher-degree circulation boundaries and are not covered.
- Tight capacities may force irrational nominations. Rational recovery compares only with the nonempty tightened problem; no claim about closeness of tightened and original optima is made.
- The stronger all-graph linear flow perturbation bound remains for S5. The present weaker bound is proved here and depends only on accepted A03 tools plus the directional sensitivity lemma.
- No exact comparator for the global scalar objective is supplied. Exact local comparison suffices to select a globally optimal profile at fixed nominations.

## Primary literature checked

Read the relevant local extracted text and inspected the corresponding original PDF passages via `pdftotext`; the originals, not repository summaries, support the comparisons. Applicable `literature/AGENTS.md` was read. No knowledge-base package or generated index was modified.

- **Gotzes, Heitsch, Henrion, Schultz (2016)**: local package `schultz2016-on-the-quantification-of-nomination`, original PDF pages 20 and 26 (printed 18 and 24): Theorem 6 gives the local affine-ray quadratic-radical/rational formula; the final section explicitly permits node-disjoint cycles with attached trees. The actual author PDF title is *Feasibility of nominations in stationary gas networks with random load*, WIAS Preprint 2158 (2015). The new bibliography entry records this version distinction. Publication title, authors, volume 84, pages 427–457, and DOI were verified at [the publisher](https://link.springer.com/article/10.1007/s00186-016-0564-y). Manuscript theorem/page locators explicitly refer to the author manuscript. KB locators: `[[schultz2016-on-the-quantification-of-nomination]] p.20`, `p.26`.
- **Vigneron (2014)**: local package `vigneron2014-geometric-optimization-and-sums-of`, [author manuscript](https://antoinevigneron.github.io/manuscripts/rational.pdf), PDF page 7 Section 2.3, page 8 Theorem 6, page 9 Section 3.2. Its bit-model extension is explicit and retains polynomial dependence on 1/ε. The manuscript credits common arrangements and approximate algebraic summation, with an explicit statement that these locators refer to the author manuscript. KB locators: `[[vigneron2014-geometric-optimization-and-sums-of]] p.7-9`.
- **Aßmann, Liers, Stingl, Vera (2018)**: local package `amann2018-deciding-robust-feasibility-and-infeasibility`, original arXiv PDF pages 15–16, 20–21: independent positive coefficient intervals, Section 4.2 tree LP reduction, Section 4.3.3 and Lemma 4.10 circulation-interval conditions linear in coefficients. Existing bibliography key is reused; no duplicate article record remains. Publication metadata agrees with [SIAM](https://epubs.siam.org/doi/10.1137/17M112470X). KB locators: `[[amann2018-deciding-robust-feasibility-and-infeasibility]] p.15-16`, `p.20-21`.
- **González Grandón, Heitsch, Henrion (2017)**: local package `henrion2017-a-joint-model-of-probabilistic`, original WIAS PDF pages 6–10: passive single-entry tree, random Gaussian exit loads and robust roughness uncertainty, explicit ellipsoidal and rectangular inner minimization. The new entry records the published article and points to the author preprint for section locators. Publication metadata was verified at [the publisher](https://link.springer.com/article/10.1007/s10287-017-0284-7). KB locator: `[[henrion2017-a-joint-model-of-probabilistic]] p.6-10`.

No priority claim rests on the absence of a matching search result. The comparison claims the precise combined guarantees and credits the local formulas, LP duality, approximation, and real-algebraic tools.

## Checks

Full commands, stdout, stderr, return codes, and elapsed times are retained in `completion-s4b-checks.json`. All checks used `/home/sgusev/miniconda3/envs/minlp-notes/bin/python` and passed.

| Check | Distinct evidence |
| --- | --- |
| `reopened_weighted_checks.py` | 360 exact panel points; 1,200 asymmetric cycle formulas, including negative/positive/zero quadratic coefficients and the zero stratum. |
| `reopened_weighted_contraction_checks.py` | 18 original/reduced physical scenarios, 72 contracted blocks; maximum objective difference 1.15e−12. |
| `check_reopened_weighted_faces_review.py` | 180 exact positive-source paths, 3,598 horizontal-level checks, 60 biconnected two-terminal blocks. |
| `check_reopened_weighted_review.py` | 55 exact panel points, five denominators tending to zero, 240 high-precision cycle and difference-flow cases. |
| `reopened_joint_weighted_checks.py` | 216 exact threshold-LP cases; 90 cycles and 15,036 independently solved physical scenarios. |
| `check_reopened_joint_weighted_review.py` | 203 independent LP cases and exact unique interior optimizer. |
| `check_reopened_joint_weighted_second.py` | 400 LP cases and 1,000 exact quadratic-root identities. |
| `exact_weighted_cactus_checks.py` | 1,200 arithmetic comparisons, 45 cycle cases including 15 capacity cases, 1,531 physical profiles, 80-bit multiblock enclosure. |
| `check_exact_weighted_cactus_review.py` | 1,220 arithmetic cases, 280 pinned-circulation/sense cases, seven special cases. |
| `check_exact_weighted_cactus_arithmetic.py` | 88 cancellation/equality/interval controls; explicit graph reconstruction for two cycles and a bridge; orientation/gauge invariance; 24 invalid schema inputs; CLI under −S and −S −O. |
| New `verification/check_a7_weighted_asymmetric.py`, ordinary and −O | 120 original 2m-coordinate LPs versus active threshold elimination (29 feasible); 32 exact directional cycle optimizations using capacity-restricted sign panels; 32 interval-swap reorientations; 1,280 independent original-law physical samples and coefficient-sensitivity checks; explicit coefficient-induced sign crossing. |

The new test is a harness, not a public directional solver. Its original coefficient LP comparator enumerates the full box-plane vertices, including inactive coordinates. During harness development, a zero-flow recovery case initially copied a negative-panel coefficient into the positive interval. The harness was corrected to leave both zero-flow coefficients at their own allowed defaults, exactly as required by the manuscript's explicit zero-flow rule. This did not require a change to the mathematical proof or existing solver. All final runs pass. Numerical sample checks supplement, rather than establish, the universal proofs.

## Build and frozen hashes

Built only Paper A by importing `verification/build_and_check.py` and calling `build('complexity')`; the CLI that also builds Paper B was not used. `completion-s4b-build.json` records all 14 current TeX/Bib input hashes, the command, and final diagnostics:

- Return code 0; PDF exists.
- Zero errors, unresolved references, unresolved citations, duplicate labels, and overfull boxes.
- No duplicate bibliography keys. Every recorded input hash was independently recomputed and matched.

Frozen SHA-256 values:

- `complexity/sections/07-weighted-cactus.tex`: `8b5645a80c0922cda4e57a1948670172268fa0cd4dc9fdc9c6505ec258a10219`
- `complexity/main.tex`: `d05e993163b102be9eb987df326b8b1b20e8f9516bd9fb3135d2633bc7f139e4`
- `complexity/references.bib`: `ff87a1b986f407b1da72303f1103391961accc4aaa6ce2442918f8cfd127b918`
- `complexity/build/main.pdf`: `7230d2f7fbdca6d55f6b3c013dfc9011b94919c9ea68569d994f8438dd8ff9c8`
- `verification/check_a7_weighted_asymmetric.py`: `f2342dfc6bc7cfac0eff7aae12a3a18e015c5b6abd26cfae9a9539097200dec2`

The manuscript is frozen at these hashes for review. Broader correlated design, energy/performance results, the general bounded-block investigation, final framing, and manuscript-wide consolidation remain assigned to later stages.
