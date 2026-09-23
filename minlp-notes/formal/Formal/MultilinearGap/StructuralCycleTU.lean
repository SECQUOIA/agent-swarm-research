import Formal.MultilinearGap.StructuralTreewidthGraph
import Formal.MultilinearGap.StructuralTreewidthDecomposition
import Formal.MultilinearGap.StructuralCycleParity
import Formal.MultilinearGap.StructuralEvenCycleColoring
import Formal.MultilinearGap.StructuralCamion

/-!
# Total unimodularity from even incidence cycles

Within each column support, pair the selected rows, leaving at most one row
unpaired. A proper two-coloring of the graph of these pairs gives row signs
whose sum in every column is zero, one, or minus one.

Every trail of the pair graph lifts to an incidence trail, with one row vertex
per paired edge. When all simple incidence cycles have even row counts, closed
incidence trails do too. Thus the pair graph has only even cycles and admits
the required two-coloring. Applying the proved Ghouila-Houri signing criterion
to every finite row selection yields total unimodularity.
-/

namespace MultilinearGap.CycleTU

noncomputable section

/-- An involution pairs the elements of a finite set, with at most one fixed
point in that set. Outside the set its values are irrelevant. -/
structure Pairing {R : Type*} (s : Finset R) where
  mate : R → R
  involutive : Function.Involutive mate
  mem : ∀ r ∈ s, mate r ∈ s
  fixed_unique : ∀ r ∈ s, ∀ t ∈ s, mate r = r → mate t = t → r = t

private def indexMate (n i : ℕ) : ℕ :=
  if i % 2 = 0 then if i + 1 < n then i + 1 else i else i - 1

private lemma indexMate_lt {n i : ℕ} (hi : i < n) : indexMate n i < n := by
  unfold indexMate
  split_ifs <;> omega

private lemma indexMate_involutive {n i : ℕ} (hi : i < n) :
    indexMate n (indexMate n i) = i := by
  unfold indexMate
  split <;> split_ifs <;> omega

private lemma indexMate_fixed_unique {n i j : ℕ} (hi : i < n) (hj : j < n)
    (hfi : indexMate n i = i) (hfj : indexMate n j = j) : i = j := by
  unfold indexMate at hfi hfj
  split_ifs at hfi hfj <;> omega

/-- Every finite set can be paired with at most one leftover element. -/
theorem exists_pairing {R : Type*} (s : Finset R) : Nonempty (Pairing s) := by
  classical
  let e := Fintype.equivFin s
  let f : s → s := fun r => e.symm ⟨indexMate s.card (e r).val,
    by simpa using indexMate_lt (e r).isLt⟩
  have hf : Function.Involutive f := by
    intro r
    apply e.injective
    apply Fin.ext
    simp only [f, Equiv.apply_symm_apply]
    exact indexMate_involutive (by simpa using (e r).isLt)
  let mate : R → R := fun r => if hr : r ∈ s then (f ⟨r, hr⟩).val else r
  refine ⟨⟨mate, ?_, ?_, ?_⟩⟩
  · intro r
    by_cases hr : r ∈ s
    · simp only [mate, dif_pos hr]
      rw [dif_pos (f ⟨r, hr⟩).property]
      exact congrArg Subtype.val (hf ⟨r, hr⟩)
    · simp [mate, hr]
  · intro r hr
    simp [mate, hr]
  · intro r hr t ht hfr hft
    have hri : indexMate s.card (e ⟨r, hr⟩).val = (e ⟨r, hr⟩).val := by
      have hh : f ⟨r, hr⟩ = ⟨r, hr⟩ := Subtype.ext (by simpa [mate, hr] using hfr)
      simpa [f] using congrArg (fun z => (e z).val) hh
    have hti : indexMate s.card (e ⟨t, ht⟩).val = (e ⟨t, ht⟩).val := by
      have hh : f ⟨t, ht⟩ = ⟨t, ht⟩ := Subtype.ext (by simpa [mate, ht] using hft)
      simpa [f] using congrArg (fun z => (e z).val) hh
    exact congrArg Subtype.val (e.injective (Fin.ext (indexMate_fixed_unique
      (by simpa using (e ⟨r, hr⟩).isLt) (by simpa using (e ⟨t, ht⟩).isLt) hri hti)))

