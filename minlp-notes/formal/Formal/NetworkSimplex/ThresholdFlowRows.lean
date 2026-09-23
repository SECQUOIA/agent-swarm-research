import Formal.NetworkSimplex.ThresholdRowOccurrences
import Formal.NetworkSimplex.ThresholdClassification

/-! Source-row identification and elementary flow facts for the bypass repairs. -/
namespace NetworkSimplex.Chain.Threshold
variable {I : Type*}
open ThreeStateCircuits

-- Row inversion deliberately simplifies constructor cases before splitting their tests.

set_option linter.flexible false in
/-- The negative full normal is supplied only by the residual-state lower bound. -/
theorem row_negative_full (D : ReductionData 3 I) (r : ProfileRow 3 I)
    (h : normalVector (D.rowNormal r) = normal 10) : r = .totalLower := by
  cases r <;> (try rfl)
  all_goals
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    simp only [ReductionData.rowNormal] at h0 h1
    (try split_ifs at h0 h1) <;>
      simp_all [normalVector, normal] <;> (try split_ifs at *) <;> omega

set_option linter.flexible false in
/-- A negative bypass coefficient at a singleton normal must be an actual upper endpoint. -/
theorem singleton_negative_bypass_endpoint [DecidableEq I]
    (D : ReductionData 3 I) (r : ProfileRow 3 I)
    (j : Fin 3) (h : normalVector (D.rowNormal r) = normal (singletonIndex j))
    (hb : rowCoefficient D r .bypassFlow = -1) : ∃ i, r = .endpointA i := by
  rw [row_bypassFlow_coefficient] at hb
  cases r <;> (try solve | simp_all [negativeBypassRow])
  · have hh := congrFun h j
    have hk : ∃ k : Fin 3, k ≠ j := by fin_cases j <;> decide
    obtain ⟨k, hk⟩ := hk
    have hh' := congrFun h k
    fin_cases j <;> fin_cases k <;>
      simp_all [singletonIndex, normal, normalVector, ReductionData.rowNormal]

set_option linter.flexible false in
/-- A zero bypass coefficient at a pair normal must be an actual lower endpoint. -/
theorem pair_zero_bypass_endpoint [DecidableEq I] (D : ReductionData 3 I) (r : ProfileRow 3 I)
    (j : Fin 3) (h : normalVector (D.rowNormal r) = normal ⟨3 + j.val, by omega⟩)
    (hb : rowCoefficient D r .bypassFlow = 0) : ∃ i, r = .endpointB i := by
  cases r <;> (try exact ⟨_, rfl⟩)
  all_goals
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    have h2 := congrFun h 2
    simp only [row_bypassFlow_coefficient, negativeBypassRow] at hb
    simp only [ReductionData.rowNormal] at h0 h1 h2
    fin_cases j <;> (try split_ifs at h0 h1 h2) <;>
      simp_all [normalVector, normal] <;> (try split_ifs at *) <;> (try simp_all) <;> omega

/-- Two participating normals cannot be supplied by the very same source row. -/
theorem ThreeBranch.row_injective (D : ReductionData 3 I) {c : Fin 16}
    {r : Fin 11 → ProfileRow 3 I} (h : ThreeBranch D c r) {i j : Fin 11}
    (hi : weight c i ≠ 0) (hj : weight c j ≠ 0) (he : r i = r j) : i = j := by
  apply normal_injective
  rw [← h i hi, ← h j hj, he]

/-- A positive subset normal never uses the negative-full source row. -/
theorem positive_row_not_totalLower (D : ReductionData 3 I) (r : ProfileRow 3 I) (e : Fin 7)
    (h : normalVector (D.rowNormal r) = normal (positiveIndex e)) : r ≠ .totalLower := by
  intro he
  subst r
  have hh := congrFun h 0
  fin_cases e <;> norm_num [normalVector, normal, positiveIndex, ReductionData.rowNormal] at hh

set_option linter.flexible false in
/-- Negative singleton rows have no bypass-flow occurrence. -/
theorem negative_singleton_bypass_zero [DecidableEq I]
    (D : ReductionData 3 I) (r : ProfileRow 3 I) (j : Fin 3)
    (h : normalVector (D.rowNormal r) = normal (negativeSingletonIndex j)) :
    rowCoefficient D r .bypassFlow = 0 := by
  cases r <;>
    (try solve | simp [row_bypassFlow_coefficient, negativeBypassRow])
  all_goals
    have h0 := congrFun h 0
    have h1 := congrFun h 1
    have h2 := congrFun h 2
    fin_cases j <;> simp_all [normalVector, normal, negativeSingletonIndex,
      ReductionData.rowNormal] <;> (try split_ifs at *)

end NetworkSimplex.Chain.Threshold
