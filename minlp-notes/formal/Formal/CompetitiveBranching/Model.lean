import Mathlib

/-!
# One-dimensional exact-gap branch-and-bound model

This module fixes the model of Theorem 1 of
`research-20260928b/bb-complexity/branching-competitiveness/competitive-branching.md`.

* `m : ℝ → ℝ` stands for `f - f* + ε`; the theorems assume `0 < m` on the
  root interval `[L, U]`.
* `q l u y = (y - l)(u - y)` is the exact gap of the node `[l, u]`, and
  `phi m α l u = m - α q_{[l,u]}`.
* A node `[l, u]` is `Valid` (pruned) when `phi` is nonnegative on `[l, u]`.
* A `Tree` stores only split points. The interval of a node is determined by
  the root interval and the split points of its ancestors: the children of a
  node on `[l, u]` with split point `y` lie on `[l, y]` and `[y, u]`.
* `MinRule m α l u t` says that every internal node of `t` is not valid and
  splits at a point `y ∈ [l, u]` that minimizes `phi` over `[l, u]`. Leaves
  are unconstrained, so every partial tree of a run of the rule qualifies.
-/

open Set

noncomputable section

namespace CompetitiveBranching

/-- The exact gap `q_B(y) = (y - l)(u - y)` of the node `B = [l, u]`. -/
def q (l u y : ℝ) : ℝ := (y - l) * (u - y)

/-- `phi_B = m - α q_B` for the node `B = [l, u]`. -/
def phi (m : ℝ → ℝ) (α l u y : ℝ) : ℝ := m y - α * q l u y

/-- The node `[l, u]` is valid (pruned): `phi_B ≥ 0` on `[l, u]`. -/
def Valid (m : ℝ → ℝ) (α l u : ℝ) : Prop :=
  ∀ y ∈ Icc l u, 0 ≤ phi m α l u y

/-- Binary branch-and-bound trees. Internal nodes store their split point. -/
inductive Tree
  | leaf : Tree
  | node (y : ℝ) (left right : Tree) : Tree

namespace Tree

/-- Number of internal nodes (splits, relaxations that were branched on). -/
def internal : Tree → ℕ
  | leaf => 0
  | node _ tl tr => internal tl + internal tr + 1

/-- Number of nodes, the paper's `T`. -/
def size : Tree → ℕ
  | leaf => 1
  | node _ tl tr => size tl + size tr + 1

open Classical in
/-- Number of internal nodes whose split point satisfies `p`. -/
def count (p : ℝ → Prop) : Tree → ℕ
  | leaf => 0
  | node y tl tr => (if p y then 1 else 0) + count p tl + count p tr

theorem size_eq (t : Tree) : t.size = 2 * t.internal + 1 := by
  induction t with
  | leaf => rfl
  | node y tl tr ihl ihr => simp only [size, internal, ihl, ihr]; ring

end Tree

/-- Every internal node of the tree on `[l, u]` is not valid and splits at a
minimizer `y ∈ [l, u]` of `phi` over `[l, u]`. Leaves are unconstrained. -/
def MinRule (m : ℝ → ℝ) (α : ℝ) : ℝ → ℝ → Tree → Prop
  | _, _, .leaf => True
  | l, u, .node y tl tr =>
      ¬ Valid m α l u ∧ y ∈ Icc l u ∧ IsMinOn (phi m α l u) (Icc l u) y ∧
        MinRule m α l y tl ∧ MinRule m α y u tr

/-- A certificate with `N` intervals for the root `[L, U]`: breakpoints
`L = s 0 < s 1 < ... < s N = U` such that every `[s j, s (j + 1)]` is valid.
Values of `s` beyond `N` are irrelevant. -/
structure IsCertificate (m : ℝ → ℝ) (α L U : ℝ) (N : ℕ) (s : ℕ → ℝ) : Prop where
  start : s 0 = L
  finish : s N = U
  lt_succ : ∀ j < N, s j < s (j + 1)
  valid : ∀ j < N, Valid m α (s j) (s (j + 1))

end CompetitiveBranching
