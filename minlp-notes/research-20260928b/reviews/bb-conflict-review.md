# Review: midpoint-conflict lower bounds for convex-piece branch-and-bound

Target: `research-20260928b/scouting/bb-tree-size-convex.md`, Section 3
(Lemma 1, Theorem 1 and its remarks, Corollaries 1–2, Theorems 2–3, Lemma 4).
Date: 2026-09-28. Reviewer: independent adversarial review; I did not write
the material. The scout report was not edited. My scripts and logs are in
[`bb-conflict/`](bb-conflict/). No scout code was reused.

## Verdict summary

| Claim | Verdict | Main point |
|---|---|---|
| Lemma 1 | correct | Write `inf` for `min` (convex `phi` need not attain its minimum on `conv{a_i}` if it is not lower semicontinuous). |
| Theorem 1 (graph bound, partition bound, attainment) | correct, with small fixes | Needs a finite tree. Covering the feasible integer points is enough. Attainment by `conv I` needs finite classes. A stronger form that allows infeasible endpoints is needed for Corollary 2 (see 2.2). |
| Remark "Robustness" (OBBT, reduced-cost fixing) and the matching claims in Section 4 | **false as stated** | Counterexample in 2.3: incumbent-based OBBT with integer rounding solves an instance with `chi = 2` in one node. Brute force finds such instances in 88 of 140 random ones. A weaker statement is true: the number of nodes is at least `chi/(2n+1)`. |
| Remark "What is not covered" | too conservative | Cuts in the integer variables that are valid for the node's feasible integer points cannot remove a conflict between feasible points. Only cuts that involve continuous or epigraph variables, which change the projected `phi`, can remove one. |
| Corollary 1(a), 1(b) | correct | — |
| Corollary 2 (Hijazi–Bonami–Ouorou ball, extended OA master, disjunctive cuts) | correct, with a fix | Theorem 1 as stated gives nothing here because there are no feasible points. The proof needs the infeasible-endpoint form. The second bullet is Dey–Dubey–Molinaro (DDM) Prop. 3 on a slightly larger cross-polytope. |
| Theorem 2 (random CVP) | correct, with minor fixes | Every step checks, including `Var N = V'`, which is also confirmed by Monte Carlo. Fixes: the conflict needs a strict inequality (open ball, or "almost surely"). The bound is vacuous for `delta >= 0.0734`. For enumeration algorithms that skip out-of-range children (sphere decoders, Lenstra/Kannan), the model's leaf count becomes "at least `V/6` nodes". Under incumbent-based tightening the bound becomes `V/(2(2n+1))` nodes. |
| Theorem 3 (correlated pairs) | correct | Condition (ii) holds for every `th in (0, pi)`, `s != 0`, `lam > 0`, with the closed form `delta = s^2 sin^2 th / (2(1+lam)(1+2 lam+cos th))`. Condition (i) holds if and only if `cos th > 0`. All numbers reproduce. The `2^k` bound is attained by variable branching when `eps` is close to `delta`. At `eps -> 0` the exact minimum is `2^{k+1}-2`. |
| Lemma 4 (path lemma) | correct as stated | "Any node order" depends on the incumbent `OPT` being available when off-path children are evaluated. Without it, depth-first search can blow up while C1 holds (21 versus 351 nodes in Section 6). Best-bound order alone does not fix this when `eps > 0`. |

## 1. The model, made explicit

The results hold in the following model. Every item is used somewhere.

- **Problem.** `OPT = min{f(x) : x in F}`, where `F` is the set of feasible
  integer points. Continuous variables are minimized out, so `phi` is the
  projected relaxation objective.
- **Relaxation `(phi, K)`.** `K` is convex and contains `F`. `phi` is convex on
  `K` and `phi <= f` on `F`; the report asks for equality, but only `<=` is
  used. Any pointwise weaker relaxation is also covered, because its node
  bounds are smaller. This includes LP/NLP-based outer-approximation
  branch-and-bound with the NLP `phi`.
- **Tree.**
  - The tree is finite and rooted. Nodes carry convex sets `Q_v`.
    Closedness is never used.
  - The children of `v` cover `Q_v ∩ Z^n`. For Theorem 1, covering
    `Q_v ∩ F` is enough; this admits SOS branching.
  - Multiway branching is allowed. Nesting `Q_child ⊆ Q_v` is not needed if
    each point is assigned to a leaf by descending from the root. Then the
    argument also covers bound inheritance, where a node's bound is the
    maximum over its ancestors.
