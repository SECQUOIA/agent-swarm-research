# Recheck: second-round revision of the calibration note

Date: 2026-09-30. Note rechecked:
[`../theory-calibration/scouting.md`](../theory-calibration/scouting.md), mainly
Section 10 ("Revision after review") and the passages it changed, against the first
review [`calibration-review.md`](calibration-review.md) (findings F1–F18). I did not
write or review the note before. I did not edit the note and did not commit anything.
My own checks are in [`calibration-recheck-checks/`](calibration-recheck-checks/)
(scripts `r1`–`r3`, logs in `logs/`). They are new code, not reruns of the author's
or the reviewer's scripts.

## Verdict

No mathematical error was found. Every change that Section 10 lists is present in the
text, and each revised statement that I rechecked is correct under its stated
hypotheses. What remains is a set of **minor** fixes: scope and wording, one citation
detail, and one numerical-agreement sentence (Section 11). None changes a theorem.

| # | Item | Verdict |
|---|---|---|
| 1 | Theorem 5.2 proof redone with uniform convergence (`eta_h = e_h + h`) | **correct**; every step rechecked |
| 2 | New hypotheses: admissible `(x*,u*)` with `r = 0`; compact `D`, `U` | **correct and needed** (step 1 uses both admissibility and `r = 0`; see 3 for compactness) |
| 3 | `U = R` counterexample (Euler transcription unbounded below for every `h`) | **correct**; exact identity `r = (u/2 - x^3)^2 + u^2/4 + x^2` proves the growth bound |
| 4 | Coercivity remark 5.2(b) | **correct**; the identity holds for vector states too (checked symbolically, `n = 2`, `m = 1`) |
| 5 | Strictness in `x`; LQ defect `h^2 alpha P (P - alpha)` | **correct** for `l = u^2/2`; general `q` gives `h^2 (P - alpha)(alpha P + q)`. Wording fix R5 |
| 6 | Tilt fix; `h_0 ~ eps e^{-lambda T}` | threshold **correct**; the scaling is **confirmed for scalar LQ only**, with a factor that grows with `lambda`. The general proof gives only `h_0` of order `c^2` (R2) |
| 7 | `O(h^2)` loss of uncorrected sampling | **correct** when `e_h = O(h)` (the remark says so; the Summary drops the condition, R6). Confirmed on two examples |
| 8 | Corollary 4.3 with four assumptions | **correct as a conditional statement**. One unrevised sentence in Section 4 still states the conclusion without conditions (R3) |
| 9 | Theorem 3.1: converse needs attainment of `f*` | **correct** |
| 10 | Leitmann–Stalford (1971) citation | bibliographic data **correct** (Crossref). The restatement the note relies on has an *integral* hypothesis; the pointwise condition is its sufficient form (R1) |
| 11 | Novelty wording | **mostly consistent**; three sentences still say "new" or "whenever" (R7) |

## 1. Theorem 5.2: hypotheses and proof

I rederived each step with the Euler data `L_t = h l`, `f_t = x + h g` and
`S^h_t = S(t_t,.) + a_t^T x`, where `a_t = p^h_t - S_x(t_t, x^h_t)`.

