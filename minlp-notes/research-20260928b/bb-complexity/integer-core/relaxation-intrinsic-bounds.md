# Relaxation-intrinsic lower bounds for integer branching with convex relaxations

Workstream `integer-core` of the
[relaxation-intrinsic B&B program](../PROGRAM.md). Date: 2026-09-28.
Status: revised after the independent review
[`integer-core-review.md`](../../reviews/integer-core-review.md). Section 9
lists every change made in response. The starting point was the scout report
[`bb-tree-size-convex.md`](../../scouting/bb-tree-size-convex.md)
(Sections 1–3) and the independent review
[`bb-conflict-review.md`](../../reviews/bb-conflict-review.md). Every
correction from that review is incorporated here (see Section 7.3). Check
scripts and logs are in this directory; Section 6 lists the commands.

## Summary

The note develops one lower-bound mechanism for branch-and-bound (B&B) with
integer branching and a convex node relaxation, and tests how far it reaches.

**Framework (Section 1).**

- Theorem 1.6: every tree whose leaves carry convex sets that cover the
  required integer points, and whose leaves all have relaxation bound at least
  `tau = OPT - eps`, has at least `kappa_tau` leaves. Here `kappa_tau`, the
  *class number*, is the minimum number of classes of integer points whose
  convex hulls have relaxation value at least `tau`. The midpoint-conflict
  clique of the scout report is a lower bound on `kappa_tau`.
- Theorem 1.7: `kappa_tau` is *exactly* the minimum number of leaves when
  arbitrary convex pieces may be used as children. Such trees exist with
  multiway branching and also with binary branching. The binary tree uses
  hemispaces (convex sets with convex complements) as leaves. The earlier
  "caterpillar" of hulls was invalid (Section 9).
- Theorem 1.8: the bound is unchanged by cuts in the integer variables that
  are valid for the node's feasible points, including the node's integer hull.
  It is also unchanged by domain reductions that remove only points outside
  the relaxation. Incumbent-based reductions (OBBT, reduced-cost fixing,
  probing) break the leaf form, as the review's counterexample shows. They
  keep a counting form: `kappa_tau <= #leaves + #certified removals`. This
  gives `#nodes >= kappa_tau / (2n+1)` for one tightening pass per node,
  `#nodes >= kappa_tau / (n+1)` for binaries, and
  `#leaves >= kappa_tau - 2n` for one pass at the root only. Changes of
  the relaxation in the continuous or epigraph variables are not covered.
  They are the only way to lower `kappa_tau`.

**Tightness for split and variable branching (Section 2). The answer is
negative in general.**

- Proposition 2.1: for a pure integer linear program with integral data and
  `m` constraints, `kappa_tau <= m + 1`. For mixed-integer linear programs,
  `kappa_tau` is at most the number of facets of the projected sublevel
  polyhedron. So the class number of a compact *pure* integer linear
  program is always polynomial. This is false for compact MILPs: an MILP
  with `2n` rows can have `kappa_tau = 2^n` (Example 2.1a).
- Theorem 2.3: combined with the Gläser–Pfetsch lower bound, this gives
  compact pure-binary instances with `kappa_tau <= L`, where `L` is the
  encoding length. For these instances every split-disjunction tree has
  `2^{n^{1/6 - o(1)}} = 2^{L^{Omega(1)}}` nodes, where `n` is the number of
  variables. The instances can be stated as feasibility problems, or as MILPs
  with one continuous variable. In the MILP form the projected relaxation is
  an unconstrained convex (piecewise-linear) function. So Q3(i) of the scout
  report ("split-tree size `<= poly * kappa^{O(1)}`") is false, even for
  unconstrained convex objectives.
- Proposition 2.4: a quadratic version of Jeroslow's instance has
  `kappa_tau = 2` and a 3-node split tree, but every variable-branching tree
  has at least `C(n+1, (n+1)/2) ~ 2^{n+1}/sqrt(pi n/2)` leaves. The count is
  exact when no branching repeats an already-fixed variable and no node with
  bound at least `tau` is branched.
- Theorem 2.2: for an unconstrained convex objective, `kappa_tau` equals the
  minimum number of facets of a lattice-free polyhedron containing the open
  sublevel set. Hence
  `1 <= omega_mid <= kappa_tau <= 2^n` for every such instance.
- Proposition 2.5: in fixed dimension, split trees have size bounded in terms
  of `n` alone.
- Whether split-tree size is polynomial in `kappa_tau` for convex
  *quadratic* objectives (ellipsoidal sublevel sets) is left open (Open
  problem 2.6). For general unconstrained convex objectives the answer is
  already negative (Theorem 2.3(b)). None of the known split-tree lower-bound
  techniques applies to a single convex quadratic.

**Random closest vector problem (Section 3).** The model is a Haar-random
unimodular lattice, a uniform target, and the continuous relaxation. With
high probability:

- Theorem 3.4: the midpoint-conflict clique number `omega` is at least
  `2^{(0.2075 - o(1)) n}`, with base `(4/3)^{1/2}`. This improves the scout's
  `(5/4)^{1/2}` and needs no bound on `lambda_1`.
- Theorem 3.5: `kappa_tau >= 2^{(0.2925 - o(1)) n}`, with base
  `(3/2)^{1/2}`. Its per-leaf counting mechanism is the one DDM use for the
  perturbed cross-polytope.
- Proposition 3.6: `omega <= 2^{(0.2612 + o(1)) n}` (via the
  Kabatiansky–Levenshtein bound) and `kappa_tau <= 2^{(1/2 + o(1)) n}`.
- Hence the scout's target `(3/2)^{n/2}` is **false for midpoint cliques**
  but **true for the class number**. The class number is exponentially
  larger than the midpoint clique on random CVP. The chromatic number and
  the segment graph are not bounded here.
- Gaussian-basis lattices are not covered. Section 3.6 identifies the
  obstacle: exponentially many short lattice vectors. The obstacle becomes
  decisive only for `n` above about 50. The numerics at `n <= 32` show only
  its onset.

**Perspective versus pairwise hull (Section 4).**

- Closed forms, including
  `delta = s^2 sin^2(th) / (2(1+lam)(1+2 lam + cos th))`.
- A full proof of the `2^k` bound and of the root exactness of the pairwise
  hull.
- An asymmetric variant with a unique optimum and no symmetry, so orbital
  fixing does not apply, that keeps the `2^k` bound.
- Everything is verified in exact rational arithmetic.

**Path lemma (Section 5).**

- A version for general integer variables, with the incumbent hypothesis made
  explicit.
- Condition C1 is equivalent to "root probing with the optimal incumbent fixes
  every variable". C1 implies `kappa_tau <= 2n + 1`, and variable-branching
  trees then have at most `2n + 1` nodes for binaries. The two can differ by
  a factor of about `n`, not 2 as first claimed (Proposition 5.2(b)).

**Open parts (Section 8).**

- Split trees versus `kappa_tau` for convex quadratic objectives.
- The true exponents of `omega` and `kappa_tau` for random CVP. We conjecture
  `kappa_tau = 2^{(1/2 + o(1)) n}`.
- Gaussian-basis lattices.

**Novelty.** Prior mechanisms:

- The pairwise argument is the Dey–Dubey–Molinaro (DDM) midpoint argument and
  the Kaibel–Weltge hiding-set argument.
- The non-pairwise counting bound ("each leaf contains at most `X` of these
  points") is DDM's argument for the perturbed cross-polytope (their
  Section 6, Lemma 12).
- Gläser–Pfetsch already used hiding sets for variable-branching trees.
- In the linear infeasibility case, `kappa` is a relative relaxation
  complexity in the sense of Kaibel–Weltge and Averkov et al.

The new elements are:

- conflicts created by objective curvature among feasible points;
- the class number as the exact semantic tree size;
- its separation from split trees;
- the random-CVP exponents and the cap estimate;
- the asymmetric perspective gadget.

Section 7 records the sources examined. A bounded search does not establish
novelty.

## 0. Conventions

- `n` is the number of integer variables and `d` the number of continuous
  variables.
- `B°(c, r)` is the open Euclidean ball and `B(c, r)` the closed one.
- `vol` is Lebesgue measure and `omega_n = vol B(0,1)`.
- `conv` is the convex hull and `[a, b]` a closed segment.
- `inf` of the empty set is `+inf`, and `phi` takes the value `+inf` outside
  its domain.
- "With high probability" (w.h.p.) means with probability `1 - o(1)` as
  `n -> inf`, with explicit bounds where stated.
- `log2` is the binary logarithm.

## 1. Framework

### 1.1 Problem, relaxation, node bound

The problem is

```
(P)   OPT = inf { f(x, y) : (x, y) in C, x in Z^n },   C ⊆ R^n x R^d.
```

`F = { x in Z^n : there is y with (x, y) in C }` is the set of feasible integer
parts, and `f(x) = inf_y { f(x, y) : (x, y) in C }` for `x in F`. `OPT = +inf`
means (P) is infeasible.

A *convex relaxation* is a convex set `K^ ⊇ C` together with a convex
function `phi^ : K^ -> R ∪ {-inf}` satisfying `phi^ <= f` on `C`. Its
*projection* onto the integer variables is

```
phi(x) = inf { phi^(x, y) : (x, y) in K^ }   (= +inf if there is no such y),   K = proj_x K^.
```

`phi` is convex on `R^n` because it is the infimal projection of the jointly
convex function `phi^ + indicator(K^)`. It satisfies `phi <= f` on `F`. For a
set `Q ⊆ R^n`, the *relaxation bound* of `Q` is

```
r(Q) = inf { phi(x) : x in Q } = inf { phi^(x, y) : (x, y) in K^, x in Q }.
```

This is the value of the node relaxation when branching constraints restrict
only `x`. Everything below depends on the relaxation only through `phi`.

We also use the exactness condition

```
(E)   phi(z) >= OPT   for every z in Z^n.
```

(E) holds for the *natural* relaxation of a convex MINLP, where
`C = K^ ∩ (Z^n x R^d)` and `phi^ = f`. In that case `K ∩ Z^n = F`, and for
`z in F` we have `phi(z) = f(z) >= OPT`.

### 1.2 Trees and certificates

**Definition 1.1 (P-covering convex-piece tree).** Fix a set of integer points
`P` with `F ⊆ P ⊆ Z^n`. This is the set of integer points the branching must
keep. `P = F` suffices for disjunctions that only need to cover feasible
points, such as SOS branching. `P = Z^n ∩ box` is the usual choice for variable
and split branching on a bounded domain. A P-covering convex-piece tree is a
finite rooted tree `T` with the following properties.

- Each node `v` carries a convex set `Q_v ⊆ R^n` (not necessarily closed),
  and `P ⊆ Q_root`.
- For each internal node `v` with children `w_1, ..., w_k` (`k >= 1`),
  `Q_v ∩ P ⊆ Q_{w_1} ∪ ... ∪ Q_{w_k}`.
- The *effective set* of `v` is `Q̄_v`, the intersection of `Q_u` over all
  nodes `u` on the path from the root to `v`. It is convex. The node bound is
  `r(v) = r(Q̄_v)`. If the sets are nested, then `Q̄_v = Q_v`. Using `Q̄_v`
  covers solvers that inherit bounds from ancestors.

This covers the following branching schemes:

- variable branching `x_i <= c ∨ x_i >= c+1`;
- split branching `pi.x <= pi_0 ∨ pi.x >= pi_0 + 1` with `pi in Z^n` and
  `pi_0 in Z`;
- multiway hyperplane branching `{pi.x = c}` over all integers `c`, with the
  two tails as pieces;
- SOS branching with `P = F`;
- "semantic" branching into arbitrary convex pieces.

**Definition 1.2 (certificates).** For a threshold `tau in [-inf, +inf]`, a
tree is a `tau`-*certificate* if every leaf `l` has `r(l) >= tau`. An
`eps`-*certificate* is a `(OPT - eps)`-certificate, with `eps >= 0`. A proof of
infeasibility is a `(+inf)`-certificate, meaning every leaf has `Q̄_l ∩ K = ∅`.

**Lemma 1.3 (B&B runs give certificates).** Consider a completed B&B run on
such a tree that prunes a node `v` only by one of the following rules:

- (i) infeasibility of the node relaxation;
- (ii) bound: `beta(v) >= UB_t - eps`, where `beta(v) <= r(v)` is any valid
  computed lower bound and `UB_t` is the incumbent value when `v` is pruned;
- (iii) integrality: the relaxation optimum `(x^, y^)` is feasible for (P) and
  `phi^(x^, y^) = f(x^, y^)`.

Then the tree is an `eps`-certificate.

*Proof.* Every incumbent value is the value of a feasible solution, so
`UB_t >= OPT`.

- In case (i), `r(v) = +inf`.
- In case (ii), `r(v) >= beta(v) >= UB_t - eps >= OPT - eps`.
- In case (iii), `r(v) = f(x^, y^) >= OPT`. ∎

The lower bounds below therefore do not depend on the branching rule, the
node selection rule, the incumbent heuristics, or the use of weaker computed
bounds.

### 1.3 Classes and conflicts

**Definition 1.4.** Fix `tau` and `P`.

- A set `I ⊆ P` is `tau`-*admissible* if `r(conv I) >= tau`. Admissibility
  is hereditary, since `J ⊆ I` implies `conv J ⊆ conv I`.
- The *class number* `kappa_tau(P)` is the least cardinality of a family of
  admissible sets whose union is `P`. By heredity we may take the family to
  be a partition.
- The *midpoint graph* `G^mid_tau(P)` has vertex set `P` and edges
  `a ~ b` (with `a != b`) iff `phi((a+b)/2) < tau`.
- The *segment graph* `G^seg_tau(P)` has the same vertices and edges
  `a ~ b` iff `inf_{[a,b]} phi < tau`.

Because `phi = +inf` off `K`, a conflict requires the midpoint (or a point of
the segment) to lie in `K`. The endpoints themselves need not be in `K` or in
`F`.

**Lemma 1.5 (graph bounds and a counting bound).**

- (a) `omega(G^mid) <= omega(G^seg) <= chi(G^seg) <= kappa_tau(P)` and
  `chi(G^mid) <= chi(G^seg)`.
- (b) For every finite `S ⊆ P`,
  `kappa_tau(P) >= |S| / max { |I ∩ S| : I admissible }`.

*Proof.*

- (a) The midpoint lies on the segment, so `G^mid ⊆ G^seg`. If `a, b` lie in
  an admissible `I`, then `[a, b] ⊆ conv I`, so `inf_{[a,b]} phi >= tau` and
  `a, b` do not conflict. So a partition into `kappa` admissible classes is a
  proper coloring of `G^seg`.
- (b) The classes cover `S`, and each class covers at most the maximum. ∎

**Theorem 1.6 (leaf lower bound).** Every P-covering `tau`-certificate has at
least `kappa_tau(P)` leaves.

*Proof.* Let `p in P`. Then `p in Q_root`. If `p in Q_v` and `v` is internal,
some child of `v` contains `p`. Because the tree is finite, `p` reaches a leaf
`l(p)` along a path all of whose sets contain `p`, so `p in Q̄_{l(p)}`.

For a leaf `l`, let `I_l = { p : l(p) = l }`. Then `I_l ⊆ Q̄_l`, and
`Q̄_l` is convex, so `conv I_l ⊆ Q̄_l` and

```
r(conv I_l) >= r(Q̄_l) = r(l) >= tau.
```

So the nonempty sets `I_l` are admissible classes covering `P`, and there are
at most as many of them as there are leaves. ∎

**Lemma 1.7a (hemispaces; Kakutani 1937, Stone).** Let `A, B ⊆ R^n` be
disjoint convex sets. Then there is a convex set `G` with `A ⊆ G`,
`B ∩ G = ∅`, and `R^n \ G` convex. Such a `G` is called a *hemispace*.

*Proof.* We prove the statement in any affine space `V` of dimension `d`, by
induction on `d`.

- **Trivial cases.** If `A = ∅`, take `G = ∅`. If `B = ∅`, take `G = V`.
  This covers `d = 0`.
- **Separation.** Otherwise `A - B` is convex and does not contain `0`, so
  `0` is not in the relative interior of `A - B`. By proper separation in
  finite dimension (Rockafellar, Theorem 11.3), there are a *non-constant*
  affine functional `g` on `V` (its linear part is nonzero) and a number
  `alpha` with `g >= alpha` on `A` and `g <= alpha` on `B`. Then
  `H = {g = alpha}` is a hyperplane of `V`, of dimension `d - 1`.
