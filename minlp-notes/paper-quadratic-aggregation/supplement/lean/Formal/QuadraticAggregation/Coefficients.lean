import Formal.QuadraticAggregation.Model
import Formal.QuadraticAggregation.ConeClosed

/-! The actual cone of quadratic and linear aggregate coefficients. -/

namespace QuadraticAggregation
open scoped BigOperators Matrix Matrix.Norms.Elementwise

abbrev Coeff (n : ℕ) := Mat n × Vec n

variable {n m : ℕ}

/-- Quadratic evaluation is linear in the coefficients. -/
noncomputable def coefficientQuadratic (x : Vec n) : Coeff n →L[ℝ] ℝ :=
  LinearMap.toContinuousLinearMap
    { toFun := fun z => q z.1 x
      map_add' := by intros; simp [q, Matrix.add_mulVec, dotProduct_add]
      map_smul' := by intros; simp [q, Matrix.smul_mulVec, dotProduct_smul] }

/-- Linear evaluation is linear in the coefficients. -/
noncomputable def coefficientLinear (x : Vec n) : Coeff n →L[ℝ] ℝ :=
  LinearMap.toContinuousLinearMap
    { toFun := fun z => z.2 ⬝ᵥ x
      map_add' := by intros; simp [add_dotProduct]
      map_smul' := by intros; simp [smul_dotProduct] }

@[simp] theorem coefficientQuadratic_apply (x : Vec n) (z : Coeff n) :
    coefficientQuadratic x z = q z.1 x := rfl

@[simp] theorem coefficientLinear_apply (x : Vec n) (z : Coeff n) :
    coefficientLinear x z = z.2 ⬝ᵥ x := rfl

namespace System

def coefficientCone (D : System n m) : Set (Coeff n) :=
  {z | ∃ w : Vec m, (∀ i, 0 ≤ w i) ∧ (D.aggA w, D.aggB w) = z}

theorem isClosed_coefficientCone (D : System n m) : IsClosed D.coefficientCone := by
  have heq : D.coefficientCone =
      {z | ∃ w : Vec m, (∀ i, 0 ≤ w i) ∧ ∑ i, w i • (D.A i, D.b i) = z} := by
    have hsum (w : Vec m) : ∑ i, w i • (D.A i, D.b i) = (D.aggA w, D.aggB w) := by
      apply Prod.ext <;> simp [aggA, aggB, Prod.fst_sum, Prod.snd_sum]
    ext z
    simp only [coefficientCone, Set.mem_ofPred, hsum]
  rw [heq]
  exact isClosed_nonnegative_span (fun i => (D.A i, D.b i))

theorem coefficientCone_smul (D : System n m) (t : ℝ) (ht : 0 ≤ t)
    (z : Coeff n) (hz : z ∈ D.coefficientCone) : t • z ∈ D.coefficientCone := by
  obtain ⟨w, hw, rfl⟩ := hz
  refine ⟨t • w, fun i => mul_nonneg ht (hw i), ?_⟩
  ext <;> simp [aggA, aggB, Finset.smul_sum, smul_smul]

theorem coefficientCone_symmetric (D : System n m) {z : Coeff n}
    (hz : z ∈ D.coefficientCone) : z.1.IsSymm := by
  obtain ⟨w, _, rfl⟩ := hz
  exact D.aggA_isSymm w

theorem certificate_of_coefficientCone (D : System n m) {z : Coeff n}
    (hz : z ∈ D.coefficientCone) (hne : z ≠ 0) (hpsd : ∀ x, 0 ≤ q z.1 x) :
    ∃ w, D.Certificate w := by
  obtain ⟨w, hw, rfl⟩ := hz
  refine ⟨w, hw, ?_, ?_, ?_⟩
  · intro heq
    apply hne
    simp [heq]
  · exact Matrix.posSemidef_iff_dotProduct_mulVec.mpr
      ⟨(Matrix.isHermitian_iff_isSymm).mpr (D.aggA_isSymm w), by simpa [q] using hpsd⟩
  · by_contra! h
    exact hne (Prod.ext h.1 h.2)

end System
end QuadraticAggregation