- **Step 1.** Growth `r >= c|z - z*|^2` together with `r(z*) = 0` at an interior point
  gives `grad r = 0` and `grad^2 r >= 2cI`. With `xdot* = g(x*,u*)`,
  `grad_x r = l_x + S_xt + S_xx g + g_x^T S_x = 0` is the adjoint equation for
  `psi = S_x(t, x*(t))`, and the terminal minimum gives `psi(T) = grad Phi(x*(T))`.
  Both new hypotheses are used:
  - admissibility, because `d/dt S_x(t,x*(t))` must equal `S_xt + S_xx g`;
  - `r = 0` on the pair, because without it `z*(t)` need not minimize `r(t,.)`.

  (`r = 0` is a normalization: `S + phi(t)` shifts `r` by `phi'(t)`. What matters is
  that `z*(t)` minimizes `r(t,.)` with quadratic growth. The note's form is fine.)
- **Step 2.**
  - `a_t = O(e_h)` follows from (T3) and the Lipschitz continuity of `S_x`.
  - The expansion of `a_{t+1} - a_t` is right, including the identity
    `S_xt + S_xx g = grad_x r - l_x - g_x^T S_x`.
  - Both brackets are `O(eta_h)`. This uses `psi(t_{t+1}) - psi(t_t) = O(h)` and
    `grad_x r(z^h) = O(e_h)`.
- **Step 3.** The integral remainder
  `R_2 = int_0^1 (1-s) D^2 S(t+sh, x+shg)[(1,g),(1,g)] ds` is the correct
  second-order Taylor remainder, and it is `C^2` in `(x,u)` for `S in C^4`,
  `g in C^2`. `D'` is needed because `x + hg` can leave `D` for non-reachable `x`.
- **Step 4 (far region).** Each lower-bound term checks out:
  - `r(z) >= c(delta - e_h)_+^2`;
  - `r(z^h) = O(e_h^2)`;
  - `h^2 |R_2(z) - R_2(z^h)| = O(h^2 delta)`, which is at most `h C eta_h delta`;
  - the two `a` terms are `O(h eta_h delta)`.

  Positivity for `delta >= M_0 eta_h` holds uniformly, with `M_0` of order `C/c`.
- **Step 5 (near region).** The gradient of `rho_t` at `z^h` vanishes: in `x` by the
  discrete adjoint, since `grad S^h_t(x^h_t) = p^h_t`; in `u` because `u^h_t` is
  interior for small `h`. The note leaves this implicit; it follows from `e_h -> 0`
  and the uniform interiority of the continuous `u*` on `[0,T]`. The Hessian is
  `h(grad^2 r + O(h) + O(e_h)) >= h(2c - o(1))` on a ball that shrinks to `z*`.
- **Step 6.** The terminal gradient is `a_N = grad(Phi - S(T,.))(x^h_N)`, so the
  terminal residual has zero gradient at `x^h_N`. Stage 0 works in `u` only, and
  `a_0` enters only as a constant. Uniqueness follows from strict positivity.
- **Rate.** Only `e_h -> 0` is used. `M_0` is fixed before `h` is made small, so the
  claim "no rate is needed" is correct.

One scope gap (R8): (T1)/(T2) write `l(x,u)`, but Check 5.3 uses a time-dependent
`l`. The proof does not change if `l` is continuous in `t` and `C^2` in `(x,u)`. State
this.

## 2. The `U = R` counterexample (Remark 5.2(c))

- `r = u^2/2 + x^6 + x^2 - x^3 u = (u - x^3)^2/2 + x^6/2 + x^2` (checked).
- Exact identity (`r1`, part c): `r - (x^2+u^2)/4 = (u/2 - x^3)^2 + 3x^2/4 >= 0`. This
  proves the growth bound with `c = 1/4` on all of `R x R`, so the grid ratio
  (0.255) can be replaced by this one-line proof.
- `Phi - S(T,.) = x^2/2`. The continuous optimum is `0`, and `(x,u,p) = 0` is an exact
  discrete KKT point with `a_t = 0`.
- The jump point costs `X^2/(2h) + X^2/2 - X^4/4`, which tends to `-inf` for every `h`.
  At `X = 1000` the values are `-2.49994e11`, `-2.49950e11`, `-2.49500e11` for
  `h = 0.1, 0.01, 0.001`.
- So dropping (T1) makes the theorem false while (T2) and (T3) hold (`e_h = 0`).
- With `U = [-K,K]` the last-stage residual at `x = 0` is `h u^2/2 - h^4 u^4/4`. It is
  nonnegative iff `h^3 u^2 <= 2`, so `h_0 <= (2/K^2)^{1/3} -> 0` as `K` grows. This
  shows concretely how `h_0` depends on the size of `U`; the note could mention it.

## 3. Coercivity remark (5.2(b))

- `r_uu = H_uu`, `r_xu = H_xu + P g_u`, `r_xx = H_xx + P g_x + g_x^T P + Pdot`.
- Hence `zeta^T grad^2 r zeta = zeta^T grad^2 H zeta + d/dt(xi^T P xi)` along
  `xidot = g_x xi + g_u eta`.
- Integrating gives the stated `Q_H` identity and `Q_H >= 2c(||xi||^2 + ||eta||^2)`,
  which is stronger than the stated `2c||eta||^2`.
- The note says "rechecked here for scalar states". `r1` part d checks the pointwise
  identity symbolically for `n = 2`, `m = 1` with random polynomial `S`, `l`, `g`.
  It is a general algebraic identity, so "for scalar states" can be dropped.
- Dontchev–Hager, SICON 31 (1993) 569–603: Crossref confirms the metadata, and the
  abstract says "an estimate is obtained for the error in the Euler approximation to
  an optimal control problem". I did not check their hypotheses; the note already
  says so.

## 4. Strictness in `x` (Remark 5.2(d))

- Euler Riccati map: `F(P') = A^2 P'/(1 + hP')`, with `A = 1 + alpha h` (checked).
- `r1` part a expands `F(P(t+h)) - P(t)` along the continuous Riccati solution. The
  `O(h)` term vanishes, and for `l = u^2/2` the `O(h^2)` term is exactly
  `alpha P (P - alpha)`, as the note says.
- For `l = (u^2 + q x^2)/2` the `O(h^2)` coefficient is `(P - alpha)(alpha P + q)`.
  This explains every sign in the review's check c3. For example, `alpha = 0, q = 1`
  gives `+P`, and `alpha = 1, q = 1` gives `P^2 - 1 < 0`.
- For `q = 0`, `alpha = 0` the defect is exactly zero (`P = 1/(1/phiT + T - t)`).
- The cost statement is correct: `Theta(h^2)` per stage on a `D` of fixed width,
  `Theta(h)` in total. My `r2` part A reproduces the review's field gaps (0.1912,
  0.1024, 0.0527, 0.0267, 0.0134, 0.0067 for `N = 10 … 320`) to `1e-15`.

