# Confirmation review (round 3) of `theory-bangbang/singular-arcs.md`

Date: 2026-09-30. Reviewer: fresh, independent referee. I did not write the
note, its scripts, or the earlier reviews (`reviews/singular-arcs-review.md`,
`reviews/singular-arcs-confirm-r1.md`, `reviews/singular-arcs-confirm-r2.md`).

Scope:

- check the two round-3 items (S1, S2) and the reviser's report from
  scratch;
- recompute what changed;
- judge the two items the reviser did not apply;
- check that nothing was strengthened.

Checks were targeted and run with `OMP_NUM_THREADS=1`, `timeout` and
`PYTHONDONTWRITEBYTECODE=1`. I ran no project-wide verification, did not
inspect CI, and committed nothing. I did not touch the note or its logs. My
scripts and logs are in `reviews/singular-arcs-confirm-r3-checks/`.

## Verdict

**Verified.**

- S1 is fixed as reported. I rechecked every mathematical statement in the
  new text with code that does not share anything with the reviser's
  `revision3_semilinear.py`: the E2 gauge, the catmix reachable set and
  change of variable, the singular-point equation, and both Kelley
  quantities. I also checked numerically that the continuous costs agree in
  both reformulations, and that for E2 the Euler costs differ by
  `O(h²)` per stage, as the new "Not tested" bullet says.
- S2 is fixed as reported. My rerun of Part K reproduces the new log line
  for line. Once the labels are swapped, it also matches the Part K lines of
  the old log.
- Both refusals are acceptable.
- Nothing was strengthened. The new text withdraws a false claim and adds
  caveats.
- Two optional wording nits are listed in Section 2. Neither affects
  correctness.

## 1. What I checked

