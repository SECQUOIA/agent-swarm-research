import QipmFormal.Coupling.Bounds
import Mathlib.Analysis.Asymptotics.Theta
import QipmFormal.Coupling.Block
import Mathlib.Analysis.Normed.Lp.ProdLp

/-! # Operator-norm scales of the exact-center blocks

The block formulas are initially represented on the usual product space. Before
any spectral norm is taken they are transported to `WithLp 2 (U × K)`, whose
norm is exactly `blockNorm`. Thus the norm results concern the orthogonal-sum
norm used for the inverse vectors, rather than the maximum product norm.
-/
open Filter Asymptotics Topology

namespace QipmFormal.Coupling
noncomputable section
variable {U K : Type*} [NormedAddCommGroup U] [NormedSpace ℝ U]
  [NormedAddCommGroup K] [NormedSpace ℝ K]

/-- Continuous block matrix with its four entries in their natural spaces. -/
def blockCLM (A : U →L[ℝ] U) (B : K →L[ℝ] U)
    (C : U →L[ℝ] K) (D : K →L[ℝ] K) : (U × K) →L[ℝ] (U × K) :=
  (A.comp (ContinuousLinearMap.fst ℝ U K) +
    B.comp (ContinuousLinearMap.snd ℝ U K)).prod
  (C.comp (ContinuousLinearMap.fst ℝ U K) +
    D.comp (ContinuousLinearMap.snd ℝ U K))

@[simp] theorem blockCLM_apply (A : U →L[ℝ] U) (B : K →L[ℝ] U)
    (C : U →L[ℝ] K) (D : K →L[ℝ] K) (z : U × K) :
    blockCLM A B C D z = (A z.1 + B z.2, C z.1 + D z.2) := rfl

/-- Transport a block map to the actual orthogonal-sum norm. -/
def euclideanBlocks : ((U × K) →L[ℝ] (U × K)) ≃L[ℝ]
    (WithLp 2 (U × K) →L[ℝ] WithLp 2 (U × K)) :=
  (WithLp.prodContinuousLinearEquiv 2 ℝ U K).symm.arrowCongr
    (WithLp.prodContinuousLinearEquiv 2 ℝ U K).symm

omit [NormedSpace ℝ U] [NormedSpace ℝ K] in
@[simp] theorem norm_euclideanBlock (z : WithLp 2 (U × K)) :
    ‖z‖ = blockNorm (WithLp.ofLp z).1 (WithLp.ofLp z).2 :=
  WithLp.prod_norm_eq_of_L2 z

omit [NormedSpace ℝ U] [NormedSpace ℝ K] in
/-- Explicit equivalence constants also make the product-norm distinction visible. -/
theorem blockNorm_equivalent (z : U × K) :
    ‖z‖ ≤ blockNorm z.1 z.2 ∧ blockNorm z.1 z.2 ≤ 2 * ‖z‖ := by
  constructor
  · exact max_le (norm_le_blockNorm_left _ _) (norm_le_blockNorm_right _ _)
  · exact (blockNorm_le_add _ _).trans (by
      have h1 : ‖z.1‖ ≤ ‖z‖ := le_max_left _ _
      have h2 : ‖z.2‖ ≤ ‖z‖ := le_max_right _ _
      linarith)

/-- A nonzero limit of the scaled operator proves its norm scale. -/
theorem norm_theta_inv_of_scaled_tendsto
    {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]
    {l : Filter ℝ} {A : ℝ → V} {A₀ : V}
    (hμ : ∀ᶠ μ in l, 0 < μ)
    (hA : Tendsto (fun μ => μ • A μ) l (𝓝 A₀)) (hA₀ : A₀ ≠ 0) :
    (fun μ => ‖A μ‖) =Θ[l] (fun μ => μ⁻¹) := by
  have ht : Tendsto (fun μ => ‖A μ‖ / μ⁻¹) l (𝓝 ‖A₀‖) := by
    apply hA.norm.congr'
    filter_upwards [hμ] with μ hμ
    simp [norm_smul, Real.norm_eq_abs, abs_of_pos hμ, mul_comm]
  exact (isTheta_of_div_tendsto_nhds_ne_zero ht (norm_ne_zero_iff.mpr hA₀)).symm

/-- The exact-center operator in continuous linear-map form. -/
def newtonCLM (μ : ℝ) (C D : U →L[ℝ] U) (F : U →L[ℝ] K)
    (T : K →L[ℝ] U) (E : K →L[ℝ] K) : (U × K) →L[ℝ] (U × K) :=
  blockCLM (μ⁻¹ • C + μ • D) (μ • T) (μ • F) (μ • E)

