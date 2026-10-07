# Referee report: consistency relaxations on tree decompositions

Date: 2026-09-30. Note under review:
[`../theory-consistency/consistency-relaxations.md`](../theory-consistency/consistency-relaxations.md)
("the note"). Reviewer: independent research agent that did not write the
note. Checks and logs: [`consistency-review-checks/`](consistency-review-checks/).
All numerical checks are floating-point (numpy 2.5.1, scipy 1.18.0/HiGHS);
Remez values carry de la Vallée Poussin lower bounds, which are rigorous up
to floating-point rounding. No project-wide verification and no CI
inspection were done. I did not run the author's scripts; every numerical
check below uses independent code.

## Overall assessment

The mathematical core is sound. I checked every proof in Sections 1–5 line
by line. I found no false theorem.

- The band identity (Theorem 2.1) is correct, with the exact constant 2.
- The tree sandwich (Theorem 3.1) and the counterexample to per-edge
  control (Proposition 3.3) are correct.
- The kink lower bound (Proposition 5.6) is correct.
- The two-dimensional counterexample to Proposition 5.4(a) is correct. It
  is even realized by a box problem with bilinear data.

The problems are in interpretation, numbers, and literature attribution:

1. The note says it "explains" the repository's sparse rates. This holds for
   the lower bounds, that is, for the ideal relaxation. For the upper rates
   the explanation is conditional or circular.
2. The limit of `n^2 gap` for the quadratic example is about `0.279`, not
   `0.288`.
3. The "factor 8 and 12" gains come from evaluating identities that [S]
   already proved. They are asymptotic and numerical.
4. The aligned hp value at `p = 12` is `1.65e-10`, not `1.3e-10`.
5. The hp rates are headlined in coefficient count `N`, although the note
   itself says `N` is not the cost.
6. Alfonsi et al. are mischaracterized.
7. The pinch-regularity lemma is classical, so it cannot be listed as
   "not found elsewhere".
8. The solver rule (E) is a heuristic. Part of it applies one-separator
   logic edge by edge, which Proposition 3.3 shows is unsafe on trees.

## Verdicts by claim

| Claim | Verdict |
|---|---|
| (A) Theorem 1.1 duality | correct (minor fix F11) |
| (A) Proposition 1.2 attainment | correct |
| (A) Proposition 1.3 "envelope loses nothing" | correct for continuous classes; fix F13 for cellwise classes; wording |
| (A) Proposition 1.4 | correct |
| (B) Theorem 2.1 band identity, constant 2 | correct (minor proof fix F12) |
| (B) Corollary 2.2 (1)–(5) | correct |
| (B) Proposition 2.3 cellwise max, PC closed form | correct |
| (B) Theorem 3.1 tree sandwich | correct; "both ends attained" needs wording fix F6 |
| (B) Propositions 3.2, 3.3; Corollary 3.4 | correct |
| (C) Proposition 5.6 `gap >= 1/(30(3+c)n)` | correct (harmless arithmetic slip F18) |
| (C) `n gap -> 2 beta`, 0.5602 at `n = 64` | correct (E1, zero width) |
| (C) "`n gap` rises toward `2 beta`" for `c > 0` | unsupported as a limit statement (F16) |
| (C) PC closed form ~ [D, Proposition 2.6] | correct as an analogue |
| (D) Lemmas 4.1, 4.2 | correct; Lemma 4.2 classical (F5) |
| (D) Proposition 4.3 | sketch (as labelled) |
| (D) Proposition 5.4 (a)–(c), 2D counterexample | correct |
| (D) Corollary 5.5 shells | correct with fixes (F10) |
| (D) Proposition 5.5, Corollary 5.7 | correct; Corollary 5.7 wording (F3) |
| (D) "explains `O(R^-2)` vs `Theta(R^-1)`" | correct for lower bounds and the ideal relaxation; gap for upper rates (F3) |
| (D) factors 8 and 12 | about 7.9 and about 11.8 asymptotically (F1, F2) |
| (D) hp aligned `exp(-bN)` | correct (trivial given alignment); value fix F7 |
| (D) hp unaligned `exp(-b sqrt N)` | correct in substance; citation and cost fixes (F8, F9) |
| (E) solver rule | heuristic; partly unjustified on trees (F14) |
| (F) literature and novelty | mostly accurate; fixes F4, F5, F20 |

