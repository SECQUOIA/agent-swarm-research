# Review of `theory-bangbang/kappa-negative.md`

Date: 2026-09-30. Reviewer: independent, adversarial verifier; I did not
write the note or its scripts. Scope: every proof step, the hypotheses, the
certificate-size bounds and their dependence on `h` and `epsilon`, the
several-switch and terminal-row parts, and the numbers. I re-checked the
numbers with my own code, in exact rational arithmetic wherever the note
claims exactness. Checks and logs: `reviews/kappa-negative-review-checks/`.

Labels used here: **exact** means rational arithmetic in my own code;
**float** means floating-point screening; **reproduced** means my code gives
the same result as the author's log. I imported the author's code only once,
to test its data convention (finding 2). Everything else is my own
implementation.

## Verdict

**Fixes needed.** The mathematics of Part 1 is sound within its stated
hypotheses. Every exact certificate claimed in Sections 5.3 and 9.1 is
reproduced by my own code. For the `q < 0` toy, `f*` is also confirmed by a
second method that uses no calibrations. Four problems need correction:

1. The thin-layer reading of the close-switch recursion (Summary item 6,
   Sections 7.2 and 9.3) is contradicted by a sweep over `N`.
2. Several two-switch instances are not the instances the note describes:
   the decimal jump times are converted through binary floats.
3. The convexity of most "positive" test instances is not stated, and it
   makes those results automatic.
4. Some summary statements drop the qualifiers that the body states.

None of these overturns a theorem. Findings 1 and 3 change what the Part 2
numerics show.

## 1. Main findings, most important first

### F1 (major). For moderately negative `eta^X_1` the break is grid-phase dependent; it is not a thin layer

The note says that for `kappa` dropping from 0.5 to 0 (`eta^X_1 = -0.275`)
the recursion "breaks only from `N = 4000` on, as a thin layer would"
(Summary item 6). Section 9.3 says "This is the behaviour of a layer whose
width shrinks exponentially in `1/|eta|`". Section 7.2 says "the break
appears only at small `h`".

