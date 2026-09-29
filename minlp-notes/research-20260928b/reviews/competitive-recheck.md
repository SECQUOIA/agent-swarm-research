# Recheck of the revised competitive-branching note and its n-dimensional companion

Date: 2026-09-29. Rechecked documents:

- [`../bb-complexity/branching-competitiveness/competitive-branching.md`](../bb-complexity/branching-competitiveness/competitive-branching.md)
  (the "main note"), as revised after [the first review](competitive-review.md);
- [`../bb-complexity/branching-competitiveness/n-dimensional.md`](../bb-complexity/branching-competitiveness/n-dimensional.md)
  (the "n-dim note").

Scripts, logs and the fetched SCIP sources are in
[`competitive-recheck/`](competitive-recheck/). I had not seen this material
before. I did not edit the notes or commit anything. All scripts are new and
written from the notes' definitions: `pl1d.py` is a new exact 1D engine, and
the SCIP rule is transcribed from the SCIP v10.0.2 source, not from the
author's script. I read the author's `scip_rule_check.py` and `multi_lb.py`
only to compare conventions (tie-breaking, certificate variant).

## Verdict

All four items hold. Every revised statement I was asked to check is correct.
The problems are small: one numerical misstatement, three wording or scope
points, and one place where the literature gives a stronger result than the
n-dim note uses.

| Item | Verdict | Main evidence |
|---|---|---|
| (1) Proposition 4' (SCIP 10 default on `f = 2 alpha abs(y - 3/238)`) | **Correct** | The rule matches `SCIPbranchGetBranchingPoint` in SCIP v10.0.2. The pull uses **global** bounds and the clamp uses **local** bounds. The exact full-tree simulation reproduces every step: `45/119`, clamp to `9/119`, `a` at `1/6`, then `mu <= 27/476 < 1/10`, the clamp binds at every level, and widths shrink by 5. `T = 2K + 1` exactly, against `T_opt = 3` |
| Proposition 4' remark on the no-clamp variant | **Numbers right, one description wrong** | `T = 11, 13, 15, 17, 19` reproduces, but that is about **4** more nodes per doubling of `log(1/eps)`, not "about 2" |
| (2) Corollary 1 corrected, `T <= 8 N_opt(eps - 2 delta) - 9`; part (b) | **Correct** | I rederived the proof. There were 77,172 exact worst-case `delta`-minimizer runs, with split points that include non-knot level crossings, and 0 violations. Edge case: the formula reads `-1` when `N_opt(eps - 2 delta) = 1` |
| (2) Proposition 2 (`N_opt = 2` implies `T <= 5`) | **Correct** | Proof checked, and both identities checked symbolically. On 15,725 exact `N_opt = 2` instances, with worst-case tie-breaking including flat segments, the maximum was `T = 5`, attained 1,311 times. `T = 5` is also attained on Theorem 3's instance A |
| (3) Theorem 3 scope (non-analytic classes; finite jets) | **Correct** | The logic holds. Exact recheck: the agreement intervals are exactly `[0, 3/13000]`, `[1/60, 27/40]` and `[9997/10000, 1]`, so all jets at `0`, `1` and `3/5` agree. Two small scope gaps remain (Problems 3 and 4) |
| (4a) Theorem N3 (`multi` needs `Omega(eps^-1/2 log(1/eps))`; certificate of about `1.21 eps^-1/2`) | **Correct** | Proof checked step by step. An independent exact count reproduces every tree size in the table. The proof's node family is confirmed internal. The certificate is validated exactly box by box |
| (4b) Guillotine overhead: `(2 N_opt - 1)^n` and `C_n log(1/eps)` | **Correct** | Both proofs checked. The 2D "imported" bound can be sharpened to `N_guill <= 2 N_opt - 1` (Berman–DasGupta–Muthukrishnan), and `n >= 3` improves to `O(N_opt^((n+1)/3))` (Hershberger–Suri–Tóth). Both come from abstracts |
| (4c) Lemma N6 (separable bracket) | **Correct** | Proof checked. On 1,629 exact grid instances, 0 violations of `slice <= G_grid <= product`. The lower bound does not depend on how `eps` is split |

## 1. Proposition 4' (SCIP 10's default branching point)

### 1.1 The rule against the SCIP 10.0.2 source

