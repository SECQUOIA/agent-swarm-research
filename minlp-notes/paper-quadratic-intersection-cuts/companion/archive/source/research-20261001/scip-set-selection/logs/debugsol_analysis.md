# Archived debug-solution audit

Reference-bound threshold: 1e-6 max(1, |MINLPLib reference|), with objective sense accounted for. Row counts count explicit diagnostic messages, including any repeated row. Final/root bounds use statistics in the original objective; internal debug warnings use the objective of the point actually loaded by the checker.

## debugsol

300 runs; limits {'30': 300}; return codes {'0': 299, '255': 1}.
Non-run artifacts: run_chunk00.log, run_chunk01.log, run_chunk02.log, run_chunk03.log, run_chunk04.log, run_chunk05.log
Statuses: {'solving was interrupted [time limit reached]': 129, 'problem is solved [optimal solution found]': 170, None: 1}

| setting | runs | intersection row messages / runs | other row messages / runs | global objective warnings / runs | local objective warnings / runs | node cutoff messages / runs | any ERROR runs | rc not 0 | final dual excludes reference | root dual excludes reference |
|---|---|---|---|---|---|---|---|---|---|---|
| scip | 60 | 17 / 1 | 3 / 1 | 24125 / 5 | 40 / 6 | 52 / 6 | 9 | 0 | 0 | 0 |
| corner | 60 | 19 / 1 | 2 / 1 | 24270 / 5 | 45 / 6 | 46 / 6 | 9 | 0 | 0 | 0 |
| eff | 60 | 9 / 1 | 1 / 1 | 20507 / 5 | 42 / 6 | 38 / 4 | 8 | 1 | 0 | 0 |
| cornerS | 60 | 19 / 1 | 2 / 1 | 25005 / 5 | 45 / 5 | 47 / 6 | 9 | 0 | 0 | 0 |
| effS | 60 | 9 / 1 | 1 / 1 | 20792 / 5 | 57 / 6 | 64 / 7 | 10 | 0 | 0 | 0 |

### Runs with diagnostics or reference flags

