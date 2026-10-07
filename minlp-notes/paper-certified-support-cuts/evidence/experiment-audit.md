# E1: independent audit of the computational evidence (Reports A and B)

Audit date: 2026-10-03. Scope: the frozen campaign records of Report A
(`research-20261002-convexification/experiments/campaign-v1`) and Report B
(`research-20261003-convexification/experiments/campaign-v2` and
`repair-discovery-v1`), and every campaign number stated in the two
`document/evidence.tex` files, plus the generated `results.md` and `coverage.md` tables.
No solver was run. No file under `research-2026100*-convexification/` or `literature/`
was modified.

## Result

- **No mismatch.** The audit script runs 418 checks against the raw `records.jsonl`
  files (and the job lists, selections, manifests, snapshots and replay outputs). Most
  checks recompute a number stated in Report A `evidence.tex`, Report B `evidence.tex`,
  or their `results.md`/`coverage.md` tables. The rest are consistency checks, such as
  records against jobs, run files, mode rotation and hash ranking. All 418 pass at the
  stated rounding.
- The script does not import producer code. It re-implements "solved", "admitted",
  "flagged" and the paired bound comparison from the wording of the evidence sections.
  It also re-evaluates every returned incumbent against the archived original model
  with its own stdlib evaluator: 270 (A), 271 (B) and 67 (repair) incumbents, all
  within 1e-5. The largest scaled violations are 1.6e-6, 1.0e-6 and 8.0e-7.
- It recomputes the SHA256 of every snapshot file listed in the three source
  manifests (101, 156 and 103 files). All match. It recomputes the hash-ranked holdout
  selections from `instancedata.csv`, whose SHA256 equals the frozen manifest entry.
  It rebuilds the repair-cohort selection rule from the campaign-v2 records and logs
  (46 discovery overruns + 4 `split_affine` recursion errors = 50 triggers, 25 groups,
  75 jobs). That result equals the frozen `repair-plan.json`.
- A mutation test confirms that the checks can fail. One dropped cut, one altered dual
  bound and one failed incumbent each produced the expected mismatches. A perturbed
  incumbent coordinate and a perturbed objective were each rejected by the evaluator.

What this audit does **not** establish:

- The cut certificates were not replayed again. The script only checks that each
  `replay.json` agrees with the records: total and per-run cut counts, pass flags,
  omitted runs equal to the unknown-cut-log records, tamper flags, and hash counts. The
  validity of the certificates still rests on the archived replay checker.
- The incumbent re-evaluation is a floating-point residual check, not a feasibility
  proof.
- The script checks dual bounds only against the stated tolerance and the archived
  reference flags. SCIP's bounds are not certified.

## Commands run (exact)

All commands were run from the repository root `/workspace/minlp-notes`.
The script uses only the Python standard library; the interpreter is the project venv.

```sh
# claim-by-claim recomputation only (exit status 1 on any mismatch); about 2 s
code/minlp_solver_lab/.venv/bin/python paper-certified-support-cuts/verification/E1_audit_experiments.py
# claim checks plus all paper-ready tables (the two generated sections below)
code/minlp_solver_lab/.venv/bin/python paper-certified-support-cuts/verification/E1_audit_experiments.py --tables
```

The two generated sections at the end of this file ("Claim-by-claim recomputation" and
"Paper-ready tables") are the verbatim stdout of the second command, which exited with
status 0. During development, a one-off in-memory mutation test was also run; it
imports the script and alters copies of records, as described above. These are
targeted checks only. No project-wide tests were run and CI was not inspected.

Input files the script reads (all read-only):

- campaign records: `campaign-v1/records.jsonl` (SHA256 8caa3279...), `campaign-v2/records.jsonl` (96ae25ca..., equal to the hash bound in `repair-plan.json`), `repair-discovery-v1/records.jsonl` (aca95f9b...);
- `jobs.json`, `completion.json`, `environment.json`, `replay.json`, `source-manifest.json` and `snapshot/` of each campaign; `runs/*.json` (cross-checked against `records.jsonl`) and the four campaign-v2 error logs;
- `holdout-selection.json` of both reports, `repair-plan.json`, `campaign-v2/cases/*.json`, `code/minlp_solver_lab/instances/instancedata.csv`;
- Report A `experiments/star-mechanism.json` and `implementation/native-kernel-benchmark.json`.

## Definitions used by the script

- **Solved**: the status is `optimal` or `gaplimit`, the return code is 0, the
  incumbent is finite and passed the archived original-model check, and neither the
  final nor the root dual bound conflicts with the reference.
- **Admitted**: A means the model was not refused by the importer
  (`source_model_mismatch`) and did not fail during construction (`worker_error`).
  B means a `model_metadata` record exists.
- **Flagged**: the incumbent check failed, an incumbent was returned but not checked,
  or a reference conflict exists. Flagged records and records without a SCIP status
  are "unavailable" in comparisons.
- **Paired bound comparison**: the comparison uses `dual` by default, or `root_dual`
  where a table says so. Mode m is better than baseline when
  `sense*(d_m - d_base) > tol*max(1,|d_m|,|d_base|)`, with `tol = 1e-6` (the stated
  value). A sensitivity table repeats the comparison at other tolerances.
- **Time**: A uses `total_seconds + source_read_seconds`. B and repair use
  `total_seconds + preparation_seconds`. Outer time is the worker wall time measured by
  the parent process.
- **Cut counts**: B and repair require `cut_log_complete == true`. A missing log means
  an unknown count, never zero.
- **Discovery allowance** (repair rule):
  `min(max_separation_seconds, separation_budget_fraction*(time_limit - preparation_seconds))`.

## Statements in the evidence sections that the experiment records cannot check

These are outside E1. Their sources are listed for whoever audits them.

- Report A: the 186 tests and 53 subtests, and the four-test harness rerun
  (`VERIFICATION.md`). The two star audits: 155 cases (76 feasible, 79 empty), 298
  pieces and 7 mutations; and 786 intervals, 88 cases, 7063 comparisons and
  3 mutations (theory/review files). The benchmark JSON does not record that timings
  are "medians of 11 batches of 20 warmed evaluations". The other benchmark numbers
  were checked: 35 rows, build 0.268 s, the five 4096-point rows, and the 256-point
  native threshold against the 65 and 169 grid points. The exact star-mechanism
  numbers were also checked with `fractions`.
- Report B: the 250 tests and 8 subtests, and the 81 tests and 3 subtests
  (`VERIFICATION.md`); the 40 polytope diagnostics and 21 separation cases (review
  records); the post-freeze source hashes (`post-freeze-changes.md`).

## Findings that matter for the paper (not mismatches)

1. **Most "better/worse" bound outcomes are below the solver's own gap limit.** The
   evidence compares final duals at a relative tolerance of 1e-6, but runs stop at a
   relative gap of 1e-4. At a tolerance of 1e-4, every "better" outcome disappears in
   campaign-v2 full and root runs, in the repair cohort and in campaign-v1 full runs.
   In v2 holdout full, `all` changes from 2/21/7 to 0/26/4 (better/tie/worse) and
   `auto` from 2/24/4 to 0/26/4. The two v2 "better" models (nous1, st_e22) differ by
   9.5e-5 and 2.2e-5 relative. The v2 "worse" outcomes that remain at 1e-4 are all on
   time-limited models: graphpart_clique-40, ex5_2_5, tln7 and waterx. Campaign-v1
   root-only differences are real (they survive 1e-2). However, the reformulation
   control also improves ex4 and genpooling_lee2, so only pointpack06 is a root
   improvement specific to the cut modes. The paper should report this tolerance table
   (section "Sensitivity ..." below), not only the 1e-6 counts.
2. **The primary v2 timings measure the implementation before the discovery repair.**
   Discovery exceeded its allowance in 46 cut-mode records. In the 30-model holdout
   full runs, 8 models per cut mode overran, with 14.18 s (all) and 14.39 s (auto) of
   excess time. Of the 16.45 s holdout overhead of `all` (187.02 vs 170.57 s), 10.77 s
   arises in these 8 repair groups. The other 22 models still show +5.68 s, or +12%
   (52.42 vs 46.74 s). Across the 25 models that every mode solved, the shifted
   geometric mean time (shift 1 s) rises from 0.549 s (baseline) to 0.989 s (all) and
   0.957 s (auto). Both cut modes are more than 10% slower on 21 of those 25 models.
3. **graphpart_clique-40 (438 vs 392) is an artifact of the defect.** In the original
   runs, discovery took 6.04 s (all) and 6.00 s (auto) against a 1 s allowance. After
   the repair, both cut modes reach the baseline bound 438. The same repair cut
   btest14's discovery from 20.38 s to 0.38 s. It also changed outcomes beyond timing:
   p_ball_10b_5p_2d_m now receives 3 cuts in `all`, where the original run had 0.
4. **Run-to-run noise is measurable and comparable to several reported differences.**
   The repair cohort reruns the native baseline on 25 groups with the same model, seed
   and limits (an A/A test). At 1e-6, this gives 3 better, 22 tied and 0 worse, all on
   time-limited models. For example, tln7 moves from 14.4755 to 14.4810 and waterx from
   514.26 to 514.72. Time ratios on solved pairs range from 0.95 to 1.05. The relative
   bound differences reported as "worse" for tln7 and waterx are of the same size as
   these A/A shifts.
5. **Cuts appear only where they cannot change the solved count.** In v2, the 7 holdout
   models that received cuts in `all` were all solved by baseline. Four of them were
   solved at the root node in every mode. None of the 5 unsolved models received a cut.
   The only positive mechanism effect is on constructed cases. On the root-only
   `simplex_quadratic_vector` run, both cut modes reach `optimal` with bound -0.50000002,
   against baseline's node-limit bound -0.50027374. In v2, `quartic_balance_8` gets no
   cut and is unsolved by every mode within 10 s. In v1, the cut modes added 24 cuts and
   solved it, but so did the cut-free reformulation control.
6. **Campaign-v1 has a reformulation confound, which the paper must keep.** The control
   is more than 10% slower than baseline on 17 of 19 commonly solved held-out models.
   Its shifted geometric mean is 0.537 s against 0.419 s for baseline (all 0.690,
   auto 0.597). Against the control, `all` and `auto` each have 3 better, 16 tied,
   1 worse and 4 unavailable comparisons.

## Referee-facing criticisms of the design, and the data that already exist

| Likely criticism | Status in the data | What already exists | What would be needed |
|---|---|---|---|
| Time limits are very short (v1: 6 s full, 2 s root; v2: 30 s full, 10 s mechanisms, 5 s root). | The v2 baseline solves 8 holdout models in < 0.1 s, 11 in 0.1-1 s and 6 in 1-5 s. No model is solved in 5-30 s, and 5 time out with SCIP relative gaps of 8.46%-302.55% across modes. The population is therefore either trivial or out of reach at this budget. | Per-model bounds and gaps for the 5 hard models (table (d)) and the hardness profile table. | Longer runs (for example 1 h) on the 5 unsolved models and on harder instances that contain supported blocks. |
| Sample size is small and mostly unaffected. | Of the 30 v2 models, 7 receive any cut in `all` and 3 in `auto`, and all 7 are already solved by baseline. The coverage counts give 12 models with no supported block, 9 (all) with eligible blocks but no cut, and 2 solved without a callback. No solved-count difference can be detected. | Coverage classification per model (`coverage.json`, reproduced in the counts above). | A population selected by structure (for example, models with quadratic-star or row-domain blocks) and evaluated prospectively, reported separately from the unfiltered holdout. |
| The host is shared; timings are noisy. | There are 36 logical CPUs. The 1-minute load average was 10.3-11.1 for v1, 10.8 at the start and 12.5 at the end of v2, and 12.0 to 11.5 for the repair. Per-run load was not recorded. | A/A baseline reruns (25 same-seed pairs; solved-pair time ratio 0.95-1.05), seed-1 repeats (ratio 0.86-1.19), and outer versus in-process times. The v2 cut-mode slowdown (SGM +80% on commonly solved models) is far larger than this noise; differences of a few percent are not. | A quiet machine, or interleaved repeated runs with confidence intervals for time ratios. |
| A single seed. | Seed-1 repeats cover only 6 models per campaign, chosen as the first six in hash order (v2) or by a fixed subset (v1). All 6 v2 models are easy (solved in < 6 s). The seed changes nous1 from `gaplimit` to `optimal`. | Seed-1 tables for v1 and v2 and the repair seed-1 group. | Several seeds on the hard models; report bound and time variation per model. |
| The bound tolerance is below the gap limit. | Finding 1 above: at 1e-4, no "better" outcome remains. | Tolerance-sensitivity table and per-model lists. | Report root-only bounds (one node) as the strength measure, and final bounds only for unsolved models; use a tolerance of at least the gap limit. |
| The primary v2 comparison ran defective code, and the repair cohort is outcome-selected. | 46 overruns and 4 crashes. The repair covers 8 of the 30 holdout full groups and is selected by the defect, so it is not a holdout. | The original and repaired run for every repair job (per-job table), and A/A baselines inside the cohort. | A complete rerun of all 30 holdout models (all phases) with the frozen corrected code, as a new prospective comparison. |
| The comparison baseline is weak (default SCIP only). | No runs with other SCIP separator settings, other solvers, or dense SDP/RLT relaxations. Native SCIP solves the star instance in about 0.10 s (v1) and 0.09 s (v2). | None. | Native SCIP with its nonlinear separators varied (for example a bilinear/RLT emphasis), and at least one other global solver on the same instances. |
| Overhead is specific to the implementation (Python callback with symbolic discovery). | In v2 holdout full, discovery is 24.41 of 27.63 callback seconds (all). Direction LPs take 0.67 s and certification 2.36 s. | Time breakdown table (b). | Amortized or offline discovery; a compiled separator, or overhead reported with discovery excluded. |
| The populations are small models. | Size caps: v1 <= 80 variables and <= 120 constraints; v2 <= 120 and <= 180. According to Report A's own audit, the v1 metadata filter requires quadratic or general nonlinear constraints; E1 did not recheck that filter. | The selection files, verified by hash ranking. | A statement that the results do not extend to larger models, or an additional size stratum. |
| The positive evidence comes only from constructed cases. | simplex_quadratic_vector (root) and the star case are author-built; the v1 quartic improvement is shared with the control. | Mechanism tables (e) and (f). | Present them as mechanism demonstrations only, which both reports already do. |

## How the generated sections map to the requested material

- (a) per-instance table of every group where a cut mode added a cut: "(a) Every instance ...", in three tables (v2, repair, v1).
- (b) time breakdown per mode (read/preparation, discovery, build, SCIP solve wall, callback, direction LPs, certification, row export, SCIP excluding callback, integration, outer); shifted geometric means; discovery-overrun attribution.
- (c) the 30 v2 holdout models with stratum, size and per-mode outcome.
- (d) bounds and gaps of the 5 unsolved v2 holdout models, with the archived MINLPLib references.
- (e) the 13 synthetic mechanism cases with one-line descriptions (from `cases.py`) and v2 full and root outcomes.
- (f) the campaign-v1 analogue: solved counts by phase, comparisons against baseline and control, the 24 held-out models, unsolved bounds, synthetic outcomes and soft-budget overshoots.
- Also: v2 solved counts by phase, the tolerance sensitivity, the models behind each outcome, A/A reruns, the hardness profile, seed repeats, v2 overshoots, and per-job repair comparisons.

## Claim-by-claim recomputation

Inputs (SHA256):
- `research-20261002-convexification/experiments/campaign-v1/records.jsonl` 8caa32792d5b6e094fa07961d37d2827a03f167f4c29572cb66ef43d063eeffe
- `research-20261003-convexification/experiments/campaign-v2/records.jsonl` 96ae25ca9e2c3ded0686702f7e37cf7f767280ebfb80adbeee407bb7d93527b6
- `research-20261003-convexification/experiments/repair-discovery-v1/records.jsonl` aca95f9bd6cec7277c31e559af109a5b26c127f788f7c727e763e464414ee92c

