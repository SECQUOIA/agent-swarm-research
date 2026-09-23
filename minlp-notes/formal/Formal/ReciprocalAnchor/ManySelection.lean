import Formal.ReciprocalAnchor.ManyThreshold

/-! Fractional submeasures of a finite law, characterized by all call inequalities. -/

namespace ReciprocalAnchor.ManyLeaf

variable {𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜]

variable {ι : Type*} [Fintype ι]

def selectionCall (p x : ι → 𝕜) (s : 𝕜) : 𝕜 :=
  ∑ i, p i * max (x i - s) 0
def selectionMass (p θ : ι → 𝕜) : 𝕜 := ∑ i, p i * θ i
def selectionMoment (p x θ : ι → 𝕜) : 𝕜 := ∑ i, p i * x i * θ i
def selectionMean (p x : ι → 𝕜) : 𝕜 := ∑ i, p i * x i

theorem selection_call_bound (p x θ : ι → 𝕜) (hp : ∀ i, 0 ≤ p i)
    (hθ : ∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) (s : 𝕜) :
    selectionMoment p x θ - selectionMass p θ * s ≤ selectionCall p x s := by
  unfold selectionMoment selectionMass selectionCall
  rw [Finset.sum_mul, ← Finset.sum_sub_distrib]
  apply Finset.sum_le_sum
  intro i _
  have h := hθ i
  have hi : (x i - s) * θ i ≤ max (x i - s) 0 := by
    by_cases hx : 0 ≤ x i - s
    · rw [max_eq_left hx]
      exact mul_le_of_le_one_right hx h.2
    · rw [max_eq_right (le_of_not_ge hx)]
      exact mul_nonpos_of_nonpos_of_nonneg (le_of_not_ge hx) h.1
  nlinarith [mul_le_mul_of_nonneg_left hi (hp i)]

omit [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜] in
theorem selection_complement_mass (p θ : ι → 𝕜) (hp : ∑ i, p i = 1) :
    selectionMass p (fun i => 1 - θ i) = 1 - selectionMass p θ := by
  simp only [selectionMass, mul_sub, mul_one, Finset.sum_sub_distrib, hp]

omit [LinearOrder 𝕜] [IsStrictOrderedRing 𝕜] in
theorem selection_complement_moment (p x θ : ι → 𝕜) :
    selectionMoment p x (fun i => 1 - θ i) = selectionMean p x - selectionMoment p x θ := by
  simp only [selectionMoment, selectionMean, mul_sub, mul_one, Finset.sum_sub_distrib]

theorem selection_necessary (p x θ : ι → 𝕜) (hp : ∀ i, 0 ≤ p i)
    (hsum : ∑ i, p i = 1) (hθ : ∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) :
    0 ≤ selectionMass p θ ∧ selectionMass p θ ≤ 1 ∧
      ∀ s, selectionMoment p x θ - selectionMass p θ * s ≤ selectionCall p x s ∧
        selectionMean p x - selectionMoment p x θ - (1 - selectionMass p θ) * s ≤
          selectionCall p x s := by
  refine ⟨Finset.sum_nonneg (fun i _ => mul_nonneg (hp i) (hθ i).1), ?_, ?_⟩
  · calc
      selectionMass p θ ≤ ∑ i, p i :=
        Finset.sum_le_sum (fun i _ => mul_le_of_le_one_right (hp i) (hθ i).2)
      _ = 1 := hsum
  · intro s
    refine ⟨selection_call_bound p x θ hp hθ s, ?_⟩
    have hc := selection_call_bound p x (fun i => 1 - θ i) hp
      (fun i => ⟨by linarith [(hθ i).2], by linarith [(hθ i).1]⟩) s
    rwa [selection_complement_mass p θ hsum, selection_complement_moment] at hc

/-- The explicit threshold selector uses only comparisons, sums, and one division. -/
def thresholdSelection (p x : ι → 𝕜) (q s : 𝕜) (i : ι) : 𝕜 :=
  if s < x i then 1 else if x i = s then
    (q - ∑ k, if s < x k then p k else 0) / (∑ k, if x k = s then p k else 0) else 0