| log | diagnostic message counts | reference flags | rc |
|---|---|---|---|
| carton9.corner.s0.log | {'variable_bound': 172} | [] | 0 |
| carton9.cornerS.s0.log | {'variable_bound': 172} | [] | 0 |
| carton9.eff.s0.log | {'variable_bound': 172} | [] | 0 |
| carton9.effS.s0.log | {'variable_bound': 172} | [] | 0 |
| carton9.scip.s0.log | {'variable_bound': 172} | [] | 0 |
| ex5_2_5.corner.s0.log | {'variable_bound': 1, 'global_objective_bound': 17387, 'local_objective_bound': 7} | [] | 0 |
| ex5_2_5.cornerS.s0.log | {'variable_bound': 1, 'global_objective_bound': 16390, 'local_objective_bound': 7} | [] | 0 |
| ex5_2_5.eff.s0.log | {'variable_bound': 1, 'global_objective_bound': 15399, 'local_objective_bound': 7, 'other_error': 1} | [] | 0 |
| ex5_2_5.effS.s0.log | {'variable_bound': 1, 'global_objective_bound': 14952, 'local_objective_bound': 7, 'other_error': 1} | [] | 0 |
| ex5_2_5.scip.s0.log | {'variable_bound': 1, 'global_objective_bound': 18109, 'local_objective_bound': 4} | [] | 0 |
| ex5_4_2.eff.s0.log | {'local_objective_bound': 1, 'other_error': 9} | [] | 255 |
| gasprod_sarawak01.corner.s0.log | {'global_objective_bound': 2019, 'local_objective_bound': 3, 'node_cutoff': 5} | [] | 0 |
| gasprod_sarawak01.cornerS.s0.log | {'global_objective_bound': 1892, 'local_objective_bound': 9, 'node_cutoff': 11} | [] | 0 |
| gasprod_sarawak01.eff.s0.log | {'global_objective_bound': 796, 'local_objective_bound': 5, 'variable_bound': 13, 'node_cutoff': 6} | [] | 0 |
| gasprod_sarawak01.effS.s0.log | {'global_objective_bound': 2162, 'local_objective_bound': 15, 'node_cutoff': 17, 'variable_bound': 21} | [] | 0 |
| gasprod_sarawak01.scip.s0.log | {'global_objective_bound': 1237, 'local_objective_bound': 4, 'node_cutoff': 5, 'variable_bound': 35} | [] | 0 |
| genpooling_lee2.corner.s0.log | {'local_objective_bound': 1, 'node_cutoff': 2} | [] | 0 |
| genpooling_lee2.effS.s0.log | {'other_error': 1, 'local_objective_bound': 6, 'node_cutoff': 11} | [] | 0 |
| genpooling_lee2.scip.s0.log | {'local_objective_bound': 4, 'node_cutoff': 13, 'other_error': 1} | [] | 0 |
| kall_congruentcircles_c52.corner.s0.log | {} | ['reported optimum differs from =opt= reference'] | 0 |
| kall_congruentcircles_c52.cornerS.s0.log | {} | ['reported optimum differs from =opt= reference'] | 0 |
| kall_congruentcircles_c52.scip.s0.log | {} | ['reported optimum differs from =opt= reference'] | 0 |
| ndcc16persp.corner.s0.log | {'node_cutoff': 2} | [] | 0 |
| ndcc16persp.cornerS.s0.log | {'node_cutoff': 2} | [] | 0 |
| ndcc16persp.effS.s0.log | {'node_cutoff': 2} | [] | 0 |
| nvs17.corner.s0.log | {'variable_bound': 5, 'global_objective_bound': 490, 'local_objective_bound': 9, 'other_error': 1, 'node_cutoff': 10} | [] | 0 |
| nvs17.cornerS.s0.log | {'variable_bound': 5, 'global_objective_bound': 490, 'local_objective_bound': 9, 'other_error': 1, 'node_cutoff': 10} | [] | 0 |
| nvs17.eff.s0.log | {'variable_bound': 28, 'local_objective_bound': 7, 'global_objective_bound': 684, 'other_error': 11, 'node_cutoff': 8} | [] | 0 |
| nvs17.effS.s0.log | {'variable_bound': 13, 'local_objective_bound': 8, 'global_objective_bound': 549, 'other_error': 2, 'node_cutoff': 9} | [] | 0 |
| nvs17.scip.s0.log | {'variable_bound': 25, 'local_objective_bound': 7, 'global_objective_bound': 441, 'other_error': 8, 'node_cutoff': 8} | [] | 0 |
| nvs24.corner.s0.log | {'variable_bound': 25, 'global_objective_bound': 4361, 'local_objective_bound': 22, 'other_error': 14, 'node_cutoff': 23} | [] | 0 |
| nvs24.cornerS.s0.log | {'variable_bound': 1, 'global_objective_bound': 6220, 'local_objective_bound': 17, 'other_error': 5, 'node_cutoff': 18} | [] | 0 |
| nvs24.eff.s0.log | {'variable_bound': 25, 'global_objective_bound': 3622, 'local_objective_bound': 19, 'other_error': 12, 'node_cutoff': 20} | [] | 0 |
| nvs24.effS.s0.log | {'variable_bound': 32, 'local_objective_bound': 18, 'global_objective_bound': 3123, 'other_error': 12, 'node_cutoff': 19} | [] | 0 |
| nvs24.scip.s0.log | {'variable_bound': 1, 'local_objective_bound': 18, 'global_objective_bound': 4332, 'other_error': 8, 'node_cutoff': 19} | [] | 0 |
| pooling_foulds5pq.cornerS.s0.log | {'node_cutoff': 2} | [] | 0 |
| pooling_foulds5pq.effS.s0.log | {'node_cutoff': 2} | [] | 0 |
| pooling_rt2pq.scip.s0.log | {'node_cutoff': 3} | [] | 0 |
| qp3.corner.s0.log | {'variable_bound': 1} | [] | 0 |
| qp3.cornerS.s0.log | {'variable_bound': 1} | [] | 0 |
| qp3.eff.s0.log | {'variable_bound': 1} | [] | 0 |
| qp3.effS.s0.log | {'variable_bound': 1} | [] | 0 |
| qp3.scip.s0.log | {'variable_bound': 1} | [] | 0 |
| st_glmp_fp2.corner.s0.log | {'variable_bound': 17, 'intersection_row': 19, 'local_objective_bound': 3, 'global_objective_bound': 13, 'other_error': 51, 'other_row': 2, 'node_cutoff': 4} | [] | 0 |
| st_glmp_fp2.cornerS.s0.log | {'variable_bound': 17, 'intersection_row': 19, 'local_objective_bound': 3, 'global_objective_bound': 13, 'other_error': 51, 'other_row': 2, 'node_cutoff': 4} | [] | 0 |
| st_glmp_fp2.eff.s0.log | {'variable_bound': 13, 'intersection_row': 9, 'local_objective_bound': 3, 'global_objective_bound': 6, 'other_error': 61, 'other_row': 1, 'node_cutoff': 4} | [] | 0 |
| st_glmp_fp2.effS.s0.log | {'variable_bound': 13, 'intersection_row': 9, 'local_objective_bound': 3, 'global_objective_bound': 6, 'other_error': 61, 'other_row': 1, 'node_cutoff': 4} | [] | 0 |
| st_glmp_fp2.scip.s0.log | {'variable_bound': 21, 'intersection_row': 17, 'local_objective_bound': 3, 'global_objective_bound': 6, 'other_error': 128, 'other_row': 3, 'node_cutoff': 4} | [] | 0 |

Unknown-variable warnings in 215 runs.
Final dual exclusions of MINLPLib: 0
Root dual exclusions of MINLPLib: 0
Global objective-warning runs: 25
Global objective-warning instances: ['ex5_2_5', 'gasprod_sarawak01', 'nvs17', 'nvs24', 'st_glmp_fp2']

