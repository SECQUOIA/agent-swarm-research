# Final solver campaign on the 43 paper instances

The campaign finished at **2026-10-03T13:33:28Z**. It contains 129 kept outcomes
(43 instances × three solvers), of which 126 satisfy the driver's measurement
rule. The other three are SCIP runs **stopped at the 8 GB memory limit**.
Their kept attempts retain final solver bounds, but they are not full-hour
measurements. No solver runs were launched during this analysis.

**Accepted closures within the one-hour solver budget: BARON 0, GUROBI 0,
SCIP 0.** BARON reports optimality on camshape100 and camshape200, but both
returned primal values are below the proved optima and both points violate
constraints. These two claims must be shown separately from accepted closures.
All 37 instances outside the six kan models remain unclosed by all three in
this campaign. All 43 lack an accepted campaign closure; calling all 43
“still open” would be wrong because the six original kan OSIL models are
proved exactly infeasible.

Our certificates close 31 instances under the source reports' stated primal
and gap conventions, substantially improve six others, and certify the
network relaxation R of six exactly infeasible kan models. The 109 finite
final solver dual values are all weaker than their corresponding certificate
values, **including six BARON values without a globality guarantee**
(catmix100/200/400/800, dtoc5 and optcdeg2). Separating these leaves 103
finite values without that warning: BARON 29, GUROBI 36 and SCIP 38.
Six of the SCIP values concern slightly tightened models, as explained below.
Of all 109 comparisons, 91 concern the original OSIL certificate and 18
concern the kan relaxation R only; excluding the six BARON disclaimers
leaves 85 and 18 respectively. These are solver-reported floating-point
values, not rigorous certificates. The comparison does not establish that the
instances remain open under other settings, longer runs or other solvers.

## Data and interpretation

[results_table.md](results_table.md) is the paper table; [results_table.csv](results_table.csv)
contains all 129 rows at their source decimal precision, including both
GAMS-returned primals and solver-log incumbents. [references.csv](references.csv)
and [references.json](references.json) record the certificate, reference
primal, exact/numerical status, listed best primal/dual and sources for all
43 instances. [reference_sources.json](reference_sources.json) freezes source
hashes. [inconsistencies.md](inconsistencies.md) and its CSV/JSON list every
forbidden-side primal difference, including printing-scale differences.

References use [open-instances-summary.md](../../open-instances-summary.md),
its linked reports and independent verifications. Grouped chain/catmix and
kan entries are expanded from their track files. Where a linked verifier
provides a stronger catmix bound or a better primal, that value is used and
identified. MINLPLib comparisons use the cached September 2026 per-instance
pages and `bound-audit/pages.json`, not the three-solver metadata bounds and
not an assumed live website state. Listed primal values can be rounded or
only tolerance feasible. A numerical improvement over them is not, by
itself, an exact-feasibility improvement.

All instances minimize except pricing050, which maximizes. With sign s = +1
for minimization and −1 for maximization, the table's dual deficit is
s(C−D), where C is our certificate and D is the final solver dual. Positive
means our certificate is stronger. The CSV also gives s(P−C), s(P_ref−P),
s(D−D_listed), and s(P_listed−P), with equivalent log-incumbent comparisons.
A negative primal-to-certificate gap is flagged. A positive dual-to-reference
primal excess would flag a cutoff of that reference; a numerical reference
alone would not prove the dual invalid. No such dual cutoff occurs here.

“Closes” means a measurement-valid run returning a global optimality claim
(GAMS model/solver status 1/1) within the 3600 s solver budget, consistent
with our certificates. Local optimality (model status 2) does not close an
instance. Even an accepted floating-point closure would not be a proof of
exact feasibility. For the two BARON claims, the solver's zero gap is
inconsistent with the certified optimum interval. Their objective deficits
are 5.2581469e-7 (camshape100) and 2.05270746e-6 (camshape200), much larger
than the requested 1e-9 absolute/relative gap. They are nevertheless within
MINLPLib's looser 1e-6 relative convention. That convention does not make the
returned points exactly feasible, so the table excludes both claims.

