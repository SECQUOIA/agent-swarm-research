import Formal.InfiniteAggregation.Model
import Formal.InfiniteAggregation.GramFrame
import Formal.InfiniteAggregation.HullCoreRoots
import Formal.InfiniteAggregation.HullModel

/-!
# A two-point decomposition for the strict hull

The perturbation direction is orthogonal to a weighted difference of the
two vectors. It need not be orthogonal to both vectors. This proves the
decomposition already in dimension two.
-/

open Set
noncomputable section
namespace InfiniteAggregation

private theorem unit_perpendicular_vector {r : ℕ} (hr : 2 ≤ r) (w : Vec r) :
    ∃ e : Vec r, qnorm e = 1 ∧ dot w e = 0 := by
  obtain ⟨f, e, P, Q, R, hf, he, hfe, _, _, hw, _⟩ :=
    exists_gram_frame hr w 0
  refine ⟨e, he, ?_⟩
  rw [hw, dot_smul_left]
  change P * (f ⬝ᵥ e) = 0
  rw [hfe, mul_zero]

/-- Every point satisfying the strict scalar hull inequalities is an
average of two feasible points with possibly unequal positive weights. -/
theorem two_point_decomposition_of_strict_hull_inequalities {r : ℕ} (hr : 2 ≤ r)
    (x : Var r) (hu : qnorm x.1 < 1) (hv : qnorm x.2 < 1)
    (hc : 1 / 2 < dot x.1 x.2 +
      Real.sqrt ((1 - qnorm x.1) * (1 - qnorm x.2))) :
    ∃ y ∈ feasible r, ∃ z ∈ feasible r, ∃ a b : ℝ,
      0 ≤ a ∧ 0 ≤ b ∧ a + b = 1 ∧ a • y + b • z = x := by
  let a := Real.sqrt (1 - qnorm x.1)
  let b := Real.sqrt (1 - qnorm x.2)
  have ha : 0 < a := Real.sqrt_pos.2 (by linarith)
  have hb : 0 < b := Real.sqrt_pos.2 (by linarith)
  have ha2 : a ^ 2 = 1 - qnorm x.1 := Real.sq_sqrt (by linarith)
  have hb2 : b ^ 2 = 1 - qnorm x.2 := Real.sq_sqrt (by linarith)
  have hab : 0 < a * b := mul_pos ha hb
  have hsqrt : Real.sqrt ((1 - qnorm x.1) * (1 - qnorm x.2)) = a * b := by
    exact Real.sqrt_mul (by linarith : 0 ≤ 1 - qnorm x.1) _
  rw [hsqrt] at hc
  have hratio : (1 / 2 - dot x.1 x.2) / (a * b) < 1 := by
    apply (div_lt_iff₀ hab).2
    linarith
  obtain ⟨k, hk, hk1⟩ := exists_between
    (max_lt (by norm_num : (0 : ℝ) < 1) hratio)
  have hk0 : 0 < k := lt_of_le_of_lt (le_max_left _ _) hk
  have hkc : 1 / 2 - dot x.1 x.2 < k * (a * b) :=
    (div_lt_iff₀ hab).1 (lt_of_le_of_lt (le_max_right _ _) hk)
  obtain ⟨e, he, hwe⟩ := unit_perpendicular_vector hr (b • x.1 - a • x.2)
  have hrel : b * dot x.1 e - a * dot x.2 e = 0 := by
    simpa only [dot, sub_dotProduct, smul_dotProduct, smul_eq_mul] using hwe
  let d := dot x.1 e / a
  have hue : dot x.1 e = a * d := by
    dsimp [d]
    field_simp
  have hve : dot x.2 e = b * d := by
    have hz : a * (dot x.2 e - b * d) = 0 := by
      rw [hue] at hrel
      nlinarith only [hrel]
    exact sub_eq_zero.1 ((mul_eq_zero.1 hz).resolve_left ha.ne')
  let y : ℝ → Var r := fun t => (x.1 + (t * a) • e, x.2 + (t * b) • e)
  have hy : ∀ t : ℝ, 2 * d * t + t ^ 2 = k → y t ∈ feasible r := by
    intro t ht
    apply (mem_feasible_iff _).2
    have hyu : qnorm (y t).1 = qnorm x.1 + a ^ 2 * k := by
      dsimp [y]
      rw [qnorm_add, qnorm_smul, he, dot_smul_right, hue]
      linear_combination a ^ 2 * ht
    have hyv : qnorm (y t).2 = qnorm x.2 + b ^ 2 * k := by
      dsimp [y]
      rw [qnorm_add, qnorm_smul, he, dot_smul_right, hve]
      linear_combination b ^ 2 * ht
    have hydot : dot (y t).1 (y t).2 = dot x.1 x.2 + (a * b) * k := by
      dsimp [y]
      simp only [dot_add_left, dot_add_right, dot_smul_left, dot_smul_right,
        hue, dot_comm e x.2, hve]
      change dot x.1 x.2 + t * a * (b * d) +
        t * b * (a * d + t * a * qnorm e) = _
      rw [he]
      linear_combination (a * b) * ht
    rw [hyu, hyv, hydot]
    constructor
    · nlinarith only [ha2, mul_pos (sq_pos_of_pos ha) (sub_pos.2 hk1)]
    constructor
    · nlinarith only [hb2, mul_pos (sq_pos_of_pos hb) (sub_pos.2 hk1)]
    · nlinarith only [hkc]
  obtain ⟨tm, tp, am, ap, _, _, htm, htp, ham, hap, hsum, hzero⟩ :=
    two_roots_weights d k hk0
  have hcomb : am • y tm + ap • y tp = x := by
    apply Prod.ext
    · ext j
      change am * (x.1 j + tm * a * e j) + ap * (x.1 j + tp * a * e j) = x.1 j
      linear_combination x.1 j * hsum + a * e j * hzero
    · ext j
      change am * (x.2 j + tm * b * e j) + ap * (x.2 j + tp * b * e j) = x.2 j
      linear_combination x.2 j * hsum + b * e j * hzero
  exact ⟨y tm, hy tm htm, y tp, hy tp htp, am, ap, ham, hap, hsum, hcomb⟩

theorem hullRegion_subset_convexHull {r : ℕ} (hr : 2 ≤ r) :
    hullRegion r ⊆ convexHull ℝ (feasible r) := by
  intro x hx
  obtain ⟨y, hy, z, hz, a, b, ha, hb, hab, hcomb⟩ :=
    two_point_decomposition_of_strict_hull_inequalities hr x hx.1 hx.2.1 hx.2.2
  rw [← hcomb]
  exact (convex_convexHull ℝ (feasible r))
    (subset_convexHull ℝ _ hy) (subset_convexHull ℝ _ hz) ha hb hab

end InfiniteAggregation
