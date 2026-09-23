import Formal.ReciprocalAnchor.ManySelection
import Formal.ReciprocalAnchor.ManyRationalSize
import Formal.ReciprocalAnchor.ManyModel
import Formal.ReciprocalAnchor.ManyRationalBound

/-! Exact rational fractional selections and polynomial bounds on their output size. -/
namespace ReciprocalAnchor.ManyLeaf
open scoped BigOperators

variable {ι : Type*} [Fintype ι]

def tailBits (N B : ℕ) : ℕ := B + 2 * (1 + N * (B + 1)) + 1

theorem thresholdSelection_bits (p x : ι → ℚ) (q s : ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hq : RationalBits q B) (i : ι) :
    RationalBits (thresholdSelection p x q s i) (tailBits (Fintype.card ι) B) := by
  classical
  have hb := rationalBits_pos hq
  have hs (f : ι → Prop) [DecidablePred f] :
      RationalBits (∑ k, if f k then p k else 0) (1 + Fintype.card ι * (B + 1)) := by
    apply rationalBits_finset_sum
    intro k _
    split_ifs
    · exact hp k
    · exact rationalBits_mono rationalBits_zero hb
  unfold thresholdSelection
  split_ifs
  · exact rationalBits_mono rationalBits_one (by unfold tailBits; omega)
  · convert rationalBits_div (rationalBits_sub hq (hs (fun k => s < x k)))
      (hs (fun k => x k = s)) using 1
    unfold tailBits
    omega
  · exact rationalBits_mono rationalBits_zero (by unfold tailBits; omega)

def momentBits (N B C : ℕ) : ℕ := 1 + N * (2 * B + C + 1)

