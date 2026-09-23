import Formal.DAGSpectral.GraphInput

namespace DAGSpectral
variable {v m : ℕ}

/-- Raw edge incidence before a topological ordering has been found. -/
def rawRelation (src dst : Fin m → Fin v) (a b : Fin v) : Prop :=
  ∃ e, src e = a ∧ dst e = b

def RawAcyclic (src dst : Fin m → Fin v) : Prop :=
  ∀ x, ¬ Relation.TransGen (rawRelation src dst) x x

theorem rawAcyclic_of_rank (src dst : Fin m → Fin v) (rank : Fin v → ℕ)
    (h : ∀ e, rank (src e) < rank (dst e)) : RawAcyclic src dst := by
  have ht {a b : Fin v} (hp : Relation.TransGen (rawRelation src dst) a b) :
      rank a < rank b := by
    induction hp with
    | single he =>
      obtain ⟨e,rfl,rfl⟩ := he
      exact h e
    | tail hp he ih =>
      obtain ⟨e,he0,he1⟩ := he
      exact ih.trans (he0 ▸ he1 ▸ h e)
  intro x hx
  exact (lt_irrefl _) (ht hx)

/-- All remaining vertices without an incoming edge from the remaining set. -/
def readyVertices (src dst : Fin m → Fin v) (remaining : Finset (Fin v)) : Finset (Fin v) :=
  remaining.filter (fun x => ∀ e, dst e = x → src e ∉ remaining)

theorem readyVertices_nonempty (src dst : Fin m → Fin v) (ha : RawAcyclic src dst)
    (remaining : Finset (Fin v)) (hne : remaining.Nonempty) :
    (readyVertices src dst remaining).Nonempty := by
  let rel := Relation.TransGen (rawRelation src dst)
  let : IsTrans (Fin v) rel := ⟨fun _ _ _ hab hbc => hab.trans hbc⟩
  let : Std.Irrefl rel := ⟨ha⟩
  have hw := Finite.wellFounded_of_trans_of_irrefl rel
  obtain ⟨x,hx,hmin⟩ := hw.has_min (remaining : Set (Fin v)) hne
  refine ⟨x, Finset.mem_filter.mpr ⟨hx, ?_⟩⟩
  intro e he hsrc
  exact hmin (src e) hsrc (.single ⟨e,rfl,he⟩)

/-- Kahn's algorithm, choosing the least available vertex at each step.
The finite minimum and every incoming-edge test are computable. -/
def kahnOrder (src dst : Fin m → Fin v) : ℕ → Finset (Fin v) → List (Fin v)
  | 0, _ => []
  | n+1, remaining =>
    if h : (readyVertices src dst remaining).Nonempty then
      let x := (readyVertices src dst remaining).min' h
      x :: kahnOrder src dst n (remaining.erase x)
    else []

/-- Coverage, no repetitions, and correct edge order for the actual computed list. -/
theorem kahnOrder_spec (src dst : Fin m → Fin v) (ha : RawAcyclic src dst)
    (n : ℕ) (remaining : Finset (Fin v)) (hsize : remaining.card ≤ n) :
    (kahnOrder src dst n remaining).Nodup ∧
    (kahnOrder src dst n remaining).toFinset = remaining ∧
    ∀ e, src e ∈ remaining → dst e ∈ remaining →
      (kahnOrder src dst n remaining).idxOf (src e) <
        (kahnOrder src dst n remaining).idxOf (dst e) := by
  induction n generalizing remaining with
  | zero =>
    have he : remaining = ∅ := Finset.card_eq_zero.mp (by omega)
    subst remaining
    simp [kahnOrder]
  | succ n ih =>
    by_cases hne : remaining.Nonempty
    · have hr := readyVertices_nonempty src dst ha remaining hne
      let x := (readyVertices src dst remaining).min' hr
      have hxready : x ∈ readyVertices src dst remaining := Finset.min'_mem _ _
      obtain ⟨hx,hno⟩ := Finset.mem_filter.mp hxready
      have hc : (remaining.erase x).card ≤ n := by
        rw [Finset.card_erase_of_mem hx]
        omega
      obtain ⟨hnod,hcover,hforward⟩ := ih (remaining.erase x) hc
      have hrun : kahnOrder src dst (n+1) remaining =
          x :: kahnOrder src dst n (remaining.erase x) := by
        simp only [kahnOrder, hr, reduceDIte, x]
      rw [hrun]
      refine ⟨List.nodup_cons.mpr ⟨?_,hnod⟩, ?_, ?_⟩
      · intro hmem
        have hm := List.mem_toFinset.mpr hmem
        rw [hcover] at hm
        exact (Finset.mem_erase.mp hm).1 rfl
      · simp only [List.toFinset_cons, hcover, Finset.insert_erase hx]
      · intro e hs hd
        have hdx : x ≠ dst e := by intro he; exact hno e he.symm hs
        by_cases hsx : x = src e
        · have hsd : src e ≠ dst e := by simpa only [hsx] using hdx
          simp [hsx, hsd]
        · have hh := hforward e (Finset.mem_erase.mpr ⟨Ne.symm hsx,hs⟩)
            (Finset.mem_erase.mpr ⟨Ne.symm hdx,hd⟩)
          simpa [List.idxOf_cons, hsx, hdx] using hh
    · have he : remaining = ∅ := Finset.not_nonempty_iff_eq_empty.mp hne
      subst remaining
      simp [kahnOrder, readyVertices]

