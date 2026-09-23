import Formal.NetworkSimplex.ThresholdSmallCompleteness
import Formal.NetworkSimplex.ThresholdClassification

/-! Complete classification of reduced positive circuits in one, two and three coordinates. -/
namespace NetworkSimplex.OneStateCircuits
open scoped BigOperators

/-- A nonzero nonnegative real dependence among the 2 reduced normals. -/
def PositiveDependence (a : Fin 2 → ℝ) : Prop :=
  (∀ i, 0 ≤ a i) ∧ (∃ i, a i ≠ 0) ∧ ∀ j, ∑ i, a i * (normal i j : ℝ) = 0

/-- Minimality is stated among all real positive dependences, without an integer bound. -/
def SupportMinimal (a : Fin 2 → ℝ) : Prop :=
  PositiveDependence a ∧ ∀ b : Fin 2 → ℝ, PositiveDependence b →
    (∀ i, b i ≠ 0 → a i ≠ 0) → ∀ i, a i ≠ 0 → b i ≠ 0

def classificationPivot : Fin 1 → Fin 2 := fun _ => 0

theorem weight_nonzero : ∀ c : Fin 1, ∃ i, weight c i ≠ 0 := by decide +kernel

theorem weight_injective : Function.Injective weight := by decide +kernel

set_option maxHeartbeats 2000000 in
-- The one-label library has one support and two coordinates.
/-- Every dependence on a listed support is a scalar multiple of the listed row. -/
theorem dependence_on_support (c : Fin 1) (a : Fin 2 → ℝ)
    (_hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0) :
    a = fun i => a (classificationPivot c) * (weight c i : ℝ) := by
  have hh := hc 0
  simp [normal, Fin.sum_univ_succ] at hh
  have he : a 1 = a 0 := by linarith
  ext i
  fin_cases i <;> simp [weight, classificationPivot, he]


/-- Each nonzero dependence supported on a library entry uses its entire support.
Together with positivity and cancellation, this is support minimality. -/
theorem minimal_support (c : Fin 1) (a : Fin 2 → ℝ)
    (hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0)
    (ha : ∃ i, a i ≠ 0) : ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
  have heq := dependence_on_support c a hs hc
  have hp : a (classificationPivot c) ≠ 0 := by
    intro hp
    obtain ⟨i, hi⟩ := ha
    have hi' := congrFun heq i
    rw [hp, zero_mul] at hi'
    exact hi hi'
  intro i
  have hi := congrFun heq i
  rw [hi, mul_ne_zero_iff]
  simp [hp]

theorem total_weight_le_five : ∀ c : Fin 1, ∑ i, weight c i ≤ 5 := by decide +kernel

theorem exists_point_of_circuit_rhs (b : Fin 2 → ℝ)
    (hb : ∀ c, 0 ≤ ∑ i, (weight c i : ℝ) * b i) :
    ∃ x : Fin 1 → ℝ, ∀ i, ∑ j, (normal i j : ℝ) * x j ≤ b i :=
  Threshold.one_full_complete b hb