| item | check | result |
|---|---|---|
| S1, E2 gauge (Remark 3.5, Section 11) | `e1` (sympy, exact) | With `F = −k₁x₁²/2 − k₂x₁x₂`: new `ℓ_1 = 0`; new `ℓ_0 = (x₁² + x₂²)/2 − k₂x₁(x₁ − x₂)`; new terminal cost `½(k₂x₁² + 2k₂x₁x₂ + (1 − 2k₂)x₂²)`, which does not contain `k₁`; constant `F(x₀) = −k₁/2`. With a cost state, the input column is `(0, 1, 0)`, which does not depend on the state, so `w ≡ 0`. Kelley quantity from a separate closed formula (for constant `b`, `ℓ_1 = 0` and linear drift, `K = bᵀℓ_{0,xx}b`): `1 − 2k₂`. This agrees with the reviser's value, which was computed from the Hamiltonian flow |
| S1, E2 costs (float) | `e1` | Continuous: for a random control, `J_old − (J_new + F(x₀))` is `5e-12` to `1.2e-10` for `k₁ = −½, 0, +½` (ODE tolerance). Euler, N = 100, random control: `J_new + F(x₀) − J_old` equals `−½h²Σ_t g_tᵀ∇²F g_t` to `1e-15`. This is exact because `F` is quadratic. It confirms "differ from the tested ones by `O(h²)` terms per stage" |
| S1, catmix reachable set | `e1` (sympy, and float ODE runs) | `θ̇ = u` at `θ = 0` and `θ̇ = 10(u − 1)/121` at `θ = 1/11`. `b(1/11) = 10/121`, `b' = −10 − 2θ < 0`, and the positive root of `b` is `√26 − 5 = 0.09902 > 1/11`. Over five random controls and constant `u = 0` or `1` (run for 50 time units), `θ` stays in `[0, 1/11]`, and `u = 1` converges to `1/11` |
| S1, catmix `ξ` formulation | `e1` (sympy) | After the gauge `dF/dξ = −θ`: `ℓ_1 = 0`, input column 1, and `ℓ_0 = θ(11θ − 1)/b`. The numerator of `dℓ_0/dθ` is `−(111θ² − 22θ + 1)`. On the arc the gauged costate is `bψ_θ + θ = 0`, so `K = ℓ_{0,ξξ} = b²ℓ_0''` at `θ_s`, which gives `2√10`. This formula is independent of the reviser's flow computation. Float: for five random controls, `C = ∫(−θ + θu)dt` equals the gauged cost `∫ℓ_0 dt − F(ξ(1)) + F(ξ(0))` to `4e-15` |
| S1, text | read Remark 3.5, Summary (novelty list), Sections 6, 7, 10 (refusal item) and 11; grep for "outside", "every gauge" and "semilinear" | The claim "in every gauge" is withdrawn in all three places. Every remaining "outside" is restricted to the formulations used in the note. The `w ≡ 0` formulations are said to lie inside the class *as read* (the 2005 definition, according to the second review). Their Euler transcriptions are marked as untested, and Felgenhauer's other hypotheses as unchecked. The E2 example (bang–singular, not bang–singular–bang) is correct (Section 4.1). The Section 10 record keeps the round-2 sentence and adds a correction note |
| S2, labels | grep in the note and in `revision2_catmix.py` | No remaining "exact Hessian" or "exact eigenvalue" in the note, except the two places in Section 8 (item 19) and Section 11 that describe the relabelling. The script's docstrings and printed labels say "analytic". The function name `exact_grad_hess` is kept, and a docstring explains why. `reviews/singular-arcs-confirm-r2-checks/d2_fb_residual.py` does import it |
| S2, numbers | `e2`: my rerun of `revision2_catmix.py K`, and `diff` | The rerun is identical to `logs/revision3_catmix_K.log`, apart from the timing lines. After replacing the labels, it is also identical to the Part K lines of `logs/revision2_catmix_ZK.log`. The finite-difference agreement is `1.1e-12` (N = 100) and `7.0e-13` (N = 200) at step `1e-5`, and `1.1e-11` and `6.7e-12` at step `1e-6`, as Section 10 R1 and Section 11 now state. Smallest `|eigenvalue|` at N = 200: analytic `1.80e-12`, central differences `9.98e-13` and `1.67e-12`, which the note correctly rounds to `1.0e-12` and `1.7e-12`. The "order only" caveat in 5.5 is warranted |
| Tables | `d4_tables.py` from round 2, rerun on the current note | 7 tables, 0 rows whose cell count differs from the header (Section 7 changed) |

## 2. Remaining problems

None that need a fix. Two optional wording nits:

- Section 11, S1, second sub-bullet: "the round-1 confirmation review" is
  the review that the rest of the note calls "the second review"
  (`singular-arcs-confirm-r1.md`). Using one name would be clearer. The
  header lists the files, so the reader can resolve it.
- Section 10, refusal item, correction note: "the reason given for E2 is
  wrong". The fact stated in round 2, that the `k₂` part is not a null
  Lagrangian by itself, is true. What was wrong is the conclusion drawn from
  it. Section 11 already says this precisely. "The conclusion drawn for E2
  is wrong" would match.

## 3. Items the reviser did not apply

- **No Euler run of the `w ≡ 0` formulations: acceptable.** The note makes
  no claim about these discrete problems. It says in Remark 3.5 that they
  were not tested and lists them as open in Section 6. The compatibility
  argument does not depend on them.
  - *For information only (not a required change).* My `e3` computed the
    reduced Hessian of the Euler transcription of the `w ≡ 0` E2
    formulation (`k₂ = 1/4`, gauge from the `k₁ = 0` problem), restricted
    to the free stages of its box-constrained optimum. This is float linear
    algebra; the problem is exactly quadratic.
  - Validation: the same code reproduces the note's `k₁ = 0` minimum
    eigenvalues, `8.2e-5`, `1.0e-5`, `1.3e-6` and `1.6e-7` at
    N = 50–400.
  - For the `w ≡ 0` formulation the minimum eigenvalue is `2.6e-5`,
    `3.3e-6`, `4.2e-7` and `5.3e-8`, that is `≈ 0.12h³ > 0`. The full
    Hessian is positive definite too, so the Euler optimum of this
    formulation is not a saddle.
  - A hand estimate agrees. Along `δu_t = ε(−1)^t`, the extra Euler term
    `h²k₂Σu_t(x₁ − x₂)_t` lowers the per-stage curvature by `k₂h³`, from
    `0.375h³` to `0.125h³`.
  - This is consistent with the note's reading, but I did not do the same
    for catmix in `ξ`. If the author wants to use it, it should be labelled
    as a single float check on E2.
