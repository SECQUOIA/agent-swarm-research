# Confirmation recheck: second-round revision of the calibration note

Date: 2026-09-30. Note checked:
[`../theory-calibration/scouting.md`](../theory-calibration/scouting.md), mainly
Section 11 and the passages it changed. The fixes were requested by the recheck
[`calibration-recheck.md`](calibration-recheck.md) (items R1–R8 plus optional items).
I did not write or review earlier versions of the note. I did not edit the note and did
not commit anything. My checks are in
[`recheck-calibration-confirm-checks/`](recheck-calibration-confirm-checks/)
(scripts `k1`–`k4`, logs in `logs/`). They are new code, not reruns of the author's or
the earlier reviewers' scripts.

## Verdict

**All eight fixes and all optional items are applied correctly.** Each was checked from
scratch, and every number that changed was recomputed independently. I found no
mathematical error, and no claim was strengthened without justification. The one real
extension, a time-dependent running cost `l(t,x,u)` in Theorem 5.2, is stated openly,
and I rechecked the proof for it. Withdrawn or narrowed claims are marked in the text,
in Section 11, and in Section 10 through its precedence note.

Four small wording points remain (Section 3 below). None changes a statement or a
number. Item 1 is the same kind of issue as R3, in the Summary.

| # | Fix | Verdict |
|---|---|---|
| R1 | Leitmann–Stalford: "pointwise (sufficient) form"; integral form; Seierstad–Sydsæter pointer dropped | **correct**. I read the source myself (GLN footnote 26, Assumption 6, "In line with", reference title) and checked Crossref |
| R2 | `h_0 ~ eps e^{-lambda T}` limited to scalar LQ; general `c^2`; tilting sketch | **correct**. All 19 measured thresholds reproduced exactly; leading-order formula and sketch bound checked symbolically |
| R3 | Section 4 closing paragraph made conditional; "uniformly" added to Corollary 4.3 | **correct**. The Summary has a similar leftover (item 1 below) |
| R4 | Check 5.3 agreement figures | **correct** (recomputed from the three JSON logs) |
| R5 | Defect `h^2 (P - alpha)(alpha P + q)`; measured exact case; "can lose" | **correct** (independent symbolic derivation, including the `h^3` term; the exact case is exact beyond leading order) |
| R6 | "`O(h^2)` when `e_h = O(h)`"; uncorrected LQ field gap/`h` | **correct** (independent box minimization; agrees to `<= 1.9e-13`) |
| R7 | Novelty leftovers | **correct**; no "new" or "whenever" wording remains outside the Section 10 history |
| R8 | `l(t,x,u)` in (T1)/(T2); interiority in step 5 | **correct**; proof rechecked step by step |
| opt. | Remark (b) vector form; (c) exact identity and `h_0 <= (2/K^2)^{1/3}`; `sqrt(a/(2b)) = 1`; Theorem 3.1(3) at a global minimizer | **correct** |

## 1. Fix-by-fix check

### R1 (Leitmann–Stalford citation)

- **Crossref** (doi 10.1007/BF00932465): G. Leitmann, H. Stalford, *A sufficiency theorem
  for optimal control*, JOTA 8(3), 169–174, 1971. This matches Section 1.1 and Sources.
- **Goenka–Liu–Nguyen, WP 20-25.** I downloaded the PDF and read it with `pdftotext`.
  - Footnote 26 restates the theorem with the integral hypothesis (i),
    `int_0^inf e^{-rho t}[H(x*,z*,lambda) - H(x,z,lambda) + <lambdadot, x* - x>] dt >= 0`,
    and the transversality condition (ii).
  - The text before it says: "In line with Leitmann and Stalford (1971), we will use
    the following assumption." Assumption 6 is the pointwise inequality
    `Hbar(x*,z*,lambda) >= Hbar(x,z,lambda)` with `Hbar = H + <lambdadot, x>`.
  - Reference [34] gives the title as "A sufficiency condition for optimal control".
  - So every statement the note makes about this source is accurate.
- **Minimization form.** Section 1.1 states the hypothesis as
  `int [H(x,u,psi) - H(x*,u*,psi) + psidot^T (x - x*)] dt >= 0`. I derived it by sign
  change (`psi = -lambda`, `H_min = -H_max`). It is correct. Together with a terminal
  (transversality) condition, it gives `J - J* >= 0` by integration by parts.
- One small point: the footnote's problem statement has no discount factor, while
  hypothesis (i) has `e^{-rho t}`. The note's reading, "infinite-horizon discounted", is
  reasonable.
