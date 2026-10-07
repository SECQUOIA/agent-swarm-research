## Root benchmark (own parser)

runs: 4869; return codes: {'0': 4869}; runs with an ERROR line: 0; statuses: {'solving was interrupted [node limit reached]': 4236, 'solving was interrupted [time limit reached]': 177, 'problem is solved [optimal solution found]': 456}

objective-sense mismatches between log and instancedata.csv: 0

root dual bounds beyond the reference by > 1e-6 max(1,|ref|): [('tricp', 'eff', 2, 1.69860431924462e-05, 0.0, '=opt=')]

### Seed 0

instances run: 347; complete in all settings: 305 (with a reference: 302); common with RGC defined: 251; instances whose first LP value differs between settings: 0

RGC values outside [0,1]: []

| setting | n | mean RGC | median RGC | sgm CPU (shift 1) | cuts gen | root-LP cuts | select s | intercut s |
|---|---|---|---|---|---|---|---|---|
| off | 251 | 0.3330 | 0.2000 | 0.968 | 0 | 0 | 0.0 | 0.0 |
| scip | 251 | 0.4469 | 0.4092 | 1.203 | 95181 | 13113 | 0.0 | 167.6 |
| corner | 251 | 0.4389 | 0.4145 | 1.256 | 95657 | 12826 | 40.8 | 202.8 |
| eff | 251 | 0.4482 | 0.4170 | 1.231 | 95131 | 13216 | 43.9 | 205.1 |
| scipS | 251 | 0.4530 | 0.4171 | 1.519 | 91307 | 13168 | 0.0 | 665.7 |
| cornerS | 251 | 0.4455 | 0.4170 | 1.682 | 94886 | 13923 | 39.0 | 909.1 |
| effS | 251 | 0.4526 | 0.4219 | 1.597 | 91870 | 13439 | 42.7 | 845.8 |

| X vs Y | n | mean D | median D | better>0.01 | worse>0.01 | Wilcoxon p (zeros dropped, |D|>1e-9) | p (zero_method=wilcox on raw D) |
|---|---|---|---|---|---|---|---|
| scip vs off | 251 | +0.1139 | +0.0023 | 110 | 16 | 5.45e-17 | 6.13e-17 |
| corner vs off | 251 | +0.1058 | +0.0023 | 111 | 14 | 1.76e-17 | 2.12e-17 |
| eff vs off | 251 | +0.1152 | +0.0033 | 114 | 15 | 1.39e-18 | 1.56e-18 |
| corner vs scip | 251 | -0.0080 | +0.0000 | 30 | 41 | 0.0708 | 0.0712 |
| eff vs scip | 251 | +0.0013 | +0.0000 | 33 | 33 | 0.996 | 0.975 |
| eff vs corner | 251 | +0.0094 | +0.0000 | 45 | 31 | 0.054 | 0.0559 |
| scipS vs scip | 251 | +0.0061 | +0.0000 | 26 | 18 | 0.0828 | 0.0933 |
| cornerS vs scipS | 251 | -0.0075 | +0.0000 | 29 | 44 | 0.0261 | 0.0282 |
| effS vs scipS | 251 | -0.0004 | +0.0000 | 35 | 32 | 0.565 | 0.567 |

### Seed 1

instances run: 305; complete in all settings: 305 (with a reference: 302); common with RGC defined: 250; instances whose first LP value differs between settings: 0

RGC values outside [0,1]: []

| setting | n | mean RGC | median RGC | sgm CPU (shift 1) | cuts gen | root-LP cuts | select s | intercut s |
|---|---|---|---|---|---|---|---|---|
| off | 250 | 0.3310 | 0.1907 | 1.120 | 0 | 0 | 0.0 | 0.0 |
| scip | 250 | 0.4349 | 0.3987 | 1.378 | 94015 | 13098 | 0.0 | 188.0 |
| corner | 250 | 0.4274 | 0.3836 | 1.437 | 93368 | 13207 | 45.3 | 235.7 |
| eff | 250 | 0.4382 | 0.3902 | 1.422 | 90995 | 12673 | 48.5 | 240.6 |

| X vs Y | n | mean D | median D | better>0.01 | worse>0.01 | Wilcoxon p (zeros dropped, |D|>1e-9) | p (zero_method=wilcox on raw D) |
|---|---|---|---|---|---|---|---|
| scip vs off | 250 | +0.1039 | +0.0026 | 109 | 15 | 3.51e-18 | 2.27e-18 |
| corner vs off | 250 | +0.0964 | +0.0008 | 107 | 18 | 2.2e-15 | 1.67e-15 |
| eff vs off | 250 | +0.1072 | +0.0028 | 107 | 21 | 1.48e-16 | 1.12e-16 |
| corner vs scip | 250 | -0.0074 | +0.0000 | 27 | 40 | 0.0621 | 0.0616 |
| eff vs scip | 250 | +0.0033 | +0.0000 | 31 | 30 | 0.427 | 0.419 |
| eff vs corner | 250 | +0.0107 | +0.0000 | 51 | 24 | 0.00186 | 0.00184 |

