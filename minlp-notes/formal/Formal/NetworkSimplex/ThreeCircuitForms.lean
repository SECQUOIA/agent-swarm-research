import Formal.NetworkSimplex.ThresholdClassification

/-! # The four forms of the reduced three-label positive circuits

The sixteen rows of `weight` are classified into the four forms of the paper's
display, each described by its own combinatorial parameter rather than by a
range of row indices:

* the **subset dependency** of a nonempty label set `S`: the upper normal of `S`
  against the lower normals of the labels of `S` (seven of them);
* the **partition** dependency of a partition `P` of the three labels: the upper
  normals of the blocks of `P` against the lower normal of the total (five);
* the **overlap** dependency at a label `a`: the upper normals of the two pairs
  through `a`, against the lower normal of `a` and the lower normal of the total
  (three);
* the **half cover**: the upper normals of all three pairs against twice the
  lower normal of the total (one).

The naming of the eleven normals is anchored to their geometry by
`normal_upperIndex`, `normal_lowerIndex`, `normal_lowerTotal` and the two
exhaustiveness lemmas `nonneg_normal_iff` and `neg_normal_iff`; the four weight
vectors are then built from that naming alone.
-/

namespace NetworkSimplex.ThreeStateCircuits

-- The decision procedures below enumerate the 256 candidate block families.
set_option maxRecDepth 4000

/-! ## Naming the eleven normals by their label sets -/

/-- The index of the upper normal `1_S` of a label set `S`. The empty set has no
upper normal; every statement below restricts to nonempty label sets. -/
def upperIndex (S : Finset (Fin 3)) : Fin 11 :=
  if 0 ∈ S then (if 1 ∈ S then (if 2 ∈ S then 6 else 3) else (if 2 ∈ S then 4 else 0))
  else (if 1 ∈ S then (if 2 ∈ S then 5 else 1) else (if 2 ∈ S then 2 else 0))

/-- The index of the lower normal `-e_j` of a single label. -/
def lowerIndex (j : Fin 3) : Fin 11 := ⟨7 + j.val, by omega⟩

/-- The index of the lower normal `-1` of the whole label set. -/
def lowerTotal : Fin 11 := 10

/-- The upper normal of a nonempty label set is its indicator vector. -/
theorem normal_upperIndex : ∀ S : Finset (Fin 3), S.Nonempty →
    ∀ j, normal (upperIndex S) j = if j ∈ S then 1 else 0 := by decide

/-- The lower normal of a label is the negated coordinate vector. -/
theorem normal_lowerIndex : ∀ j k : Fin 3,
    normal (lowerIndex j) k = if k = j then -1 else 0 := by decide

/-- The lower total normal is the negated all-ones vector. -/
theorem normal_lowerTotal : ∀ j, normal lowerTotal j = -1 := by decide

/-- The nonnegative normals are exactly the upper normals of the nonempty label
sets, so `upperIndex` names all of them and nothing else. -/
theorem nonneg_normal_iff : ∀ i : Fin 11,
    (∀ j, 0 ≤ normal i j) ↔ ∃ S : Finset (Fin 3), S.Nonempty ∧ i = upperIndex S := by decide

/-- The remaining normals are exactly the lower normals of the single labels and
the lower normal of the total. -/
theorem neg_normal_iff : ∀ i : Fin 11,
    (∃ j, normal i j < 0) ↔ (∃ j, i = lowerIndex j) ∨ i = lowerTotal := by decide

/-- The upper index of a nonempty label set is the *only* index whose normal is
the indicator vector of that set, so the naming is forced by the geometry. -/
theorem upperIndex_unique : ∀ (S : Finset (Fin 3)), S.Nonempty → ∀ i : Fin 11,
    (∀ j, normal i j = if j ∈ S then 1 else 0) → i = upperIndex S := by decide

/-- The lower index of a label is the only index whose normal is the negated
coordinate vector of that label. -/
theorem lowerIndex_unique : ∀ (j : Fin 3) (i : Fin 11),
    (∀ k, normal i k = if k = j then -1 else 0) → i = lowerIndex j := by decide

/-- The lower total index is the only index whose normal is the negated all-ones
vector. -/
theorem lowerTotal_unique : ∀ i : Fin 11, (∀ j, normal i j = -1) → i = lowerTotal := by decide

