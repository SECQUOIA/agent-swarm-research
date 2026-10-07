# Completed full-solve analysis

480 logs; 60 instances; seeds [1, 2]; settings ('off', 'scip', 'corner', 'eff').
CPU limit 300 s; unsolved/error CPU observations count as 300 s. Node means use the same pairs for every setting, excluding a pair if any node count is missing. These include observed truncated work on time-limited runs.

Return codes: {'0': 479, '255': 1}
Statuses: {'problem is solved [optimal solution found]': 302, 'solving was interrupted [time limit reached]': 177, None: 1}

## Aggregates

| scope | setting | runs | solved | errors / nonzero rc | time sgm | nodes n | nodes sgm | all-solved n | all-solved time sgm | all-solved nodes sgm |
|---|---|---|---|---|---|---|---|---|---|---|
| seed 1 | off | 60 | 37 | 1 | 18.490 | 59 | 4739.186 | 36 | 2.170 | 617.638 |
| seed 1 | scip | 60 | 38 | 0 | 18.028 | 59 | 4609.884 | 36 | 2.537 | 624.676 |
| seed 1 | corner | 60 | 38 | 0 | 17.814 | 59 | 4562.999 | 36 | 2.554 | 627.591 |
| seed 1 | eff | 60 | 38 | 0 | 17.071 | 59 | 4280.055 | 36 | 2.366 | 572.252 |
| seed 2 | off | 60 | 38 | 0 | 16.959 | 60 | 4447.082 | 37 | 2.127 | 615.963 |
| seed 2 | scip | 60 | 37 | 0 | 17.930 | 60 | 4315.883 | 37 | 2.391 | 615.970 |
| seed 2 | corner | 60 | 38 | 0 | 16.815 | 60 | 3890.052 | 37 | 2.117 | 515.445 |
| seed 2 | eff | 60 | 38 | 0 | 17.260 | 60 | 3868.773 | 37 | 2.319 | 530.645 |
| all pairs | off | 120 | 75 | 1 | 17.709 | 119 | 4589.634 | 73 | 2.148 | 616.789 |
| all pairs | scip | 120 | 75 | 0 | 17.979 | 119 | 4459.280 | 73 | 2.462 | 620.250 |
| all pairs | corner | 120 | 76 | 0 | 17.308 | 119 | 4210.599 | 73 | 2.325 | 568.406 |
| all pairs | eff | 120 | 76 | 0 | 17.166 | 119 | 4067.619 | 73 | 2.342 | 550.831 |
| exclude failure pair | off | 119 | 75 | 0 | 17.277 | 119 | 4589.634 | 73 | 2.148 | 616.789 |
| exclude failure pair | scip | 119 | 74 | 0 | 18.443 | 119 | 4459.280 | 73 | 2.462 | 620.250 |
| exclude failure pair | corner | 119 | 75 | 0 | 17.751 | 119 | 4210.599 | 73 | 2.325 | 568.406 |
| exclude failure pair | eff | 119 | 75 | 0 | 17.603 | 119 | 4067.619 | 73 | 2.342 | 550.831 |
| exclude flagged instance | off | 118 | 73 | 1 | 18.372 | 117 | 4665.009 | 71 | 2.172 | 597.949 |
| exclude flagged instance | scip | 118 | 73 | 0 | 18.597 | 117 | 4515.219 | 71 | 2.481 | 597.647 |
| exclude flagged instance | corner | 118 | 74 | 0 | 17.963 | 117 | 4283.308 | 71 | 2.360 | 551.941 |
| exclude flagged instance | eff | 118 | 74 | 0 | 17.670 | 117 | 4087.693 | 71 | 2.335 | 522.574 |

## Reference and error audit

- ex5_4_2.off.s1.log: status=None; rc=255; primal=None; dual=None; reference=7512.230145 =opt=; flags=[]
- kall_congruentcircles_c52.eff.s2.log: status=problem is solved [optimal solution found]; rc=0; primal=1.5371086884193; dual=1.5371086884193; reference=1.537110798 =opt=; flags=['reported optimum differs from =opt= reference']
Final dual bounds excluding reference: 0
Reported optimum mismatches at relative tolerance 1e-4: 0

## Paired comparisons

Ratios are geometric means of (X+shift)/(Y+shift), so <1 favours X. Tests use paired log ratios, with zero differences dropped. All-pair CPU uses the 300 s penalty; nodes are tested only on solved subsets. Per-seed p values treat instances as observations; pooled p values average the two log ratios within each instance first. Tests are exploratory, without multiplicity adjustment.