- The wording "pointwise (sufficient) form" now appears in Section 1.1, the Definition
  before Theorem 3.3, Summary item 1, the Novelty list, Section 6 and the Section 8 row.
- The Leitmann–Stalford Seierstad–Sydsæter pointer is gone. The remaining
  Sydsæter–Hammond–Seierstad–Strøm citation (l. 209) is a different, older pointer, for
  discrete Mangasarian and Arrow conditions. It is unmarked, so by the note's convention
  it is cited from memory.

### R2 (scope of the `h_0` scaling)

- **General `c^2` bound.** The argument in Remark 5.2(e) is right:
  - the far region needs `delta >= M_0 eta_h` with `M_0 ~ C/c`;
  - the near region needs `grad^2 r >= c` on a ball of radius `~ (C/c) eta_h`;
  - with a Lipschitz Hessian, this forces `eta_h <~ c^2`.

  The note words this as a property of the proof's constants, not of `h_0`, and says
  that linearity beyond quadratic residuals is open. That is accurate.
- **General tilting claim (labelled a sketch).**
  - The added residual `e[lambda|d|^2 - 2 d^T(g - g*)]` is correct (k1 e; I derived it
    directly from `S = P x^2/2 - e(x - x*)^2`).
  - The splitting `d^T(g - g*) <= L_1|d|^2 + L_2|d||v|` and the Young step are correct.
  - For scalar LQ, `r_S` minus the sketch bound is exactly `(v/2 - 2 e d)^2 >= 0` (k1 e).
    So the sketch threshold `lambda > 2(alpha - P) + 4 eps` is a conservative version of
    the exact `lambda > 2 alpha - 2P + 2e(t)`, as the note says. The exact determinant
    is `e(lambda/2 - alpha + P - e)` (k1 e).
- **Scalar-LQ leading order.**
  - My derivation-operator expansion (k1 b) gives the `O(h)` term
    `4 h e (lambda/2 - alpha + P - e)` and shows that the `h^2` coefficient minus `K`
    is `O(e)`. This matches the stated `h^2 K + O(h^2 e + h^3)`.
  - The predictions `4 m(T)/|K(T)|` are `(lambda+6)/3` for `alpha = -2, q = 0,
    phi_T = 1` (`P(T) = 1`, `K(T) = -6`) and `2 lambda - 4` for `alpha = 1, q = 1,
    Phi = 0` (`P(T) = 0`, `K(T) = -1`). Both are correct.
  - The leading-order argument assumes the binding stage is near `t = T`. At every
    measured threshold exactly one stage fails, and it is the last one, `t = N - 1`
    (k4 b).
  - The label `c = e(T)` is accurate for these problems. The (T2) constant of the tilted
    `S` is `min(stage constant, e(T))`. The stage constant is 2–7 times `e(T)`, so
    `c = e(T)` in every tested case (k4 c).
- **Table (Part B), recomputed (k2).** My method differs from the author's in three ways:
  - I test PSD-ness of the stage Hessian assembled entrywise, not the Riccati-map form.
  - I use no bisection: a 600-point geometric grid up to `N = 4e5`, then every `N` in
    `[0.8 N_bad, 1.25 N_bad]`.
  - I confirm the closed-form Riccati solutions against `solve_ivp` (`<= 1.2e-12`).

  Results:
  - All 19 values of `N_bad` equal the author's, for example 1271, 6381 and 31932 for
    `alpha = -2, lambda = 8`, and 12415 for `alpha = 1, lambda = 8, eps = 0.02`.
  - The ratios equal the table to all printed digits. The range 1.0002–1.47 relative to
    the finite-`eps` prediction is correct.
  - There is no non-monotonicity: every `N` in each window below `N_bad` is inexact,
    and every grid `N` above it is exact.
  - For five cases I computed the actual gap `J^h - B(S^h)` by exact box minimization.
    It is positive at `N_bad` (from 3.2e-9 to 4.3e-3) and zero to rounding (`<= 1e-25`)
    at `N_bad + 1`, with interior controls and `1 + h s > 0`. So the PSD test is the
    exactness test, as stated.
- The explanation of the recheck's larger ratios, 2.6–12.7, is consistent. A coarser
  grid can only lower the last inexact `N`, and every one of the recheck's 19 values is
  at least the author's.

*My own error, corrected:* my first k2 run used an absolute tolerance of `1e-14` on the
determinant `ac - b^2`. That quantity is about `h` times the margin, so at `N ~ 3e4`
the test was too loose and shifted `N_bad` by about 1500. The final run tests
`a - b^2/c` on the margin scale. Only the final run's log is kept.