- **Node bound.** `r(v) = inf{phi(x) : x in K ∩ Q_v}`. A computed dual bound
  `<= r(v)` is also covered.
- **Leaves and `eps`-certificates.** A leaf is a node without children. An
  `eps`-certificate is a tree whose leaves all satisfy `r(v) >= OPT - eps`.
  Pruning by infeasibility (`r = +inf`), by bound (`r >= UB - eps >= OPT - eps`)
  and by integrality (`r = f(x̂) >= OPT`) all produce such leaves. The
  incumbent quality `eps'` plays no role. A node whose set contains a single
  integer point is *not* a leaf unless its bound is high. This matches DDM and
  Dadush–Tiwari.
- **Not in the model.**
  - Domain reductions that remove integer points (Section 2.3).
  - Cuts in continuous or epigraph variables.
  - Symmetry handling that fixes variables. Orbital fixing `z_{v_j} = 0` in
    the Theorem 3 gadget solves it at the root.
  - Nonconvex pieces.

## 2. Lemma 1 and Theorem 1

### 2.1 Step check

- **Lemma 1.** `conv{a_i}` lies in `K` and in `Q_v` because both are convex
  and contain the `a_i`. So `r(v) <= inf_{conv{a_i}} phi`. Correct. The report
  writes `min`; `inf` is right in general.
- **Theorem 1, covering step.** In a finite tree each integer point descends
  from the root to some leaf. Correct.
- **Theorem 1, bound.** Two points in one leaf would give
  `r(v) <= phi(mid) < OPT - eps`. So the feasible points in each leaf form an
  independent set, and there are at least `chi >= omega` leaves. Correct.
- **Partition form.** Admissibility is hereditary, since
  `conv(J) ⊆ conv(I)` for `J ⊆ I`. So a cover gives a partition. Correct.
- **Attainment.** If only `F` must be covered and `F` is finite, the
  depth-1 tree with children `conv I` attains the partition number. For
  infinite `F` (CVP), `conv I` need not be closed and classes may be infinite.
  Only the lower bound is then claimed, which is fine.

### 2.2 Needed strengthening: endpoints need not be feasible

The same argument proves a statement the report uses implicitly. Let `P` be
integer points that the pieces must cover, for example all of `Z^n`. If
`a != b` are in `P`, `m = (a+b)/2 in K`, and `phi(m) < OPT - eps`, then no leaf
contains both. The reason is that `m in Q_v ∩ K`; nothing requires `a` or `b`
to be in `K`.

This form is used in three places:

- **Corollary 2.** Its first bullet has `F = ∅`, so Theorem 1 as stated gives
  the trivial bound 1. The `2^n` bound needs this form. This is exactly
  DDM Prop. 3.
- **Objective cutoffs.** It survives adding `phi(x) <= UB` to `K`, because the
  midpoint has `phi < OPT <= UB`.
- **Symmetry-breaking inequalities.** It survives inequalities such as
  `z_{u_j} >= z_{v_j}` in Theorem 3, which keep the midpoint
  `(1/2, 1/2)` feasible.

A second free refinement is to use the segment minimum,
`a ~ b iff inf_{[a,b] ∩ K} phi < OPT - eps`. Its graph contains the midpoint
graph and is the pairwise case of the report's partition bound. In the brute
force (Section 7), the segment clique exceeds the midpoint clique in 35 of 60
two-dimensional instances.

### 2.3 The "Robustness" remark is false as stated

The claim reads: "The bound also holds with presolve-style domain reductions
that use the incumbent: OBBT on `K ∩ {phi <= UB}` and reduced-cost fixing.
The offending midpoint satisfies `phi < OPT <= UB`, so it survives every such
reduction."

The midpoint does survive, but the endpoints need not. A reduction may remove
`a` when `f(a) > UB`. After that, no leaf has to contain `a`, and the covering
step of Theorem 1 fails.

**Counterexample (one dimension).** Take `phi(x) = (x - 0.4)^2`, `x in Z`,
`K = R`, and `eps = 0.01`.

- `OPT = 0.16`, attained at `x = 0`.
- `phi(0.5) = 0.01 < OPT - eps`, so `0 ~ 1` and `chi = 2`. Every
  `eps`-certificate in the report's model has at least 2 leaves.
- With incumbent `UB = 0.16`, OBBT gives `{phi <= UB} = [0, 0.8]`. Integer
  rounding of the bounds gives `x in [0, 0]`. The root bound is then
  `0.16 >= UB - eps`, so the tree has one node.
