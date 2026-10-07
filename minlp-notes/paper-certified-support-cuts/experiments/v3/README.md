# Campaign v3 runner

Implements `../campaign-v3-protocol.md` (Parts A and B) and
`../mechanism-protocol.md` (Part C). The Part S scan and the Part B selection
are produced separately by `scan/scan.py`. Nothing here modifies
`research-2026100*-convexification/` or `literature/`.

## Files

| File | Role |
|---|---|
| `snapshot.py` | Copies the live sources into `snapshot/` and writes `snapshot/source-manifest.json` (SHA-256 per file). It refuses to overwrite an existing snapshot and checks that `solver/integration.py` starts with `128fe10b`. |
| `make_jobs.py` | Creates one output directory per launch: `cases/`, a hash-verified copy of the snapshot with `frozen-cases/` and `original-osil/`, `source-manifest.json`, `jobs.json` and `build.json`. This is the campaign-v2 layout, so the archived replay runs on it unchanged. The output directory must not exist. |
| `mechanism.py` | Generates the 20 interleaved path instances, with exact optimum and witness. |
| `v3_worker.py` | The archived worker, adapted to map `all-diag` and `all-diag-mech` to `run_instance(mode='all', config=Config(...))` and to record `solver_mode`, `config_overrides` and the effective `config`. The run fails if any solver, checker or case module was imported from outside the snapshot. |
| `driver.py` | Parallel, resumable driver (described below). |
| `replay_v3.py` | Runs the archived `replay_campaign` from the output directory's snapshot copy, plus the v3 checks. Writes `replay.json`. |
| `summarize_v3.py` | Computes the protocol metrics and writes `results.md` and `summary.json`. |
| `test_v3.py` | Targeted unit tests (instance exactness, mode configurations, job counts and rotation). |

## Rules as implemented

- **Part A full** (`partA-full`): the 30 `selected` models of the frozen
  `holdout-selection.json`, in its hash order. Seeds 0, 1, 2; modes
  baseline/all/auto; 300 s soft budget and 360 s hard limit. 90 jobs, 270 runs.
- **Part A root** (`partA-root`): node limit 1, 60 s soft, 90 s hard, seed 0;
  modes baseline/all/auto/all-diag. 30 jobs, 120 runs.
- **Part B** (`partB`): the `selected` list of `scan/partB-selection.json`.
  The builder checks that the names are in the Part S pool, in
  structure-hash rank order, at most 30, and equal to the first 30 of
  `qualifying_names_in_rank_order`, and that each `osil_sha256` matches.
  Full runs use seeds 0 and 1 at 300/360 s; root runs are as in Part A.
  Reference bounds come from the snapshot copy of `instancedata.csv`.
- **Part C** (`partC`): 20 instances, n in {10, 20, 40, 80} and seeds 0-4,
  in modes baseline and `all-diag-mech`. Root runs use node limit 1 and
  120 s; full runs use 300 s with the default gap limit 1e-4. All runs use
  seed 0. 40 jobs, 80 runs, at most 4 workers (the mechanism protocol).
- **`all-diag`**: max_blocks 128, max_cuts 200, max_cuts_per_round 50,
  max_rounds 10, max_support_calls 500, max_separation_seconds 30,
  separation_budget_fraction 0.5.
- **`all-diag-mech`**: max_blocks n, max_cuts 4n, max_cuts_per_round n,
  max_rounds 10, max_support_calls 20n, max_separation_seconds 60,
  separation_budget_fraction 0.5. All other Config fields keep the frozen
  defaults.
- **Jobs**: one job is one (model, phase, seed). Within a job the modes run
  sequentially, each in a fresh process, in the order rotated by
  (model index + seed) mod (number of modes).
- **Choices the protocols leave open** (fixed here before any v3 run):
  - Part C hard limits are 180 s for root runs and 360 s for full runs.
  - Part C runs larger n first within each phase, and full runs before root
    runs, to shorten the makespan. Parts A and B run in declared order, seed
    by seed.
  - Mechanism RNG call sequence (see the `mechanism.py` docstring):
    `rng.sample(range(49), 4)`, then one `rng.random() < 0.5` draw each for
    the A/C swap, the orientation of A and the orientation of C.
  - Variable order is x_i, y_i, z_i, t_i.
  - The constant a1^2 + c1^2 of D_i is moved to the row's right-hand side.
  - The known optimum is stored both exactly (`known_optimum_exact`) and as
    binary64, which is exact. The witness is exact and passes the archived
    primal check with zero violation.

## Driver behaviour

- Uses at most W concurrent worker processes. W is capped by `jobs.json`
  (6, or 4 for Part C). Each job also holds one of six machine-wide `flock`
  slots in `.slots/`, so drivers running at the same time together never
  exceed six workers.
- Every worker is single-threaded (OMP, OpenBLAS, MKL, NumExpr, BLIS and
  vecLib set to 1; SCIP `parallel/maxnthreads` 1). Each worker runs in its own
  session. The hard limit is `subprocess` timeout followed by SIGKILL of that
  worker's process group only.
- Each run records the host load average at its start and end, the number of
  this driver's active runs, its attempt number and timestamps. Its result is
  written once to `runs/<run_id>.json` (no overwrite) and appended to
  `records.jsonl`. Worker errors, timeouts and unparsable outputs become
  records. Logs are kept in `attempts/`.
