import Formal.CubicGap.Laws

namespace CubicGap.Law

variable {ι : Type*} [Fintype ι] (μ : Law ι)

@[simp] theorem expect_point (i : ι) (f : ι → ℝ) : (point i).expect f = f i := by
  classical
  simp [expect, point, ite_mul]

@[simp] theorem expect_const (c : ℝ) : μ.expect (fun _ => c) = c := by
  simp [expect, ← Finset.sum_mul, μ.mass_one]

@[simp] theorem expect_add (f g : ι → ℝ) :
    μ.expect (fun i => f i + g i) = μ.expect f + μ.expect g := by
  simp [expect, mul_add, Finset.sum_add_distrib]

@[simp] theorem expect_sub (f g : ι → ℝ) :
    μ.expect (fun i => f i - g i) = μ.expect f - μ.expect g := by
  simp [expect, mul_sub, Finset.sum_sub_distrib]

@[simp] theorem expect_mul_const (f : ι → ℝ) (c : ℝ) :
    μ.expect (fun i => f i * c) = μ.expect f * c := by
  simp [expect, ← mul_assoc, Finset.sum_mul]

@[simp] theorem expect_const_mul (c : ℝ) (f : ι → ℝ) :
    μ.expect (fun i => c * f i) = c * μ.expect f := by
  simp_rw [mul_comm c]
  rw [expect_mul_const, mul_comm]

@[simp] theorem expect_div_const (f : ι → ℝ) (c : ℝ) :
    μ.expect (fun i => f i / c) = μ.expect f / c := by
  simp [div_eq_mul_inv]

theorem expect_mono {f g : ι → ℝ} (h : ∀ i, f i ≤ g i) :
    μ.expect f ≤ μ.expect g :=
  Finset.sum_le_sum fun i _ => mul_le_mul_of_nonneg_left (h i) (μ.nonneg i)

theorem expect_nonneg {f : ι → ℝ} (h : ∀ i, 0 ≤ f i) : 0 ≤ μ.expect f :=
  Finset.sum_nonneg fun i _ => mul_nonneg (μ.nonneg i) (h i)

@[simp] theorem expect_sum {κ : Type*} [Fintype κ] (f : κ → ι → ℝ) :
    μ.expect (fun i => ∑ j, f j i) = ∑ j, μ.expect (f j) := by
  simp only [expect, Finset.mul_sum]
  rw [Finset.sum_comm]

end CubicGap.Law
