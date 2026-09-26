# Exponential lower bound for spatial branch-and-bound with separable relaxations

Date: 2026-09-04. Status: proof written by the root agent; numerical sanity
checks passed; one independent review passed with corrections (all applied,
including a corrected theorem statement); second independent review passed
with minor scope corrections applied; novelty search completed (see the
final sections).

## Summary

For the separable concave quadratic program

```
P_n:  minimize  sum_{i=1}^n x_i (1 - x_i)
      subject to  sum_{i=1}^n x_i = k + 1/2,   x in [0,1]^n,
```

whose optimal value is `1/4`, every spatial branch-and-bound tree that
branches on variables (any coordinate, any split point, any order, any node
selection), bounds each node by any separable convex underestimator of the
objective (chords, McCormick on the bilinear form `x_i y_i` with
`y_i = 1 - x_i`, αBB, or any weaker separable relaxation), and certifies
`ε`-optimality for a fixed `ε < 1/4`, has `2^{Ω(n)}` leaves when `k` and
`n-k` are both linear in `n` (for instance `k = n/3`). With `n = 3t` and
`ε = 1/8` the bound is `(3/2)^{t/8}` leaves; an explicit tree with `O(2^n)`
nodes exists, so the size is `2^{Θ(n)}`. The restriction on `k` is
necessary: for fixed `k` (or fixed `n-k`) an `O(n^{k+1})`-node certificate
exists (Remark 7).

The instance is a continuous analogue of Jeroslow's example for integer
branch-and-bound. The relaxations have second-order convergence, so the blow-up
is combinatorial and not a cluster effect. The proof does not depend on the
branching rule at all: it lower-bounds the size of any cover of the feasible
set by boxes on which the chord relaxation is at least `1/4 - ε`.

## Setting

Write `f(x) = x(1-x)` and `F = {x in [0,1]^n : sum_i x_i = k + 1/2}` for an
integer `k` with `1 <= k <= n-1`. For a box `B = prod_i [a_i, b_i]` inside
`[0,1]^n`, the chord of `f` on `[a_i, b_i]` is

```
ℓ_i(x) = a_i b_i + (1 - a_i - b_i) x,     with  f(x) - ℓ_i(x) = (x - a_i)(b_i - x) >= 0  on [a_i, b_i].
```

The chord is the convex envelope of the concave function `f` on the interval.
A *separable relaxation* of `P_n` on `B` is any function `sum_i g_i(x_i)` with
each `g_i` convex on `[a_i, b_i]` and `g_i <= f` there; then `g_i <= ℓ_i`.
Its node bound is `LB_g(B) = inf{ sum_i g_i(x_i) : x in B ∩ F }` (`+∞` if
`B ∩ F` is empty), and

```
LB_g(B) <= LB(B) := min{ sum_i ℓ_i(x_i) : x in B ∩ F }.
```

Three standard relaxations coincide with the chord: (i) the McCormick
relaxation of `w_i = x_i y_i` with `y_i = 1 - x_i`, `y_i in [1-b_i, 1-a_i]`,
both underestimators of which reduce to `ℓ_i` after substituting `y_i`;
(ii) the αBB underestimator `f(x) - α(x - a_i)(b_i - x)` with the minimal
valid `α = 1`; (iii) the secant used by interval methods for concave terms.

A *branch-and-bound tree* is a rooted binary tree whose root carries
`[0,1]^n` and in which each internal node with box `B` has children
`B ∩ {x_i <= θ}` and `B ∩ {x_i >= θ}` for some coordinate `i` and some
`θ in (a_i, b_i)`. Call a box `B` *ε-pruned* if `B ∩ F = ∅` or
`LB(B) >= 1/4 - ε`. A tree is an *ε-certificate* if all its leaves are
ε-pruned. Any complete branch-and-bound run that uses a separable relaxation
and fathoms a node only when it is infeasible or when its bound is at least
`UB - ε` for an incumbent value `UB >= OPT = 1/4` produces an ε-certificate,
since `LB(B) >= LB_g(B) >= UB - ε >= 1/4 - ε` at every fathomed node.
(A node cannot be fathomed because its relaxation solution is exact while
`LB_g(B) < 1/4 - ε`: exactness would give a feasible point of value below
`1/4`.) Relative gap tolerances `ε_rel` are absolute tolerances `ε_rel/4`
here; a feasibility tolerance `δ` on the equality replaces `ε` by `ε + δ^2`.
Symmetry exploitation, branching on auxiliary product variables, and
non-convex (piecewise) separable underestimators are outside the definition.

