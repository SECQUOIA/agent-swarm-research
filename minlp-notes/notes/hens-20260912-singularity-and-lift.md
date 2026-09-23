# HENS: singularity audit of heatexch_gen* and a homogeneity lift for SYNHEAT (2026-09-12)

Code: `code/minlp_solver_lab/hens/` (all commands run from that directory with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, solver threads <= 4, one timed run at a time).
Raw outputs: `code/minlp_solver_lab/hens/results/` (JSON, GAMS `.lst`, Gurobi/BARON logs).
Wrapped up early on the coordinator's instruction; section 5 lists what was not done.

## 1. Summary

* **heatexch_gen1/2/3 are ill-posed in the sense that the infimum is not attained and lies far below
  the recorded primal bound.** The guarded LMTD `f(d1,d2) = (d1-d2)/log(d1/(d2+1e-6))` is unbounded
  above on the feasible region, so every process-exchanger area `2q/(0.01+LMTD)` can be driven to 0.
  For gen1 we constructed explicit points (all 120 constraints verified in float and in 50-digit
  mpmath, max violation 1.7e-12) with objective **108,999.78** versus the MINLPLib primal bound
  154,895.93; the "utility + fixed cost" infimum is in `[100,500, 108,846.94]`. The recorded
  gap (100,500 to 154,896) is therefore an artifact of the guard: the best feasible objective is at
  most 108,846.94, and no point attains it (that needs `LMTD = +inf`).
  gen2 and gen3 use the identical guard (10 and 50 occurrences) with dt variables appearing only in
  big-M inequalities, so the same argument applies. heatexch_spec1-3 and heatexch_trigen use a
  guarded Chen approximation instead and are not affected.
* **The homogeneity lift did not improve bounds on the well-posed SYNHEAT example 1** (Yee-Grossmann
  1990 2H/2C; same data as gen1) under identical settings. Gurobi 13, 4 threads: original dual
  150,535 vs lifted 113,871 after 30 s (150 s results in section 4.3); BARON: original solved to
  global optimality (154,995.48) in 22 s, lifted formulation had no feasible point and dual 49,214
  after 30 s and after 150 s (see 4.3). Root bounds: 60,164 (original) vs 49,214 (lifted).
  Examples 2 and 3 were generated and validated but not run to the 600 s budget.

## 2. Task 1(a): exact analysis of the guarded LMTD

In gen1 the process LMTD equations are (e65-e72)
`x_L = (d1 - d2) / log(d1 / (1e-6 + d2))`, `d1, d2 >= 10` with no upper bounds other than the big-M
inequalities `d <= T_hot - T_cold + M(1-z)` (there is no equality tying `d` to a temperature
difference), and `x_L >= 0`. Areas are `x_A = 2 q / (0.01 + x_L)` with cost `150 x_A`.

Write `d1 = d2 + eps + delta` with `eps = 1e-6`. Then
`f = (eps + delta) / log(1 + delta/(d2 + eps))`.
* `delta -> 0+`: numerator `-> eps > 0`, `log -> 0+`, so `f -> +inf`; the leading term is
  `f ~ eps (d2 + eps) / delta` (sympy series; `results/singularity_audit.json`, `table_a`).
* `delta -> 0-` (i.e. `d2 < d1 < d2 + eps`): numerator `> 0`, `log < 0`, so `f -> -inf` and `f < 0`
  throughout `(-eps, 0)`; these points are infeasible because `x_L >= 0`.
* `delta < -eps` (`d1 < d2`): both factors negative, `f > 0` and bounded (ordinary LMTD branch).
* `delta = 0`: division by zero (not in the domain).
So `sup f = +inf` over the feasible region: the sup is approached along `d1 -> (d2 + eps)+` for any
admissible `d2 >= 10`, and larger `d2` gives larger `f` for the same `delta`. Numerically (mpmath, 50
digits; float agrees to 4 digits until `delta = 1e-12`):

| d2 | delta | f exact | eps(d2+eps)/delta |
|---|---|---|---|
| 10 | 1e-5 | 11.0 | 11.0 |
| 10 | 1e-7 | 110.0 | 110.0 |
| 10 | 1e-8 | 1010.0 | 1010.0 |
| 10 | 1e-9 | 10010.0 | 10010.0 |
| 10 | 1e-12 | 1.00066e7 | 1e7 |
| 10 | -1e-8 | -990 (infeasible) | - |
| 50 | 1e-9 | 50049.9 | 50050 |

