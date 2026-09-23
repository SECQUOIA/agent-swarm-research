import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic

/-!
# Counting residual-certified refreshes

The deterministic cache tests at times `1, ..., T`, starting with one solve
at time zero. A failed test immediately replaces the checkpoint. Its consumed
variation interval is therefore disjoint from every later failed interval.
The budget invariant retains the unused suffix after the last checkpoint.
-/

open Finset

namespace QipmFormal.Refresh

/-- Last checkpoint after testing times `1, ..., n`. -/
noncomputable def checkpoint (cost : ℕ → ℕ → ℝ) (eta : ℝ) : ℕ → ℕ
  | 0 => 0
  | n + 1 => if eta < cost (checkpoint cost eta n) (n + 1) then n + 1
      else checkpoint cost eta n

/-- Number of solves, including the initial solve at time zero. -/
noncomputable def refreshCount (cost : ℕ → ℕ → ℝ) (eta : ℝ) : ℕ → ℕ
  | 0 => 1
  | n + 1 => if eta < cost (checkpoint cost eta n) (n + 1) then
      refreshCount cost eta n + 1 else refreshCount cost eta n

@[simp] theorem checkpoint_zero (cost : ℕ → ℕ → ℝ) (eta : ℝ) :
    checkpoint cost eta 0 = 0 := rfl

@[simp] theorem refreshCount_zero (cost : ℕ → ℕ → ℝ) (eta : ℝ) :
    refreshCount cost eta 0 = 1 := rfl

/-- The initial solve is always counted. -/
theorem one_le_refreshCount (cost : ℕ → ℕ → ℝ) (eta : ℝ) (n : ℕ) :
    1 ≤ refreshCount cost eta n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [refreshCount]
      split_ifs <;> omega

theorem refreshCount_pos (cost : ℕ → ℕ → ℝ) (eta : ℝ) (n : ℕ) :
    0 < refreshCount cost eta n := one_le_refreshCount cost eta n

/-- Failed tests add exactly one solve. -/
theorem refreshCount_of_failed {cost : ℕ → ℕ → ℝ} {eta : ℝ} {n : ℕ}
    (hfail : eta < cost (checkpoint cost eta n) (n + 1)) :
    refreshCount cost eta (n + 1) = refreshCount cost eta n + 1 := by
  rw [refreshCount, if_pos hfail]

/-- Successful tests, including equality at the threshold, add no solve. -/
theorem refreshCount_of_passed {cost : ℕ → ℕ → ℝ} {eta : ℝ} {n : ℕ}
    (hpass : cost (checkpoint cost eta n) (n + 1) ≤ eta) :
    refreshCount cost eta (n + 1) = refreshCount cost eta n := by
  rw [refreshCount, if_neg (not_lt_of_ge hpass)]

/-- With no failed tests the initial solve is the only solve. -/
theorem refresh_count_eq_one_of_no_failures {cost : ℕ → ℕ → ℝ} {eta : ℝ} {T : ℕ}
    (hpass : ∀ t < T, cost (checkpoint cost eta t) (t + 1) ≤ eta) :
    refreshCount cost eta T = 1 := by
  induction T with
  | zero => simp
  | succ n ih =>
      rw [refreshCount_of_passed (hpass n (by omega))]
      exact ih (fun t ht => hpass t (by omega))

/-- The checkpoint is never in the future. -/
theorem checkpoint_le (cost : ℕ → ℕ → ℝ) (eta : ℝ) (n : ℕ) :
    checkpoint cost eta n ≤ n := by
  induction n with
  | zero => simp
  | succ n ih =>
      rw [checkpoint]
      split_ifs <;> omega

/-- Checkpoints only move forward. -/
theorem checkpoint_monotone (cost : ℕ → ℕ → ℝ) (eta : ℝ) :
    Monotone (checkpoint cost eta) := by
  apply monotone_nat_of_le_succ
  intro n
  rw [checkpoint]
  split_ifs
  · exact (checkpoint_le cost eta n).trans (Nat.le_succ n)
  · exact le_rfl