/-- Every nonzero nonnegative dependence contains the unique listed support. -/
theorem positive_dependence_contains_circuit (a : Fin 2 → ℝ) (ha : PositiveDependence a) :
    ∃ c : Fin 1, ∀ i, weight c i ≠ 0 → a i ≠ 0 := by
  classical
  by_contra hn
  have hmissing (c : Fin 1) : ∃ i, weight c i ≠ 0 ∧ a i = 0 := by
    by_contra hm
    apply hn
    refine ⟨c, fun i hi => ?_⟩
    intro hai
    exact hm ⟨i, hi, hai⟩
  let r : Fin 2 → ℝ := fun i => if a i = 0 then 5 else -1
  have hr (c : Fin 1) : 0 ≤ ∑ i, (weight c i : ℝ) * r i := by
    obtain ⟨k, hk, hak⟩ := hmissing c
    have hw : (1 : ℝ) ≤ weight c k := by
      exact_mod_cast (show (1 : ℤ) ≤ weight c k by have := weight_nonnegative c k; omega)
    have htotal : (∑ i, (weight c i : ℝ)) ≤ 5 := by
      exact_mod_cast total_weight_le_five c
    have hg : ∀ i, 0 ≤ (weight c i : ℝ) * (r i + 1) := by
      intro i
      have hwi : (0 : ℝ) ≤ weight c i := by exact_mod_cast weight_nonnegative c i
      dsimp [r]
      split_ifs <;> nlinarith
    have hs := Finset.single_le_sum (fun i (_ : i ∈ Finset.univ) => hg i) (Finset.mem_univ k)
    have heq : (∑ i, (weight c i : ℝ) * (r i + 1)) =
        (∑ i, (weight c i : ℝ) * r i) + ∑ i, (weight c i : ℝ) := by
      simp only [mul_add, mul_one, Finset.sum_add_distrib]
    rw [heq] at hs
    have hrk : r k = 5 := by simp [r, hak]
    rw [hrk] at hs
    linarith
  obtain ⟨x, hx⟩ := exists_point_of_circuit_rhs r hr
  have hsum : ∑ i, a i * (∑ j, (normal i j : ℝ) * x j) ≤ ∑ i, a i * r i :=
    Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (hx i) (ha.1 i))
  have hzero : (∑ i, a i * (∑ j, (normal i j : ℝ) * x j)) = 0 := by
    simp_rw [Finset.mul_sum, ← mul_assoc]
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, ha.2.2, zero_mul]
    simp
  have heq : ∀ i, a i * r i = -a i := by
    intro i
    dsimp [r]
    split_ifs with hi
    · simp [hi]
    · ring
  rw [hzero] at hsum
  simp_rw [heq, Finset.sum_neg_distrib] at hsum
  obtain ⟨k, hk⟩ := ha.2.1
  have hkpos : 0 < a k := lt_of_le_of_ne (ha.1 k) (Ne.symm hk)
  have ht := Finset.single_le_sum (fun i (_ : i ∈ Finset.univ) => ha.1 i) (Finset.mem_univ k)
  linarith

/-- Each table entry is a genuine positive dependence over the reals. -/
theorem weight_positive_dependence (c : Fin 1) :
    PositiveDependence (fun i => (weight c i : ℝ)) := by
  refine ⟨fun i => by dsimp only; exact_mod_cast weight_nonnegative c i, ?_, ?_⟩
  · obtain ⟨i, hi⟩ := weight_nonzero c
    exact ⟨i, by dsimp only; exact_mod_cast hi⟩
  · intro j
    dsimp only
    exact_mod_cast normal_cancellation c j

/-- No smaller positive support exists inside a listed support. -/
theorem weight_supportMinimal (c : Fin 1) : SupportMinimal (fun i => (weight c i : ℝ)) := by
  refine ⟨weight_positive_dependence c, ?_⟩
  intro b hb hs i hi
  have hsub : ∀ k, weight c k = 0 → b k = 0 := by
    intro k hk
    by_contra hbk
    have hh := hs k hbk
    simp [hk] at hh
  dsimp only at hi
  exact (minimal_support c b hsub hb.2.2 hb.2.1 i).mpr (by exact_mod_cast hi)

/-- Exact classification: every real support-minimal positive dependence is a
positive scalar multiple of a listed circuit, with no presupposed rationality. -/
theorem supportMinimal_classification (a : Fin 2 → ℝ) (ha : SupportMinimal a) :
    ∃ c : Fin 1, ∃ t : ℝ, 0 < t ∧ ∀ i, a i = t * (weight c i : ℝ) := by
  obtain ⟨c, hc⟩ := positive_dependence_contains_circuit a ha.1
  have hrev := ha.2 (fun i => (weight c i : ℝ)) (weight_positive_dependence c)
    (fun i hi => hc i (by exact_mod_cast hi))
  have hs : ∀ i, weight c i = 0 → a i = 0 := by
    intro i hi
    by_contra hai
    have hh := hrev i hai
    simp [hi] at hh
  have heq := dependence_on_support c a hs ha.1.2.2
  obtain ⟨k, hk⟩ := weight_nonzero c
  have hapos : 0 < a k := lt_of_le_of_ne (ha.1.1 k) (Ne.symm (hc k hk))
  have hweight : (0 : ℝ) < weight c k := by
    exact_mod_cast (lt_of_le_of_ne (weight_nonnegative c k) (Ne.symm hk))
  obtain ⟨t, ht⟩ : ∃ t : ℝ, a = fun i => t * (weight c i : ℝ) := ⟨_, heq⟩
  refine ⟨c, t, ?_, fun i => congrFun ht i⟩
  have hk' := congrFun ht k
  nlinarith

