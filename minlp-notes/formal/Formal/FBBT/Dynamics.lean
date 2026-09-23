import Formal.FBBT.Contractors

namespace FBBT

/-- Bernoulli's bound in the form used by the slow affine recurrence. -/
theorem geometric_error_le (b c : ℝ) (_hb : 0 ≤ b) (hc : 0 ≤ c)
    (hbc : b + c = 1) (k : ℕ) : 1 - c ^ k ≤ (k : ℝ) * b := by
  have h := one_add_mul_le_pow (R := ℝ) (a := -b) (by linarith) k
  have heq : 1 + -b = c := by linarith
  rw [heq] at h
  nlinarith

/-- Every affine application costs at most one term of the geometric recurrence;
other updates leave the designated endpoint unchanged. -/
theorem schedule_geometric_bound (b c : ℝ) (hc : 0 ≤ c) (hbc : b + c = 1)
    (z : ℕ → ℝ) (isAffine : ℕ → Prop) [DecidablePred isAffine]
    (hz : z 0 = 0)
    (hstep : ∀ t, if isAffine t then z (t + 1) ≤ b + c * z t
      else z (t + 1) = z t) :
    ∀ t, z t ≤ 1 - c ^ ((Finset.range t).filter isAffine).card := by
  intro t
  induction t with
  | zero => simp [hz]
  | succ t ih =>
    rw [Finset.range_add_one, Finset.filter_insert]
    split_ifs with ha
    · have hnot : t ∉ (Finset.range t).filter isAffine := by simp
      rw [Finset.card_insert_of_notMem hnot, pow_succ]
      have hs := hstep t
      simp only [ha, ↓reduceIte] at hs
      have hm := mul_le_mul_of_nonneg_left ih hc
      nlinarith
    · have hs := hstep t
      simp only [ha, ↓reduceIte] at hs
      simpa [hs] using ih

/-- A designated endpoint at least one half forces a doubly exponential number
of affine updates when the circuit parameter is `2 ^ (-(2 ^ n))`. -/
theorem threshold_update_count (n k : ℕ) (z : ℝ)
    (hbound : z ≤ (k : ℝ) * ((2 : ℝ) ^ (2 ^ n))⁻¹)
    (hhalf : (1 : ℝ) / 2 ≤ z) : 2 ^ (2 ^ n - 1) ≤ k := by
  have hp : 0 < (2 : ℝ) ^ (2 ^ n) := by positivity
  have hmul : (2 : ℝ) ^ (2 ^ n) / 2 ≤ (k : ℝ) := by
    have h := (le_div_iff₀ hp).mp (show (1 : ℝ) / 2 ≤ (k : ℝ) / 2 ^ (2 ^ n) by
      simpa only [div_eq_mul_inv] using hhalf.trans hbound)
    linarith
  have hexp : 2 ^ n - 1 + 1 = 2 ^ n := Nat.sub_add_cancel Nat.one_le_two_pow
  have heq : (2 : ℝ) ^ (2 ^ n) / 2 = 2 ^ (2 ^ n - 1) := by
    conv_lhs => rw [← hexp, pow_succ]
    ring
  rw [heq] at hmul
  exact_mod_cast hmul

/-- Fairness means that an update of each kind occurs after every time index.
There is no upper bound on the delays between updates. -/
def Fair (isAffine isProduct : ℕ → Prop) : Prop :=
  (∀ n, ∃ t ≥ n, isAffine t) ∧ (∀ n, ∃ t ≥ n, isProduct t)

