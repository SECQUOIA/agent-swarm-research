import Formal.MultilinearGap.FloorCoupling
import Formal.MultilinearGap.FloorGain

/-! A coefficient-independent coupling proves the marginal-floor cube bound. -/
namespace MultilinearGap
open CubicGap
noncomputable section

/-- Sum of the inverse guarantees of the floor law and independence. -/
def floorBound (τ e : ℝ) : ℝ := 1 / floorIntegral (floorLog τ) e + 2 / easyConstant

theorem floorBound_pos {τ e : ℝ} (hτ : 0 < τ) (he : 0 < e) : 0 < floorBound τ e := by
  unfold floorBound
  positivity [floorIntegral_pos (floorLog_pos hτ) he, easyConstant_pos]

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- The two component laws are mixed with weights proportional to their inverse
termwise gains. The law depends only on the point and scalar parameters. -/
def floorMixture (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e) : Law (Vertex I) :=
  Law.mix (floorLaw x hx τ hτ) (bernoulliLaw x hx)
    ((1 / floorIntegral (floorLog τ) e) / floorBound τ e)
    ((2 / easyConstant) / floorBound τ e)
    (by positivity [floorIntegral_pos (floorLog_pos hτ) he, floorBound_pos hτ he])
    (by positivity [easyConstant_pos, floorBound_pos hτ he])
    (by rw [← add_div]; exact div_self (ne_of_gt (floorBound_pos hτ he)))

theorem floorMixture_expect (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e) (f : Vertex I → ℝ) :
    (floorMixture x hx τ hτ e he).expect f =
      ((1 / floorIntegral (floorLog τ) e) * (floorLaw x hx τ hτ).expect f +
        (2 / easyConstant) * (bernoulliLaw x hx).expect f) / floorBound τ e := by
  simp only [floorMixture, Law.expect, Law.mix, add_mul, div_mul_eq_mul_div,
    Finset.sum_add_distrib, ← Finset.sum_div, mul_assoc, ← Finset.mul_sum, ← add_div]

theorem floorMixture_hasMeans (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e) :
    HasMeans (floorMixture x hx τ hτ e he) x := by
  intro i
  rw [floorMixture_expect, floorLaw_hasMeans x hx τ hτ i, bernoulliLaw_mean]
  rw [← add_mul]
  exact mul_div_cancel_left₀ (x i) (ne_of_gt (floorBound_pos hτ he))

theorem floorMixture_deficiency (x : I → ℝ) (hx : x ∈ cube I)
    (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e) (f : Vertex I → ℝ) (u : ℝ) :
    u - (floorMixture x hx τ hτ e he).expect f =
      ((1 / floorIntegral (floorLog τ) e) * (u - (floorLaw x hx τ hτ).expect f) +
        (2 / easyConstant) * (u - (bernoulliLaw x hx).expect f)) / floorBound τ e := by
  rw [floorMixture_expect]
  apply (eq_div_iff (ne_of_gt (floorBound_pos hτ he))).mpr
  rw [sub_mul, div_mul_cancel₀ _ (ne_of_gt (floorBound_pos hτ he))]
  unfold floorBound
  ring

