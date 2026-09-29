# Competitive node-local branching in spatial branch-and-bound

Workstream `branching-competitiveness/` of the
[bb-complexity program](../PROGRAM.md). Date: 2026-09-28, revised
2026-09-29 after the independent review
[`../../reviews/competitive-review.md`](../../reviews/competitive-review.md).
Status: first-pass proofs with exact-arithmetic and floating-point checks. The
review verified the main proofs and found the errors listed in Section 10,
which are corrected in place. The `n`-dimensional continuation is in
[`n-dimensional.md`](n-dimensional.md).

Question (from Q1(b) of the [scout report](../../scouting/spatial-bb-theory.md)):
uniform bisection is within `C_n log(1/eps)` of the optimal certificate
(Theorem A there), and the log factor is attained at sharp minima. Is there a
node-local branching rule whose tree is within a constant factor of optimal on
every instance, or does every node-local rule lose a growing factor on some
instances?

## Summary

The answer depends on what the rule may see. The main case is a rule that
sees the node's relaxation solution: the box, the relaxation value, a
relaxation minimizer, the incumbent, the tolerance, and the germ of `f` at
the minimizer (its values on some small neighbourhood). For relaxations whose gap is exactly `alpha q_B` (uniform alphaBB,
or secants of `-alpha y^2`), the one-dimensional answer is positive and
sharp up to a constant:

- **Theorem 1 (upper bound, 1D).** Splitting at the relaxation minimizer, with
  no safeguard and no midpoint mixing, gives at most `8 N_opt - 9` nodes
  (`N_opt >= 2`). The optimal tree has `2 N_opt - 1` nodes, so the ratio is
  below 4 on every instance. The rule wastes at most 3 splits inside each
  interval of any certificate. The proof uses neither convexity of the
  relaxation nor any property of `f` beyond continuity.
- **Proposition 2 (due to the review).** When `N_opt = 2`, the rule uses at
  most 5 nodes, so it is exactly `5/3`-competitive on such instances. The
  review also found an instance with `N_opt = 3` and `T = 11`, so the worst
  ratio of the rule lies in `[11/5, 4)`.
- **Theorem 3 (lower bound, 1D, non-analytic classes).** Every
  deterministic rule with the same information has ratio at least 5/3, and
  randomized rules at least 4/3 in expectation. The proof is an explicit pair
  of piecewise-quadratic instances, checked in exact rational arithmetic. They
  agree on a neighbourhood of the relaxation minimizer and of both box
  endpoints, yet have different unique optimal breakpoints.
  - **Scope.** The bound concerns non-analytic function classes. For
    real-analytic `f`, for example polynomials, knowing `f` near one point
    determines `f`. The information model then collapses to full information,
    where the ratio is 1.
  - The best achievable ratio for piecewise-quadratic classes lies in
    `[5/3, 4)`.
- **Proposition 4 (safeguards hurt).** Consider the family "clamped convex
  combination of the relaxation minimizer and the midpoint" with fixed
  parameters. It contains Couenne's default `(0.25, 0.05)` and the ANTIGONE
  and BARON settings tabulated by Speakman–Lee. In this family only the pure
  minimizer rule (weight 1, clamp 0) has a bounded ratio. Every other member
  needs at least order `log(1/eps)` nodes on a fixed sharp instance with
  `N_opt = 2`.
- **Proposition 4' (SCIP 10's actual default).** SCIP's rule depends on the
  node width, so it is not in that family. On the explicit instance
  `f = 2 alpha |y - 3/238|` it still needs at least order `log(1/eps)` nodes,
  while `N_opt = 2`.
  - The persistent 0.2 clamp causes this.
  - Without the clamp, the vanishing midpoint pull alone gives much slower
    growth (numerically about `log log(1/eps)`).
- **Theorem 2 (oblivious rules, any n).** A rule whose split depends only on
  the box has ratio at least `c_n log(1/eps)`. So Theorem A is tight in
  order for every oblivious rule, not only for bisection.
- **Proposition 0 (full information, 1D).** With oracle access to `f` on the
  node box, a greedy rule is exactly optimal. The model must therefore restrict
  information for the question to be non-trivial.

**Originality is modest** (Section 8). Hansen–Jaumard–Lu (1991) already
proved that a node-local "split at the node bound's minimizer" rule is
constant-competitive in 1D, for Lipschitz bounds. The closest
competitive-analysis precedents are Daskalakis–Diakonikolas–Yannakakis (the
chord algorithm) and Baran–Demaine–Katz. What is new here is the transfer to
quadratic-gap relaxations, with a new proof, the solver-rule results, and
the `n`-dimensional negative result.

In `n >= 2` dimensions the positive question is **open**. Theorem 2 and the
constructions of Proposition 4 carry over. The 1D proof does not: its key
inequality involves one coordinate in 1D and a sum over coordinates in `n`
dimensions. Section 6 states the obstruction and a conjecture.

The continuation [`n-dimensional.md`](n-dimensional.md) adds:

- a proof that splitting all coordinates at the minimizer (`multi`) is not
  competitive;
- exact comparisons against guillotine optima on grids;
- the guillotine-overhead question.

Checks run:

- **Exact rational verification** of Theorem 3's instances, of Propositions
  4 and 4', and of Theorem 2's adversary. The Theorem 2 script was corrected
  after the review.
- **Floating-point check** of Theorem 1's per-interval bound on about 5,900
  instances. The bound was attained and never exceeded.
- **Other checks:** LP feasibility tests of long chains, searches for bad
  instances, and 2D separable runs.
- **The review's own checks:** exact searches over about 40,000 instances.

Commands and outputs are in Section 7. No project-wide checks were run.

## 1. Model

### 1.1 Instances and relaxations

- Root box `X0 = prod_i [L_i, U_i]`, objective `f` continuous on `X0`,
  optimal value `f* = min f`, no other constraints.
- **Exact-gap relaxation (G=).** For a box `B = prod [l_i, u_i]`, let
  `q_B(y) = sum_i (y_i - l_i)(u_i - y_i)` and `f_B = f - alpha q_B` with a fixed
  `alpha > 0`.
  - `f_B` is convex on every box iff `f + alpha |y|^2` is convex. Examples are
    uniform alphaBB and `g - alpha sum y_i^2` with `g` convex, relaxed by
    secants. In the scout's two-sided hypothesis this is the case
    `alpha = alpha'`.
  - Convexity is used only in Proposition 1. It is not used in Theorem 1.
- The node lower bound is `LB(B) = min_B f_B`. A relaxation minimizer is any
  `y_B` in `argmin_B f_B`.

### 1.2 Branch-and-bound runs

- Tolerance `eps > 0`. The incumbent is fixed at `f*`, so the set of processed
  nodes does not depend on the node order. Section 4.1 treats other
  incumbents.
- A node `B` is **pruned** iff `LB(B) >= f* - eps`. Write
  `m = f - f* + eps`, so `m >= eps > 0`. Then `B` is pruned iff
  `phi_B := m - alpha q_B >= 0` on `B`; such a box is called **valid**.
- A non-pruned node is split by one axis-parallel cut through its interior into
  two children.
- `T` is the number of nodes, which equals the number of relaxations solved.
  In binary trees `T = 2 (#internal nodes) + 1`.
- No bound tightening is used. The scout's Lemma 0 covers tightening for lower
  bounds; it is not needed here.

### 1.3 Certificates and the benchmark

- A **certificate** is a partition of `X0` into finitely many valid boxes.
  `N_opt` is the least number of boxes in a certificate.
- Validity passes to sub-boxes: `B' ⊆ B` implies `q_{B'} <= q_B` on `B'`.
- In 1D, every certificate with `N` intervals is the leaf set of a tree with
  `2N - 1` nodes, and the leaves of every finished tree form a certificate. So
  the best possible tree has `T_opt = 2 N_opt - 1` nodes.
- In `n` dimensions trees produce only guillotine partitions, so
  `T_opt = 2 N_guill - 1 >= 2 N_opt - 1`, where `N_guill` is the least size of
  a guillotine certificate.

### 1.4 Node-local rules and information models

A node-local rule maps what is observed at a node to a split (coordinate and
point). Nothing from other nodes is used. Three information models:

| Model | What the rule sees at node `B` |
|---|---|
| I0 (oblivious) | the box `B` (and its depth) |
| I1 (relaxation solution) | `B`, `alpha`, `eps`, the incumbent value, `LB(B)`, a relaxation minimizer `y_B` chosen by a fixed deterministic solver, and the **germ** of `f` at `y_B` (hence all its derivatives there) |
| I_inf (node oracle) | `f` on all of `B` |

Rules are deterministic unless stated otherwise. The **competitive ratio** of
a rule `R` on a class of instances is `sup T_R / T_opt`. The supremum is over
the instances `f` in the class and the tolerances `eps > 0`.

**Meaning of "germ".** Two instances that agree on some neighbourhood of
`y_B`, however small, give the rule the same I1 data. The neighbourhood is not
of a prescribed size.

- The first version wrote "`f` on a neighbourhood of `y_B`". Read literally,
  that allows the whole open box, which would make I1 equal to I_inf for
  every `f`. The recheck pointed this out.
- Theorem 3 names the sets the rule may see, so it is unaffected.

**Scope of I1 (added after the review).** The germ of `f` at `y_B`
determines a real-analytic `f`, including every polynomial, on the whole box
(identity theorem). So for analytic classes, I1 carries as much information as I_inf. This
is an information-theoretic statement; computing the greedy split is a global
optimization problem.

