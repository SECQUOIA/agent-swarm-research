import Mathlib

/-!
# Continuous switching: endpoint control and the three-block lower witness

Cumulative schedules are parameterized by three letters and two ordered real
switch times. Zero-length blocks and repeated letters are permitted. Thus the
lower bound includes every schedule with at most two switches.
-/
namespace SwitchingControl.Continuous

/-- Occupation of mode `i` in the three blocks cut at `u` and `v`. On `[0,T]`,
with `0 ≤ u ≤ v ≤ T`, this is the integrated indicator of the block word. -/
def occupation (p q r i : Fin 3) (u v t : ℝ) : ℝ :=
  (if p = i then min t u else 0) +
  (if q = i then min t v - min t u else 0) +
  (if r = i then t - min t v else 0)

/-- Before the first switch only the first letter has accumulated activity. -/
theorem occupation_first (p q r i : Fin 3) (u v t : ℝ)
    (htu : t ≤ u) (huv : u ≤ v) :
    occupation p q r i u v t = if p = i then t else 0 := by
  simp [occupation, min_eq_left htu, min_eq_left (htu.trans huv)]

/-- Between switches the first block is complete and the second is active. -/
theorem occupation_second (p q r i : Fin 3) (u v t : ℝ)
    (hut : u ≤ t) (htv : t ≤ v) :
    occupation p q r i u v t =
      (if p = i then u else 0) + (if q = i then t - u else 0) := by
  simp [occupation, min_eq_right hut, min_eq_left htv]

/-- After the second switch the third letter receives all new activity. -/
theorem occupation_third (p q r i : Fin 3) (u v t : ℝ)
    (huv : u ≤ v) (hvt : v ≤ t) :
    occupation p q r i u v t =
      (if p = i then u else 0) + (if q = i then v - u else 0) +
        (if r = i then t - v else 0) := by
  simp [occupation, min_eq_right (huv.trans hvt), min_eq_right hvt]

/-- Cumulative allocation of the five pure unit phases `01201`, on `[0,5]`. -/
def witness (i : Fin 3) (t : ℝ) : ℝ :=
  if i = 0 then min t 1 + min t 4 - min t 3
  else if i = 1 then min t 2 - min t 1 + t - min t 4
  else min t 3 - min t 2

/-- A coordinate's cumulative increments lie between zero and elapsed time. -/
def UnitIncrements (A : ℝ → ℝ) (T : ℝ) : Prop :=
  ∀ s t, 0 ≤ s → s ≤ t → t ≤ T → 0 ≤ A t - A s ∧ A t - A s ≤ t - s

/-- Endpoint errors control an entire interval when the rounded coordinate
has slope zero or one and the relaxed coordinate has unit-bounded increments. -/
theorem endpoint_bound (A : ℝ → ℝ) (T a b t c E : ℝ) (active : Bool)
    (hA : UnitIncrements A T) (ha : 0 ≤ a) (hat : a ≤ t) (htb : t ≤ b)
    (hb : b ≤ T)
    (hleft : |A a - c| ≤ E)
    (hright : |A b - (c + if active then b - a else 0)| ≤ E) :
    |A t - (c + if active then t - a else 0)| ≤ E := by
  have h1 := hA a t ha hat (htb.trans hb)
  have h2 := hA t b (ha.trans hat) htb hb
  rw [abs_le] at hleft hright ⊢
  cases active <;> simp_all <;> constructor <;> linarith

private theorem all_modes_of_error_lt_one (p q r : Fin 3) (u v : ℝ)
    (h : ∀ i : Fin 3, |witness i 5 - occupation p q r i u v 5| < 1) :
    ∀ i : Fin 3, p = i ∨ q = i ∨ r = i := by
  intro i
  by_contra hi
  push Not at hi
  have hh := h i
  simp only [occupation, hi.1, hi.2.1, hi.2.2, ↓reduceIte, add_zero] at hh
  fin_cases i <;> norm_num [witness] at hh

private theorem distinct_of_all_modes (p q r : Fin 3)
    (h : ∀ i : Fin 3, p = i ∨ q = i ∨ r = i) : p ≠ r ∧ q ≠ r := by
  revert p q r
  decide