/-- Elimination formula: J is E⁻¹ and R is the inverse Schur factor. -/
def inverseCLM (μ : ℝ) (F : U →L[ℝ] K) (T : K →L[ℝ] U)
    (J : K →L[ℝ] K) (R : U →L[ℝ] U) : (U × K) →L[ℝ] (U × K) :=
  blockCLM (μ • R) (-μ • R.comp (T.comp J))
    (-μ • J.comp (F.comp R))
    (μ⁻¹ • J + μ • J.comp (F.comp (R.comp (T.comp J))))

lemma scaled_newtonCLM (μ : ℝ) (hμ : μ ≠ 0) (C D : U →L[ℝ] U)
    (F : U →L[ℝ] K) (T : K →L[ℝ] U) (E : K →L[ℝ] K) :
    μ • newtonCLM μ C D F T E =
      blockCLM (C + μ ^ 2 • D) (μ ^ 2 • T) (μ ^ 2 • F) (μ ^ 2 • E) := by
  ext z <;> simp [newtonCLM, blockCLM, smul_add, smul_smul, hμ, pow_two]

lemma scaled_inverseCLM (μ : ℝ) (hμ : μ ≠ 0)
    (F : U →L[ℝ] K) (T : K →L[ℝ] U) (J : K →L[ℝ] K) (R : U →L[ℝ] U) :
    μ • inverseCLM μ F T J R =
      blockCLM (μ ^ 2 • R) (-μ ^ 2 • R.comp (T.comp J))
        (-μ ^ 2 • J.comp (F.comp R))
        (J + μ ^ 2 • J.comp (F.comp (R.comp (T.comp J)))) := by
  ext z <;> simp [inverseCLM, blockCLM, smul_add, smul_smul, hμ, pow_two]

lemma continuousAt_blockCLM {A : ℝ → U →L[ℝ] U} {B : ℝ → K →L[ℝ] U}
    {C : ℝ → U →L[ℝ] K} {D : ℝ → K →L[ℝ] K}
    (hA : ContinuousAt A 0) (hB : ContinuousAt B 0)
    (hC : ContinuousAt C 0) (hD : ContinuousAt D 0) :
    ContinuousAt (fun μ => blockCLM (A μ) (B μ) (C μ) (D μ)) 0 := by
  change ContinuousAt (fun μ => ContinuousLinearMap.prodL ℝ
    ((A μ).comp (ContinuousLinearMap.fst ℝ U K) +
      (B μ).comp (ContinuousLinearMap.snd ℝ U K),
     (C μ).comp (ContinuousLinearMap.fst ℝ U K) +
      (D μ).comp (ContinuousLinearMap.snd ℝ U K))) 0
  exact (ContinuousLinearMap.prodL ℝ).continuous.continuousAt.comp
    ((hA.clm_comp continuousAt_const |>.add (hB.clm_comp continuousAt_const)).prodMk
      (hC.clm_comp continuousAt_const |>.add (hD.clm_comp continuousAt_const)))


/-- The continuous elimination formula agrees with the inverse constructed in
`Block`, so its norm is a norm of the actual inverse. -/
theorem inverseCLM_eq_blockEquiv_symm (μ : ℝ) (hμ : μ ≠ 0)
    (C D : U →L[ℝ] U) (F : U →L[ℝ] K) (T : K →L[ℝ] U)
    (E : K ≃L[ℝ] K) (S : U ≃L[ℝ] U)
    (hS : HasSchurFactor μ C.toLinearMap D.toLinearMap F.toLinearMap
      T.toLinearMap E.toLinearEquiv S.toLinearEquiv) (z : U × K) :
    inverseCLM μ F T E.symm.toContinuousLinearMap S.symm.toContinuousLinearMap z =
      (blockEquiv μ C.toLinearMap D.toLinearMap F.toLinearMap T.toLinearMap
        E.toLinearEquiv S.toLinearEquiv hμ hS).symm z := by
  rw [blockEquiv_symm_apply]
  ext <;> simp [inverseCLM, blockSolve, map_sub, map_smul]
  <;> module

