# Confirmation review (round 1): `covering-upper-half.md` after revision

Date: 2026-09-30. Note checked:
[`../theory-decomposition/covering-upper-half.md`](../theory-decomposition/covering-upper-half.md),
the version revised after the first review
([`covering-upper-half-review.md`](covering-upper-half-review.md)). I also checked its
scripts and logs in [`../theory-decomposition/covering/`](../theory-decomposition/covering/)
and the cited parts of [D] (`decomposition-certificates.md`: Definition 1.2,
Lemmas 1.3–1.5, Theorem 2.5) and [E] (`extension-adaptive.md`: Proposition B.1).

I did not write the note or the first review. I edited no note and no root file,
and I committed nothing. My scripts and logs are in
[`covering-upper-half-confirm-r1-checks/`](covering-upper-half-confirm-r1-checks/).
All runs were single-threaded (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`).
They are targeted checks of this note only. I ran no project-wide verification and did
not consult CI.

## Verdict: fixes needed (minor)

All seven review items (R1–R7), the trivial item and both optional items were
addressed. I rechecked each one from scratch, by hand and by rerunning or
recomputing the numbers. None was declined. The revision states nothing beyond
what it proves or computes. The new results (Proposition 1.3, Lemma 1',
Corollaries 3.2 and 3.3) are correct. The theorems of the first version still
stand.

Two minor problems remain. Both need one sentence each.

1. **Proposition 5: the sufficient condition does not fix the cell slopes**
   (Section 6). As worded, it is false for other slopes.
2. **Section 5: "The failure is not a thinning of the band width"** conflicts
   with the `kappa = 2 beta` case that the revised paragraph now describes.

The remaining points (Section 3 below) are trivial wording and rounding issues.
There is also one optional improvement: Corollary 3.3 holds with the factor 2 in
place of `2^{w+1}`.

## 1. The review items, rechecked

**R1 (Lemma 2 sharpness). Fixed correctly.** I verified the two-kink family by
hand.

- `U = -J(s - 1/2 + delta)_+` is concave, and `L = J(-1/2 + delta - s)_+ - J(1/2 + delta)` is convex.
- `U - L` is concave and vanishes at `s = ±1`, so `L <= U` on `[-1, 1]`.
- `w(0) = J(1/2 + delta)` (for `delta < 1/2`), and both kinks lie inside `[-1/2, 1/2]`, so `Delta_U = Delta_L = J + M`.
- The ratio `(2J + 2M)/(8J(1/2 + delta) + 8M)` gives `0.4856, 0.4990, 0.4999, 0.5000` for the four logged `(M, delta)`. My hand computation gives the same values.

The example `U = L = -M s^2/2` gives `Delta_U = 2Mh` and `Delta_L = 0`, so `b >= 2` holds.
"Whether (4, 2) or any pair below (8, 8) is valid is not settled" is accurately
stated. The rerun of `check_kink_concentration.py` is identical to the log. The
first 9 lines are identical to the review's pre-revision rerun, so "earlier lines
unchanged" holds. (Wording nits: T1 below.)

**R2 (framing of Proposition 4). Fixed correctly.** Both withdrawn sentences are
gone. The Summary, the Status table and Sections 4, 5, 7.3, 7.4, 8 and 9 now say
the same thing: placement by one-edge band brackets fails; R3 and `bd` place cells
edge by edge and provably work. The LP figures quoted as evidence (naive cells
fail even with LP-optimal values; `bd` and B.4 cells pass) match
`logs/check_naive_failure.log`. I reran that script (see below). (One loose
sentence about `bd`: T2 below.)

**R3 (optimality of `1/(2n)`). Fixed correctly. The new Proposition 1.3 is
correct.** I checked each step.

- Step 1: `|r_e| <= c w_e` makes every bracket `<= 0`, and `gap >= 0`.
- Step 2: exact iff each `F_t^phi` is minimized at `x*_{V_t}`, for any fixed global minimizer `x*`.
- Step 3: the split terms of `±c a` in bag `t` are `±c(-1)^{d(t)+1} b_t`, where `b_t = sum_{u in ch(t)} w_u + w_t >= 0` and `b_t(x*) = 0`. So `Delta_t >= c b_t`.
- Step 4: `sum_t Delta_t = m` and `sum_t b_t = 2 sum_e w_e`.

I checked the chain of copies. With `P h^2 >= 1`, `U_e = 0` and `V_e = s^2`, so
`w_e = s^2`. The continuum formula `w_e = P s^2/(P + e - 1)` is the series-spring
value. The remark that (1.1) is also *sufficient* on trees is correct: `F_t^psi + c b_t = (F_t^psi - c b_t) + 2c b_t`, so one of the two conditions implies the other,
and the DP split of `F - 2c sum w` is exact.

- The rerun of `check_chain_discount.py` is identical to the log. The script is dated after its log (16:56 vs 16:43); the rerun shows that the change did not affect the output.
- Independent check (`indep_leafwise_and_discount.py`, Part B, my code, full enumeration, bags with private variables, 120 random trees): the DP split of `F - 2c* sum_e w_e` makes `psi ± c* a` exact to `8.9e-16`; `c* >= 1/(2n)` in every case (`2n c*` in `[1.000, 3.873]`). An LP over all splits is feasible at `(1 - 1e-6) c*` in 120 of 120 cases and at `1.01 c*` in 0 cases. This confirms both directions of the remark on a family the author did not test.

**R4 (per-level admissibility). Fixed correctly.** `eta_0 = eps` and, for
`j >= 1`, `eta_j = 2 eta_{j-1} < 2m(x)`, so `eta_j <= max(2m, eps)` and
`eps + max(2m, eps) <= 2(eps + m)` in both cases.

**R5 (reduced band). Mostly fixed; one sentence remains (item M2).**

- The closed forms hold. The unconstrained minimizer is `s2 = kappa s1/(kappa - beta)`, which is feasible iff `|s1| <= 1 - beta/kappa`. There the value is `-kappa beta/(kappa - beta) s1^2`. Beyond, the value is `kappa(|s1| - 1)^2 - beta`.
- The width `beta(kappa - 2beta)/(kappa - beta) s1^2` is correct.
- The one-line "no affine function" proof is valid, including for `kappa = 2 beta`.
- The new section of `check_prop4.py` reproduces: `2.4e-6`, the concavity intervals, and widths `3.56e-2`, `1.4e-17` and `3.96e-3`. The first 36 log lines are identical to the review's pre-revision rerun.

**R6 (tolerance sentence). Fixed correctly.** From the log, the ten failing
settings are `n = 6, 8` (both `eps`, both grids) and `n = 4` at `eps = 1e-3`
(both grids). The largest decrease there is `1.14e-2 -> 1.09e-2` (4.4%). The
passing-setting decreases are as quoted. The plateau ranges
`2.0e-3–2.5e-3`, `1.1e-2–1.3e-2` and `2.3e-2–2.5e-2` are right. So is
"`2.52e-3 -> 2.50e-3`, others agree to three digits". The rerun of the review's
fine-grid script matches the review's log exactly apart from timings (diff with
timing fields stripped: no differences). (Count nit: T4 below.)

**R7 (Lemma 1'). Fixed correctly. Lemma 1' is correct.** Step 1
(`F_t + sum_u U_u - U_t = g_t`) and Step 2 (the `W_t` coefficient
`sum_u(theta'_u + D') + 2D' - theta'_t = 0`, with nonnegative coefficients and
(F2)) are identities and inequalities at a single point `z`. Alignment puts each
`z_{S_u}` in `cl D_u(B)`. So the leafwise bound follows bag by bag, and each edge
appears once as a child and once as its own separator. The `eps/2 + eps/2`
accounting in Proposition 5 is right.

- The author ran no computation for Lemma 1'. My Part A tests it directly. It uses closed cells that share endpoints, so the pieces are two-valued at boundaries. Leaves are products of closed cells, overlap at boundaries and carry their own errors. Private variables are included, and there are three perturbation modes. Result: 0 violations in 300 instances, largest excess `2.2e-16`, ratio up to 1.0000 (the bound is attained).
- Sensitivity check: the same test with the bound's discount tripled gives 90 violations in 300. So the test can detect a wrong bound.

**Trivial (Remark 1.1). Fixed correctly.** `theta_t - theta_u = (E_t - E_u)/n >= 1/n`.

**Optional: Corollary 3.2 (`bd` coarsens R3). Correct.** The validity part of
Theorem 3 gives `g_{e,D} <= B(D)` on every dyadic cell. The interior case uses
Lemma 2 with `h = 8nr`; the boundary case uses `Delta_U + Delta_L <= 4G + 4Mr` and
`osc <= 2Gr + (5/2)Mr^2`. Induction on the level then shows that every cell `bd`
splits is also split by R3. My rerun of `check_bd_coarsening.py 16385` is
identical to the log: 47,782 cells, coarsening in all 8 runs. (Rounding nit: T3
below.)

**Optional: Corollary 3.3. Correct, but it can be sharpened (item O1).** It
matches Theorem 2.5 of [D], whose proof works bag by bag and for each `eta`.
Projecting to `S_e ⊂ K_t` and subdividing intervals by `ceil(sqrt(M_e/alpha))` is
right. The second display follows from Theorem 3 by summing.

**Optional: Ruozzi–Tatikonda.** Title, authors and dates (v1 17 Feb 2010,
v3 1 Dec 2012) match the arXiv abstract page, which I also checked. (Paraphrase
nit: T6 below.)

**Refusals and non-reruns.** No item was declined. The note says that
`check_graded_split.py`, `run_paths.py` and `check_naive_failure.py` were not
rerun.

- `path_cells.py`, which the last two import, is dated 15:57. That is after `run_paths.log` (15:37) and `check_naive_failure.log` (15:43).
- The review's `run_paths` rerun (16:36) came after that change and was identical.
- I reran `check_naive_failure.py 129 257` (5 min 42 s). Its output is identical to the author's log. So all figures quoted from these logs are current.

## 2. Remaining problems

**M1. Proposition 5, sufficient condition: state the cell slopes (Section 6).**
Proposition 5 fixes the slopes ("for fixed cell slopes, `l_r` equals the best
value over intercepts"). The proof then bounds the separator terms by the proof of
Theorem 3 with discount `D'`, which needs the *balanced minimizers* of the
closed-cell brackets (the paragraph after Lemma 1'). The two bulleted conditions
say nothing about slopes, and with other slopes the conclusion can fail.

Example: `n = 1`, root `-lambda s + M s^2/2`, leaf `lambda s + M s^2/2` (`f* = 0`,
`w = M s^2`), exact leaves (so the second condition holds), and constant minorants.
The cell of half-width `r` around 0 costs about `2 lambda r` in `l_r`. The
R3-adapted cells there have `r` of order `sqrt(eps/M)/n`. So for
`eps` small against `lambda^2/(n^2 M)`, the certificate does not prove `eps`. (This
is the phenomenon of Proposition 2.6 of [D].)

Fix: add to the first condition "with the cell slopes of the balanced minimizers of
the closed-cell brackets (half-width `D' w_e`), or any slopes whose closed-cell
bracket is at most `eps/(2n)`; the intercepts are then maximal."

**M2. Section 5, "The failure is not a thinning of the band width."** The revised
paragraph now says that for `kappa = 2 beta` the reduced band has *zero* width on
`|s1| <= 1/2`. That is a thinning to zero, so the lead sentence holds only for
`kappa > 2 beta`. The point of the paragraph is still right: for `kappa > 2 beta`
the reduced band keeps width of order `s1^2` yet contains no affine function, so
the obstacle is its shape. Fix: "For `kappa > 2 beta` the failure is not a thinning
of the band width", or "not only a thinning".

## 3. Trivial points (optional to fix)

- **T1 (Lemma 2 wording; Summary, Status, Sections 3 and 9).** The two-kink family *approaches* ratio 1/2 (it is `< 1/2` for every `delta > 0`). The Summary and the Status table say "reaches". Also, "the constant 8 is at most a factor 2 too large" is right for the coefficient of `w(c)/h`, or for one common constant. For the coefficient of `M h` alone, the known lower limit is 2, a factor 4 below 8. Section 3 states both limits correctly; the short forms could say "the coefficient of `w(c)/h`".
- **T2 (Section 5, "What it shows").** "These criteria refine wherever the margin `w_e` is small compared with the curvature times the squared cell size" describes R3 and B.4. `bd` refines only where the sliver of half-width `w_e/(2n)` admits no affine function within `eps/n`. Near a pinch point where `psi_e` is locally affine, it does not refine. Suggest naming R3 and B.4 in that sentence.
- **T3 (Section 4 after Corollary 3.2, Section 10 table, Revision entry).** "`g - B <= -7.1e-5`" rounds the wrong way. The logged maximum is `-7.08e-5` (D2, `eps = 1e-3`), which is larger than `-7.1e-5`. Write "`<= -7.0e-5`" or "`< -7e-5`".
- **T4 (Section 7.4).** "in one case by an order of magnitude": `n = 2` drops by more than 10 at both grids (`6.07e-3 -> 3.59e-4` at `m = 129`, `6.64e-3 -> 4.15e-4` at `m = 257`). That is two settings.
- **T5 (notation).** `D'` denotes the discount `1/(3n+1)` and also cells: in Lemma 1', `max_{D in P_e} sup_{cl D}(r_{e,D} - D' w_e)`; in Proposition 5, `l_{u,D'}`. `L_t` denotes both the lower value function (Section 0, Theorem 1) and the leaf family (Lemma 1', Proposition 5). Renaming the discount (for example `delta'`) and the leaf family would avoid misreading.
- **T6 (Section 8).** The note says Ruozzi–Tatikonda give "a characterization of the optima through graph covers". The abstract uses graph covers to characterize when the conditions for convergence to a *global* optimum are too restrictive. Suggest "graph covers to explain the limits of these guarantees".

## 4. Optional improvement

**O1. Corollary 3.3 holds with the factor 2 in place of `2^{w+1}`.** In the proof
of Theorem 2.5 of [D], each `x in E(eta)` has a leaf `B_t ∋ x_{V_t}` with
`alpha a_i^{B_t}(x) <= eps + eta` for every `i in K_t`. Since `a_i >= d_i^2` ([D],
proof of Proposition 2.4), `x_i` lies within `sqrt((eps + eta)/alpha)` of one of the
*two* endpoints of `(B_t)_i`. Projecting to the one coordinate `S_e` therefore needs
only `2|L_t|` intervals of length `l'`, not the `2^{|K_t|} |L_t|` cube projections.
Hence `sum_e N_e <= 2 ceil(sqrt(M/alpha)) N_dec(eps)`. This removes the factor
exponential in the width from the comparison with certificate size in "What this
settles". The corollary as stated is correct, only looser.

## 5. Checks run

Scripts of the note were run from `theory-decomposition/covering/`; my scripts from
`reviews/covering-upper-half-confirm-r1-checks/`. Logs are in
`reviews/covering-upper-half-confirm-r1-checks/logs/`. All runs were
single-threaded. These are targeted checks only: no project-wide verification, and
no CI result is reported here.

| Command | Log | Result |
|---|---|---|
| `python3 check_kink_concentration.py` | `rerun_check_kink_concentration.log` | identical to the author's log; first 9 lines identical to the pre-revision rerun |
| `python3 check_chain_discount.py` | `rerun_check_chain_discount.log` | identical to the author's log (script dated after its log; output unaffected) |
| `python3 check_prop4.py` | `rerun_check_prop4.log` | identical; first 36 lines identical to the pre-revision rerun |
| `python3 check_bd_coarsening.py 16385` (73 s) | `rerun_check_bd_coarsening.log` | identical; 47,782 cells; max `g - B = -7.08e-5`; coarsening in 8 of 8 runs |
| `python3 check_naive_failure.py 129 257` (5 min 42 s) | `rerun_check_naive_failure.log` | identical to the author's log (which predates the last change to `path_cells.py`) |
| `diff` of `covering/logs/rerun_review_indep_naive_fine.log` with the review's `indep_naive_fine.log`, timing fields stripped | none | no differences |
| `python3 indep_leafwise_and_discount.py` (my code, 2 s) | `indep_leafwise_and_discount.log` | Lemma 1': 0 violations in 300, max excess `2.2e-16`, max ratio 1.0000. Proposition 1.3 remark: 120 trees with private variables, `psi ± c* a` exact to `8.9e-16`, `2n c*` in `[1.000, 3.873]`, LP feasible at `(1 - 1e-6) c*` 120/120 and at `1.01 c*` 0/120 |
| `python3 sensitivity_leafwise_disc3.py` (my code) | `sensitivity_leafwise_disc3.log` | with the discount tripled in the bound: 90 violations in 300, so the Lemma 1' test can detect a wrong bound |

By hand: all steps of Proposition 1.3 and its remarks, Lemma 1', Corollaries 3.2
and 3.3 (against Theorem 2.5 of [D] and Proposition B.1 of [E]), the R1 family and
the `w = 0` example, the R4 case analysis, and the R5 closed forms.

Scope: finite grids and floating point (HiGHS). My Part A and Part B instances are
small (2–5 bags, 3–6 separator values, a binary private variable per bag).

## 6. Literature

I checked only the arXiv abstract page of Ruozzi–Tatikonda (arXiv:1002.3239) to
confirm the new citation. I ran no new novelty searches. The note's novelty wording
is qualified ("I did not find ... in short searches"; "does not establish
novelty"), and the revision did not strengthen it.