## (A) Duality

**Theorem 1.1.** Sion's hypotheses hold:

- `M = prod M_t` is convex and weak*-compact;
- `f(·, phi)` is affine and weak*-continuous, since `F_t^phi` is in `C(X_t)`;
- `f(L, ·)` is linear.

The inner supremum over the vector space `Phi_e` gives the agreement
constraints. The minimum on the `L` side is attained because a supremum of
continuous functions is lsc on a compact set. The listed hypotheses are
sufficient. Nonemptiness of `M_t` and the normalization `L(1) = 1` (so that
constants telescope) are also used.

- **F11 (Example 2, compactness).** Compactness of the truncated moment
  set depends on the generators.
  - With `1 - x_i^2` (the generators of [S]), localizing constraints give
    `L(x^{2 beta}) <= 1`, and PSD then bounds all moments.
  - With the linear generators `1 ± x_i`, compactness fails at low order.
    In 1D at order 1, `(1, y1, y2)` with `y2 >= y1^2` and `|y1| <= 1` leaves
    `y2` unbounded.
  - State the generators, for example `(u_i - x_i)(x_i - l_i)`.
- **Polynomial-split lemma.** The tree extension of [R, Lemma 1.1] is
  correct. It uses running intersection and the product domain.

**Proposition 1.2.** Correct. `sum_t D_t = 0` identically. If
`sum min D_t = 0`, every `D_t` is constant, and propagating from the leaves
makes every `d_e` constant. Coercivity holds modulo constants.

**Proposition 1.3.**

- (1) is trivial and holds for any bounded `F`.
- (2) is correct for continuous classes: the envelope has a measure
  representation, and by running intersection, consistent means define one
  point.
- **F13.** For the discontinuous cellwise classes used later, Theorem 1.1's
  continuity hypothesis fails. The statement still holds if `vex` is the
  closed convex envelope. Affine minorants of `f` and of its lsc hull
  coincide, `inf` is unchanged, and Sion only needs lower semicontinuity in
  the measures. Say this, or restrict (2) to `Phi ⊂ C`.
- **Wording.** "The envelope step loses nothing" is true for *per-bag*
  envelopes. Solvers use per-factor envelopes (McCormick, alphaBB), which
  are weaker when a bag holds several factors. Say "per-bag" in the
  summary.

**Proposition 1.4.** Correct.

## (B) Band identity and trees

**Definitions.**

- `U` is the child-side value function and `V` the parent-side one.
- `L = f* - V <= U`, since `f* = inf(U + V)`.
- The child bag receives `-phi` and the parent `+phi`, so
  `inf(G_A - phi) = -sup(phi - U)` and `inf(G_B + phi) = f* - sup(L - phi)`.
  The first equality is correct.

**Theorem 2.1, both directions.**

- *Upper direction:* `bracket <= osc(phi - psi)`, and with constants in
  `Phi`, `inf_phi osc = 2 dist`.
- *Lower direction:* shift `phi` by a constant, then clip it into `[L, U]`.
  Then `phi - psi` takes values in `[-b, a]` with `a, b >= 0`, so
  `2 dist <= a + b`.
- The constant 2 is exact: the statement is an identity, attained in every
  case.

**F12.** The proof says "since `L = U` at a pinch point, `a + b >= 0`".
Pinch points need not exist if `inf(U + V)` is not attained. Use
`a + b >= sup(L - U) = -inf w = 0` instead.

**Must the class contain the constants?** Constants telescope, so
`rho(Phi) = rho(Phi + R)` for every class. Without constants the formula
must be read with `Phi + R`. I checked this on 1779 random discrete
instances (R1):

- with constants in `Phi`: `|gap - 2 dist(Phi, Band)| <= 3.1e-14`;
- without constants: `gap = 2 dist(Phi + R, Band)` to `8e-13`, while
  `gap != 2 dist(Phi, Band)` in 1489 of 1779 cases.

Add one sentence saying that the hypothesis costs nothing.

**Attainment.**

- For finite-dimensional `Phi`, the split supremum is attained
  (Proposition 1.2).
- The distance is attained, because bounded sequences in `Phi` have
  convergent subsequences and the band is closed.
