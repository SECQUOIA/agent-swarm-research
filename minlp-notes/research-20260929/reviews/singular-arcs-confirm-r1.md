# Confirmation review (round 1) of `theory-bangbang/singular-arcs.md`

Date: 2026-09-30. Reviewer: fresh, independent referee. I did not write the
note, its scripts, or the first review (`reviews/singular-arcs-review.md`).

Scope: check each round-1 finding (F1–F6) and the reviser's report from
scratch, recompute the numbers that changed, judge the items the reviser did
not apply, and check that nothing was strengthened.

Checks were targeted and used `OMP_NUM_THREADS=1` and `timeout`. No
project-wide verification was run, CI was not inspected, and nothing was
committed. Scripts and logs are in `reviews/singular-arcs-confirm-r1-checks/`.

## Verdict

**Fixes needed (minor). All six findings were addressed, and every changed
number I recomputed reproduces.**

- F1–F5 are fixed as reported.
- F6 was done as far as access allowed. I found one further source that
  settles most of the open Felgenhauer question (see "Refusals").

Remaining problems:

- **One moderate item.** The N = 200 "KKT point" is not a verified KKT
  point (R1).
- **Four minor items.** An incorrect general sentence in the new Remark 3.9
  (R2); a spacing match stated more strongly than the data allow (R3); two
  leftover places where the `K_t ⪯ hΛI` hypothesis of F4 is missing (R4);
  selective count comparisons (R5).
- **Two small items.** An unsupported explanation for E2 (R6), and a set of
  trivial wording and formatting points (R7).