**Lemma 1 (optimal value).** `OPT(P_n) = 1/4`.

*Proof.* `F` is a polytope and the objective is concave, so the minimum is
attained at a vertex of `F`. A vertex of `{x in [0,1]^n : sum x_i = k+1/2}`
has at least `n-1` tight bound constraints, hence at most one coordinate not
in `{0,1}`; the equality forces that coordinate to be `1/2`. The objective at
such a vertex is `f(1/2) = 1/4`. □

## Theorem

**Theorem 1.** Let `n = k + m + z` with integers `k, m >= 1`, `z >= 0`, and
let `0 < ε < 1/4`. Every ε-certificate for `P_n` has at least

```
min{ (n/(n-k))^{h/2}, (n/(n-z))^{h/2} }   leaves,   where  h = m(1/2 - 2ε).
```

In particular, for `n = 3t` with `k = z = m = t`, every ε-certificate has at
least `(3/2)^{t(1/4 - ε)}` leaves; for `ε = 1/8` this is `(3/2)^{n/24}`. The
bound is trivial when `z = 0` and at most `e^{k/4}` for fixed `k`; see
Remark 7.

*Proof.* Fix an ordered partition `(H, M, Z)` of `[n]` with `|H| = k`,
`|M| = m`, `|Z| = z` and define the witness

```
w = 1_H + (1/(2m)) 1_M .
```

It lies in `F` (its coordinate sum is `k + 1/2`, all coordinates in `[0,1]`).
The leaves of an ε-certificate cover `[0,1]^n`, so `w` lies in some leaf box
`B`, and `B` is ε-pruned; since `w in B ∩ F`, this means `LB(B) >= 1/4 - ε`.

*Step 1: what containing `w` forces on `B`.* Let `A = {i : a_i > 0}` and
`D = {i : b_i < 1}` and `R = A ∪ D`. Since `w in B`: coordinates in `Z` have
`w_i = 0`, so `Z ∩ A = ∅`; coordinates in `H` have `w_i = 1`, so
`H ∩ D = ∅`. For `i in H` we get `ℓ_i(1) = f(1) = 0` because `b_i = 1`, and
for `i in Z` we get `ℓ_i(0) = f(0) = 0` because `a_i = 0`. Hence

```
1/4 - ε <= LB(B) <= sum_i ℓ_i(w_i) = sum_{i in M} ℓ_i(1/(2m)).
```

For `i notin R` the chord on `[0,1]` is identically zero, so the sum runs over
`M ∩ R`. Each term satisfies `ℓ_i(1/(2m)) <= f(1/(2m)) < 1/(2m)`. Therefore

```
|M ∩ R| > 2m (1/4 - ε) = h,     so  |A| + |D| >= |R| > h,
```

and consequently `|A| > h/2` or `|D| > h/2`.

*Step 2: a pruned box contains few witnesses.* Fix any ε-pruned box `B` and
draw `(H, M, Z)` uniformly at random among the `n!/(k! m! z!)` ordered
partitions. If `B` contains no witness there is nothing to prove. Otherwise,
by Step 1 applied to any witness in `B`, `|A| > h/2` or `|D| > h/2`, and every
witness in `B` satisfies `Z ∩ A = ∅` and `H ∩ D = ∅`. The set `Z` is a
uniformly random `z`-subset of `[n]`, so for a fixed set `A` of size `s`,

```
Pr[Z ∩ A = ∅] = C(n-s, z)/C(n, z) = prod_{j=0}^{s-1} (n-z-j)/(n-j) <= ((n-z)/n)^s,
```

and likewise `Pr[H ∩ D = ∅] <= ((n-k)/n)^{|D|}`. Hence the fraction of
witnesses contained in `B` is at most

```
min{ ((n-z)/n)^{|A|}, ((n-k)/n)^{|D|} } <= max{ ((n-z)/n)^{h/2}, ((n-k)/n)^{h/2} } =: ρ.
```

