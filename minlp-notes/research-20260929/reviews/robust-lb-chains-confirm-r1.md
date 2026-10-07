# Referee check of the first revision of "Split-robust lower bounds on uniform chains"

Date: 2026-09-30. Note checked:
`research-20260929/theory-robust-lb/robust-chains.md`, revised after review
round 1 (1452 lines; changes listed in its Section 10.1). The review that
asked for the changes is `reviews/robust-chains-review.md`. I wrote neither
the note, its scripts nor the review. My scripts and logs are in
`reviews/robust-lb-chains-confirm-r1-checks/`. They share no code with the
note's `chains/` scripts or with the review's checks.

Following `AGENTS.md`, I ran only targeted checks: no project-wide
verification and no CI. I did not commit anything or edit the note.

Labels:

- **proved**: checked by hand, step by step;
- **exact**: checked in exact arithmetic (sympy on rationals, or an
  algebraic number evaluated to 30 or more digits);
- **float**: recomputed in floating point (numpy, scipy/HiGHS, cvxpy with
  Clarabel), not interval-certified.

## Verdict in brief

All ten review items were applied correctly. I recomputed every number that
changed, with my own code, and every one agrees with the note. The proofs
added in the revision are correct: Proposition A.3, the window bookkeeping
and leftover-window bound of Theorem C.3, `Lambda = 2a + 2b + g`, the exact
corner values, and Proposition C.5. No item was refused. The work the authors
list as not done was outside the review's requests, and the reasons they
give are sound.

Two minor problems remain. Both are wording or labelling problems, not
errors in the proofs.

1. **The moment-SOS scope statements drop the condition of Proposition
   C.5.** The Summary, "For solvers" and Section 8 say without condition
   that the order-2 sparse moment-SOS relaxation is exact at the root of the
   chiral chain. Proposition C.5 proves this only when every box constraint
   is localized in every clique that contains its variable, and it says the
   other cases were not checked. I checked them, and the condition matters.
   If each box constraint is attached to one clique in the wrong orientation,
   and no redundant ball constraints are added, the root gap is 0.055 at
   `n = 5` and 0.207 at `n = 8` (float). Section 6 also identifies C.5's
   relaxation with those of Waki et al. and Lasserre. Neither paper
   localizes a box constraint in every clique by default. Details in
   Section 2.1.
2. **Statements about WALL that hold for all `n` rest on checks for
   `n <= 16`.** The note says without qualification that classes (a) and
   (a0) are exact at the root of WALL (Summary item 1, "For solvers"). It
   also says that the fixed balanced split has no cover of size independent
   of `n` (Section 2.3). These claims are true. A short proof, given in
   Section 2.2, proves them for every `n` and removes the hypothesis of
   Proposition A.3. As written, though, the note supports them only in
   floating point for `n <= 16`. The note should either qualify them or add
   the proof.

| Review item | Verdict |
|---|---|
| 1. Part 1 headline overclaims (WALL) | **fixed.** All WALL numbers recomputed (float; `Delta` exact). The new Proposition A.3 is correct. Its hypothesis is in fact provable (Section 2.2). |
| 2. Domain-wall remark | **fixed.** End-defect example recomputed. |
| 3. Relaxation scope (moment-SOS) | **fixed in Section 4.6.** The identities are exact and the SDP values recomputed. The Summary, "For solvers", Section 8 and the Section 6 attribution omit Proposition C.5's localization condition (remaining problem 1). |
| 4. "Every split class in [R] contains the balanced split" | **fixed.** Checked against [R, Section 1.2]. |
| 5. Corner cap for "any reference measure" | **fixed.** |
| 6. Leftover windows in Theorem C.3 | **fixed.** Bookkeeping, the product bound, 0.8138 and the threshold 2.3085 all recomputed. |
| 7. Binding terms in Section 4.3 | **fixed.** |
| 8. "1.0033 analytic" | **fixed.** `Lambda` proved by hand; the table of fully analytic bases recomputed. |
| 9. Loose ceilings | **fixed.** The exact corner values are proved; `mu0` and the ceilings recomputed with a different optimizer. |
| 10. Minor items | **fixed.** |

## 1. Each item, checked from scratch

### Item 1. WALL and Proposition A.3

**Text.** Summary item 1 (lines 35–84) now says "under (H1)" and states the
WALL result. Section 2.3 is retitled. The new Section 2.5 contains
Proposition A.3. Theorem A.2 is unchanged.

**Basic facts** (`c1_wall.py basic`, `c1_basic.log`; float):