theorem thresholdSelection_spec (p x : ι → 𝕜) (hp : ∀ i, 0 ≤ p i)
    (q s : 𝕜) (hlo : (∑ i, if s < x i then p i else 0) ≤ q)
    (hhi : q ≤ ∑ i, if s ≤ x i then p i else 0) :
    (∀ i, thresholdSelection p x q s i ∈ Set.Icc (0 : 𝕜) 1) ∧
      selectionMass p (thresholdSelection p x q s) = q ∧
      selectionMoment p x (thresholdSelection p x q s) = q * s + selectionCall p x s := by
  classical
  let A : 𝕜 := ∑ i, if s < x i then p i else 0
  let B : 𝕜 := ∑ i, if x i = s then p i else 0
  have hB : 0 ≤ B := Finset.sum_nonneg (fun i _ => by
    split_ifs
    · exact hp i
    · exact le_refl 0)
  have hAB : (∑ i, if s ≤ x i then p i else 0) = A + B := by
    rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    rcases lt_trichotomy (x i) s with h | h | h
    · simp [not_le.mpr h, not_lt.mpr h.le, ne_of_lt h]
    · simp [h]
    · simp [h, h.le, ne_of_gt h]
  have hd0 : 0 ≤ q - A := sub_nonneg.mpr hlo
  have hdB : q - A ≤ B := by rw [hAB] at hhi; linarith
  let r := (q - A) / B
  have hr0 : 0 ≤ r := div_nonneg hd0 hB
  have hr1 : r ≤ 1 := by
    by_cases h : B = 0
    · simp [r, h]
    · exact (div_le_one (lt_of_le_of_ne hB (Ne.symm h))).mpr hdB
  have hrB : r * B = q - A := by
    by_cases h : B = 0
    · have : q - A = 0 := by linarith
      simp [h, this]
    · exact div_mul_cancel₀ _ h
  let θ : ι → 𝕜 := fun i => if s < x i then 1 else if x i = s then r else 0
  have hθ : ∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1 := by
    intro i
    dsimp [θ]
    split_ifs <;> exact ⟨by positivity, by first | exact hr1 | norm_num⟩
  have hm : selectionMass p θ = q := by
    have he : ∀ i, p i * θ i = (if s < x i then p i else 0) +
        r * (if x i = s then p i else 0) := by
      intro i
      dsimp [θ]
      split_ifs <;> simp_all; ring
    simp_rw [selectionMass, he, Finset.sum_add_distrib, ← Finset.mul_sum]
    change A + r * B = q
    linarith
  change (∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) ∧ selectionMass p θ = q ∧
    selectionMoment p x θ = q * s + selectionCall p x s
  refine ⟨hθ, hm, ?_⟩
  have he : ∀ i, p i * x i * θ i = p i * θ i * s + p i * max (x i - s) 0 := by
    intro i
    dsimp [θ]
    split_ifs with hi heq
    · rw [max_eq_left (by linarith)]
      ring
    · rw [heq]
      simp only [sub_self, max_self, mul_zero, add_zero]
      ring
    · rw [max_eq_right (by linarith)]
      simp
  simp_rw [selectionMoment, he, Finset.sum_add_distrib, ← Finset.sum_mul]
  change selectionMass p θ * s + selectionCall p x s = _
  rw [hm]

theorem selection_of_threshold (p x : ι → 𝕜) (hp : ∀ i, 0 ≤ p i)
    (q s : 𝕜) (hlo : (∑ i, if s < x i then p i else 0) ≤ q)
    (hhi : q ≤ ∑ i, if s ≤ x i then p i else 0) :
    ∃ θ : ι → 𝕜, (∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) ∧
      selectionMass p θ = q ∧ selectionMoment p x θ = q * s + selectionCall p x s :=
  ⟨thresholdSelection p x q s, thresholdSelection_spec p x hp q s hlo hhi⟩

theorem selection_upper_attained (p x : ι → 𝕜) (hp : ∀ i, 0 ≤ p i)
    (hsum : ∑ i, p i = 1) (q : 𝕜) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ∃ s θ, (∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) ∧ selectionMass p θ = q ∧
      selectionMoment p x θ = q * s + selectionCall p x s ∧
      ∀ t, selectionMoment p x θ ≤ q * t + selectionCall p x t := by
  obtain ⟨s, hs, hs'⟩ := exists_weighted_threshold p x hp hsum q hq hq1
  obtain ⟨θ, hθ, hm, hv⟩ := selection_of_threshold p x hp q s hs hs'
  refine ⟨s, θ, hθ, hm, hv, fun t => ?_⟩
  have h := selection_call_bound p x θ hp hθ t
  rw [hm] at h
  linarith

/-- The call-price dual minimum is attained, and equals the largest selected moment. -/
theorem selection_upper_eq_sInf (p x : ι → ℝ) (hp : ∀ i, 0 ≤ p i)
    (hsum : ∑ i, p i = 1) (q : ℝ) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ∃ θ, (∀ i, θ i ∈ Set.Icc (0 : ℝ) 1) ∧ selectionMass p θ = q ∧
      selectionMoment p x θ = sInf (Set.range (fun s => q * s + selectionCall p x s)) ∧
      ∀ φ, (∀ i, φ i ∈ Set.Icc (0 : ℝ) 1) → selectionMass p φ = q →
        selectionMoment p x φ ≤ selectionMoment p x θ := by
  obtain ⟨s, θ, hθ, hm, hv, hmin⟩ := selection_upper_attained p x hp hsum q hq hq1
  refine ⟨θ, hθ, hm, ?_, ?_⟩
  · apply Eq.symm
    apply IsLeast.csInf_eq
    refine ⟨⟨s, hv.symm⟩, ?_⟩
    rintro _ ⟨t, rfl⟩
    exact hmin t
  · intro φ hφ hmφ
    have h := selection_call_bound p x φ hp hφ s
    rw [hmφ] at h
    rw [hv]
    linarith

