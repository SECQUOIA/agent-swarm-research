# Review: adaptive decomposition branch-and-bound and Conjecture 3.7 (`extension-adaptive.md`)

Date: 2026-09-30. Reviewer: an independent, adversarial verifier who did not
produce the work. Reviewed:
[`../theory-decomposition/extension-adaptive.md`](../theory-decomposition/extension-adaptive.md)
(the note), its scripts and logs in
[`../theory-decomposition/adaptive/`](../theory-decomposition/adaptive/), and
the parts of [D] (`decomposition-certificates.md`) and [K]
(`consistency-relaxations.md`) that the note cites. My own code and logs are in
[`decomposition-adaptive-review-checks/`](decomposition-adaptive-review-checks/).
All computations are floating point and single-threaded (`OMP_NUM_THREADS=1`).
I ran only targeted checks of this note. I did not run project-wide
verification and did not consult CI.

## Verdict: fixes needed

The mathematical core holds. I checked every proof marked "proved" line by
line and found no gap that changes a statement. My independent code
reproduces every LS number in the note exactly. The fixes concern claims that
are stated more broadly than they are proved or measured:

1. **(Moderate) "`C` depending only on `alpha`" is false on the staircase
   family. As a consequence, reading (R1) and Conjecture B.5 need `C` to
   depend on `w`.** On the staircase family, `N_dec / sup_eta Phi` is at least a quantity
   that tends to `4 (16/pi)^{d/2} Gamma(d/2+1)` as `eps -> 0`. This is
   `w^{Theta(w)}` (Section 3.3 below). The same gap already occurs at `|T| = 1` for a single flat bag.
   So the upper half of Conjecture B.5 (and of Conjecture 3.7) is false if
   `C` may not depend on `w`. Likewise, "under (QG) the conjecture holds in
   both readings" is established only when `C` may grow like `sqrt(w)`,
   because the base of Theorem 3.4 of [D] contains `sqrt(w)`. Theorem B.2's
   refutation of the lower half is not affected: the ratio there grows with
   `|T|`, not with `w`.
2. **(Moderate) Section A.5, obstacle 1, generalizes Proposition A.6 beyond
   what is proved.** The proposition is proved for level-synchronous
   refinement only. It does not cover "any rule that stops refining a box
   only when all configurations through it are worth at least `UBD - eps`".
3. **(Moderate) The 14–48% in Section C.2 is attributed to learned slopes,
   but slopes alone account for only 7–25%.** The "oracle" runs also start
   from the exact incumbent (`x0 = x*`), which C.1 and C.2 do not state. The
   learned incumbent alone costs 2–16%, and the two effects compound
   (Section 4.2).
4. **(Minor to moderate) The RC evidence needs two qualifications.** At
   `n = 8` the lower bound reached the tolerance (gap `9.2e-7 < eps`) at
   rounds 15 and 17. RC failed there only because its incumbent stalled. At
   `n = 16` the divergence reproduces, but the detailed trajectory does not:
   it changes under `1e-9` perturbations of the centre.
5. **(Minor)** Several numerical summaries and wordings need small
   corrections (Section 5).

## 1. What was checked, and how

