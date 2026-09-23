import Formal.MatroidSpectral.GraphicRepresentationForest
import Mathlib.Data.Matrix.Basic

/-! Incidence bases are spanning forests, and are trees in connected graphs. -/
namespace MatroidSpectral.Graphic
open SimpleGraph

variable {V : Type*} [LinearOrder V] [Finite V]

/-- The explicit rational incidence matrix, with one column per graph edge. -/
def incidenceMatrix (G : SimpleGraph V) : Matrix V (graphEdges G) ℚ :=
  fun v e => incidenceColumn e.1 v

/-- A basis of the ambient incidence-column span, using precisely the edges of H. -/
def IsIncidenceBasis (G H : SimpleGraph V) : Prop :=
  H ≤ G ∧ LinearIndepOn ℚ incidenceColumn (graphEdges H) ∧
    Submodule.span ℚ (incidenceColumn '' graphEdges H) =
      Submodule.span ℚ (incidenceColumn '' graphEdges G)

theorem edgeSpan_eq_iff_reachable_eq (G H : SimpleGraph V) :
    edgeSpan H = edgeSpan G ↔ H.Reachable = G.Reachable := by
  constructor
  · intro h
    funext u v
    apply propext
    rw [← vector_mem_iff_reachable H, h, vector_mem_iff_reachable]
  · intro h
    apply le_antisymm
    all_goals
      apply Submodule.span_le.mpr
      rintro _ ⟨u, v, huv, rfl⟩
      apply reachable_vector_mem
    · rw [← h]
      exact huv.reachable
    · rw [h]
      exact huv.reachable

theorem incidence_basis_iff_spanning_forest (G H : SimpleGraph V) :
    IsIncidenceBasis G H ↔ H ≤ G ∧ H.IsAcyclic ∧ H.Reachable = G.Reachable := by
  simp only [IsIncidenceBasis, incidence_independent_iff_acyclic, incidenceSpan_eq,
    edgeSpan_eq_iff_reachable_eq]

theorem incidence_basis_iff_maximal_forest (G H : SimpleGraph V) :
    IsIncidenceBasis G H ↔ Maximal (fun K => K ≤ G ∧ K.IsAcyclic) H := by
  rw [incidence_basis_iff_spanning_forest]
  constructor
  · rintro ⟨hle, ha, hr⟩
    exact (G.maximal_isAcyclic_iff_reachable_eq hle ha).mpr hr
  · intro h
    exact ⟨h.prop.1, h.prop.2, G.reachable_eq_of_maximal_isAcyclic H h⟩

theorem incidence_basis_iff_spanning_tree {G H : SimpleGraph V} (hG : G.Connected)
    (hHG : H ≤ G) : IsIncidenceBasis G H ↔ H.IsTree := by
  rw [incidence_basis_iff_maximal_forest]
  exact hG.maximal_le_isAcyclic_iff_isTree hHG

omit [Finite V] in
theorem incidenceMatrix_entry (G : SimpleGraph V) (v : V) (e : graphEdges G) :
    incidenceMatrix G v e = -1 ∨ incidenceMatrix G v e = 0 ∨
      incidenceMatrix G v e = 1 := by
  simp only [incidenceMatrix, incidenceColumn, edgeVector, Pi.sub_apply, Pi.single_apply]
  split_ifs <;> norm_num

end MatroidSpectral.Graphic