**R5 (wording).** The sentence "exactness only for the favourable case `alpha = 0`" (l.
1213–1214) cites a measured case with `l = (u^2 + x^2)/2`. That case is outside the
`l = u^2/2` family of the formula just above; its defect is `+h^2 P`. Also,
favourable cases are not limited to `alpha = 0`: with `q = 0` the sign is that of
`alpha P (P - alpha)`. Suggested fixes:

- give the general-`q` coefficient;
- say "exact in the measured favourable case `alpha = 0`, `q = 1`";
- in the Summary (l. 116), write "non-strict LQ fields **can** lose `Theta(h)`".

## 5. Tilt and `h_0` (Remark 5.2(e))

- The added residual `eps e^{-lambda t}[lambda|d|^2 - 2 d^T(g - g*)]` is correct.
- For `xdot = alpha x + u`, the form in `(d, v)` has determinant
  `e'(lambda/2 - alpha + P - e')` (`r1` part b). So the threshold
  `lambda > 2 alpha - 2P + 2e'` is correct, and it must hold for every `t`.
- The terminal strictness constant is exactly `eps e^{-lambda T}`.

**`h_0` scaling, measured (`r2` part B, exact test).** The stage residuals are
quadratic. With an interior trajectory, the transferred family is exact iff every
stage Hessian is PSD. On every grid `N` the computed gap agreed with this test (agreement
fraction 1.0). `h_0` below is `T/N` at the largest inexact `N` on a 160-point
geometric grid up to `N = 2e5`.

| problem | `lambda` | `eps` = 0.5 | 0.1 | 0.02 |
|---|---|---|---|---|
| `alpha = -2, q = 0, Phi = x^2/2` | 1 | exact for all `N >= 4` | `h_0/(eps e^{-lambda T}) = 3.4` | 2.6 |
| | 2 | exact for all `N >= 4` | 3.2 | 2.9 |
| | 4 | 4.0 | 3.5 | 3.4 |
| | 8 | 4.9 | 4.8 | 4.7 |
| `alpha = 1, q = 1, Phi = 0` | 4 | 4.7 | 4.2 | 4.1 |
| | 6 | 8.8 | 8.6 | 8.4 |
| | 8 | 12.7 | 12.4 | 12.1 |

