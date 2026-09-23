import Formal.MultilinearGap.StructuralFeedbackForest
import Formal.MultilinearGap.StructuralTreewidthDecomposition
import Mathlib.Combinatorics.SimpleGraph.Acyclic
import Mathlib.Combinatorics.SimpleGraph.Walk.Counting

/-! Genuine incidence forests admit a factor elimination order. -/
namespace MultilinearGap.ForestGluing
open SimpleGraph
noncomputable section
variable {I E : Type*} [Finite I] [Finite E] [DecidableEq I] [DecidableEq E]

/-- Retain precisely the incidence edges of the active factors. -/
def activeIncidence (scope : E → Finset I) (active : Finset E) : SimpleGraph (I ⊕ E) :=
  StructuralTreewidth.incidenceGraph (fun i e => e ∈ active ∧ i ∈ scope e)

omit [DecidableEq I] [DecidableEq E] in
/-- An active factor in a finite incidence forest shares at most one variable
with the other active factors. The proof chooses a longest factor-ending path. -/
theorem exists_leaf_factor (scope : E → Finset I) (active : Finset E)
    (ha : active.Nonempty) (hforest : (activeIncidence scope active).IsAcyclic) :
    ∃ e ∈ active, {i : I | i ∈ scope e ∧ ∃ f ∈ active, f ≠ e ∧ i ∈ scope f}.Subsingleton := by
  classical
  let := Fintype.ofFinite I
  let := Fintype.ofFinite E
  let G := activeIncidence scope active
  obtain ⟨root, hroot⟩ := ha
  let Paths := (e : active) × G.Path (Sum.inr root) (Sum.inr e.val)
  have hne : Nonempty Paths := ⟨⟨⟨root, hroot⟩, ⟨.nil, by simp⟩⟩⟩
  obtain ⟨p, _, hmax⟩ := Finset.exists_max_image (Finset.univ : Finset Paths)
    (fun p => p.2.val.length) Finset.univ_nonempty
  refine ⟨p.1.val, p.1.property, ?_⟩
  have hp (i : I) (hi : i ∈ scope p.1.val)
      (hf : ∃ f ∈ active, f ≠ p.1.val ∧ i ∈ scope f) :
      Sum.inl i = p.2.val.penultimate := by
    have hadj : G.Adj (Sum.inr p.1.val) (Sum.inl i) := ⟨p.1.property, hi⟩
    by_contra hne
    have hout : Sum.inl i ∉ p.2.val.support := fun hmem =>
      hne (hforest.eq_penultimate_of_adj_end p.2.property hadj hmem)
    obtain ⟨f, hfa, hfe, hif⟩ := hf
    have hadjf : G.Adj (Sum.inl i) (Sum.inr f) := ⟨hfa, hif⟩
    have hp1 := p.2.property.concat hout hadj
    have houtf : Sum.inr f ∉ (p.2.val.concat hadj).support := by
      intro hmem
      have he := hforest.eq_penultimate_of_adj_end hp1 hadjf hmem
      simp only [Walk.penultimate_concat] at he
      exact hfe (Sum.inr.inj he)
    have hp2 := hp1.concat houtf hadjf
    have hm := hmax ⟨⟨f, hfa⟩, ⟨_, hp2⟩⟩ (Finset.mem_univ _)
    simp only [Walk.length_concat] at hm
    omega
  intro i hi j hj
  exact Sum.inl.inj ((hp i hi.1 hi.2).trans (hp j hj.1 hj.2).symm)


omit [Finite I] [Finite E] [DecidableEq I] [DecidableEq E] in
/-- Deleting factors only deletes incidence edges. -/
theorem activeIncidence_mono (scope : E → Finset I) {a b : Finset E}
    (h : a ⊆ b) : activeIncidence scope a ≤ activeIncidence scope b := by
  intro v w hvw
  cases v <;> cases w <;>
    simp only [activeIncidence, StructuralTreewidth.incidenceGraph] at hvw ⊢
  · exact ⟨h hvw.1, hvw.2⟩
  · exact ⟨h hvw.1, hvw.2⟩

