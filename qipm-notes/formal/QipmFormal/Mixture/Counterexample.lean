import QipmFormal.Mixture.Residual

/-!
# A diagonal LP counterexample to common-parameter centrality

Neighbors are central points of their own diagonal LP. The uniform mixture
has small residual at the base input and large common-parameter defect. Its
width around its own mean product is zero.
-/
namespace QipmFormal.Mixture.Counterexample
noncomputable section
open scoped BigOperators
variable {I : Type*} [Fintype I] [DecidableEq I]

def coeff (μ : ℝ) (i j : I) : ℝ := if j = i then 1 else μ

def primal (μ : ℝ) (i j : I) : ℝ := if j = i then μ else 1

def diagonal (a : I → ℝ) (r j : I) : ℝ := if r = j then a r else 0

def rhs (μ : ℝ) : I → ℝ := fun _ => μ

def dual : I → ℝ := fun _ => -1

def cost : I → ℝ := fun _ => 0

theorem diagonal_mul (a x : I → ℝ) (r : I) :
    (∑ j, diagonal a r j * x j) = a r * x r := by simp [diagonal]

theorem diagonal_transpose_mul (a y : I → ℝ) (j : I) :
    (∑ r, diagonal a r j * y r) = a j * y j := by simp [diagonal]

theorem neighbor_central (μ : ℝ) (hμ : 0 < μ) (i : I) :
    (∀ j, 0 < primal μ i j ∧ 0 < coeff μ i j) ∧
    (∀ r, residual (diagonal (coeff μ i)) (primal μ i) (rhs μ) r = 0) ∧
    (∀ j, (∑ r, diagonal (coeff μ i) r j * dual r) + coeff μ i j = cost j) ∧
    (∀ j, primal μ i j * coeff μ i j = μ) := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro j; simp only [primal, coeff]; split_ifs <;> constructor <;> positivity
  · intro r
    rw [residual, diagonal_mul]
    simp only [coeff, primal, rhs]; split_ifs <;> ring
  · intro j
    rw [diagonal_transpose_mul]
    simp [dual, cost]
  · intro j; simp only [primal, coeff]; split_ifs <;> ring

omit [Fintype I] in
theorem neighbor_primal_formula (μ : ℝ) (hμ : 0 < μ) (i j : I) :
    primal μ i j = μ / coeff μ i j := by
  simp only [primal, coeff]; split_ifs <;> simp [ne_of_gt hμ]

omit [Fintype I] in
theorem neighbor_bounds (μ : ℝ) (_hμ : 0 < μ) (hμ1 : μ ≤ 1) (i j : I) :
    μ ≤ primal μ i j ∧ primal μ i j ≤ 1 ∧
    μ ≤ coeff μ i j ∧ coeff μ i j ≤ 1 ∧ |dual (I := I) j| = 1 := by
  simp only [primal, coeff, dual, abs_neg, abs_one]
  split_ifs <;> exact ⟨by linarith, by linarith, by linarith, by linarith, trivial⟩

def meanX (n μ : ℝ) : ℝ := (n - 1 + μ) / n

def meanS (n μ : ℝ) : ℝ := (1 + (n - 1) * μ) / n

theorem uniform_primal (μ : ℝ) (j : I) :
    mix (uniformWeight I) (primal μ) j = meanX (Fintype.card I) μ := by
  have hx : primal μ = fun i j : I => 1 + if i = j then μ - 1 else 0 := by
    funext i j; simp only [primal]; by_cases h : i = j <;> simp [h, eq_comm]
  rw [hx]
  simp [mix, uniformWeight, mul_add, Finset.sum_add_distrib, meanX, div_eq_mul_inv]
  ring

theorem uniform_slack (μ : ℝ) (j : I) :
    mix (uniformWeight I) (coeff μ) j = meanS (Fintype.card I) μ := by
  have hs : coeff μ = fun i j : I => μ + if i = j then 1 - μ else 0 := by
    funext i j; simp only [coeff]; by_cases h : i = j <;> simp [h, eq_comm]
  rw [hs]
  simp [mix, uniformWeight, mul_add, Finset.sum_add_distrib, meanS, div_eq_mul_inv]
  ring