| Item | Status in the note | My check | Result |
|---|---|---|---|
| Lemma A.1 (min-marginals) | proved | proof read; brute-force enumeration of all configurations on 18 random instances (`n = 4, 5`, random dyadic partitions, random slopes and linear terms, 33,870 configurations) against my DP and the author's `ls_lib.dp` | correct; max error `4.4e-16` (mine), `8.9e-16` (author's) |
| Lemma A.2 (permanence) | proved | proof read; `viol` counted in every sublevel of all my LS runs | correct; 0 violations |
| Lemma A.3, Lemma A.4 | proved | every step re-derived (drift `2(k-1)s`, Young weights, slope-error term, count of `(s,i)` pairs) | correct |
| Theorem A.5 | proved | (a)–(d) re-derived; constants recomputed; localization radius measured | correct (one wording fix, Section 5) |
| Proposition A.6 | proved | proof re-derived, including the parent-inclusion step for odd and even `r` and the level count; explicit configuration evaluated numerically | correct; worst `value/(0.075 n s^2) = -1.097` against the required `<= -1` |
| Conjecture A.7, Remark A.8 | conjecture, sketch | labels checked; localization data re-measured | labels appropriate |
| RC observations | computed | RC re-run with my DP | `n = 8` reproduced exactly; `n = 16` divergence reproduced qualitatively only (Section 4.3) |
| Section B.1 (QG remark) | argued | re-derived | correct only if `C` may depend on `w` (item 1) |
| Proposition B.1 | proved | re-derived | correct |
| Theorem B.2 | proved (binary separators) | re-derived; certificate rebuilt with my own shell partition, leaf minima and brute force over all binary sequences | correct; all values match the author's |
| Theorem B.3 | proved | re-derived | correct; also holds with Euclidean balls (Section 3.3) |
| "Relation to the earlier bounds" (B.4) | claims | re-derived | first two bullets correct; third bullet false as stated (item 1) |
| Proposition B.4 | proved from [K] | checked against [K] Proposition 2.3, Proposition 5.4(a), Lemma 4.1 | correct |
| Section B.5, Conjecture B.5 | discussion, conjecture | read | B.5 needs `C` to depend on `w`, or a Euclidean `Phi` (item 1) |
| Section C numerics | computed | independent re-implementation of LS | all LS numbers reproduced exactly |

## 2. Part A: the algorithm and its proofs

**Lemma A.1.** Cutting a configuration at the edge `(t, p(t))` leaves exactly
two couplings: `z^t_{S_t} in D_t`, and `D_t` meets `(B_{p(t)})_{S_t}`. The
parent's point `z^{p(t)}` is not tied to `D_t`. So `out(D)`, `o(B)`,
`MM(B) = o(B) + sum_u m_u(B)` and `MM(D) = out(D) + beta_{t,D}` are right,
and the top-down pass reuses the `g_t(B, D)` values. This is the standard
two-pass computation, as the note says. The brute-force check agrees to
rounding error for leaves, cells and `l_r = min_B MM(B)` in every bag.

**Lemma A.2.** Mapping a configuration to the ancestor boxes of an earlier
sublevel keeps every constraint. It does not increase the value, by (M) and
fixed slopes. A frozen box `B` of level `l < i` had `MM_l(B) >= UBD_l - eps`
when it was not split, and `UBD` never increases. The argument is complete.
The code's alphaBB with fixed `alpha` satisfies (M), because `q_{B'} <= q_B`
on `B' ⊂ B`.

**Lemma A.3.** I re-derived all constants:
`Lambda = 2(k-1)^2 (k M_a^2 w/c_g + M_a w) + alpha' A/4` comes from the Young
weight `c_g/k` and `Delta_t <= 2(k-1)s`. The slope term is
`-nu sqrt(w) 2 s sqrt(|T|)`.

**Theorem A.5.**

- (a) Dividing Lemma A.3 by `(c_g/2)|T| s_p^2` gives
  `a_p^2 <= 2 Lambda/c_g + gamma a_{p-1}`, with
  `gamma = 8 k^{3/2} M_a sqrt(w)/c_g`. The induction closes because
  `abar >= a*`.
- (b) `UBD - f* <= 2 Psi_A |T| s_i^2` and the sup-distance bound `rho s_i`
  follow as written.
- (c) At `i*`, `3 Psi_A |T| s_{i*}^2 <= eps`, so the stop test cannot fail.
- (d) At most `2 rho + 2` closed dyadic intervals of length `s` meet an
  interval of length `2 rho s`, which gives the count `(4 rho + 4)^{|V_t|}`.

I recomputed the constants quoted in Section A.3 (`logs/check_constants.log`):

| Constant | Value |
|---|---|
| `Lambda` | 319.40 |
| `gamma` | 633.6 |
| `a*` | 643.5 |
| `rho` with exact slopes | `2 + 138.4 sqrt(|T|)` |
| `Psi_A` with learned slopes | `2.07e4` |
| `rho` with learned slopes | `2 + 1114.6 sqrt(|T|)` |

