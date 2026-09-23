import CertifiedMinlp.Quadratic
import CertifiedMinlp.QuadraticElimination

/-! The elimination algorithm's finite-sum semantics agrees with ordinary
matrix PSD and the polynomial curvature theorem. -/
namespace CertifiedMinlp

open Matrix

/-- Elimination evaluates the same quadratic form as the matrix API. -/
theorem elimination_value_eq_bilinear {n : ℕ} (Q : Matrix (Fin n) (Fin n) ℝ)
    (x : Fin n → ℝ) : QuadraticElimination.value Q x = Q.toBilin' x x := by
  simp only [QuadraticElimination.value, Matrix.toBilin'_apply]
  apply Finset.sum_congr rfl
  intro i _
  apply Finset.sum_congr rfl
  intro j _
  ring

/-- For a symmetric matrix the algorithm's universal nonnegativity predicate
is exactly positive semidefiniteness, without extra definiteness assumptions. -/
theorem elimination_nonnegative_iff_posSemidef {n : ℕ}
    (Q : Matrix (Fin n) (Fin n) ℝ) (hQ : Q.IsSymm) :
    QuadraticElimination.Nonnegative Q ↔ Q.PosSemidef := by
  rw [QuadraticElimination.Nonnegative, Matrix.posSemidef_iff_dotProduct_mulVec]
  simp only [elimination_value_eq_bilinear, Matrix.toBilin'_apply', star_trivial,
    Matrix.isHermitian_iff_isSymm, hQ, true_and]

/-- Exact elimination's semantics is equivalent to global convexity of the
source quadratic, including arbitrary linear and constant terms. -/
theorem elimination_nonnegative_iff_convex {n : ℕ}
    (Q : Matrix (Fin n) (Fin n) ℝ) (b : Fin n → ℝ) (c : ℝ) :
    QuadraticElimination.Nonnegative Q ↔ ConvexOn ℝ Set.univ (quadratic Q b c) := by
  rw [quadratic_convex_iff_nonneg]
  simp only [QuadraticElimination.Nonnegative, elimination_value_eq_bilinear]

/-- The recursive field-arithmetic checker recognizes exactly the convex
quadratics when its input matrix is symmetric. -/
theorem quadratic_check_iff_convex {n : ℕ}
    (Q : Matrix (Fin n) (Fin n) ℝ) (hQ : Q.IsSymm)
    (b : Fin n → ℝ) (c : ℝ) :
    QuadraticElimination.check n Q = true ↔
      ConvexOn ℝ Set.univ (quadratic Q b c) :=
  (QuadraticElimination.check_iff n Q hQ).trans
    (elimination_nonnegative_iff_convex Q b c)

/-- Rational arithmetic alone decides PSD over all real vectors. -/
theorem rational_quadratic_check_iff_posSemidef {n : ℕ}
    (Q : Matrix (Fin n) (Fin n) ℚ) (hQ : Q.IsSymm) :
    QuadraticElimination.check n Q = true ↔
      (QuadraticElimination.realMatrix Q).PosSemidef :=
  (QuadraticElimination.rational_check_iff_real_nonnegative Q hQ).trans
    (elimination_nonnegative_iff_posSemidef _
      (QuadraticElimination.realMatrix_symmetric hQ))

/-- The exact rational elimination test recognizes global real convexity. -/
theorem rational_quadratic_check_iff_convex {n : ℕ}
    (Q : Matrix (Fin n) (Fin n) ℚ) (hQ : Q.IsSymm)
    (b : Fin n → ℝ) (c : ℝ) :
    QuadraticElimination.check n Q = true ↔
      ConvexOn ℝ Set.univ (quadratic (QuadraticElimination.realMatrix Q) b c) :=
  (QuadraticElimination.rational_check_iff_real_nonnegative Q hQ).trans
    (elimination_nonnegative_iff_convex _ b c)

end CertifiedMinlp