Sources fetched from GitHub tag `v10.0.2` are in `competitive-recheck/scip-src/`.
The installed pyscipopt reports SCIP 10.0 with defaults `branching/midpull = 0.75`,
`branching/midpullreldomtrig = 0.5`, `branching/clamp = 0.2` and
`constraints/nonlinear/branching/external = FALSE`.

- **Call site.** `cons_nonlinear.c` line 7478 branches with
  `SCIPbranchVarVal(..., SCIPgetBranchingPoint(scip, var, SCIP_INVALID), ...)`.
  With no suggestion, `SCIPbranchGetBranchingPoint` (`branch.c` lines 2393–2519)
  does the following:
  1. It takes the LP value, via `SCIPvarGetSol(var, SCIPtreeHasCurrentNodeLP(tree))`.
  2. If the node LP was solved, `midpull > 0` and both local bounds are
     finite, it sets `reldomainwidth = (ub - lb)/(gub - glb)`. Here `lb, ub`
     are the local bounds (`SCIPvarGetLbLocal`) and `glb, gub` are the global
     bounds (`SCIPvarGetLbGlobal`).
  3. If `reldomainwidth < midpullreldomtrig`, it multiplies `midpull` by it.
  4. It sets `bp = midpull (lb+ub)/2 + (1 - midpull) x` and projects `bp`
     onto `[lb, ub]`.
  5. It clamps `bp` to `[(1-c) lb + c ub, c lb + (1-c) ub]` with the **local**
     bounds, and additionally keeps it at least `1.01 epsilon max(|lb|,|ub|,1)`
     from each bound. For relative width `<= 2.02 epsilon` it uses the
     midpoint instead.
- **Match with the note.** Section 1.5 and the statement of Proposition 4'
  match steps 1–5 exactly in the model, where the global box is the root
  `[0,1]`.
- **Original bounds.** SCIP does not use the original (pre-presolve) bounds
  here.
- **Wording.** "Global width" (Section 1.5) is the right term. "Root width"
  (Section 1.5 bullet 3, Proposition 4 table) and "depth-dependent"
  (Sections 1.5, 5.2, 8.2, 10) are loose: the rule depends on the relative
  width of the variable's local domain, not on depth.

**Does the claim depend on how the relative width is measured?**

- **Inside the model it does not.** The model has no presolve and no bound
  tightening, so local-root, global and original bounds all equal `[0, 1]`.
- **The specific kink uses the reference width `W = 1` at two nodes only.**
  - `N_0`: `r = 1`, so `mu = 3/4`.
  - `N_1`: `r = 45/119`, so `mu = 135/476`.
  - With another fixed `W`, the kink `3/238` would have to be re-chosen.
- **From `N_2` on, the proof needs only `mu < 1/10`.** That means
  `w/W < 2/15`, which eventually holds for any **fixed** reference width.
  So the `log(1/eps)` mechanism, a persistent clamp with a vanishing pull,
  survives for global or original bounds alike.
- **A parent-relative width would break it.** Relative to the parent,
  `r = 1/5` after each clamped split, so `mu = 0.15` and the clamp would stop
  binding at position `1/6`. SCIP does not do this; the source confirms the
  global reference.

### 1.2 Exact trajectory (`scip_prop4prime.py`, `scip_prop4prime.log`)

The script assumes nothing from the proof. At every node it minimizes the
convex piecewise-quadratic `phi_B` exactly over its candidates: the ends, the
kink, and the stationary points of both pieces. It simulates the whole tree,
and it asserts that every invalid node contains the kink and has the kink as
its unique minimizer. The author's script instead hard-codes both facts
(proof step 1) and follows only the chain.

| node | box | position of `a` | `mu` | unclamped point | split |
|---|---|---|---|---|---|
| `N_0` | `[0, 1]` | `3/238` | `3/4` | `45/119` | `45/119` (clamp inactive) |
| `N_1` | `[0, 45/119]` | `1/30` | `135/476` | `507/8092 ≈ 0.06265 = (3/238)(1 + 14 mu)` | `9/119` (clamped) |
| `N_2` | `[0, 9/119]` | `1/6` | `27/476` | `≈ 0.01404` | `9/595` (clamped) |
| `N_3` | `[0, 9/595]` | `5/6` | `27/2380` | `≈ 0.01255` | `36/2975` (clamped) |
| `N_4` | `[36/2975, 9/595]` | `1/6` | `27/11900` | | clamped |

