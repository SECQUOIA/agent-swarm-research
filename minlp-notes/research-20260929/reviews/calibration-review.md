# Referee report: discrete calibrations for transcribed optimal-control problems

Date: 2026-09-30. Note under review:
[`../theory-calibration/scouting.md`](../theory-calibration/scouting.md) and
[`../theory-calibration/doublewell_calibration.py`](../theory-calibration/doublewell_calibration.py).
Context read: `open-instances-summary.md`; the consistency note [K]
(Theorems 1.1, 2.1, 3.1, Propositions 1.3, 3.3, Lemmas 4.1–4.2, Section 5.1);
the open-instances report at the optcdeg2, lukvle10, dtoc5 and camshape passages that
the dictionary cites; Hager (2000) and Dontchev–Hager (2001), read in full at the
cited theorems. Independent checks are in
[`calibration-review-checks/`](calibration-review-checks/) (scripts `c1`–`c5`, logs
in `logs/`). I did not edit the note and did not commit anything.

## Verdict summary

| # | Claim | Verdict |
|---|---|---|
| 1a | Exact calibrations lie in the band `f* - Gamma_t <= S_t <= V_t` | **correct** |
| 1b | [K]'s gap identities "transfer verbatim"; pinch regularity; the tangent plane as the exactness test | **correct with fixes** (F1–F3). One sentence is false as worded: per-separator band membership of the tangent plane is not sufficient (F3, counterexample c5) |
| 2a | Thm 3.1: affine bound = Lagrangian dual; exactness iff all residuals minimal on the trajectory; slopes = costates | **correct** (small fix F4) |
| 2b | Thm 3.3: mesh-uniform exactness of costate calibrations (Euler); necessity in the limit | **correct with fixes** (F5, F6). SGM is the pointwise **Leitmann–Stalford (1971)** condition, which the note does not cite |
| 2c | Runge–Kutta and trapezoid remark | **sketch; the algebra is right, the cited convergence theorem does not apply as stated** (F7) |
| 3a | Thm 3.4: local quadratic calibrations ⇔ Riccati ⇔ SOSC | **correct** (classical) |
| 3b | Thm 3.5: global LQ comparison | **correct**. However, it is exactly convexity of the condensed problem, so the novelty claim should be dropped (F8) |
| 4 | Example 3.6 numbers | **reproduced**, both bit for bit and by independent code; the interpretation needs F8 and small fixes (F15) |
| 5a | Prop 4.1 (singular stages) | **correct**; the "positive gap" consequence needs dual attainment (F4) |
| 5b | Prop 4.2 (switch window of fixed duration) | **inequality correct**; the `Theta(1/h)`-stage conclusion is a corollary that needs stated assumptions (F18) |
| 6 | Thm 5.2 (transfer) | **correct with fixes** (F10–F14). A hypothesis is missing: `r = 0` on an admissible `(x*,u*)`. Compactness of `U` is essential (counterexample c2-A). The `O(h)` rate is not needed. Verified numerically on a nonconvex example |
| 7 | Novelty | **overstated for Thm 3.3 and Thm 3.5** (F5, F8). **Thm 5.2 and Props 4.1–4.2: no prior statement found**; they are elementary |

No central claim is false. The fixes concern missing hypotheses, one misleading
characterization (F3), citations (Leitmann–Stalford; the Hager/Dontchev–Hager
scopes), and the reading of Theorem 3.5 and Example 3.6.

## 1. Discrete calibrations, the band, and the carry-over from [K]

**Lemma 2.1, Lemma 2.2, Definition 2.2: correct.** I checked the telescoping step, the
subsolution normalization, and the DP inequality. Lemma 2.2(1) needs `V_t` finite on the
`x`-section, and the exact-projection hypothesis gives that. Max-closure is correct.

**Band membership (Section 2.3): correct.** In subsolution form, telescoping a
feasible tail gives `S_t <= V_t` on states that have a feasible tail. The
inequalities `rho_s >= 0` along a feasible head give `S_t >= f* - Gamma_t` on
reachable states. Both edges are extended-valued: `V_t = +inf` where no feasible tail
exists and `Gamma_t = +inf` off the reachable set.

