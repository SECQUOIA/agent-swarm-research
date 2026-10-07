# Referee recheck: "Decomposition certificates for spatial branch-and-bound" (revised version)

Date: 2026-09-30. Note under review:
`research-20260929/theory-decomposition/decomposition-certificates.md`
(the version revised after `reviews/decomposition-review.md`; revision
listed in its Section 8). Line numbers refer to that version. I did not write
the note or the earlier review. My scripts and logs are in
`research-20260929/reviews/decomposition-recheck-checks/`. I ran targeted
checks only: no project-wide verification and no CI (AGENTS.md). The
face-exact note is being rechecked separately. Here I check only that its
hypothesis (M_b) holds and that its Theorem 1 is cited correctly.

## Verdict in brief

1. **Theorem 4.1 (separation): correct except for one rounding error.**
   - The case split, the constants and the proof are right.
   - The uniform ratio is stated with base `1.3155`, which is larger than
     `sqrt(2e/pi) = 1.3154892`. So the stated bound
     `3e-10 * 1.3155^n/sqrt(n)` does not follow for large `n`:
     - the proof's case 1 gives it only for `n <= 7035`;
     - the claim itself is false from about `n = 2.7e5` on, at extremely
       small `eps`.
   - *Fix:* write `(2e/pi)^{n/2}` in place of `1.3155^n`. One constant also
     needs a small correction (`3.2e-10` should be `3.1e-10`).
   - The McCormick version is correct, with `c = 1e-8`.
   - The grid minimum `1.26e-9` is reproduced. It is also the true
     infimum over all `eps <= 1e-4` for `n <= 300`.
   - The face-exact citation is correct: (M_b), (Q_2), `rho = 1.25`,
     `lambda = 5/9` and `eps'' = 1.25 eps` all check.