/-- Agreement with the original algebraic block model. -/
theorem newtonCLM_eq_blockOperator (μ : ℝ)
    (C D : U →L[ℝ] U) (F : U →L[ℝ] K) (T : K →L[ℝ] U)
    (E : K ≃L[ℝ] K) (z : U × K) :
    newtonCLM μ C D F T E.toContinuousLinearMap z =
      blockOperator μ C.toLinearMap D.toLinearMap F.toLinearMap T.toLinearMap
        E.toLinearEquiv z := by
  ext <;> simp [newtonCLM, blockOperator, smul_add, add_assoc]

/-- Ring inversion of the genuine Newton map equals the Schur elimination map. -/
theorem ringInverse_newtonCLM (μ : ℝ) (hμ : μ ≠ 0)
    (C D : U →L[ℝ] U) (F : U →L[ℝ] K) (T : K →L[ℝ] U)
    (E : K ≃L[ℝ] K) (S : U ≃L[ℝ] U)
    (hS : HasSchurFactor μ C.toLinearMap D.toLinearMap F.toLinearMap
      T.toLinearMap E.toLinearEquiv S.toLinearEquiv) :
    Ring.inverse (newtonCLM μ C D F T E.toContinuousLinearMap) =
      inverseCLM μ F T E.symm.toContinuousLinearMap S.symm.toContinuousLinearMap := by
  let H := newtonCLM μ C D F T E.toContinuousLinearMap
  let I := inverseCLM μ F T E.symm.toContinuousLinearMap S.symm.toContinuousLinearMap
  let e := blockEquiv μ C.toLinearMap D.toLinearMap F.toLinearMap T.toLinearMap
    E.toLinearEquiv S.toLinearEquiv hμ hS
  have hH (z : U × K) : H z = e z := newtonCLM_eq_blockOperator μ C D F T E z
  have hI (z : U × K) : I z = e.symm z :=
    inverseCLM_eq_blockEquiv_symm μ hμ C D F T E S hS z
  have hHI : H * I = 1 := by
    apply ContinuousLinearMap.ext
    intro z
    change H (I z) = z
    rw [hH, hI, e.apply_symm_apply]
  have hIH : I * H = 1 := by
    apply ContinuousLinearMap.ext
    intro z
    change I (H z) = z
    rw [hI, hH, e.symm_apply_apply]
  exact Ring.inverse_unit (Units.mk H I hHI hIH)

/-- The singularity of H is entirely removed after multiplication by μ. -/
theorem scaled_newtonCLM_tendsto
    {C D : ℝ → U →L[ℝ] U} {F : ℝ → U →L[ℝ] K}
    {T : ℝ → K →L[ℝ] U} {E : ℝ → K →L[ℝ] K}
    (hC : ContinuousAt C 0) (hD : ContinuousAt D 0)
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0) (hE : ContinuousAt E 0) :
    Tendsto (fun μ => μ • newtonCLM μ (C μ) (D μ) (F μ) (T μ) (E μ))
      (𝓝[>] (0 : ℝ)) (𝓝 (blockCLM (C 0) 0 0 0)) := by
  have hc : ContinuousAt (fun μ => blockCLM (C μ + μ ^ 2 • D μ)
      (μ ^ 2 • T μ) (μ ^ 2 • F μ) (μ ^ 2 • E μ)) 0 := by
    apply continuousAt_blockCLM <;> fun_prop
  have ht := hc.tendsto.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow, zero_smul,
    add_zero] at ht
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  exact (scaled_newtonCLM μ (ne_of_gt hμ) _ _ _ _ _).symm

/-- The scaled inverse tends to its inactive diagonal block. -/
theorem scaled_inverseCLM_tendsto
    {F : ℝ → U →L[ℝ] K} {T : ℝ → K →L[ℝ] U}
    {J : ℝ → K →L[ℝ] K} {R : ℝ → U →L[ℝ] U}
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0)
    (hJ : ContinuousAt J 0) (hR : ContinuousAt R 0) :
    Tendsto (fun μ => μ • inverseCLM μ (F μ) (T μ) (J μ) (R μ))
      (𝓝[>] (0 : ℝ)) (𝓝 (blockCLM 0 0 0 (J 0))) := by
  have hc : ContinuousAt (fun μ =>
      blockCLM (μ ^ 2 • R μ) (-μ ^ 2 • (R μ).comp ((T μ).comp (J μ)))
        (-μ ^ 2 • (J μ).comp ((F μ).comp (R μ)))
        (J μ + μ ^ 2 • (J μ).comp ((F μ).comp ((R μ).comp ((T μ).comp (J μ))))))
      0 := by
    apply continuousAt_blockCLM <;> fun_prop
  have ht := hc.tendsto.mono_left (nhdsWithin_le_nhds (s := Set.Ioi (0 : ℝ)))
  simp only [ne_eq, OfNat.ofNat_ne_zero, not_false_eq_true, zero_pow, zero_smul,
    neg_zero, add_zero] at ht
  apply ht.congr'
  filter_upwards [self_mem_nhdsWithin] with μ hμ
  exact (scaled_inverseCLM μ (ne_of_gt hμ) _ _ _ _).symm


