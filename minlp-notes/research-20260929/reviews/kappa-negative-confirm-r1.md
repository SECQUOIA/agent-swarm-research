# Confirmation review (round 1) of `theory-bangbang/kappa-negative.md`

Date: 2026-09-30. Referee: fresh and independent. I did not write the note,
its scripts or the round-1 review. Scope: check each finding of
`reviews/kappa-negative-review.md` (F1–F6) against the revised note; recompute
every number that changed; judge the items the reviser declined; check that
nothing was strengthened. Checks and logs:
`reviews/kappa-negative-confirm-r1-checks/` (`c_two.py`, `c_exact.py`,
`c_kink.py`, `logs/`).

Labels: **exact** means rational arithmetic in my own code; **float** means
floating-point screening in my own code; **40 digits** means mpmath. I
imported the author's code once, only to test its data convention (F2). All
other numbers come from my own implementations, written from the note's
definitions.

## Verdict

**Minor fixes needed (text only).** All six findings were addressed, and
every changed number I recomputed agrees with the note. My checks include an
independent float sweep of all 7 × 14 close-switch grids, which matches the
author's sweep on all 97 grids that both runs completed. They also include
exact re-checks of the revised Section 9.1 and 9.2 rows and of the `q < 0`
numbers. The new proof that the maximal recursion cannot break when the
reduced Hessian is positive definite is correct. The declined items are
reasonable and are stated as limitations.

Three small inaccuracies remain, plus two wording nits (Section 3 below).
None affects a theorem or a main conclusion.

## 1. Check of each finding

