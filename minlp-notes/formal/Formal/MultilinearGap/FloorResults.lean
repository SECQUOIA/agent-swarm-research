import Formal.MultilinearGap.FloorDomain
import Formal.MultilinearGap.FloorUpper
import Formal.MultilinearGap.FloorAsymptotics
import Formal.MultilinearGap.FloorLower

/-! Complete finite and sharp asymptotic marginal-floor results for actual
graph-hull gaps, with the two-sided strip and original-box transfer. -/

namespace MultilinearGap

open CubicGap Filter Real
open scoped Topology
noncomputable section

/-- The parameters in the source note give a uniform bound without a degree limit. -/
theorem floor_finite_bound {δ : ℝ} (hδ : 0 < δ) :
    CubeFloorBound δ (floorUpper δ) := by
  intro I hI hEq S a x ha hx hf
  have he : 0 < 1 / (floorB δ)^2 := by positivity [floorB_pos δ]
  have hτδ : floorTau δ / δ ≤ 1 / (floorB δ)^2 := by
    unfold floorTau
    apply le_of_eq
    field_simp
  simpa only [floorBound, floorUpper, floorL, floorLog, easyConstant] using
    floor_cube_gap_bound S a ha x hx δ hδ (floorTau δ) (floorTau_pos hδ)
      (1 / (floorB δ)^2) he hf hτδ

/-- Nonemptiness and boundedness are proved before taking the real supremum. -/
theorem floorSupremum_le_upper {δ : ℝ} (hδ : 0 < δ) (hδ1 : δ < 1) :
    floorSupremum δ ≤ floorUpper δ :=
  csSup_le (floorRatios_nonempty hδ hδ1) (fun _ hr => floorRatios_le (floor_finite_bound hδ) hr)

theorem floorSupremum_antitoneOn : AntitoneOn floorSupremum (Set.Ioo (0 : ℝ) 1) := by
  intro δ hδ ε hε hδε
  apply csSup_le (floorRatios_nonempty hε.1 hε.2)
  intro r hr
  exact le_csSup (floorRatios_bddAbove (floor_finite_bound hδ.1))
    (floorRatios_antitone hδε hr)

/-- The source's monotonicity extension above a floor of one half. -/
theorem floorSupremum_le_half {δ : ℝ} (hδ : 1 / 2 ≤ δ) (hδ1 : δ < 1) :
    floorSupremum δ ≤ floorSupremum (1 / 2) :=
  floorSupremum_antitoneOn (by norm_num) ⟨by linarith, hδ1⟩ hδ

/-- An actual unit-coefficient dyadic polynomial witnesses both floor constraints. -/
theorem floor_witness_mem_stripRatios {δ : ℝ} (hδ : 0 < δ) (hsmall : δ ≤ 1 / 4) :
    termwiseGap (supports (floorLevels δ)) (means (floorLevels δ)) /
      hullGap (polynomial (floorLevels δ)) (means (floorLevels δ)) ∈ stripRatios δ := by
  refine ⟨Coord (floorLevels δ), inferInstance, inferInstance,
    supports (floorLevels δ), fun _ => 1, means (floorLevels δ),
    by simp, means_mem_cube _, means_floor_strip hδ hsmall, ?_, ?_⟩
  · rw [← polynomial_eq_supportPolynomial]
    exact hullGap_positive _ (floorLevels_ge_two hδ hsmall)
  · rw [← polynomial_eq_supportPolynomial]
    simp [weightedTermwiseGap, termwiseGap]

/-- Finite lower and upper bounds on both supremum functions. -/
theorem floor_suprema_bounds {δ : ℝ} (hδ : 0 < δ) (hsmall : δ ≤ 1 / 4) :
    floorLower δ ≤ stripSupremum δ ∧ stripSupremum δ ≤ floorSupremum δ ∧
      floorSupremum δ ≤ floorUpper δ := by
  have hbd := floorRatios_bddAbove (floor_finite_bound hδ)
  have hbs := hbd.mono (stripRatios_subset_floorRatios δ)
  refine ⟨?_, ?_, floorSupremum_le_upper hδ (by linarith)⟩
  · exact (floorLower_le_ratio hδ hsmall).trans
      (le_csSup hbs (floor_witness_mem_stripRatios hδ hsmall))
  · apply csSup_le (stripRatios_nonempty (by linarith))
    intro r hr
    exact le_csSup hbd (stripRatios_subset_floorRatios δ hr)