/-- Distinct nonempty label sets have distinct upper normals. -/
theorem upperIndex_inj : ∀ S T : Finset (Fin 3), S.Nonempty → T.Nonempty →
    upperIndex S = upperIndex T → S = T := by decide

/-! ## The four forms -/

/-- `chain3-circuits-a`: the upper normal of a nonempty label set against the
lower normals of its labels. -/
def subsetWeight (S : Finset (Fin 3)) : Fin 11 → ℤ := fun i =>
  (if i = upperIndex S then 1 else 0) + ∑ j ∈ S, if i = lowerIndex j then 1 else 0

/-- A partition of the three labels: nonempty blocks, each label in exactly one. -/
def IsLabelPartition (P : Finset (Finset (Fin 3))) : Prop :=
  (∀ B ∈ P, B.Nonempty) ∧ ∀ j : Fin 3, (P.filter fun B => j ∈ B).card = 1

/-- `chain3-circuits-b`: the upper normals of the blocks of a partition against
the lower normal of the total. -/
def partitionWeight (P : Finset (Finset (Fin 3))) : Fin 11 → ℤ := fun i =>
  (∑ B ∈ P, if i = upperIndex B then 1 else 0) + (if i = lowerTotal then 1 else 0)

/-- `chain3-circuits-c`: the upper normals of the two pairs through a label `a`,
against the lower normal of `a` and the lower normal of the total. -/
def overlapWeight (a : Fin 3) : Fin 11 → ℤ := fun i =>
  (∑ b ∈ ({a}ᶜ : Finset (Fin 3)), if i = upperIndex {a, b} then 1 else 0) +
    (if i = lowerIndex a then 1 else 0) + (if i = lowerTotal then 1 else 0)

/-- The three two-label sets. -/
def labelPairs : Finset (Finset (Fin 3)) :=
  Finset.univ.filter fun B => B.card = 2

/-- `chain3-circuits-d`: the upper normals of all three pairs against twice the
lower normal of the total. -/
def halfCoverWeight : Fin 11 → ℤ := fun i =>
  (∑ B ∈ labelPairs, if i = upperIndex B then 1 else 0) +
    2 * (if i = lowerTotal then 1 else 0)

/-- A listed circuit of the first form. -/
def SubsetForm (c : Fin 16) : Prop := ∃ S : Finset (Fin 3), S.Nonempty ∧ weight c = subsetWeight S

/-- A listed circuit of the second form. -/
def PartitionForm (c : Fin 16) : Prop :=
  ∃ P : Finset (Finset (Fin 3)), IsLabelPartition P ∧ weight c = partitionWeight P

/-- A listed circuit of the third form. -/
def OverlapForm (c : Fin 16) : Prop := ∃ a : Fin 3, weight c = overlapWeight a

/-- A listed circuit of the fourth form. -/
def HalfCoverForm (c : Fin 16) : Prop := weight c = halfCoverWeight

instance : DecidablePred IsLabelPartition := fun _ => by unfold IsLabelPartition; infer_instance
instance : DecidablePred SubsetForm := fun _ => by unfold SubsetForm; infer_instance
instance : DecidablePred PartitionForm := fun _ => by unfold PartitionForm; infer_instance
instance : DecidablePred OverlapForm := fun _ => by unfold OverlapForm; infer_instance
instance : DecidablePred HalfCoverForm := fun _ => by unfold HalfCoverForm; infer_instance

/-! ## The four families are genuine positive dependences

Each family cancels for the reason its description gives: a label set against its
own labels, a partition against the total, the two pairs through a label against
that label and the total, and all three pairs against twice the total. These
proofs use only the combinatorial definitions above, not the sixteen rows.
-/

/-- Positivity of the four families. -/
theorem subsetWeight_nonneg : ∀ (S : Finset (Fin 3)) (i : Fin 11), 0 ≤ subsetWeight S i := by
  decide

theorem partitionWeight_nonneg : ∀ (P : Finset (Finset (Fin 3))) (i : Fin 11),
    0 ≤ partitionWeight P i := by decide

theorem overlapWeight_nonneg : ∀ (a : Fin 3) (i : Fin 11), 0 ≤ overlapWeight a i := by decide

theorem halfCoverWeight_nonneg : ∀ i : Fin 11, 0 ≤ halfCoverWeight i := by decide