theorem selectionMoment_bits (p x θ : ι → ℚ) {B C : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (hθ : ∀ i, RationalBits (θ i) C) :
    RationalBits (selectionMoment p x θ) (momentBits (Fintype.card ι) B C) := by
  unfold selectionMoment momentBits
  apply rationalBits_finset_sum
  intro i _
  convert rationalBits_mul (rationalBits_mul (hp i) (hx i)) (hθ i) using 1; omega

def interpolationBits (N B C : ℕ) : ℕ := 2 * (B + 3 * momentBits N B C + 2) + 2 * C + 3

theorem interpolatedSelection_bits (p x θ₀ θ₁ : ι → ℚ) (w : ℚ) {B C : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (h₀ : ∀ i, RationalBits (θ₀ i) C) (h₁ : ∀ i, RationalBits (θ₁ i) C)
    (hw : RationalBits w B) (i : ι) :
    RationalBits (interpolatedSelection p x θ₀ θ₁ w i)
      (interpolationBits (Fintype.card ι) B C) := by
  have hv₀ := selectionMoment_bits p x θ₀ hp hx h₀
  have hv₁ := selectionMoment_bits p x θ₁ hp hx h₁
  unfold interpolatedSelection
  split_ifs
  · exact rationalBits_mono (h₀ i) (by unfold interpolationBits; omega)
  · have hr := rationalBits_div (rationalBits_sub hw hv₀) (rationalBits_sub hv₁ hv₀)
    have h := rationalBits_add
      (rationalBits_mul (rationalBits_sub rationalBits_one hr) (h₀ i))
      (rationalBits_mul hr (h₁ i))
    convert h using 1
    unfold interpolationBits
    omega

/-- This explicit polynomial bounds every selected leaf coordinate. -/
def witnessBits (N B : ℕ) : ℕ :=
  interpolationBits N (B + 2) (tailBits N (B + 2) + 2)

/-- Rational input admits rational selections with bounded reduced fractions.
The construction uses two threshold selectors and their exact interpolation. -/
theorem rational_selectors_bounded (p x : ι → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q w : ℚ)
    (h : 0 ≤ q ∧ q ≤ 1 ∧ ∀ s,
      w - q * s ≤ selectionCall p x s ∧
      selectionMean p x - w - (1 - q) * s ≤ selectionCall p x s)
    {B : ℕ} (hpB : ∀ i, RationalBits (p i) B) (hxB : ∀ i, RationalBits (x i) B)
    (hqB : RationalBits q B) (hwB : RationalBits w B) (s₁ s₀ : ℚ)
    (hs₁ : (∑ i, if s₁ < x i then p i else 0) ≤ q)
    (hs₁' : q ≤ ∑ i, if s₁ ≤ x i then p i else 0)
    (hs₀ : (∑ i, if s₀ < x i then p i else 0) ≤ 1 - q)
    (hs₀' : 1 - q ≤ ∑ i, if s₀ ≤ x i then p i else 0) :
    let θ := interpolatedSelection p x (fun i => 1 - thresholdSelection p x (1 - q) s₀ i)
      (thresholdSelection p x q s₁) w
    (∀ i, θ i ∈ Set.Icc (0 : ℚ) 1) ∧
      selectionMass p θ = q ∧ selectionMoment p x θ = w ∧
      ∀ i, RationalBits (θ i) (witnessBits (Fintype.card ι) B) := by
  let θ₁ := thresholdSelection p x q s₁
  let φ := thresholdSelection p x (1 - q) s₀
  let θ₀ := fun i => 1 - φ i
  have h₁ := thresholdSelection_spec p x hp q s₁ hs₁ hs₁'
  have hφ := thresholdSelection_spec p x hp (1 - q) s₀ hs₀ hs₀'
  have h₀ : ∀ i, θ₀ i ∈ Set.Icc (0 : ℚ) 1 :=
    fun i => ⟨by dsimp [θ₀]; linarith [(hφ.1 i).2],
      by dsimp [θ₀]; linarith [(hφ.1 i).1]⟩
  have hm₀ : selectionMass p θ₀ = q := by
    rw [selection_complement_mass p φ hsum, hφ.2.1]
    ring
  have hw₀ : selectionMoment p x θ₀ ≤ w := by
    rw [selection_complement_moment, hφ.2.2]
    linarith [(h.2.2 s₀).2]
  have hw₁ : w ≤ selectionMoment p x θ₁ := by
    rw [h₁.2.2]
    linarith [(h.2.2 s₁).1]
  obtain ⟨hrange, hmass, hmoment⟩ :=
    interpolatedSelection_spec p x θ₀ θ₁ h₀ h₁.1 q w hm₀ h₁.2.1 hw₀ hw₁
  refine ⟨hrange, hmass, hmoment, ?_⟩
  have hφB : ∀ i, RationalBits (φ i) (tailBits (Fintype.card ι) (B + 2)) := by
    intro i
    apply thresholdSelection_bits
    · exact fun i => rationalBits_mono (hpB i) (by omega)
    · convert rationalBits_sub rationalBits_one hqB using 1; omega
  have h₀B : ∀ i, RationalBits (θ₀ i) (tailBits (Fintype.card ι) (B + 2) + 2) := by
    intro i
    convert rationalBits_sub rationalBits_one (hφB i) using 1; omega
  have h₁B : ∀ i, RationalBits (θ₁ i) (tailBits (Fintype.card ι) (B + 2) + 2) := by
    intro i
    apply rationalBits_mono (thresholdSelection_bits p x q s₁
      (fun i => rationalBits_mono (hpB i) (by omega : B ≤ B + 2))
      (rationalBits_mono hqB (by omega : B ≤ B + 2)) i)
    omega
  exact interpolatedSelection_bits p x θ₀ θ₁ w
    (fun i => rationalBits_mono (hpB i) (by omega))
    (fun i => rationalBits_mono (hxB i) (by omega)) h₀B h₁B
    (rationalBits_mono hwB (by omega))

/-- Rational input admits rational selectors with an explicit polynomial bit bound. -/
theorem exists_rational_selection_bounded (p x : ι → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q w : ℚ)
    (h : 0 ≤ q ∧ q ≤ 1 ∧ ∀ s,
      w - q * s ≤ selectionCall p x s ∧
      selectionMean p x - w - (1 - q) * s ≤ selectionCall p x s)
    {B : ℕ} (hpB : ∀ i, RationalBits (p i) B) (hxB : ∀ i, RationalBits (x i) B)
    (hqB : RationalBits q B) (hwB : RationalBits w B) :
    ∃ θ : ι → ℚ, (∀ i, θ i ∈ Set.Icc (0 : ℚ) 1) ∧
      selectionMass p θ = q ∧ selectionMoment p x θ = w ∧
      ∀ i, RationalBits (θ i) (witnessBits (Fintype.card ι) B) := by
  obtain ⟨s₁, hs₁, hs₁'⟩ := exists_weighted_threshold p x hp hsum q h.1 h.2.1
  obtain ⟨s₀, hs₀, hs₀'⟩ := exists_weighted_threshold p x hp hsum (1 - q)
    (by linarith [h.2.1]) (by linarith [h.1])
  exact ⟨_, rational_selectors_bounded p x hp hsum q w h hpB hxB hqB hwB
    s₁ s₀ hs₁ hs₁' hs₀ hs₀'⟩

/-- Every partial tail sum has the same polynomial bound; the algorithm does not
hide a large intermediate numerator in its finite summations. -/
theorem rational_tail_partial_bits (p : ι → ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hB : 0 < B) (S : Finset ι)
    (f : ι → Prop) [DecidablePred f] :
    RationalBits (∑ i ∈ S, if f i then p i else 0)
      (1 + Fintype.card ι * (B + 1)) := by
  have hh : ∀ i ∈ S, RationalBits (if f i then p i else 0) B := by
    intro i _
    split_ifs
    · exact hp i
    · exact rationalBits_mono rationalBits_zero hB
  apply rationalBits_mono (rationalBits_finset_sum S _ hh)
  exact Nat.add_le_add_left (Nat.mul_le_mul_right _ (Finset.card_le_univ S)) _

/-- Every partial selected moment also has polynomially bounded reduced fractions. -/
theorem rational_moment_partial_bits (p x θ : ι → ℚ) {B C : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (hθ : ∀ i, RationalBits (θ i) C) (S : Finset ι) :
    RationalBits (∑ i ∈ S, p i * x i * θ i) (momentBits (Fintype.card ι) B C) := by
  have hh : ∀ i ∈ S, RationalBits (p i * x i * θ i) (B + B + C) :=
    fun i _ => rationalBits_mul (rationalBits_mul (hp i) (hx i)) (hθ i)
  apply rationalBits_mono (rationalBits_finset_sum S _ hh)
  unfold momentBits
  have hc := Finset.card_le_univ S
  have ht := Nat.mul_le_mul_right (B + B + C + 1) hc
  nlinarith

/-- The interpolation division and its complement are actual bounded intermediate values. -/
theorem rational_interpolation_ratio_bits (p x θ₀ θ₁ : ι → ℚ) (w : ℚ) {B C : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B)
    (h₀ : ∀ i, RationalBits (θ₀ i) C) (h₁ : ∀ i, RationalBits (θ₁ i) C)
    (hw : RationalBits w B) :
    let r := (w - selectionMoment p x θ₀) /
      (selectionMoment p x θ₁ - selectionMoment p x θ₀)
    RationalBits r (B + 3 * momentBits (Fintype.card ι) B C + 2) ∧
      RationalBits (1 - r) (B + 3 * momentBits (Fintype.card ι) B C + 4) := by
  have hv₀ := selectionMoment_bits p x θ₀ hp hx h₀
  have hv₁ := selectionMoment_bits p x θ₁ hp hx h₁
  have hr := rationalBits_div (rationalBits_sub hw hv₀) (rationalBits_sub hv₁ hv₀)
  constructor
  · convert hr using 1; omega
  · convert rationalBits_sub rationalBits_one hr using 1; omega

/-- The envelope producer yields a small law whose rational atoms have polynomial size. -/
theorem exists_bounded_rational_envelope_law {J : Type*} [Fintype J] [Nonempty J]
    (c d : J → ℚ) {a b : ℚ} (hab : a < b) (m : ℚ)
    (hl : ∀ s ≤ (a : ℝ),
      affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) s = (m : ℝ) - s)
    (hr : ∀ s, (b : ℝ) ≤ s →
      affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) s = 0)
    (hleft : ∃ i, d i = -1) (hright : ∃ i, d i = 0) {B : ℕ}
    (haB : RationalBits a B) (hbB : RationalBits b B)
    (hcB : ∀ i, RationalBits (c i) B) (hdB : ∀ i, RationalBits (d i) B) :
    ∃ μ : Law (a : ℝ) (b : ℝ), ∃ p x : Fin μ.size → ℚ,
      μ.size ≤ Fintype.card J - 1 ∧ μ.mean = (m : ℝ) ∧
      μ.call = affineEnvelope (fun i => (c i : ℝ)) (fun i => (d i : ℝ)) ∧
      (∀ i, μ.mass i = (p i : ℝ) ∧ μ.location i = (x i : ℝ)) ∧
      ∀ i, RationalBits (p i) (4 * B + 2) ∧ RationalBits (x i) (4 * B + 2) := by
  classical
  obtain ⟨P, hknots, _⟩ := exists_affinePartition_with_provenance c d hab
  obtain ⟨μ, hsize, hmean, hcall, hatoms⟩ :=
    P.exists_small_rational_law m hl hr hleft hright
  choose j k l hp hx using hatoms
  refine ⟨μ, fun i => d (j i) - d (k i), fun i => P.knot (l i),
    hsize, hmean, hcall, fun i => ⟨hp i, hx i⟩, ?_⟩
  intro i
  refine ⟨rationalBits_mono (rationalBits_sub (hdB (j i)) (hdB (k i))) (by omega), ?_⟩
  change RationalBits (P.knot (l i)) (4 * B + 2)
  rcases hknots (l i) with he | he | ⟨j, k, he⟩
  · rw [he]
    exact rationalBits_mono haB (by omega)
  · rw [he]
    exact rationalBits_mono hbB (by omega)
  · rw [he]
    exact rationalBits_intersection (hcB j) (hdB j) (hcB k) (hdB k)

/-- Computing the reciprocal from rational atoms preserves a polynomial size bound. -/
theorem reciprocal_sum_bits (p x : ι → ℚ) {B : ℕ}
    (hp : ∀ i, RationalBits (p i) B) (hx : ∀ i, RationalBits (x i) B) :
    RationalBits (∑ i, p i / x i) (1 + Fintype.card ι * (2 * B + 1)) := by
  apply rationalBits_finset_sum
  intro i _
  convert rationalBits_div (hp i) (hx i) using 1; omega

/-- Casting a rational finite graph witness yields membership in the actual real hull. -/
theorem rational_representation_mem_hull {n : ℕ} {a b m t : ℚ} {q w : Fin n → ℚ}
    (p x : ι → ℚ) (y : ι → Fin n → ℚ)
    (hp : ∀ i, 0 ≤ p i) (hp1 : ∑ i, p i = 1)
    (hx : ∀ i, a ≤ x i ∧ x i ≤ b) (hy : ∀ i j, 0 ≤ y i j ∧ y i j ≤ 1)
    (hm : ∑ i, p i * x i = m) (ht : ∑ i, p i / x i = t)
    (hq : ∀ j, ∑ i, p i * y i j = q j)
    (hw : ∀ j, ∑ i, p i * (x i * y i j) = w j) :
    point (m : ℝ) (t : ℝ) (fun j => (q j : ℝ)) (fun j => (w j : ℝ)) ∈
      hull n (a : ℝ) (b : ℝ) := by
  apply finite_representation_mem_hull (fun i => (p i : ℝ))
    (fun i => (x i : ℝ)) (fun i j => (y i j : ℝ))
  · intro i; exact_mod_cast hp i
  · exact_mod_cast hp1
  · intro i; exact_mod_cast hx i
  · intro i j; exact_mod_cast hy i j
  · exact_mod_cast hm
  · exact_mod_cast ht
  · intro j; exact_mod_cast hq j
  · intro j; exact_mod_cast hw j

end ReciprocalAnchor.ManyLeaf
