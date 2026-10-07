# Confirmation review (round 2) of `theory-bangbang/window-exactness.md`

Date: 2026-09-30. Reviewer: fresh, independent referee. I did not write the
report or the earlier reviews. I read the revised report in full, the
round-2 review (`reviews/window-exactness-confirm-r1.md`), the reviser's new
script `theory-bangbang/window/revision2_checks.py` and its logs, the parts
of [R] (`theory-bangbang/report.md`: Section 0, Definition 1.1,
Theorem 2.3, Theorem 4.1) and [E] (`theory-bangbang/extension-n2.md`:
Lemma 10, Corollary 11, Sections 6.1–6.2; `n2/n2_windows.py`,
`n2/model.py`) that the revision cites. I checked each of the six items from
scratch and recomputed every new or changed number with my own code. Check
scripts and logs: `reviews/window-exactness-confirm-r2-checks/`.

## Verdict

**All six items are resolved correctly. Every new or changed number
reproduces with independent code. Nothing was refused. No theorem or
numerical claim was made stronger than its proof or check.** The new derived
claim, that the maximal recursion breaks for all small `h` on grids with an
interior stage under the hypotheses of Proposition D, follows from
Proposition D.

One small inconsistency remains (Section 3, issue 1). The round-2 change
made it visible: the reviser confirmed that [R]'s (H1)–(H5) contain no
terminal condition, but the Consequence paragraph still says that `B = f*`
holds "under its hypotheses" (those of [R, Theorem 4.1]) when
`kappa_tau >= 0`. By Theorems A and B it also needs (T). The fix is one
line. Two further points are optional.

## 1. Item-by-item check

