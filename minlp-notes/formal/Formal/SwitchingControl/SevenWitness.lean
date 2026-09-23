import Mathlib.Data.Fin.VecNotation
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Data.Fintype.Pi
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-! Exact optimization of the seven-cell rational witness over all mode words.

Discrepancy is the maximum cumulative error at cell endpoints.  The integer
numerators avoid any floating-point arithmetic in the finite certificate.
-/

namespace SwitchingControl.SevenWitness

abbrev Word (n : ℕ) := Fin n → Fin 3

/-- Number of changes between adjacent cells. -/
def switches {n : ℕ} (w : Word n) : ℕ :=
  ∑ j : Fin (n - 1), if w ⟨j.val, by omega⟩ = w ⟨j.val + 1, by omega⟩ then 0 else 1

/-- The count of cells assigned to mode `i`, through endpoint `j + 1`. -/
def count {n : ℕ} (w : Word n) (j : Fin n) (i : Fin 3) : ℕ :=
  (Finset.univ.filter fun k : Fin n => k ≤ j ∧ w k = i).card

/-- Three times the cumulative relaxed profile of the seven-cell instance. -/
def target : Fin 7 → Fin 3 → ℤ :=
  ![![1, 1, 1], ![4, 1, 1], ![4, 4, 1], ![4, 4, 4],
    ![7, 4, 4], ![8, 5, 5], ![8, 5, 8]]

/-- Maximum absolute numerator error; actual discrepancy is this divided by 3. -/
def scaledError (w : Word 7) : ℕ :=
  Finset.univ.sup fun j : Fin 7 =>
    Finset.univ.sup fun i : Fin 3 => (target j i - 3 * (count w j i : ℤ)).natAbs

/-- Exact rational endpoint discrepancy of a seven-cell word. -/
def discrepancy (w : Word 7) : ℚ := scaledError w / 3

/-- The attaining word from the paper. -/
def witness : Word 7 := ![0, 0, 1, 1, 0, 2, 2]

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Finite exhaustive reduction needs more than the default tactic budget.
/-- Exhaustive kernel reduction over all `3^7` words. -/
theorem all_vectors_lower : ∀ a b c d e f g : Fin 3,
    switches ![a, b, c, d, e, f, g] ≤ 3 → 4 ≤ scaledError ![a, b, c, d, e, f, g] := by
  decide +kernel

theorem all_words_lower (w : Word 7) : switches w ≤ 3 → 4 ≤ scaledError w := by
  have hw : w = ![w 0, w 1, w 2, w 3, w 4, w 5, w 6] := by
    funext j
    fin_cases j <;> rfl
  rw [hw]
  exact all_vectors_lower _ _ _ _ _ _ _

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Finite exhaustive reduction needs more than the default tactic budget.
theorem witness_switches : switches witness = 3 := by decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Finite exhaustive reduction needs more than the default tactic budget.
theorem witness_scaledError : scaledError witness = 4 := by decide +kernel

/-- Every word with at most three switches has discrepancy at least `4/3`. -/
theorem discrepancy_lower (w : Word 7) (h : switches w ≤ 3) :
    (4 : ℚ) / 3 ≤ discrepancy w := by
  unfold discrepancy
  exact div_le_div_of_nonneg_right (by exact_mod_cast all_words_lower w h) (by norm_num)

/-- The finite-grid optimum for the concrete seven-cell instance is exactly `4/3`. -/
theorem optimum : switches witness ≤ 3 ∧ discrepancy witness = (4 : ℚ) / 3 ∧
    ∀ w : Word 7, switches w ≤ 3 → (4 : ℚ) / 3 ≤ discrepancy w := by
  refine ⟨by rw [witness_switches], ?_, discrepancy_lower⟩
  simp [discrepancy, witness_scaledError]

/-- Cell rates of the relaxed witness, each a probability vector. -/
def relaxedRates : Fin 7 → Fin 3 → ℚ :=
  ![![1/3, 1/3, 1/3], ![1, 0, 0], ![0, 1, 0], ![0, 0, 1],
    ![1, 0, 0], ![1/3, 1/3, 1/3], ![0, 0, 1]]

theorem relaxedRates_nonneg : ∀ j i, 0 ≤ relaxedRates j i := by decide +kernel

theorem relaxedRates_sum : ∀ j, ∑ i, relaxedRates j i = 1 := by decide +kernel

