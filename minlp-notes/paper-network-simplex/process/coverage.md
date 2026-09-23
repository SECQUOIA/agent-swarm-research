# Source-to-manuscript coverage

This map includes retained developments and informative limitations. Historical
experiments need not be duplicated when stronger evidence supersedes them, but
their conclusions must not be lost. Acceptance requires manuscript locators.

| Source | Required coverage | Stage | Manuscript locator |
|---|---|---|---|
| `notes/common-factor-network-simplex.md`, literature audit | Model, known disaggregation, direct predecessors, equality-network scope | 1 | Sections 2–3; `prop:disaggregation`, `lem:block-factorization`, `thm:block-state-reduction`; accepted Stage 1 |
| `notes/network-simplex-reopened-compressed-hull.md` | Reference flow, block independence, path suppression, active-state merging, row/variable/encoding bounds | 2 | Section 4, `thm:cycle-compression`; accepted Stage 2 |
| `notes/network-simplex-observed-rank-elimination.md` | TU pivot proof, unobserved-cycle count, forest criterion, minimum coordinate completion with ambient-space caveat | 2 | Section 4, `thm:observed-compression`, `cor:forest-hull`, `prop:minimum-completion`; accepted Stage 2 |
| `results/network-simplex-cycle-theta-hull.md` | Explicit interval and six-support formulas, branch cuts, unit coefficients, compact recovery, joint-state example | 3 | Section 5, `thm:theta-hull`, `prop:theta-recovery`, `ex:joint-theta`; accepted Stage 3 |
| `results/network-simplex-parallel-path-hull.md` | All subset cuts, transportation proof, max-flow separation, coefficient and complexity distinctions | 3 | Section 5, `thm:parallel-hull`, `subsec:parallel-oracle`; accepted Stage 3 |
| `results/network-simplex-bounded-rank-hull.md` | Uniform support library, degeneracies, coefficient bound, separation complexity, exact sharp K4 section | 4 | Section 6; `thm:bounded-rank`, `thm:rank-recovery`, `lem:section-facet`, `cor:rank-three-sharp`, `rem:seven-product-k4`; accepted Stage 4 (includes new recovery and five-product example) |
| `results/network-simplex-universality.md` | Precise imported transportation theorem, layer-one map, network section, unit normalization, facet transfer | 5 | Sections 7; `thm:universality`, `cor:universal-coefficients`; accepted Stage 5 |
| `results/network-simplex-series-parallel-coefficient-growth.md` | Balanced-incidence lemma, Fibonacci family, sparse encoding, ambient facet restriction, simple degree-three realization | 5 | Section 8; `lem:balanced-incidence`, `thm:fibonacci`, `cor:fibonacci-simple`; accepted Stage 5 |
| `notes/network-simplex-reopened-series-parallel.md` | Informative failure of scalar-profile composition and earlier construction as appropriate | 5 | Section 8; `ex:small-sp`, `rem:scalar-failure`, dense-variant paragraph; accepted Stage 5 |
| `results/network-simplex-flat-chain-fixed-states.md` | Arbitrary observations, exact shared profile, subset rows, circuit bound and construction, state-dependent coefficients | 5 | Section 9; `prop:chain-profile`, `thm:fixed-chain`, `thm:two-state-chain`, `thm:three-state-chain`, `cor:chain-observed-labels`; accepted Stage 5, including reduced profile and sharp observed-label threshold |
| `code/network_simplex/`, `code/network_simplex_compressed/` | Implemented scope, exact/numerical certificate semantics, completeness/recovery, reproducible commands | 6 | `sec:computation`, `tab:implemented-scope`, certificate semantics and reproducibility subsections; accepted Stage 6 |
| `notes/network-simplex-reopened-computation.md`, benchmark JSON | Independent full EF, compression variants, cuts, repeated timing, model sizes, negative runtime findings, fair baselines | 6 | `sec:computation`, `tab:computation-opt`, `tab:computation-member`, `tab:computation-flat`, `tab:computation-ablations`; corrected native fixed-weight baselines and all-labels-observed control; accepted Stage 6 |
| `notes/network-simplex-reopened-literature.md` | Attribution of RRLT, Cayley/min-cut, fan geometry, general large coefficients and restricted multiflows | 1–7 | `subsec:prior-work`; `subsec:parallel-oracle`; `sec:bounded-rank`; `sec:universality`; `sec:sp-growth`; `sec:computation` transportation interpretation. Fiorini facet-transfer comparison added in Stage 7; precise published KD companion and equality representation retained. |
| `notes/network-simplex-reaggregation-source-boundary.md` | Homothetic merging assumptions; common matrix alone insufficient | 1 | `ex:merger-boundary`; accepted Stage 1 |
| All independent review notes and final validation | Proof corrections carried over; finite computation distinguished from proof and novelty | All | All retained proofs incorporate accepted corrections; `sec:computation` separates exact certificates from numerical comparisons; stage validation manifests and acceptance records retain full checks, negative results, and review outcomes. Final-stage and whole-manuscript review status is recorded in `PROCESS.md`. |

## Root observations before Stage 1 review

- The current practical comparisons include model construction. Stage 6 must
  strengthen the known-zero-state baseline rather than leave an easily removable
  weakness as an unexplored caveat. Persistent-model comparisons are needed only
  if a callback performance claim is retained.
- Fixed-state nested series–parallel graphs and sharp higher-rank constants are
  outside existing proved scopes. A complete paper may state these as boundaries;
  it must not silently infer them from flat chains or growing-state examples.
- Coefficients on flow/product coordinates and data-dependent simplex
  coefficients require distinct statements. A finite unit-coefficient description
  does not mean primitive integer normalization preserves that bound.
- General transportation universality requires an explicit source check for the
  first-layer coordinate injection, not only a citation to the theorem title.

## Final integration coverage

The introduction and `tab:structural-scope` distinguish the exact residual-coordinate
count of the construction from extension-complexity optimality, and foreground
the sharp three-observed-label flat-chain threshold. `cor:integral-flows` records
the classical integral-data hull equality with its decomposition-size limitation.
`fig:flat-chain` depicts the shared state profile. `sec:conclusion` reconciles the
positive and negative coefficient results and the corrected practical evidence.
The final README identifies historical closeouts and superseded benchmark claims;
short pointers in the old readiness and continuation records preserve their
original content while directing readers to the manuscript.
