# Review: ann_cumene_tanh extension (dual bound −3386.5402291369187)

Date: 2026-09-30. Reviewed: `open-instances-wave3/ann/extension.md` and the code, logs
and saved frontiers it lists. The reviewer did not produce that work. All new code and
logs are in `reviews/ann-extension-review-checks/`. Every run was single-threaded
(`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`), ran under `timeout` on the shared machine,
and was targeted at this instance. No project-wide verification was run, and CI was not
inspected.

## Verdict

**Verified.** The dual bound −3386.5402291369187 is valid for the wave-3 relaxation R,
and therefore for the OSIL model. The reviewer re-certified it independently:

- The reviewer's own rigorous bound (`annx.py`) proves f ≥ −3386.5402291369187 on
  every region that the two runs closed: 1,644,110 regions.
- It proves the same inequality on all 208,223 boxes left open at the end.
- A deterministic replay of both runs regenerated the closed regions. It reproduced the
  authors' log lines exactly and their saved frontiers bit for bit.
- Checks on volume and on random points confirm that the closed regions and the final
  open boxes cover the input domain.

The primal −3379.98239407177 and the gap arithmetic are also confirmed. The corrections
listed at the end are minor wording and diagnostic details; none of them affects the
bound.

The re-certification has limits. It rests on the reviewer's own code, which only the
reviewer has checked (Section 3). The partition into regions comes from replaying the
authors' bounding code as a black box, but its coverage was checked independently.

| item | verdict | key numbers |
|---|---|---|
| relaxation R | verified | the verifier's decoder (wave 3) and the authors' decoder give the same box, 723 bounds, identical forward rows and equal f at 50 digits (difference 3e-47) |
| replay of run 1 (1800 s) | reproduced exactly | 44 of 44 log lines identical; final frontier of 111,474 boxes identical to `open1800_v1.npz` |
| replay of run 2 (5400 s, resumed) | reproduced exactly | 166 of 166 log lines identical; final frontier of 208,223 boxes identical to `open_run2.npz`; LB −3386.5402291369187, closed-box minimum −3379.985488216472 |
| aggregation and coverage | verified | volume of closed + removed + open regions = start volume to 12 digits in both runs; 4000 random points all covered, none twice; no NaN lower bound in 2.70M evaluations |
| closed regions, reviewer's own bound | **all 1,644,110 proved ≥ L\*** | run 1: 278,495; run 2: 1,365,615 (details in 3.4) |
| final open boxes, reviewer's own bound | **all 208,223 proved ≥ L\*** | 84,235 proved infeasible; 5 needed subdivision (at most 3 nodes) |
| soundness sampling (both bounds) | 0 violations | 15,201 feasible test points in 250 boxes; smallest margin 0.0032 (authors) and 0.0091 (reviewer) |
| primal −3379.98239407177 | verified | 50 digits: −3379.9823940717715481; row violation 4.6e-27; no bound violated |
| gap arithmetic | verified | 6.5578 (0.194%), down from 644.51 (19.07%), a factor of 98.3 |
| tightness table, timeline, run table | verified from the logs | one caveat on the uniform ρ = 0.1 row (Section 4) |
| Section 5 diagnostics | mostly verified | reduced Hessian eigenvalues 39.5, 269.6 and 2.12e5 confirmed; the x772 range and the "within 50 of UB" statement are loose (Section 5) |
| literature | confirmed | source paper, Table 4: BARON absolute gap 1e20, MAiNGO 8e10 or 1e5 after 1e5 s; MINLPLib lists no dual bound |

L\* denotes −3386.5402291369187 throughout.

## 1. The relaxation R

`t_model.py` compares the decoder that `annx.py` uses with the authors' decoder
(`ann_model.decode`). The former is `annv.decode`, written by the wave-3 verifier; it
does not import the authors' code. The two agree on:

- the input box;
- the 723 constraint bounds (722 finite variable bounds and x772 ≥ 0.999);
- all 779 forward rows (targets, coefficients and right-hand sides, compared as exact
  rationals);
- the objective, to within 3.3e-47 at 20 random points evaluated with 50 digits.

R was verified in wave 3. R keeps every row and bound of the OSIL model except the
product rows and e749/e750, whose extra variables are free. Therefore min over R ≤ the
OSIL optimum, and a dual bound for R is one for the OSIL model.

## 2. Aggregation: replay of both runs

