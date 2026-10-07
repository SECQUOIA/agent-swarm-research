# waterno2_09–24: independent recheck of every period bound

Date: 2026-09-30. Verifier: independent reviewer. I did not produce the
results or the first verification.

Claims checked: the per-period bounds B_t and the certified duals of
waterno2_09, _12, _18 and _24 in `open-instances-wave2/waterno2/report.md`
(files `logs/cert_TT_w1_impl.json`, multipliers `logs/mult_TT_w1_impl.json`).

Code and logs are in `reviews/waterno2-recheck/`. Nothing under
`open-instances-wave2/waterno2/` or `reviews/waterno2-verification/` was
edited. The authors' code was only imported read-only, for one objective
comparison (Section 3), with `PYTHONDONTWRITEBYTECODE=1`.

## Summary

**All 63 period bounds of waterno2_09, _12, _18 and _24 are certified.** My
branch and bound is not the authors' `rbb.py`. At the authors' multipliers, it
proved φ_t ≥ B_t for every period, where B_t is the authors' exact stored
per-period value.

- No period timed out, and there is no discrepancy.
- The per-period limit was 2400 s. The longest run took 2154 s (waterno2_24,
  period 14).
- 61 of these periods had not been rechecked before.
- The first verifier had already certified waterno2_09 period 6 and
  waterno2_24 period 19. Both were certified again here.

The exact sums μ·rhs + Σ_t B_t, recomputed from the certified values, equal
the authors' stored exact values bit for bit:

| instance | periods certified | timed out | certified dual (rounded down, 9 dp) | equals authors' exact value | vbb2 nodes (total) | B&B time, total / longest period |
|---|---|---|---|---|---|---|
| waterno2_09 | 9 / 9 | 0 | **824.834692454** | yes | 128,103 | 2,635 s / 665 s |
| waterno2_12 | 12 / 12 | 0 | **2089.754565439** | yes | 176,530 | 3,658 s / 672 s |
| waterno2_18 | 18 / 18 | 0 | **4790.820715376** | yes | 455,806 | 9,866 s / 2,084 s |
| waterno2_24 | 24 / 24 | 0 | **6576.151388415** | yes | 644,776 | 14,357 s / 2,154 s |

The first verification already covered all six periods of waterno2_06. So
every period bound behind the five reported certified duals (06, 09, 12, 18,
24) has now been certified by code that is not `rbb.py`.

**Limit on independence.** My code is independent of the authors' code, not
of the first verifier's. It reuses the first verifier's model reader and
builder and its relaxation and node-bound code; only bound propagation is new
(Section 1). An error in the shared parts would affect both verifications.

## 1. Method

### 1.1 What is certified

For each size T, the claim is optimum ≥ μ·rhs + Σ_t B_t. The multipliers are
the stored floats λ, μ ≥ 0, and B_t is the authors' certified value for
period t. Weak duality of the period Lagrangian was confirmed by the first
verifier (`reviews/waterno2-verification/verification-report.md`, Section 2).
What remains is a rigorous proof of B_t ≤ φ_t for each period, where φ_t is
the minimum of period t's Lagrangian subproblem. Each run below uses target
= B_t. "Certified" means the branch and bound closed every node with an exact
bound ≥ B_t, or proved the node empty.

### 1.2 Branch and bound (`vbb2.py`)

`vbb2.py` is the first verifier's exact-rational B&B (`vbb.py`) with one
change: bound propagation (FBBT).

- **Why the change.** A profile of `vbb.py` on waterno2_09 period 8 showed
  92% of the run time in Fraction-based propagation (`prof_vbb.py`). Its rate
  (about 66 ms per node) would have pushed the heavy periods of 18 and 24 past
  a 40-minute limit.
- **What changed.** Propagation now uses float interval arithmetic with
  explicit outward rounding. The rate is about 18–22 ms per node.
- **Unchanged, taken from `vbb.py`:**
  - the relaxation rows, with exact rational coefficients (tangents,
    secants, McCormick);
  - the node bound, evaluated exactly in `Fraction`: min over the box of
    (c + Aᵀy)·z − y·b, for any dual vector y, with y ≥ 0 enforced on ≤ rows;
  - root OBBT with exactly evaluated bounds;
  - branching, best-first node selection and pruning.
- **Role of HiGHS.** HiGHS (through scipy) supplies only the dual vector y.
- **Pruning rule.** A node is discarded only if its exact bound is ≥ target,
  or propagation proves it empty. The result is
  φ_t ≥ min(target, bounds of open nodes and unbranchable leaves).

