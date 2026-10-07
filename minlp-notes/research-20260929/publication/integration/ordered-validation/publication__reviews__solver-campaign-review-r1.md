# Review of track solver-campaign, round 1

Reviewer: independent verifier. Reviewed: `publication/solver-runs/` (README.md,
driver.py, collect.py, check_gms.py, smoke/, the live batch). Review time:
2026-10-02 03:24-03:50 UTC, about 9-35 minutes after the batch started.
Reviewer check code and outputs: `publication/reviews/solver-campaign-r1/`.

## Verdict

**Issues (two major, no blocker).** The campaign was built as the
specification asks and is running correctly. The settings took effect. The
instances are the cached OSIL models. collect.py extracts the solvers' final
bounds correctly. The driver keeps at most 10 runs and interrupts runs at the
hard timeout. I found two major problems:

1. One of the 129 runs, optcdeg2__SCIP, is already lost. The driver marked
   it finished, so a restart will not rerun it.
2. The shared machine gives every run about 0.72 of a CPU, and there was a
   swap episode. The results will therefore not be a clean "one hour, one
   thread" measurement.

Neither problem is a coding error that makes the batch broken, so I did not
stop or restart it.

## What I verified with my own code

| check | result | kind |
|---|---|---|
| instance list | `instances.txt` equals the 43 instances of the task | verified |
| sha256 manifest | recomputed sha256 of all 43 `.gms` and 43 cached OSIL files; all 86 equal `gms_manifest.csv` | verified |
| local `.gms` = server | re-downloaded all 43 from `https://www.minlplib.org/gms/<name>.gms` (sequential, 1 s delay, 03:33:4x-03:34:55 UTC, all HTTP 200); all 43 byte-identical to `solver-runs/gms/` | verified |
| `.gms` model = cached OSIL model | GAMS 54.3 CONVERT wrote OSiL from each campaign `.gms`; my parser compared it with the cached OSIL. All 43: same variable names and order, types and bounds (exact), same constraint names, order, bounds and constants (exact), same objective sense. Every row function and the objective (linear + quadratic + nonlinear tree), evaluated in float64 at 4 random points within the bounds, agrees. The worst scaled difference is 8.0e-15 (kan_r3_h1_n9, powerflow0039r); the 43 models give 0 non-finite values. Negative controls: a 1e-7 relative change of one coefficient (chain50) and a 1e-9 change of one row bound (pricing050) are both detected | numerical evidence (float evaluation), not a proof; stronger than the author's count comparison |
| pricing050 header | header says 296 nonzeros, 295 nonlinear. GAMS 54.3 generates 296 / 249 (trace), and the model content matches the OSIL. The header's 295 counts every entry except the objvar coefficient. This is a header counting convention, not a model difference. Author's conclusion confirmed | verified |
| no hidden option overrides | no `.gms` file has `option` statements, `$set` other than the `%NLP%/%MINLP%` default, or model attributes other than `m.limrow`, `m.limcol`, `m.tolproj` | verified |
| settings took effect, smoke (18 runs) | GAMS echo `ResLim 30, OptCR 1E-9, OptCA 1E-9, Threads 1, SavePoint 1` in every log; GUROBI `TimeLimit 30, MIPGap 1e-09, MIPGapAbs 1e-09, Threads 1`, "using up to 1 threads", "Thread count was 1"; SCIP `limits/time = 30, limits/gap = 1e-09, limits/absgap = 1e-09, lp/threads = 1`, and no non-default parameters except GAMS/SCIP's fixed ones; BARON summary `optca = 1E-9`, `optcr = 1E-9` | verified |
| settings took effect, live campaign (10 runs) | same echoes with 3600. For BARON I read the input file GAMS wrote (`225a/mybaron.dat`) for all 4 live BARON runs: `EpsA: 1e-9; EpsR: 1e-9; MaxTime: 3600; Threads: 1;` | verified |
| one thread in practice | live processes: BARON and SCIP have 1 OS thread each. Each GUROBI process has 3 threads, but two of them used 2-4 CPU-s in 10 minutes (helper threads) | verified |
| time-limit semantics | GAMS/BARON docs (S_BARON.html): with threads = 1 MaxTime is CPU time. GAMS/SCIP docs: `timing/clocktype` default 2 = wall clock, and the logs show GAMS does not change it. GUROBI TimeLimit is wall clock. The README is correct | verified (docs) |
| collect.py dual bound | my own parser (trace via csv module, final summaries from the logs) agrees with `smoke/results.csv` on dual bound and primal value in 18/18 rows, and on 2/2 rows of my BARON hard-timeout test. The source rules are right: objest = solver's final bound; BARON "Best possible", GUROBI "best bound" and SCIP "Dual Bound" are end-of-run global bounds, not root values. Bounds after solver status 6/10 are correctly excluded | verified |
| concurrency | 10 campaign GAMS jobs at 03:24 and 03:48 UTC; 10 worker threads each run one job at a time | verified |
| queue order | largest first by `.gms` nonzeros: optcdeg2 (400002), dtoc5 (249996), waterno2_24 (13123), kan_r3_h1_n9 (12686), ...; the first 10 started runs match | verified |
| hard timeout | author tested SCIP (smoke/guard_timeout). I ran the author's driver into `/tmp` on BARON with reslim 300 and hard timeout 60 s (camshape800, waterno2_06), which is the case that will occur for BARON in this campaign. The driver sent SIGINT at 61 s and 65 s (5 s monitor period). BARON stopped with "Search interrupted by user", solver status 8, final bound and savepoint written, and collect.py parsed both runs correctly | verified for these two runs |
| early observation in the summary | pricing050 (max, verified upper bound -1813.8290784519730577): BARON primal is above it by 4.565e-7, SCIP by 2.799e-7, GUROBI is below by 4.20e-8. chain50 (certified lower bound 5.0722614939828627): BARON is 2.583e-9 below, SCIP 1.893e-12 below, GUROBI 1.697e-12 above. Exact rational arithmetic on the printed trace values; matches the author | verified |
| savepoints | `m_p.gdx` holds all variable levels as doubles. `gdxdump m_p.gdx dFormat=hexponential` prints them exactly, which the later exact-feasibility check should use | verified |
| README counts | 29 NLP (28 min + pricing050 max), 14 MINLP (eg 3, kan 6, waterno2 5); versions match the logs; the 16 s GAMS start delay explains BARON waterno2_06 smoke cpu/wall 0.66 | verified |

