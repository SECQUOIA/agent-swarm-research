import Formal.MultilinearGap.StructuralFrequencySlab

/-! The fractional incidence graph at an extreme degree-slab point.
Parallel fractional edges are excluded by the actual extremality equations.
The remaining graph consists of vertex-disjoint simple cycles. -/
namespace MultilinearGap.FrequencySlab
open Set
noncomputable section
variable {V E : Type*} [Fintype V] [Fintype E] [DecidableEq V] [DecidableEq E]

omit [DecidableEq V] in
/-- Two fractional coordinates cannot have the same active incidence column. -/
theorem extreme_fractional_column_injective {S : V → Finset E} {lo hi : V → ℤ}
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {e f : E} (he : e ∈ fractional x) (hf : f ∈ fractional x)
    (hcol : ∀ v ∈ active S lo hi x, e ∈ S v ↔ f ∈ S v) : e = f := by
  classical
  by_contra hne
  let d : E → ℝ := fun g => (if g = e then 1 else 0) - (if g = f then 1 else 0)
  have hz : d = 0 := extreme_kernel_eq_zero hx (fun g hg => by
    have hge : g ≠ e := fun h => hg (h ▸ he)
    have hgf : g ≠ f := fun h => hg (h ▸ hf)
    simp [d, hge, hgf]) (by
      intro v hv
      simp only [degree, d, Finset.sum_sub_distrib]
      simp [← hcol v hv])
  have h := congrFun hz e
  norm_num [d, hne] at h

private theorem pair_of_card_two {A : Type*} [DecidableEq A]
    {s : Finset A} (hs : s.card = 2) {v : A} (hv : v ∈ s) :
    ∃ w, v ≠ w ∧ s = {v, w} := by
  classical
  obtain ⟨a, b, hab, rfl⟩ := Finset.card_eq_two.mp hs
  simp only [Finset.mem_insert, Finset.mem_singleton] at hv
  rcases hv with ha | hb
  · subst v; exact ⟨b, hab, rfl⟩
  · subst v; exact ⟨a, hab.symm, Finset.pair_comm a b⟩

