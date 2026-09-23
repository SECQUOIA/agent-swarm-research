import Formal.InfiniteAggregation.Model

/-! Convexity and validity of the multipliers in the good cone. -/

noncomputable section

namespace InfiniteAggregation

/-- The discriminant condition is sufficient for a two-variable quadratic to be nonnegative. -/
theorem scalar_quadratic_nonneg {a b c : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hdisc : c ^ 2 ≤ 4 * a * b) (u v : ℝ) :
    0 ≤ a * u ^ 2 + b * v ^ 2 - c * u * v := by
  by_cases ha0 : a = 0
  · have hc0 : c = 0 := by rw [ha0] at hdisc; nlinarith [sq_nonneg c]
    simp only [ha0, hc0, zero_mul, zero_add, sub_zero]
    positivity
  · have haPos : 0 < a := lt_of_le_of_ne ha (Ne.symm ha0)
    have hprod := mul_nonneg (sub_nonneg.mpr hdisc) (sq_nonneg v)
    have hs := sq_nonneg (2 * a * u - c * v)
    nlinarith

theorem leading_nonneg (w : Weight) (hK : GoodCone w) (a b : ℝ) :
    0 ≤ w 0 * a ^ 2 + w 1 * b ^ 2 - w 2 * a * b :=
  scalar_quadratic_nonneg (hK.1 0) (hK.1 1) hK.2 a b

theorem leading_vector_nonneg {r : ℕ} (w : Weight) (hK : GoodCone w)
    (u v : Vec r) : 0 ≤ w 0 * qnorm u + w 1 * qnorm v - w 2 * dot u v := by
  have hs := Finset.sum_nonneg (fun (i : Fin r) (_ : i ∈ Finset.univ) =>
    leading_nonneg w hK (u i) (v i))
  simpa only [qnorm, dot, dotProduct, Finset.sum_add_distrib, Finset.sum_sub_distrib,
    ← Finset.mul_sum, pow_two, mul_assoc] using hs

private theorem qnorm_sub {r : ℕ} (u v : Vec r) :
    qnorm (u - v) = qnorm u - 2 * dot u v + qnorm v := by
  rw [sub_eq_add_neg, ← neg_one_smul ℝ v, qnorm_add, qnorm_smul, dot_smul_right]
  ring

private theorem dot_sub_left {r : ℕ} (u v z : Vec r) :
    dot (u - v) z = dot u z - dot v z := by
  rw [sub_eq_add_neg, ← neg_one_smul ℝ v, dot_add_left, dot_smul_left]
  ring

private theorem dot_sub_right {r : ℕ} (u v z : Vec r) :
    dot u (v - z) = dot u v - dot u z := by
  rw [sub_eq_add_neg, ← neg_one_smul ℝ z, dot_add_right, dot_smul_right]
  ring

theorem aggregate_jensen_gap {r : ℕ} (w : Weight) (x y : Var r)
    (a b : ℝ) (hab : a + b = 1) :
    a * aggregate w x + b * aggregate w y - aggregate w (a • x + b • y) =
      a * b * (w 0 * qnorm (x.1 - y.1) + w 1 * qnorm (x.2 - y.2) -
        w 2 * dot (x.1 - y.1) (x.2 - y.2)) := by
  have hb : b = 1 - a := by linarith
  subst b
  simp only [aggregate_formula, Prod.fst_add, Prod.smul_fst, Prod.snd_add,
    Prod.smul_snd, qnorm_add, qnorm_smul, dot_smul_right, dot_smul_left,
    dot_add_left, dot_add_right, qnorm_sub, dot_sub_left, dot_sub_right]
  ring

theorem goodCone_convexOn {r : ℕ} {w : Weight} (hK : GoodCone w) :
    ConvexOn ℝ Set.univ (aggregate w : Var r → ℝ) := by
  refine ⟨convex_univ, ?_⟩
  intro x _ y _ a b ha hb hab
  have hgap := aggregate_jensen_gap w x y a b hab
  have hnonneg := mul_nonneg (mul_nonneg ha hb)
    (leading_vector_nonneg w hK (x.1 - y.1) (x.2 - y.2))
  simpa only [smul_eq_mul] using (show aggregate w (a • x + b • y) ≤
    a * aggregate w x + b * aggregate w y by linarith)

theorem goodCone_hull_valid {r : ℕ} {w : Weight} (hK : GoodCone w) (hne : w ≠ 0)
    {x : Var r} (hx : x ∈ convexHull ℝ (feasible r)) : aggregate w x < 0 := by
  have hc := (goodCone_convexOn (r := r) hK).convex_lt 0
  have hsubset : feasible r ⊆ {y ∈ Set.univ | aggregate w y < 0} := by
    intro y hy
    exact ⟨Set.mem_univ _, aggregate_neg ⟨hK.1, hne⟩ hy⟩
  exact (convexHull_min hsubset hc hx).2

end InfiniteAggregation