So for scalar LQ, `h_0 ≈ C(lambda) eps e^{-lambda T}`: linear in `eps`, with a
prefactor that grows roughly linearly in `lambda`. For `alpha = -2, lambda = 8`,
`eps = 0.5` the family first becomes exact at `N = 1300`, which is consistent with the
review's inexact value at `N = 320`. The advice "`lambda` just above the threshold,
not large" is confirmed.

**R2 (scope of the scaling claim).** In the LQ case the residuals are exactly
quadratic, so the near/far split is not needed. For the general theorem, the proof's
constants give only `h_0` of order `c^2` for fixed problem data:

- the far region needs `delta >= M_0 eta_h` with `M_0 ~ C/c`;
- the near region needs `grad^2 r >= c` on a ball of radius `~ (C/c) eta_h`;
- a Lipschitz `grad^2 r` then forces `eta_h <~ c^2`.

"`h_0` scales with it" (l. 1222–1223) and the attack plan's "`h_0` scales like
`eps e^{-lambda T}`" (l. 1421–1423) should be labelled as observed for scalar LQ, with
`c^2` as the general bound from the proof. Also, "tilting makes a field strict when it
satisfies the strengthened Weierstrass condition" is verified here only for scalar LQ.
Label it a sketch.

## 6. Uncorrected sampling loses `O(h^2)` (Remark 5.2(f))

- The argument is correct: the residual gradient at `z^h` is `O(h eta_h)`, the
  curvature is `~ch`, and the terminal term costs `O(e_h^2)`. The total is
  `O(eta_h^2)`.
- The remark itself says "`O(h^2)` when `e_h = O(h)`". The Summary (l. 119–120) and the
  Section 8 row for Proposition 5.1 drop that condition (R6).
- Numerical confirmation:
  - Check 5.3: three implementations agree (0.0237, 0.0061, 0.00157, 0.00040 for
    `N = 10 … 80`).
  - Tilted LQ (`r2` part C): gap/`h^2` = 0.151, 0.146, 0.147, 0.149, 0.150, 0.150,
    0.151 for `N = 10 … 640`.
- The comment after Proposition 5.1 (l. 1093–1095) says the `O(h)` rate is attained
  for non-strict `S`, citing Remark 5.2(d). But (d) measures the *corrected* family.
  The claim also holds for the uncorrected family: in `r2` part C the uncorrected field
  gap/`h` tends to 2.55 (2.25, 2.41, 2.49, 2.52, 2.54, 2.55, 2.55). Cite that, or say
  that (d) concerns the corrected family.

## 7. Corollary 4.3

The four assumptions are the ones F18 asked for, and the proof is right: inserting
`sigmatilde = gamma|t - t_s| + o(1)` and `|grad sigmatilde| >= g_0` into the
`h`-independent inequality of Proposition 4.2 gives the stated window.

Two small points:

- The constants `Lambdatilde`, `Mtilde` and the ball radius `r >= s*` must hold
  uniformly over the stages concerned. "The hypotheses of Proposition 4.2 at the
  stages concerned" implies this, but "uniformly" should be said.
- **R3.** The closing paragraph of the exact-windows discussion (l. 1064–1066) still
  says "Propositions 4.1–4.2 show that affine calibrations need windows of fixed
  duration, that is `Theta(1/h)` stages, at singular arcs and at switches". That is
  the unconditional form the revision removed elsewhere. It should cite Corollary 4.3
  and its assumptions. For singular arcs, the `Theta(1/h)` count also needs
  convergence assumptions (discrete controls interior along the arc), which are not
  stated anywhere.

## 8. Theorem 3.1 converse

"If `f*` is attained, every exact affine family has this property at every global
minimizer" is correct. At a minimizer the telescoped sum equals `f* = B(p)`, every
term is at least its infimum, and all infima are finite. Optional: item 3 uses this
converse, so it should say "`(xbar, ubar)` a global minimizer". With `x_0` fixed,
`p_0` is not determined.

## 9. Leitmann–Stalford citation