- Results that use only the minimizer (Theorem 1, Propositions 2, 4, 4') are
  unaffected.
- Theorem 3 is a lower bound over non-analytic classes: continuous
  piecewise-quadratic `f` with `f + alpha y^2` convex, and `C^inf` `f` after
  the mollification argued in Section 5.3.
- A finite jet of order at least the degree also determines a polynomial.
  So a lower bound for polynomial classes needs a jet of order below the
  degree, and different instances. That case is open.

### 1.5 Rules considered

- `R_min`: split at the relaxation minimizer, `s = y_B` (1D).
- `R_{lambda,theta}`: split at
  `clip(lambda y_B + (1 - lambda) mid(B), l + theta w, u - theta w)`, with
  `w = u - l`, `lambda in [0,1]` and `theta in [0, 1/2)`.
  - `R_{1,0} = R_min`, and `lambda = 0` gives bisection.
  - The first version of this note attributed `(1, 0.2)` to SCIP and
    `(0.25, 0.2)` to Couenne, following the Speakman–Lee table. Both are
    corrected. Sources are the review's reading of the source code, and the
    root coordinator's check of the parameter values with pyscipopt on SCIP
    10.0.2:
    - **SCIP 10** uses `branching/midpull = 0.75`,
      `branching/midpullreldomtrig = 0.5` and `branching/clamp = 0.2`.
      - The pull `mu` toward the midpoint is `0.75`, and is multiplied by
        `r = w / (global width)` when `r < 1/2`.
      - The split is `clip(mu mid + (1 - mu) y_B, l + 0.2 w, u - 0.2 w)`.
      - The relative width `r` uses the variable's **global** bounds. The
        clamp uses the **local** (node) bounds.
      - So SCIP behaves as `(0.25, 0.2)` on nodes of at least half the global
        width. Below that it behaves as `(1 - 0.75 r, 0.2)`, approaching
        `(1, 0.2)` as nodes shrink.
      - This width-dependent rule, called `R_SCIP` here, is not in the fixed
        family. Proposition 4' treats it.
      - The recheck
        [`../../reviews/competitive-recheck.md`](../../reviews/competitive-recheck.md)
        confirmed this against the SCIP v10.0.2 source (`branch.c`).
    - **Couenne** by default uses the midpoint mode with
      `branch_midpoint_alpha = 0.25` and clamp `0.05`, that is
      `(0.25, 0.05)`, and raises the weight toward 1 at small relative gaps.
      Per-operator overrides were not checked.
    - The Speakman–Lee table also lists ANTIGONE `(0.75, 0.10)` and BARON
      `(0.70, 0.01)`.
- In `n` dimensions, `omega` splits at `y_B` along a coordinate maximizing
  `a_i(y_B) = (y_{B,i} - l_i)(u_i - y_{B,i})`. `multi` splits every coordinate
  with `a_i(y_B) > 0` at `y_B`.

## 2. Results at a glance

| Model | 1D | `n` dimensions |
|---|---|---|
| I0 | ratio at least `c log(1/eps)` for every rule (Theorem 2); bisection at most `C log(1/eps)` (scout Theorem A, which assumes a cube root box and `F = X0`) | same lower bound, `c_n log(1/eps)` (Theorem 2) |
| I1 | `R_min` below 4 (Theorem 1), worst case in `[11/5, 4)` (review), exactly `5/3` when `N_opt = 2` (Proposition 2); every rule at least 5/3 on piecewise-quadratic classes (Theorem 3); every fixed `R_{lambda,theta} ≠ R_min` and SCIP's default at least order `log(1/eps)` (Propositions 4 and 4') | open (Conjecture 1); lower bounds of Theorem 2 and Proposition 4 transfer; `multi` is not competitive ([`n-dimensional.md`](n-dimensional.md)) |
| I_inf | ratio exactly 1 (Proposition 0) | ratio 1 against `T_opt = 2 N_guill - 1` (Section 6.3). Against `2 N_opt - 1` the ratio is the guillotine overhead. In 2D, `N_guill <= 2 N_opt - 1`, so the overhead is below 2. For `n >= 3`, `N_guill = O(N_opt^((n+1)/3))`. Both are published binary-space-partition bounds, known here from abstracts. The overhead is also at most `C_n log(1/eps)` by Theorem A, for a cube root box ([`n-dimensional.md`](n-dimensional.md), Section 4) |

## 3. One-dimensional structure

This section explains why the relaxation minimizer carries the right
information. Theorem 1 does not depend on it.

**Proposition 1.** Let `n = 1`, let `f + alpha y^2` be convex on
`X0 = [L, U]`, and let `m = f - f* + eps`. For `c in X0` define

```
M(c) = min_{y in X0} [ m(y) + alpha (y - c)^2 ],      rho(c) = (M(c)/alpha)^(1/2),
P(c) = argmin_{y in X0} [ m(y) + alpha (y - c)^2 ]    (proximal set).
```

For every interval `B = [c - r, c + r] ⊆ X0`:

- (a) `B` is valid iff `r <= rho(c)`.
- (b) If `B` is invalid, then `P(c) ∩ B` is non-empty, and the set of
  relaxation minimizers of `B` equals `P(c) ∩ B`.
- (c) `rho` is 1-Lipschitz.
- (d) A partition of `X0` with breakpoint set `S` (containing `L` and `U`) is
  a certificate iff `dist(x, S) <= rho(x)` for every `x in X0`.

*Proof.*

1. **Reduction to one convex function.** On `B`,
   `phi_B(y) = m(y) - alpha (r^2 - (y-c)^2) = g_c(y) - alpha r^2`, where
   `g_c(y) = m(y) + alpha (y-c)^2 = [f(y) + alpha y^2] - 2 alpha c y + const`.
   So `g_c` is convex on `X0`.
2. **Case `P(c) ∩ B` non-empty.** Then `min_B g_c = M(c)`. So `B` is valid
   iff `M(c) >= alpha r^2`, and `argmin_B phi_B = P(c) ∩ B`.
3. **Case `P(c) ∩ B` empty, first half.** Say `P(c)` lies to the right of `B`.
   A convex function is nonincreasing to the left of its minimizers, so
   `min_B g_c = g_c(c + r) = m(c + r) + alpha r^2 > alpha r^2`. Hence `B` is
   valid.
4. **Case `P(c) ∩ B` empty, second half.** Take `p in P(c)`. Then
   `M(c) = g_c(p) >= alpha (p - c)^2 > alpha r^2`. So both sides of (a) hold.
   Steps 2–4 prove (a); step 2 with (a) proves (b).
5. **Part (c).** For each `y`, the map `c -> (m(y)/alpha + (y-c)^2)^(1/2)` is
   1-Lipschitz, being the Euclidean norm of `((m(y)/alpha)^(1/2), y - c)`.
   `rho` is their pointwise minimum.
6. **Part (d), "if".** A piece `[s_k, s_{k+1}]` with centre `c` and
   half-width `r` has `dist(c, S) = r`. So `r <= rho(c)`, and the piece is
   valid by (a).
7. **Part (d), "only if".** If `x` lies in a valid piece with centre `c`,
   then `dist(x, S) <= r - |x - c| <= rho(c) - |x - c| <= rho(x)` by (a) and
   (c). □

Consequences:

- **Covering reformulation.** The 1D certificate problem is a
  variable-radius covering. The breakpoints must form a `rho`-net:
  `dist(x, S) <= rho(x)` for all `x`.
- **Minimizers are proximal points.** An invalid node's relaxation minimizer
  is a global proximal point of `m` at the node centre.
  - Where `rho` is differentiable, `y_B = c - rho(c) rho'(c)`.
  - For a sharp minimum `m = eps + sigma |y - a|`, `P(c) = {a}` whenever
    `|c - a| <= sigma/(2 alpha)`. So `R_min` finds the kink from any
    sufficiently centred node.
  - For a smooth minimum `m = eps + gamma (y - a)^2`,
    `P(c) = (alpha c + gamma a)/(alpha + gamma)`. Here
    `rho(c)^2 = eps/alpha + (gamma/(alpha+gamma)) (c-a)^2`. So `R_min` shrinks
    nodes around `a` geometrically, with a ratio adapted to `gamma/alpha`,
    which is how the optimal certificate behaves.
- **Why the result is special to 1D.** For `n >= 2`, only the "if"
  direction of (a) survives.
  - In every dimension, `q_B(y) = |r|^2 - |y - c|^2`. So
    `min_B phi_B >= M(c) - alpha |r|^2`, and `|r| <= rho(c)` still implies
    validity.
  - The "only if" direction fails: a valid box can have `M(c) < alpha |r|^2`.
  - (b) fails too: an invalid box may have its constrained minimizer on a
    facet while the global proximal point lies outside the box.
  - Explicit examples are in [`n-dimensional.md`](n-dimensional.md),
    Section 2.1. The first version said "(a) fails"; the recheck made this
    precise.

## 4. Theorem 1: the relaxation-minimizer rule is 4-competitive in 1D

**Theorem 1.** Let `n = 1`. Assume the exact-gap relaxation, `eps > 0`, the
incumbent `f*`, and `f` continuous. Let `P` be any certificate with
`N >= 2` intervals. Then `R_min`, with any choice of minimizer at each node,
terminates with:

- at most `3` split points in the interior of each interval of `P`, and at
  most `1` in each of the two end intervals;
- at most `4N - 5` internal nodes;
- `T <= 8N - 9` nodes.

With `P` optimal, `T <= 8 N_opt - 9 < 4 (2 N_opt - 1) = 4 T_opt`. If
`N_opt = 1` the root is pruned and `T = 1`.

Notation: `P` has breakpoints `L = s_0 < s_1 < ... < s_N = U` and intervals
`J_j = [s_{j-1}, s_j]`. For a node `B`, write `B = [l_B, u_B]` and let `y_B` be
its split point.

**Lemma 1 (basic facts).**

- (i) Every internal node `B` has `y_B in (l_B, u_B)`.
- (ii) Distinct internal nodes have distinct split points.
- (iii) If `y_B in int J_j`, then `B` contains `s_{j-1}` or `s_j` in its
  interior.
- (iv) Two nodes whose interiors share a point are nested.

*Proof.*

- (i) `phi_B(l_B) = m(l_B) > 0` and likewise at `u_B`. Since
  `min_B phi_B < 0`, every minimizer is interior.
- (ii) Nested nodes: a proper descendant lies in one child, which has `y_B` as
  an endpoint. Nodes with disjoint interiors cannot share an interior point.
- (iii) `B ⊆ J_j` would make `B` valid. An interval containing `y_B > s_{j-1}`
  that is not inside `J_j` has `l_B < s_{j-1}` or `u_B > s_j`. In the first
  case `s_{j-1} in (l_B, y_B)`; the second case is symmetric.
- (iv) This is the tree property. □

**Lemma 2 (at most one split on each side of a breakpoint).** Let
`s = s_{j-1}` be an interior breakpoint and `J = J_j = [s, s']`, with
`lambda = s' - s`. Let `B1 ⊋ B2` be internal nodes that both contain `s` in
their interiors, with split points `y1 = y_{B1}` and `y2 = y_{B2}` in `int J`.
Then `B1` contains `s'` in its interior, that is `u_{B1} > s'`. The mirror
statement holds for the interval to the left of `s`.

