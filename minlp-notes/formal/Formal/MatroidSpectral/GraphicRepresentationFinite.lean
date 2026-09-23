import Formal.MatroidSpectral.GraphicRepresentationBasis
import Formal.MatroidSpectral.RepresentationReduction

/-! Finite indexing connects the explicit graph matrix to the input format. -/
namespace MatroidSpectral.Graphic
open SimpleGraph Matrix

variable {n m : ℕ} (G : SimpleGraph (Fin n)) (e : Fin m ≃ graphEdges G)

def finiteIncidence : RationalRepresentation n m := fun v j => incidenceMatrix G v (e j)

noncomputable def selectedColumns (H : SimpleGraph (Fin n)) : Finset (Fin m) := by
  classical
  exact Finset.univ.filter (fun j => H.Adj (e j).1.1.1 (e j).1.1.2)

@[simp] theorem mem_selectedColumns (H : SimpleGraph (Fin n)) (j : Fin m) :
    j ∈ selectedColumns G e H ↔ H.Adj (e j).1.1.1 (e j).1.1.2 := by
  classical
  simp [selectedColumns]

noncomputable def selectedEquiv (H : SimpleGraph (Fin n)) (hHG : H ≤ G) :
    selectedColumns G e H ≃ graphEdges H where
  toFun j := ⟨(e j).1, (mem_selectedColumns G e H j).mp j.2⟩
  invFun f := ⟨e.symm ⟨f.1, hHG f.2⟩, by
    rw [mem_selectedColumns]
    simp only [e.apply_symm_apply]
    exact f.2⟩
  left_inv j := by
    apply Subtype.ext
    exact e.symm_apply_apply j
  right_inv f := by
    apply Subtype.ext
    change (e (e.symm ⟨f.1, hHG f.2⟩)).1 = f.1
    exact congrArg (fun z : graphEdges G => z.1) (e.apply_symm_apply ⟨f.1, hHG f.2⟩)

theorem selected_independent_iff (H : SimpleGraph (Fin n)) (hHG : H ≤ G) :
    ColumnIndependent (finiteIncidence G e) (selectedColumns G e H) ↔
      LinearIndepOn ℚ incidenceColumn (graphEdges H) := by
  exact linearIndependent_equiv' (selectedEquiv G e H hHG) rfl

theorem selected_column_range (H : SimpleGraph (Fin n)) (hHG : H ≤ G) :
    Set.range (fun j : selectedColumns G e H => (finiteIncidence G e).col j) =
      incidenceColumn '' graphEdges H := by
  ext x
  constructor
  · rintro ⟨j, rfl⟩
    exact ⟨(e j).1, (mem_selectedColumns G e H j).mp j.2, rfl⟩
  · rintro ⟨f, hf, rfl⟩
    obtain ⟨j, hj⟩ := (selectedEquiv G e H hHG).surjective ⟨f, hf⟩
    refine ⟨j, ?_⟩
    exact congrArg (fun z : graphEdges H => incidenceColumn z.1) hj

theorem full_column_range : Set.range (finiteIncidence G e).col =
    incidenceColumn '' graphEdges G := by
  ext x
  constructor
  · rintro ⟨j, rfl⟩
    exact ⟨(e j).1, (e j).2, rfl⟩
  · rintro ⟨f, hf, rfl⟩
    obtain ⟨j, hj⟩ := e.surjective ⟨f, hf⟩
    exact ⟨j, congrArg (fun z : graphEdges G => incidenceColumn z.1) hj⟩

theorem finiteIncidence_base_iff (H : SimpleGraph (Fin n)) (hHG : H ≤ G) :
    IsColumnBase (finiteIncidence G e) (selectedColumns G e H) ↔
      H.IsAcyclic ∧ H.Reachable = G.Reachable := by
  rw [isColumnBase_iff_span, selected_independent_iff G e H hHG,
    selected_column_range G e H hHG, full_column_range,
    incidence_independent_iff_acyclic, incidenceSpan_eq, incidenceSpan_eq,
    edgeSpan_eq_iff_reachable_eq]

