### Root dual bounds better than the MINLPLib reference

| instance | setting | seed | root dual | ref | tag | status |
|---|---|---|---|---|---|---|
| tricp | eff | 2 | 1.698604319e-05 | 0 | =opt= | solving was interrupted [node limit reached] |

### Seed 0: settings off, scip, corner, eff, scipS, cornerS, effS

Instances: 335 with a root run; 302 complete (no time limit or error in any setting).

| setting | n | mean RGC | median RGC | mean root CPU s | sgm root CPU s (shift 1) | cuts gen. (sum) | cuts in LP at root (sum) | select time (sum s) | intercut time (sum s) |
|---|---|---|---|---|---|---|---|---|---|
| off | 251 | 0.3330 | 0.2000 | 3.34 | 0.97 | 0 | 0 | 0.0 | 0.0 |
| scip | 251 | 0.4469 | 0.4092 | 4.41 | 1.20 | 95181 | 13113 | 0.0 | 167.6 |
| corner | 251 | 0.4389 | 0.4145 | 4.58 | 1.26 | 95657 | 12826 | 40.8 | 202.8 |
| eff | 251 | 0.4482 | 0.4170 | 4.45 | 1.23 | 95131 | 13216 | 43.9 | 205.1 |
| scipS | 251 | 0.4530 | 0.4171 | 6.38 | 1.52 | 91307 | 13168 | 0.0 | 665.7 |
| cornerS | 251 | 0.4455 | 0.4170 | 7.48 | 1.68 | 94886 | 13923 | 39.0 | 909.1 |
| effS | 251 | 0.4526 | 0.4219 | 6.93 | 1.60 | 91870 | 13439 | 42.7 | 845.8 |

Paired differences D(X,Y) of RGC on the 251 common complete instances:

| X vs Y | mean D | median D | X better by > 0.01 | X worse by > 0.01 | Wilcoxon p (two-sided) |
|---|---|---|---|---|---|
| scip vs off | +0.1139 | +0.0023 | 110 | 16 | 5.45e-17 |
| corner vs off | +0.1058 | +0.0023 | 111 | 14 | 1.76e-17 |
| eff vs off | +0.1152 | +0.0033 | 114 | 15 | 1.39e-18 |
| corner vs scip | -0.0080 | +0.0000 | 30 | 41 | 0.0708 |
| eff vs scip | +0.0013 | +0.0000 | 33 | 33 | 0.996 |
| eff vs corner | +0.0094 | +0.0000 | 45 | 31 | 0.054 |
| scipS vs scip | +0.0061 | +0.0000 | 26 | 18 | 0.0828 |
| cornerS vs scipS | -0.0075 | +0.0000 | 29 | 44 | 0.0261 |
| effS vs scipS | -0.0004 | +0.0000 | 35 | 32 | 0.565 |

### Seed 1: settings off, scip, corner, eff

Instances: 335 with a root run; 302 complete (no time limit or error in any setting).

| setting | n | mean RGC | median RGC | mean root CPU s | sgm root CPU s (shift 1) | cuts gen. (sum) | cuts in LP at root (sum) | select time (sum s) | intercut time (sum s) |
|---|---|---|---|---|---|---|---|---|---|
| off | 250 | 0.3310 | 0.1907 | 4.48 | 1.12 | 0 | 0 | 0.0 | 0.0 |
| scip | 250 | 0.4349 | 0.3987 | 5.27 | 1.38 | 94015 | 13098 | 0.0 | 188.0 |
| corner | 250 | 0.4274 | 0.3836 | 5.38 | 1.44 | 93368 | 13207 | 45.3 | 235.7 |
| eff | 250 | 0.4382 | 0.3902 | 5.36 | 1.42 | 90995 | 12673 | 48.5 | 240.6 |

Paired differences D(X,Y) of RGC on the 250 common complete instances:

| X vs Y | mean D | median D | X better by > 0.01 | X worse by > 0.01 | Wilcoxon p (two-sided) |
|---|---|---|---|---|---|
| scip vs off | +0.1039 | +0.0026 | 109 | 15 | 3.51e-18 |
| corner vs off | +0.0964 | +0.0008 | 107 | 18 | 2.2e-15 |
| eff vs off | +0.1072 | +0.0028 | 107 | 21 | 1.48e-16 |
| corner vs scip | -0.0074 | +0.0000 | 27 | 40 | 0.0621 |
| eff vs scip | +0.0033 | +0.0000 | 31 | 30 | 0.427 |
| eff vs corner | +0.0107 | +0.0000 | 51 | 24 | 0.00186 |

### Seed 2: settings off, scip, corner, eff

Instances: 335 with a root run; 301 complete (no time limit or error in any setting).

| setting | n | mean RGC | median RGC | mean root CPU s | sgm root CPU s (shift 1) | cuts gen. (sum) | cuts in LP at root (sum) | select time (sum s) | intercut time (sum s) |
|---|---|---|---|---|---|---|---|---|---|
| off | 248 | 0.3338 | 0.1966 | 3.95 | 1.07 | 0 | 0 | 0.0 | 0.0 |
| scip | 248 | 0.4398 | 0.4145 | 5.00 | 1.34 | 90814 | 13174 | 0.0 | 186.7 |
| corner | 248 | 0.4302 | 0.3954 | 5.38 | 1.42 | 93929 | 13930 | 46.6 | 242.7 |
| eff | 248 | 0.4356 | 0.4095 | 5.44 | 1.41 | 93117 | 13681 | 50.7 | 252.8 |

Paired differences D(X,Y) of RGC on the 248 common complete instances:

| X vs Y | mean D | median D | X better by > 0.01 | X worse by > 0.01 | Wilcoxon p (two-sided) |
|---|---|---|---|---|---|
| scip vs off | +0.1060 | +0.0034 | 103 | 21 | 1.03e-15 |
| corner vs off | +0.0964 | +0.0002 | 103 | 21 | 2.1e-14 |
| eff vs off | +0.1018 | +0.0026 | 108 | 22 | 4.32e-15 |
| corner vs scip | -0.0096 | +0.0000 | 29 | 44 | 0.0113 |
| eff vs scip | -0.0042 | +0.0000 | 27 | 39 | 0.107 |
| eff vs corner | +0.0054 | +0.0000 | 44 | 30 | 0.0617 |

### Seed variation of RGC (same setting, different permutation seeds)

| setting | seeds | n | mean abs diff | diff > 0.01 (either sign) |
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
