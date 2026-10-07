# Calibrations along singular arcs: tangency on the whole arc, Kelley's condition, and what discretization does

Date: 2026-09-30. Status: **revised after three independent reviews**
(`reviews/singular-arcs-review.md`, findings F1–F6;
`reviews/singular-arcs-confirm-r1.md`, items R1–R7;
`reviews/singular-arcs-confirm-r2.md`, items S1–S2); the third revision
was confirmed by `reviews/singular-arcs-confirm-r3.md` (verdict: verified;
two optional nits, no fix required). Sections 9, 10 and 11
list every change and how I checked it. Proofs are complete unless labelled "sketch",
"heuristic" or "conjecture". Numbers are floating-point screening unless
marked "exact" (rational arithmetic) or "symbolic" (sympy, exact).

Cited notes:

- **[R]** `theory-bangbang/report.md` (window law, Proposition 3.1, Lemma 2.1,
  Theorem 2.3, Theorem 4.1);
- **[E]** `theory-bangbang/extension-n2.md` (layer condition `η_L`,
  Lemma 10, the maximal recursion);
- **[S]** `theory-calibration/scouting.md` (Proposition 4.1, Sketch 4.5);
- **[C]** `open-instances-wave2/cops/report.md` (catmix DP certificate);
- **[CV]** `reviews/cops-verification/verification-report.md` and
  **[CR]** `reviews/catmix-recheck.md` (independent checks of [C]).

Scripts and logs: `theory-bangbang/singular/` and
`theory-bangbang/singular/logs/`.

## Summary

The question ([R, Section 6]; [S, Sketch 4.5]) was what calibrations can
do along singular arcs of control-affine problems with a scalar control.
[R] expected that tangency `Pb = w` along the whole arc would fix `bᵀṖb`
and "presumably reproduce the Kelley/Goh conditions".

**Continuous time (Section 1–2).**

1. *Tangency on the whole arc.* A calibration that is `C²` in the state and
   exact on a singular arc (interior control, interior state, residual
   `r ≥ 0` nearby) has `S_xx b = w` at every point of the arc
   (Proposition 1.1). This is the continuous twin of [S, Proposition 4.1]
   and of [R, Proposition 3.1], now on a whole interval instead of one
   switching time.
2. *Goh.* With several controls, tangency reads `PB = W`, so `BᵀW` must be
   symmetric. `BᵀW − WᵀB` equals the matrix `∂σ̇_i/∂u_j`, so this is
   exactly Goh's necessary condition (Corollary 1.2). For a scalar control
   it is empty.
3. *Kelley.* With `P = S_xx` along the arc, the Hessian of the residual at
   the singular control is `M = Ṗ + g_xᵀP + Pg_x + H_xx`, and
   `bᵀMb = −∂_u σ̈`, the generalized Legendre–Clebsch (Kelley) quantity
   (Proposition 1.3; hand proof, plus an exact symbolic check). So every
   such calibration satisfies Kelley's condition `−∂_uσ̈ ≥ 0`, and strict
   ones satisfy it strictly. In second-variation language, tangency removes
   the `δu` terms from the calibrated second variation, so the calibration
   performs Goh's transformation, and `bᵀMb` is the coefficient `R` of the
   transformed Legendre term (Aronna–Bonnans–Dmitruk–Lotito 2012, eq. (39)).
4. *What is left free.* Tangency fixes `Pb` and `bᵀṖb`. For state
   dimension `n = 1`, it fixes everything: `P = w/b` and `M = K/b²`, so a
   strict local calibration along the arc (with the cubic correction of
   item 5) exists if and only if strict Kelley `K > 0` holds. For `n ≥ 2`, the rest of `P` obeys a Riccati inequality of
   dimension `n − 1` (the Goh-transformed accessory problem); its
   solvability is a Jacobi-type condition (Remark 1.4, sketch).
5. *Quadratic versus cubic.* For a calibration that is quadratic in the
   state, the Hessian of the residual at the other controls is
   `M + (u − u*)Z`, with `bᵀZb = c₁` fixed by the data. Such calibrations
   need `K + (u − u*)c₁ ≥ 0` on all of `U`, which is stronger than Kelley.
   A cubic term removes this condition (Proposition 1.5). A null-Lagrangian
   example shows the gap is real.
6. *Junctions.* At a junction with an order-1 arc, `σ` vanishes
   quadratically on the bang side, `|σ| ≈ ½K|u_b − u_s|s²`.
   - With a cubic correction, tangency with `β ≡ 0` can be continued a short
     way into the bang arc whenever `K > 0` (Proposition 2.1(b)).
   - Calibrations that are quadratic in the state need
     `a_j = K + (u° − u_b)c₁` not too negative (Proposition 2.1(c)).
     catmix violates this at its entry junction.
   - At a singular-to-bang junction, the layer condition `η_L > 0` of [E]
     applies unchanged (Remark 2.2).

**Discrete time (Section 3).** At a fractional stage (interior control,
the discrete analogue of a singular stage) of an Euler transcription,
exactness requires the Hessian of the stage residual to be positive
semidefinite. That gives two conditions: the stage control curvature
`κ_t = bᵀ∇²S_{t+1}b` must be `≥ 0`, and, if the state Hessian of the stage
residual is small (`K_t ⪯ hΛI`), tangency must hold up to
`|β_t| ≤ √(hΛκ_t)` (Lemma 3.1). Without `K_t ⪯ hΛI`, an isolated stage can
be exact with `|β_t| = O(1)` (Remark 3.3a). Consequences:

| | affine (costate) family | tangential quadratic family |
|---|---|---|
| fractional stages, `bᵀw > 0` | every stage with `w ≠ 0` fails; total loss `Θ(1)` | none fails (Proposition 3.4) |
| fractional stages, `bᵀw < 0` | every stage with `w ≠ 0` fails; total loss `Θ(1)` | for families with bounded Hessians **and** `K_t ⪯ hΛI` (for bounded Hessians, the one-sided condition `∇²S_{t+1} − ∇²S_t ⪯ O(h)`; Hessians that change by `O(h)` per stage are one example), every stage fails; loss `≥ ch²` each, `Θ(h)` in total (Proposition 3.3). Without `K_t ⪯ hΛI`, isolated stages can be exact through `O(1)` drops of the Hessian (Remark 3.3a). A long run of fractional stages is a saddle point of the Euler problem, whose optimum chatters (Remark 3.5) |
| bang side of a junction | window of fixed duration (`Θ(1/h)` stages), where `σ < Δ\|w\|²/(2μ)` | none if `bᵀw > 0` and a tangential continuation exists (Proposition 2.1); the condition does not involve `σ_t` |

- The sign that matters is that of `bᵀw`, which **depends on the
  formulation and on the scheme**. Adding a null Lagrangian `dF/dt` shifts
  it by `−bᵀ∇²F b`. Under a tangential calibration, the per-step control
  curvature is `h²bᵀw` for explicit Euler and `(K/3)h³` for the exact flow
  (generic `n = 1`, symbolic).
- The quantity that does not depend on the calibration is the symbol
  `f(ω)` of the discrete accessory problem at a stationary discrete singular
  point. At the alternating frequency, `f(π) ≈ h²bᵀw` for Euler and
  `f(π) = Kh³/12` for the exact flow (catmix numerics). `f(π) ≥ 0` is
  necessary for stationary quadratic calibrations (Proposition 3.6). For a
  scalar state (`n = 1`), a stationary quadratic storage exists if and only
  if `f(0) ≥ 0` and `f(π) ≥ 0` (Proposition 3.7, elementary proof). For
  `n ≥ 2` the converse is the discrete-time KYP lemma (Remark 3.8, cited).
- For a scalar state (`n = 1`) with `ℒ_uu ≠ 0`, when `f(π) < 0 < f(0)`,
  the linearized first-order conditions on a run of fractional stages have
  only alternating solutions, `(−1)^t` times an envelope that changes sign
  every `π/d₀` stages, where `f(π ± d₀) = 0` (Remark 3.9; exact for the
  stationary linear recursion, heuristic when applied to the finite catmix
  arc). The condition `f(π) < 0 < f''(π)` is not enough (Remark 3.9). For
  the catmix trapezoidal rule, `π/d₀ = 12.03` stages at `h = 1/100`,
  `1/200` and `1/400` (the same to five digits).

**Tests.**

- **E2 (n = 2, bang arc then singular arc, explicit continuous global
  quadratic calibration)** (Section 4):
  - with `bᵀw = 1/2`, the tangential families give **exact rational
    certificates (bound = discrete optimum, gap 0) at N = 50 … 1600**, with
    no failing stage;
  - the affine family fails on every singular stage and on a bang-side
    window that starts at `t = 0.27375` (prediction 0.2733); its loss is
    0.68–0.71;
  - with the gauge `bᵀw = 0`, the transferred continuous `P` fails on every
    singular stage with loss `O(h²)`, while the discrete maximal recursion
    is exact;
  - with `bᵀw = −1/2` (the same continuous problem), an Euler KKT point
    with the continuous structure exists and lies within `o(h)` of the
    continuous optimum, but it is a saddle. The best Euler points found
    chatter and lie `0.43h` below it (prediction `0.44h`). No stage-wise
    quadratic family was found, and global optimality of the chattering
    points is not established (three multistart procedures found different
    best values at N = 100).
- **catmix (Section 5).** catmix reduces exactly to a 1-D problem in the
  projective coordinate `θ = x₂/(x₁+x₂)`.
  - Its singular arc is the point `θ_s = (11 − √10)/111`, with Kelley
    quantity `K = 2√10`, tangential curvature `P_s = w/b ≈ −12.04` and
    `bw ≈ −1.005` (exact, symbolic).
  - Calibrations quadratic in `θ` work along the arc and at the exit
    junction, but not at the entry junction, where `a_j = K − c₁ = −14.1`
    (Proposition 2.1(c)); a cubic term is needed there.
  - Accessory symbols `f(π)`: Euler `≈ −1.00h²`; COPS trapezoidal rule
    **`−0.0273h³`**; exact flow `+0.527h³ = Kh³/12`.
  - So the COPS transcription turns the singular arc into a saddle. This
    explains the chattering controls (0.4543 and 0, that is `2u_s` and 0)
    that [C] observed.
  - At N = 100 a KKT point with the bang–singular–bang active set exists
    (the saddle point; float, gradient `3e-17` on its 59 arc stages, none
    at a bound). Its arc controls are **not smooth**: they oscillate from
    stage to stage within [0.055, 0.411], around `u_s = 0.227`, with an
    envelope that changes sign every 11 stages, close to the spacing
    `π/d₀ = 12.03` of Remark 3.9. At N = 200 only an approximate
    stationary point was found, not a verified KKT point (interior gradient
    `3.3e-9`, a Hessian eigenvalue of `1.8e-12`, arc stages at `u = 0` with
    slightly wrong multiplier signs; Section 5.5). It oscillates in the
    same way. Remark 3.9 explains the oscillation (heuristic): the only
    linearized modes on the arc are alternating, and an `O(h)` state
    mismatch at a junction excites them with an `O(1)` control amplitude.
  - Heuristic quantitative checks (float, Section 5.5):
    - The chattering gain over the best control that is smooth on the arc
      (with free junction stages) is `3.93–4.03e-8`, `9.80–10.11e-9` and
      `2.45–2.47e-9` at N = 100, 200 and 400 (knot spacings 4, 6 and 10
      stages), against the prediction
      `½u_s²|f(π)|(t₂ − t₁)/h·(J+1)` = `3.95e-8`, `9.87e-9` and `2.47e-9`.
      The agreement depends on how the smooth reference treats the
      junction stages: without free junction stages the ratio is 1.0–3.2.
      Boundary terms of the same order in `h` are not controlled, so this is
      a heuristic check, not a proof.
    - At the smooth base point the most negative Hessian eigenvalue
      (`−2.49e-8` in `J` units, N = 100) lies inside the range of the symbol
      (minimum `−2.60e-8`), within 0.1% of the finite-section estimate.
      At the oscillating KKT point (N = 100) it lies 21% below the symbol
      minimum (`−3.14e-8`). [C] reports `−2.5e-8` at its own local
      solution.
    - Negative-eigenvalue counts, against the prediction `m d₀/π`: 4 and 10
      at the smooth base points (N = 100, 200; predicted 4.9 and 9.8); 5 at
      the N = 100 KKT point (predicted 4.9); 7 at the approximate N = 200
      point (predicted 9.4; that point is not a verified KKT point).
  - Float screening on the COPS optimum:
    - the affine family loses `Θ(1)` (0.017–0.020 in `log(J+1)` inside a
      band of ±0.01 in `θ`);
    - the stage-wise maximal quadratic recursion breaks periodically, every
      12 stages, matching the conjugate-point spacing `π/d₀ = 12.03` of
      Remark 3.9 (heuristic). At N = 200 and 400 one more break lies near
      the entry junction. The break counts (5, 10 and 20; periodic: 5, 9
      and 19) restate the spacing and are not a separate check;
    - windows of 2 stages, matching the chattering period, leave one break
      per `N` in the quadratic model. It lies on the arc side of the entry
      junction or inside the arc, and is unexplained (Section 5.6).

**What is new, and what is not.** Items 1–3 are the classical Goh/Kelley
theory, reformulated as statements about pointwise calibrations. The
second-variation facts behind them are old (Kelley 1964; Goh 1966;
Jacobson–Speyer 1970/71; Aronna et al. 2012). Local sufficiency along the
arc and across a bang–singular junction (Propositions 1.6 and 2.1(b)) is
close in content to the Hamiltonian-method sufficiency results for
bang–singular extremals (Poggiolini–Stefani 2005–2011; the field-of-extremals
constructions in Schättler–Ledzewicz 2012). A field of extremals gives a
local calibration, so those results cover the existence part; I read only
one short Poggiolini–Stefani paper (Sources). What may be new is the
calibration form, not the optimality statements. I did not find the
following stated anywhere, but the search was limited (Sources):

- the tangency statement for calibrations, as a statement about
  calibrations that are `C²` in the state (its content is classical);
- the quadratic-versus-cubic gap;
- the Euler coefficient `h²bᵀw` and its dependence on the gauge. The
  closest work found, Felgenhauer (2016) on Euler discretization of
  bang–singular–bang problems, was read in abstract only. By the second
  review's reading of her 2005 paper, her "semilinear" class probably has
  `w ≡ 0`, where this coefficient vanishes. The formulations tested here
  lie outside that class, but equivalent formulations of E2 and catmix
  with `w ≡ 0` lie inside it; their Euler transcriptions were not tested
  (Remark 3.5);
- the use of the accessory symbol to explain catmix chattering and the
  12-stage pattern (the quantitative agreements are heuristic);
- the failing-stage counts.

Oscillating controls on singular arcs of direct transcriptions are widely
reported.

## 0. Setting and notation

- **Continuous problem** (as in [R, Section 0] and [E, Section 0]):
  `ẋ = g(x,u) = a(x) + b(x)u`, scalar `u ∈ U = [u_−, u_+]`, `Δ = u_+ − u_−`,
  cost `∫_0^T ℓ_0(x) + ℓ_1(x)u dt + Φ(x(T))`, `x(0)` fixed. Data are `C³`.
- **Hamiltonian and switching function.** `H = ℓ_0 + ℓ_1u + ψᵀg` (minimum
  principle); `σ_0(t,x) = ℓ_1(x) + b(x)ᵀψ(t)`, `σ(t) = σ_0(t,x*(t))`;
  `w_t = −∇_xσ_0(t,x*(t)) = −(∇ℓ_1 + b_xᵀψ)`. Here `b_x` is the Jacobian
  of `b`.
- **Singular arc.** An interval `I` on which `σ ≡ 0` and
  `u*(t) ∈ int U`. Since `σ̇` does not contain `u` (control-affine),
  `σ̈` is affine in `u`. The arc has **order 1** if `∂_uσ̈ ≠ 0`. The
  **Kelley quantity** is `K(t) := −∂_u σ̈(t)`, and Kelley's condition (for
  a minimum) is `K ≥ 0` on `I` (Kelley 1964; Robbins 1967).
- **Calibration.** A function `S(t,x)`. Its residual is
  `r = ℓ_0 + ℓ_1u + ∂_tS + S_xᵀg`, and its switching function is
  `σ_S = ℓ_1 + bᵀS_x`. The residual is affine in `u`:
  `r = r(t,x,u*) + σ_S·(u − u*)`.
- **Quadratic calibrations** ([R, Proposition 3.2]):
  `S = V*(t) + ψᵀd + ½dᵀP(t)d`, `d = x − x*(t)`. Along the trajectory,
  `β = Pb − w` and `M(t,u) = Ṗ + g_x(u)ᵀP + Pg_x(u) + H_xx(u)`. The
  expansion `r(t, x*+d, u*+ω) = σω + ωβᵀd + ½dᵀM(t,u*+ω)d + O(|d|³)`
  of [E, 1.1] holds.
- **Euler transcription** ([R, Section 0]):
  `ρ_t(x,u) = h(ℓ_0 + ℓ_1u) + S_{t+1}(x + h g(x,u)) − S_t(x)`. At a KKT
  point `z̄_t` with `p_{t+1} = ∇S_{t+1}(x̄_{t+1})` and
  `P_{t+1} = ∇²S_{t+1}(x̄_{t+1})`:
  - `∂_uρ = hσ_t` with `σ_t = ℓ_1 + bᵀp_{t+1}`;
  - `∇_x∂_uρ = hβ_t` with `β_t = F_xᵀP_{t+1}b − w_t^h`, where
    `w_t^h = −(∇ℓ_1(x̄_t) + b_x(x̄_t)ᵀp_{t+1})` and `F_x = I + hg_x`;
  - `∂²_uρ = h²κ_t` with `κ_t = bᵀP_{t+1}b`;
  - `K_t = ∇²_xρ`.

  A stage is **fractional** if `ū_t ∈ int U`; then `σ_t = 0`.

## 1. Continuous time: what exactness on a singular arc forces

