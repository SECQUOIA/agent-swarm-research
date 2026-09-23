import QipmFormal.Mixture.Defs

/-!
# Residual bounds from coefficient locality

All residual estimates below start with actual base and neighboring matrices.
Dependent positions are allowed to repeat a bit within a row.
-/
namespace QipmFormal.Mixture
noncomputable section
open scoped BigOperators

variable {I R C : Type*} [Fintype I] [Fintype R] [Fintype C]

omit [Fintype C] in
/-- Cauchy--Schwarz with an explicit support size. -/
theorem sum_square_le_card_mul (S : Finset C) (f : C → ℝ) :
    (∑ j ∈ S, f j) ^ 2 ≤ (S.card : ℝ) * ∑ j ∈ S, (f j) ^ 2 := by
  simpa using (Finset.sum_mul_sq_le_sq_mul_sq S (fun _ => (1 : ℝ)) f)

omit [Fintype R] in
/-- The residual of a probability mixture is the weighted matrix-change sum. -/
theorem residual_mix_eq (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (b : R → ℝ) (w : I → ℝ)
    (hw : ProbWeights w)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r) (r : R) :
    residual A (mix w x) b r =
      ∑ j, ∑ i, w i * ((A r j - A' i r j) * x i j) := by
  have hb : ∑ i, w i * b r = b r := by rw [← Finset.sum_mul, hw.2, one_mul]
  simp only [residual, mix, Finset.mul_sum]
  rw [Finset.sum_comm]
  calc
    (∑ i, ∑ j, A r j * (w i * x i j)) - b r =
        ∑ i, w i * ((∑ j, A r j * x i j) - b r) := by
      simp only [mul_sub, Finset.sum_sub_distrib]
      rw [hb]
      congr 1
      apply Finset.sum_congr rfl
      intro i _
      simp only [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = ∑ i, ∑ j, w i * ((A r j - A' i r j) * x i j) := by
      apply Finset.sum_congr rfl
      intro i _
      rw [← hfeas i r, ← Finset.sum_sub_distrib, Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro j _
      ring
    _ = _ := Finset.sum_comm

/-- Total number of coefficient positions bearing a given bit label. -/
def incidence [DecidableEq I] (D : R → Finset C) (label : R → C → I) (i : I) : ℕ :=
  ∑ r, ((D r).filter fun j => label r j = i).card

omit [Fintype C] in
/-- Sum over positions equals sum over bit incidences, including repeated labels. -/
theorem incidence_sum [DecidableEq I] (D : R → Finset C) (label : R → C → I)
    (f : I → ℝ) :
    (∑ r, ∑ j ∈ D r, f (label r j)) = ∑ i, (incidence D label i : ℝ) * f i := by
  classical
  simp only [incidence, Nat.cast_sum, Finset.sum_mul]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro r _
  calc
    (∑ j ∈ D r, f (label r j)) = ∑ j ∈ D r, ∑ i, if label r j = i then f i else 0 := by
      simp
    _ = ∑ i, ∑ j ∈ D r, if label r j = i then f i else 0 := Finset.sum_comm
    _ = _ := by simp [← Finset.sum_filter]

omit [Fintype R] in
/-- Locality collapses each dependent coefficient to its designated neighbor. -/
theorem residual_mix_local_eq (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (hw : ProbWeights w)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) (r : R) :
    residual A (mix w x) b r =
      ∑ j ∈ D r, w (label r j) *
        ((A r j - A' (label r j) r j) * x (label r j) j) := by
  classical
  rw [residual_mix_eq A A' x b w hw hfeas r]
  rw [← Finset.sum_subset (Finset.subset_univ (D r))]
  · apply Finset.sum_congr rfl
    intro j hj
    apply Finset.sum_eq_single (label r j)
    · intro i _ hi
      rw [hlocal i r j (Or.inr (Ne.symm hi))]
      ring
    · simp
  · intro j _ hj
    apply Finset.sum_eq_zero
    intro i _
    rw [hlocal i r j (Or.inl hj)]
    ring

omit [Fintype I] [Fintype C] in
/-- Cauchy--Schwarz for the changes at the designated positions. -/
theorem localChange_positions_bound (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    :
    sqNorm (fun r => ∑ j ∈ D r, w (label r j) *
      ((A r j - A' (label r j) r j) * x (label r j) j)) ≤
      4 * s * B ^ 2 * H ^ 2 * ∑ r, ∑ j ∈ D r, (w (label r j)) ^ 2 := by
  classical
  have ht (i : I) (r : R) (j : C) :
      (w i * ((A r j - A' i r j) * x i j)) ^ 2 ≤
        4 * B ^ 2 * H ^ 2 * (w i) ^ 2 := by
    have hd : |A r j - A' i r j| ≤ 2 * B :=
      (abs_sub _ _).trans (by linarith [hA r j, hA' i r j])
    have hm : |(A r j - A' i r j) * x i j| ≤ 2 * B * H := by
      rw [abs_mul]
      exact mul_le_mul hd (hx i j) (abs_nonneg _) (by positivity)
    have hsq := sq_le_sq₀ (abs_nonneg ((A r j - A' i r j) * x i j))
      (show 0 ≤ 2 * B * H by positivity)
    have hh : ((A r j - A' i r j) * x i j) ^ 2 ≤ (2 * B * H) ^ 2 := by
      simpa only [sq_abs] using hsq.mpr hm
    calc
      _ = (w i) ^ 2 * (((A r j - A' i r j) * x i j) ^ 2) := mul_pow _ _ _
      _ ≤ (w i) ^ 2 * (2 * B * H) ^ 2 := mul_le_mul_of_nonneg_left hh (sq_nonneg _)
      _ = _ := by ring
  unfold sqNorm
  calc
    _ ≤ ∑ r, (s : ℝ) * (4 * B ^ 2 * H ^ 2 * ∑ j ∈ D r, (w (label r j)) ^ 2) := by
      apply Finset.sum_le_sum
      intro r _
      calc
        _ ≤ ((D r).card : ℝ) * ∑ j ∈ D r,
          (w (label r j) * ((A r j - A' (label r j) r j) * x (label r j) j)) ^ 2 :=
            sum_square_le_card_mul _ _
        _ ≤ (s : ℝ) * ∑ j ∈ D r,
          (w (label r j) * ((A r j - A' (label r j) r j) * x (label r j) j)) ^ 2 :=
            mul_le_mul_of_nonneg_right (Nat.cast_le.mpr (hs r))
              (Finset.sum_nonneg fun _ _ => sq_nonneg _)
        _ ≤ _ := by
          apply mul_le_mul_of_nonneg_left _ (Nat.cast_nonneg _)
          rw [Finset.mul_sum]
          exact Finset.sum_le_sum fun j _ => ht (label r j) r j
    _ = _ := by simp only [← Finset.mul_sum]; ring

/-- Weighted single-flip bound, stated first directly as a sum over positions. -/
theorem weighted_residual_positions (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    sqNorm (residual A (mix w x) b) ≤
      4 * s * B ^ 2 * H ^ 2 * ∑ r, ∑ j ∈ D r, (w (label r j)) ^ 2 := by
  have he : residual A (mix w x) b = fun r => ∑ j ∈ D r,
      w (label r j) * ((A r j - A' (label r j) r j) * x (label r j) j) := by
    funext r
    exact residual_mix_local_eq A A' x b w D label hw hfeas hlocal r
  rw [he]
  exact localChange_positions_bound A A' x w D label s B H hB hH hA hA' hx hs

/-- Weighted residual bound with the exact bit-incidence profile. -/
theorem weighted_residual_bound [DecidableEq I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hw : ProbWeights w) (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    sqNorm (residual A (mix w x) b) ≤
      4 * s * B ^ 2 * H ^ 2 * ∑ i, (incidence D label i : ℝ) * (w i) ^ 2 := by
  simpa only [incidence_sum D label (fun i => w i ^ 2)] using
    weighted_residual_positions A A' x b w D label s B H hw hB hH hA hA' hx hs hfeas hlocal

/-- Total dependent incidence. -/
def totalIncidence (D : R → Finset C) : ℕ := ∑ r, (D r).card

/-- Turning a squared residual estimate into its Euclidean norm estimate. -/
theorem euclideanNorm_le_of_sqNorm_le (v : R → ℝ) (T : ℝ)
    (hT : 0 ≤ T) (hv : sqNorm v ≤ T ^ 2) : euclideanNorm v ≤ T := by
  have hn : 0 ≤ euclideanNorm v := Real.sqrt_nonneg _
  have he := euclideanNorm_sq v
  nlinarith

/-- The uniform single-flip theorem, including its exact square-root constant.
The index type can itself be the subtype of sensitive bits. -/
theorem uniform_residual_bound [Nonempty I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    euclideanNorm (residual A (mix (uniformWeight I) x) b) ≤
      2 * B * H * Real.sqrt ((s : ℝ) * totalIncidence D) / Fintype.card I := by
  have hn : (Fintype.card I : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos)
  have hsum : (∑ r, ∑ j ∈ D r, (uniformWeight I (label r j)) ^ 2) =
      (totalIncidence D : ℝ) * ((Fintype.card I : ℝ)⁻¹) ^ 2 := by
    simp [uniformWeight, totalIncidence, Nat.cast_sum, Finset.sum_mul]
  have hh := weighted_residual_positions A A' x b (uniformWeight I) D label s B H
    (uniformWeight_prob I) hB hH hA hA' hx hs hfeas hlocal
  rw [hsum] at hh
  apply euclideanNorm_le_of_sqNorm_le _ _ (by positivity)
  have hr : Real.sqrt ((s : ℝ) * totalIncidence D) ^ 2 = (s : ℝ) * totalIncidence D :=
    Real.sq_sqrt (by positivity)
  calc
    _ ≤ _ := hh
    _ = _ := by rw [div_pow, mul_pow, mul_pow, mul_pow, hr]; field_simp; ring

omit [Fintype I] [Fintype C] in
/-- A bit with no dependent positions changes no coefficient. -/
theorem zero_incidence_matrix_eq [DecidableEq I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (D : R → Finset C) (label : R → C → I) (i : I)
    (hzero : incidence D label i = 0)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    A' i = A := by
  classical
  funext r j
  apply hlocal
  by_cases hj : j ∈ D r
  · right
    intro hl
    have hc : ((D r).filter fun j => label r j = i).card = 0 := by
      have hh := Finset.single_le_sum (fun r _ => Nat.zero_le
        (((D r).filter fun j => label r j = i).card)) (Finset.mem_univ r)
      change _ ≤ incidence D label i at hh
      omega
    have hm : j ∈ (D r).filter fun j => label r j = i := Finset.mem_filter.mpr ⟨hj, hl⟩
    rw [Finset.card_eq_zero.mp hc] at hm
    simp at hm
  · exact Or.inl hj

omit [Fintype I] in
/-- A zero-incidence neighbor witness is exactly feasible for the base instance. -/
theorem zero_incidence_feasible [DecidableEq I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (label : R → C → I) (i : I)
    (hzero : incidence D label i = 0)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    residual A (x i) b = 0 := by
  have he := zero_incidence_matrix_eq A A' D label i hzero hlocal
  funext r
  simp only [residual, Pi.zero_apply]
  rw [← he, hfeas, sub_self]

/-- Matrix-change mixture, without requiring a common right-hand side. -/
def matrixChangeMix (A : R → C → ℝ) (A' : I → R → C → ℝ)
    (x : I → C → ℝ) (w : I → ℝ) : R → ℝ :=
  fun r => ∑ j, ∑ i, w i * ((A r j - A' i r j) * x i j)

omit [Fintype R] in
theorem matrixChangeMix_local_eq (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) (r : R) :
    matrixChangeMix A A' x w r = ∑ j ∈ D r, w (label r j) *
      ((A r j - A' (label r j) r j) * x (label r j) j) := by
  classical
  unfold matrixChangeMix
  rw [← Finset.sum_subset (Finset.subset_univ (D r))]
  · apply Finset.sum_congr rfl
    intro j hj
    apply Finset.sum_eq_single (label r j)
    · intro i _ hi
      rw [hlocal i r j (Or.inr (Ne.symm hi))]
      ring
    · simp
  · intro j _ hj
    apply Finset.sum_eq_zero
    intro i _
    rw [hlocal i r j (Or.inl hj)]
    ring

/-- Generic matrix-change estimate used for simultaneous primal/dual residuals.
No probability normalization or common right-hand side is required. -/
theorem matrixChangeMix_bound [DecidableEq I] (A : R → C → ℝ)
    (A' : I → R → C → ℝ) (x : I → C → ℝ) (w : I → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hlocal : ∀ i r j, j ∉ D r ∨ label r j ≠ i → A' i r j = A r j) :
    sqNorm (matrixChangeMix A A' x w) ≤
      4 * s * B ^ 2 * H ^ 2 * ∑ i, (incidence D label i : ℝ) * (w i) ^ 2 := by
  have he : matrixChangeMix A A' x w = fun r => ∑ j ∈ D r,
      w (label r j) * ((A r j - A' (label r j) r j) * x (label r j) j) := by
    funext r
    exact matrixChangeMix_local_eq A A' x w D label hlocal r
  rw [he, ← incidence_sum]
  exact localChange_positions_bound A A' x w D label s B H hB hH hA hA' hx hs

omit [Fintype I] in
/-- Sensitive-neighbor specialization. Only witnesses for the selected nonempty
set are required, and only positions labelled by that set are counted. -/
theorem sensitive_residual_bound [DecidableEq I] (S : Finset I) (hS : S.Nonempty)
    (A : R → C → ℝ) (A' : S → R → C → ℝ) (x : S → C → ℝ) (b : R → ℝ)
    (D : R → Finset C) (label : R → C → I) (s : ℕ) (B H : ℝ)
    (hB : 0 ≤ B) (hH : 0 ≤ H)
    (hA : ∀ r j, |A r j| ≤ B) (hA' : ∀ i r j, |A' i r j| ≤ B)
    (hx : ∀ i j, |x i j| ≤ H) (hs : ∀ r, (D r).card ≤ s)
    (hfeas : ∀ i r, ∑ j, A' i r j * x i j = b r)
    (hlocal : ∀ (i : S) r j, j ∉ D r ∨ label r j ≠ i.val → A' i r j = A r j) :
    euclideanNorm (residual A (mix (uniformWeight S) x) b) ≤
      2 * B * H * Real.sqrt ((s : ℝ) *
        (∑ r, ((D r).filter fun j => label r j ∈ S).card : ℕ)) / S.card := by
  classical
  let i0 : S := ⟨hS.choose, hS.choose_spec⟩
  let : Nonempty S := ⟨i0⟩
  let DS : R → Finset C := fun r => (D r).filter fun j => label r j ∈ S
  let labelS : R → C → S := fun r j =>
    if h : label r j ∈ S then ⟨label r j, h⟩ else i0
  have hls : ∀ (i : S) r j, j ∉ DS r ∨ labelS r j ≠ i → A' i r j = A r j := by
    intro i r j hl
    apply hlocal i r j
    by_cases hj : j ∈ D r
    · right
      intro he
      have hm : label r j ∈ S := he ▸ i.property
      have he' : labelS r j = i := by
        apply Subtype.ext
        simp [labelS, he]
      have hj' : j ∈ DS r := Finset.mem_filter.mpr ⟨hj, hm⟩
      rcases hl with hl | hl
      · exact hl hj'
      · exact hl he'
    · exact Or.inl hj
  have hds : ∀ r, (DS r).card ≤ s := fun r =>
    (Finset.card_filter_le _ _).trans (hs r)
  simpa only [totalIncidence, DS, Fintype.card_coe] using
    uniform_residual_bound A A' x b DS labelS s B H hB hH hA hA' hx hds hfeas hls

/-- The explicit norm used in all bounds is Mathlib's Euclidean-space norm. -/
theorem euclideanNorm_eq_norm_toLp (v : R → ℝ) :
    euclideanNorm v = ‖(WithLp.toLp 2 v : EuclideanSpace ℝ R)‖ := by
  simp [euclideanNorm, sqNorm, EuclideanSpace.norm_eq]

end
end QipmFormal.Mixture
