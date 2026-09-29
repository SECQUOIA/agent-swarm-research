# Adversarial review: robust branching points (boundary immunity and kink competitiveness)

Date: 2026-09-29. Reviewed document:
[`../bb-complexity/robust-branching-points/robust-branching.md`](../bb-complexity/robust-branching-points/robust-branching.md)
("the note"), with its scripts, logs and `results/`. Context used:
`competitive-branching.md` (Theorem 1, Propositions 4 and 4'),
`face-exact-node-complexity.md` (Section 5.3, Propositions 5.4–5.7) and
`branching-point-study.md`.

I had not seen this material before. I did not edit the note and did not
commit anything. All checking code is new and is in
[`robust-branching/`](robust-branching/). It is written from the note's
definitions and does not import the author's scripts. I read the author's
scripts only to find out what they computed (Section 8 lists one place where
the simulated scheme differs from the stated one). No project-wide checks were
run.

## Verdict

Every numbered result holds as stated, except for one parenthetical in
Theorem A(ii). The problems are:

- one false parenthetical ("in fact uncountably many" points with the stated
  constant);
- one wrong formula inside a proof, with no effect on the statement;
- two places where the Summary claims more than the theorems prove;
- several numbers that are Monte Carlo noise or floating-point artifacts;
- one simulation that is labelled as "keyed randomization" but uses a
  slightly different scheme.

One result is **stronger than the note says**: the recentring clamp is
exactly optimal, not "within one split". In 1D it meets the Proposition C
lower bound with equality for every kink.

| Claim | Verdict | Main evidence |
|---|---|---|
| Theorem A(i): every clip schedule `C_Theta` (clamp `theta_B in [theta0, theta1]`, any function of the box path, not of the relaxation point) has an uncountable Lebesgue-null trap set | **Correct** | Proof checked step by step. Alternating trap points of five schedules (fixed, depth, width, position and history dependent) replayed in 400-digit arithmetic: no split lands on `a` in 150 steps |
| Theorem A(ii): `T >= 2K+1` in 1D and with x-only selection | **Correct**; one false parenthetical; one wrong formula in the proof | Holds for all five schedules at `eps = 1e-4 ... 1e-48` and is attained with equality for the fixed clamp 1/5 (35 = 35 at `1e-24`). "(in fact uncountably many)" is false with the stated `K`: for the fixed clamp 1/5 only `a = 1/6, 5/6` qualify (Section 2.2). Proof step 5 writes the McCormick x-only bound as `\|c\| rho(1-rho) w_k^2`; it is `\|c\| rho(1-rho) w_k`. The statement survives, and is conservative by a factor 2 in `K` |
| Theorem A(iii): `T >= theta0^2 \|c\|^(1/2)/(2 eps^(1/2))` with widest-side selection | **Correct** (for schedules that depend only on the x-interval path) | Proof checked. Exact rational count for the fixed clamp 1/5 at `a = 1/6`: 13, 39, 167, 547, 1,513, 4,917, **19,537** at `eps = 1e-2 ... 1e-8`. The width schedule reproduces `check_A2d.log` exactly (15 ... 12,003) |
| Summary wording of Theorem A | **Overstated** | (a) The class is clip schedules, whose fallback is the zone's inner end. It is not "every schedule that ignores where the point sits inside the zone": the midpoint fallback also ignores that position and never traps for `theta <= 1/3` (the note's own remark). (b) The `eps^(-1/2)` claim needs the extra hypotheses of (iii), which the Summary omits |
| Recentring clamp `RC_theta`: definition, safety | **Correct** | `l + max(theta w, 2(p - l))` puts `p` at the child's centre when `p` is at relative distance in `[theta/2, theta)`, and the split stays in `[theta, 2 theta) ⊂ [theta, 1-theta]` for `theta <= 1/3`. The SCIP plugin implements the same rule, and SCIP accepts the suggested point unchanged (`branch.c`, lines 2354–2390) |
| Proposition D(i): `S <= m+2 <= J(theta)+2` | **Correct, and not sharp: in fact `S = J(theta) + 1`** | Short proof in Section 3. Exact check: 14,670 kinks, 5 values of `theta <= 1/3`, `S_RC = J+1` in every case. So `RC_theta` is exactly optimal among `theta`-safe rules, with any information |
| Proposition D(ii): `T <= 1 + 4 theta^-(m+2)/(1-theta) <= 1 + 2/(theta^2 (1-theta) d0)` for every `eps` | **Correct** | Proof checked, including the level-width step for recentring splits. Exact rational counts at `eps = 0`, the supremum over `eps`, on 52 kinks: all within the bound. Examples: 17 at `1/6`, 183 at `3/238`, 3,219 at `1e-3`, 22,703 at `1e-4` (bound 390,626) |
| Theorem B: `E[S] <= A + B log(1/d0)`, the second bound, the lower bound, slope `1/mu` | **Correct** | Proof checked line by line. Constants reproduced. Supersolution slack in closed form: minimum 0.640, 0.765, 1.349, 0.541 for the four windows, matching `chain1d_S.log` |
| Theorem B numbers (2.02 at `a = 1/6` for `[0.1, 0.3]`, and so on) | **Correct** | Nyström solve of the renewal equation and `10^7`-chain Monte Carlo: 2.0252 / 2.0253, 3.3196, 1.9305, 6.3062, 11.878; narrow windows 2.536 and 3.726; slope 0.60435 = `1/mu`. The quoted bounds 16.2 and 29.3 use the weaker of the note's two bounds; its second bound gives 12.5 and 18.1 |
| Proposition C: `S >= J+1` and `T >= 2J+1` for every `theta0`-safe rule | **Correct** | Proof checked. 21,465 exact `(a, eps)` pairs for two rules: no violation. The bound is attained by `RC_theta` for `theta0 <= 1/3`. It is not always attained for `theta0 > 1/3` (for example `theta0 = 0.45`, `a = 0.4`). The note does not claim it is |
| Proposition E: `E[T] >= c log(1/eps)` under widest-side selection | **Correct** | Proof checked. The bound is numerically tiny (0.06–0.58 against simulated means of 100–400), as the note says |
| Conjecture E' | **Properly labelled.** The fitted slopes are 0.18–0.25, not 0.18–0.29 | `10^6` runs per entry. The note's upper end (0.29) comes from 1,000-run noise |
| Keyed randomization: "exactly the same mean" | **Correct for the stated scheme; the simulation used a different one** | With keys per (variable, interval), means agree with independent draws within 2 standard errors on all 42 entries. The author's `sim_kink.py` keys on `(l, u)` only, so an x-split and a y-split on equal intervals share a draw. That scheme has a different mean, for example 5.00 against 5.47 (`a = 3/238`, `eps = 1e-2`) |
| Proposition F and the incumbent-rule statements | **Correct** | Trivial proof checked. 3 nodes with an optimal incumbent in 1D, and with `x` split first on the McCormick family |
| Lemma 0 | **Correct** | — |
| SCIP: default and LP-point runs reproduce the earlier study | **Correct** | 168/168 and 163/163 runs that are optimal in both studies have identical node counts |
| SCIP: MINLPLib ratios and CIs | **Correct** | Recomputed independently for 11 pairs. Ratios agree to 3 decimals, CIs to ±0.01, and p-values to the Wilcoxon variant. Plugin counters reproduced |
| SCIP: plugin rules compared only with each other | **Mostly.** The Summary and Section 7 blur the reference | "Recentring costs nothing measurable (0.94, CI 0.86–1.01)" is against the plugin clip `x_lp` (midpull 0), not SCIP's default. Against `default` it is 0.92 (0.71–1.15) |

