# COPS chain and catmix: rigorous dual bounds (open-instances wave 2)

Date: 2026-09-30. Status: computational results with the proofs given here.
Independently verified (Section 7): chain50–400 and catmix100/200 by
[`../../reviews/cops-verification/verification-report.md`](../../reviews/cops-verification/verification-report.md),
catmix400/800 by [`../../reviews/catmix-recheck.md`](../../reviews/catmix-recheck.md).

*Provenance note (root).* The agent that produced these results could not
write this file because its tool environment blocked report writes; the
root saved the agent's report text verbatim on 2026-09-30.

All runs were single-threaded (`OMP_NUM_THREADS=1`) on a shared machine with
load 14–30 on 36 cores, so runtimes are indicative only.

## Summary

| instance | listed primal / best listed dual | our primal (row viol.) | our rigorous dual | gap after |
|---|---|---|---|---|
| chain50 | 5.07226149 / 0.1745 | 5.0722614939828724 (2.3e-16) | 5.072261493982863 | 9.4e-15 |
| chain100 | 5.06978461 / 0.0937 | 5.0697846107387604 (2.0e-16) | 5.0697846107387505 | 9.9e-15 |
| chain200 | 5.06891734 / 0.0826 | 5.0689173417931710 (3.1e-16) | 5.068917341793162 | 9.0e-15 |
| chain400 | 5.0686217 / 0.0956 | 5.0686216946040190 (3.6e-16) | 5.068621694604009 | 1.0e-14 |
| catmix100 | −0.04806939 / −0.0666 | −0.0480694320309596 (1.0e-16) | −0.048069432038882705 | 7.9e-12 |
| catmix200 | −0.04805912 / −0.0725 | −0.0480591455801144 (1.0e-16) | −0.04805914560067171 | 2.1e-11 |
| catmix400 | −0.04805652 / −0.658 | −0.0480565477566116 (1.0e-16) | −0.048056547950296354 | 1.9e-10 |
| catmix800 | −0.04805584 / −1.489 | −0.0480559013308475 (1.05e-16) | −0.048055901841076894 | 5.1e-10 |

- The listed chain duals are ANTIGONE's and the catmix duals LINDO's. All
  listed bounds are valid; LINDO's catmix800 value is below the trivial
  bound −1.
- Our catmix primal points beat the listed ones by about 3.4e-8. The
  discrete optimum uses alternating ("chattering") controls on the singular
  arc.

## 1. Conventions

A **dual bound** is a number `L` with `L ≤ f(x)` for every exactly feasible
point `x` of the OSIL model.

**Listed values** come from the scout's `fetched.csv` (MINLPLib pages,
fetched 2026-09-29). Relative gaps use MINLPLib's convention
`|p−d|/min(|p|,|d|)`.

**Reading the OSIL files.** The reader `osilx.py` is a copy of the
verifier's reader.
- It keeps every constant as its decimal string.
- It reads the `constant` attribute of the objective. catmix's objective
  constant (−1) is included everywhere.

**Structure checks.** Every script asserts the complete row, bound,
objective and constant pattern of the file before using it
(`chain_model.extract`, `catmix_model.extract`).

**Interval arithmetic.**
- chain uses mpmath `iv` at 40 digits, because it needs sqrt, log and asinh.
- catmix uses `ivx.py`: numpy `+ − × ÷` in IEEE round-to-nearest, then one
  `nextafter` step outward. This is the same construction as the first
  wave's `ivnp.py`. Decimal constants are enclosed within ±1 ulp.

## 2. chain50/100/200/400 (COPS hanging chain)

### Structure

Variables:
- `x_0..x_N` and `u_0..u_N`, all free except `x_0 = 1` and `x_N = 3`;
- `eta = h/2 = 1/(2N)`, from the file's decimal;
- `s_i = √(1+u_i²)`.

Rows and objective:
- rows `x_{i+1} − x_i − eta(u_i + u_{i+1}) = 0`;
- length row `eta Σ_{i<N}(s_i + s_{i+1}) = 4`;
- objective `eta Σ_{i<N}(x_i s_i + x_{i+1} s_{i+1})`.

