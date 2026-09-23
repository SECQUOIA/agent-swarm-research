import Formal.MultilinearGap.LowerAsymptotics

/-! Dyadic lower witnesses under a prescribed marginal floor, including the
same leading constant for the two-sided marginal strip. -/
namespace MultilinearGap

open CubicGap Filter Real
open scoped Topology
noncomputable section

def floorLevels (δ : ℝ) : ℕ := ⌊logb 2 (1 / δ)⌋₊

def floorLower (δ : ℝ) : ℝ :=
  (floorLevels δ : ℝ) / (logb 2 (floorLevels δ) + 3)

theorem floorLevels_ge_two {δ : ℝ} (hδ : 0 < δ) (hsmall : δ ≤ 1 / 4) :
    2 ≤ floorLevels δ := by
  change 2 ≤ ⌊logb 2 (1 / δ)⌋₊
  apply Nat.le_floor
  change (2 : ℝ) ≤ logb 2 (1 / δ)
  apply (le_logb_iff_rpow_le (by norm_num : (1 : ℝ) < 2) (by positivity)).mpr
  norm_num only [rpow_ofNat, Nat.cast_ofNat, pow_two]
  exact (le_div_iff₀ hδ).mpr (by linarith)

theorem floorLevels_pow_le {δ : ℝ} (hδ : 0 < δ) (hsmall : δ ≤ 1 / 4) :
    (2 : ℝ) ^ floorLevels δ ≤ 1 / δ := by
  have hnonneg : 0 ≤ logb 2 (1 / δ) :=
    logb_nonneg (by norm_num) ((le_div_iff₀ hδ).mpr (by linarith))
  have h := Nat.floor_le hnonneg
  have hp := (le_logb_iff_rpow_le (by norm_num : (1 : ℝ) < 2)
    (by positivity : 0 < 1 / δ)).mp h
  simpa [floorLevels] using hp

/-- Every level of the dyadic family lies in its natural two-sided strip. -/
theorem means_dyadic_strip (L : ℕ) (hL : 1 ≤ L) (i : Coord L) :
    1 / (2 : ℝ)^L ≤ means L i ∧ means L i ≤ 1 - 1 / (2 : ℝ)^L := by
  have hhalf : 1 / (2 : ℝ)^L ≤ 1 / 2 := by
    apply one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 2)
    calc
      (2 : ℝ) = 2^1 := by norm_num
      _ ≤ 2^L := pow_le_pow_right₀ (by norm_num) hL
  cases i with
  | inl j =>
    have hblock : (blockCount L j : ℝ) = (2 : ℝ)^(j.val + 1) := by
      simp [blockCount]
    have hbpos : 0 < (blockCount L j : ℝ) := by rw [hblock]; positivity
    have hbupper : (blockCount L j : ℝ) ≤ (2 : ℝ)^L := by
      rw [hblock]
      exact pow_le_pow_right₀ (by norm_num) (by omega)
    have hblower : (2 : ℝ) ≤ (blockCount L j : ℝ) := by
      rw [hblock]
      calc
        (2 : ℝ) = 2^1 := by norm_num
        _ ≤ 2^(j.val + 1) := pow_le_pow_right₀ (by norm_num) (by omega)
    constructor
    · exact one_div_le_one_div_of_le hbpos hbupper
    · have := one_div_le_one_div_of_le (by norm_num : (0 : ℝ) < 2) hblower
      dsimp [means]
      linarith
  | inr i =>
    dsimp [means]
    constructor <;> linarith

theorem means_floor_strip {δ : ℝ} (hδ : 0 < δ) (hsmall : δ ≤ 1 / 4)
    (i : Coord (floorLevels δ)) :
    δ ≤ means (floorLevels δ) i ∧ means (floorLevels δ) i ≤ 1 - δ := by
  have hL := floorLevels_ge_two hδ hsmall
  have hlow : δ ≤ 1 / (2 : ℝ)^floorLevels δ := by
    have := one_div_le_one_div_of_le
      (by positivity : 0 < (2 : ℝ)^floorLevels δ) (floorLevels_pow_le hδ hsmall)
    simpa using this
  have hi := means_dyadic_strip (floorLevels δ) (by omega) i
  exact ⟨hlow.trans hi.1, hi.2.trans (by linarith)⟩