omit [DecidableEq I] in
theorem uniform_dual [Nonempty I] :
    mix (uniformWeight I) (fun _ : I => dual (I := I)) = dual := by
  funext j
  simp [mix, uniformWeight, dual, ne_of_gt (Nat.cast_pos.mpr (Fintype.card_pos))]

theorem product_formula (n μ : ℝ) :
    meanX n μ * meanS n μ = (n - 1 + μ) * (1 + (n - 1) * μ) / n ^ 2 := by
  simp only [meanX, meanS]; ring

theorem product_defect (n μ : ℝ) (hn : n ≠ 0) :
    meanX n μ * meanS n μ - μ = (n - 1) * (1 - μ) ^ 2 / n ^ 2 := by
  rw [product_formula]; field_simp; ring

theorem base_primal_residual (μ : ℝ) (j : I) :
    residual (diagonal (fun _ : I => μ))
      (mix (uniformWeight I) (primal μ)) (rhs μ) j =
        μ * (meanX (Fintype.card I) μ - 1) := by
  rw [residual, diagonal_mul, uniform_primal]
  simp [rhs]; ring

theorem base_stationarity_residual [Nonempty I] (μ : ℝ) (j : I) :
    (∑ r, diagonal (fun _ : I => μ) r j *
      mix (uniformWeight I) (fun _ : I => dual (I := I)) r) +
        mix (uniformWeight I) (coeff μ) j - cost j =
          meanS (Fintype.card I) μ - μ := by
  rw [diagonal_transpose_mul, uniform_dual, uniform_slack]
  simp [dual, cost]; ring

theorem scalar_residuals (n μ : ℝ) (hn : n ≠ 0) :
    μ * (meanX n μ - 1) = -μ * (1 - μ) / n ∧
    meanS n μ - μ = (1 - μ) / n := by
  constructor <;> dsimp [meanX, meanS] <;> field_simp <;> ring

/-- Squared stacked primal and stationarity residual. -/
def residualSquared (n μ : ℝ) : ℝ := (1 + μ ^ 2) * (1 - μ) ^ 2 / n