Assertions that pass for every chain node down to `eps = 1e-16`:

- positions alternate `1/6` and `5/6` from `N_2`;
- the width is exactly `(9/119) 5^-(k-2)`;
- `mu <= 27/476 < 1/10`;
- the unclamped relative position is `p + mu(1/2 - p)`, and the clamp binds.

Node counts over full trees, for `alpha = 1` and `alpha = 7/3` (with `eps`
scaled by `alpha`):

| `eps/alpha` | 1e-4 | 1e-6 | 1e-8 | 1e-12 | 1e-16 | 1e-24 | 1e-32 |
|---|---|---|---|---|---|---|---|
| `T_SCIP` | 7 | 11 | 13 | 19 | 25 | 35 | 47 |
| `2K + 1` (statement) | 7 | 11 | 13 | 19 | 25 | 35 | 47 |
| `T` without clamp | 7 | 9 | 11 | 13 | 15 | 17 | 19 |
| `T_min` | 3 | 3 | 3 | 3 | 3 | 3 | 3 |

- **The bound is exact.** `T_SCIP = 2K + 1`, because every off-chain child is
  pruned.
- **`N_opt = 2`.** `[0, a]` and `[a, 1]` are valid and the root is not.
- **The `eps` range.** The condition `eps < alpha (5/36)(9/119)^2 ≈ 7.94e-4 alpha`
  makes `N_0` and `N_1` invalid: their products `0.01245` and `0.00461`
  exceed `7.94e-4`.
- **Ratio.** `T_SCIP/T_opt = (2K + 1)/3`, which grows like
  `(2/3) log_25(1/eps)`.

### 1.3 Problems found in Section 5.2

- **No-clamp growth (numerical slip).** The remark says `T = 11, 13, 15, 17, 19`
  at `eps = 1e-8, 1e-12, 1e-16, 1e-24, 1e-32` is "about 2 more nodes per
  doubling of `log(1/eps)`".
  - Across actual doublings the increase is **4**:
    `1e-8 → 1e-16` gives `11 → 15`, `1e-12 → 1e-24` gives `13 → 17`, and
    `1e-16 → 1e-32` gives `15 → 19`.
  - Further out, `1e-32 → 1e-64` gives `19 → 21`.
  - The consecutive +2 steps in the list are for ratios 1.5 and 1.33 of
    `log(1/eps)`, not for doublings.
  - The conclusion, much slower growth consistent with
    `O(log log(1/eps))`, is unaffected. The +4 fits the note's own heuristic:
    the width squares every two levels, which adds 2 internal nodes per
    doubling.
- **Floating-point guards (missing caveat).** SCIP's absolute guard
  `1.01e-9 max(|lb|,|ub|,1)` overtakes the 0.2 clamp once `w < 5.05e-9`.
  - The first such chain node is `N_13` (`w ≈ 1.55e-9`). It is invalid only
    when `eps < 3.3e-19 alpha`.
  - So the proposition describes SCIP's floating-point rule exactly for
    `eps >= 3.3e-19 alpha`. The verification rows at `eps = 1e-24` and
    `1e-32` describe only the exact formula.
  - Rounding does not matter in that range: the clamp binds with a margin of
    at least `1/30 - mu/3 > 0.014` in relative position, and errors grow by
    a factor 5 per level.
  - The note's scope remark ("SCIP's branching-point formula inside the
    exact-gap 1D model") covers this in spirit. The guard threshold is worth
    one sentence.

## 2. Corollary 1 and Proposition 2

### 2.1 Corollary 1

I redid Lemma 2 with `delta`-minimizers against a certificate at tolerance
`eps' = eps - 2 delta`, so that `m - 2 delta >= alpha q_J` on each piece.

1. **Fact 1.** `m(y1) - alpha q_{B1}(y1) <= m(y2) - alpha q_{B1}(y2) + delta`.
2. **Fact 2.** `B2` is invalid, so `min phi_{B2} < 0` and
   `phi_{B2}(y2) < delta`. With `q_{B2}(y2) <= (t2+d)(t1-t2)` this gives
   `m(y2) < alpha (t2+d)(t1-t2) + delta`.