The inequality `Psi_A <= 2 Lambda + 40 k^3 M_a^2 w/c_g + 2 k^{3/2} M_a (w+1)`
holds in three parameter sets I tried. The runs stop well before `i*`
(`i* = 19` at `n = 32`, `eps = 1e-4`; LS stopped in pass 13).

As a direct test of (b), I measured the largest sup-distance from `x*_{V_t}`
of a leaf split at level `i`, in units of `s_i`
(`logs/check_localization.log`, `eps = 1e-6`):

| `n` | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| exact slopes (one pass), max over levels | 4 | 9 | 15 | 18 |
| LS with restarts, last pass | 6 | 9 | 15 | 18 |
| max divided by `sqrt(n)` (exact slopes) | 2.0 | 3.2 | 3.8 | 3.2 |

The radius grows roughly like `3 sqrt(n)`, as (b) predicts in form. The
proven constant (`138 sqrt(|T|)` with exact slopes) is about 40 times too
large.

**Proposition A.6.** The explicit configuration is consistent, so the slope
terms vanish for any slopes. For the far bags, `x'_{V_j}` is the centre of a
level-`i` box with vertex `0`. Every dyadic box of level `<= i` containing it
has `q >= s^2/2`. `F(x') <= s^2 (0.05 n + 0.3 + 2.8 r^2 + 0.8 r)`. The
parent of a level-`(i+1)` leaf inside `[-r s_{i+1}, r s_{i+1}]^2` lies inside
`[-r s_i, r s_i]^2` for `r >= 1`, whether `r` is odd or even. The number of
admissible levels is at least `(1/2) log2(2.8/eps) - 1`. I also evaluated the
explicit configuration with the smallest admissible `q` values for
`n in {63, 64, 100, 200, 400}`, all levels with `r s <= 1`, five bag
positions and a 9x9 grid of `p` (`check_propA6.py`). The worst ratio
`value/(0.075 n s^2)` was `-1.097`, and the claim needs `<= -1`. The
induction also holds at levels with `r s_i > 1`, where the square covers the
whole box. So the proposition is correct as stated.

## 3. Part B: Conjecture 3.7

### 3.1 Correct as stated

- **Proposition B.1.** The equal allocation, monotonicity of `N_inf` in the
  radius, and subdivision of a cube of side `2R` into `ceil(2 sqrt|T|)^d`
  cubes of side `R/sqrt(|T|)` give the bound. The proof of Theorem 2.5 of
  [D] is indeed per bag and per `eta`.
- **Theorem B.2 (binary separators).**
  - The relaxation is a legitimate per-factor relaxation in the sense of
    [D, Section 1.6]. A binary point is an extreme point of the
    `s`-square, so the envelope equals `a_t - alpha q_{B_y}` at domain
    points.
  - (a) follows from the slice `{0} × [0,1]^d × {1}` and convexity of
    `u -> u^{-d/2}`.
  - (b): configurations reduce to binary sequences, and `A <= D + 1` gives
    `l_r >= -eps`.
  - (c) follows.
  - The refutation needs nothing from the unspecified "copy-error"
    hypothesis of Conjecture 3.7, because copy errors are zero under exact
    fixing. It does need that hypothesis to admit integer separator
    variables. The note says this, and it labels the continuous version a
    sketch.
- **Theorem B.3.** Correct. Lemma 1.4 of [D] gives admissibility, and the
  vertices of the minimizing leaves give the covering.
- **Proposition B.4.** Correct:
  - [K, Proposition 2.3] gives `gap(PA) = max_D g_D`.
  - [K, Proposition 5.4(a)] gives `g_D <= M r_D^2 - min_D w`.
  - The level count `J` is right.
  - A closed interval of length `2r` meets at most 3 closed dyadic
    intervals of length `2r`.
- **"Contains Theorem 2.5" and "recovers Proposition 2.4 up to `2^d`".**
  Both are correct. The exact loss against Proposition 2.4 is
  `(4d/(d+2))^{d/2} <= 2^d`.

### 3.2 Staircase numerics (Section C.4) re-derived independently

