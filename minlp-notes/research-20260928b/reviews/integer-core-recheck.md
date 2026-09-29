# Recheck of the revised integer-core note

Target: [`bb-complexity/integer-core/relaxation-intrinsic-bounds.md`](../bb-complexity/integer-core/relaxation-intrinsic-bounds.md)
(the "note"), as revised after [`integer-core-review.md`](integer-core-review.md). Section 9 of
the note lists the changes.

Date: 2026-09-29. I had not seen this material before. I did not edit the note and did not
commit. I read the author's `check_revision.py` and its log but did not run or reuse that
code. All checks below come from new scripts in
[`integer-core-recheck/`](integer-core-recheck/). They use exact rational arithmetic (Python
`Fraction`, SymPy), except for one floating-point self-test of the exact tools.

## Verdict

All six revisions are correct. No revised statement is false, and every revised proof holds
when checked step by step. What remains is minor: an off-by-one in a node count, two wording
points, and a mismatch between the author's R4(b) check and its description. See
"Remaining problems".

| Item | Verdict | Main evidence |
|---|---|---|
| (1) Lemma 1.7a and Theorem 1.7(b),(c) (hemispace chain) | **Correct** | The induction proof of the lemma holds. The covering condition holds at every internal node: at the first `κ − 2` nodes because `N_{j−1} ⊆ G_j ∪ N_j`, and at the last one because `P \ (G_1 ∪ … ∪ G_{κ−2}) ⊆ I_{κ−1} ∪ I_κ`. Exact tests: 5,613 (partition, ordering) pairs with gradient halfspaces and 2,880 chains with non-smooth `φ` (`ℓ_1`) are all valid. On 1,653 of these pairs the old caterpillar fails 485 times. A non-open `E` where no halfspace works was handled by genuine Lemma 1.7a hemispaces: 360 of 360 chains valid. |
| (2) Example 2.1a (`2n` rows, `κ = 2^n`) | **Correct** | Projection, `OPT = n/2`, the `2^n`-clique and the halfspace cover are verified exactly. Exact `κ` on the window `{−1,0,1,2}^2` is 4 for `ε ∈ {0, 1/4, 49/100}` and drops to 2 at `ε = 1/2`, so the range `ε < 1/2` is sharp. |
| (3) Proposition 5.2(b) family | **Correct** | (C1), `κ = 2` (by KKT, and by exact subset DP for `n ≤ 4`), and a minimum variable-branching tree of exactly `n + 1` leaves and `2n + 1` nodes (exact DP for `n = 2..12`; full DP over all branching orders for `n ≤ 6`). |
| (4) Theorem 1.8(c) (sequential pieces; one piece per bound change; `N ≥ κ/(2n+1)` for one pass; `N ≥ κ/(n+1)` for binaries with iterated passes) | **Correct** | Chain proof and binary count re-derived, including emptied nodes. Exact tests (1,420 runs) build the tree `T'` of the proof and check Definition 1.1 on it directly: all valid, 0 violations, and `κ = L + S` is attained. An explicit exact instance has 5 > `2n` bound changes at one node, with one bound moving twice. |
| (5) Theorem 2.3(b) with `ψ` convex and strictly increasing on `[0, ∞)` | **Correct** | Proof checked. Exact toy systems with `t* = 1` behave as claimed for `ψ ∈ {t, t², |t|, t² + 2t, max(−t/2, 3t)}`. The `ε` range is sharp there, and a `ψ` that violates the hypothesis breaks the reduction. |
| (6) `δ` thresholds `0.0858` and `0.1315` | **Correct** | `(3 − √8)/2 = 0.0857864…` and `(4 − √13)/3 = 0.1314829…` are exact roots (SymPy). The stated ranges `(0, 0.08)` and `(0, 0.1)` lie inside the non-vacuous ranges. The Theorem 3.4 algebra (θ, `a²`, monotonicity iff `ρ ≥ 2/n`) was re-derived symbolically. |

## 1. Lemma 1.7a and Theorem 1.7

### Proof check

**Lemma 1.7a.** The proof holds in every step.