| ID | Source | Claim | Stated | Recomputed | Result |
|---|---|---|---|---|---|
| A.0.jobs | A ev | records equal frozen jobs (count) | 316 | 316 | PASS |
| A.0.joborder | A ev | records in job order with identical parameters (mismatching rows) | 0 | 0 | PASS |
| A.0.runfiles | A ev | per-run JSON files that disagree with records.jsonl | 0 | 0 | PASS |
| A.1 | A ev | completed runs | 316 | 316 | PASS |
| A.2 | A ev | supervised wall seconds | 443.6 | 443.567 | PASS |
| A.3 | A completion.json | status counts | {'optimal': 162, 'gaplimit': 42, 'nodelimit': 56, 'timelimit': 12, 'source_model_mismatch': 36, 'worker_error': 8} | {'optimal': 162, 'gaplimit': 42, 'timelimit': 12, 'source_model_mismatch': 36, 'worker_error': 8, 'nodelimit': 56} | PASS |
| A.4 | A ev | structured importer refusals, all phases | 36 | 36 | PASS |
| A.5 | A ev | no hard process timeout / budget exhaustion statuses | 0 | 0 | PASS |
| A.6 | A ev | every outer worker wall time below the 20 s hard timeout | True | True (6.936442899997928) | PASS |
| A.7 | A ev | excluded earlier-campaign names | 123 | 123 | PASS |
| A.8 | A ev | eligible models | 279 | 279 | PASS |
| A.9 | A ev | ranks recomputed as SHA256(prefix+name) and eligible list sorted by rank | True | True ([True, True]) | PASS |
| A.10 | A ev | selected = first 24 in rank order | [kall_congruentcircles_c42, pooling_adhya2stp, ex4, genpooling_lee2, ex9_2_6, cvxnonsep_normcon30r, pointpack06, ex14_2_9, syn15m, st_robot, ex14_1_3, tltr, ex7_2_4, ex7_2_2, pooling_adhya2pq, ex9_2_4, cvxnonsep_psig30r, cvxnonsep_normcon40, ex14_2_8, cvxnonsep_pcon40r, ex1265a, kall_circles_c6b, syn10hfsg, procsel] | [kall_congruentcircles_c42, pooling_adhya2stp, ex4, genpooling_lee2, ex9_2_6, cvxnonsep_normcon30r, pointpack06, ex14_2_9, syn15m, st_robot, ex14_1_3, tltr, ex7_2_4, ex7_2_2, pooling_adhya2pq, ex9_2_4, cvxnonsep_psig30r, cvxnonsep_normcon40, ex14_2_8, cvxnonsep_pcon40r, ex1265a, kall_circles_c6b, syn10hfsg, procsel] | PASS |
| A.11 | A ev | selected models with integer variables (instancedata.csv) | 11 | 11 | PASS |
| A.12 | A ev | selected models classified convex (instancedata.csv) | 7 | 7 | PASS |
| A.13 | A ev | initial six = first six of the ranking | [kall_congruentcircles_c42, pooling_adhya2stp, ex4, genpooling_lee2, ex9_2_6, cvxnonsep_normcon30r] | [kall_congruentcircles_c42, pooling_adhya2stp, ex4, genpooling_lee2, ex9_2_6, cvxnonsep_normcon30r] | PASS |
| A.14 | A ev | held-out full-run names = selected 24 (in hash order) | [kall_congruentcircles_c42, pooling_adhya2stp, ex4, genpooling_lee2, ex9_2_6, cvxnonsep_normcon30r, pointpack06, ex14_2_9, syn15m, st_robot, ex14_1_3, tltr, ex7_2_4, ex7_2_2, pooling_adhya2pq, ex9_2_4, cvxnonsep_psig30r, cvxnonsep_normcon40, ex14_2_8, cvxnonsep_pcon40r, ex1265a, kall_circles_c6b, syn10hfsg, procsel] | [kall_congruentcircles_c42, pooling_adhya2stp, ex4, genpooling_lee2, ex9_2_6, cvxnonsep_normcon30r, pointpack06, ex14_2_9, syn15m, st_robot, ex14_1_3, tltr, ex7_2_4, ex7_2_2, pooling_adhya2pq, ex9_2_4, cvxnonsep_psig30r, cvxnonsep_normcon40, ex14_2_8, cvxnonsep_pcon40r, ex1265a, kall_circles_c6b, syn10hfsg, procsel] | PASS |
| A.15 | A ev | historical diagnostic suite | [btest14, chp_partload, ghg_2veh, waterno2_06] | [btest14, chp_partload, ghg_2veh, waterno2_06] | PASS |
| A.16 | A ev | synthetic mechanism/control cases | 13 | 13 | PASS |
| A.17 | A ev | time limits of full-budget phases (s) | [6.0] | [6.0] | PASS |
| A.18 | A ev | root-only time limit (s) and node limit | [(2.0, 1)] | [(2.0, 1)] | PASS |
| A.19 | A ev | root-only cases: 24 held-out + five mechanisms | [cvxnonsep_normcon30r, cvxnonsep_normcon40, cvxnonsep_pcon40r, cvxnonsep_psig30r, ex1265a, ex14_1_3, ex14_2_8, ex14_2_9, ex4, ex7_2_2, ex7_2_4, ex9_2_4, ex9_2_6, exp_pair, genpooling_lee2, kall_circles_c6b, kall_congruentcircles_c42, overlapping_products, pointpack06, pooling_adhya2pq, pooling_adhya2stp, procsel, quartic_balance_8, simplex_quadratic_vector, st_robot, star_marginal_inconsistency, syn10hfsg, syn15m, tltr] | [cvxnonsep_normcon30r, cvxnonsep_normcon40, cvxnonsep_pcon40r, cvxnonsep_psig30r, ex1265a, ex14_1_3, ex14_2_8, ex14_2_9, ex4, ex7_2_2, ex7_2_4, ex9_2_4, ex9_2_6, exp_pair, genpooling_lee2, kall_circles_c6b, kall_congruentcircles_c42, overlapping_products, pointpack06, pooling_adhya2pq, pooling_adhya2stp, procsel, quartic_balance_8, simplex_quadratic_vector, st_robot, star_marginal_inconsistency, syn10hfsg, syn15m, tltr] | PASS |
| A.20 | A protocol | seed-1 repeat subset | [ex4, exp_pair, kall_congruentcircles_c42, pooling_adhya2stp, quartic_balance_8, simplex_quadratic_vector] | [ex4, exp_pair, kall_congruentcircles_c42, pooling_adhya2stp, quartic_balance_8, simplex_quadratic_vector] | PASS |
| A.21 | A ev | seeds (non-repeat, repeat) | [{0}, {1}] | [{0}, {1}] | PASS |
| A.22 | A ev | relative gap limit in every config | [0.0001] | [0.0001] | PASS |
| A.23 | A ev | thread environment set to one | [1] | [1] | PASS |
| A.24 | A audit | mode-order rotation by case index: violations | [] | [] | PASS |
| A.T.synthetic.baseline.n | A ev | synthetic/baseline selected | 13 | 13 | PASS |
| A.T.synthetic.baseline.adm | A ev | synthetic/baseline admitted | 13 | 13 | PASS |
| A.T.synthetic.baseline.sol | A ev | synthetic/baseline solved | 12 | 12 | PASS |
| A.T.synthetic.baseline.cuts | A ev | synthetic/baseline recorded cuts | 0 | 0 | PASS |
| A.T.synthetic.baseline.cases | A results.md | synthetic/baseline cases with recorded cuts | 0 | 0 | PASS |
| A.T.synthetic.baseline.time | A ev | synthetic/baseline summed in-process seconds | 6.57 | 6.57252 | PASS |
| A.T.synthetic.baseline.outer | A results.md | synthetic/baseline summed outer seconds | 16.94 | 16.93696 | PASS |
| A.T.synthetic.control.n | A ev | synthetic/control selected | 13 | 13 | PASS |
| A.T.synthetic.control.adm | A ev | synthetic/control admitted | 13 | 13 | PASS |
| A.T.synthetic.control.sol | A ev | synthetic/control solved | 13 | 13 | PASS |
| A.T.synthetic.control.cuts | A ev | synthetic/control recorded cuts | 0 | 0 | PASS |
| A.T.synthetic.control.cases | A results.md | synthetic/control cases with recorded cuts | 0 | 0 | PASS |
| A.T.synthetic.control.time | A ev | synthetic/control summed in-process seconds | 1.66 | 1.66462 | PASS |
| A.T.synthetic.control.outer | A results.md | synthetic/control summed outer seconds | 11.57 | 11.57047 | PASS |
| A.T.synthetic.all.n | A ev | synthetic/all selected | 13 | 13 | PASS |
| A.T.synthetic.all.adm | A ev | synthetic/all admitted | 13 | 13 | PASS |
| A.T.synthetic.all.sol | A ev | synthetic/all solved | 13 | 13 | PASS |
| A.T.synthetic.all.cuts | A ev | synthetic/all recorded cuts | 89 | 89 | PASS |
| A.T.synthetic.all.cases | A results.md | synthetic/all cases with recorded cuts | 7 | 7 | PASS |
| A.T.synthetic.all.time | A ev | synthetic/all summed in-process seconds | 2.51 | 2.5054 | PASS |
| A.T.synthetic.all.outer | A results.md | synthetic/all summed outer seconds | 13.18 | 13.17695 | PASS |
| A.T.synthetic.auto.n | A ev | synthetic/auto selected | 13 | 13 | PASS |
| A.T.synthetic.auto.adm | A ev | synthetic/auto admitted | 13 | 13 | PASS |
| A.T.synthetic.auto.sol | A ev | synthetic/auto solved | 13 | 13 | PASS |
| A.T.synthetic.auto.cuts | A ev | synthetic/auto recorded cuts | 72 | 72 | PASS |
| A.T.synthetic.auto.cases | A results.md | synthetic/auto cases with recorded cuts | 7 | 7 | PASS |
| A.T.synthetic.auto.time | A ev | synthetic/auto summed in-process seconds | 2.45 | 2.45072 | PASS |
| A.T.synthetic.auto.outer | A results.md | synthetic/auto summed outer seconds | 13.14 | 13.13792 | PASS |
| A.T.holdout.baseline.n | A ev | holdout/baseline selected | 24 | 24 | PASS |
| A.T.holdout.baseline.adm | A ev | holdout/baseline admitted | 20 | 20 | PASS |
| A.T.holdout.baseline.sol | A ev | holdout/baseline solved | 19 | 19 | PASS |
| A.T.holdout.baseline.cuts | A ev | holdout/baseline recorded cuts | 0 | 0 | PASS |
| A.T.holdout.baseline.cases | A results.md | holdout/baseline cases with recorded cuts | 0 | 0 | PASS |
| A.T.holdout.baseline.time | A ev | holdout/baseline summed in-process seconds | 17.4 | 17.3977 | PASS |
| A.T.holdout.baseline.outer | A ev | holdout/baseline summed outer seconds | 36.66 | 36.66206 | PASS |
| A.T.holdout.control.n | A ev | holdout/control selected | 24 | 24 | PASS |
| A.T.holdout.control.adm | A ev | holdout/control admitted | 20 | 20 | PASS |
| A.T.holdout.control.sol | A ev | holdout/control solved | 19 | 19 | PASS |
| A.T.holdout.control.cuts | A ev | holdout/control recorded cuts | 0 | 0 | PASS |
| A.T.holdout.control.cases | A results.md | holdout/control cases with recorded cuts | 0 | 0 | PASS |
| A.T.holdout.control.time | A ev | holdout/control summed in-process seconds | 20.66 | 20.66498 | PASS |
| A.T.holdout.control.outer | A ev | holdout/control summed outer seconds | 40.12 | 40.11732 | PASS |
| A.T.holdout.all.n | A ev | holdout/all selected | 24 | 24 | PASS |
| A.T.holdout.all.adm | A ev | holdout/all admitted | 20 | 20 | PASS |
| A.T.holdout.all.sol | A ev | holdout/all solved | 18 | 18 | PASS |
| A.T.holdout.all.cuts | A ev | holdout/all recorded cuts | 230 | 230 | PASS |
| A.T.holdout.all.cases | A results.md | holdout/all cases with recorded cuts | 12 | 12 | PASS |
| A.T.holdout.all.time | A ev | holdout/all summed in-process seconds | 25.41 | 25.40806 | PASS |
| A.T.holdout.all.outer | A ev | holdout/all summed outer seconds | 45.44 | 45.43703 | PASS |
| A.T.holdout.auto.n | A ev | holdout/auto selected | 24 | 24 | PASS |
| A.T.holdout.auto.adm | A ev | holdout/auto admitted | 20 | 20 | PASS |
| A.T.holdout.auto.sol | A ev | holdout/auto solved | 18 | 18 | PASS |
| A.T.holdout.auto.cuts | A ev | holdout/auto recorded cuts | 106 | 106 | PASS |
| A.T.holdout.auto.cases | A results.md | holdout/auto cases with recorded cuts | 8 | 8 | PASS |
| A.T.holdout.auto.time | A ev | holdout/auto summed in-process seconds | 23.01 | 23.00795 | PASS |
| A.T.holdout.auto.outer | A ev | holdout/auto summed outer seconds | 42.49 | 42.4875 | PASS |
| A.T.historical.baseline.n | A results.md | historical/baseline selected | 4 | 4 | PASS |
| A.T.historical.baseline.sol | A results.md | historical/baseline solved | 0 | 0 | PASS |
| A.T.historical.baseline.cuts | A results.md | historical/baseline recorded cuts | 0 | 0 | PASS |
| A.T.historical.baseline.cases | A results.md | historical/baseline cases with recorded cuts | 0 | 0 | PASS |
| A.T.historical.baseline.time | A results.md | historical/baseline summed in-process seconds | 6.22 | 6.22482 | PASS |
| A.T.historical.baseline.outer | A results.md | historical/baseline summed outer seconds | 9.6 | 9.59957 | PASS |
| A.T.historical.control.n | A results.md | historical/control selected | 4 | 4 | PASS |
| A.T.historical.control.sol | A results.md | historical/control solved | 0 | 0 | PASS |
| A.T.historical.control.cuts | A results.md | historical/control recorded cuts | 0 | 0 | PASS |
| A.T.historical.control.cases | A results.md | historical/control cases with recorded cuts | 0 | 0 | PASS |
| A.T.historical.control.time | A results.md | historical/control summed in-process seconds | 6.84 | 6.84384 | PASS |
| A.T.historical.control.outer | A results.md | historical/control summed outer seconds | 10.36 | 10.36119 | PASS |
| A.T.historical.all.n | A results.md | historical/all selected | 4 | 4 | PASS |
| A.T.historical.all.sol | A results.md | historical/all solved | 0 | 0 | PASS |
| A.T.historical.all.cuts | A results.md | historical/all recorded cuts | 24 | 24 | PASS |
| A.T.historical.all.cases | A results.md | historical/all cases with recorded cuts | 1 | 1 | PASS |
| A.T.historical.all.time | A results.md | historical/all summed in-process seconds | 6.91 | 6.91343 | PASS |
| A.T.historical.all.outer | A results.md | historical/all summed outer seconds | 10.41 | 10.41157 | PASS |
| A.T.historical.auto.n | A results.md | historical/auto selected | 4 | 4 | PASS |
| A.T.historical.auto.sol | A results.md | historical/auto solved | 0 | 0 | PASS |
| A.T.historical.auto.cuts | A results.md | historical/auto recorded cuts | 24 | 24 | PASS |
| A.T.historical.auto.cases | A results.md | historical/auto cases with recorded cuts | 1 | 1 | PASS |
| A.T.historical.auto.time | A results.md | historical/auto summed in-process seconds | 6.88 | 6.88394 | PASS |
| A.T.historical.auto.outer | A results.md | historical/auto summed outer seconds | 10.26 | 10.25954 | PASS |
| A.25.baseline | A ev | held-out refusals (baseline) | [cvxnonsep_psig30r, syn10hfsg, syn15m] | [cvxnonsep_psig30r, syn10hfsg, syn15m] | PASS |
| A.26.baseline | A ev | refusal diagnostics name a log domain (baseline) | True | True | PASS |
| A.25.control | A ev | held-out refusals (control) | [cvxnonsep_psig30r, syn10hfsg, syn15m] | [cvxnonsep_psig30r, syn10hfsg, syn15m] | PASS |
| A.26.control | A ev | refusal diagnostics name a log domain (control) | True | True | PASS |
| A.25.all | A ev | held-out refusals (all) | [cvxnonsep_psig30r, syn10hfsg, syn15m] | [cvxnonsep_psig30r, syn10hfsg, syn15m] | PASS |
| A.26.all | A ev | refusal diagnostics name a log domain (all) | True | True | PASS |
| A.25.auto | A ev | held-out refusals (auto) | [cvxnonsep_psig30r, syn10hfsg, syn15m] | [cvxnonsep_psig30r, syn10hfsg, syn15m] | PASS |
| A.26.auto | A ev | refusal diagnostics name a log domain (auto) | True | True | PASS |
| A.27 | A ev | eight worker errors = cvxnonsep_pcon40r full+root x four modes | [128_cvxnonsep_pcon40r__baseline__full, 129_cvxnonsep_pcon40r__control__full, 130_cvxnonsep_pcon40r__all__full, 131_cvxnonsep_pcon40r__auto__full, 260_cvxnonsep_pcon40r__baseline__root, 261_cvxnonsep_pcon40r__control__root, 262_cvxnonsep_pcon40r__all__root, 263_cvxnonsep_pcon40r__auto__root] | [128_cvxnonsep_pcon40r__baseline__full, 129_cvxnonsep_pcon40r__control__full, 130_cvxnonsep_pcon40r__all__full, 131_cvxnonsep_pcon40r__auto__full, 260_cvxnonsep_pcon40r__baseline__root, 261_cvxnonsep_pcon40r__control__root, 262_cvxnonsep_pcon40r__all__root, 263_cvxnonsep_pcon40r__auto__root] | PASS |
| A.27b | A ev | worker errors count | 8 | 8 | PASS |
| A.28 | A ev | pcon40r errors are variable-exponent construction failures | True | True ([('NotImplementedError', 'variable exponent')]) | PASS |
| A.29 | A ev | genpooling_lee2 statuses (baseline, control, all, auto) | [True, True, timelimit, timelimit] | [True, True, timelimit, timelimit] | PASS |
| A.30a | A ev | genpooling_lee2 baseline seconds | 5.61 | 5.6078 | PASS |
| A.30b | A ev | genpooling_lee2 control seconds | 4.89 | 4.89338 | PASS |
| A.31 | A ev | kall_circles_c6b time-limited in every mode | [timelimit, timelimit, timelimit, timelimit] | [timelimit, timelimit, timelimit, timelimit] | PASS |
| A.32 | A ev | quartic_balance_8 solved (baseline, control, all, auto) | [False, True, True, True] | [False, True, True, True] | PASS |
| A.33 | A ev | star case: baseline solved with dual ~ 1/128 | True | True (0.007812489902767096) | PASS |
| A.34a | A ev | star case baseline seconds | 0.1 | 0.10496 | PASS |
| A.34b | A ev | star case all seconds | 0.5 | 0.50374 | PASS |
| A.34c | A ev | star case auto seconds | 0.48 | 0.47989 | PASS |
| A.35a | A ev | star merging disabled: all seconds | 0.19 | 0.19377 | PASS |
| A.35b | A ev | star merging disabled: auto seconds | 0.1 | 0.10374 | PASS |
| A.35c | A ev | star merging disabled: status unchanged | [optimal, optimal] | [optimal, optimal] | PASS |
| A.36 | A ev | no_cache ablation: mechanism runs solved | [10, 10] | [10, 10] | PASS |
| A.37 | A ev | historical models passing the importer | [waterno2_06] | [waterno2_06] | PASS |
| A.38 | A ev | waterno2_06 time-limited in every mode | [timelimit, timelimit, timelimit, timelimit] | [timelimit, timelimit, timelimit, timelimit] | PASS |
| A.39.baseline | A ev | waterno2_06 lower bound (baseline) | 26.59 | 26.59088 | PASS |
| A.39.control | A ev | waterno2_06 lower bound (control) | 21.17 | 21.16721 | PASS |
| A.39.all | A ev | waterno2_06 lower bound (all) | 7.05 | 7.05151 | PASS |
| A.39.auto | A ev | waterno2_06 lower bound (auto) | 2.41 | 2.40784 | PASS |
| A.C.full.synthetic.control | A results.md | final dual vs baseline B/T/W/U (synthetic, control) | [3, 10, 0, 0] | [3, 10, 0, 0] | PASS |
| A.C.full.synthetic.all | A results.md | final dual vs baseline B/T/W/U (synthetic, all) | [2, 9, 2, 0] | [2, 9, 2, 0] | PASS |
| A.C.full.synthetic.auto | A results.md | final dual vs baseline B/T/W/U (synthetic, auto) | [2, 9, 2, 0] | [2, 9, 2, 0] | PASS |
| A.C.full.holdout.control | A results.md | final dual vs baseline B/T/W/U (holdout, control) | [1, 15, 4, 4] | [1, 15, 4, 4] | PASS |
| A.C.full.holdout.all | A results.md | final dual vs baseline B/T/W/U (holdout, all) | [1, 14, 5, 4] | [1, 14, 5, 4] | PASS |
| A.C.full.holdout.auto | A results.md | final dual vs baseline B/T/W/U (holdout, auto) | [3, 12, 5, 4] | [3, 12, 5, 4] | PASS |
| A.C.full.historical.control | A results.md | final dual vs baseline B/T/W/U (historical, control) | [0, 0, 1, 3] | [0, 0, 1, 3] | PASS |
| A.C.full.historical.all | A results.md | final dual vs baseline B/T/W/U (historical, all) | [0, 0, 1, 3] | [0, 0, 1, 3] | PASS |
| A.C.full.historical.auto | A results.md | final dual vs baseline B/T/W/U (historical, auto) | [0, 0, 1, 3] | [0, 0, 1, 3] | PASS |
| A.C.root.all | A ev | held-out root-only vs baseline B/T/W/U (all) | [3, 15, 2, 4] | [3, 15, 2, 4] | PASS |
| A.C.root.auto | A ev | held-out root-only vs baseline B/T/W/U (auto) | [3, 14, 3, 4] | [3, 14, 3, 4] | PASS |
| A.40 | A ev | candidate LPs (all, auto) | [1073, 323] | [1073, 323] | PASS |
| A.41a | A ev | callback seconds (all) | 5.59 | 5.58826 | PASS |
| A.41b | A ev | callback seconds (auto) | 3.05 | 3.05089 | PASS |
| A.42a | A ev | certification seconds (all) | 0.7 | 0.7013 | PASS |
| A.42b | A ev | certification seconds (auto) | 0.34 | 0.33864 | PASS |
| A.43 | A ev | unsuccessful support attempts (all, auto) | [95, 14] | [95, 14] | PASS |
| A.44 | A ev | screen queries and skips, all phases | [506, 2] | [506, 2] | PASS |
| A.45.hashes | A ev | frozen source/input hashes (manifest entries) | 101 | 101 | PASS |
| A.45.hashok | A ev | manifest entries whose snapshot file is missing or has a different SHA256 | 0 | 0 | PASS |
| A.46.cuts | A ev | recorded added cuts (all phases, from records) | 1082 | 1082 | PASS |
| A.46.replayed | A ev | replay: cuts replayed | 1082 | 1082 | PASS |
| A.46.perrun | A ev | replay runs whose cut count differs from the record or was not fully replayed | 0 | 0 | PASS |
| A.46.passed | A ev | replay runs failed (and overall pass flag) | [0, True] | [0, True] | PASS |
| A.46.tamper | A ev | tampering controls rejected / total | [12, 12] | [12, 12] | PASS |
| A.46.srcfiles | A ev | replay: source/input hashes verified | 101 | 101 | PASS |
| A.46.missing | A ev | records with unknown cut count (no complete cut log) | 8 | 8 | PASS |
| A.46.omitted | A ev | replay omitted runs = records with unknown cut count | [128_cvxnonsep_pcon40r__baseline__full, 129_cvxnonsep_pcon40r__control__full, 130_cvxnonsep_pcon40r__all__full, 131_cvxnonsep_pcon40r__auto__full, 260_cvxnonsep_pcon40r__baseline__root, 261_cvxnonsep_pcon40r__control__root, 262_cvxnonsep_pcon40r__all__root, 263_cvxnonsep_pcon40r__auto__root] | [128_cvxnonsep_pcon40r__baseline__full, 129_cvxnonsep_pcon40r__control__full, 130_cvxnonsep_pcon40r__all__full, 131_cvxnonsep_pcon40r__auto__full, 260_cvxnonsep_pcon40r__baseline__root, 261_cvxnonsep_pcon40r__control__root, 262_cvxnonsep_pcon40r__all__root, 263_cvxnonsep_pcon40r__auto__root] | PASS |
| A.46.bound | A ev | replay: runs bound to an original model | 308 | 308 | PASS |
| A.47 | A ev | records with an original-model output | 308 | 308 | PASS |
| A.48.inc | A ev | returned incumbents independently checked | 270 | 270 | PASS |
| A.48.incfail | A ev | checked incumbents that failed | 0 | 0 | PASS |
| A.48.reeval | A ev | incumbents re-evaluated by this script (stdlib evaluator): count, passing at 1e-5 | [270, 270] | [270, 270] | PASS |
| A.48.reevalmax | A ev | largest re-evaluated scaled violation / objective discrepancy <= 1e-5 | True | True ([1.6123683092802903e-06, 3.283648026169733e-06]) | PASS |
| A.48.refconf | A ev | final or root dual bounds conflicting with reference | 0 | 0 | PASS |
| A.X.1 | A ev | pair measures: expected pair objectives (exact) | [0, 0] | [0, 0] | PASS |
| A.X.2 | A ev | pair measures share center moments 1, 1/2, 5/16 | [[Fraction(1, 1), Fraction(1, 2), Fraction(5, 16)], [Fraction(1, 1), Fraction(1, 2), Fraction(5, 16)]] | [[Fraction(1, 1), Fraction(1, 2), Fraction(5, 16)], [Fraction(1, 1), Fraction(1, 2), Fraction(5, 16)]] | PASS |
| A.X.3 | A ev | exact center partition has three pieces | 3 | 3 | PASS |
| A.X.4 | A ev | objective at (1, 11/16, 1) and stated star minimum | [1/128, 1/128] | [1/128, 1/128] | PASS |
| A.X.5 | A ev | minimum over pieces of the piece polynomials | 1/128 | 1/128 | PASS |
| A.X.6 | A ev | pair-hull bound 0; replay accepted; changed objective rejected | [0, True, True] | [0, True, True] | PASS |
| A.X.7 | A ev | native benchmark combinations | 35 | 35 | PASS |
| A.X.8 | A ev | native build and load seconds | 0.268 | 0.268421 | PASS |
| A.X.9.univariate_square | A ev | 4096-point timings, us and ratio (univariate_square) | [5.2, 30.2, 0.17] | [5.2, 30.2, 0.17] | PASS |
| A.X.9.bivariate_quadratic_5 | A ev | 4096-point timings, us and ratio (bivariate_quadratic_5) | [30.81, 48.46, 0.64] | [30.81, 48.46, 0.64] | PASS |
| A.X.9.univariate_quartic | A ev | 4096-point timings, us and ratio (univariate_quartic) | [236.94, 27.76, 8.54] | [236.94, 27.76, 8.54] | PASS |
| A.X.9.univariate_6 | A ev | 4096-point timings, us and ratio (univariate_6) | [972.95, 43.51, 22.36] | [972.95, 43.51, 22.36] | PASS |
| A.X.9.bivariate_24 | A ev | 4096-point timings, us and ratio (bivariate_24) | [6176.34, 390.89, 15.8] | [6176.34, 390.89, 15.8] | PASS |
| A.X.12 | A ev | main separation grids (65 and 13^2 = 169 points) stay below the native threshold | True | True ([{(65, 13)}, 256]) | PASS |
| A.X.10 | A ev | single quartic at 32 points: C slower than NumPy | True | True | PASS |
| A.X.11 | A ev | low-degree rows slower in C at 4096 points; dispatch keeps NumPy | True | True | PASS |
| B.0.1 | B ev | first campaign records | 316 | 316 | PASS |
| B.0.2 | B ev | first campaign selected/admitted held-out | [24, 20] | [24, 20] | PASS |
| B.0.3 | B ev | first campaign held-out solved (baseline, control, all, auto) | [19, 19, 18, 18] | [19, 19, 18, 18] | PASS |
| B.0.4 | B ev | first campaign direction LPs (all, auto) | [1073, 323] | [1073, 323] | PASS |
| B.0.5 | B ev | first campaign callback seconds (all, auto) | [5.59, 3.05] | [5.59, 3.05] | PASS |
| B.0.6 | B ev | first campaign synthetic solved (control, all, auto, baseline) | [13, 13, 13, 12] | [13, 13, 13, 12] | PASS |
| B.0.7 | B ev | first campaign cuts replayed / incumbents checked / construction errors | [1082, 270, 8] | [1082, 270, 8] | PASS |
| B.1 | B ev | eligible list sorted by recomputed SHA256 rank | True | True | PASS |
| B.2 | B ev | eligible models | 422 | 422 | PASS |
| B.2b | B ev | eligible count field | 422 | 422 | PASS |
| B.3 | B ev | eligible stratum counts recomputed from instancedata.csv (convex, nonconvex cont., nonconvex int.) | [85, 208, 129] | [85, 208, 129] | PASS |
| B.4 | B ev | selected = first ten per stratum in rank order | [p_ball_10b_5p_2d_m, st_glmp_kk90, du-opt5, nvs24, nous1, supplychain, ex4_1_8, ex8_3_4, cvxnonsep_normcon20r, cvxnonsep_psig20r, hybriddynamic_var, graphpart_clique-40, pooling_adhya4pq, st_glmp_kk92, st_testph4, du-opt, ex5_2_5, kall_congruentcircles_c41, ex14_2_7, st_e22, kall_congruentcircles_c51, tln4, synthes1, syn05m, nvs17, tln7, st_testgr3, graphpart_2g-0066-0066, ex1223, waterx] | [p_ball_10b_5p_2d_m, st_glmp_kk90, du-opt5, nvs24, nous1, supplychain, ex4_1_8, ex8_3_4, cvxnonsep_normcon20r, cvxnonsep_psig20r, hybriddynamic_var, graphpart_clique-40, pooling_adhya4pq, st_glmp_kk92, st_testph4, du-opt, ex5_2_5, kall_congruentcircles_c41, ex14_2_7, st_e22, kall_congruentcircles_c51, tln4, synthes1, syn05m, nvs17, tln7, st_testgr3, graphpart_2g-0066-0066, ex1223, waterx] | PASS |
| B.5 | B ev | selected per stratum | [10, 10, 10] | [10, 10, 10] | PASS |
| B.6 | B ev | selected models overlapping prior convexification campaign names | [] | [] | PASS |
| B.6b | B protocol | instancedata.csv SHA256 equals frozen manifest entry | dbe97fdc90ba6b6655f8f637b76b803006c1beec416501db0385eb9c27aa5ab8 | dbe97fdc90ba6b6655f8f637b76b803006c1beec416501db0385eb9c27aa5ab8 | PASS |
| B.7 | B ev | holdout full names = selection order | [p_ball_10b_5p_2d_m, st_glmp_kk90, du-opt5, nvs24, nous1, supplychain, ex4_1_8, ex8_3_4, cvxnonsep_normcon20r, cvxnonsep_psig20r, hybriddynamic_var, graphpart_clique-40, pooling_adhya4pq, st_glmp_kk92, st_testph4, du-opt, ex5_2_5, kall_congruentcircles_c41, ex14_2_7, st_e22, kall_congruentcircles_c51, tln4, synthes1, syn05m, nvs17, tln7, st_testgr3, graphpart_2g-0066-0066, ex1223, waterx] | [p_ball_10b_5p_2d_m, st_glmp_kk90, du-opt5, nvs24, nous1, supplychain, ex4_1_8, ex8_3_4, cvxnonsep_normcon20r, cvxnonsep_psig20r, hybriddynamic_var, graphpart_clique-40, pooling_adhya4pq, st_glmp_kk92, st_testph4, du-opt, ex5_2_5, kall_congruentcircles_c41, ex14_2_7, st_e22, kall_congruentcircles_c51, tln4, synthes1, syn05m, nvs17, tln7, st_testgr3, graphpart_2g-0066-0066, ex1223, waterx] | PASS |
| B.8.jobs | B ev | records equal frozen jobs (count) | 282 | 282 | PASS |
| B.8.joborder | B ev | records in job order with identical parameters (mismatching rows) | 0 | 0 | PASS |
| B.8.runfiles | B ev | per-run JSON files that disagree with records.jsonl | 0 | 0 | PASS |
| B.9 | B ev | schedule: holdout full, diagnostic full, mechanism full, root, repeat (total 282) | [90, 30, 39, 105, 18, 282] | [90, 30, 39, 105, 18, 282] | PASS |
| B.10 | B ev | (time limit, node limit, hard timeout, seed) per phase | {'holdout': {(30.0, None, 45.0, 0)}, 'diagnostic': {(30.0, None, 45.0, 0)}, 'synthetic': {(10.0, None, 20.0, 0)}, 'root': {(5.0, 1, 15.0, 0)}, 'repeat': {(30.0, None, 45.0, 1)}} | {'holdout': {(30.0, None, 45.0, 0)}, 'diagnostic': {(30.0, None, 45.0, 0)}, 'synthetic': {(10.0, None, 20.0, 0)}, 'root': {(5.0, 1, 15.0, 0)}, 'repeat': {(30.0, None, 45.0, 1)}} | PASS |
| B.11 | B protocol | sum of hard process timeouts (minutes) < 150-minute cap | [142.75, 150.0] | [142.75, 150.0] | PASS |
| B.12 | B protocol | seed-one repeat = first six hash-ranked holdout models | [p_ball_10b_5p_2d_m, st_glmp_kk90, du-opt5, nvs24, nous1, supplychain] | [p_ball_10b_5p_2d_m, st_glmp_kk90, du-opt5, nvs24, nous1, supplychain] | PASS |
| B.13 | B ev | root-only cases = 30 holdout + five mechanisms | [cvxnonsep_normcon20r, cvxnonsep_psig20r, du-opt, du-opt5, ex1223, ex14_2_7, ex4_1_8, ex5_2_5, ex8_3_4, exp_pair, graphpart_2g-0066-0066, graphpart_clique-40, hybriddynamic_var, kall_congruentcircles_c41, kall_congruentcircles_c51, nous1, nvs17, nvs24, overlapping_products, p_ball_10b_5p_2d_m, pooling_adhya4pq, quartic_balance_8, simplex_quadratic_vector, st_e22, st_glmp_kk90, st_glmp_kk92, st_testgr3, st_testph4, star_marginal_inconsistency, supplychain, syn05m, synthes1, tln4, tln7, waterx] | [cvxnonsep_normcon20r, cvxnonsep_psig20r, du-opt, du-opt5, ex1223, ex14_2_7, ex4_1_8, ex5_2_5, ex8_3_4, exp_pair, graphpart_2g-0066-0066, graphpart_clique-40, hybriddynamic_var, kall_congruentcircles_c41, kall_congruentcircles_c51, nous1, nvs17, nvs24, overlapping_products, p_ball_10b_5p_2d_m, pooling_adhya4pq, quartic_balance_8, simplex_quadratic_vector, st_e22, st_glmp_kk90, st_glmp_kk92, st_testgr3, st_testph4, star_marginal_inconsistency, supplychain, syn05m, synthes1, tln4, tln7, waterx] | PASS |
| B.14 | B ev | mode-order rotation by model index within each phase list: violations | [] | [] | PASS |
| B.15 | B ev | relative gap limit in every config | [0.0001] | [0.0001] | PASS |
| B.16 | B ev | campaign outer wall seconds | 1338.6 | 1338.6109 | PASS |
| B.17 | B ev | status counts | {'optimal': 106, 'gaplimit': 74, 'timelimit': 31, 'nodelimit': 67, 'worker_error': 4} | {'optimal': 106, 'gaplimit': 74, 'timelimit': 31, 'worker_error': 4, 'nodelimit': 67} | PASS |
| B.18 | B ev | no hard timeouts: every outer wall below its process limit | True | True (0.6924899942668465) | PASS |
| B.19.baseline | B ev | holdout admitted (baseline) | 30 | 30 | PASS |
| B.19.all | B ev | holdout admitted (all) | 30 | 30 | PASS |
| B.19.auto | B ev | holdout admitted (auto) | 30 | 30 | PASS |
| B.20 | B ev | holdout solved (baseline, all, auto) | [25, 25, 25] | [25, 25, 25] | PASS |
| B.21 | B ev | same 25 solved models in every mode | True | True | PASS |
| B.22.baseline | B ev | holdout added cuts (baseline) | 0 | 0 | PASS |
| B.23.baseline | B ev | holdout cases with cuts (baseline) | 0 | 0 | PASS |
| B.24.baseline | B ev | holdout summed integration seconds (baseline) | 170.57 | 170.57487 | PASS |
| B.24o.baseline | B results.md | holdout summed outer seconds (baseline) | 197.3 | 197.30121 | PASS |
| B.22.all | B ev | holdout added cuts (all) | 38 | 38 | PASS |
| B.23.all | B ev | holdout cases with cuts (all) | 7 | 7 | PASS |
| B.24.all | B ev | holdout summed integration seconds (all) | 187.02 | 187.02498 | PASS |
| B.24o.all | B results.md | holdout summed outer seconds (all) | 213.2 | 213.19845 | PASS |
| B.22.auto | B ev | holdout added cuts (auto) | 10 | 10 | PASS |
| B.23.auto | B ev | holdout cases with cuts (auto) | 3 | 3 | PASS |
| B.24.auto | B ev | holdout summed integration seconds (auto) | 187.12 | 187.11848 | PASS |
| B.24o.auto | B results.md | holdout summed outer seconds (auto) | 213.56 | 213.5561 | PASS |
| B.25 | B ev | candidate LPs (all, auto) | [186, 66] | [186, 66] | PASS |
| B.26 | B ev | support calls (all, auto) | [138, 51] | [138, 51] | PASS |
| B.27.all | B ev | callback seconds (all) | 27.63 | 27.63284 | PASS |
| B.28.all | B ev | discovery seconds (all) | 24.41 | 24.40589 | PASS |
| B.29.all | B ev | discovery runs / no supported blocks / solved without separator call (all) | [28, 12, 2] | [28, 12, 2] | PASS |
| B.30.all | B ev | supported blocks / auto-eligible / declined source sides (all) | [156, 63, 186] | [156, 63, 186] | PASS |
| B.27.auto | B ev | callback seconds (auto) | 27.0 | 27.00045 | PASS |
| B.28.auto | B ev | discovery seconds (auto) | 24.63 | 24.62715 | PASS |
| B.29.auto | B ev | discovery runs / no supported blocks / solved without separator call (auto) | [28, 12, 2] | [28, 12, 2] | PASS |
| B.30.auto | B ev | supported blocks / auto-eligible / declined source sides (auto) | [156, 63, 186] | [156, 63, 186] | PASS |
| B.31.all | B ev | final dual vs baseline B/T/W/U (all) | [2, 21, 7, 0] | [2, 21, 7, 0] | PASS |
| B.31.auto | B ev | final dual vs baseline B/T/W/U (auto) | [2, 24, 4, 0] | [2, 24, 4, 0] | PASS |
| B.32 | B ev | improved final bounds occur only on models solved in all modes | True | True ([nous1, st_e22]) | PASS |
| B.33 | B ev | number of common unsolved models | 5 | 5 | PASS |
| B.34.all | B ev | unsolved five: B/T/W/U (all) | [0, 1, 4, 0] | [0, 1, 4, 0] | PASS |
| B.35.all | B ev | cuts on the unsolved five (all) | 0 | 0 | PASS |
| B.34.auto | B ev | unsolved five: B/T/W/U (auto) | [0, 1, 4, 0] | [0, 1, 4, 0] | PASS |
| B.35.auto | B ev | cuts on the unsolved five (auto) | 0 | 0 | PASS |
| B.36 | B ev | graphpart_clique-40 final lower bounds (baseline, all, auto) | [438, 392, 392] | [438, 392, 392] | PASS |
| B.37.all | B ev | root-only vs baseline B/T/W/U (all) | [1, 26, 3, 0] | [1, 26, 3, 0] | PASS |
| B.37.auto | B ev | root-only vs baseline B/T/W/U (auto) | [1, 28, 1, 0] | [1, 28, 1, 0] | PASS |
| B.38 | B ev | seed-one repeats solved (baseline, all, auto) | [6, 6, 6] | [6, 6, 6] | PASS |
| B.39.all | B ev | seed-one final dual vs baseline B/T/W/U (all) | [0, 6, 0, 0] | [0, 6, 0, 0] | PASS |
| B.39.auto | B ev | seed-one final dual vs baseline B/T/W/U (auto) | [0, 6, 0, 0] | [0, 6, 0, 0] | PASS |
| B.40.baseline | B ev | synthetic full solved (baseline) | 12 | 12 | PASS |
| B.40.all | B ev | synthetic full solved (all) | 12 | 12 | PASS |
| B.40.auto | B ev | synthetic full solved (auto) | 12 | 12 | PASS |
| B.41 | B ev | root simplex_quadratic_vector: cuts and status (all, auto) | [(2, 'optimal'), (2, 'optimal')] | [(2, 'optimal'), (2, 'optimal')] | PASS |
| B.42 | B ev | root simplex_quadratic_vector cut-mode bound ~ -0.50000002 | [-0.50000002, -0.50000002] | [-0.50000002, -0.50000002] | PASS |
| B.43 | B ev | root simplex_quadratic_vector baseline (status, bound) | [nodelimit, -0.50027374] | [nodelimit, -0.50027374] | PASS |
| B.44 | B ev | diagnostic solved (baseline, all, auto) | [5, 5, 5] | [5, 5, 5] | PASS |
| B.45 | B ev | worker errors: chp_partload and waterno2_06 in both cut modes | [111_chp_partload__all__full, 112_chp_partload__auto__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full] | [111_chp_partload__all__full, 112_chp_partload__auto__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full] | PASS |
| B.46 | B ev | error logs show split_affine RecursionError raised inside the separator (after build) | [True, True, True, True] | [True, True, True, True] | PASS |
| B.47 | B ev | baseline admits the models of the four errors | [True, True] | [True, True] | PASS |
| B.48 | B ev | seven earlier-refused models admitted (baseline) | [True, True, True, True, True, True, True] | [True, True, True, True, True, True, True] | PASS |
| B.R.diagnostic.baseline | B results.md | diagnostic/baseline: admitted, solved, cuts, cases with cuts | [10, 5, 0, 0] | [10, 5, 0, 0] | PASS |
| B.R.diagnostic.baseline.t | B results.md | diagnostic/baseline: integration seconds | 156.56 | 156.55626 | PASS |
| B.R.diagnostic.baseline.o | B results.md | diagnostic/baseline: outer seconds | 165.67 | 165.67187 | PASS |
| B.R.diagnostic.all | B results.md | diagnostic/all: admitted, solved, cuts, cases with cuts | [8, 5, 15, 2] | [8, 5, 15, 2] | PASS |
| B.R.diagnostic.all.t | B results.md | diagnostic/all: integration seconds | 103.94 | 103.93976 | PASS |
| B.R.diagnostic.all.o | B results.md | diagnostic/all: outer seconds | 123.81 | 123.81443 | PASS |
| B.R.diagnostic.auto | B results.md | diagnostic/auto: admitted, solved, cuts, cases with cuts | [8, 5, 5, 1] | [8, 5, 5, 1] | PASS |
| B.R.diagnostic.auto.t | B results.md | diagnostic/auto: integration seconds | 103.45 | 103.44954 | PASS |
| B.R.diagnostic.auto.o | B results.md | diagnostic/auto: outer seconds | 123.32 | 123.32391 | PASS |
| B.R.synthetic.baseline | B results.md | synthetic/baseline: admitted, solved, cuts, cases with cuts | [13, 12, 0, 0] | [13, 12, 0, 0] | PASS |
| B.R.synthetic.baseline.t | B results.md | synthetic/baseline: integration seconds | 10.69 | 10.68506 | PASS |
| B.R.synthetic.baseline.o | B results.md | synthetic/baseline: outer seconds | 22.08 | 22.07559 | PASS |
| B.R.synthetic.all | B results.md | synthetic/all: admitted, solved, cuts, cases with cuts | [13, 12, 13, 4] | [13, 12, 13, 4] | PASS |
| B.R.synthetic.all.t | B results.md | synthetic/all: integration seconds | 10.86 | 10.85569 | PASS |
| B.R.synthetic.all.o | B results.md | synthetic/all: outer seconds | 22.06 | 22.05681 | PASS |
| B.R.synthetic.auto | B results.md | synthetic/auto: admitted, solved, cuts, cases with cuts | [13, 12, 2, 1] | [13, 12, 2, 1] | PASS |
| B.R.synthetic.auto.t | B results.md | synthetic/auto: integration seconds | 10.69 | 10.69183 | PASS |
| B.R.synthetic.auto.o | B results.md | synthetic/auto: outer seconds | 21.87 | 21.86668 | PASS |
| B.R.cmp.diagnostic.all | B results.md | final dual vs baseline B/T/W/U (diagnostic, all) | [1, 5, 2, 2] | [1, 5, 2, 2] | PASS |
| B.R.cmp.diagnostic.auto | B results.md | final dual vs baseline B/T/W/U (diagnostic, auto) | [0, 5, 3, 2] | [0, 5, 3, 2] | PASS |
| B.R.cmp.synthetic.all | B results.md | final dual vs baseline B/T/W/U (synthetic, all) | [1, 11, 1, 0] | [1, 11, 1, 0] | PASS |
| B.R.cmp.synthetic.auto | B results.md | final dual vs baseline B/T/W/U (synthetic, auto) | [1, 11, 1, 0] | [1, 11, 1, 0] | PASS |
| B.V.holdout.all | B coverage.md | holdout/all: callback runs, calls, discovery runs, blocks, eligible, unsupported | [28, 60, 28, 156, 63, 186] | [28, 60, 28, 156, 63, 186] | PASS |
| B.V.holdout.all.cb | B coverage.md | holdout/all: callback seconds | 27.633 | 27.632838 | PASS |
| B.V.holdout.auto | B coverage.md | holdout/auto: callback runs, calls, discovery runs, blocks, eligible, unsupported | [28, 61, 28, 156, 63, 186] | [28, 61, 28, 156, 63, 186] | PASS |
| B.V.holdout.auto.cb | B coverage.md | holdout/auto: callback seconds | 27.0 | 27.000448 | PASS |
| B.V.diagnostic.all | B coverage.md | diagnostic/all: callback runs, calls, discovery runs, blocks, eligible, unsupported | [8, 11, 8, 136, 37, 188] | [8, 11, 8, 136, 37, 188] | PASS |
| B.V.diagnostic.all.cb | B coverage.md | diagnostic/all: callback seconds | 29.677 | 29.676999 | PASS |
| B.V.diagnostic.auto | B coverage.md | diagnostic/auto: callback runs, calls, discovery runs, blocks, eligible, unsupported | [8, 13, 8, 136, 37, 188] | [8, 13, 8, 136, 37, 188] | PASS |
| B.V.diagnostic.auto.cb | B coverage.md | diagnostic/auto: callback seconds | 28.681 | 28.680783 | PASS |
| B.V.synthetic.all | B coverage.md | synthetic/all: callback runs, calls, discovery runs, blocks, eligible, unsupported | [6, 16, 6, 5, 1, 1] | [6, 16, 6, 5, 1, 1] | PASS |
| B.V.synthetic.all.cb | B coverage.md | synthetic/all: callback seconds | 0.331 | 0.331011 | PASS |
| B.V.synthetic.auto | B coverage.md | synthetic/auto: callback runs, calls, discovery runs, blocks, eligible, unsupported | [6, 16, 6, 5, 1, 1] | [6, 16, 6, 5, 1, 1] | PASS |
| B.V.synthetic.auto.cb | B coverage.md | synthetic/auto: callback seconds | 0.078 | 0.07821 | PASS |
| B.49.hashes | B ev | frozen source/input hashes (manifest entries) | 156 | 156 | PASS |
| B.49.hashok | B ev | manifest entries whose snapshot file is missing or has a different SHA256 | 0 | 0 | PASS |
| B.50.cuts | B ev | recorded added cuts (all phases, from records) | 123 | 123 | PASS |
| B.50.replayed | B ev | replay: cuts replayed | 123 | 123 | PASS |
| B.50.perrun | B ev | replay runs whose cut count differs from the record or was not fully replayed | 0 | 0 | PASS |
| B.50.passed | B ev | replay runs failed (and overall pass flag) | [0, True] | [0, True] | PASS |
| B.50.tamper | B ev | tampering controls rejected / total | [14, 14] | [14, 14] | PASS |
| B.50.srcfiles | B ev | replay: source/input hashes verified | 156 | 156 | PASS |
| B.50.missing | B ev | records with unknown cut count (no complete cut log) | 4 | 4 | PASS |
| B.50.omitted | B ev | replay omitted runs = records with unknown cut count | [111_chp_partload__all__full, 112_chp_partload__auto__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full] | [111_chp_partload__all__full, 112_chp_partload__auto__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full] | PASS |
| B.50.bound | B ev | replay: runs bound to an original model | 278 | 278 | PASS |
| B.50b | B ev | complete model records (admitted runs) = replay admitted runs | [278, 278] | [278, 278] | PASS |
| B.51.inc | B ev | returned incumbents independently checked | 271 | 271 | PASS |
| B.51.incfail | B ev | checked incumbents that failed | 0 | 0 | PASS |
| B.51.reeval | B ev | incumbents re-evaluated by this script (stdlib evaluator): count, passing at 1e-5 | [271, 271] | [271, 271] | PASS |
| B.51.reevalmax | B ev | largest re-evaluated scaled violation / objective discrepancy <= 1e-5 | True | True ([9.979054992823033e-07, 9.770701392408654e-07]) | PASS |
| B.51.refconf | B ev | final or root dual bounds conflicting with reference | 0 | 0 | PASS |
| R.1 | repair-protocol | triggering records (overrun, recursion, total) | [46, 4, 50] | [46, 4, 50] | PASS |
| R.1b | repair-plan | triggering run ids equal the frozen plan | [001_p_ball_10b_5p_2d_m__all__full, 002_p_ball_10b_5p_2d_m__auto__full, 021_ex8_3_4__all__full, 022_ex8_3_4__auto__full, 030_hybriddynamic_var__all__full, 031_hybriddynamic_var__auto__full, 033_graphpart_clique-40__auto__full, 035_graphpart_clique-40__all__full, 037_pooling_adhya4pq__all__full, 038_pooling_adhya4pq__auto__full, 075_tln7__all__full, 076_tln7__auto__full, 082_graphpart_2g-0066-0066__all__full, 083_graphpart_2g-0066-0066__auto__full, 087_waterx__auto__full, 089_waterx__all__full, 091_genpooling_lee2__all__full, 092_genpooling_lee2__auto__full, 093_syn15m__all__full, 094_syn15m__auto__full, 100_cvxnonsep_pcon40r__all__full, 101_cvxnonsep_pcon40r__auto__full, 102_syn10hfsg__all__full, 103_syn10hfsg__auto__full, 105_btest14__auto__full, 107_btest14__all__full, 111_chp_partload__all__full, 112_chp_partload__auto__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full, 160_p_ball_10b_5p_2d_m__all__root, 161_p_ball_10b_5p_2d_m__auto__root, 171_nous1__all__root, 172_nous1__auto__root, 180_ex8_3_4__all__root, 181_ex8_3_4__auto__root, 189_hybriddynamic_var__all__root, 190_hybriddynamic_var__auto__root, 192_graphpart_clique-40__auto__root, 194_graphpart_clique-40__all__root, 196_pooling_adhya4pq__all__root, 197_pooling_adhya4pq__auto__root, 234_tln7__all__root, 235_tln7__auto__root, 241_graphpart_2g-0066-0066__all__root, 242_graphpart_2g-0066-0066__auto__root, 246_waterx__auto__root, 248_waterx__all__root, 265_p_ball_10b_5p_2d_m__all__repeat, 266_p_ball_10b_5p_2d_m__auto__repeat] | [001_p_ball_10b_5p_2d_m__all__full, 002_p_ball_10b_5p_2d_m__auto__full, 021_ex8_3_4__all__full, 022_ex8_3_4__auto__full, 030_hybriddynamic_var__all__full, 031_hybriddynamic_var__auto__full, 033_graphpart_clique-40__auto__full, 035_graphpart_clique-40__all__full, 037_pooling_adhya4pq__all__full, 038_pooling_adhya4pq__auto__full, 075_tln7__all__full, 076_tln7__auto__full, 082_graphpart_2g-0066-0066__all__full, 083_graphpart_2g-0066-0066__auto__full, 087_waterx__auto__full, 089_waterx__all__full, 091_genpooling_lee2__all__full, 092_genpooling_lee2__auto__full, 093_syn15m__all__full, 094_syn15m__auto__full, 100_cvxnonsep_pcon40r__all__full, 101_cvxnonsep_pcon40r__auto__full, 102_syn10hfsg__all__full, 103_syn10hfsg__auto__full, 105_btest14__auto__full, 107_btest14__all__full, 111_chp_partload__all__full, 112_chp_partload__auto__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full, 160_p_ball_10b_5p_2d_m__all__root, 161_p_ball_10b_5p_2d_m__auto__root, 171_nous1__all__root, 172_nous1__auto__root, 180_ex8_3_4__all__root, 181_ex8_3_4__auto__root, 189_hybriddynamic_var__all__root, 190_hybriddynamic_var__auto__root, 192_graphpart_clique-40__auto__root, 194_graphpart_clique-40__all__root, 196_pooling_adhya4pq__all__root, 197_pooling_adhya4pq__auto__root, 234_tln7__all__root, 235_tln7__auto__root, 241_graphpart_2g-0066-0066__all__root, 242_graphpart_2g-0066-0066__auto__root, 246_waterx__auto__root, 248_waterx__all__root, 265_p_ball_10b_5p_2d_m__all__repeat, 266_p_ball_10b_5p_2d_m__auto__repeat] | PASS |
| R.2 | B ev | selected model/phase/seed groups | 25 | 25 | PASS |
| R.2b | repair-plan | groups equal the frozen plan | [('btest14', 'full', 0), ('chp_partload', 'full', 0), ('cvxnonsep_pcon40r', 'full', 0), ('ex8_3_4', 'full', 0), ('ex8_3_4', 'root', 0), ('genpooling_lee2', 'full', 0), ('graphpart_2g-0066-0066', 'full', 0), ('graphpart_2g-0066-0066', 'root', 0), ('graphpart_clique-40', 'full', 0), ('graphpart_clique-40', 'root', 0), ('hybriddynamic_var', 'full', 0), ('hybriddynamic_var', 'root', 0), ('nous1', 'root', 0), ('p_ball_10b_5p_2d_m', 'full', 0), ('p_ball_10b_5p_2d_m', 'repeat', 1), ('p_ball_10b_5p_2d_m', 'root', 0), ('pooling_adhya4pq', 'full', 0), ('pooling_adhya4pq', 'root', 0), ('syn10hfsg', 'full', 0), ('syn15m', 'full', 0), ('tln7', 'full', 0), ('tln7', 'root', 0), ('waterno2_06', 'full', 0), ('waterx', 'full', 0), ('waterx', 'root', 0)] | [('btest14', 'full', 0), ('chp_partload', 'full', 0), ('cvxnonsep_pcon40r', 'full', 0), ('ex8_3_4', 'full', 0), ('ex8_3_4', 'root', 0), ('genpooling_lee2', 'full', 0), ('graphpart_2g-0066-0066', 'full', 0), ('graphpart_2g-0066-0066', 'root', 0), ('graphpart_clique-40', 'full', 0), ('graphpart_clique-40', 'root', 0), ('hybriddynamic_var', 'full', 0), ('hybriddynamic_var', 'root', 0), ('nous1', 'root', 0), ('p_ball_10b_5p_2d_m', 'full', 0), ('p_ball_10b_5p_2d_m', 'repeat', 1), ('p_ball_10b_5p_2d_m', 'root', 0), ('pooling_adhya4pq', 'full', 0), ('pooling_adhya4pq', 'root', 0), ('syn10hfsg', 'full', 0), ('syn15m', 'full', 0), ('tln7', 'full', 0), ('tln7', 'root', 0), ('waterno2_06', 'full', 0), ('waterx', 'full', 0), ('waterx', 'root', 0)] | PASS |
| R.3 | B ev | matched jobs = all three original modes per group, original order | [000_p_ball_10b_5p_2d_m__baseline__full, 001_p_ball_10b_5p_2d_m__all__full, 002_p_ball_10b_5p_2d_m__auto__full, 021_ex8_3_4__all__full, 022_ex8_3_4__auto__full, 023_ex8_3_4__baseline__full, 030_hybriddynamic_var__all__full, 031_hybriddynamic_var__auto__full, 032_hybriddynamic_var__baseline__full, 033_graphpart_clique-40__auto__full, 034_graphpart_clique-40__baseline__full, 035_graphpart_clique-40__all__full, 036_pooling_adhya4pq__baseline__full, 037_pooling_adhya4pq__all__full, 038_pooling_adhya4pq__auto__full, 075_tln7__all__full, 076_tln7__auto__full, 077_tln7__baseline__full, 081_graphpart_2g-0066-0066__baseline__full, 082_graphpart_2g-0066-0066__all__full, 083_graphpart_2g-0066-0066__auto__full, 087_waterx__auto__full, 088_waterx__baseline__full, 089_waterx__all__full, 090_genpooling_lee2__baseline__full, 091_genpooling_lee2__all__full, 092_genpooling_lee2__auto__full, 093_syn15m__all__full, 094_syn15m__auto__full, 095_syn15m__baseline__full, 099_cvxnonsep_pcon40r__baseline__full, 100_cvxnonsep_pcon40r__all__full, 101_cvxnonsep_pcon40r__auto__full, 102_syn10hfsg__all__full, 103_syn10hfsg__auto__full, 104_syn10hfsg__baseline__full, 105_btest14__auto__full, 106_btest14__baseline__full, 107_btest14__all__full, 111_chp_partload__all__full, 112_chp_partload__auto__full, 113_chp_partload__baseline__full, 117_waterno2_06__baseline__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full, 159_p_ball_10b_5p_2d_m__baseline__root, 160_p_ball_10b_5p_2d_m__all__root, 161_p_ball_10b_5p_2d_m__auto__root, 171_nous1__all__root, 172_nous1__auto__root, 173_nous1__baseline__root, 180_ex8_3_4__all__root, 181_ex8_3_4__auto__root, 182_ex8_3_4__baseline__root, 189_hybriddynamic_var__all__root, 190_hybriddynamic_var__auto__root, 191_hybriddynamic_var__baseline__root, 192_graphpart_clique-40__auto__root, 193_graphpart_clique-40__baseline__root, 194_graphpart_clique-40__all__root, 195_pooling_adhya4pq__baseline__root, 196_pooling_adhya4pq__all__root, 197_pooling_adhya4pq__auto__root, 234_tln7__all__root, 235_tln7__auto__root, 236_tln7__baseline__root, 240_graphpart_2g-0066-0066__baseline__root, 241_graphpart_2g-0066-0066__all__root, 242_graphpart_2g-0066-0066__auto__root, 246_waterx__auto__root, 247_waterx__baseline__root, 248_waterx__all__root, 264_p_ball_10b_5p_2d_m__baseline__repeat, 265_p_ball_10b_5p_2d_m__all__repeat, 266_p_ball_10b_5p_2d_m__auto__repeat] | [000_p_ball_10b_5p_2d_m__baseline__full, 001_p_ball_10b_5p_2d_m__all__full, 002_p_ball_10b_5p_2d_m__auto__full, 021_ex8_3_4__all__full, 022_ex8_3_4__auto__full, 023_ex8_3_4__baseline__full, 030_hybriddynamic_var__all__full, 031_hybriddynamic_var__auto__full, 032_hybriddynamic_var__baseline__full, 033_graphpart_clique-40__auto__full, 034_graphpart_clique-40__baseline__full, 035_graphpart_clique-40__all__full, 036_pooling_adhya4pq__baseline__full, 037_pooling_adhya4pq__all__full, 038_pooling_adhya4pq__auto__full, 075_tln7__all__full, 076_tln7__auto__full, 077_tln7__baseline__full, 081_graphpart_2g-0066-0066__baseline__full, 082_graphpart_2g-0066-0066__all__full, 083_graphpart_2g-0066-0066__auto__full, 087_waterx__auto__full, 088_waterx__baseline__full, 089_waterx__all__full, 090_genpooling_lee2__baseline__full, 091_genpooling_lee2__all__full, 092_genpooling_lee2__auto__full, 093_syn15m__all__full, 094_syn15m__auto__full, 095_syn15m__baseline__full, 099_cvxnonsep_pcon40r__baseline__full, 100_cvxnonsep_pcon40r__all__full, 101_cvxnonsep_pcon40r__auto__full, 102_syn10hfsg__all__full, 103_syn10hfsg__auto__full, 104_syn10hfsg__baseline__full, 105_btest14__auto__full, 106_btest14__baseline__full, 107_btest14__all__full, 111_chp_partload__all__full, 112_chp_partload__auto__full, 113_chp_partload__baseline__full, 117_waterno2_06__baseline__full, 118_waterno2_06__all__full, 119_waterno2_06__auto__full, 159_p_ball_10b_5p_2d_m__baseline__root, 160_p_ball_10b_5p_2d_m__all__root, 161_p_ball_10b_5p_2d_m__auto__root, 171_nous1__all__root, 172_nous1__auto__root, 173_nous1__baseline__root, 180_ex8_3_4__all__root, 181_ex8_3_4__auto__root, 182_ex8_3_4__baseline__root, 189_hybriddynamic_var__all__root, 190_hybriddynamic_var__auto__root, 191_hybriddynamic_var__baseline__root, 192_graphpart_clique-40__auto__root, 193_graphpart_clique-40__baseline__root, 194_graphpart_clique-40__all__root, 195_pooling_adhya4pq__baseline__root, 196_pooling_adhya4pq__all__root, 197_pooling_adhya4pq__auto__root, 234_tln7__all__root, 235_tln7__auto__root, 236_tln7__baseline__root, 240_graphpart_2g-0066-0066__baseline__root, 241_graphpart_2g-0066-0066__all__root, 242_graphpart_2g-0066-0066__auto__root, 246_waterx__auto__root, 247_waterx__baseline__root, 248_waterx__all__root, 264_p_ball_10b_5p_2d_m__baseline__repeat, 265_p_ball_10b_5p_2d_m__all__repeat, 266_p_ball_10b_5p_2d_m__auto__repeat] | PASS |
| R.4 | repair-protocol | soft budget sum / hard limit sum (s) | [1575.0, 2565.0] | [1575.0, 2565.0] | PASS |
| R.5 | B ev | phase, seed, time, node and process limits unchanged | True | True | PASS |
| R.5.runfiles | B ev | per-run JSON files that disagree with records.jsonl | 0 | 0 | PASS |
| R.6 | B ev | jobs completed | [75, 75] | [75, 75] | PASS |
| R.7 | B ev | outer wall seconds | 754.5 | 754.5104 | PASS |
| R.8 | B ev | worker errors / missing cut logs / hard timeouts | [0, 0, 0] | [0, 0, 0] | PASS |
| R.T.full.holdout.g | B ev | full/holdout: groups (records per mode) | [8, 8, 8] | [8, 8, 8] | PASS |
| R.T.full.holdout.s | B ev | full/holdout: solved per mode | [4, 4, 4] | [4, 4, 4] | PASS |
| R.T.full.holdout.id | B ev | full/holdout: same solved identities in all modes | True | True | PASS |
| R.T.full.holdout.c | B ev | full/holdout: cuts (baseline, all, auto) | [0, 12, 3] | [0, 12, 3] | PASS |
| R.T.full.diagnostic.g | B ev | full/diagnostic: groups (records per mode) | [7, 7, 7] | [7, 7, 7] | PASS |
| R.T.full.diagnostic.s | B ev | full/diagnostic: solved per mode | [4, 4, 4] | [4, 4, 4] | PASS |
| R.T.full.diagnostic.id | B ev | full/diagnostic: same solved identities in all modes | True | True | PASS |
| R.T.full.diagnostic.c | B ev | full/diagnostic: cuts (baseline, all, auto) | [0, 10, 0] | [0, 10, 0] | PASS |
| R.T.root.holdout.g | B ev | root/holdout: groups (records per mode) | [9, 9, 9] | [9, 9, 9] | PASS |
| R.T.root.holdout.s | B ev | root/holdout: solved per mode | [0, 0, 0] | [0, 0, 0] | PASS |
| R.T.root.holdout.id | B ev | root/holdout: same solved identities in all modes | True | True | PASS |
| R.T.root.holdout.c | B ev | root/holdout: cuts (baseline, all, auto) | [0, 11, 3] | [0, 11, 3] | PASS |
| R.T.repeat.holdout.g | B ev | repeat/holdout: groups (records per mode) | [1, 1, 1] | [1, 1, 1] | PASS |
| R.T.repeat.holdout.s | B ev | repeat/holdout: solved per mode | [1, 1, 1] | [1, 1, 1] | PASS |
| R.T.repeat.holdout.id | B ev | repeat/holdout: same solved identities in all modes | True | True | PASS |
| R.T.repeat.holdout.c | B ev | repeat/holdout: cuts (baseline, all, auto) | [0, 3, 0] | [0, 3, 0] | PASS |
| R.C.full.holdout.all | B ev | final dual vs matched baseline B/T/W/U (full, holdout, all) | [0, 5, 3, 0] | [0, 5, 3, 0] | PASS |
| R.C.full.holdout.auto | B ev | final dual vs matched baseline B/T/W/U (full, holdout, auto) | [0, 6, 2, 0] | [0, 6, 2, 0] | PASS |
| R.C.full.diagnostic.all | B ev | final dual vs matched baseline B/T/W/U (full, diagnostic, all) | [0, 6, 1, 0] | [0, 6, 1, 0] | PASS |
| R.C.full.diagnostic.auto | B ev | final dual vs matched baseline B/T/W/U (full, diagnostic, auto) | [0, 6, 1, 0] | [0, 6, 1, 0] | PASS |
| R.C.root.holdout.all | B ev | final dual vs matched baseline B/T/W/U (root, holdout, all) | [0, 9, 0, 0] | [0, 9, 0, 0] | PASS |
| R.C.root.holdout.auto | B ev | final dual vs matched baseline B/T/W/U (root, holdout, auto) | [0, 9, 0, 0] | [0, 9, 0, 0] | PASS |
| R.C.repeat.holdout.all | B ev | final dual vs matched baseline B/T/W/U (repeat, holdout, all) | [0, 1, 0, 0] | [0, 1, 0, 0] | PASS |
| R.C.repeat.holdout.auto | B ev | final dual vs matched baseline B/T/W/U (repeat, holdout, auto) | [0, 1, 0, 0] | [0, 1, 0, 0] | PASS |
| R.9.all | B ev | worse diagnostic bound (all) | [waterno2_06] | [waterno2_06] | PASS |
| R.9.auto | B ev | worse diagnostic bound (auto) | [waterno2_06] | [waterno2_06] | PASS |
| R.10.baseline | B ev | full holdout summed integration seconds (baseline) | 123.91 | 123.91293 | PASS |
| R.10.all | B ev | full holdout summed integration seconds (all) | 124.86 | 124.856 | PASS |
| R.10.auto | B ev | full holdout summed integration seconds (auto) | 124.82 | 124.81861 | PASS |
| R.M.full.holdout.baseline.t | repair results.md | full/holdout/baseline: integration seconds | 123.913 | 123.912932 | PASS |
| R.M.full.holdout.baseline.d | repair results.md | full/holdout/baseline: discovery seconds | 0.0 | 0.0 | PASS |
| R.M.full.holdout.baseline.i | repair results.md | full/holdout/baseline: incomplete discoveries | 0 | 0 | PASS |
| R.M.full.holdout.all.t | repair results.md | full/holdout/all: integration seconds | 124.856 | 124.856 | PASS |
| R.M.full.holdout.all.d | repair results.md | full/holdout/all: discovery seconds | 1.332 | 1.331893 | PASS |
| R.M.full.holdout.all.i | repair results.md | full/holdout/all: incomplete discoveries | 0 | 0 | PASS |
| R.M.full.holdout.auto.t | repair results.md | full/holdout/auto: integration seconds | 124.819 | 124.818612 | PASS |
| R.M.full.holdout.auto.d | repair results.md | full/holdout/auto: discovery seconds | 1.324 | 1.323823 | PASS |
| R.M.full.holdout.auto.i | repair results.md | full/holdout/auto: incomplete discoveries | 0 | 0 | PASS |
| R.M.full.diagnostic.baseline.t | repair results.md | full/diagnostic/baseline: integration seconds | 96.348 | 96.347988 | PASS |
| R.M.full.diagnostic.baseline.d | repair results.md | full/diagnostic/baseline: discovery seconds | 0.0 | 0.0 | PASS |
| R.M.full.diagnostic.baseline.i | repair results.md | full/diagnostic/baseline: incomplete discoveries | 0 | 0 | PASS |
| R.M.full.diagnostic.all.t | repair results.md | full/diagnostic/all: integration seconds | 95.496 | 95.495659 | PASS |
| R.M.full.diagnostic.all.d | repair results.md | full/diagnostic/all: discovery seconds | 2.852 | 2.851817 | PASS |
| R.M.full.diagnostic.all.i | repair results.md | full/diagnostic/all: incomplete discoveries | 2 | 2 | PASS |
| R.M.full.diagnostic.auto.t | repair results.md | full/diagnostic/auto: integration seconds | 96.718 | 96.71774 | PASS |
| R.M.full.diagnostic.auto.d | repair results.md | full/diagnostic/auto: discovery seconds | 2.9 | 2.89983 | PASS |
| R.M.full.diagnostic.auto.i | repair results.md | full/diagnostic/auto: incomplete discoveries | 2 | 2 | PASS |
| R.M.root.holdout.baseline.t | repair results.md | root/holdout/baseline: integration seconds | 5.854 | 5.854272 | PASS |
| R.M.root.holdout.baseline.d | repair results.md | root/holdout/baseline: discovery seconds | 0.0 | 0.0 | PASS |
| R.M.root.holdout.baseline.i | repair results.md | root/holdout/baseline: incomplete discoveries | 0 | 0 | PASS |
| R.M.root.holdout.all.t | repair results.md | root/holdout/all: integration seconds | 7.02 | 7.020308 | PASS |
| R.M.root.holdout.all.d | repair results.md | root/holdout/all: discovery seconds | 0.981 | 0.981376 | PASS |
| R.M.root.holdout.all.i | repair results.md | root/holdout/all: incomplete discoveries | 1 | 1 | PASS |
| R.M.root.holdout.auto.t | repair results.md | root/holdout/auto: integration seconds | 7.27 | 7.269806 | PASS |
| R.M.root.holdout.auto.d | repair results.md | root/holdout/auto: discovery seconds | 0.978 | 0.978483 | PASS |
| R.M.root.holdout.auto.i | repair results.md | root/holdout/auto: incomplete discoveries | 1 | 1 | PASS |
| R.M.repeat.holdout.baseline.t | repair results.md | repeat/holdout/baseline: integration seconds | 1.296 | 1.295861 | PASS |
| R.M.repeat.holdout.baseline.d | repair results.md | repeat/holdout/baseline: discovery seconds | 0.0 | 0.0 | PASS |
| R.M.repeat.holdout.baseline.i | repair results.md | repeat/holdout/baseline: incomplete discoveries | 0 | 0 | PASS |
| R.M.repeat.holdout.all.t | repair results.md | repeat/holdout/all: integration seconds | 1.913 | 1.913459 | PASS |
| R.M.repeat.holdout.all.d | repair results.md | repeat/holdout/all: discovery seconds | 0.147 | 0.146896 | PASS |
| R.M.repeat.holdout.all.i | repair results.md | repeat/holdout/all: incomplete discoveries | 0 | 0 | PASS |
| R.M.repeat.holdout.auto.t | repair results.md | repeat/holdout/auto: integration seconds | 1.45 | 1.449802 | PASS |
| R.M.repeat.holdout.auto.d | repair results.md | repeat/holdout/auto: discovery seconds | 0.14 | 0.13989 | PASS |
| R.M.repeat.holdout.auto.i | repair results.md | repeat/holdout/auto: incomplete discoveries | 0 | 0 | PASS |
| R.11 | B ev | discovery calls crossing the soft deadline / of which incomplete | [6, 6] | [6, 6] | PASS |
| R.12 | B ev | largest discovery excess (ms) | 3.618 | 3.617737 | PASS |
| R.13 | B ev | largest full-callback excess over the separation allowance (ms) | 29.529 | 29.529274 | PASS |
| R.14 | B ev | largest total soft-budget excess, all 75 records (ms) | 23.611 | 23.611235 | PASS |
| R.15 | B ev | formerly crashing four: incomplete discovery and a normal SCIP status | [True, True, True, True] | [True, True, True, True] | PASS |
| R.16.hashes | B ev | frozen source/input hashes (manifest entries) | 103 | 103 | PASS |
| R.16.hashok | B ev | manifest entries whose snapshot file is missing or has a different SHA256 | 0 | 0 | PASS |
| R.17.cuts | B ev | recorded added cuts (all phases, from records) | 42 | 42 | PASS |
| R.17.replayed | B ev | replay: cuts replayed | 42 | 42 | PASS |
| R.17.perrun | B ev | replay runs whose cut count differs from the record or was not fully replayed | 0 | 0 | PASS |
| R.17.passed | B ev | replay runs failed (and overall pass flag) | [0, True] | [0, True] | PASS |
| R.17.tamper | B ev | tampering controls rejected / total | [14, 14] | [14, 14] | PASS |
| R.17.srcfiles | B ev | replay: source/input hashes verified | 103 | 103 | PASS |
| R.17.missing | B ev | records with unknown cut count (no complete cut log) | 0 | 0 | PASS |
| R.17.omitted | B ev | replay omitted runs = records with unknown cut count | [] | [] | PASS |
| R.17.bound | B ev | replay: runs bound to an original model | 75 | 75 | PASS |
| R.18.inc | B ev | returned incumbents independently checked | 67 | 67 | PASS |
| R.18.incfail | B ev | checked incumbents that failed | 0 | 0 | PASS |
| R.18.reeval | B ev | incumbents re-evaluated by this script (stdlib evaluator): count, passing at 1e-5 | [67, 67] | [67, 67] | PASS |
| R.18.reevalmax | B ev | largest re-evaluated scaled violation / objective discrepancy <= 1e-5 | True | True ([7.984692308692087e-07, 1.9296228418613105e-08]) | PASS |
| R.18.refconf | B ev | final or root dual bounds conflicting with reference | 0 | 0 | PASS |
| R.19 | B ev | cuts replayed across the two current campaigns | 165 | 165 | PASS |