2. **Observation 4.2 is correct.** It holds for continuous factors on
   compact boxes; the minima are attained, and the disintegration exists.
   - Three small fixes:
     - On the decomposition side the smallest certificate has
       `2|T| - 1` members (one leaf per bag and one cell per separator),
       not "one node".
     - One "=" in the proof should be ">=".
     - The measure form is classical (Vorob'ev 1962; Lasserre 2006) and
       should be cited as such.
   - What it implies: over all splits into bag functions, the minimum
     certificate size is 1 for single trees (and `2|T| - 1` for
     decomposition certificates) whenever each per-factor relaxation is
     exact at the factor's minimum on every box, as convex envelopes are.
     So no single-tree lower bound, and no separation, can hold uniformly
     over all splits.
   - It says nothing about lower bounds that hold uniformly over a
     restricted class of splits. Examples are redistributions of the given
     algebraic terms (the balanced split is one) and splits under a fixed
     relaxation rule such as Hessian-based alphaBB (Section 2.3).
3. **Remarks 3.5 and 3.6 and the program count are correct.**
   - Remark 3.6: my own dynamic program confirms that `theta = 1/8` fails
     from `n = 17` on, at `h = 2^-6`, `2^-8` and `2^-10`. The onset does not
     depend on `h`.
   - Remark 3.5: I rederived `nu <= k^{3/2} M_a |x̂ - x*|_2`.
   - Pair counts: my counts match the note's exactly. They are exactly
     quadratic in `log2(1/h)`, which confirms `Theta(log^2)`.
   - One minor point from the first review is still open: the center must
     lie in `X0`.
4. **Berenguel et al. (2013): read in full** (open access, CC BY; PDF
   obtained).
   - It proposes an interval B&B that keeps one list per subfunction. The
     subfunctions share a single common variable (group), so the structure
     is a star. It uses a relaxed copy of the common variable and
     zero-slope combined bounds.
   - It proves only bound-validity and pruning rules. It has no complexity,
     node-count, lower-bound or separation result, and no multipliers.
   - It anticipates the note's model and algorithm in the one-separator,
     zero-slope, interval-bound case, and should be cited for that.
   - It does not anticipate Theorems 3.4 or 4.1, the lower bounds, or the
     slopes.

## 1. Theorem 4.1: uniform separation and the McCormick version

### 1.1 The two-case proof

The note's proof (lines 1034–1045) splits `eps <= 1e-4` into two cases.
I rederived each step by hand and recomputed every constant
(`logs/ratio_check.log`, section A):

| step | note | recomputed |
|---|---|---|
| Corollary 2.1 prefactor, and with `e^{-1/12}` | 0.0741, 0.068 | 0.07409, 0.06816 |
| case 1: `eps <= 0.04/n^2` gives `log(0.2/(n eps)) >= (1/2) log(1/eps)` | yes | yes (`0.2 eps^{-1/2} >= n`) |
| case 1: `L2 >= log2(225)` (`n >= 3`) | `> 7.8` | 7.8138 |
| case 1: `log2(1.96e6 * 0.2)` | 18.6 | 18.5805 |
| case 1: `(1/2)(18.6 + 1.5 L2) + 2 <= K L2` | `K = 2.2` | `K = 2.1949` |
| case 1: `3.36e7 * 2.2/ln 2` | `1.07e8` | `1.0664e8` |
| case 1: `0.034/1.07e8` | `3.2e-10` | `3.1776e-10` (**below** 3.2e-10) |
| case 2: `(1/2) log2(1.96e6 * 25) + 2` | 14.8 | 14.773 |
| case 2: `(5/3)/1.3155` | 1.2669 | 1.26695 |
| case 2 function at `n = 3` | `1.2e-9` | `1.160e-9`; increasing on `3..400` |

- The two cases cover every `eps <= 1e-4`. Case 1 needs `n >= 3` only for
  `L2 >= log2(225)`.
- Case 2 is nonempty only for `n >= 21` (`0.04/n^2 < 1e-4`). Its smallest
  value on its actual range is therefore `2.5e-8`, not `1.2e-9`. This is
  harmless.
- The first term of (a) is negative for `eps > 0.2/n`. The inequality
  `J_n(T) >= (e^{-1/2}/2) log(T^2/n)` then holds trivially, so
  `N_single >= max(...)` is true for every `eps`.
- The second term of (a) is valid for every `eps >= 0`.

**The error: the base is rounded up.**
- `sqrt(2e/pi) = 1.3154892`, but the ratio statement uses `1.3155`, and
  `ln(1.3155/sqrt(2e/pi)) = 8.17e-6`.
- Case 1 replaces `(2e/pi)^{n/2}` by `1.3155^n` in the step "the first term
  of (a) is at least `0.034 sqrt(n) 1.3155^n log(1/eps)`". That step is
  valid only while the slack between 0.0741 and 0.068 absorbs the
  rounding, which holds for `n <= 10488`.
- Case 1 then gives `3.18e-10 (2e/pi)^{n/2}/sqrt(n)`. This is at least
  `3e-10 * 1.3155^n/sqrt(n)` only for `n <= 7035`.
- **The statement itself fails for large `n`.** Normalized by
  `1.3155^n/sqrt(n)`, the exact infimum over `eps <= 1e-4` of
  `max(first, second)/(b)` is as follows (section C of the log).
  - Why the infimum sits at the crossing: as `eps` decreases, the ratio
    first term / (b) increases to its limit, and the ratio second term / (b)
    decreases. So the infimum is at the `eps` where the two terms are equal.
  - The table:

    | `n` | `ln(1/eps)` at the infimum | normalized ratio |
    |---|---|---|
    | 300 | 3.3e30 | 2.81e-9 |
    | 1e5 | 3.7e10274 | 1.24e-9 |
    | 2.5e5 | 3.9e25688 | 3.6e-10 |
    | 2.8e5 | 2.6e28771 | 2.8e-10 (below 3e-10) |
    | 1e6 | 2.4e102759 | 7.9e-13 |

  - Normalized by `(2e/pi)^{n/2}/sqrt(n)` instead, the infimum is
    `2.806e-9` at every large `n`.
  - The failing `eps` are absurdly small, so the error has no practical
    effect. But the theorem claims the bound for every `n >= 3`.

**Fixes.**
- Replace `1.3155^n` by `(2e/pi)^{n/2}` in every ratio statement:
  - line 70 (Summary);
  - line 145 (status table);
  - line 990 (Theorem 4.1);
  - line 1486 (Section 8).
- In case 1:
  - write "`0.034 sqrt(n) (2e/pi)^{n/2} log(1/eps)`";
  - replace "The ratio is at least `3.2e-10 * ...`" (line 1040) with
    "at least `3.1e-10 (2e/pi)^{n/2}/sqrt(n)`".
- In case 2, divide by `(2e/pi)^{n/2}`. The base becomes
  `(5/3)/sqrt(2e/pi) = 1.26697`, and the argument is unchanged.
- Alternatively, keep a decimal base but round it down, to `1.3154`.
- Optional: say that case 2 applies only for `n >= 21`.

### 1.2 The import of face-exact Theorem 1

- **(M_b).** alphaBB with `alpha = |b|/2` on `b x_i x_{i+1}` has gap
  `(|b|/2)(a_i + a_{i+1})`. Since `a_i = d_i (w_i - d_i) >= d_i^2`, this gap
  is at least `(|b|/2)(d_i^2 + d_{i+1}^2)`, which is at least
  `|b| d_i d_{i+1}`. Summing over edges gives exactly (M_b) as stated in
  the face-exact note (line 179): `Gamma_C >= b sum d_i d_{i+1}`, with
  `b = |b_i| = 0.8`. Unary factors are exact and add no gap.
- **(Q_D) with `D = 2`, `r = 1`.** `F_n(y) <= |y|^2 + b sum y_i y_{i+1}`,
  since `-kappa y^4 <= 0`, and `R = x* + [-1,1]^n = X0`.
- **Parameters.** `rho = D/(2b) = 1.25 <= rho_max = 1.99`, `S = 3/2`,
  `lambda = 5/9`, `eps'' = eps/(b r^2) = 1.25 eps`, and
  `exp(-5/9 * 1.000125) = 0.5738` at `eps = 1e-4`.
- **Correct use of the citation.**
  - The note's single-tree certificate (one bag, `Rel >= l_r >= f* - eps`
    on each leaf) is a certified cover in the face-exact sense.
  - Face-exact Lemma 1.2 covers runs in exactly the generality claimed in
    (a): any branching, node order, valid incumbent and same-relaxation
    tightening, counting leaves plus `2n` pieces per tightening round.
  - Corollary 1.3 there has `b in [0.503, 1)` and `kappa in [0, 1/6]`,
    which cover `b = 0.8` and `kappa = 0.1`.