/-- The graph obtained by drawing every pair from every column. -/
def pairGraph {R C : Type*} (s : C → Finset R) (p : ∀ c, Pairing (s c)) :
    SimpleGraph R where
  Adj r t := r ≠ t ∧ ∃ c, r ∈ s c ∧ (p c).mate r = t
  symm := ⟨by
    rintro r t ⟨hne, c, hr, rfl⟩
    exact ⟨hne.symm, c, (p c).mem r hr, (p c).involutive r⟩⟩
  loopless := ⟨by simp⟩

/-- A Boolean color encodes one of the two integer signs. -/
def sign (b : Bool) : ℤ := if b then 1 else -1

@[simp] lemma sign_ne_zero (b : Bool) : sign b ≠ 0 := by cases b <;> decide

lemma sign_add_eq_zero {a b : Bool} (h : a ≠ b) : sign a + sign b = 0 := by
  cases a <;> cases b <;> simp_all [sign]

/-- Opposite colors on every pair cancel, leaving at most one sign. -/
theorem pairing_signed_sum {R : Type*} {s : Finset R}
    (p : Pairing s) (color : R → Bool)
    (hc : ∀ r ∈ s, p.mate r ≠ r → color r ≠ color (p.mate r)) :
    (∑ r ∈ s, sign (color r)) ∈ ({-1, 0, 1} : Finset ℤ) := by
  classical
  let fixed := s.filter fun r => p.mate r = r
  let paired := s.filter fun r => p.mate r ≠ r
  have hz : ∑ r ∈ paired, sign (color r) = 0 := by
    apply Finset.sum_involution (fun r _ => p.mate r)
    · intro r hr
      have hr' := Finset.mem_filter.mp hr
      exact sign_add_eq_zero (hc r hr'.1 hr'.2)
    · intro r hr _ he
      exact (Finset.mem_filter.mp hr).2 he
    · intro r hr
      have hr' := Finset.mem_filter.mp hr
      exact Finset.mem_filter.mpr ⟨p.mem r hr'.1, by
        rw [p.involutive]
        exact hr'.2.symm⟩
    · intro r _
      exact p.involutive r
  have hsum : (∑ r ∈ s, sign (color r)) = ∑ r ∈ fixed, sign (color r) := by
    have he := Finset.sum_filter_add_sum_filter_not s (fun r => p.mate r = r)
      (fun r => sign (color r))
    change (∑ r ∈ fixed, sign (color r)) + (∑ r ∈ paired, sign (color r)) = _ at he
    simpa [hz] using he.symm
  rw [hsum]
  by_cases he : fixed.Nonempty
  · obtain ⟨r, hr⟩ := he
    have hf : fixed = {r} := by
      apply Finset.eq_singleton_iff_unique_mem.mpr
      refine ⟨hr, fun t ht => ?_⟩
      exact p.fixed_unique t (Finset.mem_filter.mp ht).1 r
        (Finset.mem_filter.mp hr).1 (Finset.mem_filter.mp ht).2
        (Finset.mem_filter.mp hr).2
    rw [hf]
    cases hh : color r <;> simp [sign, hh]
  · rw [Finset.not_nonempty_iff_eq_empty.mp he]
    simp

/-- A proper coloring of the pair graph simultaneously balances all columns. -/
theorem pairGraph_signed_sums {R C : Type*}
    (s : C → Finset R) (p : ∀ c, Pairing (s c)) (color : R → Bool)
    (hc : ∀ r t, (pairGraph s p).Adj r t → color r ≠ color t) :
    ∀ c, (∑ r ∈ s c, sign (color r)) ∈ ({-1, 0, 1} : Finset ℤ) := by
  intro c
  apply pairing_signed_sum (p c) color
  intro r hr hne
  exact hc r ((p c).mate r) ⟨hne.symm, c, hr, rfl⟩


section Lifting

variable {R C : Type*} (s : C → Finset R) (p : ∀ c, Pairing (s c))