`check_staircase_indep.py` builds its own shell partition of `[0,1]^d` around
the corner. It checks that the partition tiles the cube (volume 1, no
overlaps or gaps in 4,000 random samples), that the width condition holds,
and that the count respects the Lemma 3.1 bound. It computes leaf minima in
closed form, cross-checked by L-BFGS-B (max difference `2.2e-16`). It gets
`l_r` by brute force over all `2^{K+1}` binary sequences for `K <= 12`, and
by a min-plus product otherwise.

Over `d = 1, 2, 3`, `eps = 1e-2, 1e-3` and `K = 2..1024` (42 cases), every
shell count, `l_r` and size equals the author's. In every case
`l_r >= -eps`. I also checked shells with `theta < 1` (`alpha = 4, 16`); the
author's table has `theta = 1` in all 30 rows. The non-central leaf minima
are positive, as the proof requires.

A small remark on `check_staircase.py`: its `grid_excess <= 0` test shows
only that the closed form is at most the grid minimum. It does not show that
the closed form is at most the true minimum. The closed form is exact anyway.

### 3.3 Issue 1: sup-norm covering loses `w^{Theta(w)}`

The note states that on the staircase family
"`N_dec(eps) <= C^{w+1} log(K/eps) sup_eta Phi(eps, eta)` ... with `C`
depending only on `alpha`" (Section B.4), and that `Phi` "is within
`C^{w+1}` of the certificate" (Summary). This is false if `C` must not grow
with `d = w - 1`.

- **Lower bound on `N_dec` (my argument).** Take any certificate proving
  tolerance `eps`, any bag `t`, and any `y in [0,1]^d`. Apply Lemma 1.4 of
  [D] at the point of `A_t` with `y_t = y`. Some leaf `B` of bag `t`
  containing `(0, y, 1)` has `alpha q_{B_y}(y) <= eps`. Since
  `q_{B_y}(y) >= sum_i d_i(y)^2`, the point `y` lies within Euclidean
  distance `r = sqrt(eps/alpha)` of the vertex of `B_y` nearest to it.
  Inside one leaf, such points have volume at most `V_d r^d` (one orthant
  of a ball per vertex). Hence
  `|L_t| >= Gamma(d/2+1) pi^{-d/2} (alpha/eps)^{d/2}`.
- **Upper bound on `sup_eta Phi`.** Assume `alpha <= 1` and `eps <= 1/2`.
  The family
  - `e_t = a_t + eps` on the slice `(0,1)`,
  - `e_t = a_t` on `(0,0)` and `(1,1)`,
  - `e_t = a_t - eps` on `(1,0)`

  is admissible for every `eta`, since its sum is
  `m(x) + eps (A - D) <= eta + eps`. It needs at most
  `ceil(sqrt(alpha/(4 eps)))^d + 3` points per bag, so
  `sup_eta Phi <= K 2^{-(d+2)} (ceil(sqrt(alpha/(4 eps)))^d + 3)`.
- **Ratio.** `N_dec / sup_eta Phi` is at least the ratio of these two
  bounds, which tends to `4 · 4^d Gamma(d/2+1)/pi^{d/2}` as `eps -> 0`.
  The certificate of Theorem B.2(b) shows that the true ratio is also at
  most of order `4 (8d)^{d/2}`, so the loss is `w^{Theta(w)}`. For any fixed `C` this eventually exceeds
  `C^{d+2} log(K/eps)`. With `alpha = 1` and `eps = 1e-2`, the ratio divided
  by `4^{d+2}` is `0.05, 0.19, 1.06, 130, 5.8e4` at `d = 4, 12, 16, 24, 32`
  (`logs/check_staircase_indep.log`).

The loss is not specific to the staircase. Take a single flat bag: `F = 0`
on `[0,1]^d` with relaxation `-alpha q_B`, or any flat block as in
Proposition 2.4 of [D]. The same computation gives
`N_dec/sup Phi >= 2^d Gamma(d/2+1)/pi^{d/2}` for `eps <= alpha/4`, and the
ratio tends to `4^d Gamma(d/2+1)/pi^{d/2}` as `eps -> 0`.
So the upper half of Conjecture B.5, and of Conjecture 3.7 of [D] with `Psi`,
fails at `|T| = 1` unless `C` may grow like `sqrt(w)`. The cause is that
`Phi` and `Psi` measure the tolerance per coordinate (sup-norm radius
`sqrt(e/alpha)`), while the relaxation gap adds up over coordinates.

