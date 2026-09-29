# Review: relaxation-intrinsic lower bounds for integer branching (integer-core)

Target: `research-20260928b/bb-complexity/integer-core/relaxation-intrinsic-bounds.md`
and its check scripts in the same folder. Context read:
`bb-complexity/PROGRAM.md`, `scouting/bb-tree-size-convex.md`,
`reviews/bb-conflict-review.md`, and the local full texts of Gläser–Pfetsch
(including the PDF display of their system (2)), Dey–Dubey–Molinaro (DDM) and
Kaibel–Weltge.
Date: 2026-09-29. Reviewer: independent adversarial review; I did not write the
material. I did not edit the note and did not commit. My scripts and logs are in
[`integer-core/`](integer-core/). I reused only the author's *data* for the
asymmetric gadget (three lists of rationals); all computations are my own code.

## Verdict summary

| Claim | Verdict | Main point |
|---|---|---|
| Lemma 1.3, Lemma 1.5, Theorem 1.6 | correct | — |
| Theorem 1.7(a) (depth-one tree attains `kappa`) | correct | — |
| Theorem 1.7(b) (binary branching attains `kappa`) | **correct claim, invalid proof** | The caterpillar with children `conv I_1`, `conv(I_2 ∪ … ∪ I_kappa)` violates the covering condition of Definition 1.1 whenever `conv(I_2 ∪ … ∪ I_kappa)` contains a point of `I_1`. Explicit exact counterexample in 1.1; it fails for 123,130 of 208,584 (partition, ordering) pairs over 150 random instances. Fix: hemispace (Kakutani) leaves with convex complements as internal nodes (1.1). |
| Theorem 1.7(c) | correct with the same fix | For binary branching the internal nodes are in general not closed. |
| Theorem 1.8(a),(b) (cuts in `x`, feasibility reductions) | correct | (b)'s hypothesis `Q_v ∩ K ⊆ Q'_v` can be weakened to `Q̄_v ∩ F ⊆ Q'_v`, which also covers FBBT with integer rounding. |
| Theorem 1.8(c) (node form `N >= kappa/(2n+1)`, presolve form `L >= kappa - 2n`) | **correct with fixes** | The proof needs every removed piece certified relative to the *unreduced* `Q̄_v`. Sequential (Gauss–Seidel) tightening, which the author's own Part A check uses, certifies relative to partially reduced sets; a chain construction repairs this with the same count. `s_v <= 2n` holds only for one tightening pass per node; iterated propagation on general integers needs one piece per bound change. For binaries `s_v <= n`, so `N >= kappa/(n+1)`. The Part A test of the node form cannot fail in its 2-D setting. |
| Proposition 1.9, Remarks 1.10–1.11 | correct | — |
| Proposition 2.1(a),(b) | correct | — |
| Summary: "the class number of a compact linear program is therefore always polynomial" | **false for MILPs** | A compact MILP with `2n` rows has `kappa = 2^n` exactly (1.3). True for pure ILPs only. |
| Theorem 2.2(a)–(c) | correct | Proofs checked (separation, Lovász/BCCZ, lsc needed in (b), parity). |
| Theorem 2.3 (separation via Gläser–Pfetsch) | **correct with fixes** | Instance and model match (checked against the PDF). `psi(t) = t^2` is not "strictly increasing"; the correct hypothesis is weaker and `t^2` satisfies it. `L = Theta(n^2)` is Gläser–Pfetsch's claim; a dense encoding gives `L = n^{7/3 - o(1)}` and exponent `1/14`. The instances of (b) are unconstrained convex (`K = R^n`), so the Summary's "open in the pure-curvature case (unconstrained convex objective)" is wrong in scope: only the quadratic case is open. |
| Proposition 2.4 (quadratic Jeroslow) | correct, minor wording | "Exactly `C(n+1,h)`" also needs "no branching below a node whose bound is already `>= tau`". |
| Proposition 2.5 (fixed dimension) | correct | Recursion and count re-derived. Reis–Rothvoss's current abstract states flatness `O(n log^2(2n))`; the cited `log^3` is weaker but valid. |
| Section 2.6 | correct | — |
| Lemmas 3.1–3.3 (unfolding, Siegel moments, typical scales) | correct | Siegel is used only as a first moment over nonzero vectors; no Rogers formula is needed. |
| Theorem 3.4 (clique `>= 2^{(0.2075-o(1))n}`) | correct, minor | All algebra re-derived symbolically. The bound is vacuous for `delta > 0.0858`, but the statement allows `delta < 0.1`; the earlier review's range remark is only partly incorporated. |
| Theorem 3.5 (`kappa >= 2^{(0.2925-O(delta))n}/(2(n+1))`) | correct | Its counting mechanism is DDM's Section 6 argument (see Section 5 below). |
| Proposition 3.6(a)–(c) (`kappa <= 2^{n/2+o(n)}`, clique `<= 2^{0.2612n}`) | correct | KL formula, crossing `rho* = 1.436424` (angle 66.9°), covering lemma and cap-measure bound verified. Nit: `ceil(...)` should be `ceil(...) + 1` for a strict union bound. |
| Section 3.6(i): "no pairwise argument can exceed `2^{0.2612 n}`" | **overclaim** | Proposition 3.6(c) bounds only the midpoint clique number, not `chi(G^mid)`, `omega(G^seg)` or `chi(G^seg)`. |
| Section 3.6(iii), random `t`: cliques `e^{cn}` | unproved remark | Easy, but stated as fact without proof; a sketch is in 2.3. |
| Section 3.7 numerics | correctly reported, weak evidence | The "deterministic consequences" (`om43 >= N43 - M43`, at most 12 far points) cannot fail; zero violations test only the code. |
| Lemma 4.1, Lemma 4.2, Theorems 4.3–4.4 | correct | Re-verified in exact arithmetic with independent code, including the hull root value as an exact LP optimum. |
| Lemma 5.1, Proposition 5.2(a),(c) | correct | — |
| Proposition 5.2(b): `kappa <= 2n+1` | correct | — |
| Proposition 5.2(b): "simple variable branching attains it up to a factor of 2 in nodes" | **false** | Family with (C1), `kappa = 2`, and minimum variable-branching tree `n+1` leaves, `2n+1` nodes (exact, 1.4). |
| Section 7.3 (review corrections incorporated) | verified | All eight corrections of `bb-conflict-review.md` are handled, except that the `delta` range remark resurfaces in the new Theorem 3.4. |