Checked 418 items (stated values and consistency checks): 418 pass, 0 mismatch.

## Paper-ready tables

### (a) Every instance where a cut mode added at least one cut

Time is integration time (v1: total+source read; v2/repair: total+preparation). 'unknown' = no complete cut log.

| Campaign | Suite | Phase | Seed | Instance | Mode | Status | Solved | Final dual | Root dual | Nodes | Time (s) | Cuts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v2 | holdout | full | 0 | nous1 | baseline | gaplimit | yes | 1.5669178 | 0.3451122 | 3177 | 2.68 | 0 |
| v2 | holdout | full | 0 | nous1 | all | gaplimit | yes | 1.567067 | 0.3451122 | 3967 | 4.57 | 2 |
| v2 | holdout | full | 0 | nous1 | auto | gaplimit | yes | 1.567067 | 0.3451122 | 3967 | 4.63 | 2 |
| v2 | holdout | full | 0 | ex4_1_8 | baseline | gaplimit | yes | -16.739657 | -16.739657 | 1 | 0.04 | 0 |
| v2 | holdout | full | 0 | ex4_1_8 | all | gaplimit | yes | -16.73987 | -16.73987 | 1 | 0.11 | 5 |
| v2 | holdout | full | 0 | ex4_1_8 | auto | gaplimit | yes | -16.739657 | -16.739657 | 1 | 0.04 | 0 |
| v2 | holdout | full | 0 | cvxnonsep_normcon20r | baseline | gaplimit | yes | -21.74926 | -21.74926 | 1 | 0.09 | 0 |
| v2 | holdout | full | 0 | cvxnonsep_normcon20r | all | gaplimit | yes | -21.749606 | -21.749606 | 1 | 0.33 | 12 |
| v2 | holdout | full | 0 | cvxnonsep_normcon20r | auto | gaplimit | yes | -21.74926 | -21.74926 | 1 | 0.27 | 0 |
| v2 | holdout | full | 0 | cvxnonsep_psig20r | baseline | gaplimit | yes | 95.893364 | 35.602921 | 12 | 0.10 | 0 |
| v2 | holdout | full | 0 | cvxnonsep_psig20r | all | gaplimit | yes | 95.892449 | 35.603102 | 11 | 0.55 | 10 |
| v2 | holdout | full | 0 | cvxnonsep_psig20r | auto | gaplimit | yes | 95.893364 | 35.602921 | 12 | 0.30 | 0 |
| v2 | holdout | full | 0 | st_e22 | baseline | gaplimit | yes | -85.00192 | -85.00192 | 1 | 0.04 | 0 |
| v2 | holdout | full | 0 | st_e22 | all | optimal | yes | -85.000002 | - | 1 | 0.04 | 1 |
| v2 | holdout | full | 0 | st_e22 | auto | optimal | yes | -85.000002 | - | 1 | 0.04 | 1 |
| v2 | holdout | full | 0 | kall_congruentcircles_c51 | baseline | optimal | yes | 1.0730084 | 0 | 4881 | 2.94 | 0 |
| v2 | holdout | full | 0 | kall_congruentcircles_c51 | all | optimal | yes | 1.0730091 | 0 | 3880 | 3.43 | 6 |
| v2 | holdout | full | 0 | kall_congruentcircles_c51 | auto | optimal | yes | 1.0730082 | 0 | 4704 | 4.06 | 7 |
| v2 | holdout | full | 0 | syn05m | baseline | optimal | yes | 837.7324 | - | 1 | 0.06 | 0 |
| v2 | holdout | full | 0 | syn05m | all | optimal | yes | 837.7324 | - | 1 | 0.25 | 2 |
| v2 | holdout | full | 0 | syn05m | auto | optimal | yes | 837.7324 | - | 1 | 0.16 | 0 |
| v2 | diagnostic | full | 0 | cvxnonsep_psig30r | baseline | gaplimit | yes | 78.991537 | 70.048314 | 4 | 0.19 | 0 |
| v2 | diagnostic | full | 0 | cvxnonsep_psig30r | all | gaplimit | yes | 78.991537 | 70.048314 | 4 | 1.02 | 11 |
| v2 | diagnostic | full | 0 | cvxnonsep_psig30r | auto | gaplimit | yes | 78.991537 | 70.048314 | 4 | 0.84 | 0 |
| v2 | diagnostic | full | 0 | kall_circles_c6b | baseline | timelimit | no | 0.74495687 | 0 | 33492 | 30.02 | 0 |
| v2 | diagnostic | full | 0 | kall_circles_c6b | all | timelimit | no | 0.89605748 | 0 | 32792 | 30.02 | 4 |
| v2 | diagnostic | full | 0 | kall_circles_c6b | auto | timelimit | no | 0.57733109 | 0 | 33585 | 30.02 | 5 |
| v2 | synthetic | full | 0 | exp_pair | baseline | optimal | yes | 3 | - | 1 | 0.04 | 0 |
| v2 | synthetic | full | 0 | exp_pair | all | optimal | yes | 3 | - | 1 | 0.11 | 1 |
| v2 | synthetic | full | 0 | exp_pair | auto | optimal | yes | 3 | - | 1 | 0.05 | 0 |
| v2 | synthetic | full | 0 | trig_pair | baseline | gaplimit | yes | -1.414263 | -1.414263 | 1 | 0.03 | 0 |
| v2 | synthetic | full | 0 | trig_pair | all | gaplimit | yes | -1.414263 | -1.414263 | 1 | 0.07 | 2 |
| v2 | synthetic | full | 0 | trig_pair | auto | gaplimit | yes | -1.414263 | -1.414263 | 1 | 0.03 | 0 |
| v2 | synthetic | full | 0 | simplex_quadratic_vector | baseline | gaplimit | yes | -0.50000653 | -0.50027374 | 3 | 0.04 | 0 |
| v2 | synthetic | full | 0 | simplex_quadratic_vector | all | optimal | yes | -0.50000002 | - | 1 | 0.06 | 2 |
| v2 | synthetic | full | 0 | simplex_quadratic_vector | auto | optimal | yes | -0.50000002 | - | 1 | 0.07 | 2 |
| v2 | synthetic | full | 0 | star_marginal_inconsistency | baseline | optimal | yes | 0.0078124899 | - | 1 | 0.09 | 0 |
| v2 | synthetic | full | 0 | star_marginal_inconsistency | all | gaplimit | yes | 0.0078120225 | 0.0078120225 | 1 | 0.17 | 8 |
| v2 | synthetic | full | 0 | star_marginal_inconsistency | auto | optimal | yes | 0.0078124899 | - | 1 | 0.12 | 0 |
| v2 | holdout | root | 0 | ex4_1_8 | baseline | gaplimit | yes | -16.739657 | -16.739657 | 1 | 0.03 | 0 |
| v2 | holdout | root | 0 | ex4_1_8 | all | gaplimit | yes | -16.73987 | -16.73987 | 1 | 0.13 | 5 |
| v2 | holdout | root | 0 | ex4_1_8 | auto | gaplimit | yes | -16.739657 | -16.739657 | 1 | 0.04 | 0 |
| v2 | holdout | root | 0 | cvxnonsep_normcon20r | baseline | gaplimit | yes | -21.74926 | -21.74926 | 1 | 0.08 | 0 |
| v2 | holdout | root | 0 | cvxnonsep_normcon20r | all | gaplimit | yes | -21.749305 | -21.749305 | 1 | 0.34 | 11 |
| v2 | holdout | root | 0 | cvxnonsep_normcon20r | auto | gaplimit | yes | -21.74926 | -21.74926 | 1 | 0.25 | 0 |
| v2 | holdout | root | 0 | cvxnonsep_psig20r | baseline | nodelimit | no | 35.602921 | 35.602921 | 1 | 0.11 | 0 |
| v2 | holdout | root | 0 | cvxnonsep_psig20r | all | nodelimit | no | 35.602921 | 35.602921 | 1 | 0.37 | 1 |
| v2 | holdout | root | 0 | cvxnonsep_psig20r | auto | nodelimit | no | 35.602921 | 35.602921 | 1 | 0.30 | 0 |
| v2 | holdout | root | 0 | st_e22 | baseline | gaplimit | yes | -85.00192 | -85.00192 | 1 | 0.04 | 0 |
| v2 | holdout | root | 0 | st_e22 | all | optimal | yes | -85.000002 | - | 1 | 0.05 | 1 |
| v2 | holdout | root | 0 | st_e22 | auto | optimal | yes | -85.000002 | - | 1 | 0.05 | 1 |
| v2 | holdout | root | 0 | kall_congruentcircles_c51 | baseline | nodelimit | no | 0 | 0 | 1 | 0.30 | 0 |
| v2 | holdout | root | 0 | kall_congruentcircles_c51 | all | nodelimit | no | 0 | 0 | 1 | 0.54 | 1 |
| v2 | holdout | root | 0 | kall_congruentcircles_c51 | auto | nodelimit | no | 0 | 0 | 1 | 0.55 | 1 |
| v2 | holdout | root | 0 | syn05m | baseline | optimal | yes | 837.7324 | - | 1 | 0.04 | 0 |
| v2 | holdout | root | 0 | syn05m | all | optimal | yes | 837.7324 | - | 1 | 0.21 | 2 |
| v2 | holdout | root | 0 | syn05m | auto | optimal | yes | 837.7324 | - | 1 | 0.12 | 0 |
| v2 | synthetic | root | 0 | exp_pair | baseline | optimal | yes | 3 | - | 1 | 0.04 | 0 |
| v2 | synthetic | root | 0 | exp_pair | all | optimal | yes | 3 | - | 1 | 0.11 | 1 |
| v2 | synthetic | root | 0 | exp_pair | auto | optimal | yes | 3 | - | 1 | 0.05 | 0 |
| v2 | synthetic | root | 0 | simplex_quadratic_vector | baseline | nodelimit | no | -0.50027374 | -0.50027374 | 1 | 0.06 | 0 |
| v2 | synthetic | root | 0 | simplex_quadratic_vector | all | optimal | yes | -0.50000002 | - | 1 | 0.10 | 2 |
| v2 | synthetic | root | 0 | simplex_quadratic_vector | auto | optimal | yes | -0.50000002 | - | 1 | 0.07 | 2 |
| v2 | synthetic | root | 0 | star_marginal_inconsistency | baseline | nodelimit | no | 0.007812499 | 0.007812499 | 1 | 0.07 | 0 |
| v2 | synthetic | root | 0 | star_marginal_inconsistency | all | gaplimit | yes | 0.0078120225 | 0.0078120225 | 1 | 0.21 | 8 |
| v2 | synthetic | root | 0 | star_marginal_inconsistency | auto | nodelimit | no | 0.007812499 | 0.007812499 | 1 | 0.12 | 0 |
| v2 | holdout | repeat | 1 | nous1 | baseline | optimal | yes | 1.5670719 | 0.3451122 | 3323 | 2.89 | 0 |
| v2 | holdout | repeat | 1 | nous1 | all | optimal | yes | 1.5670719 | 0.3451122 | 3863 | 4.24 | 2 |
| v2 | holdout | repeat | 1 | nous1 | auto | optimal | yes | 1.5670719 | 0.3451122 | 3863 | 4.22 | 2 |

