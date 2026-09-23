import Formal.ReciprocalAnchor.Model
import Formal.ReciprocalAnchor.Separator

namespace ReciprocalAnchor

noncomputable section

abbrev JointPoint := Fin 6 → ℝ

def jointPoint (m t q₁ w₁ q₂ w₂ : ℝ) : JointPoint := ![m, t, q₁, w₁, q₂, w₂]

def jointGraph (a b : ℝ) : Set JointPoint :=
  {p | ∃ x y z : ℝ, a ≤ x ∧ x ≤ b ∧ 0 ≤ y ∧ y ≤ 1 ∧ 0 ≤ z ∧ z ≤ 1 ∧
    p = jointPoint x (1/x) y (x*y) z (x*z)}

def jointHull (a b : ℝ) : Set JointPoint := convexHull ℝ (jointGraph a b)

def jointCut (p : JointPoint) : ℝ := 2 * p 1 - g₁ (p 0) (p 2) (p 3) - g₂ (p 0) (p 4) (p 5)

theorem jointCut_affine (x y : JointPoint) (a b : ℝ) (hab : a + b = 1) :
    jointCut (a • x + b • y) = a * jointCut x + b * jointCut y := by
  simp only [jointCut, g₁, g₂, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
  nlinarith only [hab]

theorem joint_cut_valid {a b : ℝ} (ha : 0 < a) {p : JointPoint}
    (hp : p ∈ jointHull a b) : (1/400 : ℝ) ≤ jointCut p := by
  apply (convexHull_min (t := {p : JointPoint | (1/400 : ℝ) ≤ jointCut p}) ?_ ?_) hp
  · rintro p ⟨x, y, z, hx, _, hy0, hy1, hz0, hz1, rfl⟩
    have h := joint_cut_pointwise (ha.trans_le hx) hy0 hy1 hz0 hz1
    change (1/400 : ℝ) ≤ jointCut (jointPoint x (1/x) y (x*y) z (x*z))
    change (1/400 : ℝ) ≤ 2 * (1/x) - g₁ x y (x*y) - g₂ x z (x*z)
    have he : (2 : ℝ) / x = 2 * (1/x) := by ring
    rw [he] at h
    linarith
  · intro x hx y hy r s hr hs hrs
    change (1/400 : ℝ) ≤ jointCut (r • x + s • y)
    rw [jointCut_affine x y r s hrs]
    have h := add_le_add (mul_le_mul_of_nonneg_left hx hr) (mul_le_mul_of_nonneg_left hy hs)
    nlinarith only [h, hrs]

theorem first_leaf_in_hull : point 2 (3/5) (2/3) (5/3) ∈ hull 1 3 := by
  have h₁ : point 1 1 0 0 ∈ graph 1 3 := by
    refine ⟨1, 0, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [point]
  have h₂ : point (5/2) (2/5) 1 (5/2) ∈ graph 1 3 := by
    refine ⟨5/2, 1, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [point]
  have h := (convex_convexHull ℝ (graph 1 3)) (subset_convexHull ℝ _ h₁)
    (subset_convexHull ℝ _ h₂) (by norm_num : (0 : ℝ) ≤ 1/3)
    (by norm_num : (0 : ℝ) ≤ 2/3) (by norm_num : (1/3 : ℝ) + 2/3 = 1)
  change _ ∈ convexHull ℝ (graph 1 3)
  convert h using 1
  ext i
  fin_cases i <;> norm_num [point]

theorem second_leaf_in_hull : point 2 (3/5) (14/29) (40/29) ∈ hull 1 3 := by
  have h₁ : point (6/5) (5/6) 0 0 ∈ graph 1 3 := by
    refine ⟨6/5, 0, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [point]
  have h₂ : point (20/7) (7/20) 1 (20/7) ∈ graph 1 3 := by
    refine ⟨20/7, 1, ?_, ?_, ?_, ?_, ?_⟩ <;> norm_num [point]
  have h := (convex_convexHull ℝ (graph 1 3)) (subset_convexHull ℝ _ h₁)
    (subset_convexHull ℝ _ h₂) (by norm_num : (0 : ℝ) ≤ 15/29)
    (by norm_num : (0 : ℝ) ≤ 14/29) (by norm_num : (15/29 : ℝ) + 14/29 = 1)
  change _ ∈ convexHull ℝ (graph 1 3)
  convert h using 1
  ext i
  fin_cases i <;> norm_num [point]

theorem incompatible_point_not_joint :
    jointPoint 2 (3/5) (2/3) (5/3) (14/29) (40/29) ∉ jointHull 1 3 := by
  intro h
  have hc := joint_cut_valid (by norm_num : (0 : ℝ) < 1) h
  change (1/400 : ℝ) ≤ 2 * (3/5) - g₁ 2 (2/3) (5/3) - g₂ 2 (14/29) (40/29) at hc
  norm_num [g₁, g₂] at hc

/-- Intersecting the exact individual hulls misses a coupling requirement. -/
theorem individual_hulls_not_joint :
    point 2 (3/5) (2/3) (5/3) ∈ hull 1 3 ∧
    point 2 (3/5) (14/29) (40/29) ∈ hull 1 3 ∧
    jointPoint 2 (3/5) (2/3) (5/3) (14/29) (40/29) ∉ jointHull 1 3 :=
  ⟨first_leaf_in_hull, second_leaf_in_hull, incompatible_point_not_joint⟩

end
end ReciprocalAnchor
