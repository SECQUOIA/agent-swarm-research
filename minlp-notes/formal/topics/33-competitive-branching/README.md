# Competitive relaxation-minimizer branching in one dimension

Date: 2026-09-29. Status: Theorem 1 is formalized without `sorry` or new
axioms. The six modules build warning-free with `--wfail`, pass the
targeted axiom audit, and replay in the kernel. An
[independent statement review](reviews/statement-review.md) found the
statements faithful, with no loopholes, and reran the targeted checks. A
separate review of the note
([competitive-review.md](../../../research-20260928b/reviews/competitive-review.md))
confirmed Theorem 1.

This package verifies Theorem 1 of
[competitive-branching.md](../../../research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md)
(Sections 1 and 4 of the note). In one dimension, with the exact-gap
relaxation, the branch-and-bound tree that splits every non-pruned node at
a minimizer of its relaxation has at most `4N - 5` internal nodes and at most
`8N - 9` nodes whenever a certificate with `N ≥ 2` intervals exists.

The proofs are in [`Formal/CompetitiveBranching`](../../Formal/CompetitiveBranching),
namespace `CompetitiveBranching`, on the pinned Lean 4.33.1 and Mathlib
installation under `formal/`. The [claim table](CLAIMS.md) maps each claim to
its Lean declaration. The [verification record](VERIFICATION.md) lists the
commands that were run.

## Main statements

The note's formulation, in terms of `f`, `f*` and `eps`
([`Pruning.lean`](../../Formal/CompetitiveBranching/Pruning.lean)):

```lean
theorem theorem1 {L U : ℝ} {N : ℕ} {s : ℕ → ℝ} (hα : 0 < α) (hε : 0 < ε)
    (hfstar : ∀ y ∈ Icc L U, fstar ≤ f y)
    (hstart : s 0 = L) (hfinish : s N = U) (hmono : ∀ j < N, s j < s (j + 1))
    (hpieces : ∀ j < N, Pruned f α fstar ε (s j) (s (j + 1))) (hN : 2 ≤ N)
    {t : Tree} (ht : RminTree f α fstar ε L U t) :
    t.internal ≤ 4 * N - 5 ∧ t.size ≤ 8 * N - 9
```

The core formulation, in terms of `m = f - f* + eps`
([`Theorem1.lean`](../../Formal/CompetitiveBranching/Theorem1.lean)):

```lean
theorem internal_le (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    (hc : IsCertificate m α L U N s) (hN : 2 ≤ N) {t : Tree}
    (ht : MinRule m α L U t) : t.internal ≤ 4 * N - 5
```

`size_le` gives `t.size ≤ 8 * N - 9` under the same hypotheses.
`count_interval_le_three`, `count_first_interval_le_one` and
`count_last_interval_le_one` give the per-interval bounds (at most 3 split
points inside each certificate interval, at most 1 inside each end
interval). `eq_leaf_of_certificate_one` covers `N = 1`: the tree is a single
leaf. `size_lt_four_mul` and `size_add_three_le`
([`Competitive.lean`](../../Formal/CompetitiveBranching/Competitive.lean))
compare against every finished tree `t'`: `t.size + 3 ≤ 4 * t'.size`. So the
ratio is below 4 against an optimal tree too.

## Model

Every modelling choice is listed here.

- **Objective data.** `m : ℝ → ℝ` is arbitrary except for `0 < m` on the root
  `[L, U]`. It stands for `f - f* + eps`. No continuity, convexity or
  smoothness is assumed. `α > 0` is fixed.
- **Relaxation and pruning.** `q l u y = (y - l) * (u - y)`,
  `phi m α l u y = m y - α * q l u y`, and `Valid m α l u` means
  `∀ y ∈ Icc l u, 0 ≤ phi m α l u y`. This is the note's `phi_B ≥ 0` on `B`.