*Proof.*

1. **Setup.** Since `s < y1`, the child of `B1` containing `s` in its
   interior is `[l_{B1}, y1]`, and `B2` lies inside it. Hence
   `l_{B2} >= l_{B1}`, `u_{B2} <= y1` and `y2 < y1`.
2. **Notation.** Write `d = s - l_{B1} > 0` and `e = u_{B1} - s > 0`, and put
   `t_k = y_k - s`. Then `0 < t2 < t1 < min(e, lambda)`.
3. **Three facts.**
   - `y1` minimizes `phi_{B1}` over `B1`, and `y2` lies in `B1`. So
     `m(y1) - alpha (t1 + d)(e - t1) <= m(y2) - alpha (t2 + d)(e - t2)`.
   - `B2` is invalid at its minimizer `y2`. Using `y2 - l_{B2} <= t2 + d` and
     `u_{B2} - y2 <= t1 - t2`, this gives
     `m(y2) < alpha (y2 - l_{B2})(u_{B2} - y2) <= alpha (t2 + d)(t1 - t2)`.
   - `J` is valid, so `m(y1) >= alpha t1 (lambda - t1)`.
4. **Combination.** Chaining the three facts and using
   `(t1+d)(e-t1) - (t2+d)(e-t2) = (t1-t2)(e - t1 - t2 - d)` gives

   ```
   alpha t1 (lambda - t1) <= m(y1)
                          <  alpha (t2 + d)(t1 - t2) + alpha (t1 - t2)(e - t1 - t2 - d)
                          =  alpha (t1 - t2)(e - t1).
   ```

5. **Conclusion.** Since `0 < t1 - t2 < t1` and `e - t1 > 0`, the right side
   is less than `alpha t1 (e - t1)`. So `lambda < e`, that is `u_{B1} > s'`. □

*Proof of Theorem 1.*

1. **Every internal node has a split point.** By Lemma 1(i), the split point
   of an internal node lies either at an interior breakpoint or in `int J_j`
   for some `j`.
2. **Splits at breakpoints.** By Lemma 1(ii), each of the `N - 1` interior
   breakpoints is a split point at most once.
3. **Classes of splits inside an interval.** Fix `J = J_j`, and let `Y_J` be
   the internal nodes with split point in `int J`. By Lemma 1(iii) each such
   node falls into one of three classes:
   - `Y^L`: it contains `s_{j-1}` but not `s_j` in its interior;
   - `Y^R`: it contains `s_j` but not `s_{j-1}`;
   - `Y^LR`: it contains both.
4. **At most one node in `Y^LR`.** Nodes containing both breakpoints contain
   `J` and are nested (Lemma 1(iv)). If one of them splits inside `int J`,
   neither child contains both `s_{j-1}` and `s_j` in its interior. So no
   descendant is in `Y^LR`, and an ancestor in `Y^LR` would have no
   descendant containing `J`, a contradiction.
5. **At most one node in `Y^L`.** Nodes in `Y^L` share the interior point
   `s_{j-1}`, so they are nested. If `B1 ⊋ B2` were both in `Y^L`, Lemma 2
   would put `s_j` in the interior of `B1`, contradicting `B1 in Y^L`. The
   mirror lemma gives the same for `Y^R`.
6. **End intervals.** For `j = 1`, no node contains `s_0 = L` in its
   interior, so `Y^L` and `Y^LR` are empty and `|Y_{J_1}| <= 1`. Similarly
   `|Y_{J_N}| <= 1`.
7. **Count.** The number of internal nodes is at most
   `(N - 1) + 2 + 3(N - 2) = 4N - 5`, so `T <= 8N - 9`. The tree is finite
   because the number of internal nodes is bounded. □

**Corollary 1 (inexact minimizers; corrected after the review).** Suppose
the rule splits every invalid node `B` at an interior point `y` with
`phi_B(y) <= min_B phi_B + delta`, where `delta >= 0`.

- (a) If `delta < eps/2` and `N_opt(eps - 2 delta) >= 2`, then
  `T_eps <= 8 N_opt(eps - 2 delta) - 9`. Here `N_opt(eps')` is the least
  certificate size at tolerance `eps'`. If `N_opt(eps - 2 delta) = 1`, the
  root is valid at `eps` and `T_eps = 1`.
- (b) If also `phi_B(y) < 0` at every split point, `delta < eps` and
  `N_opt(eps - delta) >= 2`, then `T_eps <= 8 N_opt(eps - delta) - 9`.
  Otherwise `T_eps = 1`.
- The case `N_opt = 1` was missing in the revised version; the recheck noted
  that the formula would read `-1`.

*Proof.* Take the certificate at the stated tighter tolerance and rerun
Lemma 2.

1. **First fact.** Since `y1` is a `delta`-minimizer, it gains `+ delta`:
   `m(y1) - alpha q_{B1}(y1) <= m(y2) - alpha q_{B1}(y2) + delta`.
2. **Second fact.** It uses that `B2` is invalid at its split point `y2`.
   For a `delta`-minimizer this only gives `phi_{B2}(y2) < delta`, which
   costs a second `+ delta`. Under the extra hypothesis of (b),
   `phi_{B2}(y2) < 0` and the second fact is unchanged.
3. **Third fact.** At tolerance `eps - 2 delta` (case a) or `eps - delta`
   (case b), the third fact reads
   `m(y1) - 2 delta >= alpha t1 (lambda - t1)` or
   `m(y1) - delta >= alpha t1 (lambda - t1)`. The `delta` terms then cancel
   in the combination.
4. **Lemma 1(iii).** It still holds, because an interval valid at a tighter
   tolerance is valid at `eps`. □

The first version of this note stated (b) without the hypothesis
`phi_B(y) < 0`. Its proof overlooked the `delta` in the second fact; the
review found this. Whether that stronger form holds for all
`delta`-minimizers is **open**. The review's exact searches, 119,493 runs
with worst-case choices among `delta`-minimizers, found no violation.

### 4.1 What the proof uses

- **Used:**
  - the bilinear form of `q_B`, in step 4 of Lemma 2;
  - that the split point is an exact (or `delta`-) minimizer of the node's
    own relaxation;
  - that a certificate interval is valid at the node's pruning threshold.
- **Not used:**
  - convexity of `f_B`;
  - smoothness of `f`;
  - any property of `alpha` or `eps`. The constant is absolute.
- **Order and incumbent.** The split rule does not depend on the incumbent.
  So with any node order and any incumbents `f* <= U_t <= f* + g`, where
  `g < eps`:
  - The tree contains the fixed-`f*` tree, with the same tie-breaking.
  - Every node that is not pruned has `LB < U_t - eps <= f* - (eps - g)`, so
    it is invalid at tolerance `eps - g`.
  - The split points do not depend on the tolerance. So Theorem 1 applies
    verbatim at tolerance `eps - g`: `T <= 8 N_opt(eps - g) - 9`.
  - This direct argument is the review's; the first version routed it
    through Corollary 1.

### 4.2 Sharpness of the constants

- **Per-interval count.** The bound of 3 splits per interior interval and 1
  per end interval is attained. Both `verify_thm1.py` and the review's exact
  searches find it; the review's `11/5` instance below has per-interval
  counts `[1, 3, 1]`.
- **Two breakpoint intervals (Proposition 2).** When `N_opt = 2`, `R_min`
  uses at most 5 nodes (below).
- **Worst ratio (corrected).** The first version reported a worst case
  `(4N - 3)/(2N - 1)` tending to 2. That came from weak floating-point
  searches and is **wrong** as a worst case.
  - The review's exact instance has `alpha = 1` and `eps = 1/100`, knots
    `0, 1/16, 3/16, 7/16, 1/2, 9/16, 13/16, 15/16, 1`, and
    `m = 41/1600, 41/1600, 823/20000, 1/100, 1/100, 1/100, 823/20000, 41/1600, 41/1600`
    at those knots (convex `H`, unique minimizers).
  - It has `N_opt = 3`, and `R_min` splits at `1/2, 3/16, 7/16, 13/16, 9/16`,
    giving `T = 11`. So the worst ratio of `R_min` lies in `[11/5, 4)`.
  - This note's float simulator reproduces `N_opt = 3`, `T = 11`
    (Section 7.2).
- **Best rule in model I1.** On piecewise-quadratic classes, the best ratio
  of any I1 rule lies in `[5/3, 4)`. By Proposition 2, instances with
  `N_opt >= 3` are needed to push the lower bound above `5/3`.

**Proposition 2 (review; `T <= 5` when `N_opt = 2`).** Under the
hypotheses of Theorem 1, if `N_opt = 2`, then `R_min`, with any choice of
minimizers, uses at most 5 nodes, so its ratio on such instances is at
most `5/3`.

- This is attained, for example on Theorem 3's instance A (checked by the
  recheck).
- Together with Theorem 3, `R_min` is optimal among I1 rules on the
  `N_opt = 2` instances of **piecewise-quadratic (non-analytic) classes**.
- For analytic classes the I1 data determine `f`, so ratio 1 is possible in
  principle (Section 1.4).