**F1 (domains).** Two things change when [K] is carried over to transcriptions.

- In `B(S)`, `S_{t+1}` is evaluated on `f_t(Omega_t)`, which need not lie in the
  `x`-section `D_{t+1}` of `Omega_{t+1}`. The separator domain for `S_t` is
  `D_t ∪ f_{t-1}(Omega_{t-1})`, and the band edges are `±inf` on parts of it.
- [K, Theorem 2.1] assumes one common box `X_S` and bounded `U`, `V`. Its proof uses
  only `sup(L - U) <= 0` (true because `f* = inf(V_t + Gamma_t)`) and clipping, and
  both work with extended values. So the one-separator identity
  `gap = 2 dist_inf(Phi_t, Band_t)` carries over, provided `f*` is finite. The
  whole-horizon upper bound of [K, Theorem 3.1] uses sup-norm distances over these
  sets. On unbounded domains it is typically `+inf`; in Example 3.6 affine and
  quadratic band elements differ unboundedly. Only the lower bound stays informative.
- "Transfer verbatim" should be replaced by these two sentences.

**F2 (pinch regularity).** [K, Lemma 4.2] needs `V_t` semiconcave and `Gamma_t`
semiconcave near the pinch. [K, Lemma 4.1] proves this only for product domains, and
[K] warns that constraints tying private variables to the separator create convex
kinks. Dynamics are such constraints:

- `Gamma_{t+1}(y)` is an infimum over the fiber `f_t(x,u) = y`;
- `V_t` involves `f_t(x,u) ∈ D_{t+1}`.

Semiconcavity holds locally in the smooth interior case. For example, with Euler at
small `h` the map `x -> x + h g(x,u)` is a diffeomorphism, and with Lipschitz value
functions and interior optimal controls the argument goes through. That case must be
stated as a hypothesis; "with semiconcave data" is not enough.

**F3 (false as worded).** Section 2.3 says: "Exactness of the affine class is the
global question whether this tangent plane stays inside the band (Theorem 3.1)."
Tangent-plane band membership at each separator is **necessary but not sufficient**.
Counterexample (`c5_band_not_sufficient.py`), a path `a(s1), b(s1,s2), c(s2)` on
`[-1,1]^2`:

- data: `a = 10 s1^2`, `c = 10 s2^2`, `b = -5 exp(-|s - (0.8,0.8)|^2/0.01)`;
- `f* = 0` at the interior origin, and the costate slopes are forced to 0
  (Theorem 3.1(3));
- the constant 0 lies in both bands, yet the costate family gives bound `-5`, a gap of 5;
- the dip of `b` is hidden in each one-sided value function by `a` or `c`.

This is [K, Proposition 3.3] again. The joint condition is Theorem 3.1(2).

**Riccati band (Section 2.3, last bullet).** Plausible and labelled informally. With
the unperturbed backward Riccati solution, the residual Hessians have zero Schur
complement, so they are only PSD. Theorem 3.4 therefore needs the `eps`-perturbation,
as the note does in its proof.

## 2. Affine class

**Theorem 3.1: correct.** I rederived the Lagrangian identity. Two points:

- `B(p)` also dualizes the copy `x_0 ∈ X_0` against the `x`-section of `Omega_0`. With
  `x_0` fixed this is immaterial.
- **F4.** The "only if" in (2) needs `f*` to be attained. Without a minimizer, an exact
  calibration does not produce a trajectory that minimizes the residuals. The same
  issue affects the consequence of Proposition 4.1: "no exact affine calibration" is
  proved, but "the affine class has a positive gap" also needs the dual supremum to be
  attained. [K, Proposition 1.2]'s attainment argument uses identically-zero sums of
  directions, and that fails with dynamics rows. State "no exact affine calibration"
  or prove attainment.

**Theorem 3.2: correct** (classical).

**Theorem 3.3: correct with fixes.**