3. **Fact 3.** `m(y1) - 2 delta >= alpha t1(lambda - t1)`.
4. **Chain.** Combining the three facts gives
   `alpha t1(lambda - t1) + 2 delta < alpha (t1-t2)(e-t1) + 2 delta`, hence
   `lambda < e`.
5. **The rest of the count is unchanged.**
   - Lemma 1(i): split points are interior by hypothesis.
   - Lemma 1(ii): split points are distinct.
   - Lemma 1(iii): an interval valid at `eps'` is valid at `eps`.
   - Lemma 1(iv) and the class count need no change.

So (a) holds. For (b), fact 2 has no `delta` because `phi_{B2}(y2) < 0`, and
the certificate at `eps - delta` absorbs the single `delta` of fact 1. So
(b) holds.

**Edge case (wording).** Theorem 1 separates `N_opt = 1`; Corollary 1 does
not. If `N_opt(eps - 2 delta) = 1`, the root is valid and `T = 1`, but the
formula gives `-1`. Add "`N_opt(eps - 2 delta) >= 2`, and `T = 1` otherwise",
and the same for (b).

**Exact search** (`cor1_prop2_check.py`, seeds 11 and 12, 20,000 draws each).

- **Instances.** 38,586 instances with `N_opt >= 2`, from four families:
  convex `H`, non-convex `H`, dyadic knots with small-integer values (many
  exact ties), and chord-rigid instances.
- **Adversary.** The split point at every node maximizes the tree over:
  - all breakpoints in `{phi <= min + delta}`;
  - **both ends of every sublevel interval**. These are level crossings,
    generally not knots, so this set differs from the first review's
    knot-only candidates.
- **Values of `delta/eps`.** `1/4` and `9/20`, both below `1/2`.
- **Results.** Over 77,172 `delta`-runs:
  - 0 violations of (a);
  - 0 violations of (b), with split points restricted to `phi < 0`;
  - 0 violations of the open stronger form `8 N_opt(eps - delta) - 9` for
    unrestricted `delta`-minimizers, which the note leaves open;
  - the stronger bound was never tight.
- **Caveat.** The adversary's real choice set is a continuum, so this is
  evidence for the open form, not a proof.

### 2.2 Proposition 2

- **Proof.** I checked every case:
  - root at `s`;
  - `B2` valid;
  - `y2 = s`;
  - `y2 in int J_2`: Lemma 2 applied to the root and `B2` would force
    `U > U`;
  - `y2 in int J_1`: steps 3–6.
- **Step 5 sub-case.** When `(U - y1) - (y2 - L) <= 0`, the right side is
  `<= 0 < (y1 - s)(U - y1) <= m(y1)`. That is a contradiction, as stated.
- **Identities.** Both identities of steps 4 and 5, and the two Lemma 2
  identities, expand to zero in sympy.
- **Exact search.** In the same runs, 15,725 instances have `N_opt = 2`.
  - The worst case over all tie choices, including midpoints of flat minimal
    segments, is `T = 5`. It is attained 1,311 times and never exceeded.
  - Across all instances the largest `T/(2 N_opt - 1)` found was `11/5`,
    reached by a random instance. This matches the lower end of the note's
    `[11/5, 4)`.
- **Cross-checks** (`thm3_scope_check.py`).
  - My engine reproduces the review's `11/5` instance: `N_opt = 3`, with
    breakpoints `12209/30000` and `3391/5582`, and `T = 11` also under
    worst-case ties.
  - `R_min` has `T = 5` on Theorem 3's instance A (splits `3/5`, then
    `1/140`). So "exactly `5/3`" is attained.

**Scope of Proposition 2's last sentence.** "`R_min` is therefore optimal
among I1 rules on such instances" relies on Theorem 3. It therefore holds for
the piecewise-quadratic (non-analytic) `N_opt = 2` class, not for analytic
instances, where I1 rules can reach ratio 1. The sentence should carry the
same qualifier as Theorem 3. The `5/3` ratio of `R_min` itself needs no
qualifier.

## 3. Theorem 3's restated scope

The restated scope is correct.