/-- The incidence graph underlying the paired-row graph. -/
abbrev supportGraph : SimpleGraph (R ⊕ C) :=
  StructuralTreewidth.incidenceGraph (fun r c => r ∈ s c)

private def edgeColumn {r t : R} (h : (pairGraph s p).Adj r t) : C :=
  Classical.choose h.2

private lemma edgeColumn_mem {r t : R} (h : (pairGraph s p).Adj r t) :
    r ∈ s (edgeColumn s p h) := (Classical.choose_spec h.2).1

private lemma edgeColumn_mate {r t : R} (h : (pairGraph s p).Adj r t) :
    (p (edgeColumn s p h)).mate r = t := (Classical.choose_spec h.2).2

/-- Replace each paired-row edge by its two incidence edges. -/
def lift {r t : R} : (pairGraph s p).Walk r t →
    (supportGraph s).Walk (.inl r) (.inl t)
  | .nil => .nil
  | .cons h q => .cons (v := Sum.inr (edgeColumn s p h)) (edgeColumn_mem s p h)
      (.cons (by
        change _ ∈ s (edgeColumn s p h)
        simpa only [edgeColumn_mate s p h] using
          (p _).mem _ (edgeColumn_mem s p h)) (lift q))

/-- An incidence edge uniquely determines its original paired-row edge. -/
lemma lift_edge_origin {a b r : R} {c : C} (q : (pairGraph s p).Walk a b)
    (h : s(Sum.inl r, Sum.inr c) ∈ (lift s p q).edges) :
    s(r, (p c).mate r) ∈ q.edges := by
  induction q with
  | nil => simp [lift] at h
  | @cons a t b hadj q ih =>
    change s(Sum.inl r, Sum.inr c) ∈
      s(Sum.inl a, Sum.inr (edgeColumn s p hadj)) ::
      s(Sum.inr (edgeColumn s p hadj), Sum.inl t) :: (lift s p q).edges at h
    simp only [List.mem_cons] at h
    rcases h with h | h | h
    · have hh := Sym2.eq_iff.mp h
      simp only [Sum.inl.injEq, Sum.inr.injEq, Sum.inl_ne_inr,
        Sum.inr_ne_inl, and_false, or_false] at hh
      rcases hh with ⟨rfl, rfl⟩
      simp [edgeColumn_mate]
    · have hh := Sym2.eq_iff.mp h
      simp only [Sum.inl.injEq, Sum.inr.injEq, Sum.inl_ne_inr,
        Sum.inr_ne_inl, false_and, false_or] at hh
      rcases hh with ⟨rfl, rfl⟩
      have hm : (p (edgeColumn s p hadj)).mate r = a := by
        have he := (p (edgeColumn s p hadj)).involutive a
        simpa only [edgeColumn_mate s p hadj] using he
      simp [hm, Sym2.eq_swap]
    · exact List.mem_cons_of_mem _ (ih h)

/-- Distinct paired edges have disjoint incidence edges, so a trail lifts to
an actual incidence trail even when column vertices repeat. -/
theorem lift_isTrail {a b : R} (q : (pairGraph s p).Walk a b) (hq : q.IsTrail) :
    (lift s p q).IsTrail := by
  induction q with
  | nil => simp [lift]
  | @cons a t b hadj q ih =>
    obtain ⟨ht, hne⟩ := (SimpleGraph.Walk.isTrail_cons _ _).mp hq
    change (SimpleGraph.Walk.cons _ (SimpleGraph.Walk.cons _ (lift s p q))).IsTrail
    apply SimpleGraph.Walk.IsTrail.cons
    · apply SimpleGraph.Walk.IsTrail.cons (ih ht)
      intro he
      have he' : s(Sum.inl t, Sum.inr (edgeColumn s p hadj)) ∈ (lift s p q).edges := by
        simpa only [Sym2.eq_swap] using he
      have hh := lift_edge_origin s p q he'
      have hm : (p (edgeColumn s p hadj)).mate t = a := by
        have he := (p (edgeColumn s p hadj)).involutive a
        simpa only [edgeColumn_mate s p hadj] using he
      rw [hm] at hh
      exact hne (by simpa only [Sym2.eq_swap] using hh)
    · change s(Sum.inl a, Sum.inr (edgeColumn s p hadj)) ∉
        s(Sum.inr (edgeColumn s p hadj), Sum.inl t) :: (lift s p q).edges
      simp only [List.mem_cons, not_or]
      constructor
      · intro he
        have hh := Sym2.eq_iff.mp he
        simp only [Sum.inl_ne_inr, false_and, Sum.inl.injEq,
          and_true, false_or] at hh
        exact hadj.1 hh
      · intro he
        have hh := lift_edge_origin s p q he
        rw [edgeColumn_mate s p hadj] at hh
        exact hne hh