- **Induction.** By induction, `H` has a hemispace `G'` with `A ∩ H ⊆ G'` and
  `B ∩ H ∩ G' = ∅`. Put `G = {g > alpha} ∪ G'`.
- **`G` is convex.** Take a convex combination with weight in `(0,1)` of two
  points of `G`. If one of them has `g > alpha`, the combination does too.
  If both lie in `G'`, the combination lies in `G'`.
- **The complement is convex.** `V \ G = {g < alpha} ∪ (H \ G')`, and
  `H \ G'` is convex. The same argument applies.
- **Separation of `A` and `B`.** `A ⊆ G`, because points of `A` with
  `g = alpha` lie in `A ∩ H ⊆ G'`. `B ∩ G = ∅`, because
  `B ⊆ {g <= alpha}` and `B ∩ H` misses `G'`. ∎

**Theorem 1.7 (exactness for arbitrary convex pieces).** Let
`I_1, ..., I_kappa` be a minimum admissible partition of `P`, with
`kappa = kappa_tau(P) < inf`. Let `E = {x : phi(x) < tau}`. `E` is convex,
and `E ⊆ K` because `phi = +inf` off `K`.

- **(a) Multiway.** The depth-one tree with root `Q_root = R^n` and children
  `conv I_1, ..., conv I_kappa` is a P-covering `tau`-certificate with
  `kappa` leaves. So the minimum number of leaves over all P-covering
  `tau`-certificates is `kappa_tau(P)`.
- **(b) Binary.** By admissibility, `conv I_j ∩ E = ∅`. By Lemma 1.7a,
  choose hemispaces `G_j ⊇ conv I_j` with `G_j ∩ E = ∅`. Build a chain as
  follows.
  - Let `N_0 = R^n` and `N_j = N_{j-1} \ G_j` for
    `j = 1, ..., kappa - 2`.
  - Node `N_{j-1}` has the two children `G_j` (a leaf) and `N_j`.
  - Node `N_{kappa-2}` has the two children `G_{kappa-1}` and `G_kappa`.
  - If `kappa = 1`, the tree is the single node `G_1`. Its set contains
    `P = I_1`, so it can serve as the root. If `P` is finite, `conv P` also
    works.

  This is a binary P-covering `tau`-certificate with `kappa` leaves and
  `2 kappa - 1` nodes. For `kappa = 2` the root `N_0 = R^n` has the two
  leaves `G_1` and `G_2`.
- **(c) Closed and polyhedral pieces.**
  - (i) If `P` is finite, replace every node set `S` by `conv(S ∩ P)`. All
    sets become polytopes, and the tree remains a certificate.
  - (ii) Suppose `E` is open, for example when `K = R^n` and `phi` is finite.
    Then the `G_j` can be taken to be closed halfspaces, and the internal
    nodes `N_j` are then open polyhedra.
  - (iii) Suppose in addition that `phi` is differentiable and that
    `xh_j in argmin_{conv I_j} phi` exists, for example when `I_j` is finite.
    Then one can take the explicit halfspace
    `G_j = {x : grad phi(xh_j).(x - xh_j) >= 0}`.
  - (iv) For MILP relaxations closed halfspaces also suffice, even though
    `E` need not be open. There `K` is polyhedral and `phi` is the projection
    of a linear objective. So `E` is a partially open polyhedron: a finite
    intersection of closed and open halfspaces, since Fourier–Motzkin
    elimination preserves this form. For finite `I_j`, Motzkin's
    transposition theorem applied to the infeasible system
    "`x in conv I_j` and `x in E`" gives a linear `g` and a number `alpha`
    with `g.x <= alpha` on `conv I_j` and `g.x > alpha` on `E`.
  - Genuine hemispaces are needed only in non-polyhedral cases where `E` is
    not open. The recheck gives an example with a convex, non-lower
    semicontinuous `phi` on a square, where no halfspace can serve as a
    leaf.

*Proof.*

- **(a)** The children cover `P`, and each leaf has
  `r(conv I_j) >= tau`.
- **(b), convexity.** `N_j` is the intersection of the complements of
  `G_1, ..., G_j`, all of which are convex. So `N_j` is convex.
- **(b), covering.** At `N_{j-1}` the covering condition holds because
  `N_j = N_{j-1} \ G_j`, so `N_{j-1} ⊆ G_j ∪ N_j`. At the last internal
  node,
  `N_{kappa-2} ∩ P ⊆ P \ (G_1 ∪ ... ∪ G_{kappa-2}) ⊆ I_{kappa-1} ∪ I_kappa ⊆ G_{kappa-1} ∪ G_kappa`.
- **(b), bounds.** Every leaf has effective set contained in some `G_j`.
  Since `G_j ∩ E = ∅`, we have `phi >= tau` on `G_j`, so `r >= tau`.
- **(c)(i)** Every node set `S` is convex. Hence `conv(S ∩ P) ⊆ S` and
  `conv(S ∩ P) ∩ P = S ∩ P`. The covering relations and the lower bounds on
  the leaves are therefore preserved.
- **(c)(ii)** Strict separation from the open convex set `E` works as in the
  proof of Theorem 2.2(a).
- **(c)(iii)** First-order optimality of `xh_j` over `conv I_j` gives
  `conv I_j ⊆ G_j`. Convexity gives
  `phi(x) >= phi(xh_j) + grad phi(xh_j).(x - xh_j) >= phi(xh_j) >= tau` on
  `G_j`. If `grad phi(xh_j) = 0`, then `phi >= tau` everywhere, so
  `kappa = 1`. ∎

**The earlier binary construction was invalid.** The first version used a
"caterpillar": `conv I_1` as a leaf and `conv(I_2 ∪ ... ∪ I_kappa)` as an
internal node, then recursion. This can violate the covering condition,
because `conv(I_2 ∪ ... ∪ I_kappa)` may contain a point of `I_1` that lies in
neither child. The review gives an exact example, which
`check_revision.py` (R1) re-verifies.

- `phi = ||Ax - y||^2` with `A = [[-2, 1], [3, 3]]` and `y = (-3/5, 18/7)`.
- `P = {0..3} x {0..2}` and `eps = 1/20`.
- The classes are
  `I_1 = {(0,1), (0,2), (1,1), (1,2), (2,1), (3,1), (3,2)}`,
  `I_2 = {(0,0)}` and `I_3 = {(1,0), (2,0), (2,2), (3,0)}`.
- The point `(1,1)` of `I_1` lies in `conv(I_2 ∪ I_3)`, but in neither
  `conv I_2` nor `conv I_3`.

The hemispaces are needed because the complement of a union of convex hulls
is not convex in general.

*Remark.* The children in Theorem 1.7 are *semantically* valid: they cover
`P`, but checking this is itself a statement about the integer points in the
node. A proof system needs *syntactically* valid disjunctions, such as splits,
which cover `Z^n` for trivial reasons. Section 2 shows that the two notions
can differ exponentially. `kappa_tau` measures the part of B&B cost that is
forced by the relaxation alone.

### 1.4 Which solver operations preserve the bound

**Theorem 1.8.** Consider a B&B run, as in Lemma 1.3, that may also use the
operations below at any node. Let `L` and `N` be its numbers of leaves and
nodes.

- **(a) Cuts in the integer variables.** Suppose the relaxation at node `v`
  is taken over `Q̄_v ∩ S_v`. Here `S_v` is the intersection of convex sets,
  each containing `Q̄_u ∩ F` for the node `u` where the cut was added (`u` an
  ancestor of `v`, or `v` itself). This includes global cuts, local cuts, and
  even `S_v = conv(Q̄_v ∩ F)`. Then `L >= kappa_tau(F)`.
- **(b) Feasibility-based reductions.** These replace `Q_v` by a convex
  `Q'_v` with `Q̄_v ∩ F ⊆ Q'_v`. Examples are FBBT on the constraints, also
  with integer rounding of bounds, and probing for infeasibility. They are a
  special case of (a), so `L >= kappa_tau(F)`.
- **(c) Relaxation-certified removal of integer points.** At node `v` the
  solver performs a finite sequence of removals
  `Q̄_v = Q^(0) ⊇ Q^(1) ⊇ ... ⊇ Q^(s_v) = Q'_v` of convex sets.
  - Each step is certified relative to the *current* set: there is a convex
    `D_{v,i}` with `Q^(i-1) ∩ P ⊆ Q^(i) ∪ D_{v,i}` and
    `r(Q^(i-1) ∩ D_{v,i}) >= tau`.
  - Removals certified simultaneously on the unreduced set are also
    covered. The certificate then reads
    `Q̄_v ∩ P ⊆ Q'_v ∪ D_{v,1} ∪ ... ∪ D_{v,s_v}` with
    `r(Q̄_v ∩ D_{v,i}) >= tau`.

  Then `kappa_tau(P) <= L + sum_v s_v`. For bound tightening, one removal is
  one change of one bound of one variable, by any amount.
  - With *one tightening pass per node*, each of the `2n` bounds changes at
    most once, so `s_v <= 2n` and `N >= kappa_tau(P)/(2n+1)`. With one pass
    at the root only, `L >= kappa_tau(P) - 2n`.
  - With *iterated passes* (propagation or OBBT repeated until a fixpoint),
    `s_v` is the number of bound changes at `v`. This is at most
    `sum_i (u_i - l_i)` for the node box, plus 1 when a last change empties
    the node by moving one bound past the other. It is not bounded in terms
    of `n` alone. The recheck gives an exact node with 5 changes in
    dimension 2, where one bound moves twice. Consecutive changes of the same bound cannot be merged into
    one certified piece in general, because the merged set may contain
    points removed earlier and fractional points with a low `phi`.
  - For *binary* variables, a bound can change at most once per variable
    unless the node becomes empty, and the last removal of an emptied node
    replaces its own leaf. So `kappa_tau(P) <= L + nN`, and hence
    `N >= kappa_tau(P)/(n+1)`, even with iterated passes.
- **(d) Not covered.**
  - Any change of `(phi^, K^)` in the continuous or epigraph variables. This
    includes perspective cuts, rank-one or 2x2 cuts, outer-approximation cuts
    on epigraph variables, and switching to a stronger relaxation. The bound
    then holds with the new `phi`, which is the only way to lower `kappa`.
  - Reductions that remove feasible points without a relaxation certificate,
    such as symmetry-based (orbital) fixing and dual or dominance reductions.

*Proof.*

- **(a)** Let `I_l` be as in the proof of Theorem 1.6, with `P = F`. Every
  `p in I_l` lies in `Q̄_u ∩ F` for every ancestor `u` of `l`, hence in every
  cut set `S`. So `conv I_l ⊆ Q̄_l ∩ S_l`, and
  `r(conv I_l) >= r(Q̄_l ∩ S_l) = r(l) >= tau`.
- **(b)** Take `S_v = Q'_v` in (a); by hypothesis `Q'_v ⊇ Q̄_v ∩ F`.
- **(c), simultaneous certificates.** Give `v` the extra leaf children
  `Q̄_v ∩ D_{v,i}` (a multiway node). Its original children, or the leaf
  `Q'_v`, cover the rest. The leaf count is the same as below.
- **(c)** Build a tree `T'` from the run by replacing each node `v` with a
  chain.
  - The chain node `Q^(i-1)` has two children: the leaf
    `Q^(i-1) ∩ D_{v,i}` and the node `Q^(i)`, for `i = 1, ..., s_v`.
  - The last chain node `Q^(s_v) = Q'_v` receives the run's children of `v`.
    If `v` was a leaf of the run, `Q'_v` is a leaf.
  - Every chain node satisfies the covering condition by hypothesis.
  - Every leaf of `T'` has bound at least `tau`: the `D`-pieces by their
    certificates, a leaf `Q'_v` because the run pruned it, and all other
    leaves as in the run.
  - The sets along each root path are nested, so effective sets equal node
    sets. `T'` has `L + sum_v s_v` leaves, and Theorem 1.6 applies to it.
  - **One pass.** Each of the `2n` bounds changes at most once, so
    `s_v <= 2n` and `kappa <= L + 2nN <= (2n+1)N`.
  - **Binaries.** If the final set of `v` has no `P`-points, the last chain
    node gets only its `D`-child. Such a node contributes at most `n + 1`
    pieces and no own leaf. Every other node contributes at most `n` pieces.
    Hence `kappa <= L + nN <= (n+1)N`. ∎

**Operations that satisfy the hypothesis of (c).** The removed piece must have
relaxation bound at least `UB - eps >= OPT - eps = tau`. This holds in the
following cases.

- *OBBT with the incumbent*, applied to the current set `Q` (the sets
  change sequentially). The new bound is
  `l'_i = ceil(min { x_i : x in Q ∩ K, phi(x) <= UB - eps })`. Every
  `x in Q ∩ K` with `x_i <= l'_i - 1` has `phi(x) > UB - eps`, so the piece
  `Q ∩ {x_i <= l'_i - 1}` has bound at least `UB - eps`. The same holds with the threshold `UB`
  in place of `UB - eps`.
- *Reduced-cost fixing.* A dual certificate gives
  `phi(x) >= r_LB + lambda_i (x_i - l_i)` on `Q̄_v ∩ K` with `lambda_i > 0`.
  The removed piece `{x_i >= l_i + k}` with `r_LB + lambda_i k >= UB - eps`
  has bound at least `UB - eps`.
- *Probing.* A tentative fixing whose relaxation bound is at least
  `UB - eps` is removed.

**Proposition 1.9 (the leaf form fails under (c)).** This is the review's
counterexample. Take `phi(x) = (x - 0.4)^2` on `Z`, `K = R`, `eps = 0.01`.

- `OPT = 0.16`, and `phi(0.5) = 0.01 < OPT - eps`. So `0 ~ 1` and
  `kappa = 2`.
- OBBT with `UB = OPT` gives `{phi <= UB} = [0, 0.8]`, whose only integer
  point is `0`. So a single node suffices.

This does not contradict (c): the node form reads `1 >= 2/3`.

- `check_framework_small.py` (Part A) recomputes this example. It also checks
  `kappa <= L + S` on random 2-D instances with one sequential OBBT pass per
  node, where `S` is the number of removed pieces.
- Its further check `kappa <= (2n+1)N` cannot fail in that setting: by
  Theorem 2.2(b), `kappa <= 4 < 5`.
- `check_revision.py` (R4) adds two tests that can fail:
  - binaries with `n = 3`, where `kappa` can reach 8 while `n + 1 = 4`, with
    incumbent probing iterated to a fixpoint at every node, checking
    `kappa <= L + S` and `kappa <= (n+1)N`;
  - general integers with iterated sequential OBBT, where each bound change
    of any size is one piece certified on the current box, checking
    `kappa <= L + S`.

**Remark 1.10 (enumeration that skips out-of-range values).** Sphere decoders
and Lenstra/Kannan-type enumeration create children `{x_i = c}` only for `c`
in an interval `I`. Adding the two pieces `{x_i <= min I - 1}` and
`{x_i >= max I + 1}` turns such a tree into a P-covering tree, since both
pieces have bound above the pruning radius, which is at least `OPT`. This adds
at most two leaves per internal node, so such algorithms process at least
`kappa_tau / 3` nodes.

**Remark 1.11 (weaker relaxations).** If `phi' <= phi` pointwise, then every
`phi'`-admissible class is `phi`-admissible, so `kappa'_tau >= kappa_tau`.
Linear outer approximations of a convex objective are therefore covered, with
the bound of the stronger relaxation `phi`.

## 2. Class number versus split and variable trees

The scout report asked whether the minimum split-tree size is at most
`poly(n, L) * kappa^{O(1)}`, where `L` is the encoding length (its Q3(i)). The
answer is no in general (Theorem 2.3). The reason is structural: for *pure
integer* linear programs the class number is at most the number of
constraints plus one (Proposition 2.1(a)). It can be large only through
curvature, or through a projected sublevel polyhedron with exponentially
many facets. The latter can happen for compact MILPs (Example 2.1a).

### 2.1 Linear problems: the class number is at most the number of facets

**Proposition 2.1.**

