import Formal.MultilinearGap.Couplings

/-! Universal feedback-variable law with prescribed means and simultaneous
marginal domination. -/
namespace MultilinearGap
open CubicGap MeasureTheory Set
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

def feedbackLiteral (u : ℝ) (b : Bool) : ℝ := if b then u else 1 - u

def feedbackCell (S : Finset I) (s v : Vertex I) : ℝ :=
  ∏ j, if j ∈ S then (if v j = s j then 1 else 0) else 1

def feedbackCellMass (μ : Law (Vertex I)) (S : Finset I) (s : Vertex I) : ℝ :=
  μ.expect (feedbackCell S s)

theorem feedbackCell_eq_indicator (S : Finset I) (s v : Vertex I) :
    feedbackCell S s v = if ∀ j ∈ S, v j = s j then 1 else 0 := by
  classical
  by_cases h : ∀ j ∈ S, v j = s j
  · rw [if_pos h]
    apply Finset.prod_eq_one
    intro j _
    by_cases hj : j ∈ S
    · simp [hj, h j hj]
    · simp [hj]
  · rw [if_neg h]
    push Not at h
    obtain ⟨j, hj, hneq⟩ := h
    exact Finset.prod_eq_zero (Finset.mem_univ j) (by simp [hj, hneq])

theorem feedbackCell_mem (S : Finset I) (s v : Vertex I) :
    feedbackCell S s v ∈ Icc (0 : ℝ) 1 := by
  rw [feedbackCell_eq_indicator]
  split_ifs <;> norm_num

theorem feedbackCellMass_mem (μ : Law (Vertex I)) (S : Finset I) (s : Vertex I) :
    feedbackCellMass μ S s ∈ Icc (0 : ℝ) 1 := by
  refine ⟨μ.expect_nonneg (fun v => (feedbackCell_mem S s v).1), ?_⟩
  exact (μ.expect_mono fun v => (feedbackCell_mem S s v).2).trans_eq (μ.expect_const 1)

theorem feedbackCellMass_le_literal (μ : Law (Vertex I)) (x : I → ℝ)
    (hμ : HasMeans μ x) (S : Finset I) (s : Vertex I) {j : I} (hj : j ∈ S) :
    feedbackCellMass μ S s ≤ feedbackLiteral (x j) (s j) := by
  have h : feedbackCellMass μ S s ≤ μ.expect
      (fun v => feedbackLiteral (vertexPoint v j) (s j)) := by
    apply μ.expect_mono
    intro v
    rw [feedbackCell_eq_indicator]
    by_cases hs : ∀ i ∈ S, v i = s i
    · rw [if_pos hs]
      have hv := hs j hj
      cases hb : s j <;> simp [feedbackLiteral, vertexPoint, hv, hb]
    · rw [if_neg hs]
      cases hb : s j <;> cases hv : v j <;> norm_num [feedbackLiteral, vertexPoint, hb, hv]
  cases hb : s j
  · simpa [feedbackLiteral, hb, Law.expect_sub, hμ j] using h
  · simpa [feedbackLiteral, hb, hμ j] using h

/-- Conditional success probability before folding the common uniform variable. -/
def feedbackUniversalProbability (F : Finset I) (x : I → ℝ) (t : ℝ) (j : I) : ℝ :=
  if j ∈ F then ((if t ≤ x j then 1 else 0) +
    (if 1 - x j < t then 1 else 0)) / 2
  else if t ≤ x j then 1 else 0

omit [Fintype I] in
theorem feedbackUniversalProbability_mem (F : Finset I) (x : I → ℝ) (t : ℝ) :
    feedbackUniversalProbability F x t ∈ cube I := by
  intro j
  unfold feedbackUniversalProbability
  split_ifs <;> norm_num

omit [Fintype I] in
theorem feedbackUniversalProbability_measurable (F : Finset I) (x : I → ℝ) (j : I) :
    Measurable (fun t => feedbackUniversalProbability F x t j) := by
  unfold feedbackUniversalProbability
  split_ifs
  · exact ((Measurable.ite measurableSet_Iic measurable_const measurable_const).add
      (Measurable.ite measurableSet_Ioi measurable_const measurable_const)).div_const 2
  · exact Measurable.ite measurableSet_Iic measurable_const measurable_const

