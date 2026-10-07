# Second-wave certification targets among open MINLPLib instances

Date: 2026-09-29/30. Status: scouting report, not reviewed. It contains no
certified bounds except the hvycrash identity in Section 3.1, which has
been checked by script but not independently reviewed.

## 1. Summary

**Selection.** From the treewidth census (`../treewidth-census/census_merged.json`)
I selected every instance that meets all of these conditions:

- it is nonconvex;
- its factor-incidence width is at most 16, or its nonlinear-primal width is
  at most 6 and it has at least 50 nonlinear variables;
- its metadata gap is above 1e-4 or infinite;
- it is not one of the 11 instances closed in the first wave.

That gives 283 instances. I fetched all 283 MINLPLib instance pages and
parsed every listed feasible point and every single-solver dual bound.

**Most metadata-open instances are already closed on the instance pages.**
137 of the 283 have a best listed single-solver gap of at most 1e-4. This
includes several families named in the task:

- rocket50–400 (LINDO; COUENNE agrees on rocket100 and rocket400);
- kriging_peaks-full500 (GUROBI);
- gasnet (SCIP);
- kport40 (XPRESS);
- csched2 and csched2a (BARON);
- all waternd_* instances except fosspoly1 and blacksburg (SCIP);
- powerflow0009p, 0014p, 0014r and 0030r.

Of the 146 instances that remain:

- 25 have no listed feasible point;
- 3 have no listed dual bound;
- 4 have absolute gaps below 1e-5 (tolerance level).

**Findings from the scouting itself (Section 3).**

1. **hvycrash is closed by an identity.** At every exactly feasible point the
   objective equals −0.2185. The best listed dual bound is −2.185e8 (SCIP).
   `hvycrash_check.py` asserts the pattern in all 50 stages. MINLPLib point p3
   evaluates to −0.2185 with a maximum violation of 1.0e-12.
2. **quantum is unbounded below if Γ is taken literally.** The objective
   tends to −∞ as x3 → 1/4 from below, where Γ(2 − 1/(2·x3)) has a pole. If Γ
   is restricted to positive arguments, it is a 2-D box problem.
3. **A listed LINDO bound is invalid.** LINDO's bound for methanol50
   (0.00802826) lies above the listed point p4. I evaluated p4 in 50-digit
   arithmetic: objective 0.00793022, maximum violation 8.4e-12. The bound
   equals the objective of point p3, which suggests that a local solution was
   reported as a dual bound. Several instances are closed only by LINDO,
   including rocket200, methanol200/400, pinene100/200 and popdynm25.
4. **The OSIL reader ignores the objective constant.** `osil.py` does not
   read `<obj constant=...>`. 36 of the 283 candidates have a nonzero
   constant, including catmix (−1), methanol, pinene, popdynm and
   powerflow0039p/r. The first-wave instances have none. Any second-wave
   script must add the constant.

**Top 8 targets** (details in Sections 6 and 7). Gap is the best listed
relative gap in MINLPLib's convention `|p−d|/min(|p|,|d|)`.

| rank | target | instances | best listed gap | main tool |
|---|---|---|---|---|
| 1 | ex6_2_7, ex6_2_5 (Gibbs energy, Floudas handbook) | 2 | 5.64, 0.575 | Lagrangian over the mass balances; tangent-plane test by 2-D interval B&B |
| 2 | KAN family (kan_r3_h1_n4/n5/n9, kan_r5_h1_n3/n5/n8) | 6 | 0.018 – 6.1, one infinite | reduced-space interval B&B over 3 or 5 inputs |
| 3 | chain50–400 (COPS) | 4 | 28 – 60 | bound propagation, one multiplier for the length row, value-function certificate on a 2-D state |
| 4 | waterno2_06–24 | 5 | 0.71 – 5.8 | Lagrangian decomposition into single-period MINLPs (3 tank levels + 1 horizon row) |
| 5 | catmix100–800 (COPS) | 4 | 0.38 – 30 (LINDO bound only) | homogeneous DP for a positive bilinear system |
| 6 | pindyck | 1 | 0.23 | bound propagation, then partial Lagrangian over 16 periods |
| 7 | etamac | 1 | 0.0073 | hidden convexity: relax CES equalities to ≤ |
| 8 | pricing050 | 1 | 0.18 | separable problem with 5 coupling rows: Lagrangian dual, then B&B |

Next in line: powerflow0030p/0039p/0039r, the eg_* family, water,
ann_cumene_tanh and methanol50/100 (Section 8).

## 2. What I did

1. **Selection** (`fetch_pages.py`, output `candidates.json`): the rule in
   Section 1. Metadata gaps are taken from the census (MINLPLib
   `instancedata.csv`).
2. **Fetching**: `https://www.minlplib.org/<name>.html` for all 283 instances.
   Requests were sequential with a 1.5 s pause, fetched on 2026-09-29. Only
   the metadata part of each page was kept (cut before the embedded GAMS
   listing), in `pages/`.
3. **Parsing** (`parse_pages.py`, outputs `fetched.json` and `fetched.csv`).
   For each instance I recorded:
   - all feasible points listed with infeasibility ≤ 1e-8, and the best one;
   - the best "other point" (infeasibility > 1e-8);
   - every single-solver dual bound with its date;
   - the best dual bound, in the direction of the objective sense;
   - problem type, variable counts, source, application and references.

   `gap_best` uses MINLPLib's convention: `|p−d|/min(|p|,|d|)`, or inf if
   the signs differ or one value is 0. I checked this convention against the
   metadata values for 4stufen and rocket400. `abs_gap_best` is `|p−d|`.
   `inconsistent` marks a dual bound on the wrong side of the primal value
   (methanol50, and ghg_3veh by 3e-4 absolute). `keep` means
   `gap_best > 1e-4`.