*Step 3: counting.* Every witness lies in at least one leaf, and each leaf
contains at most a `ρ` fraction of the witnesses, so the number of leaves is
at least `1/ρ = min{(n/(n-z))^{h/2}, (n/(n-k))^{h/2}}`, which is the stated
bound. For `k = z = m = t`, `n = 3t`, the
two bases equal `2/3`, and `h/2 = t(1/4 - ε)`. □

The argument never uses that the leaves form a tree or are disjoint: any
family of ε-pruned boxes covering `F` has at least `1/ρ` members.

**Proposition 2 (matching upper bound).** For every `ε in (0, 1/4)` there is
an ε-certificate with at most `2^{n+2}` nodes.

*Proof.* Let `α in (0, 1/2)` satisfy `α(1-α) = 1/4 - ε`. Process the
coordinates in order `1, …, n`; at a node whose coordinates `1, …, i-1` are
each restricted to `[0, α]` or `[1-α, 1]`, split coordinate `i` at `α` and
then split the upper child at `1-α`. The middle child, with `x_i` restricted
to `[α, 1-α]`, has `a_i + b_i = 1`, so its chord is the constant
`α(1-α) = 1/4 - ε`; every other chord is nonnegative, hence `LB >= 1/4 - ε`
and the node is pruned. After all `n` coordinates are processed, a leaf has
every coordinate in `[0, α]` (chord `(1-α)x_i`) or in `[1-α, 1]` (chord
`(1-α)(1-x_i)`). Let `b` be the number of high coordinates. On `B ∩ F` the
sum of the chords is `(1-α)` times the total distance of `x` from the point
with low coordinates `0` and high coordinates `1`, and that distance is at
least `|k + 1/2 - b| >= 1/2`, so `LB(B) >= (1-α)/2 > 1/4 - ε` (because
`α < 1/2` gives `(1-α)/2 > 1/4 > 1/4 - ε`). Processing coordinate `i`
creates `2^{i-1}` nodes of each of four kinds (low, upper, middle, high), so
the tree has `1 + sum_{i=1}^n 2^{i+1} = 2^{n+2} - 3` nodes and `2^{n+1} - 1`
leaves. If a solver fathoms only on a strict inequality, take
`α(1-α) = 1/4 - ε + δ` for a small `δ > 0`. □

## Remarks and scope

1. **Independence of the branching rule.** Theorem 1 holds for arbitrary
   split points, variable choices, node orders, and for trees that split a
   box into any number of sub-boxes by coordinate hyperplanes, since only the
   final cover by pruned boxes is used.
2. **Bound tightening.** Consider objective-based bound tightening that
   discards coordinate slabs whose closed boxes have relaxation bound at
   least `UB - ε`. Every such slab is an ε-pruned box. A run that performs
   at most `q` such reductions per processed node gives an augmented cover
   of `F`: its final leaf boxes together with all discarded certified slabs.
   It contains at most `(q+1)·(number of processed nodes)` boxes, so Theorem 1
   gives `(number of processed nodes) >= 1/((q+1)ρ)`. Feasibility-based
   tightening removes only points outside `F`, so it preserves coverage
   without adding discarded slabs. Objective-based tightening can remove
   feasible points, which is why its discarded slabs must be counted.
   The cover theorem applies to the changed boxes and does not require
   that they be leaves of the original tree definition. (At the root,
   no feasibility-based tightening is possible for `1 <= k <= n-2`;
   for `k = n-1` it shrinks the root to `[1/2,1]^n`, which is already
   pruned, consistent with the bound `1` of Theorem 1 for `z = 0`.)