/-- Monotone primitive propagation converges to the unique feedback solution
under every fair schedule, even if update delays are unbounded. -/
theorem fair_feedback_converges (b c : ℝ) (hb : 0 < b) (hc : 0 ≤ c)
    (hbc : b + c = 1) (z w : ℕ → ℝ) (isAffine : ℕ → Prop)
    (isProduct : ℕ → Prop) (hfair : Fair isAffine isProduct) (hmz : Monotone z) (hmw : Monotone w)
    (hzu : ∀ t, z t ≤ 1) (hwu : ∀ t, w t ≤ c)
    (ha : ∀ t, isAffine t → b + w t ≤ z (t + 1))
    (hp : ∀ t, isProduct t → c * z t ≤ w (t + 1)) :
    Filter.Tendsto z Filter.atTop (nhds 1) ∧
      Filter.Tendsto w Filter.atTop (nhds c) := by
  have hzb : BddAbove (Set.range z) := ⟨1, by rintro _ ⟨t, rfl⟩; exact hzu t⟩
  have hwb : BddAbove (Set.range w) := ⟨c, by rintro _ ⟨t, rfl⟩; exact hwu t⟩
  have hzt := tendsto_atTop_ciSup hmz hzb
  have hwt := tendsto_atTop_ciSup hmw hwb
  have hzsup : (⨆ t, z t) ≤ 1 := ciSup_le hzu
  have hwsup : (⨆ t, w t) ≤ c := ciSup_le hwu
  have hprod : c * (⨆ t, z t) ≤ ⨆ t, w t := by
    apply le_of_tendsto' (hzt.const_mul c)
    intro n
    obtain ⟨t, hnt, ht⟩ := hfair.2 n
    exact (mul_le_mul_of_nonneg_left (hmz hnt) hc).trans
      ((hp t ht).trans (le_ciSup hwb (t + 1)))
  have haff : b + (⨆ t, w t) ≤ ⨆ t, z t := by
    apply le_of_tendsto' (tendsto_const_nhds.add hwt)
    intro n
    obtain ⟨t, hnt, ht⟩ := hfair.1 n
    have h := (ha t ht).trans (le_ciSup hzb (t + 1))
    have hm := hmw hnt
    linarith
  have hzeq : (⨆ t, z t) = 1 := by nlinarith
  have hweq : (⨆ t, w t) = c := by rw [hzeq] at hprod; nlinarith
  exact ⟨hzeq ▸ hzt, hweq ▸ hwt⟩

/-- An upstream primitive does not alter `z,w` after the upstream circuit is fixed. -/
inductive FeedbackAction where
  | product
  | affine
  | idle
  deriving DecidableEq

def feedbackStep (b c : ℝ) (a : FeedbackAction) (B : FeedbackBox) : FeedbackBox :=
  match a with
  | .product => productUpdate c B
  | .affine => affineUpdate b c B
  | .idle => B

def feedbackRun (b c : ℝ) (schedule : ℕ → FeedbackAction) : ℕ → FeedbackBox
  | 0 => initialBox
  | t + 1 => feedbackStep b c (schedule t) (feedbackRun b c schedule t)

def affineCount (schedule : ℕ → FeedbackAction) (t : ℕ) : ℕ :=
  ((Finset.range t).filter (fun j => schedule j = .affine)).card

theorem feedbackRun_good (b c : ℝ) (hb : 0 < b) (hc : 0 < c) (hs : b + c = 1)
    (schedule : ℕ → FeedbackAction) (t : ℕ) : Good b c (feedbackRun b c schedule t) := by
  induction t with
  | zero => exact initial_good hb hc hs
  | succ t ih =>
    simp only [feedbackRun]
    cases schedule t with
    | product => exact ih.product_good
    | affine => exact ih.affine_good
    | idle => exact ih

/-- Geometric upper bound for the actual simultaneous primitive interval hulls. -/
theorem feedbackRun_geometric_bound (b c : ℝ) (hb : 0 < b) (hc : 0 < c)
    (hs : b + c = 1) (schedule : ℕ → FeedbackAction) (t : ℕ) :
    (feedbackRun b c schedule t).lz ≤ 1 - c ^ affineCount schedule t := by
  apply schedule_geometric_bound b c hc.le hs
    (fun t => (feedbackRun b c schedule t).lz) (fun t => schedule t = .affine) rfl
  intro j
  have hg := feedbackRun_good b c hb hc hs schedule j
  cases hj : schedule j with
  | product => simp [feedbackRun, hj, feedbackStep, productUpdate]
  | affine => simpa [feedbackRun, hj, feedbackStep] using hg.affine_lz_le
  | idle => simp [feedbackRun, hj, feedbackStep]

/-- Linear upper bound, uniform over every finite schedule prefix. -/
theorem feedbackRun_linear_bound (b c : ℝ) (hb : 0 < b) (hc : 0 < c)
    (hs : b + c = 1) (schedule : ℕ → FeedbackAction) (t : ℕ) :
    (feedbackRun b c schedule t).lz ≤ (affineCount schedule t : ℝ) * b :=
  (feedbackRun_geometric_bound b c hb hc hs schedule t).trans
    (geometric_error_le b c hb.le hc.le hs _)

