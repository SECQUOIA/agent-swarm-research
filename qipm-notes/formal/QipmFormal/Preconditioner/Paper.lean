import QipmFormal.Preconditioner.Spectral
import QipmFormal.Preconditioner.Congruence
import QipmFormal.Preconditioner.PathBounds
import QipmFormal.Preconditioner.Sign
import QipmFormal.Preconditioner.Simultaneous
import QipmFormal.Preconditioner.WitnessRatio

/-! The fixed-preconditioner minimax theorem, in the manuscript's actual matrices. -/
namespace QipmFormal.Preconditioner
noncomputable section
open Matrix
open scoped BigOperators

variable {n : Type*} [Fintype n] [DecidableEq n] [Nonempty n]

/-- The Euclidean spectral condition after applying a congruence factor. -/
def congruenceCondition (A : Matrix n n ℝ) (hA : A.IsHermitian)
    (P : Matrix n n ℝ) : ℝ :=
  spectralCondition (Pᵀ * A * P) (by
    simpa only [conjTranspose_eq_transpose_of_trivial] using
      isHermitian_conjTranspose_mul_mul P hA)

def signedPathMatrix (m : ℕ) : Matrix (Fin m) (Fin m) ℝ :=
  alternatingMatrix m * pathMatrix m * alternatingMatrix m

theorem alternatingMatrix_isUnit (m : ℕ) : IsUnit (alternatingMatrix m) :=
  ⟨⟨alternatingMatrix m, alternatingMatrix m,
    alternatingMatrix_sq m, alternatingMatrix_sq m⟩, rfl⟩

theorem signedPathMatrix_posDef (m : ℕ) : (signedPathMatrix m).PosDef := by
  have h := (pathMatrix_posDef m).conjTranspose_mul_mul_same
    (mulVec_injective_iff_isUnit.mpr (alternatingMatrix_isUnit m))
  simpa only [conjTranspose_eq_transpose_of_trivial, alternatingMatrix_transpose,
    signedPathMatrix] using h

variable {m : ℕ} [NeZero m]

omit [NeZero m] in
theorem path_energy_eq (x : Fin m → ℝ) : energy (pathMatrix m) x = pathEnergy x :=
  pathMatrix_quadratic x

omit [NeZero m] in
theorem signedPath_energy_eq (x : Fin m → ℝ) :
    energy (signedPathMatrix m) x = pathEnergy (alternatingMatrix m *ᵥ x) := by
  have h := energy_congruence (pathMatrix m) (alternatingMatrix m) x
  simpa only [alternatingMatrix_transpose, signedPathMatrix, path_energy_eq] using h

omit [NeZero m] in
theorem alternating_twice (x : Fin m → ℝ) :
    alternatingMatrix m *ᵥ (alternatingMatrix m *ᵥ x) = x := by
  rw [mulVec_mulVec, alternatingMatrix_sq, one_mulVec]

theorem alternating_pathRamp_ne_zero : alternatingMatrix m *ᵥ pathRamp m ≠ 0 := by
  intro hz
  have h := alternating_twice (pathRamp m)
  rw [hz, mulVec_zero] at h
  exact pathRamp_ne_zero (Nat.pos_of_ne_zero (NeZero.ne m)) h.symm

/-- Exact ramp ratio; the paper's former constant used only a partial sum. -/
def rampRatio (m : ℕ) : ℝ := (4 * (m : ℝ)^2 - 1) / 3

theorem rampRatio_ge_sq : (m : ℝ)^2 ≤ rampRatio m := by
  have hm : (1 : ℝ) ≤ m := by exact_mod_cast Nat.one_le_iff_ne_zero.mpr (NeZero.ne m)
  unfold rampRatio
  nlinarith

