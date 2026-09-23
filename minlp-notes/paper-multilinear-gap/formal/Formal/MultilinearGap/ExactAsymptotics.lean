import Formal.MultilinearGap.ExactResults
import Formal.MultilinearGap.LowerAsymptotics

/-! Bounded logarithmic error and the normalized ratio for the exact dyadic family. -/
namespace MultilinearGap
open CubicGap Filter Real
open scoped Topology
noncomputable section

/-- The nonintegral remainder in the exact formula is nonnegative and below two. -/
theorem exact_cutoff_remainder_bounds (L s : ℕ) (hsL : s ≤ L)
    (hlo : cutoffBudget L (s + 1) ≤ 1) :
    0 ≤ ((L : ℝ) - s) / 2^s ∧ ((L : ℝ) - s) / 2^s < 2 := by
  have hp : (0 : ℝ) < 2^s := by positivity
  constructor
  · exact div_nonneg (sub_nonneg.mpr (by exact_mod_cast hsL)) hp.le
  · apply (div_lt_iff₀ hp).mpr
    have h := (div_le_one (by positivity : 0 < (2 : ℝ)^(s+1))).mp hlo
    simp only [Nat.cast_add, Nat.cast_one, pow_succ] at h
    linarith

/-- Every admissible cutoff is within two of the base-two logarithm. -/
theorem exact_cutoff_log_bounds (L s : ℕ) (hL : 2 ≤ L) (hs1 : 1 ≤ s)
    (hlo : cutoffBudget L (s + 1) ≤ 1) (hhi : 1 ≤ cutoffBudget L s) :
    logb 2 L - 2 ≤ (s : ℝ) ∧ (s : ℝ) ≤ logb 2 L + 1 := by
  have hpow : (s : ℝ) ≤ (2 : ℝ) ^ s := by
    exact_mod_cast (Nat.lt_two_pow_self (n := s)).le
  have hlow : (L : ℝ) - s + 1 ≤ (2 : ℝ)^s * 2 := by
    have h := (div_le_one (by positivity : 0 < (2 : ℝ)^(s+1))).mp hlo
    simp only [Nat.cast_add, Nat.cast_one, pow_succ] at h
    linarith
  have hhigh : (2 : ℝ)^s ≤ (L : ℝ) - s + 2 := by
    exact (one_le_div (by positivity)).mp hhi
  have hLpos : (0 : ℝ) < L := by exact_mod_cast (show 0 < L by omega)
  have hsreal : (1 : ℝ) ≤ s := by exact_mod_cast hs1
  constructor
  · have hb : (L : ℝ) ≤ (2 : ℝ)^(s+2) := by
      simp only [pow_add]
      norm_num
      nlinarith [pow_pos (by norm_num : (0 : ℝ) < 2) s]
    have hlog := logb_le_logb_of_le (by norm_num : (1 : ℝ) < 2) hLpos hb
    simp [logb_pow] at hlog
    linarith
  · have hb : (2 : ℝ)^s ≤ 2 * (L : ℝ) := by
      have hLreal : (2 : ℝ) ≤ L := by exact_mod_cast hL
      linarith
    have hlog := logb_le_logb_of_le (by norm_num : (1 : ℝ) < 2)
      (by positivity : (0 : ℝ) < 2^s) hb
    rw [logb_pow, logb_mul (by norm_num) hLpos.ne'] at hlog
    simpa [add_comm] using hlog

/-- An explicit bounded-error version of `H_L = log₂ L + O(1)`. -/
theorem hullGap_log_bounds (L : ℕ) (hL : 2 ≤ L) :
    logb 2 L - 2 ≤ hullGap (polynomial L) (means L) ∧
      hullGap (polynomial L) (means L) ≤ logb 2 L + 3 := by
  refine ⟨?_, hullGap_le_logb_add_three L hL⟩
  obtain ⟨s, hs1, hsL, hlo, hhi, heq⟩ := exists_hullGap_exact L hL
  have hs := (exact_cutoff_log_bounds L s hL hs1 hlo hhi).1
  rw [heq]
  have hdiff : (0 : ℝ) ≤ L - s := sub_nonneg.mpr (by exact_mod_cast hsL.le)
  have hterm : (0 : ℝ) ≤ ((L : ℝ) - s) / 2^s := div_nonneg hdiff (by positivity)
  linarith

/-- The exact hull gap has an absolute logarithmic error at most three. -/
theorem hullGap_log_error (L : ℕ) (hL : 2 ≤ L) :
    |hullGap (polynomial L) (means L) - logb 2 L| ≤ 3 := by
  obtain ⟨hlo, hhi⟩ := hullGap_log_bounds L hL
  exact abs_le.mpr ⟨by linarith, by linarith⟩

/-- The exact hull gap is asymptotic to `log₂ L` along all natural sizes. -/
theorem tendsto_hullGap_div_logb :
    Tendsto (fun L : ℕ => hullGap (polynomial L) (means L) / logb 2 L)
      atTop (𝓝 1) := by
  have ht : Tendsto (fun L : ℕ => logb 2 (L : ℝ)) atTop atTop := by
    exact (tendsto_log_atTop.comp tendsto_natCast_atTop_atTop).atTop_div_const
      (log_pos (by norm_num))
  have hlo : Tendsto (fun L : ℕ => 1 - 2 / logb 2 L) atTop (𝓝 1) := by
    simpa using tendsto_const_nhds.sub (tendsto_const_nhds.div_atTop ht :
      Tendsto (fun L : ℕ => 2 / logb 2 L) atTop (𝓝 0))
  have hhi : Tendsto (fun L : ℕ => 1 + 3 / logb 2 L) atTop (𝓝 1) := by
    simpa using tendsto_const_nhds.add (tendsto_const_nhds.div_atTop ht :
      Tendsto (fun L : ℕ => 3 / logb 2 L) atTop (𝓝 0))
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le' hlo hhi
  · filter_upwards [eventually_ge_atTop 2, ht.eventually (eventually_gt_atTop 0)] with L hL hp
    have h := div_le_div_of_nonneg_right (hullGap_log_bounds L hL).1 hp.le
    simpa [sub_div, div_self hp.ne'] using h
  · filter_upwards [eventually_ge_atTop 2, ht.eventually (eventually_gt_atTop 0)] with L hL hp
    have h := div_le_div_of_nonneg_right (hullGap_log_bounds L hL).2 hp.le
    simpa [add_div, div_self hp.ne'] using h

/-- The exact relaxation ratio is asymptotic to `L / log₂ L`. -/
theorem tendsto_exact_family_ratio_normalized :
    Tendsto (fun L : ℕ =>
      (termwiseGap (supports L) (means L) / hullGap (polynomial L) (means L)) /
        ((L : ℝ) / logb 2 L)) atTop (𝓝 1) := by
  have hlim : Tendsto (fun L : ℕ => (hullGap (polynomial L) (means L) / logb 2 L)⁻¹)
      atTop (𝓝 1) := by
    simpa using tendsto_hullGap_div_logb.inv₀ (by norm_num : (1 : ℝ) ≠ 0)
  apply hlim.congr'
  filter_upwards [eventually_ge_atTop 2] with L hL
  rw [termwiseGap_eq L (by omega)]
  have hLne : (L : ℝ) ≠ 0 := by exact_mod_cast (show L ≠ 0 by omega)
  field_simp

end
end MultilinearGap