/-- A raw acyclic graph's actual computed topological list. -/
def topologicalList (src dst : Fin m → Fin v) : List (Fin v) :=
  kahnOrder src dst v Finset.univ

theorem topologicalList_nodup (src dst : Fin m → Fin v) (ha : RawAcyclic src dst) :
    (topologicalList src dst).Nodup :=
  (kahnOrder_spec src dst ha v Finset.univ (by simp)).1

theorem topologicalList_mem (src dst : Fin m → Fin v) (ha : RawAcyclic src dst)
    (x : Fin v) : x ∈ topologicalList src dst := by
  apply List.mem_toFinset.mp
  change _ ∈ (kahnOrder src dst v Finset.univ).toFinset
  rw [(kahnOrder_spec src dst ha v Finset.univ (by simp)).2.1]
  exact Finset.mem_univ x

theorem topologicalList_length (src dst : Fin m → Fin v) (ha : RawAcyclic src dst) :
    (topologicalList src dst).length = v := by
  rw [← List.toFinset_card_of_nodup (topologicalList_nodup src dst ha)]
  change (kahnOrder src dst v Finset.univ).toFinset.card = v
  rw [(kahnOrder_spec src dst ha v Finset.univ (by simp)).2.1]
  exact Finset.card_fin v

/-- Computable vertex-to-position permutation, with the list lookup as its
explicit inverse. No noncomputable choice of an ordering or inverse is used. -/
def topologicalOrder (src dst : Fin m → Fin v) (ha : RawAcyclic src dst) :
    Equiv.Perm (Fin v) where
  toFun x := ⟨(topologicalList src dst).idxOf x, by
    exact lt_of_lt_of_eq (List.idxOf_lt_length_iff.mpr (topologicalList_mem src dst ha x))
      (topologicalList_length src dst ha)⟩
  invFun i := (topologicalList src dst).get ⟨i.val, by
    simpa only [topologicalList_length src dst ha] using i.isLt⟩
  left_inv x := List.idxOf_get _
  right_inv i := by
    apply Fin.ext
    exact List.get_idxOf (topologicalList_nodup src dst ha) _

theorem topologicalOrder_forward (src dst : Fin m → Fin v) (ha : RawAcyclic src dst)
    (e : Fin m) : topologicalOrder src dst ha (src e) < topologicalOrder src dst ha (dst e) :=
  (kahnOrder_spec src dst ha v Finset.univ (by simp)).2.2 e (by simp) (by simp)

theorem checkDAGWithTopologicalOrder (src dst : Fin m → Fin v) (ha : RawAcyclic src dst) :
    checkDAGWithOrder src dst (topologicalOrder src dst ha) =
      some ⟨(topologicalOrder src dst ha) ∘ src, (topologicalOrder src dst ha) ∘ dst,
        topologicalOrder_forward src dst ha⟩ :=
  checkDAGWithOrder_complete src dst _ (topologicalOrder_forward src dst ha)

end DAGSpectral
