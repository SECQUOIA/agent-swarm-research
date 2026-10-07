# Confirmation review (round 2) of `theory-bangbang/singular-arcs.md`

Date: 2026-09-30. Reviewer: fresh, independent referee. I did not write the
note, its scripts, or the earlier reviews (`reviews/singular-arcs-review.md`,
`reviews/singular-arcs-confirm-r1.md`).

Scope:

- check each round-2 item (R1–R7 and the Felgenhauer refusal item) and the
  reviser's report from scratch;
- recompute the numbers that changed;
- judge the items the reviser did not apply;
- check that nothing was strengthened.

Checks were targeted, with `OMP_NUM_THREADS=1`, `timeout`, and
`PYTHONDONTWRITEBYTECODE=1`. No project-wide verification was run, CI was not
inspected, and nothing was committed. The note and its logs were not touched.
My scripts and logs are in `reviews/singular-arcs-confirm-r2-checks/`.

## Verdict

**Fixes needed (minor).**

- R1–R7 are fixed as reported. Every changed number I recomputed reproduces.
  The R1 numbers were recomputed with independent code in the original 2-D
  COPS form, not the note's reduced model.
- The four items the reviser did not apply are acceptable: the N = 200 KKT
  repair, the E2 experiment, reading Felgenhauer (2005), and editing [C].
- One new problem is minor (S1). The reply to the Felgenhauer refusal item
  says that E2 is outside the semilinear class "in every gauge". That is
  false: a gauge of the note's own kind puts E2 in the class, with `w ≡ 0`.
  The error comes from the round-1 confirmation review, and the reviser
  adopted it. The reviser's compatibility argument is not affected, but the
  statement appears in three places.
- One item is trivial (S2): the new audit is labelled "exact", which by the
  note's own convention means rational arithmetic.

## 1. Items R1–R7 and the refusal item: what I checked

