# Review of `theory-bangbang/singular-arcs.md` (calibrations along singular arcs)

Date: 2026-09-30. Reviewer: independent verifier; I did not write the note or
its scripts. Scope: every proof step in Sections 1–3, the Goh/Kelley
identifications against a primary source, and the E2 and catmix computations,
re-derived with my own code where feasible. Checks were targeted, run with
`OMP_NUM_THREADS=1` and `timeout`; no project-wide verification; CI not
inspected; nothing committed. Scripts and logs:
`reviews/singular-arcs-review-checks/`.

## Verdict

**Fixes needed (minor to moderate); the core results stand.**

- Sections 1–3 are correct as stated, with a few imprecise constants and
  hypotheses noted below:
  - tangency on the whole arc;
  - the Goh identity `BᵀW − WᵀB = G`;
  - `bᵀMb = R = −∂_uσ̈` (Kelley);
  - the quadratic-versus-cubic gap and the null-Lagrangian example;
  - the junction statements, including the `a_j` obstruction;
  - the discrete lemmas;
  - the gauge identity and the Euler saddle computation;
  - Proposition 3.6.

  I re-derived all of them. The identities were also checked with my own
  sympy code (exact).
- The Goh and Kelley identifications agree with Aronna–Bonnans–Dmitruk–Lotito
  (2012), which I read (arXiv 1107.0161, Section 4). One equation number is
  wrong: `V` is defined in their eq. (36), not (38).
- All reported E2 and catmix numbers that I recomputed reproduce, either with
  independent code or by re-running the author's scripts.
- One interpretation needs correcting (F1). The catmix "smooth" saddle point
  is not smooth. On the arc its controls oscillate from stage to stage, with
  a slowly varying envelope: at N = 100 they range over [0.055, 0.41] around
  `u_s = 0.227`. So the "quantitative match" of the chattering gain compares
  the chattering point with an oscillating KKT point, not with a smooth one.
  It should be presented as a heuristic agreement.
- The saddle claim itself is confirmed independently, in the original 2-D
  trapezoidal form.
- A positive addition is available (F2). The curvature of the accessory symbol
  at `ω = π` predicts the "every 12 stages" pattern exactly (12.0 stages,
  independent of N), and roughly the number of negative eigenvalues. This
  gives quantitative support to the reading of Remark 3.7.
- There is a relevant paper the note does not use (F6): Felgenhauer (2016) on
  Euler discretization of bang-singular-bang problems.

## 1. What I checked, and the results

