# eg_int_s, eg_disc_s, eg_disc2_s: rigorous dual bounds (retry of wave 3, Section 5)

Date: 2026-09-30; revised 2026-10-01 after review (Section 10). Status:
computational results with the coverage argument and error analysis given
below. An independent review
([`../../reviews/eg-retry-review.md`](../../reviews/eg-retry-review.md))
found them **verified**. It re-certified every leaf of the reported trees with
independent code, except in the seven eg_disc2_s parts without the optimum,
where it checked a sample of leaves. Its minor corrections are applied
(Section 10, items 1–7). A confirmation review
([`../../reviews/eg-retry-confirm-r1.md`](../../reviews/eg-retry-confirm-r1.md))
checked these corrections and found them **verified**. Its two optional
wording nits are also applied (Section 10, item 8); that wording change was
confirmed by [`../../reviews/round4-nits-confirm.md`](../../reviews/round4-nits-confirm.md)
(verdict verified, optional nits only; root update 2026-10-01). Code
in [`retry/`](retry/), logs in `retry/logs/`, primal points in `retry/sol/`.
Each process was single-threaded (`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`) and
time-limited; up to 8 processes ran at once on a shared 36-core machine whose
load average was 25–45, so timings are indicative only.

A **dual bound** is a number L with L ≤ objvar for every exactly feasible point
of the OSIL model (`~/.cache/minlplib/minlplib/osil/<name>.osil`, read with the
decimal-preserving `reviews/open-instances-verification/osilx.py`).

## 1. Results

| instance | listed primal (MINLPLib p1) | best listed dual | **new rigorous dual bound** | new primal (50-digit OSIL check) | gap | status |
|---|---|---|---|---|---|---|
| eg_int_s | 6.45310316 | 6.32629896 (SCIP) | **6.4531031529331155** | 6.4531031593842274 | 6.5·10⁻⁹ (1.0·10⁻⁹ rel.) | closed to 10⁻⁹ relative |
| eg_disc_s | 5.76053962 | 3.36596129 (SCIP) | **5.760539610694994** | 5.7605396164535106 | 5.8·10⁻⁹ (1.0·10⁻⁹ rel.) | closed to 10⁻⁹ relative |
| eg_disc2_s | 5.64210058 | 0 (SHOT) | **5.642100574331458** | 5.6421005799711068 | 5.6·10⁻⁹ (1.0·10⁻⁹ rel.) | closed to 10⁻⁹ relative |

- All three bounds exceed every dual bound listed on the MINLPLib pages (table
  below). The listed primal values lie within a relative 10⁻⁹ of the optimum.
  Our exactly feasible points confirm the upper side.
- eg_int_s had already been reported solved by a floating-point SCIP 8.1 run
  in the literature (Section 7). The new results for it are a rigorous
  certificate and a verified primal point. No closure of eg_disc_s or
  eg_disc2_s was found in the literature.
- Each bound equals UB − tol: UB is the certified value of the search's own
  primal point, and tol = 10⁻⁹·UB is the closing tolerance.
- No branch-and-bound box was left open.
- The new primal points agree with the listed p1 values to the printed digits.
  On eg_int_s our point is 3.3·10⁻¹⁰ worse than p1 (6.4531031590519). It is
  pushed strictly inside the active side row e26 so that its feasibility can
  be certified. Evaluated at 50 digits, p1 violates e26 by 2.9·10⁻¹⁶ and, with
  its listed objvar, row e12 by 4.6·10⁻¹⁵. eg_disc_s p1 violates e12 by
  1.7·10⁻¹⁴ in the same way. eg_disc2_s p1 is exactly feasible.
- Every bound is rigorous in the sense of Section 4: outward rounding or
  explicit floating-point error bounds throughout, and a coverage argument
  (Section 3.6).

Listed values, as printed on <https://www.minlplib.org/eg_int_s.html> (and the
pages of the other instances) on 2026-09-30 (copy in
`retry/logs/minlplib_pages_20260930.txt`):

| solver | eg_int_s | eg_disc_s | eg_disc2_s |
|---|---|---|---|
| ANTIGONE | −6.82078456 | −5.89996559 | −5.22577638 |
| BARON | 0.14309125 | −0.2567667 | −5.53779193 |
| COUENNE | −6.39393306 | −8.08686 | −8.0869773 |
| GUROBI | −1.54105206 | −5.01379636 | −5.74731082 |
| LINDO | −1.20527282 | −4.0246301 | −7.56589692 |
| SCIP | **6.32629896** | **3.36596129** | −1.48945961 |
| SHOT | 0 | 0 | **0** |
| primal (p1) | 6.45310316 (infeas. 2e-16) | 5.76053962 (infeas. 9e-15) | 5.64210058 (infeas. 0) |

## 2. Structure used

`retry/egdata.py` packs the decoding of wave 3 (`eg/eg_model.py`, which
asserts the row structure) into arrays. It also asserts that γ is common to
all terms of a row and negative, and that there are 24 objective rows followed
by 4 side rows.

- **One function, four discretizations.** All four Schoonen instances
  (eg_all_s too) share the same 28 rows in y = s·x, with s_i ∈ {1, 1/10}
  exact. Row k is
  g_k(y) = Σ_{m=1}^{97} a_km exp(Σ_i γ_ki (y_i − μ_kmi)²) + (linear terms),
  over y ∈ [.3,.6]×[.4,1]×[.4,1]×[.7,1.5]×[1,2]×[3,4]×[2,5].
  - eg_int_s: y5, y6, y7 integer (16 combinations); y1–y4 continuous.
  - eg_disc_s: y1–y4 on the 0.1 grid (1764 combinations); y5–y7 continuous.
  - eg_disc2_s: y5–y7 on the 0.1 grid (3751 combinations); y1–y4 continuous.
  - eg_all_s (not a target; closed by SCIP at 7.65775209): both grids.
- **Common length scales.** Within a row, γ_ki is the same for all 97 terms
  (asserted): each row is a Gaussian-kernel (GP-type) surrogate with weights
  a_km and centres μ_km.
- **Rows.** Rows e1–e24 read objvar ≥ c_k + g_k. Side rows: e25 and e26 carry
  the linear terms −0.45 y3 and −0.45 y2 and give g ≤ −0.3503 and g ≤ −0.3740;
  e27 and e28 have identical terms (checked once; the code treats them as
  separate rows and does not rely on this), and together they give
  −346.198237 ≤ g_27 ≤ 53.801763. The coefficients of e27/e28 are large
  (Σ|a| = 39,667, max |a| = 1711), so their values come from heavy
  cancellation.
