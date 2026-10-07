<!-- Written to disk by the root from the structured return value of agent 'author:primal-water-ann-kan' (the harness blocks subagents from writing report files). Status: complete. -->

# Exactly feasible primal points: waterno2_06–24, ann_cumene_tanh, and KAN relaxation points

Date: 2026-10-01. Track: primal-water-ann-kan. Status: complete for all nine required instances. All checks were run by the code in `code/` of this folder (/workspace/minlp-notes/research-20260929/publication/primal/water-ann-kan), written for this track. Two exact checkers were written separately for waterno2, but by the same author, so none of this has been independently reviewed. Every run was a single process that took under 4 s.

## 1. Results

For each instance, the table gives a point that satisfies every constraint exactly, a rigorous enclosure of its objective value, and the rigorous gap to our dual bound. The gap is the upper end of the enclosure minus the dual bound, rounded up. For KAN, "feasible" means feasible for the network relaxation R (Section 5), because the KAN OSIL models have no exactly feasible point.

| instance | earlier primal (max row violation) | exactly feasible point: objective | dual bound (exact certified value, rounded down) | rigorous gap | gap / abs(dual) | gap / abs(primal) |
|---|---|---|---|---|---|---|
| waterno2_06 | listed p4: 282.8880373869047 (1.08e-11) | **282.888037386904807969455615812871** (exact rational) | 278.230573774560 | 4.65747 | 1.674e-2 | 1.647e-2 |
| waterno2_09 | ours: 914.011970349935 (1.0e-9) | **914.011975237085991…** (exact rational) | 824.834692454636 | 89.1773 | 1.082e-1 | 9.757e-2 |
| waterno2_12 | ours: 2233.821335281894 (1.0e-9) | **2233.821345608215233…** (exact rational) | 2089.754565439515 | 144.067 | 6.894e-2 | 6.450e-2 |
| waterno2_18 | ours: 5023.982735142767 (4.4e-9) | **5023.982760460661871…** (exact rational) | 4790.820715376162 | 233.163 | 4.867e-2 | 4.641e-2 |
| waterno2_24 | ours: 6963.795154460378 (1.0e-9) | **6963.795180156419512…** (exact rational) | 6576.151388415564 | 387.644 | 5.895e-2 | 5.567e-2 |
| ann_cumene_tanh | wave 3: −3379.98239407177 | **[−3379.982394071771548095722619880929, −3379.982394071771548095722619880928]** (width 1.0e-54) | −3386.540229136919 | 6.55784 | 1.937e-3 | 1.941e-3 |
| kan_r5_h1_n3 (point of R) | wave 3: −262.86422588507 | **−262.8642258850652404445355810866…** (width 8.4e-54) | −262.864225909222 | 2.41562e-8 | 9.190e-11 | 9.190e-11 |
| kan_r5_h1_n5 (point of R) | wave 3: 0.27258325395662 | **0.2725832539566226973074658533640…** (width 1.8e-54) | 0.272583253854 | 1.01776e-10 | 3.734e-10 | 3.734e-10 |
| kan_r5_h1_n8 (point of R) | wave 3: 0.069327860606191 | **0.06932786060619108532659407018319…** (width 4.1e-54) | 0.069327860510 | 9.56660e-11 | 1.380e-9 | 1.380e-9 |

Extra, outside the required list and run at no extra cost with the same code: the three r3 KAN instances also have points of R. kan_r3_h1_n4 has objective 0.002781237221441814129…, gap 6.88605e-11. kan_r3_h1_n5 has −0.01104267941448729530…, gap 1.07295e-10. kan_r3_h1_n9 has 0.01296366005303932849…, gap 8.95647e-11.