I re-read the reused parts of `vbb.py` before relying on them:

- the tangent and secant rows for x² and x³ (x ≥ 0 is asserted for cubes);
- the four McCormick rows;
- the sign handling of y and of infinite bounds in `exact_bound`;
- the covering branch split;
- the final bound, taken as the minimum over open nodes and leaves.

I found no error.

**Why the new propagation is rigorous.**

- Each decimal row coefficient a is enclosed as [fdn(a), fup(a)], with the
  same sign as a (asserted). Row sides are replaced by fdn(L) and fup(U).
  `fdn` and `fup` compare against the exact Fraction and step one ulp at a
  time until the enclosure holds.
- Every float product and quotient is widened by one ulp outward
  (`nextafter`). With IEEE round-to-nearest, the exact result lies strictly
  between the two neighbours of the rounded result.
- Row sums use `math.fsum`, widened by two ulps. CPython's `fsum` is correctly
  rounded; the second ulp covers the one-ulp double-rounding case that the
  Python documentation mentions for some platforms.
- The "sum of the other terms" is (sum) − (own term), rounded outward again.
- Square roots use IEEE `sqrt`, which is correctly rounded, widened by one
  ulp. Cube and cube-root propagation stays exact (`Fraction`), as in
  `vbb.py`.
- Bilinear forward and backward steps take the outward-rounded extremes over
  the four corners. Division happens only when the divisor interval excludes 0.
- NaN cannot arise, because all arithmetic operands are finite. Infinite
  bounds are counted separately, as in `vbb.py`.

### 1.3 Implied bounds (`vimplied2.py`)

The authors add implied bounds to the period subproblems. On waterno2_06,
the first verifier showed that periods 1–3 need them. I derived my own bounds
on the full model: all period rows and link rows, with the horizon row left
out, which only weakens the result. There were two steps:

1. outward-rounded FBBT;
2. two rounds of OBBT on all tank-3 link-level variables. Each OBBT bound is
   evaluated exactly from the HiGHS dual vector.

Every tightening of the authors' implied bounds (8 for T = 9, 12 and 18; 10
for T = 24) is reproduced or beaten (`logs/vimplied2_TT.log`). Examples:

- tank 3 at the start of period 1 ≥ 3.3324999992499933 (authors'
  3.332499999218251);
- tank 3 at the start of period 1 ≤ 5.936197237652735 (authors'
  5.936197237746007);
- waterno2_24, tank 3 at the start of period 23 ≥ 2.3042271866761745 (authors'
  2.304227186594236).

All tightened bounds (806 to 2129 variables per instance, stored in
`logs/my_implied_TT.json`) were given to every period run. They hold for every
feasible point of the full problem, so they keep the Lagrangian bound valid.

Effect on the subproblems (`extra_effect.py`): I compared each period's root
FBBT box in two cases:

- my bounds on the authors' 6–8 variables only;
- all of my bounds.

The two boxes differ by at most 8.3e-16 of the interval width in every period
of every size. So the extra bounds change nothing material. The subproblems
certified here are the authors' subproblems, except that my bounds on their
6–8 level variables are tighter by up to about 1e-10.

Strictly, then, I proved B_t ≤ φ′_t, where φ′_t uses my implied bounds.
Because those bounds are valid, this is enough for the final dual bound. I
did not separately certify B_t against the authors' slightly looser bounds.

### 1.4 Runs

- Each period was run by `run_period.py T t 2400 logs/my_implied_TT.json`.
- `run_period.py` asserts that the multipliers in `mult_TT_w1_impl.json`
  equal the float reprs stored in the certificate file, that μ ≥ 0, and that
  the authors' period entry is `certified`.
- `run_all.sh` ran the 61 periods not yet timed, 6 processes at a time, with
  `OMP_NUM_THREADS=1`. Periods with the largest authors' node counts ran
  first.
- The batch took about 85 min of wall time (08:04–09:30).
- waterno2_09 periods 6 and 8 were run first as timing tests, then rerun with
  logs. Both runs of each gave identical node counts.

## 2. Per-period results

"Time" is vbb2's B&B time, excluding the few seconds of model setup. The
authors' rbb node counts are listed for scale. vbb2 has no reduced-cost
tightening and needs about 1.2 times as many nodes overall (1,405,215 against
1,155,779).

**waterno2_09**

