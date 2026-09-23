import Formal.ReciprocalAnchor.ManyModel

/-! Integral identities and order bounds for finite reciprocal-anchor laws. -/
namespace ReciprocalAnchor.ManyLeaf

open MeasureTheory Set

/-- Integrating an affine call-function segment uses only rational operations. -/
theorem affine_call_integral {α β U V : ℝ} (hα : 0 < α) (hαβ : α ≤ β) :
    (∫ s in α..β, 2 * (U - V * s) / s ^ 3) =
      U * ((α ^ 2)⁻¹ - (β ^ 2)⁻¹) - 2 * V * (α⁻¹ - β⁻¹) := by
  have hn : ∀ s ∈ Icc α β, s ≠ 0 := fun s hs => ne_of_gt (hα.trans_le hs.1)
  have hc : ContinuousOn (fun s : ℝ => 2 * (U - V * s) / s ^ 3) (Icc α β) := by
    fun_prop (disch := aesop)
  have hd : ∀ s ∈ Icc α β,
      HasDerivAt (fun t : ℝ => -U / t ^ 2 + 2 * V / t)
        (2 * (U - V * s) / s ^ 3) s := by
    intro s hs
    convert! ((hasDerivAt_const s (-U)).div ((hasDerivAt_id s).pow 2) (pow_ne_zero 2 (hn s hs))).add
      ((hasDerivAt_const s (2 * V)).div (hasDerivAt_id s) (hn s hs)) using 1
    dsimp
    field_simp
    ring
  have hc' : ContinuousOn (fun s : ℝ => 2 * (U - V * s) / s ^ 3) (uIcc α β) := by
    simpa only [uIcc_of_le hαβ] using hc
  have hi := intervalIntegral.integral_eq_sub_of_hasDerivAt (a := α) (b := β)
    (by simpa only [uIcc_of_le hαβ] using hd)
    hc'.intervalIntegrable
  rw [hi]
  simp only [div_eq_mul_inv]
  ring

/-- A reciprocal is its tangent at the left endpoint plus its weighted call integral. -/
theorem reciprocal_call_identity {a b x : ℝ} (ha : 0 < a)
    (hax : a ≤ x) (hxb : x ≤ b) :
    1 / x = 1 / a - (x - a) / a ^ 2 +
      ∫ s in a..b, 2 * max (x - s) 0 / s ^ 3 := by
  have hab := hax.trans hxb
  have hx : 0 < x := ha.trans_le hax
  have hn : ∀ s ∈ Icc a b, s ≠ 0 := fun s hs => ne_of_gt (ha.trans_le hs.1)
  have hc : ContinuousOn (fun s : ℝ => 2 * max (x - s) 0 / s ^ 3) (Icc a b) := by
    fun_prop (disch := aesop)
  have hc' : ContinuousOn (fun s : ℝ => 2 * max (x - s) 0 / s ^ 3) (uIcc a b) := by
    simpa only [uIcc_of_le hab] using hc
  have hia := (hc'.intervalIntegrable (μ := volume)).mono_set (c := a) (d := x) (by
    simpa only [uIcc_of_le hax, uIcc_of_le hab] using Icc_subset_Icc_right hxb)
  have hib := (hc'.intervalIntegrable (μ := volume)).mono_set (c := x) (d := b) (by
    simpa only [uIcc_of_le hxb, uIcc_of_le hab] using Icc_subset_Icc_left hax)
  rw [← intervalIntegral.integral_add_adjacent_intervals hia hib]
  have hz : (∫ s in x..b, 2 * max (x - s) 0 / s ^ 3) = 0 := by
    calc
      _ = ∫ s in x..b, (0 : ℝ) := intervalIntegral.integral_congr (by
        intro s hs
        rw [uIcc_of_le hxb] at hs
        simp [max_eq_right (sub_nonpos.mpr hs.1)])
      _ = 0 := by simp
  have he : (∫ s in a..x, 2 * max (x - s) 0 / s ^ 3) =
      ∫ s in a..x, 2 * (x - 1 * s) / s ^ 3 := by
    apply intervalIntegral.integral_congr
    intro s hs
    rw [uIcc_of_le hax] at hs
    simp [max_eq_left (sub_nonneg.mpr hs.2)]
  rw [hz, he, affine_call_integral ha hax]
  field_simp
  ring