## Versions, models and settings

- GAMS 54.3.1, build 61154be4, Linux x86-64.
- BARON 26.5.27 (the BARON 26.5 release), built 2026-05-27.
- GUROBI 13.0.2, build v13.0.2rc1.
- SCIP 10.0.3, commit d409edf9f6; CPLEX 22.1.2.0 LP solver, Ipopt 3.14.19,
  CONOPT 4.39.1 and PaPILO 3.0.1.

The machine is a shared Intel Xeon w5-2565X, 18 physical cores / 36 hardware
threads, about 47 GB RAM and 16 GB swap. There are 29 NLP and 14 MINLP GAMS
solve statements. Files are the unmodified downloaded MINLPLib GAMS models.
Review round 1 independently checked all 43 against the cached OSIL models:
exact names, types, bounds and senses, plus numerical agreement of functions
at random points. That is strong numerical model-equivalence evidence, not
an algebraic proof. It also verified hashes and option echoes. pricing050's
header nonlinear-nonzero count (295 versus generated 249) is a counting
convention, not a model discrepancy.

Every production job used this command, with its model type and solver:

```sh
cd runs/<instance>__<solver>
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  gams <absolute-path>/gms/<instance>.gms <TYPE>=<SOLVER> \
  reslim=3600 threads=1 optcr=1e-9 optca=1e-9 lo=2 \
  logfile=gams.log o=<instance>.lst savepoint=1 trace=trace.trc traceopt=3
```

There were no solver option files. GUROBI and SCIP use wall-clock time;
BARON with one thread uses CPU time, so its wall time can exceed one hour.
Time in the paper table is GAMS solver time (`resusd`); for BARON this is
wall clock, while its limit is CPU time. The four BARON overruns are
3706.37 s (dtoc5), 3708.98 s (kan_r3_h1_n9), 3709.5 s (waterno2_24) and
3728.4 s (optcdeg2), up to 128.4 s or 3.57% beyond 3600 s. BARON's own
CPU times for those runs are 3600.01–3601.65 s. Wall and process-group CPU
time remain separate CSV columns; values are reported as measured. GAMS startup,
cleanup, solver accounting and the five-second monitor also affect timing.
One-thread settings and log evidence do not guarantee isolated-core speed.

## Admission, validity and archive

The driver allowed at most 10 simultaneous runs. A new run was admitted
only at load1 ≤ 30 and MemAvailable ≥ 8 GB; waits and admission conditions
are logged. This admission test did not keep MemAvailable above 8 GB during
runs. In particular, the first ten starts filled all slots within one second
at load1 29.9 and MemAvailable about 12.4 GB, before the load average reflected
their work. Their overload and memory pressure are disclosed per row and in
the shared-machine limitations below. This revision used a two-core affinity
limit and one thread per numerical library; it did not start the driver.

The monitor sampled every five seconds. The per-run cap counts resident
plus swapped memory, with a threshold of 8192 MiB (called “8 GB” by the
driver). The old machine-memory-floor kill rule was removed. The hard
wall timeout is 4200 s. SIGINT goes to the busiest process in the run's
group, usually the solver, because SIGINT to the whole group could destroy
GUROBI's return to GAMS. After 300 s it escalates to group SIGTERM, then
SIGKILL after another 30 s. A solver may fail to return a trace, final
summary or savepoint; graceful return is not guaranteed. In the final
campaign, all 129 kept outcomes have trace records, the three memory stops
returned with user-interrupt status 8, and none required escalation or a
hard timeout.

An attempt passes the measurement rule if it ends on its own or at the
hard timeout and process-group CPU/wall ≥ 0.9. Own completions within 60 s,
other than resource interrupts, are exempt from the ratio test; this covers
fast capability failures as well as the two BARON optimality claims. CPU
time is the maximum of wait4 accounting and sampled whole-group /proc CPU
time. Thus `valid=true` means measurement-valid, not a mathematically valid
solution or bound; even the GUROBI interface failure is measurement-valid.