theorem floorLower_le_ratio {δ : ℝ} (hδ : 0 < δ) (hsmall : δ ≤ 1 / 4) :
    floorLower δ ≤ termwiseGap (supports (floorLevels δ)) (means (floorLevels δ)) /
      hullGap (polynomial (floorLevels δ)) (means (floorLevels δ)) := by
  have hL := floorLevels_ge_two hδ hsmall
  rw [termwiseGap_eq _ (by omega)]
  exact div_le_div_of_nonneg_left (Nat.cast_nonneg _) (hullGap_positive _ hL)
    (hullGap_le_logb_add_three _ hL)

private theorem floorLog_bounds (x : ℝ) (hx : 2 ≤ x) :
    logb 2 x - 1 ≤ (⌊logb 2 x⌋₊ : ℝ) ∧ (⌊logb 2 x⌋₊ : ℝ) ≤ logb 2 x := by
  constructor
  · have := Nat.lt_floor_add_one (logb 2 x)
    linarith
  · exact Nat.floor_le (logb_nonneg (by norm_num) (by linarith))

private theorem tendsto_floorLog_div_log :
    Tendsto (fun x : ℝ => (⌊logb 2 x⌋₊ : ℝ) / log x) atTop (𝓝 (1 / log 2)) := by
  have ht : Tendsto (fun x : ℝ => log x) atTop atTop := tendsto_log_atTop
  have hi : Tendsto (fun x : ℝ => 1 / log x) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop ht
  have hlo : Tendsto (fun x : ℝ => 1 / log 2 - 1 / log x) atTop (𝓝 (1 / log 2)) := by
    simpa using tendsto_const_nhds.sub hi
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le' hlo tendsto_const_nhds
  · filter_upwards [eventually_ge_atTop 2] with x hx
    have hp : 0 < log x := log_pos (by linarith)
    have h := div_le_div_of_nonneg_right (floorLog_bounds x hx).1 hp.le
    simpa [logb, sub_div, div_right_comm, div_self hp.ne'] using h
  · filter_upwards [eventually_ge_atTop 2] with x hx
    have hp : 0 < log x := log_pos (by linarith)
    have h := div_le_div_of_nonneg_right (floorLog_bounds x hx).2 hp.le
    simpa [logb, div_right_comm, div_self hp.ne'] using h

private theorem tendsto_log_floorLog_div_log_log :
    Tendsto (fun x : ℝ => log (⌊logb 2 x⌋₊ : ℝ) / log (log x)) atTop (𝓝 1) := by
  have hc : (1 / log (2 : ℝ)) ≠ 0 := by
    exact one_div_ne_zero (ne_of_gt (log_pos (by norm_num)))
  have ht : Tendsto (fun x : ℝ => log (log x)) atTop atTop :=
    tendsto_log_atTop.comp tendsto_log_atTop
  have hsmall := (tendsto_floorLog_div_log.log hc).div_atTop ht
  have hlim : Tendsto (fun x : ℝ => 1 +
      log ((⌊logb 2 x⌋₊ : ℝ) / log x) / log (log x)) atTop (𝓝 1) := by
    simpa using tendsto_const_nhds.add hsmall
  apply hlim.congr'
  filter_upwards [eventually_ge_atTop 2, ht.eventually (eventually_gt_atTop 0)] with x hx ht0
  have hL : 1 ≤ ⌊logb 2 x⌋₊ := by
    apply Nat.le_floor
    simpa using logb_le_logb_of_le (by norm_num : (1 : ℝ) < 2) (by norm_num : (0 : ℝ) < 2) hx
  have hL0 : (⌊logb 2 x⌋₊ : ℝ) ≠ 0 := by exact_mod_cast (show ⌊logb 2 x⌋₊ ≠ 0 by omega)
  have hlog : log x ≠ 0 := ne_of_gt (log_pos (by linarith))
  rw [log_div hL0 hlog]
  field_simp
  ring

private theorem tendsto_floorLog_normalized :
    Tendsto (fun x : ℝ => ((⌊logb 2 x⌋₊ : ℝ) / (logb 2 (⌊logb 2 x⌋₊ : ℝ) + 3)) /
      (log x / log (log x))) atTop (𝓝 1) := by
  have hlog2 : log (2 : ℝ) ≠ 0 := ne_of_gt (log_pos (by norm_num))
  have ht : Tendsto (fun x : ℝ => log (log x)) atTop atTop :=
    tendsto_log_atTop.comp tendsto_log_atTop
  have hsmall : Tendsto (fun x : ℝ => 3 / log (log x)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop ht
  have hden : Tendsto (fun x : ℝ =>
      (log (⌊logb 2 x⌋₊ : ℝ) / log (log x)) / log 2 + 3 / log (log x))
      atTop (𝓝 (1 / log 2)) := by
    simpa using (tendsto_log_floorLog_div_log_log.div_const (log 2)).add hsmall
  have hlim := tendsto_floorLog_div_log.div hden (one_div_ne_zero hlog2)
  have hlim' : Tendsto (fun x : ℝ => ((⌊logb 2 x⌋₊ : ℝ) / log x) /
      ((log (⌊logb 2 x⌋₊ : ℝ) / log (log x)) / log 2 + 3 / log (log x)))
      atTop (𝓝 1) := by
    convert hlim using 1
    · funext x
      rfl
    · simp [hlog2]
  apply hlim'.congr'
  filter_upwards [eventually_ge_atTop 2, ht.eventually (eventually_gt_atTop 0)] with x hx ht0
  have hlog : log x ≠ 0 := ne_of_gt (log_pos (by linarith))
  have htne := ne_of_gt ht0
  dsimp [logb]
  field_simp

/-- The feasible strip witnesses attain sharp leading constant one as the floor
approaches zero through positive values. -/
theorem tendsto_floorLower_normalized :
    Tendsto (fun δ : ℝ => floorLower δ / (log (1 / δ) / log (log (1 / δ))))
      (𝓝[>] 0) (𝓝 1) := by
  simpa [floorLower, floorLevels, Function.comp_def, one_div] using
    tendsto_floorLog_normalized.comp tendsto_inv_nhdsGT_zero

/-- The selected number of levels diverges along all positive real floors. -/
theorem tendsto_floorLevels : Tendsto floorLevels (𝓝[>] 0) atTop := by
  change Tendsto (fun δ : ℝ => ⌊logb 2 (1 / δ)⌋₊) (𝓝[>] 0) atTop
  simpa only [Function.comp_def, one_div] using
    tendsto_nat_floor_atTop.comp
      ((tendsto_logb_atTop (by norm_num : (1 : ℝ) < 2)).comp tendsto_inv_nhdsGT_zero)

/-- The unshifted natural scale of the selected family has leading constant one. -/
theorem tendsto_floorLevels_scale :
    Tendsto (fun δ : ℝ => ((floorLevels δ : ℝ) / logb 2 (floorLevels δ)) /
      (log (1 / δ) / log (log (1 / δ)))) (𝓝[>] 0) (𝓝 1) := by
  have ht : Tendsto (fun δ : ℝ => logb 2 (floorLevels δ)) (𝓝[>] 0) atTop :=
    (tendsto_logb_atTop (by norm_num : (1 : ℝ) < 2)).comp
      (tendsto_natCast_atTop_atTop.comp tendsto_floorLevels)
  have hsmall : Tendsto (fun δ : ℝ => 3 / logb 2 (floorLevels δ)) (𝓝[>] 0) (𝓝 0) :=
    tendsto_const_nhds.div_atTop ht
  have hfactor : Tendsto (fun δ : ℝ => 1 + 3 / logb 2 (floorLevels δ))
      (𝓝[>] 0) (𝓝 1) := by simpa using hsmall.const_add 1
  have hlim : Tendsto (fun δ : ℝ =>
      (floorLower δ / (log (1 / δ) / log (log (1 / δ)))) *
        (1 + 3 / logb 2 (floorLevels δ))) (𝓝[>] 0) (𝓝 1) := by
    simpa using tendsto_floorLower_normalized.mul hfactor
  apply hlim.congr'
  filter_upwards [ht.eventually (eventually_gt_atTop 0)] with δ hlog
  have hne := ne_of_gt hlog
  have hadd : logb 2 (floorLevels δ) + 3 ≠ 0 := by linarith
  dsimp [floorLower]
  field_simp

end
end MultilinearGap
