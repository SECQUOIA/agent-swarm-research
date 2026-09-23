import Formal.NetworkSimplex.ThresholdUnreducedClassification
import Formal.NetworkSimplex.ThresholdUnreducedSupport

/-! Complete primitive circuit classification and exact dimension-specific counts. -/
namespace NetworkSimplex.Threshold.UnreducedCircuits
open scoped BigOperators

/-- The rows are distinct members of the full signed nonempty subset universe. -/
theorem normal_injective : Function.Injective normal := by decide +kernel

theorem normal_sign : ∀ i,
    normal i ≠ 0 ∧ ((∀ j, normal i j = 0 ∨ normal i j = 1) ∨
      (∀ j, normal i j = 0 ∨ normal i j = -1)) := by decide +kernel

/-- The displayed rows are exactly all signed nonzero zero-one vectors in three coordinates. -/
theorem normal_range (v : Fin 3 → ℤ) :
    v ∈ Set.range normal ↔ v ≠ 0 ∧
      ((∀ j, v j = 0 ∨ v j = 1) ∨ (∀ j, v j = 0 ∨ v j = -1)) := by
  constructor
  · rintro ⟨i, rfl⟩
    exact normal_sign i
  · rintro ⟨hne, hsign⟩
    change ∃ i, normal i = v
    rcases hsign with h | h
    all_goals
      have h0 := h 0
      have h1 := h 1
      have h2 := h 2
      rcases h0 with h0 | h0 <;> rcases h1 with h1 | h1 <;> rcases h2 with h2 | h2
    all_goals first
      | (simp [normal, funext_iff, Fin.exists_fin_succ, Fin.forall_fin_succ, h0, h1, h2]; done)
      | exact False.elim (hne (funext (fun j => by fin_cases j <;> assumption)))

/-- Nonzero nonnegative real cancellation. -/
def PositiveDependence (a : Fin 14 → ℝ) : Prop :=
  (∀ i, 0 ≤ a i) ∧ (∃ i, a i ≠ 0) ∧ ∀ j, ∑ i, a i * (normal i j : ℝ) = 0

/-- A positive circuit is minimal among the supports of positive dependencies. -/
def PositiveCircuit (a : Fin 14 → ℝ) : Prop :=
  PositiveDependence a ∧ ∀ b, PositiveDependence b →
    (∀ i, a i = 0 → b i = 0) → ∀ i, b i ≠ 0 ↔ a i ≠ 0

theorem weight_positiveDependence (c : Fin 41) :
    PositiveDependence (fun i => (weight c i : ℝ)) := by
  dsimp only [PositiveDependence]
  refine ⟨fun i => by exact_mod_cast weight_nonnegative c i, ?_, ?_⟩
  · obtain ⟨i, hi⟩ := weight_nonzero c
    exact ⟨i, by exact_mod_cast hi⟩
  · intro j
    exact_mod_cast normal_cancellation c j

theorem weight_positiveCircuit (c : Fin 41) :
    PositiveCircuit (fun i => (weight c i : ℝ)) := by
  refine ⟨weight_positiveDependence c, ?_⟩
  intro b hb hs
  have hsp : ∀ i, weight c i = 0 → b i = 0 :=
    fun i hi => hs i (by change (weight c i : ℝ) = 0; exact_mod_cast hi)
  have he := dependence_on_support c b hsp hb.2.2
  have hn : b (pivot c) ≠ 0 := by
    intro h
    obtain ⟨i, hi⟩ := hb.2.1
    have hi' := congrFun he i
    rw [h, zero_mul] at hi'
    exact hi hi'
  intro i
  rw [congrFun he i, mul_ne_zero_iff]
  exact and_iff_right hn

/-- Every real positive circuit is a positive multiple of a displayed primitive row. -/
theorem positiveCircuit_classification (a : Fin 14 → ℝ) (ha : PositiveCircuit a) :
    ∃ c : Fin 41, 0 < a (pivot c) ∧ a = fun i => a (pivot c) * (weight c i : ℝ) := by
  obtain ⟨c, hc⟩ := dependence_contains_circuit a ha.1.1 ha.1.2.1 ha.1.2.2
  have hs : ∀ i, a i = 0 → (weight c i : ℝ) = 0 := by
    intro i hi
    have hw : weight c i = 0 := by
      by_contra hw
      exact hc i hw hi
    exact_mod_cast hw
  have hmin := ha.2 (fun i => (weight c i : ℝ)) (weight_positiveDependence c) hs
  have hsp : ∀ i, weight c i = 0 → a i = 0 := by
    intro i hi
    by_contra hai
    have hwi := (hmin i).2 hai
    apply hwi
    exact_mod_cast hi
  have hp : a (pivot c) ≠ 0 := hc _ (by rw [pivot_weight]; norm_num)
  exact ⟨c, lt_of_le_of_ne (ha.1.1 _) (Ne.symm hp),
    dependence_on_support c a hsp ha.1.2.2⟩