3. **Non-separable relaxations are not covered.** The statement concerns
   relaxations whose objective underestimator is a sum of univariate convex
   functions. Relaxations that exploit the coupling constraint (for example
   RLT products of the equality with variables, or SDP constraints) are outside
   the theorem. They are not obviously better: at the root box with
   `n >= 2k+1` (or `n = 2k`, `k >= 2`), the RLT+SDP relaxation of `P_n` also
   has value `0`. Take
   `x = c·1` with `c = (k+1/2)/n`, `X_ii = c`, and `X_ij = d := (k-1/2)c/(n-1)`
   for `i ≠ j`. Then `sum_j X_ij = (k+1/2) x_i` (the RLT product of the
   equality with `x_i`), `0 <= X_ij <= x_i`, `X_ij >= x_i + x_j - 1 = (2k+1-n)/n`
   (for `n >= 2k+1` the right-hand side is nonpositive; for `n = 2k` it equals
   `1/(2k)` and `d = (2k+1)/(8k) >= 1/(2k)` when `k >= 2`; for `k = n-1`,
   including `(n,k) = (2,1)`, the point violates this bound, and at `(2,1)`
   the RLT relaxation is in fact exact), and
   `X - x x^T = (c-d) I + (d - c^2) J` has eigenvalues `c - d > 0` and
   `c - d + n(d - c^2) = c(k + 1/2 - nc) = 0`, so it is PSD; the objective
   `sum_i (x_i - X_ii)` is `0`. The behaviour of such relaxations under
   branching is left open.
4. **Second-order convergence.** The chord error on `[a_i, b_i]` is at most
   `(b_i - a_i)^2/4`, so the relaxation has second-order (Hausdorff)
   convergence in the sense of the cluster-problem literature. The lower bound
   is therefore not an artefact of first-order convergence; it is a
   combinatorial obstruction at a fixed absolute tolerance.
5. **Tolerance.** The exponent `h = m(1/2 - 2ε)` degenerates as `ε → 1/4`,
   which is necessary: for `ε = 1/4` the root alone is a certificate. As
   `ε → 0` the bound tends to `(3/2)^{t/4}` for `n = 3t`.
6. **Relevance.** Separable concave objectives over a knapsack-type equality
   are the simplest economies-of-scale models in process design. The theorem
   shows that every off-the-shelf spatial branch-and-bound scheme with
   termwise relaxations needs exponentially many nodes on this family when
   `k = Θ(n)` and `n-k = Θ(n)`, whatever branching heuristics it uses, and
   that only relaxations coupling the variables through the constraint, or
   techniques outside the model such as symmetry exploitation, could avoid
   this.
7. **Fixed `k` is easy.** For fixed `k` (or fixed `n-k`) there is an
   `ε = 0` certificate with `O(n^{min(k,n-k)+1})` nodes: branch every
   coordinate at `1/2` in order; a node with `c` coordinates restricted to
   `[1/2,1]` and `d` coordinates restricted to `[0,1/2]` has
   `LB >= (c - k - 1/2)/2 >= 1/4` when `c >= k+1` (the high coordinates sum
   to at most `k+1/2`, each unit below `1` costs `1/2`) and
   `LB >= (k + 1/2 - (n-d))/2 >= 1/4` when `d >= n-k` (the low coordinates
   must sum to at least `k+1/2-(n-d)`, each unit above `0` costs `1/2`), so
   prune as soon as `c = k+1` or `d = n-k`; no node survives depth `n`.
   For `k = 1` this tree has `n^2 + n - 1` nodes and `n(n+1)/2` leaves. This
   is why Theorem 1's bound is `min` of two terms and degenerates for
   `z = 0` or fixed `k`.

## Verification

- [Numerical checks](../code/spatial_bb_lower_bound/check_lower_bound.py):
  exact vertex enumeration confirms `OPT = 1/4` for small `n`; the chord
  relaxation is verified against the McCormick and αBB forms; the boxes used
  in Proposition 2 are checked to be pruned by solving the chord LP; and for
  random boxes containing a random witness the inequalities of Step 1
  (`LB(B) <= sum_M ℓ_i(1/(2m))`, and `|M ∩ R| > h` whenever the box is
  pruned) are verified with an LP solver. The script also checks the
  Remark 3 McCormick condition exactly for all `1 <= k <= n-1`, `n <= 12`
  (it holds whenever the stated condition holds and fails exactly for
  `k = n-1`), verifies by LP that the Remark 7 tree's leaves
  are pruned for several `(n,k)`, and checks that Theorem 1's `min` bound
  never exceeds that tree's leaf count.