**Proposition 1.1 (tangency on the whole arc).** Let `I` be a singular
arc. Let `S`, `∂_tS`, `S_x` and `S_xx` be continuous near
`{(t, x*(t)) : t ∈ I°}`, and, for the adjoint statement in (b), let
`∂_tS` be `C¹` in `x`. Assume `r ≥ 0` for all `u ∈ U` on a tube
`{t ∈ I°, |x − x*(t)| < r_0}`, and `r(t, x*(t), u*(t)) = 0`. Then for every
`t ∈ I°`:

- (a) `σ_S(t, x*(t)) = 0` and `r(t, x*(t), u) = 0` for every `u ∈ U`;
- (b) `∇_x r(t, x*(t), u) = 0` for every `u ∈ U`. In particular
  `ψ(t) := S_x(t,x*(t))` satisfies the adjoint equation, and `σ ≡ 0`;
- (c) `∇_xσ_S(t, x*(t)) = 0`, that is, **`P(t)b = w_t`** with
  `P(t) := S_xx(t, x*(t))`.

*Proof.* (a) `r(t,x*,·)` is affine on `U`, nonnegative, and zero at the
interior point `u*`, so its slope `σ_S(t,x*)` is zero and it vanishes on
`U`. (b) For each fixed `u`, `x ↦ r(t,x,u)` is `≥ 0` and zero at the
interior point `x*(t)`, so its gradient is zero there. At `u = u*` this is
`∇ℓ_0 + u*∇ℓ_1 + ∂_tS_x + S_xx g + g_xᵀS_x = 0`, which is the adjoint
equation for `S_x(t,x*(t))`. (c) Subtract (b) at two controls:
`(u − u')∇_xσ_S = 0`. Finally
`∇_xσ_S = ∇ℓ_1 + b_xᵀS_x + S_xx b = Pb − w`. □

This is [S, Proposition 4.1] (affine families, discrete) and
[R, Proposition 3.1] (a switching time), applied at every point of an
interval. For affine `S` (`P = 0`) it says that exactness forces `w ≡ 0`
on the arc.

**Corollary 1.2 (several controls: Goh's condition).** With
`g = a + Σ_j b_j u_j`, `u*` interior in `U ⊂ R^m`, and the same
hypotheses, the argument gives `PB = W` with `B = [b_1 … b_m]` and
`W = [w_1 … w_m]`, `w_i = −∇_xσ_{0,i}`. Hence `BᵀW = BᵀPB` is symmetric.
Moreover `BᵀW − WᵀB = G` with `G_ij := ∂σ̇_i/∂u_j`. So `G ≡ 0` on the
arc, which is Goh's necessary condition (Goh 1966: `∂_u(dH_u/dt)`
symmetric; `G` is antisymmetric for control-affine systems, so this means
`G = 0`). In the notation of Aronna–Bonnans–Dmitruk–Lotito (2012, eq. (36)),
this is `V ≡ 0`.

*Proof of the identity.* `σ̇_i = ∇_xσ_{0,i}·g − b_iᵀH_x`, and
`∂_{u_j}H_x = ∇ℓ_{1,j} + b_{j,x}ᵀψ = −w_j`. So
`∂_{u_j}σ̇_i = −w_iᵀb_j + b_iᵀw_j`. □ (Also checked symbolically:
`kelley_identity.py`, random polynomial data, `n = 2, 3`, `m = 2`.)