- For infinite-dimensional classes the identity holds with infima.

**Corollary 2.2.**

- (3) holds with `- sup w`, not `- 2 sup w`. Constants allow centering
  `U - psi` in `[0, sup w]`. Verified numerically (R1-B).
- (4) holds: a narrower band on `I` only increases the bracket.
- (5) holds: minimax over pairs of probability measures.

**Proposition 2.3.** Correct.

- The "`<=`" direction needs per-cell centering, which works because
  `a_D + b_D <= G`.
- R1-B checks it three ways for PC and PA on 2, 4 and 8 cells: joint LP,
  maximum of cell brackets, and the PC closed form. All agree to LP
  precision.

**Theorem 3.1.**

- *Upper bound.* Correct. It is the shift-by-constants argument of
  de Farias–Van Roy. With the DP split on a path, it is the deterministic
  finite-horizon ALP bound (F20).
- *Lower bound.* Correct. Enlarging the other classes to `B(X_e')`, the
  sides decouple and the DP split is in the full class. [D, Observation
  4.2] with infima turns each side into its super-bag infimum.
- *Random tests (R2).* 300 random 3-bag chains with classes of degree 0–2
  (900 cases). Here the bands are computed from explicit value functions,
  not by giving the other edge the full class. Results:
  - the lower bound `2 max_e dist <= gap` was never violated;
  - the DP-split upper bound was never violated;
  - the sequential bound of Corollary 3.4 was never violated;
  - the per-edge sum was below the gap in 280 cases, including cases where
    both per-edge distances are 0 and the gap is positive.
- **F6.** "Both ends are attained (T1)" is inaccurate for the lower end.
  - In the continuum, `gap/2E_n -> 1` only as `K -> inf`. I get 1.0025 at
    `K = 100` and `n = 4`.
  - The value 1.0000 at `K = 1000` on a grid comes from the grid enforcing
    `s1 = s2`.
  - Say "the lower end is approached as `K -> inf`". It is attained exactly
    in trivial cases, such as one edge.

**Proposition 3.3.** Verified by hand and on a grid (R2).

- `f* = F(1,1) = 1` and `rho(R) = 0`.
- `V_1 = 1` exactly: the coefficient of `s2` is `-9 - s1 < 0`, so the
  minimum is at `s2 = 1`. Hence `L_1 = 0`, and `0` is in `Band_1`.
- For the `M` family, `L_1 = (1 - M)(1 - s1)`, so
  `2 dist(R, Band_e) = 1 - M`. Confirmed for `M = 0.8` and `0.6`
  (0.2 and 0.4 per edge, gap 1).
- The sequential bound of Corollary 3.4 equals 1 there, so it is tight.
- The per-edge version of (B) is false, as claimed.

**Proposition 3.2 and Corollary 3.4.** Correct.

- The "what carries over" paragraph is right. With disjoint separators,
  an absorbed `phi_e` does not depend on the next separator, so the
  semiconcavity constants survive, even for discontinuous `phi_e`.
- The later bound `sum_e (M_L + M_U) h^2/8` on paths of pairs follows.

## (C) Lower bounds and Bernstein's constant

**Proposition 5.6, step by step.**

- *Step 2:* the divided-difference bounds, and `q(±4 delta) = ∓1/2` or
  beyond, giving `|q'(xi)| >= 1/(8 delta)`.
- *Step 3:* the even/odd split with `r(s^2)` and `s u(s^2)`. The Chebyshev
  extremal bound gives `|T_m((1+a)/(1-a))| <= ((1+delta)/(1-delta))^m`
  with `a = delta^2`. Then `exp(8/7)`, and `2 e^{8/7} = 6.27`.
- *Step 4:* Bernstein's inequality at `|xi| < 1/2`.
- The small cases (`delta >= min(1/8, 1/n)`, `n = 1`) are covered.
- The scaled version follows from Corollary 2.2(4). A narrower band only
  raises the bracket, and `A` is in `P_n` for `n >= 1`.
- **F18 (harmless).** `8 × 7.3 = 58.4`, not 58.1. The final `1/(30 C n)`
  is unaffected.
