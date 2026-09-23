import Formal.MultilinearGap.FamilySize

/-! Lower witnesses at every sufficiently large degree or dimension allowance,
with sharp leading constant one. -/
namespace MultilinearGap

open CubicGap Filter Real
open scoped Topology
noncomputable section

theorem hullGap_le_logb_add_three (L : ℕ) (hL : 2 ≤ L) :
    hullGap (polynomial L) (means L) ≤ logb 2 L + 3 := by
  let s := Nat.clog 2 L
  have hp : (L : ℝ) ≤ (2 : ℝ)^s := by
    exact_mod_cast Nat.le_pow_clog (by decide : 1 < 2) L
  have hs : (s : ℝ) ≤ logb 2 L + 1 := by
    dsimp [s]
    rw [← natCeil_logb_natCast]
    exact (Nat.ceil_lt_add_one (logb_nonneg (by norm_num)
      (by exact_mod_cast (show 1 ≤ L by omega)))).le
  have hdiv : 2 * (L : ℝ) / (2 : ℝ)^s ≤ 2 := by
    apply (div_le_iff₀ (by positivity : 0 < (2 : ℝ)^s)).mpr
    linarith
  exact (hullGap_bound L hL s).trans (by linarith)

/-- Explicit lower comparison function for every allowance. -/
def lowerComparison (n : ℕ) : ℝ :=
  (witnessLevels n : ℝ) / (logb 2 (witnessLevels n) + 3)

theorem lowerComparison_le_ratio (n : ℕ) (hn : 8 ≤ n) :
    lowerComparison n ≤ termwiseGap (supports (witnessLevels n)) (means (witnessLevels n)) /
      hullGap (polynomial (witnessLevels n)) (means (witnessLevels n)) := by
  have hL := witnessLevels_ge_two n hn
  rw [termwiseGap_eq _ (by omega)]
  exact div_le_div_of_nonneg_left (Nat.cast_nonneg _) (hullGap_positive _ hL)
    (hullGap_le_logb_add_three _ hL)

theorem witnessLevels_bounds (n : ℕ) (hn : 2 ≤ n) :
    logb 2 n - 2 ≤ (witnessLevels n : ℝ) ∧ (witnessLevels n : ℝ) ≤ logb 2 n := by
  have hk : 1 ≤ Nat.log 2 n := Nat.le_log_of_pow_le (by decide) hn
  have hcast : (witnessLevels n : ℝ) = (Nat.log 2 n : ℝ) - 1 := by
    rw [witnessLevels, Nat.cast_sub hk, Nat.cast_one]
  have hlow := Nat.lt_floor_add_one (logb 2 (n : ℝ))
  rw [show (2 : ℝ) = ((2 : ℕ) : ℝ) by norm_num, natFloor_logb_natCast] at hlow
  have hupp := natLog_le_logb n 2
  norm_num only [Nat.cast_ofNat] at hlow hupp
  rw [hcast]
  constructor <;> linarith

