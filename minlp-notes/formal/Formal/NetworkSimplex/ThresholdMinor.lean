import Mathlib

/-! Independent rows contain an invertible square coordinate minor. -/
namespace NetworkSimplex.Threshold

/-- Selecting a basis of columns produces a nonsingular square minor from every
linearly independent finite row family. This includes the empty minor. -/
theorem exists_nonsingular_coordinate_minor {K : Type*} [Field K] {s m : ℕ}
    (A : Matrix (Fin s) (Fin m) K) (hA : LinearIndependent K A.row) :
    ∃ e : Fin s ↪ Fin m, (A.submatrix id e).det ≠ 0 := by
  classical
  obtain ⟨κ, c, hc, hspan, hli⟩ := exists_linearIndependent' K A.col
  let : Finite κ := Finite.of_injective c hc
  let : Fintype κ := Fintype.ofFinite κ
  have hcard : Fintype.card κ = s := by
    calc
      Fintype.card κ = Module.finrank K (Submodule.span K (Set.range (A.col ∘ c))) :=
        (finrank_span_eq_card hli).symm
      _ = A.rank := by rw [hspan, Matrix.rank_eq_finrank_span_cols]
      _ = s := by simpa using hA.rank_matrix
  let e : Fin s ≃ κ := Fintype.equivOfCardEq (by simpa using hcard.symm)
  let emb : Fin s ↪ Fin m := ⟨c ∘ e, hc.comp e.injective⟩
  refine ⟨emb, Matrix.nonsingular_iff_det_ne_zero.mp ?_⟩
  apply Matrix.Nonsingular.of_linearIndependent_col
  exact hli.comp e e.injective

/-- The same independent row family has no more rows than coordinates. -/
theorem independent_rows_le_columns {K : Type*} [Field K] {s m : ℕ}
    (A : Matrix (Fin s) (Fin m) K) (hA : LinearIndependent K A.row) : s ≤ m := by
  obtain ⟨e, _⟩ := exists_nonsingular_coordinate_minor A hA
  simpa using Fintype.card_le_of_injective e e.injective

end NetworkSimplex.Threshold
