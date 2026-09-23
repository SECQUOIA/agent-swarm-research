import Formal.InfiniteAggregation.GoodSpectral
import Formal.InfiniteAggregation.GoodConvex

open scoped BigOperators Matrix
open QuadraticPrecision
namespace InfiniteAggregation

/-- Coordinates of `(u,v,t)` in the homogeneous matrix. -/
def homogeneousCoordinates {r : ℕ} (z : HomVar r) : HomIndex r → ℝ
  | none => z.2
  | some (.inl i) => z.1.1 i
  | some (.inr i) => z.1.2 i

/-- The matrix used for the spectral condition is exactly the homogeneous
quadratic polynomial of the source system. -/
theorem homogeneousMatrix_eq_homAggregate {r : ℕ} (w : Weight) (z : HomVar r) :
    homogeneousCoordinates z ⬝ᵥ (homogeneousMatrix r w *ᵥ homogeneousCoordinates z) =
      homAggregate w z := by
  rw [homogeneousMatrix_quadratic, homAggregate_formula]
  simp only [homogeneousCoordinates, qnorm, dot, dotProduct, Finset.sum_sub_distrib,
    Finset.sum_add_distrib, ← Finset.mul_sum]
  simp_rw [← sq, mul_assoc (w 2)]
  rw [← Finset.mul_sum]
  ring

/-- BDS goodness uses the actual homogeneous eigenvalue count and validity on
the ordinary convex hull of the strict feasible set. -/
def Good (r : ℕ) (w : Weight) : Prop :=
  NonnegWeight w ∧
    negativeInertia (homogeneousMatrix_hermitian r w) ≤ 1 ∧
    ∀ x ∈ convexHull ℝ (feasible r), aggregate w x < 0

theorem inertia_le_one_of_goodCone {r : ℕ} (w : Weight) (hw : GoodCone w) :
    negativeInertia (homogeneousMatrix_hermitian r w) ≤ 1 := by
  apply negativeInertia_le_one_of_nonneg_on_kernel
    (homogeneousMatrix_hermitian r w) (LinearMap.proj none)
  intro z hz
  change z none = 0 at hz
  rw [homogeneousMatrix_quadratic, hz]
  simp only [zero_pow (by decide : 2 ≠ 0), mul_zero, zero_add]
  exact Finset.sum_nonneg fun i _ =>
    leading_nonneg w hw (z (some (.inl i))) (z (some (.inr i)))

theorem inertia_eq_one_of_goodCone {r : ℕ} (w : Weight) (hw : GoodCone w)
    (hne : w ≠ 0) : negativeInertia (homogeneousMatrix_hermitian r w) = 1 := by
  apply Nat.le_antisymm (inertia_le_one_of_goodCone w hw)
  apply one_le_negativeInertia_of_negative_vector (homogeneousMatrix_hermitian r w)
    (fun i => if i = none then 1 else 0)
  rw [homogeneousMatrix_quadratic]
  simpa using constant_neg_of_goodCone w hw.1 hw.2 hne

/-- For `r≥2`, the source good multipliers are precisely the nonzero vectors
of the explicit second-order cone. -/
theorem good_iff_goodCone {r : ℕ} (hr : 2 ≤ r) (w : Weight) :
    Good r w ↔ GoodCone w ∧ w ≠ 0 := by
  constructor
  · intro h
    exact ⟨⟨h.1.1, discriminant_of_inertia_le_one hr w h.1.1 h.2.1⟩, h.1.2⟩
  · rintro ⟨hw, hne⟩
    exact ⟨⟨hw.1, hne⟩, inertia_le_one_of_goodCone w hw, fun _ hx => goodCone_hull_valid hw hne hx⟩

end InfiniteAggregation
