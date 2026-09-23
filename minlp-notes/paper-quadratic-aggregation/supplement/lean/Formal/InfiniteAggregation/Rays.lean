import Mathlib

/-! Scalar certificates for the indispensable good multiplier rays. -/

noncomputable section

namespace InfiniteAggregation

/-- The boundary ray indexed by a positive real parameter. -/
def rayWeight (τ : ℝ) : Fin 3 → ℝ := ![τ, τ⁻¹, 2]

/-- A nonzero positive multiple of the specified boundary ray. -/
def SameRay (w : Fin 3 → ℝ) (τ : ℝ) : Prop :=
  ∃ a : ℝ, 0 < a ∧ w = a • rayWeight τ

/-- Weighted AM--GM with the equality case retained. -/
theorem ray_slack_nonpos {a b c τ : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b)
    (_hc : 0 ≤ c) (hcone : c ^ 2 ≤ 4 * a * b) (hτ : 0 < τ) :
    -a / τ - b * τ + c ≤ 0 := by
  have ht0 : τ ≠ 0 := ne_of_gt hτ
  have hp : 0 ≤ a / τ + b * τ := add_nonneg (div_nonneg ha (le_of_lt hτ))
    (mul_nonneg hb (le_of_lt hτ))
  have hid : (a / τ + b * τ) ^ 2 - 4 * a * b = (a / τ - b * τ) ^ 2 := by
    field_simp
    ring
  have hs := sq_nonneg (a / τ - b * τ)
  simp only [neg_div] at *
  nlinarith

/-- Vanishing slack identifies the boundary ray, including its scale. -/
theorem ray_slack_eq_iff {w : Fin 3 → ℝ} {τ : ℝ}
    (hn : ∀ i, 0 ≤ w i) (hw : w ≠ 0)
    (hcone : (w 2) ^ 2 ≤ 4 * w 0 * w 1) (hτ : 0 < τ) :
    -w 0 / τ - w 1 * τ + w 2 = 0 ↔ SameRay w τ := by
  have ht0 : τ ≠ 0 := ne_of_gt hτ
  simp only [neg_div]
  constructor
  · intro heq
    have hid : (w 0 / τ + w 1 * τ) ^ 2 - 4 * w 0 * w 1 =
        (w 0 / τ - w 1 * τ) ^ 2 := by
      field_simp
      ring
    have hequal : w 0 / τ = w 1 * τ := by
      have hs := sq_nonneg (w 0 / τ - w 1 * τ)
      have hsum : (w 0 / τ + w 1 * τ) ^ 2 = (w 2) ^ 2 :=
        congrArg (fun x : ℝ => x ^ 2) (by linarith)
      have hz : (w 0 / τ - w 1 * τ) ^ 2 = 0 := by
        nlinarith only [hs, hid, hcone, hsum]
      nlinarith [sq_nonneg (w 0 / τ - w 1 * τ)]
    have h0 : w 0 = (w 2 / 2) * τ := by
      have hdiv : w 0 / τ = w 2 / 2 := by linarith
      exact (div_eq_iff ht0).mp hdiv
    have h1 : w 1 = (w 2 / 2) * τ⁻¹ := by
      have hm : w 1 * τ = w 2 / 2 := by linarith
      apply (mul_right_cancel₀ ht0)
      rw [hm]
      field_simp
    have hc : 0 < w 2 := by
      have hnn := hn 2
      by_contra h
      have hz : w 2 = 0 := le_antisymm (not_lt.mp h) hnn
      apply hw
      funext i
      fin_cases i <;> simp_all
    refine ⟨w 2 / 2, by positivity, ?_⟩
    funext i
    fin_cases i <;> simp [rayWeight, h0, h1]
  · rintro ⟨a, ha, rfl⟩
    simp [rayWeight]
    field_simp
    ring

/-- Distinct positive parameters specify distinct rays. -/
theorem sameRay_unique {w : Fin 3 → ℝ} {τ σ : ℝ}
    (ht : SameRay w τ) (hs : SameRay w σ) : τ = σ := by
  obtain ⟨a, ha, hea⟩ := ht
  obtain ⟨b, hb, heb⟩ := hs
  have h := hea.symm.trans heb
  have h2 := congrFun h 2
  have h0 := congrFun h 0
  change a * 2 = b * 2 at h2
  change a * τ = b * σ at h0
  have hab : a = b := by linarith
  rw [← hab] at h0
  exact mul_left_cancel₀ (ne_of_gt ha) h0

/-- Every finite multiplier family omits one parameter in the witness interval. -/
theorem exists_omitted_ray {W : Set (Fin 3 → ℝ)} (hW : W.Finite) :
    ∃ τ ∈ Set.Icc (1 : ℝ) 2, ∀ w ∈ W, ¬SameRay w τ := by
  have hf : (⋃ w ∈ W, {τ : ℝ | SameRay w τ}).Finite := by
    apply hW.biUnion
    intro w _
    apply Set.Subsingleton.finite
    intro τ ht σ hs
    exact sameRay_unique ht hs
  obtain ⟨τ, hτ, hnot⟩ := (Set.Icc_infinite (by norm_num : (1 : ℝ) < 2)).exists_notMem_finite hf
  refine ⟨τ, hτ, ?_⟩
  intro w hw hr
  apply hnot
  exact Set.mem_iUnion.mpr ⟨w, Set.mem_iUnion.mpr ⟨hw, hr⟩⟩

/-- The concrete witness Gram matrix is positive definite throughout the interval. -/
theorem witness_gram_bounds {τ : ℝ} (hτ : τ ∈ Set.Icc (1 : ℝ) 2) :
    0 < 1 - (1 / 10 : ℝ) / τ ∧
    (2 / 5 : ℝ) ^ 2 < (1 - (1 / 10 : ℝ) / τ) * (1 - (1 / 10 : ℝ) * τ) := by
  have hp : (4 / 5 : ℝ) ≤ 1 - (1 / 10 : ℝ) / τ := by
    have ht : 0 < τ := lt_of_lt_of_le (by norm_num) hτ.1
    have hd : (1 / 10 : ℝ) / τ ≤ 1 / 5 := (div_le_iff₀ ht).mpr (by nlinarith [hτ.1])
    linarith
  have hq : (4 / 5 : ℝ) ≤ 1 - (1 / 10 : ℝ) * τ := by nlinarith [hτ.2]
  constructor
  · linarith
  · have hprod := mul_le_mul hp hq (by norm_num : (0 : ℝ) ≤ 4 / 5) (by linarith)
    nlinarith

end InfiniteAggregation
