<!-- Written to disk by the root from the structured return value of author of track solver-campaign in workflow wf_2951b32d-9f3 (the harness blocks subagents from writing report files). -->

# Solver campaign: fix and relaunch after review round 1

## Summary

The campaign is fixed, tested, relaunched and running. It runs 43 instances with BARON 26.5.27, GUROBI 13.0.2 and SCIP 10.0.3 through GAMS 54.3, with 3600 s, one thread and optcr = optca = 1e-9.

- **Driver.** PID 898862, started 2026-10-02 23:45:08 UTC in `/workspace/minlp-notes/research-20260929/publication/solver-runs`.
- **Admission.** Other sessions kept load1 at 35-150, so admission held every start for 4,262 s. The first 10 runs were admitted at 2026-10-03 00:56:08 UTC (load1 29.9, MemAvailable 12.4 GB).
- **CPU share.** At 01:00 UTC the 10 runs got 0.84-0.95 of a CPU each at load about 40 on 36 logical CPUs. My own 60 s /proc sample agrees with the driver's figures (0.86-0.93 cumulative at 96 s).
- **Driver 1.** All 10 runs that driver 1 finished at a CPU share of about 0.71 are archived in `runs_archive/driver1/`. Every run is being redone.

The required changes were written by an earlier fixer agent (transcript `wf_a89a60b6-d10/agent-a68ce70fe87340209.jsonl`), which tested them in `smoke2/` but was cut off before relaunching. I reviewed and retested that code. During the first relaunch I found two more problems and fixed them (see "Changes made in this round").

## What review round 1 required, and what is now in place