**Polyline form.** Set `z_i = x_i − eta·u_i` for `i ≤ N`, and
`z_{N+1} = x_N + eta·u_N`. This parametrizes the linear rows exactly. A
feasible point is then a polyline `A=(0,1) → Q_1 → … → Q_N → B=(1,3)` with
`Q_k = ((k−½)h, z_k)`:
- piece 0 has weight `λ_0 = √(eta² + (z_1−1)²)`, placed at height 1;
- piece N has weight `λ_N = √(eta² + (3−z_N)²)`, placed at height 3;
- interior pieces have horizontal length `h` and weight `λ_k`, placed at
  their midpoints;
- `f = λ_0 + 3λ_N + Σ_k λ_k (z_k + z_{k+1})/2` and `Σ λ = 4`.

This was checked against the OSIL expression trees in 60 digits (difference
below 1e-50).

### What failed

Scripts are in `explore/`, logs in `logs/explore_chain*.log`. The first
three values are grid estimates, not bounds.
- **Length-row Lagrangian**, with every chain point restricted to the
  ellipse `|P−A| + |P−B| ≤ 4`: `d(μ*) = 4.408` at the KKT multiplier
  `μ* = 0.0076`, and the best value over μ is about 4.77 (near `μ ≈ −0.2`),
  against `f* = 5.072`. The inner minimizers are short chains, and the
  energy as a function of length is far from convex.
- **Summation-by-parts bound with one global vertical multiplier:** 3.3.
  With a fixed horizontal tension: 1.56. Both are defeated by the end pieces.
- **Exact end pieces plus the continuous catenary bound:** gaps of 1.0e-4,
  2.5e-5, 6.4e-6 and 1.6e-6, an O(h²) loss. This float result led to the
  exact version below.

### Certificate

**Identity.** Let `L = Σ_{k=1}^{N−1} λ_k`, `v_k = V + Σ_{j<k} λ_j` and
`V_k = v_k + λ_k/2`. Then

`Σ λ_k (z_k+z_{k+1})/2 = (V+L) z_N − V z_1 − Σ V_k (z_{k+1} − z_k)`.

This was checked in exact rational arithmetic.

**Pointwise step.** Since `|z_{k+1} − z_k| = √(λ_k² − h²)`,

`−V_k Δz_k ≥ −|(v_k+v_{k+1})/2| · √((v_{k+1}−v_k)² − h²)`, where
`v_{k+1} − v_k = λ_k ≥ h`.

**Lemma (discrete catenary calibration).** Let `h, H' > 0`. Define
`τ = asinh(h/2H')`, `G(v) = (v√(H'²+v²) + H'² asinh(v/H'))/2` and
`c = 2G(h/2)`. Then for all `b − a ≥ h`,

`|(a+b)/2| · √((b−a)² − h²) ≤ G(b) − G(a) − c`,

with equality when `asinh(b/H') − asinh(a/H') = 2τ`.

*Proof.*
1. Scale so that `H' = 1`. Write `a = sinh φ_a`, `b = sinh φ_b`,
   `S = (φ_a+φ_b)/2`, `D = (φ_b−φ_a)/2 > 0`, `u = |sinh S|` and
   `X = sinh D cosh D`.
2. The claim becomes
   `D − τ + (1+2u²)X − sinh τ cosh τ − 2u cosh D · √((1+u²)sinh²D − sinh²τ) ≥ 0`.
3. Apply AM–GM with weight `tanh D`. This bounds the left side below by
   `f(D) = D − τ − sinh τ cosh τ + sinh²τ coth D`.
4. `f(τ) = 0`, and `f'(D) = 1 − sinh²τ/sinh²D` changes sign at `τ`, so
   `f ≥ 0`. ∎

A float random check over 4 million cases agrees.

**Theorem.** For every feasible point and every `V` and `H' > 0`:

`f ≥ B := λ_0 + 3λ_N + (V+L) z_N − V z_1 − G(V+L) + G(V) + (N−1)c`,
with `L = 4 − λ_0 − λ_N`.

*Proof.* Apply the lemma to each interior pair `(v_k, v_{k+1})` and
telescope. ∎

