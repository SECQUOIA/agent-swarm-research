# Referee report: "Decomposition certificates for spatial branch-and-bound: complexity and an exponential separation"

Date: 2026-09-29. Note under review:
`research-20260929/theory-decomposition/decomposition-certificates.md`
(cited as "the note", with line numbers of the version dated 2026-09-29 23:11).
The referee did not write the note. Referee scripts and logs are in
`research-20260929/reviews/decomposition-review-checks/`. Only targeted checks
were run; no project-wide verification and no CI (AGENTS.md).

## Verdict in brief

- **The mathematics is correct.** I checked every proof by hand and could not
  break any of them:
  - the model: Lemmas 1.1, 1.3, 1.4, 1.5;
  - the lower bounds: Corollary 2.1, Lemma 2.2, Propositions 2.3, 2.4, 2.6,
    Theorem 2.5;
  - the upper bounds: Lemmas 3.1, 3.2, Theorems 3.3, 3.4;
  - Theorem 4.1 (a), (b), (c).

  Every constant I recomputed agrees with the note: 0.0741/0.068, 1.3155,
  0.28893, 0.53334, `Q = 159.0`, `theta <= 1.28e-3`, `4.885e5`, `3.36e7`,
  0.2778, and the `L_n(eps)` table.
- **Small fixes are needed** (Section 7 lists them):
  - The separation is not "uniform in `eps <= 0.2/n`" with the closed form,
    which is 0 at `eps = 0.2/n`.
  - Remark 3.5 says `theta = 1/2` works in the computations. Section 5.4 shows
    it does not for `n > 16`.
  - Remark 3.5 states only a Euclidean `O(sqrt(eps))` accuracy for the local
    solve. The center also needs sup-norm accuracy
    `h_0 = O(sqrt(eps/|T|))`.
  - "Counting relaxation solves only strengthens the separation" is false as
    a count. Each leaf needs one convex program per cell it meets, which is
    3–5 times the leaf count at the tested `h`, and the ratio grows like
    `log(1/h)`.
  - Proposition 2.3's `exp(Omega(w))` holds only above the threshold
    `alpha/lambda_geo > pi/(4e)`.
- **A stronger single-tree bound is already in the program, and the note
  should use it.**
  - The note's relaxation is alphaBB on each bilinear term alone. Its gap is
    at least the termwise McCormick gap, so it satisfies hypothesis (M_b) of
    the face-exact note.
  - Face-exact Theorem 1, which the face-exact review found correct,
    therefore applies. It gives at least `0.57 (5/3)^n` single-tree leaves
    (plus `2n` per tightening round) for every `eps <= 1e-4`.
  - This bound holds for McCormick as well. With Theorem 4.1(b), which also
    holds for McCormick, it gives the separation for termwise McCormick.
    That is the solver-relevant case the note says it does not cover
    (lines 433, 955).
  - Against the computed certificates, the crossover moves from `n ≈ 45–50`
    to `n ≈ 29`. Against the proven bound (b), it moves from about 86 to
    about 49.
- **Robustness to the factorization.** The proved mechanism belongs to one
  factorization and one relaxation: alphaBB on each bilinear term alone.
  - If each `g_i` is split between its two neighbouring factors before
    alphaBB is applied, Corollary 2.1 gives nothing. With the root-box alpha
    the base is 0.930. With a box-dependent alpha the relaxation is exact on
    `|x|_inf <= 0.577`.
  - In a toy B&B with this split, the clustering at `x*` disappears. The
    counts no longer depend on `eps`.
  - The counts still grow about 2.3–2.5 times per variable, from the outer
    region, and no lower bound is proved for that growth.
  - So the note's eps-uniform separation depends on the relaxation and
    factorization. An eps-independent exponential appears to remain under the
    balanced split, but it is unproven.
- **Significance.**
  - The instance-dependent upper bound (Theorem 3.4) is the most substantial
    new result. It is a certificate-size bound, with no regularity assumed
    for value functions and with explicit control of drift along chains.
  - The separation is a clean, rigorous version of a known phenomenon: the
    cluster effect of termwise relaxations, removed by paying relaxation
    error per bag.
  - It is modest in scope. The relaxation is one no solver uses in this form,
    the decomposition side is an existence result centered at `x*`, and SCIP's
    default PSD-minor cuts escape the single-tree bounds.

## 1. The certificate model (Section 1)

### 1.1 Lemmas 1.1, 1.3, 1.4, 1.5: correct

- **DP recursion (lines 141–149).** The recursion needs the variables of
  `W_u \ S_u` to be disjoint across children and from `V_t`. Running
  intersection gives this: if `i` lies in `W_u` and `W_{u'}`, then `T_i`
  contains `t`, and the path to `t` passes through `u`, so `i` is in `S_u`.
  `phi_u` is continuous, because the constraint set is a fixed box, so the
  minima are attained.
- **Lemma 1.1.** The telescoping is correct.
- **Lemma 1.3.** The induction is correct.
  - `z = (s, y)` lies in some leaf `B`, and `s` lies in `D ∩ B_{S_t}`, so (LC)
    applies.
  - For each child `u`, `z_{S_u}` lies in `B_{S_u}` and in some cell `D'`, so
    (CM) and the induction hypothesis give `psi <= phi_u`.
  - Then `l_{t,D}(s) <= G_t(z) = phi_t(s)`.
  - The root case gives `l_r <= f*`. The certificate is therefore valid for
    every point of `X0`, and it certifies `f* >= l_r`.
- **Lemma 1.4.** Correct. Top-down, each child term of `Rel_{p,B_p}(x)` is
  bounded by (CM) at `x_{S_t}`. (LC) then applies to `(B_t, D_t, x)`,
  because both boxes contain `x_{S_t}`. The gap form follows from (G).