## Major issues

### M1. optcdeg2__SCIP is lost, marked finished, and will not be rerun on restart

Driver log:

```
03:41:49Z signal SIGINT to optcdeg2__SCIP: machine MemAvailable 2.6 GB < 3.0 GB; largest run, group RSS 2287 MB
03:43:49Z signal SIGTERM to optcdeg2__SCIP ...
03:43:49Z end optcdeg2__SCIP rc -15 wall 1694s cpu/wall 0.0002 ms None ss None obj None objest None
```

- The cause was another agent's process (PID 191753, a `python3
  code/exp_separate.py` job in `research-20261001/split-practice`, RSS 31.8
  GB). MemAvailable fell from 22.4 GB (03:36) to 2.1 GB (03:45), and 8 GB of
  swap was in use. By 03:46 it was back to 30 GB.
- The memory-floor guard interrupted our largest run (2.3 GB), which could not
  relieve a 31.8 GB shortage.
- SCIP did not respond to SIGINT within the 120 s grace. On the
  150,003-variable model it had finished presolve after 40 s and printed no
  progress line in the next 27 minutes, so it was still processing the root. SIGTERM
  then killed GAMS. The run has no trace record, no final bound, no savepoint
  and no SCIP end summary.
- `run.json` says `finished: true`, so the README's restart command skips the
  run. Only `--redo` reruns it.
- The README states that "GAMS and all three solvers treat [SIGINT] as a user
  interrupt ... and still report the final bound". That was tested only on
  ex6_2_5 (10 variables) and by me on two mid-size BARON runs. It failed here
  on the largest model. The same risk applies to the hard timeout: BARON's
  time limit is CPU time, so under the current load nearly every BARON run
  will be ended by the 4200 s wall hard timeout. Large BARON runs that are
  inside a long subsolve may also miss the 120 s grace. At 03:45,
  optcdeg2__BARON was still in "Doing local search" after about 28 minutes.
- The CPU time recorded for this run is wrong: `cpu_s` 0.29, but the group had
  used at least about 1,180 CPU-s (1,183 s by /proc at about 03:43, between
  the SIGINT and the SIGTERM). `wait4` on the
  `gams` process does not include children that `gams` never reaped. collect.py
  then marks `threads_confirmed` "yes" on the bogus cpu/wall 0.0002.

Required:

- Rerun optcdeg2__SCIP: now in a separate folder (`--out rerun`) or after the
  batch with `--redo`.
- State in the README that runs ended by a guard (especially the memory floor,
  which is about other jobs, not ours) need a rerun. Better, have the driver
  leave memory-floor kills unfinished so a restart reruns them.
- Qualify the SIGINT claim.

Suggested:

- Take CPU time from the monitor's /proc samples of the whole process group,
  not only from `wait4`.
- Leave `threads_confirmed` empty when the run has no trace record.

### M2. The campaign is not a clean one-hour, one-thread measurement on this machine

- **CPU share.** My /proc measurement of each run's process group gave a CPU
  share of 0.70-0.75 for all 10 first-round runs over 1,644 s and 1,986 s.
  Load average was 195-222 on 36 logical CPUs (18 physical cores).
  - GUROBI and SCIP (wall-clock limit) will therefore get about 2,500-2,700
    CPU-s in their hour.
  - BARON (CPU-time limit) will reach the 4,200 s wall hard timeout at about
    3,000-3,100 CPU-s, before its own 3,600 CPU-s limit. BARON's tim.dat for
    waterno2_24 showed 963 CPU-s at 1,275 s wall.
  - Hyperthread siblings are busy, so even the CPU-seconds are slower than on
    a quiet core.
- **Swap.** During the 03:37-03:45 episode our live solver processes had
  0.06-0.98 GB each in swap (for example optcdeg2__BARON: 254 MB resident,
  979 MB swapped).
- **Effect.** Both effects make the solvers look weaker than they are, which
  is the direction that favors the paper's claim that these instances remain
  open. The README documents the CPU-share problem and says low-share runs
  "should be rerun when the machine is quiet". But every run so far has a low
  share, no rerun criterion is defined, and the swap episode is not recorded.
- **Not an implementation error.** The author cannot control other agents'
  load.
- **Before the paper uses these numbers,** the analysis step must either:
  - rerun the campaign (or at least every run whose conclusion could change
    with about 35% more CPU time) on an unshared machine; or
  - report per-run CPU-seconds and the load and swap conditions, and word the
    claim as "within about 2,500-3,100 CPU-s on a loaded machine".

## Minor issues

1. **Expected completion is optimistic.**
   - Under this load the 43 BARON runs will each take about 4,200-4,350 s
     (hard timeout plus interrupt), and the other 86 about 3,600 s.
   - 43 x 4,250 + 86 x 3,610 = 493,000 run-seconds over 10 slots gives about
     13.7 h, so the end will be around 17:00-17:30 UTC on 2026-10-02, not
     16:30.
   - The worst case of about 19:00 UTC stands.
2. **RSS-based memory guards do not count swapped pages.** During the
   episode, our total RSS fell from 10.2 GB to 3.5 GB while swap use rose.
   The 8 GB cap and the floor rule therefore undercount a run's footprint
   exactly when memory is short.
3. **collect.py's BARON `dual_bound_last_logged` fallback misses rows.** Its
   regex does not match progress rows with a `+` after the iteration number
   or with `NA` progress: 0 of 48 rows matched in the live
   kan_r3_h1_n9__BARON log. It is only a fallback for runs killed without a
   summary, but those are exactly the runs that need it.
4. **GUROBI fallback bounds have limited precision.** When objest is NA (seen
   for chain50, ex6_2_5 and optcdeg2, and likely for every general-nonlinear
   NLP), `dual_bound` comes from GUROBI's log line. That line has 13
   significant digits, rounded to nearest. Any comparison of a GUROBI bound
   with a certificate at the 1e-12 relative level needs this caveat. The
   README mentions low precision only for `dual_bound_last_logged`.
5. **GAMS/SCIP may return a point other than SCIP's incumbent.** In the
   chain50 smoke run, SCIP's own summary says `Primal Bound
   +5.07226149312356`, while GAMS returned objective 5.07226149398097 (the
   savepoint point). They differ by 8.6e-10. The later feasibility check
   should test the savepoint, which is what GAMS returned, and should not
   assume it is SCIP's incumbent. collect.py's 1e-6 primal consistency check
   does not flag this.
6. **ann_cumene_tanh gets results from GUROBI only.** BARON ("Cannot handle
   function 'tanh'") and SCIP ("GAMS function tanh not supported") stop with
   solver status 6. If the paper wants three solvers on this instance, it
   needs a separately labelled run with tanh rewritten, for example
   tanh(z) = 2/(1+exp(-2z)) - 1. GUROBI's 30 s smoke run had no finite bound
   (objest -1E100).
7. **No record of the commands run.**
   - The README describes how to run things but does not list what was run:
     the download, check_gms.py, the smoke driver call, the guard tests with
     their parameters, and `smoke/manual/sigtest.py`.
   - The track report (report.md) is missing; the author says the harness
     refused to write it.
   - The project rules ask for this record.

## Not checked

- I did not wait for any campaign run to finish. The 4,200 s hard timeout on
  a real campaign run, and BARON's response to SIGINT during its local-search
  phase on optcdeg2 or dtoc5, are still untested.
- The exact feasibility of any returned point was not checked; that is not
  part of this track.
- `check_gms.py` was read but not reused; my model check replaces it.

## Background state at the end of the review (03:48:41 UTC)

- **Driver.** PID 143593 alive (elapsed 33:06), 10 campaign GAMS jobs
  running, 1 run finished (optcdeg2__SCIP, lost), 118 queued.
- **Machine.** MemAvailable 29.1 GB; load average about 206.
- **CPU share.** Each first-round run had received 0.70-0.74 of a CPU so far.
- **My jobs.** My test jobs (download, convert, OSIL compare, BARON timeout
  test) all finished; none are left running. My test driver wrote only to
  `/tmp/vr_scr1/drvtest`.

## Commands run (reviewer)

All commands ran from `/workspace/minlp-notes/research-20260929/publication/solver-runs`
unless a path is given. Scratch was `/tmp/vr_scr1`.

| command | outcome |
|---|---|
| `cat progress.txt driver.log machine_load.csv`; `ps -p $(cat driver.pid)`; `ps -eo pid,ppid,pgid,...,nlwp,cmd` | driver alive; 10 runs; thread counts per process |
| `ps -L -p <gurobi pids> -o tid,time,pcpu` | GUROBI: 1 busy thread, 2 idle helper threads |
| `diff` of sorted `instances.txt` against the task's 43 names | identical |
| python hashlib over `gms/*.gms` and the cached `*.osil` vs `gms_manifest.csv` | 86/86 equal |
| `grep` for option statements and model attributes in `gms/*.gms` | none besides limrow/limcol/tolproj |
| `solver-campaign-r1/dl.sh` (curl, 1 s delay) then `sha256sum` compare | 43/43 HTTP 200, 43/43 identical |
| `solver-campaign-r1/conv.sh` (GAMS CONVERT, option `OSiL`, threads=1) | 43/43 rc 0 |
| `python3 solver-campaign-r1/osil_compare.py /tmp/vr_scr1/conv` | 43 instances, 0 differences (`osil_compare_all.log`) |
| negative controls with `osil_compare.py` on perturbed chain50 and pricing050 files | both detected |
| text extraction from `docs/S_BARON.html`, `S_SCIP.html`, `S_CONVERT.html` | MaxTime CPU time for 1 thread; SCIP clocktype default wall; CONVERT supports OSiL |
| `grep` of `runs/*__BARON/225a/mybaron.dat` | EpsA/EpsR 1e-9, MaxTime 3600, Threads 1 |
| `python3 solver-campaign-r1/reparse_runs.py smoke/runs 30 smoke/results.csv` | 18/18 rows agree; all settings OK (`reparse_smoke.txt`) |
| `python3 solver-campaign-r1/reparse_runs.py runs 3600` and `grep` of live logs | settings OK in all 10 live runs |
| `python3 driver.py --out /tmp/vr_scr1/drvtest --instances waterno2_06 camshape800 --solvers BARON --reslim 300 --hard-extra-s -240 --jobs 1` (detached, PID 199693) | both runs interrupted at 61 s / 65 s, status 8, bound and savepoint returned (`baron_hard_timeout_test_driver.log`) |
| `python3 collect.py --runs /tmp/vr_scr1/drvtest/runs --out /tmp/vr_scr1/drvtest_results`; `python3 solver-campaign-r1/reparse_runs.py /tmp/vr_scr1/drvtest/runs 300 ...` | 2/2 rows agree |
| `python3 collect.py --runs runs --out /tmp/vr_scr1/live_partial` | works on the partial campaign; shows the lost optcdeg2__SCIP with `thr=yes` |
| python Fraction arithmetic on smoke primal values vs certificates | reproduces the author's 4.6e-7, 2.8e-7, 2.6e-9, 1.9e-12 |
| `gdxdump m_p.gdx`, `gdxdump m_p.gdx Symb=x2 dFormat=hexponential` | savepoints hold exact doubles |
| /proc scans of `stat` (utime+stime per process group) and `status` (VmRSS, VmSwap); `free -g`; `ps -o ... -p 191753` | CPU share 0.70-0.75; swap episode; identified the 31.8 GB process of another agent |
| `git diff .gitignore`; `git check-ignore -v ...`; `git ls-files --others --exclude-standard ... \| xargs du -ch` | gitignore change limited to the September 29 block; tracked campaign output about 1.7 MB so far |

I did not stop, restart or modify the batch, the author's files, or any other
agent's process.
