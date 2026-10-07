# Certificates at a switch with `kappa_tau < 0`, and several switches

Date: 2026-09-30 (round-3 to round-5 revisions 2026-10-01). Status:
author's report, **revised after five independent reviews**:
`reviews/kappa-negative-review.md` (round 1, verdict "fixes needed"; changes
in Section 13), `reviews/kappa-negative-confirm-r1.md` (round 2, verdict
"minor fixes needed (text only)"; changes in Section 14),
`reviews/kappa-negative-confirm-r2.md` (round 3, verdict "minor fixes needed
(numbers only)"; changes in Section 15),
`reviews/kappa-negative-confirm-r3.md` (round 4, verdict "P1 is resolved.
Numbers verified; no fixes needed", with two optional nits; changes in
Section 16) and `reviews/kappa-negative-final-confirm-r1.md` (round 5,
verdict "Verified", with two optional nits; changes in Section 17). The
round-5 review re-reviewed the round-4 changes (review-status lines, one
heuristic range in Section 15 and an extension of a read-only check
script). The round-5 changes (the rounding in one worked example and
review-status lines) were confirmed by `reviews/round4-nits-confirm.md`
(verdict verified, optional nits only; root update 2026-10-01). Proofs are complete unless
labelled "sketch", "leading order" or "heuristic"; "leading order" means that `o(1)` factors in `h` are carried
along but not bounded explicitly. Numbers are **exact** (rational
arithmetic) unless marked **float** (floating-point screening). Scripts and
logs: `theory-bangbang/kneg/` and `theory-bangbang/kneg/logs/` (Section 12).

Cited notes:

- **[W]** `theory-bangbang/window-exactness.md` (switch self-curvature
  `kappa_tau`, (SH), Lemma 0.2, Proposition 1.2, Lemma 1.3, Remarks 1.4–1.5,
  Proposition 2.1, Theorems A–C, Propositions D–E, Section 6);
- **[R]** `theory-bangbang/report.md` (Definition 1.1, Proposition 1.2,
  Theorem 4.1 with its terminal condition);
- **[E]** `theory-bangbang/extension-n2.md` (`eta_L`, Theorem 1,
  Proposition 4, Theorem 9 (sketch), Lemma 10, Corollary 11, examples A,
  A0);
- **[SA]** `theory-bangbang/singular-arcs.md` (Kelley quantity,
  Proposition 1.3);
- reviews read for context: `reviews/window-exactness-review.md` (the
  convexification bound and its exact branch and bound),
  `reviews/window-exactness-confirm-r1.md` … `-r3.md`,
  `reviews/bangbang-n2-review.md`, `reviews/bangbang-root-fixes-confirm*.md`.

## Summary

[W] showed that at a regular switch with `kappa_tau < 0` every calibration
certificate whose windows have `o(1/h)` stages falls short of `J(zbar)` by
order `h^2` on grids whose discrete KKT point `zbar` has a fractional stage
(or a vertex stage with a small margin). This note asks which certificates
do work, at what size, whether `zbar` is in fact the discrete optimum, and
how Theorems A and B of [W] extend to several switches and to terminal rows.
Part 1 assumes LQ-structured data (affine drift, constant `b`, quadratic
`l_0` and `Phi`, `l_1` affine in `x`), for which the Euler cost `J(u)` is an
exact quadratic in the controls; this is the setting of [W, Proposition D]
and of all toys.

**Part 1: `kappa_tau < 0`, one regular switch.**

1. **Branch and bound with node-specific calibrations (Section 4).** For
   every node `{u_n in I}`, every point `z^A` of the node (the anchor) and
   every family that is quadratic at its window exit with the anchor's
   costate as slope there, the bound obeys
   `B <= J(z^A) + h sigma^A_n omega + (h^2/2) kappa_W omega^2` for every move
   `omega` of `u_n` inside `I` (Theorem 4.1, exact for LQ data). Here
   `kappa_W = b^T V_{n+1} b` is the `u`-curvature that the family's window
   sees. It is `kappa_tau + o(1)` for transferred `C^2` families
   ([W, Proposition 1.2]), and at most `kappa_tau + o(1)` (an upper bound,
   not an equality) for families exact over `R^n x U` after a window exit
   `o(1/h)` stages after the switch ([W, Proposition D]). We call bounds
   with `kappa_W <= kappa_tau + o(1)` *`kappa`-limited*. Consequences:
   - **No exact certificate with finitely many nodes** (Corollary 4.2): an
     exact certificate forces the family of the node that contains `ubar_n`
     (or has it as an end point) to be anchored at `zbar`, and that node then
     loses at least `(h^2/2)(|kappa_tau| - o(1)) w^2`, `w` the length of the
     node on one side of `ubar_n`.
   - **`epsilon`-certificates with `Theta(log(h^2/epsilon))` nodes**
     (Theorem 4.3, leading order). `O(log(h^2/epsilon))` nodes suffice. At
     least that many are needed for node families that are `kappa`-limited
     *and* have the costate of the node optimum as exit slope (for
     `epsilon > 0` nothing forces that slope; other families are not
     covered by the lower bound). The nodes grow geometrically away
     from `ubar_n`, with ratio at most `rho* = 1 + (q + sqrt(q^2 + q
     |kappa_tau|))/|kappa_tau|`, where `q = b^T Q(tau+) b = eta_L +
     kappa_tau` is the curvature of the true cost in `u_n`. A logarithmic
     count is the generic one-dimensional cost of covering a range with
     nodes that grow geometrically, for bounds whose error is second order
     in the node length (cf. Wechsung–Schaber–Barton 2014; Section 4). What
     is specific here is that `epsilon = 0` is impossible, and the explicit
     ratio `rho*`.
     The node counts
     of a greedy partition equal the predicted counts on 42 of the 44 tested
     `(N, epsilon)` pairs of the toys with `kappa_tau = -0.5` and `-1`, and
     differ by one on the other two (float; two partitions re-checked
     exactly).
2. **Lifted (parametric) calibrations give exact certificates (Section 5);
   their size is `O(N)` if a bounded number of outer nodes suffices
   (heuristic, Remark 5.5; true on every tested grid).** Treat `u_n` as a
   parameter `v` and use, for each
   `v`, the family anchored at `z(v)` = `zbar` with `u_n` replaced by `v`.
   For LQ data the anchor and its costates are affine in `v`, each stage's
   zero-loss set is an interval in `v` (Lemma 5.2), and on the interval `V`
   where all stages other than `n` are exact the bound is
   `min_{v in V} J(z(v)) = J(zbar)` (Theorem 5.3). Equivalently, it is an
   ordinary calibration of the problem with the extra constant state `v`;
   its `v`-dependence carries the curvature `q > 0` that every state-only
   calibration misses. Under a neighbour-margin condition (VM) and
   `e_h = o(sqrt h)`, `V` contains an `h`-independent neighbourhood of
   `ubar_n` for all small `h` (Theorem 5.4). Only this central node is
   proved; the rest of `U` was covered on every tested grid by a few nodes
   with ordinary node families. **Exact certificates of
   `f* = J(zbar)`** were obtained this way on every tested grid of the
   scalar toys: `kappa_tau = -0.5` at `N = 50 … 8000` and `kappa_tau = -1` at
   `N = 200 … 4000`, with 1–3 nodes; on a toy with `q < 0` with 2–6 nodes;
   and on the nonconvex two-switch toys (`kappa = -0.5`, Section 9.1) at
   all ten grids with a failing stage, `N = 500 … 4000`, with 3–9 nodes.
   On [E]'s two-state example A− (`kappa_tau = -0.3`) the same construction passes a float screening at
   the tested grids (Section 5.4); there the zero-loss set in `v` is not
   known to be an interval and was checked at finitely many points, so even
   in float this is not a certificate on all of `V`.
3. **Is `zbar` the discrete optimum? (Section 3).** At leading order the
   discrete optimum does not chatter near a regular switch: a local
   minimizer has no two fractional stages within time `c |kappa_tau|`
   (Lemma 3.1, exact for LQ data), and every bang-bang pair flip across the
   switch costs `h^2 D (j - i) + O(h^3 (j - i)^2)` (Proposition 3.2): the
   `kappa_tau` terms cancel. When `q > 0`, the fractional KKT point was the
   global optimum on every tested single-switch grid (exact, item 2). When
   `q < 0 < eta_L`, fractional KKT points near the switch are saddles
   (`H_nn < 0`), so minimizers near the reference trajectory are bang-bang
   (for the `q < 0` toy every `H_tt < 0`, so every minimizer is);
   `f* < J(zbar)` then holds for every such fractional KKT point `zbar`,
   but the optimum is still a monotone switch (exact certificates at
   `N = 200 … 2000`). On the documented two-switch instances, the KKT point
   returned by our search was the certified optimum on all 36 grids of
   Section 9.1 (for `kappa >= 0` the plain certificate is exact; the three
   `kappa = -0.5` grids at `N = 4000` were certified only in the round-2
   revision, Section 14). On an earlier instance, which differed by one
   stage of the target because the code read the decimal jump time 1.3 as
   its binary float, the search returned a non-optimal KKT point at `N = 2000`; the
   branch and bound found and certified the optimum, `0.31 h^2` lower and
   again a monotone switch structure. A local search can therefore return a
   non-optimal KKT point. We observed this on that one instance only.
4. **The convexification identity (Section 2).** For constant `b` and `l_1`
   affine in `x` (any drift, `l_0`, `Phi`), exactly
   `J(u) = Jt(u) + (h^2/2) sum_t kappa_t u_t^2`, `kappa_t = -grad l_1(t)^T b`,
   where `Jt` evaluates `l_1` at the half step `x_t + (h/2) b u_t`
   (Proposition 2.1; residual exactly 0 on the toy and on [E]'s A, A−, A0').
   `Jt` has no switch self-curvature, so on bang-bang control sequences `J`
   is a `kappa = 0` transcription plus a term linear in `u` (Corollary 2.2;
   a constant only when `u_- = -u_+`). The term `h^2 sum u_t^2`
   is the diagonal of the reduced Hessian that the left-point evaluation of
   `l_1(x) u` omits. It yields a convex relaxation only when `Jt` is convex:
   true for the scalar toy (smallest eigenvalue of `Jt`'s Hessian
   `≈ h^3/4`, relative excess 2.4% at `N = 10` and 0.025% at `N = 100`),
   false for [E]'s examples, whose `Jt` has `N - 1` or `N - 2`
   negative eigenvalues, the smallest about `-0.09 h` at `N = 800`, against
   `h^2 |kappa_tau| = 1.9e-6` (float). So the
   reviewer's convexification bound is special structure; branch and bound
   on it is again only an `epsilon`-certificate (Remark 2.3: a node with
   `ubar_n` at an end point has a strictly smaller bound).

**Part 2: several switches, close switches, terminal rows.**

5. **Theorems A and B with `k` switches (Section 6).** If every switch is
   regular with `kappa_j >= 0`, the stage-wise conclusions of [W] hold switch
   by switch: no window if all `kappa_j > 0`, one window of `O(1)` stages at
   each switch with `kappa_j = 0`, and `B = f*` with the terminal condition
   (Theorems A_k, B_k; proof by locality at the level of detail of [W],
   sketch level: (P1)–(P7) for several switches are taken from the
   hypotheses (SH_k), and the locality of each step of [R, Theorem 4.1] is
   asserted, not re-derived). A switch with `kappa_j < 0`
   behaves as in Theorem C, independently of the others. For LQ data
   `kappa_j = -grad l_1^T b` is the same at every switch; different signs
   need nonlinear `l_1`, state-dependent `b`, or time-dependent `l_1`.
6. **Close switches (Section 7).** The constants of Theorems A_k, B_k depend
   on the minimal separation `ell` of the switches and degrade as `ell -> 0`
   (with smooth data `|sigma_dot(tau_j)| <= ell sup|sigma_ddot|`, so
   `D_j = O(ell)`). A new necessary condition couples consecutive switches:
   a tangential calibration satisfying (A) with margin `eps` on the arc
   between `tau_1` and `tau_2 = tau_1 + ell` exists only if
   `eta^X_1 := kappa_2 - kappa_1 + ell (b^T H_xx b + 2 w_2^T A b - 2 eps |b|^2)
   + O(ell^2) >= 0` (Proposition 7.1, `b` constant). For data smooth in time
   this reads `ell (K - 2 eps |b|^2) + O(ell^2) >= 0` with `K` the
   Kelley-type quantity `-partial_u sigma_ddot` of [SA] evaluated at the
   merging point; then `kappa_2 - kappa_1 = O(ell)`. An `O(1)` drop of
   `kappa` across a short arc needs data that are not smooth in time (as in
   the toy, where `k` jumps) or an `ell` that is not small. When `A = 0` and
   `H_xx` is constant on the middle arc, the expansion is exact:
   `eta^X_1 = kappa_2 - kappa_1 + ell (b^T H_xx b - 2 eps |b|^2)`, so two
   switches with `kappa_1 > kappa_2 + ell b^T H_xx b` admit no tangential
   calibration even when both `kappa_j > 0`, and Theorems A_k, B_k do not
   apply. (Otherwise use (7.1) with its `2 w_2^T A b` term and `O(ell^2)`
   remainder.)
   Float checks of the discrete maximal recursion on a two-switch toy,
   `N = 1000 … 16000` (Section 9.3), show three regimes and support no
   asymptotic claim: for strongly negative `eta^X_1` (-0.49 to -0.69) it
   breaks on every grid, within 2 stages before to 5 stages after the
   first switching stage, and lifting the broken stage six times does not
   remove the break; for `eta^X_1 = -0.275` it breaks on 5 of 14 grids, not
   monotonically in `h`, and on these grids the breaks coincide with a
   small excess curvature passed from the second switch into the middle
   arc (an observation, not a tested criterion); for `eta^X_1` = -0.085,
   -0.040 and +0.160 it never breaks. So at these `h` the sign of `eta^X_1` does not
   predict the discrete behaviour. The first version's reading of the
   `-0.275` case as a thin layer is withdrawn. Most configurations with
   `eta^X_1 > 0` (9 of 10, all with rising `kappa`) are convex problems,
   for which no break is automatic, so they do not test the separation.
7. **Terminal rows (Section 8).** With affine terminal rows `C x_N = c` (as
   optcdeg2's `v_N = 0`), Theorems A_k and B_k hold with the terminal
   condition (T) replaced by its restriction to `ker C` (T_X); the rate
   `e_h` for fixed-endpoint problems is assumed, not proved. optcdeg2 has
   `kappa = 0` at both switches, so it is a `kappa = 0`, two-switch,
   terminal-row instance of Theorem B_k up to the unverified rate and (H3)
   hypotheses. For `kappa_tau < 0` the row does not help: Theorem C does not
   see it, and the excess curvature of the maximal recursion started from
   `P_N = +infinity` still decays (sketch; float Section 9.4).

Scope. Part 1 is proved for LQ-structured data; for nonlinear data the
leading-order statements carry over with `O(h^3)` errors but are not written
out. The toys are scalar (`n = 1`) except A−. Exactness of the lifted
certificates is proved on the central node (Theorem 5.4) and checked
exactly on the toys for the outer nodes; that a bounded number of outer
nodes suffices for all small `h` is a leading-order heuristic (Remark 5.5).

## 0. Setting and notation

As in [W, Section 0]: Euler transcription `x_{t+1} = x_t + h g(x_t, u_t)`,
`g = a + b u`, stage cost `L_t = h (l_0 + l_1 u)`, scalar control
`u in U = [u_-, u_+]`, `Delta = u_+ - u_-`, state boxes `D_t`, discrete KKT
point `zbar = (xbar, ubar)` with costates `p_t` and switching values
`sigma_t = l_1(xbar_t) + b^T p_{t+1}`; for the toys `dJ/du_t = h sigma_t`.
`kappa_tau = b^T w`, `w = -grad_x sigma_0(tau, x*(tau))` [W, Definition 1.1].
`Q` is the Lyapunov solution of the last arc with `Q(T) = Phi_xx`,
`eta_L = b^T Q(tau+) b - kappa_tau` [E], and

```
q := b^T Q(tau+) b = eta_L + kappa_tau,      D := |sigma_dot(tau)| Delta,      F''(tau) = D + Delta^2 eta_L .
```

`q` is the curvature of the discrete cost in the control of the switching
stage (`H_nn = h^2 q (1 + o(1))`), and `h^2 Delta^2 q` is the within-stage
curvature of the phase model [W, Remark 1.4].

**LQ-structured data** (as in [W, Proposition D]): `a` affine in `x`, `b`
constant, `l_0`, `Phi` quadratic, `l_1(t, x) = c(t)^T x + c_0(t)`. Then `J` is
an exact quadratic in `u`,

```
J(ubar + omega) = J(ubar) + h sigma^T omega + omega^T H omega / 2,
```

and `kappa_t := b^T w_t = -c(t)^T b` does not depend on the state; for
`c` constant it is the same number at every switch.

**Reduced Hessian near the switch** (LQ). With `m_t(s) = h F^{t-1-s} b`
(`s < t`, `F = I + h A`) the state sensitivities, the Hessian is the Gram
part of `l_0` and `Phi` plus the `l_1` part `h^2 c^T F^{|i-j|-1} b` off the
diagonal and `0` on it. Hence, for stages within `O(h)` of `tau`,

```
H_ij = h^2 (eta_L + O(h)) (i != j),   H_ii = h^2 (q + O(h)),
H_ii + H_jj - 2 H_ij = 2 h^2 kappa_tau + O(h^3 |i - j|)   (all i != j, |i - j| h <= 1).   (0.1)
```

(The first two are [W, Remark 1.5]; the third is computed in the proof of
Lemma 3.1.) Theorems and toys use the following families: for the scalar
toys, `S_t(x) = p_t x + P_t (x - xbar_t)^2 / 2` with the tangential choice
`P_t = -k_t = kappa_t` (then `beta_t = P_{t+1} + k_t = 0` and the stage
residual minus its value at `zbar_t` is exactly
`h d^2/2 + h sigma_t omega + (h^2/2) kappa_t omega^2`, [W, Section 7.3]).

**Node bounds.** A *node* is a set `{u_t in I_t, t in E}` of the feasible
set (other controls in `U`). Its bound is the calibration bound of
[R, Definition 1.1] over the node: the stage minima are taken over
`D_t x I_t`. Every such bound is valid for the node, for every family
([R, Proposition 1.2]).

## 1. The questions and what was known

[W, Section 6] listed what still works when `kappa_tau < 0`: the certificate
with a proved `O(h^2)` gap; exact certificates on grids with enough vertex
margin (a fraction `D/F''(tau)` of grids by the phase model); the discrete
maximal recursion at practical `h` (which breaks for all small `h` on grids
with a fractional stage, [W, Proposition D]); long windows (`Omega(1/h)`
stages, necessary only); a convexification bound special to the toy; and
branching, sketched to give only `epsilon`-certificates
[W, Proposition E]. The open items were: which certificates prove
optimality and at what size; whether `f* = J(zbar)`; and the several-switch
and terminal-row versions of Theorems A–B.

## 2. The `kappa`-split identity and the convexification bound

**Proposition 2.1 (`kappa`-split identity).** Let `b` be constant and
`l_1(t, x) = c(t)^T x + c_0(t)`; `a`, `l_0`, `Phi` arbitrary. Let `Jt(u)` be
the Euler cost with `l_1(t, x_t) u_t` replaced by
`l_1(t, x_t + (h/2) b u_t) u_t`. Then for every control sequence

```
J(u) = Jt(u) + (h^2/2) sum_t kappa_t u_t^2,        kappa_t = -c(t)^T b .
```

*Proof.* The two costs have the same states. Stage by stage,
`h [l_1(t, x_t) - l_1(t, x_t + (h/2) b u_t)] u_t = -(h^2/2) c(t)^T b u_t^2`. □

*What `Jt` is.* For a quadratic family `S`, the stage residual of `Jt` has
`u`-curvature `h^2 (b^T grad^2 S_{t+1} b - kappa_t)`, which tends to 0 for a
tangential family (`b^T S_xx b = kappa_tau` at the switch, [W,
Proposition 1.2]). So `Jt` is a transcription with zero switch
self-curvature, the case of [W, Theorem B]. The term `(h^2/2) kappa_t u_t^2`
is exactly the part of the diagonal of the reduced Hessian that the
left-point evaluation of the bilinear term omits: the off-diagonal entries
contain `h^2 c^T b` (later states see `u_t`), the diagonal does not (the
current state does not), which is (0.1). For the toy (`a = 0`, `b = 1`)
`x_t + (h/2) u_t` is the midpoint and `Jt` is the transcription of the
reformulated problem with `l_1 = 0` and terminal cost `Phi + k x^2/2`
(discrete chain rule); this is the toy identity of [W, Section 6] found by
the reviewer.

*Which structure makes `h^2 sum u_t^2` terms appear.* Exactly the
combination "explicit (left-point) evaluation of `l_1(x) u` along a
constant `b` with `grad l_1^T b != 0`". With state-dependent `b` or nonlinear
`l_1`, `kappa_t` depends on `(x_t, p_t)` and the identity holds only up to
higher-order terms (not written out).

**Corollary 2.2 (vertex sequences; a `kappa = 0` lower bound).** Write
`q_t(u) = (u - u_-)(u - u_+) <= 0` on `U` and
`Jt'(u) = Jt(u) + (h^2/2) sum_t kappa_t [(u_- + u_+) u_t - u_- u_+]`
(`Jt` plus a linear term). Then `J = Jt' + (h^2/2) sum_t kappa_t q_t(u_t)`.
(a) On every bang-bang control sequence `J = Jt'`. (b) If all
`kappa_t <= 0`, then `J >= Jt'` on `U^N`, so `f* >= min Jt'`; equality holds
if some minimizer of `Jt'` is bang-bang, and, when all `kappa_t < 0`, only
then.

*Proof.* `kappa_t u^2 = kappa_t [q_t(u) + (u_- + u_+) u - u_- u_+]`;
`q_t = 0` at the vertices and `kappa_t q_t >= 0` when `kappa_t <= 0`. If a
minimizer of `Jt'` is bang-bang, (a) gives `f* <= J = Jt'` there. If
`f* = min Jt'` and all `kappa_t < 0`, a minimizer `u*` of `J` has
`Jt'(u*) = min Jt'` and `sum kappa_t q_t(u*_t) = 0`, so it is bang-bang. □

So on bang-bang sequences `J` equals `Jt` plus the term
`(h^2/2) sum_t kappa_t [(u_- + u_+) u_t - u_- u_+]`, which is linear in `u`
and is a constant only when `u_- = -u_+` (as in all toys here).

*Remark 2.3.* (b) is the `alpha`BB underestimator of Adjiman et al. (1998)
with the exact `alpha = h^2 |kappa_t| / 2` per coordinate, made convex only
in the directions that the identity covers. Two uses:

- If `Jt'` is convex (its Hessian is `G = H - h^2 diag(kappa_t)`), `min Jt'`
  is a convex QP. This is the reviewer's bound for the toy, with gap
  `(h^2/2)|kappa_tau| (ubar_n - u_-)(u_+ - ubar_n) + [Jt'(ubar) - min Jt']`.
  The first term is at most the leading term of the window deficit,
  `(h^2/2)|kappa_tau| omega_hat_n^2`, since `(ubar_n - u_-)(u_+ - ubar_n) <=
  omega_hat_n^2`. The bracket is not bounded by this argument. A
  one-coordinate estimate (minimize `Jt'` over `u_n` alone, with
  `H_nn - h^2 kappa_tau = h^2 eta_L`) gives
  `h^2 kappa_tau^2 ((ubar_n - u_-) - (u_+ - ubar_n))^2 / (8 eta_L)`; with
  it, the whole gap is at most the leading window-deficit term when
  `|kappa_tau| <= 4 eta_L`, which holds when `q > 0`. That is a
  leading-order estimate, not a bound: other small-margin vertex stages
  can add to the bracket. Observed values ([W, Section 6], toy plus, float,
  `N = 50 … 8000`): convexification gaps 0.18–0.25 `h^2` against `K = 2`
  window deficits of 0.30–0.57 `h^2`.
- In general `Jt'` is a `kappa = 0` transcription. If [W, Theorem B]
  applied to it, its optimum would be certified exactly with one
  `O(1)`-stage window, and by (b) this would certify `f*` exactly on grids
  where `Jt'` has a bang-bang optimum, and only up to `O(h^2)` elsewhere.
  This is plausible but not checked: [W, Theorem B] assumes a stage cost
  affine in `u`, while the stage cost of `Jt'` is quadratic in `u`, and
  `Jt'` has its own KKT points, whose rate `e_h` was not examined. (By the
  phase model of [W, Remark 1.4] with `kappa = 0`, `Jt'` would have a
  fractional stage on a fraction `Delta^2 eta_L / F''(tau)` of the grids;
  heuristic, not tested.)
- Branching on `u_n` does not make this bound exact. In a child node
  `u_n in [l, r]` with `l = ubar_n` (fractional `n`, `sigma_n = 0`), the
  node underestimator `L = J + (h^2/2)|kappa_n| (u_n - l)(u_n - r)` (other
  coordinates as before) equals `J(zbar)` at `zbar` but has
  `dL/du_n = (h^2/2)|kappa_n| (l - r) < 0` there, so its minimum over the node
  is below `J(zbar)`; the same holds for a node containing `ubar_n` inside.
  So, as for calibrations (Corollary 4.2), finitely many nodes give only an
  `epsilon`-certificate: the underestimator is not exact at the minimizer
  whatever the node width, as for `alpha`BB underestimators at interior
  minimizers in general. (The first version called this the cluster
  problem of Du–Kearfott 1994 and Kannan–Barton 2017; the remarks after
  Theorem 4.3 explain why that framing overstated the link.) The node
  deficit is
  `~ h^2 kappa_tau^2 w^2 / (8 eta_L)` at leading order, smaller than the
  calibration deficit `(h^2/2)|kappa_tau| w^2` (estimate, not computed).

**When is `Jt` convex?** (`run_identity.py`, float eigenvalues; identity
residuals exact.) The identity residual is exactly 0 at random rational
controls for the toy and for [E]'s A, A−, A0' (`N = 20, 50`). The smallest
eigenvalues divided by `h^2`:

| example | `kappa_tau` | `N` | `lambda_min(H)/h^2` | `lambda_min(G)/h^2` | negative eigenvalues of `H` / of `G` |
|---|---|---|---|---|---|
| toy plus | -0.5 | 100 | -0.4950 | +0.0050 | 93 / 0 |
| toy plus | -0.5 | 800 | -0.4994 | +0.00063 | 782 / 0 |
| [E] A | +0.3 | 800 | -44.57 | -44.87 | 13 / 798 |
| [E] A− | -0.3 | 800 | -34.76 | -34.46 | 798 / 798 |
| [E] A0' | 0 | 800 | -38.43 | -38.43 | 798 / 798 |

For the toy `lambda_min(G) ≈ h^3/4 > 0` (to leading order only: with 40
digits, `lambda_min(G)/(h^3/4) - 1` is 2.4% at `N = 10`, 0.15% at `N = 40`
and 0.025% at `N = 100`, about `2.47/N^2`; `rev1_checks.py spectraG`):
`Jt` is convex and the
transcription is nonconvex only through `(h^2/2) kappa_tau sum u_t^2`. For
[E]'s examples the continuous control-to-cost map is itself nonconvex (the
running cost contains `-c x_2^2/2`, `c = 1`), and `G` has `lambda_min / h^2`
growing like `-1/h`. There the convexification gives nothing; calibrations,
which handle that nonconvexity through `S_xx`, are needed. So the
convexification bound of the toy is special structure: it needs `Jt'`
convex (or otherwise globally solvable).

## 3. Is `zbar` the discrete optimum?

**Lemma 3.1 (no two nearby fractional stages; LQ).** There is `c_0 > 0`
(depending on bounds of the data) such that for small `h` no local minimizer
of `J` over `U^N` has fractional controls at two stages `i != j` with
`|t_i - t_j| <= c_0 |kappa_tau|`, when `kappa_t = kappa_tau < 0` on that
interval.

*Proof.* Let `omega = e_i - e_j`, `i < j`. Then `m_t . omega` is 0 for
`t <= i`, `h F^{t-1-i} b` for `i < t <= j`, and `h F^{t-1-j}(F^{j-i} - I) b =
O(h^2 (j - i))` for `t > j`. The Gram part of `omega^T H omega` is therefore
`O(h^3 (j - i)) + O(h^4 (j - i)^2)`. The `l_1` part is
`2 sum_t h c^T (m_t . omega) omega_t`; only `t = j` contributes, with
`2 h c^T h F^{j-1-i} b (-1) = 2 h^2 kappa_tau (1 + O(h (j - i)))`. So
`omega^T H omega = 2 h^2 kappa_tau + O(h^3 (j - i))`, which is negative for
`(j - i) h <= c_0 |kappa_tau|`. At a local minimizer with both controls
interior, both switching values vanish, so `J` restricted to the feasible
segment through it in direction `omega` is a strictly concave quadratic with
zero slope: not a local minimum. □

For the toy, `omega^T H omega = h^2 (h |i - j| - 2k)` exactly, so
`c_0 = 2` (`|t_i - t_j| < 2|kappa_tau|`).

**Proposition 3.2 (bang-bang pair flips; LQ, `e_h = O(h)`).** Let `i < j` be
stages within `C h` of `tau`, with `ubar_i = u_+` before and `ubar_j = u_-`
after the switch (sign convention of the toys: `sigma_dot > 0`). Flipping
both (`omega = -Delta e_i + Delta e_j`) changes `J` by

```
h^2 D (j - i) + O(h^3 (j - i)^2 + h^2 (e_h + h))     (the kappa_tau terms cancel).
```

*Proof.* The first-order change is `h Delta (|sigma_i| + |sigma_j|) = h Delta
(sigma_j - sigma_i)`. By [W, Lemma 1.3] summed from `i` to `j`,
`sigma_j - sigma_i = h gamma (j - i) + h kappa_tau (ubar_j - ubar_i) +
O(h (e_h + h))(j - i) = h [gamma (j - i) + Delta |kappa_tau|] + …`. The
second-order change is `omega^T H omega / 2 = Delta^2 h^2 kappa_tau +
O(h^3 (j - i))` by the computation in Lemma 3.1. The sum is
`h^2 [D (j - i) + Delta^2 |kappa_tau| - Delta^2 |kappa_tau|] + …`. □

So moving one control across the switch against the structure (the start of
chattering) costs at least `h^2 D (1 - o(1))`, whatever `kappa_tau`. By
Corollary 2.2(a) the same holds for every bang-bang perturbation near the
switch: on bang-bang sequences the problem is the `kappa = 0` problem `Jt'`,
whose switching values increase by `h gamma` per stage with no jump.
Combined with Lemma 3.1, a minimizer near the switch is a monotone switch
with at most one fractional stage, i.e. one of the points of the phase model
[W, Remark 1.4]. *What is not proved:* that the best of these is the KKT
point `zbar` for all small `h` (the phase model is a heuristic); and the
`O(h^3)` remainders are not summed over long perturbations. This is
supplied grid by grid by the exact certificates below.

**When `q < 0 < eta_L`.** Then `H_nn = h^2 q (1 + o(1)) < 0` at stages
near the switch: a fractional stage there is a strict local maximum of `J`
along its own coordinate, so every KKT point with a fractional stage near
the switch is a saddle. Minimizers near the reference trajectory are
therefore bang-bang: away from the switch their switching values are
bounded away from 0, so their fractional stages can only lie near the
switch. (Minimizers far from the reference trajectory are not covered.)
For the `q < 0` toy below every diagonal entry `H_tt` is negative, so every
minimizer is bang-bang.
Hence `f* < J(zbar)` for such `zbar`, but the optimum is still a
monotone switch. (Phase model: within-stage curvature `h^2 Delta^2 q < 0`,
kinks convex since `D - Delta^2 kappa_tau > 0`; local minima only at
integer positions.) Section 5.3 certifies this exactly on a toy with
`q = -0.56`. That toy is the `kappa = -1` toy plus the separable term
`-h^2 sum u_t^2`: by Corollary 2.2(a) the two agree on every bang-bang
sequence; indeed, where both have the same bang-bang KKT point
(`N = 1000, 2000`), their plain-certificate gaps and vertex-flip margins
(the change of `J` when one vertex control is flipped; the switching values
themselves differ by `2h`) coincide. Their certificates do not coincide:
node bounds
are minima over continuous nodes, where the two differ (at `N = 2000` the
outer node `{u_558 in [-0.0475, 1]}` has bound `+1.763 h^2` above `f*` for
the `q < 0` toy and `+0.765 h^2` for the `kappa = -1` toy, exact,
`rev1_checks.py qneg`). Their fractional KKT points also differ.

**Answer to "can `f* = J(zbar)` fail?".** For a fractional KKT point: yes,
when `q < 0` (saddle). With several switches, KKT points that combine
different phases of the switches coexist, and a local method can return a
non-optimal one. Ours did once, on an instance that differs from the
documented one by one stage of the target (Section 9, data convention):
the global optimum (certified exactly) was another monotone KKT point
`0.31 h^2` lower. On the documented instances the returned KKT point was
the certified optimum on all 36 grids of Section 9.1 (certificates at the
three `kappa = -0.5`, `N = 4000` grids added in the round-2 revision). When
`q > 0` and the KKT point is the best phase: `f* = J(zbar)` on every grid
of the `q > 0` table of Section 5.3 and of Section 9.1, each of which now
has an exact certificate;
at leading order the optimum is monotone with at most one fractional stage
(Lemma 3.1, Proposition 3.2). The discrete optimum does not chatter near a
regular switch at leading order, unlike the singular arcs of [SA], where a
negative accessory symbol makes long runs of fractional stages saddles.

## 4. Branch and bound with node-specific calibrations

Fix the switching stage `n` (the fractional stage, or the vertex stage with
the smallest margin). Nodes are `N_I = {u_n in I}`, `I = [l, r]`.

**Theorem 4.1 (what a node bound can be; LQ, exact).** Let `z^A` be any
feasible point of `N_I` (the *anchor*), `p^A` its discrete costates and
`sigma^A` its switching values. Let `S` be any family that is quadratic at
the exit `b` of a window `W = [a, b)` containing `n` (no window: `W = {n}`,
`b = n + 1`), with slope `grad S_b(x^A_b) = p^A_b` and curvature `P_b`; the
other `S_t` are arbitrary. Let `V_t` be the window's Lyapunov transport of `P_b`
(`V_b = P_b`, `V_t = h l_{0,xx} + F^T V_{t+1} F`), and
`kappa_W := b^T V_{n+1} b`. Then for every `u in I`, with `omega = u - u^A_n`,

```
B(N_I) <= J(z^A) + h sigma^A_n omega + (h^2/2) kappa_W omega^2 .              (4.1)
```

*Proof.* By [R, Definition 1.1], `B <= S_0(x_0) + sum_{t notin W}
rho_t(z^A_t) + J_W(z^W) + (Phi - S_N)(x^A_N)` for any window trajectory
`z^W` in the node's relaxation (each infimum is at most the value at
`z^A`); with `z^W = z^A` on `W` this is `J(z^A)` by telescoping. Take `z^W`
from `x^A_a` with `u_n` changed to `u`. For LQ data the states after `n`
move by `d_t = h F^{t-1-n} b omega`. The first-order change of `J_W` is
`h omega l_1(x^A_n) + sum_{n<t<b} h (grad l_0 + grad l_1 u^A_t)^T d_t +
(p^A_b)^T d_b = h omega (l_1(x^A_n) + b^T p^A_{n+1}) = h sigma^A_n omega`
by the discrete adjoint equation; the second-order change is
`(1/2) sum_{n<t<b} h d_t^T l_{0,xx} d_t + d_b^T P_b d_b / 2 =
(h^2/2) omega^2 b^T V_{n+1} b`. The trajectory stays in the boxes for small
`h` (interior states, as in [W, Theorem C]). □