private theorem floor_normalized_squeeze (f : ℝ → ℝ)
    (hbound : ∀ δ, 0 < δ → δ ≤ 1 / 4 → floorLower δ ≤ f δ ∧ f δ ≤ floorUpper δ) :
    Tendsto (fun δ => f δ / (log (1 / δ) / log (log (1 / δ))))
      (𝓝[>] 0) (𝓝 1) := by
  have hsmall : ∀ᶠ δ : ℝ in 𝓝[>] 0, δ ≤ 1 / 4 :=
    (eventually_le_nhds (by norm_num : (0 : ℝ) < 1 / 4)).filter_mono nhdsWithin_le_nhds
  have hscale : ∀ᶠ δ : ℝ in 𝓝[>] 0,
      0 < log (1 / δ) / log (log (1 / δ)) := by
    filter_upwards [tendsto_floor_base.eventually (eventually_gt_atTop (1 : ℝ))] with δ h
    exact div_pos (by linarith) (log_pos h)
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le'
    tendsto_floorLower_normalized tendsto_floorUpper_normalized
  · filter_upwards [self_mem_nhdsWithin, hsmall, hscale] with δ hδ hs hp
    exact div_le_div_of_nonneg_right (hbound δ hδ hs).1 hp.le
  · filter_upwards [self_mem_nhdsWithin, hsmall, hscale] with δ hδ hs hp
    exact div_le_div_of_nonneg_right (hbound δ hδ hs).2 hp.le

/-- The worst ratio over every dimension and degree has sharp leading constant one. -/
theorem floorSupremum_asymptotic :
    Tendsto (fun δ => floorSupremum δ / (log (1 / δ) / log (log (1 / δ))))
      (𝓝[>] 0) (𝓝 1) := by
  apply floor_normalized_squeeze
  intro δ hδ hs
  have h := floor_suprema_bounds hδ hs
  exact ⟨h.1.trans h.2.1, h.2.2⟩

/-- Constraining means also below `1-δ` leaves the leading constant unchanged. -/
theorem stripSupremum_asymptotic :
    Tendsto (fun δ => stripSupremum δ / (log (1 / δ) / log (log (1 / δ))))
      (𝓝[>] 0) (𝓝 1) := by
  apply floor_normalized_squeeze
  intro δ hδ hs
  have h := floor_suprema_bounds hδ hs
  exact ⟨h.1, h.2.1.trans h.2.2⟩

/-- Both asymptotics use the real positive-floor limit, not just dyadic floors. -/
theorem sharp_marginal_floor_growth :
    Tendsto (fun δ => floorSupremum δ / (log (1 / δ) / log (log (1 / δ))))
      (𝓝[>] 0) (𝓝 1) ∧
    Tendsto (fun δ => stripSupremum δ / (log (1 / δ) / log (log (1 / δ))))
      (𝓝[>] 0) (𝓝 1) :=
  ⟨floorSupremum_asymptotic, stripSupremum_asymptotic⟩

/-- The same finite bound concerns the original monomials on any nonnegative box. -/
theorem marginal_floor_original_box_bound {I : Type} [Finite I]
    {δ : ℝ} (hδ : 0 < δ) (hδ1 : δ ≤ 1)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u)
    (hf : ∀ i, l i ≠ u i → δ ≤ (x i - l i) / (u i - l i)) :
    boxTermwiseGap S a l u x ≤ floorUpper δ * boxHullGap l u (supportPolynomial S a) x := by
  classical
  let _ := Fintype.ofFinite I
  exact floor_gap_bound_on_box δ (floorUpper δ) hδ.le hδ1
    (fun S a ha p hp hf => floor_finite_bound hδ I S a p ha hp hf)
    S a ha l u hl hlu x hx hf

end
end MultilinearGap
