### Files

| status | files |
|---|---|
| ok | 1601 |
| unsupported operator | 31 |

Skipped files:

- `ann_compressor_tanh`: unsupported operator: tanh
- `ann_cumene_tanh`: unsupported operator: tanh
- `ann_fermentation_tanh`: unsupported operator: tanh
- `ann_peaks_tanh`: unsupported operator: tanh
- `blendgap`: unsupported operator: erf
- `dosemin2d`: unsupported operator: erf
- `dosemin3d`: unsupported operator: erf
- `filter`: unsupported operator: log10
- `fuzzy`: unsupported operator: min
- `gastransnlp`: unsupported operator: signpower
- `oil`: unsupported operator: log10
- `oil2`: unsupported operator: log10
- `quantum`: unsupported operator: gammaFn
- `waternd_blacksburg`: unsupported operator: signpower
- `waternd_fossiron`: unsupported operator: signpower
- `waternd_fosspoly0`: unsupported operator: signpower
- `waternd_fosspoly1`: unsupported operator: signpower
- `waternd_hanoi`: unsupported operator: signpower
- `waternd_modena`: unsupported operator: signpower
- `waternd_pescara`: unsupported operator: signpower
- `waternd_shamir`: unsupported operator: signpower
- `waterno1_01`: unsupported operator: signpower
- `waterno1_02`: unsupported operator: signpower
- `waterno1_03`: unsupported operator: signpower
- `waterno1_04`: unsupported operator: signpower
- `waterno1_06`: unsupported operator: signpower
- `waterno1_09`: unsupported operator: signpower
- `waterno1_12`: unsupported operator: signpower
- `waterno1_18`: unsupported operator: signpower
- `waterno1_24`: unsupported operator: signpower
- `worst`: unsupported operator: erf

### Univariate additive terms (per row and variable)

| curvature on the variable's interval | terms | instances |
|---|---|---|
| concave | 42445 | 178 |
| convex | 978941 | 400 |
| fixed_var | 14153 | 104 |
| inferred_concave | 28752 | 64 |
| inferred_convex | 86151 | 189 |
| inferred_neither | 1104 | 2 |
| inferred_unknown | 1955 | 6 |
| neither | 1291 | 43 |
| unbounded_var | 885112 | 203 |
| unknown | 6985 | 37 |

| instances with | count |
|---|---|
| any secant variable, declared bounds | 470 |
| any secant variable, declared or inferred bounds | 687 |
| any strict secant variable | 339 |
| any separable secant variable | 247 |
| binary variables with a curved term (excluded) | 20 |

### Funnel

| row kind | variant of (i) | (i): rows / instances | (i)+(ii) | of which all bounds declared | applicable (i)+(ii)+(iii) | dropped at (iii) |
|---|---|---|---|---|---|---|
| equality | declared | 133731 / 96 | 133724 / 96 | 129491 / 88 | 122021 / 32 | degenerate 11499, unknown 204, infeasible-by-bounds 0 |
| equality | wide | 136605 / 189 | 136551 / 185 | 129491 / 88 | 122039 / 35 | degenerate 14297, unknown 215, infeasible-by-bounds 0 |
| equality | strict | 2602 / 79 | 2599 / 77 | 2452 / 68 | 214 / 17 | degenerate 2281, unknown 104, infeasible-by-bounds 0 |
| equality | separable | 2326 / 65 | 2324 / 63 | 2234 / 60 | 194 / 10 | degenerate 2034, unknown 96, infeasible-by-bounds 0 |
| inequality | declared | 11091 / 183 | 8038 / 175 | 4040 / 161 | 8027 / 172 | cannot be tight 11 |
| inequality | wide | 29287 / 256 | 26225 / 248 | 4040 / 161 | 26097 / 245 | cannot be tight 128 |
| inequality | strict | 1436 / 112 | 1426 / 111 | 1076 / 73 | 1382 / 109 | cannot be tight 44 |
| inequality | separable | 804 / 70 | 795 / 70 | 526 / 40 | 788 / 68 | cannot be tight 7 |

- variant `declared`: 202 instances have at least one applicable row of either kind.
- variant `wide`: 277 instances have at least one applicable row of either kind.
- variant `strict`: 124 instances have at least one applicable row of either kind.
- variant `separable`: 77 instances have at least one applicable row of either kind.

