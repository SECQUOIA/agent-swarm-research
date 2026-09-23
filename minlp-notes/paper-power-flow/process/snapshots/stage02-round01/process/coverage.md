# Source coverage map

This map distinguishes manuscript coverage from repository history. It is an
initial inventory at stage 1; later authors should update the pending entries.
Paths below are relative to the repository root unless stated otherwise.

| Repository source | Material relevant to this paper | Manuscript destination/status |
|---|---|---|
| `results/ac-power-flow-existential-reals.md`, Theorem 1, Sections 1 and 3 | Exact RPF model; membership; complement paths; addition and inversion; both reduction directions; degree and fixed numerical data | Covered in sections 01–02; exact counts and rational-homeomorphism statement made explicit |
| Same result, Theorem 2, Sections 1–2 | AC model; rational-cosine encoding; real-angle lift; winding count; zero reactive injections; rectangular angle box | Covered in section 03, with explicit series/shunt signs, all limits below pi, determinant crossing rule, and componentwise references |
| Same result, Corollary 3, Remarks 5–6 | Conditional NP obstruction; arbitrary algebraic degree; unique magnitudes | NP consequence covered in section 02; full algebraic-degree development stage 3 pending |
| Same result, Remarks 1–4 | Physical interpretation, loads-only comparison, angle range, lossless and tree distinctions | Exact model distinctions partly covered; stages 2–4 pending |
| Same result, Section 5 | Legacy numerical checks and exact winding evidence | Stage 4 supplement pending; new exact original-network checks supplied in stage 1 |
| `notes/review-power-flow-existential-reals-A.md` | Initial angle-semantics failure; explicit cycle counterexample; rational input; repeated copies; free-injection bounds; degree; numerical timeout limitations | RPF corrections incorporated in sections 01–02; AC counterexamples and model distinctions covered in section 03; numerical history stage 4 pending |
| `notes/review-power-flow-existential-reals-B.md` | Independent original-network exact checks and reduction audit; angle issue and follow-up | RPF proof checked; AC real-lift distinction and corrected transfer covered in section 03 |
| `notes/review-power-flow-existential-reals-C.md` | Corrected AC membership; unequal magnitudes; half-open crossings; attribution; optional angle extension | Section 03 proves a scale-independent determinant rule and extends membership to every rational cosine in (-1,1]; independent geometric checks include long arcs and axis endpoints |
| `notes/review-existential-reals-closeout.md` | Final scope corrections; singleton/coordinate-degree dependence; finite-check limits | Stage 1 complexity and verification language corrected; stages 2–4 pending |
| `notes/power-flow-existential-reals-novelty.md` | Detailed primary-literature comparison and search history | Stage 4 pending; do not repeat its broad absence claims or infer exact P from an LMI characterization |
| `code/power_flow_existential_reals/dc_resistive_build_and_check.py` | Original construction; per-bus free bounds; numerical QCQP and rectangular AC experiments | Read and compared; paper-local checker independently builds fixed-85 version and has no Gurobi dependency; numerical supplement stage 4 pending |
| `code/power_flow_existential_reals/check_winding_count_exact.py` | 360 scaled line pairs; 4,136 cycles; axis/reversal and winding regressions | New standalone `checks/check_ac_exact.py` covers determinant crossings, unequal scales, negative cosines, 177,168 cycles against a rotated cut, and 648 AC sign checks; legacy evidence stage 4 pending |
| `results/pooling-existential-theory-of-reals.md`, algebraic-degree corollary | Shared ETR-INV rational-equivalence and coordinate-projection argument | Stage 3 pending; make the power-flow consequence self-contained rather than cite pooling manuscript |
| `notes/pooling-existential-reals-novelty.md` | Shared source/complexity survey and Bienstock–Verma discussion | Stage 4 pending; no separate power-flow theorem |
| `notes/open-problems-from-literature.md`, entry 11 | Bienstock–Verma approximate NP question | Stage 3 pending; distinct model and approximation semantics must be stated |
| `notes/log.md`, power-flow entries near lines 1039–1092 | Chronology of authoring, failed angle semantics, corrections, audits | Historical duplicate; no additional result to promote |
| `notes/reopened-run-status.md`, power-flow entry | Summary of completed result | Historical duplicate |
| `notes/research-continuation-assessment.md` | Research-priority assessment | No additional theorem; paper need not reproduce prioritization |
| `notes/research-continuation-closeout.md` | Scope and evidence reconciliation | Historical duplicate of closeout; checks relevant to stage 4 |
| `notes/potential-flow-global-correlation-novelty.md` | Incidental reference to stochastic power-flow literature | No exact power-flow-feasibility development; out of mathematical scope |

