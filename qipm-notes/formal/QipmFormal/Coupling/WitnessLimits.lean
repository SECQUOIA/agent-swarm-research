import QipmFormal.Coupling.Witnesses
import Mathlib.Analysis.InnerProductSpace.PiL2

/-! # Spectral and norm certificates for the coupled witness

These formulas use the rescaled normal matrix `μ H`; consequently its largest
root tends to one without a divergent expression at the endpoint. The norm
ratios below use the Euclidean vector norm. The scalar spectral certificates
are stated explicitly, without identifying Lean's entrywise matrix norm with
an operator norm.
-/
namespace QipmFormal.Coupling.Witnesses
noncomputable section
open Matrix Filter
open scoped Topology

def largeRoot (a c : ℝ) : ℝ := (a + 3*c + Real.sqrt ((a-c)^2+4*c^2))/2
def smallRoot (a c : ℝ) : ℝ := (a + 3*c - Real.sqrt ((a-c)^2+4*c^2))/2

theorem root_sum (a c : ℝ) : largeRoot a c + smallRoot a c = a+3*c := by
  unfold largeRoot smallRoot; ring

theorem root_product (a c : ℝ) :
    largeRoot a c * smallRoot a c = c*(2*a+c) := by
  have h := Real.sq_sqrt (show 0 ≤ (a-c)^2+4*c^2 by positivity)
  unfold largeRoot smallRoot
  nlinarith

theorem root_order (a c : ℝ) : smallRoot a c ≤ largeRoot a c := by
  unfold smallRoot largeRoot
  have := Real.sqrt_nonneg ((a-c)^2+4*c^2)
  linarith

