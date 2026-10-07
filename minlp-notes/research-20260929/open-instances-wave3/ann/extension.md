# ann_cumene_tanh: a tighter rigorous dual bound (extension of report.md, Section 4)

Date: 2026-09-30. Status: computational result, independently re-certified
(*root update:* [`../../reviews/ann-extension-review.md`](../../reviews/ann-extension-review.md)
replayed both runs bit for bit, checked the coverage of the domain, and
proved f ≥ −3386.5402291369187 on every closed region and every final open
box with its own bounding code, which shares no code with `ann_tm.py`; the
review's minor corrections are applied below and listed in Section 11).
The instance is **not closed**. All runs were single-threaded
(`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`), time-limited, on a shared machine
(load average 15–20 on 36 cores during the runs, so timings are indicative).

A **dual bound** here is a number L with L ≤ f(x) for every point x of the
relaxation R of wave 3 (report.md, Section 4; the relaxation was verified in
`../../reviews/wave3-verification/verification-report.md`, Section 3). Since
R contains every feasible point of the OSIL model, L is also a dual bound for
the OSIL model.

## 1. Result

| quantity | value |
|---|---|
| primal (wave-3 point, `sol/ann_cumene_tanh.wave3.sol`, verified) | −3379.98239407177 |
| incumbent used for pruning (strictly feasible in R, interval-certified) | −3379.982394046125 |
| wave-3 dual bound (3600 s) | −4024.4949777 (gap 644.5, 19.1%) |
| **new dual bound** (1800 s + 5400 s, 2.70M boxes) | **−3386.5402291369187** |
| gap to the wave-3 primal | 6.558 (0.194%) |

The gap shrinks from 19.1% to 0.194%, a factor of 98. The printed decimal lies
below the certified double (exactly −3386.540229136918696895…), so it is itself
a valid bound. For comparison, the new code
reaches −3540.4 in 318 s and −3426.92 in 1800 s. The wave-3 code needed 3600 s
to reach −4024.49.

The bound comes from one branch and bound split into two runs:

- **Run 1.** `ann_tm.py` with the separate-symbol model, 1800 s from the full
  box. Code: `ext_logs/ann_tm_v1_snapshot.py`; log `ext_logs/run_v1_1800.log`.
  It ended with 111,474 open boxes (saved in `ext_logs/open1800_v1.npz`) and
  certified −3426.9202275613525. Every box it closed either had lb > UB, was
  proved infeasible, or was emptied by the objective cut; so its closed-box
  minimum is +∞.
- **Run 2.** The final code (`ann_tm.py`, identical to
  `ext_logs/ann_tm_run2_snapshot.py` apart from the module docstring), resumed
  from those open boxes for 5400 s with the `sep-gradsmall` settings. Log
  `ext_logs/run2_resume_5400.log`; final open boxes in `ext_logs/open_run2.npz`.

Each point of R lies in a box closed by run 1, in a part removed by domain
reduction (which contains no point of R with f ≤ UB), or in one of the saved
boxes, so L = min(closed minimum of run 1, final bound of run 2) is valid.
The same covering, including domain-reduction parts, holds inside run 2.
(Corrected after review: the domain-reduction parts were missing from this
sentence. In run 1, 27,999 reductions removed 46.2% of the domain volume.) Both runs
report min(closed minimum, least open key, UB).

## 2. What changed relative to wave 3

The wave-3 bounds were interval enclosures, mean-value forms, and a
mean-value form of a Lagrangian with fixed KKT multipliers. Report.md gives
three reasons why they were weak. This extension addresses each of them with
methods already used in this continuation.

### 2.1 Taylor models with tracked rounding (`TMModel`)

Each box of the 5 inputs is written u = m + h·ε with ε ∈ [−1, 1]⁵. Every
determined variable gets a first-order Taylor model (TM) x ∈ c + a·ε ± r,
where a has 5 entries. The rounding rules:

- **Linear rows.** The rows have exact rational coefficients, each enclosed as
  midpoint ± radius. The remainder update is
  r′ = |w|r + w_rad(|c| + S + r) + b_rad + γ_{k+1}(|w|(|c| + S) + |b|),
  with S = Σ|a_i| and γ_n = nu/(1 − nu). The computed r′ is then inflated by
  (1 + γ_{2k+20}).
- **tanh.** On the argument range [l, t], tanh(s) = αs + β + e(s) with
  |e(s)| ≤ δ, proved as follows. g = tanh − αs is convex for s ≤ 0 and
  concave for s ≥ 0. On each piece one extreme is at an end point. The other
  is bounded by the tangent line at a point near the stationary point. For
  the min-range slope, g is monotone. Two slopes are tried (chord and
  min-range), and the smaller δ is kept. All tanh values come from the
  rigorous table-exp enclosure of wave 3 (`ann_bb.tanh_pt`); no libm result is
  trusted. On boxes near the frontier, δ is within the resolution of a
  200-point grid search over α, so a better slope would not help.
- **Products in the objective.** `tm1.TM`, the product rule reviewed for the
  pindyck certificate.

On sampled boxes, the TM gap to f* is 4–7 times smaller than the wave-3
first-order bound (table in 2.2; `ext_logs/test_tm_lumped.log`).

### 2.2 One noise symbol per neuron (`SepModel`)

This is the largest single gain. A single remainder per variable adds the
linearization errors of different neurons in absolute value. Affine
arithmetic instead keeps one symbol η_n ∈ [−1, 1] per tanh neuron: 200
first-layer and 50 second-layer symbols, shared by all variables. The
objective's dependence on each neuron's error can then cancel across the
network outputs.

- **Storage.** Variables before the first tanh layer have no η terms. A
  first-layer output carries δ_n on its own symbol. The roughly 250 later
  variables store their η coefficients densely.
- **Rounding.** The bounds are those of TMModel with S = Σ|a| + Σ|e|. Sums of
  250 terms use a γ_{n+2} inflation.

Median gap between f* = −3379.98 and the box bound, on random boxes whose
relative widths are 0.5–1.5 times ρ (`test_tm.py`, 200 boxes per row; no
domain reduction in this test):

| boxes | wave-3 first-order bound | TMModel | SepModel |
|---|---|---|---|
| near the optimum, ρ = 0.3 | 5.18·10⁴ | 1.36·10⁴ | 2.68·10³ |
| near the optimum, ρ = 0.03 | 1.58·10³ | 347 | 47.6 |
| near the optimum, ρ = 0.003 | 12.7 | 2.46 | 0.446 |
| near the optimum, ρ = 0.001 | 2.06 | 0.294 | 0.0866 |
| uniform, ρ = 0.1 | 3.1·10³ (a) | 451 | 206 |

(a) From the TMModel log. The SepModel log gives 1.06·10⁴ for the same
column, because "open in both" selects different boxes (noted by the
review).

- **Remainder ratio.** Near the optimum at ρ = 0.001, the median ratio of
  remainder to linear variation, r_f/‖a_f‖₁, is 0.181 for TMModel and 0.022
  for SepModel.
- **Cost.** Both models cost about 1–2 ms per box.
- **Fathoming.** On uniform boxes with ρ = 0.1, the share of boxes fathomed at
  UB rises from 0.26 (wave 3) to 0.74 (TMModel) and 0.90 (SepModel).

### 2.3 Per-box LP dual instead of fixed multipliers

This addresses "some regions must be proved infeasible" and the indefinite
Lagrangian Hessian.

- **Constraints used.** Every finite bound of magnitude below 10⁵ on a
  non-tanh variable is a *side*: 141 sides, 21 distinct after removing copies
  such as x590 = x647 = x701. On feasible ε each side gives a linear
  inequality ã_j·ε ≥ β_j, where β_j includes the remainder.
- **Bound.** For any μ ≥ 0, weak duality over the ε-box gives
  f ≥ c_f − r_f + Σ μ_j β_j + min_ε (a_f − Σ μ_j ã_j)·ε.
- **Choice of μ.** Up to 3 sides are used: those most violated at the
  minimizer of the objective's linear part. μ is taken as the best vertex of
  the arrangement, found by enumerating μ = 0 and 56 candidate 3×3 systems. The chosen μ
  is then evaluated in outward-rounded interval arithmetic, so a poor μ still
  gives a valid bound.
- **Separate-symbol refinement.** With SepModel the bound is also evaluated
  at the same μ with the η terms of the objective and the sides combined:
  −Σ_n |e_f,n − Σ_j μ_j s_j e_j,n|. The larger value is kept.
- **Infeasibility tests.** A box is infeasible if one side cannot hold on it
  (β_j > max ã_j·ε). It is also infeasible if a nonnegative combination of the
  selected sides, with Σμ = 1, cannot hold on the ε-box (a Farkas
  certificate).

This per-box LP bound takes the place of the fixed-multiplier Lagrangian
bound and of the third-order form, which never applied here because H_L is
indefinite.

### 2.4 Domain reduction

Two rounds of interval propagation shrink the ε-box. Each round uses the side
inequalities and the objective cut −a_f·ε ≥ c_f − r_f − UB, where r_f
includes the η part for SepModel. The cut removes
only points with f > UB, and the final bound never exceeds UB, so it stays
valid.

The LP and the infeasibility tests run on the reduced ε-box. If a coordinate
shrinks below 70%, the reduced box is mapped back to u with outward rounding
and re-queued. Rounding directions: products and quotients are rounded
outward, and sums of the "rest" terms are rounded up.

### 2.5 Branching on the 5 inputs; the wave-3 bounds kept where they help

- **Search order.** Best-first, 512 boxes per batch, bisection at the
  midpoint.
- **Branching score.** For each input k: box width times the width of the
  interval gradient of the KKT Lagrangian, plus μ-weighted gradient widths of
  the LP sides. This measures curvature, as wave 3 did. Several Taylor-model
  scores that avoid the interval pass were tried; all were worse (Section 6).
- **Wave-3 interval bounds.** On boxes wider than 1/16 of the domain
  (relative, in some coordinate), the full wave-3 interval pass also runs:
  natural enclosure with clipping, mean-value forms, the centre value, and
  interval gradients. The maximum of all valid bounds is used. On smaller
  boxes only the interval-gradient pass runs, for the branching score.
- **Taylor-model clipping.** If the TM range of a bounded variable exceeds its
  bounds and the interval intersection is under 1/4 of the TM width, the TM is
  replaced by that constant interval. This is valid for feasible points only,
  which is all a lower bound needs. With a threshold of 1 instead of 1/4,
  tightness near the optimum got worse.

## 3. Rigor: what the bound relies on

1. **The relaxation R and its reduction to the 5 inputs.** These are from wave
   3 (`ann_model.decode`, asserted structure) and were verified
   independently.
2. **Floating-point behaviour.** IEEE double round-to-nearest for numpy
   elementwise operations and for scipy's sparse products. The γ_n bounds hold
   for any summation order, with or without FMA. `np.nextafter` gives the
   directed steps.
3. **Rigorous exp for tanh.** The table exp of `kan_iv.iexp_pt_fast`: a
   50-digit mpmath table of exp(j·ln2/64), a degree-8 Taylor polynomial, and a
   remainder bound. This is shared with the wave-3 KAN and ANN code.
4. **The TM product rule of `tm1.py`.** Reviewed with the pindyck
   certificate.
5. **Decimal constants.** Rows and bounds are exact Fractions, enclosed by
   `frac_iv`.

The incumbent is used only for pruning and for the objective cut. The
certified value is min(closed minimum, open keys, UB), so it is valid whatever
UB is. The primal −3379.98239407177 is the verified wave-3 point.

Soundness tests, which are sampling checks and not proofs:

- **`test_tm.py`.** Random boxes of six sizes, near the optimum and uniformly
  placed. Every sampled point that is feasible with margin 10⁻⁹ must have
  f ≥ box bound. Results: TMModel, 0 violations among 3020 feasible samples
  (smallest margin f − bound = 0.176); SepModel, 0 violations among 3020
  (smallest margin 0.0732).
- **`test_tm2.py`.** The full `fbound_combo` pipeline, including the LP,
  domain reduction with the objective cut, and the interval passes.
  - *Boxes:* near the optimum (5 sizes), from the saved frontier, halves of
    frontier boxes, and uniform boxes; 12 per family.
  - *Test points:* the box centre, random points, and constrained local
    minimizers inside the box (SLSQP).
  - *Checks:* the pipeline is called with a cutoff UBt of UB + 300 or +∞. No
    feasible point with f ≤ UBt may lie below the box bound, outside the
    reduced box, or in a box declared infeasible. Near-violations are
    re-evaluated with 50-digit mpmath.
  - *Why not UBt = UB:* a first attempt with UBt = UB was uninformative,
    because almost no test point is feasible with f ≤ UB.
  - *Result:* 0 violations among 355 qualifying feasible points in 192 box
    evaluations; the smallest margin f − bound was 0.0668. The log is
    `ext_logs/test_tm2_sep-gradsmall.log`.
  - *Limitation (from the review):* each frontier family, where the pruning
    actually happens, had only 3–7 qualifying points, so this evidence was
    thin. The review's sampling (15,201 feasible test points in 250 boxes,
    0 violations) and its full re-certification supersede it.

