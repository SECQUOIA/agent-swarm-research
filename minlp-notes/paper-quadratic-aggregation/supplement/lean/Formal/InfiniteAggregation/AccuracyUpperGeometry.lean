import Formal.InfiniteAggregation.HullRepresentations

/-! Angular tests and radial repair for finite aggregation bounds. -/
noncomputable section
open Set
namespace InfiniteAggregation

def angleWeight (t : ℝ) : Weight :=
  ![Real.cos t ^ 2, Real.sin t ^ 2, 2 * Real.cos t * Real.sin t]

def pointAngularForm {r : ℕ} (x : Var r) (t : ℝ) : ℝ :=
  (1 - qnorm x.1) * Real.cos t ^ 2 +
  2 * (dot x.1 x.2 - 1 / 2) * Real.cos t * Real.sin t +
  (1 - qnorm x.2) * Real.sin t ^ 2

theorem angleWeight_goodCone {t : ℝ} (ht : t ∈ Icc 0 (Real.pi / 2)) :
    GoodCone (angleWeight t) := by
  constructor
  · intro i
    fin_cases i
    · exact sq_nonneg _
    · exact sq_nonneg _
    · change 0 ≤ 2 * Real.cos t * Real.sin t
      exact mul_nonneg (mul_nonneg (by norm_num)
        (Real.cos_nonneg_of_mem_Icc ⟨by linarith [Real.pi_pos, ht.1], ht.2⟩))
        (Real.sin_nonneg_of_mem_Icc ⟨ht.1, by linarith [Real.pi_pos, ht.2]⟩)
  · dsimp [angleWeight]
    nlinarith

theorem angleWeight_ne_zero (t : ℝ) : angleWeight t ≠ 0 := by
  intro h
  have h0 := congrFun h 0
  have h1 := congrFun h 1
  simp only [angleWeight, Fin.isValue, Matrix.cons_val_zero, Matrix.cons_val_one,
    Pi.zero_apply] at h0 h1
  nlinarith [Real.sin_sq_add_cos_sq t]

theorem angleWeight_good {r : ℕ} (hr : 2 ≤ r) {t : ℝ}
    (ht : t ∈ Icc 0 (Real.pi / 2)) : Good r (angleWeight t) :=
  (good_iff_goodCone hr _).2 ⟨angleWeight_goodCone ht, angleWeight_ne_zero t⟩

theorem pointAngularForm_eq_neg_aggregate {r : ℕ} (x : Var r) (t : ℝ) :
    pointAngularForm x t = -aggregate (angleWeight t) x := by
  simp [pointAngularForm, angleWeight, aggregate_formula]
  ring

@[simp] theorem pointAngularForm_zero {r : ℕ} (x : Var r) :
    pointAngularForm x 0 = 1 - qnorm x.1 := by simp [pointAngularForm]
@[simp] theorem pointAngularForm_pi_div_two {r : ℕ} (x : Var r) :
    pointAngularForm x (Real.pi / 2) = 1 - qnorm x.2 := by simp [pointAngularForm]