- Without rounding, the reduced root set is `[0, 0.8]`, whose only integer
  point is 0. A single child covers it, so the tree has 1 leaf, which is still
  fewer than `chi = 2`.

**Brute force** (`thm1_bruteforce.py`). This uses exact minimum
variable-branching trees on random convex integer least-squares instances,
with OBBT and integer rounding at every node and `UB = OPT`. The minimum
number of leaves falls below the midpoint clique number in:

- 40 of 60 instances on `[0,2]^2`;
- 25 of 40 instances on `[0,3]^2`;
- 23 of 40 instances on `[0,2]^3`.

The minimum tree is often a single node.

**What is true.** Suppose every reduction at a node `v` tightens variable
bounds, and every removed part `Q_v ∩ {x_i <= l_i - 1}` or
`Q_v ∩ {x_i >= u_i + 1}` has relaxation bound `>= OPT - eps`. This holds for
OBBT on `K ∩ {phi <= UB}` (every removed point has `phi > UB >= OPT`), for
reduced-cost fixing, and for probing against `UB`.

Replace each reduction by explicit children: the reduced box plus at most
`2n` pruned outer pieces. This gives an `eps`-certificate in the report's
model with at most `L + 2n N <= (2n+1) N` leaves, where `L` and `N` are the
leaves and nodes of the original tree. Hence **`N >= chi(G_eps)/(2n+1)`**.

The brute force satisfies this bound in all 140 instances. For Theorem 2 the
corrected statement still gives `2^{(0.161 - O(delta))n}/(4n+2)` nodes. The
sentences in Section 4 ("survive incumbent-based bound tightening") and in
the Section 1.2 framing should be changed accordingly.

Reductions that remove feasible points on other grounds are not covered, even
in this weaker form. Examples are symmetry fixing and dual reductions.

### 2.4 The "What is not covered" remark is too pessimistic

Suppose a node's relaxation region `K_v` is cut by inequalities in the
integer variables that are valid for `Q_v ∩ F`. Then `K_v` is convex and
contains every feasible point of the node, so Lemma 1 still applies. **Cuts in
the integer-variable space, local or global, never remove a conflict between
feasible points.**

Only cuts that involve continuous or epigraph variables can help, because
they raise the projected `phi`. Examples are perspective cuts, rank-one or
2x2 cuts, and OA cuts on the epigraph.

Consequences:

- **Theorem 2** also holds for branch-and-cut with any cuts in `x`,
  including Chvátal–Gomory, split and lift-and-project cuts. Only objective
  (epigraph) cuts could help.
- **Theorem 3** also holds with any cuts in `z` alone. This agrees with
  Theorem 3(c): the hull that closes the gap lives in `(z, beta, t)` space.

## 3. Corollaries 1 and 2

- **Corollary 1(a).** For `mu`-strong convexity,
  `phi(mid) <= (phi(a)+phi(b))/2 - (mu/8)||a-b||^2`, and `||a-b|| >= 1`.
  Correct. On a lattice, `mu/8` can be improved to `mu lambda_1^2/8`.
- **Corollary 1(b).** This is the parallelogram identity
  `||(u+w)/2||^2 = (||u||^2+||w||^2)/2 - ||u-w||^2/4` with `u = Aa - y` and
  `w = Ab - y`. Correct.
- **Corollary 2, bullet 1.** The arithmetic is right: the midpoint of two 0/1
  points at Hamming distance `d` has squared distance `(n-d)/4 <= (n-1)/4`
  from `1/2 * 1`. The proof needs the form in 2.2 (there are no feasible
  points).
- **Corollary 2, bullet 2.** Checked:
  - The tangents of `(x - 1/2)^2` at 0 and 1 are `1/4 - x` and `x - 3/4`.
  - On `[0,1]` their maximum is `|x_i - 1/2| - 1/4`, so the projection is
    `{||x - 1/2 * 1||_1 <= n/2 - 1/4}`.
  - It contains every half-integral non-vertex point: for Hamming distance
    `d`, `(n-d)/2 <= n/2 - 1/4`.
  - It contains no 0/1 point: `n/2 > n/2 - 1/4`.

  This set is the DDM cross-polytope `{||x - 1/2 * 1||_1 <= n/2 - 1/2}` with
  a slightly larger radius. DDM Prop. 3's proof applies verbatim, and with
  binary splits it gives `2^{n+1}-1` nodes. The report should cite DDM Prop. 3
  here rather than present this as new.
