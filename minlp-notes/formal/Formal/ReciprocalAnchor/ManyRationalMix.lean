import Formal.ReciprocalAnchor.ManyRationalSize

/-! Rational interpolation between a finite law and its endpoint law. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

variable {K : ℕ}

def rationalSecant (a b m : ℚ) : ℚ := (a + b - m) / (a * b)

def rationalMixWeight (a b m t T : ℚ) : ℚ :=
  (t - T) / (rationalSecant a b m - T)

def rationalMixMass (p : Fin K → ℚ) (a b m t T : ℚ) : Fin K ⊕ Fin 2 → ℚ :=
  Sum.elim (fun i => (1 - rationalMixWeight a b m t T) * p i)
    ![rationalMixWeight a b m t T * ((b - m) / (b - a)),
      rationalMixWeight a b m t T * ((m - a) / (b - a))]

def rationalMixLocation (x : Fin K → ℚ) (a b : ℚ) : Fin K ⊕ Fin 2 → ℚ :=
  Sum.elim x ![a, b]

theorem rationalMixWeight_bounds {a b m t T : ℚ}
    (hT : T ≤ t) (ht : t ≤ rationalSecant a b m) :
    0 ≤ rationalMixWeight a b m t T ∧ rationalMixWeight a b m t T ≤ 1 := by
  have hd : 0 ≤ rationalSecant a b m - T := by linarith
  refine ⟨div_nonneg (sub_nonneg.mpr hT) hd, ?_⟩
  by_cases he : rationalSecant a b m - T = 0
  · simp [rationalMixWeight, he]
  · exact (div_le_one (lt_of_le_of_ne hd (Ne.symm he))).mpr (by linarith)

theorem rationalMixWeight_identity {a b m t T : ℚ}
    (hT : T ≤ t) (ht : t ≤ rationalSecant a b m) :
    (1 - rationalMixWeight a b m t T) * T +
      rationalMixWeight a b m t T * rationalSecant a b m = t := by
  by_cases he : rationalSecant a b m - T = 0
  · have htt : t = T := by linarith
    simp [rationalMixWeight, he, htt]
  · have h := div_mul_cancel₀ (t - T) he
    change rationalMixWeight a b m t T * (rationalSecant a b m - T) = t - T at h
    nlinarith

theorem rationalMixMass_nonneg (p : Fin K → ℚ) {a b m t T : ℚ}
    (hp : ∀ i, 0 ≤ p i) (hab : a < b) (hm : a ≤ m ∧ m ≤ b)
    (hT : T ≤ t) (ht : t ≤ rationalSecant a b m) :
    ∀ i, 0 ≤ rationalMixMass p a b m t T i := by
  obtain ⟨hr, hr1⟩ := rationalMixWeight_bounds hT ht
  rintro (i | i)
  · exact mul_nonneg (by linarith) (hp i)
  · fin_cases i <;> dsimp [rationalMixMass] <;>
      exact mul_nonneg hr (div_nonneg (sub_nonneg.mpr (by tauto)) (sub_pos.mpr hab).le)

theorem rationalMixMass_total (p : Fin K → ℚ) {a b m t T : ℚ}
    (hp : ∑ i, p i = 1) (hab : a < b) :
    ∑ i, rationalMixMass p a b m t T i = 1 := by
  simp only [rationalMixMass, Fintype.sum_sum_type, Sum.elim_inl, Sum.elim_inr,
    Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one, ← Finset.mul_sum, hp]
  have hba : b - a ≠ 0 := ne_of_gt (sub_pos.mpr hab)
  field_simp
  ring

theorem rationalMixLocation_bounds (x : Fin K → ℚ) {a b : ℚ}
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hab : a ≤ b) :
    ∀ i, a ≤ rationalMixLocation x a b i ∧ rationalMixLocation x a b i ≤ b := by
  rintro (i | i)
  · exact hx i
  · fin_cases i <;> simp [rationalMixLocation, hab]

