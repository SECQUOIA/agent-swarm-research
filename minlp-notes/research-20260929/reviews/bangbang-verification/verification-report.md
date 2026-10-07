# Verification of `theory-bangbang/report.md` (bang-bang windows, tangency, optcdeg2)

Date: 2026-09-30. Reviewer: independent verifier; I did not produce the material under
review. Scope: Part A, the optcdeg2 certificate (Section 5); Part B, the theory (Sections 1–4, 6).
No files under `theory-bangbang/` were edited or executed (the author's scripts write into
`theory-bangbang/logs/`). All code is my own, in this directory. Only targeted checks were run,
with no project-wide verification and no CI inspection.

## Summary

| item | verdict | key numbers |
|---|---|---|
| optcdeg2 lower bound 293.8760750958728 | **verified** (valid; conservative by 2.3e-12) | exact value of the same certificate: **293.87607509587509238** |
| optcdeg2 primal 293.87607509588105 | **correct as a point value, not an upper bound**; it is 6.0e-12 too high | rigorous feasible upper bound **293.87607509587509328** |
| optcdeg2 gap | **stronger than claimed** | 2.3e-12 for the author's bound (not 8.3e-12); **9.0e-16** (3.1e-18 relative) for the exact value of the same certificate |
| state enclosures `V_t` | **verified** | stored bounds are nearest-rounded (up to 0.4999 ulp inward); the certificate's one-ulp widening covers this at every stage |
| Def. 1.1, Prop. 1.2 | correct (F4-type fix) | "only if" in (2) needs `f*` attained |
| Prop. 1.3 | correct | — |
| Lemmas 2.1, 2.2 | verified | — |
| Thm. 2.3(1) | verified under (W1)–(W5) | — |
| Thm. 2.3(2) | **correct with fixes** | the explicit radius `δ_*` is not justified; a smaller fixed radius is |
| Cor. 2.4 | correct under the [Rv F18] assumptions; **confirmed numerically on a new example with `w ≠ 0`** | non-tangential window 0.270 time units (predicted 0.280) at N = 500…8000; tangential family: 0 failing stages |
| Remark 2.5 (rate `e_h`) | **citation wrong; applicability unchecked** | cited DOI and PDF are Scarinci–Veliov, not Alt–Felgenhauer–Seydenschwanz |
| Prop. 3.1 | correct, with one regularity hypothesis made explicit; I could not break it within its hypotheses | exact link to Osmolovskii–Maurer: tangency ⇔ `q_k = 0` ⇔ no Riccati jump |
| Prop. 3.2 | verified (sufficiency) | — |
| Remark 3.3 | scalar sketch correct after `τ`; **gap before `τ`** | — |
| Thm. 4.1 | correct given (H1)–(H5); **last sentence is conditional** | window exactness is assumed, not proved |
| Section 5.7 | family A does not test the window law (`w = 0` on optcdeg2) | — |
| Novelty | plausible but modest; one known connection missing | O–M / Osmolovskii–Lempio jump condition; Maurer–Pickenhain verification functions |

## Part A — the optcdeg2 certificate

### A.1 Model (`v_model.py` → `logs/model_check.json`)

I parsed the OSIL with my own ElementTree reader (expanding `mult`/`incr`) and inferred the
variable layout from the rows instead of assuming it. Checked exactly (decimal strings as
rationals):

- 150002 continuous variables, 100000 rows, no nonlinear expressions, no integer variables;
- objective `2e-4 Σ_{t=0}^{N} y_t²` (all 50001 terms), no linear part, constant 0;
- rows: `−y_t + y_{t+1} − 4e-4 v_t = 0` and
  `−v_t + v_{t+1} − 4e-4 u_t + 8e-6 y_t + 8e-5 v_t² = 0`, t = 0…N−1, all with lb = ub = 0;
- bounds: `y_0 = 10`, other `y` free; `v_0 = v_N = 0`; `v_t ≥ −1` for 1 ≤ t ≤ N−1;
  `u_t ∈ [−.2, .2]`.

The inferred layout matches the first-wave verifier's layout. No row or bound is omitted by
the certificate: both row families are substituted exactly into `ρ_t`; `y_0²` is in the stage-0
term and `y_N²` in the terminal term; `v ≥ −1` enters through `V_t`; `v_N = 0` is the terminal
set; the `u` box is `[dn(−0.2), up(0.2)] ⊇ [−1/5, 1/5]` in the author's code and exactly
`[−1/5, 1/5]` in mine.

