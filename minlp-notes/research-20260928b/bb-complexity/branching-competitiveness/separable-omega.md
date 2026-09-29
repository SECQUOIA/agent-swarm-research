# The rule `omega` on separable instances

Continuation of [`competitive-branching.md`](competitive-branching.md) (the
"main note") and [`n-dimensional.md`](n-dimensional.md) (the "n-dim note").
Date: 2026-09-29, revised the same day after the independent review
[`../../reviews/separable-omega-review.md`](../../reviews/separable-omega-review.md)
(Section 10). Status: proofs with exact-arithmetic checks. The recheck
[`../../reviews/competitive-recheck.md`](../../reviews/competitive-recheck.md)
is incorporated (Section 1.3). Scripts and logs are in
[`separable/`](separable/).

The question was to settle Conjecture 1 of the main note for separable
objectives: is the rule `omega` within a constant factor `C_n` of the optimal
tree on every separable exact-gap instance, or is there a family on which its
ratio grows?

## Summary

**Conjecture 1 is still open for separable instances.** This note proves the
tools and special cases below, lower bounds for every node-local rule that
grow exponentially with the dimension, and a negative answer to the proposed
characterization of `N_opt`.

1. **Structure (Section 2).** On separable instances every minimizer rule
   builds products of the 1D relaxation-minimizer trees of the coordinates.
   `omega` alternates between *phases*: runs of splits along one coordinate
   while the other coordinates' intervals stay fixed. Inside a phase the
   rule acts as a 1D relaxation-minimizer rule with a shifted tolerance and
   an extra stopping threshold.
2. **Phase Lemma (Theorem A, Section 4).** A phase of `omega` has at most
   `24 n_P - 25` internal nodes in 2D (at most 5 if `n_P = 1`). Here `n_P`
   is the number of boxes of any certificate that meet the line through the
   phase's fixed minimizer coordinate. The proof combines the main note's
   Theorem 1 with a new lemma (Lemma T) on splits inside a valid interval.
   In `n` dimensions the constant depends only on `n`. So `omega` is
   competitive within each phase.
   - What is not proved is that the phases do not overcount the certificate.
   - The analogous statement for the largest-deficit rule is false
     (Section 4.3).
3. **A positive theorem (Theorem B, Section 5).** Suppose one coordinate is
   arbitrary and the other is *sharp*: it has a kink that every relaxation
   finds, for example `sigma |t - c| - (t - c)^2` with `sigma` at least
   twice the box width. Then `omega` uses at most `112 N_opt` nodes and the
   largest-deficit rule at most `64 N_opt`. A proof sketch extends the bound
   for `omega` to `n - 1` sharp coordinates.
   - This covers the "sharp × quadratic" family, where the n-dim note saw
     `omega`'s ratio drift from 1.25 to 1.91.
   - Exactly verified grids reproduce that drift: the ratio is 1.71–1.91 for
     `eps <= 1e-6`, and 1.91 at `1e-11`. Theorem B shows it stays bounded.