- **McCormick.**
  - The McCormick envelope of `b x y` dominates alphaBB with `alpha = |b|/2`
    (it is the convex envelope), so its gap is at most
    `(|b|/2)(a_1 + a_2)`. That is (U^q_{0.4}).
  - Face-exact (M_b) holds for McCormick by that note's Lemma 2.1(c).
  - Theorem 3.4 uses only (QG), (L^{1,1}) and (U^q), so (b) holds verbatim.
  - The McCormick claim is therefore correct as stated.

### 1.3 The McCormick ratio and the numerical check

- **McCormick constant.** The constant `c` in
  `N_single/N_dec >= c (5/3)^n/(n log(n/eps))` can be taken as `1e-8`:
  - the grid minimum over `n <= 2000` and `1e-40 <= eps <= 1e-4` is
    `1.03e-8`, at `n = 23`, `eps = 1e-4`;
  - the limit as `eps -> 0` is `2.35e-8 n/(n-1)`.

  "Exponential for each `eps` but not uniformly as `eps -> 0`" is correct
  as a statement about the proven bounds.
- **Grid check (section B).** Over `n = 3..300` and
  `log10(1/eps) in [4, 40]` in steps of 0.005, the smallest normalized ratio
  is `1.2619e-9`, at `n = 4`, `eps = 9.5e-7`. This matches the note's
  `1.26e-9`.
  - The note's script divides by `(2e/pi)^{n/2}`, although its label says
    `1.3155^n`. For `n <= 300` the two differ in the fourth digit only.
- **Beyond the grid (section E).** For `n >= 30` the infimum over `eps` lies
  far below `1e-40`, so the grid alone does not establish the minimum. I
  therefore computed the exact infimum over all `eps <= 1e-4` for every
  `n <= 300`, by the crossing argument above. It is `1.2618e-9`, at the
  same point. The note's number is right.

## 2. Observation 4.2

### 2.1 Correctness

I checked the claims by hand; they need no numerics.

- **The factors.**
  - `g_t = G_t - phi_t(x_{S_t})` depends only on `x_{V_t}`, since
    `S_u ⊆ V_t` for `u in ch(t)`.
  - `g_t >= 0` by the definition of `phi_t` as a minimum.
  - `F = f* + sum_t g_t` (Lemma 1.1; `phi_r = f*` because `S_r = ∅`).
- **Continuity and attainment.**
  - `phi_u(s) = min_y G_u(s, y)` over a fixed compact box, with `G_u`
    jointly continuous by induction, so `phi_u` is continuous (Berge).
  - Hence each `g_t` is continuous and qualifies as a factor in the model of
    Section 1.1.
  - All minima are attained.
- **Envelopes.** `vex_B g_t` is well defined, convex and at most `g_t`. It
  is at least 0 because 0 is a convex minorant.
  - `g_t(x*_{V_t}) = 0` holds as the note says: replacing the subtree
    variables of `x*` by a better subtree solution would lower `F`.
  - So the root bound equals `f*` exactly.
- **Measure form.**
  - `X0_{V_t}` is a compact metric space, hence standard Borel, so regular
    conditional laws of `x_{R_t}` given `x_{S_t}` exist.
  - `R_t` variables are new in top-down order: if `i in R_t` also lay in a
    bag outside `sub(t)`, then `T_i` would contain `p(t)`, so `i` would be
    in `S_t`.
  - Composing finitely many kernels gives a probability measure on `X0`
    whose `V_t`-marginal is `mu_t` for every `t`.
  - The objective is then `∫ F dmu >= f*`.
- **Duality.**
  - Dualizing the marginal constraints with continuous `psi_t` gives
    `sum_t min_{V_t} (a_t - psi_t + sum_{u in ch(t)} psi_u)`.
  - Moreover, every split into bag functions is such a cost shift of the
    original one. If `sum_t delta_t(x_{V_t}) = 0`, peel leaves of `T`: a
    leaf's `delta_t` cannot depend on `x_{R_t}`, so it is a function of
    `x_{S_t}` that can be moved to the parent. So "optimization over splits"
    is exactly the Lagrangian dual.
  - `psi_t = phi_t` is continuous and attains `f*`.

