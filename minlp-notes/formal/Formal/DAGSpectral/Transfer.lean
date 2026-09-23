import Formal.DAGSpectral.PSDAlgebra

namespace DAGSpectral

/-- Transfer from a uniformly approximating information graph. This theorem
assumes the upstream sandwich; it does not construct the stochastic graph. -/
theorem relative_cover_transfer {n : ℕ} {J L Jhat Lhat : RealMatrix n}
    {η δ : ℝ} (hη0 : 0 ≤ η) (hη1 : η < 1) (hδ0 : 0 ≤ δ) (hδ1 : δ < 1)
    (hP : RelativeSandwich δ J L) (hH : RelativeSandwich δ Jhat Lhat)
    (hC : RelativeSandwich η L Lhat) :
    Loewner (((1-η)*(1-δ)/(1+δ)) • J) Jhat ∧
      Loewner Jhat (((1+η)*(1+δ)/(1-δ)) • J) := by
  have hp : 0 < 1+δ := by linarith
  have hm : 0 < 1-δ := by linarith
  have hlo := ((hP.1.smul (show 0 ≤ 1-η by linarith)).trans hC.1).trans hH.2
  have hup := (hH.1.trans hC.2).trans (hP.2.smul (show 0 ≤ 1+η by linarith))
  constructor
  · have hh := hlo.smul (inv_nonneg.mpr hp.le)
    simpa only [smul_smul, inv_mul_cancel₀ hp.ne', one_smul,
      ← div_eq_inv_mul] using hh
  · have hh := hup.smul (inv_nonneg.mpr hm.le)
    simpa only [smul_smul, inv_mul_cancel₀ hm.ne', one_smul,
      ← div_eq_inv_mul] using hh

theorem transfer_factors_accuracy {ε δ : ℝ} (hε0 : 0 < ε) (hε1 : ε < 1)
    (hδ0 : 0 ≤ δ) (hδ : δ ≤ ε / 8) :
    1 - ((1-ε / 4)*(1-δ)/(1+δ)) ≤ ε/2 ∧
      ((1+ε / 4)*(1+δ)/(1-δ)) - 1 ≤ 17*ε/28 := by
  have hp : 0 < 1+δ := by linarith
  have hm : 0 < 1-δ := by linarith
  have hprod : ε*δ ≤ ε / 8 := by nlinarith
  constructor
  · have hd : (1-ε / 4)*(1-δ)/(1+δ) ≥ 1-ε/2 := by
      apply (le_div_iff₀ hp).mpr
      nlinarith [mul_nonneg hε0.le hδ0]
    linarith
  · have hd : (1+ε / 4)*(1+δ)/(1-δ) ≤ 1+17*ε/28 := by
      apply (div_le_iff₀ hm).mpr
      nlinarith
    linarith

theorem relative_cover_transfer_accuracy {n : ℕ} {J L Jhat Lhat : RealMatrix n}
    (hJ : J.PosSemidef) {ε δ : ℝ} (hε0 : 0 < ε) (hε1 : ε < 1)
    (hδ0 : 0 ≤ δ) (hδ : δ ≤ ε / 8)
    (hP : RelativeSandwich δ J L) (hH : RelativeSandwich δ Jhat Lhat)
    (hC : RelativeSandwich (ε / 4) L Lhat) : RelativeSandwich ε J Jhat := by
  have ht := relative_cover_transfer (η := ε / 4) (by positivity) (by linarith)
    hδ0 (by linarith) hP hH hC
  have hf := transfer_factors_accuracy hε0 hε1 hδ0 hδ
  exact ⟨(psd_smul_mono hJ (by linarith)).trans ht.1,
    ht.2.trans (psd_smul_mono hJ (by linarith))⟩

end DAGSpectral