- **Lemma 1.5.** Correct.
  - Substituting the largest `beta` gives nested minima.
  - The child's inner minimum depends on the parent only through the
    constraint `D_t ∩ (B_p)_{S_t} ≠ ∅`, so the nested minimum equals the
    joint minimum.
  - The sign convention `+ lambda_t^T (z^p - z^t)` matches (3.1).
  - Numerically: my independent DP traces its minimizing configuration,
    checks every containment and intersection, and recomputes the value from
    scratch. It equals `l_r` to `1e-17` (`logs/trace_n20_theta8.log`).

### 1.2 Overlaps and boundary contacts: handled correctly

- The model uses closed boxes. (LC) is required for every pair `(B, D)` with
  `D ∩ B_{S_t} ≠ ∅`, including pairs that only touch.
- Validity uses only the covering property, not the disjoint interiors. A
  point on a shared face gets the bound from every cell that contains it.
- Both codes (the note's and mine) use closed intersections. This matches
  Lemma 1.5.
- The case `D ∩ B_{S_t} = {point}` is a lower-dimensional convex program,
  which is harmless.

### 1.3 Is the size measure fair to the single tree?

- **Cells are counted**, and in all constructions `|P_t| <= |L_t|`.
- **No hidden exponential work in a leaf.**
  - Each (LC) check is a `(w+1)`-dimensional convex program: the bag's
    factor relaxations plus affine child bounds.
  - `psi` is a minimum over child cells meeting `B_{S_u}`, which is cheap.
  - A single-tree leaf solves an `n`-dimensional program.
- **But the number of convex programs is the number of (leaf, cell) pairs,
  not the number of leaves.**
  - `beta_{t,D}` needs one program per pair with `B_{S_t} ∩ D ≠ ∅`
    (Lemma 1.5 and Section 1.5, step 3).
  - A shell leaf whose projection lies near the center meets cells of every
    finer level. Counted for one interior bag (`logs/pairs_theta16.log`,
    `logs/pairs_theta2.log`):

    | `theta` | `h` | leaves | cells | pairs | pairs/leaves | max cells per leaf |
    |---|---|---|---|---|---|---|
    | 1/16 | `2^-4` | 12,292 | 130 | 37,388 | 3.04 | 10 |
    | 1/16 | `2^-8` | 24,580 | 258 | 92,940 | 3.78 | 51 |
    | 1/16 | `2^-12` | 36,868 | 386 | 164,876 | 4.47 | 115 |
    | 1/16 | `2^-14` | 43,012 | 450 | 206,988 | 4.81 | 147 |
    | 1/2 | `2^-16` | 772 | 66 | 4,084 | 5.29 | 31 |

  - The ratio grows by about 0.17 per halving of `h`. The number of programs
    is therefore `Theta(|T| C^{w+1} log^2(|T|/eps))` for shell certificates,
    one log factor more than the size bound.
  - The size theorems are correct as stated, because size is defined as
    leaves plus cells. The sentence on lines 971–972, "Counting relaxation
    solves instead of leaves only strengthens the separation", is not
    correct as a count. It is correct only per solve, by dimension.
  - *Fix.* State the program count. Alternatively, define
    `beta_{t,D} = min over B meeting D of min_B (Rel_{t,B} - lambda^T z_S)`,
    with one program per leaf. Lemma 1.3 still holds (the leaf minimum is
    below every value on `B`). In Theorem 3.4 the drift becomes at most
    `w(B_t) + w(D_t) + w(B_p)`. As far as I can see, only constants change;
    I have not written out this proof.
  - The effect on the crossover is small: `n ≈ 29 → 32` (face-exact bound)
    and `46 → 51` (Corollary 2.1), at `eps = 1e-6` (`logs/constants.log`).
- **Special case.** With a single bag the model is exactly the single-tree
  certificate of [C], so the comparison is apples to apples. MUSE-BB-type
  single trees, which represent many children implicitly, are not covered.
  The note says so (Section 6, item 8).

### 1.4 Section 1.6 (integer separators): acceptable as a remark

When relaxations live on continuous hulls, the configurations of Lemma 1.5
range over the hulls, not over lattice points. The lemma's statement should
say so. The count claims are plausible and labelled as a remark.

## 2. Theorem 3.4 and the rest of Section 3

### 2.1 Lemma 3.1 and Lemma 3.2: correct

- **Lemma 3.1.**
  - `2^{j-1}h/g_j = 1/theta` is an integer, so the boundary of the inner
    cube lies on grid lines.
  - Kept cells have `dist_inf >= 2^{j-1} h`.
  - Each level has `(4/theta)^kk - (2/theta)^kk` cells, and
    `2^J h >= s0` covers `X`.
  - My geometric re-implementation (containment test on coordinates, not on
    grid indices) gives the same leaf counts as the note's code (372,312 at
    `n = 16`, `h = 2^-8`, `theta = 1/16`).
- **Lemma 3.2.**
  - `u ∈ T_i \ {top(i)}` if and only if `i ∈ S_u`.
  - `u` lies on the path from `t` to `top(i)` if and only if `t ∈ sub(u)`.
  - The exchange of sums then gives exactly
    `lambda_{u,i} = sum_{s in sub(u) ∩ T_i} ∂_i a_s`.

### 2.2 Theorem 3.4: correct

I rederived every step.

1. **Widths.** `w(B) <= h + theta dist_inf(B, x̂) <= 2h + theta |z - x*|_inf`
   for any `z ∈ B`. This applies to `B_t` and `D_t` with
   `|z - x*| <= rho_t + Delta_t`.
2. **Drift.**
   - `d_t <= w(D_t) + w(B_p)`.
   - `Delta_t` contains `d_t` itself, so the step divides by `1 - theta >= 1/2`.
   - This gives `a_t = 2(4h + theta(rho_t + rho_p))` and the coefficient
     `4 theta`, as stated.