- **Corollary 2, bullet 3.** The cuts `z_i >= 1/4` are valid from
  `x_i <= 0 ∨ x_i >= 1`, and `sum z_i >= n/4 > (n-1)/4`. Correct.
- **Novelty.** The report's own "low" rating is right; for bullet 2 I would
  say none. I could not re-read the HBO 2014 paper; see Section 8.

## 4. Theorem 2 (random CVP)

### 4.1 Step-by-step check

1. **Distance to the target.** For uniform `t` on `R^n/L` and `det L = 1`,
   `E|L ∩ B(t,r)| = vol B_r = (r/GH)^n`, where `GH` is the radius of the
   unit-volume ball. Markov's inequality then bounds `P(OPT < (1-delta)^2 GH^2)`.
   Correct.
2. **Shortest vector.** Siegel's mean value theorem (for `n >= 2`, over all
   nonzero vectors) gives `E #{v != 0 : ||v|| <= r} = vol B_r`. Correct. The
   bound can be halved because vectors come in `±v` pairs, but that is not
   needed.
3. **The shell is a clique.**
   - `r0^2 <= OPT + lambda_1^2/4 - eps` on the good event. Correct.
   - For `a != b` in the ball,
     `phi(mid) <= (phi(a)+phi(b))/2 - lambda_1^2/4`.
   - **Fix:** the chain gives only `phi(mid) <= OPT - eps`, while the
     conflict needs `<`. Use the open ball `||Ba - t|| < r0`, or note that
     ties have probability 0 because `t` has a density.
4. **Counting the shell.**
   - For fixed `L`, `E_t N^2 = sum_{v in L} vol(B ∩ (B+v))`. I re-derived
     this by unfolding the torus integral.
   - Siegel applied to `h(v) = vol(B ∩ (B+v))` gives `∫ h = vol(B)^2`. So
     `E N^2 = V' + V'^2` and `Var N = V'`. **Correct.**
   - The union bound needs no independence.
   - Chebyshev gives `P(N < V'/2) <= 4/V'`.
   - This is the standard Poisson-like second moment of a random affine
     lattice.

**Monte Carlo check** (`siegel_variance.py`). This uses Goldstein–Mayer
(Hecke) lattices with `p = 100003`, which approximate Haar measure; see the
table in Section 7. `Var N / V'` is 0.96–1.02 for `n = 3, 4`. For `n = 2` it
is 0.86–1.04; the `n = 2` count distribution is heavy-tailed, and the sample
variance converges slowly there. For fixed typical lattices, `Var_t N` is far
below `V'` (0.9–2.4 at `V' = 8`). The average over `L` is therefore essential,
and it is dominated by rare lattices.

### 4.2 Other points

- **Range of `delta`.** `V > 1` if and only if
  `(1-delta)^2 * 5/4 - delta > 1`, that is, `delta < (3.5 - sqrt 11)/2.5 ≈ 0.0734`.
  For `delta in [0.0734, 0.1)`, which the statement allows, the bound is
  vacuous; it is not false. State `delta in (0, 0.07)`.
- **Rate.** The exponent is `(n/2) log2(5/4 - O(delta)) = (0.161 - O(delta)) n`.
  Correct.
- **`eps <= delta GH^2`.** This is consistent: `r0^2 >= GH^2((1-delta)^2 * 5/4 - delta) > 0`,
  and `OPT - eps > 0` on the good event.
- **"Any basis".** This is automatic. A unimodular change of basis maps
  convex pieces to convex pieces and `Z^n` to `Z^n`, and the conflict relation
  depends only on the lattice vectors `Ba`. Variable fixings in one basis are
  hyperplane branchings in another.

  The claim "lattice reduction cannot help" is correct within the model but
  trivial there. The actual content is "no convex-piece tree helps".
- **Sphere decoders and Lenstra/Kannan-style algorithms.** These enumerate
  only the integer values `c` in a radius interval `I` and never create the
  children outside it, so they are not trees that cover `Q_v ∩ Z^n` literally.

  Add the two pieces `{x_i <= min I - 1}` and `{x_i >= max I + 1}`, which have
  bound `> R^2 >= OPT`; handle an empty interval the same way. This gives a
  model tree with at most `3 N_SD` leaves. So these algorithms need at least
  `V/6` nodes, not `V/2` leaves. The same argument covers LP/OA-based
  relaxations, which are weaker than the continuous one.
