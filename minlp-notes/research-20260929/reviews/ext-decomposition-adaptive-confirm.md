# Confirmation review: revised `extension-adaptive.md`

Date: 2026-09-30. Note checked:
[`../theory-decomposition/extension-adaptive.md`](../theory-decomposition/extension-adaptive.md),
revised after [`decomposition-adaptive-review.md`](decomposition-adaptive-review.md). I also
checked its scripts and logs in
[`../theory-decomposition/adaptive/`](../theory-decomposition/adaptive/). I did not write
the note or the first review. I did not edit the note and did not commit anything. My
scripts and logs are in
[`ext-decomposition-adaptive-confirm-checks/`](ext-decomposition-adaptive-confirm-checks/).
All runs were single-threaded (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`)
and are targeted checks of this note only. I ran no project-wide verification and did
not consult CI.

## Verdict: fixes needed (minor)

**All nine requested fixes are applied correctly.** I checked each one from scratch and
recomputed every number that changed. Where the reviser disagreed with the first
review (the cause of the RC sensitivity, issue 6), my checks support the reviser. The
new widened-test RC trajectories are reproducible under the perturbations that broke
the first version. Withdrawn claims are clearly marked in the text, in Section E and
in Section F.

Two new statements are slightly wrong and should be fixed. Both are quick to fix, and
neither changes a conclusion:

1. **Proposition B.6(b) (new): the displayed constant fails when `h_0 > 2`.** This
   happens for small `alpha`. The cause is inherited from the level count in
   Theorem B.2(b) (item R1 below).
2. **"At most about `22 n`" split leaves per bag per level** (status table, Sections A.3
   and A.4, command table). The note's own table gives `25.9 n` at `n = 16`
   (item R2 below).

A few wording points remain (Section 3). None changes a statement.

| # | Issue in the first review | Fix in the note | Verdict |
|---|---|---|---|
| 1 | staircase: "`C` depending only on `alpha`" | B.4 bullet and Summary corrected; `Phi_2` added to Theorem B.3; new Proposition B.6 | **correct**; one edge case in the new display (R1) |
| 2 | flat bag, reading (R1), (QG) remark | (R1) redefined; (QG) remark says `C` of order `sqrt(w)`; Conjecture B.5 with `Phi_2` | **correct** |
| 3 | obstacle 1 overgeneralized | scoped to level-synchronous refinement in A.4, A.5, Summary, status table, D | **correct** |
| 4 | C.2 attributes the excess to slopes | starting points stated; split table; `x^(-1) = 0` runs | **correct**; all numbers reproduced |
| 5 | RC `n = 8`: lower bound reached the tolerance | A.5, C.3, Summary, D say the incumbent rule failed | **correct** |
| 6 | RC `n = 16` trajectory not reproducible | cause identified as dropped touching pairs; RC rerun with widened test; old values withdrawn | **correct**; the reviser's diagnosis is supported |
| 7 | Theorem A.5(a) wording | slope bound for every pass that runs | **correct** |
| 8 | wording and numbers | several restatements | **correct**, except "at most about `22 n`" (R2) |
| 9 | one-sided grid check | two-sided KKT and value check | **correct** |

## 1. Fix-by-fix check

### Issues 1 and 2: `Phi`, `Phi_2`, Proposition B.6, reading (R1)

**Theorem B.3 with `Phi_2`.** The proof already shows that
`sum_{i in K_t} d_i^2 <= Q_t(z)`, so `z_{K_t}` is within Euclidean distance
`sqrt(Q_t(z))` of a vertex of the minimizing leaf. The `2^{|K_t|} |L_t|` vertices are
therefore a Euclidean covering set with radius `sqrt(e(z)/alpha)`, `e = alpha Q_t`.
`N^{(2)} >= N` holds because `|.|_inf <= |.|_2`. Correct.

**Proposition B.6(a), one flat bag.** I re-derived every step.

- *Lower bound on `N_dec`.* For every `y`, Lemma 1.4 of [D] gives a leaf with
  `alpha q_B(y) <= eps`. So `y` lies in the inward orthant of a Euclidean ball of
  radius `r = sqrt(eps/alpha)` around one vertex. These orthants have total volume at
  most `V_d r^d` per leaf. For `d = 1` the bound `sqrt(alpha/eps)/2` is attained.
- *`e = eps` is admissible*, and cubes of side `2 sqrt(eps/alpha)` give the bound on
  `Phi`.
- *The uniform grid* of side `1/ceil(sqrt(alpha d/(4 eps)))` has relaxed minimum
  `-alpha d h^2/4 >= -eps`.
- *The `Phi_2` lower bound* follows from `e <= eps` on `E(0)` and the volume of a
  Euclidean ball.
- *`Gamma(d/2+1) >= (d/(2e))^{d/2}`* holds for all `d`, since
  `Gamma(x+1) >= int_x^inf t^x e^{-t} dt >= x^x e^{-x}`.
- *The ratio limits* `4^d/V_d` (for `Phi`) and `1/V_d` (for `Psi`) are right.

**Proposition B.6(b), staircase.**

- *The admissible family.* It gives `sum_t e_t = m(x) + eps (A - D) <= eta + eps`, and
  `e_t >= 0` because `P >= 1 > eps`. The covering counts are:
  - `(0,1)`: `e = eps`;
  - `(0,0)` and `(1,1)`: radius `|y|_2/sqrt(alpha) >= |y|_inf` for `alpha <= 1`;
  - `(1,0)`: `e >= 2|y|^2`.

  All are correct.
- *The bound `ceil(u)^d + 3 <= 4 (alpha/eps)^{d/2}` for `eps <= alpha/4`* is correct.
  So is the bound `sup Phi_2 >= K 2^{-(d+2)} M`: every admissible family has
  `e_t <= eps` on the fat slice, because the other terms are `>= 0`.
- *The three comparisons with Theorem B.2(b).* I checked them symbolically and
  numerically. The three inequalities with `Gamma` hold for `d = 1..400`, with margin at
  least `e^{-0.73}`.

There is one gap, stated as R1 below.

**Numbers.** My own evaluation (`indep_phi_bounds.py`, written from the note's
formulas, not from `check_phi_loss.py`) reproduces every quoted value:

- staircase: `2.43, 4.01, 5.52, 7.74` and `3.29, 4.65, 5.13, 5.44`;
- flat bag: `2.68, 4.38, 5.89, 8.07` and `2.98, 3.65, 3.85, 3.97`;
- the review's `0.05, 0.19, 1.06, 130, 5.8e4`.

`check_phi_loss.py` reruns to an identical log.

**Reading (R1), the (QG) remark, Conjecture B.5.**

- (R1) now allows `C` to depend on `w`. Theorem B.2(c) correctly notes that the
  refutation survives, because `d` is fixed while `K` grows.
- The (QG) remark now says that the upper half is established with `C` of order
  `sqrt(w)`, which is what Theorem 3.4 of [D] gives. The remark says openly that `C`
  independent of `w` is not known.
- Conjecture B.5 now uses `Phi_2` and allows `C` to depend on `w`. It is still labelled
  a conjecture. The note states correctly which half becomes stronger (the lower half,
  which is Theorem B.3) and which becomes weaker. The (QG) consistency argument via
  `Phi_2 >= |T| 2^{-(w+1)}` is right.
- No claim was strengthened here beyond what is proved.

### Issue 3: scope of Proposition A.6

Obstacle 1 in A.5, the new paragraph after Proposition A.6, the Summary, the status table
and Section D all restrict the statement to level-synchronous refinement. The new
paragraph names the step that needs it: step 2 of the proof, where every other bag
still has leaves of level `<= i`. Rules that refine in another order are stated as open.
Correct.

### Issue 4: slopes versus incumbent (C.2)

- `run_ls.py` starts the oracle and zero-slope runs at `x*`, and the `c = 0` exact-slope
  runs at `0 = x*`. C.1 and C.2 now say so.
- I reran `check_slope_incumbent.py 8 1e-4`; the log is identical apart from timings.
- The note's `n = 16` log agrees exactly with the first review's independent code in
  columns A–D (`check_slope_vs_incumbent_n16.log`). I recomputed column E at `n = 16`
  (`exact_slopes_x0zero_n16.py`): 287,423 and 279,384, as stated.
- The ratios 2.322, 2.424, 2.517, 2.495, the "about twice" and "1.9 and 1.7 times LS",
  the incumbent offsets `0.27–0.76 eps`, and `nu = 1.16e-2` all match the logs.

### Issue 5: RC at `n = 8`

`rc_zero_eps1e-6_tol.log` and the first-version log are identical in every round line;
only timings differ. At rounds 15, 17, ..., 23, `l_r = -9.206e-7 >= f* - eps`, while
`UBD = 1.013e-6`. The failure is due to the incumbent rule, as the note now says in
A.5, C.3, the Summary and D.

### Issue 6: RC at `n = 16`

**The reviser's diagnosis is supported by my checks.**

- *Rerun.* `check_rc_sensitivity.py 16 0` reproduces its log exactly.
- *Pairs added by the widened test.* In the round-1 partition, all 164 (leaf, cell)
  pairs that the `1e-12` widening adds miss each other by only 1–2 ulp
  (`1.1e-16`–`2.2e-16`). Consecutive cells of one separator also have floating-point
  gaps of up to `2.2e-16` (`rc_robustness.py pairs`). So these are pairs that touch in
  exact arithmetic, and dropping them raised `l_r`.
- *Validity.* Widening can only add configurations, so it keeps `l_r` a lower bound.
- *LS is unaffected.* LS with exact slopes at `n = 16`, `eps = 1e-6` gives size 153,584,
  `l_r = -5.794424e-7`, 887,743 processed and split 413.7 with both `tol = 0` and
  `tol = 1e-12` (`ls_tol_regression.py`; the note had only an inline run).

**The new trajectories are reproducible.** This was the core of the first review's
complaint, and the note now quotes new cycle values. I re-coded the RC loop
(`rc_robustness.py`) around the author's `shell_partition` and `dp` and ran five
variants per seed:

- `tol = 1e-12` (baseline);
- `tol = 1e-10`;
- `x0 = ±1e-12` in every coordinate;
- the round-1 centre moved by `1e-9` in coordinate 2 (at `+1`);
- the round-1 centre moved by `1e-9` in coordinate 6 (interior).

All five give the same gap, incumbent and centre error to the printed digits:

- seed 0, rounds 0–17: cycle 0.714/0.971 from round 16, `UBD = -0.1377`;
- seed 1, rounds 0–12: cycle 0.533/0.557, `UBD = 0`.

The baseline matches `rc_random_n16_eps1e-4_tol.log`. So the values in A.5 are
reproducible under these perturbations, which was not true of the first version's.
Checking C.3 against the logs:

- the local-solve runs give the same stops and sizes (368,172 and 367,750; processed
  1,645,240 and 1,642,045);
- only the round-1 and round-2 bounds changed slightly.

The first version's values (`1.6e-2`/`2.9e-2`, `UBD = -0.1356`) are withdrawn in A.5, and
the old log has an appended correction line.

*Nuance (optional).* With the widened test, `1e-9` moves of the `±1` coordinates still
change the round-1 pair count (25,612 becomes 25,673–25,718). The shell partition is
therefore discontinuous in a centre on the box boundary, as the first review said, but
this does not change `l_r`. "The cause is the dropped pairs" is right for the `l_r`
jumps.

### Issue 7: Theorem A.5(a)

Part (a) now bounds `nu_p` for every pass that runs, and the proof derives it before
using whether the pass stops. Part (b) cites it for passes that stop later. The
recursion `a_p^2 <= 2 Lambda/c_g + gamma a_{p-1}` is re-derived correctly. No constant
changed. Correct.

### Issue 8: wording and numbers

`log_numbers.py` recomputes these from the author's logs.

- `|x^cons - x*|_2/(s_i sqrt(n))` is 2.65, 4.03, 5.38, 5.69, 5.84, so "about
  `5.8 sqrt(n)` from `n = 32` on" is right.
- Plateau `21 n` at `n = 32` (levels 7–11: 21.1–22.0) and `20 n` at `n = 64` (levels
  8–12: 19.8–20.3). Correct.
- Restarts versus a single oracle pass: 6.52, 6.43, 5.03, 5.33. Correct.
- B.5 item 3 and the Summary now describe a loss in the available bound, not a shown
  thinning of the bands. Correct.
- The RC random log's correction line is appended, and the command table says round 21.
  Correct.
- The random-`c` localization is 3.11–7.23 from level 6 on, and at most 11.01 at levels
  3–5. Correct.
- The "at most about `22 n`" wording is new and is contradicted at `n = 16` (R2).

### Issue 9: staircase exactness

`check_staircase.py` now checks the KKT conditions of the strictly convex, separable
leaf problem at the clipped stationary point. That is a sufficient, two-sided
certificate of the minimum. It also evaluates the relaxed function directly. My rerun
gives an identical log: KKT violation 0, value difference `<= 2.2e-16` in all 30 rows.
Correct.

## 2. Remaining problems

**R1 (minor; new display, inherited cause). Proposition B.6(b) fails for `h_0 > 2`.**

- *Cause.* B.6(b) takes `L = log2(1/h_0) + 2` from Theorem B.2(b), where
  `J + 1 <= log2(1/h_0) + 2` is used. But Lemma 3.1 of [D] has
  `J = max(0, ceil(log2(s0/h)))`. When `h_0 > 2`, that is when
  `alpha^2 K d < eps/2`, the shell count is `(J + 1)(4/theta)^d = (4/theta)^d`, while
  `log2(1/h_0) + 2 < 1`, possibly negative.
- *When it happens.* The hypotheses `alpha <= 1`, `eps <= 1/2` allow this, for
  `alpha < 1/(2 sqrt(K d))`.
- *Scan.* I scanned 1,120 cases of `(alpha, eps, K, d)`, with `alpha` from 1 down to
  `1e-3` (`indep_phi_bounds.py`). In 27 of them, all with `h_0 > 2`, the ratio of
  the B.2(b) size bound to `K 2^{-(d+2)} M` exceeds the displayed constant by up to a
  factor 1.36. One example: `alpha = 0.1`, `eps = 0.5`, `K = 2`, `d = 1`, `L = -0.82`.
- *Fix.* With `L` replaced by `J + 1 = max(0, ceil(log2(1/h_0))) + 1`, or by
  `max(1, log2(1/h_0) + 2)`, the bound holds in every scanned case. Make the same
  replacement in Theorem B.2(b).
- *Impact.* The claims "absolute `C`" and "`C^{w+1} log(K/eps)`" are unaffected.
  Theorem B.2(c) is also unaffected, because there `h_0 -> 0`.

**R2 (minor; new wording). "At most about `22 n`" is false at `n = 16`.**

- The C.1 table's own "per `n`" column is 8.8, 19.1, **25.9**, 22.7, 22.3. At `n = 16`
  the level-5 value is 413.7 = `25.9 n`.
- The Summary and the C.1 bullet scope the claim to `n = 32, 64` and are fine. The
  status table, Section A.3 ("at most about `22 n` ... effective `rho` of about
  `2.3 sqrt(n)`"), Section A.4 (after the proof) and the command table state it without
  scope.
- *Suggested wording:* "at most about `26 n` for `n <= 64` (`22 n` at `n = 32, 64`); about
  `20–21 n` on the plateau for `n >= 16`". This gives an effective `rho` of about
  `2.3–2.5 sqrt(n)`.

## 3. Wording points (optional)

- **C.1: "17–24 times the final size".** This covers the C.1 restart table
  (16.9–23.5). The C.2 LS runs give 15.5–22.8, so over all LS runs with restarts the
  ratio is about 15–24. Section F item 8 quotes "17–24" without saying which runs.
  "Compared with a single pass with exact slopes" means the oracle pass, which also has
  the exact incumbent. Given issue 4, say so.
- **A.5, `n = 8`: "After the stall the centre stops moving".** The centre does not stop.
  It alternates between two points at sup-distance about `9.8e-4` and `1.22e-3` from
  `x*`, so the error in units of `h_j` grows. "Stops approaching `x*`" would be exact.
  Also:
  - the centre error is `12–16 h_j` at rounds 10–15, not from round 0;
  - the gap cycle is exact from round 15 (round 14 has `1.586e-6`, not `1.54e-6`).
- **A.5, `n = 4`: "stops after 13 rounds".** RC stops at round 13, which is 14 rounds
  counting round 0. C.3 says "at round 13".
- **Summary and status table (Conjecture A.7): "3–7 `s` on random instances".** Add
  "from level 6 on"; A.5 already says so, and the value is up to 11 `s` at levels 3–5.
- **Summary, Proposition B.6 bullet: "`N_dec/Psi` is also at least of order
  `w^{Theta(w)}`".** This holds as `eps -> 0` (limit `1/V_d`) or for
  `eps <= alpha/d^2`, say. For fixed moderate `eps` the proven lower ratio
  `1/(2^d V_d)` is below 1 for `d <= 62`. B.6(a) states it as a limit, which is
  fine.
- **Pointer outside this note.** Section D says that the closed intersection test in
  `../dp_certificate.py` of [D] has not been checked for non-dyadic centres. [D] does
  report such runs: Sections 5.2–5.3, random `c`, certificates centred at an interior
  `x*`. So that open question is concrete and worth a separate check. I did not
  investigate it.

## 4. Commands run

From `theory-decomposition/adaptive/`, reruns of the author's scripts (logs written to my
`logs/rerun_*.log`):

| Command | Result |
|---|---|
| `python3 check_phi_loss.py` | identical to `logs/check_phi_loss.log` |
| `python3 check_staircase.py` | identical to `logs/check_staircase.log` |
| `python3 check_rc_sensitivity.py 16 0` | identical to `logs/check_rc_sensitivity.log` |
| `python3 check_slope_incumbent.py 8 1e-4` | identical to `logs/check_slope_incumbent_n8.log` (timings aside) |

From `reviews/ext-decomposition-adaptive-confirm-checks/`, my scripts (logs in `logs/`):

| Command | Log | Result |
|---|---|---|
| `python3 indep_phi_bounds.py` | `indep_phi_bounds.log` | all quoted Proposition B.6 numbers reproduced; `Gamma` inequalities hold for `d <= 400`; displayed B.6(b) constant fails in 27/1,120 cases, all with `h_0 > 2`; holds with `L -> J + 1` (R1) |
| `python3 rc_robustness.py pairs` | `rc_pairs.log` | 164 added pairs, all 1–2 ulp apart; cell partitions have floating-point gaps up to `2.2e-16` |
| `python3 rc_robustness.py traj 0 17`, `python3 rc_robustness.py traj 1 12` | `rc_robustness_seed0.log`, `rc_robustness_seed1.log` | widened-test RC trajectories identical under all five variants; baseline matches the author's `_tol` log |
| `python3 ls_tol_regression.py` | `ls_tol_regression.log` | LS `n = 16`, `eps = 1e-6` identical with `tol = 0` and `1e-12` |
| `python3 exact_slopes_x0zero_n16.py` | `exact_slopes_x0zero_n16.log` | 287,423 and 279,384 |
| `python3 log_numbers.py` | `log_numbers.log` | numbers of issue 8, C.1/C.2 ratios, random-`c` localization, RC `n = 8` centre errors |

Time: about 12 minutes of single-threaded CPU in total, most of it for the RC
trajectories.