- `c = 0.337723198904`. The minimum of `u'` on a grid of `10^6 + 1` points
  is 1.015080, and `u(-1) = -1.521`. I also found this minimum by hand: it is
  at the root `-0.0372` of `u''`, where `u' = 1.01508`.
- `m = phi(-1, c) = -0.8608039414`. The minimum on a `3001^2` grid is
  `-0.8608038368` at `(-1, 0.338)`. `phi(-1,-1) - m = 0.301804`, and the best
  diagonal value lies 0.291285 above `m`. These agree with the note.
- My own grid DP (3001 points, then coordinate-wise Brent polishing) matches
  the closed-form wall value (even `n`) or alternating value (odd `n`) to
  `2e-15`, for `n = 2..16`.
- **Proved:** for even `n` all `n/2` configurations `x^(j)` have the same
  value. Each has `n/2 + 1` entries equal to `-1`, `n/2 - 1` entries equal
  to `c`, and the same bond multiset. For odd `n`, the alternating
  configuration attains the lower bound of Proposition A.1(1).

**Proposition A.3, proof (proved).**

- I checked step 1 by cases on the parity of `i` and its position relative
  to `2j` and `2j'`.
- Step 2 is correct. A box containing `x^(j)` and `x^(j')` contains
  `[-1, c]` at indices `2j` and `2j+1`, so it contains `x^(j+1)` and hence
  `H_j`.
- In step 3, the identification of the three free factors is correct.
  `x^(j)` has `(y, z) = (-1, c)` and `x^(j+1)` has `(c, -1)`.
- The family's means agree: the right factor's mean is
  `p t - (1 - p) = s(1 + c) - 1`.
- The formula for `Delta(s, t)` is correct, and so is the condition for
  `p <= 1`.
- Step 4 (monotonicity and counting) is correct.
- The proposition needs the global optimality of the walls, and it states
  this hypothesis.