## 1. Framework (Section 1)

### 1.1 Theorem 1.7(b): the caterpillar is not a valid tree

Definition 1.1 requires, for every internal node `v`, that
`Q_v ∩ P ⊆ Q_{w_1} ∪ … ∪ Q_{w_k}`. In the caterpillar the second child of the
root is `N_1 = conv(I_2 ∪ … ∪ I_kappa)`, and its children are `conv I_2` and
`conv(I_3 ∪ … ∪ I_kappa)`. If `N_1` contains a point `p ∈ I_1` that lies in
neither child, the covering condition fails at `N_1`. Nothing in the proof
prevents this, and it happens often.

**Exact counterexample** (`caterpillar_example.py`, rational arithmetic). Take
`phi(x) = ||Ax - y||^2` on `K = R^2` with `A = [[-2, 1], [3, 3]]`,
`y = (-3/5, 18/7)`, `P = {0..3} x {0..2}`, `OPT = 2626/1225`, `eps = 1/20`.
Then `kappa = 3`, and one minimum admissible partition is

- `I_1 = {(0,1), (0,2), (1,1), (1,2), (2,1), (3,1), (3,2)}` (min over the hull `39204/15925 >= tau`),
- `I_2 = {(0,0)}`,
- `I_3 = {(1,0), (2,0), (2,2), (3,0)}` (min over the hull `2626/1225`).

`conv(I_2 ∪ I_3)` contains `(1,1) ∈ I_1`, which lies neither in `conv I_2` nor in
`conv I_3`. So the caterpillar in this order is not a P-covering tree.

