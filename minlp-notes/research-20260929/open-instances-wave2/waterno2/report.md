# waterno2: certified period-decomposition dual bounds

Date: 2026-09-30. Status: computational results, independently verified;
every period bound was rechecked
([`../../reviews/waterno2-recheck.md`](../../reviews/waterno2-recheck.md);
its branch and bound shares code with the first verifier's, not with the
authors').
*Follow-up (root, 2026-09-30 and 2026-10-01):* branching on the tank-level separators later
raised the waterno2_06 bound from 263.735099441 to 272.584700834 (gap
3.78%); see [`separator-branching.md`](separator-branching.md) and its
independent review. Cell-dependent slopes then raised it to 278.230573774
(gap 1.67%; independently verified); see [`cell-slopes.md`](cell-slopes.md). The other instances are unchanged.
All code, logs and downloaded MINLPLib files are in this directory (file list
in Section 10). Runs were single-threaded processes on a shared 36-core
machine; wall times are indicative only.

## 1. Summary

**Result.** Every waterno2 instance from 06 to 24 now has a rigorous dual
bound far above the best listed one. The bound is a Lagrangian relaxation of
the 3(T−1) tank-level links and the single horizon row. Each single-period
subproblem is bounded by our own rigorous branch and bound (`rbb.py`), not by
SCIP. The bound is valid for the exact problem (exact decimal data, exact
feasibility, exact integrality).

"Gap" is MINLPLib's relative gap |p − d| / min(|p|, |d|). "Before" uses the
listed primal and the best listed dual. "After" uses the best primal known to
us and our certified dual.

| instance | listed primal | best listed dual (solver) | gap before | certified dual (ours) | best primal (ours or listed) | gap after | certification: max / total period time, nodes |
|---|---|---|---|---|---|---|---|
| waterno2_06 | 282.8880 | 165.1903 (SCIP) | 71.2% | **263.735099** | 282.8880 (listed) | 7.26% | 151 s / 550 s, 29196 |
| waterno2_09 | 922.5953 | 273.8958 (SCIP) | 236.8% | **824.834692** | 914.0120 (ours) | 10.81% | 507 s / 2384 s, 108519 |
| waterno2_12 | 2263.3584 | 479.5051 (GUROBI) | 372.0% | **2089.754565** | 2233.8213 (ours) | 6.89% | 488 s / 3103 s, 140952 |
| waterno2_18 | 5269.6388 | 770.7362 (SCIP) | 583.7% | **4790.820715** | 5023.9827 (ours) | 4.87% | 1280 s / 7509 s, 381084 |
| waterno2_24 | 7332.7217 | 1095.1265 (SCIP) | 569.6% | **6576.151388** | 6963.7952 (ours) | 5.89% | 1368 s / 10032 s, 525224 |

The certified values are rounded down to 6 decimals; the exact rational
values are in `logs/cert_TT_w1_impl.json`. The last column is the longest
single-period certification and the sum over periods, including the SCIP
target runs.

- For waterno2_06 the certified bound is **263.735099441**. The best listed
  bound is 165.1902989 (SCIP) and the listed primal 282.8880374. The gap
  shrinks from 71.2% to 7.26%.
- The primal side of waterno2_09–24 was also improved by window
  re-optimization (Section 8). The new values are 914.01, 2233.82, 5023.98
  and 6963.80, feasible to at most 4.4e-9 in absolute row violation. For
  waterno2_06 we found no better point than MINLPLib's p4.
- The remaining gap is the duality gap of the period Lagrangian. It was not
  closed. Two-period windows, dynamic programming over level boxes and over
  horizon-row bins, and configuration probing all failed or gave at most
  about +1 (Section 7).
- **SCIP 10.0.2 is not reliable on these subproblems.** On single-period
  subproblems it reports status `optimal` at values up to 2.4 above points
  that are feasible to 1e-9 (Section 5). SCIP was therefore used only to
  suggest multipliers and target values, never as a bound.

Small instances, for scale (MINLPLib optima known):

| instance | optimum | certified period-Lagrangian bound | gap |
|---|---|---|---|
| waterno2_02 | 39.57142193 | 39.314005760 | 0.65% |
| waterno2_03 | 115.0045167 | 74.068040651 | 55.3% |
| waterno2_04 | 145.4397918 | 132.529333260 | 9.74% |

So the period Lagrangian can have a large gap even on tiny instances; its
5–11% gap on waterno2_06–24 is not specific to long horizons.

## 2. Structure (recovered exactly)

`wmodel.py` reads the OSIL file with the independent verifier's reader
(`reviews/open-instances-verification/osilx.py`, decimal strings kept) and
converts each row to a polynomial. The OSIL objective has no `constant`
attribute and no row has one (both asserted). The objective is the sum of 9T
pump-cost variables with coefficient 1 (asserted).

**Period partition** (`wmodel.structure`):

1. Remove the one row that sums one variable per period (the horizon row).
2. Remove every copy row −x_a + x_b = 0 whose two variables both appear in
   tank-balance rows (rows with coefficient ±3600).
3. Union-find on the remaining rows gives exactly T components of 166
   variables. Each component has 9 binaries and 203 rows (206 if the three
   outgoing link rows are counted, as in the first-wave report).
4. Removed rows whose variables lie in one component go back to that period.
   The rest are exactly 3 link rows per period transition.
5. The time order follows the link chain. The first period is the one that
   contains the fixed initial levels.

This holds for all T in {2, 3, 4, 6, 9, 12, 18, 24} (`logs/structure_all.log`).

**waterno2_06 details.**

- Link rows: e111–e125 (for example, e111: −x243 + x244 = 0, the end level of
  tank 1 in period 0 equals its start level in period 1).
- Horizon row: e56, x188 + … + x193 ≥ 1.752499999.
- In the GAMS scalar file every model equation appears as a block of T
  consecutive rows, one per period, in scrambled period order. This
  interleaving is presumably why the first wave's spectral ordering did not
  isolate the periods. Connected components after removing the link
  candidates do.
- In waterno2_06 the periods are identical except for the fixed demand in
  one row. In waterno2_09–24 the periods also differ in the energy-price
  coefficient of the cost rows (−0.3098, −0.1326 or −0.0826), and demands
  roughly double after hour 6.

**Physical reading** (derived from the rows; used only for interpretation):

- Stations and tanks: source → station A (3 identical variable-speed pumps)
  → tank 1 (area 1800) → stations B1 and B2 (2 pumps each) → tank 2 (area
  720) → station D (2 pumps) → tank 3 (area 1600) → demand.
- Level dynamics: E = L + (3600 s / area) × (inflow − outflow).
- Heads come from the start-of-period levels plus quadratic pipe losses.
- Pump head curves are quadratic in (flow, speed); pump power is cubic.
- Identical pumps are ordered by rows b_k ≥ b_{k'}.
- The horizon row requires a minimum total station-A outflow. Its right-hand
  side equals the total demand.

**Implied bounds** (`implied.py`): rigorous FBBT plus OBBT on the full
model. OBBT covers the level variables; for T ≤ 6 it also covers the flow
and speed variables. The tightenings that matter are on tank 3:

- start levels of periods 1, 2, 3 are ≥ 3.3325, 2.67 and 2.03125 (tank 3
  cannot drain faster than the demand);
- for waterno2_24, L3 ≥ 2.304 at the start of period 23.

For waterno2_06, OBBT also lowers some flow upper bounds slightly (for
example, a station-A pump flow ≤ 0.797 instead of 0.8).

They are valid for every feasible point, so they may be added to the period
subproblems. They raise the waterno2_06 bound from 262.702 to 263.735.

## 3. Method

1. **Lagrangian.** Dualize the link rows (multipliers λ, free) and the
   horizon row (μ ≥ 0):
   L(λ, μ) = μ·c + Σ_t φ_t(λ, μ).
   Here φ_t is the minimum over period t's own rows of its cost plus the
   linear Lagrangian terms on its start and end levels and on its horizon
   variable. `rbb.Window.objective` asserts that no variable receives two
   Lagrangian terms, so every objective coefficient is an exact float.
2. **Multipliers** (`bundle.py`).
   - Method: disaggregated trust-region cutting planes, one model per period,
     with the master LP solved by HiGHS.
   - Start: least-squares KKT multipliers at the best MINLPLib point
     (`kkt.py`, residual ≤ 3e-10) for T = 6, 9, 12 and 18. For T = 24 the
     dense KKT solve did not finish in 30 min, so it started from zero, as
     did T = 2, 3, 4.
   - Oracle: SCIP, with propagation off for T ≤ 6 and default settings for
     T ≥ 9 (faster). Because SCIP's "optimal" values can be too high, each
     value is replaced by min(SCIP value, value of every stored incumbent at
     the new multipliers). These corrections are logged as `fixes=` and were
     frequent.
   - Multipliers only need to be good, not optimal. Any float λ and any
     μ ≥ 0 give a valid bound.
3. **Rigorous subproblem bounds** (`rbb.py`, `certify.py`).
   - For each period, the target is the smallest SCIP incumbent value
     (default and no-propagation settings) minus max(1e-4, 1e-7·|value|).
   - `rbb.solve` either proves φ_t ≥ target or returns the smallest rigorous
     bound among its open nodes.
   - Every period of every instance was proved to its target (`status
     certified` in the logs).
4. **Sum.** The certified values and μ·c are added in exact rational
   arithmetic. The result is rounded down to 9 decimals.

## 4. Validity: what the certificate rests on

The claim is: optimum ≥ μ·c + Σ_t B_t, where B_t is rbb's certified lower bound
for period t at the stored multipliers.

**Weak duality.** For every exactly feasible x:

- the link residuals are 0;
- μ(c − Σ h) ≤ 0;
- the period rows hold, including the implied bounds, which are valid for
  every feasible point.

Hence f(x) ≥ μ·c + Σ_t (period-t Lagrangian value of x) ≥ μ·c + Σ_t φ_t.

**rbb soundness.** For each period, rbb computes a number B_t with
B_t ≤ φ_t. It uses these ingredients:

- **Data.** Every decimal constant from the OSIL file is enclosed as
  [down(v), up(v)] (one ulp outward, exact when v is a float). Variable
  bounds are widened outward.
- **Monomials.** Each monomial (x², x³, xy, and b·x with b binary) gets an
  auxiliary variable, so all rows become linear.
- **FBBT.** Forward and backward interval propagation rounds outward with
  `nextafter`. Float sums of n terms get an explicit margin
  1e-12·Σ|terms|. This exceeds the standard bound (n−1)·2⁻⁵³·Σ|terms| for
  n ≤ 9000 in any summation order.
  - Square roots use IEEE `sqrt`, which is correctly rounded.
  - Cube roots are checked by cubing in outward interval arithmetic.
  - Binary bounds are rounded inward only when the proven bound excludes
    the other value.
  - A box is discarded as infeasible only when interval arithmetic proves
    it empty.
- **Relaxation.**
  - Products use McCormick inequalities with exact float box bounds.
  - x² and x³ (x ≥ 0 is asserted for cubes) use tangents and secants.
    Their constants are computed rigorously for the chosen float slope; for
    cubes, the stationary point is enclosed.
- **Bound per node** (Neumaier–Shcherbina). For any dual vector y (with
  y ≥ 0 on ≤ rows), the value min over the box of (c + Aᵀy)·x − yᵀb is a
  valid bound. It is evaluated with interval coefficients and outward
  rounding. HiGHS supplies y; if the LP is infeasible, an elastic LP
  supplies it. HiGHS's optimality is never used.
- **Pruning and branching.**
  - A node is closed only if its rigorous bound is ≥ target, or FBBT proves
    it empty.
  - Reduced-cost tightening and root OBBT use the cutoff c·x < target, so
    they are valid for the statement "φ ≥ min(target, open bounds)".
  - Branching splits boxes into covering halves.

**What the certificate rests on:**

1. The correctness of our code: `wmodel.py`, `period.setup`, `rbb.py`,
   `implied.py` and `certify.py`. It has **not** been independently reviewed.
2. IEEE-754 double semantics in Python/numpy: round-to-nearest, `nextafter`,
   and correctly rounded `sqrt`.
3. The OSIL reader `osilx.py`, written by the first-wave verifier.

SCIP and HiGHS supply only hints: multipliers, targets, LP dual vectors and
branching points. A wrong hint can make the bound weaker, never invalid.

**Tolerance semantics.** The bound refers to exactly feasible points. With
feastol 1e-6, SCIP's incumbents for these subproblems lie up to about 1e-3
below the tight-tolerance values. For example, period 1 of waterno2_06 at
`logs/mult_06_w1.json` gives 0.81781 at feastol 1e-6 and 0.81870 at 1e-9
(`check_tight.py`). Targets derived from such values are therefore
conservative.

**Checks run** (targeted; no project-wide checks, no CI):

- `test_relax.py 6 data/waterno2_06.p4.sol 40` → **PASS**
  (`logs/test_relax_06.log`). For each period of MINLPLib point p4
  (violation ≈ 1e-11), and for 40 random sub-boxes containing it:
  - the point stays in every FBBT box;
  - it satisfies every relaxation row to 1.2e-11;
  - the rigorous bound for random objectives and random dual vectors never
    exceeds c·x (maximum −5.7e-8).
- `test_rbb2.py` (unreachable targets). With target = SCIP incumbent + 0.05,
  rbb must not certify, and it did not on periods 0, 1 and 5. It stopped
  with bounds of 167.16552 (incumbent 167.16584), 0.8178167 (incumbent
  0.8178104; tight-tolerance value 0.81870) and −223.45867 (incumbent
  −223.45884).
  - All three bounds are within 4e-4 of the incumbents.
  - The one bound above its 1e-6-tolerance incumbent (period 1) is still
    below the value of the 1e-9-feasible point.
  - With the reachable target (incumbent − 1e-3) all three periods were
    certified.
- `scip_unreliable_rbb.py`: on three periods, rbb's certified value lies
  below points feasible to 1e-9 (Section 5).
- `crosscheck_plain.py`: a plain B&B, without root OBBT and reduced-cost
  tightening, re-certified the waterno2_06 targets of periods 1 and 3.

## 5. SCIP findings (validity-relevant)

Setup: `scip_unreliable.py`, `scip_unreliable_rbb.py`,
`logs/scip_unreliable*.log`. It uses fixed multipliers
(`logs/scip_repro_mult.json`), single-period subproblems of waterno2_06, and
PySCIPOpt 6.2.1 with SCIP 10.0.2 / SoPlex 8.0.2.

| period | SCIP settings that report `optimal` at the wrong value | value claimed | point feasible to 1e-9 (re-solved with its pump configuration fixed) | rbb certified |
|---|---|---|---|---|
| 0 | default, feastol 1e-8 | 169.950327 | 168.108652 | ≥ 168.107652 |
| 4 | default, noobbt, seed 7, feastol 1e-8 | −5.723535 | −6.730644 | ≥ −6.731984 |
| 5 | default, seed 7 | −229.759028 | −232.172857 | ≥ −232.173990 |

- SCIP's reported dual bound is therefore **invalid by up to 2.4** on these
  166-variable, 9-binary MINLPs. The error is far outside any tolerance
  effect.
- With the binaries fixed, SCIP finds the better point. So the optimal
  pump-configuration subtree is pruned incorrectly in the full solve.
- Turning off propagation (`propagating/maxrounds = 0`) avoided the error in
  these three cases. The bundle logs still show corrections under that
  setting, however.
- Setting `presolving/maxrounds = 0` crashes the Python process with a
  segmentation fault (reproduced twice).
- The consequence for this work: on this family, SCIP dual bounds are not
  certificates. We have no evidence that the listed SCIP bounds are wrong;
  they lie far below our certified bounds. Our bounds do not use them.

## 6. Results and runtime

Per-period certification details are in `logs/cert_TT_w1_impl.{json,log}`.
Each JSON stores:

- the multipliers as float reprs (these exact floats define the bound);
- per period: the SCIP target, the certified value, the rbb status, the node
  count and the time.

Per-period time includes two SCIP runs of at most 120 s each, which only set
the target.

**waterno2_06 in detail** (`logs/cert_06_w1_impl.log`).

| period | SCIP estimate | certified φ_t | B&B nodes | time |
|---|---|---|---|---|
| 0 | 158.445520 | 158.445420 | 1789 | 33 s |
| 1 | 3.320117 | 3.320017 | 5387 | 99 s |
| 2 | 0.055952 | 0.055852 | 6067 | 108 s |
| 3 | 0.011964 | 0.011864 | 7577 | 151 s |
| 4 | −5.762229 | −5.762329 | 6631 | 119 s |
| 5 | −218.067239 | −218.067339 | 1745 | 41 s |

The horizon term is μ·c = 185.8668 × 1.752499999 (μ from
`logs/mult_06_w1_impl.json`). The sum, formed in exact rational arithmetic,
is ≥ **263.735099441**.

Other waterno2_06 variants:

- Without the implied level bounds (`logs/cert_06_w1.log`) the certified
  bound is 262.701963972.
- A plain B&B without root OBBT and reduced-cost tightening re-certified the
  targets of periods 1 and 3 (`crosscheck_plain.py`,
  `logs/crosscheck_plain_06.log`).

**Runtime** (wall time on a shared machine, single-threaded processes).

- waterno2_06:
  - bundle: about 650 s with 6 workers for the final run (18 iterations);
    earlier runs without implied bounds took about 620 s;
  - implied bounds: about 50 s;
  - certification: 151 s with 4 workers (550 s summed over periods).
- waterno2_09 and waterno2_12:
  - bundle: 27 and 41 min with 4–5 workers;
  - certification: 520 s and 601 s wall with 5 and 6 workers.
- waterno2_18 and waterno2_24:
  - bundle: 68 and 54 min with 5–9 workers; SCIP subproblems of the
    high-demand periods often hit the 120 s limit;
  - both bundles were stopped with a predicted increase of about 1–2, so
    their bounds can still be raised slightly;
  - certification: 1664 s and 1615 s wall with 8 and 10 workers. The
    slowest periods are the high-demand ones: 76k nodes and 1280 s for
    period 15 of waterno2_18.


## 7. Attempts to close the remaining gap (all exploratory, SCIP estimates unless stated)

1. **Two-period windows.** The windows keep the internal links, so they
   would reduce the gap.
   - SCIP did not solve window {0, 1} in 600 s at the period-Lagrangian
     multipliers (`logs/bundle_06_w1_final.json`,
     `logs/windows2_scip_*.log`):
     - default: dual 161.9, primal 172.3;
     - no propagation: dual 70.3, primal 173.6.
   - rbb on the same window, at the multipliers in
     `logs/mult_06_impl_tmp.json`, reached only 98.5 after 1200 s (62,499
     nodes; `logs/window01_rbb_test.log`). To help, it would have to exceed
     the sum of the two single-period values, about 162–166.
   - **Failed.**
2. **Dynamic programming over level boxes** (`dpbox.py`, `dpbundle.py`).
   - Idea: split the boundary levels into boxes, give each period copies
     constrained to the same box, and take the shortest path. This is valid
     for any box grid.
   - waterno2_06, tank 1 split at 3.5: +0.001.
   - waterno2_03, tank 1 in 12 boxes: 74.07 → 75.11.
   - waterno2_03, 2 boxes per tank (8 per boundary) with re-optimized
     multipliers: 75.38 after 7 iterations.
   - Closing the gap would need fine boxes in all three tanks, i.e. K²
     subproblems per period for K boxes per boundary. **Not pursued.**
3. **DP over bins of the horizon variable** (`dpqa.py`): +0.0005 on
   waterno2_06.
4. **Configuration probing with cutoff 282.9** (`probe_config.py`).
   - 19–35 of the 108 pump configurations per period survive.
   - Re-optimizing with no-good rows (`bundle_06_ng1.log`) gives about
     263.99 vs 263.74: at most +0.25. **Not certified.**
5. **Level probing with cutoff 282.9** (`probe_levels.py`): only 3 of the 15
   boundary-level domains shrink. **Not pursued.**
6. **Diagnosis.**
   - The Lagrangian prices tank-1 water at about −60 per level unit.
   - The period solutions jump to extreme start levels (for example L1 = 5).
     This exploits the head dependence of the pump costs, which the linear
     prices cannot pin down.
   - Example, waterno2_03: period 0 ends with tank 1 at 4.16 and period 1
     starts at 5.0. At the boundary-0 tank-1 price of −62.5 this mismatch
     lowers the bound by about 52.
   - The pure pump cost of the Lagrangian solution (154.3) is above the
     optimum (115.0). The bound is low because of such level jumps, not
     because pumping is avoided.
   - No linear price removes the jumps: the period value functions are
     nonconvex in the levels, because pump costs depend on the head and pumps
     are on/off with minimum flows.
   - Removing this gap requires coupling consecutive periods at fine level
     resolution. Neither SCIP nor our B&B could do this within the time
     limits.

## 8. Primal points

**MINLPLib points.** All points below were evaluated exactly in rational
arithmetic from the decimal `.sol` values (`evalpt.py`):

- waterno2_06 p1–p4: objective values equal the listed ones; maximum
  absolute row violation 6.6e-10 (p1), 1.1e-11 (p2, p4), 4.2e-11 (p3); no
  bound violations; binaries integral.
- Best points of the larger instances (09 p4, 12 p9, 18 p6, 24 p5):
  violations ≤ 9.8e-11.

**Window re-optimization** (`primal.py`).

- Method: fix all periods outside a 2-period window at the incumbent; SCIP
  (feastol 1e-9, 120 s) then solves the window MINLP with the true
  objective, the link rows to the fixed neighbours, and the horizon row
  restricted to the window. A result is accepted only if its exact
  evaluation shows violation ≤ 1e-8. Two passes.
- waterno2_06: nothing better than p4 was found with 2-period windows
  (120 s and 300 s limits) or 3-period windows (300 s). The only "accepted"
  change lowers the value by 2e-6 at violation 1e-9, a tolerance artifact.
  We report p4 as the best point.
- Larger instances: improved points are stored as float reprs in
  `logs/primal_TT_w2.json`. Exact evaluation:

| instance | our primal value (exact) | max abs. row violation (row) | max bound violation | binaries integral | listed primal |
|---|---|---|---|---|---|
| waterno2_09 | 914.011970350 | 1.00e-09 (e1677) | 5.73e-11 | True | 922.5953 |
| waterno2_12 | 2233.821335282 | 1.00e-09 (e2097) | 3.09e-10 | True | 2263.3584 |
| waterno2_18 | 5023.982735143 | 4.44e-09 (e299) | 8.94e-10 | True | 5269.6388 |
| waterno2_24 | 6963.795154460 | 1.00e-09 (e3896) | 9.00e-10 | True | 7332.7217 |

The improved points are not exactly feasible. Their maximum absolute row
violation is 1e-9, except 4.4e-9 for waterno2_18. MINLPLib lists points with
infeasibility up to 1e-8.


## 9. Relation to the first-wave remark

The first wave recorded that a 20-minute attempt to recover the period
partition failed. The partition is exact, and takes under a second, once the
copy rows between tank-balance variables are removed (Section 2). The first wave also
noted that "the period subproblems are MINLPs, whose bounds we could not
verify independently". That is now resolved by `rbb.py`. Each period of
waterno2_06 is certified in 33–151 s, including the two SCIP runs that set
the target, with 1.7k–7.6k B&B nodes.

## 10. Files

Core:

- `wmodel.py`: OSIL → polynomial rows (via `osilx.py`); exact period
  partition (`structure`).
- `evalpt.py`: exact rational evaluation of points.
- `period.py`: window models for SCIP (oracle only) and the Lagrangian
  objective.
- `rbb.py`: rigorous LP-based spatial B&B (the certificate).
- `implied.py`: implied bounds by rigorous FBBT/OBBT on the full model.
- `kkt.py`: least-squares KKT multipliers at a point.
- `bundle.py`: multiplier optimization.
- `certify.py`: certified-bound driver.
- `collect.py`: tables.
- `primal.py`: window re-optimization.

Checks:

- `test_relax.py`, `test_rbb2.py`, `crosscheck_plain.py`, `check_tight.py`.
- `scip_unreliable.py`, `scip_unreliable_rbb.py`.
- Earlier SCIP diagnosis scripts, superseded by `scip_unreliable.py`:
  `diag_settings.py`, `diag_window0.py`, `diag_fixed.py`,
  `diag_supergrad.py`.

Gap-closing experiments (Section 7):

- `dpbox.py`, `dpbundle.py`, `dpqa.py`;
- `probe_config.py`, `probe_levels.py`;
- `test_window_rbb.py`, `test_windows.py`, `horizon_only.py`.

Development and diagnostics: `lagr_solution.py`, `summarize.py`,
`time_periods.py`, `prof_rbb.py`, `diag_rbb_root.py`, `test_rbb.py`.

Data:

- `data/`: MINLPLib `waterno2_06.gms` and `waterno2_06.py`, and the
  solution files used. The OSIL files are read from
  `~/.cache/minlplib/minlplib/osil/`.

Logs (`logs/`):

- certificates: `cert_*_w1_impl.json` / `.log`;
- multipliers: `mult_*.json`;
- implied bounds: `implied_*.json`;
- bundle runs: `bundle_*.log` / `.json`;
- primal points: `primal_*_w2.json` / `.log`;
- SCIP findings: `scip_unreliable*.log`;
- experiments: `dp*`, `probe*`, `window01_rbb_test.log`,
  `windows2_scip_*.log`, `horizon_only_34.log`;
- structure checks: `structure_all.log`, `period0_dump.txt`.

**Commands actually run for the reported numbers.** All were run from this
directory with `OMP_NUM_THREADS=1`, and with `WATERNO2_IMPLIED=logs/implied_TT.json`
where implied bounds are used.

- `python3 implied.py T logs/implied_TT.json 2`
- `python3 bundle.py T 1 <iters> logs/bundle_TT_w1_impl.json <start> <workers> 120`
- `python3 certify.py T logs/mult_TT_w1_impl.json 1 logs/cert_TT_w1_impl.json <workers> 300000 3600`
- `python3 evalpt.py T <point>`
- `python3 test_relax.py 6 data/waterno2_06.p4.sol 40`
- `python3 test_rbb2.py 6 logs/mult_06_w1.json 0,1,5 20000 300`
- `python3 crosscheck_plain.py 6 logs/cert_06_w1_impl.json 1,3`
- `python3 check_tight.py 6 1 logs/mult_06_w1.json`
- `python3 scip_unreliable.py`
- `python3 scip_unreliable_rbb.py`
- `python3 primal.py T <start> logs/primal_TT_w2.json 2 120 2`

No project-wide checks were run and no CI results were consulted.


## Independent verification (added by the root, 2026-09-30)

An independent verifier rechecked the results with its own code
([report](../../reviews/waterno2-verification/verification-report.md)):

- **Structure:** a different recovery rule gives the same period partition
  for T = 1–24 (166 variables, 9 binaries, 203 rows per period; 3(T−1) link
  rows and one horizon row).
- **Lagrangian bound:** signs and the multiplier sign of the horizon row are
  correct; the implied tank-level bounds were proved by hand and by exact
  bound tightening for T = 6–24. Periods 1–3 depend on them.
- **Per-period bounds:** the verifier's own exact-rational branch and bound
  certified all six waterno2_06 periods at the authors' values, plus
  waterno2_09 period 6 and waterno2_24 period 19; the exact sums match for
  all T. The waterno2_06 bound 263.735099441 is reproduced independently.
  All other periods were certified later
  ([`../../reviews/waterno2-recheck.md`](../../reviews/waterno2-recheck.md)).
  (An earlier version said "The other 48 periods of sizes 09–24 were not
  rechecked"; the recheck counts 61 such periods.)
- **Primal points:** values and violations confirmed exactly (row
  violations up to 4.44e-9, bound violations up to 9.0e-10; not exactly
  feasible).
- **SCIP 10.0.2 (SoPlex 8.0.2, PySCIPOpt 6.2.1) returns wrong optimal values
  on three period subproblems.** The cheaper points were turned into exactly
  feasible rational points (168.108652, −6.730644, −232.172853, against
  SCIP's claimed optima 169.950, −5.724, −229.759). SCIP's own solution
  checker accepts them and BARON agrees with the true optima. Tolerance
  (feastol 1e-9, numerics emphasis) and presolve are ruled out; the cause
  is an invalid bound reduction in the search tree (node 288 of period 0),
  and only disabling node propagation, especially in the nonlinear
  constraint handler, fixes all three periods. `scip_unreliable.py`
  reproduces it. No upstream report has been filed; that is left to the
  user.

*Root edit (2026-09-30, closing revision):* the header and the
verification section now record the recheck of all 63 period bounds of
waterno2_09–24 (`reviews/waterno2-recheck.md`). No bound changed.