| Campaign | Suite | Phase | Seed | Instance | Mode | Status | Solved | Final dual | Root dual | Nodes | Time (s) | Cuts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| repair | holdout | full | 0 | p_ball_10b_5p_2d_m | baseline | optimal | yes | 18.718576 | 0 | 325 | 1.54 | 0 |
| repair | holdout | full | 0 | p_ball_10b_5p_2d_m | all | optimal | yes | 18.718577 | 0 | 330 | 1.78 | 3 |
| repair | holdout | full | 0 | p_ball_10b_5p_2d_m | auto | optimal | yes | 18.718576 | 0 | 325 | 1.62 | 0 |
| repair | holdout | full | 0 | ex8_3_4 | baseline | timelimit | no | -10 | -10 | 6326 | 30.02 | 0 |
| repair | holdout | full | 0 | ex8_3_4 | all | timelimit | no | -10 | -10 | 6577 | 30.02 | 6 |
| repair | holdout | full | 0 | ex8_3_4 | auto | timelimit | no | -10 | -10 | 6247 | 30.02 | 0 |
| repair | holdout | full | 0 | hybriddynamic_var | baseline | gaplimit | yes | 1.5362949 | 1.5040996 | 1117 | 0.53 | 0 |
| repair | holdout | full | 0 | hybriddynamic_var | all | gaplimit | yes | 1.5362925 | 1.5040995 | 1081 | 0.72 | 2 |
| repair | holdout | full | 0 | hybriddynamic_var | auto | gaplimit | yes | 1.5362925 | 1.5040995 | 1081 | 0.80 | 2 |
| repair | holdout | full | 0 | pooling_adhya4pq | baseline | optimal | yes | -877.64575 | -961.93218 | 101 | 0.69 | 0 |
| repair | holdout | full | 0 | pooling_adhya4pq | all | optimal | yes | -877.64574 | -961.93218 | 142 | 1.21 | 1 |
| repair | holdout | full | 0 | pooling_adhya4pq | auto | optimal | yes | -877.64574 | -961.93218 | 142 | 1.22 | 1 |
| repair | diagnostic | full | 0 | genpooling_lee2 | baseline | optimal | yes | -3849.2654 | -4957.9223 | 2006 | 5.61 | 0 |
| repair | diagnostic | full | 0 | genpooling_lee2 | all | optimal | yes | -3849.2654 | -5158.0058 | 1296 | 4.15 | 2 |
| repair | diagnostic | full | 0 | genpooling_lee2 | auto | optimal | yes | -3849.2654 | -4957.9223 | 2006 | 5.76 | 0 |
| repair | diagnostic | full | 0 | syn15m | baseline | gaplimit | yes | 853.28609 | 853.28609 | 1 | 0.11 | 0 |
| repair | diagnostic | full | 0 | syn15m | all | gaplimit | yes | 853.28672 | 853.28672 | 1 | 0.49 | 8 |
| repair | diagnostic | full | 0 | syn15m | auto | gaplimit | yes | 853.28609 | 853.28609 | 1 | 0.16 | 0 |
| repair | holdout | root | 0 | p_ball_10b_5p_2d_m | baseline | nodelimit | no | 0 | 0 | 1 | 0.63 | 0 |
| repair | holdout | root | 0 | p_ball_10b_5p_2d_m | all | nodelimit | no | 0 | 0 | 1 | 0.70 | 3 |
| repair | holdout | root | 0 | p_ball_10b_5p_2d_m | auto | nodelimit | no | 0 | 0 | 1 | 0.75 | 0 |
| repair | holdout | root | 0 | nous1 | baseline | nodelimit | no | 0.3451122 | 0.3451122 | 1 | 0.14 | 0 |
| repair | holdout | root | 0 | nous1 | all | nodelimit | no | 0.3451122 | 0.3451122 | 1 | 0.42 | 0 |
| repair | holdout | root | 0 | nous1 | auto | nodelimit | no | 0.3451122 | 0.3451122 | 1 | 0.43 | 1 |
| repair | holdout | root | 0 | ex8_3_4 | baseline | nodelimit | no | -10 | -10 | 1 | 0.63 | 0 |
| repair | holdout | root | 0 | ex8_3_4 | all | nodelimit | no | -10 | -10 | 1 | 0.87 | 6 |
| repair | holdout | root | 0 | ex8_3_4 | auto | nodelimit | no | -10 | -10 | 1 | 0.79 | 0 |
| repair | holdout | root | 0 | hybriddynamic_var | baseline | nodelimit | no | 1.5040996 | 1.5040996 | 1 | 0.09 | 0 |
| repair | holdout | root | 0 | hybriddynamic_var | all | nodelimit | no | 1.5040995 | 1.5040995 | 1 | 0.26 | 2 |
| repair | holdout | root | 0 | hybriddynamic_var | auto | nodelimit | no | 1.5040995 | 1.5040995 | 1 | 0.27 | 2 |
| repair | holdout | repeat | 1 | p_ball_10b_5p_2d_m | baseline | optimal | yes | 18.718574 | 0 | 436 | 1.30 | 0 |
| repair | holdout | repeat | 1 | p_ball_10b_5p_2d_m | all | optimal | yes | 18.718574 | 0 | 298 | 1.91 | 3 |
| repair | holdout | repeat | 1 | p_ball_10b_5p_2d_m | auto | optimal | yes | 18.718574 | 0 | 436 | 1.45 | 0 |