omit [DecidableEq I] in
theorem residualSquared_exact (μ : ℝ) (hn : (Fintype.card I : ℝ) ≠ 0) :
    sqNorm (fun _ : I => μ * (meanX (Fintype.card I) μ - 1)) +
    sqNorm (fun _ : I => meanS (Fintype.card I) μ - μ) =
      residualSquared (Fintype.card I) μ := by
  rw [(scalar_residuals _ _ hn).1, (scalar_residuals _ _ hn).2]
  simp only [sqNorm, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  dsimp [residualSquared]
  field_simp
  ring

theorem point_centered_width_zero (μ : ℝ) (j : I) :
    |mix (uniformWeight I) (primal μ) j * mix (uniformWeight I) (coeff μ) j -
      meanX (Fintype.card I) μ * meanS (Fintype.card I) μ| = 0 := by
  rw [uniform_primal, uniform_slack, sub_self, abs_zero]


theorem algebraic_gap [Nonempty I] (μ : ℝ) :
    dot cost (mix (uniformWeight I) (primal μ)) -
      dot (rhs μ) (mix (uniformWeight I) (fun _ : I => dual (I := I))) =
        (Fintype.card I : ℝ) * μ := by
  rw [uniform_dual]
  simp [dot, cost, rhs, dual]

theorem inner_product (μ : ℝ) :
    dot (mix (uniformWeight I) (primal μ)) (mix (uniformWeight I) (coeff μ)) =
      (Fintype.card I : ℝ) * (meanX (Fintype.card I) μ * meanS (Fintype.card I) μ) := by
  simp [dot, uniform_primal, uniform_slack]

theorem residualSquared_bound (n μ : ℝ) (hn : 0 < n) (hμ : 0 ≤ μ)
    (hμ1 : μ ≤ 1) : residualSquared n μ ≤ 2 / n := by
  apply (div_le_div_iff_of_pos_right hn).2
  have ha : μ ^ 2 ≤ 1 := by nlinarith
  have hb : (1 - μ) ^ 2 ≤ 1 := by nlinarith
  calc
    (1 + μ ^ 2) * (1 - μ) ^ 2 ≤ (1 + μ ^ 2) * 1 :=
      mul_le_mul_of_nonneg_left hb (by positivity)
    _ ≤ 2 := by nlinarith

/-- The choice μ = n⁻² gives a defect growing at least linearly with n. -/
theorem inverse_square_defect (n : ℝ) (hn : 2 ≤ n) :
    n / 8 ≤ meanX n (1 / n ^ 2) * meanS n (1 / n ^ 2) / (1 / n ^ 2) - 1 := by
  have hn0 : 0 < n := by linarith
  have hnne : n ≠ 0 := ne_of_gt hn0
  have hn2 : 4 ≤ n ^ 2 := by nlinarith
  have hμ : 0 < 1 / n ^ 2 := by positivity
  have hμ1 : 1 / n ^ 2 ≤ 1 / 2 := by
    apply (div_le_iff₀ (by positivity : 0 < n ^ 2)).2
    nlinarith
  have heq : meanX n (1 / n ^ 2) * meanS n (1 / n ^ 2) / (1 / n ^ 2) - 1 =
      (n - 1) * (1 - 1 / n ^ 2) ^ 2 := by
    dsimp [meanX, meanS]
    field_simp
    ring
  rw [heq]
  have ha : 1 / 4 ≤ (1 - 1 / n ^ 2) ^ 2 := by nlinarith
  calc
    n / 8 ≤ (n - 1) * (1 / 4) := by linarith
    _ ≤ (n - 1) * (1 - 1 / n ^ 2) ^ 2 :=
      mul_le_mul_of_nonneg_left ha (by linarith)

/-- A finite quantitative replacement for the asymptotic residual statement. -/
theorem inverse_square_residual (n : ℝ) (hn : 2 ≤ n) :
    residualSquared n (1 / n ^ 2) ≤ 2 / n := by
  apply residualSquared_bound _ _ (by linarith) (by positivity)
  apply (div_le_iff₀ (by positivity : 0 < n ^ 2)).2
  nlinarith

/-- Appending equally many unchanged coordinates gives these two product levels.
Their width around the mean product is at least 1/3 once q ≥ 2μ. -/
theorem two_level_width (q μ : ℝ) (hμ : 0 < μ) (hq : 2 * μ ≤ q) :
    |q - (q + μ) / 2| / ((q + μ) / 2) = (q - μ) / (q + μ) ∧
    1 / 3 ≤ (q - μ) / (q + μ) := by
  have hp : 0 < q + μ := by linarith
  constructor
  · rw [abs_of_nonneg (by linarith)]
    field_simp
    ring
  · apply (le_div_iff₀ hp).2
    linarith


/-- The second copy of the coordinates is public and unchanged in every neighbor. -/
def paddedCoeff (μ : ℝ) (i : I) : I ⊕ I → ℝ :=
  Sum.elim (coeff μ i) (fun _ => μ)

def paddedPrimal (μ : ℝ) (i : I) : I ⊕ I → ℝ :=
  Sum.elim (primal μ i) (fun _ => 1)

theorem padded_central (μ : ℝ) (hμ : 0 < μ) (i : I) :
    (∀ j, 0 < paddedPrimal μ i j ∧ 0 < paddedCoeff μ i j) ∧
    (∀ r, residual (diagonal (paddedCoeff μ i)) (paddedPrimal μ i) (rhs μ) r = 0) ∧
    (∀ j, (∑ r, diagonal (paddedCoeff μ i) r j * dual r) +
      paddedCoeff μ i j = cost j) ∧
    (∀ j, paddedPrimal μ i j * paddedCoeff μ i j = μ) := by
  have hc := neighbor_central μ hμ i
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro j; cases j with
    | inl j => exact hc.1 j
    | inr j => exact ⟨by norm_num [paddedPrimal], hμ⟩
  · intro r
    rw [residual, diagonal_mul]
    cases r with
    | inl j => simpa [residual, diagonal_mul, paddedCoeff, paddedPrimal, rhs] using hc.2.1 j
    | inr j => simp [paddedCoeff, paddedPrimal, rhs]
  · intro j
    rw [diagonal_transpose_mul]
    simp [dual, cost]
  · intro j; cases j with
    | inl j => exact hc.2.2.2 j
    | inr j => simp [paddedPrimal, paddedCoeff]

theorem padded_mean_primal [Nonempty I] (μ : ℝ) (j : I ⊕ I) :
    mix (uniformWeight I) (paddedPrimal μ) j =
      Sum.elim (fun _ => meanX (Fintype.card I) μ) (fun _ => 1) j := by
  cases j with
  | inl j => exact uniform_primal μ j
  | inr j =>
    simp [mix, paddedPrimal, uniformWeight,
      ne_of_gt (Nat.cast_pos.mpr (Fintype.card_pos))]

theorem padded_mean_slack [Nonempty I] (μ : ℝ) (j : I ⊕ I) :
    mix (uniformWeight I) (paddedCoeff μ) j =
      Sum.elim (fun _ => meanS (Fintype.card I) μ) (fun _ => μ) j := by
  cases j with
  | inl j => exact uniform_slack μ j
  | inr j =>
    simp [mix, paddedCoeff, uniformWeight,
      ne_of_gt (Nat.cast_pos.mpr (Fintype.card_pos))]

theorem padded_mean_product [Nonempty I] (μ : ℝ) :
    dot (mix (uniformWeight I) (paddedPrimal μ))
      (mix (uniformWeight I) (paddedCoeff μ)) / (Fintype.card (I ⊕ I) : ℝ) =
        (meanX (Fintype.card I) μ * meanS (Fintype.card I) μ + μ) / 2 := by
  simp only [dot, padded_mean_primal, padded_mean_slack, Fintype.sum_sum_type,
    Sum.elim_inl, Sum.elim_inr, one_mul, Finset.sum_const, Finset.card_univ,
    nsmul_eq_mul, Fintype.card_sum, Nat.cast_add]
  have hn : (Fintype.card I : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos)
  field_simp
  ring

/-- Each half of the padded model has exactly this normalized width. -/
theorem padded_coordinate_width [Nonempty I] (μ : ℝ) (hμ : 0 < μ)
    (hq : 2 * μ ≤ meanX (Fintype.card I) μ * meanS (Fintype.card I) μ)
    (j : I ⊕ I) :
    let q := meanX (Fintype.card I) μ * meanS (Fintype.card I) μ
    |mix (uniformWeight I) (paddedPrimal μ) j *
      mix (uniformWeight I) (paddedCoeff μ) j - (q + μ) / 2| / ((q + μ) / 2) =
      (q - μ) / (q + μ) := by
  dsimp only
  rw [padded_mean_primal, padded_mean_slack]
  cases j with
  | inl j => exact (two_level_width _ _ hμ hq).1
  | inr j =>
    simp only [Sum.elim_inr, one_mul]
    rw [abs_of_nonpos (by linarith)]
    field_simp
    ring

/-- At n ≥ 8, inverse-square μ makes the padded point-centered width ≥ 1/3. -/
theorem inverse_square_product_large (n : ℝ) (hn : 8 ≤ n) :
    2 * (1 / n ^ 2) ≤ meanX n (1 / n ^ 2) * meanS n (1 / n ^ 2) := by
  have hμ : 0 < 1 / n ^ 2 := by positivity
  have h := inverse_square_defect n (by linarith)
  have hdiv : 2 ≤ meanX n (1 / n ^ 2) * meanS n (1 / n ^ 2) / (1 / n ^ 2) := by
    linarith
  exact (le_div_iff₀ hμ).1 hdiv


theorem uniform_mean_product [Nonempty I] (μ : ℝ) :
    dot (mix (uniformWeight I) (primal μ)) (mix (uniformWeight I) (coeff μ)) /
        (Fintype.card I : ℝ) = meanX (Fintype.card I) μ * meanS (Fintype.card I) μ := by
  rw [inner_product]
  field_simp

omit [Fintype I] in
theorem padded_bounds (μ : ℝ) (hμ : 0 < μ) (hμ1 : μ ≤ 1)
    (i : I) (j : I ⊕ I) :
    μ ≤ paddedPrimal μ i j ∧ paddedPrimal μ i j ≤ 1 ∧
    μ ≤ paddedCoeff μ i j ∧ paddedCoeff μ i j ≤ 1 ∧ |dual (I := I ⊕ I) j| = 1 := by
  cases j with
  | inl j => exact neighbor_bounds μ hμ hμ1 i j
  | inr j => simp [paddedPrimal, paddedCoeff, dual, hμ1]

omit [DecidableEq I] in
theorem padded_uniform_dual [Nonempty I] :
    mix (uniformWeight I) (fun _ : I => dual (I := I ⊕ I)) = dual := by
  funext j
  simp [mix, uniformWeight, dual, ne_of_gt (Nat.cast_pos.mpr (Fintype.card_pos))]

/-- Public padding leaves the squared stacked residual exactly unchanged. -/
theorem padded_residualSquared_exact [Nonempty I] (μ : ℝ) :
    sqNorm (residual (diagonal (fun _ : I ⊕ I => μ))
      (mix (uniformWeight I) (paddedPrimal μ)) (rhs μ)) +
    sqNorm (fun j : I ⊕ I =>
      (∑ r, diagonal (fun _ : I ⊕ I => μ) r j *
        mix (uniformWeight I) (fun _ : I => dual (I := I ⊕ I)) r) +
          mix (uniformWeight I) (paddedCoeff μ) j - cost j) =
      residualSquared (Fintype.card I) μ := by
  rw [padded_uniform_dual]
  simp only [sqNorm, residual, diagonal_mul, diagonal_transpose_mul,
    padded_mean_primal, padded_mean_slack, rhs, dual, cost,
    Fintype.sum_sum_type, Sum.elim_inl, Sum.elim_inr]
  simp only [mul_one, sub_self, zero_pow (by omega : 2 ≠ 0), Finset.sum_const_zero,
    add_zero, mul_neg_one, neg_add_cancel, sub_zero]
  have heq : μ * meanX (Fintype.card I) μ - μ =
      μ * (meanX (Fintype.card I) μ - 1) := by ring
  rw [heq]
  simpa only [sqNorm, sub_eq_add_neg, add_comm] using
    residualSquared_exact (I := I) μ (ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos))

