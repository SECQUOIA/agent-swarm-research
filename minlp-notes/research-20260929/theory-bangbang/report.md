# Bang-bang transcriptions: window certificates, the tangency condition, and optcdeg2 closed

Date: 2026-09-30. Status: independently verified with fixes
([verification](../reviews/bangbang-verification/verification-report.md));
corrections applied by the root in Section 9.1; residual issues from a
round-1 confirmation fixed in Section 9.2; a round-2 confirmation
([report](../reviews/bangbang-root-fixes-confirm-r1.md)) found those fixes
correctly applied, and its three remaining issues are fixed in Section 9.3.
A round-3 confirmation
([report](../reviews/bangbang-root-fixes-confirm-r2.md)) found the third
revision correct; its optional nit was applied by the root. After the
round-3 follow-ups (`window-exactness.md`, `singular-arcs.md`) the root
corrected a factor-2 slip in the proof of Theorem 4.1 (step (c)), added a
missing terminal hypothesis to its statement, and added pointers to those
notes (end of Section 9). Proofs are
complete unless labelled "sketch", "heuristic" or "conjecture". The optcdeg2
bound (Section 5) uses outward-rounded interval arithmetic. Section 5.7 is a
floating-point screening.

*Provenance note (root).* The agent that produced these results could not
write this file because its tool environment blocked `.md` report writes;
the root saved the agent's report text verbatim on 2026-09-30.

Cited notes:

- **[S]** `theory-calibration/scouting.md`;
- **[Rv]** `reviews/calibration-review.md`; its corrections are built into
  the hypotheses below;
- **[O]** `open-instances/open-instances-report.md`, Section 6;
- **[V]** `reviews/open-instances-verification/verification-report.md`,
  Section 6;
- **[E]** `theory-bangbang/extension-n2.md`, the follow-up on state
  dimension `n ≥ 2`; reviewed in `reviews/bangbang-n2-review.md`, and its
  revision confirmed in `reviews/ext-bangbang-n2-confirm.md`.

## Summary

**optcdeg2 is closed.** The certified lower bound is
**293.8760750958728**. A rigorously feasible point built by the verifier
gives f* ≤ 293.87607509587509328, so the gap is **2.3e-12** (7.8e-15
relative). The previous bound was 293.8699938542 (gap 6.08e-3). The author's
refined primal point, 293.87607509588105, satisfies the rows only to 8.9e-16
and lies 6.0e-12 above that upper bound; an earlier version measured the gap
(8.3e-12) against it.

- The certificate is one quadratic calibration,
  `S_t = p_t·x + (q_t/2)(v − v_t)²`, with no windows and no head block.
- The curvature `q_t` is zero at both switches and grows on the two
  `u = −0.2` arcs.
- After `y` and `u` are eliminated exactly, each stage check is a 1-D
  interval computation; the whole run takes 6.6 s.
- An exact-rational recheck by the author on 330 stages found no violation.
- **Independent verification (exact rational arithmetic, all stages):** the
  same calibration gives exactly 293.876075095875092379… (truncated), and a
  rigorously feasible point gives f* ≤ 293.87607509587509328, so the optimum
  is bracketed within 9.0e-16. The author's bound is valid (2.3e-12 below the
  exact value of the same certificate); the author's primal point is not
  exactly feasible (rows off by 8.9e-16) and its value is 6.0e-12 too high
  (Sections 5.5 and 9).

**Window size as h → 0.** What decides it is whether the calibration's
switching function has zero state gradient at the switch point
("tangency"):

- **Non-tangential calibrations** fail on a window of fixed *duration*,
  which is Θ(1/h) stages. Costate (affine) calibrations fall here whenever
  the costate switching function depends on the state at the switch.
  Adding state dependence without tangency does not help.
- **Tangential calibrations** fail on at most O(1 + e_h/h) stages, where
  e_h is the discrete convergence error: O(1) stages when e_h = O(h), and
  possibly zero, as in optcdeg2.
- In continuous time, every calibration that is twice differentiable in the
  state and exact on the trajectory is tangential. Strict quadratic
  calibrations correspond to a Riccati inequality whose coefficient blows up
  at the switch, which forces tangency.

So field-type calibrations shrink the window to O(1) stages only when they
are tangential. The value function of the field of extremals is neither
strict nor tangential.

**Numerical checks (float screening, not certified).** On the optcdeg2
family (N = 6250 … 100000) the costate calibration fails on 2.32 time units
at every N, but this is a stage-wise Mangasarian (SGM) failure on the whole
head and tail arcs (optcdeg2 has w = 0), not a window-size effect; the
tangential calibration has no failing stage; a non-tangential offset fails
on a fixed duration of 0.047; an O(h) tangency defect fails on at most one
stage. The window law itself was tested by the verifier on a toy with
w = 0.5 (min ∫(x−a)²/2 + kxu, ẋ = u, |u| ≤ 1, k = −0.5). With the box
domain |x| ≤ 2, the affine family fails on 0.270 time units, symmetric about
the switch, at N = 500 … 8000 (0.272 at N = 500; prediction 0.280); the
tangential family has no failing stage (its terminal term is inexact,
however: terminal loss about 3.19 at `N = 1000`, so its bound is 3.19 below
`f*`; a tangential family with an exact terminal term gives an exact
rational certificate with no window, `window-exactness.md` Section 7.2). With the exact reachable set as domain, the
trajectory lies on its boundary before the switch, so the ball hypothesis
`B_r(x̄_t) ⊂ D_t` fails there; the affine window is then one-sided (before
the switch) and four times shorter, 0.068–0.070 time units, but still of
fixed duration.

**State dimension n ≥ 2 (answered in [E]).** For one regular switch, fixed
`x_0` and a free endpoint, a strict tangential quadratic calibration in the
local formulation exists if and only if one number `η_L` is positive, for any
`n`. The "no conjugate point" reading of the earlier conjecture is refuted.
In the global form that Theorem 4.1 needs, the sign of `η_L` does not decide:
even with `η_L > 0`, the solution that bounds every global-form calibration
from above can tend to `−∞` before the switch ([E, Example C]) or, in a
scalar example, after it (both blow-ups are floating-point results). See
Remark 3.3.

**Still open:** a transfer theorem for local calibrations ([E, Section 8]);
an a-priori guarantee that states far from the trajectory never undercut it
(checked stage by stage in practice; reduced to a continuous condition in
[E, Proposition 12]); singular arcs (largely worked out in
`singular-arcs.md`; a global catmix calibration and a rigorous catmix
certificate remain open); state constraints; certificates when
`κ_τ < 0` (windows of fixed duration). Window exactness, assumed in
Theorem 4.1, is decided under stated hypotheses in `window-exactness.md`
(Section 6 below).

## 0. Setting and notation

- **Transcription (P).** Minimize `Σ_{t<N} L_t(x_t,u_t) + Φ(x_N)` subject to
  `x_{t+1} = f_t(x_t,u_t)`, `(x_t,u_t) ∈ Ω_t = D_t × U`, `x_0 ∈ X_0` and
  `x_N ∈ X_N`. `D_t` is a convex state enclosure. `f*` is the optimal value.
- **Calibration and bound [S].** For a family `S = (S_t)`, the stage
  residual is `ρ_t = L_t + S_{t+1}∘f_t − S_t`. The bound is
  `B(S) = inf_{X_0} S_0 + Σ_t inf_{Ω_t} ρ_t + inf_{X_N}(Φ − S_N) ≤ f*`.
- **Exact and failing stages.** Stage `t` is *exact* at `z̄_t = (x̄_t, ū_t)`
  if `z̄_t` minimizes `ρ_t` over `Ω_t`; otherwise it *fails*.
- **Euler data, control-affine, scalar control.** Dynamics
  `f_t = x + h(a(x) + b(x)u)` and stage cost `L_t = h(ℓ_0(x) + ℓ_1(x)u)`;
  control box `U = [u_−, u_+]` with width `Δ = u_+ − u_−`. Several controls
  with distinct switching times are handled component by component.
- **Continuous problem.** Dynamics `ẋ = g = a + bu`, `x(0)` fixed;
  Hamiltonian `H = ℓ_0 + ℓ_1 u + ψᵀg`; costate switching function
  `σ_0(t,x) = ℓ_1(x) + b(x)ᵀψ(t)`, and `σ(t) = σ_0(t, x*(t))`. A switch at
  time `τ` is *regular* if `σ(τ) = 0` and `σ̇(τ) ≠ 0`. Its **state gradient**
  is `w := −∇_x σ_0(τ, x*(τ))`.
- **Continuous residual of a calibration `S`.** `r = ℓ_0 + ℓ_1u + ∂_tS + S_xᵀg`,
  where `∂_tS` is the time derivative (not the discrete family `S_t`); its
  switching function is `σ_S = ℓ_1 + bᵀS_x`.

## 1. Window certificates

**Definition 1.1 (window certificate).** The data are: disjoint windows
`W_j = {a_j, …, b_j − 1}`; functions `S_t` at all stages that are not
interior to a window; for each window, a relaxation `R_j` (window
trajectories from `x_{a_j} ∈ X_{a_j}` that obey the dynamics, where any
constraints may be dropped); optional multipliers `ν_j` for constraints
`c_j = 0` (or `c_j ≤ 0` with `ν_j ≥ 0`) dualized inside the window, such as a
terminal row. The window value is