An attempt can be interrupted early if its accumulated CPU deficit makes
0.9 unreachable under the driver's conservative prediction:
`(cpu + 10 + 1.02*(4530-wall))/4530 < 0.9`. Invalid attempts are archived and
requeued up to two times. After three attempts the driver keeps the attempt
ranked first by proper end, then trace presence, then highest CPU/wall.
“Best” here does **not** mean strongest dual or best incumbent. A driver stop
abandons unfinished attempts without spending retries. The final collector
uses `runs/`, never mixes it with archives, and preserves invalid flags.

The history matters:

- Driver 1 (PID 143593) started 2026-10-02T03:15:35Z. Its low-CPU-share
  results and the lost optcdeg2/SCIP run are in `runs_archive/driver1/` and
  excluded. optcdeg2/SCIP was redone and now has a final bound
  200.133567479732, no returned primal, and a valid time measurement.
- Driver 2 launch 1 (PID 819808) started 2026-10-02T22:56:11Z and was stopped
  after other jobs increased load and swap. Its ten abandoned folders are
  in `runs_archive/driver2_launch1_stopped/` and excluded.
- The final launch (PID 898862) started 2026-10-02T23:45:08Z, waited about
  4262 s, admitted its first jobs at 2026-10-03T00:56:08Z and ended
  2026-10-03T13:33:28Z. It completed 135 attempts: 126 passing attempts plus
  nine memory-cap attempts for three pairs. `runs/` contains 129 outcomes;
  `runs_archive/attempts/` contains the nine failed attempts, including the
  three attempts copied back as kept outcomes. Do not add those copies to
  the kept-row count. `attempts.csv` and `.json` collect the archive alone.

## Final results

| Solver | Passing measurements | Finite final duals | Returned primals | Raw optimality claims | Accepted closures | Capability failures | Other failures | Memory stops |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BARON | 43 | 35 (6 without globality guarantee) | 35 | 2 | 0 | 8 | 0 | 0 |
| GUROBI | 43 | 36 | 40 | 0 | 0 | 0 | 1 | 0 |
| SCIP | 40 | 38 | 30 | 0 | 0 | 1 | 0 | 3 |

