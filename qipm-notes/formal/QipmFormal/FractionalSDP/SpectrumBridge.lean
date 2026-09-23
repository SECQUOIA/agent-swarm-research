import QipmFormal.FractionalSDP.Spectrum
import QipmFormal.FractionalSDP.Hessian

/-! The spectral matrix represents the actual second derivative in the external
Frobenius metric on the complete equality tangent space. -/
namespace QipmFormal.FractionalSDP
noncomputable section

abbrev TangentCoords := (Fin 2 ⊕ Fin 2) → ℝ

def coordinateTangent (v : TangentCoords) : Matrix (Fin 3) (Fin 3) ℝ :=
  tangent (v (.inl 0)) (v (.inl 1)) (v (.inr 0)) (v (.inr 1))

def frobeniusPair (U V : Matrix (Fin 3) (Fin 3) ℝ) : ℝ :=
  ∑ i, ∑ j, U i j * V i j

theorem coordinateTangent_injective : Function.Injective coordinateTangent := by
  intro x y h
  have h01 := congrFun (congrFun h 0) 1
  have h11 := congrFun (congrFun h 1) 1
  have h02 := congrFun (congrFun h 0) 2
  have h12 := congrFun (congrFun h 1) 2
  funext i
  rcases i with i | i <;> fin_cases i
  · exact h01
  · exact h11
  · exact h02
  · exact h12

theorem coordinateTangent_range (U : Matrix (Fin 3) (Fin 3) ℝ) :
    U.IsSymm ∧ U.trace = 0 ∧ U 2 2 = U 0 1 ↔
      ∃ v : TangentCoords, U = coordinateTangent v := by
  rw [tangent_characterization]
  constructor
  · rintro ⟨u,v,w,z,rfl⟩
    exact ⟨Sum.elim ![u,v] ![w,z], rfl⟩
  · rintro ⟨v,rfl⟩
    exact ⟨v (.inl 0),v (.inl 1),v (.inr 0),v (.inr 1),rfl⟩

theorem frobeniusPair_operator (t : ℝ) (v : TangentCoords) :
    frobeniusPair (coordinateTangent v)
      (coordinateTangent ((reducedOperator t).mulVec v)) =
      k00 t*(v (.inl 0))^2 + 2*k01 t*v (.inl 0)*v (.inl 1) +
      k11 t*(v (.inl 1))^2 + 2/(b t*q t)*
        (g t*(v (.inr 0))^2 - 2*b t*v (.inr 0)*v (.inr 1) + a t*(v (.inr 1))^2) := by
  simp [frobeniusPair, coordinateTangent, tangent, reducedOperator,
    diagOperator, offOperator, Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
    Fintype.sum_sum_type]
  ring

/-- This identifies the computed operator with the barrier Hessian, using its
actual directional second derivative and the specified Frobenius metric. -/
theorem reducedOperator_second_derivative (t : ℝ) (v : TangentCoords)
    (hb : b t ≠ 0) (hq : q t ≠ 0) :
    HasDerivAt
      (deriv (fun s : ℝ => -Real.log ((centerMatrix t+s • coordinateTangent v).det)))
      (frobeniusPair (coordinateTangent v)
        (coordinateTangent ((reducedOperator t).mulVec v))) 0 := by
  rw [frobeniusPair_operator]
  exact center_logdet_second t _ _ _ _ hb hq

theorem reducedOperator_symmetric (t : ℝ) (u v : TangentCoords) :
    frobeniusPair (coordinateTangent u)
      (coordinateTangent ((reducedOperator t).mulVec v)) =
    frobeniusPair (coordinateTangent v)
      (coordinateTangent ((reducedOperator t).mulVec u)) := by
  simp [frobeniusPair, coordinateTangent, tangent, reducedOperator,
    diagOperator, offOperator, Matrix.mulVec, dotProduct, Fin.sum_univ_succ,
    Fintype.sum_sum_type]
  ring

@[simp] theorem coordinateTangent_zero : coordinateTangent 0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [coordinateTangent, tangent]

theorem coordinateTangent_smul (r : ℝ) (v : TangentCoords) :
    coordinateTangent (r • v) = r • coordinateTangent v := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [coordinateTangent, tangent]
  ring

/-- Each spectral value is realized by a nonzero feasible tangent matrix;
there are no other tangent eigenvalues. -/
theorem tangent_eigenvalue_iff (t r : ℝ) (hb : 0 < b t) (hq : 0 < q t)
    (ha : 0 < a t + g t) :
    (∃ v : TangentCoords, coordinateTangent v ≠ 0 ∧
      coordinateTangent ((reducedOperator t).mulVec v) = r • coordinateTangent v) ↔
      r = diagLow t ∨ r = diagHigh t ∨ r = offLow t ∨ r = offHigh t := by
  rw [← mem_reduced_spectrum_iff t r hb hq ha, ← Matrix.spectrum_toLin',
    ← Module.End.hasEigenvalue_iff_mem_spectrum]
  constructor
  · rintro ⟨v,hv,he⟩
    apply Module.End.hasEigenvalue_of_hasEigenvector (x := v)
    refine ⟨Module.End.mem_eigenspace_iff.mpr ?_, ?_⟩
    · exact coordinateTangent_injective (he.trans (coordinateTangent_smul r v).symm)
    · intro hz
      apply hv
      simp [hz]
  · intro hr
    obtain ⟨v,hv⟩ := hr.exists_hasEigenvector
    refine ⟨v, ?_, ?_⟩
    · intro hz
      exact hv.2 (coordinateTangent_injective (hz.trans coordinateTangent_zero.symm))
    · rw [show (reducedOperator t).mulVec v = r • v from hv.apply_eq_smul,
        coordinateTangent_smul]


