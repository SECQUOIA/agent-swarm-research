# Review of `theory-bangbang/window-exactness.md`

Date: 2026-09-30. Reviewer: independent adversarial verifier. I did not write
the report. I read it in full, together with the parts of [R]
(`theory-bangbang/report.md`, Sections 0–4 and 9.3) and [E]
(`theory-bangbang/extension-n2.md`, Sections 0–1, 2.5, 3, 5, 6.1, 7) that it
cites. I checked every proof step and re-ran every numerical claim about the
scalar toys and a sample of the two-state claims with my own code. Check
scripts and logs: `reviews/window-exactness-review-checks/`.

## Verdict

**The mathematical results hold as stated under the report's standing
hypotheses (SH). Every numerical claim I re-ran reproduced. A set of smaller
corrections is needed.** None of them changes a theorem. They are: one
incorrect formula in the Summary (the window duration `l_0`), a few statements
in the Summary and Section 8 that are broader than the propositions they cite
(Proposition D, the `1/log(1/h)` rate, "exact in principle", the rate
wording), an index slip in Section 7.6, a rounding artefact in the Section 7.5
table, a small radius gap in the entry-set reduction, and missing literature
(Osmolovskii–Veliov 2020, and the link between `kappa_tau` and the
Osmolovskii–Maurer quadratic form).

Summary of the checks:

| item | verdict |
|---|---|
| Lemma 0.1, Lemma 0.2 | correct; the reduction of Lemma 0.1(2) is stated at radius `r` but used at `r/2` (issue 6, repairable) |
| `mu'` remark (factor-2 slip in [R, Thm 4.1]) | **confirmed**: step (c) of [R] gives `h mu/2`, so Lemma 2.1(i) then needs `|sigma| >= Delta|beta|^2/mu`, twice the (H3) margin; the `mu' < mu` repair is correct |
| Proposition 1.2 | correct (direct from [R, Prop 3.1]) |
| Lemma 1.3 | correct; re-derived; exact identity on the toy |
| Remark 1.4 (phase model) | heuristic, labelled; numbers reproduced |
| Proposition 2.1 (decoupling) | correct |
| Theorem A (`kappa_tau > 0`) | correct; `c_*` is a specific small constant, not any `c` (wording, issue 8) |
| Theorem B (`kappa_tau = 0`) | correct; the three-case pairing argument checks; `K_0` independent of `h` |
| Theorem C (`kappa_tau < 0`) | correct; (iii) gives only a necessary duration; the Summary's closed form for `l_0` is wrong unless `a` is also constant (issue 1) |
| Proposition D | correct as stated (LQ data, exactness over `R^n x U`, exit within `K` stages); the Summary states it more broadly and attaches an unproved rate (issue 2) |
| Proposition E | correct (elementary) |
| Section 7 numerics | all re-run items reproduced (table in Section 3 below) |
| Literature and novelty | novelty claim plausible; two additions needed (Section 5) |

## 1. What I checked and how

**Proofs.** I re-derived each step with pencil and paper. Points worth
recording:

- *Lemma 0.2.* The `u`-move at `xbar_t` gives `h|sigma||omega| + (h^2/2)
  kappa^- omega^2` (KKT sign, (P3)). The `x`-move uses
  `grad_x rho(xbar,u) = h omega beta_t + O(h^2 omega^2)` and strong convexity;
  minimizing over `d` gives the displayed bound. Correct.
- *The `mu'` remark.* In [R, Thm 2.3], (W1) and (W5) use the same `mu`. [R,
  Thm 4.1] step (c) supplies only `grad_x^2 rho >= h mu/2` ([R] Section 9.3,
  item C2, says so explicitly), so (W5) would be needed with `mu/2`, i.e.
  `|sigma| > Delta|beta|^2/mu`, which (H3) does not give. The repair works:
  near `tau`, tangency gives `Delta L^2 s^2/(2 mu') < gamma_1 s` for small `s`;
  away from `tau`, the strict (H3) margin is bounded below on a compact set, so
  some `mu' < mu` keeps it; and `h[r_xx + o(1)] >= h mu'` for small `h`. No
  conclusion of [R] changes. The finding is new relative to [R] Section 9.3.
