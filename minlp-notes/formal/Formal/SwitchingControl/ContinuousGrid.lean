import Formal.SwitchingControl.Profile
import Formal.SwitchingControl.Finite
import Formal.SwitchingControl.Continuous
import Formal.SwitchingControl.Measurable

/-! From cumulative relaxed controls and grid certificates to continuous schedules. -/
namespace SwitchingControl.ContinuousGrid

open SwitchingControl.Continuous

/-- The cumulative-control class used in the manuscript. -/
structure ValidCumulative (A : Fin 3 → ℝ → ℝ) (T : ℝ) : Prop where
  initial : ∀ i, A i 0 = 0
  increments : ∀ i, UnitIncrements (A i) T
  conservation : ∀ t ∈ Set.Icc (0 : ℝ) T, ∑ i, A i t = t

noncomputable def sample {n : ℕ} (A : Fin 3 → ℝ → ℝ) : Profile n :=
  fun j i => A i (j.val + 1)

theorem sample_valid {n : ℕ} {A : Fin 3 → ℝ → ℝ}
    (hA : ValidCumulative A n) : ValidProfile (sample A : Profile n) := by
  have hb (j : Fin n) : (j.val : ℝ) + 1 ≤ n := by exact_mod_cast j.isLt
  constructor
  · intro j i
    have h := (hA.increments i) 0 (j.val + 1) (by rfl) (by positivity) (hb j)
    simpa [sample, hA.initial] using h.1
  · intro j i hj
    have h := (hA.increments i) 0 (j.val + 1) (by rfl) (by positivity) (hb j)
    simpa [sample, hA.initial, hj] using h.2
  · intro j k i hjk
    have hh : (j.val : ℝ) + 1 ≤ k.val + 1 := by exact_mod_cast Nat.add_le_add_right hjk 1
    have h := (hA.increments i) (j.val + 1) (k.val + 1) (by positivity) hh (hb k)
    constructor
    · exact sub_nonneg.mp h.1
    · dsimp [sample]
      linarith [h.2]
  · intro j
    exact hA.conservation _ ⟨by positivity, hb j⟩

/-- Integer endpoint counts for a three-block grid schedule. -/
def blockCounts (p q r i : Fin 3) (u v j : ℕ) : ℕ :=
  (if p = i then min j u else 0) +
  (if q = i then min j v - min j u else 0) +
  (if r = i then j - min j v else 0)

theorem blockCounts_cast (p q r i : Fin 3) (u v j : ℕ) (huv : u ≤ v) :
    (blockCounts p q r i u v j : ℝ) = occupation p q r i u v j := by
  have hmin : min j u ≤ min j v := min_le_min_left j huv
  have hj : min j v ≤ j := min_le_left _ _
  simp only [blockCounts, occupation, Nat.cast_add, Nat.cast_ite, Nat.cast_zero,
    Nat.cast_sub hmin, Nat.cast_sub hj, Nat.cast_min]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- The finite search checks all 243 words and their bounded block representations.
/-- Every five-letter word with two switches has a three-block representation,
including every endpoint count. This finite fact is checked in Lean's kernel. -/
theorem five_word_representation (a b c d e : Fin 3)
    (hs : Finite.switches [a, b, c, d, e] ≤ 2) :
    ∃ p q r : Fin 3, ∃ u v : Fin 6, u ≤ v ∧
      ∀ j : Fin 6, ∀ i : Fin 3,
        Finite.countPrefix [a, b, c, d, e] j.val i = blockCounts p q r i u.val v.val j.val := by
  revert a b c d e
  decide +kernel

/-- The active mode in unit cell `j` for integral switch positions. -/
def cellMode (p q r : Fin 3) (u v j : ℕ) : Fin 3 :=
  if j < u then p else if j < v then q else r

