import Formal.MultilinearGap.StructuralFeedbackBoxes
import Formal.MultilinearGap.StructuralFeedbackUniversal
import Formal.MultilinearGap.StructuralFeedbackRepair
import Formal.MultilinearGap.StructuralFeedbackLocal
import Formal.MultilinearGap.StructuralFeedbackForest
import Formal.MultilinearGap.StructuralFeedbackOrder

/-! Distributional interfaces and assembly of the feedback-variable argument. -/
namespace MultilinearGap
open CubicGap
noncomputable section
variable {I : Type*} [Fintype I] [DecidableEq I]

namespace ScopeGluing

/-- Equality of actual marginal masses implies equality of every local payoff. -/
theorem agreesOn_of_marginal_eq (μ ν : Law (Vertex I)) (s : Finset I)
    (h : ∀ z, SeparatorGluing.marginal μ (restrict s) z =
      SeparatorGluing.marginal ν (restrict s) z) : AgreesOn μ ν s := by
  classical
  intro φ hφ
  let extend : Vertex s → Vertex I := fun z i => if hi : i ∈ s then z ⟨i, hi⟩ else false
  have he (v : Vertex I) : φ (extend (restrict s v)) = φ v := by
    apply hφ
    intro i hi
    change i ∈ s at hi
    simp [extend, restrict, hi]
  have hex : (μ.map (restrict s)).expect (fun z => φ (extend z)) =
      (ν.map (restrict s)).expect (fun z => φ (extend z)) := by
    unfold Law.expect
    exact Finset.sum_congr rfl fun z _ => congrArg (· * φ (extend z)) (h z)
  simpa only [Law.expect_map, Function.comp_def, he] using hex

/-- Cell equality on a scope is the full marginal equality used in gluing. -/
theorem agreesOn_of_feedbackCellMass_eq (μ ν : Law (Vertex I)) (s : Finset I)
    (h : ∀ z : Vertex I, feedbackCellMass μ s z = feedbackCellMass ν s z) :
    AgreesOn μ ν s := by
  classical
  apply agreesOn_of_marginal_eq
  intro z
  let extend : Vertex I := fun i => if hi : i ∈ s then z ⟨i, hi⟩ else false
  have he (v : Vertex I) : restrict s v = z ↔ ∀ i ∈ s, v i = extend i := by
    constructor
    · intro hv i hi
      simpa [restrict, extend, hi] using congrFun hv ⟨i, hi⟩
    · intro hv
      funext i
      simpa [restrict, extend, i.property] using hv i i.property
  have hh := h extend
  simp only [feedbackCellMass, Law.expect, feedbackCell_eq_indicator,
    mul_ite, mul_one, mul_zero] at hh
  simpa only [SeparatorGluing.marginal, Law.map, he] using hh

end ScopeGluing

/-- A feedback scope plus a forest elimination order gives one feasible law
simultaneously retaining a 2^(-|F|) fraction of every local nonnegative payoff. -/
theorem feedback_payoff_coupling_of_order {E : Type*}
    (F : Finset I) (scope : E → Finset I) (es : List E)
    (order : ForestGluing.EliminationOrder (fun e => scope e \ F) es)
    (x : I → ℝ) (hx : x ∈ cube I) (P : E → Law (Vertex I))
    (hP : ∀ e, HasMeans (P e) x) :
    ∃ μ : Law (Vertex I), HasMeans μ x ∧
      ∀ e ∈ es, ∀ g : Vertex I → ℝ, DependsOn g (scope e : Set I) →
        (∀ v, 0 ≤ g v) → (1 / 2 : ℝ) ^ F.card * (P e).expect g ≤ μ.expect g := by
  choose R hdom hF hpair using fun e =>
    StructuralFeedback.exists_local_repair F x (P e) (hP e)
  have hagreeF (e : E) : ScopeGluing.AgreesOn (R e) (feedbackUniversalLaw F x) F :=
    ScopeGluing.agreesOn_of_feedbackCellMass_eq _ _ _ (hF e)
  have hagreePair (e : E) (i : I) :
      ScopeGluing.AgreesOn (R e) (feedbackUniversalLaw F x) (insert i F) :=
    ScopeGluing.agreesOn_of_feedbackCellMass_eq _ _ _ (hpair e i)
  obtain ⟨μ, _, hm, hlocal⟩ := ForestGluing.exists_global_feedback
    (fun e => scope e \ F) R (feedbackUniversalLaw F x) F hagreeF hagreePair es order
  refine ⟨μ, ?_, ?_⟩
  · intro i
    trans (feedbackUniversalLaw F x).expect (fun v => vertexPoint v i)
    · apply hm i
      intro v w hvw
      change (if v i then (1 : ℝ) else 0) = if w i then 1 else 0
      rw [hvw i (Finset.mem_insert_self _ _)]
    · exact feedbackUniversalLaw_hasMeans F x hx i
  · intro e he g hg hnonneg
    have hdep : DependsOn g ((F ∪ (scope e \ F) : Finset I) : Set I) := by
      apply hg.mono
      intro i hi
      by_cases hiF : i ∈ F
      · exact Finset.mem_union_left _ hiF
      · exact Finset.mem_union_right _ (Finset.mem_sdiff.mpr ⟨hi, hiF⟩)
    rw [hlocal e he g hdep]
    exact StructuralFeedback.expect_ge_of_weight_domination (P e) (R e) _ (hdom e) g hnonneg