**How often** (`binary_realization.py`, exact, 150 random instances with
`kappa >= 3`; 141 have `kappa = 3`, 9 have `kappa = 4`): for every minimum
admissible partition (up to 3000 per instance) and every ordering of its
classes I tested the literal caterpillar. The covering condition fails for
123,130 of 208,584 (partition, ordering) pairs, in 142 of the 150 instances. In
no instance did every ordering of every minimum partition fail, so a good order
usually exists; but the proof takes an arbitrary minimum partition in an
arbitrary order, and no rule for choosing one is given.

**The claim itself is true.** Fix: let `E_tau = {x ∈ K : phi(x) < tau}` (convex).
For each class, `conv I_j` and `E_tau` are disjoint convex sets. By the Kakutani–Stone
lemma (two disjoint convex sets lie in complementary hemispaces, i.e. convex sets
whose complements are convex; in `R^n` these are lexicographic halfspaces) there is
a convex `G_j ⊇ conv I_j` with `G_j ∩ E_tau = ∅` whose complement is convex.
Use leaves `G_1, …, G_kappa` and internal nodes
`N_j = R^n \ (G_1 ∪ … ∪ G_j)`, `j = 0, …, kappa - 2`:

- `N_j` is convex, and `N_{j-1} ∩ P ⊆ G_j ∪ N_j` trivially;
- `N_{kappa-2} ∩ P ⊆ I_{kappa-1} ∪ I_kappa ⊆ G_{kappa-1} ∪ G_kappa`;
- every leaf lies in some `G_j`, on which `phi >= tau`.

This gives `kappa` leaves and `2 kappa - 1` nodes, for finite or infinite `P`.
When `E_tau` is open (for example `K = R^n`), closed halfspaces
`G_j = {g_j.(x - xh_j) >= 0}` suffice, with `xh_j` the minimizer of `phi` over
`conv I_j` and `g_j = grad phi(xh_j)`; then the internal nodes are open
polyhedra. For finite `P` one can replace every set by the convex hull of its
`P`-points and get closed polytopes. `binary_realization.py` checks the
halfspace version exactly on every instance (150 of 150 valid) and also
computes the exact minimum over binary trees with hull pieces, which equals
`kappa` in 150 of 150 instances. Where (E) holds on `Z^2` (147 instances),
`kappa <= 4`, as Theorem 2.2 predicts.

Theorem 1.7(c) ("pieces can be closed halfspaces" when `K = R^n`) holds for the
leaves; for binary branching the internal nodes are open, as above.

### 1.2 Theorem 1.8

**(a) and (b).** The proofs are correct. In (b), the hypothesis
`Q_v ∩ K ⊆ Q'_v` excludes FBBT with integer rounding (rounding removes points of
`K`), although the note lists FBBT as an example. The proof only needs
`Q̄_v ∩ F ⊆ Q'_v`, which rounded FBBT satisfies, so state that.

**(c): what the proof covers.** The construction of `T'` attaches the removed
pieces `Q̄_v ∩ D_{v,i}` as leaf children of `v` and needs
`r(Q̄_v ∩ D_{v,i}) >= tau` relative to the *unreduced* effective set. Three
points need stating.

1. *Sequential tightening.* Solvers (and the author's own
   `check_framework_small.py`, Part A, whose OBBT updates variable 1 before
   testing variable 2) certify the piece for variable `i` relative to the box
   already reduced in earlier variables. That piece is certified on
   `Q^{(i-1)}_v ∩ D_i`, not on `Q̄_v ∩ D_i`, which also contains points removed
   earlier and fractional points between them. The repair is a chain: node
   `Q̄_v`, children `Q̄_v ∩ D_1` (leaf) and `Q^{(1)}_v`, whose children are
   `Q^{(1)}_v ∩ D_2` and `Q^{(2)}_v`, and so on. The leaf count is unchanged, so
   the conclusion survives, but the stated hypothesis does not cover the
   operation that was tested.
2. *Several passes.* `s_v <= 2n` assumes each bound of each variable changes at
   most once per node. Iterated propagation or OBBT on general integers can move
   the same bound several times, and consecutive pieces cannot be merged into
   one certified piece in general, because the merged set may contain fractional
   points with low `phi`. The correct count is one piece per bound change:
   `kappa <= L + (number of bound changes)`. So `N >= kappa/(2n+1)` and
   `L >= kappa - 2n` are proved only for one pass per node (or root). I did not
   find a counterexample to the stated inequalities for iterated passes.