/-- Every fractional edge has exactly one other active endpoint. -/
theorem extreme_other_endpoint {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {e : E} (he : e ∈ fractional x) {v : V}
    (hv : v ∈ active S lo hi x) (hev : e ∈ S v) :
    ∃ w, v ≠ w ∧ ((active S lo hi x).filter fun t => e ∈ S t) = {v, w} :=
  pair_of_card_two ((extreme_fractional_degree_two hfreq hx).2 e he)
    (Finset.mem_filter.mpr ⟨hv, hev⟩)

omit [DecidableEq V] in
/-- Parallel fractional edges are impossible, including in multigraph input. -/
theorem extreme_no_parallel_fractional {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {e f : E} (he : e ∈ fractional x) (hf : f ∈ fractional x)
    {v w : V} (hne : v ≠ w) (hv : v ∈ active S lo hi x) (hw : w ∈ active S lo hi x)
    (hev : e ∈ S v) (hew : e ∈ S w) (hfv : f ∈ S v) (hfw : f ∈ S w) : e = f := by
  classical
  have hend (g : E) (hg : g ∈ fractional x) (hgv : g ∈ S v) (hgw : g ∈ S w) :
      ((active S lo hi x).filter fun t => g ∈ S t) = {v,w} := by
    apply Finset.eq_of_subset_of_card_le
    · intro t ht
      have hp : {v,w} ⊆ (active S lo hi x).filter fun t => g ∈ S t := by
        intro t ht
        simp only [Finset.mem_insert, Finset.mem_singleton] at ht
        rcases ht with rfl | rfl
        · exact Finset.mem_filter.mpr ⟨hv, hgv⟩
        · exact Finset.mem_filter.mpr ⟨hw, hgw⟩
      have heq := Finset.eq_of_subset_of_card_le hp (by
        rw [(extreme_fractional_degree_two hfreq hx).2 g hg]
        simp [hne])
      exact heq ▸ ht
    · rw [(extreme_fractional_degree_two hfreq hx).2 g hg]
      simp [hne]
  apply extreme_fractional_column_injective hx he hf
  intro t ht
  have h := congrArg (fun A : Finset V => t ∈ A)
    ((hend e he hev hew).trans (hend f hf hfv hfw).symm)
  simpa only [Finset.mem_filter, ht, true_and] using Iff.of_eq h

/-- The simple graph of fractional shared coordinates on the original rows. -/
def fractionalGraph (S : V → Finset E) (lo hi : V → ℤ) (x : E → ℝ) : SimpleGraph V where
  Adj v w := v ≠ w ∧ v ∈ active S lo hi x ∧ w ∈ active S lo hi x ∧
    ∃ e ∈ fractional x, e ∈ S v ∧ e ∈ S w
  symm := ⟨by
    rintro v w ⟨hne,hv,hw,e,he,hev,hew⟩
    exact ⟨hne.symm,hw,hv,e,he,hew,hev⟩⟩
  loopless := ⟨by intro v h; exact h.1 rfl⟩

omit [DecidableEq V] in
/-- At every active row there are exactly two distinct graph neighbors. -/
theorem fractionalGraph_neighbors {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {v : V} (hv : v ∈ active S lo hi x) :
    ∃ w u : V, w ≠ u ∧ (fractionalGraph S lo hi x).neighborSet v = {w,u} := by
  classical
  obtain ⟨e, f, hef, hrow⟩ :=
    Finset.card_eq_two.mp ((extreme_fractional_degree_two hfreq hx).1 v hv)
  have he : e ∈ S v ∧ e ∈ fractional x := by
    exact Finset.mem_inter.mp (hrow ▸ Finset.mem_insert_self _ _)
  have hf : f ∈ S v ∧ f ∈ fractional x := by
    exact Finset.mem_inter.mp (hrow ▸ Finset.mem_insert_of_mem (Finset.mem_singleton_self _))
  obtain ⟨w,hvw,hew⟩ := extreme_other_endpoint hfreq hx he.2 hv he.1
  obtain ⟨u,hvu,hfu⟩ := extreme_other_endpoint hfreq hx hf.2 hv hf.1
  have hw : w ∈ active S lo hi x ∧ e ∈ S w := by
    exact Finset.mem_filter.mp (hew ▸ Finset.mem_insert_of_mem (Finset.mem_singleton_self _))
  have hu : u ∈ active S lo hi x ∧ f ∈ S u := by
    exact Finset.mem_filter.mp (hfu ▸ Finset.mem_insert_of_mem (Finset.mem_singleton_self _))
  have hwu : w ≠ u := by
    intro heq
    subst u
    exact hef (extreme_no_parallel_fractional hfreq hx he.2 hf.2 hvw hv hw.1
      he.1 hw.2 hf.1 hu.2)
  refine ⟨w,u,hwu,?_⟩
  ext t
  change (fractionalGraph S lo hi x).Adj v t ↔ t ∈ ({w,u} : Set V)
  constructor
  · rintro ⟨hne,_,ht,g,hg,hgv,hgt⟩
    have hgf : g = e ∨ g = f := by
      simpa only [hrow, Finset.mem_insert, Finset.mem_singleton] using
        (Finset.mem_inter.mpr ⟨hgv,hg⟩ : g ∈ S v ∩ fractional x)
    rcases hgf with hge | hgf
    · subst g
      have htw : t = v ∨ t = w := by
        simpa only [hew, Finset.mem_insert, Finset.mem_singleton] using
          (Finset.mem_filter.mpr ⟨ht,hgt⟩ : t ∈ (active S lo hi x).filter fun t => e ∈ S t)
      exact Or.inl (htw.resolve_left hne.symm)
    · subst g
      have htu : t = v ∨ t = u := by
        simpa only [hfu, Finset.mem_insert, Finset.mem_singleton] using
          (Finset.mem_filter.mpr ⟨ht,hgt⟩ : t ∈ (active S lo hi x).filter fun t => f ∈ S t)
      exact Or.inr (htu.resolve_left hne.symm)
  · rintro (rfl | rfl)
    · exact ⟨hvw,hv,hw.1,e,he.2,he.1,hw.2⟩
    · exact ⟨hvu,hv,hu.1,f,hf.2,hf.1,hu.2⟩

omit [DecidableEq V] in
/-- The graph obtained from the actual extreme point is a disjoint union of
simple cycles and isolated inactive rows. -/
theorem fractionalGraph_isCycles {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ) :
    (fractionalGraph S lo hi x).IsCycles := by
  classical
  intro v hn
  obtain ⟨w,hw⟩ := hn
  have hv : v ∈ active S lo hi x := hw.2.1
  obtain ⟨a,b,hab,hneighbors⟩ := fractionalGraph_neighbors hfreq hx hv
  simp [hneighbors, hab]

omit [DecidableEq V] in
/-- Every active row lies on a simple cycle spanning its whole connected
component, not merely on an assumed or externally supplied cycle. -/
theorem fractionalGraph_component_cycle {S : V → Finset E} {lo hi : V → ℤ}
    (hfreq : ∀ e, (Finset.univ.filter fun v => e ∈ S v).card ≤ 2)
    {x : E → ℝ} (hx : x ∈ (slab S lo hi).extremePoints ℝ)
    {v : V} (hv : v ∈ active S lo hi x)
    {c : (fractionalGraph S lo hi x).ConnectedComponent} (hvc : v ∈ c.supp) :
    ∃ p : (fractionalGraph S lo hi x).Walk v v,
      p.IsCycle ∧ p.toSubgraph.verts = c.supp := by
  classical
  obtain ⟨w,u,hwu,hn⟩ := fractionalGraph_neighbors hfreq hx hv
  exact (fractionalGraph_isCycles hfreq hx).exists_cycle_toSubgraph_verts_eq_connectedComponentSupp
    hvc (by rw [hn]; exact ⟨w, Or.inl rfl⟩)

end
end MultilinearGap.FrequencySlab