- If `A = ∅` or `B = ∅`, the lemma is trivial. This covers `d = 0`, where one of two
  disjoint subsets of a point is empty.
- Separation needs only finite dimension. `0 ∉ A − B` implies `0 ∉ ri(A − B)`, so
  `{0}` and `A − B` can be properly separated (Rockafellar, Thm. 11.3). This gives a
  functional with nonzero linear part, and `H` has dimension `d − 1`.
- `G = {g > α} ∪ G'` is convex. A strict combination of two points of `G` either has a
  point with `g > α`, which keeps the combination in `{g > α}`, or has both points in `G'`.
- The complement `{g < α} ∪ (H \ G')` is convex by the same argument.
- `A ⊆ G` and `B ∩ G = ∅` follow as written.

**Theorem 1.7(b).**

- `E = {φ < τ}` is convex, and `conv I_j ∩ E = ∅` is exactly `r(conv I_j) ≥ τ`.
- `N_j = ∩_{i ≤ j} (R^n \ G_i)` is convex.
- Covering at `N_{j−1}` (`j ≤ κ − 2`) is automatic, because `N_j = N_{j−1} \ G_j`
  gives `N_{j−1} ⊆ G_j ∪ N_j`.
- Covering at the last internal node `N_{κ−2}` is the only nontrivial case:
  `N_{κ−2} ∩ P = P \ (G_1 ∪ … ∪ G_{κ−2}) ⊆ I_{κ−1} ∪ I_κ ⊆ G_{κ−1} ∪ G_κ`, because
  `I_j ⊆ G_j`.
- Leaf bounds hold because each leaf lies in some `G_j` and `G_j ∩ E = ∅`.
- The proof works for any minimum partition and any ordering of its classes. The old
  caterpillar did not.

**Theorem 1.7(c).**

- (i) For convex `S`, `conv(S ∩ P) ⊆ S` and `conv(S ∩ P) ∩ P = S ∩ P`. Covering
  therefore transfers, and leaf effective sets only shrink. Correct.
- (ii) An open convex `E` and a disjoint convex set are separated by `g` with `g < α` on
  `E` and `g ≥ α` on `conv I_j`. So `G_j` is a closed halfspace, and each `N_j` is an
  intersection of open halfspaces. Correct.
- (iii) The first-order optimality condition gives `conv I_j ⊆ G_j`. The gradient
  inequality then gives `φ ≥ φ(x̂_j) ≥ τ` on `G_j`. This holds wherever `φ` is convex and
  differentiable at `x̂_j`, and it also covers points outside `K`, where `φ = +∞`.
  Correct.

### Exact tests (`t17_hemispace.py`, log `t17_hemispace.log`)

- **Part A.** On the first review's counterexample, exact `κ = 3`, and
  `(1,1) ∈ conv(I_2 ∪ I_3)` lies in neither child. The caterpillar is invalid for 2 of
  the 6 orderings. The halfspace chain and its polytope version (c)(i) are valid for all 6.
- **Part B.** 60 random 2-D and 40 random 3-D instances, with `φ = ||Ax − y||²` and
  `|P| = 12`.
  - Exact `κ` ranged over 1–4 (2-D) and 2–4 (3-D).
  - Tested all minimum partitions (capped at 30 in 2-D and 12 in 3-D) and all orderings
    (capped at 24 in 2-D and 6 in 3-D).
  - For each, the gradient halfspaces satisfied `I_j ⊆ G_j` and exact
    `min_{G_j} φ ≥ τ`, and the covering condition held at every internal node for every
    `P`-point: 4,151 of 4,151 (2-D) and 1,462 of 1,462 (3-D).
  - The polytope version (c)(i), checked with exact point-in-hull tests and exact hull
    minima, was valid in 1,370 of 1,370 and 283 of 283 cases.
  - On the same pairs the old caterpillar was invalid in 458 of 1,370 and 27 of 283.
