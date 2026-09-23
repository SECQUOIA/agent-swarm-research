import Formal.MultilinearGap.PhysicalEnvelope

/-!
# Convex cardinality factors: finite tables and exact lower envelopes

The table is required to be convex only on the counts a support can attain.
Its entries may be negative and its first differences may have either sign.
The lower endpoint is attained by an actual law with the prescribed means.
-/

namespace MultilinearGap

open CubicGap

noncomputable section

/-- Discrete convexity on the finite table of attainable counts. -/
def ConvexCountTable (φ : ℕ → ℝ) (d : ℕ) : Prop :=
  ∀ k, k + 2 ≤ d → φ (k + 1) - φ k ≤ φ (k + 2) - φ (k + 1)

/-- Continue the last slope beyond the end of a finite table. -/
def countTableExtension (φ : ℕ → ℝ) (d k : ℕ) : ℝ :=
  φ (min k d) + ((k - d : ℕ) : ℝ) * (φ d - φ (d - 1))

theorem countTableExtension_eq (φ : ℕ → ℝ) {d k : ℕ} (hk : k ≤ d) :
    countTableExtension φ d k = φ k := by
  simp [countTableExtension, min_eq_left hk, Nat.sub_eq_zero_of_le hk]

private theorem countTableExtension_diff (φ : ℕ → ℝ) {d : ℕ} (hd : 0 < d)
    (k : ℕ) :
    countTableExtension φ d (k + 1) - countTableExtension φ d k =
      φ (min k (d - 1) + 1) - φ (min k (d - 1)) := by
  by_cases hk : k < d
  · rw [countTableExtension_eq φ (by omega), countTableExtension_eq φ (by omega),
      min_eq_left (by omega)]
  · have hdk : d ≤ k := by omega
    have hs : k + 1 - d = k - d + 1 := by omega
    have he : d - 1 + 1 = d := by omega
    simp only [countTableExtension, min_eq_right (show d ≤ k + 1 by omega),
      min_eq_right hdk, min_eq_right (show d - 1 ≤ k by omega), hs,
      Nat.cast_add, Nat.cast_one, he]
    ring

theorem countTableExtension_convex {φ : ℕ → ℝ} {d : ℕ}
    (hφ : ConvexCountTable φ d) (k : ℕ) :
    countTableExtension φ d (k + 1) - countTableExtension φ d k ≤
      countTableExtension φ d (k + 2) - countTableExtension φ d (k + 1) := by
  by_cases hd : d = 0
  · subst d
    simp [countTableExtension]
  · have hd' : 0 < d := by omega
    rw [countTableExtension_diff φ hd',
      show k + 2 = (k + 1) + 1 by omega, countTableExtension_diff φ hd']
    by_cases hk : k + 2 ≤ d
    · rw [min_eq_left (show k ≤ d - 1 by omega),
        min_eq_left (show k + 1 ≤ d - 1 by omega)]
      exact hφ k hk
    · rw [min_eq_right (show d - 1 ≤ k by omega),
        min_eq_right (show d - 1 ≤ k + 1 by omega)]

variable {I : Type*}

/-- The piecewise affine interpolation of the count table at the mean count. -/
def cardinalityLower (φ : ℕ → ℝ) (s : Finset I) (x : I → ℝ) : ℝ :=
  (1 - countFrac s x) * φ (countFloor s x) +
    countFrac s x * φ (countFloor s x + 1)

theorem meanSum_le_card {s : Finset I} {x : I → ℝ} (hx : x ∈ cube I) :
    meanSum s x ≤ s.card := by
  simpa [meanSum] using Finset.sum_le_sum (s := s) (fun i _ => (hx i).2)

theorem countFloor_le_card {s : Finset I} {x : I → ℝ} (hx : x ∈ cube I) :
    countFloor s x ≤ s.card := by
  exact_mod_cast (countFloor_le hx).trans (meanSum_le_card hx)

theorem countFrac_eq_zero_of_floor_eq_card {s : Finset I} {x : I → ℝ}
    (hx : x ∈ cube I) (he : countFloor s x = s.card) : countFrac s x = 0 := by
  have hle := meanSum_le_card (s := s) hx
  have hlo := countFloor_le (s := s) hx
  rw [he] at hlo
  unfold countFrac
  rw [he]
  linarith

theorem cardinalityLower_extension (φ : ℕ → ℝ) (s : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) :
    cardinalityLower (countTableExtension φ s.card) s x = cardinalityLower φ s x := by
  have hfloor := countFloor_le_card (s := s) hx
  unfold cardinalityLower
  rw [countTableExtension_eq φ hfloor]
  by_cases h : countFloor s x < s.card
  · rw [countTableExtension_eq φ (by omega)]
  · rw [countFrac_eq_zero_of_floor_eq_card hx (by omega)]
    ring

variable [Fintype I] [DecidableEq I]

/-- Every feasible law is bounded below by the interpolated finite table. -/
theorem cardinalityLower_le_expect (φ : ℕ → ℝ) (s : Finset I)
    (hφ : ConvexCountTable φ s.card) (x : I → ℝ) (hx : x ∈ cube I)
    (μ : Law (Vertex I)) (hm : HasMeans μ x) :
    cardinalityLower φ s x ≤ μ.expect (fun v => φ (countOn s v)) := by
  have h := convex_count_expect_lower (countTableExtension φ s.card)
    (countTableExtension_convex hφ) s x μ hm
  change cardinalityLower (countTableExtension φ s.card) s x ≤ _ at h
  rw [cardinalityLower_extension φ s x hx] at h
  simpa only [countTableExtension_eq φ (countOn_le_card s _)] using h

/-- The same adjacent-count law attains every count-table interpolation. -/
theorem exists_cardinalityLower_law (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      ∀ φ : ℕ → ℝ, μ.expect (fun v => φ (countOn s v)) = cardinalityLower φ s x :=
  exists_adjacentLaw s x hx

omit [Fintype I] in
/-- A separately affine factor with the stated binary values has exactly this
lower graph-hull endpoint. This includes the multiaffine interpolant, rather
than substitution of the mean count into a continuous convex function. -/
theorem cardinality_minimum [Finite I] (φ : ℕ → ℝ) (s : Finset I)
    (hφ : ConvexCountTable φ s.card) (f : (I → ℝ) → ℝ)
    (hf : SeparatelyAffine f)
    (hv : ∀ v : Vertex I, f (vertexPoint v) = φ (countOn s v))
    (x : I → ℝ) (hx : x ∈ cube I) :
    IsLeast (envelopeValues f x) (cardinalityLower φ s x) := by
  let := Fintype.ofFinite I
  apply minimum_from_laws f hf
  · intro μ hm
    simp only [hv]
    exact cardinalityLower_le_expect φ s hφ x hx μ hm
  · obtain ⟨μ, hm, hc⟩ := exists_cardinalityLower_law s x hx
    exact ⟨μ, hm, by simpa only [hv] using hc φ⟩

end
end MultilinearGap