/-- Both feedback endpoints increase monotonically under arbitrary primitive schedules. -/
theorem feedbackRun_monotone (b c : ℝ) (hb : 0 < b) (hc : 0 < c)
    (hs : b + c = 1) (schedule : ℕ → FeedbackAction) :
    Monotone (fun t => (feedbackRun b c schedule t).lz) ∧
      Monotone (fun t => (feedbackRun b c schedule t).lw) := by
  constructor <;> apply monotone_nat_of_le_succ <;> intro t
  · cases ht : schedule t <;> simp [feedbackRun, ht, feedbackStep, productUpdate, affineUpdate]
  · have hg := feedbackRun_good b c hb hc hs schedule t
    cases ht : schedule t with
    | product => simpa only [feedbackRun, ht, feedbackStep, productUpdate] using hg.lw_le
    | affine =>
      simp only [feedbackRun, ht, feedbackStep, affineUpdate, le_max_iff, le_refl, true_or]
    | idle => simp only [feedbackRun, ht, feedbackStep, le_refl]

/-- Fair runs of the exact primitive hull updates reach `(1,c)` in the limit. -/
theorem feedbackRun_converges (b c : ℝ) (hb : 0 < b) (hc : 0 < c)
    (hs : b + c = 1) (schedule : ℕ → FeedbackAction)
    (hfair : Fair (fun t => schedule t = .affine) (fun t => schedule t = .product)) :
    Filter.Tendsto (fun t => (feedbackRun b c schedule t).lz) Filter.atTop (nhds 1) ∧
      Filter.Tendsto (fun t => (feedbackRun b c schedule t).lw) Filter.atTop (nhds c) := by
  have hm := feedbackRun_monotone b c hb hc hs schedule
  apply fair_feedback_converges b c hb hc.le hs _ _ _ _ hfair hm.1 hm.2
  · intro t; exact (feedbackRun_good b c hb hc hs schedule t).lz_le_one
  · intro t
    have hg := feedbackRun_good b c hb hc hs schedule t
    exact hg.lw_le.trans (by nlinarith [hg.lz_le_one])
  · intro t ht
    simp [feedbackRun, ht, feedbackStep, affineUpdate]
  · intro t ht
    simp [feedbackRun, ht, feedbackStep, productUpdate]

/-- At least the claimed number of affine applications is necessary to reach one half. -/
theorem feedbackRun_threshold (n : ℕ) (b c : ℝ) (hb : 0 < b) (hc : 0 < c)
    (hs : b + c = 1) (hparam : b = ((2 : ℝ) ^ (2 ^ n))⁻¹)
    (schedule : ℕ → FeedbackAction) (t : ℕ)
    (hhalf : (1 : ℝ) / 2 ≤ (feedbackRun b c schedule t).lz) :
    2 ^ (2 ^ n - 1) ≤ affineCount schedule t := by
  apply threshold_update_count n _ _ _ hhalf
  simpa [hparam] using feedbackRun_linear_bound b c hb hc hs schedule t

/-- No finite sequence reaches the limiting lower bound exactly. -/
theorem feedbackRun_lt_one (b c : ℝ) (hb : 0 < b) (hc : 0 < c)
    (hs : b + c = 1) (schedule : ℕ → FeedbackAction) (t : ℕ) :
    (feedbackRun b c schedule t).lz < 1 := by
  have h := feedbackRun_geometric_bound b c hb hc hs schedule t
  have hp : 0 < c ^ affineCount schedule t := pow_pos hc _
  linarith

/-- At the initial box, every primitive changes every endpoint by at most `b`,
while the designated lower endpoint is at distance one from its limiting value. -/
theorem initial_small_changes (b c : ℝ) (hb : 0 < b) (_hc : 0 < c)
    (hs : b + c = 1) (a : FeedbackAction) :
    |(feedbackStep b c a initialBox).lz - initialBox.lz| ≤ b ∧
    |(feedbackStep b c a initialBox).lw - initialBox.lw| ≤ b ∧
    |(feedbackStep b c a initialBox).uz - initialBox.uz| ≤ b ∧
    |(feedbackStep b c a initialBox).uw - initialBox.uw| ≤ b ∧
    |1 - initialBox.lz| = 1 := by
  have hc1 : c - 1 = -b := by linarith
  cases a <;>
    simp [feedbackStep, initialBox, productUpdate, affineUpdate, hc1,
      hb.le, abs_of_nonneg hb.le]

end FBBT