| finding | what the revision did | my check | result |
|---|---|---|---|
| F1 (thin-layer reading) | thin-layer reading and "sign of `eta^X_1` predicts" withdrawn; three regimes reported; 7 × 14 `N`-sweep; per-grid `e_2`, `eta_hat_1` table; cascade logged | own KKT search (enumeration of monotone patterns with an exact 2-D box QP per pattern, coordinate descent and then a ±12-stage 2-D scan, full KKT check) and own recursion from [E, Lemma 10]; all 7 configurations × 14 grids (float) | **Reproduced.** All 97 grids where the author's search returned a point agree exactly in `s_1`, `s_2`, fractional stages, break offset, `e_2` and `eta_hat_1` (`logs/sweep_compare.log`). The author's data gap (`eta^X_1 = -0.085`, `N = 7000`) is filled: KKT point found, no break (`e_2 = 0.163`, `eta_hat_1 = 0.071`). Break ranges −2…+5 (42 strong grids), 5 of 14 for −0.275, none for −0.085, −0.040 and +0.160: confirmed. Layer-law numbers re-derived from [E, Section 2.5] (`s_b/s_1 = exp(-2 gamma/(Delta|eta|))`): 3e-6, 1.9e-3, 5.6e-3, 4.2e-4. Break times 5.7e-4…6.7e-4, 5e-4…9e-4 and 2e-4 confirmed from the logs. Cascade log: moves of 1–4 stages, plus one of 33, and still broken after six liftings on all 12 grids. Confirmed. |
| F2 (decimal jump times) | `ktoy._piece` reads `Fraction(repr(t_i))`; Sections 9.1–9.3 rerun; old logs kept | author's `data()` against the documented rule for 7 `(t_1, t_2)` × 15 grids `N = 500 … 16000`; exact KKT points and plain gaps at `(0.7, 1.3)`, `kappa = -0.5` | **Fixed.** 0 mismatches (`logs/ktoy_data_check.log`). Exact: `N = 500` and `1000` are bang-bang with gap exactly 0, so they are exact with no window. `N = 2000` is bang-bang with change stages 598 and 778 and gap 1.532 `h^2` (597: 0.714, 778: 0.818). `N = 4000` has fractional stage 1196 (`u = -0.873`) and gap 0.8766. All as in the table (`logs/exact.log`, `logs/exact_two_N4000.log`). I did not rerun the 9-node branch and bound; the author and the round-1 reviewer each certified that optimum with their own code. The "non-optimal KKT point" episode is now attributed to the earlier instance only. |
| F2 (Section 9.2 rows) | six `(0.65, 1.35)`, `(0.7, 1.3)` rows rerun | exact, own window minimization (own derivation of the window residual), with `tau_j` from my own float KKT points at `N = 16000` | **Reproduced.** No failing stage at `(0.65, 1.35)`, `N = 1000, 2000` or at `(0.7, 1.3)`, `N = 1000`. Failing stages 1430: 0.0536, 722: 0.1541 and 1336: 0.0422 `h^3`. `K = 1` windows exactly 0 (`logs/kink.log`). The values quoted for the first-version instance (1.0048, 0.3644, 0.2644, 0.1549) match `logs/pre_revision/kink.json`. |
| F2 (Section 9.3 history) | "only `(0.55, 1.45)` and `(0.45, 1.55)` changed" | compared `logs/pre_revision/close*.json` with the new logs | Correct; the `(0.65, 1.35)` configurations did not change. |
| F3 (convexity) | convexity paragraph; weights lowered in 9.1–9.4, Summary item 6 and the status table | float eigenvalues of my own Hessian (`N = 1000`, 9 representative configurations); identity `J = h sum (x_t-a_t)^2/2 + Phi + (k_2/2) x_N^2 + ((k_1-k_2)/2) x_m^2 + (h^2/2) sum kappa_t u_t^2` re-derived | **Confirmed.** +0.5005 and +0.0005 `h^2` for `kappa = 0.5` and `0`; 979 negative eigenvalues for `kappa = -0.5`; rising configurations positive definite; falling configurations have exactly one negative eigenvalue (`logs/convexity.log`). The new short proof is correct. The recursion is the dynamic-programming step for the tail second variation plus `h|sigma_s| omega_s^2/2`. With `d_t = 0`, the coefficient `h^2 m_t/2` of `omega_t^2` after minimizing over the later controls is a Schur complement of a positive definite principal submatrix of `H + diag(h|sigma|)`, so `m_t > 0`. The 9.4 remark is also right: with fixed `x_N`, `k sum h x_t u_t` equals a constant plus `-(k/2) h^2 sum u_t^2`. |
| F4 (a)–(d) | qualifiers restored | read Summary items 1, 2 and 6, Section 4 and Theorem 4.3(b) | **Fixed.** (a) The `O(N)` heading is conditional and labelled heuristic. (b) "Need" is restricted to `kappa`-limited families with the node optimum's costate as exit slope. (c) [W, Proposition D] is stated as an upper bound. (d) The `A = 0`, constant `H_xx` condition and the need for data that are not smooth in time are stated. |
| F5.1 | "≈ `h^3/4`" | 40 digits, own matrix `G_ij/h^2 = h(N-1-max(i,j)) + 1/2` | **Confirmed.** Relative excess 2.4455% (`N = 10`), 0.15417% (`N = 40`), 0.024673% (`N = 100`, float); `≈ 2.47/N^2` holds (`logs/spectraG.log`). |
| F5.2 | "linear in `u`" | algebra | Correct. |
| F5.3 | one-coordinate estimate; condition `|kappa_tau| <= 4 eta_L` | re-derived | **Correct.** The decrease is `h^2 kappa^2 (a-b)^2/(8 eta_L)`, with `a = ubar_n - u_-` and `b = u_+ - ubar_n`. The exact comparison condition is `|kappa|(a-b) <= 4 eta_L a`, which `|kappa| <= 4 eta_L` implies. The one-coordinate value is a *lower* bound on the bracket, so it cannot prove the inequality. The note's "a leading-order estimate, not a bound" is the right hedge. |
| F5.4 | "plausible, not checked" | read | Fixed. |
| F5.5 | `q < 0` margins; "certificates coincide" corrected | exact, own code | **Reproduced.** `N = 200`: 1.32 (stage 55), 2.77 (stage 54). `N = 400`: 0.76 (stage 111), 2.21 (stage 112). `N = 2000`: `V` inner end −0.04752150757886112 (the same for both toys); outer node anchored at `z(r)` with no stage loss; bounds +1.76283 (`q < 0`) and +0.76509 (`kappa = -1`) `h^2` (`logs/exact_qneg.log`). |
| F5.6 | ratios, `N`-dependence, margins, exact cover | tally of `logs/eps.json`; read the cover code | **Confirmed.** `kappa = -1`: inner ratios 4.316–4.567, outer 2.625–3.497. 25 of 44 margins below `-epsilon` (15 by 2.9e-11 to 1.9e-7, 10 by 2.4e-6 to 1.2e-3). 42 of 44 counts equal the prediction. `epscover` uses the same rationalization (`limit_denominator(1e12)`) as `epsexact`. One sentence is still wrong; see R2. |
| F5.7 | A− caveat | read | Fixed (caveat in Summary item 2, Section 5.4 and the status table). |
| F5.8 | bang-bang claim qualified | `H_tt = h^2 (h(N-1-t) - 2)` re-derived from the `k`-split identity (`k = 3`, `phi2 = -2`); the state box is never active (`|x| <= 2 < 3`) | Correct. |
| F5.9 | "proof by locality, sketch level" | read | Fixed. |
| F6 | WSB 2014 cited; cluster framing withdrawn; novelty qualified | read the local copy (`literature/papers/wechsung2014-the-cluster-problem-revisited`: abstract, Section 3 with Table 1, Theorem 2, conclusion) | **Fixed.** The paraphrase is accurate: for `beta = 2`, the number of boxes is independent of `epsilon`, and it is 1 when `K <= lambda_1/8` (Table 1). The novelty paragraph now treats the log count as generic. |

## 2. Declined items and strengthening

- **A− lifted interval (F5.7), no denser check.** Acceptable. The note now
  says plainly that this is float screening at finitely many `v` and not a
  certificate on `V`.
- **No exact certificates at `N = 4000` (two-switch toys) or for the
  breaking close-switch configurations.** Acceptable as a limitation, and
  Section 9.1 says "not run". However, the status table now claims more than
  this; see R1.
- **Sweep data gap at `N = 7000`.** Acceptable. My independent search found
  the KKT point; there is no break.

