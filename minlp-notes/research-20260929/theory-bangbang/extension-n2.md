# Tangential quadratic calibrations for state dimension n ≥ 2: the layer condition, a counterexample, and an exact certificate

Date: 2026-09-30. Status: **revised after review and confirmed** ([Rev],
verdict "fixes needed"; a confirmation of the revision,
`reviews/ext-bangbang-n2-confirm.md`, checked the fixes and raised ten minor
items, which the root applied on 2026-09-30, Section 11.1, not
rechecked). Proofs are
complete unless they are labelled "sketch" or "leading order". Numbers are
floating-point screening unless they are marked "exact" (rational arithmetic).
The changes are listed in Section 11.

Cited notes:

- **[R]** `theory-bangbang/report.md`: Remark 3.3, Propositions 3.1–3.2,
  Theorems 2.3 and 4.1;
- **[S]** `theory-calibration/scouting.md`;
- **[Rv]** `reviews/calibration-review.md`;
- **[V]** `reviews/bangbang-verification/verification-report.md`. It finished
  while this work was running and is treated as provisional.
- **[Rev]** `reviews/bangbang-n2-review.md`, the independent review of this
  note.

Scripts and logs are in `theory-bangbang/n2/` and `theory-bangbang/n2/logs/`.

## Summary

**Question** ([R, Remark 3.3]). For state dimension `n ≥ 2`, does a
tangential strict quadratic calibration exist if and only if the maximal
backward solution `P̂` of the singular Riccati inequality is bounded, "i.e. no
conjugate point"?

**Answer.** The conjecture mixes two conditions, and they differ.

1. **The obstruction lives in a thin layer just after the switch and is
   decided by one number.** Let `Q` solve the Lyapunov equation of the last
   arc with `Q(T) = Φ_xx`, and put `β_L = Q(τ+)b − w`, `η_L = bᵀβ_L`. For any
   `n`, one regular switch, fixed `x_0` and a free endpoint:
   - if `η_L > 0`, strict tangential quadratic calibrations with linear-rate
     tangency exist in the local formulation, by an explicit construction
     (Theorem 2);
   - if `η_L < 0`, **no** exact calibration exists that is `C³` in `(t,x)`,
     with bounded derivatives up to order 3, on a uniform tube after the
     switch, strict or not (Theorem 1). Such a calibration is automatically
     tangential at `τ+` ([R, Proposition 3.1] applied to the right limit), so
     Theorem 1 is that proposition plus Lyapunov comparison;
   - if `η_L = 0`, no strict one exists.

   In the "local" formulation, where the singular condition is imposed only
   near `τ`, this is exactly the statement "`P̂` is bounded". So the
   conjecture holds in that sense, now with an explicit criterion
   (Corollary 3). This answers the continuous existence question only; see
   item 4.
2. **"`P̂` bounded" is not "no conjugate point".** Here the classical
   second-order sufficient condition (SSC) is `F''(τ) = D + Δ²η_L > 0`
   (Proposition 6). It agrees with the Osmolovskii–Maurer (O–M) quadratic
   form, where `D = |σ̇(τ)|Δ` is their `D(H)`.
   - The maximal tangential calibration is O–M's Riccati test with rank-one
     jump **in which `D(H)` is set to zero** (Propositions 4 and 6).
   - For `−D/Δ² < η_L < 0`, the trajectory satisfies the SSC, so it is a
     strict strong local minimum by the cited theorems, but it admits no exact
     calibration that is `C³` in `(t,x)` on a uniform tube after the switch.
   - **Example B** (`n = 2`) is an explicit instance: `η_L = −0.429`,
     `D = 3.066`, `F''(τ) = 1.350`. Theorem 1 does not use `n ≥ 2`, so the
     scalar sketch in [R] has the same gap.

   `D` affects only the thickness `≈ exp(−2D/(Δ²|η_L|))` of the layer in which
   the maximal solution blows up.
3. **Formulation issues.**
   - In the "global-model" version (the form of [R, Proposition 3.2], with the
     singular term on the whole horizon), extra conjugate points of a relaxed
     LQ problem can appear on both arcs. [V] noted the one before `τ`;
     Example C shows one.
   - When `b` or `ℓ_1` is nonlinear, two matrix inequalities must hold at
     once, and a maximal solution need not exist, because the Loewner order is
     not a lattice. The local formulation avoids both problems, but only for
     the continuous existence question.
4. **The local result does not feed into the transfer theorem.**
   - [R, Theorem 4.1] needs hypothesis (H3). For quadratic `S`, and for every
     `S` when `N = 0`, (H3) implies the global-model inequality (G) with
     `ε = 0` at every `t ≠ τ` (Lemma 14).
   - In example C, `η_L = +0.202`, so local calibrations exist. But **no**
     `S` satisfies (H3) with an exact terminal term, and no bounded
     global-model calibration exists. Every global-model calibration lies
     below the solution started from the largest admissible value at the
     switch, and that solution tends to `−∞` before `τ`, at `t = 0.352` for
     `ε = 0` (Proposition 15; the blow-up is float numerics).
   - Theorem 2's local calibrations also violate the far-region condition (F)
     of Section 7 and the (H3) margin, in examples A and C. So
     Proposition 12 does not apply to them either.
   - A transfer theorem for local calibrations is open (Section 8).

**Numerical tests** (Section 6):

- **Example A** (`n = 2`, `w = (0.3, 0.3) ≠ 0`):
  - the Euler transcription is **nonconvex in `u`**: at `N = 200` the reduced
    Hessian has 7 negative eigenvalues;
  - the four tangential families have **0 failing stages** at
    `N = 500 … 16000`;
  - the non-tangential Lyapunov family fails on a **fixed duration 0.868**
    (217 → 6943 stages). This is mainly a failure away from the switch: the
    failing stages are where its continuous residual has a negative minimum
    over the reachable box, `t ∈ [τ − 0.183, T]`. It is not a clean instance
    of the switch effect of [R, Theorem 2.3(2)];
  - **exact rational certificates without windows** at
    `N = 50, 200, 500, 1000, 2000, 5000` give gaps `J − B ≤ 3.0e-25`, with
    every stage checked over the full reachable box. A negative control
    (Lyapunov family) gives gap 3.96.
- **Example B**:
  - the continuous maximal solution blows up `5.754e-3` time units after the
    switch;
  - the discrete maximal recursion breaks within one stage of 0.00575 after
    the switch for `N = 1000 … 16000` (3 → 46 stages). So any quadratic
    family that is exact over `R² × U` after its window needs a window of
    fixed duration.
- With `w ≠ 0` the discrete KKT point can have **two adjacent fractional
  stages** (observed for `N = 50, 200, 500, 1000, 5000` in example A0).

**Far-region condition (H5)** (Section 7):

- it is not implied by local conditions;
- **proved**: far-region strictness of the continuous calibration on `D × U`
  implies (H5) for all small `h` (Proposition 12; proof revised after review
  so that `S_t` need only be piecewise continuous in `t`). Tangency with a
  linear rate also keeps the transfer correction smooth across the switch;
- for LQ-structured data (affine drift, constant `b`, quadratic `ℓ_0` and `Φ`,
  affine `ℓ_1`) and **global-model (G-global) calibrations**, the far region
  is automatic (Proposition 13);
- it is not automatic for local calibrations: Theorem 2's calibrations
  violate (F) in examples A and C (Section 7).

In example A the certificate checks the whole reachable box, so (H5) is
verified there, not assumed. The certificate uses the discrete maximal
recursion, which is a global-model-type family, not Theorem 2's local
construction.

## 0. Setting and notation

- **Continuous problem.** `ẋ = g(x,u) = a(x) + b(x)u` with scalar
  `u ∈ U = [u_−, u_+]` and `Δ = u_+ − u_−`. Cost
  `J = ∫_0^T ℓ_0(x) + ℓ_1(x)u dt + Φ(x(T))`. The initial state `x(0) = x_0` is
  fixed, `T` is fixed and the endpoint is free. The data are `C³`.
- **Hamiltonian and costate.** `H = ℓ_0 + ℓ_1u + ψᵀg` (minimum principle) and
  costate `ψ`. The switching function is `σ(t) = ℓ_1 + bᵀψ` along `x*`, and
  `w_t = −∇_xσ_0(t, x*(t))` as in [R, Section 0].
- **Standing assumptions.**
  - `(x*, u*)` is admissible and bang-bang with **one regular switch** at `τ`,
    from `u_a` on `[0,τ)` to `u_b` on `(τ,T]`;
  - `σ(t)(u − u*(t)) ≥ 0` (minimum principle);
  - `|σ(t)| ≥ γ_1|t − τ|` with `γ := |σ̇(τ)| > 0`;
  - `b(x*(τ)) ≠ 0`;
  - `x*` is interior to the state domain.