/-- The stronger minimax lower bound covers every invertible factor, including dense factors. -/
theorem path_congruence_minimax (P : Matrix (Fin m) (Fin m) ℝ) (hP : IsUnit P) :
    rampRatio m ≤ max
      (congruenceCondition (pathMatrix m) (pathMatrix_posDef m).1 P)
      (congruenceCondition (signedPathMatrix m) (signedPathMatrix_posDef m).1 P) := by
  apply congruence_paired_minimax (pathMatrix_posDef m) (signedPathMatrix_posDef m)
    hP (pathRamp_ne_zero (Nat.pos_of_ne_zero (NeZero.ne m))) alternating_pathRamp_ne_zero
    (le_trans (sq_nonneg _) rampRatio_ge_sq)
  · rw [path_energy_eq, pathRamp_energy, signedPath_energy_eq, alternating_pathRamp_energy]
    unfold rampRatio
    nlinarith
  · rw [signedPath_energy_eq, alternating_twice, pathRamp_energy,
      path_energy_eq, alternating_pathRamp_energy]
    unfold rampRatio
    nlinarith

/-- The manuscript's SPD-preconditioner statement, with the actual positive inverse square root. -/
theorem path_spd_minimax (M : Matrix (Fin m) (Fin m) ℝ) (hM : M.PosDef) :
    rampRatio m ≤ max
      (spectralCondition (inverseSqrt M * pathMatrix m * inverseSqrt M)
        (inverseSqrt_congruence_posDef (pathMatrix_posDef m) hM).1)
      (spectralCondition (inverseSqrt M * signedPathMatrix m * inverseSqrt M)
        (inverseSqrt_congruence_posDef (signedPathMatrix_posDef m) hM).1) := by
  simpa only [congruenceCondition, inverseSqrt_symmetric] using
    path_congruence_minimax (inverseSqrt M) (inverseSqrt_isUnit hM)

/-- The previously stated constant follows without its former dimension-four restriction. -/
theorem path_spd_original_bound (M : Matrix (Fin m) (Fin m) ℝ) (hM : M.PosDef) :
    (m : ℝ)^2 / 4 ≤ max
      (spectralCondition (inverseSqrt M * pathMatrix m * inverseSqrt M)
        (inverseSqrt_congruence_posDef (pathMatrix_posDef m) hM).1)
      (spectralCondition (inverseSqrt M * signedPathMatrix m * inverseSqrt M)
        (inverseSqrt_congruence_posDef (signedPathMatrix_posDef m) hM).1) := by
  have h := rampRatio_ge_sq (m := m)
  have hl : (m : ℝ)^2 / 4 ≤ rampRatio m := by nlinarith [sq_nonneg (m : ℝ)]
  exact hl.trans (path_spd_minimax M hM)

/-- The squared relative-condition obstruction used in the manuscript proof. -/
theorem path_relative_condition_lower :
    rampRatio m ^ 2 ≤ spectralCondition
      (inverseSqrt (pathMatrix m) * signedPathMatrix m * inverseSqrt (pathMatrix m))
      (inverseSqrt_congruence_posDef (signedPathMatrix_posDef m) (pathMatrix_posDef m)).1 := by
  apply generalized_condition_ge_sq (pathMatrix_posDef m) (signedPathMatrix_posDef m)
    (pathRamp_ne_zero (Nat.pos_of_ne_zero (NeZero.ne m))) alternating_pathRamp_ne_zero
    (le_trans (sq_nonneg _) rampRatio_ge_sq)
  · rw [path_energy_eq, pathRamp_energy, signedPath_energy_eq, alternating_pathRamp_energy]
    unfold rampRatio
    nlinarith
  · rw [signedPath_energy_eq, alternating_twice, pathRamp_energy,
      path_energy_eq, alternating_pathRamp_energy]
    unfold rampRatio
    nlinarith

theorem signedPath_condition_eq :
    spectralCondition (signedPathMatrix m) (signedPathMatrix_posDef m).1 =
      spectralCondition (pathMatrix m) (pathMatrix_posDef m).1 := by
  have h := spectralCondition_orthogonal_congruence (pathMatrix_posDef m)
    (alternatingMatrix_isUnit m) (alternatingMatrix_orthogonal m)
    (by rw [alternatingMatrix_transpose, alternatingMatrix_sq])
  simpa only [alternatingMatrix_transpose, signedPathMatrix] using h