| requirement | implementation (driver.py / collect.py) | tested by |
|---|---|---|
| A run stopped by a memory guard, a driver stop or any cause other than its own completion or the hard timeout is requeued, not marked finished | The machine memory-floor rule of driver 1 is removed. A memory-cap stop, a low-CPU-share stop or an end without a trace record that the driver did not cause makes the attempt invalid; it is archived and requeued. A driver stop (SIGTERM, or SIGKILL of the driver) leaves the run unfinished; a restart deletes it, kills leftover process groups and reruns it, and it does not count as an attempt | smoke2/memcap, keep_restart, stop_term, stop_kill, stop_kill2, v3_mem; launch-1 stop (below) |
| Validity: CPU time of the process group / wall time >= 0.9, else archive under runs_archive/ and requeue, at most 2 retries, then keep the best attempt and flag it | `run.json` fields: valid, validity, end_kind, attempt, attempts_total, kept_best. CPU time is max(wait4 of gams, sum of /proc utime+stime of all group processes). Invalid attempts go to `runs_archive/attempts/<inst>__<solver>__a<k>/`. After 3 attempts the best one (proper end, then trace record, then highest CPU/wall) is copied back with valid=false and kept_best=true | smoke2/lowcpu (taskset to one CPU), final_requeue (min ratio 1.5), early_abort, v3_basic |
| Exemption (fixer's design, kept) | The 0.9 test is skipped for attempts that completed on their own within 60 s and not at the time limit. Example: BARON and SCIP reject ann_cumene_tanh (tanh unsupported) in about 1 s at CPU/wall 0.04-0.3, mostly GAMS start-up; a retry cannot change that | smoke2/basic, final_basic, v3_basic |
| Rerun the 10 driver-1 runs; archive the old ones | `runs/`, `driver.log`, `progress.txt`, `machine_load.csv`, `driver.out` and `driver.pid` of driver 1 moved to `runs_archive/driver1/` (19 run folders, 10 finished). They are not used | ls |
| Admission: start only if load1 <= 30 and MemAvailable >= 8 GB; never more than 10 runs; log every wait | `Driver.admit`: "wait" log line when a wait begins, when its reason changes and every 10 min; "admit" line when it ends; `run.json` records admission_wait_s, load1_at_admission and mem_available_gb_at_admission | smoke2/test_admit.py (unit test, patched load and memory); smoke2/admit_live; launch 2 (7 wait lines, then the admit line at 00:56:08 UTC) |
| collect.py minor fixes | The BARON progress-row regex now accepts '+' after the iteration number and 'NA' progress: 119 rows match in driver 1's kan_r3_h1_n9__BARON log, where the old regex matched 0. When GUROBI's objest is NA the bound comes from its log line (13 significant digits), and the row gets the note "known only to +-<half unit>". New columns: attempt, attempts_total, valid, validity, end_kind, cpu_over_wall, cpu_time_wait4_s, cpu_time_proc_s, load1_mean, peak_group_swap_mb, machine_swap_used_max_gb, dual_bound_text, dual_bound_print_halfunit, solver_log_primal. Rows without a trace record get no threads_confirmed. A note flags a returned point whose objective differs from the solver's own incumbent beyond printing precision (review minor issue 5) | collect.py on driver-1 runs (`/tmp/sr_fix3/driver1.csv`), smoke2/*/results.csv, live partial state |
| Restartable; hard timeout reslim + 600 s | Kept (4,200 s). Restart skips finished runs, finishes an interrupted archiving step, and runs keep_best for runs whose attempts are used up | smoke2/lowcpu restart, keep_restart, final_basic restart (15 skipped), v3_basic restart (15 skipped) |

Other driver changes by the fixer, kept:
- The memory cap counts resident plus swapped memory.
- The SIGINT grace is 300 s (driver 1: 120 s).
- Each run records swap and mean load.
- `machine_load.csv` records swap.

## Changes made in this round

### 1. Early stop for low CPU share (new)

**What happened in launch 1.** The first relaunch (PID 819808, 2026-10-02 22:56:11 UTC) admitted 10 runs at load1 4.6.
- My independent 30 s /proc sample gave each of them a CPU share of 1.000-1.006.
- From about 23:08 UTC another session (`research-20261001`) started 16 `spar_audit.py` processes of about 3.8 GB each, plus compiles. load1 rose to 130-176, MemAvailable fell to 1.5 GB, and swap filled up (14.96 of 16 GB). 9.1 GB of our runs' memory was swapped out.
- The runs' cumulative CPU/wall fell from 1.00 to 0.86-0.90 by 23:31 UTC.

Without a change, every episode like this costs up to an hour in each of the 10 slots, ends in invalid attempts, and adds to the machine's load.

**The change.** The monitor now interrupts an attempt as soon as its CPU/wall cannot reach 0.9, even if from then on it got 1.02 CPU-seconds per second until its latest possible end:

`(cpu + 10 + 1.02 * (W_max - wall)) / W_max < 0.9`, with `W_max = reslim + 600 + 300 + 30 = 4,530 s`.

- The factor 1.02 covers GUROBI's helper threads (measured 1.005-1.006).
- The 10 s covers CPU time that the 5 s /proc samples can miss.
- An attempt stopped this way would have been invalid anyway, and it is requeued.
- With the campaign settings the rule fires once about 550 s of CPU time are lost. It would not yet have stopped the launch-1 runs (about 250 s lost at 2,047 s).

**Stopping launch 1.** I stopped launch 1 with SIGTERM at 23:31:57 UTC to install the change. A driver stop does not count as an attempt, so no retries were used. The 10 stopped run folders and a progress snapshot are in `runs_archive/driver2_launch1_stopped/`; they are not results.

**Test.** `smoke2/early_abort` and `smoke2/v3_abort`: 3 runs pinned to one CPU, reslim 600, hard timeout 200 s. The predicted firing point was about 107 s. The rule fired at 106-111 s with cpu/wall 0.32-0.34, and the attempts were archived, requeued and kept-best as designed.

### 2. SIGINT to the solver process only (bug fix)

**The finding.** In the early-abort test, GUROBI handled the interrupt itself: its log says "Status: User Interrupt (8) / Feasible (7)". But GAMS recorded solver/model status 13/13 (System Failure / Error No Solution), with no objective and no savepoint. The solver status file in the listing is cut off.

**Reproduced.** With driver 1's own manual test script (`smoke/manual/sigtest.py`, SIGINT to the whole process group):
- GUROBI interrupted at 10 s returns 7/8 with a savepoint, as in driver 1's test.
- Interrupted at 25 s or 40 s, it returns 13/13 with no solution (`smoke2/sigtest_gurobi_25s`, `smoke2/siggroup_GUROBI_40`).
- Through the driver, a group SIGINT gave GUROBI 13/13 at 20 s (`smoke2/gurobi_int`, ex6_2_5 and chain50) and at 60 s on a starved CPU (`smoke2/int_starved`).
- BARON and SCIP returned 7/8 in all these tests.

**Why it matters.** This affects every driver interrupt of a GUROBI run: hard timeout, memory cap and low-CPU-share stop.

**The fix.** SIGINT now goes only to the process of the run's group with the most CPU time (`baron`, or `gmsgenux.out` for GUROBI and SCIP). The log line names it, for example "only pid 895307 (gmsgenux.out)". SIGTERM and SIGKILL escalation still go to the whole group.

**Tests.** With solver-only SIGINT every interrupt returned 7/8, the returned objective and a savepoint:
- `smoke2/sigsolver_*`: GUROBI at 25 s and 60 s; SCIP and BARON at 25 s.
- `smoke2/v3_hard`: hard timeout 25 s, 3 solvers x ex6_2_5 and chain50, 6/6 valid.
- `smoke2/v3_abort`: low-share stop, 3/3.
- `smoke2/v3_mem`: memory cap, GUROBI and SCIP.

## Relaunch (launch 2) and its first runs

- **Command.** `cd /workspace/minlp-notes/research-20260929/publication/solver-runs && setsid nohup python3 driver.py >> driver.out 2>&1 < /dev/null &`. Driver PID 898862, own session, started 2026-10-02 23:45:08 UTC, 129 tasks queued.
- **Admission.** load1 was 149.5 at start. The driver logged "wait optcdeg2__BARON" at 23:45:08 and every 10 min after, with load1 101.0, 77.0, 66.3, 86.4, 50.6, 35.7 and 33.6. It then logged "admit optcdeg2__BARON after waiting 4262 s (load1 29.9, MemAvailable 12.4 GB)" at 00:56:08 UTC.
- **First runs.** All 10 started at 00:56:09 UTC: optcdeg2, dtoc5 and waterno2_24 with all three solvers, and kan_r3_h1_n9 with BARON. This is the queue order, largest models first.
- **Settings echo.** In launch 1, every one of the 10 logs echoed `ResLim 3600, Threads 1, OptCR 1E-9, OptCA 1E-9, SavePoint 1`. The command lines are unchanged in launch 2.
- **CPU share.**
  - The driver reported cumulative CPU/wall 0.86-0.93 at 96 s (this includes 10 simultaneous GAMS starts).
  - My independent 60 s /proc sample at about 00:58 UTC gave 0.836-0.954 per run at load1 39.5-41.6.
  - MemAvailable was 5.1-6.1 GB at that time, because of other sessions. New starts wait until it is at least 8 GB again.
- **collect.py** parsed the 10 live, unfinished run folders without error.

## Expected completion

- **No more waits or retries.** 129 runs on 10 slots. Two runs (BARON and SCIP on ann_cumene_tanh) end in about 1 s; almost every other run uses its full hour (BARON 3,600 CPU-s, GUROBI and SCIP 3,600 s wall) plus 10-30 s of GAMS start and exit. That is about 13 rounds of about 3,630 s, so about 13 h from the first admission: **about 14:00 UTC on 2026-10-03**.
- **Worst case without waits or retries.** Every run reaches the hard timeout plus the full 330 s escalation (4,530 s): about 16.4 h, so about 17:20 UTC on 2026-10-03.
- **Retries and waits come on top.** Each invalid full-length attempt adds about 6 minutes to the whole batch (one hour of one slot out of 10). Admission waits add their full length. With the load seen today, retries are likely: other sessions held the load at 35-176 for most of 23:08-00:56 UTC. `progress.txt` prints the remaining estimate every 30 s.

## Open issues and caveats

1. **Admission at load1 <= 30 does not guarantee CPU/wall >= 0.9.** With about 30 runnable processes from others, our 10 runs make about 40 runnable on 36 logical CPUs (18 physical cores), and each gets about 0.84-0.95. Some first-round attempts may therefore end just below 0.9 and be requeued, which uses up retries. If many attempts end invalid, two options exist for the user or root:
   - a lower `--max-load` (for example 26, that is 36 - 10);
   - fewer `--jobs`.

   Either needs a driver restart, which kills the running runs without counting them as attempts. I did not change the specified thresholds.
2. **Hyperthreading.** CPU/wall >= 0.9 measures time on a logical CPU, not speed. On a machine whose hyperthread siblings are busy, a CPU-second does less work than on a quiet core. The paper should state the machine (Xeon w5-2565X, 18 cores / 36 threads, shared) and the validity rule.
3. **Memory pressure from other sessions.** No rule reacts to the machine's free memory (by design; driver 1's rule interrupted our runs for another job's memory). Swapping lowers CPU/wall, so the validity rule catches it.

   If the kernel OOM killer kills a solver process, GAMS probably reports solver status 10-13. Such an attempt counts as "completed" and is not retried automatically. The analysis step should check rows with solver status 10-13 against `machine_load.csv` (MemAvailable, swap).
4. **Hard timeout without a result.** A run that reaches the hard timeout and ignores SIGINT for 300 s is valid (if its CPU/wall >= 0.9) but has no trace record and no result. This is a real outcome of the setting, and a retry would probably repeat it. In driver 1, optcdeg2__BARON ended this way, with a 120 s grace and at CPU/wall about 0.7.
5. **ann_cumene_tanh.** BARON and SCIP reject tanh (solver status 6), so only GUROBI gives a result for the unmodified model. A run with tanh rewritten is not part of this campaign.
6. **Precision.** When GAMS/Gurobi leaves objest NA (general nonlinear NLPs, for example chain50 and ex6_2_5), GUROBI's bound comes from its log line with 13 significant digits. collect.py notes the half-unit (for example ±5E-12 for chain50). GAMS can also return a point other than the solver's incumbent; for example SCIP on chain50 differs by 8.57e-10. The exact-feasibility step must read `m_p.gdx` exactly (`gdxdump m_p.gdx dFormat=hexponential`).
7. **Previously untested; now tested only on short runs.** BARON's response to SIGINT deep in a long local search of a 150,000-variable model (optcdeg2) has not been tested with solver-only SIGINT. It will show in the campaign: `kill_stage` greater than 1 in `run.json` means escalation was needed.
8. **Earlier reviewer checks still apply.** The `.gms` files, the GAMS command line and the parsing rules for final bounds are unchanged since review round 1, which verified them independently (models equal to the OSIL files, settings in effect, bound sources). I did not repeat those checks.

## Verification status

- **Verified with independent code (my own /proc sampling scripts, separate from driver.py):**
  - CPU shares of launch 1 at load1 about 14: 1.000-1.006.
  - CPU shares of launch 2 at load1 about 40: 0.836-0.954.
- **Tested** (driver behaviour on short runs, results above): admission waits and logging; requeue, archive and keep-best; low-CPU-share stop; memory cap; hard timeout; solver-only SIGINT for all three solvers; restart after SIGTERM and after SIGKILL of the driver; restart skipping finished runs; collect.py columns.
- **Not yet observed:** the end of a full-length launch-2 run (the first ones end at about 01:56-02:00 UTC on 2026-10-03).

## Commands run (this agent)

All commands were run from `/workspace/minlp-notes/research-20260929/publication/solver-runs` unless a path is given.

| command | outcome |
|---|---|
| python JSONL parsing of the two predecessor transcripts (last ~60 entries, first ~60 entries) | learned the fixer's design, tests and stop point (cut off after the `pending` edit and the admit_live test) |
| `cat driver.py collect.py README.md report.md ../reviews/solver-campaign-review-r1.md`; `diff README.md /tmp/sr_fix/README_new.md` | reviewed the code and drafts |
| `python3 collect.py --runs runs --out /tmp/sr_fix3/driver1` (driver-1 runs) | BARON '+' rows parse (last_logged -366.94 for kan_r3_h1_n9); GUROBI log-bound note present |
| `grep -cE '<new BARON row regex>' runs/kan_r3_h1_n9__BARON/gams.log` | 119 rows match |
| `ruff check --select E,F,W --line-length 120 driver.py collect.py` (3 times) | clean |
| `python3 smoke2/test_admit.py` (twice) | OK |
| `python3 driver.py --out smoke2/final_basic --reslim 30 --jobs 8 --instances ex6_2_5 chain50 pricing050 waterno2_06 ann_cumene_tanh` | 15/15 valid (cpu/wall 0.95-0.99; the two tanh rejections exempt) |
| `python3 driver.py --out smoke2/final_requeue --reslim 30 --jobs 2 --instances ex6_2_5 --solvers GUROBI SCIP --min-cpu-ratio 1.5 --max-retries 1` | both runs invalid twice, archived as a1 and a2, best kept with valid=false |
| rerun of the final_basic command; `collect.py` on final_basic, final_requeue and its attempts | 15 skipped; rows carry attempt, valid and cpu_over_wall |
| `mkdir -p runs_archive/driver1 && mv runs driver.log driver.out driver.pid progress.txt machine_load.csv runs_archive/driver1/` | driver 1 archived |
| `setsid nohup python3 driver.py > driver.out 2>&1 < /dev/null &` (launch 1, PID 819808, 22:56:11 UTC) | 10 runs admitted at once, cpu/wall 1.00 |
| own /proc CPU-share sample (30 s) and `grep` of ResLim/Threads/OptCR/OptCA/SavePoint in the 10 logs | 1.000-1.006; settings echoed in all 10 |
| `ps --sort=-rss`, `/proc/<pid>/cwd` (read-only) | the load and memory came from research-20261001 `spar_audit.py` jobs (about 3.8 GB each) and others |
| `kill -TERM 819808` (23:31:57 UTC); `mv runs/* runs_archive/driver2_launch1_stopped/` | 10 runs killed and abandoned (not counted); no leftover GAMS processes |
| python edit of driver.py (early stop) and a unit check of `cannot_reach_ratio` | rule as designed |
| `taskset -c 0 python3 driver.py --out smoke2/early_abort --reslim 600 --hard-extra-s -400 --jobs 3 --instances ex6_2_5 --max-retries 1 --max-load 1000` | fired at 106-111 s; requeue and keep-best worked; GUROBI 13/13 found |
| `python3 driver.py --out smoke2/gurobi_int --reslim 120 --hard-extra-s -100 --jobs 2 --instances ex6_2_5 chain50 --solvers GUROBI --max-load 1000` | group SIGINT at 20 s: GUROBI 13/13, no savepoint (2/2) |
| `taskset -c 2 python3 driver.py --out smoke2/int_starved --reslim 300 --hard-extra-s -240 --jobs 3 --instances ex6_2_5 --max-load 1000 --max-retries 0` | group SIGINT at 60 s: BARON 7/8, SCIP 7/8, GUROBI 13/13 |
| `python3 smoke/manual/sigtest.py <gams> gms/ex6_2_5.gms GUROBI smoke2/sigtest_gurobi_10s`; same with a 25 s sleep (`smoke2/sigtest25.py`) | 10 s: 7/8 with savepoint; 25 s: 13/13 |
| `python3 smoke2/sigtest_solver.py ... {GUROBI,SCIP,BARON} 25 solver`, `GUROBI 60 solver`, `GUROBI 40 group` | solver-only SIGINT: 7/8 with savepoint for all; group at 40 s: GUROBI 13/13 |
| python edit of driver.py (solver-only SIGINT) | done |
| `python3 driver.py --out smoke2/v3_hard --reslim 120 --hard-extra-s -95 --jobs 5 --instances ex6_2_5 chain50 --max-load 1000` | 6/6 hard timeout at 25 s, 7/8, savepoint, valid |
| `taskset -c 3 python3 driver.py --out smoke2/v3_abort --reslim 600 --hard-extra-s -400 --jobs 3 --instances ex6_2_5 --max-retries 0 --max-load 1000` | 3/3 stopped at 111 s, 7/8 with savepoint |
| `python3 driver.py --out smoke2/v3_mem --reslim 120 --mem-cap-gb 0.05 --jobs 2 --instances ex6_2_5 --solvers GUROBI SCIP --max-retries 0 --max-load 1000` | memory cap: SIGINT to gmsgenux.out, 7/8 with savepoint |
| `python3 driver.py --out smoke2/v3_basic --reslim 30 --jobs 10 --instances ex6_2_5 chain50 pricing050 waterno2_06 ann_cumene_tanh --max-retries 0 --max-load 1000`, then the same command again, then `collect.py` | normal path works; at load1 about 129, 10 of the 13 runs that reached the time limit had cpu/wall 0.60-0.89 and were correctly marked invalid; restart skipped 15; 15 rows |
| `setsid nohup python3 driver.py >> driver.out 2>&1 < /dev/null &` (launch 2, PID 898862, 23:45:08 UTC) | admission waited 4,262 s, then admitted 10 runs at 00:56:08 UTC |
| own /proc CPU-share sample (60 s) at about 00:58 UTC | 0.836-0.954 at load1 about 40 |
| `python3 collect.py --runs runs --out /tmp/sr_fix3/live_partial` | 10 live folders parsed |

Backups of intermediate driver versions: `/tmp/sr_fix3/driver_before_early_abort.py` (the fixer's version) and `/tmp/sr_fix3/driver_before_solver_sigint.py`.

## README.md (new content)

````markdown
# Current-solver campaign on the 43 paper instances

## Purpose

The paper says the 43 instances were open on MINLPLib, whose listed bounds
may be years old. This campaign records what three current global solvers
reach on each instance today under one fixed setting: BARON, GUROBI and SCIP
through GAMS 54.3, one thread, one hour. For each run it records the returned
objective, the solver's final dual bound, statuses, wall and CPU time, node
counts and a GDX savepoint of the returned point (for a later
exact-feasibility check).

This folder only runs and parses the campaign. Interpretation (comparison
with our certificates and the listed bounds, exact feasibility of returned
points) is a later step.

## Status

- Driver 1 (first driver.py), PID 143593, ran 2026-10-02 03:15:35-04:27:43
  UTC. The machine's load average was 175-240, and its 10 finished runs got
  CPU/wall 0.65-0.72. Its machine-memory-floor rule interrupted
  optcdeg2__SCIP and dtoc5__BARON because of another job's 32-37 GB process,
  and it marked optcdeg2__SCIP finished without a result. Review round 1
  rejected these runs as a measurement. All driver-1 files are in
  `runs_archive/driver1/` and are not used. Every run is redone.
- Driver 2 (current driver.py), launch 1, PID 819808, 2026-10-02
  22:56:11-23:32:04 UTC. Its first 10 runs got CPU/wall 1.00 until other
  sessions raised load1 to 130-176 and filled the swap (from about 23:08 UTC).
  It was stopped (a driver stop does not count as an attempt), two changes were
  made (the low-CPU-share stop and SIGINT to the solver process only, see
  below), and it was relaunched. The stopped run folders are in
  `runs_archive/driver2_launch1_stopped/` and are not used.
- Driver 2, launch 2, PID 898862, started 2026-10-02 23:45:08 UTC with all
  129 runs. Admission waited 4,262 s (load1 35-150 from other sessions) and
  admitted the first 10 runs at 2026-10-03 00:56:08 UTC.

## Versions

| component | version (as printed in the logs) |
|---|---|
| GAMS | 54.3.1 61154be4 (LEX-LEG x86 64bit/Linux), license G251008+0003Ac-GEN, evaluation license valid to 2027-06-30 |
| BARON | 26.5.27, built LNX-int-64 2026-05-27; subsolvers: LP/MIP CLP/CBC and ILOG CPLEX, NLP MINOS, SNOPT, External NLP, IPOPT, FILTERSQP |
| GUROBI | Gurobi Optimizer 13.0.2, build v13.0.2rc1 (GAMS/Gurobi link license) |
| SCIP | 10.0.3 (d409edf9f6); LP solver CPLEX 22.1.2.0; Ipopt 3.14.19 (linear solver ma27), CONOPT 4.39.1, PaPILO 3.0.1, CppAD, Nauty 2.8.9, sassy 2.1 |

collect.py re-reads the versions from every run's log (columns
`solver_version`, `gams_version`).

Machine: Intel Xeon w5-2565X, 18 cores, 36 hardware threads, 47 GB RAM,
16 GB swap, shared with other jobs.

## Exact settings

Each run is one GAMS job on the unmodified MINLPLib `.gms` file:

```
cd runs/<instance>__<solver>
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  gams <abs path>/gms/<instance>.gms <TYPE>=<SOLVER> reslim=3600 threads=1 \
  optcr=1e-9 optca=1e-9 lo=2 logfile=gams.log o=<instance>.lst \
  savepoint=1 trace=trace.trc traceopt=3
```

- `<TYPE>` is the model type in the file's solve statement: NLP for 29
  instances, MINLP for the 14 instances eg_*_s (3), kan_* (6) and
  waterno2_* (5). All minimize except pricing050, which maximizes.
- No solver option files and no other solver options. The files themselves
  set only `m.limrow=0; m.limcol=0; m.tolproj=0.0`.
- One thread: GAMS `threads=1`. GUROBI logs `Threads 1` and "using up to 1
  threads"; SCIP logs `lp/threads = 1`; the input file GAMS writes for BARON
  says `Threads: 1`.
- Time limit: GAMS `reslim=3600`. GUROBI and SCIP enforce it on wall-clock
  time. BARON with one thread enforces it on CPU time (GAMS/BARON
  documentation).
- Gap: `optcr=1e-9`, `optca=1e-9`, so runs stop at the time limit or at
  proven optimality, not at the default 1e-4 gap.

## How the driver runs the batch

Queue: all 129 (instance, solver) pairs, largest model (by nonzeros)
first, the three solvers of an instance together. At most 10 runs at once.

Admission: a run starts only if the 1-minute load average is at most 30
and MemAvailable is at least 8 GB. Every wait is logged in `driver.log`:
"wait" when it begins, when its reason changes and every 10 minutes; "admit"
when it ends. `run.json` records the wait and the load and memory at
admission.

Limits, checked every 5 s:

- hard wall-clock timeout reslim + 600 = 4,200 s;
- memory cap: more than 8 GB resident plus swapped memory in the run's
  process group;
- low CPU share: the attempt can no longer reach CPU/wall 0.9 even if it got
  1.02 CPU-seconds per second until its latest possible end (4,200 + 300 +
  30 = 4,530 s), with 10 s of slack. With these settings this happens once
  about 550 s of CPU time are lost. Such an attempt would be invalid anyway.

On a limit the driver sends SIGINT to the solver process only: the process
of the group with the most CPU time (`baron`, or `gmsgenux.out` for GUROBI and
SCIP). The solver stops as on a user interrupt (solver status 8). GAMS still
writes the final bound, the trace record and the savepoint. The driver does
not send SIGINT to the whole process group: then GAMS reacts as well, and
GUROBI runs interrupted after 20 s or more ended with status 13/13 and no
solution (tests in `smoke2/`). If the run is still alive 300 s after SIGINT,
the group gets SIGTERM, and SIGKILL 30 s after that; such a run has no
result. `run.json` records `kill_reason` and `kill_stage` (1 = SIGINT,
2 = SIGTERM, 3 = SIGKILL). No rule reacts to the machine's free memory.

Validity. An attempt counts (`valid` true) only if

- (a) it ended by its own completion with a trace record, or by the hard
  timeout, and
- (b) CPU time of its process group / wall time >= 0.9.

Test (b) is skipped for attempts that completed on their own within 60 s and
not at the solver's time limit. Example: BARON and SCIP reject
ann_cumene_tanh in about 1 s, mostly GAMS start-up. CPU time is the larger of
two lower bounds: the wait4 resource usage of the `gams` process and the sum
of the last /proc utime+stime samples of all processes of the group.

An invalid attempt (low CPU share, memory cap, or an end without a trace
record that the driver did not cause) is moved to
`runs_archive/attempts/<instance>__<solver>__a<k>/` and requeued at the end
of the queue, at most 2 times. After the third invalid attempt the best one is
copied back to `runs/` with `valid` false and `kept_best` true. The best one
has a proper end first, then a trace record, then the highest CPU/wall. A run
that reaches the hard timeout is valid if (b) holds, even when the solver
ignored SIGINT and returned no result. That is an outcome of the setting.

Restart: finished runs (`run.json` has `finished: true`) are skipped. A
run killed by a driver stop, or left behind by a killed driver, is deleted and
rerun from scratch; any of its processes still alive are killed first. It does
not count as an attempt. Attempt numbers continue from
`runs_archive/attempts/`.

## Files

| path | content |
|---|---|
| `instances.txt` | the 43 instances |
| `gms/` | downloaded `.gms` files (gitignored; re-download from `https://www.minlplib.org/gms/<name>.gms`) |
| `download.log` | download time and HTTP status per file (2026-10-02 02:51-02:52 UTC) |
| `check_gms.py` | sha256 of each `.gms` and count check against the cached OSIL |
| `gms_manifest.csv`, `.json` | per instance: sha256 (gms and OSIL), model type, sense, header counts, OSIL counts, match flag |
| `driver.py` | batch driver (queue, admission, limits, CPU and memory accounting, validity, retries, progress, restart) |
| `collect.py` | parser: run folders -> `results.csv`, `results.json` |
| `runs/<instance>__<solver>/` | the counted attempt: `cmd.txt`, `gams.log`, `<instance>.lst` (gitignored), `trace.trc`, `m_p.gdx` savepoint, `stdout.txt`, `run.json` (settings, attempt, admission, start and end, wall and CPU time, memory and swap, mean load, kill reason, end kind, validity, `finished`) |
| `runs_archive/attempts/` | invalid attempts, same layout |
| `runs_archive/driver1/` | driver 1: runs, `driver.log`, `progress.txt`, `machine_load.csv`, `driver.out`, `driver.pid` (not used) |
| `runs_archive/driver2_launch1_stopped/` | the 10 runs of launch 1 when it was stopped, and its progress at 23:30 UTC (not used) |
| `driver.log` | events of driver 2: start, wait, admit, signal, end, archive, requeue, keep |
| `progress.txt` | status, rewritten every 30 s |
| `machine_load.csv` | load average, MemAvailable, swap used, our running runs, our RSS and swap, every 60 s |
| `driver.pid`, `driver.out` | PID and stdout/stderr of the current driver |
| `smoke/` | driver-1 tests (smoke test, guard tests, manual SIGINT tests) |
| `smoke2/` | driver-2 tests (see report.md) |
| `report.md` | track report |

`m_p.gdx` exists only if the solver returned a point. The savepoints of
optcdeg2 and dtoc5 (up to about 15 MB each), all `.lst` files and GAMS scratch
folders are gitignored.

## Checking progress

```
cd /workspace/minlp-notes/research-20260929/publication/solver-runs
cat progress.txt                      # running runs (elapsed, CPU, memory), finished runs, time left
tail -20 driver.log                   # events, including admission waits
ps -p $(cat driver.pid) -o pid,etime,cmd
tail -3 machine_load.csv
```

## Stopping and restarting

`kill -TERM $(cat driver.pid)` stops the batch. Runs that are not already
being interrupted are killed. After a restart they are rerun from scratch and
do not count as attempts. Restart with

```
cd /workspace/minlp-notes/research-20260929/publication/solver-runs
setsid nohup python3 driver.py >> driver.out 2>&1 < /dev/null &
```

If the driver was killed with SIGKILL, the restart kills the leftover GAMS
process groups of unfinished runs itself.

## Rerunning one run

Do not start a second driver while the batch runs: the batch uses the whole
budget of 10 runs. After the batch has ended:

```
python3 driver.py --out rerun --instances chain50 --solvers SCIP
python3 collect.py --runs rerun/runs --out rerun/results
```

A run can also be repeated by hand from its `cmd.txt`.

## Collecting results

```
python3 collect.py                                          # runs/ -> results.csv, results.json
python3 collect.py --runs runs_archive/attempts --out attempts   # invalid attempts
```

It also works on a partial campaign. One row per run folder with:

- run identity, versions and settings: instance, solver, solver_version,
  gams_version, model_type, sense, reslim, optcr, optca, start_utc,
  end_utc, run_dir;
- validity: run_finished, attempt, attempts_total, valid, validity,
  end_kind, kill_reason, return_code;
- statuses: model and solver status codes and texts, termination_message;
- objective and bound: primal_objective (only for model status 1, 2, 7, 8,
  15-17), objective_reported, solver_log_primal, dual_bound,
  dual_bound_text, dual_bound_print_halfunit, dual_bound_source,
  objest_trace, dual_bound_log_final, dual_bound_last_logged, rel_gap;
- time: wall_time_s, gams_elapsed_s, solver_time_s, cpu_time_s,
  cpu_time_wait4_s, cpu_time_proc_s, cpu_over_wall, load1_mean;
- search and threads: nodes, nodes_log, threads_confirmed,
  threads_evidence;
- memory and the rest: peak_group_rss_mb, peak_group_swap_mb,
  machine_swap_used_max_gb, savepoint_gdx, generated_counts_match_osil,
  notes.

How the dual bound is chosen:

- GAMS passes the solver's final bound as the model attribute objest (trace
  field ObjectiveValueEstimate). GAMS/Gurobi leaves it NA for general
  nonlinear NLPs (seen for chain50, ex6_2_5 and optcdeg2, but not for
  pricing050).
