# Window exactness at a regular switch: a trichotomy, a theorem, and a counterexample

Date: 2026-09-30. Status: author's report, revised after three rounds of
independent checking (`reviews/window-exactness-review.md`,
`reviews/window-exactness-confirm-r1.md`,
`reviews/window-exactness-confirm-r2.md`); the third revision was
confirmed by `reviews/window-exactness-confirm-r3.md` (verdict: verified),
whose remaining wording items the root applied (Section 12.4). The changes
are listed in Section 12.
Proofs are complete unless labelled "sketch" or "heuristic". Numbers are
floating-point screening unless marked **exact** (rational arithmetic) or
**SCIP** (global solver, float tolerances). Scripts and logs:
`theory-bangbang/window/` and `theory-bangbang/window/logs/`.

Cited notes:

- **[R]** `theory-bangbang/report.md` (Definition 1.1, Lemma 2.1,
  Theorem 2.3, Proposition 3.1, Theorem 4.1);
- **[E]** `theory-bangbang/extension-n2.md` (Lemma 10, Proposition 13,
  Section 2.5, examples A, A0, B, C);
- **[S]** `theory-calibration/scouting.md` (Proposition 4.4, Sketch 5.4 and
  the "Question (transfer at switches)");
- **[V]** `reviews/bangbang-verification/verification-report.md` and its
  toy `v_window_toy.py`;
- reviews read for context: `reviews/bangbang-root-fixes-confirm.md`,
  `reviews/bangbang-n2-review.md`, `reviews/calibration-review.md`,
  `reviews/calibration-recheck.md`.

## Summary

