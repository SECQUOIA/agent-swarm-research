import Formal.ReciprocalAnchor.ManyRationalThreshold

/-! Executable rational leaf selection and its connection to the bounded witness formula. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

/-- Search two finite threshold lists, then interpolate their explicitly computed selectors. -/
def rationalSelector {K : ℕ} (p x : Fin K → ℚ) (q w : ℚ) : Option (Fin K → ℚ) := do
  let s₁ ← (rationalThreshold p x q).1
  let s₀ ← (rationalThreshold p x (1 - q)).1
  pure (interpolatedSelection p x (fun i => 1 - thresholdSelection p x (1 - q) s₀ i)
    (thresholdSelection p x q s₁) w)

/-- The emitted selector realizes both requested rational moments and has polynomial size. -/
theorem rationalSelector_spec {K B : ℕ} (p x : Fin K → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q w : ℚ)
    (h : 0 ≤ q ∧ q ≤ 1 ∧ ∀ s,
      w - q * s ≤ selectionCall p x s ∧
      selectionMean p x - w - (1 - q) * s ≤ selectionCall p x s)
    (hpB : ∀ i, RationalBits (p i) B) (hxB : ∀ i, RationalBits (x i) B)
    (hqB : RationalBits q B) (hwB : RationalBits w B) :
    ∃ θ, rationalSelector p x q w = some θ ∧
      (∀ i, θ i ∈ Set.Icc (0 : ℚ) 1) ∧ selectionMass p θ = q ∧
      selectionMoment p x θ = w ∧ ∀ i, RationalBits (θ i) (witnessBits K B) := by
  obtain ⟨s₁, he₁, hs₁, hs₁'⟩ := rationalThreshold_spec p x hp hsum q h.1 h.2.1
  obtain ⟨s₀, he₀, hs₀, hs₀'⟩ := rationalThreshold_spec p x hp hsum (1 - q)
    (by linarith [h.2.1]) (by linarith [h.1])
  refine ⟨interpolatedSelection p x (fun i => 1 - thresholdSelection p x (1 - q) s₀ i)
    (thresholdSelection p x q s₁) w, ?_, ?_⟩
  · simp [rationalSelector, he₁, he₀]
  · simpa only [Fintype.card_fin] using rational_selectors_bounded p x hp hsum q w h
      hpB hxB hqB hwB s₁ s₀ hs₁ hs₁' hs₀ hs₀'

/-- Compute each tail sum once before constructing the selector function. -/
def cachedThresholdSelector {K : ℕ} (p x : Fin K → ℚ) (q s : ℚ) : Fin K → ℚ :=
  let A := ∑ k, if s < x k then p k else 0
  let D := ∑ k, if x k = s then p k else 0
  let r := (q - A) / D
  fun i => if s < x i then 1 else if x i = s then r else 0

theorem cachedThresholdSelector_eq {K : ℕ} (p x : Fin K → ℚ) (q s : ℚ) :
    cachedThresholdSelector p x q s = thresholdSelection p x q s := rfl

/-- Counted producer of the full output list. Charges count rational comparisons,
additions, multiplications, and divisions. Four tail traversals cost eight operations
per atom; extremal-selector and moment traversals, including repeated selector evaluation,
cost twelve per entry each;
interpolation costs four per output entry. The twenty scalar operations cover both
ratios, their complement, interpolation, and branch tests. List/index overhead is
separate and polynomial in these list lengths. -/
def rationalSelectorCounted {K : ℕ} (p x : Fin K → ℚ) (q w : ℚ) : Option (List ℚ) × ℕ :=
  let r₁ := rationalThreshold p x q
  let r₀ := rationalThreshold p x (1 - q)
  match r₁.1, r₀.1 with
  | some s₁, some s₀ =>
    let θ₁ := cachedThresholdSelector p x q s₁
    let φ := cachedThresholdSelector p x (1 - q) s₀
    let θ₀ := fun i => 1 - φ i
    let low := List.ofFn θ₀
    let high := List.ofFn θ₁
    let out := List.ofFn (interpolatedSelection p x θ₀ θ₁ w)
    (some out, r₁.2 + r₀.2 + 8 * (List.ofFn x).length +
      12 * low.length + 12 * high.length + 4 * out.length + 20)
  | _, _ => (none, r₁.2 + r₀.2)