- **(a) Pure ILP.** Let `C = {x in Z^n : Ax <= b}` with `A in Z^{m x n}` and
  `b in Z^m`. Let `f = c.x` and use the natural relaxation `K = {Ax <= b}`,
  `phi = c.x` on `K`. Then `kappa_tau(Z^n) <= m + 1` for every
  `tau <= OPT`. If (P) is infeasible, `kappa_{+inf}(Z^n) <= m`.
  Rational data works too: scale each row to integers first.
- **(b) MILP.** Let `C = {(x, y) in Z^n x R^d : Ax + Gy <= b}` with rational
  data and `f = c.x + d.y`, with the natural relaxation. Let `tau < OPT` and
  `Lambda_tau = {x : there is y with Ax + Gy <= b and c.x + d.y <= tau}`.
  Suppose `Lambda_tau = {x : g_i.x <= h_i, i = 1, ..., q}` is any rational
  description. Then `kappa_tau(Z^n) <= max(q, 1)`.

*Proof.*

- **(a)** Take `H_0 = {x : c.x >= OPT}` and `H_j = {x : a_j.x >= b_j + 1}`
  for `j = 1, ..., m`.
  - They cover `Z^n`. If `z in Z^n` has `c.z < OPT`, then `z` is
    infeasible, so `a_j.z > b_j` for some `j`. Integrality then gives
    `a_j.z >= b_j + 1`.
  - They are admissible: `r(H_0) >= OPT >= tau` and `H_j ∩ K = ∅`. Each
    class `H_j ∩ Z^n` has its convex hull inside `H_j`.
  - If (P) is infeasible, drop `H_0`.
- **(b)** `Lambda_tau` contains no integer point. Such a point would be a
  feasible `x` with value at most `tau < OPT`.
  - Scale each `g_i` to be integral and put `h'_i = floor(h_i) + 1`. Every
    `z in Z^n` violates some `g_i.z <= h_i`, hence satisfies
    `g_i.z >= h'_i`.
  - For `x` in `H_i = {g_i.x >= h'_i}` and every `y` with
    `(x, y) in K^`, we have `c.x + d.y > tau`, because `x` is not in
    `Lambda_tau`. So `phi >= tau` on `H_i`.
  - If `Lambda_tau = ∅`, then `r(R^n) >= tau` and one class suffices. ∎

So for linear problems `kappa_tau` is at most the size of a description of
the projected sublevel polyhedron. It is exponential only when that
polyhedron needs exponentially many facets. Two examples:

- **The cross-polytope.** This is also the Dadush–Tiwari `2^n/n` instance,
  as described by DDM. It has `2^n + 2n` constraints, box rows included. The
  `2^n` points of `{0,1}^n` pairwise conflict (DDM, Proposition 3), so
  `2^n <= kappa_{+inf} <= 2^n + 2n`.
- **The DDM packing polytope.**
  `Q = {x in [0,1]^n : sum_{i in S} x_i <= k-1 for all |S| = k, 1.x >= k}`
  has `C(n,k) + 2n + 1` constraints.
  - Take `k`-sets `S != S'` with `|S ∩ S'| <= k-2`. The midpoint of
    `chi(S)` and `chi(S')` has `1.x = k`, and every `k`-set `T` gives
    `sum_T <= (|T ∩ S| + |T ∩ S'|)/2 <= k-1`. So the midpoint lies in `Q`
    and the two points conflict.
  - A constant-weight code of minimum distance 4 is therefore a clique. By
    the Graham–Sloane bound such codes exist with at least `C(n,k)/n`
    words, so `C(n,k)/n <= kappa_{+inf} <= C(n,k) + 2n + 1`.

In both cases `kappa` matches the known split-tree lower bounds up to
polynomial factors. This matches the remark of Gläser and Pfetsch that
hiding-set and Dadush–Tiwari strategies cannot give bounds beyond the number
of constraints. Proposition 2.1 is a formal version of that remark for the
class number.

**Example 2.1a (a compact MILP with `kappa = 2^n`).** Consider

```
min sum_i s_i   s.t.   s_i >= x_i - 1/2,   s_i >= 1/2 - x_i   (2n rows),   x in Z^n,  s in R^n.
```

Its projected relaxation is `phi(x) = ||x - (1/2) 1||_1` on `K = R^n`, with
`OPT = n/2`. For `0 <= eps < 1/2`, `kappa_tau(Z^n) = 2^n`.

- **Lower bound.** Two points of `{0,1}^n` at Hamming distance `d >= 1` have
  midpoint value `(n - d)/2 < OPT - eps`. So all `2^n` points pairwise
  conflict.
- **Upper bound.** The `2^n` halfspaces
  `H_sigma = {x : sum_i sigma_i (x_i - 1/2) >= n/2}`, for
  `sigma in {-1,1}^n`, cover `Z^n`: take `sigma_i = sign(z_i - 1/2)`, and
  note `|z_i - 1/2| >= 1/2`. On `H_sigma`,
  `phi(x) >= sum_i sigma_i (x_i - 1/2) >= OPT`.
- **Consistency with Proposition 2.1(b).** `Lambda_tau` is a cross-polytope
  with `2^n` facets.

This is the `l_1` analogue of Section 3.6(iii). It is also the
extended-formulation phenomenon (Dadush–Tiwari's compact formulation with
continuous variables) that Gläser–Pfetsch mention. So "compact implies small
`kappa`" holds only for pure integer programs. `check_revision.py` (R2)
verifies the conflicts exactly for `n <= 10` and the covering on a window
for `n <= 4`.

`check_framework_small.py`, Part B, checks (a) exactly on 30 random 2-D
instances over the box `[0,2] x [0,3]` whose root LP leaves a gap. There,
`kappa` is 2 or 3 and never exceeds `q + 1`, where `q` is the number of
non-box rows. The class number is taken over the box points.

### 2.2 Unconstrained convex objectives: the class number is a lattice-free facet number

**Theorem 2.2.**

- **(a) Unconstrained case.** Let `K = R^n` and let `phi : R^n -> R` be
  convex. Let `tau <= inf_{Z^n} phi` and `E_tau = {phi < tau}`, which is
  open and convex. If `E_tau = ∅`, then `kappa_tau(Z^n) = 1`. Otherwise
  `kappa_tau(Z^n)` equals each of the following:
  - the minimum number of closed halfspaces that cover `Z^n` and do not meet
    `E_tau`;
  - the minimum number of facets of a polyhedron `M` with `E_tau ⊆ int M`
    and `int M ∩ Z^n = ∅`.

  In particular `kappa_tau(Z^n) <= 2^n`.
- **(b) Constrained case.** Assume (E), `tau < OPT`, `K` closed, and `phi`
  lower semicontinuous. Assume also that
  `C_tau = {x in K : phi(x) <= tau}` is bounded. Then
  `kappa_tau(Z^n) <= 2^n`.
- **(c) Parity.** Under (E) and `tau <= OPT`, every clique of
  `G^mid_tau(Z^n)` has at most `2^n` vertices.

*Proof.*

- **(a), halfspaces give classes.** Closed halfspaces `H_j` that cover `Z^n`
  and miss `E_tau` give classes `Z^n ∩ H_j` with
  `conv(Z^n ∩ H_j) ⊆ H_j`. Since `phi >= tau` on `H_j`, these classes are
  admissible.
- **(a), classes give halfspaces.** Given an admissible partition, each
  `conv I_j` is disjoint from `E_tau`. Otherwise
  `r(conv I_j) < tau`. By the separation theorem for a nonempty open convex
  set and a disjoint convex set, there are `g != 0` and `alpha` with
  `g.x < alpha` on `E_tau` and `g.x >= alpha` on `conv I_j`. So
  `H_j = {g.x >= alpha}` is a closed halfspace that contains `I_j` and
  misses `E_tau`.
- **(a), polyhedra.** Closed halfspaces `{g_j.x >= alpha_j}` cover `Z^n` and
  miss `E_tau` exactly when the open polyhedron
  `O = {g_j.x < alpha_j for all j}` contains `E_tau` and no integer point.
  Take `M = cl O`. Then `int M = O`, because `O ⊇ E_tau` is nonempty and open.
- **(a), the bound `2^n`.** `E_tau` is a nonempty open convex set with no
  integer points. It is therefore contained in a maximal lattice-free convex
  set `M`, meaning `int M ∩ Z^n = ∅`, and `M` is full-dimensional. By
  Lovász's theorem, as proved by Basu, Conforti, Cornuéjols and Zambelli
  (2010, Theorem 1.2), such an `M` is a polyhedron with at most `2^n` facets.
  Since `E_tau` is open, `E_tau ⊆ int M`.
- **(b)** `C_tau` is compact and convex. It has no integer points, since an
  integer point `z in C_tau` would violate (E). If `C_tau = ∅`, then
  `kappa = 1`. Otherwise `eta = dist(C_tau, Z^n) > 0`, and
  `U = C_tau + B°(0, eta/2)` is open, convex and lattice-free.
  - Let `M ⊇ U` be maximal lattice-free. As in (a), `M` has at most `2^n`
    facets and `U ⊆ int M`.
  - The closed complements `H_i` of the facet halfspaces cover `Z^n` and
    miss `int M ⊇ C_tau`.
  - For `x in H_i ∩ K` we have `x ∉ C_tau`, so `phi(x) > tau`.
- **(c)** If `a ≡ b (mod 2)`, then `(a+b)/2` is an integer point. By (E),
  `phi((a+b)/2) >= OPT >= tau`, so `a` and `b` do not conflict. The vertices
  of a clique therefore lie in distinct classes mod 2. ∎

`kappa_tau` in (a) is thus a relative relaxation complexity: the least number
of facets of a lattice-free polyhedron containing the sublevel set `E_tau`.

- In the linear infeasibility case (`phi ≡ 0` on a polytope `K`,
  `tau = +inf`), the same separation argument shows the following. A family
  of classes covering `Z^n` whose hulls miss `K` is, up to separation, the
  family of complementary halfspaces of a polyhedron that contains `K` and
  no integer point.
- So `kappa_{+inf}` is then exactly a relaxation complexity relative to `K`,
  in the sense of Kaibel–Weltge and Averkov–Hojny–Schymura. Theorem 2.2 is
  its analogue for sublevel sets.
- For unconstrained convex objectives, `1 <= omega_mid <= kappa_tau <= 2^n`
  always holds. Theorem 3.5 shows that
random CVP comes within a constant factor of the upper end on the exponent
scale.

### 2.3 Split trees can be exponentially larger than the class number

**Theorem 2.3 (via Gläser–Pfetsch).** Let `A w <= b` be the clique–coloring
system (2) of Gläser and Pfetsch (SODA 2024; arXiv 2308.04320). It has
`r`-vertex graphs, `k = floor((1/8)(r / log r)^{2/3})`, all variables binary,
integral data (rows (2a)–(2d) of their system; the review checked the PDF
display), and box rows (2e) included in `A`. Let `m` be its number of rows,
`n = Θ(r^2)` its number of variables, and `L >= m` its encoding length.
Let `P_r = {w : Aw <= b}`. Then `P_r ∩ Z^n = ∅` and the following hold.

- **(a) Feasibility form.** `kappa_{+inf}(Z^n) <= m <= L`, but every
  split-disjunction proof of integer infeasibility of `P_r` has
  `2^{Omega(n^{1/6 - o(1)})}` nodes (Gläser–Pfetsch, Theorem 5).
  - In terms of `L` this is `2^{L^{Omega(1)}}`, and the exponent depends on
    the encoding convention.
  - Gläser–Pfetsch state `L = Θ(n^2)` and the exponent `1/12`.
  - The review computes that a dense encoding has `L = n^{7/3 - o(1)}`
    (exponent `1/14`) and a sparse one `L = n^{4/3 - o(1)}` (exponent
    `1/8`). Since `n^{1/6} = L^{1/14}` resp. `L^{1/8}`, both are consistent
    with the `n`-form.
- **(b) Optimization form.** The MILP
  `min { t : Aw - b <= t 1, w in Z^n, t in R }` has `OPT >= 1` and
  `kappa_tau(Z^n) <= m` for every `tau <= OPT`. For every `0 <= eps < 1`,
  every `Z^n`-covering split-tree `eps`-certificate that branches on `w` has
  `2^{Omega(n^{1/6 - o(1)})}` nodes.
  - The same holds for the objective `psi(t)` with `psi` convex and strictly
    increasing on `[0, inf)`, for example `psi(t) = t^2`, which gives a
    convex MIQP. The tolerance must then satisfy `0 <= eps < psi(1) - psi(0)`.
  - The projected relaxation of (b) is a finite convex function on
    `K = R^n`: `max_j (a_j.w - b_j)`, or its `psi`-version. These instances
    are therefore unconstrained convex problems in the sense of
    Theorem 2.2(a).
- **(c) Random CNFs.** Refutations of random `Theta(log n')`-CNFs with
  `O(n' 2^k)` clauses satisfy `kappa <= m = poly(n')`. With high probability,
  every split tree has `2^{n'^{Omega(1)}}` nodes (Gläser–Pfetsch, Theorem 7).

Hence no bound of the form `poly(n, L) * kappa_tau^{O(1)}` holds for the
minimum split-tree size.

*Proof.*

- **(a)** The bound on `kappa` is Proposition 2.1(a) in its infeasible
  form. The tree-size bound is Gläser–Pfetsch Theorem 5. A
  "branch-and-bound tree for (2)" in their sense is a binary tree of integer
  split disjunctions whose leaves have LP-infeasible atoms. This is exactly a
  `Z^n`-covering split `(+inf)`-certificate.
- **(b), class number.** For `w in Z^n`, `phi(w) = max_j (a_j.w - b_j)` is an
  integer, and it is at least 1 because `w` is not in `P_r`. Hence
  `OPT = t* = min_{w in Z^n} phi(w) >= 1`. The minimum is attained because
  the box rows make `phi` large outside a bounded set. The halfspaces
  `H_j = {a_j.w - b_j >= t*}` cover `Z^n`, and `phi >= t* = OPT >= tau` on
  each of them. So `kappa <= m`.
- **(b), tree size.** If `T` is a split-tree `eps`-certificate with
  `eps < 1`, every leaf has `r(l) >= OPT - eps > 0`. A point `w` in
  `Q̄_l ∩ P_r` would have `phi(w) <= 0`. So every leaf atom misses `P_r`,
  `T` is a proof of integer infeasibility of `P_r`, and (a) applies.
- **(b), other objectives.** Write `M(w) = max_j (a_j.w - b_j)`. With the
  objective `psi(t)`, the projected relaxation is
  `phi(w) = inf { psi(t) : t >= M(w) }`.
  - `phi` is finite, since the infimum of a convex function that is
    increasing on `[0, inf)` over a closed half-line is finite.
  - `phi(w) = psi(M(w))` when `M(w) >= 0`, and `phi(w) <= psi(0)` when
    `M(w) <= 0`.
  - Integer points have `M >= t* >= 1`, so `OPT = psi(t*)`.
  - The same classes satisfy `phi >= psi(t*) = OPT` on each `H_j`.
  - A leaf with `r(l) >= OPT - eps > psi(0)` cannot meet `P_r`, because
    `phi <= psi(0)` on `P_r`.
  - Here `OPT - eps > psi(0)` because `t* >= 1` and
    `eps < psi(1) - psi(0)`.
- **(c)** Apply the same argument to Gläser–Pfetsch Theorem 7, with
  Proposition 2.1(a) for the class number. ∎

*Remarks.*

- The instances in (b) have feasible points, and every integer point has
  `t >= t* >= 1`. The difficulty is that the leaves must exclude the
  fractional region `P_r`, where the relaxation value can be at most 0,
  while the split disjunctions cover all of `Z^n`. It does not come from
  conflicts among near-optimal feasible points.
- The instances in (b) are unconstrained convex problems. So split-tree
  size is not polynomially bounded by `kappa` even for finite convex `phi`
  on `K = R^n`. Only the convex *quadratic* case (Open problem 2.6) remains
  open.
- `kappa_tau(F)` with `P = F` is also at most `m`.
- The lower bound comes from interpolation, which uses the product structure
  of the constraint system and is invisible to `kappa`.
- The scout asked whether a convex quadratic objective can make known hard
  instances easy for `kappa` but keep them hard for split trees.
  - For compact instances no objective is needed: they are already easy for
    `kappa`. The quadratic form `psi(t) = t^2` in (b) keeps both properties.
  - For the cross-polytope and the Dadush–Tiwari and DDM instances, `kappa`
    is already within a polynomial factor of the known split-tree lower
    bounds (Section 2.1). So they cannot give a separation, with or without
    an objective.
