import QipmFormal.Preconditioner.Spectral
import QipmFormal.Preconditioner.Congruence

/-! Reciprocal generalized Rayleigh witnesses give a squared condition lower bound. -/
namespace QipmFormal.Preconditioner
noncomputable section
open Matrix
variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

/-- Two reciprocal generalized Rayleigh ratios certify the actual relative spectral
condition number, using the positive inverse square root of the first form. -/
theorem generalized_condition_ge_sq {A B : Matrix n n ℝ}
    (hA : A.PosDef) (hB : B.PosDef)
    {x y : n → ℝ} (hx : x ≠ 0) (hy : y ≠ 0) {t : ℝ} (ht : 0 ≤ t)
    (hxy : t * energy A x ≤ energy B x)
    (hyx : t * energy B y ≤ energy A y) :
    t ^ 2 ≤ spectralCondition (inverseSqrt A * B * inverseSqrt A)
      (inverseSqrt_congruence_posDef hB hA).1 := by
  let P := inverseSqrt A
  let zx := P⁻¹ *ᵥ x
  let zy := P⁻¹ *ᵥ y
  have hP : P * P⁻¹ = 1 :=
    mul_nonsing_inv P ((isUnit_iff_isUnit_det P).mp (inverseSqrt_isUnit hA))
  have hpx : P *ᵥ zx = x := by dsimp [zx]; rw [mulVec_mulVec, hP, one_mulVec]
  have hpy : P *ᵥ zy = y := by dsimp [zy]; rw [mulVec_mulVec, hP, one_mulVec]
  have henergy (D : Matrix n n ℝ) (v : n → ℝ) :
      energy (P * D * P) v = energy D (P *ᵥ v) := by
    simpa only [P, inverseSqrt_symmetric] using energy_congruence D P v
  have hsx : euclideanSq zx = energy A x := by
    have h := henergy A zx
    rw [hpx] at h
    simpa only [P, inverseSqrt_whitens hA, energy, one_mulVec, euclideanSq] using h
  have hsy : euclideanSq zy = energy A y := by
    have h := henergy A zy
    rw [hpy] at h
    simpa only [P, inverseSqrt_whitens hA, energy, one_mulVec, euclideanSq] using h
  have hcomp := energy_comparison (inverseSqrt_congruence_posDef hB hA) zx zy
  change energy (P * B * P) zx * euclideanSq zy ≤
    spectralCondition (P * B * P) _ * (energy (P * B * P) zy * euclideanSq zx) at hcomp
  rw [henergy, henergy, hpx, hpy, hsx, hsy] at hcomp
  have hlo := mul_le_mul hxy hyx
    (mul_nonneg ht (energy_pos hB hy).le) (energy_pos hB hx).le
  have he : 0 < energy A x * energy B y := mul_pos (energy_pos hA hx) (energy_pos hB hy)
  apply (mul_le_mul_iff_left₀ he).mp
  nlinarith [hlo, hcomp]

end
end QipmFormal.Preconditioner
