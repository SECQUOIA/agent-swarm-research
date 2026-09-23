import Mathlib

/-!
# The LP equations behind the coupling model

The normal matrix and its split are constructed from the actual constraint
matrix and central primal/slack coordinates. No norm convention is needed in
these algebraic identities.
-/

namespace QipmFormal.Coupling
noncomputable section
open scoped BigOperators
open Matrix

variable {m n : Type*} [Fintype m] [Fintype n] [DecidableEq n]

def normalMatrix (A : Matrix m n ℝ) (x s : n → ℝ) : Matrix m m ℝ :=
  A * diagonal (fun i => x i / s i) * A.transpose

def weightedGram (A : Matrix m n ℝ) (w : n → ℝ) : Matrix m m ℝ :=
  A * diagonal w * A.transpose

omit [Fintype n] in
/-- Complementarity gives the active and inactive weights exactly. -/
theorem central_weight_split (x s : n → ℝ) (B : Finset n) (μ : ℝ)
    (hμ : μ ≠ 0) (hs : ∀ i, s i ≠ 0) (hc : ∀ i, x i * s i = μ) :
    (fun i => x i / s i) =
      μ⁻¹ • (fun i => if i ∈ B then x i ^ 2 else 0) +
      μ • (fun i => if i ∈ B then 0 else (s i)⁻¹ ^ 2) := by
  funext i
  simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  split_ifs with hi
  · simp only [mul_zero, add_zero]
    field_simp [hμ, hs i]
    rw [← hc i]
    ring
  · simp only [mul_zero, zero_add]
    field_simp [hμ, hs i]
    nlinarith [hc i]

omit [Fintype m] in
/-- The equality-normal matrix is `μ⁻¹ C + μ D`, with actual Gram matrices. -/
theorem normalMatrix_split (A : Matrix m n ℝ) (x s : n → ℝ) (B : Finset n)
    (μ : ℝ) (hμ : μ ≠ 0) (hs : ∀ i, s i ≠ 0)
    (hc : ∀ i, x i * s i = μ) :
    normalMatrix A x s =
      μ⁻¹ • weightedGram A (fun i => if i ∈ B then x i ^ 2 else 0) +
      μ • weightedGram A (fun i => if i ∈ B then 0 else (s i)⁻¹ ^ 2) := by
  unfold normalMatrix weightedGram
  rw [central_weight_split x s B μ hμ hs hc]
  change A * diagonal (fun i =>
      (μ⁻¹ • (fun i => if i ∈ B then x i ^ 2 else 0)) i +
      (μ • (fun i => if i ∈ B then 0 else (s i)⁻¹ ^ 2)) i) * A.transpose = _
  rw [← diagonal_add]
  simp only [diagonal_smul, Matrix.mul_add, Matrix.add_mul,
    Matrix.mul_smul, Matrix.smul_mul]

/-- Elimination of the actual primal and dual Newton equations. -/
theorem exact_center_newton_rhs (A : Matrix m n ℝ) (x s dx ds : n → ℝ)
    (b dy : m → ℝ) (μ σ : ℝ)
    (hs : ∀ i, s i ≠ 0) (hc : ∀ i, x i * s i = μ)
    (hprimal : A *ᵥ x = b) (hdx : A *ᵥ dx = 0)
    (hdual : A.transpose *ᵥ dy + ds = 0)
    (hnewton : ∀ i, s i * dx i + x i * ds i = -(1 - σ) * μ) :
    normalMatrix A x s *ᵥ dy = (1 - σ) • b := by
  have hds (i : n) : ds i = -(A.transpose *ᵥ dy) i := by
    have h := congrFun hdual i
    simp only [Pi.add_apply, Pi.zero_apply] at h
    linarith
  have hcoord : diagonal (fun i => x i / s i) *ᵥ (A.transpose *ᵥ dy) =
      dx + (1 - σ) • x := by
    ext i
    simp only [mulVec_diagonal, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    have h := hnewton i
    rw [hds i, ← hc i] at h
    field_simp [hs i]
    nlinarith
  simp only [normalMatrix, ← mulVec_mulVec, hcoord, mulVec_add, mulVec_smul,
    hdx, hprimal, zero_add]

end
end QipmFormal.Coupling
