# Recheck of the catmix400 and catmix800 dual bounds

Date: 2026-09-30. Reviewer: independent verifier. I did not produce the results
under review, and I did not write the earlier verification.

**Claims under review.** `open-instances-wave2/cops/report.md`, Section 3:
- catmix400 dual bound −0.048056547950296354;
- catmix800 dual bound −0.048055901841076894.

The earlier verification (`reviews/cops-verification/verification-report.md`)
recomputed catmix100/200 with its own code. It checked catmix400/800 by code
reading only.

## Verdict

Both claimed bounds are **confirmed**. For each instance my certified bound is
higher (better) than the claimed one, so the claimed value is also a valid
lower bound.

| instance | claimed dual | my certified dual | mine − claimed | authors' primal | primal − mine | runtime |
|---|---|---|---|---|---|---|
| catmix400 | −0.048056547950296354 | **−0.04805654782467129** | +1.26e-10 | −0.048056547756611555 | 6.8e-11 | 43 min |
| catmix800 | −0.048055901841076894 | **−0.04805590147967565** | +3.61e-10 | −0.048055901330847467 (`_snap`) | 1.49e-10 | 43 min |

- **Runtimes:** one single-threaded process each (`OMP_NUM_THREADS=1`), wall
  clock. The two final runs ran at the same time as each other. The machine
  was shared, with load 8–13 on 36 cores, so runtimes are indicative only.
- **Primal values:** the authors' primals are the exact objective values of
  their controls, as enclosed by the 60-digit interval simulation in
  `v_catmix_model.py` (see `logs/catmix_model_400_800.log`).
- **By-product (primal).** The controls of the DP policy on the final grid
  give an exactly feasible catmix800 point with objective
  −0.0480559013312308003. This is 3.8e-13 better than the authors' best
  point; details are in the primal by-product section below.
- **Brackets on the optimum:**
  - catmix400: [−0.04805654782467129, −0.048056547756611555], width 6.8e-11;
  - catmix800: [−0.04805590147967565, −0.0480559013312308003], width 1.48e-10.

Coarser grids gave valid but weaker bounds than the claims (see the run table
below). Such a shortfall reflects grid resolution. It is not evidence against
a claimed bound: only a feasible point with a value below a claimed bound
would refute it, and none was found.

## What I used, and how independent it is

**Code.** I copied the previous verifier's files unchanged into
`reviews/catmix-recheck-checks/`. The sha256 hashes match the originals in
`reviews/cops-verification/`:

| file | sha256 prefix |
|---|---|
| `v_catmix_dp.py` | cffec48e |
| `v_catmix_model.py` | c0ddcaf2 |
| `v_catmix_selftest.py` | 80d8001c |
| `osilx.py` | 4bcdc1d8 |

I added three scripts of my own:
- **`recheck_dp.py`**, a driver. It imports the rigorous routines
  `v_catmix_dp.Maps`, `stage` and `terminal` unchanged. It adds only:
  - per-stage grid construction;
  - float diagnostics, which do not enter the bound.

  Its backward loop is the same as `v_catmix_dp.run`, and it asserts the grid
  properties that validity needs (next section).
- **`osil_crosscheck.py`**, a regex-based check of the shared OSIL reader.
- **`policy_exact.py`**, an exact rational evaluation of control vectors.

**Authors' files.** I did not import or run any of the authors' scripts. I
used their control files (`catmixN_u.npy`, `catmix800_u_snap.npy`) as data
only:
- to compute the primal θ trajectory, which places a fine window of rays
  (placement affects tightness, not validity);
- to compare primal values.

**How independent this is:**
- The implementation is independent of the authors' `catmix_bound.py`. The
  per-ray minimization differs:
  - the previous verifier's code cuts u at preimages of cone boundaries and
    applies an exact Dinkelbach step;
  - the authors use a 1-D interval branch and bound.
- The *principle* is the same: an exact DP on the 1-D projective separator,
  made rigorous by concavity and chord interpolation. An error in the
  principle would affect both implementations. The principle was checked by
  reading, by the previous verifier and by me (next section).
- The OSIL reader `osilx.py` is shared by the authors and the previous
  verifier. I cross-checked it against an independent parse.

## Validity checks

1. **OSIL reader cross-check** (`osil_crosscheck.py 400 800`). A regex parse of
   the raw files matches every item `osilx.read` returns for catmix400 and
   catmix800:
   - variable bounds and types;
   - the objective terms and constant −1;
   - row bounds;
   - all 1,600/3,200 linear coefficients;
   - all 3,200/6,400 quadratic terms, as decimal strings.