### Applicable rows, variant `declared`

| row size (nonzeros) | equality rows | inequality rows |
|---|---|---|
| 2 | 24 | 1691 |
| 3 | 32556 | 2236 |
| 4-5 | 65982 | 35 |
| 6-10 | 21090 | 4040 |
| 11-25 | 2347 | 1 |
| 26-100 | 22 | 1 |
| >=101 | 0 | 23 |

| secant items in row | equality rows | inequality rows |
|---|---|---|
| 2 | 64645 | 7899 |
| 3 | 30916 | 17 |
| 4-5 | 18288 | 26 |
| 6-10 | 7460 | 68 |
| 11-25 | 693 | 7 |
| >=26 | 19 | 10 |

- applicable equality rows with equal widths over all items (Theorem 2 applies exactly): 340 rows in 20 instances (acopf_case1354pegase_qcqp, acopf_case6468rte_qcqp, acopf_case6515rte_qcqp, acopf_case9241pegase_qcqp, acopf_caseactivsg25k_qcqp, acopf_caseactivsg70k_qcqp, arki0016, ex2_1_8, ex6_1_2, ex6_1_4, ex6_2_10, ex6_2_11, ex6_2_12, ex6_2_13, ex6_2_14, ex6_2_5, ex6_2_6, ex6_2_7, ex6_2_8, ex6_2_9).
- applicable equality rows whose secant items alone have equal widths: 2028.
- applicable rows with integer or binary items: 5316 of 130048.
- {'some items without a term': 66686, 'all items secant': 63362}.

### Applicable rows, variant `wide`

| row size (nonzeros) | equality rows | inequality rows |
|---|---|---|
| 2 | 24 | 2240 |
| 3 | 32558 | 19362 |
| 4-5 | 65983 | 78 |
| 6-10 | 21105 | 4103 |
| 11-25 | 2347 | 148 |
| 26-100 | 22 | 114 |
| >=101 | 0 | 52 |

| secant items in row | equality rows | inequality rows |
|---|---|---|
| 2 | 64649 | 25546 |
| 3 | 30916 | 45 |
| 4-5 | 18288 | 65 |
| 6-10 | 7474 | 127 |
| 11-25 | 693 | 148 |
| >=26 | 19 | 166 |

- applicable equality rows with equal widths over all items (Theorem 2 applies exactly): 340 rows in 20 instances (acopf_case1354pegase_qcqp, acopf_case6468rte_qcqp, acopf_case6515rte_qcqp, acopf_case9241pegase_qcqp, acopf_caseactivsg25k_qcqp, acopf_caseactivsg70k_qcqp, arki0016, ex2_1_8, ex6_1_2, ex6_1_4, ex6_2_10, ex6_2_11, ex6_2_12, ex6_2_13, ex6_2_14, ex6_2_5, ex6_2_6, ex6_2_7, ex6_2_8, ex6_2_9).
- applicable equality rows whose secant items alone have equal widths: 2029.
- applicable rows with integer or binary items: 22506 of 148136.
- {'some items without a term': 83797, 'all items secant': 64339}.

### Applicable rows, variant `strict`

| row size (nonzeros) | equality rows | inequality rows |
|---|---|---|
| 2 | 23 | 594 |
| 3 | 1 | 497 |
| 4-5 | 186 | 39 |
| 6-10 | 4 | 82 |
| 11-25 | 0 | 147 |
| 26-100 | 0 | 23 |
| >=101 | 0 | 0 |

| secant items in row | equality rows | inequality rows |
|---|---|---|
| 2 | 203 | 1063 |
| 3 | 1 | 31 |
| 4-5 | 6 | 36 |
| 6-10 | 4 | 92 |
| 11-25 | 0 | 137 |
| >=26 | 0 | 23 |

- applicable equality rows with equal widths over all items (Theorem 2 applies exactly): 23 rows in 7 instances (ex2_1_8, ex6_2_10, ex6_2_11, ex6_2_12, ex6_2_13, ex6_2_14, ex6_2_9).
- applicable equality rows whose secant items alone have equal widths: 23.
- applicable rows with integer or binary items: 468 of 1596.
- {'all items secant': 921, 'some items without a term': 675}.