Consequences for the note:

- Reading (R1) as defined ("`C` ... do[es] not depend on `w`") makes the
  conjecture false for trivial reasons. The meaningful distinction is the
  degree of the polynomial in `|T|`. Redefine (R1) as "degree independent of
  `w`; `C` may depend on `w`". Theorem B.2(c) already shows the failure for
  any `C` independent of `K`, so its conclusion stands.
- Under (QG), "the conjecture holds in both readings" relies on Theorem 3.4
  of [D], whose base `4/theta` is of order `sqrt(w) M_a/c_g`. So it is
  established only when `C` may grow like `sqrt(w)`.
- Replace "`C` depending only on `alpha`" by "`C` of order `sqrt(d)`,
  times a constant depending on `alpha`", or quote the factor
  `(C d)^{d/2}`.
- **Constructive option.** The proof of Theorem B.3 gives, with no change,
  the sharper statement with Euclidean balls: `z_{K_t}` lies within
  Euclidean distance `sqrt(Q_t(z))` of a vertex. Call the resulting quantity
  `Phi_2`; it satisfies `Phi_2 >= Phi`. On a flat single bag, `Phi_2` is
  within `C^d` of `N_dec` with an absolute `C`. Stating Conjecture B.5 with
  `Phi_2` appears to remove the `w^{w/2}` loss. I have not checked this
  beyond the flat and staircase cases.

## 4. Numerical checks

### 4.1 Independent re-implementation of LS

`indep_ls.py` was written from the text of Section A.2, not from `ls_lib.py`.
It differs on purpose in three places:

- bag subproblems are solved by golden-section search in `z1`, with `z2` in
  closed form or by safeguarded Newton, instead of nested bisection;
- leaves are kept sorted lexicographically, so ties are broken differently;
- the interval matching is coded separately.

Every LS number in the note is reproduced exactly: size, leaves, cells,
stopping pass and level, `l_r`, `UBD`, split counts, `viol = 0`, processed
counts and localization ratios.

| Run | Note | Reviewer |
|---|---|---|
| exact slopes, `eps = 1e-6`, sizes `n = 4..64` | 2,914 / 29,228 / 153,584 / 632,586 / 2,397,460 | identical |
| same, `l_r` at `n = 64` | `-7.171e-7` | `-7.1707e-7` |
| same, `|x^cons - x*|_2/s`, `|x^cons - x*|_inf/s` | 5.3, 11.4, 21.5, 32.2, 46.7; 4, 5, 6, 6, 6 | 5.26, 11.39, 21.44, 32.18, 46.77; 4, 5, 6, 6, 6 |
| LS with restarts, `eps = 1e-4`, `n = 4..32` | 2,841 / 21,473 / 136,187 / 459,928; processed 61,701 / 505,380 / 2,299,137 / 10,190,068 | identical |
| random `c`, `n = 8`: LS; oracle (seeds 0, 1) | 22,559 / 25,225; 19,590 / 22,075 | identical |
| random `c`, `n = 16`: LS; oracle | 147,538 / 165,598; 114,215 / 111,980 | identical |
| final-pass slope error `nu`, `n = 8` | `1.16e-2` | `1.161e-2` and `1.163e-2` |

One bug in my first version is worth recording. My last-bag Newton safeguard
rejected converged steps and left position errors of about `1e-6`. It did not
change any LS number. I fixed it (the solver now agrees with `brentq` to
`2.2e-16`, `logs/check_inner_solver.log`), and all logs in the checks folder
come from the fixed code.

**Additional data not in the note.** The note does not report the number of
convex programs, that is, (leaf, cell) pairs. For the final LS certificates
with exact slopes, pairs per leaf are 3.5, 4.4, 4.7, 4.9 and 4.8 for
`n = 4..64` (11.46 million programs at `n = 64`). This is comparable to the
3.0–4.8 pairs per leaf reported for the shell certificates of [D]. So the
size comparison of C.1 also holds for convex programs in the final
certificate. It does not hold for total work, where restarts dominate.