omit [Fintype I] in
/-- The feedback gap bound for a concrete forest elimination order, on an
arbitrary nonnegative box and for the original monomial terms. -/
theorem feedback_box_gap_of_order [Finite I] (F : Finset I) (S : Finset (Finset I))
    (es : List (Finset I)) (hmem : ∀ s, s ∈ S → s ∈ es)
    (order : ForestGluing.EliminationOrder (fun s => s \ F) es)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (z : I → ℝ) (hz : z ∈ coordinateBox l u) :
    boxTermwiseGap S a l u z ≤
      (2 : ℝ) ^ F.card * boxHullGap l u (supportPolynomial S a) z := by
  let _ := Fintype.ofFinite I
  obtain ⟨x, hx, rfl⟩ := exists_boxPoint l u hlu z hz
  choose P hP hgap using fun s => feedbackBoxDeficiency_attains_gap l u hl hlu s x hx
  obtain ⟨μ, hm, hpayoff⟩ := feedback_payoff_coupling_of_order F (fun s => s) es order x hx P hP
  have hdef (s : Finset I) (hs : s ∈ S) :
      (1 / 2 : ℝ) ^ F.card * boxHullGap l u (monomial s) (boxPoint l u x) ≤
        μ.expect (fun v => feedbackBoxDeficiency l u s x (vertexPoint v)) := by
    rw [← hgap s]
    apply hpayoff s (hmem s hs)
    · intro v w hvw
      apply feedbackBoxDeficiency_congr
      intro i hi
      unfold vertexPoint
      rw [hvw i hi]
    · intro v
      apply feedbackBoxDeficiency_nonneg l u hl hlu s x _
      intro i
      simp only [vertexPoint]
      split <;> norm_num
  have hb := feedbackBox_gap_of_local_deficiencies l u hl hlu S a ha x hx
    ((1 / 2 : ℝ) ^ F.card) (pow_pos (by norm_num) _) μ hm hdef
  simpa only [one_div, inv_pow, inv_inv] using hb


/-- The original incidence graph with feedback-variable edges deleted. Deleted
variables remain as isolated vertices, which cannot affect acyclicity. -/
def feedbackIncidence (F : Finset I) (S : Finset (Finset I)) :
    SimpleGraph (I ⊕ Finset I) :=
  ForestGluing.activeIncidence (fun s => s \ F) S

omit [Fintype I] in
/-- The feedback-variable theorem on every finite nonnegative box. The only
structural hypothesis is acyclicity of the actual residual incidence graph. -/
theorem feedback_variable_gap_bound [Finite I] (F : Finset I) (S : Finset (Finset I))
    (hforest : (feedbackIncidence F S).IsAcyclic)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (z : I → ℝ) (hz : z ∈ coordinateBox l u) :
    boxTermwiseGap S a l u z ≤
      (2 : ℝ) ^ F.card * boxHullGap l u (supportPolynomial S a) z := by
  obtain ⟨es, hes, _, ho⟩ := ForestGluing.exists_eliminationOrder_active
    (fun s => s \ F) S hforest
  exact feedback_box_gap_of_order F S es
    (fun s hs => List.mem_toFinset.mp (hes.symm ▸ hs)) ho a ha l u hl hlu z hz

omit [Fintype I] [DecidableEq I] in
/-- Berge-acyclicity gives exact termwise gaps, including zero-gap points,
fixed coordinates, empty factors, and disconnected incidence forests. -/
theorem incidence_forest_gap_exact [Finite I] (S : Finset (Finset I))
    (hforest : (ForestGluing.activeIncidence (fun s => s) S).IsAcyclic)
    (a : Finset I → ℝ) (ha : ∀ s ∈ S, 0 ≤ a s)
    (l u : I → ℝ) (hl : ∀ i, 0 ≤ l i) (hlu : ∀ i, l i ≤ u i)
    (z : I → ℝ) (hz : z ∈ coordinateBox l u) :
    boxTermwiseGap S a l u z = boxHullGap l u (supportPolynomial S a) z := by
  classical
  apply le_antisymm
  · have hf : (feedbackIncidence (∅ : Finset I) S).IsAcyclic := by
      simpa only [feedbackIncidence, Finset.sdiff_empty] using hforest
    simpa using feedback_variable_gap_bound ∅ S hf a ha l u hl hlu z hz
  · exact (box_gap_comparison S a ha l u z hlu hz).2

end
end MultilinearGap
