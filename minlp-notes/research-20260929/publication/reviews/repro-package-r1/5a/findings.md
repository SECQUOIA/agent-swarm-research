# 5a: water-audit display rerun, 80/12/1 versus 84/8/1

Written by the main reviewer from the delegated agent's returned result (the
agent could not write this file). The scratch runs are in `scratch/`. The
reviewer reran `check_display.py` in both scratch copies:
- `scratch/committed` gives `ok 84, failed 8, skipped 1`;
- `scratch/rerun` gives `ok 80, failed 12, skipped 1`.

## Cause

`bound-audit/check_display.py` and `bound-audit/audit-report.md` are the same
in the clean worktree used for the rerun (c3514f03e), HEAD and the working
tree. Neither patch touches `bound-audit/`.

The difference comes from the inputs. The water-audit chain
(`publication/reproduction/water-audit/tools/chain_c.sh`) regenerated
`results.json`, `summary.json` and the tables before running the checker, by
rerunning `cert_topopt.py` for p4/p5 and then `audit.py classify`. Only the
topopt records changed.

The two p5 points differ because `cert_topopt.py` chooses its basis with
QR column pivoting (`scipy.linalg.qr(..., pivoting=True)`). The pivot order
depends on the BLAS thread count.

| p5 point | obj_lo | inside the report's [10.33547432780, 10.33547432781]? |
|---|---|---|
| committed | 10.335474327803234… | yes |
| rerun (1 thread, reproduced exactly) | 10.33547432783171797… | no (+2.85e-11) |
| 2 threads | 10.33547432780663… | yes |

All three points are proved exactly feasible. The class, margins and verdict
do not change. p4 moves by only 7.4e-14 and still fits its interval.

## The four checks that flip

All four are the topopt p5 interval `[10.33547432780, 10.33547432781]` in
`audit-report.md`, at lines 94, 217, 550 and 805. Each is correct for the
committed certificate `logs/cert_topopt_topopt-cantilever_60x40_50.p5.json`.

## The other eight printed failures

All eight are quotations of other verifiers' or older values, which the report
itself explains at lines 1167–1170:
- line 797: emfl050_3_3;
- line 807: glider100;
- lines 843, 845 and 847: emfl050_5_5, emfl100_3_3, emfl100_5_5;
- line 959: ghg_3veh, the recheck's inward suggestion;
- line 993: emfl100_5_5, the old display;
- line 803: the verifier's nd_netgen value.

The single skip is line 158 (`≥ 0.1`, a histogram row).

## Verdict

84/8/1 is correct for the current audit report and its committed evidence.
**The audit report needs no correction.**

The package README should explain the cause. A rerun of `cert_topopt.py`
(with `OMP_NUM_THREADS=1`, as the README prescribes) gives a different valid
p5 point, so the four p5 displays then fail.