/-- Every nonempty monomial receives the same guarantee from the same law. -/
theorem floorMixture_deficiency_nonempty (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (δ : ℝ) (hδ : 0 < δ) (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e)
    (hfloor : ∀ j, δ ≤ x j) (hτδ : τ / δ ≤ e)
    (i : I) (hi : i ∈ s) (hmin : ∀ j ∈ s, x i ≤ x j) :
    hullGap (monomial s) x / floorBound τ e ≤
      x i - (floorMixture x hx τ hτ e he).expect (fun v => monomial s (vertexPoint v)) := by
  let f := fun v => monomial s (vertexPoint v)
  have hnF := monomial_deficiency_nonneg s x i hi (floorLaw x hx τ hτ)
    (floorLaw_hasMeans x hx τ hτ)
  have hnI := monomial_deficiency_nonneg s x i hi (bernoulliLaw x hx)
    (fun j => bernoulliLaw_mean x hx j)
  have hIF : 0 < floorIntegral (floorLog τ) e := floorIntegral_pos (floorLog_pos hτ) he
  have hwF : 0 ≤ (1 / floorIntegral (floorLog τ) e) *
      (x i - (floorLaw x hx τ hτ).expect f) := mul_nonneg (by positivity) hnF
  have hwI : 0 ≤ (2 / easyConstant) * (x i - (bernoulliLaw x hx).expect f) :=
    mul_nonneg (by positivity [easyConstant_pos]) hnI
  rw [floorMixture_deficiency]
  apply div_le_div_of_nonneg_right _ (floorBound_pos hτ he).le
  by_cases heasy : 1 / 2 ≤ x i ∨ ∃ j ∈ s.erase i, x j ≤ 1 / 2
  · have he' := bernoulli_easy_gap s x hx i hi hmin heasy
    have hb : hullGap (monomial s) x ≤ (2 / easyConstant) *
        (x i - (bernoulliLaw x hx).expect f) := by
      rw [div_mul_eq_mul_div]
      apply (le_div_iff₀ easyConstant_pos).mpr
      dsimp [f]
      linarith
    exact hb.trans (le_add_of_nonneg_left hwF)
  · have hlow : x i ≤ 1 / 2 := by
      have : ¬1 / 2 ≤ x i := fun h => heasy (Or.inl h)
      linarith
    have hhigh : ∀ j ∈ s.erase i, 1 / 2 < x j := by
      intro j hj
      exact lt_of_not_ge (fun h => heasy (Or.inr ⟨j, hj, h⟩))
    have hu : 0 < x i := hδ.trans_le (hfloor i)
    have hτu : τ / x i ≤ e :=
      (div_le_div_of_nonneg_left hτ.le hδ (hfloor i)).trans hτδ
    have hg := floorLaw_unique_low_gain x hx τ hτ s i hi hlow hhigh he hu hτu
    have hg' := (mul_le_mul_of_nonneg_right
      (monomial_gap_le_min s x hx i hi hmin) hIF.le).trans hg
    have hb : hullGap (monomial s) x ≤ (1 / floorIntegral (floorLog τ) e) *
        (x i - (floorLaw x hx τ hτ).expect f) := by
      have hd := (le_div_iff₀ hIF).mpr hg'
      simpa [f, div_eq_mul_inv, mul_comm] using hd
    exact hb.trans (le_add_of_nonneg_right hwI)

/-- The shared coupling also covers empty and affine terms. -/
theorem floorMixture_deficiency_all (s : Finset I) (x : I → ℝ) (hx : x ∈ cube I)
    (δ : ℝ) (hδ : 0 < δ) (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e)
    (hfloor : ∀ j, δ ≤ x j) (hτδ : τ / δ ≤ e) :
    (1 / floorBound τ e) * hullGap (monomial s) x ≤ monomialUpper s x -
      (floorMixture x hx τ hτ e he).expect (fun v => monomial s (vertexPoint v)) := by
  by_cases hs : s.Nonempty
  · obtain ⟨i, hi, hmin⟩ := monomial_min_anchor s hs x
    rw [monomialUpper_eq_anchor s x i hi hmin]
    simpa [div_eq_mul_inv, mul_comm] using
      floorMixture_deficiency_nonempty s x hx δ hδ τ hτ e he hfloor hτδ i hi hmin
  · have : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp hs
    subst s
    simp [monomial_gap_empty x hx, monomial]

/-- The finite marginal-floor bound holds for all nonnegative coefficients, all
finite dimensions, and all degrees, with actual polynomial graph-hull gaps. -/
theorem floor_cube_gap_bound (supports : Finset (Finset I))
    (a : Finset I → ℝ) (ha : ∀ s ∈ supports, 0 ≤ a s)
    (x : I → ℝ) (hx : x ∈ cube I)
    (δ : ℝ) (hδ : 0 < δ) (τ : ℝ) (hτ : 0 < τ) (e : ℝ) (he : 0 < e)
    (hfloor : ∀ j, δ ≤ x j) (hτδ : τ / δ ≤ e) :
    weightedTermwiseGap supports a x ≤
      floorBound τ e * hullGap (supportPolynomial supports a) x := by
  have h := coupling_gap_bound_general supports a ha x hx (1 / floorBound τ e)
    (div_pos one_pos (floorBound_pos hτ he)) (floorMixture x hx τ hτ e he)
    (floorMixture_hasMeans x hx τ hτ e he)
    (fun s _ => floorMixture_deficiency_all s x hx δ hδ τ hτ e he hfloor hτδ)
  simpa using h

end
end MultilinearGap