omit [Fintype I] in
theorem feedbackUniversalProbability_integral (F : Finset I) (x : I → ℝ)
    (hx : x ∈ cube I) (j : I) :
    (∫ t in (0 : ℝ)..1, feedbackUniversalProbability F x t j) = x j := by
  have hlo := intervalIntegrable_of_mem_unitInterval
    (fun t => if t ≤ x j then (1 : ℝ) else 0)
    (Measurable.ite measurableSet_Iic measurable_const measurable_const)
    (fun t => by split_ifs <;> norm_num)
  have hhi := intervalIntegrable_of_mem_unitInterval
    (fun t => if 1 - x j < t then (1 : ℝ) else 0)
    (Measurable.ite measurableSet_Ioi measurable_const measurable_const)
    (fun t => by split_ifs <;> norm_num)
  unfold feedbackUniversalProbability
  split_ifs
  · rw [intervalIntegral.integral_div, intervalIntegral.integral_add hlo hhi,
      intervalIntegral_lower_indicator (hx j),
      intervalIntegral_upper_indicator ⟨by linarith [(hx j).2], by linarith [(hx j).1]⟩]
    ring
  · exact intervalIntegral_lower_indicator (hx j)

/-- One common uniform variable, independent fair orientations on F. -/
def feedbackUniversalLaw (F : Finset I) (x : I → ℝ) : Law (Vertex I) :=
  integratedBernoulli (feedbackUniversalProbability F x)
    (feedbackUniversalProbability_mem F x) (feedbackUniversalProbability_measurable F x)

theorem feedbackUniversalLaw_hasMeans (F : Finset I) (x : I → ℝ) (hx : x ∈ cube I) :
    HasMeans (feedbackUniversalLaw F x) x := by
  intro j
  rw [feedbackUniversalLaw, integratedBernoulli_mean,
    feedbackUniversalProbability_integral F x hx j]

theorem bernoulliLaw_feedbackCellMass (p : I → ℝ) (hp : p ∈ cube I)
    (S : Finset I) (s : Vertex I) :
    feedbackCellMass (bernoulliLaw p hp) S s =
      ∏ j, if j ∈ S then feedbackLiteral (p j) (s j) else 1 := by
  unfold feedbackCellMass feedbackCell
  rw [bernoulliLaw_expect_prod p hp
    (fun j b => if j ∈ S then (if b = s j then 1 else 0) else 1)]
  apply Finset.prod_congr rfl
  intro j _
  by_cases hj : j ∈ S <;> cases s j <;> simp [hj, feedbackLiteral]

def feedbackConditionalCell (F S : Finset I) (x : I → ℝ) (s : Vertex I) (t : ℝ) : ℝ :=
  ∏ j, if j ∈ S then feedbackLiteral (feedbackUniversalProbability F x t j) (s j) else 1

theorem feedbackConditionalCell_mem (F S : Finset I) (x : I → ℝ) (s : Vertex I) (t : ℝ) :
    feedbackConditionalCell F S x s t ∈ Icc (0 : ℝ) 1 := by
  have hfactor (j : I) :
      (if j ∈ S then feedbackLiteral (feedbackUniversalProbability F x t j) (s j)
       else 1) ∈ Icc (0 : ℝ) 1 := by
    have hp := feedbackUniversalProbability_mem F x t j
    by_cases hj : j ∈ S <;> cases s j <;> simp [hj, feedbackLiteral] <;>
      constructor <;> linarith [hp.1, hp.2]
  exact ⟨Finset.prod_nonneg fun j _ => (hfactor j).1,
    Finset.prod_le_one (fun j _ => (hfactor j).1) (fun j _ => (hfactor j).2)⟩