4. **Structure** (`structure.py`, output `structure.jsonl`) for 35
   candidates. It records:
   - variable types;
   - unbounded continuous variables, overall and among nonlinear variables;
   - nonlinear operators;
   - equality and inequality row counts;
   - atom and row signatures (from `osil.analyze`);
   - dense rows and hub variables;
   - factor-incidence width upper bounds, before and after removing hub
     variables or the 3 densest rows;
   - the components of the nonlinear primal graph without hubs.

   Recomputed widths match the census values. For about 20 instances I also
   read the rows directly (Sections 5 and 7 list what was checked).
5. **Spot checks**:
   - `hvycrash_check.py`;
   - `check_points.py`, which evaluates MINLPLib points in 50-digit
     arithmetic. I downloaded three points (`sol/`): methanol50.p4,
     hvycrash.p1 and hvycrash.p3;
   - a numerical homogeneity test for ex6_2_5/7;
   - a period-decomposition test for waterno2;
   - evaluations of the quantum objective.

No project-wide checks were run. The commands actually run are listed in
Section 10.

## 3. Results found while scouting

### 3.1 hvycrash: the objective is constant on the feasible set

hvycrash (CUTE; spacecraft landing) has 201 variables and 150 equality rows
in 50 stages. The objective is `x152`. For stage k with angle `th`,
control `c` and free variable `r`, the model contains:

- an accumulator row, `x201 = A_1` and `x_j = x_{j+1} + A_k` down to `x152`,
  where `A_k = 0.00437 cos(th) / (D r^2)` and `D = 0.486237 c^2 + 0.0162079 > 0`;
- an algebraic row, `−1/r − cos(th)/(D r^3) = 0`.

The algebraic row requires `r ≠ 0`. Multiplying it by `−r` gives
`cos(th)/(D r^2) = −1`, so `A_k = −0.00437` exactly. Hence
`x152 = −50 × 0.00437 = −0.2185` at every exactly feasible point.
`hvycrash_check.py` asserts this row pattern for all 50 stages and checks
that the accumulator chain runs from x201 to x152.

- MINLPLib point p3 evaluates to −0.218499999999997 with a maximum violation
  of 1.0e-12.
- Point p1 evaluates to −0.21413 (maximum violation 4.1e-8); the page lists
  p2 at the same value with infeasibility 6e-10, but I did not evaluate p2.
  This value is −0.2185 + 0.00437: one stage has a huge `r` and an
  accumulator term near 0. Such points are only feasible within tolerance.
- Within a 1e-8 tolerance per row, values below −0.2185 are possible only by
  about 5e-7. The 50 accumulator rows contribute up to 50 × 1e-8. The
  algebraic rows add at most about 2e-8, because the identity becomes
  `cos(th)/(D r^2) = −1 − r·e` for row residual e, and `r·e > 0` needs
  `|r| < 1/√0.0162079 ≈ 7.9`.

Status: dual bound −0.2185 for exactly feasible points, which equals the
listed primal value. The only open question is exact feasibility (p3 is
feasible to 1e-12). This needs an independent review before it is reported.

### 3.2 quantum: unbounded below under the literal Γ definition

quantum (GAMS model library) has 2 variables, `a = x2 ∈ [1e-4, 10]` and
`n = x3 ∈ [1e-3, 10]`, and no constraints. The first objective term is
`0.5 n^2 Γ(2 − 1/(2n)) / Γ(1/(2n)) · a^(1/n)`. As `n → 1/4` from below,
`Γ(2 − 1/(2n)) → −∞` while the other terms stay finite. mpmath evaluations
with a = 2:

| n | objective |
|---|---|
| 0.2499999 | −6.2e5 |
| 0.24999999999 | −6.2e9 |
| 0.249999999999999 | −6.2e13 |

So the infimum is −∞ if Γ is evaluated at negative non-integer arguments,
and no finite dual bound exists. If the modeling system restricts Γ to
positive arguments, which I did not check, the domain is `n > 1/4`. There
the objective tends to +∞ at the boundary, and a 2-D interval branch and
bound should certify the listed value 0.80490293. That would need a Γ
enclosure; mpmath's `iv` has none, but Γ is monotone on each side of
1.4616. Either way this is a short item with low payoff.

### 3.3 methanol50: a listed LINDO dual bound is invalid

The methanol50 page lists these values:

- feasible point p4: 0.00793022 (page infeasibility 7e-13);
- feasible point p3: 0.00802826;
- LINDO dual bound: 0.00802826 (dated 15 Feb 2022).

With the OSIL objective constant 5.01625659 added, `check_points.py` gives
0.0079302188 for p4, with maximum violation 8.4e-12. The LINDO "bound" is
therefore 1.2% above a feasible value; it is LINDO's own local solution.

This matters for trust in single-solver closures. The instances below are
closed only by LINDO, with the next-best bound far away:

- rocket200 (SCIP 4.4%);
- methanol200 and methanol400 (other solvers give 0);
- pinene100 (GUROBI 0.042 against 19.87; pinene50 is also closed by COUENNE);
- popdynm25 (other solvers give 0);
- deb7–9;
- uselinear;
- ann_compressor_tanh, ann_fermentation_tanh and ann_peaks_tanh.

`fetched.json` has the full bound lists. Independent certificates for the
COPS members (rocket, methanol, pinene, popdynm) would have value, even
though they are not open by the listed-bound criterion.

## 4. What is still open (146 instances with best listed gap > 1e-4)

The full data is in `fetched.csv`.

- **No listed feasible point (25):** chp_shorttermplan2c, gabriel05–07,
  mpbp_03…48 (20 instances), nuclear10a. These are not dual-bound targets
  without a primal.
- **No finite dual bound listed (3):** ann_cumene_tanh, cesam2cent, quantum.
- **Infinite relative gap: primal and dual of different sign, or dual 0 (15):**
  arki0002, deb6, eg_disc2_s, junkturn, kall_circlespolygons_c1p5b/c1p6a,
  kan_r5_h1_n8, methanol100, parabol_p, popdynm50/100/200, transswitch0030p,
  var_con10, wastepaper6.