**Fixes (all minor).**
1. Line 1152, "one node certifies every tolerance `eps >= 0`, in a single
   tree and in a decomposition certificate alike".
   - In a decomposition certificate the smallest size is
     `sum_t |L_t| + sum_{t != r} |P_t| = |T| + (|T| - 1)`: one leaf per bag,
     one cell per separator, zero minorants on the cells and `psi = 0`.
   - Say "one node in a single tree, and one leaf per bag (size `2|T| - 1`)
     in a decomposition certificate".
2. Line 1158, "the root bound is `f* + sum_t min vex_{X0} g_t >= f*`".
   - The root bound is `f* + min_x sum_t vex g_t(x_{V_t})`, which is at
     least `f* + sum_t min vex g_t`, not equal to it.
   - Write ">=", and add "and `<= F(x*) = f*`, so it equals `f*`".
3. Line 1162, "Equivalently".
   - The measure statement is the primal (local-consistency relaxation
     exact). The split statement is its dual, with the dual optimum
     attained because `phi_t` is continuous.
   - "Dually" is more precise.
   - Cite the classical sources:
     - Vorob'ev, "Consistent families of measures and their extensions",
       Theory Probab. Appl. 7 (1962), for gluing marginals along
       running-intersection families;
     - Lasserre, SIAM J. Optim. 17(3) (2006), whose sparse moment
       relaxations rely on this gluing;
     - in discrete graphical models, the same fact is tightness of the
       local polytope on junction trees, with the min-marginal
       reparametrization as dual optimum.

     I checked these sources at the bibliographic level only. The note
     labels the statement "the coordinator's observation", so it makes no
     priority claim, but a citation is needed.
4. A useful addition, relating Observation 4.2 to the envelope bound.
   - The envelope bound of a fixed split is itself a Lagrangian bound:
     `vex_B f(x) = min {∫ f dnu : nu on B, mean nu = x}`.
   - So per-factor envelopes enforce only mean (first-moment) consistency of
     the bag copies. This corresponds to affine cost shifts.
   - Observation 4.2 builds the nonlinear dual-optimal shift into the
     factors.

### 2.2 What it implies about lower bounds "uniform over all splits"

Precisely:

- **What it rules out.** Fix `F` and a width-`w` tree decomposition. Take the
  minimum, over all continuous splits `F = sum_t ã_t(x_{V_t})`, of the
  smallest certificate size at any `eps >= 0`. That minimum is 1 for
  single trees and `2|T| - 1` for decomposition certificates. This holds for
  any per-factor relaxation that is exact at each factor's minimum on every
  box: convex envelopes, and even the constant minorant `min_B ã_t`.
  Consequently:
  - no nontrivial single-tree lower bound holds uniformly over all splits;
  - no separation holds uniformly over all splits;
  - both sides collapse, not only the single tree.
- **What it does not rule out.**
  - *Fixed relaxation rules not exact at factor minima.*
    - Take alphaBB with Hessian-derived `alpha`. The conditional margins
      `g_t` are typically not `C^2`, because value functions have kinks
      where the subtree minimizer switches. So the rule may not even apply,
      and where it applies it has a positive gap.
    - A lower bound uniform over splits for a fixed algebraic rule is not
      excluded by the observation.
  - *Restricted split classes.* Examples: redistributing the given terms,
    quadratic or polynomial cost shifts, or splits computable in polynomial
    time.
    - The balanced split of Section 4.1 is such a shift. Its interior
      Hessian blocks `[[1, 0.8], [0.8, 1]]` are the terms of a chordal PSD
      decomposition of `2I + 0.8A`.
    - Degree-2 shifts already remove the proved eps-dependent clustering
      on this family, as Section 4.1 reports.
    - Whether an eps-independent exponential lower bound holds uniformly
      over such a restricted class is open. Section 4.1 says so.
  - *Cost of describing the split.* If the split may vary, a fair
    certificate must pay for describing it. The conditional-margin split has
    size 1 but encodes the value functions.
    - A meaningful uniform statement would charge, for example, the number
      of pieces of piecewise-affine `psi_t`.
    - Decomposition certificates are exactly such objects (Lemma 1.5), so
      this would put both methods in one model. This is a suggestion, not a
      required fix.

The note's own conclusion (lines 1176–1181) is correct: single-tree lower
bounds must fix the factorization and the per-factor relaxation, or restrict
the admissible splits. It would help to add the first bullet (both sides
collapse) and the second (fixed algebraic rules and restricted split classes
remain open).

## 3. Remarks 3.5 and 3.6 and the program count

### 3.1 The `theta` claims (Remark 3.5, last item; Remark 3.6)

Before this revision the note said "`theta = 1/2` works in the computed
examples". It now says "`theta = 1/16` works for every tested `n` and
`theta = 1/8` fails for `n > 16`" (lines 886–890). I checked this with my
own code, `shell_dp.py`:
- shell partitions built in exact integer units;
- a bottom-up dynamic program over the certificate with zero slopes;
- each convex program solved by golden-section search in `z_1`, over the
  closed-form (interior bags) or bisection (last bag) minimum in `z_2`.