3. *Binaries.* A binary variable changes a bound at most once per node, so
   `s_v <= n` and `N >= kappa/(n+1)`. Theorem 4.3(b) can use `2^k/(2k+1)`.

The Part A test of `kappa <= (2n+1)N` is vacuous: on `[0,2]^2` with the natural
relaxation, (E) holds and `C_tau` is bounded, so `kappa <= 2^2 = 4 < 5 <= 5N`
(Theorem 2.2(b)). Only `kappa <= L + S` is a real test there.

Proposition 1.9 and Remark 1.10 (including empty enumeration intervals, which
get two out-of-range pieces) are correct.

### 1.3 Proposition 2.1 and the Summary sentence on compact programs

Proposition 2.1 is correct. The Summary's "The class number of a compact linear
program is therefore always polynomial" follows the MILP bound and is false for
MILPs. Counterexample (`c1_and_compact_milp.py`, Part 2): the compact MILP

```
min sum_i s_i  s.t.  s_i >= x_i - 1/2,  s_i >= 1/2 - x_i  (2n rows),  x in Z^n, s in R^n
```

has projected relaxation `phi(x) = ||x - (1/2) 1||_1` on `K = R^n` and
`OPT = n/2`. For `eps < 1/2` all `2^n` points of `{0,1}^n` pairwise conflict
(midpoint value `(n-d)/2`). The `2^n` halfspaces
`{sum_i sigma_i (x_i - 1/2) >= n/2}` cover `Z^n` with `phi >= OPT`. So
`kappa = 2^n` exactly with `2n` rows. This is the `l1` twin of Section 3.6(iii)
and the Dadush–Tiwari extended-formulation phenomenon that Gläser–Pfetsch
mention. Proposition 2.1(b) is consistent with it: the projected sublevel set is
a cross-polytope with `2^n` facets. The sentence should say "compact pure
integer linear program", and the Section 2 opening ("for linear problems the
class number is always small") should say the same.

### 1.4 Proposition 5.2(b): "up to a factor of 2"

Under (C1), both the variable-branching tree (at most `2D+1` nodes) and `kappa`
(at most `2n+1`) are `O(n)`, but the tree is not within a factor 2 of `kappa`.
Family (`c1_and_compact_milp.py`, Part 1, exact): `phi(z) = sum_i (z_i - a)^2`,
`a = 1/(2n)`, `K = [0,1]^n`, `eps = 1/(8n^2)`.

- `OPT = 1/(4n)` at `z = 0` only. (C1) holds: each wrong fixing has bound
  `(1-a)^2 >= OPT`.
- `kappa = 2`: the classes are `{0}` and `{0,1}^n ∩ {1.z >= 1}`. The minimum of
  `phi` over `K ∩ {1.z >= 1}` is at `z = (1/n) 1` (KKT verified exactly), with
  value `1/(4n) = OPT`. The root bound is 0, so `kappa >= 2`.
- Every variable-branching certificate has at least `n+1` leaves and `2n+1`
  nodes (exact DP for `n = 2..10`; the path to `0` must fix all `n` variables).

So `nodes/kappa = (2n+1)/2`. Replace the sentence by "under (C1) both the
variable-branching tree and `kappa` are at most `2n+1`".

### 1.5 Other framework items

- Proposition 2.4 is correct, and `check_framework_small.py` Part C agrees with
  `C(n+1,h)`. "Exactly `C(n+1,h)` leaves" also needs "and no branching at a node
  whose bound is already `>= tau`" (a certificate may branch below a prunable
  node). The count uses only the node-bound pattern, so it holds equally for the
  linear Jeroslow instance; the quadratic objective adds `kappa = 2` for the
  optimization version.
- Proposition 2.5: the recursion, the extension of the primitive dual vector to
  `pi ∈ Z^n` (saturated sublattice), the nonempty slices, and the count
  `1 + S(j) <= (q+4)(1 + S(j-1))` are right. Lower-dimensional `C_tau ∩ A` is
  covered by thickening. Current Reis–Rothvoss abstract (arXiv 2303.14605 v5):
  flatness `O(n log^2(2n))`. Their subspace-flatness algorithm runs in
  `(log n)^{O(n)}`; whether it yields split trees of that size is unchecked
  and would sharpen both Proposition 2.5 and the remark in Open problem 2.6.

