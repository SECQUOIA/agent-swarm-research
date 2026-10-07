<!-- Written to disk by the root from the structured return value of agent 'author:solver-campaign' (the harness blocks subagents from writing report files). Status: complete. -->

The 129-run campaign is launched and the smoke test passed. One file is missing: the harness refused to let a subagent write report.md, so the report is in this summary and README.md is the written record.

**Campaign.** 43 instances x BARON 26.5.27, GUROBI 13.0.2 (build v13.0.2rc1) and SCIP 10.0.3 (d409edf9f6), all through GAMS 54.3.1 (61154be4). It runs as one detached driver, PID 143593, started 2026-10-02 03:15:35 UTC. The first 10 runs were alive at 03:23 UTC; none had finished yet, so results.csv and results.json for the campaign do not exist yet.
- Each run: `<TYPE>=<SOLVER> reslim=3600 threads=1 optcr=1e-9 optca=1e-9 lo=2 logfile=gams.log o=<inst>.lst savepoint=1 trace=trace.trc traceopt=3`.
- TYPE is the model type the .gms declares: NLP for 29 instances, MINLP for 14. Only pricing050 maximizes.
- No option files. OMP_NUM_THREADS, MKL_NUM_THREADS and OPENBLAS_NUM_THREADS are set to 1.
- Each run has its own folder `runs/<inst>__<solver>/` with cmd.txt, gams.log, the .lst, trace.trc, m_p.gdx and run.json.
- The queue runs the largest models first.
- Expected end is about 16:30 UTC on 2026-10-02 (13 rounds of about one hour). The worst case, every run hitting the hard timeout, is about 19:00 UTC.

**Driver.** At most 10 runs at once. Hard timeout at reslim + 600 = 4200 s wall. A run is also interrupted if its memory exceeds 8 GB, or if the machine's free memory drops below 3 GB (our largest run above 1 GB, at most one per 60 s).
- An interrupt sends SIGINT to the run's process group; all three solvers then stop with solver status 8 and still report the final bound, trace and savepoint. SIGTERM follows after 120 s and SIGKILL 30 s later if needed.
- Restart skips finished runs and reruns unfinished ones from scratch.
- `progress.txt` is rewritten every 30 s, `driver.log` records events, and `machine_load.csv` records load and memory every 60 s.

**collect.py.** Writes one row per run to results.csv and results.json: instance, solver, versions, status codes and texts, primal objective, dual bound with its source, raw objest, final and last-logged log bounds, wall/GAMS/solver/CPU time, nodes, thread confirmation with evidence, memory, savepoint flag, model-count check, settings and notes. It also works on a partial campaign.
- The dual bound is objest when present, else the solver's final summary in the log: BARON "Best possible", GUROBI "Best objective ..., best bound ...", SCIP "Dual Bound". These are final global bounds, not root relaxation values.
- When both exist they must agree to 1e-10 relative, otherwise the row gets a note.
- A bound counts only after solver status 1, 2, 3, 4 or 8.
- Values of 1e20 or larger are written as inf.

**Downloads and gms/OSIL check.** All 43 .gms files downloaded one at a time with a 1 s delay, all HTTP 200; sha256 values are in gms_manifest.csv. The header counts in each .gms were compared with counts computed from the cached OSIL (objvar elimination taken into account). 42 of 43 match on every count.
- The exception is pricing050: its .gms header states 295 nonlinear nonzeros, while the OSIL implies 249.
- GAMS 54.3 itself generates pricing050 with 296 nonzeros and 249 nonlinear nonzeros, so the model matches the OSIL; only the header comment is off.
- All 18 smoke runs' GAMS-generated counts match the OSIL.

**Smoke test (18 runs, 30 s each).** Instances: ex6_2_5, chain50, plus pricing050 (the maximization case), waterno2_06 (MINLP), optcdeg2 (largest) and ann_cumene_tanh (tanh).
- Options took effect: every log echoes the GAMS settings; GUROBI says "using up to 1 threads" and SCIP sets lp/threads = 1. BARON prints no thread line, but its CPU/wall ratio was 0.95-1.00, apart from one run at 0.66 that spent 15 s in GAMS startup. All 18 rows are marked threads confirmed.
- Wherever objest and the log bound both exist, they agree.
- GUROBI leaves objest NA for chain50, ex6_2_5 and optcdeg2, so the log bound is needed there.
- No dual bound is on the wrong side of the primal value, including the max case.
- Savepoints were written whenever a point was returned; GAMS writes none for "no solution" outcomes.
- BARON and SCIP reject tanh and stop with status 6 (capability problems).
- BARON failed on optcdeg2 with "Insufficient memory for data structures" at about 1 GB (status 12/10). Its objest of 1.39998598654172 was therefore not used as a bound. In the full run it was still going after 7 minutes.
- Tests of the timeout guard, the memory guard, skip-on-restart and stop/restart all behaved as intended, with no leftover processes.

**Early observation (not analysis).** In the 30 s runs, BARON and SCIP returned pricing050 values above our verified upper bound −1813.8290784519730577, by 4.6e-7 and 2.8e-7. For chain50, BARON's value was 2.6e-9 below our certified bound 5.0722614939828627 and SCIP's 1.9e-12 below. Those points therefore meet the constraints only within solver tolerances, so the savepoints must be checked for exact feasibility before any solver primal value is used.

## Commands run (from the agent's structured return)