### Seed 2

instances run: 305; complete in all settings: 304 (with a reference: 301); common with RGC defined: 248; instances whose first LP value differs between settings: 0

RGC values outside [0,1]: []

| setting | n | mean RGC | median RGC | sgm CPU (shift 1) | cuts gen | root-LP cuts | select s | intercut s |
|---|---|---|---|---|---|---|---|---|
| off | 248 | 0.3338 | 0.1966 | 1.066 | 0 | 0 | 0.0 | 0.0 |
| scip | 248 | 0.4398 | 0.4145 | 1.339 | 90814 | 13174 | 0.0 | 186.7 |
| corner | 248 | 0.4302 | 0.3954 | 1.415 | 93929 | 13930 | 46.6 | 242.7 |
| eff | 248 | 0.4356 | 0.4095 | 1.411 | 93117 | 13681 | 50.7 | 252.8 |

| X vs Y | n | mean D | median D | better>0.01 | worse>0.01 | Wilcoxon p (zeros dropped, |D|>1e-9) | p (zero_method=wilcox on raw D) |
|---|---|---|---|---|---|---|---|
| scip vs off | 248 | +0.1060 | +0.0034 | 103 | 21 | 1.03e-15 | 9.38e-16 |
| corner vs off | 248 | +0.0964 | +0.0002 | 103 | 21 | 2.1e-14 | 3.14e-14 |
| eff vs off | 248 | +0.1018 | +0.0026 | 108 | 22 | 4.32e-15 | 4.92e-15 |
| corner vs scip | 248 | -0.0096 | +0.0000 | 29 | 44 | 0.0113 | 0.0111 |
| eff vs scip | 248 | -0.0042 | +0.0000 | 27 | 39 | 0.107 | 0.112 |
| eff vs corner | 248 | +0.0054 | +0.0000 | 44 | 30 | 0.0617 | 0.0626 |

seed-averaged D(corner,scip) over 248 instances common to all seeds: mean -0.0085, better/worse > 0.01: 22/46, Wilcoxon p 0.00191
seed-averaged D(eff,scip) over 248 instances common to all seeds: mean +0.0001, better/worse > 0.01: 27/33, Wilcoxon p 0.852

seed 0 scip vs off: top 25 instances contribute 65.7% of the total RGC gain; median +0.0023

### Seed noise (same setting, two seeds, both complete with defined RGC)

| setting | seeds | n | mean abs diff | n abs diff > 0.01 |
|---|---|---|---|---|
| off | 0 vs 1 | 267 | 0.0091 | 41 |
| off | 0 vs 2 | 266 | 0.0095 | 42 |
| off | 1 vs 2 | 266 | 0.0096 | 34 |
| scip | 0 vs 1 | 251 | 0.0202 | 63 |
| scip | 0 vs 2 | 251 | 0.0212 | 66 |
| scip | 1 vs 2 | 250 | 0.0151 | 60 |
| corner | 0 vs 1 | 252 | 0.0220 | 64 |
| corner | 0 vs 2 | 250 | 0.0235 | 62 |
| corner | 1 vs 2 | 250 | 0.0131 | 63 |
| eff | 0 vs 1 | 250 | 0.0214 | 72 |
| eff | 0 vs 2 | 249 | 0.0195 | 60 |
| eff | 1 vs 2 | 249 | 0.0126 | 62 |

## Full solves (own parser)

runs: 480, instances 60; rc: {'0': 479, '255': 1}; statuses: {'problem is solved [optimal solution found]': 302, 'solving was interrupted [time limit reached]': 177, None: 1}; runs with ERROR line: [('ex5_4_2', 'off', 1)]

nonzero return codes: [(('ex5_4_2', 'off', 1), '255', None)]

### seed 1

| setting | solved/runs | CPU sgm | nodes n | nodes sgm | all-solved n | CPU sgm there | nodes sgm there |
|---|---|---|---|---|---|---|---|
| off | 37/60 | 18.490 | 59 | 4739.2 | 36 | 2.170 | 617.6 |
| scip | 38/60 | 18.028 | 59 | 4609.9 | 36 | 2.537 | 624.7 |
| corner | 38/60 | 17.814 | 59 | 4563.0 | 36 | 2.554 | 627.6 |
| eff | 38/60 | 17.071 | 59 | 4280.1 | 36 | 2.366 | 572.3 |