- **Part C: non-open `E`, where a genuine hemispace is needed.**
  - Setup: `Q = [0,1] × [−1,1]`. Put `φ = −1` on `int Q`,
    `φ(0, s) = (s+1)(s+1/2)` on the left edge, and `φ = +∞` elsewhere. This `φ` is
    convex but not lsc.
  - With `τ = 0`: `E = int Q ∪ ({0} × (−1, −1/2))`, `P = {−1,0,1}²`, and exact `κ = 3`.
  - Every minimum partition has a class containing `(0,0)` and `(0,1)`. No closed
    halfspace can serve as its leaf. It would have to support `Q` at `(0,0)`, so it
    would be `{x_1 ≤ 0}`, which contains `(0, −3/4) ∈ E`. No open halfspace works either.
  - The recursion of Lemma 1.7a gives, for example,
    `G = {x_1 < 0} ∪ {x_1 = 0, x_2 > −1/2}`.
  - All 180 constructed hemispaces passed exact tests: `I ⊆ G`, `G ∩ E = ∅`, and
    randomized convexity of `G` and of its complement. 78 of them are not halfspaces.
  - All 360 chains (partition × separator choice × ordering) and all 60 polytope
    versions are valid.
  - So hemispaces are genuinely needed in the generality of Theorem 1.7(b), and the
    lemma supplies them.
- **Part D: open but non-smooth `E`.**
  - Setup: `φ = ||x − (1/2)1||_1` on `R²` (Example 2.1a, `n = 2`), with
    `P = {−1,0,1,2}²` and exact `κ = 4`.
  - Closed separating halfspaces were found for every class of 60 minimum partitions.
  - All 2,880 chains are valid. This tests (c)(ii) without gradients.

## 2. Example 2.1a (`ex21a_compact_milp.py`, log `.log`)

The proof is correct.

- **Projection.** `min Σ s_i` over the `2n` rows equals `||x − 1/2||_1`. This was checked
  with matching primal and dual values on 300 random rational `x`.
- **`OPT = n/2`.** Checked exactly over `{−2..3}^n` for `n ≤ 4`.
- **Midpoints and conflicts.** The midpoint value is `(n − d)/2` (all pairs, `n ≤ 8`).
  All `2^n` points pairwise conflict for `ε ∈ {0, 1/4, 49/100}`, `n ≤ 10`.
- **Covering and bounds.** The `2^n` halfspaces cover `{−2..3}^n` (`n ≤ 4`), with
  `φ ≥ σ·(x − 1/2)` pointwise and `min_{H_σ} φ = n/2`.
- **Exact `κ` on a window.** With `P = {−1,0,1,2}²` (subset DP), `κ = 4` for
  `ε < 1/2` and `κ = 2` at `ε = 1/2`, so the stated range is sharp.
- **Proposition 2.1(b).** `Λ_τ` has `2^n` facet inequalities (`n ≤ 4`).

## 3. Proposition 5.2(b) (`prop52b_family.py`, log `.log`)

The family and its proof are correct.

- **Optimum and (C1).** `OPT = 1/(4n)` is attained uniquely at 0 (`n ≤ 10`). (C1) holds
  because `(1 − a)² ≥ τ`.
- **Class `{1·z ≥ 1}`.** Its minimum over `[0,1]^n ∩ {1·z ≥ 1}` is `1/(4n) = OPT`,
  attained at `(1/n)1`. Exact KKT holds there, with multiplier `2(1/n − a) > 0`.
- **Root.** `a1 ∈ conv P` has `φ = 0 < τ`, so `κ = 2`. Exact subset DP over all
  partitions of `{0,1}^n` confirms `κ = 2` for `n = 2, 3, 4`.
- **Minimum trees.** A node fixing only zeros is prunable iff all `n` variables are
  fixed. The exact minimum variable-branching tree has `n + 1` leaves and `2n + 1` nodes
  for `n = 2..12` (DP by counts). A full DP over all branching orders gives the same
  result for `n ≤ 6`.
- **Ratio.** `nodes/κ = (2n+1)/2`, matching "a factor of about `n`".
- **Split trees.** The split tree `{1·z ≤ 0} ∨ {1·z ≥ 1}` has 3 nodes. So the gap is
  specific to variable branching, which the note does not claim otherwise.

## 4. Theorem 1.8(c)

### Proof check

**Chain construction.**