/-- The smallest selected moment is the total mean minus the greatest moment
of a complementary selection. -/
theorem selection_lower_eq_mean_sub_sInf (p x : ι → ℝ) (hp : ∀ i, 0 ≤ p i)
    (hsum : ∑ i, p i = 1) (q : ℝ) (hq : 0 ≤ q) (hq1 : q ≤ 1) :
    ∃ θ, (∀ i, θ i ∈ Set.Icc (0 : ℝ) 1) ∧ selectionMass p θ = q ∧
      selectionMoment p x θ = selectionMean p x -
        sInf (Set.range (fun s => (1 - q) * s + selectionCall p x s)) ∧
      ∀ φ, (∀ i, φ i ∈ Set.Icc (0 : ℝ) 1) → selectionMass p φ = q →
        selectionMoment p x θ ≤ selectionMoment p x φ := by
  obtain ⟨ψ, hψ, hmψ, hvψ, hmax⟩ := selection_upper_eq_sInf p x hp hsum
    (1 - q) (by linarith) (by linarith)
  refine ⟨fun i => 1 - ψ i,
    fun i => ⟨by linarith [(hψ i).2], by linarith [(hψ i).1]⟩, ?_, ?_, ?_⟩
  · rw [selection_complement_mass p ψ hsum, hmψ]; ring
  · rw [selection_complement_moment, hvψ]
  · intro φ hφ hmφ
    have h := hmax (fun i => 1 - φ i)
      (fun i => ⟨by linarith [(hφ i).2], by linarith [(hφ i).1]⟩)
      (by rw [selection_complement_mass p φ hsum, hmφ])
    rw [selection_complement_moment] at h ⊢
    linarith

/-- Interpolating the extremal selectors uses one exact rational ratio. -/
def interpolatedSelection (p x θ₀ θ₁ : ι → 𝕜) (w : 𝕜) : ι → 𝕜 :=
  let v₀ := selectionMoment p x θ₀
  let v₁ := selectionMoment p x θ₁
  if v₀ = v₁ then θ₀ else
    let r := (w - v₀) / (v₁ - v₀)
    fun i => (1 - r) * θ₀ i + r * θ₁ i

theorem interpolatedSelection_spec (p x θ₀ θ₁ : ι → 𝕜)
    (h₀ : ∀ i, θ₀ i ∈ Set.Icc (0 : 𝕜) 1)
    (h₁ : ∀ i, θ₁ i ∈ Set.Icc (0 : 𝕜) 1) (q w : 𝕜)
    (hm₀ : selectionMass p θ₀ = q) (hm₁ : selectionMass p θ₁ = q)
    (hw₀ : selectionMoment p x θ₀ ≤ w) (hw₁ : w ≤ selectionMoment p x θ₁) :
    (∀ i, interpolatedSelection p x θ₀ θ₁ w i ∈ Set.Icc (0 : 𝕜) 1) ∧
      selectionMass p (interpolatedSelection p x θ₀ θ₁ w) = q ∧
      selectionMoment p x (interpolatedSelection p x θ₀ θ₁ w) = w := by
  let v₀ := selectionMoment p x θ₀
  let v₁ := selectionMoment p x θ₁
  by_cases heq : v₀ = v₁
  · rw [interpolatedSelection, if_pos heq]
    refine ⟨h₀, hm₀, ?_⟩
    change v₀ = w
    change v₀ ≤ w at hw₀
    change w ≤ v₁ at hw₁
    linarith
  have hd : 0 < v₁ - v₀ := by
    change v₀ ≤ w at hw₀
    change w ≤ v₁ at hw₁
    rcases lt_or_gt_of_ne heq with h | h <;> linarith
  let r := (w - v₀) / (v₁ - v₀)
  have hr : 0 ≤ r := div_nonneg (sub_nonneg.mpr hw₀) hd.le
  have hr1 : r ≤ 1 := (div_le_one hd).mpr (by linarith)
  have hid : r * (v₁ - v₀) = w - v₀ := div_mul_cancel₀ _ (ne_of_gt hd)
  let θ := fun i => (1 - r) * θ₀ i + r * θ₁ i
  have hθ : ∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1 := by
    intro i
    dsimp [θ]
    refine ⟨add_nonneg (mul_nonneg (by linarith) (h₀ i).1)
      (mul_nonneg hr (h₁ i).1), ?_⟩
    have hA := mul_le_of_le_one_right (by linarith : 0 ≤ 1 - r) (h₀ i).2
    have hB := mul_le_of_le_one_right hr (h₁ i).2
    linarith
  have hm : selectionMass p θ = (1 - r) * selectionMass p θ₀ + r * selectionMass p θ₁ := by
    unfold selectionMass
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    dsimp [θ]
    ring
  have hv : selectionMoment p x θ = (1 - r) * v₀ + r * v₁ := by
    dsimp [v₀, v₁]
    unfold selectionMoment
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl
    intro i _
    dsimp [θ]
    ring
  rw [interpolatedSelection, if_neg heq]
  change (∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) ∧ selectionMass p θ = q ∧
    selectionMoment p x θ = w
  refine ⟨hθ, ?_, ?_⟩
  · rw [hm, hm₀, hm₁]; ring
  · rw [hv]; nlinarith