## 2. Class number versus split trees, and random CVP

### 2.1 Theorem 2.3: match with Gläser–Pfetsch

I read system (2) in the PDF (the markdown omits it): rows (2a)–(2d) with
integral coefficients, and (2e) `x, y, z ∈ [0,1]` as box rows. All variables are
binary, and `n = r(k-1) + r + C(r,2) = Theta(r^2)`. A "branch-and-bound tree
for (2)" is a binary tree of integer split disjunctions whose leaves have an
LP-infeasible system; internal nodes may be infeasible. That is exactly a
`Z^n`-covering split `(+inf)`-certificate in the note's model. Theorem 5 and
Corollary 6 bound the number of leaves. So (a) is a correct corollary.

For (b) I checked `t* >= 1` on a small instance (`r = 4`, `k = 3`, `n = 18`,
all `2^18` binary points: `t* = 1`), that `P_r` is nonempty (exact point), and
the leaf argument (`gp_system.py`). Fixes:

- **`psi(t) = t^2` is not strictly increasing on `R`.** The argument needs only
  `inf_{t >= t*} psi(t) - inf_{t >= 0} psi(t) > eps`, which holds for any convex
  `psi` strictly increasing on `[0, ∞)`, including `t^2` with `eps < 1`. The
  projected relaxation is `max(0, M(w))^2`, equal to `0 = psi(0)` on `P_r`.
  State the hypothesis this way.
- **Encoding length.** Gläser–Pfetsch write `L ∈ Theta(n^2)`. With `m/n ~ k`
  growing, a dense encoding has `L = Theta(n^2 k) = n^{7/3 - o(1)}`, and a
  sparse one `L = n^{4/3 - o(1)}` (`gp_system.py`, Part 1). The exponent
  `1/12` is therefore convention-dependent (`1/14` dense, `1/8` sparse). The
  separation `2^{L^{Omega(1)}}` versus `kappa <= m <= L` is unaffected. Say
  "`2^{n^{1/6 - o(1)}}` with `n` the number of variables" or "`2^{L^{Omega(1)}}`".
- **Scope of the open problem.** In (b), `K = R^n` and `phi(w) = max_j(a_j.w - b_j)`
  is a finite convex function (or `max(0, ·)^2` of it). These instances belong to
  the unconstrained class of Theorem 2.2(a). The Summary calls that class "the
  pure-curvature case (unconstrained convex objective)" and says split trees
  versus `kappa` are open there. Theorem 2.3(b) already answers that negatively.
  Only the quadratic case (ellipsoidal sublevel sets), as stated in Open
  problem 2.6 and Section 8, remains open. The Summary ("pure-curvature case",
  twice) should say "convex quadratic".
- (c) is fine: with `k = c log n'` clauses of width `k`, `m = O(n' 2^k)` is
  polynomial.

### 2.2 Theorem 2.2

Correct. (a): halfspaces from classes by separating the open set `E_tau` from
`conv I_j`; `int(cl O) = O` for a nonempty open polyhedron; `2^n` from Lovász's
theorem (maximal lattice-free sets are polyhedra with at most `2^n` facets; the
parity argument) plus existence of a maximal lattice-free superset (BCCZ).
(b) needs `phi` lsc, which is stated. (c) is the parity argument.

### 2.3 Random CVP (Section 3)

I re-derived every step.

- **Lemma 3.1–3.2.** Unfolding over the torus and Siegel's first moment over
  nonzero vectors, applied to `f(a) = vol(A ∩ (A-a))` (bounded, compact
  support), give `E N^2 = V + V^2` and `E M_A(s)`. No Rogers higher moment is
  used. Correct.
- **Lemma 3.3.** (a) is a first moment over `t` for each lattice; (b) halves by
  `±v`; (c) Chebyshev. Correct.