- **Metadata correct** (Crossref): G. Leitmann, H. Stalford, "A sufficiency theorem for
  optimal control", JOTA 8(3) (1971) 169–174, doi 10.1007/BF00932465.
- **R1 (precision).** The only restatement the note relies on is Goenka–Liu–Nguyen
  (Birmingham WP 20-25). I read it: its footnote 26 restates the LS theorem with an
  **integral** hypothesis along admissible pairs,
  `int [H(x*,z*,lambda) - H(x,z,lambda) + <lambdadot, x* - x>] dt >= 0`, plus a
  transversality condition. The pointwise augmented-Hamiltonian inequality is their
  Assumption 6, used "in line with" LS, and it implies the integral condition. A 2010
  paper in Applied Mathematics and Computation also speaks of "the integral form of the
  Leitmann–Stalford sufficiency conditions" (search-result abstract only).
- The note's wording "the pointwise condition … is Leitmann–Stalford" (l. 199–203,
  604–611) should read "the pointwise (sufficient) form of the Leitmann–Stalford
  condition". I could not read the paywalled original either.
- "Also in Seierstad–Sydsæter's treatment" (l. 610) is unverified by both review
  rounds. Mark it as cited from memory or drop it.
- The attribution itself (the condition behind Theorem 3.3 is classical, and only the
  mesh-uniform statement remains) is right.

## 10. Novelty wording

Section 6 is consistent with the review: Theorem 3.5 is kept as a reading; Theorem 3.3
is new only in its mesh-uniform statement; Theorem 5.2 and Propositions 4.1–4.2 are
"not found stated before; elementary". **R7**, three leftovers:

- l. 67 and l. 129: "is new". The note elsewhere says "not found stated before"; use
  that.
- l. 105: "the most substantive new result". Suggest "the most substantive result not
  found stated before".
- l. 1339–1341: "whenever the continuous problem has an exact strict calibration on
  compact state and control sets" omits (T3) and interior optimal controls. Add them.

## 11. List of fixes (all minor)

- **R1.** Say "pointwise (sufficient) form of the Leitmann–Stalford condition"; note
  that the GLN restatement is integral; mark or drop the Seierstad–Sydsæter pointer.
- **R2.** Label `h_0 ~ eps e^{-lambda T}` as a scalar-LQ observation (measured
  `h_0 ≈ C(lambda) eps e^{-lambda T}`, `C` = 2.6–12.7 in the tests). The general proof
  gives order `c^2`. Label the general tilting claim a sketch.
- **R3.** Section 4, l. 1064–1066: make the `Theta(1/h)` sentence conditional (cite
  Corollary 4.3; singular arcs need their own convergence assumptions).
- **R4.** Check 5.3, l. 1274: "agree to about `1e-11`" holds for the transferred and
  uncorrected rows (at most `2e-11`). The costate-affine row differs by up to `1.5e-9`
  (`N = 40, 80`; see Section 12). Say "to `2e-9`".
- **R5.** Remark 5.2(d): give the general-`q` defect `(P - alpha)(alpha P + q)`,
  describe the measured exact case correctly, and write "can lose `Theta(h)`" in the
  Summary.
- **R6.** Summary item 5 and the Section 8 row for Proposition 5.1: "`O(h^2)` when
  `e_h = O(h)`". Fix the cross-reference after Proposition 5.1 (Section 6 above).
- **R7.** Novelty leftovers at l. 67, 105, 129, 1339–1341.
- **R8.** Theorem 5.2: allow `l(t,x,u)` (continuous in `t`, `C^2` in `(x,u)`), since
  Check 5.3 uses it. Optionally say that `x^h_t`, `u^h_t` are interior for small `h`.
- **Optional.**
  - Remark 5.2(b): drop "for scalar states".
  - Remark 5.2(c): replace the grid ratio by the exact identity.
  - Section 3.1 sanity check (l. 675–676): "outside the concave region" should be
    "outside `|x| < sqrt(a/(2b)) = 1`, where `w` exceeds its convex envelope". The
    concave region is `|x| < 0.577`, and `min x = 1.068 > 1` refers to the former.
  - Theorem 3.1(3): state that `(xbar, ubar)` is a global minimizer.