| item | check | result |
|---|---|---|
| R1: N = 100 point | `d1`: my own code for the COPS trapezoidal rule in the original 2-D form, `x_{i+1} = x_i + h/2(A(u_i)x_i + A(u_{i+1})x_{i+1})`. mpmath at 40 digits, hand-written adjoint gradient, and a Hessian from central differences of that gradient (step `1e-12`). Values are in `J` units, which are the note's `log(J+1)` units times `J+1 = 0.952` | `J = −0.0480693947983`; arc 14..72, no stage at a bound; `max abs(g) = 2.8e-17`; 5 negative eigenvalues, the most negative `−3.1436e-8`; eigenvalue nearest zero `4.29e-9` (the note: `4.5e-9` in log units); Newton step `2.5e-10` (the note: `4.8e-10`; both at noise level). `d6`: the bang-stage multipliers are at least `1.7e-7` in size, with the right signs, so strict complementarity holds. The claim "KKT point to float accuracy" stands |
| R1: N = 200 point | `d1` | Bound stages 28, 118, 120, 129 and 138, with `g` = `1.45e-8`, `2.59e-9`, `−2.66e-11`, `−2.47e-10`, `−3.45e-10`; the last three have the wrong sign. Interior `max abs(g) = 3.13e-9`; 7 negative eigenvalues, the most negative `−4.0134e-9`; smallest eigenvalue `1.72e-12`; Newton step 20.85. Range `[0, 0.4679]` over the whole arc and `[0.0369, 0.4679]` on the interior stages; largest deviation 0.468, at stage 119; envelope sign changes 31, 43, …, 112 as stated. All agree with the note after the unit factor |
| R1: repair attempt (Part L) | `d1` on the saved end points; `d2`: what makes up the Fischer–Burmeister residual | After 400 iterations: stages 28 and 118 are at a bound with correct signs; stages 129 and 138 sit at `u = 1.17e-4` and `8.1e-5`, with `g = −6.9e-11` and `−8.1e-11`. Interior gradient `1.27e-10`, smallest `abs(eigenvalue)` `2.0e-10`, Newton step 0.223. After 4000 iterations: `1.25e-10`, `2.5e-10` and 0.283. The residual is dominated by the scaled interior gradient (scale `4.0e4`). The log shows the interior gradient at `1.4e-10` after 10 iterations and flat afterwards, so "lowered … then stagnated" is accurate. The negative result is stated as such |
| R1: text | read the Summary, 5.5, the table, and Sections 6–10 | "exists" is now restricted to N = 100; the N = 200 point is called approximate everywhere; the `J_ref − J_saddle` entry is "not reported"; the 24% offset and the count 7 are labelled indicative. The smooth reference at N = 200 takes only the bang layout. I confirmed that this layout (`u = 1` up to stage 27, `u = 0` at stage 28 and after stage 145) is also that of the stored COPS point |
| R2: Remark 3.9 | by hand; `d3`, which reuses the independent symbol code of round 1 (`c1_symbol_independent.py`) | `(0.5, 1, 1, 0, 1)`: `N(x) = 2.25 − x`, `f(0) = 5`, `f(π) = 1.444`, `m₊ = 1.25`, `m₋ = 3.25`, `tr Φ/2 = 2.25`, eigenvalues 4.2656 and 0.2344. `(−0.5, 1, −2, −0.25, 1)`: `N(x) = −1 + 0.5x`; near `π`, `f = (−6 + e²)/(1 + 2e²)`, so `f''(π) = 26`; `tr Φ/2 = 2`, eigenvalues `2 ± √3`. The sign rule follows from `m₊ − m₋ = −4(aR − cS)`. Small-`h` form: `f(ω) ≈ m₊/ω²` for `abs(1 − a) ≪ ω ≪ 1` when `m± = O(h³)`; Goh's form gives `Kh³/ω²` there; the algebra of `−(K + 4φ)/(K − 4φ)` is right, and the bullet is labelled heuristic. Exact flow at N = 200 (new, `d3`): `m₊/h³ = 6.22547`, `m₋/h³ = 2.07519`, `tr Φ/2 = −2.000025`. Trapezoidal rule at N = 100: the small-`h` form differs by `2.95e-7`. The Summary bullet now states the proved condition |
| R3 | `d1` | N = 100: sign changes 18, 29, 40, 51, 62, spacing exactly 11, which is 8.6% below 12.03 ("9%"). N = 200: mean 11.57 over the first seven intervals. The wording "close to, but shorter than" is right |
| R4 | expanded `∇²_xρ_t` by hand | `K_t = F_xᵀP_{t+1}F_x − P_t + hH_xx = P_{t+1} − P_t + O(h)` for bounded Hessians and costates. So `K_t ⪯ hΛI` is the one-sided condition `P_t ⪰ P_{t+1} − O(h)`, as stated, and it is consistent with the Remark 3.3a drop `β_tβ_tᵀ/κ_t`. The hypothesis is now present in the Summary "Discrete time" paragraph, after Lemma 3.1, in the table, after Proposition 3.3, and in Section 7 |
| R5 | `logs/revision2_windows_L1.log`, `logs/catmix_windows.log` | break lists as stated; counts 5, 10 and 20 in both logs; 5, 9 and 19 periodic breaks. The eigenvalue counts at the oscillating points (5, and 7 labelled indicative) now appear next to the reference counts. The break count is stated once, as a restatement of the spacing |
| R6 | reasoning | Euler has `F` and `L` affine in `u`, so `ℒ_uu = 0`. Both differences are named, "may" is used, and the question is listed in Section 6 |
| R7(a) | `d4`: GFM cell counts, splitting at every unescaped pipe, including pipes in code spans | 7 tables, 0 mismatches. In GFM, `\|` inside a code span in a table renders as a pipe |
| R7(b) | grep | "for every `h`" is gone from the Summary, Remark 3.9 and 5.6. Only the round-1 record in Section 9 keeps "independent of `h`", next to the three values of `h`; that is harmless |
| R7(c) | `treewidth-census/instancedata.csv` | `primalbound` of catmix100 is `−0.04806939108`; the gaps `4.095e-8` and `6.49e-9` are right |
| Felgenhauer | read the new bullet in Remark 3.5, Section 6, Section 10 and Sources; `d5` (sympy) | the class definition is correctly attributed to the round-1 review's reading. However, "E2 is outside the class in every gauge" is false (S1) |

## 2. Remaining problems

**S1 (minor): E2 is inside the semilinear class in a suitable gauge, and the
reduced catmix problem is inside it after a change of state variable.
"Outside the class" is a property of the formulation, not of the problem.**