### A.2 State enclosures (`v_states.py` → `logs/states_check.json`, `logs/vt_reviewer.npy`)

Same method as [O] (one forward and one backward interval pass, with `g(v) = v − 8e-5 v²`
increasing for `v < 6250`), implemented independently. Each step is computed exactly in
rationals and rounded outward to the dyadic grid 2^-110. The inverse of `g` is enclosed by an
exact Newton step, which lands below the root because `g` is concave, plus exact checks. The
final boxes are rounded outward to doubles.

- `V_t ⊂ [−1, 1.2134]`; maximum width 2.089.
- The stored `open-instances/logs/optcdeg2_vbounds.npy` are **round-to-nearest** values of the
  exact enclosure. At 34424 stages they cut off up to 1.11e-16 (**0.4999 ulp**) of the exact
  enclosure, so they are not themselves an outward enclosure.
- The certificate widens every stored bound by one ulp (`I.dn`, `I.up`). With that widening
  it **contains my rigorous enclosure at all 50001 stages**. The certificate domain is
  therefore valid, but only because of that widening. Report 5.4 should say so.
- Side remark: rounding to doubles at every step, which I tried first, accumulates to 3.6e-12
  over 50000 steps. That is still rigorous but wider. The grid version is needed for the
  containment comparison.

### A.3 Exact recomputation of the lower bound (`v_qcal_exact.py` → `logs/qcal_exact.json`)

Certificate data: `py, pv, q, c` from `theory-bangbang/logs/optcdeg2_qcal_data.npz`, taken as
exact rationals. Any data give a valid bound. Everything below uses Python `Fraction`
arithmetic.

- **Elimination of y (exact).** `ρ_t = A2 y² + (B0 − Q1·8e-6·e) y + const`, with
  `A2 = 2e-4 + Q1(8e-6)²/2 > 0` asserted at every stage and `e = g(v) + 4e-4 u − c_{t+1}`. I
  derived the reduced residual `G(v,e) = F(v) + K2 e² + K1' e` by hand. At about 110 stages
  (every 500th, ±3 around both switches, and the ends) I checked it exactly against the
  definition of `ρ_t` at three `(v,u)` points each. I also checked that `y*` is the minimizer.
- **Elimination of u (exact).** `u` enters only through `e`, which is affine in `u`. Hence,
  exactly, `inf_{v,u} = min(inf_V G(v,e_−(v)), inf_V G(v,e_+(v)), [K2>0] inf_{R*} G*(v))`,
  with `G* = F − K1'²/(4K2)`. Here `R*` is the set of `v` whose unconstrained minimizer
  `e* = −K1'/(2K2)` lies in `[e_−(v), e_+(v)]`; I enclosed it by exact `g⁻¹` bounds. This
  identity is exact: `G_± ≥` the `u`-minimum pointwise, and the `u`-minimum equals `G*` on
  `R*`. The interior-`u` piece was never active (0 stages).
- **Univariate minimization (rigorous).** Each piece is a polynomial of degree ≤ 4 on an
  interval. The minimum is taken over the endpoints and the local minima. Local minima are
  isolated with an exact Sturm sequence of `G'` and bracketed by exact sign changes; float
  roots serve only as seeds. On a bracket of width `w`, `G ≥ G(l) − max|G''|·w²`; the largest
  slack was 9.5e-29. 11596 quartics were handled: 7785 seeded brackets, and no fallback
  bisections, even-multiplicity roots or endpoint roots.
- **Summation.** Stage minima are rounded down to the grid 2^-200 and summed as integers. The
  loss from this rounding is 1.6e-56.

Results:

| quantity | reviewer (exact) | report |
|---|---|---|
| stage-0 term | 1014.9964727128661 | [1014.9964727128655, 1014.9964727128666] |
| terminal term | −1.8598627153335e-4 | −1.8598627153335e-4 |
| **lower bound** | **293.87607509587509237940** | 293.8760750958728 |
| author stage LB minus exact stage minimum | max −3.7e-19 (0 of 49999 stages above) | — |
| worst stage | 3091 (fractional control) | 3091 |