### Applicable rows, variant `separable`

| row size (nonzeros) | equality rows | inequality rows |
|---|---|---|
| 2 | 4 | 47 |
| 3 | 0 | 491 |
| 4-5 | 186 | 35 |
| 6-10 | 4 | 56 |
| 11-25 | 0 | 136 |
| 26-100 | 0 | 23 |
| >=101 | 0 | 0 |

| secant items in row | equality rows | inequality rows |
|---|---|---|
| 2 | 184 | 512 |
| 3 | 0 | 29 |
| 4-5 | 6 | 32 |
| 6-10 | 4 | 66 |
| 11-25 | 0 | 126 |
| >=26 | 0 | 23 |

- applicable equality rows with equal widths over all items (Theorem 2 applies exactly): 10 rows in 1 instances (ex2_1_8).
- applicable equality rows whose secant items alone have equal widths: 10.
- applicable rows with integer or binary items: 464 of 982.
- {'all items secant': 311, 'some items without a term': 671}.

### Top 40 instances by applicable rows (variant `separable`)

| instance | applicable rows | equality | inequality | eq. with equal widths | vars | rows | type | convex | primal bound | dual bound |
|---|---|---|---|---|---|---|---|---|---|---|
| `kall_circlespolygons_c1p6a` | 72 | 72 | 0 | 0 | 1110 | 1134 | QCP | False | 3.743965334 | 0.0 |
| `kall_circlespolygons_c1p5b` | 60 | 60 | 0 | 0 | 791 | 816 | QCP | False | 3.769605964 | 0.0 |
| `gastrans135` | 52 | 0 | 52 | 0 | 1193 | 2472 | MINLP | False | 0.0 | 0.0 |
| `kall_circlespolygons_c1p5a` | 24 | 24 | 0 | 0 | 158 | 174 | QCP | False | 2.848720213 | 0.0 |
| `st_m2` | 21 | 0 | 21 | 0 | 30 | 21 | QP | False | -856648.8187 | -856648.8187 |
| `gastrans582_cold13` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cold13_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cold17` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cold17_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool12` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool12_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool14` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool14_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_freezing27` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False |  | inf |
| `gastrans582_freezing27_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False |  | inf |
| `gastrans582_freezing30` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_freezing30_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild10` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild10_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild11` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild11_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm15` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm15_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm31` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm31_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `st_fp8` | 20 | 0 | 20 | 0 | 24 | 20 | QP | False | 15639.0 | 15639.0 |
| `st_rv3` | 20 | 0 | 20 | 0 | 20 | 20 | QP | False | -35.76067064 | -35.76067064 |
| `st_rv7` | 20 | 0 | 20 | 0 | 30 | 20 | QP | False | -138.1874971 | -138.1874971 |
| `st_rv8` | 20 | 0 | 20 | 0 | 40 | 20 | QP | False | -132.661629 | -132.661629 |
| `st_rv9` | 20 | 0 | 20 | 0 | 50 | 20 | QP | False | -120.1531085 | -120.1531085 |
| `ex2_1_5` | 11 | 0 | 11 | 0 | 10 | 11 | QP | False | -268.0146315 | -268.0146316 |
| `super3t` | 11 | 2 | 9 | 0 | 1056 | 1343 | MBNLP | False | -0.6859653973 | -1.0 |
| `ex2_1_10` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | 49318.01796 | 49318.01796 |
| `ex2_1_7` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | -4150.410134 | -4150.410134 |
| `ex2_1_8` | 10 | 10 | 0 | 10 | 24 | 10 | QP | False | 15639.0 | 15639.0 |
| `st_fp7a` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | -354.7506124 | -354.7506125 |
| `st_fp7b` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | -634.7506124 | -634.7506126 |
| `st_fp7c` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | -8695.012248 | -8695.012249 |
| `st_fp7d` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | -114.7506124 | -114.7506125 |
| `st_fp7e` | 10 | 0 | 10 | 0 | 20 | 10 | QP | False | -3730.410134 | -3730.410134 |

### Instances with applicable rows by problem type and convexity (variant `separable`)

| type | convex | instances |
|---|---|---|
| MBNLP | False | 3 |
| MBQP | False | 1 |
| MINLP | False | 22 |
| NLP | False | 4 |
| QCP | False | 9 |
| QCQP | False | 1 |
| QP | False | 37 |

All 10 instances with applicable equality rows (rows in parentheses): `kall_circlespolygons_c1p6a` (72), `kall_circlespolygons_c1p5b` (60), `kall_circlespolygons_c1p5a` (24), `super3t` (2), `ex2_1_8` (10), `kall_circlespolygons_c1p11` (8), `kall_circlespolygons_c1p12` (8), `kall_circlespolygons_c1p13` (8), `ex14_1_6` (1), `st_robot` (1).

### Top 40 instances by applicable rows (variant `strict`)

| instance | applicable rows | equality | inequality | eq. with equal widths | vars | rows | type | convex | primal bound | dual bound |
|---|---|---|---|---|---|---|---|---|---|---|
| `ringpack_30_1` | 92 | 0 | 92 | 0 | 433 | 7898 | MBQCP | False | -56.40514551 | -62.57465297 |
| `ringpack_30_2` | 92 | 0 | 92 | 0 | 463 | 8768 | MBQCP | False | -59.40775612 | -62.57465297 |
| `kall_circlespolygons_c1p6a` | 72 | 72 | 0 | 0 | 1110 | 1134 | QCP | False | 3.743965334 | 0.0 |
| `kall_circlespolygons_c1p5b` | 60 | 60 | 0 | 0 | 791 | 816 | QCP | False | 3.769605964 | 0.0 |
| `gastrans135` | 52 | 0 | 52 | 0 | 1193 | 2472 | MINLP | False | 0.0 | 0.0 |
| `ringpack_20_1` | 35 | 0 | 35 | 0 | 215 | 2547 | MBQCP | False | -39.34126268 | -41.71643531 |
| `ringpack_20_2` | 35 | 0 | 35 | 0 | 235 | 2927 | MBQCP | False | -39.34126268 | -41.71643531 |
| `kall_circles_c8a` | 28 | 0 | 28 | 0 | 22 | 86 | QCP | False | 2.540919138 | 2.540912934 |
| `kall_circlespolygons_c1p5a` | 24 | 24 | 0 | 0 | 158 | 174 | QCP | False | 2.848720213 | 0.0 |
| `super3t` | 22 | 8 | 14 | 0 | 1056 | 1343 | MBNLP | False | -0.6859653973 | -1.0 |
| `kall_circles_c7a` | 21 | 0 | 21 | 0 | 20 | 69 | QCP | False | 2.662812179 | 2.662810981 |
| `kall_congruentcircles_c71` | 21 | 0 | 21 | 0 | 18 | 60 | QCP | False | 1.502212856 | 1.502211969 |
| `kall_congruentcircles_c72` | 21 | 0 | 21 | 0 | 18 | 60 | QCP | False | 1.966314471 | 1.96631268 |
| `st_m2` | 21 | 0 | 21 | 0 | 30 | 21 | QP | False | -856648.8187 | -856648.8187 |
| `gastrans582_cold13` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cold13_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cold17` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cold17_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool12` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool12_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool14` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_cool14_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_freezing27` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False |  | inf |
| `gastrans582_freezing27_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False |  | inf |
| `gastrans582_freezing30` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_freezing30_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild10` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild10_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild11` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_mild11_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm15` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm15_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm31` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `gastrans582_warm31_95` | 20 | 0 | 20 | 0 | 2186 | 3732 | MINLP | False | 0.0 | 0.0 |
| `st_fp8` | 20 | 0 | 20 | 0 | 24 | 20 | QP | False | 15639.0 | 15639.0 |
| `st_rv3` | 20 | 0 | 20 | 0 | 20 | 20 | QP | False | -35.76067064 | -35.76067064 |
| `st_rv7` | 20 | 0 | 20 | 0 | 30 | 20 | QP | False | -138.1874971 | -138.1874971 |
| `st_rv8` | 20 | 0 | 20 | 0 | 40 | 20 | QP | False | -132.661629 | -132.661629 |
| `st_rv9` | 20 | 0 | 20 | 0 | 50 | 20 | QP | False | -120.1531085 | -120.1531085 |
| `kall_circles_c6a` | 15 | 0 | 15 | 0 | 18 | 54 | QCP | False | 2.111715465 | 2.11171366 |