**Question.** [R, Theorem 4.1] proves that a transferred strict tangential
calibration is exact at every stage outside an `O(1)`-stage window around a
regular switch (when `e_h = O(h)`), and concludes `B = f*` only under an
extra assumption: the discrete trajectory attains the infimum of the window
relaxation ("window exactness"; open item "uniform conditioning of switch
windows"). Is window exactness a theorem?

**Answer: it depends on the sign of one number.** Let

```
kappa_tau := b(x*(tau))^T w,        w = -grad_x sigma_0(tau, x*(tau)),
```

the *switch self-curvature*. For every calibration that is `C^2` in the
state and exact on the trajectory, tangency ([R, Proposition 3.1]) gives
`b^T S_xx b = kappa_tau` at the switch, so `h^2 kappa_tau` is, up to
`o(h^2)`, the curvature in `u` of every Euler stage residual near the switch
(Proposition 1.2). It is fixed by the data, not by the calibration.

1. **Decoupling (Proposition 2.1).** For a window of a bounded number of
   stages near the switch, the window value differs from the sum of the
   stage-wise minima by `O(h^3)`, and each stage loss equals, up to
   `O(h^3)`, the loss of the scalar problem
   `min_u [h sigma_t (u - ubar_t) + h^2 kappa_tau (u - ubar_t)^2 / 2]`.
   So at order `h^2` an `O(1)`-stage window is no better than stage-wise
   checks: the window's controls interact only at order `h^3`.
2. **`kappa_tau > 0`: no window is needed (Theorem A).** Every stage is
   exact for all small `h`, and the rate used drops from `e_h = O(h)` to
   `e_h <= c_* sqrt(h)`, where `c_*` is a specific small constant (so
   `e_h = o(sqrt(h))` suffices). This removes the window-exactness
   assumption from [R, Theorem 4.1] in this case. The stage conclusion does
   not use the terminal condition (T) of (SH); (T) is needed only for
   `B = f*`. So, up to the rate hypothesis on `e_h` (not verified there),
   Theorem A explains the observation that [V]'s tangential family
   (family B) has no failing stage `1 … N-1` in [V]'s toy
   (`kappa_tau = +0.5`): family B meets the isotropic margin of (SH)
   (Section 7.1), and of the calibration hypotheses checked (margins and
   terminal condition) it violates only (T). (The
   toy's target `a(t)` also jumps at `t = 1`, away from `tau`, which the
   `C^3` data hypothesis (H1) does not literally allow; noted in the third
   revision.) For
   family B the stage exactness is in fact immediate at every `N`, with no
   rate hypothesis: its stage residual minus its value at `zbar_t` is
   exactly `h d^2/2 + h sigma_t omega + h^2 omega^2/4` (Section 7.2). The
   same observation for [E]'s examples A and A0
   (`kappa_tau = +0.3`) is consistent with Theorem A but not covered by it:
   the three continuous tangential families [E] screened there (cmax, clin,
   clin.02) all lie outside (SH), and its fourth family without failures
   (rmax) is discrete, so (SH) does not apply to it (Section 7.5).
3. **`kappa_tau = 0`: window exactness is a theorem (Theorem B).** At most
   one stage can fail, it fails only at order `h^3`, and the window of
   `2K_0 + 1` stages centred on it is exact for all small `h`, with `K_0`
   independent of `h` (it is proportional to the stage's `h^3` deficit
   constant `C_4` divided by the strictness `mu'`). Here the window's controls do
   interact: the deviation `h b omega` created at the failing stage is
   carried by the state through the neighbouring stages, whose strict
   convexity in the state pays for it. `kappa_tau = 0` holds for every
   problem with `b` constant and `grad l_1(x*(tau))^T b = 0`, e.g. `b`
   constant and `l_1 = 0`. optcdeg2 is of this kind, but it has two
   switches and the terminal row `v_N = 0`, so it is outside (SH) and
   Theorem B does not apply to it as stated.
4. **`kappa_tau < 0`: counterexample (Theorem C).** If the discrete KKT point
   has an interior (fractional) control at a stage `n` in the window, then
   every window of `o(1/h)` stages with the calibration at its exit has
   value at least `h^2 |kappa_tau| omega_hat^2 / 2 (1 - o(1))` below the
   trajectory, with `omega_hat >= Delta/2`; a similar bound holds at a
   vertex stage with `|sigma_n| <= (1 - delta) h Delta |kappa_tau| / 2`.
   For LQ-structured data the same bound holds for every quadratic family
   with the discrete costate slopes that is exact **over `R^n x U`** at
   every stage after the window and at the terminal, when the window's exit
   lies `o(1/h)` stages after the switch (Proposition D). In that case the
   proof shows only that the excess of the exit curvature `b^T P_b b` over
   `b^T w` has `limsup <= 0`. For an exit a bounded number of stages after
   the switch, the proof shows that this excess is at most
   `O((log(1/h))^{-1/2})`. That the excess decays like `1/log(1/h)`, and
   not faster, is a heuristic (leading-order law and numerics). Families
   that are exact only over the state boxes, which is what a certificate
   needs, are not covered. Branching on the fractional control with a fixed
   family prunes no node (Proposition E). A window can repair the defect
   only if it lasts at least a fixed time `l_0 - o(1)` after the fractional
   stage (Theorem C(iii); `l_0 = |kappa_tau| / (C_M |b|^2)` when `a` and `b`
   do not depend on the state), i.e. `Omega(1/h)` stages. This is a
   necessary condition only: no window that stops before the end of the
   horizon is shown to be exact.

**What still works when `kappa_tau < 0`** (Section 6): the certificate
itself, with a proved gap of order at most `h^2` (on the toy below, 0.35–0.53
`h^2` on the grids with an interior stage and 0–0.018 `h^2` on the
others); exact certificates on the grids without an interior stage and
with enough vertex margin, when `e_h = o(sqrt(h))` (predicted fraction of
grids `D/F''(tau)`, observed 0.29 against 0.27); and, at practical `h`, the
discrete maximal recursion of [E, Lemma 10]. That recursion gives an exact
certificate whenever it does not break ([E, Lemma 10]). For LQ data, at an
interior stage it continues only if `|kappa_tau| < eta_hat_1`, where the
excess `eta_hat_1` has `limsup <= 0` as `h -> 0` (Proposition D; positive
in all runs, and heuristically decaying like `1/log(1/h)`; Section 7.6).
So, under the hypotheses of Proposition D, it breaks for all small `h` on
grids with an interior stage. The condition `|kappa_tau| < eta_hat_1` is
necessary only; no sufficient condition for the recursion not to break is
proved. In float it does not break at any tested `N <= 32000` for
`kappa_tau = -0.1` and `-0.05`, and it breaks at every tested `N` with an
interior stage for `kappa_tau = -0.5`. On the toy with `kappa_tau = -0.5`, a
trivial convexification bound is tighter than every window certificate
tested (Section 6).

**Numerical checks** (Section 7).

- *[V]'s toy* (`kappa_tau = +0.5`): a transferred linear-rate tangential
  family gives an **exact** rational certificate with gap exactly 0 at
  `N = 500, 1000, 2000, 4000, 8000`, with no window. [V]'s tangential
  family B, which has no failing *stage*, has an **inexact terminal term**
  (`P_N = 1/2 > Phi_xx = 0`; terminal loss 3.19, exact at `N = 1000`): its
  bound is valid but 3.19 below `f*`, so it is not an exact certificate.
  Neither [R] nor [V] claimed it as one.
- *Toy with `kappa_tau = -0.5`* (same dynamics, `k = +0.5`): window deficits
  for `K = 0 … 4` stages on each side are 0.3888, 0.3877, …, 0.3853 `h^2`
  at `N = 1000`, against the prediction 0.3888 (exact rational values for
  `K <= 2` and for the single-flip upper bound). SCIP finds the global
  optimum of the transcription equal to the KKT value to `1e-9` at
  `N = 50 … 200`, so the window bound is strictly below `f*` (by
  `9.2e-4 … 3.1e-5`).
- *Toy with `kappa_tau = 0`*: with a deliberately curved tangential family,
  the fractional stage fails at order `h^3` (0.04–0.43 `h^3`); the window
  with one stage on each side has minimum **exactly 0** (exact rational, at
  an exact rational KKT point) at `N = 1000, 4000, 8000`.
- *Two-state examples of [E]*: example A (`kappa_tau = +0.3`) has no failing
  stage; the same data with `k_2 = +0.3` (`kappa_tau = -0.3`) has window
  deficits 0.20–0.47 `h^2` that windows with `K <= 3` reduce by at most 6%;
  with `k_2 = 0` (`kappa_tau = 0`) the defect is `O(h^3)` and is removed by
  windows of 4 stages per side when the family's strictness is `eps = 0.1`
  (float Schur certificate at `N = 1000, 4000`), and of 16–32 stages when
  `eps = 0.02` (single-direction bound; certified at `N = 4000` only)
  (Section 7.5). These families satisfy [E]'s anisotropic global-form
  condition with equality, not the isotropic margin of (SH), so the
  two-state rows are consistent with Theorems A–C but are not instances of
  them.
- *Discrete switching structure*: the fraction of grids whose KKT point has
  an interior stage is predicted by a phase model as
  `Delta^2 (kappa_tau + eta_L) / F''(tau)`: 0.820, 0.547, 0.727 predicted
  against 0.816, 0.528, 0.708 observed on 250 grids for the three toys.

**Consequence for [R, Theorem 4.1].** Under (SH), that is, its hypotheses
plus the terminal condition (T) and `b(x*(tau)) != 0` (Section 0.3),
`B = f*` holds without a window if `kappa_tau > 0` (with
`e_h <= c_* sqrt(h)`), and with one window of `O(1)` stages if
`kappa_tau = 0` (with `e_h = O(h)`). (T) matters: on [V]'s toy, family B
has every stage exact, yet `B = f* - 3.19` because `P_N = 1/2 > Phi_xx = 0`.
That toy's target jumps at `t = 1`, so it lies outside [R]'s smooth-data
hypothesis (H1), but the mechanism does not use the jump (Section 7.2;
Section 8, first bullet). If
`kappa_tau < 0`, then along any sequence of grids whose KKT points have an
interior stage, for all small `h` the certificate with windows of `o(1/h)`
stages gives `B <= J(zbar) - c h^2` (`c > 0`), so it cannot prove optimality
of `zbar` (by the phase model such grids are a positive fraction; 53% on the
toy). This contradicts `B = f*` when `f* = J(zbar)`, as on the toy of
Section 7.3, where SCIP finds `f* = J(zbar)` to about `1e-9` at
`N <= 200`. The answer to the question of [S] ("windows of at most `W`
stages, `W` independent of `h`") is yes for `kappa_tau >= 0` and no for
`kappa_tau < 0` on such grid sequences, within transferred `C^2` calibrations (Theorem C)
and, for LQ data, within all quadratic families with costate slopes that
are exact over `R^n x U` after a window exit `o(1/h)` stages after the
switch (Proposition D).

## 0. Setting, window relaxation, standing hypotheses

**0.1 Data.** As in [R, Section 0]: Euler transcription with
`f_t(x,u) = x + h g(x,u)`, `g = a(x) + b(x) u`,
`L_t = h (l_0(x) + l_1(x) u)` (time dependence of `a`, `l_0` allowed if
smooth near `tau`), scalar control `u in U = [u_-, u_+]`, `Delta = u_+ - u_-`,
state enclosures `D_t` (convex, compact). A calibration family `S_t` has
stage residuals `rho_t = L_t + S_{t+1} o f_t - S_t`. A discrete KKT point is
`zbar = (xbar, ubar)` with costates `p` and switching values
`sigma_t = l_1(xbar_t) + b(xbar_t)^T p_{t+1}`. Write `s_t = |t_t - tau|`
(`t_t = t h`), `d = x - xbar_t`, `omega = u - ubar_t`,
`omega_hat_t = max(ubar_t - u_-, u_+ - ubar_t)`.

**0.2 Window relaxation.** For consecutive stages `W = {a, …, b-1}` and an
entry set `E`, let

```
J_W(z)  = sum_{t in W} L_t(x_t, u_t) + S_b(x_b) - S_a(x_a),
beta_W(E) = inf { J_W(z) : x_a in E, x_{t+1} = f_t(x_t, u_t), u_t in U, x_t in D_t }.
```

This is [R, Definition 1.1] with the dynamics kept, the state constraints
`x_t in D_t` kept (keeping constraints is allowed there; it only helps), the
calibration `S_b` at the exit and no dualized rows. The window is **exact**
if `beta_W(D_a) = J_W(zbar)`. "Entry set a small ball" means
`E = B_r(xbar_a) cap D_a`; Lemma 0.1 shows the two versions agree.

**0.3 Standing hypotheses (SH).** The hypotheses of [R, Theorem 4.1] —
(H1)–(H5) together with the time regularity of `partial_t S` listed after
it — for a sequence `h -> 0`, and in addition:

- **(T)** the terminal term is exact: `Phi - S^h_N` attains its minimum over
  `D_N` at `xbar_N` (for LQ data this follows from `P(T) <= Phi_xx`; in
  general from the terminal part of [E, Proposition 12]);
- `b(x*(tau)) != 0`, and `gamma := |sigma_dot(tau)| > 0` (regular switch;
  for scalar control-affine problems `sigma_dot` does not depend on `u`, so
  it is continuous at `tau`).

`S^h_t = S(t_t, .) + a_t^T x` is the transferred family of [R, Theorem 4.1].
The proof of that theorem (steps (a)–(e)) gives, for small `h`, with
constants independent of `h` and on `B_t := B_r(xbar_t) cap D_t`:

- **(P1)** `grad_x rho_t(zbar_t) = 0`, `d_u rho_t(zbar_t) = h sigma_t`, and
  `sigma_t (u - ubar_t) >= 0` for all `u in U`.
- **(P2)** `grad_x^2 rho_t(x,u) >= h mu' I` on `B_t x U`.
- **(P3)** `d_u^2 rho_t(x,u) = h^2 kappa_t(x,u)` with
  `kappa_t(x,u) = b(x)^T grad^2 S^h_{t+1}(f_t(x,u)) b(x)` and
  `|kappa_t(x,u) - kappa_tau| <= C_kappa (s_t + |x - xbar_t| + e_h + h)`
  (Proposition 1.2).
- **(P4)** `beta_t := grad_x d_u rho_t(zbar_t) / h` satisfies
  `|beta_t| <= L s_t + C_beta (e_h + h)`; `|grad_x d_u^2 rho_t| <= C h^2`
  and `||grad_x^2 rho_t|| <= C_M h` on `B_t x U`.
- **(P5)** `|sigma_t - sigma(t_t)| <= C_sigma e_h`, and
  `gamma_1 |t - tau| <= |sigma(t)| <= gamma_2 |t - tau|` for
  `|t - tau| <= delta_sigma` ([R, (W2)]); the margin (W5) of [R] holds with
  `mu'`.
- **(P6)** far region: `rho_t(z) >= rho_t(zbar_t)` for `x in D_t` with
  `|x - xbar_t| >= r/2`, `u in U` ([R, (W4)/(H5)] at radius `r/2`).
- **(P7)** `|f_t(x,u) - x| <= G h`, and
  `|g(xbar + d, ubar + omega) - g(xbar, ubar) - b(xbar) omega| <= C_g |d|`.

*On `mu'`.* [R, Theorem 4.1, step (c)] used `h mu / 2`, while (W5) of
[R, Theorem 2.3] is then needed with `mu/2`, i.e. twice the (H3) margin.
Any `mu' < mu` works for (P2) for small `h`, and (H3)'s strict margin,
compactness away from `tau` and, near `tau`, `|beta(t)| <= L|t - tau|`
(tangency plus Lipschitz `S_xx`; see (P4)) against
`|sigma| >= gamma_1 |t - tau|` give (W5) with some `mu' < mu` (wording
sharpened by the root after a check of the root edits). We use such a `mu'`. (This closes a factor-2 slip in the proof of
[R, Theorem 4.1]; no conclusion there changes. The root applied this
correction to [R, Theorem 4.1, step (c)] on 2026-09-30, and also added the
terminal hypothesis of Section 8 to [R]'s statement.)

*On the rate `e_h = O(h)`* (added after review). Proposition 2.1,
Theorem B and Proposition D assume `e_h <= C_e h`. Osmolovskii–Veliov
(ESAIM:COCV 26 (2020) 47, Theorem 5.1) prove
`||x^h - xhat||_{1,1} + ||u^h - uhat||_1 + ||p^h - phat||_{1,1} <= C h`,
assuming strong metric subregularity (SMsR) of the continuous optimality
map. The theorem is stated for solutions of the discrete problem with their
costates, but its proof uses only the discrete Euler optimality system
(their (5.1)–(5.3)), so it covers discrete KKT points near the reference. For purely
bang-bang controls whose switching function grows linearly at its zeros,
their Corollary 4.2 gives SMsR under a second-order bound
`2 Omega(dx, du) >= -mu_0 ||du||_1^2` with `mu_0 < mu`. Their norm satisfies
`||x||_inf <= ||x||_{1,1}`, so this gives `e_h = O(h)` for states and
costates in `L^infinity`. Their setting differs from ours: Lagrange-type
cost with no terminal term (`p_N = 0`), data Lipschitz in `t` (their (C1);
the toys of Section 7 have a jump of `a(t)` at `t = 1`), and the a-priori
assumption (C3) that the discrete solution lies near the reference. The
transfer to terminal costs `Phi` and to the toys is not checked here.

**Lemma 0.1 (telescoping; entry reduction).** (1) For any functions `S_t`
on the interior stages, `J_W(z) = sum_{t in W} rho_t(z_t)` along the window
dynamics, so `J_W(z) - J_W(zbar) = sum_{t in W} [rho_t(z_t) - rho_t(zbar_t)]`.
(2) Under (P6), (P7), if `|W| h <= r / (8 G)` and `h` is small, every window
trajectory with `|x_a - xbar_a| >= r` has `J_W(z) >= J_W(zbar)`. Hence
`beta_W(D_a) = J_W(zbar)` iff `beta_W(B_r(xbar_a) cap D_a) = J_W(zbar)`.
(3) *(Near the switch; added after review.)* Assume also (P1)–(P5),
`e_h <= C_e h`, `|W| <= Kbar` and `s_t <= C_W h` for `t in W`. Then for small
`h`, `rho_t(z) >= rho_t(zbar_t)` for every `t in W` and every
`z in D_t x U` with `|x - xbar_t| >= r/4`. Hence every window trajectory
with `|x_a - xbar_a| >= r/2` has `J_W(z) >= J_W(zbar)`, so it suffices to
consider entries in `B_{r/2}(xbar_a)`; their window states lie in
`B_{3r/4}(xbar_t) subset B_t`.

*Proof.* (1) The `S_t` telescope. (2) `|x_t - x_a| <= G h |W|` and
`|xbar_t - xbar_a| <= G h |W|`, so `|x_t - xbar_t| >= r - 2 G h |W| >= r/2`
for all `t in W`; apply (P6) at every stage and (1). (3) For
`|x - xbar_t| >= r/2` use (P6). For `r/4 <= |d| < r/2` the point is in
`B_t`, and Lemma 0.2 (before minimizing over `d`, dropping the
nonnegative first-order term) gives
`rho_t(z) - rho_t(zbar_t) >= -C h^2 - C h^2 |d| + (h mu'/2) |d|^2`, because
`|beta_t| <= L C_W h + C_beta (C_e h + h) = O(h)` by (P4) and `kappa_t^-` is
bounded. This is `>= h [mu' r^2 / 32 - C h (1 + r)] >= 0` for small `h`.
Since `2 G h |W| -> 0`, entries with `|x_a - xbar_a| >= r/2` keep
`|x_t - xbar_t| >= r/4` at every `t in W`, and entries in
`B_{r/2}(xbar_a)` keep `|x_t - xbar_t| < 3r/4`. Sum with (1). □

**Lemma 0.2 (stage lower bound).** Under (P1)–(P4), for `z = (xbar_t + d,
ubar_t + omega) in B_t x U`,

```
rho_t(z) - rho_t(zbar_t) >= h|sigma_t||omega| + (h^2/2) kappa_t^- omega^2
                            + h omega beta_t^T d - C h^2 omega^2 |d| + (h mu'/2) |d|^2,
```

with `kappa_t^- = min_{u in U} kappa_t(xbar_t, u)`. Minimizing over `d`:

```
rho_t(z) - rho_t(zbar_t) >= h|sigma_t||omega| + (h^2/2) omega^2 [kappa_t^- - (|beta_t| + C h Delta)^2 / (h mu')].
```

*Proof.* This is [R, Lemma 2.1] before its last step: move `u` at `xbar_t`
(Taylor in `u`, (P1), (P3)), then move `x` at fixed `u` (strong convexity
(P2) on the convex set `B_t`; `grad_x rho_t(xbar_t, u) = h omega beta_t +
O(h^2 omega^2)` by (P1), (P4)). □

## 1. The switch self-curvature

**Definition 1.1.** `kappa_tau := b(x*(tau))^T w`, with
`w = -grad_x sigma_0(tau, x*(tau))` and `sigma_0 = l_1 + b^T psi`.

**Proposition 1.2 (every `C^2` calibration sees the same `kappa_tau`).** If
`S` satisfies the hypotheses of [R, Proposition 3.1], then
`b^T S_xx(tau, x*(tau)) b = kappa_tau`. For the transferred family of
[R, Theorem 4.1], `d_u^2 rho_t(x,u) = h^2 kappa_t(x,u)` with (P3).

*Proof.* Proposition 3.1 of [R] gives `S_xx b = w` at `(tau, x*(tau))`;
multiply by `b^T`. For Euler data `L_t` and `f_t` are affine in `u`, so
`d_u^2 rho_t = h^2 b^T grad^2 S^h_{t+1}(f_t) b` with
`grad^2 S^h_{t+1} = S_xx(t_{t+1}, .)`; (P3) follows from the Lipschitz
continuity of `S_xx` in `t` and `x` and `|f_t(x,u) - x*(tau)| <=
|x - xbar_t| + e_h + C(s_t + h)`. □

So the sign of `kappa_tau` is a property of the transcription, not of the
calibration. It is **not** invariant under reformulations that are
equivalent in continuous time. If `b` is constant and `l_1 = grad G^T b`,
the problem can be rewritten with `l_1 = 0`, running cost
`l_0 - grad G^T a` and terminal cost `Phi + G` (because `l_1 u = dG/dt -
grad G^T a`). The Euler transcription of the rewritten problem has
`kappa_tau = 0` and differs from the original one by
`sum_t (h^2/2) (a + b u_t)^T grad^2 G (a + b u_t) + O(h^3)`, a separable
term in the controls; `eta_L` and `F''(tau)` do not change. The toys "plus"
and "zero" of Section 7 are such a pair (`kappa_tau = -0.5` and `0`, both
with `eta_L = 2.0226`).

**Lemma 1.3 (discrete switching increments).** For smooth data and stages
near `tau`,

```
sigma_{t+1} - sigma_t = h sigma_dot(tau) + h (ubar_{t+1} - ubar_t) kappa_tau + O(h (s_t + e_h + h)).
```

*Proof.* With `v := grad l_1 + b_x^T p` evaluated at `(xbar_t, p_{t+2})`,
`x_{t+1} - x_t = h g(xbar_t, ubar_t)` and the discrete adjoint
`p_{t+1} - p_{t+2} = h grad_x H(xbar_{t+1}, ubar_{t+1}, p_{t+2})`,

```
sigma_{t+1} - sigma_t = h [v^T a - b^T (grad l_0 + a_x^T p)] + h (ubar_t - ubar_{t+1}) b^T v + O(h^2).
```

The bracket is the `u`-independent expression of `sigma_dot`, and
`-b^T v -> b^T w = kappa_tau` at `(x*(tau), psi(tau))`; the errors are
Lipschitz in `(x, p)`. □

Across a complete switch the controls change by `Delta` against the sign of
`sigma_dot`, so the total change of `sigma` across the switch is
`h (gamma - Delta kappa_tau)` in magnitude. Positive `kappa_tau` shrinks the
jump; if `gamma < Delta kappa_tau`, two adjacent interior controls become
possible. This is consistent with [E]'s observation of two adjacent
fractional stages in examples A0 (`gamma = 0.326 < Delta kappa_tau = 0.6`)
and B (`1.533 < 2.4`) and their absence in example A (`1.641 > 0.6`).

**Remark 1.4 (phase model; heuristic, checked numerically).** Let
`F_h(theta)` be the discrete cost of the controls that switch at the
continuous stage position `theta` (one interior control at stage
`floor(theta)`). Within a stage `F_h` is quadratic with curvature
`h^2 Delta^2 b^T Q b = h^2 Delta^2 (kappa_tau + eta_L)` (Remark 1.5), and its
average curvature is `h^2 F''(tau) = h^2 (D + Delta^2 eta_L)` ([E,
Proposition 6]). So at integers the slope jumps by `h^2 (D - Delta^2
kappa_tau)`. If `D > Delta^2 kappa_tau` and the phase of `tau/h` is
equidistributed, the KKT point has an interior stage for a fraction
`Delta^2 (kappa_tau + eta_L) / F''(tau)` of the grids; and when `kappa_tau <
0`, a vertex stage with `|sigma_t| < h Delta |kappa_tau| / 2` occurs for a
further fraction `Delta^2 |kappa_tau| / F''(tau)` (the one-sided slopes
`h Delta |sigma_{s-1}|` and `h Delta |sigma_s|` add up to
`h^2 (D - Delta^2 kappa_tau)`). The transferred family is then stage-wise
exact near the switch on a fraction `D / F''(tau)` of the grids. Section 7.7
checks both fractions.

*Relation to the Osmolovskii–Maurer form* (added after review). The kink
jump `D - Delta^2 kappa_tau` is the switch term of the O–M quadratic form in
the notation of [E, Section 3]: `D xi^2 + 2[H_x] xbar_av xi` with
`[H_x] = -w^T Delta u` and `xbar_av = b Delta u xi / 2` (fixed `x_0`, `xbar = 0`
before `tau`), so `2[H_x] xbar_av xi = -Delta^2 kappa_tau xi^2`. The
within-stage curvature `Delta^2 b^T Q b` is the O–M arc term, and the two add
up to `F''(tau)`. So `kappa_tau` itself is a known quantity:
`-Delta^2 kappa_tau` is the classical O–M cross term at the switch. What this
note adds is its role as the `u`-curvature of every tangential stage
residual (Proposition 1.2) and the consequences for windows. Check
(`revision_checks.py om`): `(D - Delta^2 kappa_tau) + Delta^2 b^T Q(tau+) b`
equals `F''(tau)` from finite differences of the continuous cost to within
`5.3e-10` on [E]'s examples A, A− and A0' (`kappa_tau = +0.3, -0.3, 0`). Given
`eta_L = b^T Q b - kappa_tau` the split is an algebraic identity; the
finite differences check the total, as [E] already did, and the sign of
the cross term was checked by hand against [E]'s formulas.

**Remark 1.5 (the discrete Hessian of the window controls).** In the
scalar toy of Section 7 the reduced objective is an exact quadratic with
`d^2 J / du_i du_j = h^2 [h (N - 1 - max(i,j)) + phi_2 + k (1 - delta_ij)]`
(`toy.hessian`). Near the switch this is
`h^2 [eta_L 1 1^T + kappa_tau I] + O(h^3)` with `kappa_tau = -k` and
`eta_L = Q(tau+) + k`. A heuristic expansion (not written out here) gives
the same form for general Euler data. The rank-one part is the net shift of
the switch, whose curvature `eta_L` is spread over the whole last arc; the
diagonal part is the stage's self-interaction. A tangential exit calibration
keeps only the diagonal part (its net-shift curvature is
`b^T(P_b b - w) -> 0`), which is the mechanism behind Sections 2 and 5.

## 2. Decoupling: bounded windows gain only `O(h^3)`

For `t` near the switch define the scalar stage loss

```
m_t := min_{u in U} [ h sigma_t (u - ubar_t) + (h^2/2) kappa_tau (u - ubar_t)^2 ]  <= 0 .
```

If `kappa_tau >= 0` then `m_t = 0`. If `kappa_tau < 0`, then
`m_t = -h^2 |kappa_tau| omega_hat_t^2 / 2` at an interior stage
(`sigma_t = 0`) and `m_t = min(0, h |sigma_t| Delta - h^2 |kappa_tau|
Delta^2 / 2)` at a vertex stage.

**Proposition 2.1 (decoupling).** Assume (SH) with `e_h <= C_e h`. Let
`W_h` be windows of at most `Kbar` stages with `s_t <= C_W h` for
`t in W_h` (`Kbar`, `C_W` fixed). Then for small `h`

```
| beta_W(D_a) - J_W(zbar) - sum_{t in W} m_t | <= C h^3,
| inf_{D_t x U} rho_t - rho_t(zbar_t) - m_t |  <= C h^3   (t in W).
```

So an `O(1)`-stage window improves the stage-wise bound by `O(h^3)` only.

*Proof.* In the window, (P3)–(P4) and `e_h <= C_e h` give
`kappa_t^- >= kappa_tau - C h` and `(|beta_t| + C h Delta)^2 / (h mu') <=
C h`. *Lower bound.* At each `t in W` and every `z in D_t x U`:
on `B_t x U`, Lemma 0.2 (minimized over `d`) gives
`rho_t(z) - rho_t(zbar_t) >= min_omega [h |sigma_t| |omega| + (h^2/2)
omega^2 (kappa_tau - C h)] >= m_t - C h^3`; outside `B_t`, (P6) gives
`rho_t(z) >= rho_t(zbar_t) >= rho_t(zbar_t) + m_t`. Sum with
Lemma 0.1(1); this holds for every entry, so no entry reduction is needed.
(Revised after review: the first version reduced to entries in
`B_{r/2}(xbar_a)` via Lemma 0.1(2), which is stated at radius `r`.)
*Upper bound.* Take `x_a = xbar_a` and at each stage the minimizer
`omega*_t` of `m_t`. Then `|d_t| <= C Kbar h`. At each stage, the `u`-move
at `xbar_t` costs at most `m_t + C h^3`, and the `x`-move at fixed `u`
costs at most `|grad_x rho_t(xbar_t, u_t)| |d_t| + C_M h |d_t|^2 / 2 <=
C h^2 |d_t| + C h |d_t|^2 = O(Kbar^2 h^3)` because
`grad_x rho_t(xbar_t, u_t) = h omega beta_t + O(h^2) = O(h^2)`. Summing,
`beta_W - J_W(zbar) <= sum m_t + C Kbar^3 h^3`. The stage statement is the
case `|W| = 1` (upper bound with `d = 0`). □

## 3. `kappa_tau > 0`: no window is needed

**Theorem A.** Assume (SH) and `kappa_tau > 0`. There are `c_*, h_0 > 0`
such that, if `e_h <= c_* sqrt(h)` and `h <= h_0`, every stage is exact over
`D_t x U`. With (T), `B(S^h) = J(zbar)`, so `f* = J(zbar)` and the
certificate is exact with no window.

*Proof.* By Lemma 0.2 it suffices that for all `|omega| <= Delta`

```
(*)   |sigma_t| + (h|omega|/2) [kappa_t^- - (|beta_t| + C h Delta)^2 / (h mu')] >= 0 ,
```

and (P6) covers states outside the ball. Fix `delta_0 <= kappa_tau /
(4 C_kappa)`; for `s_t <= delta_0` and small `h`, (P3) gives `kappa_t^- >=
kappa_tau / 2`.

(i) *Near zone.* If `(|beta_t| + C h Delta)^2 <= h mu' kappa_tau / 2`, the
bracket in (*) is `>= 0`. By (P4) this holds when `L s_t <= sqrt(h mu'
kappa_tau / 8)` and `C_beta e_h + C' h <= sqrt(h mu' kappa_tau / 8)`; the
second holds for small `h` if `c_* <= sqrt(mu' kappa_tau / 8) / (2 C_beta)`.
So all stages with `s_t <= s_1(h) := sqrt(h mu' kappa_tau / 8) / L` are
exact, including the interior and the switching stages.

(ii) *Intermediate zone* `s_1(h) <= s_t <= delta_2 := min(delta_0,
delta_sigma, gamma_1 mu' / (4 Delta L^2))` (`delta_sigma` from (P5); added
after review). By (P5), `|sigma_t| >= gamma_1 s_t - C_sigma e_h`, and
the bracket is `>= -(2/(h mu'))(L^2 s_t^2 + (C_beta e_h + C' h)^2)`. So (*)
follows from `gamma_1 s_t - C_sigma e_h >= (Delta/mu')(L^2 s_t^2 +
(C_beta e_h + C' h)^2)`. The first term on the right is `<= gamma_1 s_t /
4`; the rest, `C_sigma e_h + O(h)`, is `<= gamma_1 s_1(h) / 2` for small `h`
if also `c_* <= gamma_1 sqrt(mu' kappa_tau / 8) / (4 L C_sigma)`.

(iii) *Far zone* `s_t >= delta_2`: the margin (W5) and compactness give
`|sigma(t)| - Delta |beta(t)|^2 / (2 mu') >= m_0 > 0`, which absorbs the
`O(e_h + h)` perturbations and the `O(h)` term `(h Delta / 2)
max(0, -kappa_t^-)`, as in [R, Theorem 2.3(1)]. □

*Remarks.* The window of [R, Theorem 4.1] is empty here. The proof of the
stage conclusion uses (P1)–(P6), which come from [R, Theorem 4.1]
((H1)–(H5)); it does not use the terminal condition (T). (T) enters only in
the last sentence, `B(S^h) = J(zbar)`. (Added in the second revision.) The rate
`e_h <= c_* sqrt(h)` needs the specific small constant `c_*` of steps
(i)–(ii) (it depends on `mu'`, `kappa_tau`, `L`, `C_beta`, `C_sigma` and
`gamma_1`), not any constant; in particular `e_h = o(sqrt(h))` suffices. It
is weaker than the `O(h)` rate that [R, Theorem 2.3(1)] uses to get `O(1)`
failing stages; [R, Remark 2.5] found `O(h)` sufficient for that and noted
that a Hölder rate `h^{1/2}` gives only `O(h^{-1/2})` failing stages there.
Necessity of either rate is not shown. (Corrected after review: the first
version said "any `c`" in the Summary and called `O(h)` "necessary".) The
interior stage is handled by the positive `u`-curvature
`h^2 kappa_tau / 2`, which beats the `O(h^3)` cross-term penalty
`h^2 |beta_t|^2 / (h mu')`.

## 4. `kappa_tau = 0`: window exactness holds

**Theorem B.** Assume (SH), `kappa_tau = 0` and `e_h <= C_e h`. For small
`h`:

(a) at most one stage `n = n_h` has `|sigma_t| < gamma h / 3`, and
`s_n <= C_1 h`;

(b) every stage `t != n` is exact over `D_t x U`;

(c) there is `K_0`, independent of `h`, such that for every fixed
`K >= K_0` the window `W = {n - K, …, n + K}` is exact:
`beta_W(D_a) = J_W(zbar)`.

With (T), `B = J(zbar) = f*`, using one window of `2 K_0 + 1` stages. One
can take `K_0 = ceil(128 C_4 / (mu' |b(x*(tau))|^2))`, where `C_4` is the
constant in `rho_n(z) - rho_n(zbar_n) >= -C_4 h^3 omega^2 + (h mu'/4)|d|^2`
(step 2 below). The constant is crude, and since `C_4` contains
`C_3^2 / mu'`, `K_0` can grow like `1/mu'^2`. Section 7 shows `K = 1`
suffices on the scalar toy, and `K` of 4–32 on the two-state example (which
is outside (SH), Section 7.5), growing there roughly like `1/eps`.

*Proof.* (a) By (P5), `|sigma_t| >= gamma_1 s_t - C_sigma C_e h`, so stages
with `|sigma_t| < gamma h/3` have `s_t < C_1 h`, `C_1 := (gamma/3 +
C_sigma C_e)/gamma_1`. On that zone, Lemma 1.3 with `kappa_tau = 0` gives
`sigma_{t+1} - sigma_t = h sigma_dot(tau) + O(h^2)`: consecutive values
move monotonically by `gamma h (1 + O(h))`, so at most one of them lies in
`(-gamma h/3, gamma h/3)`.

(b) For `t != n`, `|sigma_t| >= max(gamma h/3, gamma_1 s_t - C_sigma C_e
h)`, and the bracket in (*) of Theorem A is `>= -h [C_kappa (s_t/h + C_e +
1) + 2(L^2 s_t^2/h^2 + C^2)/mu']`, because `kappa_tau = 0`. Hence (*) holds
for `s_t <= c` small and `h` small (the linear first-order term dominates
the quadratic ones), and the far zone is as in Theorem A(iii).

(c) Step 1 (reduction). By Lemma 0.1(3) (the window has `2K + 1` stages
and `s_t <= (C_1 + K + 1) h`) it suffices to take `x_a in B_{r/2}(xbar_a)`;
then all window states lie in the balls `B_t` for small `h`. (Revised after
review: the first version cited Lemma 0.1(2), which is stated at radius
`r`.) Step 2 (stage bounds). Lemma 0.2 at `t in W`, with `kappa_t^- >=
-C_2(K) h`, `|beta_t| <= C_3(K) h`, and the cross terms absorbed by half of
the strict convexity (`C_3 h^2 |omega||d| <= (h mu'/4)|d|^2 + C_3^2 h^3
omega^2 / mu'`), gives

```
rho_t(z_t) - rho_t(zbar_t) >= h |sigma_t||omega_t| - C_4(K) h^3 omega_t^2 + (h mu'/4) |d_t|^2 .
```

For `t != n` the first-order term `>= (gamma h^2 / 3)|omega_t|` dominates
`C_4(K) h^3 omega_t^2` for small `h` (with `K` fixed), leaving
`>= (h/2)|sigma_t||omega_t| + (h mu'/4)|d_t|^2`. For `t = n`, the constants
do not depend on `K` (`s_n <= C_1 h`): `>= -C_4 h^3 omega_n^2 + (h mu'/4)
|d_n|^2`. Summing,

```
J_W(z) - J_W(zbar) >= (1/2) sum_{t != n} h |sigma_t||omega_t| - C_4 h^3 omega_n^2 + (h mu'/4) sum_{t in W} |d_t|^2 .
```

Step 3 (the state carries the deviation). By (P7),
`d_{t+1} = d_t + h b(xbar_t) omega_t + e_t` with `|e_t| <= C_g h |d_t|`. For
`j = 1, …, K`,
`d_{n+j} - d_{n+1-j} = h b_n omega_n + sum_{t != n} h b_t omega_t + sum e_t`
(sums over `n+1-j <= t <= n+j-1`). Put `delta = h |b_n||omega_n|`,
`V = h Bbar sum_{t != n} |omega_t|`, `Z = C_g h sum_{t in W} |d_t|`.

- If `V >= delta/4`: the first-order sum is `>= (gamma h / (6 Bbar)) V >=
  (gamma |b_n| / (24 Bbar)) h^2 |omega_n| >= C_4 h^3 omega_n^2` for small
  `h`.
- If `Z >= delta/4`: `sum |d_t|^2 >= (sum |d_t|)^2 / (2K+1) >= |b_n|^2
  omega_n^2 / (16 C_g^2 (2K+1))`, and `(h mu'/4)` times this dominates
  `C_4 h^3 omega_n^2` for small `h`.
- Otherwise `|d_{n+j} - d_{n+1-j}| >= delta/2` for all `j`, the `K` pairs
  are disjoint, and `sum_{t in W} |d_t|^2 >= K delta^2 / 8`, so
  `(h mu'/4) sum |d_t|^2 >= (K mu' |b_n|^2 / 32) h^3 omega_n^2 >=
  C_4 h^3 omega_n^2` once `K >= 32 C_4 / (mu' |b_n|^2)`; for small `h`,
  `|b_n| >= |b(x*(tau))|/2`.

In all cases `J_W(z) >= J_W(zbar)`. □

*Remarks.*

- The window must extend on **both** sides of `n`: with a free entry state,
  the stages before `n` pin the state and the stages after `n` see the
  shifted state; the pairing in step 3 uses both.
- Stage `n` may or may not fail: its `O(h^3)` sign depends on the family
  (for example on the sign of `b^T S_xx(t_{n+1}, .) b = O(h)`). A discrete
  family with exact discrete tangency `P_{n+1} b = w` makes it exact without
  a window; this is what the optcdeg2 certificate did (`q = 0` at both
  switching stages, [R, Section 5.3]; there `w = 0`, so `kappa_tau = 0`).
  optcdeg2 is outside (SH) (two switches, terminal row `v_N = 0`), so this
  is an analogy, not an application of Theorem B.

## 5. `kappa_tau < 0`: window exactness fails

**Theorem C.** Assume (SH) and `kappa_tau < 0`. Let `W_h` be windows with
`|W_h| h -> 0`, and entry sets containing `xbar_a`.

(i) If `W_h` contains a stage `n` with `ubar_n in (u_-, u_+)`, then

```
beta_W - J_W(zbar) <= -(h^2/2) |kappa_tau| omega_hat_n^2 (1 - o(1)),   omega_hat_n >= Delta/2 .
```

(ii) If `W_h` contains a vertex stage `n` with `|sigma_n| <= (1 - delta)
h Delta |kappa_tau| / 2` for a fixed `delta > 0`, then
`beta_W - J_W(zbar) <= -(delta/2) h^2 Delta^2 |kappa_tau| (1 - o(1))`.

(iii) For windows `[a, b)` of any length, with `x_a = xbar_a` fixed, the
same move changes `J_W` by at most `(h^2/2) omega^2 [kappa_tau + o(1) + C_M
|b|^2 l e^{2 C_g l}]`, `l = (b - n - 1) h`, where `|b|` bounds `|b(x)|` near
the trajectory and `C_g` is the state Lipschitz constant of `g = a + b u`
(P7). So a window can be exact only if it lasts at least `l_0 - o(1)` after
`n`, where `C_M |b|^2 l_0 e^{2 C_g l_0} = |kappa_tau|`: at least
`(l_0 - o(1))/h` stages, i.e. `Omega(1/h)`. If `a` and `b` do not depend on
the state, `C_g = 0` and `l_0 = |kappa_tau| / (C_M |b|^2)`. This is a
necessary condition only. Whether any window that stops before `T` is then
exact is not shown. The window `[0, N)` (the whole problem, entry `x_0`,
`Phi` at the exit) is exact exactly when `f* = J(zbar)`, but it is no
decomposition. (Corrected after review: the first version wrote
`Theta(1/h)` and, in the Summary, gave the closed form for `l_0` whenever
`b` is constant.)

In cases (i)–(ii), if `f* = J(zbar)`, the certificate of [R, Theorem 4.1]
with such windows gives `B <= f* - c h^2` with `c > 0`: window exactness
fails.

*Proof.* Take `x_a = xbar_a`, keep all controls except `u_n`, and move
`u_n` to its farther bound (`omega = +-omega_hat_n`) in (i), or to the other
vertex in (ii). Stages before `n` do not change. Stage `n` changes by
`h sigma_n omega + (h^2/2) omega^2 kappa_n(xbar_n, xi)`, with `sigma_n = 0`
in (i), and `kappa_n -> kappa_tau` by (P3), because `|sigma_n| = O(h)`
forces `s_n = O(h + e_h) -> 0` by (P5). For `t > n` in `W`, `omega_t = 0`
and `|d_t| <= h |b||omega| e^{C_g (t-n) h}`, so by (P1) and (P4)
`rho_t(xbar_t + d_t, ubar_t) - rho_t(zbar_t) <= C_M h |d_t|^2 / 2 =
O(h^3)`. Their sum is `O(|W| h^3) = o(h^2)`, which gives (i) and (ii); (iii)
is the same sum without `|W| h -> 0`. The window trajectory stays within
`O(h)` of `zbar`, hence in `D_t` (interior states, (W1)). Finally
`B = S_0(x_0) + sum_{t notin W} inf rho_t + beta_W + inf(Phi - S_N) <=
J(zbar) + (beta_W - J_W(zbar))`. □

By the phase model (Remark 1.4, heuristic), case (i) or (ii) occurs on a
fraction of about `1 - D/F''(tau)` of the grids: 73% predicted and 71%
observed for the toy of Section 7.3.

**Proposition D (quadratic families exact over `R^n x U` fail; LQ data).**
Assume (SH) with LQ-structured data (`a` affine, `b` constant, `l_0`, `Phi`
quadratic, `l_1` affine), `e_h <= C_e h`, and `kappa_tau < 0`. Let
`S_t = p_t^T x + (x - xbar_t)^T P_t (x - xbar_t) / 2` be any quadratic family
with the discrete costate slopes that is exact **over `R^n x U`** at every
stage `t >= b` and at the terminal (`P_N <= Phi_xx`), where `b - s <= K` for
a fixed `K` (`s` the switching stage). Then `limsup_{h -> 0} (b^T P_b b -
b^T w) <= 0`; quantitatively, `b^T P_b b - b^T w <= C (log(1/h))^{-1/2}`.
Every window `[a, b)` with `(b - a) h -> 0` that contains an interior stage
`n` has `beta_W - J_W(zbar) <= -(h^2/2) |kappa_tau| omega_hat_n^2 (1 - o(1))`.
The same holds, with `limsup <= 0` but without the explicit rate, if
`b - s <= K` is replaced by `(b - s) h -> 0`.

*Scope.* The comparison [E, Lemma 10(5)] used below covers only families
that are exact over `R^n x U`. A certificate needs exactness only over the
state boxes `D_t`; such families are not covered (as [E, Corollary 11]
already notes). (Hypotheses stated precisely after review; the first
Summary said "every quadratic family that is exact after the window".)

*Proof.* Let `Phat` be the discrete maximal recursion of [E, Lemma 10] with
`eps = 0`: `Phat_t = h H + F^T Phat_{t+1} F - beta_t beta_t^T / m_t`,
`beta_t = F^T Phat_{t+1} b - w`, `m_t = 2|sigma_t|/(h Delta) + b^T
Phat_{t+1} b`, `F = I + h A`. By [E, Lemma 10(5)], `P_t <= Phat_t` for
`t >= b`.
`Phat_t <=` the discrete Lyapunov solution, and `Phat_t >= P^tr_t`, the
transferred family, which is exact over `R^n x U` on stages `t >= s + C`
for LQ data (Lemma 0.2 is then global in `d`); so `||Phat_t|| <= C_P` on
`[s + K', N]`, `K' := max(b - s, C)`. Put `eta_t := b^T beta_t`. Expanding `F = I + O(h)`,

```
eta_{t-1} = eta_t - (eta_t + O(h))^2 / m_t + O(h),      m_t <= C_3 (t - s)   (t > s),
```

using `|sigma_t| <= gamma_2 (t - s) h + C h`. So `eta_{t-1} <= eta_t + C_1
h` always, and `eta_{t-1} <= eta_t + C_1 h - theta^2 / (4 C_3 (t - s))` when
`eta_t >= theta` (small `h`). Fix `theta, delta > 0` and `J = floor(delta /
h)`. If `eta_t >= theta` on all of `[s + K', s + J]`, summing gives
`eta_{s+K'} <= C + C_1 delta - (theta^2 / (4 C_3)) log(J / (K' + 1)) ->
-infinity` (because `K' h -> 0`), a contradiction for small `h`. So some
`t* <= s + J` has `eta_{t*} < theta`, and then `eta_{s+K'} <= theta + C_1
delta`. As `theta, delta` are arbitrary, `limsup eta_{s+K'} <= 0`.
*Rate* (added after review). For `K'` bounded take
`delta = (log(1/h))^{-1/2}` and `theta^2 = 8 C_3 (C + C_1 + 1) / log(1/h)`.
Then `J/(K' + 1) >= h^{-1/2}` for small `h`, so
`(theta^2/(4 C_3)) log(J/(K'+1)) >= C + C_1 + 1`, the contradiction above
applies, and `eta_{s+K'} <= theta + C_1 delta = O((log(1/h))^{-1/2})`. A
sharper comparison with the continuous law below would presumably give
`O(1/log(1/h))`; that is not proved here. From `s + K'` down to `b`
(at most `K'` stages) drop the pushes: `Phat_t <= h H + F^T Phat_{t+1} F`,
so `b^T Phat_b b <= b^T Phat_{s+K'+1} b + O(h)` (if `b >= s + C`, then
`K' = b - s` and only the step from `b + 1` to `b` is used). Hence
`b^T P_b b - b^T w <= b^T Phat_b b - b^T w <= eta_{s+K'} + O(h)`. (`m_t > 0`
on `[b, N]` holds for `Phat` because it holds for the exact family `P` and
`m_t` increases with `P_{t+1}`.) For the window, with `x_a = xbar_a` and only `u_n` moved,
`J_W` changes by exactly `h sigma_n omega + (h^2/2) omega^2 b^T V_{n+1} b`,
where `V` is the window's Lyapunov recursion from `P_b` (LQ data; the exit
slope is `p_b`). Since `P_b <= Phat_b` and `Phat` is bounded above by its
Lyapunov transport from `s + K' + 1`,
`b^T V_{n+1} b <= b^T Phat_{s+K'+1} b + C (s + K' + 1 - n) h <=
kappa_tau + o(1)`, by `eta_{s+K'} <= o(1)` and `(s + K' + 1 - n) h -> 0`. □

For a bounded exit offset `b - s <= K` the proof bounds the excess by
`O((log(1/h))^{-1/2})`; for `(b - s) h -> 0` it gives only `limsup <= 0`.
That the decay is logarithmic and no faster is a heuristic: the leading-order law of
[E, Section 2.5] gives `eta_hat(s) ~ [1/eta_1 + (Delta/(2 gamma))
log(s_1/s)]^{-1}` at time `s` after the switch, and Section 7.6 is
consistent with it. By that law an interior stage is exact for the maximal
family only while `eta_hat(h) > |kappa_tau|`, i.e. roughly for
`h > s_1 exp(-(2 gamma/Delta)(1/|kappa_tau| - 1/eta_1))` (heuristic).

**Proposition E (branching on the window controls with a fixed family).**
Under the hypotheses of Theorem C(i), partition `U` for the interior
control `u_n` into finitely many intervals, fixed as `h -> 0`, and bound
each node `{u_n in I}` by the same family and window. Then for small `h`
every node with `|I| > 0` has bound `< J(zbar)`; no node is pruned.

*Proof.* The node contains `zbar` with `u_n` replaced by some `u in I`
with `|u - ubar_n| >= |I|/2`. As in Theorem C, this window trajectory has
`J_W - J_W(zbar) <= (h^2/2) (u - ubar_n)^2 (kappa_tau + o(1)) < 0`, and the
node bound is at most `J(zbar)` plus this. □

Node-specific families face the same obstruction at their own interior
stages (Theorem C applies to every KKT point), so branching yields only
`epsilon`-certificates: the node containing `ubar_n` with width `delta`
keeps a deficit of order `h^2 |kappa_tau| delta^2`. This is the "cluster
problem" of branch and bound (Du–Kearfott 1994; Wechsung–Schaber–Barton
2014), here with a relaxation that is second order in the node width but
with the wrong sign of curvature in `u_n` (sketch; not written out).

## 6. What still works when `kappa_tau < 0`

- **Near-exact certificates.** The certificate with the transferred family
  is valid and its gap is `-sum_{t in W} m_t + O(h^3)` by Proposition 2.1,
  with `|m_t| <= h^2 |kappa_tau| Delta^2 / 2` on at most
  `Delta |kappa_tau| / gamma + 2` stages (Lemma 1.3). So the gap is `O(h^2)`
  in general. It is `Theta(h^2)` along grid sequences with an interior
  stage or a vertex stage of small margin (Theorem C(i)–(ii)), and `O(h^3)`
  (0 for small `h`, next bullet) on grids where every stage has enough
  vertex margin. On the toy of Section 7.3 the gap is 0.35–0.53 `h^2` on the
  grids with an interior stage (`3.3e-8` at `N = 8000`) and 0 or
  `0.018 h^2` on the others.
- **Grids with enough vertex margin.** Assume in addition
  `e_h = o(sqrt(h))` (for example `e_h = O(h)`). If the KKT point has no
  interior stage and every vertex stage satisfies `|sigma_t| > h Delta
  |kappa_tau| / 2 (1 + delta)`, every stage is exact for small `h` (the proof
  of Theorem A(ii)–(iii), with the `u`-concavity term absorbed by the
  first-order margin). The rate matters: with `e_h ~ c sqrt(h)` the cross
  term `Delta (|beta_t| + C h Delta)^2 / (2 mu')` near the switch is of order
  `h`, the same order as the margin `h Delta |kappa_tau| / 2`. (Rate added
  after review.) Predicted fraction of grids: `D / F''(tau)` (Remark 1.4).
- **The discrete maximal recursion** at practical `h` (Proposition D and the
  heuristic threshold after it). It is not a transferred continuous family:
  its pushes `beta_t beta_t^T / m_t` keep the excess `b^T P b - b^T w`
  positive in all runs, and the excess at the first stage after the switch
  decays (Proposition D with a bounded exit offset: at most
  `O((log(1/h))^{-1/2})`; heuristically like `1/log(1/h)`). It gives an
  exact certificate whenever it does not break ([E, Lemma 10]); at an
  interior stage, not breaking requires `|kappa_tau| < eta_hat_1` (a
  necessary condition only). On the toys it does not break at any tested
  `N <= 32000` for `kappa_tau = -0.1, -0.05`, and it breaks at the interior
  stage of every tested grid that has one for `kappa_tau = -0.5`
  (Section 7.6).
- **Long windows** (Theorem C(iii)). A window must last at least
  `l_0 - o(1)` time units after the interior stage, i.e. `Omega(1/h)`
  stages. This is necessary only. Whether any window that stops before `T`
  is then exact is open; only the whole problem (window `[0, N)`) is known
  to be exact, exactly when `f* = J(zbar)`. Windows this long are
  `Omega(1/h)`-stage nonconvex problems. (Corrected after review: the first
  version said "exact in principle".)
- **A convexification bound beats the window certificates on the toy**
  (added after review; the observation is the reviewer's). In toy plus,
  `x_{t+1} = x_t + h u_t` gives exactly
  `sum_t h k x_t u_t = (k/2)(x_N^2 - x_0^2) - (k/2) h^2 sum_t u_t^2`, so
  `J_plus(u) = J_zero(u) - (k/2) h^2 sum_t u_t^2` with `J_zero` the convex
  transcription of toy zero. Since `u_t^2 <= 1`,
  `f*_plus >= min J_zero - (k/2) h^2 N`. The relaxation `u_t^2 <= 1` is
  tight at every vertex stage, so the gap to `J(zbar)` is
  `J_zero(ubar) - min J_zero + (k/2) h^2 (1 - ubar_n^2)`. Float check (`revision_checks.py lb`, identity residual
  `<= 2.3e-14`): its gap to `J(zbar)` is 0.18–0.25 `h^2` at
  `N = 50, 100, 150, 200, 1000, 4000, 8000`, against K = 2 window deficits
  of 0.30–0.57 `h^2`. The reviewer confirmed this in exact arithmetic and
  closed the gap to `1e-11` by a small exact branch and bound (15–19 nodes,
  `N <= 200`). This is specific to the toy's separable concavity; it does
  not contradict Theorem C, which concerns calibration (window)
  certificates, and branch and bound still gives only
  `epsilon`-certificates.
- **Reformulation** (Proposition 1.2 remark): if the modeller can choose the
  transcription, writing `l_1 u` as an exact discrete differential (when
  `b` is constant and `l_1 = grad G^T b`) gives `kappa_tau = 0`. This
  changes the MINLP instance, so it is not a certificate for a given
  instance.
- **Branching** gives `epsilon`-certificates only (Proposition E).

## 7. Numerical checks

All runs: `OMP_NUM_THREADS=1`, single thread, from `theory-bangbang/window/`.

### 7.1 Toys and continuous data

Scalar toy (`toy.py`): `min int_0^2 (x - a(t))^2/2 + k x u dt + Phi(x(2))`,
`x' = u`, `|u| <= 1`, `x(0) = 0`, `a = 2` on `[0,1)`; state box `|x| <= 2`
(contains every feasible state). `w = -k`, `b = 1`, `kappa_tau = -k`.

| toy | `k` | `a` on `[1,2]` | `Phi` | `tau` | `gamma` | `kappa_tau` | `eta_L` | `D` | `F''` | `b^T Q b` |
|---|---|---|---|---|---|---|---|---|---|---|
| verifier ([V]) | -0.5 | -2 | 0 | 0.21370 | 1.7863 | +0.5 | 1.2863 | 3.5726 | 8.7178 | 1.7863 |
| plus | +0.5 | -1 | `x` | 0.47741 | 1.5226 | -0.5 | 2.0226 | 3.0452 | 11.1355 | 1.5226 |
| zero | 0 | -1 | `x + x^2/4` | 0.47741 | 1.5226 | 0 | 2.0226 | 3.0452 | 11.1355 | 2.0226 |

(`toy_runs.py cont` → `logs/toy_cont.json`; minimum-principle sign
violation 0 for all three; `|sigma(t)| >= 0.44, 0.31, 0.31 |t - tau|`.)
Toys plus and zero are the same continuous problem (`int k x u = k x(T)^2/2`),
with Euler transcriptions that differ by `(k/2) h^2 sum u_t^2`.

Families (all quadratic, `S_t = p_t x + P_t (x - xbar_t)^2/2`, `P_t =
P(t h)`), with the global-form conditions of [E, Lemma 1.1] checked on a
grid of 8000 times (`min_G = min [P' + 1 - 2 eps - beta^2/|sigma|]`,
`beta = P + k`):

| toy, family | `P(t)` | `eps` | `min_G` | `min_A` | terminal margin `phi_2 - 2 eps - P(T)` |
|---|---|---|---|---|---|
| verifier, linear rate | `1/2` (`t <= tau`), `1/2 - 0.3 (t - tau)` | 0.01 | 0.315 | 0.68 | 0.0159 |
| verifier, [V] family B | `1/2` | 0 | 1 | 1 | **-0.5** |
| plus | `-1/2` | 0.1 | 0.8 | 0.8 | 0.3 |
| zero, "kink" | `0` (`t <= tau`), `-0.3 (t - tau)` | 0.01 | 0.243 | 0.68 | 0.937 |
| zero, affine | `0` | 0.1 | 0.8 | 0.8 | 0.3 |

All are strict tangential global-form calibrations (`P(tau) b = w`), except
that [V]'s family B violates the terminal condition `P(T) <= Phi_xx`.
In this scalar case the isotropic margin of (SH) ((H3)/(W5): one `mu` with
`M(t) >= mu` and `|sigma(t)| > Delta beta(t)^2 / (2 mu)` for `t != tau`) also
holds (checked after review, `revision_checks.py sh` →
`logs/revision_sh.json`): `sup_t beta^2/|sigma| = 0.365` (verifier, linear
rate) and `0.437` (zero, kink) against `inf_t M = 0.7`, and `beta = 0` for
the constant families. So the scalar families meet the margin
hypotheses of (SH); the rate hypothesis on `e_h` is not verified for them.

### 7.2 [V]'s toy (`kappa_tau = +0.5`): Theorem A

`toy_runs.py verifier` → `logs/toy_verifier.json`. Exact checks use the
float controls as rationals, with the single interior control corrected by
one exact Newton step so that `sigma_n = 0` exactly (`toy.exact_kkt_traj`,
which also asserts the exact KKT signs); every stage minimum over
`D_t x U` and the terminal minimum are computed exactly by face enumeration.

| `N` | interior stage | failing stages (float) | **exact** gap `J - B` | [V] family B: terminal loss |
|---|---|---|---|---|
| 500 | none | 0 | 0 | 3.19694 |
| 1000 | 106 (`u = -0.146`) | 0 | 0 | 3.19389 (exact 3.1938893…) |
| 2000 | 213 | 0 | 0 | 3.19250 |
| 4000 | none | 0 | 0 | 3.19158 |
| 8000 | 854 | 0 | 0 | 3.19125 |

The linear-rate family certifies the discrete optimum exactly, with no
window, at every `N`. Family B has no failing stage `1 … N-1` (as [V]
found). This is immediate at every `N` (added in the second revision): with
`P_t = 1/2` and `k = -1/2`, the stage-residual formula of `toy.py` has
`K_t = h`, `beta_t = P_{t+1} + k = 0` and `kap_t = 1/2`, so
`rho_t - rho_t(zbar_t) = h d^2/2 + h sigma_t omega + h^2 omega^2/4 >= 0` by
the KKT sign `sigma_t omega >= 0` (`revision2_checks.py famB` checks the
Hessian in rational arithmetic; the logged float stage losses are
`<= 3.3e-31`). This uses neither (T) nor a rate on `e_h`. But
`Phi - S_N = -(1/4)(x - xbar_N)^2` is concave (`P_N = 1/2 > Phi_xx = 0`),
so its terminal term is inexact: the bound is valid but 3.19 below `f*`.
Over the box `|x| <= 2` the terminal loss is exactly `(2 + |xbar_N|)^2/4`
(added in the third revision; this matches the logged losses at all five
`N`, and in rational arithmetic at `N = 1000`; `revision3_checks.py
famBterm`). Neither this term nor the stage Hessian above involves the
target `a(t)`; the target enters only through `xbar`. Neither [R] nor [V]
used family B as a certificate; [R]'s "the tangential family fails on none"
refers to stages in the window-law test. So, for that sentence of [R], this
is a clarification, not a correction. It does show that the conclusion
`B = f*` of [R, Theorem 4.1] needs a terminal condition such as (T)
(Section 8, first bullet).

### 7.3 Toy plus (`kappa_tau = -0.5`): Theorem C

`toy_runs.py plus` → `logs/toy_plus.json`; family `P = -1/2`, for which the
stage residual minus its value at `zbar_t` is exactly
`h d^2/2 + h sigma_t omega - (k/2) h^2 omega^2`.
Windows `{s - K, …, s + K}`, entry `[-2, 2]`. Values are deficits
`(J_W(zbar) - beta_W) / h^2`.

| `N` | interior (`ubar`) | `sigma/h` at `s-1, s, s+1` | stage loss (pred.) | `K = 0` | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|---|---|
| 500 | none | -1.704, 0.820, 2.348 | 0 (0) | 0 | 0 | 0 | 0 | 0 |
| 1000 | 238 (-0.247) | -2.148, 0, 1.901 | 0.38878 (0.38878) | 0.38878 | 0.38774 | 0.38691 | 0.38611 | 0.38532 |
| 2000 | none | -2.032, 0.491, 2.015 | 0.01800 (0.01800) | 0.01800 | 0.01667 | 0.01560 | 0.01457 | 0.01356 |
| 4000 | 954 (0.184) | -1.931, 0, 2.115 | 0.35041 (0.35041) | 0.35041 | 0.35018 | 0.34999 | 0.34981 | 0.34963 |
| 8000 | 1909 (-0.461) | -2.253, 0, 1.793 | 0.53333 (0.53333) | 0.53333 | 0.53315 | 0.53301 | 0.53287 | 0.53274 |

- **Exact** (rational, at the exact KKT point): at `N = 1000` and 4000 the
  window minima for `K = 0, 1, 2` equal the float values to the digits
  shown, and the single-flip trajectory lowers `J_W` for every `K <= 4`
  (by 0.38878 … 0.38256 `h^2` at `N = 1000`).
- The windows gain only `O(K h^3)`, as Proposition 2.1 predicts; the
  minimizer is always the single flip of the interior (or weakest vertex)
  control, with the entry state shifted by 0.4–0.9 `h`.
- *Fixed duration.* With the entry fixed at `x_0` (window `[0, b)`), the
  flip changes `J_W` by exactly `(h^2 omega^2 / 2) [h (b - 1 - n) - k]`
  (stage residual above, `d_t = h omega` after `n`). So it lowers `J_W`
  exactly when `b - 1 - n < k/h` = 250, 1000, 2000 post-switch stages at
  `N = 1000, 4000, 8000`, i.e. 0.5 time units, as Theorem C(iii) predicts
  (here the drift is `a = 0`, not to be confused with the target `a(t)` of
  the cost, and `b = 1`, `C_M = 1`, `C_g = 0`, so
  `l_0 = |kappa_tau| / (C_M |b|^2) = 0.5`). At `b - 1 - n = k/h` the change
  is 0; the float scan resolves this tie by rounding (it reports 251,
  1000, 2000; the reviewer's code 251, 1001, 2000). This concerns the single
  flip only and does not show that longer windows are exact. (Tie and
  scope stated after review.)
- **SCIP** (`toy_runs.py scip` → `logs/toy_scip.json`; spatial branch and
  bound on the transcription with states as variables; `feastol 1e-9`,
  absolute gap `1e-12`): status optimal at `N = 50, 100, 150, 200` (all
  with an interior stage), dual bound below `J(zbar)` by `1.7e-10 …
  7.9e-10`; SCIP's controls, re-simulated, cost `J(zbar) + 1.5e-11 …
  3.0e-10`. So `f* = J(zbar)` to about `1e-9`, while the `K = 2` window bound
  is below by `9.2e-4, 1.7e-4, 5.4e-5, 3.1e-5`: the certificate is strictly
  below `f*`.

### 7.4 Toy zero (`kappa_tau = 0`): Theorem B

`toy_runs.py zero` → `logs/toy_zero.json`; family "kink" (`c = 0.3`). Float entries such as
`< 1e-21` are rounding (in units of `h^3`).
Stage `n` loss is predicted as `(h^3/2) omega_hat^2 c theta / (1 - c
theta)` with `c theta = -P_{n+1}/h`.

| `N` | interior (`ubar`) | `-P_{n+1}/h` | stage-`n` loss `/h^3` | window deficit `/h^3`, `K = 0` | `K = 1` | `K = 2` | `K = 3` |
|---|---|---|---|---|---|---|---|
| 1000 | 238 (-0.186) | 0.088 | 0.0680 | 0.0680 (exact) | **0 (exact)** | **0 (exact)** | `< 1e-21` |
| 2000 | 477 (-0.996) | 0.176 | 0.4266 | 0.4266 | `< 4e-21` | `< 1e-21` | `< 2e-21` |
| 4000 | 954 (0.138) | 0.053 | 0.0362 | 0.0362 (exact) | **0 (exact)** | **0 (exact)** | `< 2e-20` |
| 8000 | 1909 (-0.347) | 0.106 | 0.1072 | 0.1072 (exact) | **0 (exact)** | **0 (exact)** | `< 2e-18` |
| 16000 | none | 0.211 | 0 | 0 | 0 | 0 | 0 |

"Exact" entries are rational window minima at the exact KKT point (0 means
exactly 0). The affine family `P = 0` has no failing stage at any `N` (max
loss `3.7e-20`): the window is needed only because the "kink" family has
`b^T P_{n+1} b < 0`, as the remark after Theorem B says. Only stage `n`
fails, as Theorem B(b) says.

### 7.5 Two-state examples of [E] (`n2win.py`, `n2_runs.py`)

Data of [E, example A] (`rho = 2, q = 0.3, c = 1, x_20 = 0.5`, `k_1 =
-0.3`), with `k_2 = -0.3` (A, `kappa_tau = +0.3`), `+0.3` (A−, `-0.3`) and
`0` (A0', `0`). Family: [E]'s continuous linear-rate tangential
construction (`eps = 0.02`, `delta_1 = 0.1`), transferred; it exists for all
three (no pre-switch blow-up). Stage losses over the exact reachable box;
windows `{s-K, …, s+K}` with the reachable box as entry, minimized by
enumerating all faces (float).

*Hypotheses* (added after review). This family (`continuous_family` of
`n2/model.py`) satisfies [E]'s anisotropic global-form condition (G) with
**equality** outside the layer `(tau, tau + delta_1]`, by construction:
`M - 2 eps I = (Delta / (2|sigma|)) beta beta^T`. On the last arc after the
layer the smallest eigenvalue of the difference is `<= 3e-8` in absolute
value (float, central differences for `P'`). Both eigenvalues are this
small: on the last arc the norm of the difference is `<= 2.6e-8`, and
outside the layer it is `<= 4.9e-8` (the maximum occurs before the switch),
or `<= 2.6e-8` relative to `|M|` (third revision, `revision3_checks.py aniso`
with three stencils on 3000 points per segment, and `anisogrid` with the
central stencil on 20000 points). It does
**not** satisfy the isotropic (H3)/(W5) margin in (SH), which needs
`sup_t Delta |beta|^2 / (2|sigma|) < inf_t lambda_min(M) = 2 eps`: the
supremum is 2.45 (A), 4.17 (A−), 3.23 (A0') at `eps = 0.02` and 17.4 (A0')
at `eps = 0.1`, against 0.04 and 0.2 (`revision_checks.py sh` →
`logs/revision_sh.json`). So the rows below are consistent with
Theorems A–C but are not instances of them. The proofs would plausibly
carry over to the anisotropic form (Lemma 0.2 with `beta^T K_t^{-1} beta`
in place of `|beta|^2 / (h mu')`), but this is not written out.

*[E]'s own families on its examples A and A0* (added in the second
revision; `revision2_checks.py shE` → `logs/revision2_shE.json`). [E]
screened three continuous tangential families ([E, Section 6.2]), all with
`eps = 0.02`: *cmax* (no layer; logarithmic tangency), *clin*
(`delta_1 = 0.1`, the family above) and *clin.02* (`delta_1 = 0.02`), on its
example A and on its example A0 (`rho = 1`, `c = 0.2`, otherwise as A; not
the A0' above). None of the six family–example pairs meets the isotropic
margin. In all six, `inf_t lambda_min(M) = 2 eps = 0.04`: where (G) holds
with equality, `M - 2 eps I` is rank one and positive semidefinite, so
`lambda_min(M) = 2 eps` there, exactly by construction (the computed
deviation is scheme dependent: up to about `1e-5` for cmax near
`t - tau = 1e-8`, float noise of about `2e-11` relative to `|M|`, and
`<= 1e-9` for clin and clin.02; root edit after the round-3 confirmation). Meanwhile `Delta |beta|^2 / (2|sigma|)` is
2.45 (A) and 1.98 (A0) near `t = T`, and its supremum over
`t <= tau - 0.1` is already 0.140 (A) and 0.336 (A0). For cmax
the ratio also grows without bound as `t -> tau+`, because `|beta|` decays
only logarithmically (A: 3.1, 117, 6.3e3, 3.9e5 at `t - tau = 1e-2, 1e-4,
1e-6, 1e-8`). The anisotropic residual
`R = M - 2 eps I - (Delta/(2|sigma|)) beta beta^T` is zero outside the
linear-rate layer by construction (`continuous_family` integrates `P' = G`
with equality there), so its computed value measures only numerical error
(differencing `P`, and evaluating `sigma` near `tau`). For clin and
clin.02 the norm of `R` (both eigenvalues) is at most `1.04e-7`, or
`5.2e-8` relative to `|M|` (same stencils and grids as in *Hypotheses*). For
cmax, `|M|` grows roughly like `1/(t - tau)`, more precisely like
`1/((t - tau) log^2(1/(t - tau)))` (117, 6.27e3, 4.87e4 and 3.9e5 at
`t - tau = 1e-4, 1e-6, 1e-7, 1e-8` on A), and
the absolute residual there depends on the stencil: at `t - tau = 1e-8`,
`lambda_min(R)` is `+2.8e-6` with the central difference of step
`0.1 (t - tau)` used in the second revision and about `-1.6` with a
five-point stencil of step `0.05 (t - tau)`. Relative to `|M|`, the norm of
`R` is at most `4.5e-6` with five-point stencils (steps `0.05 (t - tau)` and
`0.005 (t - tau)`). With the central difference it is `2.9e-3`: a
truncation error along `beta` that is positive on these data, so
`lambda_min(R)` does not detect it. So an absolute residual for cmax is not
meaningful; the equality itself holds by construction. (Corrected in the
third revision, `revision3_checks.py aniso`, `anisogrid`. The second
revision stated `|lambda_min(R)| <= 1e-7` for clin and clin.02,
`<= 4e-6` for cmax, and `inf_t lambda_min(M)` within `4e-6` of 0.04; these
figures depend on the stencil and the grid, and the reviewer's code gives
`1.04e-7` for clin.02 on A.) [E]'s fourth family without failing
stages, rmax, is the discrete maximal recursion and not a transferred
continuous family, so (SH) does not apply to it. Hence [E]'s observation
that no tangential family fails on A and A0 is consistent with Theorem A
but is not an instance of it.

| example | `tau` | `gamma` | `eta_L` | `D` | `F''` |
|---|---|---|---|---|---|
| A (`kappa_tau = +0.3`) | 1.31545 | 1.6411 | 1.0475 | 3.2823 | 7.4724 |
| A− (`-0.3`) | 1.17183 | 1.4621 | 1.5286 | 2.9242 | 9.0387 |
| A0' (`0`) | 1.23498 | 1.5383 | 1.2798 | 3.0766 | 8.1957 |

`n2_runs.py windows` → `logs/n2_windows.json` (deficits `/h^2`):

| example, `N` | interior | failing stage: loss (pred.) | `K = 0` | 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| A, 500 … 8000 | yes, all `N` | none (max loss `2.6e-21 h^3`) | 0 | 0 | 0 | 0 |
| A−, 500 | none | `s-1`: 0.0139 (0.0150) | 0 | 0 | 0 | 0 |
| A−, 1000 | none | `s-1`: 0.3921 (0.3931) | 0 | 0.3827 | 0.3765 | 0.3703 |
| A−, 2000 | 1171 (0.777) | `s`: 0.4731 (0.4737) | 0.4731 | 0.4706 | 0.4682 | 0.4657 |
| A−, 4000 | 2343 (0.163) | `s`: 0.2028 (0.2029) | 0.2028 | 0.2022 | 0.2017 | 0.2012 |
| A−, 8000 | none | `s+1`: 0.4417 (0.4412) | 0 | 0.4416 | 0.4416 | 0.4416 |
| A0', 500 | 308 | `s`: `0.248 h^3` | `0.248 h^3` | `0.184 h^3` | `0.166 h^3` | `0.151 h^3` |
| A0', 1000 | 617 | `s`: `1.215 h^3` | `1.215 h^3` | `0.967 h^3` | `0.880 h^3` | `0.815 h^3` |
| A0', 2000 | none | none | 0 | 0 | 0 | 0 |
| A0', 4000 | 2469 | `s`: `0.0006 h^3` | `0.0006 h^3` | `0.0003 h^3` | `0.0003 h^3` | `0.0002 h^3` |
| A0', 8000 | 4939 | `s`: `0.010 h^3` | `0.010 h^3` | `0.006 h^3` | `0.005 h^3` | `0.005 h^3` |

- A: consistent with Theorem A; also [E, Sections 6.2–6.3] found no
  failing stage for all tangential families on A and A0 (`kappa_tau = 0.3`
  in both). Those families lie outside (SH) (paragraph *[E]'s own
  families* above), so this too is consistency, not an instance.
- A−: consistent with Theorem C. The measured losses match `m_t` of Section 2 (vertex
  stages with `|sigma|/h = 0.293, 0.103, 0.079 < 0.3` fail). Windows reduce
  the deficit by at most 6% for `K <= 3`. Exception at `N = 500`: the
  leading-order deficit (`0.0139 h^2`) is small enough that the `O(h^3)`
  window terms cover it and the `K = 1` window is exact. This is a finite-`h`
  effect, allowed by Proposition 2.1.
- A0': consistent with Theorem B. Only one stage fails, at order `h^3`; windows with
  `K <= 3` reduce its deficit by at most a third (next paragraph for larger
  `K`).

*Window size in the degenerate two-state case* (`n2_runs.py azero` →
`logs/n2_azero.json`). Two checks per window `{n-K, …, n+K}`:

- the *single-direction bound*: the minimum over the entry state and the
  failing control only (the other controls at `ubar`), an upper bound on the
  window value; a positive deficit proves the window inexact;
- a *Schur certificate* (`certify_window`, float, a sufficient condition for
  exactness written in matrix form after the proof of Theorem B): with `F` =
  (entry state, failing control) and `L` the other controls, require
  `H_FF > 0` and `|g_t| >= lambda_- w_t / 2` for `t in L`, where `lambda_-`
  is the negative part of the smallest eigenvalue of the Schur complement
  `H_LL - H_LF H_FF^{-1} H_FL` and `w_t` the width of the control range.
  Then `J_W >= J_W(zbar)` on the box (the entry constraint is relaxed).

| `eps`, `N` | stage-`n` loss `/h^3` | single-direction deficit `/h^3` for `K = 1, 2, 4, 8, 16, 32` | Schur certificate holds for `K =` |
|---|---|---|---|
| 0.1, 1000 | 2.287 | 0.826, 0.404, 0, 0, 0, 0 | 4, 8, 16 (fails at 32, 64) |
| 0.1, 4000 | 0.0003 | 0.0001, 2e-5, 0, 0, 0, 0 | 4, 8, 16, 32 (fails at 64) |
| 0.02, 1000 | 1.215 | 0.967, 0.880, 0.758, 0.547, 0.124, 0 | none up to 64 |
| 0.02, 4000 | 0.0006 | 0.0003, 0.0003, 0.0002, 0.0001, 0, 0 | 32 |

With `eps = 0.1` the window with 4 stages per side is exact (certified at
both `N`); with `eps = 0.02` about 16–32 stages per side are needed, so the
window size grows roughly like `1/eps` (the family's smallest strictness on
the last arc is `lambda_min(M) = 2 eps`). The bound `K_0` of Theorem B,
which does not apply here as stated (see *Hypotheses*), may grow like
`1/mu'^2`. The certificate is only sufficient: it fails for large `K`
(where far vertex stages enter with larger curvature terms and `K h` is no
longer small) and at `eps = 0.02`, `N = 1000`, where the single-direction
bound already vanishes at `K = 32`. For `K <= 2` (`eps = 0.1`, both `N`),
`K <= 16` (`eps = 0.02`, `N = 1000`) and `K <= 8` (`eps = 0.02`, `N = 4000`)
the block `H_FF` is indefinite and the single-direction deficit proves the
window inexact; for example `K = 2` at `eps = 0.1`, `N = 4000` has deficit
`1.84e-5 h^3 > 0` (printed as 0 before the revision). The reviewer's full
minimum over the box by face enumeration gives, at `eps = 0.1`, 0.826,
0.404, 0.130, `6e-19` `h^3` for `K = 1 … 4` at `N = 1000`, and `1.2e-4`,
`1.8e-5`, `2e-15`, `2e-15` at `N = 4000`.

### 7.6 Discrete maximal recursion and the log layer

`toy_runs.py rmax` → `logs/toy_rmax.json` (toy plus with `k in {0.5, 0.2,
0.1, 0.05}`, all one-switch extremals with the minimum-principle signs
checked) and `n2_runs.py rmax` → `logs/n2_rmax.json` (A−).
`eta_hat_1 := b^T Phat_{s+1} b - b^T w`, the excess curvature of the
maximal family at the first stage after the switch (`s` the switching
stage). For LQ data `b^T w = kappa_tau`, so at an interior stage
`m_s = b^T Phat_{s+1} b = kappa_tau + eta_hat_1`, and the recursion
continues past `s` (a necessary condition for exactness there,
[E, Lemma 10(2)]) iff `kappa_tau + eta_hat_1 > 0`. (Corrected after review:
the first version printed `b^T (F^T Phat_{s+2} b - w)`, one stage later.
The toy rows were computed with `Phat_{s+1}` and are unchanged; the A− row
had used `Phat_{s+2}` and was recomputed, `n2_runs.py rmax`.)

| `N` | 500 | 1000 | 2000 | 4000 | 8000 | 16000 | 32000 |
|---|---|---|---|---|---|---|---|
| toy `k = 0.5`: `eta_hat_1` | 0.294 | 0.242 | 0.222 | 0.205 | 0.179 | 0.182 | 0.152 |
| toy `k = 0.5`: break | none (bang-bang) | interior stage | none (bang-bang) | interior | interior | none (bang-bang) | interior |
| toy `k = 0.1`: `eta_hat_1` | 0.293 | 0.261 | 0.235 | 0.213 | 0.196 | 0.202 | 0.178 |
| toy `k = 0.1`: break | none | none | none | none | none | none | none |
| A− (`kappa_tau = -0.3`): `eta_hat_1` | 0.202 | 0.185 | 0.154 | 0.141 | — (`m_{s+1} <= 0`) | 0.125 | 0.115 |
| A−: break | none | `s-1` | interior | interior | `s+1` | interior | `s` |

- With `k = 0.05` the recursion never breaks either (7 grids, `N = 500 …
  32000`); with `k = 0.2` it breaks at 5 of the 7 grids (stage `s-6 … s`).
- Where it does not break, every stage and the terminal are exact (float
  stage losses `<= 3.2e-16`): an exact certificate with no window at
  `kappa_tau = -0.1` and `-0.05`, at grids with an interior stage.
- `eta_hat_1` decays, as Proposition D requires, and slowly. The
  leading-order law `[1/eta_L + (1/gamma) log(1/h)]^{-1}` (heuristic) is
  within 21% in either direction: it is 4–17% below the toy values
  (`k = 0.5`: law 0.243 … 0.146 against 0.294 … 0.152) and 10–21% above the
  A− values (law 0.226 … 0.137 against 0.202 … 0.115; before the index
  correction the A− values were 0.220 … 0.126). By that law the
  `k = 0.1` recursion would break only below `h ~ 3e-7` (`N ~ 7e6`;
  extrapolation, not tested).

### 7.7 Phase model (Remark 1.4)

`phase_check.py` → `logs/phase_check.json`: 250 grids `N = 101, 105, …,
1097`.

| toy | predicted interior fraction `4 b^T Q b / F''` | observed | two interior stages |
|---|---|---|---|
| verifier | 0.820 | 0.816 | 0 |
| plus | 0.547 | 0.528 | 0 |
| zero | 0.727 | 0.708 | 0 |

For toy plus, the transferred family is stage-wise exact near the switch on
29.2% of the grids; predicted `D/F'' = 27.3%`.

## 8. What this changes in [R] and [S]

- [R, Theorem 4.1], last sentence: under (SH), "window exactness" is
  automatic and the window is empty if `kappa_tau > 0` (Theorem A; rate
  `e_h <= c_* sqrt(h)` with a specific small `c_*` suffices); it is a
  theorem with a window of `2 K_0 + 1` stages if `kappa_tau = 0`
  (Theorem B; `e_h = O(h)`); and if `kappa_tau < 0` window exactness fails
  for all small `h` along any sequence of grids whose KKT points have an
  interior stage (Theorem C), which by the phase model is a positive
  fraction of grids. On such grids the certificate gives
  `B <= J(zbar) - c h^2` (`c > 0`) and cannot prove optimality of `zbar`;
  the conclusion `B = f*` then fails whenever `f* = J(zbar)` (as on the toy
  of Section 7.3, by SCIP at `N <= 200`). The open item "uniform conditioning of switch windows" is answered in
  this sense: bounded windows are uniformly well conditioned exactly when
  `kappa_tau >= 0`. Separately, [R, Theorem 4.1]'s conclusion `B = f*`
  also needs a terminal condition such as (T), which (H1)–(H5) do not
  contain: by [R, Proposition 1.2] the bound includes `inf(Phi - S_N)`,
  and the argument needs this infimum attained at `xbar_N` too. [V]'s
  family B shows the gap (Section 7.2): it meets the margin hypotheses
  checked in Section 7.1, every stage is exact (so every window is exact),
  yet `B = f* - 3.19` because `P_N = 1/2 > Phi_xx = 0`. [V]'s toy
  has a jump of the target `a(t)` at `t = 1`, so it is not a literal
  counterexample to the `C^3` data hypothesis (H1). The mechanism,
  `P(T) > Phi_xx`, does not depend on that jump: neither family B's stage
  Hessian nor its terminal loss `(2 + |xbar_N|)^2/4` involves `a(t)`.
  Whether a variant with a smooth target meets every hypothesis of
  [R, Theorem 4.1], including the rate `e_h = O(h)`, was not checked. This
  is a missing hypothesis in the statement of [R, Theorem 4.1]; its stage
  conclusions are unaffected. [R] is maintained by the root and was not
  changed here. (Added in the third revision; the observation is the
  round-3 reviewer's.)
- [R, Summary] / [V] (a clarification, not a correction): the tangential
  family of the `w = 0.5` toy ([V]'s family B) has no failing stage, as [R]
  says, but its terminal term is inexact (`P_N = 1/2 > Phi_xx = 0`), so its
  bound is valid but 3.19 below `f*`; neither [R] nor [V] claimed it as a
  certificate. A tangential family with an exact terminal term exists and
  certifies exactly (Section 7.2).
- [R, Remark 2.5]: for `kappa_tau > 0`, a rate `e_h <= c_* sqrt(h)` (in
  particular `e_h = o(sqrt(h))`) suffices; [R] used `O(h)`, which is
  sufficient there. Necessity of either rate is not shown. For the `O(h)`
  rate itself, Osmolovskii–Veliov (2020, Theorem 5.1) is a candidate source
  (Section 0.3; transfer to [R]'s setting not checked).
- [S], "Question (transfer at switches)": yes with `W = 0` for
  `kappa_tau > 0` and with `W = 2 K_0 + 1` for `kappa_tau = 0`; no for
  `kappa_tau < 0` within transferred `C^2` calibrations and, for LQ data,
  within all quadratic families with costate slopes that are exact over
  `R^n x U` after a window exit `o(1/h)` stages after the switch
  (Proposition D). Families exact only over the state boxes, and field
  calibrations with a Hessian jump across the switching surface, are not
  covered by these negative results.
- [S, Sketch 5.4] expected `O(1)` windows to be well conditioned. They are
  well conditioned only when `kappa_tau >= 0`; for `kappa_tau < 0` their
  controls decouple at order `h^2` (Proposition 2.1) and the window inherits
  the `u`-concavity of the stages.

## 9. Status

*Root, 2026-10-01:* the case `kappa_tau < 0` (which certificates do work)
and several switches are treated in [`kappa-negative.md`](kappa-negative.md).

| item | status |
|---|---|
| Lemma 0.1, Lemma 0.2 | proved (0.2 is [R, Lemma 2.1] before its last step; 0.1(3), the near-switch entry reduction at radius `r/2`, added after review) |
| `mu'` remark (factor 2 in the proof of [R, Theorem 4.1]) | proved; no conclusion of [R] changes |
| Proposition 1.2, Lemma 1.3 | proved (smooth data) |
| Remark 1.4 (phase model) | heuristic; checked on 250 grids per toy; its kink jump `D - Delta^2 kappa_tau` is the O–M switch term (derivation, checked against [E]'s formulas) |
| Remark 1.5 (Hessian `h^2[eta_L 1 1^T + kappa_tau I]`) | exact for the toy; heuristic in general |
| Proposition 2.1 (decoupling) | proved, windows of bounded size near the switch, `e_h = O(h)` |
| Theorem A (`kappa_tau > 0`, no window) | proved, `e_h <= c_* sqrt(h)` with a specific small `c_*`; the stage conclusion does not use (T) |
| Theorem B (`kappa_tau = 0`, window exactness) | proved, `e_h = O(h)`; constant `K_0` crude (may grow like `1/mu'^2`) |
| Theorem C (`kappa_tau < 0`, counterexample) | proved for transferred families; (iii) is a necessary duration only (`Omega(1/h)` stages) |
| Proposition D (quadratic families exact over `R^n x U`) | proved for LQ-structured data, `e_h = O(h)`, exit `o(1/h)` stages after the switch; excess `O((log(1/h))^{-1/2})` proved for a bounded exit offset; `1/log(1/h)` heuristic; families exact only over boxes not covered |
| Proposition E (branching, fixed family) | proved; node-specific families: sketch |
| threshold of the maximal recursion | heuristic (leading-order law of [E, Section 2.5]) |
| toy certificates (Sections 7.2, 7.4) | exact rational arithmetic |
| toy window deficits (7.3) | float, with exact rational checks at `N = 1000, 4000` |
| global optimum of toy plus | SCIP, float tolerances, `N <= 200` |
| two-state results (7.5), maximal recursion (7.6) | float screening; the two-state families (this report's and [E]'s cmax, clin, clin.02) are outside (SH) (anisotropic condition with equality), so 7.5 illustrates Theorems A–C |
| isotropic (SH) margin (7.1, 7.5), O–M split, convexification bound (Section 6) | float screening (`revision_checks.py`; [E]'s families cmax, clin, clin.02 on A and A0: `revision2_checks.py shE`) |
| anisotropic equality (G) for the two-state families (7.5) | holds by construction; the computed residual is numerical error (clin, clin.02 and this report's family: norm `<= 1.04e-7`; cmax: `<= 4.5e-6` relative to `\|M\|` with five-point stencils; `revision3_checks.py aniso`, `anisogrid`) |
| family B stage exactness (7.2) | exact algebra (stage Hessian checked in rational arithmetic, `revision2_checks.py famB`); needs neither (T) nor a rate on `e_h` |
| family B terminal loss `(2 + \|xbar_N\|)^2/4` (7.2) | exact algebra; matches the logs at five `N`, rational at `N = 1000` (`revision3_checks.py famBterm`) |
| [R, Theorem 4.1]'s `B = f*` needs a terminal condition such as (T) (Section 8) | shown by [V]'s family B, whose toy has a target jump (not a literal counterexample to (H1)); a smooth-target variant was not checked |

## 10. Literature and novelty

Examined for this report (bibliographic details from search results or
from [R], [E]; papers not read in full unless stated):

- W. Alt, R. Baier, M. Gerdts, F. Lempio, *Error bounds for Euler
  approximation of linear-quadratic control problems with bang-bang
  solutions*, Numer. Algebra Control Optim. 2(3) (2012) 547–570
  ([record](https://www.aimsciences.org/article/doi/10.3934/naco.2012.2.547)).
  Per the abstract: discrete and continuous controls coincide except on a
  set of measure `O(sqrt(h))`, and `O(h)` under stronger smoothness. This is
  the kind of estimate (H4) needs; not checked against our `e_h`, which
  also includes costates in `L^infinity`.
- W. Alt, R. Baier, F. Lempio, M. Gerdts, Optimization 62 (2013) 9–32, and
  W. Alt, U. Felgenhauer, M. Seydenschwanz, COAP 69 (2018) 825–856, as cited
  in [R, Remark 2.5].
- A. Wechsung, S. D. Schaber, P. I. Barton, *The cluster problem
  revisited*, J. Global Optim. 58(3) 429–438, DOI 10.1007/s10898-013-0059-9
  (online 2013; details from the
  [MIT record](https://dspace.mit.edu/handle/1721.1/103614)); R. Kannan,
  P. I. Barton, *The cluster problem in constrained global optimization*,
  J. Global Optim. 69(3) (2017) 629–676, DOI 10.1007/s10898-017-0531-z
  (details from the MIT record); K. Du, R. B. Kearfott (1994), the original
  cluster-problem paper (cited from these, not checked). From the
  abstracts: relaxations must converge at least to second order to avoid
  clustering near a minimizer. Used only for the analogy in
  Proposition E.
- H. Maurer, N. P. Osmolovskii (2003) and the second-order theory cited in
  [R], [E] (`D`, `eta_L`, `F''`). Added after review: in [E]'s notation the
  O–M switch cross term `2[H_x] xbar_av xi` equals `-Delta^2 kappa_tau xi^2`
  (Remark 1.4). So `kappa_tau` is, up to the factor `-Delta^2`, a classical
  quantity of the O–M quadratic form.
- N. P. Osmolovskii, V. M. Veliov, *Metric sub-regularity in optimal
  control of affine problems with free end state*, ESAIM:COCV 26 (2020) 47,
  DOI 10.1051/cocv/2019046
  ([Numdam record](https://www.numdam.org/item/COCV_2020__26_1_A47_0)).
  Added after review; for this revision the PDF was downloaded from Numdam
  and Sections 1–3 (hypotheses (A1), (A2'), Theorem 3.2), the statement of
  Corollary 4.2 and Section 5 (Theorem 5.1 and its proof) were read in
  text form. Theorem 5.1: under (C1)–(C3), solutions of the discrete Euler
  optimality system satisfy
  `||x^h - xhat||_{1,1} + ||u^h - uhat||_1 + ||p^h - phat||_{1,1} <= C h`,
  hence `e_h = O(h)` in `L^infinity`, the rate assumed by Proposition 2.1,
  Theorem B and Proposition D (details and differences of setting in
  Section 0.3). The paper's second-order sufficient conditions (Section 2,
  Corollary 2.4) are for the continuous problem; Section 5 contains no
  discrete second-order condition. (The review records that an automated
  page summary claimed a "discrete second-order sufficient condition"; the
  text does not contain one.)

Novelty (qualified): brief searches (three queries on Euler discretization
of bang-bang problems, discrete switching structure and discrete
second-order conditions, plus, after review, the reviewer's five searches
and one search for this revision) found no statement of the decoupling of
bounded windows or of the trichotomy for window certificates. The switch
self-curvature `kappa_tau` is **not** new as a quantity: `-Delta^2 kappa_tau`
is the O–M switch cross term. What appears new, within these searches, is
its role as the `u`-curvature of every tangential stage residual
(Proposition 1.2) and the resulting trichotomy. The works examined give
error estimates for discrete KKT points and second-order sufficiency for
the continuous problem; none of them treats exactness of calibration or
window certificates for the discrete problem. The ingredients are
elementary; the phase model is a heuristic in the spirit of the known
`O(h)`/`O(sqrt(h))` switching-set estimates. The observation that the Euler
transcription of `l_1(x) u` is not a discrete exact differential is
classical in substance.

## 11. Commands run and files

Scripts (all in `theory-bangbang/window/`):

- `toy.py` — scalar toy, KKT solver (one-switch search plus active-set
  refinement with the exact Hessian), families, exact face-enumeration box
  QP (float or `Fraction`), stage/terminal/window problems, exact rational
  KKT point;
- `toy_cont.py` — continuous switching function and switch data, family
  margin checks;
- `toy_runs.py` — parts `cont verifier plus zero rmax scip`;
- `n2win.py` — window problems for [E]'s two-state examples (imports
  `theory-bangbang/n2/model.py` and `discrete.py` read-only);
- `n2_runs.py` — parts `windows rmax azero` (`rmax` index corrected in
  the revision);
- `phase_check.py` — Remark 1.4;
- `revision_checks.py` — parts `rmaxidx sh om lb` (added in the revision;
  Section 12);
- `revision2_checks.py` — parts `shE famB rmaxrow` (added in the second
  revision; Section 12.2);
- `revision3_checks.py` — parts `famBterm aniso anisogrid` (added in the
  third revision; Section 12.3).

Commands (targeted runs only; no project-wide verification; CI not
inspected):

1. `python3 toy_runs.py cont` → `logs/toy_cont.json` (seconds).
2. `python3 toy_runs.py verifier`, `python3 toy_runs.py plus`,
   `python3 toy_runs.py zero` → `logs/toy_{verifier,plus,zero}.log` (the
   first `verifier` run stopped on an empty-list bug and was rerun). These
   logs predate the exact rational KKT correction: their exact checks used
   the float controls as they are, which left rounding-level residues
   (for example an exact window minimum of `-4.3e-24` instead of 0).
3. After adding `exact_kkt_traj`: `python3 toy_runs.py verifier plus zero`
   → `logs/toy_exactparts.log`, overwriting `logs/toy_{verifier,plus,zero}.json`
   (about 1 minute). The JSON files and this log are the results reported.
4. `python3 toy_runs.py rmax` → `logs/toy_rmax.{log,json}` (a few minutes).
5. `python3 toy_runs.py scip` → `logs/toy_scip.{log,json}` (about 11 s).
6. `python3 n2_runs.py windows`, `python3 n2_runs.py rmax`,
   `python3 n2_runs.py azero` → `logs/n2_*.{log,json}` (a few minutes
   each). A first version of `azero` solved the full window problems with
   SCIP; it was stopped after about 10 minutes on the first case and
   replaced by the Schur certificate of Section 7.5 (its log was
   overwritten).
7. `python3 phase_check.py` → `logs/phase_check.json` (twice: the second
   run added the stage-wise-exact fraction).
8. A one-off check of the Hessian formula of Remark 1.5 against exact
   differencing of `sigma` (relative difference `<= 4.1e-11`, all three
   toys, `N = 200`); not logged.
9. Exploratory one-off scripts in `/tmp` (parameter scans for the toy and
   the two-state variants, timing tests); their results are reproduced by
   the scripts above.
10. Three web searches and two page fetches (the MIT records of the
    cluster-problem papers; Section 10).

Revision after review (all with `OMP_NUM_THREADS=1`, from
`theory-bangbang/window/`; targeted checks only, no project-wide
verification, CI not inspected, nothing committed):

11. `python3 revision_checks.py rmaxidx om` →
    `logs/revision_rmaxidx_om.log`, `logs/revision_{rmaxidx,om}.json`
    (about 4 s).
12. `python3 revision_checks.py sh` → `logs/revision_sh.{log,json}` (about
    16 s).
13. `python3 revision_checks.py lb` → `logs/revision_lb.{log,json}` (about
    5 s).
14. After correcting the index in `n2_runs.py rmax`:
    `python3 n2_runs.py rmax > logs/n2_rmax.log` → `logs/n2_rmax.json`
    (about 15 s; overwrites the first version's log and JSON; the new JSON
    also keeps the old quantity under `b_beta`, which reproduces the old
    row 0.220 … 0.126).
15. One web search (Osmolovskii–Veliov record) and one download of the
    paper's PDF from Numdam into `/tmp`, converted with `pdftotext` and read
    (Sections 1–3, Corollary 4.2, Section 5).
16. The review's own re-runs (independent code in
    `reviews/window-exactness-review-checks/`) were not re-run; where the
    text cites them it says so.

Second revision (round-2 checking; same conditions: `OMP_NUM_THREADS=1`,
from `theory-bangbang/window/`, targeted checks only, no project-wide
verification, CI not inspected, nothing committed):

17. `python3 revision2_checks.py famB rmaxrow` →
    `logs/revision2_famB_rmaxrow.log`, `logs/revision2_{famB,rmaxrow}.json`
    (under 1 s; reads `logs/toy_verifier.json` and `logs/toy_rmax.json`, no
    new solves).
18. `python3 revision2_checks.py shE` → `logs/revision2_shE.{log,json}`
    (about 15 s; imports `n2/model.py` read-only).
19. Read-only inspection of `logs/toy_scip.json` (SCIP values quoted in the
    Consequence paragraph and Section 8), of [R, Theorem 4.1] ((H1)–(H5))
    and of [E, Lemma 10] and [E, Section 6.2] (families and examples). The
    round-2 reviewer's scripts (`reviews/window-exactness-confirm-r1-checks/`)
    were not re-run. No web searches.

Third revision (round-3 checking; same conditions: `OMP_NUM_THREADS=1`,
from `theory-bangbang/window/`, targeted checks only, no project-wide
verification, CI not inspected, nothing committed):

20. `python3 revision3_checks.py famBterm | tee logs/revision3_famBterm.log`
    → `logs/revision3_famBterm.json` (about 4 s; recomputes the verifier
    KKT points at `N = 500 … 8000`).
21. `python3 revision3_checks.py aniso > logs/revision3_aniso.log` →
    `logs/revision3_aniso.json` (about 47 s; imports `n2/model.py`
    read-only).
22. `python3 revision3_checks.py anisogrid > logs/revision3_anisogrid.log` →
    `logs/revision3_anisogrid.json` (about 54 s).
23. Two one-off scripts in `/tmp`, not logged: `r3_lminM_where.py` (where
    `lambda_min(M)` of cmax deviates from `2 eps`: sampled at
    `t - tau = 1e-8 … 1e-3`, deviations above `1e-6` occur only for
    `t - tau <= 1e-6`) and `r3_dense_grid.py` (the
    20000-point residual split into the pieces before the switch and on the
    last arc; on the last arc this report's family has norm `<= 2.6e-8`).
24. Read-only: the round-3 review and its logs
    (`reviews/window-exactness-confirm-r2-checks/logs/d1_shE.log`,
    `d3_cmax_aniso_probe.log`), and [R] Proposition 1.2, Theorem 2.3 and
    Theorem 4.1. The reviewer's scripts were not re-run. No web searches.

## 12. Revision after review

### 12.1 Round 1

Round 1 of independent checking (`reviews/window-exactness-review.md`)
raised ten points. Each was verified before changing the text. None changes
a theorem; items 1, 2 and 4 correct statements that were broader than their
proofs.

1. **`l_0` closed form (Summary item 4; Theorem C(iii)).** *Verified:*
   Theorem C(iii) gives `C_M |b|^2 l_0 e^{2 C_g l_0} = |kappa_tau|`, where
   `C_g` is the state Lipschitz constant of `g = a + b u` (P7); `C_g = 0`
   needs `a` and `b` both state independent. The two-state examples have
   `b` constant but `a = A x`, so the old wording ("when `b` does not depend
   on the state") was wrong for them. *Changed:* the Summary now says "when
   `a` and `b` do not depend on the state", and (iii) says "at least
   `l_0 - o(1)`". The toy check of Section 7.3 is unaffected (drift `a = 0`,
   `b = 1`, `C_M = 1`); it was restated with the exact change
   `(h^2 omega^2/2)[h(b - 1 - n) - k]`, which also explains the tie at
   `b - 1 - n = k/h` (the review's 1001 against 1000 at `N = 4000`).
2. **Proposition D stated too broadly.** *Verified:* the proof uses
   [E, Lemma 10(5)], which compares only families exact over `R^n x U`, and
   bounds the exit offset `b - s`. The harmonic-sum argument gives only
   `limsup <= 0`; we made it quantitative (`delta = (log 1/h)^{-1/2}`,
   `theta^2 ~ 1/log(1/h)`), which gives `O((log(1/h))^{-1/2})`, as the
   review said. We also checked that the proof carries over to exits with
   `(b - s) h -> 0` (take `K' = max(b - s, C)`; `log(J/(K'+1)) -> infinity`
   still holds). *Changed:* the Summary, Consequence paragraph, Section 6,
   Section 8 and the status table now state exactness over `R^n x U`, the
   exit condition and the proved rate. The `1/log(1/h)` rate and the word
   "only" are labelled heuristic. The proposition now includes the
   `(b - s) h -> 0` extension, the explicit rate, and a *Scope* note that
   families exact only over the state boxes are not covered.
3. **Section 7.6 index slip.** *Verified* (`revision_checks.py rmaxidx`):
   for toy plus, `Phat_{s+1} + k` = 0.2936, 0.2421, 0.2222, 0.2046, 0.1790
   (the tabulated values), while `b^T(F^T Phat_{s+2} b - w)` = 0.343, 0.290,
   0.259, 0.234, 0.207. `m_s = b^T Phat_{s+1} b` is the quantity whose
   sign decides the break at an interior stage. We also found that the A−
   row had been computed with the printed (`Phat_{s+2}`) formula
   (`n2_runs.py`), unlike the toy rows. *Changed:* the definition is now
   `eta_hat_1 = b^T Phat_{s+1} b - b^T w`; `n2_runs.py rmax` was corrected
   and rerun; the A− row is now 0.202, 0.185, 0.154, 0.141, — (the
   recursion breaks at `s+1` for `N = 8000`, so `Phat_{s+1}` does not
   exist), 0.125, 0.115. The break pattern is unchanged. The law comparison
   now reads "within 21%" (law 10–21% above the A− values, 4–17% below the
   toy values).
4. **"Exact in principle" / `Theta(1/h)` stages.** *Verified:*
   Theorem C(iii) bounds one particular move, so it gives a necessary
   duration only. We also checked the review's remark that "the whole
   remaining horizon with `Phi` at the exit" is trivially exact: that holds
   for the whole problem, window `[0, N)` with entry `x_0` (exact iff
   `f* = J(zbar)`). For `[a, N)` with `a > 0` and a free entry, exactness
   requires `V_a - S_a` to be minimized at `xbar_a` (`V_a` the tail value
   function), which is not automatic. So the text claims exactness only for
   `[0, N)`. *Changed:* Summary item 4, Theorem C(iii) and the Section 6
   bullet ("Long windows") now say `Omega(1/h)` stages, necessary only.
5. **Section 7.5 attributions.** *Verified* (`revision_checks.py sh`): the
   two-state family meets the anisotropic condition with equality
   (`|lambda_min(M - 2 eps I - (Delta/(2|sigma|)) beta beta^T)| <= 3e-8` on
   the last arc) but not the isotropic (SH) margin:
   `sup Delta|beta|^2/(2|sigma|)` = 2.45, 4.17, 3.23 (`eps = 0.02`) and 17.4
   (A0', `eps = 0.1`) against `inf lambda_min(M) = 2 eps` = 0.04, 0.2. The
   scalar families do meet it (0.365 and 0.437 against 0.7; `beta = 0` for
   the constant families). *Changed:* "A: Theorem A" etc. now read
   "consistent with Theorem …"; a *Hypotheses* paragraph in Section 7.5 and
   a sentence in Section 7.1 record the check; the Summary no longer says
   Theorem A "explains" [E]'s examples.
6. **Entry-reduction radius.** *Verified:* Lemma 0.1(2) needs
   `|x_a - xbar_a| >= r`, while Proposition 2.1 and Theorem B step 1 used it
   at `r/2`; entries between `r/2` and `r` could leave the balls `B_t`.
   *Changed:* new Lemma 0.1(3) proves the near-switch reduction at radius
   `r/2` (Lemma 0.2 gives `-O(h^2) + (h mu'/2)|d|^2 >= 0` for
   `|d| >= r/4` because `|beta_t| = O(h)` near the switch); Theorem B step 1
   cites it. Proposition 2.1's lower bound now uses per-stage bounds on all
   of `D_t x U` and needs no reduction.
7. **Section 7.5 table (`eps = 0.1`, `N = 4000`, `K = 2`).** *Verified* in
   `logs/n2_azero.json`: the single-direction deficit is `1.844e-5 h^3 > 0`
   (the review's full face enumeration gives the same). *Changed:* printed
   as `2e-5`; the text below the table names this case and lists all
   `(eps, N, K)` with indefinite `H_FF`.
8. **Rate wording.** *Verified* against [R, Remark 2.5] (which found `O(h)`
   sufficient for `O(1)` failing stages and noted that a Hölder rate gives
   `O(h^{-1/2})` failing stages) and against the constants of Theorem A,
   steps (i)–(ii). For the vertex-margin bullet we redid the estimate: with
   `e_h ~ c sqrt(h)` the cross term near the switch is of order `h`, the
   same order as the margin, while `e_h = o(sqrt(h))` makes it `o(h)`.
   *Changed:* `c_*` (specific, small) in the Summary, Theorem A remark,
   Section 8 and the status table; "needed" → "suffices"; "found
   necessary" → "found sufficient"; the vertex-margin bullet now assumes
   `e_h = o(sqrt(h))`.
9. **Minor wording.** *Verified* each point: [R]'s Summary sentence refers
   to stages; family B's bound is valid (`P_N = 1/2 > Phi_xx = 0`); the
   Theorem C statements are asymptotic in `h`; by Proposition 2.1 the gap
   is `-sum m_t + O(h^3)`, which is `Theta(h^2)` only with an interior or
   small-margin stage; optcdeg2 has three control arcs (two switches) and
   `v_N = 0` ([R, Section 5.1]), outside (H2) and the free-endpoint setting;
   Theorem A zone (ii) used the lower bound on `|sigma|` without
   restricting to `|t - tau| <= delta_sigma`. *Changed:* "invalid" →
   "inexact" (Summary, 7.2, Section 8, marked as a clarification of [R]);
   "on any grid" → "along any sequence of grids …, for all small `h`"
   (Consequence paragraph, Section 8); Section 6 gap stated as `O(h^2)` in
   general; optcdeg2 marked as outside (SH) (Summary item 3, remark after
   Theorem B); `delta_sigma` added to (P5) and to `delta_2`. While editing
   Theorem B, we also noted, as the review did, that `C_4` contains
   `C_3^2/mu'`, so `K_0` may grow like `1/mu'^2`, and replaced "scaling like
   `1/mu'`" accordingly.
10. **Literature.** *Verified* by reading the Osmolovskii–Veliov paper
    (Section 10): Theorem 5.1 gives the `O(h)` estimate in
    `W^{1,1} x L^1 x W^{1,1}` for solutions of the discrete optimality
    system, under SMsR (Corollary 4.2 for bang-bang controls with linearly
    growing switching functions and `2 Omega >= -mu_0 ||du||_1^2`), (C1)
    data Lipschitz in `t`, and (C3) a-priori closeness. One additional
    difference from our setting that the review did not mention: (C1)
    excludes the jump of `a(t)` at `t = 1` in the toys. We derived the O–M
    link by hand from [E, Section 3] (`[H_x] = -w^T Delta u`,
    `xbar_av = b Delta u xi/2`) and checked the total against
    finite-difference `F''` on A, A−, A0' (`revision_checks.py om`, within
    `5.3e-10`). *Changed:* a rate remark in Section 0.3, an O–M paragraph
    after Remark 1.4, two literature entries, and a revised novelty
    statement that `kappa_tau` is a known quantity and the novelty is its
    role in window exactness.

Not in the list above, but taken from the review's body: the
convexification lower bound for toy plus (new bullet in Section 6). We
re-checked it in float (`revision_checks.py lb`): gap 0.18–0.25 `h^2`
against K = 2 window deficits of 0.30–0.57 `h^2` at `N = 50 … 8000`; the
exact branch and bound is the reviewer's and was not re-run.

What was not re-checked: the review's own numerical reproductions (cited
where used), the `eps = 0.02` Schur certificates, and the numeric constants
of Theorem B (for example the factor 128 in `K_0`).

### 12.2 Round 2

Round 2 of independent checking (`reviews/window-exactness-confirm-r1.md`)
found all ten round-1 items resolved and raised three problems and three
optional points. Each was verified before changing the text. None changes a
theorem, a proof or a computed number other than the two rounding slips
in item 3.

1. **Summary item 4 attached the proved rate to the wrong case.**
   *Verified* by re-reading the proof of Proposition D. The rate step needs
   `J/(K'+1) >= h^{-1/2}` with `J = floor(delta/h)`, which holds for a
   bounded `K'`. If `K'` grows with `(K'+1) h -> 0`, `log(J/(K'+1))` still
   tends to infinity, so `limsup <= 0` holds, but it can grow arbitrarily
   slowly (for example like `log log(1/h)` when `K' h ~ 1/log(1/h)`), so no
   rate follows. The statement of Proposition D and the status table were
   already correct. *Changed:* Summary item 4 now says that for an exit
   `o(1/h)` stages after the switch the proof gives only `limsup <= 0`, and
   that the `O((log(1/h))^{-1/2})` bound holds for an exit a bounded number
   of stages after the switch. The sentence after Proposition D and the
   Section 6 bullet on the maximal recursion now name the bounded offset
   too (the latter concerns the first stage after the switch, a bounded
   offset, so its rate claim was already covered).
2. **Summary item 2 generalized an unchecked hypothesis claim.**
   *Verified:* round 1 had checked only the family `continuous_family`
   with `eps = 0.02`, `delta_1 = 0.1` ([E]'s clin) on [E]'s example A, and
   on this report's variants A− and A0'. [E]'s example A0 (`rho = 1`,
   `c = 0.2`) and [E]'s families cmax and clin.02 had not been checked.
   *Rerun:* `revision2_checks.py shE` checks all three continuous tangential
   families of [E, Section 6.2] (cmax, clin, clin.02; `eps = 0.02`) on [E]'s
   A and A0. The claim holds: none of the six pairs meets the isotropic
   margin (`inf_t lambda_min(M)` within `4e-6` of 0.04 (stencil
   dependent; see Section 12.3, item 3), against
   `Delta|beta|^2/(2|sigma|)` of 2.45 (A) and 1.98 (A0) near `t = T` and
   0.140, 0.336 before the switch; for cmax the ratio also grows without
   bound as `t -> tau+`, up to `3.9e5` at `t - tau = 1e-8` on A). The A,
   clin value 2.446 agrees with round 1 (2.45). [E]'s rmax family is
   discrete, so (SH) does not apply to it; clin+3h is clin sampled at
   `t + 3h` (an `O(h)` tangency defect) and is not among the families
   without failures ([E] reports failing stages at `N = 500, 1000` on A).
   *Changed:* Summary item 2 now names the three families and says why
   rmax is not covered; a new
   paragraph *[E]'s own families* in Section 7.5 gives the numbers; the
   Section 7.5 bullet for A and the status table say that [E]'s families
   are outside (SH) as well.
3. **Section 7.6 table, toy `k = 0.1`, `N = 4000`.** *Verified*
   (`revision2_checks.py rmaxrow`, reading `logs/toy_rmax.json`):
   `eta_hat_1 = 0.213455`, which rounds to 0.213, not 0.214. All other
   entries of the `k = 0.5` and `k = 0.1` rows match the log to three
   digits. *Changed:* 0.214 → 0.213. While reading the same log we also
   found that the largest float stage loss where the recursion does not
   break is `3.12e-16` (`k = 0.05`, `N = 4000`), slightly above the printed
   bound `3.1e-16`; the bound now reads `<= 3.2e-16`.
4. **(Optional) "exact when `|kappa_tau|` is small compared with …".**
   *Verified:* the text read as a proved sufficient condition. What is
   proved: the recursion gives an exact certificate whenever it does not
   break ([E, Lemma 10(1)–(3)]: with `m_t > 0` at every stage each stage is
   exact over `R^n x U`, hence over `D_t x U`, and `P_N = Phi_xx`), and at
   an interior stage `s` it continues only if
   `m_s = kappa_tau + eta_hat_1 > 0` ([E, Lemma 10(2)]). No condition on
   `kappa_tau` that prevents a break elsewhere is proved; for example, at
   `kappa_tau = -0.2` the recursion breaks at vertex stages up to 6 stages
   before the switch (Section 7.6). The float statements were rechecked in
   `logs/toy_rmax.json`: no break at any of the 7 grids for `k = 0.1` and
   `0.05`; for `k = 0.5` a break at stage `s` on each of the four grids with
   an interior stage (`N = 1000, 4000, 8000, 32000`) and none on the three
   others. *Changed:* the Summary paragraph "What still works" and the
   Section 6 bullet now state the sufficient condition (no break), the
   necessary condition at an interior stage, and the float results
   separately, and say that no sufficient condition on `kappa_tau` is
   proved. The Summary also states the consequence that the old wording
   ("proved: to 0") left implicit: under the hypotheses of Proposition D,
   `limsup eta_hat_1 <= 0 < |kappa_tau|`, so the recursion breaks for all
   small `h` on grids with an interior stage.
5. **(Optional) "`B = f*` fails".** *Verified:* Theorem C gives
   `beta_W - J_W(zbar) <= -c h^2`, hence `B <= J(zbar) - c h^2`. This
   contradicts `B = f*` only if `f* = J(zbar)`, as Theorem C itself says.
   (If `zbar` is not a global minimizer, `B = f*` is not excluded by
   Theorem C.) *Changed:* the Consequence paragraph now says that the
   certificate gives `B <= J(zbar) - c h^2` and cannot prove optimality of
   `zbar`, and that this contradicts `B = f*` when `f* = J(zbar)`, as on the
   toy (SCIP, `N <= 200`; values rechecked in `logs/toy_scip.json`). The
   first bullet of Section 8 now says "window exactness fails" and adds the
   same qualification for `B = f*`.
6. **(Optional) Drift `a = 0`; Theorem A and (T).** *Verified:* in the toy,
   `a(t)` is the target of the running cost (Section 7.1), while
   Theorem C(iii) uses `a` for the drift of `g = a + b u`; the toy's drift
   is 0. For (T): the proof of Theorem A's stage conclusion uses (P1)–(P6),
   which come from (H1)–(H5) of [R, Theorem 4.1]; none of these is a
   terminal condition (checked in [R]), so (T) enters only through
   `B(S^h) = J(zbar)`. For [V]'s family B (`P = 1/2`, `k = -1/2`) the
   stage-residual formula of `toy.py` gives `K_t = h`, `beta_t = 0`,
   `kap_t = 1/2` (`revision2_checks.py famB`, rational arithmetic), so each
   stage residual minus its value at `zbar_t` is
   `h d^2/2 + h sigma_t omega + h^2 omega^2/4 >= 0` (wording made exact in
   the third revision); the
   logged float stage losses are `<= 3.3e-31`. *Changed:* Section 7.3 and
   round-1 item 1 say "drift `a = 0`"; a sentence in the remarks after
   Theorem A and in Summary item 2 says the stage conclusion does not use
   (T); Summary item 2 and Section 7.2 record that family B's stage
   exactness is immediate at every `N` without a rate hypothesis; the
   status table notes both.

What was not re-checked in round 2: the round-2 reviewer's own scripts
(not re-run), and the numeric constants of Theorem B.

### 12.3 Round 3

Round 3 of independent checking (`reviews/window-exactness-confirm-r2.md`)
found all six round-2 items resolved and raised one minor problem and two
optional points. Each was verified before changing the text. None changes a
theorem or a proof. Item 1 adds a missing hypothesis to one sentence of the
Summary and records the same gap in the statement of [R, Theorem 4.1];
item 3 withdraws absolute residual figures that depended on the
differencing scheme.

1. **The Consequence paragraph omitted (T).** *Verified:* [R, Theorem 4.1]
   ((H1)–(H5) and the regularity list after it), [R, Theorem 2.3]
   ((W1)–(W5)) and [R, Proposition 1.2] were re-read. None contains a
   terminal condition, while the bound `B` contains `inf(Phi - S_N)` and
   Proposition 1.2(2) needs every infimum attained. Theorems A and B give
   `B = f*` only with (T). For [V]'s family B, the terminal term over
   `|x| <= 2` is `-(1/4)(x - xbar_N)^2` (because `p_N = Phi'(xbar_N) = 0`),
   so its loss is `(2 + |xbar_N|)^2/4`. `revision3_checks.py famBterm`
   recomputed the KKT points at `N = 500 … 8000`: the formula equals the
   logged terminal losses in float at all five `N` and in rational
   arithmetic at `N = 1000`, and the recomputed `J(zbar)` equals the logged
   value. Every stage is exact (Section 7.2) and the linear-rate family
   certifies `f* = J(zbar)` exactly, so `B = f* - 3.19`. The caveat was
   checked too: the toy's target `a(t)` jumps at `t = 1`, so (H1) fails.
   The target does not enter family B's stage Hessian (`[[h, 0], [0,
   h^2/2]]` in `(d, omega)`) or its terminal term; it enters only through
   `xbar`. *Changed:* the Consequence paragraph now begins "Under (SH), that
   is, its hypotheses plus the terminal condition (T) and
   `b(x*(tau)) != 0`" (the second condition is also part of (SH)). It then
   says that (T) matters, citing family B together with the caveat about
   the jump. The first bullet of Section 8 now records that
   [R, Theorem 4.1]'s `B = f*` also needs a terminal condition such as (T),
   with the same caveat, and says that a smooth-target variant was not
   checked. Section 7.2 gives the terminal-loss formula, and its last
   sentence now limits "a clarification, not a correction" to [R]'s
   sentence about failing stages. Summary item 2, which said that family B
   violates only (T) among the hypotheses checked, now also notes the jump,
   for consistency with the caveat. The status table has two new rows. [R]
   itself was not changed (the root maintains it).
2. **(Optional) "stage residual is exactly".** *Verified* from the
   stage-residual formula of `toy.py` (gradient `(0, h sigma_t)`, Hessian
   `[[K_t, h beta_t], [h beta_t, h^2 kap_t]]`). For family B, `K_t = h`,
   `beta_t = 0` and `kap_t = 1/2`. For toy plus with `P = -1/2`, `K_t = h`,
   `beta_t = 0` and `kap_t = -1/2 = -k`. The quoted expressions are
   `rho_t - rho_t(zbar_t)`, not `rho_t`. *Changed:* Summary item 2,
   Section 7.3 and round-2 item 6 now say "stage residual minus its value
   at `zbar_t`".
3. **(Optional) cmax residual figure.** *Verified*
   (`revision3_checks.py aniso`: three stencils on 3000 points per segment;
   `anisogrid`: central stencil on 20000 points). The residual
   `R = M - 2 eps I - (Delta/(2|sigma|)) beta beta^T` is zero by
   construction outside the linear-rate layer, so its computed value is
   numerical error. For cmax at `t - tau = 1e-8` on A (`|M| = 3.9e5`),
   `lambda_min(R)` is `+2.8e-6` with the central difference of step
   `0.1 (t - tau)` and about `-1.6` with the five-point stencil of step
   `0.05 (t - tau)`, as the reviewer found. The central difference has
   `lambda_max(R) = 1134`, a relative error of `2.9e-3` along `beta`, which
   `lambda_min(R)` does not see. Relative to `|M|`, the norm of `R` is at
   most `4.5e-6` (A: `4.48e-6`, `2.58e-6`; A0: `4.23e-6`, `2.59e-6`) with
   the two five-point stencils. For clin and clin.02 the residual hardly
   depends on the stencil (by about 1%), but the sampled maximum depends on
   the grid:
   clin.02 on A gives `9.7e-8` on 3000 points and `1.04e-7` on 20000
   points (the reviewer's figure), so "`<= 1e-7`" was slightly wrong. The
   same check showed that "`inf_t lambda_min(M)` within `4e-6` of 0.04" is
   also stencil dependent for cmax (up to `4.75e-6` below 0.04 on A with
   the five-point stencil of step `0.005 (t - tau)`). On the equality pieces
   `lambda_min(M) = 2 eps` exactly, since `M - 2 eps I` is rank one and
   positive semidefinite. *Changed:* the paragraph *[E]'s own families* in
   Section 7.5 now says that `R = 0` by construction, gives the residual
   norm relative to `|M|`, drops the absolute cmax figure, gives
   `inf_t lambda_min(M) = 2 eps` with numerical deviation `<= 5e-6`
   (superseded: scheme dependent, up to about `1e-5`; Section 12.4)
   (cmax) and `<= 1e-9` (clin, clin.02), and records the old figures. The
   round-1 figure for this report's family ("`<= 3e-8` on the last arc",
   *Hypotheses* paragraph) measured `lambda_min` only. It was rechecked for
   both eigenvalues: the norm is `<= 4.9e-8` outside the layer
   (`<= 2.6e-8` on the last arc, one-off check 23 of Section 11;
   `<= 2.6e-8` relative to `|M|`), so the
   figure stands, and a sentence now says so. Status table: new row. The
   conclusion is unchanged: the isotropic margin fails by a large factor
   (ratio 2.45 or 1.98 near `T` against `2 eps = 0.04`).

What was not re-checked in round 3: the round-3 reviewer's scripts (not
re-run; our own code reproduces the figures quoted from them); a variant of
[V]'s toy with a smooth target (not constructed); and the numeric constants
of Theorem B.

### 12.4 Root edits after the round-3 confirmation

The round-3 confirmation
([`../reviews/window-exactness-confirm-r3.md`](../reviews/window-exactness-confirm-r3.md))
returned "verified" with one minor and four optional wording items. The
root applied all five: Section 7.5 now says that `lambda_min(M) = 2 eps`
holds exactly by construction and that the computed deviation for cmax is
scheme dependent (up to about `1e-5`; the figure "`<= 5e-6`" in Section
12.3, item 3, is superseded); the *Hypotheses* paragraph gives the last-arc
norm `<= 2.6e-8` beside the maximum `<= 4.9e-8`, which occurs before the
switch; the growth of `|M|` for cmax is stated as roughly `1/(t - tau)`,
with the logarithmic correction; Summary item 2 says "calibration
hypotheses checked (margins and terminal condition)"; Section 12.2, item
2, points to Section 12.3, item 3. No result changes.