/-- The identity preconditioner has the matching quadratic upper bound. -/
theorem path_condition_upper :
    spectralCondition (pathMatrix m) (pathMatrix_posDef m).1 ≤ 4 * (m : ℝ)^2 := by
  have hm : 0 < (m : ℝ)^2 := sq_pos_of_pos (by exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne m))
  have h := spectralCondition_le_of_bounds (pathMatrix_posDef m)
    (l := 1 / (m : ℝ)^2) (u := 4) (by positivity) (by
      intro x
      rw [path_energy_eq]
      have hlo := path_norm_le x
      have hhi := path_energy_le x
      have hn : euclideanSq x = ∑ i, x i ^ 2 := by simp [euclideanSq, dotProduct, pow_two]
      rw [hn]
      constructor
      · rw [one_div_mul_eq_div]
        apply (div_le_iff₀ hm).mpr
        simpa only [mul_comm] using hlo
      · exact hhi)
  simpa using h

/-- Explicit two-sided bounds establish Θ(m²), with no asymptotic premise. -/
theorem path_condition_bounds :
    rampRatio m ≤ spectralCondition (pathMatrix m) (pathMatrix_posDef m).1 ∧
      spectralCondition (pathMatrix m) (pathMatrix_posDef m).1 ≤ 4 * (m : ℝ)^2 := by
  refine ⟨?_, path_condition_upper⟩
  have h := path_congruence_minimax (1 : Matrix (Fin m) (Fin m) ℝ) isUnit_one
  simpa only [congruenceCondition, transpose_one, one_mul, mul_one,
    signedPath_condition_eq, max_self] using h

def edgePathMatrix (e : Fin m → ℝ) : Matrix (Fin m) (Fin m) ℝ :=
  signedPathIncidence e * (signedPathIncidence e)ᵀ

omit [NeZero m] in
theorem edgePathMatrix_posDef {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1) :
    (edgePathMatrix e).PosDef := by
  let S := signMatrix (pathVertexSigns e)
  have hS : S * S = 1 := signMatrix_sq (pathVertexSigns_sq he)
  have hu : IsUnit S := ⟨⟨S, S, hS, hS⟩, rfl⟩
  have h := congruence_posDef (pathMatrix_posDef m) hu
  simpa only [S, signMatrix_transpose, signedPathMatrix_switching he, edgePathMatrix] using h

/-- Every legal edge signing has the same spectrum condition as the unsigned path. -/
theorem edgePath_condition_eq {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1) :
    spectralCondition (edgePathMatrix e) (edgePathMatrix_posDef he).1 =
      spectralCondition (pathMatrix m) (pathMatrix_posDef m).1 := by
  let S := signMatrix (pathVertexSigns e)
  have hS : S * S = 1 := signMatrix_sq (pathVertexSigns_sq he)
  have hu : IsUnit S := ⟨⟨S, S, hS, hS⟩, rfl⟩
  have h := spectralCondition_orthogonal_congruence (pathMatrix_posDef m) hu
    (by simpa only [S, signMatrix_transpose] using hS)
    (by simpa only [S, signMatrix_transpose] using hS)
  simpa only [S, signMatrix_transpose, signedPathMatrix_switching he, edgePathMatrix] using h

/-- The identity upper bound is uniform over the entire signed-path family. -/
theorem all_signed_paths_identity_bound {e : Fin m → ℝ} (he : ∀ i, e i ^ 2 = 1) :
    spectralCondition (edgePathMatrix e) (edgePathMatrix_posDef he).1 ≤ 4 * (m : ℝ)^2 := by
  rw [edgePath_condition_eq he]
  exact path_condition_upper

end
end QipmFormal.Preconditioner
