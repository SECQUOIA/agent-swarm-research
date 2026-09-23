import Formal.MultilinearGap.StructuralFrequencyBipartite
import Formal.MultilinearGap.StructuralFrequencySharpness

/-! The sharpness witnesses have exactly their advertised odd girth. -/
namespace MultilinearGap.StructuralFrequencyCycle
noncomputable section
open Fin.NatCast

private theorem cycle_ne_next (k : ℕ) (i : Cycle k) : i ≠ i + 1 := by
  intro h
  have hh : (1 : Cycle k) = 0 := add_left_cancel (h.symm.trans (add_zero i).symm)
  have hv := congrArg Fin.val hh
  simp at hv

/-- Any simple cycle in the cycle incidence rows visits every original edge. -/
theorem cycle_edge_surjective (k t : ℕ) (row edge : Cycle t → Cycle k)
    (hr : Function.Injective row) (he : Function.Injective edge)
    (hi : ∀ i, edge i ∈ support k (row i) ∧ edge i ∈ support k (row (i + 1))) :
    Function.Surjective edge := by
  have hprev (i : Cycle t) : i ≠ i - 1 := by
    intro h
    apply cycle_ne_next t (i - 1)
    simpa using h.symm
  have hrow (i : Cycle t) :
      (∃ j, edge j = row i) ∧ (∃ j, edge j = row i - 1) := by
    have h₁ := (hi i).1
    have h₂ := (hi (i - 1)).2
    simp only [support, Finset.mem_insert, Finset.mem_singleton] at h₁ h₂
    have hp : i - 1 + 1 = i := by simp
    rw [hp] at h₂
    rcases h₁ with h₁ | h₁ <;> rcases h₂ with h₂ | h₂
    · exact False.elim (hprev i (he (h₁.trans h₂.symm)))
    · exact ⟨⟨i, h₁⟩, ⟨i-1, h₂⟩⟩
    · exact ⟨⟨i-1, h₂⟩, ⟨i, h₁⟩⟩
    · exact False.elim (hprev i (he (h₁.trans h₂.symm)))
  have hclosed (e : Cycle k) (hh : ∃ i, edge i = e) : ∃ i, edge i = e + 1 := by
    obtain ⟨i, rfl⟩ := hh
    have h₁ := (hi i).1
    have h₂ := (hi i).2
    simp only [support, Finset.mem_insert, Finset.mem_singleton] at h₁ h₂
    rcases h₁ with h₁ | h₁
    · rcases h₂ with h₂ | h₂
      · exact False.elim (cycle_ne_next t i (hr (h₁.symm.trans h₂)))
      · have hh : row (i+1) = edge i + 1 := (sub_eq_iff_eq_add.mp h₂.symm)
        simpa only [hh] using (hrow (i+1)).1
    · have hh : row i = edge i + 1 := (sub_eq_iff_eq_add.mp h₁.symm)
      simpa only [hh] using (hrow i).1
  have hall (n : ℕ) : ∃ i, edge i = edge 0 + (n : Cycle k) := by
    induction n with
    | zero => exact ⟨0, by simp⟩
    | succ n ih => simpa only [Nat.cast_add, Nat.cast_one, add_assoc] using hclosed _ ih
  intro e
  simpa using hall (e - edge 0).val

/-- The cycle's indexed support rows have no shorter simple odd cycle. -/
theorem support_oddGirth (k : ℕ) :
    FrequencyOddGirthAtLeast (support k) (2 * k + 3) := by
  intro t row edge hr he hi
  have hc := Fintype.card_le_of_surjective edge (cycle_edge_surjective k t row edge hr he hi)
  simpa only [Fintype.card_fin] using hc

/-- The displayed cycle itself attains the claimed length. -/
theorem support_cycle_attained (k : ℕ) :
    ∃ (row edge : Cycle k → Cycle k), Function.Injective row ∧
      Function.Injective edge ∧
      (∀ i, edge i ∈ support k (row i) ∧ edge i ∈ support k (row (i + 1))) := by
  exact ⟨id, id, Function.injective_id, Function.injective_id, fun i => by simp [support]⟩

/-- Original distinct factor supports are indexed bijectively by the cycle. -/
def supportEquiv (k : ℕ) : Cycle k ≃ {s // s ∈ supports k} :=
  Equiv.ofBijective (fun v => ⟨support k v, Finset.mem_image.mpr ⟨v, Finset.mem_univ v, rfl⟩⟩)
    ⟨fun v w h => support_injective k (congrArg Subtype.val h), by
      intro s
      obtain ⟨v, _, hv⟩ := Finset.mem_image.mp s.property
      exact ⟨v, Subtype.ext hv⟩⟩

@[simp] theorem supportEquiv_val (k : ℕ) (v : Cycle k) :
    (supportEquiv k v).val = support k v := rfl

@[simp] theorem supportEquiv_symm_support (k : ℕ) (s : {s // s ∈ supports k}) :
    support k ((supportEquiv k).symm s) = s.val :=
  congrArg Subtype.val ((supportEquiv k).apply_symm_apply s)

/-- The original support family used by the sharp polynomial has odd girth
at least its full cycle length. -/
theorem supports_oddGirth (k : ℕ) :
    FrequencyOddGirthAtLeast (fun s : {s // s ∈ supports k} => s.val) (2 * k + 3) := by
  intro t row edge hr he hi
  apply support_oddGirth k t (fun i => (supportEquiv k).symm (row i)) edge
    ((supportEquiv k).symm.injective.comp hr) he
  intro i
  simpa only [supportEquiv_symm_support] using hi i

/-- The original support family also contains a simple cycle of that length. -/
theorem supports_cycle_attained (k : ℕ) :
    ∃ (row : Cycle k → {s // s ∈ supports k}) (edge : Cycle k → Cycle k),
      Function.Injective row ∧ Function.Injective edge ∧
      (∀ i, edge i ∈ (row i).val ∧ edge i ∈ (row (i + 1)).val) := by
  exact ⟨supportEquiv k, id, (supportEquiv k).injective, Function.injective_id,
    fun i => by simp [support]⟩

end
end MultilinearGap.StructuralFrequencyCycle
