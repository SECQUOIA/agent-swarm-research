import Formal.NetworkSimplex.ThresholdRowOccurrences
import Formal.NetworkSimplex.ThresholdOccurrence

/-! Unit product coefficients derived from the actual row branches. -/
namespace NetworkSimplex.Chain.Threshold
open scoped BigOperators
open ThreeStateCircuits

/-- The nonempty subset's index in the seven positive normals; the empty input
has an arbitrary total value and can never match a nonzero circuit normal. -/
def subsetIndex (s : Finset (Fin 3)) : Fin 7 :=
  if 0 ∈ s then
    if 1 ∈ s then if 2 ∈ s then 6 else 3
    else if 2 ∈ s then 4 else 0
  else if 1 ∈ s then if 2 ∈ s then 5 else 1 else 2

theorem normal_subset_index : ∀ (k : Fin 11) (s : Finset (Fin 3)),
    normalVector (.subset s) = normal k → k = positiveIndex (subsetIndex s) := by
  decide +kernel

theorem normal_singleton_index : ∀ (k : Fin 11) (j : Fin 3),
    normalVector (.subset {j}) = normal k → k = singletonIndex j := by decide +kernel

theorem normal_negative_singleton_index : ∀ (k : Fin 11) (j : Fin 3),
    normalVector (.negativeSingleton j) = normal k → k = negativeSingletonIndex j := by
  decide +kernel

@[simp] theorem normalVector_empty : normalVector (.subset (∅ : Finset (Fin 3))) = 0 := by
  funext j
  simp [normalVector]

theorem normal_nonzero : ∀ k : Fin 11, normal k ≠ 0 := by decide +kernel

variable {I : Type*} [DecidableEq I]

def endpointASet (D : ReductionData 3 I) (i : I) : Finset (Fin 3) :=
  Finset.univ.filter fun j => observesA (D.c i j.succ)

def endpointBSet (D : ReductionData 3 I) (i : I) : Finset (Fin 3) :=
  Finset.univ.filter fun j => D.c i j.succ = .bOnly

