import Formal.MatroidSpectral.GraphicRepresentationFinite

/-! Arbitrary labelled multigraphs, including loops and parallel edges.

Deleting an edge deletes its label, not all edges with the same endpoints.
The forest predicate says that each selected edge separates its endpoints
when deleted. Reachability is actual walk reachability in the underlying
simple graph, so this predicate also excludes loops and parallel-edge cycles.
-/
namespace MatroidSpectral.Graphic
open SimpleGraph Matrix

variable {n m : ℕ} (tail head : Fin m → Fin n)

def multigraphIncidence : RationalRepresentation n m :=
  fun v e => edgeVector (tail e) (head e) v

def underlyingGraph (B : Finset (Fin m)) : SimpleGraph (Fin n) :=
  fromEdgeSet {a | ∃ e ∈ B, s(tail e, head e) = a}

def IsMultigraphForest (B : Finset (Fin m)) : Prop :=
  ∀ e ∈ B, ¬(underlyingGraph tail head (B.erase e)).Reachable (tail e) (head e)

theorem multigraph_span_eq (B : Finset (Fin m)) :
    Submodule.span ℚ ((multigraphIncidence tail head).col '' (B : Set (Fin m))) =
      edgeSpan (underlyingGraph tail head B) := by
  apply le_antisymm
  · apply Submodule.span_le.mpr
    rintro _ ⟨e, he, rfl⟩
    change edgeVector (tail e) (head e) ∈ _
    by_cases h : tail e = head e
    · simp [h, edgeVector_self]
    · apply adj_vector_mem
      rw [underlyingGraph, fromEdgeSet_adj]
      exact ⟨⟨e, he, rfl⟩, h⟩
  · apply Submodule.span_le.mpr
    rintro _ ⟨u, v, huv, rfl⟩
    rw [underlyingGraph, fromEdgeSet_adj] at huv
    obtain ⟨⟨e, he, heq⟩, _⟩ := huv
    have hm : edgeVector (tail e) (head e) ∈
        Submodule.span ℚ ((multigraphIncidence tail head).col '' (B : Set (Fin m))) :=
      Submodule.subset_span ⟨e, he, rfl⟩
    change edgeVector u v ∈ Submodule.span ℚ _
    rcases Sym2.eq_iff.mp heq with h | h
    · simpa only [h.1, h.2] using hm
    · rw [h.1, h.2, edgeVector_reverse] at hm
      simpa only [neg_neg] using
        (Submodule.span ℚ ((multigraphIncidence tail head).col '' (B : Set (Fin m)))).neg_mem hm

theorem multigraph_independent_iff_forest (B : Finset (Fin m)) :
    ColumnIndependent (multigraphIncidence tail head) B ↔ IsMultigraphForest tail head B := by
  change LinearIndepOn ℚ (multigraphIncidence tail head).col (B : Set (Fin m)) ↔ _
  rw [linearIndepOn_iff_notMem_span]
  simp only [IsMultigraphForest]
  apply forall_congr'
  intro e
  apply imp_congr_right
  intro _
  rw [← Finset.coe_erase, multigraph_span_eq]
  exact not_congr (vector_mem_iff_reachable _ _ _)

theorem multigraph_range_eq_image (B : Finset (Fin m)) :
    Set.range (fun e : B => (multigraphIncidence tail head).col e) =
      (multigraphIncidence tail head).col '' (B : Set (Fin m)) := by
  ext x
  constructor
  · rintro ⟨e, rfl⟩
    exact ⟨e, e.2, rfl⟩
  · rintro ⟨e, he, rfl⟩
    exact ⟨⟨e, he⟩, rfl⟩

theorem multigraph_base_iff_spanning_forest (B : Finset (Fin m)) :
    IsColumnBase (multigraphIncidence tail head) B ↔
      IsMultigraphForest tail head B ∧
        (underlyingGraph tail head B).Reachable =
          (underlyingGraph tail head Finset.univ).Reachable := by
  rw [isColumnBase_iff_span, multigraph_independent_iff_forest,
    multigraph_range_eq_image, multigraph_span_eq]
  have he : Set.range (multigraphIncidence tail head).col =
      (multigraphIncidence tail head).col '' ((Finset.univ : Finset (Fin m)) : Set (Fin m)) := by
    simp
  rw [he, multigraph_span_eq, edgeSpan_eq_iff_reachable_eq]

theorem multigraph_reduced_base_iff_spanning_forest (B : Finset (Fin m)) :
    IsBase (reducedRepresentation (multigraphIncidence tail head)) B ↔
      IsMultigraphForest tail head B ∧
        (underlyingGraph tail head B).Reachable =
          (underlyingGraph tail head Finset.univ).Reachable := by
  rw [reducedRepresentation_isBase_iff, multigraph_base_iff_spanning_forest]

theorem multigraph_loop_excluded {B : Finset (Fin m)}
    (hB : IsMultigraphForest tail head B) {e : Fin m} (he : e ∈ B) : tail e ≠ head e := by
  intro h
  apply hB e he
  rw [h]

theorem multigraph_parallel_excluded {B : Finset (Fin m)}
    (hB : IsMultigraphForest tail head B) {e f : Fin m}
    (he : e ∈ B) (hf : f ∈ B) (hpar : s(tail e, head e) = s(tail f, head f)) : e = f := by
  by_contra hne
  apply hB e he
  apply Adj.reachable
  rw [underlyingGraph, fromEdgeSet_adj]
  exact ⟨⟨f, Finset.mem_erase.mpr ⟨Ne.symm hne, hf⟩, hpar.symm⟩,
    multigraph_loop_excluded tail head hB he⟩