theorem nonneg_quadratic_of_angular {p q c : ℝ}
    (h : ∀ t ∈ Icc 0 (Real.pi / 2),
      0 ≤ p * Real.cos t ^ 2 + 2 * c * Real.cos t * Real.sin t + q * Real.sin t ^ 2)
    {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    0 ≤ p * a ^ 2 + 2 * c * a * b + q * b ^ 2 := by
  by_cases haz : a = 0
  · subst a
    have hq := h (Real.pi / 2) ⟨by positivity, le_rfl⟩
    simp only [Real.cos_pi_div_two, Real.sin_pi_div_two] at hq
    have : 0 ≤ q := by nlinarith
    simpa using mul_nonneg this (sq_nonneg b)
  have hap : 0 < a := lt_of_le_of_ne ha (Ne.symm haz)
  let z := b / a
  have hz : 0 ≤ z := div_nonneg hb ha
  have ht := h (Real.arctan z)
    ⟨Real.arctan_nonneg.2 hz, (Real.arctan_lt_pi_div_two z).le⟩
  rw [Real.cos_arctan, Real.sin_arctan] at ht
  have hs : 0 < Real.sqrt (1 + z ^ 2) := by positivity
  have hmul := mul_nonneg ht (sq_nonneg (a * Real.sqrt (1 + z ^ 2)))
  have hid : (p * (1 / Real.sqrt (1 + z ^ 2)) ^ 2 +
      2 * c * (1 / Real.sqrt (1 + z ^ 2)) * (z / Real.sqrt (1 + z ^ 2)) +
      q * (z / Real.sqrt (1 + z ^ 2)) ^ 2) *
      (a * Real.sqrt (1 + z ^ 2)) ^ 2 = p * a ^ 2 + 2 * c * a * b + q * b ^ 2 := by
    field_simp
    dsimp [z]
    field_simp
  rwa [hid] at hmul

theorem scalar_copositive_condition {p q c : ℝ}
    (h : ∀ a b : ℝ, 0 ≤ a → 0 ≤ b → 0 ≤ p * a ^ 2 - 2 * c * a * b + q * b ^ 2) :
    0 ≤ p ∧ 0 ≤ q ∧ c ≤ Real.sqrt (p * q) := by
  have hp : 0 ≤ p := by simpa using h 1 0 (by norm_num) (by norm_num)
  have hq : 0 ≤ q := by simpa using h 0 1 (by norm_num) (by norm_num)
  refine ⟨hp, hq, ?_⟩
  by_cases hc : c ≤ 0
  · exact hc.trans (Real.sqrt_nonneg _)
  have hcp : 0 < c := lt_of_not_ge hc
  have hpp : 0 < p := by
    by_contra hn
    have hpz : p = 0 := le_antisymm (not_lt.mp hn) hp
    have hh := h (q + 1) c (by linarith) hcp.le
    rw [hpz] at hh
    nlinarith [mul_nonneg hq (sq_nonneg c), sq_pos_of_pos hcp]
  have hqq : 0 < q := by
    by_contra hn
    have hqz : q = 0 := le_antisymm (not_lt.mp hn) hq
    have hh := h c (p + 1) hcp.le (by linarith)
    rw [hqz] at hh
    nlinarith [mul_nonneg hp (sq_nonneg c), sq_pos_of_pos hcp]
  have hh := h (Real.sqrt q) (Real.sqrt p) (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
  rw [Real.sq_sqrt hq, Real.sq_sqrt hp] at hh
  have hs : Real.sqrt q * Real.sqrt p = Real.sqrt (p * q) := by
    rw [← Real.sqrt_mul hq, mul_comm]
  have hs2 := Real.sq_sqrt (mul_nonneg hp hq)
  have hsp := Real.sqrt_pos.2 (mul_pos hpp hqq)
  have hh' : 0 ≤ 2 * p * q - 2 * c * Real.sqrt (p * q) := by nlinarith [hh]
  nlinarith

theorem angular_tests_subset_closedRegion {r : ℕ} {x : Var r}
    (h : ∀ t ∈ Icc 0 (Real.pi / 2), 0 ≤ pointAngularForm x t) : x ∈ closedRegion r := by
  have hquad := fun a b ha hb => nonneg_quadratic_of_angular h (a := a) (b := b) ha hb
  have hc := scalar_copositive_condition (p := 1 - qnorm x.1)
    (q := 1 - qnorm x.2) (c := 1 / 2 - dot x.1 x.2) (by
      intro a b ha hb
      have hh := hquad a b ha hb
      nlinarith)
  exact ⟨by linarith [hc.1], by linarith [hc.2.1], by linarith [hc.2.2]⟩

/-- Radial scaling mixes the angular form with its value at the origin. -/
theorem pointAngularForm_smul {r : ℕ} (x : Var r) (s t : ℝ) :
    pointAngularForm (s • x) t = s ^ 2 * pointAngularForm x t +
      (1 - s ^ 2) * pointAngularForm (0 : Var r) t := by
  simp only [pointAngularForm, Prod.smul_fst, Prod.smul_snd, qnorm_smul,
    dot_smul_left, dot_smul_right, Prod.fst_zero, Prod.snd_zero, qnorm_zero,
    dot_zero_left]
  ring

theorem pointAngularForm_origin_ge (r : ℕ) (t : ℝ) :
    1 / 2 ≤ pointAngularForm (0 : Var r) t := by
  simp only [pointAngularForm, Prod.fst_zero, Prod.snd_zero, qnorm_zero, dot_zero_left]
  nlinarith [Real.sin_sq_add_cos_sq t, sq_nonneg (Real.cos t - Real.sin t)]

/-- The radial repair factor, together with its displacement estimate. -/
theorem radial_factor {a : ℝ} (ha : 0 ≤ a) :
    ∃ s : ℝ, 0 ≤ s ∧ s ≤ 1 ∧ s ^ 2 * (1 + 2 * a) = 1 ∧ 1 - s ≤ a := by
  let s := 1 / Real.sqrt (1 + 2 * a)
  have hp : 0 < 1 + 2 * a := by positivity
  have hsqrt : 0 < Real.sqrt (1 + 2 * a) := Real.sqrt_pos.2 hp
  have hs : 0 < s := by dsimp [s]; positivity
  have hs2 : s ^ 2 * (1 + 2 * a) = 1 := by
    dsimp [s]
    rw [div_pow, Real.sq_sqrt hp.le]
    field_simp
  have hsle : s ≤ 1 := by
    have hmul := mul_nonneg (sq_nonneg s) ha
    nlinarith
  have hsqs : s ^ 2 ≤ s := by nlinarith
  have hsa : 1 - s ≤ a := by
    have hm := mul_nonneg ha (show 0 ≤ 1 + s - 2 * s ^ 2 by nlinarith)
    have hn : (1 - s - a) * (1 + s) ≤ 0 := by nlinarith [hs2]
    nlinarith
  exact ⟨s, hs.le, hsle, hs2, hsa⟩

/-- A uniform angular violation bound is repaired by one radial scaling. -/
theorem radial_repair {r : ℕ} {x : Var r} {a : ℝ} (ha : 0 ≤ a)
    (h : ∀ t ∈ Icc 0 (Real.pi / 2), -a ≤ pointAngularForm x t) :
    ∃ s : ℝ, 0 ≤ s ∧ s ≤ 1 ∧ 1 - s ≤ a ∧ s • x ∈ closedRegion r := by
  obtain ⟨s, hs, hs1, heq, hdist⟩ := radial_factor ha
  refine ⟨s, hs, hs1, hdist, angular_tests_subset_closedRegion ?_⟩
  intro t ht
  rw [pointAngularForm_smul]
  have h1 := mul_nonneg (sq_nonneg s) (show 0 ≤ pointAngularForm x t + a by linarith [h t ht])
  have h2 := mul_nonneg (show 0 ≤ 1 - s ^ 2 by nlinarith)
    (show 0 ≤ pointAngularForm (0 : Var r) t - 1 / 2 by linarith [pointAngularForm_origin_ge r t])
  nlinarith

end InfiniteAggregation
