import Formal.QuadraticAggregation.Dines
import Formal.QuadraticAggregation.ShorModel

/-! # Boundary examples for quadratic aggregation
The unused coordinates remain free, as in the three-dimensional source examples.
-/
open scoped BigOperators Matrix
open Set
noncomputable section
namespace QuadraticAggregation.Boundary

def strip : System 3 2 where
  A := ![Matrix.diagonal ![1, 0, 0], Matrix.diagonal ![-1, 0, 0]]
  symmetric i := by fin_cases i <;> exact Matrix.isSymm_diagonal _
  b := ![0, ![1, 0, 0]]
  c := ![-4, 3]

@[simp] theorem strip_eval_zero (x : Vec 3) : strip.eval x 0 = x 0 ^ 2 - 4 := by
  simp [strip, System.eval, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring
@[simp] theorem strip_eval_one (x : Vec 3) : strip.eval x 1 = -(x 0 ^ 2) + 2 * x 0 + 3 := by
  simp [strip, System.eval, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring

theorem strip_feasible (x : Vec 3) : x ∈ strip.feasible ↔ -2 < x 0 ∧ x 0 < -1 := by
  constructor
  · intro h
    have h0 := h 0
    have h1 := h 1
    simp only [strip_eval_zero, strip_eval_one] at h0 h1
    have hlow : -2 < x 0 := by nlinarith [sq_nonneg (x 0 + 2)]
    have hhigh : x 0 < 2 := by nlinarith [sq_nonneg (x 0 - 2)]
    refine ⟨hlow, ?_⟩
    by_contra! hh
    nlinarith [mul_nonneg (show 0 ≤ x 0 + 1 by linarith) (show 0 ≤ 3 - x 0 by linarith)]
  · rintro ⟨hl, hu⟩ i
    fin_cases i
    · change strip.eval x 0 < 0
      rw [strip_eval_zero]
      nlinarith [mul_pos (show 0 < x 0 + 2 by linarith) (show 0 < 2 - x 0 by linarith)]
    · change strip.eval x 1 < 0
      rw [strip_eval_one]
      nlinarith [mul_pos (show 0 < -(x 0 + 1) by linarith) (show 0 < 3 - x 0 by linarith)]

theorem strip_nonempty : strip.feasible.Nonempty := by
  refine ⟨![-(3/2), 0, 0], (strip_feasible _).2 ?_⟩
  norm_num

theorem strip_zero_not_convexHull : (0 : Vec 3) ∉ convexHull ℝ strip.feasible := by
  have hsub : convexHull ℝ strip.feasible ⊆ {x : Vec 3 | x 0 < -1} := by
    apply convexHull_min
    · intro x hx; exact ((strip_feasible x).1 hx).2
    · exact (convex_Iio (-1 : ℝ)).linear_preimage (LinearMap.proj (0 : Fin 3) : Vec 3 →ₗ[ℝ] ℝ)
  intro h
  have := hsub h
  norm_num at this

theorem strip_agg_q (w : Vec 2) (x : Vec 3) :
    q (strip.aggA w) x = (w 0 - w 1) * x 0 ^ 2 := by
  rw [System.agg_q]
  simp [strip, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring

theorem strip_psd_iff (w : Vec 2) : (strip.aggA w).PosSemidef ↔ w 1 ≤ w 0 := by
  constructor
  · intro h
    have hh := h.dotProduct_mulVec_nonneg ![1,0,0]
    change 0 ≤ q (strip.aggA w) ![1,0,0] at hh
    rw [strip_agg_q] at hh
    norm_num at hh
    linarith
  · intro h
    apply Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
    · exact Matrix.isHermitian_iff_isSymm.mpr (strip.aggA_isSymm w)
    · intro x
      change 0 ≤ q (strip.aggA w) x
      rw [strip_agg_q]
      exact mul_nonneg (sub_nonneg.mpr h) (sq_nonneg _)

theorem strip_convex_aggregation_admits_zero (w : Vec 2)
    (hw : ∀ i, 0 ≤ w i) (hw0 : w ≠ 0) (hpsd : (strip.aggA w).PosSemidef) :
    (∑ i, w i * strip.eval 0 i) < 0 := by
  have hle := (strip_psd_iff w).1 hpsd
  have hpos : 0 < w 0 := by
    by_contra! h
    apply hw0
    ext i
    fin_cases i <;> simp only [Pi.zero_apply]
    · exact le_antisymm h (hw 0)
    · exact le_antisymm (hle.trans h) (hw 1)
  simp only [Fin.sum_univ_two, strip_eval_zero, strip_eval_one, Pi.zero_apply]
  nlinarith

/-- Opposite first two inequalities force an empty strict system. -/
def hyperbola : System 3 3 where
  A := ![!![0, 1/2, 0; 1/2, 0, 0; 0, 0, 0],
         !![0, -(1/2), 0; -(1/2), 0, 0; 0, 0, 0], Matrix.diagonal ![1,-1,0]]
  symmetric i := by
    fin_cases i
    · ext a b; fin_cases a <;> fin_cases b <;> rfl
    · ext a b; fin_cases a <;> fin_cases b <;> rfl
    · exact Matrix.isSymm_diagonal _
  b := 0
  c := ![-1, 1, 0]

@[simp] theorem hyperbola_eval_zero (x : Vec 3) : hyperbola.eval x 0 = x 0 * x 1 - 1 := by
  simp [hyperbola, System.eval, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring
@[simp] theorem hyperbola_eval_one (x : Vec 3) : hyperbola.eval x 1 = -(x 0 * x 1) + 1 := by
  simp [hyperbola, System.eval, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring
@[simp] theorem hyperbola_eval_two (x : Vec 3) : hyperbola.eval x 2 = x 0 ^ 2 - x 1 ^ 2 := by
  simp [hyperbola, System.eval, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring

theorem hyperbola_strict_empty : hyperbola.feasible = ∅ := by
  apply Set.eq_empty_iff_forall_notMem.mpr
  intro x hx
  have h0 := hx 0
  have h1 := hx 1
  simp only [hyperbola_eval_zero, hyperbola_eval_one] at h0 h1
  linarith

theorem hyperbola_closed (x : Vec 3) :
    x ∈ hyperbola.closedFeasible ↔ x 0 * x 1 = 1 ∧ x 0 ^ 2 ≤ x 1 ^ 2 := by
  constructor
  · intro h
    have h0 := h 0
    have h1 := h 1
    have h2 := h 2
    simp only [hyperbola_eval_zero, hyperbola_eval_one, hyperbola_eval_two] at h0 h1 h2
    constructor <;> linarith
  · rintro ⟨h0, h1⟩ i
    fin_cases i
    · change hyperbola.eval x 0 ≤ 0
      rw [hyperbola_eval_zero]; linarith
    · change hyperbola.eval x 1 ≤ 0
      rw [hyperbola_eval_one]; linarith
    · change hyperbola.eval x 2 ≤ 0
      rw [hyperbola_eval_two]; linarith

theorem hyperbola_closed_nonempty : hyperbola.closedFeasible.Nonempty := by
  refine ⟨![1,1,0], (hyperbola_closed _).2 ?_⟩
  norm_num

theorem hyperbola_closed_bound {x : Vec 3} (hx : x ∈ hyperbola.closedFeasible) :
    -1 ≤ x 0 ∧ x 0 ≤ 1 := by
  obtain ⟨hxy, hsq⟩ := (hyperbola_closed x).1 hx
  have hprod : x 0 ^ 2 * x 1 ^ 2 = 1 := by nlinarith [sq_nonneg (x 0 * x 1 - 1)]
  have hfour : (x 0 ^ 2) ^ 2 ≤ 1 := by
    have := mul_le_mul_of_nonneg_left hsq (sq_nonneg (x 0))
    nlinarith
  constructor <;> nlinarith [sq_nonneg (x 0 - 1), sq_nonneg (x 0 + 1)]

theorem hyperbola_closed_hull_proper : convexHull ℝ hyperbola.closedFeasible ≠ Set.univ := by
  have hsub : convexHull ℝ hyperbola.closedFeasible ⊆ {x : Vec 3 | x 0 ≤ 1} := by
    apply convexHull_min
    · intro x hx; exact (hyperbola_closed_bound hx).2
    · exact (convex_Iic (1 : ℝ)).linear_preimage (LinearMap.proj (0 : Fin 3) : Vec 3 →ₗ[ℝ] ℝ)
  intro h
  have hh := hsub (a := ![2,0,0]) (by rw [h]; trivial)
  norm_num at hh

theorem hyperbola_agg_q (w : Vec 3) (x : Vec 3) :
    q (hyperbola.aggA w) x = (w 0 - w 1) * x 0 * x 1 + w 2 * (x 0 ^ 2 - x 1 ^ 2) := by
  rw [System.agg_q]
  simp [hyperbola, q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
  ring

theorem hyperbola_psd_trivial (w : Vec 3) (h : (hyperbola.aggA w).PosSemidef) :
    hyperbola.aggA w = 0 ∧ hyperbola.aggB w = 0 := by
  have hq (x : Vec 3) : 0 ≤ (w 0 - w 1) * x 0 * x 1 + w 2 * (x 0 ^ 2 - x 1 ^ 2) := by
    rw [← hyperbola_agg_q]
    exact h.dotProduct_mulVec_nonneg x
  have h0 := hq ![1,0,0]
  have h1 := hq ![0,1,0]
  have h2 := hq ![1,1,0]
  have h3 := hq ![1,-1,0]
  norm_num at h0 h1 h2 h3
  have hw2 : w 2 = 0 := by linarith
  have hw01 : w 0 = w 1 := by linarith
  constructor
  · ext i j
    fin_cases i <;> fin_cases j <;>
      simp [System.aggA, hyperbola, Fin.sum_univ_succ, hw2, hw01]
  · simp [System.aggB, hyperbola]

theorem hyperbola_no_certificate (w : Vec 3) : ¬ hyperbola.Certificate w := by
  rintro ⟨_, _, hp, hnon⟩
  obtain ⟨hA, hB⟩ := hyperbola_psd_trivial w hp
  exact hnon.elim (fun h => h hA) (fun h => h hB)

theorem strip_hhc : strip.HHC := strip.hhc_pair

/-- The independent forms of the hyperbola system. -/
def hyperbolaPair : System 3 2 where
  A := ![hyperbola.A 0, hyperbola.A 2]
  symmetric i := by fin_cases i <;> apply hyperbola.symmetric
  b := ![hyperbola.b 0, hyperbola.b 2]
  c := ![hyperbola.c 0, hyperbola.c 2]

/-- Reinsert the negative of the first form. -/
def duplicateNegative : Vec 2 →ₗ[ℝ] Vec 3 where
  toFun y := ![y 0, -y 0, y 1]
  map_add' x y := by ext i; fin_cases i <;> simp [add_comm]
  map_smul' r x := by ext i; fin_cases i <;> simp

theorem hyperbola_hom_factor (z : Vec 3 × ℝ) :
    hyperbola.homEval z = duplicateNegative (hyperbolaPair.homEval z) := by
  ext i
  fin_cases i
  · rfl
  · simp [System.homEval, hyperbolaPair, duplicateNegative, hyperbola,
      q, dotProduct, Matrix.mulVec, Fin.sum_univ_succ]
    ring
  · rfl

theorem hyperbola_hhc : hyperbola.HHC := by
  intro l hl
  have h := (hyperbolaPair.hhc_pair l hl).linear_image duplicateNegative
  rw [Set.image_image] at h
  have heq : hyperbola.homEval = duplicateNegative ∘ hyperbolaPair.homEval :=
    funext hyperbola_hom_factor
  rw [heq]
  exact h

/-- The exact covariance slack used in the source counterexample. -/
def stripSlack : Mat 3 := Matrix.diagonal ![7/2, 0, 0]

theorem stripSlack_psd : stripSlack.PosSemidef := by
  apply Matrix.PosSemidef.diagonal
  intro i
  fin_cases i <;> norm_num [stripSlack]

theorem strip_shor_residual (i : Fin 2) :
    strip.eval 0 i + tracePair (strip.A i) stripSlack = -(1/2) := by
  fin_cases i <;>
    norm_num [strip, System.eval, q, tracePair, stripSlack, Matrix.trace,
      Matrix.diag, Matrix.diagonal, Matrix.mul_apply, dotProduct, Matrix.mulVec,
      Fin.sum_univ_three, Matrix.cons_val_two,
      Matrix.vecHead, Matrix.vecTail]

theorem strip_zero_mem_shor : (0 : Vec 3) ∈ strip.shorProjection := by
  refine ⟨stripSlack, stripSlack_psd, ?_⟩
  intro i
  rw [strip_shor_residual]
  norm_num

theorem strip_shor_strictly_larger : convexHull ℝ strip.feasible ⊂ strip.shorProjection := by
  refine Set.ssubset_iff_subset_ne.mpr ⟨?_, ?_⟩
  · exact convexHull_min strip.feasible_subset_shorProjection strip.convex_shorProjection
  · intro h
    exact strip_zero_not_convexHull (h.symm ▸ strip_zero_mem_shor)

theorem hyperbola_closed_hull_bound :
    convexHull ℝ hyperbola.closedFeasible ⊆ {x : Vec 3 | |x 0| ≤ 1} := by
  apply convexHull_min
  · intro x hx
    exact abs_le.mpr (hyperbola_closed_bound hx)
  · have heq : {x : Vec 3 | |x 0| ≤ 1} =
        (LinearMap.proj (0 : Fin 3) : Vec 3 →ₗ[ℝ] ℝ) ⁻¹' Set.Icc (-1) 1 := by
      ext x
      change |x 0| ≤ (1 : ℝ) ↔ -1 ≤ x 0 ∧ x 0 ≤ 1
      exact abs_le
    rw [heq]
    exact (convex_Icc (-1 : ℝ) 1).linear_preimage _

/-- Strict feasibility cannot be removed from the closed-system equivalence. -/
theorem hyperbola_closed_equivalence_fails :
    ¬ (convexHull ℝ hyperbola.closedFeasible ≠ Set.univ ↔
      ∃ w, hyperbola.Certificate w) := by
  intro h
  obtain ⟨w, hw⟩ := h.mp hyperbola_closed_hull_proper
  exact hyperbola_no_certificate w hw

theorem strip_convex : Convex ℝ strip.feasible := by
  have heq : strip.feasible =
      (LinearMap.proj (0 : Fin 3) : Vec 3 →ₗ[ℝ] ℝ) ⁻¹' Set.Ioo (-2) (-1) := by
    ext x
    exact strip_feasible x
  rw [heq]
  exact (convex_Ioo (-2 : ℝ) (-1)).linear_preimage _

theorem strip_hull_eq : convexHull ℝ strip.feasible = strip.feasible :=
  strip_convex.convexHull_eq

theorem strip_hull_proper : convexHull ℝ strip.feasible ≠ Set.univ := by
  intro h
  exact strip_zero_not_convexHull (h.symm ▸ Set.mem_univ 0)

/-- Intersection of the strict, globally convex, nonzero nonnegative aggregations. -/
def stripConvexAggregations : Set (Vec 3) := {x | ∀ w : Vec 2,
  (∀ i, 0 ≤ w i) → w ≠ 0 → (strip.aggA w).PosSemidef →
    (∑ i, w i * strip.eval x i) < 0}

theorem strip_zero_mem_convexAggregations : (0 : Vec 3) ∈ stripConvexAggregations :=
  strip_convex_aggregation_admits_zero

theorem strip_convexAggregations_ne_hull :
    stripConvexAggregations ≠ convexHull ℝ strip.feasible := by
  intro h
  exact strip_zero_not_convexHull (h ▸ strip_zero_mem_convexAggregations)

theorem strip_shor_block_witness : (shorBlock (0 : Vec 3) stripSlack).PosSemidef := by
  apply (shorBlock_posSemidef_iff _ _).mpr
  have hz : outer (0 : Vec 3) = 0 := by ext i j; simp [outer]
  rw [hz, sub_zero]
  exact stripSlack_psd

theorem strip_shor_proper : strip.shorProjection ≠ Set.univ := by
  intro h
  have hx : (![3,0,0] : Vec 3) ∈ strip.shorProjection := h.symm ▸ Set.mem_univ _
  obtain ⟨Y, hY, hc⟩ := hx
  have hA : (strip.A 0).PosSemidef := by
    apply Matrix.PosSemidef.diagonal
    intro i
    fin_cases i <;> norm_num [strip]
  have ht := tracePair_nonneg hA hY
  have hh := hc 0
  rw [strip_eval_zero] at hh
  norm_num at hh
  linarith

end QuadraticAggregation.Boundary