```
β_j = inf_{R_j} [ Σ_{W_j} L_t + S_{b_j}(x_{b_j}) − S_{a_j}(x_{a_j}) + ν_jᵀ c_j ].
```

A window containing `t = 0` uses `X_0` and has no entry term; a window ending
at `N` uses `Φ` instead of `S_N`. The bound is
`B = inf S_0 + Σ_{t outside windows} inf ρ_t + Σ_j β_j + inf(Φ − S_N)`.

**Proposition 1.2 (validity and exactness).** (1) `B ≤ f*` for all data.
(2) If some optimal trajectory attains every infimum, then `B = f*`; the
converse holds when `f*` is attained;
for a window this means its restriction attains `β_j` and satisfies
`ν_jᵀc_j = 0`.

*Proof.* Along a feasible trajectory the `S` terms telescope. Dualized
equality constraints vanish (inequality terms are ≤ 0), and each window
restriction lies in `R_j`. Each remaining term is bounded by its infimum;
equality holds iff every step is tight. □

This extends [S, Proposition 4.4] with explicit entry sets and relaxations.

**Proposition 1.3 (sign-certified windows).** Let `J(e,u)` be the window
objective with states eliminated, entry state `e` in a box `E`, controls in
`U^W`; let `G_t` enclose `∂J/∂u_t` over all of `E × U^W`; let
`D_+ = {t : G_t > 0}`, `D_− = {t : G_t < 0}`, and `F` the remaining ("free")
stages. Then
`inf J = inf { J(e,u) : u_t = u_− on D_+, u_t = u_+ on D_−, (e, u_F) ∈ E × U^F }`.

*Proof.* Move the coordinates in `D_±` to their vertices one at a time. Each
move follows a segment in the box along which the partial derivative has a
fixed sign, so `J` does not increase. □

For Euler data, `∂J/∂u_t = h(ℓ_1 + bᵀp_{t+1})`, where `p` is the window
adjoint with `p_b = ∇S_b`. The enclosures come from a forward reachable tube
and a backward interval adjoint. The optcdeg2 head block of [O] is the case
`E = {x_0}` with no free stages.

**Remark 1.4 (terminal rows).** Fixed terminal components such as `v_N = 0`
block the vertex argument directly. Dualizing the row with any `ν`
(Proposition 1.2) frees the end; the natural choice is the terminal costate,
0.5952523741 for optcdeg2. This removes the obstruction noted in
[O, Section 6.6]. It was not needed in the end (Section 5).

**Remark 1.5 (free sets).** If the tube has width `δ`, the enclosure of the
switching function is at least about `|∇_xσ_0|δ` wide; near a switch this
leaves `Θ(δ/(γh))` free stages, where `γ` is the switching-function slope. If
`b` and `ℓ_1` do not depend on the state and `S_b` is affine (optcdeg2), only
the adjoint is uncertain; that uncertainty grows backward from the window
end as `O((kh)²δ)`, so a switch at the window end costs `O(1)` free stages.
For the optcdeg2 tail entered through the first-wave box at `t = 47290`
(`y ∈ [−7.75, 20.76]`), a float estimate puts the uncertainty of `p_v` at
`0.58·w_y + 0.07`, which exceeds the switching-function slope over about 100
stages, so the window would need branching on the entry box.

**Remark 1.6 (cost).** One tube plus one adjoint sweep (`O(|W| n²)` interval
operations), plus a global problem in `n + |F|` variables.

## 2. Local stage analysis and the window law (discrete, rigorous)

At stage `t`, write `ρ = ρ_t`, `z̄ = (x̄, ū)` and `ω = u − ū`. Define the
stage switching function `σ_t = ∂_uρ(z̄)/h` and the state gradient of that
switching function `β_t = ∇_x∂_uρ(z̄)/h`. If `∇S_{t+1}(x̄_{t+1}) = p_{t+1}`,
then `σ_t = ℓ_1 + bᵀp_{t+1}` and
`β_t = ∇ℓ_1 + (∇b)ᵀp_{t+1} + (I + hg_x)ᵀ ∇²S_{t+1}(x̄_{t+1}) b`. For affine
`S`, `β_t → −w` at the switch; for quadratic `S` with Hessian `P`,
`β ≈ Pb − w`. "Tangency" means `P(τ)b = w`.

**Lemma 2.1 (local sufficient condition).** Let `ρ` be `C²` and assume
(a) `∇_xρ(z̄) = 0`; (b) `σ_t ω ≥ 0` for all `u ∈ U` (KKT sign condition);
(c) `∇²_xρ(x,u) ⪰ hμI` on `(B_r(x̄) ∩ D_t) × U`; (d) `∂²_uρ(x̄,u) ≥ h²κ` for
all `u ∈ U`; (e) `|β_t| ≤ B` and `|∇_x∂²_uρ(x̄,u)| ≤ h²C` for all `u ∈ U`.
Then on `(B_r(x̄) ∩ D_t) × U`:

```
ρ(x,u) − ρ(z̄) ≥ h|ω| [ |σ_t| + (hκ/2)|ω| − |ω|(B + hC|ω|/2)² / (2μ) ].
```

So `z̄` is a local minimum over the ball if either (i)
`|σ_t| ≥ Δ(B + hCΔ/2)²/(2μ) + (hΔ/2)·max(0, −κ)`, or (ii)
`hκ ≥ (B + hCΔ/2)²/μ` (covering fractional stages, where `σ_t = 0`).

*Proof.* (1) By (b) and (d), `ρ(x̄,u) − ρ(z̄) ≥ h|σ_t||ω| + (h²κ/2)ω²`.
(2) By (a) and (e), `|∇_xρ(x̄,u)| ≤ h|ω|B + (h²C/2)ω²`. (3) By (c), `ρ(·,u)` is
strongly convex with modulus `hμ`, so
`ρ(x,u) ≥ ρ(x̄,u) − |∇_xρ(x̄,u)|²/(2hμ)`. (4) Combine. □

**Lemma 2.2 (local necessary condition; [S, Proposition 4.2] for general
families).** Assume `z̄` minimizes `ρ` over `Ω_t`, `B_r(x̄) ⊂ D_t`, and
`ū = u_−`; let the secant switching function be
`Σ(x) = (ρ(x,u_+) − ρ(x,u_−))/(hΔ)`, with `g = ∇Σ(x̄)`; assume
`ρ(x̄+d, u_−) ≤ ρ(z̄) + (hΛ/2)|d|²` and
`Σ(x̄+d) ≤ Σ(x̄) + gᵀd + (M_s/2)|d|²` for `|d| ≤ r`, and
`s* = Δ|g|/(Λ + ΔM_s) ≤ r`. Then `Σ(x̄) ≥ Δ|g|²/(2(Λ + ΔM_s))`.

*Proof.* Exactness gives `0 ≤ [ρ(x̄+d, u_−) − ρ(z̄)] + hΔ·Σ(x̄+d)`. Take
`d = −s·g/|g|` and minimize the upper bound over `s`. □

For Euler data, `Σ(x̄) = σ_t + O(h)` and `g = β_t + O(h)`.

**Theorem 2.3 (window law at a regular switch).** Take a sequence `h → 0`,
with trajectories `z̄^h`, families `S^h`, and one switching time `τ`. Assume:

- **(W1)** Lemma 2.1 (a), (c)–(e) with `κ ≥ −κ_−`, the upper bounds of
  Lemma 2.2, and `B_r(x̄_t) ⊂ D_t` hold at every stage, with constants
  independent of `h`.
- **(W2)** Continuous limits `σ(·)`, `β(·)` exist with
  `|σ_t − σ(t_t)| + |β_t − β(t_t)| ≤ e_h → 0`; `σ` vanishes only at `τ`, and
  `γ_1|t−τ| ≤ |σ(t)| ≤ γ_2|t−τ|` for `|t − τ| ≤ δ_σ`.
- **(W3)** The KKT sign condition (b) holds at every stage.
- **(W4)** Far-region separation: `ρ_t(z) ≥ ρ_t(z̄_t)` whenever
  `|x − x̄_t| ≥ r`.
- **(W5)** Margin away from the switch: `|σ(t)| > Δ|β(t)|²/(2μ)` for
  `t ≠ τ`.

Then:

1. **Tangential case.** If `|β(t)| ≤ L|t−τ|` for `|t − τ| ≤ δ_σ` (shrink
   `δ_σ` if needed), every stage with `|t_t − τ| ≥ C_0(e_h + h)` is exact. At
   most `2C_0(e_h + h)/h + 1` stages fail, which is `O(1)` when `e_h = O(h)`.
2. **Non-tangential case.** If `β(τ) ≠ 0` and `s* ≤ r`, then for small `h`
   every stage with `|t_t − τ| ≤ δ_1 = min(δ_*, δ_β, δ_σ)` fails, where
   `δ_* = Δ|β(τ)|²/(4γ_2(Λ + ΔM_s))` and `|β(t)|² > |β(τ)|²/2` for
   `|t − τ| ≤ δ_β`: `Θ(1/h)` stages. (Corrected after verification: the
   original statement used `δ_*` alone, which ignores how fast `β` varies
   and where the upper bound `|σ| ≤ γ_2|t−τ|` of (W2) holds.)