/-- Within each grid cell the cumulative schedule has its selected unit slope. -/
theorem occupation_cell (p q r i : Fin 3) (u v j : ℕ) (huv : u ≤ v)
    (t : ℝ) (ht : (j : ℝ) ≤ t ∧ t ≤ j + 1) :
    occupation p q r i u v t = occupation p q r i u v j +
      (if cellMode p q r u v j = i then t - j else 0) := by
  have huv' : (u : ℝ) ≤ v := by exact_mod_cast huv
  by_cases hju : j < u
  · have hj1 : (j : ℝ) + 1 ≤ u := by exact_mod_cast hju
    rw [occupation_first _ _ _ _ _ _ _ (by linarith) huv',
      occupation_first _ _ _ _ _ _ _ (by linarith) huv']
    simp only [cellMode, hju, ↓reduceIte]
    split_ifs <;> ring
  · have huj : (u : ℝ) ≤ j := by exact_mod_cast Nat.le_of_not_gt hju
    by_cases hjv : j < v
    · have hj1 : (j : ℝ) + 1 ≤ v := by exact_mod_cast hjv
      rw [occupation_second _ _ _ _ _ _ _ (by linarith) (by linarith),
        occupation_second _ _ _ _ _ _ _ huj (by linarith)]
      simp only [cellMode, hju, hjv, ↓reduceIte]
      split_ifs <;> ring
    · have hvj : (v : ℝ) ≤ j := by exact_mod_cast Nat.le_of_not_gt hjv
      rw [occupation_third _ _ _ _ _ _ _ huv' (by linarith),
        occupation_third _ _ _ _ _ _ _ huv' hvj]
      simp only [cellMode, hju, hjv, ↓reduceIte]
      split_ifs <;> ring

private theorem unit_cell_cover (t : ℝ) (ht : t ∈ Set.Icc (0 : ℝ) 5) :
    ∃ j : Fin 5, (j.val : ℝ) ≤ t ∧ t ≤ j.val + 1 := by
  by_cases h1 : t ≤ 1
  · exact ⟨0, by simpa using And.intro ht.1 h1⟩
  by_cases h2 : t ≤ 2
  · exact ⟨1, by norm_num; constructor <;> linarith⟩
  by_cases h3 : t ≤ 3
  · exact ⟨2, by norm_num; constructor <;> linarith⟩
  by_cases h4 : t ≤ 4
  · exact ⟨3, by norm_num; constructor <;> linarith⟩
  · exact ⟨4, by norm_num; constructor <;> linarith [ht.2]⟩

/-- Endpoint error certificates for three-block grid schedules control every
continuous time, for arbitrary cumulative relaxed inputs. -/
theorem five_endpoints_bound {A : Fin 3 → ℝ → ℝ} (hA : ValidCumulative A 5)
    (p q r : Fin 3) (u v : Fin 6) (huv : u ≤ v) (E : ℝ)
    (he : ∀ j : Fin 6, ∀ i : Fin 3,
      |A i j.val - occupation p q r i u.val v.val j.val| ≤ E) :
    ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) 5,
      |A i t - occupation p q r i u.val v.val t| ≤ E := by
  intro i t ht
  obtain ⟨j, hj⟩ := unit_cell_cover t ht
  have hright := he ⟨j.val + 1, by omega⟩ i
  have hleft := he ⟨j.val, by omega⟩ i
  have hcell := occupation_cell p q r i u.val v.val j.val huv t hj
  have hend := occupation_cell p q r i u.val v.val j.val huv (j.val + 1)
    ⟨by linarith, le_rfl⟩
  have hb : (j.val : ℝ) + 1 ≤ 5 := by exact_mod_cast j.isLt
  have hbound := endpoint_bound (A i) 5 j.val (j.val + 1) t
    (occupation p q r i u.val v.val j.val) E
    (decide (cellMode p q r u.val v.val j.val = i)) (hA.increments i)
    (by positivity) hj.1 hj.2 hb hleft
  simp only [Nat.cast_add, Nat.cast_one] at hright
  rw [hend] at hright
  simp only [Bool.decide_iff] at hbound
  rw [hcell]
  exact hbound hright

/-- The five-cell upper bound, stated in the endpoint language consumed here. -/
def FiveGridUpper (E : ℝ) : Prop :=
  ∀ B : Profile 5, ValidProfile B → ∃ w : List (Fin 3),
    w.length = 5 ∧ Finite.switches w ≤ 2 ∧
      ∀ j : Fin 5, ∀ i : Fin 3,
        |B j i - (Finite.countPrefix w (j.val + 1) i : ℝ)| ≤ E

private theorem five_list_representation (w : List (Fin 3)) (hw : w.length = 5)
    (hs : Finite.switches w ≤ 2) :
    ∃ p q r : Fin 3, ∃ u v : Fin 6, u ≤ v ∧
      ∀ j : Fin 6, ∀ i : Fin 3,
        Finite.countPrefix w j.val i = blockCounts p q r i u.val v.val j.val := by
  rcases w with _ | ⟨a, w⟩
  · simp at hw
  rcases w with _ | ⟨b, w⟩
  · simp at hw
  rcases w with _ | ⟨c, w⟩
  · simp at hw
  rcases w with _ | ⟨d, w⟩
  · simp at hw
  rcases w with _ | ⟨e, w⟩
  · simp at hw
  have hnil : w = [] := List.length_eq_zero_iff.mp (by simpa using hw)
  subst w
  exact five_word_representation a b c d e hs

/-- A five-cell endpoint theorem implies a continuous-time upper bound for
every cumulative relaxed input, with at most two switches. -/
theorem continuous_upper_of_five_grid {E : ℝ} (hE : 0 ≤ E)
    (hgrid : FiveGridUpper E) {A : Fin 3 → ℝ → ℝ} (hA : ValidCumulative A 5) :
    ∃ p q r : Fin 3, ∃ u v : ℝ, 0 ≤ u ∧ u ≤ v ∧ v ≤ 5 ∧
      ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) 5,
        |A i t - occupation p q r i u v t| ≤ E := by
  obtain ⟨w, hw, hs, herr⟩ := hgrid (sample A) (sample_valid hA)
  obtain ⟨p, q, r, u, v, huv, hc⟩ := five_list_representation w hw hs
  refine ⟨p, q, r, u.val, v.val, by positivity, by exact_mod_cast huv,
    by exact_mod_cast Nat.le_of_lt_succ v.isLt, ?_⟩
  apply five_endpoints_bound hA p q r u v huv E
  intro j i
  rw [← blockCounts_cast _ _ _ _ _ _ _ huv, ← hc j i]
  by_cases hj : j.val = 0
  · simp [hj, Finite.countPrefix, hA.initial, hE]
  · have hh := herr ⟨j.val - 1, by omega⟩ i
    have heq : j.val - 1 + 1 = j.val := by omega
    have heq' : ((j.val - 1 : ℕ) : ℝ) + 1 = j.val := by exact_mod_cast heq
    simpa only [sample, heq, heq'] using hh

/-- Measurable simplex-valued rates yield a valid cumulative input. -/
theorem measurable_valid {α : Fin 3 → ℝ → ℝ} {T : ℝ}
    (hα : Measurable.SimplexRates α T) :
    ValidCumulative (Measurable.cumulative α) T :=
  ⟨Measurable.cumulative_initial α, Measurable.cumulative_increments hα,
    fun _ ht => Measurable.cumulative_conservation hα ht⟩

/-- Normalize a positive time scale to the five-unit horizon. -/
theorem normalize_valid {A : Fin 3 → ℝ → ℝ} {d : ℝ} (hd : 0 < d)
    (hA : ValidCumulative A (5 * d)) :
    ValidCumulative (fun i t => A i (d * t) / d) 5 := by
  constructor
  · intro i
    simp [hA.initial]
  · intro i s t hs hst ht
    have h := (hA.increments i) (d * s) (d * t) (mul_nonneg hd.le hs)
      (mul_le_mul_of_nonneg_left hst hd.le) (by nlinarith)
    rw [← sub_div]
    constructor
    · exact div_nonneg h.1 hd.le
    · apply (div_le_iff₀ hd).mpr
      nlinarith [h.2]
  · intro t ht
    rw [← Finset.sum_div, hA.conservation (d * t)
      ⟨mul_nonneg hd.le ht.1, by nlinarith [ht.2]⟩]
    field_simp

/-- The continuous upper bound scales together with the horizon and error. -/
theorem scaled_continuous_upper_of_five_grid {E d : ℝ} (hE : 0 ≤ E) (hd : 0 < d)
    (hgrid : FiveGridUpper E) {A : Fin 3 → ℝ → ℝ}
    (hA : ValidCumulative A (5 * d)) :
    ∃ p q r : Fin 3, ∃ u v : ℝ, 0 ≤ u ∧ u ≤ v ∧ v ≤ 5 * d ∧
      ∀ i : Fin 3, ∀ t ∈ Set.Icc (0 : ℝ) (5 * d),
        |A i t - occupation p q r i u v t| ≤ d * E := by
  obtain ⟨p, q, r, u, v, hu, huv, hv, herr⟩ :=
    continuous_upper_of_five_grid hE hgrid (normalize_valid hd hA)
  refine ⟨p, q, r, d*u, d*v, mul_nonneg hd.le hu,
    mul_le_mul_of_nonneg_left huv hd.le, by nlinarith, ?_⟩
  intro i t ht
  have htime : t / d ∈ Set.Icc (0 : ℝ) 5 :=
    ⟨div_nonneg ht.1 hd.le, (div_le_iff₀ hd).mpr ht.2⟩
  have he := herr i (t / d) htime
  have htdiv : d * (t / d) = t := by field_simp
  simp only [htdiv] at he
  have hoc := occupation_scale p q r i u v (t / d) d hd.le
  rw [htdiv] at hoc
  rw [hoc]
  have he' := mul_le_mul_of_nonneg_left he hd.le
  have habs : |d * (A i t / d - occupation p q r i u v (t / d))| ≤ d * E := by
    simpa only [abs_mul, abs_of_pos hd] using he'
  simpa only [mul_sub, mul_div_cancel₀ _ hd.ne'] using habs

/-- Positive time dilation preserves the cumulative relaxed-control class. -/
theorem dilate_valid {A : Fin 3 → ℝ → ℝ} {d : ℝ} (hd : 0 < d)
    (hA : ValidCumulative A 5) :
    ValidCumulative (fun i t => d * A i (t / d)) (5 * d) := by
  constructor
  · intro i
    simp [hA.initial]
  · intro i s t hs hst ht
    have h := (hA.increments i) (s / d) (t / d) (div_nonneg hs hd.le)
      ((div_le_div_iff_of_pos_right hd).mpr hst) ((div_le_iff₀ hd).mpr ht)
    rw [← mul_sub]
    constructor
    · exact mul_nonneg hd.le h.1
    · have hh := mul_le_mul_of_nonneg_left h.2 hd.le
      simpa only [mul_sub, mul_div_cancel₀ _ hd.ne'] using hh
  · intro t ht
    rw [← Finset.mul_sum, hA.conservation (t / d)
      ⟨div_nonneg ht.1 hd.le, (div_le_iff₀ hd).mpr ht.2⟩]
    field_simp

/-- The explicit lower-bound input is a member of the cumulative class. -/
theorem witness_valid : ValidCumulative witness 5 :=
  ⟨witness_zero, witness_unit_increments, fun t _ => witness_sum t⟩

end SwitchingControl.ContinuousGrid