### 4.2 Issue 3: slopes versus incumbent in Section C.2

The note's "oracle" runs start at `x0 = x*`, so `UBD = f*` from the first
sweep (`run_ls.py`, modes `oracle` and `random`). The same holds for the
`c = 0` table of C.1, where `x0 = 0 = x*`. The note does not state this.
The LS rows use a learned incumbent. In the final LS pass the incumbent was
still `0.27–0.76 eps` above `f*` at the start of the pass.

`check_slope_vs_incumbent.py` reruns the final pass with each ingredient
swapped (size relative to exact slopes with exact incumbent):

| Instance | slopes of LS, exact incumbent | exact slopes, incumbent of LS | both (= LS) |
|---|---|---|---|
| `n = 8`, seed 0 | 1.074 | 1.022 | 1.152 |
| `n = 8`, seed 1 | 1.078 | 1.020 | 1.143 |
| `n = 16`, seed 0 | 1.103 | 1.060 | 1.292 |
| `n = 16`, seed 1 | 1.253 | 1.161 | 1.479 |

So "learned slopes cost 14–48% more certificate size than exact slopes"
should read: learned slopes and a learned incumbent together cost 14–48%;
slopes alone cost 7–25%, and the incumbent alone 2–16%.

The incumbent also explains part of the value of restarts. One pass with the
exact slopes but `x0 = 0` gives 45,491 and 53,506 at `n = 8`, about twice the
size of LS with restarts (22,559 and 25,225;
`logs/indep_random_n8_eps1e-4.log`).

### 4.3 Issue 4: re-centering (RC)

- **`n = 8`, `c = 0`.** My re-run (`check_rc_indep.py`, own DP, the reviewed
  `shells` of [D]) matches the author's log to all printed digits through
  round 18. It shows the same period-2 cycle and the same stuck
  `UBD = 1.0126e-6`. The added column `exact-inc-stop` shows that at rounds
  15 and 17 the root gap is `9.206e-7 < eps`. The lower bound had reached
  the tolerance, and RC failed only because its incumbent (`F` at consistent
  points) was `1.01e-6` above `f*`. The centre does drift away in units of
  `h_j` (16 → 160 `h_j` from round 15 to 18), so the note's description is
  accurate as far as it goes. But this run is evidence against RC's
  incumbent rule, not against localization of the minimizing configuration.
  Section A.5 should say so.
- **`n = 16`, random `c`, seed 0.** My re-run also diverges, but along a
  different path. The incumbent never improves on `F(0) = 0`, the gap stays
  between 0.25 and 1.05, and the centre error reaches 5,657 `h_j` at
  round 14. The author's run instead reaches `UBD = -0.1356` with a gap
  cycling between `1.6e-2` and `2.9e-2`.
  - The two runs differ from round 1 on, although both DPs give identical
    root bounds on identical partitions.
  - The cause: the round-0 consistent point has coordinates exactly at
    `±1`, and the two implementations' consistent points differ by up to
    `7.7e-9`. Perturbing a single `±1` coordinate of the centre by `1e-9`
    changes the round-1 root bound by up to 0.19
    (`logs/check_rc_sensitivity.log`). Shell partitions around a centre on
    the boundary of the box are discontinuous in the centre.
  - So "RC diverges at `n = 16`" is reproducible. The cycle values and the
    stalled incumbent are one realization of an ill-conditioned iteration
    and should not be quoted as properties of RC.
- **`n = 16` with a local solve.** Not re-run. The logs are consistent with
  the note.

## 5. Smaller corrections

- **Section A.5, obstacle 1 (issue 2).** The proof of Proposition A.6 uses
  that at sublevel `i` every other bag has leaves of level `<= i` at the
  alternating point, so each contributes a deficit of at least `0.2 s^2`.
  A refinement order that is not level-synchronous (for example, refining
  near the minimizing configuration first) can shrink those deficits before
  far boxes are tested. The statement should be limited to level-synchronous
  refinement, or to rules that test all bags at a common width. Section D
  already scopes it correctly ("rules out LS").