*Proof* (the review's, checked here line by line; units `alpha = 1`). Let
`J_1 = [L, s]` and `J_2 = [s, U]` be the certificate.

1. **Root.** If the root splits at `s`, then `T = 3`. By symmetry let it split
   at `y1 in int J_2`. Then `[y1, U] ⊆ J_2` is valid.
2. **Second node.** If `B2 = [L, y1]` is valid, then `T = 3`. Otherwise `B2`
   splits at `y2`.
   - `y2 = s`: both children are valid, and `T = 5`.
   - `y2 in int J_2`: Lemma 2 applied to the root and `B2`, which both contain
     `s` in their interiors, would put `U` in the interior of the root. This
     is impossible.
   - `y2 in int J_1`: then `[L, y2]` is valid, and it remains to show that
     `B3 = [y2, y1]` is valid.
3. **Setup for a contradiction.** Suppose `B3` is invalid, and take `w in B3`
   with `m(w) < (w - y2)(y1 - w)`.
4. **`w` lies right of `s`.** `y2` minimizes `phi_{B2}` and `w in B2`, so
   `m(y2) <= m(w) + (y2-L)(y1-y2) - (w-L)(y1-w) < (y2-L)(w-y2)`. Validity of
   `J_1` at `y2` gives `m(y2) >= (y2-L)(s-y2)`. Hence `w > s`.
5. **`w` lies left of `s`.** `y1` minimizes the root relaxation, so
   `m(y1) <= m(w) + (y1-L)(U-y1) - (w-L)(U-w) < (y1-w)((U-y1) - (y2-L))`.
   Validity of `J_2` at `y1` gives `m(y1) >= (y1-s)(U-y1) > 0`.
   - If `(U-y1) - (y2-L) <= 0`, this is already a contradiction.
   - Otherwise `(y1-s)(U-y1) < (y1-w)(U-y1)`, so `w < s`.
6. **Conclusion.** Steps 4 and 5 contradict each other, so `B3` is valid and
   `T <= 5`. □

The two identities used in steps 4 and 5 were rechecked:

```
(w-y2)(y1-w) + (y2-L)(y1-y2) - (w-L)(y1-w) = (y2-L)(w-y2)
(w-y2)(y1-w) + (y1-L)(U-y1) - (w-L)(U-w)   = (y1-w)((U-y1) - (y2-L))
```

The first version's remark "two wasted splits are possible" (a right split,
then a left split, found by `chain_lp.py`) is consistent with this: after the
two wasted splits the third node is valid, so `T = 5`. The first version's
open question "can an adversary force `7/3` with `N = 2`?" is answered
negatively for every rule, because `R_min` never exceeds 5 nodes there.

## 5. Lower bounds

### 5.1 Theorem 2: oblivious rules lose `log(1/eps)` in every dimension

**Theorem 2.** Let `n >= 1`, `alpha > 0`, `X0 = [0,1]^n`, and let `R` be an
oblivious rule (model I0). Then there is `a in [1/3, 2/3]^n`, depending only on
`R`, with the following property. For the exact-gap instance
`f_a(y) = 2 alpha |y - a|_1`, which has `f* = 0` and `f_a + alpha |y|^2`
convex, and for every `eps in (0, alpha/9)`:

- `N_opt <= 2^n`;
- `T_R >= 2 ceil(n log_36(alpha/(9 eps))) + 1`.

So the ratio of `R` is at least
`(2 n log_36(alpha/(9 eps)) + 1)/(2^(n+1) - 1)`.

*Proof.*

1. **Pruning for `f_a`.** Write `m = eps + 2 alpha |y - a|_1`. If `a` lies in
   the interior of `B`, then `phi_B(a) = eps - alpha q_B(a)`, so `B` is
   invalid when `alpha q_B(a) > eps`.
2. **Certificate with `2^n` boxes.** Take the orthant boxes at `a`, whose
   sides are `[0, a_i]` or `[a_i, 1]`. With `t_i = |y_i - a_i|` and sides of
   length `w_i <= 1`,
   `phi_C(y) = eps + sum_i (2 alpha t_i - alpha t_i (w_i - t_i)) >= eps > 0`.
   So `N_opt <= 2^n`.
3. **Adversary invariants.** Build a chain of nodes `B_0 = X0, B_1, ...`, each
   a child of the previous one under `R`. Alongside, keep intervals
   `A_k^(i) ⊆ side_i(B_k)` satisfying:
   - (P1) each endpoint of `side_i(B_k)` is at distance at least `|A_k^(i)|`
     from `A_k^(i)`;
   - (P2) `|A_k^(i)| >= 6^(-k_i)/3`, where `k_i` is the number of the first
     `k` splits made along coordinate `i`;
   - (P3) `A_{k+1}^(i) ⊆ A_k^(i)`.