omit [Finite I] [Finite E] [DecidableEq E] in
theorem mem_covered_iff (scope : E → Finset I) (es : List E) (i : I) :
    i ∈ covered scope es ↔ ∃ e ∈ es, i ∈ scope e := by
  induction es with
  | nil => simp [covered]
  | cons e es ih => simp [covered, ih]

/-- Enumerate the active factors in a valid elimination order. This is derived
from ordinary graph acyclicity, including disconnected forests and empty scopes. -/
theorem exists_eliminationOrder_active (scope : E → Finset I) (active : Finset E)
    (hforest : (activeIncidence scope active).IsAcyclic) :
    ∃ es : List E, es.toFinset = active ∧ es.Nodup ∧ EliminationOrder scope es := by
  classical
  revert hforest
  induction active using Finset.strongInductionOn
  rename_i active ih
  intro hforest
  by_cases hz : active = ∅
  · subst active
    exact ⟨[], rfl, List.nodup_nil, .nil⟩
  obtain ⟨e, he, hleaf⟩ := exists_leaf_factor scope active
    (Finset.nonempty_iff_ne_empty.mpr hz) hforest
  have hf : (activeIncidence scope (active.erase e)).IsAcyclic :=
    hforest.anti (activeIncidence_mono scope (Finset.erase_subset e active))
  obtain ⟨es, hes, hn, ho⟩ := ih (active.erase e) (Finset.erase_ssubset he) hf
  have hnot : e ∉ es := by
    intro hmem
    have : e ∈ active.erase e := hes ▸ List.mem_toFinset.mpr hmem
    exact (Finset.mem_erase.mp this).1 rfl
  refine ⟨e :: es, ?_, List.nodup_cons.mpr ⟨hnot, hn⟩, .cons e es ho ?_⟩
  · simp [hes, Finset.insert_erase he]
  · intro i hi j hj
    apply hleaf
    · obtain ⟨f, hf, hif⟩ := (mem_covered_iff scope es i).mp
        (Finset.mem_inter.mp hi).1
      have hfa : f ∈ active.erase e := hes ▸ List.mem_toFinset.mpr hf
      exact ⟨(Finset.mem_inter.mp hi).2, f, Finset.mem_of_mem_erase hfa,
        (Finset.mem_erase.mp hfa).1, hif⟩
    · obtain ⟨f, hf, hjf⟩ := (mem_covered_iff scope es j).mp
        (Finset.mem_inter.mp hj).1
      have hfa : f ∈ active.erase e := hes ▸ List.mem_toFinset.mpr hf
      exact ⟨(Finset.mem_inter.mp hj).2, f, Finset.mem_of_mem_erase hfa,
        (Finset.mem_erase.mp hfa).1, hjf⟩

omit [DecidableEq E] in
/-- Every finite ordinary incidence forest has a factor elimination order. -/
theorem exists_eliminationOrder (scope : E → Finset I)
    (hforest : (StructuralTreewidth.incidenceGraph (fun i e => i ∈ scope e)).IsAcyclic) :
    ∃ es : List E, (∀ e, e ∈ es) ∧ es.Nodup ∧ EliminationOrder scope es := by
  classical
  let := Fintype.ofFinite E
  have heq : activeIncidence scope Finset.univ =
      StructuralTreewidth.incidenceGraph (fun i e => i ∈ scope e) := by
    ext v w
    cases v <;> cases w <;> simp [activeIncidence, StructuralTreewidth.incidenceGraph]
  obtain ⟨es, hes, hn, ho⟩ := exists_eliminationOrder_active scope Finset.univ
    (heq.symm ▸ hforest)
  refine ⟨es, ?_, hn, ho⟩
  intro e
  apply List.mem_toFinset.mp
  rw [hes]
  exact Finset.mem_univ e

end
end MultilinearGap.ForestGluing