`replay.py` loads the authors' bounding code as a black box: the v1 snapshot for run 1,
and `ann_tm.py` with the `sep-gradsmall` settings for run 2. It calls only
`fbound_combo`, `incumbent` and `kkt_lag`. The queue logic of `ann_tm.bnb` is written out
again, operation by operation, so that the order of boxes is reproduced. The replay also
records every region the run closes:

- **processed boxes with lb ≥ UB − tol**, including lb = +∞;
- **boxes shortened by domain reduction.** The part removed is stored as at most 10 slab
  boxes.
- **boxes closed on being taken from the queue** (key ≥ UB − tol);
- **boxes too narrow to split.**

The last two kinds did not occur in either run. The replay stops at the authors'
processed-box counts.

**Results** (`replay_run1.log`, `replay_run2.log`, `leaves_check.log`):

- **Exact reproduction.** Every progress line (processed, open, UB, LB, closed volume,
  reduced volume) is identical to the authors' logs, apart from the wall time. The final
  frontiers equal the saved `.npz` files as multisets of (lo, hi, key) rows, bit for bit.
  So `ext_logs/ann_tm_v1_snapshot.py` is the code that produced run 1. `ann_tm.py`
  produced run 2; it differs from `ann_tm_run2_snapshot.py` only in the module docstring.
- **Run 1 (563,656 boxes).** 212,092 processed boxes were closed:
  - 211,919 had lb = +∞ (proved infeasible, or emptied by the objective cut);
  - 173 had a finite lb, the least being −3379.9557947883436, which is above UB.

  So the closed-box minimum is +∞, as the report says. In addition, 27,999 domain
  reductions removed 46.18% of the domain volume (66,403 slabs).
- **Run 2 (2,134,528 boxes).** 899,981 processed boxes were closed:
  - 886,360 had lb = +∞;
  - 13,621 had a finite lb, the least being −3379.985488216472.

  In addition, 465,634 slabs came from domain reductions. The final LB is
  min(−3379.985488216472, least open key −3386.5402291369187, UB) = L\*.
- **Volume check.** Closed volume + removed volume + final open volume equals the start
  volume to 12 digits in both runs. For run 2 the start is the volume of the run-1
  frontier, 0.026892055874 of the domain.
- **Coverage.** Four thousand random points were tested: 2000 uniform in the domain, and
  1000 in random boxes of each saved frontier. Every point lies in a closed region or a
  final open box, and none lies in two regions.
- **NaN.** None of the 2.70M lower bounds was NaN. This matters because the queue logic
  (`keep = lb < UB − tol`) would silently close a box whose bound is NaN.

The combination rule of `extension.md` Section 1 is therefore correct:
L = min(closed minimum of run 1, final bound of run 2).

## 3. Independent re-certification with the reviewer's bound (`annx.py`)

### 3.1 Method

`annx.py` does not use the authors' code. It works as follows:

- **Affine forms.** Each determined variable is written as x = C + A·ξ ± r, with
  ξ ∈ [−1, 1]^255: 5 input symbols and one symbol per tanh neuron. Nothing is clipped,
  so every form is valid on the whole box, not only at feasible points.
- **Rounding.** Every floating-point step carries a relative slack τ = 1e-12, at least
  30 times the γ_n bound of any sum used (n ≤ 260, γ_n ≤ 3e-14). The slack also covers
  the representation errors of the rational constants.
- **tanh.** The reviewer's own interval exp is used: reduction by an enclosure of ln 2,
  a degree-22 Taylor polynomial with a remainder bound, and outward rounding with
  `nextafter`. It relies on IEEE +, −, ×, ÷ only; no libm transcendental is trusted.
  The linearization tanh(s) = αs + β ± δ on [l, t] works as follows:
  - g = tanh − αs is split into pieces at 0 and at points just either side of ±s₀,
    where s₀ is the float stationary point.
  - On a piece inside s ≤ 0 or s ≥ 0, g′ = sech² − α is monotone. If g′ has one rigorous
    sign at both ends of the piece, the extremes of g are at the ends.
  - Otherwise the piece gets the crude enclosure [tanh(a) − αb, tanh(b) − αa].

  This argument differs from the authors' tangent-line argument.