4. **Start.** `A_0^(i) = [1/3, 2/3]`.
5. **Step.** Suppose `R` splits `B_k` along coordinate `i` at `s`, and let
   `A = A_k^(i)`.
   - One of `A ∩ [l_i, s]` and `A ∩ [s, u_i]` has length at least `|A|/2`.
     Call it `A'`, and let `B_{k+1}` be the child on that side.
   - Set `A_{k+1}^(i)` to the middle third of `A'`. Its length is
     `|A'|/3 >= |A|/6`. Its distance to each end of `A'`, and hence to each
     end of the child's side, is `|A'|/3`.
   - Other coordinates are unchanged.
   Since `R` is oblivious, the chain does not depend on `a`.
6. **Choice of `a`.** Take `a in ∩_k prod_i A_k^(i)`, a nested intersection of
   non-empty compact sets. By (P1), `(a_i - l_i)(u_i - a_i) >= |A_k^(i)|^2`
   for every `i` and `k`.
7. **Chain nodes are invalid.** Some coordinate has `k_i <= k/n`, so (P2)
   gives `q_{B_k}(a) >= 36^(-k/n)/9`. By step 1, `B_k` is invalid, hence
   internal, whenever `k < n log_36(alpha/(9 eps))`.
8. **Count.** The chain therefore has at least
   `ceil(n log_36(alpha/(9 eps)))` internal nodes. □

Remarks:

- **Bisection.** For bisection itself, the review of the scout report shows
  that some minimizers are much cheaper than others: sparse binary digits
  give 513 nodes at `eps = 2^-1000`. Theorem 2 needs only one bad `a` per
  rule; the adversary supplies it.
- **Order is tight.** Theorem A of the scout report gives the matching order
  `O(log(1/eps))` for bisection.

### 5.2 Proposition 4: safeguards and midpoint mixing are not competitive

For `lambda in [0,1]` and `theta in [0, 1/2)`, let
`pi(p) = clip(lambda p + (1 - lambda)/2, theta, 1 - theta)`. This is the
relative position of `R_{lambda,theta}`'s split point in a node whose
relaxation minimizer sits at relative position `p`.

**Proposition 4.** Let `(lambda, theta) ≠ (1, 0)`. Then the equation
`pi(p) = p/(1 - p)` has a root `p̄ in (0, 1/2)`. Put
`kappa = p̄/(1 - p̄) in (0,1)` and take the instance
`f(y) = 2 alpha |y - p̄|` on `[0,1]` with exact gap. Then for every
`eps in (0, alpha p̄ (1 - p̄))`:

- `N_opt = 2`, and `R_min` uses `T = 3`;
- `T_{R_{lambda,theta}} >= 2 K + 1`, where
  `K = ceil( log(alpha p̄(1-p̄)/eps) / (2 log(1/kappa)) )`.

So `R_{lambda,theta}` has unbounded ratio, growing like `log(1/eps)`, on a
single fixed instance.

Explicit values:

| Rule | `(lambda, theta)` | `p̄` | `kappa` |
|---|---|---|---|
| SCIP deep-node limit; also SCIP with `midpull = 0` | `(1, 0.2)` | `1/6` | `1/5` |
| SCIP on nodes of at least half the global width | `(0.25, 0.2)` | `0.3117` | `0.4529` |
| Couenne default | `(0.25, 0.05)` | `0.3117` | `0.4529` |
| ANTIGONE, per Speakman–Lee (from the review) | `(0.75, 0.10)` | `0.2287` | `0.2965` |
| BARON, per Speakman–Lee (from the review) | `(0.70, 0.01)` | `0.2421` | `0.3195` |
| scout's `mix` | `(0.8, 0.02)` | `0.2127` | `0.2702` |
| exact example | `(2/3, 0.2)` | `1/4` | `1/3` |
| bisection | `(0, ·)` | `1/3` | `1/2` |

SCIP's actual default is not a fixed member of the family; it is treated in
Proposition 4' below.

When the clip is inactive, `p̄` solves
`lambda p^2 + (3/2)(1 - lambda) p - (1 - lambda)/2 = 0`. When the clip at
`theta` binds, `p̄ = theta/(1 + theta)`.

*Proof.*

1. **Existence of `p̄`.** `h(p) = pi(p) - p/(1-p)` is continuous on
   `[0, 1/2]`. At `0`, `h(0) = max(theta, (1-lambda)/2)`, which is positive
   exactly when `(lambda, theta) ≠ (1, 0)`. At `1/2`, `h = 1/2 - 1 < 0`.
2. **The minimizer is the kink.** For `B = [l, u] ∋ p̄` of width `w <= 1`,
   `phi_B(y) = eps + 2 alpha |y - p̄| - alpha (y-l)(u-y)` is convex.
   - Its right derivative at `p̄` is `2 alpha - alpha(u + l - 2 p̄) >= alpha (2 - w) > 0`.
   - Its left derivative there is at most `-alpha (2 - w) < 0`.
   - So the unique relaxation minimizer is `p̄`, and the node is invalid iff
     `alpha (p̄ - l)(u - p̄) > eps`.
3. **Other nodes are pruned.** Let `B = [l, u]` with `p̄ <= l`. For
   `y in B`,
   `phi_B(y) = eps + 2 alpha (y - p̄) - alpha (y-l)(u-y) >= eps + 2 alpha (y-l) - alpha (y-l) w >= eps`.
   The case `p̄ >= u` is symmetric. Hence nodes without `p̄` in their
   interior are pruned, and in particular `[0, p̄]` and `[p̄, 1]` are valid.
   The root is invalid, so `N_opt = 2`, and `R_min` splits the root at `p̄`,
   giving `T = 3`.
4. **Induction hypothesis.** Node `B_k` of the chain has width `kappa^k`, and
   `p̄` sits at relative position `p̄` or `1 - p̄` in it.
5. **Induction step.** If the position is `p̄`, then `R_{lambda,theta}`
   splits at relative position `pi(p̄) = kappa > p̄`. The child `[l, s]`
   contains `p̄`, has width `kappa^(k+1)`, and has `p̄` at relative position
   `p̄/kappa = 1 - p̄`. The case `1 - p̄` is the mirror image, since the rule
   commutes with reflection.
6. **Count.** `B_k` is invalid iff `alpha p̄ (1 - p̄) kappa^(2k) > eps`. This
   holds for `k = 0, ..., K - 1`. □

Consequences:

- **Uniqueness in the family.** Within the fixed-parameter family, the pure
  relaxation-minimizer rule is the only member with a bounded competitive
  ratio (Theorem 1). The family contains the Couenne default and the
  ANTIGONE and BARON settings tabulated by Speakman–Lee, but not SCIP's
  width-dependent default. That default is covered by Proposition 4'.
- **Scope.** Safeguards may still be useful for reasons outside the model:
  inexact or degenerate relaxations, bound tightening, and constraints.
  Corollary 1 shows that inexactness alone does not require them.

**Proposition 4' (SCIP 10's width-dependent default).** In the model the
global box is the root `[0, 1]`, so the global width is 1. Let `R_SCIP` split
an invalid node `[l, u]` of width `w` at

```
clip( mu mid + (1 - mu) y_B,  l + w/5,  u - w/5 ),     mu = 3/4 if w >= 1/2,  mu = 3w/4 if w < 1/2
```

(Section 1.5). Take the exact-gap instance `f(y) = 2 alpha |y - a|` on
`[0,1]` with `a = 3/238`. Then `N_opt = 2`, `R_min` uses 3 nodes, and for
`0 < eps < alpha (5/36)(9/119)^2`:

```
T_{R_SCIP} >= 2 K + 1,   K = 2 + #{ k >= 2 : alpha (5/36) (9/119)^2 25^-(k-2) > eps }.
```

So `R_SCIP` needs at least order `log(1/eps)/log 25` relaxations on a fixed
instance where two leaves suffice.

*Proof.*

1. **Minimizers and pruning.** As in steps 2 and 3 of Proposition 4, every
   node containing `a` in its interior has relaxation minimizer `a`. It is
   invalid iff `alpha (a - l)(u - a) > eps`. `N_opt = 2`, and `R_min` uses 3
   nodes.
2. **Root.** `w = 1`, so `mu = 3/4`, and the split is
   `3/8 + a/4 = 45/119`. This lies inside `[1/5, 4/5]`, so the clamp is
   inactive. The child `N_1 = [0, 45/119]` contains `a`, at relative position
   `1/30`.
3. **`N_1`.** `w = 45/119 < 1/2`, so `mu = 135/476`. The unclamped point is
   `(3/238)(1 + 14 mu) ≈ 0.0627`. This is below `l + w/5 = 9/119 ≈ 0.0756`,
   so the clamp binds and the split is `9/119`. The child
   `N_2 = [0, 9/119]` has `a` at relative position exactly `1/6`.
4. **From `N_2` on.** Every later node has `w <= 9/119`, so
   `mu <= 27/476 < 1/10`.
   - With `a` at relative position `1/6`, the unclamped point is at relative
     position `(1 - mu)/6 + mu/2 = 1/6 + mu/3 < 1/5`. So the clamp binds at
     `1/5`. The child `[l, l + w/5]` has `a` at relative position `5/6`.
   - With `a` at `5/6`, the mirror computation clamps at `4/5`, and the child
     has `a` at `1/6`.
   - So from `N_2` the chain is the `(1, 0.2)` chain of Proposition 4: widths
     `(9/119) 5^-(k-2)`, relative positions alternating `1/6` and `5/6`.
5. **Counting.** Node `N_k`, for `k >= 2`, is invalid iff
   `alpha (5/36) w_k^2 > eps`. `N_0` and `N_1` are invalid under the stated
   bound on `eps`, since their products `a(1-a)` and `a(45/119 - a)` exceed
   `(5/36)(9/119)^2`. Every invalid chain node is internal. □

Remarks:

- **Verification.** `scip_rule_check.py` verifies the chain in exact
  rationals, down to `eps = 1e-32`, where `T = 47` and `R_min` has 3 nodes.
  The recheck's independent full-tree simulation gives `T = 2K + 1` exactly.
- **Reference width.** The specific kink `3/238` relies on the reference
  width 1 at the first two nodes, where `mu = 3/4` and `mu = 135/476`.
  - With another fixed reference width, the kink would have to be re-chosen.
  - The `log(1/eps)` mechanism needs only a **fixed** reference width. From
    `N_2` on, the proof uses only `mu < 1/10`, which eventually holds for any
    fixed reference.
  - A parent-relative width would not have this property, but SCIP does not
    use one.
- **Floating-point guards.** SCIP also keeps the split at least
  `1.01e-9 max(|l|, |u|, 1)` from each bound. On this instance that guard
  overtakes the 0.2 clamp only at chain nodes that are invalid when
  `eps < 3.3e-19 alpha` (the recheck's computation). So the proposition
  describes SCIP's floating-point rule exactly for `eps >= 3.3e-19 alpha`.
  The verification rows at `eps = 1e-24` and `1e-32` describe the exact
  formula, not SCIP.
- **The clamp is what matters.** With the clamp removed (clamp 0, same
  vanishing pull), the same instance gives `T = 11, 13, 15, 17, 19` at
  `eps = 1e-8, 1e-12, 1e-16, 1e-24, 1e-32`. That is about **4** more nodes
  per doubling of `log(1/eps)`: `1e-8 → 1e-16` gives `11 → 15`, and
  `1e-16 → 1e-32` gives `15 → 19`. The first version said "about 2", which
  was a slip found by the recheck. The growth is consistent with
  `O(log log(1/eps))`.
  - Heuristically, without a clamp the pull `mu = 3w/4` puts the split within
    `O(w^2)` of the kink, so node widths around the kink shrink
    quadratically.
  - This is numerical only.
  - Random kinks (20 draws) give the same picture: mean `T = 43.4` with the
    clamp against `18.9` without it, at `eps = 1e-32`.
- **Relation to the review.** The review found the same `log(1/eps)` growth
  by exact simulation at `a = 1/6`. It noted that a proof needs a kink whose
  chain reaches the clamp regime at relative position `1/6`; `a = 3/238` is
  such a kink.
- **Scope.** This concerns SCIP's branching-point formula inside the
  exact-gap 1D model. It says nothing about SCIP's actual relaxations, which
  are McCormick-type rather than exact-gap.

### 5.3 Theorem 3: no I1 rule beats 5/3 in 1D (non-analytic classes)

Take `alpha = 1` on `[0,1]` and `eps = 1/10000`. Write each instance as
`f = H - y^2 - eps`, where `H` is a maximum of lines, so `f + y^2` is convex
and `m = H - y^2`. The lines are:

- the chords of `y^2`: `chord(a,b)(y) = (a+b) y - a b`;
- `g_-(y) = h1 + (4/5)(y - 3/5)` and `g_+(y) = h1 + (6/5)(y - 3/5)`, with
  `h1 = 143/300`;
- `e_0(y) = eps + y/6` and `e_1(y) = (5/3) y - 2/3 + eps`.

The instances are:

```
H_A = max{ chord(0,1/3), chord(1/3,1), g_-, g_+, e_0, e_1 }
H_B = max{ chord(0,3/5), chord(3/5,1), g_-, g_+, e_0, e_1 }
```

**Theorem 3.** Consider the class of continuous piecewise-quadratic `f`
with `f + y^2` convex, and any deterministic rule in model I1. The rule may
also see `f` on `[0, 30 eps/13] ∪ [1/60, 27/40] ∪ [1 - 3 eps, 1]`, which
contains both endpoints and the relaxation minimizer. Such a rule splits the root of A and
of B at the same point, and one of the two instances gets
`T >= 5 = (5/3)(2 N_opt - 1)`. Any randomized rule has expected
`T >= 4 = (4/3)(2 N_opt - 1)` on one of them.

*Proof.* The facts below are verified in exact rational arithmetic by
`lb_pair.py` (log in Section 7). They can also be checked by hand from the
lines.

1. **Same optimal value.** `min m = eps` in both instances, attained at
   `y = 0` and `y = 1`. Here `e_0` and `e_1` give `m = eps + y/6 - y^2` and
   `m = eps + (1-y)(1/3 - (1-y))` near the ends. So `f* = 0` in both.
2. **Same root relaxation.** On each linear piece of `H`, `H - y` has slope
   (line slope `- 1`). The slopes are `< 0` for the lines active left of
   `3/5` (`1/6`, `1/3` or `3/5`, `4/5`) and `> 0` for those active right of
   it (`6/5`, `4/3` or `8/5`, `5/3`).
   - So in both instances the root relaxation `min (H - y)` has the unique
     minimizer `3/5`.
   - Its value is `h1 - 3/5 = -37/300`.
3. **Identical near the minimizer and the ends.** Both `H`'s equal
   `max(g_-, g_+)` on `[1/60, 27/40]`, `e_0` on `[0, 30 eps/13]`, and `e_1` on
   `[1 - 3 eps, 1]`. So all data of model I1, and `f` on the stated set,
   coincide.
4. **Unique optimal breakpoints.**
   - A: `[0, b]` is valid iff `b <= 1/3`, and `[c, 1]` iff `c >= 1/3`. The
     reason is that `H_A` equals `chord(0, 1/3)` on `[6 eps, 1/140]` and
     `chord(1/3, 1)` on `[27/40, 1 - 3 eps]`, where `m` equals the
     corresponding cap. Any interval sticking out beyond `1/3` on either side
     violates validity at such points.
   - B: the same holds with `3/5`. Here `H_B` equals `chord(0, 3/5)` on
     `[30 eps/13, 1/60]` and `chord(3/5, 1)` on `[107/120, 1 - 15 eps]`.
   - In both instances `H >= ` its two chords, so `N_opt = 2`, and the
     two-piece certificate is unique.
5. **Deterministic conclusion.** Let `sigma` be the common root split. If
   `sigma ≠ 1/3`, a child in A is invalid; if `sigma ≠ 3/5`, a child in B is
   invalid. An invalid child adds at least 2 nodes.
6. **Randomized conclusion.** A randomized rule draws `sigma` from the same
   distribution on both instances. One of the events `sigma ≠ 1/3` and
   `sigma ≠ 3/5` has probability at least `1/2`. □

Remarks:

- **Scaling and smoothness.** The construction is invariant under affine
  rescaling of the box. It can plausibly be made `C^inf` (argued here and by
  the review, not computed): extend each `H` to `R` as the
  same maximum of lines, and mollify at a scale `zeta < eps`.
  - The result is convex and `>= H`. It equals `H` outside the
    `zeta`-neighbourhoods of the kinks.
  - The tight chord segments of step 4 shrink by `zeta` at each end but
    survive, so the unique breakpoints stay exactly `1/3` and `3/5`.
  - The instances still agree near `3/5` and near the ends. The smoothed kink
    at `3/5` gives a unique root minimizer, the same in both, because
    `H_A = H_B` there.
  - This was argued, not computed.
- **Scope (added after the review).**
  - A and B are piecewise quadratic, not analytic. The theorem is a lower
    bound over non-analytic classes.
  - For real-analytic classes, including polynomials, `f` near `3/5`
    determines `f`, so I1 equals I_inf and Proposition 0 applies.
  - If I1 is restricted to finite local data (the box, `LB`, `y_B`, the
    incumbent, `eps`, and any finite one-sided jet of `f` at `y_B` and at the
    endpoints), the theorem holds for the same instances, because A and B
    agree near those points.
  - A lower bound for polynomials of bounded degree `d` would need jets of
    order below `d` and polynomial instances. It is open.
- **What larger information buys.** Model I_inf breaks the construction:
  `f` differs on `(30 eps/13, 1/60)` and on `(27/40, 1 - 3 eps)`.
  Proposition 0 below shows that I_inf rules are exactly optimal.

### 5.4 Proposition 0: full node information makes 1D trivial

**Proposition 0.** In 1D with model I_inf, the following rule gives
`T = 2 N_opt - 1`: at an invalid node `[l, u]`, split at
`b(l) = max{ b : [l, b] valid }`.

*Proof.*

1. **`b(l)` exists and is useful.** It exists because validity of `[l, b]` is
   a closed condition in `b` that holds for `b` near `l`, since `m >= eps`.
   It satisfies `b(l) < u` because the node is invalid.
2. **Shape of the tree.** The left child is valid. The right children are
   `[x_k, U]`, and the leaves are the greedy partition.
3. **Optimality.** For interval covers with hereditary validity, the greedy
   partition is optimal by the usual exchange argument. □

## 6. n dimensions

### 6.1 What transfers

- **Oblivious rules.** Theorem 2 is already stated for every `n`.
- **Safeguarded and mixed rules.** Proposition 4 transfers to rules that
  apply `R_{lambda,theta}` along an arbitrarily chosen coordinate. Take
  `f(y) = 2 alpha sum_i |y_i - p̄|` on `[0,1]^n`.
  - Every node containing `a = (p̄, ..., p̄)` in its interior has relaxation
    minimizer `a`, because each coordinate has slope `2 alpha >= alpha w_i`.
  - Such a node is invalid when `alpha q_B(a) > eps`, as in step 1 of
    Theorem 2.
  - A split along coordinate `i` acts on that coordinate exactly as in 1D:
    the width shrinks by `kappa`, and the relative position alternates between
    `p̄` and `1 - p̄`.
  - After `k` splits some coordinate has been split at most `k/n` times. So
    `T >= 2 ceil( n log(alpha p̄(1-p̄)/eps) / (2 log(1/kappa)) ) + 1`, while
    `N_opt <= 2^n`.
- **Theorem 3 (not proved in `n` dimensions).** A constant-factor lower
  bound for model I1 in `n` dimensions should follow by adding a sharp term
  `2 alpha sum_{i>=2} |y_i - 1/2|` to Theorem 3's instances. The argument was
  not written out or checked, so it is not claimed.

### 6.2 Why the proof of Theorem 1 does not extend

1. **Validity is no longer a radius condition.** For a box with centre `c` and
   half-widths `r`, `B` is valid iff
   `m(y) + alpha |y - c|^2 >= alpha |r|^2` on `B`.
   - The global proximal point of `m` at `c` may lie outside an invalid box.
     The box's relaxation minimizer then lies on a facet, with
     `a_i(y_B) = 0` in some coordinates.
   - So Proposition 1(a) fails, and the rule must choose a coordinate.
2. **The key inequality loses its force.** For nested nodes `B1 ⊋ B2` with
   minimizer `y1` of `B1` and minimizer `y2` of `B2`, both in a certificate
   box `C`, the three facts of Lemma 2 still combine to

   ```
   alpha q_C(y1) <= m(y1) <= m(y2) + alpha (q_{B1}(y1) - q_{B1}(y2))
                           <  alpha q_{B1}(y1) - alpha (q_{B1}(y2) - q_{B2}(y2)).
   ```

   - In 1D the right side is `alpha (t1 - t2)(e - t1)`, which forces `B1` to
     overhang the far end of `C`.
   - In `n` dimensions both sides are sums over coordinates. The inequality
     only says that `B1` overhangs `C` in some coordinate, which is true for
     every node not contained in `C`. Nothing constrains the split coordinate.
3. **No chain structure.** The 1D count rests on the fact that nodes whose
   split lies in a certificate interval contain one of its two endpoints, and
   such nodes form at most three chains. A box can fail to lie in `C` because
   of any of its `2n` facets, and nodes crossing a facet of `C` need not be
   nested.

### 6.3 Full node information in n dimensions

With model I_inf, a rule can compute an optimal guillotine certificate of the
node box and make its first cut. By the Bellman principle this attains
`T_opt = 2 N_guill - 1`. So against the benchmark of Section 1.3 the I_inf
ratio is exactly 1 in every dimension. The first version's table mixed the
two benchmarks; the review pointed this out.

Measured against `2 N_opt - 1` instead, the ratio is the guillotine
overhead `sup (2 N_guill - 1)/(2 N_opt - 1)`.
[`n-dimensional.md`](n-dimensional.md), Section 4, gives:

- a self-contained bound by grid refinement;
- the bound `C_n log(1/eps)` from Theorem A, for a cube root box;
- published binary-space-partition bounds, known from abstracts:
  `N_guill <= 2 N_opt - 1` in 2D and `O(N_opt^((n+1)/3))` for `n >= 3`;
- grid experiments, in which no overhead survives fine grids.

### 6.4 Conjecture and evidence

**Conjecture 1.** For each `n` there is a `C_n` such that `omega` satisfies
`T <= C_n N_opt` on every exact-gap instance on a box in `R^n`. Recall that
`omega` splits at the relaxation minimizer along a coordinate maximizing
`(y_{B,i} - l_i)(u_i - y_{B,i})`.

A weaker version replaces `N_opt` by `N_guill`. A still weaker version allows
a factor `O(log log(1/eps))`.

The continuation [`n-dimensional.md`](n-dimensional.md) adds:

- a proof that the variant `multi` is **not** competitive (Theorem N3);
- exact comparisons of `omega`, a largest-deficit rule and `multi` against
  exact guillotine optima on candidate grids;
- the guillotine-overhead question.

**Evidence** (`sep2d.py`, `sep2d.log`).

- **Setting.** Separable 2D instances `m = m_1(y_1) + m_2(y_2)`. Each `m_i`
  is polyhedral in the sense of Section 7, with a geometric grid of knots
  around the minimizers down to `1e-13`, so node bounds are exact.
- **Results.** Node counts at `eps = 1e-2 ... 1e-10`:

| Family | bisection | `omega` | `multi` | bounded certificate |
|---|---|---|---|---|
| sharp point `2 abs(t) - t^2` in both coordinates | 13 → 63 | 7 | 5 | 4 cells, all `eps` |
| four rigid sawtooth breakpoints per coordinate | 49 → 993 | 23–35 | 29–39 | 16 cells, all `eps` |
| shallow kinks `0.3 abs(t)` | 19 → 71 | 15 → 25, then constant | 17 → 25, then constant | — |
| sharp `x_1`, quadratic `x_2` | 17 → 107 | 15 → 71 | 13 → 69 | — (`N_opt` grows like `log(1/eps)`) |
| quadratic in both | 39 → 329 | 33 → 289 | 29 → 247 | — (`log(1/eps)`) |

- **Reading.** Where an `eps`-independent certificate exists, the minimizer
  rules stay bounded while bisection grows like `log(1/eps)`. Where `N_opt`
  itself grows, all rules grow at comparable rates.
- **A correction.** An earlier version of `sep2d.py` omitted the box
  endpoints when minimizing each separable term. That produced a spurious
  2000-node blow-up for a widest-coordinate variant (`omegaW`). After the
  fix, `omegaW` behaves like `omega` up to a factor below 2.
- **Limits.** Separable instances are a restricted test. No non-separable 2D
  experiment was run.

### 6.5 Two-sided gaps

The scout's hypothesis allows `alpha q_B <= f - f_B <= alpha' q_B` with
`kappa = alpha'/alpha > 1`. Theorem 1 uses the exact form of `phi_B` in the
first fact of Lemma 2. With a two-sided gap that fact weakens to
`m(y1) - g_{B1}(y1) <= m(y2) - g_{B1}(y2)`, with `g_{B1}` anywhere between
`alpha q_{B1}` and `alpha' q_{B1}`, and the conclusion is lost.

