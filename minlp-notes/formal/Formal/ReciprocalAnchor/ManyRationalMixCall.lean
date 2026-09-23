import Formal.ReciprocalAnchor.ManyRationalMix

/-! Mixing a finite rational law with its endpoint law preserves call inequalities. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

variable {K : ℕ}

def rationalEndpointCall (a b m s : ℚ) : ℚ :=
  (b - m) / (b - a) * max (a - s) 0 + (m - a) / (b - a) * max (b - s) 0

theorem rational_call_secant {a b x : ℚ} (hab : a < b)
    (hx : a ≤ x ∧ x ≤ b) (s : ℚ) :
    max (x - s) 0 ≤ rationalEndpointCall a b x s := by
  have h₁ : 0 ≤ (b - x) / (b - a) :=
    div_nonneg (sub_nonneg.mpr hx.2) (sub_pos.mpr hab).le
  have h₂ : 0 ≤ (x - a) / (b - a) :=
    div_nonneg (sub_nonneg.mpr hx.1) (sub_pos.mpr hab).le
  apply max_le
  · calc
      x - s = (b - x) / (b - a) * (a - s) + (x - a) / (b - a) * (b - s) := by
        field_simp [ne_of_gt (sub_pos.mpr hab)]
        ring
      _ ≤ _ := add_le_add (mul_le_mul_of_nonneg_left (le_max_left _ _) h₁)
        (mul_le_mul_of_nonneg_left (le_max_left _ _) h₂)
  · exact add_nonneg (mul_nonneg h₁ (le_max_right _ _))
      (mul_nonneg h₂ (le_max_right _ _))

theorem rational_call_le_endpoints (p x : Fin K → ℚ) {a b m : ℚ}
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hm : ∑ i, p i * x i = m)
    (hab : a < b) (s : ℚ) :
    (∑ i, p i * max (x i - s) 0) ≤ rationalEndpointCall a b m s := by
  calc
    (∑ i, p i * max (x i - s) 0) ≤
        ∑ i, p i * rationalEndpointCall a b (x i) s :=
      Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (rational_call_secant hab (hx i) s) (hp i)
    _ = _ := by
      unfold rationalEndpointCall
      simp only [mul_add, Finset.sum_add_distrib, ← mul_assoc, ← Finset.sum_mul]
      have hleft : (∑ i, p i * ((b - x i) / (b - a))) = (b - m) / (b - a) := by
        simp only [← mul_div_assoc, ← Finset.sum_div, mul_sub, Finset.sum_sub_distrib,
          ← Finset.sum_mul, hp1, one_mul, hm]
      have hright : (∑ i, p i * ((x i - a) / (b - a))) = (m - a) / (b - a) := by
        simp only [← mul_div_assoc, ← Finset.sum_div, mul_sub, Finset.sum_sub_distrib,
          ← Finset.sum_mul, hp1, one_mul, hm]
      rw [hleft, hright]

theorem rationalMix_call (p x : Fin K → ℚ) (a b m t T s : ℚ) :
    (∑ i, rationalMixMass p a b m t T i * max (rationalMixLocation x a b i - s) 0) =
      (1 - rationalMixWeight a b m t T) * (∑ i, p i * max (x i - s) 0) +
        rationalMixWeight a b m t T * rationalEndpointCall a b m s := by
  simp only [rationalMixMass, rationalMixLocation, Fintype.sum_sum_type,
    Sum.elim_inl, Sum.elim_inr, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  simp_rw [mul_assoc]
  rw [← Finset.mul_sum]
  unfold rationalEndpointCall
  ring

/-- Endpoint interpolation can only increase the call function at every threshold. -/
theorem rational_call_le_mix (p x : Fin K → ℚ) {a b m t T : ℚ}
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hm : ∑ i, p i * x i = m)
    (hab : a < b) (hT : T ≤ t) (ht : t ≤ rationalSecant a b m) (s : ℚ) :
    (∑ i, p i * max (x i - s) 0) ≤
      ∑ i, rationalMixMass p a b m t T i * max (rationalMixLocation x a b i - s) 0 := by
  rw [rationalMix_call]
  have h := rational_call_le_endpoints p x hp hp1 hx hm hab s
  have hr := (rationalMixWeight_bounds hT ht).1
  nlinarith [mul_nonneg hr (sub_nonneg.mpr h)]

/-- Every leaf realizable on the base law remains admissible after interpolation. -/
theorem rationalMix_preserves_leaf_calls (p x : Fin K → ℚ) {a b m t T q w : ℚ}
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hm : ∑ i, p i * x i = m)
    (hab : a < b) (hT : T ≤ t) (ht : t ≤ rationalSecant a b m)
    (hcall : ∀ s, w - q * s ≤ (∑ i, p i * max (x i - s) 0) ∧
      m - w - (1 - q) * s ≤ (∑ i, p i * max (x i - s) 0)) :
    ∀ s, w - q * s ≤
      (∑ i, rationalMixMass p a b m t T i * max (rationalMixLocation x a b i - s) 0) ∧
      m - w - (1 - q) * s ≤
      (∑ i, rationalMixMass p a b m t T i * max (rationalMixLocation x a b i - s) 0) := by
  intro s
  have h := rational_call_le_mix p x hp hp1 hx hm hab hT ht s
  exact ⟨(hcall s).1.trans h, (hcall s).2.trans h⟩

end ReciprocalAnchor.ManyLeaf
