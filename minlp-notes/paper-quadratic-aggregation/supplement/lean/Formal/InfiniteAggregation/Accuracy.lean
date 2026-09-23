import Formal.InfiniteAggregation.AccuracyUpper
import Formal.InfiniteAggregation.AccuracyLower
import Formal.InfiniteAggregation.AccuracyRate

/-! Optimal approximation error and constructive tolerance budgets. -/

open Filter Asymptotics

namespace InfiniteAggregation

theorem optimalError_le_upper {r N : ℕ} (hr : 2 ≤ r) (hN : 2 ≤ N) :
    optimalError r N ≤ ENNReal.ofReal (accuracyUpperBound N) :=
  (optimalError_le_family (angleCuts_admissible hr hN) (card_angleCuts_le N)).trans
    (hausdorffError_angleCuts_le hr hN)

/-- The source's exact two-sided constants hold for the infimum without attainment. -/
theorem optimalError_bounds {r N : ℕ} (hr : 2 ≤ r) (hN : 2 ≤ N) :
    ENNReal.ofReal (accuracyLowerBound N) ≤ optimalError r N ∧
      optimalError r N ≤ ENNReal.ofReal (accuracyUpperBound N) :=
  ⟨accuracy_lower_le_optimalError hr (by omega), optimalError_le_upper hr hN⟩

theorem optimalError_ne_top {r N : ℕ} (hr : 2 ≤ r) (hN : 2 ≤ N) :
    optimalError r N ≠ ⊤ :=
  ne_top_of_le_ne_top ENNReal.ofReal_ne_top (optimalError_le_upper hr hN)

theorem optimalError_toReal_bounds {r N : ℕ} (hr : 2 ≤ r) (hN : 2 ≤ N) :
    accuracyLowerBound N ≤ (optimalError r N).toReal ∧
      (optimalError r N).toReal ≤ accuracyUpperBound N := by
  obtain ⟨hl, hu⟩ := optimalError_bounds hr hN
  exact ⟨(ENNReal.ofReal_le_iff_le_toReal (optimalError_ne_top hr hN)).1 hl,
    ENNReal.toReal_le_of_le_ofReal (by unfold accuracyUpperBound; positivity) hu⟩

theorem optimalError_theta {r : ℕ} (hr : 2 ≤ r) :
    (fun N => (optimalError r N).toReal) =Θ[atTop]
      (fun N : ℕ => (1 : ℝ) / (N : ℝ) ^ 2) :=
  inverse_square_theta (fun N hN => (optimalError_toReal_bounds (N := N) hr hN).1)
    (fun N hN => (optimalError_toReal_bounds (N := N) hr hN).2)

/-- Tolerance sufficiency constructs a concrete family; it does not use infimum attainment. -/
theorem exists_family_for_tolerance {r : ℕ} (hr : 2 ≤ r) {ε : ℝ} (hε : 0 < ε) :
    ∃ W : Finset Weight, admissibleFamily r W ∧ W.card ≤ accuracyBudget ε ∧
      hausdorffError r W ≤ ENNReal.ofReal ε := by
  refine ⟨angleCuts (accuracyBudget ε), angleCuts_admissible hr (accuracyBudget_ge_two hε),
    card_angleCuts_le _, ?_⟩
  exact (hausdorffError_angleCuts_le hr (accuracyBudget_ge_two hε)).trans
    (ENNReal.ofReal_le_ofReal (accuracyBudget_upper hε))

/-- Any admissible family satisfying a tolerance obeys the necessary budget. -/
theorem necessary_family_budget {r N : ℕ} (hr : 2 ≤ r) (hN : 1 ≤ N)
    (W : Finset Weight) (hW : admissibleFamily r W) (hcard : W.card ≤ N)
    {ε : ℝ} (hε : 0 < ε) (herr : hausdorffError r W ≤ ENNReal.ofReal ε) :
    Real.sqrt ((Real.sqrt 2 * (Real.log 2) ^ 2 / 1600) / ε) ≤ N := by
  apply accuracyLowerBound_budget (by omega) hε
  have h := (accuracy_lower_le_hausdorffError hr hN W hW hcard).trans herr
  exact (ENNReal.ofReal_le_ofReal_iff hε.le).1 h

end InfiniteAggregation
