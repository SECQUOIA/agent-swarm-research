# Stock rerun after review round 1

120 stock runs; same 300 CPU-second limit, clock type 1 and seeds 1/2. Unsolved/error CPU counts as 300 s; shifts: CPU 1 s, nodes 100. All-setting subsets use all five settings. Truncated node counts measure work performed, not effort to solve an unsolved instance.

Stock statuses: {'problem is solved [optimal solution found]': 77, 'solving was interrupted [time limit reached]': 43}
Stock return codes: {'0': 120}

| scope | setting | solved / runs | CPU sgm | nodes n / sgm | all-five-solved n | CPU / nodes sgm there |
|---|---|---|---|---|---|---|
| seed 1 | off | 37 / 60 | 18.490 | 59 / 4739.2 | 36 | 2.170 / 617.6 |
| seed 1 | stock-scip | 38 / 60 | 16.066 | 59 / 5444.3 | 36 | 1.992 / 623.5 |
| seed 1 | patched-scip | 38 / 60 | 18.028 | 59 / 4609.9 | 36 | 2.537 / 624.7 |
| seed 1 | corner | 38 / 60 | 17.814 | 59 / 4563.0 | 36 | 2.554 / 627.6 |
| seed 1 | eff | 38 / 60 | 17.071 | 59 / 4280.1 | 36 | 2.366 / 572.3 |
| seed 2 | off | 38 / 60 | 16.959 | 60 / 4447.1 | 37 | 2.127 / 616.0 |
| seed 2 | stock-scip | 39 / 60 | 15.858 | 60 / 5057.4 | 37 | 1.864 / 604.8 |
| seed 2 | patched-scip | 37 / 60 | 17.930 | 60 / 4315.9 | 37 | 2.391 / 616.0 |
| seed 2 | corner | 38 / 60 | 16.815 | 60 / 3890.1 | 37 | 2.117 / 515.4 |
| seed 2 | eff | 38 / 60 | 17.260 | 60 / 3868.8 | 37 | 2.319 / 530.6 |
| pooled | off | 75 / 120 | 17.709 | 119 / 4589.6 | 73 | 2.148 / 616.8 |
| pooled | stock-scip | 77 / 120 | 15.962 | 119 / 5245.7 | 73 | 1.926 / 614.0 |
| pooled | patched-scip | 75 / 120 | 17.979 | 119 / 4459.3 | 73 | 2.462 / 620.3 |
| pooled | corner | 76 / 120 | 17.308 | 119 / 4210.6 | 73 | 2.325 / 568.4 |
| pooled | eff | 76 / 120 | 17.166 | 119 / 4067.6 | 73 | 2.342 / 550.8 |
| exclude off failure | off | 75 / 119 | 17.277 | 119 / 4589.6 | 73 | 2.148 / 616.8 |
| exclude off failure | stock-scip | 76 / 119 | 16.361 | 119 / 5245.7 | 73 | 1.926 / 614.0 |
| exclude off failure | patched-scip | 74 / 119 | 18.443 | 119 / 4459.3 | 73 | 2.462 / 620.3 |
| exclude off failure | corner | 75 / 119 | 17.751 | 119 / 4210.6 | 73 | 2.325 / 568.4 |
| exclude off failure | eff | 75 / 119 | 17.603 | 119 / 4067.6 | 73 | 2.342 / 550.8 |

P-values are exploratory. Pooled tests average the seed log ratios within each instance before testing; pair-solved subsets may differ by comparison. Tests with fewer than ten nonzero differences are not reported (—).