This is the computation of [W, Theorem C and Proposition D] with an
arbitrary anchor. A bound is called **`kappa`-limited** when
`kappa_W <= kappa_tau + theta_h` with `theta_h -> 0`. Known cases: the
transferred families of [R, Theorem 4.1] with `|W| h -> 0` ([W,
Proposition 1.2]: `b^T P b -> kappa_tau` near the switch; the transport over
`|W|` stages adds `O(|W| h)`), and, for the KKT anchor, quadratic families
exact over `R^n x U` after a window exit `o(1/h)` stages after the switch
([W, Proposition D], which gives `limsup kappa_W <= kappa_tau`: an upper
bound, not an equality, and that is all that `kappa`-limited requires).
For anchors at node KKT points other than `zbar`,
Proposition D's proof applies verbatim when the node's KKT point has the
same switching structure (switching values growing linearly away from the
switch); we assume this where needed.

**Corollary 4.2 (no finite exact certificate at a fractional stage).**
Assume `f* = J(zbar)` and that `n` is a fractional stage of `zbar`. Let a
certificate partition `U` for `u_n` into finitely many intervals and bound
each node by a calibration bound (the stage infima over an open or half-open
interval equal those over its closure, so we may take the intervals closed,
overlapping at end points). If
the families of the nodes that contain `ubar_n` are `kappa`-limited, the
certificate is not exact: some node has bound `< J(zbar)`.

*Proof.* Some node `N_I`, `I = [l, r]`, contains `ubar_n` and has positive
length on one side of it, say `r > ubar_n`. Its optimum is `zbar`. For every
family, `B(S) = J(zbar) - sum_t [rho_t(zbar_t) - inf rho_t] - (terminal
loss)` (telescoping, [R, Proposition 1.2]), so `B = J(zbar)` requires every
stage outside the windows and the terminal term to be minimized at `zbar`.
At interior states this forces zero `x`-gradients, i.e. (backwards from the
terminal) slopes equal to `zbar`'s costates at every stage outside the
windows. So `z^A = zbar` is an admissible anchor in Theorem 4.1, and (4.1)
with `u = r` and `sigma_n = 0` gives
`B <= J(zbar) - (h^2/2)(|kappa_tau| - theta_h)(r - ubar_n)^2 < J(zbar)`. □

*Vertex stages are different.* If `n` is a vertex stage with a small margin
(`0 < |sigma_n| < h Delta |kappa_tau| / 2`, [W, Theorem C(ii)]), the same
argument gives `B <= J(zbar) + h |sigma_n| w - (h^2/2)(|kappa_tau| -
theta_h) w^2` for the node `[ubar_n, ubar_n ± w]`, which is `< J(zbar)` only
when `w > 2 |sigma_n| / (h |kappa_tau|)`. Cutting the range of `u_n` at
distance `w_1 < 2 |sigma_n| / (h |kappa_tau|)` from `ubar_n` makes the inner
node exact, and the outer node has optimum
`J(zbar) + h |sigma_n| w_1 + (H_nn/2) w_1^2` at leading order, so a finite
exact certificate with
ordinary node families exists on such grids when the outer node's own
deficit is smaller than that (not run with ordinary families only; on the
small-margin vertex grids of Section 5.3 the lifted certificate used two
nodes). The
obstruction of Corollary 4.2 is specific to `sigma_n = 0`.

This strengthens [W, Proposition E] (fixed family) to node-specific
families, with the class stated: what matters is not the anchor but the
`u`-curvature `kappa_W` that the window can see.

**Theorem 4.3 (node count for `epsilon`-certificates; leading order).**
Assume LQ data, (SH), `kappa_tau < 0`, `q > 0`, a fractional stage `n`,
`f* = J(zbar)`, and the neighbour-margin condition (VM) of Theorem 5.4. Let
`0 < rho_0 <= rho = c_0 / (2 eta_bar)` (Theorem 5.4), so that for
`|v - ubar_n| <= rho_0` every stage other than `n` of `z(v)` (`zbar` with
`u_n = v`) is exact for its transferred family and `z(v)` is the optimum of
`{u_n = v}` (Theorem 5.3). Let
`w_0 = sqrt(2 epsilon / (h^2 |kappa_tau|))` and

```
rho_u = 1 + 2 q / |kappa_tau|,        rho* = 1 + (q + sqrt(q^2 + q |kappa_tau|)) / |kappa_tau| .
```