| period | authors' B_t | vbb2 | nodes | time (s) | authors' rbb nodes |
|---|---|---|---|---|---|
| 0 | 1032.6492748313672 | certified | 5345 | 109 | 5561 |
| 1 | -70.76341370615185 | certified | 16363 | 331 | 13679 |
| 2 | -80.80022719893006 | certified | 26809 | 547 | 23681 |
| 3 | -85.682051627878 | certified | 29477 | 665 | 25051 |
| 4 | -104.08311829430082 | certified | 19493 | 388 | 14965 |
| 5 | -112.11839520357162 | certified | 18165 | 358 | 15273 |
| 6 | -759.9355220257974 | certified | 2397 | 44 | 1747 |
| 7 | -121.97794465562745 | certified | 6521 | 125 | 5303 |
| 8 | -476.0964217318226 | certified | 3533 | 67 | 3259 |

**waterno2_12**

| period | authors' B_t | vbb2 | nodes | time (s) | authors' rbb nodes |
|---|---|---|---|---|---|
| 0 | 2078.157299476928 | certified | 5337 | 107 | 5545 |
| 1 | -146.90889830896742 | certified | 16349 | 324 | 13593 |
| 2 | -154.1326349860017 | certified | 27279 | 573 | 23999 |
| 3 | -157.29333795296807 | certified | 29329 | 672 | 24917 |
| 4 | -180.34639403743066 | certified | 19407 | 400 | 14897 |
| 5 | -193.33149426608466 | certified | 21611 | 439 | 16469 |
| 6 | -1533.4292535137579 | certified | 6103 | 114 | 3787 |
| 7 | -199.9341821368137 | certified | 15817 | 317 | 12549 |
| 8 | -609.0209427044781 | certified | 18961 | 387 | 10223 |
| 9 | 59.77722073916513 | certified | 6235 | 122 | 5489 |
| 10 | 9.563819128712542 | certified | 6773 | 142 | 6235 |
| 11 | -778.6021172926055 | certified | 3329 | 62 | 3249 |

**waterno2_18**

| period | authors' B_t | vbb2 | nodes | time (s) | authors' rbb nodes |
|---|---|---|---|---|---|
| 0 | 2364.6754526192926 | certified | 5343 | 115 | 5591 |
| 1 | -167.636025419696 | certified | 16579 | 339 | 13749 |
| 2 | -174.17139646704283 | certified | 26871 | 545 | 23765 |
| 3 | -176.86058720221777 | certified | 28947 | 620 | 24671 |
| 4 | -199.74093177969692 | certified | 19747 | 397 | 15157 |
| 5 | -213.68762115216035 | certified | 22385 | 448 | 16729 |
| 6 | -1579.2474851809566 | certified | 6087 | 115 | 3773 |
| 7 | -239.16865952038214 | certified | 16417 | 328 | 13001 |
| 8 | -679.565029935841 | certified | 15765 | 336 | 8803 |
| 9 | -2.8082761213559277 | certified | 6207 | 118 | 5405 |
| 10 | 21.02678346423247 | certified | 9687 | 194 | 8965 |
| 11 | 36.702908226581684 | certified | 9943 | 197 | 9149 |
| 12 | 4.36770464163553 | certified | 12033 | 234 | 11485 |
| 13 | 71.13893822969268 | certified | 11433 | 228 | 9335 |
| 14 | -160.07591532674817 | certified | 89431 | 2039 | 75973 |
| 15 | -165.3957208229065 | certified | 90981 | 2084 | 76821 |
| 16 | -185.06224840752637 | certified | 61631 | 1407 | 53729 |
| 17 | -960.688648494385 | certified | 6319 | 121 | 4983 |

**waterno2_24**