theorem feedbackConditionalCell_integrable (F S : Finset I) (x : I → ℝ) (s : Vertex I) :
    IntervalIntegrable (feedbackConditionalCell F S x s) volume 0 1 := by
  apply intervalIntegrable_of_mem_unitInterval _ _ (feedbackConditionalCell_mem F S x s)
  apply Finset.measurable_prod
  intro j _
  by_cases hj : j ∈ S <;> cases s j <;>
    simp only [hj, feedbackLiteral, Bool.false_eq_true, ↓reduceIte]
  · exact measurable_const.sub (feedbackUniversalProbability_measurable F x j)
  · exact feedbackUniversalProbability_measurable F x j
  · exact measurable_const
  · exact measurable_const

theorem feedbackUniversalLaw_cellMass (F S : Finset I) (x : I → ℝ) (s : Vertex I) :
    feedbackCellMass (feedbackUniversalLaw F x) S s =
      ∫ t in (0 : ℝ)..1, feedbackConditionalCell F S x s t := by
  unfold feedbackCellMass feedbackUniversalLaw integratedBernoulli
  rw [integratedLaw_expect]
  apply intervalIntegral.integral_congr
  intro t _
  exact bernoulliLaw_feedbackCellMass _ _ S s

omit [Fintype I] in
/-- On an endpoint interval of length m, every required feedback literal has
conditional probability at least one half; aligned outside literals are certain. -/
theorem feedbackUniversalLiteral_endpoint (F : Finset I) (x : I → ℝ)
    (j : I) (a b : Bool) (m t : ℝ)
    (hm : m ≤ feedbackLiteral (x j) a)
    (hout : j ∉ F → a = b)
    (ht : if b then t ≤ m else 1 - m < t) :
    (if j ∈ F then (1 / 2 : ℝ) else 1) ≤
      feedbackLiteral (feedbackUniversalProbability F x t j) a := by
  by_cases hj : j ∈ F
  · cases ha : a <;> cases hb : b <;>
      simp only [feedbackLiteral, ha, hb, Bool.false_eq_true, ↓reduceIte] at hm ht ⊢ <;>
      simp only [feedbackUniversalProbability, if_pos hj] <;>
      split_ifs <;> norm_num at * <;> linarith
  · have hab := hout hj
    subst a
    cases hb : b <;>
      simp only [feedbackLiteral, hb, Bool.false_eq_true, ↓reduceIte] at hm ht ⊢ <;>
      simp only [feedbackUniversalProbability, if_neg hj] <;>
      split_ifs <;> norm_num at * <;> linarith

/-- A common endpoint interval supplies the entire 2^(-|F|) mass guarantee. -/
theorem feedbackConditionalCell_endpoint (F S : Finset I) (x : I → ℝ)
    (s : Vertex I) (b : Bool) (m t : ℝ)
    (hm : ∀ j ∈ S, m ≤ feedbackLiteral (x j) (s j))
    (hout : ∀ j ∈ S, j ∉ F → s j = b)
    (ht : if b then t ≤ m else 1 - m < t) :
    (1 / 2 : ℝ) ^ F.card ≤ feedbackConditionalCell F S x s t := by
  have heq : (∏ j : I, if j ∈ F then (1 / 2 : ℝ) else 1) = (1 / 2 : ℝ) ^ F.card := by
    simp [Finset.prod_ite_mem]
  rw [← heq]
  apply Finset.prod_le_prod
  · intro j _
    split_ifs <;> norm_num
  · intro j _
    by_cases hj : j ∈ S
    · rw [if_pos hj]
      exact feedbackUniversalLiteral_endpoint F x j (s j) b m t (hm j hj) (hout j hj) ht
    · rw [if_neg hj]
      split_ifs <;> norm_num