**Proposition 1.3 (second order: Kelley's quantity is the `b–b` entry).**
In addition, let `S_xx` be `C¹` in `(t,x)`, and let `∂_tS` be `C²` in `x`,
near the arc. Then for `t ∈ I°`:

- (a) `∇²_x r(t, x*(t), u) ⪰ 0` for every `u ∈ U`. At `u = u*(t)` it equals
  `M(t, u*(t))` with `P = S_xx(t,x*(t))`: the third derivatives of `S`
  cancel against the total derivative `Ṗ`, as in [E, Lemma 14].
- (b) `bᵀM(t,u*)b = R(t) := bᵀH_xx b + bᵀẇ + 2wᵀg_x b − wᵀḃ`, and
  `R(t) = K(t) = −∂_uσ̈(t)`.

Hence `K ≥ 0` on the arc (Kelley's condition). If `r ≥ ε|x − x*(t)|²`,
then `K ≥ 2ε|b|²`.

*Proof.* (a) As in Proposition 1.1(b), `x*(t)` minimizes `r(t,·,u)`. The
Hessian formula follows by differentiating `r` twice:
`∂_tS_xx + S_xxx[g] = Ṗ` at `(x*, u*)`.

(b) Differentiate `Pb = w` along the arc (`P` is `C¹` there):
`Ṗb = ẇ − Pḃ`, so `bᵀṖb = bᵀẇ − wᵀḃ`. Also `bᵀPg_xb = wᵀg_xb`. This
gives `bᵀMb = R`.

For `R = −∂_uσ̈`, treat `u` as a parameter and write `D` for the derivative
along `ẋ = g`, `ψ̇ = −H_x`. Then:

- `σ̇ = F_1(x,ψ) = −wᵀa − bᵀH_x^0`, where `H_x^0 = ∇ℓ_0 + a_xᵀψ` (the
  `u`-terms cancel);
- using `∂_uH_x = −w`, `Dw = w_xg + b_xᵀH_x` and `D(H_x^0) = H^0_xx g − a_xᵀH_x`,
  `∂_uσ̈ = aᵀσ_{0,xx}b + wᵀb_xa − 2wᵀa_xb − (b_xb)ᵀH_x^0 − bᵀH^0_xxb`,
  where `σ_{0,xx} = −w_x` is the state Hessian of `σ_0`;
- `R` does not depend on `u`: its `u`-coefficient is
  `bᵀσ_{0,xx}b − bᵀσ_{0,xx}b − wᵀb_xb + 2wᵀb_xb − wᵀb_xb = 0`;
- evaluating `R` at `u = 0` gives exactly `−∂_uσ̈`. □

*Checks.* Symbolic, exact (`kelley_identity.py`,
`logs/kelley_identity.log`). For random integer polynomial data with
`n = 2` and `n = 3` (three seeds each):

- `σ̇` is free of `u`;
- `R = −∂_uσ̈` holds identically in `(x, ψ, u)`;
- with `P` kept symbolic under `Pb = w` and `Ṗb = ẇ − Pḃ`,
  `bᵀMb − K ≡ 0`.

*Relation to Goh's transformation.* For any symmetric `C¹` `P`, the second
variation `Ω = ½δx_TᵀΦ_xxδx_T + ∫ ½δxᵀH_xxδx − δu wᵀδx` equals

```
½δx_Tᵀ(Φ_xx − P_T)δx_T + ∫ [ ½δxᵀM δx + δu βᵀδx ] dt     (δx(0) = 0).
```

Tangency (`β ≡ 0`) removes every `δu` term, so on the arc the calibrated
second variation is a quadratic form in `δx` alone. Writing
`δx = ζ + bv` with `v̇ = δu` gives Goh's transformed form, whose Legendre
coefficient is `bᵀMb = R`. Aronna et al. (2012, eq. (39)) define
`R = BᵀQB − CB_1 − (CB_1)ᵀ − Ṡ`, with `Q = H_xx`, `C = H_ux = −wᵀ`,
`B_1 = g_xb − ḃ` and `S` the symmetric part of `CB`. For `m = 1` this is
the `R` above. The Jacobson–Speyer "limit approach" (a Riccati equation
with control weight tending to zero) arrives at the same structure from the
other side.

**Remark 1.4 (what tangency leaves free; sketch for `n ≥ 2`).** Tangency
fixes the column `Pb = w` and the entry `bᵀṖb`. The other entries of `Ṗb`
are then also fixed (`Ṗb = ẇ − Pḃ`), but they involve `P` through
`Pḃ`. The block of `P` on `b^⊥` and its derivative are free.

- **`n = 1`:** `P = w/b` and `M = K/b²`. A local strict calibration along
  the arc (Proposition 1.6) exists if and only if `K > 0` (with `b ≠ 0`).
- **`n ≥ 2`:** in a frame `(b/|b|, E(t))`, `M ⪰ 2μ` is equivalent to
  `K ≥ 2μ|b|²` plus a Schur-complement inequality. That inequality is a
  Riccati differential inequality of dimension `n − 1` for `EᵀPE`, with
  control weight `K/|b|²` and input `Eᵀb_1`, where `b_1 = g_xb − ḃ`. This
  is the Riccati inequality of the Goh-transformed accessory problem. It
  can be solved backward on a compact arc exactly when its solution does
  not blow up, which is a Jacobi-type (no conjugate point) condition. The
  details were not written out (sketch). In E2 (Section 4) it is the scalar
  inequality `ṗ₂₂ ≥ 2p₂₂ − 1 + (p₂₂ + k₂)²/K`.

**Proposition 1.5 (quadratic versus higher-order calibrations).** For `C³`
`S` with tangency, `∇²_x r(t, x*, u) = M(t,u*) + (u − u*)Z(t)`, where
`Z = ∇²_xσ_S = σ_{0,xx} + Pb_x + b_xᵀP + S_xxx[b,·,·]`.

- (a) If `S` is quadratic in `x`, then `S_xxx = 0` and
  `bᵀZb = c₁(t) := bᵀσ_{0,xx}b + 2wᵀb_xb` is fixed by the data. Exactness
  then needs `K + (u − u*)c₁ ≥ 0` at both vertices, in addition to
  Kelley's `K ≥ 0`.
- (b) The tensor `S_xxx[b,·,·]` can be any symmetric matrix (for
  `b ≠ 0`), and choosing it does not change `P`, `Ṗ` or `M(t,u*)`
  (adjust `∂_tS_xx`). Taking `S_xxx[b,·,·] = −(σ_{0,xx} + Pb_x + b_xᵀP)`
  gives `Z = 0`.

*Proof.* Differentiate `r = r(t,x,u*) + σ_S(u − u*)` twice in `x` at
`x*(t)`. (b) In coordinates with `b = e_1`, set `T_{1jk} := Y_jk` and fill
the other entries by symmetry. □

*Example (the gap is real).* Take `ẋ = u`, `|u| ≤ 1`, and cost
`∫ ℓ_0(x) + (x²/2)u dt`. The term `(x²/2)u = d/dt(x³/6)` is a null
Lagrangian, so the problem differs from `min ∫ℓ_0` only by endpoint terms.

- Along the singular arc `x ≡ x_s` (`ℓ_0'(x_s) = 0`, `u* = 0`),
  `K = ℓ_0''(x_s)` and `c₁ = ℓ_1'' = 1`.
- The quadratic class needs `K − 1 ≥ 0`, from the vertex `u = −1`.
- The cubic calibration `S − x³/6`, with `S` quadratic for `∫ℓ_0`, has
  `Z = 0` and needs only `K > 0` (Proposition 1.6).

(For catmix the quadratic class is enough on the arc, but not at the entry
junction; Sections 2 and 5.3.)

**Proposition 1.6 (local sufficiency along the arc).** Let `P` be `C¹` on
a compact subinterval `I_0 ⊂ I°`, with `Pb = w` and `M(t, u*(t)) ⪰ 2μI`.
Take `S = V*(t) + ψᵀd + ½dᵀPd + (1/6)T(t)[d,d,d]`, with `T` chosen as in
Proposition 1.5(b) (bounded and `C¹` when `b(x*(t)) ≠ 0`). Then
`r(t, x*+d, u) ≥ μ|d|² − C|d|³` for all `u ∈ U` and `t ∈ I_0`, so `S` is
a strict local calibration on a tube around the arc. For quadratic `S`
(`T = 0`) the same holds if `M(t,u) ⪰ 2μI` at both vertices.

*Proof.* `r(t,x*+d,u) = σ_S(t,x*+d)(u − u*) + r(t,x*+d,u*)`. The first
factor is `½dᵀZd + O(|d|³) = O(|d|³)`. The second is
`½dᵀM(t,u*)d + O(|d|³)`, because the value and gradient vanish by the
choice of `V*` and `ψ`. □

## 2. Junctions between bang and singular arcs

**Proposition 2.1 (junction behaviour and local tangential continuation).**
Let `t_j` be a junction between a bang arc with control `u_b` and an
order-1 singular arc with `K(t_j) > 0`, and let `u_b ≠ u_s := u*(t_j±)`
(the singular control at the junction; the control is discontinuous
there). Let `u°` be the vertex other than `u_b`, and let `s ≥ 0` be the
distance from `t_j` into the bang arc. Then:

- (a) On the bang side, `σ = −½K(t_j)(u_b − u_s)s² + o(s²)`. The sign is
  the one the minimum principle requires, which in turn requires
  `K(t_j) > 0`.
- (b) *(`C³` calibrations.)* Let `P` be a tangential Hessian on the arc
  with `M(t_j, u_s) ≻ 0`. Then there is a calibration, `C³` in `x`, with
  the cubic correction `Z ≡ 0` of Proposition 1.5, with `β ≡ 0` on
  `(t_j − δ, t_j + δ)` (so on part of the bang arc too), and strict on a
  tube there. Its Hessian `P` is continuous at `t_j`; `Ṗ` may jump.
- (c) *(Quadratic calibrations.)* For `S` quadratic in `x`, `Z = N_0(P)` is
  fixed. With `P` tangential at `t_j`, the `b–b` entry of `M(t, u°)` on the
  bang side tends to
  `a_j := K(t_j) + (u° − u_b)c₁(t_j)`. This differs from its value on the
  arc because `Ṗb = ẇ − Pḃ` jumps with the control.
  - If `a_j > 0`, part (b) holds with quadratic `S` (`Z = N_0`).
  - If `a_j < −K(t_j)|u_b − u_s|/(4Δ)`, then no calibration that is
    quadratic in `x` is exact on a tube on the bang side of `t_j`. Here `P`
    is `C¹` on each side up to `t_j`, and upward jumps are allowed.

*Proof.* (a) `σ(t_j) = σ̇(t_j) = 0` (`σ̇` is continuous and vanishes on the
arc). `σ̈` is affine in `u`, vanishes at `u_s` and has slope `−K`, so its
one-sided value on the bang side is `−K(u_b − u_s)`.

(b) On the bang side, prescribe the column `Ṗb = ẇ − Pḃ` (with `ẇ`, `ḃ`
along the bang arc), so `β ≡ 0`. The identity of Proposition 1.3(b) holds
along any extremal, since its proof never used `σ = 0`. So
`bᵀM(t,u_b)b = K(t)`, which is continuous and positive. The `b–b` entry of
`M(t, u°)` is the same number, because `Z = 0`. The off-diagonal block may
jump at `t_j`. The `b^⊥` block of `Ṗ` is free, so a large enough choice
makes `M(t,u) ⪰ μ` near `t_j` (Schur complement with respect to the `b–b`
entry). The expansion `r = σω + ½dᵀM(t,u)d + O(|d|³)` then gives `r ≥ 0`,
because `σω ≥ 0` by the minimum principle.

(c) The case `a_j > 0` is (b) with `Z = N_0`. For the second case, first,
tangency at the one-sided limit is forced: `r(t, x*, u) = σ(u − u_b) → 0`,
then argue as in Proposition 1.1, as in [R, Proposition 3.1, robustness].
So `β → 0` as `s → 0`, and in particular `η := bᵀβ → 0`. Since `P` and
`w` are `C¹` up to `t_j` on the bang side, `|β| = O(s)`.

Next, the vertex inequality in the direction `b`
([E, Theorem 1, "Mechanism"]) gives
`bᵀM(t,u°)b ≥ Δη²/(2|σ|) − O(s)`. The remainder is small because the test
displacement has size `2|σ|/|η| = O(s)` whenever `|η| ≳ s`.

Write `P b = w + β`. As in the proof of Proposition 1.3(b),
`bᵀM(t,u°)b = η̇ + a_j + O(s + |β|) = η̇ + a_j + O(s)`. (For `n ≥ 2`
the remainder contains terms such as `βᵀḃ` and `βᵀg_xb`, which involve
the components of `β` orthogonal to `b`; hence `|β|`, not `|η|`.) Let
`ϵ = −1` if the bang arc
precedes the junction and `ϵ = +1` if it follows it, so that `η̇ = ϵη'`
with `' = d/ds`. Put `|σ| ≈ γs²` with `γ = ½K|u_b − u_s|`, and
`y := ϵη/s`. The inequality becomes `s y' ≥ −a_j − y + Δy²/(2γ) − o(1)`.
(When `|η| ≪ s`, the vertex inequality with the test step `λ = √s` in
direction `b` gives only `bᵀM(t,u°)b ≥ −2|σ|Δ/λ² − O(λ) = −O(√s)`. Then
`ϵη' ≥ −a_j − o(1) > 0` makes `y ≥ |a_j|/2` for small `s`, and the
argument continues with `|η| ≳ s`.) The
right-hand side is at least `−a_j − γ/(2Δ) − o(1)`, which is `≥ c > 0`
when `a_j < −γ/(2Δ)`. Then `y(s) ≥ y(s_0) + c log(s/s_0)` for all
`s_0 < s`, while `y(s_0)` stays bounded as `s_0 → 0` (`η` is `C¹` with
`η(0) = 0`). This is a contradiction. Upward jumps of `P` inside the bang
arc only lower `η` further, as in [E, Corollary 3]. □

The remainder bookkeeping in (c) was written at the level of
[E, Theorem 1, "Mechanism"] in the first version. The review completed it
(its Section 2.2); I rechecked the three steps above (the `O(|β|)`
remainder, the `λ = √s` step, and the `(1 + o(1))` factor in
`|σ| = γs²(1 + o(1))`, which leaves `min_y [Δy²/(2γ) − y] = −γ/(2Δ)`
unchanged in the limit). The case `−γ/(2Δ) ≤ a_j ≤ 0` (a non-tangential
linear-rate continuation) was not worked out.

This is consistent with McDanell–Powers (1971): with strict GLC and
`q = 1`, the control may jump at the junction. Away from the junction `β`
may become nonzero, and [R, Theorem 2.3] governs the bang arc. For catmix,
`a_j = −14.10` at the entry junction, against the threshold `−1.22`, so
quadratic calibrations in `θ` fail there and a cubic term is needed. At the
exit junction `a_j = +26.75` (Section 5.3).

**Remark 2.2 (singular-to-bang junction: the layer condition).** If the
last arc `(t_j, T]` is bang with free endpoint, then [E, Theorem 1]'s short
proof applies verbatim. Tangency holds at `t_j+` (Proposition 1.1 and
continuity), and `P ⪯ Q_ε` by Lyapunov comparison, so
`η_ε = bᵀ(Q_ε(t_j+) − P(t_j+))b ≥ 0`. Hence **`η_L = bᵀ(Q(t_j+)b − w) > 0`
is necessary** for a strict calibration, as at a regular switch. Because
`σ` now vanishes quadratically, the singular coefficient `Δ/(2|σ|)` of
[R, Proposition 3.2] grows like `s⁻²`. In the leading-order layer equation
`η' = Δη²/(2cs²)`, `η_1 > 0` gives `η ≈ 2cs/Δ`: linear-rate tangency
comes automatically, instead of the logarithmic rate at a regular switch
([E, 2.5]). If `η_1 < 0`, the solution still blows up at a positive `s`.
(Sketch: the sufficiency direction of [E, Theorem 2] was not redone for
quadratic `σ`. The global-form caveats of [E, Section 4] apply unchanged.)
For catmix, `η_L = 1` exactly (Section 5.3).

## 3. Discrete time: fractional stages, the sign of `bᵀw`, and the accessory symbol

**Lemma 3.1 (exactness at a fractional stage).** Let `ρ = ρ_t` be `C²`
near `z̄_t`, with `x̄_t` interior and `ū_t ∈ int U`.

- (a) *Necessary.* If `z̄_t` minimizes `ρ` locally, then
  `[[K_t, hβ_t],[hβ_tᵀ, h²κ_t]] ⪰ 0`. In particular `κ_t ≥ 0`, and if
  `K_t ⪯ hΛI`, then `|β_t|² ≤ hΛκ_t`.
- (b) *Sufficient* ([R, Lemma 2.1(ii)]). If `∇²_xρ ⪰ hμ` on a ball times
  `U`, `∂²_uρ(x̄,u) ≥ h²κ` for `u ∈ U`, and
  `hκ ≥ (|β_t| + hCΔ/2)²/μ`, then `z̄_t` is a minimizer on the ball.
  This condition does not involve `σ_t`, so it also covers vertex stages.

*Proof.* (a) Second-order necessary condition at an interior minimum. For
the bound, take `d = −(s/Λ)β_t` in `dᵀK_td + 2hsβ_tᵀd + h²κ_ts² ≥ 0`.
(b) is [R, Lemma 2.1]. □

So at fractional stages the **control curvature `κ_t = bᵀP_{t+1}b` must
be nonnegative**, and a family with `K_t ⪯ hΛI` must be **tangential to
within `√h`**. For bounded Hessians, `K_t = P_{t+1} − P_t + O(h)` (with
`P_t = ∇²S_t(x̄_t)`), so `K_t ⪯ hΛI` is the one-sided condition
`P_{t+1} − P_t ⪯ O(h)`: going back from stage `t+1` to stage `t`, the
Hessian may not drop by more than `O(h)`. Hessians that change by `O(h)`
per stage are one example. Without this condition a stage can be exact with
`|β_t| = O(1)` (Remark 3.3a). Near tangency pins `P_{t+1}b ≈ w`, so
`κ_t ≈ bᵀw`.

**Proposition 3.2 (affine families fail on the whole arc).** For
`S_t = p_tᵀx`, `κ_t = 0` and `β_t = −w_t^h`. A fractional stage with
`w_t^h ≠ 0` is not exact ([S, Proposition 4.1]). If moreover
`ρ(x̄+d, ū+ω) ≤ ρ̄ + hωβ_tᵀd + ½hΛ|d|²` on a ball containing
`d = ω̂w/Λ`, where `ω̂ = max(ū − u_−, u_+ − ū)`, then the loss is at least
`½hω̂²|w_t^h|²/Λ`. Along a discrete singular arc that converges to one
with `w ≠ 0`, the total loss is at least
`≈ ∫_arc ω̂(t)²|w(t)|²/(2Λ) dt`, which is `Θ(1)`: **the bound of the
affine class does not converge to `f*`**. □

(This answers the "size of the gap is not quantified" item of
[S, Proposition 4.1].)

**Proposition 3.3 (`bᵀw < 0`: no family is exact at fractional stages).**
Assume `|∇²S_{t+1}| ≤ Λ_S` near the trajectory, `K_t ⪯ hΛI`, and
`bᵀw_t^h ≤ −c < 0` at a fractional stage. Then for `h ≤ h_0(c, Λ, Λ_S)`
the stage is not exact, and its loss is at least `c'h²`.

*Proof.* From `P_{t+1}b = F_x^{−T}(w_t^h + β_t)`,
`κ_t ≤ bᵀw_t^h + C_1h + C_3|β_t|`. If the stage is exact, Lemma 3.1 gives
`κ_t ≥ 0` and `|β_t| ≤ √(hΛΛ_S)|b|`, so `0 ≤ −c + O(√h)`, which is a
contradiction. For the loss:

- if `|β_t| < c/(2C_3)`, then `κ_t ≤ −c/2 + C_1h`, and moving `u` alone
  loses `½h²|κ_t|ω̂²`;
- otherwise, moving `d` along `β_t` loses
  `½h²ω̂²(|β_t|²/(hΛ) − κ_t) = Ω(h)`. □

So, over a discrete singular arc, the total loss is `Θ(h)` or more for
**every** family with bounded Hessians and `K_t ⪯ hΛI` on the arc (the
one-sided condition `P_{t+1} − P_t ⪯ O(h)`; Hessians that change by `O(h)`
per stage are one example). By [S, Proposition 5.1] (sampling a
`C^{1,1}` solution) it is also `O(h)`.

**Remark 3.3a (the hypothesis `K_t ⪯ hΛI` matters).** With bounded
Hessians alone, an isolated fractional stage can be exact. Take any
`P_{t+1}` with `κ_t = bᵀP_{t+1}b > 0` and let `P_t` drop by the `O(1)`
amount of the maximal recursion, `P_t = F_xᵀP_{t+1}F_x + hH_xx − β_tβ_tᵀ/κ_t`
(`H` evaluated with `p_{t+1}`).
Then `K_t = β_tβ_tᵀ/κ_t` is `O(1)`, not `O(h)`, and the stage is exact
([E, Lemma 10]). *Check (exact rational, `revision_e2.py` item 5).* In E2
with `k₁ = +1/2` (`bᵀw = −1/2`), N = 100, at a mid-arc fractional stage of
the KKT point with the continuous structure: `P_{t+1} = e₁e₁ᵀ` gives
`κ_t = 1`, `|β_t| = 1.52`, `K_t` with eigenvalues `0` and `2.31`
(`h = 0.03`), and the stage passes the exact test. The previous stage then
has `κ_{t−1} = bᵀP_tb = −1.22 < 0` and fails for every `P_{t−1}`. The
same mechanism makes the last stage of family B2 in E2 exact with
`|β_t| = 0.34` (Section 4.3).

*Sketch (not needed elsewhere).* On a long run with `bᵀw_t^h ≤ −c`, an exact
fractional stage needs `|β_t| ≥ β₀ > 0` (from the proof of Proposition 3.3),
hence (Schur complement, `κ_t ≤ Λ_S|b|²`) `λ_max(K_t) ≥ β₀²/(Λ_S|b|²)`, and
`tr(P_{t+1} − P_t) = tr K_t + O(h) ≥ k₀ − O(h)` with `k₀ > 0`. A failing
stage contributes at least `−2nΛ_S` to `Σ_t tr(P_{t+1} − P_t)`, and that sum
over the run is at most `2nΛ_S`. So at least a fraction
`≈ k₀/(k₀ + 2nΛ_S)` of the stages fails, up to `O(1)` stages. No lower
bound on the loss of those stages follows without `K_t ⪯ hΛI`.

**Proposition 3.4 (`bᵀw > 0`: tangential families have no failing
stage).** Let `S` be a continuous calibration, `C³` near the arc. Assume:

- `β ≡ 0` on `[t_1 − δ, t_2 + δ]` (the arc plus bang-side neighbourhoods of
  its junctions, Proposition 2.1);
- `M(t,u) ⪰ 2μ` for `u ∈ U` and `bᵀw ≥ 2κ_0 > 0` there.

Let the discrete family be the transfer `S^h_t = S(t_t,·) + a_tᵀx` of
[R, Theorem 4.1], with discrete KKT points that converge with
`e_h = o(√h)`. Then for small `h`, every stage with `t_t` in that
neighbourhood (fractional or vertex) is exact on a ball.

*Proof.* We have `β_t = O(h + e_h) = o(√h)`,
`κ_t = bᵀw + O(h + e_h) ≥ κ_0`, and `∇²_xρ_t ⪰ hμ` ([R, Theorem 4.1],
step (c)). Lemma 3.1(b) applies. □

- The vertex stages next to a junction are covered even though `σ_t` is
  tiny there (`|σ| ~ s²`).
- The assumption `e_h = o(√h)` is not automatic. With `bᵀw > 0`, Euler
  adds a term `½h²κ Σu_t² ≈ ½hκ∫u²`, a cheap-control regularization. In
  E2 the discrete junction layer then has width `O(√h)` (Section 4.2).
- A family built directly at the discrete level avoids the assumption. An
  example is the maximal recursion of [E, Lemma 10], which balances `β_t`
  against `κ_t` stage by stage. It needs neither exact tangency nor a bound
  on `e_h`, only that the recursion does not break.

**Remark 3.5 (`bᵀw` depends on the formulation; the Euler optimum
chatters when it is negative).**

- *Gauge.* Adding `dF/dt = ∇F·g` to the integrand, and compensating with
  `F(x_0) − F(x_T)` in the cost, leaves the continuous problem unchanged.
  It maps `ψ ↦ ψ − ∇F`, `σ ↦ σ`, `w ↦ w − ∇²F b` and `P ↦ P − ∇²F`, so
  `bᵀw ↦ bᵀw − bᵀ∇²Fb`. On the discrete side,
  `Σ_t h∇F(x_t)·g_t = F(x_N) − F(x_0) − ½h²Σ_t g_tᵀ∇²F(x_t)g_t + O(h²)`
  (a Taylor expansion per stage). So the Euler problem acquires a stage term
  `−½h²(bᵀ∇²Fb)u_t²`, the same shift. For Euler, `bᵀw` is the
  scheme's own `h²` control curvature, not a property of the continuous
  problem.
- *Saddle.* At a KKT point with a run of `m` fractional stages, perturb
  by `δu_t = ε(−1)^t` on the run. The perturbed state is
  `δx_t = (−1)^tη_t` with `η_{t+1} + F_xη_t = −hbε`, so `|η_t| = O(hε)`.
  The Euler Lagrangian has no `u²` term, so the second-order change of the
  objective is
  `Σ_t [½h δx_tᵀH_xxδx_t − hδu_t w_tᵀδx_t] + ½δx_NᵀΦ_xxδx_N
  = ½h²ε² Σ_t bᵀw_t + O(mh³ε² + h²ε²)`.
  If `bᵀw ≤ −c` on a run of duration `mh ≥ τ_0`, this is negative for
  small `h`, so the KKT point is not a local minimizer. The Euler optimum
  then does not follow the singular arc; in E2 it chatters (Section 4.3).
  Under exact tangency the same number is `½Σh²κ_tε²`, the calibration's
  control curvature, as it must be, since the objective difference equals
  `Σρ_t`.
- If `bᵀw ≡ 0`, the next order decides. With exact discrete tangency
  (`β_t = 0`), `κ_t = bᵀF_x^{−T}w = −h wᵀg_xb + O(h²)`. In E2 with
  `k₁ = 0` (`bᵀw = 0`, `w ≠ 0`) this is `hk₂ > 0`, and the maximal
  recursion finds a family with `κ_t ≈ 0.91h` (Section 4.3).
- If `b` and `ℓ_1` do not depend on the state (the classical `ẋ = u`,
  `∫x²` example, or optcdeg2), then `w = −(∇ℓ_1 + b_xᵀψ) ≡ 0` itself, not
  only `bᵀw`. Affine families are then already tangential.
- *Relation to Felgenhauer (2016).* Felgenhauer proves, for a
  "semilinear" class of bang–singular–bang problems and under second-order
  conditions, that an Euler discretization of the first-order optimality
  system (a variational inequality) has a solution with the same
  bang–singular–bang structure, converging with order one in `L¹`. I read
  only the abstract (Sources), so I could not check what "semilinear" means
  there, nor whether her discrete system coincides with the KKT system of
  the Euler transcription used here. The two statements are compatible
  under either reading. If the class has `b` and `ℓ_1` state-independent,
  then `w ≡ 0` and the saddle mechanism above does not arise. If it
  includes E2-like data (`b` constant, `ℓ_1` linear), her result concerns
  solutions of the optimality system, that is, KKT points, while the saddle
  statement concerns whether such a point is a local minimizer. In E2 with
  `k₁ = +1/2` a KKT point with the continuous structure does exist and lies
  within `o(h)` of `J*` (Section 4.3), but it is a saddle.
- *The semilinear class (second review).* Felgenhauer's open 2005 paper
  (Control Cybernet. 34(3), 763–785, Section 2, as read by the second
  review) defines her semilinear class as `min k(x(1))` subject to
  `ẋ = f(t,x) + B(t)u`, with `B` independent of the state. I could not open
  that paper myself (the server returned a bot-check page), and the 2016
  definition was not seen. If the 2016 class is the same, the first reading
  above applies: a Mayer cost and a state-independent `B` give `w ≡ 0`, so
  the `h²bᵀw` term vanishes.

  Membership in this class is a property of the formulation, not of the
  problem. (Round 2 said that E2 is outside the class "in every gauge";
  that was wrong and is withdrawn, Section 11, S1.)
  - *The formulations used in this note are outside the class.* E2 with
    `ℓ_1 = k₁x₁ + k₂x₂`, `k₂ = 1/4`: in Mayer form, with a cost state, its
    input column contains `ℓ_1(x)`, which depends on the state. Catmix in
    `x` or in `θ`: `b` depends on the state.
  - *Equivalent formulations with `w ≡ 0` lie inside it* (symbolic,
    `revision3_semilinear.py`).
    - E2: the gauge `F = −k₁x₁²/2 − k₂x₁x₂` gives `ℓ_1 = 0`,
      `ℓ_0 = (x₁² + x₂²)/2 − k₂x₁(x₁ − x₂)` and `b = e₁`, and the Kelley
      quantity stays `1 − 2k₂`. The term `k₂x₂u` is not a null Lagrangian
      by itself, but `k₂x₂u + k₂x₁(x₁ − x₂) = d(k₂x₁x₂)/dt` is, and the
      gauge moves the remainder into `ℓ_0`.
    - Catmix: for every admissible control, `θ` stays in `[0, 1/11]`
      (`θ(0) = 0`; `θ̇ = u ≥ 0` at `θ = 0` and `θ̇ = 10(u − 1)/121 ≤ 0` at
      `θ = 1/11`),
      and there `b ≥ b(1/11) = 10/121 > 0`. So `ξ = ∫₀^θ dθ'/b(θ')` is a
      change of state on the reachable set, with `ξ̇ = a/b + u`, and the
      gauge `dF/dξ = −θ` removes `ℓ_1`. This gives
      `ℓ_0 = θ(11θ − 1)/b(θ)`, the same singular point
      (`111θ² − 22θ + 1 = 0`) and `K = 2√10`.
  - *Not tested.* The Euler transcriptions of these `w ≡ 0` formulations
    are different discrete problems: for E2 they differ from the tested
    ones by `O(h²)` terms per stage (gauge bullet above), and for catmix
    the change of variable also changes the scheme. None of them was run.
  - The compatibility argument of the bullet *Relation to Felgenhauer
    (2016)* is unaffected. Under this reading of the class, her Euler result would concern `w ≡ 0`
    formulations, where the `h²bᵀw` term vanishes; this agrees with the
    point that `bᵀw` depends on the formulation and the scheme.
  - Her other hypotheses were not checked. For example, E2's optimal
    control is bang–singular (the arc runs to `T`), not
    bang–singular–bang.

**3.6 Other schemes: the accessory symbol.** For a general time-invariant
one-step scheme `θ' = F(θ,u)`, with stage cost `L`, near a stationary
discrete singular point (`F = θ`, `L_u + qF_u = 0`,
`q = L_θ/(1 − F_θ)`), let `ℒ = L + qF`. The second variation along
`δθ_{t+1} = F_θδθ_t + F_uδu_t` is a Toeplitz form with symbol

```
f(ω) = ℒ_uu + 2ℒ_θu Re G(ω) + ℒ_θθ |G(ω)|²,   G(ω) = F_u/(e^{iω} − F_θ).
```

(Written for `n = 1`; the matrix version is analogous.)

**Proposition 3.6 (necessity at the alternating frequency).** If a
stationary quadratic storage `φ = qθ + ½Pθ²` makes the quadratic model of
every stage residual on a long run of fractional stages nonnegative, then
`f(π) ≥ 0`.

*Proof.* Along the 2-periodic perturbation
`(δθ_t, δu_t) = (−1)^t(η, ε)`, with `η = −F_uε/(1 + F_θ)`, `δθ_t²` is
constant. So the storage terms `½P(δθ_{t+1}² − δθ_t²)` vanish at every
stage, and each stage residual equals `½ε²f(π)`. □

**Proposition 3.7 (`n = 1`: the converse).** Let `n = 1`, `a := F_θ ≠ ±1`,
`c := F_u ≠ 0`, and write `Q, S, R` for `ℒ_θθ, ℒ_θu, ℒ_uu`. The stage
condition for a stationary storage `P` is
`M(P) = [[Q + P(a² − 1), S + Pac], [S + Pac, R + Pc²]] ⪰ 0`. Then:

- (a) `M(P) ⪰ 0` if and only if `f(0) ≥ 0`, `f(π) ≥ 0` and
  `|m₀ − 2c²P| ≤ |1 − a²|·√(f(0)f(π))`, where `m₀ = Qc² − 2Sac + R(a² − 1)`.
  So a stationary quadratic storage exists if and only if `f(0) ≥ 0` and
  `f(π) ≥ 0`, and the admissible `P` form an interval of length
  `|1 − a²|√(f(0)f(π))/c²`.
- (b) `f(ω)|e^{iω} − a|² = Qc² + 2Sc(cos ω − a) + R(1 − 2a cos ω + a²)` is
  affine in `cos ω`. So `f ≥ 0` on the whole circle if and only if
  `f(0) ≥ 0` and `f(π) ≥ 0`: for `n = 1` the frequency condition of the KYP
  lemma reduces to its two endpoints.

*Proof.* (b) Insert `Re G = c(cos ω − a)/|e^{iω} − a|²` and
`|G|² = c²/|e^{iω} − a|²`. (a) `M(P) = M₀ + PN` with `M₀ = [[Q, S], [S, R]]`
and `N = [[a² − 1, ac], [ac, c²]]`. The vectors `v₊ = (c, 1 − a)` and
`v₋ = (c, −1 − a)` (in `(δθ, δu)`) satisfy `aδθ + cδu = ±δθ`, so
`v₊ᵀNv₊ = v₋ᵀNv₋ = 0`; they are independent (determinant `−2c`), and
`v₊ᵀNv₋ = −2c²`. In the basis `(v₊, v₋)`,
`M(P) ≅ [[m₊, m₀ − 2c²P], [m₀ − 2c²P, m₋]]` with
`m₊ = v₊ᵀM₀v₊ = (1 − a)²f(0)` (since `G(0) = c/(1 − a)`),
`m₋ = v₋ᵀM₀v₋ = (1 + a)²f(π)` (since `G(π) = −c/(1 + a)`), and
`m₀ = v₊ᵀM₀v₋`. A symmetric `2 × 2` matrix is positive semidefinite if and
only if its diagonal entries and its determinant are nonnegative. □

*Check (`revision_catmix.py` Part E, mpmath 50 digits).* For the catmix
trapezoidal rule at `h = 1/100` and `1/400`, `m₊ = (1 − a)²f(0)` and
`m₋ = (1 + a)²f(π)` hold to `1e-47`. As a sanity check, no `P` on a grid
around `m₀/(2c²)` makes `M(P)` positive semidefinite (`f(π) < 0`). For the
exact flow at `h = 1/100` the admissible interval has half-width `0.219`,
and `M(P) ≻ 0` at its centre.

**Remark 3.8 (`n ≥ 2`; cited).** For `n ≥ 2` the stage condition is the
non-strict discrete-time KYP matrix inequality. Megretski (2010,
Theorem 1.4; read) states it explicitly: if `(A, B)` is controllable, a
symmetric `P` with `σ(x,u) + xᵀPx − (Ax + Bu)ᵀP(Ax + Bu) ⪰ 0` exists if and
only if `σ ⪰ 0` on `L(z) = {(x,u) : zx = Ax + Bu}` for every `|z| = 1`. (His
storage has the opposite sign to ours. Where `det(zI − A) ≠ 0`, the
condition on `L(z)` is `f(ω) ⪰ 0` for the matrix symbol.) The first version
cited Rantzer (1996) for this; I could not access that paper, and the
review could not confirm that it states the discrete-time version, so I no
longer rely on it.

For non-stationary storages on a finite arc, boundary terms of size
`|P|η² = O(h²ε²)` enter. They are negligible for Euler (`f(π) ~ h²` per
stage, summed over `1/h` stages), but not when `f(π) ~ h³`: then they are
of the same order as the whole-arc sum `(1/h)·h³ε²`. The review measured
this at the catmix saddle point: the plain alternating direction on the
free block has **positive** curvature (`+9.0e-7` at N = 100), while a
tapered alternating direction has `−2.46e-8`, close to the symbol value
`−2.60e-8` (review, check `v6b`).

**Remark 3.9 (the oscillation length and conjugate points; heuristic
where stated).** Let `n = 1` and `R = ℒ_uu ≠ 0`. On a stationary run of
fractional stages, the linearized first-order conditions (state equation,
costate equation, stationarity in `u`) reduce to a recursion
`(δθ_{t+1}, λ_{t+1}) = Φ(δθ_t, λ_t)` with `det Φ = 1`. Eliminating
`δu_t = −(Sδθ_t + cλ_{t+1})/R` gives
`tr Φ/2 = (Qc² − 2Sac + R(1 + a²))/(2(aR − cS)) = −(m₊ + m₋)/(m₊ − m₋)`
(notation of Proposition 3.7). So the eigenvalues `z, 1/z` of `Φ` satisfy
`(z + 1/z)/2 = cos ω₀ := −(m₊ + m₋)/(m₊ − m₋)`, which is the zero of the
affine function `N(cos ω) = f(ω)|e^{iω} − a|²` of Proposition 3.7(b)
(`N(1) = m₊`, `N(−1) = m₋`).

- If `f(π) < 0 < f(0)`, then `m₋ < 0 < m₊`, `|cos ω₀| < 1`, and **every**
  solution is `(−1)^t (A cos d₀t + B sin d₀t)` with `d₀ = π − ω₀`: an
  alternating mode whose envelope changes sign every `π/d₀` stages and does
  not decay. No solution decays away from the junctions. (This is exact for
  the stationary linear recursion.) The condition cannot be replaced by
  `f(π) < 0 < f''(π)`: for `(a, c, Q, S, R) = (−0.5, 1, −2, −0.25, 1)`,
  `f(0) = −0.22`, `f(π) = −6` and `f''(π) = 26`, but `m₊ = −0.5` and
  `m₋ = −1.5` have the same sign, and the eigenvalues are real (3.73 and
  0.27).
- If `f > 0` on the circle, then `m₊, m₋ > 0` and `|cos ω₀| > 1`, so the
  eigenvalues are real. They are negative if `m₊ > m₋` and positive if
  `m₋ > m₊`. Example of the second case: `(a, c, Q, S, R) = (0.5, 1, 1, 0, 1)`
  has `min f = f(π) = 1.44 > 0`, `m₊ = 1.25`, `m₋ = 3.25`, and eigenvalues
  4.27 and 0.23. (Both examples: `revision2_catmix.py` Part M, with `Φ`
  built from the linear equations directly, not from the formula above.)
- *Small `h` (heuristic).* For a consistent scheme, `m₋ = (1 + a)²f(π) ≈
  4f(π)`, and `m₊ ≈ Kh³`: for `|1 − a| ≪ ω ≪ 1`, `f(ω) ≈ m₊/ω²`, while
  Goh's form gives `Kh³/ω²` there (the triangle-wave argument below, at
  frequency `ω`). With `f(π) = φh³`, this gives
  `tr Φ/2 ≈ −(K + 4φ)/(K − 4φ)`, so for `f > 0` the eigenvalues are negative
  when `4φ < K`. Catmix numbers (Part M): `m₊/h³ = 6.13, 6.23, 6.27` at
  `h = 1/100, 1/200, 1/400`, against `K = 6.32`.
  - Exact flow: `m₋/h³ = 2.04, 2.08` at `h = 1/100, 1/200`, against
    `4K/12 = 2.11`; `tr Φ/2 = −2.0001, −2.00003`. So the eigenvalues are
    about `−0.268` and `−3.73`: the alternating modes decay by a factor
    `0.27` per stage and stay at the junctions.
  - Trapezoidal rule: `m₋/h³ = −0.106, −0.107, −0.108`, against
    `4φ = −0.109`; the small-`h` form gives `tr Φ/2 = −0.966071`, within
    `3e-7` of the values below.
- Catmix, trapezoidal rule (Part A and E): `cos ω₀ = tr Φ/2 = −0.96607`,
  `d₀ = 0.26124` rad per stage, so `π/d₀ = 12.03` stages at `h = 1/100`,
  `1/200` and `1/400` (the same to five digits; by the small-`h` form it
  has a limit as `h → 0`, heuristic). The Taylor estimate
  `d₀ ≈ √(2|f(π)|/f''(π)) = 0.2627`, with `f''(π) = 0.79058h³`, is the one
  the review proposed.

Heuristic consequences, checked only numerically (Sections 5.5, 5.6):

- *Oscillating KKT points.* Near the stationary point, a KKT point with the
  bang–singular–bang active set can deviate from it only through these
  alternating modes. The state entering the arc differs from `θ_s^h` by
  `O(h)` (the junction does not fall on the grid), and an alternating
  control of amplitude `ε` moves `θ` by only about `|F_u|ε/2 = O(hε)`. So a
  control amplitude of order 1 is to be expected, and no smooth KKT point
  with this active set exists in general. This argument uses `n = 1` and
  `ℒ_uu ≠ 0`. In E2 (Section 4.3; `bᵀw < 0`) the KKT point with the
  continuous structure is smooth, but E2 differs from the catmix
  trapezoidal rule in two ways: it has `n = 2`, and it uses Euler, whose
  Lagrangian is affine in `u` (`ℒ_uu = 0`, outside the hypothesis of this
  remark). With more states, other (hyperbolic) modes may absorb the
  mismatch, but which of the two differences matters was not checked.
- *Conjugate points.* For the stationary accessory problem, the envelopes
  of the Jacobi solutions change sign every `π/d₀` stages, so a
  Riccati-type (maximal) recursion cannot stay exact over much more than
  `π/d₀` stages.
- *Counts.* `f < 0` on an arc of length `2d₀` around `π`, so a Toeplitz
  section of `m` stages has about `m d₀/π` negative eigenvalues. For the
  recursion breaks, the count `m d₀/π = m/(π/d₀)` only restates the
  spacing; it is not a separate prediction. A discrete Morse index theorem
  would link the two counts (not checked).

*Schemes compared (generic `n = 1`, symbolic, `catmix_continuous.py`
Part 2).* With the continuous tangential calibration
`φ = ψ_sθ + ½P_sθ² + C_3θ³/6`:

- explicit Euler gives stage control curvature exactly `h²·bw` (no `h³`
  term);
- the exact flow (piecewise-constant control, exact integration) gives
  `0·h² + (K/3)h³`.

The invariant `f(π)` of the exact flow was computed for catmix as
`0.52703h³`, against `K/12 = 0.52705`. *Heuristic reason:* an alternating
control of amplitude `ε` makes `v = ∫δu` a triangle wave of amplitude
`εh/2`. By Goh's form its cost is `½K⟨v²⟩ = Kε²h²/24` per unit time, that
is `½ε²·(Kh³/12)` per step. So for the exact flow **the alternating
direction is stabilized by Kelley's condition itself, at order `h³`**. A
scheme with an `O(h³)` defect of the wrong sign can undo it; the COPS
trapezoidal rule does, on catmix (Section 5.4).

## 4. Test E2: a 2-D problem with a bang arc and a singular arc

**4.1 Problem** (`lqsing.py`). `ẋ₁ = u`, `ẋ₂ = x₁ − x₂`, `u ∈ [−1,1]`,
`x(0) = (1,0)`, `T = 3`, with cost

```
J = ∫_0^T [ (x₁² + x₂²)/2 + (k₁x₁ + k₂x₂)u ] dt + ½ x(T)ᵀ diag(k₂ − k₁, K) x(T),
```

where `k₂ = 1/4` and `K = 1 − 2k₂ = 1/2`.

- `k₁` enters only through the null Lagrangian `d/dt(k₁x₁²/2)`,
  compensated in the terminal term, so the continuous problem does not
  depend on `k₁` (`J(k₁) = J(0) − k₁/2`).
- `b = e₁`, `w = −(k₁, k₂)`, `bᵀw = −k₁`. The Kelley quantity is
  `K = 1 − 2k₂ = 1/2` (from `σ̈ = −(1 − 2k₂)u + …`), and `c₁ = 0` because
  `b` is constant and `ℓ_1` affine. So `a_j = K > 0` in
  Proposition 2.1(c).
- The component `w₂ = −k₂ ≠ 0` is orthogonal to `b`, so the tangential `P`
  is not trivial.

**Extremal (float check, `σ` computed by backward integration):**

- `u = −1` on `[0, t₁)`, with `t₁ = 1.1982904373` the root of
  `3 − 2t − 2e^{−t} = 0`.
- Then a singular arc on the stable line `x₂ = −x₁`, with `u_s = −2x₁`
  (`u_s(t₁) = 0.396`), up to `T`. The terminal term makes the arc
  compatible with the transversality conditions at `T`.
- `σ > 0` on `[0, t₁)` (minimum `1.25e-7` at the last sample), and
  `σ(t₁ − s)/s² → 0.3491`, against `½K|u_b − u_s| = 0.34915`
  (Proposition 2.1(a)).
- `J* = 0.3989691259` for `k₁ = −1/2`.

**Continuous calibration (exact, by hand).** Take
`P = [[−k₁, −k₂], [−k₂, p₂₂]]`. It is tangential everywhere
(`Pb = w`, `β ≡ 0`), and `M = [[K, p₂₂ + k₂], [p₂₂ + k₂, ṗ₂₂ − 2p₂₂ + 1]]`
(Remark 1.4). The data are exactly quadratic, so `r = σω + ½dᵀMd`.

- With `p₂₂ ≡ 1/4` (a fixed point of `ṗ₂₂ = 2p₂₂ − 1 + (p₂₂ + k₂)²/K`),
  `M = ½[[1,1],[1,1]] ⪰ 0` and `F − P = ¼[[1,1],[1,1]] ⪰ 0`. This is a
  **global** calibration on `[0,T] × R² × U`, so the extremal is globally
  optimal.
- With `p₂₂ = 1/4 − δ`, `0 < δ < 2`, it is strict.
- Its `b–b` entry is `K = 1/2`, as Proposition 1.3 says.

**Discrete tests** (`lqsing_run.py`). Euler; the float QP gives the active
set; an **exact rational KKT point** is obtained by forward shooting in
`p_0`, and all KKT signs are checked exactly. Families:

- **A**: affine;
- **B1**: `S_t = p_tᵀx + ½(x − x̄_t)ᵀP_δ(x − x̄_t)` with `δ = 1/10`, the
  continuous tangential calibration transferred;
- **B2**: the discrete maximal recursion of [E, Lemma 10] with margin
  `ε = 0.01`, computed in floats and rounded to dyadic rationals.

The stage residuals are exactly quadratic in `(d, ω)`. So exactness over
`R² × U` is decided exactly by [E, Lemma 10], in rational arithmetic, and
an exact stage-wise family is a global certificate: bound equals the
discrete KKT value. `lqsing_selftest.py` checks the quadratic model
against the residual evaluated from its definition, at random rational
points, and checks the telescoping identity. The difference is 0 in both
checks, for A and B1 and for all three `k₁`.

**4.2 Results, `k₁ = −1/2` (`bᵀw = +1/2`)** (`logs/lqsing_k1_m1_2.jsonl`):

| N | discrete optimum J | first fractional stage (time) | A: failing (bang / fractional) | A: bang window starts | A: loss | B1, B2 |
|---|---|---|---|---|---|---|
| 50 | 0.435370076042 | 0.96 | 46 (12 / 34) | 0.24 | 0.676 | 0 failing; exact certificate |
| 100 | 0.417127566403 | 1.05 | 91 (26 / 65) | 0.27 | 0.683 | same |
| 200 | 0.408067608991 | 1.08 | 182 (54 / 128) | 0.27 | 0.692 | same |
| 400 | 0.403534320192 | 1.1175 | 364 (113 / 251) | 0.27 | 0.701 | same |
| 800 | 0.401259869978 | 1.14 | 727 (231 / 496) | 0.27375 | 0.708 | same |
| 1600 | 0.400118057044 | 1.156875 | 1454 (471 / 983) | 0.27375 | 0.714 | same |

- **Tangential families:** no failing stage at any `N`, including the
  vertex stages next to the junction. `B = J` holds exactly in rational
  arithmetic, so each row is a certificate of global optimality of the
  discrete KKT point. (The reduced QP is also convex here, minimum Hessian
  eigenvalue `1.9e-3` at `N = 50` down to `1.8e-6` at `N = 1600`, so this
  is a test of the calibration mechanism, not a hard instance.)
- **Affine family:**
  - it fails on every fractional stage (Proposition 3.2) and on a bang-side
    window;
  - the window's start is predicted by `σ(t) = Δ|w|²/(2μ) = |k|² = 0.3125`
    ([R, Theorem 2.3(2)] with `K_t = hI`), that is `t = 0.2733`: a window
    of fixed duration 0.925;
  - its loss tends to about 0.71, `Θ(1)`.
- **Discrete junction layer:** the first fractional stage comes *before*
  `t₁` by 0.238, 0.148, 0.118, 0.081, 0.058 and 0.041 time units
  (N = 50 … 1600). That is `O(√h)` (a factor 2.9 between `N = 200` and
  `1600`, against `√8 = 2.83`), the cheap-control layer of Proposition 3.4.
  B1 is unaffected because here `β_t = hg_xᵀw` does not depend on the
  discrete state.

**4.3 Results, other gauges** (`logs/lqsing_k1_0.jsonl`,
`logs/lqsing_k1_p1_2.jsonl`). The continuous problem is the same.

- **`k₁ = 0` (`bᵀw = 0`), N = 50, 100, 200, 400, 800:**
  - Discrete optimum `J` = 0.168449674988, 0.158475966255, 0.153665437464,
    0.151303155754, 0.150132628184 (`J* = 0.1489691259`).
  - The reduced Hessian is positive definite with minimum eigenvalue
    `8.2e-5, 1.0e-5, 1.3e-6, 1.6e-7, 2.0e-8`. That scales like `h³`
    (`≈ 0.375h³`), so the alternating direction is stabilized only at the
    next order (Remark 3.5).
  - A fails on all fractional stages plus a bang window starting at
    0.78–0.795 (prediction for `|k|² = 1/16`: 0.7858); loss
    0.102–0.104.
  - B1 has `κ_t = 0` and `β_t = O(h)`. It fails on every fractional stage,
    with loss `2.6e-3, 6.6e-4, 1.6e-4, 4.1e-5, 1.0e-5`, that is `O(h²)`.
    At N = 800 it also fails one bang stage (`t = 1.1925`, the last stage
    before the first fractional stage).
  - B2 has no failing stage and is an exact certificate at every `N`. On
    its fractional stages `κ_t ≈ 0.91h > 0` (median `0.919h` and `0.913h`
    at N = 200 and 800) and `|β_t| ≈ 0.95h` (median of the Euclidean norm;
    the 90% quantile is also `0.95h`). So the tangency defect is `O(h)`,
    well inside the `√h` tolerance of Lemma 3.1, and the recursion trades it
    for positive control curvature. It does not impose exact discrete
    tangency, which would give `κ_t = hk₂ + O(h²)`. The exception is the last
    stage, where `|β_t| = 0.34`: B2 starts from `P_N = F − 2εI`, which is not
    tangential, and its first step makes that stage exact through an `O(1)`
    drop of `P` (the mechanism of Remark 3.3a).
  - The junction layer is `O(h)`: the first fractional stage comes before
    `t₁` by 0.058, 0.028, 0.013, 0.006 and 0.002.
- **`k₁ = +1/2` (`bᵀw = −1/2`), N = 50, 100, 200, 400:**
  - The reduced Hessian has about `N` negative eigenvalues (46, 94, 192 and
    388, from the review). The minimum is `−1.72e-3, −4.40e-4, −1.11e-4,
    −2.80e-5`, against `h²bᵀw = −1.80e-3, −4.50e-4, −1.12e-4, −2.81e-5`
    (Remark 3.5).
  - *KKT point with the continuous structure* (`revision_e2.py`): the
    active set of the `k₁ = 0` optimum (bang, then free), solved exactly in
    rationals, with all KKT signs checked. Unlike the catmix saddle point
    (Section 5.5), it is smooth on the arc: its controls deviate from the
    neighbour average by at most `1.3e-2, 4.2e-3, 1.4e-3, 3.8e-4`. It has
    `(J_smooth − J*)/h = +0.040, +0.020, +0.011, +0.005`, so
    `J_smooth − J* = o(h)` here. This is partly a coincidence of the
    example: the Euler error in the `k₁ = 0` gauge is about `+0.31h`, and the
    gauge term `−¼h²Σu_t² ≈ −¼h∫u*² = −0.309h` almost cancels it. The
    point is a saddle (Remark 3.5).
  - *Chattering points.* The best points found **chatter between the
    vertices**, with one fractional stage each. Three L-BFGS-B multistart
    procedures were used: the first version's 23 starts, the review's 31
    starts, and 64 new starts with another seed (`revision_e2.py`). Every
    one of the 64 new starts ended at a different local value, so there are
    many local minima. Best values found, KKT signs checked exactly:
    `J` = −0.12419752, −0.11340107, −0.10737058, −0.10424644. At N = 100 the
    new run found the lowest value; the first version had −0.11330285 and
    the review −0.11339182. (The first version's N = 100 point had no
    fractional stage; its counts were 1, 0, 1, 1, not "0, 1, 1, 1" as first
    written.)
  - *Size of the gain.* Relative to the KKT point with the continuous
    structure, `(J − J_smooth)/h = −0.426, −0.432, −0.433, −0.433`. The
    prediction concerns exactly this comparison: chattering between `±1`
    replaces `u_s²` by 1 in the extra term `−¼h²Σu²`, which gives
    `−¼h∫_arc(1 − u_s²) = −0.441h`. Relative to `J* = −0.10103`,
    `(J − J*)/h = −0.386, −0.412, −0.423, −0.429`. The first version compared
    with `J*` directly; that is valid here only because
    `J_smooth − J* = o(h)`.
  - A loses 1.36–1.48; B1 fails on 18–139 stages (tests run at the first
    version's points).
  - B2 breaks at `t = 2.88, 2.88, 2.97, 2.985` (`m_t ≤ 0`), so by
    [E, Corollary 11] no quadratic stage-wise family with these costate
    slopes is exact on all later stages and at the break stage.
  - Global optimality of the chattering points is not established.

## 5. catmix

**5.1 Exact reduction.** COPS catmix is `ẋ₁ = u(10x₂ − x₁)`,
`ẋ₂ = u(x₁ − 10x₂) − (1−u)x₂`, `x(0) = (1,0)`, `u ∈ [0,1]`, `T = 1`,
minimize `x₁(1) + x₂(1) − 1`. With `m = x₁ + x₂` and `θ = x₂/m`:

```
ṁ = −(1−u)θ m,   θ̇ = a(θ) + b(θ)u,   a = θ² − θ,   b = 1 − 10θ − θ²,
J + 1 = exp(C),  C = ∫_0^1 (−θ + θu) dt.
```

So catmix is a 1-D Lagrange problem (`ℓ_0 = −θ`, `ℓ_1 = θ`) up to a
monotone transform. A reduced calibration `φ(t,θ)` gives the Mayer
calibration `S = m·exp(φ)`, whose residual is `S` times the reduced
residual. This is the structural reason why the DP of [C] lives on a 1-D
projective separator.

**5.2 Singular data (exact, symbolic; `catmix_continuous.py` Part 1).**
On `σ = 0`, `σ̇ = 0` reduces to `111θ² − 22θ + 1 = 0`.

| quantity | exact | value |
|---|---|---|
| `θ_s` | `(11 − √10)/111` | 0.0706101111697 |
| `u_s` | `−1/13 + 5√10/52` | 0.227142082708 |
| `ψ_s` | `5/52 − 7√10/65` | −0.244399132634 |
| `w_s` | `−11√10/10` | −3.47850542619 |
| `P_s = w_s/b_s` | `−3113/260 − 11√10/520` | −12.0399712582 |
| `K = −∂_uσ̈` | `2√10` | 6.32455532034 |
| `b_s w_s` | `(22√10 − 12452)/12321` | −1.0049857878 |
| `c₁` | `(28169128 − 74672√10)/1367631` | 20.4243647611 |
| `b_s²M(u*)` | `2√10` (= `K`, Remark 1.4) | 6.32455532034 |
| `K + (u − u_s)c₁` at `u = 0`, `1` | | 1.68532, 22.1097 |

- Strict Kelley holds.
- The vertex condition of the quadratic class (Proposition 1.5(a)) holds
  on the arc, so a quadratic tangential calibration exists along the arc
  (Proposition 1.6).
- At the junctions the quadratic class needs Proposition 2.1(c)
  (Section 5.3). It fails at the entry junction `t₁`, where a cubic term in
  `θ` is needed (Proposition 2.1(b)).
- `P_s < 0`: the tangential curvature is concave, consistent with the
  concavity of the value function in `y` used by [C].
- `bw < 0`: Euler in `θ` has the wrong sign (Section 3).

**5.3 Junctions (float, `catmix_junctions.py`).**

- `t₁ = 0.136299034595` and `t₂ = 0.725230107592`;
  `J* = −0.048055685860877`. [C]'s discrete optima for N = 100, 200, 400
  and 800 lie below it by 1.37e-5, 3.5e-6, 8.6e-7 and 2.2e-7, a rate of
  `O(h²)`. (The trapezoidal transcription is not a restriction of the
  continuous problem, so its optimum may lie on either side.)
- The minimum-principle signs hold on both bang arcs.
- `σ(t₂ + s)/s² → 0.71829` and `σ(t₁ − s)/s² → −2.4440`, against
  `−½K(u_b − u_s)` = 0.718286 and −2.443991 (Proposition 2.1(a)).
- Layer number at `t₂` (last arc `u = 0`, `Q(1) = 0`): `Q(t₂+) = −0.0597`
  and `η_L = b_s²(Q(t₂+) − P_s) = 1 > 0` (Remark 2.2). This holds
  **exactly**: on the last arc the reduced cost-to-go is
  `V = log(1 − θ(1 − e^{−τ}))` (`τ` the time to go), so `Q = V_θθ = −ψ²`;
  with `bψ = −θ` at the junction (`σ = θ + bψ = 0`) and
  `w = −(1 − (10 + 2θ)ψ)`,
  `η_L = −b²ψ² + b(1 − (10 + 2θ)ψ) = −θ² + (1 − 10θ − θ²) + (10 + 2θ)θ = 1`.
  (Symbolic check: `revision_catmix.py` Part D.)
- Quadratic-class junction numbers (Proposition 2.1(c); exact data of
  5.2):
  - entry junction `t₁` (`u_b = 1`, `u° = 0`):
    `a_j = K − c₁ = −14.0998`, below the threshold
    `−K(1 − u_s)/4 = −1.2220`, so no calibration quadratic in `θ` exists on
    the bang side of `t₁`;
  - exit junction `t₂` (`u_b = 0`, `u° = 1`): `a_j = K + c₁ = +26.749 > 0`.
- Whether a global-form calibration exists on the whole horizon was not
  checked (the caveats of [E, Section 4] apply).

**5.4 Discrete singular points and accessory symbols** (`catmix_schemes.py`,
50-digit mpmath; the discrete singular point agrees with `θ_s`, `u_s` to
10 digits in every scheme):

| scheme | `f(π)` at `h` = 1/100, 1/200, 1/400 | limit | minimum of `f` over `ω` |
|---|---|---|---|
| Euler in `θ` | `−1.0212h², −1.0130h², −1.0090h²` | `bw·h² = −1.0050h²` | at `ω = π` |
| Euler in `x` (2-D) | `−1.0172h², −1.0085h², −1.0042h²` | `−1.000h²` | at `ω = π` |
| trapezoidal rule (COPS; Cayley map in `y = Q(u)x`) | `−0.02729h³` (all three) | `−0.0273h³` | at `ω = π` |
| exact flow | `+0.52699h³, +0.52703h³` | `Kh³/12 = 0.52705h³` | at `ω = π` (positive) |

- At `ω = π/64`, `f/h³` lies between `1.8·10³` and `2.6·10³` in every
  scheme; the minimum over the 64 grid frequencies is at `ω = π`.
- **The COPS transcription and both Euler variants make the singular arc a
  saddle (`f(π) < 0`); the exact flow does not.** By Proposition 3.6, no
  stationary quadratic calibration is exact on a long run of fractional
  stages of the COPS transcription.

**5.5 The COPS saddle and the chattering optimum** (float; `catmix_trap.py`
and `revision_catmix.py`, reduced model; it reproduces the COPS objective
of the stored N = 100 controls to `8e-16`. The review reproduced the saddle
point independently in the original 2-D trapezoidal form, with mpmath.)

- **KKT point with the bang–singular–bang active set (the saddle point),
  N = 100.** Computed by damped Newton on the 59 arc stages 14–72,
  `J = −0.0480693947983`. Audit (`revision2_catmix.py` Part K, analytic
  Hessian by a second-order adjoint, float): gradient `3.3e-17` on the arc
  stages,
  none of which is at a bound; the smallest Hessian eigenvalue in absolute
  value is `4.5e-9`, and the Newton step is `5e-10`. So this is a KKT point
  to float accuracy.
  - The first version called this point "smooth". **It is not.** Its arc
    controls oscillate from stage to stage: they range over
    `[0.055, 0.411]`, around `u_s = 0.227`, and deviate from the neighbour
    average by up to 0.353.
  - The alternating envelope `(−1)^i(u_i − (u_{i−1} + u_{i+1})/2)` changes
    sign at stages 18, 29, 40, 51 and 62: exactly every 11 stages. This is
    close to, but 9% shorter than, the spacing `π/d₀ = 12.03` that
    Remark 3.9 gives for a stationary run. The base point is far from the
    stationary point, so exact agreement is not expected.
  - No smooth KKT point was found. In the review, Newton from a smooth start
    stalled at gradient `7e-8` (review check `v7`). [C]'s smooth-start local
    solve (`J = −0.04806939757`) is another stationary point, `2.8e-9` below
    this one.
  - Hessian on the arc stages: 5 negative eigenvalues (against
    `m d₀/π = 4.9`), the most negative `−3.30e-8` in `log(J+1)`
    (`−3.14e-8` in `J`), with an eigenvector that alternates at every stage.
  - This eigenvalue lies 21% below the symbol minimum `f(π) = −2.73e-8`
    (in `log(J+1)`), and 26% below the finite-section estimate
    `f(π) + ½f''(π)(π/(m+1))² = −2.620e-8` for `m = 59` stages. A
    Toeplitz section cannot have an eigenvalue below the minimum of its
    symbol, so non-Toeplitz effects are present. The first version guessed
    junction transients (not checked). The check below points instead to
    the oscillating base point: at a smooth base point with the same
    junctions, the most negative eigenvalue lies inside the symbol range,
    within 0.1% of the finite-section estimate.
- **N = 200: an approximate stationary point only.** The damped Newton run
  with an active-set loop (`logs/catmix_trap_saddle_as.log`,
  `J = −0.0480591359149`) stopped at a point that is **not a verified KKT
  point** (Part K; this was found by the second review, R1):
  - five arc stages sit at `u = 0` (28, 118, 120, 129, 138). At 120, 129
    and 138 the gradient is `−2.8e-11`, `−2.6e-10` and `−3.6e-10`, the
    wrong sign for a lower bound;
  - on the 113 interior stages the gradient is `3.3e-9`; the analytic
    Hessian (second-order adjoint, float) there has an eigenvalue of
    `1.8e-12` (largest `1.7e-3`; central-difference Hessians give `1.0e-12`
    and `1.7e-12`, so only its order is meaningful), and the Newton step has
    `max|du| = 21`. So the stationarity residual is not resolved.
  - A time-limited semismooth Newton / Levenberg–Marquardt run on the
    Fischer–Burmeister form of the KKT conditions, with the analytic
    Hessian (Part L, 400 iterations), lowered the interior gradient to
    `1.3e-10` and then stagnated. At its end two arc stages are at `u = 0` with
    correct signs, stages 129 and 138 sit at `u ≈ 1e-4` with gradient
    `−7e-11` and `−8e-11`, the smallest Hessian eigenvalue is `2.1e-10`,
    and the Newton step is still `0.22`. A 4000-iteration rerun ended in
    the same state. So no verified KKT point with this active set was found
    at N = 200.
  - Qualitatively the approximate point oscillates like the N = 100 point:
    its arc controls cover `[0, 0.468]` (`[0.037, 0.468]` on the interior
    stages), the largest deviation from the neighbour average is 0.468
    (stage 119, between two zero stages), and the envelope changes sign at
    stages 31, 43, 54, 66, 78, 89, 101 and 112 (mean spacing 11.6), and
    irregularly after that, where the zero stages lie. Its Hessian has 7
    negative eigenvalues (against `m d₀/π = 9.4` for its 113 interior
    stages), the most negative `−4.22e-9`, 24% below `f(π) = −3.41e-9`.
    Because the point is not a KKT point, these numbers are indicative only
    and are not used below.
- **Smooth reference** (`revision_catmix.py` Part C). This is the best
  control that is piecewise linear in the stage index on the arc, with knots
  every `s = 4`, 6 or 10 stages (`s ≥ 4` excludes the alternating mode). The
  first and last arc stages are free, so they can absorb the `O(h)` state
  mismatch at the off-grid junctions. The bang stages are those of the
  saddle point (N = 100) or of the approximate N = 200 point (both bang
  arcs as in the stored COPS point: `u = 1` before stage 28, `u = 0` after
  stage 145), or of the stored COPS point (N = 400); only this stage layout
  is taken from those points. The
  reference is a constrained minimizer, not a KKT point of the full problem:
  its gradient on the arc stages is up to `9e-8`, `2e-8` and `8e-10` at
  N = 100, 200 and 400. The prediction in the table is
  `½u_s²|f(π)|(t₂ − t₁)/h·(J+1)`: the per-stage gain of alternating at the
  maximal amplitude `ε = u_s`, over the `(t₂ − t₁)/h` arc stages.

  | N | `J_ref − J_chatter` (s = 4, 6, 10) | predicted gain | ratio | `J_ref − J_saddle` |
  |---|---|---|---|---|
  | 100 | 3.93e-8, 3.98e-8, 4.03e-8 | 3.95e-8 | 0.995–1.021 | 2.0e-9 – 3.0e-9 |
  | 200 | 9.84e-9, 9.80e-9, 10.11e-9 | 9.87e-9 | 0.993–1.025 | not reported (no verified KKT point) |
  | 400 | 2.45e-9, 2.47e-9, 2.46e-9 | 2.47e-9 | 0.992–1.001 | (no saddle point computed) |

  - Without free junction stages the reference is worse, and the ratio is
    1.23–1.65 (N = 100), 1.55–3.20 (N = 200) and 1.00–1.11 (N = 400).
  - Hessian at the best reference point: the most negative eigenvalue is
    `−2.618e-8` (N = 100, 59 interior stages) and `−3.375e-9` (N = 200, 118
    stages), against `f(π) = −2.73e-8` and `−3.41e-9`, and against the
    finite-section estimates `−2.620e-8` and `−3.376e-9` (within 0.1%).
    There are 4 and 10 negative eigenvalues, against `m d₀/π` = 4.9 and
    9.8 (Remark 3.9). The eigenvector alternates at every stage.
- **Stationary 2-cycle** (`revision_catmix.py` Part B, mpmath). The best
  2-periodic orbit with controls `(v, 0)` has `v = 0.454285 ≈ 2u_s`. Its
  gain per stage over the stationary point equals `½u_s²|f(π)|` to a
  relative `1e-6` (the quartic correction at amplitude `ε = u_s` is
  `−9.4e-7` relative). So the per-stage content of the prediction holds even
  at the full amplitude `ε = u_s`, which the lower control bound imposes
  (hence the controls `2u_s = 0.4543` and 0).
- **What the comparisons show, and what they do not.**
  - The first version compared the chattering point with the oscillating
    KKT point: `3.72e-8` (N = 100) and `9.67e-9` (N = 200, the approximate
    point), against the predicted `3.95e-8` and `9.87e-9`, and called this
    a quantitative match. That compared unlike quantities (review F1), and I
    withdraw the claim.
  - Against the smooth reference with free junction stages, the gain agrees
    with the prediction within 3% at N = 100, 200 and 400, and scales like
    `h²`.
  - This is still a heuristic check, not a confirmation. The prediction
    ignores boundary terms at the junctions, which are of the same order
    `h²ε²` as the whole-arc gain (Remark 3.8). The reference is also a
    choice: with fixed junction stages the gain changes by up to a factor
    3.2 (N = 200). At N = 100 the J values of the near-smooth reference
    points, the oscillating KKT point and [C]'s point spread over `6e-9`,
    about 15% of the gain.
  - [C]'s "3.4e-8" is measured against its own local solve
    (`−0.04806939757`), which [C] calls the MINLPLib value. MINLPLib lists
    `−0.04806939108` (full precision; `treewidth-census/instancedata.csv`).
    The gap of the chattering point to that value is `4.10e-8`, and [C]'s
    local solve lies `6.5e-9` below it.
- At N = 400 the damped-Newton saddle computation did not converge
  (gradient `1.7e-7`, controls leaving `[0,1]`) and was not rerun. The
  smooth reference above replaces it for the gain comparison.

**5.6 Calibration screening on the COPS optimum** (float; the reduced
problem is 1-D, with residuals over `θ ∈ [0,1]`, `u ∈ [0,1]`).

- *Chattering KKT points,* polished by Newton on their interior stages
  (`catmix_windows.py`): gradients `2e-17`–`4e-17`, KKT signs verified
  (float). `J` = −0.0480694320309772, −0.0480591455801168,
  −0.0480565477567615 for `N` = 100, 200, 400. These are float values of
  float-polished controls, not certified.
- *Affine family* (`catmix_calib.py`, grid plus local refinement):
  - over the full range `θ ∈ [0,1]` it fails at 100/101, 200/201 and
    400/401 stages, with loss 0.89–0.91 in `log(J+1)`;
  - within `|θ − θ̄_t| ≤ 0.01` it fails at all fractional stages, at the
    bang stages from `t ≈ 0.05`, and on the whole last arc, with loss
    0.0170, 0.0190 and 0.0200: `Θ(1)`, as Proposition 3.2 predicts;
  - on the last arc the failure is a Mangasarian (SGM) failure:
    `H_θθ = 2ψ(1−u) < 0`, like optcdeg2's tails in [R, 5.2].
  - This confirms the expectation in [C, Section 4] that a fixed-costate
    Lagrangian "would lose first-order".
- *Maximal quadratic recursion,* quadratic model over `θ ∈ R` and the
  control box, 1-D windowed analogue of [E, Lemma 10]:

  | N | stage-wise (L = 1): breaks | windows of 2 stages: breaks | windows of 4 stages: breaks |
  |---|---|---|---|
  | 100 | 5 (stages 17, 29, …, 65: every 12 stages) | 1 (t = 0.63) | 1 (t = 0.61) |
  | 200 | 10 (stage 30, then 39, 51, …, 135: every 12 stages) | 1 (t = 0.155) | 1 (t = 0.145) |
  | 400 | 20 (stage 55, then 64, 76, …, 280: every 12 stages) | 1 (t = 0.1375) | 1 (t = 0.1325) |

  - The maximal `P` on the arc stays in `[−12.16, −11.72]`, close to the
    continuous tangential value `P_s = −12.04`, as tangency predicts.
  - Break stages (`logs/revision2_windows_L1.log`; the arcs of the
    chattering points start at stages 14, 28 and 55). At N = 100 all five
    breaks are 12 stages apart. At N = 200 and 400 the first break lies
    near the entry junction (stage 30, 2 stages into the arc; stage 55, the
    first arc stage), at or next to the unexplained 2-stage-window break
    below. It is followed by a gap of 9 stages, and all later breaks are
    exactly 12 stages apart.
  - This periodic spacing matches the conjugate-point spacing
    `π/d₀ = 12.03` stages of Remark 3.9 (computed at the three `h`). The
    counts of periodic breaks, 5, 9 and 19, agree with `m d₀/π` = 4.9, 9.8
    and 19.6 for the `m` = 59, 118 and 236 arc stages, but that is the same
    observation as the spacing, not a second check. The match is
    heuristic: the recursion restarts from `P = 0` after each break, and
    the arc is not stationary near the junctions. (It replaces the first
    version's qualitative reading, "the band of admissible `P` is narrow";
    by Proposition 3.7 that band is empty when `f(π) < 0`.)
  - Windows aligned with the chattering period remove all but one break.
    Letting a failing window grow to 6 stages did not remove that break
    (`logs/catmix_windows_adaptive.log`).
  - *Where the remaining 2-stage-window break lies.* In the reduced scheme,
    stage `i` (control `u_i`) covers about `[t_i − h/2, t_i + h/2]`.
    - N = 400: the failing window is stages 55–56, the first two arc
      stages. Stage 55 starts 0.02 stage before `t₁ = 0.1363`, so the
      window lies on the arc side of the junction.
    - N = 200: stages 31–32 (`t = 0.155`), 3–4 stages into the arc (the
      first arc stage is 28).
    - N = 100: `t = 0.63`, inside the arc.
    - With windows of 1 or 2 stages, no window of bang stages breaks at any
      `N`. (With 4-stage windows at N = 400, the failing window, stages
      53–56, straddles the junction.)

    Proposition 2.1(c) concerns the bang side of `t₁`. The first version
    read the N = 200 and 400 breaks as "the discrete trace of that
    obstruction" and called them expected. The locations do not support
    this, and I withdraw that reading: the remaining break is unexplained.
    (One possible factor, not checked: after a break the recursion restarts
    from `P = 0`, which removes the tangency at `t₁` on which
    Proposition 2.1(c) relies.)
  - The true (nonlinear, global-in-`θ`) window residuals of this family
    were not checked, and no certificate was built.
- *What this means for [C].* The COPS DP certificate is not a
  stage-wise quadratic calibration: [C]'s grid has about 14,000 rays per
  stage, including a dense band around the singular point. The screening
  and Proposition 2.1 suggest that a much smaller certificate might use:
  - quadratic storage in `θ` at every second stage, with 2-stage windows
    (3-D checks in `(θ, u_i, u_{i+1})`);
  - a cubic term in `θ` near the entry junction (Proposition 2.1(c),
    continuous time);
  - some treatment of the one remaining window break, whose cause is
    unknown.

  This is a conjecture, not tested beyond the quadratic model.

## 6. What remains open

- Existence of a global tangential calibration for catmix on the whole
  horizon (bang arcs in the global form of [E, Section 4]). It must be
  cubic or higher in `θ` near the entry junction (Proposition 2.1(c)).
- A proof of Remark 1.4 (the reduced Riccati condition for `n ≥ 2`), of
  the sufficiency half of Remark 2.2 for quadratic `σ`, and of
  Proposition 2.1(c) in the range `−γ/(2Δ) ≤ a_j ≤ 0`.
- The discrete convergence rate `e_h` near junctions: E2 shows an `O(√h)`
  layer when `bᵀw > 0` (Proposition 3.4 needs `e_h = o(√h)`, or discrete
  tangency).
- The general law `f(π) = Kh³/12 + (scheme defect)·h³` for exact-flow-like
  schemes: shown for the exact flow on catmix numerically and
  heuristically, not proved.
- The trapezoidal defect was only computed for catmix.
- A controlled asymptotic for the chattering gain when `f(π) ~ h³`: the
  junction boundary terms are of the same order as the gain (Remark 3.8),
  and the "smooth" baseline is not a KKT point (Section 5.5).
- A proof that, for `f(π) < 0`, generic KKT points with the
  bang–singular–bang active set oscillate with an `O(1)` control amplitude
  (Remark 3.9 gives the linear mechanism only), and a proof of the
  conjugate-point reading of the 12-stage breaks (a discrete Morse index
  statement for the maximal recursion with resets).
- A verified KKT point with the bang–singular–bang active set for the COPS
  transcription at N ≥ 200 (Section 5.5: at N = 200 only an approximate
  stationary point with a nearly singular Hessian was found), or evidence
  that none exists with this active set.
- Whether the linear mechanism of Remark 3.9 needs `ℒ_uu ≠ 0`, and whether
  E2's smooth KKT point is due to `n = 2` or to `ℒ_uu = 0` (Remark 3.9).
- The cause of the one remaining 2-stage-window break on catmix (5.6), and
  of the break near the entry junction in the stage-wise recursion at
  N = 200 and 400.
- Felgenhauer's (2016) "semilinear" class. According to the second review,
  her 2005 paper (Control Cybernet. 34(3)) defines the semilinear class as
  `min k(x(1))` subject to `ẋ = f(t,x) + B(t)u`, with `B` independent of the
  state. If the 2016 paper uses the same class, then `w ≡ 0` there, so the
  `h²bᵀw` mechanism of Remark 3.5 does not arise. The formulations tested
  here lie outside that class (E2 with `ℓ_1 = k₁x₁ + k₂x₂`; catmix in `x`
  or `θ`), but equivalent formulations of both problems with `w ≡ 0` lie
  inside it (Remark 3.5, corrected in round 3). Still open: whether the
  2016 class is indeed this one (neither paper was accessible to me),
  whether her discretized optimality system is the KKT system of the Euler
  transcription of such a `w ≡ 0` formulation, and how those Euler
  transcriptions behave (not tested).
- A rigorous window certificate for COPS catmix along the lines of 5.6.
- Singular arcs of higher order (Fuller phenomena) and several controls
  beyond Corollary 1.2.

## 7. Status

| item | status |
|---|---|
| Proposition 1.1, Corollary 1.2 | proved; the Goh identity also checked symbolically |
| Proposition 1.3 (`bᵀMb = R = −∂_uσ̈`) | proved by hand; symbolic check with random polynomial data (`n = 2, 3`) |
| Remark 1.4 | `n = 1` proved; `n ≥ 2` sketch |
| Propositions 1.5, 1.6 | proved (local) |
| Proposition 2.1 | (a), (b) proved (local); (c) proved for `a_j < −γ/(2Δ)` (remainder terms completed in review round 1 and rechecked); the case `−γ/(2Δ) ≤ a_j ≤ 0` is open |
| Remark 2.2 | necessity proved (as in [E, Theorem 1]); layer asymptotics sketch; catmix `η_L = 1` exact |
| Lemma 3.1, Propositions 3.2–3.4 | proved under the stated assumptions (the `√h` tangency bound of 3.1(a) and Proposition 3.3 assume `K_t ⪯ hΛI`, and 3.3 bounded Hessians; 3.4 assumes `e_h = o(√h)`) |
| Remark 3.3a | isolated exact stage: exact rational example; fraction-of-stages bound: sketch |
| Remark 3.5 | the saddle computation is proved at leading order; gauge identity proved; relation to Felgenhauer (2016) from her abstract and, for the class definition, the second review's reading of her 2005 paper; `w ≡ 0` formulations of E2 and catmix inside that class: symbolic (round 3) |
| Proposition 3.6 | proved |
| Proposition 3.7 (`n = 1` converse) | proved; checked numerically (mpmath) |
| Remark 3.8 (`n ≥ 2`) | cites Megretski (2010, Theorem 1.4) |
| Remark 3.9 | the linear mode structure is proved for the stationary recursion (`n = 1`, `ℒ_uu ≠ 0`, `f(π) < 0 < f(0)`); two counterexamples to weaker statements checked numerically; the small-`h` form of `tr Φ/2` is heuristic, checked on catmix; its use for the finite catmix arc (oscillating KKT points, 12-stage breaks, eigenvalue counts) is heuristic, supported by float numerics |
| exact flow `f(π) = Kh³/12` | catmix numerics plus heuristic |
| E2 tangential certificates, `k₁ = −1/2`, N ≤ 1600; `k₁ = 0` (B2), N ≤ 800 | exact rational |
| E2 affine windows, losses, gauges `k₁ = 0` (B1), `+1/2` | exact failing-stage tests; float losses and local searches; KKT point with continuous structure for `k₁ = +1/2` exact |
| catmix singular data (5.2), `η_L` | exact, symbolic |
| catmix junctions, schemes, saddle, smooth reference, screening | float (mpmath 50 digits for 5.4 and for the 2-cycle); KKT point with the bang–singular–bang active set verified (float) at N = 100 only, N = 200 point approximate; chattering-gain and eigenvalue agreements are heuristic |

## 8. Commands run and files

All runs used `OMP_NUM_THREADS=1` from `theory-bangbang/singular/`, with
`timeout`. Only targeted checks were run: no project-wide verification and
no CI inspection.

1. `python3 kelley_identity.py` → `logs/kelley_identity.log` (symbolic
   identities).
2. `python3 lqsing_run.py -1/2 50 100 200 400 800 1600`, `… 0 50 100 200 400 800`,
   `… 1/2 50 100 200 400` → `logs/lqsing_k1_m1_2.jsonl`, `logs/lqsing_k1_0.jsonl`,
   `logs/lqsing_k1_p1_2.jsonl`. The N = 1600 exact run takes about 150 s.
3. `python3 lqsing_selftest.py k1 N` for `(−1/2, 100)`, `(0, 100)`,
   `(1/2, 60)` → `logs/lqsing_selftest.log`.
4. `python3 catmix_continuous.py` → `logs/catmix_continuous.log`.
5. `python3 catmix_schemes.py` → `logs/catmix_schemes.log`.
6. `python3 catmix_junctions.py` → `logs/catmix_junctions.log`.
7. `python3 catmix_trap.py 100 200 400` → `logs/catmix_trap_saddle.log`
   (converged at N = 100 only). A rerun with an active-set loop,
   `python3 catmix_trap.py 100 200` → `logs/catmix_trap_saddle_as.log`
   (N = 200: about 22 min; its result is only an approximate stationary
   point, Section 10, R1).
8. `python3 catmix_calib.py N chatter [1e-10 0.01]` for N = 100, 200, 400
   → `logs/catmix_calib.log` (full range), `logs/catmix_calib_band.log`
   (band 0.01). Only family A is reported: its second family resets `P` to
   0 at breaks and is superseded by `catmix_windows.py`.
9. `python3 catmix_windows.py N fixed 1 2 4` (N = 100, 200, 400) →
   `logs/catmix_windows.log`; `python3 catmix_windows.py N adaptive 2` →
   `logs/catmix_windows_adaptive.log`.
   - An N = 800 run was stopped at its time limit while still polishing the
     KKT point (finite-difference Hessian); it gave no result.
   - An earlier N = 800 screening without polishing (15–22 breaks for
     L = 1, 2, 4) used the stored controls, whose KKT accuracy is unknown;
     it is not reported.
   - (The fixed-window runs predate the `fixed|adaptive` argument; the
     current call is `catmix_windows.py N fixed L …`.)

Revision after review round 1 (same conditions):

10. `python3 revision_catmix.py A B` → `logs/revision_catmix_AB.log`
    (symbol `f(0)`, `f(π)`, `f''(π)`, exact `d₀`, predicted eigenvalue
    counts; stationary 2-cycle; about 1 min).
11. `python3 revision_catmix.py C` → `logs/revision_catmix_C.log` (smooth
    reference at N = 100, 200, 400 and Hessians at N = 100, 200; about
    3.5 min). A first run set the arc start one stage too late at N = 200
    (it ignored that the saddle point's first arc stage sits at the bound 0)
    and took the saddle Hessian over 4 bound stages; it was stopped and
    rerun after the fix. Only the rerun is reported.
12. `python3 revision_catmix.py D` → `logs/revision_catmix_D.log` (exact
    `η_L`); `python3 revision_catmix.py E` → `logs/revision_catmix_E.log`
    (Proposition 3.7 and the transfer matrix of Remark 3.9; about 2 min).
13. `python3 revision_e2.py` → `logs/revision_e2.log` (E2 values read back
    from the logs; `k₁ = +1/2` KKT point with the continuous structure and a
    new multistart; B2 `β_t` statistics; Remark 3.3a example; about 2 min).

Revision after review round 2 (same conditions, with
`PYTHONDONTWRITEBYTECODE=1`; no earlier log was overwritten):

14. `python3 revision2_catmix.py Z K` → `logs/revision2_catmix_ZK.log`
    (MINLPLib arithmetic; audit of the saved N = 100 and 200 points with an
    analytic second-order-adjoint Hessian (float), checked against central
    differences; envelope, deviations, finite-section estimates; about
    10 s).
15. `python3 revision2_catmix.py L` → `logs/revision2_catmix_L.log`
    (semismooth Newton / Levenberg–Marquardt attempt at N = 200, 400
    iterations, 24 s; end point saved as
    `logs/catmix200_r2_attempt_u.npy`, not a KKT point), and
    `python3 revision2_catmix.py L=4000` → `logs/revision2_catmix_L4000.log`
    (4000 iterations, 192 s; end point
    `logs/catmix200_r2_attempt4000_u.npy`, not a KKT point).
16. `python3 revision2_catmix.py M` → `logs/revision2_catmix_M.log`
    (Remark 3.9: the two toy examples, and `m₊`, `m₋`, `tr Φ/2` for the
    trapezoidal rule at N = 100, 200, 400 and the exact flow at N = 100,
    200; a few minutes, mostly the exact flow).
17. `python3 catmix_windows.py N fixed 1` for N = 100, 200, 400 →
    `logs/revision2_windows_L1.log` (full list of stage-wise break stages;
    same numbers of breaks as `logs/catmix_windows.log`).

Revision after review round 3 (same conditions, with
`PYTHONDONTWRITEBYTECODE=1`; no earlier log was overwritten):

18. `python3 revision3_semilinear.py` → `logs/revision3_semilinear.log`
    (sympy: E2 in the gauge `F = −k₁x₁²/2 − k₂x₁x₂`; catmix reachable set,
    sign of `b`, and the formulation in `ξ = ∫dθ/b` with a gauge; Kelley
    quantities from the Hamiltonian flow; about 1 s).
19. `python3 revision2_catmix.py K` → `logs/revision3_catmix_K.log` (Part K
    rerun after the script's output labels and docstrings were changed from
    "exact Hessian" to "analytic Hessian (second-order adjoint, float)";
    every number equals that of `logs/revision2_catmix_ZK.log`; about 10 s).

Scripts: `kelley_identity.py`, `lqsing.py`, `lqsing_run.py`,
`lqsing_selftest.py`, `catmix_continuous.py`, `catmix_schemes.py`,
`catmix_junctions.py`, `catmix_trap.py`, `catmix_calib.py`,
`catmix_windows.py`, `revision_catmix.py`, `revision_e2.py`,
`revision2_catmix.py`, `revision3_semilinear.py`. The catmix
scripts read the stored COPS controls
`open-instances-wave2/cops/logs/catmixN_u.npy` as data.

## 9. Revision after review (round 1)

The review is `reviews/singular-arcs-review.md`. I checked each finding
before changing the text. Commands are those of Section 8, items 10–13;
all are float or mpmath computations unless marked exact.

**F1 (moderate): the catmix "smooth" saddle point oscillates. Confirmed;
claim corrected.**

- *Check.* From the saved controls `logs/catmix{100,200}_smooth_u.npy`, the
  arc controls range over `[0.0548, 0.4106]` (N = 100) and
  `[0.0369, 0.4679]` (N = 200). The deviation from the neighbour average is
  up to 0.353 and 0.386. The alternating envelope changes sign every 11–12
  stages. All of this reproduces the review's numbers. (The ranges were
  already in `logs/catmix_trap_saddle.log` as `smooth_free_u`; the first
  version did not report them.) *Round-2 correction (Section 10, R1):* the
  N = 200 point is not a verified KKT point; 0.386 skipped its zero stages,
  and the whole-arc deviation is 0.468.
- *Changes.*
  - "Smooth" is replaced by "KKT point with the bang–singular–bang active
    set", with the oscillation described (Summary; Section 5.5).
  - The claim that the chattering gain matches the prediction
    quantitatively (`3.72e-8` against `3.95e-8`) is withdrawn.
  - A like-for-like reference was added: the best control that is smooth on
    the arc (Part C). Against it the gain agrees within 3% at N = 100, 200
    and 400. N = 400 was untested before.
  - The agreement is stated as heuristic, for two reasons. The junction
    boundary terms are of the same order in `h`, and the result depends on
    the reference: the ratio is 1.0–3.2 without free junction stages.
  - The explanation of the eigenvalue below the symbol minimum is changed
    from "junction transients" (never checked) to the oscillating base
    point. At the smooth reference, which has the same junctions, the most
    negative eigenvalue lies inside the symbol range: `−2.62e-8` against
    `f(π) = −2.73e-8` at N = 100, and `−3.37e-9` against `−3.41e-9` at
    N = 200.
  - The stationary 2-cycle computation (Part B) shows that the per-stage
    gain formula holds to a relative `1e-6` even at amplitude `ε = u_s`.
- *Also corrected.* At N = 200 the saddle point has 7 negative eigenvalues
  on its 113 interior stages. The first version reported 8, the count from
  the Hessian of the last Newton iterate. (Round 2: that point is only an
  approximate stationary point; Section 10, R1.)

**F2 (suggested addition): the symbol curvature explains the 12-stage
pattern. Confirmed; added and sharpened.**

- *Check* (Part A).
  - `f''(π) = 0.79058h³` at `h = 1/100`, `1/200` and `1/400`, as the review
    found.
  - The exact zero of `f` near `π` gives `d₀ = 0.26124`. The review's Taylor
    value is `0.2627`.
  - `π/d₀ = 12.03` stages, independent of `h`.
  - Predicted counts `m d₀/π`: 4.91 (`m` = 59), 9.40 or 9.81 (`m` = 113 or
    118) and 19.6 (`m` = 236).
- *Proofs added.*
  - Proposition 3.7: for `n = 1`, `f(ω)|e^{iω} − a|²` is affine in `cos ω`.
  - The transfer matrix of the linearized first-order recursion has
    `tr Φ/2 = cos ω₀` (proved by hand; checked to 12 digits in Part E).
  - So for `f(π) < 0` its solutions are exactly the alternating modes with
    envelope wavenumber `d₀`.
- *Changes.*
  - Remark 3.9 is new. It covers the conjugate-point spacing, the eigenvalue
    counts, and a heuristic mechanism for the oscillating KKT point.
  - In Section 5.6, the qualitative reading ("the band of admissible `P` is
    narrow") is replaced by the conjugate-point match: breaks 12 stages
    apart; 5, 10 and 20 breaks against 4.9, 9.8 and 19.6. (Round 2: the
    counts restate the spacing, and at N = 200 and 400 one break lies near
    the entry junction; Section 10, R5.)
  - Labelled heuristic where it is applied to the finite arc.

**F3 (minor): the remaining window break lies on the arc side. Confirmed;
interpretation withdrawn.**

- *Check.*
  - Break stages from `logs/catmix_windows.log`: 55 (N = 400), 31
    (N = 200) and 63 (N = 100).
  - First arc stages of the stored COPS points: 55, 28 and 14.
  - Stage `i` covers about `[t_i − h/2, t_i + h/2]`, because
    `y_i = Q(u_i)x_i ≈ x(t_i + h/2)`.
  - So the N = 400 window is the first two arc stages, starting 0.02 stage
    before `t₁`. At N = 200 it starts 3–4 stages into the arc. No window of
    bang stages breaks for `L = 1, 2`.
- *Change.* Section 5.6 and the Summary no longer read the break as the
  discrete trace of Proposition 2.1(c). The break is now called unexplained.

**F4 (minor): the Summary overstated Proposition 3.3. Confirmed;
corrected.**

- *Check.*
  - Exact rational example (`revision_e2.py` item 5, E2, `k₁ = +1/2`,
    N = 100). With `P_{t+1} = e₁e₁ᵀ` and the `O(1)` drop of the maximal
    recursion, a fractional stage passes the exact Lemma 10 test with
    `K_t` eigenvalues `0` and `2.31` (`h = 0.03`).
  - The previous stage then has `κ = −1.22` and must fail.
  - Family B2 in E2 uses the same mechanism at its last stage
    (`|β_t| = 0.34`).
- *Changes.*
  - The Summary table and the sentence after Proposition 3.3 now include
    the hypothesis `K_t ⪯ hΛI`.
  - Remark 3.3a is new: the example, plus a sketch that a fixed fraction of
    the stages still fails with bounded Hessians alone. That sketch gives no
    loss bound.

**F5 (minor slips). All confirmed and corrected.**

- (a) Section 4.2: the distances are `0.238, 0.148, 0.118, 0.081, 0.058,
  0.041` (log, `revision_e2.py` item 1). Also, the first fractional stage
  comes *before* `t₁`, so "lags" was the wrong word. The same holds for
  `k₁ = 0`, where the N = 100 values were also added.
- (b) The `k₁ = +1/2` fractional-stage counts of the first version's
  points are 1, 0, 1, 1 (log).
- (c) The KKT point with the continuous structure for `k₁ = +1/2` was
  solved exactly (item 2): `(J_smooth − J*)/h = +0.040, +0.020, +0.011,
  +0.005`. Section 4.3 now states that the `0.44h` prediction compares
  chattering with this point, and that comparing with `J*` needs
  `J_smooth − J* = o(h)`.
- (d) A new multistart (64 starts, another seed; item 3) found
  `J = −0.11340107` at N = 100. That is lower than the first version
  (`−0.11330285`) and the review (`−0.11339182`). Every start ended at a
  different local value. Section 4.3 now reports the best value found by
  any of the three procedures and keeps the caveat on global optimality.
- (e) The `k₁ = 0` window starts are 0.78, 0.78, 0.795, 0.7875, 0.7875
  (log): the range is now 0.78–0.795.
- (f) At N = 800, B1 fails one bang stage, `t = 1.1925` (log). This is now
  stated.
- (g) B2 at `k₁ = 0` (item 4): the median `|β_t|/h` is 0.948 and 0.945 at
  N = 200 and 800. The per-component medians per `√h` are 0.083/0.081 and
  0.041/0.041; those were the first version's "0.04–0.08". The text now
  gives the norm, `O(h)`.
- (h) `η_L = 1` exactly: by hand, and in sympy (Part D). Remark 2.2 and
  Section 5.3 are changed.
- (i) Remark 3.5: `b` and `ℓ_1` state-independent give `w ≡ 0` by the
  definition `w = −(∇ℓ_1 + b_xᵀψ)`. optcdeg2 has `w = 0` ([R]). The
  examples are now listed separately from the `bᵀw = 0`, `w ≠ 0` case
  (E2 with `k₁ = 0`).
- (j) ABDL, arXiv version, read again: `V` is defined in eq. (36); eq. (38)
  defines the bracket `[f_i, f_j]`. Corollary 1.2 now cites (36).
- (k) [C] (`open-instances-wave2/cops/report.md`) says its local solve from
  a smooth start gives `−0.04806939757`. Also,
  `−0.04806939757 − (−0.0480694320309596) = 3.45e-8`, while the gap to the
  listed `−0.04806939` is `4.2e-8`. Section 5.5 says this now. (Round 2:
  the full-precision listed value is `−0.04806939108`, and the gap is
  `4.10e-8`; Section 10, R7(c).)
- *Found while checking.*
  - The `k₁ = +1/2` B2 break times are 2.88, 2.88, 2.97 and 2.985, not
    "2.9–2.99".
  - The `k₁ = +1/2` minimum eigenvalues for all four `N` were added from
    the logs.

**F6 (literature). Done as far as access allowed.**

- *Felgenhauer (2016).*
  - Only the abstract was accessible (RePEc/IDEAS; Crossref confirms the
    bibliographic data). The publisher's page needs a login, and an open
    copy of a related 2013 paper sat behind a captcha.
  - So her hypotheses could not be checked. Remark 3.5 now explains why her
    result and the saddle statement are compatible under either reading of
    "semilinear": her result concerns solutions of the discretized
    optimality system, and in E2 such a KKT point exists but is a saddle.
  - The novelty item on `h²bᵀw` is qualified, and the question is listed in
    Section 6.
- *Discrete-time KYP.*
  - For `n = 1`, the only case the note uses, the converse is now proved
    directly (Proposition 3.7). The proof also shows that only `ω = 0` and
    `ω = π` matter.
  - For `n ≥ 2` the note cites Megretski (2010), Theorem 1.4. I read it: it
    is an explicit discrete-time non-strict KYP lemma under
    controllability.
  - Rantzer (1996) is no longer relied on.
- *Hamiltonian sufficiency.*
  - I read the short Poggiolini–Stefani paper (PoS CSTNA2005) in part. It
    proves strong local optimality of bang–singular extremals by building a
    field of non-intersecting extremals, assuming coercivity of the
    extended second variation on the singular arc and strict generalized
    Legendre–Clebsch.
  - The later papers (2008, 2011) and Schättler–Ledzewicz (2012) were
    identified by search but not read.
  - The novelty paragraph now says that the local sufficiency statements
    (Propositions 1.6, 2.1(b)) are close in content to these results.

**From the review's proof notes (Section 2.2; not in the F-list).**

- *Changes.*
  - In Proposition 2.1(c) the remainder is `O(s + |β|) = O(s)`, not
    `O(s + |η|)`.
  - The `|η| ≪ s` step now uses the test step `λ = √s`.
- *Check.* I checked the three steps by hand. The status row now says the
  proof is complete for `a_j < −γ/(2Δ)`.

## 10. Revision after review (round 2)

The second review is `reviews/singular-arcs-confirm-r1.md` (items R1–R7
and one refusal item). I checked each item before changing the text, with
my own code where a number was involved (Section 8, items 14–17). All
computations are float or mpmath unless marked exact.

**R1 (moderate): the N = 200 point is not a verified KKT point.
Confirmed; claims restricted to N = 100, and the N = 200 numbers qualified
or dropped.**

- *Check* (`revision2_catmix.py` Part K). The Hessian is now computed
  analytically by a second-order adjoint (analytic second partials of the
  stage maps, float arithmetic). It agrees with central differences of the
  analytic gradient to `1.1e-12` (N = 100) and `7e-13` (N = 200) with step
  `1e-5`, and to `1.1e-11` and `7e-12` with step `1e-6`. (Round 3: this
  sentence first called the Hessian "exact" and quoted only the N = 200
  values; Section 11, S2.)
  - N = 100: gradient `3.3e-17` on the 59 arc stages, none at a bound;
    smallest `|eigenvalue|` `4.5e-9`; Newton step `4.8e-10`. A KKT point to
    float accuracy.
  - N = 200: arc stages 28–145; stages 28, 118, 120, 129 and 138 are at
    `u = 0`, with gradients `1.5e-8`, `2.7e-9`, `−2.8e-11`, `−2.6e-10`,
    `−3.6e-10` (the last three have the wrong sign); interior gradient
    `3.3e-9`; smallest eigenvalue of the analytic Hessian `1.8e-12`
    (largest `1.7e-3`);
    Newton step `max|du| = 21`. All as the review found (its values: 38 or
    22 with finite-difference Hessians).
  - The review's "0.386 against 0.468": the first version's 0.386 treated
    the interior stages as one sequence, skipping the zero stages. Over the
    whole arc the largest deviation from the neighbour average is 0.468, at
    stage 119, between two zero stages.
- *Attempt to repair* (Part L, new). A semismooth Newton method with
  Levenberg–Marquardt damping on the Fischer–Burmeister form of the KKT
  conditions of the 118 arc stages, with the analytic Hessian, started from
  the saved point. In 400 iterations it lowered the interior gradient to
  `1.3e-10` and then stagnated: the smallest eigenvalue at its end point is
  `2.1e-10`, the Newton step is `0.22`, and stages 129 and 138 sit at
  `u ≈ 1e-4` with gradient `≈ −8e-11`. A rerun with 4000 iterations
  (192 s, `logs/revision2_catmix_L4000.log`) reduced the residual norm by
  only 9% more and ended in the same state (interior gradient `1.3e-10`,
  smallest `|eigenvalue|` `2.6e-10`, Newton step `0.28`). So no verified KKT point
  with this active set was found at N = 200. This negative result is kept
  in Section 5.5 and as an open item in Section 6.
- *Changes.*
  - Summary and Section 5.5: "a KKT point with the bang–singular–bang
    active set exists" now refers to N = 100 only. The N = 200 point is
    described as an approximate stationary point, with the numbers above.
  - Its range is given over the whole arc (`[0, 0.468]`), with the
    interior-stage range `[0.037, 0.468]` in brackets; the deviation is
    0.468.
  - The N = 200 entry of the column `J_ref − J_saddle` (`1.3e-10` to
    `4.4e-10`, below the first-order uncertainty of a point with gradient
    `3.3e-9`) is replaced by "not reported".
  - The eigenvalue offset is stated for N = 100 only (21% below `f(π)`, 26%
    below the finite-section estimate). The N = 200 offset (24%) and count
    (7) are kept only as indicative values, labelled as such.
  - The smooth reference at N = 200 takes only its bang-stage layout from
    this point (`u = 1` before stage 28, `u = 0` after stage 145, the same
    as in the stored COPS point), so the gain comparison is unaffected. The
    text now says so.

**R2 (minor): a wrong general sentence in Remark 3.9, and a Summary
condition that was not the one proved. Both confirmed and corrected.**

- *Check* (Part M; the transfer map `Φ` is built by solving the linear
  first-order equations, not from the half-trace formula).
  - `(a, c, Q, S, R) = (0.5, 1, 1, 0, 1)`: `min f = f(π) = 1.44 > 0`,
    `m₊ = 1.25 < m₋ = 3.25`, `tr Φ/2 = 2.25`, eigenvalues 4.27 and 0.23:
    real and positive, so "real and negative" is false in general.
  - `(a, c, Q, S, R) = (−0.5, 1, −2, −0.25, 1)`: `f(0) = −0.22`,
    `f(π) = −6`, `f''(π) = 26`, `tr Φ/2 = 2`, eigenvalues 3.73 and 0.27:
    `f(π) < 0 < f''(π)` does not give the oscillating modes.
  - Catmix exact flow: `m₊/h³ = 6.13, 6.23` and `m₋/h³ = 2.04, 2.08` at
    `h = 1/100, 1/200` (the review: 6.13 and 2.04 at `h = 1/100`), so
    `tr Φ/2 = −2.0001, −2.00003`.
- *Changes.*
  - Remark 3.9: the sentence now reads "the eigenvalues are real; negative
    if `m₊ > m₋`, positive if `m₋ > m₊`", with the first example. The
    second example is stated after the first bullet.
  - A small-`h` form `tr Φ/2 ≈ −(K + 4φ)/(K − 4φ)` (`f(π) = φh³`) is
    added, labelled heuristic. It rests on `m₊ ≈ Kh³`, argued from Goh's
    form, and is checked on catmix: `m₊/h³ = 6.13, 6.23, 6.27` for the
    trapezoidal rule against `K = 6.32`, and the formula reproduces the
    trapezoidal `tr Φ/2 = −0.966071` to `3e-7` and the exact-flow limit
    `−2`.
  - Summary: the bullet now states the proved condition, `f(π) < 0 < f(0)`
    with `n = 1` and `ℒ_uu ≠ 0`, and says that `f(π) < 0 < f''(π)` is not
    enough.

**R3 (minor): the envelope spacing was stated as a match. Confirmed;
corrected.**

- *Check* (Part K, envelope `(−1)^i(u_i − (u_{i−1} + u_{i+1})/2)`). N = 100:
  sign changes at stages 18, 29, 40, 51, 62, exactly 11 apart. N = 200
  (approximate point): 31, 43, 54, 66, 78, 89, 101, 112 (mean spacing 11.6),
  then irregular. The first version's "arc stages 2, 13, 24, 35, 46" used an
  unstated offset; the stages are now absolute stage numbers.
- *Change.* Section 5.5 and the Summary now say "every 11 stages, close to
  (9% shorter than) `π/d₀ = 12.03`", and that exact agreement is not
  expected because the base point is far from the stationary point. The
  12-stage spacing of the recursion breaks, which does match, is stated
  separately (R5).

**R4 (minor): the `K_t ⪯ hΛI` hypothesis was missing in two places.
Confirmed; added.**

- *Check.* Lemma 3.1(a) gives `|β_t|² ≤ hΛκ_t` only under `K_t ⪯ hΛI`
  (its proof uses the test vector `d = −(s/Λ)β_t`). In the Remark 3.3a
  example, `K_t = β_tβ_tᵀ/κ_t` has eigenvalue `2.31` at `h = 0.03`, so
  `K_t ⪯ hΛI` would need `Λ ≥ 77`; with `Λ = O(1)` the example violates the
  unqualified "tangential to within `√h`". Expanding `∇²_xρ_t` gives
  `K_t = F_xᵀP_{t+1}F_x − P_t + O(h) = P_{t+1} − P_t + O(h)` for bounded
  Hessians and costates, so `K_t ⪯ hΛI` is the one-sided condition
  `P_{t+1} − P_t ⪯ O(h)`; "Hessians that change by `O(h)` per stage" is
  sufficient, not equivalent.
- *Changes.* The hypothesis is added to the Summary's "Discrete time"
  paragraph and to the sentence after Lemma 3.1. The gloss in the Summary
  table and after Proposition 3.3 now names the one-sided condition and
  gives `O(h)` changes as one example. The Section 7 row says which
  statements assume `K_t ⪯ hΛI`.

**R5 (minor): selective or double-counted count comparisons. Confirmed;
corrected.**

- *Check.*
  - Full break lists of the stage-wise recursion (item 17, same break
    numbers as before): N = 100: 17, 29, 41, 53, 65; N = 200: 30, then 39,
    51, …, 135; N = 400: 55, then 64, 76, …, 280. After the first break
    (N = 200, 400) the spacing is exactly 12. The first break lies 2 stages
    into the arc (N = 200) or at the first arc stage (N = 400), at or next
    to the unexplained 2-stage-window break (stages 31–32 and 55–56). The
    periodic breaks number 5, 9 and 19.
  - Negative eigenvalues at the oscillating points: 5 at N = 100 (against
    `m d₀/π = 4.9`) and 7 at the approximate N = 200 point (against 9.4).
- *Changes.* The Summary, Remark 3.9 ("Counts"), and Sections 5.5 and 5.6
  now state the break-count agreement once, as the same observation as the
  12-stage spacing, and name the junction-side break. Both the reference
  counts (4, 10) and the oscillating-point counts (5, 7) are given, the
  latter N = 200 value as indicative only (R1).

**R6 (minor): the explanation of E2's smooth KKT point was untested.
Confirmed; reworded.**

- *Check.* Remark 3.9 assumes `n = 1` and `ℒ_uu ≠ 0`. E2 uses Euler, whose
  stage map and cost are affine in `u`, so `ℒ_uu = 0`, and it has `n = 2`.
  No computation separated the two effects.
- *Change.* Remark 3.9 now names both differences, says "may" for the
  hyperbolic-mode explanation, and states that which difference matters was
  not checked. Section 6 lists this as open. (Not done: a test, for example
  an `ℒ_uu = 0` scheme for catmix, or an `ℒ_uu ≠ 0` scheme for E2. It
  would be a new computation beyond this revision.)

**R7 (trivial). All three corrected.**

- (a) The Summary table row "bang side of a junction" had unescaped pipes
  in the code span `Δ|w|²/(2μ)`, which split the cell in GitHub-flavoured
  Markdown. They are now escaped (`\|`). A script check of every table row
  in this note (cells split at unescaped pipes) finds no other row whose
  cell count differs from its header.
- (b) "`π/d₀ = 12.03` for every `h`" now reads "at `h = 1/100`, `1/200`
  and `1/400` (the same to five digits)". Section 5.6's "which does not
  depend on `h`" is replaced in the same way. The small-`h` form of R2
  suggests that `π/d₀` has a limit as `h → 0`; this is labelled heuristic.
- (c) `treewidth-census/instancedata.csv` lists `primalbound` `−0.04806939108`
  for catmix100. The chattering point (`−0.0480694320309772`) lies
  `4.10e-8` below it (Part Z), and [C]'s local solve `−0.04806939757` lies
  `6.5e-9` below it, so [C]'s phrase "reproduces the MINLPLib value
  −0.04806939757" is inaccurate. Section 5.5 now quotes the full listed
  value. [C] itself is not changed here.

**Refusal item (Felgenhauer 2016 hypotheses): narrowed as far as access
allowed.**

- *Check.*
  - The open PDF of Felgenhauer (2005) that the review read
    (matwbn.icm.edu.pl) returned a bot-check page to me, and I did not try
    to get around it. The bibliographic record (geodesic.mathdoc.fr) and
    the author's publication list (b-tu.de) do not state the class. So the
    class definition rests on the review's reading: `min k(x(1))` subject
    to `ẋ = f(t,x) + B(t)u`, with `B` independent of the state.
  - The 2016 abstract (IDEAS) says "for the so-called semilinear case" and
    does not define it; the keywords include "Euler method".
  - Osmolovskii–Veliov (2020), which cites the 2016 paper, was read in its
    introduction and the start of its Section 5: it treats Euler
    discretization of control-affine problems with state-dependent
    `B(t,x)` under a strong metric subregularity condition, analysed in
    detail for bang–bang controls. In the parts read I found neither a
    definition of Felgenhauer's class nor a sign criterion like `bᵀw` or
    `f(π)`.
  - Under the review's reading, `w = −(∇ℓ_1 + b_xᵀψ) ≡ 0` in that class
    (Mayer cost, `b_x = 0`). E2 in Mayer form has input column
    `(b, ℓ_1(x))` with `ℓ_1 = k₁x₁ + k₂x₂`; the `k₁` part is a null
    Lagrangian, the `k₂ = 1/4` part is not, so E2 is outside the class.
    Catmix has `b(θ) = 1 − 10θ − θ²`, also outside.
    *Round-3 correction (Section 11, S1):* this is true for the
    formulations used here, but not for the problems, and the reason given
    for E2 is wrong. `k₂x₂u + k₂x₁(x₁ − x₂) = d(k₂x₁x₂)/dt` is a null
    Lagrangian, so the gauge `F = −k₁x₁²/2 − k₂x₁x₂` removes `ℓ_1` from E2.
    For catmix, the change of state `ξ = ∫dθ/b` (with `b ≥ 10/121` on the
    reachable set `θ ∈ [0, 1/11]`) followed by a gauge does the same. Both
    give `w ≡ 0` formulations inside the class.
- *Changes.* Remark 3.5 has a new bullet with this reading and its caveat
  (the 2016 definition was not seen). The Section 6 item is narrowed to
  that caveat and to whether her discretized optimality system is the
  Euler KKT system. The novelty paragraph and Sources are updated.

## 11. Revision after review (round 3)

The third review is `reviews/singular-arcs-confirm-r2.md` (items S1 and
S2). I checked both items with my own computations before changing the
text (Section 8, items 18 and 19). No new literature was read for this
round.

**S1 (minor): E2 and catmix are not outside Felgenhauer's semilinear class
"in every gauge". Confirmed; the claim is withdrawn and corrected.**

- *Check* (`revision3_semilinear.py`, sympy, exact;
  `logs/revision3_semilinear.log`).
  - E2. With `F = −k₁x₁²/2 − k₂x₁x₂`,
    `dF/dt = −(k₁x₁ + k₂x₂)u − k₂x₁(x₁ − x₂)`. Adding it to the integrand
    gives `ℓ_1 = 0` and `ℓ_0 = (x₁² + x₂²)/2 − k₂x₁(x₁ − x₂)`. The terminal
    cost becomes `½(k₂x₁² + 2k₂x₁x₂ + (1 − 2k₂)x₂²)`, which does not contain
    `k₁`, plus the constant `F(x₀) = −k₁/2`; this matches
    `J(k₁) = J(0) − k₁/2` (Section 4.1). Since `b = e₁` is constant,
    `w = −∇ℓ_1 = 0`, and adding a cost state gives `ẋ = f(x) + Bu` with
    constant `B` and a Mayer cost, which is the class as read. The Kelley
    quantity `−∂_uσ̈`, computed from the Hamiltonian flow in both
    formulations, is `1 − 2k₂` in each.
  - Where the round-2 argument went wrong: `k₂x₂u` is not a null
    Lagrangian by itself, but `k₂x₂u + k₂x₁(x₁ − x₂)` is, and a gauge may
    move the remainder into `ℓ_0`. I had adopted the round-1 confirmation
    review's wording without checking it.
  - Catmix. `θ(0) = 0`, `θ̇ = u ≥ 0` at `θ = 0` and
    `θ̇ = 10(u − 1)/121 ≤ 0` at `θ = 1/11`, so `θ ∈ [0, 1/11]` for every
    admissible control. There `b` is decreasing (`b' = −10 − 2θ`), so
    `b ≥ b(1/11) = 10/121 > 0`; the positive root of `b` is
    `√26 − 5 = 0.0990 > 1/11`. With `ξ = ∫₀^θ dθ'/b`, `ξ̇ = a/b + u`, and
    the gauge `dF/dξ = −θ` removes `ℓ_1` and gives
    `ℓ_0 = θ(11θ − 1)/b(θ)`. In this formulation the singular point
    equation is again `111θ² − 22θ + 1 = 0`, and `K = 2√10` at `θ_s`, as in
    Section 5.2. The script also recomputes `K = 2√10` in the `θ`
    formulation.
  - So "outside the class" holds for the formulations used here (E2 with
    `ℓ_1 = k₁x₁ + k₂x₂`, `k₂ = 1/4`; catmix in `x` or `θ`) and fails for the
    problems.
- *Changes.*
  - Remark 3.5, last bullet: the "every gauge" sentence is replaced by the
    two statements above (formulations used here outside; equivalent
    `w ≡ 0` formulations inside), with the E2 gauge and the catmix change
    of variable, and the note that the Euler transcriptions of the `w ≡ 0`
    formulations were not tested. I also added that Felgenhauer's other
    hypotheses were not checked; for example, E2's optimal control is
    bang–singular, not bang–singular–bang.
  - Section 6: the Felgenhauer item says the same and adds, as open
    questions, the KKT system of such a `w ≡ 0` formulation and the
    behaviour of its Euler transcription.
  - Summary (novelty list): one sentence added.
  - Section 10, refusal item: the round-2 sentence is kept as the record,
    followed by a correction note.
  - Section 7: the Remark 3.5 row mentions the symbolic check.
- *Effect.* The compatibility argument of Remark 3.5 is unchanged: under
  the review's reading of the class, Felgenhauer's Euler result would
  concern `w ≡ 0` formulations, where the `h²bᵀw` term vanishes. Not done:
  an Euler run of these formulations. It would be a new computation, beyond
  this revision.

**S2 (trivial): "exact" was used for a float Hessian, and the
finite-difference agreement was quoted for one `N` only. Confirmed;
corrected.**

- *Check.*
  - The header reserves "exact" for rational arithmetic. The Part K Hessian
    is analytic (a second-order adjoint), but it is evaluated in floats.
  - `logs/revision2_catmix_ZK.log` gives `max|H_fd − H|` = `1.1e-12`
    (N = 100) and `7.0e-13` (N = 200) at step `1e-5`, and `1.1e-11` and
    `6.7e-12` at step `1e-6`. Section 10 quoted only the N = 200 values.
  - A rerun of Part K (`logs/revision3_catmix_K.log`) reproduces every
    number of the old log.
  - At N = 200 the central-difference Hessians give smallest `|eigenvalue|`
    `1.0e-12` and `1.7e-12`, against `1.8e-12` for the analytic one, so only
    the order of that eigenvalue is meaningful. No conclusion depends on
    more.
- *Changes.*
  - "Exact Hessian" is now "analytic Hessian (second-order adjoint,
    float)" in Section 5.5 (three places), Section 8 (item 14) and
    Section 10, R1 (three places). Section 10, R1 now gives the
    finite-difference agreement at both `N`, with a correction note.
  - Section 5.5 now notes that the N = 200 eigenvalue `1.8e-12` is
    meaningful only in order.
  - In `revision2_catmix.py`, the docstrings and the printed labels now say
    "analytic". The function name `exact_grad_hess` is kept, because the
    review's check script `d2_fb_residual.py` imports it. The old log
    `logs/revision2_catmix_ZK.log` still carries the label "exact Hessian".

## Sources

The bibliographic details of the entries below were checked by web search
on 2026-09-30. Texts read (arXiv or open PDFs, extracted with
`pdftotext`):

- the Goh-transformation section of Aronna et al. (2012);
- Section 1.1 of Megretski (2010);
- parts of Poggiolini–Stefani (2005);
- the introduction and the start of Section 5 of Osmolovskii–Veliov (2020)
  (added in round 2).

Only the abstracts of Felgenhauer (2012, 2016) and of Poggiolini–Stefani
(2008) were read. The other papers were not read for this note; statements
attributed to them are the standard ones.

- H. J. Kelley, *A second variation test for singular extremals*, AIAA
  Journal 2 (1964) 1380–1382.
- B. S. Goh, *Necessary conditions for singular extremals involving
  multiple control variables*, J. SIAM Control 4 (1966) 716–731.
- H. M. Robbins, *A generalized Legendre–Clebsch condition for the singular
  cases of optimal control*, IBM J. Res. Dev. 11 (1967) 361–372 (from
  memory; not checked).
- J. P. McDanell, W. F. Powers, *Necessary conditions for joining optimal
  singular and nonsingular subarcs*, SIAM J. Control 9(2) (1971); a NASA
  NTRS copy exists (19710001931).
- D. H. Jacobson, J. L. Speyer, *Necessary and sufficient conditions for
  optimality for singular control problems: a limit approach*, Harvard
  Division of Engineering and Applied Physics Technical Report 604 (March
  1970, NTRS 19700016063). A journal version appeared in J. Math. Anal.
  Appl. (1971); details not checked.
- M. S. Aronna, J. F. Bonnans, A. V. Dmitruk, P. A. Lotito, *Quadratic order
  conditions for bang-singular extremals*, Numerical Algebra, Control and
  Optimization 2(3) (2012) 511–546, DOI 10.3934/naco.2012.2.511,
  [arXiv:1107.0161](https://arxiv.org/abs/1107.0161). Their Section 4
  (Goh transformation, eqs. (35)–(41), Theorem 4.4) was read; the
  identification of `R` and `V` above is from there. In the arXiv version,
  `V` is defined in eq. (36), `R` in eq. (39), `B₁` in eq. (30); eq. (38)
  defines the bracket `[f_i, f_j]`.
- A. Megretski, *KYP lemma for non-strict inequalities and the associated
  minimax theorem*, [arXiv:1008.2552](https://arxiv.org/abs/1008.2552)
  (2010). Section 1.1 (discrete time, Theorems 1.1–1.4) was read;
  Theorem 1.4 is the non-strict discrete-time KYP lemma used in Remark 3.8.
- A. Rantzer, *On the Kalman–Yakubovich–Popov lemma*, Systems & Control
  Letters 28(1) (1996) 7–10. Cited in the first version for the discrete
  KYP lemma; not accessed, and no longer relied on.
- U. Felgenhauer, *Discretization of semilinear bang-singular-bang control
  problems*, Computational Optimization and Applications 64(1) (2016)
  295–326, DOI 10.1007/s10589-015-9800-2. Abstract only (RePEc/IDEAS;
  bibliographic data confirmed with Crossref). The abstract says that the
  paper analyzes a discretization of the first-order optimality system,
  written as a variational inequality, under second-order conditions. For
  the "semilinear" case it proves that the discrete control keeps the
  bang–singular–bang structure, with first-order `L¹` convergence (Euler
  method, by the keywords).
- U. Felgenhauer, *Structural stability investigation of bang-singular-bang
  optimal controls*, J. Optim. Theory Appl. 152(3) (2012) 605–631. Abstract
  only.
- U. Felgenhauer, *Optimality properties of controls with bang-bang
  components in problems with semilinear state equation*, Control and
  Cybernetics 34(3) (2005) 763–785 (bibliographic record:
  geodesic.mathdoc.fr, item CC_2005_34_3_a7). Not read by me: the open PDF
  (matwbn.icm.edu.pl/ksiazki/cc/cc34/cc3438.pdf) returned a bot-check page.
  The class definition used in Remark 3.5 is the second review's reading of
  its Section 2.
- N. P. Osmolovskii, V. M. Veliov, *Metric sub-regularity in optimal
  control of affine problems with free end state*, ESAIM: COCV 26 (2020),
  DOI 10.1051/cocv/2019046 (open PDF via numdam.org). Introduction and the
  start of Section 5 read: Euler error estimates for control-affine
  problems `ẋ = a(t,x) + B(t,x)u` under strong metric subregularity,
  analysed in detail for bang–bang controls. It cites Felgenhauer (2016)
  and W. Alt, U. Felgenhauer, M. Seydenschwanz, *Euler discretization for a
  class of nonlinear optimal control problems with control appearing
  linearly*, Comput. Optim. Appl. 69 (2018) 825–856 (bibliographic entry
  only; not read).
- L. Poggiolini, G. Stefani, *On second order sufficient optimality
  conditions for a bang-singular arc*, Proceedings of Science
  PoS(CSTNA2005)017 (2005). Introduction and outline read. The approach is
  Hamiltonian: a field of non-intersecting extremals from a Lagrangian
  submanifold. The assumptions include coercivity of the extended second
  variation on the singular arc and strict generalized Legendre–Clebsch.
- L. Poggiolini, G. Stefani, *Sufficient optimality conditions for a
  bang–singular extremal in the minimum time problem*, Control and
  Cybernetics 37 (2008) 469–490 (abstract); *Bang-singular-bang extremals:
  sufficient optimality conditions*, J. Dyn. Control Syst. 17 (2011)
  469–514 (bibliographic record from search only).
- H. Schättler, U. Ledzewicz, *Geometric Optimal Control: Theory, Methods
  and Examples*, Springer (2012). Not read; cited, as the review suggested,
  for field-of-extremals constructions around singular arcs.
- D. J. Bell, D. H. Jacobson, *Singular Optimal Control Problems*,
  Academic Press (1975) (from memory; not checked).
- Numerical oscillations on singular arcs in direct methods (search
  snippets only; not read):
  - [arXiv:2010.06744](https://arxiv.org/abs/2010.06744) (Atkins et al.,
    PASA; discretization artifacts that resemble chattering);
  - [arXiv:1507.00172](https://arxiv.org/abs/1507.00172) (oscillations on
    singular arcs that vanish as `h → 0`);
  - [arXiv:2503.09123](https://arxiv.org/abs/2503.09123) (fluctuations of
    direct-collocation solutions along singular arcs);
  - AIChE Annual Meeting 2009 and 2013 abstracts on the regularization of
    singular problems, the latter using catalyst mixing as a test case.

  None of these snippets states a sign criterion like `bᵀw` or `f(π)`.
  The closest work found is Felgenhauer (2016), read in abstract only
  (Remark 3.5). Whether such a criterion exists elsewhere in the
  literature on Euler or collocation discretizations of singular problems
  was checked only in part: the parts of Osmolovskii–Veliov (2020) that I
  read contain none; Alt–Felgenhauer–Seydenschwanz (2018) and work by
  Biegler's group were not checked.