3. **Solving the recursion.**
   - `Gamma` is nonnegative and strictly upward, hence nilpotent.
   - The Schur test gives `||Gamma||_2 <= 4 theta sqrt((k-1) D_k)`.
   - `|d|_2 <= 2|a|_2`.
   - `|a|^2 <= 12(16|T|h^2 + theta^2 (1+Delta) sum rho^2)`, because each
     node is a parent at most `Delta` times.
   - `sum Delta_t^2 <= K_1 sum d^2`, by Cauchy–Schwarz over `k - 1` terms,
     each counted over at most `sum_{j<=k-2} Delta^j` descendants.
4. **Errors.**
   - Each Taylor bracket is at least `-(M_a sqrt(w) r_t Delta_t + (M_a w/2) Delta_t^2)`,
     since at most `w` coordinates differ.
   - The slope error is at most `sqrt(w) nu |d|_2`.
5. **Absorbing.** Young's inequality with weight `c_g/(4k)` gives
   `k M_a^2 w/c_g`. The constants 768 (= 48 x 16), 3072 and 384 are right.
   The `X^2` coefficient is `c_g/4 + c_g/8 + c_g/2 = 7c_g/8 < c_g`.
6. **Count.** `J + 1 <= log2(s0/h) + 2`, and
   `N <= 2|T|(J+1)(4/theta)^{w+1}`.

Minor points:
- The center must lie in `X0`. The statement says only `|x̂ - x*|_inf <= h`.
- The summary form `O(M_a sqrt(w)/c_g)` for the base (line 725) also needs
  `alpha' A <~ w M_a^2/c_g`.
- The proof never uses `∇F(x*) = 0`, so boundary minimizers are covered, as
  the note says.

### 2.3 Theorem 3.3: correct, and not new

The note says it is not new (lines 674–683), and I agree:
- zero slopes;
- `|z^t - x| <= 2(k-1)h`;
- `h = min(eps/(4(k-1)G|T|), sqrt(2 eps/(alpha' A|T|)))`.

### 2.4 Remark 3.5: two fixes

- **Center accuracy (lines 823–827).**
  - The claim `nu <= k^{3/2} M_a delta` is right: each `lambda_{t,i}` sums
    at most `k` gradients, and each `(s, i)` appears in at most `k - 1`
    separators.
  - But the center must also satisfy `|x̂ - x*|_inf <= h_0 = O(sqrt(eps/|T|))`.
    Otherwise the central cells have width `|x̂ - x*|_inf`, and the
    `|T| h^2` term exceeds `eps`.
  - A Euclidean error of `O(sqrt(eps))` does not give this sup-norm bound.
    It can sit in one coordinate.
  - *Fix.* "A local solve with `|x̂ - x*|_inf <= h_0` suffices; for paths this
    also gives `nu = O(sqrt(eps))`."
- **Inconsistency (line 833).** "`theta = 1/2` works in the computed
  examples" is contradicted by Remark 3.6 and Section 5.4:
  - `theta = 1/8` fails for `n > 16`;
  - `theta = 1/2` works only at `n = 3` (E4).

  Replace it with "`theta = 1/16` works for all tested `n`", as Section 6,
  item 2 says.

### 2.5 Remark 3.6: confirmed, and the threshold scales with the conditioning

- **Confirmed independently.** My DP at `n = 20`, `theta = 1/8`, `h = 2^-8`
  gives `l_r = -2.49837e-2` (note: `-2.4984e-2`).
  - The minimizing configuration alternates in bags 3–15.
  - Each of those bags has leaves at `±[0.4375, 0.5] x ∓[0.5625, 0.625]`
    (or the equal-valued neighbour), drift 0.125, and bag value `-0.00625`.
  - The configuration passes every containment and intersection check.
- **The threshold tracks the conditioning.** "The dependence of `theta` on
  `M_a/c_g` is real" rested on one instance. I swept `b` at `h = 2^-6`,
  `n = 24` and `n = 40` (`logs/sweep_*.log`). The gap either grows linearly
  in `n` ("fails") or grows like `|T| h^2` ("ok": ratio 1.72 ≈ 39/23).

  | `b` | `c_g` | `(1-b)/(2b)` | `theta = 1/2` | `1/4` | `1/8` | `1/16` |
  |---|---|---|---|---|---|---|
  | 0.50 | 0.40 | 0.50 | fails (0.070 → 0.164) | ok | ok | ok |
  | 0.60 | 0.30 | 0.33 | fails (1.09 → 1.99) | ok | ok | ok |
  | 0.70 | 0.20 | 0.21 | fails | fails (0.30 → 0.60) | ok | ok |
  | 0.80 | 0.10 | 0.125 | fails | fails | fails (0.050 → 0.150) | ok |
  | 0.85 | 0.05 | 0.088 | fails | fails | fails (0.56 → 1.15) | ok |

  - The largest admissible `theta` follows the mechanism's threshold
    `(1-b)/(2b)`. That threshold is linear in the curvature margin along the
    alternating direction, as (T2)'s `theta ~ c_g/M_a` predicts in order.
  - At `b = 0.8` the quartic term lowers the threshold just below 0.125, so
    `theta = 1/8` fails.
  - The note may cite this table as support.

### 2.6 Is global (QG) reasonable or necessary, and what happens otherwise?

- **Qualitatively, (QG) is free.** On a compact box it is equivalent to a
  unique global minimizer with local quadratic growth, by compactness (line
  182). It excludes nothing that has a unique nondegenerate minimizer.