- Theorem 2.3 depends on the cited theorem, which we did not re-prove.
  - The local text rendering omits the display of system (2). The review
    read it in the PDF: the rows have integral coefficients and include the
    box rows.
  - The theorem's statement was checked in the local full text
  (`glaser2024-sub-exponential-lower-bounds-for`, Theorems 5 and 7,
  Corollary 6, and the definition of branch-and-bound trees in Section 2).

### 2.4 Variable branching: an exponential gap with `kappa = 2`

**Proposition 2.4 (quadratic Jeroslow instance).** Let `n` be odd and
`h = (n+1)/2`. Consider `min (1.x - n/2)^2` over `x in {0,1}^n`, with the
natural relaxation on `K = [0,1]^n`. Then `OPT = 1/4`. For `0 <= eps < 1/4`
and `tau = OPT - eps`:

- **(a)** `kappa_tau(Z^n) = kappa_tau({0,1}^n) = 2`.
- **(b)** The single split `1.x <= h-1 ∨ 1.x >= h` gives a 3-node
  certificate.
- **(c)** Every variable-branching `eps`-certificate on the binaries, with
  any rule and any order, has at least `C(n+1, h)` leaves. It has exactly
  `C(n+1, h)` leaves when it contains no branching on an already-fixed
  variable and no branching at a node whose bound is already at least
  `tau`. Note `C(n+1, h) ~ 2^{n+1} / sqrt(pi (n+1)/2)`.

*Proof.*

- **(a)** The classes `Z^n ∩ {1.x <= h-1}` and `Z^n ∩ {1.x >= h}` cover
  `Z^n`, because `1.z` is an integer and `n/2` is not. On `K` intersected
  with either halfspace, `phi >= 1/4 >= tau`. Also `kappa >= 2`, since
  `r(R^n) = 0 < tau`.
- **(b)** The same two halfspaces are the children of the split; each has
  bound `1/4 >= tau`.
- **(c), reduction.** Two kinds of branching only add leaves, so we
  contract them:
  - branching on an already-fixed variable, which creates an empty child
    and a copy of the node;
  - branching below a node whose bound is already at least `tau`, which can
    be made a leaf.

  After these contractions the tree is still a certificate and has no more
  leaves. So assume neither occurs.
- **(c), leaves.** A node fixes `a` variables to 1 and `b` variables to 0.
  - Its bound is 0 when `a <= h-1` and `b <= h-1`. The relaxation optimum
    then has the non-integer sum `n/2`, so neither integrality nor
    infeasibility can prune the node, and `0 < tau`.
  - Otherwise its bound is at least `1/4 >= tau`.
  - So a node is a leaf exactly when `max(a, b) >= h`.
- **(c), counting.** Branching on any free variable produces `(a+1, b)` and
  `(a, b+1)`. The number of leaves `T(a, b)` below a node therefore depends
  only on `(a, b)` and satisfies `T = 1` if `max(a, b) >= h`, and
  `T(a, b) = T(a+1, b) + T(a, b+1)` otherwise.
  - The solution is `T(a, b) = C(u+v, u)` with `u = h-a` and `v = h-b`.
    This follows from Pascal's rule, with boundary values
    `C(v, 0) = C(u, u) = 1`.
  - So `T(0, 0) = C(2h, h) = C(n+1, h)`. ∎

- This is Jeroslow's (1974) parity instance, stated with a convex quadratic
  objective, so the gap is relaxation-intrinsic for the natural MIQP
  relaxation. The leaf count uses only the pattern of node bounds, so it
  holds equally for the linear infeasible version. The quadratic objective
  adds the optimization form with `kappa = 2`.
- `check_framework_small.py`, Part C, computes the exact minimum over all
  variable-branching trees by dynamic programming over partial assignments
  for `n = 3, 5, 7`. It confirms `C(n+1, h)` = 6, 20, 70.
- Cuts in `x` cannot help here, because `K = conv{0,1}^n`. A single
  disjunctive cut on the epigraph variable, from the split in (b), makes the
  root bound `1/4`.

### 2.5 Fixed dimension

**Proposition 2.5.** Assume (E), `K` closed, `phi` lower semicontinuous,
`eps > 0` and `tau = OPT - eps`. Assume `C_tau = {x in K : phi(x) <= tau}`
is bounded. Then there is a `Z^n`-covering split-tree `eps`-certificate with
at most `S(n) = 2 prod_{j=1}^{n} (floor(Flt(j)) + 5)` nodes. Here `Flt(j)` is
the flatness constant: every compact convex set in `R^j` without points of a
full-rank affine lattice `Lambda` has `Lambda`-width at most `Flt(j)`.

Known values of `Flt(j)`:

- `O(j^{3/2})` (Banaszczyk, Litvak, Pajor and Szarek, 1999);
- `O(j log^3 j)` (Reis and Rothvoss, 2023); the current arXiv version
  (2303.14605 v5, per the review) states `O(j log^2(2j))`;
- `O(j)` for ellipsoids.

So `S(n) = n^{O(n)}`, independently of the data. In particular the ratio
"minimum split tree / `kappa_tau`" is at most `S(n)`.

*Proof.* A node whose effective set `Q` misses `C_tau` is a valid leaf: if
`x in Q ∩ K` had `phi(x) < tau`, then `x` would lie in `C_tau`. `C_tau` is
compact and integer-free by (E). We describe a recursive procedure on
rational affine subspaces `A` with `Lambda_A = A ∩ Z^n` nonempty and of full
rank in `A`, `dim A = j`. The procedure keeps a node whose effective set lies
in `A` (initially `A = R^n`).

- **Base cases.** If `C_tau ∩ A = ∅`, the node is a leaf. If `j = 0`, then
  `A = {a}` with `a` an integer point, and `a` is not in `C_tau`, so
  `C_tau ∩ A = ∅`.
- **Branching direction.** Otherwise take a primitive dual vector `y` of
  `Lambda_A - a_0` that attains a width at most `Flt(j)` for the compact set
  `C_tau ∩ A`.
  - Since `Lambda_0 = Z^n ∩ (A - a_0)` is a saturated sublattice, `y`
    extends to some `pi in Z^n`.
  - Then `pi.x` is an integer on `Lambda_A`. Its values on `C_tau ∩ A` lie
    in an interval containing
    `q <= floor(Flt(j)) + 1` integers `c_min, ..., c_max`.
- **Splits.** Branch on `pi.x <= c_min - 1 ∨ pi.x >= c_min`. The left child
  misses `C_tau`. Then, for `c = c_min, ..., c_max` in turn, branch the
  current right child on `pi.x <= c ∨ pi.x >= c+1`.
  - The left child is the slice `A ∩ {pi.x = c}`, which is nonempty in the
    lattice because `y` is primitive. Recurse on it with `j - 1`.
  - The final right child misses `C_tau`.
- **Counting.** Each split covers `Z^n`. These `q + 1` splits create
  `2(q+1)` nodes, `q` of which are slice roots. So
  `S(j) <= 3 + q(1 + S(j-1))`, hence `1 + S(j) <= (q+4)(1 + S(j-1))`, and
  `S(0) = 1`. ∎

### 2.6 What `kappa` measures, and the open case

The results above separate two costs.

- **The semantic cost.** This is `kappa_tau`. It is forced by the relaxation
  and is attained by arbitrary convex pieces (Theorem 1.7).
- **The syntactic cost.** This is the extra cost of certifying the
  disjunctions.
  - For variable branching it can be exponential even when `kappa = 2`
    (Proposition 2.4).
  - For split branching it can be exponential when `kappa <= L`
    (Theorem 2.3). This includes unconstrained convex objectives
    (Theorem 2.3(b)), but only in growing dimension (Proposition 2.5).

Consequences for the scout's Q3(ii) ("B&C beats B&B exactly when cuts shrink
the class number"):

- Cuts in the integer variables never lower `kappa_tau(F)`
  (Theorem 1.8(a)).
- Such cuts can still shrink split or variable trees exponentially. Take the
  linear Jeroslow instance `{x in [0,1]^n : 2 1.x = n}` with `n` odd.
  Variable branching needs `2^{Omega(n)}` nodes. The two Chvátal–Gomory cuts
  `1.x <= (n-1)/2` and `1.x >= (n+1)/2` close it at the root. Meanwhile
  `kappa = 2`, with classes `{2 1.x <= n-1}` and `{2 1.x >= n+1}`.
- So "exactly when" is false. The correct statement is weaker: *relative to
  the best semantic tree*, cutting helps only by changing the relaxation in
  the continuous or epigraph variables so that `kappa` decreases.

**Open problem 2.6 (convex quadratic objectives).** Let
`phi(x) = ||Bx - t||^2` with `K = R^n`; this is unconstrained convex integer
least squares. Is the minimum split-tree `eps`-certificate always of size
`poly(n) * kappa_tau^{O(1)}`? For general unconstrained convex `phi` the
answer is no (Theorem 2.3(b), whose `phi` is piecewise linear). The question
is whether ellipsoidal sublevel sets behave better.

- Known bounds: `1 <= kappa_tau <= 2^n` (Theorem 2.2) and split trees are
  at most `n^{O(n)}` (Proposition 2.5).
- A negative answer needs a split-tree lower-bound technique that works for
  a single convex quadratic.
  - The Dadush–Tiwari / DDM Helly argument needs many linear constraints.
  - Interpolation needs a product structure.
  - Midpoint, hiding-set and class arguments are bounded by `kappa`.
  - Theorem 2.3(b) transfers interpolation to a piecewise-linear `phi` with
    many pieces. A single quadratic has no such structure.
- The current Reis–Rothvoss flatness bound, and their subspace-flatness
  algorithm with running time `(log n)^{O(n)}`, might sharpen the
  `n^{O(n)}` upper bound. We did not check whether that algorithm yields
  split trees of that size.
- A positive answer would give split-tree certificates of size `2^{O(n)}`
  for every CVP instance, since `kappa <= 2^n`. We know of no such
  certificates. Voronoi-cell CVP algorithms certify optimality with
  `2^{O(n)}` relevant vectors, but not with a branching tree.

## 3. Random closest vector problems

### 3.1 Model and tools

**Model.**

- `X_n = SL_n(R)/SL_n(Z)` is the space of unimodular lattices (`n >= 2`),
  with its Haar probability measure `mu`.
- `L ~ mu` is the random lattice. Given `L`, the target `t` is uniform on
  the torus `R^n / L`.
- `B` is any basis of `L`, and `phi(x) = ||Bx - t||^2` on `K = R^n`, so
  `OPT = dist(t, L)^2`.
- A unimodular change of basis maps convex pieces to convex pieces and
  `Z^n` to `Z^n`, and conflicts depend only on the lattice vectors `Bz`. All
  statements are therefore basis-free. In particular they apply to every
  lattice reduction (LLL, BKZ) and to every enumeration order.
- `GH` is the radius of the ball of volume 1, so `GH^2 ~ n/(2 pi e)`. In
  *GH units* lengths are divided by `GH`, and then `vol B(0, r) = r^n`.
- For a bounded measurable `A ⊆ R^n`, `N_A = #{v in L : v - t in A}`. We
  write `u = v - t` for lattice points seen from the target.
- Conflict at `tau = OPT - eps`: for lattice points `u != w`, midpoint
  conflict means `||u + w||^2 < 4(OPT - eps)`, because
  `phi((a+b)/2) = ||(u+w)/2||^2`.

**Lemma 3.1 (unfolding).** Fix `L` with covolume 1, and measurable
`g, h >= 0`. Then

- (i) `E_t sum_{v in L} g(v - t) = ∫ g`;
- (ii) `E_t [sum_v g(v - t)] [sum_w h(w - t)] = sum_{a in L} ∫ g(x) h(x + a) dx`.

*Proof.*

- (i) Let `D` be a fundamental domain. The translates `v - D`, `v in L`,
  tile `R^n` up to null sets, so
  `∫_D sum_v g(v - t) dt = sum_v ∫_{v - D} g = ∫ g`.
- (ii) Write `w = v + a`. Then apply (i) to `x -> g(x) h(x + a)` for each
  `a`, using Tonelli's theorem. ∎

**Siegel's mean value theorem** (Siegel 1945): for `n >= 2` and bounded
measurable `f >= 0` with compact support,

```
E_mu sum_{v in L \ {0}} f(v) = ∫ f.
```

**Lemma 3.2 (moments).** Let `A` be bounded and measurable and `V = vol A`.

- (a) `E_t N_A = V` for every `L`.
- (b) `E_{L,t} N_A^2 = V + V^2`, so `Var(N_A) = V` under the joint law.
- (c) For `s > 0`, the ordered pair count
  `M_A(s) = #{(v, w) : v != w, v - t in A, w - t in A, ||v - w|| < s}`
  has `E_{L,t} M_A(s) = ∫_{||a|| < s} vol(A ∩ (A - a)) da`.

*Proof.*

- (a) This is Lemma 3.1(i) with `g = 1_A`.
- (b) Lemma 3.1(ii) with `g = h = 1_A` gives
  `E_t N_A^2 = sum_{a in L} vol(A ∩ (A - a))`. The term `a = 0` equals
  `V`. Siegel's theorem applied to `f(a) = vol(A ∩ (A - a))` gives expected
  sum `∫ f = V^2` over `a != 0`.
- (c) Use the same computation with the extra factor `1[||a|| < s]`, and
  drop `a = 0`. ∎

**Lemma 3.3 (typical scales).** For `delta in (0, 1)`:

- (a) `P(OPT < (1-delta)^2 GH^2) <= (1-delta)^n`;
- (b) `P(lambda_1(L) < (1-delta) GH) <= (1-delta)^n / 2`;
- (c) `P(OPT > (1+delta)^2 GH^2) <= (1+delta)^{-n}`;
- (d) `P(N_{B°(0,r)} >= T) <= vol(B°(0,r)) / T`.

*Proof.*

- (a) `OPT < r^2` iff `N_{B°(0,r)} >= 1`. Apply Markov's inequality with
  Lemma 3.2(a).
- (b) Nonzero vectors of length below `r` come in pairs `±v`. Siegel's
  theorem gives expected count `vol B_r`, and Markov's inequality applies to
  half the count.
- (c) `P(N = 0) <= Var(N) / (E N)^2 = 1/V`, by Chebyshev's inequality and
  Lemma 3.2(b).
- (d) This is Markov's inequality. ∎

### 3.2 Lower bound for the conflict clique

**Theorem 3.4.** Fix `delta in (0, 0.08)`, `rho in (1, 4/3)` with
`rho ((1-delta)^2 - delta) > 1`, and `0 <= eps <= delta GH^2`. In GH units
put `r_0^2 = (1-delta)^2 - delta`, `R^2 = rho r_0^2` and `V = R^n`, so that
`V > 1` grows exponentially. The bound is vacuous for
`delta >= (3 - sqrt 8)/2 = 0.0858`, where `(4/3) r_0^2 <= 1`. With
probability at least

```
1 - (1-delta)^n - 4/V - 2n (4(rho-1)/rho)^{n/2},
```

the lattice points `u` with `||u|| < R` contain a clique of `G^mid_tau(Z^n)`
of size at least `V/4`. Hence every `Z^n`-covering convex-piece
`eps`-certificate has at least `V/4` leaves. As `delta -> 0` and
`rho -> 4/3`, `V^{1/n} -> (4/3)^{1/2}`, so the bound is
`2^{(0.2075 - o(1)) n}`.

*Proof.*

- **Conflict criterion.** Work on the event `OPT >= (1-delta)^2`, in GH
  units. Then `OPT - eps >= r_0^2`, so `||u + w|| < 2 r_0` implies a
  conflict.
- **Non-conflicting pairs are close.** For `u, w` in the open ball of
  radius `R`,
  `||u + w||^2 = 2||u||^2 + 2||w||^2 - ||u - w||^2 < 4R^2 - ||u - w||^2`.
  So a non-conflicting pair has `||u - w||^2 < 4(R^2 - r_0^2) =: s_1^2`.
- **Counting.** Let `N = N_{B°(0,R)}`, and let `M` be the number of
  unordered non-conflicting pairs in that ball. Deleting one point of each
  such pair leaves a clique of size at least `N - M`.
- **Expected pair count.** By Lemma 3.2(c),
  `E M <= J / 2` with `J = ∫_{||a|| < s_1} vol(B_R ∩ (B_R - a)) da`.