- **Constraints.** Every bound of R that the affine range can violate enters an LP over
  all 255 symbols, solved with HiGHS. HiGHS only supplies the multipliers μ ≥ 0. The
  bound is then evaluated by weak duality in outward-rounded interval arithmetic:

  f ≥ C_f − r_f − Σ_j μ_j (s_j(C_j − b_j) + r_j) − ‖A_f − Σ_j μ_j s_j A_j‖₁.

  An infeasible LP is replaced by an elastic LP. A box is also infeasible if some bound
  cannot hold anywhere on it.
- **Objective cut.** None is used. Every region is proved against the target L\*
  directly.
- **Subdivision.** A region below the target is bisected along its relatively widest
  input, up to 4000 nodes.

**Assumptions:**

- IEEE double round-to-nearest in numpy and scipy;
- `np.nextafter` gives the directed steps;
- the verifier's decoder is correct (it agrees exactly with the authors', Section 1);
- `mpmath` is used only for the ln 2 enclosure and for the tests.

### 3.2 Checks of the reviewer's own code

- **tanh enclosure.** At 5007 points (normal, uniform up to ±40, tiny, subnormal and
  |z| = 350), the enclosure contains the 60-digit value every time (`t_basic.log`).
- **Linearization.**
  - 404 intervals, sampled at 303 points each, gave 0 violations (`t_basic.log`).
  - 900 extreme intervals (|s| up to 1000, widths from 1e-14 to 1e3), sampled at 201
    points plus the exact stationary points, also gave 0 violations (`t_tanhlin2.log`).
  - The worst ratio |error|/δ was 1.000000, so δ is tight.
- **Forward pass.** At 21 points the affine forms enclose the 50-digit objective
  (`t_basic.log`).
- **Soundness sampling** (`t_sound.py`, `t_sound.log`). The boxes were 25 near the
  optimum at each of six sizes (ρ = 0.1 to 1e-4), 25 uniform at each of two sizes, and
  50 run-2 frontier boxes (the 25 with the lowest keys and 25 random).
  - Test points were float-feasible samples and SLSQP local minimizers (the verifier's
    `annv.local_min`). Any point within 1e-3 of a bound was re-evaluated at 50 digits.
  - Result: 15,201 feasible test points and 0 violations, for both the reviewer's bound
    and the authors' `fbound_combo`. The latter was run with UB = +∞ and with UB + 10.
  - Smallest margins: 0.0091 for the reviewer's bound and 0.0032 for the authors'.
  - Both bounds flag the same number of boxes as infeasible (13, 19 and 20 in the three
    families that have any). This compares counts only, not individual boxes.

### 3.3 Strength compared with the authors' bound

The two bounds are of similar strength, and neither dominates.

- **Near the optimum.** The reviewer's bound is higher by a median of 1.25 at ρ = 0.1,
  shrinking to 0.03 at ρ = 0.001. The authors' bound is higher by a median of 0.004 at
  ρ = 1e-4 (`t_sound.log`).
- **On the final frontier** (4096 random boxes, `t_cmp2.log`). The authors' bound, from
  processing each box once, closes 53.5% of them. The reviewer's one-shot bound closes
  58.1%. Where both bounds are finite, the reviewer's is higher by a median of 0.40.
- **Consequence.** A full LP over all symbols and sides helps a little. It does not
  remove the obstruction described in Section 5 of the report. The reviewer's one-shot
  bound over the whole final frontier is still −3386.625, so it does not improve L\* on
  its own.

### 3.4 Results (`verify_boxes.py`; logs `ver_leaves_run1.log`, `ver_leaves_run2.log`, `ver_open_run2.log`)

| set | regions | proved ≥ L\* | proved infeasible (one shot) | needed subdivision | most nodes |
|---|---|---|---|---|---|
| run 1, closed boxes and removed slabs | 278,495 | 278,495 | 231,958 | 1,512 | 223 |
| run 2, closed boxes and removed slabs | 1,365,615 | 1,365,615 | 1,068,293 | 173 | 21 |
| final open boxes (`open_run2.npz`) | 208,223 | 208,223 | 84,235 | 5 | 3 |

Every region is proved to satisfy f ≥ L\* on R. Together with the coverage in Section 2,
this gives min over R ≥ L\* = −3386.5402291369187, independently of the authors' per-box
bounds. Wall time was 360 s, 1280 s and 374 s with 4, 5 and 4 processes.

## 4. Review of the authors' code and of the other claims

**Code (read in full).** No error was found in the rigor of the following parts:

