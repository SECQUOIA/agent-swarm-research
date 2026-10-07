| instance | listed primal | best listed dual (solver) | gap before | certified dual (ours) | best primal (ours or listed) | gap after | certification: max / total period time, nodes |
|---|---|---|---|---|---|---|---|
| waterno2_06 | 282.8880 | 165.1903 (SCIP) | 71.2% | **263.735099** | 282.8880 (listed) | 7.26% | 151 s / 550 s, 29196 |
| waterno2_09 | 922.5953 | 273.8958 (SCIP) | 236.8% | **824.834692** | 914.0120 (ours) | 10.81% | 507 s / 2384 s, 108519 |
| waterno2_12 | 2263.3584 | 479.5051 (GUROBI) | 372.0% | **2089.754565** | 2233.8213 (ours) | 6.89% | 488 s / 3103 s, 140952 |
| waterno2_18 | 5269.6388 | 770.7362 (SCIP) | 583.7% | **4790.820715** | 5023.9827 (ours) | 4.87% | 1280 s / 7509 s, 381084 |
| waterno2_24 | 7332.7217 | 1095.1265 (SCIP) | 569.6% | **6576.151388** | 6963.7952 (ours) | 5.89% | 1368 s / 10032 s, 525224 |

| instance | our primal value (exact) | max abs. row violation (row) | max bound violation | binaries integral | listed primal |
|---|---|---|---|---|---|
| waterno2_09 | 914.011970350 | 1.00e-09 (e1677) | 5.73e-11 | True | 922.5953 |
| waterno2_12 | 2233.821335282 | 1.00e-09 (e2097) | 3.09e-10 | True | 2263.3584 |
| waterno2_18 | 5023.982735143 | 4.44e-09 (e299) | 8.94e-10 | True | 5269.6388 |
| waterno2_24 | 6963.795154460 | 1.00e-09 (e3896) | 9.00e-10 | True | 7332.7217 |