- **Bounding `J`.** Write `J = ∫_{B_R} vol(B_R ∩ B(x, s_1)) dx`. For `z`
  in `B_R ∩ B(x, s_1)` and `theta in [0,1]`, averaging the two inequalities
  gives
  `||z - theta x||^2 + theta(1-theta)||x||^2 < (1-theta)R^2 + theta s_1^2`.
  Hence `vol(B_R ∩ B(x, s_1)) <= (A - b||x||^2)^{n/2}` in GH units, where
  `A = (1-theta)R^2 + theta s_1^2` and `b = theta(1-theta)`.
  - Choose `1 - theta = s_1^2 / (2R^2) = 2(rho-1)/rho`, so
    `theta = (2-rho)/rho`.
  - Then `A - bR^2 = s_1^2 - s_1^4/(4R^2) = 4(rho-1) r_0^2 / rho =: a^2`.
  - The function `r -> r^{n-1} (A - b r^2)^{n/2}` is nondecreasing on
    `[0, R]` when `bR^2 <= (1 - 1/n) a^2`. That condition is equivalent to
    `rho >= 2/n`, which holds.
  - Therefore
    `J <= n ∫_0^R r^{n-1} (A - b r^2)^{n/2} dr <= n R^n a^n = n V a^n`, and
    `2J/V <= 2n (4(rho-1)/rho)^{n/2}`, using `r_0 <= 1`.
- **Probabilities.**
  - By Chebyshev's inequality and Lemma 3.2(b),
    `P(N < V/2) <= Var(N)/(V/2)^2 = 4/V`.
  - By Markov's inequality, `P(M >= V/4) <= 4 E M / V <= 2J/V`.
  - With Lemma 3.3(a), outside these three events
    `N - M > V/2 - V/4 = V/4`.
- **Rate.** `V^{1/n} = (rho r_0^2)^{1/2}`. ∎

*Checks.*

- `check_cvp_integrals.py` evaluates the exact
  `J/V = n (2R)^n ∫_0^{sqrt((rho-1)/rho)} y^{n-1} I_{1-y^2}((n+1)/2, 1/2) dy`
  to 30 digits for `n` up to 320.
  - The ratio of the exact value to the bound is at most `0.059`.
  - The exponent of the exact value changes sign at `rho = 4/3`.
- The lens-fraction formula matches Monte Carlo to 3 digits.
- On 30 Goldstein–Mayer lattices per `n` (Section 3.7), the exact clique
  number of the conflict graph restricted to `B°(0, (4/3)^{1/2} OPT^{1/2})`
  was never below `N - M`.

### 3.3 Lower bound for the class number

**Theorem 3.5.** Fix `delta in (0, 0.1)` and `0 <= eps <= delta GH^2`. In GH
units put `R^2 = (3/2)(1-delta)^2 - delta` and `V_c = R^n`. Here `V_c > 1`
for `delta < (4 - sqrt 13)/3 = 0.1315`. With probability
at least `1 - (3/2)(1-delta)^n - 4/V_c`,

```
kappa_tau(Z^n) >= V_c / (2(n+1)) = 2^{(0.2925 - O(delta)) n} / (2(n+1)).
```

So every `Z^n`-covering convex-piece `eps`-certificate has at least that many
leaves.

*Proof.* Work on the events `OPT >= (1-delta)^2`,
`lambda_1 >= 1 - delta` and `N >= V_c/2`, where `N = N_{B°(0,R)}` (GH
units). By Lemma 3.3(a), 3.3(b) and Chebyshev, all three hold with the stated
probability. Let `r_in^2 = OPT - eps >= (1-delta)^2 - delta`.

- **Classes lie in caps.** Let `I` be admissible. Then `conv(BI - t)` does
  not meet `B°(0, r_in)`. By separation there is a unit vector `e` with
  `<e, x> >= r_in` on `conv(BI - t)`. Every point `u` of `I` with
  `||u|| < R` therefore lies in the cap
  `{||u|| < R, <e, u> >= r_in}`.
- **Caps lie in small balls.** A point `u` in the cap satisfies
  `||u - r_in e||^2 = ||u||^2 - 2 r_in <e, u> + r_in^2 < R^2 - r_in^2 =: a^2`.
- **The small balls hold few lattice points.**
  `a^2 <= R^2 - (1-delta)^2 + delta = (1-delta)^2 / 2 <= lambda_1^2 / 2`.
  So distinct lattice points `p, q` in the open ball `B°(c, a)`, with
  `c = r_in e`, satisfy
  `<p - c, q - c> = (||p-c||^2 + ||q-c||^2 - ||p-q||^2)/2 < (2a^2 - lambda_1^2)/2 <= 0`.
  - `c` itself is not among them unless it is the only one, because
    `a < lambda_1`.
  - A set of nonzero vectors in `R^n` with pairwise negative inner products
    has at most `n + 1` elements (proof below).
- **Counting.** Each admissible class contains at most `n + 1` of the `N`
  lattice points of `B°(0, R)`. By Lemma 1.5(b),
  `kappa >= N/(n+1) >= V_c/(2(n+1))`.

*Pairwise obtuse vectors.* Suppose `v_1, ..., v_m` are nonzero with pairwise
negative inner products, and `m >= n + 2`.

- Then `v_1, ..., v_{m-1}` are linearly dependent. Write the dependence as
  `sum_{i in S} alpha_i v_i = sum_{i in T} beta_i v_i` with
  `alpha, beta > 0`, `S ∩ T = ∅` and `S` nonempty.
- Let `w` be the common value. Then
  `||w||^2 = sum_{i in S, j in T} alpha_i beta_j <v_i, v_j> <= 0`, so
  `w = 0`.
- Then `0 = <w, v_m> = sum_{i in S} alpha_i <v_i, v_m> < 0`, a
  contradiction. ∎

*Remark 3.5a (a small improvement).* The cap contents can also be bounded
with the Kabatiansky–Levenshtein bound. Lift the cap ball to a hemisphere of
`S^n` and choose `R^2` slightly above `3/2`. This raises the exponent from
`0.2925` to about `0.2975`, which we do not pursue
(`check_cvp_exponents.py`).

### 3.4 Upper bounds and the separation between clique and class number

**Proposition 3.6.**

- **(a) Deterministic.** For every lattice, every target and every
  `eps >= 0`: `omega(G^mid_tau) <= 2^n` and `kappa_tau(Z^n) <= 2^n`
  (Theorem 2.2).
- **(b) Class number.** Fix `delta in (0, 0.1)`. With probability at least
  `1 - (1+delta)^{-n} - e^{-delta n}`,

  ```
  kappa_tau(Z^n) <= e^{delta n} (sqrt 2 (1+delta))^n + O(n^2 log n) 2^{n/2} = 2^{(1/2 + O(delta)) n}.
  ```

- **(c) Clique.** Let `e_+ = 0.26124...` be defined as follows. Let
  `rho* = 1.43642...` be the root of
  `(1/2) log2 rho = R_KL(arccos((2 - rho)/rho))`, and put
  `e_+ = (1/2) log2 rho*`. Here `R_KL` is the Kabatiansky–Levenshtein
  exponent. Then w.h.p. `omega(G^mid_tau) <= 2^{(e_+ + o(1)) n}`.

Together with Theorem 3.5, for fixed small `delta` and w.h.p.,

```
kappa_tau / omega >= 2^{(0.2925 - 0.2612 - O(delta)) n} = 2^{(0.031 - O(delta)) n}.
```

So the hypergraph (class) bound is exponentially stronger than the conflict
clique on random CVP. The scout's heuristic target `(3/2)^{n/2}` is
unattainable for cliques, but it holds for the class number.

*Proof of (b).* Let `r_in = (OPT - eps)^{1/2}`. For a unit vector `e`, the
closed halfspace `H_e = {x : <x - t, e> >= r_in}` misses `B°(t, r_in)`, so
it is admissible (Theorem 2.2(a)). We cover all lattice points with such
halfspaces.

- **Near points.** Points `u` with `||u|| < sqrt 2 r_in` are covered one by
  one, using `H_{u/||u||}`. This works because
  `<u, u/||u||> = ||u|| >= OPT^{1/2} >= r_in`.
  - Their number is at most `N_{B°(0, sqrt(2 OPT))}`.
  - With probability at least `1 - (1+delta)^{-n} - e^{-delta n}`, we have
    `OPT <= (1+delta)^2` (Lemma 3.3(c)). Markov's inequality then bounds
    this count by `e^{delta n} (sqrt 2 (1+delta))^n`.
- **Far points.** Points with `||u|| >= sqrt 2 r_in` are covered by `H_e`
  for any `e` at angle at most `pi/4` from `u`, since then
  `<u, e> >= ||u||/sqrt 2 >= r_in`. It remains to cover `S^{n-1}` by caps of
  angular radius `pi/4`.
- **Covering lemma.** `S^{n-1}` can be covered by
  `M <= ceil(pi n^2 log(1 + 2n) / sin^{n-2}(pi/4 - (pi/2 + 1)/n)) + 1 = O(n^2 log n 2^{n/2})`
  caps of angular radius `pi/4`.
  - Let `Y` be a maximal `(1/n)`-separated set in chordal distance, so
    `|Y| <= (1 + 2n)^n`. Every point lies within angle `pi/(2n)` of `Y`.
  - Pick `M` independent uniform centers. A fixed `y` is missed by all caps
    of angular radius `phi_1 = pi/4 - pi/(2n)` with probability at most
    `exp(-M sigma(phi_1))`.
  - The normalized cap measure satisfies
    `sigma(phi_1) >= (1/(pi n)) sin^{n-2}(phi_1 - 1/n)`.
  - By the union bound over `Y`, some choice covers all of `Y` within
    `phi_1`, and hence covers the sphere within `pi/4`. ∎

*Proof of (c).* Normalize `OPT = 1`. Split a clique `S` into three parts.

- **`S_1 = {u : ||u||^2 < rho*}`.** `|S_1| <= N_{B°(0, sqrt(rho*))}`,
  which is at most `2^{((1/2) log2 rho* + O(delta) + gamma) n}` with
  probability at least `1 - (1+delta)^{-n} - 2^{-gamma n}`, by Lemma 3.3(c)
  and (d).
- **`S_2 = {u : rho* <= ||u||^2 < 2.2}`.** For `u, w` in `S_2` with
  `a = ||u||^2` and `b = ||w||^2`, the conflict gives
  `2<u,w> < 4 - a - b`. Hence
  `<û, ŵ> < (4 - a - b)/(2 sqrt(ab)) <= 2/sqrt(ab) - 1 <= (2 - rho*)/rho*`,
  using `a + b >= 2 sqrt(ab)`. So `S_2` is a spherical code with angle
  greater than `theta* = arccos((2 - rho*)/rho*)`, and by
  Kabatiansky–Levenshtein
  `|S_2| <= A(n, theta*) <= 2^{(R_KL(theta*) + o(1)) n}`.
- **`S_3 = {u : ||u||^2 >= 2.2}`.** Here
  `<û, ŵ> < 2/sqrt(ab) - 1 <= -1/11`. At most `1 + 11 = 12` unit vectors
  can have pairwise inner products at most `-1/11`, because
  `0 <= ||sum û||^2 <= k - k(k-1)/11`.
- **Choice of `rho*`.** It balances the two exponents, which gives `e_+`.
  `check_cvp_exponents.py` computes `rho* = 1.436424`,
  `e_+ = 0.261241`, and `R_KL(60 deg) = 0.4014` as a sanity check. ∎

### 3.5 Consequences for algorithms

With the probabilities of Theorems 3.4–3.5, and for any basis of the random
lattice, the following hold.

1. Every `Z^n`-covering convex-piece `eps`-certificate for the continuous
   relaxation has at least `2^{(0.2925 - O(delta)) n}/(2(n+1))` leaves. This
   includes:
   - variable branching in any reduced basis;
   - general splits;
   - multiway hyperplane branching;
   - "semantic" trees.
2. Enumeration methods that create only in-range children process at least
   a third of that number of nodes (Remark 1.10). These include
   Fincke–Pohst and Schnorr–Euchner sphere decoders with any reduction and
   any ordering, and Lenstra/Kannan-type enumeration.
3. With one pass of incumbent-based bound tightening at every node, at least
   `1/(2n+1)` of that number of nodes are needed (Theorem 1.8(c)). With
   iterated passes, the count is leaves plus bound changes.
4. Branch-and-cut with arbitrary cuts in `x` needs as many leaves: this
   includes Chvátal–Gomory, split, lift-and-project cuts, and the node's
   integer hull (Theorem 1.8(a)). Only cuts or relaxations involving the
   objective (epigraph) variable can help.
5. Pointwise weaker relaxations are also covered (Remark 1.11). An example
   is outer approximation of the objective.

The constant `eps` may be as large as `delta GH^2 ~ delta n/(2 pi e)`, an
absolute tolerance that grows linearly with `n`.

### 3.6 Remarks on limits of the method, the orthogonal lattice, and Gaussian bases

**(i) The pair method stops at `4/3`.** This is a heuristic.

- Among `rho^{n/2}` Poisson-like points at squared radius `rho`, a pair
  conflicts iff the angle is above `arccos((2 - rho)/rho)`.
- Each point has about `rho^{n/2} (4(rho-1)/rho^2)^{n/2}` non-conflicting
  partners.
- Greedy or Turán selection yields about
  `min(rho, rho^2/(4(rho-1)))^{n/2}`, which is maximized at `rho = 4/3`.
- Proposition 3.6(c) confirms that no *midpoint-clique* argument can
  exceed `2^{(0.2612 + o(1)) n}`. It does not bound the chromatic number
  `chi(G^mid)`, which is also a pairwise quantity and at most `kappa`. It
  does not bound the segment graph either, whose conflict condition is
  weaker for points of unequal norms.

**(ii) The class number probably reaches `2^{n/2}`.** This is a heuristic,
not proved.

- The class bound of Theorem 3.5 is limited by the use of `lambda_1` to
  control cap contents.
- If every cap of the form `B(t + r_in e, a)` with `a^2 = R^2 - r_in^2 <= OPT`
  contained only `2^{o(n)}` lattice points, uniformly in `e`, then
  Lemma 1.5(b) with `R^2 = 2 OPT` would give `kappa >= 2^{(1/2 - o(1)) n}`.
  This would match Proposition 3.6(b).
- A Poisson heuristic, and Rogers-type higher moments, suggest that the
  maximal number of lattice points in a ball of volume `O(1)` is `2^{o(n)}`
  for Haar lattices.
- **Conjecture 3.7.** For Haar-random `L` and uniform `t`, w.h.p.
  `kappa_tau(Z^n) = 2^{(1/2 + o(1)) n}` for every fixed small `eps/GH^2`.

**(iii) The orthogonal lattice.** Let `L = Z^n` with target
`t = (1/2) 1`, so `phi(x) = ||x - (1/2) 1||^2`. The problem is trivial
(round), yet every `eps`-certificate with the continuous relaxation and
`eps < 1/4` has at least `2^n` leaves.

- `OPT = n/4` is attained by all `2^n` points of `{0,1}^n`.
- Two such points at Hamming distance `d` have midpoint value
  `(n - d)/4 < OPT - eps`.
- Replacing each `(x_i - t_i)^2` by its convex hull over the integers (the
  piecewise-linear interpolation, a univariate mixed-integer epigraph hull)
  makes the root bound exact.
- This is the simplest instance of the message of Section 4: here the
  difficulty belongs to the relaxation, not to the lattice.
- *Remark (random `t`, sketch, not a full proof).* For uniform `t`, cliques
  of size `e^{c n}` with a small `c > 0` should exist.
  - Let `T` be the set of coordinates with `|frac(t_i) - 1/2| < eta`, so
    `|T| ~ 2 eta n`.
  - For `S ⊆ T`, let `x^S` be the rounding of `t` with the coordinates in
    `S` moved to the farther neighbour.
  - Moving one coordinate costs at most `2 eta`. A midpoint over the
    difference set `D` saves at least `1/4 - eta` per coordinate of `D`.
  - So `x^S` and `x^{S'}` conflict when
    `|D| (1/4 - eta) > 2 eta |S ∩ S'| + eps`.
  - A constant-weight code in `T` with weight `|T|/2` and relative distance
    above `4 eta/(1 - 4 eta)` (plus `O(eps/|T|)`) therefore gives a clique.
    Such codes have positive rate for small `eta` (Gilbert–Varshamov).
  - We did not optimize `c`.