*Proof.* (1) Let `s = |t_t − τ|`. Then `|σ_t| ≥ γ_1 s − e_h` and
`|β_t| ≤ Ls + e_h`. For `s ≤ min(δ_σ, γ_1μ/(4ΔL²))`, condition (i) of
Lemma 2.1 follows from `(3γ_1/4)s ≥ e_h + Δ(e_h + hCΔ/2)²/μ + hΔκ_−/2`,
which holds for `s ≥ C_0(e_h + h)`. Farther from `τ`, (W5), continuity and
compactness give a uniform margin `m_0 > 0`, which absorbs the `O(e_h + h)`
perturbations. Lemma 2.1 covers the ball; (W4) covers the rest. (2) By
Lemma 2.2, exactness needs `Σ_t ≥ Δ|g_t|²/(2(Λ + ΔM_s))`. For
`|t_t − τ| ≤ δ_1` we have `|σ(t_t)| ≤ γ_2 s` (because `δ_1 ≤ δ_σ`) and
`γ_2 s ≤ Δ|β(τ)|²/(4(Λ+ΔM_s)) < Δ|β(t)|²/(2(Λ+ΔM_s))` with a margin, and the
`O(h + e_h)` differences between `(Σ_t, g_t)` and `(σ(t_t), β(t_t))` do not
close it for small `h`. □

**Corollary 2.4 (costate calibrations).** For affine families,
`β(τ) = −w`. If `w ≠ 0`, the failing window has fixed duration, `Θ(1/h)`
stages. [Rv, F18] adds the required assumptions: uniform convergence of
states and costates near the switch, interior states, and uniqueness of the
slopes if all affine calibrations are to be covered. If `w = 0`, affine
families are tangential (e.g. when `b` and `ℓ_1` do not depend on the state,
or when `n = 1` and `ℓ_1 ≡ 0`, since then `ψ(τ) = 0`); they can then fail
only where the stage-wise Mangasarian condition (SGM) fails on whole arcs.
When `b` and `ℓ_1` do not depend on the state, `β ≡ 0` and nothing else is
needed. In the case `n = 1`, `ℓ_1 ≡ 0` with state-dependent `b`, the claim
also needs the margin (W5) away from `τ`, because
`β(t) = b'(x*(t))ψ(t) ≠ 0` for `t ≠ τ` in general. optcdeg2 is of the first
kind (`b = e_v`, `ℓ_1 = 0`).

**Remark 2.5 (units and rates; corrected after verification).** The
failing window has fixed *duration* for non-tangential families and
`O(1 + e_h/h)` *stages* for tangential ones. For linear problems,
Alt–Baier–Lempio–Gerdts (Optimization 62 (2013) 9–32) give O(h) adjoints and
O(h) controls in L1 under a slope condition on the switching function. For
nonlinear control-affine problems, Alt–Felgenhauer–Seydenschwanz (COAP 69(3)
(2018) 825–856, DOI 10.1007/s10589-017-9969-7) treat Mayer costs with control
bounds only and prove Hölder-type estimates under a growth condition and a
better order under a stronger condition; whether they provide the O(h) rate
in L∞ for discrete states and costates at KKT points that Theorem 2.3(1)
needs is unverified here (full text not accessed). With a Hölder rate
`h^{1/2}`, Theorem 2.3(1) gives `O(h^{-1/2})` failing stages, not O(1).
Terminal state constraints such as optcdeg2's `v_N = 0` appear to be outside
that class. (An earlier version cited a DOI and PDF that are in fact
Scarinci–Veliov, COAP 69(2) (2018) 403–422, on linear-quadratic problems.) The
optcdeg2 certificate does not depend on any rate.
With only uniform convergence, Theorem 2.3(1) gives `o(1/h)` failing stages,
so the rate matters here, unlike in the smooth transfer theorem, where [Rv]
found uniform convergence sufficient.

## 3. Tangential calibrations in continuous time

**Proposition 3.1 (every calibration that is `C²` in the state and exact on
the trajectory is tangential).** Assume, on a neighbourhood of
`(τ, x*(τ))`:

- `S`, `S_x` and `S_xx` are continuous in `(t,x)`;
- the time derivative `∂_tS` exists for `t ≠ τ` and is `C¹` in `x`, and
  `∂_tS` and `∇_x∂_tS` extend continuously up to `t = τ` from each side
  (one-sided time regularity, made explicit after verification). So `r` and
  `∇_x r` have one-sided limits `r^±(τ,·,u)` and `∇_x r^±(τ,·,u)`, which may
  differ;
- `r(t,x,u) ≥ 0` for all `u ∈ U` and all `(t,x)` in the neighbourhood with
  `t ≠ τ`, and `r = 0` along `(x*, u*)` on both sides of `τ` (exactness on
  the trajectory, [Rv, F10]);
- `x*(τ)` is interior, `Δ > 0`, and `ψ(t) := S_x(t, x*(t))` is the costate
  used to define `w`.

Then `S_xx(τ, x*(τ))·b = w`, i.e. `∇_xσ_S(τ, x*(τ)) = 0`.

*Proof.* Each side of `τ` is handled separately, as in [E, Theorem 1,
step 2]. Take `t > τ`; the case `t < τ` is the same.
(1) `r` is affine in `u` with slope `σ_S = ℓ_1 + bᵀS_x`, and
`σ_S(t, x*(t)) = σ(t)`. So exactness gives
`r(t, x*(t), u) = σ(t)(u − u*(t))`. `σ` is continuous because `S_x` is, and
`σ(τ) = 0` because `r ≥ 0` forces `σ(t)(u − u*(t)) ≥ 0` for all `u` while
`u*` changes vertex at `τ`. Letting `t ↓ τ` gives `r^+(τ, x*(τ), u) = 0` for
every `u ∈ U`.
(2) `r^+(τ,·,u) ≥ 0` near the interior point `x*(τ)` (as a limit of
`r ≥ 0`) and vanishes there, so `∇_x r^+(τ, x*(τ), u) = 0` for every `u`.
(3) `∇_x r^+(τ, x, u)` is affine in `u` with slope `∇_xσ_S(τ, x)`. The slope
contains `S_x` and `S_xx` but not `∂_tS`, so it is the same from both sides.
Subtracting the two vertices gives `Δ∇_xσ_S(τ, x*(τ)) = 0`.
(4) Finally, `∇_xσ_S = S_xx b + ∇ℓ_1 + b_xᵀψ = S_xx b − w`. □

Strictness is not used. The field value function escapes this result only
because its Hessian jumps across the switching surface.

*Robustness (verifier).* Time-discontinuous `S` gives no escape (validity
forces a jump `j ≥ 0` minimized at `x*(τ)`, each one-sided family is
tangential, so `j_xx b = 0`); for residuals not affine in `u` the two
one-sided limits give secant tangency; with several controls tangency holds
in the jump direction `[u]`; interiority of `x*(τ)` in the region where
`r ≥ 0` is required is essential (on a reachable-set boundary the proof
fails and non-tangential families lose less).

*Relation to Osmolovskii–Maurer (worked out by the verifier).* In the
Q-transformation of Maurer–Osmolovskii (2003), following
Osmolovskii–Lempio (2002), the jump condition at a switch involves
`q_{k+} = ([ẋ]^k)ᵀQ^{k+} − [ψ̇]^k`; for control-affine dynamics
`q_{k+} = [u]^k (Qb − w)ᵀ = [u]^k βᵀ`. So tangency is exactly the case in which
their Riccati solution does not jump; their jumping solutions certify the
second variation with switching-time variations but, by Proposition 3.1,
cannot be Hessians of a pointwise `C²` verification function.

**Proposition 3.2 (sufficient second-order condition: a Riccati inequality
with a singular coefficient).** Take the quadratic calibration
`S = V*(t) + ψᵀd + ½ dᵀP(t)d`, `d = x − x*(t)`, where `V*` is the cost-to-go
along `x*` and `P` is continuous and piecewise `C¹`. Then
`r(t, x*, u) = σ(t)·ω`, `∇_x r(t, x*, u) = β(t)·ω` with `β = Pb − w_t` and
`w_t := −∇_xσ_0(t, x*(t))`, and `∇²_x r = M(t,u) + O(|d|)` with
`M(t,u) = Ṗ + g_x(u)ᵀP + P g_x(u) + H_xx(u)`. If, for all `t` and all
`u ∈ U`,

```
M(t,u) − 2εI − (Δ/(2|σ(t)|)) β βᵀ ⪰ 0,
```

then `r(t, x*+d, u) ≥ (ε − C|d|)|d|²`.

*Proof.* Expand `r` to second order in `d`. The Schur form gives
`½dᵀMd ≥ ε|d|² + Δ(βᵀd)²/(4|σ|)`. Minimizing over `x = |βᵀd|`,
`|ω||σ| − |ω|x + Δx²/(4|σ|) ≥ |ω||σ|(1 − |ω|/Δ) ≥ 0` for `|ω| ≤ Δ`. □

This is the Riccati inequality of the accessory LQ problem with state weight
`Q − 2ε`, cross term `−w_t`, and control weight `2|σ|/Δ` (the quadratic
minorant of the first-order bang-bang cost `|σ||ω|` on `|ω| ≤ Δ`). The
coefficient `Δ/(2|σ|) ~ 1/|t−τ|` is not integrable at the switch, so any
bounded solution must satisfy `β → 0` there: the condition forces tangency.
More precisely, for continuous bounded `P` it forces only
`∫|β|²/|σ| < ∞` (so `β → 0`, possibly logarithmically), not
`|β| = O(|t−τ|)`.