(a) *Upper bound.* For every fixed `rho' < rho_u` and small `h` there is a
partition of `[ubar_n - rho_0, ubar_n + rho_0]` into at most
`1 + 2 ceil(log(rho_0 / w_0) / log rho')` intervals whose bounds with
transferred families anchored at their own optima are
`>= J(zbar) - epsilon`: the central interval `[ubar_n - w_0, ubar_n + w_0]`
and geometric intervals `[ubar_n + delta_i, ubar_n + delta_{i+1}]`,
`delta_{i+1} = rho' delta_i`, and their mirror images.

(b) *Lower bound.* Every partition of the same range into intervals whose
bounds are `kappa`-limited, whose families have exit slope equal to the
costate of the node optimum (as for every family that is exact at the node
optimum outside its window, by the argument of Corollary 4.2), and that are
`>= J(zbar) - epsilon`, has at least
`2 log(rho_0 / (C w_0)) / log(rho* + o(1)) - O(1)` intervals. For
`epsilon > 0` nothing forces a node family to be exact anywhere, so the
exit-slope condition is a restriction of the class, not a consequence;
families outside the class are not covered by (b).

So `O(log(h^2 / epsilon))` nodes in the switching control suffice, each
costing one calibration (`O(N)`), and node families of the class in (b)
need at least that many; no finite number of `kappa`-limited nodes gives
`epsilon = 0` (Corollary 4.2).

*Proof (leading order).* On `[ubar_n - rho_0, ubar_n + rho_0]` the node
optimum is `z(v)` and `J(z(v)) = J(zbar) + (H_nn/2)(v - ubar_n)^2` with
`H_nn = h^2 q (1 + o(1))`. (a) The central node with anchor `zbar` loses
only at stage `n`: `max over the two ends of (h^2/2)|kappa_tau| w_0^2 (1 +
o(1)) = epsilon`. A node `[ubar_n + delta, ubar_n + delta + w]` has its
optimum at `z(ubar_n + delta)`, where stage `n` is a vertex of the node with
`sigma_n = H_nn delta / h`; its loss over `[0, w]` is
`max(0, -(H_nn delta w - (h^2/2)|kappa_n| w^2))`, zero iff
`w <= 2 q delta / |kappa_tau| (1 + o(1))`; the other stages are exact by
(VM). So these nodes are exact for their own optima, which exceed
`J(zbar)`. Covering from `delta_1 = w_0` to `rho_0` with ratio `rho'` gives
(a). (b) By (4.1) with the anchor at the node optimum `z(ubar_n + delta)`
and `u` at the far end, `B <= J(zbar) + h^2 [q delta^2/2 + q delta w -
(|kappa_tau| - theta) w^2/2](1 + o(1))`. `B >= J(zbar) - epsilon` forces
`w <= (rho* - 1 + o(1)) delta + w_0 (1 + o(1))`, i.e.
`delta_{i+1} <= (rho* + o(1)) delta_i + w_0`. The node containing
`ubar_n` has half-length `<= w_0 (1 + o(1))` by Corollary 4.2's estimate.
Iterating, `delta_i <= C w_0 (rho* + o(1))^i`, which reaches `rho_0` only
for `i >= log(rho_0 / (C w_0)) / log(rho* + o(1))`. □

*Remarks.* The greedy partition (each node as long as possible) attains
the ratio `rho*` (it uses the slack `epsilon` in each node, which (a) does
not).

*Relation to the cluster problem (revised after review).* The node bound
is a relaxation whose error is second order in the node length, with
prefactor `h^2 |kappa_tau| / 2`. For such relaxations
Wechsung–Schaber–Barton (2014) show that the number of boxes in the cluster
around a minimizer does not depend on `epsilon`, and that it is 1 when the
prefactor is at most `lambda_1/8` (`lambda_1` the smallest Hessian
eigenvalue at the minimizer, here `H_nn = h^2 q`). In one dimension,
covering a fixed range with nodes that grow geometrically away from the
minimizer costs `Theta(log(1/epsilon))` nodes for any relaxation with
second-order error; that is the depth of the geometric covering, not a
cluster blow-up. So the logarithmic count of Theorem 4.3 is the generic
one-dimensional behaviour and is not new. What is specific here:

- `epsilon = 0` is impossible with finitely many `kappa`-limited nodes
  (Corollary 4.2), because the bound is not exact at the minimizer whatever
  the node width: a node that contains `ubar_n` or has it as an end point
  loses `(h^2/2)(|kappa_tau| - o(1)) w^2`, with `w > 0` its length on one
  side of `ubar_n`. (Relaxations that are not exact at an interior
  minimizer, such as `alpha`BB, behave the same way in general; what is
  specific is that here this holds for every `kappa`-limited calibration
  bound, including the node-specific ones);
- the explicit ratio `rho*`, which includes the first-order term
  `h sigma^A_n omega` of the anchored bound (4.1);
- the lifted bound of Section 5 removes the obstruction.

**Numbers** (`run_kneg.py eps`, float node bounds; `epsexact`, exact
re-check). Greedy partitions of `U` for `u_n`, transferred family
`P = -k` anchored at each node's KKT point; counts against
`1 + sum_± ceil(log(a_±/w_0)/log rho*)` with `a_± = u_+ - ubar_n`,
`ubar_n - u_-` (the whole control range, i.e. `rho_0 = a_±`):

| toy, `N` | `q` | `rho*` | `epsilon/h^2`: 1e-1 | 1e-2 | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 | 1e-8 |
|---|---|---|---|---|---|---|---|---|---|---|
| `kappa = -0.5`, 1000 | 1.522 | 7.553 | 3 (3) | 3 (3) | 5 (5) | 6 (6) | 7 (7) | 8 (8) | 9 (9) | 11 (11) |
| `kappa = -0.5`, 4000 | 1.5225 | 7.555 | 3 (3) | 3 (3) | 5 (5) | 6 (6) | 7 (7) | 8 (8) | 9 (9) | — |
| `kappa = -0.5`, 8000 | 1.5225 | 7.555 | 2 (2) | 3 (3) | 5 (5) | 6 (6) | 7 (7) | 8 (8) | — | — |
| `kappa = -1`, 1001 | 1.441 | 4.316 | 3 (3) | 5 (5) | 6 (7) | 7 (7) | 9 (9) | 11 (11) | 13 (13) | 14 (14) |
| `kappa = -1`, 1002 | 1.441 | 4.317 | 3 (3) | 5 (5) | 6 (6) | 8 (8) | 9 (9) | 11 (11) | 12 (13) | 14 (14) |
| `kappa = -1`, 4002 | 1.441 | 4.317 | 2 (2) | 3 (3) | 5 (5) | 7 (7) | 9 (9) | 9 (9) | 11 (11) | — |

(observed, predicted in parentheses; "—": below float resolution of `J`,
`epsilon < 100 u_round`.) The ratios of consecutive node ends (distances
from `ubar_n`, nodes not touching `±1`) are 7.553–7.695 for
`kappa = -0.5`, against `rho* = 7.553`. For `kappa = -1` they are
4.316–4.567 in the inner rings, against `rho* = 4.316`, and 2.625–3.497 in
the outermost rings (one per side at most; `logs/eps.json`). Those smaller
outer ratios do not contradict Theorem 4.3, which bounds ratios from above
and concerns only the range within `rho_0` of `ubar_n`. The first ring is
slightly wider than `rho*` because the central node uses its whole
`epsilon`. At fixed `epsilon / h^2` the predicted counts depend on `N`
essentially only through the position of `ubar_n` (`q` and `rho*` change
by less than 0.1% between the tested `N`), for both toys, and the observed
counts follow them (except the two `kappa = -1` counts discussed below).
For `kappa = -0.5` the counts at `N = 1000, 4000, 8000` agree except at
`epsilon / h^2 = 1e-1`, where `N = 8000` has 2 nodes (predicted 2) against
3 at `N = 1000` and `4000`: there `ubar_n = -0.461` lies within
`w_0 = sqrt(2 epsilon / (h^2 |kappa_tau|)) = 0.632` of `u_- = -1`, so the
central node reaches `u_-` (float rerun: central node `[-1, 0.172]`,
`rev2_checks.py eps01`). At other `epsilon` the predicted split between
the two sides changes with `ubar_n` (for example 3 + 2 outer nodes towards
`u_+` and `u_-` at `N = 1000` against 2 + 3 at `N = 4000`,
`epsilon / h^2 = 1e-4`) while the
total does not. For `kappa = -1` the counts at
`N = 1001, 1002` and `4002` differ by up to 2 at fixed `epsilon / h^2`, for
the same reason (`ubar_n = 0.129, 0.313, -0.905`). The prediction
applies the ratio `rho*` over the whole control range, while Theorem 4.3
concerns only the range within `rho_0` of `ubar_n`; farther out the
neighbour stages lose their margins, the node optima are no longer `z(v)`,
and nodes can be relatively longer, which explains the two counts one below
the prediction. For `kappa = -1` the greedy rule (each node as long as
possible) stalled in that outer range at some `(N, epsilon)`: a node ended
where no further node could start. A backtracking step (shorten the
previous node by 30% and retry) removed the stalls. The float partitions
were built with target `epsilon` (no safety factor), and 25 of the 44
logged minimum node margins lie below `-epsilon`, 15 of them by a relative
`3e-11` to `2e-7` and 10 by `2e-6` to `1.2e-3` (rounding; the largest
excesses occur where `epsilon` is within a few hundred `u_round` of `J`).
So the float table is screening, not a certificate. Exact re-check, only at
`N = 1000`, `kappa = -0.5`: the
partitions for `epsilon/h^2 = 1e-4` (6 nodes) and `1e-8` (11 nodes), built
in float with target `0.9 epsilon`, have exact node bounds
`>= J(zbar) - 0.90 epsilon` and `>= J(zbar) - 0.909 epsilon`
(`logs/epsexact.json`), and their rationalized node ends cover `[-1, 1]`
without gaps (`rev1_checks.py epscover`, added in revision).

## 5. Lifted (parametric) calibrations: exact certificates

**5.1 Construction.** Fix the stage `n` and a node `N_I`. For `v in I` let
`z(v)` be the anchor `z^A` with `u_n` replaced by `v` (states re-simulated),
`p(v)` its costates, and `S^v` the family with slopes `p(v)` and fixed
curvatures `P_t`. The *lifted bound* of a subinterval `V subset I` is

```
B_lift(V) := min_{v in V} B(S^v; {u_n = v}),
```

the calibration bound of the slice `{u_n = v}` (stage `n` has no control
there), minimized over `v`.

**Lemma 5.1 (validity).** `min {J(z) : z feasible, u_n in V} >= B_lift(V)`.

*Proof.* For each `v`, `B(S^v; {u_n = v})` is a valid bound for the slice
([R, Proposition 1.2]); take the minimum over `v`. □

*Lifted-state reading.* Add the constant state `v_{t+1} = v_t`, `v_0 in V`
free, and let stage `n` use `u_n = v_n`. The family
`S_t(x, v) = S^v_t(x) + c_t(v)`, with `c_t(v)` the cost-to-go of `z(v)` from
stage `t` minus `S^v_t(x_t(v))`, is a calibration of this lifted problem in
the sense of [R, Definition 1.1]; when every stage is exact for every `v`,
its bound is `inf_{v in V} S_0(x_0, v) = min_{v in V} J(z(v))`. The
`v`-dependence of the initial term carries the curvature `H_nn / 2 =
(h^2/2) q (1 + o(1))` of the true cost in `u_n`, which a calibration on `x`
alone cannot represent at the switch ([W, Proposition 1.2] forces its
`u`-curvature to `kappa_tau`); in continuous time this curvature lives in
field-type calibrations whose Hessian jumps across the switching surface,
which [W] noted are not covered by its negative results.

**Lemma 5.2 (structure; LQ, exact).** For LQ data and fixed curvatures
`P_t`:

1. `z(v)`, `p(v)` and `sigma_t(v) = sigma^A_t + H_{tn} (v - u^A_n) / h` are
   affine in `v`.
2. For `t != n`, `rho^v_t(z) - rho^v_t(z_t(v)) = h sigma_t(v) omega +
   Q_t(d, omega)` with `d = x - x_t(v)`, `omega = u - u^A_t` and a quadratic
   `Q_t` that does not depend on `v` (its coefficients are `K_t`, `beta_t`,
   `kappa_t` of the family). Hence the loss of stage `t` over
   `R^n x U_t`, `loss_t(v) = -min_{d, omega} [h sigma_t(v) omega + Q_t]`, is
   convex in `v` (a supremum of affine functions), and
   `{v : loss_t(v) = 0}` is an interval. The same holds over the boxes
   `D_t x U_t` when the minimizing `d` stays interior (as in the toys, where
   `beta_t = 0` and the minimizing `d` is 0).
3. Stage `n` (no control) has residual `K_n`-quadratic in `d` with zero
   gradient at `x_n(v)`: exact for all `v` iff `K_n >= 0` on the box. The
   terminal term has slope `grad Phi(x_N(v))` and Hessian `Phi_xx - P_N`:
   exact for all `v` iff (T) holds.
4. On `V := intersection of the zero-loss intervals` (with 3.),
   `B_lift(V) = min_{v in V} [J(z^A) + h sigma^A_n (v - u^A_n) +
   (H_nn/2)(v - u^A_n)^2]`, a one-dimensional quadratic minimization.

*Proof.* 1: `J` is quadratic, states are affine in the controls, and the
adjoint is linear in states and controls. 2: with slopes `p(v)` the
`x`-gradient of the residual at `z_t(v)` is 0, its `u`-derivative is
`h sigma_t(v)`, and its second-order part depends only on `P_t`, `P_{t+1}`
and the data. 3: as in [W, Section 7.2] and [R, Theorem 4.1]. 4: telescoping
for each `v`, then `J(z(v))` is the stated quadratic. □

For vertex stages with `kappa_t < 0` and `beta_t = 0` (the toys), the
zero-loss condition is the affine inequality
`h sigma_t(v) omega_f + (h^2/2) kappa_t omega_f^2 >= 0`, `omega_f` the
move to the other end of `U_t`: the vertex-margin condition
`|sigma_t(v)| >= h Delta |kappa_t| / 2` of [W, Section 6], now as a function
of `v`.

**Theorem 5.3 (exact certificate from one lifted node).** If, for a node
`N_I` with anchor `z^A` and the interval `V subset I` of Lemma 5.2, every
other part of `I` is covered by nodes whose bounds are `>= J*` and
`B_lift(V) >= J*`, where `J*` is the cost of a feasible point, then
`f* = J*` (an exact certificate). If `z^A = zbar`, `n` is a fractional stage
(`sigma_n = 0`) or a vertex stage, `ubar_n in V`, and `H_nn > 0`, then
`B_lift(V) = J(zbar)`.

*Proof.* Lemmas 5.1–5.2. With `z^A = zbar`, the quadratic of Lemma 5.2(4)
has minimum at `ubar_n` (fractional: zero slope; vertex: the KKT sign
`sigma_n (v - ubar_n) >= 0` and `H_nn > 0`). □

**Theorem 5.4 (the central node is exact for all small `h`).** Assume (SH)
with LQ data, `e_h = o(sqrt h)`, `kappa_tau < 0`, `q > 0`, the terminal
condition (T), and

> **(VM)** for some `c_0 > 0` and all small `h`, every vertex stage `t != n`
> of `zbar` has `|sigma_t| >= h (Delta |kappa_tau| / 2 + c_0)`.

Let `eta_bar >= sup |H_{tn}| / h^2` over stages within `C h` of `tau`
(`eta_bar = eta_L + o(1)`). Then for small `h` the lifted node anchored at
`zbar` has `V supset [ubar_n - rho, ubar_n + rho] cap U` with
`rho = c_0 / (2 eta_bar)`, and `B_lift(V) = J(zbar)`. In particular `zbar`
is optimal among all feasible points with `|u_n - ubar_n| <= rho`.

*Proof.* For `|v - ubar_n| <= rho`: near the switch,
`|sigma_t(v) - sigma_t| = |H_{tn}| |v - ubar_n| / h <= h c_0 / 2`, so
`|sigma_t(v)| >= h (Delta |kappa_tau| / 2 + c_0 / 2)` with the KKT sign
kept; far from the switch `|sigma_t| >= c s_t` and the change is `O(h)`.
`z(v)` differs from `zbar` in one control, so it is within `e_h + O(h)` of
the continuous trajectory and its costates likewise. The argument of
[W, Section 6, second bullet] (Theorem A, zones (ii)–(iii), with the
`u`-concavity term `h^2 Delta |kappa_tau| / 2` absorbed by the margin, and
`e_h = o(sqrt h)` making the cross terms `o(h)`) applies at every stage
`t != n` of `z(v)` with constants uniform in `v`; so each such stage is
exact for `S^v`. Stage `n` and the terminal term are exact by
Lemma 5.2(3) ((P2) and (T)). Theorem 5.3 concludes. □

*When (VM) holds.* By [W, Lemma 1.3] the neighbours of a fractional stage
have `|sigma_{n-1}| = h [gamma + (u_+ - ubar_n)|kappa_tau|] + o(h)` and
`|sigma_{n+1}| = h [gamma + (ubar_n - u_-)|kappa_tau|] + o(h)`; stages
further out have larger margins. So (VM) holds for every position of
`ubar_n` if `gamma > Delta |kappa_tau| / 2` (i.e. `2 D > Delta^2 |kappa_tau|`),
and otherwise for `ubar_n` away from the ends of `U`. If it fails at some
stages, lift them too: `E` = the stages with small margin (at most
`Delta |kappa_tau| / gamma + 2` of them); `z(v)`, `v in U^E`, is affine,
the zero-loss conditions are affine in `v`, and `B_lift` is the minimum of
the quadratic `J(z(v))` over a box in `|E|` variables, computable exactly
(`lifted.py`, `lifted_box`). It equals `J(zbar)` iff `zbar` is optimal among
the controls that differ from `ubar` only on `E` (which Section 3 supports
at leading order).

**Remark 5.5 (outer nodes; heuristic).** Outside the central node the
problem `{u_n in I}` has optimum `>= J(zbar) + c h^2` (phase-model
convexity), and ordinary node families lose at most `O(h^2)` per
small-margin stage. Everything scales with `h^2` and, in the rescaled
switch-local model, converges as `h -> 0`; so a number of outer nodes
independent of `h` should suffice. This is not proved (a proof would also
need uniformity over the phase of `tau / h`, which does not converge as
`h -> 0`). On the scalar
single-switch toys 1–2 outer nodes sufficed at every `N` (Section 5.3); on
the two-switch toys 3–9 nodes including bisections (Section 9.1; 2–13 on
the earlier instance of that section).

**5.2 Size.** The lifted certificate consists of: the anchor's costates and
their derivative in `v` (two adjoint sweeps, `O(N n^2)`), the interval `V`
(one affine condition per stage), a one-dimensional quadratic minimization,
and the outer nodes, each an ordinary calibration (`O(N)`). With `O(1)`
outer nodes the total is `O(N)`, the size of a single calibration, and it is
exact. Compare: windows of `o(1/h)` stages never; fixed node families
`Theta(N log(h^2/epsilon))` for an `epsilon`-certificate; the maximal
recursion exact only while it does not break, which fails for small `h` on
grids with a fractional stage ([W, Proposition D]).

**5.3 Results on the toys** (`run_kneg.py lifted lifted2 qneg`; exact
rational arithmetic throughout: exact KKT points, exact node KKT points,
exact stage minima over the boxes, exact `V` and quadratic minima). Toy
plus of [W] (`x' = u`, `a = 2` then `-1` at `t = 1`, `k x u`, `Phi = x`,
box `|x| <= 2`) with `k = 0.5` (`kappa_tau = -0.5`, `q = 1.52`) and
`k = 1` (`kappa_tau = -1`, `q = 1.44`, box `|x| <= 3`); tangential family
`P = -k`. "gap" is `(J(zbar) - B)/h^2` of the plain transferred
certificate; node bounds are given as `(B - J(zbar))/h^2`.