lemma blockCLM_active_ne_zero {C : U →L[ℝ] U} (hC : C ≠ 0) :
    blockCLM C (0 : K →L[ℝ] U) 0 0 ≠ 0 := by
  intro hz
  apply hC
  ext u
  have hh := congrArg (fun A : (U × K) →L[ℝ] (U × K) => (A (u, 0)).1) hz
  simpa using hh

lemma blockCLM_inactive_ne_zero {J : K →L[ℝ] K} (hJ : J ≠ 0) :
    blockCLM (0 : U →L[ℝ] U) 0 0 J ≠ 0 := by
  intro hz
  apply hJ
  ext v
  have hh := congrArg (fun A : (U × K) →L[ℝ] (U × K) => (A (0, v)).2) hz
  simpa using hh

/-- The spectral norm of the exact-center operator is Θ(μ⁻¹), in the
orthogonal-sum norm. Nontriviality of the active limit is explicit. -/
theorem newton_norm_theta
    {C D : ℝ → U →L[ℝ] U} {F : ℝ → U →L[ℝ] K}
    {T : ℝ → K →L[ℝ] U} {E : ℝ → K →L[ℝ] K}
    (hC : ContinuousAt C 0) (hD : ContinuousAt D 0)
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0) (hE : ContinuousAt E 0)
    (hC₀ : C 0 ≠ 0) :
    (fun μ => ‖euclideanBlocks (newtonCLM μ (C μ) (D μ) (F μ) (T μ) (E μ))‖)
      =Θ[𝓝[>] (0 : ℝ)] (fun μ => μ⁻¹) := by
  apply norm_theta_inv_of_scaled_tendsto (l := 𝓝[>] (0 : ℝ))
    (show ∀ᶠ μ in 𝓝[>] (0 : ℝ), 0 < μ from self_mem_nhdsWithin)
  · have ht := euclideanBlocks.continuous.tendsto
      (blockCLM (C 0) (0 : K →L[ℝ] U) 0 0) |>.comp
        (scaled_newtonCLM_tendsto hC hD hF hT hE)
    simpa [Function.comp_def] using ht
  · exact (map_ne_zero_iff euclideanBlocks euclideanBlocks.injective).mpr
      (blockCLM_active_ne_zero hC₀)

/-- The inactive block supplies the inverse norm Θ(μ⁻¹). The lemma
`inverseCLM_eq_blockEquiv_symm` connects this formula to the actual inverse. -/
theorem inverse_norm_theta
    {F : ℝ → U →L[ℝ] K} {T : ℝ → K →L[ℝ] U}
    {J : ℝ → K →L[ℝ] K} {R : ℝ → U →L[ℝ] U}
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0)
    (hJ : ContinuousAt J 0) (hR : ContinuousAt R 0) (hJ₀ : J 0 ≠ 0) :
    (fun μ => ‖euclideanBlocks (inverseCLM μ (F μ) (T μ) (J μ) (R μ))‖)
      =Θ[𝓝[>] (0 : ℝ)] (fun μ => μ⁻¹) := by
  apply norm_theta_inv_of_scaled_tendsto (l := 𝓝[>] (0 : ℝ))
    (show ∀ᶠ μ in 𝓝[>] (0 : ℝ), 0 < μ from self_mem_nhdsWithin)
  · have ht := euclideanBlocks.continuous.tendsto
      (blockCLM (0 : U →L[ℝ] U) 0 0 (J 0)) |>.comp
        (scaled_inverseCLM_tendsto hF hT hJ hR)
    simpa [Function.comp_def] using ht
  · exact (map_ne_zero_iff euclideanBlocks euclideanBlocks.injective).mpr
      (blockCLM_inactive_ne_zero hJ₀)