Because `V` and `H'` are arbitrary, they may depend on `(z_1, z_N)`. No
bounds on the interior heights are used.

**Why it is exact.**
- At the discrete optimum the horizontal tension `H` is constant on the
  interior pieces.
- Consecutive midpoint tensions are `H sinh(θ_0 + 2kτ)` with
  `H' = √(H² − eta²)`, so the lemma holds with equality all along the
  optimal chain.
- `B` at the KKT end values equals the KKT value to about 40 digits.

**End window.** The remaining problem is `min over (z_1, z_N)` of
`max over (V, H')` of `B`, solved by a 2-D interval branch and bound
(`chain_bound.py`).
- **Domain:** `z_1 ∈ [−2−h, 4+h]`, `z_N ∈ [−h, 6+h]`. This follows from
  `L ≥ (N−1)h`.
- **Infeasible boxes:** discarded when they violate
  `L ≥ √((1−h)² + (z_N−z_1)²)`, the chord condition.
- **Multipliers:** computed per box by a closed-form 1-D monotone equation.
  Validity does not depend on this choice.
- **Box bounds:** the larger of the natural extension and a mean-value form.
  The gradient formulas match 60-digit finite differences to 1.5e-20.
- **Target:** `f_KKT − 1e-14`.

### Results

| instance | our dual | primal (KKT, 60 digits) | boxes | time |
|---|---|---|---|---|
| chain50 | 5.072261493982863 | 5.0722614939828723164 | 11,121 | 13 s |
| chain100 | 5.0697846107387505 | 5.0697846107387605575 | 15,329 | 18 s |
| chain200 | 5.068917341793162 | 5.0689173417931710002 | 21,057 | 25 s |
| chain400 | 5.068621694604009 | 5.0686216946040190144 | 27,843 | 34 s |

- There are no unresolved leaves.
- The primal vectors (`logs/chainN_primal.txt`) are double-rounded, with row
  violations of at most 3.6e-16.
- The listed primal values are optimal to their printed digits.

**What was checked:** the structure, the objective decomposition, the
identity, the gradients, the lemma (proof plus random check), the branch and
bound, and primal feasibility.

## 3. catmix100/200/400/800 (COPS catalyst mixing)

### Structure

Variables:
- `u_0..u_N ∈ [0,1]`;
- states `x1`, `x2`, free except `x1_0 = 1` and `x2_0 = 0`.

Objective and rows:
- objective `x1_N + x2_N − 1`, where the −1 is the OSIL objective constant;
- rows `P(u_{i+1}) x_{i+1} = Q(u_i) x_i`, with
  `P(u) = [[1+au, −bu], [−au, ep+cu]]` and `Q(u) = [[1−au, bu], [au, em−cu]]`.

Constants:
- `a = 1/(2N)`, `b = 10a` and `ep, em = 1 ± a`;
- `c` is `9a` up to a float artifact (for example 4.5000000000000005e-2); it
  is used exactly as written.

Consequences:
- `det P > 0` on [0,1], so the states are functions of the controls.
- With `y_i = Q(u_i)x_i` we have `y_i = M(u_i) y_{i−1}`, where
  `M = Q adj(P)/det P` is entrywise nonnegative (checked). So `y` stays in
  the positive quadrant, and the problem is linear and homogeneous in `y`.
  The separator is effectively the 1-D ray `θ = y_2/(y_1+y_2)`.
- The objective is at least −1 because `x ≥ 0`.

### Primal

- A local solve from a smooth start reproduces the MINLPLib value
  −0.04806939757 (N=100). That point is a saddle: its reduced Hessian has an
  eigenvalue of −2.5e-8.
- The float-DP policy followed by L-BFGS-B gives this pattern: `u = 1` for
  14/28/55/109 steps, then controls alternating between about 0.4543 and 0
  (chattering, an artifact of the trapezoidal rule), then `u = 0` to the end.
- Objective values are for the exactly feasible point with these float
  controls, enclosed by 60-digit interval simulation
  (`logs/catmixN_primal.json`):
  - N=100: −0.0480694320309596
  - N=200: −0.0480591455801144
  - N=400: −0.0480565477566116
  - N=800: −0.0480559013308475 (from `_snap`)