def naturalWeight (c : Fin 41) (i : Fin 14) : ℕ := (weight c i).toNat

@[simp] theorem naturalWeight_cast (c : Fin 41) (i : Fin 14) :
    (naturalWeight c i : ℝ) = (weight c i : ℝ) := by
  rw [naturalWeight, ← Int.cast_natCast, Int.toNat_of_nonneg (weight_nonnegative c i)]

@[simp] theorem naturalWeight_pivot (c : Fin 41) : naturalWeight c (pivot c) = 1 := by
  simp [naturalWeight, pivot_weight]

/-- Primitive normalization refers to actual integer weights, not an assumed bounded search. -/
def PrimitiveCircuit (a : Fin 14 → ℕ) : Prop :=
  PositiveCircuit (fun i => (a i : ℝ)) ∧ Finset.univ.gcd a = 1

theorem naturalWeight_primitive (c : Fin 41) : PrimitiveCircuit (naturalWeight c) := by
  constructor
  · simpa only [naturalWeight_cast] using weight_positiveCircuit c
  · have h := Finset.gcd_dvd (f := naturalWeight c) (Finset.mem_univ (pivot c))
    rw [naturalWeight_pivot] at h
    exact Nat.dvd_one.mp h

/-- Complete classification over all natural weights, with no coefficient bound premise. -/
theorem primitiveCircuit_iff (a : Fin 14 → ℕ) :
    PrimitiveCircuit a ↔ ∃ c : Fin 41, a = naturalWeight c := by
  constructor
  · intro ha
    obtain ⟨c, _, he⟩ := positiveCircuit_classification (fun i => (a i : ℝ)) ha.1
    have hn (i : Fin 14) : a i = a (pivot c) * naturalWeight c i := by
      have h := congrFun he i
      rw [← naturalWeight_cast] at h
      exact_mod_cast h
    have hd : a (pivot c) ∣ Finset.univ.gcd a := by
      apply Finset.dvd_gcd
      intro i _
      exact ⟨naturalWeight c i, hn i⟩
    rw [ha.2] at hd
    have hp := Nat.dvd_one.mp hd
    exact ⟨c, funext (fun i => by simpa only [hp, one_mul] using hn i)⟩
  · rintro ⟨c, rfl⟩
    exact naturalWeight_primitive c

theorem naturalWeight_injective : Function.Injective naturalWeight := by
  intro c d h
  apply weight_injective
  ext i
  have hi := congrArg (fun w => (w i : ℝ)) h
  simpa only [naturalWeight_cast, Int.cast_inj] using hi

/-- Dimension restriction embeds the full signed-subset universe in its first coordinates. -/
def InDimension (d : ℕ) (a : Fin 14 → ℕ) : Prop :=
  ∀ i, a i ≠ 0 → ∀ j : Fin 3, d ≤ j.val → normal i j = 0

instance (d : ℕ) (a : Fin 14 → ℕ) : Decidable (InDimension d a) :=
  inferInstanceAs (Decidable (∀ i, a i ≠ 0 → ∀ j : Fin 3, d ≤ j.val → normal i j = 0))

def library (d : ℕ) : Finset (Fin 41) :=
  Finset.univ.filter (fun c => InDimension d (naturalWeight c))

def normalLibrary (d : ℕ) : Finset (Fin 14) :=
  Finset.univ.filter (fun i => ∀ j : Fin 3, d ≤ j.val → normal i j = 0)

theorem normal_counts : (normalLibrary 1).card = 2 ∧ (normalLibrary 2).card = 6 ∧
    (normalLibrary 3).card = 14 := by decide +kernel

theorem library_counts : (library 1).card = 1 ∧ (library 2).card = 5 ∧
    (library 3).card = 41 := by decide +kernel

theorem primitive_circuits_exact (d : ℕ) :
    {a | PrimitiveCircuit a ∧ InDimension d a} = ↑((library d).image naturalWeight) := by
  ext a
  simp only [Set.mem_ofPred_eq, Finset.mem_coe, Finset.mem_image, library,
    Finset.mem_filter, Finset.mem_univ, true_and, primitiveCircuit_iff]
  constructor
  · rintro ⟨⟨c, rfl⟩, hc⟩
    exact ⟨c, hc, rfl⟩
  · rintro ⟨c, hc, rfl⟩
    exact ⟨⟨c, rfl⟩, hc⟩

theorem primitive_circuit_count (d : ℕ) :
    {a | PrimitiveCircuit a ∧ InDimension d a}.ncard = (library d).card := by
  rw [primitive_circuits_exact, Set.ncard_coe_finset,
    Finset.card_image_of_injective _ naturalWeight_injective]