| claim | how I checked | result |
|---|---|---|
| Prop 1.1 (tangency on the arc) | proof re-derived step by step | correct |
| Cor 1.2 (Goh) | re-derived; own sympy check, random polynomial data, `n = 2, 3`, `m = 2` (`v1`) | `G = BᵀW − WᵀB` exactly; `G` antisymmetric, so Goh's symmetry condition means `G = 0`; ABDL's `V = ½(CB − (CB)ᵀ) = ½G` with `C = H_ux = −Wᵀ` |
| Prop 1.3 (`bᵀMb = R = −∂_uσ̈`) | re-derived (a) and (b) by hand; own sympy check of the intermediate formula for `∂_uσ̈` in the proof, and of `R = −∂_uσ̈` identically in `(x, ψ, u)`, `n = 2, 3` (`v1`) | all identities hold exactly; `R` matches ABDL eq. (39) with `Q = H_xx`, `C = −wᵀ`, `B_1 = g_xb − ḃ` (their eq. (30)), `S = −wᵀb` |
| Prop 1.3(a), Prop 1.5 (`∇²_x r = M(u*) + (u − u*)Z`) | own sympy check for an explicit cubic `S(t,x)` around a moving point with `ẋ* = g(x*, u*)`, `n = 2` (`v1`) | holds exactly; also `M(u) − M(u*) = (u − u*)(Z − S_xxx[b])` for quadratic `S` |
| Prop 1.5 example | by hand | `K = ℓ_0''(x_s)`, `c₁ = 1`; the quadratic class needs `K ≥ 1`; `S − x³/6` has `Z = 0`. The gap is real |
| Prop 1.6 | by hand | correct |
| Prop 2.1(a) | by hand; catmix and E2 numerics | correct (`σ(t₁ − s)/s² → 0.34921` against 0.34915 in E2, own code `v3`) |
| Prop 2.1(b) | by hand | correct |
| Prop 2.1(c) | by hand, including the remainder bookkeeping the note calls sketched | correct; see Section 2.2 |
| Remark 2.2 | by hand, against [E, Theorem 1] | necessity correct; for catmix, `η_L = 1` **exactly** (see F5) |
| Lemma 3.1, Props 3.2–3.4 | by hand, against [R, Lemma 2.1] and [E, Lemma 10] | correct under the stated hypotheses; the Summary wording of 3.3 is slightly stronger than the proposition (F4) |
| Remark 3.5 (gauge; Euler saddle) | by hand, including the transient of the non-alternating mode; E2 numerics (`v5`) | correct. Minimum reduced-Hessian eigenvalue `−1.72e-3, −4.40e-4, −1.11e-4, −2.80e-5` against `h²bᵀw = −1.80e-3, −4.50e-4, −1.12e-4, −2.81e-5` (N = 50…400) |
| Prop 3.6 | by hand | correct: along `(−1)^t(η, ε)` the storage terms cancel and each stage's quadratic model equals `½ε²f(π)` |
| Remark 3.7 (KYP) | not re-proved | cited; see F6 on the discrete-time source |
| E2 continuous (4.1) | own closed-form and ODE code (`v3`) | `t₁ = 1.1982904373`; `J* = 0.1489691259 / 0.3989691259 / −0.1010308741` for `k₁ = 0, −½, +½`; `σ = 0.3125` at `t = 0.2733`, `σ = 0.0625` at `t = 0.7858`; global calibration `P = [[−k₁, −k₂], [−k₂, ¼]]` and `M`, `F − P` re-derived by hand |
| E2 exact certificates (4.2, 4.3) | own QP, own exact rational KKT solve and own exact 3×3 principal-minor stage test (`v4`), N = 50, 100, 200 (`k₁ = −½`) and 50, 100 (`k₁ = 0`) | same `J`, same failure counts for A, B1 exact with zero failing stages, terminal test passes; the author's `lqsing_selftest.py` re-run gives a difference of 0 |
| E2 `k₁ = +½` chattering (4.3) | own multistart (`v5`, `v5b`) and own smooth KKT point | chattering confirmed; see F5 for the baseline and for a better local optimum at N = 100 |
| E2 `k₁ = 0`, B2 statistics (4.3) | author's `fam_B2`, own statistics (`v9`) | `κ_t ≈ 0.919h` and `0.913h` confirmed; the `|β_t|` statement is misleading (F5) |
| catmix reduction (5.1) | by hand | exact; the Mayer calibration `S = m·exp(φ)` has residual `S·r_reduced` |
| catmix singular data (5.2) | own sympy code (`v2`) | `θ_s`, `u_s`, `ψ_s`, `w_s`, `P_s`, `K = 2√10`, `bw`, `c₁`, `b²M(u*) = K` all reproduce. **Cross-check in the original 2-D Mayer form:** the Kelley quantity there equals `e^{C₀}·2√10`, as the monotone reduction predicts |
| catmix junctions (5.3) | own ODE code, direct simulation of the 2-D system (`v2`); author's `catmix_junctions.py` re-run | `t₁ = 0.136299034595`, `t₂ = 0.725230107592`, `J* = −0.048055685860877`; `a_j = −14.0998` (threshold `−1.2220`) at entry, `+26.7489` at exit |
| catmix symbols (5.4) | author's scheme code, plus my own symbol-curvature evaluation (`v8`) | `f(π)/h³ = −0.02729` for the trapezoid, confirmed |
| catmix saddle (5.5) | own mpmath (40 digits) implementation of the **original 2-D** COPS trapezoidal transcription, not the author's reduced model (`v6`, `v6b`) | J of the stored COPS controls is `−0.04806943203095955` (matches [C]); the saved saddle point has gradient `2.8e-17`, correct KKT signs, 5 negative eigenvalues, lowest `−3.144e-8` in J units with a fully alternating eigenvector, and `J_smooth − J_chatter = 3.72326e-8`. All match the note. See F1 on "smooth" |
| catmix screening (5.6) | author's `catmix_windows.py 100 fixed 1 2` and `catmix_calib.py 100 chatter 1e-10 0.01` re-run | reproduce the logged breaks (17, 29, 41, 53, 65; one break at 0.63) and the affine band loss 0.01700 |

## 2. Proof notes

### 2.1 Section 1