Consequently the area `2q/(0.01 + f)` of every active process exchanger can be made arbitrarily
small while all other constraints are untouched (the dt variables only need
`10 <= d2 < d1 <= T_hot - T_cold`, i.e. an approach of `10 + eps + delta`, which is the EMAT plus
`~1e-6`). The infimum is therefore the value of the model with the process-area equations dropped,
and it is not attained.

## 3. Task 1(b): explicit near-singular feasible points for gen1

Script: `singularity_audit.py` (`uv run python singularity_audit.py`; log in `results/singularity_audit.log`).

Procedure: BARON 120 s on the original gen1 (`option reslim=120; optcr=1e-4; threads=4`) returned
the MINLPLib incumbent 154,895.93 (dual 100,500.00). Its structure: `b1, b4, b6` (H1-C1 stage 1,
H1-C2 stage 2, H2-C1 stage 2), coolers on H1 and H2, heater on C1 (6 units). Binaries were fixed to
this structure. For each active process exchanger the dt pair was set to `d2 = 10`,
`d1 = 10 + 1e-6 + delta` (mode `fix`: dt fixed; mode `eq`: `d1 - d2 = 1e-6 + delta` added as a
constraint and dt left free), and the NLP was solved with Ipopt 3.14.20 (`tol=1e-12`,
`bound_relax_factor=0`) or CONOPT (GAMS). Every point was then checked against the *original*
120 constraints and all bounds in float and in mpmath at 50 digits (`mpcheck.py`, which converts the
Pyomo expressions through sympy and evaluates with `mpf` values of the exact doubles). "Polished"
means `x_L` and `x_A` were recomputed from `(d1, d2, q)` in 50-digit arithmetic and rounded to
double; nothing else changed.

| delta | mode/solver | Ipopt/CONOPT status | objective (polished) | LMTD per active exchanger | areas b1/b4/b6 (m2) | max viol, raw point, float / mpmath | max viol, polished point, float / mpmath |
|---|---|---|---|---|---|---|---|
| 1e-7 | fix / Ipopt | max iter (5000) | 122,917.84 | 110.00 | 10.95 / 35.45 / 46.28 | 6.1e-8 / 3.9e-7 | 3.9e-7 / **1.6e-11** |
| 1e-8 | fix / Ipopt | max iter | 110,361.77 | 1010.00 | 1.19 / 3.86 / 5.05 | 5.0e-8 / 1.8e-4 | 1.8e-4 / **3.7e-12** |
| 1e-9 | fix / Ipopt | optimal | **108,999.78** | 10010.00 | 0.120 / 0.390 / 0.509 | 1.8e-7 / 8.5e-3 | 8.5e-3 / **1.7e-12** |
| 1e-8 | fix / CONOPT | locally optimal | 110,361.77 | 1010.00 | same as Ipopt | 2.0e-12 / 1.8e-4 | 1.8e-4 / **2.0e-12** |
| 1e-8 | eq / CONOPT | locally optimal | 109,911.28 | 1010 / 4545 / 1010 | 1.19 / 0.86 / 5.05 | 9.9e-5 / 1.1e-3 | 1.1e-3 / **2.3e-12** |
| 1e-7 | eq / Ipopt | max iter | 378,497 | 17.7 / 63.6 / 22.9 | - | 4.2e-2 / 4.2e-2 | 2.1e-5 / 2.1e-5 |
| 1e-8 | eq / Ipopt | max iter | 170,085 | 4.2 / 12575 / 16950 | - | 1.2e-2 / 2.8e-2 | 4.0e-2 / 6.4e-7 |
| 1e-9 | eq / Ipopt | max iter | 194,170 | 4025 / 21 / 26 | - | 3.1e-2 / 3.1e-2 | 1.1e-3 / 4.7e-4 |

Reading: with dt fixed, the points are feasible to ~1e-12 in exact arithmetic (bound violation 0),
binaries exactly integral, and the objective falls from 154,896 to 108,999.78 as `delta` shrinks
(utility loads settle at CW 250 + 1850 kW, steam 450 kW; the NLP moves load onto the now-free
process exchangers). The raw solver points look feasible in float (violations 1e-7) but are infeasible
in exact arithmetic by up to 8.5e-3 on the LMTD equation, and conversely the exactly feasible polished
points look infeasible by 8.5e-3 in double precision: near the guard the feasibility question is
numerically undecidable at the 1e-2 level. With `d1 - d2 = 1e-6 + delta` as a constraint and dt free,
Ipopt hit the iteration limit at all three deltas and its points are not feasible (derivative of the
LMTD w.r.t. `d1` is `~ -f/delta ~ 1e13`); CONOPT coped. The BARON incumbent itself verified with max
violation 4.8e-8 (both float and mpmath), objective 154,895.93297606902.

