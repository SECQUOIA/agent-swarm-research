import Formal.MultilinearGap.StructuralTreewidthGraph

/-! Actual cycle localization and coloring gluing across one shared vertex. -/

namespace MultilinearGap.TreewidthGraph

variable {V : Type*} {H K : SimpleGraph V} {s u v : V}

/-- The two pieces can meet along incident edges only at `s`. Isolated vertices
in the common ambient vertex type have no effect. -/
def MeetOnlyAt (H K : SimpleGraph V) (s : V) : Prop :=
  ∀ a b c, H.Adj a b → K.Adj b c → b = s

lemma MeetOnlyAt.symm (h : MeetOnlyAt H K s) : MeetOnlyAt K H s := by
  intro a b c hk hh
  exact h c b a hh.symm hk.symm

/-- Once a walk has entered the first piece, it stays there until it visits the
shared vertex. The endpoint is allowed to be that vertex. -/
lemma walk_stays_in_piece (hsep : MeetOnlyAt H K s)
    (p : (H ⊔ K).Walk u v) (havoid : s ∉ p.support.dropLast)
    (a : V) (ha : H.Adj a u) : ∀ e ∈ p.edges, e ∈ H.edgeSet := by
  induction p generalizing a with
  | nil => simp
  | @cons u b v hab q ih =>
    have hav : s ≠ u ∧ s ∉ q.support.dropLast := by
      simpa only [SimpleGraph.Walk.support_cons,
        List.dropLast_cons_of_ne_nil q.support_ne_nil, List.mem_cons, not_or] using havoid
    have hab' : H.Adj u b := by
      rcases hab with hh | hk
      · exact hh
      · exact (hav.1 (hsep a u b ha hk).symm).elim
    intro e he
    simp only [SimpleGraph.Walk.edges_cons, List.mem_cons] at he
    rcases he with rfl | he
    · exact hab'
    · exact ih hav.2 u hab' e he

lemma path_end_not_mem_dropLast (p : H.Walk u v) (hp : p.IsPath) :
    v ∉ p.support.dropLast := by
  have hn : (p.support.dropLast ++ [v]).Nodup := by
    rw [p.dropLast_support_concat]
    exact hp.support_nodup
  have hd := (List.nodup_append.mp hn).2.2
  have hd' : ∀ a ∈ p.support.dropLast, a ≠ v := by simpa using hd
  exact fun hv => hd' v hv rfl

