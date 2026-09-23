import Formal.MultilinearGap.StructuralFrequencyCycle

/-! Actual scalar graph-hull and termwise gaps on every odd cycle. -/
namespace MultilinearGap.StructuralFrequencyCycle
open CubicGap
noncomputable section

/-- Every coordinate is strictly interior. -/
def meanPoint (k : ℕ) : Cycle k → ℝ := fun _ => 1 / 2

theorem meanPoint_mem_cube (k : ℕ) : meanPoint k ∈ cube (Cycle k) := by
  intro i
  norm_num [meanPoint]

@[simp] theorem complement_meanPoint (k : ℕ) : failureComplement (meanPoint k) = meanPoint k := by
  funext i
  norm_num [failureComplement, meanPoint]

/-- The polynomial whose factors are the adjacent pairs on the cycle. -/
def polynomial (k : ℕ) : (Cycle k → ℝ) → ℝ := supportPolynomial (supports k) (fun _ => 1)

theorem baseline_support (k : ℕ) (v : Cycle k) :
    failureBaseline (support k v) (meanPoint k) = 1 / 2 := by
  rw [failureBaseline, complement_meanPoint,
    monomialUpper_eq_anchor (support k v) (meanPoint k) v (by simp [support])
      (fun _ _ => le_rfl)]
  norm_num [meanPoint]

theorem shiftedCoverage_cycle (k : ℕ) (μ : Law (Vertex (Cycle k))) :
    shiftedCoverage (supports k) (fun _ => 1) (meanPoint k) μ =
      μ.expect (fun f => ∑ v, covered f v) - (2 * (k : ℝ) + 3) / 2 := by
  unfold shiftedCoverage
  rw [sum_supports]
  have he (v : Cycle k) : failureCovered (support k v) = fun f => covered f v := by
    funext f
    exact failureCovered_support k f v
  simp only [one_mul, baseline_support, he,
    Finset.sum_sub_distrib, Finset.sum_const, Finset.card_univ, Fintype.card_fin,
    nsmul_eq_mul, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat, Law.expect_sum]
  ring

/-- The exact hull gap is `(L-1)/2`, attained by explicit finite rounding. -/
theorem polynomial_hullGap (k : ℕ) :
    hullGap (polynomial k) (meanPoint k) = (k : ℝ) + 1 := by
  have hgreat := hullGap_isGreatest_shiftedCoverage (supports k) (fun _ => 1)
    (fun _ _ => zero_le_one) (meanPoint k) (meanPoint_mem_cube k)
  rw [complement_meanPoint] at hgreat
  apply le_antisymm
  · obtain ⟨μ, hm, hv⟩ := hgreat.1
    have hbound := expected_coverage_le k μ hm
    rw [shiftedCoverage_cycle] at hv
    change hullGap (polynomial k) (meanPoint k) = _ at hv
    linarith
  · have hround : HasMeans (roundingLaw k) (meanPoint k) := roundingLaw_mean k
    have hbound := hgreat.2 ⟨roundingLaw k, hround, rfl⟩
    rw [shiftedCoverage_cycle, roundingLaw_total_coverage] at hbound
    change _ ≤ hullGap (polynomial k) (meanPoint k) at hbound
    linarith

/-- The sum of the actual individual monomial widths is `L/2`. -/
theorem polynomial_termwiseGap (k : ℕ) :
    weightedTermwiseGap (supports k) (fun _ => 1) (meanPoint k) =
      (2 * (k : ℝ) + 3) / 2 := by
  unfold weightedTermwiseGap
  rw [sum_supports]
  have hterm (v : Cycle k) : hullGap (monomial (support k v)) (meanPoint k) = 1 / 2 := by
    rw [monomial_hullGap_of_min_coordinate _ _ (meanPoint_mem_cube k) v
      (by simp [support]) (fun _ _ => le_rfl)]
    have hs : (∑ i ∈ support k v, meanPoint k i) = 1 := by
      simp [meanPoint, support_card]
    rw [hs, support_card]
    norm_num [meanPoint]
  simp only [one_mul, hterm, Finset.sum_const, Finset.card_univ,
    Fintype.card_fin, nsmul_eq_mul, Nat.cast_add, Nat.cast_mul, Nat.cast_ofNat]
  ring

/-- Every odd-cycle constant is attained by the actual polynomial graph hull. -/
theorem polynomial_ratio (k : ℕ) :
    weightedTermwiseGap (supports k) (fun _ => 1) (meanPoint k) /
      hullGap (polynomial k) (meanPoint k) =
      (2 * (k : ℝ) + 3) / (2 * (k : ℝ) + 2) := by
  rw [polynomial_hullGap, polynomial_termwiseGap]
  have hk : (k : ℝ) + 1 ≠ 0 := by positivity
  have hk' : 2 * (k : ℝ) + 2 ≠ 0 := by positivity
  field_simp

/-- The triangle supplies the sharp three-halves example in the frequency-two class. -/
theorem triangle_ratio : FrequencyTwo (supports 0) ∧
    weightedTermwiseGap (supports 0) (fun _ => 1) (meanPoint 0) /
      hullGap (polynomial 0) (meanPoint 0) = 3 / 2 := by
  exact ⟨frequencyTwo_supports 0, by simpa using polynomial_ratio 0⟩

end
end MultilinearGap.StructuralFrequencyCycle