| scope | subset | X vs Y | n pairs / instances | CPU shifted ratio / p | nodes shifted ratio / p | only X / only Y solved |
|---|---|---|---|---|---|---|
| seed 1 | all | stock-scip vs off | 60 / 60 | 0.8756 / 0.05443 | — | 1 / 0 |
| seed 1 | pair solved | stock-scip vs off | 37 / 37 | 0.9392 / 0.08793 | 1.0187 / 0.1478 | 1 / 0 |
| seed 1 | all five solved | stock-scip vs off | 36 / 36 | 0.9438 / 0.1206 | 1.0082 / 0.1948 | 1 / 0 |
| seed 1 | exclude off failure | stock-scip vs off | 59 / 59 | 0.9614 / 0.08793 | — | 1 / 0 |
| seed 1 | all | patched-scip vs stock-scip | 60 / 60 | 1.1150 / 1.468e-06 | — | 1 / 1 |
| seed 1 | pair solved | patched-scip vs stock-scip | 37 / 37 | 1.1772 / 1.174e-06 | 1.0016 / — | 1 / 1 |
| seed 1 | all five solved | patched-scip vs stock-scip | 36 / 36 | 1.1823 / 1.733e-06 | 1.0016 / — | 1 / 1 |
| seed 1 | exclude off failure | patched-scip vs stock-scip | 59 / 59 | 1.1168 / 2.038e-06 | — | 1 / 1 |
| seed 2 | all | stock-scip vs off | 60 / 60 | 0.9387 / 0.01205 | — | 1 / 0 |
| seed 2 | pair solved | stock-scip vs off | 38 / 38 | 0.9086 / 0.01755 | 0.9888 / 0.1442 | 1 / 0 |
| seed 2 | all five solved | stock-scip vs off | 37 / 37 | 0.9160 / 0.02816 | 0.9844 / 0.1848 | 1 / 0 |
| seed 2 | exclude off failure | stock-scip vs off | 60 / 60 | 0.9387 / 0.01205 | — | 1 / 0 |
| seed 2 | all | patched-scip vs stock-scip | 60 / 60 | 1.1229 / 1.581e-07 | — | 0 / 2 |
| seed 2 | pair solved | patched-scip vs stock-scip | 37 / 37 | 1.1841 / 3.569e-07 | 1.0159 / — | 0 / 2 |
| seed 2 | all five solved | patched-scip vs stock-scip | 37 / 37 | 1.1841 / 3.569e-07 | 1.0159 / — | 0 / 2 |
| seed 2 | exclude off failure | patched-scip vs stock-scip | 60 / 60 | 1.1229 / 1.581e-07 | — | 0 / 2 |
| pooled | all | stock-scip vs off | 120 / 60 | 0.9066 / 0.003315 | — | 2 / 0 |
| pooled | pair solved | stock-scip vs off | 75 / 38 | 0.9236 / 0.005131 | 1.0034 / 0.09022 | 2 / 0 |
| pooled | all five solved | stock-scip vs off | 73 / 37 | 0.9296 / 0.007924 | 0.9960 / 0.1207 | 2 / 0 |
| pooled | exclude off failure | stock-scip vs off | 119 / 60 | 0.9499 / 0.003473 | — | 2 / 0 |
| pooled | all | patched-scip vs stock-scip | 120 / 60 | 1.1189 / 1.666e-07 | — | 1 / 3 |
| pooled | pair solved | patched-scip vs stock-scip | 74 / 37 | 1.1807 / 2.355e-07 | 1.0087 / — | 1 / 3 |
| pooled | all five solved | patched-scip vs stock-scip | 73 / 37 | 1.1832 / 2.355e-07 | 1.0088 / — | 1 / 3 |
| pooled | exclude off failure | patched-scip vs stock-scip | 119 / 60 | 1.1199 / 1.545e-07 | — | 1 / 3 |