The author's per-stage lower bounds never exceed the exact stage minima over a smaller domain
(mine). This is the expected direction and independently confirms the author's interval code.
The author's bound is valid. It is 2.29e-12 below the exact value of the same certificate
because the cell enclosures lose 2.8e-12 on the middle arc. Runtime: 17.7 s.

### A.4 Primal re-evaluation (`v_primal.py` → `logs/primal_check.json`)

- **The author's point**, rebuilt exactly as in `optcdeg2_kkt_primal_check.py` (float64
  simulation, `v_N := 0`) and evaluated in exact rationals: objective 293.87607509588104904,
  maximum row violation 8.88e-16, bound violation 1.11e-17 (the double 0.2 exceeds `.2`). This
  reproduces the report.
- **A rigorous upper bound.** Controls are set to exactly ±1/5, `u_3091` to the stored double,
  and `u_47290` is left free. I simulated in mpmath interval arithmetic at 200 bits, bracketing
  `u_47290` in `[u* − 1e-40, u* + 1e-40]`:
  - `v_N(a) = −3.8e-44 < 0 < v_N(b) = +3.8e-44` rigorously, so by the intermediate value
    theorem some `u_47290` in the bracket gives `v_N = 0` exactly;
  - `min_t v_t = −0.8315 ≥ −1`, and all controls lie in `[−1/5, 1/5]`;
  - the objective enclosure over the bracket has upper end **293.8760750958750932772142**
    (width 4.7e-44).

  So **f\* ≤ 293.87607509587509328**. The author's primal value is **5.96e-12 above** the
  objective of this feasible point. Its row violations of 1e-16, multiplied by costates of
  about 100, account for the difference. The report says the effect of repairing the rows "was
  not bounded"; it is now bounded, and repairing *lowers* the value.

### A.5 Gap, and a consistency check (`diag_stage_losses.py` → `logs/diag_stage_losses.log`)

- Author's certified bound vs the rigorous upper bound: **2.29e-12**, not 8.3e-12.
- Exact value of the same certificate vs the rigorous upper bound: **8.98e-16**, or 3.1e-18
  relative.
- Diagnostic: along a 2^-300-accurate version of the feasible trajectory, the telescoping
  identity holds to 5e-85. All stage losses are ≥ 0, and their sum is 8.978e-16, which equals
  UB − LB. Essentially all of it comes from stage 3091: in the certificate data
  `pv(3092) = 7.6e-12`, not the 6.2e-12 quoted in 5.3, and `u_3091` is fractional. All other
  stages lose less than 1e-24.

**Verdict, Part A: verified.** optcdeg2 is closed. The certified bound 293.8760750958728 is
valid. With the same calibration, evaluated exactly, the bound is 293.87607509587509238 against
a rigorous upper bound of 293.87607509587509328.

Fixes to the report:

1. State the gap against a rigorous upper bound (2.3e-12), not against the float point.
2. Say that the stored `V_t` are nearest-rounded and that validity rests on the one-ulp
   widening.
3. Change `p_v(3092) = 6e-12` to 7.6e-12 for the certificate data.

**Unchecked:** the author's own scripts were not re-run, and Sections 5.7–5.8 were not
reproduced. I relied on Python `Fraction` (exact arithmetic) and mpmath `iv` (primal only) as
libraries.

## Part B — theory

**Definition 1.1, Proposition 1.2 — correct (small fix).** Validity holds: telescoping,
equality rows vanish, `ν ≥ 0` handles inequality rows, and each window restriction lies in
`R_j`. As with [Rv F4], the "only if" in (2) needs `f*` to be attained.

**Proposition 1.3 — correct.** The coordinate-by-coordinate vertex move is valid because the
sign enclosure covers the whole box `E × U^W` and `J` is C¹. It applies to the relaxation
without state constraints, as Definition 1.1 allows. The formula
`∂J/∂u_t = h(ℓ_1 + bᵀp_{t+1})` is correct. Remarks 1.4–1.6 were not checked numerically; the
1.5 estimate is heuristic.

**Lemma 2.1 — verified.** Step (1) is a Taylor expansion in `u` using (b) and (d). Step (2) is
a Taylor expansion of `∇_xρ(x̄,·)` using (a) and (e). Step (3) is strong convexity on the convex
set `B_r ∩ D_t`. Criteria (i) and (ii) follow because `|ω| ≤ Δ`.