/-- Circuit supports, counted without duplicates or ray-scaling ambiguity. -/
def circuitSupport (c : Fin 1) : Finset (Fin 2) := Finset.univ.filter (fun i => weight c i ≠ 0)

theorem circuitSupport_injective : Function.Injective circuitSupport := by decide +kernel

def circuitSupports : Finset (Finset (Fin 2)) := Finset.univ.image circuitSupport

/-- Exactly one support occurs in the complete circuit library. -/
theorem circuitSupports_card : circuitSupports.card = 1 := by
  rw [circuitSupports, Finset.card_image_of_injective _ circuitSupport_injective]
  decide

/-- The listed rows are 2 distinct normal directions. -/
theorem normal_injective : Function.Injective normal := by decide +kernel

theorem normal_count : (Finset.univ.image normal).card = 2 := by
  rw [Finset.card_image_of_injective _ normal_injective]
  decide

/-- The finite list is exactly the supports of all real positive minimal dependences. -/
theorem mem_circuitSupports_iff (S : Finset (Fin 2)) :
    S ∈ circuitSupports ↔ ∃ a : Fin 2 → ℝ, SupportMinimal a ∧
      ∀ i, i ∈ S ↔ a i ≠ 0 := by
  constructor
  · intro h
    obtain ⟨c, _, rfl⟩ := Finset.mem_image.mp h
    refine ⟨fun i => (weight c i : ℝ), weight_supportMinimal c, ?_⟩
    intro i
    simp [circuitSupport]
  · rintro ⟨a, ha, hS⟩
    obtain ⟨c, t, ht, he⟩ := supportMinimal_classification a ha
    apply Finset.mem_image.mpr
    refine ⟨c, Finset.mem_univ _, ?_⟩
    ext i
    rw [hS i, he i]
    simp [circuitSupport, ne_of_gt ht]

/-- A positive minimal dependence has a unique listed support. -/
theorem supportMinimal_unique_support (a : Fin 2 → ℝ) (ha : SupportMinimal a) :
    ∃! c : Fin 1, ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
  obtain ⟨c, t, ht, he⟩ := supportMinimal_classification a ha
  have hc : ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
    intro i
    rw [he i]
    simp [ne_of_gt ht]
  refine ⟨c, hc, ?_⟩
  intro d hd
  apply circuitSupport_injective
  ext i
  simp only [circuitSupport, Finset.mem_filter, Finset.mem_univ, true_and]
  exact (hd i).symm.trans (hc i)

end NetworkSimplex.OneStateCircuits

namespace NetworkSimplex.TwoStateCircuits
open scoped BigOperators

/-- A nonzero nonnegative real dependence among the 6 reduced normals. -/
def PositiveDependence (a : Fin 6 → ℝ) : Prop :=
  (∀ i, 0 ≤ a i) ∧ (∃ i, a i ≠ 0) ∧ ∀ j, ∑ i, a i * (normal i j : ℝ) = 0

/-- Minimality is stated among all real positive dependences, without an integer bound. -/
def SupportMinimal (a : Fin 6 → ℝ) : Prop :=
  PositiveDependence a ∧ ∀ b : Fin 6 → ℝ, PositiveDependence b →
    (∀ i, b i ≠ 0 → a i ≠ 0) → ∀ i, a i ≠ 0 → b i ≠ 0

def classificationPivot : Fin 5 → Fin 6 := ![0, 1, 2, 0, 2]

set_option maxHeartbeats 2000000 in
-- Expanding the five supports requires 30 scalar coordinate checks.
/-- Every dependence on a listed support is a scalar multiple of the listed row. -/
theorem dependence_on_support (c : Fin 5) (a : Fin 6 → ℝ)
    (hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0) :
    a = fun i => a (classificationPivot c) * (weight c i : ℝ) := by
  fin_cases c <;>
    (simp only [Fin.forall_fin_succ] at hs hc
     simp [weight, normal, Fin.sum_univ_succ] at hs hc
     ext i
     fin_cases i <;> simp [weight, classificationPivot] <;> simp_all <;> linarith)