/-- Mark the row side of the incidence graph. -/
def rowFactor : R ⊕ C → Bool := Sum.elim (fun _ => true) (fun _ => false)

lemma lift_pathParity {a b : R} (q : (pairGraph s p).Walk a b) :
    TreewidthGraph.pathParity rowFactor (lift s p q) = (q.length : ZMod 2) + 1 := by
  induction q with
  | nil => simp [lift, TreewidthGraph.pathParity, TreewidthGraph.factorWeight, rowFactor]
  | @cons a t b h q ih =>
    change 1 + (0 + TreewidthGraph.pathParity rowFactor (lift s p q)) =
      ((q.length + 1 : ℕ) : ZMod 2) + 1
    rw [ih]
    push_cast
    ring

/-- Each lifted paired edge contributes one row vertex to closed-walk parity. -/
theorem lift_cycleParity {a : R} (q : (pairGraph s p).Walk a a) :
    TreewidthGraph.cycleParity rowFactor (lift s p q) = (q.length : ZMod 2) := by
  have hh := TreewidthGraph.pathParity_eq_start_add_tail rowFactor (lift s p q)
  rw [lift_pathParity] at hh
  change (q.length : ZMod 2) + 1 = 1 + TreewidthGraph.cycleParity rowFactor (lift s p q) at hh
  linear_combination -hh

end Lifting


/-- Even row counts on incidence cycles force even lengths on paired cycles. -/
theorem pairGraph_even_cycles {R C : Type*} (s : C → Finset R)
    (p : ∀ c, Pairing (s c))
    (heven : ∀ v (q : (supportGraph s).Walk v v), q.IsCycle →
      TreewidthGraph.cycleParity rowFactor q = 0) :
    ∀ r (q : (pairGraph s p).Walk r r), q.IsCycle → Even q.length := by
  intro r q hq
  have hh := TreewidthGraph.cycleParity_eq_zero_of_isTrail rowFactor heven
    (lift s p q) (lift_isTrail s p q hq.isTrail)
  rw [lift_cycleParity] at hh
  exact ZMod.natCast_eq_zero_iff_even.mp hh

/-- The incidence-cycle hypothesis constructs the signing, including the
choice of pairings and the proper coloring of their graph. -/
theorem exists_balancing_colors {R C : Type*}
    (s : C → Finset R)
    (heven : ∀ v (q : (supportGraph s).Walk v v), q.IsCycle →
      TreewidthGraph.cycleParity rowFactor q = 0) :
    ∃ color : R → Bool, ∀ c,
      (∑ r ∈ s c, sign (color r)) ∈ ({-1, 0, 1} : Finset ℤ) := by
  let p : ∀ c, Pairing (s c) := fun c => Classical.choice (exists_pairing (s c))
  obtain ⟨color, hc⟩ := StructuralEvenCycle.exists_bool_coloring (pairGraph s p)
    (pairGraph_even_cycles s p heven)
  exact ⟨color, pairGraph_signed_sums s p color (fun _ _ h => hc h)⟩

/-- The bipartite support of a zero-one matrix, with rows on the left. -/
abbrev matrixGraph {R C : Type*} (A : Matrix R C ℤ) : SimpleGraph (R ⊕ C) :=
  StructuralTreewidth.incidenceGraph (fun r c => A r c = 1)

