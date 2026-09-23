import Formal.MultilinearGap.BoxTransfer
import Formal.MultilinearGap.MonomialEnvelope

/-! The actual gap-ratio classes with a lower marginal bound, and transfer to
original nonnegative boxes, including fixed coordinates. -/

namespace MultilinearGap

open CubicGap

noncomputable section

/-- Every dimension and degree are allowed. Included coefficients are positive. -/
def floorRatios (δ : ℝ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    (∀ s ∈ S, 0 < a s) ∧ x ∈ cube I ∧ (∀ i, δ ≤ x i) ∧
      0 < hullGap (supportPolynomial S a) x ∧
      r = weightedTermwiseGap S a x / hullGap (supportPolynomial S a) x}

/-- The stronger two-sided constraint on every coordinate mean. -/
def stripRatios (δ : ℝ) : Set ℝ := {r | ∃ (I : Type) (hI : Fintype I)
    (hEq : DecidableEq I),
  letI := hI
  letI := hEq
  ∃ (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    (∀ s ∈ S, 0 < a s) ∧ x ∈ cube I ∧ (∀ i, δ ≤ x i ∧ x i ≤ 1 - δ) ∧
      0 < hullGap (supportPolynomial S a) x ∧
      r = weightedTermwiseGap S a x / hullGap (supportPolynomial S a) x}

def floorSupremum (δ : ℝ) : ℝ := sSup (floorRatios δ)
def stripSupremum (δ : ℝ) : ℝ := sSup (stripRatios δ)

theorem floorRatios_antitone : Antitone floorRatios := by
  intro δ ε hδε r hr
  obtain ⟨I, hI, hEq, S, a, x, ha, hx, hf, hg, he⟩ := hr
  exact ⟨I, hI, hEq, S, a, x, ha, hx, fun i => hδε.trans (hf i), hg, he⟩

theorem stripRatios_subset_floorRatios (δ : ℝ) : stripRatios δ ⊆ floorRatios δ := by
  rintro r ⟨I, hI, hEq, S, a, x, ha, hx, hs, hg, he⟩
  exact ⟨I, hI, hEq, S, a, x, ha, hx, fun i => (hs i).1, hg, he⟩

/-- A common bound for all nonnegative polynomials at floor-constrained points. -/
def CubeFloorBound (δ U : ℝ) : Prop :=
  ∀ (I : Type) [Fintype I] [DecidableEq I]
    (S : Finset (Finset I)) (a : Finset I → ℝ) (x : I → ℝ),
    (∀ s ∈ S, 0 ≤ a s) → x ∈ cube I → (∀ i, δ ≤ x i) →
      weightedTermwiseGap S a x ≤ U * hullGap (supportPolynomial S a) x

theorem floorRatios_le {δ U : ℝ} (hU : CubeFloorBound δ U)
    {r : ℝ} (hr : r ∈ floorRatios δ) : r ≤ U := by
  obtain ⟨I, hI, hEq, S, a, x, ha, hx, hf, hg, rfl⟩ := hr
  let _ := hI
  let _ := hEq
  exact (div_le_iff₀ hg).mpr (hU I S a x (fun s hs => (ha s hs).le) hx hf)

theorem floorRatios_bddAbove {δ U : ℝ} (hU : CubeFloorBound δ U) :
    BddAbove (floorRatios δ) := ⟨U, fun _ hr => floorRatios_le hU hr⟩

private theorem bilinear_gap_positive {v : ℝ} (hv : 0 < v) (hv1 : v < 1) :
    0 < hullGap (monomial (Finset.univ : Finset (Fin 2))) (fun _ => v) := by
  rw [monomial_hullGap_of_min_coordinate _ _ (fun _ => ⟨hv.le, hv1.le⟩)
    0 (Finset.mem_univ _) (fun _ _ => le_rfl)]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul,
    Nat.cast_ofNat]
  apply sub_pos.mpr
  exact max_lt hv (by linarith)

private theorem bilinear_polynomial :
    supportPolynomial {(Finset.univ : Finset (Fin 2))} (fun _ => 1) =
      monomial Finset.univ := by
  funext x
  simp [supportPolynomial]

