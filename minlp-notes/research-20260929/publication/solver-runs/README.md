# Finished solver campaign and publication analysis

The final campaign (driver PID 898862) ended 2026-10-03T13:33:28Z:
**129 outcomes, 126 passing time measurements, three SCIP memory-cap stops**.
The analysis is complete. No new solver runs are authorized for this task.

Start with [report.md](report.md) and the paper table
[results_table.md](results_table.md) / [results_table.csv](results_table.csv).
Accepted closures: BARON 0, GUROBI 0, SCIP 0. BARON's two raw optimality
claims are contradicted by the certificates. All 37 instances outside the
six exactly infeasible kan models remain unclosed by all three in this
campaign; the kan certificates apply to the network relaxation R.
There are 109 finite dual values, including six BARON values without a
globality guarantee; the other 103 split BARON 29, GUROBI 36 and SCIP 38.
Six SCIP values concern slightly tightened models. Ten rows disclose the
first batch's machine overload and memory pressure; all ten passed the
measurement rule. The report includes the response to the solver-analysis
review and high-precision checks of three GUROBI waterno2 improvements.

## Reproduce the analysis without solving

From this directory:

```sh
python3 collect.py --help > analysis-collect-help.txt
python3 collect.py > collect.log
python3 collect.py --runs runs_archive/attempts --out attempts > collect-attempts.log
PYTHONDONTWRITEBYTECODE=1 python3 build_references.py
PYTHONDONTWRITEBYTECODE=1 python3 check_points.py > point_checks.log
PYTHONDONTWRITEBYTECODE=1 python3 analyze.py > analyze.log
PYTHONDONTWRITEBYTECODE=1 python3 verify_analysis.py > verification.log
```

Use `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1` and
`taskset -c 0,1` to reproduce this revision's two-core limit; the exact
commands and results are in report.md. Python needs mpmath. `check_points.py` also needs the campaign GDX savepoints,
`gdxdump` on PATH, the cached OSIL files in
`~/.cache/minlplib/minlplib/osil/`, and the existing read-only evaluator in
`../../bound-audit/audit_eval.py`. It checks 18 selected points sequentially;
none of these commands launches a solver. Source files and hashes are
recorded in `references.*` and `reference_sources.json`.

## Files

| File / directory | Purpose |
|---|---|
| `report.md` | Final protocol, results, inconsistencies, review responses, commands and limits |
| `results_table.md`, `.csv` | 129 paper rows; CSV preserves source decimal tokens and full comparisons |
| `results.csv`, `.json` | Collector output for kept outcomes only |
| `references.csv`, `.json` | 43 certificate/primal/listed references, exact/numerical status and sources |
| `reference_sources.json` | SHA256 of local reference sources |
| `inconsistencies.md`, `.csv`, `.json` | Every returned/log primal beyond a certificate; printing and scope caveats |
| `analysis_summary.json`, `analyze.log` | Counts and campaign comparison summary |
| `point_checks.json`, `.log` | Selected GDX-point feasibility evaluations at 50 digits |
| `verification.log` | Targeted artifact checks; no project-wide or CI checks |
| `build_references.py`, `check_points.py`, `analyze.py`, `verify_analysis.py` | Reproducible analysis and targeted validation |
| `collect.py` | Collector including reproducible solver-warning and first-batch flags; usage `--runs DIR --out PREFIX` |
| `review_r1_check.py`, `review_r1_evidence.json`, `.log` | Targeted recheck of the independent review's evidence and numerical agreement |
| `attempts.csv`, `.json` | Nine archived memory-cap attempts; do not add kept copies twice |
| `PROGRESS.json` | Completed work, remaining limits and background-job state |
| `instances.txt`, `gms_manifest.csv`, `.json`, `check_gms.py`, `download.log` | Models, hashes/counts, and download provenance |
| `gms/` | Original MINLPLib GAMS models (gitignored) |
| `runs/<instance>__<solver>/` | `cmd.txt`, `run.json`, `gams.log`, trace, listing, stdout and optional GDX point |
| `driver.py`, `driver.log`, `progress.txt`, `machine_load.csv`, `driver.out`, `driver.pid` | Historical driver and final campaign evidence |
| `runs_archive/driver1/` | Rejected first launch; excluded from final results |
| `runs_archive/driver2_launch1_stopped/` | Abandoned relaunch; excluded from final results |
| `runs_archive/attempts/` | Nine invalid memory-cap attempts, including the three kept copies |
| `smoke/`, `smoke2/` | Historical smoke, interruption, admission and restart tests |
| `report.prev.md`, `report.running.md` | First-launch and relaunch reports with previous authors' command records |