/-- A cycle whose internal vertices avoid the articulation stays in one piece. -/
lemma cycle_edges_in_one_piece_of_avoid (hsep : MeetOnlyAt H K s)
    (p : (H ⊔ K).Walk u u) (hp : p.IsCycle)
    (havoid : s ∉ p.support.tail.dropLast) :
    (∀ e ∈ p.edges, e ∈ H.edgeSet) ∨ (∀ e ∈ p.edges, e ∈ K.edgeSet) := by
  cases p with
  | nil => exact (hp.ne_nil rfl).elim
  | @cons u b u hab q =>
    simp only [SimpleGraph.Walk.support_cons, List.tail_cons] at havoid
    rcases hab with hh | hk
    · left
      intro e he
      simp only [SimpleGraph.Walk.edges_cons, List.mem_cons] at he
      rcases he with rfl | he
      · exact hh
      · exact walk_stays_in_piece hsep q havoid u hh e he
    · right
      have hq : ∀ e ∈ q.edges, e ∈ K.edgeSet := by
        have heq : H ⊔ K = K ⊔ H := sup_comm H K
        let q' : (K ⊔ H).Walk b u := q.transfer (K ⊔ H) (by
          intro e he
          rw [← heq]
          exact q.edges_subset_edgeSet he)
        have hav' : s ∉ q'.support.dropLast := by
          simpa [q', SimpleGraph.Walk.support_transfer] using havoid
        have hh' := walk_stays_in_piece hsep.symm q' hav' u hk
        simpa [q', SimpleGraph.Walk.edges_transfer] using hh'
      intro e he
      simp only [SimpleGraph.Walk.edges_cons, List.mem_cons] at he
      rcases he with rfl | he
      · exact hk
      · exact hq e he

/-- Every simple cycle in the union of pieces meeting at one vertex lies wholly
in a single piece. This establishes the cycle step of series/block gluing. -/
theorem cycle_edges_in_one_piece (hsep : MeetOnlyAt H K s)
    (p : (H ⊔ K).Walk u u) (hp : p.IsCycle) :
    (∀ e ∈ p.edges, e ∈ H.edgeSet) ∨ (∀ e ∈ p.edges, e ∈ K.edgeSet) := by
  classical
  by_cases hs : s ∈ p.support
  · let q := p.rotate s hs
    have hq : q.IsCycle := hp.rotate hs
    have havoid : s ∉ q.support.tail.dropLast := by
      have ht := path_end_not_mem_dropLast q.tail hq.isPath_tail
      rwa [SimpleGraph.Walk.support_tail_of_not_nil q hq.not_nil] at ht
    have hlocal := cycle_edges_in_one_piece_of_avoid hsep q hq havoid
    have he : q.edges.Perm p.edges := (p.rotate_edges s hs).perm
    simpa only [he.mem_iff] using hlocal
  · apply cycle_edges_in_one_piece_of_avoid hsep p hp
    exact fun h => hs (List.mem_of_mem_tail (List.mem_of_mem_dropLast h))

/-- Good colorings glue when the same ambient coloring is good on both pieces.
Matching colorings on an articulation can be arranged by `good_swap`. -/
theorem good_union_at_vertex (hsep : MeetOnlyAt H K s)
    (factor color : V → Bool) (hH : Good factor color H) (hK : Good factor color K) :
    Good factor color (H ⊔ K) := by
  intro u p hp c hc
  rcases cycle_edges_in_one_piece hsep p hp with hh | hk
  · have hgood := hH u (p.transfer H hh) (hp.transfer hh) c
    have hm : Monochromatic factor color c (p.transfer H hh) := by
      simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hc
    simpa [cycleParity, SimpleGraph.Walk.support_transfer] using hgood hm
  · have hgood := hK u (p.transfer K hk) (hp.transfer hk) c
    have hm : Monochromatic factor color c (p.transfer K hk) := by
      simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hc
    simpa [cycleParity, SimpleGraph.Walk.support_transfer] using hgood hm

/-- General walk propagation through a vertex separator. -/
lemma walk_stays_in_piece_of_separator (P : V → Prop)
    (hsep : ∀ a b c, H.Adj a b → K.Adj b c → P b)
    (p : (H ⊔ K).Walk u v)
    (havoid : ∀ x ∈ p.support.dropLast, ¬ P x)
    (a : V) (ha : H.Adj a u) : ∀ e ∈ p.edges, e ∈ H.edgeSet := by
  induction p generalizing a with
  | nil => simp
  | @cons u b v hab q ih =>
    have hav : ¬ P u ∧ ∀ x ∈ q.support.dropLast, ¬ P x := by
      simpa only [SimpleGraph.Walk.support_cons,
        List.dropLast_cons_of_ne_nil q.support_ne_nil, List.mem_cons,
        forall_eq_or_imp] using havoid
    have hab' : H.Adj u b := by
      rcases hab with hh | hk
      · exact hh
      · exact (hav.1 (hsep a u b ha hk)).elim
    intro e he
    simp only [SimpleGraph.Walk.edges_cons, List.mem_cons] at he
    rcases he with rfl | he
    · exact hab'
    · exact ih hav.2 u hab' e he

/-- Edge-junction formulation of two graphs sharing only their terminals. -/
def MeetOnlyAtPair (H K : SimpleGraph V) (s t : V) : Prop :=
  ∀ a b c, H.Adj a b → K.Adj b c → b = s ∨ b = t

lemma MeetOnlyAtPair.symm {t : V} (h : MeetOnlyAtPair H K s t) :
    MeetOnlyAtPair K H s t := by
  intro a b c hk hh
  exact h c b a hh.symm hk.symm

/-- A walk with no internal separator vertex uses only one of the two pieces. -/
lemma walk_edges_in_one_piece_of_internal_avoid (P : V → Prop)
    (hsep : ∀ a b c, H.Adj a b → K.Adj b c → P b)
    (p : (H ⊔ K).Walk u v)
    (havoid : ∀ x ∈ p.support.tail.dropLast, ¬ P x) :
    (∀ e ∈ p.edges, e ∈ H.edgeSet) ∨ (∀ e ∈ p.edges, e ∈ K.edgeSet) := by
  cases p with
  | nil => exact Or.inl (by simp)
  | @cons u b v hab q =>
    simp only [SimpleGraph.Walk.support_cons, List.tail_cons] at havoid
    rcases hab with hh | hk
    · left
      intro e he
      simp only [SimpleGraph.Walk.edges_cons, List.mem_cons] at he
      rcases he with rfl | he
      · exact hh
      · exact walk_stays_in_piece_of_separator P hsep q havoid u hh e he
    · right
      let q' := q.transfer (K ⊔ H) (by
        intro e he
        rw [sup_comm K H]
        exact q.edges_subset_edgeSet he)
      have hav' : ∀ x ∈ q'.support.dropLast, ¬ P x := by
        simpa [q', SimpleGraph.Walk.support_transfer] using havoid
      have hh' := walk_stays_in_piece_of_separator P
        (fun a b c hk hh => hsep c b a hh.symm hk.symm) q' hav' u hk
      have hq : ∀ e ∈ q.edges, e ∈ K.edgeSet := by
        simpa [q', SimpleGraph.Walk.edges_transfer] using hh'
      intro e he
      simp only [SimpleGraph.Walk.edges_cons, List.mem_cons] at he
      rcases he with rfl | he
      · exact hk
      · exact hq e he

/-- Every simple terminal path of parallel pieces lies entirely in one child. -/
theorem parallel_path_edges_in_one_piece {t : V} (hsep : MeetOnlyAtPair H K s t)
    (p : (H ⊔ K).Walk s t) (hp : p.IsPath) :
    (∀ e ∈ p.edges, e ∈ H.edgeSet) ∨ (∀ e ∈ p.edges, e ∈ K.edgeSet) := by
  apply walk_edges_in_one_piece_of_internal_avoid (fun x => x = s ∨ x = t) hsep p
  intro x hx
  have hs : s ∉ p.support.tail := by
    have hn := hp.support_nodup
    rw [← p.cons_tail_support] at hn
    exact (List.nodup_cons.mp hn).1
  have ht := path_end_not_mem_dropLast p hp
  intro heq
  rcases heq with rfl | rfl
  · exact hs (List.mem_of_mem_dropLast hx)
  · exact ht (List.mem_of_mem_tail (by
      simpa only [List.tail_dropLast] using hx))

/-- Rotating a closed walk changes neither its factor parity nor its colors. -/
theorem cycleParity_rotate [DecidableEq V] (factor : V → Bool)
    (p : H.Walk u u) (x : V) (hx : x ∈ p.support) :
    cycleParity factor (p.rotate x hx) = cycleParity factor p := by
  exact ((p.support_rotate x hx).perm.map (factorWeight factor)).sum_eq

theorem monochromatic_rotate [DecidableEq V] (factor color : V → Bool) (c : Bool)
    (p : H.Walk u u) (x : V) (hx : x ∈ p.support) :
    Monochromatic factor color c (p.rotate x hx) ↔ Monochromatic factor color c p := by
  simp [Monochromatic]

/-- A parallel-union cycle missing one terminal lies in one child. -/
theorem parallel_cycle_edges_in_one_piece_of_missing {t : V}
    (hsep : MeetOnlyAtPair H K s t) (p : (H ⊔ K).Walk u u) (hp : p.IsCycle)
    (hs : s ∉ p.support) :
    (∀ e ∈ p.edges, e ∈ H.edgeSet) ∨ (∀ e ∈ p.edges, e ∈ K.edgeSet) := by
  classical
  by_cases ht : t ∈ p.support
  · let q := p.rotate t ht
    have hq : q.IsCycle := hp.rotate ht
    have hlocal : (∀ e ∈ q.edges, e ∈ H.edgeSet) ∨
        (∀ e ∈ q.edges, e ∈ K.edgeSet) := by
      apply walk_edges_in_one_piece_of_internal_avoid
        (fun x => x = s ∨ x = t) hsep q
      intro x hx heq
      rcases heq with rfl | rfl
      · apply hs
        have hm : x ∈ q.support :=
          List.mem_of_mem_tail (List.mem_of_mem_dropLast hx)
        simpa [q] using hm
      · have hn := path_end_not_mem_dropLast q.tail hq.isPath_tail
        apply hn
        rwa [SimpleGraph.Walk.support_tail_of_not_nil q hq.not_nil]
    have he : q.edges.Perm p.edges := (p.rotate_edges t ht).perm
    simpa only [he.mem_iff] using hlocal
  · apply walk_edges_in_one_piece_of_internal_avoid
      (fun x => x = s ∨ x = t) hsep p
    intro x hx heq
    have hm : x ∈ p.support := List.mem_of_mem_tail (List.mem_of_mem_dropLast hx)
    rcases heq with rfl | rfl
    · exact hs hm
    · exact ht hm

/-- Transfer the good-cycle property back along a cycle contained in a child. -/
lemma cycle_even_of_edges_in_piece {J : SimpleGraph V}
    (factor color : V → Bool) (hJ : Good factor color J)
    (p : H.Walk u u) (hp : p.IsCycle) (c : Bool)
    (hc : Monochromatic factor color c p)
    (he : ∀ e ∈ p.edges, e ∈ J.edgeSet) : cycleParity factor p = 0 := by
  have hm : Monochromatic factor color c (p.transfer J he) := by
    simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hc
  simpa [cycleParity, SimpleGraph.Walk.support_transfer] using
    hJ u (p.transfer J he) (hp.transfer he) c hm

/-- Parallel-cycle compatibility, expressed directly on actual simple paths. -/
def ParallelColorsCompatible (factor color : V → Bool)
    (H K : SimpleGraph V) (s t : V) : Prop :=
  ∀ (p : H.Walk s t) (q : K.Walk s t), p.IsPath → q.IsPath →
    ∀ c, Monochromatic factor color c p → Monochromatic factor color c q →
      pathParity factor p + pathParity factor q = factorWeight factor s + factorWeight factor t

/-- Good-coloring closure for parallel composition of actual graphs. -/
theorem good_union_at_pair {t : V} (hst : s ≠ t)
    (hsep : MeetOnlyAtPair H K s t)
    (factor color : V → Bool) (hH : Good factor color H) (hK : Good factor color K)
    (hcomp : ParallelColorsCompatible factor color H K s t) :
    Good factor color (H ⊔ K) := by
  classical
  intro u p hp c hc
  by_cases hs : s ∈ p.support
  · by_cases ht : t ∈ p.support
    · let q := p.rotate s hs
      have hq : q.IsCycle := hp.rotate hs
      have hqc : Monochromatic factor color c q := (monochromatic_rotate _ _ _ _ _ _).mpr hc
      have htq : t ∈ q.support := by simpa [q] using ht
      let a := q.takeUntil t htq
      let b := q.dropUntil t htq
      have hab : a.append b = q := q.take_spec htq
      have ha : a.IsPath := hq.isPath_takeUntil htq
      have hb : b.IsPath := by
        have habcycle : (a.append b).IsCycle := hab ▸ hq
        exact habcycle.isPath_of_append_right (SimpleGraph.Walk.not_nil_of_ne hst)
      have hm : Monochromatic factor color c a ∧ Monochromatic factor color c b := by
        rw [← monochromatic_append, hab]
        exact hqc
      have hl := parallel_path_edges_in_one_piece hsep a ha
      have hr := parallel_path_edges_in_one_piece hsep b.reverse hb.reverse
      have hbe : b.reverse.edges = b.edges.reverse := by simp
      simp only [hbe, List.mem_reverse] at hr
      suffices heven : cycleParity factor q = 0 by
        simpa [q, cycleParity_rotate] using heven
      rcases hl with haH | haK <;> rcases hr with hbH | hbK
      · apply cycle_even_of_edges_in_piece factor color hH q hq c hqc
        intro e he
        rw [← hab, SimpleGraph.Walk.edges_append, List.mem_append] at he
        exact he.elim (haH e) (hbH e)
      · have hpa := ha.transfer haH
        have hpb := (hb.transfer hbK).reverse
        have hma : Monochromatic factor color c (a.transfer H haH) := by
          simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hm.1
        have hmb : Monochromatic factor color c (b.transfer K hbK).reverse := by
          simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hm.2
        have heq := hcomp (a.transfer H haH) (b.transfer K hbK).reverse hpa hpb c hma hmb
        rw [pathParity_reverse] at heq
        simp only [pathParity, SimpleGraph.Walk.support_transfer] at heq
        rw [← hab, cycleParity_append]
        unfold pathParity
        linear_combination heq
      · have hpa := (hb.transfer hbH).reverse
        have hpb := ha.transfer haK
        have hma : Monochromatic factor color c (b.transfer H hbH).reverse := by
          simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hm.2
        have hmb : Monochromatic factor color c (a.transfer K haK) := by
          simpa [Monochromatic, SimpleGraph.Walk.support_transfer] using hm.1
        have heq := hcomp (b.transfer H hbH).reverse (a.transfer K haK) hpa hpb c hma hmb
        rw [pathParity_reverse] at heq
        simp only [pathParity, SimpleGraph.Walk.support_transfer] at heq
        rw [← hab, cycleParity_append]
        unfold pathParity
        linear_combination heq
      · apply cycle_even_of_edges_in_piece factor color hK q hq c hqc
        intro e he
        rw [← hab, SimpleGraph.Walk.edges_append, List.mem_append] at he
        exact he.elim (haK e) (hbK e)
    · have hsep' : MeetOnlyAtPair H K t s := fun a b c hh hk => (hsep a b c hh hk).symm
      rcases parallel_cycle_edges_in_one_piece_of_missing hsep' p hp ht with he | he
      · exact cycle_even_of_edges_in_piece factor color hH p hp c hc he
      · exact cycle_even_of_edges_in_piece factor color hK p hp c hc he
  · rcases parallel_cycle_edges_in_one_piece_of_missing hsep p hp hs with he | he
    · exact cycle_even_of_edges_in_piece factor color hH p hp c hc he
    · exact cycle_even_of_edges_in_piece factor color hK p hp c hc he

/-- A nonempty walk cannot lie in a graph where its start is isolated. -/
lemma not_edges_in_piece_of_start_isolated {J : SimpleGraph V}
    (p : J.Walk u v) (huv : u ≠ v) (hiso : ∀ x, ¬ H.Adj u x) :
    ¬ (∀ e ∈ p.edges, e ∈ H.edgeSet) := by
  cases p with
  | nil => exact (huv rfl).elim
  | @cons u w v huw q =>
    intro he
    exact hiso w (he s(u, w) (by simp))

/-- A simple terminal path through series pieces splits at their common vertex.
The two returned ambient walks transfer directly to the respective child graphs. -/
theorem series_path_decomposition {m t : V}
    (hsep : MeetOnlyAt H K m) (hst : s ≠ t) (hsm : s ≠ m) (hmt : m ≠ t)
    (hs : ∀ x, ¬ K.Adj s x) (ht : ∀ x, ¬ H.Adj t x)
    (p : (H ⊔ K).Walk s t) (hp : p.IsPath) :
    ∃ (a : (H ⊔ K).Walk s m) (b : (H ⊔ K).Walk m t),
      a.IsPath ∧ b.IsPath ∧ (∀ e ∈ a.edges, e ∈ H.edgeSet) ∧
        (∀ e ∈ b.edges, e ∈ K.edgeSet) ∧ a.append b = p := by
  classical
  have hm : m ∈ p.support := by
    by_contra hm
    have hlocal := walk_edges_in_one_piece_of_internal_avoid
      (fun x => x = m) hsep p (by
        intro x hx hxm
        subst x
        exact hm (List.mem_of_mem_tail (List.mem_of_mem_dropLast hx)))
    rcases hlocal with he | he
    · apply not_edges_in_piece_of_start_isolated p.reverse hst.symm ht
      simpa using he
    · exact not_edges_in_piece_of_start_isolated p hst hs he
  let a := p.takeUntil m hm
  let b := p.dropUntil m hm
  have ha : a.IsPath := hp.takeUntil hm
  have hb : b.IsPath := hp.dropUntil hm
  have hab : a.append b = p := p.take_spec hm
  have haH : ∀ e ∈ a.edges, e ∈ H.edgeSet := by
    have hlocal := walk_edges_in_one_piece_of_internal_avoid
      (fun x => x = m) hsep a (by
        intro x hx hxm
        subst x
        exact path_end_not_mem_dropLast a ha
          (List.mem_of_mem_tail (by simpa only [List.tail_dropLast] using hx)))
    rcases hlocal with he | he
    · exact he
    · exact (not_edges_in_piece_of_start_isolated a hsm hs he).elim
  have hbK : ∀ e ∈ b.edges, e ∈ K.edgeSet := by
    have hlocal := walk_edges_in_one_piece_of_internal_avoid
      (fun x => x = m) hsep b.reverse (by
        intro x hx hxm
        subst x
        exact path_end_not_mem_dropLast b.reverse hb.reverse
          (List.mem_of_mem_tail (by simpa only [List.tail_dropLast] using hx)))
    rcases hlocal with he | he
    · exact (not_edges_in_piece_of_start_isolated b.reverse hmt.symm ht he).elim
    · simpa using he
  exact ⟨a, b, ha, hb, haH, hbK, hab⟩

/-- Every vertex of a nonempty walk is incident with one of its graph edges. -/
lemma exists_adj_of_mem_support {J : SimpleGraph V} {x : V}
    (p : J.Walk u v) (hn : ¬ p.Nil) (hx : x ∈ p.support) : ∃ y, J.Adj x y := by
  obtain ⟨e, he, hx⟩ := (SimpleGraph.Walk.mem_support_iff_exists_mem_edges_of_not_nil hn).mp hx
  have hj := p.edges_subset_edgeSet he
  induction e using Sym2.inductionOn with
  | hf a b =>
    simp only [Sym2.mem_iff] at hx
    rcases hx with rfl | rfl
    · exact ⟨b, hj⟩
    · exact ⟨a, hj.symm⟩

/-- Simple paths in pieces meeting at an articulation concatenate to a simple path. -/
theorem series_append_isPath {m t : V} (hsep : MeetOnlyAt H K m)
    (p : H.Walk s m) (q : K.Walk m t) (hp : p.IsPath) (hq : q.IsPath)
    (hsm : s ≠ m) (hmt : m ≠ t) :
    ((p.mapLe (show H ≤ H ⊔ K from le_sup_left)).append
      (q.mapLe (show K ≤ H ⊔ K from le_sup_right))).IsPath := by
  rw [SimpleGraph.Walk.isPath_def, SimpleGraph.Walk.support_append]
  simp only [SimpleGraph.Walk.support_mapLe_eq_support]
  refine List.nodup_append.mpr ⟨hp.support_nodup, hq.support_nodup.tail, ?_⟩
  intro x hx y hy hxy
  subst y
  obtain ⟨a, ha⟩ := exists_adj_of_mem_support p (SimpleGraph.Walk.not_nil_of_ne hsm) hx
  obtain ⟨b, hb⟩ := exists_adj_of_mem_support q (SimpleGraph.Walk.not_nil_of_ne hmt)
    (List.mem_of_mem_tail hy)
  have hxm : x = m := hsep a x b ha.symm hb
  have hn := hq.support_nodup
  rw [← q.cons_tail_support] at hn
  exact (List.nodup_cons.mp hn).1 (hxm ▸ hy)

end MultilinearGap.TreewidthGraph
