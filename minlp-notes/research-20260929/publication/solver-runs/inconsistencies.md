# Certificate inconsistencies in the final campaign

Every positive forbidden-side difference is retained, including differences explained by printing. The returned GAMS point and the solver log incumbent are distinct observations; their duplicate flags are not independent failures. No final solver dual cuts off a reference primal. Full decimal margins and classifications are in [inconsistencies.csv](inconsistencies.csv).

All rows below are primal discrepancies. For minimization the margin is C−P; for pricing050 (max) it is P−C. A positive margin contradicts exact feasibility unless source printing explains it. The kan rows compare with R, whose certificate does not apply to tolerance-feasible OSIL points. All six original kan models are exactly infeasible.

| Instance | Solver | Returned primal forbidden margin | Log incumbent forbidden margin | Interpretation |
|---|---|---:|---:|---|
| camshape100 | BARON | 5.2581469E-7 | 5.2581469E-7 | returned point numerically infeasible; feasibility-tolerance effect; reported optimal with zero solver gap |
| camshape100 | SCIP | 1.5191022E-7 | 1.5191022E-7 | returned point numerically infeasible; feasibility-tolerance effect |
| camshape200 | BARON | 0.00000205270746 | 0.00000205270746 | returned point numerically infeasible; feasibility-tolerance effect; reported optimal with zero solver gap |
| camshape200 | SCIP | 6.3589286E-7 | 6.3589286E-7 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| camshape400 | BARON | 0.00000815450068 | 0.00000815450068 | returned point numerically infeasible; feasibility-tolerance effect |
| camshape400 | SCIP | 0.00000183227113 | 0.00000183227113 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| camshape800 | BARON | 0.09365569719715 | 0.09365569719715 | returned point numerically infeasible; feasibility-tolerance effect |
| camshape800 | GUROBI | 0.02328447110410 | 0.02328447110380 | returned point numerically infeasible; feasibility-tolerance effect |
| catmix100 | BARON | 1.48187204E-9 | 1.48187204E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain100 | BARON | 3.9306405E-9 | 3.9306405E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain100 | GUROBI | 2.231113305E-7 | 2.231117505E-7 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain100 | SCIP | — | 4.592105E-10 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain200 | BARON | 3.324632E-9 | 3.324632E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain200 | SCIP | 1.382E-12 | 1.182022E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain400 | BARON | 8.731229E-9 | 8.731229E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain400 | SCIP | — | 8.84219E-10 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain50 | BARON | 6.888293E-9 | 6.888293E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| chain50 | GUROBI | 2.01996813E-7 | 2.01996863E-7 | returned point numerically infeasible; feasibility-tolerance effect |
| chain50 | SCIP | 3.19613E-10 | 1.566313E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| dtoc5 | BARON | 0.00000238996117 | 0.00000238996117 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| dtoc5 | GUROBI | 1.3936294E-7 | 1.3936314E-7 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| etamac | BARON | 3.34037807E-7 | 3.34037807E-7 | returned point numerically infeasible; feasibility-tolerance effect |
| etamac | GUROBI | 2.85107407E-7 | 0.000001062701907 | returned point numerically infeasible; feasibility-tolerance effect |
| ex6_2_5 | BARON | 3.29241E-12 | 3.29241E-12 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| ex6_2_5 | GUROBI | — | 2.8582229241E-7 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| kan_r3_h1_n4 | GUROBI | 0.00065942100490325 | 0.0006594210049034 | R comparison only; known exact infeasibility of OSIL |
| kan_r3_h1_n4 | SCIP | 0.00176772953844896 | 0.00176772953306305 | R comparison only; known exact infeasibility of OSIL |
| kan_r3_h1_n5 | GUROBI | 2.742351E-9 | 2.742348E-9 | R comparison only; known exact infeasibility of OSIL |
| kan_r5_h1_n3 | GUROBI | 0.013090062917 | 0.01309006288 | R comparison only; known exact infeasibility of OSIL |
| kan_r5_h1_n5 | GUROBI | 1.06475386E-7 | 1.0647535E-7 | R comparison only; known exact infeasibility of OSIL |
| lnts100 | GUROBI | 6.9424E-9 | 6.9424E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| lnts100 | SCIP | 2.56E-12 | 2.560E-12 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| lnts50 | GUROBI | 5.608947E-9 | 5.6089E-9 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| optcdeg2 | BARON | 6.231509E-8 | 6.231509E-8 | certificate-inconsistent primal; tolerance effect suspected, this point unchecked |
| pindyck | BARON | 4.368613836068E-7 | 4.368613836068E-7 | returned point numerically infeasible; feasibility-tolerance effect |
| pindyck | GUROBI | 1.3836068E-12 | — | within source printing precision; no established contradiction |
| powerflow0039p | GUROBI | 0.00124788354 | 0.00124788014 | returned point numerically infeasible; feasibility-tolerance effect |
| pricing050 | BARON | 0.0000010463230577 | 0.0000010463230577 | returned point numerically infeasible; feasibility-tolerance effect |
| pricing050 | SCIP | 4.500930577E-7 | 4.500930577E-7 | returned point numerically infeasible; feasibility-tolerance effect |

The known waterno2 nonlinear propagation defect in [scip-bug/report.md](../scip-bug/report.md) is a different failure mode: an invalid cutoff and a too-high dual/optimal value. No whole-instance SCIP run here claims optimality or cuts off our reference point. These results do not test whether the defect occurred internally. The new campaign discrepancies match known feasibility-tolerance phenomena; no new solver defect is established.

Selected savepoints were evaluated at 50 digits from exact binary64 levels against the decimal OSIL model. The original 15 selected points have positive row violations; three additional GUROBI waterno2 points are recorded in point_checks.json and the report. These are numerical checks, not interval proofs or repairs; log incumbent vectors were not independently available.