- **Quantitatively, `c_g` is global and can be tiny.**
  - `c_g <= min over x ≠ x*` of `m(x)/|x - x*|^2`.
  - A second local minimizer with value `f* + delta` at distance `D` forces
    `c_g <= delta/D^2`. The base becomes at least `(C M_a D^2/delta)^{w+1}`.
  - When `delta ~ eps`, the bound is no better in form than the worst-case
    Theorem 3.3.
  - When `delta = 0` (several global minimizers), the theorem gives nothing.
    If the multipliers differ at the minimizers, one slope per separator
    cannot be right at both.
  - The same `theta` is used everywhere, so regions far from every minimizer
    are refined at the rate set by the worst direction.
- **Some growth is necessary** for `log(1/eps)`. Proposition 2.4 (flat
  minima) forces `eps^{-(w+1)/2}`.
- **What a stronger version would need.** Local (QG) near `x*` plus a margin
  `m >= mu` away from it. The shell ratio `theta` would then grow with the
  distance. With several near-optimal local minima, one would use
  multi-center shells with slopes per region. That requires cell-dependent
  slopes, and the telescoping identity then leaves mismatch terms (the note's
  obstacle (i), line 884).
- *Suggested addition to Section 6, item 4.* State the `delta/D^2`
  degradation explicitly.

## 3. Corollary 2.1, Theorem 4.1, and robustness to the factorization

### 3.1 Corollary 2.1: correct

- **Anisotropic Theorem 3.1.**
  - AM–GM gives `(m+eps)^{-n/2} <= n^{-n/2} prod (alpha_j a_j)^{-1/2}`.
  - Each arcsine integral equals `pi`, which gives the constant
    `(n/pi^2)^{n/2} (prod alpha)^{1/2}`.
  - [C]'s remark after Theorem 3.1 states this form.
  - It extends to runs with same-relaxation tightening by [C, Lemma 2.1],
    using `a_j^C <= a_j^A` coordinatewise.
- **Weights.** alphaBB of `b x_i x_{i+1}` has gap `(|b|/2)(a_i + a_{i+1})`
  on every box, so `alpha_j = |b|` for interior `j` and `|b|/2` at the ends.
  A larger or box-dependent `alpha` only increases the gap.
  - A nonuniform diagonal shift with `4 alpha_i alpha_{i+1} >= b^2` still
    gives interior weights at least `|b|` by AM–GM, up to end effects. So
    the bound does not depend on the alphaBB variant.
- **Ellipsoid, polar coordinates, `J_n` bound, Stirling.** All correct.
  - `det H = |b|^n sinh((n+1) theta_b)/sinh theta_b` is the Chebyshev
    `U_n(1/|b|)` recurrence.
  - For `b = 0.8`, `det H <= (4/3) 1.6^n`. The ratio to `(4/3)1.6^n` is 1.0
    to six digits at `n = 10, 40`.
- **Constants.**
  - `2 sqrt(3/16) (4pi)^{-1/2} e^{-1/2}/2 = 0.07409`; with `e^{-1/12}` this
    is 0.06816.
  - Threshold `|b| = 0.53334`.
  - `L_n(eps)` reproduced with scipy quadrature in log variables: for
    example `L_40(1e-6) = 3.869e5` and `L_80(1e-6) = 2.919e10`.

### 3.2 Theorem 4.1: correct, with one fix

- **(b)** is correct.
  - `M_a = 2.8`: the largest spectral norm of the bag Hessians over
    `phi'' ∈ [0.8, 2]` is 2.8000.
  - `Q = 159.0`; (T1) needs `theta <= 1/8`; (T2) needs `theta <= 1.280e-3`.
  - `4Z = 4.885e5`, and `2 x 4096^2 = 3.355e7`.
  - `log2(2/h_0) = (1/2) log2(1.954e6 (n-1)/eps)`. The note's 1.96e6 is a
    conservative rounding.
- **(c)** is correct: 0.27784, with `R^2 = 0.6`, and `J_2` is exact.
- **Uniformity (line 924) is false as stated.**
  - At `eps = 0.2/n` the closed form of (a) is `log(1) = 0`, while the
    displayed ratio `c 1.3155^n/(sqrt n (1 + log n/log(1/eps)))` is positive.
  - The exact integral bound is positive there: `L_10 = 4.4` and
    `L_40 = 2.6e4` at `eps = 0.2/n`. So the conclusion survives if (a) is
    stated with `L_n(eps)`.
  - *Fix.* Use `L_n(eps)`, or restrict to `eps <= 0.1/n`, or write the ratio
    with `log(0.2/(n eps))/log(n/eps)`.

### 3.3 A stronger single-tree bound is already proved in the program

- **The note's relaxation satisfies (M_b).** The face-exact note's hypothesis
  (M_b) asks for a gap of at least `b sum d_i d_{i+1}`. The note's relaxation
  has gap `(|b|/2)(a_i + a_{i+1}) >= (|b|/2)(d_i^2 + d_{i+1}^2) >= |b| d_i d_{i+1}`,
  since `a_i >= d_i^2`. A random test over `2e5` boxes and points finds no
  violation: the minimum slack is `+1.2e-7`.
- **Face-exact Theorem 1 therefore applies.**
  - (Q_2) holds on `R = [-1,1]^n` (face-exact Lemma 1.1), and
    `rho = 1.25 <= 1.99`.
  - Every certificate, and every run's leaves plus tightening pieces, has at
    least `(5/3)^n exp(-(5/9)(1 + eps/0.8))` members.
  - This is `>= 0.57 (5/3)^n` for `eps <= 1e-4`. The base is 1.667, against
    1.3155, but there is no `log(1/eps)` factor.