| `kappa_tau`, `N` | stage `n` | `ubar_n` | gap | lifted `V` | outer nodes (bound) | nodes |
|---|---|---|---|---|---|---|
| -0.5, 50 | fractional | 0.592 | 0.634 | [-0.333, 1] | [-1, -0.333] (+0.651) | 2 |
| -0.5, 100 | fractional | 0.355 | 0.459 | [-0.5, 1] | [-1, -0.5] (+0.556) | 2 |
| -0.5, 150 | fractional | 0.118 | 0.313 | [-0.674, 0.848] | [0.848, 1] (+0.405), [-1, -0.674] (+0.478) | 3 |
| -0.5, 200 | fractional | -0.118 | 0.313 | [-0.851, 0.668] | (+0.470), (+0.408) | 3 |
| -0.5, 500 | vertex | -1 | 0 | — | — | 1 (transferred family exact) |
| -0.5, 1000 | fractional | -0.247 | 0.389 | [-0.941, 0.568] | (+0.505), (+0.366) | 3 |
| -0.5, 2000 | vertex (`sigma/h = 0.491`) | -1 | 0.018 | [-1, -0.242] | [-0.242, 1] (+0.809) | 2 |
| -0.5, 4000 | fractional | 0.184 | 0.350 | [-0.615, 0.892] | (+0.381), (+0.486) | 3 |
| -0.5, 8000 | fractional | -0.461 | 0.533 | [-1, 0.406] | [0.406, 1] (+0.572) | 2 |
| -1, 200 | fractional | 0.528 | 1.167 | [-0.284, 0.906] | (+0.103), (+0.474) | 3 |
| -1, 1000, 1003 | vertex | -1 | 0 | — | — | 1 |
| -1, 1001 | fractional | 0.129 | 0.637 | [-0.516, 0.667] | (+0.209), (+0.299) | 3 |
| -1, 1002 | fractional | 0.313 | 0.862 | [-0.407, 0.776] | (+0.154), (+0.373) | 3 |
| -1, 2000 | vertex (`sigma/h = 0.117`) | -1 | 1.766 | [-1, -0.048] | (+0.765) | 2 |
| -1, 4000 | vertex (`sigma/h = -0.046`) | +1 | 1.908 | [0.019, 1] | (+0.739) | 2 |

Every row is an **exact certificate of `f* = J(zbar)`**: the nodes cover
`U` for `u_n` with all other controls free, and every node bound is
`>= J(zbar)`. The outer nodes are exact for their own optima (no stage
loses), which lie `0.10`–`0.81 h^2` above `J(zbar)`. In a one-off check
(not logged), the two end points of `V` at `N = 1000`, `kappa_tau = -0.5`,
were re-checked by rebuilding `z(v)` from scratch and recomputing all stage
minima (`lifted_check_ends`): both largest losses exactly 0. Times: under 1 s for `N <= 500`, 10 s (`N = 1000`), 184 s
(`N = 4000`), 563 s (`N = 8000`), dominated by exact stage minima.

*The `q < 0` toy* (`k = 3`, `Phi = x - x^2`, so `kappa_tau = -3`,
`q = -0.56`, `eta_L = 2.44`; it equals the `k = 1` toy plus
`-h^2 sum u_t^2`). Every diagonal entry `H_tt` is negative, so every
minimizer is bang-bang. At `N = 1000` the plain
transferred certificate is exact; a KKT point with two fractional stages
exists there (found by the active-set method from a fractional start in a
one-off float run, not logged) and lies `4.6 h^2` above `f*`, as a saddle
should (the review found, in exact arithmetic, a KKT point with adjacent
fractional stages 278, 279 lying `4.613 h^2` above `f*`). At `N = 200, 400,
2000` the weakest vertex stages lose (gaps 3.82, 6.06, 1.766 `h^2`); the
box version (`certify_multi`: lift the worst stage, split when needed) gives
exact certificates with 5, 6 and 2 nodes. At `N = 200` and 400 two adjacent
stages have small margins against `Delta |kappa_tau| / 2 = 3`: `|sigma|/h`
= 1.32 and 2.77 (stages 55 and 54) at `N = 200`, and 0.76 and 2.21
(stages 111 and 112) at `N = 400` (exact, `rev1_checks.py qneg`; the first
version gave the `N = 200` values for both grids). So the certificate
splits on two controls.

**5.4 Two-state example A− (float screening).** [E]'s example A− (`n = 2`,
`kappa_tau = -0.3`, `q = 1.2286`) with the transferred tangential family of
[W, Section 7.5] (`eps = 0.02`, `delta_1 = 0.1`); stage minima over the exact
reachable box by face enumeration (`run_n2lift.py`, imports [E]'s and [W]'s
code read-only; node KKT points by active-set Newton with the exact reduced
Hessian). Here `beta_t != 0`, so `V` was found by bisection on the
zero-loss condition rather than in closed form.

| `N` | failing stage (loss `/h^2`) | `ubar_n` | lifted `V` | outer node bound `- J(zbar)`, `/h^2` | certified (float) |
|---|---|---|---|---|---|
| 500 | 292: 0.0139 | 1.0000 | [0.0410, 1.0000] | [-1.000, 0.041]: +0.8454 | yes |
| 1000 | 585: 0.3921 | 1.0000 | [-0.0834, 1.0000] | [-1.000, -0.083]: +0.8332 | yes |
| 2000 | 1171: 0.4731 | 0.7771 | [-0.3306, 1.0000] | [-1.000, -0.331]: +0.7538 | yes |
| 4000 | 2343: 0.2028 | 0.1631 | [-0.8242, 1.0000] | [-1.000, -0.824]: +0.5989 | yes |

At all four grids one stage fails for the transferred family (a
small-margin vertex at `N = 500, 1000`, the fractional stage at
`N = 2000, 4000`; the losses agree with [W, Section 7.5]). The lifted node
covers most of `U` (its other end is `u_+` in every case) and one ordinary
node anchored at its own optimum covers the rest, with bound `0.60`–`0.85
h^2` above `J(zbar)` and no stage loss. So in float the lifted construction
passes the screening for `f* = J(zbar)` on this nonconvex two-state
example, where the convexification of Section 2 is unavailable. This is
screening, not a certificate, for two reasons. First, the bisection for `V`
and all stage minima are in floating point (tolerance `1e-12 h^2` on the
losses), and no exact recheck was made. Second, with `beta_t != 0` and
stage minima over the reachable box, the zero-loss set of a stage in `v`
is not shown to be an interval: Lemma 5.2(2) covers minima over
`R^n x U_t`, or over boxes when the minimizing `d` stays interior, and
neither was checked here. The bisection tests finitely many `v`, so zero
loss on all of `V` is not established, even in float. Times: 72 s to
23 min per grid.

## 6. Several regular switches: Theorems A_k, B_k

**Standing hypotheses (SH_k).** Those of (SH) [W, Section 0.3] with (H2)
replaced by: `(x*, u*)` bang-bang with `k` regular switches
`tau_1 < … < tau_k` (`sigma(tau_j) = 0`, `sigma_dot(tau_j) != 0`,
`b(x*(tau_j)) != 0`); (H3) with tangency `S_xx b = w_j` at every `tau_j` and
the margin `|sigma| > Delta |beta|^2 / (2 mu)` for `t` off the switches; the
time regularity of `partial_t S` of [R, Theorem 4.1] on each open arc with
one-sided limits at each `tau_j`; (T) (or (T_X), Section 8). Let
`ell = min_j (tau_{j+1} - tau_j) > 0` and `s_t := min_j |t_t - tau_j|`.
Then (P1)–(P7) of [W] hold with this `s_t`, and (P3) holds near each `tau_j`
with its own `kappa_j := b(x*(tau_j))^T w_j` ([W, Proposition 1.2] applies at
each switch: [R, Proposition 3.1] is local in time).

**Theorem A_k.** If all `kappa_j > 0`, there are `c_*, h_0 > 0` such that
for `e_h <= c_* sqrt h` and `h <= h_0` every stage is exact over `D_t x U`;
with (T), `B = J(zbar) = f*` with no window.

**Theorem B_k.** If all `kappa_j >= 0` and `e_h = O(h)`, then for small `h`:
near each switch with `kappa_j = 0` at most one stage `n_j` fails, at order
`h^3`; near each switch with `kappa_j > 0` none does; and for every fixed
`K >= K_0 = max_j K_0^{(j)}` the windows `W_j = {n_j - K, …, n_j + K}` are
exact. With (T), `B = f*` with at most one window of `2K + 1` stages per
`kappa_j = 0` switch.

**Theorem C_k.** If some `kappa_j < 0`, [W, Theorem C] holds at that switch
(for windows around it), whatever the other switches.

*Proof (by locality; sketch level, at the level of detail of [W]).*
(P1)–(P7) for several switches are taken from (SH_k) as stated above, and
the locality of each step (a)–(e) of [R, Theorem 4.1] is asserted, not
re-derived. Every step of [W]'s proofs is local: Lemma 0.2 is per stage; the
zones of Theorem A are taken around each `tau_j` with
`delta_2 <= ell / 3`, so they are disjoint, and the far zone uses the margin
(W5) on the compact set `{s_t >= delta_2}`; Theorem B(a)–(b) and the
pairing argument (c) use only the stages of one window and the state
recursion inside it; for small `h`, `(2K + 1) h < ell / 3`, so the windows
are disjoint and Lemma 0.1(3) applies to each; the bound sums the
contributions of stages, windows and the terminal term ([R, Definition 1.1]
allows several windows). Theorem C's move is inside one window. □

The constants (`c_*`, `h_0`, `K_0`, the zone radii) depend on `ell`, the
slopes `gamma_j = |sigma_dot(tau_j)|` and the margins, and no uniformity in
`ell` is claimed. For LQ data with `l_1` independent of `t`,
`kappa_j = -c^T b` is the same at every switch; different values need
time-dependent or nonlinear `l_1` or state-dependent `b`.

## 7. Close switches

**7.1 Degeneration.** If the data are `C^3` with bounded derivatives and two
consecutive switches are `ell` apart, then `sigma_dot` vanishes between
them (Rolle), so `gamma_j <= ell sup |sigma_ddot|` and `D_j = O(ell)`. The
hypotheses of Theorems A_k–B_k then hold with constants that degrade as
`ell -> 0` (the lower slope `gamma_1`, the zone radius `delta_sigma <= ell/2`
and the margin on the middle arc all shrink), so `h_0` shrinks with `ell`.
Two switches a bounded number of stages apart as `h -> 0` are not regular
switches of a fixed continuous problem (they merge into a double zero of
`sigma`); that regime is outside this note. One discrete remark: for two
`kappa = 0` switches whose windows overlap, the pairing argument in the
proof of [W, Theorem B] does not cover perturbations that move `u_{n_1}`
and `u_{n_2}` in opposite directions, because the state deviation is then
confined to the stages between `n_1` and `n_2`; the proof then needs about
`c K_0` stages between them. Whether such windows are nevertheless exact
was not determined.

**7.2 A coupling condition between consecutive switches.**

**Proposition 7.1 (necessary condition; `b` constant).** Let
`tau_1 < tau_2 = tau_1 + ell` be consecutive switches, `A_m = g_x` and
`H_xx` evaluated along the middle arc (control `u_m`), and let `P` be a
quadratic calibration ([E, Section 0]: `P` bounded, piecewise `C^1`, upward
jumps allowed) that satisfies (A) with margin `eps` on `(tau_1, tau_2)`,
tangency at both switches (`P(tau_j±) b = w_j`), and, after `tau_2`, the
conditions of [E, Proposition 4] (so that `P(tau_2+) <= M_2 :=
Qhat(tau_2+) - beta_2 beta_2^T / eta_2`, with `Qhat` the maximal solution
from the later arcs and `eta_2 > 0`). Let `X` solve the Lyapunov equation
`X_dot + A_m^T X + X A_m + H_xx = 2 eps I` on `(tau_1, tau_2)` with
`X(tau_2) = M_2`. Then

```
eta^X_1 := b^T X(tau_1+) b - kappa_1 >= 0,
eta^X_1 = kappa_2 - kappa_1 + ell [ b^T H_xx b + 2 w_2^T A_m b - 2 eps |b|^2 ] + O(ell^2).   (7.1)
```

*Proof.* `M_2 b = Qhat b - beta_2 (beta_2^T b) / eta_2 = Qhat b - beta_2 =
w_2`, so `b^T M_2 b = kappa_2`. By upward jumps `P(tau_2-) <= P(tau_2+) <=
M_2`. On the middle arc, `E := X - P` satisfies `E_dot + A_m^T E + E A_m =
2 eps I - M(t, u_m) <= 0` by (A), so backward Lyapunov comparison from
`E(tau_2-) >= 0` gives `E >= 0` ([E, Theorem 1, step 3]). Tangency at
`tau_1` gives `P(tau_1+) b = w_1`, so
`0 <= b^T E(tau_1+) b = b^T X(tau_1+) b - kappa_1`. Expansion:
`X(tau_1) = M_2 + int (A_m^T X + X A_m + H_xx - 2 eps I) dt`, and
`X b = w_2 + O(ell)` on the arc, so
`b^T (A_m^T X + X A_m) b = 2 w_2^T A_m b + O(ell)`. □

*Reading.* (7.1) is [E, Theorem 9]'s necessity step made quantitative for
two nearby switches. With smooth data, `kappa_2 - kappa_1 = ell b^T w_dot +
O(ell^2)`, and `b^T H_xx b + 2 w^T A b + b^T w_dot` is `b^T M b` for a tangent
`P` (`P b = w`), which [SA, Proposition 1.3] identifies with the Kelley-type
quantity `K = -partial_u sigma_ddot`. So

```
eta^X_1 = ell (K - 2 eps |b|^2) + O(ell^2)     (smooth data, b constant, l_1 affine),
```

and strict tangential calibrations at two merging switches need `K > 0`
at the merging point (a necessary condition; sufficiency would follow the
sketch of [E, Theorem 9] and is not proved). The relation to the
Osmolovskii–Maurer second-order condition for two switches was not worked
out. With data that are not smooth in time (or for a fixed `ell` not small),
`kappa_2 - kappa_1` enters at order 1. When `A_m = 0` and `H_xx` is constant
on the middle arc, `X(tau_1) = M_2 + ell (H_xx - 2 eps I)` exactly, so
`eta^X_1 = kappa_2 - kappa_1 + ell (b^T H_xx b - 2 eps |b|^2)` with no
remainder: **if `kappa_1 > kappa_2 + ell b^T H_xx b`, no tangential
calibration exists, even when both `kappa_j > 0`**, so Theorems A_k and B_k
do not apply; the obstruction is the
`eta_L < 0` layer of [E, Theorem 1] at `tau_1`, created by the later switch.

*Discrete counterpart (float, Section 9.3; revised after review).* For the
scalar two-switch toy with `k` jumping inside the middle arc (data not
smooth in time), the discrete maximal recursion ([E, Lemma 10], which
bounds every quadratic family exact over `R x U` on the later stages)
behaves in three ways on the tested grids (`N = 1000 … 16000`):

- strongly negative `eta^X_1` (-0.49 to -0.69): it breaks on every grid,
  between 2 stages before and 5 stages after the first switching stage; by
  [E, Corollary 11] every such family then fails at that stage, so a
  window (or lifting) must contain it, and lifting the broken stage six
  times in a row does not remove the break;
- moderately negative `eta^X_1` (-0.275): it breaks on some grids only
  (5 of 14), not monotonically in `h`; on these grids the breaks coincide
  with a small excess passed from the second switch into the middle arc
  (Section 9.3; an observation on 14 grids, not a tested criterion);
- slightly negative or positive `eta^X_1` (-0.085, -0.040, +0.160, and the
  convex rising-`kappa` configurations): no break up to `N = 16000`.

So the continuous condition `eta^X_1 >= 0` is necessary for a tangential
calibration (Proposition 7.1), but at the tested `h` its sign does not
predict the discrete recursion. The first version explained the moderate
case by the exponentially thin layer of [E, Section 2.5]. That explanation
is withdrawn: the layer law puts the blow-up at about `3e-6` times an
`O(1)` scale there, far below every tested `h`. For the strongly negative
cases, on grids where the second switch has a fractional stage, the break
lies a roughly constant time after the first switch at larger `N`
(`1.2e-4` to `9.7e-4` after the phase position `theta_1` of the first
switch, defined in Section 9.3; within a factor of 1.2, 1.7 and 1.6 per
configuration). This does not hold at `N = 1000`: there the second switch is
fractional for `(0.5, 1.5)` and `(0.45, 1.55)`, but the breaks lie `0` and
`-1.6e-3` from `theta_1` (0.8 stage before it; `logs/sweep.json`,
`break_time_minus_theta1`). The larger-`N` times are consistent with the layer law (blow-up
at the matching time times `exp(-2 gamma / (Delta |eta|))`) only if its
matching time, which was not determined, is between about 0.1 and 0.5,
a factor-5 range across the three configurations (about 0.30–0.35,
0.10–0.17 and 0.29–0.48). This is a consistency observation (order of
magnitude only), not a test or a fit of that law. No asymptotic claim is
made. (The numbers in this paragraph were corrected in round 3; the
round-2 values used a wrong `theta_1` formula, Section 15.)

## 8. Terminal rows

**(T_X).** Affine terminal rows `C x_N = c` (with discrete multiplier
`nu`, `p_N = grad Phi(xbar_N) + C^T nu`). Replace (T) by: `Phi - S^h_N`
restricted to `{C x = c} cap D_N` is minimized at `xbar_N`; for quadratic
`S`, `Z^T (Phi_xx - P_N) Z >= 0` with `Z` a basis of `ker C` (the slope
condition holds by the discrete KKT system).

**Proposition 8.1.** Under (SH_k) with (T) replaced by (T_X) and the rate
`e_h` assumed for the fixed-endpoint discrete KKT points, Theorems A_k,
B_k and C_k hold.

*Proof.* The stage conclusions never used (T) ([W, Theorem A, remarks]);
the bound's terminal term is the infimum over `X_N = {C x = c}`
([R, Definition 1.1], [R, Remark 1.4]); (T_X) makes it exact. □

*Status of the rate.* Osmolovskii–Veliov (2020) give `e_h = O(h)` for
free-endpoint Lagrange problems; fixed terminal components are outside
their setting ([R, Remark 2.5] already noted this for optcdeg2). So
Proposition 8.1 is conditional on the rate.

*optcdeg2* ([R, Section 5]). `b = e_v`, `l_1 = 0`, so `w = 0` and
`kappa_j = 0` at both switches (stages 3091 and 47290 of 50000, far apart);
terminal row `v_N = 0`; nonlinear drift; a state bound `v >= -1` (state
constraints are outside (SH); whether the bound is active along the optimum
is not settled here). So it is a `kappa = 0`,
two-switch, terminal-row instance of Theorem B_k, up to the unverified rate
and the (H3) hypotheses (a continuous tangential calibration with the
isotropic margin was not constructed; the certificate used a discrete
schedule). The theorem predicts at most one `h^3` failure per switch,
repairable by `O(1)` windows; the actual certificate needed none because
its curvature `q_t` vanishes exactly at both switching stages
(`b^T P_{n+1} b = 0`, remark after [W, Theorem B]).

**`kappa_tau < 0` with a terminal row.** Theorem C is unchanged: its window
move never reaches the terminal stage. A row frees `P_N` in the directions
off `ker C` (formally `P_N = +infinity` there). The maximal recursion then
starts from a curvature of order `1/h` near `T` (scalar toy:
`P_{N-1} = h + |sigma_{N-1}|/h - 2 k`), but its singular pushes bring it
back to `O(1)` within a fixed time (`P ~ 2|sigma| / (Delta (T - t))` in the
continuous analogue), so it is bounded on `[s + K', s + delta/h]` and the
harmonic-sum argument of [W, Proposition D] applies: the excess at the
switch still tends to 0 (sketch). Float check: Section 9.4.

## 9. Further numerical checks

All runs single-threaded, from `theory-bangbang/kneg/`. Two-switch toy
(`run_multi.py`): `x' = u`, `|u| <= 1`, `x(0) = 0`, `T = 2`, target `a = 4`
on `[0, t_1)`, `-4` on `[t_1, t_2)`, `4` on `[t_2, 2]`, `Phi = (x - 3)^2/2`,
box `|x| <= 4`, `k(t)` piecewise constant; the KKT points found have the
control `+1, -1, +1` with switches `tau_1 < tau_2` that move with
`(t_1, t_2)` and `k`. Switch
times were located on the `kappa`-free transcription (convex for constant
`k`, L-BFGS-B), then the KKT point by a phase scan and active-set Newton,
then exact rational KKT points.

