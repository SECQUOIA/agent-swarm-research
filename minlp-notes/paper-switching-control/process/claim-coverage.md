# Definitive claim coverage and development map

Every substantive CIA result file in results/ and every distinct development
in its investigation notes has a disposition below. The inventory is
process/stage06-repo-inventory.txt. Historical derivations, search failures,
and repeated reviews are evidence, not additional theorems. Earlier candidate
notes are retained in stage06-coverage-before.md; their final disposition here
supersedes provisional language. Stages 1–6 are accepted in their process
records. The separate whole-manuscript five-reviewer cycle is also complete;
see stage07-acceptance.md for final acceptance.

Locators are stable LaTeX labels in the indicated section files. The higher
reach material formerly in the second half of07-predecessors-and-frontier.tex
is preserved verbatim in14-higher-reach.tex and appears as an appendix.

| Repository result/development | Final manuscript disposition and precise locators |
| --- | --- |
| cia-uniform-switching-obstruction | 02-uniform-one-switch: thm:uniform, thm:uniform-grid, thm:one-switch, cor:one-switch-grid, prop:three-cells, ex:five-mode-conjecture, ex:three-cell-conjecture. Includes repeated competing modes, recurrence and refinement obstruction. |
| cia-exact-two-switch-worst-case | 03-heavy-and-reach: thm:reach-three;05-small-budget-minimax: thm:small-one-sided,thm:small-full,eq:two-switch-exact,eq:two-switch-expansion. |
| cia-two-switch-equal-masses | 05-small-budget-minimax: cor:equal-masses; distinct smaller equal-total guarantee retained. The all-light result gives an additional exact instance band in07. |
| cia-universal-heavy-mode-rounding | 03-heavy-and-reach: lem:prefix-repeat,lem:first-repeat,thm:heavy,thm:one-sided-reduction; arbitrary horizon and measurable-input treatment retained. |
| cia-general-four-block-reach | 04-four-block-certificates: thm:reach-four,lem:weighted-pair; subsec:event-lp,subsec:pair-symmetry,subsec:pair-certificates. Complete necessary LP,10 types,179 finite and10 polynomial all-n certificates. |
| cia-five-mode-four-block-reach; earlier n4 three-block certificates | Explicitly subsumed by the analytic three-block and all-n four-block theorems. Independent historical exact checks retained unchanged in verification/reference. No duplicate main theorem or weaker competing claim. |
| cia-exact-three-switch-worst-case | 05-small-budget-minimax: thm:small-full,eq:three-switch-exact,eq:three-switch-expansion; n5–11 plateau and n>=12 uniform regime. |
| cia-distinct-reach-investigation | 05-small-budget-minimax: prop:three-mode-failure strengthened to an exact all-word one-sided instance optimum18673/18396, with analytic lower proof and matching021 schedule. It is not an exact minimax value. |
| cia-adjacent-repeat-investigation | 05-small-budget-minimax final two subsections retain the prescribed-heavy and fixed-pair-position counterexamples. Largest-heavy adjacent-pair strengthening is explicitly unproved and unused. |
| cia-three-switch-heavy-mode | Specialized heavy proof subsumed by thm:heavy. All-light lemma and extra consequences retained separately in07: lem:all-light,cor:light-boundaries. |
| cia-two-switch-global-upper | 07: lem:third-mass retains input-dependent sufficient condition and separating example. Older global rational coefficient is explicitly dominated by the exact final theorem. |
| cia-three-switch-global-upper | 07: prop:analytic-four-upper,eq:analytic-four-gap retain the certificate-free predecessor, n5–11 plateau, asymptotic comparison. |
| cia-arbitrary-block-one-sided-bound | 06-general-budgets: lem:mode-removal,thm:general-coefficient,cor:general-bounds. Both terminal-mass choices and constant-mode branch proved. |
| cia-arbitrary-switch-global-bound | 06: cor:general-plateau,prop:general-asymptotics,eq:sharp-first-correction; full and equal-mass consequences distinct. |
| cia-seeded-arbitrary-switch-bound | 06: thm:seeded,cor:seed-consequences,prop:seed-series. Negative seed is not clipped; extra n16 four-switch plateau and exact integer plateau test retained. |
| cia-many-mode-switching-investigation | 07: prop:dimension-free and attributed eq:classical-small-mode.14 appendix: lem:general-exclusion pinpoints the unproved weighted premise. No general five-block claim. |
| cia-reopened-general-reach | 14 appendix: subsec:negative-relaxation,eq:negative-event-objective retain exact nonphysical witness; lem:event-interpolation proves chronology criterion; prop:chronological-chamber adds a complete exact primal/dual result for ONE stated chamber. Other chambers remain open and unused. |
| cia-finite-grid-one-switch-minimax; cia-reopened-finite-grid | 08: thm:finite-one includes both LP families, full reduction/elimination, O(N²) rational formula and compressed extremizers; ex:five-nine is independently proved; failed nonuniform simplification retained. |
| cia-exact-three-mode-one-switch | 08: cor:three-unit-one covers all residues and matching constructions, plus N1 exception; subsumed by general formula but explicit useful specialization retained. |
| cia-five-interval-two-switch-minimax; cia-reopened-small-grid-boundary | 09: thm:five-cells; original14,400-history/243-word checks retained, with new complete floor automaton proof. Published Corollary5 correction preserves source attainment restrictions. |
| cia-fixed-switch-budget-algorithm; cia-reopened-practical-algorithm | 10: thm:linear-one-switch,lem:final-residual,prop:subset-DP,thm:fixed-budget,lem:candidate-labels. Dominance, three candidates, eligible boundaries, fixed initial mode, crossing queries, signed residuals, repeated modes, unused modes, bit/space complexity, and dwell on maximal runs all retained. No transition-graph extension or FPT-in-budget-alone claim. |
| cia-sharp-grid-transfer; cia-reopened-grid-transfer | 11: thm:sharp-transfer,cor:opt-transfer,prop:binary-transfer,prop:transfer-sharpness. Full chronology proof, strict instance AND minimax upper transfer, sharp m-cycle family and precise source-half-grid distinction. |
| Public profile computations | 12: eq:public-continuous,tab:public-profile,tab:public-certificates. Fresh pinned input, normalized/quantized error bounds, same-grid budgets0–3 on M12/24/48, fine12,000-cell one-switch solve, independent all-pair/boundary checks and direct schedule evaluation. Old runtime values replaced by fresh samples. |
| Readiness/novelty/literature notes | 00 introduction,13 discussion, bibliography and stage04/05/06 source records. Established CIA/flow/DP/dwell/state-error tools credited. No unsupported priority, state-performance, or solver-superiority assertion. Genuine research questions separated from complete results. |