- **Robustness.** Section 4 claims robustness to incumbent-based bound
  tightening. This holds only in the node form `V/(2(2n+1))` (Section 2.3).
  Almost all shell points have `f > OPT`, so OBBT with `UB = OPT` may remove
  them.
- **Numerics in Section 3.2.** `cvp_count.py` uses Gaussian bases scaled to
  determinant 1. These lattices are not Haar-distributed, so the table does
  not test Theorem 2's constant. The report says this for MIMO but not in the
  table caption.

## 5. Theorem 3 (correlated pairs)

Let `c = cos th` and `w = (u+v)/||u+v||`. Then `u'y = v'y = s cos(th/2)`, and
`w` is an eigenvector of `uu' + vv'` with eigenvalue `1 + c`. This gives
closed forms, checked against direct 2x2 solves on 200 random `(th, s, lam)`
to within `1.1e-14`:

- `g10 = s^2 (1 + 2 lam - c) / (2(1+lam))`
- `g11 = s^2 lam / (lam + 1 + c)`
- `ĝ(1/2,1/2) = 2 lam s^2 / (2 lam + 1 + c)`
- `delta = g10 - ĝ(1/2,1/2) = s^2 sin^2 th / (2(1+lam)(1 + 2 lam + c))`

Consequences:

- **Condition (ii).** `delta > 0` holds for every `th in (0, pi)`, `s != 0`,
  `lam > 0`. Replace "holds by strict convexity and symmetry, verified
  numerically" with this formula. (Direct strict-convexity argument: the
  second derivative of `y'(A + tE)^{-1} y` is `2 w'EA^{-1}Ew`, which is
  positive because `E = vv' - uu'` has `Ew != 0` for `w != 0`.)
- **Condition (i).** After expansion, (i) is equivalent to
  `c + c^2 > 0`, that is, **`cos th > 0`**, independently of `s` and `lam`.
  At `th = pi/2` it holds with equality and part (a) fails (more optima).
  State the gadget for `th in (0, pi/2)`.
- **Reported numbers.** At `th = 0.3, s = 3, lam = 1`: `delta = 0.04968`,
  `g00 - g10 = 4.3995`, `g10 - g11 = 1.5552`. They reproduce.

Parts (a)–(c):

- **(a)** The exchange argument is correct. If some `b_j = 2`, then some
  `b_i = 0` because `sum b <= k`, and moving one feature changes the value by
  `-(g00 - g10) + (g10 - g11) < 0`. So `OPT = k g10`, attained by exactly the
  `2^k` one-per-block supports.
- **(b)** The perspective objective after minimizing out `beta` is
  `g(z) = y'(I + X diag(z) X'/lam)^{-1} y`. This is the standard formula,
  convex as a matrix-fractional function of an affine argument. It is
  separable across orthogonal blocks.
  - The budget does not break the argument. The midpoint has `sum z = k`, so
    it lies in `K`, and only its value is used.
  - `g(mid) = OPT - |D| delta` is correct.
  - A reduced (symmetrized) node relaxation matches a full 2k-variable
    CVXPY/Clarabel model to `6e-8` on 25 random fixings.
- **(c)** The root value of the 4-term disjunctive relaxation, computed as an
  LP over per-block convex combinations with the budget, equals `k g10`
  (difference at most `7e-15` for `k = 2, 5, 10`). Correct.

**Exact minimum variable-branching trees** (DP over multisets of block
states, `k = 1..8`):

| `eps` | minimum leaves for `k = 1..8` |
|---|---|
| `1e-6` | 2, 6, 14, 30, 62, 126, 254, 510 (`= 2^{k+1} - 2`) |
| `0.9 delta` | 2, 4, 8, 16, 32, 64, 128, 256 (`= 2^k`) |

So Theorem 3(b) is tight for variable branching when `eps` is just below
`delta`, but not as `eps -> 0`.

For `k = 2` I also computed the exact minimum over **arbitrary convex pieces**
covering the 11 feasible supports, that is, the report's partition number:

- At `eps = 1e-6` it is 6. The midpoint graph has clique and chromatic
  number 4. So the hypergraph refinement is strictly stronger here, and
  variable branching is optimal.
- At `eps = 0.9 delta` it is 4.

The scout's most-fractional counts (6, 14, 36, 82, ...) are consistent with
these minima.

