# Confirmation review (round 3) of `theory-bangbang/window-exactness.md`

Date: 2026-09-30. Reviewer: fresh, independent referee. I did not write the
report or the earlier reviews. I read the third revision in full where it
changed (header; Summary items 2 and 4; the Consequence paragraph;
Section 0.3; Sections 7.1–7.3 and 7.5; Sections 8, 9 and 11; Section 12.3)
and read the rest for consistency. I also read the round-3 review
(`reviews/window-exactness-confirm-r2.md`) and its logs, the reviser's new
script `theory-bangbang/window/revision3_checks.py` and its three logs, and
the parts of [R] (`theory-bangbang/report.md`) that the revision cites:
Section 0, Definition 1.1, Proposition 1.2, Theorem 2.3, Theorem 4.1 with
its Scope paragraph, the Summary paragraph on [V]'s toy, and Remark 3.3. I
checked each item from scratch and recomputed every new or changed number
with my own code. Check scripts and logs are in
`reviews/window-exactness-confirm-r3-checks/`.

## Verdict

**All three round-3 items are resolved correctly. Every new or changed
number reproduces with independent code. The refusals are reasonable.
Nothing was made stronger than its proof or check.** The main fix is
sound: the Consequence paragraph now requires (SH), including (T). The new
claim that [R, Theorem 4.1]'s `B = f*` lacks a terminal hypothesis follows
from [R, Proposition 1.2(2)], and the report states the needed caveat about
the jump in the toy's target.

What remains is minor and optional (Section 3). The main point concerns
one new absolute figure. The report now says that `lambda_min(M) = 2 eps`
holds for cmax "numerically within `5e-6`". That figure depends on the
differencing scheme, just like the figure it replaced. Read pointwise, the
reviser's own log already exceeds it (`5.8e-6`). The other four points are
wording. None affects a theorem, a proof or a conclusion.

## 1. Item-by-item check