| scope | subset | X vs Y | n pairs | CPU shifted ratio | faster / slower >10% | CPU Wilcoxon n / p | node shifted ratio | nodes Wilcoxon n / p | solved only X / only Y | exact solved-count p |
|---|---|---|---|---|---|---|---|---|---|---|
| seed 1 | all | scip vs off | 60 | 0.9763 | 8 / 14 | 60 / 0.1788 | — | 0 / — | 2 / 1 | 1 |
| seed 1 | all settings solved | scip vs off | 36 | 1.1158 | 7 / 13 | 36 / 0.09082 | 1.0098 | 36 / 0.1768 | 2 / 1 | 1 |
| seed 1 | pair solved | scip vs off | 36 | 1.1158 | 7 / 13 | 36 / 0.09082 | 1.0098 | 36 / 0.1768 | 2 / 1 | 1 |
| seed 1 | all | corner vs off | 60 | 0.9653 | 9 / 11 | 60 / 0.5123 | — | 0 / — | 1 / 0 | 1 |
| seed 1 | all settings solved | corner vs off | 36 | 1.1211 | 7 / 11 | 36 / 0.2077 | 1.0139 | 36 / 0.5 | 1 / 0 | 1 |
| seed 1 | pair solved | corner vs off | 37 | 1.1001 | 8 / 11 | 37 / 0.3255 | 1.0047 | 37 / 0.6592 | 1 / 0 | 1 |
| seed 1 | all | eff vs off | 60 | 0.9272 | 13 / 9 | 60 / 0.8015 | — | 0 / — | 1 / 0 | 1 |
| seed 1 | all settings solved | eff vs off | 36 | 1.0619 | 11 / 9 | 36 / 0.7518 | 0.9368 | 36 / 0.633 | 1 / 0 | 1 |
| seed 1 | pair solved | eff vs off | 37 | 1.0303 | 12 / 9 | 37 / 0.9739 | 0.9145 | 37 / 0.4697 | 1 / 0 | 1 |
| seed 1 | all | corner vs scip | 60 | 0.9888 | 8 / 5 | 60 / 0.6213 | — | 0 / — | 1 / 1 | 1 |
| seed 1 | all settings solved | corner vs scip | 36 | 1.0047 | 7 / 5 | 36 / 0.7303 | 1.0040 | 36 / 0.381 | 1 / 1 | 1 |
| seed 1 | pair solved | corner vs scip | 37 | 1.0043 | 7 / 5 | 37 / 0.6919 | 1.0016 | 37 / 0.2914 | 1 / 1 | 1 |
| seed 1 | all | eff vs scip | 60 | 0.9497 | 10 / 1 | 60 / 0.07079 | — | 0 / — | 1 / 1 | 1 |
| seed 1 | all settings solved | eff vs scip | 36 | 0.9517 | 9 / 1 | 36 / 0.07594 | 0.9277 | 36 / 0.02 | 1 / 1 | 1 |
| seed 1 | pair solved | eff vs scip | 37 | 0.9530 | 9 / 1 | 37 / 0.07594 | 0.9255 | 37 / 0.01362 | 1 / 1 | 1 |
| seed 1 | all | eff vs corner | 60 | 0.9605 | 9 / 5 | 60 / 0.1954 | — | 0 / — | 0 / 0 | — |
| seed 1 | all settings solved | eff vs corner | 36 | 0.9472 | 8 / 5 | 36 / 0.2798 | 0.9239 | 36 / 0.1167 | 0 / 0 | — |
| seed 1 | pair solved | eff vs corner | 38 | 0.9384 | 9 / 5 | 38 / 0.1954 | 0.9106 | 38 / 0.05623 | 0 / 0 | — |
| seed 2 | all | scip vs off | 60 | 1.0541 | 4 / 10 | 60 / 0.07993 | — | 0 / — | 0 / 1 | 1 |
| seed 2 | all settings solved | scip vs off | 37 | 1.0846 | 4 / 9 | 37 / 0.1099 | 1.0000 | 37 / 0.07234 | 0 / 1 | 1 |
| seed 2 | pair solved | scip vs off | 37 | 1.0846 | 4 / 9 | 37 / 0.1099 | 1.0000 | 37 / 0.07234 | 0 / 1 | 1 |
| seed 2 | all | corner vs off | 60 | 0.9920 | 8 / 8 | 60 / 0.6877 | — | 0 / — | 0 / 0 | — |
| seed 2 | all settings solved | corner vs off | 37 | 0.9969 | 7 / 8 | 37 / 0.5008 | 0.8596 | 37 / 0.5329 | 0 / 0 | — |
| seed 2 | pair solved | corner vs off | 38 | 0.9873 | 8 / 8 | 38 / 0.6877 | 0.8552 | 38 / 0.414 | 0 / 0 | — |
| seed 2 | all | eff vs off | 60 | 1.0168 | 7 / 8 | 60 / 0.8187 | — | 0 / — | 0 / 0 | — |
| seed 2 | all settings solved | eff vs off | 37 | 1.0616 | 6 / 8 | 37 / 0.6117 | 0.8808 | 37 / 0.8325 | 0 / 0 | — |
| seed 2 | pair solved | eff vs off | 38 | 1.0266 | 7 / 8 | 38 / 0.8187 | 0.8467 | 38 / 0.6243 | 0 / 0 | — |
| seed 2 | all | corner vs scip | 60 | 0.9411 | 9 / 5 | 60 / 0.2137 | — | 0 / — | 1 / 0 | 1 |
| seed 2 | all settings solved | corner vs scip | 37 | 0.9192 | 8 / 5 | 37 / 0.3129 | 0.8596 | 37 / 0.05935 | 1 / 0 | 1 |
| seed 2 | pair solved | corner vs scip | 37 | 0.9192 | 8 / 5 | 37 / 0.3129 | 0.8596 | 37 / 0.05935 | 1 / 0 | 1 |
| seed 2 | all | eff vs scip | 60 | 0.9646 | 8 / 6 | 60 / 0.6219 | — | 0 / — | 1 / 0 | 1 |
| seed 2 | all settings solved | eff vs scip | 37 | 0.9788 | 7 / 6 | 37 / 0.8394 | 0.8808 | 37 / 0.2901 | 1 / 0 | 1 |
| seed 2 | pair solved | eff vs scip | 37 | 0.9788 | 7 / 6 | 37 / 0.8394 | 0.8808 | 37 / 0.2901 | 1 / 0 | 1 |
| seed 2 | all | eff vs corner | 60 | 1.0250 | 6 / 10 | 60 / 0.3862 | — | 0 / — | 0 / 0 | — |
| seed 2 | all settings solved | eff vs corner | 37 | 1.0649 | 5 / 10 | 37 / 0.224 | 1.0247 | 37 / 0.5083 | 0 / 0 | — |
| seed 2 | pair solved | eff vs corner | 38 | 1.0398 | 6 / 10 | 38 / 0.3862 | 0.9900 | 38 / 0.7457 | 0 / 0 | — |
| all pairs (instance-averaged tests) | all | scip vs off | 120 | 1.0144 | 12 / 24 | 60 / 0.04016 | — | 0 / — | 2 / 2 | — |
| all pairs (instance-averaged tests) | all settings solved | scip vs off | 73 | 1.0999 | 11 / 22 | 37 / 0.04601 | 1.0048 | 37 / 0.1087 | 2 / 2 | — |
| all pairs (instance-averaged tests) | pair solved | scip vs off | 73 | 1.0999 | 11 / 22 | 37 / 0.04601 | 1.0048 | 37 / 0.1087 | 2 / 2 | — |
| all pairs (instance-averaged tests) | all | corner vs off | 120 | 0.9786 | 17 / 19 | 60 / 0.3764 | — | 0 / — | 1 / 0 | — |
| all pairs (instance-averaged tests) | all settings solved | corner vs off | 73 | 1.0563 | 14 / 19 | 37 / 0.2347 | 0.9325 | 37 / 0.9678 | 1 / 0 | — |
| all pairs (instance-averaged tests) | pair solved | corner vs off | 75 | 1.0415 | 16 / 19 | 38 / 0.3677 | 0.9260 | 38 / 0.7979 | 1 / 0 | — |
| all pairs (instance-averaged tests) | all | eff vs off | 120 | 0.9710 | 20 / 17 | 60 / 0.9711 | — | 0 / — | 1 / 0 | — |
| all pairs (instance-averaged tests) | all settings solved | eff vs off | 73 | 1.0618 | 17 / 17 | 37 / 0.8151 | 0.9080 | 37 / 0.6807 | 1 / 0 | — |
| all pairs (instance-averaged tests) | pair solved | eff vs off | 75 | 1.0284 | 19 / 17 | 38 / 0.9826 | 0.8795 | 38 / 0.5016 | 1 / 0 | — |
| all pairs (instance-averaged tests) | all | corner vs scip | 120 | 0.9646 | 17 / 10 | 60 / 0.2655 | — | 0 / — | 2 / 1 | — |
| all pairs (instance-averaged tests) | all settings solved | corner vs scip | 73 | 0.9604 | 15 / 10 | 37 / 0.2878 | 0.9280 | 37 / 0.09407 | 2 / 1 | — |
| all pairs (instance-averaged tests) | pair solved | corner vs scip | 74 | 0.9608 | 15 / 10 | 37 / 0.296 | 0.9279 | 37 / 0.09407 | 2 / 1 | — |
| all pairs (instance-averaged tests) | all | eff vs scip | 120 | 0.9571 | 18 / 7 | 60 / 0.5785 | — | 0 / — | 2 / 1 | — |
| all pairs (instance-averaged tests) | all settings solved | eff vs scip | 73 | 0.9653 | 16 / 7 | 37 / 0.6671 | 0.9036 | 37 / 0.1315 | 2 / 1 | — |
| all pairs (instance-averaged tests) | pair solved | eff vs scip | 74 | 0.9658 | 16 / 7 | 37 / 0.6671 | 0.9029 | 37 / 0.1315 | 2 / 1 | — |
| all pairs (instance-averaged tests) | all | eff vs corner | 120 | 0.9922 | 15 / 15 | 60 / 0.9443 | — | 0 / — | 0 / 0 | — |
| all pairs (instance-averaged tests) | all settings solved | eff vs corner | 73 | 1.0051 | 13 / 15 | 37 / 0.8272 | 0.9737 | 37 / 0.966 | 0 / 0 | — |
| all pairs (instance-averaged tests) | pair solved | eff vs corner | 76 | 0.9878 | 15 / 15 | 38 / 0.9443 | 0.9495 | 38 / 0.8078 | 0 / 0 | — |