theorem selection_interpolate (p x θ₀ θ₁ : ι → 𝕜)
    (h₀ : ∀ i, θ₀ i ∈ Set.Icc (0 : 𝕜) 1)
    (h₁ : ∀ i, θ₁ i ∈ Set.Icc (0 : 𝕜) 1) (q w : 𝕜)
    (hm₀ : selectionMass p θ₀ = q) (hm₁ : selectionMass p θ₁ = q)
    (hw₀ : selectionMoment p x θ₀ ≤ w) (hw₁ : w ≤ selectionMoment p x θ₁) :
    ∃ θ, (∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) ∧
      selectionMass p θ = q ∧ selectionMoment p x θ = w :=
  ⟨interpolatedSelection p x θ₀ θ₁ w,
    interpolatedSelection_spec p x θ₀ θ₁ h₀ h₁ q w hm₀ hm₁ hw₀ hw₁⟩

/-- The two families of call inequalities characterize fractional submeasures of
one fixed finite law. The statement includes zero or unit selected mass. -/
theorem fractional_selection_iff (p x : ι → 𝕜) (hp : ∀ i, 0 ≤ p i)
    (hsum : ∑ i, p i = 1) (q w : 𝕜) :
    (∃ θ, (∀ i, θ i ∈ Set.Icc (0 : 𝕜) 1) ∧
      selectionMass p θ = q ∧ selectionMoment p x θ = w) ↔
    0 ≤ q ∧ q ≤ 1 ∧ ∀ s,
      w - q * s ≤ selectionCall p x s ∧
      selectionMean p x - w - (1 - q) * s ≤ selectionCall p x s := by
  constructor
  · rintro ⟨θ, hθ, hm, hv⟩
    simpa only [hm, hv] using selection_necessary p x θ hp hsum hθ
  · rintro ⟨hq, hq1, hw⟩
    obtain ⟨s₁, θ₁, hθ₁, hm₁, hv₁, _⟩ := selection_upper_attained p x hp hsum q hq hq1
    obtain ⟨s₀, φ, hφ, hmφ, hvφ, _⟩ := selection_upper_attained p x hp hsum
      (1 - q) (by linarith) (by linarith)
    apply selection_interpolate p x (fun i => 1 - φ i) θ₁
      (fun i => ⟨by linarith [(hφ i).2], by linarith [(hφ i).1]⟩) hθ₁ q w
    · rw [selection_complement_mass p φ hsum, hmφ]; ring
    · exact hm₁
    · rw [selection_complement_moment, hvφ]
      linarith [(hw s₀).2]
    · linarith [(hw s₁).1]

/-- All leaves can be selected independently on the same anchor law. -/
theorem simultaneous_fractional_selection {J : Type*} (p x : ι → 𝕜)
    (hp : ∀ i, 0 ≤ p i) (hsum : ∑ i, p i = 1) (q w : J → 𝕜)
    (h : ∀ j, 0 ≤ q j ∧ q j ≤ 1 ∧ ∀ s,
      w j - q j * s ≤ selectionCall p x s ∧
      selectionMean p x - w j - (1 - q j) * s ≤ selectionCall p x s) :
    ∃ θ : J → ι → 𝕜, ∀ j, (∀ i, θ j i ∈ Set.Icc (0 : 𝕜) 1) ∧
      selectionMass p (θ j) = q j ∧ selectionMoment p x (θ j) = w j := by
  exact Classical.axiomOfChoice
    (fun j => (fractional_selection_iff p x hp hsum (q j) (w j)).mpr (h j))

end ReciprocalAnchor.ManyLeaf
