# Review of `separable-omega.md` (the rule `omega` on separable instances)

Reviewed note:
[`../bb-complexity/branching-competitiveness/separable-omega.md`](../bb-complexity/branching-competitiveness/separable-omega.md),
with its scripts in `../bb-complexity/branching-competitiveness/separable/`.
Context read: `competitive-branching.md` (main note), `n-dimensional.md`, and
[`competitive-recheck.md`](competitive-recheck.md). Date: 2026-09-29.

I did not write the note. All checks below use my own scripts in
[`separable-omega/`](separable-omega/). They share no code with the author's
scripts. The only thing taken from the author is the definition of two test
instances (the knot rule of the quadratic interpolant and the dyadic caps),
which I reimplemented so that the same instances are tested. Everything is
exact rational arithmetic (`fractions`, `sympy`), except one guillotine DP on
candidate grids. That DP runs in floats with a conservative guard, and every
certificate it returns is rebuilt and checked box by box in exact arithmetic.

## Verdict

The proofs of the six numbered results are essentially correct. I found one
substantive gap in Theorem C, one false claim about `omega`, one false claim
about the deficit rule, and two numerical conclusions that do not survive
finer or stated-rule recomputation. The largest finding is positive: the open
question of Section 6 has an answer. The ambiguity of Theorem C does iterate,
and on the same instances every I1 rule's worst-case ratio grows exponentially
in `n`.

| Item | Claim | Verdict |
|---|---|---|
| 1 | Lemma 2.1 (products of 1D minimizer trees), phases | Correct. It needs the coordinate-wise minimizer selection that Section 1.1 assumes |
| 2 | Lemma T, Theorem A | Correct. The bounds are loose: at most 1 split node inside a valid interval was observed, against 5, 26, 75 |
| 2' | Corollary A' | Correct up to two slips. The displayed formula is false at `n_P = 1`. The case `tau = 0` is outside Theorem A as stated, but Theorem 1' covers it |
| 3 | Theorem B (`omega <= 112 N_opt`, `deficit <= 64 N_opt`) | Correct |
| 3' | Sketch for `n - 1` sharp coordinates | Plausible, and labelled as a sketch in Sections 5 and 7.2. "Answers (2)" overstates it: it cites Theorem B, which is 2D only, and the sketch does not cover `deficit` |
| 3'' | "`deficit` is competitive within a phase (Theorem A)" (Answers, item 2) | **False** in the sense of Corollary A'. Counterexample below |
| 4 | Theorem C (`7/3` deterministic, `(7 - 4/n)/3` randomized, every `n >= 2`) | The bounds are true. **The proof is written only for `n = 2`.** The author's parameter choice for `n >= 3` fails from `n = 12` on. I give a valid choice for all `n`, with a symbolic check. The information model is respected |
| 4' | "`omega` itself attains `7/3` there" | **False for `n >= 3`.** On `A_n`, `omega` uses `2^(n+1) - 1` nodes. A tie-free variant does the same on every labelling |
| 4'' | "Whether repeated ambiguity can push the lower bound beyond `7/3` ... is open" | **Resolved here.** On the same instances, deterministic rules need ratio at least `11/3, 19/3, 31/3` for `n = 3, 4, 5`, and roughly `2^(n+2)/(3n)` in general |
| 5 | Proposition D | (a)–(c) are correct. (d) needs a qualifier. The table has small discrepancies |
| 6 | Lemma 3.2 (`N(b/2) <= 3 N(b)`) | Correct |
| — | Section 5: the drift "levels off near 1.5", "1.47 at `1e-11`" | **Wrong.** With finer grids and exactly verified certificates, `omega`/grid is 1.71–1.91 for `eps <= 1e-6`. At `1e-11` it is `44/23 = 1.91`, the n-dim note's value |
| — | Section 7.1: "`omega` within 5% of `OPT_min`"; "`omega` = grid optimum" on dyadic caps | **These depend on an undocumented tie rule.** Under the rule the note states, `omega/OPT_min` is 1.33–1.59 on caps × quadratic, and `omega` is 1.5–1.8 times the note's grid optimum on dyadic caps (`1e-3` to `1e-7`) |

## 1. Structure lemma and phases (Section 2)

**Lemma 2.1: correct.**

- The relaxation separates, and its minimizer set is the product of the
  coordinate minimizer sets.
- The invalid-box argument (all `w_i = 0` implies valid) is correct for every
  selection.

**Scope point.** Products of 1D trees need a selection `y_i(J)` that depends
only on the coordinate's own interval. Section 1.1 assumes this ("chosen by a
fixed deterministic rule"). A solver that picks a point of a non-singleton
optimal face from global data could break the product structure.