- collect.py also reads each solver's end-of-run summary in the log: BARON
  `Best possible = ...`, GUROBI `Best objective ..., best bound ...`, SCIP
  `Dual Bound : ...`. These are final global bounds, not root or node
  relaxation values.
- `dual_bound` is objest when available, otherwise the log value. When both
  exist they must agree to 1e-10 relative; otherwise the row gets a note.
- A bound counts only after solver status 1, 2, 3, 4 or 8. After a solver
  failure the reported objest stays in `objest_trace` with a note.
- Values of magnitude >= 1e20 are written as `inf`/`-inf`.
- `dual_bound_last_logged` is the last progress-table value. For BARON it is
  the lower-bound column when minimizing and the upper-bound column when
  maximizing; rows with `+` or `NA` are read. It is a fallback for runs that
  ended without a final summary.

Precision (important for comparisons with certificates at the 1e-12 level):

- `dual_bound_text` is the decimal string as its source printed it. The
  trace prints 15 significant digits, GUROBI's log summary 13, BARON's and
  SCIP's summaries 15, BARON's progress table 6. `dual_bound_print_halfunit`
  is half a unit in the last printed digit. A GUROBI bound taken from the log
  (objest NA) gets a note such as "known only to +-5E-12". Compare with exact
  rational arithmetic on the text and allow this half unit.
