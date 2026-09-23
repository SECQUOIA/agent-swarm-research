import Formal.FBBT.OriginalRun

/-! Schedule-independent doubly exponential primitive iteration lower bounds. -/
namespace FBBT

/-- Applications of the designated affine equation `z = b_n + w`. -/
def designatedCount {n : ℕ} (schedule : ℕ → CircuitVar n) (t : ℕ) : ℕ :=
  ((Finset.range t).filter fun k => schedule k = .z).card

theorem feedback_count_eq {n : ℕ} (schedule : ℕ → CircuitVar n) (t : ℕ) :
    affineCount (fun k => feedbackAction (schedule k)) t = designatedCount schedule t := by
  unfold affineCount designatedCount
  congr 1
  ext k
  simp only [Finset.mem_filter]
  cases schedule k <;> simp [feedbackAction]

theorem strongRun_nonempty (n : ℕ) (schedule : ℕ → CircuitVar n) (t : ℕ) :
    (strongRun n schedule t).carrier.Nonempty := by
  let Q := feedbackRun (bValue n) (cValue n) (fun k => feedbackAction (schedule k)) t
  have hg := feedbackRun_good (bValue n) (cValue n) (bValue_pos n) (cValue_pos n)
    (bValue_add_cValue n) (fun k => feedbackAction (schedule k)) t
  exact ⟨embed n (1, cValue n), (embed_mem_strongBox_iff n _ Q).mpr hg.feasible⟩

/-- Fixing the upstream circuit exactly can only increase the designated lower bound. -/
theorem PrimitiveRun.le_strong {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    (states t).lower .z ≤
      (feedbackRun (bValue n) (cValue n) (fun k => feedbackAction (schedule k)) t).lz := by
  have hs := (strongRun_isRun n schedule).comparison h (strongBox_initial_subset_unit n) t
  exact Box.lower_mono hs (strongRun_nonempty n schedule t) .z

/-- The geometric bound holds for every original run and every finite prefix;
fairness is unnecessary for this iteration lower bound. -/
theorem PrimitiveRun.geometric_bound {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    (states t).lower .z ≤ 1 - (cValue n) ^ designatedCount schedule t := by
  have hg := feedbackRun_geometric_bound (bValue n) (cValue n) (bValue_pos n)
    (cValue_pos n) (bValue_add_cValue n) (fun k => feedbackAction (schedule k)) t
  rw [feedback_count_eq] at hg
  exact (h.le_strong t).trans hg

theorem PrimitiveRun.linear_bound {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    (states t).lower .z ≤ (designatedCount schedule t : ℝ) * bValue n :=
  (h.geometric_bound t).trans
    (geometric_error_le _ _ (bValue_pos n).le (cValue_pos n).le (bValue_add_cValue n) _)

/-- At least `2^(2^n-1)` applications of the affine equation are required before
an original unit-box run can raise its designated lower endpoint to one half. -/
theorem PrimitiveRun.threshold {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ)
    (hhalf : (1 : ℝ) / 2 ≤ (states t).lower .z) :
    2 ^ (2 ^ n - 1) ≤ designatedCount schedule t := by
  apply threshold_update_count n _ _ _ hhalf
  simpa only [bValue_inverse_power] using h.linear_bound t

/-- The same bound holds for total primitive updates. -/
theorem PrimitiveRun.total_updates {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ)
    (hhalf : (1 : ℝ) / 2 ≤ (states t).lower .z) : 2 ^ (2 ^ n - 1) ≤ t := by
  apply (h.threshold t hhalf).trans
  exact (Finset.card_filter_le _ _).trans_eq (Finset.card_range t)

/-- No finite original primitive schedule reaches the limiting lower endpoint exactly. -/
theorem PrimitiveRun.z_lt_one {n : ℕ} {schedule : ℕ → CircuitVar n}
    {states : ℕ → Box (CircuitVar n)} (h : PrimitiveRun n schedule states) (t : ℕ) :
    (states t).lower .z < 1 :=
  (h.le_strong t).trans_lt (feedbackRun_lt_one (bValue n) (cValue n) (bValue_pos n)
    (cValue_pos n) (bValue_add_cValue n) (fun k => feedbackAction (schedule k)) t)

/-- The main iteration theorem, with both arbitrary-order lower bound and fair limit. -/
theorem doubly_exponential_fbbt (n : ℕ) (schedule : ℕ → CircuitVar n)
    (states : ℕ → Box (CircuitVar n)) (h : PrimitiveRun n schedule states)
    (hf : FairSchedule schedule) :
    Filter.Tendsto (fun t => (states t).lower .z) Filter.atTop (nhds 1) ∧
    (∀ t, (1 : ℝ) / 2 ≤ (states t).lower .z → 2 ^ (2 ^ n - 1) ≤ designatedCount schedule t) ∧
    (∀ t, (states t).lower .z < 1) :=
  ⟨h.z_tendsto_one hf, h.threshold, h.z_lt_one⟩

/-- A concrete fair schedule cycles through the finite equation list. -/
noncomputable def roundRobin (n t : ℕ) : CircuitVar n :=
  (Fintype.equivFin (CircuitVar n)).symm
    ⟨t % Fintype.card (CircuitVar n), Nat.mod_lt _
      (Fintype.card_pos_iff.mpr ⟨CircuitVar.z⟩)⟩

theorem roundRobin_fair (n : ℕ) : FairSchedule (roundRobin n) := by
  intro i t
  let m := Fintype.card (CircuitVar n)
  let j := Fintype.equivFin (CircuitVar n) i
  have hm : 0 < m := Fintype.card_pos_iff.mpr ⟨CircuitVar.z⟩
  refine ⟨m * t + j.val, by nlinarith, ?_⟩
  unfold roundRobin
  apply (Fintype.equivFin (CircuitVar n)).injective
  simp only [Equiv.apply_symm_apply]
  apply Fin.ext
  change (m * t + j.val) % m = j.val
  have hj : j.val < m := j.isLt
  simp [Nat.add_mod, Nat.mod_eq_of_lt hj]

/-- An explicit fair run exists and satisfies the complete slow-convergence theorem. -/
theorem canonical_slow_run (n : ℕ) :
    PrimitiveRun n (roundRobin n) (originalRun n (roundRobin n)) ∧
    Filter.Tendsto (fun t => (originalRun n (roundRobin n) t).lower .z)
      Filter.atTop (nhds 1) ∧
    (∀ t, (1 : ℝ) / 2 ≤ (originalRun n (roundRobin n) t).lower .z →
      2 ^ (2 ^ n - 1) ≤ designatedCount (roundRobin n) t) := by
  have hr := originalRun_isRun n (roundRobin n)
  exact ⟨hr, hr.z_tendsto_one (roundRobin_fair n), hr.threshold⟩

end FBBT