- **Gap ≥ 1 (33):** arki0017, catmix400/800, chain50/100/200/400, deb10,
  ex6_2_7, ex8_3_5, ex8_3_7, ex8_5_1, glider200/400, hvycrash, kan_r3_h1_n4,
  kan_r5_h1_n3, nuclear10b/14a/25a/49a, saa_2, sfacloc1_4_80/90/95,
  transswitch0014r/0030r, var_con5, waternd_fosspoly1, waterno2_09/12/18/24.
- **0.1 ≤ gap < 1 (30):** catmix100/200, eg_disc_s, ex6_2_5, ex8_3_2/3/4/8/9,
  feedtray, gabriel09, heatexch_gen1/3, kall_circlespolygons_c1p5a,
  kall_circlesrectangles_c6r39, kan_r3_h1_n5/n9, ndcc14persp, ndcc16persp,
  pindyck, pricing050, qapw, sfacloc1_3_80/90/95, super3t,
  topopt-cantilever/mbb_60x40_50, waterno2_06, waterund32.
- **0.01 ≤ gap < 0.1 (19):** arki0015, blendgap, eg_int_s, ghg_2veh,
  heatexch_gen2, hydroenergy3, kall_circlesrectangles_c6r29, kan_r5_h1_n5,
  methanol50 (invalid LINDO bound; with the valid bound 0 the gap is
  infinite), nuclear14b/25b/49b, tln12, topopt-zhou-rozvany_75,
  transswitch0014p, water, waterful2, waterund28/36.
- **1e-4 < gap < 0.01 (21):** bayes2_20/30, chp_shorttermplan1b/2d, cont6-qq,
  crudeoil_li03/21, etamac, ex6_2_13, ex8_4_7, gasprod_sarawak16/81,
  kall_circlesrectangles_c6r1, pooling_digabel19, powerflow0030p/0039p/0039r,
  wastepaper5, waternd_blacksburg, waterund25/27.

Caveats on these bands:

- ex8_5_1, bayes2_20/30 and wastepaper5 have absolute gaps below 2e-6. Their
  large relative gaps come from values near 0.
- ex6_2_13 is at 1.0e-4, on the threshold.

## 5. Structure of the inspected candidates

The table was generated from `fetched.json`. Widths are factor-incidence /
nonlinear-primal upper bounds from the census. Gaps use MINLPLib's
convention; "inf" means the relative gap is undefined or infinite.

