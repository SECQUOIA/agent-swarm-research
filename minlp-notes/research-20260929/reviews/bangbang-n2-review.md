# Review of `theory-bangbang/extension-n2.md` (tangential quadratic calibrations for n ≥ 2)

Date: 2026-09-30. Reviewer: independent, adversarial; I did not produce the work.
Scripts and logs for this review: `reviews/bangbang-n2-review-checks/` and its `logs/`.

## Verdict

**Fixes needed. The main results survive.**

What holds:

- Every proved statement I checked is correct: Lemma 1.1, Lemma 1.3, Theorems 1 and 2,
  Corollary 3, Proposition 4, Proposition 6, Lemma 10 and Corollary 11.
- The Osmolovskii–Maurer (O–M) relation is correct. I checked it against the primary sources.
- Every numerical claim I re-implemented reproduces. This includes the counterexample (example B)
  and the exact rational certificates for example A.

What needs fixing:

1. **Interpretation gap (the substantive issue).** [R, Theorem 4.1] is the transfer theorem the
   calibration program relies on. Its hypothesis (H3) implies the *global-model* inequality.
   - The positive "local" answer (Theorem 2) therefore does not feed into [R, Theorem 4.1] when
     the global model fails.
   - Theorem 2's own local calibrations violate the far-region condition (F) of Proposition 12,
     both in example C and in example A.
   - For LQ data, Proposition 13 ("(H5) automatic") holds only for global-model calibrations. The
     Summary drops that qualifier.
   - In example C, **no** calibration satisfies [R]'s (H3). I checked this with a comparison
     argument that starts from the largest admissible value at the switch.
2. **Numerical error, minor.** The continuous blow-up distances for example B were read off an
   output grid, not the integrator's event. The correct value is `5.754e-3`, not `5.87e-3`; the
   other entries in Section 6.4 change similarly. The conclusions stand. Agreement with the
   discrete break time improves; agreement with the leading-order prediction worsens.
3. **Simplification.** Theorem 1 has a three-line proof: one-sided [R, Proposition 3.1] plus
   Lyapunov comparison. Its hypotheses already imply tangency, so the remark "no tangency is
   assumed" needs rewording.
4. **Several wording fixes.** See the issue list.

## What I checked and how

- **Continuous quantities** (`v_exact_cont.py`): exact symbolic computation (sympy, rational
  data). The cost of switching at `θ` is an exact polynomial in `θ`; `τ` is a root of `F'`, taken
  to 40 digits; `F''(τ)` is computed exactly. `σ` comes from the adjoint equations. `Q` is solved
  in closed form: `Q11 = q(T−t)`, `Q12 = q(T−t)²/2`, `Q22 = ρ + q(T−t)³/3 − c(T−t)`. The O–M form
  `Ω` is computed separately, by integrating the linearized state, without `Q`. The author used
  numpy polynomials and finite differences.
- **Singular Riccati** (`v_riccati.py`, `v_riccati_sens.py`): integrated in plain time (Radau,
  LSODA, DOP853) and in log time, with several blow-up thresholds. The author integrated in log
  time only.
- **Discrete side** (`v_discrete.py`), written from the problem statement:
  - Euler states written explicitly as affine functions of `u`, so `J(u)` is an exact quadratic
    with a closed-form Hessian;
  - KKT points found by *enumeration* (bang-bang, then a run of 0–2 interior stages, then
    bang-bang), with every sign condition checked;
  - my own derivation of the stage quadratic and of the maximal recursion;
  - my own face-enumeration box minimum.
- **Exact certificate** (`v_certify.py`): Fraction arithmetic over my own KKT point, costates and
  family, with the reachable box and exact face enumeration.
- **Theorem 2 and Proposition 4 instance** (`v_localtsqc.py`, `v_localtsqc_by.py`, `v_prop4.py`):
  I built the local construction of Theorem 2 for examples C and A and checked (A), (G-local), the
  sign of `bᵀy`, the tube radius, the [R] (H3) margin, and the far region over the continuous
  reachable box.