### R3 (Section 4 closing paragraph)

- l. 1092–1100 now starts "Under the assumptions (i)–(iv) of Corollary 4.3". It says
  that the singular-arc count needs convergence assumptions that are not stated here.
- Corollary 4.3 (l. 1017–1019) now requires `Lambdatilde`, `Mtilde` and `r >= s*` to
  hold "uniformly over these stages and in `h`".
- The Section 8 row and the Section 7 bullet are also conditional. For the Summary, see
  item 1 in Section 3.

### R4 (Check 5.3 agreement)

I read the three JSON logs directly (k4 a).

- **Author versus review:**
  - transferred: `1.93e-11` at `N = 10`, `<= 5e-15` otherwise;
  - uncorrected: `<= 8.2e-13`;
  - costate-affine: `1.16e-11`, `1.64e-10`, `1.455e-9`, `1.486e-9`.
- **Author versus recheck:**
  - transferred and uncorrected: `<= 4.2e-14`, except the transferred value at
    `N = 10`, where the author's is `1.048e-6` higher (the recheck's polish shortfall);
  - costate-affine: `<= 3.33e-10`.
- The review's `max|a_{t+1} - a_t|/h^2` is 5.288 (`N = 5`) and 5.537, 5.607, 5.631,
  5.641, 5.646 (`N = 10 … 160`).
- The author's maximal state error divided by `h` is 0.87, 0.86, 0.85 and 0.84.

The note's sentences (l. 1406–1417) match all of these.

### R5 (Remark 5.2(d))

- **Independent symbolic derivation (k1 a).** `P(t+h)` is expanded with a derivation
  operator along `Pdot = P^2 - 2 alpha P - q`. The result is
  `F(P(t+h)) - P(t) = h^2 (P - alpha)(alpha P + q) + O(h^3)`, and for `q = 0` the
  coefficient is `alpha P (P - alpha)`. A numerical check with the closed-form `P`
  converges to `K` as `h -> 0`.
- The exact zero for `alpha = q = 0`, `P = 1/(1/phi_T + T - t)`, is confirmed.
- For the measured exact case `alpha = 0, q = 1, Phi = 0` (`P = tanh(T - t)`),
  `F(P(t+h)) - P(t)` is positive on a grid of 60 values of `h` in `[1e-4, 1]`. Its
  minimum over `h^2` is `3.3e-5 > 0`. So the case is exact at every order, not only to
  leading order, which is consistent with the review's measured zero gaps.
- The sign statements ("negative for `alpha < 0 < P` and for `0 < P < alpha`") are
  correct as sufficient cases.
- The Summary (l. 122) now says "can lose `Theta(h)`".

### R6 (`e_h = O(h)`; uncorrected LQ field loss)

- The condition "when `e_h = O(h)`" now appears in the Summary (l. 129–130), after
  Proposition 5.1 (l. 1127) and in the Section 8 row.
- **Recomputed (k3).** I used `P` from `solve_ivp`, the reachable-interval `D_t`,
  `U = [-5, 5]`, and exact box minimization of each 2-D quadratic residual (corners,
  edges, interior point). The uncorrected field family has gap/`h` = 2.2450, 2.4125,
  2.4879, 2.5231, 2.5401, 2.5484, 2.5526 for `N = 10 … 640`. That rounds to the note's
  2.25, 2.41, 2.49, 2.52, 2.54, 2.55, 2.55.
- Agreement:
  - with the author's Part C: `<= 1.7e-14`;
  - with the recheck's `r2`: `<= 1.7e-13`;
  - the author's transferred field gaps versus the review's c4: `<= 1.43e-13`. The
    note's "2e-13" is correct.
- As a strict-case contrast, the tilted uncorrected family (`lambda = 1`, `eps = 0.5`)
  gives gap/`h^2` = 0.151 … 0.151, which matches the recheck.
- The sentence after Proposition 5.1 now correctly says that Remark 5.2(d) measures
  the corrected family.

### R7 (novelty wording)

- A grep finds no "is new" or "whenever" wording outside the Section 10 history.
- "Most substantive new result" now reads "the most substantive result not found
  stated before".
- The Section 6 sentence on Theorem 5.2 (l. 1477–1482) names compact sets, interior
  optimal controls and (T3).

### R8 (time-dependent `l`) and the proof

I redid steps 1–6 with `L_t = h l(t_t, x, u)`.

