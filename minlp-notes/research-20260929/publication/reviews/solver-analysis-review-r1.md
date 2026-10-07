Verdict: issues

# Independent review of the final solver campaign analysis (round 1)

Reviewed: `publication/solver-runs/` (report.md, README.md, results_table.md/.csv,
results.csv/.json, references.*, inconsistencies.*, point_checks.*, driver.py,
driver.log, runs/, runs_archive/). Reviewer code and logs are in
`publication/reviews/solver-analysis-r1/`. I wrote my own extraction,
comparison and point-check code. I did not import or run the author's
`collect.py`, `build_references.py`, `check_points.py`, `analyze.py` or
`verify_analysis.py`. No solver was run, and nothing was committed or sent anywhere.

## Summary

The raw data support the numbers. All of the following are confirmed from
the raw artifacts:

- 129 kept outcomes, all from driver PID 898862. Every run used `threads=1`,
  `reslim=3600`, `optcr=optca=1e-9`, the thread environment variables and no
  option file. GAMS echoes `Threads 1` and `ResLim 3600`. GUROBI echoes
  `TimeLimit 3600`, `Threads 1` and "Thread count was 1". SCIP echoes
  `limits/time = 3600` and `lp/threads = 1`.
- The validity rule re-derived from run.json and the trace solver status
  matches the stored `valid` flag for every run. There are 126 valid runs and
  3 invalid SCIP memory-cap runs.
- driver.log records 135 starts and 135 ends: 126 valid plus 9 memory-cap
  attempts. The only signals are the 9 SIGINTs at the memory cap. There was
  no SIGTERM, SIGKILL, hard timeout, low-CPU stop, abandoned run or ERROR.
  Each kept memory-cap copy is byte-identical to its archived attempt.
  `best_key` picked the attempt with the highest CPU/wall, as documented.
  For ex6_2_5 the three ratios tie at 0.9995 and the first attempt was kept.
- Every long valid run ended at the time limit (solver status 3).
- The re-extracted model/solver status, returned primal, final dual and
  solver time agree exactly with results.csv, results_table.csv and
  results_table.md for all 129 rows. The trace `objest` agrees with the
  solver's final log summary wherever both exist.
- All headline numbers are reproduced:
  - finite final duals: 35/36/38 (109 in total; 91 against OSIL
    certificates, 18 against the kan relaxation R);
  - returned primals: 35/40/30;
  - two model-status-1 claims (BARON camshape100/200);
  - no dual beats a certificate; the smallest deficit is 5.2581469e-7
    (BARON camshape100);
  - no dual cuts off a reference primal or a MINLPLib listed primal;
  - five duals improve the listed MINLPLib dual;
  - 36 returned-primal flags (5 against R only) and 38 log-incumbent flags,
    on 39 distinct pairs, with the same log-only and returned-only pairs;
  - 16 returned/incumbent differences (12 SCIP, 4 GUROBI);
  - the CPU/wall and CPU-second ranges, the swap peaks and the memory-stop
    table.
- The objective sense is handled correctly: pricing050 maximizes in the
  trace (Direction 1) and in the reference table, and the three pricing050
  rows are compared with s = −1.
- Reference values:
  - Every certificate and reference primal string in references.csv appears
    verbatim in the research-tree sources. The only exceptions are the four
    camshape exact optima, which are the verified exact values rounded
    outward in the 20th digit.
  - The catmix entries use the verifiers' stronger bounds, as the report
    states.
  - The MINLPLib best listed dual and primal, recomputed from
    `bound-audit/pages.json` using only "primal"-section points, match for
    all 43 instances. optcdeg2's 292.417 "other" point, with infeasibility
    1e-6, is correctly excluded.
- My own GAMS-text evaluator re-checked 9 of the 15 savepoints (60 digits,
  exact binary64 levels). It reproduces the author's worst rows and
  violation sizes: for example camshape100/BARON 9.995e-11 (e100) plus a
  9.997e-11 bound violation, camshape800/BARON 3.314e-7 (e2), and
  powerflow0039p/GUROBI 6.811e-7 (e73).

Two issues do not change any count or conclusion, but should be fixed before
the table and report go into a paper. First, six BARON "dual bounds" are
values that BARON itself says may not be valid global bounds. Second, the
first admitted batch of 10 runs ran under markedly worse machine conditions
than the other runs, and the report's shared-machine section does not say
so. The remaining items are minor wording or completeness fixes.

## Issues

### 1. major: six BARON final duals are reported without BARON's own "globality not guaranteed" disclaimer

- **Location:** results_table.md/.csv rows catmix100, catmix200, catmix400,
  catmix800, dtoc5 and optcdeg2 for BARON. Also report.md "Final results",
  which counts 35 BARON finite final duals and says "BARON returns finite
  bounds on every model it accepts". Also the 109-dual headline.
