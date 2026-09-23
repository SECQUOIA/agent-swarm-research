import Formal.MultilinearGap.AsymptoticScalars
import Formal.MultilinearGap.FloorIntegralBounds

/-! Parameter estimates and sharp scalar asymptotics for a marginal floor. -/
namespace MultilinearGap
open Filter Real Asymptotics
open scoped Topology
noncomputable section

/-- The logarithmic scale, bounded away from zero. -/
def floorB (δ : ℝ) : ℝ := max 2 (log (1 / δ))
/-- Shift of the common reciprocal density. -/
def floorTau (δ : ℝ) : ℝ := δ / (floorB δ)^2
/-- Normalizing logarithm for the shifted reciprocal density. -/
def floorL (δ : ℝ) : ℝ := log ((1 + floorTau δ) / floorTau δ)

lemma floorB_ge_two (δ : ℝ) : 2 ≤ floorB δ := le_max_left _ _
lemma floorB_pos (δ : ℝ) : 0 < floorB δ := lt_of_lt_of_le (by norm_num) (floorB_ge_two δ)
lemma floorTau_pos {δ : ℝ} (hδ : 0 < δ) : 0 < floorTau δ :=
  div_pos hδ (sq_pos_of_pos (floorB_pos δ))
lemma floorL_pos {δ : ℝ} (hδ : 0 < δ) : 0 < floorL δ := by
  apply log_pos
  apply (lt_div_iff₀ (floorTau_pos hδ)).mpr
  linarith

/-- Every permitted anchor has a shift no larger than the uniform gain shift. -/
lemma floorTau_div_le {δ u : ℝ} (hδ : 0 < δ) (hu : δ ≤ u) :
    floorTau δ / u ≤ 1 / (floorB δ)^2 := by
  have hu0 : 0 < u := hδ.trans_le hu
  unfold floorTau
  apply (div_le_iff₀ hu0).mpr
  simpa [div_eq_mul_inv, mul_comm] using
    mul_le_mul_of_nonneg_right hu (inv_nonneg.mpr (sq_nonneg (floorB δ)))

lemma floorTau_le_eighth {δ : ℝ} (hδ : δ ≤ 1 / 2) : floorTau δ ≤ 1 / 8 := by
  have hB := floorB_ge_two δ
  unfold floorTau
  apply (div_le_iff₀ (sq_pos_of_pos (floorB_pos δ))).mpr
  nlinarith