2. **Structure and exact nonnegativity** (`v_catmix_model.py 400 800`).
   - The full row pattern is asserted.
   - Over [0,1], the exact minimum of each entry of `Nm = Q adj(P)`, of
     `T = (1,1) adj(P)` and of `Q` is ≥ 0.
   - `det P ≥ 1 + a > 0`.
   - `ep + em = 2` exactly, and `c − 9a = 1e-18` for both N.
3. **Stage self-test at the new sizes** (`v_catmix_selftest.py 400` and `800`):
   40 stages × 17 off-grid rays. The rigorous stage bound never exceeds a dense
   float minimum:
   - max(LB − dense) = −7.8e-16 at both N;
   - the bound stays within 2.0e-15 (N=400) and 1.8e-15 (N=800) of the dense
     minimum.
4. **My reading of the rigorous routines** in `v_catmix_dp.py`:
   - `qmin_lb` / `peval_lo`: lower coefficients are valid because u ≥ 0; the
     vertex term is a global lower bound for A > 0; rounding is directed
     outward.
   - `dinkelbach`: correct sign-dependent use of D_min / D_max.
   - Crude bound: valid because the chord values are clipped at 0 (V ≥ 0).
   - Cone ranges: verified by rigorous quadratic bounds before use.
   - Terminal map: `(1,1)adj(P)/det P`.
   - Initial map: `Q(u_0)x_0`.
   - Final value: `dn(w0 − 1)`.
   - Incumbents and all float quantities affect only which bound is used or
     where u is cut, never validity.
   
   I found no validity problem.
5. **Grid validity** (asserted in `recheck_dp.build_grids` for every stage):
   - every ray is dyadic with at most 30 fractional bits, so `1 − θ` and the θ
     differences are exact;
   - 0 and 1 are present;
   - the rays are strictly increasing.
   
   Any such grid gives a valid bound.
6. **Consistency:**
   - Every bound computed here lies below every known primal value.
   - Two runs repeated with the diagnostic switched on reproduced their bounds
     bit for bit (N=400 wide band 2^-19; N=400 narrow band 2^-19). The first
     was run once through `v_catmix_dp.py` and once through my driver, so this
     also checks that the driver matches `v_catmix_dp.run`.
   - The largest per-ray loss against the float incumbent was 2.0e-15 in every
     N=400/800 run. This is the rigorous minimization's own slack.
   - At N=100, my driver reproduces the previous verifier's config-A bound
     −0.048069432031981114 bit for bit, using a different grid (below).

## Grid design: what limits the bound

The grid for each stage has three parts:
- a base (`v_catmix_dp.make_grid`: 2^-13 on [0, 13/128], 2^-7 above);
- bands of finer dyadic rays;
- a window of 401 rays at spacing 2^-24 around the authors' θ trajectory.

**Findings from the N=400 experiments** (full table below):
- **Base spacing does not matter.** Base 2^-15 and base 2^-13, with the same
  band, gave bit-identical bounds.
- **A wider window helps little.** It improved the bound by only 1.3e-10 out
  of a gap of 1.9e-8.
- **Band spacing on the singular arc sets the gap.** Across runs where the
  path stays inside a uniform band of spacing d:
  - gap ≈ n_arc · C · d², where n_arc is the number of singular-arc stages
    (236 at N=400, 472 at N=800);
  - the fitted C was 1.2–1.4 at N=400 and 1.4–1.8 at N=800.
  
  This is an empirical fit, not a proven law.

**Why (heuristic explanation, supported by a float diagnostic).**
- On the singular arc, many control paths have nearly the same cost.
- The DP lower bound follows the path where the chord interpolation
  underestimates V the most, which is the coarsest reachable part of the grid.

The diagnostic `tree_support` in `recheck_dp.py` measures where the bound's
dependence lies. It pushes the weights of the chord values the bound depends
on forward from x_0, through the float argmin controls. It shows:
- **The dependence is a single narrow bundle.** On the arc it covers 2–14
  rays and settles in one place for hundreds of stages.
- **It avoids the fine window around the authors' trajectory.** On the arc it
  sits in band cones instead.
- **With a narrow band [0.0703, 0.0710] at 2^-19, it went to the one coarse
  cone left.** That cone, [0.070190, 0.070301], lies just below the band. The
  bundle sat in it from stage 56 to 290, about 3.5e-4 below the arc. The gap
  rose to 1.3e-6, against 1.06e-9 with the wide band [0.0695, 0.0717].

**Final design.**
- A fine **core** at 2^-21 over [0.0703, 0.0710].
- A **shell** at 2^-19 over [0.0695, 0.0717], so that no coarse cone lies
  near the arc.