/-- Rows outside the circuit support are ignored before applying occurrence analysis. -/
def supportedCoefficient (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (z : Coordinate 3 I) (k : Fin 11) : ℤ :=
  if weight c k = 0 then 0 else rowCoefficient D (r k) z

theorem supportedCoefficient_sum (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (z : Coordinate 3 I) :
    (∑ k, weight c k * supportedCoefficient D c r z k) =
      ∑ k, weight c k * rowCoefficient D (r k) z := by
  apply Finset.sum_congr rfl
  intro k _
  by_cases h : weight c k = 0 <;> simp [supportedCoefficient, h]

omit [DecidableEq I] in
private theorem endpointA_branch_index (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (hr : ThreeBranch D c r)
    (i : I) (k : Fin 11) (hk : weight c k ≠ 0) (he : r k = .endpointA i) :
    k = positiveIndex (subsetIndex (endpointASet D i)) ∧
      normal k = normalVector (.subset (endpointASet D i)) := by
  have hn := hr k hk
  rw [he] at hn
  change normalVector (.subset (endpointASet D i)) = normal k at hn
  exact ⟨normal_subset_index k _ hn, hn.symm⟩

omit [DecidableEq I] in
private theorem endpointB_branch_index (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (hr : ThreeBranch D c r)
    (i : I) (k : Fin 11) (hk : weight c k ≠ 0) (he : r k = .endpointB i) :
    k = positiveIndex (subsetIndex (endpointBSet D i)) ∧
      normal k = normalVector (.subset (endpointBSet D i)) := by
  have hn := hr k hk
  rw [he] at hn
  change normalVector (.subset (endpointBSet D i)) = normal k at hn
  exact ⟨normal_subset_index k _ hn, hn.symm⟩

theorem threeBranch_aProduct_unit (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (hr : ThreeBranch D c r) (i : I) (j : Fin 3) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) (.aProduct i j) ∧
      (∑ k, weight c k * rowCoefficient D (r k) (.aProduct i j)) ≤ 1 := by
  rw [← supportedCoefficient_sum D c r (.aProduct i j)]
  apply signed_occurrence_sum_unit c j (subsetIndex (endpointASet D i))
    (subsetIndex (endpointBSet D i))
  · intro k
    by_cases h : weight c k = 0
    · simp [supportedCoefficient, h]
    · simpa [supportedCoefficient, h] using row_aProduct_bounds D (r k) i j
  · intro k hk
    have hw : weight c k ≠ 0 := by intro h; simp [supportedCoefficient, h] at hk
    have hp : 0 < rowCoefficient D (r k) (.aProduct i j) := by
      simpa [supportedCoefficient, hw] using hk
    rcases row_aProduct_positive D (r k) i j hp with ⟨he, ht⟩ | ⟨he, ht⟩
    · left
      apply normal_singleton_index k j
      have hn := hr k hw
      simpa [he, ReductionData.rowNormal, ht] using hn
    · right
      obtain ⟨hi, hn⟩ := endpointA_branch_index D c r hr i k hw he
      refine ⟨hi, ?_⟩
      rw [← hi, hn]
      simp [normalVector, endpointASet, ht]
  · intro k hk
    have hw : weight c k ≠ 0 := by intro h; simp [supportedCoefficient, h] at hk
    have hp : rowCoefficient D (r k) (.aProduct i j) < 0 := by
      simpa [supportedCoefficient, hw] using hk
    rcases row_aProduct_negative D (r k) i j hp with ⟨he, ht⟩ | ⟨he, ht⟩ | ⟨he, ht⟩
    · left
      apply normal_negative_singleton_index k j
      simpa [he, ReductionData.rowNormal, ht] using hr k hw
    · left
      apply normal_negative_singleton_index k j
      simpa [he, ReductionData.rowNormal, ht] using hr k hw
    · right
      obtain ⟨hi, hn⟩ := endpointB_branch_index D c r hr i k hw he
      refine ⟨hi, ?_⟩
      rw [← hi, hn]
      have hnot : D.c i j.succ ≠ .bOnly := by rcases ht with ht | ht <;> simp [ht]
      simp [normalVector, endpointBSet, hnot]

theorem threeBranch_bProduct_unit (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (hr : ThreeBranch D c r) (i : I) (j : Fin 3) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) (.bProduct i j) ∧
      (∑ k, weight c k * rowCoefficient D (r k) (.bProduct i j)) ≤ 1 := by
  rw [← supportedCoefficient_sum D c r (.bProduct i j)]
  apply signed_occurrence_sum_unit c j (subsetIndex (endpointBSet D i))
    (subsetIndex (endpointASet D i))
  · intro k
    by_cases h : weight c k = 0
    · simp [supportedCoefficient, h]
    · simpa [supportedCoefficient, h] using row_bProduct_bounds D (r k) i j
  · intro k hk
    have hw : weight c k ≠ 0 := by intro h; simp [supportedCoefficient, h] at hk
    have hp : 0 < rowCoefficient D (r k) (.bProduct i j) := by
      simpa [supportedCoefficient, hw] using hk
    rcases row_bProduct_positive D (r k) i j hp with ⟨he, ht⟩ | ⟨he, ht⟩
    · left
      apply normal_singleton_index k j
      have hn := hr k hw
      simpa [he, ReductionData.rowNormal, ht] using hn
    · right
      obtain ⟨hi, hn⟩ := endpointB_branch_index D c r hr i k hw he
      refine ⟨hi, ?_⟩
      rw [← hi, hn]
      simp [normalVector, endpointBSet, ht]
  · intro k hk
    have hw : weight c k ≠ 0 := by intro h; simp [supportedCoefficient, h] at hk
    have hp : rowCoefficient D (r k) (.bProduct i j) < 0 := by
      simpa [supportedCoefficient, hw] using hk
    rcases row_bProduct_negative D (r k) i j hp with ⟨he, ht⟩ | ⟨he, ht⟩ | ⟨he, ht⟩
    · left
      apply normal_negative_singleton_index k j
      simpa [he, ReductionData.rowNormal, ht] using hr k hw
    · left
      apply normal_negative_singleton_index k j
      simpa [he, ReductionData.rowNormal, ht] using hr k hw
    · right
      obtain ⟨hi, hn⟩ := endpointA_branch_index D c r hr i k hw he
      refine ⟨hi, ?_⟩
      rw [← hi, hn]
      have hnot : ¬ observesA (D.c i j.succ) := by simp [ht, observesA]
      simp [normalVector, endpointASet, hnot]

theorem threeBranch_bypassProduct_unit (D : ReductionData 3 I) (c : Fin 16)
    (r : Fin 11 → ProfileRow 3 I) (hr : ThreeBranch D c r) (j : Fin 3) :
    -1 ≤ ∑ k, weight c k * rowCoefficient D (r k) (.bypassProduct j) ∧
      (∑ k, weight c k * rowCoefficient D (r k) (.bypassProduct j)) ≤ 1 := by
  have hh := signed_occurrence_sum_unit c j 0 0
    (fun k => -supportedCoefficient D c r (.bypassProduct j) k)
  have hf : ∀ k, -1 ≤ -supportedCoefficient D c r (.bypassProduct j) k ∧
      -supportedCoefficient D c r (.bypassProduct j) k ≤ 1 := by
    intro k
    by_cases h : weight c k = 0
    · simp [supportedCoefficient, h]
    · have h' := row_bypassProduct_bounds D (r k) j
      simp only [supportedCoefficient, h, if_false]
      omega
  have hp : ∀ k, 0 < -supportedCoefficient D c r (.bypassProduct j) k →
      k = singletonIndex j ∨ k = positiveIndex 0 ∧ normal (positiveIndex 0) j = 1 := by
    intro k hk
    have hw : weight c k ≠ 0 := by intro h; simp [supportedCoefficient, h] at hk
    have hs : rowCoefficient D (r k) (.bypassProduct j) < 0 := by
      simpa [supportedCoefficient, hw] using hk
    have he := row_bypassProduct_negative D (r k) j hs
    have hn := hr k hw
    by_cases ho : D.observedH j.succ = true
    · left
      apply normal_singleton_index k j
      simpa [he, ReductionData.rowNormal, ho] using hn
    · have hz : normal k = 0 := by
        simpa [he, ReductionData.rowNormal, ho, normalVector_empty] using hn.symm
      exact False.elim (normal_nonzero k hz)
  have hn : ∀ k, -supportedCoefficient D c r (.bypassProduct j) k < 0 →
      k = negativeSingletonIndex j ∨ k = positiveIndex 0 ∧ normal (positiveIndex 0) j = 0 := by
    intro k hk
    have hw : weight c k ≠ 0 := by intro h; simp [supportedCoefficient, h] at hk
    have hs : 0 < rowCoefficient D (r k) (.bypassProduct j) := by
      simpa [supportedCoefficient, hw] using hk
    have he := row_bypassProduct_positive D (r k) j hs
    have hn := hr k hw
    by_cases ho : D.observedH j.succ = true
    · left
      apply normal_negative_singleton_index k j
      simpa [he, ReductionData.rowNormal, ho] using hn
    · have hz : normal k = 0 := by
        simpa [he, ReductionData.rowNormal, ho, normalVector_empty] using hn.symm
      exact False.elim (normal_nonzero k hz)
  obtain ⟨hl, hu⟩ := hh hf hp hn
  simp only [mul_neg, Finset.sum_neg_distrib, supportedCoefficient_sum] at hl hu
  omega

end NetworkSimplex.Chain.Threshold