### Intersection rows after correcting st_glmp_fp2 nlobjvar

| log | raw intersection messages | re-evaluated | still violates by > LP feastol | largest corrected violation (negative = slack) |
|---|---|---|---|---|
| st_glmp_fp2.corner.s0.log | 19 | 19 | 0 | -0.332672694197 |
| st_glmp_fp2.cornerS.s0.log | 19 | 19 | 0 | -0.332672694197 |
| st_glmp_fp2.eff.s0.log | 9 | 9 | 0 | -0.0175438188008 |
| st_glmp_fp2.effS.s0.log | 9 | 9 | 0 | -0.0175438188008 |
| st_glmp_fp2.scip.s0.log | 17 | 17 | 0 | -0.0859044484376 |
## debugsol_withsym

43 runs; limits {'30': 43}; return codes {'0': 41, '255': 1, None: 1}.
Non-run artifacts: run.log
Statuses: {'solving was interrupted [time limit reached]': 17, 'problem is solved [optimal solution found]': 24, None: 1, 'solving was interrupted [termination signal received]': 1}

| setting | runs | intersection row messages / runs | other row messages / runs | global objective warnings / runs | local objective warnings / runs | node cutoff messages / runs | any ERROR runs | rc not 0 | final dual excludes reference | root dual excludes reference |
|---|---|---|---|---|---|---|---|---|---|---|
| corner | 22 | 0 / 0 | 0 / 0 | 18361 / 2 | 7 / 3 | 7 / 2 | 5 | 1 | 0 | 0 |
| eff | 21 | 0 / 0 | 23 / 2 | 16126 / 2 | 17 / 3 | 6 / 1 | 5 | 1 | 0 | 0 |

### Runs with diagnostics or reference flags

| log | diagnostic message counts | reference flags | rc |
|---|---|---|---|
| carton9.corner.s0.log | {'variable_bound': 172} | [] | 0 |
| carton9.eff.s0.log | {'variable_bound': 172} | [] | 0 |
| ex5_2_5.corner.s0.log | {'variable_bound': 1, 'global_objective_bound': 16342, 'local_objective_bound': 3} | [] | 0 |
| ex5_2_5.eff.s0.log | {'variable_bound': 3, 'other_row': 16, 'global_objective_bound': 15330, 'local_objective_bound': 11, 'other_error': 1} | [] | 0 |
| ex5_4_2.eff.s0.log | {'local_objective_bound': 1, 'other_error': 9} | [] | 255 |
| ex8_3_9.corner.s0.log | {'other_error': 2} | [] | 0 |
| ex8_3_9.eff.s0.log | {'other_row': 7, 'other_error': 3} | [] | 0 |
| gasprod_sarawak01.corner.s0.log | {'global_objective_bound': 2019, 'local_objective_bound': 3, 'node_cutoff': 5} | [] | 0 |
| gasprod_sarawak01.eff.s0.log | {'global_objective_bound': 796, 'local_objective_bound': 5, 'variable_bound': 13, 'node_cutoff': 6} | [] | 0 |
| genpooling_lee2.corner.s0.log | {'local_objective_bound': 1, 'node_cutoff': 2} | [] | 0 |
| kall_congruentcircles_c52.corner.s0.log | {} | [] | None |

Unknown-variable warnings in 30 runs.
Final dual exclusions of MINLPLib: 0
Root dual exclusions of MINLPLib: 0
Global objective-warning runs: 4
Global objective-warning instances: ['ex5_2_5', 'gasprod_sarawak01']

### Intersection rows after correcting st_glmp_fp2 nlobjvar

| log | raw intersection messages | re-evaluated | still violates by > LP feastol | largest corrected violation (negative = slack) |
|---|---|---|---|---|

## Objective mapping diagnosis

| instance | original linear part at solution | quadratic part | constant | actual solution objective | objvar in solution file |
|---|---|---|---|---|---|
| st_glmp_fp2 | 0 | 7.6275 | 0 | 7.6275 | 7.6275 |
| ex5_2_5 | -8699.9999995406 | 5199.9999993339 | 0 | -3500.0000002067 | -3500.0000002067 |
| nvs17 | -2220.4 | 1120 | 0 | -1100.4 | -1100.4 |
| nvs24 | -2036.2 | 1003 | 0 | -1033.2 | -1033.2 |
| gasprod_sarawak01 | -45620.39190921 | 0 | 14104.987000025 | -31515.404909186 | -31515.404909186 |

SCIP reader_osil.c names generated helpers nlobjvar and objconstvar. debug.c ignores unknown names in solution files, defaults missing original values to 0, and computes its reference objective from loaded linear objective coefficients. Thus these files do not supply the nonlinear/constant helper values. st_glmp_fp2 rows are re-evaluated above with nlobjvar=7.6275; other row, variable-bound and node diagnostics are not certified harmless by this analysis. A clean whole-run validity check would require correctly mapped helper values.

Seed-0 archived run-log inventory: {'debug-solution': 343, 'root only': 2918}
Ordinary full-solve seed-0 logs: []