How to read the results:
- **The gap statements now rest on exactly feasible points.** For each waterno2 instance and for ann_cumene_tanh, a point exists that satisfies every row, bound and integrality requirement of the cached OSIL model exactly. For the three r5 KAN instances, a point exists that satisfies every row of the OSIL model except the partition-of-unity rows, plus every variable bound. Such a point lies in R.
- **waterno2_06.** The listed MINLPLib point p4 is not exactly feasible. Its largest row violation is 1.08e-11, in row e94. A point within 3.1e-13 of p4 is exactly feasible. Its objective is the rational number 282888037386904807969455615812871 / 10^30. This is 1.1e-13 above the sum of p4's cost values (282.8880373869047) and 2.0e-13 below the objvar value in p4's file (282.888037386905012). The gap to our dual bound 278.230573774 is 1.674% of the dual. This is the 1.67% of the summary, now measured against an exactly feasible point.
- **waterno2_09–24.** The exact points cost 4.9e-6, 1.03e-5, 2.53e-5 and 2.57e-5 more than our earlier tolerance-feasible points. In relative terms this is 4e-9 to 5e-9. The relative gaps to the dual are 10.82%, 6.89%, 4.87% and 5.90%, the same as in the summary at its precision.
- **ann_cumene_tanh.** The wave-3 primal point is exactly feasible as it stands. More precisely, the point defined by its five input values (the 16-digit decimals in `sol/ann_cumene_tanh.wave3.sol`) is exactly feasible. The 30-digit rounding of all 794 coordinates in that file is not, because of rounding. The gap is 0.194%, as in the summary.
- **KAN.** The improved wave-3 values are attained by points of R, so they are valid upper bounds on the optimum of R. The gaps of about 1e-10 (2.4e-8 absolute for r5_n3) match the summary.

## 2. waterno2: method (exact algebraic construction)

All rows of waterno2 are polynomials of degree at most 3 with decimal coefficients. The code in `code/water_exact.py` builds a point in which every coordinate is either rational or an element of a quadratic field Q(w_k). Here w_k is the speed of one running pump station in one period. No coordinate mixes two fields, so every row can be decided exactly.

1. **Fix the binaries and simplify.** The binaries are taken from the numerical point and substituted. Some single-variable rows meet a variable bound; these pin the variable (for example, an off pump has flow 0 and speed 0.6). Some pairs of rows pin a linear form; these become equalities. For example, the two big-M rows of a running pump force pump head = station head. Pinned variables: 191, 227, 267, 378 and 489. Pair equalities: 20, 50, 78, 130 and 182 (for 06, 09, 12, 18 and 24).
2. **Alias the pump flows.** The pumps of one station share one speed variable and one head. If h(q, w) = H holds for two identical pumps with the same w and H, the pump-curve rows force their flows q to be equal. So the flows of the running pumps of a station are aliased to one representative. These representatives are the free choices ("seeds"): 10, 20, 31, 49 and 64 running stations. Each seed starts at the exact decimal value from the numerical point.
3. **Linear phase.** The linear rows express every tank level and flow total as an affine function of the seeds. Some constraints are active at the numerical point: tank levels at their bounds (for example, the tank-1 level at 5 for several consecutive periods in waterno2_09) and the horizon row. These are imposed as exact equalities by a minimum-norm correction of the seeds, computed in exact rational arithmetic. Dependent active constraints are removed by exact elimination. The largest seed correction was 3.0e-16 (06), 1.1e-10 (09), 8.8e-9 (12), 1.0e-9 (18) and 6.1e-10 (24).
4. **Nonlinear phase.** Equality rows are solved one unknown at a time. Each station speed is a symbol, and values are polynomials in that one symbol. Once the flows and levels are known, the pump-curve row of a running station becomes a quadratic in its speed w with rational coefficients. The speed is fixed as the root nearest the numerical speed, with a rational isolating interval (lo, hi) of width 2e-45. A sign change of the quadratic on (lo, hi) proves that exactly one root lies inside. The discriminant is checked not to be a rational square, so the root is irrational.
   Some station-B head rows are active at the numerical point, namely head ≥ the head required by tank 2. These are imposed as equalities, so the station-B head is rational. A few speeds are not determined by any row because their station-B head row is inactive. These were fixed at rationals: 0.8 in most cases (x533 in 06; x794 and x802 in 09; x1068 in 12; x1596 in 18; x2114 in 24). In 12 the others were x1059 = 0.800000000001236 and x1074 = 0.897069455653731. A few slack-type variables were also left free. These were fixed at their active bound or at the numerical value: heads of stations that are off (1000) and the slacks x548–x553-type (100).