set_option maxRecDepth 100000 in
/-- The integer target really is three times the cumulative relaxed input. -/
theorem target_eq_cumulative : ∀ j i, (target j i : ℚ) / 3 =
    ∑ k ∈ Finset.univ.filter (fun k : Fin 7 => k ≤ j), relaxedRates k i := by
  decide +kernel

/-- The scaled-error definition is exactly the maximum of endpoint errors. -/
theorem scaledError_le_iff (w : Word 7) (b : ℕ) :
    scaledError w ≤ b ↔
      ∀ j i, (target j i - 3 * (count w j i : ℤ)).natAbs ≤ b := by
  simp [scaledError, Finset.sup_le_iff]

/-- Numerator scaling agrees with the usual rational absolute endpoint error. -/
theorem endpoint_error_eq (w : Word 7) (j : Fin 7) (i : Fin 3) :
    |(target j i : ℚ) / 3 - count w j i| =
      ((target j i - 3 * (count w j i : ℤ)).natAbs : ℚ) / 3 := by
  rw [Nat.cast_natAbs, Int.cast_abs]
  push_cast
  calc
    |(target j i : ℚ) / 3 - count w j i| =
        |((target j i : ℚ) - 3 * count w j i) / 3| := by congr 1; ring
    _ = _ := by rw [abs_div]; norm_num

/-- The discrepancy bound holds exactly when every cumulative endpoint error does. -/
theorem discrepancy_le_iff (w : Word 7) (b : ℚ) :
    discrepancy w ≤ b ↔ ∀ j i, |(target j i : ℚ) / 3 - count w j i| ≤ b := by
  constructor
  · intro h j i
    rw [endpoint_error_eq]
    apply le_trans _ h
    unfold discrepancy
    apply div_le_div_of_nonneg_right _ (by norm_num)
    exact_mod_cast (show (target j i - 3 * (count w j i : ℤ)).natAbs ≤ scaledError w from
      le_trans (Finset.le_sup (f := fun i : Fin 3 =>
        (target j i - 3 * (count w j i : ℤ)).natAbs) (Finset.mem_univ i))
        (Finset.le_sup (f := fun j : Fin 7 => Finset.univ.sup fun i : Fin 3 =>
          (target j i - 3 * (count w j i : ℤ)).natAbs) (Finset.mem_univ j)))
  · intro h
    obtain ⟨j, _, hj⟩ := Finset.exists_mem_eq_sup (Finset.univ : Finset (Fin 7))
      Finset.univ_nonempty (fun j => Finset.univ.sup fun i : Fin 3 =>
        (target j i - 3 * (count w j i : ℤ)).natAbs)
    obtain ⟨i, _, hi⟩ := Finset.exists_mem_eq_sup (Finset.univ : Finset (Fin 3))
      Finset.univ_nonempty (fun i => (target j i - 3 * (count w j i : ℤ)).natAbs)
    simpa [discrepancy, scaledError, hj, hi, endpoint_error_eq] using h j i

/-- Pure input alternating between modes zero and one. -/
def alternating (n : ℕ) : Word n := fun j => ⟨j.val % 2, by omega⟩

/-- Integer endpoint discrepancy between two pure mode words. -/
def integerError {n : ℕ} (v w : Word n) : ℕ :=
  Finset.univ.sup fun j : Fin n =>
    Finset.univ.sup fun i : Fin 3 => ((count v j i : ℤ) - count w j i).natAbs

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive reduction checks every one of the 243 five-cell words.
theorem five_alternating_lower :
    ∀ w : Word 5, switches w ≤ 2 → 1 ≤ integerError (alternating 5) w := by
  decide +kernel

set_option maxRecDepth 100000 in
set_option maxHeartbeats 0 in
-- Exhaustive reduction checks every one of the 729 six-cell words.
theorem six_alternating_lower :
    ∀ w : Word 6, switches w ≤ 3 → 1 ≤ integerError (alternating 6) w := by
  decide +kernel

/-- A five-cell schedule attaining error one for the lower-bound instance. -/
theorem five_alternating_attained :
    switches (![0, 0, 0, 1, 1] : Word 5) ≤ 2 ∧
    integerError (alternating 5) ![0, 0, 0, 1, 1] = 1 := by decide +kernel

