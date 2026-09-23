import Formal.MultilinearGap.StructuralFrequency

/-!
# The frequency-two dual multigraph

A support is a factor vertex and a variable is an edge. Variables in only one
support get one private dummy endpoint; unused variables get two. Thus all
edges are loopless and the incidence row at each factor is its original support.
-/
namespace MultilinearGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]
namespace FrequencyTwo

abbrev Factor (S : Finset (Finset I)) := {s // s ∈ S}
abbrev DualVertex (S : Finset (Finset I)) := Sum (Factor S) (I × Bool)

def factorsAt (S : Finset (Finset I)) (i : I) : Finset (Factor S) :=
  Finset.univ.filter fun s => i ∈ s.val

omit [Fintype I] in
@[simp] theorem mem_factorsAt (S : Finset (Finset I)) (i : I) (s : Factor S) :
    s ∈ factorsAt S i ↔ i ∈ s.val := by simp [factorsAt]

omit [Fintype I] in
theorem card_factorsAt (S : Finset (Finset I)) (i : I) :
    (factorsAt S i).card = (S.filter fun s => i ∈ s).card := by
  apply Finset.card_bij (fun s _ => s.val)
  · intro s hs
    exact Finset.mem_filter.mpr ⟨s.property, (mem_factorsAt S i s).mp hs⟩
  · intro s hs t ht h
    exact Subtype.ext h
  · intro s hs
    exact ⟨⟨s, (Finset.mem_filter.mp hs).1⟩,
      (mem_factorsAt S i _).mpr (Finset.mem_filter.mp hs).2, rfl⟩

private def EndpointSpecification (S : Finset (Finset I)) (i : I)
    (l r : DualVertex S) : Prop :=
  l ≠ r ∧
    (∀ s : Factor S, (l = Sum.inl s ∨ r = Sum.inl s) ↔ i ∈ s.val) ∧
    (∀ j b, (l = Sum.inr (j, b) ∨ r = Sum.inr (j, b)) → j = i)

omit [Fintype I] in
private theorem endpoints_exist (S : Finset (Finset I)) (hS : FrequencyTwo S) (i : I) :
    ∃ l r, EndpointSpecification S i l r := by
  have hc : (factorsAt S i).card ≤ 2 := by rw [card_factorsAt]; exact hS i
  have hm (s : Factor S) := mem_factorsAt S i s
  interval_cases hn : (factorsAt S i).card
  · have he : factorsAt S i = ∅ := Finset.card_eq_zero.mp hn
    refine ⟨Sum.inr (i, false), Sum.inr (i, true), ?_⟩
    refine ⟨by simp, ?_, ?_⟩
    · intro s
      have hh := hm s
      simpa [he] using hh
    · intro j b h
      rcases h with h | h <;> exact (Prod.mk.inj (Sum.inr.inj h)).1.symm
  · obtain ⟨s, hs⟩ := Finset.card_eq_one.mp hn
    refine ⟨Sum.inl s, Sum.inr (i, false), ?_⟩
    refine ⟨by simp, ?_, ?_⟩
    · intro t
      have hh := hm t
      simpa [hs, eq_comm] using hh
    · intro j b h
      rcases h with h | h
      · cases h
      · exact (Prod.mk.inj (Sum.inr.inj h)).1.symm
  · obtain ⟨s, t, hst, he⟩ := Finset.card_eq_two.mp hn
    refine ⟨Sum.inl s, Sum.inl t, ?_⟩
    refine ⟨by simpa using hst, ?_, ?_⟩
    · intro u
      have hh := hm u
      simpa [he, eq_comm] using hh
    · intro j b h
      rcases h with h | h <;> cases h

/-- The actual occurrence set gives the endpoints; private vertices supply any
missing occurrences. -/
def dualGraph (S : Finset (Finset I)) (hS : FrequencyTwo S) :
    FrequencyGraph (DualVertex S) I where
  left i := (endpoints_exist S hS i).choose
  right i := (endpoints_exist S hS i).choose_spec.choose
  loopless i := (endpoints_exist S hS i).choose_spec.choose_spec.1

@[simp] theorem incident_factor (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (s : Factor S) : (dualGraph S hS).incident (Sum.inl s) = s.val := by
  ext i
  rw [FrequencyGraph.mem_incident]
  exact (endpoints_exist S hS i).choose_spec.choose_spec.2.1 s

/-- A private dummy endpoint has no incidence except possibly its own variable. -/
theorem incident_dummy_subset (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (i : I) (b : Bool) : (dualGraph S hS).incident (Sum.inr (i, b)) ⊆ {i} := by
  intro j hj
  have h := (endpoints_exist S hS j).choose_spec.choose_spec.2.2 i b
    ((FrequencyGraph.mem_incident _ _ _).mp hj)
  simpa using h.symm

theorem incident_dummy_card_le_one (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (i : I) (b : Bool) : ((dualGraph S hS).incident (Sum.inr (i, b))).card ≤ 1 := by
  simpa using Finset.card_le_card (incident_dummy_subset S hS i b)

/-- Dummy vertices have zero objective weight. -/
def dualWeight (S : Finset (Finset I)) (a : Finset I → ℝ) : DualVertex S → ℝ
  | Sum.inl s => a s.val
  | Sum.inr _ => 0

omit [Fintype I] [DecidableEq I] in
theorem dualWeight_nonneg (S : Finset (Finset I)) (a : Finset I → ℝ)
    (ha : ∀ s ∈ S, 0 ≤ a s) (v : DualVertex S) : 0 ≤ dualWeight S a v := by
  cases v with
  | inl s => exact ha s.val s.property
  | inr j => exact le_rfl

/-- Every weighted incidence-row expression equals its original support sum. -/
theorem sum_dualWeight (S : Finset (Finset I)) (hS : FrequencyTwo S)
    (a f : Finset I → ℝ) :
    ∑ v : DualVertex S, dualWeight S a v * f ((dualGraph S hS).incident v) =
      ∑ s ∈ S, a s * f s := by
  simp only [DualVertex, Fintype.sum_sum_type, dualWeight, incident_factor,
    zero_mul, Finset.sum_const_zero, add_zero]
  exact Finset.sum_attach S (fun s => a s * f s)

end FrequencyTwo
end
end MultilinearGap
