# Prospective native-model computational results

The new holdout contains 30 models selected before implementation outcomes: ten convex, ten continuous nonconvex and ten integer nonconvex models. Previous failures and synthetic mechanisms are reported separately. All three modes share the same source-faithful model builder; the cut modes retain native nonlinear constraints and do not introduce feature graph equalities.

Application runs use a 30-second total soft budget and mechanism runs ten seconds. Root-only runs use five seconds and one node. Source loading and integration setup are charged to the soft budget; interpreter imports and independent checking are included in outer wall time. Runs are sequential with one solver and BLAS thread. The host also runs unrelated work, so timings are descriptive.

| Suite | Mode | Complete admitted records | Numerically solved | Recorded cuts | Cases with cuts | Integration seconds | Outer seconds |
|---|---|---:|---:|---:|---:|---:|---:|
| holdout | baseline | 30/30 | 25/30 | 0 | 0 | 170.57 | 197.30 |
| holdout | all | 30/30 | 25/30 | 38 | 7 | 187.02 | 213.20 |
| holdout | auto | 30/30 | 25/30 | 10 | 3 | 187.12 | 213.56 |
| diagnostic | baseline | 10/10 | 5/10 | 0 | 0 | 156.56 | 165.67 |
| diagnostic | all | 8/10 | 5/10 | 15 | 2 | 103.94 | 123.81 |
| diagnostic | auto | 8/10 | 5/10 | 5 | 1 | 103.45 | 123.32 |
| synthetic | baseline | 13/13 | 12/13 | 0 | 0 | 10.69 | 22.08 |
| synthetic | all | 13/13 | 12/13 | 13 | 4 | 10.86 | 22.06 |
| synthetic | auto | 13/13 | 12/13 | 2 | 1 | 10.69 | 21.87 |

Denominators retain every selected case, including importer rejection, worker failure and timeout. Complete admitted records count returned model metadata, so a missing record does not establish an importer refusal. The four original diagnostic worker errors occurred during discovery after successful model construction. Solved means optimal or gaplimit status with a returned incumbent that passed the independent numerical original-model checks.

| Suite | Mode versus baseline | Better final dual | Tie | Worse | Unavailable or flagged |
|---|---|---:|---:|---:|---:|
| holdout | all | 2 | 21 | 7 | 0 |
| holdout | auto | 2 | 24 | 4 | 0 |
| diagnostic | all | 1 | 5 | 2 | 2 |
| diagnostic | auto | 0 | 5 | 3 | 2 |
| synthetic | all | 1 | 11 | 1 | 0 |
| synthetic | auto | 1 | 11 | 1 | 0 |

Dual comparisons use tolerance 1e-6 times the larger bound scale. Any failed original-model primal check or dual/reference conflict is flagged and excluded from favorable comparisons; the raw record remains. The original-model checks use scaled tolerance 1e-5 for every row, variable bound, integrality condition, domain and objective. These checks do not certify SCIP's complete solve or dual bounds.

Independent replay results are reported separately and are required before claiming any saved added cut is certified. Missing cut logs mean unknown cut counts, not zero. Detailed statuses, rejected structures, soft-budget overshoots, paired root bounds, seed-1 repeats and instance-level comparisons are saved in summary.json; raw records, logs, exact source-model data and implementation snapshots are retained.

All phases contain 282 records and 123 recorded added cuts.
