import QipmFormal.Coupling.WitnessLimits
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.CStarAlgebra.Basic

/-! # Euclidean operator norms of the sparse LP witnesses

The scoped matrix norm in this file is the norm induced on Euclidean space.
The characteristic roots are identified with the entire spectrum, then the
Hermitian spectral theorem supplies the exact operator norm.
-/
namespace QipmFormal.Coupling.Witnesses
noncomputable section
open Matrix
open scoped Matrix.Norms.L2Operator

/-- The actual induced Euclidean operator norm, independent of matrix norm scopes. -/
def operatorNorm (A : Matrix (Fin 2) (Fin 2) ℝ) : ℝ :=
  ‖Matrix.toEuclideanCLM (n := Fin 2) (𝕜 := ℝ) A‖

private theorem hermitian_norm {A : Matrix (Fin 2) (Fin 2) ℝ} (hA : A.IsHermitian) :
    ‖A‖ = ‖hA.eigenvalues‖ := by
  conv_lhs => rw [hA.spectral_theorem]
  simp only [Unitary.conjStarAlgAut_apply, ← Unitary.coe_star,
    CStarRing.norm_mul_coe_unitary, CStarRing.norm_coe_unitary_mul,
    Matrix.l2_opNorm_diagonal]
  rfl

private theorem spectrum_iff_det {A : Matrix (Fin 2) (Fin 2) ℝ} (r : ℝ) :
    r ∈ spectrum ℝ A ↔ (A-r • 1).det = 0 := by
  rw [Matrix.mem_spectrum_iff_isRoot_charpoly]
  simp only [Polynomial.IsRoot, Matrix.eval_charpoly]
  have h : Matrix.scalar (Fin 2) r - A = -(A-r • 1) := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.scalar, sub_eq_add_neg]
  rw [h, Matrix.det_neg]
  norm_num

private theorem norm_of_spectrum {A : Matrix (Fin 2) (Fin 2) ℝ} (hA : A.IsHermitian)
    {l s : ℝ} (hs : 0 ≤ s) (hsl : s ≤ l)
    (hsp : ∀ r, r ∈ spectrum ℝ A ↔ r = l ∨ r = s) : operatorNorm A = l := by
  change ‖A‖ = l
  rw [hermitian_norm hA]
  apply le_antisymm
  · apply (pi_norm_le_iff_of_nonneg (le_trans hs hsl)).mpr
    intro i
    have hi : hA.eigenvalues i ∈ spectrum ℝ A := by
      rw [hA.spectrum_real_eq_range_eigenvalues]
      exact ⟨i, rfl⟩
    rcases (hsp _).mp hi with h | h
    · simp [h, abs_of_nonneg (le_trans hs hsl)]
    · simpa [h, abs_of_nonneg hs] using hsl
  · have hl : l ∈ spectrum ℝ A := (hsp _).mpr (Or.inl rfl)
    rw [hA.spectrum_real_eq_range_eigenvalues] at hl
    obtain ⟨i, rfl⟩ := hl
    simpa [Real.norm_eq_abs, abs_of_nonneg (le_trans hs hsl)] using
      norm_le_pi_norm hA.eigenvalues i

theorem coupled_hermitian (a c : ℝ) : (coupledH a c).IsHermitian := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [coupledH, Matrix.conjTranspose_apply]

/-- No eigenvalues are omitted by the two radical formulas. -/
theorem coupled_spectrum (a c r : ℝ) :
    r ∈ spectrum ℝ (coupledH a c) ↔ r = largeRoot a c ∨ r = smallRoot a c := by
  rw [spectrum_iff_det]
  have hs := root_sum a c
  have hp := root_product a c
  have hf : (coupledH a c-r • 1).det = (r-largeRoot a c)*(r-smallRoot a c) := by
    simp [Matrix.det_fin_two, coupledH]
    nlinarith [congrArg (fun x : ℝ => r*x) hs]
  rw [hf, mul_eq_zero, sub_eq_zero, sub_eq_zero]