- **Abbreviations.** `D := γΔ` (O–M's `D(H)`); `κ := Δ/(2γ) = Δ²/(2D)`. On a
  given arc, `u°` is the vertex that is not `u*(t)`, and `ω = u − u*(t)`.
- **Quadratic calibrations** ([R, Proposition 3.2]).
  `S = V*(t) + ψ(t)ᵀd + ½dᵀP(t)d` with `d = x − x*(t)`. `P` is bounded and
  `C¹` on each arc; upward jumps are allowed (see (J)). Put
  `β(t) = P(t)b − w_t` and
  `M(t,u) = Ṗ + g_x(u)ᵀP + Pg_x(u) + H_xx(u)`, which is affine in `u`.
- **N = 0.** The case where `b` is constant and `ℓ_1` is affine. Then `M`
  does not depend on `u`.
- **Last-arc Lyapunov solutions.** On `(τ,T]` let `A = g_x(x*, u_b)` and let
  `Q_ε` solve `Q̇ + AᵀQ + QA + H_xx(u_b) = 2εI` with
  `Q_ε(T) = Φ_xx(x*(T)) − 2εI`. Put `Q := Q_0`. Then `Q_ε = Q − εR` with
  `R(t) = 2Ψ(T,t)ᵀΨ(T,t) + 2∫_t^T Ψ(s,t)ᵀΨ(s,t)ds ≻ 0`, where `Ψ` is the
  transition matrix of `ξ̇ = Aξ`.
- **Layer data.** `β_ε := Q_ε(τ+)b − w_τ` and `η_ε := bᵀβ_ε`, with `b`, `w`
  taken at `(x*(τ), ψ(τ))`. **`η_L := η_0`** and `β_L := β_0`.

## 1. Which singular Riccati inequality

**1.1 Expansion.** `r = ℓ_0 + ℓ_1u + S_t + S_xᵀg` is affine in `u`, and

```
r(t, x*+d, u*+ω) = σω + ω βᵀd + ½ dᵀ M(t, u*+ω) d + R₃,   |R₃| ≤ C(1+|ω|)|d|³.
```

This refines [R, Proposition 3.2]: the Hessian is evaluated at the actual
control `u`.

**Lemma 1.1 (vertex reduction).** Fix `t ≠ τ` and `ε ≥ 0`. The quadratic part
satisfies `σω + ωβᵀd + ½dᵀM(t,u)d ≥ ε|d|²` for all `d ∈ Rⁿ` and all `u ∈ U` if
and only if

- **(A)** `M(t, u*(t)) ⪰ 2εI`, and
- **(G)** `M(t, u°) − 2εI − (Δ/(2|σ(t)|)) ββᵀ ⪰ 0`.

*Proof.* Write `u = u* + λω°` with `λ ∈ [0,1]` and `|ω°| = Δ`. The quadratic
part equals `(1−λ)·½dᵀM(t,u*)d + λ·[|σ|Δ + ω°βᵀd + ½dᵀM(t,u°)d]`, because `M`
is affine in `u`. So it is at least `ε|d|²` for all `λ` iff it is at both
vertices. At `u°`, the condition
`|σ|Δ + ω°βᵀd + ½dᵀ(M° − 2ε)d ≥ 0 ∀d` is the Schur-complement condition
`[M° − 2ε, ω°β; ω°βᵀ, 2|σ|Δ] ⪰ 0`, which is (G). □

[R, Proposition 3.2] requires (G) for **all** `u`, including `u*`. That is
sufficient but stronger than needed: the `ββᵀ` term is not needed at `u*`.

**Definition 1.2 (TSQC).** Given `ε > 0`, `P` is a *tangential strict
quadratic calibration* (TSQC) if:

- **(T)** `P(T) ⪯ Φ_xx(x*(T)) − 2εI`;
- **(A)** holds for all `t ≠ τ`;
- one of:
  - **(G-global)** (G) holds for all `t ≠ τ` (the "global model", as in [R]);
  - **(G-local)** (G) holds for `0 < |t − τ| ≤ δ_0`, for some `δ_0 > 0`;
- **(J)** at any jump, `P(t+) ⪰ P(t−)`;
- **(Tan)** `|β(t)| ≤ L|t − τ|` (tangency with linear rate).

**Lemma 1.3.**

- Under (T), (A) and (G-global), Lemma 1.1 and the remainder bound give
  `r ≥ (ε − C|d|)|d|²` for all `t ≠ τ` and all `u`.
- Under (T), (A) and (G-local) with bounded `P`,
  `r(t, x*+d, u) ≥ (ε/2)|d|²` for `|d| ≤ r_1`, with `r_1` uniform in `t`.
- In both cases, `Φ − S(T)` has growth `ε|d|²` at `x*(T)`.

So `S` is a strict local calibration on a uniform tube.

*Proof of the local case.* For `|t−τ| ≤ δ_0` use Lemma 1.1 plus the remainder.
For `|t−τ| > δ_0` we have `|σ| ≥ γ_1δ_0`. At `u°`,
`r ≥ γ_1δ_0Δ − Δ|β||d| − C|d|² − C|d|³`, which exceeds `(ε/2)|d|²` for
`|d| ≤ r_1(δ_0)`. At `u*`, `r ≥ ε|d|² − C|d|³`. Since `r` is affine in `u`, the
bound holds for every `u`. □

**1.4 How the endpoint and switching conditions enter.**

- *Terminal:* only (T). With fixed terminal components the condition applies on
  the free subspace, and the terminal multiplier enters `Φ` ([R, Remark 1.4]).
- *Initial:* none, since `x_0` is fixed.
- *Validity across a time jump* requires `P(t+) ⪰ P(t−)`: the cost identity
  picks up `+½dᵀ[P]d ≥ 0` ([V, Proposition 3.1 discussion]).
- *At the switch:* for bounded `P` the singular coefficient forces
  `β(τ±) = 0`, i.e. tangency ([R, Proposition 3.1]). It forces this only at
  the rate `∫|β|²/|σ| < ∞`, possibly logarithmic, so the linear rate (Tan) is a
  separate requirement. Theorem 2 shows it can be met.
- *The switching-time curvature `D`* does not enter the sign condition. It
  enters only through `κ = Δ²/(2D)` (Section 2.5).

## 2. The layer condition

**Theorem 1 (obstruction).** Let `S` be exact on the trajectory,
`r(t, x*(t), u*(t)) = 0`. Assume `S` is `C³` in `(t,x)` on the tube
`{τ < t ≤ T, |x − x*(t)| < r_0}`, with derivatives up to order 3 bounded. Assume
`r ≥ 0` on the tube for all `u ∈ U`, and that `Φ − S(T,·)` is minimal at
`x*(T)` on the ball of radius `r_0`. Then:

- `η_L ≥ 0`;
- if `r ≥ ε|x − x*(t)|²` and `Φ − S(T)` grows like `ε|d|²` with `ε > 0`, then
  `η_ε ≥ 0`, hence `η_L ≥ ε bᵀR(τ)b > 0`.

*Proof* (shortened after review; the short route was pointed out by [Rev]).

1. *Hessian and costate.* Exactness and `r ≥ 0` give `∇_x r = 0` along the
   trajectory, so `S_x(t, x*(t)) = ψ(t)`: the adjoint equation, with the
   terminal condition from the minimality of `Φ − S(T)`. Let
   `P(t) := S_xx(t, x*(t))`. It is `C¹` and bounded on `(τ,T]`, and
   `r_xx(t, x*, u*) = M(t,u*)` with `M` affine in `u`. At `u°` the same
   identity holds for quadratic `S`; for general `C³` `S`, `r_xx(t, x*, u°)`
   has an extra third-derivative term (Lemma 14). Step 3 uses only `u*`.
2. *Tangency at `τ+`* ([R, Proposition 3.1] applied to the right limit).
   Bounded derivatives up to order 3 make `S` and its derivatives up to
   order 2 uniformly continuous on the tube. So `r` and `∇_x r` extend
   continuously to `t = τ` from the right, and `P(τ+)` exists. For `t > τ`,
   `r(t, x*(t), u) = σ(t)(u − u_b) → 0`, so `r(τ+, x*(τ), u) = 0` for every
   `u ∈ U`. Also `r(τ+, ·, u) ≥ 0` near the interior point `x*(τ)`. Hence
   `∇_x r(τ+, x*(τ), u) = 0` at both vertices. Their difference is
   `Δ·∇_xσ_S = Δ(P(τ+)b − w) = Δβ(τ+)`, so `β(τ+) = 0`.
3. *Comparison.* Second-order necessary conditions give `M(t,u_b) ⪰ 2εI` and
   `P(T) ⪯ Φ_xx − 2εI`. For `E := Q_ε − P`,
   `Ė = −AᵀE − EA − (M(t,u_b) − 2εI)` and `E(T) ⪰ 0`. So
   `E(t) = Ψ(T,t)ᵀE(T)Ψ(T,t) + ∫_t^TΨ(s,t)ᵀ(M − 2ε)Ψ(s,t)ds ⪰ 0`, i.e.
   `P ⪯ Q_ε`.
4. *Conclusion.* With `X := E(τ+) ⪰ 0` and step 2,
   `η_ε = bᵀ(Q_ε(τ+)b − w) = bᵀXb + bᵀβ(τ+) = bᵀXb ≥ 0`.

So `η_ε ≥ 0`, and `η_L = η_ε + εbᵀR(τ)b`. □

*Mechanism (the original proof; still valid, and it shows how `P̂` fails).*
Steps 1 and 3 give `η(τ+s) ≤ η_ε(s) := bᵀ(Q_ε(τ+s)b − w) → η_ε` as `s ↓ 0`,
with `η(t) := bᵀ(Pb − w)`. Suppose `η_ε < 0`.

- *Vertex inequality in the direction `b`.* Take `t = τ + s`,
  `d = −θ·sgn(ω°η)·b` with `θ > 0`, and write `m° := bᵀM(t,u°)b`. From
  `r(t, x*+d, u°) ≥ 0` and the expansion,
  `0 ≤ |σ|Δ − θΔ|η| + ½θ²m° + Cθ³|b|³`. Choose `θ = 2|σ|/|η|`; this is
  admissible for small `s`. It gives `m° ≥ Δη²/(2|σ|) − C'|σ|/|η|`.
- *Blow-up.* For `s ≤ s_1`, `η(τ+s) ≤ η_ε/2 =: −a < 0`. With
  `|σ(τ+s)| ≤ γ_2s` and `η̇ = bᵀṖb + O(1) = m° + O(1)` (`P`, `b`, `w` are
  `C¹`), `η̇ ≥ Δa²/(2γ_2s) − C''`. Integrating from `s` to `s_1`,
  `η(τ+s) ≤ η(τ+s_1) + C''s_1 − (Δa²/(2γ_2)) log(s_1/s) → −∞`, which
  contradicts the boundedness of `P`.

*Remarks.*

- Tangency is not a hypothesis, but the hypotheses imply it (step 2). So
  `η_L < 0` rules out every exact calibration that is `C³` in `(t,x)`, with
  bounded derivatives up to order 3, on a uniform tube after the switch.
  Tangential or not is not a separate case: every such calibration is
  tangential at `τ+`. What remains are calibrations whose Hessian jumps
  across the switching surface, such as the value function of the field of
  extremals (compare Noble–Schättler's work on broken extremals and value
  functions with switching surfaces; see Sources), and windows.
- Nothing requires `n ≥ 2`.
- Theorem 1 is elementary: it is [R, Proposition 3.1] plus Lyapunov
  comparison.

**Theorem 2 (existence, local version).** If `η_L > 0`, then for every
sufficiently small `ε > 0` there is a TSQC in the local sense (Definition 1.2
with (G-local)). It is continuous at `τ` and tangential with linear rate.

*Construction.* Fix small `δ_1 > 0`.

1. *After the layer.* `P := Q_ε` on `[τ+δ_1, T]`. This satisfies (T) and (A).
   Put `β_1 := β(τ+δ_1)` and `η_1 := bᵀβ_1 = η_ε + O(δ_1)`, which is `> 0` for
   small `ε` and `δ_1`.
2. *Layer `(τ, τ+δ_1]`, prescribed `β`.* Prescribe `β(τ+s) = φ(s)β_1`, where:
   - `κ̄ := sup_{s ≤ δ_1} Δs/(2|σ(τ+s)|)`;
   - `φ(s) = 1/(1 + 2κ̄η_1 log(δ_1/s))` on `[δ_2, δ_1]`;
   - `φ(s) = λs/δ_2` on `(0, δ_2]`, with `λ := min(1, 1/(4κ̄η_1))` and `δ_2`
     chosen so that `φ(δ_2) = λ` (a fixed fraction of `δ_1`).

   Let `G*(P,t)` and `G°(P,t)` be the lower bounds on `Ṗ` from (A) and (G).
   `G°` contains the singular term `(Δ/(2|σ|))ββᵀ`. Set
   `G_m := G° + [G* − G°]_+`, so `G_m ⪰ G*, G°` and
   `|G_m − G°| = O(1 + |P|)`: by Weyl's inequality, removing the PSD singular
   term only lowers eigenvalues. Solve backward from `τ+δ_1`:

   ```
   Ṗ = G_m(P,t) + y yᵀ/(bᵀy),   y := v − G_m b,   v := φ'(s)β_1 − Pḃ + ẇ.
   ```

   Then `Ṗb = v`, so `β = Pb − w` follows the prescription exactly. `Ṗ ⪰ G_m`
   gives (A) and (G).
3. *Before the switch.* `P(τ−) := P(τ+)`, so `β(τ) = 0`.
   - On `[τ−δ_0, τ)`, with `δ_0 := δ_1`, solve `Ṗ = G_m(P,t)` backward. In the
     class `|β(t)| ≤ K|t−τ|` the singular term is `O(|t−τ|)` and Lipschitz in
     `P` with a bounded constant, so Picard iteration gives a solution with
     `β = O(|t−τ|)`.
   - On `[0, τ−δ_0)`, solve `Ṗ = G*(P,t)`, which is linear and exists
     globally.

*Proof that the construction works.*

- **`bᵀy > 0`.** `bᵀy = φ'η_1 − bᵀG°b + O(1+|P|)`, and
  `bᵀG°b ≤ κ̄φ²η_1²/s + O(1+|P|)`.
  - On the logarithmic part, `φ' = 2κ̄η_1φ²/s`, so
    `φ'η_1 − κ̄φ²η_1²/s = ½φ'η_1 ≥ κ̄η_1²λ²/δ_1`.
  - On the linear part, `κ̄φ²η_1²/s ≤ κ̄λ²η_1²/δ_2 ≤ ¼φ'η_1`.

  In both cases `bᵀy ≥ ½φ'η_1 − C(1+|P|) > 0` for small `δ_1`, as long as `P`
  stays bounded.
- **`P` stays bounded.**
  `|yyᵀ/(bᵀy)| ≤ 4φ'|β_1|²/η_1 + O(φ²/s) + O(δ_1(1+|P|)²)`. Since
  `∫φ' = 1` and `∫_0^{δ_1}φ²/s ds < ∞` (`φ ~ 1/log` near `δ_1`, and linear
  near 0), a Gronwall argument on the short interval keeps `P` bounded.
- **Conditions.** (G-local), (A), (T) and (J) hold by construction, and (Tan)
  holds with `L = λ|β_1|/δ_2`. Lemma 1.3 then gives strictness on a uniform
  tube. □

**Corollary 3 (characterization).** A local TSQC exists for some `ε > 0` if
and only if `η_L > 0`.

*Proof.* "If" is Theorem 2. "Only if": a quadratic `S` with piecewise-`C¹`
`P` and upward jumps is not literally `C³` in `(t,x)`, so Theorem 1 is not
quoted; its short argument is repeated directly. On `(τ,T]`, (A) and (T) give
`P ⪯ Q_ε` between jumps by the comparison of Theorem 1, step 3. At an upward
jump `P(t_j−) ⪯ P(t_j+)`, so `Q_ε − P` stays `⪰ 0` backward across it: upward
jumps only help. Tangency (Tan) gives `β(τ+s) → 0`. Hence
`η_ε = lim_{s↓0} bᵀ(Q_ε − P)(τ+s)b ≥ 0`, and `η_L ≥ εbᵀR(τ)b > 0`. □

In the local formulation, the maximal solution is `Q_ε` on
`[τ+δ_0, T]` followed by the singular equation on the layer. By the proof of
Theorem 1 and by Theorem 2, it is bounded on the layer for small `δ_0` exactly
when `η_ε > 0`. This is the precise sense in which "tangential calibration
⇔ `P̂` bounded" holds.

**Proposition 4 (sharp bound at the switch; rank-one jump).**

- If `P` satisfies (T) and (A) on `(τ,T]` with margin `ε` (upward jumps
  allowed), and `P(τ+)b = w`, then `η_ε ≥ 0`. If `η_ε > 0`,
  `P(τ+) ⪯ Q_ε(τ+) − β_εβ_εᵀ/η_ε`. If `η_ε = 0`, then `β_ε = 0` and the
  bound reads `P(τ+) ⪯ Q_ε(τ+)`.
- The construction of Theorem 2 attains `P(τ) = Q_ε(τ+δ_1) − β_1β_1ᵀ/η_1 + O(δ_1)`.

*Proof.* `X := Q_ε(τ+) − P(τ+) ⪰ 0` by the comparison in step 3 of Theorem 1
(and the jump argument of Corollary 3), and `Xb = Q_ε(τ+)b − w = β_ε`. So
`η_ε = bᵀXb ≥ 0`; Theorem 1 is not needed. If `η_ε = 0`, then `Xb = 0` because
`X ⪰ 0`. If `η_ε > 0`, the Schur complement of
`[[X, Xb],[bᵀX, bᵀXb]] ⪰ 0` gives `X ⪰ (Xb)(Xb)ᵀ/(bᵀXb) = β_εβ_εᵀ/η_ε`.

For attainment: in the layer, both the singular term and `yyᵀ/(bᵀy)` equal
`c(t)β_1β_1ᵀ` up to terms whose integral is `O(δ_1)`. Tangency,
`(P(τ+δ_1) − P(τ))b = β_1 + O(δ_1)`, then fixes `∫c = 1/η_1 + O(δ_1)`. □

So the best possible tangential Hessian at the switch is the last-arc Lyapunov
solution minus the rank-one term `ββᵀ/η`.

**2.5 Layer asymptotics (leading order; sketch).** Keep only the singular term
on the layer, with `κ(s) → κ`. Then:

- `β' = κηβ/s` and `η' = κη²/s`, so `β/η` is constant;
- if `η_1 > 0`: `η(s) = η_1/(1 + κη_1 log(s_1/s))` and `β → 0` at the same
  logarithmic rate. The total drop of `P` is `β_1β_1ᵀ/η_1`, as in
  Proposition 4;
- if `η_1 < 0`: `P` blows up at `s_b = s_1 exp(−1/(κ|η_1|))`.

Because `κ = Δ²/(2D)`, the exponent is `2D/(Δ²|η_1|)`. Under the SSC
(Proposition 6) this exponent exceeds 2. Checks:

- A0: `η(10⁻¹⁴) = 0.0106`, predicted 0.0101.
- B (`ε = 0`, local model): blow-up at `2.40e-3` for `δ_0 = 0.1` (predicted
  `2.81e-3`, ratio 1.17) and at `4.01e-3` for `δ_0 = 0.2` (predicted
  `5.61e-3`, ratio 1.40). The values are the integrator's event times
  (corrected after review; see Section 11).

So the leading-order law gives the right order of magnitude, within a factor
of 1.4 in these two cases; it is not accurate beyond that. It explains why the
obstruction can be invisible at practical `h` (Example B2 below).

**Theorem 9 (several switches; sketch).** For switches `τ_1 < … < τ_k`, define
`P_max` backward:

- it is the Lyapunov solution (with `2ε`) on each arc;
- at each `τ_j`, starting with the last switch, it jumps down by
  `β_jβ_jᵀ/η_j`, where `β_j := P_max(τ_j+)b_j − w_j` and `η_j := b_jᵀβ_j`.

A local TSQC exists if and only if `η_j > 0` at every switch.

- *Necessity:* Theorem 1 at each switch, with `Q_ε` replaced by `P_max`. The
  induction uses Proposition 4, `P(τ_j−) ⪯ P(τ_j+) ⪯ P_max(τ_j+) − β_jβ_jᵀ/η_j`,
  together with Lyapunov comparison on the arc between switches. As in the
  short proof of Theorem 1, tangency plus `P ⪯ P_max` on the following arc
  gives `η_j = b_jᵀ(P_max − P)(τ_j+)b_j ≥ 0` directly ([Rev]).
- *Sufficiency:* Theorem 2 at each switch. The perturbations are `O(ε + δ)`,
  and `η_j > 0` is an open condition.

The details of the induction were not written out.

## 3. Relation to the classical second-order conditions and to Osmolovskii–Maurer

**Proposition 6 (second variation).** Let `F(θ)` be the cost of the control
that switches from `u_a` to `u_b` at time `θ`. Then
`F''(τ) = D + Δ²η_L`.

*Proof.* Use the exact identity
`J(u) = S(0,x_0) + ∫_0^T r dt + (Φ − S(T))(x(T))`, with `P = Q` on `(τ,T]`
and `P` continuous at `τ`. Then `r = ½dᵀM(u_b)d + … = O(|d|³)` on the last
arc, and `Φ − S(T)` is flat to second order.

For `θ = τ + ξ` with `ξ > 0`, on `[τ, τ+ξ]` we have `d = bω(t−τ) + O(ξ²)` with
`ω = u_a − u_b`. Then
`∫r = ∫_0^ξ(γΔs + η_LΔ²s)ds + O(ξ³) = ½(D + Δ²η_L)ξ²`. The case `ξ < 0` is
symmetric: on `[τ−|ξ|, τ]` the control is `u_b` instead of `u_a`, so
`ω = u_b − u_a` and `d = bω(t − τ + |ξ|) + O(ξ²)`. Since `β(τ−) = β_L`
(`P` is continuous at `τ`), the integral is again `½(D + Δ²η_L)ξ²`. After `τ`,
`d = O(|ξ|)` and `r = O(|ξ|³)`. (Corrected after review: the first version
wrote `d = bω(τ − t)`; the integral was unchanged.) □

Checked by finite differences on 9 distinct logged parameter sets
(`logs/explore_family.log`, `logs/examples_summary.json`), with agreement to
4–7 digits; for example B: formula 1.34981, finite differences 1.349807.

**O–M quadratic form.** Osmolovskii–Maurer (Research Report RB 2007/85,
eqs. (151) and (156)) write the second variation as

`Ω = Σ_i [D^i(H)ξ_i² + 2[H_x]^i x̄_av^i ξ_i] + ∫⟨H_xx x̄, x̄⟩ + (endpoint form)`,
with `[x̄]^i = [ẋ]^i ξ_i`.

With `x_0` fixed and one switch, `x̄ = 0` before `τ` and
`x̄(τ+) = [ẋ]ξ = bΔu·ξ`, and `[H_x] = −wᵀΔu`. So `Ω = (D + Δ²η_L)ξ²`, in
agreement with Proposition 6. The SSC is therefore `D > 0` together with
`D + Δ²η_L > 0`.

**O–M Riccati test with jumps, and the calibration version.**

- Using Lyapunov `Q` on the arcs, the switch term of `Ω` becomes a quadratic
  form in `(ξ, x̄(τ−))`. Completing the square gives the jump
  `Q(τ−) = Q(τ+) − qqᵀ/b⁺` with `q := Q(τ+)[ẋ] + [H_x]ᵀ = Δu·β_L` and
  `b⁺ = D + qᵀ[ẋ] = D + Δ²η_L`.
- This is the condition `b_{k+}[Q]^k = q_{k+}ᵀq_{k+}` that [V] quotes from
  Maurer–Osmolovskii (2003) and Osmolovskii–Lempio (2002). It was derived
  here from the quadratic form above and then **checked against
  Maurer–Osmolovskii (2003)** (by [Rev], and again from the PDF for this
  revision):
  - eq. (47): `q_{k+} = ([ẋ]^k)*Q^{k+} − [ψ̇]^k`,
    `b_{k+} = D^k(H) + q_{k+}[ẋ]^k`;
  - eqs. (56)–(57), their Proposition 4.3, attributed to Osmolovskii–Lempio
    (2002): if `b_{k+} > 0` and `b_{k+}[Q]^k = (q_{k+})*(q_{k+})`, then `ω_k`
    is a perfect square;
  - Theorem 4.4 (fixed `x_0`, one switch): `b_1 ≥ 0` plus a terminal
    condition.

  Here `[ψ̇] = −[H_x]`, so `q = Δu·β_L` and `b_1 = D + Δ²η_L`. These Riccati
  tests extend the quadratic verification-function approach of
  Maurer–Pickenhain (1995) to broken extremals (Maurer–Osmolovskii 2003,
  Section 4).
- The **maximal tangential calibration** jumps by `β_Lβ_Lᵀ/η_L = qqᵀ/(qᵀ[ẋ])`
  (Proposition 4): **the same formula with `D` set to 0**. It exists iff
  `qᵀ[ẋ] > 0`.
- O–M's `Q` itself has `β(τ−) = β_L·D/(D + Δ²η_L)`. It is non-tangential
  whenever `q ≠ 0`, so it certifies the integrated second variation but is not
  a pointwise calibration. [V] made the same observation ("tangency ⇔ `q_k = 0`").

**Corollary 7 (counterexample to the "no conjugate point" reading).**

If `−D/Δ² < η_L < 0`, then:

- `D > 0` and `F''(τ) > 0`, so the extremal satisfies the bang-bang SSC and is
  a strict strong local minimum. This is by Agrachev–Stefani–Zezza (2002) and
  Osmolovskii–Maurer; the theorems are cited, not re-proved. The statement
  used is Maurer–Osmolovskii (2003), Theorem 3.2 (checked in the PDF for this
  revision): a bang-bang control with `Arg min_{v∈U} σ(t)v = [u(t−0), u(t+0)]`,
  `D^k(H) > 0` and `Ω > 0` on the critical cone minus 0 is a strict strong
  minimum. Here `Ω = (D + Δ²η_L)ξ²` (Proposition 6).
- Yet Theorem 1 excludes every `C³` exact calibration on a uniform tube, and
  hence every tangential strict quadratic calibration.
- The maximal solution `P̂` blows up in the layer after `τ`.

**Example B** (Section 6) is an instance with `n = 2`:

- `η_L = −0.4291`, `D = 3.0660`, `F''(τ) = 1.3498`;
- strict bang-bang: `|σ(t)| ≥ 0.06|t−τ|`;
- the one-switch extremal is the best bang-bang control with at most 3
  switches on a 61-point grid.

**Why `D` drops out.** `D` is the integral of the first-order term `|σ|Δ` over
a wrong-control interval of length `ξ`, i.e. a cost that appears only after
integrating along an actual switching-time variation. A calibration must be
nonnegative pointwise. At `(τ+s, x*+d)` with `|d| ~ s`, the term `|σ|Δ ≈ γsΔ`
is used up by the Schur complement against `ωβᵀd`. That is where `κ = Δ/(2γ)`
comes from. Nothing of `D` is left over to pay for `η_L < 0`.

## 4. The global-model version, and the conjecture as literally stated

**Theorem 8 (N = 0, global model; sketch).** When `b` is constant and `ℓ_1`
is affine, (A) and (G-global) are a single Riccati inequality:

`Ṗ ⪰ −AᵀP − PA − H_xx + 2εI + (Δ/(2|σ|))(Pb − w)(Pb − w)ᵀ`.

Let `P̂` be its maximal solution backward from `P(T) = Φ_xx − 2εI`,
continued through `τ` by its tangential limit `P̂(τ) := lim P̂(τ+s)` (this
limit has `β = 0`). Then a global-model TSQC with linear rate exists for this
`ε` iff `P̂` is bounded on `[0,T]∖{τ}`.

- *Necessity:* Riccati comparison on `[τ+δ,T]` as `δ → 0`, and on the left in
  the class `β = O(|t−τ|)`. In that class the closed-loop coefficient
  `(Δ/2|σ|)β` is bounded, so comparison and continuous dependence hold.
- *Sufficiency:* if `η̂ > 0` near `τ+`, apply the layer construction of
  Theorem 2 to `P̂`. It lowers `P(τ)` by `o(1)` as `δ_1 → 0`, and continuous
  dependence keeps the continuation before `τ` bounded. If instead `η̂ ≤ 0`
  near `τ+`, boundedness forces `|η̂| ≤ Cs`, and then `β̂ = O(s)` already.

The comparison through the singular point was not written out in full.

**The global model is strictly more restrictive.** Example C has
`η_L = +0.202 > 0`, so a local TSQC exists (Theorem 2). But:

- its global-model `P̂` becomes tangential only very slowly: `|β̂| = 0.15–0.27`
  at `s = 10⁻¹⁴`, as the leading-order law with `κη_1 ≈ 0.1` predicts;
- its tangential continuation blows up **before** the switch, at `t ≈ 0.46`
  (`ε = 0`) and `t ≈ 0.72` (`ε = 0.02`), for every `δ_1` tried whose
  integration completed (`logs/caseC.json`; the integration at `ε = 0.02`,
  `δ_1 = 0.05` stopped with "step size too small"). This is a conjugate point of the relaxed LQ problem
  with control weight `2|σ|/Δ`. It is the pre-`τ` gap [V] pointed out in
  [R, Remark 3.3], and it is not a property of the optimal control problem.
- After review this is established for **every** global-model calibration,
  not only the continuations tried (Proposition 15 below), given the
  (floating-point) blow-up of `P̄` at `t = 0.352`.

**4.1 Relation to the transfer theorem [R, Theorem 4.1]** (added after
review; the observation is due to [Rev]).

**Lemma 14 ((H3) implies the global model).** Let `S` satisfy (H3) of
[R, Theorem 4.1]: `∇²_x r ⪰ μI` on a tube for all `u ∈ U`, and
`|σ| > Δ|β|²/(2μ)` for `t ≠ τ`. Put `P(t) := S_xx(t, x*(t))`. If `S` is
quadratic in `x` (the class of Section 0), or if `N = 0`, then `P` satisfies
(A) and (G) with `ε = 0`, strictly, at every `t ≠ τ`.

*Proof.* At `u = u*(t)` the third-derivative terms of `r_xx` and of `Ṗ`
cancel, so `r_xx(t, x*, u*) = M(t, u*)`, and (H3) gives `M(t,u*) ⪰ μI`. If
`S` is quadratic in `x`, `r_xx(t, x*, u°) = M(t,u°)` as well. If `N = 0`,
`M(t,u°) = M(t,u*)`. In both cases, by the margin,
`M(t,u°) − (Δ/(2|σ|))ββᵀ ⪰ (μ − Δ|β|²/(2|σ|))I ≻ 0`. □

For general `S` with `N ≠ 0`, `r_xx(t,x*,u°)` differs from `M(t,u°)` by
`ω°` times third-derivative terms, and the lemma is not claimed.

**Proposition 15 (comparison from the largest admissible value; `N = 0`).**
Let `N = 0`, `ε ≥ 0` and `η_ε > 0`. Put
`P_max := Q_ε(τ+) − β_εβ_εᵀ/η_ε`, and let `P̄` solve the global-model equation
`Ṗ = G(P,t) := −(AᵀP + PA + H_xx) + 2εI + (Δ/(2|σ|))ββᵀ` backward on
`[0,τ)` from `P̄(τ) = P_max`, in the class `β̄ = O(|t−τ|)` (Picard, as in
Theorem 2, step 3). Let `P` satisfy (T), (A) on `(τ,T]`, (G) on `[0,τ)`, (J),
and tangency with `β(t) = O(|t−τ|)`. Then `P ⪯ P̄` wherever `P̄` exists.
Hence, if `P̄` has an eigenvalue that tends to `−∞` at some `t_b ∈ (0,τ)`, no
such `P` is bounded on `[0,τ)`.

*Proof.*

1. On `(τ,T]`: `P ⪯ Q_ε` (Corollary 3), so `P(τ+) ⪯ P_max` by
   Proposition 4. By (J), `P(τ−) ⪯ P(τ+) ⪯ P_max`.
2. Before `τ`, let `E := P̄ − P`, `c := Δ/(2|σ|)` and `Ā := A − cbβ̄ᵀ`. Using
   `β̄β̄ᵀ − ββᵀ = Ebβ̄ᵀ + β̄bᵀE − EbbᵀE`,
   `Ė ⪯ G(P̄) − G(P) = −(ĀᵀE + EĀ) − cEbbᵀE ⪯ −(ĀᵀE + EĀ)`.
   `Ā` is bounded, because `cβ̄ = O(1)`. So Lyapunov comparison backward from
   `E(τ−) ⪰ 0` gives `E ⪰ 0`. Upward jumps of `P` only increase `E`
   backward. □

*Numerics for example C* (`revision_checks.py cpre`, float; own computation
with the author's `model.py`):

- `P̄` blows up at `t_b = 0.3520` (`ε = 0`) and `t_b = 0.4965` (`ε = 0.02`).
  At the event (`max|P̄| = 10⁸`), `λ_min(P̄) ≈ −1.2·10⁸` (resp. `−1.4·10⁸`)
  while `λ_max(P̄) = 0.081` (resp. `0.024`), so the blow-up is to `−∞`.
- The start offset (`τ − 10⁻⁹` or `τ − 10⁻⁶`) and the integrator (LSODA,
  DOP853) change `t_b` by at most `2·10⁻⁶`.
- The earlier continuations from smaller `P(τ)` blew up sooner in the
  backward integration, at the later clock times 0.46 and 0.72, as `P ⪯ P̄`
  requires.
- For example A the same integration reaches `t = 0` without blow-up, for
  both `ε`.
- These numbers agree with [Rev] (0.352 and 0.496), which used a different
  implementation.

**Consequence for [R, Theorem 4.1].** An exact terminal term for a sequence
`h → 0` forces `P(T) ⪯ Φ_xx(x*(T))`, and (H3) includes tangency and a
Lipschitz `P`. By Lemma 14 (`N = 0`) and Proposition 15 with `ε = 0`, **no
`S` satisfies (H3) of [R, Theorem 4.1] together with an exact terminal term
in example C**, given the (floating-point) blow-up of `P̄` at `t = 0.352`,
although `η_L > 0` and local calibrations exist (Theorem 2).
So [R, Theorem 4.1] cannot give `B = f*` for C with any `S`. The only
certification route shown for C is the discrete maximal recursion with
`ε = 0` (Section 5, float, not exact). The positive local answer
(Theorem 2) does not feed into [R, Theorem 4.1] whenever the global model
fails.

**N ≠ 0.** When `b` depends on the state or `ℓ_1` is nonlinear, (A) and
(G-global) are two lower bounds on `Ṗ` in the Loewner order. The feasible set
is convex, because (G) is an LMI in `(P, Ṗ)`, but in general it has no greatest
element. So "the maximal solution `P̂`" is not defined, and the conjecture
should be read either in the local formulation (Theorems 1–2 cover general
`N`) or as feasibility of the LMI system.

## 5. Discrete side: the maximal recursion and window lower bounds

Setting: Euler data. The family is
`S_t(x) = p_tᵀx + ½(x − x̄_t)ᵀP_t(x − x̄_t)`, where `p_t` are the discrete
costates, so the residual gradient at `x̄_t` is 0. Assume the stage residual is
exactly quadratic in `(d,ω)`, as for LQ-structured data such as the examples
below:

```
ρ_t − ρ_t(z̄) = hσ_tω + hωβ_tᵀd + ½dᵀK_td + ½h²κ_tω²,
K_t = hH_xx + F_xᵀP_{t+1}F_x − P_t,   β_t = F_xᵀP_{t+1}b − w,   κ_t = bᵀP_{t+1}b.
```

**Lemma 10 (exactness over `Rⁿ × U`; maximal recursion; comparison).**

1. *Vertex stage* (`ū_t` a vertex, `σ_tω ≥ 0`). Stage `t` is exact over
   `Rⁿ × U` with margin (`K_t − 2hεI` in place of `K_t`) iff
   `m_t := 2|σ_t|/(hΔ) + κ_t > 0` and `K_t − 2hεI ⪰ β_tβ_tᵀ/m_t`, apart from
   the degenerate case `m_t = 0`, `β_t = 0`.
2. *Fractional stage* (`σ_t = 0`, both signs of `ω`). The same holds with
   `m_t = κ_t`.
3. *Maximal recursion.* The largest admissible `P_t` is
   `P̂_t = hH_xx + F_xᵀP̂_{t+1}F_x − 2hεI − β_tβ_tᵀ/m_t`.
4. *Monotonicity.* The map `P_{t+1} ↦ P̂_t` is monotone in the Loewner order.
5. *Comparison.* Every family that is exact over `Rⁿ × U` on stages `t ≥ b`,
   with `P_N ⪯ Φ_xx`, satisfies `P_t ⪯ P̂_t` for `t ≥ b`.

*Proof.*

- *Parts 1–2.* For fixed `ω̂ = |ω| ∈ (0,Δ]`, minimizing over `d` gives the
  condition `β_tᵀ(K_t − 2hε)⁺β_t ≤ 2|σ_t|/(hω̂) + κ_t`. Its right side is
  smallest at `ω̂ = Δ`. The Schur form of that condition is part 1, and the
  admissible set `{K ⪰ ββᵀ/m}` has a least element. Part 2 is the same
  argument with `σ_t = 0` and `ω` of either sign.
- *Monotonicity.* For `m > 0`,
  `dᵀP̂_td = min_v [(F_xd − vb)ᵀP_{t+1}(F_xd − vb) + hdᵀ(H_xx − 2ε)d + 2v wᵀd + 2|σ_t|v²/(hΔ)]`,
  and the bracket is increasing in `P_{t+1}`. This is one Bellman step of the
  relaxed discrete LQ problem.
- *Comparison:* induction with monotonicity. □

**Corollary 11.** Suppose the recursion with `ε = 0` breaks at stage `t_b`,
i.e. `m_{t_b} < 0`. Then no quadratic family with costate slopes that is exact
over `Rⁿ × U` on all stages `> t_b` can be exact at stage `t_b`, even over the
reachable box: the failing point `(x̄_{t_b}, u°)` has `d = 0`. So a window must
contain `t_b`. In example B, `t_b` lies within one stage of 0.00575 after the
switch for `N = 1000 … 16000` (measured 0.006, 0.006, 0.0055, 0.00575,
0.00575; at `N = 500` it is 0.008, also within one stage, `h = 0.004`). So
windows need `Θ(1/h)` stages. Exactness over the box alone, as opposed to
`Rⁿ`, is not covered by this comparison.

**Remarks.**

- *The discrete maximal recursion is more flexible than a fixed continuous
  calibration.* In example C with `ε = 0`, the recursion never breaks for
  `N = 500 … 16000`, although it is non-tangential at the switch
  (`|β_s| ≈ 0.3`). By Lemma 10 every stage is then exact over `R² × U`; the
  float stage-loss check was run at `N = 1000, 4000, 16000`. It absorbs the
  non-tangency in pushes of size `β_tβ_tᵀ/m_t`, with `m_t` growing linearly in
  the distance from the switch.
  - `max|P|` depends on whether the KKT point has an interior (fractional)
    stage (corrected after review; the first version listed only the `N`
    without one). The table is from `revision_checks.py crmax`:

    | `N` | 500 | 1000 | 2000 | 4000 | 8000 | 16000 |
    |---|---|---|---|---|---|---|
    | interior stage | yes | no | yes | no | yes | no |
    | `max\|P\|`, `ε = 0` | 11.4 | 4.6 | 22.7 | 10.2 | 88.0 | 11.0 |
    | break, `ε = 0.02` (stage, time from 0) | none | none | 42 (0.042) | none | 378 (0.0945) | none |

  - At the interior stage `m_t = κ_t ≈ 0.27` (`ε = 0`), because the
    `2|σ_t|/(hΔ)` term is absent. At the vertex stages `m_t ≥ 0.44` when there
    is no interior stage. The smaller `m_t` gives a larger push, which then
    grows in the backward recursion before the switch.
  - With `ε = 0.02` the recursion breaks only at `N` that have an interior
    stage (2000 and 8000), and far before the switch. It does not break at
    `N = 500`, which also has one (`max|P| = 67`).

  So the recursion shows no `h`-independent continuous limit in this range,
  and it is not covered by the window law of [R], which is about fixed
  continuous families. Whether it eventually breaks with `ε = 0` as `h → 0`,
  along the `N` with an interior stage, was not tested beyond `N = 16000`.
- *Two fractional stages.* With `w ≠ 0`, the discrete switching function
  depends on the previous stage's control through the state. The KKT point can
  then have two adjacent interior controls. This happened in example A0 at
  `N = 50, 200, 500, 1000, 5000` and in example B at `N = 500`. A plain
  bisection on the switching time missed this: its result violated the KKT
  signs by `5e-4` until an active-set Newton refinement was added
  (`discrete.py`, `refine_kkt`).

## 6. Numerical tests

**6.1 The example family** (`n2/model.py`). The dynamics are the double
integrator `ẋ_1 = x_2`, `ẋ_2 = u`, with `u ∈ [−1,1]` and `T = 2`. The cost is

`J = ∫ [e x_2 + (q/2)x_1² − (c/2)x_2² + (k_1x_1 + k_2x_2)u] dt − a x_1(T) + (ρ/2)x_2(T)²`.

- `w = −(k_1, k_2)`, so the costate switching function depends on the state.
- `b` is constant and `ℓ_1` affine, so `N = 0`.
- With constant `b`, the term `ℓ_1u` could be removed by adding a quadratic
  `G(x)` to the calibration (a "gauge"). The affine calibration class is not
  invariant under such changes; the quadratic class and `β`, `η_L` are.
  "`w ≠ 0`" therefore means "the costate (affine) calibration is
  non-tangential in these coordinates".

| example | parameters (others 0; `a = 1`) | `τ` | `η_L` | `D` | `F''(τ)` (finite differences) | `Δ²\|η_L\|/D` | role |
|---|---|---|---|---|---|---|---|
| A | `ρ=2, k=(−.3,−.3), q=.3, c=1, x_20=.5` | 1.31546 | +1.0475 | 3.2823 | 7.4724 (7.4724) | — | certificate; **nonconvex** in `u` |
| A0 | `ρ=1, k=(−.3,−.3), q=.3, c=.2, x_20=.5` | 1.53697 | +0.6173 | 0.6521 | 3.1213 (3.1213) | — | hidden-convex variant |
| B | `ρ=1, k=(.6,−1.2), q=1, c=.5, x_20=.5, e=.3` | 1.19803 | −0.4291 | 3.0660 | 1.3498 (1.3498) | 0.560 | counterexample |
| B2 | `ρ=.5, k=(.5,−.6), q=.3, c=.2` | 1.59551 | −0.1743 | 4.2576 | 3.5605 (3.5605) | 0.164 | thin layer |
| C | `ρ=.5, k=(.5,−.2), q=.3, c=.2` | 1.40561 | +0.2021 | 4.0820 | 4.8904 (4.8904) | — | global model fails |

- In every case the minimum-principle sign check holds (violation `≤ 9e-16`),
  and the one-switch extremal is at least as good as the best bang-bang
  control with at most 3 switches on a 61-point grid (`logs/examples_summary.json`).
- A and B are strictly bang-bang: `|σ(t)| ≥ 1.2|t−τ|` and `≥ 0.06|t−τ|`
  respectively (`logs/strict_bangbang_check.json`).
- Nonconvexity of A: at `N = 200` the Hessian of the reduced objective
  `J(u)`, which is an exact quadratic, has 7 negative eigenvalues (minimum
  `−1.1e-3`; `logs/scan_nonconvex.log`). A0's reduced Hessian is positive
  definite (minimum `3.0e-5`; `logs/exampleA0_reduced_hessian.json`), so A0 is
  convex after condensing, as in [Rv, F8].

**6.2 Window law on example A (float screening,** `n2_windows.py`**).** Each
stage residual is jointly quadratic, and its minimum over the reachable box
`D_t × U` is computed exactly in floating point by enumerating the faces of the
box. A stage fails if its loss exceeds `1e-12`. The families are:

- *affine:* `P = 0`;
- *Lyap:* discrete Lyapunov with `ε = 0.02`, non-tangential;
- *rmax:* the discrete maximal recursion of Lemma 10, `ε = 0.02`;
- *cmax:* the continuous global-model `P̂` sampled, logarithmic tangency;
- *clin, clin.02:* the linear-rate construction with `δ_1 = 0.1` and `0.02`,
  sampled;
- *clin+3h:* clin sampled at `t + 3h` (an `O(h)` tangency defect).

| N | affine | Lyap (duration) | rmax | cmax | clin | clin.02 | clin+3h |
|---|---|---|---|---|---|---|---|
| 500 | 499 | 217 (0.868) | 0 | 0 | 0 | 0 | 149 |
| 1000 | 999 | 434 (0.868) | 0 | 0 | 0 | 0 | 22 |
| 2000 | 1999 | 867 (0.867) | 0 | 0 | 0 | 0 | 0 |
| 4000 | 3999 | 1736 (0.868) | 0 | 0 | 0 | 0 | 0 |
| 8000 | 7999 | 3471 (0.868) | 0 | 0 | 0 | 0 | 0 |
| 16000 | 15999 | 6943 (0.868) | 0 | 0 | 0 | 0 | 0 |

- *affine* fails at every stage: the running cost is concave in `x_2`, so the
  failure is a Leitmann–Stalford/SGM failure on whole arcs, not a switch
  effect.
- *Lyap* fails on a fixed duration: at `N = 16000` the failing stages are
  `[s−1466, s+5476]`, i.e. the whole last arc plus 0.18 time units before the
  switch. This is `Θ(1/h)` stages, but it is **not a clean instance** of the
  non-tangential case of the window law, [R, Theorem 2.3(2)] (corrected after
  review). Checks with the continuous family `Q_ε`, `ε = 0.02`
  (`revision_checks.py lyapW5`):
  - the minimum of its residual `r` over the reachable box is negative
    exactly on `t ∈ [τ − 0.183, T]` (grid step `5·10⁻⁴`), which matches the
    failing stages (`1466h = 0.183`). This compares box with box. Over the
    true reachable set the confirmation found the residual negative only on
    about `[τ + 0.005, T]` (sampled every 0.01): the 0.183 time units before
    `τ` come from box states that cannot be reached, so they are not
    intrinsic;
  - the (W5) margin `|σ| > Δ|β|²/(2μ)`, with `μ = 2ε`, fails on the larger
    set `t ∈ [0.35, 2]`, because `|β| = 0.99–1.69` on the last arc.

  So the failure is mainly a margin and far-region failure along the whole
  last arc, reaching `T`. The switch effect (`|β(τ)| = 0.99 ≠ 0`) is present
  inside that region but is not isolated by this test.
- The tangential families have no failing stage at any `N`.
- *clin+3h* fails at small `N` on stages 23–171 after the switch, away from
  the switch. The sampled `P̂` is tight in the Schur complement, so shifting
  it breaks the inequality; the failures disappear for `N ≥ 2000`.
- A0 gives the same picture: tangential families 0 failures for
  `N = 500 … 16000`, Lyap on a fixed duration 1.04.
- In A and A0 the logarithmic rate (cmax) was enough. The linear rate is what
  the proof of [R, Theorem 2.3(1)] uses, but it was not needed here.
- In example C the logarithmic rate is far too slow and the global model fails
  before the switch (Section 4).

**6.3 Exact certificate for example A (rational arithmetic,**
`n2_certify.py`**).**

- *Data.* The rmax family with `ε = 0.02` is certificate data (float `p_t`,
  `x̄_t`, `P_t`), converted exactly to rationals. Problem data are exact
  decimals and `h = 2/N`.
- *Domains.* `D_t` is the exact reachable box:
  `x_2 ∈ x_20 ± th` and `x_1 ∈ th·x_20 ± h²t(t−1)/2`. It contains every
  feasible state, so no constraint is added and (H5) is checked, not assumed.
- *Bound.* `B = S_0(x_0) + Σ_t min_{D_t×U} ρ_t + min_{D_N}(Φ − S_N)`. Each
  minimum of a quadratic over a box is computed exactly by enumerating faces.
  The global minimum lies in the relative interior of some face; where the
  free Hessian block is singular, the minimum is also attained on a smaller
  face.
- *Upper bound.* The float KKT controls, converted exactly, with exact states
  and exact cost `J`.
- *Result.* `f*_N ∈ [B, J]` rigorously.

| N | `B` (rounded down) | `J` | `J − B` (exact) | fractional stages | time |
|---|---|---|---|---|---|
| 50 | −2.3901205246161497 | −2.3901205246161492 | 1.4e-29 | [32] | 0.1 s |
| 200 | −2.3955677925703105 | −2.3955677925703105 | 1.3e-26 | [131] | 0.4 s |
| 500 | −2.3966731723827288 | −2.3966731723827288 | 2.0e-27 | [328] | 0.7 s |
| 1000 | −2.3970431851580400 | −2.3970431851580396 | 8.5e-27 | [657] | 1.8 s |
| 2000 | −2.3972286588444520 | −2.3972286588444520 | 7.3e-26 | [1315] | 3.8 s |
| 5000 | −2.3973398227663028 | −2.3973398227663023 | 3.0e-25 | [3288] | 13.4 s |

- No stage loss exceeds `1e-20` at any `N`, so no window is used.
- *Negative control* (Lyap family, `N = 1000`): `J − B = 3.96`, with 434
  stages losing more than `1e-20`. This matches the float screening exactly.
- A0 gives gaps `≤ 2.4e-25` for `N = 50 … 5000`; its Lyap control gives 1.87
  at `N = 200` and 1.88 at `N = 1000`.
- *Cross-check* (`n2_crosscheck.py`): on 20–21 stages per family and example,
  2·10⁵ random points plus a 31³ grid in the box never gave a lower value than
  the face enumeration (largest difference `6.9e-18`, i.e. rounding).
- These are the author's own checks, not an independent verification.

**6.4 Example B: the obstruction in continuous and discrete time**
(`caseB.py`, `logs/caseB.json`).

| | `ε = 0` | `ε = 0.02` |
|---|---|---|
| continuous `P̂` (global model): blow-up at `s_b` after `τ` | 5.754e-3 | 1.321e-2 |
| local model, layer `δ_0 = 0.2` / `0.1` | 4.01e-3 / 2.40e-3 | 8.63e-3 / 4.99e-3 |
| leading-order prediction `δ_0 e^{−1/(κ\|η_L\|)}` | 5.6e-3 / 2.8e-3 | — |

The continuous values are the integrator's event times. The first version
read them off the last point of a 300-point output grid in log time (5.87e-3,
1.33e-2, 4.08e-3 / 2.46e-3, 9.25e-3 / 5.48e-3). `model.singular_riccati_after`
now returns the event time, and `caseB.py` was rerun. The global-model value
does not change with the switch point to log time (`s_top = 0.19, 0.1, 0.05`
agree to 10 digits) and agrees with [Rev]'s plain-time integrations.

Discrete maximal recursion: break stage `t_b − s`, with time after the switch
in parentheses.

| N | 500 | 1000 | 2000 | 4000 | 8000 | 16000 |
|---|---|---|---|---|---|---|
| `ε = 0` | 2 (0.008) | 3 (0.006) | 6 (0.006) | 11 (0.0055) | 23 (0.00575) | 46 (0.00575) |
| `ε = 0.02` | 4 (0.016) | 6 (0.012) | 13 (0.013) | 26 (0.013) | 53 (0.01325) | 106 (0.01325) |

At `N = 8000` and `16000` the discrete break time (0.00575 and 0.01325) lies
within one stage of the continuous blow-up distance (0.005754 and 0.01321).
The number of stages grows like `1/h`. By Corollary 11, every quadratic family
with costate slopes that is exact over `R² × U` after its window needs a
window reaching within one stage of 0.00575 time units past the switch.

**6.5 Thin layers (example B2).**

- `Δ²|η_L|/D = 0.16`, and the continuous blow-up is only `3.38e-7` after the
  switch (`ε = 0`; `1.10e-5` for `ε = 0.02`; event times,
  `revision_checks.py blowup`; the first version gave `3.5e-7`).
- At practical `N` the discrete recursion survives the last arc. It breaks
  *before* the switch, at 408, 25 and 4 stages before it for
  `N = 1000, 4000, 16000` (`logs/caseB2_thin.json`).
- **Expected behaviour, not tested:** the `Θ(1/h)` signature of Theorem 1
  should appear only once `h` is below the layer width
  `≈ exp(−2D/(Δ²|η_L|))`. The finest step tested, `h = 1.25e-4`, is far
  above `3.4e-7`.

## 7. The far-region condition (H5)

**Status.** (H5)/(W4) of [R] requires `ρ_t(z) ≥ ρ_t(z̄_t)` for
`|x − x̄_t| ≥ r`. It is a global property.

- **Local data do not imply it.** Add to `ℓ_0` a smooth bump
  `−K·φ((x − x_far)/δ)` supported outside a tube around `x*` but inside the
  reachable set. Every local condition ((A), (G), (T), tangency) is unchanged.
  For large `K`, some control reaches the bump and beats `x*`, so no family is
  exact and (H5) must fail.
- **It can be reduced to a continuous condition, checked once** (below).

**Proposition 12 (continuous far-region strictness implies (H5)).** Revised
after review: the first version assumed `S ∈ C²` in `(t,x)`, which needs `P`
to be `C²` in `t`. Theorem 2's `P` is only piecewise `C¹`, with kinks at
`τ ± δ` and a jump in `Ṗ` at `τ`. Step 2 now uses a time-averaged expansion.
Assume (H1), (H2) and (H4) of [R, Theorem 4.1], and:

- *Regularity.* `S` and `S_x` are continuous on `[0,T] × D'` for a
  neighbourhood `D'` of `D`. `S_t` and `S_xt` exist except at finitely many
  times, are bounded, and are continuous in `t` between those times. `S_x`,
  `S_xx`, `S_t` and `S_xt` are Lipschitz in `x`, uniformly in `t`. For the
  quadratic `S` of Section 0 this holds when `P` is continuous and piecewise
  `C¹` with bounded `Ṗ`, as in Theorem 2.
- *Exactness on a tube.* `S_x(t,x*(t)) = ψ(t)`, `r = 0` along `(x*,u*)`, and
  `r ≥ 0` on a tube around it, so `∇_x r(t, x*(t), u*(t)) = 0` wherever `S_t`
  exists.
- *Tangency with a linear rate:* `|β(t)| ≤ L|t − τ|`.
- **(F)**: there are `r_0, c_far > 0` with
  - `r(t,x,u) ≥ c_far` for all `t` (where `S_t` exists), `u ∈ U` and `x ∈ D`
    with `|x − x*(t)| ≥ r_0`;
  - `Φ − S(T)` exceeds its value at `x*(T)` by at least `c_far` on the same
    set.

Then for all small `h`, the transferred family `S^h_t = S(t_t,·) + a_tᵀx`,
with `a_t = p^h_t − S_x(t_t, x^h_t)`, satisfies (W4) with radius
`r_0 + e_h + Ch`, at every stage and at the terminal.

*Proof.* Write `z̄_t = (x̄_t, ū_t) = (x^h_t, u^h_t)` and `η_h = h + e_h`. The
switch stages are the `O(1 + e_h/h)` stages whose interval contains `τ` or
where `ū_t ≠ u*(t_t)`.

1. *The correction stays smooth across the switch.* With
   `y_θ = x̄_t + θg(z̄_t)`,
   `S_x(t_{t+1}, x̄_{t+1}) − S_x(t_t, x̄_t) = ∫_0^h [S_xt + S_xx g](t_t+θ, y_θ) dθ`,
   and wherever `S_xt` exists, `S_xt + S_xx g = ∇_x r − ℓ_x − g_xᵀS_x`. With
   the discrete adjoint `p_t − p_{t+1} = h(ℓ_x + g_xᵀp_{t+1})` and the
   Lipschitz bounds, this gives
   `a_{t+1} − a_t = −hg_xᵀ(p_{t+1} − S_x(t_t,x̄_t)) − ∫_{t_t}^{t_{t+1}} ∇_x r(s, x*(s), ū_t) ds + O(hη_h)`.
   The first term is `O(he_h)`. Off the switch stages the integrand is 0. On
   them it is `(ū_t − u*(s))β(s) = O(|s − τ|) = O(η_h)` **by linear-rate
   tangency**. Hence `a_{t+1} − a_t = O(hη_h)` at every stage. (H4)
   compares `p_{t+1}` with `ψ(t_t)`, so directly
   `a_t = p_t − S_x(t_t, x̄_t) = O(e_h + h) = O(η_h)`; only `a_N = O(e_h)`.
   The later bounds use only `O(hη_h)`.
2. *The residual is close to the averaged `r`.*
   `S(t_{t+1}, x + hg) − S(t_t, x) = ∫_0^h [S_t + S_xᵀg](t_t+θ, x+θg) dθ`, and
   the Lipschitz bounds on `S_t`, `S_x` give
   `ρ_t(z) = ∫_{t_t}^{t_{t+1}} r(s, x, u) ds + (a_{t+1} − a_t)ᵀx + h a_{t+1}ᵀg(x,u) + E_t(z)`,
   with `|E_t| ≤ Ch²` on `D × U`. So
   `ρ_t(z) − ρ_t(z') = ∫ [r(s,z) − r(s,z')] ds + O(hη_h)` on the bounded set
   `D × U`. Only piecewise continuity of `S_t` in `t` is used.
3. *The trajectory point.* For `s` in the stage interval,
   `r(s, z̄_t) ≤ σ(s)(ū_t − u*(s)) + |β(s)||ū_t − u*(s)||x̄_t − x*(s)| + C|x̄_t − x*(s)|²`.
   This is `O(η_h²)` off the switch stages and `O(η_h)` on them, so
   `∫ r(s, z̄_t) ds ≤ Chη_h`.
4. *Conclusion.* If `|x − x̄_t| ≥ r_0 + e_h + Ch`, then `|x − x*(s)| ≥ r_0`
   on the whole stage interval, so `∫ r(s,x,u) ds ≥ hc_far` by (F), and
   `ρ_t(z) − ρ_t(z̄_t) ≥ h[c_far − Cη_h] > 0` for small `h`. The terminal
   term `Φ − S(T,·) − a_Nᵀx`, with `a_N = O(e_h)`, is handled the same way
   using the second part of (F). □

The revised steps 1–2 follow [S, Theorem 5.2] with integrals over the stage
in place of values at `t_t`. They were written for this revision; the
confirmation (`reviews/ext-bangbang-n2-confirm.md`, item 4) checked them and
found two imprecisions without effect, fixed in Section 11.1.

**Scope.** Using Proposition 12 inside [R, Theorem 4.1] also needs (H3).
(H3) implies (A) and (G) with `ε = 0` at every `t ≠ τ` for quadratic `S`,
and for every `S` when `N = 0` (Lemma 14). So in that use, Proposition 12 concerns global-model calibrations.
Local calibrations are different: Theorem 2's calibrations violate (F) in
examples A and C (below).

**Proposition 13 (LQ-structured data, global-model calibrations).** Assume
`a(x)` is affine, `b` is constant, `ℓ_0` and `Φ` are quadratic, `ℓ_1` is
affine, and `S` is quadratic. Then `r` and the Euler stage residuals are exact
quadratics in `(d,ω)`. So:

- (T), (A) and (G-global) give `r ≥ ε|d|²` for **all** `d`, by Lemma 1.1 with
  `R₃ = 0`. That is (F) with `c_far = εr_0²`.
- In discrete time, exactness over `Rⁿ × U` (Lemma 10) implies exactness over
  every convex box.

The data of examples A, A0, B and C are of this type. □

The conclusion needs a global-model calibration. One exists for A and A0: the
continuous global-model families with `ε = 0.02` reach `t = 0` without
blow-up (`logs/examples_summary.json`), and so does the discrete maximal
recursion. None exists for B (`η_L < 0`) or for C (Proposition 15).

**Local calibrations violate (F) and the (H3) margin in examples A and C**
(added after review; own check `revision_checks.py localF`, float, confirming
[Rev]). After the layer, Theorem 2's `P` equals `Q_ε` for every `δ_1`, so
`M = 2εI` there. For LQ data this gives
`r(t, x*+d, u*+ω) = σω + ωβᵀd + ε|d|²` exactly, and the minimum over the
continuous reachable box `D_t × U` has a closed form. On `[τ + 0.02, T]`
(2001 sampled times, so the result holds for every `δ_1 ≤ 0.02`):

| example, `ε` | min of `r` over `D_t × U` | (F) fails at | min of (H3) margin `\|σ\| − Δ\|β\|²/(2μ)`, `μ = 2ε` |
|---|---|---|---|
| A, 0.02 | −6.55 | every sampled `t` | −70 |
| A, 0.01 | −6.72 | every sampled `t` | −144 |
| C, 0.02 | −2.55 | every sampled `t` | −7.1 |
| C, 0.01 | −2.90 | every sampled `t` | −15.6 |

- The closed form was checked against `r` evaluated from its definition
  (difference `≤ 3·10⁻¹⁵` at 400 random points), and the box minimum against
  a 401 × 401 grid (`revision_checks.py rcheck`).
- [Rev] found −6.6 for A and −4.5 for C over its whole instances, including
  the part before `τ`.
- So these local calibrations are not calibrations on the reachable set, and
  Proposition 12 does not apply to them. The reason is structural: after the
  layer, (A) with equality leaves only the margin `2εI`, while `|β|` stays at
  1.01–1.71 (A) and 0.53–0.57 (C) on `[τ + 0.02, T]`.

**What remains assumed in general.** For nonlinear data, (F) is a condition on
the continuous `S` over `[0,T] × D × U`: `n + 2` dimensions, independent of
`h`. It can be checked once, for example by interval branch-and-bound, instead
of stage by stage. I found no a-priori condition on the problem data alone
that implies (F), beyond LQ structure or global convexity of `r(t,·,u)` on `D`.
The convex case is immediate: Lemma 2.1 of [R] then applies with the ball
replaced by `D`.

## 8. Open questions

- Theorem 9 (several switches) and Theorem 8 (global model, `N = 0`) are
  sketches: the induction and the comparison through the singular point need
  to be written out.
- The borderline case `η_L = 0` for non-strict calibrations.
- Discrete lower bounds on window size for exactness over the **box** only;
  Corollary 11 covers exactness over `Rⁿ`.
- **A transfer theorem for local calibrations** (added after review). It
  would be a version of [R, Theorem 4.1] that uses only (G-local): a small
  ball radius, with (W4) at that radius. The far region is the real
  obstruction there, since Theorem 2's calibrations violate (F) in examples A
  and C. Example C, where local calibrations exist but no global-model
  calibration does (Proposition 15), is the test case.
- The growth of the discrete maximal recursion in example C as `h → 0`.
  Along the `N` whose KKT point has an interior stage, `max|P|` is 11.4,
  22.7 and 88.0 at `N = 500, 2000, 8000` (`ε = 0`). Does it eventually break
  with `ε = 0`?
- In the regime `−D/Δ² < η_L < 0`: whether windows of `O(log(1/h))` stages, or
  several small windows accumulating at the switch, can replace one window of
  fixed duration. Not tested.
- Singular arcs, state constraints, several controls: unchanged from [R].
  (*Root, 2026-09-30:* singular arcs are now treated in
  [`singular-arcs.md`](singular-arcs.md), and window exactness at one
  regular switch in [`window-exactness.md`](window-exactness.md).)

## 9. Status

[Rev] checked the proved items of the first version and re-implemented most
numerics (not the cmax, clin and clin+3h screening families). Items added or
changed after review are marked. The confirmation
(`reviews/ext-bangbang-n2-confirm.md`) checked them, apart from the sketches
of Theorems 8 and 9 beyond the added necessity note. The changes are listed
in Section 11.

| item | status |
|---|---|
| Lemma 1.1 (vertex reduction), Lemma 1.3 | proved |
| Theorem 1 (obstruction; any `n`; tangency implied by the hypotheses) | proved; short proof via [R, Proposition 3.1] plus Lyapunov comparison |
| Theorem 2 (existence, local version, linear rate) | proved; continuous existence only, does not feed into [R, Theorem 4.1] (Section 4.1) |
| Corollary 3 (local TSQC ⇔ `η_L > 0`) | proved; jumps in `P` covered |
| Proposition 4 (rank-one bound, sharp in the limit) | proved (`η_ε ≥ 0`; case `η_ε = 0` added); attainment argued to `O(δ_1)` |
| Section 2.5 layer asymptotics | leading order (sketch); same order as numerics, within a factor 1.4 for B |
| Proposition 6 (`F'' = D + Δ²η_L`) | proved; matches the O–M form (RB 2007/85) and finite differences |
| O–M jump with `D` removed | derived here; checked against Maurer–Osmolovskii (2003), eqs. (47), (56)–(57) and Theorem 4.4 |
| Corollary 7 (counterexample to the "no conjugate point" reading) | proved, given the cited SSC theorems (MO 2003, Theorem 3.2); example B |
| Theorem 8 (global model, `N = 0`) | sketch |
| Lemma 14 ((H3) ⇒ global model, quadratic `S` or `N = 0`) | proved; added after review, checked in `reviews/ext-bangbang-n2-confirm.md` |
| Proposition 15 (comparison from `P_max`) and its application to C | proof added after review, checked in `reviews/ext-bangbang-n2-confirm.md`; the blow-up of `P̄` is float numerics |
| `N ≠ 0`: no maximal solution in general | remark |
| Theorem 9 (several switches) | sketch |
| Lemma 10, Corollary 11 (discrete) | proved (Corollary 11 for exactness over `Rⁿ × U`) |
| Proposition 12 ((F) ⇒ (H5)) | proof revised after review (time-averaged step, piecewise-continuous `S_t`); follows [S, Theorem 5.2]; revision checked in `reviews/ext-bangbang-n2-confirm.md` (two harmless imprecisions, fixed in Section 11.1) |
| Proposition 13 | proved, for global-model (G-global) calibrations only |
| Theorem 2's calibrations and (F), (H3) margin in A and C | violated (float, own check and [Rev]) |
| Example A screening (6.2) | float; the Lyap control is mainly a margin/far-region failure |
| Example A and A0 certificates (6.3) | exact rational arithmetic; reproduced by [Rev] |
| Example B tables (6.4), B2, C | float; continuous blow-up distances corrected after review |

## 10. Commands run and files

All runs were from `theory-bangbang/n2/` with `OMP_NUM_THREADS=1`: targeted
checks only, no project-wide verification, no CI inspection. Timeouts were
≤ 50 min per command; the longest run was about 3 min.

1. `python3 explore_family.py` → `logs/explore_family.log` (`F''` check;
   bang-bang grid).
2. `python3 scan_rmax.py` → `logs/scan_rmax.log`;
   `python3 scan_caseB.py` → `logs/scan_caseB.log`;
   `python3 scan_nonconvex.py` → `logs/scan_nonconvex.log`.
3. `python3 caseB.py` → `logs/caseB.{log,json}`; B2 inline →
   `logs/caseB2_thin.{log,json}`.
4. `python3 caseC.py` → `logs/caseC.{log,json}`; inline checks →
   `logs/caseC_global_vs_local.*` and `logs/caseC_rmax_exact.*`.
5. `python3 n2_windows.py A0 …` and `python3 n2_windows.py A 500 1000 2000 4000 8000 16000`
   → `logs/n2_windows.jsonl` (records tagged `A0` and `A`) and
   `logs/n2_windows_A.log`.
6. `python3 n2_certify.py 50 200 500 1000 2000 5000 lyap 200 1000` (A0) and
   `python3 n2_certify.py A 50 200 500 1000 2000 5000 lyap 1000` →
   `logs/n2_certify.jsonl`.
7. `python3 n2_crosscheck.py` → `logs/n2_crosscheck.{log,json}`.
8. `python3 examples_summary.py` → `logs/examples_summary.{log,json}`; inline
   checks → `logs/strict_bangbang_check.json` and
   `logs/exampleA0_reduced_hessian.json`.

Revision after review (same rules; `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=1`;
each run under `timeout`):

9. `python3 caseB.py` after the fix in `model.singular_riccati_after` →
   `logs/caseB.{log,json}` (overwritten; 72 s). The continuous values changed
   as listed in Section 6.4. The discrete values, `η_L`, `D` and `F''` are
   unchanged.
10. `python3 revision_checks.py blowup cpre localF lyapW5` →
    `logs/revision_checks_fast.log` and `logs/revision_checks_<part>.json`
    (under a minute).
11. `python3 revision_checks.py crmax` → `logs/revision_checks_crmax.{log,json}`
    (a few minutes).
12. `python3 revision_checks.py rcheck` → `logs/revision_checks_rcheck.{log,json}`.
13. Inline: `|β|` range of `Q_ε` on `[τ + 0.02, T]` for A and C (Section 7;
    not logged).
14. Sources: Maurer–Osmolovskii (2003) PDF downloaded to a scratch directory
    and read with `pdftotext` (eqs. (41), (47), (56)–(57), Theorems 3.2 and
    4.4, reference list). Two web searches for the published form of
    Noble–Schättler.

Files:

- `model.py`: the continuous family, `F''`, the singular Riccati equation, and
  the continuous calibration families;
- `discrete.py`: the Euler transcription, KKT solve with active-set
  refinement, the families, and the exact box minimum in floating point;
- `n2_windows.py`, `n2_certify.py`, `n2_crosscheck.py`, `caseB.py`,
  `caseC.py`, `examples_summary.py`, and the `scan_*.py` scripts;
- `revision_checks.py`: the checks added after review (Section 11).

The earlier record tagged `A` in the first screening run was relabelled `A0`
when the nonconvex example became the main example A. A failed screening run
for example C, which aborted because the continuous layer construction broke
down at `δ_1 = 0.1`, left no log. The failure recorded in `logs/caseC.json`
is a different one: the continuation at `ε = 0.02`, `δ_1 = 0.05` stopped with
"step size too small".

## Sources

- N. P. Osmolovskii, H. Maurer, *Second order optimality conditions for
  bang–bang control problems, Part 2*, Research Report RB/85/2007, IBS PAN:
  eqs. (94), (151), (156) (the quadratic form and `D^i(H)`),
  [PDF](https://www.rcin.org.pl//Content/217459/PDF/RB-2007-85.pdf),
  [record](https://rcin.org.pl/publication/255071).
- H. Maurer, N. P. Osmolovskii, *Second order conditions for bang-bang control
  problems*, Control Cybern. 32(3) (2003),
  [record](https://geodesic.mathdoc.fr/item/CC_2003_32_3_a8/),
  [PDF](http://matwbn.icm.edu.pl/ksiazki/cc/cc32/cc3238.pdf). Checked for this
  revision: eq. (47), eqs. (56)–(57) (Proposition 4.3), Theorem 3.2 (the
  sufficient condition for a strict strong minimum) and Theorem 4.4.
- A. A. Agrachev, G. Stefani, P. Zezza, *Strong optimality for a bang-bang
  trajectory*, SIAM J. Control Optim. 41 (2002) 991–1014 (bibliographic
  details as in the reference list of Maurer–Osmolovskii 2003). Cited for
  "SSC ⇒ strict strong local minimum"; the theorem itself was not read.
- H. Maurer, S. Pickenhain, *Second-order sufficient conditions for control
  problems with mixed control-state constraints* (title as in publication
  records and in [R]; the Maurer–Osmolovskii reference list says "optimal
  control problems"), J. Optim. Theory
  Appl. 86 (1995) 649–667 (details from the same reference list). This is the
  Riccati approach to second-order sufficiency (quadratic verification
  functions) that Maurer–Osmolovskii (2003, Section 4) and Osmolovskii–Lempio
  extend to broken extremals. Not read for this note.
- J. Noble, H. Schättler, *Sufficient conditions for relative minima of broken
  extremals in optimal control theory*, listed as "submitted" (2001) in
  Maurer–Osmolovskii (2003); J. Noble, D.Sc. thesis, *Parametrized families of
  broken extremals and sufficient conditions for relative minima*, Washington
  University in St. Louis, 1999
  ([record](https://www.mathgenealogy.org/id.php?id=38317)). This line of work
  treats fields of broken extremals and value functions with switching
  surfaces, which is the nonsmooth alternative left open by Theorem 1. The
  journal version is J. Noble, H. Schättler, J. Math. Anal. Appl. 269 (2002)
  98–128 (details from a secondary citation, reference [20] of
  arXiv:1506.00569); the work was not read.
- Novelty: [Rev]'s brief web search found no prior statement of Theorems 1–2,
  of the "`D(H)` set to zero" reading, or of the counterexample in
  Corollary 7. These results are elementary.
- The SICON link in [R] now returns an HTML page instead of the PDF (checked
  2026-09-30).

## 11. Revision after review

Review: [Rev] (`reviews/bangbang-n2-review.md`), verdict "fixes needed; the
main results survive". Each issue was verified before the text was changed.
The own checks below use the author's `model.py` and `discrete.py` plus the
new `n2/revision_checks.py`. They are targeted float checks, not CI and not
an independent re-review.

1. **The local result does not connect to the transfer theorem** (review
   issue 1). *Verified.*
   - Lemma 14 (new) proves that (H3) of [R, Theorem 4.1] implies (A) and (G)
     with `ε = 0` at every `t ≠ τ`. Scope: for quadratic `S`, and for every
     `S` when `N = 0`. For general `S` with `N ≠ 0` it is not claimed,
     because `r_xx(t,x*,u°)` then contains third-derivative terms.
   - Proposition 15 (new) writes out the comparison from
     `P_max = Q_ε(τ+) − β_εβ_εᵀ/η_ε` that [Rev] used.
   - `revision_checks.py cpre`: for example C, `P̄` blows up to `−∞` at
     `t = 0.3520` (`ε = 0`) and `0.4965` (`ε = 0.02`), robust to the start
     offset and the integrator. For A there is no blow-up. This agrees with
     [Rev].
   - Consequence added (Section 4.1): no `S` satisfies (H3) with an exact
     terminal term in example C, so [R, Theorem 4.1] cannot give `B = f*`
     for C.
   - `revision_checks.py localF`: after the layer, Theorem 2's `P = Q_ε`
     violates (F) and the (H3) margin at every sampled time in A and C. The
     minimum of `r` over the reachable box is −6.55 (A) and −2.55 (C) at
     `ε = 0.02`. This covers the post-layer part only; [Rev]'s −4.5 for C
     includes the part before `τ`. The closed form was validated by
     `revision_checks.py rcheck`.
   - Text changed: Summary item 3 ("avoids both problems ... only for the
     continuous existence question"), new Summary item 4, the (H5) bullets
     ("for global-model (G-global) calibrations"), Section 4.1 (new),
     Section 7 (Scope paragraph, Proposition 13 heading, new table), the new
     open item in Section 8, and the status table.
2. **Continuous blow-up distances** (issue 2). *Verified.*
   - `model.singular_riccati_after` returned `exp(r2.t[-1])`, the last point
     of the `t_eval` grid, instead of the event time. It now returns
     `t_events` (phase 1 also uses `t_events`).
   - `caseB.py` was rerun. New values: `5.754e-3`, `1.321e-2`,
     `4.01e-3 / 2.40e-3`, `8.63e-3 / 4.99e-3`. They agree with [Rev] to the
     digits shown and do not depend on `s_top`.
   - B2 blow-up: `3.38e-7`, not `3.5e-7` (the old value was not logged).
   - Unaffected: the pre-switch blow-up times 0.46 and 0.72 of `caseC.py`.
     `continuous_family` integrates without `t_eval`, so `r3.t[-1]` is the
     event time there.
   - Section 2.5: the leading-order predictions are off by factors 1.40 and
     1.17. "Matches numerics" was replaced by "same order, within a factor
     1.4".
   - Text changed: Summary, Sections 2.5, 6.4 and 6.5, and the status table.
3. **Theorem 1** (issue 3). *Verified.* The hypotheses imply `β(τ+) = 0` by
   the right-limit version of [R, Proposition 3.1]. Then
   `η_ε = bᵀ(Q_ε − P)(τ+)b ≥ 0`.
   - The short proof is now the proof. The blow-up argument is kept as the
     "mechanism".
   - "No tangency is assumed" and "tangential or not" were reworded.
   - The Summary now says `C³` in `(t,x)` with bounded derivatives up to
     order 3 on a uniform tube after the switch.
   - Proposition 4 no longer cites Theorem 1 for `η_ε ≥ 0`.
4. **Lyapunov negative control** (issue 4). *Verified* with
   `revision_checks.py lyapW5`.
   - The (W5) margin fails on `t ∈ [0.349, 2]`, with `|β| = 0.99–1.69` on
     the last arc.
   - The box minimum of the continuous residual is negative exactly on
     `[τ − 0.183, T]`, which matches the discrete failing stages
     `[s − 1466, s + 5476]` at `N = 16000` (`1466h = 0.183`).
   - Section 6.2 and the Summary now say that this is mainly a margin and
     far-region failure, with the switch effect present but not isolated.
5. **Example C discrete recursion** (issue 5). *Verified*, with one addition,
   using `revision_checks.py crmax`.
   - With `ε = 0`, `max|P|` is 11.4, 4.6, 22.7, 10.2, 88.0 and 11.0 for
     `N = 500 … 16000`. The large values occur at the `N` whose KKT point has
     an interior stage (500, 2000, 8000).
   - With `ε = 0.02` the recursion breaks at `N = 2000` and 8000. Both have
     an interior stage, but `N = 500` has one and does not break. [Rev] did
     not list `N = 500`.
   - Section 5 now reports the full table, and the Section 8 item was
     updated.
6. **Example B2** (issue 6): "appears only once `h` is below the layer width"
   is now labelled expected behaviour, not tested.
7. **"0.00575 for every `N`"** (issue 7). *Verified* from the rerun
   `caseB.py`: 0.006, 0.006, 0.0055, 0.00575 and 0.00575 for
   `N = 1000 … 16000`. Now "within one stage of 0.00575" (Corollary 11,
   Summary, Section 6.4).
8. **Proposition 12 regularity** (issue 8). *Verified* that Theorem 2's `P`
   has kinks at `τ ± δ` and a jump in `Ṗ` at `τ`, so the first version's
   `C²` hypothesis failed.
   - The averaged-expansion option was chosen. It needs only piecewise
     continuous `S_t` and `S_xt` and Lipschitz bounds in `x`.
   - Steps 1–3 now integrate over the stage. The (W4) radius is now
     `r_0 + e_h + Ch`, and tangency with a linear rate is stated explicitly.
   - This revised proof has not been checked independently. Proposition 12
     still does not apply to Theorem 2's calibrations, because they violate
     (F) (item 1).
9. **Small errors and citations** (issue 9).
   - Proposition 6: for `ξ < 0` the deviation is `d = bω(t − τ + |ξ|)`,
     with `ω = u_b − u_a`. The integral is unchanged.
   - Proposition 4: `η_ε ≥ 0`, and the case `η_ε = 0` (then `β_ε = 0`) was
     added.
   - Corollary 3: the "only if" proof now covers upward jumps directly.
   - Theorem 9: the direct necessity argument was noted.
   - O–M line: upgraded to "checked against Maurer–Osmolovskii (2003), eqs.
     (47), (56)–(57) and Theorem 4.4". I read these in the PDF myself. I also
     cite their Theorem 3.2 for the SSC used in Corollary 7.
   - Citations added: Maurer–Pickenhain (1995), and Noble–Schättler (thesis
     1999; the 2001 manuscript cited by Maurer–Osmolovskii). Neither was
     read. The journal version of Noble–Schättler was not located.
   - A novelty line was added: "not found in a brief search; elementary".

Not adopted:

- [Rev]'s side observations were not added, because they were not rechecked
  here: Proposition 4 attained at rate `O(δ_1²)`, and the `ε = 0.02` breaks
  of the B2 recursion.

### 11.1 Root edits after the confirmation (2026-09-30)

The confirmation (`reviews/ext-bangbang-n2-confirm.md`) found the revision's
fixes correct and listed ten minor remaining items. Each was checked against
the text, the logs or the confirmation's sources before the text was
changed. No result, number in a table, or proof conclusion changes.

1. **Float caveat (item 1).** The bold Consequence in Section 4.1 and the
   Section 4 bullet now say "given the (floating-point) blow-up of `P̄` at
   `t = 0.352`".
2. **Broken table (item 2).** The stray table header at the start of
   Section 9 is deleted; the status line there now cites the confirmation.
3. **Section 5, example C (item 3).** "`m_t ≥ 0.45`" became "`≥ 0.44`" (the
   minimum is 0.448 at `N = 4000`, `ε = 0`, per the confirmation).
4. **Proposition 12, step 1 (item 4).** `a_t = O(e_h + h) = O(η_h)`, and only
   `a_N = O(e_h)`; the later bounds use only `O(hη_h)`. The sentence saying
   that steps 1–2 were not checked independently now cites the
   confirmation.
5. **Scope paragraph in Section 7 (item 5).** "(H3) implies (G-global)"
   became "(H3) implies (A) and (G) with `ε = 0` at every `t ≠ τ`", as in
   Summary item 4 and Lemma 14.
6. **Noble–Schättler (item 6).** The journal version is cited, J. Math.
   Anal. Appl. 269 (2002) 98–128, from a secondary citation; it was not
   read.
7. **Lyapunov failure before `τ` (item 7).** One sentence in Section 6 says
   that the 0.183 time units before `τ` come from box states that cannot be
   reached (the confirmation's reachable-set computation).
8. **Pre-existing log statements (item 8).** Section 4 now says that one
   continuation (`ε = 0.02`, `δ_1 = 0.05`) stopped with "step size too
   small", which `logs/caseC.log` shows; Section 10 no longer attributes
   that logged failure to `δ_1 = 0.1`.
9. **Theorem 1, step 1 (item 9).** The identity is stated at `u*`; at `u°`
   it holds for quadratic `S` only, and step 3 uses only `u*`.
10. **Maurer–Pickenhain title (item 10).** The Sources entry uses the title
    of the publication records, which [R] checked against Crossref.
11. **Header.** It cites the confirmation.
12. **Status table, Section 9 (closing audit, 2026-09-30).** The rows for
    Lemma 14, Proposition 15 and Proposition 12 said "not re-checked". They
    now say "checked in `reviews/ext-bangbang-n2-confirm.md`", which
    rechecked all three proofs line by line (its Verdict and item 4).
13. **Table rendering (closing audit, 2026-09-30).** In the example table
    of Section 6.1, the header cell `Δ²|η_L|/D` split into extra
    cells, so GitHub-flavoured Markdown did not render the table. The same
    happened to one row of the Section 6.4 table (`κ|η_L|`). The `|`
    characters inside these code spans are now escaped as `\|`. The text is
    unchanged.