- **Old log `logs/revision2_catmix_ZK.log` keeps the label "exact Hessian":
  acceptable.** Section 11 says so, the new log uses the corrected label,
  and the numbers are identical. Not rewriting old logs matches the note's
  stated practice ("no earlier log was overwritten").

## 4. Was anything strengthened?

No.

- The round-2 claim "outside the class in every gauge" is withdrawn.
- The new positive statement, that equivalent `w ≡ 0` formulations lie
  inside the class, is:
  - conditional on the class as read from the 2005 paper;
  - checked symbolically (and by me, independently);
  - accompanied by two new caveats: the Euler transcriptions were not
    tested, and Felgenhauer's other hypotheses were not checked.
- The Summary novelty item still says "probably" for the class, and it now
  adds the untested caveat.
- The Section 7 row is limited to "symbolic (round 3)" for the membership
  statement.
- S2 only weakens: the Hessian is now "float", and the N = 200 eigenvalue is
  meaningful "only in order".

## 5. Commands run (targeted only)

These were run in `reviews/singular-arcs-confirm-r3-checks/` unless stated
otherwise. All runs used `OMP_NUM_THREADS=1`, `timeout` and
`PYTHONDONTWRITEBYTECODE=1`.

1. `python3 e1_semilinear_independent.py` → `e1_semilinear_independent.log`
   (sympy and scipy; E2 gauge, Kelley quantity by a closed formula,
   continuous and Euler cost identities; catmix reachable set, `ξ`
   formulation, singular-point equation, `K`, cost identity; a few seconds).
2. From `theory-bangbang/singular/`:
   `python3 revision2_catmix.py K > …/e2_partK_rerun.log`, then `diff`
   against `logs/revision3_catmix_K.log` and, with labels replaced, against
   `logs/revision2_catmix_ZK.log` (about 10 s).
3. `python3 e3_w0_euler_hessian.py` → `e3_w0_euler_hessian.log`
   (informational; E2 Euler reduced Hessians for the `k₁ = 0` and `w ≡ 0`
   formulations at N = 50–400; a few seconds).
4. From the continuation root:
   `python3 reviews/singular-arcs-confirm-r2-checks/d4_tables.py
   theory-bangbang/singular-arcs.md` (table cell counts).
5. Read `revision3_semilinear.py` and its log, the header and docstrings of
   `revision2_catmix.py`, and both Part K logs. I also used `grep` on the
   note.

## 6. Sources examined

- Project files:
  - the note;
  - `reviews/singular-arcs-confirm-r2.md` and its check scripts (`d2`,
    `d4`);
  - `theory-bangbang/singular/revision3_semilinear.py`,
    `revision2_catmix.py`, `lqsing.py` (header only);
  - `logs/revision3_semilinear.log`, `logs/revision3_catmix_K.log` and
    `logs/revision2_catmix_ZK.log`.
- Literature: none read for this round. S1 concerns only the class
  definition as quoted in the note (the second review's reading of
  Felgenhauer 2005, Section 2: `min k(x(1))` subject to
  `ẋ = f(t,x) + B(t)u`). I did not open Felgenhauer's papers, so I cannot
  confirm that definition or her other hypotheses; the note says the same.