| Campaign | Suite | Phase | Seed | Instance | Mode | Status | Solved | Final dual | Root dual | Nodes | Time (s) | Cuts |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | synthetic | full | 0 | quartic_balance_4 | baseline | optimal | yes | -1.000001 | -2.433976 | 177 | 0.19 | 0 |
| v1 | synthetic | full | 0 | quartic_balance_4 | control | optimal | yes | -1.0000019 | -2.433976 | 190 | 0.25 | 0 |
| v1 | synthetic | full | 0 | quartic_balance_4 | all | gaplimit | yes | -1.0000854 | -1.0265167 | 95 | 0.29 | 20 |
| v1 | synthetic | full | 0 | quartic_balance_4 | auto | gaplimit | yes | -1.0000854 | -1.0265167 | 95 | 0.42 | 20 |
| v1 | synthetic | full | 0 | quartic_balance_8 | baseline | timelimit | no | -2.5867279 | -7.7391145 | 5015 | 6.00 | 0 |
| v1 | synthetic | full | 0 | quartic_balance_8 | control | optimal | yes | -2.0000041 | -5.9139848 | 1506 | 1.05 | 0 |
| v1 | synthetic | full | 0 | quartic_balance_8 | all | gaplimit | yes | -2.0001491 | -3.0053743 | 951 | 0.78 | 24 |
| v1 | synthetic | full | 0 | quartic_balance_8 | auto | gaplimit | yes | -2.0001491 | -3.0053743 | 951 | 0.78 | 24 |
| v1 | synthetic | full | 0 | trig_pair | baseline | gaplimit | yes | -1.414263 | -1.414263 | 1 | 0.02 | 0 |
| v1 | synthetic | full | 0 | trig_pair | control | gaplimit | yes | -1.4142329 | -1.4142329 | 1 | 0.03 | 0 |
| v1 | synthetic | full | 0 | trig_pair | all | gaplimit | yes | -1.4142693 | -1.4142693 | 1 | 0.13 | 5 |
| v1 | synthetic | full | 0 | trig_pair | auto | gaplimit | yes | -1.4142693 | -1.4142693 | 1 | 0.10 | 5 |
| v1 | synthetic | full | 0 | simplex_product | baseline | optimal | yes | -0.25000001 | - | 1 | 0.03 | 0 |
| v1 | synthetic | full | 0 | simplex_product | control | optimal | yes | -0.25 | - | 1 | 0.03 | 0 |
| v1 | synthetic | full | 0 | simplex_product | all | optimal | yes | -0.25 | - | 1 | 0.06 | 1 |
| v1 | synthetic | full | 0 | simplex_product | auto | optimal | yes | -0.25 | - | 1 | 0.04 | 1 |
| v1 | synthetic | full | 0 | simplex_quadratic_vector | baseline | gaplimit | yes | -0.50000653 | -0.50027374 | 3 | 0.04 | 0 |
| v1 | synthetic | full | 0 | simplex_quadratic_vector | control | optimal | yes | -0.50000001 | - | 1 | 0.02 | 0 |
| v1 | synthetic | full | 0 | simplex_quadratic_vector | all | optimal | yes | -0.50000123 | -0.50129845 | 5 | 0.14 | 9 |
| v1 | synthetic | full | 0 | simplex_quadratic_vector | auto | optimal | yes | -0.50000069 | -0.50016228 | 5 | 0.08 | 5 |
| v1 | synthetic | full | 0 | overlapping_products | baseline | optimal | yes | -0.50000001 | - | 1 | 0.03 | 0 |
| v1 | synthetic | full | 0 | overlapping_products | control | optimal | yes | -0.50000001 | - | 1 | 0.03 | 0 |
| v1 | synthetic | full | 0 | overlapping_products | all | optimal | yes | -0.50000001 | - | 1 | 0.41 | 13 |
| v1 | synthetic | full | 0 | overlapping_products | auto | optimal | yes | -0.50000001 | - | 1 | 0.40 | 12 |
| v1 | synthetic | full | 0 | star_marginal_inconsistency | baseline | optimal | yes | 0.0078124899 | - | 1 | 0.10 | 0 |
| v1 | synthetic | full | 0 | star_marginal_inconsistency | control | optimal | yes | 0.0078119454 | -0.00010673899 | 9 | 0.10 | 0 |
| v1 | synthetic | full | 0 | star_marginal_inconsistency | all | optimal | yes | 0.0078124091 | -7.6812463e-05 | 11 | 0.50 | 17 |
| v1 | synthetic | full | 0 | star_marginal_inconsistency | auto | optimal | yes | 0.0078116462 | -0.00012803018 | 9 | 0.48 | 5 |
| v1 | holdout | full | 0 | kall_congruentcircles_c42 | baseline | optimal | yes | 0.8584072 | 0 | 123 | 0.23 | 0 |
| v1 | holdout | full | 0 | kall_congruentcircles_c42 | control | gaplimit | yes | 0.85835206 | 0 | 131 | 0.33 | 0 |
| v1 | holdout | full | 0 | kall_congruentcircles_c42 | all | optimal | yes | 0.85840614 | 0 | 289 | 0.80 | 21 |
| v1 | holdout | full | 0 | kall_congruentcircles_c42 | auto | gaplimit | yes | 0.85836401 | 0 | 141 | 0.55 | 13 |
| v1 | holdout | full | 0 | pooling_adhya2stp | baseline | gaplimit | yes | -549.85464 | -574.78261 | 831 | 0.92 | 0 |
| v1 | holdout | full | 0 | pooling_adhya2stp | control | gaplimit | yes | -549.85514 | -574.78261 | 421 | 1.63 | 0 |
| v1 | holdout | full | 0 | pooling_adhya2stp | all | gaplimit | yes | -549.85478 | -574.78261 | 401 | 2.67 | 15 |
| v1 | holdout | full | 0 | pooling_adhya2stp | auto | gaplimit | yes | -549.84896 | -574.78261 | 671 | 2.36 | 11 |
| v1 | holdout | full | 0 | ex4 | baseline | optimal | yes | -8.0641362 | -9.7648404 | 15 | 0.89 | 0 |
| v1 | holdout | full | 0 | ex4 | control | optimal | yes | -8.0641362 | -9.3916537 | 18 | 1.47 | 0 |
| v1 | holdout | full | 0 | ex4 | all | optimal | yes | -8.0641362 | - | 20 | 1.43 | 14 |
| v1 | holdout | full | 0 | ex4 | auto | optimal | yes | -8.0641362 | -9.3916537 | 18 | 1.36 | 0 |
| v1 | holdout | full | 0 | genpooling_lee2 | baseline | optimal | yes | -3849.2654 | -4957.9223 | 2006 | 5.61 | 0 |
| v1 | holdout | full | 0 | genpooling_lee2 | control | optimal | yes | -3849.2654 | -4939.0902 | 2738 | 4.89 | 0 |
| v1 | holdout | full | 0 | genpooling_lee2 | all | timelimit | no | -4303.588 | -4928.544 | 1050 | 6.00 | 23 |
| v1 | holdout | full | 0 | genpooling_lee2 | auto | timelimit | no | -4373.813 | -4931.716 | 1007 | 6.00 | 24 |
| v1 | holdout | full | 0 | cvxnonsep_normcon30r | baseline | optimal | yes | -34.243967 | - | 1 | 0.08 | 0 |
| v1 | holdout | full | 0 | cvxnonsep_normcon30r | control | optimal | yes | -34.243967 | - | 1 | 0.15 | 0 |
| v1 | holdout | full | 0 | cvxnonsep_normcon30r | all | optimal | yes | -34.243967 | - | 1 | 0.43 | 24 |
| v1 | holdout | full | 0 | cvxnonsep_normcon30r | auto | optimal | yes | -34.243967 | - | 1 | 0.14 | 0 |
| v1 | holdout | full | 0 | pointpack06 | baseline | optimal | yes | 0.36111164 | 1.1485993 | 2099 | 1.37 | 0 |
| v1 | holdout | full | 0 | pointpack06 | control | optimal | yes | 0.36111209 | 1.1485993 | 2586 | 2.51 | 0 |
| v1 | holdout | full | 0 | pointpack06 | all | optimal | yes | 0.36111224 | 0.83333333 | 2493 | 2.86 | 24 |
| v1 | holdout | full | 0 | pointpack06 | auto | optimal | yes | 0.36111281 | 0.83333333 | 2257 | 2.45 | 15 |
| v1 | holdout | full | 0 | tltr | baseline | optimal | yes | 48.066667 | - | 1 | 0.07 | 0 |
| v1 | holdout | full | 0 | tltr | control | optimal | yes | 48.066667 | - | 1 | 0.25 | 0 |
| v1 | holdout | full | 0 | tltr | all | optimal | yes | 48.066667 | - | 1 | 0.82 | 22 |
| v1 | holdout | full | 0 | tltr | auto | optimal | yes | 48.066667 | - | 1 | 0.60 | 11 |
| v1 | holdout | full | 0 | ex7_2_4 | baseline | gaplimit | yes | 3.9177418 | 2.3769505 | 1831 | 1.25 | 0 |
| v1 | holdout | full | 0 | ex7_2_4 | control | gaplimit | yes | 3.9176201 | 2.2383875 | 2591 | 1.96 | 0 |
| v1 | holdout | full | 0 | ex7_2_4 | all | gaplimit | yes | 3.9177138 | 2.268134 | 1671 | 1.68 | 13 |
| v1 | holdout | full | 0 | ex7_2_4 | auto | gaplimit | yes | 3.9177833 | 2.225963 | 1942 | 1.61 | 5 |
| v1 | holdout | full | 0 | pooling_adhya2pq | baseline | gaplimit | yes | -549.84226 | -572.4023 | 481 | 0.37 | 0 |
| v1 | holdout | full | 0 | pooling_adhya2pq | control | gaplimit | yes | -549.85205 | -572.4023 | 481 | 0.51 | 0 |
| v1 | holdout | full | 0 | pooling_adhya2pq | all | gaplimit | yes | -549.84919 | -572.4023 | 581 | 1.23 | 21 |
| v1 | holdout | full | 0 | pooling_adhya2pq | auto | gaplimit | yes | -549.85202 | -574.78261 | 499 | 0.96 | 9 |
| v1 | holdout | full | 0 | cvxnonsep_normcon40 | baseline | optimal | yes | -32.629671 | -58.267502 | 7 | 0.07 | 0 |
| v1 | holdout | full | 0 | cvxnonsep_normcon40 | control | optimal | yes | -32.629671 | -58.267506 | 3 | 0.33 | 0 |
| v1 | holdout | full | 0 | cvxnonsep_normcon40 | all | optimal | yes | -32.629671 | -58.267506 | 3 | 0.58 | 24 |
| v1 | holdout | full | 0 | cvxnonsep_normcon40 | auto | optimal | yes | -32.629671 | -58.267506 | 3 | 0.35 | 0 |
| v1 | holdout | full | 0 | ex1265a | baseline | optimal | yes | 10.3 | - | 1 | 0.07 | 0 |
| v1 | holdout | full | 0 | ex1265a | control | optimal | yes | 10.3 | - | 1 | 0.10 | 0 |
| v1 | holdout | full | 0 | ex1265a | all | optimal | yes | 10.3 | - | 1 | 0.20 | 5 |
| v1 | holdout | full | 0 | ex1265a | auto | optimal | yes | 10.3 | - | 1 | 0.12 | 0 |
| v1 | holdout | full | 0 | kall_circles_c6b | baseline | timelimit | no | 0 | 0 | 6323 | 6.02 | 0 |
| v1 | holdout | full | 0 | kall_circles_c6b | control | timelimit | no | 0 | 0 | 2521 | 6.00 | 0 |
| v1 | holdout | full | 0 | kall_circles_c6b | all | timelimit | no | 0 | 0 | 2381 | 6.00 | 24 |
| v1 | holdout | full | 0 | kall_circles_c6b | auto | timelimit | no | 0 | 0 | 2136 | 6.00 | 18 |
| v1 | historical | full | 0 | waterno2_06 | baseline | timelimit | no | 26.590876 | 26.590876 | 1 | 6.00 | 0 |
| v1 | historical | full | 0 | waterno2_06 | control | timelimit | no | 21.167212 | 21.167212 | 1 | 6.00 | 0 |
| v1 | historical | full | 0 | waterno2_06 | all | timelimit | no | 7.0515052 | 7.0515052 | 1 | 6.00 | 24 |
| v1 | historical | full | 0 | waterno2_06 | auto | timelimit | no | 2.4078412 | 2.4078412 | 1 | 6.02 | 24 |
| v1 | synthetic | root | 0 | quartic_balance_8 | baseline | nodelimit | no | -7.7391145 | -7.7391145 | 1 | 0.10 | 0 |
| v1 | synthetic | root | 0 | quartic_balance_8 | control | nodelimit | no | -5.9139848 | -5.9139848 | 1 | 0.11 | 0 |
| v1 | synthetic | root | 0 | quartic_balance_8 | all | nodelimit | no | -3.0053743 | -3.0053743 | 1 | 0.25 | 24 |
| v1 | synthetic | root | 0 | quartic_balance_8 | auto | nodelimit | no | -3.0053743 | -3.0053743 | 1 | 0.23 | 24 |
| v1 | synthetic | root | 0 | simplex_quadratic_vector | baseline | nodelimit | no | -0.50027374 | -0.50027374 | 1 | 0.04 | 0 |
| v1 | synthetic | root | 0 | simplex_quadratic_vector | control | optimal | yes | -0.50000001 | - | 1 | 0.03 | 0 |
| v1 | synthetic | root | 0 | simplex_quadratic_vector | all | nodelimit | no | -0.50129845 | -0.50129845 | 1 | 0.12 | 9 |
| v1 | synthetic | root | 0 | simplex_quadratic_vector | auto | nodelimit | no | -0.50016228 | -0.50016228 | 1 | 0.10 | 5 |
| v1 | synthetic | root | 0 | overlapping_products | baseline | optimal | yes | -0.50000001 | - | 1 | 0.03 | 0 |
| v1 | synthetic | root | 0 | overlapping_products | control | optimal | yes | -0.50000001 | - | 1 | 0.04 | 0 |
| v1 | synthetic | root | 0 | overlapping_products | all | optimal | yes | -0.50000001 | - | 1 | 0.38 | 2 |
| v1 | synthetic | root | 0 | overlapping_products | auto | optimal | yes | -0.50000001 | - | 1 | 0.39 | 2 |
| v1 | synthetic | root | 0 | star_marginal_inconsistency | baseline | nodelimit | no | 0.007812499 | 0.007812499 | 1 | 0.07 | 0 |
| v1 | synthetic | root | 0 | star_marginal_inconsistency | control | nodelimit | no | -0.00010673899 | -0.00010673899 | 1 | 0.08 | 0 |
| v1 | synthetic | root | 0 | star_marginal_inconsistency | all | nodelimit | no | -7.3113013e-05 | -7.3113013e-05 | 1 | 0.46 | 4 |
| v1 | synthetic | root | 0 | star_marginal_inconsistency | auto | nodelimit | no | -0.00010673899 | -0.00010673899 | 1 | 0.41 | 1 |
| v1 | holdout | root | 0 | kall_congruentcircles_c42 | baseline | nodelimit | no | 0 | 0 | 1 | 0.13 | 0 |
| v1 | holdout | root | 0 | kall_congruentcircles_c42 | control | nodelimit | no | 0 | 0 | 1 | 0.24 | 0 |
| v1 | holdout | root | 0 | kall_congruentcircles_c42 | all | nodelimit | no | 0 | 0 | 1 | 0.56 | 20 |
| v1 | holdout | root | 0 | kall_congruentcircles_c42 | auto | nodelimit | no | 0 | 0 | 1 | 0.46 | 13 |
| v1 | holdout | root | 0 | pooling_adhya2stp | baseline | nodelimit | no | -574.78261 | -574.78261 | 1 | 0.40 | 0 |
| v1 | holdout | root | 0 | pooling_adhya2stp | control | nodelimit | no | -574.78261 | -574.78261 | 1 | 1.62 | 0 |
| v1 | holdout | root | 0 | pooling_adhya2stp | all | nodelimit | no | -574.78261 | -574.78261 | 1 | 1.97 | 6 |
| v1 | holdout | root | 0 | pooling_adhya2stp | auto | nodelimit | no | -574.78261 | -574.78261 | 1 | 1.91 | 1 |
| v1 | holdout | root | 0 | ex4 | baseline | nodelimit | no | -10.761374 | -10.761374 | 1 | 0.43 | 0 |
| v1 | holdout | root | 0 | ex4 | control | nodelimit | no | -10.610223 | -10.610223 | 1 | 0.50 | 0 |
| v1 | holdout | root | 0 | ex4 | all | nodelimit | no | -10.025166 | -10.025166 | 1 | 0.68 | 14 |
| v1 | holdout | root | 0 | ex4 | auto | nodelimit | no | -10.610223 | -10.610223 | 1 | 0.53 | 0 |
| v1 | holdout | root | 0 | genpooling_lee2 | baseline | nodelimit | no | -5094.1987 | -5094.1987 | 1 | 0.78 | 0 |
| v1 | holdout | root | 0 | genpooling_lee2 | control | nodelimit | no | -4993.6194 | -4993.6194 | 1 | 0.92 | 0 |
| v1 | holdout | root | 0 | genpooling_lee2 | all | nodelimit | no | -4997.4949 | -4997.4949 | 1 | 1.34 | 6 |
| v1 | holdout | root | 0 | genpooling_lee2 | auto | nodelimit | no | -4994.9826 | -4994.9826 | 1 | 1.27 | 1 |
| v1 | holdout | root | 0 | cvxnonsep_normcon30r | baseline | optimal | yes | -34.243967 | - | 1 | 0.08 | 0 |
| v1 | holdout | root | 0 | cvxnonsep_normcon30r | control | nodelimit | no | -34.243969 | -34.243969 | 1 | 0.08 | 0 |
| v1 | holdout | root | 0 | cvxnonsep_normcon30r | all | nodelimit | no | -34.243968 | -34.243968 | 1 | 0.31 | 24 |
| v1 | holdout | root | 0 | cvxnonsep_normcon30r | auto | nodelimit | no | -34.243969 | -34.243969 | 1 | 0.08 | 0 |
| v1 | holdout | root | 0 | pointpack06 | baseline | nodelimit | no | 1.1485993 | 1.1485993 | 1 | 0.21 | 0 |
| v1 | holdout | root | 0 | pointpack06 | control | nodelimit | no | 1.1485993 | 1.1485993 | 1 | 0.57 | 0 |
| v1 | holdout | root | 0 | pointpack06 | all | nodelimit | no | 0.83333333 | 0.83333333 | 1 | 0.96 | 24 |
| v1 | holdout | root | 0 | pointpack06 | auto | nodelimit | no | 0.83333333 | 0.83333333 | 1 | 0.77 | 15 |
| v1 | holdout | root | 0 | tltr | baseline | optimal | yes | 48.066667 | - | 1 | 0.06 | 0 |
| v1 | holdout | root | 0 | tltr | control | nodelimit | no | 44.871393 | 44.871393 | 1 | 0.37 | 0 |
| v1 | holdout | root | 0 | tltr | all | optimal | yes | 48.066667 | - | 1 | 0.86 | 4 |
| v1 | holdout | root | 0 | tltr | auto | nodelimit | no | 44.395892 | 44.395892 | 1 | 1.10 | 1 |
| v1 | holdout | root | 0 | ex7_2_4 | baseline | nodelimit | no | 2.3416167 | 2.3416167 | 1 | 0.09 | 0 |
| v1 | holdout | root | 0 | ex7_2_4 | control | nodelimit | no | 2.2383875 | 2.2383875 | 1 | 0.19 | 0 |
| v1 | holdout | root | 0 | ex7_2_4 | all | nodelimit | no | 2.2737166 | 2.2737166 | 1 | 0.51 | 13 |
| v1 | holdout | root | 0 | ex7_2_4 | auto | nodelimit | no | 2.225963 | 2.225963 | 1 | 0.34 | 6 |
| v1 | holdout | root | 0 | pooling_adhya2pq | baseline | nodelimit | no | -572.4023 | -572.4023 | 1 | 0.16 | 0 |
| v1 | holdout | root | 0 | pooling_adhya2pq | control | nodelimit | no | -572.4023 | -572.4023 | 1 | 0.27 | 0 |
| v1 | holdout | root | 0 | pooling_adhya2pq | all | nodelimit | no | -572.4023 | -572.4023 | 1 | 0.78 | 6 |
| v1 | holdout | root | 0 | pooling_adhya2pq | auto | nodelimit | no | -572.4023 | -572.4023 | 1 | 0.68 | 0 |
| v1 | holdout | root | 0 | cvxnonsep_normcon40 | baseline | nodelimit | no | -58.267502 | -58.267502 | 1 | 0.07 | 0 |
| v1 | holdout | root | 0 | cvxnonsep_normcon40 | control | nodelimit | no | -58.267506 | -58.267506 | 1 | 0.14 | 0 |
| v1 | holdout | root | 0 | cvxnonsep_normcon40 | all | nodelimit | no | -58.267506 | -58.267506 | 1 | 0.34 | 24 |
| v1 | holdout | root | 0 | cvxnonsep_normcon40 | auto | nodelimit | no | -58.267506 | -58.267506 | 1 | 0.15 | 0 |
| v1 | holdout | root | 0 | ex1265a | baseline | optimal | yes | 10.3 | - | 1 | 0.06 | 0 |
| v1 | holdout | root | 0 | ex1265a | control | optimal | yes | 10.3 | - | 1 | 0.10 | 0 |
| v1 | holdout | root | 0 | ex1265a | all | optimal | yes | 10.3 | - | 1 | 0.21 | 5 |
| v1 | holdout | root | 0 | ex1265a | auto | optimal | yes | 10.3 | - | 1 | 0.08 | 0 |
| v1 | holdout | root | 0 | kall_circles_c6b | baseline | nodelimit | no | 0 | 0 | 1 | 0.32 | 0 |
| v1 | holdout | root | 0 | kall_circles_c6b | control | nodelimit | no | 0 | 0 | 1 | 0.94 | 0 |
| v1 | holdout | root | 0 | kall_circles_c6b | all | nodelimit | no | 0 | 0 | 1 | 1.10 | 12 |
| v1 | holdout | root | 0 | kall_circles_c6b | auto | nodelimit | no | 0 | 0 | 1 | 1.19 | 17 |
| v1 | synthetic | no_cache | 0 | quartic_balance_8 | all | gaplimit | yes | -2.0001491 | -3.0053743 | 951 | 0.75 | 24 |
| v1 | synthetic | no_cache | 0 | quartic_balance_8 | auto | gaplimit | yes | -2.0001491 | -3.0053743 | 951 | 0.88 | 24 |
| v1 | synthetic | no_cache | 0 | simplex_quadratic_vector | all | optimal | yes | -0.50000123 | -0.50129845 | 5 | 0.13 | 9 |
| v1 | synthetic | no_cache | 0 | simplex_quadratic_vector | auto | optimal | yes | -0.50000069 | -0.50016228 | 5 | 0.08 | 5 |
| v1 | synthetic | no_cache | 0 | overlapping_products | all | optimal | yes | -0.50000001 | - | 1 | 0.40 | 11 |
| v1 | synthetic | no_cache | 0 | overlapping_products | auto | optimal | yes | -0.50000001 | - | 1 | 0.44 | 11 |
| v1 | synthetic | no_cache | 0 | star_marginal_inconsistency | all | optimal | yes | 0.0078123633 | -0.00016474198 | 9 | 0.53 | 16 |
| v1 | synthetic | no_cache | 0 | star_marginal_inconsistency | auto | optimal | yes | 0.0078116462 | -0.00012803018 | 9 | 0.45 | 4 |
| v1 | synthetic | pairs_only | 0 | star_marginal_inconsistency | all | optimal | yes | 0.0078123633 | -0.00016474198 | 9 | 0.19 | 14 |
| v1 | synthetic | pairs_only | 0 | star_marginal_inconsistency | auto | optimal | yes | 0.0078119454 | -0.00010673899 | 9 | 0.10 | 0 |
| v1 | synthetic | repeat | 1 | quartic_balance_8 | baseline | timelimit | no | -2.5727335 | -7.7391145 | 5370 | 6.00 | 0 |
| v1 | synthetic | repeat | 1 | quartic_balance_8 | control | optimal | yes | -2.0000061 | -5.9139848 | 1362 | 1.04 | 0 |
| v1 | synthetic | repeat | 1 | quartic_balance_8 | all | gaplimit | yes | -2.0001795 | -3.0053743 | 781 | 0.69 | 24 |
| v1 | synthetic | repeat | 1 | quartic_balance_8 | auto | gaplimit | yes | -2.0001795 | -3.0053743 | 781 | 0.64 | 24 |
| v1 | synthetic | repeat | 1 | simplex_quadratic_vector | baseline | gaplimit | yes | -0.50000653 | -0.50027374 | 3 | 0.04 | 0 |
| v1 | synthetic | repeat | 1 | simplex_quadratic_vector | control | optimal | yes | -0.50000001 | - | 1 | 0.03 | 0 |
| v1 | synthetic | repeat | 1 | simplex_quadratic_vector | all | optimal | yes | -0.50000123 | -0.50129845 | 5 | 0.12 | 9 |
| v1 | synthetic | repeat | 1 | simplex_quadratic_vector | auto | optimal | yes | -0.50000072 | -0.50016228 | 5 | 0.09 | 5 |
| v1 | holdout | repeat | 1 | kall_congruentcircles_c42 | baseline | optimal | yes | 0.85840655 | 0 | 174 | 0.25 | 0 |
| v1 | holdout | repeat | 1 | kall_congruentcircles_c42 | control | optimal | yes | 0.8584066 | 0 | 195 | 0.34 | 0 |
| v1 | holdout | repeat | 1 | kall_congruentcircles_c42 | all | optimal | yes | 0.85840609 | 0 | 145 | 0.70 | 21 |
| v1 | holdout | repeat | 1 | kall_congruentcircles_c42 | auto | gaplimit | yes | 0.85836831 | 0 | 121 | 0.50 | 13 |
| v1 | holdout | repeat | 1 | pooling_adhya2stp | baseline | gaplimit | yes | -549.85302 | -574.78261 | 651 | 0.88 | 0 |
| v1 | holdout | repeat | 1 | pooling_adhya2stp | control | gaplimit | yes | -549.85546 | -574.78261 | 489 | 1.60 | 0 |
| v1 | holdout | repeat | 1 | pooling_adhya2stp | all | gaplimit | yes | -549.8146 | -574.78261 | 601 | 2.37 | 15 |
| v1 | holdout | repeat | 1 | pooling_adhya2stp | auto | gaplimit | yes | -549.84499 | -574.78261 | 569 | 2.03 | 11 |
| v1 | holdout | repeat | 1 | ex4 | baseline | optimal | yes | -8.0641664 | - | 9 | 1.30 | 0 |
| v1 | holdout | repeat | 1 | ex4 | control | optimal | yes | -8.0641364 | -9.8204992 | 31 | 1.56 | 0 |
| v1 | holdout | repeat | 1 | ex4 | all | optimal | yes | -8.0641362 | -9.2103466 | 31 | 2.46 | 14 |
| v1 | holdout | repeat | 1 | ex4 | auto | optimal | yes | -8.0641364 | -9.8204992 | 31 | 1.45 | 0 |

### (b) Time breakdown (seconds, sums over runs)

Nesting: SCIP solve wall contains the callback; the callback contains direction LPs, certification, row export (and, in v2/repair, discovery). 'SCIP excl. callback' = solve wall - callback.

Campaign-v2:

| Suite | Phase | Mode | Runs | Read/prep | Discovery (inside callback) | Build | SCIP solve wall | Callback | Direction LPs | Certification | Row export | Screening | SCIP excl. callback | Integration total | Outer wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| holdout | full | baseline | 30 | 0.050 | 0.000 | 2.089 | 168.433 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 168.433 | 170.575 | 197.301 |
| holdout | full | all | 30 | 0.056 | 24.406 | 2.163 | 184.796 | 27.633 | 0.669 | 2.357 | 0.005 | n/a | 157.164 | 187.025 | 213.198 |
| holdout | full | auto | 30 | 0.064 | 24.627 | 2.058 | 184.987 | 27.000 | 0.297 | 1.962 | 0.001 | n/a | 157.987 | 187.118 | 213.556 |
| diagnostic | full | baseline | 10 | 0.109 | 0.000 | 9.026 | 147.420 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 147.420 | 156.556 | 165.672 |
| diagnostic | full | all | 10 | 0.022 | 28.548 | 0.824 | 103.090 | 29.677 | 0.246 | 0.841 | 0.002 | n/a | 73.413 | 103.940 | 123.814 |
| diagnostic | full | auto | 10 | 0.025 | 27.828 | 0.825 | 102.596 | 28.681 | 0.121 | 0.705 | 0.001 | n/a | 73.915 | 103.450 | 123.324 |
| synthetic | full | baseline | 13 | 0.005 | 0.000 | 0.330 | 10.350 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 10.350 | 10.685 | 22.076 |
| synthetic | full | all | 13 | 0.005 | 0.035 | 0.315 | 10.534 | 0.331 | 0.119 | 0.128 | 0.002 | n/a | 10.203 | 10.856 | 22.057 |
| synthetic | full | auto | 13 | 0.005 | 0.041 | 0.329 | 10.355 | 0.078 | 0.013 | 0.004 | 0.000 | n/a | 10.277 | 10.692 | 21.867 |
| holdout | root | baseline | 30 | 0.051 | 0.000 | 2.038 | 11.926 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 11.926 | 14.018 | 39.563 |
| holdout | root | all | 30 | 0.053 | 24.199 | 2.148 | 35.824 | 25.192 | 0.290 | 0.556 | 0.002 | n/a | 10.633 | 38.034 | 63.866 |
| holdout | root | auto | 30 | 0.048 | 23.393 | 2.076 | 34.733 | 23.879 | 0.053 | 0.361 | 0.000 | n/a | 10.854 | 36.865 | 62.297 |
| synthetic | root | baseline | 5 | 0.002 | 0.000 | 0.121 | 0.160 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 0.160 | 0.284 | 4.537 |
| synthetic | root | all | 5 | 0.001 | 0.041 | 0.132 | 0.434 | 0.294 | 0.085 | 0.118 | 0.001 | n/a | 0.141 | 0.569 | 5.239 |
| synthetic | root | auto | 5 | 0.002 | 0.035 | 0.128 | 0.243 | 0.066 | 0.014 | 0.004 | 0.000 | n/a | 0.177 | 0.374 | 4.687 |
| holdout | repeat | baseline | 6 | 0.013 | 0.000 | 0.338 | 9.256 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 9.256 | 9.608 | 14.945 |
| holdout | repeat | all | 6 | 0.011 | 4.684 | 0.314 | 14.689 | 5.386 | 0.108 | 0.553 | 0.000 | n/a | 9.303 | 15.016 | 19.999 |
| holdout | repeat | auto | 6 | 0.009 | 4.738 | 0.296 | 14.589 | 5.410 | 0.043 | 0.592 | 0.000 | n/a | 9.179 | 14.895 | 20.147 |

Repair cohort:

| Suite | Phase | Mode | Runs | Read/prep | Discovery (inside callback) | Build | SCIP solve wall | Callback | Direction LPs | Certification | Row export | Screening | SCIP excl. callback | Integration total | Outer wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| holdout | full | baseline | 8 | 0.021 | 0.000 | 1.143 | 122.747 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 122.747 | 123.913 | 131.364 |
| holdout | full | all | 8 | 0.029 | 1.332 | 1.080 | 123.744 | 1.912 | 0.138 | 0.277 | 0.002 | n/a | 121.832 | 124.856 | 132.071 |
| holdout | full | auto | 8 | 0.024 | 1.324 | 1.039 | 123.752 | 1.739 | 0.080 | 0.254 | 0.001 | n/a | 122.013 | 124.819 | 132.320 |
| diagnostic | full | baseline | 7 | 0.092 | 0.000 | 8.709 | 87.546 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 87.546 | 96.348 | 102.661 |
| diagnostic | full | all | 7 | 0.126 | 2.852 | 8.849 | 86.511 | 4.080 | 0.252 | 0.837 | 0.003 | n/a | 82.431 | 95.496 | 101.996 |
| diagnostic | full | auto | 7 | 0.100 | 2.900 | 9.293 | 87.313 | 3.273 | 0.042 | 0.240 | 0.000 | n/a | 84.040 | 96.718 | 103.206 |
| holdout | root | baseline | 9 | 0.029 | 0.000 | 1.124 | 4.699 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 4.699 | 5.854 | 13.528 |
| holdout | root | all | 9 | 0.024 | 0.981 | 1.086 | 5.907 | 1.547 | 0.128 | 0.315 | 0.001 | n/a | 4.360 | 7.020 | 14.733 |
| holdout | root | auto | 9 | 0.029 | 0.978 | 1.143 | 6.094 | 1.362 | 0.070 | 0.252 | 0.001 | n/a | 4.732 | 7.270 | 15.029 |
| holdout | repeat | baseline | 1 | 0.002 | 0.000 | 0.068 | 1.226 | 0.000 | 0.000 | 0.000 | 0.000 | n/a | 1.226 | 1.296 | 2.122 |
| holdout | repeat | all | 1 | 0.004 | 0.147 | 0.073 | 1.836 | 0.250 | 0.031 | 0.026 | 0.000 | n/a | 1.585 | 1.913 | 2.774 |
| holdout | repeat | auto | 1 | 0.004 | 0.140 | 0.065 | 1.380 | 0.143 | 0.000 | 0.000 | 0.000 | n/a | 1.237 | 1.450 | 2.372 |

Campaign-v1:

| Suite | Phase | Mode | Runs | Read/prep | Discovery (pre-solve) | Build | SCIP solve wall | Callback | Direction LPs | Certification | Row export | Screening | SCIP excl. callback | Integration total | Outer wall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| holdout | full | baseline | 24 | 0.018 | 0.000 | 0.749 | 16.628 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 16.628 | 17.398 | 36.662 |
| holdout | full | control | 24 | 0.018 | 0.355 | 0.706 | 19.584 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 19.584 | 20.665 | 40.117 |
| holdout | full | all | 24 | 0.018 | 0.329 | 0.659 | 24.399 | 5.588 | 4.704 | 0.701 | 0.025 | 0.000 | 18.811 | 25.408 | 45.437 |
| holdout | full | auto | 24 | 0.017 | 0.335 | 0.678 | 21.975 | 3.051 | 2.540 | 0.339 | 0.013 | 0.098 | 18.924 | 23.008 | 42.488 |
| historical | full | baseline | 4 | 0.051 | 0.000 | 0.591 | 5.582 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 5.582 | 6.225 | 9.600 |
| historical | full | control | 4 | 0.052 | 0.750 | 0.793 | 5.249 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 5.249 | 6.844 | 10.361 |
| historical | full | all | 4 | 0.036 | 0.803 | 0.830 | 5.243 | 0.250 | 0.177 | 0.063 | 0.003 | 0.000 | 4.994 | 6.913 | 10.412 |
| historical | full | auto | 4 | 0.039 | 0.790 | 0.778 | 5.276 | 0.204 | 0.138 | 0.043 | 0.003 | 0.013 | 5.072 | 6.884 | 10.260 |
| synthetic | full | baseline | 13 | 0.001 | 0.000 | 0.293 | 6.278 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6.278 | 6.573 | 16.937 |
| synthetic | full | control | 13 | 0.001 | 0.071 | 0.228 | 1.363 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.363 | 1.665 | 11.570 |
| synthetic | full | all | 13 | 0.001 | 0.078 | 0.242 | 2.183 | 1.165 | 0.898 | 0.210 | 0.008 | 0.000 | 1.018 | 2.505 | 13.177 |
| synthetic | full | auto | 13 | 0.001 | 0.081 | 0.236 | 2.131 | 1.093 | 0.855 | 0.166 | 0.006 | 0.032 | 1.039 | 2.451 | 13.138 |
| holdout | root | baseline | 24 | 0.019 | 0.000 | 0.759 | 2.419 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 2.419 | 3.199 | 22.617 |
| holdout | root | control | 24 | 0.017 | 0.347 | 0.661 | 5.289 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 5.289 | 6.317 | 25.626 |
| holdout | root | all | 24 | 0.017 | 0.331 | 0.610 | 9.241 | 3.879 | 3.270 | 0.511 | 0.016 | 0.000 | 5.362 | 10.202 | 29.816 |
| holdout | root | auto | 24 | 0.016 | 0.328 | 0.672 | 7.916 | 2.152 | 1.808 | 0.239 | 0.007 | 0.056 | 5.764 | 8.935 | 28.636 |
| synthetic | root | baseline | 5 | 0.001 | 0.000 | 0.111 | 0.167 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.167 | 0.279 | 4.235 |
| synthetic | root | control | 5 | 0.001 | 0.047 | 0.080 | 0.169 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.169 | 0.297 | 4.287 |
| synthetic | root | all | 5 | 0.001 | 0.046 | 0.074 | 1.114 | 0.899 | 0.809 | 0.072 | 0.004 | 0.000 | 0.215 | 1.235 | 5.438 |
| synthetic | root | auto | 5 | 0.001 | 0.047 | 0.067 | 1.047 | 0.862 | 0.762 | 0.065 | 0.004 | 0.017 | 0.185 | 1.162 | 5.288 |
| holdout | repeat | baseline | 3 | 0.003 | 0.000 | 0.143 | 2.285 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 2.285 | 2.431 | 4.858 |
| holdout | repeat | control | 3 | 0.003 | 0.073 | 0.153 | 3.269 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 3.269 | 3.499 | 5.912 |
| holdout | repeat | all | 3 | 0.003 | 0.069 | 0.149 | 5.307 | 1.256 | 1.115 | 0.100 | 0.005 | 0.000 | 4.051 | 5.528 | 7.920 |
| holdout | repeat | auto | 3 | 0.003 | 0.068 | 0.139 | 3.772 | 0.759 | 0.672 | 0.042 | 0.003 | 0.029 | 3.013 | 3.983 | 6.465 |
| synthetic | repeat | baseline | 3 | 0.001 | 0.000 | 0.066 | 6.013 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 6.013 | 6.080 | 8.419 |
| synthetic | repeat | control | 3 | 0.001 | 0.026 | 0.059 | 1.034 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.034 | 1.120 | 3.355 |
| synthetic | repeat | all | 3 | 0.000 | 0.019 | 0.042 | 0.777 | 0.182 | 0.106 | 0.064 | 0.003 | 0.000 | 0.595 | 0.838 | 3.103 |
| synthetic | repeat | auto | 3 | 0.001 | 0.023 | 0.055 | 0.704 | 0.159 | 0.087 | 0.052 | 0.003 | 0.009 | 0.545 | 0.782 | 3.204 |
| synthetic | no_cache | all | 5 | 0.001 | 0.040 | 0.067 | 1.752 | 1.003 | 0.867 | 0.112 | 0.006 | 0.000 | 0.749 | 1.860 | 5.890 |
| synthetic | no_cache | auto | 5 | 0.001 | 0.048 | 0.087 | 1.767 | 0.892 | 0.794 | 0.078 | 0.004 | 0.000 | 0.874 | 1.903 | 6.039 |
| synthetic | pairs_only | all | 1 | 0.000 | 0.023 | 0.006 | 0.164 | 0.097 | 0.068 | 0.023 | 0.001 | 0.000 | 0.067 | 0.194 | 0.918 |
| synthetic | pairs_only | auto | 1 | 0.000 | 0.025 | 0.007 | 0.072 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.072 | 0.104 | 0.868 |

Shifted geometric means (shift 1 s) of integration time; paired time ratios on commonly solved models:

| Campaign | Suite | Mode | Runs with time | SGM time, all (s) | Both solved | SGM time, both solved (s) | >10% faster than baseline | >10% slower | Within 10% |
|---|---|---|---|---|---|---|---|---|---|
| v2 | holdout | baseline | 30 | 1.552 | 25 | 0.549 | 0 | 0 | 25 |
| v2 | holdout | all | 30 | 2.144 | 25 | 0.989 | 0 | 21 | 4 |
| v2 | holdout | auto | 30 | 2.102 | 25 | 0.957 | 0 | 21 | 4 |

| Campaign | Suite | Mode | Runs with time | SGM time, all (s) | Both solved | SGM time, both solved (s) | >10% faster than baseline | >10% slower | Within 10% |
|---|---|---|---|---|---|---|---|---|---|
| v1 | holdout | baseline | 23 | 0.419 | 19 | 0.377 | 0 | 0 | 19 |
| v1 | holdout | control | 23 | 0.537 | 19 | 0.517 | 2 | 17 | 0 |
| v1 | holdout | all | 23 | 0.690 | 18 | 0.574 | 2 | 15 | 1 |
| v1 | holdout | auto | 23 | 0.597 | 18 | 0.464 | 1 | 13 | 4 |

### (c) The 30 campaign-v2 holdout models (full runs, seed 0)

Cell = status, '*' if not numerically solved, integration seconds, recorded cuts. Hash order.

| Model | Stratum | Vars | Cons | OSiL bytes | Integer | Reference primal | baseline | all | auto |
|---|---|---|---|---|---|---|---|---|---|
| p_ball_10b_5p_2d_m | convex | 80 | 109 | 20750 | yes | 18.71857799 | optimal 1.47s 0c | optimal 5.46s 0c | optimal 5.58s 0c |
| st_glmp_kk90 | nonconvex_continuous | 5 | 7 | 1481 | no | 3.0 | gaplimit 0.03s 0c | gaplimit 0.07s 0c | gaplimit 0.05s 0c |
| du-opt5 | convex | 20 | 9 | 16628 | yes | 8.07365758 | optimal 0.69s 0c | optimal 0.80s 0c | optimal 0.83s 0c |
| nvs24 | nonconvex_integer | 10 | 10 | 25754 | yes | -1033.2 | gaplimit 4.96s 0c | gaplimit 5.04s 0c | gaplimit 5.05s 0c |
| nous1 | nonconvex_integer | 50 | 43 | 7921 | yes | 1.567072 | gaplimit 2.68s 0c | gaplimit 4.57s 2c | gaplimit 4.63s 2c |
| supplychain | nonconvex_integer | 27 | 30 | 4794 | yes | 2260.256563 | optimal 0.24s 0c | optimal 0.43s 0c | optimal 0.49s 0c |
| ex4_1_8 | nonconvex_continuous | 2 | 1 | 1119 | no | -16.73889318 | gaplimit 0.04s 0c | gaplimit 0.11s 5c | gaplimit 0.04s 0c |
| ex8_3_4 | nonconvex_continuous | 110 | 76 | 18898 | no | -3.579982383 | timelimit* 30.02s 0c | timelimit* 30.02s 0c | timelimit* 30.02s 0c |
| cvxnonsep_normcon20r | convex | 40 | 21 | 3970 | yes | -21.74914736 | gaplimit 0.09s 0c | gaplimit 0.33s 12c | gaplimit 0.27s 0c |
| cvxnonsep_psig20r | convex | 42 | 22 | 5152 | yes | 95.89738736 | gaplimit 0.10s 0c | gaplimit 0.55s 10c | gaplimit 0.30s 0c |
| hybriddynamic_var | nonconvex_integer | 81 | 100 | 12519 | yes | 1.536415162 | gaplimit 0.54s 0c | gaplimit 3.00s 0c | gaplimit 3.08s 0c |
| graphpart_clique-40 | nonconvex_integer | 120 | 40 | 124801 | yes | 1183.0 | timelimit* 30.02s 0c | timelimit* 30.01s 0c | timelimit* 30.02s 0c |
| pooling_adhya4pq | nonconvex_continuous | 58 | 77 | 10505 | no | -877.6457399 | optimal 0.69s 0c | optimal 2.61s 0c | optimal 2.75s 0c |
| st_glmp_kk92 | nonconvex_continuous | 4 | 8 | 1483 | no | -12.0 | gaplimit 0.04s 0c | gaplimit 0.07s 0c | gaplimit 0.04s 0c |
| st_testph4 | convex | 3 | 10 | 1795 | yes | -80.5 | optimal 0.03s 0c | optimal 0.03s 0c | optimal 0.03s 0c |
| du-opt | convex | 20 | 9 | 16725 | yes | 3.556340052 | optimal 3.20s 0c | optimal 3.52s 0c | optimal 3.24s 0c |
| ex5_2_5 | nonconvex_continuous | 32 | 19 | 13101 | no | -3500.0 | timelimit* 30.02s 0c | timelimit* 30.02s 0c | timelimit* 30.02s 0c |
| kall_congruentcircles_c41 | nonconvex_continuous | 12 | 24 | 4267 | no | 0.8584073463 | gaplimit 0.13s 0c | gaplimit 1.04s 0c | gaplimit 1.00s 0c |
| ex14_2_7 | nonconvex_continuous | 6 | 9 | 18928 | no | 0.0 | optimal 0.14s 0c | optimal 0.17s 0c | optimal 0.14s 0c |
| st_e22 | nonconvex_continuous | 2 | 5 | 1196 | no | -85.0 | gaplimit 0.04s 0c | optimal 0.04s 1c | optimal 0.04s 1c |
| kall_congruentcircles_c51 | nonconvex_continuous | 14 | 34 | 6001 | no | 1.073009183 | optimal 2.94s 0c | optimal 3.43s 6c | optimal 4.06s 7c |
| tln4 | nonconvex_integer | 24 | 24 | 4288 | yes | 8.3 | optimal 0.17s 0c | optimal 0.28s 0c | optimal 0.28s 0c |
| synthes1 | convex | 6 | 6 | 2185 | yes | 6.00975909 | optimal 0.11s 0c | optimal 0.12s 0c | optimal 0.11s 0c |
| syn05m | convex | 20 | 28 | 4052 | yes | 837.7324009 | optimal 0.06s 0c | optimal 0.25s 2c | optimal 0.16s 0c |
| nvs17 | nonconvex_integer | 7 | 7 | 10537 | yes | -1100.4 | optimal 0.84s 0c | optimal 0.85s 0c | optimal 0.92s 0c |
| tln7 | nonconvex_integer | 63 | 42 | 9350 | yes | 15.0 | timelimit* 30.02s 0c | timelimit* 30.02s 0c | timelimit* 30.02s 0c |
| st_testgr3 | convex | 20 | 20 | 6600 | yes | -20.59 | optimal 0.13s 0c | optimal 0.34s 0c | optimal 0.32s 0c |
| graphpart_2g-0066-0066 | nonconvex_integer | 108 | 36 | 17370 | yes | -2865560.0 | optimal 1.07s 0c | optimal 3.47s 0c | optimal 3.47s 0c |
| ex1223 | convex | 11 | 13 | 2832 | yes | 4.579582402 | gaplimit 0.07s 0c | gaplimit 0.36s 0c | gaplimit 0.11s 0c |
| waterx | nonconvex_integer | 70 | 54 | 12854 | yes | 909.0278626 | timelimit* 30.02s 0c | timelimit* 30.02s 0c | timelimit* 30.02s 0c |

### (d) The five unsolved campaign-v2 holdout models: bounds and gaps

Archived reference = MINLPLib primal / dual bound. SCIP rel. gap = |p-d|/min(|p|,|d|).

| Campaign | Model | Mode | Status | Primal | Dual | Abs gap | SCIP rel. gap | Archived reference | Nodes | Time (s) | Cuts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v2 | ex8_3_4 | baseline | timelimit | -3.5799823 | -10 | 6.4200177 | 179.33% | -3.579982383 / -5.8 | 6216 | 30.02 | 0 |
| v2 | ex8_3_4 | all | timelimit | -3.5799823 | -10 | 6.4200177 | 179.33% | -3.579982383 / -5.8 | 5848 | 30.02 | 0 |
| v2 | ex8_3_4 | auto | timelimit | -3.5799823 | -10 | 6.4200177 | 179.33% | -3.579982383 / -5.8 | 5745 | 30.02 | 0 |
| v2 | graphpart_clique-40 | baseline | timelimit | 1544 | 438 | 1106 | 252.51% | 1183.0 / 1183.0 | 429 | 30.02 | 0 |
| v2 | graphpart_clique-40 | all | timelimit | 1578 | 392 | 1186 | 302.55% | 1183.0 / 1183.0 | 370 | 30.01 | 0 |
| v2 | graphpart_clique-40 | auto | timelimit | 1578 | 392 | 1186 | 302.55% | 1183.0 / 1183.0 | 370 | 30.02 | 0 |
| v2 | ex5_2_5 | baseline | timelimit | -3500 | -4490.2392 | 990.23912 | 28.29% | -3500.0 / -3500.000004 | 29147 | 30.02 | 0 |
| v2 | ex5_2_5 | all | timelimit | -3500 | -4494.8157 | 994.81561 | 28.42% | -3500.0 / -3500.000004 | 28852 | 30.02 | 0 |
| v2 | ex5_2_5 | auto | timelimit | -3500 | -4497.6188 | 997.61877 | 28.50% | -3500.0 / -3500.000004 | 28727 | 30.02 | 0 |
| v2 | tln7 | baseline | timelimit | 15.7 | 14.475541 | 1.2244586 | 8.46% | 15.0 / 14.99999999 | 48858 | 30.02 | 0 |
| v2 | tln7 | all | timelimit | 15.7 | 14.469017 | 1.2309825 | 8.51% | 15.0 / 14.99999999 | 46887 | 30.02 | 0 |
| v2 | tln7 | auto | timelimit | 15.7 | 14.46701 | 1.23299 | 8.52% | 15.0 / 14.99999999 | 46194 | 30.02 | 0 |
| v2 | waterx | baseline | timelimit | 921.35825 | 514.26438 | 407.09387 | 79.16% | 909.0278626 / 807.0073387 | 4534 | 30.02 | 0 |
| v2 | waterx | all | timelimit | 921.35825 | 514.03152 | 407.32673 | 79.24% | 909.0278626 / 807.0073387 | 4302 | 30.02 | 0 |
| v2 | waterx | auto | timelimit | 921.35825 | 514.06461 | 407.29365 | 79.23% | 909.0278626 / 807.0073387 | 4396 | 30.02 | 0 |

### (e) The 13 synthetic mechanism cases (campaign-v2 full runs, 10 s)

| Case | Stratum (cases.py) | Description | Known optimum | baseline | all | auto |
|---|---|---|---|---|---|---|
| quartic_balance_4 | composite polynomial mechanism | min sum_i (x_i^4 - x_i^2), sum_i x_i = 0, x in [-1,1]^4; optimum -1 (separable nonconvex quartic with a linking row) | -1 | optimal; dual -1.000001; 0.29 s; 0 cuts | optimal; dual -1.000001; 0.24 s; 0 cuts | optimal; dual -1.000001; 0.24 s; 0 cuts |
| quartic_balance_8 | composite polynomial mechanism | same as quartic_balance_4 with 8 variables; optimum -2 | -2 | timelimit (unsolved); dual -2.4380859; 10.00 s; 0 cuts | timelimit (unsolved); dual -2.4424303; 10.02 s; 0 cuts | timelimit (unsolved); dual -2.4424303; 10.00 s; 0 cuts |
| cubic_moment | shared polynomial curve | min x^3 s.t. x^2 >= 1/4, x in [0,1]; optimum 1/8 (shared polynomial curve) | 0.125 | optimal; dual 0.125; 0.02 s; 0 cuts | optimal; dual 0.125; 0.02 s; 0 cuts | optimal; dual 0.125; 0.02 s; 0 cuts |
| exp_pair | general exp curve | min e^x + e^-x s.t. e^x + e^-x >= 3, x in [-2,2]; optimum 3 (same exp expression in objective and row) | 3 | optimal; dual 3; 0.04 s; 0 cuts | optimal; dual 3; 0.11 s; 1 cuts | optimal; dual 3; 0.05 s; 0 cuts |
| log_pair | general log curve | min log x - (1/2) log(1+2x), x in [1/4,2]; optimum log(1/4) - (1/2) log(3/2) (log curve) | -1.5890269 | gaplimit; dual -1.5890433; 0.03 s; 0 cuts | gaplimit; dual -1.5890433; 0.03 s; 0 cuts | gaplimit; dual -1.5890433; 0.03 s; 0 cuts |
| trig_pair | general trigonometric curve | min sin x + cos x, x in [-pi,pi]; optimum -sqrt(2) (trigonometric curve) | -1.4142136 | gaplimit; dual -1.414263; 0.03 s; 0 cuts | gaplimit; dual -1.414263; 0.07 s; 2 cuts | gaplimit; dual -1.414263; 0.03 s; 0 cuts |
| simplex_product | coupled two-variable domain | min -xy on {x+y<=1} in [0,1]^2; optimum -1/4 (box McCormick gives -1/2) | -0.25 | optimal; dual -0.25000001; 0.03 s; 0 cuts | optimal; dual -0.25000001; 0.03 s; 0 cuts | optimal; dual -0.25000001; 0.03 s; 0 cuts |
| simplex_quadratic_vector | coupled quadratic vector | min x^2 + y^2 - 4xy on {x+y<=1} in [0,1]^2; optimum -1/2 (quadratic vector on a simplex) | -0.5 | gaplimit; dual -0.50000653; 0.04 s; 0 cuts | optimal; dual -0.50000002; 0.06 s; 2 cuts | optimal; dual -0.50000002; 0.07 s; 2 cuts |
| overlapping_products | overlapping coupled blocks | min -y(x+z), x+y<=1, y+z<=1, [0,1]^3; optimum -1/2 (two overlapping coupled blocks) | -0.5 | optimal; dual -0.50000001; 0.03 s; 0 cuts | optimal; dual -0.50000001; 0.02 s; 0 cuts | optimal; dual -0.50000001; 0.03 s; 0 cuts |
| star_marginal_inconsistency | pair marginals versus merged quadratic star | min (y-1/4-x/2)^2 + (y-5z/8)^2 + x(1-x) + z(1-z) on [0,1]^3; optimum 1/128 at (1,11/16,1); exact pair hulls glued on shared center moments give 0 | 0.0078125 | optimal; dual 0.0078124899; 0.09 s; 0 cuts | gaplimit; dual 0.0078120225; 0.17 s; 8 cuts | optimal; dual 0.0078124899; 0.12 s; 0 cuts |
| affine_control | neutral no nonlinear structure | min sum_i (i+1) x_i s.t. sum_i x_i >= 1, [0,1]^8; optimum 1 (no nonlinear structure; neutral control) | 1 | optimal; dual 1; 0.02 s; 0 cuts | optimal; dual 1; 0.03 s; 0 cuts | optimal; dual 1; 0.03 s; 0 cuts |
| convex_redundant_control | adverse unnecessary convexification | min sum_i (x_i^2 + x_i^4), [-1,1]^8; optimum 0 (convex; unnecessary convexification, adverse control) | 0 | optimal; dual 0; 0.02 s; 0 cuts | optimal; dual 0; 0.02 s; 0 cuts | optimal; dual 0; 0.02 s; 0 cuts |
| binary_product_control | neutral native integer products | min -x0 x1 - x2 x3, sum x_i <= 2, binary x; optimum -1 (native integer products; neutral control) | -1 | optimal; dual -1; 0.03 s; 0 cuts | optimal; dual -1; 0.02 s; 0 cuts | optimal; dual -1; 0.03 s; 0 cuts |

Campaign-v2 root-only mechanism runs (5 s, one node):

| Case | Stratum (cases.py) | Description | Known optimum | baseline | all | auto |
|---|---|---|---|---|---|---|
| quartic_balance_8 | composite polynomial mechanism | same as quartic_balance_4 with 8 variables; optimum -2 | -2 | nodelimit (unsolved); dual -7.7391145; 0.09 s; 0 cuts | nodelimit (unsolved); dual -7.7391145; 0.13 s; 0 cuts | nodelimit (unsolved); dual -7.7391145; 0.12 s; 0 cuts |
| exp_pair | general exp curve | min e^x + e^-x s.t. e^x + e^-x >= 3, x in [-2,2]; optimum 3 (same exp expression in objective and row) | 3 | optimal; dual 3; 0.04 s; 0 cuts | optimal; dual 3; 0.11 s; 1 cuts | optimal; dual 3; 0.05 s; 0 cuts |
| simplex_quadratic_vector | coupled quadratic vector | min x^2 + y^2 - 4xy on {x+y<=1} in [0,1]^2; optimum -1/2 (quadratic vector on a simplex) | -0.5 | nodelimit (unsolved); dual -0.50027374; 0.06 s; 0 cuts | optimal; dual -0.50000002; 0.10 s; 2 cuts | optimal; dual -0.50000002; 0.07 s; 2 cuts |
| overlapping_products | overlapping coupled blocks | min -y(x+z), x+y<=1, y+z<=1, [0,1]^3; optimum -1/2 (two overlapping coupled blocks) | -0.5 | optimal; dual -0.50000001; 0.03 s; 0 cuts | optimal; dual -0.50000001; 0.02 s; 0 cuts | optimal; dual -0.50000001; 0.02 s; 0 cuts |
| star_marginal_inconsistency | pair marginals versus merged quadratic star | min (y-1/4-x/2)^2 + (y-5z/8)^2 + x(1-x) + z(1-z) on [0,1]^3; optimum 1/128 at (1,11/16,1); exact pair hulls glued on shared center moments give 0 | 0.0078125 | nodelimit (unsolved); dual 0.007812499; 0.07 s; 0 cuts | gaplimit; dual 0.0078120225; 0.21 s; 8 cuts | nodelimit (unsolved); dual 0.007812499; 0.12 s; 0 cuts |

### Campaign-v2: solved counts and paired comparisons by phase

| Campaign | Suite | Phase | Mode | Runs | Admitted | Solved | Statuses | Cuts | Runs with cuts | Unknown cut logs | Integration s | Outer s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v2 | holdout | full | baseline | 30 | 30 | 25 | {'gaplimit': 11, 'optimal': 14, 'timelimit': 5} | 0 | 0 | 0 | 170.57 | 197.30 |
| v2 | holdout | full | all | 30 | 30 | 25 | {'gaplimit': 10, 'optimal': 15, 'timelimit': 5} | 38 | 7 | 0 | 187.02 | 213.20 |
| v2 | holdout | full | auto | 30 | 30 | 25 | {'gaplimit': 10, 'optimal': 15, 'timelimit': 5} | 10 | 3 | 0 | 187.12 | 213.56 |
| v2 | diagnostic | full | baseline | 10 | 10 | 5 | {'gaplimit': 4, 'optimal': 1, 'timelimit': 5} | 0 | 0 | 0 | 156.56 | 165.67 |
| v2 | diagnostic | full | all | 10 | 8 | 5 | {'gaplimit': 4, 'optimal': 1, 'timelimit': 3, 'worker_error': 2} | 15 | 2 | 2 | 103.94 | 123.81 |
| v2 | diagnostic | full | auto | 10 | 8 | 5 | {'gaplimit': 4, 'optimal': 1, 'timelimit': 3, 'worker_error': 2} | 5 | 1 | 2 | 103.45 | 123.32 |
| v2 | synthetic | full | baseline | 13 | 13 | 12 | {'gaplimit': 3, 'optimal': 9, 'timelimit': 1} | 0 | 0 | 0 | 10.69 | 22.08 |
| v2 | synthetic | full | all | 13 | 13 | 12 | {'gaplimit': 3, 'optimal': 9, 'timelimit': 1} | 13 | 4 | 0 | 10.86 | 22.06 |
| v2 | synthetic | full | auto | 13 | 13 | 12 | {'gaplimit': 2, 'optimal': 10, 'timelimit': 1} | 2 | 1 | 0 | 10.69 | 21.87 |
| v2 | holdout | root | baseline | 30 | 30 | 9 | {'gaplimit': 6, 'nodelimit': 21, 'optimal': 3} | 0 | 0 | 0 | 14.02 | 39.56 |
| v2 | holdout | root | all | 30 | 30 | 9 | {'gaplimit': 5, 'nodelimit': 20, 'optimal': 4, 'timelimit': 1} | 21 | 6 | 0 | 38.03 | 63.87 |
| v2 | holdout | root | auto | 30 | 30 | 9 | {'gaplimit': 5, 'nodelimit': 20, 'optimal': 4, 'timelimit': 1} | 2 | 2 | 0 | 36.87 | 62.30 |
| v2 | synthetic | root | baseline | 5 | 5 | 2 | {'nodelimit': 3, 'optimal': 2} | 0 | 0 | 0 | 0.28 | 4.54 |
| v2 | synthetic | root | all | 5 | 5 | 4 | {'gaplimit': 1, 'nodelimit': 1, 'optimal': 3} | 11 | 3 | 0 | 0.57 | 5.24 |
| v2 | synthetic | root | auto | 5 | 5 | 3 | {'nodelimit': 2, 'optimal': 3} | 2 | 1 | 0 | 0.37 | 4.69 |
| v2 | holdout | repeat | baseline | 6 | 6 | 6 | {'gaplimit': 2, 'optimal': 4} | 0 | 0 | 0 | 9.61 | 14.94 |
| v2 | holdout | repeat | all | 6 | 6 | 6 | {'gaplimit': 2, 'optimal': 4} | 2 | 1 | 0 | 15.02 | 20.00 |
| v2 | holdout | repeat | auto | 6 | 6 | 6 | {'gaplimit': 2, 'optimal': 4} | 2 | 1 | 0 | 14.90 | 20.15 |