## 12. Numerical checks run for this recheck

All are floating point, not certified.

- **`r1_symbolic.py`** (sympy, 1.4 s). Checks the LQ defect expansion (general `q`),
  the tilt determinant, the `U = R` identities and jump costs, and the vector-state
  coercivity identity. All pass.
- **`r2_tilted_lq.py`** (35 s). My own exact box minimization of quadratic stage
  residuals (stationary point, edge critical points, corners). Part A reproduces the
  review's c4/c4b field and tilted gaps to `1e-15`. Part B gives the `h_0` table
  above. Part C gives the uncorrected-family losses.
- **`r3_check53.py`** (2 min 36 s). A third implementation of Check 5.3. It solves the
  full KKT system in `(u,x,p)` by `scipy.optimize.root` (KKT residual `<= 1e-15`), uses
  a 2001 × 1001 stage grid with Powell polish, and analytic derivatives.

| `N` | transferred gap | uncorrected gap | costate-affine gap | (T3) error / `h` | max`|a_{t+1}-a_t|/h^2` (`t >= 1`) |
|---|---|---|---|---|---|
| 10 | 0.0021149 | 0.0236725 | 8.7722846 | 3.38 | 4.41 |
| 20 | 6e-15 | 0.0060564 | 8.7106054 | 3.27 | 5.14 |
| 40 | 1e-14 | 0.0015676 | 8.6585751 | 3.21 | 5.42 |
| 80 | 2e-14 | 0.00040286 | 8.6330892 | 3.18 | 5.54 |

- **Agreement with the other two implementations.**
  - Transferred and uncorrected gaps agree to `<= 4e-14` for `N >= 20`.
  - Costate gaps agree with the author's to `<= 3.3e-10`. The author–review difference
    is `1.5e-9` at `N = 40, 80`.
  - At `N = 10` my transferred gap is `1.05e-6` lower. At stage 9, Powell stopped short
    of the minimum that L-BFGS-B finds (diagnostic rerun: 2.114943e-3 versus
    2.115991e-3). The other two implementations agree with each other to `2e-11`.
    The discrepancy is a weakness of my polish and does not affect any claim.
- **Conclusions confirmed:** exact for `h <= 0.05` and not at `h = 0.1`, so
  `h_0 in (0.05, 0.1)`; costate calibrations lose about 8.6; uncorrected sampling
  loses `O(h^2)`.

## Commands run

These are targeted local checks only: no project-wide verification, no CI inspection,
no commits. All ran in `reviews/calibration-recheck-checks/`:

- `OMP_NUM_THREADS=1 python3 r1_symbolic.py` → `logs/r1_symbolic.{json,log}`
- `OMP_NUM_THREADS=1 python3 r2_tilted_lq.py` → `logs/r2_tilted_lq.{json,log}`
- `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 r3_check53.py`
  → `logs/r3_check53.{json,log}`
- An inline diagnostic (`python3 -` importing `r3_check53.py`'s functions) for the
  `N = 10` stage-9 polish difference; no files written.
- An inline comparison of the three Check 5.3 implementations from their JSON/log
  files; no files written.
- Crossref API lookups for doi 10.1007/BF00932465 (Leitmann–Stalford) and
  10.1137/0331026 (Dontchev–Hager 1993).
- Goenka–Liu–Nguyen WP 20-25 PDF, converted with `pdftotext` in `/tmp` and read at the
  Leitmann–Stalford restatement.
- Web searches for Leitmann–Stalford restatements.

## Sources

- Leitmann–Stalford 1971 (Crossref metadata): https://doi.org/10.1007/BF00932465
- Goenka–Liu–Nguyen, WP 20-25 (restatement, footnote 26 and Assumption 6): https://repec.cal.bham.ac.uk/pdf/20-25.pdf
- Dontchev–Hager 1993 (Crossref metadata and abstract): https://doi.org/10.1137/0331026
- "Applying the Leitmann–Stalford sufficient conditions to maximization control problems with non-concave Hamiltonian", Appl. Math. Comput. (2010), doi 10.1016/j.amc.2010.03.070 (search-result abstract only)