- *Numerics (R3, own LP on a graded grid).* The bound holds for
  `c = 0.5, 2, 8` and `n = 1, 2, 3, 4, 6, 8, 16, 32`. It is loose by factors
  of 30–70. My LP values match the note's E6 values to all printed digits
  (for example `c = 2`, `n = 4`: 0.2010).

**Which Bernstein constant, and is the factor 2 consistent?**

- `beta = lim 2n E_{2n}(|x|) = 0.2801694990`. The note's `beta` is this one.
- For the zero-width band `U = L = -|s|`, Theorem 2.1 gives
  `gap = 2 E_n(|s|)`, so `n gap -> 2 beta = 0.560339`. The factor 2 is the
  2 of (B) and is consistent.
- An independent Remez computation (R3) gives `n · gap` = 0.540967 (`n = 4`),
  0.559996 (32), 0.560253 (64), 0.560318 (128) and 0.560334 (256).
- The note's 0.5602 at `n = 64` is right. The table's
  `E_64 gap = 0.0087539` matches the Remez value 8.75396e-3.
- **F16.** Section 5.4 says `n gap` "rises toward `2 beta`" for
  `c = 0.5, 2, 8`. The data (0.49, 0.42, 0.33 at `n = 128`) do not show the
  limit. A scaling heuristic makes `2 beta` plausible: at scale `1/n` the
  band width `c s^2` is negligible. Present it as a conjecture.

**Piecewise constants.**

- `gap(PC) = max_D (sup_D L - inf_D U)` is correct.
- The upper bound `min(osc_D L, osc_D U) - w_min` is correct.
- Proposition 5.2's count `|lambda|/sqrt(2 M eps)` is correct. Because
  `w(s) <= F(x* + (s - s*) e_i) - f*`, we have `M <= M_F`. So it has the
  same order as [D, Proposition 2.6] (`|lambda*|/(6 sqrt(M_F eps))`), with
  a larger constant, in the idealized exact-bag model.
- "Reproduces" is fair as "is the idealized analogue of".

## (D) Instances

**Lemma 4.1.** Correct. An infimum over a fixed box of functions that are
`M`-semiconcave in `s` is `M`-semiconcave.

**Lemma 4.2.** Correct. The `tau(h - g)` argument gives `h = g`, and a
singleton superdifferential of a semiconcave function gives
differentiability.

- The sandwich with `A` is correct.
- The distance from `A` to the band is at most `max(M_L, M_U)/2 |v|^2`.
  Note the crossing: `A` can lie below `L` by at most `(M_U/2)|v|^2`.
- **F5.** This is a standard fact of semiconcave analysis. A semiconvex
  function lying below a semiconcave one and touching it at an interior
  point makes both differentiable there with the same gradient. It is also
  immediate from Ilmanen's lemma: a `C^{1,1}` function between them
  touches both. See Cannarsa–Sinestrari 2004, Fathi–Zavidovique 2010 and
  Bernard 2010. Remove the lemma from "not found elsewhere". What is new is
  reading it as "value-function bands have no kinks at interior pinch
  points".

**Proposition 4.3.** It is a sketch, correctly labelled.

- The extension estimate in step 2 omits the `M|s|^2` terms. They do not
  cancel outside the box.
- A local version around the box is needed. That is fixable, but the
  status must stay "sketch".

**Proposition 5.4.**

- (a): the chords argument is correct.
- (b): semiconvexity on convex `X_e` gives global sub- and supergradient
  inequalities. Correct.
- (c): Taylor on convex cells. Correct.
- *2D counterexample.* Verified (R4): the affine cell bracket is
  `1/2 - delta` exactly for `delta = 0, 0.1, 0.25, 0.4, 0.5`.
- *New observation.* With `delta = 0` the example is the band of a box
  problem with bilinear (`C^{1,1}`) data:
  - child bag `u s1 + (1 - u) s2`, `u` in `[0, 1]`;
  - parent bag `v (1 - s1 - s2)`, `v` in `[0, 1]`.

  The affine split gap computed from the bag data is `1/2`. The pinch set
  is the whole boundary of the square. So with smooth box data, boundary
  pinch sets can defeat affine splits at first order in 2D. This does not
  contradict Lemma 4.2, which is interior. It is worth one sentence, because
  it shows that the interior hypothesis carries real weight.