theorem finiteIncidence_base_iff_tree {H : SimpleGraph (Fin n)} (hG : G.Connected)
    (hHG : H ≤ G) :
    IsColumnBase (finiteIncidence G e) (selectedColumns G e H) ↔ H.IsTree := by
  rw [finiteIncidence_base_iff G e H hHG]
  have h := incidence_basis_iff_spanning_tree hG hHG
  rw [incidence_basis_iff_spanning_forest] at h
  simpa only [hHG, true_and] using h

theorem reducedIncidence_base_iff (H : SimpleGraph (Fin n)) (hHG : H ≤ G) :
    IsBase (reducedRepresentation (finiteIncidence G e)) (selectedColumns G e H) ↔
      H.IsAcyclic ∧ H.Reachable = G.Reachable := by
  rw [reducedRepresentation_isBase_iff, finiteIncidence_base_iff G e H hHG]

theorem finiteIncidence_entry (v : Fin n) (j : Fin m) :
    finiteIncidence G e v j = -1 ∨ finiteIncidence G e v j = 0 ∨
      finiteIncidence G e v j = 1 :=
  incidenceMatrix_entry G v (e j)

/-- The graph of an arbitrary selected set of matrix columns. -/
def selectedGraph (B : Finset (Fin m)) : SimpleGraph (Fin n) :=
  fromEdgeSet {a | ∃ j ∈ B, s((e j).1.1.1, (e j).1.1.2) = a}

theorem selectedGraph_le (B : Finset (Fin m)) : selectedGraph G e B ≤ G := by
  intro u v huv
  rw [selectedGraph, fromEdgeSet_adj] at huv
  obtain ⟨⟨j, _, hj⟩, _⟩ := huv
  have hmem : s(u, v) ∈ G.edgeSet := by
    rw [← hj]
    exact (e j).2
  exact hmem

@[simp] theorem selectedColumns_selectedGraph (B : Finset (Fin m)) :
    selectedColumns G e (selectedGraph G e B) = B := by
  ext j
  rw [mem_selectedColumns, selectedGraph, fromEdgeSet_adj]
  constructor
  · rintro ⟨⟨k, hk, he⟩, _⟩
    have hkj : k = j := e.injective (Subtype.ext ((oriented_edge_eq_iff _ _).mp he))
    simpa only [hkj] using hk
  · intro hj
    exact ⟨⟨j, hj, rfl⟩, ne_of_lt (e j).1.2⟩

theorem arbitrary_columns_independent_iff (B : Finset (Fin m)) :
    ColumnIndependent (finiteIncidence G e) B ↔ (selectedGraph G e B).IsAcyclic := by
  have h := selected_independent_iff G e (selectedGraph G e B) (selectedGraph_le G e B)
  simpa only [selectedColumns_selectedGraph, incidence_independent_iff_acyclic] using h

/-- Every actual column basis, not just a preselected forest, has the stated graph meaning. -/
theorem arbitrary_columns_base_iff (B : Finset (Fin m)) :
    IsColumnBase (finiteIncidence G e) B ↔
      (selectedGraph G e B).IsAcyclic ∧
        (selectedGraph G e B).Reachable = G.Reachable := by
  simpa only [selectedColumns_selectedGraph] using
    finiteIncidence_base_iff G e (selectedGraph G e B) (selectedGraph_le G e B)

theorem arbitrary_reduced_columns_base_iff (B : Finset (Fin m)) :
    IsBase (reducedRepresentation (finiteIncidence G e)) B ↔
      (selectedGraph G e B).IsAcyclic ∧
        (selectedGraph G e B).Reachable = G.Reachable := by
  rw [reducedRepresentation_isBase_iff, arbitrary_columns_base_iff]

theorem arbitrary_columns_tree_iff (B : Finset (Fin m)) (hG : G.Connected) :
    IsColumnBase (finiteIncidence G e) B ↔ (selectedGraph G e B).IsTree := by
  simpa only [selectedColumns_selectedGraph] using
    finiteIncidence_base_iff_tree G e hG (selectedGraph_le G e B)

end MatroidSpectral.Graphic
