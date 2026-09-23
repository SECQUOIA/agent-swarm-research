import Formal.QuadraticPrecision.RowLowerContact

namespace QuadraticPrecision

/-- A finite family of diameter-bounded classes covering a uniform grid must
have the usual square-root covering size. No interval/facet regularity is used. -/
theorem grid_pattern_count {α : Type*} [Fintype α] (N : ℕ) (hN : 0 < N)
    (hcard : Fintype.card α ≤ N) (color : Fin (N + 1) → α) (ε : ℝ)
    (hdiam : ∀ i j, color i = color j →
      ((i : ℝ) / (N : ℝ) - (j : ℝ) / (N : ℝ)) ^ 2 ≤ 4 * ε) :
    1 ≤ 4 * ε * (N : ℝ) ^ 2 := by
  obtain ⟨i, j, hij, hc⟩ := Fintype.exists_ne_map_eq_of_card_lt color (by
    simp only [Fintype.card_fin]; omega)
  have hNR : (0 : ℝ) < N := by exact_mod_cast hN
  have hsep : 1 ≤ ((i : ℝ) - (j : ℝ)) ^ 2 := by
    rcases lt_or_gt_of_ne (Fin.val_ne_of_ne hij) with h | h
    · have h' : (i:ℝ)+1 ≤ (j:ℝ) := by exact_mod_cast h
      nlinarith [sq_nonneg ((j:ℝ) - (i:ℝ) - 1)]
    · have h' : (j:ℝ)+1 ≤ (i:ℝ) := by exact_mod_cast h
      nlinarith [sq_nonneg ((i:ℝ) - (j:ℝ) - 1)]
  have h := mul_le_mul_of_nonneg_right (hdiam i j hc) (sq_nonneg (N:ℝ))
  have he : ((i : ℝ) / (N : ℝ) - (j : ℝ) / (N : ℝ)) ^ 2 * (N:ℝ) ^ 2 =
      ((i:ℝ)-(j:ℝ)) ^ 2 := by
        field_simp
  rw [he] at h
  nlinarith [hsep.trans h]

/-- Finite affine LPs with attained fiber minima satisfy the exponential row
bound. Equalities have an arbitrary index set and are not counted. The separate
LP-closure theorem supplies the attained minima for finite extended formulations. -/
theorem square_row_bound_of_attainment
    {V κ : Type*} [AddCommGroup V] [Module ℝ V]
    (M : ℕ) (row : Fin M → V →ᵃ[ℝ] ℝ) (eqn : κ → V →ᵃ[ℝ] ℝ)
    (X T : V →ᵃ[ℝ] ℝ) (ε : ℝ)
    (hgraph : ∀ x ∈ Set.Icc (0 : ℝ) 1, ∃ z,
      (∀ i, row i z ≤ 0) ∧ (∀ k, eqn k z = 0) ∧ X z = x ∧ T z = x ^ 2)
    (hlo : ∀ p, (∀ i, row i p ≤ 0) → (∀ k, eqn k p = 0) →
      X p ∈ Set.Icc (0 : ℝ) 1 → (X p) ^ 2 - ε ≤ T p)
    (hatt : ∀ x ∈ Set.Icc (0 : ℝ) 1, ∃ p,
      (∀ i, row i p ≤ 0) ∧ (∀ k, eqn k p = 0) ∧ X p = x ∧
      ∀ v, (∀ i, row i v ≤ 0) → (∀ k, eqn k v = 0) → X v = x → T p ≤ T v) :
    1 ≤ 4 * ε * ((2:ℝ)^M) ^ 2 := by
  classical
  let N := 2 ^ M
  have hN : 0 < N := pow_pos (by decide) _
  have hNR : (0 : ℝ) < N := by exact_mod_cast hN
  let x (i : Fin (N + 1)) : ℝ := (i:ℝ) / (N:ℝ)
  have hx : ∀ i, x i ∈ Set.Icc (0 : ℝ) 1 := by
    intro i
    constructor
    · exact div_nonneg (Nat.cast_nonneg _) hNR.le
    · apply (div_le_one hNR).2
      exact_mod_cast (show i.val ≤ N by omega)
  choose p hp hep hXp hmin using fun i => hatt (x i) (hx i)
  let color (i : Fin (N + 1)) : Finset (Fin M) := Finset.univ.filter fun k => row k (p i) = 0
  have hc : Fintype.card (Finset (Fin M)) ≤ N := by simp [N]
  have h := grid_pattern_count N hN hc color ε ?_
  · simpa [N] using h
  intro i j hij
  have hmid : (x i + x j)/2 ∈ Set.Icc (0 : ℝ) 1 := by
    constructor <;> linarith [(hx i).1, (hx i).2, (hx j).1, (hx j).2]
  obtain ⟨z, hz, hez, hXz, hTz⟩ := hgraph _ hmid
  have hactive : ∀ k, row k (p i) = 0 → row k (p j) = 0 := by
    intro k hk
    have hk' : k ∈ color i := by simp [color, hk]
    rw [hij] at hk'
    simpa [color] using hk'
  have hcontact := square_contact_of_minimum_lifts row eqn X T (p i) (p j) z ε
    (hp i) hz (hep i) (hep j) hez hactive
    (by simpa [hXp] using hXz) (by simpa [hXz] using hTz)
    (by intro v hv hev hXv; exact hmin i v hv hev (hXv.trans (hXp i)))
    (hlo (p i) (hp i) (hep i) (by simpa [hXp] using hx i))
    (hlo (p j) (hp j) (hep j) (by simpa [hXp] using hx j))
  simpa only [hXp] using hcontact

/-- The algebraic row lower bound in the logarithmic form used by the paper. -/
theorem row_log_lower_bound (M : ℕ) {ε : ℝ} (hε : 0 < ε)
    (h : 1 ≤ 4 * ε * ((2 : ℝ) ^ M) ^ 2) :
    (1/2 : ℝ) * Real.logb 2 (1/ε) - 1 ≤ M := by
  have hh := Real.logb_le_logb_of_le (by norm_num : (1 : ℝ) < 2)
    (by norm_num : (0 : ℝ) < 1) h
  have hfour : Real.logb 2 4 = 2 := by
    have hpow := Real.logb_pow 2 2 2
    norm_num [Real.logb_self_eq_one (by norm_num : (1:ℝ) < 2)] at hpow
    exact hpow
  rw [Real.logb_mul (by positivity) (by positivity),
    Real.logb_mul (by norm_num) (ne_of_gt hε), hfour,
    Real.logb_pow, Real.logb_pow, Real.logb_self_eq_one (by norm_num)] at hh
  simp only [Real.logb_one, Nat.cast_ofNat, mul_one] at hh
  simp only [one_div, Real.logb_inv]
  linarith

end QuadraticPrecision