- Theorems A and B survive such a solver with minor changes. Inside a phase
  the other intervals are fixed, and Theorem 1 allows any minimizer at each
  node.
- It is worth one sentence in the note.

**Phases: correct.**

- The containment of a phase in `S_i(A; beta, tau)` is right, including the
  strict or non-strict tie condition.
- An internal node of a phase satisfies the split condition, and so does its
  parent inside the phase. So phases are ancestor-closed subsets of the
  internal nodes of `S`.

## 2. Lemma T, Theorem A, Corollary A' (Section 4)

**Lemma T.** I rechecked every step.

- **Step 1.** The chain `a_l(y) - b <= m(y) < a_D(y) - beta` gives
  `a_l(y) - a_D(y) < kappa tau <= kappa L R`. The identity of Lemma 2.2(a)
  gives `(*)`.
  - Dividing `L gR < kappa L R` by `L > 0` gives `gR < kappa R`. The split
    point is interior, so `L > 0`.
  - The same argument gives `gL < kappa L`, and so `|l| < (1 + kappa)|D|`.
- **Step 2.** Each left step removes `R_k >= tau / L_k >= tau / |l|`. So
  `gR_j >= nL(j) tau / |l|`, and `(*)` gives `nL(j) L_j < kappa |l|`.
  - A left step whose child is still in the chain has `L_j > |l|/(1+kappa)`.
  - Hence `nL(j) <= kappa(kappa+1) - 1`, so there are at most
    `kappa(kappa+1)` left steps.
- **Step 3.** The split nodes inside `l` form an ancestor-closed forest. Its
  leaves are pairwise interior-disjoint and longer than `|l|/(1+kappa)`, so
  there are at most `kappa` of them. Every node lies on one of at most
  `kappa` root-to-leaf chains.

The constant `c_kappa = kappa(2 kappa(kappa+1) + 1)` is correct.

**Theorem A.** Both cases are correct. The first ancestor with `F >= -b` is a
leaf of `T_b`, because `F` does not decrease along a path (Lemma 2.2(b)).
Theorem 1' is a direct corollary of the main note's Theorem 1, applied to
`m + b`.

**Corollary A'.** The budget inequality
`beta + (d-1) tau >= eps + sum_k (F_k + w_k) = eps + sum_k m_k(y_k)` and the
slice form are correct. Two slips:

- **`n_P = 1`.** The displayed bound `4 n_P - 5 + c_{d-1}(4 n_P - 4)` equals
  `-1` at `n_P = 1`. The Summary correctly says "at most 5 if `n_P = 1`"; the
  corollary should say the same (`c_{d-1}`).
  - Explicit instance (`lemmaT_check.py`, Part 4): both coordinates are tents
    with the root minimizer `1/2`, and `omega` splits `x` at the root. The
    3-box certificate `[0,1] x {[0,2/5], [2/5,3/5], [3/5,1]}` has exactly one
    box meeting the phase segment `[0,1] x {1/2}`.
  - That phase has 1 internal node.
- **`tau = 0`.** Theorem A assumes `tau > 0`. If every other coordinate's
  minimizer is an endpoint, then `tau = 0`, `beta = eps + sum_k m_k(y_k)`,
  and the phase is the minimizer tree stopped at `beta`. Theorem 1' bounds
  it by `4N - 5`.
  - This case is common: 5,218 of the 10,023 random 2D phases I checked.
  - One sentence fixes it.

**Checks** (`lemmaT_check.py 1500 11`).

- **1D instances.** 3,000 cases (1,500 instances, each with strict and
  non-strict ties), about half convex and half non-convex, with three
  minimizer selections, `kappa in {1,2,3}` and `beta < 0` allowed.
  - Lemma T was checked on every leaf of `T_b`, and also on the maximal
    valid interval `[a, u*(a)]` started at every endpoint of a split node.
  - The maximum count was 1 for every `kappa`. The largest `|S|/N` was `5/3`.
- **Adversarial search.** Hill climbing over non-convex knot values also
  found at most 1 split node inside a valid interval, for `kappa = 1` and
  `kappa = 2`.
- **2D phases.** 10,023 phases of `omega` on random instances were checked
  against the slice budget. The largest internal count per `N_P` was 1.5.

## 3. Theorem B and the sketch (Section 5)

**Theorem B: correct.**