- **Evidence:** the BARON logs of exactly these six runs print
  `*** User did not provide appropriate variable bounds ***` and
  `*** Globality is therefore not guaranteed ***` (`warnings.log`). BARON is
  therefore not claiming that its "Best possible" value (for example
  −1.17902146621 on catmix100, 0.000273134 on dtoc5, 2.31984 on optcdeg2) is
  a valid global lower bound. Neither the table nor the report mentions
  this. For catmix this matters to the reader: the report says GUROBI and
  SCIP have no finite bound on all four catmix models. BARON then looks like
  the only solver with a finite catmix bound, but BARON disclaims those
  bounds.
- **Effect on conclusions:** none. All six values are far below the
  certificates (C−D from 1.13 to 291.6).
- **Suggested fix:**
  - Add a note "BARON: globality not guaranteed (unbounded variables)" to
    these six rows.
  - In report.md, say that 103 of the 109 finite duals are bounds the solver
    claims as global bounds, and 6 are BARON values that BARON disclaims.
    Alternatively, exclude the six from the "finite dual" count.
  - Make collect/analyze detect this message so the flag is reproducible.

### 2. major: the first batch of 10 runs ran under overload and memory pressure; the report gives only pooled ranges

- **Location:** report.md "Shared-machine limits" and "Admission, validity
  and archive"; results_table.md, where these rows carry no note.
- **Evidence (`checks.log` §4, machine_load.csv):**
  - The 10 jobs admitted together at 2026-10-03T00:56:09Z are dtoc5,
    optcdeg2 and waterno2_24 for all three solvers, plus kan_r3_h1_n9/BARON.
  - After admission, machine load1 rose to 47–51 on 36 hardware threads.
    MemAvailable fell to 1.06 GB, below the 8 GB admission floor. Machine
    swap reached 6.6 GB, and our own groups held about 3–3.8 GB of swap.
    The per-run mean load1 was 33.0–33.6, against a median of 12.2 for the
    other runs.
  - These 10 runs have the 10 lowest CPU/wall ratios of all 117 long runs
    (0.956–0.981). Every other long run has CPU/wall ≥ 0.9991.
  - All four BARON solver times above 3600.5 s are in this batch (3706.4 to
    3728.4 s). GAMS SolverTime for BARON is BARON's wall clock, while
    BARON's limit is CPU time (3600.0–3601.7 s CPU).
  - The round-2 reviewer's live sample at 600 s
    (`reviews/solver-campaign-r2/logs_cpu_share_1.txt`) shows load 46–49 and
    a cumulative CPU share of 0.86–0.90 for the same 10 runs.
  - The admission rule cannot prevent this: it tests the lagging 1-minute
    load and MemAvailable before each start, and all 10 slots were filled
    within one second.
- **Why it matters:** the report's statement "The final long runs all
  exceed the 0.9 rule; no low-CPU-share retry was needed" is true. The pooled
  ranges, however, hide that one identifiable batch differs from the rest by
  about 2–4% CPU share and ran with heavy swapping. Per-group swap peaks of
  613/655/1088 MiB are all optcdeg2 runs in this batch. Swap stalls reduce
  work per CPU-second in ways CPU/wall does not fully capture. Three
  instances therefore have all their solver comparisons measured under
  worse conditions.
- **Suggested fix:**
  - State these batch-specific facts in report.md: time window, peak load,
    minimum MemAvailable, swap, the CPU/wall gap and the BARON wall-time
    overruns.
  - Add a table note to the 10 rows.
  - Say explicitly that admission control did not keep MemAvailable above
    8 GB during runs.
  - Whether to rerun these 10 runs under quiet conditions is the user's
    decision. It is not needed for the bound conclusions, which hold
    regardless.

### 3. minor: "Several GAMS solver times slightly exceed 3600 s" understates the BARON overruns

- **Location:** report.md "Versions, models and settings"; the Time column
  definition in results_table.md.
- **Evidence:** four BARON times are 3706.4, 3708.98, 3709.5 and 3728.4 s,
  up to 3.6% over. In those runs BARON's own CPU time was 3600.0–3601.65 s.
  All other solver times are ≤ 3602.5 s.
- **Suggested fix:** give the maximum overrun. Explain that the BARON Time
  value is wall clock while its limit is CPU time, so contention appears as
  extra wall time (see issue 2).

### 4. minor: solver warnings about the returned point or the model are not surfaced