**Caveat (not an error).** The gadget has a `Z_2^k` symmetry. Symmetry-breaking
*inequalities* `z_{u_j} >= z_{v_j}` keep the midpoints and do not help, by the
form in 2.2. Symmetry *fixing* `z_{v_j} = 0` makes the root exact. So the
phrase "exponential gain that no branching rule can match" is right about
branching, but a solver with orbital fixing would solve this gadget at once.
A non-symmetric version would be more convincing: perturb the blocks so that
`delta_j > 0` but the one-per-block supports have distinct values within `eps`.

## 6. Lemma 4 (path lemma)

The proof is correct under its stated hypotheses:

- the relaxation is monotone under added fixings (automatic for
  `inf_{K ∩ Q_v} phi`);
- the incumbent value is `OPT`;
- the rule branches only on unfixed binaries.

Nodes that do not contain `z°` have some wrong fixing, so their bound is at
least the single-fixing bound, which is `>= OPT - eps`. The nodes that contain
`z°` form a path with one pruned sibling per branching. Hence the tree has
`2D + 1 <= 2p + 1` nodes.

Answers to the specific questions:

- **Monotonicity is enough.** No other property of the relaxation is used.
- **Node order and the incumbent.** Best-bound order is not needed, but the
  incumbent `OPT` must be known when off-path children are evaluated; they
  must be pruned when created or when selected.
  - Without an initial incumbent, depth-first search can explore wrong
    subtrees.
  - Best-bound order alone does not suffice for `eps > 0`. An off-path node with bound in
    `[OPT - eps, OPT)` can be selected before `z°` is found, and it is then
    branched because `UB = inf`.
  - Example (`lemma4_order.py`): `phi = sum (z_i - 0.1)^2`, `p = 10`, C1
    holds. Depth-first search that explores the `z_i = 1` child first uses
    21 nodes with incumbent `OPT` and 351 without.
- **Wording.** State the incumbent assumption in the summary and in Section 4
  ("for all branching rules").
- **"C1 is weaker than root exactness".** Correct: root exactness gives root
  bound `OPT`, and monotonicity gives C1.

## 7. Computations run (targeted, local only)

All commands ran from `research-20260928b/reviews/bb-conflict/` with Python
3.13, NumPy 2.5, SciPy 1.18 and CVXPY 1.9 (Clarabel). Floating point only.
These are my runs, not CI results; no project-wide checks were run and CI was
not inspected.

**`python3 thm3_gadget.py 8`** (`thm3_gadget.log`):

- closed forms versus numeric;
- conditions (i) and (ii) on 200 random parameter sets;
- reduced relaxation versus CVXPY;
- hull root value;
- the `k = 2` partition number;
- exact minimum variable-branching trees for `k = 1..8` at two values of
  `eps`.

**`python3 thm3_k2_extra.py`** (`thm3_k2_extra.log`): for `k = 2`, the
midpoint clique and chromatic numbers versus the partition number.

**`python3 thm1_bruteforce.py`** (`thm1_bruteforce.log`, `.jsonl`): 140
random instances of `min ||Ax - y||^2` over the integer points of a box.

- The chain `omega_mid <= chi_mid <= chi_seg <= part <= L_var` held in all
  60 instances on `[0,2]^2`. Here `part` is the exact partition number over
  arbitrary convex pieces and `L_var` is the exact minimum variable-branching
  tree.
- `omega_mid <= L_var` held in all 140 instances.
- `part == L_var` in 45 of 60.
- The OBBT counterexamples and the `chi/(2n+1)` node bound are reported in
  Section 2.3.

**`python3 siegel_variance.py`** (`siegel_variance.log`): Goldstein–Mayer
lattices, `p = 100003`.

| `n` | `V'` | samples | mean `N` | `Var N` | `Var/V'` |
|---:|---:|---:|---:|---:|---:|
| 2 | 2 | 40000 | 1.991 | 1.850 ± 0.064 | 0.93 |
| 2 | 8 | 40000 | 8.008 | 8.32 ± 1.2 | 1.04 |
| 2 | 20 | 40000 | 19.997 | 17.1 ± 1.5 | 0.86 |
| 3 | 2 | 40000 | 2.005 | 2.044 ± 0.046 | 1.02 |
| 3 | 8 | 40000 | 7.995 | 7.87 ± 0.21 | 0.98 |
| 3 | 20 | 40000 | 19.990 | 19.2 ± 0.7 | 0.96 |
| 4 | 2 | 20000 | 1.989 | 1.991 ± 0.043 | 1.00 |
| 4 | 8 | 20000 | 8.008 | 8.15 ± 0.23 | 1.02 |
| 4 | 20 | 20000 | 19.966 | 19.7 ± 0.7 | 0.98 |

