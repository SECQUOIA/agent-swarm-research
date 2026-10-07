# Protocol: interleaved path family (fixed before any run)

Written 2026-10-03, before any run of this family with the cut separator.
A pilot of native SCIP alone (no separator) on the deterministic family with
all triples equal to the Proposition 6.1 example was run first, to check that
the family is nontrivial for SCIP; its results are recorded in
`pilot-native.md` and are not part of the results below.

## Purpose

Measure, on a constructed family where the theory predicts a gap, how much
of SCIP's root gap the certified block cuts close, and what that costs in
a complete solve. This is a mechanism study, not an application benchmark.
It is reported separately from the MINLPLib campaigns.

## Instances

For n in {10, 20, 40, 80} and seed in {0, 1, 2, 3, 4} (20 instances):

- Variables x_i, y_i, z_i in [0, 1] and t_i in [-10, 10], i = 1..n.
- For each triple draw four distinct values from {k/64 : k = 0..48} uniformly
  without replacement (Python `random.Random(1000*n + seed)`), sort them as
  t1 < t2 < t3 < t4, and set A = {t1, t3}, C = {t2, t4} or the reverse with
  probability 1/2. Orient each set randomly: (a1, a2) is A in random order,
  (c1, c2) is C in random order.
- Rows: D_i(x_i, y_i, z_i) - t_i <= 0 with
  D_i = (y - a1 - (a2 - a1) x)^2 + (y - c1 - (c2 - c1) z)^2 + x(1 - x) + z(1 - z),
  expanded into linear and quadratic coefficients (all dyadic, exactly
  representable in binary64), plus the coupling row sum_i y_i <= 0.8 n.
- Objective: minimize sum_i t_i.
- Known optimum: sum_i delta_i^2 / 2 with delta_i = min |s - t| over s in A_i,
  t in C_i (Theorem 6.2). The coupling row is not binding because every
  optimal y_i is a midpoint of two values at most 3/4.

## Modes

- `baseline`: native SCIP 10.0 through the common model builder.
- `all-diag`: the `all` separator with raised work limits: max_blocks = n,
  max_cuts = 4n, max_cuts_per_round = n, max_rounds = 10,
  max_support_calls = 20n, max_separation_seconds = 60,
  separation_budget_fraction = 0.5. All other settings are the frozen
  defaults. `auto` is not run: its frozen admission rule excludes these
  blocks (one nonlinear row and no affine domain row per block).

## Runs and metrics

- Root runs: node limit 1, time limit 120 s.
- Full runs: time limit 300 s, relative gap 1e-4.
- One SCIP thread, one BLAS thread, seed 0. Runs may execute in up to four
  parallel single-threaded workers on the shared host; timings are therefore
  descriptive.
- Metrics: root dual bound; root gap closed,
  (root_dual(all-diag) - root_dual(baseline)) / (opt - root_dual(baseline));
  final status, nodes, total time, separation time, number of cuts;
  independent original-model primal check of every incumbent; replay of every
  recorded cut against the original model and the stored SCIP row.
- All 80 runs are reported, including failures and timeouts.
