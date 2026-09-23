import QipmFormal.Coupling.WitnessSpectrum

/-! # Actual norm-tight witness parameters and endpoint limits

The parameters use the induced Euclidean operator norm and Euclidean vector
norm, applied to the actual normal matrix and its nonsingular inverse.
All three limits are along positive `μ` in the paper's radical parameterization.
-/
namespace QipmFormal.Coupling.Witnesses
noncomputable section
open Matrix Filter
open scoped Topology

def conditionNumber (H : Matrix (Fin 2) (Fin 2) ℝ) := operatorNorm H * operatorNorm H⁻¹
def firstAmplification (H : Matrix (Fin 2) (Fin 2) ℝ) :=
  operatorNorm H * vectorNorm (H⁻¹ *ᵥ rhs) / vectorNorm rhs
def filteringParameter (H : Matrix (Fin 2) (Fin 2) ℝ) :=
  operatorNorm H * vectorNorm (H⁻¹ *ᵥ (H⁻¹ *ᵥ rhs)) / vectorNorm (H⁻¹ *ᵥ rhs)
def paperH (μ : ℝ) := coupledH (thetaOne (paperT μ)) (theta (paperT μ))

theorem paperH_normal {μ : ℝ} (hμ : 0 < μ) :
    paperH μ = normal coupledA (coupledX (paperT μ)) (coupledS (paperT μ)) :=
  (coupled_normal (paperT_domain hμ).1 (paperT_domain hμ).2).symm

