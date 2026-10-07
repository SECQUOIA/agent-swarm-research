# Row hulls: how often does the structure occur in MINLPLib?

Date: 2026-09-21. Companion to
[Row hulls](../results/row-hull-separable-concave.md). Code, raw output and the
full set of tables are in `code/row_hull/minlplib_scan/` (`scan.py`,
`summarize.py`, `scan.jsonl`, `summary.md`, `scan.log`).

## Result

The scan covers the 1,632 OSiL files of the local MINLPLib copy; 1,601 were
analysed and 31 were skipped because of operators the repository's OSiL parser
does not support (list below). No file hit the 300 s timeout.

A linear row is *applicable* when (i) at least two of its variables are secant
items, (ii) all its variables have finite bounds, and (iii) it is an equality
row that is nondegenerate, or an inequality row that can be tight. The answer
depends strongly on how strictly "secant item" is read:

| variant of (i) | meaning | instances with an applicable row | with an applicable equality row | equality rows | inequality rows |
|---|---|---|---|---|---|
| `declared` | variable has a certified convex or concave additive term on its declared bounds | 202 | 32 | 122,021 | 8,027 |
| `wide` | same, bounds may come from one round of inference | 277 | 35 | 122,039 | 26,097 |
| `strict` | `wide`, and the model bounds the term on its secant side | 124 | 17 | 214 | 1,382 |
| `separable` | `strict`, and in the row that carries the term the variable is in no multivariate term | 77 | 10 | 194 | 788 |

The `separable` variant is the one that matches the note's setting, so the
headline is: **77 of 1,601 instances (4.8%) have at least one structurally
applicable row; 10 have an applicable equality row; Theorem 2 (equal widths)
applies exactly to 10 rows, all in `ex2_1_8`.** The large `declared` counts are
almost entirely convex squares in the ACOPF instances (99.8% of the equality
rows) and convex terms in convex MINLPs (`fo*`, `slay*`, `p_ball*`, ...), where
the model only needs the tangent side and joint convexification along a row
gains nothing.

In the `separable` variant all 77 instances are nonconvex: 37 QP (mostly the
small concave `st_*` and `ex2_1_*` problems), 22 MINLP (all `gastrans*`), 9 QCP,
4 NLP, 3 MBNLP, 1 MBQP, 1 QCQP. Rows are small: 184 of the 194 equality rows
have exactly two secant items; inequality rows have up to 50 (`st_rv9`). Seven of the 77
instances are open in MINLPLib (gap above 0.01%); see the last table.

## What the counts mean

They are a structural upper bound on applicability, not a measurement of
benefit. A counted row satisfies the hypotheses under which the row hull is
strictly smaller than the term-wise relaxation *of that row alone*. Nothing is
said about whether the gap matters for the instance's bound, whether other
constraints already close it, or whether a solver's presolve changes the row.
No cut was generated and no solver was run. Conversely, rows that become
applicable only after reformulation (aggregated rows, presolved bounds,
substituted variables) are not counted.

## Method and simplifications

1. **Parser.** `uenv.osil.read_osil` (imported, unchanged). Instances with
   operators it does not know (`tanh`, `erf`, `signpower`, `log10`, `min`,
   `gammaFn`) are skipped. The `signpower` instances are water and gas networks;
   `signpower` is neither convex nor concave on an interval around zero.
2. **Additive univariate terms.** The top-level sum of each nonlinear
   expression is flattened (through `sum`, `minus`, `negate`, products with
   constants, division by constants). A summand in one variable with at least
   one nonlinear operator is a term; terms of the same variable in the same row
   are added up into one function, together with pure squares `c*x_k^2` from
   `<quadraticCoefficients>`. Univariate expressions nested inside other
   functions are not terms. A square `x_k^2` that stands next to a bilinear
   term in `x_k` (expanded `(x_i - x_j)^2`) is counted as a term in all variants
   except `separable`.
3. **Curvature.** Certified on the variable's interval: closed-form rules for
   `x^2`, `x^p`, `exp`, `log`, `sqrt` of a bare variable; otherwise
   `uenv.curvature.certify_pieces` (ball arithmetic), preceded by a certified
   refutation (second derivative strictly negative at one sample point and
   strictly positive at another gives "neither"). An undecided sliver at an end
   point where the function is finite (`x^0.6` at 0) is accepted by continuity.
   A 5 s limit per expression and any failure give "unknown". The label is the
   curvature of the signed term as it appears in the row. Bounds of magnitude
   `>= 1e20` are infinite. Large finite "big-M" bounds count as finite.