## Seed-to-seed variability

| setting | solved both | solved seed 1 only / seed 2 only | shifted CPU ratio seed 2 / 1 | median absolute log CPU ratio | CPU differs >10% | shifted node ratio seed 2 / 1 | median absolute log node ratio | nodes differ >10% |
|---|---|---|---|---|---|---|---|---|
| off | 37 | 0 / 1 | 0.9823 | 0.0351 | 14 | 0.9516 | 0.1043 | 19 |
| scip | 37 | 1 / 0 | 0.9901 | 0.0478 | 14 | 1.0188 | 0.0878 | 18 |
| corner | 38 | 0 / 0 | 0.9174 | 0.0652 | 16 | 0.8853 | 0.1154 | 19 |
| eff | 38 | 0 / 0 | 1.0166 | 0.0450 | 16 | 0.9625 | 0.1032 | 19 |

## Per-instance observations

| instance | seed | off CPU / nodes | scip CPU / nodes | corner CPU / nodes | eff CPU / nodes |
|---|---|---|---|---|---|
| blend531 | 1 | 43.35 / 13608.0 | 77.46 / 23537.0 | 116.02 / 40058.0 | 34.82 / 8165.0 |
| blend531 | 2 | 85.11 / 29590.0 | 133.65 / 37747.0 | 99.3 / 34576.0 | 78.42 / 23010.0 |
| blend852 | 1 | 219.26 / 57037.0 | TL 300.0 / 99192.0 | 121.86 / 41359.0 | 75.4 / 21905.0 |
| blend852 | 2 | 256.5 / 82370.0 | TL 300.0 / 101835.0 | 176.95 / 58150.0 | 75.6 / 16045.0 |
| carton9 | 1 | 27.73 / 5324.0 | 22.89 / 4798.0 | 20.26 / 4723.0 | 23.08 / 4493.0 |
| carton9 | 2 | 22.0 / 4773.0 | 21.18 / 4774.0 | 23.31 / 5057.0 | 21.42 / 5426.0 |
| crudeoil_lee1_09 | 1 | 12.45 / 185.0 | 12.31 / 97.0 | 12.09 / 112.0 | 10.6 / 98.0 |
| crudeoil_lee1_09 | 2 | 10.87 / 98.0 | 13.65 / 139.0 | 15.7 / 67.0 | 12.22 / 124.0 |
| crudeoil_pooling_ct2 | 1 | 26.34 / 6785.0 | 20.01 / 3217.0 | 16.13 / 3365.0 | 17.03 / 2142.0 |
| crudeoil_pooling_ct2 | 2 | 19.49 / 3761.0 | 31.13 / 7039.0 | 34.82 / 9666.0 | 15.25 / 962.0 |
| edgecross14-039 | 1 | 28.4 / 708.0 | 31.41 / 771.0 | 35.58 / 978.0 | 31.32 / 771.0 |
| edgecross14-039 | 2 | 35.0 / 1026.0 | 33.72 / 1051.0 | 39.14 / 1180.0 | 34.26 / 1051.0 |
| ex1264 | 1 | 0.1 / 1.0 | 0.08 / 1.0 | 0.07 / 1.0 | 0.05 / 1.0 |
| ex1264 | 2 | 0.1 / 1.0 | 0.1 / 1.0 | 0.08 / 1.0 | 0.09 / 1.0 |
| ex2_1_6 | 1 | 0.01 / 10.0 | 0.01 / 8.0 | 0.02 / 8.0 | 0.01 / 8.0 |
| ex2_1_6 | 2 | 0.0 / 10.0 | 0.01 / 8.0 | 0.0 / 8.0 | 0.02 / 8.0 |
| ex5_2_2_case1 | 1 | 0.01 / 35.0 | 0.03 / 92.0 | 0.03 / 33.0 | 0.02 / 34.0 |
| ex5_2_2_case1 | 2 | 0.02 / 35.0 | 0.03 / 66.0 | 0.03 / 31.0 | 0.02 / 35.0 |
| ex5_2_2_case3 | 1 | 0.02 / 18.0 | 0.01 / 9.0 | 0.01 / 17.0 | 0.01 / 19.0 |
| ex5_2_2_case3 | 2 | 0.01 / 18.0 | 0.01 / 19.0 | 0.02 / 21.0 | 0.01 / 19.0 |
| ex5_2_4 | 1 | 0.04 / 92.0 | 0.04 / 120.0 | 0.04 / 115.0 | 0.07 / 183.0 |
| ex5_2_4 | 2 | 0.06 / 92.0 | 0.04 / 119.0 | 0.04 / 115.0 | 0.07 / 198.0 |
| ex5_2_5 | 1 | TL 300.0 / 180516.0 | TL 300.0 / 164032.0 | TL 300.0 / 170434.0 | TL 300.0 / 169621.0 |
| ex5_2_5 | 2 | TL 300.0 / 180876.0 | TL 300.0 / 166267.0 | TL 300.0 / 165416.0 | TL 300.0 / 166465.0 |
| ex5_4_2 | 1 | ERROR None / None | 0.07 / 133.0 | 0.06 / 114.0 | 0.07 / 98.0 |
| ex5_4_2 | 2 | 3.3 / 5859.0 | 0.09 / 133.0 | 0.04 / 112.0 | 0.09 / 98.0 |
| ex8_3_2 | 1 | TL 300.0 / 41193.0 | TL 300.0 / 32723.0 | TL 300.0 / 36804.0 | TL 300.0 / 30820.0 |
| ex8_3_2 | 2 | TL 300.0 / 45113.0 | TL 300.0 / 36062.0 | TL 300.0 / 37143.0 | TL 300.0 / 22076.0 |
| ex8_3_9 | 1 | TL 300.0 / 77193.0 | TL 300.0 / 72756.0 | TL 300.0 / 76299.0 | TL 300.0 / 47481.0 |
| ex8_3_9 | 2 | TL 300.0 / 84159.0 | TL 300.0 / 69002.0 | TL 300.0 / 77553.0 | TL 300.0 / 68211.0 |
| gabriel01 | 1 | TL 300.0 / 68400.0 | TL 300.0 / 65680.0 | TL 300.0 / 65260.0 | TL 300.0 / 72591.0 |
| gabriel01 | 2 | TL 300.0 / 75089.0 | TL 300.0 / 67878.0 | TL 300.0 / 67615.0 | TL 300.0 / 77759.0 |
| gasprod_sarawak01 | 1 | 0.83 / 482.0 | 2.17 / 577.0 | 3.11 / 1257.0 | 2.3 / 764.0 |
| gasprod_sarawak01 | 2 | 1.05 / 546.0 | 1.98 / 650.0 | 1.36 / 235.0 | 2.42 / 720.0 |
| genpooling_lee2 | 1 | 5.72 / 2429.0 | 5.87 / 2860.0 | 5.77 / 2823.0 | 4.99 / 2147.0 |
| genpooling_lee2 | 2 | 5.69 / 2813.0 | 3.11 / 1275.0 | 2.69 / 936.0 | 5.8 / 2328.0 |
| genpooling_meyer04 | 1 | TL 300.0 / 165693.0 | TL 300.0 / 169478.0 | TL 300.0 / 155570.0 | TL 300.0 / 162985.0 |
| genpooling_meyer04 | 2 | TL 300.0 / 166948.0 | TL 300.0 / 153747.0 | TL 300.0 / 149387.0 | TL 300.0 / 160271.0 |
| kall_circlespolygons_c1p11 | 1 | 0.62 / 461.0 | 0.09 / 25.0 | 0.13 / 25.0 | 0.11 / 20.0 |
| kall_circlespolygons_c1p11 | 2 | 0.07 / 20.0 | 0.11 / 35.0 | 0.12 / 35.0 | 0.09 / 20.0 |
| kall_circlesrectangles_c6r1 | 1 | TL 300.0 / 54582.0 | TL 300.0 / 41294.0 | TL 300.0 / 45258.0 | TL 300.0 / 41400.0 |
| kall_circlesrectangles_c6r1 | 2 | TL 300.0 / 46852.0 | TL 300.0 / 44469.0 | TL 300.0 / 44973.0 | TL 300.0 / 46021.0 |
| kall_congruentcircles_c52 | 1 | 1.24 / 1569.0 | 2.07 / 2203.0 | 1.64 / 1910.0 | 2.06 / 2419.0 |
| kall_congruentcircles_c52 | 2 | 1.57 / 1940.0 | 1.68 / 2067.0 | 1.0 / 1206.0 | 3.27 / 3830.0 |
| kall_diffcircles_10 | 1 | TL 300.0 / 249337.0 | TL 300.0 / 234993.0 | TL 300.0 / 234789.0 | TL 300.0 / 227407.0 |
| kall_diffcircles_10 | 2 | TL 300.0 / 248362.0 | TL 300.0 / 240190.0 | TL 300.0 / 239016.0 | TL 300.0 / 234829.0 |
| kall_diffcircles_5b | 1 | 5.61 / 9516.0 | 7.8 / 15197.0 | 9.72 / 14024.0 | 7.35 / 10518.0 |
| kall_diffcircles_5b | 2 | 8.07 / 14381.0 | 12.69 / 22104.0 | 6.24 / 8888.0 | 8.41 / 12816.0 |
| kall_diffcircles_6 | 1 | 5.94 / 8760.0 | 7.92 / 11298.0 | 6.23 / 8037.0 | 4.99 / 6105.0 |
| kall_diffcircles_6 | 2 | 5.29 / 7227.0 | 6.54 / 8080.0 | 5.24 / 6219.0 | 6.56 / 8395.0 |
| ndcc16persp | 1 | TL 300.0 / 26949.0 | TL 300.0 / 15909.0 | TL 300.0 / 14612.0 | TL 300.0 / 17987.0 |
| ndcc16persp | 2 | TL 300.0 / 17219.0 | TL 300.0 / 14489.0 | TL 300.0 / 14036.0 | TL 300.0 / 14173.0 |
| nvs17 | 1 | 2.59 / 159.0 | 2.23 / 164.0 | 2.22 / 159.0 | 1.93 / 89.0 |
| nvs17 | 2 | 1.98 / 131.0 | 2.11 / 164.0 | 2.24 / 149.0 | 2.0 / 101.0 |
| nvs24 | 1 | 10.87 / 1113.0 | 12.78 / 2142.0 | 10.1 / 1444.0 | 11.25 / 2149.0 |
| nvs24 | 2 | 10.92 / 843.0 | 11.25 / 2605.0 | 11.8 / 2869.0 | 9.19 / 989.0 |
| pointpack04 | 1 | 0.02 / 9.0 | 0.05 / 14.0 | 0.06 / 14.0 | 0.05 / 14.0 |
| pointpack04 | 2 | 0.04 / 12.0 | 0.06 / 14.0 | 0.06 / 14.0 | 0.06 / 14.0 |
| pointpack08 | 1 | 52.49 / 34922.0 | 72.21 / 43588.0 | 72.59 / 43588.0 | 70.17 / 43588.0 |
| pointpack08 | 2 | 56.99 / 37656.0 | 55.43 / 35314.0 | 55.21 / 35314.0 | 55.46 / 35314.0 |
| pointpack12 | 1 | TL 300.0 / 86236.0 | TL 300.0 / 80601.0 | TL 300.0 / 81798.0 | TL 300.0 / 85296.0 |
| pointpack12 | 2 | TL 300.0 / 88105.0 | TL 300.0 / 83398.0 | TL 300.0 / 85090.0 | TL 300.0 / 86180.0 |
| pooling_adhya1pq | 1 | 0.27 / 445.0 | 0.5 / 771.0 | 0.46 / 599.0 | 0.4 / 410.0 |
| pooling_adhya1pq | 2 | 0.32 / 488.0 | 0.43 / 602.0 | 0.36 / 411.0 | 0.37 / 506.0 |
| pooling_bental4pq | 1 | 0.01 / 4.0 | 0.04 / 30.0 | 0.04 / 15.0 | 0.05 / 31.0 |
| pooling_bental4pq | 2 | 0.02 / 4.0 | 0.05 / 25.0 | 0.02 / 15.0 | 0.05 / 31.0 |
| pooling_bental5tp | 1 | 0.74 / 497.0 | 1.64 / 836.0 | 1.03 / 528.0 | 1.27 / 552.0 |
| pooling_bental5tp | 2 | 0.68 / 339.0 | 0.65 / 261.0 | 1.08 / 480.0 | 1.58 / 859.0 |
| pooling_foulds4pq | 1 | 0.71 / 21.0 | 6.15 / 57.0 | 4.73 / 66.0 | 2.64 / 23.0 |
| pooling_foulds4pq | 2 | 0.76 / 21.0 | 1.62 / 30.0 | 5.82 / 95.0 | 7.26 / 39.0 |
| pooling_foulds5pq | 1 | 1.56 / 84.0 | 13.52 / 174.0 | 23.99 / 627.0 | 33.21 / 1125.0 |
| pooling_foulds5pq | 2 | 1.45 / 116.0 | 24.75 / 462.0 | 10.04 / 329.0 | 21.87 / 92.0 |
| pooling_rt2pq | 1 | 0.18 / 224.0 | 0.21 / 220.0 | 0.29 / 212.0 | 0.28 / 198.0 |
| pooling_rt2pq | 2 | 0.18 / 227.0 | 0.22 / 207.0 | 0.21 / 149.0 | 0.43 / 398.0 |
| qp3 | 1 | TL 300.0 / 21048.0 | TL 300.0 / 21650.0 | TL 300.0 / 19691.0 | TL 300.0 / 19962.0 |
| qp3 | 2 | TL 300.0 / 4723.0 | TL 300.0 / 4673.0 | TL 300.0 / 4222.0 | TL 300.0 / 4692.0 |
| space25 | 1 | TL 300.0 / 64750.0 | TL 300.0 / 62658.0 | TL 300.0 / 66712.0 | TL 300.0 / 64517.0 |
| space25 | 2 | TL 300.0 / 66517.0 | TL 300.0 / 65300.0 | TL 300.0 / 65070.0 | TL 300.0 / 70594.0 |
| sssd16-07persp | 1 | TL 300.0 / 415544.0 | TL 300.0 / 191279.0 | TL 300.0 / 273100.0 | TL 300.0 / 303268.0 |
| sssd16-07persp | 2 | TL 300.01 / 402300.0 | TL 300.0 / 206226.0 | TL 300.0 / 324369.0 | TL 300.0 / 304541.0 |
| sssd18-08persp | 1 | TL 300.0 / 317213.0 | TL 300.0 / 295919.0 | TL 300.01 / 292128.0 | TL 300.0 / 293881.0 |
| sssd18-08persp | 2 | TL 300.0 / 331506.0 | TL 300.01 / 296582.0 | TL 300.0 / 271274.0 | TL 300.0 / 259901.0 |
| sssd20-04persp | 1 | TL 300.01 / 487291.0 | TL 300.01 / 561554.0 | TL 300.01 / 543082.0 | TL 300.01 / 578994.0 |
| sssd20-04persp | 2 | TL 300.01 / 521522.0 | TL 300.01 / 537371.0 | TL 300.0 / 478749.0 | TL 300.01 / 591573.0 |
| sssd25-08persp | 1 | TL 300.01 / 282179.0 | TL 300.01 / 236085.0 | TL 300.0 / 212790.0 | TL 300.0 / 213508.0 |
| sssd25-08persp | 2 | TL 300.0 / 226825.0 | TL 300.01 / 247595.0 | TL 300.01 / 218823.0 | TL 300.01 / 226497.0 |
| st_e07 | 1 | 0.0 / 4.0 | 0.02 / 7.0 | 0.01 / 4.0 | 0.01 / 5.0 |
| st_e07 | 2 | 0.01 / 4.0 | 0.0 / 7.0 | 0.01 / 9.0 | 0.01 / 4.0 |
| st_e31 | 1 | 0.84 / 773.0 | 0.82 / 872.0 | 0.87 / 621.0 | 0.91 / 865.0 |
| st_e31 | 2 | 0.74 / 673.0 | 0.74 / 755.0 | 0.75 / 808.0 | 0.6 / 730.0 |
| st_fp7e | 1 | 1.07 / 3673.0 | 0.37 / 1198.0 | 0.33 / 1198.0 | 0.36 / 1198.0 |
| st_fp7e | 2 | 1.05 / 3673.0 | 0.39 / 1198.0 | 0.38 / 1198.0 | 0.39 / 1198.0 |
| st_glmp_fp2 | 1 | 0.01 / 10.0 | 0.01 / 10.0 | 0.0 / 9.0 | 0.01 / 6.0 |
| st_glmp_fp2 | 2 | 0.0 / 10.0 | 0.02 / 10.0 | 0.01 / 9.0 | 0.01 / 6.0 |
| st_glmp_fp3 | 1 | 0.0 / 3.0 | 0.01 / 3.0 | 0.01 / 3.0 | 0.01 / 1.0 |
| st_glmp_fp3 | 2 | 0.01 / 3.0 | 0.01 / 3.0 | 0.01 / 3.0 | 0.01 / 1.0 |
| st_qpc-m3a | 1 | 2.56 / 5427.0 | 0.99 / 2775.0 | 1.05 / 2775.0 | 1.04 / 2775.0 |
| st_qpc-m3a | 2 | 2.48 / 5419.0 | 1.1 / 3027.0 | 1.07 / 3027.0 | 1.15 / 3027.0 |
| st_qpk3 | 1 | 0.06 / 142.0 | 0.08 / 144.0 | 0.06 / 144.0 | 0.03 / 144.0 |
| st_qpk3 | 2 | 0.04 / 140.0 | 0.06 / 137.0 | 0.06 / 137.0 | 0.05 / 137.0 |
| st_robot | 1 | 0.01 / 8.0 | 0.01 / 7.0 | 0.01 / 7.0 | 0.02 / 1.0 |
| st_robot | 2 | 0.01 / 8.0 | 0.01 / 7.0 | 0.01 / 7.0 | 0.01 / 1.0 |
| st_rv9 | 1 | 0.75 / 1517.0 | 1.1 / 2368.0 | 1.2 / 2368.0 | 1.12 / 2368.0 |
| st_rv9 | 2 | 0.99 / 1971.0 | 0.85 / 1773.0 | 0.87 / 1773.0 | 0.92 / 1773.0 |
| tln12 | 1 | TL 300.0 / 104031.0 | TL 300.0 / 110129.0 | TL 300.0 / 88110.0 | TL 300.0 / 90169.0 |
| tln12 | 2 | TL 300.0 / 100803.0 | TL 300.0 / 94588.0 | TL 300.0 / 83302.0 | TL 300.0 / 101065.0 |
| tln7 | 1 | TL 300.0 / 280364.0 | 283.04 / 308290.0 | TL 300.01 / 258490.0 | TL 300.05 / 212663.0 |
| tln7 | 2 | TL 300.0 / 295740.0 | TL 300.0 / 256678.0 | TL 300.0 / 263708.0 | TL 300.0 / 254868.0 |
| wastewater11m2 | 1 | TL 300.0 / 45262.0 | TL 300.0 / 41591.0 | TL 300.0 / 47154.0 | TL 300.0 / 55819.0 |
| wastewater11m2 | 2 | TL 300.71 / 43465.0 | TL 300.0 / 43675.0 | TL 300.0 / 42712.0 | TL 300.0 / 46076.0 |
| wastewater12m2 | 1 | TL 300.0 / 31858.0 | TL 300.0 / 27044.0 | TL 300.0 / 24602.0 | TL 300.0 / 29973.0 |
| wastewater12m2 | 2 | TL 300.0 / 29447.0 | TL 300.0 / 25036.0 | TL 300.0 / 25780.0 | TL 300.0 / 26114.0 |
| wastewater15m1 | 1 | 46.36 / 51937.0 | 22.54 / 22654.0 | 21.22 / 21608.0 | 22.96 / 21608.0 |
| wastewater15m1 | 2 | 15.52 / 16019.0 | 35.18 / 47771.0 | 3.37 / 3315.0 | 6.43 / 6879.0 |
| waterund08 | 1 | TL 300.0 / 188844.0 | TL 300.0 / 198726.0 | TL 300.0 / 209208.0 | TL 300.0 / 208186.0 |
| waterund08 | 2 | TL 300.0 / 194366.0 | TL 300.0 / 216997.0 | TL 300.0 / 211127.0 | TL 300.0 / 197867.0 |
| waterund18 | 1 | TL 300.0 / 154561.0 | TL 300.0 / 147163.0 | TL 300.0 / 154468.0 | TL 300.0 / 143646.0 |
| waterund18 | 2 | TL 300.0 / 146642.0 | TL 300.0 / 130026.0 | TL 300.0 / 143194.0 | TL 300.0 / 142707.0 |
| waterund27 | 1 | TL 300.0 / 10480.0 | TL 300.0 / 8651.0 | TL 300.0 / 9581.0 | TL 300.0 / 8563.0 |
| waterund27 | 2 | TL 300.0 / 9513.0 | TL 300.0 / 10468.0 | TL 300.0 / 10178.0 | TL 300.0 / 9759.0 |