**Lemma 2.2 — verified.** The one-dimensional maximization gives `s*` and the stated
threshold. The Euler relations `Σ = σ_t + O(h)` and `g = β_t + O(h)` are correct.

**Theorem 2.3(1) — verified under (W1)–(W5).** I rechecked the inequality
`(3γ_1/4)s ≥ e_h + Δ(e_h + hCΔ/2)²/μ + hΔκ_−/2`, including the restriction
`s ≤ γ_1μ/(4ΔL²)`. The far-from-switch margin needs `σ` and `β` continuous on `[0,T]`, which
is implicit in (W2). (W4) assumes global exactness outside the balls, so the theorem is local
in substance. The report says as much.

**Theorem 2.3(2) — correct with fixes.** The proof uses `|g_t| → |β(τ)|` for every stage with
`|t_t − τ| ≤ δ_*`. That holds only as `t_t → τ`, while `δ_*` depends on `|β(τ)|`, `γ_2`, `Λ` and
`M_s`, not on how fast `β` varies. Fix: take `δ_1 = min(δ_*, δ_β)`, where
`|β(t)|² > |β(τ)|²/2` for `|t − τ| ≤ δ_β`. Then `γ_2 s ≤ Δ|β(τ)|²/(4(Λ+ΔM_s)) <
Δ|β(t)|²/(2(Λ+ΔM_s))` with a margin, and the Θ(1/h) conclusion stands.

The interior hypothesis `B_r ⊂ D_t` matters in practice. In my toy (below), the trajectory
lies on the boundary of the exact reachable set before the switch. With that tight domain the
non-tangential window becomes one-sided and four times shorter: 0.068–0.070 instead of 0.27.
It still has a fixed duration.

**Corollary 2.4 — correct under the [Rv F18] assumptions, and now tested with `w ≠ 0`**
(`v_window_toy.py`). The problem is `min ∫_0^2 (x−a)²/2 + k x u`, `ẋ = u`, `|u| ≤ 1`,
`x(0) = 0`, with `a = 2` on `[0,1)` and `−2` on `[1,2]`, and `k = −0.5`. So `w = −k = 0.5`, there
is one regular switch at `τ ≈ 0.2136`, and the discrete KKT signs were checked.

- Affine family (non-tangential), box domain `|x| ≤ 2`: 68, 135, 270, 540, 1079 failing stages
  at N = 500…8000, i.e. **0.270 time units**, symmetric about `τ`. The prediction `2k²/γ` is
  0.280.
- Family `S = p x − (k/2)(x − x̄)²` (tangential, `Pb = w`): **0 failing stages at every N**.

This is the test the report lacks: on optcdeg2 `w = 0`, so Section 5.7 family A does not probe
Corollary 2.4. There, family A's 2.32 time units are the whole head and tail arcs (SGM failure),
as report 5.2 itself says. The Summary's "Numerical check" paragraph presents it as a
window-size result; reword it.

Minor: in the `n = 1`, `ℓ_1 ≡ 0` example with state-dependent `b`, the claim "fail only where
SGM fails" also needs the margin (W5) away from `τ`, because `β(t) = b'(x*)ψ(t) ≠ 0` for
`t ≠ τ`.

**Remark 2.5, the rate `e_h` — the citations are wrong and applicability is unchecked.**

- The link given as "Alt et al. (COAP, s10589-017-9948-z)" and the univaq PDF are both
  **Scarinci–Veliov**, *Higher-order numerical scheme for linear quadratic problems with
  bang–bang controls*, COAP 69(2):403–422 (2018). I checked the PDF text.
- Bayreuth eref 63114 is Alt–Baier–Lempio–Gerdts, *Optimization* 62 (2013) 9–32: linear
  problems, O(h) adjoints and O(h) in L1 for controls, under a slope condition on the switching
  function.
- The Alt–Felgenhauer–Seydenschwanz paper is COAP 69(3):825–856 (2018),
  DOI 10.1007/s10589-017-9969-7. Per the abstract, it treats Mayer costs, nonlinear dynamics
  with the control entering linearly, and control bounds only. It proves Hölder-type estimates
  under a growth condition and a better order under a stronger second-order condition.