- *Lemma 1.3.* With `p_{t+1} - p_{t+2} = h grad_x H(xbar_{t+1}, ubar_{t+1},
  p_{t+2})` and `v = grad l_1 + (Db)^T p`, the difference is
  `h[v^T a - b^T(grad l_0 + a_x^T p)] + h(u_t - u_{t+1}) b^T v + O(h^2)`. The
  bracket is the `u`-free form of `sigma_dot`, and `w = -v` at the switch, so
  `-b^T v -> kappa_tau`. Correct. For the toy it is an exact identity:
  `sigma_{t+1} - sigma_t = h(a_{t+1} - x_{t+1}) + h(u_{t+1} - u_t)(-k)`.
- *Proposition 2.1.* Lower bound: per stage, Lemma 0.2 inside the ball and
  (P6) outside it (where `rho_t >= rho_t(zbar_t) >= rho_t(zbar_t) + m_t`)
  give `rho_t - rho_t(zbar_t) >= m_t - C h^3` on all of `D_t x U`; summing
  and telescoping gives the window bound for **every** entry, so Lemma 0.1(2)
  is not even needed here. Upper bound: the move `x_a = xbar_a`,
  `omega_t = omega*_t` costs `m_t + O(h^3)` per stage from the `u`-move plus
  `O(Kbar^2 h^3)` from the carried state. Correct.
- *Theorem A.* The three zones check, including the constants for `c_*`.
  Zone (i) needs `L s_t + C_beta e_h + C'h <= sqrt(h mu' kappa_tau/2)`, which
  holds for `s_t <= s_1(h)` and `c_* <= sqrt(mu' kappa_tau/8)/(2 C_beta)`.
  Zone (ii) uses `(Delta/mu') L^2 s^2 <= gamma_1 s/4` and
  `C_sigma e_h + O(h) <= gamma_1 s_1(h)/2`. Zone (iii) is [R, Thm 2.3(1)]
  with `mu'`. One small omission: `delta_2` should also be at most `delta_sigma`
  (where the lower bound `|sigma| >= gamma_1|t - tau|` holds).
- *Theorem B.* (a) follows from Lemma 1.3 with `kappa_tau = 0` and
  `e_h = O(h)`: consecutive `sigma_t` move by `gamma h(1 + O(h))`, so at most
  one lies in an interval of width `2 gamma h/3`. (b) follows because the
  first-order term `>= gamma h^2/3 |omega|` beats the `O(h^3)` curvature and
  cross terms near `tau`. (c) I checked the three cases: `V >= delta/4` (the
  first-order sums pay), `Z >= delta/4` (Cauchy–Schwarz over `2K+1` states),
  otherwise the `K` disjoint pairs `(n+1-j, n+j)` each carry
  `|d_{n+j} - d_{n+1-j}| >= delta/2`, so `sum |d_t|^2 >= K delta^2/8`. The
  stage-`n` constant `C_4` does not depend on `K` because `s_n <= C_1 h`, so
  `K_0 = ceil(128 C_4/(mu'|b(x*(tau))|^2))` is independent of `h`, and `h_0`
  depends on `K`. Correct. (`C_4` contains `C_3^2/mu'`, so `K_0` can grow
  like `1/mu'^2`, not only `1/mu'`; the report calls the constant crude.)
- *Theorem C.* (i)/(ii): moving only `u_n` changes stage `n` by
  `h sigma_n omega + (h^2/2) omega^2 kappa_n`, with `kappa_n -> kappa_tau`
  because `|sigma_n| = O(h)` forces `s_n -> 0`; the later stages cost
  `C_M h|d_t|^2/2 = O(h^3)` each, `o(h^2)` in total when `|W|h -> 0`.
  (iii): summing `C_M h^3|b|^2 omega^2 e^{2 C_g (t-n)h}/2` gives the stated
  bound. Correct. The bound on `B` uses `sum_{t notin W} inf rho_t <=
  sum rho_t(zbar_t)`. Correct.