- **Theorem 3.4.** Checked symbolically (`cvp_constants.py`): the averaging
  identity; `theta = (2-rho)/rho`; `A - bR^2 = 4(rho-1) r_0^2/rho`; and
  `(1-1/n)a^2 - bR^2 = 2 r_0^2 (rho-1)(n rho - 2)/(n rho)`, so monotonicity
  holds iff `rho >= 2/n`. The deletion and probability steps are right.
  The author's `check_cvp_integrals.log` (read, not rerun) shows the bound is
  exponentially tight, and my hand computation of the exact rate agrees, so `4/3` is the limit
  of this method. The bound is non-vacuous only for
  `delta < 0.0858` (need `(4/3)((1-delta)^2 - delta) > 1`); the statement's
  `delta < 0.1` should be tightened, as the earlier review asked for the old
  theorem.
- **Theorem 3.5.** Correct: separation of `conv(BI - t)` from the open ball
  gives the cap; caps lie in balls of radius `a` with `a^2 <= lambda_1^2/2`;
  lattice points there have pairwise negative inner products about the center
  (strict, because the ball is open), hence at most `n+1`; if the center is a
  lattice point it is alone. Non-vacuous for `delta < 0.1315`.
- **Proposition 3.6(b).** The near/far split, the cap angle `pi/4`, and the
  covering lemma are correct. I checked the cap-measure bound
  `sigma(phi) >= sin^{n-2}(phi - 1/n)/(pi n)` against the exact incomplete-beta
  value for `n = 4..400` (ratio at least 7), and `M = Theta(n^2 log n 2^{n/2})`
  (ratio to `n^2 log n 2^{n/2}` about 23 for large `n`). Nit: with
  `M = ceil(log|Y|/sigma)` the union bound gives failure probability `<= 1`,
  not `< 1`; use `+1`.
- **Proposition 3.6(c).** The three-part split, the bound
  `<û,ŵ> < 2/sqrt(ab) - 1`, the constant 12, and the KL application are
  correct. The KL formula used is valid for `0 < theta < pi/2`, and
  `theta* = 66.9°` lies there. My implementation gives `rho* = 1.436424`,
  `e_+ = 0.261241`, `R_KL(60°) = 0.40141`, and Remark 3.5a's `0.29746`.
- **Section 3.6(i) overclaims.** "Proposition 3.6(c) confirms that no pairwise
  argument can exceed `2^{0.2612n}`" is not what 3.6(c) proves: it bounds
  `omega(G^mid)`. The chromatic number `chi(G^mid)` (also a pairwise quantity,
  also `<= kappa`), and the segment graph (whose conflict threshold on
  `<û,ŵ>` is weaker for unequal norms) are not bounded. Say "no midpoint-clique
  argument".
- **Section 3.6(iii), random `t`.** The claim of cliques `e^{cn}` has no proof.
  Sketch: coordinates with `|t_i - 1/2| < eta` number about `2 eta n`; among
  them take a constant-weight code of weight `w` and distance `d` (GV); flipping
  a set `S` costs at most `2 eta |S|`, and a midpoint over a difference set `D`
  saves at least `|D|(1/4 - eta)` (from `(1/2 - eta)^2` down to at most
  `eta^2` per coordinate); so two codewords conflict when
  `d(1/4 - eta) > 2 eta w + eps`. With `w = m/2` this asks for relative
  distance above `4 eta/(1 - 4 eta)` (plus `O(eps/m)`), and such constant-weight
  codes have positive rate for small `eta`. It should be labeled a remark
  with this sketch.

### 2.4 Section 3.7 numerics

The scripts compute what the table reports, and the Haar-like scales
(`OPT/GH^2`, `lambda_1^2/GH^2` near 1) are informative. Two caveats:

- `om43 >= N43 - M43` holds for every graph (deleting one endpoint of each
  non-edge leaves a clique), and "at most 12 members with `phi >= 2.2 OPT`" is a
  theorem. Zero violations therefore test only the code, not the theorems.
- For `n >= 24` points are enumerated only up to `1.55 OPT`, while `Nc` counts
  points with `phi < OPT + lambda_1^2/2`; when `lambda_1^2 > 1.1 OPT`, `Nc` is
  truncated. This makes the reported class bound conservative, not wrong.