/-- One bilinear monomial has ratio one at every interior equal-mean point. -/
theorem one_mem_floorRatios {δ : ℝ} (hδ : 0 < δ) (hδ1 : δ < 1) :
    1 ∈ floorRatios δ := by
  let v := (1 + δ) / 2
  have hv : 0 < v := by dsimp [v]; linarith
  have hv1 : v < 1 := by dsimp [v]; linarith
  have hg := bilinear_gap_positive hv hv1
  refine ⟨Fin 2, inferInstance, inferInstance, {Finset.univ}, fun _ => 1,
    fun _ => v, by simp, fun _ => ⟨hv.le, hv1.le⟩,
    (fun _ => by dsimp [v]; linarith), ?_, ?_⟩
  · simpa only [bilinear_polynomial] using hg
  · simp only [weightedTermwiseGap, bilinear_polynomial, Finset.sum_singleton, one_mul]
    exact (div_self hg.ne').symm

/-- The midpoint gives a nonempty strip class through the endpoint floor one half. -/
theorem one_mem_stripRatios {δ : ℝ} (hδ : δ ≤ 1 / 2) : 1 ∈ stripRatios δ := by
  have hg := bilinear_gap_positive (by norm_num : (0 : ℝ) < 1 / 2)
    (by norm_num : (1 / 2 : ℝ) < 1)
  refine ⟨Fin 2, inferInstance, inferInstance, {Finset.univ}, fun _ => 1,
    fun _ => 1 / 2, by simp, fun _ => by norm_num,
    (fun _ => ⟨hδ, by linarith⟩), ?_, ?_⟩
  · simpa only [bilinear_polynomial] using hg
  · simp only [weightedTermwiseGap, bilinear_polynomial, Finset.sum_singleton, one_mul]
    exact (div_self hg.ne').symm

theorem floorRatios_nonempty {δ : ℝ} (hδ : 0 < δ) (hδ1 : δ < 1) :
    (floorRatios δ).Nonempty := ⟨1, one_mem_floorRatios hδ hδ1⟩

theorem stripRatios_nonempty {δ : ℝ} (hδ : δ ≤ 1 / 2) :
    (stripRatios δ).Nonempty := ⟨1, one_mem_stripRatios hδ⟩

variable {I : Type*} [Fintype I] [DecidableEq I]

/-- Preserve the requested floor when assigning arbitrary means to fixed coordinates. -/
def floorBoxParameter (δ : ℝ) (l u x : I → ℝ) (i : I) : ℝ :=
  if l i = u i then δ else (x i - l i) / (u i - l i)

omit [Fintype I] [DecidableEq I] in
theorem floorBoxParameter_mem {δ : ℝ} (hδ : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (l u x : I → ℝ) (hlu : ∀ i, l i ≤ u i) (hx : x ∈ coordinateBox l u) :
    floorBoxParameter δ l u x ∈ cube I := by
  intro i
  unfold floorBoxParameter
  split_ifs with he
  · exact ⟨hδ, hδ1⟩
  · have hd : 0 < u i - l i := sub_pos.mpr (lt_of_le_of_ne (hlu i) he)
    exact ⟨div_nonneg (sub_nonneg.mpr (hx i).1) hd.le,
      (div_le_one hd).mpr (sub_le_sub_right (hx i).2 _)⟩

omit [Fintype I] [DecidableEq I] in
theorem floorBoxParameter_floor (δ : ℝ) (l u x : I → ℝ)
    (hf : ∀ i, l i ≠ u i → δ ≤ (x i - l i) / (u i - l i)) :
    ∀ i, δ ≤ floorBoxParameter δ l u x i := by
  intro i
  unfold floorBoxParameter
  split_ifs with he
  · exact le_rfl
  · exact hf i he

omit [Fintype I] [DecidableEq I] in
theorem floorBoxParameter_map (δ : ℝ) (l u x : I → ℝ)
    (hx : x ∈ coordinateBox l u) :
    boxPoint l u (floorBoxParameter δ l u x) = x := by
  funext i
  dsimp [boxPoint, floorBoxParameter]
  split_ifs with he
  · have hi := hx i
    simp only [he, sub_self, zero_mul, add_zero]
    linarith
  · rw [mul_div_cancel₀ _ (sub_ne_zero.mpr (Ne.symm he))]
    ring

/-- The floor condition is preserved by positive expansion of original terms. -/
theorem floor_gap_bound_box_transfer (δ C : ℝ)
    (hbound : ∀ (S : Finset (Finset I)) (b : Finset I → ℝ),
      (∀ s ∈ S, 0 ≤ b s) → ∀ p ∈ cube I, (∀ i, δ ≤ p i) →
        weightedTermwiseGap S b p ≤ C * hullGap (supportPolynomial S b) p)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (p : I → ℝ) (hp : p ∈ cube I) (hf : ∀ i, δ ≤ p i) :
    boxTermwiseGap S a l u (boxPoint l u p) ≤
      C * boxHullGap l u (supportPolynomial S a) (boxPoint l u p) := by
  have he : (fun q => supportPolynomial S a (boxPoint l u q)) =
      supportPolynomial (boxExpansionSupports S) (boxPolynomialCoefficient S a l u) := by
    funext q
    exact supportPolynomial_box_expansion S a l u q
  rw [boxHullGap_eq_of_mem l u hlu _ p hp, he]
  exact (boxTermwiseGap_le_expansion S a ha l u hl hlu p hp).trans
    (hbound _ _ (fun t _ => boxPolynomialCoefficient_nonneg S a ha l u hl hlu t) p hp hf)

/-- Bound the original, unexpanded termwise gap at the actual box point. -/
theorem floor_gap_bound_on_box (δ C : ℝ) (hδ : 0 ≤ δ) (hδ1 : δ ≤ 1)
    (hbound : ∀ (S : Finset (Finset I)) (b : Finset I → ℝ),
      (∀ s ∈ S, 0 ≤ b s) → ∀ p ∈ cube I, (∀ i, δ ≤ p i) →
        weightedTermwiseGap S b p ≤ C * hullGap (supportPolynomial S b) p)
    (S : Finset (Finset I)) (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (x : I → ℝ) (hx : x ∈ coordinateBox l u)
    (hf : ∀ i, l i ≠ u i → δ ≤ (x i - l i) / (u i - l i)) :
    boxTermwiseGap S a l u x ≤ C * boxHullGap l u (supportPolynomial S a) x := by
  have hb := floor_gap_bound_box_transfer δ C hbound S a ha l u hl hlu
    (floorBoxParameter δ l u x) (floorBoxParameter_mem hδ hδ1 l u x hlu hx)
    (floorBoxParameter_floor δ l u x hf)
  simpa only [floorBoxParameter_map δ l u x hx] using hb

end
end MultilinearGap