| instance | type | vars (bin/int) | nl vars | width fac/nl | best primal | best dual (solver) | gap (best listed) | gap (metadata) |
|---|---|---|---|---|---|---|---|---|
| chain50 | NLP | 102 (0/0) | 102 | 4/101 | 5.072 | 0.1745 (ANTIGONE) | 28.06 | inf |
| chain100 | NLP | 202 (0/0) | 202 | 4/201 | 5.07 | 0.09367 (ANTIGONE) | 53.12 | inf |
| chain200 | NLP | 402 (0/0) | 402 | 4/401 | 5.069 | 0.08257 (ANTIGONE) | 60.39 | inf |
| chain400 | NLP | 802 (0/0) | 802 | 4/801 | 5.069 | 0.09564 (ANTIGONE) | 52 | inf |
| catmix100 | QCP | 303 (0/0) | 303 | 4/1 | -0.04807 | -0.06656 (LINDO) | 0.3846 | inf |
| catmix200 | QCP | 603 (0/0) | 603 | 4/1 | -0.04806 | -0.07255 (LINDO) | 0.5095 | inf |
| catmix400 | QCP | 1203 (0/0) | 1203 | 4/1 | -0.04806 | -0.6581 (LINDO) | 12.69 | inf |
| catmix800 | QCP | 2403 (0/0) | 2403 | 4/1 | -0.04806 | -1.489 (LINDO) | 29.98 | inf |
| waterno2_06 | MBNLP | 996 (54/0) | 252 | 9/2 | 282.9 | 165.2 (SCIP) | 0.7125 | 1.61 |
| waterno2_09 | MBNLP | 1494 (81/0) | 378 | 9/2 | 922.6 | 273.9 (SCIP) | 2.368 | 5.874 |
| waterno2_12 | MBNLP | 1992 (108/0) | 504 | 9/2 | 2263 | 479.5 (GUROBI) | 3.72 | 7.067 |
| waterno2_18 | MBNLP | 2988 (162/0) | 756 | 9/2 | 5270 | 770.7 (SCIP) | 5.837 | 12.74 |
| waterno2_24 | MBNLP | 3984 (216/0) | 1008 | 9/2 | 7333 | 1095 (SCIP) | 5.696 | 14.44 |
| kan_r3_h1_n4 | MBNLP | 1129 (288/0) | 832 | 11/1 | 0.002781 | 0.0003908 (GUROBI) | 6.117 | inf |
| kan_r3_h1_n5 | MBNLP | 1410 (360/0) | 1040 | 11/1 | -0.01104 | -0.01303 (GUROBI) | 0.1798 | 2457 |
| kan_r3_h1_n9 | MBNLP | 2534 (648/0) | 1872 | 11/1 | 0.01296 | 0.008143 (GUROBI) | 0.5921 | inf |
| kan_r5_h1_n3 | MBNLP | 838 (216/0) | 612 | 11/1 | -262.3 | -789.7 (GUROBI) | 2.011 | 19.91 |
| kan_r5_h1_n5 | MBNLP | 1392 (360/0) | 1020 | 11/1 | 0.2727 | 0.2679 (GUROBI) | 0.01784 | inf |
| kan_r5_h1_n8 | MBNLP | 2223 (576/0) | 1632 | 11/1 | 0.3606 | -45 (GUROBI) | inf | inf |
| hvycrash | NLP | 201 (0/0) | 150 | 4/2 | -0.2185 | -2.185e+08 (SCIP) | 1e+09 | inf |
| ex6_2_5 | NLP | 9 (0/0) | 9 | 6/2 | -70.75 | -111.4 (BARON) | 0.5748 | 4.146 |
| ex6_2_7 | NLP | 9 (0/0) | 9 | 6/2 | -0.1608 | -1.067 (BARON) | 5.635 | 7.422 |
| etamac | NLP | 97 (0/0) | 35 | 9/2 | -15.29 | -15.41 (SCIP) | 0.007257 | 0.0722 |
| pindyck | NLP | 116 (0/0) | 64 | 9/2 | -1170 | -1438 (SCIP) | 0.2285 | 0.6146 |
| pricing050 (max) | NLP | 50 (0/0) | 50 | 6/0 | -1814 | -1534 (SCIP) | 0.1822 | 0.5731 |
| eg_disc_s | MINLP | 8 (0/4) | 7 | 8/6 | 5.761 | 3.366 (SCIP) | 0.7114 | inf |
| eg_disc2_s | MINLP | 8 (0/3) | 7 | 8/6 | 5.642 | 0 (SHOT) | inf | inf |
| eg_int_s | MINLP | 8 (0/3) | 7 | 8/6 | 6.453 | 6.326 (SCIP) | 0.02004 | inf |
| quantum | NLP | 2 (0/0) | 2 | 3/1 | 0.8049 | - | inf | inf |
| powerflow0030p | NLP | 236 (0/0) | 230 | 16/7 | 576.9 | 572.8 (GUROBI) | 0.007077 | inf |
| powerflow0039p | NLP | 282 (0/0) | 272 | 16/7 | 4.187e+04 | 4.182e+04 (GUROBI) | 0.001214 | 388.7 |
| powerflow0039r | QCQP | 282 (0/0) | 272 | 16/7 | 4.187e+04 | 4.18e+04 (GUROBI) | 0.001535 | 0.01462 |
| water | NLP | 41 (0/0) | 32 | 8/13 | 904.9 | 826.5 (SCIP) | 0.09485 | 0.3499 |
| waterful2 | MBNLP | 629 (56/0) | 116 | 24/1 | 933.1 | 850.9 (GUROBI) | 0.09666 | 0.9988 |
| feedtray | MBNLP | 97 (7/0) | 80 | 15/2 | -13.41 | -21.31 (GUROBI) | 0.5897 | 3.891 |
| heatexch_gen1 | MBNLP | 112 (12/0) | 80 | 13/1 | 1.549e+05 | 1.08e+05 (LINDO) | 0.4345 | 0.5405 |
| heatexch_gen2 | MBNLP | 148 (16/0) | 126 | 10/1 | 6.358e+05 | 6.274e+05 (LINDO) | 0.0135 | 0.08879 |
| ann_cumene_tanh | NLP | 794 (0/0) | 277 | 15/1 | -3380 | - | inf | inf |
| methanol50 | NLP | 1505 (0/0) | 488 | 27/6 | 0.00793 | 0.008028 (LINDO, invalid) | (inconsistent) | inf |
| methanol100 | NLP | 3005 (0/0) | 800 | 25/6 | 0.007828 | 0 (BARON) | inf | inf |
| popdynm50 | QCQP | 2815 (0/0) | 1159 | 81/2 | 1.975e+04 | 0 (BARON) | inf | inf |
| glider200 | NLP | 2615 (0/0) | 2212 | 14/4 | -2.421e+06 | -3.358e+11 (COUENNE) | 1.387e+05 | inf |
| glider400 | NLP | 5215 (0/0) | 4412 | 14/4 | -1248 | -1e+07 (LINDO) | 8012 | inf |
| junkturn | QCQP | 200008 (0/0) | 199999 | 11/3 | 0.0001011 | 0 (BARON) | inf | inf |
| cesam2cent | NLP | 316 (0/0) | 207 | 11/1 | 0.508 | - | inf | inf |
| waternd_fosspoly1 | MBNLP | 1429 (1276/0) | 153 | 22/6 | 3.229e+05 | 2.658e+04 (SCIP) | 11.15 | 11.62 |
| saa_2 | MBNLP | 4407 (400/0) | 3606 | 12/4 | 12.16 | 6.023 (GUROBI) | 1.019 | 5.094 |
| sfacloc1_4_95 | MBNLP | 295 (9/0) | 128 | 16/2 | 11.18 | 2.103 (GUROBI) | 4.318 | 7.364 |

Structure notes, family by family. "Checked" means I read or asserted the
rows. Other items come from `structure.jsonl` and page metadata.

- **chain (COPS hanging chain).** Checked.
  - Variables: heights x_0..x_N (free; x_0 = 1, x_N = 3 fixed) and slopes
    u_0..u_N (free).
  - Rows: N linear trapezoid rows `x_{i+1} − x_i = (h/2)(u_i + u_{i+1})`,
    and one dense nonlinear length equality
    `(h/2) Σ (s_i + s_{i+1}) = 4` with `s_i = √(1+u_i²)`.
  - Objective: `(h/2) Σ (x_i s_i + x_{i+1} s_{i+1})`.
  - Nonconvexity: the state-times-control product `x·√(1+u²)` and the
    reverse-convex length equality.
  - Width: 4; 2 without the length row. The nonlinear-primal width of N−1
    comes only from the length row.
  - All 2N variables are unbounded. The best listed bound (ANTIGONE,
    0.09–0.17) is essentially trivial.
- **catmix (COPS catalyst mixing).** Checked.
  - Variables: control u_i ∈ [0,1] and states (x1_i, x2_i), all free.
  - Rows: 2N bilinear trapezoid equalities (u·x products; h/2 = 0.005 for
    N = 100).
  - Objective: `x1_N + x2_N − 1`, with the −1 held in the OSIL objective
    constant.
  - State dimension 2; separator (x1, x2, u); width 4.
  - LINDO is the only solver with a bound, and it degrades with N (−0.067 at
    N = 100, −1.49 at N = 800, against −0.048).