- Core and shell on the arc stages with a margin: 40–310 at N=400, 95–600 at
  N=800.
- The 2^-24 window on all other stages, where the bundle does follow the
  authors' trajectory. It is skipped on stages 56–288 (N=400) and 112–576
  (N=800), where the bundle ignores it.
- N=800 only: an extra 2^-17 band over [0.060, 0.0695] on stages 570–650, to
  cover the exit from the arc.

**Result of the final runs.** The bundle stayed well inside the core:

| N | stages | θ range of the bundle | width | rays |
|---|---|---|---|---|
| 400 | 60–285 | [0.070526, 0.070693] | ≤ 2.4e-6 | ≤ 6 |
| 800 | 120–570 | [0.070568, 0.070652] | ≤ 2.4e-6 | ≤ 6 |

The margin to the core edges is ≥ 2.3e-4. The final gaps (6.8e-11 and
1.49e-10) agree with the fit.

**Consistency with the claims.** The authors' band spacing was 1e-6. With the
fit above, it predicts gaps of about 2.6e-10 (N=400) and 7.1e-10 (N=800). The
claimed gaps are 1.9e-10 and 5.1e-10. So the claimed values are consistent
with the band-spacing effect, within a factor of about 1.4.

## All runs (every value is a valid rigorous bound)

**Gap definitions.** For N=400/800, "gap" is the authors' exact primal minus the
bound. For N=100 it is the previous verifier's polished primal
−0.048069432030979596 minus the bound.

**Notation.**
- `win` = 401 rays at 2^-24 around the authors' θ trajectory, on all stages
  unless a skip range is stated.
- `band X@e` = rays at spacing 2^-e over X, on all stages unless a stage range
  is stated.

**Runtimes.** Up to four single-threaded runs shared the machine at a time,
so runtimes vary with load.

| N | grid | bound | gap | mean rays/stage | pairs | time |
|---|---|---|---|---|---|---|
| 100 | base 13, band [0.0700,0.0714]@17 (stages 10–78), win | −0.04806943498510797 | 2.95e-9 | 1,465 | 7.7e7 | 130 s |
| 100 | same, band @19 | −0.048069432031981114 | 1.0e-12 | 1,839 | 2.4e8 | 391 s |
| 400 | base 13, band [0.0695,0.0717]@17, win (`mid`) | −0.048056566992440326 | 1.92e-8 | 1,617 | 2.2e8 | 353 s |
| 400 | base 15, same band, win (`e2`) | −0.048056566992440326 | 1.92e-8 | 4,058 | 3.8e8 | 618 s |
| 400 | base 13, same band, win at 2^-21 (`e3`) | −0.04805656686521554 | 1.91e-8 | 1,603 | 2.1e8 | 340 s |
| 400 | base 13, band [0.0695,0.0717]@19, win (`e1`) | −0.0480565488169118 | 1.06e-9 | 2,476 | 8.2e8 | 1,234 s |
| 400 | base 13, band [0.0703,0.0710]@19 (stages 45–300), win | −0.04805784021300497 | 1.29e-6 | 1,572 | 3.6e8 | 527 s |
| 400 | same, band @20 | −0.04805776371857396 | 1.22e-6 | 1,799 | 7.1e8 | 1,160 s |
| 400 | **final**: core [0.0703,0.0710]@21 + shell [0.0695,0.0717]@19 (stages 40–310), win skipped 56–288 | **−0.04805654782467129** | **6.8e-11** | 2,629 | 1.74e9 | **2,578 s** |
| 800 | base 13, band [0.0695,0.0717]@17, win (`mid`) | −0.04805594302333783 | 4.17e-8 | 1,617 | 3.5e8 | 568 s |
| 800 | base 13, band [0.0704,0.0709]@20 (stages 95–595), win | −0.04806322465405422 | 7.3e-6 | 1,660 | 8.3e8 | 1,225 s |
| 800 | base 13, band [0.0695,0.0717]@18, win | −0.04805591378357322 | 1.25e-8 | 1,903 | 4.9e8 | 811 s |
| 800 | **final**: core [0.0703,0.0710]@21 + shell [0.0695,0.0717]@19 (stages 95–600) + [0.060,0.0695]@17 (570–650), win skipped 112–576 | **−0.04805590147967565** | **1.49e-10** | 2,647 | 1.88e9 | **2,595 s** |

The largest per-ray loss against the float incumbent was 2.0e-15 in every
N=400/800 run (2.1e-15 at N=100), and every run needed at most one widening of
a cone range.

## Primal by-product