- **The sharp example.** `phi_J` is linear on each side of `c`, with slopes
  `±sigma + 2c - l - u`.
  - If `c` is interior, the slopes have opposite signs, since
    `|l + u - 2c| < u - l <= sigma/2`.
  - If the interval lies on one side of `c`, the slope points away from `c`.
  - So (S1) and (S2) hold, the minimizers are unique, and `m_z >= 0`
    because `|t - c| <= U - L < sigma`.
- **Phase 1.** It lies in `S_x(X; eps - omega0, omega0)`, with budget
  exactly `eps`.
- **After the `z`-split.** The subtree is the 1D tree `T_eps` restricted to
  `I`. The leaf count `2 #leaves(T_eps) + 2 (|S_1| + 1)` and the constants
  56 and 32 check.
- **Deficit rule.** The implication `F_x < -eps/2` is strict in all cases,
  including `omega0 = eps/2`.

**Check** (`thmB_review.py 1200 5`).

- **Instances.** 1,200 random instances, with the `x`-coordinate convex or
  non-convex and minimizer selections `wmax`, `left` and `right`. The
  sharp coordinate uses `sigma in {2, 3, 10}` and a random `c`.
- **Coverage.** Both coordinate orders (which covers both tie orders) and
  both rules.
- **Results.** (S1) and (S2) held on random intervals, and every bound of
  the theorem held. The largest leaves/`N_x(eps)` was 4.0 for both rules,
  and the largest phase-1 size/`N` was 1.33.

**Sketch for `n - 1` sharp coordinates.**

- **The budget claim is right.** With `U` the unsplit sharp coordinates,
  `b = eps - sum_U omega_k + |U| max_U omega_k >= eps`.
- **The summation is only indicated.** Phases with the same pattern of
  split sides have interior-disjoint roots, and phase roots are leaves of
  earlier phases. That gives a recursion with a constant depending on `n`.
  The number of states per sharp coordinate is 3 (unsplit, left, right), not
  2, so "at most `2^(n-1)` sides" undercounts. This is harmless for a sketch.
- **Numerical check.** For `n = 3` with two sharp coordinates, the largest
  leaves/`N_x(eps)` was 7 for both rules (300 instances).
- **Label check.**
  - Sections 5 and 7.2 and Summary item 3 correctly call it a sketch.
  - "Answers (2)" says "both are competitive when all but one coordinate is
    sharp (Theorem B)". Theorem B is 2D only, and the sketch covers only
    `omega`.
  - It should read: "`omega` and `deficit` in 2D (Theorem B); `omega` for
    `n - 1` sharp coordinates (sketch)".

**The deficit rule is not "competitive within a phase".** Answers (2) says
this follows from Theorem A. It does not.

- **Why Theorem A does not apply.** Theorem A needs `omega`'s threshold
  `w >= tau`.
  - A `deficit` phase splits `D` iff `F(D) < -max(beta, eps - beta)`. It is
    the minimizer tree stopped at a budget of at least `eps/2`.
  - The slice budget is `eps + m_other(y_other)`, which can be much larger.
- **Counterexample** (`thmB_review.py`, Part 3).
  - `x` has `m = t^2` (exact). `z` is the tent
    `H = max(0, (1-eps)t, (1+eps)t - eps)`, with root value `-eps/2`,
    `w = 1/4` and `m_z(1/2) = 1/4 - eps/2`.
  - `deficit` splits `x` first. Its first phase keeps `z = [0,1]` and has
    2, 3, 4, 5, 6, 7, 7, 8 internal nodes at `eps = 1e-3, ..., 1e-10`.
  - An explicit certificate, verified box by box, has exactly one box
    meeting the phase segment `[0,1] x {1/2}`: the strip
    `[0,1] x [2/5,3/5]`, with 1D pieces above and below it. So `n_P = 1`.
- **No global failure.** The whole `deficit` tree is also small, at most 17
  nodes, against `N_opt >= N_x(eps) = 7`. So this does not refute
  competitiveness of `deficit`; it only refutes the phase-wise claim.

## 4. Theorem C (Section 6)

### 4.1 The written proof (`n = 2`) and the information model

For `n = 2`, `r0 = 3/20` and `eps = 1/100`, every step checks exactly
(`thmC_check.py`).

- **Basic facts.** `H_R` and `H_N` are convex. Both roots have the unique
  minimizer `1/2` and value `-1/10`, and `min m_R + min m_N = 0`.
- **Cuts.** The `R`-cut children have margin `1/200`. Every `N`-cut child is
  invalid, with the bound and the sweep both giving `-37/200`.
- **Exact agreement regions.** `R = N` on `[155/398, 243/398]`, and
  `R - N = 19/100` on `[0, 3/398]` and `[395/398, 1]`. These contain the
  note's stated intervals.