## 4. Runs

| run | settings | time | boxes | bound |
|---|---|---|---|---|
| wave 3 (`ann_fast.py`, best-first) | interval + mean-value + fixed Lagrangian | 3600 s | 2.37M | −4024.4949777 |
| run 1 (`run_v1_1800.log`) | SepModel, LP, domain reduction, full interval pass | 1800 s | 563,656 | −3426.9202275613525 |
| run 2 (`run2_resume_5400.log`) | the same, resumed; interval pass only on boxes > 1/16, otherwise gradient pass only | 5400 s | 2,134,528 (208,223 left open) | **−3386.5402291369187** |

Progress of the certified bound (from the logs):

| time | bound |
|---|---|
| 318 s | −3540.38 (run 1) |
| 1069 s | −3455.2 |
| 1800 s | −3426.92 |
| 1800 + 2068 s | −3398.22 |
| 1800 + 2732 s | −3394.39 |
| 1800 + 4438 s | −3388.60 |
| 1800 + 5401 s | −3386.5402291369187 (least open key; the closed-box minimum is −3379.9855) |

## 5. Why the gap does not close

- **The frontier lies along the constraint surface.** The open boxes are spread
  over the domain: their median normalized distance from the optimum was 0.46
  at 1800 s (`dbg_open2.py`). Their centres mostly have x772 slightly below
  0.999 (1/10/50/90/99% quantiles 0.977, 0.9885, 0.996, 0.998, 0.9999; 4.5%
  have x772 ≥ 0.999), so most violate x772 ≥ 0.999 slightly, and the
  objective values at the centres are mostly within −25 to +70 of UB
  (quantiles of f(centre) − UB: −23, −12.6, 17.4, 70.6, 171). (Quantiles
  from the review; the earlier text said "x772 between 0.97 and 0.995" and
  "within about 50 of UB".) On the surface x772 = 0.999, f is nearly flat over a large
  region. At the optimum, the reduced Hessian of the Lagrangian on the tangent
  space of the two active constraints has eigenvalues 40, 270 and 2.1·10⁵ in
  coordinates normalized to the unit box (finite differences). A quadratic
  model with eigenvalue 40 suggests that along this direction f changes by
  only about 20 (½·40·1²) across the whole domain.