I compared the revision with the round-1 review's quotations of the first
version and read the material added in revision. The new statements are
labelled float, observation or heuristic, and the numbers I checked are
right. The new mathematics (convexity paragraph, positive-definite proof,
Remark 2.3 estimate) is correct. The withdrawals are explicit. The only places
where the revision says more than its evidence supports are R1 and R3.

## 3. Remaining problems

**R1 (minor; overstatement introduced in revision).** The status table row
"exact certificates of `f*` on toys" says "`f* = J(zbar)` on every
single-switch grid and every documented two-switch grid". Section 9.1 did not
run the certificate at `N = 4000` for `kappa = -0.5`, on three grids with
plain gaps 0.87–0.88 `h^2`. So `f* = J(zbar)` is not established there. This
matters because the note itself records a case where the search returned a
non-optimal KKT point. Summary item 3 and Section 3 ("certified optimum on
every tested grid") are correct only if "tested" means "where the certificate
was run". *Fix:* write "every two-switch grid where the certificate was run
(`kappa = -0.5`, `N <= 2000`; `kappa >= 0` automatically)".

**R2 (minor; the note's own table contradicts it).** Section 4 says: "For
`kappa = -0.5` the counts do not depend on `N` at fixed `epsilon / h^2`". The
table gives 3 nodes at `epsilon/h^2 = 1e-1` for `N = 1000` and 4000, but 2
for `N = 8000`. The prediction is also 2, so the explanation is the same as
for `kappa = -1` (the position of `ubar_n`). The round-1 review checked only
`N = 1000` and 4000. *Fix:* give the exception, or state the `ubar_n`
dependence for both toys.

**R3 (minor; caveat missing in Section 7.2).** Section 7.2 says that for the
strongly negative cases, "the observed break times (`2e-4` to `9e-4` after
the switch on grids where the second switch is fractional) agree in order of
magnitude with that law". Two things are missing:

1. Section 9.3's caveat. The law's matching scale `s_1` is not determined,
   and agreement requires `s_1` between 0.1 and 0.5, which differs by a factor
   of 5 across the three configurations. So this is a consistency
   observation, not a test.
2. The qualifier "at larger `N`". At `N = 1000` the second switch is
   fractional for `(0.5, 1.5)` and `(0.45, 1.55)`, but the breaks lie 0 and
   `-3.7e-4` from `theta_1` (`logs/sweep.json`, `break_time_minus_theta1`).

*Fix:* copy the 9.3 wording into 7.2.

**Nits (optional).**

- Section 9.3 says "There `eta_hat_1 <= -0.34`", but the `N = 8000` value is
  −0.337. Write "≤ −0.33".
- The status table says the moderate case is "decided by the excess carried
  in from the second switch". The threshold `e_2 <= 0.08` was chosen after the
  fact on 14 grids, and the only vertex-grid break (`N = 8000`, `e_2 = 0.079`)
  lies just below it. "Observed to coincide with small `e_2`" matches the
  evidence.

## 4. Literature examined by this referee

- Local: `literature/papers/wechsung2014-the-cluster-problem-revisited/fulltext.md`
  (abstract, Sections 1 and 3 including Table 1, Section 4 with Theorem 2,
  conclusion).
- Cited notes at the relevant places: [E] `extension-n2.md` Section 2.5
  (layer law), Section 5 (Lemma 10, Corollary 11); the round-1 review.
- No web searches. That the novelty statements are qualified was checked by
  reading; I did not extend the search, and an unsuccessful search does not
  establish novelty.

## 5. Commands run (targeted only)

All commands were run from `reviews/kappa-negative-confirm-r1-checks/` with
`OMP_NUM_THREADS=1` and explicit `timeout`. No project-wide verification was
run, CI was not inspected, and nothing was committed.

1. `python3 c_two.py <cfg> 1000,1500,…,16000` for the 7 configurations
   (background, about 1 min each) → `logs/sweep_<cfg>.log`; comparison with
   the author's `sweep.json` → `logs/sweep_compare.log` (97 agree; 1 is the
   author's gap).
2. `python3 c_exact.py two qneg` → `logs/exact.log`, `logs/exact_two.json`,
   `logs/exact_qneg.{log,json}`. The first run stopped at the `kappa = -1`
   toy, `N = 200`, because that toy has a fractional KKT point there and no
   bang-bang one. The grids were then restricted to what is checked
   (`N = 2000` for that toy), and the part was rerun.
3. An inline run of the `two` part at `N = 4000` →
   `logs/exact_two_N4000.log`.
4. `python3 c_kink.py` → `logs/kink.{log,json}` (exact, about 2 min).
5. Inline: float eigenvalues → `logs/convexity.log`; 40-digit spectra →
   `logs/spectraG.log` (a first attempt had a wrong diagonal in my own
   matrix and was discarded); data-convention test of the author's
   `ktoy.data` → `logs/ktoy_data_check.log`; tally of the author's
   `logs/eps.json` (printed only).
6. A mistake: to stop a slow `find /` search for old copies of the note, I
   used `pgrep -f` with a pattern that also matched the issuing shell, and
   `kill` then stopped that shell. No files were affected. The search was
   repeated over the repository and `/tmp` only; it found no old copy of the
   note.