- `ann_tm.py`: the tanh linearization (convex and concave pieces with tangent lines; the
  min-range slope, for which g is monotone), the affine rule with midpoint–radius
  weights, the separate-symbol bookkeeping (E rows and the new symbol per neuron), the
  clipping (valid only at feasible points, which is all that is needed), `_phi_rig`,
  `_phi_rig_s`, `_farkas_rig`, `_fbbt`, `reduced_box`, and the bnb/resume logic;
- `tm1.TM` with 255 symbols;
- the wave-3 interval passes (`old_bounds`, `grad_only`).

Two further points:

- **Objective cut.** It removes only points with f > UB at the time of the cut. Because
  UB never increases and the final value is min(…, UB), the removal is harmless.
- **NaN.** A NaN lower bound would close its box silently, since `lb < UB − tol` is then
  false. The replay found none, and the reviewer's re-certification makes this point
  moot for the reported runs. A guard (`np.nan_to_num(lb, nan=-inf)`) would still be
  prudent in future runs.

**Claims checked against the logs:**

- **Tightness table (Section 2.2).** It matches `test_tm_{sep,lumped}.log`, as do the
  remainder ratios (0.181 and 0.022) and the fathoming shares (0.26, 0.74 and 0.90).
  Caveat: in the uniform ρ = 0.1 row, the wave-3 value 3.1e3 comes from the lumped log.
  The separate-symbol log gives 1.06e4 for the same column, because "open in both"
  selects different boxes.
- **Soundness tests (Section 3).** `test_tm.py`: 3020 feasible samples per model; smallest
  margins 0.0732 (SepModel) and 0.176 (TMModel). `test_tm2.py`: 355 points; smallest
  margin 0.06683. Weakness: in `test_tm2`, the frontier families, where pruning actually
  happens, had only 3–7 qualifying points each. The reviewer's sampling and the full
  re-certification supersede these tests.
- **Constraint sides (Section 2.3).** 141 sides, 21 distinct, confirmed. The count of 56
  candidate systems is C(8, 3), confirmed.
- **Runs (Section 4).** Processed counts, the 318 s value −3540.38, the 1800 s value
  −3426.92, and the times 1800 + 2068, 2732 and 4438 s with −3398.22, −3394.39 and
  −3388.60 all match the logs.
- **Section 6 table.** Every entry matches its log. Note: `cmp_sepfast.log` and
  `cmp_sepfast2.log` both print "model sepfast"; the curvature-only variant cannot be
  told apart from the log header.
- **Sub-box of half-width 0.02 (Section 5).** The value −3380.6372672042103 after 900 s
  and 354,978 boxes matches `local_close_0.02.log`.
- **Printed decimal.** The printed −3386.5402291369187 lies below the stored double
  −3386.54022913691869689…, so it is a valid bound as printed.

## 5. Section 5 diagnostics

- **Reduced Hessian.** `t_diag.py` computes it by 40-digit central differences in
  normalized coordinates. At u\*, the Lagrangian f − 58.51(x647 + 1) − 20891.4(x772 − 0.999)
  has full-Hessian eigenvalues −44.4, 191.6, 576.1, 3.97e4 and 2.24e5. On the tangent
  space of x647 and x772, the eigenvalues are 39.5, 269.6 and 2.12e5. Confirmed.
- **Active constraints.** x647 is active (1.25e-12 from its bound), as are its copies
  x590 and x701, and so is x772 (1.0e-12 from its bound). This supports "strictly
  feasible" in the sense of the inner float bounds.
- **1800 s frontier centres.**
  - **x772.** The quantiles (1, 10, 50, 90, 99%) are 0.977, 0.9885, 0.996, 0.998 and
    0.9999. The report's "between 0.97 and 0.995" is loose: the median lies above 0.995,
    and 4.5% of the centres satisfy x772 ≥ 0.999.
  - **Distance from u\*.** The median normalized distance is 0.464. Confirmed.
  - **Objective.** f(centre) − UB has quantiles −23, −12.6, 17.4, 70.6 and 171.
    "Within about 50 of UB" holds for most boxes but not all.
- **Not reproduced.** The 2·10⁵ multipliers in frontier LPs, the "two thirds" share,
  and the `local_scan.py` result (−3113.84) exist only as console output, and the
  reviewer did not rerun them.

## 6. Literature