| period | authors' B_t | vbb2 | nodes | time (s) | authors' rbb nodes |
|---|---|---|---|---|---|
| 0 | -20.12822981641362 | certified | 5367 | 112 | 5597 |
| 1 | 5.83046366957419 | certified | 16219 | 332 | 13601 |
| 2 | -6.9990820616555105 | certified | 27003 | 564 | 23789 |
| 3 | -13.619191730486104 | certified | 29659 | 673 | 25213 |
| 4 | -28.41729881984659 | certified | 19277 | 400 | 14827 |
| 5 | -33.33642387598448 | certified | 19513 | 393 | 15569 |
| 6 | -1224.3340328676031 | certified | 6155 | 116 | 3803 |
| 7 | 142.41570823464255 | certified | 16541 | 329 | 13157 |
| 8 | -229.59617632094958 | certified | 14171 | 307 | 7835 |
| 9 | 403.6719378897309 | certified | 6335 | 132 | 5767 |
| 10 | 383.9424819150157 | certified | 7719 | 163 | 7117 |
| 11 | 430.07235060240237 | certified | 8817 | 184 | 8353 |
| 12 | 337.43643719838406 | certified | 8937 | 185 | 8481 |
| 13 | 429.483515864795 | certified | 9173 | 190 | 8199 |
| 14 | 253.0565166272879 | certified | 95023 | 2154 | 83527 |
| 15 | 245.10970768938293 | certified | 73797 | 1636 | 64801 |
| 16 | 230.29848848567596 | certified | 55791 | 1283 | 48063 |
| 17 | 395.4734585503302 | certified | 10001 | 203 | 9227 |
| 18 | 492.61565403490795 | certified | 14637 | 288 | 12717 |
| 19 | 795.585216392664 | certified | 5639 | 107 | 4363 |
| 20 | 311.27805929947976 | certified | 39269 | 915 | 34231 |
| 21 | 532.1378095366374 | certified | 8349 | 170 | 6023 |
| 22 | -55.54550940616585 | certified | 82465 | 1916 | 65399 |
| 23 | 612.408863398666 | certified | 64919 | 1601 | 35565 |

**Exact sums** (`vsum2.py`, `logs/vsum2.log`). The horizon rhs is the exact
decimal of the horizon row, and μ is the exact stored float. Each sum is
formed in `Fraction`:

- 09: 3627661341387654598825371 / 4398046511104000000000 = 824.834692454636…
- 12: 9190837775594918144252281 / 4398046511104000000000 = 2089.754565439516…
- 18: 5267563083146225483626937 / 1099511627776000000000 = 4790.820715376162…
- 24: 115688878681251187594323079 / 17592186044416000000000 = 6576.151388415564…

Each equals the authors' `certified_bound_exact`, and each rounds down to the
value in the report.

## 3. Checks of the verifier code

All checks are targeted; no project-wide checks were run.

1. **Propagation against exact propagation** (`test_fbbt.py`,
   `logs/test_fbbt.log`).
   - Setup: 1500 random sub-boxes of waterno2_09 periods 0 and 3,
     waterno2_18 period 15, and waterno2_24 periods 22 and 23. From each box,
     one pass of row propagation and one pass of monomial propagation were
     run both in vbb2 (float) and in `vbb.py` (exact).
   - Required: the float box contains the exact box, and a float "empty"
     result implies an exact "empty" result.
   - Outcome: 0 violations in 3000 pass comparisons (1944 with both boxes
     non-empty, 1036 with both empty, and 20 where only the exact pass proved
     emptiness).
   - Result: **PASS**.
2. **Exactly feasible points** (same log). The first verifier built exactly
   feasible rational points for waterno2_06 periods 0, 4 and 5. For 300
   random sub-boxes around each point, full FBBT never removed the point and
   never declared the box empty.
3. **Negative control on an exactly feasible point** (`control.py`,
   `logs/control.log`).
   - Setup: waterno2_06 period 0 at the SCIP-reproduction multipliers. The
     point was re-checked exactly (maximum violation 0) and has value
     v = 168.10865202980798.
   - With target v + 0.05, vbb2 did **not** certify. It ended with bound
     v − 1.8e-13.
   - With target v − 1e-3, it certified.
4. **Negative controls on in-scope periods** (`control_upper.py`,
   `scip_point.py`). The target was the authors' SCIP estimate + 0.05. In both
   periods vbb2 did not certify, and in both the rigorous bound it reached lies
   below the value of a point feasible to about 1e-11:

   | period | authors' SCIP estimate (feastol 1e-6) | vbb2 bound at stop | SCIP point at feastol 1e-11: exact value (max row violation) |
   |---|---|---|---|
   | 09 p8 | −476.0963217 | −476.0959957892 (tree exhausted, 104 s) | −476.0959955868 (6.6e-12) |
   | 24 p19 | 795.5853164 | 795.5894964855 (600 s limit) | 795.5894969196 (2.8e-12) |

   The bounds lie 2.0e-7 and 4.3e-7 below these points. Both bounds lie
   *above* the authors' feastol-1e-6 estimates. For 24 p19, a solve at
   feastol 1e-9 gave 795.5894957 (violation 6.5e-10). That is 8e-7 below my
   bound, so I also solved at 1e-10 and 1e-11. Both gave 795.5894969, above
   my bound.

   The values rise as the tolerance tightens (1e-6: 795.586899; 1e-9:
   795.5894957; 1e-11: 795.5894969). SCIP's loose-tolerance points exploit
   row violations of about 1e-6, and here that is worth up to about 4e-3 in
   objective. This is more than the "about 1e-3" stated in the authors'
   report. It affects only how conservative their targets are, not validity.