/-- `1_S = ∑_{j ∈ S} e_j`. -/
theorem subsetWeight_cancellation : ∀ (S : Finset (Fin 3)), S.Nonempty →
    ∀ j, ∑ i, subsetWeight S i * normal i j = 0 := by decide

/-- The blocks of a partition cover every label exactly once. -/
theorem partitionWeight_cancellation : ∀ (P : Finset (Finset (Fin 3))), IsLabelPartition P →
    ∀ j, ∑ i, partitionWeight P i * normal i j = 0 := by decide

/-- The two pairs through `a` cover `a` twice and every other label once. -/
theorem overlapWeight_cancellation : ∀ (a : Fin 3),
    ∀ j, ∑ i, overlapWeight a i * normal i j = 0 := by decide

/-- The three pairs cover every label exactly twice. -/
theorem halfCoverWeight_cancellation :
    ∀ j, ∑ i, halfCoverWeight i * normal i j = 0 := by decide

/-- Every displayed form has an entry equal to one, so its integer entries have
no common divisor other than `±1`: each form is already the primitive
representative of its ray. -/
theorem forms_have_unit_entry :
    (∀ S : Finset (Fin 3), S.Nonempty → ∃ i, subsetWeight S i = 1) ∧
      (∀ P : Finset (Finset (Fin 3)), IsLabelPartition P → ∃ i, partitionWeight P i = 1) ∧
      (∀ a : Fin 3, ∃ i, overlapWeight a i = 1) ∧ (∃ i, halfCoverWeight i = 1) := by decide

/-! ## Distinct parameters give distinct circuits -/

/-- Distinct nonempty label sets give distinct subset dependencies. -/
theorem subsetWeight_inj : ∀ S T : Finset (Fin 3), S.Nonempty → T.Nonempty →
    subsetWeight S = subsetWeight T → S = T := by decide

/-- Distinct partitions give distinct partition dependencies. -/
theorem partitionWeight_inj : ∀ P Q : Finset (Finset (Fin 3)), IsLabelPartition P →
    IsLabelPartition Q → partitionWeight P = partitionWeight Q → P = Q := by decide

/-- Distinct labels give distinct overlap dependencies. -/
theorem overlapWeight_inj : ∀ a b : Fin 3, overlapWeight a = overlapWeight b → a = b := by decide

/-! ## Every listed circuit has exactly one form -/

/-- Exactly one of the four forms holds for each listed circuit. -/
theorem forms_exclusive : ∀ c : Fin 16,
    (SubsetForm c ∧ ¬ PartitionForm c ∧ ¬ OverlapForm c ∧ ¬ HalfCoverForm c) ∨
    (¬ SubsetForm c ∧ PartitionForm c ∧ ¬ OverlapForm c ∧ ¬ HalfCoverForm c) ∨
    (¬ SubsetForm c ∧ ¬ PartitionForm c ∧ OverlapForm c ∧ ¬ HalfCoverForm c) ∨
    (¬ SubsetForm c ∧ ¬ PartitionForm c ∧ ¬ OverlapForm c ∧ HalfCoverForm c) := by decide

/-- The four forms exhaust the library. -/
theorem forms_exhaustive (c : Fin 16) :
    SubsetForm c ∨ PartitionForm c ∨ OverlapForm c ∨ HalfCoverForm c := by
  rcases forms_exclusive c with ⟨h, _⟩ | ⟨_, h, _⟩ | ⟨_, _, h, _⟩ | ⟨_, _, _, h⟩
  · exact Or.inl h
  · exact Or.inr (Or.inl h)
  · exact Or.inr (Or.inr (Or.inl h))
  · exact Or.inr (Or.inr (Or.inr h))

/-! ## Realization: every parameter value occurs -/

/-- Every nonempty label set occurs as a subset dependency. -/
theorem exists_subsetForm : ∀ S : Finset (Fin 3), S.Nonempty →
    ∃ c : Fin 16, weight c = subsetWeight S := by decide

/-- Every partition of the labels occurs as a partition dependency. -/
theorem exists_partitionForm : ∀ P : Finset (Finset (Fin 3)), IsLabelPartition P →
    ∃ c : Fin 16, weight c = partitionWeight P := by decide

/-- Every label occurs as the centre of an overlap dependency. -/
theorem exists_overlapForm : ∀ a : Fin 3, ∃ c : Fin 16, weight c = overlapWeight a := by decide