- `for n in $(cat instances.txt); do curl -sS -o gms/$n.gms https://www.minlplib.org/gms/$n.gms; sleep 1; done -> 43x HTTP 200`
- `python3 check_gms.py (twice) -> 42/43 match, pricing050 header NL count 295 vs 249`
- `gams gms/pricing050.gms NLP=SCIP reslim=1 threads=1 lo=2 trace=trace.trc traceopt=3 (smoke/manual/pricing_counts) -> generated 296 nz, 249 NL nz`
- `gams gms/ex6_2_5.gms NLP={BARON,GUROBI,SCIP} reslim=30 threads=1 optcr=1e-9 optca=1e-9 lo=2 logfile=gams.log savepoint=1 trace=trace.trc traceopt=3 (smoke/manual/<S>) -> format exploration; GUROBI objest NA`
- `python3 smoke/manual/sigtest.py <gams> gms/ex6_2_5.gms {SCIP,GUROBI,BARON} sig_<S> -> SIGINT gives graceful stop, solver status 8, bound and savepoint kept`
- `text search of GAMS docs S_BARON.html, S_GUROBI.html, S_SCIP.html for threads, time and memory semantics`
- `python3 -m pyflakes; ruff check --select E,F,W --line-length 120 driver.py collect.py check_gms.py -> clean`
- `python3 driver.py --out smoke --reslim 30 --jobs 10 --instances ex6_2_5 chain50 pricing050 waterno2_06 optcdeg2 ann_cumene_tanh -> 18/18 finished`
- `python3 collect.py --runs smoke/runs --out smoke/results (3x, after parser fixes) -> 18 rows`
- `python3 driver.py --out smoke/guard_timeout --reslim 60 --hard-extra-s -50 --instances ex6_2_5 --solvers SCIP -> SIGINT at 10 s, status 8, bound kept`
- `python3 driver.py --out smoke/guard_memory --reslim 60 --mem-cap-gb 0.1 --instances ex6_2_5 --solvers SCIP -> SIGINT at 5 s, status 8, bound kept`
- `rerun of the smoke driver command -> 18 skipped`
- `setsid python3 driver.py --out smoke/restart_test --reslim 40 --instances ex6_2_5 --solvers SCIP GUROBI; kill -TERM <pid> -> runs killed, finished=false, no orphans; python3 driver.py --out smoke/restart_test --reslim 5 ... -> both rerun`
- `6 trivial GAMS jobs in /tmp/gamsov (deleted) -> process overhead 0.29-0.51 s`
- `cd solver-runs && setsid nohup python3 driver.py > driver.out 2>&1 < /dev/null & -> campaign launched, driver PID 143593`
- `python3 collect.py --runs runs --out /tmp/partial_results (deleted) -> parsed 10 in-progress runs without error`
- `per-process CPU-share sampling over 30 s at 03:22 UTC -> our solver processes got 0.53-0.75 CPU each`

## Open issues (from the agent's structured return)

- Machine oversubscription (main issue): within 5 minutes of launch the load average rose from 21 to 164-194 on 36 logical CPUs (18 physical cores), from other agents' SCIP compiles and Python checks. Measured at 03:22 UTC, our 10 solver processes got 0.53-0.75 of a CPU each. If this persists, GUROBI and SCIP (wall-clock limits) get only about 2,000-2,700 CPU-seconds. BARON (CPU-time limit with one thread) will likely hit the required 4,200 s wall hard timeout first and be interrupted gracefully at roughly 2,200-3,200 CPU-seconds. Each run records cpu_time_s, cpu_over_wall and load, and machine_load.csv logs the load every minute. The analysis step should rerun affected runs on a quiet machine (driver.py --out rerun ...).
- report.md was not written because the harness refuses report files from subagents; the report content is in this result's summary.
- collect.py has not yet parsed a full-length (3600 s) run; the code paths are the same as in the 30 s smoke runs. Spot-check a few rows against the logs after the batch ends.
- GAMS/Gurobi leaves objest NA for some NLP models (chain50, ex6_2_5, optcdeg2). For those, the dual bound comes from Gurobi's final 'best bound' line, printed with 13 significant digits.
- BARON and SCIP do not support tanh, so ann_cumene_tanh will give status 6 (capability problems) for both. BARON failed on optcdeg2 at 30 s with 'Insufficient memory for data structures' (status 12/10); the full-length run was still going after 7 minutes.
- No savepoint is written when a solver returns no point. Returned points must be checked for exact feasibility: smoke values for pricing050 and chain50 already violate our verified bounds by 1.9e-12 to 4.6e-7, so those points are only tolerance-feasible.
- GAMS start or exit took 6-15 s in 2 of the 22 driver test runs (normally 0.3 s). This counts in wall_time_s but not in gams_elapsed_s or solver_time_s.
- The memory guard (8 GB per run, 3 GB machine floor) is an experimental condition enforced by the driver, not a solver option. Any interruption it causes is recorded in kill_reason.

## Background jobs at return time

- Driver PID 143593 (process group 143593, own session), started 2026-10-02T03:15:35Z. Command: cd /workspace/minlp-notes/research-20260929/publication/solver-runs && setsid nohup python3 driver.py > driver.out 2>&1 < /dev/null &. Log: /workspace/minlp-notes/research-20260929/publication/solver-runs/driver.log (stdout/stderr in driver.out). Progress: cat /workspace/minlp-notes/research-20260929/publication/solver-runs/progress.txt; liveness: ps -p 143593 -o pid,etime,cmd. Machine load: machine_load.csv. Expected end about 16:30 UTC 2026-10-02, worst case about 19:00 UTC. Then run: python3 collect.py (writes results.csv and results.json). Stop: kill -TERM 143593 (active runs are killed and stay unfinished); restart with the same command.