**Remark 3.3 (existence; scalar sketch, answered in [E]).** Take the maximal
backward solution `P̂` of the inequality of Proposition 3.2, with
`P(T) = Φ_xx − 2ε` on the free terminal components and no constraint on
fixed ones; by comparison, every solution satisfies `P ≤ P̂`. Scalar case,
near `τ+` (if `P̂` is still finite there): `β̂` either tends to 0 like
`1/log(1/s)`, or `P̂` blows up in a layer just after `τ`, before the backward
integration reaches `τ`. (The first version called this blow-up "a conjugate
point"; that label is wrong, see below.) The logarithmic rate is too slow (it
would give an `o(1)`-duration window but not `O(h)`), but one can take `β = κs` on
`(0, s_1]` with `κs_1 ≤ β̂(s_1)` and continue with equality; that gives a
linear-rate tangential solution, and comparison preserves the terminal
condition. *Gap (verifier):* the earlier claim that before `τ` "there is no
constraint" is true only at the endpoint `t = 0`. The inequality must still
be solvable backward on `[0, τ)`, where the singular coefficient reappears;
backward comparison makes `P` at most the equality solution, which can blow
up to −∞ (a conjugate point of the relaxed LQ problem with control weight
`2|σ|/Δ`, not of the optimal control problem; [E, Section 4]).
Osmolovskii–Maurer's Theorem 4.4 (fixed `x_0`, one switch) needs
nothing before `τ` because critical variations vanish there, but a
pointwise verification function does. The first version conjectured that,
for `n ≥ 2`, a tangential solution exists if and only if `P̂` is bounded
("no conjugate point").

*Answer ([E]; one regular switch, fixed `x_0`, free endpoint, `x*`
interior).* Let `Q` solve the Lyapunov equation of the last arc with
`Q(T) = Φ_xx`, and put `β_L = Q(τ+)b − w` and `η_L = bᵀβ_L`.

- *Local formulation* (the singular condition imposed only near `τ`), any
  `n`. A strict tangential quadratic calibration with linear-rate tangency
  exists if and only if `η_L > 0` ([E, Theorem 2 and Corollary 3]). If
  `η_L < 0`, no exact calibration that is `C³` in `(t,x)`, with bounded
  derivatives up to order 3, exists on a uniform tube after the switch,
  strict or not ([E, Theorem 1]; its proof is Proposition 3.1 applied to
  the right limit plus Lyapunov comparison). Before `τ − δ_0` only the
  non-singular condition remains, which is linear and always solvable
  ([E, Theorem 2, step 3]). In this formulation the maximal solution is
  bounded exactly when a tangential calibration exists, so the conjecture
  holds in that sense.
- *"No conjugate point" is the wrong reading, also for the scalar sketch.*
  The bang-bang second-order sufficient condition is `D + Δ²η_L > 0` with
  `D = |σ̇(τ)|Δ` ([E, Proposition 6]; it agrees with the
  Osmolovskii–Maurer quadratic form). If `−D/Δ² < η_L < 0`, the extremal is
  a strict strong local minimum by the cited sufficiency theorems, yet `P̂`
  blows up after `τ` and no such calibration exists
  ([E, Corollary 7]; Example B, `n = 2`: `η_L = −0.429`, `D = 3.066`,
  `F''(τ) = 1.350`). The argument does not use `n ≥ 2`, so the scalar
  sketch has the same gap: `η_L < 0` forces the blow-up even when the SSC
  holds.
- *In the global form, the sign of `η_L` does not decide.* The sketch above
  uses the global form (the inequality of Proposition 3.2 on the whole
  horizon), so the singular term also acts on the last arc. There `P̂ ⪯ Q`,
  and what matters near `τ+` is `η̂ = bᵀ(P̂b − w)`, which is at most
  `bᵀ(Qb − w) → η_L` ([E, Theorem 8]). So `η_L < 0` still forces the
  blow-up, but `P̂` can also blow up when `η_L > 0`, at a conjugate point of
  the relaxed LQ problem that need not lie near `τ` ([E, Summary item 3]). Scalar example (found by the round-2
  confirmation; float, not certified; `revision3_checks.py`): `ẋ = u`,
  `|u| ≤ 1`, cost `∫x²/2 dt − 0.9x(T)²/2 + 0.399x(T)`, `x(0) = 1.01`,
  `u = −1` then `u = +1` with the switch at `τ = 1`, `T = 2`. In exact
  arithmetic, `σ̇(τ) = −0.01`, `D = 0.02`, `η_L = 0.1` and `F''(τ) = 0.42`,
  so the SSC holds and local calibrations exist ([E, Theorem 2]). Yet the
  global-form `P̂` (`Ṗ = −1 + P²/|σ|`, `P(T) = −0.9`) tends to `−∞` at
  `t = 1.587`, 0.587 time units after `τ` (at `t = 1.596` for `ε = 0.01`).
  The sign of `η_L` decides only in the local formulation.
- *Before `τ`, in the global form.* With the singular term on the whole
  horizon (the form of Proposition 3.2; (H3) of Theorem 4.1 implies it with
  `ε = 0` for quadratic `S`, and for any `S` when `b` is constant and `ℓ_1`
  affine, [E, Lemma 14]), the obstruction before `τ` noted above does occur. In
  [E, Example C], `η_L = +0.202`, so local calibrations exist, but every
  global-form calibration lies below a solution that tends to `−∞` at
  `t = 0.352`, before `τ` (`ε = 0`; [E, Proposition 15]; the blow-up is a
  floating-point result, not a certificate).

So the scalar sketch is complete near `τ+`: it states which behaviours can
occur there, and gives the linear-rate construction when `β̂ → 0`. In the
local formulation the sign of `η_L` decides which one occurs, and before `τ`
the sketch is completed by [E, Theorem 2, step 3]. In the global form,
existence can fail on either side of `τ` even when `η_L > 0`: after `τ` in
the scalar example above, before `τ` in [E, Example C]. The maximal
tangential calibration is the Osmolovskii–Maurer Riccati test with rank-one
jump in which `D(H)` is set to zero ([E, Section 3]; see also the paragraph
after Proposition 3.1).

**Remark 3.4 (field value function; heuristic).** The value function `V` of
the field of extremals has residual `r = |σ_V||u − u_f|`, which vanishes on
every field trajectory: it is not strict, and [Rv] shows that non-strict
fields lose `Θ(h)`. Its switching surface is transversal, so it is not
tangential. Tilting keeps `β(τ) ≠ 0` in general.

**Remark 3.5 (corrections from [Rv] built in).** The trajectory is
admissible and the residual vanishes on it; `U` is compact (`Δ` appears in
every bound); strictness in the state is needed (`μ > 0`; on optcdeg2,
margin 0 loses 1.07e-4); rate versus uniform convergence: see Remark 2.5; no
exponential tilt is used; the margins are explicit.

## 4. Transfer to transcriptions

**Theorem 4.1 (transfer with O(1)-stage switch windows).** Assume:

- **(H1)** `U = [u_−, u_+]`; `D` is compact and convex and encloses every
  feasible state; the data are `C³` and `Φ` is `C²`.
- **(H2)** `(x*, u*)` is admissible and bang-bang, with one regular switch
  at `τ`.
- **(H3)** `S` is `C⁴` in `x`, with `∇³S` Lipschitz in `t`, on a tube around
  `x*`; `r = 0` on the trajectory and `S_x(t, x*(t)) = ψ(t)`; `∇²_x r ⪰ μI`
  on the tube for all `u ∈ U`; tangency `β(τ) = 0`; the margin
  `|σ| > Δ|β|²/(2μ)` for `t ≠ τ`.
- **(H4)** Discrete KKT points `(x^h, u^h, p^h)` satisfy the KKT sign
  conditions, with
  `e_h = max_t(|x^h_t − x*(t_t)| + |p^h_{t+1} − ψ(t_t)|) → 0`.
- **(H5)** Far-region separation (W4) holds for the transferred family.