**(iv) Gaussian-basis lattices (the MIMO and integer least-squares model).**
Take `B` with i.i.d. `N(0,1)` entries, scaled to determinant 1, and a uniform
target.

- **What transfers.** Lemma 3.3(a) holds for every fixed lattice (first
  moment over `t` only). So `OPT >= (1-delta)^2 GH^2` holds with probability
  at least `1 - (1-delta)^n` for any basis distribution.
- **What does not.** Everything that uses Siegel's theorem fails: the
  variance of `N` and the pair count `J`. Section 3.3 also used
  `lambda_1 ~ GH`, which fails.
- **The obstacle.** For Gaussian bases the columns have normalized length
  about `sqrt e`, while `GH ~ (n/(2 pi e))^{1/2}`. So
  `lambda_1/GH <= e (2 pi/n)^{1/2} -> 0`.
  - The lattice has exponentially many vectors, namely short integer
    combinations of the near-orthogonal columns, whose length is below
    `s_1 = Theta(GH)`.
  - A first-moment estimate suggests their number exceeds `V = rho^{n/2}`
    for every `rho > 1`. We did not make this estimate rigorous.
  - Then the deletion and Turán arguments of Theorem 3.4 give nothing, and
    the caps of Theorem 3.5 can hold exponentially many lattice points.
- **A plausible route.** The conflicts in this model probably come from the
  near-tie structure of item (iii): coordinates of the optimum whose
  residual correlation `<r, b_i>` is close to `||b_i||^2/2`. Proving that
  such coordinates are numerous, and that cross-terms stay controlled at the
  random optimum, needs control of the landscape near the random optimum.
  This is the same obstacle as in the sparse-regression workstream.
- **Numerics are pre-asymptotic.** The bound `lambda_1/GH <= 6.8/sqrt n`
  exceeds 1 until `n ~ 46`. For `n <= 32` (Section 3.7), Gaussian-basis
  lattices have `lambda_1/GH ~ 1` and behave like Haar lattices. Small-`n`
  computations therefore cannot test the asymptotic Gaussian regime.
- **Conjecture 3.8.** For Gaussian-basis lattices with a uniform target,
  w.h.p. `omega >= 2^{c n}` for some `c > 0`. Status: open.

### 3.7 Numerical checks (random lattices, `n = 8..32`)

**Setup.**

- **Command:** `check_cvp_bounds.py`. The results are in `cvp_bounds.jsonl`
  (`n <= 20`) and `cvp_bounds_big.jsonl` (`n = 24, 28, 32`). The summary
  is produced by `summarize_cvp.py`.
- **Instances:** 30 per `(kind, n)`.
- **Lattices:**
  - "gm" are Goldstein–Mayer lattices
    `{x : x_1 = a.x_{2..n} mod p}`, scaled to determinant 1, with
    `p ~ 2^{2n+8}` for `n <= 20` and `p ~ 2^{44}` for `n >= 24`. They equidistribute to Haar measure as
    `p -> inf`.
  - "gauss" are Gaussian bases scaled to determinant 1.
- **Solver:** LLL, then exact enumeration. The target is `t = B U` with `U`
  uniform on `[0,1)^n`. Floating point is used throughout, with a relative
  tolerance of `1e-10` in the conflict test.

**Per-instance quantities.**

- `N43` is the number of lattice points with `phi < (4/3) OPT`.
- `M43` is the number of non-conflicting pairs among them.
- `om43` is the exact clique number of the conflict graph on those points
  (greedy if more than 150 points).
- `Nc/(n+1)` is the class-number lower bound certified by the proof of
  Theorem 3.5. Here `Nc` counts points with `phi < OPT + lambda_1^2/2`.
- `omg` is a greedy clique among all points with `phi < 2.5 OPT`
  (`n <= 20` only).

Medians:

| kind | `n` | `OPT/GH^2` | `lambda_1^2/GH^2` | `N43` | `M43` | `om43` | `Nc/(n+1)` | `omg` | `(4/3)^{n/2}` | `(3/2)^{n/2}` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gm | 8 | 0.97 | 1.11 | 3 | 0 | 3 | 0.67 | 7 | 3.2 | 5.1 |
| gm | 16 | 0.99 | 1.02 | 8 | 0 | 8 | 1.26 | 24 | 10.0 | 25.6 |
| gm | 20 | 0.98 | 1.03 | 17.5 | 0 | 16.5 | 2.43 | 43 | 17.8 | 57.7 |
| gm | 24 | 0.96 | 1.03 | 20.5 | 0 | 20.5 | 3.84 | – | 31.6 | 129.7 |
| gm | 28 | 0.99 | 1.06 | 52 | 0 | 52 | 11.5 | – | 56.1 | 291.9 |
| gm | 32 | 0.96 | 1.03 | 53 | 0 | 53 | 15.3 | – | 99.8 | 656.8 |
| gauss | 8 | 0.95 | 1.13 | 3 | 0 | 3 | 0.50 | 6 | 3.2 | 5.1 |
| gauss | 16 | 0.94 | 0.95 | 5.5 | 0 | 5.5 | 0.85 | 20 | 10.0 | 25.6 |
| gauss | 20 | 0.96 | 0.96 | 10.5 | 0 | 10.5 | 1.40 | 33 | 17.8 | 57.7 |
| gauss | 24 | 0.99 | 0.88 | 21.5 | 0.5 | 21 | 2.12 | – | 31.6 | 129.7 |
| gauss | 28 | 1.00 | 0.79 | 51 | 2.5 | 48.5 | 3.91 | – | 56.1 | 291.9 |
| gauss | 32 | 0.97 | 0.75 | 59.5 | 2.5 | 56 | 3.62 | – | 99.8 | 656.8 |

**What these numbers establish, and what they do not.**

- **Deterministic consequences hold on every instance, but they test only
  the code.**
  - `om43 >= N43 - M43`, the deletion step of Theorem 3.4, holds on all 420
    instances. It holds for every graph, since deleting one endpoint of each
    non-edge leaves a clique.
  - The greedy cliques never contained more than 3 points with
    `phi >= 2.2 OPT`. The proof of Proposition 3.6(c) shows at most 12, so
    this cannot fail either.
- **The Haar-lattice scales look as predicted.**
  - For Goldstein–Mayer lattices, `OPT/GH^2` is about 0.96–0.99 and
    `lambda_1^2/GH^2` about 1.03.
  - `N43` tracks `(4/3)^{n/2}`. `M43` is 0 in the median, so the whole
    `4/3`-ball is a clique.
- **Gaussian bases are drifting.** `lambda_1^2/GH^2` falls from 1.13 to
  0.75 over `n = 8..32`, and non-conflicting pairs appear at `n >= 28`. This
  is the start of the obstacle of Section 3.6(iv).
- **The class bound is weak at this size.** The certified bound `Nc/(n+1)`
  is still smaller than the clique at `n <= 32`, because of the `n + 1`
  factor.
  - For `n >= 24`, points were enumerated only up to `1.55 OPT`. So `Nc`
    is truncated when `lambda_1^2 > 1.1 OPT`, and the reported class bound
    is then conservative. It overtakes the clique asymptotically, since
  `0.2925 > 0.2612`.
- **Exponents cannot be read off.** Small-`n` data cannot test exponents.
  The greedy cliques at `n = 20` (43) already exceed `2^{0.2612 n} = 37`.
  This does not contradict Proposition 3.6(c), whose bound hides factors
  `2^{o(n)}`. The scout's `1.17^n = 2^{0.2265 n}` greedy growth lies inside
  the proven window `[2^{0.2075 n}, 2^{0.2612 n}]`. Small-`n` data cannot
  locate the exponent within it.
- **An atypical Gaussian instance.** For `n = 24`, seed 21, `OPT/GH^2` is
  1.22 and 84 of the pairs in the `4/3`-ball do not conflict. The greedy
  clique of 241 is still at least `N43 - M43 = 210`. This is the obstacle of
  Section 3.6(iv) in a small case.

## 4. Perspective relaxation versus the pairwise hull

### 4.1 The perspective relaxation in `z`

The problem is sparse ridge regression:

```
min ||y - X beta||^2 + lam ||beta||^2   s.t.  beta_i = 0 if z_i = 0,  z in {0,1}^p,  sum z <= k,
```

with `lam > 0`. Its perspective relaxation is

```
min ||y - X beta||^2 + lam sum_i s_i   s.t.  beta_i^2 <= s_i z_i,  z in [0,1]^p,  sum z <= k.
```

Minimizing out `(beta, s)` gives the projected relaxation `g(z)`, with the
convention that `beta_i^2 / 0` is `0` if `beta_i = 0` and `+inf` otherwise.

**Lemma 4.1.** For `z in [0,1]^p`,

```
g(z) = inf_beta { ||y - X beta||^2 + lam sum_i beta_i^2 / z_i } = y'(I + X diag(z) X'/lam)^{-1} y.
```

Moreover:

- `g` is convex;
- at binary `z` with support `S`, `g(z)` equals the ridge objective on `S`;
- a node relaxation with fixings `z_i in {0,1}` is `inf g` over the
  corresponding face.

*Proof.*

- **Formula.** Let `S = supp z` and `D = diag(z_S)`. The infimum is over
  `beta_S` of a strictly convex quadratic. Its value is
  `y'y - y'X_S (X_S'X_S + lam D^{-1})^{-1} X_S'y`. By the Woodbury identity
  this equals `y'(I + X_S D X_S'/lam)^{-1} y`, and
  `X_S D X_S' = X diag(z) X'`.
- **Convexity.** We have
  `g(z) = sup_w { 2y'w - ||w||^2 - sum_i z_i (x_i'w)^2 / lam }`, where the
  supremum is attained at `w = (I + X diag(z) X'/lam)^{-1} y`. This is a
  supremum of affine functions of `z`, hence convex. ∎

`check_perspective_gadget.py`, item 2, compares the formula with direct
minimization over `beta` at 40 digits on 20 random nodes, including zero
entries of `z`. The maximal difference is `4.6e-41`.

### 4.2 The block and its closed forms

The instance has `k` blocks.

- Block `j` lives in its own orthogonal copy of `R^2`, with features
  `u_j, v_j` of unit length and response `y_j`.
- `X` is block diagonal and `p = 2k`.
- By Lemma 4.1, `g(z) = sum_j g_j(z_{u_j}, z_{v_j})` with
  `g_j(a, b) = y_j'(I_2 + (a u_j u_j' + b v_j v_j')/lam)^{-1} y_j`, because
  the matrix is block diagonal.

For one block write `g00 = ||y||^2`, `g10 = g(1,0)`, `g01 = g(0,1)`,
`g11 = g(1,1)` and `ĝ = g(1/2, 1/2)`.

**Lemma 4.2 (symmetric block).** Let `u = e_1`, `v = (cos th, sin th)` with
`th in (0, pi)`, `c = cos th`, `w = (u+v)/||u+v||` and `y = s w` with
`s != 0`. Then

```
g00 = s^2,   g10 = g01 = s^2 (1 + 2 lam - c) / (2(1+lam)),   g11 = s^2 lam / (lam + 1 + c),
ĝ = 2 lam s^2 / (2 lam + 1 + c),
delta := g10 - ĝ = s^2 sin^2 th / (2 (1+lam) (1 + 2 lam + c)) > 0,
(g00 - g10) - (g10 - g11) = s^2 c (1 + c) / ((1+lam)(1+lam+c)).
```

So the diminishing-returns condition (i), `g00 - g10 > g10 - g11`, holds iff
`cos th > 0`.

*Proof.*

- **`g10`.** By Sherman–Morrison,
  `(I + uu'/lam)^{-1} = I - uu'/(lam+1)`. So
  `g10 = s^2 - s^2 (u'w)^2/(lam+1)`, where
  `(u'w)^2 = cos^2(th/2) = (1+c)/2`. `g01` is the same by symmetry.
- **`g11` and `ĝ`.** `w` is an eigenvector of `uu' + vv'` with eigenvalue
  `1 + c`. So `y` is an eigenvector of the matrices defining `g11` and `ĝ`,
  with eigenvalues `1 + (1+c)/lam` and `1 + (1+c)/(2 lam)`.
- **`delta`.** Over the common denominator the numerator is
  `(1+2lam)^2 - c^2 - 4lam(1+lam) = 1 - c^2`.
- **Condition (i).** A direct expansion gives the last display. ∎

These identities are checked symbolically (sympy residual 0) in
`check_perspective_gadget.py`, item 1. The factorization of the last display
is printed as `2 c (c+1)`.

### 4.3 The symmetric gadget

**Theorem 4.3.** Let `th in (0, pi/2)`, `s != 0`, `lam > 0` and `k >= 1`, and
let all blocks equal the block of Lemma 4.2. Let `0 <= eps < delta` and
`tau = OPT - eps`. Then:

- **(a)** `OPT = k g10`. The optimal supports are exactly the `2^k`
  one-per-block supports.
- **(b)** These `2^k` supports are pairwise midpoint-conflicting. Hence
  `kappa_tau(F) >= 2^k`. Every `F`-covering convex-piece `eps`-certificate
  with the perspective relaxation has at least `2^k` leaves. This covers
  variable, split, SOS and semantic branching, and it remains true with
  arbitrary cuts in `z` (Theorem 1.8(a)). With incumbent-based reductions at
  every node, at least `2^k/(2k+1)` nodes are needed (binaries, Theorem 1.8(c)).
- **(c)** Replace each block's perspective terms by the convex hull of the
  block's mixed-integer epigraph (a 4-term disjunctive formulation in
  `(z, beta, s)`). Then the root bound equals `OPT`, and a single node
  suffices once the incumbent is known.

*Proof.*

- **(a)** Let `b_j in {0,1,2}` be the number of features that a support uses
  in block `j`. The value is `sum_j H(b_j)` with `H(0) = g00`,
  `H(1) = g10` and `H(2) = g11`.
  - Let `pi = g10 - g11 > 0`; adding a feature cannot increase the ridge
    value, and here `pi > 0` by the closed forms.
  - Then `H(b) >= g10 - pi (b - 1)` for `b in {0,1,2}`. There is equality
    at `b = 1, 2`. At `b = 0` the inequality is strict, by condition (i),
    since `c > 0`.
  - Summing, `sum_j H(b_j) >= k g10 - pi (sum_j b_j - k) >= k g10`.
  - Equality requires `sum b_j = k` and no `b_j = 0`, hence all `b_j = 1`.
    Every such support has value `k g10`.
- **(b)** Let two one-per-block supports differ on a nonempty block set `D`.
  - Their midpoint equals `(1/2, 1/2)` on the blocks in `D`, agrees with
    both supports elsewhere, and has `sum z = k`, so it lies in the
    relaxation's domain.
  - By separability, `g(mid) = OPT - |D| delta <= OPT - delta < tau`.
  - Apply Theorem 1.6, Lemma 1.5 and Theorem 1.8. There are `n = 2k`
    binary variables, so `n + 1 = 2k + 1`.
- **(c)** The hull relaxation's value at a block point `z_j` is at least
  `min { sum_p mu_p G(p) : mu in Delta_4, sum_p mu_p p = z_j }`, with
  `p in {0,1}^2` and `G(p) = H(|p|)`.
  - For `mu` in the simplex, `sum_p mu_p G(p) >= sum_p mu_p (g10 - pi(|p| - 1))`.
    With `pi` as in (a) this equals `g10 - pi(z_{u_j} + z_{v_j} - 1)`.
  - Summing over blocks and using `sum z <= k` gives root value at least
    `k g10 - pi (sum z - k) >= k g10 = OPT`.
  - This is weak LP duality, with `nu_j = g10 + pi` as the certificate. ∎

**Exact minimum variable-branching trees (from the review; not proved
here).** For `th = 0.3`, `s = 3`, `lam = 1` and `k <= 8`, the minimum number
of leaves is `2^k` when `eps` is just below `delta`, and `2^{k+1} - 2` as
`eps -> 0`. For `k = 2`, the exact minimum over arbitrary convex pieces is 6
at `eps = 1e-6`, while the midpoint bound is 4. So the hypergraph refinement
is strictly stronger here too.

### 4.4 An asymmetric gadget: unique optimum, no symmetry