- **Prop 1.1.** (a) An affine function of `u`, nonnegative on `U` and zero at
  an interior point, vanishes on `U`. (b) `∇_x r = 0` at `(x*, u)` for every
  `u`, and at `u*` this is exactly `ψ̇ = −H_x` for `ψ = S_x(t, x*(t))`.
  (c) Subtracting (b) at two controls gives `∇_xσ_S = Pb − w = 0`. The
  regularity stated suffices.
- **Cor 1.2.** `σ̇_i = −w_iᵀg − b_iᵀH_x` and `∂_{u_j}H_x = −w_j` give
  `G_ij = b_iᵀw_j − w_iᵀb_j`. Tangency gives `BᵀW = BᵀPB`, which is
  symmetric, so `G = 0`. This is Goh's condition in ABDL's form `V ≡ 0`.
- **Prop 1.3.** `Ṗb = ẇ − Pḃ` and symmetry of `P` give
  `bᵀṖb = bᵀẇ − wᵀḃ` and `2bᵀPg_xb = 2wᵀg_xb`. The strictness corollary
  `K ≥ 2ε|b|²` follows from `∇²_x r ⪰ 2εI`. The Kelley sign convention
  (`−∂_uσ̈ ≥ 0` for a minimum, `H` minimized) is the standard one for
  order 1.
- **Prop 1.5(b).** A fully symmetric tensor with `T[b,·,·] = Y` exists for
  every symmetric `Y`. The time derivative of the cubic term
  `(1/6)T[d,d,d]` automatically cancels `S_xxx[ẋ*]` in `Ṗ`, so `P`, `Ṗ` and
  `M(t,u*)` are unchanged. This confirms "(adjust `∂_tS_xx`)".
- **Remark 1.4.** For E2, `M = [[K, p₂₂ + k₂], [p₂₂ + k₂, ṗ₂₂ − 2p₂₂ + 1]]`
  and the scalar inequality follow by hand. The `n ≥ 2` statement is
  correctly labelled a sketch.

### 2.2 Proposition 2.1(c): the remainder bookkeeping closes

The note labels the remainder terms as sketched. I checked them.

- **Remainder in the Hessian identity.** For `n ≥ 2` the identity
  `bᵀ∇²_x r(u°) b = η̇ + a_j + …` carries `O(|β|)`, not `O(|η|)`: the terms
  `βᵀḃ`, `βᵀg_xb` and `βᵀb_xb` involve the components of `β` orthogonal to
  `b`. But `β` is `C¹` up to `t_j` with `β(t_j) = 0` (tangency at the
  one-sided limit), so the remainder is `O(s)` anyway. Suggested wording:
  `O(s + |β|) = O(s)`.
- **The case `|η| ≪ s`.** The test step `λ = √s` in direction `b` gives
  `m° ≥ −2|σ|Δ/λ² − O(λ) = −O(√s)`. Hence `ϵη' ≥ |a_j| − o(1)`, and so
  `y = ϵη/s ≥ |a_j|/2` for small `s`. This puts the argument in the
  `|η| ≳ s` regime, where the step `λ = 2|σ|/|η| = O(s)` is admissible.
- **The log-growth contradiction.** With `|σ| = γs²(1 + o(1))`, the bound
  `min_y [Δy²/(2γ) − y] = −γ/(2Δ)` survives the `(1 + o(1))` factor. The
  contradiction `y(s) ≥ y(s₀) + c·log(s/s₀)` is then valid.

So part (c) is proved for `a_j < −γ/(2Δ)`, under the stated regularity
(`P` `C¹` up to `t_j` on the bang side). The status row may say
"proved (reviewer completed the remainder terms)". The case
`−γ/(2Δ) ≤ a_j ≤ 0` remains open, as the note says.

### 2.3 Section 3

- **Lemma 3.1(a).** Take `d = −(s/Λ)β` in the 3×3 Hessian form. Correct.
- **Prop 3.2.** The loss formula follows from the stated upper bound.
  Correct.
- **Prop 3.3.**
  - The step `κ_t = bᵀF_x^{−T}(w^h + β) ≤ bᵀw^h + C₁h + C₃|β|` and the
    two-case loss bound are correct.
  - The hypothesis `K_t ⪯ hΛI` is essential (F4).