| # | round-3 item | what I checked | result |
|---|---|---|---|
| 1 | Consequence paragraph omitted (T); optional clause in Section 8 | **[R] read:** (H1)–(H5) of Theorem 4.1 and the regularity list after it contain no terminal condition. (H1) asks only that `Phi` be `C^2`. (H3) fixes `S_x(t, x*(t)) = psi(t)` but not `S_xx(T)`. [R]'s bound contains `inf(Phi - S_N)` (Definition 1.1, Section 0). Proposition 1.2(2) gives `B = f*` iff an optimal trajectory attains every infimum (converse when `f*` is attained), so the terminal infimum must be attained at `xbar_N`. Theorem 2.3 ((W1)–(W5)) concerns stages only. [R]'s Scope paragraph and Remark 3.3 do mention an exact terminal term (`P(T) = Phi_xx - 2 eps`), but for the constructions, not in the hypotheses of Theorem 4.1. "Regular switch" in (H2) means `sigma(tau) = 0`, `sigma_dot(tau) != 0` ([R, Section 0]), so the Consequence paragraph's gloss is accurate: (SH) = [R]'s hypotheses plus (T) plus `b(x*(tau)) != 0` (the last is not implied by regularity). **Family B terminal loss, own code** (`c1_famB_terminal.py`, independent of `toy.py`): own one-switch KKT scan and own adjoint at `N = 500 … 8000` (KKT sign violation `<= 7.5e-13`). `J` matches the logged `J` to `4.4e-16`. `p_N = 0`, so `Phi - S_N = -(x - xbar_N)^2/4` and the loss over `\|x\| <= 2` is `(2 + \|xbar_N\|)^2/4`. This equals the logged terminal losses to relative `2.3e-13` at all five `N`. At `N = 1000` in `Fraction` arithmetic the formula gives exactly the logged exact value `3.1938893123459935` (= `2546963838241/797449000000`). The stage Hessian `[[h, 0], [0, h^2/2]]` (`K_t = h + P - P`, `beta_t = P + k = 0`, `kap_t = P = 1/2`) and the terminal term indeed do not involve `a(t)`. With every stage exact and `f* = J(zbar)` (exact linear-rate certificate, earlier rounds), `B = J(zbar) - 3.19 = f* - 3.19`. **Text:** the Consequence paragraph, Summary item 2, Section 7.2, the first bullet of Section 8, the status-table rows and Section 12.3 item 1 say this consistently, with the jump caveat and "smooth-target variant not checked". Theorems A and B (Sections 3, 4) already say "with (T)". | resolved |
| 2 | "stage residual is exactly" (optional) | From the definitions: `rho_t = h[(x - a_t)^2/2 + k x u] + S_{t+1}(x + h u) - S_t(x)` with `S_t = p_t x + P (x - xbar_t)^2/2` gives gradient `(0, h sigma_t)` at `zbar_t` (discrete adjoint) and Hessian `[[h, h(P + k)], [h(P + k), h^2 P]]`. Family B (`P = 1/2`, `k = -1/2`): `rho_t - rho_t(zbar_t) = h d^2/2 + h sigma_t omega + h^2 omega^2/4`. Toy plus (`P = -1/2`, `k = 1/2`): `h d^2/2 + h sigma_t omega - (k/2) h^2 omega^2`. Summary item 2, Section 7.3 and Section 12.2 item 6 now say "minus its value at `zbar_t`"; grep finds no other occurrence of the shorthand. | resolved |
| 3 | cmax residual figure (optional) | Own code (`c2_aniso.py`), with [E]'s `continuous_family` as the object under test. On the cmax log segment I took `P` from the dense output in `lam = log(t - tau)` directly (pulled out of the closure) and differenced in `lam`, which avoids cancellation in `t`. With this scheme, `\|\|R\|\| / \|\|M\|\| <= 5.3e-8` (A) and `5.1e-8` (A0). So the interpolant satisfies `P' = G` to about `5e-8` relative, and the `4.5e-6` of the five-point `t`-stencils is differencing error, as the report says. I reproduce with the report's `t`-schemes: at `t - tau = 1e-8` on A, central (step `0.1 s`) gives `lambda_min(R) = +2.82e-6` and `lambda_max(R) = 1134`; five-point (step `0.05 s`) gives `lambda_min(R) = -1.60`; `\|M\| = 3.9e5`. Maximum relative norm: `2.9e-3` (central) and `4.49e-6`, `4.23e-6` (five-point, A, A0). The large eigenvector of `R` is parallel to `beta` (cosine `1.000000`), so "a truncation error along `beta`" is right. A central step of `0.1 s` on a `1/s`-type singularity gives a relative truncation error of about `0.3%`, consistent with `2.9e-3`. clin, clin.02: norm `9.5e-8` (A, clin.02, last arc, 4000 points), so `<= 1.04e-7` on 20000 points is plausible; relative `<= 4.8e-8`. `inf lambda_min(M) - 2 eps` is at most `7.5e-10` in absolute value (so `<= 1e-9` holds). This report's family: last arc `<= 2.57e-8` (A0', `eps = 0.02`); before the switch up to `4.77e-8` (A0', `eps = 0.1`); relative `<= 2.6e-8`. So "`<= 4.9e-8` outside the layer", "`<= 2.6e-8` relative" and the round-1 "`<= 3e-8` on the last arc" all hold. The only figure that is not robust is the new cmax `lambda_min(M)` deviation (Section 3, item 1). | resolved (one optional follow-up) |

## 2. Refusals

1. **No smooth-target variant of [V]'s toy.** Reasonable. The report does
   not claim a literal counterexample to (H1). It says the variant was not
   checked, and it bases the "missing hypothesis" statement on the proof
   structure ([R, Proposition 1.2(2)]), not on the toy. As an optional
   screening check (`c3_smooth_target.py`, float, not certified) I used the
   `C^infinity` target `a(t) = -2 tanh((t - 1)/0.05)`. The candidate
   `u = +1` on `[0, tau)`, `-1` after it satisfies the minimum-principle
   signs exactly as before, with `tau = 0.213700`,
   `sigma_dot(tau) = 1.7863` and `min |sigma|/|t - tau| = 0.44`. (The
   second root, `tau = 1.786`, violates the signs.) The discrete KKT points
   at `N = 1000, 4000` (sign violation `<= 4.4e-13`) give family B terminal
   losses of `3.190` and `3.191`. For this family `beta = 0` and
   `r_xx = 1` for any target, so the margin and convexity parts of (H3) do
   not depend on `a(t)`. This supports the report's statement that the
   mechanism does not use the jump. It does not certify `f* = J(zbar)` for
   the smooth variant, and it does not check `e_h = O(h)`. So the caveat
   in the report remains the right wording.
2. **[R] not edited.** Correct; the root maintains [R], and Section 8
   records the gap.
3. **Section 12.2 item 2 left unchanged** ("within `4e-6` of 0.04").
   Acceptable for a historical entry, since Section 7.5 and Section 12.3
   item 3 record the correction. However, round-2 item 6 received an inline
   note ("wording made exact in the third revision") and item 2 did not. A
   pointer would help (Section 3, item 5).
4. **Round-3 reviewer's scripts not re-run.** Acceptable: `revision3_checks.py`
   reproduces the quoted numbers (for example `-1.599` against the
   reviewer's `-1.641`, both "about `-1.6`"), and so does my code.

## 3. Remaining problems

All are minor or optional. No result depends on them.

1. **(Minor) New stencil-dependent figure for cmax.** Section 7.5 says:
   "`lambda_min(M) = 2 eps` there (numerically within `5e-6` for cmax and
   `1e-9` for clin and clin.02)". Section 12.3 item 3 says: "numerical
   deviation `<= 5e-6` (cmax)". The deviation occurs at
   `t - tau ~ 1e-8`, where `|M| ~ 3.9e5`. There it is float noise of
   about `1e-11` relative to `|M|`, and its size depends on the scheme:
   - The reviser's log (`logs/revision3_aniso.json`, field
     `max_dev_lambda_min_M_from_2eps`) gives a pointwise maximum of
     `5.35e-6` and `5.83e-6` on A and `5.47e-6` on A0 with the two
     five-point stencils. So the pointwise reading ("there") is already
     exceeded in the reviser's own log.
   - The infimum reading holds for the reviser's stencils (at most
     `4.75e-6` below 0.04). With my `lam`-differenced derivative the
     infimum is `4.4e-6` to `5.8e-6` below 0.04 on A, depending on the
     step (`6.1e-6` on a slightly different grid). The pointwise maximum
     reaches `7.7e-6` on A0 (`logs/c2c_cmax_lminM.log`).

   This is the same kind of problem as round-3 item 3, moved from `R` to
   `lambda_min(M)`. *Fix:* "`lambda_min(M) = 2 eps` exactly by
   construction; the computed deviation is scheme dependent (up to about
   `1e-5` for cmax near `t - tau = 1e-8`, about `2e-11` relative to `|M|`;
   `<= 1e-9` for clin and clin.02)". Alternatively, drop the cmax number.
   Apply the same change in Section 12.3 item 3.
2. **(Optional wording) Section 7.5, *Hypotheses*.** The text says: "On the
   last arc … `<= 3e-8` … Both eigenvalues are this small: outside the
   layer the norm of the difference is `<= 4.9e-8`". But `4.9e-8` is
   larger than `3e-8`. It is attained before the switch (A0',
   `eps = 0.1`: `4.77e-8` before the switch against `1.43e-8` on the last
   arc, own check). The figure that supports "this small" is the last-arc
   norm `<= 2.6e-8` (own check: `2.57e-8`), and it appears only in
   Section 12.3 and in the unlogged one-off of Section 11, item 23.
   *Fix:* "on the last arc the norm is `<= 2.6e-8`; the maximum outside
   the layer, `4.9e-8`, occurs before the switch".
3. **(Optional wording) Section 7.5, *[E]'s own families*: "For cmax, `|M|`
   grows like `1/(t - tau)`".** Since `|beta|` decays like `1/log`,
   `|M| ~ Delta|beta|^2/(2|sigma|) ~ 1/((t - tau) log^2(1/(t - tau)))`.
   The computed values are `117`, `6.27e3`, `4.87e4`, `3.9e5` at
   `t - tau = 1e-4, 1e-6, 1e-7, 1e-8`: a factor of 7 to 8 per decade, not
   10. Say "roughly like" or give the log factor.
4. **(Optional wording) Summary item 2.** "Of the hypotheses checked it
   violates only (T)" is followed by the note that the target jump is not
   allowed by (H1). Read together, the two statements seem to contradict
   each other. *Fix:* "of the calibration hypotheses checked (margins and
   terminal condition) it violates only (T)".
5. **(Optional) Section 12.2 item 2.** Add a pointer after "within `4e-6` of
   0.04": "(stencil dependent; see Section 12.3, item 3)". Round-2 item 6
   already has an inline note of this kind.

## 4. Was anything strengthened?

New or changed material in the third revision:

- Consequence paragraph: weakened. It now requires (SH), including (T) and
  `b != 0`, and it adds a correct, caveated illustration of why (T)
  matters.
- Section 8, first bullet, and the status-table row: a new claim that
  [R, Theorem 4.1]'s `B = f*` needs a terminal condition. The claim is
  supported by [R, Proposition 1.2(2)] and by [R]'s hypothesis list (read).
  Its only example violates (H1), and the text says so. It also says that
  a smooth variant was not checked, and it limits the correction to the
  statement (the stage conclusions are unaffected). The wording is not
  stronger than the evidence. My optional screening (Section 2, item 1)
  points the same way.
- Section 7.2: the terminal-loss formula is exact algebra, and I
  reproduced it independently (float at five `N`, rational at
  `N = 1000`). "It does show that … needs a terminal condition" relies on
  the Section 8 caveat, which the sentence cites.
- Section 7.5 and Section 12.3 item 3: the absolute cmax residual was
  withdrawn and replaced by relative figures, which reproduce. One new
  absolute figure is scheme dependent (Section 3, item 1). This is a
  precision issue, not a strengthened claim.
- Summary item 2 and Section 7.3: wording made exact.

Nothing was made stronger than its proof or check.

## 5. Commands run and files

All from `reviews/window-exactness-confirm-r3-checks/` with
`OMP_NUM_THREADS=1` and a `timeout`. These were targeted checks only: no
project-wide verification, CI not inspected, nothing committed.

1. `python3 c1_famB_terminal.py | tee logs/c1_famB_terminal.log` →
   `logs/c1_famB_terminal.json` (about 10 s). Own KKT scan and adjoint for
   the verifier toy at `N = 500 … 8000`, the family B terminal-loss
   formula against `theory-bangbang/window/logs/toy_verifier.json`, and a
   rational check at `N = 1000`. Independent of `toy.py`.
2. `python3 c2_aniso.py > logs/c2_aniso.log` → `logs/c2_aniso.json` (under
   a minute). Anisotropic residual `R` and `lambda_min(M) - 2 eps` for
   [E]'s cmax, clin and clin.02 on A and A0 and for this report's family on
   A−, A0' (`eps = 0.02, 0.1`), per segment. It uses my own stencils and a
   `lam`-derivative on the cmax log segment. `n2/model.py` is imported
   read-only (object under test).
3. `python3 c2b_cmax_where.py > logs/c2b_cmax_where.log` and
   `python3 c2c_cmax_lminM.py > logs/c2c_cmax_lminM.log` (seconds each).
   These locate the cmax deviations in `t - tau`, check step dependence and
   give the direction of `R` relative to `beta`.
4. `python3 c3_smooth_target.py | tee logs/c3_smooth_target.log` (seconds).
   Optional screening of a smooth-target variant (Section 2, item 1).
5. Read-only: `theory-bangbang/window/revision3_checks.py`,
   `logs/revision3_{famBterm,aniso,anisogrid}.{log,json}`,
   `logs/toy_verifier.json`, `n2/model.py` (`continuous_family`),
   `window/revision2_checks.py` (stencil of the second revision), the
   round-3 review and `d3_cmax_aniso_probe.log`, and [R] as listed at the
   top. The reviser's scripts were not re-run, because my own code
   reproduces their outputs. No web searches.

## 6. Limits

- I checked proofs only where the revision touched them (the role of (T)
  in Theorems A and B and in [R, Proposition 1.2]). I did not re-derive
  numeric constants, and I did not re-check round-1 or round-2 items
  beyond what the three round-3 items touch.
- The anisotropic-residual checks are float screening, like the report's.
  "`R = 0` by construction" was confirmed by reading `continuous_family`:
  on every piece outside the linear-rate layer it integrates `P' = G`.
- The smooth-target check is float screening. It does not certify `f*`
  and does not check `e_h = O(h)`.
- Literature: the revision makes no new literature or novelty claims, so
  none was re-examined.