For six fixed lattices (`n = 3`, `V' = 8`, 4000 targets each), the mean was
7.97–8.03, but `Var_t N` was only 0.88–2.37. The identity
`E_L Var_t N = V'` therefore comes from rare lattices with short vectors. The
Chebyshev bound `4/V'` is valid but loose: the observed `P(N < V'/2)` was
0.02–0.05 for `V' = 8` and `20`.

**`python3 lemma4_order.py`** (`lemma4_order.log`): the node-order example in
Section 6.

## 8. Novelty assessment

The web-search quota was exhausted (200/200) before this review started, and
the Semantic Scholar API returned HTTP 429. I used WebFetch on arXiv abstract,
PDF and listing-search pages, plus the local library.

**Sources examined, and what they contain:**

- **DDM, "Lower bounds on the size of general branch-and-bound trees"**
  (local `dey2023-lower-bounds-on-the-size`; I read Sections 2–6).
  - Prop. 3 is the midpoint argument for the cross-polytope. Two integer
    points in a leaf give a half-integral point in the atom.
  - Lemma 7 is a Helly-type "generalized Dadush–Tiwari" argument.
  - Section 6 reuses half-integral points for perturbed cross-polytopes.
  - Everything is linear and infeasibility-based. There are no conflicts
    between *feasible* points and no curvature.
- **Dadush–Tiwari, arXiv 2006.04124** (abstract): branching proofs of integer
  infeasibility of polytopes; a lower bound of `2^n/n`, which DDM restate as
  Helly-based. No objective, not nonlinear.
- **Beame et al., "Stabbing Planes", arXiv 1710.03219** (full text via
  `pdftotext`). The paper states it is "unable to establish size lower bounds"
  and gives depth/rank lower bounds via real communication complexity. There
  is no midpoint argument.
- **Fleming–Göös–Impagliazzo–Pitassi–Robere–Tan–Wigderson, arXiv 2102.05019**
  (full text, grep): lower bounds for SP* via translation to Cutting Planes.
  Superpolynomial size lower bounds for SP are stated as open. No objective or
  nonlinear setting.
- **Gläser–Pfetsch** (local): interpolation, linear.
  **Krishnamoorthy–Pataki 2009** (local): lower bounds for ordinary
  (variable-branching) B&B on knapsacks, linear.
- **Hanrot–Stehlé, arXiv 0705.0965** (abstract): complexity analysis of
  Kannan's fixed-enumeration algorithm.
- **Aono–Nguyen–Seito–Shikata, ePrint 2018/586** (abstract): lower bounds for
  enumeration with extreme pruning on a fixed basis and order, via cylinder
  intersections.
- **Seethaler–Jaldén–Studer–Bölcskei, arXiv 0905.1215** (abstract):
  sphere-decoding complexity tails for Gaussian bases, not improved by lattice
  reduction. This is still fixed-order enumeration.
- **Jaldén–Ottersten 2005: not accessible.** From memory, it proves
  exponential expected complexity for fixed-order sphere decoding at fixed SNR.
- **arXiv listing searches** (by WebFetch):
  - "branch-and-bound lower bound integer least squares": 1 irrelevant hit.
  - `"branch-and-bound" "lower bound" "tree size"`: 0 hits.
  - `"sphere decoding" complexity lower bound`: 5 hits, all fixed-decoder
    results.
  - `"general branch-and-bound"`: 10 hits (DDM, Gläser–Pfetsch, Dash–Dubey;
    none nonlinear).
  - `branch-and-bound "mixed-integer convex" complexity nodes`: 0 hits.
  - "branch-and-bound lower bound nodes convex quadratic integer": 1
    irrelevant hit.
  - "perspective relaxation branch-and-bound nodes lower bound": 1 irrelevant
    hit.
- **Local perspective and indicator papers** (Han–Gómez–Atamtürk 2x2;
  Atamtürk–Gómez 2018 and 2020; Wei–Gómez–Küçükyavuz 2021; Bestuzheva et al.
  perspective cuts): node counts are empirical only; none has a tree-size
  theorem.
- **Hijazi–Bonami–Ouorou 2014: not in the local library.** The local
  `hijazi2012` is the on/off-constraints paper. Lubin et al. 2016 (local)
  confirm the `2^n`-tangent ball example and the `2n`-hyperplane extended
  formulation. I could not verify the HBO remark on OA branch-and-cut node
  counts.