- At chain node `Q^(i−1)`, the hypothesis `Q^(i−1) ∩ P ⊆ Q^(i) ∪ D_{v,i}`, intersected
  with `Q^(i−1)`, gives covering by the two children `Q^(i−1) ∩ D_{v,i}` and `Q^(i)`.
- The `D`-leaves are certified, run leaves are pruned on `Q'_v`, and Theorem 1.6 gives
  `κ ≤ L + Σ s_v`.
- The simultaneous variant (multiway node) is also right.
- Nesting of the run's sets is not even needed, because effective sets are
  intersections along the path.

**One pass.** `s_v ≤ 2n`, so `κ ≤ L + 2nN ≤ (2n+1)N`. Correct.

**Binaries with iterated passes.**

- A free binary variable can change a bound once. A second change on the same variable
  empties the node.
- If the final set has no `P`-points, the last chain node keeps only its `D`-child.
  Covering still holds, because `Q^(s−1) ∩ P ⊆ D_s`.
- An emptied run leaf therefore contributes at most `n + 1` leaves of `T'`. Any other
  node contributes at most `n` pieces, plus 1 if it is a run leaf.
- Hence `κ ≤ L + nN ≤ (n+1)N`. Correct.

**OBBT, reduced-cost fixing and binary probing** satisfy the hypothesis as stated.

### Exact tests (`thm18c_counting.py`, log `.log`)

**Model.**

- `φ = ||Ax − y||²` on the box (natural relaxation), with `P` the box points and
  `UB = OPT`.
- All node bounds are exact box minima, and `κ` is exact.
- Each reduction is certified on the current box, and each bound change counts as one
  piece. A change may cover several units: `c` is the largest value with
  `r(box ∩ {x_i ≤ c}) ≥ τ`, which removes at least as much as the ceil rule of OBBT.
- For every instance I computed, over all variable-branching trees, the minimum `N` and
  the minimum `L + S`.
- For the min-`N` run I built `T'` and verified Definition 1.1 on it directly: covering
  at every chain node and every branching node for all `P`-points, exact leaf bounds, and
  a leaf count equal to `L + S` (minus dropped leaves of emptied nodes).

**Results.** All `T'` are valid, and there are 0 violations of `κ ≤ L + S` and of the
claimed node forms.

| Setting | Runs | `κ` range | max `κ/N` | Notes |
|---|---|---|---|---|
| binaries `n = 3`, one pass / iterated | 200 + 200 | 2–4 | 4 = `n + 1` | binary node bound attained |
| binaries `n = 3`, iterated, probing continued on prunable boxes | 200 | 2–5 | 4 | 210 emptied nodes; at most `n + 1 = 4` pieces at an emptied node |
| binaries `n = 4`, iterated | 20 | 2–5 | 4 | |
| integers `n = 2` on `[0,2]×[0,3]`, one pass / iterated | 200 + 200 | 2–4 | 3 / 4 | up to 5 > `2n` changes at one node when iterated |
| integers `n = 3` on `[0,1]²×[0,2]`, one pass / iterated | 200 + 200 | 2–4 | 4 | |

The minimum slack of `L + S − κ` is 0, so the counting form is attained.

**Iterated passes exceed `2n` changes** (`thm18c_iterated_example.py`, log `.log`).

- Instance: `A = [[−3, −3], [2, 1]]`, `y = (−159/20, 29/8)`, `ε = 0`, root box
  `[0,2] × [0,3]`.
- Iterated tightening makes 5 certified bound changes at the root, and the lower bound of
  `x_2` moves twice (0 → 1 → 2). One pass makes only 2.
- The root reduces to the point `(1,2)` and is pruned: `N = 1`, `L = 1`, `S = 5`,
  `κ = 3`.
- This illustrates the note's point that `s_v` is not bounded by `2n` for iterated passes.

**Open problem 6** (not a claim of the note; `openprob6_search.py`, log `.log`).

- A counterexample to `N ≥ κ/(2n+1)` under iterated passes needs `n ≥ 3`. In 2-D,
  `κ ≤ 4 < 5`.
- I searched 1,500 random exact instances on `[0,2]³` for a root that iterated
  tightening prunes while the midpoint clique is 8.
