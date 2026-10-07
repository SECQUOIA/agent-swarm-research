# Campaign 4 runner

Implements `../campaign-v4-protocol.md`, Parts C2, C3, B2 and D. Part S (star
oracle scale) is `star_bench.py` with `star-bench.{json,log,md}` in this
directory; it is separate from this runner and not part of the snapshot.
Nothing here modifies `research-2026100*-convexification/`, `literature/`,
`../v3/` or `../v3d/`.

## Files

| File | Role |
|---|---|
| `snapshot.py` | Builds `snapshot/` from the manifest-verified campaign-3 snapshot (`../v3/snapshot`, integration.py `128fe10b...`), applies the two additions of the protocol to `research-20261003-convexification/solver/integration.py` by exact text replacement (`PATCHES`), adds the runner files listed in `common.RUNNER_FILES`, the protocol, `../v3d/README-diagnostic.md` and the frozen campaign-3 Part B selection, writes `scip-parameters.json` and `source-manifest.json` (SHA-256 per file). Refuses to overwrite. |
| `make_jobs.py` | Creates one output directory per launch, in the campaign-2/3 layout (`cases/`, snapshot copy with `frozen-cases/` and `original-osil/`, `source-manifest.json`, `jobs.json`, `build.json`). `--smoke` keeps a part's rules but uses one path instance or two models at 10 s soft / 30 s hard. |
| `mechanism.py` | Byte-identical copy of `../v3/mechanism.py` (interleaved path family, exact optimum and witness). |
| `v4_worker.py` | Runs one case in one mode (mode table below), including mode `gurobi`; independent primal check of every incumbent; refuses modules imported from outside the snapshot. |
| `driver.py` | The campaign-3 driver; worker path, slot directory (`v4/.slots`, six slots shared by all campaign-4 drivers) and the recorded package list (gurobipy added) differ. Resumable; stop with SIGTERM. |
| `replay_v4.py` | Archived replay of every recorded cut with tampering controls per cut mode, plus checks of the recorded Config, SCIP parameters (requested and effective) and Gurobi parameters against the mode. |
| `summarize_v4.py` | Metrics (docstring): solved counts, SGM, median per-run time ratios, SCIP time excluding the separator callback, paired bounds, root gap closed, pair-hull reference 0 and closure of the residual gap for the path family, separator funnel with row-binding rejection causes, time decomposition, native SCIP separator activity. Accepts campaign-3 directories, and `DIR=REFDIR` to add campaign-3 runs of the same models as modes `c3:<mode>`. |
| `test_v4.py` | Targeted tests (below). |
| `scanD/scan_d.py` | Part D pool, scan, qualification (`run`, `report`) and the hard-model selection from the screening run (`select`). |

## Code: the two additions (snapshot `integration.py` SHA-256 35b5a4fd928e...)

1. `Config.row_directions: bool = False`, validated as a bool. When True,
   `RowSeparator._directions` runs exactly the `v3d` code (for each source
   side the direction (affine block coefficients of that side, e_j), if
   nonzero, then the frozen remainder-only direction); when False the frozen
   loop runs unchanged.
2. `run_instance(..., scip_params=None)`: `model.setParam(key, value)` for
   every item, after the standard parameters and before the separator is
   included and `optimize` runs, in every mode; recorded as `scip_params`
   in every result (also the not-admitted results). Names that
   `run_instance` sets itself (`limits/time`, `limits/nodes`, `limits/gap`,
   `parallel/maxnthreads`, `randomization/randomseedshift`) are refused.

`snapshot/scip-parameters.json` records, for every parameter used, the value,
SCIP's default and SCIP's description; `snapshot.py` checks each name with
`Model.getParams()`, that the value is not the default, and that
`getParam` returns it after `setParam`.

## Modes as implemented (`v4_worker.mode_config`)