- **Consequences** (`logs/constants.log`):

  | comparison at `eps = 1e-6` | Corollary 2.1 | face-exact Theorem 1 |
  |---|---|---|
  | first `n` where the bound exceeds the computed certificate (`3.72e4 (n-1)`) | 46 (note: 45–50) | 29 |
  | same, counting convex programs (x4.47) | 51 | 32 |
  | first `n` where the bound exceeds Theorem 4.1(b) (proven vs proven) | 86 (closed form) | 49 |

  - The note's `log(1/eps)` form is still needed for uniformity as
    `eps -> 0` at fixed `n`. So Theorem 4.1(a) should state the maximum of
    the two bounds.
  - Because Theorem 1 covers termwise McCormick, and (b) holds for McCormick
    (line 957), **the separation holds for termwise McCormick**, with an
    eps-free single-tree bound. Lines 433–436, 955–958 and Section 6, item 1
    should be revised.
  - SCIP's default PSD-minor cuts escape both bounds (face-exact review,
    Section 5.2(b)).

### 3.4 Robustness to the factorization

The objective can be split into factors in several equally cheap ways. The
table gives the Corollary 2.1 base `sqrt(4e/pi · alpha_geo/lambda_geo)`, with
`lambda_geo = 1.6` (`logs/constants.log`). Exponential growth needs a base
above 1.

| factorization and alpha rule | `alpha` per factor | interior weight | base |
|---|---|---|---|
| note: `b x_i x_{i+1}` alone (any box) | 0.400 | 0.800 | **1.3155** |
| PROGRAM: `g_i + b x_i x_{i+1}`, root-box alpha | 0.247 | 0.494 | 1.034 |
| PROGRAM, alpha on boxes near `x* = 0` | 0.140 | 0.281 | 0.779 |
| balanced: `g_i/2 + g_{i+1}/2 + b x_i x_{i+1}`, root-box alpha | 0.200 | 0.400 | **0.930** |
| balanced, box-dependent alpha, boxes in `abs(x)_inf <= 0.577` | 0 | 0 | none (exact) |

- **The proven single-tree mechanism depends on the factorization.**
  - With the balanced split and the root-box alpha, the exact bound
    `L_n(1e-6)` is 0.83, 0.16 and 0.012 at `n = 10, 40, 80`. It decreases,
    so there is no exponential.
  - With a box-dependent alpha, every factor is convex on
    `|x|_inf <= 1/sqrt 3`. One box certifies that cube.
- **The unary split alone does not matter.** In the note's relaxation the
  convex unary terms are exact and contribute no gap, so distributing them
  among factors changes nothing. What changes the result is merging them
  into the bilinear factor before relaxing. That is a different relaxation,
  equally cheap.
- **Toy single-tree B&B.** I compared the factorizations with the same
  algorithm (`split_bb.py`):
  - own code;
  - incumbent `f* = 0`;
  - pruning by a Frank–Wolfe lower bound;
  - widest-side bisection; "+cvx" splits at ±0.5 when possible, so the
    convex inner cube becomes one leaf;
  - `c = 0`.

  My `balS` counts at `eps = 1e-4` (404, 1,000 and 2,476 at `n = 6, 7, 8`)
  match the face-exact note's `abbS` logs. Leaves:

  | `n` | note `1e-2` | note `1e-4` | note `1e-6` | balanced `1e-2` | balanced `1e-4` | balanced `1e-6` | balanced +cvx `1e-4` (= `1e-6`) | balanced root-alpha `1e-4` |
  |---|---|---|---|---|---|---|---|---|
  | 4 | 212 | 468 | 736 | 60 | 64 | 64 | 23 | 318 |
  | 5 | 668 | 1,518 | 2,414 | 152 | 162 | 162 | 60 | 836 |
  | 6 | 2,208 | 5,250 | 8,316 | 380 | 404 | 404 | 140 | 2,174 |
  | 7 | 7,384 | 17,972 | 28,438 | 946 | 1,000 | 1,000 | 322 | 5,580 |
  | 8 | 24,666 | 60,094 | 95,460 | 2,338 | 2,476 | 2,476 | 768 | – |
  | 9 | – | 199,240 | – | – | – | – | 1,792 | – |
  | 10 | – | – | – | – | – | – | 4,173 | – |

  - **Note split.** Growth is about 3.4 per variable, and the count grows
    with `log(1/eps)`. At `n = 7`, `eps = 1e-6`, 15,550 of the 28,438 leaves
    lie within 0.05 of `x*`: the clustering that Corollary 2.1 bounds.
  - **Balanced split, box-dependent alpha.**
    - The count is independent of `eps`.
    - With "+cvx" there is one leaf near `x*`.
    - Growth is still about 2.3–2.5 per variable, from the outer region
      `|x|_inf > 0.5`. The relaxation errors of wide coordinates add up over
      `n` factors, while the margin there is `O(1)`.
    - The `seed0` runs (`c ~ U(-0.2, 0.2)`) give the same picture
      (`logs/split_*_seed0_*.log`).
  - **Balanced split, root-box alpha.** It keeps a cluster at `x*` (1,522 of
    5,580 leaves within 0.05 of `x*` at `n = 7`, `eps = 1e-4`) and grows about
    2.6 per variable. Only `eps = 1e-4` was run.
- **Answer to the question.** A single tree with the balanced split avoids
  the mechanism the note proves: the `log(1/eps)` clustering at `x*`, with
  its exponential prefactor. In these runs it does not avoid exponential
  growth in `n`, but that growth does not depend on `eps`, and no lower bound
  is proved for it.
  - The decomposition side also gets cheaper with that split, because bags
    are exact near `x*`.
  - So the eps-uniform separation of Theorem 4.1 is a property of relaxing
    bilinear terms alone. An eps-independent separation under the balanced
    split looks plausible but is open.
  - This matches the face-exact review's finding for per-factor envelopes.