5. **Speeds at their bounds.** Several running stations have their speed exactly at its lower bound 0.8 in the numerical point. In waterno2_18 the exact root came out slightly below 0.8, first for x1602, then for x1601 and x1600. The numerical point itself has x1602 = 0.79999999953, below the bound. For each failing station, the station flow was shifted up by 1e-9. With the head pinned, the speed increases with the flow, and the linear phase was re-solved. The retry is automatic and logged. Three stations needed a shift. No other instance needed one.
6. **Costs.** Each cost variable appears in one row: cost ≥ (power expression)/price. The power expression lies in one field. Each cost is set to a rational upper bound of that value, rounded up on a 1e-30 grid. The objective, which is the sum of the costs, is then an exact rational number. The cost rows hold strictly or with equality.
7. **Check.** `verify()` evaluates every OSIL row and bound in exact field arithmetic (`code/qfield.py`):
   - Equalities must reduce to exactly 0.
   - An inequality sign is decided exactly. For p + r·w with rational p, r, the code compares the rational −p/r with the isolated root by evaluating the quadratic at it.
   The construction steps above only produce candidates; validity rests on this check alone.

Irrational speeds per instance: 9 (06), 18 (09), 28 (12), 48 (18) and 63 (24). All other coordinates are rational or lie in the field of one speed.

**Second exact check** (`code/check_water_point.py`). This check reads only the point file and the OSIL model, and uses neither the construction nor qfield. It rewrites each w_k as (−B + s·√d)/(2A), with d = B² − 4AC and the sign s fixed exactly from (lo, hi). Values are pairs a + b√d, and signs are decided by comparing a² with b²d. The result for all five instances: every equality row (735, 1104, 1473, 2211 and 2949 rows) reduces to exactly zero, and every inequality row, variable bound and integrality requirement holds. The objective equals the stored rational (`logs/check_water_points.log`).

**OSIL reading cross-check.** `code/check_water_mp.py` evaluates the same points at 60 digits with the earlier reader `osilx.py`/`ev.py`, which was written by another agent. All rows agree to 1.3e-57 and there are no bound violations (`logs/check_water_mp.log`). As a further check, the reader in this track reproduces wave 2's exact evaluation of p4: objective 282.8880373869047 and a row violation of 1.08e-11 in e94 (`logs/test_osil_p4.log`).

## 3. ann_cumene_tanh: method (forward construction with an existence argument)

`code/fwd.py` and `code/nn_exact.py` build the point as follows:
- The five inputs x723–x727 are fixed at rationals. These are the 16-digit decimals of the wave-3 point: 1854640286460337/5·10^12, 982921746111241/1.25·10^15, 1620252679906157/10^15, 9494678019619749/10^16 and 734065236105183/10^15.
- Every other variable is **defined** by one equality row in which it is the only unknown. The variable must appear linearly, and the interval enclosure of its coefficient must exclude 0. The variable's value is then the row solved for it. The tanh rows define a neuron output as tanh of a known argument. The bilinear rows e749 and e782–e787 define x754 and x787–x792 by division by x753, x746 or x766, whose enclosures exclude 0.
- All 789 equality rows are used as definitions, in an acyclic order. So the real point x* given by the definitions satisfies every equality row exactly.
- The code encloses x* in outward-rounded intervals (mpmath iv, 60 digits). The only inequality row, e789 (x772 ≥ 0.999), is proved with margin 9.98e-13. All 728 finite variable bounds are proved; the bound x647 ≥ −1 has margin 1.25e-12. There are no integer variables.
- The objective enclosure has width 1.0e-54.

The wave-3 point already sat strictly inside the two active constraints, x647 ≥ −1 and x772 ≥ 0.999, so no input had to be moved.

As a cross-check, `code/check_nn_point.py` evaluates the interval midpoints with the earlier reader osilx/ev at 60 digits. The largest row residual is 9.6e-42, the objective agrees with the enclosure, and no bound is violated.