*Data convention (revised after review).* The stage data are
`a_t = a(t h)`, `k_t = k(t h)` with `a(t) = a_i` on `[t_i, t_{i+1})`, the
jump times read as the decimals they denote (`t_i = 13/10`, not the binary
float nearest to 1.3). The first version of `ktoy.py` compared
`Fraction(float(t_i))` with `t h`. For `t_i` = 0.45, 0.55, 0.65, 1.3, 1.35,
1.55 the binary float is larger than `t_i`, so at grids with a stage at
`t h = t_i` exactly, that stage kept the old target value (one or two
stages per grid, for `(t_1, t_2)` = (0.65, 1.35), (0.7, 1.3), (0.55, 1.45),
(0.45, 1.55) at `N >= 1000`, and for (0.7, 1.3) also at `N = 500`; checked
against the documented rule for every `N` used). All Section 9 numbers below are from reruns with the exact
convention (`logs/two.json`, `kink.json`, `close.json`, `close2.json`,
`sweep.json`); the first-version logs are kept in `logs/pre_revision/`.
The jump of `k` in Section 9.3 is at a dyadic time and was never affected.

*Convexity of most instances (added after review).* For `x' = u`,
`x_0 = 0` and `k` piecewise constant with one jump at stage `m`, the
summation identity behind Proposition 2.1 gives exactly
`J = h sum_t (x_t - a_t)^2/2 + Phi(x_N) + (k_2/2) x_N^2 + ((k_1 - k_2)/2) x_m^2
+ (h^2/2) sum_t kappa_t u_t^2`. Float eigenvalues of the reduced Hessian at
`N = 1000` (`rev1_checks.py convexity`): positive definite for every
Section 9.1 instance with `kappa >= 0` (smallest eigenvalue `+0.50 h^2` for
`kappa = 0.5`, `+0.0005 h^2` for `kappa = 0`) and for every Section 9.3
configuration with rising `kappa` (`k_1 > k_2`); 979 negative eigenvalues
for `kappa = -0.5`; exactly one negative eigenvalue (the rank-one term
`((k_1 - k_2)/2) x_m^2`) for every falling-`kappa` configuration. Two
consequences make the results on the convex instances automatic:

- With `P = -k` and constant `k <= 0` (`kappa = -k >= 0`), every stage has
  `K_t = h`, `beta_t = 0` and `u`-curvature `kappa >= 0`, so the stage
  residual minus its value at `zbar_t` is
  `h sigma_t omega + h d^2/2 + (h^2/2) kappa omega^2 >= 0` at every KKT point
  (`sigma_t omega >= 0`), and `Phi_xx - P_N = 1 - kappa >= 0` (here
  `kappa <= 0.5`). The plain certificate is exact at every KKT point,
  whatever the separation.
- If the reduced Hessian `H` is positive definite, the discrete maximal
  recursion cannot break at any KKT point. Each step of the recursion is
  one dynamic-programming step of a tail problem ([E, Lemma 10],
  monotonicity proof) whose Hessian in the tail controls is the
  corresponding principal submatrix of `H` plus the nonnegative diagonal
  `h |sigma_s|`. That Hessian is positive definite, so the coefficient
  `h^2 m_t / 2` of `v_t^2` after minimizing over the later controls is
  positive (short proof, scalar toy).

So these instances test nothing about separation or locality; only the
nonconvex ones (`kappa < 0` in 9.1, falling `kappa` in 9.3) do.

**9.1 Two switches, same `kappa` (exact).** Tangential family `P = -k`
(`beta = 0` at every stage); `(T)` holds (`-k <= Phi_xx = 1`). Documented
instances (exact jump times; rerun after review, `logs/two.json`; the
certificates of the three `kappa = -0.5`, `N = 4000` rows were run in the
round-2 revision, `logs/rev2_two4000.json`).

| `kappa` | `(t_1, t_2)` | `ell` | `N` | switching stages | fractional (`u`) | plain gap `/h^2` | certificate |
|---|---|---|---|---|---|---|---|
| +0.5 | (0.5, 1.5) | 0.320 | 500 | [83, 162] | 162 (-0.152) | 0.0000 | exact, no window |
| +0.5 | (0.5, 1.5) | 0.320 | 1000 | [166, 325] | 166 (0.032), 325 (-0.616) | 0.0000 | exact, no window |
| +0.5 | (0.5, 1.5) | 0.320 | 2000 | [333, 652] | 333 (-0.408) | 0.0000 | exact, no window |
| +0.5 | (0.5, 1.5) | 0.320 | 4000 | [667, 1304] | 1304 (0.849) | 0.0000 | exact, no window |
| +0.5 | (0.6, 1.4) | 0.110 | 500 | [134, 161] | 134 (-0.711) | 0.0000 | exact, no window |
| +0.5 | (0.6, 1.4) | 0.110 | 1000 | [269, 323] | 269 (-0.965) | 0.0000 | exact, no window |
| +0.5 | (0.6, 1.4) | 0.110 | 2000 | [539, 647] | none | 0.0000 | exact, no window |
| +0.5 | (0.6, 1.4) | 0.110 | 4000 | [1078, 1294] | 1078 (-0.768), 1294 (0.695) | 0.0000 | exact, no window |
| 0 | (0.5, 1.5) | 0.420 | 500 | [71, 176] | none | 0.0000 | exact, no window |
| 0 | (0.5, 1.5) | 0.420 | 1000 | [142, 352] | 142 (0.595), 352 (-0.274) | 0.0000 | exact, no window |
| 0 | (0.5, 1.5) | 0.420 | 2000 | [285, 705] | 285 (0.690), 705 (-0.331) | 0.0000 | exact, no window |
| 0 | (0.5, 1.5) | 0.420 | 4000 | [571, 1411] | 571 (0.881), 1411 (-0.444) | 0.0000 | exact, no window |
| 0 | (0.6, 1.4) | 0.240 | 500 | [116, 177] | 116 (0.741) | 0.0000 | exact, no window |
| 0 | (0.6, 1.4) | 0.240 | 1000 | [234, 354] | 354 (-0.629) | 0.0000 | exact, no window |
| 0 | (0.6, 1.4) | 0.240 | 2000 | [468, 710] | 468 (-0.436) | 0.0000 | exact, no window |
| 0 | (0.6, 1.4) | 0.240 | 4000 | [937, 1420] | none | 0.0000 | exact, no window |
| 0 | (0.65, 1.35) | 0.150 | 500 | [141, 179] | 141 (-0.074) | 0.0000 | exact, no window |
| 0 | (0.65, 1.35) | 0.150 | 1000 | [282, 357] | 282 (0.153) | 0.0000 | exact, no window |
| 0 | (0.65, 1.35) | 0.150 | 2000 | [565, 715] | 565 (0.949) | 0.0000 | exact, no window |
| 0 | (0.65, 1.35) | 0.150 | 4000 | [1132, 1430] | 1430 (0.188) | 0.0000 | exact, no window |
| 0 | (0.7, 1.3) | 0.055 | 500 | [166, 180] | 166 (0.292) | 0.0000 | exact, no window |
| 0 | (0.7, 1.3) | 0.055 | 1000 | [334, 361] | none | 0.0000 | exact, no window |
| 0 | (0.7, 1.3) | 0.055 | 2000 | [668, 722] | 722 (0.964) | 0.0000 | exact, no window |
| 0 | (0.7, 1.3) | 0.055 | 4000 | [1336, 1445] | 1336 (-0.168) | 0.0000 | exact, no window |
| -0.5 | (0.5, 1.5) | 0.495 | 500 | [62, 186] | 62 (-0.706) | 0.7276 (62: 0.7276) | exact, 5 nodes (4 leaves) |
| -0.5 | (0.5, 1.5) | 0.495 | 1000 | [125, 373] | 125 (-0.729) | 0.7470 (125: 0.7470) | exact, 3 nodes (3 leaves) |
| -0.5 | (0.5, 1.5) | 0.495 | 2000 | [251, 747] | 251 (-0.774) | 0.7865 (251: 0.7865) | exact, 3 nodes (3 leaves) |
| -0.5 | (0.5, 1.5) | 0.495 | 4000 | [503, 1495] | 503 (-0.864) | 0.8685 (503: 0.8685) | exact, 3 nodes (3 leaves; round 2) |
| -0.5 | (0.7, 1.3) | 0.180 | 500 | [149, 194] | none | 0.0000 | exact, no window |
| -0.5 | (0.7, 1.3) | 0.180 | 1000 | [299, 389] | none | 0.0000 | exact, no window |
| -0.5 | (0.7, 1.3) | 0.180 | 2000 | [598, 778] | none | 1.5320 (597: 0.7140; 778: 0.8180) | exact, 9 nodes (5 leaves) |
| -0.5 | (0.7, 1.3) | 0.180 | 4000 | [1196, 1557] | 1196 (-0.873) | 0.8766 (1196: 0.8766) | exact, 3 nodes (3 leaves; round 2) |
| -0.5 | (0.75, 1.25) | 0.095 | 500 | [173, 198] | 173 (0.087) | 0.2953 (173: 0.2953) | exact, 3 nodes (3 leaves) |
| -0.5 | (0.75, 1.25) | 0.095 | 1000 | [346, 395] | 346 (0.234) | 0.3808 (346: 0.3808) | exact, 3 nodes (3 leaves) |
| -0.5 | (0.75, 1.25) | 0.095 | 2000 | [693, 790] | 693 (-0.990) | 0.9901 (693: 0.9901) | exact, 3 nodes (3 leaves) |
| -0.5 | (0.75, 1.25) | 0.095 | 4000 | [1387, 1580] | 1580 (-0.873) | 0.8769 (1580: 0.8769) | exact, 3 nodes (3 leaves; round 2) |

- `kappa = +0.5` and `kappa = 0` (24 grids, separations `ell` = 0.055–0.42):
  the plain certificate is exact (gap exactly 0, no window), including grids
  with fractional stages at both switches. These problems are convex and
  the family `P = -k` is exact at every KKT point (see the convexity
  paragraph above), so these rows are automatic: they are consistent with
  Theorems A_k and B_k but test nothing about separation or locality. (For
  `kappa = 0` the family has `b^T P_{n+1} b = 0` exactly, so not even the
  `h^3` failure of Theorem B occurs.)
- `kappa = -0.5` (nonconvex): at 10 of the 12 grids one or two stages fail
  for the plain certificate, at one or both switches (Theorem C_k), with
  plain gaps 0.30–1.53 `h^2`. At `(0.7, 1.3)`, `N = 500, 1000`, the KKT
  point is bang-bang with enough vertex margin and the plain certificate
  is exact. The box branch and bound (`certify_multi`: lifted nodes on the
  failing stage, ordinary nodes elsewhere, splits when neither suffices)
  gives exact certificates of `f* = J(zbar)` with 3–9 nodes on all ten
  grids with a failing stage (`N = 500 … 4000`). At `(0.7, 1.3)`,
  `N = 2000`, the KKT point is bang-bang with two small-margin vertex
  stages (597 and 778); the certificate needs 9 nodes (5 leaves) and finds
  no better point. This reproduces the review's independent result for this
  instance (switching stages 598 and 778, plain gap 1.532 `h^2`, 9 nodes).
  At `N = 4000` the first revision did not run the certificate, although
  its status table claimed `f* = J(zbar)` there, which the evidence did not
  then support (Section 14). The round-2 run (`rev2_checks.py two4000`, same settings as
  `run_multi.py two`) certifies all three `N = 4000` grids exactly: in each
  case one lifted node on the fractional stage and two ordinary outer
  nodes, no better point found, about 80 s per grid.

*Earlier instance, kept as a negative result.* With the first-version data
convention, `(t_1, t_2) = (0.7, 1.3)` had the target jump at `t_2` one
stage late (stage `0.65 N`). On that instance at `N = 2000`
(`logs/pre_revision/two.json`), our KKT search returned a point with a
fractional stage at the second switch (778, `u = -0.111`) and a
small-margin vertex at the first (plain gap 1.247 `h^2`). A node anchor was
`0.30991158604134855 h^2` better: fractional stage 597 at the first switch
(`u = -0.0054`), second switch at a vertex. With incumbent updates the
certificate proved that point globally optimal, with 13 nodes (8 leaves;
splits on both switching controls and one two-stage lifted box). The
review reproduced this value exactly on that instance and certified the
same optimum with its own branch and bound (7 nodes). So a local KKT
search can return a non-optimal KKT point when several phase combinations
of two switches compete; on the documented instances this did not happen
on any of the 36 grids. On that earlier instance the rows `(0.7, 1.3)`,
`N = 500, 1000, 4000` also differed (plain gaps 0.752, 0.500, 0.616
`h^2`; exact certificates with 2 nodes at `N = 500, 1000`).

**9.2 Two switches, `kappa = 0`, a family with `h^3` failures (exact).**

`k = 0`; family `P(t) = 0` before `tau_1`, `-0.3 dist(t, {tau_1, tau_2})`
between the switches and `-0.3 (t - tau_2)` after (tangential at both
switches, `b^T P_{n+1} b < 0` after them). The switch times `tau_j` are the
phase positions of the KKT point at `N = 16000` (error `O(1e-4)`, about one
stage at `N = 4000`; the misplacement enters the `h^3` constant, which is
why it varies with `N`). Window minima `{n - K, …, n + K}` over the state box
and `U`, exact.

| `(t_1, t_2)` | `ell` | `N` | fractional | failing stages (loss `/h^3`) | window deficits `/h^3`, `K = 0, 1, 2` |
|---|---|---|---|---|---|
| (0.5, 1.5) | 0.420 | 1000 | [142, 352] | 352: 0.0069 | 352: 0.00692, 0, 0 |
| (0.5, 1.5) | 0.420 | 2000 | [285, 705] | 705: 0.0152 | 705: 0.0152, 0, 0 |
| (0.5, 1.5) | 0.420 | 4000 | [571, 1411] | 1411: 0.0363 | 1411: 0.0363, 0, 0 |
| (0.6, 1.4) | 0.240 | 1000 | [354] | 354: 0.0512 | 354: 0.0512, 0, 0 |
| (0.6, 1.4) | 0.240 | 2000 | [468] | 468: 0.1307 | 468: 0.131, 0, 0 |
| (0.6, 1.4) | 0.240 | 4000 | [] | none | — |
| (0.65, 1.35) | 0.150 | 1000 | [282] | none | — |
| (0.65, 1.35) | 0.150 | 2000 | [565] | none | — |
| (0.65, 1.35) | 0.150 | 4000 | [1430] | 1430: 0.0536 | 1430: 0.0536, 0, 0 |
| (0.7, 1.3) | 0.055 | 1000 | [] | none | — |
| (0.7, 1.3) | 0.055 | 2000 | [722] | 722: 0.1541 | 722: 0.154, 0, 0 |
| (0.7, 1.3) | 0.055 | 4000 | [1336] | 1336: 0.0422 | 1336: 0.0422, 0, 0 |

(Documented instances, rerun after review, `logs/kink.json`. The rows
`(0.5, 1.5)` and `(0.6, 1.4)` are unchanged; the six rows `(0.65, 1.35)`
and `(0.7, 1.3)` replace those of the first-version data convention, which
had failing-stage losses 1.0048, 0.3644, 0.2644, 0.1549 `h^3` at other
stages; the review reproduced 1.0048 and 0.2644 on that instance.)

At most one stage fails per grid, at order `h^3`, and the window with one
stage on each side has minimum exactly 0 at every failing stage, for
separations `ell` from 0.055 to 0.42: as Theorem B_k says, with `K_0 = 1`
here. This problem is convex (`kappa = 0`, Section 9 convexity paragraph),
but the family is deliberately not the exact one, so the check is still a
test of the window statement, not of nonconvexity.

**9.3 Close switches with different `kappa` (float; revised after review).**
`k(t) = k_1` before the dyadic midpoint `t_k` of the middle arc and `k_2`
after; Proposition 7.1 predicts `eta^X_1 = kappa_2 - kappa_1 + ell`
(`eps = 0`; exact here since `A = 0`, `H_xx = 1`). The jump of `k` at
`t_k`, away from the switches, is data that are not smooth in time: it is
outside the `C^3` hypothesis (H1), as the targets' jumps already are, and
it is what allows an `O(1)` drop of `kappa` across a short arc. Discrete
maximal recursion ([E, Lemma 10], `eps = 0`) from `P_N = Phi_xx`; "no
break" means that it does not break, and then every stage is exact over
`R x U` (float stage losses over the boxes `<= 7.2e-16`). Documented
instances (`logs/close.json`, `close2.json`; rerun after review):

| `kappa_1 -> kappa_2` | `(t_1, t_2)` | `ell` | predicted `eta^X_1` | `N` = 1000 | 2000 | 4000 | 8000 |
|---|---|---|---|---|---|---|---|
| +0.5 -> +0.0 | (0.5, 1.5) | 0.415 | -0.085 | no break | no break | no break | no break |
| +0.5 -> +0.0 | (0.6, 1.4) | 0.225 | -0.275 | no break | no break | break at `s_1-14` | break at `s_1-18` |
| +0.0 -> +0.5 | (0.5, 1.5) | 0.325 | +0.825 | no break | no break | no break | no break |
| +0.0 -> +0.5 | (0.6, 1.4) | 0.130 | +0.630 | no break | no break | no break | no break |
| +0.0 -> +0.5 | (0.65, 1.35) | 0.035 | +0.535 | no break | no break | no break | no break |
| +0.5 -> +0.3 | (0.5, 1.5) | 0.360 | +0.160 | no break | no break | no break | no break |
| +0.5 -> +0.3 | (0.6, 1.4) | 0.160 | -0.040 | no break | no break | no break | no break |
| +0.3 -> +0.5 | (0.5, 1.5) | 0.320 | +0.520 | no break | no break | no break | no break |
| +0.3 -> +0.5 | (0.6, 1.4) | 0.115 | +0.315 | no break | no break | no break | no break |
| +0.3 -> +0.5 | (0.65, 1.35) | 0.015 | +0.215 | no break | no break | no break | no break |
| +1.0 -> +0.0 | (0.5, 1.5) | 0.410 | -0.590 | break at `s_1+0` | break at `s_1+0` | break at `s_1+0` | break at `s_1+0` |
| +1.0 -> +0.0 | (0.55, 1.45) | 0.310 | -0.690 | break at `s_1-1` | break at `s_1+0` | break at `s_1+2` | break at `s_1+1` |
| +1.0 -> +0.0 | (0.45, 1.55) | 0.510 | -0.490 | break at `s_1+0` | break at `s_1+0` | break at `s_1-1` | break at `s_1-1` |
| +0.0 -> +1.0 | (0.5, 1.5) | 0.200 | +1.200 | no break | no break | no break | no break |
| +0.0 -> +1.0 | (0.55, 1.45) | 0.095 | +1.095 | no break | no break | no break | no break |
| +0.0 -> +1.0 | (0.45, 1.55) | 0.310 | +1.310 | no break | no break | no break | no break |

(`s_1` = first switching stage of the KKT point; two configurations whose
constant-`k` base problem had no two-switch structure were skipped. Against
the first-version data convention, only the configurations at
`(0.55, 1.45)` and `(0.45, 1.55)` changed: in three table rows `ell`,
`eta^X_1` and the break offsets moved slightly, and in the fourth
(`+0.0 -> +1.0` at `(0.45, 1.55)`) only the fractional stages of the KKT
points; no break appeared or disappeared.)

*Convexity.* The nine rising-`kappa` configurations (`k_1 > k_2`) are
convex problems (Section 9, convexity paragraph), so their "no break" is
automatic. Among the ten configurations with `eta^X_1 > 0`, only
`+0.5 -> +0.3` at `(0.5, 1.5)` (`eta^X_1 = +0.16`) is nonconvex (one
negative eigenvalue). All falling-`kappa` configurations are nonconvex.
So the separations down to `ell = 0.015` in rising configurations test
nothing; the informative rows are the falling ones.

*`N`-sweep of the falling configurations (added after review;
`run_multi.py sweep`, `logs/sweep.json`).* Break position in stages from
`s_1` ("—": no break; "n/f": the KKT search returned no point, a gap in the
data):