- Double-vector row violations are at most 1.05e-16.

### Certificate

**Concavity.** The value functions are
- `V_{N−1}(y) = min_u (1,1) P(u)^{-1} y`;
- `V_{i−1}(y) = min_u V_i(M(u) y)`;
- `J* + 1 = min_{u_0} V_0(Q(u_0) x_0)`.

Each is a minimum of linear functions of `y`, so it is concave, positively
homogeneous and superadditive.

**Chord lower bounds.** Take grid rays `r_k = (1−θ_k, θ_k)` covering
`θ ∈ [0,1]`. The `θ_k` are dyadic, so `1 − θ_k` is exact. If
`w_k ≤ V_i(r_k)`, then `W_i(s r_k + t r_{k+1}) = s w_k + t w_{k+1} ≤ V_i` for
`s, t ≥ 0`.

**Recursion.** `w_j^{(i−1)}` is set to a rigorous lower bound of
`min_{u∈[0,1]} W_i(M(u) r_j)`, clipped at 0 (valid because `V ≥ 0`). The
final bound is `min_{u_0} W_0(Q(u_0)x_0) − 1`.

**Per-ray 1-D interval branch and bound over u.** Each subinterval gets a
rigorous lower bound:
- **Chord pieces:** the candidate cones are filtered by exact interval cross
  products. On each chord piece `ℓ_k(Nm(u) r_j)/D(u)` we use the natural
  extension, monotonicity, and a second-order Taylor bound with an interval
  second derivative.
- **Coefficients:** the chord coefficients are computed in a
  cancellation-free form, `α = w_k − σ_k θ_k` and `β = w_k + σ_k(1−θ_k)`.
- **Many cones:** for subintervals spanning many cones, a Lipschitz
  mean-value bound uses `f' ∈ S'·[w] + S·[σ]·Θ'` together with rigorous point
  values.
- **Leaf values:** each stage value is the minimum of the leaf lower bounds.
  The loss against float incumbents is at most 1e-14 per stage.

**Grid.**
- Uniform spacing 1e-5 on [0, 0.1], plus 181 rays on [0.1, 1].
- 4,000 extra rays in the singular-arc band [0.0685, 0.0725].
- A 401-ray window (spacing 1e-7) around the primal trajectory, transported
  backward by the primal controls.
- About 14,080 rays per stage in total.

**Checks.**
- positivity of all maps on [0,1];
- composing the maps along the primal reproduces `J`;
- a randomized self-test: the stage bound never exceeds a dense-sampled
  minimum (margin 1.3e-15).

### Results (`catmix_bound.py N 1e-5 200 1e-7 0.0685 0.0725 1e-6`)

| N | our dual | gap abs / rel | interval evals | time |
|---|---|---|---|---|
| 100 | −0.048069432038882705 | 7.9e-12 / 1.6e-10 | 1.6e8 | 21 min |
| 200 | −0.04805914560067171 | 2.1e-11 / 4.3e-10 | 2.5e8 | 32 min |
| 400 | −0.048056547950296354 | 1.9e-10 / 4.0e-9 | 3.9e8 | 47 min |
| 800 | −0.048055901841076894 | 5.1e-10 / 1.1e-8 | 6.1e8 | 70 min |

**Earlier grid designs (all valid, looser):**
- Uniform 1e-4 (N=100): gap 8.1e-7.
- 1e-5 plus window: gaps 1.1e-9, 1.5e-8, 3.2e-8 and 5.0e-8 for
  N=100/200/400/800.
- A float error profile shows that this loss accumulates only on the
  singular arc, which motivated the band.
- For N=100, a uniform 3e-6 grid gives the bit-identical bound. So the
  remaining 7.9e-12 is probably slack in our primal, not in the bound.

**Engineering failures along the way (all fixed):** a crude multi-cone bound
caused exponential branching; cancellation in the chord coefficients put a
floor of about 1e-13 on the bounds; accumulated transported windows produced
near-duplicate rays.

**Not checked:** there is no independent reimplementation, and the catmix
primal is not proved optimal beyond the stated gaps.

## 4. Mechanism classes and fit with the program principle