My float sweep (own KKT search, own recursion; author's data convention) is
in `logs/close_sweep.log`. Same configuration, `(t_1, t_2) = (0.6, 1.4)`:

| `N` | 1000 | 1500 | 2000 | 2500 | 3000 | 3500 | 4000 | 5000 | 6000 | 7000 | 8000 | 10000 | 12000 | 16000 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| break − `s_1` (stages) | none | none | none | none | −4 | 0 | −14 | none | none | −7 | −18 | none | none | none |

The break is not monotone in `h`. It depends on the grid phase.

- At `N = 2000` the excess after the switch is
  `P_{s_1+1} - kappa_1 = -0.06`. At `N = 4000` it is `-0.46`
  (`logs/close_profile.log`). At `N = 4000`, `P` then blows down within 14
  stages *before* the switch.
- The layer law of [E, Section 2.5] puts the blow-up at
  `s_b ~ s_1 exp(-2 gamma/(Delta |eta|))`. With `gamma ≈ 3.5`, `Delta = 2`
  and `|eta| = 0.275`, `exp(-12.7) ≈ 3e-6`, times an `O(0.1)` scale. That
  is far below every tested `h`. So the law does not explain breaks at
  `N = 3000–8000`.

For the strong drop (`eta^X_1 = -0.59`, `(0.5, 1.5)`) the recursion breaks
at every tested `N` up to 16000 (`logs/close_sweep2.log`). The break lies
0–5 stages *after* `s_1`. At `N = 6000, 10000, 16000` this is a roughly
constant time of about `6e-4` after the switch, which is consistent with a
resolved layer. "Within two stages" holds only on the 12 grids in the note.
For `eta^X_1 = -0.085` and `-0.04` there is no break up to `N = 16000`.

**Requested change.** Drop the thin-layer explanation for the
`eta^X_1 = -0.275` case and the sentence "the sign of `eta^X_1` predicts the
behaviour of the discrete recursion at small `h`". Report the three regimes
as observed:

- robust break for strongly negative `eta^X_1`;
- phase-dependent breaks for moderately negative `eta^X_1`;
- no break up to `N = 16000` for slightly negative or positive `eta^X_1`.

Make no asymptotic claim.

### F2 (moderate). Decimal jump times are not "decided exactly"; several instances differ from the documented ones

`ktoy._piece` compares `Fraction(t_i) * N <= t * T` with `t_i` a Python
float. Its comment says "decided exactly (dyadic floats)". This holds for
0.5, 0.75, 1.25 and 1.5. For 0.45, 0.55, 0.65, 1.3, 1.35 and 1.55, however,
`Fraction(float(t_i)) > t_i`. A stage with `t h = t_i` exactly then keeps
the old target value, although the documented rule is
`a(t) = a_i on [t_i, t_{i+1})`.

I tested the author's `data()` directly. The stage with `a != intended` is:

- `(0.7, 1.3)`: stage `0.65 N` at every tested `N`;
- `(0.65, 1.35)`: two stages (`0.325 N` and `0.675 N`);
- `(0.55, 1.45)` and `(0.45, 1.55)`: one or two stages.

One stage of a target that jumps by 8 is an `O(h)` change in the costates,
so the discrete optimum can change. At `(0.7, 1.3)`, `N = 2000`,
`kappa = -0.5`:

- **Author's instance** (exact, my code): the optimum is the point with
  fractional stage 597 (`u = -0.005412156536219817`). It lies
  `0.30991158604134855 h^2` below the KKT point with fractional stage 778.
  This reproduces Section 9.1 to all printed digits. My own box branch and
  bound certifies it with 7 nodes (5 leaves).
- **Documented instance** (`t_2 = 13/10` exactly): the optimum is a
  different, bang-bang point with switching stages 598 and 778. It has two
  small-margin vertex stages and a plain gap of `1.532 h^2`. My box branch
  and bound certifies it exactly with 9 nodes
  (`logs/two_bb_documented_instance.log`).

So the "KKT search returned a non-optimal point" episode holds for the
code's instance only.

**Requested change.** Either convert `t_i` exactly (`Fraction(str(t_i))`) and
rerun the affected rows, or state the convention ("`a` switches at the first
stage with `t h > fl(t_i)` when `fl(t_i) > t_i`") and fix the code comment.
Sections 9.2 and 9.3 are affected in the same way. Their float conclusions
should not change, but stage numbers and fractional stages will.

### F3 (moderate). Most "positive" test instances are convex; say so

By Proposition 2.1, for `x' = u`, `x_0 = 0` and piecewise-constant `k`:

```
J = J_0 + Phi(x_N) + (k_2/2) x_N^2 + ((k_1 - k_2)/2) x(t_k)^2 + (h^2/2) sum_t kappa_t u_t^2 .
```

Here `x(t_k)` is the state at the first stage with `k = k_2`. Float
smallest eigenvalues of the reduced Hessian at `N = 1000`
(`logs/convexity.log`):

| case | smallest eigenvalue `/h^2` | negative eigenvalues |
|---|---|---|
| Section 9.1, `kappa = +0.5` | `+0.50` | 0 |
| Section 9.1, `kappa = 0` | `+0.0005` | 0 |
| Section 9.1, `kappa = -0.5` | `-0.4995` | 979 |
| Section 9.3, `kappa` rising (all) | `> 0` | 0 |
| Section 9.3, `kappa` falling (all) | `< 0` | 1 |

For `kappa >= 0` the tangential family `P = -k` has, at every stage,
`beta_t = 0`, `K_t = h` and `u`-curvature `-k >= 0`, and the terminal
condition holds. So every stage loss is zero exactly when the KKT sign
holds, and the gap is exactly 0 at *every* KKT point. This is consistent
with `J` being convex.

- The 24 "exact, no window" grids of Section 9.1 (`kappa >= 0`) are
  therefore automatic. They test nothing about locality or separation.
- In Section 9.3, 9 of the 10 configurations with `eta^X_1 > 0` (all
  "rising `kappa`" ones, including `ell = 0.015`) are convex problems. Only
  `+0.5 -> +0.3` at `(0.5, 1.5)` is nonconvex.
- Section 9.2 uses the convex `kappa = 0` toy with a deliberately poor
  family; that check is still meaningful as a window test.

**Requested change.** State the convexity and lower the evidential weight of
these rows for Theorems A_k and B_k and for "`eta^X_1 > 0` never breaks".

### F4 (moderate). Summary statements drop qualifiers that the body states

- **Summary item 2** is headed "Lifted (parametric) calibrations give exact
  certificates of size `O(N)`". Only the central node is proved
  (Theorem 5.4). That `O(1)` outer nodes suffice is a heuristic
  (Remark 5.5). The heading should say "`O(N)` if a bounded number of outer
  nodes suffices (heuristic; true on all tested grids)".
- **Summary item 1** says "`epsilon`-certificates need and suffice
  `Theta(log(h^2/epsilon))` nodes". The lower bound (Theorem 4.3(b)) holds
  only for node families that are `kappa`-limited *and* whose exit slope
  equals the costate of the node optimum. For `epsilon > 0` nothing forces
  that slope (the argument of Corollary 4.2 needs exactness). The class must
  be restated where "need" appears. The task summary's wording ("node
  families anchored at node optima") is correct.
- **Summary item 1**: "`kappa_W` ... is `kappa_tau + o(1)` for families exact
  over `R^n x U`". [W, Proposition D] gives only `limsup <= kappa_tau`. That
  upper bound is what "`kappa`-limited" needs, but it is not an equality.
- **Summary item 6** states "`kappa_1 > kappa_2 + ell b^T H_xx b` ⇒ no
  tangential calibration" without its conditions (`A = 0`, `H_xx` constant;
  otherwise use (7.1) with its `2 w^T A b` term and `O(ell^2)` remainder).
  It also does not say that an `O(1)` drop of `kappa` across a short arc
  needs data that are not smooth in time, as in the toy, or `ell` not small.
  The body says both.

### F5 (minor). Wording and smaller inaccuracies

1. **`lambda_min(G) = h^3/4`** (Summary item 4, Section 2) holds only to
   leading order. My 40-digit eigenvalues give
   `lambda_min(G)/h^2 = (h/4)(1 + r)` with `r = 2.4%` (`N = 10`), 0.15%
   (`N = 40`) and 0.025% (`N = 100`) (`logs/spectra.log`). Write "≈".
2. **"On bang-bang sequences `J` is a `kappa = 0` transcription plus a
   constant"** (Summary item 4). By Corollary 2.2 it is plus a *linear*
   term, which is constant only when `u_- = -u_+`.
3. **Remark 2.3, first bullet.** "Never larger than the leading term of the
   window deficit" is justified only for the first term of the gap. The
   bracket `[Jt'(ubar) - min Jt']` is not bounded. A one-coordinate estimate
   gives `≈ h^2 kappa^2 (ubar_n - u_- - (u_+ - ubar_n))^2 / (8 eta_L)`; with
   it the inequality holds when `|kappa_tau| <= 4 eta_L` (true if `q > 0`).
   Other small-margin vertex stages can also add to the bracket. State it as
   leading order, or as observed ([W]'s 0.18–0.25 against 0.30–0.57 `h^2`).
4. **Remark 2.3, second bullet.** [W, Theorem B] does not apply verbatim to
   `Jt'`. Its stage cost is quadratic in `u` (`L_t` is not affine in `u`, as
   [W, Section 0] assumes), and `Jt'` has its own KKT points and rate. Label
   it "plausible, not checked".
5. **Section 5.3, `q < 0` toy.** The margins "1.32 and 2.77" are the
   `N = 200` values; at `N = 400` they are 0.76 and 2.21 (exact).
   "Certificates coincide" with the `k = 1` toy is too strong. Plain gaps
   and vertex margins coincide, but the outer-node bounds differ (0.765
   against 1.763 `h^2` at `N = 2000`).
6. **Section 4 numbers.**
   - "Inner ratios 4.316–4.567 (`kappa = -1`)" omits logged ratios of
     2.63–3.50 at the outermost rings. These do not contradict
     Theorem 4.3, which gives upper bounds on ratios, but the range is
     selective.
   - "Counts do not depend on `N` at fixed `epsilon/h^2`" holds for
     `kappa = -0.5`. For `kappa = -1` the counts at `N = 1001/1002` and
     `4002` differ by up to 2, through `ubar_n`; the predictions differ in
     the same way.
   - Several logged float node margins lie below `-epsilon` by a relative
     `1e-5` to `1e-3` (rounding). Only two partitions were checked exactly.
7. **Section 5.4 (A−, float).** With `beta_t != 0` and stage minima over the
   reachable box, the zero-loss set in `v` is not shown to be an interval:
   Lemma 5.2(2) covers `R^n x U`, or boxes with an interior minimizer. The
   bisection checks finitely many points, so the float certificate does not
   establish zero loss on all of `V`. Add this caveat.
8. **Section 3, "the optimum is bang-bang" when `q < 0`.** This needs every
   possible fractional stage of a minimizer to lie near the switch, where
   `H_tt ≈ h^2 q < 0`. That holds for minimizers near the reference
   trajectory, and trivially for the toy (`H_tt < 0` at every `t`). Say so.
9. **Theorems A_k, B_k ("proved (locality)").** The argument is sound at the
   level of detail of [W]. However, (P1)–(P7) for several switches are taken
   from (SH_k) and the per-step locality of [R, Theorem 4.1] (a)–(e) is
   asserted, not re-derived. Call it a "proof by locality (sketch level)".

### F6 (literature). Cite Wechsung–Schaber–Barton (2014) and reframe the cluster-problem comparison

[W] cites A. Wechsung, S. D. Schaber, P. I. Barton, *The cluster problem
revisited*, J. Global Optim. 58 (2014) 429–438. A local copy is at
`literature/papers/wechsung2014-the-cluster-problem-revisited`; I read the
abstract, Sections 1–3 and the conclusion. Their result: with second-order
convergent relaxations, the number of boxes in the cluster does not depend
on `epsilon`, and there is a prefactor threshold below which the cluster
problem disappears.

In one dimension, any second-order relaxation that branches geometrically
needs `O(log(1/epsilon))` nodes to cover a fixed range. That is the depth
cost of bisection, not a cluster blow-up. So the sentence "in one dimension
this gives `Theta(log(1/epsilon))` boxes" in cluster-problem language
overstates the link. What is specific here is:

- that `epsilon = 0` is impossible with finitely many `kappa`-limited nodes
  (Corollary 4.2), because the relaxation is not exact at the minimizer
  whatever the node width;
- the explicit ratio `rho*`, which includes the first-order term of the
  anchored bound.

The note should cite Wechsung et al. and qualify Theorem 4.3's novelty
accordingly. I found nothing that contradicts the note's other novelty
statements. An unsuccessful search does not establish novelty, and the note
already says so.

## 2. Check of the mathematics, section by section

**Proposition 2.1 and Corollary 2.2.** Correct. The stage identity is one
line. Corollary 2.2(b) holds, including "only then" when all `kappa_t < 0`.
I re-derived the `alpha`BB reading.

**Section 2, "`Jt` has zero switch self-curvature".** Correct. `J` and `Jt`
transcribe the same continuous problem, so tangential families have
`b^T S_xx b -> kappa_tau`, and `Jt`'s stage residual has `u`-curvature
`h^2 (b^T S_xx b - kappa_t) -> 0`.

**Lemma 3.1.** Correct.

- The Gram part of `omega^T H omega` is `O(h^3 (j - i)) + O(h^4 (j - i)^2)`.
- The `l_1` part receives a contribution only at `t = j`.
- The toy formula `omega^T H omega = h^2 (h|i - j| - 2k)` follows from
  `H_ij`.
- An exact search for the `q < 0` toy at `N = 1000` found a KKT point with
  adjacent fractional stages 278 and 279. It is a saddle
  (`det H_FF / h^4 = -5.64`) and lies `4.613 h^2` above `f*`. This confirms
  the note's unlogged "4.6 `h^2`" (`logs/qneg_saddle.log`).

**Proposition 3.2.** Correct, using [W, Lemma 1.3]
(`sigma_{t+1} - sigma_t = h sigma_dot + h kappa (u_{t+1} - u_t) + ...`).

- For the toy this increment is exact:
  `sigma_{t+1} - sigma_t = -h (x_{t+1} - a_{t+1}) - h k (u_{t+1} - u_t)`.
- The remainder `h^2 (e_h + h)` should carry a factor `(j - i)`. This is
  harmless because `j - i <= 2C`.
- "No chattering at leading order" is correctly labelled a leading-order
  argument. Only single pair flips about `zbar` are treated, and additivity
  of several flips is plausible but not shown.

**Theorem 4.1.** Correct for LQ data.

- The first-order term telescopes to `h sigma^A_n omega` by the discrete
  adjoint. This holds for any anchor (the adjoint recursion holds for any
  control), provided the exit slope is `p^A_b`.
- The second-order term is `(h^2/2) omega^2 b^T V_{n+1} b`. `l_1` is affine
  and the controls after `n` are unchanged, so `l_1` adds no curvature.

**Corollary 4.2.** Correct within its class.

- Exactness at an interior optimum forces zero `x`-gradients and, backwards
  from the terminal term, slopes equal to `zbar`'s costates. This also holds
  through later windows, by the gradient of the window term with respect to
  its entry state.
- The class "`kappa`-limited, quadratic at the exit" is a real restriction.
  Families exact only over the boxes `D_t` are not covered by
  [W, Proposition D]. The note says this.

**Theorem 4.3.** The algebra is correct (leading order).

- Node loss: `max(0, (h^2/2)|kappa| w^2 - h^2 q delta w)`.
- Upper ratio: `rho_u = 1 + 2q/|kappa|`.
- Lower ratio: `B >= J - epsilon` gives
  `w <= [q delta + sqrt(q^2 delta^2 + q|kappa| delta^2 + kappa^2 w_0^2)]/|kappa|
  <= (rho* - 1) delta + w_0`.
- `rho* = 7.5526` for `q = 1.522`, `|kappa| = 0.5` (matches).
- Class restriction for (b): see F4.

**Lemmas 5.1–5.2 and Theorem 5.3.** Correct.

- The lifted-state reading checks out: the lifted stage residual equals
  `rho^v_t(x,u) - rho^v_t(z(v)_t)`, and `S_0(x_0, v) = J(z(v))`.
- Convexity of `loss_t(v)` over `R^n x U` holds as a supremum of affine
  functions. Over boxes it can fail when the `d`-range shifts with `v` (see
  F5.7).

**Theorem 5.4.** Correct for LQ data, given the zone argument of
[W, Theorem A]. I re-derived it, since [W] states the needed fact only as
the second bullet of its Section 6.

- For LQ data only `sigma_t(v)` depends on `v`. `K_t`, `beta_t` and
  `b^T P b` do not.
- (VM) with `c_0/2` absorbs the `o(1)` corrections.
- Stages at distance `>= C(h + e_h)` are handled by zone (ii).
- Stages nearer the switch have `|beta_t|^2/(h mu') = o(1)` when
  `e_h = o(sqrt h)`.
- The toys satisfy (VM) for every position of `ubar_n` (`gamma = 1.52 > 0.5`
  and `1.44 > 1`), but the rate `e_h` is not proved for them (target jump at
  `t = 1`).

**Remark 5.5.** Correctly labelled heuristic. A uniformity argument would
need compactness over the phase of `tau/h` as well as `h -> 0`.

**Section 6 (Theorems A_k, B_k, C_k).** Plausible; see F5.9. For B_k, the
disjointness of the windows (`(2K+1) h < ell/3`) and the summation over
windows under [R, Definition 1.1] are fine.

**Proposition 7.1.** Correct.

- `M_2 b = w_2` follows from `beta_2^T b = eta_2`.
- Backward Lyapunov comparison is valid with upward jumps inside the arc.
- The `O(ell)` expansion and the exact form for `A = 0` with constant
  `H_xx` are right.
- The Kelley reading via [SA, Proposition 1.3(b)] is right for constant `b`:
  `R = b^T H_xx b + b^T w_dot + 2 w^T A b`.
- For the toy, the jump in `k` lies outside (H1), as the note says. The
  necessity argument does not need smoothness in time.

**Section 7.1.** Correct (Rolle on the `C^2` middle arc). The
overlapping-window remark is a sketch, and is labelled as one.

**Section 8.**

- Proposition 8.1 is correct as stated: conditional on the rate, and with
  (SH_k) adapted to fixed endpoints, which is implicit.
- `P_{N-1} = h + |sigma_{N-1}|/h - 2k` is right (limit
  `P_N -> infinity`).
- The `N = 16000` remark of Section 9.4 is right, and more generally true.
  With `P' := P + k` and `sigma^k_t = sigma^0_t - k h u_t` at vertex stages,
  the recursion for `P'` and its start `P'_{N-1} = h + |sigma^0_{N-1}|/h`
  do not depend on `k` whenever the KKT points coincide, which they do
  when `u_n = 0`.

## 3. Numerical re-checks

All runs were single-threaded with `OMP_NUM_THREADS=1` and explicit
timeouts. My code (`vtoy.py`) was first validated (`logs/validate.log`): the
closed-form stage loss matches direct evaluation of the residual,
`dJ/du_t = h sigma_t` holds, and the Hessian formula matches second
differences. All gave 0 mismatches at `N = 40`, `k = 1/2` and `k = 1`.

| item | method | result |
|---|---|---|
| Section 5.3, `kappa = -0.5`, `N = 50, 100, 150, 200, 500, 1000, 2000, 4000, 8000` | exact, own code | all 9 rows reproduced (`zbar`, `n`, `ubar_n`, plain gap, `V`, outer bounds); all certified |
| Section 5.3, `kappa = -1`, `N = 200, 1000, 1001, 1002, 1003, 2000, 4000` | exact, own code | all 7 rows reproduced and certified |
| `V` end points | exact, `z(v)` rebuilt from scratch | largest loss exactly 0 at both ends on every row |
| outer nodes | exact | exact for their own optima (bound = anchor value) on every row; this was unlogged in the note |
| `q < 0` toy, `N = 200, 400, 1000, 2000` | exact, no calibration | `f*` = best single-switch vertex KKT point (5, 7, 1, 7 nodes) |
| `q < 0` toy, plain gaps | exact | 3.82, 6.06, 0, 1.766 `h^2` reproduced |
| Section 9.1, all nine `kappa = -0.5` grids with `N <= 2000` | exact, own box branch and bound | all certified (2–7 nodes); eight optima equal the author's `zbar`; the ninth equals the author's improved point |
| `(0.7, 1.3)`, `N = 2000`, documented instance | exact | different, bang-bang optimum; certified (9 nodes) (F2) |
| Section 9.2, 4 rows (own `tau`'s from `N = 16000`) | exact | failing-stage losses 1.0048, 0.1307, 0.2644, 0.0069 `h^3` reproduced; `K = 1` windows exactly 0 |
| Section 4, greedy counts | float, own code | `kappa = -0.5`, `N = 1000, 4000`: all reproduced; `kappa = -1`: equal wherever my greedy (no backtracking) completes, including `12 (13)` |
| author's `eps.json` | tally | 44 pairs, 42 equal, 2 off by one, as claimed |
| own partitions, `N = 1000` | exact | 6 and 11 nodes; worst exact bound `-0.95 epsilon` and `-0.90 epsilon`; cover without gaps |
| Section 9.3 table, 8 configurations × 4 `N` | float, own KKT and recursion | every tested row reproduced (same `s_1`, breaks, fractional stages) |
| Section 9.3, extra `N` up to 16000 | float | see F1 |
| Section 2 spectra (A−, A at `N = 100`) | float, own Hessian by second differences | reproduced |
| Section 2, toy `lambda_min(G)` | 40 digits | `≈ h^3/4` only (F5.1) |

The "`q < 0`, no calibration" route works as follows:

- every coordinate has `H_tt < 0`, so `f* = min` over vertices;
- `J = Jc - (k/2) h^2 sum u_t^2` with `Jc` strictly convex;
- branch and bound fixes coordinates to `±1`, and each node is bounded by
  an exact convex QP whose KKT point is checked exactly.

The smallest vertex-stage margins of the `q < 0` toy agree with the note at
`N = 200`; at `N = 400` see F5.5.

Not re-checked: Section 5.4 (A−, float, 72 s to 23 min per grid in the
author's runs); the "lifting cascade" of Section 7.2 (one-off, not logged);
the `row` table of Section 9.4 beyond the arithmetic of its plain gaps
(`0.25 * 1.90625^2 = 0.9084`, and likewise at `N = 1000, 2000, 4000`).

## 4. Requested changes (summary)

1. Rewrite the close-switch conclusions (Summary item 6, Sections 7.2 and
   9.3) as in F1. Add the `N`-sweep, or at least state that moderate
   negative `eta^X_1` gives phase-dependent breaks.
2. Fix or document the decimal-time data convention (F2), and say which
   instance each Section 9 number refers to.
3. State the convexity of the `kappa >= 0` two-switch toys and of the
   rising-`kappa` configurations, and lower their weight as evidence (F3).
4. Restore the qualifiers in Summary items 1, 2 and 6 (F4).
5. Make the wording fixes of F5. The most important are `≈ h^3/4`, "plus a
   linear term", the Remark 2.3 inequality, and the A− interval caveat.
6. Cite Wechsung–Schaber–Barton (2014) and reframe Theorem 4.3's
   cluster-problem comparison (F6).

## 5. Literature examined by the reviewer

- Local: `literature/papers/wechsung2014-the-cluster-problem-revisited`
  (abstract, Sections 1–3, conclusion read); `du1994-...` and
  `kannan2017-...` (presence and index entries); `adjiman1998-...` (presence).
- Cited notes read at the relevant places: [W] Sections 0–6 (Lemma 1.3,
  Theorems A–C, Propositions D–E, Section 6); [E] Sections 0–2.5, Lemma 10,
  Corollary 11, Theorem 9; [R] Definition 1.1, Remark 1.4, Theorem 4.1;
  [SA] Proposition 1.3.
- No web searches were made by the reviewer.

## 6. Commands run (targeted only)

All commands were run from `reviews/kappa-negative-review-checks/` with
`OMP_NUM_THREADS=1`. No project-wide verification was run, CI was not
inspected, and nothing was committed. Background runs used `timeout`; no
process was killed by pattern.

1. `python3 v_single.py validate` → `logs/validate.log`.
2. `python3 v_single.py cert 1/2 50 100 150 200 500 1000 2000` →
   `logs/cert_k05_small.log`; `cert 1/2 4000 8000` →
   `logs/cert_k05_large.log` (450 s and 1536 s); `cert 1 200 1000 1001 1002
   1003 2000 4000` → `logs/cert_k1.log`.
3. `python3 v_qneg.py 200 400 1000 2000` → `logs/qneg.log`;
   `python3 v_qneg_saddle.py` → `logs/qneg_saddle.log`.
4. `python3 v_two.py 1/2 7/10 13/10 2000 597 778` →
   `logs/two_07_13_N2000.log` (documented instance; scan only).
   `python3 v_two_compare.py` → `logs/two_compare.log`. Both compare the
   documented instance with the author's points. These are superseded for
   the author's instance by the next items.
5. A one-off check of the author's `ktoy.data` at decimal jump times (the
   only import of author code; the output is quoted in F2).
6. `python3 v_two.py 1/2 f:0.7 f:1.3 2000 597 778` →
   `logs/two_07_13_N2000_authorconv.log`. This uses 1-D branching on `u_597`
   only. It does not close the outer range: there stage 778 loses about
   `0.3 h^2`. It is a negative result and is kept.
7. `python3 v_two_bb.py 1/2 f:0.7 f:1.3 2000 597 0 778 -1` →
   `logs/two_bb_07_13_N2000.log`; `python3 v_two_all.py` →
   `logs/two_all.log`; `python3 v_two_bb.py 1/2 7/10 13/10 2000 597 1 777
   -1` → `logs/two_bb_documented_instance.log`.
8. `python3 v_kink.py ...` (4 configurations) → `logs/kink.log`.
9. `python3 v_eps.py 0.5 1000 4000` and `v_eps.py 1.0 1001 1002 4002` →
   `logs/eps_k05.log`, `logs/eps_k1.log`; `python3 v_epsexact.py` →
   `logs/epsexact.log`.
10. `python3 v_close.py` → `logs/close.log`; `v_close_profile.py` →
    `logs/close_profile.log`; `v_close_sweep.py ...` →
    `logs/close_sweep.log`; `v_close_sweep2.py` (4 configurations) →
    `logs/close_sweep2.log`.
11. `python3 v_spectra.py` → `logs/spectra.log`; `python3 v_convexity.py` →
    `logs/convexity.log`.