lemma floorL_gt_one {δ : ℝ} (hδ : 0 < δ) (hδ' : δ ≤ 1 / 2) : 1 < floorL δ := by
  have hτ := floorTau_pos hδ
  have hτ' := floorTau_le_eighth hδ'
  have hx : 3 < (1 + floorTau δ) / floorTau δ := by
    apply (lt_div_iff₀ hτ).mpr
    linarith
  unfold floorL
  exact (lt_log_iff_exp_lt (div_pos (by positivity) hτ)).mpr (exp_one_lt_three.trans hx)

lemma tendsto_floor_base :
    Tendsto (fun δ : ℝ => log (1 / δ)) (𝓝[>] 0) atTop := by
  simpa only [one_div, log_inv, Function.comp_def] using
    (tendsto_neg_atBot_atTop.comp tendsto_log_nhdsGT_zero)
lemma floorB_eventually : ∀ᶠ δ : ℝ in 𝓝[>] 0, floorB δ = log (1 / δ) := by
  filter_upwards [tendsto_floor_base.eventually (eventually_ge_atTop (2 : ℝ))] with δ hδ
  exact max_eq_right hδ
lemma tendsto_floorB : Tendsto floorB (𝓝[>] 0) atTop :=
  tendsto_floor_base.congr' (floorB_eventually.mono fun _ h => h.symm)
lemma tendsto_floorTau : Tendsto floorTau (𝓝[>] 0) (𝓝 0) := by
  have hi : Tendsto (fun δ => 1 / floorB δ) (𝓝[>] 0) (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_floorB
  unfold floorTau
  simpa [div_eq_mul_inv, inv_pow] using
    (tendsto_id.mono_left nhdsWithin_le_nhds).mul (hi.pow 2)
lemma floorL_identity {δ : ℝ} (hδ : 0 < δ) :
    floorL δ = log (1 / δ) + 2 * log (floorB δ) + log (1 + floorTau δ) := by
  have hB := floorB_pos δ
  have hτ := floorTau_pos hδ
  rw [floorL, log_div (by positivity) (ne_of_gt hτ)]
  rw [floorTau, log_div (ne_of_gt hδ) (ne_of_gt (sq_pos_of_pos hB)), log_pow]
  simp only [one_div, log_inv]
  ring
lemma tendsto_floorL_div_B :
    Tendsto (fun δ => floorL δ / floorB δ) (𝓝[>] 0) (𝓝 1) := by
  have hlog : Tendsto (fun δ => log (1 + floorTau δ)) (𝓝[>] 0) (𝓝 0) := by
    simpa using ((tendsto_const_nhds (x := (1 : ℝ))).add tendsto_floorTau).log
      (by norm_num : (1 : ℝ) + 0 ≠ 0)
  have ht := ((tendsto_const_nhds (x := (1 : ℝ))).add
    ((tendsto_log_div_self.comp tendsto_floorB).const_mul 2)).add
    (hlog.div_atTop tendsto_floorB)
  simp only [mul_zero, add_zero] at ht
  apply ht.congr'
  filter_upwards [floorB_eventually, self_mem_nhdsWithin] with δ hB hδ
  dsimp at hδ ⊢
  rw [floorL_identity hδ, ← hB]
  field_simp [ne_of_gt (floorB_pos δ)]
lemma floorL_equivalent_B : floorL ~[𝓝[>] 0] floorB :=
  (isEquivalent_iff_tendsto_one (Filter.Eventually.of_forall
    fun δ => ne_of_gt (floorB_pos δ))).mpr tendsto_floorL_div_B
lemma tendsto_floorL : Tendsto floorL (𝓝[>] 0) atTop :=
  floorL_equivalent_B.symm.tendsto_atTop tendsto_floorB
lemma tendsto_floor_log_ratio :
    Tendsto (fun δ => log (floorL δ) / log (floorB δ)) (𝓝[>] 0) (𝓝 1) :=
  (isEquivalent_iff_tendsto_one
    ((tendsto_log_atTop.comp tendsto_floorB).eventually_ne_atTop 0)).mp
      (floorL_equivalent_B.log tendsto_floorB)
lemma tendsto_floorL_div_B_sq :
    Tendsto (fun δ => floorL δ / (floorB δ)^2) (𝓝[>] 0) (𝓝 0) := by
  have ht := tendsto_floorL_div_B.mul
    (tendsto_const_nhds.div_atTop tendsto_floorB (a := (1 : ℝ)))
  simpa [div_eq_mul_inv, inv_pow, pow_two, mul_assoc] using ht
lemma tendsto_floor_scale :
    Tendsto (fun δ => (floorL δ / log (floorL δ)) /
      (log (1 / δ) / log (log (1 / δ)))) (𝓝[>] 0) (𝓝 1) := by
  have ht := tendsto_floorL_div_B.div tendsto_floor_log_ratio (by norm_num : (1 : ℝ) ≠ 0)
  simp only [div_one] at ht
  apply ht.congr'
  filter_upwards [floorB_eventually,
    tendsto_floorL.eventually (eventually_gt_atTop (1 : ℝ))] with δ hB hL
  have hB0 := ne_of_gt (floorB_pos δ)
  have hlogB : log (floorB δ) ≠ 0 := ne_of_gt (log_pos (by linarith [floorB_ge_two δ]))
  have hlogL : log (floorL δ) ≠ 0 := ne_of_gt (log_pos hL)
  dsimp
  rw [← hB]
  field_simp

/-- Explicit reciprocal gain and the independent-law contribution. -/
def floorUpper (δ : ℝ) : ℝ :=
  1 / floorIntegral (floorL δ) (1 / (floorB δ)^2) + 2 / (1 - exp (-1))

lemma floorUpper_pos {δ : ℝ} (hδ : 0 < δ) : 0 < floorUpper δ := by
  have hI := floorIntegral_pos (floorL_pos hδ)
    (div_pos one_pos (sq_pos_of_pos (floorB_pos δ)))
  exact add_pos (div_pos one_pos hI) (div_pos (by norm_num) independent_gain_pos)

lemma tendsto_floor_lower_normalized :
    Tendsto (fun δ => 1 / (1 + floorL δ / (floorB δ)^2) -
      (1 - 1 / floorL δ) / (2 * log (floorL δ))) (𝓝[>] 0) (𝓝 1) := by
  have ha := (tendsto_const_nhds (x := (1 : ℝ))).div
    ((tendsto_const_nhds (x := (1 : ℝ))).add tendsto_floorL_div_B_sq)
    (by norm_num : (1 : ℝ) + 0 ≠ 0)
  have hb : Tendsto (fun δ => 1 / floorL δ) (𝓝[>] 0) (𝓝 0) :=
    tendsto_const_nhds.div_atTop tendsto_floorL
  have hc := ((tendsto_const_nhds (x := (1 : ℝ))).sub hb).div_atTop
    ((tendsto_log_atTop.comp tendsto_floorL).const_mul_atTop (by norm_num : (0 : ℝ) < 2))
  simpa using ha.sub hc

lemma tendsto_floor_upper_normalized :
    Tendsto (fun δ => 1 + 1 / log (floorL δ)) (𝓝[>] 0) (𝓝 1) := by
  simpa using (tendsto_const_nhds (x := (1 : ℝ))).add
    (tendsto_const_nhds.div_atTop (tendsto_log_atTop.comp tendsto_floorL) (a := (1 : ℝ)))


/-- The integral gain is asymptotic to `log L / L`. -/
theorem tendsto_floorIntegral_normalized :
    Tendsto (fun δ => floorIntegral (floorL δ) (1 / (floorB δ)^2) /
      (log (floorL δ) / floorL δ)) (𝓝[>] 0) (𝓝 1) := by
  apply tendsto_of_tendsto_of_tendsto_of_le_of_le'
    tendsto_floor_lower_normalized tendsto_floor_upper_normalized
  · filter_upwards [tendsto_floorL.eventually (eventually_gt_atTop (1 : ℝ))] with δ hL
    have hL0 : 0 < floorL δ := by linarith
    have hl : 0 < log (floorL δ) := log_pos hL
    have hB := floorB_pos δ
    have he : 0 < 1 / (floorB δ)^2 := div_pos one_pos (sq_pos_of_pos (floorB_pos δ))
    have h := div_le_div_of_nonneg_right (floorIntegral_lower hL he) (div_nonneg hl.le hL0.le)
    convert h using 1
    field_simp
  · filter_upwards [tendsto_floorL.eventually (eventually_gt_atTop (1 : ℝ))] with δ hL
    have hL0 : 0 < floorL δ := by linarith
    have hl : 0 < log (floorL δ) := log_pos hL
    have he : 0 < 1 / (floorB δ)^2 := div_pos one_pos (sq_pos_of_pos (floorB_pos δ))
    have h := div_le_div_of_nonneg_right (floorIntegral_upper hL he) (div_nonneg hl.le hL0.le)
    convert h using 1
    field_simp
    ring


/-- Inverting the normalized gain preserves the leading constant; the fixed
independence contribution vanishes on the diverging logarithmic scale. -/
theorem tendsto_floorUpper_normalized :
    Tendsto (fun δ => floorUpper δ /
      (log (1 / δ) / log (log (1 / δ)))) (𝓝[>] 0) (𝓝 1) := by
  have hi := (tendsto_const_nhds (x := (1 : ℝ))).div
    tendsto_floorIntegral_normalized (by norm_num : (1 : ℝ) ≠ 0)
  have hc := (tendsto_log_div_self.comp tendsto_floorL).const_mul (2 / (1 - exp (-1)))
  have ht : Tendsto (fun δ =>
      (1 / (floorIntegral (floorL δ) (1 / (floorB δ)^2) /
        (log (floorL δ) / floorL δ)) +
        (2 / (1 - exp (-1))) * (log (floorL δ) / floorL δ)) *
        ((floorL δ / log (floorL δ)) /
          (log (1 / δ) / log (log (1 / δ))))) (𝓝[>] 0) (𝓝 1) := by
    simpa using (hi.add hc).mul tendsto_floor_scale
  apply ht.congr'
  filter_upwards [tendsto_floorL.eventually (eventually_gt_atTop (1 : ℝ))] with δ hL
  have hL0 : floorL δ ≠ 0 := ne_of_gt (by linarith)
  have hl : log (floorL δ) ≠ 0 := ne_of_gt (log_pos hL)
  dsimp [floorUpper]
  field_simp

end
end MultilinearGap
