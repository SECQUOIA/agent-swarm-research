import Formal.CompetitiveBranching.Competitive

/-!
# Theorem 1 in terms of `f`, `f*` and `ε`

The note prunes a node `B = [l, u]` when `LB(B) = min_B f_B ≥ f* - ε`, where
`f_B = f - α q_B` is the exact-gap relaxation, and `R_min` splits at a
minimizer of `f_B` over `B`. With `m = f - f* + ε` one has
`phi_B = f_B - (f* - ε)`, so pruning is `Valid` and the two minimizer sets
agree. This module proves these identities and restates Theorem 1 directly
for `f`. The pruning test is written pointwise, `∀ y ∈ B, f* - ε ≤ f_B y`,
which equals `LB(B) ≥ f* - ε` whether or not the minimum is attained.
The value `f*` is only required to be a lower bound of `f` on `[L, U]`.
-/

open Set

noncomputable section

namespace CompetitiveBranching

variable {f : ℝ → ℝ} {α fstar ε : ℝ}

/-- The exact-gap relaxation `f_B = f - α q_B` of the node `B = [l, u]`. -/
def relax (f : ℝ → ℝ) (α l u y : ℝ) : ℝ := f y - α * q l u y

/-- The pruning test `LB(B) ≥ f* - ε`, written pointwise on `B = [l, u]`. -/
def Pruned (f : ℝ → ℝ) (α fstar ε l u : ℝ) : Prop :=
  ∀ y ∈ Icc l u, fstar - ε ≤ relax f α l u y

/-- `m = f - f* + ε`. -/
def shifted (f : ℝ → ℝ) (fstar ε : ℝ) : ℝ → ℝ := fun y => f y - fstar + ε

theorem phi_shifted (l u y : ℝ) :
    phi (shifted f fstar ε) α l u y = relax f α l u y - (fstar - ε) := by
  simp only [phi, shifted, relax]
  ring

theorem valid_shifted_iff {l u : ℝ} :
    Valid (shifted f fstar ε) α l u ↔ Pruned f α fstar ε l u := by
  simp only [Valid, Pruned, phi_shifted, sub_nonneg]

theorem isMinOn_shifted_iff {l u y : ℝ} :
    IsMinOn (phi (shifted f fstar ε) α l u) (Icc l u) y ↔
      IsMinOn (relax f α l u) (Icc l u) y := by
  simp only [isMinOn_iff, phi_shifted, sub_le_sub_iff_right]

/-- A run of `R_min` in the note's terms: every internal node is not pruned
and splits at a minimizer of its relaxation `f_B` over `B`. -/
def RminTree (f : ℝ → ℝ) (α fstar ε : ℝ) : ℝ → ℝ → Tree → Prop
  | _, _, .leaf => True
  | l, u, .node y tl tr =>
      ¬ Pruned f α fstar ε l u ∧ y ∈ Icc l u ∧ IsMinOn (relax f α l u) (Icc l u) y ∧
        RminTree f α fstar ε l y tl ∧ RminTree f α fstar ε y u tr

theorem rminTree_iff :
    ∀ (t : Tree) (l u : ℝ),
      RminTree f α fstar ε l u t ↔ MinRule (shifted f fstar ε) α l u t := by
  intro t
  induction t with
  | leaf => intros; simp [RminTree, MinRule]
  | node y tl tr ihl ihr =>
    intro l u
    simp only [RminTree, MinRule, valid_shifted_iff, isMinOn_shifted_iff, ihl, ihr]

/-- `m = f - f* + ε > 0` on `[L, U]` when `f* ≤ f` there and `ε > 0`. -/
theorem shifted_pos {L U : ℝ} (hε : 0 < ε) (hfstar : ∀ y ∈ Icc L U, fstar ≤ f y) :
    ∀ y ∈ Icc L U, 0 < shifted f fstar ε y := by
  intro y hy
  have := hfstar y hy
  simp only [shifted]
  linarith

/-- **Theorem 1 for `f`.** Let `α > 0`, `ε > 0`, `f* ≤ f` on `[L, U]`, and let
`L = s 0 < ... < s N = U`, `N ≥ 2`, have every piece pruned. Then every
`R_min` tree on `[L, U]`, with any choice of minimizers, has at most
`4N - 5` internal nodes and at most `8N - 9` nodes. -/
theorem theorem1 {L U : ℝ} {N : ℕ} {s : ℕ → ℝ} (hα : 0 < α) (hε : 0 < ε)
    (hfstar : ∀ y ∈ Icc L U, fstar ≤ f y)
    (hstart : s 0 = L) (hfinish : s N = U) (hmono : ∀ j < N, s j < s (j + 1))
    (hpieces : ∀ j < N, Pruned f α fstar ε (s j) (s (j + 1))) (hN : 2 ≤ N)
    {t : Tree} (ht : RminTree f α fstar ε L U t) :
    t.internal ≤ 4 * N - 5 ∧ t.size ≤ 8 * N - 9 := by
  have hc : IsCertificate (shifted f fstar ε) α L U N s :=
    ⟨hstart, hfinish, hmono, fun j hj => valid_shifted_iff.mpr (hpieces j hj)⟩
  have ht' := (rminTree_iff t L U).mp ht
  exact ⟨internal_le hα (shifted_pos hε hfstar) hc hN ht',
    size_le hα (shifted_pos hε hfstar) hc hN ht'⟩

end CompetitiveBranching