/-- Every schedule with at most two switches has error at least one against
`01201`. The quantified time is in the actual continuous horizon `[0,5]`. -/
theorem three_block_lower_bound (p q r : Fin 3) (u v : ℝ)
    (hu : 0 ≤ u) (huv : u ≤ v) (hv : v ≤ 5) :
    ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) 5,
      1 ≤ |witness i t - occupation p q r i u v t| := by
  by_contra h
  push Not at h
  have hterm : ∀ i : Fin 3, |witness i 5 - occupation p q r i u v 5| < 1 :=
    fun i => h i 5 (by norm_num)
  obtain ⟨hpr, hqr⟩ := distinct_of_all_modes p q r
    (all_modes_of_error_lt_one p q r u v hterm)
  have ht := hterm r
  simp only [occupation, hpr, hqr, ↓reduceIte, zero_add,
    min_eq_right hv] at ht
  have hv0 : 0 ≤ v := hu.trans huv
  fin_cases r <;> simp only [Fin.mk_zero', Fin.mk_one, Fin.reduceFinMk] at hpr hqr
  · have hd := h 0 1 (by norm_num)
    norm_num [witness, occupation, hpr, hqr] at ht hd
    rcases le_total v 1 with hh | hh
    · rw [min_eq_right hh] at hd
      rw [abs_lt] at ht hd
      linarith
    · rw [min_eq_left hh] at hd
      norm_num at hd
  · have hd := h 1 2 (by norm_num)
    norm_num [witness, occupation, hpr, hqr] at ht hd
    rcases le_total v 2 with hh | hh
    · rw [min_eq_right hh] at hd
      rw [abs_lt] at ht hd
      linarith
    · rw [min_eq_left hh] at hd
      norm_num at hd
  · have hd := h 2 3 (by norm_num)
    norm_num [witness, occupation, hpr, hqr] at ht hd
    rcases le_total v 3 with hh | hh
    · rw [min_eq_right hh] at hd
      rw [abs_lt] at ht hd
      linarith
    · rw [min_eq_left hh] at hd
      norm_num at hd

/-- The witness starts with zero mass in every mode. -/
theorem witness_zero (i : Fin 3) : witness i 0 = 0 := by
  fin_cases i <;> norm_num [witness]

/-- The witness allocates exactly one unit of activity per unit of time. -/
theorem witness_sum (t : ℝ) : ∑ i : Fin 3, witness i t = t := by
  simp [Fin.sum_univ_succ, witness]
  ring

/-- The displayed witness belongs to the cumulative relaxed-control class. -/
theorem witness_unit_increments (i : Fin 3) : UnitIncrements (witness i) 5 := by
  intro s t hs hst ht
  fin_cases i <;> norm_num [witness, min_def]
  all_goals split_ifs <;> constructor <;> linarith

/-- Switching from mode zero to one at time two and to two at time four
attains error at most one against the continuous witness. -/
theorem witness_attaining_schedule (i : Fin 3) (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 5) :
    |witness i t - occupation 0 1 2 i 2 4 t| ≤ 1 := by
  fin_cases i <;> norm_num [witness, occupation, min_def]
  all_goals rw [abs_le]
  all_goals split_ifs <;> constructor <;> linarith [ht.1, ht.2]

/-- This particular relaxed input has continuous two-switch optimum exactly
one, expressed without relying on existence of a supremum or minimum. -/
theorem witness_optimal_error :
    (∀ p q r : Fin 3, ∀ u v : ℝ, 0 ≤ u → u ≤ v → v ≤ 5 →
      ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) 5,
        1 ≤ |witness i t - occupation p q r i u v t|) ∧
    (∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) 5,
      |witness i t - occupation 0 1 2 i 2 4 t| ≤ 1) :=
  ⟨three_block_lower_bound, witness_attaining_schedule⟩

/-- Time dilation multiplies the integrated occupation by the same factor. -/
theorem occupation_scale (p q r i : Fin 3) (u v t d : ℝ) (hd : 0 ≤ d) :
    occupation p q r i (d * u) (d * v) (d * t) =
      d * occupation p q r i u v t := by
  simp only [occupation, ← mul_min_of_nonneg _ _ hd]
  split_ifs <;> ring

/-- The same witness obstruction holds on every positive rescaling of the
five-unit horizon, with lower error equal to the scale factor. -/
theorem scaled_three_block_lower_bound (d : ℝ) (hd : 0 < d)
    (p q r : Fin 3) (u v : ℝ)
    (hu : 0 ≤ u) (huv : u ≤ v) (hv : v ≤ 5 * d) :
    ∃ i : Fin 3, ∃ t ∈ Set.Icc (0 : ℝ) (5 * d),
      d ≤ |d * witness i (t / d) - occupation p q r i u v t| := by
  obtain ⟨i, t, ht, herr⟩ := three_block_lower_bound p q r (u / d) (v / d)
    (div_nonneg hu hd.le) ((div_le_div_iff_of_pos_right hd).mpr huv)
    ((div_le_iff₀ hd).mpr hv)
  refine ⟨i, d * t, ⟨mul_nonneg hd.le ht.1, ?_⟩, ?_⟩
  · nlinarith [ht.2]
  · have hoc := occupation_scale p q r i (u / d) (v / d) t d hd.le
    simp only [mul_div_cancel₀ _ hd.ne'] at hoc
    rw [hoc]
    have htime : d * t / d = t := by field_simp
    rw [htime, ← mul_sub, abs_mul, abs_of_pos hd]
    nlinarith

end SwitchingControl.Continuous
