import CertifiedMinlp.MonomialConcave
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Data.Matrix.Mul

/-! The actual directional Hessian of a real-power monomial on the positive orthant. -/
namespace CertifiedMinlp

open Finset Filter
open scoped Topology

variable {I : Type*} [Fintype I]

omit [Fintype I] in
private theorem hasDerivAt_prod_logarithmic {f : I → ℝ → ℝ} {g : I → ℝ} {t : ℝ}
    (s : Finset I) (h : ∀ i ∈ s, HasDerivAt (f i) (f i t * g i) t) :
    HasDerivAt (fun u => ∏ i ∈ s, f i u) ((∏ i ∈ s, f i t) * ∑ i ∈ s, g i) t := by
  classical
  induction s using Finset.induction_on with
  | empty => simpa using hasDerivAt_const t (1 : ℝ)
  | @insert i s hi ih =>
    simp only [Finset.mem_insert] at h
    have hd := (h i (Or.inl rfl)).mul (ih fun j hj => h j (Or.inr hj))
    simp only [Finset.prod_insert hi, Finset.sum_insert hi]
    convert! hd using 1
    ring

/-- First derivative of the actual monomial along an affine line. -/
theorem realMonomial_line_hasDerivAt (a x v : I → ℝ) (t : ℝ)
    (hx : ∀ i, 0 < x i + t * v i) :
    HasDerivAt (fun u => realMonomial a (fun i => x i + u * v i))
      (realMonomial a (fun i => x i + t * v i) *
        ∑ i, a i * v i / (x i + t * v i)) t := by
  apply hasDerivAt_prod_logarithmic
  intro i _
  have hd := ((hasDerivAt_id t).mul_const (v i)).const_add (x i)
  have hp := hd.rpow_const (p := a i) (Or.inl (ne_of_gt (hx i)))
  dsimp at hp
  rw [Real.rpow_sub_one (ne_of_gt (hx i))] at hp
  convert! hp using 1
  ring

/-- The derivative of the logarithmic slope along an affine line. -/
theorem realMonomial_slope_hasDerivAt (a x v : I → ℝ) (t : ℝ)
    (hx : ∀ i, 0 < x i + t * v i) :
    HasDerivAt (fun u => ∑ i, a i * v i / (x i + u * v i))
      (-∑ i, a i * (v i / (x i + t * v i)) ^ 2) t := by
  have hd : ∀ i ∈ (univ : Finset I),
      HasDerivAt (fun u => a i * v i / (x i + u * v i))
        (-(a i * (v i / (x i + t * v i)) ^ 2)) t := by
    intro i _
    have h := (hasDerivAt_const t (a i * v i)).div
      (((hasDerivAt_id t).mul_const (v i)).const_add (x i)) (ne_of_gt (hx i))
    dsimp at h
    convert! h using 1
    field_simp
    ring
  simpa only [Finset.sum_neg_distrib] using HasDerivAt.fun_sum hd

/-- Differentiating the explicit first derivative gives the Hessian quadratic form. -/
theorem realMonomial_line_slope_hasDerivAt (a x v : I → ℝ) (t : ℝ)
    (hx : ∀ i, 0 < x i + t * v i) :
    HasDerivAt (fun u => realMonomial a (fun i => x i + u * v i) *
        ∑ i, a i * v i / (x i + u * v i))
      (realMonomial a (fun i => x i + t * v i) *
        ((∑ i, a i * v i / (x i + t * v i)) ^ 2 -
          ∑ i, a i * (v i / (x i + t * v i)) ^ 2)) t := by
  convert! (realMonomial_line_hasDerivAt a x v t hx).mul
    (realMonomial_slope_hasDerivAt a x v t hx) using 1
  ring

/-- Literal second derivative along any line, without assuming a Hessian formula. -/
theorem realMonomial_line_second_deriv (a x v : I → ℝ) (t : ℝ)
    (hx : ∀ i, 0 < x i + t * v i) :
    deriv (deriv (fun u => realMonomial a (fun i => x i + u * v i))) t =
      realMonomial a (fun i => x i + t * v i) *
        ((∑ i, a i * v i / (x i + t * v i)) ^ 2 -
          ∑ i, a i * (v i / (x i + t * v i)) ^ 2) := by
  have hpos : ∀ᶠ u in 𝓝 t, ∀ i, 0 < x i + u * v i := by
    apply Filter.eventually_all.mpr
    intro i
    exact (continuous_const.add (continuous_id.mul continuous_const)).continuousAt.eventually
      (lt_mem_nhds (hx i))
  have heq : deriv (fun u => realMonomial a (fun i => x i + u * v i)) =ᶠ[𝓝 t]
      (fun u => realMonomial a (fun i => x i + u * v i) *
        ∑ i, a i * v i / (x i + u * v i)) := by
    filter_upwards [hpos] with u hu
    exact (realMonomial_line_hasDerivAt a x v u hu).deriv
  rw [heq.deriv_eq]
  exact (realMonomial_line_slope_hasDerivAt a x v t hx).deriv

/-- At the base point, this is the quadratic form of
`m(x) D (a aᵀ - diag a) D`, where `D = diag (1 / x)`. -/
theorem realMonomial_directional_hessian (a x v : I → ℝ) (hx : x ∈ positiveOrthant) :
    deriv (deriv (fun t => realMonomial a (fun i => x i + t * v i))) 0 =
      realMonomial a x * ((∑ i, a i * (v i / x i)) ^ 2 -
        ∑ i, a i * (v i / x i) ^ 2) := by
  simpa only [zero_mul, add_zero, mul_div_assoc] using
    realMonomial_line_second_deriv a x v 0 (by simpa [positiveOrthant] using hx)

/-- The matrix expression in the paper has exactly the directional quadratic form above. -/
theorem realMonomial_hessian_matrix_form [DecidableEq I] (a x v : I → ℝ) :
    dotProduct v
      ((Matrix.diagonal (fun i => 1 / x i) *
        (Matrix.vecMulVec a a - Matrix.diagonal a) *
          Matrix.diagonal (fun i => 1 / x i)).mulVec v) =
      (∑ i, a i * (v i / x i)) ^ 2 - ∑ i, a i * (v i / x i) ^ 2 := by
  simp only [← Matrix.mulVec_mulVec, Matrix.sub_mulVec, Matrix.vecMulVec_mulVec,
    dotProduct, Matrix.mulVec_diagonal, Pi.sub_apply, Pi.smul_apply, op_smul_eq_mul]
  have hi : (∑ i, a i * (1 / x i * v i)) = ∑ i, a i * (v i / x i) := by
    apply Finset.sum_congr rfl
    intro i _
    ring
  rw [hi]
  simp_rw [mul_sub]
  rw [Finset.sum_sub_distrib, pow_two, Finset.sum_mul]
  congr 1 <;> apply Finset.sum_congr rfl <;> intro i _ <;> ring

/-- The displayed Hessian formula, stated through its values in every direction. -/
theorem realMonomial_directional_hessian_matrix [DecidableEq I] (a x v : I → ℝ)
    (hx : x ∈ positiveOrthant) :
    deriv (deriv (fun t => realMonomial a (fun i => x i + t * v i))) 0 =
      realMonomial a x * dotProduct v
        ((Matrix.diagonal (fun i => 1 / x i) *
          (Matrix.vecMulVec a a - Matrix.diagonal a) *
            Matrix.diagonal (fun i => 1 / x i)).mulVec v) := by
  rw [realMonomial_hessian_matrix_form]
  exact realMonomial_directional_hessian a x v hx

end CertifiedMinlp
