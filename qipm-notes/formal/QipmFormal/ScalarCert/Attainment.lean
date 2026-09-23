import QipmFormal.ScalarCert.XLocalization

/-!
# Attainment of the scalar-dilation supremum

The ratio is continuous on `(0,1)`.  Its values above the certified lower
bound lie inside the compact interval `[4611/5000,9701/10000]`, and the
strict lower witness belongs to that interval.  The maximum on the compact
interval therefore bounds the ratio on all of `(0,1)` and equals `cstar`.
-/

namespace QipmFormal.ScalarCert

open Real Set

/-- The explicit inverse of `P` is continuous, including at zero. -/
theorem Pinv_continuous : Continuous Pinv := by
  unfold Pinv
  exact (continuous_const.sub
    ((continuous_const.add (continuous_id.pow 2)).sqrt.inv₀
      (fun y => (sqrt_one_add_sq_pos y).ne'))).sqrt

/-- `A` is continuous wherever `|v| < 1`. -/
theorem A_continuousAt {v : ℝ} (hv : |v| < 1) : ContinuousAt A v := by
  unfold A
  exact (continuousAt_const.sub (continuousAt_id.pow 2)).sqrt.div
    (continuousAt_const.sub (continuousAt_id.pow 2)) (one_sub_sq_pos hv).ne'

/-- The dilation ratio is continuous at every point of `(0,1)`. -/
theorem ratio_continuousAt {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    ContinuousAt ratio v := by
  have hv : |v| < 1 := by rwa [abs_of_pos hv0]
  have hY : ContinuousAt Y v := (Y_deriv hv).continuousAt
  have hW : ContinuousAt W v :=
    Pinv_continuous.continuousAt.comp (hY.mul (A_continuousAt hv))
  have hWmem := W_mem hv0 hv1
  have hWabs : |W v| < 1 := by
    rw [abs_of_nonneg hWmem.1]
    exact hWmem.2
  exact ((Y_deriv hWabs).continuousAt.comp hW).div hY (Y_pos hv0 hv1).ne'

/-- Continuity on the full domain of the scalar-dilation supremum. -/
theorem ratio_continuousOn : ContinuousOn ratio (Ioo (0 : ℝ) 1) :=
  fun _ hv => (ratio_continuousAt hv.1 hv.2).continuousWithinAt

/-- The supremum defining `cstar` is attained at an interior point. -/
theorem cstar_attained : ∃ v ∈ Ioo (0 : ℝ) 1, ratio v = cstar := by
  have hsub : Icc ((4611 : ℝ) / 5000) (9701 / 10000) ⊆ Ioo (0 : ℝ) 1 := by
    intro v hv
    constructor <;> linarith [hv.1, hv.2]
  have hv0window := maximizer_localization v0_pos v0_lt_one a0_lt_ratio_v0
  have hv0mem : v0 ∈ Icc ((4611 : ℝ) / 5000) (9701 / 10000) :=
    ⟨hv0window.1.le, hv0window.2.le⟩
  obtain ⟨v, hv, hmax⟩ := isCompact_Icc.exists_isMaxOn ⟨v0, hv0mem⟩
    (ratio_continuousOn.mono hsub)
  have hvdom : v ∈ Ioo (0 : ℝ) 1 := hsub hv
  have hthreshold : (68743 : ℝ) / 50000 < ratio v :=
    lt_of_lt_of_le a0_lt_ratio_v0 (hmax hv0mem)
  have hglobal : ∀ w ∈ Ioo (0 : ℝ) 1, ratio w ≤ ratio v := by
    intro w hw
    by_cases h : (68743 : ℝ) / 50000 < ratio w
    · obtain ⟨hlo, hhi⟩ := maximizer_localization hw.1 hw.2 h
      exact hmax ⟨hlo.le, hhi.le⟩
    · exact (not_lt.mp h).trans hthreshold.le
  refine ⟨v, hvdom, le_antisymm ?_ ?_⟩
  · exact le_csSup bddAbove_ratio ⟨v, hvdom, rfl⟩
  · apply csSup_le (s := ratio '' Ioo (0 : ℝ) 1) ⟨ratio v, ⟨v, hvdom, rfl⟩⟩
    rintro y ⟨w, hw, rfl⟩
    exact hglobal w hw

/-- Every point attaining `cstar` lies in the certified interval in both coordinates. -/
theorem cstar_location_of_eq {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1)
    (h : ratio v = cstar) :
    (4611 : ℝ) / 5000 < v ∧ v < (9701 : ℝ) / 10000 ∧
      (43 : ℝ) / 50 < xOf v ∧ xOf v < (943 : ℝ) / 1000 := by
  apply cstar_maximizer_location hv0 hv1
  rw [h]
  exact cstar_bounds.1

end QipmFormal.ScalarCert
