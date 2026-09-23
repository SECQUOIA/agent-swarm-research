import Formal.QuadraticPrecision.ProductLower
import Formal.QuadraticPrecision.SquareLift

/-! Exact unrestricted-integer one-sided precision count for the unit-square product. -/
namespace QuadraticPrecision
noncomputable section

theorem product_epigraph_integer_upper (p : ℕ) :
    HasEpigraphLift productDomain productFunction ((1/4:ℝ)^p/4) p := by
  apply product_epigraph_of_square_hypograph
  have h := (square_hasBinaryHypographLift p).toInteger
  have he : (squareWidth p)^2/4 = (1/4:ℝ)^p/4 := by
    unfold squareWidth
    rw [← pow_mul, mul_comm p 2, pow_mul]
    norm_num
  change HasHypographLift {x : Input 1 | x 0 ∈ Set.Icc 0 1}
    (fun x => (x 0)^2) ((1/4:ℝ)^p/4) p
  rwa [he] at h

theorem product_hypograph_integer_upper (p : ℕ) :
    HasHypographLift productDomain productFunction ((1/4:ℝ)^p/4) p :=
  product_hypograph_of_epigraph (product_epigraph_integer_upper p)

/-- Equality thresholds are feasible; the error is not merely an unattained infimum. -/
theorem product_epigraph_lift_iff {p : ℕ} {ε : ℝ} :
    HasEpigraphLift productDomain productFunction ε p ↔ (1/4:ℝ)^p/4 ≤ ε := by
  constructor
  · exact product_epigraph_integer_lower
  · intro he
    obtain ⟨q,L,hcontains,hsound⟩ := product_epigraph_integer_upper p
    refine ⟨q,L,hcontains, ?_⟩
    intro v hv
    exact ⟨(hsound v hv).1, by linarith [(hsound v hv).2]⟩

theorem product_hypograph_lift_iff {p : ℕ} {ε : ℝ} :
    HasHypographLift productDomain productFunction ε p ↔ (1/4:ℝ)^p/4 ≤ ε := by
  constructor
  · exact product_hypograph_integer_lower
  · intro he
    obtain ⟨q,L,hcontains,hsound⟩ := product_hypograph_integer_upper p
    refine ⟨q,L,hcontains, ?_⟩
    intro v hv
    exact ⟨(hsound v hv).1, by linarith [(hsound v hv).2]⟩

theorem product_epigraph_count_iff {p : ℕ} {ε : ℝ} (hε : 0 < ε) :
    HasEpigraphLift productDomain productFunction ε p ↔ squarePrecisionCount ε ≤ p := by
  rw [product_epigraph_lift_iff, squarePrecisionCount_le_iff hε]

theorem product_hypograph_count_iff {p : ℕ} {ε : ℝ} (hε : 0 < ε) :
    HasHypographLift productDomain productFunction ε p ↔ squarePrecisionCount ε ≤ p := by
  rw [product_hypograph_lift_iff, squarePrecisionCount_le_iff hε]

theorem product_one_sided_minimum {ε : ℝ} (hε : 0 < ε) :
    HasEpigraphLift productDomain productFunction ε (squarePrecisionCount ε) ∧
    HasHypographLift productDomain productFunction ε (squarePrecisionCount ε) ∧
    (∀ p, HasEpigraphLift productDomain productFunction ε p → squarePrecisionCount ε ≤ p) ∧
    (∀ p, HasHypographLift productDomain productFunction ε p → squarePrecisionCount ε ≤ p) :=
  ⟨(product_epigraph_count_iff hε).mpr le_rfl,
    (product_hypograph_count_iff hε).mpr le_rfl,
    fun _ h => (product_epigraph_count_iff hε).mp h,
    fun _ h => (product_hypograph_count_iff hε).mp h⟩

/-- The concrete product epigraph lift used for the exact upper bound. -/
def productExactEpigraphLift (p : ℕ) :=
  productUpperLift (squareBinaryLift p true).toIntegerLift

/-- Its worst permitted error occurs at a residual midpoint on the antidiagonal. -/
theorem productExactEpigraphLift_attains (p : ℕ) :
    (![squareWidth p/2, 1-squareWidth p/2],
      (squareWidth p/2)*(1-squareWidth p/2)-(squareWidth p)^2/4) ∈
      (productExactEpigraphLift p).relaxation := by
  apply productUpperLift_attains
  · constructor
    · exact div_nonneg (squareWidth_pos p).le (by norm_num)
    · linarith [squareWidth_le_one p]
  · rw [← BinaryLinearLift.relaxation_eq_integer]
    have he : (squareWidth p/2)^2+(squareWidth p)^2/4 = (squareWidth p)^2/2 := by ring
    rw [he]
    apply (squareLift_relaxation p true _ _).mpr
    obtain ⟨b,v,t,r,q,hb,hy,hr,he,hv,ht,hq,hw⟩ := (squareRelaxation_attains p).1
    exact ⟨b,v,t,r,q,hb,hy,hr,he,hv,ht,hq.2.2,hw⟩

end
end QuadraticPrecision
