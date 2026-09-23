import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Algebra.Order.Star.Real
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic

namespace CertifiedMinlp
open Finset Matrix
variable {I : Type*} [Fintype I]

/-- Weighted Cauchy--Schwarz, with zero weights allowed. -/
theorem monomial_weighted_cauchy (a u : I → ℝ) (ha : ∀ i, 0 ≤ a i) :
    (∑ i, a i * u i) ^ 2 ≤ (∑ i, a i) * ∑ i, a i * u i ^ 2 := by
  apply Finset.sum_sq_le_sum_mul_sum_of_sq_le_mul univ
    (fun i _ ↦ ha i) (fun i _ ↦ mul_nonneg (ha i) (sq_nonneg _))
    (fun i _ ↦ ?_)
  ring_nf
  exact le_refl _

theorem monomial_middle_nonnegative (a u : I → ℝ) (ha : ∀ i, a i ≤ 0) :
    0 ≤ (∑ i, a i * u i)^2 - ∑ i, a i * u i^2 := by
  have H : ∑ i, a i * u i^2 ≤ 0 :=
    Finset.sum_nonpos fun i _ ↦ mul_nonpos_of_nonpos_of_nonneg (ha i) (sq_nonneg _)
  nlinarith [sq_nonneg (∑ i, a i * u i)]

theorem monomial_middle_nonpositive (a u : I → ℝ) (ha : ∀ i, 0 ≤ a i)
    (hs : ∑ i, a i ≤ 1) :
    (∑ i, a i * u i)^2 - ∑ i, a i * u i^2 ≤ 0 := by
  have H := monomial_weighted_cauchy a u ha
  have hsum : 0 ≤ ∑ i, a i * u i^2 :=
    Finset.sum_nonneg fun i _ ↦ mul_nonneg (ha i) (sq_nonneg _)
  nlinarith [mul_nonneg (sub_nonneg.mpr hs) hsum]

/-- The one-positive-exponent middle form is nonnegative. This includes zero
negative weights and the empty negative block. -/
theorem monomial_middle_one_positive (b v : I → ℝ) (p u : ℝ)
    (hb : ∀ i, 0 ≤ b i) (hp : 1 + ∑ i, b i ≤ p) :
    0 ≤ (p * u - ∑ i, b i * v i)^2 - p * u^2 + ∑ i, b i * v i^2 := by
  let q := p * u - ∑ i, b i * v i
  let w : Option I → ℝ := Option.elim' 1 b
  let z : Option I → ℝ := Option.elim' q v
  have hw : ∀ i, 0 ≤ w i := by
    intro i; cases i with
    | none => exact zero_le_one
    | some i => exact hb i
  have H := monomial_weighted_cauchy w z hw
  simp only [w, z, Fintype.sum_option, Option.elim'_none, Option.elim'_some, one_mul] at H
  have hB : 0 ≤ ∑ i, b i := Finset.sum_nonneg fun i _ ↦ hb i
  have hV : 0 ≤ ∑ i, b i * v i^2 :=
    Finset.sum_nonneg fun i _ ↦ mul_nonneg (hb i) (sq_nonneg _)
  have hQ : 0 ≤ q^2 + ∑ i, b i * v i^2 := add_nonneg (sq_nonneg _) hV
  have hmul := mul_le_mul_of_nonneg_right hp hQ
  have hlin : q + ∑ i, b i * v i = p * u := by dsimp [q]; ring
  rw [hlin] at H
  have hp0 : 0 < p := by linarith
  have hbound : p * u^2 ≤ q^2 + ∑ i, b i * v i^2 := by
    nlinarith
  dsimp [q] at hbound
  linarith

variable [DecidableEq I]

noncomputable def monomialLowerBlock (b : I → ℝ) : Matrix I I ℝ :=
  Matrix.diagonal b + Matrix.vecMulVec b b

omit [Fintype I] in
theorem monomialLowerBlock_posDef [Finite I] (b : I → ℝ) (hb : ∀ i, 0 < b i) :
    (monomialLowerBlock b).PosDef := by
  exact (Matrix.PosDef.diagonal hb).add_posSemidef
    (by simpa using Matrix.posSemidef_vecMulVec_self_star b)

theorem monomialLowerBlock_mulVec (b : I → ℝ) (hb : ∀ i, 0 ≤ b i) :
    monomialLowerBlock b *ᵥ (fun _ ↦ 1 / (1 + ∑ i, b i)) = b := by
  have hd : 1 + ∑ i, b i ≠ 0 := by
    have H := Finset.sum_nonneg (fun i (_ : i ∈ univ) ↦ hb i)
    linarith
  ext i
  simp [monomialLowerBlock, Matrix.add_mulVec, Matrix.mulVec_diagonal,
    Matrix.vecMulVec_mulVec, dotProduct, ← Finset.sum_mul]
  field_simp

theorem monomialLowerBlock_inverse_quadratic (b : I → ℝ) (hb : ∀ i, 0 < b i) :
    b ⬝ᵥ ((monomialLowerBlock b)⁻¹ *ᵥ b) = (∑ i, b i) / (1 + ∑ i, b i) := by
  have hdet := (Matrix.isUnit_iff_isUnit_det _).mp (monomialLowerBlock_posDef b hb).isUnit
  have H := monomialLowerBlock_mulVec b (fun i ↦ (hb i).le)
  have HI : (monomialLowerBlock b)⁻¹ *ᵥ b = fun _ ↦ 1 / (1 + ∑ i, b i) := by
    calc
      _ = (monomialLowerBlock b)⁻¹ *ᵥ
          (monomialLowerBlock b *ᵥ fun _ ↦ 1 / (1 + ∑ i, b i)) := congrArg _ H.symm
      _ = _ := by rw [Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ hdet, Matrix.one_mulVec]
  rw [HI]
  simp [dotProduct, ← Finset.sum_mul, div_eq_mul_inv]

theorem monomial_schur (p B : ℝ) (hB : 0 ≤ B) (hp : 1 + B ≤ p) :
    p * (p - 1) - p^2 * B / (1 + B) = p * (p - 1 - B) / (1 + B) ∧
      0 ≤ p * (p - 1 - B) / (1 + B) := by
  have hd : 1 + B ≠ 0 := by linarith
  constructor
  · field_simp; ring
  · apply div_nonneg
    · apply mul_nonneg <;> linarith
    · linarith

end CertifiedMinlp