The float forward pass of the final-grid DP policy gives controls
(`logs/catmixN_final_policy_u.npy`). `policy_exact.py` evaluates them in exact
rational arithmetic:
- the double control values are taken exactly;
- the constants are the exact OSIL decimals;
- the states are the exact solution of the linear rows, and all are
  nonnegative.

The resulting point is exactly feasible.

| N | exact objective of policy controls | vs authors' best |
|---|---|---|
| 400 | −0.0480565477559440726 | 6.7e-13 worse |
| 800 | −0.0480559013312308003 | 3.8e-13 better than `_snap`; 1.86e-12 better than non-snap |

The 60-digit interval simulation in `recheck_dp.py` gives the same values.

I did not produce or check a double-rounded full variable vector for these
points. Such a vector would carry row violations of about 1e-16, like the
authors' vectors.

## Not checked, and caveats

- **Shared principle.** Both implementations rest on the same DP principle
  (homogeneity, concavity, chord interpolation). It was checked by reading
  and by exact nonnegativity checks; there is no third method.
- **Heuristic diagnostics.** The float diagnostics (`tree_support`, the
  n_arc·C·d² fit) are grid-design heuristics. They do not enter the bounds.
- **Remaining gap.** I did not try to close the remaining 6.8e-11 / 1.49e-10.
  Halving the core spacing would cost about 4× per run (roughly 3 h here).
- **Scope.** I did not recheck catmix100/200 or the chain instances.
- **Optimality.** The catmix optima are not known beyond the brackets above.

## Commands run (targeted; no CI or project-wide checks)

All commands were run from `reviews/catmix-recheck-checks/` with
`OMP_NUM_THREADS=1` (also `OPENBLAS_NUM_THREADS=1` and `MKL_NUM_THREADS=1`).

**Checks:**
- `python3 v_catmix_selftest.py 400` and `800` (`logs/catmix_selftest_{400,800}.log`;
  these also write `logs/catmixN_theta_traj.npy`).
- `python3 v_catmix_model.py 400 800` (`logs/catmix_model_400_800.log`).
- `python3 osil_crosscheck.py 400 800` (`logs/osil_crosscheck.log`).

**Bound runs:**
- `python3 v_catmix_dp.py N 13 0.0695 0.0717 17 200 24` for N = 400 and 800
  (`logs/catmixN_mid.log`).
- `python3 v_catmix_dp.py 400 13 0.0695 0.0717 19 200 24` (`e1`).
- `python3 v_catmix_dp.py 400 15 0.0695 0.0717 17 200 24` (`e2`).
- `python3 v_catmix_dp.py 400 13 0.0695 0.0717 17 200 21` (`e3`).
- `recheck_dp.py` runs for all other rows of the run table, with the options
  shown in each log's JSON line: `logs/cal100_*`, `logs/c400_*`,
  `logs/c800_*`, `logs/tree*.log`, `logs/catmix{400,800}_final.log`.

  The final commands were:
  - `python3 recheck_dp.py 400 13 --sband 0.0703 0.0710 21 40 310 --sband 0.0695 0.0717 19 40 310 --win 200 24 logs/catmix400_theta_traj.npy --win-skip 56 288 --tree logs/tree400_final.json --save-traj logs/catmix400_final_policy_traj.npy --save-u logs/catmix400_final_policy_u.npy`
  - `python3 recheck_dp.py 800 13 --sband 0.0703 0.0710 21 95 600 --sband 0.0695 0.0717 19 95 600 --sband 0.060 0.0695 17 570 650 --win 200 24 logs/catmix800_theta_traj.npy --win-skip 112 576 --tree logs/tree800_final.json --save-traj logs/catmix800_final_policy_traj.npy --save-u logs/catmix800_final_policy_u.npy`

**Primal check:**
- `python3 policy_exact.py 400 logs/catmix400_final_policy_u.npy` and the same
  for 800 (`logs/policy_exact_{400,800}.log`).

## Files

All files are in `research-20260929/reviews/catmix-recheck-checks/`:
- **my scripts:** `recheck_dp.py`, `osil_crosscheck.py`, `policy_exact.py`;
- **unchanged copies of the previous verifier's files:** `v_catmix_dp.py`,
  `v_catmix_model.py`, `v_catmix_selftest.py`, `osilx.py`;
- **`logs/`:** the run logs, JSON result lines, θ trajectories, tree-support
  diagnostics (`tree*.json`) and policy controls
  (`catmix{400,800}_final_policy_u.npy`). `logs/catmix100_theta_traj.npy` is a
  copy from `reviews/cops-verification/logs/`, used for the N=100 calibration.
