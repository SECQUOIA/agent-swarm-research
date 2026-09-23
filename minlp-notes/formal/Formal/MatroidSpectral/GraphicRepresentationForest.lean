import Formal.MatroidSpectral.GraphicRepresentation
import Mathlib.LinearAlgebra.LinearIndependent.Basic

/-! An explicit rational incidence representation of finite simple graphs.

Ordering the vertices chooses an orientation. Each column has a positive entry
at its smaller endpoint and a negative entry at its larger endpoint.
-/
namespace MatroidSpectral.Graphic
open SimpleGraph

variable {V : Type*} [LinearOrder V]

abbrev OrientedEdge (V : Type*) [LinearOrder V] := {p : V × V // p.1 < p.2}

def incidenceColumn (e : OrientedEdge V) : V → ℚ := edgeVector e.1.1 e.1.2

def graphEdges (G : SimpleGraph V) : Set (OrientedEdge V) := {e | G.Adj e.1.1 e.1.2}

theorem oriented_edge_eq_iff (e f : OrientedEdge V) :
    s(e.1.1, e.1.2) = s(f.1.1, f.1.2) ↔ e = f := by
  constructor
  · intro h
    rcases Sym2.eq_iff.mp h with h | h
    · apply Subtype.ext
      exact Prod.ext h.1 h.2
    · have he := e.2
      have hf := f.2
      rw [h.1, h.2] at he
      exact (lt_asymm he hf).elim
  · rintro rfl
    rfl

theorem incidenceSpan_eq (G : SimpleGraph V) :
    Submodule.span ℚ (incidenceColumn '' graphEdges G) = edgeSpan G := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro _ ⟨e, he, rfl⟩
    exact adj_vector_mem G he
  · apply Submodule.span_le.mpr
    rintro _ ⟨u, v, huv, rfl⟩
    change edgeVector u v ∈ Submodule.span ℚ (incidenceColumn '' graphEdges G)
    rcases lt_or_gt_of_ne huv.ne with hlt | hgt
    · exact Submodule.subset_span ⟨⟨(u, v), hlt⟩, huv, rfl⟩
    · have hm : incidenceColumn (⟨(v, u), hgt⟩ : OrientedEdge V) ∈
          Submodule.span ℚ (incidenceColumn '' graphEdges G) :=
        Submodule.subset_span ⟨⟨(v, u), hgt⟩, huv.symm, rfl⟩
      change edgeVector v u ∈ _ at hm
      rw [edgeVector_reverse] at hm
      simpa only [neg_neg] using
        (Submodule.span ℚ (incidenceColumn '' graphEdges G)).neg_mem hm

theorem graphEdges_delete (G : SimpleGraph V) (e : OrientedEdge V) :
    graphEdges (G.deleteEdges {s(e.1.1, e.1.2)}) = graphEdges G \ {e} := by
  ext f
  simp only [graphEdges, Set.mem_ofPred_eq, deleteEdges_adj, Set.mem_singleton_iff,
    oriented_edge_eq_iff, Set.mem_sdiff]

theorem incidenceSpan_delete (G : SimpleGraph V) (e : OrientedEdge V) :
    Submodule.span ℚ (incidenceColumn '' (graphEdges G \ {e})) =
      edgeSpan (G.deleteEdges {s(e.1.1, e.1.2)}) := by
  rw [← graphEdges_delete, incidenceSpan_eq]

theorem incidence_independent_iff_acyclic [Finite V] (G : SimpleGraph V) :
    LinearIndepOn ℚ incidenceColumn (graphEdges G) ↔ G.IsAcyclic := by
  rw [linearIndepOn_iff_notMem_span]
  simp_rw [incidenceSpan_delete, incidenceColumn, vector_mem_iff_reachable]
  constructor
  · intro h
    apply isAcyclic_iff_forall_adj_isBridge.mpr
    intro u v huv
    rcases lt_or_gt_of_ne huv.ne with hlt | hgt
    · exact h ⟨(u, v), hlt⟩ huv
    · have hh := h ⟨(v, u), hgt⟩ huv.symm
      rw [isBridge_iff]
      intro hr
      apply hh
      simpa [Sym2.eq_swap] using hr.symm
  · intro h e he
    exact (isAcyclic_iff_forall_adj_isBridge.mp h he)

/-- Reversing any chosen set of column orientations leaves independence unchanged. -/
def reorientedColumn (reverse : OrientedEdge V → Bool) (e : OrientedEdge V) : V → ℚ :=
  (if reverse e then (-1 : ℚˣ) else 1) • incidenceColumn e

theorem reorientedColumn_eq (reverse : OrientedEdge V → Bool) (e : OrientedEdge V) :
    reorientedColumn reverse e =
      if reverse e then edgeVector e.1.2 e.1.1 else edgeVector e.1.1 e.1.2 := by
  unfold reorientedColumn
  split_ifs
  · rw [edgeVector_reverse]
    simp [incidenceColumn]
  · simp [incidenceColumn]

theorem reoriented_independent_iff (reverse : OrientedEdge V → Bool)
    (S : Set (OrientedEdge V)) :
    LinearIndepOn ℚ (reorientedColumn reverse) S ↔
      LinearIndepOn ℚ incidenceColumn S := by
  exact LinearIndependent.units_smul_iff (fun e : S => incidenceColumn e.1)
    (fun e : S => if reverse e.1 then (-1 : ℚˣ) else 1)

theorem reoriented_independent_iff_acyclic [Finite V] (G : SimpleGraph V)
    (reverse : OrientedEdge V → Bool) :
    LinearIndepOn ℚ (reorientedColumn reverse) (graphEdges G) ↔ G.IsAcyclic := by
  rw [reoriented_independent_iff, incidence_independent_iff_acyclic]

end MatroidSpectral.Graphic