- **Source paper.** Its text was fetched from arXiv 1801.07114. Section 5.4 (cumene
  process) and Table 4 give:
  - the problem: 14 MLPs; 794 variables, 789 equalities and 1 inequality in the full
    space; 5 inputs and purity ≥ 0.999;
  - BARON (full space, F1–F4): absolute gap 1·10²⁰ after 100,000 s;
  - MAiNGO (reduced space): absolute gap 1·10¹¹ (F3) or 8·10¹⁰ (envelope), and 1·10⁵
    with the adapted setting;
  - "BARON does not improve its initial lower bound on the objective at all."

  The report's summary is accurate. The arXiv title reads "Global Deterministic
  Optimization with Artificial Neural Networks Embedded"; the JOTA title is the one the
  report gives.
- **MINLPLib.** The instance page (fetched) lists the primal bound −3379.982394 and no
  dual bound.
- **Later work.** A brief search found no later certificate. The two optimization-online
  PDFs from 2025 again returned HTTP 404. A 2026 PSE-community entry (LAPSE:2026.0427)
  that the search surfaced could not be fetched (HTTP 429) and was not examined.
- **Novelty.** The report's qualified novelty statement is therefore reasonable.

## 7. Corrections suggested for `extension.md`

1. **Section 1, combination argument.** "Each point of R lies in a box closed by run 1 or
   in one of the saved boxes" omits the regions removed by domain reduction: 46.2% of
   the domain volume in run 1. Suggested wording: "…lies in a closed box, in a part
   removed by domain reduction (which contains no point of R with f ≤ UB), or in a
   saved box." The same applies to run 2.
2. **Section 5, x772 of the frontier centres.** Replace "between 0.97 and 0.995" with
   "mostly between 0.98 and 0.9999 (median 0.996)".
3. **Section 5, objective values.** Replace "within about 50 of UB" with "mostly within
   −25 to +70 of UB".
4. **Section 2.2, uniform ρ = 0.1 row.** Note that the wave-3 value 3.1e3 comes from the
   TMModel test; with the SepModel box set it is 1.06e4.
5. **Status line.** Once the root accepts this review, "not independently verified" can
   refer to it.
6. **Optional.** Add a NaN guard in `bnb`.

None of these changes the bound, the gap or the conclusions.

## 8. Commands run (targeted only; from `reviews/ann-extension-review-checks/` unless noted)

- `python3 replay.py run1 /tmp/annrev/replay_run1.npz` (1805 s) and
  `python3 replay.py run2 /tmp/annrev/replay_run2.npz` (5220 s). Logs:
  `replay_run1.log`, `replay_run2.log`.
- `python3 leaves.py extract …` for each run, and
  `python3 leaves.py /tmp/annrev/replay_run1.npz /tmp/annrev/replay_run2.npz /tmp/annrev/leaves_all.npz 2000`
  (`leaves_check.log`).
- `python3 verify_boxes.py <regions.npz> <out.npz> -3386.5402291369187 4|5` on the run-1
  regions, the run-2 regions and `open_run2.npz` (`ver_leaves_run1.log`,
  `ver_leaves_run2.log`, `ver_open_run2.log`).
- `python3 t_basic.py`, `t_tanhlin2.py`, `t_model.py`, `t_diag.py`, `t_cmp2.py`,
  `t_sound.py 25 400 7`; logs of the same names.
- Console-only exploration, with no log kept: `t_frontier.py`, `t_speed.py`, `t_cmp.py`.
- `python3 annv.py points` in `reviews/wave3-verification/ann/` (primal re-evaluation;
  output quoted in the verdict table).
- Web: the arXiv abstract and PDF of 1801.07114, the MINLPLib instance page, and two
  searches.

Large intermediate files (replay records, region lists and per-region results, about
50 MB) are in `/tmp/annrev/` and were not copied into the repository. They can be
regenerated with the commands above.

## 9. Files

`reviews/ann-extension-review-checks/`:

| file | content |
|---|---|
| `annx.py` | the reviewer's rigorous bound: affine forms with 255 symbols, own interval exp/tanh, full LP with weak duality, subdivision |
| `replay.py` | deterministic replay of both runs, recording every closed region |
| `leaves.py` | frontier identity, volume and coverage checks; extraction of the closed regions (slabs for domain reductions) |
| `verify_boxes.py` | proves f ≥ target on many regions (multiprocessing) |
| `t_basic.py`, `t_tanhlin2.py`, `t_model.py`, `t_sound.py`, `t_diag.py`, `t_cmp2.py` (+ `.log`) | checks described above |
| `t_frontier.py`, `t_speed.py`, `t_cmp.py` | console-only exploration |
