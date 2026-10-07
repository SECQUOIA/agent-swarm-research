# Frozen short-run computational results

This experiment measures a bounded prototype under default native SCIP handling. All modes retain native nonlinear constraints. The held-out population was selected before new optimization outcomes and is separate from the synthetic and historical cases.

Each full run has a six-second soft budget including integration setup; root-only runs have two seconds and one node. Each cold worker is limited to 20 seconds and runs alone with one solver and BLAS thread. Interpreter startup and independent primal checks are recorded in outer wall time. Nonpreemptive setup or support calls may overshoot the soft budget; these are listed in summary.json. Missing worker cut logs mean unknown cut counts. Unrelated jobs share the host, so small time differences are descriptive.

| Suite | Mode | Numerically solved | Recorded cuts | Cases with recorded cuts | Integration seconds | Outer seconds |
|---|---|---:|---:|---:|---:|---:|
| synthetic | baseline | 12/13 | 0 | 0 | 6.57 | 16.94 |
| synthetic | control | 13/13 | 0 | 0 | 1.66 | 11.57 |
| synthetic | all | 13/13 | 89 | 7 | 2.51 | 13.18 |
| synthetic | auto | 13/13 | 72 | 7 | 2.45 | 13.14 |
| holdout | baseline | 19/24 | 0 | 0 | 17.40 | 36.66 |
| holdout | control | 19/24 | 0 | 0 | 20.66 | 40.12 |
| holdout | all | 18/24 | 230 | 12 | 25.41 | 45.44 |
| holdout | auto | 18/24 | 106 | 8 | 23.01 | 42.49 |
| historical | baseline | 0/4 | 0 | 0 | 6.22 | 9.60 |
| historical | control | 0/4 | 0 | 0 | 6.84 | 10.36 |
| historical | all | 0/4 | 24 | 1 | 6.91 | 10.41 |
| historical | auto | 0/4 | 24 | 1 | 6.88 | 10.26 |

Final dual-bound comparisons use tolerance 1e-6 times the larger bound scale. A record with a failed original-model primal check or a dual/reference conflict is flagged and excluded from favorable comparisons, while retained in the raw output.

| Suite | Mode versus baseline | Better | Tie | Worse | Unavailable or flagged |
|---|---|---:|---:|---:|---:|
| synthetic | control | 3 | 10 | 0 | 0 |
| synthetic | all | 2 | 9 | 2 | 0 |
| synthetic | auto | 2 | 9 | 2 | 0 |
| holdout | control | 1 | 15 | 4 | 4 |
| holdout | all | 1 | 14 | 5 | 4 |
| holdout | auto | 3 | 12 | 5 | 4 |
| historical | control | 0 | 0 | 1 | 3 |
| historical | all | 0 | 0 | 1 | 3 |
| historical | auto | 0 | 0 | 1 | 3 |

The independently evaluated original-model checks use scaled tolerance 1e-5. They test bounds, integrality, domains, objective and every original constraint. These numerical checks and the added-cut certificates do not certify SCIP's search or dual bounds.

Detailed instance comparisons, root results, repeats, negative outcomes, and caching/star ablations are in `summary.json`; raw records, exact model data, source snapshots and worker logs are retained in this campaign directory. The separate replay output is required to assess saved cut validity and model binding.

The `no_cache` ablation disables sample caching, support-point exchange, repeated-point skipping, and automatic screening together. Its outcomes cannot isolate the effect of caching alone. The optional native sampler has a separate kernel microbenchmark; these solver workers do not compile or load it.

There are 316 raw records and 1082 recorded added cuts across all phases.