- **Theorem A.5(a).** The bound on `nu_p` holds whenever pass `p` runs
  (pass `p - 1` did not stop). Part (b) uses it for passes that do stop.
  State it that way; the proof already supports it.
- **"About `5.8 sqrt(n)`".** The ratios `|x^cons - x*|_2/(s sqrt(n))` are
  2.6, 4.0, 5.4, 5.7 and 5.8 for `n = 4..64`, so 5.8 holds only from
  `n = 32`. The consistent point is exactly self-similar across levels on
  the symmetric `c = 0` instance, which is why the ratios are "identical to
  two digits". Supporting data not quoted in the note: on the non-symmetric
  random-`c` runs (`n = 8, 16`), `|x^cons - x*|_inf/s` stays between 3.1
  and 7.2 (author's logs). This mildly supports Conjecture A.7 beyond the
  symmetric case.
- **"About `22 n` split leaves per bag per level".** This is the maximum
  over levels. At `n = 64` it is attained at level 6 (1,428). The plateau at
  levels 8–12 is about 1,290, that is, `20 n`.
- **"The restarts multiply the processed count by about 20".** The factor 20
  is processed count over final size. A single pass already has a ratio of
  4.0–6.2 (oracle rows in C.1 and C.2). Compared with a single oracle pass at
  the same `eps`, restarts multiply the processed count by 5.0–6.5
  (C.2 rows).
- **Section B.5, item 3.** "Loses a factor 2 per edge" is a degradation of
  the lower bound `m' >= m̃/2`. It is not a shown thinning of the reduced
  bands. The summary's "can thin out" should say "the available bound
  thins".
- **Command table.** The RC random log ends after round 21, not round 20.

## 6. Not checked

- Novelty, beyond the note's own disclaimer.
- The continuous-separator sketch after Theorem B.2.
- Remark A.8.
- The RC runs with a local solve.
- LS with restarts at `eps = 1e-6` for `n > 32`.

## 7. Commands run (targeted; from `reviews/decomposition-adaptive-review-checks/`)

All runs used `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`,
Python 3.13.11, NumPy 2.5.1, SciPy 1.18.0. No project-wide verification was
run, and CI was not consulted.

| Command | Log | Result |
|---|---|---|
| `python3 check_minmarginals.py` | `logs/check_minmarginals.log` | Lemma A.1 verified by enumeration |
| `python3 run_indep_ls.py oracle "4 8 16 32 64" 1e-6` | `logs/indep_oracle_eps1e-6.log` | C.1 exact-slope table reproduced exactly |
| `python3 run_indep_ls.py scaling "4 8 16 32" 1e-4` | `logs/indep_scaling_eps1e-4.log` | C.1 restart table reproduced exactly |
| `python3 run_indep_ls.py random "8" 1e-4` | `logs/indep_random_n8_eps1e-4.log` | C.2 `n = 8` reproduced; one-pass exact slopes from `x0 = 0` |
| `python3 check_slope_vs_incumbent.py 8 1e-4`, `... 16 1e-4` | `logs/check_slope_vs_incumbent_n8.log`, `..._n16.log` | C.2 `n = 16` LS and oracle reproduced; slope and incumbent split (Section 4.2) |
| `python3 check_localization.py "4 8 16 32" 1e-6` | `logs/check_localization.log` | measured split radius about `3 sqrt(n) s_i` |
| `python3 check_propA6.py` | `logs/check_propA6.log` | Proposition A.6 step 2 inequality holds (worst `-1.097`) |
| `python3 check_constants.py` | `logs/check_constants.log` | Section A.3 constants confirmed |
| `python3 check_staircase_indep.py` | `logs/check_staircase_indep.log` | Theorem B.2 certificate confirmed; `w^{Theta(w)}` gap between `N_dec` and `Phi` |
| `python3 check_rc_indep.py zero 8 1e-6 18`, `... random 16 1e-4 14` | `logs/check_rc_zero_n8.log`, `logs/check_rc_random_n16.log` | Section 4.3 |
| inline scripts (recorded in logs) | `logs/check_inner_solver.log`, `logs/check_rc_sensitivity.log` | solver accuracy; RC sensitivity to the centre |