- **Analytic `f`.** For real-analytic `f`, the values on any open subinterval
  determine `f` on the box, by the identity theorem. So I1 carries the same
  information as I_inf, and Proposition 0 gives ratio 1. The statement that
  this is information-theoretic only is also right: the greedy split is a
  global problem.
- **Finite jets.** A jet of order at least the degree determines a
  polynomial. So any lower bound for polynomial classes must use jets of
  lower order, and different instances. Marking this open is correct.
- **Restriction to finite local data.** Restricting to finite local data
  only weakens the rule, so the lower bound holds a fortiori.
- **Exact check** (`thm3_scope_check.py`). The instances satisfy all the
  needed facts:
  - `min m = eps` at exactly `{0, 1}`;
  - root value `-37/300` with the unique minimizer `3/5`;
  - `N_opt = 2`, with unique breakpoints `1/3` (A) and `3/5` (B);
  - `[0, b]` valid iff `b <= s*`, probed exactly;
  - maximal agreement intervals exactly `[0, 3/13000]`, `[1/60, 27/40]` and
    `[9997/10000, 1]`.

  So every one-sided jet at `0` and `1`, and every jet at `3/5`, agrees.
- **The `C^inf` remark.** It remains argued, not computed, as the note says.
  I checked the argument: convexity plus a symmetric mollifier gives
  `H_zeta >= H`, with equality away from the kinks.
  - The chord segments survive, so the breakpoints stay exactly `1/3` and
    `3/5`.
  - `m_zeta(0) = m_zeta(1) = eps` as long as `zeta` is below the distance
    from the ends to the nearest kink. That distance is `30 eps/13` in B, so
    `zeta < eps` suffices.
  - The root minimizer stays exactly `3/5` in both instances: `H - y` has
    slopes `-1/5` and `+1/5` there.

**Precision point (new).** The I1 table says the rule sees "`f` ... on a
neighbourhood of `y_B`" without fixing the neighbourhood.

- Read literally, the whole open box is a neighbourhood of `y_B`. Then I1
  equals I_inf for **every** `f`, analytic or not, and Theorem 3 would be
  false.
- The theorem itself is precise, because it names the sets the rule may see.
- I1 should say "the germ of `f` at `y_B`", or "on a neighbourhood of
  prescribed size". With that reading, the analytic-class remark and
  Theorem 3 are both exactly right.

## 4. The n-dimensional note

### 4.1 Theorem N3

**Proof check.** Every step holds.

- **Closed forms.** The stationary point `(l+u)/4` lies in `[l, u]` iff
  `u >= 3l` and is interior iff `u > 3l`. Otherwise the minimum is `l^2` at
  `x = l`. `F_z = -w^2/4`.
- **Product structure.** It follows by induction on depth. All `2^D` dyadic
  `z`-intervals appear with every `x`-interval, and validity depends on the
  `z`-interval only through its width.
- **Spine and interior chain.** `[0, 4^-k]` splits at `4^-(k+1)`. Then
  `r_j` increases to `4l/3 < 3l <= 3 r_j`, so the pieces `L_j` are never
  split in `x` again, and `L_j` appears at depth `k + 1 + j`.
- **Invalidity at `D <= 2k`.** It needs `eps < (5/36) 16^-k`.
  - `K = floor(log_16(5/(36 eps)))` allows equality in principle.
  - The bound `F_x(L_j) = eps + r_{j-1}^2 < eps + 16^-k/9` is strict,
    because `r_{j-1} < 4l/3`. So the step holds. The note writes `<=`; this
    is a trivial nit.
- **Count and constants.** Each `k` contributes `(k - 1) 4^k` nodes. The
  constants check: `4^K > 0.0932 eps^-1/2`, `0.186 = 2 × 0.0932`, and
  `K >= (1/4) log2(1/eps) - 2`.
- **Part (a).** Pieces of `z`-width `sqrt(2 eps)` in `S_0` (where
  `F_x = eps/2`), and of width `2l` in `S_k`. The construction actually
  gives `+2` rather than `+3`; the stated bound is valid.
  `1/sqrt 2 + 1/2 = 1.2071 <= 1.21`.
- **Counting convention.** `multi`'s 4-way splits are counted as one parent
  and four children, with `T >= 2 (internal) + 1`. Emulating them with
  binary splits would only add nodes, so the lower bound is conservative.