I could not access the full text, so it is unverified that the rate Theorem 2.3(1) needs
(O(h) in L∞ for discrete states and costates at KKT points) is provided there, and under which
hypotheses. With a Hölder rate `h^{1/2}`, Theorem 2.3(1) gives O(h^{-1/2}) failing stages, not
O(1). Terminal state constraints such as optcdeg2's `v_N = 0` appear to be outside that class.
The optcdeg2 certificate does not depend on any of this.

**Proposition 3.1 — correct, with one regularity hypothesis made explicit. I could not break it
within its hypotheses.** The proof needs
`r(τ, x*(τ), u_±) = 0` from the one-sided limits and `∇_x r(τ, x*(τ), u)` to exist. So `S_t`
must be continuous up to `τ` from each side and C¹ in `x`, not only `S ∈ C²` in `x`. Attempts
to break it:

- *Nonsmooth S* (Hessian jump across a surface through `x*(τ)`, as in the field value
  function): excluded by the C² hypothesis. This is the only escape, as the report says.
- *Time-discontinuous S* (`S⁺(τ,·) ≠ S⁻(τ,·)`): validity forces the jump
  `j = S⁺ − S⁻ ≥ 0` with its minimum at `x*(τ)`. Exactness and `r^± ≥ 0` then give
  `S_t⁺ = S_t⁻` at `x*`, and `σ(τ) = 0`. Each one-sided family is then separately tangential
  (`S^±_xx b = w`), so jumps must satisfy `j_xx b = 0`. No escape.
- *Residuals not affine in `u`:* step (1) is unnecessary. The two one-sided limits alone give
  `∇_x[r(τ,x*,u_+) − r(τ,x*,u_−)] = 0` (secant tangency). The proposition generalizes.
- *Several controls:* tangency holds only in the jump direction `[u]`.
- *`x*(τ)` on the boundary of the set where `r ≥ 0` is required* (for example the reachable
  set; in my toy, `x*` is the maximal reachable state before `τ`): the proof fails, and
  non-tangential families lose less. Interiority is essential and is correctly assumed.

*Relation to Osmolovskii–Maurer (worked out here; the report left it open).* In the
Q-transformation of Maurer–Osmolovskii (Control Cybern. 32 (2003), Section 4.3, following
Osmolovskii–Lempio 2002), the jump condition at `t_k` is `b_{k+}[Q]^k = q_{k+}ᵀ q_{k+}`, with
`q_{k+} = ([ẋ]^k)ᵀ Q^{k+} − [ψ̇]^k` and `b_{k+} = D^k(H) + q_{k+}[ẋ]^k`. For control-affine
dynamics, `[ẋ]^k = b[u]^k` and `[ψ̇]^k = wᵀ[u]^k`, so **`q_{k+} = [u]^k (Qb − w)ᵀ = [u]^k βᵀ`**.
Therefore:

- tangency ⇔ `q_k = 0` ⇔ the O–M solution does not jump, and then `b_k = D^k(H) > 0` is just
  the strict bang-bang condition;
- O–M's jumping solutions certify the second variation with switching-time variations, but
  by Proposition 3.1 they cannot be the Hessians of a pointwise C² verification function.

**Proposition 3.2 — verified (sufficiency).** I rederived `r = σω`, `∇_x r = (Pb − w_t)ω` and
`∇²_x r = M(t,u)` at `d = 0`, and the Schur-complement step. The accessory-LQ reading is
correct. The forcing remark is right for continuous bounded `P`. It forces only
`∫|β|²/|σ| < ∞` (β → 0, possibly logarithmically), not `|β| = O(|t−τ|)`; Remark 3.3 says so.

**Remark 3.3 — scalar sketch correct after `τ`; gap before `τ`.** After `τ`, I checked the
log-decay versus blow-up dichotomy and the linear-rate modification with forward comparison
against `P̂`, assuming sign conventions with `bΔ/γ > 0`.

"Before `τ` there is no constraint at `t = 0`" is true only for the endpoint. The inequality
must still be solvable backward on `[0, τ)`, where the singular coefficient reappears. There,
backward comparison makes `P ≤` the equality solution, which can blow up to −∞: a
conjugate-point-type obstruction. O–M's Theorem 4.4 (fixed `x_0`, one switch) needs nothing
before `τ`, because critical variations vanish there. A pointwise verification function does
need something. The `n ≥ 2` conjecture remains open.

**Remark 3.4 — heuristic.** It is consistent with the above: the field value function's
Hessian jump corresponds to `q_k ≠ 0`.