- *Proposition D.* I checked the recursion `eta_{t-1} = eta_t - (eta_t +
  O(h))^2/m_t + O(h)` (needs `||Phat_t|| <= C_P`, which the sandwich
  `P^tr <= Phat <= Lyapunov` gives on `[s + K', N]`), the bound
  `m_t <= C_3(t - s)`, the harmonic-sum contradiction, the step from
  `s + K'` down to `b` by dropping pushes, and the exact LQ formula
  `J_W` change `= h sigma_n omega + (h^2/2) omega^2 b^T V_{n+1} b`. Correct
  under the stated hypotheses. The proof also extends (reviewer's sketch) to
  exits with `(b - s)h -> 0` instead of `b - s <= K`, because
  `log((delta/h)/(b - s)) -> infinity` still holds.
- *Proposition E.* The node contains the single-flip point with
  `|u - ubar_n| >= |I|/2`. Correct and elementary.

**Numerics.** I wrote new code (`rv_toy.py`, `rv_runs.py`, `rv_n2.py`,
`rv_n2_azero.py`) without importing or copying the report's scripts. It
differs from the report's code in these ways:

- my own KKT search: fit `J` exactly as a quadratic in the switching control
  for each candidate switch stage, then check KKT signs at every stage, with
  no refinement step;
- stage residuals and window objectives built by **direct simulation** of
  `sum L_t + S_b(x_b) - S_a(x_a)`, with the quadratic coefficients extracted
  by exact polarization (no closed-form coefficient formulas);
- my own face-enumeration box-QP (exact rationals or float);
- for the global optimum of toy plus, an exact convexification lower bound and
  a small exact branch and bound instead of SCIP (Section 3).

For the two-state examples I imported only [E]'s KKT solver and continuous
family as inputs. I recomputed the costates, the KKT signs, and the stage and
window objectives myself.

## 2. Findings on hypotheses, uniformity, entry set and switch stage

- **Uniformity in `h`.** All constants in Lemma 0.2, Proposition 2.1 and
  Theorems A–C are independent of `h` as claimed. In Theorem B, `K_0` is
  independent of `h`, and `h_0` depends on `K`. This matches the statement
  "for every fixed `K >= K_0` … for small `h`".
- **Entry set.** The window uses the free entry `D_a`. Lemma 0.1(2) proves
  the reduction for entries at distance `>= r`, but Proposition 2.1 and
  Theorem B, step 1, use it for entries at distance `>= r/2`, and (P6) is
  stated at radius `r/2`. Entries at distance between `r/2` and `r` can have
  window states leaving `B_r`, where (P2) is not available. The gap is
  harmless:
  - Proposition 2.1 does not need the reduction (see Section 1).
  - For Theorem B, near-switch stages satisfy `rho_t >= rho_t(zbar_t)`
    whenever `|d| >= r'` for any fixed `r' > 0` and small `h`, because
    Lemma 0.2 gives `-O(h^2) + (h mu'/2)|d|^2` inside the ball and (P6)
    applies outside it. So the reduction holds with `r/4` in place of `r`.

  The proof should say this (issue 6).
- **Switch stage.** The interior stage and the small-`sigma` vertex stage
  are treated correctly in all three cases. For `kappa_tau <= 0`, Lemma 1.3
  gives increments `sigma_{t+1} - sigma_t` of the same sign and of size at
  least `gamma h (1 - o(1))`, so for small `h` there is at most one interior
  stage (Theorem B(a) states this for `kappa_tau = 0`; Theorem C needs only
  one). Two adjacent interior stages occur only when
  `gamma < Delta kappa_tau`, which needs `kappa_tau > 0`, and Theorem A covers
  every stage then.
- **Hypotheses of the two-state illustrations.** The family in Section 7.5 is
  `continuous_family` of `n2/model.py`: the global-model maximal solution,
  with **equality** in the anisotropic Schur condition (G) on the last arc
  (`M - 2 eps I = (Delta/(2|sigma|)) beta beta^T`, a rank-one excess). (SH)
  requires the isotropic (H3)/(W5) margin `|sigma| > Delta|beta|^2/(2 mu)`
  with `mu <= lambda_min(M) = 2 eps`. That is much stronger, and the report
  does not check it. So the labels "A: Theorem A", "A−: Theorem C" and
  "A0': Theorem B" are illustrations, not instances. The scalar toys do
  satisfy (SH): for example, the verifier family has margin
  `0.129 (t - tau)^2 < 0.44 (t - tau)` on the last arc. The theorems
  themselves are unaffected; their proofs would carry over to the anisotropic
  Schur form, but that is not written out (issue 5).

## 3. Numerical re-verification (reviewer's code)

All runs single-threaded and short (at most about 10 s each). "Exact" means
rational arithmetic.

| report claim | reviewer result | status |
|---|---|---|
| continuous data (7.1): `tau` = 0.21370 / 0.47741 / 0.47741; `gamma`, `eta_L`, `D`, `F''`, `b^TQb`; PMP violation 0; `|sigma| >= 0.44, 0.31, 0.31 |t - tau|` | closed-form `tau` from `sigma(tau) = -1.5 tau^2 + 5 tau - 1` (verifier) and `-1.5 tau^2 + 7 tau - 3` (plus, zero); all table values identical to 4–5 digits; PMP violation 0 | reproduced |
| 7.2 verifier toy, linear-rate family: exact gap 0 at N = 500 … 8000 | exact gap **0** at all five `N` (no failing stage, terminal loss 0) | reproduced (exact) |
| 7.2 family B terminal loss 3.19694 … 3.19125; exact 3.1938893… at N = 1000 | 3.196944, 3.1938893123…, 3.19250, 3.19158, 3.19125; equals `(2 + |xbar_N|)^2/4`; family B stage losses 0 at N = 1000 | reproduced (exact) |
| 7.3 toy plus deficits, N = 1000: 0.38878, 0.38774, 0.38691, 0.38611, 0.38532 `h^2` | same five values; K ≤ 2 exact at N = 1000 and 4000; argmin is the single flip with entry shift −0.42 … −0.55 `h`; argmin states inside the box | reproduced |
| 7.3 other `N` (500, 2000, 4000, 8000) and predictions `m_t` | identical (0 at N = 500; 0.01800 … 0.01356 at N = 2000; 0.35041 … 0.34963; 0.53333 … 0.53274) | reproduced |
| 7.3 fixed-entry duration: 251, 1000, 2000 stages | 251, 1001, 2000 (the N = 4000 case is the tie `b - 1 - n = k/h` exactly, decided by rounding) | reproduced |
| 7.3 SCIP: `f* = J(zbar)` to about 1e-9 at N = 50 … 200; K = 2 window below by 9.2e-4 … 3.1e-5 | exact branch and bound: `f* >= J(zbar) - 1e-11` (tolerance) at N = 50, 100, 150, 200 (15–19 nodes); K = 2 deficits 9.17e-4, 1.75e-4, 5.38e-5, 3.05e-5 | reproduced independently of SCIP |
| (new) window bound strictly below `f*` at larger `N` | exact lower bound `f* >= min J_zero - (k/2) h^2 N` (below) exceeds the K = 2 window bound at N = 50 … 200, **1000 and 4000** | extends the SCIP check |
| 7.4 toy zero: stage-`n` loss 0.0680, 0.4266, 0.0362, 0.1072 `h^3`; K = 1, 2 windows exactly 0 at N = 1000, 4000, 8000; N = 16000 no interior stage | same losses (exact) and prediction formula; K = 1 and K = 2 exact minimum **exactly 0**; K = 0 exact deficit > 0; affine family: loss 0 near the switch | reproduced (exact) |
| 7.5 A (N = 1000, 2000): no failing stage | window values `<= 2.3e-21 h^2` | reproduced (float) |
| 7.5 A−: N = 1000 `s-1` 0.3921, windows 0, 0.3827, 0.3765; N = 2000 0.4731, 0.4706, 0.4682; N = 8000 `s+1` 0.4417, 0.4416, 0.4416 | 0.3921, 0, 0.3827, 0.3765; 0.4731, 0.4706, 0.4682; 0.4417, 0.44164, 0.44159 | reproduced (float) |
| 7.5 A0' N = 1000 (eps = 0.02): 1.215, 0.967, 0.880 `h^3` | 1.215, 0.967, 0.880 | reproduced (float) |
| 7.5 A0' eps = 0.1: window with 4 stages per side exact at N = 1000 and 4000 (Schur certificate) | full minimum over the box by face enumeration: N = 1000: K = 1, 2, 3, 4 give 0.826, 0.404, 0.130, `6e-19` `h^3`; N = 4000: 1.2e-4, 1.8e-5, `2e-15`, `2e-15` | reproduced, with a stronger method |
| 7.6 maximal recursion, toy `k = 0.5`: "`eta_hat_1`" 0.294 … 0.152, breaks at the interior-stage grids; `k = 0.1` never breaks, stages exact | 0.2936, 0.2421, 0.2222, 0.2046, 0.1790, 0.1816, 0.1516 (this is `Phat_{s+1} + k`, see issue 3); same break pattern; `k = 0.1` no break, float stage losses `<= 1.7e-15` | reproduced |
| 7.7 phase model: interior fractions 0.816 / 0.528 / 0.708; stagewise exact 0.292 | 0.820 / 0.528 / 0.708; 0.292. The one differing grid (N = 225, verifier) is a control equal to −1 up to `5e-14` that my tolerance classed as interior, so 0.816 is right | reproduced |
| the Hessian of Remark 1.5 | my window objectives are built by simulation and polarization; they agree with the report's values to all printed digits | consistent |

**The convexification lower bound (reviewer's addition, exact).** In toy
plus, `sum_t h k x_t u_t = (k/2) x_N^2 - (k/2) h^2 sum u_t^2` exactly (the
residual of this identity is exactly 0 in my runs). So
`J_plus(u) = J_zero(u) - (k/2) h^2 sum u_t^2`. Since `J_zero` is convex and
`u_t^2 <= 1`, we get `f*_plus >= min J_zero - (k/2) h^2 N`. The minimum of
`J_zero` is attained at its exact rational KKT point. The gap of this bound
to `J(zbar)` is 0.18–0.25 `h^2` on all tested grids. That is below the
window deficits (0.35–0.57 `h^2`), so the trivial convexification is tighter
than the tangential-window certificate. This does not contradict anything in
the report: Theorem C is about calibration-type (window) certificates, not
about how hard the instance is to certify. It is worth one sentence in
Section 6, because standard spatial branch and bound on the separable
concavity closes the gap to `1e-11` in 15–19 nodes here. That is still only
an `epsilon`-certificate, in line with the cluster-problem remark after
Proposition E.

## 4. Issues and requested changes

Numbered by importance. None changes a theorem.

1. **Summary item 4: the closed form for `l_0` is wrong as stated.** It says
   "`l_0 = |kappa_tau|/(C_M|b|^2)` when `b` does not depend on the state".
   Theorem C(iii) gives `C_M|b|^2 l_0 e^{2 C_g l_0} = |kappa_tau|`. `C_g` is
   the state Lipschitz constant of `g = a + b u`, so it vanishes only when
   `a` is also constant (the toy has `a = 0`). With `b` constant and `a`
   state dependent, the formula without the exponential overstates the
   necessary duration. Fix: "when `a` and `b` do not depend on the state".
   In (iii), also say "at least `l_0 - o(1)`".
2. **Proposition D is stated more broadly in the Summary and Section 8 than
   it is proved.**
   - The Summary says "every quadratic family that is exact after the
     window". The proposition needs exactness **over `R^n x U`** at every
     stage `t >= b`, with the exit at most `K` stages after the switch.
     Families that are exact only over the reachable boxes (what a
     certificate needs) are not covered, because [E, Lemma 10(5)] compares
     only `R^n`-exact families. Add both qualifiers, or add the extension to
     `(b - s)h -> 0` (the proof carries over, Section 1).
   - The Summary says the excess "tends to 0 like `1/log(1/h)`". The proof
     gives only `limsup <= 0`. Its harmonic-sum argument, made quantitative,
     gives an upper bound of order `1/sqrt(log(1/h))`. A refined comparison
     would give `O(1/log(1/h))`. The word "only" (a lower bound on the rate)
     rests on the leading-order law and the numerics. Label the rate as
     heuristic, as the status table already does for the threshold.
3. **Section 7.6: index slip in the definition of `eta_hat_1`.** The text
   defines `eta_hat_1 := b^T(F^T Phat_{s+2} b - w)`. The tabulated values
   are `Phat_{s+1} + k`: I get exactly 0.2936, 0.2421, … with `Phat_{s+1}`,
   and 0.343, 0.290, … with `Phat_{s+2}`. The criterion "exact at an
   interior stage only if `kappa_tau + eta_hat_1 > 0`" is `m_s =
   b^T Phat_{s+1} b > 0`, which matches the table, not the text. Fix the
   formula to `Phat_{s+1}` (stage `s` in [E]'s indexing). The 25% comparison
   with the log law is unaffected in substance.
4. **"Windows of fixed duration: exact in principle" (Section 6), and
   "`Theta(1/h)` stages" (Summary, Theorem C).** Theorem C(iii) proves only a
   necessary condition, so `Omega(1/h)` stages are needed. That a window of
   fixed duration `l >= l_0` that stops before `T` is exact is not shown.
   Only the trivial window over the whole remaining horizon, with `Phi` at
   the exit, is exact (when `f* = J(zbar)`). Reword: "necessary: `Omega(1/h)`
   stages; sufficiency of any window shorter than the remaining horizon is
   open".
5. **Section 7.5 attributions.** The two-state family satisfies the
   anisotropic global-form condition with equality, not the isotropic (H3)
   margin in (SH) (Section 2). Say "consistent with Theorem A/B/C" rather
   than "Theorem A/B/C". The same applies to the Summary sentence that
   Theorem A "explains" [E]'s examples A and A0.
6. **Entry-set reduction radius** (Lemma 0.1(2) used at `r/2`; Section 2).
   Add the one-line argument that near-switch stages satisfy
   `rho_t >= rho_t(zbar_t)` for `|d| >= r'` and small `h`, or restate
   Lemma 0.1(2) with a radius that matches (P6).
7. **Section 7.5 table, `eps = 0.1`, `N = 4000`.** The entry "0" for K = 2 is
   `1.84e-5 h^3 > 0` (the report's own log; my full minimum is the same). The
   window is inexact there, which is consistent with the text below the
   table, but the table reads as exact. Print it as `2e-5`.
8. **Rate wording.**
   - Theorem A needs `e_h <= c_* sqrt(h)` with a specific small `c_*`
     (depending on `mu'`, `kappa_tau`, `L`, `C_beta`, `C_sigma`), not "`c
     sqrt(h)`" for any `c`. The Section 8 line "the rate needed is
     `o(sqrt(h))`" should read "suffices"; necessity is not shown.
   - The Theorem A remark says [R, Remark 2.5] "found `O(h)` necessary"; [R]
     found it sufficient for its `O(1)` bound, and noted that a Hölder rate
     weakens that bound.
   - Section 6, second bullet ("enough vertex margin"), needs `e_h = O(h)`
     (or `o(sqrt(h))`); with `e_h ~ c sqrt(h)` the cross term contributes
     `O(h)` at the same order as `h Delta |kappa_tau|/2`. State the rate.
9. **Smaller wording points.**
   - "Invalid terminal term" (Summary, 7.2): the bound with family B is
     valid but not tight (`P_N = 1/2 > Phi_xx = 0`); say "inexact terminal
     term". Neither [R] nor [V] claimed family B as a certificate; [R]'s
     "fails on none" referred to stages in the window-law test. So this is a
     clarification of [R], not a correction.
   - "cannot be obtained … on any grid whose KKT point has an interior
     stage" (Consequence paragraph and Section 8) is an asymptotic
     statement. Say "along any sequence of grids with an interior stage, for
     all small `h`".
   - Section 6, first bullet: the gap is `O(h^2)` in general and
     `Theta(h^2)` only on grids of type (i)/(ii); it is 0 on the others.
   - Theorem B, "This case contains … optcdeg2": optcdeg2 has
     `kappa_tau = 0`, but with two switches and the terminal row `v_N = 0`
     it is outside (SH). Say so.
   - Theorem A zone (ii): add `delta_2 <= delta_sigma`.

## 5. Literature and novelty

Searched briefly (five web searches; one full text read): Alt–Baier–Gerdts–
Lempio (NACO 2012), Alt–Felgenhauer–Seydenschwanz (COAP 69(3) 2018, abstract),
Alt–Schneider–Seydenschwanz (AMC 2016, record), Veliov's linear-case error
analysis (record), Felgenhauer's stability papers (records), and
Osmolovskii–Veliov, *Metric sub-regularity in optimal control of affine
problems with free end state*, ESAIM:COCV 26 (2020) 47 (full text read with
`pdftotext`, Sections 2 and 5).

- **Needed addition: Osmolovskii–Veliov 2020, Theorem 5.1.** Their setting
  is affine problems of Lagrange type with a fixed horizon and a free end
  state, whose optimality map is strongly metrically subregular (SMsR).
  SMsR follows from their condition (A2') (Theorem 3.2). For purely
  bang-bang controls whose switching function grows linearly at its zeros,
  Corollary 4.2 gives SMsR under the extra bound
  `2 Omega(dx, du) >= -mu_0 ||du||_1^2` with `mu_0 < mu`. Under SMsR,
  solutions of the **discrete optimality system** (5.1)–(5.3) of the Euler
  scheme near the reference satisfy
  `||x^h - x||_{1,1} + ||u^h - u||_1 + ||p^h - p||_{1,1} <= C h`.
  The `W^{1,1}` norms control `L^infinity`, so this supplies `e_h = O(h)` for
  states and costates at discrete KKT points. That is exactly the rate that
  Theorem B, Proposition 2.1 and Proposition D assume, and that [R]'s
  Remark 2.5 left open. It needs their assumption (C3), that the discrete
  solution is near the reference. Their problem is of Lagrange type, and I
  did not check the transfer to Mayer terms. The report should cite it.
- **Link to the Osmolovskii–Maurer form (reviewer's derivation).** With
  [E]'s notation, the switch term of the O–M quadratic form is
  `D xi^2 + 2[H_x] xbar_av xi`, with `[H_x] = -w^T Delta u` and
  `xbar_av = b Delta u xi/2`. This equals `(D - Delta^2 kappa_tau) xi^2`.
  So `-Delta^2 kappa_tau` is the classical O–M cross term at the switch. The
  phase model's kink jump `h^2(D - Delta^2 kappa_tau)` is that switch term,
  and its within-stage curvature `h^2 Delta^2 b^T Q b` is the arc term; they
  add to `F'' = D + Delta^2 eta_L`. The report should say that `kappa_tau` is
  this known quantity. The new content is its role as the `u`-curvature of
  every tangential stage residual, and the resulting trichotomy for window
  certificates.
- **None of the works examined proves discrete-problem exactness of
  calibration or window certificates, or the trichotomy.** They give error
  estimates for discrete KKT points and, in the continuous problem,
  second-order sufficiency. The report's qualified novelty claim is
  plausible within these brief searches. The WebFetch summary of the
  Osmolovskii–Veliov paper claimed a "discrete second-order sufficient
  condition"; the text does not contain one. I record this so that nobody
  cites that summary.

## 6. Commands run and files

All commands were run from `reviews/window-exactness-review-checks/` with
`OMP_NUM_THREADS=1`. They are targeted checks only: no project-wide
verification, CI not inspected, nothing committed.

1. `python3 -c "…tau_of, pmp_check…"`: continuous switch data (Section 3,
   first row; printed only, not logged).
2. `python3 rv_runs.py verifier` → `logs/verifier.{log,json}` (exact, about 7 s).
3. `python3 rv_runs.py plus` → `logs/plus.{log,json}` (about 18 s).
4. `python3 rv_runs.py zero` → `logs/zero.{log,json}` (exact, about 15 s).
5. `python3 rv_runs.py lb` → `logs/lb.{log,json}` (exact bound and branch
   and bound, about 3 s).
6. `python3 rv_runs.py phase` → `logs/phase.{log,json}`.
7. `python3 rv_runs.py rmax` → `logs/rmax.{log,json}`.
8. `python3 rv_n2.py` → `logs/n2.{log,json}` (imports [E]'s `solve_kkt`,
   `reach_box` and `transferred` read-only).
9. `python3 rv_n2_azero.py` → `logs/n2_azero.{log,json}` (full face
   enumeration, up to 11 variables, about 9 s per window).
10. A one-off comparison of my KKT search with the report's `toy.kkt` on the
    250 verifier grids (imported read-only; printed only, not logged). Only
    N = 225 differed (tolerance, Section 3).
11. Web searches and one fetch as listed in Section 5.

Files: `rv_toy.py` (model, KKT search, exact box QP, stage and window
objectives by simulation), `rv_runs.py` (parts), `rv_n2.py`,
`rv_n2_azero.py`, `logs/`.

## 7. Limits of this review

- I did not re-run the report's own scripts. I reproduced their outputs with
  independent code.
- The two-state checks are float screening, like the report's, and cover six
  cases (A−, A, A0') plus the A0' `eps = 0.1` windows. I did not re-check the
  `eps = 0.02` Schur certificates or the A− maximal recursion.
- The proof checks are by hand. For Theorem B and Proposition D I checked the
  logic and the orders of the constants, not every numeric constant (for
  example the factor 128 in `K_0`).
- The heuristic parts (phase model, log law) were checked only against the
  numbers they predict.