private theorem theta_positive {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    0 < thetaOne t ∧ 0 < theta t := by
  have hμ := centerParameter_pos ht hu
  have h1 : 0 < 1-t := by linarith
  exact ⟨div_pos (sq_pos_of_pos h1) hμ, div_pos (sq_pos_of_pos ht) hμ⟩

theorem coupled_parameter_certificates {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    (centerParameter t)^2 * conditionNumber (coupledH (thetaOne t) (theta t)) =
      scaledKappa t ∧
    firstAmplification (coupledH (thetaOne t) (theta t)) = xiCertificate t ∧
    (centerParameter t)^2 * filteringParameter (coupledH (thetaOne t) (theta t)) =
      scaledRhoCertificate t := by
  obtain ⟨ha,hc⟩ := theta_positive ht hu
  constructor
  · rw [conditionNumber, coupled_conditionNumber ha hc]
    exact (scaledKappa_eq_normal ht hu).symm
  constructor
  · rw [firstAmplification, rhs_norm, div_one, coupled_operatorNorm ha hc,
      coupled_first_norm ha hc]
    exact (xiCertificate_eq ht hu).symm
  · rw [filteringParameter, coupled_operatorNorm ha hc, coupled_second_norm ha hc,
      coupled_first_norm ha hc, scaledRhoCertificate_eq ht hu]
    have hd : 2*thetaOne t+theta t ≠ 0 := by positivity
    have h5 : Real.sqrt 5 ≠ 0 := by positivity
    field_simp [ne_of_gt hc, hd, h5]

/-- The three headline coupled limits, with actual induced norms. -/
theorem coupled_parameter_limits :
    Tendsto (fun μ => μ^2 * conditionNumber (paperH μ)) (𝓝[>] 0) (𝓝 (1/2)) ∧
    Tendsto (fun μ => firstAmplification (paperH μ)) (𝓝[>] 0) (𝓝 (Real.sqrt 5/2)) ∧
    Tendsto (fun μ => μ^2 * filteringParameter (paperH μ)) (𝓝[>] 0)
      (𝓝 (1/(2*Real.sqrt 5))) := by
  have he : ∀ μ : ℝ, 0 < μ →
      μ^2 * conditionNumber (paperH μ) = scaledKappa (paperT μ) ∧
      firstAmplification (paperH μ) = xiCertificate (paperT μ) ∧
      μ^2 * filteringParameter (paperH μ) = scaledRhoCertificate (paperT μ) := by
    intro μ hμ
    have h := coupled_parameter_certificates (paperT_domain hμ).1 (paperT_domain hμ).2
    simpa only [paperT_parameter hμ, paperH] using h
  constructor
  · apply (paper_certificates_limits.1.mono_left nhdsWithin_le_nhds).congr'
    filter_upwards [self_mem_nhdsWithin] with μ hμ
    exact (he μ hμ).1.symm
  constructor
  · apply (paper_certificates_limits.2.1.mono_left nhdsWithin_le_nhds).congr'
    filter_upwards [self_mem_nhdsWithin] with μ hμ
    exact (he μ hμ).2.1.symm
  · apply (paper_certificates_limits.2.2.1.mono_left nhdsWithin_le_nhds).congr'
    filter_upwards [self_mem_nhdsWithin] with μ hμ
    exact (he μ hμ).2.2.symm

/-- The decoupled witness has exact norm-tight parameters in the small-μ regime. -/
theorem decoupled_parameters {μ : ℝ} (hμ : 0 < μ) (hu : 2 * μ ^ 2 ≤ 1) :
    conditionNumber (decoupledH μ) = 1/(2*μ^2) ∧
    firstAmplification (decoupledH μ) = 1 ∧ filteringParameter (decoupledH μ) = 1 := by
  constructor
  · exact decoupled_conditionNumber hμ hu
  obtain ⟨hf,hs⟩ := decoupled_inverse_norms hμ
  constructor
  · rw [firstAmplification, rhs_norm, div_one, decoupled_operatorNorm hμ hu, hf]
    exact inv_mul_cancel₀ (ne_of_gt hμ)
  · rw [filteringParameter, decoupled_operatorNorm hμ hu, hf, hs]
    field_simp

def paperSlowVector (μ : ℝ) :=
  slowEigenvector ((1-paperT μ)^2) ((paperT μ)^2)

/-- This is a nonzero eigenvector for the smaller eigenvalue of the actual normal matrix. -/
theorem paperSlowVector_eigen {μ : ℝ} (hμ : 0 < μ) :
    paperSlowVector μ ≠ 0 ∧
    paperH μ *ᵥ paperSlowVector μ =
      smallRoot (thetaOne (paperT μ)) (theta (paperT μ)) • paperSlowVector μ := by
  have ht := (paperT_domain hμ).1
  constructor
  · exact slowEigenvector_ne_zero (ne_of_gt (sq_pos_of_pos ht))
  have he : paperH μ = μ⁻¹ • coupledH ((1-paperT μ)^2) ((paperT μ)^2) := by
    unfold paperH coupledH thetaOne theta
    rw [paperT_parameter hμ]
    ext i j; fin_cases i <;> fin_cases j <;> simp <;> ring
  rw [he, Matrix.smul_mulVec, paperSlowVector, slowEigenvector_eigen, smul_smul]
  unfold thetaOne theta
  rw [paperT_parameter hμ, smallRoot_div _ _ hμ]
  congr 1
  ring

/-- The absolute projection of the normalized solution onto its slow eigenspace. -/
def slowSolutionAmplitude (μ : ℝ) : ℝ :=
  |((vectorNorm ((paperH μ)⁻¹ *ᵥ rhs))⁻¹ • ((paperH μ)⁻¹ *ᵥ rhs)) ⬝ᵥ
      paperSlowVector μ / vectorNorm (paperSlowVector μ)|

theorem slowSolutionAmplitude_eq {μ : ℝ} (hμ : 0 < μ) :
    slowSolutionAmplitude μ = slowAmplitude (paperT μ) := by
  obtain ⟨ha,hc⟩ := theta_positive (paperT_domain hμ).1 (paperT_domain hμ).2
  unfold slowSolutionAmplitude paperH
  rw [coupled_normalized_direction ha hc]
  exact (slowAmplitude_eq_overlap (paperT μ)).symm

/-- The finite-μ slow eigenspace rotates; its amplitude has this limiting value. -/
theorem slowSolutionAmplitude_limit :
    Tendsto slowSolutionAmplitude (𝓝[>] 0) (𝓝 (1/Real.sqrt 5)) := by
  apply (paper_certificates_limits.2.2.2.mono_left nhdsWithin_le_nhds).congr'
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  exact (slowSolutionAmplitude_eq hμ).symm

end
end QipmFormal.Coupling.Witnesses
