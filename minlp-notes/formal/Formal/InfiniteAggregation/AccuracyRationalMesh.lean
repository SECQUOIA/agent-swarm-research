import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Analysis.Calculus.MeanValue
import Mathlib.Algebra.Order.Round
import Mathlib.Tactic

/-! Rational slopes give a finite angular net on the positive quadrant. -/

noncomputable section

namespace InfiniteAggregation

open Set Real

/-- The angles of the two integer coefficient families, including both axes. -/
def rationalAngleMesh (m : ℕ) : Set ℝ :=
  {θ | ∃ j : ℕ, j ≤ m ∧
    (θ = arctan ((j : ℝ) / m) ∨ θ = π / 2 - arctan ((j : ℝ) / m))}

theorem arctan_abs_sub_le (x y : ℝ) : |arctan x - arctan y| ≤ |x - y| := by
  have h := (convex_univ : Convex ℝ (Set.univ : Set ℝ)).norm_image_sub_le_of_norm_deriv_le
    (fun z _ => differentiable_arctan z)
    (C := 1) (fun z _ => by
      rw [Real.deriv_arctan, Real.norm_eq_abs, abs_of_nonneg (by positivity : 0 ≤ 1 / (1 + z ^ 2))]
      exact (div_le_one (by positivity)).2 (by nlinarith [sq_nonneg z]))
    (x := y) (y := x) (mem_univ _) (mem_univ _)
  simpa only [Real.norm_eq_abs, one_mul] using h

/-- Nearest integer sampling on the unit interval, with both endpoints included. -/
theorem exists_nearest_grid_point (m : ℕ) (hm : 1 ≤ m) (x : ℝ)
    (hx : x ∈ Icc (0 : ℝ) 1) :
    ∃ j : ℕ, j ≤ m ∧ |(j : ℝ) / m - x| ≤ 1 / (2 * (m : ℝ)) := by
  have hm0 : (0 : ℝ) < m := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hm)
  let k : ℤ := round (x * m)
  have hk := abs_sub_round (x * (m : ℝ))
  change |x * (m : ℝ) - (k : ℝ)| ≤ 1 / 2 at hk
  have hk' := abs_le.mp hk
  have hk0 : 0 ≤ k := by
    have : (-1 : ℝ) < k := by nlinarith [mul_nonneg hx.1 hm0.le]
    have : (-1 : ℤ) < k := by exact_mod_cast this
    omega
  have hkm : k ≤ (m : ℤ) := by
    have : (k : ℝ) < (m : ℝ) + 1 := by nlinarith [mul_le_mul_of_nonneg_right hx.2 hm0.le]
    have : k < (m : ℤ) + 1 := by exact_mod_cast this
    omega
  refine ⟨k.toNat, by omega, ?_⟩
  have heq : (k.toNat : ℝ) = (k : ℝ) := by exact_mod_cast Int.toNat_of_nonneg hk0
  rw [heq]
  have habs : |(k : ℝ) / m - x| = |x * m - k| / m := by
    rw [show (k : ℝ) / m - x = -(x * m - k) / m by field_simp; ring]
    rw [abs_div, abs_neg, abs_of_pos hm0]
  rw [habs]
  calc
    |x * m - k| / m ≤ (1 / 2) / m := div_le_div_of_nonneg_right hk hm0.le
    _ = 1 / (2 * (m : ℝ)) := by ring

theorem rationalAngleMesh_zero (m : ℕ) : 0 ∈ rationalAngleMesh m := by
  exact ⟨0, Nat.zero_le _, Or.inl (by simp)⟩

theorem rationalAngleMesh_pi_div_two (m : ℕ) : π / 2 ∈ rationalAngleMesh m := by
  exact ⟨0, Nat.zero_le _, Or.inr (by simp)⟩

theorem rationalAngleMesh_subset (m : ℕ) (hm : 1 ≤ m) :
    rationalAngleMesh m ⊆ Icc (0 : ℝ) (π / 2) := by
  intro θ hθ
  rcases hθ with ⟨j, hj, hθ | hθ⟩
  all_goals
    have hm0 : (0 : ℝ) < m := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hm)
    have hjm : (j : ℝ) / m ≤ 1 := (div_le_one hm0).2 (by exact_mod_cast hj)
    have ha0 : 0 ≤ arctan ((j : ℝ) / m) := arctan_nonneg.mpr (by positivity)
    have ha1 : arctan ((j : ℝ) / m) ≤ π / 4 := by
      rw [← arctan_one]
      exact arctan_le_arctan_iff.mpr hjm
    subst θ
    constructor <;> linarith [Real.pi_pos]

private theorem exists_nearest_first_half (m : ℕ) (hm : 1 ≤ m) (θ : ℝ)
    (hθ : θ ∈ Icc (0 : ℝ) (π / 4)) :
    ∃ j : ℕ, j ≤ m ∧ |arctan ((j : ℝ) / m) - θ| ≤ 1 / (2 * (m : ℝ)) := by
  have hi : arctan (tan θ) = θ := arctan_tan (by linarith [Real.pi_pos, hθ.1])
    (by linarith [Real.pi_pos, hθ.2])
  have ht : tan θ ∈ Icc (0 : ℝ) 1 := by
    constructor
    · exact tan_nonneg_of_nonneg_of_le_pi_div_two hθ.1 (by linarith [Real.pi_pos, hθ.2])
    · apply arctan_le_arctan_iff.mp
      rw [hi, arctan_one]
      exact hθ.2
  obtain ⟨j, hj, hdist⟩ := exists_nearest_grid_point m hm (tan θ) ht
  refine ⟨j, hj, ?_⟩
  calc
    |arctan ((j : ℝ) / m) - θ| = |arctan ((j : ℝ) / m) - arctan (tan θ)| := by rw [hi]
    _ ≤ |(j : ℝ) / m - tan θ| := arctan_abs_sub_le _ _
    _ ≤ 1 / (2 * (m : ℝ)) := hdist

/-- The maximum distance to the rational angular mesh is at most `1 / (2m)`. -/
theorem rationalAngleMesh_covers (m : ℕ) (hm : 1 ≤ m) (θ : ℝ)
    (hθ : θ ∈ Icc (0 : ℝ) (π / 2)) :
    ∃ t ∈ rationalAngleMesh m, |t - θ| ≤ 1 / (2 * (m : ℝ)) := by
  by_cases hhalf : θ ≤ π / 4
  · obtain ⟨j, hj, hd⟩ := exists_nearest_first_half m hm θ ⟨hθ.1, hhalf⟩
    exact ⟨_, ⟨j, hj, Or.inl rfl⟩, hd⟩
  · obtain ⟨j, hj, hd⟩ := exists_nearest_first_half m hm (π / 2 - θ)
      ⟨by linarith [hθ.2], by linarith⟩
    refine ⟨_, ⟨j, hj, Or.inr rfl⟩, ?_⟩
    convert hd using 1
    rw [← abs_neg]
    congr 1
    ring

end InfiniteAggregation