/-- Each nonzero dependence supported on a library entry uses its entire support.
Together with positivity and cancellation, this is support minimality. -/
theorem minimal_support (c : Fin 5) (a : Fin 6 → ℝ)
    (hs : ∀ i, weight c i = 0 → a i = 0)
    (hc : ∀ j, ∑ i, a i * (normal i j : ℝ) = 0)
    (ha : ∃ i, a i ≠ 0) : ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
  have heq := dependence_on_support c a hs hc
  have hp : a (classificationPivot c) ≠ 0 := by
    intro hp
    obtain ⟨i, hi⟩ := ha
    have hi' := congrFun heq i
    rw [hp, zero_mul] at hi'
    exact hi hi'
  intro i
  have hi := congrFun heq i
  rw [hi, mul_ne_zero_iff]
  simp [hp]

theorem total_weight_le_five : ∀ c : Fin 5, ∑ i, weight c i ≤ 5 := by decide +kernel

theorem exists_point_of_circuit_rhs (b : Fin 6 → ℝ)
    (hb : ∀ c, 0 ≤ ∑ i, (weight c i : ℝ) * b i) :
    ∃ x : Fin 2 → ℝ, ∀ i, ∑ j, (normal i j : ℝ) * x j ≤ b i :=
  Threshold.two_full_complete b hb

/-- Every nonzero nonnegative dependence contains one of the 5 listed supports. -/
theorem positive_dependence_contains_circuit (a : Fin 6 → ℝ) (ha : PositiveDependence a) :
    ∃ c : Fin 5, ∀ i, weight c i ≠ 0 → a i ≠ 0 := by
  classical
  by_contra hn
  have hmissing (c : Fin 5) : ∃ i, weight c i ≠ 0 ∧ a i = 0 := by
    by_contra hm
    apply hn
    refine ⟨c, fun i hi => ?_⟩
    intro hai
    exact hm ⟨i, hi, hai⟩
  let r : Fin 6 → ℝ := fun i => if a i = 0 then 5 else -1
  have hr (c : Fin 5) : 0 ≤ ∑ i, (weight c i : ℝ) * r i := by
    obtain ⟨k, hk, hak⟩ := hmissing c
    have hw : (1 : ℝ) ≤ weight c k := by
      exact_mod_cast (show (1 : ℤ) ≤ weight c k by have := weight_nonnegative c k; omega)
    have htotal : (∑ i, (weight c i : ℝ)) ≤ 5 := by
      exact_mod_cast total_weight_le_five c
    have hg : ∀ i, 0 ≤ (weight c i : ℝ) * (r i + 1) := by
      intro i
      have hwi : (0 : ℝ) ≤ weight c i := by exact_mod_cast weight_nonnegative c i
      dsimp [r]
      split_ifs <;> nlinarith
    have hs := Finset.single_le_sum (fun i (_ : i ∈ Finset.univ) => hg i) (Finset.mem_univ k)
    have heq : (∑ i, (weight c i : ℝ) * (r i + 1)) =
        (∑ i, (weight c i : ℝ) * r i) + ∑ i, (weight c i : ℝ) := by
      simp only [mul_add, mul_one, Finset.sum_add_distrib]
    rw [heq] at hs
    have hrk : r k = 5 := by simp [r, hak]
    rw [hrk] at hs
    linarith
  obtain ⟨x, hx⟩ := exists_point_of_circuit_rhs r hr
  have hsum : ∑ i, a i * (∑ j, (normal i j : ℝ) * x j) ≤ ∑ i, a i * r i :=
    Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (hx i) (ha.1 i))
  have hzero : (∑ i, a i * (∑ j, (normal i j : ℝ) * x j)) = 0 := by
    simp_rw [Finset.mul_sum, ← mul_assoc]
    rw [Finset.sum_comm]
    simp_rw [← Finset.sum_mul, ha.2.2, zero_mul]
    simp
  have heq : ∀ i, a i * r i = -a i := by
    intro i
    dsimp [r]
    split_ifs with hi
    · simp [hi]
    · ring
  rw [hzero] at hsum
  simp_rw [heq, Finset.sum_neg_distrib] at hsum
  obtain ⟨k, hk⟩ := ha.2.1
  have hkpos : 0 < a k := lt_of_le_of_ne (ha.1 k) (Ne.symm hk)
  have ht := Finset.single_le_sum (fun i (_ : i ∈ Finset.univ) => ha.1 i) (Finset.mem_univ k)
  linarith