- `primal_objective` is the objective of the point GAMS returned. GAMS can
  return a point other than the solver's own incumbent: in a 30 s chain50 run,
  SCIP's summary says 5.07226149312356 but the returned point has
  5.07226149398097. A note flags such differences. The exact-feasibility check
  must use the savepoint, read exactly with
  `gdxdump m_p.gdx dFormat=hexponential`.

## Expected completion

The first 10 runs were admitted at 2026-10-03 00:56:08 UTC. Two runs (BARON
and SCIP on ann_cumene_tanh) end in about 1 s; almost every other run uses
its full hour plus 10-30 s of GAMS start and exit.

- If every attempt is valid and there are no more admission waits: about 13
  rounds of about 3,630 s, so about 13 h. Expected end about 14:00 UTC on
  2026-10-03.
- Worst case without waits or retries: every run reaches the hard timeout and
  the full escalation (4,530 s), about 16.4 h, so about 17:20 UTC on
  2026-10-03.
- Each invalid full-length attempt adds about 6 minutes to the batch (one
  slot-hour out of 10), and admission waits add their full length. Given the
  load from other sessions on 2026-10-02 (35-176 for most of 23:08-00:56
  UTC), some delay is likely. `progress.txt` prints the remaining estimate.

## Caveats for interpretation

- The machine is shared. Admission at load1 <= 30 does not guarantee
  CPU/wall >= 0.9: with about 30 runnable processes from others, our 10 runs
  got 0.84-0.95 each at load about 40. The validity rule and the retries handle
  this. Runs with `kept_best` true are not valid measurements.
- CPU/wall >= 0.9 measures time on a logical CPU. When hyperthread siblings
  are busy, a CPU-second does less work than on a quiet core. Report the
  machine and the rule with the results.
- BARON's time limit is CPU time; GUROBI's and SCIP's are wall-clock time.
  A valid GUROBI or SCIP run had at least about 3,240 CPU-seconds.
- No rule reacts to the machine's free memory. If the kernel OOM killer kills
  a solver, GAMS probably reports solver status 10-13 and the attempt counts as
  completed. Check such rows against `machine_load.csv`.
- ann_cumene_tanh: BARON ("Cannot handle function 'tanh'") and SCIP ("GAMS
  function tanh not supported") stop with solver status 6, so only GUROBI
  gives a result for the unmodified model.
- Solver results are floating-point claims within the solvers' tolerances,
  not proofs. Returned points must be checked for exact feasibility
  (savepoints) before primal values are compared with our certificates.
````