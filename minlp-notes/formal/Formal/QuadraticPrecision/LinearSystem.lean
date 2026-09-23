import Mathlib

/-! Finite real affine row systems. Row counts refer to the actual finite
family of inequalities; equalities can be represented by paired rows. -/
namespace QuadraticPrecision
noncomputable section
variable {V W : Type*} [AddCommGroup V] [Module ℝ V]
  [AddCommGroup W] [Module ℝ W]

/-- A concrete finite linear extended formulation with real coefficients. -/
structure LinearSystem (V : Type*) [AddCommGroup V] [Module ℝ V] where
  rowCount : ℕ
  row : Fin rowCount → V →ᵃ[ℝ] ℝ

def LinearSystem.feasible (S : LinearSystem V) : Set V :=
  {x | ∀ i, S.row i x ≤ 0}

theorem LinearSystem.convex (S : LinearSystem V) : Convex ℝ S.feasible := by
  have he : S.feasible = ⋂ i, (S.row i) ⁻¹' Set.Iic 0 := by ext; simp [feasible]
  rw [he]
  exact convex_iInter fun i => (convex_Iic (0 : ℝ)).affine_preimage (S.row i)

/-- Affine substitution preserves linearity and introduces no inequality rows. -/
def LinearSystem.preimage (S : LinearSystem W) (f : V →ᵃ[ℝ] W) : LinearSystem V where
  rowCount := S.rowCount
  row i := (S.row i).comp f

@[simp] theorem LinearSystem.feasible_preimage (S : LinearSystem W) (f : V →ᵃ[ℝ] W) :
    (S.preimage f).feasible = f ⁻¹' S.feasible := rfl

/-- Combining two finite systems adds their exact row counts. -/
def LinearSystem.append (S T : LinearSystem V) : LinearSystem V where
  rowCount := S.rowCount + T.rowCount
  row := Fin.addCases S.row T.row

@[simp] theorem LinearSystem.feasible_append (S T : LinearSystem V) :
    (S.append T).feasible = S.feasible ∩ T.feasible := by
  ext x
  simp [feasible, append, Fin.forall_fin_add]

def IsFinitePolyhedron (C : Set V) : Prop := ∃ S : LinearSystem V, C = S.feasible

theorem IsFinitePolyhedron.convex {C : Set V} (h : IsFinitePolyhedron C) : Convex ℝ C := by
  obtain ⟨S, rfl⟩ := h
  exact S.convex

end
end QuadraticPrecision