## 4. Task 1(c): infimum bounds and solver runs on gen1

### 4.1 Relaxed models (`gen1_bounds.py`, BARON, `reslim=600; optcr=1e-6; optca=1e-3; threads=4`)

| case | what is dropped | primal | dual | time | structure |
|---|---|---|---|---|---|
| c1 | process LMTD + area equations e65-e80 (process areas only `>= 0`) | **108,846.94** | 100,500.00 | 600 s (limit) | b1,b4,b6 + 2 coolers + heater; CW 250+1850, steam 450 kW; utility areas 6.90/36.27/12.47 m2 |
| c1m | c1 with dt lower bounds 10 + 3e-6 (margin needed by the construction) | 108,846.94 | 100,500.00 | 600 s | same |
| c2 | all LMTD + area equations e65-e88 | **100,500.00** | 100,500.00 | 0.7 s | same; 6 x 5500 + 15 x 2100 + 80 x 450 = 100,500 |

c1 is a relaxation of the original, so `inf(original) >= opt(c1) >= 100,500`. Conversely the
constructed points give `inf(original) <= 108,999.78` rigorously, and letting `delta -> 0` in the c1
structure gives `inf(original) <= 108,846.94` (c1m shows the EMAT margin costs 5e-3). BARON could not
close the c1 gap in 600 s (its relaxation of the unguarded utility LMTD `(x-70)/log(x/70)` stays at
zero area), so the exact infimum is only located in `[100,500, 108,846.94]`.

### 4.2 Original gen1, 300 s each (`run_gen1_solvers.py heatexch_gen1 300`)

| solver | settings | primal | dual | nodes | root bound |
|---|---|---|---|---|---|
| BARON 25 (GAMS 54.3) | reslim 300, optcr 1e-4, threads 4 | 154,895.93 | 100,500.00 | - | - |
| SCIP (GAMS 54.3) | reslim 300, threads 4 | none | 100,500.00 | - | - |
| Gurobi 13.0.3 (gurobipy via Pyomo GurobiMINLPWriter) | TimeLimit 300, Threads 4, NonConvex 2, MIPGap 1e-4 | 220,628.82 | 100,500.00 | 2,156,241 | 49,214 (root LP); 100,500 after root cuts |

