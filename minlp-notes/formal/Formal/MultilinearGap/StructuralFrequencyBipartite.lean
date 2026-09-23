import Formal.MultilinearGap.StructuralFrequencyRounding

/-! A two-coloring of the actual factor incidence rows excludes every
fractional odd cycle in the explicit layout. -/
namespace MultilinearGap
open CubicGap StructuralFrequencyCycle
noncomputable section
variable {V E C : Type*} [Fintype V] [Fintype E] [Fintype C]
  [DecidableEq V] [DecidableEq E] [DecidableEq C]

/-- Adjacent distinct rows receive different colors. Private and unused
coordinates impose no additional condition. -/
def FrequencyBipartite (S : V → Finset E) : Prop :=
  ∃ color : V → Bool, ∀ v w e, v ≠ w → e ∈ S v → e ∈ S w → color v ≠ color w

/-- Every simple odd cycle in the loopless incidence multigraph has length
at least `g`. Distinct row and edge labels preserve parallel-edge semantics. -/
def FrequencyOddGirthAtLeast (S : V → Finset E) (g : ℕ) : Prop :=
  ∀ (k : ℕ) (row : Cycle k → V) (edge : Cycle k → E),
    Function.Injective row → Function.Injective edge →
    (∀ i, edge i ∈ S (row i) ∧ edge i ∈ S (row (i + 1))) → g ≤ 2 * k + 3

namespace FrequencyCycleLayout
variable {S : V → Finset E} {z : E → ℝ}

omit [Fintype V] [Fintype E] [Fintype C] [DecidableEq V] [DecidableEq E] [DecidableEq C] in
/-- Every fractional cycle is an actual cycle of the input incidence graph. -/
theorem length_le_of_oddGirth (D : FrequencyCycleLayout S z C)
    {g : ℕ} (hg : FrequencyOddGirthAtLeast S g) (c : C) : g ≤ 2 * D.size c + 3 := by
  apply hg (D.size c) (D.row c) (D.edge c)
  · intro i j h
    have he := D.row_injective (a₁ := ⟨c,i⟩) (a₂ := ⟨c,j⟩) h
    simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and] using he
  · intro i j h
    have he := D.edge_injective (a₁ := ⟨c,i⟩) (a₂ := ⟨c,j⟩) h
    simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and] using he
  · intro i
    exact ⟨((D.incident c i _).mpr (Or.inl rfl)).1,
      ((D.incident c (i + 1) _).mpr (Or.inr (by simp))).1⟩

omit [Fintype V] [Fintype E] [Fintype C] [DecidableEq V] [DecidableEq E] [DecidableEq C] in
/-- An actual bipartite incidence system has no odd cycle in its fractional
layout. The proof sums the two opposite color indicators around the cycle. -/
theorem isEmpty_of_bipartite (D : FrequencyCycleLayout S z C)
    (hbi : FrequencyBipartite S) : IsEmpty C := by
  classical
  obtain ⟨color, hc⟩ := hbi
  refine ⟨fun c => ?_⟩
  let b : Cycle (D.size c) → ℕ := fun i => if color (D.row c i) then 1 else 0
  have hpair (i : Cycle (D.size c)) : b i + b (i + 1) = 1 := by
    have hi : i ≠ i + 1 := by
      intro h
      have hh : (1 : Cycle (D.size c)) = 0 := by
        exact add_left_cancel (h.symm.trans (add_zero i).symm)
      have hv := congrArg Fin.val hh
      simp at hv
    have hrow : D.row c i ≠ D.row c (i + 1) := by
      intro h
      have hh := D.row_injective (a₁ := ⟨c,i⟩) (a₂ := ⟨c,i+1⟩) h
      have he : i = i + 1 := by simpa only [Sigma.mk.inj_iff, heq_eq_eq, true_and] using hh
      exact hi he
    have hv := ((D.incident c i (D.edge c i)).mpr (Or.inl rfl)).1
    have hw := ((D.incident c (i + 1) (D.edge c i)).mpr (Or.inr (by simp))).1
    have hn := hc _ _ _ hrow hv hw
    cases he : color (D.row c i) <;> cases hf : color (D.row c (i+1)) <;>
      simp_all [b]
  have heq := congrArg (fun f : Cycle (D.size c) → ℕ => ∑ i, f i) (funext hpair)
  have hshift : (∑ i : Cycle (D.size c), b (i + 1)) = ∑ i, b i :=
    Equiv.sum_comp (Equiv.addRight (1 : Cycle (D.size c))) b
  simp only [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, smul_eq_mul, mul_one] at heq
  rw [hshift] at heq
  omega

end FrequencyCycleLayout
end
end MultilinearGap
