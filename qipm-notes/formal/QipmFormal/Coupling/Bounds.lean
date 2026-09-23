import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! # Euclidean norm estimates for the two exact inverse vectors

The norm is explicitly the orthogonal-sum norm, rather than Lean's default
maximum norm on a product. The lower bound uses the upper coordinate to control
cancellation in the lower coordinate of the second inverse.
-/
namespace QipmFormal.Coupling

variable {U K : Type*} [NormedAddCommGroup U] [NormedAddCommGroup K]

noncomputable def blockNorm (u : U) (v : K) : ℝ :=
  Real.sqrt (‖u‖ ^ 2 + ‖v‖ ^ 2)

lemma blockNorm_nonneg (u : U) (v : K) : 0 ≤ blockNorm u v := Real.sqrt_nonneg _

lemma blockNorm_sq (u : U) (v : K) : blockNorm u v ^ 2 = ‖u‖ ^ 2 + ‖v‖ ^ 2 :=
  Real.sq_sqrt (by positivity)

lemma norm_le_blockNorm_left (u : U) (v : K) : ‖u‖ ≤ blockNorm u v := by
  have := blockNorm_sq u v
  have := blockNorm_nonneg u v
  nlinarith [sq_nonneg ‖v‖]

lemma norm_le_blockNorm_right (u : U) (v : K) : ‖v‖ ≤ blockNorm u v := by
  have := blockNorm_sq u v
  have := blockNorm_nonneg u v
  nlinarith [sq_nonneg ‖u‖]

lemma blockNorm_le_add (u : U) (v : K) : blockNorm u v ≤ ‖u‖ + ‖v‖ := by
  have := blockNorm_sq u v
  have := blockNorm_nonneg u v
  nlinarith [norm_nonneg u, norm_nonneg v]

variable [NormedSpace ℝ U] [NormedSpace ℝ K]

lemma blockNorm_smul (a : ℝ) (u : U) (v : K) :
    blockNorm (a • u) (a • v) = |a| * blockNorm u v := by
  have h := blockNorm_sq (a • u) (a • v)
  simp only [norm_smul, Real.norm_eq_abs] at h
  have h' := blockNorm_sq u v
  have := blockNorm_nonneg (a • u) (a • v)
  have : 0 ≤ |a| * blockNorm u v := mul_nonneg (abs_nonneg _) (blockNorm_nonneg _ _)
  apply (sq_eq_sq₀ (blockNorm_nonneg _ _) this).mp
  calc
    _ = |a| ^ 2 * (‖u‖ ^ 2 + ‖v‖ ^ 2) := by rw [h]; ring
    _ = _ := by rw [← h']; ring

lemma firstInverse_bounds (μ p₀ P G : ℝ) (p : U) (g : K)
    (hμ : 0 ≤ μ) (hp₀ : p₀ ≤ ‖p‖) (hp : ‖p‖ ≤ P) (hg : ‖g‖ ≤ G) :
    μ * p₀ ≤ blockNorm (μ • p) (μ • -g) ∧
      blockNorm (μ • p) (μ • -g) ≤ μ * (P + G) := by
  rw [blockNorm_smul, abs_of_nonneg hμ]
  constructor
  · exact mul_le_mul_of_nonneg_left (hp₀.trans (norm_le_blockNorm_left _ _)) hμ
  · exact mul_le_mul_of_nonneg_left
      ((blockNorm_le_add _ _).trans (by simpa using add_le_add hp hg)) hμ

/-- `h` represents `E⁻¹ g` and `r` represents `E⁻¹ F q`. The two hypotheses
relating `h` and `g` follow from uniform bounds on `E` and `E⁻¹`. -/
lemma secondInverse_bounds (μ q₀ Q A B T : ℝ) (q : U) (g h r : K)
    (hq₀ : 0 < q₀) (hA : 0 ≤ A) (hB : 0 ≤ B) (hT : 0 ≤ T)
    (hqlo : q₀ ≤ ‖q‖) (hqhi : ‖q‖ ≤ Q)
    (hgh : ‖g‖ ≤ A * ‖h‖) (hhg : ‖h‖ ≤ B * ‖g‖) (hr : ‖r‖ ≤ T) :
    ‖g‖ + μ ^ 2 ≤ (A + (A * T + 1) / q₀) * blockNorm (μ ^ 2 • q) (-h - μ ^ 2 • r) ∧
    blockNorm (μ ^ 2 • q) (-h - μ ^ 2 • r) ≤
      (Q + T + B) * (‖g‖ + μ ^ 2) := by
  let y := blockNorm (μ ^ 2 • q) (-h - μ ^ 2 • r)
  have hy : 0 ≤ y := blockNorm_nonneg _ _
  have hq : μ ^ 2 * q₀ ≤ y := by
    have h := norm_le_blockNorm_left (μ ^ 2 • q) (-h - μ ^ 2 • r)
    simp only [norm_smul, Real.norm_eq_abs, abs_of_nonneg (sq_nonneg μ)] at h
    exact (mul_le_mul_of_nonneg_left hqlo (sq_nonneg μ)).trans h
  have hr' : ‖μ ^ 2 • r‖ ≤ μ ^ 2 * T := by
    simpa [norm_smul, Real.norm_eq_abs, abs_of_nonneg (sq_nonneg μ)] using
      mul_le_mul_of_nonneg_left hr (sq_nonneg μ)
  have hh : ‖h‖ ≤ y + μ ^ 2 * T := by
    have htri := norm_add_le (-h - μ ^ 2 • r) (μ ^ 2 • r)
    simp only [sub_add_cancel, norm_neg] at htri
    exact htri.trans (add_le_add (norm_le_blockNorm_right _ _) hr')
  constructor
  · change ‖g‖ + μ ^ 2 ≤ (A + (A * T + 1) / q₀) * y
    have hg : ‖g‖ ≤ A * (y + μ ^ 2 * T) :=
      hgh.trans (mul_le_mul_of_nonneg_left hh hA)
    have hqt : μ ^ 2 ≤ y / q₀ := (le_div_iff₀ hq₀).2 (by nlinarith [hq])
    have hpos : 0 ≤ A * T + 1 := by positivity
    have ht := mul_le_mul_of_nonneg_left hqt hpos
    calc
      _ ≤ A * y + (A * T + 1) * μ ^ 2 := by nlinarith [hg]
      _ ≤ A * y + (A * T + 1) * (y / q₀) := add_le_add_right ht _
      _ = _ := by ring
  · change y ≤ (Q + T + B) * (‖g‖ + μ ^ 2)
    have hQ : 0 ≤ Q := (norm_nonneg q).trans hqhi
    have hup : y ≤ μ ^ 2 * Q + (B * ‖g‖ + μ ^ 2 * T) := by
      apply (blockNorm_le_add _ _).trans
      apply add_le_add
      · simpa [norm_smul, Real.norm_eq_abs, abs_of_nonneg (sq_nonneg μ)] using
          mul_le_mul_of_nonneg_left hqhi (sq_nonneg μ)
      · exact (norm_sub_le _ _).trans (by simpa using add_le_add hhg hr')
    nlinarith [mul_nonneg (hQ.trans (le_add_of_nonneg_right hT)) (norm_nonneg g),
      mul_nonneg hB (sq_nonneg μ)]

end QipmFormal.Coupling