/-- Each table entry is a genuine positive dependence over the reals. -/
theorem weight_positive_dependence (c : Fin 5) :
    PositiveDependence (fun i => (weight c i : ℝ)) := by
  refine ⟨fun i => by dsimp only; exact_mod_cast weight_nonnegative c i, ?_, ?_⟩
  · obtain ⟨i, hi⟩ := weight_nonzero c
    exact ⟨i, by dsimp only; exact_mod_cast hi⟩
  · intro j
    dsimp only
    exact_mod_cast normal_cancellation c j

/-- No smaller positive support exists inside a listed support. -/
theorem weight_supportMinimal (c : Fin 5) : SupportMinimal (fun i => (weight c i : ℝ)) := by
  refine ⟨weight_positive_dependence c, ?_⟩
  intro b hb hs i hi
  have hsub : ∀ k, weight c k = 0 → b k = 0 := by
    intro k hk
    by_contra hbk
    have hh := hs k hbk
    simp [hk] at hh
  dsimp only at hi
  exact (minimal_support c b hsub hb.2.2 hb.2.1 i).mpr (by exact_mod_cast hi)

/-- Exact classification: every real support-minimal positive dependence is a
positive scalar multiple of a listed circuit, with no presupposed rationality. -/
theorem supportMinimal_classification (a : Fin 6 → ℝ) (ha : SupportMinimal a) :
    ∃ c : Fin 5, ∃ t : ℝ, 0 < t ∧ ∀ i, a i = t * (weight c i : ℝ) := by
  obtain ⟨c, hc⟩ := positive_dependence_contains_circuit a ha.1
  have hrev := ha.2 (fun i => (weight c i : ℝ)) (weight_positive_dependence c)
    (fun i hi => hc i (by exact_mod_cast hi))
  have hs : ∀ i, weight c i = 0 → a i = 0 := by
    intro i hi
    by_contra hai
    have hh := hrev i hai
    simp [hi] at hh
  have heq := dependence_on_support c a hs ha.1.2.2
  obtain ⟨k, hk⟩ := weight_nonzero c
  have hapos : 0 < a k := lt_of_le_of_ne (ha.1.1 k) (Ne.symm (hc k hk))
  have hweight : (0 : ℝ) < weight c k := by
    exact_mod_cast (lt_of_le_of_ne (weight_nonnegative c k) (Ne.symm hk))
  obtain ⟨t, ht⟩ : ∃ t : ℝ, a = fun i => t * (weight c i : ℝ) := ⟨_, heq⟩
  refine ⟨c, t, ?_, fun i => congrFun ht i⟩
  have hk' := congrFun ht k
  nlinarith

/-- Circuit supports, counted without duplicates or ray-scaling ambiguity. -/
def circuitSupport (c : Fin 5) : Finset (Fin 6) := Finset.univ.filter (fun i => weight c i ≠ 0)

theorem circuitSupport_injective : Function.Injective circuitSupport := by decide +kernel

def circuitSupports : Finset (Finset (Fin 6)) := Finset.univ.image circuitSupport

/-- Exactly five different supports occur in the complete circuit library. -/
theorem circuitSupports_card : circuitSupports.card = 5 := by
  rw [circuitSupports, Finset.card_image_of_injective _ circuitSupport_injective]
  decide

theorem normal_count : (Finset.univ.image normal).card = 6 := by
  rw [Finset.card_image_of_injective _ normal_injective]
  decide

/-- The finite list is exactly the supports of all real positive minimal dependences. -/
theorem mem_circuitSupports_iff (S : Finset (Fin 6)) :
    S ∈ circuitSupports ↔ ∃ a : Fin 6 → ℝ, SupportMinimal a ∧
      ∀ i, i ∈ S ↔ a i ≠ 0 := by
  constructor
  · intro h
    obtain ⟨c, _, rfl⟩ := Finset.mem_image.mp h
    refine ⟨fun i => (weight c i : ℝ), weight_supportMinimal c, ?_⟩
    intro i
    simp [circuitSupport]
  · rintro ⟨a, ha, hS⟩
    obtain ⟨c, t, ht, he⟩ := supportMinimal_classification a ha
    apply Finset.mem_image.mpr
    refine ⟨c, Finset.mem_univ _, ?_⟩
    ext i
    rw [hS i, he i]
    simp [circuitSupport, ne_of_gt ht]