theorem actual_residualSquared_exact [Nonempty I] (μ : ℝ) :
    sqNorm (residual (diagonal (fun _ : I => μ))
      (mix (uniformWeight I) (primal μ)) (rhs μ)) +
    sqNorm (fun j : I =>
      (∑ r, diagonal (fun _ : I => μ) r j *
        mix (uniformWeight I) (fun _ : I => dual (I := I)) r) +
          mix (uniformWeight I) (coeff μ) j - cost j) =
      residualSquared (Fintype.card I) μ := by
  simp_rw [sqNorm, base_primal_residual, base_stationarity_residual]
  exact residualSquared_exact μ (ne_of_gt (Nat.cast_pos.mpr Fintype.card_pos))


/-- Uniform constants make the paper's Θ(1/n) product claim explicit. -/
theorem small_parameter_product_bounds (n μ : ℝ) (hn : 2 ≤ n)
    (hμ : 0 ≤ μ) (hμn : μ ≤ 1 / n) :
    1 / (2 * n) ≤ meanX n μ * meanS n μ ∧
    meanX n μ * meanS n μ ≤ 2 / n := by
  have hn0 : 0 < n := by linarith
  have hm : μ * n ≤ 1 := (le_div_iff₀ hn0).1 hμn
  have hμ1 : μ ≤ 1 := by nlinarith
  have hx0 : 1 / 2 ≤ meanX n μ := by
    apply (le_div_iff₀ hn0).2
    linarith
  have hx1 : meanX n μ ≤ 1 := by
    apply (div_le_iff₀ hn0).2
    linarith
  have hs0 : 1 / n ≤ meanS n μ := by
    apply (div_le_div_iff_of_pos_right hn0).2
    nlinarith
  have hs1 : meanS n μ ≤ 2 / n := by
    apply (div_le_div_iff_of_pos_right hn0).2
    nlinarith
  constructor
  · calc
      1 / (2 * n) = (1 / 2) * (1 / n) := by ring
      _ ≤ meanX n μ * meanS n μ :=
        mul_le_mul hx0 hs0 (by positivity) (by linarith)
  · calc
      meanX n μ * meanS n μ ≤ 1 * (2 / n) :=
        mul_le_mul hx1 hs1 (by linarith [div_pos (by norm_num : (0 : ℝ) < 1) hn0])
          (by norm_num)
      _ = 2 / n := by ring