theorem rationalSelectorCounted_value {K : ℕ} (p x : Fin K → ℚ) (q w : ℚ) :
    (rationalSelectorCounted p x q w).1 = (rationalSelector p x q w).map List.ofFn := by
  cases he₁ : (rationalThreshold p x q).1 <;>
    cases he₀ : (rationalThreshold p x (1 - q)).1 <;>
      simp [rationalSelectorCounted, rationalSelector, he₁, he₀, cachedThresholdSelector_eq]

theorem rationalSelectorCounted_polynomial {K : ℕ} (p x : Fin K → ℚ) (q w : ℚ) :
    (rationalSelectorCounted p x q w).2 ≤ 64 * (K + 1) ^ 2 := by
  have h₁ := rationalThreshold_polynomial_cost p x q
  have h₀ := rationalThreshold_polynomial_cost p x (1 - q)
  cases he₁ : (rationalThreshold p x q).1 <;>
    cases he₀ : (rationalThreshold p x (1 - q)).1 <;>
      simp only [rationalSelectorCounted, he₁, he₀, List.length_ofFn]
  all_goals nlinarith [Nat.zero_le (K ^ 2)]

/-- The concrete emitted list has the same exact moments and bit bound as the
mathematical selector, so the cost theorem applies to a successful producer. -/
theorem rationalSelectorCounted_spec {K B : ℕ} (p x : Fin K → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q w : ℚ)
    (h : 0 ≤ q ∧ q ≤ 1 ∧ ∀ s,
      w - q * s ≤ selectionCall p x s ∧
      selectionMean p x - w - (1 - q) * s ≤ selectionCall p x s)
    (hpB : ∀ i, RationalBits (p i) B) (hxB : ∀ i, RationalBits (x i) B)
    (hqB : RationalBits q B) (hwB : RationalBits w B) :
    ∃ θ, (rationalSelectorCounted p x q w).1 = some (List.ofFn θ) ∧
      (∀ i, θ i ∈ Set.Icc (0 : ℚ) 1) ∧ selectionMass p θ = q ∧
      selectionMoment p x θ = w ∧ ∀ i, RationalBits (θ i) (witnessBits K B) := by
  obtain ⟨θ, he, hθ⟩ := rationalSelector_spec p x hp hsum q w h hpB hxB hqB hwB
  refine ⟨θ, ?_, hθ⟩
  rw [rationalSelectorCounted_value, he]
  rfl

/-- Selecting every leaf adds the charges of the actually executed producers. -/
def rationalAllSelectorsWork {K n : ℕ} (p x : Fin K → ℚ) (q w : Fin n → ℚ) : ℕ :=
  ∑ j, (rationalSelectorCounted p x (q j) (w j)).2

theorem rationalAllSelectorsWork_polynomial {K n : ℕ}
    (p x : Fin K → ℚ) (q w : Fin n → ℚ) :
    rationalAllSelectorsWork p x q w ≤ n * (64 * (K + 1) ^ 2) := by
  calc
    _ ≤ ∑ _j : Fin n, 64 * (K + 1) ^ 2 :=
      Finset.sum_le_sum (fun j _ => rationalSelectorCounted_polynomial p x (q j) (w j))
    _ = _ := by simp

/-- Every leaf in the finite family is produced successfully on the same rational law. -/
theorem rationalAllSelectors_spec {K n B : ℕ} (p x : Fin K → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q w : Fin n → ℚ)
    (h : ∀ j, 0 ≤ q j ∧ q j ≤ 1 ∧ ∀ s,
      w j - q j * s ≤ selectionCall p x s ∧
      selectionMean p x - w j - (1 - q j) * s ≤ selectionCall p x s)
    (hpB : ∀ i, RationalBits (p i) B) (hxB : ∀ i, RationalBits (x i) B)
    (hqB : ∀ j, RationalBits (q j) B) (hwB : ∀ j, RationalBits (w j) B) :
    ∃ θ : Fin n → Fin K → ℚ, ∀ j,
      (rationalSelectorCounted p x (q j) (w j)).1 = some (List.ofFn (θ j)) ∧
      (∀ i, θ j i ∈ Set.Icc (0 : ℚ) 1) ∧ selectionMass p (θ j) = q j ∧
      selectionMoment p x (θ j) = w j ∧ ∀ i, RationalBits (θ j i) (witnessBits K B) := by
  exact Classical.axiomOfChoice (fun j =>
    rationalSelectorCounted_spec p x hp hsum (q j) (w j) (h j) hpB hxB (hqB j) (hwB j))

end ReciprocalAnchor.ManyLeaf