**Exact recount** (`multi_n3_check.py`, `multi_n3_check.log`). Every rule's
decision depends only on (`x`-interval, `z`-width), so tree sizes follow from
a memoized recursion. This is a different method from the author's
node-by-node simulation. `F_x` is minimized over candidates, and the note's
closed form is asserted at every call.

| `eps` | `multi` | `omega` | `deficit` | `bis` (ties to `z` / to `x`) | proof's certificate | note's certificate, exact | proved internal `>=` |
|---|---|---|---|---|---|---|---|
| 1e-2 | 45 | 35 | 35 | 43 / 29 | 14 | 14 | 0 |
| 1e-3 | 117 | 87 | 87 | 123 / 125 | 38 | 38 | 0 |
| 1e-4 | 789 | 231 | 231 | 379 / 253 | 123 | 121 | 16 |
| 1e-5 | 5013 | 935 | 935 | 1531 / 1021 | 385 | 375 | 144 |
| 1e-6 | 13205 | 3751 | 4775 | 4091 / 4093 | 1209 | 1180 | 912 |
| 1e-7 | 74645 | 10919 | 19111 | — | 3823 | 3727 | 5008 |
| 1e-8 | 353173 | 39591 | 39591 | — | 12077 | 11772 | 5008 |

- **Tree sizes.** `multi`, `omega` and `deficit` match the note's table
  exactly. `omega` and `deficit` had no ties.
- **Bisection depends on tie-breaking.** The note's `bis` column is the
  ties-to-`z` convention; ties to `x` give different counts. `bis` is only a
  reference rule, so this does not matter.
- **The proof's node family.** At every `eps`, all nodes `L_j × J` at depth
  `2k` are internal. Their number equals `sum (k - 1) 4^k`.
- **Certificates.**
  - "Proof's certificate" is part (a)'s construction, with `z`-pieces of
    width `2l` and a rational `h <= 2 sqrt(eps)`. Every box was validated
    exactly, and every size is within the bound of (a).
  - The note's table uses the tighter width `2 sqrt(F_x)`, checked there in
    floats. The exact version of that variant reproduces the note's sizes
    14, 38, 121, 375, 1180, 3727 and 11772, so those certificates are valid.
- **Ratios.** The table's ratio columns are therefore correct as lower
  bounds.

### 4.2 Guillotine overhead

- **Lemma N4.**
  - (a) Cells of such a partition are sub-boxes of valid boxes, and the cuts
    form a tree.
  - (b) At most `2N` face values per axis give at most `2N - 1` slabs. Every
    box of `P` is a union of grid cells, so each cell lies in one box.
  - (c) `(2 (2N-1)^n - 1)/(2N - 1) <= 2 (2N - 1)^(n-1)`.

  All correct.
- **Proposition N5.** Uniform bisection trees are guillotine and their leaves
  are valid. Theorem A bounds the number of nodes, hence the number of
  leaves. The hypotheses are stated: a cube root box and `F = X0`, with
  `kappa = 1` for the exact gap. Correct, conditional on Theorem A, which I
  did not recheck. The main note's results table quotes `C_n log(1/eps)`
  without the cube-box hypothesis; it should carry it, or say "bounded
  aspect ratio".
- **Literature.** Web search was exhausted, so I read the abstracts through
  the OpenAlex API.
  - **Paterson–Yao** (J. Algorithms 1992; SODA 1990 version): "BSPs of
    linear size for any set of orthogonal line segments in the plane". The
    note's recollection is right.
  - **Berman–DasGupta–Muthukrishnan**, "Exact size of binary space
    partitionings and improved rectangle tiling algorithms" (SIAM J.
    Discrete Math. 2002, doi 10.1137/S0895480101384347). The abstract states
    an upper bound of `2n - 1` when the rectangles tile the space.
    - Applied through Lemma N4(a), this gives directly, without the
      maximal-segment step, `N_guill <= 2 N_opt - 1` in 2D.
    - The overhead ratio is then `(2 N_guill - 1)/(2 N_opt - 1) < 2`.
    - The n-dim note's "`N_guill <= c N_opt` if the imported theorem holds"
      can be replaced by this explicit `c = 2`.
  - **Hershberger–Suri–Tóth**, "Binary space partitions of orthogonal
    subdivisions" (SIAM J. Comput. 2005, doi 10.1137/S0097539704445706).
    Every subdivision of `n` boxes in `d >= 3` dimensions refines into a BSP
    of size `O(n^((d+1)/3))`, tight for `d = 3`.
    - This gives `N_guill = O(N_opt^((n+1)/3))`, which is far better than
      N4(b)'s `(2 N_opt - 1)^n`.
    - It confirms the note's statement that 3D subdivisions can need
      superlinear BSPs (`Omega(n^(4/3))`).
    - Whether exact-gap valid families can force such subdivisions remains
      the open question, as the note says.

  I did not read the full texts. The "size" notion (fragments, which equal
  leaves for a tiling) is taken from the abstracts' usage.