- **Prop 3.4.** Lemma 3.1(b) with `|β_t| = o(√h)` and `κ_t ≥ κ₀` gives
  exactness at vertex and fractional stages. Correct under the stated
  assumption `e_h = o(√h)`.
- **Remark 3.5, saddle.** With `F_x ≈ I`, the response to `δu_t = ε(−1)^t`
  starting from `δx = 0` is `δx_t = hbε·[t odd]` plus a slowly varying
  `O(hε)` mode. The cross term averages to `½h²ε²wᵀb` per stage. The slow
  mode contributes `O(h²ε²)` in total. This confirms the stated expansion.
- **Prop 3.6.** Correct.
- **Remark 3.7.** The point about boundary terms is borne out numerically.
  At the catmix saddle, the plain (untapered) alternating direction on the
  free block has **positive** curvature: `+8.98e-7` at N = 100 and
  `+1.23e-7` at N = 200 (`v6b`). A tapered alternating direction has
  negative curvature: `−2.46e-8` and `−2.82e-9`, against the symbol values
  `f(π)(J+1) = −2.60e-8` and `−3.25e-9`. So when `f(π) ~ h³`, the saddle
  direction must be tapered, as the remark implies.

## 3. Findings (most important first)

**F1 (moderate): the catmix "smooth" saddle is not smooth, and the
chattering-gain comparison is heuristic.**

- **What the saved saddle points look like.** The KKT points computed by
  `catmix_trap.py`, described as "smooth ('singular-like')" and with
  "the continuous structure", have the bang–arc–bang active set, but their
  arc controls oscillate strongly from stage to stage:
  - N = 100: `0.3786, 0.1103, 0.2998, 0.1973, …, 0.0585, 0.4106, …`, range
    `[0.055, 0.411]` around `u_s = 0.227`;
  - N = 200: range `[0.037, 0.468]`;
  - the largest deviation from the neighbour average is 0.35 at N = 100;
  - the alternating envelope changes sign every 11–12 stages (`v8`).
- **No smooth KKT point was found.** Newton from a genuinely smooth start
  (`u = u_s` on the arc) injects large alternating components in its first
  step, because the Hessian is nearly singular in alternating directions. It
  then stalls at gradient `7e-8` (`v7`). [C]'s smooth-start local solve
  (`−0.04806939757`) is yet another point, `2.8e-9` below the note's
  `−0.0480693948`.
- **Consequences.**
  - The saddle claim (negative curvature, alternating eigenvectors) is
    unaffected, and I confirmed it independently in the 2-D form.
  - The gain formula `½u_s²|f(π)|(t₂ − t₁)/h` assumes a baseline with no
    alternating component. The measured `J_smooth − J_chatter = 3.72e-8`
    uses an oscillating baseline, so the 6% agreement (and 2% at N = 200)
    is not a like-for-like test.
  - The boundary terms that Remark 3.7 identifies are also of order
    `h²ε²`, the same order in `h` as the predicted gain. So the formula is
    not a controlled leading-order asymptotic; it is a heuristic.
  - The most negative eigenvalue (`−3.14e-8`) lies below the minimum of the
    Toeplitz symbol (`−2.60e-8`). That is impossible for a Toeplitz
    section, so non-Toeplitz effects are present. The note attributes them
    to junction transients (not checked). An equally plausible cause is that
    the Hessian is evaluated at a base point that oscillates with amplitude
    up to about 0.18, far from the stationary discrete singular point.
- **Suggested fix.**
  - Rename "smooth" to "KKT point with the bang-singular-bang active set"
    and describe its oscillating controls.
  - Present the gain and eigenvalue agreements as heuristic,
    order-of-magnitude checks with the right `h²` scaling, not as
    quantitative confirmation.
  - Mention the alternative explanation of the 20% eigenvalue difference.

**F2 (positive; suggested addition): the symbol curvature explains the
12-stage pattern quantitatively.**

- **Numbers.** At the trapezoidal discrete singular point,
  `f(π) = −0.02729h³` and `f''(π) = 0.7906h³` (`v8`; both scale with `h³`).
- **Derivation (heuristic).**
  - The Jacobi equation for a slowly varying envelope `A` of `(−1)^i A_i` is
    `−½f''A'' + f(π)A = 0`.
  - It has oscillatory solutions with wavenumber
    `d₀ = √(2|f(π)|/f'') = 0.263` per stage.
  - The conjugate points are therefore `π/d₀ = 12.0` stages apart,
    independently of N.