4. **Secant items.** A variable is a secant item if at least one of its terms,
   anywhere in the instance (objective included), is convex or concave.
   `strict` additionally requires the secant side to be needed where the term
   stands: a concave term in a `<=` row or a minimized objective, a convex term
   in a `>=` row or a maximized objective, either in an equality or ranged row.
   Binary variables (and integers within `[0,1]`) are never secant items,
   because their chord is exact at the integer points; 20 instances have such
   terms. General integer variables are kept.
5. **Rows.** Only rows with no nonlinear part and no quadratic entries are
   tested. Rows whose expression tree contains only linear terms are not tested
   (counted per instance as `n_rows_linear_in_nl_tree`). The objective is not a
   row. Ranged rows count as inequality rows.
6. **Condition (ii).** Declared bounds, or, for a variable with an infinite
   declared bound, the bound implied by one round of row-activity inference
   over the linear rows using declared bounds only. Inference never tightens a
   finite declared bound and ignores integrality. A variable bounded only by
   the tested row itself acts as a slack; such equality rows come out as
   degenerate, which is the correct answer.
7. **Condition (iii), equality rows.** Widths `w_i = |a_i|(u_i - l_i)`, fixed
   variables dropped, `B` as in the note. Degenerate means some subset of widths
   sums to `B` within `1e-9 * max(1, sum w, |B|)`. Exact test by
   meet-in-the-middle for at most 25 items; closed form for equal widths (`B/w`
   integer) at any size; exact bitset dynamic program for integer data with
   `n * sum w <= 4e9`; otherwise "unknown" (not counted as applicable).
8. **Condition (iii), inequality rows.** No subset-sum test. The row must be
   able to be tight without fixing every variable: `0 < B < sum w` for a finite
   side. This is weaker than nondegeneracy.
9. **Equal widths.** Reported over all items of the row with positive width,
   which is what Theorem 2 needs. Equal widths over the secant items alone are
   reported separately in `summary.md`.
10. **Output.** `scan.jsonl` has one line per instance. Identical row records
    are stored once with `count` and `first_row`. Terms are counted in full in
    `term_counts` and `term_shapes`; only the first 200 are listed individually
    (`terms_first`).

## Commands

Run from `code/row_hull/minlplib_scan/`. One worker process, one thread; the
parent process only waits and enforces the per-file timeout. The scan took
about 15 minutes; the `arki*` instances account for almost half of the analysis time.

```
nice -n 19 uv run --project /workspace/minlp-notes/code/minlp_solver_lab \
    python scan.py ~/.cache/minlplib/minlplib/osil scan.jsonl --timeout 300 > scan.log 2>&1
nice uv run --project /workspace/minlp-notes/code/minlp_solver_lab \
    python summarize.py scan.jsonl ../../minlp_solver_lab/instances/instancedata.csv > summary.md
```

Checks run: the scanner on hand-picked instances (`ex2_1_8`, `squfl010-025`,
`alan`, `fo7`, `hydro`, `waterx`, ...) with the records inspected by eye, and
ad hoc calls of the subset-sum, curvature and flattening helpers. There is no
test file. No project-wide verification was run.

## Tables

### Files and skipped instances


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

### Univariate additive terms (one per row and variable)

Prefix `inferred_`: the interval came from bound inference. `unbounded_var` and `fixed_var` terms were not classified.


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

Entries are rows / instances.


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

### Top 40 instances by applicable rows, variant `separable`


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

### Problem types, variant `separable`


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

### Open instances, variant `separable`

Relative gap between the MINLPLib primal and dual bounds above 0.01%. Instances without a primal bound are omitted.


| instance | applicable rows | of which equality | type | convex | primal bound | dual bound | gap |
|---|---|---|---|---|---|---|---|
| `btest14` | 1 | 0 | NLP | False | -59.81738781 | -61.3487556 | 2.50% |
| `chp_partload` | 8 | 0 | MBNLP | False | 23.29810754 | 20.54512031 | 11.82% |
| `ghg_3veh` | 1 | 0 | MBNLP | False | 7.75400605 | 6.391782164 | 17.57% |
| `kall_circlespolygons_c1p5a` | 24 | 24 | QCP | False | 2.848720213 | 0.0 | 100.00% |
| `kall_circlespolygons_c1p5b` | 60 | 60 | QCP | False | 3.769605964 | 0.0 | 100.00% |
| `kall_circlespolygons_c1p6a` | 72 | 72 | QCP | False | 3.743965334 | 0.0 | 100.00% |
| `super3t` | 11 | 2 | MBNLP | False | -0.6859653973 | -1.0 | 31.40% |

The same tables for the variants `strict`, `declared` and `wide` (distributions, top 40, problem types) are in `code/row_hull/minlplib_scan/summary.md`.