Patched vs stock non-timing final signatures differ on 51 pairs.
Both-solved signature differences: 5 [{'instance': 'blend531', 'seed': 2, 'differences': {'nodes': [37747.0, 21287.0], 'primal LP': [('11470', '0'), ('6297', '0')], 'dual LP': [('98505', '1044426'), ('56092', '598741')]}}, {'instance': 'carton9', 'seed': 1, 'differences': {'nodes': [4798.0, 4349.0], 'primal': [205.137079374686, 205.137079374654], 'dual': [205.137079374686, 205.137079374654], 'primal LP': [('1839', '0'), ('1722', '0')], 'dual LP': [('10447', '252724'), ('9558', '229801')]}}, {'instance': 'carton9', 'seed': 2, 'differences': {'nodes': [4774.0, 4722.0], 'primal': [205.13707935605, 205.137079364837], 'dual': [205.13707935605, 205.137079364837], 'primal LP': [('1908', '4'), ('1890', '1')], 'dual LP': [('10127', '241583'), ('9892', '246435')]}}, {'instance': 'edgecross14-039', 'seed': 1, 'differences': {'nodes': [771.0, 805.0], 'primal LP': [('341', '0'), ('348', '0')], 'dual LP': [('2040', '276597'), ('2059', '275337')]}}, {'instance': 'edgecross14-039', 'seed': 2, 'differences': {'nodes': [1051.0, 1049.0], 'primal LP': [('474', '0'), ('466', '0')], 'dual LP': [('2691', '301909'), ('2681', '300424')]}}]
First-LP / root dual bound differences: []
Pairs with both root statistics available: 117
Time-limited pairs can differ in truncated work because of load; this is not a pure count of capture-caused divergences.
stock-scip vs off solved only X [('ex5_4_2', 1), ('gabriel01', 2)] only Y []
patched-scip vs stock-scip solved only X [('tln7', 1)] only Y [('blend852', 1), ('blend852', 2), ('gabriel01', 2)]
Stock reference flags: []
Load: {'first': '2026-10-04T02:36:40.780307+00:00', 'last': '2026-10-04T03:28:45.368382+00:00', 'load1_min': 5.31884765625, 'load1_max': 125.85302734375, 'wall_timeouts': [{'event': 'done', 'utc': '2026-10-04T02:48:40.764050+00:00', 'load': [95.65478515625, 91.5361328125, 54.1943359375], 'instance': 'blend852', 'seed': 1, 'returncode': 124, 'wall': 720.0266877520007}, {'event': 'done', 'utc': '2026-10-04T02:48:41.393635+00:00', 'load': [95.65478515625, 91.5361328125, 54.1943359375], 'instance': 'blend852', 'seed': 2, 'returncode': 124, 'wall': 720.6563743269999}, {'event': 'done', 'utc': '2026-10-04T02:49:17.495253+00:00', 'load': [74.3779296875, 86.68896484375, 53.95458984375], 'instance': 'ex5_2_5', 'seed': 2, 'returncode': 124, 'wall': 720.0424323730003}, {'event': 'done', 'utc': '2026-10-04T02:49:24.278970+00:00', 'load': [66.08447265625, 84.5087890625, 53.595703125], 'instance': 'ex8_3_2', 'seed': 2, 'returncode': 124, 'wall': 720.024005457999}, {'event': 'done', 'utc': '2026-10-04T02:49:11.851322+00:00', 'load': [79.4599609375, 87.88232421875, 54.15966796875], 'instance': 'ex5_2_5', 'seed': 1, 'returncode': 124, 'wall': 723.5871756960005}, {'event': 'done', 'utc': '2026-10-04T02:49:22.820912+00:00', 'load': [70.18359375, 85.61474609375, 53.78271484375], 'instance': 'ex8_3_2', 'seed': 1, 'returncode': 124, 'wall': 720.0317816650004}, {'event': 'done', 'utc': '2026-10-04T02:49:39.745827+00:00', 'load': [55.21728515625, 81.201171875, 53.00830078125], 'instance': 'ex8_3_9', 'seed': 2, 'returncode': 124, 'wall': 720.0380807420006}, {'event': 'done', 'utc': '2026-10-04T02:49:38.437226+00:00', 'load': [58.45751953125, 82.2685546875, 53.19775390625], 'instance': 'ex8_3_9', 'seed': 1, 'returncode': 124, 'wall': 720.039406748001}], 'stock_median_wall_cpu': 1.2046666666666666}