- 1,179 roots were pruned, but their clique numbers were at most 4. No counterexample was
  found, and the question stays open.

## 5. Theorem 2.3(b) with general `ψ` (`thm23_objective.py`, log `.log`)

**Proof check.** The proof is correct. I read `ψ` as real-valued and convex on `R`.

- `φ(w) = ψ̃(M(w))` with `ψ̃(s) = inf_{t ≥ s} ψ(t)`. It is finite: for `M ≥ 0` it equals
  `ψ(M)`, and for `M < 0` it is a minimum of a continuous function over `[M, 0]`.
- `φ = ψ(M)` for `M ≥ 0` and `φ ≤ ψ(0)` on `P_r`.
- `OPT = ψ(t*)`, because integer points have `M ≥ t* ≥ 1`.
- `φ ≥ ψ(t*)` on each `H_j`, so `κ ≤ m`.
- A leaf with `r ≥ OPT − ε > ψ(0)` misses `P_r`, because `ε < ψ(1) − ψ(0) ≤ ψ(t*) − ψ(0)`.
- Strictness is used only to make this range nonempty.

**Exact test.** I used two small integral systems with `t* = 1` and `P_r ≠ ∅`: a parity
system `2(w_1 + w_2 + w_3) = 3`, and `w_1 + w_2 = 1`, `w_1 = w_2`, both with box rows.

- For `ψ ∈ {t, t², |t|, t² + 2t, max(−t/2, 3t)}`:
  - `OPT = ψ(t*)`;
  - the `H_j` cover the integer window, with `φ ≥ OPT` on sampled points of `H_j`;
  - `φ ≤ ψ(0)` on `P_r` (102 points for the parity system, including its 6 vertices;
    the single point of `P_r` for the other system);
  - for `ε ∈ [0, ψ(1) − ψ(0))`, neither the root nor any leaf meeting `P_r` is a
    certificate.
- The root becomes a certificate exactly at `ε = OPT − ψ(0)`, so the range is sharp for
  these systems.
- With `ψ = (t − 1)²`, which violates the hypothesis, the root is already a certificate
  at `ε = 0`.

## 6. `δ` thresholds (`delta_thresholds.py`, log `.log`)

- **Theorem 3.4.** `(4/3)((1−δ)² − δ) = 1` at `δ = 3/2 − √2 = (3 − √8)/2 = 0.08579`.
  - `(1−δ)² − δ` decreases on `(0, 1/2)`.
  - At `δ = 0.08`, `1/r_0² = 1.3048 < 4/3`, so admissible `ρ` exist.
- **Theorem 3.5.** `(3/2)(1−δ)² − δ = 1` at `δ = (4 − √13)/3 = 0.13148`.
  - At `δ = 0.1`, `R² = 1.115 > 1`.
  - The cap-ball radius is `R² − ((1−δ)² − δ) = (1−δ)²/2`, as used in the proof.
- **Theorem 3.4 proof algebra.**
  - `θ = (2 − ρ)/ρ` and `A − bR² = 4 r_0²(ρ − 1)/ρ`.
  - `(1 − 1/n)a² − bR² = 2 r_0²(ρ−1)(nρ − 2)/(nρ)`, so monotonicity holds iff
    `ρ ≥ 2/n`. The sign expression decreases in `r`, so checking `r = R` suffices.
  - `4(ρ − 1)/ρ < 1` iff `ρ < 4/3`.
- **Exponents.** `0.2075188` and `0.2924813`.

## Remaining problems

None affects a stated result.

1. **Theorem 1.7(b), `κ = 1`.** The construction "the root has the single child `G_1`"
   has 2 nodes, not `2κ − 1 = 1`, and the root then has one child, so the tree is not
   binary. Fix: for `κ = 1`, take the root to be `G_1`, or `conv P` when `P` is finite.
2. **Lemma 1.7a wording.** "Nonzero affine functional" should read "non-constant affine
   functional" (nonzero linear part), so that `H` is a hyperplane. It may also help to
   say that the separation step is the finite-dimensional proper separation of `0` from
   `A − B`, valid because `0 ∉ ri(A − B)`.