Bulky listings and the largest GDX savepoints are gitignored. A savepoint
can exist without a usable returned primal; use model status, not file
presence, to decide whether an objective is a primal value.

## Historical production protocol

Versions: GAMS 54.3.1, BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3.
Models were unmodified. Each job used:

```sh
cd runs/<instance>__<solver>
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  gams <absolute-path>/gms/<instance>.gms <TYPE>=<SOLVER> \
  reslim=3600 threads=1 optcr=1e-9 optca=1e-9 lo=2 \
  logfile=gams.log o=<instance>.lst savepoint=1 trace=trace.trc traceopt=3
```

There are 29 NLP and 14 MINLP jobs per solver. pricing050 maximizes;
all others minimize. No option files were used. GUROBI/SCIP limits are wall
clock; BARON with one thread limits CPU time. Wall/CPU/solver time remain
separate columns. The historical shared machine had 18 cores / 36 threads;
these measurements are not isolated-core benchmarks.

The final driver used at most 10 simultaneous jobs, admitting starts only
at load1 ≤ 30 and MemAvailable ≥ 8 GB. It capped each group's RSS+swap at
8192 MiB, applied a 4200 s hard wall timeout, interrupted the busiest solver
process with SIGINT, and escalated to group SIGTERM after 300 s then SIGKILL
after another 30 s. Graceful return of a bound/trace/savepoint is possible,
not guaranteed. All kept final outcomes did return trace records; only the
three memory stops were driver-interrupted, without escalation.

Measurement validity requires own completion or hard timeout and CPU/wall
≥ 0.9; own completions under 60 s before resource interruption are exempt.
CPU uses the maximum of wait4 and sampled whole-group /proc accounting.
Invalid attempts are archived and retried twice. After three attempts,
the driver keeps the attempt ranked by proper end, trace presence and
CPU/wall, not by objective quality. “Valid” is a measurement flag, not a
mathematical guarantee. The three SCIP rows are explicitly **stopped at
the 8 GB memory limit**, using the final bound of the kept attempt.

The historical launch command was:

```sh
setsid nohup python3 driver.py >> driver.out 2>&1 < /dev/null &
```

This is a reproduction record, not an instruction to rerun this campaign.
The obsolete launch estimates, machine-memory-floor rule and blanket
SIGINT guarantee in the old README are superseded by this final record.

## Bound and primal sources

The collector takes the final dual from GAMS `objest` when available,
otherwise the end-of-run solver summary. GUROBI's summary has only 13
significant digits; printing half-units are retained. Progress-table
bounds are kept separately and are not used as final duals. Bounds after
solver failures are excluded. Sentinel magnitudes ≥ 1e20 become infinities.
GUROBI/etamac reports no final bound (`-`), so no finite value is inferred.

GAMS's returned objective and the log incumbent may differ. Both are
compared in the CSV, but GDX checks test the GAMS-returned point. All
reported primals are floating-point claims; positive high-precision row
residuals establish numerical evidence of infeasibility, not exact
repairs. BARON rejects sin/cos on lnts50/100/200/400 and powerflow0030p/0039p,
cos only on hvycrash, and tanh on ann_cumene_tanh. See the final report for the
GUROBI/lukvle10 POW failure, and the distinction from the known SCIP bug.