### 4.3 Lemma N6 (separable bracket)

**Proof check.**

- **Upper bound.** Product boxes have `sum_i F_i >= 0`, and the product
  partition is guillotine.
- **Lower bound.** On the line `y_j = t_j` for `j ≠ i`, every certificate box
  meeting the line has `F_j(C_j) <= m_j(t_j) = eps_j`. This holds even when
  `t_j` lies on a face, since then `a_j = 0`. So `C_i` is valid for
  `m_i + sum_{j≠i} eps_j`. These intervals cover `[L_i, U_i]`, and validity
  is hereditary in 1D, so they contain a 1D certificate with at most as many
  pieces. Correct.

**Observation (precision).**

- The lower bound does not depend on how `eps` is split:
  `m_i + sum_{j≠i} eps_j = (m_i - eps_i) + eps`. It is the 1D problem for
  coordinate `i` at the full tolerance `eps`.
- The upper bound uses the smaller tolerances `eps_i`, and can be minimized
  over the split.
- So "the product of 1D certificates" in the Summary means certificates at
  the split tolerances, not the product of the slice certificates. This is
  worth stating.

**Exact consistency check** (`lemma_n6_check.py 2000 7`).

- **Setup.** 1,629 random separable instances with a random split of `eps`.
  For each, `G` is the exact least guillotine certificate on a grid that
  contains all knots and both coordinates' greedy breakpoints. So
  `G >= N_guill >= N_opt`, and the product certificate lies on the grid.
- **Result.** `max_i slice_i <= G <= product` held in every instance.
  - `G < product` in 868 instances, confirming that non-product
    certificates win.
  - `G = slice` in 45.
  - The largest `G/slice` was `11/3`, and the largest `product/G` was 2.
- **What it shows.** It can refute the lemma but not confirm `N_opt`; it
  found no refutation. The script also asserts that the slice bound does not
  depend on the split.

### 4.4 Wording error in Section 2.1

The Summary (item 1) and the heading of Section 2.1 say that the criterion
"valid iff `r <= rho(c)`" fails **in both directions** in 2D. Only one
direction fails.

- **The other direction holds.** `q_B(y) = |r|^2 - |y - c|^2` in every
  dimension, so `min_B phi_B >= M(c) - alpha |r|^2`. Hence
  `|r| <= rho(c)` implies validity for all `n`.
- **The `k = 10` example** is a valid box with `M(c) < |r|^2`. It shows that
  the converse fails.
- **The `k = 4` example** is an invalid box whose proximal point is outside
  it. It shows that Proposition 1(b) fails, not a direction of 1(a).
- **Status of the body text.** The body of Section 2.1 ("Both fail",
  referring to the two properties (a) and (b)) is correct. Only the Summary
  item and the heading misstate it.
- **Main note, Section 3.** "Part (a) fails for `n >= 2`" should say that
  its "only if" direction fails.

`examples_n1_check.py` confirms the example values exactly:

- `k = 4`: minimum of the `x`-part `4/25` at `x = 1/2`, `min phi_B = eps - 9/100`,
  proximal point `x = 39/100`.
- `k = 10`: minimum of the `x`-part `2/5`, `min phi_B = eps + 3/20`,
  `M(c) = eps + 81/440 < 5/16`.

## Remaining problems (all minor)

1. **Proposition 4' remark.** The no-clamp counts are right, but they grow by
   about 4 nodes per doubling of `log(1/eps)`, not 2 (Section 1.3). The
   `O(log log)` reading is unaffected.