| # | round-2 item | what I checked | result |
|---|---|---|---|
| 1 | Summary item 4: rate attached to the wrong case | Re-read the proof of Proposition D. With `J = floor(delta/h)`, `delta = (log 1/h)^{-1/2}`, `theta^2 = 8 C_3 (C + C_1 + 1)/log(1/h)`, the bound `J/(K'+1) >= h^{-1/2}` holds for bounded `K'`, so `(theta^2/(4 C_3)) log(J/(K'+1)) >= C + C_1 + 1` and `eta_{s+K'} <= theta + C_1 delta = O((log 1/h)^{-1/2})`. If `K'` grows with `(K'+1) h -> 0`, `log(J/(K'+1))` still tends to infinity but can grow arbitrarily slowly, so only `limsup <= 0` follows. Summary item 4 now gives `limsup <= 0` for an exit `o(1/h)` stages after the switch and the rate only for a bounded offset. So do the sentence after Proposition D, the Section 6 bullet (first stage after the switch, a bounded offset) and the status table. No other occurrence of the rate is attached to `o(1/h)` exits (grep of all `(log(1/h))^{-1/2}` and `o(1/h)` occurrences). | resolved |
| 2 | Summary item 2: [E]'s families outside (SH) | Own code (`d1_shE.py`): sigma, states and costates as exact piecewise polynomials (sympy), own `tau` by root finding (agrees with [E]'s `find_switch` to `2e-15` on A and A0), own five-point `P'`, with [E]'s `continuous_family` (eps = 0.02) as the object under test. Also checked that [E]'s cmax, clin and clin.02 are `continuous_family(p, 0.02, delta1)` with `delta1 = None, 0.1, 0.02` (`n2_windows.py`), and that A0 is `rho = 1, c = 0.2` ([E, Section 6.1]). Results: `inf lambda_min(M)` = 0.039996–0.0399999 in all six pairs (within `4e-6` of 0.04); ratio `Delta|beta|^2/(2|sigma|)` near `T` = 2.446 (A), 1.975 (A0); sup over `t <= tau - 0.1` = 0.1398 (A), 0.3356 (A0); cmax on A at `t - tau = 1e-2, 1e-4, 1e-6, 1e-8`: 3.13, 117.4, 6270, 3.895e5. The value at `T` also follows in closed form: all three families have `P(T) = Phi_xx - 2 eps I`, so `beta(T) = (-0.3, rho - 0.34)` and `|sigma(T)| = 1.16313` (A), `0.26608` (A0), giving 2.4465 and 1.9754. On the equality pieces `M = 2 eps I + (rank one)`, so `lambda_min(M) = 2 eps` exactly there. The failure of the isotropic margin is therefore robust, not a sampling artifact. rmax is the discrete recursion of [E, Lemma 10] (`eps = 0.02`), so (SH) does not apply to it. clin+3h fails at `N = 500, 1000` on A ([E, Section 6.2] table: 149 and 22 failing stages), so "fourth family without failures" is accurate. | resolved |
| 3 | 7.6 table `0.214` | `logs/toy_rmax.json`: `eta_hat_1 = 0.213455` at `k = 0.1`, `N = 4000`, so it rounds to 0.213. All other `k = 0.5` and `k = 0.1` entries match the log to three digits. The largest float stage loss where the recursion does not break is `3.1203e-16` (`k = 0.05`, `N = 4000`), so `<= 3.2e-16` is correct and `<= 3.1e-16` was not (`d2_famB_rmax.py`). | resolved |
| 4 | "What still works": maximal-recursion wording | The Summary and the Section 6 bullet now separate three things. (a) Proved: no break implies an exact certificate ([E, Lemma 10(1)–(3)], read). (b) Necessary only: at an interior stage the recursion continues iff `m_s = kappa_tau + eta_hat_1 > 0`. (c) Float results. Log check: `k = 0.1` and `0.05` never break (7 grids each); `k = 0.5` breaks exactly on the four grids with an interior stage, at stage `s`; `k = 0.2` breaks at `s - 6, s - 3, s - 1, s, s` on 5 of 7 grids; `eta_hat_1 > 0` in all 28 runs. The new sentence "under the hypotheses of Proposition D, it breaks for all small `h` on grids with an interior stage" is correct. If the recursion reaches `s + 1` without breaking, `Phat` is exact over `R^n x U` on all stages `>= s + 1` with `P_N = Phi_xx`. Proposition D then applies with `b = s + 1` (bounded offset) and gives `eta_hat_1 <= C (log 1/h)^{-1/2} + O(h) < |kappa_tau|` for small `h`, so `m_s < 0`. For `kappa_tau < 0` the interior stage is the unique switching stage (Lemma 1.3: two adjacent interior stages need `gamma < Delta kappa_tau`). | resolved |
| 5 | "`B = f*` fails" | Consequence paragraph: "gives `B <= J(zbar) - c h^2` … cannot prove optimality of `zbar` … contradicts `B = f*` when `f* = J(zbar)`". Section 8, first bullet: "window exactness fails", then the same qualification. Both are right. `B <= J(zbar) + (beta_W - J_W(zbar))` holds without (T), since every infimum is at most its value at `zbar`. SCIP values rechecked in `logs/toy_scip.json`: dual below `J(zbar)` by `4.8e-10, 1.7e-10, 7.5e-10, 7.9e-10`; re-simulated controls above by `1.5e-11 … 3.0e-10`; `K = 2` window below by `9.2e-4, 1.7e-4, 5.4e-5, 3.1e-5`. All match the text. | resolved |
| 6 | Drift `a = 0`; Theorem A and (T) | Section 7.3 and round-1 item 1 now say "drift `a = 0`". [R, Theorem 4.1] read: (H1)–(H5) contain no terminal condition ((H1) only asks `Phi` to be `C^2`), so the stage conclusion of Theorem A does not use (T). Family B: I derived the stage residual symbolically from the definitions (`x_{t+1} = x_t + h u_t`, `L_t = h[(x-a)^2/2 + k x u]`, `S_t = p_t x + P (x - xbar_t)^2/2`, discrete adjoint), independently of `toy.py`. With `P = 1/2`, `k = -1/2`, the result is exactly `rho_t(zbar + (d, omega)) - rho_t(zbar) = h d^2/2 + h sigma_t omega + h^2 omega^2/4`, `sigma_t = k xbar_t + p_{t+1}` (`d2_famB_rmax.py`). So stage exactness at every `N` needs only the KKT sign, as stated. The logged float stage losses (`<= 3.24e-31`) match "`<= 3.3e-31`". | resolved |

## 2. Refusals

None. The reviser applied all six items. For item 2 the reviser ran the
missing check rather than weakening the claim, which is the better option.
The check reproduces (item 2 above).

## 3. Remaining problems

1. **The Consequence paragraph omits (T) (minor; pre-existing, made visible
   by item 6).** It begins: "Under its hypotheses, `B = f*` holds without a
   window if `kappa_tau > 0` …, and with one window of `O(1)` stages if
   `kappa_tau = 0`." Here "its" means [R, Theorem 4.1]. The report itself
   now states that [R]'s (H1)–(H5) contain no terminal condition (Theorem A
   remarks; Section 12.2 item 6). Theorems A and B give `B = f*` only
   "with (T)". Family B on [V]'s toy shows why (T) matters. That family
   meets the other hypotheses the report checked, and every stage is exact,
   yet `B = f* - 3.19` because `P_N = 1/2 > Phi_xx = 0`. So the sentence
   is false as written. *Fix:* "Under (SH), that is, its hypotheses plus
   the terminal condition (T), `B = f*` holds …".

   The same observation bears on [R] itself. [R, Theorem 4.1] concludes
   `B = f*` from (H1)–(H5), `e_h = O(h)` and window exactness. It does not
   assume that `Phi - S_N` is minimized at `xbar_N`, although
   [R, Proposition 1.2(2)] needs every infimum to be attained, including
   the terminal one. Section 8 lists what the report changes in [R] but
   does not say this. A clause in its first bullet would record it: "[R]'s
   `B = f*` also needs a terminal condition such as (T), which (H1)–(H5)
   do not contain." (Caveat: [V]'s toy has a jump of the target `a(t)` at
   `t = 1`, so it is not a literal counterexample to [R]'s `C^3` data
   hypothesis. The mechanism, `P(T) > Phi_xx`, does not depend on that
   jump.) This concerns [R]'s statement, which the root maintains. I have
   not changed [R].