The symmetric gadget has a `Z_2^k` symmetry. Orbital fixing `z_{v_j} = 0`,
which Theorem 1.8(d) excludes, makes its root exact. The following variant
has no symmetry and a unique optimum.

**Theorem 4.4.** Let block `j` have arbitrary unit features `u_j, v_j` and a
response `y_j`. Define `g*_j = min(g10_j, g01_j)`,
`Delta_j = |g10_j - g01_j|` and `delta_j = g*_j - ĝ_j`. Assume:

- **(H1)** `max_j (g*_j - g11_j) < min_j (g00_j - g*_j)` (global
  diminishing returns);
- **(H2)** `sum_j Delta_j + eps < min_j delta_j`.

Then:

- **(a)** `OPT = sum_j g*_j`. If every `Delta_j > 0`, the optimal support is
  unique: in each block it picks the better feature.
- **(b)** All `2^k` one-per-block supports are pairwise midpoint-conflicting
  at `tau = OPT - eps`, so every certificate as in Theorem 4.3(b) has at
  least `2^k` leaves.
- **(c)** The pairwise-hull relaxation has root bound `OPT`.

*Proof.* Choose `pi` in the nonempty interval
`[max_j (g*_j - g11_j), min_j (g00_j - g*_j)]`. Then `pi > 0` and
`H_j(b) >= g*_j - pi (b - 1)`, with `H_j(1) = g*_j`.

- **(a)** Argue as in Theorem 4.3(a) and (c). For uniqueness, pick `pi` in
  the interior of the interval, so that `b_j in {0,2}` is strict; then use
  `Delta_j > 0` inside each block.
- **(b)** For two supports that differ on `D != ∅`:
  `g(mid) <= sum_{j in D} (g*_j - delta_j) + sum_{j not in D} (g*_j + Delta_j)`.
  The right side is at most `OPT - min_j delta_j + sum_j Delta_j < OPT - eps`.
- **(c)** The dual certificate is the same `pi`. ∎

**Exact instances** (`check_perspective_gadget.py`, items 3–5, rational
arithmetic).

- **Symmetric instance.** `u = (1,0)`, `v = (3/5, 4/5)`, `y = u + v` and
  `lam = 1`, so `s^2 = 16/5`.
  - Block values: `g00 = 16/5`, `g10 = g01 = 48/25`, `g11 = 16/13`,
    `ĝ = 16/9`, and `delta = 32/225`, which equals the closed form.
  - `(g00 - g10) - (g10 - g11) = 192/325 > 0`.
  - For `k = 2, 3, 4`, all supports with `|S| <= k` were enumerated
    (11, 42 and 163 supports) using the full `2k x 2k` matrix.
    - `OPT = k g10` exactly.
    - The optimal supports are exactly the `2^k` one-per-block supports.
    - Every pairwise midpoint has value exactly `OPT - |D| delta`.
  - The hull dual certificate gives exactly `k g10` for `k = 2, 5, 10`.
- **Asymmetric instance.**
  - Features: `u_j = (1,0)` and six distinct Pythagorean directions `v_j`,
    from `(3/5, 4/5)` to `(28/53, 45/53)`, with cosines between `0.32` and
    `0.69`.
  - Responses: `y_j = sigma_j (u_j + v_j) + (p_j, 0)`, where the scales
    `sigma_j` equalize `s_j^2` and the rational perturbations `p_j` have
    size about `1/200`.
  - Results:
    - (H1) and (H2) hold exactly for `k = 2, 3, 4, 6`.
    - At `k = 6`: `sum Delta = 0.0225 < min delta = 0.1120`, so any
      `eps < 0.0895` is allowed.
    - All `2k` singleton values are distinct.
    - For `k <= 4`, exhaustive exact enumeration confirms a unique optimum
      equal to `sum g*_j`, and that all `C(2^k, 2)` pairs of one-per-block
      supports conflict, with midpoints computed from the full matrix.
    - The hull dual certificate equals `OPT` exactly.

*Interpretation.* On these instances every branching scheme, with any cuts
in `z` and any incumbent-based tightening (up to the factor `2k+1` in nodes), needs
`2^k` leaves. One convexification in `(z, beta, s)` space removes all
conflicts. This is a relaxation-intrinsic form of "strengthening beats
branching", and it holds without exploitable symmetry.

## 5. The path lemma and root probing

**Setting.**

- Integer variables have finite bounds `l <= x <= u`, and `P` is the set of
  integer points of the box.
- Branching is on variables. Every branching is *proper*: both children
  contain integer points of the parent box.
- The node bound is `r(box)`, which is automatically monotone under added
  fixings.

**Lemma 5.1 (path lemma).** Let `x° in F` and suppose the incumbent value
`UB = f(x°)` is available when each node is created or selected, and that the
node is pruned before branching if `r >= UB - eps`. Assume

```
(C1)  r(box ∩ {x_i <= x°_i - 1}) >= UB - eps  for every i with l_i < x°_i,
      r(box ∩ {x_i >= x°_i + 1}) >= UB - eps  for every i with x°_i < u_i.
```

Then every such run, with any branching rule and any node selection,
processes at most `2D + 1` nodes. Here `D <= sum_i (u_i - l_i)` is the number
of branchings at nodes that contain `x°`. For binary variables, `D <= n`.

*Proof.*

- **Nodes without `x°` are pruned.** A node box that does not contain `x°`
  lies in `box ∩ {x_i <= x°_i - 1}` or in `box ∩ {x_i >= x°_i + 1}` for
  some `i`. By monotonicity and (C1), its bound is at least `UB - eps`, so
  it is pruned when it is created or selected. Hence only nodes that contain
  `x°` are branched.
- **The branched nodes form a chain.** At each such branching exactly one
  child contains `x°`. So the branched nodes form a chain of length `D`, and
  the tree has at most `1 + 2D` nodes.
- **Bounding `D`.** A proper branching strictly shrinks the integer range of
  one coordinate. So `D <= sum_i (u_i - l_i)`. ∎

*The incumbent hypothesis is needed.* The review's `lemma4_order.py` uses
`phi = sum_i (z_i - 0.1)^2` with `p = 10`, where C1 holds. Depth-first search
that explores the `z_i = 1` child first uses 21 nodes when `UB = OPT` is
known from the start, and 351 nodes when it is not. Best-bound order alone
does not fix this for `eps > 0`: an off-path node with bound in
`[OPT - eps, OPT)` may be branched before the incumbent is found.

**Proposition 5.2 (C1, probing and the class number).**

- **(a) C1 is root probing.** (C1) holds iff root probing with incumbent
  `UB = f(x°)` removes all `2n` one-sided pieces `{x_i <= x°_i - 1}` and
  `{x_i >= x°_i + 1}`, that is, iff probing fixes `x = x°`. If moreover
  `phi(x°) = f(x°)`, the reduced root `{x°}` is pruned by bound. The run then
  uses one node plus `2n` probes.
- **(b) C1 bounds the class number.** Under (E) and (C1),
  `kappa_tau(P) <= 2n + 1` for `tau = OPT - eps`. So in the (C1) regime,
  both the class number and the variable-branching tree (at most `2n + 1`
  nodes for binaries, by Lemma 5.1) are `O(n)`. They need not agree up to a
  constant factor.
  - Example: `phi(z) = sum_{i=1}^{n} (z_i - a)^2` with `a = 1/(2n)`, on
    `K = [0,1]^n`, with `eps = 1/(8n^2)`.
  - (C1) holds, `kappa_tau = 2`, and every variable-branching certificate
    has at least `n + 1` leaves and `2n + 1` nodes.
  - So the node count can exceed `kappa` by a factor of about `n`. The
    first version of this note wrongly claimed a factor of at most 2.
- **(c) C1 is weaker than root exactness.** Root exactness
  (`r(R^n) >= UB - eps`) implies (C1) by monotonicity. The converse fails.
  Take `phi = sum_{i=1}^{p} (z_i - 0.1)^2` on `[0,1]^p` with `p <= 80` and
  small `eps`:
  - the root bound is `0 < OPT - eps = 0.01 p - eps`;
  - every single wrong fixing has bound `0.81 >= OPT`.

*Proof.*

- **(a)** This is the definition of probing against `UB - eps`, together
  with Lemma 5.1 applied with `D = 0`.
- **(b)** The classes are the `P`-points in each one-sided piece, with bound
  at least `UB - eps >= OPT - eps` by (C1), together with the class `{x°}`,
  whose bound `phi(x°)` is at least `OPT` by (E). Every other box point lies
  in some one-sided piece.
- **(b), example.**
  - `OPT = n a^2 = 1/(4n)`, attained only at `z = 0`.
  - A wrong fixing `z_i = 1` has bound `(1-a)^2 >= 1/4 >= OPT`, so (C1)
    holds.
  - The classes `{0}` and `{0,1}^n ∩ {1.z >= 1}` are admissible. The
    minimum of `phi` over `[0,1]^n ∩ {1.z >= 1}` is attained at the
    projection `(1/n) 1` of `a 1`, where it equals `1/(4n) = OPT`. The root
    bound is `0 < tau`, so `kappa = 2`.
  - A node that fixes a set `S` of variables to 0 and none to 1 has bound
    `|S| a^2 = |S|/(4n^2)`. This is at least `tau = 1/(4n) - 1/(8n^2)` only
    when `|S| = n`.
  - So the leaf containing `0` fixes all `n` variables. Its root path makes
    `n` branchings, each with a sibling, which gives at least `n + 1` leaves
    and `2n + 1` nodes.
  - `check_revision.py` (R3) confirms these counts exactly for
    `n = 2..8`.
- **(c)** The computations are immediate. ∎

*Remarks.*

- (C1) is a statement about `2n` single fixings. It is the "easy side"
  counterpart of the conflict bound: large cliques force large trees, and
  (C1) forces linear trees.
- There is no converse. A small `kappa` does not imply (C1) (Proposition 2.4
  has `kappa = 2`).
- The sparse-regression workstream studies when (C1) holds with high
  probability.

## 6. Checks run

All commands ran from `research-20260928b/bb-complexity/integer-core/`, with
Python 3.13, NumPy 2.5, SciPy 1.18, SymPy 1.14 and mpmath 1.3. These are
targeted local checks. No project-wide checks were run, and CI was not
inspected. No scout code was reused. The lattice utilities
(`lattice_tools.py`: LLL, enumeration, Goldstein–Mayer and Gaussian bases,
exact maximum clique) were written for this workstream.

| Command | Establishes | Result |
|---|---|---|
| `python3 check_perspective_gadget.py` (`.log`) | Lemma 4.1 formula (40 digits); Lemma 4.2 closed forms and condition (i) (symbolic); Theorems 4.3–4.4 on exact rational instances, including exhaustive support enumeration and full-matrix midpoints for `k <= 4`, and the hull dual certificates | all checks pass; maximum formula deviation `4.6e-41`; symbolic residuals 0 |
| `python3 check_cvp_integrals.py` (`.log`) | the pair-count bound of Theorem 3.4 against the exact integral (30 digits, `n <= 320`); threshold `rho = 4/3`; lens formula against Monte Carlo | ratio exact/bound at most `0.059`; the exponent changes sign at `rho = 4/3` |
| `python3 check_cvp_exponents.py` (`.log`) | the constants `0.2075`, `0.2925`, `e_+ = 0.26124` (`rho* = 1.436424`), Remark 3.5a (`0.2975`), and `R_KL(60°) = 0.4014` | as stated |
| `python3 check_cvp_bounds.py 8,12,16,20,24,28 30 cvp_bounds.jsonl gm,gauss 16` | Section 3.7 for `n <= 20` | 240 instances. The run was stopped at `n = 24`, where 56-bit Goldstein–Mayer entries exceeded float LLL precision. The prime size was then capped at `2^44`. |
| `python3 check_cvp_bounds.py 24,28,32 30 cvp_bounds_big.jsonl gm,gauss 12` | Section 3.7 for `n = 24..32` | 179 of 180 instances. One Gaussian instance (`n = 24`, seed 21) was stopped because its exact clique search (294 vertices) was too slow. It was rerun alone (`missing_instance.log`) after two changes: CVP by growing radius, and an exact clique only when `N43 <= 150`, else greedy. |
| `python3 summarize_cvp.py cvp_bounds.jsonl cvp_bounds_big.jsonl` (`cvp_summary.log`) | the table of Section 3.7; deterministic consequences on every instance | 420 instances; 0 violations |
| `python3 check_framework_small.py` (`.log`) | Part A: the 1D counterexample and `kappa <= L + S` under one sequential incumbent-OBBT pass per node (exact `kappa`, exact minimum OBBT trees, 40 instances on `[0,2]^2`); the `(2n+1)N` part is vacuous there (Theorem 2.2(b) gives `kappa <= 4`). Part B: Proposition 2.1(a) (exact `kappa`, 30 ILPs on `[0,2] x [0,3]`). Part C: Proposition 2.4 (exact minimum variable trees, `n = 3, 5, 7`) | Part A: 0 violations; the leaf form fails in all 40 instances. Part B: 30 instances with a root gap, `kappa in {2, 3}`, 0 violations of `kappa <= q + 1`, with equality in 6 instances. Part C: minimum leaves 6, 20, 70 `= C(n+1, h)`; `kappa = 2` |
| `python3 check_revision.py` (`.log`), added after the review; R1 and R4(b) strengthened after the recheck | R1: the caterpillar counterexample of Theorem 1.7 (exact rational). Then 25 random 2-D instances with `kappa >= 3` (exact), testing all minimum partitions (up to 30) and orderings (up to 24): leaf bounds, and covering at every internal node point by point, for the gradient-halfspace chain and for the old caterpillar. R2: Example 2.1a. R3: the Proposition 5.2(b) counterexample (exact DP, `n = 2..8`). R4(a): Theorem 1.8(c) for binaries, `n = 3`, iterated incumbent probing (40 instances, exact `kappa` and minimum trees). R4(b): general integers with iterated sequential OBBT, each bound change of any size being one piece (100 instances). R5: `delta` ranges | R1: `(1,1) ∈ conv(I_2 ∪ I_3)` but in neither child. The chain is valid on 4290 of 4290 (partition, ordering) pairs; the caterpillar is invalid on 292 of them. R2: all pairs conflict for `n <= 10`; the halfspaces cover the window for `n <= 4`. R3: (C1) holds, `kappa = 2`, and the minimum tree has `n+1` leaves and `2n+1` nodes. R4(a): 0 violations of `kappa <= L+S` and `kappa <= (n+1)N`; maximum `kappa/N = 4 = n+1`, so the binary bound is attained. R4(b): 0 violations of `kappa <= L+S`; slack 0 in 25 of 100 instances; up to 5 > `2n` bound changes at one node. R5: `0.0858` and `0.1315` |

The earlier SLSQP-based version of `check_framework_small.py` was too slow
and was stopped. It was replaced by an exact 2-D computation (unconstrained
minimizer if it lies in the hull, else the minimum over segments), which is
the version recorded above.

The review's own checks (`reviews/bb-conflict/*.py`) were not rerun. Their
reported numbers are cited as such. Floating-point tolerances are about
`1e-9` to `1e-10`, and all margins in the checks are orders of magnitude
larger. The Section 4 checks use exact rational arithmetic.

## 7. Sources examined, novelty, and corrections

### 7.1 Sources examined in this workstream

**Local full texts:**

- **Dey–Dubey–Molinaro, "Lower bounds on the size of general branch-and-bound
  trees"** (Math. Prog. 198, 2023; local
  `dey2023-lower-bounds-on-the-size`). Read: Sections 1–2 (model, BB
  hardness), 4 (Lemma 7, the generalized Dadush–Tiwari Helly argument, and
  the packing polytope), 5 (Proposition 3, the midpoint argument for the
  cross-polytope), and, after the review, 6 (perturbed cross-polytope,
  Lemma 12 and the proof of their Theorem 2). DDM state that their packing and set-cover instances use
  exponentially many constraints. They also restate Dadush–Tiwari's open
  question on polytopes with polynomially many constraints.
- **Gläser–Pfetsch, "Sub-exponential lower bounds for branch-and-bound with
  general disjunctions via interpolation"** (SODA 2024, arXiv 2308.04320;
  local `glaser2024-sub-exponential-lower-bounds-for`). Read: abstract,
  Section 1, Theorems 1–5 and 7, Corollary 6, and the clique–coloring
  system. Their introduction notes that hiding-set and Dadush–Tiwari
  strategies "cannot exceed the number of constraints"; Proposition 2.1 is a
  formal version of this remark. It also cites Gläser–Pfetsch (Math. Prog.
  2023), who use hiding sets for variable-branching trees.
