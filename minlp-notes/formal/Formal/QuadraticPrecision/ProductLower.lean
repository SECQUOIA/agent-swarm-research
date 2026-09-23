import Formal.QuadraticPrecision.Product
import Formal.QuadraticPrecision.LowerPullback

namespace QuadraticPrecision
noncomputable section

def productAntidiagonal : Input 1 →ᵃ[ℝ] Input 2 :=
  AffineMap.pi ![(LinearMap.proj 0).toAffineMap,
    AffineMap.const ℝ (Input 1) 1 - (LinearMap.proj 0).toAffineMap]

def productDiagonal : Input 1 →ᵃ[ℝ] Input 2 :=
  AffineMap.pi (fun _ => (LinearMap.proj 0).toAffineMap)

theorem unitIntervalDomain_convex : Convex ℝ unitIntervalDomain :=
  (convex_Icc (0:ℝ) 1).linear_preimage (LinearMap.proj 0 : Input 1 →ₗ[ℝ] ℝ)

theorem product_epigraph_integer_lower {p : ℕ} {ε : ℝ}
    (h : HasEpigraphLift productDomain productFunction ε p) :
    (1/4:ℝ)^p/4 ≤ ε := by
  apply concaveProduct_epigraph_integer_lower
  have hp := h.pullback productAntidiagonal unitIntervalDomain unitIntervalDomain_convex
    (by
      intro x hx i
      fin_cases i
      · exact hx
      · change 0 ≤ 1-x 0 ∧ 1-x 0 ≤ 1
        constructor <;> linarith [hx.1,hx.2])
  convert hp using 1
  funext x
  simp [productFunction, concaveProductOne, productAntidiagonal]

theorem product_hypograph_integer_lower {p : ℕ} {ε : ℝ}
    (h : HasHypographLift productDomain productFunction ε p) :
    (1/4:ℝ)^p/4 ≤ ε := by
  apply square_hypograph_integer_lower
  have hp := h.pullback productDiagonal unitIntervalDomain unitIntervalDomain_convex
    (by intro x hx i; exact hx)
  convert hp using 1
  funext x
  simp [productFunction, squareOne, productDiagonal, pow_two]

end
end QuadraticPrecision