- **Assessment of "same per-factor relaxations on both sides".** The
  comparison is internally consistent and fair:
  - the decomposition uses no stronger information per box;
  - its copy relaxation is weaker per virtual box;
  - it wins by having exponentially many virtual boxes (Lemma 1.4).

  But the statement is about a relaxation class and a factorization, not
  about search structure alone. The title, the Summary (items 4–5) and
  Section 4 should say "with each bilinear term relaxed alone, for example
  alphaBB or McCormick". They should mention the balanced split.

## 4. Section 2 lower bounds

- **Lemma 2.2: correct.**
  - Lemma 1.4 at `x = (x̄_{-K}, y)` gives a leaf `B ∈ L_t` with
    `m + eps >= sum_{i in K} alpha_i a_i^B(y)`.
  - Overcounting by all leaves with `y ∈ B_K` and integrating gives the
    constant.
  - Separator cells are not needed, as the note says.
- **Proposition 2.3: correct.**
  - A bag containing a block of size `w + 1` equals it.
  - The block bags are distinct, and no other factor can be assigned to
    them.
  - *Fix.* The Summary (item 6, line 68) and the status table (line 98) say
    `exp(Omega(w))` unconditionally. It holds only when
    `alpha/lambda_geo(H_g) > pi/(4e)`, as the statement itself says
    (line 476).
- **Proposition 2.4: correct.**
  - The vertex-neighbourhood volume `2^d s^{d/2}` and
    `E[Q_k] >= s_0 d/(d+2)` are right.
  - Jensen's inequality over the convex function `N^{-2/d}` gives
    `v K (alpha d K/(4(d+2) eps))^{d/2}`.
  - The `n^{(w+1)/2}` factor is a genuine model-level counterpart of the
    audit's ETH remark. With accuracy relative to `n` it disappears; the
    note says "absolute accuracy".
  - *Fix (line 521).* "Tight up to constants" means up to factors
    `((d+2) alpha'/alpha)^{d/2}/v`, which is exponential in `d`. Say "tight
    in `K` and `eps`, up to factors `C^d`".
- **Theorem 2.5: correct.** `d_i <= sqrt((eps+eta)/alpha)` puts `x_{K_t}` in
  a cube around a vertex, and `2^{|K_t|} |L_t|` cubes cover the projection.
- **Proposition 2.6: correct as stated** (child of the root, one-dimensional
  separator).
  - Step 1 uses (LC) at the root, (CM), Lemma 1.3 for the other children,
    and `beta <= min_D phi_t`.
  - Step 2 is Taylor's theorem along `e_i`, with `G_r(z) <= F(x)`.
  - In step 3 the window argument is right, since `2 r_1 < rho_0`, and the
    `3 eps` bound follows.
  - Step 4 is the contradiction.
  - The implicit-function remark is right: uniqueness of `x*` makes the
    subtree minimizer at `s*` unique, and the principal Hessian block is
    positive definite.
  - The deeper-node case is correctly labelled as a sketch.

## 5. Numerics (Section 5)

**Reproduced with independent code** (`indep_dp.py`):
- my own geometric shell partition;
- golden-section minimization in `z1` (90 steps), where the note uses
  bisection on the derivative;
- configuration tracing.

| check | note | referee |
|---|---|---|
| gap `n = 16`, `theta = 1/16`, `h = 2^-8` | 5.7e-5, size 372,312 | 5.6763e-5, size 372,312 |
| gap `n = 20`, `theta = 1/8`, `h = 2^-8` | 2.50e-2 | 2.4984e-2 |
| gap `n = 20`, `theta = 1/16`, `h = 2^-8` | 7.3e-5 | 7.2632e-5 |
| root `n = 6`, seed 1, `theta = 1/4`, `h = 2^-5`, affine / zero | -0.2053542354 / -0.3609833848 | -0.2053542355 / -0.3609833848 |
| alternating configuration, `theta = 1/8` | drift 0.125, `-0.00625` per bag | same; checks pass; value = `l_r` to `1e-17` |

**Validity check (E3) is one-sided; a sharper version passes.**
- E3 compares the minorants with grid value functions `phi^grid >= phi_t`.
  A violation smaller than the grid error would go undetected. The reported
  margins, down to `-5e-7`, are comparable to that error.
- I evaluated `phi_t` accurately at every cell's endpoints and midpoint:
  grid DP start, then L-BFGS-B over the subtree variables.
- The worst values of `l_{t,D}(s) - phi_t(s)` are:
  - `-1.4e-7` (885 points; `n = 5`, seed 0, `theta = 1/8`, `h = 2^-6`);
  - `-1.8e-6` (504 points; `n = 6`, seed 1, `theta = 1/4`, `h = 2^-5`).
- These margins are well above floating-point error, so there is no
  violation (`logs/valid_*.log`).

**Other numbers checked.**
- **E1 and E4.** Size per bag per halving is `3072 + 32 = 3104`: the level
  counts `(64^2 - 32^2) + (64 - 32)`. This matches "about 3.1e3". The E4
  floor `2 x 0.0315 x 2^-14 = 3.84e-6` also matches.
- **Crossover.** "45–50" is reproduced for the exact Corollary 2.1 integral:
  46 at `eps = 1e-6`, 47 at `1e-4`, 45 at `1e-8`.
- **Real runs versus computed certificates.** The toy single tree with the
  note's own relaxation grows about 3.3–3.4 per variable
  (`logs/split_note_*.log`).
  - At `eps = 1e-4` it needs 60,094 leaves at `n = 8` and 199,240 at `n = 9`.
  - The computed decomposition certificates are 173,608 at `n = 8` (E1) and
    about 198,400 at `n = 9` (8 bags of about 24,800 each at `h = 2^-8`, the
    `h` that E1 needs at this `eps`).
  - At `eps = 1e-6`, `n = 8`, the tree needs 95,460 leaves against 238,696
    for the certificate. The growth rates put the crossing again near `n = 9`.
  - So an actual bisection tree passes the unoptimized shell certificate
    near `n ≈ 9`, far earlier than the proven bounds cross (29–86). This
    compares one algorithm, and the certificate needs `x*`. The note could add
    it as evidence that both the proven bounds are loose.