**Information model.** At the root, every item is identical in all `A_i`:

- the box, `eps`, `alpha`, the incumbent and the relaxation value;
- the unique minimizer `(1/2, ..., 1/2)`;
- `f` on a neighbourhood of the minimizer, so the germ;
- `f` near every corner, checked exactly for `n = 2, 3, 4`. Near a corner,
  every coordinate has `R - N` equal to the same constant.

The deterministic bound needs only the root decision, so the argument is
sound.

- **Facets are not covered.** The instances do **not** agree near facet
  centres: `f(A_1) - f(A_2) = 19/100` at `(0, 1/2)`. So a rule that may see
  `f` near the whole boundary of the box, the literal analogue of Theorem 3's
  "both endpoints", is not covered. The note says "corners", which is
  accurate. A remark would help.
- **Randomized bound.** It is a correct averaging over `i`.

### 4.2 Gap: `n >= 3`

**The note's argument covers only `n = 2`.**

- The note gives the proof for `n = 2` and says "the other dimensions are
  checked exactly by `lb_coord.py`" for `n = 2, 3, 4, 6`. A finite check does
  not prove "every `n >= 2`".
- The text never says how to choose `r0` for `n >= 3`.
- The script uses `r0 = (n-1)/(4n) + 1/50`, that is, `c := 1/4 - r0 = 1/(4n) - 1/50`.
  - This **fails for every `n >= 12`**.
  - At `n = 12` the root value plus `eps` is exactly 0, so the root is
    valid, and the wrong-cut bound is already positive (`1/2200`).
  - For `n >= 13` both are positive.

**Fix, with a symbolic proof** (`thmC_check.py`, Part 1). With `c = 1/4 - r0`,
the conditions the proof uses are:

- (1) `lL` and `lR` dominate at `1/2`: `nc < 1/4 + eps/2`;
- (2) the root is invalid: `nc > eps`;
- (3) a wrong cut is invalid: `c > eps(2n-1)/(2n(n-1))`;
- (4) the right cut is valid: its margin is identically `eps/2`;
- (5) the agreement near the corners holds identically. `N`'s own lines
  dominate at `0` and `1` with slack `3 eps/(8(n-1))`.

Condition (3) implies (2). The admissible interval is non-empty iff
`eps < (n-1)/(2n)`.

- **Uniform choice.** `r0 = 1/4 - 1/(5n)` satisfies all conditions for every
  `n >= 2` when `eps = 1/100`, as a sign check of polynomials in `n`. It
  gives the note's `3/20` at `n = 2`.
- **Exact confirmation.** All items were also checked exactly for
  `n = 2, ..., 40`. With this choice Theorem C holds as stated for every `n`.

### 4.3 `omega` on these instances

"`omega` itself attains `7/3` there" (Summary item 4) is true only for
`n = 2`.

- **Omitted instance.** With ties to the lowest index, `omega` uses
  `3, 7, 15, ..., 2^(n+1) - 1` nodes on `A_1, ..., A_n`. It cuts every `N`
  coordinate before the `R` coordinate. This was checked for `n = 2, 3, 4`
  with `r0 = 1/4 - 1/(5n)` and for `n = 3, 4, 6` with the author's `r0`.
- **What the note reports.** Section 6 reports only `A_1` and `A_2`.
- **Not a tie artefact** (`omega_tiefree.py`).
  - Move the `R` coordinate's root minimizer to `1/2 + 1/50`, keeping its
    root value. Take its two outer lines through the new split point, so
    that cutting it there still leaves both children valid.
  - Then `omega` strictly prefers every `N` coordinate, and uses exactly
    `2^(n+1) - 1` nodes on **every** labelling, for `n = 2, ..., 5`, while
    `N_opt = 2`. Here `OPT_min` has 2 leaves.
- **Consequences.**
  - If Conjecture 1 holds for `omega`, its constant satisfies
    `C_n >= (2^(n+1) - 1)/3`.
  - Conjecture S1's constant satisfies `C_n >= 2^(n-1)` in leaves.
  - Section 7.2 states only `C_2 >= 2`.

### 4.4 The ambiguity iterates (answer to the open question)

The note says: "After a wrong cut the children remain ambiguous among the
other `A_i`, but a second wrong cut can make a child valid, so the argument
does not simply iterate." Restricting attention to *corner nodes* makes the
argument iterate.

**Proposition C+ (review).** Take the same instances, with `r0` as in
Section 4.2, and any `n >= 2`.

