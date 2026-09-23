import Formal.MultilinearGap.StructuralFrequencyComponents
import Formal.MultilinearGap.StructuralFrequencyOddCycle

/-! Extracting indexed cycles from the fractional incidence graph. -/
namespace MultilinearGap.FrequencySlab
open Set
noncomputable section
variable {V E : Type*} [Fintype V] [Fintype E] [DecidableEq E]

omit [Fintype E] in
theorem fractional_incident_iff_pair {S : V → Finset E}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {e : E} {v w : V} (hne : v ≠ w)
    (hev : e ∈ S v) (hew : e ∈ S w) (t : V) :
    e ∈ S t ↔ t = v ∨ t = w := by
  classical
  have hsub : {v,w} ⊆ Finset.univ.filter (fun t => e ∈ S t) := by
    intro t ht
    simp only [Finset.mem_insert, Finset.mem_singleton] at ht
    rcases ht with rfl | rfl <;> simp [hev, hew]
  have heq := Finset.eq_of_subset_of_card_le hsub (by simpa [hne] using hfreq e)
  have hh := congrArg (fun A : Finset V => t ∈ A) heq
  simpa using (Iff.of_eq hh).symm

/-- A component indexed in cyclic order, before proving its length odd. -/
structure IndexedFractionalCycle (S : V → Finset E) (x : E → ℝ)
    (A : Set V) where
  n : ℕ
  three_le : 3 ≤ n
  row : Fin n → V
  edge : Fin n → E
  row_injective : Function.Injective row
  edge_injective : Function.Injective edge
  row_range : Set.range row = A
  fractional_edge : ∀ i, edge i ∈ fractional x
  endpoints : letI : NeZero n := ⟨by omega⟩; ∀ i v, edge i ∈ S v ↔ v = row i ∨ v = row (i + 1)