## 3. Section 4 (perspective gadget) and Section 5

`perspective_exact.py` (exact, independent code):

- Lemma 4.1: Woodbury form equals the direct support-wise minimization
  **exactly** on 30 random rational nodes with zero entries.
- Lemma 4.2: all closed forms (`g00`, `g10 = g01`, `g11`, `ĝ`, `delta`, and the
  condition-(i) difference `s^2 c(1+c)/((1+lam)(1+lam+c))`) hold exactly at 48
  rational parameter sets; sympy via the adjugate gives zero residuals.
- Theorem 4.3 (symmetric instance, `k = 2, 3, 4`): `OPT = k g10`, exactly `2^k`
  optimal supports, all midpoints `OPT - |D| delta`; the hull root value,
  computed as the exact LP optimum (maximum of the concave Lagrangian dual over
  all breakpoints), equals `OPT`. Full `2k x 2k` inverses agree with the
  separable formula on all `z ∈ {0, 1/2, 1}^{2k}` for `k <= 3`.
- Theorem 4.4 (asymmetric data): (H1) and (H2) hold; the admissible `eps` bound
  is `0.13203, 0.12752, 0.09616, 0.08953` for `k = 2, 3, 4, 6`; unique optimum
  (`k <= 4`, exhaustive); all one-per-block pairs conflict; hull LP value equals
  `OPT`.

The proofs of 4.3 and 4.4 are correct. The node form in 4.3(b) can use
`2k + 1` (binaries).

Section 5: Lemma 5.1 and Proposition 5.2(a),(c) are correct; the incumbent
hypothesis is explicit. For 5.2(b) see 1.4.

## 4. Incorporation of `bb-conflict-review.md`

Checked item by item against its Section 9. Handled: node form and 1-D
counterexample (1.8(c), 1.9); infeasible-endpoint conflicts, finite trees,
covering `F` (Definitions 1.1, 1.4, Theorem 1.6); segment graph; cuts in `x`
(1.8(a)); sphere decoders `kappa/3` (Remark 1.10) and the tightening form;
strict conflicts (open balls); separate reporting of Gaussian bases; closed
form of `delta` and `cos th > 0`; symmetry caveat (Theorem 4.4); incumbent in
Lemma 5.1; `inf` for `min`. The old Corollary 2 (HBO ball) is dropped rather
than corrected, which is acceptable. The `delta` range remark resurfaces for
the new Theorem 3.4 (2.3 above).

## 5. Novelty

Web search was not available; the arXiv export API returned HTTP 429. I used
arXiv search pages through WebFetch and the local library.

- **Sources examined.** DDM full text, Sections 4–6 (the note read Sections
  1–2, 4, 5 only); Kaibel–Weltge Definition 1 and Proposition 7;
  Gläser–Pfetsch (PDF, including system (2) and the bibliography; [15] is
  "On computing small variable disjunction branch-and-bound trees", Math.
  Prog. 2023); Reis–Rothvoss abstract (arXiv 2303.14605 v5). arXiv searches:
  "branch-and-bound lower bound tree size convex" (1 irrelevant hit),
  "integer least squares branch and bound lower bound" (1 irrelevant hit),
  "relaxation complexity" (13 hits: Kaibel–Weltge; Averkov–Schymura;
  Averkov–Hojny–Schymura 2105.12509 and 2203.05224; Aprile–Averkov–Di Summa–Hojny
  2206.12253; Averkov–Keil–Weltge 2606.11852; none mentions B&B trees),
  "relaxation complexity lattice-free" (Averkov–Basu–Paat 1705.02015 only),
  `"general disjunctions" lower bound` (DDM and Gläser–Pfetsch only).
- **Missed prior mechanism (should be credited).** DDM Section 6 (perturbed
  cross-polytope, Lemma 12 and the proof of their Theorem 2) bounds the number
  of `0/1` points any leaf can contain (Sauer–Shelah: more than
  `sum_{i<s} C(n,i)` points force a hull point with `s` half-coordinates inside
  the polytope) and divides. That is exactly the non-pairwise counting bound of
  Lemma 1.5(b) and the mechanism of Theorem 3.5. So "the hypergraph refinement"
  as a lower-bound technique is in DDM; what is new is its use with objective
  curvature and the cap/obtuse-set estimate on random lattices.