/-- Multiplying the two genuine Euclidean operator-norm scales gives the
condition-number scale. The inverse identities are supplied separately by the
Schur factor and `inverseCLM_eq_blockEquiv_symm`. -/
theorem condition_norm_theta
    {C D : ℝ → U →L[ℝ] U} {F : ℝ → U →L[ℝ] K}
    {T : ℝ → K →L[ℝ] U} {E J : ℝ → K →L[ℝ] K} {R : ℝ → U →L[ℝ] U}
    (hC : ContinuousAt C 0) (hD : ContinuousAt D 0)
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0) (hE : ContinuousAt E 0)
    (hJ : ContinuousAt J 0) (hR : ContinuousAt R 0)
    (hC₀ : C 0 ≠ 0) (hJ₀ : J 0 ≠ 0) :
    (fun μ => ‖euclideanBlocks (newtonCLM μ (C μ) (D μ) (F μ) (T μ) (E μ))‖ *
      ‖euclideanBlocks (inverseCLM μ (F μ) (T μ) (J μ) (R μ))‖)
      =Θ[𝓝[>] (0 : ℝ)] (fun μ => (μ ^ 2)⁻¹) := by
  simpa only [← pow_two, inv_pow] using
    (newton_norm_theta hC hD hF hT hE hC₀).mul (inverse_norm_theta hF hT hJ hR hJ₀)


/-- Norm-tight encoding now supplies the premise used by `filtering_tight`,
from the norm of the actual operator rather than a separate assumed scale. -/
theorem normTight_theta_inv
    {C D : ℝ → U →L[ℝ] U} {F : ℝ → U →L[ℝ] K}
    {T : ℝ → K →L[ℝ] U} {E : ℝ → K →L[ℝ] K} {α : ℝ → ℝ}
    (hC : ContinuousAt C 0) (hD : ContinuousAt D 0)
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0) (hE : ContinuousAt E 0)
    (hC₀ : C 0 ≠ 0)
    (hα : α =Θ[𝓝[>] (0 : ℝ)]
      (fun μ => ‖euclideanBlocks (newtonCLM μ (C μ) (D μ) (F μ) (T μ) (E μ))‖)) :
    α =Θ[𝓝[>] (0 : ℝ)] (fun μ => μ⁻¹) :=
  hα.trans (newton_norm_theta hC hD hF hT hE hC₀)

/-- The condition number of the actual inverse has scale Θ(μ⁻²). Schur
invertibility is required only eventually at positive μ; continuity of the
inverse blocks is available from `continuousAt_operator_inverse`. -/
theorem newton_condition_theta
    {C D : ℝ → U →L[ℝ] U} {F : ℝ → U →L[ℝ] K} {T : ℝ → K →L[ℝ] U}
    {E : ℝ → K ≃L[ℝ] K} {S : ℝ → U ≃L[ℝ] U}
    (hC : ContinuousAt C 0) (hD : ContinuousAt D 0)
    (hF : ContinuousAt F 0) (hT : ContinuousAt T 0)
    (hE : ContinuousAt (fun μ => (E μ).toContinuousLinearMap) 0)
    (hJ : ContinuousAt (fun μ => (E μ).symm.toContinuousLinearMap) 0)
    (hR : ContinuousAt (fun μ => (S μ).symm.toContinuousLinearMap) 0)
    (hC₀ : C 0 ≠ 0) (hJ₀ : (E 0).symm.toContinuousLinearMap ≠ 0)
    (hSchur : ∀ᶠ μ in 𝓝[>] (0 : ℝ), HasSchurFactor μ (C μ).toLinearMap
      (D μ).toLinearMap (F μ).toLinearMap (T μ).toLinearMap
      (E μ).toLinearEquiv (S μ).toLinearEquiv) :
    (fun μ => ‖euclideanBlocks
        (newtonCLM μ (C μ) (D μ) (F μ) (T μ) (E μ).toContinuousLinearMap)‖ *
      ‖euclideanBlocks (Ring.inverse
        (newtonCLM μ (C μ) (D μ) (F μ) (T μ) (E μ).toContinuousLinearMap))‖)
      =Θ[𝓝[>] (0 : ℝ)] (fun μ => (μ ^ 2)⁻¹) := by
  apply IsTheta.symm
  apply (condition_norm_theta hC hD hF hT hE hJ hR hC₀ hJ₀).symm.trans_eventuallyEq
  filter_upwards [hSchur, self_mem_nhdsWithin] with μ hS hμ
  rw [ringInverse_newtonCLM μ (ne_of_gt hμ) _ _ _ _ _ _ hS]

end
end QipmFormal.Coupling