/-- The call kernel is continuous on a positive interval. -/
theorem continuousOn_call_kernel {a b x : ℝ} (ha : 0 < a) :
    ContinuousOn (fun s : ℝ => 2 * max (x - s) 0 / s ^ 3) (Icc a b) := by
  fun_prop (disch := intro s hs; exact pow_ne_zero 3 (ne_of_gt (ha.trans_le hs.1)))

/-- Formula (6), first for an arbitrary finite family of masses. -/
theorem finite_reciprocal_call_identity {ι : Type*} [Fintype ι] {a b : ℝ}
    (ha : 0 < a) (hab : a ≤ b) (p x : ι → ℝ)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) :
    (∑ i, p i / x i) = (∑ i, p i) / a -
      ((∑ i, p i * x i) - a * ∑ i, p i) / a ^ 2 +
        ∫ s in a..b, 2 * (∑ i, p i * max (x i - s) 0) / s ^ 3 := by
  have hi : ∀ i, IntervalIntegrable
      (fun s : ℝ => p i * (2 * max (x i - s) 0 / s ^ 3)) volume a b := by
    intro i
    apply IntervalIntegrable.const_mul
    apply ContinuousOn.intervalIntegrable
    simpa only [uIcc_of_le hab] using continuousOn_call_kernel (x := x i) ha
  have hs : (∫ s in a..b, 2 * (∑ i, p i * max (x i - s) 0) / s ^ 3) =
      ∑ i, p i * (∫ s in a..b, 2 * max (x i - s) 0 / s ^ 3) := by
    calc
      _ = ∫ s in a..b, ∑ i, p i * (2 * max (x i - s) 0 / s ^ 3) := by
        congr 1; funext s
        simp only [Finset.mul_sum, Finset.sum_div]
        apply Finset.sum_congr rfl
        intro i _; ring
      _ = _ := by rw [intervalIntegral.integral_finsetSum (fun i _ => hi i)]
                  simp only [intervalIntegral.integral_const_mul]
  rw [hs]
  calc
    _ = ∑ i, p i * (1 / a - (x i - a) / a ^ 2 +
        ∫ s in a..b, 2 * max (x i - s) 0 / s ^ 3) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [← reciprocal_call_identity ha (hx i).1 (hx i).2]
      ring
    _ = _ := by
      have ht : ∀ i, p i * (1 / a - (x i - a) / a ^ 2 +
          ∫ s in a..b, 2 * max (x i - s) 0 / s ^ 3) =
          p i / a - (p i * x i / a ^ 2 - p i * a / a ^ 2) +
          p i * (∫ s in a..b, 2 * max (x i - s) 0 / s ^ 3) := by
        intro i
        ring
      simp_rw [ht]
      simp only [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.sum_div,
        ← Finset.sum_mul]
      ring

/-- Every finite probability law satisfies the reciprocal call identity. -/
theorem Law.reciprocal_eq_call_integral {a b : ℝ} (μ : Law a b)
    (ha : 0 < a) (hab : a ≤ b) :
    μ.reciprocal = 1 / a - (μ.mean - a) / a ^ 2 +
      ∫ s in a..b, 2 * μ.call s / s ^ 3 := by
  simpa only [Law.reciprocal, Law.mean, Law.call, μ.total, mul_one] using
    finite_reciprocal_call_identity ha hab μ.mass μ.location μ.bounds