- The residual identity `rho_t = h[H(.,.,p_{t+1}) - q_t^T x]` holds, with
  `q_t = grad_x H(x^h_t,u^h_t,p^h_{t+1})` from the discrete adjoint. `D` is an
  enclosure, not a constraint, so it carries no multipliers.
- In (2) I checked the constant `K = G + L_H R_D` and the far/near split. The far
  region, distance `>= delta` with `e_h <= delta/2`, gives
  `c delta^2/4 - (2K+L) e_h > 0`. The near ball lies in `B_{2 delta}` and is handled by
  convexity plus the first-order condition.
- Only `e_h -> 0` is used, with no rate.
- **F5 (attribution).** SGM is the pointwise **Leitmann–Stalford** sufficient condition
  (G. Leitmann, H. Stalford, *A sufficiency theorem for optimal control*, JOTA 8
  (1971) 169–174, doi 10.1007/BF00932465): `(x*,u*)` optimizes the augmented
  Hamiltonian `H + psidot^T x`, which is `H - grad_x H*^T x` along the adjoint. I
  confirmed the form from a restatement in Goenka–Liu–Nguyen, *SIR economic
  epidemiological models with disease induced mortality* (J. Math. Econ. 2021; WP
  version, Assumption 6 and footnote 26). The original is paywalled.
  - The note calls SGM "the stage-wise global Mangasarian condition" and says "the
    standard continuous proof uses only SGM". That is the Leitmann–Stalford theorem and
    should be cited as such. It is also in Seierstad–Sydsæter's treatment.
  - The discrete counterpart (Theorem 3.1(2) with affine `S`) is Tamminen's "Lagrangian
    minimized in state and control", already cited.
  - What remains new is only the mesh-uniform perturbation statement.
- **F6.**
  - The Summary's "or more generally if a strict pointwise condition (SGM) holds" omits
    the local-convexity hypothesis of (2). It is automatic when `x*(t)`, `u*(t)` are
    interior: strict SGM gives `grad^2 H >= 2cI` at `z*`, and continuity does the rest.
    It is a real extra hypothesis when `u*(t) ∈ ∂U`. Say so.
  - In (3), "at every `t`" should read "at every continuity point of `u*` (one-sided
    limits otherwise)".
  - In (3), "exact" should mean exact on `(x^h,u^h)`.
- **Numerical sanity check** (`c1`, double well with `xi = 1.3`, trajectory outside the
  concave region, `min x = 1.068 > 1`): the costate-affine gap is `<= 2.2e-16` at
  `N = 50, 200, 1000`, as (2) predicts. With `xi = 0.3`, SGM fails and the gap is
  2.8–2.9.

**F7 (Runge–Kutta remark: sketch; citation wrong in scope).** The algebra is correct.
Dualizing stages and update gives `psi_k = psi_{k+1} + sum_i lambda_i` and
`chi_i = psi_{k+1} + sum_j a_ji lambda_j / b_i`, which match Hager's (15), (18), (19).
The node terms have the Euler form, with `b_i > 0` giving the right sign. The trapezoid
node terms at the averaged costate are also correct. However:

- Hager's Theorem 2.1 assumes **`U = R^m`**, a Mayer cost, and a scheme of **order
  `kappa >= 2`**, so it does not cover Euler.
