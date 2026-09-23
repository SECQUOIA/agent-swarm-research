import QipmFormal.ScalarCert.Elasticity
import QipmFormal.ScalarCert.Enclosures

/-!
# Towards the upper certificate: the elasticity `E` and the `E > 2` threshold

`E v = Y v / v` has the power series `∑ (2 - 2^{-k}) v^{2k}/(2k+1)`, whose
`k = 0` term is the constant `1` and whose remaining terms are strictly
increasing on `(0,1)`.  Hence `E` is strictly increasing, which turns the
appendix's region `E > 2` into an explicit interval `v > v₂`.

The appendix uses the threshold `x > 4/5`, i.e. `v > 4√2/√41 ≈ 0.88345`.
We instead certify `v₂ = 177/200 = 0.885`.  Note this is slightly *larger*
than the appendix's threshold, so the region `(v₂,1)` is a proper subset of
the appendix's; what makes it valid is that `v₂` is still below the true root
of `E = 2` (`≈ 0.8871093`), which is what `E_v2_le_two` certifies.
-/

namespace QipmFormal.ScalarCert

open Real Set Finset

set_option exponentiation.threshold 100000

/-- Power series for `E`. -/
theorem hasSum_E {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) :
    HasSum (fun k : ℕ => (2 - (1/2 : ℝ) ^ k) / (2 * (k : ℝ) + 1) * v ^ (2 * k)) (E v) := by
  have habs : |v| < 1 := by rwa [abs_of_pos hv0]
  have h := (hasSum_Y habs).div_const v
  rw [E]
  refine h.congr_fun ?_
  intro k
  field_simp
  ring

/-- `E` is strictly increasing on `(0,1)`. -/
theorem E_strictMonoOn : StrictMonoOn E (Ioo 0 1) := by
  intro a ha b hb hab
  have hsa := hasSum_E ha.1 ha.2
  have hsb := hasSum_E hb.1 hb.2
  refine hasSum_lt (i := 1) ?_ ?_ hsa hsb
  · intro k
    have hcoef : (0:ℝ) ≤ (2 - (1/2 : ℝ) ^ k) / (2 * (k : ℝ) + 1) := by
      have hp : (0:ℝ) < 2 * (k : ℝ) + 1 := by positivity
      exact div_nonneg (coef_nonneg k) hp.le
    have hpow : a ^ (2 * k) ≤ b ^ (2 * k) := pow_le_pow_left₀ ha.1.le hab.le _
    exact mul_le_mul_of_nonneg_left hpow hcoef
  · have hab2 : a ^ (2 * 1) < b ^ (2 * 1) := by
      simpa using pow_lt_pow_left₀ hab ha.1.le (by norm_num : 2 ≠ 0)
    have hc : (0:ℝ) < (2 - (1/2 : ℝ) ^ 1) / (2 * ((1:ℕ) : ℝ) + 1) := by norm_num
    exact mul_lt_mul_of_pos_left hab2 hc

/-! ### The threshold `v₂ = 177/200` -/

/-- `v₂ = 177/200`. -/
noncomputable def v2 : ℝ := 177 / 200

lemma v2_pos : 0 < v2 := by rw [v2]; norm_num
lemma v2_lt_one : v2 < 1 := by rw [v2]; norm_num
lemma v2_cast : v2 = ((177 : ℕ) : ℝ) / ((200 : ℕ) : ℝ) := by rw [v2]; norm_num

set_option maxRecDepth 1000000 in
theorem accHi_v2 : accHi (177 * 177) (200 * 200) (10 ^ 20) 0 49
    = 198650845420592013062 := by decide

set_option maxRecDepth 1000000 in
theorem pow_v2_nat : 177 ^ 101 * 10 ^ 5 ≤ 200 ^ 101 := by decide

lemma pow_v2 : v2 ^ 101 ≤ 1 / 10 ^ 5 := by
  rw [v2, div_pow, div_le_div_iff₀ (by positivity) (by positivity), one_mul]
  exact_mod_cast pow_v2_nat

lemma tail_v2 :
    2 * v2 ^ (2 * (49 + 1) + 1) / ((2 * ((49 : ℕ) + 1 : ℝ) + 1) * (1 - v2 ^ 2))
      ≤ 1 / 10 ^ 6 := by
  have hden : (2 * ((49 : ℕ) + 1 : ℝ) + 1) * (1 - v2 ^ 2) = 875771 / 40000 := by
    rw [v2]; push_cast; norm_num
  have hnn : (0:ℝ) ≤ v2 ^ 101 := pow_nonneg v2_pos.le _
  have hp := pow_v2
  rw [show 2 * (49 + 1) + 1 = 101 from rfl, hden, div_le_iff₀ (by norm_num)]
  linarith

/-- `Y v₂ ≤ 2 v₂`, i.e. `E v₂ ≤ 2`. -/
theorem Y_v2_le : Y v2 ≤ 2 * v2 := by
  have h := Y_le_accHi (a := 177) (b := 200) (s := 10 ^ 20) (z := v2)
    v2_cast (by norm_num) (by norm_num) (by norm_num) 49
  rw [accHi_v2] at h
  have ht := tail_v2
  push_cast at h ht
  have hrat : v2 * (198650845420592013062 / 10 ^ 20) + 1 / 10 ^ 6 ≤ 2 * v2 := by
    rw [v2]; norm_num
  linarith

theorem E_v2_le_two : E v2 ≤ 2 := by
  rw [E, div_le_iff₀ v2_pos]
  linarith [Y_v2_le]

/-- On the appendix's region `E > 2` the variable is bounded below by `v₂`. -/
theorem lt_of_two_lt_E {v : ℝ} (hv0 : 0 < v) (hv1 : v < 1) (hE : 2 < E v) : v2 < v := by
  rcases lt_trichotomy v2 v with h | h | h
  · exact h
  · rw [← h] at hE; linarith [E_v2_le_two]
  · have := E_strictMonoOn ⟨hv0, hv1⟩ ⟨v2_pos, v2_lt_one⟩ h
    linarith [E_v2_le_two]

end QipmFormal.ScalarCert
