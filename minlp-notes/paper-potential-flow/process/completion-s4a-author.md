# S4a author report

Date: 2026-09-10. Status: authored and ready for five independent reviews; not accepted. Worktree: `/home/sgusev/repo/minlp-notes-potential-flow`.

## Deliverable and scope

Replaced `complexity/sections/06-weighted.tex` with a complete standalone section (about 1, 100 source lines). All ten promoted results assigned to S4a are proved, plus the supplied signed-path refinement, the universal pairwise-pressure hull characterization and additive endpoint recovery, and the qualitative region classifications for every fixed nonlinear power. Updated their coverage rows as authored, pending review. Added five bibliography entries; accepted sections01–05, macros, main structure, Paper B, and source-result files were not changed. No appendix, commit, or subagent was created. Preserved pre-existing uncommitted work.

The section is organized by mathematical dependence:

1. Tree formula, polynomial-bit rational quadratic certificates, arbitrary-support hardness and its approximation gap, exact support/cut-direction algorithms.
2. Fixed-global-rank and supplied signed-path faces, interval-resistance elimination through the accepted box-leaf lemma, exact algebraic recovery, and fixed-nomination arbitrary-support companions.
3. Fully explicit triangle and theta gadgets, both discrete hardness reductions, exact verifiers, positive integer scaling, and unit-cost DAG total-flow hardness.
4. Cactus circulation-box geometry, finite-set convex hulls, exact rational optimizing scenarios, additive scalar evaluation, and the exact scalar SRS barrier.
5. Universal objective-dependent hull classes with all quantified converse restorations, followed by full-vector region convexity and the qualitative nonlinear-power extension.

## Proof audit and details made explicit

- Proved the bounded-polytope rational-QP certificate lemma directly. Stationary systems can be singular: the objective is constant on each stationary affine intersection, and rational linear feasibility supplies a point. The arbitrary-dimensional certificate argument is separate from fixed-dimensional face enumeration.
- Checked the comb realization, unit-magnitude coefficients, half-unit no gap, 1/8 value/witness obstruction, endpoint rounding, and optional integer resistance conversion. Included the exact O(n²K) arithmetic pseudopolynomial algorithm for this family.
- Checked zero-cut contraction and rational nomination disaggregation; cut-flow marks; strict adjoint order and polyhedral normal-cone conditions on degenerate domains; closed-face limits; resistance-independent face transfer; rational arrangement/QP optimization; and complete state recovery. The path count k=t+2 and support bound k≤2p−2 are explicit.
- Checked the signed-path perturbation acts on potentials, with compensating source at a marked vertex. Positive sources give peaks; negative sources give valleys; zero coefficients and returning paths are covered. The finite family has k+2P free nominations, P=k−1+r_actual. Global rank retains every circulation in one algebraic core. Recovery uses the accepted scalar-box lemma, not an unpublished fixed-core result. No finite-set conclusion is inferred on cyclic graphs.
- Re-derived both gadget objective identities, physical signs, exact endpoint states, gap constants, preprocessing outputs, and encoding bounds. For weighted potentials common resistance scaling amplifies the objective gap. For flows it does not; nomination scaling supplies the separate constant-error consequence. Unit-cost DAG edge counts and total-flow identity are explicit.
- Checked cactus root ordering, envelope strictness, attained endpoints for finite sets, Cartesian-product convex hulls, independent block choices, and the difference between rational exact scenario recovery and SRS-hard scalar comparison. The SRS reduction uses the weak ≤ convention and preserves equality, with fixed trivial outputs.
- Proved the missing pairwise-pressure hull converse using the accepted theta formula and quantified restoration. The three restoration constants are R=12(10000m²)³ for weighted potentials, R=18(10000m²)³ for pairwise potentials, and R=18000(10⁹m²)³ for linear flows. Each proof explicitly checks energy competitors, induced balanced nominations, pressure/flow sensitivity, positive coefficients, and retained strict gaps.
- The positive pressure-hull proof refers to the cactus paragraph following the accepted general envelope theorem, rather than silently applying an adjacent-terminal lemma to arbitrary terminals. Additive endpoint recovery has an explicit 2M-evaluation loss budget and requires an applicable fixed-scenario accuracy-bit evaluator; it makes no algorithmic claim for arbitrary continuous input laws.
- Proved cyclic-edge deletion, including the constant-state case, strict injective flow and potential-drop coordinates, and the endpoint-chord consequence of convexity. Nonconvexity after restoration uses this injectivity rather than the inadequate assertion that every one-dimensional image is a segment.
- Rechecked the nonlinear-power theta derivatives a′(0)=5/8 and a″(0)=(γ−1)/32, and the potential-curve derivative 1+[a/(a+1)]^(γ−1). All differentiation is at positive outer-flow arguments; the realized cross-flow interval is strictly positive, so γ<1 is covered without differentiating the cross law at zero. Uniform energy restoration and rational density prove existence only. Positive-width thickening is separately existential, with no hidden polynomial encoding claim.
- No theorem filters scenarios by flow or potential operating constraints. No theorem asserts a new generic energy, confluence, quadratic-certificate, knapsack, or convex-graph mechanism. No implementation is claimed for the abstract exact algorithms.

## Source reading and citation checks

Read the ten required result statements and the three included supporting notes. Read the detailed tree/global-rank and cactus geometry arguments, and relevant historical second reviews of signed paths, fixed support/global rank, weighted-flow restoration, cactus flow geometry, quadratic region convexity, and the nonlinear-power extension. These are leads and audit aids; the manuscript has self-contained proofs and cites no repository note as theorem authority.

Primary literature was checked directly:

- Levi, Perakis, Romero, *A continuous knapsack problem with separable convex utilities*, ORL 42 (2014), pp.367–373: local full text and original PDF p.2/printed368, Proposition1. It uses the classical convex endpoint-forcing Subset Sum mechanism (with a different separable objective). DOI 10.1016/j.orl.2014.06.007. Credited at the reduction.
- Del Pia, Dey, Molinaro, *Mixed-integer quadratic programming is in NP*: local full text and original PDF p.3, Section2.2/Theorem3, explicitly credit Vavasis. The local manuscript is dated October 10, 2018. Primary author/institution records verify journal publication in Mathematical Programming162, 225–240 (2017), despite the local package's 2016 identifier. The bibliography distinguishes the version and gives DOI 10.1007/s10107-016-1036-0.
- Vavasis, *Quadratic programming is in NP*, IPL36(2), 73–77 (1990): official publisher abstract and author publication record verified title, year, theorem scope and DOI 10.1016/0020-0190(90)90100-C. No full-text reading is claimed; the necessary bounded-polytope lemma is proved in this section and the modern primary restatement is inspected.
- Labbé, Plein, Schmidt, local author manuscript, Section5 (tree chapter; Lemmas13–14 and Theorem20): checked tree cut formulas and the ordinary pairwise nomination predecessor. S4a uses the author-manuscript locator explicitly. The original accepted-section citations were not modified.
- Aßmann, Liers, Stingl, Vera, local arXiv-v1 manuscript, Sections4.2–4.3.3: checked tree coefficient-linearity and cycle-interval linearization, particularly Lemma4.10. These are credited as prior positive mechanisms.
- Wang and Hasler, *Convexity of Resistive Circuit Characteristics*, local full text and original report, Theorem 4, p.13 and conclusion p.21: source-variable scalar transfer convexity, with other-parameter extensions proposed as further work. This is different from full-vector convexity under resistance variation. The report is available; no stale access gap is repeated. The local package labels it 1997, but the inspected PDF has no verified date and the official handle returned 429. Following the lead's same metadata finding, the bibliography conservatively cites an undated EPFL report. The unresolved date is bibliographic, not a proof dependency.
- Brandenberg and Stursberg, local August16, 2023 preprint of the2025 JOTA article: Definitions1–2 and Theorem18 (not the published numbering in older notes), concerning linear differential-flow polytope nondegeneracy. Original PDF and full text were checked. The bibliography records preprint locators and published DOI 10.1007/s10957-025-02792-4. The theorem is a structural comparator, not a proof dependency.

The separate Hasler–Wang 1993 nonlinear-tolerance paper remains unread, which prevents an unrestricted publication-priority claim. The manuscript states that limitation without conflating it with the now-inspected convexity report. Existing source conventions for SRS and the real-algebraic primitives remain those established in accepted sections.

## Validation

`completion-s4a-checks.json` records the interpreter, script hashes, return codes, and full output for ten existing scripts. All passed using `/home/sgusev/miniconda3/envs/minlp-notes/bin/python`. Their imports/source references were checked before execution.

| Check | Distinct evidence |
| --- | --- |
| `check_signed_path_adjoint.py` | 192 signed paths, 32 returning paths, 275 zero coefficients, 3394 exact threshold checks. |
| `check_weighted_nomination_tree_review.py` | 100 complete capped-simplex optimizations, 1751 exact vertex states, 2000 mixtures, half-unit gap and rounding. |
| `fixed_support_global_rank_checks.py` | 12 graphs, 48 paths, 4 returning paths, 506 threshold levels, 36 balanced gradient checks. |
| `fixed_support_weighted_tree_checks.py` | 3119 stationary candidates, 30 exact contractions, 4 degenerate QP controls. |
| `weighted_arc_cycle_rank_hardness_checks.py` | 3 symbolic identities, 3 exact theta states, 1778 scenarios/40 instances, 43 target subsets. |
| `weighted_arc_unit_cost_checks.py` | 62 unit-cost DAG scenarios: counts, positivity, balances, objective and integer data. |
| `weighted_potential_cycle_hardness_checks.py` | 3 symbolic identities, 3 rational triangle states, 1776 scenarios/44 instances, 68 target subsets. |
| `weighted_tree_sign_pattern_checks.py` | 2818 stationary candidates, 148 exact cut-direction counts. |
| `check_weighted_tree_characterization_second.py` | 192 exact subdivided states, 144 negative controls, 98 exact restoration bounds. |
| `cactus_uncertainty_hulls_checks.py` | 3 exact theta states, 18 cactus grids, 18 coordinate sweeps, restored-edge gaps. |

These checks provide exact identities and numerical regression evidence as stated; they do not prove the universal theorems or implement the abstract bit algorithms. No redundant new suite was added.

Built only Paper A by importing `verification/build_and_check.py` and invoking `build('complexity')`. Final `completion-s4a-build.json` records all current manuscript input SHA256 hashes: return code 0, no LaTeX errors, undefined references, undefined citations, duplicate labels, or overfull boxes. The first build's six overfull boxes were removed by normal prose/math reflow; the final build is clean. Paper B was not built.

## Remaining work and boundaries

No known missing proof or unresolved mathematical issue remains within the asserted S4a scope. Five independent stage reviews and a distinct correction agent are still required before acceptance; this report does not close that gate. The author did not request or spawn reviewers.

S4b still owns weighted-cactus accuracy-bit compilers and general bounded-block-rank nomination faces. Later stages retain correlated design/performance, source-priority closeout, introduction/conclusion/abstract, and final whole-paper framing. The qualitative power-law theorem supplies no extra algorithmic conclusion, and exact cactus scalar-value comparison is deliberately not conflated with exact scenario search. Optional figures can be added during final framing after the mathematics is stable.