| Campaign | Suite | Phase | Comparison | Bound | Better | Tie | Worse | Unavailable |
|---|---|---|---|---|---|---|---|---|
| v2 | holdout | full | all vs baseline | dual | 2 | 21 | 7 | 0 |
| v2 | holdout | full | auto vs baseline | dual | 2 | 24 | 4 | 0 |
| v2 | diagnostic | full | all vs baseline | dual | 1 | 5 | 2 | 2 |
| v2 | diagnostic | full | auto vs baseline | dual | 0 | 5 | 3 | 2 |
| v2 | synthetic | full | all vs baseline | dual | 1 | 11 | 1 | 0 |
| v2 | synthetic | full | auto vs baseline | dual | 1 | 11 | 1 | 0 |
| v2 | holdout | root | all vs baseline | dual | 1 | 26 | 3 | 0 |
| v2 | holdout | root | auto vs baseline | dual | 1 | 28 | 1 | 0 |
| v2 | synthetic | root | all vs baseline | dual | 1 | 4 | 0 | 0 |
| v2 | synthetic | root | auto vs baseline | dual | 1 | 4 | 0 | 0 |
| v2 | holdout | repeat | all vs baseline | dual | 0 | 6 | 0 | 0 |
| v2 | holdout | repeat | auto vs baseline | dual | 0 | 6 | 0 | 0 |
| v2 | holdout | full | all vs baseline | root_dual | 1 | 20 | 2 | 7 |
| v2 | holdout | full | auto vs baseline | root_dual | 0 | 23 | 0 | 7 |

Sensitivity of better/tie/worse counts to the relative comparison tolerance:

| Campaign | Suite | Phase | Mode vs baseline | tol 1e-9 | tol 1e-6 (stated) | tol 1e-4 | tol 1e-3 | tol 1e-2 |
|---|---|---|---|---|---|---|---|---|
| v2 | holdout | full | all | 3/20/7 | 2/21/7 | 0/26/4 | 0/28/2 | 0/29/1 |
| v2 | holdout | full | auto | 2/23/5 | 2/24/4 | 0/26/4 | 0/28/2 | 0/29/1 |
| v2 | holdout | root | all | 1/26/3 | 1/26/3 | 0/29/1 | 0/29/1 | 0/29/1 |
| v2 | holdout | root | auto | 1/28/1 | 1/28/1 | 0/29/1 | 0/29/1 | 0/29/1 |
| repair | holdout | full | all | 2/3/3 | 0/5/3 | 0/7/1 | 0/8/0 | 0/8/0 |
| repair | holdout | full | auto | 1/5/2 | 0/6/2 | 0/7/1 | 0/8/0 | 0/8/0 |
| v1 | holdout | full | control | 2/10/8 (+4 n/a) | 1/15/4 (+4 n/a) | 0/20/0 (+4 n/a) | 0/20/0 (+4 n/a) | 0/20/0 (+4 n/a) |
| v1 | holdout | full | all | 3/9/8 (+4 n/a) | 1/14/5 (+4 n/a) | 0/19/1 (+4 n/a) | 0/19/1 (+4 n/a) | 0/19/1 (+4 n/a) |
| v1 | holdout | full | auto | 4/10/6 (+4 n/a) | 3/12/5 (+4 n/a) | 0/19/1 (+4 n/a) | 0/19/1 (+4 n/a) | 0/19/1 (+4 n/a) |
| v1 | holdout | root | control | 4/11/5 (+4 n/a) | 2/15/3 (+4 n/a) | 2/15/3 (+4 n/a) | 2/15/3 (+4 n/a) | 2/15/3 (+4 n/a) |
| v1 | holdout | root | all | 5/11/4 (+4 n/a) | 3/15/2 (+4 n/a) | 3/15/2 (+4 n/a) | 3/15/2 (+4 n/a) | 3/15/2 (+4 n/a) |
| v1 | holdout | root | auto | 5/10/5 (+4 n/a) | 3/14/3 (+4 n/a) | 3/14/3 (+4 n/a) | 3/14/3 (+4 n/a) | 3/14/3 (+4 n/a) |

Models behind the better/worse outcomes at the stated tolerance 1e-6:

| Campaign | Suite | Phase | Mode vs baseline | Outcome at tol 1e-06 | Models |
|---|---|---|---|---|---|
| v2 | holdout | full | all | better | nous1, st_e22 |
| v2 | holdout | full | all | worse | ex4_1_8, cvxnonsep_normcon20r, cvxnonsep_psig20r, graphpart_clique-40, ex5_2_5, tln7, waterx |
| v2 | holdout | full | auto | better | nous1, st_e22 |
| v2 | holdout | full | auto | worse | graphpart_clique-40, ex5_2_5, tln7, waterx |
| v2 | holdout | root | all | better | st_e22 |
| v2 | holdout | root | all | worse | ex4_1_8, cvxnonsep_normcon20r, graphpart_clique-40 |
| v2 | holdout | root | auto | better | st_e22 |
| v2 | holdout | root | auto | worse | graphpart_clique-40 |
| repair | holdout | full | all | worse | hybriddynamic_var, tln7, waterx |
| repair | holdout | full | auto | worse | hybriddynamic_var, waterx |
| v1 | holdout | full | control | better | ex9_2_6 |
| v1 | holdout | full | control | worse | kall_congruentcircles_c42, ex7_2_4, ex7_2_2, pooling_adhya2pq |
| v1 | holdout | full | all | better | ex9_2_6 |
| v1 | holdout | full | all | worse | kall_congruentcircles_c42, genpooling_lee2, ex7_2_4, ex7_2_2, pooling_adhya2pq |
| v1 | holdout | full | auto | better | pooling_adhya2stp, ex9_2_6, ex7_2_4 |
| v1 | holdout | full | auto | worse | kall_congruentcircles_c42, genpooling_lee2, pointpack06, ex7_2_2, pooling_adhya2pq |

Models behind the better/worse outcomes that survive a tolerance equal to the 1e-4 gap limit:

| Campaign | Suite | Phase | Mode vs baseline | Outcome at tol 0.0001 | Models |
|---|---|---|---|---|---|
| v2 | holdout | full | all | worse | graphpart_clique-40, ex5_2_5, tln7, waterx |
| v2 | holdout | full | auto | worse | graphpart_clique-40, ex5_2_5, tln7, waterx |
| v2 | holdout | root | all | worse | graphpart_clique-40 |
| v2 | holdout | root | auto | worse | graphpart_clique-40 |
| repair | holdout | full | all | worse | waterx |
| repair | holdout | full | auto | worse | waterx |
| v1 | holdout | full | all | worse | genpooling_lee2 |
| v1 | holdout | full | auto | worse | genpooling_lee2 |
| v1 | holdout | root | control | better | ex4, genpooling_lee2 |
| v1 | holdout | root | control | worse | tltr, ex7_2_4, ex7_2_2 |
| v1 | holdout | root | all | better | ex4, genpooling_lee2, pointpack06 |
| v1 | holdout | root | all | worse | ex7_2_4, ex7_2_2 |
| v1 | holdout | root | auto | better | ex4, genpooling_lee2, pointpack06 |
| v1 | holdout | root | auto | worse | tltr, ex7_2_4, ex7_2_2 |

Baseline A/A reruns (native SCIP only; quantifies run-to-run and seed variation on the shared host):

| Rerun pair | Pairs | Better | Tie | Worse | Status changes | Both solved | Min time ratio | Median time ratio | Max time ratio |
|---|---|---|---|---|---|---|---|---|---|
| v2 baseline -> repair baseline, same seed and model (25 groups) | 25 | 3 | 22 | 0 | 0 | 9 | 0.95 | 1.00 | 1.05 |
| v2 baseline seed 0 -> seed 1 (6 holdout models) | 6 | 2 | 4 | 0 | 1 | 6 | 0.86 | 1.09 | 1.19 |
| v1 baseline seed 0 -> seed 1 (6 models) | 6 | 2 | 3 | 1 | 0 | 5 | 0.96 | 1.05 | 1.47 |

Hardness profile of the application populations (integration time of solved runs):

| Campaign | Suite | Mode | Models | Solved < 0.1 s | 0.1-1 s | 1-5 s | >= 5 s | Unsolved or not admitted |
|---|---|---|---|---|---|---|---|---|
| v2 | holdout | baseline | 30 | 8 | 11 | 6 | 0 | 5 |
| v2 | holdout | all | 30 | 4 | 12 | 7 | 2 | 5 |
| v2 | holdout | auto | 30 | 5 | 11 | 7 | 2 | 5 |
| v1 | holdout | baseline | 24 | 11 | 5 | 2 | 1 | 5 |
| v1 | holdout | control | 24 | 8 | 6 | 5 | 0 | 5 |
| v1 | holdout | all | 24 | 6 | 7 | 5 | 0 | 6 |
| v1 | holdout | auto | 24 | 7 | 7 | 4 | 0 | 6 |

Primary campaign-v2 discovery overruns (allowance = min(max_separation_seconds, separation_budget_fraction * (time limit - preparation))) and where the cut-mode overhead arises:

| Suite | Phase | Mode | Runs with record | Discovery over allowance | Discovery s | Excess over allowance s | Mode vs baseline s (repair groups) | Mode vs baseline s (other groups) |
|---|---|---|---|---|---|---|---|---|
| holdout | full | all | 30 | 8 | 24.41 | 14.18 | 134.61 vs 123.84 | 52.42 vs 46.74 |
| holdout | full | auto | 30 | 8 | 24.63 | 14.39 | 134.96 vs 123.84 | 52.16 vs 46.74 |
| holdout | root | all | 30 | 9 | 24.20 | 20.12 | 27.42 vs 6.17 | 10.61 vs 7.84 |
| holdout | root | auto | 30 | 9 | 23.39 | 19.41 | 26.90 vs 6.17 | 9.96 vs 7.84 |
| holdout | repeat | all | 6 | 1 | 4.68 | 2.95 | 5.31 vs 1.36 | 9.70 vs 8.25 |
| holdout | repeat | auto | 6 | 1 | 4.74 | 2.98 | 5.13 vs 1.36 | 9.76 vs 8.25 |
| diagnostic | full | all | 8 | 5 | 28.55 | 21.86 | 42.88 vs 36.28 | 61.06 vs 60.23 |
| diagnostic | full | auto | 8 | 5 | 27.83 | 21.07 | 42.57 vs 36.28 | 60.88 vs 60.23 |
| synthetic | full | all | 13 | 0 | 0.03 | 0.00 | 0.00 vs 0.00 | 10.86 vs 10.69 |
| synthetic | full | auto | 13 | 0 | 0.04 | 0.00 | 0.00 vs 0.00 | 10.69 vs 10.69 |
| synthetic | root | all | 5 | 0 | 0.04 | 0.00 | 0.00 vs 0.00 | 0.57 vs 0.28 |
| synthetic | root | auto | 5 | 0 | 0.04 | 0.00 | 0.00 vs 0.00 | 0.37 vs 0.28 |

Seed-one repeats (campaign-v2):

| Model | Mode | Seed-0 status / time (s) / cuts | Seed-1 status / time (s) / cuts |
|---|---|---|---|
| p_ball_10b_5p_2d_m | baseline | optimal / 1.47 / 0 | optimal / 1.36 / 0 |
| p_ball_10b_5p_2d_m | all | optimal / 5.46 / 0 | optimal / 5.31 / 0 |
| p_ball_10b_5p_2d_m | auto | optimal / 5.58 / 0 | optimal / 5.13 / 0 |
| st_glmp_kk90 | baseline | gaplimit / 0.03 / 0 | gaplimit / 0.04 / 0 |
| st_glmp_kk90 | all | gaplimit / 0.07 / 0 | gaplimit / 0.05 / 0 |
| st_glmp_kk90 | auto | gaplimit / 0.05 / 0 | gaplimit / 0.04 / 0 |
| du-opt5 | baseline | optimal / 0.69 / 0 | optimal / 0.75 / 0 |
| du-opt5 | all | optimal / 0.80 / 0 | optimal / 0.76 / 0 |
| du-opt5 | auto | optimal / 0.83 / 0 | optimal / 0.86 / 0 |
| nvs24 | baseline | gaplimit / 4.96 / 0 | gaplimit / 4.28 / 0 |
| nvs24 | all | gaplimit / 5.04 / 0 | gaplimit / 4.21 / 0 |
| nvs24 | auto | gaplimit / 5.05 / 0 | gaplimit / 4.19 / 0 |
| nous1 | baseline | gaplimit / 2.68 / 0 | optimal / 2.89 / 0 |
| nous1 | all | gaplimit / 4.57 / 2 | optimal / 4.24 / 2 |
| nous1 | auto | gaplimit / 4.63 / 2 | optimal / 4.22 / 2 |
| supplychain | baseline | optimal / 0.24 / 0 | optimal / 0.29 / 0 |
| supplychain | all | optimal / 0.43 / 0 | optimal / 0.45 / 0 |
| supplychain | auto | optimal / 0.49 / 0 | optimal / 0.46 / 0 |

Soft-budget overshoots > 0.01 s (campaign-v2):

| Campaign | Run | Soft budget (s) | Integration (s) | Excess (s) |
|---|---|---|---|---|
| v2 | 021_ex8_3_4__all__full | 30.0 | 30.0163 | 0.0163 |
| v2 | 022_ex8_3_4__auto__full | 30.0 | 30.0165 | 0.0165 |
| v2 | 023_ex8_3_4__baseline__full | 30.0 | 30.0179 | 0.0179 |
| v2 | 033_graphpart_clique-40__auto__full | 30.0 | 30.0176 | 0.0176 |
| v2 | 034_graphpart_clique-40__baseline__full | 30.0 | 30.0153 | 0.0153 |
| v2 | 035_graphpart_clique-40__all__full | 30.0 | 30.0143 | 0.0143 |
| v2 | 048_ex5_2_5__all__full | 30.0 | 30.0167 | 0.0167 |
| v2 | 049_ex5_2_5__auto__full | 30.0 | 30.0172 | 0.0172 |
| v2 | 050_ex5_2_5__baseline__full | 30.0 | 30.0176 | 0.0176 |
| v2 | 075_tln7__all__full | 30.0 | 30.0177 | 0.0177 |
| v2 | 076_tln7__auto__full | 30.0 | 30.0203 | 0.0203 |
| v2 | 077_tln7__baseline__full | 30.0 | 30.0186 | 0.0186 |
| v2 | 087_waterx__auto__full | 30.0 | 30.0193 | 0.0193 |
| v2 | 088_waterx__baseline__full | 30.0 | 30.0192 | 0.0192 |
| v2 | 089_waterx__all__full | 30.0 | 30.0190 | 0.0190 |
| v2 | 105_btest14__auto__full | 30.0 | 30.0186 | 0.0186 |
| v2 | 106_btest14__baseline__full | 30.0 | 30.0204 | 0.0204 |
| v2 | 107_btest14__all__full | 30.0 | 30.0204 | 0.0204 |
| v2 | 108_ghg_2veh__baseline__full | 30.0 | 30.0205 | 0.0205 |
| v2 | 109_ghg_2veh__all__full | 30.0 | 30.0202 | 0.0202 |
| v2 | 110_ghg_2veh__auto__full | 30.0 | 30.0202 | 0.0202 |
| v2 | 113_chp_partload__baseline__full | 30.0 | 30.0228 | 0.0228 |
| v2 | 114_kall_circles_c6b__auto__full | 30.0 | 30.0205 | 0.0205 |
| v2 | 115_kall_circles_c6b__baseline__full | 30.0 | 30.0207 | 0.0207 |
| v2 | 116_kall_circles_c6b__all__full | 30.0 | 30.0204 | 0.0204 |
| v2 | 117_waterno2_06__baseline__full | 30.0 | 30.0246 | 0.0246 |
| v2 | 123_quartic_balance_8__all__full | 10.0 | 10.0195 | 0.0195 |
| v2 | 192_graphpart_clique-40__auto__root | 5.0 | 6.7439 | 1.7439 |
| v2 | 194_graphpart_clique-40__all__root | 5.0 | 6.7685 | 1.7685 |

### Repair cohort: original versus repaired run, per job

| Phase | Suite | Model | Mode | Status orig/repair | Dual orig/repair | Time orig/repair (s) | Discovery orig/repair (s) | Cuts orig/repair | Repair discovery incomplete |
|---|---|---|---|---|---|---|---|---|---|
| full | holdout | p_ball_10b_5p_2d_m | baseline | optimal / optimal | 18.718576 / 18.718576 | 1.47 / 1.54 | 0 / 0 | 0 / 0 | False |
| full | holdout | p_ball_10b_5p_2d_m | all | optimal / optimal | 18.718576 / 18.718577 | 5.46 / 1.78 | 4.0029132 / 0.12853808 | 0 / 3 | False |
| full | holdout | p_ball_10b_5p_2d_m | auto | optimal / optimal | 18.718576 / 18.718576 | 5.58 / 1.62 | 4.1286745 / 0.14535032 | 0 / 0 | False |
| full | holdout | ex8_3_4 | all | timelimit / timelimit | -10 / -10 | 30.02 / 30.02 | 2.71177 / 0.098871464 | 0 / 6 | False |
| full | holdout | ex8_3_4 | auto | timelimit / timelimit | -10 / -10 | 30.02 / 30.02 | 2.6841301 / 0.11367291 | 0 / 0 | False |
| full | holdout | ex8_3_4 | baseline | timelimit / timelimit | -10 / -10 | 30.02 / 30.02 | 0 / 0 | 0 / 0 | False |
| full | holdout | hybriddynamic_var | all | gaplimit / gaplimit | 1.5362949 / 1.5362925 | 3.00 / 0.72 | 2.4409692 / 0.095824397 | 0 / 2 | False |
| full | holdout | hybriddynamic_var | auto | gaplimit / gaplimit | 1.5362949 / 1.5362925 | 3.08 / 0.80 | 2.4818169 / 0.076191665 | 0 / 2 | False |
| full | holdout | hybriddynamic_var | baseline | gaplimit / gaplimit | 1.5362949 / 1.5362949 | 0.54 / 0.53 | 0 / 0 | 0 / 0 | False |
| full | holdout | graphpart_clique-40 | auto | timelimit / timelimit | 392 / 438 | 30.02 / 30.02 | 6.0027848 / 0.65503049 | 0 / 0 | False |
| full | holdout | graphpart_clique-40 | baseline | timelimit / timelimit | 438 / 438 | 30.02 / 30.02 | 0 / 0 | 0 / 0 | False |
| full | holdout | graphpart_clique-40 | all | timelimit / timelimit | 392 / 438 | 30.01 / 30.02 | 6.0423311 / 0.6548706 | 0 / 0 | False |
| full | holdout | pooling_adhya4pq | baseline | optimal / optimal | -877.64575 / -877.64575 | 0.69 / 0.69 | 0 / 0 | 0 / 0 | False |
| full | holdout | pooling_adhya4pq | all | optimal / optimal | -877.64575 / -877.64574 | 2.61 / 1.21 | 1.8581662 / 0.13600572 | 0 / 1 | False |
| full | holdout | pooling_adhya4pq | auto | optimal / optimal | -877.64575 / -877.64574 | 2.75 / 1.22 | 1.9721789 / 0.14384221 | 0 / 1 | False |
| full | holdout | tln7 | all | timelimit / timelimit | 14.469017 / 14.480169 | 30.02 / 30.02 | 1.24332 / 0.063368963 | 0 / 0 | False |
| full | holdout | tln7 | auto | timelimit / timelimit | 14.46701 / 14.480973 | 30.02 / 30.02 | 1.2816703 / 0.045662662 | 0 / 0 | False |
| full | holdout | tln7 | baseline | timelimit / timelimit | 14.475541 / 14.480973 | 30.02 / 30.02 | 0 / 0 | 0 / 0 | False |
| full | holdout | graphpart_2g-0066-0066 | baseline | optimal / optimal | -2865560 / -2865560 | 1.07 / 1.06 | 0 / 0 | 0 / 0 | False |
| full | holdout | graphpart_2g-0066-0066 | all | optimal / optimal | -2865560 / -2865560 | 3.47 / 1.05 | 2.3963904 / 0.076492372 | 0 / 0 | False |
| full | holdout | graphpart_2g-0066-0066 | auto | optimal / optimal | -2865560 / -2865560 | 3.47 / 1.09 | 2.3438111 / 0.059973622 | 0 / 0 | False |
| full | holdout | waterx | auto | timelimit / timelimit | 514.06461 / 514.26438 | 30.02 / 30.02 | 1.4977743 / 0.084099093 | 0 / 0 | False |
| full | holdout | waterx | baseline | timelimit / timelimit | 514.26438 / 514.72401 | 30.02 / 30.02 | 0 / 0 | 0 / 0 | False |
| full | holdout | waterx | all | timelimit / timelimit | 514.03152 / 514.49296 | 30.02 / 30.02 | 1.4814036 / 0.077921466 | 0 / 0 | False |
| full | diagnostic | genpooling_lee2 | baseline | optimal / optimal | -3849.2654 / -3849.2654 | 5.56 / 5.61 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | genpooling_lee2 | all | optimal / optimal | -3849.2654 / -3849.2654 | 7.26 / 4.15 | 1.6174259 / 0.16744913 | 0 / 2 | False |
| full | diagnostic | genpooling_lee2 | auto | optimal / optimal | -3849.2654 / -3849.2654 | 7.05 / 5.76 | 1.5626517 / 0.14205794 | 0 / 0 | False |
| full | diagnostic | syn15m | all | gaplimit / gaplimit | 853.28609 / 853.28672 | 1.29 / 0.49 | 1.1610531 / 0.066065609 | 0 / 8 | False |
| full | diagnostic | syn15m | auto | gaplimit / gaplimit | 853.28609 / 853.28609 | 1.26 / 0.16 | 1.1468773 / 0.048436994 | 0 / 0 | False |
| full | diagnostic | syn15m | baseline | gaplimit / gaplimit | 853.28609 / 853.28609 | 0.11 / 0.11 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | cvxnonsep_pcon40r | baseline | gaplimit / gaplimit | -46.602868 / -46.602868 | 0.24 / 0.24 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | cvxnonsep_pcon40r | all | gaplimit / gaplimit | -46.602868 / -46.602868 | 1.44 / 0.42 | 1.2004041 / 0.13836788 | 0 / 0 | False |
| full | diagnostic | cvxnonsep_pcon40r | auto | gaplimit / gaplimit | -46.602868 / -46.602868 | 1.40 / 0.36 | 1.1772012 / 0.12665176 | 0 / 0 | False |
| full | diagnostic | syn10hfsg | all | gaplimit / gaplimit | 1267.3566 / 1267.3566 | 2.87 / 0.41 | 2.5037036 / 0.097291002 | 0 / 0 | False |
| full | diagnostic | syn10hfsg | auto | gaplimit / gaplimit | 1267.3566 / 1267.3566 | 2.84 / 0.39 | 2.4869235 / 0.099455828 | 0 / 0 | False |
| full | diagnostic | syn10hfsg | baseline | gaplimit / gaplimit | 1267.3566 / 1267.3566 | 0.34 / 0.34 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | btest14 | auto | timelimit / timelimit | -115.59607 / -72.284455 | 30.02 / 30.02 | 19.692306 / 0.47951992 | 0 / 0 | False |
| full | diagnostic | btest14 | baseline | timelimit / timelimit | -72.296277 / -72.284455 | 30.02 / 30.02 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | btest14 | all | timelimit / timelimit | -115.59607 / -72.284455 | 30.02 / 30.02 | 20.37887 / 0.37813125 | 0 / 0 | False |
| full | diagnostic | chp_partload | all | worker_error / timelimit | - / 20.324697 | - / 30.00 | - / 1.0036177 | None / 0 | True |
| full | diagnostic | chp_partload | auto | worker_error / timelimit | - / 20.324697 | - / 30.00 | - / 1.0007915 | None / 0 | True |
| full | diagnostic | chp_partload | baseline | timelimit / timelimit | 20.324697 / 20.324697 | 30.02 / 30.00 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | waterno2_06 | baseline | timelimit / timelimit | 81.639861 / 81.639861 | 30.02 / 30.02 | 0 / 0 | 0 / 0 | False |
| full | diagnostic | waterno2_06 | all | worker_error / timelimit | - / 76.753373 | - / 30.00 | - / 1.0008945 | None / 0 | True |
| full | diagnostic | waterno2_06 | auto | worker_error / timelimit | - / 76.753373 | - / 30.02 | - / 1.002916 | None / 0 | True |
| root | holdout | p_ball_10b_5p_2d_m | baseline | nodelimit / nodelimit | 0 / 0 | 0.70 / 0.63 | 0 / 0 | 0 / 0 | False |
| root | holdout | p_ball_10b_5p_2d_m | all | nodelimit / nodelimit | 0 / 0 | 4.84 / 0.70 | 4.1915685 / 0.16220567 | 0 / 3 | False |
| root | holdout | p_ball_10b_5p_2d_m | auto | nodelimit / nodelimit | 0 / 0 | 4.78 / 0.75 | 3.9945948 / 0.11378903 | 0 / 0 | False |
| root | holdout | nous1 | all | nodelimit / nodelimit | 0.3451122 / 0.3451122 | 0.57 / 0.42 | 0.37305912 / 0.071201092 | 0 / 0 | False |
| root | holdout | nous1 | auto | nodelimit / nodelimit | 0.3451122 / 0.3451122 | 0.49 / 0.43 | 0.34728056 / 0.081357841 | 0 / 1 | False |
| root | holdout | nous1 | baseline | nodelimit / nodelimit | 0.3451122 / 0.3451122 | 0.15 / 0.14 | 0 / 0 | 0 / 0 | False |
| root | holdout | ex8_3_4 | all | nodelimit / nodelimit | -10 / -10 | 3.66 / 0.87 | 2.9316779 / 0.089367858 | 0 / 6 | False |
| root | holdout | ex8_3_4 | auto | nodelimit / nodelimit | -10 / -10 | 3.45 / 0.79 | 2.7462579 / 0.085726357 | 0 / 0 | False |
| root | holdout | ex8_3_4 | baseline | nodelimit / nodelimit | -10 / -10 | 0.70 / 0.63 | 0 / 0 | 0 / 0 | False |
| root | holdout | hybriddynamic_var | all | nodelimit / nodelimit | 1.5040996 / 1.5040995 | 2.40 / 0.26 | 2.2787003 / 0.09668506 | 0 / 2 | False |
| root | holdout | hybriddynamic_var | auto | nodelimit / nodelimit | 1.5040996 / 1.5040995 | 2.28 / 0.27 | 2.1772335 / 0.095078223 | 0 / 2 | False |
| root | holdout | hybriddynamic_var | baseline | nodelimit / nodelimit | 1.5040996 / 1.5040996 | 0.13 / 0.09 | 0 / 0 | 0 / 0 | False |
| root | holdout | graphpart_clique-40 | auto | timelimit / nodelimit | 0 / 0.28571429 | 6.74 / 2.33 | 5.6032803 / 0.24962431 | 0 / 0 | True |
| root | holdout | graphpart_clique-40 | baseline | nodelimit / nodelimit | 0.28571429 / 0.28571429 | 2.24 / 2.01 | 0 / 0 | 0 / 0 | False |
| root | holdout | graphpart_clique-40 | all | timelimit / nodelimit | 0 / 0.28571429 | 6.77 / 2.05 | 5.7578789 / 0.2497184 | 0 / 0 | True |
| root | holdout | pooling_adhya4pq | baseline | nodelimit / nodelimit | -961.93218 / -961.93218 | 0.62 / 0.62 | 0 / 0 | 0 / 0 | False |
| root | holdout | pooling_adhya4pq | all | nodelimit / nodelimit | -961.93218 / -961.93218 | 2.64 / 0.88 | 1.8922779 / 0.1235099 | 0 / 0 | False |
| root | holdout | pooling_adhya4pq | auto | nodelimit / nodelimit | -961.93218 / -961.93218 | 2.56 / 0.92 | 1.9458335 / 0.16804001 | 0 / 0 | False |
| root | holdout | tln7 | all | nodelimit / nodelimit | 13.811394 / 13.811394 | 1.52 / 0.40 | 1.1463868 / 0.05716433 | 0 / 0 | False |
| root | holdout | tln7 | auto | nodelimit / nodelimit | 13.811394 / 13.811394 | 1.49 / 0.36 | 1.1747536 / 0.041291688 | 0 / 0 | False |
| root | holdout | tln7 | baseline | nodelimit / nodelimit | 13.811394 / 13.811394 | 0.32 / 0.35 | 0 / 0 | 0 / 0 | False |
| root | holdout | graphpart_2g-0066-0066 | baseline | nodelimit / nodelimit | -2891969.6 / -2891969.6 | 0.32 / 0.32 | 0 / 0 | 0 / 0 | False |
| root | holdout | graphpart_2g-0066-0066 | all | nodelimit / nodelimit | -2891969.6 / -2891969.6 | 2.61 / 0.39 | 2.310963 / 0.067744127 | 0 / 0 | False |
| root | holdout | graphpart_2g-0066-0066 | auto | nodelimit / nodelimit | -2891969.6 / -2891969.6 | 2.66 / 0.35 | 2.3008781 / 0.054004325 | 0 / 0 | False |
| root | holdout | waterx | auto | nodelimit / nodelimit | 182.84245 / 182.84245 | 2.45 / 1.06 | 1.3729463 / 0.089570933 | 0 / 0 | False |
| root | holdout | waterx | baseline | nodelimit / nodelimit | 182.84245 / 182.84245 | 0.99 / 1.05 | 0 / 0 | 0 / 0 | False |
| root | holdout | waterx | all | nodelimit / nodelimit | 182.84245 / 182.84245 | 2.41 / 1.06 | 1.4837242 / 0.063779245 | 0 / 0 | False |
| repeat | holdout | p_ball_10b_5p_2d_m | baseline | optimal / optimal | 18.718574 / 18.718574 | 1.36 / 1.30 | 0 / 0 | 0 / 0 | False |
| repeat | holdout | p_ball_10b_5p_2d_m | all | optimal / optimal | 18.718574 / 18.718574 | 5.31 / 1.91 | 3.9510482 / 0.14689619 | 0 / 3 | False |
| repeat | holdout | p_ball_10b_5p_2d_m | auto | optimal / optimal | 18.718574 / 18.718574 | 5.13 / 1.45 | 3.977984 / 0.13989018 | 0 / 0 | False |