- **Relation to relaxation complexity.** For `phi ≡ 0` on a polytope `K` and
  `tau = +inf`, a family of classes covering `Z^n` with hulls missing `K` is,
  up to separation, the complement-halfspace family of a polyhedron containing
  `K` with no integer points. So `kappa_{+inf}` is a relative relaxation
  complexity in the sense of Kaibel–Weltge and Averkov–Hojny–Schymura, and
  Theorem 2.2 is its sublevel-set analogue. The note says "close in spirit"; it
  is closer than that. Rate Theorem 2.2 low to moderate: it is separation plus
  Lovász's facet bound.
- **Other items.** The ratings in 7.2 are otherwise reasonable. Theorem 1.7 is
  immediate once `kappa` is defined (and the binary version needs the fix).
  Proposition 2.1/Theorem 2.3 are elementary corollaries of Gläser–Pfetsch's
  own remark. Proposition 2.4 is Jeroslow's instance; the lattice-path count is
  standard and I did not check whether the exact count is in the literature.
  The random-CVP results remain the most novel part: I found no
  branching-independent node lower bound for CVP or integer least squares.
  Section 4 is a gadget; Section 5 is folklore.

An unsuccessful bounded search does not establish novelty.

## 6. Checks run (targeted, local; not CI)

All from `research-20260928b/reviews/integer-core/`, Python 3.13.11, SymPy
1.14, mpmath 1.3, SciPy 1.18, NumPy 2.5.1. No project-wide checks were run and
CI was not inspected. The author's scripts were read but not rerun.

| Command | Establishes | Result |
|---|---|---|
| `python3 binary_realization.py 150 20260929` (`.log`) | Theorem 1.7(b): caterpillar validity for all minimum partitions and orderings; exact binary minimum with hull pieces; reviewer's halfspace tree; `kappa <= 4` under (E) | covering fails in 123,130 of 208,584 pairs (142 of 150 instances; never for all orderings); `f_bin = kappa` and the halfspace tree valid in 150 of 150; `kappa <= 4` in all 147 instances with (E) |
| `python3 caterpillar_example.py 1` (`.log`) | explicit exact caterpillar failure and the halfspace repair | as in 1.1 |
| `python3 c1_and_compact_milp.py` (`.log`) | Proposition 5.2(b) counterexample (`n = 2..10`); compact MILP with `kappa = 2^n` (`n <= 10`, cover check `n <= 5`) | as in 1.3–1.4 |
| `python3 gp_system.py` (`.log`) | encoding sizes of GP system (2); `t* = 1`, `P_r ≠ ∅`, `t^2` leaf argument for `r = 4, k = 3` | dense exponent 2.14–2.28 (→ 7/3), sparse 1.20–1.30 (→ 4/3); `t* = 1` |
| `python3 perspective_exact.py` (`.log`) | Section 4, exact | all checks pass |
| `python3 cvp_constants.py` (`.log`) | Section 3 algebra, exponents, KL crossing, covering lemma, `delta` ranges | as in 2.3 |

## 7. What remains unchecked

- The Gläser–Pfetsch theorems themselves (interpolation, Pudlák's circuit bound)
  and Lovász/BCCZ, flatness constants, Kabatiansky–Levenshtein, Siegel, and
  Goldstein–Mayer equidistribution: used as cited.
- Whether iterated bound propagation can actually violate
  `N >= kappa/(2n+1)` (only the proof gap is shown).
- Remark 3.5a beyond recomputing its number (the lifting argument is plausible;
  I did not write it out).
- The author's lattice numerics (`check_cvp_bounds.py`) were read, not rerun.
- The exact minimum variable-branching trees for the perspective gadget
  (`2^{k+1} - 2`), cited from the earlier review.
- Whether Reis–Rothvoss subspace branching converts to `(log n)^{O(n)}` split
  trees.
- A full literature sweep: lattice-enumeration lower bounds (Hanrot–Stehlé,
  Aono et al.) and proof-complexity work beyond the sources above.