**Validation.** It reproduces the numbers of the note and of the first
review to all printed digits:

| case | note or first review | my code |
|---|---|---|
| `n = 16`, `theta = 1/16`, `h = 2^-8` | gap `5.6763e-5`, size 372,312 | gap `5.6763e-5`, size 372,312 |
| `n = 20`, `theta = 1/8`, `h = 2^-8` | gap `2.4984e-2` | gap `2.4984e-2` |

**Onset** (`logs/theta_threshold.log`). Root gap `f* - l_r`:

| `theta` | `h` | `n = 15` | `n = 16` | `n = 17` | `n = 18` | `n = 19` |
|---|---|---|---|---|---|---|
| 1/8 | `2^-6` | 8.45e-4 | 9.08e-4 | **6.23e-3** | 1.248e-2 | 1.873e-2 |
| 1/8 | `2^-8` | 5.28e-5 | 5.68e-5 | **6.23e-3** | 1.248e-2 | 1.873e-2 |
| 1/8 | `2^-10` | 3.30e-6 | 3.55e-6 | **6.23e-3** | 1.248e-2 | 1.873e-2 |
| 1/16 | `2^-8` | – | 5.68e-5 | 6.07e-5 | 6.47e-5 | – |

- At `n <= 16` the gap is the normal `O(|T| h^2)` term. It falls by 16 for
  every factor 4 in `h`, and at `n = 16`, `h = 2^-8` it equals the
  `theta = 1/16` value.
- From `n = 17` on the gap is `6.2337e-3` for every `h`, identical to
  5 digits.
- At `n = 18` it is `1.2484e-2`, the note's `1.25e-2`. The
  `theta = 1/16` value at `n = 18` is `6.47e-5`, the note's `6.5e-5`.

- The failure starts exactly at `n = 17`, and it starts there at every `h`
  tested. It grows by `0.00625` per added variable. This matches the note's
  "fails for `n > 16`", which before this check was an extrapolation from
  `n = 18`.
- The onset does not depend on `h`, as the mechanism predicts: the pattern
  lives at `|x| ≈ 0.5`, where the shell cells are the same for every dyadic
  `h <= 2^-2`.
- **Why `-0.00625` exactly.** At `theta = 1/8` the drift is
  `d = 2 theta |x| = 0.125`. A bag then evaluates
  `x^2 (1 - b) - 2 b theta x^2 - kappa x^4`. With `b = 0.8` and
  `theta = 1/8` the quadratic part cancels, and the bag value is exactly
  `-kappa x^4 = -0.00625` at `x = 0.5`.
  - This also explains why `(1-b)/(2b) = 0.125` is exactly the borderline
    at `b = 0.8`: the quartic term tips it.
  - The first review's `b`-sweep table fits this: the largest admissible
    `theta` is the largest power of `1/2` strictly below `(1-b)/(2b)`, for
    `b = 0.5, 0.6, 0.7, 0.8, 0.85`.

Remark 3.6 cites this sweep correctly.

### 3.2 Center accuracy (Remark 3.5)

The corrected text is right.
- **Slope error.** Let `delta = x̂ - x*`, and let `g_{s,i}` be the change of
  `∂_i a_s` between `x*` and `x̂`.
  - The change of `lambda_{t,i}` is `sum_{s in sub(t) ∩ T_i} g_{s,i}`, a sum
    of at most `k - 1` terms.
  - By Cauchy–Schwarz, and because each pair `(s, i)` is counted for at
    most `k - 1` separators `t`,
    `nu^2 <= (k-1)^2 sum_s |g_s|^2 <= (k-1)^2 M_a^2 sum_s |delta_{V_s}|^2 <= (k-1)^2 k M_a^2 |delta|_2^2`.
  - So `nu <= k^{3/2} M_a |delta|_2`, as stated. The componentwise sum must
    be used here. Bounding each component by the full gradient norm would
    lose a factor `sqrt(w+1)`.
- **"`O(sqrt(eps))` when `n = O(|T|)`".**
  - With `|delta|_inf <= h_0`, the first (T3) bound holds when
    `k n c_g^2 <= 768 |T| M_a^2 w`.
  - It suffices that `k^3 n <= 3072 |T| w`, because `c_g <= k M_a/2`.
  - For paths this is `8(|T|+1) <= 3072 |T|`. The second (T3) bound holds
    with even more room.
  - So the claim is correct, with constants depending on `k` and `w`.

Two minor points:
- **Wording (line 871–873).** "The center may be off by `h` in sup-norm and
  the slopes by `nu = O(sqrt(eps))` ..., with constants independent of `|T|`
  and `n`" reads as if the center tolerance were also independent of `|T|`.
  Suggested wording: "the center may be off by
  `h <= h_0 = O(sqrt(eps/|T|))` in sup-norm, and the slopes by
  `nu = O(sqrt(eps))` in total Euclidean norm, where the constant in the
  slope tolerance does not depend on `|T|` or `n`".