**Fooling value** (`c1_wall.py family`, `c1_family.log`; mpmath at 50
digits, independent of the note's code):

- `Delta(779/10000, 467/2000) = 0.0113432715072065816942716048937`. This
  equals the note's value to all 30 printed digits.
- With `s = 31/400` and `t = ybar`, `Delta = 0.0113430041`. The optimum of
  the closed form is `0.0113432716` at `(0.077893, 0.233524)`.

**Optimality of the family** (`c1b_dual.py`, `c1b_dual.log`; float). I
computed the dual bound of the fixed balanced split on `H_j` with affine
shifts `(ly, lz)`, minimizing every factor directly: edges in 1-D, and the
interior from an `801^2` grid with polishing. Its best value is
`LB - f* = -0.0113432715` at `ly = -lz = 0.23409`. So the gap on `H_j` is
`0.0113432715`, to about `1e-10`. The note says "optimal up to about
`1e-7`", which is conservative. My first, coarser dual run gave a value
`2e-8` too high, because a minimizer of the middle factor was missed (kept
in `c1_family.log` as a negative example).

**Root gaps of the fixed split on WALL** (`c3_wall_rootgap.py`,
`c3_wall_rootgap.log`). I solved a grid LP (164 points per axis, plus `c`)
for even `n = 4..16`. It gives 0.0205219 per wall pair for `n <= 14`, and
0.1435845 in total at `n = 16`. These are lower bounds on the gap. The
note's column-generation values are 0.0205224 per pair and 0.1436159 at
`n = 16`. Both codes show that the increment drops slightly at `n = 16`
(`7 × 0.0205224 = 0.14366` against 0.14362). So "`0.0205 (n/2 - 1)`" holds
at the printed three digits but is not an exact formula. No change is
needed. The cap `phi(-1,-1) - m = 0.302` (Proposition A.1(1)) is correct.

**Branch-and-bound counts.** I did not re-run them. The note's counts
(`logs/bb_wall.log`: spread 3, 5, ..., 15; bisection 4, 7, ..., 22; one leaf
for odd `n` and for class (a)) match the review's independently computed
counts exactly. The table reproduces the log.

### Item 2. Domain-wall remark

`c1_wall.py endfrust`, `c1_endfrust.log` (own DP, float):

- `phi` has minimum `-0.35125` at `(-1, 0.45)`. I also checked this by hand:
  `phi(-1, y) = -0.25 + y^2/2 - 0.45 y`.
- For odd `n`, the minimizer is `(-1, 0.45, ..., -1)`.
- For even `n = 6..12`, the minimizer has a defect at one end, and its
  mirror image has the same value (my DP returned the mirror image at
  `n = 6`).
- With both ends restricted to `<= -0.9`, the best value is higher by
  0.148774 (`n = 6`) and 0.157419 (`n = 8, 10, 12`).
- For `n = 4`, the minimizer is the symmetric
  `(-0.6048, -0.2419, -0.2419, -0.6048)`.

All of this agrees with the note. The old sentence is withdrawn and both
cases are described (Section 2.2 remarks, lines 357–367).

The restricted values are grid-DP values, and a grid value is an upper
bound on the restricted minimum. So "worse by at least 0.149" is accurate
only up to the grid error. It is labelled floating point, which is
adequate.

### Item 3. Relaxation scope: Proposition C.5

`c2_chiral.py identities` (exact), `c2_chiral.py sdp` and
`c4_sdp_variants.py` (float):

- The decomposition of the bracket has residual 0, and so do the two
  end-term identities, the identity `1 + y = (1+y)^2/2 + (1-y^2)/2`, and the
  telescoping for `n = 6`.
- Each term has degree at most 4. It is either a sum of squares or a sum of
  squares times one linear box constraint, on one pair clique.
  `b/2 - g >= 0` and `a - g >= 0` follow from `g <= b/2`. The certificate
  uses `1 + x_{e+1}` and `1 - x_e` on clique `e`, and both bounds of `x_1`
  and of `x_n` on the end cliques.
- My own order-2 moment SDP with every box constraint localized in every
  clique gives `3.1e-9` (`n = 5`) and `1.3e-9` (`n = 7`). This agrees with
  the note's `1.9e-8` and `1.8e-8`.

So Proposition C.5 is correct as stated. The remaining problem concerns the
statements around it (Section 2.1).

### Item 4. Classes of [R]

[R, Section 1.2] defines (a) as `span{1, t, t^2, u_i}`, (a0) as
`span{1, t, u_i}`, and `b_d` relative to a base split. [R, Section 1.1]
defines the balanced and unsplit factorizations.

- (a) and (a0) contain every reweighting of `u`, so they contain the
  balanced split.
- `b_d` contains it exactly when the two base splits differ by
  polynomials of degree at most `d` (Lemma 1.1).

The new Summary text (lines 55–62) is correct.

### Item 5. Corner cap restricted to Lebesgue measure

The Summary (lines 147–152) and Section 5 (lines 1047–1053, 1110–1112) now
restrict the cap to Lebesgue measure and say that other product measures
were not optimized. Fixed.

### Item 6. Leftover windows in Theorem C.3

- **Bookkeeping** (`c2_chiral.py leftover`, `c2_part1.log`). I enumerated
  the windows directly for every `k <= 11` and `n < 200`. The number of
  full windows is always `G = floor((n+1)/(k+1))`, and there is a leftover
  window exactly when `r = n - G(k+1)` lies in `[1, k-1]` (0 mismatches).
  When `k + 1` divides `n`, the pinned index is `n`. The extended Lemma B.1
  covers this case: an end index lies in one factor only. The remark after
  the proof of Theorem C.3, step 1, about end windows is also correct.
- **Item 1 of the theorem.** Transport gives `Phi_r <= exp(-mu gamma_r)`,
  and `gamma_r >= 0`. Correct.
- **Item 2, product bound (proved).**
  - For a coordinate `j` with `0 in B_j`, the factor is `|B_j|/2 <= 1`.
    Otherwise `|B_j| <= 1 - |p_j|`.
  - The separable bound `f_r(p) <= sum c_j p_j^2` follows from
    `|xy|(|x| + |y|) <= x^2 + y^2` on `[-1, 1]^2`.
  - I computed the suprema from their closed-form critical points (where
    `2 M d (1 - d) = 1`, `M = mu c`), not on a grid. At `mu = 2.112` they
    are 0.5, 0.5 and 0.81381. The interior supremum reaches 1 at
    `mu = 2.30854`. At that `mu` the end constant still gives 0.5224.
  - So "every `r` and every `mu < 2.3085`" is correct.

### Item 7. Binding terms

`logs/checks_note.log` lists the terms 0.8314 (`0.75 -> 0.8`), 0.8284,
0.8284, 0.8201, 0.8190 and the point-mass term 0.8138. The corrected
sentence (lines 893–899) matches this list.

### Item 8. Fully analytic base

- **`Lambda` (proved by hand).** `d_x W = (a - g y) x + y (b + g y/2)`. For
  fixed `y`, the maximum over `x` of its absolute value is
  `a - g y + |y| (b + g y/2)`. This is increasing on `[0, 1]`, with
  derivative `b - g + g y > 0`, and decreasing on `[-1, 0]`, with derivative
  `-(b + g + g y) < 0`. Its largest value is `a + b + g/2`, at `y = -1`. The
  same argument works for `d_y W`. A grid check at four further parameter
  points agrees (`c2_part1.log`). Window-end and length-1 windows have
  smaller constants, so `Lambda = 2a + 2b + g` is valid for every window
  variable.
- **Bases** (`c2_part1.log`). The fully analytic bases are 1.00093, 1.00186,
  1.00322, 1.00513, 1.00613, 1.00717, 1.00802 and 1.00867 for
  `k = 7, 8, 10, 15, 20, 30, 50, 100`. The limit is 1.00934. The function
  `((k-1) g_inf - a q)/(k+1) = g_inf - (2 g_inf + a q)/(k+1)` increases in
  `k`, so the supremum is not attained. The values with `Lambda = 3.4` are
  1.00077 to 1.00714. The transport bases with LP gaps are 1.0004, 1.0015,
  1.0025 and 1.0033 for `P_2` (`k = 4..7`), and 1.0046 and 1.0049 for `P_1`
  (`k = 6, 7`). For item 2, `(1/0.83139)^{1/8} = 1.02335`. All agree with the
  note.
- The labels are now right. "1.0033" carries "with the LP-computed window
  gap", and "fully analytic" is used only for the Proposition C.2 bound.

### Item 9. Ceilings

- **Exact corner values (proved).** On `[0, 1]^2`, `d_x W >= 0` because
  `a - g y > 0`, and `d_y W >= 0` because `b - g x/2 >= 0`. The end terms
  are nondecreasing. So the factor minima of the base split equal
  `f_k(s)`. Since `LB <= min_B f_k = f_k(s)`, we get `V(B) = f_k(s)` for
  every class. A sampling check on 200 random corner boxes found no
  violation (`c2_part2.log`). The symmetry `W(-y, -x) = W(x, y)` is
  correct.
- **`mu0`** (`c2_chiral.py corner`, `c2_part2.log`). I used a different
  parametrization (`s = 1 - exp(-|z|)`), Powell followed by BFGS, and other
  random starts. I get `mu0 = 3.2379, 3.1527, 3.0990, 3.0620` for
  `k = 4..7`, at the same boxes as the note. Ceilings: 1.0075, 1.0268,
  1.0441 and 1.0582 for class (a); 1.0502, 1.0607, 1.0828 and 1.0880 for
  `P_1`. For long windows, `mu0 = 2.9983` (`k = 10`) and 2.9283 (`k = 20`).
  The uniform-bulk limit is 2.8626 at `s = 0.8321`, giving
  `exp(2.8626 g_inf) = 1.1608`. All agree with the note.
- The direction is right: these are upper bounds on the method's ceiling,
  so a better search can only lower them. "About 1.16" is labelled
  heuristic. The review's proved band for `Gamma_n` (its Section 4.3(i))
  would justify `gamma_k/(k+1) -> g_inf`; the note conservatively says
  "not checked beyond `k = 12`".

### Item 10. Minor items

- `(79/8)^{1/5} = 1.581` and `(144/15)^{1/5} = 1.572`. The last steps are
  `79/55 = 1.436` and `144/102 = 1.412`. Correct.
- The sparse-narrow extrapolation is now labelled as resting on one size.
- Theorem A.2: `L` now covers the single factor at `n = 2`. With
  `k >= 2`, the case `n = 2` falls under step 3, and
  `sqrt(2)(n-1) L h <= eps/2`. Correct.
- The table cell is fixed.

## 2. Remaining problems

### 2.1 Moment-SOS scope: the localization condition is dropped (minor)

**Where.**

- Summary item 3, scope bullet (lines 139–145): "the minimal-order sparse
  moment-SOS relaxation (order 2, pair cliques, box constraints) is exact at
  the root".
- "For solvers" (lines 174–176): "moment-SOS relaxations of order 2 ... are
  exact at the root".
- Section 8 (lines 1299–1301).
- Section 6 (lines 1200–1212): "The relaxation of Proposition C.5 is the
  correlative-sparsity relaxation of Waki, Kim, Kojima and Muramatsu ...
  and of Lasserre".

**Why it matters.** Proposition C.5 assumes that each box constraint is
localized, with a bivariate multiplier, in every clique that contains its
variable. Its proof needs `1 + x_{e+1}` and `1 - x_e` on clique `e`. The
standard formulations differ:

- Lasserre (2006), Assumption 3.2 (local copy, `fulltext.md` line 177),
  *partitions* the constraints among the cliques. Each constraint is
  localized in one clique only, and a redundant ball constraint is added per
  clique.
- The basic sparse relaxation of Waki et al. (2006), their (20), gives each
  constraint's multiplier the support of the constraint's own variables, so
  a box constraint gets a univariate multiplier. Their Section 5.5 enlarges
  the support to one clique containing the constraint, or to the union of
  all such cliques (local copy, `fulltext.md` line 571).

I checked these variants (`c4_sdp_variants.py`, `c4b_scs.py`,
`c4c_ball.py`; float, Clarabel, one SCS cross-check):

| order-2 sparse relaxation, pair cliques, linear box constraints | `n = 5` | `n = 8` |
|---|---|---|
| every box constraint in every clique (Proposition C.5) | `3e-9` | `1.5e-9` |
| one clique per constraint: `1 + x_i` in `(i-1, i)`, `1 - x_i` in `(i, i+1)` | `1e-9` | `1.6e-9` |
| one clique per constraint, opposite orientation | **`-0.0553`** (SCS: `-0.0553`) | **`-0.2072`** |
| the same, plus Lasserre's ball constraint `2 - x^2 - y^2 >= 0` per clique | `2e-9` | `3.7e-9` |
| Waki et al. (20): univariate multipliers for box constraints | effectively unbounded (solver value `-1.2e7`) | effectively unbounded (`-2.3e7`) |
| the same, plus moment bounds `abs(y_alpha) <= 1` | `-0.0628` | – |

So the order-2 sparse relaxation is root-exact in some legitimate
implementations and not in others.

- *Proved* for the "every clique" setting and for the one-clique assignment
  in the right orientation (the same certificate).
- *Float only* for Lasserre's construction with ball constraints.
- Not exact without either condition.

The main message of Section 4.6 is unaffected. Theorem C.3 concerns
factorable relaxations with shared `x_i` and `x_i^2` lifts, not moment-SOS
relaxations.

**Suggested fix.**

- Add the condition, for example "with each box constraint localized in the
  cliques that contain its variable, or with Lasserre's redundant ball
  constraints", to the Summary bullet, "For solvers" and Section 8.
- In Section 6, say that C.5's relaxation is a variant: Lasserre assigns
  each constraint to one clique, and Waki et al.'s basic form uses
  univariate multipliers for univariate constraints.
- Proposition C.5's parenthetical "this case was not checked" can be
  replaced by the table above (labelled floating point).

### 2.2 WALL claims for all `n` rest on `n <= 16` (minor; a short proof is available)

**Where.**

- Summary item 1 (line 70): "Classes (a) and (a0) are exact at the root of
  WALL".
- "For solvers" (lines 167–169): "letting the solver reweight `u` ...
  closes the root".
- Section 2.3 (lines 379–382): the fixed balanced split "has no cover of
  size independent of `n`".
- These rest on `logs/wall_basic.log`, which covers `n <= 16` only. The
  Section 7 status row and Section 8 qualify them; these three places do
  not.

**A proof for every even `n >= 4`.** Global optimality for odd `n` is
already proved in the note.

Split `f_n` as follows. Bond `e` joins `x_e` and `x_{e+1}`.

- First bond: `F_1 = u(x_1) + b x_2 (x_1 + 1)`.
- Last bond: `F_{n-1} = u(x_n) + b x_{n-1} (x_n + 1)`.
- Odd interior bonds (`e = 3, 5, ..., n-3`): `G = b(x+1)(y+1) - b`.
- Even bonds (`e = 2, 4, ..., n-2`):
  `H = u(x) + u(y) + b x y - b(x + y)`.

Properties of this split:

- It is a split of `f_n` (sympy: residual 0 for `n = 4, 6, 8, 10`;
  `c1c_split_identity.log`).
- Relative to the balanced split it moves `u(x_i)/2` and `b x_i` between the
  two factors of `x_i`, so it lies in class (a0).
- Its factor minima:
  - `F_1, F_{n-1} >= u(-1)`, because `u' > b` on `[-1, 1]`;
  - `G >= -b`;
  - `H >= H(-1, c)`.
- Their sum, `2 u(-1) - (n/2 - 2) b + (n/2 - 1) H(-1, c)`, equals the wall
  value for every `n` (sympy, symbolic in `n`).

So the walls are global minimizers for every even `n`. The hypothesis of
Proposition A.3 then holds, and classes (a0) and (a) are root-exact for
every `n`.

The only non-symbolic step is `min_{[-1,1]^2} H = H(-1, c)`
(`c1_wall.py a0`, `c1_a0.log`).

- I enumerated the corners and the edge critical points by exact real-root
  isolation (sympy, rational coefficients).
- I found the interior critical points from the exact resultant in `x`,
  with `y` solved at 40 digits.
- The minimum is `H(-1, c) = H(c, -1) = -0.759607882868`. The next
  candidate is 0.5756 higher. A `4001^2` grid agrees.

This step is checked with exact root isolation and high-precision
evaluation, but it is not interval-certified.

**Suggested fix.** Either add "(checked for `n <= 16`, floating point)" at
the three places, or add the split above as a short lemma. The lemma would
remove the hypothesis of Proposition A.3, the corresponding open item in
Section 8 and the qualifier in the Section 7 status row.

## 3. Items the authors did not apply

- **"No review item was left unaddressed."** Correct.
- **The 801-point grid LP was stopped.** Acceptable. My dual bound confirms
  the closed-form value to about `1e-10` (Section 1, item 1).
- **Not done: a proof of the walls' optimality, (a)/(a0) beyond
  `n = 16`, and covers for the end-defect example.** None of these was
  requested. Section 2.2 above closes the first two. The third is honestly
  recorded as open in Section 8.

## 4. Was anything strengthened beyond the evidence?

I compared every revised passage with its evidence.

- The new claims about the chiral chain are proved or correctly labelled:
  `Lambda`, the exact corner values, the leftover bound, the analytic table
  and the ceiling values. The heuristic 1.16 is labelled.
- The only statements broader than their support are the two minor
  problems of Section 2.
- The authors withdrew rather than extended the old claims:
  - "`mu0` stays near 3.5–4" and the estimate 1.2;
  - "every split class considered in [R] contains the balanced split";
  - the always-a-wall remark.
- The novelty statements are hedged. Proposition A.3 and the identity of
  Proposition C.5 are credited to the review.

## 5. Commands run

All from `reviews/robust-lb-chains-confirm-r1-checks/`, with
`OMP_NUM_THREADS=1` (and `OPENBLAS_NUM_THREADS=1` where noted in the
scripts). The machine was heavily loaded, with a load average near 38. Each
run took between a few seconds and a few minutes.

| Command | Log | What |
|---|---|---|
| `python3 c1_wall.py basic` | `c1_basic.log` | WALL constants; own DP + Brent polish, `n = 2..16` |
| `python3 c1_wall.py family` | `c1_family.log` | `Delta` at 50 digits; closed-form optimum; first (coarse) dual |
| `python3 c1b_dual.py` | `c1b_dual.log` | sharper dual bound of the fixed split on `H_j` |
| `python3 c1_wall.py a0` | `c1_a0.log` | period-two class-(a0) split; `min H` by critical-point enumeration |
| `python3 c1c_split_identity.py` | `c1c_split_identity.log` | split identity and wall-value identity (sympy) |
| `python3 c1_wall.py endfrust` | `c1_endfrust.log` | end-defect example |
| `python3 c3_wall_rootgap.py 4,5,6,8,10,12,14,16 161` | `c3_wall_rootgap.log` | grid-LP root gaps of the fixed split on WALL |
| `python3 c2_chiral.py identities\|lam\|analytic\|leftover` | `c2_part1.log` | C.1/C.5 identities, `Lambda`, analytic bases, leftover suprema, window bookkeeping |
| `python3 c2_chiral.py corner`; `python3 c2_chiral.py sdp` | `c2_part2.log` | corner monotonicity, `mu0`, ceilings; own order-2 SDP |
| `python3 c4_sdp_variants.py`; `python3 c4b_scs.py`; `python3 c4c_ball.py` | `c4_sdp_variants.log`, `c4b_scs.log`, `c4c_ball.log` | localization variants of the order-2 sparse relaxation |

Literature examined for Section 2.1: the local copies
`literature/papers/lasserre2006-convergent-sdprelaxations-in-polynomial-optimization/fulltext.md`
(Assumption 3.2 and the construction of `Q_r`) and
`literature/papers/waki2006-sums-of-squares-and-semidefinite/fulltext.md`
(the sparse relaxation (20) and its Section 5.5). I did not search further.
Whether particular software packages (for example TSSOS or SparsePOP)
localize univariate constraints in every clique was not checked.