The finite-dual and returned-primal counts include the kept memory-stop
outcomes; passing measurements exclude them. “No solution returned” means
no incumbent usable as a primal, not a proof of infeasibility. Placeholder
GAMS objectives (for example GUROBI's 0.02 on optcdeg2) are retained only
as raw data in `results.csv`, never as feasible primal values.

Only five final duals improve MINLPLib's listed best dual: BARON on
camshape100, camshape200 and camshape400; GUROBI on lnts200; SCIP on
waterno2_18. All five remain weaker than our certificates. Many listed
bounds are stronger than these one-hour runs; historical listed bounds
are not a matched runtime baseline. GUROBI has no finite final bound on
ann_cumene_tanh, all four catmix models or etamac. SCIP has no finite final
bound on all four catmix models. BARON reports 35 finite values on the
models it accepts; six carry its own warning, “Globality is therefore not
guaranteed”, because appropriate variable bounds were not provided.
Those 35 values split into 29 without
this disclaimer and six with it. **No solver supplies a finite catmix bound
with an unqualified globality claim.** There is no certificate-consistent closure.

SCIP tightened log/pow argument lower bounds to 1e-9 on ex6_2_5, ex6_2_7,
etamac, hvycrash, lukvle10 and pindyck. Its six finite dual values there concern
a slightly tightened model; they are all weaker than the corresponding
certificates. These qualifications change the interpretation of the finite
values, not the raw counts or comparison conclusions.

The waterno2 and ANN comparison is particularly clear:

| Instance | Our certificate | Strongest campaign dual | Solver | Reference primal |
|---|---:|---:|---|---:|
| waterno2_06 | 278.230573 | 142.831148612344 | GUROBI | 282.8880374 |
| waterno2_09 | 824.834692 | 220.683687371791 | GUROBI | 914.011970350 |
| waterno2_12 | 2089.754565 | 454.55506441964 | GUROBI | 2233.821335282 |
| waterno2_18 | 4790.820715 | 891.934497969825 | SCIP | 5023.982735143 |
| waterno2_24 | 6576.151388 | 1074.43904635414 | SCIP | 6963.795154460 |
| ann_cumene_tanh | -3386.5403 | no finite bound | — | -3379.9823940717715481 |

These comparisons use the finished campaign, not the rejected first launch.
GUROBI's returned primals on waterno2_09, waterno2_12 and waterno2_24 improve
MINLPLib's listed best primals by 2.604794556432, 1.12727833282 and
37.70136730126 respectively. They remain worse than our reference primals.
Their available savepoints were checked at 50 digits in this revision:

| GUROBI point | Returned primal | Listed best primal | Maximum violation | Worst row |
|---|---:|---:|---:|---|
| waterno2_09 | 919.990495243568 | 922.5952898 | 9.999939745976e-7 | e144 |
| waterno2_12 | 2262.23109566718 | 2263.358374 | 6.668760743622e-7 | e200 |
| waterno2_24 | 7295.02032369874 | 7332.721691 | 9.222574349714e-7 | e2022 |

Maximum violation includes row, variable-bound and integrality violations;
the worst violation in each case is a row violation. No domain error or
unknown variable occurred. These are numerical evidence of small
infeasibilities, not exact-feasibility certificates or repairs. GUROBI's
waterno2_06 point remains unchecked. The chain and catmix families likewise have large final dual deficits even
where solver primals are close to our reference values. The eg solvers do
not close any of the three small MINLPs; even the near-optimal BARON primal
on eg_int_s leaves a large dual gap.
GUROBI's eg_int_s log explicitly warns that its maximum constraint violation
5.9580e-5 exceeds its own tolerance. The table labels that returned point
accordingly rather than presenting a bare feasible-point claim.

## The three memory-cap outcomes

Each pair hit the cap on all three attempts. We retain the last final bound
reported by the **kept attempt**, not the strongest bound over retries or a
progress-table bound. All three ended with GAMS solver status 8; pindyck
has model status 14 and no returned primal. These rows remain flagged
`valid=false` and cannot be described as full one-hour SCIP runs.

| Instance / SCIP | Kept attempt | Solver time (s) | Wall time (s) | Returned primal | Final bound |
|---|---:|---:|---:|---:|---:|
| ex6_2_5 | 1 / 3 | 1515.639 | 1534.12 | -70.7184889007037 | -592.077342771028 |
| ex6_2_7 | 1 / 3 | 1962.771 | 1986.33 | -0.160846800069042 | -1.42171210528426 |
| pindyck | 2 / 3 | 2546.128 | 2566.0 | none | -1625.39840602367 |

The kept ex6_2_5 attempt reached 8209 MiB RSS+swap, ex6_2_7 8196 MiB,
and pindyck 8195 MiB when interrupted. Monitoring and shutdown allow a
small overshoot. No attempt was rerun during this analysis, and no further
runs are proposed as part of this completed task.

## Capability and interface failures

- BARON rejects sin and cos on **lnts50, lnts100, lnts200, lnts400,
  powerflow0030p and powerflow0039p**, and cos on **hvycrash**, whose model
  contains no sin. These seven rows have model/solver
  status 14/6 and zero solver time. BARON also rejects tanh on
  ann_cumene_tanh, for eight capability failures in total.
- SCIP rejects tanh on ann_cumene_tanh (14/6). GUROBI accepts the unchanged
  model, returns a primal −3379.98236532438, but no finite dual bound.
- GUROBI fails immediately on lukvle10 with error 10024: “In a nonlinear
  expression POW should have at least one constant argument.” The GAMS
  result is 13/13. This is an interface/model-expression failure, not an
  OOM outcome or a time-limit failure; the log identifies its cause.

No functions were rewritten, unsupported models were not replaced by
surrogates, and failures remain in the 43-instance denominator.

## Inconsistencies and cheap feasibility checks

There are 36 returned-primal forbidden-side flags and 38 solver-log
incumbent flags on 39 distinct instance/solver pairs. These are overlapping
observations, not 74 independent errors. Of the 36 returned-primal flags,
five compare only with R, one (GUROBI/pindyck, margin 1.3836068e-12) is
within the trace's ±5e-12 printing uncertainty, and 30 are beyond printing
precision for the OSIL certificates. No final dual is beyond a reference
primal. [inconsistencies.md](inconsistencies.md) gives the complete list,
including three log-only flags on SCIP chain100, SCIP chain400 and
GUROBI ex6_2_5 where a GAMS returned point differs from the solver incumbent.

Eighteen selected savepoints were checked sequentially at 50 decimal digits,
including the three GUROBI waterno2 points added in this revision.
`gdxdump ... dFormat=hexponential` supplies exact binary64 levels; the script
converts them to exact decimal values and evaluates the cached decimal OSIL
model, including objective/row constants, variable bounds and integrality.
All 18 selected points have positive row violations. This is high-precision
numerical evidence of infeasibility, not an interval proof of the residual
or an exact-feasibility repair. [point_checks.json](point_checks.json) stores
objectives, worst rows, row/bound/integrality residuals and domain errors.
The checked GAMS point does not stand in for an unavailable log-incumbent
vector.

| Point | Primal beyond certificate | Maximum row violation | Row |
|---|---:|---:|---|
| BARON camshape100 | 5.2581469e-7 | 9.99500391848e-11 | e100 |
| BARON camshape200 | 2.05270746e-6 | 9.99746102410e-11 | e200 |
| BARON camshape400 | 8.15450068e-6 | 9.99876456213e-11 | e400 |
| BARON camshape800 | 0.09365569719715 | 3.31426311075e-7 | e2 |
| GUROBI camshape800 | 0.02328447110410 | 9.74737313199e-7 | e58 |
| GUROBI powerflow0039p | 0.00124788354 | 6.81076174112e-7 | e73 |
| GUROBI chain50 | 2.01996813e-7 | 6.69328240306e-8 | e52 |
| BARON pricing050 (max) | 1.0463230577e-6 | 3.41130497708e-7 | e6 |
| SCIP pricing050 (max) | 4.500930577e-7 | 1.22469101952e-7 | e5 |

The largest objective discrepancies arise from small row violations in
sensitive models. They do not establish a new dual-bound defect. The
camshape400 behavior matches the known infeasible MINLPLib p2 point;
the two camshape optimality claims and the large camshape800 deviations
are new observations from this campaign, consistent with the known
feasibility-tolerance issue. Other checked points (SCIP camshape100,
BARON/GUROBI etamac, BARON pindyck and two kan points) show the same general
problem. Unchecked discrepancies remain explicitly unresolved as to the
returned vector; the certificate already rules out exact feasibility if
the printed objective is accurate beyond its printing uncertainty.

The separate [SCIP bug report](../scip-bug/report.md) proves invalid cutoffs
on waterno2 period subproblems caused by nonlinear propagation of rounded
cube identities. That specific defect is **not demonstrated by this
whole-instance campaign**: SCIP claims no waterno2 optimum, returns no
waterno2 primal, and its final bounds are well below our certificates.
These outcomes do not exclude an internal bad cutoff. Our rigorous
certificates do not use these solver bounds. The broader
[bound audit](../../bound-audit/audit-report.md) also distinguishes invalid
duals from tolerance-feasible primals; this campaign provides the latter
kind of evidence, with no new proven invalid dual.

## Shared-machine limits

For valid runs longer than 60 s, measured CPU/wall ranges are BARON
0.9645–0.9998, GUROBI 0.9749–1.0051 and SCIP 0.9561–0.9998. Process-group
CPU time ranges are 3600.66–3610.83 s, 3517.68–3620.47 s and
3457.69–3612.73 s respectively. The final long runs all exceed the 0.9
rule; no low-CPU-share retry was needed. This fixes the first launch's
0.65–0.72 CPU-share problem but does not create an isolated-core benchmark.

The first admitted batch started at **2026-10-03T00:56:09Z** and finished
between 01:56:11Z and 01:58:31Z. It comprised dtoc5, optcdeg2 and waterno2_24
for all three solvers, plus kan_r3_h1_n9/BARON. Load rose to 47–51 on 36
hardware threads (sampled maximum 50.95); per-run metadata record
MemAvailable as low as 1.06 GB and machine swap up to 6.6 GB. Our groups
held up to 3.8 GB of swap in the machine samples. Mean load for these runs
was 33.0–33.6, versus a median 11.4 for the other long runs. Their CPU/wall
ratios, 0.9561–0.9811, are the ten lowest among all 117 long kept runs;
every other long run has ratio at least 0.9991. All four BARON wall-time
overruns and all three solvers' largest group-swap peaks occurred in this
batch. Admission control checked lagging load and memory before starts;
it did not prevent subsequent overload or preserve the 8 GB memory floor.

All ten runs passed the stated measurement validity rule. Their time
comparisons need this batch-specific limitation. The bound conclusions do
not depend on these timings or runs: our certificates are independent,
every finite campaign dual value is weaker, no campaign dual cuts off a
reference primal, and removing these ten outcomes leaves those comparisons
unchanged. No rerun was performed or proposed.

Peak per-group swap reached 613.4 MiB (BARON), 655.1 MiB (GUROBI), and
1088.4 MiB (SCIP). Swap and busy hyperthread siblings may still reduce
work per CPU-second. CPU/wall is a scheduling measure, not a speed measure,
and need not catch every memory-pressure effect. Preserve per-run CPU
seconds, mean load and swap columns and `machine_load.csv` when using these
results. The defensible statement is performance under this documented
shared-machine protocol, not what each solver achieves on a quiet machine.

## Response to review round 1

This section responds to the independent [solver-analysis review round 1](../reviews/solver-analysis-review-r1.md).
I checked its evidence against the raw logs, traces, run metadata, machine
samples and models before changing the analysis. [review_r1_evidence.json](review_r1_evidence.json)
and [review_r1_evidence.log](review_r1_evidence.log) record the checks.

| Issue | Resolution |
|---|---|
| Major 1: six BARON values lack a globality guarantee | Collector detects the warning; raw CSV/JSON and paper CSV/table flag all six. The headline remains 109 finite values, of which six are disclaimed; the other 103 split 29/36/38. All catmix statements reflect the disclaimer. |
| Major 2: overloaded first batch | Collector identifies all ten starts from driver PID and timestamp; CSV/table flag each row. Admission and limitations disclose the batch window, load, memory, swap, ratios and overruns. All ten passed the validity rule; bound conclusions do not depend on them. No experiments were repeated. |
| Minor 3: understated BARON wall overruns | Report and table definition give all four times, up to 3728.4 s, and distinguish BARON's CPU limit from reported wall time. |
| Minor 4: GUROBI and SCIP warnings | GUROBI eg_int_s has an explicit tolerance-warning status and 5.9580e-5 note. All six SCIP rows flag log/pow argument lower bounds tightened to 1e-9 and the resulting model scope. |
| Minor 5: waterno2 primal improvements | Report and rows give all three improvements. Existing savepoints checked at 50 digits; maximum violations and worst rows reported above and in point_checks.json. These points are numerically infeasible. waterno2_06 remains unchecked. |
| Minor 6: hvycrash capability wording | Report, README and generated table distinguish hvycrash's cos-only failure from the six sin/cos failures. |

I agree with all six requested fixes and the review's headline counts.
Two small evidence details are corrected: the median mean load of the
other long kept runs is 11.4, not 12.2; ex6_2_5's log argument bound was
raised from 9.9e-10, rather than zero or a negative value, to 1e-9.
Neither correction changes the review's findings.

## Response to earlier campaign review round 1 and partial round 2

| Review item | Final treatment / evidence |
|---|---|
| M1: lost optcdeg2/SCIP, incorrect CPU accounting, overconfident SIGINT claim | Old launch excluded; final optcdeg2/SCIP redone, valid, final bound retained. CPU uses whole-group samples plus wait4. Missing traces cannot confirm threads. Graceful return is qualified, with solver-only SIGINT and escalation. |
| M2: loaded machine and unrecorded swap | Rejected launch archived; admission and explicit CPU validity rule added; final CPU/wall and CPU-second ranges, per-run load/swap, and remaining hardware-sharing caveat reported. No isolated-core claim. |
| Minor 1: optimistic completion estimate | Forecast removed; actual final timestamps and 135 attempts reported. |
| Minor 2: RSS cap misses swapped pages | Cap uses RSS+swap; swap columns retained. |
| Minor 3: BARON progress regex misses '+' and NA | Existing collector fix retained; final results use trace/final summary, never low-precision progress as a final bound. |
| Minor 4: GUROBI fallback precision | Existing 13-digit source and half-unit columns retained; source decimal arithmetic used; no precision-free claims. |
| Minor 5: returned point differs from SCIP incumbent | Both objectives preserved and compared; 16 rows differ beyond source printing (12 SCIP, 4 GUROBI); GDX checks use the returned point only. |
| Minor 6: tanh unsupported | Failures explicitly retained; GUROBI's no-finite-bound outcome shown; no rewritten model runs. |
| Minor 7: missing report and commands | Final report and reproduction commands written; predecessor command records preserved in report.prev.md and report.running.md, clearly historical. |

Round-2 `reviews/solver-campaign-r2/PROGRESS.json` contains a reading-state
placeholder with no completed checks, findings or verdict. It is not an
independent endorsement of the relaunch. This analysis inspected final
artifacts and ran the targeted checks below; it did not restart those
review tasks or run their solver tests.

## Reproduction and commands actually run

For this solver-analysis review revision, the following exact commands ran
from `research-20260929/publication/solver-runs/`. CPU affinity was limited
to cores 0 and 1 and numerical libraries to one thread. No command invokes
a solver; `gdxdump`, called by the point checker, only reads savepoints.

```sh
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 review_r1_check.py > review_r1_evidence.log
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 collect.py --help > analysis-collect-help.txt
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 collect.py > collect.log
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 collect.py --runs runs_archive/attempts --out attempts > collect-attempts.log
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 check_points.py > point_checks.log
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 analyze.py > analyze.log
OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 taskset -c 0,1 python3 verify_analysis.py > verification.log
```

Final executions all exited 0: evidence agrees with all 129 independent
review primal/dual/status rows; collection produced 129 kept and nine
archived rows; point checks covered 18 savepoints; regenerated analysis and
targeted verification confirmed 129 outcomes, 126 valid measurements,
35/36/38 finite dual values, 35/40/30 returned primals, two contradicted
optimality claims, zero accepted closures, five listed-dual improvements,
and 36 returned/38 log primal flags on 39 pairs. There is still no
certificate-beating finite dual or reference-primal cutoff. Six BARON
values are now explicitly separated; all warning and batch flags are
verified from raw artifacts. The reference and model hashes are unchanged.

The evidence script was run before edits and again after regeneration.
Its first run failed because short capability runs have no mean load;
the median now uses other long runs. A later numerical-agreement check
initially compared integer statuses with the review's string statuses;
explicit conversion fixed it. The verifier was once started before the
table regeneration had completed and failed on the missing new column;
it passed after regeneration. These were analysis-check failures; no
solver or campaign artifact was changed. One documentation patch referenced
a nonexistent context line and was corrected before application.

From the repository root, the final whitespace check was:

```sh
git diff --check -- research-20260929/publication/solver-runs/collect.py research-20260929/publication/solver-runs/README.md research-20260929/publication/solver-runs/report.md research-20260929/publication/solver-runs/PROGRESS.json
```

It exited 0. An earlier `git diff --check -- research-20260929/publication/solver-runs/`
reported existing trailing whitespace in raw solver logs; those logs were
not edited. The final check targets the revised tracked code and documents.
Read-only evidence inspection used `cat`, `sed`, `rg`, `ls`,
`git status --short` and inline Python summaries; it included the reviewer's
code/logs, all relevant raw warnings, first-batch metadata, machine samples,
capability messages and savepoint presence. The calculation of the other
long-run median used `taskset -c 0,1 python3 -` with an inline JSON summary.
Only targeted local verification ran. CI and project-wide checks were not
inspected or run.

The commands below record the **initial analysis**, before this revision.
From `research-20260929/publication/solver-runs/`, the completed campaign
can be analyzed without running a solver:

```sh
python3 collect.py --help > analysis-collect-help.txt
python3 collect.py > collect.log
python3 collect.py --runs runs_archive/attempts --out attempts > collect-attempts.log
PYTHONDONTWRITEBYTECODE=1 python3 build_references.py
PYTHONDONTWRITEBYTECODE=1 python3 check_points.py > point_checks.log
PYTHONDONTWRITEBYTECODE=1 python3 analyze.py > analyze.log
PYTHONDONTWRITEBYTECODE=1 python3 verify_analysis.py > verification.log
```

In the initial analysis the collector was read before invocation and not
changed; this revision adds the warning and batch fields described above. The first
three commands succeeded: 129 finished kept rows and nine archived rows.
Reference generation succeeded for 43 instances, including the more precise
waterno2 and ANN primals in the linked reports. The point-check script's
first two attempts failed on GDX text syntax (lowercase padded variable
type, then a trailing comma on the level token); those parsing errors were
fixed, and the final command succeeded for all 15 points. Analysis succeeded
for all 129 rows. The final verification result is in `verification.log`.
Reference generation and the final two analysis commands were repeated
after analysis-script edits. `verify_analysis.py` also confirmed all 86
GAMS/OSIL hashes against the campaign manifest.
`git diff --check -- research-20260929/publication/solver-runs/README.md
research-20260929/publication/solver-runs/report.md
research-20260929/publication/solver-runs/PROGRESS.json` passed from the
repository root. `ps -p 898862 -o pid=,stat=,etime=,cmd=` returned no row
(exit 1), confirming that the historical driver PID is no longer present.

Read-only inspection used `cat`, `sed`, `rg`, inline Python JSON/CSV
summaries, `command -v gdxdump` and selected `gdxdump ...
dFormat=hexponential` output. One exploratory summary failed converting an
empty solver-time field for a capability outcome; it did not change any
result file. An `rg` inspection referenced nonexistent optional paths; the
actual source paths were then located. These are inspection failures,
not campaign outcomes.

For a historical rerun, the production launch was:

```sh
setsid nohup python3 driver.py >> driver.out 2>&1 < /dev/null &
```

That command is recorded for reproducibility and was **not executed in this
analysis**. Model downloads and the original smoke/guard/restart commands,
with their outcomes, remain in `report.prev.md`; the relaunch changes and
its targeted test commands remain in `report.running.md`. They are previous
authors' work, not checks run here. No project-wide verification was run,
CI status/logs were not inspected, and no external contacts were made.

## Remaining limits

No new solver experiment, exact repair or upstream report is needed to
complete this requested analysis. Unchecked primal vectors, exact
feasibility of the numerical reference primals, internal manifestations of
the known SCIP defect, and performance on an isolated machine remain
unresolved. They limit the paper's wording, not the completeness of the
reported campaign. There are no analysis background jobs.