## 6. Significance and novelty

**What is new**, relative to the audit's sources (I ran no new search):

1. **The model** (cells on continuous separators, affine cell minorants,
   leaf-by-leaf convex checks). This is the continuous analogue of AND/OR
   B&B with cached separator bounds, with value caching replaced by cell
   partitions. Its bookkeeping is new; its ingredients are not:
   - Lemma 1.5 is the standard copy-constraint Lagrangian (Nowak; the
     Cifuentes–Dey–Xu tree-decomposition copy formulation);
   - Junge–Osinga use cell-graph value bounds.
2. **Theorem 3.4 is the main contribution.**
   - Robertson–Cheng–Scott, MUSE-BB Section 5.3 and Kannan Theorem 6.5.23 give
     convergence orders of child bounds at one level, and need `C^2` value
     functions and optimal multipliers.
   - Theorem 3.4 instead bounds the **certificate size** over a recursive
     tree decomposition. It needs no regularity of value functions, because
     it compares each configuration with its consistent point and pays with
     (QG). It controls drift along chains, and Remark 3.6 shows that the
     drift condition is necessary in kind.
   - The ingredients are known: multipliers equal to downstream gradients,
     shell partitions as in [C], and absorption by the margin. The
     combination and the count appear new.
   - Practical content is limited, because the certificate is centered at
     `x*`. The adaptive algorithm is open (Section 3.4).
3. **Section 2 bounds certificate size for every tree decomposition of a
   given width.**
   - The instances are separable blocks, as in Zhang–Sun Theorem 4, so the
     hardness sits inside one bag.
   - This fills the audit's C3 gap ("no certificate-size lower bound
     `(C/eps)^{Omega(w)}`") only for this separable construction.
4. **Theorem 4.1.**
   - The single-tree half is [C] Theorem 3.1 on a path. The audit notes that
     Theorem 3.1 "already covers separable problems, so C1's content is not
     specific to paths".
   - The decomposition half is Theorem 3.4.
   - The differences from Basu et al. (2023) and Dey–Shah (2022) are real:
     - no ties (a unique nondegenerate minimizer);
     - continuous separators that are never fixed;
     - a lower bound that comes from the relaxation gap;
     - a B&B, not a DP, on the fast side.
   - The difference from Dechter–Mateescu is also real: pruned trees with a
     fixed relaxation.
   - The mechanism itself is the cluster effect (Neumaier;
     Wechsung–Schaber–Barton), removed because the decomposition pays
     relaxation error per bag rather than per `n`-dimensional box. A clean,
     rigorous statement of this appears new, but it is modest.
   - Berenguel et al. (2013) is still unread in full (line 1202). That must
     be done before a priority claim.

**Is the separation meaningful for solvers?** Only qualitatively.
- **Relaxation.**
  - alphaBB on an isolated bilinear term is dominated by McCormick, which
    is the convex envelope, so no solver uses it.
  - The McCormick version follows from face-exact Theorem 1 (Section 3.3).
  - SCIP's default PSD-minor cuts escape both single-tree bounds.
  - Convexity detection on aggregated expressions also escapes them.
  - So does merging unary terms into the bilinear factors (Section 3.4).
- **Constants.**
  - Proven against proven, the single tree loses only from `n ≈ 49`
    (face-exact bound) or `n ≈ 86` (Corollary 2.1).
  - Against computed certificates it loses from `n ≈ 29` or 46; counting
    convex programs, from 32 or 51.
  - At the sizes of the program's SCIP probe (`n <= 16`), the proven
    single-tree bound is 2–3 orders of magnitude below the computed
    certificates: `L_16(1e-6) = 376` against 5.1e5.
  - Actual single trees are far above the lower bounds. A bisection tree
    with the note's relaxation already exceeds the computed certificate at
    `n ≈ 9` (Section 5). The shell certificates are far from optimal: 3.1e3
    leaves per bag per halving for a two-variable bag.
- **Algorithm.** The decomposition side is an existence result that needs
  `x*` to accuracy `sqrt(eps/|T|)`. Certifying that a local solution is
  global is the whole difficulty (Section 6, item 3).
- **Useful message for solvers.** Separator-cell dynamic programming with
  gradient-based affine child bounds avoids the per-box cluster effect of
  termwise relaxations, and the drift condition (`theta` of order `c/M`) is
  the design constraint.

## 7. Per-claim verdicts