/-- A positive minimal dependence has a unique listed support. -/
theorem supportMinimal_unique_support (a : Fin 6 → ℝ) (ha : SupportMinimal a) :
    ∃! c : Fin 5, ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
  obtain ⟨c, t, ht, he⟩ := supportMinimal_classification a ha
  have hc : ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
    intro i
    rw [he i]
    simp [ne_of_gt ht]
  refine ⟨c, hc, ?_⟩
  intro d hd
  apply circuitSupport_injective
  ext i
  simp only [circuitSupport, Finset.mem_filter, Finset.mem_univ, true_and]
  exact (hd i).symm.trans (hc i)

end NetworkSimplex.TwoStateCircuits

namespace NetworkSimplex.OneStateCircuits
open scoped BigOperators

theorem classificationPivot_weight : ∀ c, weight c (classificationPivot c) = 1 := by
  decide +kernel

def naturalWeight (c : Fin 1) (i : Fin 2) : ℕ := (weight c i).toNat

@[simp] theorem naturalWeight_cast (c : Fin 1) (i : Fin 2) :
    (naturalWeight c i : ℝ) = (weight c i : ℝ) := by
  rw [naturalWeight, ← Int.cast_natCast, Int.toNat_of_nonneg (weight_nonnegative c i)]

@[simp] theorem naturalWeight_pivot (c : Fin 1) : naturalWeight c (classificationPivot c) = 1 := by
  simp [naturalWeight, classificationPivot_weight]

/-- The gcd normalization is over all natural weights, without an a priori bound. -/
def PrimitiveCircuit (a : Fin 2 → ℕ) : Prop :=
  SupportMinimal (fun i => (a i : ℝ)) ∧ Finset.univ.gcd a = 1

theorem naturalWeight_primitive (c : Fin 1) : PrimitiveCircuit (naturalWeight c) := by
  constructor
  · simpa only [naturalWeight_cast] using weight_supportMinimal c
  · have h := Finset.gcd_dvd (f := naturalWeight c) (Finset.mem_univ (classificationPivot c))
    rw [naturalWeight_pivot] at h
    exact Nat.dvd_one.mp h

/-- Every primitive positive circuit is exactly one listed integer vector. -/
theorem primitiveCircuit_iff (a : Fin 2 → ℕ) :
    PrimitiveCircuit a ↔ ∃ c : Fin 1, a = naturalWeight c := by
  constructor
  · intro ha
    obtain ⟨c, t, _, he⟩ := supportMinimal_classification (fun i => (a i : ℝ)) ha.1
    have hp : (a (classificationPivot c) : ℝ) = t := by
      simpa only [classificationPivot_weight, Int.cast_one, mul_one] using
        he (classificationPivot c)
    have hn (i : Fin 2) : a i = a (classificationPivot c) * naturalWeight c i := by
      have h := he i
      rw [← hp, ← naturalWeight_cast] at h
      exact_mod_cast h
    have hd : a (classificationPivot c) ∣ Finset.univ.gcd a := by
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

/-- All primitive positive circuits form exactly this finite image. -/
theorem primitive_circuits_exact :
    {a | PrimitiveCircuit a} = ↑(Finset.univ.image naturalWeight) := by
  ext a
  simp only [Set.mem_ofPred_eq, Finset.mem_coe, Finset.mem_image,
    Finset.mem_univ, true_and, primitiveCircuit_iff]
  exact exists_congr (fun _ => eq_comm)

/-- Count of all primitive circuits, including completeness over unbounded weights. -/
theorem primitive_circuit_count : {a | PrimitiveCircuit a}.ncard = 1 := by
  rw [primitive_circuits_exact, Set.ncard_coe_finset,
    Finset.card_image_of_injective _ naturalWeight_injective]
  decide

theorem library_weight_bound : ∀ c i, naturalWeight c i ≤ 1 := by decide +kernel

theorem library_weight_attained : ∃ c i, naturalWeight c i = 1 := by decide +kernel

/-- The exact largest primitive weight is 1. -/
theorem primitive_weight_maximum :
    (∀ a, PrimitiveCircuit a → ∀ i, a i ≤ 1) ∧
      ∃ a, PrimitiveCircuit a ∧ ∃ i, a i = 1 := by
  constructor
  · intro a ha
    obtain ⟨c, rfl⟩ := (primitiveCircuit_iff a).mp ha
    exact library_weight_bound c
  · obtain ⟨c, i, hi⟩ := library_weight_attained
    exact ⟨naturalWeight c, naturalWeight_primitive c, i, hi⟩