Optional (wording only; no result depends on these):

2. Summary item 2 says family B's "stage residual is exactly
   `h d^2/2 + h sigma_t omega + h^2 omega^2/4`". This is the residual
   minus its value at `zbar_t`, as Section 7.2 writes correctly
   (`rho_t - rho_t(zbar_t) = …`). Section 7.3 uses the same shorthand, so
   this is at least consistent within the report.
3. Section 7.5, paragraph *[E]'s own families*: "The anisotropic residual
   outside the linear-rate layer is `<= 1e-7` … for clin and clin.02, and
   `<= 4e-6` for cmax (numerical differentiation near `tau`)." For cmax
   this absolute number depends on the differencing scheme. Near
   `t - tau = 1e-8`, `|M|` is about `3.9e5`. My five-point stencil with
   step `0.05 (t - tau)` gives `lambda_min = -1.64` there (relative
   `4e-6`), and step `0.005 (t - tau)` gives `-1.9e-2`. The reviser's
   central difference (step `0.1 (t - tau)`) gives `+3e-6`, but its `M` is
   `0.3%` too large along `beta`. `lambda_min` cannot see that error,
   because it is one-sided in the rank-one direction. For clin.02 on A my
   stencil gives `1.04e-7`, against the log's `9.5e-8`. None of this
   affects the conclusion. Equality in (G) holds by construction
   (`continuous_family` integrates `P' = G`), and the isotropic margin
   fails robustly (item 2 above). Suggest "equality up to
   differencing error (relative to `|M|`, at most about `4e-6`)", or drop
   the cmax number.

## 4. Was anything strengthened?

New or changed material in the second revision:

- Summary item 4, the sentence after Proposition D and the Section 6
  bullet: weakened to what is proved (item 1).
- Summary item 2 and the Section 7.5 paragraph *[E]'s own families*: now
  backed by a check of all six family–example pairs. The check reproduces
  independently, and the key number at `t = T` also follows in closed form.
- Theorem A remark ("the stage conclusion does not use (T)"): correct
  ([R]'s (H1)–(H5) read).
- Section 7.2, family B stage exactness at every `N`: correct (independent
  symbolic derivation). The `revision2_checks.py famB` "rational
  arithmetic" check only evaluates `toy.py`'s Hessian formula at
  `h = 1/500`. The text describes it accurately, and the formula itself is
  right.
- Summary "What still works": the claim that the recursion breaks for all
  small `h` on interior-stage grids is new. It is a correct corollary of
  Proposition D (item 4 above).
- Consequence paragraph and Section 8: weakened to `B <= J(zbar) - c h^2`
  plus the conditional contradiction (item 5).
- 7.6 table and stage-loss bound: corrected to the log values (item 3).

Nothing was made stronger than its proof or check.

## 5. Commands run and files

All from `reviews/window-exactness-confirm-r2-checks/` with
`OMP_NUM_THREADS=1`. These were targeted checks only: no project-wide
verification, CI not inspected, nothing committed.

1. `python3 d2_famB_rmax.py > logs/d2_famB_rmax.log` → `logs/d2_famB_rmax.json`
   (under 5 s). Symbolic family-B residual from the definitions (sympy);
   read-only analysis of the report's `logs/toy_rmax.json`.
2. `python3 d1_shE.py > logs/d1_shE.log` → `logs/d1_shE.json` (about 15 s).
   Own piecewise-polynomial `sigma`, own `tau`, own five-point `P'`; [E]'s
   `continuous_family` and `find_switch` imported read-only.
3. `python3 d3_cmax_aniso_probe.py > logs/d3_cmax_aniso_probe.log`
   (about 10 s): the cmax anisotropic residual on A near `tau+` for two
   differencing schemes and several steps (numbers quoted in Section 3,
   item 3).
4. Read-only inspection of `theory-bangbang/window/revision2_checks.py`,
   `logs/revision2_*.{log,json}`, `logs/toy_scip.json`,
   `theory-bangbang/n2/n2_windows.py` and `model.py`, and of [R] and [E] as
   listed at the top. No web searches. The reviser's scripts were not
   re-run, because my own code reproduces their outputs.

## 6. Limits

- Proof checks are by hand, for logic and the order of constants. I did not
  re-derive numeric constants such as the 128 in `K_0`, and I did not
  re-check round-1 items beyond what the six round-2 items touch.
- The two-state margin checks are float screening, like the report's. The
  near-`T` value is also confirmed in closed form.
- No literature was re-examined in this round, since the revision made no
  new literature claims.