3. **Theorem 1.8(c), iterated passes.** "`s_v` is at most `Σ_i (u_i − l_i)`" should read
   `Σ_i (u_i − l_i) + 1` when the node empties. The emptying change moves a bound past
   the other bound.
4. **The author's R4(b) does not test "by any amount".** Section 1.9 and the Section 6
   table describe R4(b) as "one piece per bound change". The code (`obbt` in
   `check_revision.py`) raises or lowers a bound one unit at a time and counts each unit
   step as a piece. Unit steps are valid certified removals, so the check is sound. But
   it gives a weaker inequality than the claim and never merges several units into one
   change. My `thm18c_counting.py` tests the stated rule (one piece per change of any
   size) and finds slack 0 in some instances, where the author reports minimum slack 1.
   R1 likewise tests one partition per instance, with `κ ≤ 2` in 54 of 60 instances. My
   Part B covers all minimum partitions and orderings with `κ` up to 4.
5. **Optional addition to Theorem 1.7(c)(ii).** Closed halfspaces also suffice when `E`
   is a partially open polyhedron, which is the case for every MILP relaxation. By
   Motzkin's transposition theorem, a polytope disjoint from `{x ∈ K : c·x < τ}`, with
   `K` polyhedral, lies in a closed halfspace missing that set. Genuine hemispaces are
   needed only in non-polyhedral, non-open cases such as Part C.
6. **Unclear remark (not part of the revision).** The first remark after Theorem 2.3's
   proof says the difficulty lies "in the integer points that the split disjunctions must
   also cover (with `t` near 0)". Integer points have `t ≥ 1`. The intended meaning seems
   to be that the leaves must exclude the fractional region `P_r` (where `t` can be near
   0) while covering all of `Z^n`.

## Checks run (targeted, local; not CI)

All commands ran from `research-20260928b/reviews/integer-core-recheck/` with Python
3.13.11, SymPy 1.14.0, NumPy 2.5.1 and SciPy 1.18.0. No project-wide checks were run, and
CI was not inspected. The author's scripts were read, not run.

| Command | Establishes | Result |
|---|---|---|
| `python3 selftest_exact.py` | the exact tools in `exact.py` (hull minimum, box minimum, halfspace minimum) against SciPy on 300 random cases | max relative deviation 9e-10, 6e-11, 1e-12 |
| `python3 t17_hemispace.py` (52 s) | Theorem 1.7 and Lemma 1.7a, Parts A–D (Section 1 above) | all chains and polytope versions valid; caterpillar invalid in 2/6, 458/1,370 and 27/283 cases |
| `python3 ex21a_compact_milp.py` | Example 2.1a | all checks pass; `κ = 4` on the window for `ε < 1/2`, 2 at `ε = 1/2` |
| `python3 prop52b_family.py` | Proposition 5.2(b) family, `n = 2..12` | (C1), `κ = 2`, `n + 1` leaves and `2n + 1` nodes |
| `python3 thm18c_counting.py 20260929 200` (3 min) | Theorem 1.8(c), 1,420 exact runs with explicit `T'` | 0 violations; all `T'` valid; binary bound `n + 1` attained |
| `python3 thm18c_iterated_example.py` | an explicit node with 5 > `2n` bound changes | as in Section 4 |
| `python3 openprob6_search.py 1 1500` (30 s) | small search related to Open problem 6 | no counterexample |
| `python3 thm23_objective.py` | Theorem 2.3(b) reduction for general `ψ` | as in Section 5 |
| `python3 delta_thresholds.py` | `δ` thresholds and Theorem 3.4 algebra | as in Section 6 |

## What remains unchecked

- The Gläser–Pfetsch lower bound itself and the encoding exponents of Theorem 2.3. They
  are cited, and the first review checked them.
- Section 9 items 4 and 8 and the "minor changes" list. They were outside the six items
  assigned, and I checked them only where they touch those items: Theorem 4.3(b)'s factor
  `2k + 1` follows from the binary form of Theorem 1.8(c) with `n = 2k`, and Section 3.5
  item 3 is consistent with the revised Theorem 1.8(c).
- Open problem 6. It remains open; my search is small and 3-D only.
