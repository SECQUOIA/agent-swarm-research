# Stage 6, round 1 — independent review 5

## Verdict

**One major experimental-control issue and one minor reproducibility issue need correction.** The changed exact flat-chain implementation passed my code review and independent checks. The published raw measurements are internally consistent and faithfully rendered; the major issue is an omitted elementary fixed-weight LP baseline that materially changes the optimization comparison, not fabricated or incorrectly summarized measurements.

## Findings

1. **R5-S06-01 — major: exploit fixed weights in the joint full/global optimization baselines.** Locations: `code/network_simplex_benchmarks/strong_baselines.py`, `optimize_ef`, especially lines 42–78; computation subsections “Baselines that retain the elementary reductions” and “Size savings and runtime tradeoffs”; optimization tables. All three measured optimization cases fix every simplex weight. Nevertheless, the full/global builder constructs variable-weight balance and capacity rows, retains all fixed `y` columns and the simplex row, and leaves every scaled capacity as a general inequality. With fixed weights, the same classical disaggregation can instead use just state-flow variables, `A f^j = lambda_j b`, and native variable bounds `0 <= f^j <= lambda_j u`. Original `y` objective terms become a constant; additional original-coordinate rows are mapped with their fixed `y` contribution moved to the right-hand side. Global state merging remains exact. This is one joint sparse LP, so it does not incur the repeated solver-call overhead of the included independent-network baseline, and it remains valid for the aggregate-budget case.

   I implemented this direct formulation independently in `verification/reviewer5/stage06-round01/check_fixed_y_baseline.py`, using the frozen instances, saved objective vectors, fixed weights, and coupled row. After one warmup and five rotated runs, all objectives agreed within `1e-7`. Median total milliseconds were:

   | Case | Current global | Constant-weight global | Initial compression |
   |---|---:|---:|---:|
   | Original sparse instance | 6.86 | **3.53** | 5.94 |
   | Same instance with budget | 6.38 | **5.08** | 6.48 |
   | All labels observed | 62.62 | **32.57** | 10.68 |

   The constant-weight full builder likewise reduced medians from 36.49 to 20.04 ms, 51.05 to 33.65 ms, and 56.75 to 32.04 ms in the three cases. Raw runs, ranges, objectives, and actual model sizes are in `check_fixed_y_baseline.json`. These are reviewer diagnostic measurements on the shared host, not proposed replacement publication values.

   Add this elementary full/global fixed-weight baseline to the official protocol (or use it as the fixed-weight branch of the strengthened baselines), verify its original-coordinate reconstruction and coupled-row mapping, rerun the relevant comparisons, and update the tables and interpretation. Keep the current free-weight API for cases in which weights really are variables. The all-labels-observed control still supports a graph-local benefit in my check, but the original-case “similar total times” narrative understates the advantage of a simpler global formulation, and the size/time gains over full disaggregation are overstated by avoidable variable-weight machinery. I classify this as major because it affects the paper's central practical comparison and requires new official experimental results and interpretation, rather than a local prose repair. The existence of LP presolve does not resolve the concern: the measured direct formulation is materially faster despite solving the same LP projection.

2. **R5-S06-02 — minor: the table generator does not actually verify the complete case grid.** Locations: `verification/stage06-tables.py`, lines 10–17; the manuscript's reproduction paragraph and the same claim in the author/README documentation. The script verifies list lengths and recomputes summaries, but it does not verify the distinct `(length, weight regime, feasible/infeasible)` flat cases, membership state counts, optimization case identities/order, or expected method coverage. In a private copy I replaced one flat case by a duplicate of another, retaining 16 records but only 15 distinct cases. The generator still printed `PASS` and generated five tables. This counterexample is retained in `verification/reviewer5/stage06-round01/grid-check.json` and its private `grid-check/` directory. The actual frozen data have the correct complete grid, which I independently verified. Add explicit set/count checks and the required optimization-name/order and method checks, so the documented validation is real. This is minor because no present published number or actual case is missing.

## Code and mathematical checks