2. **Corollary 1.** State `N_opt(eps - 2 delta) >= 2` (resp.
   `N_opt(eps - delta) >= 2`); otherwise `T = 1` (Section 2.1).
3. **Proposition 2.** The sentence "`R_min` is optimal among I1 rules on such
   instances" needs Theorem 3's qualifier, piecewise-quadratic (non-analytic)
   classes (Section 2.2).
4. **The I1 definition.** "`f` on a neighbourhood of `y_B`" should be the
   germ at `y_B`, or a neighbourhood of prescribed size. Otherwise I1 is
   I_inf for every `f` (Section 3).
5. **n-dim note, Summary item 1 and Section 2.1 heading.** "Fails in both
   directions" is wrong. `|r| <= rho(c)` still implies validity in every
   dimension. The main note's Section 3 has the same imprecision
   (Section 4.4).
6. **Guillotine overhead.**
   - The 2D bound can be made explicit and unconditional up to citation:
     `N_guill <= 2 N_opt - 1` (Berman–DasGupta–Muthukrishnan).
   - For `n >= 3`, `N_guill = O(N_opt^((n+1)/3))` (Hershberger–Suri–Tóth)
     supersedes `(2 N_opt - 1)^n`.
   - The main note's table should carry Theorem A's cube-box hypothesis
     (Section 4.2).
7. **SCIP wording and guard caveat.**
   - Replace "root width" and "depth-dependent" with "global width" and
     "width-dependent".
   - Mention that SCIP's absolute epsilon guards take over only for
     `eps < 3.3e-19 alpha` on this instance, so the `1e-24` and `1e-32`
     rows concern the formula, not SCIP (Section 1.3).
8. **Separable bracket.** Say that the product uses 1D certificates at the
   split tolerances `eps_i`, while the slice bound is at the full `eps`
   (Section 4.3).

## Commands run

Targeted checks only, all from `research-20260928b/reviews/competitive-recheck/`
with single-threaded Python and exact `fractions` (sympy for identities). No
project-wide checks were run, and CI was not inspected.

| Command | Result |
|---|---|
| `curl` of `src/scip/{branch,cons_nonlinear,set,scip_branch}.c` and `var.c` at tag `v10.0.2`; pyscipopt `getParam` and `writeParams` | rule and defaults as in Section 1.1 (`scip-src/`) |
| `python3 scip_prop4prime.py` | all chain assertions pass; `T = 2K + 1` at 7 tolerances for 2 values of `alpha`; no-clamp counts; guard threshold (`scip_prop4prime.log`) |
| `python3 cor1_prop2_check.py 20000 11` and `... 20000 12` | 38,586 instances; Theorem 1, Proposition 2 and Corollary 1 (a) and (b): 0 violations; stronger form: 0 violations; identities true (`cor1_prop2_s11.log`, `cor1_prop2_s12.log`) |
| `python3 thm3_scope_check.py` | Theorem 3 facts, agreement intervals, `R_min` `T = 5` on A and 3 on B; review's `11/5` instance reproduced (`thm3_scope_check.log`) |
| `python3 multi_n3_check.py 8` | table of Section 4.1; all assertions pass (`multi_n3_check.log`) |
| `python3 lemma_n6_check.py 2000 7` | 1,629 instances, 0 violations (`lemma_n6_check.log`) |
| `python3 examples_n1_check.py` | Examples N1 values; sufficient direction as an inequality (`examples_n1_check.log`) |
| OpenAlex API queries (`curl`) | abstracts of Berman–DasGupta–Muthukrishnan 2002, Hershberger–Suri–Tóth 2005 and Paterson–Yao 1990/1992 |

## Not checked

- Theorem A itself, which Proposition N5 uses, and the full texts of the three
  BSP papers.
- The floating-point experiments of the n-dim note: Sections 4 (grid
  MILP/DP), 5.2, 5.3 and 6, `aniso*`, `leafshape`, `sep_families*`,
  `sharp_quad` and `poly2d*`.
- Conjecture 1.
- Other parts of the main note, except as they bear on items (1)–(3).
- A run of real SCIP on an exact-gap instance. SCIP would not branch on the
  convex `2 alpha |y - a|` at all, so the proposition is necessarily a
  statement about the branching-point formula inside the model.