| Campaign | Suite | Phase | Comparison | Bound | Better | Tie | Worse | Unavailable |
|---|---|---|---|---|---|---|---|---|
| repair | holdout | full | all vs baseline | dual | 0 | 5 | 3 | 0 |
| repair | holdout | full | auto vs baseline | dual | 0 | 6 | 2 | 0 |
| repair | diagnostic | full | all vs baseline | dual | 0 | 6 | 1 | 0 |
| repair | diagnostic | full | auto vs baseline | dual | 0 | 6 | 1 | 0 |
| repair | holdout | root | all vs baseline | dual | 0 | 9 | 0 | 0 |
| repair | holdout | root | auto vs baseline | dual | 0 | 9 | 0 | 0 |
| repair | holdout | repeat | all vs baseline | dual | 0 | 1 | 0 | 0 |
| repair | holdout | repeat | auto vs baseline | dual | 0 | 1 | 0 | 0 |

### (f) Campaign-v1 (Report A) analogue

| Campaign | Suite | Phase | Mode | Runs | Admitted | Solved | Statuses | Cuts | Runs with cuts | Unknown cut logs | Integration s | Outer s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | synthetic | full | baseline | 13 | 13 | 12 | {'gaplimit': 3, 'optimal': 9, 'timelimit': 1} | 0 | 0 | 0 | 6.57 | 16.94 |
| v1 | synthetic | full | control | 13 | 13 | 13 | {'gaplimit': 2, 'optimal': 11} | 0 | 0 | 0 | 1.66 | 11.57 |
| v1 | synthetic | full | all | 13 | 13 | 13 | {'gaplimit': 4, 'optimal': 9} | 89 | 7 | 0 | 2.51 | 13.18 |
| v1 | synthetic | full | auto | 13 | 13 | 13 | {'gaplimit': 4, 'optimal': 9} | 72 | 7 | 0 | 2.45 | 13.14 |
| v1 | holdout | full | baseline | 24 | 20 | 19 | {'gaplimit': 5, 'optimal': 14, 'source_model_mismatch': 3, 'timelimit': 1, 'worker_error': 1} | 0 | 0 | 1 | 17.40 | 36.66 |
| v1 | holdout | full | control | 24 | 20 | 19 | {'gaplimit': 5, 'optimal': 14, 'source_model_mismatch': 3, 'timelimit': 1, 'worker_error': 1} | 0 | 0 | 1 | 20.66 | 40.12 |
| v1 | holdout | full | all | 24 | 20 | 18 | {'gaplimit': 4, 'optimal': 14, 'source_model_mismatch': 3, 'timelimit': 2, 'worker_error': 1} | 230 | 12 | 1 | 25.41 | 45.44 |
| v1 | holdout | full | auto | 24 | 20 | 18 | {'gaplimit': 5, 'optimal': 13, 'source_model_mismatch': 3, 'timelimit': 2, 'worker_error': 1} | 106 | 8 | 1 | 23.01 | 42.49 |
| v1 | historical | full | baseline | 4 | 1 | 0 | {'source_model_mismatch': 3, 'timelimit': 1} | 0 | 0 | 0 | 6.22 | 9.60 |
| v1 | historical | full | control | 4 | 1 | 0 | {'source_model_mismatch': 3, 'timelimit': 1} | 0 | 0 | 0 | 6.84 | 10.36 |
| v1 | historical | full | all | 4 | 1 | 0 | {'source_model_mismatch': 3, 'timelimit': 1} | 24 | 1 | 0 | 6.91 | 10.41 |
| v1 | historical | full | auto | 4 | 1 | 0 | {'source_model_mismatch': 3, 'timelimit': 1} | 24 | 1 | 0 | 6.88 | 10.26 |
| v1 | holdout | root | baseline | 24 | 20 | 10 | {'nodelimit': 10, 'optimal': 10, 'source_model_mismatch': 3, 'worker_error': 1} | 0 | 0 | 1 | 3.20 | 22.62 |
| v1 | holdout | root | control | 24 | 20 | 8 | {'nodelimit': 12, 'optimal': 8, 'source_model_mismatch': 3, 'worker_error': 1} | 0 | 0 | 1 | 6.32 | 25.63 |
| v1 | holdout | root | all | 24 | 20 | 9 | {'nodelimit': 11, 'optimal': 9, 'source_model_mismatch': 3, 'worker_error': 1} | 158 | 12 | 1 | 10.20 | 29.82 |
| v1 | holdout | root | auto | 24 | 20 | 8 | {'nodelimit': 12, 'optimal': 8, 'source_model_mismatch': 3, 'worker_error': 1} | 54 | 7 | 1 | 8.94 | 28.64 |
| v1 | synthetic | root | baseline | 5 | 5 | 2 | {'nodelimit': 3, 'optimal': 2} | 0 | 0 | 0 | 0.28 | 4.23 |
| v1 | synthetic | root | control | 5 | 5 | 3 | {'nodelimit': 2, 'optimal': 3} | 0 | 0 | 0 | 0.30 | 4.29 |
| v1 | synthetic | root | all | 5 | 5 | 2 | {'nodelimit': 3, 'optimal': 2} | 39 | 4 | 0 | 1.24 | 5.44 |
| v1 | synthetic | root | auto | 5 | 5 | 2 | {'nodelimit': 3, 'optimal': 2} | 32 | 4 | 0 | 1.16 | 5.29 |
| v1 | holdout | repeat | baseline | 3 | 3 | 3 | {'gaplimit': 1, 'optimal': 2} | 0 | 0 | 0 | 2.43 | 4.86 |
| v1 | holdout | repeat | control | 3 | 3 | 3 | {'gaplimit': 1, 'optimal': 2} | 0 | 0 | 0 | 3.50 | 5.91 |
| v1 | holdout | repeat | all | 3 | 3 | 3 | {'gaplimit': 1, 'optimal': 2} | 50 | 3 | 0 | 5.53 | 7.92 |
| v1 | holdout | repeat | auto | 3 | 3 | 3 | {'gaplimit': 2, 'optimal': 1} | 24 | 2 | 0 | 3.98 | 6.46 |
| v1 | synthetic | repeat | baseline | 3 | 3 | 2 | {'gaplimit': 1, 'optimal': 1, 'timelimit': 1} | 0 | 0 | 0 | 6.08 | 8.42 |
| v1 | synthetic | repeat | control | 3 | 3 | 3 | {'optimal': 3} | 0 | 0 | 0 | 1.12 | 3.35 |
| v1 | synthetic | repeat | all | 3 | 3 | 3 | {'gaplimit': 1, 'optimal': 2} | 33 | 2 | 0 | 0.84 | 3.10 |
| v1 | synthetic | repeat | auto | 3 | 3 | 3 | {'gaplimit': 1, 'optimal': 2} | 29 | 2 | 0 | 0.78 | 3.20 |
| v1 | synthetic | no_cache | all | 5 | 5 | 5 | {'gaplimit': 1, 'optimal': 4} | 60 | 4 | 0 | 1.86 | 5.89 |
| v1 | synthetic | no_cache | auto | 5 | 5 | 5 | {'gaplimit': 1, 'optimal': 4} | 44 | 4 | 0 | 1.90 | 6.04 |
| v1 | synthetic | pairs_only | all | 1 | 1 | 1 | {'optimal': 1} | 14 | 1 | 0 | 0.19 | 0.92 |
| v1 | synthetic | pairs_only | auto | 1 | 1 | 1 | {'optimal': 1} | 0 | 0 | 0 | 0.10 | 0.87 |

| Campaign | Suite | Phase | Comparison | Bound | Better | Tie | Worse | Unavailable |
|---|---|---|---|---|---|---|---|---|
| v1 | synthetic | full | control vs baseline | dual | 3 | 10 | 0 | 0 |
| v1 | synthetic | full | all vs baseline | dual | 2 | 9 | 2 | 0 |
| v1 | synthetic | full | auto vs baseline | dual | 2 | 9 | 2 | 0 |
| v1 | holdout | full | control vs baseline | dual | 1 | 15 | 4 | 4 |
| v1 | holdout | full | all vs baseline | dual | 1 | 14 | 5 | 4 |
| v1 | holdout | full | auto vs baseline | dual | 3 | 12 | 5 | 4 |
| v1 | historical | full | control vs baseline | dual | 0 | 0 | 1 | 3 |
| v1 | historical | full | all vs baseline | dual | 0 | 0 | 1 | 3 |
| v1 | historical | full | auto vs baseline | dual | 0 | 0 | 1 | 3 |
| v1 | holdout | root | control vs baseline | dual | 2 | 15 | 3 | 4 |
| v1 | holdout | root | all vs baseline | dual | 3 | 15 | 2 | 4 |
| v1 | holdout | root | auto vs baseline | dual | 3 | 14 | 3 | 4 |
| v1 | synthetic | root | control vs baseline | dual | 2 | 2 | 1 | 0 |
| v1 | synthetic | root | all vs baseline | dual | 1 | 2 | 2 | 0 |
| v1 | synthetic | root | auto vs baseline | dual | 2 | 2 | 1 | 0 |
| v1 | holdout | repeat | control vs baseline | dual | 1 | 1 | 1 | 0 |
| v1 | holdout | repeat | all vs baseline | dual | 2 | 1 | 0 | 0 |
| v1 | holdout | repeat | auto vs baseline | dual | 2 | 0 | 1 | 0 |
| v1 | synthetic | repeat | control vs baseline | dual | 2 | 1 | 0 | 0 |
| v1 | synthetic | repeat | all vs baseline | dual | 2 | 1 | 0 | 0 |
| v1 | synthetic | repeat | auto vs baseline | dual | 2 | 1 | 0 | 0 |
| v1 | synthetic | full | all vs control | dual | 0 | 9 | 4 | 0 |
| v1 | synthetic | full | auto vs control | dual | 0 | 10 | 3 | 0 |
| v1 | holdout | full | all vs control | dual | 3 | 16 | 1 | 4 |
| v1 | holdout | full | auto vs control | dual | 3 | 16 | 1 | 4 |
| v1 | holdout | full | control vs baseline | root_dual | 2 | 6 | 2 | 14 |
| v1 | holdout | full | all vs baseline | root_dual | 2 | 5 | 2 | 15 |
| v1 | holdout | full | auto vs baseline | root_dual | 3 | 4 | 3 | 14 |

The 24 campaign-v1 held-out models (full runs, 6 s); cell = status ('*' unsolved), seconds, cuts:

| Model | Vars | Rows | OSiL bytes | Integer | Convex | Reference primal | baseline | control | all | auto |
|---|---|---|---|---|---|---|---|---|---|---|
| kall_congruentcircles_c42 | 12 | 24 | 4270 | no | no | 0.858407346 | optimal 0.23s 0c | gaplimit 0.33s 0c | optimal 0.80s 21c | gaplimit 0.55s 13c |
| pooling_adhya2stp | 46 | 79 | 9104 | no | no | -549.8030502 | gaplimit 0.92s 0c | gaplimit 1.63s 0c | gaplimit 2.67s 15c | gaplimit 2.36s 11c |
| ex4 | 36 | 30 | 15115 | yes | yes | -8.064136165 | optimal 0.89s 0c | optimal 1.47s 0c | optimal 1.43s 14c | optimal 1.36s 0c |
| genpooling_lee2 | 53 | 92 | 16270 | yes | no | -3849.265424 | optimal 5.61s 0c | optimal 4.89s 0c | timelimit* 6.00s 23c | timelimit* 6.00s 24c |
| ex9_2_6 | 16 | 12 | 2368 | no | no | -1.0 | gaplimit 0.05s 0c | optimal 0.06s 0c | optimal 0.12s 0c | optimal 0.05s 0c |
| cvxnonsep_normcon30r | 60 | 31 | 5523 | yes | yes | -34.24396574 | optimal 0.08s 0c | optimal 0.15s 0c | optimal 0.43s 24c | optimal 0.14s 0c |
| pointpack06 | 13 | 21 | 6258 | no | no | 0.3611111113 | optimal 1.37s 0c | optimal 2.51s 0c | optimal 2.86s 24c | optimal 2.45s 15c |
| ex14_2_9 | 4 | 5 | 7515 | no | no | 2.22044605e-15 | optimal 0.05s 0c | optimal 0.06s 0c | optimal 0.07s 0c | optimal 0.05s 0c |
| syn15m | 55 | 89 | 10902 | yes | yes | 853.2847292 | refused* 0.00s 0c | refused* 0.01s 0c | refused* 0.00s 0c | refused* 0.00s 0c |
| st_robot | 8 | 8 | 2216 | no | no | 0.0 | optimal 0.05s 0c | optimal 0.06s 0c | optimal 0.04s 0c | optimal 0.04s 0c |
| ex14_1_3 | 3 | 4 | 1445 | no | no | -1.665334537e-16 | optimal 0.03s 0c | optimal 0.04s 0c | optimal 0.03s 0c | optimal 0.03s 0c |
| tltr | 48 | 54 | 8250 | yes | no | 48.06666667 | optimal 0.07s 0c | optimal 0.25s 0c | optimal 0.82s 22c | optimal 0.60s 11c |
| ex7_2_4 | 8 | 4 | 2432 | no | no | 3.918010226 | gaplimit 1.25s 0c | gaplimit 1.96s 0c | gaplimit 1.68s 13c | gaplimit 1.61s 5c |
| ex7_2_2 | 6 | 5 | 1703 | no | no | -0.3888114343 | gaplimit 0.15s 0c | gaplimit 0.17s 0c | gaplimit 0.25s 0c | gaplimit 0.16s 0c |
| pooling_adhya2pq | 33 | 57 | 7052 | no | no | -549.8030502 | gaplimit 0.37s 0c | gaplimit 0.51s 0c | gaplimit 1.23s 21c | gaplimit 0.96s 9c |
| ex9_2_4 | 8 | 7 | 1666 | no | no | 0.5 | optimal 0.03s 0c | optimal 0.04s 0c | optimal 0.09s 0c | optimal 0.04s 0c |
| cvxnonsep_psig30r | 62 | 32 | 7201 | yes | yes | 78.99885434 | refused* 0.01s 0c | refused* 0.01s 0c | refused* 0.01s 0c | refused* 0.01s 0c |
| cvxnonsep_normcon40 | 40 | 1 | 4328 | yes | yes | -32.62966972 | optimal 0.07s 0c | optimal 0.33s 0c | optimal 0.58s 24c | optimal 0.35s 0c |
| ex14_2_8 | 4 | 5 | 6178 | no | no | 0.0 | optimal 0.04s 0c | optimal 0.06s 0c | optimal 0.07s 0c | optimal 0.05s 0c |
| cvxnonsep_pcon40r | 79 | 40 | 9038 | yes | yes | -46.59916883 | error* -s ?c | error* -s ?c | error* -s ?c | error* -s ?c |
| ex1265a | 35 | 44 | 6952 | yes | no | 10.3 | optimal 0.07s 0c | optimal 0.10s 0c | optimal 0.20s 5c | optimal 0.12s 0c |
| kall_circles_c6b | 18 | 54 | 10292 | no | no | 1.973599702 | timelimit* 6.02s 0c | timelimit* 6.00s 0c | timelimit* 6.00s 24c | timelimit* 6.00s 18c |
| syn10hfsg | 77 | 112 | 13994 | yes | yes | 1267.35355 | refused* 0.00s 0c | refused* 0.00s 0c | refused* 0.01s 0c | refused* 0.00s 0c |
| procsel | 10 | 7 | 1725 | yes | no | -1.923098738 | optimal 0.04s 0c | optimal 0.03s 0c | optimal 0.04s 0c | optimal 0.04s 0c |

Campaign-v1 admitted held-out models not solved in every mode:

| Campaign | Model | Mode | Status | Primal | Dual | Abs gap | SCIP rel. gap | Archived reference | Nodes | Time (s) | Cuts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| v1 | genpooling_lee2 | baseline | optimal | -3849.2654 | -3849.2654 | 0 | 0.00% | -3849.265424 / -3849.265433 | 2006 | 5.61 | 0 |
| v1 | genpooling_lee2 | control | optimal | -3849.2654 | -3849.2654 | 0 | 0.00% | -3849.265424 / -3849.265433 | 2738 | 4.89 | 0 |
| v1 | genpooling_lee2 | all | timelimit | -3209.0381 | -4303.588 | 1094.5499 | 34.11% | -3849.265424 / -3849.265433 | 1050 | 6.00 | 23 |
| v1 | genpooling_lee2 | auto | timelimit | -3838.6666 | -4373.813 | 535.14641 | 13.94% | -3849.265424 / -3849.265433 | 1007 | 6.00 | 24 |
| v1 | kall_circles_c6b | baseline | timelimit | 2.1582602 | 0 | 2.1582602 | inf | 1.973599702 / 1.973597167 | 6323 | 6.02 | 0 |
| v1 | kall_circles_c6b | control | timelimit | 2.1582601 | 0 | 2.1582601 | inf | 1.973599702 / 1.973597167 | 2521 | 6.00 | 0 |
| v1 | kall_circles_c6b | all | timelimit | 2.1582601 | 0 | 2.1582601 | inf | 1.973599702 / 1.973597167 | 2381 | 6.00 | 24 |
| v1 | kall_circles_c6b | auto | timelimit | 2.1582601 | 0 | 2.1582601 | inf | 1.973599702 / 1.973597167 | 2136 | 6.00 | 18 |

Campaign-v1 synthetic cases (full runs, 6 s):

| Case | Stratum (cases.py) | Description | Known optimum | baseline | control | all | auto |
|---|---|---|---|---|---|---|---|
| quartic_balance_4 | composite polynomial mechanism | min sum_i (x_i^4 - x_i^2), sum_i x_i = 0, x in [-1,1]^4; optimum -1 (separable nonconvex quartic with a linking row) | -1 | optimal; dual -1.000001; 0.19 s; 0 cuts | optimal; dual -1.0000019; 0.25 s; 0 cuts | gaplimit; dual -1.0000854; 0.29 s; 20 cuts | gaplimit; dual -1.0000854; 0.42 s; 20 cuts |
| quartic_balance_8 | composite polynomial mechanism | same as quartic_balance_4 with 8 variables; optimum -2 | -2 | timelimit (unsolved); dual -2.5867279; 6.00 s; 0 cuts | optimal; dual -2.0000041; 1.05 s; 0 cuts | gaplimit; dual -2.0001491; 0.78 s; 24 cuts | gaplimit; dual -2.0001491; 0.78 s; 24 cuts |
| cubic_moment | shared polynomial curve | min x^3 s.t. x^2 >= 1/4, x in [0,1]; optimum 1/8 (shared polynomial curve) | 0.125 | optimal; dual 0.125; 0.02 s; 0 cuts | optimal; dual 0.125; 0.02 s; 0 cuts | optimal; dual 0.125; 0.03 s; 0 cuts | optimal; dual 0.125; 0.02 s; 0 cuts |
| exp_pair | general exp curve | min e^x + e^-x s.t. e^x + e^-x >= 3, x in [-2,2]; optimum 3 (same exp expression in objective and row) | 3 | optimal; dual 3; 0.04 s; 0 cuts | optimal; dual 3; 0.05 s; 0 cuts | optimal; dual 3; 0.05 s; 0 cuts | optimal; dual 3; 0.03 s; 0 cuts |
| log_pair | general log curve | min log x - (1/2) log(1+2x), x in [1/4,2]; optimum log(1/4) - (1/2) log(3/2) (log curve) | -1.5890269 | gaplimit; dual -1.5890433; 0.02 s; 0 cuts | gaplimit; dual -1.5890433; 0.02 s; 0 cuts | gaplimit; dual -1.5890433; 0.03 s; 0 cuts | gaplimit; dual -1.5890433; 0.02 s; 0 cuts |
| trig_pair | general trigonometric curve | min sin x + cos x, x in [-pi,pi]; optimum -sqrt(2) (trigonometric curve) | -1.4142136 | gaplimit; dual -1.414263; 0.02 s; 0 cuts | gaplimit; dual -1.4142329; 0.03 s; 0 cuts | gaplimit; dual -1.4142693; 0.13 s; 5 cuts | gaplimit; dual -1.4142693; 0.10 s; 5 cuts |
| simplex_product | coupled two-variable domain | min -xy on {x+y<=1} in [0,1]^2; optimum -1/4 (box McCormick gives -1/2) | -0.25 | optimal; dual -0.25000001; 0.03 s; 0 cuts | optimal; dual -0.25; 0.03 s; 0 cuts | optimal; dual -0.25; 0.06 s; 1 cuts | optimal; dual -0.25; 0.04 s; 1 cuts |
| simplex_quadratic_vector | coupled quadratic vector | min x^2 + y^2 - 4xy on {x+y<=1} in [0,1]^2; optimum -1/2 (quadratic vector on a simplex) | -0.5 | gaplimit; dual -0.50000653; 0.04 s; 0 cuts | optimal; dual -0.50000001; 0.02 s; 0 cuts | optimal; dual -0.50000123; 0.14 s; 9 cuts | optimal; dual -0.50000069; 0.08 s; 5 cuts |
| overlapping_products | overlapping coupled blocks | min -y(x+z), x+y<=1, y+z<=1, [0,1]^3; optimum -1/2 (two overlapping coupled blocks) | -0.5 | optimal; dual -0.50000001; 0.03 s; 0 cuts | optimal; dual -0.50000001; 0.03 s; 0 cuts | optimal; dual -0.50000001; 0.41 s; 13 cuts | optimal; dual -0.50000001; 0.40 s; 12 cuts |
| star_marginal_inconsistency | pair marginals versus merged quadratic star | min (y-1/4-x/2)^2 + (y-5z/8)^2 + x(1-x) + z(1-z) on [0,1]^3; optimum 1/128 at (1,11/16,1); exact pair hulls glued on shared center moments give 0 | 0.0078125 | optimal; dual 0.0078124899; 0.10 s; 0 cuts | optimal; dual 0.0078119454; 0.10 s; 0 cuts | optimal; dual 0.0078124091; 0.50 s; 17 cuts | optimal; dual 0.0078116462; 0.48 s; 5 cuts |
| affine_control | neutral no nonlinear structure | min sum_i (i+1) x_i s.t. sum_i x_i >= 1, [0,1]^8; optimum 1 (no nonlinear structure; neutral control) | 1 | optimal; dual 1; 0.03 s; 0 cuts | optimal; dual 1; 0.02 s; 0 cuts | optimal; dual 1; 0.02 s; 0 cuts | optimal; dual 1; 0.02 s; 0 cuts |
| convex_redundant_control | adverse unnecessary convexification | min sum_i (x_i^2 + x_i^4), [-1,1]^8; optimum 0 (convex; unnecessary convexification, adverse control) | 0 | optimal; dual 0; 0.03 s; 0 cuts | optimal; dual -1.6e-08; 0.03 s; 0 cuts | optimal; dual -1.6e-08; 0.03 s; 0 cuts | optimal; dual -1.6e-08; 0.02 s; 0 cuts |
| binary_product_control | neutral native integer products | min -x0 x1 - x2 x3, sum x_i <= 2, binary x; optimum -1 (native integer products; neutral control) | -1 | optimal; dual -1; 0.02 s; 0 cuts | optimal; dual -1; 0.02 s; 0 cuts | optimal; dual -1; 0.02 s; 0 cuts | optimal; dual -1; 0.03 s; 0 cuts |

Soft-budget overshoots > 0.01 s (campaign-v1):

| Campaign | Run | Soft budget (s) | Integration (s) | Excess (s) |
|---|---|---|---|---|
| v1 | 138_kall_circles_c6b__baseline__full | 6.0 | 6.0153 | 0.0153 |
| v1 | 153_waterno2_06__auto__full | 6.0 | 6.0164 | 0.0164 |

