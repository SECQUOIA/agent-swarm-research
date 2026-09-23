import Formal.MultilinearGap.IntegratedLaws

/-! Repair local laws by filling their nonnegative residual marginals with
conditionally independent Bernoulli coordinates. -/
namespace MultilinearGap.StructuralFeedback

open CubicGap
noncomputable section
variable {S I : Type*} [Fintype S] [Fintype I] [DecidableEq I]

def feedbackMass (P : Law (S × (I → Bool))) (s : S) : ℝ :=
  ∑ v, P.weight (s, v)

def pairMass (P : Law (S × (I → Bool))) (i : I) (s : S) (b : Bool) : ℝ :=
  ∑ v, if v i = b then P.weight (s, v) else 0

theorem pairMass_add (P : Law (S × (I → Bool))) (i : I) (s : S) :
    pairMass P i s false + pairMass P i s true = feedbackMass P s := by
  rw [pairMass, pairMass, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro v _
  cases v i <;> simp

theorem feedbackMass_sum (P : Law (S × (I → Bool))) :
    ∑ s, feedbackMass P s = 1 := by
  simpa [feedbackMass, Fintype.sum_prod_type] using P.mass_one

private theorem bernoulli_cell (x : I → ℝ) (hx : x ∈ cube I) (i : I) (b : Bool) :
    (∑ v, if v i = b then (bernoulliLaw x hx).weight v else 0) =
      if b then x i else 1 - x i := by
  have ht : (∑ v, if v i = true then (bernoulliLaw x hx).weight v else 0) = x i := by
    simpa [Law.expect, vertexPoint, mul_ite] using bernoulliLaw_mean x hx i
  cases b
  · have hsum : (∑ v, if v i = false then (bernoulliLaw x hx).weight v else 0) +
        (∑ v, if v i = true then (bernoulliLaw x hx).weight v else 0) = 1 := by
      rw [← Finset.sum_add_distrib]
      convert (bernoulliLaw x hx).mass_one using 1
      apply Finset.sum_congr rfl
      intro v _
      cases v i <;> simp
    simp only [Bool.false_eq_true, ↓reduceIte]
    linarith
  · simpa using ht

/-- Nonnegative binary marginals of common mass have a simultaneous extension,
including zero mass and an empty outside-coordinate set. -/
theorem exists_residual (h : ℝ) (hh : 0 ≤ h) (r : I → Bool → ℝ)
    (hr : ∀ i b, 0 ≤ r i b) (hsum : ∀ i, r i false + r i true = h) :
    ∃ w : (I → Bool) → ℝ, (∀ v, 0 ≤ w v) ∧ (∑ v, w v) = h ∧
      ∀ i b, (∑ v, if v i = b then w v else 0) = r i b := by
  by_cases hz : h = 0
  · refine ⟨fun _ => 0, by simp, by simp [hz], ?_⟩
    intro i b
    have h0 : r i false + r i true = 0 := by simpa [hz] using hsum i
    have hf := hr i false
    have ht := hr i true
    cases b <;> simp only [ite_self, Finset.sum_const_zero] <;> linarith
  · have hp : 0 < h := lt_of_le_of_ne hh (Ne.symm hz)
    let x : I → ℝ := fun i => r i true / h
    have hx : x ∈ cube I := by
      intro i
      exact ⟨div_nonneg (hr i true) hh,
        (div_le_one hp).mpr (by linarith [hsum i, hr i false])⟩
    refine ⟨fun v => h * (bernoulliLaw x hx).weight v,
      fun v => mul_nonneg hh ((bernoulliLaw x hx).nonneg v), ?_, ?_⟩
    · rw [← Finset.mul_sum, (bernoulliLaw x hx).mass_one, mul_one]
    · intro i b
      have heq : (∑ v, if v i = b then h * (bernoulliLaw x hx).weight v else 0) =
          h * (∑ v, if v i = b then (bernoulliLaw x hx).weight v else 0) := by
        rw [Finset.mul_sum]
        apply Finset.sum_congr rfl
        intro v _
        split_ifs <;> simp
      rw [heq, bernoulli_cell]
      cases b
      · simp only [Bool.false_eq_true, ↓reduceIte, x]
        field_simp
        nlinarith [hsum i]
      · simp only [↓reduceIte, x]
        field_simp

/-- Entrywise domination of the desired feedback and pair marginals suffices
for a probability-law repair, without changing any of those marginals. -/
theorem exists_repaired_law (P : Law (S × (I → Bool))) (t : ℝ) (ht : 0 ≤ t)
    (q : S → ℝ) (r : I → S → Bool → ℝ)
    (hq : ∑ s, q s = 1) (hrsum : ∀ i s, r i s false + r i s true = q s)
    (hdomq : ∀ s, t * feedbackMass P s ≤ q s)
    (hdomr : ∀ i s b, t * pairMass P i s b ≤ r i s b) :
    ∃ R : Law (S × (I → Bool)),
      (∀ z, t * P.weight z ≤ R.weight z) ∧
      (∀ s, feedbackMass R s = q s) ∧
      ∀ i s b, pairMass R i s b = r i s b := by
  have hres (s : S) := exists_residual (q s - t * feedbackMass P s)
    (sub_nonneg.mpr (hdomq s))
    (fun i b => r i s b - t * pairMass P i s b)
    (fun i b => sub_nonneg.mpr (hdomr i s b))
    (fun i => by rw [sub_add_sub_comm, ← mul_add, hrsum, pairMass_add])
  choose w hw hmass hpair using hres
  let R : Law (S × (I → Bool)) := {
    weight := fun z => t * P.weight z + w z.1 z.2
    nonneg := fun z => add_nonneg (mul_nonneg ht (P.nonneg z)) (hw z.1 z.2)
    mass_one := by
      rw [Fintype.sum_prod_type]
      have hslice (s : S) : (∑ v, (t * P.weight (s, v) + w s v)) = q s := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, hmass]
        simp [feedbackMass]
      simp_rw [hslice]
      exact hq }
  refine ⟨R, ?_, ?_, ?_⟩
  · intro z
    exact le_add_of_nonneg_right (hw z.1 z.2)
  · intro s
    change (∑ v, (t * P.weight (s, v) + w s v)) = q s
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, hmass]
    simp [feedbackMass]
  · intro i s b
    change (∑ v, if v i = b then t * P.weight (s, v) + w s v else 0) = r i s b
    have heq (v : I → Bool) :
        (if v i = b then t * P.weight (s, v) + w s v else 0) =
          t * (if v i = b then P.weight (s, v) else 0) +
            (if v i = b then w s v else 0) := by
      split_ifs <;> simp
    simp_rw [heq]
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, hpair]
    simp [pairMass]


