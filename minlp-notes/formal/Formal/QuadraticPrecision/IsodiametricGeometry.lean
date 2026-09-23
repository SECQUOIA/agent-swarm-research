import Mathlib.Analysis.InnerProductSpace.Projection.Reflection
import Mathlib.MeasureTheory.Measure.Haar.InnerProductSpace
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.MeasureTheory.Measure.Support

/-! Geometry of a polarization towards a halfspace containing the origin. -/
open Set MeasureTheory
open scoped InnerProductSpace
noncomputable section
namespace QuadraticPrecision.Isodiametric
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]

/-- Reflection in the hyperplane with unit normal `e` and offset `t`. -/
def reflect (e : E) (t : ℝ) (z : E) : E :=
  z + (2 * (t - ⟪e, z⟫_ℝ)) • e

lemma inner_reflect {e : E} (he : ‖e‖ = 1) (t : ℝ) (z : E) :
    ⟪e, reflect e t z⟫_ℝ = 2 * t - ⟪e, z⟫_ℝ := by
  simp only [reflect, inner_add_right, inner_smul_right, real_inner_self_eq_norm_sq, he]
  ring

lemma reflect_involutive {e : E} (he : ‖e‖ = 1) (t : ℝ) :
    Function.Involutive (reflect e t) := by
  intro z
  rw [reflect, inner_reflect he]
  simp only [reflect, ← add_smul, add_assoc]
  have : 2 * (t - ⟪e, z⟫_ℝ) + 2 * (t - (2 * t - ⟪e, z⟫_ℝ)) = 0 := by ring
  rw [this, zero_smul, add_zero]

lemma reflect_eq {e : E} (he : ‖e‖ = 1) (t : ℝ) (z : E) :
    reflect e t z = (2 * t) • e + (Submodule.reflection (ℝ ∙ e)ᗮ) z := by
  rw [Submodule.reflection_orthogonal_apply, Submodule.reflection_singleton_apply]
  simp only [he]
  simp only [reflect, neg_sub]
  module

lemma reflect_dist {e : E} (he : ‖e‖ = 1) (t : ℝ) (x y : E) :
    dist (reflect e t x) (reflect e t y) = dist x y := by
  rw [reflect_eq he, reflect_eq he, dist_add_left]
  exact (Submodule.reflection (ℝ ∙ e)ᗮ).dist_map x y

lemma reflect_continuous (e : E) (t : ℝ) : Continuous (reflect e t) := by
  unfold reflect
  fun_prop

lemma reflect_norm_sq {e : E} (he : ‖e‖ = 1) (t : ℝ) (z : E) :
    ‖reflect e t z‖ ^ 2 = ‖z‖ ^ 2 + 4 * t * (t - ⟪e, z⟫_ℝ) := by
  rw [reflect, norm_add_sq_real, inner_smul_right, real_inner_comm z e,
    norm_smul, he, mul_one, Real.norm_eq_abs, sq_abs]
  ring

lemma reflect_dist_sq {e : E} (he : ‖e‖ = 1) (t : ℝ) (x y : E) :
    dist x (reflect e t y) ^ 2 = dist x y ^ 2 +
      4 * (t - ⟪e, x⟫_ℝ) * (t - ⟪e, y⟫_ℝ) := by
  simp only [dist_eq_norm, reflect]
  rw [show x - (y + (2 * (t - ⟪e, y⟫_ℝ)) • e) =
      (x - y) - (2 * (t - ⟪e, y⟫_ℝ)) • e by abel,
    norm_sub_sq_real, inner_smul_right, inner_sub_left,
    real_inner_comm x e, real_inner_comm y e, norm_smul, he, mul_one,
    Real.norm_eq_abs, sq_abs]
  ring

