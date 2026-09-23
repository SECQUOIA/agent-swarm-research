import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.LinearAlgebra.Determinant
import Mathlib.LinearAlgebra.Basis.VectorSpace

namespace QuadraticPrecision
open MeasureTheory Module

/-- Positive volume supplies a full-dimensional contact simplex, for any origin. -/
theorem exists_nondegenerate_contacts {d : ℕ} {S : Set (Fin d → ℝ)}
    (hS : volume S ≠ 0) (o : Fin d → ℝ) :
    ∃ t : Fin d → S, Matrix.det (fun i j => (t j).val i - o i) ≠ 0 := by
  classical
  let T := (fun x : Fin d → ℝ => x - o) '' S
  have hT : volume T ≠ 0 := by
    simpa [T, sub_eq_add_neg, Set.image_add_right, measure_preimage_add_right] using hS
  have hspan : ⊤ ≤ Submodule.span ℝ T := by
    by_contra h
    have hn : Submodule.span ℝ T ≠ ⊤ := by simpa using h
    exact hT (measure_mono_null Submodule.subset_span
      (Measure.addHaar_submodule volume _ hn))
  let ι := (linearIndepOn_empty ℝ (id : (Fin d → ℝ) → (Fin d → ℝ))).extend (Set.empty_subset T)
  let b : Basis ι ℝ (Fin d → ℝ) := Basis.ofSpan hspan
  let := Fintype.ofFinite ι
  have hc : Fintype.card ι = Fintype.card (Fin d) := by
    rw [← Module.finrank_eq_card_basis b, Module.finrank_pi]
  let e := Fintype.equivOfCardEq hc
  let c := b.reindex e
  have hm (j : Fin d) : c j ∈ T := by
    apply Basis.ofSpan_subset hspan
    refine ⟨e.symm j, ?_⟩
    change b (e.symm j) = b.reindex e j
    exact (Basis.reindex_apply b e j).symm
  choose t ht hte using hm
  refine ⟨fun j => ⟨t j, ht j⟩, ?_⟩
  have hd := (Pi.basisFun ℝ (Fin d)).isUnit_det c
  have heq : (fun i j => t j i - o i) = (Pi.basisFun ℝ (Fin d)).toMatrix c := by
    ext i j
    change (t j - o) i = c j i
    exact congrFun (hte j) i
  rw [heq]
  exact hd.ne_zero

end QuadraticPrecision