- **Kaibel–Weltge, "Lower bounds on the sizes of integer programs without
  additional variables"** (Math. Prog. 154, 2015; local
  `kaibel2015-lower-bounds-on-the-sizes`). Read: Definition 1 (hiding set)
  and Proposition 7. A hiding set is exactly a clique of the segment graph
  `G^seg` for `phi ≡ 0` on `K = conv X`. Their proof ("each facet is
  violated by at most one point of `H`") is the pairwise case of Lemma 1.5.
- **Averkov–Schymura, "Complexity of linear relaxations in integer
  programming"** (Math. Prog. 194, 2022; local
  `averkov2022-complexity-of-linear-relaxations-in`). Metadata only. It is
  the relaxation-complexity literature to which Theorem 2.2 is analogous.

**Review material.**

- The independent reviews
  [`bb-conflict-review.md`](../../reviews/bb-conflict-review.md) and
  [`integer-core-review.md`](../../reviews/integer-core-review.md), with
  their scripts. We used their reported numbers and counterexamples, and
  re-derived each fix ourselves (Section 9).
- The second review also searched arXiv for "relaxation complexity" (13 hits,
  none on B&B trees). It read the PDF display of the Gläser–Pfetsch system
  and the current Reis–Rothvoss abstract.

**Online, via arXiv API listing queries** (2026-09-28; the web-search quota
of this session was exhausted):

- `abs:"branch-and-bound" AND abs:tree AND abs:"lower bound" AND abs:size`
  (6 hits; only DDM and Gläser–Pfetsch are relevant, and both are linear);
- `all:"branch-and-bound" AND all:"lower bound" AND all:convex AND all:integer`
  (10 hits, none on tree size);
- `abs:"sphere decoding" AND abs:complexity AND abs:"lower bound"` (5 hits,
  all fixed-decoder results).

**Standard results used from memory** (statements not re-read in this
session):

- Siegel's mean value theorem (1945);
- Lovász (1989) and Basu–Conforti–Cornuéjols–Zambelli (2010, Theorem 1.2)
  on maximal lattice-free convex sets;
- the flatness theorem, with the constants of Banaszczyk–Litvak–Pajor–Szarek
  (1999) and Reis–Rothvoss (2023);
- the Kabatiansky–Levenshtein bound (1978), whose standard form and
  60-degree value `0.4014` were checked numerically;
- Goldstein–Mayer (2003) equidistribution;
- Jeroslow (1974);
- the Micciancio–Voulgaris Voronoi-cell algorithm.

### 7.2 Novelty assessment (cautious)

- **Lemma 1.5, Theorem 1.6.**
  - The pairwise part is the DDM midpoint argument and the Kaibel–Weltge
    hiding-set argument.
  - The counting bound of Lemma 1.5(b) is DDM's argument for the perturbed
    cross-polytope (their Section 6). There, Lemma 12 uses the Sauer–Shelah
    lemma: more than `sum_{i<s} C(n,i)` points of `{0,1}^n` in a leaf force
    a point with `s` half-coordinates into the leaf's hull, and the number of
    leaves follows by division. So the non-pairwise "at most `X` points per
    leaf" technique is DDM's. Theorem 3.5 uses the same mechanism, with a
    cap and obtuse-set estimate in place of Sauer–Shelah.
  - Using *objective* curvature to make feasible, near-optimal points
    conflict appears new in the sources above, but it is a short extension.
    Novelty: low to moderate.
- **Theorem 1.7 (exactness of the class number) and Theorem 1.8(a),(c).**
  These are simple. The formulation "the class number is the exact semantic
  tree size" was not found. The node form under incumbent reductions follows
  the review. Novelty: low to moderate.
- **Proposition 2.1 and Theorem 2.3.** The observation is elementary, and
  the separation is a direct corollary of Gläser–Pfetsch. Its value is
  clarifying: it answers the scout's Q3(i) negatively. Novelty: low, with
  useful consequences.
- **Theorem 2.2 (lattice-free facet characterization, `kappa <= 2^n`).**
  This is separation plus Lovász's facet bound. In the linear infeasibility
  case `kappa` is a relative relaxation complexity in the sense of
  Kaibel–Weltge and Averkov–Hojny–Schymura (Section 2.2), and Theorem 2.2 is
  the sublevel-set analogue. Novelty: low to moderate.
- **Theorems 3.4–3.5 and Proposition 3.6 (random CVP exponents and the
  clique–class separation).** No branching-independent lower bound for CVP
  or integer least squares appears in the sources examined. All
  sphere-decoding lower bounds found concern fixed decoders. The methods are
  standard: Siegel's formula, second moments, Rankin-type counting and
  Kabatiansky–Levenshtein. The class bound follows DDM's per-leaf counting
  scheme. Novelty: moderate. The lattice-enumeration
  lower-bound literature (Hanrot–Stehlé, Aono et al.) was checked only
  through the review's abstracts.
- **Section 4.** The weakness of the perspective relaxation on correlated
  pairs is folklore. The branching-independent `2^k` statement and the
  asymmetric variant were not found. Novelty: low to moderate.
- **Proposition 2.4.** This is Jeroslow's instance. The lattice-path count
  is standard, and we did not check whether the exact count appears in the
  literature.
- **Section 5.** Likely folklore. Novelty: low.

An unsuccessful bounded search does not establish novelty.

### 7.3 Corrections from the review, and where they are handled

| Review finding | Here |
|---|---|
| Robustness remark false; node form `chi/(2n+1)` holds | Theorem 1.8(c), Proposition 1.9; checked in `check_framework_small.py`, Part A |
| Need infeasible-endpoint conflicts, finite trees, `inf` for `min` | Definitions 1.1 and 1.4 (conflicts need only the midpoint or segment point in `K`), Theorem 1.6 |
| Segment graph as a free refinement | Definition 1.4, Lemma 1.5 |
| Cuts in `x` valid for feasible points do not remove conflicts | Theorem 1.8(a),(b),(d) |
| Theorem 2: strictness, range of `delta`, sphere decoders `V/6`, tightening `V/(2(2n+1))`, numerics on Gaussian bases | Theorems 3.4 and 3.5 use open balls; the `delta` ranges are `(0, 0.08)` for Theorem 3.4 (vacuous from `0.0858`) and `(0, 0.1)` for Theorem 3.5 (vacuous from `0.1315`); the scout's shell bound is superseded; Remark 1.10 (factor 3), Section 3.5, Section 3.7 (Haar-like lattices are reported separately) |
| Theorem 3: closed form of `delta`, condition (i) iff `cos th > 0`, exact tree sizes, symmetry caveat | Lemma 4.2, Theorem 4.3, Section 4.3 remark, Theorem 4.4 |
| Lemma 4: incumbent needed | Lemma 5.1 hypothesis and the remark after it |

## 8. Open problems

1. **Tightness for convex quadratics (Open problem 2.6).** For unconstrained
   convex integer quadratic minimization, is the minimum split-tree
   certificate `poly(n) * kappa^{O(1)}`? For unconstrained piecewise-linear
   convex objectives the answer is no (Theorem 2.3(b)).
   - An exponential split-tree lower bound for an integer-free ellipsoid
     whose `kappa` is polynomial would settle it negatively.
   - Split-tree certificates of size `2^{O(n)}` for all CVP instances would
     be a (surprising) step toward a positive answer.
2. **Exponents for random CVP.** Close the window
   `0.2075 <= e(omega_mid) <= 0.2612` and `0.2925 <= e(kappa) <= 0.5`. Also
   bound `chi(G^mid)` and the segment graph, which Proposition 3.6(c) does
   not cover.
   Conjecture 3.7 claims `e(kappa) = 1/2`. A proof would follow from a
   uniform `2^{o(n)}` bound on the number of lattice points in the caps
   (Section 3.6(ii)), for example via Rogers' higher moment formulas.
3. **Gaussian-basis lattices (Conjecture 3.8).** Show exponential cliques or
   class numbers for Gaussian bases, with uniform targets or in the MIMO
   model.
4. **When is `kappa` attained by splits?** Find structural conditions beyond
   fixed dimension (Proposition 2.5) and beyond condition (C1)
   (Proposition 5.2) under which split or variable trees are within
   `poly(n) * kappa` leaves. The linear case shows that such conditions must
   exclude compact infeasible "cores". The quadratic Jeroslow instance shows
   that for variable branching they must exclude parity structure.
5. **Exact minimum variable-branching trees for the perspective gadget.**
   Prove the review's observation: `2^{k+1} - 2` leaves as `eps -> 0`, and
   `2^k` for `eps` close to `delta`.
6. **Iterated bound tightening.** Can iterated incumbent-based propagation on
   general integers actually violate `N >= kappa/(2n+1)`? The proof of
   Theorem 1.8(c) gives this bound only for one pass per node, but no
   counterexample is known.

## 9. Revision after review (2026-09-29)

The review [`integer-core-review.md`](../../reviews/integer-core-review.md)
(scripts in `reviews/integer-core/`) found one invalid proof, three false
claims, and several gaps. We re-derived each fix ourselves; the new checks are
in `check_revision.py` (log `check_revision.log`). The table lists the
changes.

| # | Review finding | Change in this note | Own check |
|---|---|---|---|
| 1 | Theorem 1.7(b): the caterpillar tree (`conv I_1`, then `conv(I_2 ∪ … ∪ I_kappa)`) violates the covering condition; exact counterexample | The proof is replaced. Lemma 1.7a (hemispaces, with a self-contained proof by induction on dimension) gives leaves `G_j ⊇ conv I_j` avoiding `E = {phi < tau}`, and the internal nodes are the convex complements `N_j`. Closed halfspaces suffice when `E` is open, with explicit gradient halfspaces for differentiable `phi`. Polytopes suffice for finite `P` via `conv(S ∩ P)`. The counterexample is recorded after the theorem. | R1 |
| 2 | "The class number of a compact linear program is always polynomial" is false for MILPs | Restricted to pure integer programs in the Summary and the Section 2 opening. Example 2.1a (a compact MILP with `2n` rows and `kappa = 2^n`) is added, with proof. | R2 |
| 3 | Proposition 5.2(b): "variable branching attains `kappa` up to a factor 2 in nodes" is false | Replaced by "both are `O(n)`". The counterexample family (`kappa = 2`, `2n+1` nodes) is added, with proof. | R3 |
| 4 | Section 3.6(i): Proposition 3.6(c) bounds only the midpoint clique | Reworded to "midpoint-clique argument". `chi(G^mid)` and the segment graph are stated as not bounded, in the Summary and in Open problem 2. | — |
| 5 | Theorem 1.8(c): pieces were certified on the unreduced set; `s_v <= 2n` holds only for one pass; binaries give `n+1`; the node-form test was vacuous | (c) is restated for sequential removals certified on the current set (chain construction; same leaf count). The count is one piece per bound change. `N >= kappa/(2n+1)` is claimed for one pass per node only, with `N >= kappa/(n+1)` for binaries even with iterated passes. (b) is weakened to `Q̄_v ∩ F ⊆ Q'_v`, which covers rounded FBBT. New tests that can fail are added. Iterated passes on general integers are listed as Open problem 6. | R4(a),(b) |
| 6 | Theorem 2.3: `psi = t^2` is not strictly increasing; the encoding exponent depends on the convention; the (b) instances are unconstrained convex | The hypothesis is now `psi` convex and strictly increasing on `[0, inf)`, with the proof redone. The bound is stated as `2^{n^{1/6 - o(1)}} = 2^{L^{Omega(1)}}`, with `1/12` (Gläser–Pfetsch), `1/14` (dense) and `1/8` (sparse). The open question is narrowed to convex *quadratic* objectives in the Summary, Section 2.6, Open problem 2.6 and Section 8. | — (the statement is cited; the review's `gp_system.py` checked `t* = 1` on a small instance) |
| 7 | Theorem 3.4 is vacuous for `delta > 0.0858` | Range changed to `delta in (0, 0.08)` with `rho((1-delta)^2 - delta) > 1`, and the threshold `(3 - sqrt 8)/2` is stated. Theorem 3.5's threshold `(4 - sqrt 13)/3 = 0.1315` is stated. | R5 |
| 8 | Novelty: DDM Section 6 (Lemma 12) is the per-leaf counting mechanism; `kappa` is a relative relaxation complexity | Credited in the Summary and Section 7.2, after reading DDM Section 6 ourselves. The Section 2.2 remark now states the relaxation-complexity identification. Theorem 2.2's novelty is lowered to low to moderate. | — |

**Minor changes.**

- Proposition 2.4 "exactly": also requires that no node with bound at least
  `tau` is branched. We also note that the count holds for the linear
  Jeroslow instance.
- Proposition 2.5: the current Reis–Rothvoss flatness constant
  `O(j log^2(2j))` is cited.
- Proposition 3.6(b): `ceil(...) + 1` in the covering lemma, for a strict
  union bound.
- Section 3.6(iii), random `t`: now labelled as a remark, with a sketch.
- Section 3.7: states that the "deterministic consequences" can only test
  the code, and that `Nc` is truncated (conservative) for `n >= 24`.
- Theorem 4.3(b): node factor `2k + 1` for binaries, instead of `4k + 1`.
- Theorem 2.3: states that the review read system (2) in the PDF (integral
  rows).

**Commands run for this revision** (from this directory; targeted local
checks only; no project-wide checks, CI not inspected).

- `python3 check_revision.py > check_revision.log`, covering R1–R5. The
  results are in the Section 6 table.
- R1 and R3 use exact rational arithmetic. R4 uses floating point with
  tolerances of `1e-9` to `1e-12` for bounds and uses exact enumeration for
  `kappa`.

The earlier checks (`check_perspective_gadget.py`, `check_cvp_*.py`,
`check_framework_small.py`) cover statements whose content did not change, so
they were not rerun. Only the text describing what `check_framework_small.py`
Part A establishes was corrected.

### 9.1 Second round (recheck of 2026-09-29)

The recheck [`integer-core-recheck.md`](../../reviews/integer-core-recheck.md)
found all six revisions correct and listed minor points. Changes:

| # | Recheck point | Change |
|---|---|---|
| 1 | Theorem 1.7(b) for `kappa = 1`: 2 nodes, and a root with a single child | For `kappa = 1` the tree is the single node `G_1` (or `conv P` for finite `P`), whose set contains `P`. The case `kappa = 2` is spelled out. |
| 2 | Lemma 1.7a: "nonzero" should be "non-constant" affine functional | Reworded. The separation step now cites proper separation of `0` from `A - B`, since `0` is not in `ri(A - B)` (Rockafellar, Theorem 11.3), so `H` is a hyperplane. |
| 3 | Theorem 1.8(c): the bound `sum_i (u_i - l_i)` on bound changes needs `+1` when the node empties | Added, together with the recheck's example of 5 changes at one node in dimension 2. |
| 4 | R4(b) counted unit steps, not one piece per change of any size; R1 tested one partition per instance, mostly with `kappa <= 2` | R4(b) now implements the stated rule: the largest certified move of a bound is one piece. Over 100 instances: 0 violations, slack 0 in 25, and up to 5 changes at one node. R1 now uses 25 instances with `kappa >= 3`, all minimum partitions (up to 30) and orderings (up to 24), and checks covering point by point: the chain is valid on 4290 of 4290 pairs, and the caterpillar is invalid on 292. The descriptions in Proposition 1.9 and Section 6 were updated. The earlier minimum slack of 1 came from the unit-step counting. |
| 5 | Optional: closed halfspaces suffice for MILP relaxations; hemispaces are needed only in non-open, non-polyhedral cases | Added as Theorem 1.7(c)(iv), with the Motzkin-transposition argument and a pointer to the recheck's example. |
| 6 | The remark after Theorem 2.3 about integer points "with `t` near 0" was unclear | Rewritten. Integer points have `t >= 1`. The leaves must exclude the fractional region `P_r`, where the relaxation value can be at most 0, while the splits cover `Z^n`. |

Command for this round, run from this directory: `python3 check_revision.py
> check_revision.log`, which reruns R1–R5 with the strengthened R1 and R4(b).
No other checks were affected.