| Mode | run_instance mode | Config overrides | SCIP parameters |
|---|---|---|---|
| baseline | baseline | - | - |
| all, auto | all, auto | - (frozen) | - |
| all-diag | all | max_blocks 128, max_cuts 200, max_cuts_per_round 50, max_rounds 10, max_support_calls 500, max_separation_seconds 30, separation_budget_fraction 0.5 | - |
| all-diag-mech | all | max_blocks n, max_cuts 4n, max_cuts_per_round n, max_rounds 10, max_support_calls 20n, max_separation_seconds 60, separation_budget_fraction 0.5 | - |
| frozen-wide | all | max_blocks n, max_cuts 16n, max_cuts_per_round 4n, max_rounds 10, max_support_calls 40n, max_separation_seconds 60, separation_budget_fraction 0.5 | - |
| rowdir-wide | all | frozen-wide limits + row_directions True | - |
| all-diag-rowdir | all | all-diag limits + row_directions True | - |
| baseline-novarlocks | baseline | - | `constraints/nonlinear/checkvarlocks = 'd'` |
| baseline-extra | baseline | - | `separating/eccuts/freq = 0`, `nlhdlr/quadratic/useintersectioncuts = TRUE`, `separating/interminor/freq = 0`, `separating/rlt/detecthidden = TRUE`, `separating/rlt/hiddenrlt = TRUE` |
| baseline-noaggr, all-noaggr, all-diag-noaggr, all-diag-rowdir-noaggr | as the base mode | as the base mode | base mode's + `presolving/donotaggr = TRUE`, `presolving/donotmultaggr = TRUE` |
| gurobi | - | - | Gurobi 13.0.3: Threads 1, NonConvex 2, MIPGap 1e-4, OutputFlag 0, Seed = job seed, TimeLimit = remaining soft budget |

Notes on baseline-extra (SCIP 10.0.2 names, checked with `getParams()`):
the separators are switched on at the root (`freq 0`, SCIP's own convention
for root-only separators, as RLT by default and as the certified separator).
`separating/rlt/freq` is already 0 by default, so RLT runs without a further
setting; `hiddenrlt` makes RLT (not only McCormick) cuts for hidden products,
as in `verification/R7-editor_native_settings.py`. SCIP counts a separator
call only when it does not return DIDNOTRUN; in all checks so far (path
family, eight Part B models, smoke runs, toy models) `eccuts` never made a
productive call (no edge-concave aggregation found), whereas `interminor`,
RLT and intersection cuts did. Every SCIP record holds
`native_statistics` (separator and nonlinear-handler tables, effective
parameter values, transformed status of every original variable), so the
activity of each native separator is reported per run.

Mode gurobi builds the model from the case JSON (variables with bounds and
types, linear and quadratic row terms, objective with constant; rows with
`nl` are refused), runs Gurobi, and writes a record in the SCIP schema:
status `optimal` (Gurobi OPTIMAL with ObjBound = ObjVal to 1e-9) or
`gaplimit` (other OPTIMAL), `timelimit`, etc.; `primal` = ObjVal, `dual` =
ObjBound, `nodes` = NodeCount, `solver_runtime_seconds` = Runtime,
`gurobi_work`, the incumbent in `original_values`, `cuts` = []. Time is
charged as for SCIP: TimeLimit is the soft budget minus preparation and
model build (milliseconds). The record carries `model_sha256` but no
`original_model`, so the archived replay lists it among the omitted runs
(it has no cuts); `replay_v4.py` checks its parameters.

## Measurements added in the worker (frozen solver code unchanged)

- `row_binding_rejection_causes`: the worker wraps the module-level
  `_audit_inserted_row`; when it rejects a row (return value passed through
  unchanged) the cause is the first failing check, in the audit's order:
  `aliased_transformed_column`, `column_set_differs_variable_not_column`
  (a source variable is aggregated, multi-aggregated, fixed or negated),
  `column_set_differs_tiny_coefficient_dropped` (coefficient below SCIP's
  epsilon 1e-9 not stored), `column_set_differs_other`,
  `coefficient_rounded_to_integer`, `coefficient_differs_other`,
  `lhs_infinite`, `constant_nonfinite`, `bound_differs`,
  `finite_upper_side`, `local_row`. The worker fails the run if the causes do
  not add up to the separator's `row_binding_rejections`.
- `native_statistics`: `build_model` is wrapped so that `run_instance` gets a
  delegating model object whose `freeProb` first reads SCIP's statistics
  (after `run_instance` has computed all its times).

## Rules as implemented (choices the protocol leaves open, fixed before any campaign-4 run)

- **C2** (`partC2`): the 20 campaign-3 instances (regenerated and compared
  with `../v3/runs/partC/cases`). Full: baseline-novarlocks, baseline-extra,
  frozen-wide, gurobi at 300 s soft / 360 s hard; root: the three SCIP modes,
  node limit 1, 120 s / 180 s. 40 jobs, 140 runs. Its baseline and
  all-diag-mech comparisons come from campaign 3 (`summarize_v4.py
  runs/partC2=../v3/runs/partC`).
