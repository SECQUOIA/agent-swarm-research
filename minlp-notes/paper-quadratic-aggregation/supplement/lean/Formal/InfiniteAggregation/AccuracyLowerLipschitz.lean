import Formal.InfiniteAggregation.ClosedObstruction
import Formal.InfiniteAggregation.GramBound

/-! Elementary Euclidean estimates for the lower-bound witnesses. -/

noncomputable section
namespace InfiniteAggregation

lemma accuracy_dot_abs_le {r : ℕ} (u v : Vec r) {A B : ℝ}
    (hA : 0 ≤ A) (hB : 0 ≤ B) (hu : qnorm u ≤ A ^ 2)
    (hv : qnorm v ≤ B ^ 2) : |dot u v| ≤ A * B := by
  have hc := (gramPSD_vectors u v).2.2
  have hab : qnorm u * qnorm v ≤ A ^ 2 * B ^ 2 :=
    mul_le_mul hu hv (qnorm_nonneg v) (sq_nonneg A)
  have hp : 0 ≤ A * B := mul_nonneg hA hB
  nlinarith [sq_abs (dot u v)]

lemma accuracy_qnorm_difference {r : ℕ} (u v : Vec r) {D : ℝ}
    (hD : 0 ≤ D) (hu : qnorm u ≤ 1) (hv : qnorm v ≤ 1)
    (hd : qnorm (u - v) ≤ D ^ 2) : |qnorm u - qnorm v| ≤ 2 * D := by
  have hc : |dot u v| ≤ 1 := by
    simpa using accuracy_dot_abs_le u v (A := 1) (B := 1) (by norm_num)
      (by norm_num) (by simpa using hu) (by simpa using hv)
  have hs : qnorm (u + v) ≤ 2 ^ 2 := by
    rw [qnorm_add]
    linarith [(le_abs_self (dot u v)).trans hc]
  have hb := accuracy_dot_abs_le (u - v) (u + v) hD (by norm_num : (0 : ℝ) ≤ 2) hd hs
  have heq : dot (u - v) (u + v) = qnorm u - qnorm v := by
    simp only [dot, sub_dotProduct, dotProduct_add, qnorm]
    rw [dotProduct_comm v u]
    ring
  rw [heq] at hb
  nlinarith

lemma accuracy_dot_difference {r : ℕ} (x y : Var r) {D : ℝ}
    (hD : 0 ≤ D) (hxu : qnorm x.1 ≤ 1) (hyv : qnorm y.2 ≤ 1)
    (hdu : qnorm (x.1 - y.1) ≤ D ^ 2)
    (hdv : qnorm (x.2 - y.2) ≤ D ^ 2) :
    |dot x.1 x.2 - dot y.1 y.2| ≤ 2 * D := by
  have hu : |dot (x.1 - y.1) y.2| ≤ D := by
    simpa using accuracy_dot_abs_le (x.1 - y.1) y.2 hD
      (by norm_num : (0 : ℝ) ≤ 1) hdu (by simpa using hyv)
  have hv : |dot x.1 (x.2 - y.2)| ≤ D := by
    simpa using accuracy_dot_abs_le x.1 (x.2 - y.2)
      (by norm_num : (0 : ℝ) ≤ 1) hD (by simpa using hxu) hdv
  have heq : dot x.1 x.2 - dot y.1 y.2 =
      dot x.1 (x.2 - y.2) + dot (x.1 - y.1) y.2 := by
    simp only [dot, sub_dotProduct, dotProduct_sub]
    ring
  rw [heq]
  exact (abs_add_le _ _).trans (by linarith)

/-- A dimension-independent Lipschitz bound on the product of two unit balls.
The hypothesis on `D` is supplied by the genuine Euclidean distance. -/
theorem accuracy_ray_lipschitz {r : ℕ} {τ : ℝ} (hτ : τ ∈ Set.Icc (1 : ℝ) 2)
    (x y : Var r) {D : ℝ} (hD : 0 ≤ D)
    (hxu : qnorm x.1 ≤ 1) (hxv : qnorm x.2 ≤ 1)
    (hyu : qnorm y.1 ≤ 1) (hyv : qnorm y.2 ≤ 1)
    (hdu : qnorm (x.1 - y.1) ≤ D ^ 2)
    (hdv : qnorm (x.2 - y.2) ≤ D ^ 2) :
    |aggregate (rayWeight τ) x - aggregate (rayWeight τ) y| ≤ 10 * D := by
  have ht : 0 < τ := by linarith [hτ.1]
  have hi : 0 ≤ 1 / τ := by positivity
  have hi' : 1 / τ ≤ 1 := (div_le_one ht).2 hτ.1
  have hu := accuracy_qnorm_difference x.1 y.1 hD hxu hyu hdu
  have hv := accuracy_qnorm_difference x.2 y.2 hD hxv hyv hdv
  have hc := accuracy_dot_difference x y hD hxu hyv hdu hdv
  have heq : aggregate (rayWeight τ) x - aggregate (rayWeight τ) y =
      τ * (qnorm x.1 - qnorm y.1) + (1 / τ) * (qnorm x.2 - qnorm y.2) -
      2 * (dot x.1 x.2 - dot y.1 y.2) := by
    simp only [aggregate_formula, rayWeight, Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.cons_val]
    ring
  rw [heq]
  calc
    _ ≤ |τ * (qnorm x.1 - qnorm y.1) + (1 / τ) * (qnorm x.2 - qnorm y.2)| +
        |2 * (dot x.1 x.2 - dot y.1 y.2)| := abs_sub _ _
    _ ≤ |τ * (qnorm x.1 - qnorm y.1)| + |(1 / τ) * (qnorm x.2 - qnorm y.2)| +
        |2 * (dot x.1 x.2 - dot y.1 y.2)| := by gcongr; exact abs_add_le _ _
    _ = τ * |qnorm x.1 - qnorm y.1| + (1 / τ) * |qnorm x.2 - qnorm y.2| +
        2 * |dot x.1 x.2 - dot y.1 y.2| := by
      rw [abs_mul, abs_mul, abs_mul, abs_of_pos ht, abs_of_nonneg hi]
      norm_num
    _ ≤ τ * (2 * D) + (1 / τ) * (2 * D) + 2 * (2 * D) := by gcongr
    _ ≤ 10 * D := by
      nlinarith [mul_nonneg (sub_nonneg.mpr hτ.2) hD,
        mul_nonneg (sub_nonneg.mpr hi') hD]

end InfiniteAggregation