/-- Exact counts of all primitive positive circuits, not only the displayed candidates. -/
theorem full_signed_subset_circuit_counts :
    {a | PrimitiveCircuit a ∧ InDimension 1 a}.ncard = 1 ∧
    {a | PrimitiveCircuit a ∧ InDimension 2 a}.ncard = 5 ∧
    {a | PrimitiveCircuit a ∧ InDimension 3 a}.ncard = 41 := by
  simpa only [primitive_circuit_count] using library_counts

theorem library_max_weights :
    (∀ c ∈ library 1, ∀ i, naturalWeight c i ≤ 1) ∧
    (∀ c ∈ library 2, ∀ i, naturalWeight c i ≤ 1) ∧
    (∀ c ∈ library 3, ∀ i, naturalWeight c i ≤ 2) := by decide +kernel

theorem library_max_weights_attained :
    (∃ c ∈ library 1, ∃ i, naturalWeight c i = 1) ∧
    (∃ c ∈ library 2, ∃ i, naturalWeight c i = 1) ∧
    (∃ c ∈ library 3, ∃ i, naturalWeight c i = 2) := by decide +kernel

theorem primitive_weight_bound {d M : ℕ}
    (hbound : ∀ c ∈ library d, ∀ i, naturalWeight c i ≤ M)
    (a : Fin 14 → ℕ) (ha : PrimitiveCircuit a) (hd : InDimension d a) : ∀ i, a i ≤ M := by
  obtain ⟨c, rfl⟩ := (primitiveCircuit_iff a).mp ha
  exact hbound c (Finset.mem_filter.mpr ⟨Finset.mem_univ _, hd⟩)

/-- Classification also proves the support bounds used by finite enumeration. -/
theorem library_support_bounds : ∀ d : Fin 3, ∀ c ∈ library (d.val + 1),
    (Finset.univ.filter (fun i => naturalWeight c i ≠ 0)).card ≤ d.val + 2 := by
  decide +kernel

/-- The restricted normal library is exactly the full signed-subset universe in that dimension. -/
theorem normalLibrary_range (d : ℕ) (v : Fin 3 → ℤ) :
    (∃ i ∈ normalLibrary d, normal i = v) ↔
      v ≠ 0 ∧ ((∀ j, v j = 0 ∨ v j = 1) ∨ (∀ j, v j = 0 ∨ v j = -1)) ∧
        ∀ j : Fin 3, d ≤ j.val → v j = 0 := by
  constructor
  · rintro ⟨i, hi, rfl⟩
    exact ⟨(normal_sign i).1, (normal_sign i).2, (Finset.mem_filter.mp hi).2⟩
  · rintro ⟨hne, hsign, hd⟩
    obtain ⟨i, rfl⟩ := (normal_range v).mpr ⟨hne, hsign⟩
    exact ⟨i, Finset.mem_filter.mpr ⟨Finset.mem_univ _, hd⟩, rfl⟩

/-- A maximum is an upper bound for all primitive circuits and is attained by one. -/
def WeightMaximum (d M : ℕ) : Prop :=
  (∀ a, PrimitiveCircuit a → InDimension d a → ∀ i, a i ≤ M) ∧
    ∃ a, PrimitiveCircuit a ∧ InDimension d a ∧ ∃ i, a i = M

theorem weightMaximum_of_library {d M : ℕ}
    (hbound : ∀ c ∈ library d, ∀ i, naturalWeight c i ≤ M)
    (hattain : ∃ c ∈ library d, ∃ i, naturalWeight c i = M) : WeightMaximum d M := by
  refine ⟨fun a ha hd => primitive_weight_bound hbound a ha hd, ?_⟩
  obtain ⟨c, hc, i, hi⟩ := hattain
  exact ⟨naturalWeight c, naturalWeight_primitive c, (Finset.mem_filter.mp hc).2, i, hi⟩

/-- The exact largest primitive weights are one, one, and two. -/
theorem full_signed_subset_weight_maxima :
    WeightMaximum 1 1 ∧ WeightMaximum 2 1 ∧ WeightMaximum 3 2 :=
  ⟨weightMaximum_of_library library_max_weights.1 library_max_weights_attained.1,
    weightMaximum_of_library library_max_weights.2.1 library_max_weights_attained.2.1,
    weightMaximum_of_library library_max_weights.2.2 library_max_weights_attained.2.2⟩

/-- No support-size hypothesis was needed to classify these circuits. The usual bound follows. -/
theorem primitive_support_bound (d : Fin 3) (a : Fin 14 → ℕ)
    (ha : PrimitiveCircuit a) (hd : InDimension (d.val + 1) a) :
    (Finset.univ.filter (fun i => a i ≠ 0)).card ≤ d.val + 2 := by
  obtain ⟨c, rfl⟩ := (primitiveCircuit_iff a).mp ha
  exact library_support_bounds d c (Finset.mem_filter.mpr ⟨Finset.mem_univ _, hd⟩)

end NetworkSimplex.Threshold.UnreducedCircuits