4. **Lower bounds for every node-local rule (Theorems C and C', Section 6).**
   The model is I1: the rule sees the node's relaxation solution and `f`
   near the minimizer, and here also near the box corners.
   - **Theorem C.** In every dimension `n >= 2`, every deterministic I1 rule
     has ratio at least `7/3` on separable instances, and every randomized
     rule at least `(7 - 4/n)/3`. The 1D bounds were `5/3` and `4/3`.
     - The instances are convex and separable, have `N_opt = 2`, and agree
       near the relaxation minimizer and near every corner of the box.
     - They differ only in which coordinate must be cut.
   - **Theorem C' (the iteration is due to the review).** On the same
     instances the ambiguity iterates.
     - Deterministic rules need ratio at least `11/3`, `19/3`, `31/3` and
       `17` for `n = 3, 4, 5, 6`, and about `2^(n+2)/(3n)` in general.
       Randomized rules need about the same.
     - So the competitive constant of **every** node-local I1 rule on these
       non-analytic classes grows exponentially in `n`. Rules with memory
       across nodes are not covered.
   - **`omega` on these instances.** `omega` uses 7 nodes for `n = 2`. For
     `n >= 3` it uses `2^(n+1) - 1` nodes on `A_n`, and on every labelling
     of a tie-free variant, while `N_opt = 2`.
5. **`N_opt` is not a function of the 1D certificate sizes
   (Proposition D, Section 3).** Two separable 2D families have 1D certificate
   sizes `N_i(b)` of the same order, `Θ(log(1/b))`, in every coordinate. Yet
   one has `N_opt = Θ(log(1/eps))` and the other `N_opt = Θ(log^2(1/eps))`.
   - So no formula in the functions `N_i` that is insensitive to bounded
     factors determines `N_opt` up to constants.
   - In particular `N_opt ≍ min over budget splits of prod_i N_i(eps_i)` is
     false: the product overestimates by a log factor on the first family,
     and the slice lower bound underestimates by a log factor on the second.
6. **Evidence (Section 7).** Computations compare `omega` with the best
   offline rule that splits at relaxation minimizers (`OPT_min`, computed
   exactly). The comparison depends on how minimizers are chosen when the
   node relaxation is flat on a segment (Section 1.1).
   - With the selection used in the first version (knots and endpoints
     only), `omega` is within 5% of `OPT_min` on every family tested.
   - When the most central point of a flat segment is taken instead,
     `omega/OPT_min` rises to 1.33–1.63 on caps × quadratic and to 1.5–1.8
     on dyadic caps. `OPT_min` itself is unchanged.
   - Against exactly verified grid optima, `OPT_min` loses up to a factor
     1.91. These grid ratios are lower bounds on the loss relative to
     `N_guill`.
   - Hill-climbing searches found no ratio above 2. The largest-deficit
     rule drifts above `OPT_min` (1.23) on anisotropic quadratics.

Answers to the three questions posed:

- **(1) Characterizing `N_opt`.** It is bracketed by the slice bound
  `max_i N_i(eps)` and the product bound
  `min_{sum eps_i = eps} prod_i N_i(eps_i)`. Both are off by a log factor on
  explicit families. No formula in the sizes `N_i` that is insensitive to
  bounded factors can work (Proposition D). The true structure is multiscale
  and non-product (Section 3).
- **(2) `omega` and the deficit rule.**
  - **Proved.** `omega` is competitive within each phase (Theorem A); the
    same claim for `deficit` is false (Section 4.3). Both rules are
    competitive in 2D when one coordinate is sharp (Theorem B). For `n - 1`
    sharp coordinates there is only a sketch, and only for `omega`.
  - **Searches.** No instance with ratio growing in `eps` was found.
  - **Growth in `n`.** On the ambiguity instances `omega`'s ratio is at
    least `(2^(n+1) - 1)/3`. So any constant `C_n` for `omega` must grow
    exponentially in `n`, as it must for every I1 rule (Theorem C').
  - **Remaining gap.** A full proof for separable instances needs a bound on
    how many phases can use the same certificate box (Section 7.3).
- **(3) Fallback results.** A positive theorem for a natural subclass
  (Theorem B). The lower bound for all node-local rules in `n >= 2` is
  `7/3` (Theorem C) and grows exponentially in `n` (Theorem C').

All checks are exact (Python `fractions`), except the float guillotine DP on
candidate grids, whose optimal certificates are then verified exactly box by
box. Commands are in Section 8. No project-wide checks were run and CI was not
inspected.

## 1. Setting

### 1.1 Separable instances

- **Scaling.** Scale `f` and `eps` so that `alpha = 1`.
- **Instance.** The root box is `X0 = prod_i X_i` with `X_i = [L_i, U_i]`. The
  objective is `f(y) = f* + sum_i m_i(y_i)`, where each `m_i` is continuous
  on `X_i` with `min m_i = 0`, so `f* = min f`. The main note's
  `m = f - f* + eps` is `eps + sum_i m_i` here.
- **Convex class.** The instance is in the convex class if every
  `m_i(t) + t^2` is convex. Theorems A and B and Lemma T do not need
  convexity. The instances of Theorem C and Proposition D are in the convex
  class.
- **1D node data.** For an interval `J = [l, u]` in coordinate `i`, write
  `a_J(t) = (t - l)(u - t)` and `phi_{i,J} = m_i - a_J`. Then:
  - `F_i(J) = min_J phi_{i,J}` is the 1D node value;
  - `y_i(J)` is a minimizer, chosen by a fixed deterministic rule;
  - `w_i(J) = a_J(y_i(J))` is the gap at the minimizer.

  So `F_i(J) = m_i(y_i(J)) - w_i(J)`.
- **Minimizer selection.**
  - **Assumption.** The selection `y_i(J)` depends only on coordinate `i`
    and its interval `J` (a coordinate-wise selection). The relaxation
    separates, so its minimizer set is the product of the coordinate
    minimizer sets. A solver that picked points of a non-singleton optimal
    face using global data could break the product structure of Section 2.
  - **Scope.** The proofs of Theorems A and B allow any coordinate-wise
    selection. Theorem C needs none, since its root minimizer is unique.
    Theorem C' uses coordinate-wise selection at corner nodes.
  - **Two selections in the computations.** They differ only when `phi_J`
    is constant on a segment between knots, which happens on every cell of
    the "caps" and "dyadic caps" families.
    - **`knot`:** among the minimizing knots and endpoints, the one with the
      largest `w`, then the leftmost. All runs of the first version used it.
      The first version misdescribed it as "the minimizer with the largest
      `w`".
    - **`proj`:** the point of the whole minimizer set with the largest `w`,
      that is, the centre of `J` projected onto the minimizer set, flat
      segments included. This resembles the face centre of an
      interior-point solver.
  - **Default.** Computations use `knot` unless stated.
- **Box data.** A box `B = prod_i J_i` has relaxation value
  `f* + sum_i F_i(J_i)` and relaxation minimizer `y_B = (y_i(J_i))_i`. It is
  valid iff `sum_i F_i(J_i) + eps >= 0`.
- **Budgets.** An interval `J` is *valid at budget `b`* if `F_i(J) >= -b`.
  For an interval `A`, `N_{i,A}(b)` is the least number of pieces in a
  partition of `A` into intervals valid at budget `b`. Write
  `N_i(b) = N_{i,X_i}(b)`. For `b > 0` this is finite, since `m_i >= 0` makes
  every piece of length at most `2 sqrt(b)` valid.

### 1.2 Rules and benchmarks

- **`omega`** splits an invalid box at `y_B` along the coordinate with the
  largest `w_i(J_i)`, with ties to the lowest index.
- **`deficit`** splits along the coordinate with the smallest `F_i(J_i)`
  among those with `w_i(J_i) > 0`, with ties to the lowest index.
- **`OPT_min`** is the least number of leaves of any tree that splits every
  invalid node at its relaxation minimizer along some coordinate with
  `w_i > 0`. The coordinate may be chosen offline. It is a lower bound for
  every minimizer rule, and it is computed exactly by a memoized recursion
  (`sepexact.opt_min`).
- **Benchmarks.** `N_opt` is the least certificate (any partition into valid
  boxes). `N_guill` is the least guillotine certificate. The best tree has
  `T_opt = 2 N_guill - 1` nodes.

### 1.3 Facts from the recheck used here

The recheck [`../../reviews/competitive-recheck.md`](../../reviews/competitive-recheck.md)
supplies three facts.

- **(R1) Guillotine overhead in 2D.** `N_guill <= 2 N_opt - 1`
  (Berman–DasGupta–Muthukrishnan 2002, via refinement of a certificate). So in
  2D, comparing against arbitrary certificates costs at most a factor 2. All
  bounds proved below are already against `N_opt`.
- **(R2) Radius sufficiency.** A box with centre `c` and half-width vector
  `r` is valid if `|r|^2 <= eps + M(c)`, where
  `M(c) = min_{y in X0} (m(y) - eps + |y - c|^2)` in the main note's notation.
  Here that is `min_y (sum_i m_i(y_i) + |y - c|^2)`. The proof is
  `phi_B(y) = sum_i m_i(y_i) + |y - c|^2 - |r|^2` on `B`.
- **(R3) Split tolerances.** In the bracket of Lemma N6, the product bound
  uses certificates at the split tolerances `eps_i`, while the slice bound is
  at the full `eps`.

## 2. Structure of minimizer rules on separable instances

**Lemma 2.1 (products of 1D trees).**

- Let `T_i` be the 1D relaxation-minimizer tree of coordinate `i`. Its root
  is `X_i`, and a node `J` with `w_i(J) > 0` has children `[l, y_i(J)]` and
  `[y_i(J), u]`.
- Every node of a minimizer rule's tree on a separable instance is a product
  `prod_i J_i` with `J_i` a node of `T_i`.
- `omega`'s choice at `prod_i J_i` depends only on the numbers
  `w_i(J_i)`. Validity depends only on the numbers `F_i(J_i)`.

*Proof.* Induction on depth. The relaxation separates, so a split along `i`
at `y_B` replaces `J_i` by a child of `J_i` in `T_i`. An invalid box has some
`w_i > 0`: if all `w_i = 0`, every `y_i` is an endpoint and
`F_i = m_i(y_i) >= 0`, so the box is valid. □

**Lemma 2.2 (1D facts).** Let `J' = [p, q] ⊆ J = [l, u]` and `t in J'`.

- (a) `a_J(t) - a_{J'}(t) = (t - p)(u - q) + (p - l)(q - t) + (p - l)(u - q) >= 0`.
  The expression is linear in `t`, and its minimum over `[p, q]` is
  `min(a_J(p), a_J(q))`.
- (b) `F_i(J') >= F_i(J) + a_J(y) - a_{J'}(y)` with `y = y_i(J')`. In
  particular `F_i` does not decrease from parent to child.
- (c) `F_i(J') >= F_i(J) + min(a_J(p), a_J(q))`.

*Proof.* For (a), expand `(t - l) = (t - p) + (p - l)` and
`(u - t) = (q - t) + (u - q)`. For (b),
`F_i(J') = m_i(y) - a_{J'}(y) = phi_{i,J}(y) + a_J(y) - a_{J'}(y)`, and
`phi_{i,J}(y) >= F_i(J)`. Part (c) follows from (a) and (b). □

**Theorem 1' (the main note's Theorem 1 with a budget).** Let `A` be an
interval, `b > 0`, and `N = N_{i,A}(b) >= 2`. The relaxation-minimizer tree of
`A` stopped at budget `b` has at most `4N - 5` internal nodes and `4N - 4`
leaves. It splits `J` iff `F_i(J) < -b`. If `N = 1`, the tree is `A` alone.

*Proof.* Apply Theorem 1 of the main note to `m_i + b`, which is at least
`b > 0` and continuous. Then `F_i(J) >= -b` iff
`min_J (m_i + b - a_J) >= 0`, which is the main note's validity. Adding a
constant does not move minimizers. Theorem 1 needs only continuity and
positivity. □

**Phases.** An *`i`-phase* of `omega` is a maximal connected set of `omega`
nodes that are split along `i` and share the same intervals `J_{-i}` in the
other coordinates. Its root is `A × J_{-i}` with `A` in `T_i`.

- Inside the phase, the other coordinates' data are frozen:
  - `beta = eps + sum_{k≠i} F_k(J_k)`;
  - `tau = max_{k≠i} w_k(J_k)`;
  - the point `y_{-i} = (y_k(J_k))_{k≠i}`.
- A node `D × J_{-i}` of the phase is split along `i` only if
  `F_i(D) < -beta` (it is invalid) and `w_i(D) >= tau` (`omega` prefers `i`).
  With ties the second condition may be strict.
- So the phase is contained in the *pruned tree* `S_i(A; beta, tau)`. Its
  root is `A`, and it splits `D` iff `F_i(D) < -beta` and `w_i(D) >= tau`.
- The *phase segment* is `A × {y_{-i}}`.

## 3. Question (1): what determines `N_opt`

### 3.1 The bracket

**Proposition 3.1** (Lemma N6 of the n-dim note, with (R3)).

```
max_i N_i(eps)  <=  N_opt  <=  N_guill  <=  min over eps_1 + ... + eps_n = eps of  prod_i N_i(eps_i).
```

*Proof.*

- **Upper bound.** A product of 1D certificates at budgets `eps_i` has
  `sum_i F_i >= -sum_i eps_i = -eps` on every box, and it is guillotine.
- **Lower bound.** The *slice argument* gives it; it is used repeatedly
  below. Fix `i` and a point `y`. Every box `C` of a certificate that meets
  the line `{y' : y'_k = y_k for k ≠ i}` has
  `F_k(C_k) <= m_k(y_k) - a_{C_k}(y_k) <= m_k(y_k)` for `k ≠ i`. Hence
  `F_i(C_i) >= -(eps + sum_{k≠i} m_k(y_k))`.
- **Conclusion.** These intervals `C_i` cover `X_i`, and validity passes to
  sub-intervals. So they contain a partition into at most as many pieces
  valid at budget `eps + sum_{k≠i} m_k(y_k)`. Choosing `y_k` with
  `m_k(y_k) = 0` gives `N_i(eps)`. □

**Slice form, used in Section 4.** For any segment `A × {y_{-i}}`, the
number of certificate boxes meeting it is at least
`N_{i,A}(eps + sum_{k≠i} m_k(y_k))`.

### 3.2 Doubling

**Lemma 3.2 (budget halving costs a factor 3).** For continuous `m_i >= 0`
and `b > 0`, `N_{i,A}(b/2) <= 3 N_{i,A}(b)`.

*Proof.* Take a piece `K = [l, u]` of an optimal certificate at budget `b`.

1. **Short pieces.** If `|K|^2/4 <= b/2`, then
   `F_i(K) >= -max a_K = -|K|^2/4 >= -b/2`.
2. **Otherwise, cut in three.** Let `p1 < p2` be the roots of `a_K = b/2`.
3. **Middle piece.** By Lemma 2.2(c), `[p1, p2]` has
   `F_i >= F_i(K) + b/2 >= -b/2`.
4. **End pieces.** Since `u - p1 >= |K|/2`, the end piece `[l, p1]` has
   length at most `b/|K|`. So `F_i >= -b^2/(4|K|^2) >= -b/2`, because
   `b < |K|^2/2`. The piece `[p2, u]` is symmetric. □

### 3.3 No formula in the 1D certificate sizes

Take two 1D functions on `[0, 1]`, both in the convex class:

- `q(t) = t^2`;
- `g`, the "dyadic caps": `g = 0` at `0` and at `s_k = 2^-k` (`k >= 0`),
  and `g(t) = (t - s_{k+1})(s_k - t)` on the cell `C_k = [s_{k+1}, s_k]`.
  Here `g + t^2` is linear on each cell, with slopes `3·2^{-k-1}` increasing
  in `t`.

**Proposition D.** There are constants `c, C > 0` and `b_0, eps_0 > 0` such
that, for `0 < b <= b_0` and `0 < eps <= eps_0`:

- (a) `c log(1/b) <= N_q(b), N_g(b) <= C log(1/b)`. The two coordinates
  have 1D certificate sizes of the same order at every budget.
- (b) The instance `q(x) + q(z)` on `[0,1]^2` has
  `N_guill <= 1 + 3 ceil((1/2) log_2(1/eps))`.
- (c) The instance `g(x) + g(z)` has `N_opt >= c log^2(1/eps)`.
- (d) Consequences:
  - the product bound of Proposition 3.1 is `Θ(log^2(1/eps))` for `q ⊕ q`,
    a log factor too large;
  - the slice bound is `Θ(log(1/eps))` for `g ⊕ g`, a log factor too small;
  - no formula in the sizes `(N_i(·))_i` determines `N_opt` up to constant
    factors if it is insensitive to bounded multiplicative changes of the
    `N_i`. Such formulas include the product and slice forms and anything
    built from orders of growth.
  - The functions `N_q` and `N_g` themselves differ by bounded factors
    (asymptotically `N_g ≈ 1.6 N_q`). A contrived formula sensitive to such
    factors is not excluded.

*Proof of (a) for `q`.* For `J = [l, u]`,
`phi_J(t) = 2t^2 - (l + u)t + lu`.

- **Node values.** If `u >= 3l` the minimizer is `(l+u)/4` and
  `F = (6lu - l^2 - u^2)/8`. Otherwise the minimizer is `l` and
  `F = l^2 >= 0`.
- **Upper bound.** The pieces `[0, sqrt(8b)]` (with `F = -b`) and
  `[3^j sqrt(8b), 3^{j+1} sqrt(8b)]` (with `F >= 0`) certify.
- **Lower bound.** The piece containing `0` has `u <= sqrt(8b)`. A piece
  with `u >= 7l` has `F <= -u^2/56`, so every valid piece has
  `u <= max(7l, sqrt(56 b))`. Reaching `1` needs at least
  `log_7(1/sqrt(56 b))` pieces.

*Proof of (a) for `g`.*

- **Deficit at a breakpoint.** For a breakpoint `s` in the interior of `I`,
  `F_g(I) <= g(s) - a_I(s) = -a_I(s)`.
- **Upper bound.** The cells `C_0, ..., C_{K-1}` have `F = 0`, since `phi`
  vanishes on a cell. The piece `[0, s_K]` has `F >= -s_K^2/4`. So
  `N_g(b) <= K + 1` for `4^{-K}/4 <= b`.
- **Lower bound.** An interval containing `s_{k+1}, s_k, s_{k-1}` has
  `F <= -(s_k - s_{k+1})(s_{k-1} - s_k) = -2^{-2k-1}`.
  - Let `K_b = max{k : 2^{-2k-1} > b}`.
  - A valid piece contains at most two of the `K_b + 2` points
    `s_0, ..., s_{K_b + 1}`. Three of them in one interval are consecutive,
    and the middle one has index in `[1, K_b]`.
  - So `N_g(b) >= (K_b + 2)/2`.

*Proof of (b).*

- **The Moreau term.** `M(c) = min_{y in [0,1]^2} (|y|^2 + |y - c|^2) = |c|^2/2`,
  attained at `y = c/2`.
- **Innermost square.** Put `rho_0 = sqrt(eps)`. The square `[0, rho_0]^2`
  has `|r|^2 = eps/2`.
- **Shells.** For `rho >= rho_0`, the squares `[rho, 2 rho] × [0, rho]`,
  `[0, rho] × [rho, 2 rho]` and `[rho, 2 rho]^2` have `|r|^2 = rho^2/2`. Their
  values of `|c|^2/2` are `5 rho^2/4`, `5 rho^2/4` and `9 rho^2/4`.
- **Validity.** All of these boxes are valid by (R2).
- **The partition.** Doubling `rho` from `rho_0` until `2 rho >= 1`, and
  clipping to the unit square, gives a guillotine partition with
  `1 + 3 ceil(log_2(1/rho_0))` boxes. At each level, cut `x` at `rho`, then
  `z` at `rho` in both halves.

*Proof of (c).* Fix a certificate of `g ⊕ g`.

1. **Lines and targets.** For `j >= 0` let `Λ_j` be the line `z = s_j` and
   `X_j = [0, s_{j+1}]`. Let `K = max{k : 2^{-2k-1} > eps}` and
   `J* = max{j : 4^{-j-2} >= eps}`.
2. **Claim 1: a box that meets two lines far apart avoids `X_j`.** Suppose a
   valid box `C = I × J` meets `Λ_j` and `Λ_{j'}` with `j' >= j + 2`, and
   `j <= J*`.
   - Then `J ⊇ [s_{j+2}, s_j]`, so `F_g(J) <= -2^{-2j-3}`.
   - Hence `F_g(I) >= 2^{-2j-3} - eps >= 2^{-2j-4} > 0`.
   - A positive value rules out breakpoints in the interior of `I`, and also
     `0` (breakpoints accumulate there). So `I` lies in one cell `C_k`, and
     `F_g(I) <= max_{C_k} g = 4^{-k-2}`.
   - So `4^{-k-2} >= 4^{-j-2}`, that is `k <= j`, and `I` does not meet the
     interior of `X_j`.
3. **Claim 2: many boxes along each line.** For `j <= J*`, let `P_j` be the
   set of boxes that meet `Λ_j` at points with `x` in the interior of `X_j`.
   - Such a box has `F_g(C_z) <= 0`, so `F_g(C_x) >= -eps`.
   - Their `x`-intervals cover `X_j`. By the three-point argument of (a),
     restricted to the points `s_{j+1}, ..., s_{K+1}`,
     `|P_j| >= (K - j + 1)/2`.
4. **Claim 3: each box is counted at most twice.** By Claim 1, a box lies in
   `P_j` for at most two values of `j`, and they are consecutive.
5. **Count.** `N_opt >= (1/2) sum_{j=0}^{J*} (K - j + 1)/2`. Since
   `J* = K - O(1)` and `K = Θ(log(1/eps))`, this is `Θ(log^2(1/eps))`. □

**Numbers** (`separable/propD_redo.py`, `propD_redo.log`). Revised after the
review:

- the first version used a knot interpolant of `q`, which lies above `t^2`;
  all `q` numbers are now for the exact `q = t^2`;
- the `g ⊕ g` upper bounds now include exact product certificates.

| `b` or `eps` | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 |
|---|---|---|---|---|---|
| `N_g(b)` / `N_q(b)` (exact greedy; certified bracket for `q`) | 5 / 3 | 7 / 4 | 8 / 4 | 10 / 5 | 12 / 5 |
| `g ⊕ g`: lower bound from the proof of (c) | 4 | 7 | 10 | 14 | 20 |
| `g ⊕ g`: best exactly verified upper bound on `N_guill` (grid optimum or product certificate) | 27 | 49 | 80 | 102 | 144 |
| `q ⊕ q`: the construction of (b) | 16 | 22 | 28 | 31 | 37 |
| `q ⊕ q`: exactly verified grid optimum | 6 | 8 | 9 | 11 | 13 |
| `omega` leaves, `g ⊕ g`, `knot` / `proj` selection | 27 / 41 | 50 / 84 | 81 / 143 | 102 / 181 | 145 / 264 |
| `omega` leaves, `q ⊕ q` | 7 | 10 | 13 | 16 | 18 |

- **`g ⊕ g`.** The upper bound tracks `N_g(eps)^2`, and the product
  certificate is optimal or near-optimal on these grids. The proof's lower
  bound grows like `K^2/8` and is far from tight at these tolerances.
  - Under `knot`, `omega` is within one box of the best upper bound.
  - Under `proj`, `omega` spends a split in the middle of every flat cell
    and is 1.5–1.8 times larger (Section 7.1).
- **`q ⊕ q`.** The grid optimum grows linearly in `log(1/eps)`. The
  construction of (b) proves only the order.

**What the right object is.** Validity couples coordinates through
`sum_i F_i(J_i)` on every product of intervals. The functions
`b -> N_i(b)` forget where along the axis the deficits and surpluses sit.
`q` has growing surplus away from its minimizer, which lets boxes grow like
Whitney cubes. `g` has deficits at every scale spread along the axis, which
forces a product structure near each line `z = s_j`. So `N_opt` depends on
the interval functions `J -> F_i(J)` themselves. The bracket of
Proposition 3.1 is the most that the sizes `N_i` alone can give.

## 4. The Phase Lemma

All of this section is one-dimensional. Fix a coordinate, drop the index
`i`, and let `m >= 0` be continuous, not necessarily convex. Fix `beta` in
`R`, `tau > 0`, an integer `kappa >= 1`, and put `b = beta + kappa tau > 0`.

A node `D` of the relaxation-minimizer tree is a *split node* if
`F(D) < -beta` and `w(D) >= tau`. The pruned tree `S(A; beta, tau)` splits
exactly its split nodes, starting from `A`.

### 4.1 Lemma T and the Phase Lemma

**Lemma T (split nodes inside a valid interval).** Let `ℓ` be an interval
with `F(ℓ) >= -b`. Then at most `c_kappa = kappa (2 kappa (kappa + 1) + 1)`
internal nodes of `S(A; beta, tau)` lie inside `ℓ`. In particular
`c_1 = 5`.

*Proof.*

1. **The gap inequality.** Let `D = [p, q] ⊆ ℓ = [p0, q0]` be a split node
   with split point `y`. Put `L = y - p`, `R = q - y`, `gL = p - p0` and
   `gR = q0 - q`.
   - Validity of `ℓ` gives `m(y) >= a_ℓ(y) - b`.
   - `D` is a split node: `m(y) - a_D(y) < -beta`.
   - Hence `a_ℓ(y) - a_D(y) < kappa tau <= kappa L R`. By Lemma 2.2(a):

     ```
     L gR + R gL + gL gR < kappa tau <= kappa L R.          (*)
     ```

   - So `gR < kappa R` and `gL < kappa L`, and
     `|ℓ| < (1 + kappa)|D|`. Every split node inside `ℓ` is longer than
     `|ℓ|/(1 + kappa)`.
2. **Chains.** Let `D^1 ⊋ D^2 ⊋ ... ⊋ D^r` be split nodes inside `ℓ`, each
   a child of the previous one.
   - Call step `k` *left* if `D^{k+1} = [p_k, y_k]`. It removes the right
     part, of length `R_k`.
   - Since `w(D^k) = L_k R_k >= tau` and `L_k <= |ℓ|`, each left step removes
     at least `tau/|ℓ|`. So after `nL` left steps, `gR >= nL tau/|ℓ|`.
   - Then `(*)` at `D^j` gives `nL(j) L_j < kappa |ℓ|`.
   - A left step at `j` produces `D^{j+1}` of length `L_j`, which is a split
     node inside `ℓ`, so `L_j > |ℓ|/(1 + kappa)`. Hence
     `nL(j) < kappa (kappa + 1)`.
   - So there are at most `kappa (kappa + 1)` left steps, and symmetrically
     at most `kappa (kappa + 1)` right steps. A chain has at most
     `2 kappa (kappa + 1) + 1` nodes.
3. **Few chains.** The split nodes inside `ℓ` are closed under taking
   ancestors that lie inside `ℓ`.
   - Their minimal elements are pairwise disjoint and longer than
     `|ℓ|/(1 + kappa)`, so there are at most `kappa` of them.
   - Every such node lies on a chain from a maximal element to a minimal
     one. So there are at most `kappa` chains, each of at most
     `2 kappa (kappa + 1) + 1` nodes. □

**Theorem A (Phase Lemma).** Let `N = N_A(b)` with `b = beta + kappa tau`.
Then `S(A; beta, tau)` has at most `4N - 5 + c_kappa (4N - 4)` internal nodes
if `N >= 2`, and at most `c_kappa` if `N = 1`. For `kappa = 1` this is
`24N - 25` (and 5 when `N = 1`).

*Proof.* Let `T_b` be the relaxation-minimizer tree of `A` stopped at budget
`b`. Let `D` be an internal node of `S(A; beta, tau)`.

- **Case `F(D) < -b`.** Every ancestor also has `F < -b` (Lemma 2.2(b)), so
  `D` is an internal node of `T_b`. There are at most `4N - 5` of these, by
  Theorem 1'.
- **Case `F(D) >= -b`.** Let `ℓ` be the first ancestor-or-self of `D` with
  `F(ℓ) >= -b`. It is a leaf of `T_b` and contains `D`. By Lemma T at most
  `c_kappa` split nodes lie in each leaf, and `T_b` has at most `4N - 4`
  leaves. □

### 4.2 Phases of `omega`

**Corollary A' (phases of `omega`).** Consider an `i`-phase of `omega` in
dimension `d` with root `A × J_{-i}` and phase segment `A × {y_{-i}}`. Let
`n_P` be the number of boxes of any certificate that meet the segment.

- **Case `tau > 0`.** The phase has at most
  `4 n_P - 5 + c_{d-1}(4 n_P - 4)` internal nodes if `n_P >= 2`, and at most
  `c_{d-1}` if `n_P = 1`. In 2D this is `24 n_P - 25`, respectively 5.
- **Case `tau = 0`.** Every other coordinate's minimizer is then an endpoint
  of its interval. The phase has at most `4 n_P - 5` internal nodes if
  `n_P >= 2`, and none if `n_P = 1`.

*Proof.*

- **Containment.** The phase is contained in `S_i(A; beta, tau)` (Section 2),
  with `beta = eps + sum_{k≠i} F_k` and `tau = max_{k≠i} w_k`.
- **Budget.** With `kappa = d - 1`,
  `b = beta + kappa tau >= eps + sum_{k≠i} (F_k + w_k) = eps + sum_{k≠i} m_k(y_k)`.
- **Monotonicity.** `N_A(·)` is nonincreasing, so
  `N_A(b) <= N_A(eps + sum_{k≠i} m_k(y_k))`.
- **Slice.** That is at most `n_P` by the slice form of Proposition 3.1. For
  `tau > 0`, Theorem A gives the bound.
- **Case `tau = 0`.** Now `w_k = 0` and `F_k = m_k(y_k)` for `k ≠ i`, so
  `beta = eps + sum_{k≠i} m_k(y_k)`, the slice budget itself.
  - The threshold `w_i(D) >= 0` is vacuous, since an invalid node has an
    interior minimizer.
  - So the phase is the relaxation-minimizer tree of `A` stopped at `beta`,
    and Theorem 1' gives `4 N_A(beta) - 5 <= 4 n_P - 5`. □

The case `tau = 0` is not rare. The review found it in 5,218 of 10,023
random 2D phases. The first version omitted it, and wrote the bound without
the case `n_P = 1`, where the displayed formula gives `-1`. The review
exhibits an instance with `n_P = 1` whose phase has one internal node.

So inside one phase, `omega` is competitive against the certificate's
trace on the phase segment, however large the other coordinates' deficit
`-sum_{k≠i} F_k` is. The threshold `tau` is what makes this true. Without
it, a phase with `beta <= 0` could refine far beyond the slice certificate.
Section 4.3 shows that this happens for the deficit rule.

**Exact check** (`separable/phase_check.py`, `phase_check.log`). There were
6,000 random 1D instances, half convex and half non-convex, with
`kappa in {1, 2, 3}`, `tau` in `[1e-5, 1e-1]` and `b` in `[1e-6, 1e-1]`.
Results:

- the maximum number of split nodes inside one leaf of `T_b` was 1 or 2,
  against the bounds 5, 26 and 75;
- `|S| <= 4N - 5 + c_kappa (4N - 4)` held throughout;
- the largest `|S|/N_A(b)` was 2.

An LP search over chain geometries (`chainlp3.py`, `chainlp3.log`, 30,000
random geometries per `kappa`) found no chain inside a valid interval longer
than 2, 3 and 3 nodes for `kappa = 1, 2, 3`. The proof's bounds are
`5, 13, 25`. The LP uses only the
values of `m` at split points, so it also covers non-convex `m`.

### 4.3 The deficit rule is not competitive within a phase

The first version claimed, in its answer to question (2), that the deficit
rule is competitive within a phase "by Theorem A". **That claim is false and
is withdrawn.**

- **Why Theorem A does not apply.** The deficit rule has no threshold
  `w >= tau`.
  - In a phase with frozen data `beta, tau`, it splits `D` only if
    `F_i(D) < -beta` and `F_i(D)` is not larger than the frozen values
    `F_k` of the other coordinates with `w_k > 0` (ties by index).
  - In 2D this means, up to ties, `F_i(D) < -max(beta, eps - beta)`. So the
    phase is the relaxation-minimizer tree stopped at the budget
    `max(beta, eps - beta)`,
    which is at least `eps/2`.
  - The slice budget `eps + sum_{k≠i} m_k(y_k)` can be much larger.
- **Counterexample.** The instance is the review's; it was re-derived here
  with this note's engine (`deficit_phase.py`, `deficit_phase.log`).
  - **Instance.** `x` has `m_x = t^2` exactly, and `z` is the tent
    `H_z = max(0, (1 - eps)t, (1 + eps)t - eps)`, `m_z = H_z - t^2`.
  - **Root.** The `z`-coordinate has minimizer `1/2`, value `-eps/2`,
    `w_z = 1/4` and `m_z(1/2) = 1/4 - eps/2`. The `x`-coordinate has value
    `-1/8`, so `deficit` splits `x` first.
  - **Growth.** Its first phase (`z = [0,1]` frozen) has 2, 3, 4, 5, 6, 7, 7
    and 8 internal nodes at `eps = 1e-3, ..., 1e-10`.
  - **A certificate with `n_P = 1`.** The strip `[0,1] × [2/5, 3/5]` is
    valid, with value `F_x([0,1]) + F_z([2/5,3/5]) + eps = 0.115 + eps/2`.
    - Complete it by 1D pieces at budget `eps` on `[0,1] × [0, 2/5]` and
      `[0,1] × [3/5, 1]`, where `F_z = 0`.
    - Exactly one box of this certificate meets the phase segment
      `[0,1] × {1/2}`, so `n_P = 1`.
- **What this does not show.** The whole `deficit` tree stays small (at most
  17 nodes, against `N_x(eps) = 3, ..., 7`). The example refutes only the
  phase-wise claim, not competitiveness of the deficit rule.

## 5. A positive theorem: one arbitrary coordinate, the others sharp

**Definition.** Coordinate `z` is *sharp at `c in int Z`* if both of the
following hold:

- (S1) every interval `J` containing `c` in its interior has minimizer `c`,
  and `m_z(c) = 0`. So `F_z(J) = -a_J(c)` and `w_z(J) = a_J(c)`.
- (S2) every interval on one side of `c` has `w_z = 0` and `F_z >= 0`.

Example: `m_z(t) = sigma |t - c| - (t - c)^2` with
`sigma >= 2 (U_z - L_z)`. This is in the convex class, and `phi_J` is
piecewise linear with a single kink at `c`.

- On an interval containing `c`, the slopes on the two sides of `c` are
  `±sigma - (l + u - 2c)`. They have opposite signs.
- On an interval `[l', u']` on one side, `phi` is linear with slope
  `±sigma + 2c - l' - u'`. It is minimized at the endpoint nearest `c`, where
  its value is `m_z >= 0`.

**Theorem B.** Let `n = 2`, let `x` be an arbitrary continuous coordinate,
and let `z` be sharp at `c`. Put `N = N_x(eps)`. Then:

- (i) `N_opt >= N`;
- (ii) `omega` has at most `56 N` leaves, so `T_omega <= 112 N_opt - 1`;
- (iii) `deficit` has at most `32 N` leaves, so `T_deficit <= 64 N_opt - 1`.

Both hold for either tie-breaking order.

*Proof.*

1. **Part (i).** It is the slice through `z = c`: there `m_z(c) = 0`.
2. **Phase 1.** Until `z` is split, every node is `I × Z` with
   `F_z(Z) = -omega0` and `w_z(Z) = omega0`, where `omega0 = a_Z(c)`.
   - `omega` splits `x` at such a node iff it is invalid,
     `F_x(I) < -(eps - omega0)`, and `w_x(I) >= omega0` (or `>` under the
     other tie order).
   - So phase 1 is contained in `S_x(X; eps - omega0, omega0)`, whose budget
     with `kappa = 1` is `b = eps`.
   - By Theorem A it has `|S_1| <= 24N - 25` internal nodes (`<= 5` if
     `N = 1`) and `|S_1| + 1` leaves.
3. **After the `z`-split.** A phase-1 leaf `I × Z` is either valid, and then
   it is one leaf, or it is split along `z` at `c`.
   - The halves `I × Z^±` have `F_z = w_z = 0` by (S2).
   - From then on `omega` splits `x` exactly as the 1D rule at budget `eps`
     does. A box with `w_x = 0` has `F_x >= 0` and is valid.
4. **Leaves under a phase-1 leaf `I`.**
   - If `F_x(I) < -eps`, then `I` is an internal node of `T_eps`, the 1D
     tree stopped at `eps` (all its ancestors have smaller `F_x`). Each half
     then has as many leaves as `T_eps` has inside `I`.
   - If `F_x(I) >= -eps`, both halves are valid.
   - Phase-1 leaves are disjoint. So the total is at most
     `2 (#leaves of T_eps) + 2 (|S_1| + 1)`.
5. **Count for `omega`.** By Theorem 1' this is at most
   `2(4N - 4) + 2(24N - 24) = 56N - 56` when `N >= 2`, and at most 14 when
   `N = 1`.
6. **The deficit rule.** It splits `x` at `I × Z` iff `w_x(I) > 0`,
   `F_x(I) <= -omega0` and `F_x(I) < omega0 - eps`. Either way
   `F_x(I) < -eps/2`.
   - So its phase 1 lies inside `T_{eps/2}`, which has at most
     `4 N_x(eps/2) - 4 <= 12N - 4` leaves by Lemma 3.2.
   - The rest is as for `omega`: at most `2(4N - 4) + 2(12N - 4) <= 32N`
     leaves. □

**Exact check** (`separable/thmB_check.py`, `thmB_check.log`). There were
2,000 random instances. In each, `x` is a random convex or non-convex knot
instance and `z = 2|t - c| - (t - c)^2` with random `c`, and `eps` ranges
over `1e-1 … 1e-6`. All three bounds held:

- the phase-1 bound;
- the `omega` bound;
- the `deficit` bound.

The largest leaves-to-`N_x(eps)` ratio was 3.33 for both rules, and the
largest phase-1 size was `1.5 N`.

**Remarks.**

- **More sharp coordinates.** Let coordinates `2, ..., n` be sharp and `x`
  arbitrary. Each `x`-phase then runs while a set `U` of sharp coordinates
  is still unsplit. It has `beta = eps - sum_U omega_k`,
  `tau = max_U omega_k` and `kappa = |U|`, so its budget is again at least
  `eps`, and Theorem A bounds it by `N_{x,I}(eps)`.
  - Each sharp coordinate is in one of 3 states (unsplit, left half, right
    half), so there are at most `3^(n-1)` state patterns.
  - Phases with the same pattern have interior-disjoint roots, and phase
    roots are leaves of earlier phases.
  - Summing gives `T_omega <= C_n N_x(eps) <= C_n N_opt`.

  This is a proof sketch, for `omega` only; the constant was not optimized.
  The review found leaves `<= 7 N_x(eps)` for both rules on 300 random
  instances with `n = 3`.
- **The drift family.** The n-dim note's "sharp × quadratic" family is
  covered: `x = 2|t - 1/3| - (t - 1/3)^2` (sharp) and `z` the knot
  interpolant of `(t - 29/70)^2`. Its drift is real but bounded.
  - **Grids.** Revised after the review. The grid optimum is the smaller of
    two exactly verified grid optima: the first version's grids
    (`exp1.log`, `exp7.log`), and strip-adapted grids built as the review
    proposed (`drift_grid.py`, `drift_grid.log`).
  - **Strip-adapted grids.** In `x`, the points `1/3 ± d`, with `d`
    geometric of ratio 4 from `eps/4`. In `z`, `omega`'s cuts plus the
    greedy breakpoints at every strip budget `eps + m_x(1/3 ± d)`; up to
    41 × 200 points.

  | `eps` | 1e-3 | 1e-4 | 1e-5 | 1e-6 | 1e-7 | 1e-8 | 1e-9 | 1e-10 | 1e-11 |
  |---|---|---|---|---|---|---|---|---|---|
  | slice `N_z(eps)` (lower bound on `N_opt`) | 4 | 6 | 7 | 8 | 10 | 11 | 12 | 13 | 15 |
  | grid optimum (upper bound on `N_guill`) | 8 | 11 | 13 | 14 | 16 | 18 | 20 | 22 | 23 |
  | `omega` leaves `= OPT_min` | 10 | 14 | 18 | 24 | 28 | 32 | 36 | 38 | 44 |
  | `omega`/grid optimum | 1.25 | 1.27 | 1.38 | 1.71 | 1.75 | 1.78 | 1.80 | 1.73 | 1.91 |

  - **The ratio against `N_opt`.** It lies between `omega`/grid optimum
    (1.71–1.91 for `eps <= 1e-6`) and `omega`/slice, which is at most 3.0
    (`24/8` at `1e-6`, `36/12` at `1e-9`).
  - **Growth rates.** The grid optimum grows by about 2 per decade and
    `omega` by about 4, consistent with an asymptotic ratio near 2.
    Theorem B bounds the ratio in any case.
  - **Where the loss comes from.** `omega` equals `OPT_min` at every
    tolerance, under both minimizer selections. The whole loss is the 1D
    loss of splitting a quadratic at relaxation minimizers.
  - **A correction.** The first version said the ratio "levels off near 1.5"
    and called the n-dim note's 1.91 at `1e-11` a float artefact. Both
    statements were wrong. The value 1.91 at `1e-11` is confirmed, on
    exactly verified grids.

## 6. Lower bounds for every node-local rule in `n >= 2`

Model I1 (main note, Section 1.4, with the recheck's "germ" reading): at a
node the rule sees:

- the box, `eps`, the incumbent and the relaxation value;
- the relaxation minimizer `y_B`, selected coordinate-wise (Section 1.1);
- `f` on a neighbourhood of `y_B`.

Here it may also see `f` near every corner of the box. It may **not** see
`f` near the centres of the facets: the instances below differ there, for
example by `19/100` at `(0, 1/2)` for `n = 2`. Theorem 3 of the main note, in
1D, covered both endpoints, which are the whole boundary of an interval.

### 6.1 Instances

**Parameters.** Fix `n >= 2` and `eps > 0`, and choose `c` with

```
eps (2n - 1) / (2n (n - 1))  <  c  <  (1 + 2 eps) / (4n).          (6.1)
```

Such a `c` exists iff `eps < (n - 1)/(2n)`. For `eps = 1/100`, the choice
`c = 1/(5n)` works for every `n >= 2`. Put

```
sL = 1 - eps/(4(n-1)),  sR = 1 + eps/(4(n-1)),  phi = (n-1) c - eps/2,  phi' = phi/(n-1) = c - eps/(2(n-1)),
lL(t) = 1/2 - c + sL (t - 1/2),   lR(t) = 1/2 - c + sR (t - 1/2).
```

The first version wrote `r0 = 1/4 - c`, with `r0 = 3/20` (`c = 1/10`) for
`n = 2`. Its script used `r0 = (n-1)/(4n) + 1/50` for `n >= 3`. That choice
violates (6.1) from `n = 12` on, where the root becomes valid; the review
found this. `c = 1/(5n)` gives `r0 = 3/20` at `n = 2`.

Define two 1D functions on `[0, 1]` by `m = H - t^2`:

```
R ('rigid'):     H_R = max( lL, lR, t/2 + phi,   3t/2 - 1/2 + phi  )
N ('non-rigid'): H_N = max( lL, lR, t/2 - phi',  3t/2 - 1/2 - phi' )
```

Instance `A_i` (`i = 1, ..., n`) uses `R` in coordinate `i` and `N` in the
others, on `[0, 1]^n`.

**Lemma 6.1.** Under (6.1):

- (a) `H_R` and `H_N` are convex. Both have the unique root minimizer `1/2`,
  with root value `-c`.
- (b) `R = N` on a neighbourhood of `1/2`, and `R - N = phi + phi'` on
  neighbourhoods of `0` and of `1`.
- (c) `min R = phi` and `min N = -phi'`, so `min R + (n-1) min N = 0`, and
  `f* = min f` in every `A_i`.
- (d) `F_R([0, 1/2]) = F_R([1/2, 1]) = phi`.
- (e) `N(0) = N(1) = -phi'`. Hence `F_N(J) <= -phi'` for every interval `J`
  that contains `0` or `1`.

*Proof.*

- **(a).** `H_R` and `H_N` are maxima of lines. At `1/2`, `lL = lR = 1/2 - c`.
  The floor lines are `1/4 + phi` (for `R`) and `1/4 - phi'` (for `N`).
  - Now `1/2 - c - (1/4 + phi) = 1/4 + eps/2 - nc > 0` by the right half of
    (6.1). So near `1/2` both functions equal `max(lL, lR)`.
  - The convex piecewise-linear function `H - t` has slope `sL - 1 < 0` just
    left of `1/2` and `sR - 1 > 0` just right. So `1/2` is its unique
    minimizer, and the value is `1/2 - c - 1/2 = -c`.
- **(b).** Near `1/2` this follows from (a). Near `0`, the floor lines are
  active in both functions:
  - for `R`, `phi - lL(0) = nc - eps/2 - eps/(8(n-1)) > 0`, which the left
    half of (6.1) implies;
  - for `N`, `-phi' - lL(0) = 3 eps/(8(n-1)) > 0`;
  - also `lR(0) < lL(0)`, and the other floor line is lower by `1/2` at `0`.

  So near `0`, `H_R - H_N = phi + phi'`. The same computation at `1`, with
  the floor lines `3t/2 - 1/2 ± ...` and `lR(1)`, gives the same margins.
- **(c).** `a_{[0,1/2]} + t^2 = t/2` and `a_{[1/2,1]} + t^2 = 3t/2 - 1/2`.
  - So `R = H_R - t^2 >= phi + t(1/2 - t) >= phi` on `[0, 1/2]`, and
    `>= phi + (t - 1/2)(1 - t) >= phi` on `[1/2, 1]`.
  - Equality holds at `0` by (b). `N` is the same with `-phi'`.
- **(d).** By the identities in (c), `phi_{R,[0,1/2]} = H_R - t/2 >= phi`,
  with equality at `0`. Likewise `phi_{R,[1/2,1]} = H_R - 3t/2 + 1/2 >= phi`,
  with equality at `1`.
- **(e).** `N(0) = H_N(0) = -phi'` and `N(1) = H_N(1) - 1 = -phi'`, by (b).
  If `0 in J`, then `F_N(J) <= phi_{N,J}(0) = N(0)`. □

**Exact check** (`separable/lb_coord.py`, `lb_coord.log`), with `eps = 1/100`
and `c = 1/(5n)`, for **every** `n = 2, ..., 40`:

- all items of Lemma 6.1;
- the facts used below: the root is invalid, the right cut leaves children
  with margin exactly `eps/2`, and every wrong-cut child is invalid (by the
  analytic bound and by a sweep over 999 exact cut points).

The agreement neighbourhoods are computed exactly from the knots:

- `R = N` on an interval containing `[0.3906, 0.6094]` for every `n`;
- `R - N` is constant on `[0, a_n]` and `[1 - a_n, 1]`, with
  `a_n = 3/398` (`n = 2`) down to `3/15598` (`n = 40`), about
  `3 eps/(4(n-1))`.

### 6.2 Theorem C: one wrong coordinate

**Theorem C.** Let `n >= 2` and assume (6.1).

- (a) Every deterministic I1 rule has `T >= 7` on some `A_i`, where
  `N_opt = N_guill = 2` and `T_opt = 3`. Its ratio is at least `7/3`.
- (b) Every randomized I1 rule has `E[T] >= 7 - 4/n` on some `A_i`. Its ratio
  is at least `(7 - 4/n)/3`.

*Proof.*

1. **Identical root data.** By Lemma 6.1(a), (b) and (c), every `A_i` has
   the same:
   - root minimizer `(1/2, ..., 1/2)` and root value `-nc`;
   - incumbent `f* = 0`;
   - `f` near the minimizer (all coordinates have `R = N` there);
   - `f` near every corner (there `R - N` equals the same constant in every
     coordinate).
2. **The root is invalid.** `-nc + eps < 0`, since (6.1) gives
   `nc > eps + eps/(2(n-1))`.
3. **The right cut is valid.** In `A_i`, cutting coordinate `i` at `1/2`
   gives children with value
   `phi + (n-1)(-c) + eps = eps/2 >= 0`, by Lemma 6.1(d). So
   `N_opt = N_guill = 2` and `T_opt = 3`.
4. **Every other cut fails twice.** Cutting a coordinate `j ≠ i` at any
   point gives two children, each containing `0` or `1` in coordinate `j`.
   - By Lemma 6.1(e), each has value at most
     `-phi' - c - (n-2) c + eps = -nc + eps + eps/(2(n-1)) < 0`.
   - Both are invalid, each needs at least two children, and `T >= 7`.
5. **Deterministic rules.** The rule must cut the root and cannot tell the
   `A_i` apart. If it cuts coordinate `j`, it has `T >= 7` on every `A_i`
   with `i ≠ j`.
6. **Randomized rules.** Let `p_j` be the probability that the root cut is
   along `j`. Take `i` with `p_i <= 1/n`. Then on `A_i`,
   `E[T] >= 3 p_i + 7(1 - p_i) >= 7 - 4/n`. □

### 6.3 Theorem C': the ambiguity iterates

The first version left open whether the ambiguity can be repeated. The
review answered this, on the same instances. The argument below is the
review's, re-derived and checked here.

**Definitions.**

- A node is a *corner node* if each of its intervals contains `0` or `1`.
- `S(v)` is the set of coordinates whose interval at `v` is not `[0, 1]`
  (the coordinates cut on the way to `v`).
- A coordinate `i` is *free* at `v` if `i` is not in `S(v)`.

**Theorem C' (review).** Assume (6.1) and `nc > 3 eps/2`, which holds for
`eps = 1/100` and `c = 1/(5n)`. Let `G(n)` be the value of the minimax
problem defined in step 7 below. Then:

- (a) every deterministic I1 rule has `T >= 2 G(n) + 1` on some `A_i`, with
  `G(n) >= ceil((2^(n+1) - n - 3)/(n - 1))`. Exactly, `G(2), ..., G(6)` are
  `3, 5, 9, 15, 25` (`G(6)` from the closing audit), which gives ratios at
  least `7/3, 11/3, 19/3, 31/3, 17`;
- (b) every randomized I1 rule has
  `E[T] >= 2 (2^(n+1) - n - 2)/n + 1` on some `A_i`, which gives ratios at
  least `5/3, 25/9, 14/3, 119/15` for `n = 2, ..., 5`.

Both ratios grow like `2^(n+2)/(3n)`.

Two assumptions matter:

- **Coordinate-wise selection** of minimizers (Section 1.1).
- **Node-locality**, as in the I1 model: the rule's decision at a node
  depends only on that node's data, and nothing is carried over from other
  nodes.

A rule with memory across nodes escapes the bound. It can learn `i` the first
time a cut produces two valid children, and then cut `i` first everywhere
else, using `O(n)` nodes on `A_i`. So pseudocost-type rules, which learn
across nodes, are not covered by these exponential lower bounds.

*Proof.*

1. **Identical data at corner nodes.** Let `v` be a corner node, and let
   `i, i'` both be free at `v`.
   - **Tolerance and incumbent.** `eps` is the same, and the incumbent is
     `f* = 0` in both, by Lemma 6.1(c).
   - **Box, value and minimizer.** In `A_i` and `A_{i'}`, every cut
     coordinate carries `N` on the same interval. Every free coordinate is
     `[0, 1]`, where `R` and `N` have the same minimizer `1/2` and value `-c`.
     So the relaxation value and the (coordinate-wise) minimizer agree.
   - **`f` near the minimizer.** Exactly,
     `f_{A_i}(y) - f_{A_{i'}}(y) = (R - N)(y_i) - (R - N)(y_{i'})`. Near
     `y_B`, both `y_i` and `y_{i'}` are near `1/2`, where `R = N`.
   - **`f` near the corners of `v`.** There `y_i, y_{i'}` are near `0` or
     `1`, where `R - N` takes the same constant value.
2. **Invalidity at corner nodes.** `v` is invalid in `A_i` for every free
   `i`.
   - Each cut coordinate contributes at most `-phi' = -c + eps/(2(n-1))`
     (Lemma 6.1(e)), and each free coordinate `-c`.
   - So the value is at most `-nc + eps(1 + |S(v)|/(2(n-1))) <= -nc + 3 eps/2 < 0`.
3. **A reference tree.** Fix a deterministic node-local rule.
   - By step 1, at a corner node its decision is the same in all instances
     for which the node is free of `i`. This is where node-locality is
     used: the decision may depend only on the node's own data.
   - Cutting a free coordinate (at any point) gives two corner children, with
     `S` larger by one.
   - Re-cutting a coordinate in `S` gives one corner child with the same `S`,
     and one child that is not a corner node.
   - So the corner nodes reached from the root form a tree `RT`, determined
     by the rule alone.
4. **Counting in each instance.** By step 2 and induction from the root, for
   every `i` all nodes `v` of `RT` with `i` free are reached and are internal
   in the rule's tree on `A_i`. So `T(A_i) >= 2 N_i + 1`, where `N_i` is the
   number of such nodes.
   - If the rule never stops on some `A_i`, then `T = ∞` and there is
     nothing to prove.
5. **Growth of `RT`.** Let `b_d` be the number of nodes of `RT` with
   `|S| = d` that cut a free coordinate; call them *branching nodes*.
   - Each branching node has two corner children with `|S| = d + 1`.
   - Each child starts a chain of re-cuts, and the chain ends at a branching
     node, unless the rule never stops (step 4).
   - The two children, and children of different branching nodes, root
     disjoint subtrees. So their chains end at distinct branching nodes
     with `|S| = d + 1`.
   - Hence `b_{d+1} >= 2 b_d`. The root is a branching node, since every
     coordinate is free there, so `b_0 = 1`.
   - So `RT` has at least `2^d` nodes with `|S| = d`, for each
     `d = 0, ..., n - 1`. Each is counted in `N_i` for the `n - d` values of
     `i` free at it, which gives
     `sum_i N_i >= sum_{d=0}^{n-1} 2^d (n - d) = 2^(n+1) - n - 2`.
6. **Conclusion.**
   - **(a).** Let `j` be the coordinate cut at the root. It is not free at
     any other node of `RT`, so `N_j = 1`. The maximum of the other `N_i` is
     at least their average, which is at least `(2^(n+1) - n - 3)/(n - 1)`.
     This sharpening is the closing audit's; the plain average gives
     `(2^(n+1) - n - 2)/n`.
   - **(b).** Use Yao's principle with the uniform distribution on
     `{A_1, ..., A_n}`: every deterministic rule has average `T` at least
     `2 (sum_i N_i)/n + 1`.
7. **Exact values of `G(n)`.** `G(n)` is the minimum over trees `RT` of
   `max_i N_i`.
   - Re-cuts only add counted nodes, so it suffices to consider trees in
     which every node cuts a free coordinate, with independent choices in
     the two children.
   - A dynamic program over the set `S`, keeping the Pareto-minimal vectors
     `(N_i)_i`, computes `G(n)` exactly (`thmC_iter.py`). It gives
     `3, 5, 9, 15` for `n = 2, ..., 5`.
   - The closing audit computed `G(6) = 25` with an independent program
     (vector `(1, 19, 25, 25, 25, 25)`), which gives ratio at least 17. This
     note's program did not finish `n = 6` within its time limit. □

**Checks** (`separable/thmC_iter.py`, `thmC_iter.log`).

- **Corner nodes.** 2,000 random corner nodes for each `n = 2, ..., 5`. In
  every free `A_i` they had identical values and minimizers and were
  invalid.
- **Attainment.** Consider the rule that follows an optimal reference tree
  and cuts each free coordinate at `1/2`.
  - Simulated exactly, it attains `T = 2 N_i + 1` on every `A_i`:
    `[3, 7]`, `[3, 11, 11]`, `[3, 15, 19, 19]` and `[3, 23, 31, 31, 31]` for
    `n = 2, ..., 5` (`thmC_iter.log`; `n = 5` in `thmC_sim5.log`).
  - Once coordinate `i` is cut at `1/2`, both children are valid, by
    Lemma 6.1(d) and (e): margin `eps/2 + |S'| eps/(2(n-1))`.
  - So on this family the best deterministic node-local ratio is exactly
    `(2 G(n) + 1)/3` for `n <= 5`. The review (`n <= 4`) and the closing
    audit (`n <= 5`) report the same.

### 6.4 `omega` on these instances

The first version said that `omega` "attains `7/3`" here. That is true only
for `n = 2`.

**Proposition 6.2.** Under the assumptions of Theorem C', on `A_i`, `omega`
with ties to the lowest index uses exactly `2^(i+1) - 1` nodes. In particular
it uses `2^(n+1) - 1` on `A_n`.

*Proof.*

- **At a corner node.** Every free coordinate has `w = 1/4`, at its
  minimizer `1/2`.
- **A cut `N` coordinate.** Its interval is `[0, 1/2]` or `[1/2, 1]`, since
  `omega` cuts at minimizers. There `phi_N` is constant, equal to `-phi'`,
  on the floor segment. That segment runs from the endpoint to the first
  knot, at distance `t_N ≈ 3 eps/(4(n-1))`.
  - Both selections pick the knot end of that segment, so `w <= t_N/2 < 1/4`.
- **The order of cuts.** So `omega` cuts the free coordinates in index order
  at `1/2`, on every branch.
  - Corner nodes are invalid until coordinate `i` is cut (step 2 above).
  - After that, both children are valid (the margin in the attainment check
    above).
- **Count.** `omega` cuts `i` levels of full binary tree, which gives
  `2^i` leaves. □

Exact simulation under both minimizer selections (`lb_coord.log`) gives
`3, 7, ..., 2^(n+1) - 1` on `A_1, ..., A_n` for `n = 2, ..., 5`. The
deficit rule does the same.

**A tie-free variant.** The count is not an artefact of the tie order.

- **The variant.** Replace `R` by `R'`, whose root minimizer is
  `p = 1/2 + 1/50`, with the same root value `-c`:

  ```
  H_R' = max( sL-line and sR-line through (p, p - c),  p t + phi,  (1+p) t - p + phi )
  ```

  - `a_{[0,p]} + t^2 = p t` and `a_{[p,1]} + t^2 = (1+p) t - p`, so cutting
    `R'` at `p` leaves children with value `phi` in that coordinate, as in
    Lemma 6.1(d).
  - The analogue of (a) needs `nc < p(1-p) + eps/2`.
- **Why `omega` loses on every labelling.** At the root, `w_{R'} = p(1-p) =
  156/625 < 1/4 = w_N`. So `omega` strictly prefers every uncut `N`
  coordinate. It cuts all of them first and `R'` last.
- **Count.** It uses `2^(n+1) - 1` nodes on every labelling, while
  `N_opt = 2` and `OPT_min` has 2 leaves (cut `R'` first).
- **Check.** Exact for `n = 2, ..., 5`, under both selections
  (`lb_coord.log`).

**Consequences.**

- **For `omega`.** If Conjecture 1 holds for `omega`, its constant satisfies
  `C_n >= (2^(n+1) - 1)/3`.
- **For Conjecture S1 (Section 7.2).** The constant satisfies
  `C_n >= 2^(n-1)`, in leaves.
- **Comparison.** Theorem C' shows that every I1 rule needs a constant
  exponential in `n`. `omega`'s `(2^(n+1) - 1)/3` is of the same order as
  the minimax bound `(2 G(n) + 1)/3`, larger by at most a factor of about
  `n/2`.

### 6.5 Remarks

- **Scope.** As for Theorem 3 of the main note, these are bounds for
  non-analytic classes. The instances are piecewise quadratic and in the
  convex class, and they agree on open sets without agreeing everywhere.
- **Why this is new to `n >= 2`.** In 1D the only ambiguity is where to
  cut, which costs 2 extra nodes out of 5. Here a wrong coordinate leaves
  both children invalid. Theorem C' shows that this can be repeated in
  every branch, once per dimension.
- **Selection caveat for Theorem C'.** At a corner node, a cut `N`
  coordinate has a flat minimizer segment. A solver that broke such ties
  using `f` far from the minimizer could in principle leak `i`. Theorem C
  is not affected, since its root minimizer is unique.
- **Credit.** Theorem C (every `n`) is this note's; the admissible range
  (6.1) was made explicit after the review. Theorem C' and the tie-free
  variant of Section 6.4 are the review's.

## 7. Toward Conjecture 1 for separable instances

### 7.1 `omega` and the best minimizer rule

The best offline minimizer rule `OPT_min` separates two losses:

- the loss from splitting at relaxation minimizers, measured by
  `OPT_min/N_opt`;
- the loss from `omega`'s coordinate choice, measured by `omega/OPT_min`.

Exact values under the two minimizer selections of Section 1.1. Sources:
`exp2.log`, `exp2_more.log`, `exp3.log`, `tie_rule.log`, `drift_grid.log`,
`propD_redo.log`; grid optima are from the exactly verified DP.

| Family | `eps` range | `omega/OPT_min`, `knot` | `omega/OPT_min`, `proj` | `OPT_min/`grid optimum |
|---|---|---|---|---|
| sharp × quadratic | 1e-3 … 1e-11 (`proj`: to 1e-8) | 1.00 | 1.00 | 1.25–1.91 (both) |
| quadratic × quadratic | 1e-3 … 1e-8 (`proj`: to 1e-7) | 1.00–1.05 | 1.00–1.05 | 1.38–1.55 |
| caps (6 rigid breakpoints) × quadratic | 1e-3 … 1e-8 | 1.00 | 1.33–1.63 | 1.07–1.35 (`knot`) |
| quadratic × (1/20) quadratic | 1e-3, 1e-4 | 1.00 | not rerun | 1.41 |
| quadratic × (1/100) quadratic | 1e-3 … 1e-10 | 1.000–1.007 | not rerun | — |
| dyadic caps × dyadic caps (Prop. D) | 1e-3 … 1e-7 | 1.00 | 1.52–1.82 | `OPT_min` within 1 of the best upper bound |

- **The selection matters on caps families.** On families whose node
  relaxations are flat on whole cells (the caps families), `proj` makes
  `omega` split in the middle of a flat cell. That doubles the subtree below.
  - `OPT_min` and `deficit` are unchanged (`deficit = OPT_min` there under
    both selections).
  - On dyadic caps at `eps = 1e-8, 1e-9, 1e-10`, `omega` under `proj` has
    363, 421 and 544 leaves, against 196, 227 and 290 under `knot`, a factor
    1.85–1.88.
  - Each wasted split doubles one subtree and cannot repeat along a path, so
    the review expects the factor to stay below 2. That is a heuristic.
- **Quadratic-type families** do not have flat segments, and there the two
  selections give identical counts.
- **The first version's summary** ("`omega` within 5% of `OPT_min` on every
  family") holds only under `knot`.

On the anisotropic family (`g = 1/100`, `knot`), `deficit/OPT_min` rises from
1.00 to 1.23 at `eps = 1e-9` and is 1.21 at `1e-10`. That matches the
n-dim note's observation that the deficit rule drifts. The drift comes from
its coordinate choice.

**Searches.** These are hill climbs over instances whose `H` in each
coordinate is a maximum of 5–30 random lines. The `eps` is drawn from
`1e-2 … 1e-8` (`1e-2 … 1e-6` for the grid searches). Each restart takes
60–100 improvement steps.

| Search (restarts) | Objective | Best found |
|---|---|---|
| `search2.py omega`, 6 lines (400) | `omega/OPT_min` | 1.667 (5 leaves against 3) |
| `search2.py omega`, 10 lines (200) | `omega/OPT_min` | 1.500 (12 against 8) |
| `search2.py deficit`, 6 lines (400) | `deficit/OPT_min` | 1.600 (8 against 5) |
| `search.py omega`, 5 lines (300) | `omega/`grid optimum | 2.000 (14 against 7) |
| `search.py omega`, 8 lines (80) | `omega/`grid optimum | 2.000 (10 against 5) |

The best grid-search instances were classified with `classify.py`
(`classify.log`):

| Instance | `omega` | `deficit` | `OPT_min` | grid optimum | slice |
|---|---|---|---|---|---|
| `s1_omega_13` | 14 | 13 | 13 | 7 | 3 |
| `s1_omega_22` | 10 | 8 | 8 | 5 | 4 |
| `s2_omega_21` | 12 | 8 | 8 | 7 | 3 |

- **Where the loss comes from.** In these instances most of the loss is the
  minimizer-split loss: `OPT_min/`grid optimum is up to 13/7 ≈ 1.86. The
  coordinate-choice loss `omega/OPT_min` is up to 1.5.
- **What the searches miss.** The searches (all under `knot`) did not find
  the ambiguity instances of Section 6. Those reach `omega/OPT_min = 2` in
  leaves for `n = 2`, also without ties (the tie-free variant). Random
  instances are far from them.
- **Scope.** No search instance comes close to a growing ratio. The
  instances are small (`N_opt <= 7`), so these searches test constants, not
  growth.

### 7.2 Two conjectures that together give Conjecture 1 (separable case)

- **Conjecture S1 (coordinate choice).** On separable instances,
  `omega <= C_n OPT_min`.
- **Conjecture S2 (split points).** On separable instances,
  `OPT_min <= C_n N_opt`.

- **What is proved.** Theorem B proves both for `n = 2` when one
  coordinate is sharp, since `OPT_min <= omega` and `N_opt <= OPT_min`. The
  sketch after it extends this to `n - 1` sharp coordinates.
- **Lower bound for S1.** The tie-free instances of Section 6.4 show that
  S1 needs `C_n >= 2^(n-1)` in leaves: `omega` has `2^n` leaves, `OPT_min`
  has 2.
- **Growth in `n` is forced.** By Theorem C', a constant in Conjecture 1
  itself must grow at least like `2^(n+2)/(3n)` for every I1 rule, and like
  `(2^(n+1) - 1)/3` for `omega`.
- **Data.** In `n = 2` the data above suggest small constants for both
  conjectures. Under `proj` on caps families, the S1 ratio approaches 2.

### 7.3 Where the proof stops

By Corollary A', every `omega` node lies in a phase `P` that has at most
`24 n_P` nodes. So a proof for separable 2D instances would follow from:

- **Conjecture S3 (phase accounting).** `sum_P n_P <= C N_opt`, or the
  weaker `sum_P N_{A_P}(b_P) <= C N_opt`, summed over the phases of `omega`.

Evidence and obstacles:

- **Measured sums.** `sum_P N_{A_P}(b_P)` is about twice `omega`'s number of
  internal nodes and about 2.5 times the grid optimum on
  quadratic × quadratic (132 against 51 at `1e-8`, `exp6.log`).
  - On the grid-optimal certificate, a box meets at most 4–9 phase segments,
    and `sum_P n_P` is 2.2–4.9 times the certificate size (`exp4.log`, three
    families, `eps = 1e-3 … 1e-8`).
  - There is no clear growth over this range. The quadratic × quadratic
    values drift slightly, from 3.6 to 4.8–4.9. No proof is known.
- **Where overcounting could arise.** The natural way is for many phases to
  cross the same certificate box. That happens along a long chain of
  alternating one-split phases (a spiral) toward a corner of the
  certificate. Three observations bear on such chains:
  - the first, a proof sketch, excludes them near edge points;
  - the second explains why that argument fails at corners;
  - the third, a heuristic, suggests that corners are still harmless in the
    convex class.
  - **Near an edge point** of a certificate facet, consider nodes whose other
    interval lies inside both neighbouring boxes' ranges. Those two boxes
    then give the crossing coordinate compatible budgets. So Lemma 2 of the
    main note, applied to the crossing coordinate, allows at most one wasted
    split on each side. Each phase there is `O(1)` by Corollary A'.
  - **At corners** the budgets are incompatible: the crossing node's other
    interval sticks out of the neighbouring box. The 1D lemma then only
    gives the weakened inequality of the main note's Section 6.2.
  - **In the convex class**, the relaxation minimizer of a 1D interval is the
    proximal point of its centre. A chain converging to a point where `m`
    vanishes is captured in finitely many steps by the kink that validity of
    the adjacent boxes forces there. This was argued for specific
    configurations but not proved in general.
- **Why accumulation seems hard (heuristic).** The natural accumulation
  scenario is a certificate with `r` stacked boxes on one side and `c` tall
  boxes on the other. It could make `omega` pay `r·c` against `r + c`. In
  the configurations worked through, the coordinate rule itself blocks it:
  - To start the product, `omega` would have to refine the other coordinate
    first, across the region of the tall boxes.
  - The tall boxes need a surplus in their own coordinate that is fragile at
    scale `1/c`. A small, fragile surplus on a wide interval forces a central
    relaxation minimizer in that coordinate, hence a large `w` there.
  - So `omega` refines that coordinate first and never forms the product.

  This was checked by hand for a few configurations, not proved. The phase
  lemma alone does not capture it; a proof of S3 would have to.

## 8. Computations

All scripts are in [`separable/`](separable/) and were run from there with
single-threaded Python 3 and exact `fractions`. The only floating-point
component is the guillotine DP in `gdp_sep.c`, compiled with
`gcc -O2 -shared -fPIC -o libgdp_sep.so gdp_sep.c`.

- **What the DP does.** It works on candidate grids with a conservative
  guard (`F_1 + F_2 + eps >= 1e-13`). The grids contain `omega`'s cuts and
  the greedy 1D breakpoints at budgets `eps·2^k`.
- **Exact verification.** The optimal certificate is reconstructed and every
  box is re-verified in exact arithmetic (`sepexact.guill_grid`).
- **Reading the numbers.** A grid optimum is an upper bound on `N_guill`, so
  ratios against it are lower bounds on the true ratio.
- **Memory.** At most about 150 MB: grids of at most 60 points per axis, and
  41 × 200 for `drift_grid.py`.
- **Minimizer selection.** Every script uses `knot` (Section 1.1) unless it
  says otherwise. `tie_rule.py`, `propD_redo.py` and `lb_coord.py` run both
  `knot` and `proj`.

| Command | Output (log) | Used in |
|---|---|---|
| `python3 exp1.py sharp_quad 60` | grid optimum, slice, product, `omega`, `deficit`, charges per box (`exp1.log`) | Section 5 |
| `python3 exp2.py sharp_quad 50`, `python3 exp2.py quad_quad 50`, `python3 exp2.py caps_quad 50`, `python3 exp2.py quad_flatquad 50` | `omega`, `OPT_min`, grid optimum (`exp2.log`, `exp2_more.log`; the last run stopped at `eps = 1e-5`, where the thinned grid admitted no certificate) | Section 7.1 |
| `python3 exp3.py 1/100` | anisotropic `omega`, `deficit`, `OPT_min` to `eps = 1e-10` (`exp3.log`) | Section 7.1 |
| `python3 exp4.py {sharp_quad,quad_quad,caps_quad} 50` | phase segments per certificate box (`exp4.log`) | Section 7.3 |
| `python3 exp5.py` | first-version Proposition D numbers, with a knot interpolant of `q` (`exp5.log`); superseded by `propD_redo.py` | — |
| `python3 propD_redo.py` | Proposition D numbers with the exact `q` (`QuadCoord`), product certificates for `g ⊕ g`, `omega` under both selections, and the proof's lower bound (`propD_redo.log`) | Section 3.3 |
| `python3 exp6.py {quad_quad,sharp_quad}` | `sum_P N_{A_P}(b_P)` (`exp6.log`) | Section 7.3 |
| `python3 phase_check.py 3000 1`, `python3 phase_check.py 3000 2` | Lemma T and Theorem A, 6,000 instances, all assertions passed (`phase_check.log`) | Section 4 |
| `python3 chainlp3.py k 30000 k` for `k = 1, 2, 3` | longest feasible chains 2, 3, 3 (`chainlp3.log`) | Section 4 |
| `python3 thmB_check.py 2000 5` | Theorem B on 2,000 random instances, all assertions passed (`thmB_check.log`) | Section 5 |
| `python3 exp7.py 60` | sharp × quadratic at `eps = 1e-9, 1e-10, 1e-11`, first-version grids (`exp7.log`) | Section 5 |
| `python3 drift_grid.py 200` | sharp × quadratic with strip-adapted grids (the review's recipe), exactly verified (`drift_grid.log`) | Section 5 |
| `python3 deficit_phase.py` | the deficit-phase counterexample (`deficit_phase.log`) | Section 4.3 |
| `python3 lb_coord.py $(seq 2 40)` | Lemma 6.1 and Theorem C for every `n = 2, ..., 40` with `c = 1/(5n)`, all items hold. For `n <= 5` also `omega` and `deficit` on every `A_i` under both selections, `OPT_min` (`n = 2`), and the tie-free variant (`lb_coord.log`; the same run restricted to `n = 2, ..., 5` is in `lb_coord_small.log`) | Section 6 |
| `python3 thmC_iter.py 5 4 2000` | Theorem C': corner-node checks, `G(n)` by the Pareto DP, the averaging bounds, and an explicit rule attaining `2 G(n) + 1` for `n <= 4` (`thmC_iter.log`) | Section 6.3 |
| inline `best_tree(5)` and `simulate` from `thmC_iter.py` | the explicit rule attains `2 G(5) + 1 = 31` (`thmC_sim5.log`) | Section 6.3 |
| inline `G(6)` from `thmC_iter.py`, with a 1,500 s limit | did not finish; `G(6) = 25` rests on the closing audit (`thmC_G6.log`) | Section 6.3 |
| `python3 tie_rule.py FAMILY KMIN KMAX` for `caps_quad 3 8`, `sharp_quad 3 8`, `quad_quad 3 7`, `dyadic_caps 3 7`, plus an inline `omega`-only run on dyadic caps at `1e-8 … 1e-10` | `omega`, `deficit`, `OPT_min` under `knot` and `proj` (`tie_rule.log`) | Sections 3.3, 7.1 |
| `python3 search2.py omega 100 11 6 400`, `python3 search2.py deficit 100 12 6 400`, `python3 search.py omega 60 13 5 300` | searches (`s2_omega_11.log`, `s2_deficit_12.log`, `s1_omega_13.log`) | Section 7.1 |
| `python3 search2.py omega 100 21 10 200`, `python3 search.py omega 60 22 8 80` | larger-instance searches (`s2_omega_21.log`, `s1_omega_22.log`) | Section 7.1 |
| `python3 classify.py LOG` for the three grid-search logs | `omega`, `deficit`, `OPT_min`, grid optimum, slice of the best instance (`classify.log`) | Section 7.1 |

Scratch scripts `chainlp.py`, `chainlp2.py` and `chainlp4.py` are LP
feasibility probes for chains around a breakpoint. They informed Lemma T and
Section 7.3, and their outputs are quoted only qualitatively.

## 9. Open questions

1. Conjectures S1, S2 and S3 (Section 7), and hence Conjecture 1 for
   separable instances, first in `n = 2`.
2. The exact best deterministic ratio of I1 rules in `n >= 2`.
   - It is at least `(2 G(n) + 1)/3`, with `G(2..6) = 3, 5, 9, 15, 25`,
     which is about `2^(n+2)/(3n)` (Theorem C').
   - It is exactly that on the family of Section 6 for `n <= 5`.
   - Is some I1 rule `2^(O(n))`-competitive on separable instances? Can
     other families force a faster growth?
   - Combining the position ambiguity of the main note's Theorem 3 with the
     coordinate ambiguity of Theorem C would raise the randomized 2D bound
     to `11/6`, by a minimax computation, if suitable instances exist. None
     were constructed.
3. A characterization of `N_opt` for separable instances up to constants,
   in terms of the interval functions `F_i` (Proposition D rules out the
   sizes `N_i` alone). A candidate is a multiscale "budget field": a
   partition of the axes into dyadic scales with per-scale budget splits.
4. The deficit rule on anisotropic quadratics: does `deficit/OPT_min` stay
   bounded (it was 1.21–1.23 at `eps <= 1e-9`)?
5. Non-convex separable instances. Theorems A and B hold for them.
   Section 7.3's heuristic against spirals uses convexity.
6. The effect of the minimizer selection. Is `omega` under `proj` within a
   factor 2 of `omega` under `knot` on every separable instance? (The review
   gives a heuristic.)

## 10. Revision after review (2026-09-29)

The review [`../../reviews/separable-omega-review.md`](../../reviews/separable-omega-review.md)
confirmed:

- Lemma 2.1 and the phase containment;
- Lemma T, Theorem A and Theorem B;
- Proposition D (a)–(c) and Lemma 3.2;
- the `n = 2` proof of Theorem C and its information model.

Each item below was re-derived and rechecked with this note's own scripts
before it was changed.

| Review item | Change |
|---|---|
| Theorem C proved only for `n = 2`; the script's `r0 = (n-1)/(4n) + 1/50` fails for `n >= 12` | New Section 6.1: admissible range (6.1) for `c = 1/4 - r0`, derived here; Lemma 6.1 and Theorem C proved for every `n`; `c = 1/(5n)` (the review's choice) checked exactly for `n = 2, ..., 40` (`lb_coord.log`). The exact agreement intervals are now computed from the knots (the first grid-based detection missed the corner interval, which is narrower than `1/2000`, from `n = 17` on) |
| The ambiguity iterates (review's Proposition C+) | Included, with credit, as Theorem C' (Section 6.3). Proof written out; `G(n)` recomputed by an independent Pareto DP, corner nodes checked, attainment by an explicit rule for `n <= 4` (`thmC_iter.log`). Question 2 of Section 9 revised |
| "`omega` itself attains `7/3`" is false for `n >= 3` | Replaced by Proposition 6.2 (`2^(i+1) - 1` nodes on `A_i`, with proof) and the tie-free variant (`2^(n+1) - 1` on every labelling), both checked exactly for `n <= 5` under both selections. Consequences for Conjecture 1 and S1 in Sections 6.4 and 7.2 |
| `deficit` "competitive within a phase (Theorem A)" is false | Withdrawn. New Section 4.3 with the review's counterexample, re-derived with `QuadCoord` (`deficit_phase.log`) |
| Corollary A': formula gives `-1` at `n_P = 1`; case `tau = 0` outside Theorem A | Both cases stated and proved (Section 4.2); `tau = 0` via Theorem 1' |
| "Answers (2)" overstated Theorem B | Now: both rules in 2D (Theorem B); `n - 1` sharp coordinates only sketched, for `omega` only. Sketch now counts `3^(n-1)` states |
| Drift "levels off near 1.5"; "1.47 at `1e-11`"; "`omega`/slice at most 2.9" | Strip-adapted grids (the review's recipe) recomputed with this note's DP and verified exactly (`drift_grid.log`): 1.71–1.91 for `eps <= 1e-6`, 1.91 at `1e-11`, which is the n-dim note's value. `omega`/slice at most 3.0. Summary and Section 5 corrected |
| Tie rule: the code used minimizing knots and endpoints only, not the stated rule; under the stated rule `omega/OPT_min` is 1.33–1.59 on caps × quadratic, and dyadic caps are 1.5–1.9 times larger | Both selections now implemented (`Coord.sel`), described in Section 1.1, and rerun (`tie_rule.log`): caps × quadratic 1.33–1.63 (to `1e-8`), dyadic caps 1.52–1.82 (to `1e-7`) and 1.85–1.88 (`1e-8` to `1e-10`, `omega` only). Summary item 6 and Section 7.1 corrected |
| Proposition D(d) too strong; table used an interpolant of `q`; `g ⊕ g` grid optima not optimal | Qualifier added (formulas insensitive to bounded factors). Table redone with the exact `q` and product certificates (`propD_redo.log`), including the proof's lower bound 4, 7, 10, 14, 20 |
| Minor: coordinate-wise selection assumption; facets not covered by Theorem C; grid ratios are lower bounds on the loss | Stated in Sections 1.1, 6 and Summary item 6 |

**What did not change.** The review's own scripts were not reused. The
unrechecked parts of Section 7 are unchanged and still labelled as evidence
or heuristics:

- the searches;
- the phase-accounting statistics;
- the anisotropic deficit drift;
- the corner discussion.

No project-wide checks were run and CI was not inspected.

**Closing audit (2026-09-29).** The closing audit
[`../../reviews/closing-audit-a.md`](../../reviews/closing-audit-a.md)
(item 2) confirmed the following:

- Theorem C for every `n >= 2` with `c = 1/(5n)`;
- Theorem C' in the node-local I1 model;
- Proposition 6.2 and the tie-free variant.

It reproduced `G(2..5)` and computed `G(6) = 25`. Changes made in response:

| Audit item | Change |
|---|---|
| Theorem C' referred to "step 5" for `G(n)` | Now "step 7", where `G(n)` is defined |
| Step 5's claim that each node leads to a distinct branching node is not injective (nodes on one re-cut chain lead to the same node) | Rewritten as a count of branching nodes: `b_{d+1} >= 2 b_d`, `b_0 = 1` |
| Node-locality should be explicit | Added to the statement of Theorem C' and to step 3. A rule with memory across nodes, such as a pseudocost-type rule, escapes the bound with `O(n)` nodes on `A_i` |
| Step 1 should mention the incumbent | Added (`f* = 0` in every `A_i`) |
| Optional: `N_j = 1` for the root's cut coordinate | Used in step 6: `G(n) >= ceil((2^(n+1) - n - 3)/(n - 1))`, credited to the audit |
| New value `G(6) = 25` | Added to Theorem C'(a), credited to the audit. It is not reproduced here: this note's dynamic program, which has no pruning cap, did not finish within 1,500 s (`thmC_G6.log`) |
| Attainment extends to `n = 5` | Reproduced here: `T(A_i) = [3, 23, 31, 31, 31]` (`thmC_sim5.log`) |

No project-wide checks were run and CI was not inspected. Nothing was
committed.