- It bounds the Hamiltonian minimizer `u(x^h_k, psi^h_k)`, **not the stage controls
  `u_{ki}`** (Hager's Remark 2.2: those may converge more slowly).
- The RK version of (A3) needs uniform convergence of the stage values
  `(Y_i, U_i, chi_i)`, which Theorem 2.1 does not state.
- With control bounds, Hager's Theorem 7.2 (second-order schemes, `0 <= c_i <= 1`) or
  Dontchev–Hager–Veliov (SINUM 2000) apply.
- Label the remark "sketch" in the Summary too, where it currently reads "by the same
  computation". Section 1.3's description of Hager's theorem should add "`U = R^m`,
  order `>= 2`".
- For Euler, the `O(h)` `L^inf` estimate with control constraints is Dontchev–Hager,
  SICON 31 (1993) 569–603. Dontchev–Hager, Math. Comp. 70 (2001) treats state
  constraints and gives only `O(h^{2/3})` in `L^inf`.

## 3. Quadratic class

**Theorem 3.4: correct** (classical in substance, as stated).

- I checked (1⇒2) (tail PD, DP step, pivot = Hessian after partial minimization).
- I checked (2⇒3): the perturbed data form an open set; `K_t - eps I` has a PD `uu` block
  and zero Schur complement, so it is PSD; terminal `eps I`.
- I checked (3⇒1): telescoping gives quadratic growth, and LICQ holds because the
  Jacobian contains `-I`. The accessory form can also be read off directly as the sum
  of residual Hessian forms.

**Theorem 3.5: correct, but it is convexity of the condensed problem (F8).** With
affine dynamics:

- the reduced objective `J(u)` has Hessian `sum_t z_t^T grad^2 L_t z_t + xi_N^T grad^2 Phi xi_N`
  along linearized (here exact) trajectories;
- this is at least the comparison LQ form, which is PD iff the comparison Riccati
  recursion is well defined with PD pivots (Theorem 3.4, 1⇔2, applied to `(A,B,M,Qh_N)`);
- the feasible set in `u` is convex;
- so the hypotheses of Theorem 3.5 are exactly a certificate that the condensed
  problem is strictly convex. "Every KKT point is a global minimizer" is then
  immediate, and the quadratic `S` is the DP form of that certificate.

Numerically (`c1`), the critical `a` at which the unperturbed discrete Riccati
recursion first fails equals the critical `a` at which the reduced-Hessian lower bound
`(2/h)D^T D - 2ah E` loses definiteness, to about `1e-10`:

| `N` | critical `a` |
|---|---|
| 50 | 2.51729 |
| 200 | 2.47977 |
| 1000 | 2.46987 |
| 5000 | 2.46789 |

The limit is `pi^2/4 = 2.46740`. The equivalence of Riccati pivots with a PD reduced
Hessian is standard in structured QP and MPC practice (Rao–Wright–Rawlings 1998; HPIPM
states that the classical Riccati recursion requires a PD reduced Hessian). Rephrase
the novelty item as "the calibration (DP) form of a hidden-convexity certificate". The
"Scope" paragraph is right that it strictly extends Theorem 3.2(1) for affine
dynamics. The interval-Hessian extension to nonlinear `f_t` is valid as a sufficient
check.

## 4. Example 3.6 (double well)

**Reproduced.**

- `c0`: rerunning `doublewell_calibration.py` gives output identical to the stored log
  (max abs difference 0 in `J` and all gaps). Runtime is 5 min 34 s single-threaded, not
  "about 1 minute".
- `c1` is independent code, with different KKT solver, stage minimization, and bounds.

| quantity | `a = 2` | `a = 2.4` | `a = 3` |
|---|---|---|---|
| `J` (identical to the note to 1e-16) | −0.32470 … −0.32991 | −0.46454 … −0.47321 | −0.74743 … −0.76318 |
| costate-affine gap, `N = 50 … 5000` | 2.813, 2.850, 2.860, 2.862 | 3.991, 4.038, 4.051, 4.053 | 6.041, 6.104, 6.120, 6.123 |
| best affine gap (closed form; `B(0)` equals it to `<= 9e-16`; random `p` stay below) | 0.6587 … 0.6699 | 0.9508 … 0.9665 | 1.463 … 1.486 |
| quadratic: min stage-Hessian bound / `h` | `1.000e-3` | `1.000e-3` | Riccati fails at `t/N` = 0.080, 0.090, 0.093, 0.0934 |
| `lambda_min` of reduced-Hessian lower bound | `> 0` (`1.9e-4` at 5000) | `> 0` (`2.7e-5` at 5000) | `< 0` |

- The argument that the best affine bound is exact is correct: weak duality against the
  per-stage convexified problem, whose value is attained by the constant path because
  `vex w` is flat on `|x| <= sqrt(a/2b)`. It needs `|xi| <= sqrt(a/(2b))` (true for
  `xi = 0.3`); add this.
- The residual gradients at the trajectory are `<= 2.3e-16`, and the stage Hessians are
  bounded below by constant PD matrices. So the quadratic bound equals `J` up to
  rounding, as reported.

**Interpretation (F8, F15).**

- For `a < pi^2/4` the transcription is a convex problem after condensing, so its KKT
  point is unique and global; no calibration is needed to see this. The example shows
  that the per-stage (affine) class cannot see hidden convexity. It is not an instance
  of certifying a genuinely nonconvex problem. Say this next to the table.
- "The costate-affine gap is about 2.9" should read 2.81–2.86 for `a = 2`.
- "Exact up to the conjugate point `a T^2 = pi^2/4`" holds only in the limit; at finite
  `N` the discrete threshold lies above `pi^2/4` (2.517 at `N = 50`).
- The script docstring says "Example 3.9".

## 5. Failure modes

**Proposition 4.1: correct.** The argument is elementary: an affine residual in `u`
minimized at an interior point gives `sigma = 0`, so `x̄` minimizes `rho(., u)` for
every `u`, and subtraction does the rest. F4 applies to the "positive gap" consequence.
The `x^2`, `|u| <= 1` example is a correct non-overreach check.

**Proposition 4.2: the inequality is correct.** I redid the one-dimensional
minimization: `s* = Delta|grad sigma|/(Lambda + Delta M_s)` gives the stated bound. The
`h`-scaling is also correct, since all of `sigma`, `Lambda`, `M_s` carry a factor `h`
and so do `s*` and the threshold. **F18.** The conclusion "fails on a window of fixed
duration, hence `Theta(1/h)` stages" additionally needs:

- `grad_x sigmatilde` bounded away from 0 near the switch;
- uniform convergence of discrete states and costates near the switch, so that the
  discrete switching function is `gamma|t - t_s| + o(1)`; for bang-bang problems this
  is Alt–Baier–Gerdts–Lempio / Veliov-type theory, not (A3);
- interior states;
- uniqueness of slopes (Theorem 3.1(3)), so that the statement covers all affine
  calibrations, not only costate ones.

State it as a corollary under these assumptions. optcdeg2's failing head window
(3092 stages, ending at the switch) is consistent with it.

**F17 (Section 4.3).** "Convex pure state constraints are harmless" holds for
Theorem 3.2. For Theorem 3.3 it is unproved:

- discrete multipliers `nu_t = O(1)` at junctions make `q_t = O(1/h)`;
- the extra term is minimized at `x^h_t` over convex `D`, which helps;
- but an SGM with measure multipliers and the corresponding convergence theory (only
  `O(h^{2/3})` in `L^inf`, Dontchev–Hager 2001) would be needed.

## 6. Theorem 5.2 (transfer)

I checked every step.

- **Step 1** is **not implied by (T2) as written (F10).** (T2) gives
  `r >= c|z - z*(t)|^2`, which at `z*` gives only `r >= 0`. Step 1 needs
  `r(t, x*(t), u*(t)) = 0` and `xdot* = g(x*, u*)`, `x*(0) = xi`: the adjoint equation
  uses `xdot* = g`. Add "`(x*, u*)` is admissible and `r` vanishes on it", that is, `S`
  is an exact (not merely strict) calibration.
- **Steps 2–6: correct.**
  - Step 2: the Taylor identity gives `a_{t+1} - a_t = O(h^2)`.
  - Step 3: the residual formula has the right signs.
  - `R_2` is `C^2` because `S in C^4` and `g in C^2`.
  - Step 4, far region: `hc(delta - Kh)^2 - C_1 h^3 - C_2 h^2 delta > 0` for
    `delta >= M_0 h`.
  - Step 5, near region: zero gradient at `z^h` because `grad S^h_t(x^h_t) = p^h_t`;
    Hessian `>= h(2c - o(1))`.
  - Step 6: the terminal gradient is `a_N = grad(Phi - S(T,.))(x^h_N)`; uniqueness
    holds.
  - Constants are uniform because `[0,T] x D x U` is compact, and `D' ⊃ D + h_0 G B_1`
    handles `x + hg ∉ D`.
  - The proof also works for time-dependent `l`, which I used below.

**What "strict" means.** (T2) is uniform quadratic growth of the HJ residual on the
compact `D x U`. Equivalently, `r(t,.) > 0` off `z*(t)` uniformly in `t`, together with
`grad^2 r(t, z*(t)) >= 2cI`. **It implies the coercivity of Hager and Dontchev–Hager**,
which the note left unchecked. Along linearized pairs `(xi, eta)` with `xi(0) = 0`,
`d/dt[xi^T S_xx(t,x*) xi]` accounts exactly for `grad^2 r - grad^2 H`. Hence

```
Q_H(xi,eta) = int zeta^T grad^2 r(t,z*) zeta dt + xi(T)^T grad^2(Phi - S(T,.)) xi(T) >= 2c ||eta||^2_{L2}.
```

**F12 (rate not needed; citations).** Replace `h` by `eta_h = e_h + h` in the proof:

- `a_t = O(e_h)` and `a_{t+1} - a_t = O(h eta_h)`;
- `h r(z^h) = O(h e_h^2)`;
- the far region then holds for `delta >= M_0 eta_h`.

So uniform convergence `e_h -> 0` suffices. The rate is irrelevant, which also matters
for RK stage controls and state-constrained estimates. For Euler with interior controls,
Dontchev–Hager (SICON 1993) supplies (T3) given the coercivity above. I did not check
their remaining smoothness hypotheses in detail. Hager 2000, Theorem 2.1 does not cover
Euler (F7).

**F11 (compactness is essential; counterexample).** Take
`min int_0^T (u^2/2 + x^6 + x^2) dt + Phi(x(T))` with `Phi(x) = x^2/2 - x^4/4`,
`xdot = u`, `x(0) = 0`, `u ∈ R`.

- `S = -x^4/4` is a `C^inf` strict calibration on all of `R x R`:
  `r = (u - x^3)^2/2 + x^6/2 + x^2 >= (x^2 + u^2)/4` (grid ratio `>= 0.2526`), and
  `Phi - S(T,.) = x^2/2`. The continuous optimum is `0`, unique.
- `(x,u,p) = 0` is an exact discrete KKT point with `a_t = 0`.
- **For every `h` the Euler transcription is unbounded below.** One last step to `X`
  costs `X^2/(2h) + X^2/2 - X^4/4`; at `X = 1000` this is `<= -2.5e11` for
  `h = 0.1, 0.01, 0.001` (`c2`, Part A). The last-stage residual is unbounded below.

So on unbounded control sets a strict continuous calibration says nothing about the
transcription. This is the "negative far from the trajectory for all `h`" failure;
(T1) excludes it. Consequences:

- Example 3.6 (free `u`) and the attack plan's first test are **outside** Theorem 5.2
  as stated. They work only because the comparison calibration is quadratic and `g` is
  affine.
- An unbounded-domain version needs a growth condition, for example
  `sup |D^2 S|(1 + |g|)^2 = o(r/h)`.

**F13 (Proposition 5.1 and Summary item 5).** "Sampling `S` without the correction
loses `O(h)`" is an upper bound. In the strict setting of Theorem 5.2 the uncorrected
family's gap to the discrete optimum is **`O(h^2)`**:

- the correction removes a residual gradient of `O(h^2)` against curvature `~ch`,
  which costs `O(h^3)` per stage;
- the terminal term costs `O(h^2)`.

Measured (`c2`, Part B): 0.0237, 0.0061, 0.00157, 0.00040, 0.00010 for
`N = 10 … 160`. The `O(h)` rate is attained only for non-strict `S` (below).

**Positive test, genuinely nonconvex (`c2`, Part B).** The problem is
reverse-engineered:

- `S = sin(2x+t) + 0.3x^3`;
- `(x*,u*) = (0.2 + 0.4 sin 2t, 0.8 cos 2t)`;
- `r = (u-u*)^2(1 + 0.5 sin 5x) + (x-x*)^2(1.2 + sin 4(x-x*))`, nonconvex, `c = 0.2`;
- `l = r - S_t - S_x u`, `Phi = S(T,.) + (x - x*(T))^2(1 + 0.3 sin 7x)`;
- `U = [-2, 2]`.

Every stage residual was minimized globally by a dense grid plus local polish.

| `N` | 5 | 10 | 20 | 40 | 80 | 160 |
|---|---|---|---|---|---|---|
| transferred family gap | 0.084 | 0.0021 | 2e-15 | 3e-15 | 7e-15 | 7e-15 |
| costate-affine gap | 8.66 | 8.77 | 8.71 | 8.66 | 8.63 | 8.62 |
| (T3) error / `h` | 3.6 | 3.4 | 3.3 | 3.2 | 3.2 | 3.2 |

`max|a_{t+1} - a_t|/h^2 ≈ 5.6` at every `N`, as step 2 predicts. So the theorem
certifies a nonconvex transcription where costate calibrations fail, with
`h_0 ∈ (0.05, 0.1)` here.

**Strictness in `x` is needed (`c3`, `c4`).** For scalar LQ, `V = P x^2/2` (a field,
`r = 0` on every field trajectory), the transferred residual minimized over `u` has
curvature `(F(P(t+h)) - P(t))/2` in `x`. This is negative, of order `-h^2`, for
`xdot = x + u, l = (u^2+x^2)/2` and for `xdot = ±2x + u, Phi = x^2/2`. The transferred
field calibration then has gap `Theta(h)` for every `h`: 0.191, 0.102, 0.053, 0.027,
0.013, 0.0067 for `N = 10 … 320`. It is exact only when the sign happens to be favorable,
as for `xdot = u`.

**F14 (tilting remark).** The note says to tilt by `-eps e^{-lambda t}|x - x*|^2` with
`lambda` large. The tilt works (`c4b`): the tilted family is exact, with gap
`<= 7e-14` at `N = 40 … 2560`, while the untilted gap stays `Theta(h)`. But:

- `lambda` must exceed a problem-dependent threshold; for `xdot = alpha x + u` it is
  `lambda > 2 alpha - 2P + 2 eps'`;
- the strictness constant is about `eps e^{-lambda T}`, and `h_0` scales with it;
- with `lambda = 8` (constant `1.7e-4`) the family is not yet exact at `N = 320`, with
  gap 1.6e-3.

"`lambda` large" should read "`lambda` above the threshold, and not larger, since
`h_0 ~ c`". The attack plan's "explicit constants" item is therefore essential for
practical use.

**Scope items the note already states correctly:** `x_N` free only; no state or
terminal constraints (`D` is an enclosure); interior optimal controls. "Rigorous
checking with `O(log(1/h))` boxes per stage" is plausible and labelled a sketch. With a
floating-point KKT point, the certificate gives `f* >= J - tiny`, not exact equality.

## 7. Novelty

- **Discrete calibrations, Theorems 3.1, 3.2, 3.4:** classical, as the note says.
- **Theorem 3.3 (F5):** the pointwise condition is Leitmann–Stalford (1971). The
  discrete global form is Tamminen (2019) and discrete Krotov. What remains is the
  elementary mesh-uniform perturbation statement: modest, not found stated.
- **Theorem 3.5 (F8):** convexity of the condensed problem, certified by a Riccati
  factorization of the reduced-Hessian lower bound. Known in substance; drop it from the
  novelty list or restate it as a reading.
- **Propositions 4.1–4.2:** not found stated; elementary. Reasonable as "observations".
- **Theorem 5.2:** my searches found no statement that a strict continuous calibration
  plus convergent discrete KKT points yields global optimality of fine transcriptions.
  The searches covered:
  - Krotov discrete conditions and the Irkutsk "canonical" discrete theory (Sorokin
    2014, 2017);
  - Hager 2000; Dontchev–Hager 1993/2001;
  - Malanowski–Büskens–Maurer and Mittelmann-type discrete SSC, which are all local;
  - Ohsawa–Bloch–Leok discrete HJ theory.

  The closest related text is Abhijeet et al., *Convexity in optimal control problems*
  (arXiv:2404.08621, 2024). It asserts global uniqueness from strict convexity of `H`
  in `u`, which conjugate points contradict (Example 3.6 at `a = 3`), and it reports
  spurious optima under coarse discretization, but it proves no transfer. Theorem 5.2
  looks new; its proof is short (a Taylor expansion plus stability of a strict minimum),
  and with F10–F12 it is correct. The claim "the one result with potential practical
  weight" is fair, with two caveats: strict smooth global calibrations are rare outside
  constructed or LQ-like cases, and `h_0` can be small (F14).

## Minor

- Proposition 3.7: "Theorem 3.3 gives `c_stage` = one convex program" holds only in case
  (1). In the SGM case the stage problems are nonconvex (F9).
- Proposition 2.3 remark: replacing computed ray values by concave minorants yields a
  calibration only if done backward, stage by stage, since lowering `W_i` can break
  `W_{i-1}(r_j) <= W_i(M r_j)`. The loss accumulates over stages (F16).
- Section 2.2 dual: the min is attained under [K, Theorem 1.1]'s compactness and
  continuity; state them.
- The dictionary spot checks agree with the open-instances report: optcdeg2 concave
  windows `t < 3092` and `t >= 47290`, head `m = 3080`, tail gap 6.1e-3; dtoc5
  `lambda_t < 1/4`; lukvle10 last three pairs; camshape `U_m(c/2) >= 0` for `m <= n-1`.

## Commands run (targeted only; no project-wide verification, no CI)

All in `reviews/calibration-review-checks/`:

- `OMP_NUM_THREADS=1 python3 ../../theory-calibration/doublewell_calibration.py`
  → `logs/c0_original_rerun.{log,json}`; 5 min 34 s; identical to the stored log.
- `OMP_NUM_THREADS=4 python3 c1_doublewell_independent.py` → `logs/c1_*` (1 min).
- `OMP_NUM_THREADS=4 python3 c2_transfer_theorem.py` → `logs/c2_*` (Parts A–C, 1 min).
- `python3 c3_nonstrict_lq_sign.py`, `python3 c4_nonstrict_lq_gap.py`,
  `python3 c4b_tilted_small_lambda.py`, `python3 c5_band_not_sufficient.py`
  → `logs/c3_*`, `logs/c4_*`, `logs/c4b_*`, `logs/c5_*`.
- Literature:
  - Hager (2000) PDF and Dontchev–Hager (2001) PDF converted with `pdftotext` in
    `/tmp` and read at Theorems 2.1 and 7.2 and the introduction.
  - Leitmann–Stalford metadata via the Crossref/OpenAlex APIs; its statement via the
    restatement in Goenka–Liu–Nguyen (Birmingham WP 20-25).
  - Web searches as listed in Sources.

These are local targeted checks, not CI results.

## Sources

- Leitmann–Stalford 1971: https://doi.org/10.1007/BF00932465
- Goenka–Liu–Nguyen (restatement of Leitmann–Stalford): https://repec.cal.bham.ac.uk/pdf/20-25.pdf
- Hager 2000: https://people.clas.ufl.edu/hager/files/rk.pdf
- Dontchev–Hager 2001: https://people.clas.ufl.edu/hager/files/discrete.pdf ; https://www.ams.org/mcom/2001-70-233/S0025-5718-00-01184-4/
- Tamminen 2019: https://www.esaim-cocv.org/10.1051/cocv/2018012
- Sorokin 2014: https://mathnet.ru/eng/at14117 ; Sorokin 2017: https://m.math-net.ru/eng/iigum296
- HPIPM (Riccati and reduced Hessian): https://arxiv.org/pdf/2003.02547
- Abhijeet et al. 2024: https://arxiv.org/abs/2404.08621