/-- The complete padded counterexample, stated using its actual residuals and
its actual mean complementarity rather than the auxiliary scalar formulas. -/
theorem padded_quantitative_failure [Nonempty I]
    (hn : 8 ≤ (Fintype.card I : ℝ)) :
    let μ : ℝ := 1 / (Fintype.card I : ℝ) ^ 2
    let x := mix (uniformWeight I) (paddedPrimal μ)
    let y := mix (uniformWeight I) (fun _ : I => dual (I := I ⊕ I))
    let s := mix (uniformWeight I) (paddedCoeff μ)
    let μw := dot x s / (Fintype.card (I ⊕ I) : ℝ)
    sqNorm (residual (diagonal (fun _ : I ⊕ I => μ)) x (rhs μ)) +
      sqNorm (fun j : I ⊕ I =>
        (∑ r, diagonal (fun _ : I ⊕ I => μ) r j * y r) + s j - cost j) ≤
          2 / (Fintype.card I : ℝ) ∧
    ∀ j, 1 / 3 ≤ |x j * s j - μw| / μw := by
  dsimp only
  constructor
  · rw [padded_residualSquared_exact]
    exact inverse_square_residual _ (by linarith)
  · intro j
    rw [padded_mean_product]
    have hμ : 0 < 1 / (Fintype.card I : ℝ) ^ 2 := by positivity
    have hq := inverse_square_product_large (Fintype.card I) hn
    rw [padded_coordinate_width _ hμ hq j]
    exact (two_level_width _ _ hμ hq).2


