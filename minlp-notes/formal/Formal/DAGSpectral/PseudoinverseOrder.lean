import Formal.DAGSpectral.Pseudoinverse

namespace DAGSpectral
open Matrix
noncomputable section
variable {n : ℕ} {A B : RealMatrix n}

/-- The Moore–Penrose inverse vanishes on the information kernel. -/
theorem pseudoInverse_mulVec_zero (hA : A.IsHermitian) {x : Fin n → ℝ}
    (hx : A *ᵥ x = 0) : DAGSpectral.pseudoInverse A hA *ᵥ x = 0 := by
  have he : DAGSpectral.pseudoInverse A hA =
      DAGSpectral.pseudoInverse A hA * DAGSpectral.pseudoInverse A hA * A := by
    calc
      _ = DAGSpectral.pseudoInverse A hA * A * DAGSpectral.pseudoInverse A hA :=
        (pseudoInverse_mul_mul_self hA).symm
      _ = _ := by rw [Matrix.mul_assoc, pseudoInverse_commute hA, ← Matrix.mul_assoc]
  rw [he, ← Matrix.mulVec_mulVec, hx, Matrix.mulVec_zero]

/-- The orthogonal range projection leaves every pseudoinverse quadratic
value unchanged; only the kernel condition on the removed vector is needed. -/
theorem contrastVariance_eq_of_kernel_difference (hA : A.IsHermitian)
    {x y : Fin n → ℝ} (hxy : A *ᵥ (x - y) = 0) :
    DAGSpectral.contrastVariance A hA x = DAGSpectral.contrastVariance A hA y := by
  have hg := pseudoInverse_mulVec_zero hA hxy
  have he : DAGSpectral.pseudoInverse A hA *ᵥ x = DAGSpectral.pseudoInverse A hA *ᵥ y := by
    simpa only [Matrix.mulVec_sub, sub_eq_zero] using hg
  have hh : (x-y) ⬝ᵥ (DAGSpectral.pseudoInverse A hA *ᵥ y) = 0 := by
    rw [symmetric_dot (pseudoInverse_isHermitian hA), hg, zero_dotProduct]
  unfold contrastVariance
  rw [he]
  simpa only [sub_dotProduct, sub_eq_zero] using hh

/-- The two-sided Moore–Penrose matrix inequality holds on the entire ambient
space because both inverses vanish on the common kernel. -/
theorem RelativeSandwich.pseudoInverse {η : ℝ} (h : RelativeSandwich η A B)
    (hA : A.PosSemidef) (hB : B.PosSemidef) (hη0 : 0 ≤ η) (hη1 : η < 1) :
    Loewner ((1+η)⁻¹ • DAGSpectral.pseudoInverse A hA.isHermitian)
      (DAGSpectral.pseudoInverse B hB.isHermitian) ∧
    Loewner (DAGSpectral.pseudoInverse B hB.isHermitian)
      ((1-η)⁻¹ • DAGSpectral.pseudoInverse A hA.isHermitian) := by
  have hquad (x : Fin n → ℝ) :
      (1+η)⁻¹ * DAGSpectral.contrastVariance A hA.isHermitian x ≤
        DAGSpectral.contrastVariance B hB.isHermitian x ∧
      DAGSpectral.contrastVariance B hB.isHermitian x ≤
        (1-η)⁻¹ * DAGSpectral.contrastVariance A hA.isHermitian x := by
    let y := A *ᵥ (DAGSpectral.pseudoInverse A hA.isHermitian *ᵥ x)
    have hy : Estimable A y := ⟨_,rfl⟩
    have hkerA : A *ᵥ (x - y) = 0 := by
      dsimp [y]
      rw [Matrix.mulVec_sub, Matrix.mulVec_mulVec, Matrix.mulVec_mulVec,
        Matrix.mul_assoc, pseudoInverse_commute hA.isHermitian, ← Matrix.mul_assoc,
        pseudoInverse_mul_self_mul, sub_self]
    have hkerB := (h.kernel_iff hA hB hη1 (x-y)).mp hkerA
    rw [contrastVariance_eq_of_kernel_difference hA.isHermitian hkerA,
      contrastVariance_eq_of_kernel_difference hB.isHermitian hkerB]
    exact h.contrastVariance hA hB hη0 hη1 hy
  constructor
  · apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
      ((pseudoInverse_isHermitian hB.isHermitian).sub
        ((pseudoInverse_isHermitian hA.isHermitian).smul (IsSelfAdjoint.all _)))
    intro x
    simpa only [star_trivial, Matrix.sub_mulVec, dotProduct_sub, Matrix.smul_mulVec,
      dotProduct_smul, smul_eq_mul, sub_nonneg, DAGSpectral.contrastVariance] using (hquad x).1
  · apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
      (((pseudoInverse_isHermitian hA.isHermitian).smul (IsSelfAdjoint.all _)).sub
        (pseudoInverse_isHermitian hB.isHermitian))
    intro x
    simpa only [star_trivial, Matrix.sub_mulVec, dotProduct_sub, Matrix.smul_mulVec,
      dotProduct_smul, smul_eq_mul, sub_nonneg, DAGSpectral.contrastVariance] using (hquad x).2

end
end DAGSpectral