end NetworkSimplex.OneStateCircuits

namespace NetworkSimplex.TwoStateCircuits
open scoped BigOperators

theorem classificationPivot_weight : ∀ c, weight c (classificationPivot c) = 1 := by
  decide +kernel

def naturalWeight (c : Fin 5) (i : Fin 6) : ℕ := (weight c i).toNat

@[simp] theorem naturalWeight_cast (c : Fin 5) (i : Fin 6) :
    (naturalWeight c i : ℝ) = (weight c i : ℝ) := by
  rw [naturalWeight, ← Int.cast_natCast, Int.toNat_of_nonneg (weight_nonnegative c i)]

@[simp] theorem naturalWeight_pivot (c : Fin 5) : naturalWeight c (classificationPivot c) = 1 := by
  simp [naturalWeight, classificationPivot_weight]

/-- The gcd normalization is over all natural weights, without an a priori bound. -/
def PrimitiveCircuit (a : Fin 6 → ℕ) : Prop :=
  SupportMinimal (fun i => (a i : ℝ)) ∧ Finset.univ.gcd a = 1

theorem naturalWeight_primitive (c : Fin 5) : PrimitiveCircuit (naturalWeight c) := by
  constructor
  · simpa only [naturalWeight_cast] using weight_supportMinimal c
  · have h := Finset.gcd_dvd (f := naturalWeight c) (Finset.mem_univ (classificationPivot c))
    rw [naturalWeight_pivot] at h
    exact Nat.dvd_one.mp h

/-- Every primitive positive circuit is exactly one listed integer vector. -/
theorem primitiveCircuit_iff (a : Fin 6 → ℕ) :
    PrimitiveCircuit a ↔ ∃ c : Fin 5, a = naturalWeight c := by
  constructor
  · intro ha
    obtain ⟨c, t, _, he⟩ := supportMinimal_classification (fun i => (a i : ℝ)) ha.1
    have hp : (a (classificationPivot c) : ℝ) = t := by
      simpa only [classificationPivot_weight, Int.cast_one, mul_one] using
        he (classificationPivot c)
    have hn (i : Fin 6) : a i = a (classificationPivot c) * naturalWeight c i := by
      have h := he i
      rw [← hp, ← naturalWeight_cast] at h
      exact_mod_cast h
    have hd : a (classificationPivot c) ∣ Finset.univ.gcd a := by
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

/-- All primitive positive circuits form exactly this finite image. -/
theorem primitive_circuits_exact :
    {a | PrimitiveCircuit a} = ↑(Finset.univ.image naturalWeight) := by
  ext a
  simp only [Set.mem_ofPred_eq, Finset.mem_coe, Finset.mem_image,
    Finset.mem_univ, true_and, primitiveCircuit_iff]
  exact exists_congr (fun _ => eq_comm)

/-- Count of all primitive circuits, including completeness over unbounded weights. -/
theorem primitive_circuit_count : {a | PrimitiveCircuit a}.ncard = 5 := by
  rw [primitive_circuits_exact, Set.ncard_coe_finset,
    Finset.card_image_of_injective _ naturalWeight_injective]
  decide

theorem library_weight_bound : ∀ c i, naturalWeight c i ≤ 1 := by decide +kernel

theorem library_weight_attained : ∃ c i, naturalWeight c i = 1 := by decide +kernel

/-- The exact largest primitive weight is 1. -/
theorem primitive_weight_maximum :
    (∀ a, PrimitiveCircuit a → ∀ i, a i ≤ 1) ∧
      ∃ a, PrimitiveCircuit a ∧ ∃ i, a i = 1 := by
  constructor
  · intro a ha
    obtain ⟨c, rfl⟩ := (primitiveCircuit_iff a).mp ha
    exact library_weight_bound c
  · obtain ⟨c, i, hi⟩ := library_weight_attained
    exact ⟨naturalWeight c, naturalWeight_primitive c, i, hi⟩

end NetworkSimplex.TwoStateCircuits

namespace NetworkSimplex.ThreeStateCircuits
open scoped BigOperators

def classificationPivot : Fin 16 → Fin 11 :=
  ![0, 1, 2, 3, 4, 5, 6, 6, 0, 1, 2, 0, 3, 3, 4, 3]

theorem classificationPivot_weight : ∀ c, weight c (classificationPivot c) = 1 := by
  decide +kernel