- **Still open from the first review:**
  - Theorem 3.4 (line 754) should require `x̂ in X0`. Lemma 3.1 assumes
    `p in X`, and the Lipschitz bound behind `nu <= k^{3/2} M_a |delta|` is
    only assumed on `X0`.
  - The summary base `O(M_a sqrt(w)/c_g)` (line 775) still needs
    `alpha' A <~ w M_a^2/c_g`. The added "for `M_a >= c_g`" is not enough
    when `alpha' A` is large. On the path family both hold.

### 3.3 The (leaf, cell) convex-program count

The statements are:
- line 269–273 (Section 1.3): one program per pair, pairs 3–5 times the
  leaves, ratio growing like `log(1/h)`;
- lines 1071–1083 (Section 4): the counts, and `Theta(|T| C^{w+1} log^2(|T|/eps))`
  programs.

My geometric count for an interior bag, with closed intersections and the
separator taken as the first coordinate (`logs/pairs_theta16.log`,
`theta = 1/16`):

| `h` | leaves | cells | pairs | pairs/leaves | max cells per leaf |
|---|---|---|---|---|---|
| `2^-4` | 12,292 | 130 | 37,388 | 3.042 | 10 |
| `2^-8` | 24,580 | 258 | 92,940 | 3.781 | 51 |
| `2^-12` | 36,868 | 386 | 164,876 | 4.472 | 115 |
| `2^-14` | 43,012 | 450 | 206,988 | 4.812 | 147 |
| `2^-20` | 61,444 | 642 | 357,900 | 5.825 | 243 |

- The counts match the note's exactly.
- With `j = log2(1/h)`, the counts over `j = 4, 6, ..., 20` fit
  `pairs = 512 j^2 + 7744 j - 1780` exactly (the second differences are
  constant), while `leaves = 3072 j + 4`. So pairs/leaves is `j/6 + O(1)`.
  This confirms the "0.17 per halving" and the `log^2` growth.
- The mechanism is clear. The about `4/theta` leaves per level whose
  separator projection touches the center each meet about
  `(1/theta)(j - log2(1/theta) - 1)` finer cells:
  `2 (1/theta)^2 = 512` in the quadratic coefficient.
- The general statement `Theta(|T| C^{w+1} log^2)` follows from the same
  geometry with the base `C` enlarged. As written it is a counting remark,
  not a proved theorem. That is acceptable, but "shell certificates need"
  would read better as "for shell certificates, the number of programs is".
- The per-leaf variant is valid, since it only lowers `beta`. Its drift
  bound `w(B_t) + w(D_t) + w(B_p)` is right. The note correctly says that
  the constants are not written out.
- With `theta = 1/8` the pattern is the same (3.07, 3.81, 4.50, 5.17 at
  `h = 2^-4`, `2^-8`, `2^-12`, `2^-16`; `logs/pairs_theta8.log`).

## 4. Literature: Berenguel, Casado, García, Hendrix, Messine (JOGO 2013)

**Source.** J. Glob. Optim. 56(3):1101–1121 (2013),
DOI 10.1007/s10898-012-9928-x. It is open access under CC BY. I read the
full published PDF, fetched from
`https://rd.springer.com/content/pdf/10.1007/s10898-012-9928-x.pdf`.
`link.springer.com` returned a JavaScript challenge. A local copy and its
text extraction are in `decomposition-recheck-checks/berenguel2013.{pdf,txt}`
(sha256 `cce246d3…8774`).

### 4.1 What the paper does

- **Problem class.** Box-constrained `min f(x) = sum_{j=1}^p f^[j](z^[j], x_n)`.
  - The subfunctions have disjoint private variables `z^[j]` and one
    **common variable `x_n` shared by all subfunctions** (Section 1, eq. (4)).
  - The authors say the theory is valid for a group of common variables but
    present it for one. All experiments use `p = 2`.
  - In the note's terms this is a star: every pair of bags meets in the same
    separator. There are no chains, no deeper trees, and no separators that
    differ between edges.
- **Algorithm (IBB–DSP, "decomposed sub-function perspective").**
  - One interval B&B list `L^[j]`, `Q^[j]` per subfunction, in its own
    `n^[j]`-dimensional space, with a copy of `x_n` per subfunction.
  - Example 2 notes that relaxing `x_3^[1] = x_3^[2]` gives a lower bound:
    the copy relaxation.
  - Bounds come from interval inclusion functions (natural extension
    intersected with the Baumann form). There are no convex relaxations.
  - Selection rule 6 re-evaluates stored bounds, three phases combine the
    lists into full-dimensional boxes at the end, and division is bisection
    of the widest side.