- *Where.*
  - Remark 3.5, last bullet: "E2 is then outside the class in every gauge
    (in Mayer form its input column contains `ℓ_1 = k₁x₁ + k₂x₂`, and the
    `k₂` part is not a null Lagrangian), and so is catmix (`b` depends on
    `θ`)".
  - Section 6, Felgenhauer item: "E2 (`k₂ ≠ 0`) and catmix (`b` depends on
    `θ`) lie outside it".
  - Section 10, refusal item: "the `k₂ = 1/4` part is not, so E2 is outside
    the class".
  - The wording comes from the round-1 confirmation review ("E2 is outside
    the class in every gauge"), so the error is that review's, and the
    reviser adopted it.
- *Why it is false for E2* (`d5`, sympy, exact). The note's gauge adds
  `dF/dt = ∇F·g` to the integrand. Take `F = −k₁x₁²/2 − k₂x₁x₂`. Then:
  - the new `ℓ_1` is 0;
  - the new `ℓ_0` is `(x₁² + x₂²)/2 − k₂x₁(x₁ − x₂)`;
  - the new terminal cost is `½(k₂x₁² + 2k₂x₁x₂ + (1 − 2k₂)x₂²)`, and the
    constant is `F(x₀) = −k₁/2`. This matches `J(k₁) = J(0) − k₁/2` in
    Section 4.1.

  Since `b = e₁` is constant, adding a cost state gives `ẋ = f(x) + Bu`
  with constant `B` and a Mayer cost. That is the class as read. In this
  gauge `w ≡ 0`, and the Kelley quantity is still `1 − 2k₂`. The
  `k₂x₂u` term is not a null Lagrangian by itself, but
  `k₂x₂u + k₂x₁(x₁ − x₂) = d(k₂x₁x₂)/dt` is. A gauge moves the difference
  into `ℓ_0`, which the class allows.
- *Catmix.* The statement is true for the COPS formulation in `x` and for
  the `θ` formulation. It is not a property of the problem.
  - For every admissible control, `θ` stays in `[0, 1/11]`: at `θ = 1/11`,
    `θ̇ = 10(u − 1)/121 ≤ 0`, and at `θ = 0`, `θ̇ = u ≥ 0`.
  - On `[0, 1/11]`, `b(θ) ≥ 10/121 > 0`; the positive root of `b` is
    `√26 − 5 = 0.0990`.
  - So `y = ∫₀^θ dθ'/b(θ')` is a global change of state on the reachable
    set, with `ẏ = a/b + u`. A 1-D gauge `F(y) = −∫θ dy` then removes
    `ℓ_1`, which puts the reduced problem in the class with `w ≡ 0`.
- *Effect.* The compatibility argument of Remark 3.5 is unaffected. If
  anything, it becomes sharper. If Felgenhauer's class is the one read in
  2005, her Euler result concerns the `w ≡ 0` formulations. Their Euler
  transcriptions are discrete problems that this note did not test, and
  there the `h²bᵀw` term vanishes. This agrees with the note's own point
  that `bᵀw` "depends on the formulation and on the scheme".
- *Fix.* In the three places, write that the formulations used in this note
  are outside the class: E2 with `ℓ_1 = k₁x₁ + k₂x₂` and `k₂ = 1/4`, and
  catmix in `x` or `θ`. Add that equivalent formulations inside it exist:
  - E2: the gauge `F = −k₁x₁²/2 − k₂x₁x₂`;
  - catmix: `y = ∫dθ/b`, then a gauge.

  In those formulations `w ≡ 0`, and their Euler transcriptions were not
  tested. The Section 6 item can then ask whether the 2016 class is the 2005
  one, and whether her discrete system is the Euler KKT system of such a
  formulation.

**S2 (trivial): "exact" is used for float numbers.**

- The status header says numbers are floating-point "unless marked 'exact'
  (rational arithmetic) or 'symbolic'". The new audit uses "exact Hessian by
  a second-order adjoint" (5.5), "the exact Hessian there has an eigenvalue
  of `1.8e-12`" (5.5), and "smallest exact eigenvalue `1.8e-12`" (Section 10,
  R1). These are float numbers from an analytic Hessian. Suggested wording:
  "analytic Hessian (second-order adjoint, float)".
- In Section 10, R1 says the Hessian agrees with central differences "to
  `7e-13` (step `1e-5`) and `7e-12` (step `1e-6`)". Those are the N = 200
  values; at N = 100 the log gives `1.1e-12` and `1.1e-11`. "About `1e-12`
  and `1e-11`" covers both. My independent Hessian (`d1`) agrees with the
  note's to the unit factor at both `N`, so the conclusions are unaffected.