- **Lyapunov control** (`v_lyap_margin.py`): the (W5) margin of the negative-control family.
- **Author's code**: I reran `n2_certify.py A 200 1000` in a scratch directory; the gaps match
  the logs. I also instrumented `model.singular_riccati_after` to locate the blow-up discrepancy.
- **Sources**: I fetched Osmolovskii–Maurer RB 2007/85 and Maurer–Osmolovskii, Control Cybern.
  32(3) (2003), and ran a brief web search on novelty.

## Claim-by-claim results

| Claim | Result |
|---|---|
| Lemma 1.1 (vertex reduction), Lemma 1.3 | Correct. Checked the affine-in-`λ` reduction, the Schur step (valid since `2|σ|Δ > 0` for `t ≠ τ`), and the local tube argument. |
| Theorem 1 (`η_L < 0` ⇒ no `C³` exact calibration on a uniform tube after `τ`) | Correct. The proof is valid, but a much shorter one exists (issue 3). |
| Theorem 2 (existence when `η_L > 0`, local version, linear rate) | Correct. Checked the `φ` profile, `bᵀy > 0` on both parts, the Weyl step for `G_m`, the boundedness argument, and the pre-switch Picard step. Numerical instances for C and A confirm it (below). |
| Corollary 3 | Correct. Theorem 1 needs `C³` in `(t,x)`; a quadratic `S` with piecewise-`C¹` `P` and upward jumps is not literally covered, but the argument goes through. Worth one sentence. |
| Proposition 4 (bound `Q_ε − β_εβ_εᵀ/η_ε`; attained up to `O(δ_1)`) | Correct. Numerically the construction attains the bound at rate `O(δ_1²)`, better than claimed. |
| Section 2.5 (layer asymptotics) | Algebra correct: `η(s) = η_1/(1 + κη_1 log(s_1/s))`, `s_b = s_1 exp(−1/(κ|η_1|))`, exponent `2D/(Δ²|η_1|) > 2` under SSC. "Matches numerics" is overstated after the blow-up correction (issue 5). |
| Proposition 6 (`F''(τ) = D + Δ²η_L`) | Correct. Exact agreement to 40 digits in all five examples, and `Ω(O–M) = F''` exactly. One typo in the proof (issue 10). |
| O–M relation (jump with `D(H)` set to 0) | Correct. Checked against the primary source (see below). |
| Corollary 7 and example B | Correct, given the cited SSC theorems. Example B's data verified exactly. |
| Theorem 8 (global model, `N = 0`) | Sketch, correctly labelled. The failure of the global model in example C is now established by comparison from the largest admissible `P(τ)` (below). |
| Theorem 9 (several switches) | Sketch, correctly labelled. The induction outline is plausible. At each switch, tangency plus `P ⪯ P_max` gives `η_j = bᵀ(P_max − P)(τ_j+)b ≥ 0` directly. |
| `N ≠ 0`: no maximal solution | A remark without an example. The report's "need not exist" is fine; the author's summary says "ill-posed", which is stronger than what is shown. |
| Lemma 10, Corollary 11 | Correct. Checked the vertex and fractional-stage conditions, the Schur form, the Bellman (min over `v`) form, monotonicity, and that the failing point has `d = 0`. |
| Proposition 12 | Correct as a conditional statement. Its hypotheses are not met by the report's own local constructions (issue 1), and its `C²`-in-`t` hypothesis is not met by Theorem 2's `P` (issue 9). |
| Proposition 13 | Correct *with (G-global)*, as its proof states. The Summary's unqualified wording is wrong for local calibrations (issue 1). |
| Numerics (Section 6) | All re-implemented items reproduce, except the continuous blow-up distances (issue 2). |

### Theorem 1: correct, but it follows in three lines