lemma dist_le_reflect_dist {e : E} (he : ‖e‖ = 1) {t : ℝ} {x y : E}
    (hx : ⟪e, x⟫_ℝ ≤ t) (hy : ⟪e, y⟫_ℝ ≤ t) :
    dist x y ≤ dist x (reflect e t y) := by
  have h := reflect_dist_sq he t x y
  have hp : 0 ≤ 4 * (t - ⟪e, x⟫_ℝ) * (t - ⟪e, y⟫_ℝ) :=
    mul_nonneg (mul_nonneg (by norm_num) (sub_nonneg.mpr hx)) (sub_nonneg.mpr hy)
  nlinarith [dist_nonneg (x := x) (y := y), dist_nonneg (x := x) (y := reflect e t y)]

/-- Keep doubly occupied pairs and move singly occupied pairs into `H`. -/
def polarize (r : E → E) (H K : Set E) : Set E :=
  (K ∩ r ⁻¹' K) ∪ ((K ∪ r ⁻¹' K) ∩ H)

omit [InnerProductSpace ℝ E] in
lemma polarize_compact {r : E → E} (hr : Function.Involutive r)
    (hc : Continuous r) {H K : Set E} (hH : IsClosed H) (hK : IsCompact K) :
    IsCompact (polarize r H K) := by
  have hp : r ⁻¹' K = r '' K := by
    ext x
    constructor
    · intro hx; exact ⟨r x, hx, hr x⟩
    · rintro ⟨y, hy, rfl⟩; simpa [hr y] using hy
  unfold polarize
  rw [hp]
  exact (hK.inter (hK.image hc)).union ((hK.union (hK.image hc)).inter_right hH)

lemma polarize_diameter {e : E} (he : ‖e‖ = 1) {t D : ℝ} {K : Set E}
    (hD : ∀ x ∈ K, ∀ y ∈ K, dist x y ≤ D) :
    ∀ x ∈ polarize (reflect e t) {z | ⟪e, z⟫_ℝ ≤ t} K,
    ∀ y ∈ polarize (reflect e t) {z | ⟪e, z⟫_ℝ ≤ t} K, dist x y ≤ D := by
  intro x hx y hy
  rcases hx with hx | ⟨hx, hxH⟩ <;> rcases hy with hy | ⟨hy, hyH⟩
  · exact hD x hx.1 y hy.1
  · rcases hy with hy | hy
    · exact hD x hx.1 y hy
    · rw [← reflect_dist he t x y]; exact hD _ hx.2 _ hy
  · rcases hx with hx | hx
    · exact hD x hx y hy.1
    · rw [← reflect_dist he t x y]; exact hD _ hx _ hy.2
  · rcases hx with hx | hx <;> rcases hy with hy | hy
    · exact hD x hx y hy
    · exact (dist_le_reflect_dist he hxH hyH).trans (hD x hx _ hy)
    · rw [dist_comm]
      exact (dist_le_reflect_dist he hyH hxH).trans (hD y hy _ hx)
    · rw [← reflect_dist he t x y]; exact hD _ hx _ hy

lemma polarize_bounded {e : E} (he : ‖e‖ = 1) {t R : ℝ} (ht : 0 ≤ t)
    {K : Set E} (hK : K ⊆ Metric.closedBall 0 R) :
    polarize (reflect e t) {z | ⟪e, z⟫_ℝ ≤ t} K ⊆ Metric.closedBall 0 R := by
  intro z hz
  rcases hz with hz | ⟨hz, hzH⟩
  · exact hK hz.1
  rcases hz with hz | hz
  · exact hK hz
  have hn : ‖z‖ ≤ ‖reflect e t z‖ := by
    have heq := reflect_norm_sq he t z
    have hp : 0 ≤ 4 * t * (t - ⟪e, z⟫_ℝ) :=
      mul_nonneg (mul_nonneg (by norm_num) ht) (sub_nonneg.mpr hzH)
    nlinarith [norm_nonneg z, norm_nonneg (reflect e t z)]
  simpa only [Metric.mem_closedBall, dist_zero_right] using hn.trans (by
    simpa only [Metric.mem_closedBall, dist_zero_right] using hK hz)

end QuadraticPrecision.Isodiametric