/-- A six-cell schedule attaining error one for the lower-bound instance. -/
theorem six_alternating_attained :
    switches (![0, 0, 0, 1, 1, 1] : Word 6) ≤ 3 ∧
    integerError (alternating 6) ![0, 0, 0, 1, 1, 1] = 1 := by decide +kernel

/-- A real endpoint must incur error at least `4/3` under the switch budget. -/
theorem real_lower (w : Word 7) (h : switches w ≤ 3) :
    ∃ j i, (4 : ℝ) / 3 ≤ |(target j i : ℝ) / 3 - count w j i| := by
  obtain ⟨j, _, hj⟩ := Finset.exists_mem_eq_sup (Finset.univ : Finset (Fin 7))
    Finset.univ_nonempty (fun j => Finset.univ.sup fun i : Fin 3 =>
      (target j i - 3 * (count w j i : ℤ)).natAbs)
  obtain ⟨i, _, hi⟩ := Finset.exists_mem_eq_sup (Finset.univ : Finset (Fin 3))
    Finset.univ_nonempty (fun i => (target j i - 3 * (count w j i : ℤ)).natAbs)
  refine ⟨j, i, ?_⟩
  have hn : 4 ≤ (target j i - 3 * (count w j i : ℤ)).natAbs := by
    simpa [scaledError, hj, hi] using all_words_lower w h
  have hq : (4 : ℚ) / 3 ≤ |(target j i : ℚ) / 3 - count w j i| := by
    rw [endpoint_error_eq]
    exact div_le_div_of_nonneg_right (by exact_mod_cast hn) (by norm_num)
  have hh := (Rat.cast_le (K := ℝ)).mpr hq
  simpa only [Rat.cast_div, Rat.cast_abs, Rat.cast_sub, Rat.cast_natCast,
    Rat.cast_intCast, Rat.cast_ofNat] using hh

/-- The attaining word meets the same endpoint bound over the real numbers. -/
theorem real_witness_upper :
    ∀ j i, |(target j i : ℝ) / 3 - count witness j i| ≤ (4 : ℝ) / 3 := by
  intro j i
  have hq := (discrepancy_le_iff witness ((4 : ℚ) / 3)).mp (le_of_eq optimum.2.1) j i
  have hh := (Rat.cast_le (K := ℝ)).mpr hq
  simpa only [Rat.cast_div, Rat.cast_abs, Rat.cast_sub, Rat.cast_natCast,
    Rat.cast_intCast, Rat.cast_ofNat] using hh

/-- A positive integer maximum error is realized at an endpoint, also over `ℝ`. -/
theorem pure_real_lower {n : ℕ} [NeZero n] (v w : Word n)
    (h : 1 ≤ integerError v w) :
    ∃ j i, (1 : ℝ) ≤ |(count v j i : ℝ) - count w j i| := by
  obtain ⟨j, _, hj⟩ := Finset.exists_mem_eq_sup (Finset.univ : Finset (Fin n))
    Finset.univ_nonempty (fun j => Finset.univ.sup fun i : Fin 3 =>
      ((count v j i : ℤ) - count w j i).natAbs)
  obtain ⟨i, _, hi⟩ := Finset.exists_mem_eq_sup (Finset.univ : Finset (Fin 3))
    Finset.univ_nonempty (fun i => ((count v j i : ℤ) - count w j i).natAbs)
  refine ⟨j, i, ?_⟩
  have hn : 1 ≤ ((count v j i : ℤ) - count w j i).natAbs := by
    simpa [integerError, hj, hi] using h
  have hz : (1 : ℤ) ≤ (((count v j i : ℤ) - count w j i).natAbs : ℤ) := by
    exact_mod_cast hn
  rw [Int.natCast_natAbs] at hz
  exact_mod_cast hz

theorem five_real_lower (w : Word 5) (h : switches w ≤ 2) :
    ∃ j i, (1 : ℝ) ≤ |(count (alternating 5) j i : ℝ) - count w j i| :=
  pure_real_lower _ _ (five_alternating_lower w h)

theorem six_real_lower (w : Word 6) (h : switches w ≤ 3) :
    ∃ j i, (1 : ℝ) ≤ |(count (alternating 6) j i : ℝ) - count w j i| :=
  pure_real_lower _ _ (six_alternating_lower w h)

end SwitchingControl.SevenWitness