The new mathematics is correct: Proposition 3.7, the transfer-matrix
identity of Remark 3.9, and the Remark 3.3a example and sketch. My own code
(independent of the note's scripts) confirms it.

## 1. Findings F1–F6: what I checked

| item | check | result |
|---|---|---|
| F1: oscillating saddle point | reloaded `logs/catmix{100,200}_smooth_u.npy` (`c2`) | interior arc ranges `[0.0548, 0.4106]` (N = 100) and `[0.0369, 0.4679]` (N = 200) reproduce; "smooth" label removed; the 3.72e-8 match is withdrawn. But see R1 for N = 200 |
| F1: smooth reference (Part C) | reran `revision_catmix.py C` (output identical to `logs/revision_catmix_C.log` apart from timings) and recomputed every ratio from the JSON | with free junction stages, ratios 0.995–1.021, 0.993–1.025, 0.992–1.001; without them, 1.23–1.65, 1.55–3.20, 1.00–1.11; all as stated. The note frames the agreement as heuristic, with the reference dependence and the boundary terms stated |
| F1: eigenvalue explanation | `c3`: lowest eigenvalue of an m-stage Toeplitz section, `f(π) + ½f''(π)(π/(m+1))²` | smooth reference: `−2.6178e-8` against the estimate `−2.6202e-8` (N = 100, m = 59) and `−3.3749e-9` against `−3.3763e-9` (N = 200, m = 118), within 0.1%. The oscillating point lies 25–26% below the estimate. This supports the revised explanation (oscillating base point) more sharply than the note says; it could be added |
| F1: Part B 2-cycle | rerun identical | the best 2-cycle has `v = 0.454285 ≈ 2u_s`; gain equals `½u_s²·abs(f(π))` to a relative `9.4e-7` at `ε = u_s` |
| F2: symbol curvature, `d₀` | `c1`: my own mpmath code (Cayley map and `expm` written from `A(u)`; fixed point, costate and symbol derived here; transfer map built numerically from the stage Hessian, not from the note's formula) | `f(π)/h³ = −0.027286`, `f''(π)/h³ = 0.79058`, `d₀ = 0.261236`, `π/d₀ = 12.026` at N = 100, 200, 400; `det Φ = 1`; `tr Φ/2 = cos ω₀` to 12 digits; exact flow `tr Φ/2 = −2.0001` (N = 100). Predicted gains 3.9461e-8, 9.8654e-9, 2.4664e-9 reproduce |
| F2: Proposition 3.7 | by hand | correct: `v₊ = (c, 1−a)`, `v₋ = (c, −1−a)` are `N`-null, `v₊ᵀNv₋ = −2c²`, `m₊ = (1−a)²f(0)`, `m₋ = (1+a)²f(π)`; interval length `abs(1−a²)·√(f(0)f(π))/c²` |
| F2: Remark 3.9 half-trace | by hand: eliminated `δu` and `λ_{t+1}` | `Φ = [[α + γκ/α, −γ/α], [−κ/α, 1/α]]` with `α = a − cS/R`, `γ = c²/R`, `κ = Q − S²/R`; `det Φ = 1`; `tr Φ/2 = (Qc² − 2Sac + R(1+a²))/(2(aR − cS)) = −(m₊+m₋)/(m₊−m₋)`. Correct. One bullet is wrong in general (R2) |
| F2: 12-stage breaks | `logs/catmix_windows.log`; arc sizes of the stored COPS points (`c2`: m = 59, 118, 236) | spacing 12 after a first gap of 9 (N = 200, 400) confirmed; counts 5, 10, 20 as stated (see R5) |
| F3: window-break location | `c2`, `catmix_trap.py` docstring | `y_i = (I + h/2 A(u_i))x_i ≈ x(t_i + h/2)`, so control `u_i` covers `[t_i − h/2, t_i + h/2]`; N = 400 stage 55 starts at 0.13625, 0.02 stage before `t₁ = 0.136299`; first arc stages 14, 28, 55; L = 1 and L = 2 break only on arc stages. Interpretation correctly withdrawn |
| F4: Summary table, Remark 3.3a | reran `revision_e2.py` (identical log); checked the example and sketch by hand | example correct (`K_t = ββᵀ/κ`, eigenvalue `1.521² = 2.31`; previous stage `κ = −1.22`); the sketch's trace-counting argument is sound (it uses `K_t ⪰ 0` at exact stages and telescoping of `tr P`). Two places still omit the hypothesis (R4) |
| F5 (a)–(i) | `revision_e2.py` rerun; logs | all as stated: distances 0.238 … 0.041; counts 1, 0, 1, 1; `(J_smooth − J*)/h` = +0.040 … +0.005; N = 100 best −0.11340107; window 0.78–0.795; B1 one bang failure at t = 1.1925 (N = 800); `|β|` ≈ 0.95h; `η_L = 1` exactly (by hand and sympy Part D); `w ≡ 0` examples separated. B2 break times 2.88, 2.88, 2.97, 2.985 |
| F5 (j) | read arXiv 1107.0161 (`pdftotext`) | the note is right: (36) defines `V`, (38) the bracket `[f_i, f_j]`, (39) `R`, (30) `B₁`. The first review's remark that (38) is `Ω` was wrong |
| F5 (k) | arithmetic; `open-instances-wave2/cops/report.md`; MINLPLib `instancedata.csv` | the stated differences 3.45e-8, 4.2e-8 and 2.8e-9 are correct. See R7 on the full-precision listed value |
| F6: Megretski | read arXiv 1008.2552, Section 1.1 | Theorem 1.4 is as quoted: `(A, B)` controllable; `σ_P = σ + x′Px − (Ax+Bu)′P(Ax+Bu) ⪰ 0` for some `P` iff `σ ⪰ 0` on `L(z)` for all `abs(z) = 1`. The sign remark is correct |
| F6: Poggiolini–Stefani | PoS(CSTNA2005)017 read (introduction); bibliographic search | the 2005 paper treats a Mayer problem with single-input control-affine dynamics and assumes coercivity of the extended second variation. The 2008 (Control Cybernet. 37, 469–490) and 2011 (JDCS 17, 469–514) data are correct (both start at p. 469). The novelty wording is suitably qualified |

Nothing in the revision strengthens a claim that was criticised, except the
two statements in R3 and R7. Withdrawn claims (the 3.72e-8 match and the
junction reading of the window break) are clearly marked as withdrawn.

## 2. Remaining problems

**R1 (moderate): the N = 200 point is an approximate stationary point, not a
verified KKT point, and its active set is not bang–singular–bang.**

Check `c2` uses the note's own reduced model and gradient, on the saved
`logs/catmix200_smooth_u.npy`.

- Five stages of the arc `28..145` sit at the bound `u = 0`: 28 (the entry
  stage), 118, 120, 129 and 138. At stages 120, 129 and 138 the gradient is
  negative (`−2.8e-11`, `−2.6e-10`, `−3.6e-10`), which is the wrong
  multiplier sign for a lower bound. These violations are below the interior
  gradient level, but they are not KKT signs.
- On the 113 interior stages the gradient is `3.3e-9`. The Hessian there has
  an eigenvalue near `1e-12`, with both finite-difference steps (`1e-6`,
  `1e-5`). The resulting Newton step has `max abs(du)` of 38 or 22,
  depending on the step. So the stationarity residual is not resolved: the
  point is not shown to be close to a KKT point.
- For comparison, the N = 100 point is clean: gradient `3e-17`, no bound
  stages inside the arc, Newton step `4e-10`, smallest eigenvalue magnitude
  `4.5e-9`.
- The following statements depend on the N = 200 point:
  - Summary, "A KKT point with the bang–singular–bang active set exists …
    [0.037, 0.468] at N = 200";
  - Section 5.5, "KKT point … at N = 200 … on 113 interior stages";
  - the `J_ref − J_saddle` column at N = 200 (1.3e-10 to 4.4e-10). This is
    smaller than the first-order uncertainty of an unconverged point with
    gradient `3.3e-9`;
  - the N = 200 eigenvalue offset (24%) and the count 7.
- The range `[0.037, 0.468]` covers only the interior stages. The arc also
  contains the four zero stages, and the largest deviation from the neighbour
  average over the whole arc is 0.468, not 0.386.
- Fix:
  - restrict "a KKT point with the bang–singular–bang active set exists" to
    N = 100;
  - describe the N = 200 point as an approximate stationary point
    (interior gradient `3.3e-9`, near-singular Hessian, four interior zero
    stages, three with slightly wrong multiplier signs);
  - drop or qualify the N = 200 `J_ref − J_saddle` values and eigenvalue
    statements.
- The qualitative picture (oscillation with an 11–12 stage envelope) is not
  affected. Neither is the like-for-like gain comparison, whose references
  do not use this point.

**R2 (minor): a general sentence in Remark 3.9 is false, and the Summary
states a different condition from the one proved.**

- Remark 3.9, second bullet: "If `f > 0` on the circle, the eigenvalues are
  real and negative."
  - From the note's own formula, `tr Φ/2 = −(m₊+m₋)/(m₊−m₋)`. With
    `m₊, m₋ > 0` the eigenvalues are real. They are negative only if
    `m₊ > m₋`, and positive if `m₋ > m₊`.
  - Counterexample (`c1`): `(a, c, Q, S, R) = (0.5, 1, 1, 0, 1)`. Then
    `min f = 1.44 > 0`, `tr Φ/2 = 2.25`, and the eigenvalues are 4.27 and
    0.23.
  - For the catmix exact flow the sentence is true, and for a general
    reason: in 1-D, `m₊ ≈ Kh³` and `m₋ ≈ 4·Kh³/12 = Kh³/3` (`c1`: 6.13 and
    2.04 in units of `h³` at N = 100, against `K = 6.32`). So `tr Φ/2 → −2`.
    That limit could replace the general sentence.
- Summary, item "When `f(π) < 0 < f''(π)`": Remark 3.9 proves the statement
  under `f(π) < 0 < f(0)`, with `n = 1` and `ℒ_uu ≠ 0`.
  - `f''(π) > 0` is not sufficient. Check `c4` uses
    `(a, c, Q, S, R) = (−0.5, 1, −2, −0.25, 1)`, which gives
    `N(x) = −1 + 0.5x`. Then `f(0) = −0.22`, `f(π) = −6`, `f''(π) = 26`,
    and the eigenvalues are real (3.73 and 0.27).
  - The Summary bullet should use the proved condition and state `n = 1`.

**R3 (minor): the envelope spacing is stated as a match, but it is 4–9%
short.**

- Section 5.5 says the envelope sign changes are "what Remark 3.9 predicts
  (sign changes every 12.03 stages)".
- At N = 100 the sign changes are exactly 11 stages apart (four intervals;
  `c2` and the first review's `v8`). At N = 200 the first seven intervals
  average 11.6 stages.
- The 12-stage spacing of the maximal-recursion breaks does match 12.03. The
  oscillation of the KKT point is only close to it, which is plausible
  because the base point is far from the stationary point.
- Suggested wording: "close to the predicted 12.03 (11.0 at N = 100, about
  11.6 at N = 200)".

**R4 (minor): two places still omit the `K_t ⪯ hΛI` hypothesis that F4 was
about.**

- The Summary's "Discrete time" paragraph says tangency "must hold up to
  `|β_t| ≤ √(hΛκ_t)` (Lemma 3.1)". Section 3, after Lemma 3.1, says "a
  family must be tangential to within `√h`".
- Lemma 3.1(a) gives this bound only when `K_t ⪯ hΛI`. The note's own
  Remark 3.3a example is exact with `abs(β_t) = 1.52`, `κ_t = 1` and
  `h = 0.03`, so it violates the unqualified sentences.
- Add "when `K_t ⪯ hΛI`" in both places.
- The gloss "(Hessians that change by `O(h)` per stage)" in the Summary table
  and after Proposition 3.3 describes a sufficient condition. The hypothesis
  is one-sided (`P_{t+1} − P_t ⪯ O(h)`), so "for example" would be more
  accurate.

**R5 (minor): the count comparisons are selective or double-counted.**

- *Negative eigenvalues.* The Summary and Section 5.5 compare only the smooth
  reference's counts (4 and 10 against 4.9 and 9.8). At the oscillating
  point the counts are 5 and 7, against 4.9 and 9.4. The N = 200 comparison
  (7 against 9.4) is not stated anywhere (see also R1). Stating both keeps
  the heuristic honest.
- *Recursion breaks.* `m d₀/π = m/(π/d₀)`, so "the counts 5, 10, 20 match"
  is the same observation as "the breaks are 12 stages apart", not a second
  confirmation.
- At N = 200 and 400 one of the counted breaks is the junction-side break
  that the note calls unexplained: stage 30, and stage 55, the first arc
  stage. The periodic breaks number 9 and 19.
- Say this once, as a single heuristic agreement.

**R6 (minor): the explanation offered for E2's smooth KKT point is
untested.**

- Remark 3.9 says that "with more states, other (hyperbolic) modes can absorb
  the mismatch: in E2 … the KKT point … is smooth".
- E2 differs from catmix-trapezoid in two ways. Besides `n = 2`, E2 uses
  Euler, whose Lagrangian is affine in `u`, so `ℒ_uu = 0`. That is outside
  Remark 3.9's hypothesis `R ≠ 0`.
- Which difference matters was not checked. Write "may", or name both
  differences.

**R7 (trivial).**

- *Table formatting.* In the Summary table, the row "bang side of a junction"
  contains a pipe inside a code span (`Δ|w|²`). In GitHub-flavoured Markdown
  this splits the cell, so the row gets four cells, and the tangential-family
  entry of that row is dropped when rendered. The reviser saw this and left
  it; escaping the pipe (`\|`) or writing `‖w‖²` fixes it. Recommended.
- *"For every h".* The Summary says "`π/d₀ = 12.03` stages for every `h`".
  It was computed at three values of `h`. "At h = 1/100, 1/200, 1/400
  (h-independent to five digits)" is accurate. Section 9 and Remark 3.9
  already say this.
- *F5(k).* MINLPLib's full-precision value for catmix100 is `−0.04806939108`
  (`treewidth-census/instancedata.csv`). The gap of the chattering point to
  it is `4.10e-8`. [C] says its local solve "reproduces the MINLPLib value
  −0.04806939757", which is not the listed value. The note's arithmetic is
  right; quoting the full listed value would remove the ambiguity.

## 3. Items the reviser did not apply

- **Felgenhauer (2016) hypotheses: acceptable, and now mostly resolvable.**
  - The 2016 paper is behind a login (I also could not open it), and the
    2013 copy is behind a captcha.
  - The same author's open paper, Felgenhauer, *Optimality properties of
    controls with bang-bang components in problems with semilinear state
    equation*, Control Cybernet. 34(3) (2005) 763–785
    (matwbn.icm.edu.pl/ksiazki/cc/cc34/cc3438.pdf, Section 2), defines the
    class: `min k(x(1))` subject to `ẋ = f(t,x) + B(t)u`, "the matrix
    `B = B(t)` is independent of the state".
  - If the 2016 "so-called semilinear case" is the same class, which is
    likely but not verified:
    - Mayer cost and state-independent `B` give `w = −(∇ℓ_1 + b_xᵀψ) ≡ 0`,
      so the note's `h²bᵀw` term vanishes there;
    - E2 is outside the class in every gauge. In Mayer form its input
      column includes `ℓ_1 = k₁x₁ + k₂x₂` with `k₂ ≠ 0`, and the `k₂` part
      is not a null Lagrangian;
    - catmix is outside the class, because `b` depends on `θ`.
  - This supports the first branch of Remark 3.5's compatibility argument.
    It lets the Section 6 open item be narrowed, with the caveat that the
    2016 definition itself was not seen.
- **Schättler–Ledzewicz and Poggiolini–Stefani 2008/2011 not read:
  acceptable.** The novelty paragraph is qualified. Optionally, the 2008
  paper is openly available from the University of Florence repository
  (flore.unifi.it, handle 2158/331898).
- **N = 400 saddle not recomputed: acceptable.** The note does not use it,
  and the smooth reference replaces it. R1 asks for the same treatment of
  the N = 200 point.
- **Markdown pipe: should be fixed** (R7). It is a one-character change, and
  the defect drops a table cell.

## 4. Commands run (targeted only)

In `reviews/singular-arcs-confirm-r1-checks/`, or in
`theory-bangbang/singular/` with `PYTHONDONTWRITEBYTECODE=1` so that no
bytecode cache is written. All runs used `OMP_NUM_THREADS=1` and `timeout`;
the note's logs were not touched.

1. `python3 revision_catmix.py A B E` → `rerun_revision_catmix_ABE.log`
   (identical to `logs/revision_catmix_AB.log` + `_E.log`).
2. `python3 revision_catmix.py C` → `rerun_revision_catmix_C.log` (identical
   apart from timings; about 4 min).
3. `python3 revision_e2.py` → `rerun_revision_e2.log` (identical).
4. `python3 c1_symbol_independent.py` → `c1_symbol_independent.log`. This is
   independent code for the trapezoid and exact-flow symbols, `d₀`, the
   transfer map and `m±`, plus the R2 toy example (about 3 min).
5. `python3 ../../reviews/singular-arcs-confirm-r1-checks/c2_saddle_points.py`
   (run from `theory-bangbang/singular/`) → `c2_saddle_points.log`. It
   reports the envelope, the bound stages and KKT signs, the Hessian at two
   finite-difference steps, the Newton step, and the COPS arc stages (about
   2 min).
6. `python3 c3_toeplitz_section.py` → `c3_toeplitz_section.log`
   (finite-section eigenvalue estimate).
7. `python3 c4_r2_second_example.py` → `c4_r2_second_example.log` (second
   R2 example).

No project-wide checks were run, and CI was not inspected.

## 5. Sources examined

- M. S. Aronna, J. F. Bonnans, A. V. Dmitruk, P. A. Lotito,
  [arXiv:1107.0161](https://arxiv.org/abs/1107.0161): equations (30) and
  (35)–(41) read.
- A. Megretski, [arXiv:1008.2552](https://arxiv.org/abs/1008.2552):
  Section 1.1, Theorems 1.3–1.4, read.
- U. Felgenhauer, Comput. Optim. Appl. 64(1) (2016) 295–326: abstract and
  keywords only, via
  [IDEAS/RePEc](https://ideas.repec.org/a/spr/coopap/v64y2016i1d10.1007_s10589-015-9800-2.html).
  The keywords include "Euler method". The abstract does not define
  "semilinear".
- U. Felgenhauer, Control Cybernet. 34(3) (2005) 763–785,
  [PDF](http://matwbn.icm.edu.pl/ksiazki/cc/cc34/cc3438.pdf): abstract and
  Section 2 (problem class) read.
- L. Poggiolini, G. Stefani, [PoS(CSTNA2005)017](https://pos.sissa.it/018/017/pdf):
  abstract and introduction read. For the 2008 and 2011 papers, bibliographic
  data were checked by search ([FLORE 2008](https://flore.unifi.it/handle/2158/331898)).
- Project files: the note; `reviews/singular-arcs-review.md` and its checks
  `v7`, `v8`; `theory-bangbang/singular/*.py` and logs;
  `open-instances-wave2/cops/report.md`; `treewidth-census/instancedata.csv`
  (MINLPLib value).
