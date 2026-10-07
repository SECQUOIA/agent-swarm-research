# Protocol: campaign v3 (fixed before any v3 run)

Written 2026-10-03 for the paper. It answers three questions that the
earlier campaigns could not: does the corrected implementation change the
comparison on the v2 holdout when runs are longer and repeated; does the
method help on models that actually contain the structure it targets; and
how often does that structure occur. Campaign v2 and the repair cohort
remain separate records and are not replaced.

## Code

The live code in `research-20261003-convexification/solver` and
`research-20261002-convexification/solver` (repaired discovery; SHA-256 of
`solver/integration.py` 128fe10b...), snapshotted before the first run. The
frozen `Config` defaults are used for `all` and `auto`. No parameter is tuned
on v3 outcomes. SCIP 10.0.2 through PySCIPOpt 6.2.1.

## Part S: structural scan (no optimization)

Pool: the 422 models of `research-20261003-convexification/experiments/
holdout-selection.json` (`eligible_names_in_rank_order`), minus the 30 v2
holdout models. For each model: read, build the common model, and run block
discovery only (`discover` with the frozen `Config`), with a 60 s deadline.
Record admission status, number of admitted blocks, their dimensions,
numbers of nonlinear sides and affine domain rows, quadratic or not, and
whether the frozen `auto` rule admits the block. Report counts for the whole
pool and by stratum. No solver bound is computed.

## Part A: v2 holdout, corrected code, longer and repeated

The 30 v2 holdout models. Modes baseline, all, auto. Full runs: soft budget
300 s (hard process limit 360 s), seeds 0, 1, 2. Root runs: node limit 1,
60 s, seed 0, modes baseline, all, auto and `all-diag` (below).

## Part B: structure-selected sample

From the Part S pool, a model qualifies if it is admitted and discovery
finds at least one block that the frozen `auto` rule admits. Rank qualifying
models by SHA-256 of `convexification-structure-v3:` + name and take the
first 30 (all of them if fewer qualify). Modes baseline, all, auto. Full
runs: 300 s (hard 360 s), seeds 0 and 1. Root runs as in Part A.

## Part C: mechanism family

As in `mechanism-protocol.md`.

## Mode `all-diag` (root runs only)

`all` with raised work limits: max_blocks 128, max_cuts 200,
max_cuts_per_round 50, max_rounds 10, max_support_calls 500,
max_separation_seconds 30, separation_budget_fraction 0.5. It measures
whether the frozen limits, rather than the cuts themselves, bound the root
effect. It is not a deployable setting.

## Execution

Each job is one (model, phase, seed); within a job the modes run
sequentially in a rotated order, so that the modes of one comparison see
similar host load. At most six jobs run in parallel, each single-threaded
(SCIP and BLAS). The host is shared with unrelated work; per-run load is
recorded at start and end. Every job and every failure is reported.

## Metrics

- Solved: optimal or gap-limit status with an incumbent that passes the
  independent original-model check (scaled tolerance 1e-5).
- Times: shifted geometric mean (shift 1 s) over models solved by all
  modes, per seed and pooled; per-model time ratios.
- Bounds: paired final and root dual-bound comparisons at relative
  tolerance 1e-4 (the gap limit), and also 1e-6 for comparison with v2.
- Cuts: counts, methods, replay of every recorded cut against the archived
  original model and the stored SCIP row, with tampering controls.
- A/A variation: seeds of the baseline.