/-- Every failed test sets the next checkpoint to that test's time. -/
theorem checkpoint_of_failed {cost : ℕ → ℕ → ℝ} {eta : ℝ} {n : ℕ}
    (hfail : eta < cost (checkpoint cost eta n) (n + 1)) :
    checkpoint cost eta (n + 1) = n + 1 := by
  rw [checkpoint, if_pos hfail]

/-- A successful test preserves the checkpoint. -/
theorem checkpoint_of_passed {cost : ℕ → ℕ → ℝ} {eta : ℝ} {n : ℕ}
    (hpass : cost (checkpoint cost eta n) (n + 1) ≤ eta) :
    checkpoint cost eta (n + 1) = checkpoint cost eta n := by
  rw [checkpoint, if_neg (not_lt_of_ge hpass)]

/-- Equality at the threshold preserves both the checkpoint and solve count. -/
theorem cache_unchanged_at_threshold {cost : ℕ → ℕ → ℝ} {eta : ℝ} {n : ℕ}
    (heq : cost (checkpoint cost eta n) (n + 1) = eta) :
    checkpoint cost eta (n + 1) = checkpoint cost eta n ∧
      refreshCount cost eta (n + 1) = refreshCount cost eta n :=
  ⟨checkpoint_of_passed heq.le, refreshCount_of_passed heq.le⟩

/-- With no failed tests the initial checkpoint is retained. -/
theorem checkpoint_eq_zero_of_no_failures {cost : ℕ → ℕ → ℝ} {eta : ℝ} {T : ℕ}
    (hpass : ∀ t < T, cost (checkpoint cost eta t) (t + 1) ≤ eta) :
    checkpoint cost eta T = 0 := by
  induction T with
  | zero => simp
  | succ n ih =>
      rw [checkpoint_of_passed (hpass n (by omega))]
      exact ih (fun t ht => hpass t (by omega))

/-- Failed intervals are disjoint, as a consequence of the cache recurrence.
The later test need not itself fail for this stronger statement. -/
theorem failed_intervals_disjoint {cost : ℕ → ℕ → ℝ} {eta : ℝ} {i j : ℕ}
    (hij : i < j) (hfail : eta < cost (checkpoint cost eta i) (i + 1)) :
    Disjoint (Ico (checkpoint cost eta i) (i + 1))
      (Ico (checkpoint cost eta j) (j + 1)) := by
  have hsep : i + 1 ≤ checkpoint cost eta j := by
    rw [← checkpoint_of_failed hfail]
    exact checkpoint_monotone cost eta (Nat.succ_le_of_lt hij)
  apply Finset.disjoint_left.mpr
  intro k hki hkj
  have hi := (Finset.mem_Ico.mp hki).2
  have hj := (Finset.mem_Ico.mp hkj).1
  omega

/-- A failed test consumes strictly more than the threshold amount of variation. -/
theorem failed_test_charge_strict {G epsilon eta variation test : ℝ}
    (hG : 0 < G) (hepsilon : epsilon ≤ eta / (2 * G))
    (hbound : test ≤ G * (epsilon + variation)) (hfail : eta < test) :
    eta / (2 * G) < variation := by
  have heps : epsilon * (2 * G) ≤ eta :=
    (le_div_iff₀ (by positivity : 0 < 2 * G)).mp hepsilon
  apply (div_lt_iff₀ (by positivity : 0 < 2 * G)).mpr
  nlinarith

/-- Weak form of the strict charge, convenient for the budget invariant. -/
theorem failed_test_charge {G epsilon eta variation test : ℝ}
    (hG : 0 < G) (hepsilon : epsilon ≤ eta / (2 * G))
    (hbound : test ≤ G * (epsilon + variation)) (hfail : eta < test) :
    eta / (2 * G) ≤ variation :=
  (failed_test_charge_strict hG hepsilon hbound hfail).le