## Further developments completed while writing

- Foundations: attained continuous and finite-grid extrema, exact cell averaging
  for every grid schedule, and continuous-minimax domination by grid minimax.
- Three-mode one-sided structural example: exact all-word optimum, not merely
  failure of a distinct-word construction (05,prop:three-mode-failure).
- Equal-mass exact INSTANCE band `(n-k)^2<=k` (07,cor:light-boundaries).
- Exact chronological realizability criterion and ONE ordered chamber bound
  (14,lem:event-interpolation and prop:chronological-chamber).
- Complete all-N three-mode floor-history realization by averaging integral
  paths (09,prop:floor-automaton), beyond a finite numerical chamber search.
- Exact continuous F3,2=T/5, exact six-cell/three-switch value1, and exact
  seven-cell/three-switch value4/3 with all exceptional repairs and matching
  witness (09,cor:three-two-continuous,cor:six-cells,thm:seven-cells).
- The failed2s+1-cell unit-error extension is resolved by the seven-cell theorem.
  Continuous F3,3 remains in the explicit proved bandT/7..T/6.
- Continuous rational word/time-cell LP benchmark, including k>N, repeated and
  zero-duration modes, degeneracy, exact vertex enumeration (10, final subsection).
- Strict minimax transfer through an attained grid maximizer, exact additive
  coarsening with nonaligned input integration, nested fine-grid scope, input
  perturbation, and explicit dwell-refinement failure (11,cor:opt-transfer,
  thm:certified-coarsening,cor:coarse-perturbation,ex:dwell-grid-gap).
- Explicit classical small-mode comparison attributed to Zeile–Robuschi–Sager
  Corollary1 (07,eq:classical-small-mode). This is a sourced consequence, not a
  new unrestricted CIA bound or claimed hard-budget tightness result.
- Exact continuous public one-switch optimum4721469/2500000, independently
  evaluated affine crossings and attained schedule; fine-grid gap1031/2500000.
  Uniform n3/s2 continuous1/6 benchmark proved directly and coarse values
  independently enumerated (12).
- Reproducible matched-method and fixed-budget scaling measurements, exact
  derived-data/table validation, PDF figures, and complete offline runner.

## Remaining open directions: no theorem depends on them

General five-block reach and exact higher-budget finite-mode minimax; exact
continuous F3,3; a general floor-history switch law beyond the enumerated
lengths; the largest-heavy adjacent-pair strengthening; transfer/coarsening
under arbitrary dwell or coupled transition constraints; broader matched
solver comparisons and actual nonlinear trajectory/objective performance.
No unsuccessful search, relaxed LP witness, timing sample, or conjectured
identity is promoted to a proved assertion.