- **waterno2 (water network operation; Gleixner, Held, Huang, Vigerske).** Checked.
  - T identical period blocks of 166 variables and 9 binaries (pumps and
    valves; identical pumps are ordered by rows `b_k ≥ b_{k+T}`).
  - Blocks are linked only by 3 tank-level copy rows per period transition
    (tank areas 1800, 720 and 1600 m²; level balances with 3600 s per
    period).
  - One horizon-wide row sums one variable in [0, 5] from each period and
    bounds the sum below; it is probably a minimum delivered or pumped
    volume. Removing these 3(T−1)+1 rows leaves exactly T components of 166
    variables.
  - Nonlinearities: quadratic and cubic pump curves, pressure-loss squares,
    and B·C switching products. None of the nonlinear variables is
    unbounded.
  - Width 9 at every T.
- **KAN (Kolmogorov–Arnold networks; Karia, Lastrucci, Schweidtmann 2025).** Checked.
  - Inputs: 3 or 5, bounded to about [−1.75, 1.75]; one hidden layer of n
    neurons.
  - Each edge function is SiLU `x/(1+e^{−x})` plus a spline encoded with
    binaries (interval selection) and B·C products.
  - The objective is an affine function of the network output.
  - All inequality rows without binaries are box bounds on inputs and
    pre-activations, so there are no other constraints.
  - Reduced dimension: 3 or 5.
- **hvycrash.** Section 3.1.
- **ex6_2_5, ex6_2_7 (Gibbs free-energy minimization).** Checked.
  - Variables: 9 (3 phases × 3 components), each in [1e-7, component total].
  - Constraints: 3 linear mass balances.
  - No objective term mixes phases (61 and 78 terms checked).
  - Each phase function is positively homogeneous of degree 1: second
    differences along rays are about 1e-15, at the level of coefficient
    rounding.
  - ex6_2_7: all three phase functions are identical (UNIQUAC-type).
    ex6_2_5: two identical liquid phases and one ideal phase (3 terms).
- **etamac (ETA-MACRO, Manne).** Checked.
  - 9 periods; objective `−Σ β_t ln C_t`.
  - New-vintage output is `YN_t = CES(K, E, N)` with ρ = −1.22 over
    Cobb–Douglas nests; the CES is concave.
  - YN_t appears only in its defining row and in
    `Y_{t+1} = 0.815 Y_t + YN_t`; Y_t appears in the budget row
    `Y_t = C_t + I_t + EC_t` with the favourable sign.
  - The first period has the same form with a constant.
  - All other rows are linear. 96 of 97 variables have no upper bound.
- **pindyck (OPEC cartel pricing, Pindyck 1978).** Checked.
  - 16 periods; control: price p_t ≥ 0.
  - States: total demand (linear in lagged prices), fringe supply
    `s_{t+1} = 0.75 s_t + 1.02^{−cs_t/7}(1.1 + 0.1 p_t)`, cumulative fringe
    supply cs, and reserves r.
  - Revenue `(p_t − 250/r_t)·d_t`; the objective is the discounted revenue
    sum.
  - State dimension 3–4; width 9. 112 of 116 variables have no upper bound.
- **pricing050 (Davarnia; marketing).** Checked.
  - Maximization of a linear objective (negative costs) over 50 variables in
    [0, 10].
  - 5 dense rows, each a sum of univariate terms `a·x·exp(−g(x))` with g
    one of 0.1x, 0.01x² or 0.001x³.
  - All nonlinear terms are univariate (nonlinear-primal width 0).