| `kappa_1 -> kappa_2` | `(t_1, t_2)` | `eta^X_1` | 1000 | 1500 | 2000 | 2500 | 3000 | 3500 | 4000 | 5000 | 6000 | 7000 | 8000 | 10000 | 12000 | 16000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| +0.5 -> +0.0 | (0.5, 1.5) | -0.085 | — | — | — | — | — | — | — | — | — | n/f | — | — | — | — |
| +0.5 -> +0.0 | (0.6, 1.4) | -0.275 | — | — | — | — | -4 | +0 | -14 | — | — | -7 | -18 | — | — | — |
| +0.5 -> +0.3 | (0.5, 1.5) | +0.160 | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| +0.5 -> +0.3 | (0.6, 1.4) | -0.040 | — | — | — | — | — | — | — | — | — | — | — | — | — | — |
| +1.0 -> +0.0 | (0.5, 1.5) | -0.590 | +0 | +0 | +0 | +0 | +0 | +1 | +0 | +0 | +2 | +0 | +0 | +3 | +1 | +5 |
| +1.0 -> +0.0 | (0.55, 1.45) | -0.690 | -1 | +0 | +0 | +1 | +0 | +1 | +2 | +2 | +3 | +1 | +1 | +1 | +2 | +2 |
| +1.0 -> +0.0 | (0.45, 1.55) | -0.490 | +0 | -1 | +0 | -1 | -2 | +0 | -1 | +0 | +1 | +0 | -1 | +1 | +0 | +0 |

This reproduces the review's sweep for `eta^X_1 = -0.275` grid by grid and
its break offsets for `eta^X_1 = -0.59`. Two quantities of the recursion
were recorded to describe the moderate case: the excess carried into the
middle arc from the second switch,
`e_2 = P_{m_k} - kappa_2 - (s_2 - m_k) h` (`m_k` the first stage with
`k = k_2`, `s_2` the second switching stage), and the excess just after the
first switch, `eta_hat_1 = P_{s_1 + 1} - kappa_1`. For
`eta^X_1 = -0.275`, `(0.6, 1.4)`:

| `N` | 1000 | 1500 | 2000 | 2500 | 3000 | 3500 | 4000 | 5000 | 6000 | 7000 | 8000 | 10000 | 12000 | 16000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| second switch | v | v | v | v | f | f | f | v | v | f | v | v | v | v |
| `e_2` | +0.261 | +0.245 | +0.222 | +0.213 | -0.001 | -0.001 | -0.002 | +0.214 | +0.176 | -0.002 | +0.079 | +0.190 | +0.193 | +0.186 |
| `eta_hat_1` | -0.018 | -0.034 | -0.063 | -0.073 | -0.513 | -0.551 | -0.502 | -0.073 | -0.127 | -0.545 | -0.337 | -0.110 | -0.105 | -0.114 |
| break − `s_1` | — | — | — | — | -4 | +0 | -14 | — | — | -7 | -18 | — | — | — |

(v: the second switch is at a vertex; f: it has a fractional stage.)
Observations (float, these grids only):