- **Location:** results_table.md notes; report.md.
- **Evidence (`warnings.log`):**
  - GUROBI eg_int_s prints "Warning: max constraint violation (5.9580e-05)
    exceeds tolerance" for its returned point (8.84042547339). The table
    nevertheless labels the row "time limit, feasible point" without a note.
  - SCIP raises the lower bound of log/pow arguments from 0 (or from a
    negative value) to 1e-9 ("Check your model formulation or use option
    expr/log/minzerodistance") on ex6_2_5, ex6_2_7, etamac, hvycrash,
    lukvle10 and pindyck. SCIP's final dual on these rows is therefore a
    bound for a slightly tightened model. The rows are not affected
    numerically here, because all these duals are far weaker than the
    certificates.
- **Suggested fix:** add a note to the GUROBI eg_int_s row ("solver reports
  max violation 6e-5 beyond its tolerance"). Add one sentence in report.md
  on SCIP's minzerodistance tightening as a caveat on what a "solver dual"
  means.

### 5. minor: GUROBI waterno2 primals that beat MINLPLib's listed values are not mentioned

- **Location:** report.md "Final results" and the waterno2 paragraph.
- **Evidence (`compare.log`):** GUROBI returns 919.990 (waterno2_09),
  2262.231 (waterno2_12) and 7295.020 (waterno2_24). The listed best primals
  are 922.595, 2263.358 and 7332.722. These are improvements of 2.6, 1.1 and
  37.7 that are consistent with the certificates, though worse than our
  reference primals. Their points are unchecked. The other 11
  certificate-consistent "better than listed" returned primals differ only
  at the listed printing precision (8–10 digits). The report has a sentence
  on duals that improve listed duals, but nothing on primals.
- **Suggested fix:** add one sentence. Say that the three points were not
  feasibility-checked; GUROBI's waterno2_06 point has not been checked
  either.

### 6. minor: hvycrash capability wording

- **Location:** report.md "Capability and interface failures"; README.md.
- **Evidence:** hvycrash contains only `cos` (0 `sin(` occurrences), and
  BARON's log reports only "Cannot handle function 'cos'".
- **Suggested fix:** write "sin/cos (hvycrash: cos)".

Checked and found correct, with no issue: driver code paths for killed or
abandoned runs (not counted; run dirs are deleted before each attempt, so a
stale trace cannot validate a run), the short-run exemption, keep-best
selection and copy, and the bound source (objest, falling back to the
solver's final summary; failure statuses are excluded). Also correct: GUROBI
etamac "-" handled as no bound, and the catmix and ann_cumene_tanh `-1E100`
values handled as −∞. The report states the memory-cap, capability and
interface failures honestly: the kept-attempt bound is not the strongest
over retries (ex6_2_7 attempts 2 and 3 had stronger bounds), and the rows
are flagged invalid. The two BARON optimality claims are correctly
characterized: the duals are valid, the primals lie below the exact optima,
and the claims are within MINLPLib's 1e-6 relative convention but outside
the requested 1e-9 tolerance.

## Commands run

All commands ran from `research-20260929/publication/reviews/solver-analysis-r1/`
unless a `cd` is shown. Each ran as one process; the point checks used
`nice -n 10`. All final runs exited 0.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 extract.py > extract.log      # 129 run dirs from raw run.json/trace/gams.log/.lst
PYTHONDONTWRITEBYTECODE=1 python3 checks.py > checks.log 2>&1   # validity, attempts, value agreement, conditions
PYTHONDONTWRITEBYTECODE=1 python3 compare.py > compare.log 2>&1 # certificates, references, MINLPLib, flags
PYTHONDONTWRITEBYTECODE=1 python3 mdtable.py > mdtable.log      # results_table.md vs re-extracted values (via tee)
nice -n 10 python3 pointcheck.py camshape100 BARON camshape800 GUROBI camshape800 BARON chain50 GUROBI \
  pricing050 SCIP pricing050 BARON etamac GUROBI powerflow0039p GUROBI kan_r5_h1_n3 GUROBI > pointcheck.log 2>&1
cd ../../solver-runs && { grep -l "Globality is therefore not guaranteed" runs/*__BARON/gams.log; \
  grep -l "exceeds tolerance" runs/*/gams.log; grep -l "minzerodistance" runs/*/gams.log; \
  grep -c "sin(" gms/hvycrash.gms; } > ../reviews/solver-analysis-r1/warnings.log
```

Inspection commands (read-only), run from `publication/solver-runs/`:

- `awk 'NR>=34' driver.log > /tmp/sar1_final.log`, then `grep -c`/`grep`
  for `end … attempt`, `valid True`, `start`, `signal`, `SIGTERM|SIGKILL`,
  `admit`, and `ERROR|abandon|removed|hard timeout|low cpu`.
- `ls runs_archive/*`.
- `gdxdump runs/camshape100__BARON/m_p.gdx dFormat=hexponential | head`.
- `grep`/`tail` on selected `gams.log` and `trace.trc` files (BARON
  time-limit summaries, GUROBI bound lines, the lukvle10 error).
- `grep -rn` of the certificate values in `open-instances-summary.md`,
  `open-instances-wave2/cops/report.md`, `reviews/cops-verification/`,
  `reviews/catmix-recheck.md`, `reviews/open-instances-verification/` and
  `publication/primal/water-ann-kan/report.md`.
- Inline `python3 -c` summaries of run.json load, memory and swap fields
  and of machine_load.csv.
- `git status --short` and `git log --oneline -3` on solver-runs.

Failures and fixes in my own code during the review:

- The first `compare.py` run counted MINLPLib "other"-section points as
  listed primals, which produced a spurious optcdeg2 mismatch. It also
  compared the model status as an int against a string. Both were fixed and
  the script was rerun.
- The first `pointcheck.py` run missed the second bound statement on lines
  like `x1.lo = 1; x1.up = …;`, so it reported bound violation 0 for
  camshape100/BARON. The regex was fixed and the script was rerun, giving
  9.997e-11.

These are targeted local checks only. No project-wide verification was run,
and CI was not consulted.