- The `delta > 0` versions are cell-level brackets, not bands of a problem:
  `inf w = 0` fails. The log's "gap = -0.1" at `delta = 0.6` shows this.
  Call them `g_D`, not "gap".

**Corollary 5.5.** Correct with fixes (F10).

- [D, Lemma 3.1] gives `w(B) <= theta · dist_inf(B, s*)`, a minimum
  distance, so the shell cubes satisfy `M r^2 <= w_min`.
- The split "shells inside the ball, cubes of diameter `c rho0^2/(2G)`
  outside" does not tile. Cubes meeting the ball boundary have
  `w_min < c rho0^2`. Put the shells on the inscribed cube
  `Q(s*, rho0/sqrt k)` and use `w >= c rho0^2/k` outside it. Only the
  `O_eps(1)` term changes.
- `O((Mk/c)^{k/2} log(1/eps))` hides a factor of order `4^k`: `(4/theta)^k`,
  with `theta` rounded to a power of 2. Write `O((C M k/c)^{k/2} ...)`.

**Proposition 5.5.**

- (a): Trefethen's Theorem 8.2 gives `2 M rho^{-n}/(rho - 1)` for Chebyshev
  truncation, and the factor 2 of Theorem 2.1 gives `4 M ...`. Correct.
- (b): the multivariate Jackson theorem gives `O(n^-2)` for `C^{1,1}`.
  Correct; `C_k` is uncomputed.

**Curvature jump.** The claims hold:

- the band contains `-s^2` for `c >= 1`;
- no `C^2` band element exists for `0 < c < 1`;
- `O(n^-2)` is *proved*, because `U = -(s_+)^2` is `C^{1,1}` and in the
  band. Only the `Omega(n^-2)` half is numerical.

**E4.** The "0" entries are exact. Checked (R6) with an explicit band
element: `T - kappa (s - 0.3)^2` lies in the band for `kappa` between about
1.296 and 1.5, so `gap(P_n) = 0` for `n >= 2`. Cite this rather than the LP,
whose fine-grid upper estimates rise to `7e-5` at `n = 64`.

### Link to the repository's rates (F1–F3)

**F1 (number).** The note says "`n^2 gap -> 0.288`" for `2 E_n((y_+)^2)`.
Since `(y_+)^2 = (y^2 + y|y|)/2`, this equals `E_n(y|y|)`.

- 0.288 is the value at `n = 64`, and the sequence is still decreasing.
  Remez (R3) gives:

  | `n` | 64 | 128 | 256 | 512 |
  |---|---|---|---|---|
  | `n^2 gap` | 0.28802 | 0.28358 | 0.28138 | 0.28028 |

- The differences halve, so the extrapolated limit is about 0.2792.
- So the ideal gap is about `0.0698/R^2`, not `0.072/R^2`.

**F2 (factors 8 and 12, recomputed).**

- *Affine recourse.* `2 E_{2R}(|y|) ~ beta/R = 0.28017/R` against [S]'s
  `1/(9 pi (R+1)) ~ 0.03537/R`. The asymptotic ratio is
  `9 pi beta = 7.92`. At finite `R` the ratio is 11.47, 9.81, 8.89, 8.41
  and 8.17 for `R = 2, 4, 8, 16, 32`.
- *Quadratic example.* `0.0698/R^2` against `2/(27 pi (2R+2)^2) ~ 0.005895/R^2`.
  The asymptotic ratio is 11.8 (not 12.2). At finite `R` it is 42.2, 23.5,
  16.9, 14.2 and 13.0.
- **Attribution.** "The identity raises the lower-bound constants" credits
  the wrong source. The identities `-rho >= 2 E_{2R}` are [S]'s own
  Propositions 1 and 2. The gain comes only from evaluating `E_n`, with
  Bernstein's classical constant for `|y|` and floating-point values for
  `y|y|`.
- These are asymptotic or numerical, not certified finite-`R` bounds.
  Certifying them needs interval-arithmetic de la Vallée Poussin bounds,
  which are easy to add.

**F3 (the "explanation").** It holds for the lower-bound side:

- the ideal relaxation's gap is exactly `2 dist(P_{2R}, Band)`;
- it lower-bounds the SDP gap;
- so kinks at pinch points force `Omega(1/R)` in 1D (Proposition 5.6).

For the upper rates it does not explain [S]:

- The SDP gap also contains the bag-relaxation error
  `sum_t delta_t(F_t^phi)` (Proposition 1.4), which depends on the split
  and is not analysed here.
- The independent route to `dist(P_n, Band) = O(n^-2)` is
  Proposition 4.3. It is a sketch, and it needs an interior pinch point and
  `w >= delta_0` on `∂X_e`.
- Corollary 5.7 *derives* band approximability *from* [S]'s theorem, so it
  cannot explain that theorem.
- Rephrase the summary and the end of Section 5.4:

  > The band identity gives the exact value of the ideal relaxation, which
  > explains the lower bounds and the mechanism, `R^-1` from kinks at pinch
  > points. The `O(R^-2)` upper rates of [S] are consistent with it, and are
  > explained by it conditionally on Proposition 4.3.

- *Corollary 5.7 wording.* The proof gives, for each `n`, a band element
  within `O(n^-2)` of `P_n`. It does not give one fixed band function with
  `E_n = O(n^-2)`, which is what the sentence "the band ... always contains
  functions that polynomials of degree `n` approximate to `O(n^-2)`" can be
  read to say.

### hp classes (F7–F9)

**F7 (value).** The aligned two-cell value at `p = 12` is `1.6468e-10`,
not `1.311e-10`.

- This is a Remez de la Vallée Poussin lower bound (`8.2342e-11` per cell)
  together with the Chebyshev-interpolant upper bound (R5).
- `p = 4` and `p = 8` agree with the note: `6.1743e-3` and `2.4245e-6`.
- The note's value is a grid-LP lower estimate at the LP tolerance. The
  adaptive `3.2e-10` entry has the same status. Label such entries as
  lower estimates, or use Remez.

**F8 (basis and citation).**

- *Aligned case.* Proposition 5.8 is correct and trivial: the maximum over
  cells of `2 E_p`.
- *Unaligned case.* Gui–Babuška (1986) treat `x^alpha` singularities
  located at mesh nodes, in the energy norm. The note's unaligned kink is
  inside the smallest cell. The `exp(-b sqrt N)` rate there follows from an
  elementary argument: the singular cell's error is proportional to its
  width `sigma^m`, the other cells need degree `O(m)`, and `N ~ m^2`.