- **The limiting enclosure is x772.** Its enclosure is dominated by the
  linearization errors of the 50 second-layer tanh neurons. It enters the
  bound multiplied by the constraint's multiplier, about 2·10⁴ at the optimum
  and 2·10⁵ in LP solutions near the frontier. In about two thirds of the
  finite-bound frontier boxes, no side is violated at the minimizing corner of
  the linearized objective. There the bound is the objective TM alone, and only
  splitting helps. A console-only check on 1024 random frontier boxes tried
  two changes: choosing μ with the η terms included (candidate enumeration
  plus exact coordinate ascent on the full dual function), and using 1, 2 or
  3 LP sides. Neither changed the share of fathomed boxes (0.403) or the
  median deficit UB − lb (27.7).
- **Even the optimum's neighbourhood closes slowly.** A B&B restricted to the
  sub-box |u − u*| ≤ 0.02·(domain width) reached −3380.637 after 900 s
  (354,978 boxes; gap 0.655, 1.9·10⁻⁴ relative; `ext_logs/local_close_0.02.log`).
  Along the weak direction, f varies by only about 0.008 across this sub-box.
  This is the cluster effect of a first-order method at an ill-conditioned
  constrained minimum.
- **No other near-optimal local minimum was found.** 120 SLSQP starts from
  frontier box centres (`local_scan.py`) gave only 3 feasible local solutions:
  the known optimum and one at −3113.84. The other starts failed to reach
  feasibility. This is weak evidence only.