- (a) Every deterministic I1 rule has `T >= 2 G(n) + 1` on some `A_i`. Here
  `G(n) >= ceil((2^(n+1) - n - 2)/n)`. Exactly, `G(2), ..., G(5) = 3, 5, 9, 15`.
- (b) Every randomized rule has `E[T] >= 2(2^(n+1) - n - 2)/n + 1` on some
  `A_i`.

*Proof sketch.*

1. **Definitions.** Call a node a *corner node* if each of its intervals
   contains `0` or `1`. Let `S(v)` be the set of coordinates cut on the path
   to `v`.
2. **Identical data.** For every `i` not in `S(v)`, the I1 data at `v` are
   identical in all such `A_i`: the box, value, minimizer, germ, `f` near the
   box corners and the incumbent. Uncut coordinates are `[0,1]`, where `R`
   and `N` share the minimizer `1/2` and agree near it and differ by a
   constant near `0` and `1`. Cut coordinates carry `N`.
3. **Invalidity.** `v` is invalid in `A_i`. Each cut coordinate has
   `F_N <= m_N(0 or 1) = -c + eps/(2(n-1))`, each uncut one has `-c`, so the
   value is at most `-nc + eps(1 + |S|/(2(n-1))) < 0`.
4. **One reference tree.** A deterministic rule therefore follows a single
   reference tree on all corner nodes. Every such node with `|S| < n` is
   internal in `A_i` for every free `i`.
5. **Growth of the tree.** Cutting an uncut coordinate gives two corner
   children. Re-cutting a coordinate gives one corner child, and it may give
   one valid non-corner child; this is the case the note had in mind. So
   there are at least `2^d` corner nodes with `|S| = d`, for each
   `d = 0, ..., n-1`.
6. **Counting.** With `N_i` the number of corner nodes free of `i`,
   `T(A_i) >= 2 N_i + 1` and
   `sum_i N_i >= sum_{d=0}^{n-1} 2^d (n - d) = 2^(n+1) - n - 2`. Averaging
   gives (b), by Yao's principle.
7. **Exact minimax.** `G(n)` is the exact min-max of `N_i` over reference
   trees. A Pareto dynamic program computes it (`thmC_iter.py`). □

Numbers (`thmC_iter.log`):

| `n` | deterministic ratio `>=` | randomized ratio `>=` | the note's bounds |
|---|---|---|---|
| 2 | 7/3 | 5/3 | 7/3, 5/3 |
| 3 | 11/3 | 25/9 | 7/3, 17/9 |
| 4 | 19/3 | 14/3 | 7/3, 2 |
| 5 | 31/3 | 119/15 | 7/3, 31/15 |
| 8 | 42.3 (averaging) | 42.2 | 7/3, 13/6 |

**Checks.**

- **Corner nodes.** Random corner nodes for `n = 2, 3, 4`, including the
  author's `r0`, always had identical data and were invalid.
- **Explicit rules.** A "balanced" rule realizes the reference tree of
  `G(n)`. Run exactly, it attains `T = 2 G(n) + 1`: `[3, 11, 11]` for
  `n = 3` and `[3, 19, 15, 19]` for `n = 4`. So on this family the minimax is
  exactly `(2 G(n) + 1)/3` for `n <= 4`.
- **Caveat.** The argument uses the note's coordinate-wise minimizer
  selection. At corner nodes the `N` coordinate's minimizer set can be a
  flat segment. A solver that broke such ties using `f` far from the
  minimizer could in principle leak `i`. The note's own statement at the root
  does not need this, because the root minimizer is unique.

**Consequences for the note.**

- Section 6 "Open" and Section 9, question 2: the lower bound grows, at
  least like `2^(n+2)/(3n)`, on the very same instances. The interval
  `[7/3, C_n]` should become `[(2 G(n) + 1)/3, C_n]`.
- Every I1 rule that is `C_n`-competitive on these non-analytic classes,
  `omega` or any other, needs `C_n` exponential in `n`.
- This strengthening is the review's, not the note's.

## 5. Proposition D (Section 3.3)

**(a) Correct.**

- **`q`.** The closed forms and the certificate `[0, sqrt(8b)]`,
  `[3^j s, 3^(j+1) s]` are correct.
  - For the lower bound, at `u = 7l` one gets `F = -u^2/49`, which is at most
    the stated `-u^2/56`.
  - The ratio argument gives `N_q >= 1 + log_7(1/sqrt(56 b))`.