- For sup-norm free-knot, variable-degree approximation, cite
  DeVore–Scherer (1980, "Variable knot, variable degree spline
  approximation to `x^beta`").
- The sentence "if the cells are placed without knowing the kinks, a
  geometric mesh graded toward each kink" contradicts itself. Grading needs
  approximate kink locations, as in bisection toward a detected kink.

**F9 (cost measure).** `N` is not the right cost measure, as Proposition
5.9 itself says. Yet "exponential in `N`" is a headline, and Section 6
ranks strategies by `N`. In cost terms (moment relaxations of the bags):

- *Aligned hp* reaches `eps` with `p ~ log(1/eps)`. The incident bag blocks
  then have side `binom(|V_t| + p/2, p/2) ~ (log 1/eps)^{|V_t|}/|V_t|!`.
- *PA shells* (1D separators, path of pairs) need `O(log^2(1/eps))`
  fixed-size subproblems per bag.
- So for `|V_t| >= 3`, h-refinement can be cheaper than hp. The `N`
  comparisons (32 vs 124 vs 512) are not cost comparisons.
- Restate the hp claims in the Proposition 5.9 cost: cells times block
  sizes. Otherwise mark `N` as a proxy for the idealized exact-bag model.

## (E) Solver rule

The rule is a heuristic, as the status table says. The summary should say
so too.

**Justified by theory:**

- *Step 1:* by Proposition 5.1(2)–(3), local multipliers are the only
  candidate slopes for an exact affine split at an interior `C^1` optimum.
  The check certifies only if the local point `x̂` is a global minimizer.
- *Kinks away from the pinch set are harmless:* Proposition 2.3 and E4.

**Not justified on trees:**

- The rule applies per-separator decisions "edge by edge" using the
  *original* `U_e` and `w_e`. Step 3's "leave a cell if `w_e` exceeds the
  target" is sound for one separator (Proposition 2.3).
- On trees, the bands after absorbing earlier splits can be thinner.
  Corollary 3.4 says quadratic growth "need not survive". Proposition 3.3
  shows that original-band diagnostics can report zero loss on every edge
  while the gap is 1.
- **F14.** Base per-edge decisions on the *reduced* bands of Corollary 3.4
  (sequential elimination), or on the joint dual marginals. Or state
  explicitly that the edge-by-edge use is unjustified.
- The Chebyshev decay threshold (0.8) and the kink detector were tested on
  one 1D function.

**Interpretation of [O].** The relation to the open-instance certificates
is plausible and is labelled interpretive. That is fine.

## (F) Prior work and what is new

**Checked by me.**

- **de Farias–Van Roy.** I read the NeurIPS 2001 text (Theorem 3.1 there
  is the Lyapunov-weighted form). The note's quotation of the OR 2003 bound
  `||J* - Phi r~||_{1,c} <= (2/(1 - alpha)) min_r ||J* - Phi r||_inf`, with
  `e` in the span, is accurate. The factor 2 has the same origin: shifting
  the best approximant by a constant.
  - **F20.** On a path with the DP split, the upper bound of Theorem 3.1 is
    exactly the deterministic finite-horizon ALP bound. The ALP constraints
    `Phi_t r_t <= g_t + Phi_{t+1} r_{t+1}` are the split relaxation.
  - So the upper half is "known in substance" in that case. What is new is
    the infimum over all exact splits, the `2 max_e` lower bound, and the
    counterexample.
- **Alfonsi–Coyaud–Ehrlacher–Lombardi** (arXiv 1905.05663, Section 5 read).
  - Proposition 5.1 gives `I^N <= I <= I^N + K/N` for piecewise constants
    and a `K`-Lipschitz cost; Wasserstein bounds come from moving mass
    within cells.
  - The `O(1/N^2)` rate for piecewise affine test functions comes from a
    first-order Taylor expansion of a `C^{1,1}` cost on product cells.
    For `|x - y|^p` there is an extra marginal condition.
  - **F4.** The rates do *not* "come from approximating the Kantorovich
    potentials". Correct the description. The structural analogy with
    Sections 5.2–5.3 (cellwise test functions; first vs second order)
    stands.
- **Korda–Magron–Ríos-Zertuche** (arXiv 2303.14824, Section 3 read).
  - To split `f = f1 + f2 >= eps`, they take `g(x) = min_y f2(x, y) - eps/2`,
    a one-sided value function shifted into the `eps`-widened band. They
    approximate it by a Jackson polynomial to within `eps/2 - eta`.
  - This is the sufficiency direction of Theorem 2.1 for a band of positive
    width, in the SOS setting. It yields only a first-order (Lipschitz)
    approximation.
  - The equality and the clipping (necessity) direction are not there. The
    "not found" item 1 should say that KMR use the upper-bound direction.
- **Bernstein's constant.** The value `0.2801694990` (Varga–Carpenter) and
  the definition `lim 2n E_{2n}(|x|)` are confirmed.
- **Ilmanen's lemma.** Fathi–Zavidovique and Bernard (arXiv 1007.3463)
  confirm the insertion lemma, from which Lemma 4.2 is immediate (F5).

**Searches with no hit.** Several searches found no statement of:

- `gap = 2 dist(Phi, Band)` with a two-sided band;
- the tree sandwich with a lower bound;
- the per-edge counterexample.

The searches covered Lagrangian or dual-decomposition bounds with
restricted multiplier or message classes, continuous-MRF dual
decomposition, and ALP. An unsuccessful search does not establish novelty.

**Precise novelty statement.** I recommend the following:

- *Known in substance:*
  - duality (A);
  - the zero-width identity (Han–Jiao–Weissman; [S]);
  - the one-sided "`gap <= 2 ×` approximation error, with constants" (ALP);
  - its positive-width sufficiency form (KMR's construction);
  - the band-bracket form `Delta(Phi)` (already in [R, Proposition 3.3 and
    Section 3.4] in this repository);
  - the pinch-regularity fact (semiconcave analysis);
  - hp rates (DeVore–Scherer, Gui–Babuška).
- *New, as far as found:*
  - the exact identity `Delta = 2 dist(Phi, Band)` via clipping, and the
    max-over-cells formula;
  - the tree lower bound `2 max_e`, the infimum over joint exact splits,
    and the counterexample to per-edge control;
  - the `Omega(1/n)` bound for kinked pinch points with positive width;
  - the observation that affine splits are second order at interior pinch
    points of box problems, together with the 2D failure at boundary pinch
    sets (my R4 addition);
  - the idealized shell count.
- All of the new items are elementary. Their value is in organizing the
  quantity that matters, as the note says.

## Required fixes (summary)

1. **F1.** Replace "`n^2 gap -> 0.288`" and "`0.072/R^2`" with "0.288 at
   `n = 64`, decreasing; extrapolated about 0.279, that is about
   `0.070/R^2`". The factor becomes about 11.8, and 13.0 at `R = 32`.
2. **F2.** Credit the constant gains to evaluating [S]'s own identities.
   Label them asymptotic or numerical, and give the finite-`R` ratios.
3. **F3.** Limit "explains" to the ideal relaxation and the lower bounds.
   Say that the upper rates need the bag-relaxation error and
   Proposition 4.3 (a sketch), and that Corollary 5.7 is derived from [S].
   Fix the wording of Corollary 5.7.
4. **F4.** Correct the description of Alfonsi et al.
5. **F5.** Lemma 4.2 is classical; drop it from "not found".
6. **F6.** Change "both ends attained" to "the lower end is approached as
   `K -> inf`".
7. **F7.** The aligned `p = 12` value is `1.65e-10`. Label LP values near
   the tolerance as lower estimates.
8. **F8.** Fix the hp citation: an elementary argument plus DeVore–Scherer;
   Gui–Babuška is for node singularities. Fix the self-contradictory
   sentence about unknown kinks.
9. **F9.** State the hp rates in the Proposition 5.9 cost, or mark `N` as a
   proxy. h-shells can be cheaper.
10. **F10.** Fix the tiling in Corollary 5.5 (inscribed cube). Expose the
    `C^k` factor.
11. **F11.** Specify the box generators `1 - x_i^2` for compactness.
12. **F12.** In Theorem 2.1, get `a + b >= 0` from `inf w = 0`. Add that a
    class without constants is handled by `Phi + R`.
13. **F13.** For cellwise classes in Proposition 1.3(2), use lsc hulls or
    restrict to continuous classes. Say "per-bag" envelopes.
14. **F14.** Mark the solver rule as heuristic in the summary. Base tree
    decisions on reduced bands or on dual marginals.
15. **F16.** The limit `2 beta` for `c > 0` is a conjecture.
16. **F18, minor.**
    - `58.1` should read `58.4`.
    - The script docstrings use stale numbering: "Theorem 3.2",
      "Remark 3.4", "Proposition 4.1".
    - The `delta > 0` 2D values are cell brackets `g_D`, not gaps.
    - Cite the explicit quadratic band element for E4.
17. **F20.** Identify the path/DP-split upper bound with the finite-horizon
    ALP bound, and refine the novelty list as above.

## Commands run (targeted checks only)

All commands were run in
`research-20260929/reviews/consistency-review-checks/`, with logs in `logs/`:

```
python3 r1_band_identity.py   # 1779 random one-separator cases + explicit-bag example; 17 s
python3 r2_tree.py            # Prop 3.3 family, 900 random 3-bag chains, T1 sweep; 10 s
python3 r3_kink_rates.py      # Remez E_n(|x|) to n=256, E_n(x|x|) to n=512, E6(c) LP, factors; a few minutes
python3 r4_2d_affine.py       # 2D sandwich: bilinear realization and 1/2 - delta
python3 r5_hp_aligned.py      # aligned hp bracket at p = 4, 8, 12
python3 r6_e4_band_element.py # explicit quadratic band element for E4
```

- The hp section of `r3_kink_rates.py` failed to level at `p = 12` on the
  right cell, whose error is at round-off. `r5_hp_aligned.py` replaces it.
- Web sources read:
  - de Farias–Van Roy, NeurIPS 2001;
  - Alfonsi et al., arXiv 1905.05663, Section 5;
  - Korda–Magron–Ríos-Zertuche, arXiv 2303.14824, Section 3;
  - search results on Bernstein's constant and Ilmanen's lemma.
- No project-wide verification, no CI inspection, no edits to the note,
  no commits.