## 6. Failed or unhelpful variants (300 s runs unless stated)

These comparisons ran concurrently on a loaded machine, so they are indicative
only.

| variant | bound at 300 s | note |
|---|---|---|
| TMModel alone, linear-sensitivity branching (console only, not logged) | −11,899 | TM remainders on large boxes are huge, and branching on linear sensitivity is poor |
| TMModel + interval pass + gradient-width branching + domain reduction (console only) | −3741.3 | |
| SepModel, same settings (`cmp_sep_nofull.log`) | −3547.6 | chosen |
| + full-dual μ (coordinate ascent) (`cmp_sep_full.log`) | −3560.7 | 13% fewer boxes in the same time, no tighter |
| no interval pass, TM branching score including linear terms (`cmp_sepfast.log`) | −3941.3 | splitting along directions of linear variation leaves the lower child's bound unchanged |
| interval pass kept, TM score (`cmp_sep_tmsmear.log`) | −3946.4 | |
| curvature-only TM score, without / with the interval pass (`cmp_sepfast2.log`, `cmp_sep_nofull_tmsmear2.log`) | −3807.0 / −3835.6 | |
| TM score with the KKT Lagrangian, interval pass only on boxes > 1/16 (`cmp_hybrid.log`) | −3542.2 (fresh), −3425.46 resumed from the 1800 s frontier vs −3420.40 (`res_hybrid.log`, `res_nofull.log`) | 1.7× more boxes but a smaller gain per box |
| gradient-only pass on boxes ≤ 1/16 (chosen for run 2) | same bounds and branching as the full pass on 512 frontier boxes | 12% faster |