- **`g`.** The upper bound (cells with `F = 0`, plus `[0, s_K]`) is correct.
  - The three-point bound
    `F <= -(s_k - s_(k+1))(s_(k-1) - s_k) = -2^(-2k-1)` is correct.
  - The count `N_g(b) >= (K_b + 2)/2` is correct. Shared endpoints only
    increase the incidence sum.
- **Exact values** (`propD_check.py`). `N_q` for the **exact** `q`, with a
  certified bracket, and `N_g` for `b = 1e-2, ..., 1e-10` both lie within
  the stated bounds.

**(b) Correct.** `M(c) = |c|^2/2`, and clipping is fine because
`q_(B ∩ X0) <= q_B` on `B ∩ X0`.

- The construction was built exactly for `eps = 1e-2, ..., 1e-12`.
- Every box was valid, the areas summed to 1, and the count **equals** the
  bound `1 + 3 ceil((1/2) log2(1/eps))`: 13, 16, 22, ..., 61.

**(c) Correct.** I checked each step:

- Claim 1: `F_g(I) >= 2^(-2j-4) > 0` forces `I` into a single cell `C_k`
  with `4^(-k-2) >= 4^(-j-2)`.
- Claim 2: the line argument, counted on `K - j + 1` points.
- Claim 3: a box is counted at most twice, on consecutive lines.
- Exact random tests of the three-point bound (3,000 intervals) and of
  Claim 1 (627 valid boxes) found no violations.
- The resulting lower bounds are 4, 7, 10, 14, 20 at `eps = 1e-3, ..., 1e-7`.
  They grow like `K^2/8`.

**(d) Needs a qualifier.** "No function of the 1D certificate sizes
determines `N_opt` up to constant factors" is literally too strong.

- `N_q` and `N_g` are different functions. For example, at `b = 1e-4`,
  `N_q = 4` and `N_g = 7`, and asymptotically `N_g ≈ 1.6 N_q`. A contrived
  function could tell them apart.
- The proposition proves the statement for every formula that is
  insensitive to bounded multiplicative changes of the `N_i`. This includes
  the product and slice forms and anything built from orders of growth.
- State it that way.

**Table of Section 3.3 (minor).**

- **`q` column.** It is computed for a knot interpolant of `q`, which lies
  above `t^2`, not for `q` itself. The exact `N_q(1e-4)` is 4, not 3, and
  `omega` on exact `q ⊕ q` gives 7 leaves at `1e-3`, not 8.
- **`g ⊕ g` grid optima.** They are not optimal. Exact product certificates
  have 49 boxes at `1e-4` (note: 50) and 144 at `1e-7` (note: 145)
  (`propD_extra.py`).
- **"`omega` matches it exactly".** This holds only for the author's tie rule
  (Section 7 below).

## 6. Lemma 3.2 (budget halving): correct

- **Short pieces.** They are valid at `b/2`.
- **Middle piece.** It gains `min(a_K(p1), a_K(p2)) = b/2` by
  Lemma 2.2(c).
- **End pieces.** They have length at most `b/|K|`. Then
  `b^2/(4|K|^2) <= b/2` because `b < |K|^2/2`.
- **Checks.** Exact greedy on 1,500 random instances gave a largest ratio of
  `N(b/2)/N(b) = 2`. A 400-cap sawtooth gave at most 1.6, and dyadic caps at
  most 1.2. So the factor 3 is not attained in these tests; it is not
  claimed to be tight.

## 7. Numerical claims outside the numbered results

**Section 5 and Summary item 3 (the drift family).** The same instance
reproduces the note's `omega` counts and slice values exactly (`sharp(1/3)`
× the knot interpolant of `(t - 29/70)^2`). The note's grid optima, however,
come from grids of about 25 × 50 points.

My DP uses grids built for strip structure, with sizes up to 41 × 202:

- `x = 1/3 ± d`, with `d` geometric of ratio 4 starting from `eps/4`;
- `z` = the greedy breakpoints at each strip budget `eps + m_x(1/3 ± d)`,
  plus `omega`'s cuts.

Every returned certificate was verified exactly (`sharpquad_grid.py`).

| `eps` | 1e-6 | 1e-7 | 1e-8 | 1e-9 | 1e-10 | 1e-11 |
|---|---|---|---|---|---|---|
| grid optimum, note | 15 | 18 | 20 | 24 | 27 | 30 |
| grid optimum, here (exactly verified) | 14 | 16 | 18 | 20 | 22 | 23 |
| `omega` leaves (both) | 24 | 28 | 32 | 36 | 38 | 44 |
| `omega`/grid, here | 1.71 | 1.75 | 1.78 | 1.80 | 1.73 | **1.91** |