Set `S^h_t = S(t_t, ·) + a_tᵀx`, with `a_t = p^h_t − S_x(t_t, x^h_t)`. Then
every stage with `|t_t − τ| ≥ C(e_h + h)` is exact. If `e_h = O(h)`, the
discrete trajectory attains the infimum of the resulting `O(1)`-stage
switch window (window exactness, an assumption — see "uniform conditioning
of switch windows" in Section 6), **and** the terminal term is exact
(`Φ − S^h_N` attains its infimum over `X_N` at `x^h_N`; the infimum may be
taken over `X_N ∩ D`, since `D` encloses every feasible state; for LQ data
(quadratic `Φ` and `S`) and a free endpoint, where `p^h_N = ∇Φ(x^h_N)`, this
follows from `P(T) ⪯ Φ_xx` with `P(T) = S_xx(T, ·)`), then `B = f*`. (Root correction, 2026-09-30:
the terminal condition was missing from the statement; by Proposition 1.2
the bound includes `inf(Φ − S_N)`, so it is needed; found in
`window-exactness.md`, Section 8. Corrected after
verification: window exactness is assumed, not proved. Also, the time
derivative `∂_tS` of the continuous `S` must be `C²` in `x` on the tube, with
`∂_tS`, `∇_x∂_tS` and `∇²_x∂_tS` continuous in `(t,x)` for `t < τ` and for
`t > τ` and extending continuously up to `t = τ` from each side, and `S_xx`
must be Lipschitz in `t`; the list was completed in Section 9.3. These
conditions give the hypotheses of Proposition 3.1 except continuity of `S`
itself at `τ`, which its proof does not use (`S_x` is continuous there
because `S_x(t, x*(t)) = ψ(t)` and `S_xx` is jointly continuous; `S` can jump
at `τ` only by a constant), and step (c)
uses the time continuity of `∇²_x∂_tS`. Tangency in (H3) is then redundant,
since convexity plus the margin give `r ≥ 0` near the trajectory and
Proposition 3.1 forces it.)

*Proof.* (a) The discrete adjoint gives `∇_xρ_t(z^h_t) = p^h_t − p^h_t = 0`.
(b) `∂_uρ_t(z^h_t) = h·σ^h_t`, and the KKT sign condition holds.
(c) `∇²_xρ_t = h·[r_xx + o(1)] ⪰ hμ'I` for any fixed `μ' < μ` and small `h`
(root correction, 2026-09-30: the earlier text used `hμ/2`, which would need
(W5) with `μ/2`, i.e. `|σ| > Δ|β|²/μ`, twice the (H3) threshold; (H3)'s
strict margin and compactness away from `τ`, and near `τ` the bound
`|β(t)| ≤ L|t − τ|` (tangency plus the Lipschitz regularity of `S_xx`)
against `|σ| ≥ γ_1|t − τ|`, give (W5) with some `μ' < μ`, so no conclusion
changes; found in `window-exactness.md`, Section 0.3): the difference quotient
of `S_xx` in `t` tends to `∇²_x∂_tS` uniformly on each side of `τ` (at the
stage containing `τ` it is an average of the two sides, each `⪰ μI`).
(e) `β_t = β(t_t) + O(h + e_h)` and `σ^h_t = σ(t_t) + O(e_h)`. Theorem 2.3(1)
then applies with `μ'` in place of `μ` and `e_h + h` in place of `e_h`. □

*Scope ([E, Section 4.1]).* For quadratic `S`, and for every `S` when `b` is
constant and `ℓ_1` affine, (H3) implies the global-form inequality of
Proposition 3.2 with `ε = 0` at every `t ≠ τ` ([E, Lemma 14]). That form can
fail when local calibrations exist: in [E, Example C], `η_L = +0.202`, yet no
`S` satisfies (H3) together with an exact terminal term, because every
global-form calibration lies below a solution that tends to `−∞` before `τ`
([E, Proposition 15]; the blow-up is a floating-point result). The scalar
example of Remark 3.3 (constant `b`, `ℓ_1 = 0`, `η_L = 0.1`) fails in the
same way after `τ`: every global-form calibration with `P(T) ≤ Φ_xx` lies
below `P̂`, which tends to `−∞` at `t = 1.587` (floating point). So the local
existence result of Remark 3.3 does not feed into this theorem; a transfer
theorem for local calibrations is open.

## 5. optcdeg2

**5.1 Structure.** `h = 4e-4` and `N = 50000`. Dynamics `y' = v`,
`v' = u − 0.02y − 0.2v²`; cost `(h/2)Σy²`; data `y_0 = 10`, `v_0 = v_N = 0`,
`v ≥ −1`, `|u| ≤ 0.2`. The control is `−0.2`, then `+0.2`, then `−0.2`, with
fractional controls at stages 3091 and 47290.

**5.2 Diagnosis.** `b = e_v` and `ℓ_1 = 0`, so `w = 0`: the affine
calibration is already tangential. It fails because `H_vv = −0.4ψ_v < 0` on
both `u = −0.2` arcs: an SGM failure on whole arcs, not a switch effect. In
float screening its loss is 0.6258 in total: 0.6197 on the head and 0.00604
on the tail.

**5.3 Calibration.**
`S_t(y,v) = py_t·y + pv_t·v + (q_t/2)(v − v_t)²`.

- `(py, pv)` are the discrete costates of a refined KKT point. The
  refinement moved `s1` by 4e-5 steps; its own costate computation then gave
  `p_v(3092) = 6.2e-12` (`logs/refine_primal.log`), and the costates
  recomputed from the refined controls, which are the certificate data, give
  `p_v(3092) = 7.6e-12` (`logs/optcdeg2_qcal_data.npz`). Before the
  refinement, `p_v(3092) = −1.2e-3` and the stage-3091 loss was 7.3e-8.
- **Head schedule:** `q_{s1} = 0`, then backward
  `q_t = q_{t+1}(1 − 0.4h v_t)² − 0.4h pv_{t+1} − 2κ_H h`.
- **Middle arc:** `q = 0`.
- **Tail schedule:** `q_{s2+1} = 0`, then forward
  `q_{t+1} = (q_t + 0.4h pv_{t+1} + 2κ_T h)/(1 − 0.4h v_t)²`.
- Margins: `κ_H = 1`, `κ_T = 0.05`; endpoints `q_0 = −34.10`, `q_N = 0.286`.
- The Hessian is `P = diag(0, q)`, so `β_t ∝ (0, q_{t+1})`; it vanishes
  exactly at both switching stages.

**5.4 Rigorous evaluation.** The minimum over free `y` is exact (`ρ_t` is a
convex quadratic in `y`). What remains is a polynomial
`ρ̃(v_t + d, u_t + D) = Σ c_jk d^j D^k` with `j ≤ 4`, `k ≤ 2`, whose
coefficients are enclosed with ivnp; the constant and linear coefficients are
re-associated (e.g. `vs(P1v − P0v) + …`) so that large costate terms cancel
before rounding. `d` ranges over the first-wave interval `V_t`, covered by 162 geometric
cells (the stored `V_t` bounds are round-to-nearest, up to 0.4999 ulp inward
at 34424 stages; the certificate widens every stored bound by one ulp, which
the verifier confirmed covers a rigorous recomputation at every stage); the minimum over
`D` is exact (quadratic in `D`); cells with a lower bound below −1e-16 are
bisected. Stage 0 is computed exactly with `y_1 = 10` and
`v_1 = h(u − 0.2)`. The terminal term is `−py_N²/(2h)` with `v_N = 0` in
`X_N`. The total is summed with `math.fsum` and rounded down one ulp. Fixed
decimal constants are enclosed by outward rounding, and the control bound
`.2` by `[dn(−0.2), up(0.2)]`.

**5.5 Results** (`logs/optcdeg2_qcal_certify.json`):

| quantity | value |
|---|---|
| certified bound | **293.8760750958728** |
| rigorous upper bound (verifier, `v_primal.py`) | 293.87607509587509328: a feasible point with controls ±1/5, the stored `u_3091`, and `u_47290` bracketed in interval arithmetic so that `v_N = 0` holds exactly for some value in the bracket |
| author's primal point (`optcdeg2_kkt_primal_check.json`) | 293.87607509588105; rows 8.88e-16; bounds 0 (same 1.1e-17 formal caveat as [V]); not exactly feasible, 6.0e-12 above the rigorous upper bound |
| gap | **2.3e-12** (7.8e-15 relative) to the rigorous upper bound |
| exact value of the same certificate (verifier) | 293.876075095875092379… (truncated); 9.0e-16 below the rigorous upper bound |
| stage-0 term | [1014.9964727128655, 1014.9964727128666] |
| terminal term | −1.8598627153e-4 |
| `Σ(c00_hi − LB)` | 3.2e-12 (head 3.9e-13, middle 2.84e-12, tail 2.6e-15) |
| worst stage | 3091, loss 1.0e-15 |
| cells refined | 1.33e6 |
| run time | 6.6 s |

The gap is rounding-level. The author's primal point satisfies the rows only
to 8.9e-16. The verifier bounded the effect of repairing the rows: its
rigorously feasible point (see the table) is 6.0e-12 lower, so repairing
lowers the value (row violations of about 1e-16 times costates of about
100). An
earlier version measured the gap against the float point (8.3e-12; the exact
difference of the two doubles is 8.24e-12) and against the first-wave float
point 293.876075095886 (1.3e-11), whose rows also hold only to 8.9e-16.
Earlier runs of the same script: 293.87607508929676 (unconditioned
coefficients, 561 s), then 293.8760750919655 (sequential summation lost
3.9e-9).

**5.6 Checks** (`optcdeg2_qcal_recheck.py`). Exact rational arithmetic on
330 stages (near both switches, at both ends, and 150 random stages): the
residual evaluated from its definition, with an exact minimum over `y`, and
the 15 coefficients recovered by exact interpolation — 0 containment
violations (widest coefficient interval 1.3e-13) and 0 violations in
pointwise checks of the cell minima (minimum margin 6.8e-20). Float
sampling over all stages: minimum of `ρ − LB` is −1.8e-13 (float rounding on
terms of size about 1e3). This is the author's own recheck, not an
independent verification.

**5.7 Window law on the optcdeg2 family** (float screening; a stage fails if
its loss exceeds 1e-12). Families: **A** affine; **B** tangential; **C** B
plus a constant offset `Q̄ = 0.05` after the first switch
(non-tangential); **D** B with the tail profile shifted 5 stages earlier (an
`O(h)` tangency defect).

| N | A failing stages (duration) | B failing stages (loss) | C failing stages (duration) | D failing stages (loss) |
|---|---|---|---|---|
| 6250 | 723 (2.314) | 0 (4e-14) | 15 (0.048) | 1 (3.6e-9) |
| 12500 | 1447 (2.315) | 0 | 30 (0.048) | 1 (4.8e-10) |
| 25000 | 2898 (2.318) | 0 | 59 (0.047) | 1 (3.4e-11) |
| 50000 | 5799 (2.320) | 0 | 118 (0.047) | 1 (5.3e-12) |
| 100000 | 11599 (2.320) | 0 (7e-13) | 236 (0.047) | 0 (below threshold) |

Family A is not a window-law test: optcdeg2 has `w = 0`, so family A is
tangential, and its failing stages (2.32 time units, the whole head and tail
`u = −0.2` arcs) are the SGM failure of Section 5.2. The window law with
`w ≠ 0` was tested on the verifier's toy (Summary). Family C fails on
`[−105, +12]` stages around `s2` at `N = 50000` (predicted after-switch side
0.0045 time units; observed 0.0048). Family D's single-stage loss scales like
`h³`.

**5.8 Margin sensitivity** (`N = 50000`):

| `(κ_H, κ_T)` | total loss |
|---|---|
| (0, 0) | 1.07e-4 |
| (0.02, 0.002) | 1.85e-5 |
| (0.1, 0.01) | 1.4e-7 |
| (1, 0.05) | 1.2e-13 |

Strictness is needed.

## 6. Capability, costs, and what remains open

**What a certificate needs.** A discrete KKT point that is in fact the
global optimum; a costate sweep plus a curvature schedule (a
Riccati/Lyapunov sweep costing `O(N n³)`); state enclosures (an `O(N)`
interval propagation); `N` fixed-dimension stage checks (with shells
probably `O(log(1/h))` boxes per stage, a sketch; for optcdeg2 a 1-D check
after exact eliminations); and, for each switch, one window problem in
`n + m(2W+1)` variables, only when stage checks fail there.

**Open.** A transfer theorem for local calibrations: their existence for any
`n` is settled by the sign of `η_L` ([E, Corollary 3]; Remark 3.3), but
(H3) of Theorem 4.1 implies the global form (for quadratic `S`, or `b`
constant and `ℓ_1` affine), which can fail when `η_L > 0`
([E, Section 4.1 and Section 8]; Remark 3.3); (H5) as an a-priori property (reduced to a
continuous far-region condition in [E, Proposition 12], automatic for
LQ-structured data with global-form calibrations, [E, Proposition 13]);
uniform conditioning of nonempty switch windows (answered by
`window-exactness.md`, see below); the discrete rate
`e_h = O(h)` for nonlinear problems (literature-dependent); singular arcs
(worked out in `singular-arcs.md`, see below); state constraints and
boundary arcs; simultaneous switches of several controls.

*Update (root, 2026-09-30).* Two of these items were followed up and
reviewed (an initial review and three confirmation rounds each):

- **Window exactness** (`window-exactness.md`). Whether it holds is decided
  by the sign of the switch self-curvature `κ_τ = b(x*(τ))ᵀw`, which every
  `C²` calibration exact on the trajectory shares. Under the hypotheses of
  Theorem 4.1 (with its exact terminal term) and `b(x*(τ)) ≠ 0`: `κ_τ > 0`
  gives `B = f*` with no window (and only `e_h ≤ c_*√h` for a specific
  small `c_*`); `κ_τ = 0` gives `B = f*` with one window of `O(1)` stages
  (with `e_h = O(h)`); `κ_τ < 0` is a counterexample on grids whose KKT
  point has a fractional stage (a positive fraction of grids by a heuristic
  phase model): for the transferred calibration, every window of `o(1/h)`
  stages falls short by order `h²`, and a repair needs a window of fixed
  duration. For LQ data the negative result extends to all quadratic
  families with the discrete costate slopes that are exact over `Rⁿ × U` at
  every stage after the window and at the terminal, for a window exit
  `o(1/h)` stages after the switch (families exact only over the state
  boxes, which is what a certificate needs, are not covered).
- **Singular arcs** (`singular-arcs.md`). A `C²` calibration exact on a
  singular arc is tangential along the whole arc (`PB = W`); with several
  controls this forces `BᵀW` to be symmetric, which is exactly Goh's
  condition (empty for a scalar control). Its residual curvature equals
  Kelley's coefficient, so exact calibrations imply Kelley's condition. For
  Euler, the sign of `bᵀw` decides whether tangential families certify
  fractional stages (`bᵀw > 0`, given `e_h = o(√h)` near junctions) or
  whether, for families with bounded Hessians and `K_t ⪯ hΛI`, every
  fractional stage fails and a smooth KKT point with a run of fractional
  stages is a saddle (`bᵀw < 0`); `bᵀw` depends on the formulation and the
  scheme, and the calibration-independent quantity is an accessory symbol
  `f(π)`. On catmix this explains the chattering of the COPS transcription
  (the quantitative agreements are heuristic, float checks); no rigorous
  catmix certificate was built.

**Novelty.** The window-law dichotomy, the tangency result (Proposition 3.1)
and the singular-coefficient Riccati inequality (control weight `2|σ|/Δ`)
were not found stated; all are elementary, and Proposition 3.1 is the
continuous-time twin of [S, Prop. 4.1]. Related prior work:
Osmolovskii–Lempio (2002) and Maurer–Osmolovskii (2003), Riccati equations
with rank-one jumps (tangency is their no-jump case); Maurer–Pickenhain
(1995), quadratic verification functions via Riccati equations (full entries
in Sources). Searches were limited.

## 7. Status table

| item | status |
|---|---|
| Definition 1.1, Propositions 1.2 and 1.3 | proved |
| Remarks 1.4–1.6 | remarks; the 1.5 estimate is float only |
| Lemmas 2.1 and 2.2, Theorem 2.3 | proved under (W1)–(W5); part (2) with the corrected radius `δ_1 = min(δ_*, δ_β, δ_σ)` |
| Corollary 2.4 | proved, with the [Rv] assumptions; the `n = 1`, `ℓ_1 ≡ 0`, state-dependent `b` case also needs (W5) |
| Proposition 3.1 | proved, under one-sided regularity of `∂_tS`, each side handled separately (proof revised in Section 9.2; re-derived step by step by the round-2 confirmation) |
| Proposition 3.2 | proved (sufficiency); tangency forcing is remark-level |
| Remark 3.3 | scalar sketch complete near `τ+`; the `n ≥ 2` question is answered in [E]: local formulation, exists iff `η_L > 0` (any `n`); "no conjugate point" reading refuted (Example B); `η_L < 0` forces the blow-up in both forms; in the global form `P̂` can also blow up when `η_L > 0`, before `τ` (Example C) or after it (scalar example; both float blow-ups) |
| Remark 3.4 | heuristic |
| Theorem 4.1 | proved given (H1)–(H5) and the time regularity of `∂_tS` stated after the theorem (completed in Section 9.3; step (c) uses `μ' < μ`, root correction of 2026-09-30); `B = f*` additionally assumes window exactness and an exact terminal term (the latter missing from the original statement; root correction after `window-exactness.md` Section 8); window exactness is proved there for `κ_τ ≥ 0` (with `b(x*(τ)) ≠ 0` and rate hypotheses on `e_h`) and refuted for `κ_τ < 0` on grids with a fractional stage, within transferred calibrations; for quadratic `S` (or `b` constant, `ℓ_1` affine) (H3) implies the global form, so local calibrations are not covered ([E, Section 4.1]) |
| optcdeg2 bound | certified in interval arithmetic; gap 2.3e-12 to a rigorous upper bound; independently verified in exact rational arithmetic (optimum bracketed within 9.0e-16) |
| Section 5.7 window law | float screening; family A is the SGM failure of Section 5.2, not a window-law test |
| singular arcs | in `singular-arcs.md`: exact `C²` calibrations are tangential on the arc, which forces Goh's condition, and imply Kelley's (proved); Euler sign criterion proved under stated assumptions (the `bᵀw > 0` half assumes `e_h = o(√h)` near junctions; the `bᵀw < 0` half assumes bounded Hessians and `K_t ⪯ hΛI`); `bᵀw` depends on the formulation; a global catmix calibration and a rigorous catmix certificate open |
| state constraints | open |

## 8. Commands run and files

All runs used `OMP_NUM_THREADS=1`, from `theory-bangbang/`; only targeted
checks, no project-wide verification, no CI inspection.

1. `python3 optcdeg2_explore.py` → `logs/explore1.log`
2. `python3 optcdeg2_refine_primal.py` → `logs/refine_primal.log`,
   `logs/optcdeg2_kkt_u.npy`, `logs/optcdeg2_kkt_primal.json`
3. `UFILE=logs/optcdeg2_kkt_u.npy python3 optcdeg2_explore.py` →
   `logs/explore2.log`
4. `python3 optcdeg2_qcal_certify.py 1.0 0.05`, three runs with edits between
   them; the final one is `logs/qcal_certify_run3.log`. Outputs:
   `logs/optcdeg2_qcal_certify.json`, `logs/optcdeg2_qcal_stage_lb.npy`,
   `logs/optcdeg2_qcal_data.npz`.
5. `python3 optcdeg2_qcal_recheck.py` → `logs/optcdeg2_qcal_recheck.json`
6. `python3 optcdeg2_kkt_primal_check.py` →
   `logs/optcdeg2_kkt_primal_check.json`
7. `python3 optcdeg2_family_windows.py` with `6250 12500 25000`, then
   `50000 100000` → `logs/optcdeg2_family_windows.jsonl`
8. Second revision (Section 9.2): `timeout 120 python3 revision2_checks.py`
   → `logs/revision2_checks.log` (reads stored results only, under a
   second). Crossref and RePEc lookups of the cited DOIs, the Bayreuth eref
   and mathdoc records, and the first page of the univaq PDF read with
   `pdftotext` in `/tmp`; an HTTP check of the old SICON link.
9. Third revision (Section 9.3):
   `OMP_NUM_THREADS=1 timeout 120 python3 revision3_checks.py` →
   `logs/revision3_checks.log` (scalar example of Remark 3.3; about 3 s).
   `curl` of the Maurer–Osmolovskii PDF (matwbn) and of its mathdoc record;
   page 1 of the PDF read with `pdftotext` in `/tmp`.

## Sources

Bibliographic details below were checked against Crossref, RePEc, the
Bayreuth eref record or the mathdoc record on 2026-09-30, and the
Maurer–Osmolovskii title against page 1 of the linked PDF; the papers were
not read for this report unless stated.

- N. P. Osmolovskii, F. Lempio, *Transformation of quadratic forms to perfect
  squares for broken extremals*, Set-Valued Analysis 10(2–3) (2002) 209–232,
  DOI [10.1023/A:1016588116615](https://doi.org/10.1023/A:1016588116615).
- H. Maurer, N. P. Osmolovskii, *Second order optimality conditions for
  bang–bang control problems*, Control and Cybernetics 32(3) (2003) 555–584,
  [record](https://geodesic.mathdoc.fr/item/CC_2003_32_3_a8/) (which shortens
  the title to "Second order conditions for bang-bang control problems"),
  [PDF](http://matwbn.icm.edu.pl/ksiazki/cc/cc32/cc3238.pdf) (title as
  printed on page 1). Parts were read by the verifier and for [E]
  (Section 4, the jump condition and Theorem 4.4).
- H. Maurer, S. Pickenhain, *Second-order sufficient conditions for control
  problems with mixed control-state constraints*, J. Optim. Theory Appl.
  86(3) (1995) 649–667, DOI
  [10.1007/BF02192163](https://doi.org/10.1007/BF02192163).
- W. Alt, R. Baier, F. Lempio, M. Gerdts, *Approximations of linear control
  problems with bang-bang solutions*, Optimization 62(1) (2013) 9–32, DOI
  [10.1080/02331934.2011.568619](https://doi.org/10.1080/02331934.2011.568619),
  [Bayreuth eref record](https://eref.uni-bayreuth.de/63114).
- W. Alt, U. Felgenhauer, M. Seydenschwanz, *Euler discretization for a
  class of nonlinear optimal control problems with control appearing
  linearly*, Comput. Optim. Appl. 69(3) (2018) 825–856, DOI
  [10.1007/s10589-017-9969-7](https://doi.org/10.1007/s10589-017-9969-7).
  Only the abstract was seen (Remark 2.5).
- T. Scarinci, V. M. Veliov, *Higher-order numerical scheme for linear
  quadratic problems with bang–bang controls*, Comput. Optim. Appl. 69(2)
  (2018) 403–422, DOI
  [10.1007/s10589-017-9948-z](https://doi.org/10.1007/s10589-017-9948-z),
  [univaq PDF](https://ricerca.univaq.it/bitstream/11697/151290/1/7.pdf).
  An earlier version of this report listed this DOI and PDF as "Alt et al."
  (Remark 2.5).
- Further Osmolovskii–Maurer material on the Riccati approach:
  [Riccati chapter](https://www.springerprofessional.de/second-order-sufficient-optimality-conditions-for-a-control-prob/3214908),
  [IMPAN slides](https://old.impan.pl/dzialalnosc/konferencje/konferencje-wspolorganizowane-przez-impan/xxxv/osmolovski.pdf).
  The "SICON paper" link given in an earlier version
  (`uni-muenster.de/.../SICON_40257.pdf`) returned 404 on 2026-09-30.

## 9. Revision after verification (root, 2026-09-30)

### 9.1 First revision

An independent verifier checked Parts A and B
([report](../reviews/bangbang-verification/verification-report.md)). The
root applied its findings, which the verifier had established with its own
code and derivations:

1. optcdeg2: exact rational recomputation of the same calibration
   (293.876075095875092379…, truncated), a rigorously feasible point
   (f* ≤ 293.87607509587509328), gap 9.0e-16; the author's primal point is
   not exactly feasible; the `V_t` rounding and one-ulp widening are now
   described (Section 5.4, Summary).
2. Proposition 1.2: the converse of (2) needs `f*` attained.
3. Theorem 2.3(2): the failure radius is `δ_1 = min(δ_*, δ_β)`; the Θ(1/h)
   conclusion stands. (`δ_σ` was added to the minimum in Section 9.2, M1.)
4. Summary: the optcdeg2 family-A failure is an SGM failure on whole arcs
   (w = 0), not a window-size result; the verifier's w = 0.5 toy tests the
   window law (affine family fails on 0.270 time units, predicted 0.280;
   tangential family on none).
5. Remark 2.5: citations corrected; the O(h) rate for nonlinear problems is
   unverified; a Hölder rate would give `O(h^{-1/2})` failing stages.
6. Proposition 3.1: one-sided time regularity made explicit; robustness
   checks and the exact relation to Osmolovskii–Maurer added.
7. Proposition 3.2 and Remark 3.3: the forcing gives only
   `∫|β|²/|σ| < ∞`; the scalar sketch has a gap before `τ`.
8. Theorem 4.1: `B = f*` assumes window exactness; regularity conditions
   added; tangency in (H3) is redundant.
9. Novelty: prior Riccati-with-jumps and quadratic verification-function
   work cited.

Not rechecked by the verifier: the author's scripts, Sections 5.7–5.8, and
the Alt–Felgenhauer–Seydenschwanz full text. The `n ≥ 2` conjecture was
then worked out in [E] (see Section 9.2, R5).

### 9.2 Second revision, after the round-1 confirmation

A round-1 confirmation of the first revision found items of the verifier's
report that had not been applied, and a few new ones. Each was checked
before the text was changed. Numerical checks read stored results only
(`revision2_checks.py` → `logs/revision2_checks.log`); no certificate or
screening run was repeated, because none of the changes affects them. This
second revision has not been re-checked independently. (A round-2
confirmation later checked it; see Section 9.3.)

- **R1 (gap against a rigorous upper bound).** Checked in exact rationals:
  the certified bound (the stored double) is 2.29e-12 below the verifier's
  rigorous upper bound 293.87607509587509328 (7.8e-15 relative), and
  8.24e-12 below the author's float point, which lies 5.96e-12 above the
  upper bound. The Summary and Section 5.5 now state the gap as 2.3e-12,
  add the rigorous upper bound and the exact certificate value to the
  table, and replace "the effect of repairing that exactly was not
  bounded" with the verifier's result that repairing lowers the value.
- **R2 (`p_v(3092)`).** `logs/optcdeg2_qcal_data.npz` gives 7.599e-12;
  `logs/refine_primal.log` gives 6.19e-12 from the refinement's own costate
  computation, and `logs/explore1.log` gives −1.15e-3 before refinement.
  Section 5.3 now gives both values and says which one is the certificate
  data.
- **R3 (Sources).** Crossref and RePEc confirm that DOI
  10.1007/s10589-017-9948-z is Scarinci–Veliov, COAP 69(2) 403–422; the
  first page of the univaq PDF (read with `pdftotext`) shows the same paper.
  The Sources entry "Alt et al. ... (title from memory)" was replaced by full
  entries for Scarinci–Veliov, Alt–Baier–Lempio–Gerdts and
  Alt–Felgenhauer–Seydenschwanz, consistent with Remark 2.5.
- **R4 (Proposition 3.1 regularity).** Checked that the proof needs
  one-sided limits of `r` and `∇_x r`, which requires one-sided continuity
  of the time derivative `∂_tS` and of `∇_x∂_tS`, not of `S`. The hypothesis
  is now stated on `∂_tS`, with `S`, `S_x`, `S_xx` continuous, and `r ≥ 0`
  is assumed for `t ≠ τ`. The proof now treats each side separately
  (`r(t,x*(t),u) = σ(t)(u − u*(t)) → 0`, as in [E, Theorem 1, step 2]) and
  notes that the `u`-slope of `∇_x r` contains no `∂_tS`, so either side
  gives tangency. Section 0 now writes the time derivative in `r` as `∂_tS`,
  to separate it from the discrete family `S_t`.
- **R5 (consistency with [E]).** Checked [E] Summary, Theorems 1–2,
  Corollaries 3 and 7, Lemma 14, Proposition 15 and Section 4.1, and the
  confirmation `reviews/ext-bangbang-n2-confirm.md` (which verified the
  revised [E] and asked that the Example C blow-up be labelled a float
  result). Remark 3.3 now keeps the scalar sketch, removes the label "a
  conjugate point" and the sentence "the relation to this construction is
  not worked out", and adds [E]'s answer: the `η_L > 0` criterion in the
  local formulation (any `n`), the refutation of the "no conjugate point"
  reading (Corollary 7, Example B; it applies to the scalar sketch too), and
  the pre-`τ` obstruction in the global form (Example C, Proposition 15,
  float blow-up). Updated with pointers to [E]: the Summary ("Still open"
  and a new paragraph), the Section 6 open list, the status table, the last
  line of Section 9.1, and a new Scope paragraph after Theorem 4.1 (M4).
- **M1 (Theorem 2.3(2) radius).** Checked: the proof of part (2) uses
  `|σ(t)| ≤ γ_2|t−τ|`, which (W2) gave only "near `τ`". (W2) now names that
  neighbourhood `|t − τ| ≤ δ_σ`, part (2) uses
  `δ_1 = min(δ_*, δ_β, δ_σ)`, and part (1) restricts its near-switch step to
  `s ≤ min(δ_σ, γ_1μ/(4ΔL²))`, with the linear tangency bound assumed on the
  same neighbourhood.
- **M2 (toy numbers).** From the verifier's logs
  (`window_toy_k-0.5_{box,reach}.json`): with the box domain the affine
  family fails on 68, 135, 270, 540, 1079 stages at `N = 500 … 8000`
  (0.272, then 0.270, 0.270, 0.270, 0.26975 time units, symmetric about the
  switch); with the exact reachable set on 17, 35, 69, 136, 274 stages, all
  at or before the switch stage (0.068–0.070). The tangential family fails
  on none in both cases. The Summary now gives the domain, the `N` range and
  the reachable-set result.
- **M3 (Corollary 2.4).** Checked: for `n = 1`, `ℓ_1 ≡ 0` and
  state-dependent `b`, affine families have `β(t) = b'(x*(t))ψ(t)`, which is
  nonzero away from `τ`, so exactness there also needs (W5). Added.
- **M4 (Theorem 4.1).** The parenthetical now names the time derivative
  `∂_tS` of the continuous `S`. The Scope paragraph points to
  [E, Section 4.1] (Lemma 14; Example C, float blow-up).
- **M5 (Section 5.7).** Added a sentence that family A's failure on
  optcdeg2 (`w = 0`) is the SGM failure of Section 5.2; its 2.32 time units
  equal the head arc (1.237) plus the tail arc (1.084).
- **M6 (novelty and Sources).** "Must be cited" became "Related prior
  work". Full Sources entries were added for Osmolovskii–Lempio,
  Maurer–Osmolovskii (Control Cybern. 32(3) 555–584),
  Maurer–Pickenhain (JOTA 86(3) (1995) 649–667),
  Alt–Baier–Lempio–Gerdts and Alt–Felgenhauer–Seydenschwanz; details
  checked against Crossref, RePEc, eref and mathdoc. The old SICON link
  returned 404 and is now marked so.
- **M7 (rounding of the exact lower bound).** The exact value is
  293.87607509587509237940; it is now quoted truncated,
  293.876075095875092379…, in the Summary, Section 5.5 and Section 9.1. The
  bracket 9.0e-16 is unchanged (9.006e-16 against the quoted upper bound).

### 9.3 Third revision, after the round-2 confirmation

A round-2 confirmation
([report](../reviews/bangbang-root-fixes-confirm-r1.md)) found all 14 items
of Section 9.2 correctly applied and raised three remaining issues. Each was
checked before the text was changed. No certificate or screening run was
repeated, because none of the changes affects them. This third revision has
not been re-checked independently.

- **C1 (Remark 3.3: the sign of `η_L` in the global form).** Checked in [E]:
  Summary item 3 (in the global form, conjugate points of the relaxed LQ
  problem can appear on both arcs) and Theorem 8 (the criterion uses `η̂`,
  not `η_L`); `P̂ ⪯ Q` follows by comparison because the singular term is
  positive semidefinite. Reproduced the confirmation's scalar example with a
  separate script (`revision3_checks.py` → `logs/revision3_checks.log`). In
  exact arithmetic (sympy): `σ(τ − s) = s(1 + 50s)/100 > 0` and
  `σ(τ + s) = −s(1 + 50s)/100 < 0`, so the minimum-principle signs hold;
  `σ̇(τ) = −1/100`, `D = 1/50`, `η_L = 1/10`, `F'(τ) = 0` and
  `F''(τ) = 21/50 = D + Δ²η_L`. In floating point, two methods (the
  linearization `φ̈ = (1 − 2ε)φ/|σ|`, and `y = −1/P`) give the global-form
  blow-up at `t = 1.587328` (`ε = 0`) and `t = 1.596350` (`ε = 0.01`), as
  the confirmation found; in the local formulation (`Q` on `[τ + δ_0, T]`,
  the singular equation on the layer) `P` stays bounded (`0.0005` at
  `s = 1e-12`, for `δ_0 = 0.05` and `0.2`). The direction
  `η_L < 0 ⇒ blow-up` was also checked on a second scalar set (`x(τ) = 0.5`,
  `Φ_xx = −1.1`: `η_L = −0.1`, `D = 1`, `F''(τ) = 0.6`, so the SSC holds):
  the global-form `P̂` blows up at `t = 1.378`, and the local one at
  `s = 7.0e-4` after `τ` (`δ_0 = 0.05`). Text changed: the false sentence
  now says that `η_L < 0` forces the blow-up even when the SSC holds; "in
  the layer after `τ`" became "after `τ`"; a new bullet explains the global
  form and gives the scalar example; the sketch's dichotomy near `τ+` now
  says "if `P̂` is still finite there"; the closing paragraph says that the
  sketch is complete near `τ+`, that `η_L` decides only in the local
  formulation, and that in the global form existence can fail on either
  side of `τ`. Also updated: the Summary paragraph on `n ≥ 2`, the Scope
  paragraph after Theorem 4.1 (the scalar example has constant `b` and
  `ℓ_1 = 0`, so by [E, Lemma 14] (H3) implies the global form, and backward
  comparison puts every calibration with `P(T) ≤ Φ_xx` below `P̂`), the
  Section 6 open list and the status table.
- **C2 (Theorem 4.1 regularity).** Checked: Proposition 3.1 needs `∂_tS`
  and `∇_x∂_tS` to extend continuously to `τ` from each side, which
  Theorem 4.1 did not state; `∇²_x r` in (H3) contains `∇²_x∂_tS`, so "`∂_tS`
  `C¹` in `x`" was too weak; and step (c) compares the difference quotient
  of `S_xx` in `t` with `∇²_x∂_tS`, which needs its time continuity
  (one-sided at `τ`). With the new list, `S` and `S_x` are continuous in `t`
  because `∂_tS` and `∇_x∂_tS` are bounded on each side, and `S_xx` is by
  the Lipschitz condition, so Proposition 3.1 applies. Text changed: the
  parenthetical after Theorem 4.1 now requires `∂_tS` to be `C²` in `x`,
  with `∂_tS`, `∇_x∂_tS` and `∇²_x∂_tS` continuous on each side of `τ` up to
  `τ`. Step (c) now reads `h·[r_xx + o(1)]` and gives the reason; the
  earlier `O(h + e_h)` would need a Lipschitz condition in `t` that is not
  assumed, and only `⪰ hμ/2` is used (later corrected to `⪰ hμ'I`,
  `μ' < μ`; see the root edit after round 3 at the end of this section). The Theorem 4.1 row of the status
  table is updated. No conclusion changes.
- **C3 (Maurer–Osmolovskii title).** Checked: page 1 of the linked matwbn
  PDF (read with `pdftotext`) prints "Second order optimality conditions
  for bang–bang control problems" (Control and Cybernetics vol. 32 (2003)
  No. 3; 30 pages, consistent with 555–584); the mathdoc record gives
  "Second order conditions for bang-bang control problems". The Sources
  entry now uses the printed title and notes the record's shorter one; the
  Sources preamble says the title was checked against the PDF.
- **Status lines.** The header now records the round-2 confirmation and this
  revision. The Proposition 3.1 row of the status table says that the
  confirmation re-derived the revised proof step by step, and the end of
  Section 9.2 points here. Section 8, item 9, lists the commands.

*Root edit (2026-09-30), from `reviews/bangbang-root-fixes-confirm-r2.md`:* the
Theorem 4.1 parenthetical no longer claims the listed conditions include all
of Proposition 3.1's regularity hypotheses; it states the exception
(continuity of `S` at `τ`, unused by the proof). No conclusion changed.

*Root edit (2026-09-30, closing revision):* the header now records the
round-3 confirmation (`reviews/bangbang-root-fixes-confirm-r2.md`), and the
source of the previous root edit is corrected from
`reviews/bangbang-root-fixes-confirm.md` to
`reviews/bangbang-root-fixes-confirm-r2.md`, where that nit was raised.

*Root edit (2026-09-30, after round 3):* changes from
`window-exactness.md` (Sections 0.3, 7.2 and 8) and `singular-arcs.md`.
(1) Theorem 4.1, step (c): `hμ/2` replaced by `hμ'I` with `μ' < μ` (a
factor-2 slip against the (H3) margin; no conclusion changes); step (e)
now says Theorem 2.3(1) applies with `μ'`. (2) Theorem 4.1's statement now
requires an exact terminal term for `B = f*` (a missing hypothesis; the
stage conclusions are unaffected). (3) The Summary's "the tangential family
fails on none" now says it has no failing stage but an inexact terminal
term; the Summary's "Still open" line points to the follow-ups. (4)
Section 6 and the status table now point to the answers on window
exactness and singular arcs. These edits were checked by an independent
agent (`round3-root-edits-confirm` workflow), whose items are applied
here. Item (2) was added to the statement only after that check found it
missing. A second check (`round3-root-fixes-confirm-r2`) led to the current
wording: the terminal infimum is over `X_N` (or `X_N ∩ D`), the remark on
quadratic data assumes quadratic `Φ` and `S` and a free endpoint, and the
Summary says window exactness is decided under stated hypotheses. A third
check (`round3-root-fixes-confirm-r3`) verified these.