def restrictedCoordinateTangent (v : Fin 2 → ℝ) : Matrix (Fin 3) (Fin 3) ℝ :=
  tangent (v 0) (v 1) 0 0

theorem restrictedCoordinateTangent_injective : Function.Injective restrictedCoordinateTangent := by
  intro x y h
  funext i
  fin_cases i
  · exact congrFun (congrFun h 0) 1
  · exact congrFun (congrFun h 1) 1

theorem restrictedCoordinateTangent_range (U : Matrix (Fin 3) (Fin 3) ℝ) :
    U.IsSymm ∧ U.trace = 0 ∧ U 2 2 = U 0 1 ∧ U 0 2 = 0 ∧ U 1 2 = 0 ↔
      ∃ v : Fin 2 → ℝ, U = restrictedCoordinateTangent v := by
  rw [restricted_tangent_characterization]
  constructor
  · rintro ⟨u,v,rfl⟩
    exact ⟨![u,v],rfl⟩
  · rintro ⟨v,rfl⟩
    exact ⟨v 0,v 1,rfl⟩

theorem frobeniusPair_restricted_operator (t : ℝ) (v : Fin 2 → ℝ) :
    frobeniusPair (restrictedCoordinateTangent v)
      (restrictedCoordinateTangent ((diagOperator t).mulVec v)) =
      k00 t*(v 0)^2 + 2*k01 t*v 0*v 1 + k11 t*(v 1)^2 := by
  simp [frobeniusPair, restrictedCoordinateTangent, tangent,
    diagOperator, Matrix.mulVec, dotProduct, Fin.sum_univ_succ]
  ring

theorem restrictedOperator_second_derivative (t : ℝ) (v : Fin 2 → ℝ)
    (hb : b t ≠ 0) (hq : q t ≠ 0) :
    HasDerivAt
      (deriv (fun s : ℝ => -Real.log ((centerMatrix t+s • restrictedCoordinateTangent v).det)))
      (frobeniusPair (restrictedCoordinateTangent v)
        (restrictedCoordinateTangent ((diagOperator t).mulVec v))) 0 := by
  rw [frobeniusPair_restricted_operator]
  simpa [restrictedCoordinateTangent] using center_logdet_second t (v 0) (v 1) 0 0 hb hq

@[simp] theorem restrictedCoordinateTangent_zero : restrictedCoordinateTangent 0 = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [restrictedCoordinateTangent, tangent]

theorem restrictedCoordinateTangent_smul (r : ℝ) (v : Fin 2 → ℝ) :
    restrictedCoordinateTangent (r • v) = r • restrictedCoordinateTangent v := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [restrictedCoordinateTangent, tangent]
  ring

theorem restricted_tangent_eigenvalue_iff (t r : ℝ) (hq : 0 < q t) :
    (∃ v : Fin 2 → ℝ, restrictedCoordinateTangent v ≠ 0 ∧
      restrictedCoordinateTangent ((diagOperator t).mulVec v) =
        r • restrictedCoordinateTangent v) ↔ r = diagLow t ∨ r = diagHigh t := by
  rw [← mem_diag_spectrum_iff t r hq, ← Matrix.spectrum_toLin',
    ← Module.End.hasEigenvalue_iff_mem_spectrum]
  constructor
  · rintro ⟨v,hv,he⟩
    apply Module.End.hasEigenvalue_of_hasEigenvector (x := v)
    refine ⟨Module.End.mem_eigenspace_iff.mpr ?_, ?_⟩
    · exact restrictedCoordinateTangent_injective
        (he.trans (restrictedCoordinateTangent_smul r v).symm)
    · intro hz
      apply hv
      simp [hz]
  · intro hr
    obtain ⟨v,hv⟩ := hr.exists_hasEigenvector
    refine ⟨v, ?_, ?_⟩
    · intro hz
      exact hv.2 (restrictedCoordinateTangent_injective
        (hz.trans restrictedCoordinateTangent_zero.symm))
    · rw [show (diagOperator t).mulVec v = r • v from hv.apply_eq_smul,
        restrictedCoordinateTangent_smul]

open scoped Matrix.Norms.Frobenius

theorem reducedOperator_iteratedFDeriv (t : ℝ) (v : TangentCoords)
    (hb : b t ≠ 0) (hq : q t ≠ 0) :
    iteratedFDeriv ℝ 2 (fun Y : Matrix (Fin 3) (Fin 3) ℝ => -Real.log Y.det)
      (centerMatrix t) (fun _ => coordinateTangent v) =
      frobeniusPair (coordinateTangent v)
        (coordinateTangent ((reducedOperator t).mulVec v)) := by
  rw [frobeniusPair_operator]
  exact center_iteratedFDeriv_two t _ _ _ _ hb hq

theorem restrictedOperator_iteratedFDeriv (t : ℝ) (v : Fin 2 → ℝ)
    (hb : b t ≠ 0) (hq : q t ≠ 0) :
    iteratedFDeriv ℝ 2 (fun Y : Matrix (Fin 3) (Fin 3) ℝ => -Real.log Y.det)
      (centerMatrix t) (fun _ => restrictedCoordinateTangent v) =
      frobeniusPair (restrictedCoordinateTangent v)
        (restrictedCoordinateTangent ((diagOperator t).mulVec v)) := by
  rw [frobeniusPair_restricted_operator]
  simpa [restrictedCoordinateTangent] using
    center_iteratedFDeriv_two t (v 0) (v 1) 0 0 hb hq

end
end QipmFormal.FractionalSDP