- **Agreement with the data.**
  - It matches the stage-wise maximal recursion, which breaks every 12
    stages at N = 100, 200 and 400.
  - It matches the saddle's envelope, which changes sign every 11–12 stages.
  - It roughly predicts the number of negative eigenvalues, `m·d₀/π`: 4.9
    against 5 observed at N = 100, and 9.4 against 8 at N = 200.
- **Suggestion.** Replace the qualitative reading of Remark 3.7 ("the band of
  admissible `P` is narrow") with this computation, labelled as a heuristic
  check. This is a quantitative confirmation of the accessory-symbol
  mechanism.

**F3 (minor): the remaining 2-stage-window break sits on the arc side of
the entry junction, not on the bang side.**

- **Where the breaks are.**
  - At N = 400 the break is at stage 55, which is the first chattering stage
    (`t = 0.1375 > t₁ = 0.1363`).
  - At N = 200 it is at `t = 0.155`, 3–4 stages into the arc.
- **Why this matters.** Proposition 2.1(c) excludes quadratic calibrations on
  the *bang* side of `t₁`.
- **What to say.** The note already labels the link as an interpretation. It
  should add that the break lies on the arc side, which weakens the link, and
  that the N = 100 break (`t = 0.63`) is unexplained.

**F4 (minor): the Summary overstates Proposition 3.3.**

- **The overstatement.** The Summary and the author's claim say "no family
  with bounded Hessians is exact at fractional stages". Proposition 3.3 also
  assumes `K_t ⪯ hΛI`, that is, Hessians that change by `O(h)` per stage.
- **Why the extra hypothesis matters.** With bounded Hessians alone, an
  isolated fractional stage can be made exact by an `O(1)` drop in `P`
  (large `K_t`, large `β_t`). Only over a long run do bounded Hessians force
  most stages to fail.
- **Fix.** Add the hypothesis to the Summary sentence, or say "on all but
  `O(1)` stages of a long run" (the latter would need a short argument).

**F5 (minor): numerical and text slips.**

1. *Section 4.2, junction-layer lags.* The note lists five lags,
   "0.24, 0.12, 0.081, 0.058 and 0.041", for six N. From the log they are
   0.238, 0.148, 0.118, 0.081, 0.058 and 0.041 (N = 50 … 1600). The value
   at N = 100 is missing, and "0.12" is the N = 200 value. The ratio
   `0.118/0.041 = 2.9 ≈ √8` is right.
2. *Section 4.3, `k₁ = +½`.* The fractional-stage counts are 1, 0, 1, 1 in
   `logs/lqsing_k1_p1_2.jsonl`, not "0, 1, 1 and 1".
3. *Section 4.3, `k₁ = +½` prediction.* The prediction `¼h∫(1 − u_s²)`
   compares the chattering point with the smooth KKT point; it does not
   compare either with `J*`.
   - The comparison with `J*` is valid only because the smooth Euler KKT
     point of this gauge is within `o(h)` of `J*`. I computed
     `(J_smooth − J*)/h = +0.040, +0.020, +0.011, +0.005` (N = 50…400,
     `v5`). Please state this.
   - The Euler error in the `k₁ = 0` gauge is `+0.31h`.
     `¼∫u*² = 0.309` cancels it almost exactly in the `k₁ = +½` gauge.
4. *Section 4.3, `k₁ = +½` multistart.* My multistart found a lower local
   optimum at N = 100: `J = −0.11339182`, against the note's `−0.11330`
   (`v5b`). This supports the note's caveat that global optimality is not
   established. Say that the reported values are the best found by one
   procedure.
5. *Section 4.3, `k₁ = 0` A window start.* It lies in 0.78–0.795 (N = 200
   gives 0.795), not 0.78–0.7875.
6. *Section 4.3, `k₁ = 0` B1.* At N = 800, B1 also fails one bang stage
   (`t = 1.1925`, next to the junction), which the text omits.
7. *Section 4.3, B2 tangency defect.* "`|β_t| ≈ (0.04–0.08)√h`" are
   per-component medians (0.083 and 0.041). The Euclidean norm is
   `|β_t| ≈ 0.95h` at both N = 200 and 800, that is, `O(h)`, well inside
   the `√h` tolerance. The `√h` normalization suggests a larger defect than
   there is.
8. *Remark 2.2 and Section 5.3, `η_L`.* For catmix, `η_L = 1` exactly, not
   only to 10 digits. On the last arc (`u = 0`) the reduced cost-to-go is
   `log(1 − θ(1 − e^{−τ}))`, so `Q = V_θθ = −ψ²`. With `bψ = −θ` at the
   junction,
   `η_L = −b²ψ² + b(1 − (10 + 2θ)ψ) = −θ² + 1 − 10θ − θ² + (10 + 2θ)θ = 1`.
   (Exact sympy: `v2`.)
9. *Remark 3.5, examples.* "b constant and ℓ_1 constant" (`ẋ = u`, `∫x²`;
   optcdeg2) gives `w ≡ 0`, not merely `bᵀw ≡ 0`. These are the "affine
   families are already tangential" case. E2 with `k₁ = 0` is the genuine
   `bᵀw = 0`, `w ≠ 0` example.
10. *Corollary 1.2, equation number.* ABDL define `V` in eq. (36). Eq. (38)
    is the second variation `Ω`.
11. *Section 5.5, comparison with [C].* [C]'s "3.4e-8" is measured against
    its own smooth-start local solve (`−0.04806939757`). Against the 8-digit
    listed value `−0.04806939` the gap is `4.2e-8`. The note's KKT point
    (`−0.0480693948`) and [C]'s are different points, `2.8e-9` apart.

**F6 (literature).**

- **Felgenhauer (2016).** U. Felgenhauer, *Discretization of semilinear
  bang-singular-bang control problems*, Comput. Optim. Appl. 64(1) (2016)
  295–326. The abstract (read via RePEc; the paper itself was not read)
  states that, for the "semilinear" case and under second-order conditions,
  the Euler discrete control keeps the bang-singular-bang structure, with
  first-order convergence in L1.
  - This is directly relevant to the note's claims about the sign of `bᵀw`
    and chattering for Euler.
  - If "semilinear" means constant `b` and a state-independent `ℓ_1`, then
    `w ≡ 0` and there is no conflict: the next order decides, as Remark 3.5
    says.
  - The note should check the paper's hypotheses and cite it. Its novelty
    sentence on "the Euler coefficient `h²bᵀw`" should be qualified until
    then.
- **Discrete-time KYP.** Remark 3.7 cites Rantzer (1996) for the
  discrete-time, non-strict KYP lemma. I could not access the paper to
  confirm that it states the discrete-time version (its main theorem is
  usually quoted in continuous time).
  - Either cite a source that states the discrete-time non-strict version
    explicitly, or state the hypotheses used: `(F_θ, F_u)` controllable and
    `F_θ` not on the unit circle.
  - For catmix, `F_θ = 1 − O(h)`, so the second hypothesis holds, but only
    with an `O(h)` margin.
- **Local sufficiency at bang-singular junctions.** Hamiltonian-method
  sufficiency results for bang-singular-bang extremals seem to be the closest
  classical counterpart to Propositions 1.6 and 2.1(b). I recall, but did
  not check, work by Poggiolini and Stefani, and the field constructions in
  Schättler–Ledzewicz, *Geometric Optimal Control* (2012). The note's
  "Sources" section does not mention this line of work. Novelty claims for
  "the tangency statement for calibrations" should say that the Goh/Kelley
  content is classical (the note does) and that Hamiltonian local
  sufficiency proofs for bang-singular junctions exist (not checked by me).

## 4. Assessment of the author's claims

| claim (author's list) | assessment |
|---|---|
| Prop 1.1, Goh corollary | verified |
| Prop 1.3, Kelley; `n = 1` characterization | verified (hand and own symbolic check) |
| Prop 1.5, quadratic vs cubic | verified, including the example |
| Prop 2.1 | (a), (b) verified; (c) verified with the remainder terms completed (Section 2.2); catmix `a_j` numbers verified |
| Euler discrete results (Lemma 3.1, Props 3.2–3.4, Remark 3.5) | verified under the stated hypotheses; the Summary wording of 3.3 needs its extra hypothesis (F4) |
| Prop 3.6, exact-flow symbol | necessity verified; `(K/3)h³` symbolic result reproduced from the author's log; `Kh³/12` numeric plus heuristic, as labelled; KYP citation needs a discrete-time source (F6) |
| E2 results | verified independently (exact) for N ≤ 200; minor slips (F5 items 1–7) |
| catmix reduction and singular data | verified exactly, including a 2-D cross-check of `K` |
| catmix accessory symbols and saddle | saddle and `f(π)` verified independently; "smooth" label wrong, and the quantitative gain match is heuristic (F1) |
| catmix screening | reproduced at N = 100; the 12-stage pattern is quantitatively explained (F2); the entry-junction reading is weaker than stated (F3) |

## 5. Commands run (targeted only)

In `reviews/singular-arcs-review-checks/`, all with `OMP_NUM_THREADS=1` and
`timeout`:

1. `python3 v1_identities.py` → `v1_identities.log` (Section 1 identities,
   exact sympy): all True.
2. `python3 v2_catmix_continuous.py` → `v2_catmix_continuous.log` (catmix
   singular data, 2-D Kelley cross-check, `J*`, exact `η_L = 1`).
3. `python3 v3_e2_continuous.py` → `v3_e2_continuous.log` (E2 continuous
   extremal, window predictions).
4. `python3 v4_e2_discrete.py -1/2 50 100 200` and `… 0 50 100` →
   `v4_e2_discrete_m1_2.log`, `v4_e2_discrete_0.log` (exact E2
   certificates, own code).
5. `python3 v5_e2_chatter.py`, `python3 v5b_e2_chatter_vals.py` → logs (E2
   `k₁ = +½`: smooth baseline, chattering values).
6. `python3 -W ignore v6_catmix_trap_saddle.py 100` →
   `v6_catmix_trap_saddle_100.log` (2-D trapezoidal saddle, mpmath Hessian).
7. `python3 v6b_catmix_trap_directional.py` →
   `v6b_catmix_trap_directional.log` (tapered and plain alternating
   curvature, N = 100, 200).
8. `python3 -W ignore v7_catmix_smooth_start.py 100` →
   `v7_catmix_smooth_start_100.log` (Newton from a smooth start).
9. `python3 v8_symbol_curvature.py` → `v8_symbol_curvature.log` (`f''(π)`,
   conjugate-point spacing, envelope of the saved saddles).
10. `python3 v9_b2_stats.py` → `v9_b2_stats.log` (B2 `κ`, `β` statistics).
11. Author's scripts re-run from `theory-bangbang/singular/`, output to
    `/tmp`, logs untouched:
    - `catmix_windows.py 100 fixed 1 2`;
    - `catmix_calib.py 100 chatter 1e-10 0.01`;
    - `catmix_junctions.py`;
    - `lqsing_selftest.py -1/2 60`.

    All reproduce the logged values. The bytecode cache that these imports
    created in `theory-bangbang/singular/__pycache__` was removed afterwards.

CI was not inspected, and no project-wide checks were run. The author's
larger runs (N = 400–1600 exact certificates, N = 200 active-set saddle,
N = 400 screening) were not repeated; I checked their logs for internal
consistency only.

## 6. Sources examined

- M. S. Aronna, J. F. Bonnans, A. V. Dmitruk, P. A. Lotito, *Quadratic order
  conditions for bang-singular extremals*, NACO 2(3) (2012) 511–546,
  arXiv:1107.0161. Section 4 read (text from the arXiv PDF); eqs. (30),
  (35)–(41), Theorem 4.4 and Remark 5 checked against the note.
- U. Felgenhauer, *Discretization of semilinear bang-singular-bang control
  problems*, Comput. Optim. Appl. 64(1) (2016) 295–326. Abstract only, via
  RePEc (ideas.repec.org).
- A. Rantzer, *On the Kalman–Yakubovich–Popov lemma*, Systems & Control
  Letters 28(1) (1996) 7–10. Bibliographic record only (Lund University
  portal); full text not accessed.
- Cited project notes read for the referenced statements:
  - `theory-bangbang/report.md` (Lemma 2.1, Theorem 2.3, Propositions 3.1
    and 3.2, Theorem 4.1);
  - `theory-bangbang/extension-n2.md` (Section 0, Theorem 1 and its
    Mechanism, Corollary 3, Lemma 10, Corollary 11, Lemma 14);
  - `theory-calibration/scouting.md` (Proposition 4.1, Sketch 4.5,
    Proposition 5.1);
  - `open-instances-wave2/cops/report.md` and `cops/catmix_model.py` (the
    COPS transcription).
- Kelley's, Goh's and Robbins' original papers were not read; the sign
  conventions were checked against ABDL and by derivation.