## 4. Assumptions and what is proved

- **waterno2 (proof in exact arithmetic).** Python `fractions` only, with no floating point. The point file defines the point exactly: each symbol is given by (A, B, C, lo, hi), and each coordinate by rationals or by c0 + c1·w_k. The claim also depends on the correctness of the OSIL reader `code/osil.py`. That reader was cross-checked against `osilx.py`, as described in Section 2.
- **ann_cumene_tanh and KAN (proof by enclosure).** These rest on two assumptions:
  - mpmath 1.3.0's iv context encloses +, −, ×, ÷ and exp with outward rounding. tanh is evaluated through the identity tanh(s) = 1 − 2/(exp(2s) + 1). The SiLU rows are evaluated as written in the OSIL model, z/(1 + exp(−z)). Interval endpoints are converted to rationals exactly from the raw mpf tuples.
  - The existence argument is the definitional structure of Section 3, which the code checks as it builds the point.
- **The dual bounds are taken as certified by earlier work and not re-examined here:**
  - waterno2_06: certB, exact 39157472136693483/140737488355328 (cellslopes/logs/certB_verify.json);
  - waterno2_09–24: `certified_bound_exact` in open-instances-wave2/waterno2/logs/cert_TT_w1_impl.json;
  - ann_cumene_tanh: −3386.5402291369187 (binary64);
  - KAN: `dual_bound` in open-instances-wave3/logs/<name>.result.json, which is a bound for R.
- **What is numerical only:** the 60-digit cross-checks and the `*.approx40.sol` files. The `.sol` files are 40-digit roundings and are not exactly feasible.

## 5. KAN: the relaxation R and the points

The OSIL models are exactly infeasible, because the partition-of-unity rows are inconsistent in exact decimals (proved by the wave-3 verifier). The claims therefore concern R. R is the OSIL model without:
- the partition rows Σ_m B_m = 1;
- the bounds B ≥ 0;
- every intermediate-variable bound except the input class and the hidden class.

R keeps every other row, the one-hot rows and the big-M rows. Since R only drops constraints, any point that satisfies the OSIL model minus the partition rows lies in R.

Construction (`nn_exact.py kan_r5_h1_nX`):
- **Inputs.** The five inputs are fixed at the exact binary64 values of the wave-3 input vector u in open-instances-wave3/logs/<name>.result.json. The input variable indices are taken from the wave-3 decoder only as a hint. The construction then has to determine every variable, and it does.
- **Partition rows.** The partition rows are identified by their form: linear equalities with all coefficients 1, right-hand side 1, over continuous variables. There are 54, 90 and 144 of them, three per edge. They are never used.
- **Interval binaries.** When an edge argument becomes known, the code sets its interval binary to the first knot interval whose big-M rows hold for the whole enclosure of the argument.
- **Definitions.** Every other variable is defined by one row as in Section 3. In layer 1 the edge arguments are rational, so the B-spline bases are exact rationals. SiLU makes the remaining values transcendental.

Checks for kan_r5_h1_n3 / n5 / n8:
- 617 / 1027 / 1642 equality rows are used as definitions.
- The 18 / 30 / 48 one-hot rows hold exactly.
- 360 / 600 / 960 big-M rows hold exactly (layer 1), and 72 / 120 / 192 are proved by intervals (layer 2). The smallest margin is 1.4e-2.
- **Every** variable bound of the OSIL model is proved, including the ones R drops.
- 216 / 360 / 576 binaries are exactly 0 or 1.

The cross-check with osilx at 60 digits gives these largest residuals:
- kept rows: 2.0e-43, 5.4e-43 and 1.5e-43;
- partition rows: 3.3e-16, 2.0e-16 and 5.8e-16, matching the verifier's values;
- no bound is violated.

## 6. What failed or was adjusted

