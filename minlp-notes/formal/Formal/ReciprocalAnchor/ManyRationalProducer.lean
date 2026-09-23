import Formal.ReciprocalAnchor.ManyRationalSelector
import Formal.ReciprocalAnchor.ManyRationalMixCall

/-! An executable finite rational-law to graph-witness producer. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

def mixedMass {K : ℕ} (p x : Fin K → ℚ) (a b m t : ℚ) (i : Fin (K + 2)) : ℚ :=
  rationalMixMass p a b m t (∑ j, p j / x j) (finSumFinEquiv.symm i)

def mixedLocation {K : ℕ} (x : Fin K → ℚ) (a b : ℚ) (i : Fin (K + 2)) : ℚ :=
  rationalMixLocation x a b (finSumFinEquiv.symm i)

/-- Each output leaf is a complete rational list, with a proved-successful optional result. -/
def rationalWitnessProducer {K n : ℕ} (p x : Fin K → ℚ) (a b m t : ℚ)
    (q w : Fin n → ℚ) : Fin n → Option (List ℚ) × ℕ :=
  fun j => rationalSelectorCounted (mixedMass p x a b m t) (mixedLocation x a b) (q j) (w j)

private theorem sum_reindex {K : ℕ} (f : Fin K ⊕ Fin 2 → ℚ) :
    (∑ i : Fin (K + 2), f (finSumFinEquiv.symm i)) = ∑ i, f i :=
  Equiv.sum_comp finSumFinEquiv.symm f

/-- The actual mixed arrays form a probability law with the prescribed two moments. -/
theorem mixedLaw_spec {K : ℕ} (p x : Fin K → ℚ) {a b m t : ℚ}
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hm : ∑ i, p i * x i = m)
    (ha : 0 < a) (hab : a < b) (hmab : a ≤ m ∧ m ≤ b)
    (hT : (∑ i, p i / x i) ≤ t) (ht : t ≤ rationalSecant a b m) :
    (∀ i, 0 ≤ mixedMass p x a b m t i) ∧
      (∑ i, mixedMass p x a b m t i = 1) ∧
      (∀ i, a ≤ mixedLocation x a b i ∧ mixedLocation x a b i ≤ b) ∧
      (∑ i, mixedMass p x a b m t i * mixedLocation x a b i = m) ∧
      (∑ i, mixedMass p x a b m t i / mixedLocation x a b i = t) := by
  refine ⟨fun i => rationalMixMass_nonneg p hp hab hmab hT ht _, ?_,
    fun i => rationalMixLocation_bounds x hx hab.le _, ?_, ?_⟩
  · unfold mixedMass
    rw [sum_reindex]
    exact rationalMixMass_total p hp1 hab
  · unfold mixedMass mixedLocation
    rw [sum_reindex (fun i => rationalMixMass p a b m t (∑ j, p j / x j) i *
      rationalMixLocation x a b i)]
    exact rationalMix_mean p x hm hab
  · unfold mixedMass mixedLocation
    rw [sum_reindex (fun i => rationalMixMass p a b m t (∑ j, p j / x j) i /
      rationalMixLocation x a b i)]
    exact rationalMix_reciprocal p x rfl ha hab hT ht

/-- The executable producer succeeds on every leaf realizable by the input law. -/
theorem rationalWitnessProducer_spec {K n B : ℕ} (p x : Fin K → ℚ) {a b m t : ℚ}
    (q w : Fin n → ℚ) (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hm : ∑ i, p i * x i = m)
    (ha : 0 < a) (hab : a < b) (hmab : a ≤ m ∧ m ≤ b)
    (hT : (∑ i, p i / x i) ≤ t) (ht : t ≤ rationalSecant a b m)
    (hq : ∀ j, 0 ≤ q j ∧ q j ≤ 1)
    (hcall : ∀ j s, w j - q j * s ≤ selectionCall p x s ∧
      m - w j - (1 - q j) * s ≤ selectionCall p x s)
    (hpB : ∀ i, RationalBits (mixedMass p x a b m t i) B)
    (hxB : ∀ i, RationalBits (mixedLocation x a b i) B)
    (hqB : ∀ j, RationalBits (q j) B) (hwB : ∀ j, RationalBits (w j) B) :
    ∃ θ : Fin n → Fin (K + 2) → ℚ, ∀ j,
      (rationalWitnessProducer p x a b m t q w j).1 = some (List.ofFn (θ j)) ∧
      (∀ i, θ j i ∈ Set.Icc (0 : ℚ) 1) ∧
      (∑ i, mixedMass p x a b m t i * θ j i = q j) ∧
      (∑ i, mixedMass p x a b m t i * mixedLocation x a b i * θ j i = w j) ∧
      ∀ i, RationalBits (θ j i) (witnessBits (K + 2) B) := by
  obtain ⟨hp', hp1', _, hm', _⟩ := mixedLaw_spec p x hp hp1 hx hm ha hab hmab hT ht
  apply rationalAllSelectors_spec _ _ hp' hp1' q w _ hpB hxB hqB hwB
  intro j
  refine ⟨(hq j).1, (hq j).2, ?_⟩
  intro s
  have hc := rationalMix_preserves_leaf_calls p x hp hp1 hx hm hab hT ht (hcall j) s
  have he : selectionCall (mixedMass p x a b m t) (mixedLocation x a b) s =
      ∑ i, rationalMixMass p a b m t (∑ j, p j / x j) i *
        max (rationalMixLocation x a b i - s) 0 := by
    unfold selectionCall mixedMass mixedLocation
    exact sum_reindex (fun i => rationalMixMass p a b m t (∑ j, p j / x j) i *
      max (rationalMixLocation x a b i - s) 0)
  rw [he, show selectionMean (mixedMass p x a b m t) (mixedLocation x a b) = m from hm']
  exact hc

/-- Total selector charge on the mixed law is polynomial in atom and leaf counts. -/
theorem rationalWitnessProducer_cost {K n : ℕ} (p x : Fin K → ℚ) (a b m t : ℚ)
    (q w : Fin n → ℚ) :
    (∑ j, (rationalWitnessProducer p x a b m t q w j).2) ≤ n * (64 * (K + 3) ^ 2) := by
  exact rationalAllSelectorsWork_polynomial _ _ _ _

end ReciprocalAnchor.ManyLeaf