/-- The repaired law preserves every specified marginal of a target law while
retaining a fixed fraction of each cell of the original law. -/
theorem exists_repaired_law_to_target (P Q : Law (S × (I → Bool)))
    (t : ℝ) (ht : 0 ≤ t)
    (hdomq : ∀ s, t * feedbackMass P s ≤ feedbackMass Q s)
    (hdomr : ∀ i s b, t * pairMass P i s b ≤ pairMass Q i s b) :
    ∃ R : Law (S × (I → Bool)),
      (∀ z, t * P.weight z ≤ R.weight z) ∧
      (∀ s, feedbackMass R s = feedbackMass Q s) ∧
      ∀ i s b, pairMass R i s b = pairMass Q i s b :=
  exists_repaired_law P t ht (feedbackMass Q) (pairMass Q)
    (feedbackMass_sum Q) (pairMass_add Q) hdomq hdomr

/-- Cell domination implies the simultaneous payoff guarantee for every
nonnegative function; no further factor depending on the scope is incurred. -/
theorem expect_ge_of_weight_domination {Ω : Type*} [Fintype Ω]
    (P R : Law Ω) (t : ℝ) (hdom : ∀ z, t * P.weight z ≤ R.weight z)
    (g : Ω → ℝ) (hg : ∀ z, 0 ≤ g z) :
    t * P.expect g ≤ R.expect g := by
  simp only [Law.expect, Finset.mul_sum, ← mul_assoc]
  exact Finset.sum_le_sum fun z _ => mul_le_mul_of_nonneg_right (hdom z) (hg z)

end
end MultilinearGap.StructuralFeedback
