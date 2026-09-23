import Formal.DAGSpectral.RationalFactorization
import Formal.DAGSpectral.RatMatrix

/-! Rational LDL applies directly to input matrices certified PSD over the reals. -/
namespace DAGSpectral
open Matrix

/-- Restricting the quadratic-form test to rational vectors preserves PSD. -/
theorem rationalPSD_of_realPSD {n : ℕ} {A : Matrix (Fin n) (Fin n) ℚ}
    (hA : (ratMatrixReal A).PosSemidef) : A.PosSemidef := by
  apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
  · ext i j
    have he := congrArg (fun M => M i j) hA.isHermitian
    simp only [conjTranspose_apply, star_trivial,ratMatrixReal_apply] at he ⊢
    exact_mod_cast he
  · intro x
    have he := hA.dotProduct_mulVec_nonneg (fun i => (x i : ℝ))
    simp only [star_trivial,ratMatrixReal_mulVec,dotProduct] at he ⊢
    exact_mod_cast he

/-- Finite indexed form of the concrete output, for labelled factor enumeration. -/
theorem rationalLDL_fin_reconstruct {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : A.PosSemidef) (i j : Fin n) :
    A i j = ∑ k : Fin (rationalLDL n A).length,
      ((rationalLDL n A).get k).1 * ((rationalLDL n A).get k).2 i *
        ((rationalLDL n A).get k).2 j := by
  rw [rationalLDL_reconstruct A hA i j]
  unfold factorValue
  conv_lhs => rw [←List.ofFn_get (rationalLDL n A),List.map_ofFn,List.sum_ofFn]
  rfl

/-- Real reconstruction with the same rational weights and columns. -/
theorem rationalLDL_real_reconstruct {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) (i j : Fin n) :
    ratMatrixReal A i j = ∑ k : Fin (rationalLDL n A).length,
      (((rationalLDL n A).get k).1 : ℝ) * (((rationalLDL n A).get k).2 i : ℝ) *
        (((rationalLDL n A).get k).2 j : ℝ) := by
  rw [ratMatrixReal_apply]
  exact_mod_cast rationalLDL_fin_reconstruct A (rationalPSD_of_realPSD hA) i j

/-- The producer supplies, rather than assumes, a finite positive rational factorization. -/
theorem exists_rational_rankOne_factors {n : ℕ} (A : Matrix (Fin n) (Fin n) ℚ)
    (hA : (ratMatrixReal A).PosSemidef) :
    ∃ r ≤ n, ∃ w : Fin r → ℚ, ∃ v : Fin r → Fin n → ℚ,
      (∀ k, 0 < w k ∧ v k ≠ 0) ∧
      ∀ i j, A i j = ∑ k, w k * v k i * v k j := by
  refine ⟨(rationalLDL n A).length,rationalLDL_length_le n A,
    (fun k => ((rationalLDL n A).get k).1),
    (fun k => ((rationalLDL n A).get k).2), ?_, ?_⟩
  · intro k
    exact rationalLDL_factors A (rationalPSD_of_realPSD hA) _ (List.get_mem _ k)
  · exact rationalLDL_fin_reconstruct A (rationalPSD_of_realPSD hA)

end DAGSpectral