- **Results, all short validity statements.**

  | result | content |
  |---|---|
  | Theorem 1 | subfunction range test against `g^[j](x_n)`, the best upper value found for a given midpoint value of the common variable |
  | Proposition 1 | if all lists use the same uniform bisection of `x_n`, the box `Psi^[k](Y)` gives a lower bound of `f^[k]` over `(T^[k], Y)`; `Psi^[k](Y)` is the box of list `k` with the smallest bound among those whose `x_n`-interval meets `Y` |
  | Proposition 2 | `F^[j](X) + sum_{k != j} lb^[k]` is a lower bound of `f` on the extension of `X` |
  | Theorem 2 | the sharper bound `F_DSP = F^[j](X) + sum_{k != j} F^[k](Psi^[k](X_n))` |
  | Theorem 3 | monotonicity test in the common variable, combining derivative enclosures across lists |
  | Property 7 (UVCV) | drop a box if some other list has no box whose common interval meets it |
- **Complexity.** There is no theorem or bound on nodes, boxes or
  evaluations, and no lower bound. The only complexity statements are
  informal:
  - the abstract: the effort "increases exponentially with the problem
    dimension in the worst case. For separable functions this effort is
    less";
  - Section 4: "the number of boxes generated by Algorithm 1 in the worst
    case has an exponential behaviour in the dimension".
- **Experiments.**
  - 13 test functions of dimension 3–9, made by joining two standard test
    functions through one shared variable.
  - The termination criterion is box width `eps in {1e-3, 1e-6}`, to find
    all minimizers. It is not an optimality-gap tolerance.
  - Effort is a weighted count of inclusion-function evaluations.
  - At `1e-3`, IBB–DSP needs less effort on all 13 problems.
  - At `1e-6`, it needs less effort on only 6 of 13 and less CPU time on 4.
    For example, problem 9 needs 5.67e6 effort against 1.62e6, and 7329 s
    against 17 s. The authors attribute this to list growth that weakens
    `F_DSP` and makes the `Psi` search expensive.
  - Two decompositions of the Colville function differ in effort by a
    factor of about 10. The authors conclude that the choice of
    decomposition matters.

### 4.2 Does it anticipate the note?

- **The model and algorithm, in a special case: yes.** `F_DSP` is the note's
  child bound `psi_{u,B} = min{beta_{u,D'} : D' ∩ B_{S_u} ≠ ∅}` with zero
  slopes (Section 1.3), in these circumstances:
  - one level only (a star with one separator);
  - interval bounds in place of convex relaxations;
  - "cells" given implicitly by the `x_n`-projections of the other lists'
    boxes;
  - Example 2 is the copy relaxation.

  So the certificate model and the fixed-slope algorithm of Section 1.5,
  restricted to zero slopes and one separator, have a direct continuous
  precedent. The note should cite it as such, in Section 1.5 and in
  Section 6, item 11.
- **Not anticipated:**
  - the instance-dependent size bound (Theorem 3.4) or any other size
    bound;
  - affine slopes or Lagrange multipliers, or drift along chains;
  - lower bounds (Section 2, Corollary 2.1);
  - the separation (Theorem 4.1);
  - the worst-case bound (Theorem 3.3), which the note already attributes
    elsewhere.

  The paper's claims of exponential worst-case growth are informal and
  concern interval B&B in general.
- **A possible link, not checked.** The loss of the decomposed method at
  the tighter tolerance fits, in kind, what Proposition 2.6 predicts for
  zero-slope child bounds. But their termination is width-based, and I did
  not check the separator multipliers of their test functions. The note
  should not claim this link without such a check.