1. **A first construction run hit the speed bounds.** The first run for waterno2_06 stopped on unknowns that no row determines: heads of stations that are off, and slack-type variables. The fix was to fix them at an active bound or at the numerical value. Later, waterno2_18 failed its exact check because a speed root lay below its bound 0.8. The numerical point had x1602 = 0.79999999953, below the bound.
2. **A blanket flow shift was inconsistent.** Shifting the flow of every station whose speed sits at a bound made the active constraints of 06 and 09 inconsistent. In 09, for example, station x802 also has its flow at its lower bound 0.25. The final code shifts only stations whose exact check fails, by 1e-9 each. Only waterno2_18 needed this, for three stations; its log shows the three attempts.
3. **An endpoint conversion bug was fixed.** Converting interval endpoints with mp.mpf(X.a) can round when the mp and iv precisions differ. The code now reads the raw endpoint tuples.
4. Nothing resisted. No instance needed an interval Newton or Krawczyk step, because every point is either algebraic and checked exactly (waterno2) or defined explicitly row by row (ANN and KAN).

## 7. Files

All paths are relative to /workspace/minlp-notes/research-20260929/publication/primal/water-ann-kan.
- `points/waterno2_TT.exact.json` (TT = 06, 09, 12, 18, 24): the exactly feasible points.
  - Fields: `symbols` gives each w_k as (A, B, C, lo, hi), the unique root of A w² + B w + C in (lo, hi). `x` gives each variable as a rational string or as {w, c0, c1} = c0 + c1·w_k. `objective` is the exact rational.
- `points/<name>.point.json` (ann_cumene_tanh, kan_r5_h1_n3/n5/n8, plus the extras kan_r3_h1_n4/n5/n9).
  - Fields: `inputs` holds the exact rationals. `x` holds rationals, or outward-rounded intervals {lo, hi} with the row `defined_by`. `objective_lo` and `objective_hi` are rounded outward. `dropped_rows` lists the KAN partition rows. `gap_upper` is rounded up. `log` holds the run messages.
- `points/<name>.approx40.sol`: 40-digit roundings in MINLPLib .sol format, for convenience. These are not exactly feasible.
- `code/osil.py`: OSIL reader with exact decimals.
- `code/qfield.py` and `code/test_qfield.py`: quadratic-field arithmetic and its randomized test.
- `code/water_exact.py`: the waterno2 construction and exact check.
- `code/check_water_point.py`: the second exact checker.
- `code/check_water_mp.py`: the 60-digit cross-check with osilx.
- `code/fwd.py`: forward construction with interval enclosures.
- `code/nn_exact.py`: driver for the ANN and KAN instances.
- `code/check_nn_point.py`: the 60-digit cross-check with osilx.
- `code/gaps.py`: the gap table, in exact arithmetic.
- `code/to_sol.py`: writes the .sol roundings.
- `code/test_osil_p4.py`: reader sanity test.
- `logs/`: output of every run listed in Section 8.

## 8. Commands run

All commands were run from `code/` with Python 3.13 and mpmath 1.3.0, one process at a time. These are the targeted checks of this track only; no CI or project-wide checks were run. Here `<wave2>` = research-20260929/open-instances-wave2/waterno2.