/-- The cycle condition supplies signs for every finite row selection. -/
theorem transpose_columnSigning {R C : Type*} (A : Matrix R C ℤ)
    (h01 : ∀ r c, A r c = 0 ∨ A r c = 1)
    (heven : ∀ v (q : (matrixGraph A).Walk v v), q.IsCycle →
      TreewidthGraph.cycleParity rowFactor q = 0) :
    ColumnSigning A.transpose := by
  classical
  intro k g hg
  let s : C → Finset (Fin k) := fun c => Finset.univ.filter fun j => A (g j) c = 1
  let f : supportGraph s →g matrixGraph A := {
    toFun := Sum.map g id
    map_rel' := by
      intro u v h
      cases u <;> cases v <;> simp_all [supportGraph,
        StructuralTreewidth.incidenceGraph, s] }
  have hf : Function.Injective f := Sum.map_injective.mpr ⟨hg, Function.injective_id⟩
  have hpar : ∀ v (q : (supportGraph s).Walk v v), q.IsCycle →
      TreewidthGraph.cycleParity rowFactor q = 0 := by
    intro v q hq
    have hh := heven (f v) (q.map f) (hq.map hf)
    rw [TreewidthGraph.cycleParity_map] at hh
    have hfac : rowFactor ∘ f = rowFactor := by funext x; cases x <;> rfl
    rwa [hfac] at hh
  obtain ⟨color, hc⟩ := exists_balancing_colors s hpar
  refine ⟨fun j => sign (color j), ?_, ?_⟩
  · intro j
    cases color j <;> simp [sign]
  · intro c
    have hs : (∑ j, A.transpose c (g j) * sign (color j)) =
        ∑ j ∈ s c, sign (color j) := by
      rw [Finset.sum_filter]
      apply Finset.sum_congr rfl
      intro j _
      rcases h01 (g j) c with h | h <;> simp [Matrix.transpose_apply, h]
    rw [hs]
    have hh := hc c
    simp only [Finset.mem_insert, Finset.mem_singleton] at hh
    rcases hh with hh | hh | hh
    · exact ⟨-1, by simpa using hh.symm⟩
    · exact ⟨0, by simpa using hh.symm⟩
    · exact ⟨1, by simpa using hh.symm⟩

/-- A zero-one matrix is totally unimodular when every simple support cycle
contains an even number of row vertices (equivalently length divisible by four).
This derives all finite minor bounds; no determinant criterion is assumed. -/
theorem totallyUnimodular_of_even_cycles {R C : Type*} (A : Matrix R C ℤ)
    (h01 : ∀ r c, A r c = 0 ∨ A r c = 1)
    (heven : ∀ v (q : (matrixGraph A).Walk v v), q.IsCycle →
      TreewidthGraph.cycleParity rowFactor q = 0) :
    A.IsTotallyUnimodular := by
  have hh := (transpose_columnSigning A h01 heven).totallyUnimodular.transpose
  simpa using hh


/-- The same criterion in the repository's incidence convention: variables
are on the left and the factors indexing matrix rows are on the right. -/
theorem totallyUnimodular_of_even_factor_cycles {R C : Type*} (A : Matrix R C ℤ)
    (h01 : ∀ r c, A r c = 0 ∨ A r c = 1)
    (heven : ∀ v (q : (StructuralTreewidth.incidenceGraph
        (fun c r => A r c = 1)).Walk v v), q.IsCycle →
      TreewidthGraph.cycleParity (Sum.elim (fun _ => false) (fun _ => true)) q = 0) :
    A.IsTotallyUnimodular := by
  apply totallyUnimodular_of_even_cycles A h01
  let f : matrixGraph A →g StructuralTreewidth.incidenceGraph (fun c r => A r c = 1) := {
    toFun := Sum.swap
    map_rel' := by intro v w h; cases v <;> cases w <;> exact h }
  have hf : Function.Injective f := by
    intro x y h
    have hh := congrArg Sum.swap h
    change Sum.swap (Sum.swap x) = Sum.swap (Sum.swap y) at hh
    simpa only [Sum.swap_swap] using hh
  intro v q hq
  have hh := heven (f v) (q.map f) (hq.map hf)
  rw [TreewidthGraph.cycleParity_map] at hh
  have hfac : (Sum.elim (fun _ : C => false) (fun _ : R => true)) ∘ f = rowFactor := by
    funext x
    cases x <;> rfl
  rwa [hfac] at hh

end
end MultilinearGap.CycleTU
