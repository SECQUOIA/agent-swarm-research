import Mathlib

/-! Upper-tail thresholds, including atoms and endpoint masses. -/
namespace ReciprocalAnchor.ManyLeaf
open MeasureTheory Set Filter ProbabilityTheory Function
open scoped Topology

/-- Every prescribed probability mass has an upper-tail threshold. An atom at
that threshold can be split to obtain exactly the prescribed mass. -/
theorem probability_upper_tail_threshold (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    ∃ s ∈ Icc a b, μ.real (Ioi s) ≤ q ∧ q ≤ μ.real (Ici s) := by
  have hb : cdf μ b = 1 := by
    rw [cdf_eq_real]
    calc
      μ.real (Iic b) = μ.real univ := measureReal_congr (by
        filter_upwards [h] with x hx
        apply propext
        change (x ≤ b ↔ True)
        exact iff_true_intro hx.2)
      _ = 1 := by simp
  have ha : ∀ x < a, cdf μ x = 0 := by
    intro x hx
    rw [cdf_eq_real, measureReal_def]
    have hz : μ (Iic x) = 0 := measure_eq_zero_iff_ae_notMem.mpr (by
      filter_upwards [h] with y hy
      simp only [mem_Iic]
      linarith [hy.1])
    simp [hz]
  let A : Set ℝ := {x | x ∈ Icc a b ∧ 1 - q ≤ cdf μ x}
  have hbA : b ∈ A := ⟨⟨hab, le_rfl⟩, by rw [hb]; linarith [hq.1]⟩
  have hne : A.Nonempty := ⟨b, hbA⟩
  have hbd : BddBelow A := ⟨a, fun x hx => hx.1.1⟩
  let s := sInf A
  have hsa : a ≤ s := le_csInf hne (fun x hx => hx.1.1)
  have hsb : s ≤ b := csInf_le hbd hbA
  have hleft : leftLim (cdf μ) s ≤ 1 - q := by
    apply le_of_tendsto ((monotone_cdf μ).tendsto_leftLim s)
    filter_upwards [self_mem_nhdsWithin] with x hx
    change x < s at hx
    by_cases hxa : x < a
    · rw [ha x hxa]
      linarith [hq.2]
    · have hxb : x ≤ b := le_trans (le_of_lt hx) hsb
      by_contra hn
      have hxA : x ∈ A := ⟨⟨le_of_not_gt hxa, hxb⟩, le_of_lt (lt_of_not_ge hn)⟩
      exact (not_le_of_gt hx) (csInf_le hbd hxA)
  have hright : 1 - q ≤ cdf μ s := by
    apply ge_of_tendsto (((cdf μ).right_continuous s).mono Ioi_subset_Ici_self)
    filter_upwards [self_mem_nhdsWithin] with x hx
    change s < x at hx
    obtain ⟨y, hy, hyx⟩ := exists_lt_of_csInf_lt hne hx
    exact hy.2.trans ((monotone_cdf μ) hyx.le)
  refine ⟨s, ⟨hsa, hsb⟩, ?_, ?_⟩
  · rw [measureReal_def, ← measure_cdf μ,
      (cdf μ).measure_Ioi (tendsto_cdf_atTop μ), ENNReal.toReal_ofReal]
    · linarith
    · exact sub_nonneg.mpr (cdf_le_one μ s)
  · rw [measureReal_def, ← measure_cdf μ,
      (cdf μ).measure_Ici (tendsto_cdf_atTop μ), ENNReal.toReal_ofReal]
    · linarith
    · linarith [hq.1]

end ReciprocalAnchor.ManyLeaf