- **Citing works.** OpenAlex lists 7 citing works, which I checked by title
  and metadata only:
  - Deussen–Naumann, "Subdomain separability in global optimization"
    (JOGO, 2022);
  - Lundell et al., separability reformulations for convex MINLP (JOGO,
    2018);
  - Locatelli–Schoen, historical notes (EURO J. Comput. Optim., 2021);
  - four others.

  None suggests a complexity result on this structure. The companion paper
  (Berenguel et al., ICCSA 2012, LNCS 7335, "On lower bounds using
  additively separable terms in interval B&B") was not read.

**Fixes to the note.**
- Line 1434–1436: replace "checked only at abstract level" with a
  one-sentence description, for example: "read in full: interval B&B with
  one list per subfunction sharing one common variable, a copy relaxation
  and zero-slope combined bounds (their Theorem 2); no complexity results".
- Line 1535–1536: remove "Not done: reading Berenguel et al.".
- Add the citation in Section 1.5, as the one-separator, zero-slope,
  interval-bound precedent.
- The literature audit (`literature/decomposition-bb-prior.md`, lines
  529–537, 767–772, 803–804) should be updated the same way. It is outside
  the note under review.

## 5. Per-claim verdicts

| Claim | Location | Verdict | Fix |
|---|---|---|---|
| Theorem 4.1, case split and constants | l. 1034–1045 | correct | `3.2e-10` should be `3.1e-10`; case 2 is nonempty only for `n >= 21` |
| Uniform ratio `>= 3e-10 * 1.3155^n/sqrt(n)` | l. 70, 145, 989–991, 1486 | false for `n >~ 2.7e5` (base rounded up); proof valid for `n <= 7035` | use `(2e/pi)^{n/2}` or `1.3154^n` |
| Second term of (a), from face-exact Theorem 1 | l. 966, 1001–1009 | correct: (M_b), (Q_2), `rho`, `S`, `lambda`, `eps''` check; used within its scope | — |
| McCormick variant | l. 993–998, 1052–1058 | correct | may state `c = 1e-8` |
| Grid check `1.26e-9` | l. 1047–1048 | correct; also the exact infimum over all `eps <= 1e-4`, `n <= 300` | the script normalizes by `(2e/pi)^{n/2}`, not `1.3155^n` |
| Observation 4.2, split form | l. 1147–1160 | correct | decomposition side has size `2|T| - 1`, not one node; "=" should be ">=" in the proof |
| Observation 4.2, measure form and duality | l. 1162–1174 | correct (measurability, attainment and running intersection check) | "dually"; cite Vorob'ev (1962) and Lasserre (2006); every split is a cost shift |
| Scope of Observation 4.2 | l. 1176–1181 | correct | add: both sides collapse; fixed algebraic rules and restricted split classes remain open |
| Remark 3.5, `theta` constants | l. 886–890 | correct; onset `n = 17` confirmed at three `h` | — |
| Remark 3.5, center and multipliers | l. 871–882 | correct (`nu <= k^{3/2} M_a |delta|_2` rederived) | wording on which tolerance is `|T|`-free; `x̂ in X0` still missing (l. 754) |
| Remark 3.6 | l. 892–909 | correct; per-bag value `-kappa x^4` explains `-0.00625` exactly | — |
| (leaf, cell) program count | l. 269–273, 1071–1083 | correct; counts reproduced exactly; exactly quadratic in `log2(1/h)` | "for shell certificates, the number of programs is" |
| Berenguel et al. (2013) | l. 1433–1436, 1535 | now read in full: a precedent for the zero-slope, one-separator algorithm; no complexity results | cite in Section 1.5; update Section 6, item 11 |

## 6. What I verified myself, sources, and commands

**By hand:**
- every step of the Theorem 4.1 ratio proof, with the constants of
  Corollary 2.1 and of (b) (`Q = 159.0`, `theta <= 1.28e-3`,
  `h_0^2 = eps/(4.885e5 (n-1))`, `2 * 4096^2 = 3.355e7`);
- that the note's relaxation and McCormick satisfy (M_b) and (U^q_{0.4});
- Observation 4.2: continuity, attainment, disintegration, running
  intersection, the duality, and that every split is a cost shift;
- the bound `nu <= k^{3/2} M_a |delta|_2` and the conditions (T3) for
  `n = O(|T|)`;
- the alternating-configuration algebra of Remark 3.6.

**Sources examined:**
- the note (all sections, with focus on Sections 1.3, 2.1, 3.3, 4 and 8);
- the first review (`reviews/decomposition-review.md`);
- the face-exact note, Sections 1–3 (Lemma 1.1, (M_b), (Q_D), Lemma 1.2,
  Theorem 1, Corollary 1.3);
- the note's `revision_checks.py` and `logs/revision_checks.log`;
- the full text of Berenguel et al. (2013);
- OpenAlex and Semantic Scholar metadata (open-access status, citing
  works);
- web search results for Vorob'ev (1962) and Lasserre (2006), at the
  bibliographic level.

**Commands.** All were run in
`research-20260929/reviews/decomposition-recheck-checks/`, with Python
3.13.11, NumPy 2.5.1 and mpmath 1.3.0. These are targeted local checks, not
CI.

| Command | Log | Result |
|---|---|---|
| `python3 ratio_check.py` | `logs/ratio_check.log` | constants; grid minimum `1.2619e-9` (`n = 4`, `eps = 9.5e-7`); exact infimum over all `eps`, `n <= 300`: `1.2618e-9`; base-rounding failure from `n ≈ 2.7e5`; McCormick `c` minimum `1.03e-8` |
| `python3 shell_dp.py pairs 4 4 6 8 10 12 14 16 18 20` | `logs/pairs_theta16.log` | pair counts equal the note's; exactly quadratic in `j` |
| `python3 shell_dp.py pairs 3 4 8 12 16` | `logs/pairs_theta8.log` | the same pattern at `theta = 1/8` |
| `python3 shell_dp.py gap 16 4 8`, `gap 20 3 8` | `logs/gap_validation.log` | `5.6763e-5` (size 372,312) and `2.4984e-2`, equal to the note and the first review |
| `python3 shell_dp.py gap N 3 J` for `N = 15..19`, `J = 6, 8, 10`; `gap 17 4 8`, `gap 18 4 8` | `logs/theta_threshold.log` | onset of the `theta = 1/8` failure at `n = 17` for every `h`; `theta = 1/16` fine |
| `curl` of the Springer PDF (rd.springer.com) and `pdftotext -layout` | `berenguel2013.pdf`, `berenguel2013.txt` | full text read |