- **Trees.** `Tree` is an inductive binary tree whose internal nodes store
  only their split point. A node's interval follows from the root interval
  and its ancestors' split points: the children of a node on `[l, u]` split
  at `y` lie on `[l, y]` and `[y, u]`. Storing `(l, y, u)` at every node
  would only add consistency conditions. `Tree.internal` counts internal
  nodes; `Tree.size` counts all nodes (the note's `T`), and
  `Tree.size_eq : t.size = 2 * t.internal + 1`. `Tree.count p` counts
  internal nodes whose split point satisfies `p`.
- **Minimizer rule.** `MinRule m α l u t` requires that every internal node
  on `[l, u]` is not `Valid`, and that its split point `y` satisfies
  `y ∈ Icc l u` and `IsMinOn (phi m α l u) (Icc l u) y`. Any minimizer may
  be chosen at each node. Leaves are unconstrained, so the bound holds for
  every partial tree of a run, not only the finished tree.
- **Certificate.** `IsCertificate m α L U N s` for `s : ℕ → ℝ` requires
  `s 0 = L`, `s N = U`, `s j < s (j + 1)` and `Valid m α (s j) (s (j + 1))`
  for all `j < N`. Values of `s` beyond `N` are irrelevant. Breakpoint
  indices agree with the note. Interval indices are shifted by one: the
  note's `J_{j+1} = [s_j, s_{j+1}]` is interval `j` here, for `j < N`.
- **Native formulation.** [`Pruning.lean`](../../Formal/CompetitiveBranching/Pruning.lean)
  defines `relax f α l u y = f y - α * q l u y` (the note's `f_B`) and the
  pruning test `Pruned`, written as `∀ y ∈ B, f* - eps ≤ f_B y`. This equals
  `LB(B) = min_B f_B ≥ f* - eps` whether or not the minimum is attained.
  `RminTree` splits non-pruned nodes at minimizers of `f_B`. With
  `m = shifted f fstar ε = f - f* + eps`, `phi_shifted`, `valid_shifted_iff`,
  `isMinOn_shifted_iff` and `rminTree_iff` identify the two models exactly.
  Only `f* ≤ f` on `[L, U]` is assumed, not that `f*` is the minimum.
- **Comparison trees.** `Partition m α l u t'` is a finished tree under any
  split rule: every split point is in the open node interval and every leaf
  is valid. Internal nodes may be valid. `Partition.certificate` turns its
  leaves into a certificate with `t'.internal + 1` intervals.

## Proof route

The formal proof follows the note's lemmas but replaces the global classes
`Y^L`, `Y^R`, `Y^LR` by structural induction on the tree.

1. `node_facts` (Lemma 1(i)): at an internal node, `phi < 0` at the split
   point, and the split point is interior because `m > 0` at the endpoints.
2. `key_left` and `key_right` (Lemma 2 and its mirror) are the algebraic
   core. The bilinear identity enters through `linarith`.
3. [`Counting.lean`](../../Formal/CompetitiveBranching/Counting.lean) fixes a
   valid interval `[a, b]` with `a < b`. It bounds the number of split points
   in `(a, b)` for a subtree on `[l, u]`. The bound is 0 when neither `a` nor
   `b` is interior to `[l, u]` (Lemma 1(iii)). It is at most 1 when `b` is
   not interior (class `Y^L`) or `a` is not interior (class `Y^R`); these two
   cases use Lemma 2 through `count_left_zero` and `count_right_zero`. It is
   at most 3 in general. `count_eq_le_one` is Lemma 1(ii).
4. `internal_le` charges each internal node to the half-open certificate
   interval `[s j, s (j + 1))` that contains its split point, so each label
   combines the breakpoint `s j` with the interior of the next interval. The
   budgets are 1 for `j = 0`, 2 for `j = N - 1`, and 4 otherwise, which sum
   to `4N - 5`.

## Check of the paper proof

No gap was found. The formalization supports every step of Sections 1.2–1.3
and 4 used by Theorem 1. Two observations:

- Lemma 2 needs weaker hypotheses than stated. The inner node `B₂` only has
  to lie in the child `[l_{B1}, y1]` of `B1` and have its split point above
  `s`. It need not contain `s` in its interior, and `B1` need not either.
  `key_left` and `key_right` are proved in this weaker form.
- Continuity of `f` is not used. It matters only for the existence of
  minimizers, which the formal statements assume by quantifying over trees.

## Not formalized

- Existence of relaxation minimizers (the note uses continuity of `f`), and
  the branch-and-bound run as a process. The note's termination claim
  follows informally: every partial tree of a run is a `MinRule` tree, so a
  run performs at most `4N - 5` splits. No run semantics is formalized.
- Section 4.1: other node orders and incumbents above `f*`, and
  Corollary 1 (inexact minimizers with tolerance `delta`). The incumbent
  remark follows from `internal_le` by instantiation, without a separate
  Lean statement: if every incumbent is at most `f* + g` with
  `0 ≤ g < eps`, every split node is invalid for `m' = f - f* + (eps - g)`,
  so the run's tree is a `MinRule` tree for `m'`, and `internal_le` applies
  with a certificate at tolerance `eps - g`. The independent
  [review](../../../research-20260928b/reviews/competitive-review.md) found
  the note's proof of Corollary 1 incomplete; it proves the bound with
  `N_opt(eps - 2 delta)` instead of `N_opt(eps - delta)`. Neither form is
  formalized here.
- The direction of `T_opt = 2 N_opt - 1` saying that every certificate is
  the leaf set of a tree with `2N - 1` nodes. Only the direction needed for
  the comparison theorem (finished tree to certificate) is proved.
- Section 4.2 sharpness claims and all numerical searches and checks.
- Proposition 0, Proposition 1 (proximal structure), Proposition 4
  (safeguarded rules), Theorem 2 (oblivious rules), and Theorem 3 (the 5/3
  deterministic and 4/3 randomized lower bounds).
- All `n`-dimensional statements, including Conjecture 1 and Section 6.

## Files

- [`Model.lean`](../../Formal/CompetitiveBranching/Model.lean): `q`, `phi`,
  `Valid`, `Tree`, `MinRule`, `IsCertificate`.
- [`Lemmas.lean`](../../Formal/CompetitiveBranching/Lemmas.lean): validity
  on sub-intervals, Lemma 1(i), Lemma 2 and its mirror.
- [`Counting.lean`](../../Formal/CompetitiveBranching/Counting.lean):
  per-subtree split-point bounds.
- [`Theorem1.lean`](../../Formal/CompetitiveBranching/Theorem1.lean):
  per-interval bounds, `4N - 5`, `8N - 9`, and `N = 1`.
- [`Competitive.lean`](../../Formal/CompetitiveBranching/Competitive.lean):
  certificates from finished trees and the ratio bound below 4.
- [`Pruning.lean`](../../Formal/CompetitiveBranching/Pruning.lean): the
  statement for `f`, `f*` and `eps`.
- [`verification/AuditCompetitiveBranching.lean`](verification/AuditCompetitiveBranching.lean):
  the targeted axiom audit.
