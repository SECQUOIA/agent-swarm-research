import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Tactic

/-! Extremal eigenvalues and simultaneous conditioning under arbitrary congruences. -/
namespace QipmFormal.Preconditioner
noncomputable section
open Matrix
open scoped BigOperators
variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

def energy (A : Matrix n n ℝ) (x : n → ℝ) : ℝ := x ⬝ᵥ (A *ᵥ x)
def euclideanSq (x : n → ℝ) : ℝ := x ⬝ᵥ x

def minEigen (A : Matrix n n ℝ) (hA : A.IsHermitian) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty hA.eigenvalues

def maxEigen (A : Matrix n n ℝ) (hA : A.IsHermitian) : ℝ :=
  Finset.univ.sup' Finset.univ_nonempty hA.eigenvalues

/-- The ratio of the largest and smallest actual eigenvalues. -/
def spectralCondition (A : Matrix n n ℝ) (hA : A.IsHermitian) : ℝ :=
  maxEigen A hA / minEigen A hA

theorem minEigen_pos {A : Matrix n n ℝ} (hA : A.PosDef) : 0 < minEigen A hA.1 := by
  exact (Finset.lt_inf'_iff _).mpr (fun i _ => hA.eigenvalues_pos i)

theorem minEigen_le_maxEigen {A : Matrix n n ℝ} (hA : A.IsHermitian) :
    minEigen A hA ≤ maxEigen A hA := by
  let i : n := Classical.choice inferInstance
  exact (Finset.inf'_le _ (Finset.mem_univ i)).trans
    (Finset.le_sup' _ (Finset.mem_univ i))

omit [DecidableEq n] [Nonempty n] in
theorem energy_pos {A : Matrix n n ℝ} (hA : A.PosDef) {x : n → ℝ} (hx : x ≠ 0) :
    0 < energy A x := by simpa [energy] using hA.dotProduct_mulVec_pos hx

omit [DecidableEq n] [Nonempty n] in
theorem euclideanSq_pos {x : n → ℝ} (hx : x ≠ 0) : 0 < euclideanSq x := by
  apply lt_of_le_of_ne
  · exact Finset.sum_nonneg (fun i _ => mul_self_nonneg (x i))
  · exact Ne.symm (mt dotProduct_self_eq_zero.mp hx)

omit [Nonempty n] in
private theorem energy_spectral {A : Matrix n n ℝ} (hA : A.IsHermitian) (x : n → ℝ) :
    energy A x = ∑ i, hA.eigenvalues i *
      ((star (hA.eigenvectorUnitary : Matrix n n ℝ) *ᵥ x) i)^2 := by
  conv_lhs => rw [hA.spectral_theorem]
  simp only [energy, Unitary.conjStarAlgAut_apply, ← mulVec_mulVec]
  rw [dotProduct_mulVec]
  have he : x ᵥ* (hA.eigenvectorUnitary : Matrix n n ℝ) =
      star (hA.eigenvectorUnitary : Matrix n n ℝ) *ᵥ x := by
    ext i
    simp [vecMul, mulVec, dotProduct, mul_comm]
  rw [he]
  simp [dotProduct, mulVec_diagonal, pow_two, mul_left_comm]

omit [Nonempty n] in
private theorem euclideanSq_spectral {A : Matrix n n ℝ} (hA : A.IsHermitian) (x : n → ℝ) :
    euclideanSq x = ∑ i, ((star (hA.eigenvectorUnitary : Matrix n n ℝ) *ᵥ x) i)^2 := by
  let U : Matrix n n ℝ := hA.eigenvectorUnitary
  have hU : U * star U = 1 := Unitary.coe_mul_star_self _
  have he : (star U *ᵥ x) ⬝ᵥ (star U *ᵥ x) = x ⬝ᵥ x := by
    rw [dotProduct_mulVec]
    have hv : (star U *ᵥ x) ᵥ* star U = x := by
      rw [← vecMul_transpose]
      have hs : (star U)ᵀ = U := by simp [Matrix.star_eq_conjTranspose]
      rw [hs, vecMul_vecMul, hU, vecMul_one]
    rw [hv]
  simpa [euclideanSq, dotProduct, pow_two, U] using he.symm

theorem energy_bounds {A : Matrix n n ℝ} (hA : A.IsHermitian) (x : n → ℝ) :
    minEigen A hA * euclideanSq x ≤ energy A x ∧
      energy A x ≤ maxEigen A hA * euclideanSq x := by
  rw [energy_spectral hA, euclideanSq_spectral hA, Finset.mul_sum, Finset.mul_sum]
  constructor
  · exact Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_right
      (Finset.inf'_le _ (Finset.mem_univ i)) (sq_nonneg _)
  · exact Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_right
      (Finset.le_sup' _ (Finset.mem_univ i)) (sq_nonneg _)

omit [DecidableEq n] [Nonempty n] in
theorem euclideanSq_nonneg (x : n → ℝ) : 0 ≤ euclideanSq x :=
  Finset.sum_nonneg (fun i _ => mul_self_nonneg (x i))

theorem spectralCondition_pos {A : Matrix n n ℝ} (hA : A.PosDef) :
    0 < spectralCondition A hA.1 :=
  div_pos ((minEigen_pos hA).trans_le (minEigen_le_maxEigen hA.1)) (minEigen_pos hA)

/-- Any two quadratic Rayleigh quotients differ by at most the spectral condition number. -/
theorem energy_comparison {A : Matrix n n ℝ} (hA : A.PosDef) (x y : n → ℝ) :
    energy A x * euclideanSq y ≤
      spectralCondition A hA.1 * (energy A y * euclideanSq x) := by
  have hl := (energy_bounds hA.1 y).1
  have hu := (energy_bounds hA.1 x).2
  have hxy := mul_le_mul_of_nonneg_right hu (euclideanSq_nonneg y)
  have hyx := mul_le_mul_of_nonneg_right hl (euclideanSq_nonneg x)
  have hmm := minEigen_pos hA
  have hmx : 0 ≤ maxEigen A hA.1 :=
    ((minEigen_pos hA).trans_le (minEigen_le_maxEigen hA.1)).le
  have hp := mul_le_mul_of_nonneg_left hyx hmx
  dsimp [spectralCondition]
  rw [div_mul_eq_mul_div]
  apply (le_div_iff₀ hmm).mpr
  nlinarith [mul_le_mul_of_nonneg_right hxy hmm.le]

/-- The cross ratio of two forms is bounded by the product of their condition numbers. -/
theorem energy_cross_product_le {A B : Matrix n n ℝ} (hA : A.PosDef) (hB : B.PosDef)
    {x y : n → ℝ} (hx : x ≠ 0) (hy : y ≠ 0) :
    energy B x * energy A y ≤
      (spectralCondition A hA.1 * spectralCondition B hB.1) *
        (energy A x * energy B y) := by
  have h₀ := energy_comparison hA y x
  have h₁ := energy_comparison hB x y
  have hp := mul_le_mul h₀ h₁
    (mul_nonneg (energy_pos hB hx).le (euclideanSq_nonneg y))
    (mul_nonneg (spectralCondition_pos hA).le
      (mul_nonneg (energy_pos hA hx).le (euclideanSq_nonneg y)))
  have hs : 0 < euclideanSq x * euclideanSq y :=
    mul_pos (euclideanSq_pos hx) (euclideanSq_pos hy)
  apply (mul_le_mul_iff_left₀ hs).mp
  nlinarith [hp]

/-- Reciprocal witness ratios force one of two SPD matrices to be ill conditioned. -/
theorem paired_energy_minimax {A B : Matrix n n ℝ} (hA : A.PosDef) (hB : B.PosDef)
    {x y : n → ℝ} (hx : x ≠ 0) (hy : y ≠ 0) {t : ℝ} (ht : 0 ≤ t)
    (hxy : t * energy A x ≤ energy B x)
    (hyx : t * energy B y ≤ energy A y) :
    t ≤ max (spectralCondition A hA.1) (spectralCondition B hB.1) := by
  have hp := energy_cross_product_le hA hB hx hy
  have hlo := mul_le_mul hxy hyx
    (mul_nonneg ht (energy_pos hB hy).le) (energy_pos hB hx).le
  have he : 0 < energy A x * energy B y := mul_pos (energy_pos hA hx) (energy_pos hB hy)
  have ht2 : t * t ≤ spectralCondition A hA.1 * spectralCondition B hB.1 := by
    apply (mul_le_mul_iff_left₀ he).mp
    nlinarith [hlo, hp]
  by_contra hn
  have ha := (lt_of_le_of_lt (le_max_left _ _) (lt_of_not_ge hn))
  have hb := (lt_of_le_of_lt (le_max_right _ _) (lt_of_not_ge hn))
  have ha0 := spectralCondition_pos hA
  have hb0 := spectralCondition_pos hB
  nlinarith

omit [DecidableEq n] [Nonempty n] in
/-- Congruence transports quadratic energy exactly. -/
theorem energy_congruence (A P : Matrix n n ℝ) (x : n → ℝ) :
    energy (Pᵀ * A * P) x = energy A (P *ᵥ x) := by
  simp only [energy, ← mulVec_mulVec, dotProduct_mulVec]
  simp only [← vecMul_transpose, vecMul_vecMul, Matrix.mul_assoc]

omit [Nonempty n] in
/-- Every invertible congruence preserves positive definiteness. -/
theorem congruence_posDef {A P : Matrix n n ℝ} (hA : A.PosDef) (hP : IsUnit P) :
    (Pᵀ * A * P).PosDef := by
  simpa only [Matrix.star_eq_conjTranspose, Matrix.conjTranspose_eq_transpose_of_trivial]
    using hP.posDef_star_left_conjugate_iff.mpr hA

/-- A fixed invertible factor cannot suppress two reciprocal witness ratios. -/
theorem congruence_paired_minimax {A B P : Matrix n n ℝ}
    (hA : A.PosDef) (hB : B.PosDef) (hP : IsUnit P)
    {x y : n → ℝ} (hx : x ≠ 0) (hy : y ≠ 0) {t : ℝ} (ht : 0 ≤ t)
    (hxy : t * energy A x ≤ energy B x)
    (hyx : t * energy B y ≤ energy A y) :
    t ≤ max (spectralCondition (Pᵀ * A * P) (congruence_posDef hA hP).1)
      (spectralCondition (Pᵀ * B * P) (congruence_posDef hB hP).1) := by
  have hPP : P * P⁻¹ = 1 := mul_nonsing_inv P ((isUnit_iff_isUnit_det P).mp hP)
  have hpx : P *ᵥ (P⁻¹ *ᵥ x) = x := by rw [mulVec_mulVec, hPP, one_mulVec]
  have hpy : P *ᵥ (P⁻¹ *ᵥ y) = y := by rw [mulVec_mulVec, hPP, one_mulVec]
  have hx' : P⁻¹ *ᵥ x ≠ 0 := by intro hz; simp [hz] at hpx; exact hx hpx.symm
  have hy' : P⁻¹ *ᵥ y ≠ 0 := by intro hz; simp [hz] at hpy; exact hy hpy.symm
  apply paired_energy_minimax (congruence_posDef hA hP) (congruence_posDef hB hP)
    hx' hy' ht
  · simpa only [energy_congruence, hpx] using hxy
  · simpa only [energy_congruence, hpy] using hyx

omit [Nonempty n] in
private theorem eigenvector_sq_pos {A : Matrix n n ℝ} (hA : A.IsHermitian) (i : n) :
    0 < euclideanSq (hA.eigenvectorBasis i) := by
  apply euclideanSq_pos
  intro h
  apply hA.eigenvectorBasis.orthonormal.ne_zero i
  exact PiLp.ext (fun j => congrFun h j)

omit [Nonempty n] in
private theorem energy_eigenvector {A : Matrix n n ℝ} (hA : A.IsHermitian) (i : n) :
    energy A (hA.eigenvectorBasis i) =
      hA.eigenvalues i * euclideanSq (hA.eigenvectorBasis i) := by
  simp only [energy, hA.mulVec_eigenvectorBasis, dotProduct_smul, smul_eq_mul, euclideanSq]

/-- Quadratic bounds certify the condition number of the actual matrix. -/
theorem spectralCondition_le_of_bounds {A : Matrix n n ℝ} (hA : A.PosDef)
    {l u : ℝ} (hl : 0 < l)
    (hb : ∀ x : n → ℝ, l * euclideanSq x ≤ energy A x ∧ energy A x ≤ u * euclideanSq x) :
    spectralCondition A hA.1 ≤ u / l := by
  have hmin : l ≤ minEigen A hA.1 := by
    apply (Finset.le_inf'_iff _ _).mpr
    intro i _
    have h := (hb (hA.1.eigenvectorBasis i)).1
    rw [energy_eigenvector] at h
    exact (mul_le_mul_iff_left₀ (eigenvector_sq_pos hA.1 i)).mp h
  have hmax : maxEigen A hA.1 ≤ u := by
    apply (Finset.sup'_le_iff _ _).mpr
    intro i _
    have h := (hb (hA.1.eigenvectorBasis i)).2
    rw [energy_eigenvector] at h
    exact (mul_le_mul_iff_left₀ (eigenvector_sq_pos hA.1 i)).mp h
  exact div_le_div₀ (((minEigen_pos hA).trans_le (minEigen_le_maxEigen hA.1)).le.trans hmax)
    hmax hl hmin

omit [Nonempty n] in
theorem euclideanSq_mulVec_orthogonal {P : Matrix n n ℝ} (hP : Pᵀ * P = 1)
    (x : n → ℝ) : euclideanSq (P *ᵥ x) = euclideanSq x := by
  have h := energy_congruence (1 : Matrix n n ℝ) P x
  simpa [energy, euclideanSq, hP] using h.symm

/-- Orthogonal changes of coordinates preserve the spectral condition number. -/
theorem spectralCondition_orthogonal_congruence {A P : Matrix n n ℝ}
    (hA : A.PosDef) (hP : IsUnit P) (hPP : Pᵀ * P = 1) (hPP' : P * Pᵀ = 1) :
    spectralCondition (Pᵀ * A * P) (congruence_posDef hA hP).1 =
      spectralCondition A hA.1 := by
  apply le_antisymm
  · apply spectralCondition_le_of_bounds (congruence_posDef hA hP) (minEigen_pos hA)
    intro x
    simpa only [energy_congruence, euclideanSq_mulVec_orthogonal hPP] using
      energy_bounds hA.1 (P *ᵥ x)
  · apply spectralCondition_le_of_bounds hA (minEigen_pos (congruence_posDef hA hP))
    intro x
    have h := energy_bounds (congruence_posDef hA hP).1 (Pᵀ *ᵥ x)
    have hn : euclideanSq (Pᵀ *ᵥ x) = euclideanSq x :=
      euclideanSq_mulVec_orthogonal (by simpa using hPP') x
    simpa only [energy_congruence, mulVec_mulVec, hPP', one_mulVec, hn] using h
end
end QipmFormal.Preconditioner
