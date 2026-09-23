import Formal.NetworkSimplex.ThresholdFlowRepair

/-! The exceptional bypass coefficients identify three distinct actual gadgets. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open ThreeStateCircuits
variable {I : Type*} [DecidableEq I]

private theorem positive_bypass_coefficient (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r) (e : Fin 7)
    (he : weight c (positiveIndex e) ≠ 0) :
    rowCoefficient D (r (positiveIndex e)) .bypassFlow = bypassVector r (positiveIndex e) := by
  have hn := positive_row_not_totalLower D _ e (hr _ he)
  simp only [positiveIndex] at hn
  simp only [row_bypassFlow_coefficient, bypassVector, positiveIndex, e.isLt, if_true,
    hn, if_false, zero_sub]
  split_ifs <;> simp_all

theorem negative_bypass_distinct_witness (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r)
    (hb : circuitCoefficient D c r .bypassFlow = -2) :
    ∃ i₀ i₁ i₂ : I, c = 11 ∧ r 0 = .endpointA i₀ ∧ r 1 = .endpointA i₁ ∧
      r 2 = .endpointA i₂ ∧ i₀ ≠ i₁ ∧ i₀ ≠ i₂ ∧ i₁ ≠ i₂ ∧
      circuitCoefficient D c r (.aFlow i₀) = -1 := by
  rw [circuit_bypass_eq D hr] at hb
  rcases bypass_cases r c with hu | ⟨hc, _, h0, h1, h2⟩ | ⟨_, hp, _⟩
  · omega
  · subst c
    have hn0 := hr 0 (by decide : weight 11 0 ≠ 0)
    have hn1 := hr 1 (by decide : weight 11 1 ≠ 0)
    have hn2 := hr 2 (by decide : weight 11 2 ≠ 0)
    have hb0 : rowCoefficient D (r 0) .bypassFlow = -1 := by
      have he : rowCoefficient D (r 0) .bypassFlow = bypassVector r 0 := by
        simpa [positiveIndex] using positive_bypass_coefficient D hr (0 : Fin 7) (by decide)
      exact he.trans h0
    have hb1 : rowCoefficient D (r 1) .bypassFlow = -1 := by
      have he : rowCoefficient D (r 1) .bypassFlow = bypassVector r 1 := by
        simpa [positiveIndex] using positive_bypass_coefficient D hr (1 : Fin 7) (by decide)
      exact he.trans h1
    have hb2 : rowCoefficient D (r 2) .bypassFlow = -1 := by
      have he : rowCoefficient D (r 2) .bypassFlow = bypassVector r 2 := by
        simpa [positiveIndex] using positive_bypass_coefficient D hr (2 : Fin 7) (by decide)
      exact he.trans h2
    obtain ⟨i₀, hi0⟩ := singleton_negative_bypass_endpoint D (r 0) 0 hn0 hb0
    obtain ⟨i₁, hi1⟩ := singleton_negative_bypass_endpoint D (r 1) 1 hn1 hb1
    obtain ⟨i₂, hi2⟩ := singleton_negative_bypass_endpoint D (r 2) 2 hn2 hb2
    have h01 : i₀ ≠ i₁ := by
      intro h
      have he : (0 : Fin 11) = 1 := hr.row_injective D (by decide) (by decide)
        (by rw [hi0, hi1, h])
      exact (by decide : (0 : Fin 11) ≠ 1) he
    have h02 : i₀ ≠ i₂ := by
      intro h
      have he : (0 : Fin 11) = 2 := hr.row_injective D (by decide) (by decide)
        (by rw [hi0, hi2, h])
      exact (by decide : (0 : Fin 11) ≠ 2) he
    have h12 : i₁ ≠ i₂ := by
      intro h
      have he : (1 : Fin 11) = 2 := hr.row_injective D (by decide) (by decide)
        (by rw [hi1, hi2, h])
      exact (by decide : (1 : Fin 11) ≠ 2) he
    refine ⟨i₀, i₁, i₂, rfl, hi0, hi1, hi2, h01, h02, h12, ?_⟩
    have h10 := row_negative_full D (r 10) (hr 10 (by decide))
    simp only [circuitCoefficient, Fin.sum_univ_succ, Fin.sum_univ_zero]
    simp [weight, row_aFlow_coefficient, hi0, hi1, hi2, h10, Ne.symm h01, Ne.symm h02]
  · omega