/-- Simultaneous marginal domination. Every outside coordinate specified by the
cell must have the same target bit; in particular this applies to F union {i}
for any i outside F, and to F alone. The comparison law is arbitrary. -/
theorem feedbackUniversalLaw_dominates (F S : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hμ : HasMeans μ x) (s : Vertex I) (b : Bool)
    (hout : ∀ j ∈ S, j ∉ F → s j = b) :
    (1 / 2 : ℝ) ^ F.card * feedbackCellMass μ S s ≤
      feedbackCellMass (feedbackUniversalLaw F x) S s := by
  let m := feedbackCellMass μ S s
  let c := (1 / 2 : ℝ) ^ F.card
  have hm : m ∈ Icc (0 : ℝ) 1 := feedbackCellMass_mem μ S s
  have hcoord : ∀ j ∈ S, m ≤ feedbackLiteral (x j) (s j) :=
    fun j hj => feedbackCellMass_le_literal μ x hμ S s hj
  rw [feedbackUniversalLaw_cellMass]
  change c * m ≤ _
  cases hb : b
  · have hint := intervalIntegrable_of_mem_unitInterval
      (fun t => if 1 - m < t then (1 : ℝ) else 0)
      (Measurable.ite measurableSet_Ioi measurable_const measurable_const)
      (fun t => by split_ifs <;> norm_num)
    have hbound : ∀ t, c * (if 1 - m < t then (1 : ℝ) else 0) ≤
        feedbackConditionalCell F S x s t := by
      intro t
      by_cases ht : 1 - m < t
      · rw [if_pos ht, mul_one]
        exact feedbackConditionalCell_endpoint F S x s false m t hcoord
          (by simpa [hb] using hout) ht
      · rw [if_neg ht, mul_zero]
        exact (feedbackConditionalCell_mem F S x s t).1
    have hi := intervalIntegral.integral_mono (by norm_num : (0 : ℝ) ≤ 1)
      (hint.const_mul c) (feedbackConditionalCell_integrable F S x s) hbound
    rw [intervalIntegral.integral_const_mul,
      intervalIntegral_upper_indicator ⟨by linarith [hm.2], by linarith [hm.1]⟩] at hi
    simpa using hi
  · have hint := intervalIntegrable_of_mem_unitInterval
      (fun t => if t ≤ m then (1 : ℝ) else 0)
      (Measurable.ite measurableSet_Iic measurable_const measurable_const)
      (fun t => by split_ifs <;> norm_num)
    have hbound : ∀ t, c * (if t ≤ m then (1 : ℝ) else 0) ≤
        feedbackConditionalCell F S x s t := by
      intro t
      by_cases ht : t ≤ m
      · rw [if_pos ht, mul_one]
        exact feedbackConditionalCell_endpoint F S x s true m t hcoord
          (by simpa [hb] using hout) ht
      · rw [if_neg ht, mul_zero]
        exact (feedbackConditionalCell_mem F S x s t).1
    have hi := intervalIntegral.integral_mono (by norm_num : (0 : ℝ) ≤ 1)
      (hint.const_mul c) (feedbackConditionalCell_integrable F S x s) hbound
    rw [intervalIntegral.integral_const_mul, intervalIntegral_lower_indicator hm] at hi
    exact hi

/-- Equation (2): every marginal on F and one outside variable is dominated. -/
theorem feedbackUniversalLaw_dominates_pair (F : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hμ : HasMeans μ x) (s : Vertex I) (i : I) :
    (1 / 2 : ℝ) ^ F.card * feedbackCellMass μ (insert i F) s ≤
      feedbackCellMass (feedbackUniversalLaw F x) (insert i F) s := by
  apply feedbackUniversalLaw_dominates F (insert i F) x μ hμ s (s i)
  intro j hj hjF
  rcases Finset.mem_insert.mp hj with rfl | hj
  · rfl
  · exact False.elim (hjF hj)

/-- Equation (3), including the empty feedback scope. -/
theorem feedbackUniversalLaw_dominates_feedback (F : Finset I) (x : I → ℝ)
    (μ : Law (Vertex I)) (hμ : HasMeans μ x) (s : Vertex I) :
    (1 / 2 : ℝ) ^ F.card * feedbackCellMass μ F s ≤
      feedbackCellMass (feedbackUniversalLaw F x) F s := by
  apply feedbackUniversalLaw_dominates F F x μ hμ s true
  intro j hj hjF
  exact False.elim (hjF hj)

end
end MultilinearGap