Wave 3's third-order bound (`ann_h3.py`) never applies at the optimum,
because the Lagrangian Hessian there is indefinite. A second-order argument
in the pindyck style would have to use the active constraints, for example
f − λg + σg² ≤ f on {0 ≤ g ≤ λ/σ}. Its convexity region would be a tiny box
around the optimum, so it would not remove the flat valley. This was assessed
but not implemented.

## 7. Literature and novelty

- **Source paper.** Schweidtmann and Mitsos, "Deterministic global
  optimization with artificial neural networks embedded", J. Optim. Theory
  Appl. 180 (2019) 925–948 ([arXiv 1801.07114](https://arxiv.org/abs/1801.07114)).
  It is the source of the cumene case study: 5 inputs, 14 MLPs, 794 variables,
  789 equalities and 1 inequality, purity ≥ 0.999.
  - MAiNGO in reduced space did not converge: absolute gap 8·10¹⁰, or 1·10⁵
    with adapted settings, after 100,000 s.
  - BARON in full space never improved its initial lower bound.
- **MINLPLib** lists no dual bound for ann_cumene_tanh
  (`open-instances-scout/fetched.csv`).
- **Later work.** A brief web search found no later global certificate. Two
  optimization-online PDFs on tanh relaxations in MAiNGO/MeLOn (April 2025)
  returned HTTP 404 and were not examined.
- **Novelty.** Within this search, the bound above is the best rigorous dual
  bound known for the instance. The search was brief, so this is not a claim
  of priority.

The methods themselves (affine arithmetic, Taylor models, LP duals over
linearizations, and interval constraint propagation) are standard. The
contribution is applying them with tracked rounding to this instance.

## 8. Commands run (targeted only; no project-wide checks, no CI)

All from `open-instances-wave3/ann/`, with `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`
and `timeout`:

- `python3 test_tm.py 200` and `python3 test_tm.py 200 sep`
  (logs `ext_logs/test_tm_{lumped,sep}.log`); earlier console-only runs with
  100–200 boxes during development.
- `python3 test_tm2.py 12 sep-gradsmall` (log `ext_logs/test_tm2_sep-gradsmall.log`).
  Two earlier attempts: one with 30 boxes per family was stopped by the tool's
  time limit and its output was lost; one with cutoff UB had almost no
  qualifying test points and was stopped.
- `python3 ann_tm.py 1e-6 300 … <model>` for the comparisons in Section 6
  (`ext_logs/cmp_*.log`, `res_*.log`).
- `python3 ann_tm.py 1e-6 1800 ext_logs/open1800_v1.npz sep` (run 1).
- `python3 ann_tm.py 1e-6 5400 ext_logs/open_run2.npz sep-gradsmall ext_logs/open1800_v1.npz`
  (run 2).
- `python3 local_close.py 0.02 900`, `python3 local_scan.py ext_logs/open1800_v1.npz 120`,
  and `python3 dbg_open2.py <npz>` (diagnostics), plus short inline profiling
  and δ-optimality checks.

## 9. Files (all new; nothing from wave 3 was edited)

| file | content |
|---|---|
| `ann_tm.py` | TMModel, SepModel, tanh linearization, LP dual, domain reduction, B&B driver with resume and checkpoints |
| `test_tm.py`, `test_tm2.py` | soundness and tightness tests |
| `local_close.py`, `local_scan.py`, `dbg_open2.py` | diagnostics |
| `ext_logs/` | run logs, saved frontiers (`open1800_v1.npz`, `open_run2.npz`), code snapshots of both runs |

## 10. Possible next steps (not done)

- **Neuron-argument branching.** Split on the argument of the few second-layer
  neurons that dominate the x772 enclosure, instead of only on the inputs.
- **Second-order Taylor models** for the second tanh layer, so that quadratic
  terms can cancel across neurons.
- **A certified local argument around the optimum**, combined with a change of
  coordinates that follows the flat direction of the constraint surface.

## 11. Root revision after review (2026-09-30)

From [`../../reviews/ann-extension-review.md`](../../reviews/ann-extension-review.md)
(verdict: verified; all issues minor, none affecting the bound). Changes:
the header records the independent re-certification; the combination
argument in Section 1 now includes the parts removed by domain reduction;
the Section 2.2 table notes which log the wave-3 uniform value comes from;
Section 3 notes that `test_tm2.py` had few frontier points; Section 5 gives
the review's quantiles. Not reproduced by the review (console-only claims):
the multipliers of 2·10⁵ in frontier LPs, the "two thirds" share of frontier
boxes, and the `local_scan` value −3113.84. The review also recommends a NaN
guard in the B&B driver (a NaN lower bound would close its box silently;
the replay found none among 2.70M evaluations), and observed that a full LP
over all 255 symbols and all constraint sides (the reviewer's own bound,
with its own affine forms and tanh linearization) closes 58.1% of 4096
final-frontier boxes, against 53.5% for the authors' per-box bound
(`fbound_combo`, 3-side LP), consistent with Section 5's view that
the choice of multipliers is not the main obstruction.
