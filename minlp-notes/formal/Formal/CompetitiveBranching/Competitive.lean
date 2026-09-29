import Formal.CompetitiveBranching.Theorem1

/-!
# Comparison with every finished tree

A finished tree with an arbitrary split rule (`Partition`) splits every
internal node in the interior of its interval and has only valid leaves.
Its leaves form a certificate with `internal + 1` intervals
(`Partition.certificate`), so Theorem 1 gives `T_min + 3 ≤ 4 T` for every
such tree `T`, in particular for an optimal one (`size_add_three_le`).
-/

open Set

noncomputable section

namespace CompetitiveBranching

variable {m : ℝ → ℝ} {α : ℝ}

/-- A finished tree on `[l, u]` under an arbitrary split rule: every split
point is interior and every leaf is valid. Internal nodes may be valid. -/
def Partition (m : ℝ → ℝ) (α : ℝ) : ℝ → ℝ → Tree → Prop
  | l, u, .leaf => Valid m α l u
  | l, u, .node y tl tr => y ∈ Ioo l u ∧ Partition m α l y tl ∧ Partition m α y u tr

/-- Concatenating certificates of `[l, y]` and `[y, u]`. -/
theorem IsCertificate.append {l y u : ℝ} {N₁ N₂ : ℕ} {s₁ s₂ : ℕ → ℝ}
    (h₁ : IsCertificate m α l y N₁ s₁) (h₂ : IsCertificate m α y u N₂ s₂) :
    IsCertificate m α l u (N₁ + N₂) (fun j => if j ≤ N₁ then s₁ j else s₂ (j - N₁)) := by
  set s : ℕ → ℝ := fun j => if j ≤ N₁ then s₁ j else s₂ (j - N₁) with hs
  have hlow : ∀ j ≤ N₁, s j = s₁ j := fun j hj => if_pos hj
  have hhigh : ∀ j, N₁ ≤ j → s j = s₂ (j - N₁) := by
    intro j hj
    by_cases h : j ≤ N₁
    · have hj' : j = N₁ := le_antisymm h hj
      rw [hlow j h, hj', h₁.finish, Nat.sub_self, h₂.start]
    · exact if_neg h
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [hlow 0 (Nat.zero_le _), h₁.start]
  · rw [hhigh _ (Nat.le_add_right _ _), Nat.add_sub_cancel_left, h₂.finish]
  · intro j hj
    by_cases h : j < N₁
    · rw [hlow j h.le, hlow (j + 1) h]
      exact h₁.lt_succ j h
    · rw [hhigh j (not_lt.mp h), hhigh (j + 1) (by omega),
        show j + 1 - N₁ = j - N₁ + 1 by omega]
      exact h₂.lt_succ _ (by omega)
  · intro j hj
    by_cases h : j < N₁
    · rw [hlow j h.le, hlow (j + 1) h]
      exact h₁.valid j h
    · rw [hhigh j (not_lt.mp h), hhigh (j + 1) (by omega),
        show j + 1 - N₁ = j - N₁ + 1 by omega]
      exact h₂.valid _ (by omega)

/-- The leaves of a finished tree form a certificate with one interval per
leaf, that is, with `internal + 1` intervals. -/
theorem Partition.certificate :
    ∀ (t : Tree) (l u : ℝ), l < u → Partition m α l u t →
      ∃ s : ℕ → ℝ, IsCertificate m α l u (t.internal + 1) s := by
  intro t
  induction t with
  | leaf =>
    intro l u hlu hv
    refine ⟨fun j => if j = 0 then l else u, ?_, ?_, ?_, ?_⟩
    · simp
    · simp [Tree.internal]
    · intro j hj
      simp only [Tree.internal] at hj
      obtain rfl : j = 0 := by omega
      simpa using hlu
    · intro j hj
      simp only [Tree.internal] at hj
      obtain rfl : j = 0 := by omega
      simpa [Partition] using hv
  | node y tl tr ihl ihr =>
    rintro l u - ⟨hy, htl, htr⟩
    obtain ⟨s₁, h₁⟩ := ihl l y hy.1 htl
    obtain ⟨s₂, h₂⟩ := ihr y u hy.2 htr
    have h := h₁.append h₂
    rw [show tl.internal + 1 + (tr.internal + 1) = (Tree.node y tl tr).internal + 1 by
      simp only [Tree.internal]; ring] at h
    exact ⟨_, h⟩

/-- **Competitive ratio below 4.** A minimizer-rule tree on `[L, U]` and any
finished tree on `[L, U]` satisfy `T_min + 3 ≤ 4 T`. -/
theorem size_add_three_le {L U : ℝ} (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    {t t' : Tree} (ht : MinRule m α L U t) (ht' : Partition m α L U t') :
    t.size + 3 ≤ 4 * t'.size := by
  cases t' with
  | leaf =>
    cases t with
    | leaf => simp [Tree.size]
    | node y tl tr => exact absurd ht' ht.1
  | node y tl tr =>
    obtain ⟨s, hc⟩ := Partition.certificate (.node y tl tr) L U
      (ht'.1.1.trans ht'.1.2) ht'
    have h := size_le hα hpos hc (by simp [Tree.internal]) ht
    rw [Tree.size_eq (.node y tl tr)]
    omega

/-- The minimizer-rule tree has fewer than four times as many nodes as any
finished tree, in particular an optimal one. -/
theorem size_lt_four_mul {L U : ℝ} (hα : 0 < α) (hpos : ∀ y ∈ Icc L U, 0 < m y)
    {t t' : Tree} (ht : MinRule m α L U t) (ht' : Partition m α L U t') :
    t.size < 4 * t'.size := by
  have := size_add_three_le hα hpos ht ht'
  omega

end CompetitiveBranching