- **C3** (`partC3`): `mechanism.py` with seeds 5-9 for n in {10, 20, 40, 80}
  (names checked to be new). Full: baseline, all-diag-mech, rowdir-wide,
  baseline-extra, gurobi; root: the four SCIP modes. Limits as C2. 40 jobs,
  180 runs.
- **B2** (`partB2`): the 30 models of the frozen campaign-3 Part B selection
  (checked against `../v3/runs/partB/cases`), root only, node limit 1, 60 s /
  90 s: baseline-noaggr, all-noaggr, all-diag-noaggr, all-diag-rowdir-noaggr,
  baseline-extra. 30 jobs, 150 runs. Campaign-3 root runs of the same models
  are the `c3:` reference.
- **D**: see `scanD/` below. Root (`partD-root`): baseline, all, all-diag,
  all-diag-rowdir, baseline-extra, node limit 1, 120 s / 180 s (100 runs).
  Full (`partD-full`): baseline, all, auto, baseline-extra, seed 0, 300 s /
  360 s (80 runs). Reference bound for the root gap: MINLPLib `primalbound`.
- Path-family parts run larger n first and full before root; seed 0; gap
  limit 1e-4 (frozen Config). Six workers for every part (protocol,
  Execution). Modes of a job run back to back, rotated by (model index +
  seed) mod (number of modes).
- Root bound in the summaries: `root_dual`, or the final dual bound for a
  run that ended at the root without one (SCIP reports no root bound when
  the cuts let it prune the root node).

## Part D pool, scan and selection (`scanD/`, done)

- Pool rule (`scan_d.py`): 120 < nvars <= 1000, `convex == False`,
  `nquadfunc + npolynomfunc >= 1`, OSiL file below 2,000,000 bytes, and not a
  case of campaigns 1-3. "Used in campaigns 1-3" means a case file of
  campaign 1, campaign 2 (with its diagnostic and repair runs), campaign 3
  (Parts A, B, C and the v3d diagnostic) or a name in the frozen campaign-2
  eligible list scanned by campaign-3 Part S. The prior-work exclusion lists
  of campaigns 1 and 2 (`excluded_names`) were not runs of campaigns 1-3 and
  are not excluded; this admits, e.g., `kriging_peaks-full100` and
  `heatexch_gen2`. Pool: 322 models (excluded after the metadata filter:
  btest14 and waterno2_06 as used, 17 files of 2 MB or more).
- Scan (2026-10-03 17:03-17:08 UTC, 307 s, 6 processes, snapshot manifest
  `098bda40...`): 301 admitted, 4 killed at 120 s in `build`, 17 refused;
  discovery completed for all admitted models. Qualifying: 85
  (`scanD/qualifying.json`, `scanD/scan-summary.md`, `scanD/records.jsonl`).
- Screening (`scanD/screen/`, built with `make_jobs.py partD-screen`, run with
  `driver.py`, 6 workers, about 11 min): 85 baseline runs, 60 s, seed 0:
  optimal 16, gaplimit 11 (all 27 pass the primal check), timelimit 58.
  Hard: 58. Records copied to `scanD/screen-records.jsonl`.
- Selection (`scanD/partD-selection.json`), first 20 hard qualifying models
  by SHA-256 of `convexification-hard-v4:` + name: blend480,
  kall_ellipsoids_tc05a, kall_ellipsoids_tc02b, pooling_sppa0stp,
  camshape100, multiplants_mtg1a, ringpack_20_2, mpbp_31, hydroenergy2,
  waternd2, kriging_peaks-full100, multiplants_mtg1c, blend718,
  kall_circlesrectangles_c6r1, pooling_sppa0pq, kall_circlespolygons_c1p5b,
  sonet23v4, ringpack_20_1, crudeoil_li03, multiplants_mtg6. All 20 hit the
  60 s limit in screening.
- Expected consequence of the frozen limits: in modes `all` and `auto` the
  separation budget is min(1 s, 5% of the limit) = 1 s, which includes lazy
  discovery. In the scan, discovery took more than 1 s on 12 of the 20
  selected models (up to 7.7 s), so on those models `all`/`auto` will most
  likely stop in discovery and add no cuts (the smoke run shows this at its
  0.5 s budget). That is the frozen behaviour; all-diag (30 s) is not affected.