## Primary-source dependencies

The local `literature/AGENTS.md` was read. Literature files were not changed.
Page locators refer to page markers in archived full text and, where indicated,
the original PDF. Preprint and journal numbering must not be silently conflated.

| Source | Verified material / intended use | Status |
|---|---|---|
| `literature/papers/abrahamsen2022-the-art-gallery-problem-is/` | Archived STOC/arXiv copy, Definition 5 and Theorem 7, p.11; ETR-INV variable interval and all three equation forms | Text read; original PDF p.11 visually checked; stage 1 cited explicitly with version qualification |
| `literature/papers/abrahamsen2019-dynamic-toolbox-for-etrinv/` | Complexity conventions p.1–2; Theorem 1 p.3; rational equivalence and linear extension, Definitions 4–5 p.4 | Read; conventions cited in stage 1; universality and degree stage 3 pending |
| `literature/papers/schaefer2024-the-existential-theory-of-the/` | Complexity definitions, current broader comparison, ETR-INV | Stage 4 pending |
| `literature/papers/bienstock2019-strong-np-hardness-of-ac/` | Lossless fixed-magnitude model p.1; approximate NP discussion p.6 | Stage 3/4 pending |
| Gan–Low 2014, *Optimal power flow in direct current networks* | Provenance of resistive model; exactness regimes | Stage 4 primary-source verification pending |
| Lavaei–Low 2012, *Zero duality gap in optimal power flow problem* | Appendix B, Case 2; scope of zero-reactive reasoning | Cached primary PDF text inspected, Appendix B Case 2; section 03 uses a self-contained counterexample and does not import its discrete-phase assertion. Full literature comparison stage 4 pending |
| Dörfler–Chertkov–Bullo 2013, *Synchronization in complex oscillator networks and smart grids* | Oscillator equilibrium equation and cohesive-angle analysis | Cached primary full text read, Eq. (1) and supplementary Lemma 2; section 03 cites the equation/background only, not its global uniqueness assertion. Our real-lift lemma is proved independently |
| Jeeninga–De Persis–van der Schaft, DC power grids with constant-power loads, Parts I/II | Fixed-source loads-only feasibility characterization; precise relation to this model | Stage 3/4 primary-source verification pending |
| Lehmann–Grastien–Van Hentenryck, AC-feasibility on tree networks | Different hardness regime; input encoding distinctions | Stage 3/4 primary-source verification pending |
| Bienstock–Muñoz, LP formulations for polynomial optimization | Approximation with bounded structure and irrational exact solutions | Stage 3/4 pending if used |

New independent results developed during manuscript preparation belong in this
map as they are proved and reviewed. Stage 1 adds the explicit size bound,
exact rational homeomorphism (including unused variables), and license-free
original-network checker. Stage 2 develops and proves: membership for all
rational cosines greater than -1; an exact determinant crossing count;
the fundamental-cycle angle-budget criterion; strictly positive principal-only
windows with size-dependent polynomial-bit cosines; and the positive-width
one-sided reactive-interval corollary. These are draft results awaiting the
stage-2 independent review process. Structural and numerical extensions remain
for stage 3.