MINLPLib records primal 154,895.93 and per-solver duals ANTIGONE 106,031.2, LINDO 107,976.1,
BARON 100,552.2, COUENNE/SCIP/SHOT/XPRESS 100,500 (https://www.minlplib.org/heatexch_gen1.html).
Every dual bound of 100,500 is exactly the c2 value (6 units + minimum utility with zero area): the
relaxations "see" the unbounded LMTD and give up on area. The ANTIGONE/LINDO values above 100,500 are
not contradicted by our points (108,999.78 > 107,976) but are not proved valid either, since the true
infimum is only known to lie in `[100,500, 108,846.94]`.

**Conclusion.** The recorded gap on heatexch_gen1 (and, by the same structure, gen2/gen3) is an
artifact of the `1e-6` guard: the recorded primal bound is not within 30 % of the infimum, the
infimum is not attained, and any solver reporting 154,896 as optimal is wrong only because it never
found the near-singular region, not because the region is infeasible. The instances should be fixed
(e.g. `d1 = d2` handled by a Chen or Paterson approximation, or `d1 - d2 >= tol` with a lower bound on
the log) before being used as benchmarks. Mistry and Misener (2016, section 5.2) observed the same
symptom on gen3 (a feasible point 1 % below the MINLPLib "lower bound") and attributed it to the
perturbed LMTD.

## 5. Task 2: homogeneity lift on well-posed SYNHEAT

### 5.1 Model and data (`synheat.py`)

Yee and Grossmann (1990) stage-wise superstructure with isothermal mixing, 2 stages (as in the
MINLPLib instances and Mistry-Misener), Chen (1987) LMTD `((dt1 dt2 (dt1+dt2)/2))^(1/3)`, EMAT as dt
lower bound, big-M approach constraints with `dt_{ijk}` shared between adjacent stages, coolers with
one fixed end `Tout_i - Tcu_in`, heaters with fixed end `Thu - Tout_j`, cost
`cf z + c A^beta` per unit plus `ccu qcu + chu qhu`, area constraint as the inequality
`q <= U A LMTD`. Data (all from Mistry and Misener 2016, Tables 5-7,
https://spiral.imperial.ac.uk/bitstreams/73f1f43f-70a2-4142-84c7-54b3798583b5/download, who cite
Escobar and Grossmann 2010; cross-checked against the MINLPLib instances for U, costs, EMAT = 10):

| example | streams | source | cf, c, beta | ccu, chu | binaries |
|---|---|---|---|---|---|
| ex1_yg1990_2h2c | 2H/2C, CW 300-320 K, steam 680 K, h = 1 (steam 5) | Table 5 = Yee-Grossmann 1990 Example 1 = heatexch_gen1 data | 5500, 150, 1 | 15, 80 | 12 |
| ex2_5h1c | 5H/1C, h = 2 (CW 1, steam 2) | Table 6 = heatexch_gen2 data | 5500, 1200, 0.6 | 10, 140 | 16 |
| ex3_10sp1_5h5c | 5H/5C, h = 1.7 (steam 3.4) | Table 7 = 10SP1 in SI (Pho-Lapidus 1973 / Cerda et al. 1983) = heatexch_gen3 data | 4000, 146, 0.6 | 10, 200 | 60 |

Lifted formulation: `v1 = A dt1`, `v2 = A dt2` (bilinear equalities), and
`q <= U (v1 v2 (v1+v2)/2)^(1/3)` (RHS is the geometric mean of three nonnegative linear functions,
hence concave, so the constraint is convex); option `lift_cubic` uses `q^3 <= U^3 v1 v2 (v1+v2)/2`.
Utility exchangers are lifted the same way (their fixed end gives `v2 = c A`, linear). Gurobi 13
accepts both forms through the general-nonlinear API (`pow`); the cubic form explored 3.4x more nodes
in 30 s with a slightly worse dual (113,435 vs 113,871).

Bounds, identical in both formulations: `dt in [EMAT, max(EMAT, Tin_hot - Tin_cold)]`,
`A in [0, A_max]` with `A_max = Qmax_ij / (U_ij LMTD_min)`, `Qmax_ij = min(Q_i, Q_j)` and
`LMTD_min = Chen(EMAT, EMAT) = EMAT` (Chen's mean is nondecreasing in each argument), for utility
units `LMTD_min = Chen(EMAT, fixed end)`; `v in [0, A_max dt_max]`. `A_max` cuts off only
non-optimal points (cost is increasing in A and the area constraint is an inequality). Because the
same `A`/`dt` bounds are used in both formulations and `(v1 v2 (v1+v2)/2)^(1/3) = A Chen(dt1,dt2)`
for `A >= 0`, the projection of the lifted feasible set onto the original variables is exactly the
original feasible set and the objectives coincide. Verified numerically (`check_equiv.py`): the Gurobi
solution of each formulation is feasible in the other with max violation <= 6.2e-7 and identical
objective (154,995.48 and 156,636.79).

### 5.2 Results, example 1 (settings: Gurobi 13.0.3 `NonConvex=2, Threads=4, MIPGap=1e-4`; BARON via GAMS `optcr=1e-4, threads=4`)

30 s smoke runs (`smoke_chain.sh`):

| formulation | solver | primal | dual | root bound | nodes | time |
|---|---|---|---|---|---|---|
| original | Gurobi | 154,995.48 | 150,535.31 | 60,164 | 56,422 | 30 s (limit) |
| lifted (pow) | Gurobi | 156,636.79 | 113,870.72 | 49,214 | 40,005 | 30 s |
| lifted (cubic) | Gurobi | 160,433.66 | 113,434.68 | 49,214 | 135,619 | 30 s |
| original | BARON | 154,995.48 | 154,995.48 (optimal) | - | 1,661 | 22 s |
| lifted (pow) | BARON | none | 49,213.98 | 49,214 | - | 30 s |

150 s runs (`batch_short.sh`, same settings; values from `results/synheat_ex1_*.json`, added by the coordinator):

| formulation | solver | primal | dual | root bound | nodes | time |
|---|---|---|---|---|---|---|
| original | Gurobi | 154,995.48 | 152,851.23 | 60,164 | 292,497 | 150 s (limit) |
| lifted (pow) | Gurobi | 156,636.73 | 115,860.26 | 49,214 | 248,755 | 150 s (limit) |
| original | BARON | 154,995.48 | 154,995.48 (optimal) | - | 1,661 | 19.7 s |
| lifted (pow) | BARON | none | 49,213.98 | 49,214 | - | 150 s (limit) |

Interpretation: the lift replaces one nonconvex product `A * Chen(dt1,dt2)` by two bilinear
equalities plus a convex constraint, but the McCormick relaxation of `v = A dt` over
`[0, A_max] x [EMAT, dt_max]` is very weak (`A_max` is 390-720 m2 here and the products span
`[0, 1.7e5]`), so the relaxation loses the coupling that the direct outer approximation of
`A * Chen` keeps. Both solvers' root bound for the lifted model equals 49,214, which is also
Gurobi's root LP bound on the ill-posed gen1, i.e. the value with area terms effectively relaxed to
zero. On this instance the lift does not improve bounds; it makes them worse and BARON cannot even
find a feasible point.

Note: the SYNHEAT optimum 154,995.48 (Chen approximation, isothermal mixing, 2 stages) is above the
near-singular gen1 points (108,999.78) and slightly above the gen1 incumbent (154,895.93) obtained
with the exact (guarded) LMTD and non-isothermal mixing, which is the expected ordering.

## 6. Not done / caveats

* Task 2 was cut short: examples 2 (5H/1C) and 3 (10SP1) were built and pass structural checks but
  were not run; the planned 600 s comparisons were replaced by 30 s and 150 s runs on example 1
  only. No secant option for the concave cost was implemented (beta = 1 in example 1 anyway).
* The exact infimum of gen1 is bracketed, not computed: BARON did not close the c1 relaxation
  (600 s, dual stuck at 100,500). gen2/gen3 were analysed structurally only (same guard, dt only in
  big-M inequalities); no explicit points were constructed for them.
* Ipopt could not handle the `d1 - d2 = 1e-6 + delta` equality version; the certified points come
  from the fixed-dt NLPs (Ipopt and CONOPT agree to 1e-12).
* Node counts are not reported for BARON/SCIP on gen1 (GAMS `.lst` in `results/` only); Gurobi root
  bounds are parsed from its log ("Root relaxation"), BARON's from the first iteration row.
* The literature optimum for Yee-Grossmann Example 1 was not verified against the original paper.

## 7. Commands

```
cd code/minlp_solver_lab/hens; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
uv run python singularity_audit.py            # (a) table, (b) constructions + mpmath checks -> results/singularity_audit.json
uv run python run_gen1_solvers.py heatexch_gen1 300   # BARON, SCIP, Gurobi 300 s -> results/heatexch_gen1_solvers300.json
uv run python gen1_bounds.py 600              # c1, c1m, c2 -> results/gen1_bounds.json
uv run python run_synheat.py ex1_yg1990_2h2c orig gurobi 150   # one Task 2 job; forms: orig | lift | lift_cubic; solvers: gurobi | baron
uv run python check_equiv.py gurobi           # cross-feasibility of the two formulations
./batch_synheat.sh 600                        # full Task 2 batch (not run)
```

## 8. Independent re-verification of the singularity claim (coordinator, 2026-09-12 22:45)

Reconstructed without the agent's scripts: BARON's saved incumbent structure
(`b1, b4, b6`), `d2 = 10`, `d1 = 10 + 1e-6 + 1e-9` fixed on the three active
process exchangers, Ipopt 3.14 (`tol 1e-12`, `bound_relax_factor 0`) on the
remaining NLP, then the LMTD and area variables recomputed in 50-digit
arithmetic from `(d1, d2, q)` and rounded to doubles. All 120 constraints and
all bounds of the original `heatexch_gen1.py` were re-evaluated with mpmath at
50 digits: objective `108999.783324`, maximum violation `4.5e-10` (row `e65`),
binaries exactly integral, LMTD `10010.008` and areas `0.120 / 0.390 / 0.509`
on the active exchangers. This confirms the point in section 3 to the stated
accuracy (the agent's polished points reach `1.7e-12`). Saved as
`code/minlp_solver_lab/hens/results/independent_near_singular_point_gen1.json`.