5. **Objective.** For every period of T = 9, 12 and 18, the objective used by
   vbb2 (`vmodel.period_objective`) equals the authors'
   `rbb.Window.objective` coefficient for coefficient, compared by variable
   name (`compare_obj.py`, `logs/compare_obj.log`). The first verifier checked
   T = 6 and 24.
6. **Regression.** waterno2_09 period 6 and waterno2_24 period 19 are
   certified by both `vbb.py` (first verifier) and vbb2.

## 4. What the certificate rests on, and what was not checked

The certificate rests on:

1. **Correctness of the verifier code.**
   - `osilx.py`, the OSIL reader written by the first-wave verifier;
   - `vstruct.py` and `vmodel.py`, the period structure and Lagrangian
     objective, written by the first waterno2 verifier;
   - `vbb.py`'s relaxation, exact node bound and search, reviewed by the
     first verifier and re-read by me;
   - my new propagation in `vbb2.py`.

   The new propagation was tested (Section 3) but not formally proved. The
   code was not reviewed by a third party.
2. **IEEE-754 double arithmetic in CPython.** This means round-to-nearest for
   ×, ÷ and −, correctly rounded `sqrt`, `nextafter`, and `fsum` accurate to
   within the 2-ulp margin. `float(Fraction)` conversions are checked exactly
   inside `fdn` and `fup`.
3. **Validity of the implied bounds** in `logs/my_implied_TT.json`. They were
   produced by the same propagation code and by OBBT with exactly evaluated
   bounds.

HiGHS and SCIP supply only dual vectors and test points. A wrong hint can
weaken the bound or slow the search, but cannot make a certificate invalid.

Not checked here:

- the primal points and gaps (the first verifier confirmed them);
- the multiplier optimization (it does not affect validity);
- the small instances waterno2_02–04;
- the authors' runtimes.

## 5. Files (`reviews/waterno2-recheck/`)

Code:

- `vbb2.py`: the B&B used here (subclass of `../waterno2-verification/vbb.py`
  with outward-rounded float propagation).
- `vimplied2.py`: implied bounds on the full model.
- `run_period.py`: one period at the authors' multipliers and target.
- `run_all.sh`, `jobs.txt`: the parallel batch.
- `vsum2.py`: exact sums.

Checks:

- `test_fbbt.py`, `control.py`, `control_upper.py`, `scip_point.py`,
  `compare_obj.py`, `extra_effect.py`;
- `prof_vbb.py`: the profile of `vbb.py` that motivated the change.

Logs (`logs/`):

- `rb_TT_pNN.{log,json}`: one per period, 63 in total;
- `vimplied2_TT.log`, `my_implied_TT.json`;
- `vsum2.log`, `run_all.log`;
- `test_fbbt.log`, `control.log`, `control_upper_*.log`, `scip_point_*.log`,
  `compare_obj.log`, `extra_effect.log`.

## 6. Commands run

All commands were run from `reviews/waterno2-recheck/` with
`OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1`. They are targeted checks only.
No project-wide checks were run and no CI was consulted.

```
python3 prof_vbb.py 9 8 90                                  # profile of vbb.py (not logged)
python3 test_fbbt.py 300                                    # logs/test_fbbt.log
python3 vimplied2.py {9,12,18,24} 2                         # logs/vimplied2_TT.log, logs/my_implied_TT.json
python3 run_period.py 9 {6,8} 2400 logs/my_implied_09.json  # timing runs, then rerun with logs
./run_all.sh jobs.txt                                       # 61 periods, 6 at a time, limit 2400 s
python3 compare_obj.py 9 12 18                              # logs/compare_obj.log
python3 control.py 600                                      # logs/control.log
python3 vsum2.py 9 12 18 24                                 # logs/vsum2.log
python3 extra_effect.py 9 12 18 24                          # logs/extra_effect.log
python3 control_upper.py {9 8,24 19} 0.05 600               # logs/control_upper_*.log
python3 scip_point.py 24 19 300 {1e-6,1e-9,1e-10,1e-11}     # logs/scip_point_24_p19_*.log
python3 scip_point.py 9 8 300 {1e-10,1e-11}                 # logs/scip_point_09_p08_*.log
```
