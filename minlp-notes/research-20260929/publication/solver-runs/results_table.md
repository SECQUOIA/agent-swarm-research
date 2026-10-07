# Final solver campaign: per-instance results

All values are solver reports, not rigorous certificates. Full printed values and all comparisons are in [results_table.csv](results_table.csv); reference sources are in [references.csv](references.csv).

BARON makes two optimality claims, both contradicted by our certified bounds. Accepted closures: **BARON 0, GUROBI 0, SCIP 0**. All 37 instances outside the six exactly infeasible kan models remain unclosed by all three solvers in this campaign. All 43 lack an accepted campaign closure.

There are **109 finite dual values, including six BARON values without a globality guarantee** (catmix100/200/400/800, dtoc5, optcdeg2). The other 103 comprise BARON 29, GUROBI 36 and SCIP 38; six SCIP values concern slightly tightened models, as noted per row. No solver supplies a finite catmix bound with an unqualified globality claim. Ten rows flag the first admitted batch under machine overload and memory pressure; all passed the measurement validity rule.

`Time` is GAMS solver time in seconds; for BARON it is wall clock while the 3600 s limit is CPU time. Four BARON values are 3706.37, 3708.98, 3709.5 and 3728.4 s; CSV also gives wall/CPU time. `C−D` means certificate minus solver dual for minimization, solver dual minus certificate for maximization: positive means the certificate is stronger. Infinite or missing duals give Infinity or —. Negative `P−C` in the CSV flags a primal beyond the certificate. For kan, comparisons concern R and do not certify the OSIL model.

`Closes` requires a valid run, a global optimality claim within the 3600 s solver budget and consistency with the certificates. Capability failures and the three memory stops are explicit outcomes; memory stops use the kept attempt and are excluded from full-hour measurements. Markdown numbers use 12 significant digits; CSV preserves source decimal tokens.