| Claim | Location | Verdict | Fix |
|---|---|---|---|
| Lemma 1.1 | l. 151–156 | correct | — |
| Definition 1.2, remarks | l. 193–239 | correct | "Checking": each pair `(B, D)` is one program; state the pair count (Section 1.3) |
| Lemma 1.3 | l. 243–255 | correct | — |
| Lemma 1.4 | l. 259–275 | correct | — |
| Lemma 1.5 | l. 283–297 | correct (also numerically) | — |
| Section 1.6 | l. 328–340 | correct as a remark | configurations range over continuous hulls |
| Corollary 2.1 | l. 357–384 | correct | — |
| Path-family facts, constants | l. 386–430 | correct | — |
| Coverage statement "does not cover McCormick" | l. 431–436 | gap | face-exact Theorem 1 covers McCormick and the note's relaxation, with bound `0.57 (5/3)^n` |
| Lemma 2.2 | l. 440–459 | correct | — |
| Proposition 2.3 | l. 461–489 | correct | Summary item 6 and status table: `exp(Omega(w))` only above the `pi/(4e)` threshold |
| Proposition 2.4 | l. 491–532 | correct | "tight up to constants" means up to `C^d` |
| Theorem 2.5 | l. 534–554 | correct | — |
| Proposition 2.6 | l. 556–596 | correct as stated (root child, 1D separator) | — |
| Lemma 3.1 | l. 602–619 | correct | — |
| Lemma 3.2, (3.1) | l. 621–654 | correct | — |
| Theorem 3.3 | l. 658–683 | correct, not new (as stated) | — |
| Theorem 3.4 | l. 687–801 | correct | center in `X0`; the summary base needs `alpha' A <~ w M_a^2/c_g` |
| Remark 3.5, center and multipliers | l. 821–827 | correct with fix | the center needs `abs(x̂ - x*)_inf <= h_0 = O(sqrt(eps/abs(T)))`, not only Euclidean `O(sqrt eps)` |
| Remark 3.5, constants | l. 831–834 | false as stated | `theta = 1/2` does not work for `n > 16`; say `theta = 1/16` |
| Remark 3.6 | l. 836–848 | correct | cite the `b` sweep (Section 2.5): the threshold scales with `(1-b)/(2b)` |
| Section 3.5, Conjecture 3.7 | l. 866–888 | appropriate | — |
| Theorem 4.1(a) | l. 899–909 | correct | add `max(·, 0.57 (5/3)^n)` from face-exact Theorem 1 |
| Theorem 4.1(b), (c) | l. 911–950 | correct | — |
| Separation "uniformly in `eps <= 0.2/n`" | l. 923–924 | false as stated | the closed form is 0 at `eps = 0.2/n`; use `L_n(eps)` or `eps <= 0.1/n` |
| Scope: McCormick not covered | l. 954–958 | gap | McCormick separation follows from face-exact Theorem 1 plus (b) |
| Scope: "counting relaxation solves only strengthens" | l. 969–972 | false as a count | programs = pairs, 3–5x the leaves; `log^2` asymptotically; or use per-leaf `beta` |
| Scope: crossover `n ≈ 45–50` | l. 973–978, 1111–1117 | correct for Corollary 2.1 | with face-exact Theorem 1: `n ≈ 29` |
| Factorization dependence | Summary 4–5, Section 4 | significance gap | the proved mechanism disappears under the balanced split (Section 3.4); state it |
| Section 5 tables | l. 991–1141 | correct (reproduced) | E3 is one-sided; add the sharper check |
| Section 6, item 1 "one natural relaxation family" | l. 1146–1153 | overstated | alphaBB on isolated bilinear terms is dominated by McCormick and unused; cite face-exact Theorem 1 |
| Section 6, item 11 novelty | l. 1196–1203 | fair | read Berenguel et al. in full |

## 8. What I verified myself, and commands run

All commands were run from
`research-20260929/reviews/decomposition-review-checks/` with Python 3.13.11,
NumPy 2.5.1, SciPy 1.18.0 and mpmath 1.3.0. Logs are in `logs/`. These are
targeted local checks, not CI.

**By hand.** Every proof listed in Section 7:
- the DP recursion and the running-intersection facts;
- the Schur-test bound on `Gamma`;
- the Young weights and the constants 768, 3072 and 384;
- the Stirling and `J_n` bounds;
- the Prop 2.4 expectation;
- the Prop 2.6 window argument;
- the (M_b) inequality for the note's relaxation.

**Commands.**
- `python3 constants.py > logs/constants.log`:
  - the Corollary 2.1 constants and threshold;
  - `L_n(eps)` by scipy quadrature, including at `eps = 0.2/n`;
  - the Theorem 4.1(b)/(c) constants and `M_a`;
  - the factorization bases and the balanced-split `L_n`;
  - the (M_b) random test and the face-exact bound;
  - the crossovers, including proven against proven.
- `python3 indep_dp.py gap 16 4 8`, `gap 20 3 8`, `gap 20 4 8`
  (`logs/gap_n16_mu4_j8.log`, `logs/gap_n20_mu3_j8.log`,
  `logs/gap_n20_mu4_j8.log`).
- `python3 indep_dp.py trace 20 3 8 > logs/trace_n20_theta8.log`.
- `python3 indep_dp.py pairs 4 4 6 8 10 12 14` and
  `python3 indep_dp.py pairs 1 4 8 12 16` (`logs/pairs_theta16.log`,
  `logs/pairs_theta2.log`).
- `python3 indep_dp.py valid 5 0 3 6` and `valid 6 1 2 5`
  (`logs/valid_n5_seed0.log`, `logs/valid_n6_seed1.log`).
- `python3 indep_dp.py sweep 6 B 24,40 MU` for `B ∈ {0.5, 0.6, 0.7, 0.8, 0.85}`
  and `MU ∈ {1, 2, 3, 4}` (`logs/sweep_b*_mu*.log`).
- `python3 split_bb.py REL CMODE EPS 2 3 4 5 6 7 8` for:
  - `REL ∈ {note, balS}`, `CMODE ∈ {zero, seed0}`,
    `EPS ∈ {1e-2, 1e-4, 1e-6}`;
  - `balR zero 1e-4 2..7`;
  - `balS+cvx zero 1e-4 2..10` and `balS+cvx zero 1e-6 2..9`;
  - `note+cvx zero 1e-4 2..7`;
  - `note zero 1e-4 8 9` and `note zero 1e-6 8`.

  Logs: `logs/split_*.log`.

**Read, not rerun.** The note's `logs/*.log`, the face-exact note's
`bb_runs_v2.log` and `leaves_abbS.log` (for the `abbS` cross-check), and
[C] Sections 1–3 and 6.