/-- Call-function dominance gives the claimed reciprocal-moment lower bound. -/
theorem Law.reciprocal_lower_of_call_le {a b : ℝ} (μ : Law a b)
    (ha : 0 < a) (hab : a ≤ b) {C : ℝ → ℝ} (hC : ContinuousOn C (Icc a b))
    (hle : ∀ s ∈ Icc a b, C s ≤ μ.call s) :
    1 / a - (μ.mean - a) / a ^ 2 + (∫ s in a..b, 2 * C s / s ^ 3) ≤
      μ.reciprocal := by
  rw [μ.reciprocal_eq_call_integral ha hab]
  apply add_le_add_right
  have hn : ∀ s ∈ Icc a b, s ^ 3 ≠ 0 := fun s hs =>
    pow_ne_zero 3 (ne_of_gt (ha.trans_le hs.1))
  have hC' : ContinuousOn (fun s : ℝ => 2 * C s / s ^ 3) (Icc a b) := by
    fun_prop (disch := aesop)
  have hμ : ContinuousOn (fun s : ℝ => 2 * μ.call s / s ^ 3) (Icc a b) := by
    unfold Law.call
    fun_prop (disch := aesop)
  apply intervalIntegral.integral_mono_on hab
    ((by simpa only [uIcc_of_le hab] using hC') :
      ContinuousOn (fun s : ℝ => 2 * C s / s ^ 3) (uIcc a b)).intervalIntegrable
    ((by simpa only [uIcc_of_le hab] using hμ) :
      ContinuousOn (fun s : ℝ => 2 * μ.call s / s ^ 3) (uIcc a b)).intervalIntegrable
  intro s hs
  exact div_le_div_of_nonneg_right (mul_le_mul_of_nonneg_left (hle s hs) (by norm_num))
    (pow_nonneg (ha.trans_le hs.1).le 3)

/-- For equal means, the call order implies the reciprocal-moment order. -/
theorem Law.reciprocal_mono {a b : ℝ} (μ ν : Law a b)
    (ha : 0 < a) (hab : a ≤ b) (hm : μ.mean = ν.mean)
    (hcall : ∀ s ∈ Icc a b, μ.call s ≤ ν.call s) : μ.reciprocal ≤ ν.reciprocal := by
  rw [μ.reciprocal_eq_call_integral ha hab, hm]
  apply ν.reciprocal_lower_of_call_le ha hab _ hcall
  unfold Law.call
  fun_prop

/-- Taylor's identity with the positive-part kernel, in an explicit derivative form.
The derivative hypotheses are the usual twice continuously differentiable case. -/
theorem twice_differentiable_call_identity {a b x : ℝ} {f f' f'' : ℝ → ℝ}
    (hax : a ≤ x) (hxb : x ≤ b)
    (hd : ∀ s ∈ Icc a b, HasDerivAt f (f' s) s)
    (hdd : ∀ s ∈ Icc a b, HasDerivAt f' (f'' s) s)
    (hc : ContinuousOn f'' (Icc a b)) :
    f x = f a + f' a * (x - a) + ∫ s in a..b, f'' s * max (x - s) 0 := by
  have hab := hax.trans hxb
  have hkernel : ContinuousOn (fun s => f'' s * max (x - s) 0) (uIcc a b) := by
    rw [uIcc_of_le hab]
    exact hc.mul (by fun_prop)
  have hia := (hkernel.intervalIntegrable (μ := volume)).mono_set (c := a) (d := x) (by
    simpa only [uIcc_of_le hax, uIcc_of_le hab] using Icc_subset_Icc_right hxb)
  have hib := (hkernel.intervalIntegrable (μ := volume)).mono_set (c := x) (d := b) (by
    simpa only [uIcc_of_le hxb, uIcc_of_le hab] using Icc_subset_Icc_left hax)
  have hz : (∫ s in x..b, f'' s * max (x - s) 0) = 0 := by
    calc
      _ = ∫ s in x..b, (0 : ℝ) := intervalIntegral.integral_congr (by
        intro s hs
        rw [uIcc_of_le hxb] at hs
        simp [max_eq_right (sub_nonpos.mpr hs.1)])
      _ = 0 := by simp
  have he : (∫ s in a..x, f'' s * max (x - s) 0) =
      ∫ s in a..x, f'' s * (x - s) := by
    apply intervalIntegral.integral_congr
    intro s hs
    rw [uIcc_of_le hax] at hs
    simp only [max_eq_left (sub_nonneg.mpr hs.2)]
  have hcont : ContinuousOn (fun s => f'' s * (x - s)) (uIcc a x) := by
    rw [uIcc_of_le hax]
    exact (hc.mono (Icc_subset_Icc_right hxb)).mul (by fun_prop)
  have hderiv : ∀ s ∈ uIcc a x, HasDerivAt
      (fun s => f s + (x - s) * f' s) (f'' s * (x - s)) s := by
    intro s hs
    rw [uIcc_of_le hax] at hs
    have hs' : s ∈ Icc a b := ⟨hs.1, hs.2.trans hxb⟩
    convert! (hd s hs').add (((hasDerivAt_const s x).sub (hasDerivAt_id s)).mul
      (hdd s hs')) using 1
    dsimp
    ring
  have hi := intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hcont.intervalIntegrable
  rw [← intervalIntegral.integral_add_adjacent_intervals hia hib, hz, he, hi]
  ring

end ReciprocalAnchor.ManyLeaf