**chain.** A Lagrangian on the linear height constraint, with tension
multipliers that depend on the configuration (cumulative mass); an exact
closed-form calibration (a discrete Weierstrass field) along the path; and
one localized exact window, the 2-D end values, by interval branch and
bound. This partly fits the principle: the structure is a path with an
exact window, but the key ingredient is a value-function calibration, not
fixed multipliers. The fixed-multiplier length-row Lagrangian fails because
the length row is effectively reverse-convex.

**catmix.** An exact DP on a 1-D projective separator, made rigorous by
concavity (chord interpolation) and by per-stage exact control minimization.
The certificate amounts to costates localized to cones of states, a
state-localized Lagrangian. It is the fix for the first wave's failed
cell-constant DP: homogeneity reduces the separator to 1-D, and concavity
makes the interpolation error second-order instead of first-order. A
fixed-costate Lagrangian was not tried; the singular arc suggests it would
lose first-order.

## 5. Commands run (targeted only; no CI or project-wide checks)

**chain:** `chain_model.py 50 100`; `chain_bound.py 1e-12 50`;
`chain_bound.py 1e-13 50 100 200 400`; `chain_bound.py 1e-14 50 100 200 400`
(final; `logs/chain_all_run_1e-14.log`, `logs/chainN_bound.json`);
`explore/chain_*` and `explore/calibration_random_check.py`.

**catmix:** `catmix_model.py 100 200`; `catmix_primal.py 100 200 400 800`;
`explore/catmix_primal_{snap,finer}.py`; `catmix_bound.py` with the grids
listed in Section 3 (final logs `logs/catmixN_bound_final.log` and the
matching `*_band*.json`); `explore/catmix_error_profile.py`;
`explore/catmix_stage_lb_selftest.py`.

## 6. Files (in `research-20260929/open-instances-wave2/cops/`)

`chain_model.py`, `chain_bound.py`, `catmix_model.py`, `catmix_primal.py`,
`catmix_bound.py`, `ivx.py`, `osilx.py`; `explore/` (failed and design
experiments); `logs/` (JSON results, primal vectors, controls as `.npy`).

## 7. Independent verification (added by the root, 2026-09-30)

An independent verifier rechecked the results with its own code
([report](../../reviews/cops-verification/verification-report.md)):

- **chain50–400: verified.** The polyline form matches the OSIL model to
  below 1e-50; the summation-by-parts identity holds in exact rational
  arithmetic; the calibration lemma's proof is correct line by line (the
  AM–GM step leaves a perfect square; equality holds exactly when `D = τ`);
  a 200,000-case 50-digit test found a minimum slack of +1.7e-31. The
  verifier's own 2-D interval branch and bound certifies all four dual
  bounds with no unresolved boxes. One non-rigorous squaring in the
  authors' pruning test is negligible and does not affect the result.
- **catmix: verified.** `M ≥ 0` and `P^{-1} ≥ 0` on [0,1] hold exactly
  (including the `c` decimal artifact; also `ep + em = 2`, so
  `M = 2P^{-1} − I`). The verifier's own DP with a different per-ray method
  certifies catmix100 ≥ −0.04806943203114456 (7.7e-12 better than this
  report's bound) and catmix200 ≥ −0.04805914559907277. A 40-digit Newton
  polish finds a KKT point at −0.048069432030979596, so the catmix100
  optimum is bracketed within 1.65e-13. **Correction:** the remark in
  Section 3 that the remaining 7.9e-12 is "probably slack in our primal" is
  wrong; almost all of it was slack in the bound. catmix400/800 duals were
  checked by code reading only in this verification; they were recomputed
  independently later
  ([`../../reviews/catmix-recheck.md`](../../reviews/catmix-recheck.md);
  tighter than claimed).
- **Novelty (brief search):** no prior global certificates found for these
  instances and no equivalent discrete calibration lemma; the closest paper
  (arXiv:2510.20917) treats fixed-link-length chains, a different model.

*Root edit (2026-09-30, closing revision):* the header and Section 7 now
record that `reviews/catmix-recheck.md` recomputed the catmix400/800 dual
bounds independently (tighter than claimed). No bound changed.