- **Strongly negative `eta^X_1` (-0.49 to -0.69): robust break.** The
  recursion breaks on all 42 grids `N = 1000 … 16000`, between 2 stages
  before and 5 stages after `s_1`. The statement "within two stages" of the
  first version held only on its 12 grids. On grids where the second switch
  has a fractional stage (`e_2 ≈ 0`), the break lies a roughly constant
  time after the first switch at larger `N`: `5.7e-4 … 6.7e-4` for
  `(0.5, 1.5)` (`N = 3500, 6000, 10000, 16000`), `5.7e-4 … 9.7e-4` for
  `(0.55, 1.45)` (`N = 2500, 3500, 4000, 5000, 6000`), `1.2e-4 … 2.0e-4`
  for `(0.45, 1.55)` (`N = 6000, 10000`); at `N = 1000` the second switch
  is also fractional
  for `(0.5, 1.5)` and `(0.45, 1.55)`, and the breaks lie `0` and
  `-1.6e-3` from `theta_1` (0.8 stage before it). Here `theta_1` is the
  phase position of the first switch in the phase model of
  [W, Remark 1.4]: the control goes from `+1` to `-1`, so
  `theta_1 = t_{s_1} + h (1 + u_{s_1}) / 2` if stage `s_1` is fractional
  and `theta_1 = t_{s_1}` if it is a vertex (`logs/sweep.json`,
  `break_time_minus_theta1`; numbers corrected in round 3, Section 15).
  The larger-`N` behaviour resembles that of a
  resolved layer. The leading-order law of [E, Section 2.5],
  `s_b = s_1 exp(-2 gamma / (Delta |eta|))` with `gamma = a - x(tau_1)`
  (3.70, 3.58, 3.81) and `Delta = 2`, gives `s_b / s_1 = 1.9e-3, 5.6e-3,
  4.2e-4`; the observed times match if the matching scale `s_1` of that
  law ([E]'s matching time, not the switching stage `s_1` of the tables)
  is 0.1–0.5, which was not determined (order of magnitude only, not a
  fit). On grids where the second switch is at a vertex, `e_2 > 0`
  reduces the incoming excess, and the break moves to within a stage or two
  of `s_1`.
- **Moderately negative `eta^X_1` (-0.275): grid-dependent breaks.** The
  recursion breaks at 5 of the 14 grids (`N = 3000, 3500, 4000, 7000,
  8000`), not monotonically in `h`, and does not break at `N = 1000 …
  2500, 5000, 6000, 10000, 12000, 16000`. On these 14 grids the breaks
  coincide with a small `e_2`: the five breaking grids have `e_2 <= 0.079`
  (four have a fractional stage at the second switch and `e_2 ≈ 0`; at
  `N = 8000` the second switch is a vertex and `e_2 = 0.079`), and there
  `eta_hat_1 <= -0.33` (`-0.337` at `N = 8000`, `-0.50` to `-0.55` on the
  other four). On the nine grids without a break `e_2 >= 0.176`, the
  carried-in excess offsets most of `eta^X_1`, and `eta_hat_1 >= -0.127`.
  The separation between `e_2 = 0.079` and `0.176` was read off these 14
  grids after the fact; it is not a predicted or tested threshold, and the
  only breaking grid with a vertex second switch lies just below it. The
  layer law puts the continuous blow-up at
  `s_b / s_1 = exp(-3.5/0.275) ≈ 3e-6`, far below every tested `h`
  (`>= 1.25e-4`). So these breaks are not the thin layer: the layer is not
  resolved on any tested grid. **The first version's statement that this
  case "breaks only from `N = 4000` on, as a thin layer would" is wrong
  and is withdrawn**; it rested on the four grids 1000, 2000, 4000, 8000.
- **Slightly negative or positive `eta^X_1` (-0.085, -0.040, +0.160): no
  break** on any tested grid up to `N = 16000` (one KKT search failure, at
  `N = 7000` for -0.085). For -0.085, even with `e_2 ≈ 0` the excess after
  the first switch is only `-0.13`. For -0.040 (`kappa_2 = 0.3`) a
  fractional second switch does not remove the excess (`e_2 >= 0.13` on
  every grid).

So, at the tested `h`, the sign of `eta^X_1` does **not** predict the
behaviour of the discrete recursion: two configurations with
`eta^X_1 < 0` never break, and the moderate one breaks on some grids only.
The first version's sentence "the sign of `eta^X_1` predicts the
behaviour of the discrete recursion at small `h`" is withdrawn. We make
no asymptotic claim.

*Heuristic reading (not tested; labelled as such).* `e_2` is the excess
that the recursion keeps after the second switch. By the harmonic-sum
argument of [W, Proposition D] it should tend to 0 like
`(log(1/h))^{-1/2}`; on vertex grids it decreases only slowly here (0.26
at `N = 1000`, 0.19 at `N = 16000` for `(0.6, 1.4)`). With `kappa_2 = 0`, a
fractional stage at the second switch removes it at once (the recursion
returns `P_t = h` there). Near a switch the recursion in stage units is
nearly independent of `h` and depends on the phase of the switch. So for
`eta^X_1 = -0.275`, the fraction of breaking grids may change slowly with
`h` until `h` reaches the layer scale (`~1e-6` here). The tested grids say
nothing about the limit.

*Lifting cascade (logged in revision; `rev1_checks.py cascade`,
`logs/rev1_cascade.json`).* For the three `kappa = 1 -> 0` configurations at
`N = 1000, 2000, 4000, 8000`, treating the broken stage's control as a
parameter and rerunning the recursion, six times in a row: the recursion
still breaks after six lifted stages on all 12 grids. Each lifting moves
the break 1–4 stages earlier, except one move of 33 stages
(`(0.45, 1.55)`, `N = 2000`). So a single lifted stage does not suffice; how
large the repair must be as `h -> 0` was not determined. No exact
certificate was attempted for the configurations that break.

**9.4 Terminal row (toy plus data, `x_N` fixed).**

Toy plus data with `k = -0.5, 0, 0.5` and the row `x_N = -63/64` instead of
`Phi`; the row pins the switch at `t = 0.5078125`, so every grid has one
fractional stage. "Free end": the toy with `Phi = x` and the same `k`
(`kappa = -0.5`: [W]'s toy plus, whose `eta_hat_1` values these reproduce);
"—": no fractional stage on that grid. Plain gaps exact (`N <= 4000`),
recursions float.

| `kappa` | `N` | fractional (`u`) | plain gap `/h^2` (exact) | `eta_hat_1`, row (`P_N = +inf`) | `eta_hat_1`, free end | recursion break, row / free |
|---|---|---|---|---|---|---|
| +0.5 | 500 | 126 (0.906) | 0.0000 | 0.2472 | — | none / — |
| +0.5 | 1000 | 253 (0.812) | 0.0000 | 0.2243 | 0.2768 | none / none |
| +0.5 | 2000 | 507 (0.625) | 0.0000 | 0.2074 | 0.2552 | none / none |
| +0.5 | 4000 | 1015 (0.250) | 0.0000 | 0.1956 | — | none / — |
| +0.5 | 8000 | 2031 (-0.500) | — | 0.1881 | 0.2107 | none / none |
| +0.5 | 16000 | 4062 (0.000) | — | 0.1683 | 0.1988 | none / none |
| 0 | 500 | 126 (0.906) | 0.0000 | 0.2751 | 0.2938 | none / none |
| 0 | 1000 | 253 (0.812) | 0.0000 | 0.2443 | 0.2615 | none / none |
| 0 | 2000 | 507 (0.625) | 0.0000 | 0.2196 | 0.2354 | none / none |
| 0 | 4000 | 1015 (0.250) | 0.0000 | 0.1994 | 0.2140 | none / none |
| 0 | 8000 | 2031 (-0.500) | — | 0.1825 | 0.1962 | none / none |
| 0 | 16000 | 4062 (0.000) | — | 0.1683 | 0.1812 | none / none |
| -0.5 | 500 | 126 (0.906) | 0.9084 | 0.2959 | — | 126 / — |
| -0.5 | 1000 | 253 (0.812) | 0.8213 | 0.2596 | 0.2421 | 253 / 238 |
| -0.5 | 2000 | 507 (0.625) | 0.6602 | 0.2295 | — | 507 / — |
| -0.5 | 4000 | 1015 (0.250) | 0.3906 | 0.2029 | 0.2046 | 1015 / 954 |
| -0.5 | 8000 | 2031 (-0.500) | — | 0.1758 | 0.1790 | 2031 / 1909 |
| -0.5 | 16000 | 4062 (0.000) | — | 0.1683 | — | 4062 / — |

- `kappa = +0.5` and `0`: the tangential family `P = -k` gives an exact
  certificate (gap exactly 0) at every exact grid; the terminal term is
  trivial (`X_N` is a point). Consistent with Proposition 8.1, but automatic:
  for `k <= 0` these problems are convex and `P = -k` is exact at every KKT
  point, as in Section 9 (convexity paragraph; added in revision).
- `kappa = -0.5`: the plain gap is exactly `(h^2/2)|kappa_tau| omega_hat^2`
  (for example `0.25 (1.90625)^2 = 0.9084` at `N = 500`): Theorem C does not
  see the row. The maximal recursion started from `P_N = +infinity` breaks
  at the fractional stage at every `N`; its excess `eta_hat_1` decays from
  0.30 to 0.17 over `N = 500 … 16000` and stays within 10% of the free-end
  values where both exist. So the row does not rescue `kappa_tau < 0`, as
  the sketch in Section 8 says. (At `N = 16000` the fractional control is
  exactly 0, so by Proposition 2.1 the three values of `k` give the same
  KKT point up to the multiplier and the same `eta_hat_1`.)
- A lifted certificate was not tried with the row: with all other controls
  fixed, the row pins `u_n`, so the lifting must move a second control.

## 10. Status

| item | status |
|---|---|
| Proposition 2.1 (`kappa`-split identity) | proved (exact algebra); residual exactly 0 on four examples |
| Corollary 2.2 (vertex sequences; `kappa = 0` lower bound) | proved |
| Remark 2.3 (`alpha`BB reading; convexification gap; `min Jt'` via [W, Theorem B]) | remark; the gap comparison with the window deficit is a leading-order estimate (one coordinate); applying [W, Theorem B] to `Jt'` is plausible, not checked (stage cost quadratic in `u`); the phase-model fraction is heuristic, not tested |
| convexity of `Jt` (toy yes, [E]'s examples no) | float eigenvalues; toy `lambda_min(G) ≈ h^3/4` (40 digits, relative excess `≈ 2.47/N^2`) |
| Lemma 3.1 (no two nearby fractional stages) | proved, LQ data |
| Proposition 3.2 (pair flips cost `h^2 D (j - i)`) | proved up to the stated remainders, LQ data, `e_h = O(h)` |
| "no chattering at leading order"; `zbar` optimal when `q > 0` | leading-order argument; exact certificates on all tested single-switch grids |
| `q < 0`: fractional KKT points near the switch are saddles | proved (`H_nn < 0`); minimizers near the reference trajectory are bang-bang (every minimizer for the toy, all `H_tt < 0`); exact certificates of the bang-bang optimum at 4 grids |
| Theorem 4.1 (upper bound on node bounds) | proved, LQ data, any anchor |
| Corollary 4.2 (no finite exact `kappa`-limited certificate) | proved for a fractional stage; at small-margin vertex stages finite exact certificates can exist (remark after it) |
| Theorem 4.3 (`Theta(log(h^2/epsilon))` nodes) | leading order; lower bound only for `kappa`-limited families with the node optimum's costate as exit slope; the log count is generic for second-order bounds in 1-D (Wechsung et al. 2014), the ratio `rho*` and `epsilon = 0` impossibility are specific; counts match predictions on the toys (float screening, some margins below `-epsilon` by rounding; two exact re-checks with full cover) |
| Lemmas 5.1–5.2, Theorem 5.3 (lifted certificate) | proved, LQ data |
| Theorem 5.4 (central node exact for small `h`) | proved under (SH), LQ, (VM), `e_h = o(sqrt h)`, (T) |
| Remark 5.5 (bounded number of outer nodes; hence `O(N)` certificate size) | heuristic; 1–2 outer nodes on the single-switch toys, 3–9 nodes in total on the two-switch toys (exact; 13 on the earlier instance of Section 9.1) |
| exact certificates of `f*` on toys | exact rational arithmetic (Sections 5.3, 9.1); `f* = J(zbar)` on every single-switch grid of Section 5.3 and on all 36 documented two-switch grids of Section 9.1 (`kappa >= 0`: plain certificate exact; `kappa = -0.5`: branch and bound, at `N = 4000` run only in the round-2 revision, before which this row overstated the evidence); on one grid of an earlier, one-stage-different instance the optimum was a different (monotone) KKT point than the one our search returned |
| A− lifted certificate | float screening; zero loss checked at finitely many `v` (the zero-loss set is not shown to be an interval with `beta != 0` over boxes) |
| Theorems A_k, B_k, C_k | proof by locality at the level of detail of [W] (sketch level: (P1)–(P7) taken from (SH_k), locality of [R, Theorem 4.1] asserted); constants depend on `ell`, no uniformity in `ell`; the two-switch toys with `kappa >= 0` are convex, so their exact certificates are automatic |
| Section 7.1 (degeneration, overlapping windows) | remarks; the overlapping-window statement is a sketch |
| Proposition 7.1 (coupling condition) | proved (necessity); expansion to `O(ell^2)`; exact form without remainder when `A = 0` and `H_xx` constant; Kelley reading uses [SA, Proposition 1.3]; sufficiency not proved |
| discrete maximal recursion at close switches (Section 9.3) | float; strongly negative `eta^X_1`: breaks on every grid up to `N = 16000`; moderately negative: grid-dependent breaks (5 of 14 grids), observed to coincide with a small excess `e_2` carried in from the second switch (separation read off the 14 grids after the fact, not tested); slightly negative or positive: no break up to `N = 16000`; no asymptotic claim; the thin-layer reading of the first version is withdrawn; 9 of the 10 positive-`eta^X_1` configurations are convex |
| Proposition 8.1 (terminal rows) | proved, conditional on the rate `e_h` for fixed endpoints |
| Proposition D with a terminal row | sketch; float check |

## 11. Literature and novelty

Examined (local folder `literature/` and openly accessible pages; papers not
read in full unless stated):

- C. S. Adjiman, S. Dallwig, C. A. Floudas, A. Neumaier, *A global
  optimization method, alphaBB, for general twice-differentiable
  constrained NLPs — I. Theoretical advances*, Comput. Chem. Eng. 22 (1998)
  1137–1158, and part II (Adjiman, Androulakis, Floudas), 1159–1179 (local
  `literature/papers/adjiman1998-*`, summaries read). Corollary 2.2(b) is an
  `alpha`BB underestimator with an exactly known `alpha`.
- K. Du, R. B. Kearfott, *The cluster problem in multivariate global
  optimization*, J. Global Optim. 5 (1994); R. Kannan, P. I. Barton, *The
  cluster problem in constrained global optimization*, J. Global Optim. 69
  (2017) 629–676 (local copies; the Kannan–Barton abstract and
  introduction read).
- A. Wechsung, S. D. Schaber, P. I. Barton, *The cluster problem
  revisited*, J. Global Optim. 58 (2014) 429–438,
  DOI 10.1007/s10898-013-0059-9 (local copy
  `literature/papers/wechsung2014-the-cluster-problem-revisited`; abstract,
  Sections 1–3, Theorem 2 and the conclusion read in revision; cited in
  [W] but missing from the first version of this note). For relaxations
  with second-order convergence, the number of boxes in the cluster around
  an unconstrained minimizer does not depend on `epsilon`, and it is 1 when
  the prefactor is at most `lambda_1/8`. In one dimension, a
  `Theta(log(1/epsilon))` node count is then the generic cost of covering a
  fixed range geometrically, not a cluster blow-up. So the logarithmic count
  of Theorem 4.3 is not new; the first version's framing of it as an
  instance of the cluster problem overstated the link and is withdrawn
  (Section 4, remarks). What is specific to this note: that `epsilon = 0`
  is impossible with finitely many `kappa`-limited calibration nodes
  (Corollary 4.2), the explicit ratio `rho*` (which includes the
  first-order term of the anchored bound), and the lifted bound that removes
  the obstruction.
- L. Poggiolini, M. Spadini, *Bang–bang trajectories with a double
  switching time: sufficient strong local optimality conditions*
  (arXiv:1010.1149), and L. Poggiolini, *Structural stability of bang–bang
  trajectories with a double switching time in the minimum time problem*
  (arXiv:1607.05564) (arXiv abstract pages and search-result snippets
  only). There a "double switch" is two control components switching at
  the same time; per the search snippets, a small perturbation generically
  splits it into two simple switches with a short bang arc between them,
  the multi-input analogue of Section 7's close switches. Not used beyond
  this pointer.
- Osmolovskii–Veliov (2020) and the second-order theory as cited in [W];
  the Kelley quantity as in [SA].
- Search on global optimality certificates for discretized bang-bang
  problems: found work on mixed-integer optimal control certificates
  (Sager and coauthors; convex MINLP certificates), none on calibration
  certificates for Euler transcriptions.

Novelty (qualified; four web searches, two arXiv abstract pages and the
local index, not exhaustive): we did not find the `kappa`-split identity stated as such
(its content is the elementary diagonal-deficit computation of the reduced
Hessian, and the toy case was the reviewer's), the lifted calibration for
bang-bang transcriptions, the ratio `rho*` of the node-count estimate
(the logarithmic count itself is generic, Wechsung et al. 2014),
or the coupling condition (7.1). All are elementary. An unsuccessful search
does not establish novelty. The lifted
certificate is, in branch-and-bound terms, a parametric (continuum of
nodes) bound; parametric bounding is standard in global optimization, and
the claim here is only its use with calibrations to obtain exact
certificates.

## 12. Commands run and files

Scripts (`theory-bangbang/kneg/`):

- `ktoy.py` — general scalar toy (piecewise-constant target and `k`,
  optional terminal row), KKT search (phase scan plus active-set Newton,
  node bounds), exact rational KKT points, exact stage/terminal losses,
  window problems, discrete maximal recursion (also from
  `P_N = +infinity`). Revised after review: jump times are read as the
  decimals they denote (`_exact_time`), see Section 9.
- `lifted.py` — node bounds with fixed families, lifted interval
  (closed form for `beta = 0`), one-control and box branch and bound
  (`certify`, `certify_multi`, the latter with incumbent updates and
  multi-stage lifting), float greedy `epsilon`-partitions with
  backtracking.
- `run_kneg.py` — parts `lifted lifted2 eps epsexact qneg`.
- `run_identity.py` — identity residuals (exact) and Hessian spectra
  (float).
- `run_n2lift.py` — float lifted certificate on [E]'s A− (imports
  `window/n2win.py`, `n2/discrete.py`, `n2/model.py` read-only).
- `run_multi.py` — parts `two kink close close2 row sweep` (`sweep` added
  in revision; its `theta_1` formula corrected and a `u_s1` field added in
  round 3, Section 15).
- `rev1_checks.py` — revision checks: parts `spectraG` (40-digit spectra),
  `convexity`, `qneg` (exact margins and outer-node bounds), `epscover`
  (exact cover of the re-checked partitions), `cascade` (lifting cascade).
- `rev2_checks.py` — round-2 checks: parts `two4000` (exact certificates
  at the three `kappa = -0.5`, `N = 4000` grids of Section 9.1), `eps01`
  (float partitions at `epsilon / h^2 = 1e-1`), `tallies` (read-only
  tallies of `logs/eps.json` and `logs/sweep.json`).
- `rev3_checks.py` — round-3 checks (read-only, seconds): parts `compare`
  (rerun `logs/sweep.json` against the round-2 log
  `logs/pre_revision/sweep_r2.json`) and `tallies` (break times after
  `theta_1`, implied matching times, `theta_1` against `N`; in round 4,
  Section 16, `tallies` also compares the round-2 formula with its own
  `N = 16000` value and gives the overall ranges).
- `tables.py` — Markdown tables from the JSON logs (part `sweep` added in
  revision).

Commands (targeted runs only; `OMP_NUM_THREADS=1`; no project-wide
verification; CI not inspected; nothing committed):

1. `python3 run_kneg.py lifted qneg` → `logs/lifted_qneg.log`,
   `logs/lifted.json` (about 14 min, mostly `N = 4000, 8000`). Its first
   `qneg` version used the one-control certificate and failed at `N = 200`
   (60 nodes; a second small-margin stage); `qneg` was then switched to
   `certify_multi` and rerun (item 4), overwriting `logs/qneg.json`.
2. `python3 run_kneg.py eps epsexact` and `python3 run_kneg.py eps` →
   `logs/eps.{log,json}`, `logs/epsexact.json` (minutes). Earlier attempts:
   one crashed when the greedy rule stalled at `epsilon = 1e-12 h^2`
   (below float resolution; such `epsilon` are now skipped); one stalled in
   the outer range for `kappa = -1` (backtracking added); the first exact
   re-check used target `0.999 epsilon` and missed by `0.6%` at
   `epsilon = 1e-8 h^2` (float rounding; target `0.9 epsilon` since).
3. `python3 run_identity.py` → `logs/identity.{log,json}` (seconds).
4. `python3 run_kneg.py qneg lifted2 epsexact` →
   `logs/qneg_lifted2_epsexact.log`, `logs/qneg.json`, `logs/lifted2.json`,
   `logs/epsexact.json` (about 2 min; a first attempt stopped on an exact
   KKT-sign assertion at a node anchor; anchors were then allowed to be
   non-KKT, which keeps the bounds valid).
5. `python3 run_n2lift.py` → `logs/n2lift.{log,json}` (float; about 30 min).
6. `python3 run_multi.py two kink close row` → `logs/multi.log`,
   `logs/two.json` (three attempts: the first stopped when a node anchor was
   better than `zbar` (incumbent updates added), the second on the
   KKT-sign assertion; the third completed `two`, then its `close` stopped on
   a configuration without two switches).
7. `python3 run_multi.py close2` → `logs/close2.{log,json}` (minutes).
8. `python3 run_multi.py kink close row` → `logs/multi2.log`,
   `logs/kink.json`, `logs/close.json` (kink switch times now from the
   `N = 16000` KKT point; the first `kink` run used the `N = 400` switch
   times, accurate only to `±0.0025`, and is superseded). Its `row` part
   stopped on a fixed-endpoint case without a fractional stage.
9. `python3 run_multi.py row` → `logs/row.{log,json}` (seconds; four
   attempts: two exact-KKT fixes for bang-bang fixed-endpoint points (the
   multiplier is now the midpoint of its admissible interval), then the
   terminal value was changed from `-1` to `-63/64`, because `x_N = -1`
   puts the switch on a grid point at every tested `N`, and the active-set
   start of the row multiplier was fixed (the first version could return a
   point violating the row)).
10. `python3 tables.py two|kink|close_compact|row|n2lift` (tables of
    Sections 5.4 and 9 from the JSON logs). The JSON logs of items 6–8
    (`two`, `kink`, `close`, `close2`) were overwritten by the revision
    reruns (items 13–14); the first-version files are kept in
    `logs/pre_revision/`.
11. One-off commands, not logged: timing and structure scans for the toys
    (`/tmp/kstruct_scan.py`: the `k = 2` scalar toy has no single-switch
    structure and was dropped; target intervals for two-switch toys), the
    `kappa`-drop exploration for close switches, and the lifting cascade
    check of Section 7.2 (`fam_rmax` with the broken stages treated as
    parameters, six iterations at four `N` for two configurations).
12. Four web searches and two arXiv abstract-page fetches (Section 11), and
    a grep of the local literature index; the local Kannan–Barton paper's
    abstract and introduction read.

Commands run in the revision (2026-09-30; targeted only,
`OMP_NUM_THREADS=1`, explicit `timeout`; no project-wide verification; CI
not inspected; nothing committed; no process killed):

13. `python3 run_multi.py two kink` → `logs/rev1_two_kink.log`,
    `logs/two.json`, `logs/kink.json` (about 10 min wall time) and
    `python3 run_multi.py close close2` → `logs/rev1_close.log`,
    `logs/close.json`, `logs/close2.json` (minutes), after the
    `ktoy.py` data-convention fix. Before the fix: a check of `ktoy.data`
    against the documented rule `a(t) = a_i` on `[t_i, t_{i+1})` (one-off,
    output quoted in Section 9: one or two mismatching stages per grid for
    four `(t_1, t_2)`; after the fix, 0 mismatches for all seven
    `(t_1, t_2)` and `N` in {500, …, 16000} tested).
14. `python3 run_multi.py sweep` → `logs/sweep.log`, `logs/sweep.json`
    (about 20 min wall time; 7 configurations × 14 grids, one KKT search
    failure).
15. `python3 rev1_checks.py convexity qneg epscover` →
    `logs/rev1_{convexity,qneg,epscover}.json` (about 2 min);
    `python3 rev1_checks.py spectraG` → `logs/rev1_spectraG.{log,json}`
    (minutes); `python3 rev1_checks.py cascade` → `logs/rev1_cascade.json`
    (about 1 min).
16. `python3 tables.py two|kink|close_compact|sweep` (revised tables of
    Section 9); one-off Python tallies of `logs/eps.json` (ratios, margins
    below `-epsilon`).
17. Literature: the local copy of Wechsung–Schaber–Barton (2014) read
    (abstract, Sections 1–3, Theorem 2, conclusion); [W, Section 6] and
    [W, Proposition D] and [E, Section 2.5] re-read for the numbers quoted.
    No web searches in the revision.

Commands run in the round-2 revision (2026-09-30; targeted only,
`OMP_NUM_THREADS=1`, explicit `timeout`; no project-wide verification; CI
not inspected; nothing committed; no process killed). New script
`rev2_checks.py` (parts `two4000`, `eps01`, `tallies`):

18. `python3 rev2_checks.py tallies eps01` → `logs/rev2_tallies.json`,
    `logs/rev2_eps01.json` (seconds). `tallies` only reads `logs/eps.json`
    and `logs/sweep.json` (per-side predicted node counts; break times
    after `theta_1` on grids with a fractional second switch; layer-law
    ratios and implied matching times; `e_2`, `eta_hat_1` for
    `eta^X_1 = -0.275`). `eps01` reruns the float greedy partition for
    `kappa = -0.5`, `epsilon / h^2 = 1e-1`, `N = 1000, 4000, 8000`.
    (Its break times after `theta_1` and implied matching times came from
    the round-2 `logs/sweep.json` with a wrong `theta_1`; they are
    superseded by item 22, Section 15. `logs/rev2_tallies.json` is kept as
    run.)
19. `python3 rev2_checks.py two4000` → `logs/rev2_two4000.{log,json}`
    (exact; about 4 min, 77–82 s per grid): the box branch and bound of
    Section 9.1 at the three `kappa = -0.5`, `N = 4000` grids, with the
    settings of `run_multi.py two`. Run in the background; its completion
    was awaited with polling loops on the log file (no `pgrep`/`pkill`).
20. Read `reviews/kappa-negative-confirm-r1.md` and, for the layer-law
    notation, [E, Section 2.5]. No web searches and no new literature in
    this round.

A mistake during the work: one waiting loop used `pgrep -f` with a pattern
that matched its own shell, and a `pkill -f` early on killed the issuing
shell together with a background exploration (no files were affected; the
exploration was rerun).

Commands run in the round-3 revision (2026-10-01; targeted only,
`OMP_NUM_THREADS=1`, explicit `timeout`; no project-wide verification; CI
not inspected; nothing committed; no process killed). `run_multi.py sweep`
was corrected (Section 15); new script `rev3_checks.py` (parts `compare`,
`tallies`):

21. Copied `logs/sweep.{json,log}` to `logs/pre_revision/sweep_r2.{json,log}`,
    then `python3 run_multi.py sweep` → `logs/sweep.{log,json}` (float;
    98 records; per-grid times sum to 975 s). Run in the background and
    awaited with a polling loop on the log file.
22. `python3 rev3_checks.py compare tallies` → `logs/rev3_compare.json`,
    `logs/rev3_tallies.json` (read-only; seconds).
23. `python3 tables.py sweep`: the break table of Section 9.3, regenerated
    from the rerun log, is identical to the table in the text (`diff`).
24. Read `reviews/kappa-negative-confirm-r2.md`, [W, Remark 1.4], and
    `reviews/kappa-negative-confirm-r1.md` (source of its `-3.7e-4`). No
    web searches and no new literature in this round.

Commands run in the round-4 revision (2026-10-01; targeted only,
`OMP_NUM_THREADS=1`, explicit `timeout`; no project-wide verification; CI
not inspected; nothing committed; no process killed). `rev3_checks.py`
part `tallies` was extended (Section 16, N2); no other code changed:

25. Copied `logs/rev3_tallies.json` to `/tmp`, then
    `python3 rev3_checks.py tallies` → `logs/rev3_tallies.json`
    (read-only; seconds). A one-off Python comparison with the copy: the
    six old records are unchanged in every old field; each
    `P1_theta1_vs_N16000_in_stages` record gained the fields
    `theta1_N16000_roundtwo` and `rows_N_roundtwo_own_ref`, and one record
    `P1_theta1_overall` was added.
26. Read `reviews/kappa-negative-confirm-r3.md`, and its `c3_summary.py`
    (Check 4 part) and `logs/summary3.json` to see which reference it used
    and what it found. No web searches and no new literature in this round.

Commands run in the round-5 revision (2026-10-01; targeted only; no
project-wide verification; CI not inspected; nothing committed; no process
killed; no code changed, Section 17):

27. A one-off Python computation (float, read-only; under a second) from
    `logs/rev3_tallies.json`: `u_{s_1}(16000)` from the two fields
    `theta1_N16000` and `theta1_N16000_roundtwo` of `(0.55, 1.45)` and
    `(0.45, 1.55)`, then the two worked examples of Section 16 with
    unrounded and with rounded inputs. Read
    `reviews/kappa-negative-final-confirm-r1.md`. No web searches and no
    new literature in this round.

## 13. Revision after review (round 1)

Review: `reviews/kappa-negative-review.md` (independent; verdict "fixes
needed"; no theorem overturned). Each finding was first checked
independently with our own runs, then the text was changed. This revision
was re-reviewed in `reviews/kappa-negative-confirm-r1.md` (Section 14).

**F1 (major): the thin-layer reading of the close-switch recursion.**
*Check.* New `N`-sweep with the author's code (`run_multi.py sweep`, 7
falling-`kappa` configurations × 14 grids `N = 1000 … 16000`, float). It
reproduces the review grid by grid for `eta^X_1 = -0.275` (breaks at
`N = 3000, 3500, 4000, 7000, 8000` at `-4, 0, -14, -7, -18` stages from
`s_1`; none elsewhere) and its break offsets for `eta^X_1 = -0.59`
(0, 0, 0, +1, 0, +2, 0, +3, +1, +5 at the review's grids). The
layer-law estimate was recomputed: `exp(-3.5/0.275) ≈ 3e-6` times an
`O(1)` scale, below every tested `h`. Two recorded quantities explain the
moderate case: the recursion breaks exactly where the excess `e_2` carried
in from the second switch is `<= 0.08`. (Round 2: "explain" and "exactly
where" overstate the evidence, since the threshold was read off the same
14 grids; now "coincide with small `e_2`", Section 14, N2.) *Change.*
Summary item 6, Section 7.2 (discrete counterpart) and Section 9.3 rewritten: three
regimes as observed, sweep table and per-grid table added, thin-layer
explanation and "the sign of `eta^X_1` predicts the behaviour at small `h`"
withdrawn, no asymptotic claim; a heuristic reading is labelled as such.
"Within two stages" corrected to "2 stages before to 5 after" (all 42
strong-drop grids). The lifting cascade, unlogged in the first version, was
rerun and logged on the documented instances (`rev1_checks.py cascade`).

**F2 (moderate): decimal jump times converted through binary floats.**
*Check.* `ktoy.data` was compared with the documented rule at every grid
used: mismatching stages exactly as the review says (stage `0.65 N` for
`(0.7, 1.3)`; `0.325 N`, `0.675 N` for `(0.65, 1.35)`; one or two for
`(0.55, 1.45)`, `(0.45, 1.55)`). *Change.* `ktoy._piece` now reads jump
times exactly (`Fraction(repr(t_i))`; 0 mismatches after the fix) and the
wrong code comment was replaced. Sections 9.1, 9.2 and 9.3 were rerun.
On the documented `(0.7, 1.3)`, `N = 2000` instance our KKT search returns
the bang-bang point with switching stages 598 and 778 (plain gap
1.532 `h^2`), and the box branch and bound certifies it exactly with 9
nodes, as the review found. At `N = 500, 1000` that configuration's plain
certificate is now exact. The "KKT search returned a non-optimal point"
episode is kept as a documented result for the earlier instance only
(Summary item 3, Sections 3 and 9.1, status table). Section 9.2: two
`(0.65, 1.35)` rows now have no failing stage, and the `(0.7, 1.3)` rows
changed; the conclusion (at most one `h^3` failure, `K = 1` windows exact)
is unchanged. Section 9.3: three table rows changed slightly (and the KKT
points of a fourth); no break appeared or disappeared. First-version logs: `logs/pre_revision/`.

**F3 (moderate): most positive instances are convex.** *Check.* Float
reduced-Hessian eigenvalues at `N = 1000` (`rev1_checks.py convexity`):
positive definite for all `kappa >= 0` instances of 9.1 and all rising-`kappa`
configurations of 9.3; exactly one negative eigenvalue for each falling
configuration; 979 for `kappa = -0.5`. We also checked algebraically that
`P = -k` is exact at every KKT point when `kappa >= 0` (stage residual
`h sigma omega + h d^2/2 + (h^2/2) kappa omega^2`). We added a short argument
that the maximal recursion cannot break when the reduced Hessian is
positive definite. *Change.* New convexity paragraph at the start of
Section 9. Sections 9.1, 9.2 and 9.3, Summary item 6 and the status table
state that these rows are automatic and do not test separation or
locality. The same remark was added to the `kappa >= 0` rows of Section 9.4
(fixed endpoint; convex for `k <= 0` because `sum h k x_t u_t` is then a
constant plus `-(k/2) h^2 sum u_t^2`).

**F4 (moderate): summary qualifiers.** *Check.* Compared each summary
statement with the body and with [W, Proposition D] (which gives
`b^T P_b b - b^T w <= C (log(1/h))^{-1/2}`, an upper bound). *Change.*
(a) Item 2's heading now says that the size is `O(N)` only if a bounded
number of outer nodes suffices (heuristic, Remark 5.5), and that only the
central node is proved. (b) Item 1 and the text after Theorem 4.3 restrict
"need" to `kappa`-limited families whose exit slope is the node optimum's
costate. (c) Item 1 and Section 4 say "at most `kappa_tau + o(1)`" for
[W, Proposition D]. (d) Item 6 states the `A = 0`, constant `H_xx` condition
for the remainder-free form, and that an `O(1)` drop of `kappa` across a
short arc needs data that are not smooth in time or `ell` not small.

**F5 (minor).**

1. *`lambda_min(G) = h^3/4`.* Checked with 40-digit eigenvalues
   (`rev1_checks.py spectraG`): relative excess 2.4% (`N = 10`), 0.15%
   (`N = 40`), 0.025% (`N = 100`). Now "≈ `h^3/4`, leading order" (Summary
   item 4, Section 2).
2. *"Plus a constant".* Checked against Corollary 2.2: the extra term is
   linear in `u`, constant only when `u_- = -u_+`. Corrected in Summary
   item 4; a sentence added after Corollary 2.2.
3. *Remark 2.3 inequality.* Re-derived: the bound by the window deficit
   holds for the first term only. The one-coordinate estimate of the
   bracket is the review's; we re-derived it, and the condition
   `|kappa_tau| <= 4 eta_L` (true when `q > 0`). Now stated as a
   leading-order estimate, with [W]'s observed values (checked in
   [W, Section 6]: 0.18–0.25 against `K = 2` window deficits 0.30–0.57
   `h^2`).
4. *[W, Theorem B] for `Jt'`.* Agreed (stage cost quadratic in `u`). Now
   "plausible, not checked" (Remark 2.3, status table).
5. *`q < 0` margins and "certificates coincide".* Exact recomputation
   (`rev1_checks.py qneg`): `N = 200`: 1.32, 2.77 (stages 55, 54);
   `N = 400`: 0.76, 2.21 (stages 111, 112); outer-node bound at `N = 2000`
   `+1.763 h^2` (`q < 0` toy) against `+0.765 h^2` (`kappa = -1` toy).
   Corrected in Sections 3 and 5.3: KKT points, plain gaps and vertex-flip
   margins coincide where both have the same bang-bang KKT point;
   certificates do not.
6. *Section 4 numbers.* Tallied from `logs/eps.json`: `kappa = -1`
   outer-ring ratios 2.625–3.497; counts at `N = 1001, 1002, 4002` differ
   by up to 2 (predictions likewise); 25 of 44 float margins below
   `-epsilon` (10 by a relative `2e-6` to `1.2e-3`, 15 by at most `2e-7`).
   All stated in Section 4. Added an exact check that the two re-checked
   partitions cover `[-1, 1]` without gaps (`rev1_checks.py epscover`).
7. *A− interval.* Agreed: with `beta_t != 0` and box minima, Lemma 5.2(2)
   does not give an interval. Caveat added in Summary item 2, Section 5.4
   and the status table. No denser check was run (72 s to 23 min per grid
   per evaluation).
8. *"The optimum is bang-bang" for `q < 0`.* Qualified: minimizers near
   the reference trajectory, and every minimizer of the toy (all
   `H_tt < 0`, checked from the exact Hessian formula
   `H_tt = h^2 (h (N - 1 - t) + phi2)` with `phi2 = -2` and `h (N - 1 - t) < T = 2`).
   Summary item 3, Sections 3 and 5.3.
9. *Theorems A_k, B_k.* Relabelled "proof by locality, sketch level"
   (Summary item 5, Section 6, status table).

**F6 (literature).** *Check.* Read the local copy of
Wechsung–Schaber–Barton (2014) (abstract, Sections 1–3, Theorem 2,
conclusion): second-order relaxations give a cluster size independent of
`epsilon`, and 1 box when the prefactor is at most `lambda_1/8`. *Change.*
Cited in Section 11. The remarks after Theorem 4.3 now say that the
logarithmic count is the generic one-dimensional cost of geometric
covering, not a cluster effect. The specific contributions are
`epsilon = 0` impossibility (Corollary 4.2), the ratio `rho*`, and the
lifted bound. Remark 2.3, Summary item 1, the novelty paragraph and the
status table were adjusted.

**Not changed.** The theorems and their proofs in Sections 2–8 (the review
found them correct within their hypotheses); the exact certificates of
Sections 5.3 and 9.1 that the review reproduced; Section 9.4 (dyadic data,
unaffected by F2).

## 14. Revision after review (round 2)

Review: `reviews/kappa-negative-confirm-r1.md` (independent confirmation
of the round-1 revision; verdict "minor fixes needed (text only)"; it
reproduced every changed number it recomputed, and none of its items
affects a theorem or a main conclusion). Each item below was first checked against our logs or by a
rerun, then the text was changed. This revision was re-reviewed in
`reviews/kappa-negative-confirm-r2.md` (Section 15).

**R1 (minor): `f* = J(zbar)` claimed on grids where no certificate had
been run.** *Check.* `logs/two.json`: the three `kappa = -0.5`, `N = 4000`
rows of Section 9.1 have no certificate record (plain gaps 0.8685, 0.8766,
0.8769 `h^2`), yet the status table said "`f* = J(zbar)` on every
single-switch grid and every documented two-switch grid". As written, that
claim was not supported, and "every tested grid" in Summary item 3 and
Section 3 was correct only if "tested" meant "where the certificate was
run". *Rerun.* Instead of only narrowing the claim, we ran the missing
certificates: `rev2_checks.py two4000` (exact rational arithmetic, the
box branch and bound `certify_multi` with the settings of
`run_multi.py two`, about 80 s per grid). The exact KKT points agree with
`logs/two.json` (switching stages, fractional stage, plain gap). All three
grids are certified, each with 3 nodes (one lifted node on the fractional
stage, two ordinary outer nodes), and no node anchor is better than
`zbar`, so `f* = J(zbar)` there (`logs/rev2_two4000.{log,json}`). *Change.*
Section 9.1 table and text (the three rows now read "exact, 3 nodes";
"seven grids, `N <= 2000`" becomes "all ten grids with a failing stage,
`N = 500 … 4000`"; the first revision's omission is stated), Summary items
2 and 3, Section 3 and the status table now say "all 36 grids of
Section 9.1" and state that the `N = 4000` certificates were added in this
round. Remark 5.5's range of 3–9 nodes is unchanged.

**R2 (minor): "for `kappa = -0.5` the counts do not depend on `N`".**
*Check.* `logs/eps.json`: at `epsilon / h^2 = 1e-1` the counts are 3, 3, 2
at `N = 1000, 4000, 8000`, with predictions 3, 3, 2, so the sentence was
wrong. Recomputing the predicted count side by side
(`rev2_checks.py tallies`) shows the cause: at `N = 8000`,
`ubar_n - u_- = 0.539 < w_0 = 0.632`, so the `u_-` side needs no outer
node; at `N = 1000` and `4000` both sides need one. A float rerun of the
greedy partition (`rev2_checks.py eps01`) gives the central node
`[-1, 0.172]` and one outer node `[0.172, 1]` at `N = 8000`, against three
nodes at `N = 1000, 4000`. `q` and `rho*` differ by less than 0.1% between
the tested `N`, so the predicted counts depend on `N` essentially only
through `ubar_n`, for both toys. *Change.* Section 4: the sentence is
replaced by the `ubar_n` dependence for both toys, with this exception
stated.

**R3 (minor): Section 7.2 lacked the caveats of Section 9.3.** *Check.*
`logs/sweep.json` (`break_time_minus_theta1`), tallied by
`rev2_checks.py tallies`: on grids with a fractional second switch the
break lies `5.7e-4 … 6.7e-4` after `theta_1` for `(0.5, 1.5)`
(`N = 3500, 6000, 10000, 16000`), `5.7e-4 … 9.7e-4` for `(0.55, 1.45)`
(`N = 2500, 3500, 4000, 5000, 6000`) and `1.2e-4 … 2.0e-4` for
`(0.45, 1.55)` (`N = 6000, 10000`); at `N = 1000` the second switch is
fractional for `(0.5, 1.5)` and `(0.45, 1.55)` and the breaks lie `0` and
`-1.63e-3` from `theta_1`. The layer-law ratios
`exp(-2 gamma / (Delta |eta|))` were recomputed (1.89e-3, 5.58e-3,
4.20e-4; 2.97e-6 for `eta^X_1 = -0.275`); the matching times that would
reproduce the observed break times are 0.30–0.35, 0.10–0.17 and
0.29–0.48, so agreement needs a matching time between about 0.1 and 0.5,
a factor-5 range across the three configurations. [Corrected in round 3
(Section 15, P1). The round-2 version of this entry gave `5.3e-4 … 9.2e-4`,
`2.0e-4 … 2.1e-4`, `-3.73e-4` ("as the review says") and the matching
times 0.095–0.16 and 0.48–0.50. These came from a `theta_1` with the wrong
sign of `u_{s_1}` in `logs/sweep.json`. The review of this round
(`reviews/kappa-negative-confirm-r1.md`, line 103) quoted its `-3.7e-4`
from the same log field, so that agreement was not an independent check.
The ranges and ratios above are from `rev3_checks.py tallies`.] *Change.* Section 7.2
now says "at larger `N`", states the `N = 1000` exception, and says that
the agreement is a consistency observation that needs an undetermined
matching time of 0.1–0.5, not a test. Section 9.3 now lists the grids of
each range and the `N = 1000` exception, says that the `s_1` of the layer
law is [E]'s matching time and not the switching stage `s_1` of the
Section 9.3 tables, and says "resembles that of a resolved layer" instead of "is the
behaviour of a resolved layer".

**N1 (nit): `eta_hat_1 <= -0.34`.** *Check.* `logs/sweep.json`: the
breaking grids have `eta_hat_1` = -0.513, -0.551, -0.502, -0.545 and
-0.3375 (`N = 8000`). The bound `<= -0.34` was false. *Change.* Section
9.3 now says `<= -0.33` and gives the values.

**N2 (nit): "decided by the excess carried in from the second switch".**
*Check.* The five breaking grids of the `eta^X_1 = -0.275` configuration
have `e_2 <= 0.079` and the nine others `e_2 >= 0.176`
(`rev2_checks.py tallies`). The split was read off these same 14 grids
after the fact, and the only breaking grid with a vertex second switch
(`N = 8000`, `e_2 = 0.079`) lies just below it. So "decided by",
"exactly where" and "what decides" claimed more than the data show.
*Change.* The status table, Summary item 6, Section 7.2 and Section 9.3
now say that the breaks coincide with a small `e_2` on the tested grids,
that the separation was read off after the fact and is not a tested
criterion; the round-1 entry F1 above carries a pointer to this change.

**Not changed.** The theorems and proofs of Sections 2–8; the exact
certificates of Sections 5.3, 9.1 (`N <= 2000`) and 9.2; the float tables
of Sections 4 and 9.3 (only the text around them changed); Section 9.4.

## 15. Revision after review (round 3)

Review: `reviews/kappa-negative-confirm-r2.md` (independent confirmation
of the round-2 revision; verdict "minor fixes needed (numbers only)"; it
found R1, R2 and both nits of round 2 resolved and the R3 wording properly
hedged). It raised one item, P1. The item was first checked by a
derivation, a rerun and a comparison of logs, then the text was changed.
This revision was re-reviewed in `reviews/kappa-negative-confirm-r3.md`
(Section 16).

**P1 (minor; numbers in a float observation): wrong phase position
`theta_1` of a fractional first switch.** The review is right.

*Check 1 (derivation; proved, elementary).* In the toy `x' = u`, stage `n`
moves `x` by `h u_n`. The phase model of [W, Remark 1.4] replaces the
stage by a switch at `theta` in `[t_n, t_{n+1}]`, with `+1` before `theta`
and `-1` after it; this moves `x` by
`(theta - t_n) - (t_{n+1} - theta) = 2 (theta - t_n) - h`. Equating the two
gives `theta = t_n + h (1 + u_n) / 2`. This is the rule
`theta = t_n + h (u_n - u_after) / (u_before - u_after)` that
`run_multi.py kink` already uses, with `u_before = +1`, `u_after = -1`. It
tends to `t_n` as `u_n -> -1`, which matches the vertex rule
`theta_1 = t_{s_1}`. The round-2 `run_multi.py sweep` used
`t_n + h (1 - u_n) / 2`, which tends to `t_{n+1}` instead. The two
formulas differ by `h u_{s_1}`, so only grids with a fractional first
switch (where `s_1` is the fractional stage) are affected.

*Check 2 (rerun and log comparison; float).* The formula in `run_multi.py`
was corrected, a field `u_s1` was added to each record, and
`run_multi.py sweep` was rerun for all 7 configurations and 14 grids (the
round-2 log is kept as `logs/pre_revision/sweep_r2.{json,log}`).
`rev3_checks.py compare` (`logs/rev3_compare.json`): in all 98 records,
every field present in both logs other than `break_time_minus_theta1` and
the run time is identical. So the break stages, `e_2` and `eta_hat_1` are
unchanged, and so are both tables of Section 9.3; the break table also
regenerates identically with `tables.py sweep`. `break_time_minus_theta1`
changed on exactly the 24 grids that have a fractional first switch and a
break, each time by `-h u_{s_1}` (deviation at most `5.4e-17`), and on no
other grid. Of these 24, only the 4 below belong to the quoted set
(strongly negative configurations, grids with a fractional second switch);
the other 20 values were not quoted in the text.

| configuration | `N` | `u_{s_1}` | round 2 | corrected |
|---|---|---|---|---|
| `(0.55, 1.45)` | 4000 | -0.8821 | `5.29e-4` | `9.71e-4` |
| `(0.55, 1.45)` | 6000 | +0.5000 | `9.17e-4` | `7.50e-4` |
| `(0.45, 1.55)` | 1000 | +0.6275 | `-3.73e-4` | `-1.63e-3` |
| `(0.45, 1.55)` | 6000 | +0.2647 | `2.11e-4` | `1.23e-4` |

These agree with the review's table to the digits given (the review rebuilt
the KKT points with its own code). The other 9 quoted grids have a vertex
first switch, and their values are unchanged.

*Check 3 (tallies; float, read from the rerun log).*
`rev3_checks.py tallies` (`logs/rev3_tallies.json`) computes the ranges
and the implied matching times from the log; round 2 had typed the ranges
into `rev2_checks.py`. On grids with a fractional second switch and
`N > 1000`, the break lies `5.71e-4 … 6.67e-4` after `theta_1` for
`(0.5, 1.5)`, `5.71e-4 … 9.71e-4` for `(0.55, 1.45)` and
`1.23e-4 … 2.00e-4` for `(0.45, 1.55)`. Overall this is `1.2e-4 … 9.7e-4`,
and within each configuration the times vary by a factor of 1.2, 1.7 and
1.6. With the unchanged layer-law ratios `1.890e-3`, `5.581e-3` and
`4.199e-4`, the matching times that would reproduce these break times are
0.30–0.35, 0.10–0.17 and 0.29–0.48. Overall that is 0.10–0.48, still
"about 0.1 to 0.5", a factor of about 5. At `N = 1000` for
`(0.45, 1.55)`, the break is at the start of the fractional stage `s_1`,
0.81 stage before `theta_1`. So the `N = 1000` exception is more
pronounced than round 2 stated.

*Check 4 (consistency of the convention with the data; float, heuristic).*
If `theta_1` is the right phase position, `theta_1(N)` should approach the
continuous switch time smoothly. On the 20 grids with a fractional first
switch and `N < 16000` (all three strongly negative configurations),
`theta_1(N) - theta_1(16000)` lies between `-0.70` and `-0.01` stages of
grid `N` with the corrected formula. With the round-2 formula, with its own
`theta_1(16000)` as the reference, it lies between `-1.29` and `+0.48`
stages. [Corrected in round 4 (Section 16, N2). The round-3 text gave
`-1.33 … +0.52`, which measured the round-2 values against the corrected
`theta_1(16000)`.] This supports the derivation but does
not replace it: the reference `theta_1(16000)` is itself a discrete value,
and the consistently negative offset of the corrected values was not
analysed.

*Change.*
- Section 7.2: `2e-4` to `9e-4` becomes `1.2e-4` to `9.7e-4`, with the
  per-configuration factors; `-3.7e-4` becomes `-1.6e-3` (0.8 stage
  before `theta_1`); the matching times become 0.30–0.35, 0.10–0.17 and
  0.29–0.48; a pointer to this section was added.
- Section 9.3: the ranges for `(0.55, 1.45)` and `(0.45, 1.55)` and the
  `N = 1000` value were corrected, and the convention for `theta_1` is now
  stated once there.
- Section 14, R3: the numbers were replaced. A bracketed note gives the
  round-2 values and their cause, and says that the round-2 review's
  `-3.7e-4` came from the same log field.
- Code: `run_multi.py` (formula, comment and `u_s1` field);
  `rev2_checks.py` (a comment says that its typed-in ranges are
  superseded); new `rev3_checks.py`.
- Header and Section 12 (files; item 18 note; items 21–24).

The conclusion is unchanged. For the strongly negative cases, the larger-`N`
break times are consistent with the layer law only for an undetermined
matching time of about 0.1–0.5. This is a consistency observation, not a
test, and no asymptotic claim is made.

**Not changed.** The theorems and proofs of Sections 2–8; all exact
certificates; the float tables of Sections 4 and 9.3; Section 9.4; the
moderate (`eta^X_1 = -0.275`) and weak cases of Section 9.3, whose quoted
numbers do not involve `theta_1`.

## 16. Revision after review (round 4)

Review: `reviews/kappa-negative-confirm-r3.md` (independent confirmation
of the round-3 revision; verdict "P1 is resolved. Numbers verified; no
fixes needed"). It rebuilt the KKT points with its own code and agreed
with every changed number. It listed two optional nits, N1 and N2, and
said that neither affects a number in the main text or a conclusion. Both
were checked and applied. This revision was re-reviewed in
`reviews/kappa-negative-final-confirm-r1.md` (Section 17).

**N1 (nit): stale status line in Section 14.** *Check.* The Section 14
preamble said "These changes have not been re-reviewed", but
`reviews/kappa-negative-confirm-r2.md` reviewed them (the header and the
Section 15 preamble say so). The Section 15 preamble had the same stale
line, since `reviews/kappa-negative-confirm-r3.md` reviewed the round-3
changes; the header also said that the round-3 changes had not been
re-reviewed. *Change.* The Section 14 preamble now says "This revision was
re-reviewed in `reviews/kappa-negative-confirm-r2.md` (Section 15)", as the
review suggested, and the Section 15 preamble says the same with
`reviews/kappa-negative-confirm-r3.md` (Section 16). The header now lists
the fourth review and says that only the round-4 changes are unreviewed.

**N2 (nit; a heuristic float check): the reference in Section 15, Check 4.**
*Check.* The review is right. `rev3_checks.py tallies` measured both the
corrected and the round-2 `theta_1(N)` against the *corrected*
`theta_1(16000)`. For `(0.5, 1.5)` the `N = 16000` first switch is a vertex,
so both formulas give the same reference. For `(0.55, 1.45)` and
`(0.45, 1.55)` it is fractional (`u_{s_1} = -0.5436` and `+0.5891`), so the
round-2 reference differs by `-h u_{s_1}` with `h = 1/8000`. In stages of
grid `N`, the round-2 values therefore shift by `(N / 16000) u_{s_1}(16000)`.
We extended `rev3_checks.py tallies` to also measure the round-2 formula
against its own `theta_1(16000)` and to report the ranges over all 20 grids
(float, read from `logs/sweep.json`; `logs/rev3_tallies.json`, record
`P1_theta1_overall`). Results (stages of grid `N`):

| formula | reference `theta_1(16000)` | range |
|---|---|---|
| corrected | corrected | `-0.701 … -0.014` |
| round 2 | corrected (round-3 text) | `-1.329 … +0.522` |
| round 2 | round 2 (its own) | `-1.289 … +0.478` |

The new extremes are `(0.55, 1.45)`, `N = 6000`
(`-1.0856 + (6000/16000)(-0.5436) ≈ -1.289`) and `(0.45, 1.55)`, `N = 2500`
(`0.386 + (2500/16000)(0.5891) ≈ 0.478`). We checked both by hand from the
per-grid values. All three ranges agree with the review's `c3_summary.py`
(`logs/summary3.json`, from its own KKT points) to within `3e-12` stages,
over the same 20 grids. The old fields of
`logs/rev3_tallies.json` are unchanged (Section 12, item 25).
*Change.* Section 15, Check 4 now quotes `-1.29 … +0.48` for the round-2
formula with its own reference. A bracketed note gives the round-3 range
and its reference. The contrast with the corrected range (`-0.70 … -0.01`,
unchanged) and the heuristic reading of it do not change.

*Code.* `rev3_checks.py`, part `tallies`: new fields
`theta1_N16000_roundtwo` and `rows_N_roundtwo_own_ref`, a new record
`P1_theta1_overall`, and a docstring line. The part only reads
`logs/sweep.json`, and the existing fields are computed by unchanged code,
so the change cannot alter a reported result. The comparison in item 25
confirms this. Section 12 (script description; items 25–26) was updated.

**Not changed.** Everything else: the theorems and proofs, all exact
certificates, all float tables, and every number in Sections 7.2, 9.3 and
14 and in Checks 1–3 of Section 15. The conclusion of Section 15 is
unchanged.

## 17. Revision after review (round 5)

Review: `reviews/kappa-negative-final-confirm-r1.md` (independent
confirmation of the round-4 revision; verdict "Verified"). It found N1 and
N2 of round 4 applied correctly, and all new numbers in Sections 15 and 16
agreed with its own rebuild of the KKT points to within `5e-12` stages. It
listed two optional nits, O1 and O2, and said that neither affects a number
in the main text or a conclusion. Both were checked and applied. These
changes have not been re-reviewed.

**O1 (optional): rounding in a worked example of Section 16.** *Check*
(float, Section 12, item 27). From `logs/rev3_tallies.json`, the
`(0.55, 1.45)`, `N = 6000` value of the round-2 formula against the
corrected reference is `-1.085573`, and
`u_{s_1}(16000) = -8000 (theta1_N16000_roundtwo - theta1_N16000) = -0.543612`.
So the value against its own reference is
`-1.085573 + 0.375 (-0.543612) ≈ -1.28943`, which agrees with the logged
`-1.2894273`. The review is right: with the rounded inputs shown before,
`-1.086 + 0.375 (-0.5436) = -1.28985`, which rounds to `-1.290`, not
`-1.289`. With `-1.0856` the line gives `-1.28945`, which rounds to
`-1.289`. The second example already checks:
`0.386 + (2500/16000)(0.5891) = 0.47805`, which rounds to `0.478`, as does
the logged `0.47757`. *Change.* The first
example now reads `-1.0856 + (6000/16000)(-0.5436) ≈ -1.289`. The second
uses `≈` instead of `=` as well, since its inputs are also rounded. The
quoted range `-1.289 … +0.478` does not change.

**O2 (optional): review-status lines.** *Check.* The header and the
Section 16 preamble said that the round-4 changes had not been
re-reviewed. `reviews/kappa-negative-final-confirm-r1.md` reviewed them.
*Change.* The Section 16 preamble now says "This revision was re-reviewed
in `reviews/kappa-negative-final-confirm-r1.md` (Section 17)". The header
now lists the fifth review, says that it re-reviewed the round-4 changes,
and says that only the round-5 changes are unreviewed. The date line now
reads "round-3 to round-5 revisions".

**Not changed.** Everything else, including every number outside the one
worked example of Section 16, all code and all logs.