## 1. Model, rules and safety (Sections 1.1–1.3, Lemma 0)

- **1D kink.** The open test `alpha (a-l)(u-a) > eps` and the relaxation
  minimizer `a` follow from steps 2–3 of Proposition 4 of the competitive
  note. `N_opt = 2` and `T(R_min) = 3` for `eps < alpha a(1-a)`. In 1D and
  with x-only selection, `T = 2 (#open chain nodes) + 1 <= 2S + 1`. Correct.
- **McCormick family.** I rederived the open test from the envelope. At
  `x = a` the underestimator is `max(-X_u (Y - Y_l), |X_l| (Y - Y_u))`, so
  `LB = -|c| w_y (a-l_x)(u_x-a)/w_x`, with `yhat` at relative position `rho`
  for `c < 0`. The bound does not depend on `b`, provided
  `L > |c| max(b, 1-b)`. Correct.
- **Lemma 0.** (i) `ceil(ln 2/-ln 0.8) = 4`. (ii)
  `ln 2/-ln(1-delta) >= (1-delta) ln 2/delta` holds because
  `-ln(1-delta) <= delta/(1-delta)`. Both correct.
- **SCIP's `k1:a` instance** is `f = 2|x-a| - (x-a)^2`, not the `2 alpha
  |x-a|` of Section 1.1. With the secant relaxation of the concave square it
  has exactly the same open nodes and minimizers. I checked the one-sided
  derivatives at `a` and the pruning of non-straddling nodes. So the
  statement "gives the exact-gap model with `alpha = 1`" is right in effect.
  It should say that the function differs.

## 2. Theorem A

### 2.1 Proof

- **Steps 1–3** are correct: nested zones, "the rule follows the itinerary",
  intersection and injectivity, and measure at most `(2 theta1)^k`. One
  point, which the note does not state: `a` lies in `K_Theta` exactly when it
  lies in an **open** zone at every step, because a kink at a zone's inner
  end is split. So `K_Theta` is contained in the depth-`k` zone unions, and
  the null-set argument covers all of `K_Theta`, not only the constructed
  points. This is fine.
- **Step 4**: `theta_k (1 - theta_{k+1}) < rho_k < theta_k` gives
  `rho_k(1-rho_k) > theta0/4`. Correct.
- **Step 5 (1D)** is correct.
- **Step 5 (McCormick, x-only)** is wrong as written. For a box of full
  height the bound is `|c| w_y (a-l)(u-a)/w_x = |c| rho(1-rho) w_k`, not
  `... w_k^2`. Since `w_k <= 1`, the true bound is larger, so the claimed `K`
  remains a valid lower bound. The true count grows twice as fast in
  `log(1/eps)`. My counts: McCormick x-only `T` = 23, 45, 69, 91, 137,
  against 1D `T` = 13, 23, 35, 47, 69 at `eps = 1e-8, 1e-16, 1e-24, 1e-32,
  1e-48` (fixed clamp 1/5).
- **Steps 6–8 (iii)** are correct: common columns, aspect ratio
  `w_y >= theta0 w_x`, and the level-`K` boxes cover `[0,1]` in `y` with
  `w_y <= w_K`.
- **Numbers.** Theorem A(ii) holds for all five schedules I tested,
  including a history-dependent one (`0.15` or `0.3` by the parity of the
  number of left zones). Example: history schedule, `eps = 1e-48`, `T = 73`
  against the bound 59. For the fixed clamp 1/5, the bound is attained:
  `T = 23 = 2K+1` at `1e-16` and `35 = 2K+1` at `1e-24`. The author's
  `chain1d.log` compares every schedule with the `theta0 = 1/10` bound, which
  is weaker than the theorem's bound for three of the four schedules. It is
  not wrong.

### 2.2 The parenthetical "(in fact uncountably many)" in (ii)

The statement is false with the stated `K`. Take the fixed clamp 1/5.

- Suppose the itinerary of `a` has a run of length at least 2 starting at
  step `k`, say `RR`. Then `1 - rho_k < theta^2 = 0.04`, so
  `rho_k(1-rho_k) < 0.04 < theta0/4 = 0.05`.
- For `eps in [0.04 * 25^-k, 0.05 * 25^-k)`, chain node `k` is closed, so
  `T <= 2k+1`. But `K >= k+1`, so the claimed bound is `2K+1 >= 2k+3`.
- So only the two alternating itineraries qualify: `a = 1/6` and `a = 5/6`.

`check_thmA.py` part A3 confirms this for itineraries with one run of length 2.
The first violations are at `eps = 0.0447`, `0.002`, `3.2e-6` and `5.0e-9`, for
runs starting at steps 0, 1, 3 and 5. The remark after step 4 already says
"with a weaker constant", so the fix is to move that qualifier into the
statement.

### 2.3 Scope of the Summary's wording

- **The class.** The Summary and the task paraphrase say "every deterministic
  clamp schedule that does not look at where the point sits inside the
  zone". The theorem is about clip schedules, whose fallback is the zone's
  inner end, so the child is the whole zone.
  - The midpoint fallback also ignores the position inside the zone, and it
    escapes. Exact check (`check_midfallback.py`): 3,000 kinks each for
    `theta = 1/5, 1/4, 1/3`. None traps, and
    `S = ceil(log2(theta/d0)) + 1` exactly.
  - The note's own "What causes the trap" remark states the right property.
    The Summary should use it.
- **The `eps^(-1/2)` claim.** The Summary says "Omega(eps^(-1/2)) on the
  McCormick family with widest-side selection" for every such schedule.
  Theorem A(iii) needs two extra hypotheses:
  - `theta_B` depends only on the x-interval path;
  - y-splits are `theta0`-safe.

  If `theta_B` depends on `w_y` or on y-history, different columns follow
  different x-chains, and the proof does not apply.

### 2.4 Remark on SCIP's default (Conjecture A')

A simple fact narrows the conjecture. With SCIP's formula, the split lands on
`a` **iff `a` is the midpoint of the node**, because the pull `mu_B > 0` at
every node:

- Unclamped: `mu mid + (1 - mu) a = a` iff `mid = a`.
- Clamped: `a` would have to equal `l + 0.2 w`, but then the unclamped point
  exceeds `l + 0.2 w` because `mid > l + 0.2 w`, so the clamp would not bind.

So the exceptional set is the set of kinks that are the midpoint of a node on
their own chain. What remains is to show that `mid(a) = a` is not an identity
along any decision sequence, since the endpoints are polynomial in `a`. This
is not a proof. It is a suggestion for closing Conjecture A'.

## 3. The recentring clamp and Proposition D

- **Definition.** `RC_theta` is deterministic and `theta`-safe for
  `theta <= 1/3`. It is well defined at `p = l`, where it gives the clip, and
  at `d = theta/2`, where both branches coincide.
- **Proposition D(i)** is correct as stated, but it is not sharp. For
  `d0 < theta`:
  - Let `m = min{j : d0 theta^-j >= theta/2}` and
    `J = min{j : d0 >= theta^(j+1)}`. Then `m <= J` because
    `theta^(j+1)/2 < theta^(j+1)`.
  - If `d_m >= theta`, then `d0 >= theta^(m+1)`, so `J = m` and
    `S = m + 1 = J + 1`.
  - If `theta/2 <= d_m < theta`, then `J >= m + 1` and
    `S = m + 2 <= J + 1`.
  - With Proposition C, `S_RC = J + 1` exactly.

  So `RC_theta` is **optimal** in the number of splits among all
  `theta`-safe rules, deterministic or randomized, with any information. The
  statements "within one split of the best safe rule" (Summary, Sections 4,
  7) and "`S <= J(theta) + 2`" should be replaced by this.
  - Exact check (`check_CD.py` C1): 14,670 kinks for
    `theta in {1/10, 1/5, 1/4, 3/10, 1/3}`, including `theta^j/2` and
    `theta^j` with small perturbations. `S_RC - (J+1) = 0` in every case.
    The clip exceeds `J+1` by up to 24 splits, and one kink traps.
  - The note's own `chain1d.log` table [C] already shows equality in every
    row.
- **Proposition D(ii)** is correct.
  - The one step that is not a direct copy of face-exact 5.4(c): a recentring
    x-split shrinks the interval by `2 rho in [theta, 2 theta)`, not by
    `theta`. Boxes that arrive from level `k-1` still have
    `w_y > theta |I_{k-1}| >= |I_k|/2 >= theta |I_k|`, so level-`k` x-split
    boxes number at most `theta^-(k+1)`.
  - Bound arithmetic: `theta^-m < 1/(2 d0)` holds.
  - Exact counts at `eps = 0` are the supremum over `eps`, because a
    deterministic rule's tree only grows as `eps` decreases. They are all
    within the first bound. Examples: `1/6` 17 (bound 126); `3/238` 183;
    `0.0102` 191; `0.0999` 33; `1e-3` 3,219 (15,626); `1e-4` 22,703
    (390,626); `theta = 1/3`, `a = 1/10` 43 (271).
- **"At `a = 1/6` ... 17 nodes for every `eps`."** The count is 17 for
  `eps < 0.0123` and smaller above that. This is harmless; "at most 17" is
  exact.

## 4. Theorem B

- **Proof.** I checked every step:
  - the chain law;
  - the decomposition `log(1/d') = log(1/d) - log(1/theta) + log(r/(1-r))^+`
    and `integral_d^(2d) log(d/(theta-d)) dtheta = d`;
  - the reduction and the three cases (linear in `s`, equality at `s = 0`
    by `B = 1/delta`, and at `s = 1` by the definition of `A`);
  - the truncation and monotone-convergence argument (`g >= 0` needs
    `A >= 0` and `d <= 1/2`; both hold);
  - Wald's identity for the bounded stopping time `N`, and
    `d_N in [theta0/2, 1/2)`.
- **Constants** for `[0.1, 0.3]`: `delta = 0.70397`, `A = 3.13076`,
  `B = 1.42051`, `1/mu = 0.60435`. Correct.
- **E[S].** Nyström solve (`N = 3000` and `6000` agree to `1e-4`) and `10^7`
  Monte Carlo chains:

  | `a` | Nyström | Monte Carlo | note |
  |---|---|---|---|
  | 1/6 | 2.0252 | 2.0253 ± 0.0003 | 2.02 |
  | 3/238 | 3.3196 | 3.3194 | 3.32 |
  | 0.1999 | 1.9305 | 1.9306 | 1.93 |
  | 1e-4 | 6.3062 | 6.3062 | 6.31 |
  | 1e-8 | 11.8778 | 11.8779 | 11.88 |
  | 1/6, `[0.15, 0.25]` | 2.5359 | 2.5355 | 2.54 |
  | 1/6, `[0.19, 0.21]` | 3.72 (grid-sensitive) | 3.7258 | 3.73 |

  The slope on `[1e-14, 1e-8]` is 0.60435, equal to `1/mu`.
- **Supersolution slack**, in closed form on a 20,000-point grid: 0.6403,
  0.7651, 1.3486, 0.5411 for the four windows, each attained at
  `d = theta0`. This matches the author. Two more windows with
  `delta > 0` (`[0.2, 0.5]`, `[0.05, 0.1]`) also have positive slack.
- **Quoted bounds.** "The bound gives 5.68, 9.34, 5.42, 16.2 and 29.3" uses
  only the first bound. The note's own second bound gives **12.5** at
  `a = 1e-4` and **18.1** at `a = 1e-8`. At `3/238` it gives 9.61, which is
  weaker.
- **"The 99.99% quantile of `S` is at most 20."** With `10^7` chains it is
  21 at `a = 1e-8`. This is a nit.
- **1D node counts** (`10^6` runs): 3.73, 4.67, 5.02, 5.05, 5.05 at
  `eps = 1e-2, 1e-4, 1e-8, 1e-16, 1e-32` for `a = 1/6`, and 7.58 at `1e-8`
  for `3/238`. The note's figures (3.7, 4.7, 5.0, 5.1, 5.0; "7.6 against 7")
  match.

## 5. Proposition C

- **Proof.** Correct. While `a < theta0 u` every allowed split exceeds `a`,
  the child is `[0, s]`, and `u_k >= theta0^k`. The first `J` chain nodes
  have `a < theta0^(k+1) <= theta0 u_k` because `ceil(x-1) < x`, and they
  are open under the stated condition.
- **Second bullet.** The choice `a = (2 theta0 eps/(alpha(1-theta0)))^(1/2)`
  gives `alpha a^2 (1-theta0)/theta0 = 2 eps` and `a < theta0`. The ratio
  bound follows.
- **Exact check.** 21,465 `(a, eps)` pairs with `RC_0.2` and `C_0.2`: no
  `T < 2J+1`.
- **Tightness.** By Section 3, the bound `J+1` on `S` is attained for every
  kink when `theta0 <= 1/3`. For larger `theta0` it can fail to be attained
  (`theta0 = 0.45`, `a = 0.4`: `J+1 = 2`, but no safe rule reaches `a` in 2
  splits). The note does not claim tightness.
- **Interpretation.** "Obstruction is safety, not information" is fair.
  Proposition C is elementary. Its value is in pairing it with Lemma 0 and
  Proposition D.

## 6. Proposition E, Conjecture E' and keyed randomization

- **Proposition E proof.** Correct.
  - The density of `d1` is `a/(D(1-d1)^2) >= a/D`.
  - Absolute distance is preserved by clamps, which gives
    `w_x = theta_root d1/d`.
  - Openness of the path follows from `w_y >= theta0 w_x` and
    `rho(1-rho) >= d/2` with `d <= 1/2`.
  - The boxes `v(Y)` form an antichain, `1/w_y >= 1/w_x` at an x-split, and
    the integral in `d1` is correct.
  - The argument is pathwise given `d1`. The divergence comes only from
    `E[1/d1] = infinity`, that is, from the draw distribution having a
    density near the flip point. This is worth saying: it explains why every
    deterministic safe rule is bounded on a fixed kink while every continuous
    random clamp is not.
- **Simulations.** My C code (`mc2d.c`, `10^6` runs per entry, widest side,
  ties to `x`):

  | `a`, window | mean `T` at `1e-4 / 1e-6 / 1e-8` | median at `1e-8` | 99% quantile at `1e-8` | note |
  |---|---|---|---|---|
  | 1/6, `[0.1, 0.3]` | 44.3 / 137.5 / **389.8 ± 1.0** | 21 | **3,709** | 44 / 134 / 435; median 21; 99% quantile 5,663 |
  | 3/238, `[0.1, 0.3]` | 176.9 / 386.8 / 962.7 | 855 | 2,745 | 177 / 385 / 969; 857; 2,849 |
  | 0.25, `[0.1, 0.3]` | 33.0 / 103.2 / 293.5 | 3 | 3,785 | 36 / 108 / 311; 3; 3,741 |
  | 1/3, `[0.05, 0.35]` | 11.0 / 40.1 / 113.5 | 3 | 2,659 | 12 / 45 / 101; 3; 2,637 |

  The `1/6` row of the note is off by about 12% in the mean and about 50% in
  the 99% quantile. This is 1,000-run noise: the note's own standard error at
  `1e-8` is 41.7. The conclusions do not change.
- **Medians at 3/238.** 43, 177, 245, 365, 555, 855 from `1e-3` to `1e-8`.
  The note has 43, 177, 247, 365, 563, 857. This matches.
- **Conjecture E' slopes** (`log10` mean between `1e-4` and `1e-8`): 0.18
  at 3/238, 0.21 at 0.0102, 0.24 at 1/6, 0.25 at 0.1999, 0.24 at 0.25, 0.25
  at 1/3 with `[0.05, 0.35]`. So the range is 0.18–0.25, not 0.18–0.29.
- **Proposition E bound against simulation.** 0.06–0.58 against means of
  100–420. The bound shows divergence only, as the note says.
- **Keyed randomization.** The argument (along a path, every key is new, so
  path probabilities are unchanged and `E[T]` is identical) is correct for
  keys per **(variable, interval)**.
  - With per-variable keys, the 42 entries agree with independent draws
    within `|z| <= 1.9`. Example: `a = 1/6`, `1e-8`: 389.3 against 392.5.
  - The medians stay bounded: 213 at 3/238 and 251 at 0.0102.
  - `sim_kink.py` keys the draw on `(l, u)` only, so the root x-split and a
    later y-split on `[0, 1]` share one draw. That is a different scheme, and
    its mean differs from the independent one:
    - 5.00 against 5.47 at `a = 3/238`, `eps = 1e-2` (`z = -587`);
    - 175.5 against 177.9 at `a = 0.0102`, `1e-4` (`z = -88`).
  - The differences are small (below 10%) and vanish in noise at `1e-8`. The
    "keyed" rows of the table therefore come from a scheme that the
    exact-equality argument does not cover. The rows 337 and 1,086 against
    435 and 969 are noise in any case. At `10^6` runs all three schemes give
    about 390 and about 962.

## 7. Proposition F and the incumbent rule

- **Proposition F.** Correct and elementary. An incumbent value `v` used on a
  path becomes an endpoint of both children, so it is never strictly inside a
  later interval of that path.
- **3 nodes with an optimal incumbent.** Correct in 1D, and on the McCormick
  family with ties to `x`. The weakness named in the note (nodes without the
  incumbent fall back to the clip) is real. The SCIP runs show it: `x_inc`
  2,565 nodes at `a = 1/6`.
- **The plugin's test.** `x_inc` requires the incumbent **point** to lie in
  the node box, as the definition says. SCIP accepts a suggested point that
  lies strictly inside the domain without clamping it (`branch.c`,
  lines 2354–2390, SCIP 10.0.3 source in `~/build-scip`). This matches the
  43 sub-1% children reported for `x_inc`.

## 8. SCIP experiments (spot checks, `check_scip.py`)

- **Run inventory.** 2,052 runs, 12 settings × 57 instances × 3 seeds. The
  status counts match the note's table. The five crashes are on
  wastewater05m1 (rclamp s1, lp_rclamp s1) and wastewater05m2 (x_recenter s0,
  c10 s2, x_noclamp s2), as stated.
- **Reproduction of the earlier study.** `default`: 168 runs optimal in both
  studies, 168 with identical node counts. `lp`: 163 and 163. Correct.
- **Node ratios.** Recomputed with my own aggregation: per-instance shifted
  geometric mean over seeds (shift 10), exponentiated mean log ratio,
  bootstrap with 20,000 resamples, and `scipy` Wilcoxon.

  | Pair | Mine | Note |
  |---|---|---|
  | rclamp / default | 0.963 (0.87–1.06), p 0.58, 11/10, sep 0/0 | 0.963 (0.87–1.06), 0.576 |
  | lp_rclamp / lp | 0.996 (0.90–1.09), p 0.78 | 0.996 (0.90–1.09), 0.769 |
  | x_rclamp / x_default | 0.996 (0.88–1.12) | same |
  | x_lp_rclamp / x_lp | 1.001 (0.93–1.07) | same |
  | x_recenter / x_lp | 0.939 (0.86–1.01), p 0.30, 17/10 | 0.939 (0.86–1.01), 0.291 |
  | x_inc / x_lp | 1.047 (0.95–1.17) | same |
  | x_noclamp / x_lp | 1.999 (1.43–2.98), sep 2/18 | 1.999 (1.43–2.96), sep 2/18 |
  | c10 / default, rclamp / c10, x_default / default | agree to 3 decimals | — |

  The alternative "ratio of the shifted geometric means over instances"
  agrees to 0.004.
- **Plugin counters.** Correct:
  - `x_lp`: LP value on a bound in 32.9% of continuous branchings, point
    moved in 50.5%;
  - `x_recenter`: recentred 9.8% (88,273 of 901,422);
  - `x_inc`: 675 incumbent splits, 43 children below 1%;
  - `x_noclamp`: 66.1% children below 1%.
- **Synthetic runs.** 3,840 runs, all with primal minus dual at most `eps`,
  the known optimum accepted, and no bound above the optimum (maximum primal
  and dual `1e-15`). The table entries I compared against `summary.md` (1D
  and McCormick at `1e-8`) match.
- **Wording issues found in the checks:**
  - **"Trap points 1/6 and 0.1999" (Section 6.3, twice).** 0.1999 is not in
    `K_0.2`. The clip makes 5 clamped splits and then splits at `a`. The 1D
    count saturates at 13, reached at `1e-8`. It is a near-trap point with a
    long finite chain, as in the face-exact note.
  - **Summary: "SCIP's default ... with or without the random clamp:
    1,600–6,500 nodes at `1e-8`".** `rclamp` reaches 6,828 at `a = 0.1999`.
  - **"`p >= 0.58`"** for the four random-clamp pairs. The smallest is 0.576.
    This is a nit.
  - **Reference for recentring.** "None of the safe rules differs from
    SCIP's default beyond seed noise" and "It costs nothing measurable on
    MINLPLib (0.94, CI 0.86–1.01)" (Section 7). For recentring and the
    incumbent rule the reference is `x_lp`, the plugin with midpull 0. The
    direct comparisons are:
    - `x_recenter / default` 0.92 (0.71–1.15);
    - `x_recenter / x_default` 0.92 (0.75–1.09).

    These are also neutral, but with CIs twice as wide. The recommendation
    to SCIP should quote the comparison it rests on.
  - **Mixed arms in the Summary.** The McCormick bullet
    (`C_0.2` 7,190, random clamp 228, "recentring 21 (plugin)") compares
    Arm P with Arm X. The plugin's own clip gives 9,743. The note marks
    "(plugin)", but a like-for-like pair would be clearer.

## 9. Corrections requested in the note

1. **Proposition D(i) and the Summary, Sections 4 and 7.** Replace "at most
   `J(theta) + 2`" and "within one split of the best safe rule" with
   "`S = J(theta) + 1`, the Proposition C lower bound: `RC_theta` is
   split-optimal among `theta`-safe rules in 1D". Add the three-line proof
   from Section 3.
2. **Theorem A(ii).** Drop "(in fact uncountably many)", or qualify it "with
   a smaller constant in `K`". For the fixed clamp 1/5 the stated bound holds
   only at `1/6` and `5/6`.
3. **Theorem A, proof step 5.** The McCormick x-only bound is
   `|c| rho_k(1 - rho_k) w_k`, not `... w_k^2`. The statement stands, and
   the true `K` is about twice as large.
4. **Summary, Theorem A bullet.**
   - Say "clip schedules (fallback at the zone's inner end)" instead of
     "schedules that do not look at where the point sits inside the zone".
     The midpoint fallback is a counterexample to the broader reading.
   - State the hypotheses of A(iii) where `eps^(-1/2)` is claimed.
5. **`C_0.2` count at `a = 1/6`, `eps = 1e-8`, widest side.** It is 19,537
   in exact arithmetic, not 19,541 (Section 5 text and table). The 19,541 is
   the floating-point tie artifact that the face-exact note already
   documents. My C code in doubles reproduces 19,541.
6. **Section 5 table, `a = 1/6` rows.** The mean at `1e-8` is about 390, not
   435 or 337, and the 99% quantile is about 3,700, not 5,663. Report the
   standard errors or use more runs. The Conjecture E' slope range is
   0.18–0.25.
7. **Keyed simulation.** `sim_kink.py` keys on `(l, u)` without the
   variable. Either key on `(variable, l, u)`, the scheme the
   equal-mean argument covers, or say that the simulated scheme shares draws
   across `x` and `y`.
8. **Section 6.3.** 0.1999 is not a trap point. The default range is
   1,587–6,828 with `rclamp` included.
9. **Section 7 recommendation.** Quote `x_recenter / default` (0.92,
   0.71–1.15) next to `x_recenter / x_lp`.
10. **Theorem B remarks (optional).** Quote the second bound where it is
    smaller (12.5 and 18.1). The 99.99% quantile at `a = 1e-8` is 21.
11. **Section 1.1 / 6.2 (optional).** State that `k1:a` uses
    `2|x-a| - (x-a)^2`, which has the same open nodes and minimizers as the
    model.

## 10. Novelty notes

No literature search was possible in this session: the web-search quota was
exhausted. The notes below are my assessment, not a search result.

- **Theorem A** generalizes the face-exact note's Proposition 5.5 (a fixed
  clamp) to clamps that depend on the box path. The proof is the standard
  nested-interval (Cantor or iterated-function-system) construction. It is
  modest, but it is the right general statement, and the diagnosis ("the
  fallback is the zone's inner end") is useful.
- **The recentring clamp.** I do not know it from the SCIP, Couenne or
  BARON rules summarized in the context notes, which use a clip, a midpoint
  pull or the incumbent. With the correction above, the fact that it is
  split-optimal among safe rules is the cleanest positive result of the
  note. A literature check for "balanced" or "centred" fallbacks in spatial
  branching is still needed before claiming originality.
- **Theorem B** uses standard tools: a Foster–Lyapunov supersolution plus
  Wald's identity. It is a sound and complete application.
- **Propositions C and F** are elementary. The keyed equal-mean statement is
  linearity of expectation.
- **Proposition E** is new in this program and gives a clear mechanism: the
  draw density near the flip point.

## 11. Commands run

All commands were run in `research-20260928b/reviews/robust-branching/`. At
most 4 processes ran at a time.

```
python3 check_thmA.py A1 A3 > check_thmA_A1A3.log      # Theorem A(ii), trap points, uncountability parenthetical
python3 check_thmA.py A4 > check_thmA_A4.log            # Theorem A(iii), exact/60-digit widest-side counts
python3 check_thmB.py B1 B4 > check_thmB_B1B4.log       # Theorem B constants, bounds, closed-form slack
python3 check_thmB.py B2 B3 B5 > check_thmB_B2B3B5.log  # Nystrom, 1e7 Monte Carlo, 1D node counts
python3 check_CD.py C1 C2 > check_CD_C.log              # Propositions C, D(i) (exact rationals)
python3 check_CD.py D2 > check_CD_D2.log                # Proposition D(ii) (exact rationals, eps = 0)
python3 check_midfallback.py > check_midfallback.log    # midpoint fallback never traps (theta <= 1/3)
gcc -O2 -o mc2d mc2d.c -lm && python3 run_mc2d.py > run_mc2d.log   # Proposition E, Conjecture E', keyed schemes
python3 check_scip.py > check_scip.log                  # SCIP spot checks from the raw JSONL
```

The `mc2d` binary was deleted after the run; recompile it with the command
above. These are targeted checks only. No project-wide checks were run, and
no CI results are involved.

## 12. What remains unchecked

- How faithfully Arm X re-implements `cons_nonlinear.c`'s variable selection.
  I checked only the reproduction statistic (`x_default / default` 1.005,
  6/19 wins/losses, p = 0.016), which the note already reports as a tilt.
  I did not read `scoreBranchingCandidates`.
- The Arm P event-handler timing: whether every `SCIPgetBranchingPoint` call
  at a node sees the redrawn clamp. I did not trace SCIP's event order.
- MINLPLib time ratios, the subgroup ratios and the correctness deviations
  (4.5e-8 and so on). I read them from `summary.md` but did not recompute
  them. The seed-noise table was only read.
- The synthetic SCIP runs beyond the `1e-8` tables.
- Conjecture E' (a rate `eps^(-gamma)`) and the claim that the median grows
  for every near-boundary kink. These are numerical only, in the note and
  here.
- Theorem A(iii) for schedules that depend on y-history. It is not claimed,
  and I think it is open.
- Novelty against the literature (no search was possible).