## Commands

```bash
V4=/workspace/minlp-notes/paper-certified-support-cuts/experiments/v4
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cd $V4
```

(i) Snapshot: exists (86 files, manifest `098bda4033b5...`); the scan, the
screening and the smoke runs used it. Do not recreate it.

(ii) Build the job lists (each copies the verified snapshot):

```bash
$PY make_jobs.py partC2 --output runs/partC2
$PY make_jobs.py partC3 --output runs/partC3
$PY make_jobs.py partB2 --output runs/partB2
$PY make_jobs.py partD-root --selection scanD/partD-selection.json --output runs/partD-root
$PY make_jobs.py partD-full --selection scanD/partD-selection.json --output runs/partD-full
```

(iii) Launch. One chain, at most six workers:

```bash
nohup bash -c "$PY driver.py runs/partC3 --workers 6 && \
               $PY driver.py runs/partC2 --workers 6 && \
               $PY driver.py runs/partB2 --workers 6 && \
               $PY driver.py runs/partD-root --workers 6 && \
               $PY driver.py runs/partD-full --workers 6" > runs/launch-v4.log 2>&1 &
# Resume after a stop or crash: rerun the same command (finished runs are skipped).
# Progress: tail -f runs/launch-v4.log; wc -l runs/*/records.jsonl
```

The drivers may also be started at the same time (separate `nohup` lines);
the six slots in `v4/.slots` keep the total at six workers.

(iv) Replay (exit 0 only if passed; writes `runs/<part>/replay.json`):

```bash
for p in partC2 partC3 partB2 partD-root partD-full; do $PY replay_v4.py runs/$p > runs/replay-$p.log; done
```

(v) Summaries (after the replay):

```bash
$PY summarize_v4.py runs/partC2=../v3/runs/partC runs/partC3 runs/partB2=../v3/runs/partB \
    runs/partD-root runs/partD-full scanD/screen --dest .
# Funnel and time decomposition of the campaign-3 cut modes (no rejection causes recorded there):
$PY summarize_v4.py ../v3/runs/partA-full ../v3/runs/partA-root ../v3/runs/partB ../v3/runs/partC \
    ../v3d/runs/partA-root-rowdir ../v3d/runs/partB-root-rowdir ../v3d/runs/partC-rowdir --dest campaign3-funnel
```

Targeted tests: `$PY -m unittest test_v4` (11 tests, about 75 s).

## Wall-time estimate (6 workers)

Based on campaign-3 Part C and Part B, the v3d diagnostic, the Part D
screening (all 20 selected models hit 60 s) and the smoke runs. The upper
bounds assume that every run reaches its hard limit.

| Launch | Expected | Upper bound |
|---|---|---|
| C3 | 55-65 min. In campaign 3, baseline and all-diag-mech reached 300 s on every n >= 40 instance and on some n = 20; baseline-extra and gurobi are assumed similar; rowdir-wide took at most 42 s (v3d). Ten n >= 40 full jobs take about 4 x 300 s + 40 s each. | (100 x 360 + 80 x 180) s / 6 = 2.3 h |
| C2 | 50-60 min (three SCIP modes and gurobi mostly at 300 s for n >= 40; frozen-wide root up to the 60 s separation budget). | (80 x 360 + 60 x 180) s / 6 = 1.8 h |
| B2 | 2-4 min (campaign-3 Part B root runs took 1-7 s). | 150 x 90 s / 6 = 38 min |
| D root | 30-45 min (the root of these models often does not finish in 120 s; all-diag uses up to 30 s of separation). | 100 x 180 s / 6 = 50 min |
| D full | 70-80 min (nearly every run is expected to reach 300 s; 20 jobs of about 1200 s on 6 workers). | 80 x 360 s / 6 = 80 min |
| Replay | about 20-30 min in total (path family about 10 ms per cut, up to about 30 000 cuts in C3; Part D about 0.1 s per cut, up to about 8 000 cuts in D root). | |

Expected total about 3.5-4 h run in sequence (about 3.2 h of work if the
drivers run concurrently); upper bound about 6.7 h.

## Verification done (targeted; no project-wide tests, no CI)