/-! Structural parameters of the examples: B = 1, one coefficient per row
and column, and exactly one input-dependent position per input bit. -/

omit [Fintype I] in
theorem diagonal_coefficient_bound (a : I → ℝ) (ha : ∀ j, |a j| ≤ 1) (r j : I) :
    |diagonal a r j| ≤ 1 := by
  by_cases h : r = j
  · simp [diagonal, h, ha j]
  · simp [diagonal, h]

theorem diagonal_row_support (a : I → ℝ) (r : I) :
    (Finset.univ.filter fun j => diagonal a r j ≠ 0).card ≤ 1 := by
  calc
    _ ≤ ({r} : Finset I).card := Finset.card_le_card (by
      intro j hj
      have h : r = j := by
        by_contra h
        simp [diagonal, h] at hj
      simp [h])
    _ = 1 := Finset.card_singleton r

theorem diagonal_column_support (a : I → ℝ) (j : I) :
    (Finset.univ.filter fun r => diagonal a r j ≠ 0).card ≤ 1 := by
  calc
    _ ≤ ({j} : Finset I).card := Finset.card_le_card (by
      intro r hr
      have h : r = j := by
        by_contra h
        simp [diagonal, h] at hr
      simp [h])
    _ = 1 := Finset.card_singleton j

omit [Fintype I] in
theorem example_matrix_bounds (μ : ℝ) (hμ : 0 ≤ μ) (hμ1 : μ ≤ 1) :
    (∀ r j : I, |diagonal (fun _ => μ) r j| ≤ 1) ∧
    (∀ i r j : I, |diagonal (coeff μ i) r j| ≤ 1) ∧
    (∀ r j : I ⊕ I, |diagonal (fun _ => μ) r j| ≤ 1) ∧
    (∀ (i : I) (r j : I ⊕ I), |diagonal (paddedCoeff μ i) r j| ≤ 1) := by
  have ha (i j : I) : |coeff μ i j| ≤ 1 := by
    simp only [coeff]
    split_ifs <;> simp [abs_of_nonneg hμ, hμ1]
  refine ⟨?_, ?_, ?_, ?_⟩
  · exact diagonal_coefficient_bound _ (fun _ => by simpa [abs_of_nonneg hμ])
  · intro i; exact diagonal_coefficient_bound _ (ha i)
  · exact diagonal_coefficient_bound _ (fun _ => by simpa [abs_of_nonneg hμ])
  · intro i
    apply diagonal_coefficient_bound
    intro j; cases j with
    | inl j => exact ha i j
    | inr j => simpa [paddedCoeff, abs_of_nonneg hμ]