theorem largeRoot_pos {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    0 < largeRoot a c := by
  unfold largeRoot
  have := Real.sqrt_nonneg ((a-c)^2+4*c^2)
  positivity

theorem smallRoot_pos {a c : ℝ} (ha : 0 < a) (hc : 0 < c) :
    0 < smallRoot a c := by
  have hl := largeRoot_pos ha hc
  have hp := root_product a c
  have : 0 < c*(2*a+c) := by positivity
  nlinarith

/-- Both displayed roots are eigenvalues: the characteristic determinant vanishes. -/
theorem roots_characteristic (a c : ℝ) :
    (coupledH a c - largeRoot a c • (1 : Matrix (Fin 2) (Fin 2) ℝ)).det = 0 ∧
    (coupledH a c - smallRoot a c • (1 : Matrix (Fin 2) (Fin 2) ℝ)).det = 0 := by
  have hs := root_sum a c
  have hp := root_product a c
  constructor
  · simp [Matrix.det_fin_two, coupledH]
    nlinarith [congrArg (fun x : ℝ => x * largeRoot a c) hs]
  · simp [Matrix.det_fin_two, coupledH]
    nlinarith [congrArg (fun x : ℝ => x * smallRoot a c) hs]

theorem largeRoot_div (a c : ℝ) {μ : ℝ} (hμ : 0 < μ) :
    largeRoot (a/μ) (c/μ) = largeRoot a c / μ := by
  have he : (a/μ-c/μ)^2+4*(c/μ)^2 = ((a-c)^2+4*c^2)/μ^2 := by ring
  unfold largeRoot
  rw [he, Real.sqrt_div (by positivity), Real.sqrt_sq (le_of_lt hμ)]
  ring

theorem smallRoot_div (a c : ℝ) {μ : ℝ} (hμ : 0 < μ) :
    smallRoot (a/μ) (c/μ) = smallRoot a c / μ := by
  have he : (a/μ-c/μ)^2+4*(c/μ)^2 = ((a-c)^2+4*c^2)/μ^2 := by ring
  unfold smallRoot
  rw [he, Real.sqrt_div (by positivity), Real.sqrt_sq (le_of_lt hμ)]
  ring

def rescaledLarge (t : ℝ) := largeRoot ((1-t)^2) (t^2)
def regularRatio (t : ℝ) := 2*(1-t)/(2-3*t)
def scaledKappa (t : ℝ) :=
  (regularRatio t)^2 * (rescaledLarge t)^2 / (2*(1-t)^2+t^2)
def xiCertificate (t : ℝ) :=
  rescaledLarge t * Real.sqrt 5 / (2*(1-t)^2+t^2)
def scaledRhoCertificate (t : ℝ) :=
  rescaledLarge t * (regularRatio t)^2 *
    Real.sqrt (25*t^4 + ((1-t)^2+3*t^2)^2) /
      (Real.sqrt 5 * (2*(1-t)^2+t^2))

theorem rescaledLarge_limit : Tendsto rescaledLarge (𝓝 0) (𝓝 1) := by
  have h : ContinuousAt rescaledLarge 0 := by
    unfold rescaledLarge largeRoot
    fun_prop
  simpa [rescaledLarge, largeRoot] using h.tendsto

theorem regularRatio_limit : Tendsto regularRatio (𝓝 0) (𝓝 1) := by
  have h : ContinuousAt regularRatio 0 := by
    unfold regularRatio
    fun_prop (disch := norm_num)
  simpa [regularRatio] using h.tendsto

theorem scaledKappa_limit : Tendsto scaledKappa (𝓝 0) (𝓝 (1/2)) := by
  have h : ContinuousAt scaledKappa 0 := by
    unfold scaledKappa regularRatio rescaledLarge largeRoot
    fun_prop (disch := norm_num)
  simpa [scaledKappa, regularRatio, rescaledLarge, largeRoot] using h.tendsto

theorem xiCertificate_limit :
    Tendsto xiCertificate (𝓝 0) (𝓝 (Real.sqrt 5/2)) := by
  have h : ContinuousAt xiCertificate 0 := by
    unfold xiCertificate rescaledLarge largeRoot
    fun_prop (disch := norm_num)
  simpa [xiCertificate, rescaledLarge, largeRoot] using h.tendsto

theorem scaledRhoCertificate_limit :
    Tendsto scaledRhoCertificate (𝓝 0) (𝓝 (1/(2*Real.sqrt 5))) := by
  have h : ContinuousAt scaledRhoCertificate 0 := by
    unfold scaledRhoCertificate rescaledLarge largeRoot regularRatio
    fun_prop (disch := norm_num)
  convert h.tendsto using 1
  norm_num [scaledRhoCertificate, rescaledLarge, largeRoot, centerParameter, regularRatio]
  ring

/-- The regularized condition number is exactly `μ² λ_max / λ_min`. -/
theorem scaledKappa_eq {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    scaledKappa t = (centerParameter t)^2 *
      (largeRoot ((1-t)^2) (t^2) / smallRoot ((1-t)^2) (t^2)) := by
  have ha : 0 < (1-t)^2 := sq_pos_of_pos (by linarith)
  have hc : 0 < t^2 := sq_pos_of_pos ht
  have hl := largeRoot_pos ha hc
  have hs := smallRoot_pos ha hc
  have hp := root_product ((1-t)^2) (t^2)
  have hd : 2*(1-t)^2+t^2 ≠ 0 := by positivity
  have ht0 : t ≠ 0 := ne_of_gt ht
  have hh : 2-3*t ≠ 0 := by linarith
  have he : smallRoot ((1-t)^2) (t^2) =
      t^2*(2*(1-t)^2+t^2) / largeRoot ((1-t)^2) (t^2) := by
    apply (eq_div_iff (ne_of_gt hl)).mpr
    nlinarith [hp]
  rw [he]
  unfold scaledKappa regularRatio centerParameter rescaledLarge
  field_simp [ne_of_gt hl, hd, hh, ht0]

/-- The continuous certificate is the norm-tight first-inverse formula. -/
theorem xiCertificate_eq {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    xiCertificate t = largeRoot (thetaOne t) (theta t) *
      (Real.sqrt 5 / (2*thetaOne t+theta t)) := by
  have hμ := centerParameter_pos ht hu
  have hd : 2*(1-t)^2+t^2 ≠ 0 := by positivity
  unfold thetaOne theta
  rw [largeRoot_div _ _ hμ]
  unfold xiCertificate rescaledLarge
  field_simp [ne_of_gt hμ, hd]

/-- The continuous certificate is `μ²` times the second/first inverse norm ratio. -/
theorem scaledRhoCertificate_eq {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    scaledRhoCertificate t = (centerParameter t)^2 *
      (largeRoot (thetaOne t) (theta t) *
        (Real.sqrt (25*(theta t)^2+(thetaOne t+3*theta t)^2) /
          (theta t*(2*thetaOne t+theta t)*Real.sqrt 5))) := by
  have hμ := centerParameter_pos ht hu
  have ht0 : t ≠ 0 := ne_of_gt ht
  have hd : 2*(1-t)^2+t^2 ≠ 0 := by positivity
  have h5 : Real.sqrt 5 ≠ 0 := by positivity
  have he : 25*(t^2/centerParameter t)^2+
      ((1-t)^2/centerParameter t+3*(t^2/centerParameter t))^2 =
      (25*t^4+((1-t)^2+3*t^2)^2)/(centerParameter t)^2 := by ring
  unfold thetaOne theta
  rw [largeRoot_div _ _ hμ, he, Real.sqrt_div (by positivity),
    Real.sqrt_sq (le_of_lt hμ)]
  have hm : centerParameter t = t * regularRatio t := by
    unfold centerParameter regularRatio; ring
  unfold scaledRhoCertificate rescaledLarge
  rw [hm]
  have hr : regularRatio t ≠ 0 := by
    intro h
    rw [hm, h, mul_zero] at hμ
    exact (lt_irrefl 0 hμ)
  field_simp [ht0, hr, hd, h5]

def slowEigenvector (a c : ℝ) : Fin 2 → ℝ := ![-c, a+c-smallRoot a c]

theorem slowEigenvector_eigen (a c : ℝ) :
    coupledH a c *ᵥ slowEigenvector a c = smallRoot a c • slowEigenvector a c := by
  have hs := root_sum a c
  have hp := root_product a c
  have he := congrArg (fun x : ℝ => x * smallRoot a c) hs
  ext i; fin_cases i <;>
    simp [coupledH, slowEigenvector, mulVec, dotProduct, Fin.sum_univ_succ] <;>
    nlinarith

theorem slowEigenvector_ne_zero {a c : ℝ} (hc : c ≠ 0) :
    slowEigenvector a c ≠ 0 := by
  intro h
  have h0 := congrFun h 0
  change -c = 0 at h0
  exact hc (neg_eq_zero.mp h0)

/-- Absolute overlap of `(2,-1)/√5` with the normalized slow eigenvector. -/
def slowAmplitude (t : ℝ) :=
  |(-2*t^2 - ((1-t)^2+t^2-smallRoot ((1-t)^2) (t^2))) /
    (Real.sqrt 5 * Real.sqrt (t^4+
      ((1-t)^2+t^2-smallRoot ((1-t)^2) (t^2))^2))|

theorem slowAmplitude_limit :
    Tendsto slowAmplitude (𝓝 0) (𝓝 (1/Real.sqrt 5)) := by
  have h : ContinuousAt slowAmplitude 0 := by
    unfold slowAmplitude smallRoot
    fun_prop (disch := norm_num)
  convert h.tendsto using 1
  norm_num [slowAmplitude, smallRoot, abs_div, abs_of_nonneg (Real.sqrt_nonneg _)]

/-- The amplitude certificate is the actual normalized eigenvector overlap. -/
theorem slowAmplitude_eq_overlap (t : ℝ) :
    slowAmplitude t =
      |(![2/Real.sqrt 5, -1/Real.sqrt 5] ⬝ᵥ
        slowEigenvector ((1-t)^2) (t^2)) /
          vectorNorm (slowEigenvector ((1-t)^2) (t^2))| := by
  unfold slowAmplitude slowEigenvector
  rw [vectorNorm_pair]
  simp only [dotProduct, Fin.sum_univ_succ, Fin.isValue, Matrix.cons_val_zero,
    Matrix.cons_val_succ, Fin.sum_univ_zero, add_zero]
  congr 1
  have he : (-t^2)^2 + ((1-t)^2+t^2-smallRoot ((1-t)^2) (t^2))^2 =
      t^4 + ((1-t)^2+t^2-smallRoot ((1-t)^2) (t^2))^2 := by ring
  rw [he]
  ring

/-- The condition certificate uses the roots of the actual unscaled normal matrix. -/
theorem scaledKappa_eq_normal {t : ℝ} (ht : 0 < t) (hu : t < 2 / 3) :
    scaledKappa t = (centerParameter t)^2 *
      (largeRoot (thetaOne t) (theta t) / smallRoot (thetaOne t) (theta t)) := by
  rw [scaledKappa_eq ht hu]
  unfold thetaOne theta
  rw [largeRoot_div _ _ (centerParameter_pos ht hu),
    smallRoot_div _ _ (centerParameter_pos ht hu)]
  congr 1
  exact (div_div_div_cancel_right₀ (ne_of_gt (centerParameter_pos ht hu)) _ _).symm

/-- All scalar certificates also converge along the original radical parameterization. -/
theorem paper_certificates_limits :
    Tendsto (fun μ => scaledKappa (paperT μ)) (𝓝 0) (𝓝 (1/2)) ∧
    Tendsto (fun μ => xiCertificate (paperT μ)) (𝓝 0) (𝓝 (Real.sqrt 5/2)) ∧
    Tendsto (fun μ => scaledRhoCertificate (paperT μ)) (𝓝 0)
      (𝓝 (1/(2*Real.sqrt 5))) ∧
    Tendsto (fun μ => slowAmplitude (paperT μ)) (𝓝 0) (𝓝 (1/Real.sqrt 5)) :=
  ⟨scaledKappa_limit.comp paperT_tendsto_zero,
    xiCertificate_limit.comp paperT_tendsto_zero,
    scaledRhoCertificate_limit.comp paperT_tendsto_zero,
    slowAmplitude_limit.comp paperT_tendsto_zero⟩

end
end QipmFormal.Coupling.Witnesses