**Theorem 4.1 — correct given (H1)–(H5), with fixes.** I checked steps (a)–(e), including
`∇²_xρ_t = h[r_xx + O(h + e_h)]` and `β_t = β(t_t) + O(h + e_h)`. The fixes:

1. "Adding an exact window of O(1) stages gives `B = f*`" is conditional. By Proposition 1.2(2),
   window exactness means the discrete trajectory attains the window infimum. That is an
   assumption, the report's own open item "uniform conditioning of switch windows", not a
   consequence.
2. `S_t` must be C¹ in `x`, and `S_xx` Lipschitz in `t`.
3. Tangency in (H3) is redundant. Convexity plus the margin give `r ≥ 0` near the trajectory,
   and Proposition 3.1 then forces tangency. This is harmless.
4. The `e_h = O(h)` caveat above applies.

**Novelty.**

- The discrete window-law dichotomy and Proposition 3.1 were not found stated. Both are
  elementary; Proposition 3.1 is the continuous-time twin of [S, Prop. 4.1].
- The report should cite:
  - Osmolovskii–Lempio, Set-Valued Anal. 10 (2002) 209–232, and Maurer–Osmolovskii (2003):
    Riccati with rank-one jumps; tangency is `q_k = 0` there;
  - Maurer–Pickenhain (JOTA 1995): quadratic verification functions via Riccati equations.
    O–M note that their linear equation (41) is the Maurer–Pickenhain equation with all
    controls on the boundary.
- The singular-coefficient Riccati inequality (control weight `2|σ|/Δ`) is, to my search,
  new in this form. Searches were limited.

## Commands run

All commands were run from `reviews/bangbang-verification/` with `OMP_NUM_THREADS=1`,
single-threaded.

1. `python3 v_model.py` → `logs/model_check.json` (structure verified).
2. `python3 v_states.py` → `logs/states_check.json`, `logs/vt_reviewer.npy` (a first version
   rounding to doubles every step was superseded by the 2^-110 grid version).
3. `python3 v_qcal_exact.py 3080 3100` and `python3 v_qcal_exact.py 47280 47400` (smoke tests,
   outputs removed), then `python3 v_qcal_exact.py` → `logs/qcal_exact.json`,
   `logs/qcal_exact_run.log`, `logs/qcal_exact_stage_min.npy` (17.7 s).
4. `python3 v_primal.py` → `logs/primal_check.json` (8.8 s).
5. `python3 diag_stage_losses.py` → `logs/diag_stage_losses.log` (tail only; about 4 min).
6. `python3 v_window_toy.py -0.5 reach` and `python3 v_window_toy.py -0.5 box` →
   `logs/window_toy_k-0.5_{reach,box}.json`. A first run with `k = +0.5` was discarded because
   that case has a second switch near `T`, so the one-switch point is not a KKT point.
7. Web searches and fetches: Osmolovskii–Maurer papers (text of Maurer–Osmolovskii 2003,
   Section 4); records for Alt–Felgenhauer–Seydenschwanz (COAP 69(3)), Scarinci–Veliov
   (COAP 69(2)) and Alt–Baier–Lempio–Gerdts (Optimization 62).

These are targeted local checks. No CI results were consulted or duplicated.

## Sources

- Maurer, Osmolovskii, *Second order optimality conditions for bang-bang control problems*,
  Control Cybern. 32 (2003): https://bibliotekanauki.pl/articles/970524.pdf
- Osmolovskii, Maurer, *Equivalence of second order optimality conditions for bang–bang
  control problems, Part 2*, Control Cybern. 36 (2007):
  https://www.rcin.org.pl//Content/217459/PDF/RB-2007-85.pdf
- Osmolovskii, Lempio, Set-Valued Anal. 10 (2002): https://doi.org/10.1023/A:1016588116615
- Alt, Felgenhauer, Seydenschwanz, COAP 69(3) (2018):
  https://ideas.repec.org/a/spr/coopap/v69y2018i3d10.1007_s10589-017-9969-7.html
- Scarinci, Veliov, COAP 69(2) (2018) (the DOI and PDF the report attributes to Alt et al.):
  https://ideas.repec.org/a/spr/coopap/v69y2018i2d10.1007_s10589-017-9948-z.html
- Alt, Baier, Lempio, Gerdts, Optimization 62 (2013): https://eref.uni-bayreuth.de/63114