omit [Fintype V] in
theorem cycle_getVert_add_one {G : SimpleGraph V} {v : V} (p : G.Walk v v)
    (hn : 0 < p.length) [NeZero p.length] (i : Fin p.length) :
    p.getVert (i + 1).val = p.getVert (i.val + 1) := by
  classical
  have : NeZero p.length := ⟨by omega⟩
  by_cases h : i.val + 1 < p.length
  · rw [Fin.val_add_one_of_lt' h]
  · have hi : i.val + 1 = p.length := by omega
    have hz : i + 1 = 0 := by
      apply Fin.ext
      simp [Fin.val_add, hi]
    rw [hz, Fin.val_zero, hi, p.getVert_zero, p.getVert_length]

/-- Every graph cycle gives actual coordinate edges with exact original-row
incidence. No graph edge is confused with a parallel input coordinate. -/
theorem indexedFractionalCycle_of_walk {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (_hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {v : V} (p : (fractionalGraph S lo hi x).Walk v v) (hp : p.IsCycle) :
    Nonempty (IndexedFractionalCycle S x p.toSubgraph.verts) := by
  classical
  have hn := hp.isCircuit.three_le_length
  have : NeZero p.length := ⟨by omega⟩
  let row : Fin p.length → V := fun i => p.getVert i.val
  have hrow : Function.Injective row := by
    intro i j hij
    apply Fin.ext
    exact hp.getVert_injOn' (by change i.val ≤ _; omega)
      (by change j.val ≤ _; omega) hij
  have hadj (i : Fin p.length) : (fractionalGraph S lo hi x).Adj (row i) (row (i+1)) := by
    change (fractionalGraph S lo hi x).Adj (p.getVert i.val) (p.getVert (i+1).val)
    rw [cycle_getVert_add_one p (by omega)]
    exact p.adj_getVert_succ i.isLt
  choose edge he using (fun i => (hadj i).2.2.2)
  have hend (i : Fin p.length) (t : V) :
      edge i ∈ S t ↔ t = row i ∨ t = row (i+1) :=
    fractional_incident_iff_pair hfreq (hadj i).1 (he i).2.1 (he i).2.2 t
  have hedge : Function.Injective edge := by
    intro i j hij
    have h1 : row i = row j ∨ row i = row (j+1) :=
      (hend j _).mp (hij ▸ (he i).2.1)
    rcases h1 with h1 | h1
    · exact hrow h1
    have h2 : row (i+1) = row j ∨ row (i+1) = row (j+1) :=
      (hend j _).mp (hij ▸ (he i).2.2)
    rcases h2 with h2 | h2
    · have hi := hrow h1
      have hj := hrow h2
      have hh : (1 + 1 : Fin p.length) = 0 := by
        apply add_left_cancel (a := j)
        simpa only [add_assoc, add_zero] using (show j + 1 + 1 = j by rw [← hi, hj])
      have htwo : (1 + 1 : Fin p.length).val = 2 := by
        norm_num [Fin.val_add, Fin.val_natCast,
          Nat.mod_eq_of_lt (by omega : 1 < p.length),
          Nat.mod_eq_of_lt (by omega : 2 < p.length)]
      have hh' := congrArg Fin.val hh
      rw [htwo, Fin.val_zero] at hh'
      omega
    · exact add_right_cancel (hrow h2)
  refine ⟨⟨p.length, hn, row, edge, hrow, hedge, ?_, fun i => (he i).1, hend⟩⟩
  ext t
  rw [p.mem_verts_toSubgraph]
  constructor
  · rintro ⟨i, rfl⟩
    exact p.getVert_mem_support _
  · intro ht
    obtain ⟨i, hi, hile⟩ := p.mem_support_iff_exists_getVert.mp ht
    by_cases hil : i < p.length
    · exact ⟨⟨i,hil⟩, hi⟩
    · have hil' : i = p.length := by omega
      refine ⟨⟨0, by omega⟩, ?_⟩
      simpa [row, hil'] using hi

namespace IndexedFractionalCycle
variable {S : V → Finset E} {lo hi : V → ℤ} {x : E → ℝ} {A : Set V}
variable (D : IndexedFractionalCycle S x A)

instance : NeZero D.n := ⟨by have := D.three_le; omega⟩

theorem incident
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    (hx : x ∈ (slab S lo hi).extremePoints ℝ) (i : Fin D.n) (e : E) :
    e ∈ S (D.row i) ∧ e ∈ fractional x ↔
      e = D.edge i ∨ e = D.edge (i-1) := by
  classical
  have hfirst : D.edge i ∈ S (D.row i) ∩ fractional x :=
    Finset.mem_inter.mpr ⟨(D.endpoints i _).mpr (Or.inl rfl), D.fractional_edge i⟩
  have hsecond : D.edge (i-1) ∈ S (D.row i) ∩ fractional x :=
    Finset.mem_inter.mpr ⟨(D.endpoints (i-1) _).mpr (Or.inr (by simp)),
      D.fractional_edge (i-1)⟩
  have hne : D.edge i ≠ D.edge (i-1) := by
    intro h
    have hh := D.edge_injective h
    have hz : (1 : Fin D.n) = 0 := by
      have := sub_eq_self.mp hh.symm
      exact this
    have hn := D.three_le
    have hh' := congrArg Fin.val hz
    norm_num [Fin.val_natCast, Nat.mod_eq_of_lt (by omega : 1 < D.n)] at hh' 
  have hv := active_of_fractional_incident hfreq hx (D.fractional_edge i)
    (Finset.mem_inter.mp hfirst).1
  have heq : {D.edge i, D.edge (i-1)} = S (D.row i) ∩ fractional x := by
    apply Finset.eq_of_subset_of_card_le
    · intro e he
      simp only [Finset.mem_insert, Finset.mem_singleton] at he
      rcases he with rfl | rfl <;> assumption
    · rw [(extreme_fractional_degree_two hfreq hx).1 _ hv]
      simp [hne]
  simpa only [Finset.mem_inter, Finset.mem_insert, Finset.mem_singleton] using
    (congrArg (fun T : Finset E => e ∈ T) heq.symm |> Iff.of_eq)

omit [Fintype V] [DecidableEq E] in
theorem outside (v : V) (hv : ∀ i, D.row i ≠ v) (i : Fin D.n) : D.edge i ∉ S v := by
  classical
  intro h
  rcases (D.endpoints i v).mp h with h | h
  · exact hv i h.symm
  · exact hv (i+1) h.symm

theorem odd (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2) : Odd D.n :=
  extreme_indexed_cycle_odd hx D.edge D.row D.edge_injective D.fractional_edge
    (D.incident hfreq hx) D.outside

end IndexedFractionalCycle

/-- All fractional coordinates are partitioned by finitely many actual graph
components, with no repeated row between the extracted cycles. -/
theorem exists_indexed_cycle_family {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ) :
    ∃ (n : ℕ) (A : Fin n → Set V) (D : (c : Fin n) → IndexedFractionalCycle S x (A c)),
      Function.Injective (fun t : (c : Fin n) × Fin (D c).n => (D t.1).row t.2) ∧
      (∀ e ∈ fractional x, ∃ c i, (D c).edge i = e) := by
  classical
  classical
  let G := fractionalGraph S lo hi x
  let C := {c : G.ConnectedComponent // ∃ v ∈ active S lo hi x, v ∈ c.supp}
  let : Fintype C := Fintype.ofFinite C
  let equiv := Fintype.equivFin C
  let component (c : Fin (Fintype.card C)) : G.ConnectedComponent := (equiv.symm c).val
  let A (c : Fin (Fintype.card C)) := (component c).supp
  have hex (c : Fin (Fintype.card C)) : Nonempty (IndexedFractionalCycle S x (A c)) := by
    obtain ⟨v,hv,hvc⟩ := (equiv.symm c).property
    obtain ⟨p,hp,hverts⟩ := fractionalGraph_component_cycle hfreq hx hv hvc
    have hd := indexedFractionalCycle_of_walk hfreq hx p hp
    simpa only [hverts] using hd
  let D (c : Fin (Fintype.card C)) : IndexedFractionalCycle S x (A c) :=
    Classical.choice (hex c)
  have hmem (c : Fin (Fintype.card C)) (i : Fin (D c).n) :
      (D c).row i ∈ (component c).supp := by
    change (D c).row i ∈ A c
    exact (Set.ext_iff.mp (D c).row_range _).mp ⟨i,rfl⟩
  refine ⟨Fintype.card C, A, D, ?_, ?_⟩
  · rintro ⟨c,i⟩ ⟨d,j⟩ h
    change (D c).row i = (D d).row j at h
    have hcd : component c = component d :=
      SimpleGraph.ConnectedComponent.eq_of_common_vertex (hmem c i) (h.symm ▸ hmem d j)
    have heq : c = d := equiv.symm.injective (Subtype.ext hcd)
    subst d
    have hij := (D c).row_injective h
    subst j
    rfl
  · intro e he
    have hcard := (extreme_fractional_degree_two hfreq hx).2 e he
    obtain ⟨v,hv⟩ := Finset.card_pos.mp (show 0 <
        ((active S lo hi x).filter fun v => e ∈ S v).card by omega)
    obtain ⟨hv,hev⟩ := Finset.mem_filter.mp hv
    let c : C := ⟨G.connectedComponentMk v, v, hv,
      SimpleGraph.ConnectedComponent.connectedComponentMk_mem⟩
    have hvc : v ∈ A (equiv c) := by
      change v ∈ ((equiv.symm (equiv c)).val).supp
      simp only [Equiv.symm_apply_apply]
      exact SimpleGraph.ConnectedComponent.connectedComponentMk_mem
    rw [← (D (equiv c)).row_range] at hvc
    obtain ⟨i,hi⟩ := hvc
    have hh := ((D (equiv c)).incident hfreq hx i e).mp ⟨hi ▸ hev, he⟩
    rcases hh with hh | hh
    · exact ⟨equiv c, i, hh.symm⟩
    · exact ⟨equiv c, i-1, hh.symm⟩

end
end MultilinearGap.FrequencySlab