- **Cancellation.** At the eg_int_s optimum, Σ_m |a_km e^{E_km}| is 61 for
  the active objective row e12, against |g_12| = 7.1. For the active side row
  e26 it is 78, against a Gaussian part of −0.083.

Best points found (float exploration, `retry/explore.py`, then certified):

| instance | integers | continuous part | active at the point |
|---|---|---|---|
| eg_int_s | (2, 4, 3) | x = (0.56422, 0.64685, 1, 0.93907) | objective row e12 alone; side row e26; bound x3 = 1 |
| eg_disc_s | (3, 10, 8, 12) | y5–y7 = (1.08002, 3.48536, 2.24158) | objective rows e8, e12 |
| eg_disc2_s | (11, 34, 24) | x = (0.33999, 1, 0.75262, 1.23707) | objective rows e8, e10, e12; bound x2 = 1 |

The landscape is flat across integer combinations: for eg_disc2_s, local
solves (6 starts per combination) gave 75 combinations with a local minimum
below 6.0 and 507 below 7.0 (optimum 5.642); for eg_disc_s, 10 below 6.0
(optimum 5.761). These are heuristic local minima, used only to understand the
search.

## 3. Method

### 3.1 Second-order Taylor model with the cancellation kept (`egfast.py`, `egtm.py`)

For a box X with centre c and radii r (integer coordinates either fixed, with
r_i = 0, or relaxed to their integer interval), write x = c + d. One term is
a·e^E with E(c + d) = E₀ + L(d) + Q(d), where

- L = Σ_i v_i d_i with v_i = 2γ_i s_i t_i and t_i = μ_i + s_i c_i;
- Q = Σ_i γ_i s_i² d_i² ≤ 0 (all γ < 0).

Then e^E = e^{E₀}(1 + L + Q + L²/2 + R), with

- R = LQ + Q²/2 + u³e^{θu}/6, where u = L + Q and θ ∈ (0, 1);
- |R| ≤ ℓq + q²/2 + (ℓ + q)³e^ℓ/6, where ℓ = Σ|v_i|r_i and q = Σ|γ_i|s_i²r_i².

Summing over the 97 terms with their signs gives g_k(c + d) = G + ∇·d +
dᵀHd/2 + ρ with |ρ| ≤ P. G, ∇ and H are signed sums:

- G = Σ_m w_m, with w_m = a_m e^{E₀m};
- ∇ = Σ_m w_m v_m;
- H = Σ_m w_m v_m v_mᵀ + diag(2γs²)·Σ_m w_m.

Their cancellation is therefore kept; only the remainder P = Σ_m |w_m| R̄_m is
summed in absolute value. This is the main difference from wave 3, whose
natural and mean-value enclosures summed term ranges.

- **Third-order alternative.** The beyond-quadratic part may also be bounded
  as a signed cubic C₃ = Σ_m w_m(L³/6 + LQ) plus a fourth-order remainder:
  - |C₃| ≤ (1/6)Σ_{ijk}|T_ijk|r_ir_jr_k + Σ_{ij}|U_ij|r_ir_j², where
    T_ijk = Σ_m w_m v_mi v_mj v_mk and U_ij = γ_j s_j² Σ_m w_m v_mi;
  - |R₄| ≤ q²/2 + ℓ²q/2 + ℓq²/2 + q³/6 + (ℓ + q)⁴e^ℓ/24.

  Per row, the smaller of the two totals is used. Both are valid, so the
  minimum is valid.
- **From the model to affine bounds.** The quadratic part is bounded by
  constants over the box: ½Σ_i min(H_ii, 0)r_i² − Σ_{i<j}|H_ij|r_ir_j from
  below. This gives, for every row k and every x ∈ X,

  aL_k + β_k·(x − c) ≤ g_k(x) ≤ aU_k + β_k·(x − c),

  with β_k the computed gradient. Its error bound, times r, is folded into
  aL_k and aU_k.

Tightness against wave 3 (`retry/cmp_bounds.py`, log `logs/cmp_bounds.log`).
The table gives the median gap between the sampled minimum of g_k over a box
and the lower bound, over 64 boxes × 24 objective rows. The boxes have
relative width ρ and lie around the eg_int_s optimum.

| ρ | wave 3 (natural ∩ mean value) | natural | Taylor model (this work) |
|---|---|---|---|
| 0.3 | 7.69 | 7.69 | 2.44 |
| 0.1 | 1.17 | 2.72 | 0.061 |
| 0.03 | 0.115 | 0.834 | 0.0075 |
| 0.01 | 0.013 | 0.270 | 0.0018 |
| 0.003 | 0.0016 | 0.084 | 0.00055 |

The sampled minimum overstates the true minimum, so at small ρ the gaps are
inflated by the sampling. The ratio of the wave-3 gap to the Taylor-model gap
is 3.2 at ρ = 0.3, 19 at ρ = 0.1, 15 at ρ = 0.03, 7.1 at ρ = 0.01 and 2.9 at
ρ = 0.003. So the Taylor model is 15–19 times tighter at the medium sizes
0.1 and 0.03, and about 3–7 times tighter at the other sizes. The same
sampled minimum enters every column, so its overstatement also lowers the
ratios at small ρ; by how much was not measured.

### 3.2 Floating-point arithmetic with explicit error bounds

The production model (`egfast.Fast`) computes the term data and moment sums
in plain double precision and bounds the error explicitly; the derivation is
in the module docstring. In summary:

- **Rigorous exp (`fexp`).** Argument reduction x = m·ln2/64 + r with a
  Cody–Waite split of ln2/64 (the split is checked exactly with Fractions).
  A degree-6 Taylor polynomial for e^r (|r| ≤ 0.0055) and the 50-digit table
  of kan_iv give relative error below 2.2·10⁻¹⁵, enclosed with factors
  1 ± 4·10⁻¹⁵. No libm result is used.
- **Term data.** Every float constant (a, μ, γ, s) has relative error ≤ 2u,
  with u = 2⁻⁵³.
  - Per element, |t̃ − t| ≤ 3.1u(|μ̃| + |s̃c| + |t̃|).
  - |Ẽ − E| ≤ dE = 1.01Σ_i|γ̃_i|[(2|t̃_i| + δt_i)δt_i + (d + 5)u(|t̃_i| + δt_i)²].
  - |w̃ − w| ≤ |ã|·(half-width of the exp enclosure)·(1 + 4u) + (1.02dE + 4u)|w̃|.