- **The "correction" of the n-dim note is itself wrong.** The n-dim note's
  1.91 at `1e-11` was not a float artefact. A lower bound of 1.91 holds on
  this note's own instance.
- **Wrong statements.** "Levels off near 1.5" and "exact recomputation gives
  about 1.5" are both wrong.
- **What is right.** Boundedness itself follows from Theorem B.
- **Growth rates.** The grid optimum grows by about 2 per decade and `omega`
  by about 4, which is consistent with an asymptotic ratio near 2.
- **Section 7.1.** The row "sharp × quadratic, `OPT_min`/grid 1.25–1.60"
  should read up to 1.91, since `omega = OPT_min` on this family.
- **Slice column.** "`omega`/slice ... at most 2.9" is wrong. It is
  `24/8 = 3.0` at `1e-6` and `36/12 = 3.0` at `1e-9` (`slice_check.py`).

**Section 7.1 and Section 3.3: the tie rule.** Section 1.1 says the
computations take "among the minimizers, the one with the largest `w`, then
the leftmost".

- **What the code does.** The author's `sepexact.Coord.node` compares only
  knots and endpoints.
- **When this matters.** The two differ when `phi_J` is constant on a
  segment. This happens on every cell of the dyadic caps and of the "caps"
  family, where `phi = 0` on the whole cell. The stated rule, and an
  interior-point solver's centre of the optimal face, both pick the cell
  midpoint, with `w > 0`. `omega` then spends a useless split there, which
  doubles the subtree below it.
- **Results** (`selection_check.py`):

  | Family | `eps` | `omega`, code's rule | `omega`, stated rule | `OPT_min`, stated rule (centre rule for dyadic caps) |
  |---|---|---|---|---|
  | dyadic caps × dyadic caps | 1e-3 … 1e-10 | 27, 50, 81, 102, 145, 196, 227, 290 | 41, 84, 143, 181, 264, 363, 421, 544 (ratio 1.52 → 1.88) | 27, 50, 81, 102 (to 1e-6) |
  | caps(k/7) × quadratic | 1e-3 … 1e-6 | 32, 46, 60, 81 (`= OPT_min`) | 48, 76, 104, 146 | 36, 52, 68, 92 (`omega/OPT_min` 1.33 → 1.59) |

- **What to change.** "`omega` is within 5% of `OPT_min` on every family
  tested" and "`omega` matches the grid optimum" for dyadic caps hold for the
  code's tie rule (knots and endpoints only, the same as leftmost or
  rightmost here), not for the rule the note states. The note should name
  the rule actually used.
- **Why the note should say this.** The loss is a factor below about 2 in
  these runs. I expect it to stay below 2, since each wasted split doubles
  one subtree and cannot repeat along a path; this is a heuristic, not
  checked. Still, `omega`'s behaviour on flat minimizer sets is a genuine
  modelling choice, and interior-point solvers make the unfavourable one.

**Summary item 6 wording.** "Within a factor 1.9 of the exact grid optimum":
the grid optimum is an upper bound on `N_guill`. Such ratios are lower
bounds on the true loss, not bounds on it.

## 8. Novelty notes

- **Elementary results.** Lemma 2.1, Theorem 1', Proposition 3.1 and
  Lemma 3.2 are routine consequences of the main note.
- **Lemma T and Theorem A.** New in this workstream. They reuse the
  "three facts" mechanism of the main note's Lemma 2, adding a clean
  threshold device (`w >= tau`).
- **Theorem B.** A modest but genuine special case.
- **Theorem C.** Indistinguishable instances that differ only in which
  coordinate matters are a standard adversary technique from decision-tree
  and online lower bounds. Its use for node-local spatial branching looks
  new; I did not search the literature. The corner-node iteration (Section
  4.4) shows that the mechanism is much stronger than the note states. It
  forces the competitive constant of every I1 rule on these non-analytic
  classes to grow exponentially in `n`.
- **Proposition D.** It uses standard ingredients: a Whitney-type
  certificate for `q ⊕ q`, and caps at every dyadic scale. The conclusion is
  useful for the program. I did no literature search for rectangle-partition
  analogues.

## 9. Corrections requested (in order of weight)

1. **Theorem C for `n >= 3`.** Give the general `r0` condition,
   `eps(2n-1)/(2n(n-1)) < 1/4 - r0 < (1 + 2 eps)/(4n)`, for example
   `r0 = 1/4 - 1/(5n)`, and the general-`n` argument. Replace the script's
   `r0`, which fails for `n >= 12`.