- **Step 1** is pointwise in `t`. With `xdot* = g(x*, u*)`, the equation
  `grad_x r = 0` is the adjoint equation for a time-dependent `l`. `psi` is `C^1`
  because `x*` is.
- **Step 2.** The discrete adjoint gives `-h l_x(t_t, z^h_t)`. The identity for
  `S_xt + S_xx g` gives `+h l_x` at the same point, so the two cancel. The remaining
  terms are `-h g_x^T(p_{t+1} - S_x(t_t, x^h_t)) - h grad_x r(t_t, z^h_t) + O(h^2)`.
  The `O(h^2)` term involves only `S` and `g`.
- **Steps 3–6.** `l` enters only through `r(t_t, ·)`. The proof uses:
  - `r(t_t, z^h) = O(e_h^2)`;
  - `grad_x r(t_t, z^h) = O(e_h)`;
  - uniform continuity of `grad^2_{(x,u)} r` on `[0,T] x D x U`.

  The joint continuity required in (T1) supplies all three.
- **Step 5 interiority.** It follows from `e_h -> 0` and the positive distance of the
  continuous `x*` and `u*` from the boundary. That distance is positive because `x*`
  and `u*` are continuous, `[0,T]` is compact, and (T2) makes them interior.
- The note after the proof (l. 1204–1210) says exactly this.

### Optional items

- **Remark 5.2(b).**
  - The component formulas `r_uu = H_uu`, `r_xu = H_xu + P g_u`,
    `r_xx = H_xx + P g_x + g_x^T P + Pdot` are correct.
  - The identity `zeta^T grad^2 r zeta = zeta^T grad^2 H zeta + d/dt(xi^T P xi)` holds
    pointwise. I checked it symbolically for `n = 3`, `m = 2`, a time-dependent `l` and
    random polynomial data (k1 d).
  - The bound `Q_H >= 2c(||xi||^2 + ||eta||^2)` follows.
- **Remark 5.2(c).**
  - The identity `r - (x^2+u^2)/4 = (u/2 - x^3)^2 + 3x^2/4` holds (k1 f).
  - The last-stage residual at `x = 0` is `-h u^2 (h^3 u^2 - 2)/4`, so `h_0 <= (2/K^2)^{1/3}`.
  - "Theorem 5.2 applies" with `U = [-K, K]`, `D = [-KT, KT]` holds. (T2) holds
    globally, `(0,0,0)` is an exact discrete KKT point, so `e_h = 0`, and `S` is
    `C^inf`.
- **Section 3.1.** `w = -2x^2 + x^4` has minima at `±1` and concave region
  `|x| < 1/sqrt 3 = 0.577`. `vex w = w` for `|x| >= 1`, and tangents there support
  `w` globally, so SGM holds on the trajectory.
- **Theorem 3.1(3).** The theorem is now stated at a global minimizer, the adjoint
  formula is limited to `1 <= t <= N-1`, and `p_0` cancels from `B(p)` when `x_0` is
  fixed. All three are correct.

## 2. Claims strengthened or withdrawn

- **Strengthened, openly:**
  - Theorem 5.2 now allows `l(t,x,u)`. The proof supports it (R8 above).
  - Remark 5.2(b) states the stronger `2c(||xi||^2 + ||eta||^2)` bound. It is correct.
  - Remark 5.2(c) adds `h_0 <= (2/K^2)^{1/3}`. It is correct and is an upper bound only.
  - Remark 5.2(d) adds "if `F(P(t+h)) >= P(t)` at every stage, the transferred field
    family is exact". It is correct for an interior trajectory. It also needs
    `1 + hP > 0`, which holds automatically for small `h`.
- **Narrowed or withdrawn:**
  - The general `h_0 ~ eps e^{-lambda T}` claim is now limited to scalar LQ.
  - The Seierstad–Sydsæter pointer is dropped.
  - "For scalar states", the grid ratio 0.255, "agree to about 1e-11" and "≈ 5.6 at
    every `N`" are all replaced.

  Each change is recorded in Section 11. Section 10 keeps the first-revision wording
  as history, and its precedence note (l. 1664–1667) points to Section 11.
- The header says the second revision "has not been rechecked". This report is that
  recheck; the root agent may update the header.

## 3. Remaining problems (all minor wording)