### Instances with applicable rows by problem type and convexity (variant `strict`)

| type | convex | instances |
|---|---|---|
| MBNLP | False | 3 |
| MBQCP | False | 6 |
| MBQP | False | 1 |
| MINLP | False | 22 |
| NLP | False | 9 |
| NLP | unknown | 1 |
| QCP | False | 37 |
| QCQP | False | 1 |
| QP | False | 44 |

All 17 instances with applicable equality rows (rows in parentheses): `kall_circlespolygons_c1p6a` (72), `kall_circlespolygons_c1p5b` (60), `kall_circlespolygons_c1p5a` (24), `super3t` (8), `ex2_1_8` (10), `chp_partload` (1), `kall_circlespolygons_c1p11` (8), `kall_circlespolygons_c1p12` (8), `kall_circlespolygons_c1p13` (8), `ex6_2_10` (3), `ex6_2_13` (3), `ex6_2_12` (2), `ex6_2_14` (2), `ex6_2_9` (2), `ex14_1_6` (1), `ex6_2_11` (1), `st_robot` (1).

### Top 40 instances by applicable rows (variant `declared`)

| instance | applicable rows | equality | inequality | eq. with equal widths | vars | rows | type | convex | primal bound | dual bound |
|---|---|---|---|---|---|---|---|---|---|---|
| `acopf_caseactivsg70k_qcqp` | 84841 | 84841 | 0 | 8 | 900023 | 1016476 | QCQP | False | 16439499.83 | 0.0 |
| `acopf_caseactivsg25k_qcqp` | 25579 | 25579 | 0 | 4 | 328043 | 365034 | QCQP | False | 6017830.612 | 3129447.108 |
| `acopf_case9241pegase_qcqp` | 5450 | 5450 | 0 | 64 | 145389 | 155089 | QCP | False | 315911.5561 | 84371.82 |
| `acopf_case6515rte_qcqp` | 2653 | 2653 | 0 | 96 | 89575 | 93059 | QCP | False | 109802.2206 | 20952.4 |
| `acopf_case6468rte_qcqp` | 2099 | 2099 | 0 | 60 | 88932 | 90966 | QCP | False | 86829.01902 | 21550.35 |
| `acopf_case1354pegase_qcqp` | 1109 | 1109 | 0 | 16 | 19236 | 21580 | QCP | False | 74069.35457 | 23037.69 |
| `unitcommit_200_0_5_mod_7` | 293 | 0 | 293 | 0 | 28142 | 77776 | MBQCP | False | 33727321.42 | 33674114.7 |
| `unitcommit_200_100_2_mod_7` | 249 | 0 | 249 | 0 | 35370 | 69569 | MBQCP | False | 32736736.16 | 32731550.87 |
| `p_ball_30b_10p_2d_m` | 189 | 0 | 189 | 0 | 410 | 529 | MBQCP | True | 41.93395425 | 19.51243222 |
| `slay10m` | 180 | 0 | 180 | 0 | 290 | 405 | MBQP | True | 129579.8838 | 129579.8838 |
| `fo9_ar25_1` | 162 | 0 | 162 | 0 | 180 | 435 | MINLP | True | 32.18643105 | 32.18642335 |
| `fo9_ar2_1` | 162 | 0 | 162 | 0 | 180 | 435 | MINLP | True | 32.625 | 32.62498658 |
| `fo9_ar3_1` | 162 | 0 | 162 | 0 | 180 | 435 | MINLP | True | 24.81547619 | 24.81547617 |
| `fo9_ar4_1` | 162 | 0 | 162 | 0 | 180 | 435 | MINLP | True | 23.46428571 | 23.46428571 |
| `fo9_ar5_1` | 162 | 0 | 162 | 0 | 180 | 435 | MINLP | True | 23.46428571 | 23.46428535 |
| `o9_ar4_1` | 162 | 0 | 162 | 0 | 180 | 435 | MINLP | True | 236.1384562 | 236.1238687 |
| `fo9` | 144 | 0 | 144 | 0 | 182 | 343 | MBNLP | True | 23.46428571 | 23.46428544 |
| `slay09m` | 144 | 0 | 144 | 0 | 234 | 324 | MBQP | True | 107805.7529 | 107805.7529 |
| `p_ball_10b_7p_3d_m` | 132 | 0 | 132 | 0 | 154 | 219 | MBQCP | True | 109.8032151 | 109.803207 |
| `fo8_ar25_1` | 128 | 0 | 128 | 0 | 144 | 347 | MINLP | True | 28.0451814 | 28.04518138 |
| `fo8_ar2_1` | 128 | 0 | 128 | 0 | 144 | 347 | MINLP | True | 30.34061042 | 30.34060987 |
| `fo8_ar3_1` | 128 | 0 | 128 | 0 | 144 | 347 | MINLP | True | 23.91005347 | 23.91005345 |
| `fo8_ar4_1` | 128 | 0 | 128 | 0 | 144 | 347 | MINLP | True | 22.38189652 | 22.38189649 |
| `fo8_ar5_1` | 128 | 0 | 128 | 0 | 144 | 347 | MINLP | True | 22.38189652 | 22.38189646 |
| `o8_ar4_1` | 128 | 0 | 128 | 0 | 144 | 347 | MINLP | True | 243.0707486 | 243.0706612 |
| `fo8` | 112 | 0 | 112 | 0 | 146 | 273 | MBNLP | True | 22.38189652 | 22.38189649 |
| `slay08m` | 112 | 0 | 112 | 0 | 184 | 252 | MBQP | True | 84960.21242 | 84960.21242 |
| `fo7_ar25_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 23.0935676 | 23.0935676 |
| `fo7_ar2_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 24.83984707 | 24.83984703 |
| `fo7_ar3_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 22.51747101 | 22.51747099 |
| `fo7_ar4_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 20.72982507 | 20.72982504 |
| `fo7_ar5_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 17.74932941 | 17.7493294 |
| `m7_ar25_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 143.585 | 143.585 |
| `m7_ar2_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 190.235 | 190.235 |
| `m7_ar3_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 143.585 | 143.585 |
| `m7_ar4_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 106.7568769 | 106.7568769 |
| `m7_ar5_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 106.4600058 | 106.4600058 |
| `no7_ar25_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 107.8153083 | 107.8153052 |
| `no7_ar2_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 107.8153083 | 107.8153071 |
| `no7_ar3_1` | 98 | 0 | 98 | 0 | 112 | 269 | MINLP | True | 107.8153083 | 107.8153081 |

