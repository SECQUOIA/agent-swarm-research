import CertifiedMinlp.SafeCuts
import Mathlib.Analysis.Convex.Deriv
import Mathlib.Analysis.Calculus.Deriv.AffineMap
import Mathlib.Analysis.Convex.SpecificFunctions.Pow

/-! The analytic premise for rational cuts: derivatives along feasible segments
of a convex function give support inequalities, including at boundary points. -/
namespace CertifiedMinlp

open Set

section Segment
variable {E : Type*} [AddCommGroup E] [Module ℝ E]

/-- A right derivative at the beginning of a segment bounds its secant slope.
The convexity assumption is on the original function and domain. -/
theorem support_of_segment_right_derivative
    {g : E → ℝ} {B : Set E} {z x : E} {d : ℝ}
    (hg : ConvexOn ℝ B g) (hz : z ∈ B) (hx : x ∈ B)
    (hd : HasDerivWithinAt (g ∘ AffineMap.lineMap z x) d (Ioi (0 : ℝ)) 0) :
    g z + d ≤ g x := by
  have hc := hg.comp_affineMap (AffineMap.lineMap z x)
  have h := hc.le_slope_of_hasDerivWithinAt_Ioi
    (by simpa using hz) (by simpa using hx) (by norm_num : (0 : ℝ) < 1) hd
  simpa [slope_def_field, sub_eq_add_neg, add_comm] using h

end Segment

section Differentiable
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- An ambient derivative supplies the segment derivative. Only convexity on
the checked domain and differentiability at the support point are required. -/
theorem support_of_hasFDerivAt
    {g : E → ℝ} {B : Set E} {z x : E} {p : E →L[ℝ] ℝ}
    (hg : ConvexOn ℝ B g) (hz : z ∈ B) (hx : x ∈ B)
    (hp : HasFDerivAt g p z) : g z + p (x - z) ≤ g x := by
  apply support_of_segment_right_derivative hg hz hx
  have hline : HasDerivAt (AffineMap.lineMap z x) (x - z) (0 : ℝ) :=
    AffineMap.hasDerivAt_lineMap
  have hcomp := hp.comp_hasDerivAt_of_eq 0 hline (AffineMap.lineMap_apply_zero z x).symm
  exact hcomp.hasDerivWithinAt

end Differentiable

section Coordinates
variable {ι : Type*} [Fintype ι]

/-- The paper's coordinate form of the segment derivative condition. -/
theorem support_of_feasible_segment_derivatives
    {g : (ι → ℝ) → ℝ} {B : Set (ι → ℝ)} {z p : ι → ℝ}
    (hg : ConvexOn ℝ B g) (hz : z ∈ B)
    (hp : ∀ x ∈ B, HasDerivWithinAt
      (fun θ : ℝ => g (fun j => z j + θ * (x j - z j)))
      (dot p (fun j => x j - z j)) (Ioi (0 : ℝ)) 0) :
    ∀ x ∈ B, g z + dot p (fun j => x j - z j) ≤ g x := by
  intro x hx
  apply support_of_segment_right_derivative hg hz hx
  have heq : g ∘ AffineMap.lineMap z x =
      (fun θ : ℝ => g (fun j => z j + θ * (x j - z j))) := by
    funext θ
    simp only [Function.comp_apply]
    congr 1
    funext j
    simp [AffineMap.lineMap_apply_module', add_comm]
  rw [heq]
  exact hp x hx

end Coordinates

/-- Convexity at an included boundary does not guarantee a finite support slope. -/
theorem neg_sqrt_convex : ConvexOn ℝ (Icc (0 : ℝ) 1) (fun x => -Real.sqrt x) := by
  exact Real.strictConcaveOn_sqrt.concaveOn.neg.subset
    (fun _ hx => hx.1) (convex_Icc _ _)

/-- Every finite candidate slope fails somewhere on the unit interval. -/
theorem neg_sqrt_no_finite_support (p : ℝ) :
    ∃ x ∈ Icc (0 : ℝ) 1, -Real.sqrt x < p * x := by
  let t : ℝ := 1 / (|p| + 1)
  have ha : 0 < |p| + 1 := by positivity
  have ht : 0 < t := one_div_pos.mpr ha
  have hmul : (|p| + 1) * t = 1 := by dsimp [t]; field_simp
  have htle : t ≤ 1 := by
    dsimp [t]
    exact (div_le_one ha).mpr (by linarith [abs_nonneg p])
  have hpt : -1 < p * t := by
    have hp : 0 ≤ (p + |p|) * t := mul_nonneg (by linarith [neg_abs_le p]) ht.le
    nlinarith
  refine ⟨t ^ 2, ⟨sq_nonneg _, by nlinarith⟩, ?_⟩
  rw [Real.sqrt_sq ht.le]
  nlinarith [mul_pos (by linarith : 0 < p * t + 1) ht]

/-- Both coordinate restrictions at the origin are identically zero, so their
finite derivatives do not justify a supporting vector for the two-variable map. -/
theorem neg_sqrt_product_axis_derivatives :
    HasDerivAt (fun t : ℝ => -Real.sqrt (t * 0)) 0 0 ∧
    HasDerivAt (fun t : ℝ => -Real.sqrt (0 * t)) 0 0 := by
  constructor <;> simpa using (hasDerivAt_const (0 : ℝ) (0 : ℝ))

/-- The zero vector supplied by those two axis derivatives fails at (1,1). -/
theorem neg_sqrt_product_zero_not_support :
    ¬ (∀ x y : ℝ, 0 ≤ x → 0 ≤ y → 0 ≤ -Real.sqrt (x * y)) := by
  intro h
  have := h 1 1 (by norm_num) (by norm_num)
  norm_num at this

end CertifiedMinlp