1. **Summary item 4 (l. 103–107).** The sentence says the costate calibration "fails on
   a time window whose *duration* does not shrink with `h`" and only then adds "under
   stated convergence assumptions that is `Theta(1/h)` stages". But the fixed duration
   is itself the conditional conclusion of Corollary 4.3; it needs (i)–(iii). Fixed
   duration and `Theta(1/h)` stages are the same statement. Suggested wording: "under
   the assumptions of Corollary 4.3, the costate calibration fails on a time window of
   fixed duration, that is `Theta(1/h)` stages". This is the Summary counterpart of R3.
2. **Section 4 closing paragraph (l. 1095–1097).** For singular arcs, Proposition 4.1
   also needs interior discrete *states* (`xbar_t in int D`) and a full-dimensional
   `U`. The sentence lists only interior controls, nonzero `grad_x sigma` and unique
   slopes. Suggest "discrete states and controls are interior".
3. **Remark 5.2(e), scalar LQ (l. 1321–1322, 1350–1351).** "Derived to leading order" is
   a formal asymptotic argument. It drops the `O(h^2 e + h^3)` remainder and assumes the
   binding stage is near `T`. My k4 b confirms that assumption for the two test
   problems but does not prove it. The note's header says proofs are complete unless
   labelled "sketch". Suggestions:
   - write "formal leading-order derivation";
   - in "So for scalar LQ, `h_0 ≈ C(lambda) eps e^{-lambda T}`", add the condition
     already stated two sentences earlier (`K(T) < 0`, binding stage near `T`).

   The numbers are correct.
4. **Pre-existing, outside R1–R8 (optional).**
   - "Linear-cost certificate" (l. 151, 336, 1480) versus the `O(N log N)` checking
     cost of Remark 5.2(h) and Section 3.3. "Linear-size certificate, `O(N log N)`
     check" would be exact.
   - Section 10 item 6 (l. 1723) still says "`O(h^2)` in the strict case" without
     "when `e_h = O(h)`". The precedence note does not list Remark (f), though
     Section 11 R6 covers it.
   - The Definition (l. 634–635) says the GLN restatement "assumes only the time
     integral". It also assumes a transversality condition, as Section 1.1 says.

## 4. Numerical and symbolic checks run for this recheck

All are floating point or symbolic, not certified. All ran single-threaded
(`OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`).

- **`k1_symbolic.py`** (sympy, 1.8 s):
  - the LQ defect, including the `h^3` term;
  - the tilted `O(h)` and `O(h^2)` terms;
  - the exact cases;
  - the coercivity identity for `n = 3`, `m = 2` with a time-dependent `l`;
  - the tilt determinant and a direct derivation of `r_S`;
  - the Young-sketch bound as an exact square;
  - the `U = R` identity and the last-stage residual.

  All pass.
- **`k2_tilted_h0.py`** (22 s): the `h_0` thresholds by grid plus exhaustive window, and
  direct gaps at `N_bad` and `N_bad + 1`.
- **`k3_uncorrected_lq.py`** (0.6 s): uncorrected, transferred and tilted-uncorrected
  LQ field gaps, compared with the author's Part C, the recheck's r2 and the review's c4.
- **`k4_logs_and_binding.py`** (0.1 s): Check 5.3 differences from the three logs, the
  review's a-increments, the binding stage, and the (T2) constant of the tilted `S`.

## Commands run

These are targeted local checks only: no project-wide verification, no CI inspection, no
commits. All ran in `reviews/recheck-calibration-confirm-checks/`:

- `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 k1_symbolic.py`
  → `logs/k1_symbolic.{json,log}`
- `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 k2_tilted_h0.py`
  → `logs/k2_tilted_h0.{json,log}`. It ran twice. The first run had the loose
  determinant tolerance described under R2, and its log was overwritten.
- `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 k3_uncorrected_lq.py`
  → `logs/k3_uncorrected_lq.{json,log}`
- `OMP_NUM_THREADS=1 python3 k4_logs_and_binding.py` → `logs/k4_logs_and_binding.{json,log}`
- Inline `python3 -c` reads of the author's, the review's and the recheck's JSON logs
  (no files written).
- `curl` of the Goenka–Liu–Nguyen PDF to `/tmp`, converted with `pdftotext` and read at
  footnote 26, Assumption 6, Remark 2 and reference [34].
- Crossref API lookup of doi 10.1007/BF00932465.
- `grep` of the note for leftover wording.

## Sources

- Leitmann–Stalford 1971 (Crossref metadata): https://doi.org/10.1007/BF00932465
- Goenka–Liu–Nguyen, WP 20-25 (footnote 26, Assumption 6, reference [34]): https://repec.cal.bham.ac.uk/pdf/20-25.pdf
