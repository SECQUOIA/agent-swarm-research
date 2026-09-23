import Formal.DAGSpectral.PSDAlgebra

namespace DAGSpectral
open scoped BigOperators
open Matrix

theorem entrywise_quadratic_bound {n : ℕ} (D : RealMatrix n) {a : ℝ}
    (ha : 0 ≤ a) (hD : ∀ i j, |D i j| ≤ a) (x : Fin n → ℝ) :
    |x ⬝ᵥ (D *ᵥ x)| ≤ (n : ℝ) * a * (∑ i, x i ^ 2) := by
  have hp (i j : Fin n) : |x i * D i j * x j| ≤ a / 2 * (x i ^ 2 + x j ^ 2) := by
    rw [abs_mul, abs_mul]
    have h := mul_le_mul_of_nonneg_right
      (mul_le_mul_of_nonneg_left (hD i j) (abs_nonneg (x i))) (abs_nonneg (x j))
    have hs : 0 ≤ (|x i| - |x j|) ^ 2 := sq_nonneg _
    have hi := sq_abs (x i)
    have hj := sq_abs (x j)
    nlinarith [mul_nonneg ha hs]
  calc
    |x ⬝ᵥ (D *ᵥ x)| = |∑ i, ∑ j, x i * D i j * x j| := by
      simp only [dotProduct, Matrix.mulVec, Finset.mul_sum, mul_assoc]
    _ ≤ ∑ i, |∑ j, x i * D i j * x j| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, ∑ j, |x i * D i j * x j| :=
      Finset.sum_le_sum fun i _ => Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ i, ∑ j, a / 2 * (x i ^ 2 + x j ^ 2) :=
      Finset.sum_le_sum fun i _ => Finset.sum_le_sum fun j _ => hp i j
    _ = (n : ℝ) * a * (∑ i, x i ^ 2) := by
      simp only [mul_add, Finset.sum_add_distrib, ← Finset.mul_sum,
        Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
      ring

theorem entrywise_identity_bounds {n : ℕ} (D : RealMatrix n) (hD : D.IsHermitian)
    {a : ℝ} (ha : 0 ≤ a) (hb : ∀ i j, |D i j| ≤ a) :
    Loewner ((-(n : ℝ) * a) • (1 : RealMatrix n)) D ∧
      Loewner D (((n : ℝ) * a) • (1 : RealMatrix n)) := by
  constructor
  · apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
      (hD.sub (Matrix.isHermitian_one.smul (by rfl)))
    intro x
    have h := (abs_le.mp (entrywise_quadratic_bound D ha hb x)).1
    simp only [star_trivial, Matrix.sub_mulVec, Matrix.smul_mulVec,
      Matrix.one_mulVec, dotProduct_sub, dotProduct_smul, smul_eq_mul]
    simpa only [dotProduct, ← pow_two, sub_nonneg, neg_mul] using h
  · apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
      ((Matrix.isHermitian_one.smul (by rfl)).sub hD)
    intro x
    have h := (abs_le.mp (entrywise_quadratic_bound D ha hb x)).2
    simp only [star_trivial, Matrix.sub_mulVec, Matrix.smul_mulVec,
      Matrix.one_mulVec, dotProduct_sub, dotProduct_smul, smul_eq_mul]
    simpa only [dotProduct, ← pow_two, sub_nonneg] using h

theorem relativeSandwich_of_entrywise {n : ℕ} {A B : RealMatrix n}
    (hA : A.IsHermitian) (hB : B.IsHermitian) (hfloor : Loewner 1 A)
    {a η : ℝ} (ha : 0 ≤ a) (hη : (n : ℝ) * a ≤ η)
    (hentry : ∀ i j, |(B - A) i j| ≤ a) : RelativeSandwich η A B := by
  have hη0 : 0 ≤ η := le_trans (mul_nonneg (Nat.cast_nonneg _) ha) hη
  have hbound := entrywise_identity_bounds (B - A) (hB.sub hA) ha hentry
  have hlow : Loewner ((-η) • (1 : RealMatrix n)) (B - A) :=
    (psd_smul_mono Matrix.PosSemidef.one (by linarith)).trans hbound.1
  have hupp : Loewner (B - A) (η • (1 : RealMatrix n)) :=
    hbound.2.trans (psd_smul_mono Matrix.PosSemidef.one hη)
  have hf := hfloor.smul hη0
  constructor
  · unfold Loewner at *
    have h := hlow.add hf
    convert h using 1; module
  · unfold Loewner at *
    have h := hupp.add hf
    convert h using 1; module

end DAGSpectral