## 3. Items the reviser did not apply

- **R1, no verified N = 200 KKT point: acceptable.** The claim is restricted
  to N = 100, where I confirmed it independently, including strict
  complementarity on the bang stages. The failed repair is recorded
  accurately, and the question is listed as open. The gain comparison does
  not depend on the N = 200 point.
- **R6, no experiment: acceptable.** The explanation is now a "may" with
  both differences named, and it is listed in Section 6.
- **Felgenhauer (2005) not read by the reviser: acceptable.** The class
  definition is attributed to the round-1 review's reading, and not getting
  around a bot-check page was the right call. I did not fetch the paper
  either. S1 does not depend on the details of the class beyond the quoted
  form `ẋ = f(t,x) + B(t)u` with a Mayer cost.
- **[C] not edited: acceptable** (outside the note's scope). For the root:
  `open-instances-wave2/cops/report.md` line 215 still says that
  `−0.04806939757` "reproduces the MINLPLib value", and line 31 says "beat
  the listed ones by about 3.4e-8". Against the listed `−0.04806939108` the
  gap is `4.10e-8`.

## 4. Was anything strengthened?

Apart from S1, no. Claims criticised in round 2 were weakened or qualified:

- N = 200 is approximate;
- the spacing is "close to", not a match;
- the break counts are a restatement of the spacing;
- the E2 explanation is a "may".

The withdrawn claims of round 1 stay withdrawn. The new material is:

- the small-`h` form in Remark 3.9, labelled heuristic and checked;
- the Part L negative result;
- the Felgenhauer bullet. Its E2 and catmix sentences state more than is
  true (S1).

## 5. Commands run (targeted only)

In `reviews/singular-arcs-confirm-r2-checks/` unless stated otherwise. All
runs used `OMP_NUM_THREADS=1`, `timeout`, and `PYTHONDONTWRITEBYTECODE=1`.

1. `python3 d1_audit_2d.py 100` → `d1_audit_2d_100.log` (4 s), and
   `python3 d1_audit_2d.py 200 L400 L4000` → `d1_audit_2d_200.log` (about
   1 min). This is independent code in the 2-D COPS form, auditing the saved
   N = 100 and N = 200 points and both Part L end points.
2. `python3 ../../reviews/singular-arcs-confirm-r2-checks/d2_fb_residual.py`,
   run from `theory-bangbang/singular/` → `d2_fb_residual.log`. It is a
   diagnostic that uses the note's own functions. A first inline version of
   the same code gave identical output.
3. `python3 d3_remark39_small_h.py` → `d3_remark39_small_h.log` (the round-1
   independent symbol code; exact flow at N = 200, and the small-`h` form).
4. `python3 d4_tables.py theory-bangbang/singular-arcs.md` (run from the
   continuation root) → `d4_tables.log`.
5. `python3 d5_gauge_semilinear.py` → `d5_gauge_semilinear.log` (sympy; E2
   gauge, catmix reachable set and `b`). A first run printed the wrong root
   of `b`; the print was fixed and the script rerun, and the log is the
   rerun.
6. `python3 d6_bang_multipliers.py` → `d6_bang_multipliers.log` (bang-stage
   multipliers).
7. Read the note's new logs (`revision2_catmix_{ZK,L,L4000,M}.log`,
   `revision2_windows_L1.log`), `catmix_windows.log`, the script
   `revision2_catmix.py`, the stored COPS controls, and the MINLPLib CSV.

No project-wide checks were run, and CI was not inspected.

## 6. Sources examined

- Project files: the note; `reviews/singular-arcs-confirm-r1.md` and its
  check `c1_symbol_independent.py`; `theory-bangbang/singular/*.py` and
  logs; `open-instances-wave2/cops/report.md` (Primal section) and
  `logs/catmix{100,200,400}_u.npy`; `treewidth-census/instancedata.csv`.
- Literature: no new texts were read for this round. S1 rests on the note's
  own gauge identity (Remark 3.5) and on the class definition as quoted in
  the note, not on reading Felgenhauer's papers. The GFM rule on escaped
  pipes in table cells is from the GitHub Flavored Markdown specification
  (tables extension), from memory.