- **Moment sums.** Formed with einsum. The error bound is the propagated
  data error plus (M + 3)u Σ|·|, which holds for any summation order, with or
  without FMA. All derived quantities get a further relative slack of 10⁻¹²
  (about 9000u).

`egtm.Model` is an **independent interval-arithmetic version** of the same
models, the second-order model and the third-order alternative. It uses
outward rounding (one ulp per operation) through `ia.NI`, the exp of
`kan_iv.iexp_pt_fast` (wave 3), and a sum bound of (n + 2)·2u Σ|·|. It shares
none of the float error analysis above and was 3.7–7.7 times slower in these
runs (CPU-time ratios from Section 5: 5.7 for B/A, 7.7 for H/C, 3.7 for I/E).
Replays with it (`EGMODEL=ni`, Section 5) followed the same trees and
certified the same bounds:

- run B (eg_int_s, order 2);
- run H (eg_int_s, final code);
- run I (eg_disc_s, final code). Here there is one exception: in part 1 the
  interval model closed one box one level earlier (55,971 boxes against
  55,973). Its bounds are at times tighter by about 10⁻¹¹.

### 3.3 Natural enclosure

On boxes wider than 1/16 of the domain in some coordinate, every row is also
enclosed by the natural interval extension. Each term's exponent is
separable, so its range is exact up to the error bounds of 3.2. The
intersection with the Taylor bounds is used.

### 3.4 Per-box bound: row bound, domain reduction, LP dual, Farkas test (`egbb.py`)

Let θ = UB − tol be the current cutoff.

1. **Row bound.** lb₀ = max_k (c_k + min over the box of aL_k + β_k·d). The
   box is infeasible if some side row's enclosure misses its bounds.
2. **Domain reduction.** Two rounds of interval propagation on the linear
   inequalities, with outward rounding:
   - β_k·d ≤ θ − c_k − aL_k for the 24 objective rows. This is the objective
     cut; it removes only points with objvar > θ.
   - aL_s + β_s·d ≤ ghi_s and aU_s + β_s·d ≥ glo_s for the side rows. The
     side bounds are rounded outward, so these are relaxations.

   Integer coordinates are rounded inward. If the reduced box is empty, it
   contains no feasible point with objvar ≤ θ.
3. **LP.** min t subject to t ≥ c_k + aL_k + β_k·d and the side-row
   inequalities, over the reduced box, solved with HiGHS (highspy). Only the
   dual vector is used. Weak duality
   (Σ_k y_k)·objvar ≥ Σ_k y_k(c_k + aL_k + β_k·d) + Σ_s z_s·(side row ≤ 0)
   is evaluated in outward-rounded interval arithmetic and minimized over the
   box in closed form, then divided by an interval enclosure of Σ_k y_k. If
   this minimum (the combined value vl) is negative and that enclosure is
   not proved positive, the LP gives no bound (a guard added after review;
   it never acted when runs A–E and G–I were run again with it, Section 10).
   If vl ≥ 0, it is divided by the upper end of the enclosure; this needs no
   guard, because y ≥ 0 and its float sum is positive, so Σ_k y_k > 0.
   A poor LP solution only weakens the bound.
4. **Farkas test.** If the LP is infeasible, a phase-1 LP over the side rows
   and the objective cuts gives a vector z ≥ 0. If Σ_j z_j·row_j(d) > 0 on
   the whole box (checked in interval arithmetic), the box contains no
   feasible point with objvar ≤ θ.

### 3.5 Branching

The search is best-first, with batches of 256 boxes. Continuous coordinates
are bisected; an integer interval [a, b] is split into [a, ⌊m⌋] and
[⌊m⌋ + 1, b]. The split coordinate maximizes the estimated loss of the affine
models, r_i Σ_j |H_ij| r_j + r_i ∂P/∂r_i. Rows are weighted by:

- the LP multipliers when the LP was solved, otherwise the leading objective
  row;
- plus every side row that is not yet proved satisfied on the box.

Without the side-row weights the first version stalled (Section 6).

### 3.6 Coverage argument and the certified value

Every feasible point of the instance lies in one of the following:

- (a) an open box (bounded by the box's key);
- (b) a box closed because its bound reached the cutoff θ in force at that
  time;
- (c) a part removed by domain reduction or the Farkas test, where every
  feasible point has objvar > θ;
- (d) a box proved infeasible.

Children cover their parent; integer splits cover all integers of the
interval. Cutoffs only decrease, and every cutoff is ≥ UB_final − tol. The
certified value is therefore min(UB_final − tol, least open key, bounds of
boxes too small to split). The last set was empty in every run.

- **Resumed runs** add the earlier run's minimum. The saved minimum also
  includes UB − tol at save time.
- **Runs split into parts** (`k K`: the integer coordinate with the largest
  range is split into K consecutive value ranges) report a bound per part. The
  instance bound is the minimum over the parts. The parts use a common
  incumbent, which is valid because the incumbent is a feasible point of the
  whole instance.
- **NaN guard.** A NaN bound is replaced by −∞, so it never closes a box.

### 3.7 Primal points

1. A local minimax solve (SLSQP, integers fixed), started from the listed p1
   point and from the best open boxes.
2. A push into the interior of nearly active side rows; the smallest margin
   in 10⁻¹³…10⁻¹⁰ that certifies is used.
3. A rigorous evaluation on the interval path. The point must lie in the
   inner-rounded box, have integral integer coordinates, and satisfy the side
   rows against inner-rounded bounds.

`retry/verify_primal.py` writes the point to `retry/sol/<name>.retry.sol`,
with objvar set to the 60-digit maximum of the objective rows rounded up at
the 20th digit. It then evaluates the OSIL model at 50 digits with
`open-instances-wave2/small/ev.py`: all three points have zero row and bound
violation.

## 4. Rigor: what the bounds rely on, and the checks

The bounds rely on:

1. **The decoding.** `eg/eg_model.py` asserts the expression structure of
   every row; `egdata.py` asserts common, negative γ per row and the row
   classes. Cross-check (`test_decode.py`): at 30 random points,
   all 28 rows evaluated by osilx at 50 digits lie in both point enclosures
   (interval and fast path). Result: 0 misses in 1680 comparisons.
2. **The analytic expansion and remainder bounds** of 3.1. These are
   elementary; they are stated in the `egfast.py` docstring.
3. **IEEE double arithmetic** with round-to-nearest. The bounds hold for any
   summation order, with or without FMA. `np.nextafter` is used for directed
   steps in the interval code. `ldexp` scaling is exact for normal results.
4. **The exp enclosures.** For `fexp`, the error analysis in the docstring
   and the 50-digit table. For the interval path, the kan_iv exp reviewed in
   wave 3.
5. **The coverage logic** of 3.6 in `egbb.BB.run`.

HiGHS and SLSQP are used only to propose multipliers and points; both are
re-checked rigorously.

Sampling checks (these are not proofs):

- `test_fexp.py`: 11,007 arguments in [−750, 600], compared with 50-digit
  mpmath. 0 enclosure failures; maximum relative width 9.0·10⁻¹⁵.
- `test_models.py`: random boxes of relative width 0.3, 0.03, 0.001 and
  10⁻⁵, with integers fixed or relaxed, 128 boxes × 300 points per size and
  instance. The affine models of both the fast and the interval Taylor model,
  and both natural enclosures, contain the float row values. Result: maximum
  of (model − value) is negative in every case.
- `test_bound.py`: the full per-box pipeline (models, row bound, domain
  reduction with the objective cut, LP dual, Farkas test).
  - Boxes: 48 per instance, near the best point (5 sizes) and uniform
    (3 sizes), with integers fixed or relaxed.
  - Cutoffs: UB + 0.5 and UB + 5.
  - Test points: the centre, 60 random points and 3 local minimizers per box.
  - Requirement: every point that is feasible with margin 10⁻⁹ and has
    objvar ≤ cutoff must lie in the reduced box and have objvar ≥ the box
    bound. Near-misses are re-evaluated at 50 digits.
  - Result with the final code (`logs/test_bound_final.log`): 0 violations
    among 1289, 1999 and 2307 qualifying points for eg_int_s, eg_disc_s and
    eg_disc2_s. The smallest margins (objvar − bound) were 1.6·10⁻⁵,
    4.4·10⁻⁶ and 5.2·10⁻⁶.
  - An earlier run with the second-order-only code (`logs/test_bound.log`)
    also had 0 violations (6598 qualifying points).
  - Limitation: almost all qualifying points come from boxes near the best
    point. Uniform boxes rarely contain feasible points with objvar ≤ UB + 5.

The strongest checks of the floating-point error analysis are the replays
B, H and I (Section 5). In them the interval-arithmetic model, which shares
none of that analysis, reproduced the branch and bound box for box.

- For eg_disc2_s this work ran no replay: about 1.15 million boxes at about
  4–8 times the cost of the fast runs (Section 3.2) was out of budget. The
  independent review later replayed part 1 of run G (i7 ∈ [24, 27], the part
  with the optimum) with the interval model and got the same tree (134,607
  boxes) and the same certified value (review, Section 6), in 5,755 s
  against 1,515 s for the fast run (ratio 3.8). The other seven parts have no
  interval replay.
- That instance uses the same code paths as the other two: continuous
  coordinates with scale 1 as in eg_int_s, and integer coordinates with
  scale 1/10 as in eg_disc_s.

## 5. Runs

All runs: `python3 egbb.py <name> <tol_rel> <time> [save] [resume] [k K]` in
`retry/`. "Order 2" means the second-order remainder only (the code before
the third-order alternative was added; the current code reproduces it with
`EG_ORDER=2`).

| run | instance, tolerance | model | boxes | time | result | log |
|---|---|---|---|---|---|---|
| A | eg_int_s, 10⁻⁹ | fast, order 2 | 66,423 | 401 s | 6.4531031529331155 | `int_1e-9.log` |
| B | eg_int_s, 10⁻⁹ | **interval (egtm.Model)**, order 2 | 66,423 | 2280 s | 6.4531031529331155 (same tree as A) | `int_ni_1e-9.log` |
| C | eg_int_s, 10⁻⁹ | fast, final code | 56,189 | 274 s | 6.4531031529331155 | `int9_final.log` |
| D | eg_disc_s, 10⁻⁶ | fast, order 2, 2 parts | 187,445 + 146,201 | 1655 + 1289 s | 5.7605338559159165 | `disc_p0.log`, `disc_p1.log` |
| E | eg_disc_s, 10⁻⁹ | fast, final code, 2 parts | 62,779 + 55,973 | 726 + 650 s | **5.760539610694994** | `disc9_p0.log`, `disc9_p1.log` |
| F | eg_disc2_s, 10⁻⁶ | fast; 4 parts, order 2 to a checkpoint, then resumed with the final code (parts 1 and 2 split 3 ways) | 453,628 + 1,127,664 | 4408 + 12,661 s (about 70 min wall) | 5.642094937872979 | `disc2_p*.log`, `disc2_p*_r.log`, `disc2_p[12]s*_r.log` |
| G | eg_disc2_s, 10⁻⁹ | fast, final code, 8 parts (i7 in [20,23], [24,27], …, [44,47], [48,50]) | 1,152,830 (36,521–223,449 per part) | 12,378 s (38 min wall) | **5.642100574331458** | `disc2_9_p*.log` |
| H | eg_int_s, 10⁻⁹ | **interval**, final code (replay of C) | 56,189 (same tree as C) | 2113 s | 6.4531031529331155 | `int9_ni3.log` |
| I | eg_disc_s, 10⁻⁹ | **interval**, final code, 2 parts (replay of E) | 62,779 + 55,971 | 2660 + 2373 s | 5.760539610694994 | `disc9_ni3_p*.log` |

Computation per instance (CPU time of the reported runs, single-threaded
processes):

- eg_int_s: 4.6 min (274 s, run C);
- eg_disc_s: 23 min (run E);
- eg_disc2_s: 3.4 h for run G (38 min wall on 8 processes), plus 4.7 h for
  the 10⁻⁶ run F.

The interval replays B, H and I and the ablations come on top.

Run F in detail:

- **Stage 1 (order 2).** Parts 0–3 split i7 into [20, 27], [28, 35],
  [36, 43] and [44, 50]. They ran until their checkpoints at 400 iterations
  (parts 0, 1, 3) and 600 iterations (part 2), processing 100,607, 100,607,
  151,807 and 100,607 boxes.
- **Stage 2 (final code, resumed from these checkpoints).**
  - Part 3 closed after 134,284 boxes; part 0 after 244,366.
  - Parts 1 and 2 were stopped at their 600-iteration checkpoints
    (153,600 boxes each). Their 98,478 and 82,130 open boxes were split
    three ways (`split_ckpt.py`) and finished in about 72,000 and 75,000
    boxes per piece.
  - Every stage and piece certified the same value, UB − tol =
    5.642094937872979, with no open boxes left.

## 6. What did not work, and corrections made during the work

- **Wave 3, for reference.** The wave-3 code (`eg/eg_bb.py`) enclosed each row
  by the natural extension intersected with the mean-value form. On eg_int_s
  it processed 44,111 boxes in 603 s and closed about 800 of them (42,546 were
  left open); its bound was 2.43. By the table in 3.1, the Taylor model is
  15–19 times tighter at medium box sizes (ρ = 0.1 and 0.03) and about 3–7
  times tighter at the other sizes. The new code also adds three things the
  wave-3 code lacked: the LP across the 24 rows, domain reduction, and the
  Farkas test for the side rows.
- **First version: stall in infeasible regions (console only).** In the first
  version, the split scores were weighted by the objective rows only. On
  eg_int_s it processed 24,063 boxes in 240 s and reached only 0.105.
  - **Symptom.** The lowest open boxes were infeasible: every sampled point
    violated a side row. The relaxed integer coordinates i5 and i6 were
    never split.
  - **Cause.** The Taylor remainder of e27/e28 was about 5,000 there
    (Σ|a| ≈ 40,000), so no proof of infeasibility was possible.
  - **Fix.** The side rows not yet proved satisfied were added to the score
    weights (3.5), and the Farkas test was added (3.4). The next run closed
    eg_int_s to 10⁻⁶.

  The log of the failed run was overwritten.
- **Error constants too generous for 10⁻⁹ (corrected).** The first float error
  bounds used dE = 10⁻¹³Σ|γ|(|t| + 1)² and an exp half-width of 10⁻¹⁴. The
  eg_int_s run at 10⁻⁹ then stalled at 6.45310315047, with 146,000 open boxes
  of width about 10⁻¹⁰.
  - **Cause.** Relative to the objective row e12, the LP multiplier of the
    active side row e26 is 22.3 (on a box of half-width 10⁻⁴ around the
    optimum). With the old constants, the per-term error bound on e26 was
    about 6·10⁻¹²|w|, so about 5·10⁻¹⁰ in total (Σ|w| = 78). Multiplied by
    22, this costs about 10⁻⁸ in the bound, more than the whole tolerance of
    6.5·10⁻⁹.
  - **Fix.** The per-element bounds of 3.2 replaced the uniform ones.
  - **Second change at the same time.** The incumbent improved from
    6.4531031635 to 6.4531031594 (smaller push margin, 3.7). This gave the
    cutoff more room below the optimum. The two effects were not separated.

  The rerun (run A) closed in 401 s.
- **An error constant that was too small (corrected; affected results
  discarded).** An intermediate version bounded |t̃ − t| by a uniform
  5·10⁻¹⁵, assuming the float constants had relative error u. They are
  midpoints of one-ulp enclosures, so their error is up to 2u, and the worst
  case under the asserted magnitudes is 8.0·10⁻¹⁵. The following results came
  from that version and **are not used**:
  - a first eg_int_s run at 10⁻⁶ (closed in 166 s);
  - an eg_disc_s run that reached 4.85 in 1060 s;
  - an eg_disc2_s run that reached 1.72 in 1060 s.

  Every reported bound comes from runs started after the correction.
- **Ablation on eg_int_s (10⁻⁶, final code, 900 s limit;
  `logs/abl_*.log`).**

  | variant | boxes | time | result |
  |---|---|---|---|
  | full | 55,903 | 591 s | closed (6.453096706283059) |
  | without domain reduction | 57,499 | 583 s | closed |
  | second-order remainder only | 66,141 | 615 s | closed |
  | without the LP | 125,375 (stopped) | 900 s | 6.4526561, 30,720 boxes open |

  - **The LP is essential near the optimum.** There, objective row e12 and
    side row e26 must be combined.
  - **Domain reduction barely matters** on this instance.
  - **Third order.** The third-order remainder saves 15% of the boxes on
    eg_int_s, but each box costs about 2–3 times more. On eg_disc_s it cut the
    boxes from 333,646 (order 2, 10⁻⁶; run D) to 118,752 (10⁻⁹; run E). On a
    sample of 256 open boxes of the order-2 eg_disc2_s frontier, it closed 52%
    at once, against 3% for order 2 (console only).
- **The interval-arithmetic model** (run B) reproduced run A box for box but
  took 5.7 times longer. It serves as a check, not for production.
- **A capped exp in the interval model (fixed; no effect on run B).** When run
  B started, `egtm.iexp_up` capped its argument at 700, which would
  understate e^ℓ for ℓ > 700. It now returns +∞ there. The cap was never
  reached: for every row, term and box of all three instances,
  ℓ = Σ_i 2|γ_i|s_i|t_i|r_i ≤ 16.97. This bound takes, per coordinate, the
  largest |t_i| over the root box and the root half-width as r_i, and is
  computed in exact arithmetic (`retry/check_ell_bound.py`). Run H used the
  fixed code, and a rerun of run B with it followed the same tree
  (Section 10).
- **Not tried: envelopes of the individual exp terms.** The task suggested
  bounding each term by its convex/concave envelope on the box. This was not
  implemented. Any per-term bound sums the 97 terms' errors in absolute value,
  which is the weakness of the natural enclosure. At the eg_int_s optimum, Σ|w|
  is 8.6 times |g| on the active objective row e12, and about 900 times the
  Gaussian part of the active side row e26 (Σ|w| = 78 against −0.083). The
  Taylor model keeps the cancellation in G, ∇, H and the cubic coefficients
  and leaves only the remainder in absolute value. This is a design argument,
  not a measured comparison.

## 7. Literature and novelty

Examined:

- **The MINLPLib pages** of the four instances (fetched 2026-09-30; Section 1).
  No listed dual bound closes eg_int_s, eg_disc_s or eg_disc2_s. SCIP closes
  eg_all_s.
- **A. Göß, R. Burlacu, A. Martin, "Parabolic approximation & relaxation for
  MINLP"**, J. Glob. Optim. 94 (2026) 951–996 (local copy
  `literature/papers/go2026-parabolic-approximation-relaxation-for-minlp/`;
  arXiv 2407.06143). Their Table 17 reports runs with SCIP 8.1 and Gurobi 11
  (8 threads, 4 h limit, values printed to one decimal).
  - **Reading of the columns.** The headers read "primal value | dual
    value", but the numbers fit only the reverse order for these
    minimization problems. For example, eg_disc_s (optimum 5.7605) shows
    3.6 | 5.8, and 3.6 cannot be a primal value. Many runs show "inf" in the
    second column, which fits a run without a primal solution. The values
    below use the reverse reading: first column dual, second column primal.
  - eg_int_s: SCIP on the original model finishes in 9085.1 s with both
    values 6.5, i.e. it reports the instance solved;
  - eg_disc_s: SCIP stops at the time limit with dual 3.6 and primal 5.8.
    This SCIP entry carries an asterisk: the paper excludes the instance
    from its SCIP evaluation because it caused numerical and/or memory
    errors;
  - eg_disc2_s: SCIP stops at the time limit with dual −1.1 and primal 6.3;
  - Gurobi reaches the time limit on the original model of all three.

  So eg_int_s had already been solved by a floating-point solver run
  (8 threads, SCIP's tolerances). The result here for eg_int_s is a rigorous
  certificate, not the first solution.
- **A. Göß, "Clash of MINLP relaxations: piecewise linear vs. global
  parabolic"**, arXiv 2603.16505 (2026). Appendix B, Table 4 lists dual-bound
  improvements over the MINLPLib values; it has no eg_* entry.
- **A. Cristofari, G. Di Pillo, G. Liuzzi, S. Lucidi**, J. Optim. Theory Appl.
  209 (2026) 38 (local copy). It gives best-known primal values only
  (6.4531, 5.7605, 5.6421, 7.6578).
- **C. D'Ambrosio, "Solving well-structured MINLP problems"**, habilitation
  thesis, Université Paris 13 (local copy
  `literature/papers/rovatti2014-optimistic-milp-modeling-of-non/`). It
  reprints "A storm of feasibility pumps for nonconvex MINLP", whose tables
  include the eg_* instances with primal (feasibility-pump) results only.
- **Web searches.** Two queries ("Bram Schoonen MINLP model collection eg_*
  Gaussian surrogate"; "eg_disc2_s OR eg_int_s MINLPLib dual bound") found no
  other dual bounds. No paper describing the origin of the models was found.

Novelty, qualified:

- **eg_disc_s and eg_disc2_s.** Within this search, the bounds above are the
  best known dual bounds, and both closures appear to be new.
- **eg_int_s.** The bound is, as far as found, the first certificate with
  outward rounding; the instance itself was reported solved by SCIP 8.1.

An unsuccessful search does not establish novelty. The methods are standard:
Taylor models with interval remainders, LP relaxations of affine models, FBBT,
and Farkas certificates. The contribution is their application to these
GP-type minimax rows with the cancellation kept and with tracked rounding.

## 8. Commands run (targeted only; no project-wide checks, no CI)

All from `open-instances-wave3/eg/retry/`, with
`OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1` and `timeout`:

- **Exploration and comparisons.**
  - `python3 explore.py <name> <starts> 0` for the three instances
    (`logs/explore_*.log`).
  - `python3 cmp_bounds.py` (`logs/cmp_bounds.log`).
- **Certificates.**
  - `python3 egbb.py eg_int_s 1e-9 1800 logs/int_1e-9.npz` (run A).
  - `EGMODEL=ni python3 egbb.py eg_int_s 1e-9 5400 logs/int_ni_1e-9.npz`
    (run B).
  - `python3 egbb.py eg_int_s 1e-9 3600 logs/int9_final.npz` (run C).
  - `python3 egbb.py eg_disc_s 1e-6 3600 logs/disc_p$k.npz - $k 2` (run D) and
    `python3 egbb.py eg_disc_s 1e-9 5400 logs/disc9_p$k.npz - $k 2` (run E),
    for k = 0, 1.
  - Run F (eg_disc2_s, Section 5):
    - `python3 egbb.py eg_disc2_s 1e-6 3600 logs/disc2_p$k.npz - $k 4` for
      k = 0..3, stopped after 400–600 iterations; their last checkpoints
      were copied to `logs/disc2_p${k}_o2.npz`;
    - resumed with the final code:
      `python3 egbb.py eg_disc2_s 1e-6 5400 logs/disc2_p${k}_r.npz logs/disc2_p${k}_o2.npz`;
    - parts 1 and 2 were stopped again at their 600-iteration checkpoints
      (copied to `logs/disc2_p${p}_r600.npz`), split three ways
      (`python3 split_ckpt.py logs/disc2_p${p}_r600.npz 3 logs/disc2_p${p}s`),
      and resumed (`logs/disc2_p${p}s${k}_r.log`).
- Run G: `python3 egbb.py eg_disc2_s 1e-9 3600 logs/disc2_9_p$k.npz - $k 8`
  for k = 0..7.
- Replays: `EGMODEL=ni python3 egbb.py eg_int_s 1e-9 9000 logs/int9_ni3.npz`
  (run H) and
  `EGMODEL=ni python3 egbb.py eg_disc_s 1e-9 9000 logs/disc9_ni3_p$k.npz - $k 2`
  (run I).
- **Ablations.** `python3 egbb.py eg_int_s 1e-6 900` with `EG_NOLP=1`,
  `EG_NOFBBT=1`, `EG_ORDER=2`, and none (`logs/abl_*.log`).
- **Checks.**
  - `python3 test_fexp.py`, `python3 test_models.py`,
    `python3 test_decode.py 30` (`logs/test_fexp.log`, `logs/test_models.log`,
    `logs/test_decode.log`).
  - `python3 test_bound.py <name> 6 1` (an earlier version of the code,
    `logs/test_bound.log`) and `python3 test_bound.py <name> 6 7`
    (final code, `logs/test_bound_final.log`).
  - `python3 verify_primal.py <name> <npz>` for the three instances.
  - `python3 summary.py` (`logs/summary.log`): every piece of every run in
    Section 5 reports no open boxes, and the minimum over pieces, including
    the closed parts recorded in resumed checkpoints, is the stated bound.
- **After review (2026-10-01; Section 10).**
  - `python3 check_ell_bound.py` (`logs/check_ell_bound.log`).
  - `python3 check_fexp_r.py` (`logs/check_fexp_r.log`).
  - `python3 cmp_bounds.py`, output compared with `logs/cmp_bounds.log`
    by `diff`.
  - `logs/guard/run_guard.sh`: runs A–E and G–I again with the guarded
    `egbb.py` through `python3 check_guard.py <egbb.py arguments>`, with the
    original arguments, `EGMODEL`/`EG_ORDER` settings and no checkpoint
    file, and with time limits of 3600–9000 s, never below the original ones
    (`logs/guard/*_guard.log`). Then `python3 logs/guard/compare.py`
    (`logs/guard/compare.log`).

## 9. Files

All under `open-instances-wave3/eg/`; nothing from wave 3 was edited.

| file | content |
|---|---|
| `retry/egdata.py` | arrays from the wave-3 decoder, extra structure assertions, float evaluator |
| `retry/egtm.py` | interval-arithmetic (NI) natural enclosure and Taylor model (second order and the third-order alternative) |
| `retry/egfast.py` | fast rigorous version: `fexp`, per-element error bounds, second/third-order remainders |
| `retry/egbb.py` | per-box bound (row bound, domain reduction, LP dual, Farkas), best-first B&B, parts, resume, primal polish |
| `retry/split_ckpt.py` | splits a checkpoint into K files for parallel resumption |
| `retry/summary.py` | collects the certified value of every run piece from the logs (`logs/summary.log`) |
| `retry/explore.py` | float local search per integer combination (heuristic) |
| `retry/verify_primal.py` | writes `retry/sol/<name>.retry.sol` and checks it at 50 digits on the OSIL model |
| `retry/test_*.py`, `retry/cmp_bounds.py` | the checks of Section 4 and the comparison of 3.1 |
| `retry/check_ell_bound.py`, `retry/check_fexp_r.py`, `retry/check_guard.py` | checks added after review (Section 10): exact bound on ℓ, exact check of the `fexp` argument reduction, counting wrapper for the `dual_value` guard |
| `retry/logs/guard/` | the reruns with the guard (`*_guard.log`), their script `run_guard.sh`, and `compare.py` with its output `compare.log` |
| `retry/logs/` | run logs, checkpoints (`*.npz`), MINLPLib page extract, exploration results (`explore_*.npy`) |
| `retry/logs/` (superseded) | `test_int.log`, `disc_1e-6.log`, `disc2_1e-6.log`: runs of the version with the too-small error constant (Section 6), not used (their checkpoints were deleted); `int_o3_1e-6.log`: a first 10⁻⁶ run of the final code, the same as `abl_full.log` |
| `retry/sol/` | the three primal points |

## 10. Revision after review (2026-10-01)

The independent review
([`../../reviews/eg-retry-review.md`](../../reviews/eg-retry-review.md),
round 1, verdict **verified**) listed minor items in its Section 1. Each was
checked here before anything was changed. No bound, primal value or closure
claim changed. Labels: **by hand**; **exact** (rational arithmetic);
**rerun** (code run again and its output compared with the original log).

1. **CPU time of eg_int_s (Section 5).**
   - Issue: the text said "7 min (run C)".
   - Check: `logs/int9_final.log` ends with `time 274s`, as in the run
     table. The 401 s (6.7 min) of `logs/int_1e-9.log` belong to run A.
   - Change: "4.6 min (274 s, run C)".
2. **Justification of the exp cap (Section 6).**
   - Issue: the text bounded ℓ by 100 on eg_int_s using |γ| ≤ 46.4,
     |t| ≤ 4 and r ≤ 1.5. These figures give only
     ℓ ≤ 7·2·46.4·4·1.5 ≈ 3,900.
   - Check (exact): `check_ell_bound.py` bounds ℓ for every row and term by
     Σ_i |γ_i| s_i (ub_i − lb_i) max_{x_i ∈ [lb_i, ub_i]} |μ_i + s_i x_i|
     over the root box. This covers every box of every run, since box
     centres lie in the root box and radii are at most the root half-widths.
     The maximum is 16.964 for each of the three instances, which share
     their data (`logs/check_ell_bound.log`). This agrees with the review's
     ℓ ≤ 17. (The largest |t| is 3.0.)
   - Change: Section 6 now states ℓ ≤ 16.97 for all three instances and
     how it is obtained. The conclusion is unchanged: the cap at 700 was
     never reached and had no effect on run B. Rerun: run B with the current,
     uncapped `iexp_up` reproduced the original log line by line (item 3).
   - Note: the class `egtm.FastModel` still caps ℓ at 700. No script uses
     it (checked with `grep`), and the same bound applies to it.
3. **Guard in `egbb.BB.dual_value` (code change).**
   - Issue: for a negative combined value vl, the bound vl/Σ_k y_k used the
     lower end S.lo of the enclosure of Σ_obj y_k without checking
     S.lo > 0. `egtm.isum` subtracts an absolute 10⁻³⁰⁰, so S.lo ≤ 0 when
     Σ y_k is about 10⁻³⁰⁰ or less. The old code then returned a positive
     bound, which is invalid (S.lo < 0), or stopped with
     `ZeroDivisionError` (S.lo = 0). The earlier test `ys.sum() > 0` does
     not exclude this.
   - Check (by hand): the LP has a free variable t with cost 1 and
     coefficient −1 in each objective row, so dual feasibility makes
     Σ_obj y_k = 1 up to HiGHS's tolerances. The case is not expected.
   - Change: if vl < 0 and S.lo ≤ 0, `dual_value` now returns −∞ (no bound
     from this LP). The branch vl ≥ 0 (division by S.hi) is unchanged. The
     new code can therefore differ from the old one only where the old one
     returned an invalid bound or stopped with an error.
   - Rerun: runs A–E and G–I were run again with the guarded code through
     `check_guard.py`. It counts every call with S.lo ≤ 0, which includes
     every call where the guard acts, and changes nothing else. Runs A, B
     and D used `EG_ORDER=2`; B, H and I used `EGMODEL=ni`. Results
     (`logs/guard/compare.log`):

     | run | pieces | rerun log equal to the original apart from timings | `dual_value` calls | calls with S.lo ≤ 0 |
     |---|---|---|---|---|
     | A (eg_int_s, fast, order 2) | 1 | yes | 33,645 | 0 |
     | B (eg_int_s, interval, order 2) | 1 | yes | 33,645 | 0 |
     | C (eg_int_s, fast, final code) | 1 | yes | 28,437 | 0 |
     | D (eg_disc_s 10⁻⁶, fast, order 2) | 2 | yes, both | 167,211 | 0 |
     | E (eg_disc_s, fast, final code) | 2 | yes, both | 59,630 | 0 |
     | G (eg_disc2_s, fast, final code) | 8 | yes, all eight | 583,148 | 0 |
     | H (eg_int_s, interval, final code) | 1 | yes | 28,437 | 0 |
     | I (eg_disc_s, interval, final code) | 2 | yes, both | 59,628 | 0 |

     - Equal logs mean, at every logged iteration, the same numbers of
       processed and open boxes, the same incumbent, bound, LP count and
       statistics, and at the end the same certified value and primal
       point.
     - Over all 993,781 calls, the smallest float sum Σ_obj y_k was
       0.9999999999999998 and the smallest S.lo was 0.9999999999999938.
     - So the guard never acted, the old code never took the invalid path
       in these runs, and every reported result is unchanged.
     - Runs A, B and D also confirm that the current code with
       `EG_ORDER=2` reproduces these order-2 runs (Section 5).
     - The reruns ran 18 processes at once at a load average of 27–44.
       They took 803–3,823 s per piece, 39,373 s (10.9 CPU-hours) in
       total, about 65 min of wall time.

   - Not rerun: run F (the superseded 10⁻⁶ run of eg_disc2_s, 4.7
     CPU-hours with resumed and split checkpoints; no reported bound
     depends on it), the ablations and `test_bound.py`.
4. **Table 17 of Göß, Burlacu and Martin (Section 7).**
   - Check: Table 17 on page 988 of the local PDF (`pdftotext`) and in
     `fulltext.md`. The headers read "primal value | dual value". The
     numbers fit only the reverse order: 3.6 | 5.8 for eg_disc_s (optimum
     5.7605) and −1.1 | 6.3 for eg_disc2_s (optimum 5.6421). The SCIP entry
     of eg_disc_s carries an asterisk. Appendix B.5 says that eg_disc_s was
     excluded from the SCIP evaluation because it "caused numerical and/or
     memory errors".
   - Change: Section 7 states the reading used and the asterisk. The
     Gurobi bullet now says that Gurobi reaches the time limit on the
     original models. The old wording "solves none of the three" was loose:
     on the model type "both" of eg_int_s, Gurobi stopped after 989.0 s
     with "inf | inf".
5. **Tightness ratios (Sections 3.1 and 6).**
   - Check: from `logs/cmp_bounds.log`, the ratio of the wave-3 gap to the
     Taylor-model gap is 3.2 (ρ = 0.3), 19 (0.1), 15 (0.03), 7.1 (0.01)
     and 2.9 (0.003). Rerun: `cmp_bounds.py` printed output identical to the
     log (`diff`).
   - Change: both places now give the ratios. "15–20 times" became "15–19
     times at ρ = 0.1 and 0.03, about 3–7 times at the other sizes".
6. **`fexp` docstring (`egfast.py`; comment only).**
   - Issue (review): the docstring bounds |r̃ − r| by 10⁻¹⁸, but where
     x − mL1 is inexact the bound is about 1.2·10⁻¹⁸.
   - Check (by hand): the docstring did not say why x − mL1 is exact. It is
     exact for every argument, by Sterbenz's lemma. L1 is below ln2/64 by a
     relative 2.75·10⁻¹⁰. The computed m (`rint`, ties to even) satisfies
     (|m| − ½)·ln2/64 ≤ |x| ≤ (|m| + ½)·ln2/64 up to a relative error of
     about 10⁻¹⁶, far below that margin. So mL1/2 ≤ x ≤ 2mL1 for m ≥ 1, and
     likewise for m ≤ −1; m = 0 is trivial. The bound 10⁻¹⁸ therefore
     holds, and the review's inexact case does not arise. Without the
     exactness the bound would be 1.3·10⁻¹⁸. Both are far inside the slack:
     the final factors are 1 ± 4·10⁻¹⁵, while about 1 ± 2.1·10⁻¹⁵ is
     needed.
   - Check (exact): `check_fexp_r.py` (`logs/check_fexp_r.log`) used
     152,472 arguments. Of these, 52,472 are float neighbours of reduction
     boundaries (every boundary with |m| ≤ 300 or |m| > 64,340, and 2% of
     the others); 100,000 are uniform in [−700, 700]. x − mL1 was exact in
     every case, and the largest |r̃ − r| was 4.3·10⁻¹⁹.
   - Change: the docstring now gives the Sterbenz step and the bound
     without it. This is a comment; no result can change.
7. **Other updates.** The status line refers to the review. Section 4
   mentions the review's interval replay of eg_disc2_s part 1. Section 3.4
   mentions the guard. Sections 8 and 9 list the new commands and files.
8. **Optional nits of the confirmation review.** The confirmation review
   ([`../../reviews/eg-retry-confirm-r1.md`](../../reviews/eg-retry-confirm-r1.md),
   verdict **verified**) found items 1–7 applied correctly and listed two
   optional nits in its Section 3. Each was checked here before the change.
   Both are wording only; no bound, primal value, closure claim or other
   number of a result changed.
   - N1 (Section 3.4, step 3). Issue: "If that enclosure is not proved
     positive, the LP gives no bound" is broader than the code. Check (by
     hand, `egbb.BB.dual_value`): the code returns −∞ only when vl < 0 and
     S.lo ≤ 0. For vl ≥ 0 it divides by S.hi whatever S.lo is, which is
     valid because y ≥ 0 and the test `ys.sum() > 0` give Σ_k y_k > 0.
     Change: step 3 now says that the LP gives no bound if the combined
     value vl is negative and that enclosure is not proved positive, and
     adds why the case vl ≥ 0 needs no guard. Item 3 above already
     described the code exactly.
   - N2 (Sections 3.2 and 4). Issue: Section 4 said that an interval replay
     of eg_disc2_s would cost "6–10 times" as much, and Section 3.2 said
     "4–8 times slower". Check: the final `time` lines of the run logs give
     CPU-time ratios of 2280/401 = 5.7 (B/A), 2113/274 = 7.7 (H/C) and
     (2660 + 2373)/(726 + 650) = 3.7 (I/E). The review's replay of
     eg_disc2_s part 1 took 5,755 s against 1,515 s (3.8; review,
     Section 6). Change: Section 3.2 now gives the measured range 3.7–7.7
     and the three ratios. Section 4 now says "about 4–8 times" with a
     reference to Section 3.2, and gives the review's replay times. Timings
     remain indicative only (shared machine).
   - Header: the status line now cites the confirmation review and its
     verdict.