theorem rationalMix_mean (p x : Fin K → ℚ) {a b m t T : ℚ}
    (hm : ∑ i, p i * x i = m) (hab : a < b) :
    (∑ i, rationalMixMass p a b m t T i * rationalMixLocation x a b i) = m := by
  simp only [rationalMixMass, rationalMixLocation, Fintype.sum_sum_type,
    Sum.elim_inl, Sum.elim_inr, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  simp_rw [mul_assoc]
  rw [← Finset.mul_sum, hm]
  have hba : b - a ≠ 0 := ne_of_gt (sub_pos.mpr hab)
  field_simp
  ring

theorem rationalMix_reciprocal (p x : Fin K → ℚ) {a b m t T : ℚ}
    (hrec : ∑ i, p i / x i = T) (ha : 0 < a) (hab : a < b)
    (hT : T ≤ t) (ht : t ≤ rationalSecant a b m) :
    (∑ i, rationalMixMass p a b m t T i / rationalMixLocation x a b i) = t := by
  simp only [rationalMixMass, rationalMixLocation, Fintype.sum_sum_type,
    Sum.elim_inl, Sum.elim_inr, Fin.sum_univ_two, Matrix.cons_val_zero, Matrix.cons_val_one]
  simp_rw [mul_div_assoc]
  rw [← Finset.mul_sum, hrec]
  have he : (b - m) / (b - a) / a + (m - a) / (b - a) / b = rationalSecant a b m := by
    have ha0 := ne_of_gt ha
    have hb0 := ne_of_gt (ha.trans hab)
    have hba := ne_of_gt (sub_pos.mpr hab)
    unfold rationalSecant
    field_simp
    ring
  calc
    _ = (1 - rationalMixWeight a b m t T) * T + rationalMixWeight a b m t T *
        ((b - m) / (b - a) / a + (m - a) / (b - a) / b) := by ring
    _ = t := by rw [he]; exact rationalMixWeight_identity hT ht

theorem rationalMix_cardinality : Fintype.card (Fin K ⊕ Fin 2) = K + 2 := by simp

theorem rationalSecant_bits {a b m : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B) :
    RationalBits (rationalSecant a b m) (5 * B + 2) := by
  convert rationalBits_div (rationalBits_sub (rationalBits_add ha hb) hm)
    (rationalBits_mul ha hb) using 1 <;> first | rfl | omega

theorem rationalMixWeight_bits {a b m t T : ℚ} {B : ℕ}
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hT : RationalBits T B) :
    RationalBits (rationalMixWeight a b m t T) (8 * B + 4) := by
  convert rationalBits_div (rationalBits_sub ht hT)
    (rationalBits_sub (rationalSecant_bits ha hb hm) hT) using 1 <;> first | rfl | omega

/-- Every output mass has linear bit length in the input coordinate bound. -/
theorem rationalMixMass_bits (p : Fin K → ℚ) {a b m t T : ℚ} {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B)
    (ha : RationalBits a B) (hb : RationalBits b B) (hm : RationalBits m B)
    (ht : RationalBits t B) (hT : RationalBits T B) :
    ∀ i, RationalBits (rationalMixMass p a b m t T i) (12 * B + 6) := by
  have hr := rationalMixWeight_bits ha hb hm ht hT
  have hba := rationalBits_sub hb ha
  rintro (i | i)
  · exact rationalBits_mono
      (rationalBits_mul (rationalBits_sub rationalBits_one hr) (hp i)) (by omega)
  · fin_cases i
    · exact rationalBits_mono
        (rationalBits_mul hr (rationalBits_div (rationalBits_sub hb hm) hba)) (by omega)
    · exact rationalBits_mono
        (rationalBits_mul hr (rationalBits_div (rationalBits_sub hm ha) hba)) (by omega)

theorem rationalMixLocation_bits (x : Fin K → ℚ) {a b : ℚ} {B : ℕ}
    (hx : ∀ i, RationalBits (x i) B) (ha : RationalBits a B) (hb : RationalBits b B) :
    ∀ i, RationalBits (rationalMixLocation x a b i) B := by
  rintro (i | i)
  · exact hx i
  · fin_cases i
    · exact ha
    · exact hb

end ReciprocalAnchor.ManyLeaf