theorem underlying_delete_le_erase (B : Finset (Fin m)) (e : Fin m) :
    (underlyingGraph tail head B).deleteEdges {s(tail e, head e)} ≤
      underlyingGraph tail head (B.erase e) := by
  intro u v huv
  rw [deleteEdges_adj, underlyingGraph, fromEdgeSet_adj] at huv
  obtain ⟨⟨⟨f, hf, hfe⟩, hne⟩, he⟩ := huv
  rw [underlyingGraph, fromEdgeSet_adj]
  refine ⟨⟨f, Finset.mem_erase.mpr ⟨?_, hf⟩, hfe⟩, hne⟩
  intro h
  subst f
  exact he (Set.mem_singleton_iff.mpr hfe.symm)

theorem multigraph_forest_acyclic {B : Finset (Fin m)}
    (hB : IsMultigraphForest tail head B) : (underlyingGraph tail head B).IsAcyclic := by
  apply isAcyclic_iff_forall_adj_isBridge.mpr
  intro u v huv
  rw [underlyingGraph, fromEdgeSet_adj] at huv
  obtain ⟨⟨e, he, heq⟩, _⟩ := huv
  rw [isBridge_iff]
  intro hr
  rw [← heq] at hr
  have hh := hr.mono (underlying_delete_le_erase tail head B e)
  apply hB e he
  rcases Sym2.eq_iff.mp heq with h | h
  · simpa only [h.1, h.2] using hh
  · simpa only [h.1, h.2] using hh.symm

theorem multigraph_forest_of_acyclic {B : Finset (Fin m)}
    (ha : (underlyingGraph tail head B).IsAcyclic)
    (hl : ∀ e ∈ B, tail e ≠ head e)
    (hp : ∀ e ∈ B, ∀ f ∈ B, s(tail e, head e) = s(tail f, head f) → e = f) :
    IsMultigraphForest tail head B := by
  intro e he hr
  have hadj : (underlyingGraph tail head B).Adj (tail e) (head e) := by
    rw [underlyingGraph, fromEdgeSet_adj]
    exact ⟨⟨e, he, rfl⟩, hl e he⟩
  apply (isAcyclic_iff_forall_adj_isBridge.mp ha hadj)
  apply hr.mono
  intro u v huv
  rw [underlyingGraph, fromEdgeSet_adj] at huv
  obtain ⟨⟨f, hf, hfe⟩, hne⟩ := huv
  rw [deleteEdges_adj, underlyingGraph, fromEdgeSet_adj]
  refine ⟨⟨⟨f, (Finset.mem_erase.mp hf).2, hfe⟩, hne⟩, ?_⟩
  intro h
  have heq := hp f (Finset.mem_erase.mp hf).2 e he
    (hfe.trans (Set.mem_singleton_iff.mp h))
  exact (Finset.mem_erase.mp hf).1 heq

theorem multigraph_forest_iff (B : Finset (Fin m)) :
    IsMultigraphForest tail head B ↔
      (underlyingGraph tail head B).IsAcyclic ∧
      (∀ e ∈ B, tail e ≠ head e) ∧
      (∀ e ∈ B, ∀ f ∈ B, s(tail e, head e) = s(tail f, head f) → e = f) := by
  constructor
  · intro h
    exact ⟨multigraph_forest_acyclic tail head h,
      fun _ he => multigraph_loop_excluded tail head h he,
      fun _ he _ hf hp => multigraph_parallel_excluded tail head h he hf hp⟩
  · rintro ⟨ha, hl, hp⟩
    exact multigraph_forest_of_acyclic tail head ha hl hp

/-- In a connected multigraph, bases are spanning trees with no selected loop
or pair of parallel labelled edges. -/
theorem multigraph_base_iff_spanning_tree (B : Finset (Fin m))
    (hG : (underlyingGraph tail head Finset.univ).Connected) :
    IsColumnBase (multigraphIncidence tail head) B ↔
      (underlyingGraph tail head B).IsTree ∧
      (∀ e ∈ B, tail e ≠ head e) ∧
      (∀ e ∈ B, ∀ f ∈ B, s(tail e, head e) = s(tail f, head f) → e = f) := by
  rw [multigraph_base_iff_spanning_forest, multigraph_forest_iff]
  constructor
  · rintro ⟨⟨ha, hl, hp⟩, hr⟩
    refine ⟨⟨?_, ha⟩, hl, hp⟩
    refine { preconnected := ?_, nonempty := hG.nonempty }
    intro u v
    rw [hr]
    exact hG u v
  · rintro ⟨ht, hl, hp⟩
    refine ⟨⟨ht.isAcyclic, hl, hp⟩, ?_⟩
    funext u v
    exact propext ⟨fun _ => hG u v, fun _ => ht.connected u v⟩

theorem multigraphIncidence_entry (v : Fin n) (e : Fin m) :
    multigraphIncidence tail head v e = -1 ∨
      multigraphIncidence tail head v e = 0 ∨
      multigraphIncidence tail head v e = 1 := by
  simp only [multigraphIncidence, edgeVector, Pi.sub_apply, Pi.single_apply]
  split_ifs <;> norm_num

end MatroidSpectral.Graphic