theorem positive_bypass_distinct_witness (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r)
    (hb : circuitCoefficient D c r .bypassFlow = 2) :
    ∃ i₀ i₁ i₂ : I, c = 15 ∧ r 3 = .endpointB i₀ ∧ r 4 = .endpointB i₁ ∧
      r 5 = .endpointB i₂ ∧ i₀ ≠ i₁ ∧ i₀ ≠ i₂ ∧ i₁ ≠ i₂ ∧
      circuitCoefficient D c r (.aFlow i₀) = 1 := by
  rw [circuit_bypass_eq D hr] at hb
  rcases bypass_cases r c with hu | ⟨_, hn, _⟩ | ⟨hc, _, h0, h1, h2⟩
  · omega
  · omega
  · subst c
    have hn0 := hr 3 (by decide : weight 15 3 ≠ 0)
    have hn1 := hr 4 (by decide : weight 15 4 ≠ 0)
    have hn2 := hr 5 (by decide : weight 15 5 ≠ 0)
    have hb0 : rowCoefficient D (r 3) .bypassFlow = 0 := by
      have he : rowCoefficient D (r 3) .bypassFlow = bypassVector r 3 := by
        simpa [positiveIndex] using positive_bypass_coefficient D hr (3 : Fin 7) (by decide)
      exact he.trans h0
    have hb1 : rowCoefficient D (r 4) .bypassFlow = 0 := by
      have he : rowCoefficient D (r 4) .bypassFlow = bypassVector r 4 := by
        simpa [positiveIndex] using positive_bypass_coefficient D hr (4 : Fin 7) (by decide)
      exact he.trans h1
    have hb2 : rowCoefficient D (r 5) .bypassFlow = 0 := by
      have he : rowCoefficient D (r 5) .bypassFlow = bypassVector r 5 := by
        simpa [positiveIndex] using positive_bypass_coefficient D hr (5 : Fin 7) (by decide)
      exact he.trans h2
    obtain ⟨i₀, hi0⟩ := pair_zero_bypass_endpoint D (r 3) 0 hn0 hb0
    obtain ⟨i₁, hi1⟩ := pair_zero_bypass_endpoint D (r 4) 1 hn1 hb1
    obtain ⟨i₂, hi2⟩ := pair_zero_bypass_endpoint D (r 5) 2 hn2 hb2
    have h01 : i₀ ≠ i₁ := by
      intro h
      have he : (3 : Fin 11) = 4 := hr.row_injective D (by decide) (by decide)
        (by rw [hi0, hi1, h])
      exact (by decide : (3 : Fin 11) ≠ 4) he
    have h02 : i₀ ≠ i₂ := by
      intro h
      have he : (3 : Fin 11) = 5 := hr.row_injective D (by decide) (by decide)
        (by rw [hi0, hi2, h])
      exact (by decide : (3 : Fin 11) ≠ 5) he
    have h12 : i₁ ≠ i₂ := by
      intro h
      have he : (4 : Fin 11) = 5 := hr.row_injective D (by decide) (by decide)
        (by rw [hi1, hi2, h])
      exact (by decide : (4 : Fin 11) ≠ 5) he
    refine ⟨i₀, i₁, i₂, rfl, hi0, hi1, hi2, h01, h02, h12, ?_⟩
    have h10 := row_negative_full D (r 10) (hr 10 (by decide))
    simp only [circuitCoefficient, Fin.sum_univ_succ, Fin.sum_univ_zero]
    simp [weight, row_aFlow_coefficient, hi0, hi1, hi2, h10, Ne.symm h01, Ne.symm h02]

theorem negative_bypass_witness (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r)
    (hb : circuitCoefficient D c r .bypassFlow = -2) :
    ∃ i, r 0 = .endpointA i ∧ circuitCoefficient D c r (.aFlow i) = -1 := by
  obtain ⟨i₀, i₁, i₂, _, h0, _, _, _, _, _, ha⟩ := negative_bypass_distinct_witness D hr hb
  exact ⟨i₀, h0, ha⟩

theorem positive_bypass_witness (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (hr : ThreeBranch D c r)
    (hb : circuitCoefficient D c r .bypassFlow = 2) :
    ∃ i, r 3 = .endpointB i ∧ circuitCoefficient D c r (.aFlow i) = 1 := by
  obtain ⟨i₀, i₁, i₂, _, h0, _, _, _, _, _, ha⟩ := positive_bypass_distinct_witness D hr hb
  exact ⟨i₀, h0, ha⟩

end NetworkSimplex.Chain.Threshold
