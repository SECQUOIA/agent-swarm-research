import Formal.QuadraticPrecision.Spectral
import Formal.QuadraticPrecision.AffineBoundary
import Formal.QuadraticPrecision.LowerContact
import Mathlib.Analysis.Convex.Function

open scoped BigOperators Matrix
open Matrix
namespace QuadraticPrecision
variable {ι : Type*} [Fintype ι] [DecidableEq ι]

theorem eigenvalues_nonneg_of_negativeInertia_zero {H : Matrix ι ι ℝ}
    (hH : H.IsHermitian) (hz : negativeInertia hH = 0) : ∀ j, 0 ≤ hH.eigenvalues j := by
  have hn : IsEmpty {j // hH.eigenvalues j < 0} := Fintype.card_eq_zero_iff.mp hz
  intro j
  by_contra h
  exact hn.false ⟨j, lt_of_not_ge h⟩

theorem spectralCoordinate_mix {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (j : ι) (x y : ι → ℝ) (s t : ℝ) :
    spectralCoordinate hH j (s • x + t • y) =
      s * spectralCoordinate hH j x + t * spectralCoordinate hH j y := by
  simp [spectralCoordinate_eq_dotProduct, dotProduct_add, dotProduct_smul]

/-- The spectral criterion implies convexity of the actual polynomial on every
convex domain. Affine terms are arbitrary. -/
theorem spectral_quadratic_convexOn {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (heig : ∀ j, 0 ≤ hH.eigenvalues j) (a : ι → ℝ) (b : ℝ)
    (D : Set (ι → ℝ)) (hD : Convex ℝ D) :
    ConvexOn ℝ D (fun x => dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b) := by
  refine ⟨hD, ?_⟩
  intro x hx y hy s t hs ht hst
  simp only [spectral_quadratic hH, spectralCoordinate_mix,
    add_dotProduct, smul_dotProduct, smul_eq_mul]
  have hterm : ∀ j,
      hH.eigenvalues j * (s * spectralCoordinate hH j x + t * spectralCoordinate hH j y)^2 ≤
      s * (hH.eigenvalues j * spectralCoordinate hH j x ^ 2) +
      t * (hH.eigenvalues j * spectralCoordinate hH j y ^ 2) := by
    intro j
    have hh : (s * spectralCoordinate hH j x + t * spectralCoordinate hH j y)^2 ≤
        s * spectralCoordinate hH j x ^ 2 + t * spectralCoordinate hH j y ^ 2 := by
      nlinarith [mul_nonneg (mul_nonneg hs ht)
        (sq_nonneg (spectralCoordinate hH j x - spectralCoordinate hH j y))]
    have hm := mul_le_mul_of_nonneg_left hh (heig j)
    nlinarith
  have hsum := Finset.sum_le_sum (fun j (_ : j ∈ Finset.univ) => hterm j)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum] at hsum
  nlinarith [congrArg (fun z : ℝ => z * b) hst]

theorem negativeInertia_zero_convexOn {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (hz : negativeInertia hH = 0) (a : ι → ℝ) (b : ℝ)
    (D : Set (ι → ℝ)) (hD : Convex ℝ D) :
    ConvexOn ℝ D (fun x => dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b) :=
  spectral_quadratic_convexOn hH (eigenvalues_nonneg_of_negativeInertia_zero hH hz) a b D hD

theorem negativeInertia_zero_exact_epigraph {n : ℕ}
    {H : Matrix (Fin n) (Fin n) ℝ} (hH : H.IsHermitian)
    (hz : negativeInertia hH = 0) (a : Fin n → ℝ) (b : ℝ)
    (D : Set (Input n)) (hD : Convex ℝ D) :
    HasEpigraphLift D (quadraticPolynomial H a b) 0 0 := by
  apply convexOn_has_exact_epigraph
  change ConvexOn ℝ D (fun x => dotProduct x (H *ᵥ x) / 2 + dotProduct a x + b)
  simpa only [dotProduct_comm] using
    negativeInertia_zero_convexOn hH hz a b D hD

/-- The spectral criterion implies concavity of the actual polynomial on every
convex domain. Affine terms are arbitrary. -/
theorem spectral_quadratic_concaveOn {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (heig : ∀ j, hH.eigenvalues j ≤ 0) (a : ι → ℝ) (b : ℝ)
    (D : Set (ι → ℝ)) (hD : Convex ℝ D) :
    ConcaveOn ℝ D (fun x => dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b) := by
  refine ⟨hD, ?_⟩
  intro x hx y hy s t hs ht hst
  simp only [spectral_quadratic hH, spectralCoordinate_mix,
    add_dotProduct, smul_dotProduct, smul_eq_mul]
  have hterm : ∀ j,
      hH.eigenvalues j * (s * spectralCoordinate hH j x + t * spectralCoordinate hH j y)^2 ≥
      s * (hH.eigenvalues j * spectralCoordinate hH j x ^ 2) +
      t * (hH.eigenvalues j * spectralCoordinate hH j y ^ 2) := by
    intro j
    have hh : (s * spectralCoordinate hH j x + t * spectralCoordinate hH j y)^2 ≤
        s * spectralCoordinate hH j x ^ 2 + t * spectralCoordinate hH j y ^ 2 := by
      nlinarith [mul_nonneg (mul_nonneg hs ht)
        (sq_nonneg (spectralCoordinate hH j x - spectralCoordinate hH j y))]
    have hm := mul_le_mul_of_nonpos_left hh (heig j)
    nlinarith
  have hsum := Finset.sum_le_sum (fun j (_ : j ∈ Finset.univ) => hterm j)
  simp only [Finset.sum_add_distrib, ← Finset.mul_sum] at hsum
  nlinarith [congrArg (fun z : ℝ => z * b) hst]

theorem positiveInertia_zero_concaveOn {H : Matrix ι ι ℝ} (hH : H.IsHermitian)
    (hz : positiveInertia hH = 0) (a : ι → ℝ) (b : ℝ)
    (D : Set (ι → ℝ)) (hD : Convex ℝ D) :
    ConcaveOn ℝ D (fun x => dotProduct x (H *ᵥ x) / 2 + dotProduct x a + b) := by
  apply spectral_quadratic_concaveOn hH _ a b D hD
  have hn : IsEmpty {j // 0 < hH.eigenvalues j} := Fintype.card_eq_zero_iff.mp hz
  intro j
  by_contra h
  exact hn.false ⟨j, lt_of_not_ge h⟩

theorem positiveInertia_zero_exact_hypograph {n : ℕ}
    {H : Matrix (Fin n) (Fin n) ℝ} (hH : H.IsHermitian)
    (hz : positiveInertia hH = 0) (a : Fin n → ℝ) (b : ℝ)
    (D : Set (Input n)) (hD : Convex ℝ D) :
    HasHypographLift D (quadraticPolynomial H a b) 0 0 := by
  apply concaveOn_has_exact_hypograph
  change ConcaveOn ℝ D (fun x => dotProduct x (H *ᵥ x) / 2 + dotProduct a x + b)
  simpa only [dotProduct_comm] using
    positiveInertia_zero_concaveOn hH hz a b D hD

end QuadraticPrecision