| Instance | Solver | Status | Time (s) | Primal P | Dual D | C−D (sense adjusted) | Closes | Notes |
|---|---|---|---:|---:|---:|---:|---|---|
| ann_cumene_tanh | BARON | capability failure | 0.0 | — | — | — | no | tanh unsupported; no finite final dual bound |
| ann_cumene_tanh | GUROBI | time limit, feasible point | 3601.569 | -3379.98236532 | -Infinity | Infinity | no | no finite final dual bound |
| ann_cumene_tanh | SCIP | capability failure | — | — | — | — | no | tanh unsupported; no finite final dual bound |
| camshape100 | BARON | optimality claim contradicted | 0.45 | -4.28414764756 | -4.28414764756 | 5.2581469e-7 | no | 50-digit point check: max row violation 1e-10 (e100); returned primal beyond certificate; log incumbent beyond certificate; optimality claim inconsistent with certificate |
| camshape100 | GUROBI | time limit, feasible point | 3602.44 | -4.28414702728 | -4.51619982399 | 0.232052702238 | no |  |
| camshape100 | SCIP | time limit, feasible point | 3600.005 | -4.28414727366 | -4.52868261398 | 0.244535492229 | no | 50-digit point check: max row violation 7.72e-10 (e63); returned primal beyond certificate; log incumbent beyond certificate |
| camshape200 | BARON | optimality claim contradicted | 23.22 | -4.27850228570 | -4.27850228570 | 0.00000205270746 | no | 50-digit point check: max row violation 1e-10 (e200); returned primal beyond certificate; log incumbent beyond certificate; optimality claim inconsistent with certificate |
| camshape200 | GUROBI | time limit, feasible point | 3601.733 | -4.27850006347 | -4.80194671335 | 0.523446480355 | no |  |
| camshape200 | SCIP | time limit, feasible point | 3600.006 | -4.27850086889 | -4.84321438129 | 0.564714148294 | no | returned primal beyond certificate; log incumbent beyond certificate |
| camshape400 | BARON | time limit, feasible point | 3600.5 | -4.27569663343 | -4.62237809041 | 0.346689611486 | no | 50-digit point check: max row violation 1e-10 (e400); returned primal beyond certificate; log incumbent beyond certificate |
| camshape400 | GUROBI | time limit, feasible point | 3601.568 | -4.21971290723 | -5.01165019102 | 0.735961712090 | no |  |
| camshape400 | SCIP | time limit, feasible point | 3600.006 | -4.27569031120 | -5.05804066293 | 0.782352184009 | no | returned primal beyond certificate; log incumbent beyond certificate |
| camshape800 | BARON | time limit, locally optimal point | 3601.4 | -4.36792983915 | -5.14464335341 | 0.870369211454 | no | 50-digit point check: max row violation 3.31e-07 (e2); returned primal beyond certificate; log incumbent beyond certificate |
| camshape800 | GUROBI | time limit, feasible point | 3602.059 | -4.29755861306 | -5.15809593077 | 0.883821788814 | no | 50-digit point check: max row violation 9.75e-07 (e58); returned primal beyond certificate; log incumbent beyond certificate |
| camshape800 | SCIP | time limit, feasible point | 3600.002 | -4.27427414195 | -5.20340885232 | 0.929134710364 | no |  |
| catmix100 | BARON | time limit, feasible point | 3600.04 | -0.0480694335130 | -1.17902146621 | 1.13095203418 | no | BARON: globality not guaranteed (inappropriate variable bounds); returned primal beyond certificate; log incumbent beyond certificate |
| catmix100 | GUROBI | time limit, feasible point | 3601.735 | -0.0480693551766 | -Infinity | Infinity | no | no finite final dual bound |
| catmix100 | SCIP | time limit, feasible point | 3600.024 | -0.0480693913776 | -Infinity | Infinity | no | no finite final dual bound |
| catmix200 | BARON | time limit, feasible point | 3600.12 | -0.0480591455774 | -2.87289907642 | 2.82483993082 | no | BARON: globality not guaranteed (inappropriate variable bounds) |
| catmix200 | GUROBI | time limit, feasible point | 3601.517 | -0.0480590526808 | -Infinity | Infinity | no | no finite final dual bound |
| catmix200 | SCIP | time limit, feasible point | 3600.006 | -0.0480591217155 | -Infinity | Infinity | no | no finite final dual bound |
| catmix400 | BARON | time limit, feasible point | 3600.48 | -0.0480565476256 | -8.41112796959 | 8.36307142176 | no | BARON: globality not guaranteed (inappropriate variable bounds) |
| catmix400 | GUROBI | time limit, feasible point | 3602.223 | -0.0480563817441 | -Infinity | Infinity | no | no finite final dual bound |
| catmix400 | SCIP | time limit, feasible point | 3600.001 | -0.0480565138067 | -Infinity | Infinity | no | no finite final dual bound |
| catmix800 | BARON | time limit, feasible point | 3600.13 | -0.0480559012733 | -54.6078031939 | 54.5597472924 | no | BARON: globality not guaranteed (inappropriate variable bounds) |
| catmix800 | GUROBI | time limit, feasible point | 3601.274 | -0.0480555759054 | -Infinity | Infinity | no | no finite final dual bound |
| catmix800 | SCIP | time limit, feasible point | 3600.0 | -0.0480558495448 | -Infinity | Infinity | no | no finite final dual bound |
| chain100 | BARON | time limit, feasible point | 3600.02 | 5.06978460681 | -409.135107507 | 414.204892118 | no | returned primal beyond certificate; log incumbent beyond certificate |
| chain100 | GUROBI | time limit, feasible point | 3602.432 | 5.06978438763 | -76.0184717333 | 81.0882563440 | no | dual from 13-digit GUROBI log; see printing half-unit in results.csv; returned primal beyond certificate; log incumbent beyond certificate |
| chain100 | SCIP | time limit, feasible point | 3600.0 | 5.06978461096 | -275.718218003 | 280.788002614 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; log incumbent beyond certificate |
| chain200 | BARON | time limit, feasible point | 3600.08 | 5.06891733847 | -395.443027309 | 400.511944651 | no | returned primal beyond certificate; log incumbent beyond certificate |
| chain200 | GUROBI | time limit, feasible point | 3601.724 | 5.06891913950 | -140.856922281 | 145.925839622 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; dual from 13-digit GUROBI log; see printing half-unit in results.csv |
| chain200 | SCIP | time limit, feasible point | 3600.0 | 5.06891734179 | -902.592565811 | 907.661483153 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; returned primal beyond certificate; log incumbent beyond certificate |
| chain400 | BARON | time limit, feasible point | 3600.75 | 5.06862168587 | -888.294516287 | 893.363137981 | no | returned primal beyond certificate; log incumbent beyond certificate |
| chain400 | GUROBI | time limit, feasible point | 3601.559 | 5.06894139709 | -682.862851554 | 687.931473249 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; dual from 13-digit GUROBI log; see printing half-unit in results.csv |
| chain400 | SCIP | time limit, feasible point | 3600.0 | 5.06862169517 | -1673.16248865 | 1678.23111034 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; log incumbent beyond certificate |
| chain50 | BARON | time limit, locally optimal point | 3600.06 | 5.07226148709 | -88.8872732852 | 93.9595347792 | no | returned primal beyond certificate; log incumbent beyond certificate |
| chain50 | GUROBI | time limit, feasible point | 3601.962 | 5.07226129199 | -36.2436405304 | 41.3159020244 | no | dual from 13-digit GUROBI log; see printing half-unit in results.csv; 50-digit point check: max row violation 6.69e-08 (e52); returned primal beyond certificate; log incumbent beyond certificate |
| chain50 | SCIP | time limit, feasible point | 3600.001 | 5.07226149366 | -74.9056748135 | 79.9779363075 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; returned primal beyond certificate; log incumbent beyond certificate |
| dtoc5 | BARON | time limit, feasible point | 3706.37 | 5.38966972922 | 0.000273134009568 | 5.38939898517 | no | BARON: globality not guaranteed (inappropriate variable bounds); first admitted batch: machine overload and memory pressure; passed measurement validity rule; returned primal beyond certificate; log incumbent beyond certificate |
| dtoc5 | GUROBI | time limit, feasible point | 3601.629 | 5.38967197982 | -781.515624375 | 786.905296494 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule; returned primal beyond certificate; log incumbent beyond certificate |
| dtoc5 | SCIP | time limit, feasible point | 3602.174 | 50008.00034 | 0.000019999 | 5.38965212018 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule |
| eg_disc2_s | BARON | time limit, feasible point | 3600.09 | 5.98824222069 | -5.02452672571 | 10.6666273000 | no |  |
| eg_disc2_s | GUROBI | time limit, feasible point | 3601.623 | 14.5310509233 | -6.37450863475 | 12.0166092091 | no |  |
| eg_disc2_s | SCIP | time limit, feasible point | 3600.003 | 7.47730137345 | -2.83013002499 | 8.47223059932 | no |  |
| eg_disc_s | BARON | time limit, feasible point | 3600.09 | 5.88203742818 | 1.08630444698 | 4.67423516371 | no |  |
| eg_disc_s | GUROBI | time limit, feasible point | 3601.621 | 6.28623126968 | -2.86089160167 | 8.62143121236 | no |  |
| eg_disc_s | SCIP | time limit, feasible point | 3600.004 | 7.78793357941 | 2.71549916578 | 3.04504044491 | no |  |
| eg_int_s | BARON | time limit, feasible point | 3600.07 | 6.45310315904 | 0.879339371088 | 5.57376378185 | no |  |
| eg_int_s | GUROBI | time limit, point exceeds solver tolerance | 3601.632 | 8.84042547339 | -1.90678635916 | 8.35988951209 | no | GUROBI reports max constraint violation 5.9580e-05 beyond its tolerance |
| eg_int_s | SCIP | time limit, feasible point | 3600.002 | 6.85732181656 | 5.43888535430 | 1.01421779864 | no | GAMS returned point differs from solver log incumbent; both compared in CSV |
| etamac | BARON | time limit, locally optimal point | 3600.01 | -15.2946759774 | -16.5147077865 | 1.22003214312 | no | 50-digit point check: max row violation 6.8e-07 (e16); returned primal beyond certificate; log incumbent beyond certificate |
| etamac | GUROBI | time limit, feasible point | 3601.677 | -15.2946759285 | — | — | no | GAMS returned point differs from solver log incumbent; both compared in CSV; 50-digit point check: max row violation 9.93e-07 (e10); returned primal beyond certificate; log incumbent beyond certificate; no finite final dual bound |
| etamac | SCIP | time limit, no primal | 3600.014 | — | -15.5138681230 | 0.219192479663 | no | SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model |
| ex6_2_5 | BARON | time limit, locally optimal point | 3600.07 | -70.7520778335 | -157.339807914 | 86.5877300804 | no | returned primal beyond certificate; log incumbent beyond certificate |
| ex6_2_5 | GUROBI | time limit, feasible point | 3601.629 | -70.7520778334 | -128.325187347 | 57.5731095135 | no | GAMS returned point differs from solver log incumbent; both compared in CSV; dual from 13-digit GUROBI log; see printing half-unit in results.csv; log incumbent beyond certificate |
| ex6_2_5 | SCIP | stopped at the 8 GB memory limit | 1515.639 | -70.7184889007 | -592.077342771 | 521.325264938 | no | INVALID time measurement; kept attempt 1 of 3; final bound retained; SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model; GAMS returned point differs from solver log incumbent; both compared in CSV |
| ex6_2_7 | BARON | time limit, feasible point | 3600.06 | -0.160847615464 | -1.40937659321 | 1.24852897775 | no |  |
| ex6_2_7 | GUROBI | time limit, feasible point | 3601.63 | -0.160847615464 | -1.58442163961 | 1.42357402414 | no | dual from 13-digit GUROBI log; see printing half-unit in results.csv |
| ex6_2_7 | SCIP | stopped at the 8 GB memory limit | 1962.771 | -0.160846800069 | -1.42171210528 | 1.26086448982 | no | INVALID time measurement; kept attempt 1 of 3; final bound retained; SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model |
| hvycrash | BARON | capability failure | 0.0 | — | — | — | no | cos unsupported; no finite final dual bound |
| hvycrash | GUROBI | time limit, no primal | 3602.443 | — | -2141300000.00 | 2141299999.78 | no | dual from 13-digit GUROBI log; see printing half-unit in results.csv |
| hvycrash | SCIP | time limit, no primal | 3600.007 | — | -218500000 | 218499999.782 | no | SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model |
| kan_r3_h1_n4 | BARON | time limit, feasible point | 3602.54 | 0.191869254680 | -512.732925360 | 512.735706597 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r3_h1_n4 | GUROBI | time limit, feasible point | 3602.039 | 0.00212181614768 | -9.29033977655 | 9.29312101370 | no | OSIL exactly infeasible; certificate and reference primal concern R only; returned primal beyond certificate; log incumbent beyond certificate |
| kan_r3_h1_n4 | SCIP | time limit, feasible point | 3600.0 | 0.00101350761413 | -0.00593130486004 | 0.00871254201262 | no | OSIL exactly infeasible; certificate and reference primal concern R only; GAMS returned point differs from solver log incumbent; both compared in CSV; 50-digit point check: max row violation 9.62e-07 (e1383); returned primal beyond certificate; log incumbent beyond certificate |
| kan_r3_h1_n5 | BARON | time limit, feasible point | 3601.25 | 11.5276766220 | -44.0030110312 | 43.9919683516 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r3_h1_n5 | GUROBI | time limit, feasible point | 3601.522 | -0.0110426822641 | -5.83812169043 | 5.82707901090 | no | OSIL exactly infeasible; certificate and reference primal concern R only; returned primal beyond certificate; log incumbent beyond certificate |
| kan_r3_h1_n5 | SCIP | time limit, feasible point | 3600.0 | 0.141699541122 | -22.8494267148 | 22.8383840352 | no | OSIL exactly infeasible; certificate and reference primal concern R only; GAMS returned point differs from solver log incumbent; both compared in CSV |
| kan_r3_h1_n9 | BARON | time limit, feasible point | 3708.98 | 691.884957563 | -300.495137652 | 300.508101311 | no | OSIL exactly infeasible; certificate and reference primal concern R only; first admitted batch: machine overload and memory pressure; passed measurement validity rule |
| kan_r3_h1_n9 | GUROBI | time limit, feasible point | 3601.281 | 0.108110003406 | -128.708539226 | 128.721502886 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r3_h1_n9 | SCIP | time limit, feasible point | 3600.001 | 16.6392067343 | -205.030105056 | 205.043068716 | no | OSIL exactly infeasible; certificate and reference primal concern R only; GAMS returned point differs from solver log incumbent; both compared in CSV |
| kan_r5_h1_n3 | BARON | time limit, feasible point | 3601.1 | -32.9537071057 | -24696.7041619 | 24433.8399360 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r5_h1_n3 | GUROBI | time limit, feasible point | 3602.223 | -262.877315972 | -2833.82666792 | 2570.96244202 | no | OSIL exactly infeasible; certificate and reference primal concern R only; 50-digit point check: max row violation 8.17e-07 (e1052); returned primal beyond certificate; log incumbent beyond certificate |
| kan_r5_h1_n3 | SCIP | time limit, feasible point | 3600.003 | -211.453526431 | -8568.34225810 | 8305.47803219 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r5_h1_n5 | BARON | time limit, feasible point | 3600.66 | 3.97338072569 | -10.8047753713 | 11.0773586252 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r5_h1_n5 | GUROBI | time limit, feasible point | 3601.535 | 0.272583147379 | -2.44555167613 | 2.71813492998 | no | OSIL exactly infeasible; certificate and reference primal concern R only; returned primal beyond certificate; log incumbent beyond certificate |
| kan_r5_h1_n5 | SCIP | time limit, feasible point | 3600.001 | 3.83753204078 | -10.8047753713 | 11.0773586252 | no | OSIL exactly infeasible; certificate and reference primal concern R only; GAMS returned point differs from solver log incumbent; both compared in CSV |
| kan_r5_h1_n8 | BARON | time limit, feasible point | 3600.26 | 31.9125890376 | -216.534782608 | 216.604110468 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r5_h1_n8 | GUROBI | time limit, feasible point | 3601.269 | 4.05480187485 | -168.578585778 | 168.647913638 | no | OSIL exactly infeasible; certificate and reference primal concern R only |
| kan_r5_h1_n8 | SCIP | time limit, feasible point | 3600.0 | 96.3272872291 | -234.210425334 | 234.279753194 | no | OSIL exactly infeasible; certificate and reference primal concern R only; GAMS returned point differs from solver log incumbent; both compared in CSV |
| lnts100 | BARON | capability failure | 0.0 | — | — | — | no | sin/cos unsupported; no finite final dual bound |
| lnts100 | GUROBI | time limit, feasible point | 3601.531 | 0.554595394224 | 0.551893222965 | 0.00270217820127 | no | returned primal beyond certificate; log incumbent beyond certificate |
| lnts100 | SCIP | time limit, feasible point | 3600.001 | 0.554595401164 | 0.519475858554 | 0.0351195426126 | no | returned primal beyond certificate; log incumbent beyond certificate |
| lnts200 | BARON | capability failure | 0.0 | — | — | — | no | sin/cos unsupported; no finite final dual bound |
| lnts200 | GUROBI | time limit, feasible point | 3602.219 | 0.554577018507 | 0.552265826638 | 0.00231118946444 | no |  |
| lnts200 | SCIP | time limit, feasible point | 3600.005 | 0.554577016126 | 0.507782467085 | 0.0467945490178 | no |  |
| lnts400 | BARON | capability failure | 0.0 | — | — | — | no | sin/cos unsupported; no finite final dual bound |
| lnts400 | GUROBI | time limit, feasible point | 3601.522 | 0.554572426749 | 0.550885686672 | 0.00368672702763 | no |  |
| lnts400 | SCIP | time limit, feasible point | 3600.0 | 0.554572413704 | 0.545087494953 | 0.00948491874706 | no |  |
| lnts50 | BARON | capability failure | 0.0 | — | — | — | no | sin/cos unsupported; no finite final dual bound |
| lnts50 | GUROBI | time limit, feasible point | 3602.429 | 0.554668759329 | 0.554646860480 | 0.000021904457628 | no | returned primal beyond certificate; log incumbent beyond certificate |
| lnts50 | SCIP | time limit, feasible point | 3600.002 | 0.554668764940 | 0.518794584214 | 0.0358741807241 | no |  |
| lukvle10 | BARON | time limit, locally optimal point | 3600.52 | 352.891210603 | 0.0117328655649 | 352.226292540 | no |  |
| lukvle10 | GUROBI | interface/model-expression failure | — | — | — | — | no | GUROBI error 10024: POW needs at least one constant argument; no finite final dual bound |
| lukvle10 | SCIP | time limit, feasible point | 3600.002 | 353.049244141 | 347.646742306 | 4.59128309957 | no | SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model; GAMS returned point differs from solver log incumbent; both compared in CSV |
| optcdeg2 | BARON | time limit, feasible point | 3728.4 | 293.876075034 | 2.31984116239 | 291.556233933 | no | BARON: globality not guaranteed (inappropriate variable bounds); first admitted batch: machine overload and memory pressure; passed measurement validity rule; returned primal beyond certificate; log incumbent beyond certificate |
| optcdeg2 | GUROBI | time limit, no primal | 3601.561 | — | 166.816964152 | 127.059110943 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule; dual from 13-digit GUROBI log; see printing half-unit in results.csv |
| optcdeg2 | SCIP | time limit, no primal | 3601.814 | — | 200.133567480 | 93.7425076161 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule |
| pindyck | BARON | time limit, feasible point | 3600.03 | -1170.48628587 | -3067.37503163 | 1896.88874619 | no | 50-digit point check: max row violation 3.49e-07 (e91); returned primal beyond certificate; log incumbent beyond certificate |
| pindyck | GUROBI | time limit, feasible point | 3601.961 | -1170.48628544 | -1829.19878739 | 658.712501951 | no | returned primal beyond certificate (printing-scale) |
| pindyck | SCIP | stopped at the 8 GB memory limit | 2546.128 | — | -1625.39840602 | 454.912120588 | no | INVALID time measurement; kept attempt 2 of 3; final bound retained; SCIP: log/pow argument lower bounds tightened to 1e-9; dual is for a slightly tightened model |
| powerflow0030p | BARON | capability failure | 0.0 | — | — | — | no | sin/cos unsupported; no finite final dual bound |
| powerflow0030p | GUROBI | time limit, feasible point | 3601.523 | 576.915992456 | 569.890824735 | 7.00258756341 | no |  |
| powerflow0030p | SCIP | time limit, no primal | 3600.009 | — | 0 | 576.893412299 | no |  |
| powerflow0039p | BARON | capability failure | 0.0 | — | — | — | no | sin/cos unsupported; no finite final dual bound |
| powerflow0039p | GUROBI | time limit, feasible point | 3601.523 | 41869.0502370 | 41765.7115905 | 103.339894320 | no | 50-digit point check: max row violation 6.81e-07 (e73); returned primal beyond certificate; log incumbent beyond certificate |
| powerflow0039p | SCIP | time limit, no primal | 3600.004 | — | 2 | 41867.0514849 | no |  |
| powerflow0039r | BARON | time limit, feasible point | 3600.03 | 41869.0515109 | 41268.7509414 | 600.300541907 | no |  |
| powerflow0039r | GUROBI | time limit, feasible point | 3601.721 | 41869.0515116 | 41618.4939762 | 250.557507058 | no |  |
| powerflow0039r | SCIP | time limit, no primal | 3600.001 | — | 41745.9299435 | 123.121539798 | no |  |
| pricing050 | BARON | time limit, feasible point | 3600.01 | -1813.82907741 | -1055.02849148 | 758.800586971 | no | 50-digit point check: max row violation 3.41e-07 (e6); returned primal beyond certificate; log incumbent beyond certificate |
| pricing050 | GUROBI | time limit, feasible point | 3601.941 | -1813.82907849 | -1418.11253584 | 395.716542612 | no |  |
| pricing050 | SCIP | time limit, feasible point | 3600.005 | -1813.82907800 | -1514.52108768 | 299.307990773 | no | 50-digit point check: max row violation 1.22e-07 (e5); returned primal beyond certificate; log incumbent beyond certificate |
| waterno2_06 | BARON | time limit, feasible point | 3600.59 | 295.423726397 | 80.2349888858 | 197.995584114 | no |  |
| waterno2_06 | GUROBI | time limit, feasible point | 3601.567 | 283.127448096 | 142.831148612 | 135.399424388 | no |  |
| waterno2_06 | SCIP | time limit, no primal | 3600.003 | — | 130.130142237 | 148.100430763 | no |  |
| waterno2_09 | BARON | time limit, feasible point | 3601.39 | 976.983387431 | 123.341058238 | 701.493633762 | no |  |
| waterno2_09 | GUROBI | time limit, feasible point | 3602.067 | 919.990495244 | 220.683687372 | 604.151004628 | no | 50-digit point check: max row violation 1e-06 (e144); reported primal improves MINLPLib listed primal by 2.604794556432; 50-digit maximum violation 9.99994e-07 |
| waterno2_09 | SCIP | time limit, no primal | 3600.003 | — | 217.717273877 | 607.117418123 | no |  |
| waterno2_12 | BARON | time limit, feasible point | 3600.55 | 2367.78938003 | 151.273129649 | 1938.48143535 | no |  |
| waterno2_12 | GUROBI | time limit, feasible point | 3602.04 | 2262.23109567 | 454.555064420 | 1635.19950058 | no | 50-digit point check: max row violation 6.67e-07 (e200); reported primal improves MINLPLib listed primal by 1.12727833282; 50-digit maximum violation 6.66876e-07 |
| waterno2_12 | SCIP | time limit, no primal | 3600.007 | — | 453.856471288 | 1635.89809371 | no |  |
| waterno2_18 | BARON | time limit, feasible point | 3600.11 | 5606.51998897 | 144.587532191 | 4646.23318281 | no |  |
| waterno2_18 | GUROBI | time limit, feasible point | 3601.269 | 5296.93466951 | 712.855772926 | 4077.96494207 | no |  |
| waterno2_18 | SCIP | time limit, no primal | 3600.011 | — | 891.934497970 | 3898.88621703 | no |  |
| waterno2_24 | BARON | time limit, feasible point | 3709.5 | 7658.18587358 | 96.9091443094 | 6479.24224369 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule |
| waterno2_24 | GUROBI | time limit, feasible point | 3601.489 | 7295.02032370 | 815.732010947 | 5760.41937705 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule; 50-digit point check: max row violation 9.22e-07 (e2022); reported primal improves MINLPLib listed primal by 37.70136730126; 50-digit maximum violation 9.22257e-07 |
| waterno2_24 | SCIP | time limit, no primal | 3600.001 | — | 1074.43904635 | 5501.71234165 | no | first admitted batch: machine overload and memory pressure; passed measurement validity rule |