| command | outcome |
|---|---|
| python3 test_osil_p4.py (first run as /tmp/t_osil.py) | p4 objective 282.8880373869047, max row violation 1.08e-11 (e94), as in the wave-2 report |
| /tmp/t_active.py waterno2_TT <point> for TT = 06, 09, 12, 18, 24 (exploratory, not kept) | listed the active rows and bounds at the numerical points |
| python3 test_qfield.py | 300 random fields, 6000 sign tests against mpmath at 60 digits: 0 failures |
| python3 water_exact.py 6 <wave2>/data/waterno2_06.p4.sol ../points/waterno2_06.exact.json | first run stuck (free slack variables); after the fix: exact check passed, objective 282.888037386904807969… |
| python3 water_exact.py T <wave2>/logs/primal_TT_w2.json ../points/waterno2_TT.exact.json for T = 9, 12, 18, 24 | first runs: 09, 12 and 24 passed; 18 failed (speed x1602 below 0.8). Blanket flow-shift version: 06, 09 and 12 inconsistent. Final adaptive version: all five pass; 18 passes after 3 shifted stations |
| python3 check_water_point.py ../points/waterno2_*.exact.json | all rows, bounds and integrality exact; objectives match |
| python3 check_water_mp.py ../points/waterno2_*.exact.json | row residual ≤ 1.3e-57 with osilx; no bound violation |
| python3 nn_exact.py ann_cumene_tanh | 789/789 rows as definitions; e789 and all bounds proved; enclosure width 1.0e-54 |
| python3 nn_exact.py kan_r5_h1_n3 (also n5, n8, and the extras kan_r3_h1_n4/n5/n9) | all variables determined; all kept rows and all bounds proved; gaps as in the table |
| python3 check_nn_point.py ../points/*.point.json | kept-row residuals ≤ 9.6e-42; partition rows 1.8e-16 to 2.5e-15; no bound violation |
| python3 gaps.py | the gap table in Section 1 |
| python3 to_sol.py ../points/*.json | wrote the .approx40.sol files |

## Commands run (from the agent's structured return)

- `python3 /tmp/t_osil.py (saved as code/test_osil_p4.py, rerun): p4 obj 282.8880373869047, max row viol 1.08e-11 at e94`
- `python3 /tmp/t_active.py waterno2_TT <point> for 06,09,12,18,24 (exploratory listing of active constraints)`
- `python3 /tmp/t_qf.py (saved as code/test_qfield.py, rerun): bad 0`
- `python3 water_exact.py 6 .../waterno2/data/waterno2_06.p4.sol ../points/waterno2_06.exact.json (first run: stuck on free slack variables; fixed; then passed)`
- `python3 water_exact.py {9,12,18,24} .../waterno2/logs/primal_TT_w2.json ../points/waterno2_TT.exact.json (first run: 18 failed on speed x1602 < 0.8; the blanket-shift version was inconsistent for 06/09/12; final adaptive version: all pass)`
- `python3 check_water_point.py ../points/waterno2_{06,09,12,18,24}.exact.json: all exact checks pass`
- `python3 check_water_mp.py ../points/waterno2_*.exact.json: residual <= 1.3e-57 with osilx`
- `python3 nn_exact.py ann_cumene_tanh (rerun after the endpoint-conversion fix): passed`
- `python3 nn_exact.py kan_r5_h1_n3 / kan_r5_h1_n5 / kan_r5_h1_n8: passed`
- `python3 nn_exact.py kan_r3_h1_n4 / kan_r3_h1_n5 / kan_r3_h1_n9 (extra): passed`
- `python3 check_nn_point.py ../points/*.point.json: kept rows <= 9.6e-42, partition rows 1.8e-16..2.5e-15, no bound violations`
- `python3 gaps.py: gap table`
- `python3 to_sol.py ../points/*.json: wrote 40-digit .sol roundings`

## Open issues (from the agent's structured return)

- report.md was not written because the tool environment blocks report files for subagents. Its full text is in 'summary' and should be saved verbatim at /workspace/minlp-notes/research-20260929/publication/primal/water-ann-kan/report.md.
- No independent review: all checks are this track's own code. For waterno2 there are two separately written exact checkers by the same author, and the OSIL reading was cross-checked against the earlier osilx.py reader at 60 digits.
- The dual bounds (certB for waterno2_06, the cert_TT_w1_impl exact values, ANN -3386.5402291369187, KAN result.json dual_bound) were taken as certified by earlier work and not re-examined.
- The ANN and KAN proofs assume mpmath 1.3.0's iv context rounds +, -, *, / and exp outward; tanh is evaluated via 1 - 2/(exp(2s)+1).
- KAN claims concern the relaxation R only: the OSIL KAN models have no exactly feasible point (earlier proof). Our points violate only the partition rows, by up to 5.8e-16 in 60-digit evaluation.
- The *.approx40.sol files are 40-digit roundings for convenience and are not exactly feasible; the JSON point files define the exact points.
- Exploratory scripts /tmp/t_active.py were not kept; the parser and qfield tests were copied into code/.