- **eg_disc_s, eg_disc2_s, eg_int_s (Bram Schoonen's collection).** Checked.
  - 7 decision variables: 3 or 4 bounded integers (small ranges) and 3 or 4
    continuous variables in boxes.
  - 28 rows `objvar ≥ c_k + f_k(x)`; each f_k is a sum of 97 products of 7
    Gaussians, so the problem is a minimax.
  - Integer combinations: eg_disc_s 1764, eg_disc2_s 3751, eg_int_s 16.
  - eg_all_s (all integer, 28224 combinations) is closed by SCIP alone.
- **powerflow0030p/0039p/0039r.**
  - AC optimal power flow on the IEEE 30/39-bus cases, in polar (p) or
    rectangular (r) form.
  - Angle-difference limits of ±0.26 rad, apparent-power line limits and
    quadratic cost.
  - Width 16; 11 after removing 8 hub variables.
  - powerflow0030r has the same primal value as 0030p and is closed by
    ANTIGONE (576.8934129).
  - powerflow0039p/0039r carry an objective constant of 2 in the OSIL.
- **water (GAMS model library).**
  - 41 variables, 25 equality rows, 16 degrees of freedom.
  - 14 pipes with Hazen–Williams losses `q|q|/d^5.33` and diameter costs
    `d^1.29`; diameters in [0.15, 2].
- **waterful2.** 629 variables, 56 binaries, width 24; pressure losses
  `C·square(C)`.
- **feedtray (Viswanathan & Grossmann).**
  - Distillation column with 7 feed-location binaries and a tray-by-tray
    chain.
  - Vapor pressure is exp of a polynomial in T/Tc; enthalpies are
    polynomials. Width 15.
- **heatexch_gen1/2 (Escobar & Grossmann).**
  - Stage-wise heat-exchanger-network superstructure with 12 or 16 binaries.
  - LMTD terms with ln; area^0.6 costs. Width 13 or 10.
  - The best bound is from LINDO; the other solvers are far lower
    (heatexch_gen2: 627371 against about 580000).
- **ann_cumene_tanh (Schweidtmann & Mitsos 2019).**
  - 794 variables, 789 equality rows and 1 inequality, so about 5 degrees
    of freedom; 250 tanh neurons.
  - 66 variables are unbounded. No dual bound is listed.
- **methanol50/100 (COPS parameter estimation).**
  - Least squares (objective constant 5.016 in the OSIL) over a collocation
    model.
  - 5 kinetic parameters in [0, ∞) are hub variables of degree 900.
  - Listed duals are 0 (plus the invalid LINDO value on methanol50).
- **popdynm50/100/200 (COPS marine population dynamics).**
  - Least squares with 7 hub parameters. Width 81–84 because of dense linear
    coupling; nonlinear-primal width 2.
  - Duals are 0 against 19746.5.
- **glider200/400 (COPS hang glider).**
  - Free final time: one hub step variable of degree 1601; 4 states and 1
    control.
  - Listed primal values across sizes: −244053 (glider50; confirmed by BARON
    −244077.6 and LINDO), −1255.06 (glider100; closed by COUENNE and LINDO),
    −2.42e6 (glider200), −1247.97 (glider400).
  - The discretized models therefore behave very differently across sizes.
    glider400's listed primal is probably far from optimal.
- **junkturn (CUTEr / QPLIB 8683).**
  - 200008 variables: a convex quadratic objective (sum of squared torques)
    with bilinear rigid-body dynamics; all variables free.
  - Listed primal 1.01e-4 (p2), but the "other point" p1 has objective
    2.05e-6 at infeasibility 4e-7. The primal side is also uncertain.
- **cesam2cent (social accounting matrix, cross entropy).**
  - 157 ln terms, 98 degrees of freedom.
  - Same primal value as cesam2log (0.50796), which ANTIGONE alone closed at
    5.3e-5.
- **waternd_fosspoly1** (1276 binaries, width 22), **saa_2** (400 binaries,
  6 hubs of degree up to 3802, degree-12 product terms) and
  **sfacloc1_4_95** (chance-constrained facility location, 8 hubs) were not
  inspected beyond `structure.jsonl`.

## 6. Ranking

Scores are my judgment on a 1–5 scale:

- **T**: tractability of a rigorous structure-aware dual bound that closes
  most of the gap;
- **P**: payoff, meaning the size of the best listed gap, the number of
  instances, and interest in the instance or family.

| target | T | P | T×P | deciding facts |
|---|---|---|---|---|
| ex6_2_7, ex6_2_5 | 4.5 | 3 | 13.5 | 6 degrees of freedom; phase-separable; homogeneous; open since the 1999 handbook; BARON gap 564% / 57% |
| KAN family (6) | 4 (r3) / 3 (r5) | 3.5 | 12–14 | 3- or 5-D reduced space; box only; new 2025 family; gaps up to 612% |
| chain50–400 | 2.5 | 5 | 12.5 | width 2 after one multiplier; best listed bounds trivial; COPS classic; 4 sizes |
| waterno2_06–24 | 2.5 | 5 | 12.5 | clean period decomposition; the census's flagship constant-width family with growing gaps |
| catmix100–800 | 2.5 | 4.5 | 11 | 2-D positive bilinear system; only LINDO has a bound; COPS |
| pindyck | 3.5 | 3 | 10.5 | 116 variables, 16 periods; free variables probably cause most of the gap |
| powerflow0030p/0039p/0039r | 3 | 3.5 | 10.5 | ACOPF interest is high, but gaps are 0.12–0.7% and the SDP route is standard |
| etamac | 5 | 2 | 10 | almost certain via convexity; gap only 0.73% |
| pricing050 | 4 | 2.5 | 10 | separable with 5 coupling rows |
| hvycrash | done | 2 | – | Section 3.1 |
| eg_* (3) | 4.5 | 1.5 | 7 | brute-force enumeration plus 3–4-D interval B&B; obscure source |
| water | 3 | 2.5 | 7.5 | 16 degrees of freedom; GAMS classic; 9.5% gap |
| ann_cumene_tanh | 3 | 2.5 | 7.5 | about 5 degrees of freedom, but a flowsheet with possible recycle |
| methanol50/100 | 2 | 3.5 | 7 | 5 unbounded parameters; validated collocation needed |
| quantum | 5 | 1 | 5 | Section 3.2 |
| glider, junkturn, popdynm, waternd_fosspoly1, saa_2, heatexch, feedtray | ≤ 2 | 2–4 | < 7 | see Section 8 |

The top 8 (Section 7) follow the T×P order. I placed etamac and pricing050
ahead of powerflow because their certificates would follow the program's
structure-aware approach. The powerflow bounds would come mostly from
standard SDP machinery; see Section 8.

## 7. Attack plans for the top 8

**1. ex6_2_7 and ex6_2_5.**

- Structure: Section 5. Each phase function G_p is homogeneous of degree 1,
  and only the 3 mass balances couple the phases.
- Lagrangian: dualize the mass balances with multipliers λ, taken as the
  chemical potentials at the listed point, which can be downloaded from
  MINLPLib. Then

      L(λ) = λᵀb + Σ_p min_{n_p ∈ box} [G_p(n_p) − λᵀn_p].

- Each inner minimum is `t · min_y (g_p(y) − λᵀy)` over compositions y in
  the 2-simplex (limited by the box), with t the total moles of the phase.
  The inner function is the tangent-plane distance of phase-stability
  analysis.
- Certify its minimum with a 2-D interval branch and bound using outward
  rounding. It needs careful enclosures of `y ln y` and `ln(linear form)`
  near the 1e-7 bounds, plus an explicit bound on the truncation caused by
  those bounds.
- ex6_2_7: the three phase functions are identical, so L(λ*) equals the
  convex envelope of G at the feed. Three phases suffice for three
  components, so no duality gap is expected up to the 1e-7 truncation. If
  the tangent-plane distance is negative somewhere, the listed point is not
  global; the minimizer then gives a better phase split and a new λ.
- ex6_2_5: the ideal third phase differs, so a gap can remain only if the
  envelope needs three liquid points. The fallback is branching on one
  liquid composition.
- Also: verify homogeneity with the exact decimal coefficients, not only
  numerically. The same code applies to the other ex6_* Gibbs instances.
- Effort: days. Risk: low.

**2. KAN family (6 instances).**

- Reconstruct each univariate edge function from the rows:
  - SiLU part;
  - spline knots and coefficients from the binary interval-selection
    encoding.
- Validate the reconstruction against the MINLP rows:
  - fix the inputs at many points;
  - solve the forward pass exactly;
  - compare in 50-digit arithmetic.
- Run a reduced-space interval branch and bound over the 3-D or 5-D input
  box. Bounds come from:
  - exact range bounds per spline piece (piecewise polynomials: endpoints
    and interior critical points);
  - interval SiLU;
  - centered or monotonicity forms for the output layer.
- Handle the objective's affine map and any objective constant in the OSIL
  explicitly.
- Expect r = 3 (n = 4, 5, 9) to be quick. kan_r5_h1_n8 (5-D, 8 neurons, no
  finite relative gap) is the hardest.
- Before investing, check the source paper for global solutions already
  reported with the authors' own method.
- Risk: decoding mistakes; the forward-pass comparison controls them.

**3. chain50–400.**

- (a) Bound propagation. The length row gives `Σ w_i s_i = 4` with
  `Σ w_i = 1` and `s_i ≥ 1`. That bounds every `|u_i|` and gives
  `|x_i − 1| ≤ 4`, which removes the free variables behind the collapse of
  solver bounds.
- (b) Dualize the single length row with the multiplier μ from the KKT
  point. What remains is a chain with 1-D state x and trapezoid coupling of
  consecutive slopes, i.e. a DP on the state (x_i, u_i).
- (c) A plain Lagrangian on the dynamics rows will be weak. For fixed u the
  stage terms are linear in x, so the stage minimum jumps to box corners
  unless u equals the optimal control. Instead, build a value-function
  lower bound `W_i(x, u)`:
  - take linear terms from the costates and quadratic terms from the
    discrete Riccati recursion of the second variation at the KKT point;
  - verify the stage inequalities
    `w_i (x+μ) s(u) + W_{i+1}(x + h(u+u')/2, u') − W_i(x, u) ≥ −ε_i`
    on the propagated box by 3-D interval branch and bound. The N stages
    are independent and cheap.
- This is the discrete analogue of the Weierstrass field-of-extremals proof
  for the catenary, which is valid while `x + μ > 0`.
- Main risk: one quadratic W may fail far from the optimal trajectory. In
  that case split the box, use a minimum of several quadratics, or use
  coarse interval DP cells only away from the trajectory.
- Payoff: the largest relative gaps among well-known instances. Success
  would also answer the census question for a width-2 family.

**4. waterno2_06–24.**

- Dualize, with multipliers from the listed primal point or a local solve:
  - the 3(T−1) tank-level copy rows;
  - the single horizon-wide row.
- The Lagrangian then splits into T independent single-period MINLPs of 166
  variables and 9 binaries each. Single-period and short-horizon versions
  (waterno2_01–04) are solved in MINLPLib.
- The dual bound is `Σ_t (bound of period t)`, maximized over the 3(T−1)+1
  multipliers by a bundle method.
- Two levels of rigor:
  - first, use SCIP's dual bounds on the small subproblems, which are valid
    bounds but solver claims;
  - then certify the period subproblems independently. Enumerate the pump
    configurations (at most 2^9 per period, fewer with the ordering rows)
    and bound each continuous hydraulic NLP by bound propagation plus
    interval branch and bound.
- The Lagrangian gap comes from nonconvexity of the per-period value
  function in the tank levels. If it is large, use a DP on the 3 levels
  with coarse cells, or add level-cut valid inequalities.
- The listed primal for T = 18 and 24 may also be improvable. Record the
  best period-by-period primal repair.
- Payoff: this is the census example of constant width with a growing gap
  (0.71 → 5.8 best listed).

**5. catmix100–800.**

- Bound propagation: show that the states stay in the simplex
  `x ≥ 0, x1 + x2 ≤ 1`. The trapezoid matrices are M-matrices for u in
  [0, 1] and h ≤ 0.01; check this.
- For fixed controls the dynamics are linear. So the true value function
  `V_i(x)` is concave and positively homogeneous in x, i.e. a minimum of
  linear functions.
- The trapezoid couples u_i and u_{i+1}, so certify by backward recursion on
  `V_i(θ, u_i)`, where θ = x2/(x1+x2) and u_i is the previous control:
  - represent the bound as a minimum of linear forms in x;
  - handle the next control by interval cells in u'.
- Each stage map is `I + O(h)`, so the loss per stage is `O(h·δ)` for cell
  width δ, and the total loss is `O(δ)`. This avoids the first-order loss
  per stage that sank the generic cell DP in the first wave. It needs to be
  checked on catmix100 before scaling.
- Remember the objective constant −1.
- Payoff: LINDO is the only listed bound, and it degrades from 38% to 3000%
  with N.

**6. pindyck.**

- First derive bounds on all 112 variables without upper bounds, then rerun
  a solver. The same was done as a baseline in the first wave.
  - Price is bounded because OPEC demand `d_t = td_t − s_t ≥ 0` and td
    decreases in past prices.
  - Reserves `r_t ≥ 500 − Σ d` bound the 250/r terms.
  - Fringe supply is bounded by its recursion.
- Then use a partial Lagrangian on the linear state rows (total demand,
  cumulative supply, reserves, OPEC demand) with multipliers from a local
  solution. This leaves per-period blocks with the two nonlinear rows (fringe
  supply, revenue) in 3–5 variables.
- Certify the blocks by interval branch and bound, as for lukvle10. If a
  duality gap remains, keep the fringe-supply recursion exact and run a
  small exact block DP over pairs of periods.
- Payoff: 23% best listed gap on a classic model. Risk: moderate, because
  exp(cs)·p couples the states nonlinearly.

**7. etamac.**

- Relax the 9 CES equalities `YN_t = CES_t(K, E, N)` (and the first-period
  row) to `YN_t ≤ CES_t`.
  - This is a valid relaxation for a lower bound.
  - It is convex: the objective is −ln, the other rows are linear, and CES
    with ρ < 0 over concave Cobb–Douglas nests is concave.
  - It should be tight: YN increases future Y, which relaxes the budget
    row, and utility increases in C.
- Solve the convex relaxation. Obtain a rigorous bound by weak duality at
  the computed multipliers: for the convex Lagrangian `φ`,
  `φ(x) ≥ φ(x̂) + ∇φ(x̂)ᵀ(x − x̂)`, minimized over a propagated box, gives a
  certified value.
- Check concavity symbolically (composition rules) and numerically
  (Hessian eigenvalues at samples).
- Payoff: small (the gap is 0.73%), but it is a clean example of hidden
  convexity that MINLPLib's convexity flag misses. Effort: about a day.

**8. pricing050.**

- The Lagrangian dual over the 5 coupling rows separates into 50 univariate
  problems on [0, 10]. Each is certified by 1-D interval branch and bound,
  and the dual is minimized over 5 multipliers.
- The Shapley–Folkman bound on the duality gap is at most about 6 times the
  largest per-variable nonconvexity. That should already cut most of the
  18% gap.
- Close the rest by branch and bound on the few variables whose Lagrangian
  maximizers are not unique or sit in nonconcave regions. This is
  essentially the decision-diagram setting of the source paper (Davarnia
  2021); check that paper's reported bounds first.
- Remember that the problem is a maximization: the dual bound is an upper
  bound.

## 8. Other candidates and notes

- **powerflow0030p/0039p/0039r.**
  - An SDP (or chordal-SDP) relaxation of the rectangular form, with the
    angle limits written as linear constraints on the W matrix, plus a
    verified dual solution (Jansson-style rounding) may close these if the
    relaxation is exact. That is not known for these variants with
    ±0.26 rad limits.
  - Separately, 0030r is closed by ANTIGONE. If the rectangular model is a
    relaxation of the polar one under `V e^{iθ}`, with matching bounds and
    objective, that bound transfers to 0030p. Checking this is cheap.
- **eg_disc_s, eg_disc2_s, eg_int_s.** Enumerate the integer combinations
  and run a 3- or 4-D interval branch and bound on the minimax of 28 smooth
  functions (vectorized Gaussian enclosures). This is almost certainly
  tractable (about 1e4 small boxes per combination), but the interest is
  low. eg_all_s (closed by SCIP only) can be checked by pure enumeration of
  28224 points.
- **quantum.** Section 3.2. First decide the Γ-domain question.
- **water.** Small, but loops and signed powers. A dual bound by
  enumeration over diameter cells with flow-direction branching might work
  (16 degrees of freedom). Not assessed in detail.
- **ann_cumene_tanh.** About 5 degrees of freedom. If the flowsheet admits a
  forward evaluation order (no recycle), this is a reduced-space interval
  branch and bound like the KAN family, and it would supply the first dual
  bound listed for the instance.
- **methanol50/100, popdynm50/100/200, and pinene and gasoil.** COPS
  parameter estimation with 3–7 unbounded parameters. A reduced space over
  the parameters would need validated solutions of the collocation system.
  First prove parameter bounds from the objective level set. The payoff is
  moderate to high, including independent checks of the LINDO-only
  closures; the effort is high.
- **glider200/400.** The listed values suggest that the discretized models
  admit solutions far from the COPS reference (about 1248), possibly
  through the free step variable. Understand the model before bounding
  anything.
- **junkturn.** 200008 variables. Both the primal and the dual side are
  uncertain (see Section 5), so it is not a first-wave-style target.
- **cesam2cent.** Check equivalence with cesam2log, which ANTIGONE alone
  closed. The payoff is small.
- **heatexch_gen1/2, feedtray, sfacloc1_*, saa_2, waternd_fosspoly1,
  nuclear*, ex8_3_*.** Moderate to wide structure plus binaries, and no
  specific mechanism identified. Not recommended for the second wave.
- **Instances with no listed primal** (mpbp_*, gabriel05–07, nuclear10a,
  chp_shorttermplan2c) need a primal first.

## 9. Caveats

- Widths are heuristic upper bounds from the census. The "state dimension"
  and decomposition claims above come from direct row inspection only where
  marked "checked".
- The listed bounds are MINLPLib's as of the fetch. They are solver claims
  of mixed reliability (Section 3.3). Gaps use MINLPLib's convention, which
  inflates gaps when values are near 0.
- The T and P scores are judgments, not measurements. None of the top-8
  plans has been tried yet.

## 10. Files and commands

Files in this directory:

- `fetch_pages.py`: selects candidates (`candidates.json`) and fetches pages
  (`pages/`, log `fetch.log`).
- `parse_pages.py`: produces `fetched.json` (all fields, including the full
  dual-bound lists) and `fetched.csv` (one row per candidate).
- `structure.py`: produces `structure.jsonl` (35 instances) and
  `structure.log`.
- `hvycrash_check.py`: the Section 3.1 pattern check.
- `check_points.py`: 50-digit evaluation of downloaded MINLPLib points
  (`sol/methanol50.p4.sol`, `sol/hvycrash.p1.sol`, `sol/hvycrash.p3.sol`),
  using `../open-instances/osil_eval.py`. It reads the OSIL objective
  constant from the file and adds it, because `osil.py` and `osil_eval.py`
  omit it.

Commands run (targeted only; no project-wide checks, no CI):

```
python3 fetch_pages.py            # 283 pages, sequential, 1.5 s delay
python3 parse_pages.py            # 283 parsed, 146 kept
python3 structure.py <35 names>   # see structure.jsonl
python3 hvycrash_check.py         # pattern asserted for 50 stages
python3 check_points.py methanol50.p4 hvycrash.p1 hvycrash.p3
```

I also ran inline Python checks for the ex6_2 phase separability and
homogeneity, the waterno2 period decomposition, the etamac variable
occurrences, the KAN inequality rows, the quantum objective near n = 1/4, and
the objective constants in the candidate OSIL files.