- Resumable: rerunning the same command skips runs whose result file exists
  and reconciles the ledger. An interrupted run is retried as attempt k+1,
  and earlier logs are kept. Stop with `kill -TERM <pid>` or Ctrl-C, not
  SIGKILL: the driver then kills only its own worker groups and records
  nothing for the interrupted runs. The pid is in `sessions.jsonl`, which
  logs every start and stop or end. A per-directory lock prevents two drivers
  from running on the same directory.

## Commands

```bash
V3=/workspace/minlp-notes/paper-certified-support-cuts/experiments/v3
PY=/workspace/minlp-notes/code/minlp_solver_lab/.venv/bin/python
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $V3
```

(i) Snapshot. It already exists (created 2026-10-03T06:29Z, 73 files,
integration.py 128fe10b13d2...), and the smoke test ran against it. Recreate
it only if a source changes before any output directory is built:

```bash
$PY snapshot.py                 # refuses if snapshot/ exists; rm -rf snapshot first to redo
```

(ii) Build job lists. Each command copies the verified snapshot into its
output directory:

```bash
$PY make_jobs.py partA-full --output runs/partA-full
$PY make_jobs.py partA-root --output runs/partA-root
$PY make_jobs.py partC      --output runs/partC
# after the scan has written scan/partB-selection.json:
$PY make_jobs.py partB --selection scan/partB-selection.json --output runs/partB
```

(iii) Launch. Run the drivers one after another, so that at most six workers
run at a time. The global slots enforce this limit even if two drivers
overlap.

```bash
nohup bash -c "$PY driver.py runs/partA-full --workers 6 && \
               $PY driver.py runs/partA-root --workers 6 && \
               $PY driver.py runs/partC --workers 4" > runs/launch-A-C.log 2>&1 &
# Part B, after the scan and make_jobs partB:
nohup $PY driver.py runs/partB --workers 6 > runs/launch-B.log 2>&1 &
# Resume after a stop or crash: rerun the same driver command.
# Progress: tail -f runs/launch-A-C.log; wc -l runs/*/records.jsonl
```

(iv) Replay. Each command writes `runs/<part>/replay.json` and exits 0 only
if the replay passed:

```bash
for p in partA-full partA-root partC partB; do $PY replay_v3.py runs/$p; done
```

(v) Summarize. This writes `results.md` and `summary.json` in `$V3`; run it
after the replay so that replay results are included:

```bash
$PY summarize_v3.py runs/partA-full runs/partA-root runs/partC runs/partB --dest .
```

Targeted tests: `$PY -m unittest test_v3`.

## Wall-time estimate (W = 6; Part C W = 4)

These estimates are based on campaign v2 (30 s budget) and on single n=80 Part C
measurements. The upper bounds assume that every run reaches its hard limit.

| Launch | Expected | Upper bound |
|---|---|---|
| Part A full | 50-70 min. In v2, 5 of the 30 models (ex5_2_5, ex8_3_4, graphpart_clique-40, tln7, waterx) reached the time limit in every mode. That gives 15 jobs of about 3 x 300 s; the other runs take under 10 s each. | 270 x 360 s / 6 = 4.5 h |
| Part A root | 5-10 min. all-diag stops at 30 s of separation. | 120 x 90 s / 6 = 30 min |
| Part C | 10-20 min. An n=80 root run took 3 s in baseline and 12 s in all-diag-mech; the n=10 full runs took 2-3 s. | (40 x 360 + 40 x 180) s / 4 = 1.5 h |
| Part B | Unknown before the scan; about 1-2 h if a third of the models time out. | (180 x 360 + 120 x 90) s / 6 = 3.5 h |
| Replay | Minutes per part, at about 10-80 ms per cut. Part A root and Part C have at most about 6000 cuts each. | |

Expected total: about 2-3.5 h, run sequentially.

## Smoke test (`smoke/`, not used in the paper)

`make_jobs.py smoke` uses two v2 holdout models, cvxnonsep_normcon20r and
ex4_1_8:

- full runs at 5 s soft and 20 s hard, seeds 0 and 1, baseline/all/auto;
- root runs at 5 s, baseline/all/auto/all-diag.

It also uses two mechanism instances with n=10 (seeds 0 and 1) at the Part C
limits. Altogether: 10 jobs and 28 runs, run with W=4 in 14 s
(`smoke/run/`, `smoke/driver.log`). All 28 runs completed. Replay passed:
426 of 426 recorded cuts were replayed, with no configuration mismatches.
All 14 tampering mutations were rejected in each cut mode (all, all-diag,
all-diag-mech). Results are in `smoke/results.md`.

| Instance | Optimum | Root dual baseline | Root dual all-diag-mech (cuts) | Root gap closed | Full nodes baseline / mech |
|---|---:|---:|---:|---:|---:|
| interleaved_path_n10_s0 | 51/1024 = 0.0498047 | -0.249230 | -0.120093 (40) | 0.432 | 2562 / 661 |
| interleaved_path_n10_s1 | 43/4096 = 0.0104980 | -0.252259 | -0.177547 (40) | 0.284 | 902 / 324 |

The failure paths were also exercised on scratch copies outside the
repository:

- forced hard-limit kills, recorded as `process_timeout`;
- a forced worker error, recorded as `worker_error`;
- a SIGTERM stop, followed by a resume that ran only the remaining runs, as
  attempt 1 with the attempt-0 logs kept.

Replay handled the failed runs as omitted runs without cuts.