theorem coupled_operatorNorm {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    operatorNorm (coupledH a c) = largeRoot a c :=
  norm_of_spectrum (coupled_hermitian a c) (smallRoot_pos ha hc).le
    (root_order a c) (coupled_spectrum a c)

theorem coupled_inverse_spectrum {a c : ℝ} (ha : 0 < a) (hc : 0 < c) (r : ℝ) :
    r ∈ spectrum ℝ (coupledH a c)⁻¹ ↔
      r = (largeRoot a c)⁻¹ ∨ r = (smallRoot a c)⁻¹ := by
  have hd : 2*a+c ≠ 0 := by positivity
  have hl : largeRoot a c ≠ 0 := ne_of_gt (largeRoot_pos ha hc)
  have hs : smallRoot a c ≠ 0 := ne_of_gt (smallRoot_pos ha hc)
  have hsum := root_sum a c
  have hprod := root_product a c
  rw [spectrum_iff_det]
  have hf : ((coupledH a c)⁻¹-r • 1).det * (c*(2*a+c)) =
      (r*largeRoot a c-1)*(r*smallRoot a c-1) := by
    rw [coupled_inverse (ne_of_gt hc) hd]
    have hp : (r*largeRoot a c-1)*(r*smallRoot a c-1) =
        r^2*(c*(2*a+c))-r*(a+3*c)+1 := by
      nlinarith [congrArg (fun x : ℝ => r*x) hsum,
        congrArg (fun x : ℝ => r^2*x) hprod]
    rw [hp]
    simp [Matrix.det_fin_two]
    field_simp [ne_of_gt hc, hd]
    ring
  have hz : c*(2*a+c) ≠ 0 := mul_ne_zero (ne_of_gt hc) hd
  rw [← mul_eq_zero_iff_right hz, hf, mul_eq_zero]
  constructor
  · rintro (h | h)
    · left; rw [← one_div]; exact (eq_div_iff hl).mpr (sub_eq_zero.mp h)
    · right; rw [← one_div]; exact (eq_div_iff hs).mpr (sub_eq_zero.mp h)
  · rintro (rfl | rfl) <;> simp [hl, hs]

theorem coupled_inverse_operatorNorm {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    operatorNorm (coupledH a c)⁻¹ = (smallRoot a c)⁻¹ := by
  apply norm_of_spectrum ((coupled_hermitian a c).inv)
    (inv_nonneg.mpr (largeRoot_pos ha hc).le)
    ((inv_le_inv₀ (largeRoot_pos ha hc) (smallRoot_pos ha hc)).mpr (root_order a c))
  intro r
  rw [coupled_inverse_spectrum ha hc]
  exact or_comm

/-- Euclidean spectral condition number of the actual coupled normal matrix. -/
theorem coupled_conditionNumber {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    operatorNorm (coupledH a c) * operatorNorm (coupledH a c)⁻¹ =
      largeRoot a c / smallRoot a c := by
  rw [coupled_operatorNorm ha hc, coupled_inverse_operatorNorm ha hc, div_eq_mul_inv]

private theorem supNorm_pair (x y : ℝ) : ‖![x,y]‖ = max |x| |y| := by
  apply le_antisymm
  · apply (pi_norm_le_iff_of_nonneg (le_trans (abs_nonneg x) (le_max_left _ _))).mpr
    intro i; fin_cases i
    · simp [Real.norm_eq_abs]
    · simp [Real.norm_eq_abs]
  · exact max_le (by simpa [Real.norm_eq_abs] using norm_le_pi_norm ![x,y] 0)
      (by simpa [Real.norm_eq_abs] using norm_le_pi_norm ![x,y] 1)

/-- The decoupled normal matrix has norm `μ⁻¹` in the small-parameter regime. -/
theorem decoupled_operatorNorm {μ : ℝ} (hμ : 0 < μ) (hu : 2 * μ ^ 2 ≤ 1) :
    operatorNorm (decoupledH μ) = μ⁻¹ := by
  have he : decoupledH μ = diagonal ![μ⁻¹, 2*μ] := by
    ext i j; fin_cases i <;> fin_cases j <;> simp [decoupledH]
  have hle : 2*μ ≤ μ⁻¹ := by
    rw [← one_div, le_div_iff₀ hμ]
    nlinarith
  change ‖decoupledH μ‖ = μ⁻¹
  rw [he, Matrix.l2_opNorm_diagonal, supNorm_pair]
  rw [abs_of_pos (inv_pos.mpr hμ), abs_of_pos (show 0 < 2*μ by positivity),
    max_eq_left hle]

theorem decoupled_inverse_operatorNorm {μ : ℝ} (hμ : 0 < μ) (hu : 2 * μ ^ 2 ≤ 1) :
    operatorNorm (decoupledH μ)⁻¹ = (2*μ)⁻¹ := by
  have he : (decoupledH μ)⁻¹ = diagonal ![μ, (2*μ)⁻¹] := by
    rw [decoupled_inverse (ne_of_gt hμ)]
    ext i j; fin_cases i <;> fin_cases j <;> simp
  have hle : μ ≤ (2*μ)⁻¹ := by
    rw [← one_div, le_div_iff₀ (show 0 < 2*μ by positivity)]
    nlinarith
  change ‖(decoupledH μ)⁻¹‖ = (2*μ)⁻¹
  rw [he, Matrix.l2_opNorm_diagonal, supNorm_pair]
  rw [abs_of_pos hμ, abs_of_pos (inv_pos.mpr (show 0 < 2*μ by positivity)),
    max_eq_right hle]

theorem decoupled_conditionNumber {μ : ℝ} (hμ : 0 < μ) (hu : 2 * μ ^ 2 ≤ 1) :
    operatorNorm (decoupledH μ) * operatorNorm (decoupledH μ)⁻¹ = 1/(2*μ^2) := by
  rw [decoupled_operatorNorm hμ hu, decoupled_inverse_operatorNorm hμ hu]
  field_simp

end
end QipmFormal.Coupling.Witnesses
