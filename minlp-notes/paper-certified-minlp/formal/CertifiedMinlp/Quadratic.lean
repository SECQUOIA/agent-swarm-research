import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.Convex.Function
import Mathlib.Tactic

/-! Exact global curvature of finite quadratic polynomials. -/
namespace CertifiedMinlp

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The polynomial represented by a quadratic matrix, linear coefficients, and a constant. -/
def quadratic (Q : Matrix n n ℝ) (b : n → ℝ) (c : ℝ) (x : n → ℝ) : ℝ :=
  Q.toBilin' x x + b ⬝ᵥ x + c

/-- The exact Jensen deficit, including cancellation of the affine part. -/
theorem quadratic_jensen_identity (Q : Matrix n n ℝ) (b : n → ℝ) (c : ℝ)
    (x y : n → ℝ) {s t : ℝ} (hst : s + t = 1) :
    s * quadratic Q b c x + t * quadratic Q b c y -
      quadratic Q b c (s • x + t • y) =
      s * t * Q.toBilin' (x - y) (x - y) := by
  simp only [quadratic, map_add, map_smul, LinearMap.add_apply,
    LinearMap.smul_apply, smul_eq_mul, map_sub, LinearMap.sub_apply,
    dotProduct_add, dotProduct_smul]
  have ht : t = 1 - s := by linarith
  rw [ht]
  ring

/-- Global convexity is equivalent to nonnegativity of the quadratic form.
This statement even allows nonsymmetric coefficient matrices. -/
theorem quadratic_convex_iff_nonneg (Q : Matrix n n ℝ) (b : n → ℝ) (c : ℝ) :
    ConvexOn ℝ Set.univ (quadratic Q b c) ↔ ∀ x, 0 ≤ Q.toBilin' x x := by
  constructor
  · intro h x
    have hm : quadratic Q b c ((1 / 2 : ℝ) • x + (1 / 2 : ℝ) • (-x)) ≤
        (1 / 2 : ℝ) • quadratic Q b c x + (1 / 2 : ℝ) • quadratic Q b c (-x) :=
      h.2 (Set.mem_univ x) (Set.mem_univ (-x)) (by norm_num) (by norm_num)
        (by norm_num)
    have hi := quadratic_jensen_identity Q b c x (-x)
      (s := (1 / 2 : ℝ)) (t := (1 / 2 : ℝ)) (by norm_num)
    have hd : x - -x = (2 : ℝ) • x := by ext i; simp; ring
    rw [hd] at hi
    simp only [map_smul, LinearMap.smul_apply, smul_eq_mul] at hi
    simp only [smul_eq_mul] at hm
    nlinarith
  · intro h
    refine ⟨convex_univ, fun x _ y _ s t hs ht hst => ?_⟩
    have hp := mul_nonneg (mul_nonneg hs ht) (h (x - y))
    rw [← quadratic_jensen_identity Q b c x y hst] at hp
    simpa only [smul_eq_mul] using (sub_nonneg.mp hp)

/-- For a symmetric real matrix, the exact global convexity test is positive
semidefiniteness. Linear and constant coefficients do not affect this test. -/
theorem quadratic_convex_iff_posSemidef (Q : Matrix n n ℝ)
    (hQ : Q.IsHermitian) (b : n → ℝ) (c : ℝ) :
    ConvexOn ℝ Set.univ (quadratic Q b c) ↔ Q.PosSemidef := by
  rw [quadratic_convex_iff_nonneg, Matrix.posSemidef_iff_dotProduct_mulVec]
  simp only [Matrix.toBilin'_apply', star_trivial, hQ, true_and]

/-- Restricting the global test to any convex domain, including a box with
fixed coordinates, preserves convexity. -/
theorem quadratic_convex_on (Q : Matrix n n ℝ) (hQ : Q.PosSemidef)
    (b : n → ℝ) (c : ℝ) (S : Set (n → ℝ)) (hS : Convex ℝ S) :
    ConvexOn ℝ S (quadratic Q b c) :=
  ((quadratic_convex_iff_posSemidef Q hQ.isHermitian b c).2 hQ).subset
    (Set.subset_univ _) hS

/-- The bilinear representation is the usual matrix quadratic polynomial. -/
theorem quadratic_eq_matrix (Q : Matrix n n ℝ) (b : n → ℝ) (c : ℝ)
    (x : n → ℝ) : quadratic Q b c x = x ⬝ᵥ Q *ᵥ x + b ⬝ᵥ x + c := by
  simp [quadratic, Matrix.toBilin'_apply']

/-- Testing the negative matrix gives the exact global concavity test. -/
theorem quadratic_concave_iff_neg_posSemidef (Q : Matrix n n ℝ)
    (hQ : Q.IsHermitian) (b : n → ℝ) (c : ℝ) :
    ConcaveOn ℝ Set.univ (quadratic Q b c) ↔ (-Q).PosSemidef := by
  have he : quadratic (-Q) (-b) (-c) = -quadratic Q b c := by
    funext x
    simp [quadratic, neg_add_rev]
    ring
  rw [← neg_convexOn_iff, ← he]
  exact quadratic_convex_iff_posSemidef (-Q) hQ.neg (-b) (-c)

/-- Splitting an off-diagonal monomial coefficient equally between its two
symmetric matrix entries preserves that monomial exactly. -/
theorem quadratic_offDiagonal_split (a x y : ℝ) :
    x * (a / 2) * y + y * (a / 2) * x = a * x * y := by ring

end CertifiedMinlp