def dependent (r : I) : Finset I := {r}

def bitLabel (r _j : I) : I := r

def paddedDependent : I ⊕ I → Finset (I ⊕ I) :=
  Sum.elim (fun r => {Sum.inl r}) (fun _ => ∅)

def paddedBitLabel (r _j : I ⊕ I) : I := Sum.elim id id r

omit [Fintype I] in
theorem example_locality (μ : ℝ) (i r j : I)
    (h : j ∉ dependent r ∨ bitLabel r j ≠ i) :
    diagonal (coeff μ i) r j = diagonal (fun _ => μ) r j := by
  by_cases hrj : r = j
  · subst j
    have hi : r ≠ i := by simpa [dependent, bitLabel] using h
    simp [diagonal, coeff, hi]
  · simp [diagonal, hrj]

omit [Fintype I] in
theorem padded_example_locality (μ : ℝ) (i : I) (r j : I ⊕ I)
    (h : j ∉ paddedDependent r ∨ paddedBitLabel r j ≠ i) :
    diagonal (paddedCoeff μ i) r j = diagonal (fun _ => μ) r j := by
  by_cases hrj : r = j
  · subst j
    cases r with
    | inl r =>
      have hi : r ≠ i := by simpa [paddedDependent, paddedBitLabel] using h
      simp [diagonal, paddedCoeff, coeff, hi]
    | inr r => simp [diagonal, paddedCoeff]
  · simp [diagonal, hrj]

omit [Fintype I] [DecidableEq I] in
theorem dependent_row_bound (r : I) : (dependent r).card ≤ 1 := by simp [dependent]

omit [Fintype I] [DecidableEq I] in
theorem padded_dependent_row_bound (r : I ⊕ I) : (paddedDependent r).card ≤ 1 := by
  cases r <;> simp [paddedDependent]

theorem dependent_column_bound (j : I) :
    (Finset.univ.filter fun r => j ∈ dependent r).card ≤ 1 := by
  apply le_trans (Finset.card_le_card (show
    (Finset.univ.filter fun r => j ∈ dependent r) ⊆ {j} from ?_)) (by simp)
  intro r hr
  have hr' := (Finset.mem_filter.mp hr).2
  simpa [dependent, eq_comm] using hr'

theorem padded_dependent_column_bound (j : I ⊕ I) :
    (Finset.univ.filter fun r => j ∈ paddedDependent r).card ≤ 1 := by
  apply le_trans (Finset.card_le_card (show
    (Finset.univ.filter fun r => j ∈ paddedDependent r) ⊆ {j} from ?_)) (by simp)
  intro r hr
  have hr' := (Finset.mem_filter.mp hr).2
  cases r <;> cases j <;> simp_all [paddedDependent, Finset.mem_singleton]

theorem example_incidence (i : I) : incidence dependent bitLabel i = 1 := by
  have hh (r : I) : ((dependent r).filter fun j => bitLabel r j = i).card =
      if r = i then 1 else 0 := by
    by_cases h : r = i <;> simp [dependent, bitLabel, h]
  simp only [incidence, hh]
  simp

omit [DecidableEq I] in
theorem example_totalIncidence : totalIncidence (dependent (I := I)) = Fintype.card I := by
  simp [totalIncidence, dependent]

theorem padded_example_incidence (i : I) : incidence paddedDependent paddedBitLabel i = 1 := by
  have hh (r : I ⊕ I) :
      ((paddedDependent r).filter fun j => paddedBitLabel r j = i).card =
        if r = Sum.inl i then 1 else 0 := by
    cases r with
    | inl r => by_cases h : r = i <;> simp [paddedDependent, paddedBitLabel, h]
    | inr r => simp [paddedDependent]
  simp only [incidence, hh]
  simp

omit [DecidableEq I] in
theorem padded_example_totalIncidence :
    totalIncidence (paddedDependent (I := I)) = Fintype.card I := by
  simp [totalIncidence, Fintype.sum_sum_type, paddedDependent]

end
end QipmFormal.Mixture.Counterexample