theorem tendsto_witnessLevels_div_log :
    Tendsto (fun n : ℕ => (witnessLevels n : ℝ) / log n) atTop (𝓝 (1 / log 2)) := by
  have ht : Tendsto (fun n : ℕ => log (n : ℝ)) atTop atTop :=
    tendsto_log_atTop.comp tendsto_natCast_atTop_atTop
  have hi : Tendsto (fun n : ℕ => 2 / log n) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop ht
  have hlo : Tendsto (fun n : ℕ => 1 / log 2 - 2 / log n) atTop (𝓝 (1 / log 2)) := by
    simpa using tendsto_const_nhds.sub hi
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le' hlo tendsto_const_nhds
  · filter_upwards [eventually_ge_atTop 2] with n hn
    have hp : 0 < log (n : ℝ) := log_pos (by exact_mod_cast (show 1 < n by omega))
    have h := (div_le_div_of_nonneg_right (witnessLevels_bounds n hn).1 hp.le)
    simpa [logb, sub_div, div_right_comm, div_self hp.ne'] using h
  · filter_upwards [eventually_ge_atTop 2] with n hn
    have hp : 0 < log (n : ℝ) := log_pos (by exact_mod_cast (show 1 < n by omega))
    have h := (div_le_div_of_nonneg_right (witnessLevels_bounds n hn).2 hp.le)
    simpa [logb, div_right_comm, div_self hp.ne'] using h

theorem tendsto_log_witnessLevels_div_log_log :
    Tendsto (fun n : ℕ => log (witnessLevels n : ℝ) / log (log n)) atTop (𝓝 1) := by
  have hc : (1 / log (2 : ℝ)) ≠ 0 := by
    exact one_div_ne_zero (ne_of_gt (log_pos (by norm_num)))
  have ht : Tendsto (fun n : ℕ => log (log (n : ℝ))) atTop atTop :=
    tendsto_log_atTop.comp (tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)
  have hsmall := (tendsto_witnessLevels_div_log.log hc).div_atTop ht
  have hlim : Tendsto (fun n : ℕ => 1 +
      log ((witnessLevels n : ℝ) / log n) / log (log n)) atTop (𝓝 1) := by
    simpa using tendsto_const_nhds.add hsmall
  apply hlim.congr'
  filter_upwards [eventually_ge_atTop 8, ht.eventually (eventually_gt_atTop 0)] with n hn ht0
  have hL0 : (witnessLevels n : ℝ) ≠ 0 := by
    exact_mod_cast (show witnessLevels n ≠ 0 by have := witnessLevels_ge_two n hn; omega)
  have hlog : log (n : ℝ) ≠ 0 :=
    ne_of_gt (log_pos (by exact_mod_cast (show 1 < n by omega)))
  rw [log_div hL0 hlog]
  field_simp
  ring

/-- The explicit feasible lower witnesses have leading constant one at every
degree and dimension allowance, rather than only along a subsequence. -/
theorem tendsto_lowerComparison_normalized :
    Tendsto (fun n : ℕ => lowerComparison n / (log n / log (log n)))
      atTop (𝓝 1) := by
  have hlog2 : log (2 : ℝ) ≠ 0 := ne_of_gt (log_pos (by norm_num))
  have ht : Tendsto (fun n : ℕ => log (log (n : ℝ))) atTop atTop :=
    tendsto_log_atTop.comp (tendsto_log_atTop.comp tendsto_natCast_atTop_atTop)
  have hsmall : Tendsto (fun n : ℕ => 3 / log (log n)) atTop (𝓝 0) :=
    tendsto_const_nhds.div_atTop ht
  have hden : Tendsto (fun n : ℕ =>
      (log (witnessLevels n : ℝ) / log (log n)) / log 2 + 3 / log (log n))
      atTop (𝓝 (1 / log 2)) := by
    simpa using (tendsto_log_witnessLevels_div_log_log.div_const (log 2)).add hsmall
  have hlim := tendsto_witnessLevels_div_log.div hden (one_div_ne_zero hlog2)
  have hlim' : Tendsto (fun n : ℕ => ((witnessLevels n : ℝ) / log n) /
      ((log (witnessLevels n : ℝ) / log (log n)) / log 2 + 3 / log (log n)))
      atTop (𝓝 1) := by
    convert hlim using 1
    · funext n
      rfl
    · simp [hlog2]
  apply hlim'.congr'
  filter_upwards [eventually_ge_atTop 8, ht.eventually (eventually_gt_atTop 0)] with n hn ht0
  have hlog : log (n : ℝ) ≠ 0 :=
    ne_of_gt (log_pos (by exact_mod_cast (show 1 < n by omega)))
  have htne := ne_of_gt ht0
  dsimp [lowerComparison, logb]
  field_simp

end
end MultilinearGap