**Assessment:**

- **Lemma 1 / Theorem 1.** The mechanism is DDM Prop. 3 (and HBO's
  edge-midpoint lemma). The new element is using objective curvature to create
  conflicts among *feasible* points, which is impossible for linear objectives,
  together with the partition characterization. No prior statement was found
  in the sources above. It is a natural, short extension; novelty is
  low to moderate.
- **Theorem 2.** No branching-independent lower bound for CVP or integer least
  squares was found. All lattice and sphere-decoding lower bounds examined are
  for fixed-order enumeration. The variance step is standard (Siegel's theorem
  for random affine lattices). This is the most interesting item. Novelty is
  moderate as a statement; the proof is short.
  - For contrast, a slab-covering (Bang plank) argument would give only about
    `2 GH · lambda_1(L*) = Θ(n)` queries. So the midpoint route is the right
    tool here. This is my estimate, not from a source.
- **Theorem 3.** A gadget; the weakness it exhibits is folklore. The
  branching-independent `2^k` statement was not found. Low to moderate
  novelty.
- **Lemma 4.** An elementary observation about probing. Likely folklore. Low
  novelty.
- **Corollary 2.** No novelty; bullet 2 is DDM Prop. 3.

An unsuccessful bounded search does not establish novelty. In particular, I
did not see the lattice-algorithm literature on Lenstra-type and M-ellipsoid
enumeration (Dadush–Peikert–Vempala) or the proof-complexity literature
beyond the papers named above.

## 9. Corrections to make in the scout report (when it is revised)

1. **Section 3.1, Robustness remark, and Section 4, "survive incumbent-based
   bound tightening".** Replace with the node form: if reductions remove only
   regions of relaxation value `>= OPT - eps` via variable bounds, then
   `#nodes >= chi/(2n+1)`. Add the 1D counterexample as the reason the leaf
   form fails.
2. **Theorem 1.** Add the form in which endpoints need not be feasible
   (conflict whenever `(a+b)/2 in K` and `phi((a+b)/2) < OPT - eps`, for integer
   points that must be covered). Use it in Corollary 2. Optionally use segment
   minima instead of midpoints. State that the tree is finite, and that
   covering `F` suffices.
3. **"What is not covered".** Integer-space cuts valid for the node's feasible
   points are covered. Only cuts involving continuous or epigraph variables,
   and reductions that remove feasible points, are not.
4. **Theorem 2.**
   - Use `delta in (0, 0.07)`.
   - Make the conflict strict (open ball, or almost surely).
   - For sphere decoders and Lenstra/Kannan-type algorithms, state
     `>= V/6` nodes (implicit children).
   - Note that "any basis" is automatic.
   - Say that the Section 3.2 numerics use Gaussian bases, not Haar lattices.
5. **Theorem 3.**
   - Replace the numerical verification of (ii) with the closed form of
     `delta`.
   - State (i) as `th in (0, pi/2)`.
   - Optionally add the exact minima (`2^k` at `eps` near `delta`;
     `2^{k+1}-2` at `eps -> 0`).
   - Add the symmetry caveat.
6. **Lemma 4 and summary.** "Any node order" requires the incumbent `OPT` when
   off-path children are evaluated.
7. **Corollary 2, bullet 2.** Cite DDM Prop. 3 and note that the projection is
   a cross-polytope.
8. **Lemma 1.** `min` → `inf`.

## 10. What remains unchecked

- The HBO 2014 paper itself (Example 1, Lemma 2.1, the OA branch-and-cut
  remark), and Jaldén–Ottersten 2005: not accessible.
- A full proof-complexity literature sweep (web search unavailable), including
  Lenstra-type and M-ellipsoid enumeration lower bounds and any 2025–2026
  work on nonlinear B&B tree sizes not indexed by the arXiv queries above.
- Section 3.5 (heuristic DDM mechanism) and the Section 3.6 computations
  (sparse regression, MIMO, cliques from B&B pools). I did not rerun or audit
  the scout's scripts.
- Section 3.2's heuristic `(3/2)^{n/2}` target and the `1.17^n` greedy-clique
  growth.
- Exact-arithmetic verification. All computations are floating point, with
  tolerances around `1e-7`–`1e-9`. The DP margins (`delta ≈ 0.05`) are far
  above these tolerances.