/-- The half cover occurs. -/
theorem exists_halfCoverForm : ∃ c : Fin 16, weight c = halfCoverWeight := ⟨15, by decide⟩

/-! ## The counts seven, five, three and one -/

/-- The seven nonempty label sets. -/
theorem nonemptyLabelSets_card :
    ((Finset.univ : Finset (Finset (Fin 3))).filter fun S => S.Nonempty).card = 7 := by decide

/-- The five partitions of the three labels. -/
theorem labelPartitions_card :
    ((Finset.univ : Finset (Finset (Finset (Fin 3)))).filter IsLabelPartition).card = 5 := by
  decide

/-- The three two-label sets. -/
theorem labelPairs_card : labelPairs.card = 3 := by decide

/-- The subset dependencies of the library. -/
def subsetForms : Finset (Fin 16) := Finset.univ.filter SubsetForm
/-- The partition dependencies of the library. -/
def partitionForms : Finset (Fin 16) := Finset.univ.filter PartitionForm
/-- The overlap dependencies of the library. -/
def overlapForms : Finset (Fin 16) := Finset.univ.filter OverlapForm
/-- The half cover of the library. -/
def halfCoverForms : Finset (Fin 16) := Finset.univ.filter HalfCoverForm

/-- Seven subset dependencies, one for each nonempty label set. -/
theorem subsetForms_card : subsetForms.card = 7 := by decide

/-- Five partition dependencies, one for each partition of the three labels. -/
theorem partitionForms_card : partitionForms.card = 5 := by decide

/-- Three overlap dependencies, one for each label. -/
theorem overlapForms_card : overlapForms.card = 3 := by decide

/-- One half cover. -/
theorem halfCoverForms_card : halfCoverForms.card = 1 := by decide

/-- The four forms partition the sixteen listed circuits. -/
theorem forms_union : subsetForms ∪ partitionForms ∪ overlapForms ∪ halfCoverForms =
    Finset.univ := by decide

/-- FC38, counting form: `7 + 5 + 3 + 1 = 16`. -/
theorem forms_card_total :
    subsetForms.card + partitionForms.card + overlapForms.card + halfCoverForms.card =
      (Finset.univ : Finset (Fin 16)).card := by
  rw [subsetForms_card, partitionForms_card, overlapForms_card, halfCoverForms_card]
  decide

/-! ## The classification of all primitive positive circuits -/

/-- FC38: every real support-minimal positive dependence among the eleven reduced
normals is a positive multiple of one of the four displayed forms. This theorem
exports existence; `forms_exclusive` separately gives exclusivity for the library. -/
theorem supportMinimal_four_forms (a : Fin 11 → ℝ) (ha : SupportMinimal a) :
    ∃ t : ℝ, 0 < t ∧
      ((∃ S : Finset (Fin 3), S.Nonempty ∧ ∀ i, a i = t * (subsetWeight S i : ℝ)) ∨
       (∃ P : Finset (Finset (Fin 3)), IsLabelPartition P ∧
          ∀ i, a i = t * (partitionWeight P i : ℝ)) ∨
       (∃ b : Fin 3, ∀ i, a i = t * (overlapWeight b i : ℝ)) ∨
       (∀ i, a i = t * (halfCoverWeight i : ℝ))) := by
  obtain ⟨c, t, ht, he⟩ := supportMinimal_classification a ha
  refine ⟨t, ht, ?_⟩
  rcases forms_exhaustive c with ⟨S, hS, hw⟩ | ⟨P, hP, hw⟩ | ⟨b, hw⟩ | hw
  · exact Or.inl ⟨S, hS, fun i => by rw [he i, congrFun hw i]⟩
  · exact Or.inr (Or.inl ⟨P, hP, fun i => by rw [he i, congrFun hw i]⟩)
  · exact Or.inr (Or.inr (Or.inl ⟨b, fun i => by rw [he i, congrFun hw i]⟩))
  · exact Or.inr (Or.inr (Or.inr fun i => by rw [he i, congrFun hw i]))

/-- The second half of FC38: the only doubled weight in the library is the one on
the lower total normal of the half cover. -/
theorem weight_eq_two_iff : ∀ (c : Fin 16) (i : Fin 11),
    weight c i = 2 ↔ HalfCoverForm c ∧ i = lowerTotal := by decide

end NetworkSimplex.ThreeStateCircuits
