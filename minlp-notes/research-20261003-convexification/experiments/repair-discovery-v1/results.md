# Corrected discovery: matched regression results

This cohort was selected because the original campaign exposed a discovery error or exceeded its existing discovery budget. It is not a new prospective holdout. All original records remain in campaign-v2, including the four failed workers and their unknown cut logs. The corrected implementation has its own source snapshot, matched baselines, unchanged models, seeds and budgets.

| Phase | Population | Mode | Numerically solved | Recorded cuts | Integration seconds | Discovery seconds | Incomplete discovery |
|---|---|---|---:|---:|---:|---:|---:|
| full | holdout | baseline | 4/8 | 0 | 123.913 | 0.000 | 0 |
| full | holdout | all | 4/8 | 12 | 124.856 | 1.332 | 0 |
| full | holdout | auto | 4/8 | 3 | 124.819 | 1.324 | 0 |
| full | diagnostic | baseline | 4/7 | 0 | 96.348 | 0.000 | 0 |
| full | diagnostic | all | 4/7 | 10 | 95.496 | 2.852 | 2 |
| full | diagnostic | auto | 4/7 | 0 | 96.718 | 2.900 | 2 |
| root | holdout | baseline | 0/9 | 0 | 5.854 | 0.000 | 0 |
| root | holdout | all | 0/9 | 11 | 7.020 | 0.981 | 1 |
| root | holdout | auto | 0/9 | 3 | 7.270 | 0.978 | 1 |
| repeat | holdout | baseline | 1/1 | 0 | 1.296 | 0.000 | 0 |
| repeat | holdout | all | 1/1 | 3 | 1.913 | 0.147 | 0 |
| repeat | holdout | auto | 1/1 | 0 | 1.450 | 0.140 | 0 |

| Phase | Population | Mode versus matched baseline | Better final dual | Tie | Worse | Unavailable or flagged |
|---|---|---|---:|---:|---:|---:|
| full | holdout | all | 0 | 5 | 3 | 0 |
| full | holdout | auto | 0 | 6 | 2 | 0 |
| full | diagnostic | all | 0 | 6 | 1 | 0 |
| full | diagnostic | auto | 0 | 6 | 1 | 0 |
| root | holdout | all | 0 | 9 | 0 | 0 |
| root | holdout | auto | 0 | 9 | 0 | 0 |
| repeat | holdout | all | 0 | 1 | 0 | 0 |
| repeat | holdout | auto | 0 | 1 | 0 | 0 |

Discovery now stops at deadline checks between units of work. An incomplete discovery is discarded, and native SCIP continues. A single nonpreemptive operation can still overshoot a soft deadline; every measured excess is listed in repair-summary.json. These checks provide a bounded fallback, not a hard real-time guarantee.

There are 75 records, 42 recorded cuts, 67 returned-incumbent checks and 0 unknown cut logs. Independent replay and metric audit are separate artifacts; numerical incumbent checks and cut certificates do not certify the complete SCIP solve.
