import Mathlib.Analysis.Matrix.Order
import Mathlib.Tactic

/-! Real PSD order used by the rational DAG construction after scalar extension. -/
namespace DAGSpectral
open scoped BigOperators MatrixOrder
open Matrix

abbrev RealMatrix (n : ℕ) := Matrix (Fin n) (Fin n) ℝ

def Loewner {n : ℕ} (A B : RealMatrix n) : Prop := (B - A).PosSemidef

def RelativeSandwich {n : ℕ} (η : ℝ) (A B : RealMatrix n) : Prop :=
  Loewner ((1 - η) • A) B ∧ Loewner B ((1 + η) • A)

namespace Loewner
variable {n m : ℕ} {A B C : RealMatrix n}

theorem refl (A : RealMatrix n) : Loewner A A := by
  simp [Loewner, Matrix.PosSemidef.zero]

theorem trans (hAB : Loewner A B) (hBC : Loewner B C) : Loewner A C := by
  exact le_trans (show A ≤ B from hAB) (show B ≤ C from hBC)

theorem add (hAB : Loewner A B) {D : RealMatrix n} (hCD : Loewner C D) :
    Loewner (A + C) (B + D) := by
  exact add_le_add (show A ≤ B from hAB) (show C ≤ D from hCD)

theorem smul (hAB : Loewner A B) {a : ℝ} (ha : 0 ≤ a) :
    Loewner (a • A) (a • B) := by
  unfold Loewner at *
  simpa only [smul_sub] using hAB.smul ha

theorem congruence (hAB : Loewner A B) (K : Matrix (Fin m) (Fin n) ℝ) :
    Loewner (K * A * K.transpose) (K * B * K.transpose) := by
  unfold Loewner at *
  simpa only [Matrix.mul_sub, Matrix.sub_mul, conjTranspose_eq_transpose_of_trivial] using
    hAB.mul_mul_conjTranspose_same K

theorem quadratic (hAB : Loewner A B) (x : Fin n → ℝ) :
    x ⬝ᵥ (A *ᵥ x) ≤ x ⬝ᵥ (B *ᵥ x) := by
  have h := hAB.dotProduct_mulVec_nonneg x
  simpa only [star_trivial, Matrix.sub_mulVec, dotProduct_sub, sub_nonneg] using h

end Loewner

variable {n : ℕ} {A B : RealMatrix n} {η : ℝ}

theorem psd_smul_mono (hA : A.PosSemidef) {a b : ℝ} (hab : a ≤ b) :
    Loewner (a • A) (b • A) := by
  unfold Loewner
  simpa only [sub_smul] using hA.smul (sub_nonneg.mpr hab)

theorem RelativeSandwich.congruence (h : RelativeSandwich η A B)
    {m : ℕ} (K : Matrix (Fin m) (Fin n) ℝ) :
    RelativeSandwich η (K * A * K.transpose) (K * B * K.transpose) := by
  constructor
  · simpa only [Matrix.mul_smul, Matrix.smul_mul] using h.1.congruence K
  · simpa only [Matrix.mul_smul, Matrix.smul_mul] using h.2.congruence K

theorem RelativeSandwich.add_prior (h : RelativeSandwich η A B) (hη : 0 ≤ η)
    {H : RealMatrix n} (hH : H.PosSemidef) : RelativeSandwich η (A + H) (B + H) := by
  constructor
  · simpa only [smul_add, one_smul] using
      h.1.add (psd_smul_mono hH (show 1 - η ≤ 1 by linarith))
  · simpa only [smul_add, one_smul] using
      h.2.add (psd_smul_mono hH (show 1 ≤ 1 + η by linarith))

theorem RelativeSandwich.kernel_iff (h : RelativeSandwich η A B)
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hη : η < 1) (x : Fin n → ℝ) :
    A *ᵥ x = 0 ↔ B *ᵥ x = 0 := by
  have hAx : 0 ≤ x ⬝ᵥ (A *ᵥ x) := by simpa using hA.dotProduct_mulVec_nonneg x
  have hBx : 0 ≤ x ⬝ᵥ (B *ᵥ x) := by simpa using hB.dotProduct_mulVec_nonneg x
  have hlo := h.1.quadratic x
  have hup := h.2.quadratic x
  simp only [Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul] at hlo hup
  constructor
  · intro hx
    apply (hB.dotProduct_mulVec_zero_iff x).mp
    simp only [star_trivial]
    rw [hx, dotProduct_zero, mul_zero] at hup
    exact le_antisymm hup hBx
  · intro hx
    apply (hA.dotProduct_mulVec_zero_iff x).mp
    simp only [star_trivial]
    rw [hx, dotProduct_zero] at hlo
    nlinarith

end DAGSpectral