- `python -m unittest test_v4`: 11 tests passed. They check the mode table
  and the recorded SCIP parameters; that `Config` accepts only a bool for
  `row_directions` and that every other default equals the campaign-3
  value; that `scip_params` is applied, recorded and refuses reserved or
  unknown names; that the snapshot `integration.py` equals the campaign-3
  file with exactly the `PATCHES` applied; the fresh C3 instances (exact
  optimum, witness passes the primal check with zero violation, names new)
  and that C2/B2 cases equal campaign 3; job counts, rotation and limits;
  **same cuts as campaign 3 with defaults**: campaign-3 snapshot versus
  campaign-4 snapshot, each in its own process, root, 60 s, on ex4_1_8 and
  cvxnonsep_normcon20r (mode all) and interleaved_path_n10_s0
  (all-diag-mech), identical cut records, root bounds and support-call
  counts, with and without an explicit `row_directions=False`;
  **rowdir-wide reproduces v3d**: interleaved_path_n20_s4, root, gives the
  root bound 0.04833984375003908 and the 320 cut normals of the v3d record
  `all-diag-mech-wide` exactly, and frozen-wide gives a lower bound; mode
  gurobi reaches the known optimum of interleaved_path_n10_s0 (60 s) and its
  incumbent passes the primal check.

### Smoke runs (`smoke/`, 10 s soft / 30 s hard; not used in the paper)

All six parts were built with `make_jobs.py PART --smoke` against the final
snapshot and run together (6 slots, 64 s wall). All 46 runs completed (no
failures). Replay passed in every part, with no Config, SCIP-parameter or
Gurobi-parameter mismatches; every tampering mutation was rejected in every
cut mode. Summary: `smoke/results.md`.

| Part | Cases | Runs | Statuses | Cuts replayed | Tamper modes |
|---|---|---:|---|---:|---|
| C2 | interleaved_path_n10_s0 | 7 | optimal 3, nodelimit 3, timelimit 1 (gurobi) | 320/320 | frozen-wide |
| C3 | interleaved_path_n10_s5 (fresh) | 9 | optimal 5, nodelimit 3, gaplimit 1 | 400/400 | all-diag-mech, rowdir-wide |
| B2 | pooling_bental4tp, wastewater04m2 | 10 | nodelimit 9, optimal 1 | 56/56 | all-noaggr, all-diag-noaggr, all-diag-rowdir-noaggr |
| D screen | blend480, crudeoil_pooling_ct4 | 2 | timelimit 2 | 0 | - |
| D root | blend480, kall_ellipsoids_tc05a | 10 | timelimit 10 | 297/297 | all-diag, all-diag-rowdir |
| D full | blend480, kall_ellipsoids_tc05a | 8 | timelimit 8 | 0 | - |

Root bounds of the path instances (optimum; gap closed versus the baseline
in parentheses; closure of the residual gap root/opt in brackets; the
pair-hull bound is 0):

| Instance | Optimum | Baseline | baseline-novarlocks | baseline-extra | all-diag-mech | frozen-wide | rowdir-wide |
|---|---:|---:|---:|---:|---:|---:|---:|
| n10_s0 (C2; baseline and all-diag-mech from campaign 3) | 0.0498047 | -0.249230 [-5.0] | -0.001257 (0.829) [-0.025] | -0.088639 (0.537) [-1.78] | -0.120093 (0.432) [-2.41] | 0.000381 (0.835) [0.008] | - |
| n10_s5 (C3) | 0.0191650 | -0.242435 [-12.6] | - | -0.092692 (0.572) [-4.84] | -0.148933 (0.357) [-7.77] | - | 0.0191649 (1.0) [1.0], solved at the root |

Full runs at 10 s: n10_s0 gurobi reached the time limit (bound 0.049727,
about 61 000 nodes); all SCIP modes solved it in 1-3 s. n10_s5: all modes
solved it; gurobi 0.34 s. Row-binding rejection causes seen: path family
`column_set_differs_tiny_coefficient_dropped` (3-6 per run); B2 (no
aggregation) `coefficient_rounded_to_integer`; Part D
`column_set_differs_variable_not_column` (15 on blend480, which has fixed,
aggregated and multi-aggregated variables). Native separators in
baseline-extra: intersection cuts on every model, interminor on
wastewater04m2, blend480 and kall_ellipsoids_tc05a, eccuts none.
