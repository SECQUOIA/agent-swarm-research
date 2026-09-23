import Formal.NetworkSimplex.ThresholdOccurrence

/-! Completeness of the reduced three-state positive-circuit library. -/
namespace NetworkSimplex.ThreeStateCircuits
open scoped BigOperators

/-- A nonzero nonnegative real dependence among the eleven reduced normals. -/
def PositiveDependence (a : Fin 11 → ℝ) : Prop :=
  (∀ i, 0 ≤ a i) ∧ (∃ i, a i ≠ 0) ∧ ∀ j, ∑ i, a i * (normal i j : ℝ) = 0

/-- Minimality is stated among all real positive dependences, without an integer bound. -/
def SupportMinimal (a : Fin 11 → ℝ) : Prop :=
  PositiveDependence a ∧ ∀ b : Fin 11 → ℝ, PositiveDependence b →
    (∀ i, b i ≠ 0 → a i ≠ 0) → ∀ i, a i ≠ 0 → b i ≠ 0

def boundsOfRhs (r : Fin 11 → ℝ) : ThreeStateBounds :=
  ⟨-r 7, -r 8, -r 9, -r 10, r 0, r 1, r 2, r 3, r 4, r 5, r 6⟩

@[simp] theorem rhs_boundsOfRhs (r : Fin 11 → ℝ) : rhs (boundsOfRhs r) = r := by
  funext i
  fin_cases i <;> simp [rhs, boundsOfRhs]

/-- The existing sixteen-test feasibility theorem applies to arbitrary eleven right sides. -/
theorem exists_point_of_circuit_rhs (r : Fin 11 → ℝ)
    (hr : ∀ c, 0 ≤ ∑ i, (weight c i : ℝ) * r i) :
    ∃ x : Fin 3 → ℝ, ∀ i, ∑ j, (normal i j : ℝ) * x j ≤ r i := by
  have htests : CircuitTests (boundsOfRhs r) := by
    intro c
    rw [rhs_boundsOfRhs]
    exact hr c
  obtain ⟨x, y, z, hh⟩ := (circuit_tests_iff_feasible _).mp htests
  refine ⟨![x, y, z], ?_⟩
  intro i
  rcases hh with ⟨h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11⟩
  fin_cases i <;> simp [normal, boundsOfRhs, Fin.sum_univ_succ] at * <;> linarith

/-- Every nonzero nonnegative dependence contains one of the sixteen listed supports. -/
theorem positive_dependence_contains_circuit (a : Fin 11 → ℝ) (ha : PositiveDependence a) :
    ∃ c : Fin 16, ∀ i, weight c i ≠ 0 → a i ≠ 0 := by
  classical
  by_contra hn
  have hmissing (c : Fin 16) : ∃ i, weight c i ≠ 0 ∧ a i = 0 := by
    by_contra hm
    apply hn
    refine ⟨c, fun i hi => ?_⟩
    intro hai
    exact hm ⟨i, hi, hai⟩
  let r : Fin 11 → ℝ := fun i => if a i = 0 then 5 else -1
  have hr (c : Fin 16) : 0 ≤ ∑ i, (weight c i : ℝ) * r i := by
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
theorem weight_positive_dependence (c : Fin 16) :
    PositiveDependence (fun i => (weight c i : ℝ)) := by
  refine ⟨fun i => by dsimp only; exact_mod_cast weight_nonnegative c i, ?_, ?_⟩
  · obtain ⟨i, hi⟩ := weight_nonzero c
    exact ⟨i, by dsimp only; exact_mod_cast hi⟩
  · intro j
    dsimp only
    exact_mod_cast normal_cancellation c j

/-- No smaller positive support exists inside a listed support. -/
theorem weight_supportMinimal (c : Fin 16) : SupportMinimal (fun i => (weight c i : ℝ)) := by
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
theorem supportMinimal_classification (a : Fin 11 → ℝ) (ha : SupportMinimal a) :
    ∃ c : Fin 16, ∃ t : ℝ, 0 < t ∧ ∀ i, a i = t * (weight c i : ℝ) := by
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
def circuitSupport (c : Fin 16) : Finset (Fin 11) := Finset.univ.filter (fun i => weight c i ≠ 0)

theorem circuitSupport_injective : Function.Injective circuitSupport := by decide +kernel

def circuitSupports : Finset (Finset (Fin 11)) := Finset.univ.image circuitSupport

/-- Exactly sixteen different supports occur in the complete circuit library. -/
theorem circuitSupports_card : circuitSupports.card = 16 := by
  rw [circuitSupports, Finset.card_image_of_injective _ circuitSupport_injective]
  decide

/-- The listed rows are eleven distinct normal directions. -/
theorem normal_injective : Function.Injective normal := by decide +kernel

theorem normal_count : (Finset.univ.image normal).card = 11 := by
  rw [Finset.card_image_of_injective _ normal_injective]
  decide

/-- The finite list is exactly the supports of all real positive minimal dependences. -/
theorem mem_circuitSupports_iff (S : Finset (Fin 11)) :
    S ∈ circuitSupports ↔ ∃ a : Fin 11 → ℝ, SupportMinimal a ∧
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
theorem supportMinimal_unique_support (a : Fin 11 → ℝ) (ha : SupportMinimal a) :
    ∃! c : Fin 16, ∀ i, a i ≠ 0 ↔ weight c i ≠ 0 := by
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

end NetworkSimplex.ThreeStateCircuits