### Instances with applicable rows by problem type and convexity (variant `declared`)

| type | convex | instances |
|---|---|---|
| IQCQP | True | 1 |
| IQP | True | 6 |
| MBNLP | False | 3 |
| MBNLP | True | 16 |
| MBQCP | False | 10 |
| MBQCP | True | 19 |
| MBQCQP | True | 2 |
| MBQP | False | 1 |
| MBQP | True | 8 |
| MINLP | False | 22 |
| MINLP | True | 32 |
| MINLP | unknown | 2 |
| MIQP | True | 4 |
| NLP | False | 19 |
| NLP | unknown | 1 |
| QCP | False | 41 |
| QCQP | False | 3 |
| QP | False | 12 |

### Open instances (variant `separable`, any applicable row)

| instance | applicable rows | of which equality | type | convex | primal bound | dual bound | gap |
|---|---|---|---|---|---|---|---|
| `btest14` | 1 | 0 | NLP | False | -59.81738781 | -61.3487556 | 2.50% |
| `chp_partload` | 8 | 0 | MBNLP | False | 23.29810754 | 20.54512031 | 11.82% |
| `ghg_3veh` | 1 | 0 | MBNLP | False | 7.75400605 | 6.391782164 | 17.57% |
| `kall_circlespolygons_c1p5a` | 24 | 24 | QCP | False | 2.848720213 | 0.0 | 100.00% |
| `kall_circlespolygons_c1p5b` | 60 | 60 | QCP | False | 3.769605964 | 0.0 | 100.00% |
| `kall_circlespolygons_c1p6a` | 72 | 72 | QCP | False | 3.743965334 | 0.0 | 100.00% |
| `super3t` | 11 | 2 | MBNLP | False | -0.6859653973 | -1.0 | 31.40% |