### seed 2

| setting | solved/runs | CPU sgm | nodes n | nodes sgm | all-solved n | CPU sgm there | nodes sgm there |
|---|---|---|---|---|---|---|---|
| off | 38/60 | 16.959 | 60 | 4447.1 | 37 | 2.127 | 616.0 |
| scip | 37/60 | 17.930 | 60 | 4315.9 | 37 | 2.391 | 616.0 |
| corner | 38/60 | 16.815 | 60 | 3890.1 | 37 | 2.117 | 515.4 |
| eff | 38/60 | 17.260 | 60 | 3868.8 | 37 | 2.319 | 530.6 |

### seeds 1 + 2

| setting | solved/runs | CPU sgm | nodes n | nodes sgm | all-solved n | CPU sgm there | nodes sgm there |
|---|---|---|---|---|---|---|---|
| off | 75/120 | 17.709 | 119 | 4589.6 | 73 | 2.148 | 616.8 |
| scip | 75/120 | 17.979 | 119 | 4459.3 | 73 | 2.462 | 620.3 |
| corner | 76/120 | 17.308 | 119 | 4210.6 | 73 | 2.325 | 568.4 |
| eff | 76/120 | 17.166 | 119 | 4067.6 | 73 | 2.342 | 550.8 |

### excluding the pair ex5_4_2 seed 1

| setting | solved/runs | CPU sgm | nodes n | nodes sgm | all-solved n | CPU sgm there | nodes sgm there |
|---|---|---|---|---|---|---|---|
| off | 75/119 | 17.277 | 119 | 4589.6 | 73 | 2.148 | 616.8 |
| scip | 74/119 | 18.443 | 119 | 4459.3 | 73 | 2.462 | 620.3 |
| corner | 75/119 | 17.751 | 119 | 4210.6 | 73 | 2.325 | 568.4 |
| eff | 75/119 | 17.603 | 119 | 4067.6 | 73 | 2.342 | 550.8 |

### excluding kall_congruentcircles_c52

| setting | solved/runs | CPU sgm | nodes n | nodes sgm | all-solved n | CPU sgm there | nodes sgm there |
|---|---|---|---|---|---|---|---|
| off | 73/118 | 18.372 | 117 | 4665.0 | 71 | 2.172 | 597.9 |
| scip | 73/118 | 18.597 | 117 | 4515.2 | 71 | 2.481 | 597.6 |
| corner | 74/118 | 17.963 | 117 | 4283.3 | 71 | 2.360 | 551.9 |
| eff | 74/118 | 17.670 | 117 | 4087.7 | 71 | 2.335 | 522.6 |

### Solved-set differences (pairs solved by X but not Y)

- off only: []; corner only: [('ex5_4_2', 1)]
- off only: []; eff only: [('ex5_4_2', 1)]
- scip only: [('ex5_4_2', 1), ('tln7', 1)]; off only: [('blend852', 1), ('blend852', 2)]
- scip only: [('tln7', 1)]; corner only: [('blend852', 1), ('blend852', 2)]
- scip only: [('tln7', 1)]; eff only: [('blend852', 1), ('blend852', 2)]
- eff only: []; corner only: []

solved runs with CPU > 150 s (sensitive to the limit): [(176.95, 'blend852', 'corner', 2), (219.26, 'blend852', 'off', 1), (256.5, 'blend852', 'off', 2), (283.04, 'tln7', 'scip', 1)]

### Paired comparisons (shifted ratios; Wilcoxon on instance-averaged log ratios)

| X vs Y | all-pair CPU ratio | p (60 inst) | common-solved CPU ratio | p | common-solved node ratio | p |
|---|---|---|---|---|---|---|
| scip vs off | 1.0144 | 0.0402 | 1.0999 | 0.046 (n=37) | 1.0048 | 0.109 |
| corner vs off | 0.9786 | 0.376 | 1.0563 | 0.235 (n=37) | 0.9325 | 0.968 |
| eff vs off | 0.9710 | 0.971 | 1.0618 | 0.815 (n=37) | 0.9080 | 0.681 |
| corner vs scip | 0.9646 | 0.265 | 0.9604 | 0.288 (n=37) | 0.9280 | 0.0941 |
| eff vs scip | 0.9571 | 0.578 | 0.9653 | 0.667 (n=37) | 0.9036 | 0.131 |
| eff vs corner | 0.9922 | 0.944 | 1.0051 | 0.827 (n=37) | 0.9737 | 0.966 |

### Reference checks

- reported optimum differs: kall_congruentcircles_c52 eff s2 primal 1.537108688419 ref 1.537110798 (=opt=) diff -2.11e-06

