import Mathlib

/-! Counting strict slope changes in a finite upper envelope. -/
namespace ReciprocalAnchor.ManyLeaf

/-- The indices at which a finite monotone slope sequence strictly increases. -/
noncomputable def slopeJumps {N : ℕ} (p : Fin (N + 1) → ℝ) : Finset (Fin N) :=
  Finset.univ.filter fun i => p i.castSucc < p i.succ

/-- Distinct strict changes have distinct slopes on their right. -/
theorem slopeJumps_right_injective {N : ℕ} (p : Fin (N + 1) → ℝ)
    (hp : Monotone p) : Set.InjOn (fun i : Fin N => p i.succ) (slopeJumps p) := by
  intro i hi j hj hij
  have hi' : p i.castSucc < p i.succ := (Finset.mem_filter.mp hi).2
  have hj' : p j.castSucc < p j.succ := (Finset.mem_filter.mp hj).2
  by_contra hne
  rcases lt_or_gt_of_ne hne with hij' | hji'
  · have hle : i.succ ≤ j.castSucc := by
      apply Fin.le_iff_val_le_val.mpr
      have := Fin.lt_def.mp hij'
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    have := (hp hle).trans_lt hj'
    exact (ne_of_lt this) hij
  · have hle : j.succ ≤ i.castSucc := by
      apply Fin.le_iff_val_le_val.mpr
      have := Fin.lt_def.mp hji'
      simp only [Fin.val_succ, Fin.val_castSucc]
      omega
    have := (hp hle).trans_lt hi'
    exact (ne_of_lt this) hij.symm

/-- A monotone sequence using finitely many input slopes has at most one fewer
strict slope changes than there are input lines. Repeated slopes and inactive
input lines do not affect the bound. -/
theorem slopeJumps_card_le {I : Type*} [Fintype I] {N : ℕ}
    (p : Fin (N + 1) → ℝ) (hp : Monotone p) (d : I → ℝ)
    (hinput : ∀ k, ∃ i, p k = d i) :
    (slopeJumps p).card ≤ Fintype.card I - 1 := by
  classical
  let right := (slopeJumps p).image fun i => p i.succ
  have hc : right.card = (slopeJumps p).card :=
    Finset.card_image_of_injOn (slopeJumps_right_injective p hp)
  have hzero : p 0 ∉ right := by
    intro hz
    obtain ⟨i, hi, he⟩ := Finset.mem_image.mp hz
    have hj := (Finset.mem_filter.mp hi).2
    have hle : (0 : Fin (N + 1)) ≤ i.castSucc := Fin.zero_le _
    have hlt := (hp hle).trans_lt hj
    exact (ne_of_lt hlt) he.symm
  have hsub : insert (p 0) right ⊆ Finset.univ.image d := by
    intro x hx
    have hx' : ∃ k, x = p k := by
      rcases Finset.mem_insert.mp hx with h | h
      · exact ⟨0, h⟩
      · obtain ⟨i, _, hi⟩ := Finset.mem_image.mp h
        exact ⟨i.succ, hi.symm⟩
    obtain ⟨k, rfl⟩ := hx'
    obtain ⟨i, hi⟩ := hinput k
    exact Finset.mem_image.mpr ⟨i, Finset.mem_univ _, hi.symm⟩
  have hcard := (Finset.card_le_card hsub).trans (Finset.card_image_le)
  rw [Finset.card_insert_of_notMem hzero, hc, Finset.card_univ] at hcard
  omega

end ReciprocalAnchor.ManyLeaf