A heuristic suggests the loss may be only a function of `kappa`:

- An adversarial gap can move the relaxation minimizer of a node containing a
  sharp kink of slope `sigma` away from the kink only if
  `sigma < (alpha' - alpha) w/2`. That happens at `O(log kappa)` scales at
  most.
- Nodes that are not centred near a kink are not covered by this argument.

This is not a proof. The two-sided case is open.

## 7. Computations

All commands were run from this directory, with `OMP_NUM_THREADS=1` for the
numpy scripts. The logs sit next to the scripts.

- **Exact** checks use Python `fractions`: `lb_pair.py`, `prop4_check.py`
  (rational cases) and `thm2_check.py`.
- **Floating-point** checks cover everything else. They are illustrations,
  not certificates.

### 7.1 Instance model used in 1D numerics

`poly1d.py` represents `H = m + y^2` (with `alpha = 1`) as a convex
piecewise-linear function through knots. Between knots `m` is a concave cap of
curvature `-2`, the extreme allowed. For such instances:

- `H` minus a chord is convex and piecewise linear, so node values and
  relaxation minimizers are exact minima over interior knots.
- The greedy certificate `b <- min over knots k in (a,b) of k + m(k)/(k - a)`
  is exact.

Every exact-gap instance is a limit of these.

**Why this class suffices for some rules.** The argument needs `H` convex:
the interpolant lies above `H` only then. The review pointed this out.
Consider rules that see only the box, the relaxation value and the
minimizer, and not `f` near it. Replace `H`
by the piecewise-linear interpolant of its values at the root endpoints and
at the minimizers of the processed nodes. This raises `H` elsewhere and leaves
every node value and observed minimizer unchanged, up to ties. So for such
rules these instances are without loss of generality.

**Rounding guard.** A guard `TOL = 1e-12` treats relaxation values
`>= -1e-12` as pruned. The 1D runs use tolerances between `1e-12` and `1e-2`.
At the smallest tolerances the guard is comparable to `eps`, so counts there
are less reliable.