- [Independent review](../notes/review-spatial-bb-lower-bound.md): PASS WITH
  CORRECTIONS. The reviewer found that the theorem statement had `max` where
  the proof gives `min`, that the exponential claim needs `k, n-k = Θ(n)`,
  and that the Remark 3 condition was misstated; all corrections above were
  applied. The reviewer reports LP checks of the `k = 1` and `k = n-1`
  trees up to `n = 50` and of the cover counterexample to the `max` form;
  those reviewer scripts were not archived. A new independent checker
  ([script](../code/spatial_bb_lower_bound/review_lower_bound_repro.py),
  [2026-09-25 output](../code/spatial_bb_lower_bound/review_lower_bound_repro-2026-09-25.log))
  reproduces the reviewer's listed checks with exact and HiGHS chord-LP
  bounds. It does not reproduce one wording in the review's check list: the
  invalid justification `1/n <= d` fails at 22 of the 36 pairs with
  `n >= 2k`, `n <= 12`, not at all of them.

- [Second independent review](../notes/review-spatial-bb-second.md): core
  results pass; the underestimator bound now uses an infimum to allow arbitrary
  convex endpoint behavior, and objective-tightening slabs are explicitly
  included in the cover.

## Related work and novelty

A literature agent searched WebSearch, the arXiv API, Optimization Online,
dblp, and Semantic Scholar (rate-limited) and read the closest papers. No
statement of this kind for spatial branch-and-bound was found. An
unsuccessful search does not establish priority. The nearest results:

- R. Jeroslow, Trivial integer programs unsolvable by branch-and-bound,
  Math. Program. 6 (1974) 105–109: the integer program `2 sum x_i = 2n+1`,
  `x in {0,1}^{2n}`, needs `Ω(2^n)` nodes under variable branching. `P_n` is
  the continuous relaxation of this instance with integrality replaced by the
  penalty `sum x_i(1-x_i)`; the present theorem allows arbitrary split points,
  any separable convex underestimator, and only asks for a fixed tolerance.
- S. Dey, Y. Dubey, M. Molinaro, Lower bounds on the size of general
  branch-and-bound trees, Math. Program. 198 (2023): exponential bounds for
  general-disjunction branching in integer programming, via points that must
  be separated. Pure integer setting; they note Jeroslow-type instances are
  easy for general disjunctions, which is why variable branching is essential
  here as well.
- D. Bertsimas, R. Cory-Wright, S. Lo, J. Pauphilet, Disjunctive
  branch-and-bound for certifiably optimal low-rank matrix completion,
  arXiv:2305.12292, Proposition 1: for their SDP+McCormick relaxation, any node
  with fewer than `n-3` branched rows per column pair keeps the root value, so
  more than `2^{n-4}` nodes are expanded before the bound moves. That is a
  no-improvement depth statement for one structured relaxation, not a leaf
  count for certifying a fixed gap under any separable relaxation.
- The cluster problem (K. Du, R. B. Kearfott 1994; A. Wechsung, S. Schaber,
  P. I. Barton 2014; R. Kannan, P. I. Barton 2017; A. Neumaier, Acta Numerica
  2004, Section 15): asymptotic counts of unfathomable boxes around a single
  nondegenerate minimizer as the tolerance tends to zero. For second-order
  relaxations, which include the chords used here, the cluster count is
  bounded, so that theory does not predict the present blow-up; the present
  bound comes from exponentially many spread-out near-optimal vertices at a
  fixed tolerance.
- D. Grigoriev (2001) and M. Laurent (2003): the knapsack equality
  `sum x_i = k + 1/2` over `{0,1}^n` needs `Ω(n)` sum-of-squares rounds; the
  same instance family in a different proof system.
- Information-based complexity (Nemirovski–Yudin; Vavasis 1991): oracle
  lower bounds for adversarial function classes, not for a fixed instance and
  a fixed algorithm class.


### Updated literature scope (2026-09-05)

A [follow-up literature comparison](../notes/spatial-bb-strengthening-novelty.md)
identified Coniglio's ICLR 2026 spatial lower bound under midpoint branching,
in addition to Jarre's binary SDP lower bound. Thus exponential spatial
lower bounds in general are already known. The tentative novelty claim here
is restricted to the specified arbitrary-split, fixed-gap relaxation model.
The literature note records which source portions were read and which
appendix proof remained inaccessible after a browser challenge.


### Known global cut outside the model

A [classical Boolean-quadric clique inequality](../notes/spatial-bb-known-clique-cut.md)
closes the root after equality-product linearization. Thus this family is
an obstruction to the specified spatial certificate system, not a
computationally hard optimization problem or an obstruction to all known
cutting-plane methods.