def naturalWeight (c : Fin 16) (i : Fin 11) : ℕ := (weight c i).toNat

@[simp] theorem naturalWeight_cast (c : Fin 16) (i : Fin 11) :
    (naturalWeight c i : ℝ) = (weight c i : ℝ) := by
  rw [naturalWeight, ← Int.cast_natCast, Int.toNat_of_nonneg (weight_nonnegative c i)]

@[simp] theorem naturalWeight_pivot (c : Fin 16) : naturalWeight c (classificationPivot c) = 1 := by
  simp [naturalWeight, classificationPivot_weight]

/-- The gcd normalization is over all natural weights, without an a priori bound. -/
def PrimitiveCircuit (a : Fin 11 → ℕ) : Prop :=
  SupportMinimal (fun i => (a i : ℝ)) ∧ Finset.univ.gcd a = 1

theorem naturalWeight_primitive (c : Fin 16) : PrimitiveCircuit (naturalWeight c) := by
  constructor
  · simpa only [naturalWeight_cast] using weight_supportMinimal c
  · have h := Finset.gcd_dvd (f := naturalWeight c) (Finset.mem_univ (classificationPivot c))
    rw [naturalWeight_pivot] at h
    exact Nat.dvd_one.mp h

/-- Every primitive positive circuit is exactly one listed integer vector. -/
theorem primitiveCircuit_iff (a : Fin 11 → ℕ) :
    PrimitiveCircuit a ↔ ∃ c : Fin 16, a = naturalWeight c := by
  constructor
  · intro ha
    obtain ⟨c, t, _, he⟩ := supportMinimal_classification (fun i => (a i : ℝ)) ha.1
    have hp : (a (classificationPivot c) : ℝ) = t := by
      simpa only [classificationPivot_weight, Int.cast_one, mul_one] using
        he (classificationPivot c)
    have hn (i : Fin 11) : a i = a (classificationPivot c) * naturalWeight c i := by
      have h := he i
      rw [← hp, ← naturalWeight_cast] at h
      exact_mod_cast h
    have hd : a (classificationPivot c) ∣ Finset.univ.gcd a := by
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

/-- All primitive positive circuits form exactly this finite image. -/
theorem primitive_circuits_exact :
    {a | PrimitiveCircuit a} = ↑(Finset.univ.image naturalWeight) := by
  ext a
  simp only [Set.mem_ofPred_eq, Finset.mem_coe, Finset.mem_image,
    Finset.mem_univ, true_and, primitiveCircuit_iff]
  exact exists_congr (fun _ => eq_comm)

/-- Count of all primitive circuits, including completeness over unbounded weights. -/
theorem primitive_circuit_count : {a | PrimitiveCircuit a}.ncard = 16 := by
  rw [primitive_circuits_exact, Set.ncard_coe_finset,
    Finset.card_image_of_injective _ naturalWeight_injective]
  decide

theorem library_weight_bound : ∀ c i, naturalWeight c i ≤ 2 := by decide +kernel

theorem library_weight_attained : ∃ c i, naturalWeight c i = 2 := by decide +kernel

/-- The exact largest primitive weight is 2. -/
theorem primitive_weight_maximum :
    (∀ a, PrimitiveCircuit a → ∀ i, a i ≤ 2) ∧
      ∃ a, PrimitiveCircuit a ∧ ∃ i, a i = 2 := by
  constructor
  · intro a ha
    obtain ⟨c, rfl⟩ := (primitiveCircuit_iff a).mp ha
    exact library_weight_bound c
  · obtain ⟨c, i, hi⟩ := library_weight_attained
    exact ⟨naturalWeight c, naturalWeight_primitive c, i, hi⟩

end NetworkSimplex.ThreeStateCircuits

namespace NetworkSimplex.Threshold

/-- The reduced libraries have exactly one, five and sixteen primitive positive circuits. -/
theorem reduced_primitive_circuit_counts :
    {a | OneStateCircuits.PrimitiveCircuit a}.ncard = 1 ∧
    {a | TwoStateCircuits.PrimitiveCircuit a}.ncard = 5 ∧
    {a | ThreeStateCircuits.PrimitiveCircuit a}.ncard = 16 :=
  ⟨OneStateCircuits.primitive_circuit_count, TwoStateCircuits.primitive_circuit_count,
    ThreeStateCircuits.primitive_circuit_count⟩

end NetworkSimplex.Threshold