/-- Each failure is charged once; variation since the last checkpoint is
retained in the invariant, so successful tests cannot spend it twice. -/
theorem refresh_budget {cost : ℕ → ℕ → ℝ} {delta : ℕ → ℝ}
    {G epsilon eta : ℝ} {T : ℕ}
    (hG : 0 < G) (hepsilon : epsilon ≤ eta / (2 * G))
    (htest : ∀ t < T, cost (checkpoint cost eta t) (t + 1) ≤
      G * (epsilon + ∑ j ∈ Ico (checkpoint cost eta t) (t + 1), delta j)) :
    ((refreshCount cost eta T : ℝ) - 1) * (eta / (2 * G)) +
      (∑ j ∈ Ico (checkpoint cost eta T) T, delta j) ≤ ∑ j ∈ range T, delta j := by
  induction T with
  | zero => simp
  | succ n ih =>
      have hprev := ih (fun t ht => htest t (by omega))
      have hexpand := Finset.sum_Ico_succ_top (f := delta) (checkpoint_le cost eta n)
      rw [Finset.sum_range_succ]
      by_cases hfail : eta < cost (checkpoint cost eta n) (n + 1)
      · have hcharge := failed_test_charge hG hepsilon (htest n (by omega)) hfail
        rw [checkpoint_of_failed hfail, refreshCount, if_pos hfail]
        simp only [Ico_self, sum_empty, add_zero, Nat.cast_add, Nat.cast_one]
        linarith
      · rw [checkpoint, if_neg hfail, refreshCount, if_neg hfail, hexpand]
        linarith

/-- The finite pathwise refresh bound. A zero-length path costs exactly its
initial solve, and any successful suffix is handled by nonnegativity. -/
theorem refresh_count_bound {cost : ℕ → ℕ → ℝ} {delta : ℕ → ℝ}
    {G epsilon eta : ℝ} {T : ℕ}
    (hG : 0 < G) (heta : 0 < eta) (hepsilon : epsilon ≤ eta / (2 * G))
    (hdelta : ∀ j < T, 0 ≤ delta j)
    (htest : ∀ t < T, cost (checkpoint cost eta t) (t + 1) ≤
      G * (epsilon + ∑ j ∈ Ico (checkpoint cost eta t) (t + 1), delta j)) :
    (refreshCount cost eta T : ℝ) ≤ 1 + 2 * G * (∑ j ∈ range T, delta j) / eta := by
  have hbudget := refresh_budget hG hepsilon htest
  have htail : 0 ≤ ∑ j ∈ Ico (checkpoint cost eta T) T, delta j := by
    apply Finset.sum_nonneg
    intro j hj
    exact hdelta j (Finset.mem_Ico.mp hj).2
  have hcharge : ((refreshCount cost eta T : ℝ) - 1) * (eta / (2 * G)) ≤
      ∑ j ∈ range T, delta j := by linarith
  have hcharge' : ((refreshCount cost eta T : ℝ) - 1) * eta ≤
      (∑ j ∈ range T, delta j) * (2 * G) := by
    apply (div_le_iff₀ (by positivity : 0 < 2 * G)).mp
    simpa only [mul_div_assoc] using hcharge
  calc
    (refreshCount cost eta T : ℝ) ≤
        (eta + 2 * G * (∑ j ∈ range T, delta j)) / eta := by
      apply (le_div_iff₀ heta).mpr
      nlinarith
    _ = (1 + 2 * G * (∑ j ∈ range T, delta j) / eta) := by
      rw [add_div, div_self heta.ne']

/-- Zero projective variation requires only the initial solve. -/
theorem refresh_count_eq_one_of_zero_variation {cost : ℕ → ℕ → ℝ} {delta : ℕ → ℝ}
    {G epsilon eta : ℝ} {T : ℕ}
    (hG : 0 < G) (heta : 0 < eta) (hepsilon : epsilon ≤ eta / (2 * G))
    (hdelta : ∀ j < T, 0 ≤ delta j)
    (htest : ∀ t < T, cost (checkpoint cost eta t) (t + 1) ≤
      G * (epsilon + ∑ j ∈ Ico (checkpoint cost eta t) (t + 1), delta j))
    (hzero : ∑ j ∈ range T, delta j = 0) :
    refreshCount cost eta T = 1 := by
  have hbound := refresh_count_bound hG heta hepsilon hdelta htest
  rw [hzero] at hbound
  have hle : refreshCount cost eta T ≤ 1 := by
    exact_mod_cast (by simpa using hbound : (refreshCount cost eta T : ℝ) ≤ 1)
  exact Nat.le_antisymm hle (one_le_refreshCount cost eta T)

end QipmFormal.Refresh