**A float artefact.** Before the guard was added, a search reported
`T = 7, N = 2` for `R_min`. On inspection the "splits" were at points within
`1e-10` of node endpoints, with margins `1e-10` and `1e-18`. The guard removed
it; all numbers below are with the guard.

### 7.2 Commands and outputs

**Theorem 1 check.** `python3 verify_thm1.py 3000 7` and
`python3 verify_thm1.py 3000 8`, logged in `verify_thm1.log`.

- Instances: random polyhedral instances; rigid-breakpoint instances built
  from chords plus random extra lines; and sampled sharp, quadratic and
  quartic functions. Instances that failed construction were skipped.
- For the greedy certificate the script classifies split points per interval
  as `Y^L`, `Y^R`, `Y^LR` and asserts each class has at most one element and
  that `T <= 8N - 9`.

```
instances checked: 2977; max interior-interval splits 3; max end-interval splits 1; max T/(2N-1) = 1.889; all assertions passed
instances checked: 2964; max interior-interval splits 3; max end-interval splits 1; max T/(2N-1) = 1.889; all assertions passed
```

**Worst ratio of `R_min`.** `python3 search_ratio.py K E 6 400 seed` with
`(K,E,seed) = (1,4,1), (2,4,2), (4,3,3)`, logged in `sr1.log`, `sr2.log`,
`sr4.log`. This is hill-climbing over rigid-breakpoint instances.

```
BEST ratio 1.6667 T=5 N=2
BEST ratio 1.8000 T=9 N=3
BEST ratio 1.8889 T=17 N=5
```

**Random 1D searches.** `python3 search1d.py min 80 1e-10 3` and
`python3 search1d.py bis 80 1e-10 2`, logged in `search1d_min.log` and
`search1d_bis.log`. These use 80 random knots with hill climbing.

```
min: BEST (1.112, T=99, N=45)
bis: BEST (6.253, T=569, N=46)
```

**Rigid breakpoint with extra lines.** `python3 search_n2.py min 8 4 1` and
`python3 search_n2.py bis 8 2 1`, logged in `search_n2_min.log` and
`search_n2_bis.log`. The instance has a rigid breakpoint at `1/3` and 8 extra
lines, with `eps = 1e-12`.

```
min: BEST T=3, N=2        bis: BEST T=39, N=2
```

**Chain LPs.** `python3 chain_lp.py 0` and `python3 chain_patterns.py`,
logged in `chain_lp.log` and `chain_patterns.log`.

- The LP asks whether some instance realizes a prescribed chain of `R_min`
  wasted splits around one breakpoint with `N_opt = 2`, and maximizes the
  invalidity margin `delta`.
- Chain lengths 1 and 2 are feasible, with margins `0.22` and `0.044`. The
  length-2 chain is one right split, then one left split.
- Lengths 3–8 are infeasible for all 3000 random split sequences tried per
  length (best margins `-1.8e-8` to `-1.2e-6`).
- The best margin is negative for all 36 pattern/position combinations
  (`RR`, `RRR`, `LRL`, `RLRL`, ... at `s = 0.1, 0.5, 0.9, 0.99`). These
  searches are consistent with Lemma 2 and prove nothing beyond it.

**Theorem 3 check.** `python3 lb_pair.py`, logged in `lb_pair.log`, in exact
rationals.

```
== A (rigid at 1/3): 7 knots; min m = 1/10000 (eps = 1/10000); argmin m at ['0', '1']
   root LB (min of m - q) = -37/300 = -0.123333; minimizers ['3/5']
   [0,b] valid iff b <= 1/3; [a,1] valid iff a >= 1/3
== B (rigid at 3/5): 7 knots; min m = 1/10000 (eps = 1/10000); argmin m at ['0', '1']
   root LB (min of m - q) = -37/300 = -0.123333; minimizers ['3/5']
   [0,b] valid iff b <= 3/5; [a,1] valid iff a >= 3/5
f_A = f_B on [1/60, 27/40] = [0.0167, 0.6750]; both equal max(g_left, g_right) there
```

**Proposition 4 check.** `python3 prop4_check.py`, logged in
`prop4_check.log`. It is exact for `(1, 1/5)`, `(1, 1/50)` and `(2/3, 1/5)`,
and uses floats for `(0.25, 0.2)` and `(0.8, 0.02)`. Every run meets the
predicted chain bound. The pure minimizer gives `T = 3` throughout.

```
theta=1/5 a=1/6   eps=1e-4 .. 1e-16: T_clamp = 7, 13, 17, 23      T_unclamped = 3
lam=2/3 theta=1/5 p*=1/4 eps=1e-4 .. 1e-16: T = 9, 17, 25, 35
lam=0.25 theta=0.2 (Couenne)       eps=1e-4 .. 1e-16: T = 11, 23, 35, 47
```

**Theorem 2 check.** `python3 thm2_check.py`, logged in `thm2_check.log`, in
exact rationals.

- The script builds the adversary against oblivious rules: bisection, a
  golden-ratio split and a 10%-split, all along the widest side, in `n = 1, 2`.
- It then simulates the tree with exact separable node values. All runs
  exceed the bound `2 ceil(n log_36(1/(9 eps))) + 1`. For example, at
  `n = 2` and `eps = 1e-12`, bisection gives `T = 83` against the bound 31,
  with `N_opt <= 4`.
- **Correction.** The first version pruned every node that did not contain
  `a` in its interior. That is wrong for `n >= 2`, and it undercounted `T`
  (it reported 27, 53, 81 for `n = 2` bisection). The corrected
  script gives 29, 55, 83, matching the review's independent
  implementation. The assertions were lower bounds and remain valid.

**Proposition 4' check.** `python3 scip_rule_check.py`, logged in
`scip_rule_check.log`, in exact rationals.

```
instance a = 3/238; SCIP-default chain (first nodes, relative position of a):
   [0, 1]  width 1  rel. position 3/238
   [0, 45/119]  width 0.378151  rel. position 1/30
   [0, 9/119]  width 0.0756303  rel. position 1/6
   [0, 9/595]  width 0.0151261  rel. position 5/6
   [36/2975, 9/595]  width 0.00302521  rel. position 1/6
eps=1e-8  nodes {'scip': 13, 'scip_noclamp': 11, 'pure_min': 3}; predicted SCIP chain >= 6 invalid nodes -> T >= 13
eps=1e-16 nodes {'scip': 25, 'scip_noclamp': 15, 'pure_min': 3}; predicted SCIP chain >= 12 invalid nodes -> T >= 25
eps=1e-32 nodes {'scip': 47, 'scip_noclamp': 19, 'pure_min': 3}; predicted SCIP chain >= 23 invalid nodes -> T >= 47
random a (20 draws), eps = 1e-32: scip: max 51 mean 43.4, scip_noclamp: max 19 mean 18.9
```

**The review's `11/5` instance, rechecked with this note's simulator.**
`poly1d.py` gives `N_opt = 3`, `T_min = 11`, greedy breakpoints
`0.40697, 0.60749`, and splits `0.5, 0.8125, 0.5625, 0.1875, 0.4375` (an
inline check; the review's exact script is
`../../reviews/competitive/rmin_11_5.py`).

**2D separable runs.** `python3 sep2d.py`, logged in `sep2d.log`. The table is
in Section 6.4.

Other scratch runs were superseded or had the bugs described above
(`sep2d` endpoints, the float artefact); they are not reported. No
project-wide checks were run and CI was not inspected.

## 8. Literature and novelty

### 8.1 Sources examined

Local:

- the scout report `../../scouting/spatial-bb-theory.md` (all) and its review
  `../../reviews/spatial-bb-review.md` (Sections 1–6, 8, 9);
- the SCIP/Couenne branching-point notes in
  `research-20260922/scouting/scout_literature.md` and
  `brainstorm2-solvercore.md`;
- the Cheng–Basu summary in `../../scouting/data-driven-minlp-config.md` and
  the local text of arXiv:2601.23249 (abstract and introduction).

Web:

- the arXiv API was queried three times, for "branching point" with
  branch-and-bound and competitive or tree size; for instance-optimal or
  competitive-ratio branch-and-bound in global or Lipschitz optimization; and
  for Piyavskii with optimal or certificate;
- general web search was unavailable (session quota exhausted).

None of these returned a competitive analysis of branching points for
relaxation-based spatial branch-and-bound. The search was small. **It does
not establish novelty.**

The review examined further sources (its Section 8):

- the Hansen–Jaumard–Lu abstract;
- the full text of Daskalakis–Diakonikolas–Yannakakis;
- the Baran–Demaine–Katz abstract;
- the full text of Speakman–Lee;
- the SCIP and Couenne source code.

Section 8.2 relies on the review for those sources. They were not reread
here.

### 8.2 Comparison (revised after the review)

- **Hansen, Jaumard, Lu (1991)** (abstract, quoted in both reviews). For 1D
  Lipschitz functions, Piyavskii's algorithm uses at most `2 n_B + 1`
  evaluations, where `n_B` is the best certificate.
  - In 1D, Piyavskii's lower bound on a subinterval between consecutive
    evaluation points depends only on the two endpoint values. So Piyavskii is
    a node-local rule that splits at the minimizer of the node bound.
  - HJL is therefore a constant-competitive "split at the node bound's
    minimizer" result of the same kind as Theorem 1, 35 years earlier.
  - The first version's claimed difference ("Piyavskii's lower envelope is
    global") was wrong in 1D and is withdrawn.
  - What differs: here the node bound is a relaxation with a quadratic gap,
    validity depends on `f` over the whole node rather than on two endpoint
    values, and the proof is a different charging argument (Lemma 2).
- **Daskalakis, Diakonikolas, Yannakakis**, "How good is the Chord
  algorithm?" (SODA 2010; SIAM J. Comput. 2016; arXiv:1309.7084), as
  summarized by the review, which read the full text.
  - A per-instance competitive analysis of the chord algorithm for convex
    curve approximation, with lower bounds for every algorithm in an oracle
    model.
  - The chord algorithm's ratio grows (logarithmically or doubly
    logarithmically in `1/eps`, depending on the distance), and for the
    vertical distance every algorithm has unbounded ratio.
  - This is the closest precedent for the type of result in Theorem 3. By
    contrast, in the exact-gap model the optimal ratio is a constant in
    `[5/3, 4)`.
