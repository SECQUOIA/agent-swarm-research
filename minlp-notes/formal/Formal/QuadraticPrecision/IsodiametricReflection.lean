import Formal.QuadraticPrecision.IsodiametricGeometry

/-! Reflection preserves Euclidean volume; its fixed hyperplane is null. -/
open Set MeasureTheory
open scoped InnerProductSpace
noncomputable section
namespace QuadraticPrecision.Isodiametric
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [MeasurableSpace E] [BorelSpace E]

/-- The reflection viewed as a measurable involution. -/
def reflectEquiv {e : E} (he : ‖e‖ = 1) (t : ℝ) : E ≃ᵐ E where
  toFun := reflect e t
  invFun := reflect e t
  left_inv := reflect_involutive he t
  right_inv := reflect_involutive he t
  measurable_toFun := (reflect_continuous e t).measurable
  measurable_invFun := (reflect_continuous e t).measurable

variable [FiniteDimensional ℝ E]

lemma reflect_measurePreserving {e : E} (he : ‖e‖ = 1) (t : ℝ) :
    MeasurePreserving (reflect e t) (volume : Measure E) volume := by
  have h := ((Submodule.reflection (ℝ ∙ e)ᗮ).measurePreserving).add_left
    (volume : Measure E) ((2 * t) • e)
  have hf : reflect e t = fun z => (2 * t) • e + (Submodule.reflection (ℝ ∙ e)ᗮ) z :=
    funext (reflect_eq he t)
  rw [hf]
  exact h

lemma hyperplane_null {e : E} (he : ‖e‖ = 1) (t : ℝ) :
    volume {z : E | ⟪e, z⟫_ℝ = t} = 0 := by
  let s : AffineSubspace ℝ E :=
    { carrier := {z | ⟪e, z⟫_ℝ = t}
      smul_vsub_vadd_mem' := by
        intro c x y z hx hy hz
        simp only [vsub_eq_sub, vadd_eq_add, mem_ofPred_eq] at *
        simp only [inner_add_right, inner_smul_right, inner_sub_right, hx, hy, hz]
        ring }
  apply Measure.addHaar_affineSubspace volume s
  intro hs
  have hmem : (t + 1) • e ∈ s := by rw [hs]; trivial
  change ⟪e, (t + 1) • e⟫_ℝ = t at hmem
  simp only [inner_smul_right, real_inner_self_eq_norm_sq, he, one_pow, mul_one] at hmem
  linarith

lemma reflect_halfspace_ae {e : E} (he : ‖e‖ = 1) (t : ℝ) :
    ∀ᵐ z ∂(volume : Measure E),
      reflect e t z ∈ {z | ⟪e, z⟫_ℝ ≤ t} ↔ z ∉ {z | ⟪e, z⟫_ℝ ≤ t} := by
  have hz : ∀ᵐ z ∂(volume : Measure E), ⟪e, z⟫_ℝ ≠ t := by
    rw [ae_iff]
    simpa using hyperplane_null he t
  filter_upwards [hz] with z hz
  simp only [inner_reflect he, not_le]
  constructor
  · intro h
    exact lt_of_le_of_ne (by linarith) hz.symm
  · intro h; linarith

omit [MeasurableSpace E] [BorelSpace E] [FiniteDimensional ℝ E] in
/-- Reflecting a point beyond the half-diameter sphere across a nearer hyperplane
sends it to the opposite side of that sphere, more than `D` away. -/
lemma exists_improving_reflection {x : E} {D : ℝ} (hD : 0 ≤ D)
    (hx : D / 2 < ‖x‖) :
    ∃ e : E, ∃ t : ℝ, ‖e‖ = 1 ∧ 0 < t ∧
      t < ⟪e, x⟫_ℝ ∧ ‖reflect e t x‖ < ‖x‖ ∧ D < dist x (reflect e t x) := by
  let r := ‖x‖
  have hr : 0 < r := lt_of_le_of_lt (by positivity) hx
  let e := r⁻¹ • x
  have he : ‖e‖ = 1 := by
    dsimp [e]
    rw [norm_smul, Real.norm_eq_abs, abs_of_pos (inv_pos.mpr hr)]
    exact inv_mul_cancel₀ hr.ne'
  have hxe : x = r • e := by
    dsimp [e]
    rw [smul_smul, mul_inv_cancel₀ hr.ne', one_smul]
  have hex : ⟪e, x⟫_ℝ = r := by
    conv_rhs => rw [← mul_one r]
    conv_lhs => rw [hxe]
    rw [inner_smul_right, real_inner_self_eq_norm_sq, he, one_pow]
  let t := (r - D / 2) / 2
  have ht : 0 < t := by dsimp [t]; linarith
  have htx : t < ⟪e, x⟫_ℝ := by rw [hex]; dsimp [t]; linarith
  have href : reflect e t x = (-D / 2) • e := by
    rw [reflect, hex, hxe, ← add_smul]
    congr 1
    dsimp [t]
    ring
  have hn : ‖reflect e t x‖ = D / 2 := by
    rw [href, norm_smul, he, mul_one, Real.norm_eq_abs, abs_of_nonpos]
    · ring
    · linarith
  refine ⟨e, t, he, ht, htx, hn ▸ hx, ?_⟩
  rw [href, dist_eq_norm, hxe, ← sub_smul, norm_smul, he, mul_one,
    Real.norm_eq_abs, abs_of_nonneg (by linarith : 0 ≤ r - -D / 2)]
  linarith

end QuadraticPrecision.Isodiametric