The hypotheses ("`C³` in `(t,x)` on `{τ < t ≤ T, |x−x*(t)| < r_0}` with bounded derivatives up to
order 3") already force tangency:

1. `S`, `S_t`, `S_x`, `S_xt` and `S_xx` extend continuously to `t = τ`, and so do `r` and `∇_x r`.
2. `r(τ+, x*(τ), u) = σ(τ)(u − u_b) = 0` for every `u`, and `r(τ+, ·, u) ≥ 0` near `x*(τ)`. So
   `∇_x r(τ+, x*(τ), u) = 0` for both vertices. This is [R, Proposition 3.1] applied to the right
   limit, and it gives `β(τ+) = 0`.
3. Step 2 of the report's proof gives `P ⪯ Q_ε` on `(τ,T]`, hence `X := Q_ε(τ+) − P(τ+) ⪰ 0`. With
   `P(τ+)b = w` this gives `η_ε = bᵀXb ≥ 0`.

The blow-up argument (steps 3–4) is valid and explains the *mechanism*. The result itself,
however, is [R, Proposition 3.1] plus Lyapunov comparison. Two consequences:

- The remark "No tangency is assumed" should say that tangency is *implied* by the hypotheses.
- "Tangential or not" in the Summary is vacuous.

The same observation shows that in Proposition 4, `η_ε ≥ 0` does not need Theorem 1.

### Relation to Osmolovskii–Maurer: checked against the primary sources

- **RB 2007/85** (downloaded from the cited RCIN link):
  - eq. (94) defines `D^i(H) = −(d/dt)(Δ_iH)|_{τ_i+0}`;
  - eq. (151) gives the form `Σ D^i(H)τ̄_i² − 2[H_x]^i x̄^i_av τ̄_i + ∫⟨H_xx x̄,x̄⟩ + d`;
  - eq. (156) states its equality with `Ω`, via `ξ = −τ̄`.

  The report's citations are accurate. With `D = γΔ`, `[H_x] = −wΔu` and `[ẋ] = bΔu`, I get
  `Ω = (D + Δ²η_L)ξ²`, in exact agreement with `F''(τ)` in all five examples.
- **Maurer–Osmolovskii, Control Cybern. 32(3) (2003)**
  ([PDF](http://matwbn.icm.edu.pl/ksiazki/cc/cc32/cc3238.pdf)):
  - eq. (47): `q_{k+} = ([ẋ]^k)*Q^{k+} − [ψ̇]^k`, `b_{k+} = D^k(H) + q_{k+}[ẋ]^k`;
  - eqs. (56)–(57), Proposition 4.3, attributed to Osmolovskii–Lempio 2002: jump condition
    `b_{k+}[Q]^k = (q_{k+})*(q_{k+})`;
  - Theorem 4.4 (fixed `x_0`, one switch): condition `b_1 = D^1(H) + ([ẋ]¹)*Q(τ_1)[ẋ]¹ − [ψ̇]¹[ẋ]¹ ≥ 0`
    plus a terminal condition.

  These are exactly the report's formulas. In this setting `b_1 = D + Δ²η_L`. The report's
  sentence "I derived it from the quadratic form above and did not check it against those
  papers" can be upgraded to "checked": cite eqs. (47), (56)–(57) and Theorem 4.4.
- **The "`D(H)` set to 0" identity** `β_Lβ_Lᵀ/η_L = qqᵀ/(qᵀ[ẋ])` is exact algebra, since
  `q = Δu·β_L`. So is `β(τ−) = β_L·D/(D + Δ²η_L)` for the O–M solution.
- **Agrachev–Stefani–Zezza** (SIAM J. Control Optim. 41 (2002) 991–1014) appears with these
  details in the reference list of RB 2007/85. The citation is correct; I did not read the
  theorem itself.

### Example B (counterexample): data verified exactly

- `τ = 1.1980270`, `η_L = −0.429054`, `D = 3.066023`, `F''(τ) = 1.3498072`. The difference
  `F'' − (D + 4η_L)` is `5e-41`.
- The switch is regular: `σ̇(τ) = 1.5330`.
- PMP signs hold. `min|σ(t)|/|t−τ| = 0.0605`, attained at `t = 0`, where `σ(0) = −0.0725`.
- So `−D/Δ² < η_L < 0`. The SSC holds via Maurer–Osmolovskii Theorem 4.4 and the ASZ/O–M
  sufficiency theorems. Theorem 1 excludes every `C³` calibration on a uniform tube.

The refutation of the reading "`P̂` bounded = no conjugate point" stands. Two caveats:

- The bang-bang grid search is only supporting evidence. Local optimality is what the argument
  needs, and it comes from the SSC.
- The margin `σ(0) = −0.0725` is small but nonzero, so strict bang-bang holds.

### Example C: the global model fails for *every* calibration, not just the ones tried

The report's evidence is that particular continuations blow up before `τ`. I strengthened it:

- By Proposition 4, every tangential `P` satisfying (A) and (T) has
  `P(τ) ⪯ P_max := Q_ε(τ+) − β_εβ_εᵀ/η_ε`.
- The backward singular Riccati equation on `[0,τ)` is a relaxed-LQ Riccati equation, so it is
  monotone in its data at `τ`.
- Started from `P_max`, it blows up at `t = 0.352` (`ε = 0`) and `t = 0.496` (`ε = 0.02`)
  (`logs/v_riccati.json`). This is consistent with the report's `0.46` and `0.72` from smaller
  starting values.
- Hence no global-model calibration exists for C, even with `ε = 0`.

For example A the same test does not blow up, consistent with the report.

## Numerical reproduction

| Item | Report | Independent result |
|---|---|---|
| `τ, η_L, D, F''`: A | 1.31546, +1.0475, 3.2823, 7.4724 | 1.315455, +1.047533, 3.282258, 7.472390 (exact) |
| same: A0 / B / B2 / C | see report table | all agree to the digits shown |
| strict bang-bang ratio A / B | 1.2 / 0.06 | 1.206 / 0.0605 |
| reduced Hessian, A, `N = 200` | 7 negative, min −1.1e-3 | 7 negative, min −1.109e-3 (dense closed form; checked against `σ` differences to 1e-17). At `N = 500`: 11 negative. |
| reduced Hessian, A0, `N = 200` | positive definite, min 3.0e-5 | positive definite, min 2.98e-5 |
| two adjacent interior stages | A0 at `N = 50, 200, 500, 1000, 5000`; B at `N = 500` | same; each KKT point is the only one found by the one-switch enumeration |
| float screening A: rmax / Lyap failing stages, `N = 500, 1000, 2000, 4000` | 0 / 217, 434, 867, 1736 | identical, same stage ranges. A0: 0 / 259, 520, 1041, 2082 |
| exact certificate A, `J − B` | ≤ 3.0e-25 for `N = 50 … 5000` | 3.3e-29, 5.7e-28, 1.7e-27, 1.4e-26, 5.8e-26, 2.5e-25 (`N = 50, 200, 500, 1000, 2000, 5000`); no stage loss > 1e-20 |
| negative control (Lyap, A, `N = 1000`) | 3.96, 434 stages | 3.9585, 434 stages |
| A0 certificate | ≤ 2.4e-25 | 3.7e-28 (`N = 200`), 8.7e-27 (`N = 1000`) |
| B discrete break (stages after switch), `ε = 0` | 2, 3, 6, 11, 23, 46 | identical |
| same, `ε = 0.02` | 4, 6, 13, 26, 53, 106 | identical |
| B continuous blow-up, global model, `ε = 0` / `0.02` | 5.87e-3 / 1.33e-2 | **5.754e-3 / 1.321e-2** |
| B local model, `δ_0 = 0.2 / 0.1`, `ε = 0` | 4.08e-3 / 2.46e-3 | **4.006e-3 / 2.396e-3** |
| B local model, `δ_0 = 0.2 / 0.1`, `ε = 0.02` | 9.25e-3 / 5.48e-3 | **8.63e-3 / 4.99e-3** |
| B2 continuous blow-up | 3.5e-7 | 3.38e-7 |
| B2 discrete break before the switch, `N = 1000, 4000, 16000` | 408, 25, 4 | same break stage; my count at `N = 16000` is 5 because I index the pure bang-bang switch differently |
| C discrete recursion, `ε = 0` | never breaks; `max|P|` 4.6, 10.2, 11.0 at `N = 1000, 4000, 16000` | never breaks for `N = 500 … 16000`; same values, but 22.7 at `N = 2000` and 88 at `N = 8000` (issue 6) |

The blow-up discrepancy has a definite cause. `model.singular_riccati_after` returns
`exp(r2.t[-1])`, which is the last point of a 300-point `t_eval` grid (log spacing ≈ 0.10), not
the event time `r2.t_events`. With an instrumented run, the event is at `s = 0.0057536` while the
returned value is `0.0058721`. The returned value also changes with `s_top`: 5.87e-3, 5.82e-3 and
5.84e-3. My value is stable to 7 digits across three integrators and thresholds from 1e6 to 1e10.

## Theorem 2 instance and the far region

Construction for example C (`ε = 0.02`, `δ_1 = δ_0 = 0.02`; here `λ = 1`, so the profile is
linear):

- `min bᵀy = 0.187 > 0` in the layer, and `max|P| = 5.5`;
- (A) holds on all sampled times, and (G) holds on `|t−τ| ≤ δ_0`, both up to 1e-14;
- `P(τ)b = w` to 3e-11;
- uniform tube radius `r_1 = 0.077`.

With `ε = 0.01` and `δ_1 = 0.01`, `r_1 = 0.037`. So a local TSQC exists for C, as Theorem 2
says, although the global model fails.

For example A (`δ_1 = 0.02`, `λ = 0.42`) the construction also works at every sampled time. The
integrator's trial stages at the kink of `φ'` briefly showed `bᵀy < 0`; at `δ_1 = 0.005` this
does not happen. Proposition 4: `|P(τ) − P_max|` equals 2.9e-2, 6.4e-3, 1.5e-3, 3.7e-4 and
9.2e-5 for `δ_1 = 0.04, 0.02, 0.01, 0.005, 0.0025` in C, and `P(τ) − P_max ⪯ 0` up to rounding.

The same calibrations fail the conditions the program needs downstream:

- **[R] (H3) margin.** `|σ| > Δ|β|²/(2μ)` with `μ = λ_min(r_xx)` fails at 2309 of 3000 sampled
  times for C (minimum −1.0e3), and also for A (minimum −70). This is expected: after the layer
  `P = Q_ε`, so `M = 2εI` while `|β|` is of order 0.5–1.
- **Far region (F).** The minimum of `r(t,x,u)` over the continuous reachable box `D_t` and
  `u ∈ U` is −4.5 for C and −6.6 for A. So these local calibrations are not calibrations on the
  reachable set. For A the certificate works only because it uses the global-model-type discrete
  family (rmax).

## Issues (most important first)

1. **The local result does not connect to [R, Theorem 4.1]; state this.**
   - (H3) of [R, Theorem 4.1] (`∇²_x r ⪰ μI` for all `u`, plus the margin `|σ| > Δ|β|²/(2μ)`)
     implies `M(t,u°) − (Δ/(2|σ|))ββᵀ ≻ 0` for all `t ≠ τ`, i.e. (G-global). So [R]'s transfer
     theorem needs a global-model calibration.
   - In example C none exists (comparison from `P_max`, above), so [R, Theorem 4.1] cannot be
     applied to C with any `S`, although `η_L > 0`.
   - Theorem 2's local calibrations also violate (F) in both C and A (above), so Proposition 12
     does not apply to them either.
   - Fixes:
     - (a) In the Summary and Section 7, qualify "for LQ-structured data (H5) is automatic" as
       "for global-model calibrations (G-global)". Proposition 13's proof already uses (G-global).
     - (b) Replace or qualify "The local formulation avoids both problems" (Summary item 3):
       it avoids them for the continuous existence question only.
     - (c) Add an open item: a transfer theorem for local calibrations, with a small ball
       radius and (W4) at that radius, in which the far region is the real obstruction.

   Example C's discrete maximal recursion (exact in float at `ε = 0`) is then the only
   certification route shown for C.
2. **Continuous blow-up distances (Sections 2.5, 6.4, Summary).** Replace:
   - `5.87e-3` → `5.75e-3`, and "0.0059" in the Summary → "0.00575";
   - `1.33e-2` → `1.32e-2`;
   - `4.08e-3 / 2.46e-3` → `4.01e-3 / 2.40e-3`;
   - `9.25e-3 / 5.48e-3` → `8.63e-3 / 4.99e-3`.

   Also fix `singular_riccati_after` to return `t_events`. After the fix, the discrete break time
   (0.00575 and 0.01325) agrees with the continuous value (0.005754 and 0.01321) to within one
   stage at `N = 16000`.
3. **Theorem 1.**
   - Give the short proof, or at least note that the hypotheses imply `β(τ+) = 0`. Then
     `η_ε = bᵀ(Q_ε − P)(τ+)b ≥ 0` follows directly.
   - Reword "No tangency is assumed" and "tangential or not".
   - The Summary says "`C³` in the state"; the theorem needs `C³` in `(t,x)` with bounded
     derivatives up to order 3 on the tube after `τ`.
4. **The Lyapunov negative control is not a clean instance of the non-tangential window law**
   (Section 6.2).
   - Its failure covers the whole last arc plus 0.18 before `τ`.
   - For the continuous `Q_ε` family, (W5) fails on `t ∈ [0.35, 2]`, with `|β| = 0.99–1.69` on
     the last arc (`logs/v_lyap_margin.log`). So the failure is mostly a margin (far-field)
     failure, not the switch effect of [R, Theorem 2.3(2)].
   - Keep it as a negative control, but drop "the non-tangential case of the window law", or
     say both effects are present.
5. **"Matches numerics" in Section 2.5 and the status table is overstated.** With corrected
   blow-up values, the leading-order predictions for B are off by a factor of 1.4 (`δ_0 = 0.2`:
   5.6e-3 vs 4.0e-3) and 1.2 (`δ_0 = 0.1`: 2.8e-3 vs 2.4e-3). Say "same order; within a factor
   1.4".
6. **Example C, discrete recursion (Section 5, Remarks).**
   - "`max|P|` grows with `N` (4.6, 10.2, 11.0)" lists only the `N` whose KKT point has no
     interior stage. At `N = 2000` and `8000`, where there is one, `max|P|` is 22.7 and 88.
   - The `ε = 0.02` breaks happen exactly at those `N`.
   - Report the full sequence and the link to the fractional stage (`m_t = κ_t` there).
7. **Example B2 (Section 6.5).** "The `Θ(1/h)` signature … appears only once `h` is below the
   layer width" is an untested extrapolation; label it as expected behaviour. (At `ε = 0.02` the
   B2 recursion breaks 8 stages before the switch at `N = 500` and 0–3 stages before it for
   `N = 1000 … 16000`; not in the report.)
8. **Corollary 11 and Summary: "0.00575 after the switch for every `N` from 1000 to 16000".** The
   measured values are 0.006, 0.006, 0.0055, 0.00575 and 0.00575. Say "within one stage of
   0.00575".
9. **Proposition 12 hypothesis.** "`S ∈ C²` in `(t,x)`" needs `P ∈ C²` in `t`. Theorem 2's `P`
   is only piecewise `C¹`: `Ṗ` has kinks at `τ ± δ` and a jump at `τ`. Either state that a
   smoothed `P` is needed, or replace step 2 by the averaged expansion
   `ρ_t = ∫_{t_t}^{t_{t+1}} r(s,x,u) ds + O(h²)`, which needs only piecewise-continuous `S_t`.
10. **Small errors.**
    - Proposition 6 proof: for `ξ < 0` the deviation on `[τ−|ξ|, τ]` is `d = bω(t − τ + |ξ|)`,
      not `bω(τ − t)`. The integral is unchanged.
    - Corollary 3: note that jumps in `P` are allowed; the Theorem 1 argument covers them
      because upward jumps only help.
    - Proposition 4: `η_ε > 0` should be `η_ε ≥ 0` (strictly positive under the margin).
11. **O–M line.** Upgrade "derived here; O–M's published form taken from [V], not re-checked" to
    "checked against Maurer–Osmolovskii (2003), eqs. (47), (56)–(57) and Theorem 4.4".

## Novelty wording

The report makes no explicit novelty claim. Classical ingredients are attributed correctly: the
O–M quadratic form, the Riccati test with rank-one jumps, and the ASZ/O–M sufficiency theorems.

A brief web search found no prior statement of:

- Theorems 1–2 (smooth calibrations exist near a regular switch iff `η_L > 0`);
- the "`D(H)` set to zero" reading of the maximal tangential Hessian;
- the counterexample to the reading "bounded `P̂` = no conjugate point".

These are elementary; Theorem 1 in particular is [R, Proposition 3.1] plus Lyapunov comparison.
If a novelty sentence is added, it should say "not found in a brief search; elementary". Two
missing citations are worth adding:

- Maurer–Pickenhain (1995), the Riccati/quadratic verification-function approach that
  Maurer–Osmolovskii (2003) extend to broken extremals;
- the Noble–Schättler line on broken extremals and value functions with switching surfaces,
  which is relevant to the report's remark that only nonsmooth calibrations remain when
  `η_L < 0`.

## Not checked

- The cmax, clin and clin+3h screening families. I re-implemented only rmax and Lyap.
- The finite-difference logs in `explore_family.log`. They are superseded by the exact
  computation.
- The A0 leading-order check `η(10⁻¹⁴) = 0.0106`.
- The full induction for Theorem 9 and the singular-point comparison for Theorem 8. Both are
  labelled sketches.
- The statements of the ASZ (2002) theorems themselves.

## Commands run

All runs used `OMP_NUM_THREADS=1` (and `OPENBLAS_NUM_THREADS=1` for the numpy-heavy scripts),
from `reviews/bangbang-n2-review-checks/` unless noted. These are targeted checks only: no
project-wide verification, no CI inspection, no commits. Each run took a few minutes at most.

1. `python3 v_exact_cont.py` → `logs/v_exact_cont.{log,json}`
2. `python3 v_riccati.py` → `logs/v_riccati.{log,json}`; `python3 v_riccati_sens.py` →
   `logs/v_riccati_sens.log`
3. The author's `model.singular_riccati_after`, run inline, with `solve_ivp` instrumented to
   print `t_events` (no files written in the author's directory).
4. `python3 v_discrete.py hess | kkt | rmaxB | windows 500 1000 2000 4000` →
   `logs/v_discrete_*.{log,json}`
5. `python3 v_certify.py A:50:rmax A:200:rmax A:500:rmax A:1000:rmax A:2000:rmax A:1000:lyap A0:200:rmax A0:1000:rmax`,
   then `A:5000:rmax` → `logs/v_certify.{log,jsonl}`
6. `python3 v_localtsqc.py`, `python3 v_localtsqc_by.py`, `python3 v_prop4.py` →
   `logs/v_localtsqc*.{log,json}`, `logs/v_prop4.{log,json}`
7. `python3 v_lyap_margin.py` → `logs/v_lyap_margin.log`
8. The author's `n2_certify.py A 200 1000`, run in `/tmp/n2run` with `PYTHONPATH` set to the
   author's `n2/`. Gaps 1.34e-26 and 8.53e-27 match `logs/n2_certify.jsonl`.
9. Web: RB 2007/85 PDF (`pdftotext`, eqs. (94), (151), (156)); Maurer–Osmolovskii 2003 PDF
   (eqs. (47), (56)–(57), Theorem 4.4); searches on verification functions and broken extremals.

## Sources

- N. P. Osmolovskii, H. Maurer, Research Report RB/85/2007, IBS PAN,
  [PDF](https://www.rcin.org.pl//Content/217459/PDF/RB-2007-85.pdf).
- H. Maurer, N. P. Osmolovskii, *Second order conditions for bang-bang control problems*,
  Control Cybern. 32(3) (2003), [record](https://geodesic.mathdoc.fr/item/CC_2003_32_3_a8/),
  [PDF](http://matwbn.icm.edu.pl/ksiazki/cc/cc32/cc3238.pdf).
- N. P. Osmolovskii, F. Lempio, *Transformation of quadratic forms to perfect squares for broken
  extremals*, Set-Valued Anal. 10 (2002) 209–232 (cited via Maurer–Osmolovskii 2003).
- Noble–Schättler, broken extremals: [thesis record](https://www.mathgenealogy.org/id.php?id=38317);
  related [arXiv 1709.07775](https://arxiv.org/pdf/1709.07775).