- **Baran, Demaine, Katz (2008)**, adaptive integration of Lipschitz
  functions (abstract, via the review): a logarithmic competitive ratio with a
  matching lower bound. Another per-instance competitive precedent.
- **Bachoc, Cesari, Gerchinovitz (2021)** and the Piyavskii regret papers
  (arXiv:2002.02390, 2108.10859): instance-dependent certified complexity for
  Lipschitz functions, within log factors. They do not consider relaxations or
  node-local rules.
- **Cheng–Basu (arXiv:2601.23249).** In MILP, local score-based branching can
  produce trees exponentially larger than optimal. The contrast holds: for 1D
  spatial branching with an exact quadratic gap, the purely local minimizer
  rule is constant-competitive. The multivariate question, where the variable
  choice enters, is where negative results appear: `multi` is not
  competitive ([`n-dimensional.md`](n-dimensional.md)).
- **Sandwich algorithms (an analogy only).** By Proposition 1, the relaxation
  minimizer is where a tangent of `H = f + alpha y^2` is parallel to the chord
  of `alpha y^2` over the node.
  - The sandwich "chord rule" (Burkard, Hamacher, Rote 1991; Rote 1992) uses
    the chord of the approximated function itself.
  - The two coincide only when `m(l) = m(u)`.
  - The first version called them the same rule; that was imprecise.
  - The review reports DDY's remark that Rote's and Yang–Goh's analyses give
    worst-case costs in `eps`, not per-instance ratios.
- **Solver practice.**
  - Couenne's default `(0.25, 0.05)` is a member of Proposition 4's family,
    and so has unbounded ratio on a fixed sharp 1D instance.
  - SCIP 10's default is width-dependent. Proposition 4' proves the same
    `log(1/eps)` loss on an explicit instance; its clamp is the cause.
  - The repository's SCIP probe (`brainstorm2-solvercore.md`, probe B)
    compared `midpull = 0` (the `(1, 0.2)` member, LP point with clamp) and
    `midpull = 1` (the midpoint with clamp) against the default
    `midpull = 0.75`. The node-count ratios were 0.90 and 1.01. These are
    small effects on MINLPLib, where relaxations are McCormick-type rather
    than exact-gap.
- **Finite termination.** Al-Khayyal–Sherali and Shectman–Sahinidis prove
  finite termination when branching at relaxation solutions for concave and
  bilinear problems. These are qualitative precursors. Theorem 1 is
  quantitative, but only for exact quadratic gaps.
- **Branching-point volumes.** Speakman–Lee optimize branching points by
  relaxation volume. That is not a competitive analysis.
- **Program credits.** The Dey–Dubey–Molinaro midpoint argument credited in
  the program concerns lower bounds for integer branching and is not used
  here. Of the mechanisms the program names, Bachoc–Cesari–Gerchinovitz is
  the relevant one. Hansen–Jaumard–Lu and DDY, which the program does not
  name, are the closest precedents for this workstream.

### 8.3 Originality (revised)

Originality is **modest**. The phenomenon, a node-local rule that is
constant-competitive in 1D while oblivious rules lose a log factor, is known
from Hansen–Jaumard–Lu for Lipschitz bounds. The new elements:

- **Theorem 1.** The transfer to relaxations with a quadratic gap, where
  validity depends on the whole node, with a new charging proof (Lemma 2).
- **Theorem 3.** A constant lower bound `5/3` for the relaxation-solution
  information model, on non-analytic classes. Its adversary technique is
  standard; the constant and instances are new as far as checked.
- **Propositions 4 and 4'.** Every fixed clamped or mixed branching point,
  and SCIP's default, loses `log(1/eps)` on a fixed sharp instance where the
  pure minimizer does not. No precedent was found.
- **Proposition 1.** The Moreau-envelope characterization of 1D validity. The
  Moreau envelope is standard; this use was not found elsewhere.
- **Routine or folklore:** Theorem 2 (a routine adversary) and Proposition 0
  (the greedy exchange argument).

Not searched: the interval-analysis literature and the Sukharev–Danilin
"sequentially optimal search" line.

## 9. Open questions

1. **Constant in 1D.**
   - The worst ratio of `R_min` lies in `[11/5, 4)`.
   - The best ratio of any I1 rule on piecewise-quadratic classes lies in
     `[5/3, 4)`.
   - With `N_opt = 2` both equal `5/3` (Proposition 2 and Theorem 3).
     Improving the lower bound needs `N_opt >= 3`.
2. **Corollary 1, stated form.** Does `T_eps <= 8 N_opt(eps - delta) - 9`
   hold for every `delta`-minimizer?
3. **Polynomial classes.** Is there a constant lower bound above 1 for rules
   that see only a jet of order below the degree?
4. **Conjecture 1** (`n >= 2`, rule `omega`). See
   [`n-dimensional.md`](n-dimensional.md) for the current evidence and for
   the proof that `multi` is not competitive.
5. **Guillotine overhead** in `n >= 2`. See
   [`n-dimensional.md`](n-dimensional.md), Section 4.
6. **Two-sided gaps.** Is `R_min` `C(kappa)`-competitive under
   `alpha q_B <= f - f_B <= alpha' q_B`?
7. **Face-exact relaxations (Q2).** Section 3.7 of the scout report shows that
   splitting at the LP solution gives 3 nodes on the McCormick example, while
   widest bisection needs `Omega(eps^(-1/2))`. Is there a competitive rule for
   McCormick relaxations, or a lower bound?
8. **Constraints.** With a feasible set, the relaxation minimizer may be
   infeasible, and certificates may prune by infeasibility. The proof of
   Theorem 1 uses `F = X0`.
9. **SCIP without the clamp.** Is the vanishing pull alone
   `O(log log(1/eps))`-competitive on sharp instances, as the numerics
   suggest?

## 10. Revision after review (2026-09-29)

The review [`../../reviews/competitive-review.md`](../../reviews/competitive-review.md)
confirmed the following:

- Theorem 1 and Lemma 2, with exact searches over about 40,000 instances;
- Theorem 3, in exact arithmetic;
- Proposition 4 as a statement about its family;
- Theorem 2, Proposition 0 and Proposition 1.

Changes made in response:

| Review item | Change |
|---|---|
| Corollary 1 proof incomplete (fact 2 also gains `delta`) | Corollary 1 restated: (a) `8 N_opt(eps - 2 delta) - 9`, (b) `8 N_opt(eps - delta) - 9` if split points have `phi_B(y) < 0`; the first version's unconditional form is marked open (Section 4) |
| Incumbent remark | replaced by the review's direct argument (Section 4.1) |
| New result: `T <= 5` when `N_opt = 2` | included as Proposition 2 with the review's proof, rechecked (identities verified symbolically) |
| Worst case "tends to 2" wrong | replaced by the review's exact `11/5` instance, rechecked with `poly1d.py`; worst ratio of `R_min` in `[11/5, 4)` (Section 4.2) |
| Theorem 3 scope (I1 is degenerate for analytic `f`) | stated in Section 1.4 and Section 5.3: lower bound over non-analytic classes; also valid with finite local jets; polynomial case open |
| Solver defaults | SCIP 10: `midpull 0.75`, `reldomtrig 0.5`, clamp `0.2` (width-dependent); Couenne `(0.25, 0.05)`; Speakman–Lee's ANTIGONE and BARON rows added (Sections 1.5, 5.2, 8.2) |
| Proposition 4 does not cover SCIP's default | new Proposition 4' proves `Omega(log(1/eps))` for SCIP's rule on `a = 3/238` (exact check `scip_rule_check.py`); the clamp is the cause |
| `thm2_check.py` undercounts `T` for `n >= 2` | fixed with exact separable node values; `n = 2` bisection now 29/55/83 (Section 7.2) |
| Table inconsistency for I_inf in `n` dimensions | fixed: ratio 1 against `2 N_guill - 1`; overhead only against `2 N_opt - 1` (Sections 2, 6.3) |
| "Chord rule" identification | weakened to an analogy (Section 8.2) |
| WLOG argument needs convex `H` | stated (Section 7.1); `poly1d.py` docstring fixed |
| Novelty relative to HJL | withdrawn difference; HJL, DDY and Baran–Demaine–Katz cited; originality stated as modest (Sections 8.2, 8.3) |
| "Two wasted splits" remark, open question on `7/3` | reconciled with Proposition 2; question answered negatively |

### 10.1 Second recheck (2026-09-29)

The recheck [`../../reviews/competitive-recheck.md`](../../reviews/competitive-recheck.md)
verified the following in exact arithmetic, with the SCIP v10.0.2 source for
Proposition 4':

- Proposition 4';
- Corollary 1 as corrected;
- Proposition 2;
- the restated scope of Theorem 3;
- Theorem N3, Lemma N4, Lemma N6 and Examples N1 of the companion note.

It found only minor problems. Fixes:

| Recheck item | Change |
|---|---|
| SCIP pull uses **global** width, clamp uses **local** bounds; "depth-dependent" and "root width" were loose | reworded to "global width" and "width-dependent" (Sections 1.5, 5.2, 8.2, 10) |
| Kink `3/238` relies on reference width 1 at two nodes | remark added: the `log(1/eps)` mechanism needs only a fixed reference width (Section 5.2) |
| No-clamp counts grow by about 4 per doubling of `log(1/eps)`, not 2 | corrected (Section 5.2) |
| SCIP's absolute `1e-9` guards take over for `eps < 3.3e-19 alpha` | caveat added; the `1e-24` and `1e-32` rows describe the formula, not SCIP (Section 5.2) |
| Corollary 1 needs `N_opt(...) >= 2` | added, with `T = 1` otherwise (Section 4) |
| "`R_min` optimal among I1 rules" needs Theorem 3's qualifier | restricted to piecewise-quadratic classes (Proposition 2) |
| I1 as "`f` on a neighbourhood of `y_B`" equals I_inf if the neighbourhood is unrestricted | I1 now uses the germ of `f` at `y_B` (Section 1.4) |
| Theorem A's cube-box hypothesis missing from the table | added (Section 2) |
| Proposition 1(a) fails in only one direction in `n` dimensions | Section 3 and the companion note corrected |
| Published guillotine bounds (Berman–DasGupta–Muthukrishnan; Hershberger–Suri–Tóth) | used in the table and in the companion note, as known from abstracts |
| Lemma N6 mixes tolerances | the companion note states that the product uses the split tolerances and the slice bound the full `eps` |