Read the new flat-chain implementation, both changed test files, the strong baseline module, benchmark driver, API documentation, manuscript README, table generator, author record, and validation manifest. Checked the accepted mathematical interfaces used by them.

The flat implementation correctly groups only globally observed labels, merges all others, eliminates the residual profile, and retains exact original-domain checks. Its zero-row handling and fixed small-label circuits agree with the accepted formulation. The one- and two-label recovery formulas do not construct a library. General recovery enumerates unrestricted full-rank reduced bases, correctly allowing positive residual branch flow. The two three-label bypass repairs have the correct sign under the code's `cut <= 0` convention. Compact flow recovery and the compatibility accessors correctly distinguish grouped weighted entries from normalized original-state flows, including zero weights and a zero observed-label count.

The existing strong full/global optimization formulations are mathematically correct, including preservation of all original `y` objective and constraint contributions when weights are genuinely variable. My major finding concerns their unnecessary use of that representation when all weights are fixed. The point-membership two-state reduction correctly intersects both scaled capacity bounds and all fixed observations, removes exactly zero-weight states, and handles one positive state directly. Its tolerance-based aggregate balance check and numerical LP statuses are accurately distinguished from exact membership certificates.

The fixed-weight objective factorization and the aggregate-budget limitation are correctly explained. The two-supplier transportation application has the stated underlying parallel-path graph despite one reversed traversal per path. It assumes common balances and capacities and does not incorrectly extend component-hull exactness through arbitrary added side constraints.

## Independent checks actually run

- Rehashed **all 82 frozen external dependencies** in the validation manifest; every hash matched.
- Independently recomputed **483 timing summaries**, checked **515 timed method statuses**, and checked all actual flat, membership, and optimization case identities. All passed.
- Reproduced all **five generated table files byte-for-byte** in a private directory before performing the intentional grid mutation described above.
- Reran the combined test command: **21 tests passed**.
- Wrote `check_flat_independent.py`, which imports the production interface but independently constructs the complete path–simplex vertex hull. Across **96 queries** with 7–11 original labels and 0–3 observed labels, all numerical vertex-hull comparisons agreed. Verified **69 decompositions exactly** against original arc bounds, balances, aggregates, observations, and original weights. Verified **27 exact violated unit-coefficient cuts** against **1,664 exact original hull vertices**. Cases include zero residual weights and multiple unused positive global states.
- Ran the independent fixed-weight baseline comparison described in R5-S06-01. Its objective and constraint substitutions were checked directly, and every measured objective agreed with the frozen official optimum within `1e-7`.

## Scientific interpretation and coverage

Apart from the missing fixed-weight joint baseline, the section is candid and useful: it preserves negative findings, distinguishes global from block-local reductions, includes the all-labels-observed and coupled-budget controls, and reports the reversal of the previous boundary-face flat-chain speedup. It does not imply industrial validation, persistent-callback superiority, native-code optimality, exact LP optimality, or peak-memory measurements. The data clearly distinguish membership-only and decomposition-inclusive exact queries. Warmup exact audits and numerical global-support audits are identified as such; I found no claim that every floating-point optimum is an exact optimality certificate.

The changed code implements the important new manuscript developments rather than merely describing them. Historical source and audit references are preserved, and the rational-reconstruction adapter's restricted purpose is clear. No additional mathematical result appears necessary for this stage beyond resolving the experimental comparison.

## Build and presentation

Built a private copy of the snapshot. It produced a **45-page PDF** with no final warnings, unresolved references/citations, or overfull/underfull boxes. Visually inspected pages **40 and 42**, covering the optimization and flat-chain tables and their surrounding explanations. The tables are legible, captions identify their workloads, and the layout fits the page.

## Limitations and independence

The reviewer timing comparison is a controlled diagnostic on a shared host; the official study should rerun the strengthened methods under its own recorded protocol rather than copy these times into publication tables. I did not rerun the entire official long benchmark or every historical audit, establish literature priority, or independently verify every publisher metadata field. I did not read other current-round reports, coordinate findings, spawn agents, or edit manuscript/production sources. All generated evidence and intentionally altered test data are confined to the assigned reviewer directory.