2. **`omega` on Theorem C's instances.** Replace "`omega` itself attains
   `7/3`" by the correct count, `2^(n+1) - 1` nodes on `A_n`, tie-free
   variant included. Update Section 7.2 (`C_n >= 2^(n-1)` in S1).
3. **The open question.** Replace the "Open" remark of Section 6 and
   question 2 of Section 9 by Proposition C+, or cite this review.
4. **Section 5 and Summary item 3.** Withdraw "levels off near 1.5" and
   "gives 1.47". A finer, exactly verified grid gives 1.91 at `1e-11`.
5. **Answers (2).** Remove "`deficit` is competitive within a phase
   (Theorem A)"; it is false (Section 3). Qualify "all but one coordinate
   sharp" (2D for both rules; sketch for `omega` only).
6. **Section 1.1 and Section 7.1.** State the tie rule actually used (knots
   and endpoints only). Report, or at least flag, that the stated rule gives
   `omega/OPT_min` up to 1.59 on caps × quadratic.
7. **Minor.**
   - Corollary A' at `n_P = 1`, and the case `tau = 0`.
   - Proposition D(d): add the qualifier.
   - Table of Section 3.3: the `q` column is the interpolant, not `q`; the
     `g ⊕ g` grid optima are not optimal.
   - "`omega`/slice at most 2.9" should be 3.0.
   - "`2^(n-1)` sides" should be `3^(n-1)` states.
   - Summary item 6 wording.

## Commands run

All commands were run from `research-20260928b/reviews/separable-omega/`, with
single-threaded Python 3 and exact `fractions` (`sympy` 1.14 for Part 1 of
`thmC_check.py`). The DP library was built with
`gcc -O2 -shared -fPIC -o libgdp8.so gdp8.c` (`sharpquad_grid.py` builds it
if it is missing). The largest DP table (41 × 202 grid, `uint8`) took about
69 MB. These are targeted checks only: no project-wide checks were run, and CI
was not inspected.

| Command | Result (log) |
|---|---|
| `python3 thmC_check.py` | symbolic conditions; exact items for `n = 2..40` with `r0 = 1/4 - 1/(5n)`, all hold; the author's `r0` fails at `n = 12, 13, 14`; information model; rule counts (`thmC_check.log`) |
| `python3 thmC_iter.py` | `G(n) = 3, 5, 9, 15`; corner-node checks with 0 violations; `omega` `[3, 7, ..., 2^(n+1)-1]`; balanced rule attains `2G+1` (`thmC_iter.log`) |
| `python3 omega_tiefree.py` | `2^(n+1) - 1` nodes on every labelling, `n = 2..5`; `N_opt = 2` (`omega_tiefree.log`) |
| `python3 lemmaT_check.py 1500 11` | Lemma T, Theorem A, 2D phases: all assertions pass; `n_P = 1` example (`lemmaT_check.log`; Part 4 rerun after fixing the example instance) |
| `python3 thmB_review.py 1200 5` | Theorem B: all assertions pass; `n = 3` sketch data; `deficit` phase counterexample (`thmB_review.log`) |
| `python3 propD_check.py 1500 3`, `python3 propD_extra.py` | Proposition D (a)–(c), exact `q ⊕ q` certificate, `omega` counts, Lemma 3.2; product certificates for `g ⊕ g` (`propD_check.log`, `propD_extra.log`) |
| `python3 selection_check.py` | tie-rule dependence on `g ⊕ g` and caps × quadratic (`selection_check.log`) |
| `python3 sharpquad_grid.py` | finer exact-verified grid optima for the drift family (`sharpquad_grid.log`) |
| `python3 slice_check.py` | slice values and `omega`/slice for the drift table (`slice_check.log`) |

## Not checked

- **Section 7 experiments.** The hill-climbing searches (`search*.py`,
  `classify.py`), the phase-accounting statistics (`exp4`, `exp6`), and the
  anisotropic `deficit` drift (`exp3`). The `chainlp3` LP was not rerun; my
  own adversarial search replaces it for Lemma T.
- **Section 7.3.** The edge-point sketch, the corner discussion and the
  convex-class heuristic. These are labelled as sketches and heuristics.
- **The `n - 1` sharp sketch.** Its full summation was not written out;
  there is only numerical support for `n = 3`.
- **Published BSP bounds.** (R1) is taken from the recheck, which read
  abstracts only.
- **Smoothing and analytic scope.** The `C^inf` smoothing and the
  analytic-class caveat of Theorem C are the same as Theorem 3's and were not
  re-examined. Proposition C+ inherits the same scope: non-analytic,
  piecewise-quadratic classes.
- **Literature.** No literature search was done for the novelty notes.
