import QipmFormal.Coupling.Asymptotics
import QipmFormal.Coupling.Paper
import Mathlib.Analysis.Calculus.FDeriv.Analytic
import Mathlib.Analysis.Normed.Ring.Units
import Mathlib.Topology.Instances.Matrix
import Mathlib.Tactic

/-! # Regularity needed by the exact-center coupling law

These lemmas derive the rate alternatives from differentiability or analyticity.
They do not assert the external theorem that a strictly complementary LP has an
analytic central path. Continuity also supplies the uniform norm bounds used in
the block estimates; invertibility supplies continuity of the inverse itself.
-/

open Filter Asymptotics Topology

namespace QipmFormal.Coupling

variable {V : Type*} [NormedAddCommGroup V] [NormedSpace ℝ V]

/-- A differentiable coupling that vanishes at the endpoint is at most linear. -/
theorem coupling_isBigO_of_differentiable {g : ℝ → V}
    (hg : DifferentiableAt ℝ g 0) (hzero : g 0 = 0) :
    g =O[𝓝 (0 : ℝ)] (fun μ : ℝ => μ) := by
  simpa [hzero] using hg.isBigO_sub

/-- A nonzero first derivative gives exactly linear coupling. -/
theorem coupling_isTheta_of_hasDerivAt {g : ℝ → V} {d : V}
    (hg : HasDerivAt g d 0) (hzero : g 0 = 0) (hd : d ≠ 0) :
    g =Θ[𝓝 (0 : ℝ)] (fun μ : ℝ => μ) := by
  have ht := (show Tendsto (fun μ : ℝ => (μ, (0 : ℝ))) (𝓝 0)
      (𝓝 0 ×ˢ pure 0) from tendsto_id.prodMk tendsto_const_pure)
  exact ⟨by simpa [hzero, Function.comp_def] using (hg.isTheta_sub hd).1.comp_tendsto ht,
    by simpa [hzero, Function.comp_def] using (hg.isTheta_sub hd).2.comp_tendsto ht⟩

/-- Analyticity and zero constant and linear coefficients give quadratic decay.
This avoids any assumption about a first nonzero Taylor coefficient existing. -/
theorem coupling_isBigO_sq_of_analytic {g : ℝ → V}
    (hg : AnalyticAt ℝ g 0) (hzero : g 0 = 0) (hderiv : deriv g 0 = 0) :
    g =O[𝓝 (0 : ℝ)] (fun μ : ℝ => μ ^ 2) := by
  obtain ⟨p, hp⟩ := hg
  have hp1 : p 1 (fun _ => (1 : ℝ)) = 0 := by rw [← hp.deriv, hderiv]
  have hp1' (μ : ℝ) : p 1 (fun _ => μ) = 0 := by
    have h := (p 1).map_smul_univ (fun _ => μ) (fun _ => (1 : ℝ))
    simpa [hp1] using h
  have hpartial (μ : ℝ) : p.partialSum 2 μ = 0 := by
    simp only [FormalMultilinearSeries.partialSum, Finset.sum_range_succ,
      Finset.sum_range_zero, zero_add, hp.coeff_zero, hzero, hp1']
  simpa [hpartial, Real.norm_eq_abs, sq_abs] using hp.isBigO_sub_partialSum_pow 2

/-- The two endpoint-vanishing analytic alternatives used by the paper. -/
theorem analytic_coupling_rate_cases {g : ℝ → V}
    (hg : AnalyticAt ℝ g 0) (hzero : g 0 = 0) :
    (g =Θ[𝓝 (0 : ℝ)] (fun μ : ℝ => μ)) ∨
      (g =O[𝓝 (0 : ℝ)] (fun μ : ℝ => μ ^ 2)) := by
  by_cases hd : deriv g 0 = 0
  · exact Or.inr (coupling_isBigO_sq_of_analytic hg hzero hd)
  · exact Or.inl (coupling_isTheta_of_hasDerivAt hg.differentiableAt.hasDerivAt hzero hd)

omit [NormedSpace ℝ V] in
/-- Convergence gives an explicit positive eventual upper bound. -/
theorem eventually_norm_upper {ι : Type*} {l : Filter ι} {f : ι → V} {v : V}
    (hf : Tendsto f l (𝓝 v)) :
    ∃ B > 0, ∀ᶠ i in l, ‖f i‖ ≤ B := by
  refine ⟨‖v‖ + 1, by positivity, ?_⟩
  exact (hf.norm.eventually (gt_mem_nhds (by linarith : ‖v‖ < ‖v‖ + 1))).mono
    fun _ h => h.le

omit [NormedSpace ℝ V] in
/-- A nonzero limit supplies the lower bound needed to prevent cancellation. -/
theorem eventually_norm_lower {ι : Type*} {l : Filter ι} {f : ι → V} {v : V}
    (hf : Tendsto f l (𝓝 v)) (hv : v ≠ 0) :
    ∃ b > 0, ∀ᶠ i in l, b ≤ ‖f i‖ := by
  have hv' : 0 < ‖v‖ := norm_pos_iff.mpr hv
  refine ⟨‖v‖ / 2, by positivity, ?_⟩
  exact (hf.norm.eventually (lt_mem_nhds (by linarith : ‖v‖ / 2 < ‖v‖))).mono
    fun _ h => h.le

/-- Inversion is continuous at an invertible operator, rather than being a
separate regularity assumption. -/
theorem continuousAt_operator_inverse [CompleteSpace V]
    {S : ℝ → V →L[ℝ] V} (hS : ContinuousAt S 0) (hunit : IsUnit (S 0)) :
    ContinuousAt (fun μ => Ring.inverse (S μ)) 0 := by
  obtain ⟨u, hu⟩ := hunit
  have h := NormedRing.inverse_continuousAt u
  rw [hu] at h
  exact h.comp hS

/-- The same invertibility hypothesis gives analytic inversion. -/
theorem analyticAt_operator_inverse [CompleteSpace V]
    {S : ℝ → V →L[ℝ] V} (hS : AnalyticAt ℝ S 0) (hunit : IsUnit (S 0)) :
    AnalyticAt ℝ (fun μ => Ring.inverse (S μ)) 0 := by
  obtain ⟨u, hu⟩ := hunit
  have h := analyticAt_inverse (𝕜 := ℝ) u
  rw [hu] at h
  exact h.comp hS

/-- Analytic dependence is preserved when applying an operator to a vector. -/
theorem analyticAt_operator_apply
    {W : Type*} [NormedAddCommGroup W] [NormedSpace ℝ W]
    {A : ℝ → V →L[ℝ] W} {v : ℝ → V}
    (hA : AnalyticAt ℝ A 0) (hv : AnalyticAt ℝ v 0) :
    AnalyticAt ℝ (fun μ => A μ (v μ)) 0 :=
  ((ContinuousLinearMap.id ℝ (V →L[ℝ] W)).analyticAt_bilinear _).comp₂ hA hv

section Uniform

variable {U K : Type*} [NormedAddCommGroup U] [NormedSpace ℝ U]
  [NormedAddCommGroup K] [NormedSpace ℝ K] [CompleteSpace K]

omit [NormedSpace ℝ U] in
/-- All uniform estimates in the filtering theorem follow from continuity,
nonzero limiting p and q, and invertibility of the limiting inactive block. -/
theorem uniformBounds_of_continuous
    {p q : ℝ → U} {g r : ℝ → K} {E : ℝ → K →L[ℝ] K}
    (hp : ContinuousAt p 0) (hq : ContinuousAt q 0)
    (hg : ContinuousAt g 0) (hr : ContinuousAt r 0)
    (hE : ContinuousAt E 0) (hunit : IsUnit (E 0))
    (hp0 : p 0 ≠ 0) (hq0 : q 0 ≠ 0) :
    Nonempty (UniformBounds (𝓝 (0 : ℝ)) p q g
      (fun μ => Ring.inverse (E μ) (g μ)) r) := by
  obtain ⟨pL, hpL, hplo⟩ := eventually_norm_lower hp hp0
  obtain ⟨pU, _, hphi⟩ := eventually_norm_upper hp
  obtain ⟨gU, _, hghi⟩ := eventually_norm_upper hg
  obtain ⟨qL, hqL, hqlo⟩ := eventually_norm_lower hq hq0
  obtain ⟨qU, _, hqhi⟩ := eventually_norm_upper hq
  obtain ⟨A, hA, hAhi⟩ := eventually_norm_upper hE
  obtain ⟨B, hB, hBhi⟩ := eventually_norm_upper
    (continuousAt_operator_inverse hE hunit)
  obtain ⟨T, hT, hThi⟩ := eventually_norm_upper hr
  have hu : ∀ᶠ μ in 𝓝 (0 : ℝ), IsUnit (E μ) :=
    hE.eventually (Units.isOpen.mem_nhds hunit)
  refine ⟨⟨pL, pU, gU, qL, qU, A, B, T, hpL, hqL,
    hA.le, hB.le, hT.le, ?_⟩⟩
  filter_upwards [hplo, hphi, hghi, hqlo, hqhi, hAhi, hBhi, hThi, hu]
    with μ hpL hpU hgU hqL hqU hA hB hT hu
  refine ⟨hpL, hpU, hgU, hqL, hqU, ?_, ?_, hT⟩
  · have hinv : E μ (Ring.inverse (E μ) (g μ)) = g μ := by
      have hh := congrArg (fun L : K →L[ℝ] K => L (g μ))
        (Ring.mul_inverse_cancel (E μ) hu)
      exact hh
    calc
      ‖g μ‖ = ‖E μ (Ring.inverse (E μ) (g μ))‖ := congrArg norm hinv.symm
      _ ≤ ‖E μ‖ * ‖Ring.inverse (E μ) (g μ)‖ := (E μ).le_opNorm _
      _ ≤ A * ‖Ring.inverse (E μ) (g μ)‖ :=
        mul_le_mul_of_nonneg_right hA (norm_nonneg _)
  · exact ((Ring.inverse (E μ)).le_opNorm _).trans
      (mul_le_mul_of_nonneg_right hB (norm_nonneg _))

/-- Uniform bounds remain valid on a finer filter, including approach from
positive central parameters. -/
def UniformBounds.mono {l l' : Filter ℝ} {p q : ℝ → U} {g h r : ℝ → K}
    (bounds : UniformBounds l p q g h r) (hl : l' ≤ l) :
    UniformBounds l' p q g h r :=
  { bounds with bounds := bounds.bounds.filter_mono hl }

end Uniform

section FiniteBlocks

variable {U K : Type*} [NormedAddCommGroup U] [InnerProductSpace ℝ U]
  [NormedAddCommGroup K] [InnerProductSpace ℝ K]
  [FiniteDimensional ℝ U] [FiniteDimensional ℝ K]

/-- The continuous-operator representation of a finite-dimensional equivalence. -/
noncomputable def equivalenceOperator {W : Type*} [NormedAddCommGroup W]
    [NormedSpace ℝ W] [FiniteDimensional ℝ W] (e : W ≃ₗ[ℝ] W) : W →L[ℝ] W :=
  e.toContinuousLinearEquiv.toContinuousLinearMap

lemma equivalenceOperator_isUnit {W : Type*} [NormedAddCommGroup W]
    [NormedSpace ℝ W] [FiniteDimensional ℝ W] (e : W ≃ₗ[ℝ] W) :
    IsUnit (equivalenceOperator e) := e.toContinuousLinearEquiv.toUnit.isUnit

@[simp] lemma equivalenceOperator_inverse_apply {W : Type*} [NormedAddCommGroup W]
    [NormedSpace ℝ W] [FiniteDimensional ℝ W] (e : W ≃ₗ[ℝ] W) (v : W) :
    Ring.inverse (equivalenceOperator e) v = e.symm v := by
  change Ring.inverse (↑e.toContinuousLinearEquiv.toUnit : W →L[ℝ] W) v = _
  rw [Ring.inverse_unit]
  rfl

omit [FiniteDimensional ℝ U] [FiniteDimensional ℝ K] in
/-- Composition of analytic operator families is analytic. -/
theorem analyticAt_operator_comp
    {A : ℝ → K →L[ℝ] U} {B : ℝ → U →L[ℝ] K}
    (hA : AnalyticAt ℝ A 0) (hB : AnalyticAt ℝ B 0) :
    AnalyticAt ℝ (fun μ => (A μ).comp (B μ)) 0 :=
  ((ContinuousLinearMap.compL ℝ U K U).analyticAt_bilinear _).comp₂ hA hB

namespace BlockFamily

variable (d : BlockFamily U K)

omit [FiniteDimensional ℝ K] in
/-- At the endpoint the quadratic Schur correction vanishes, so S₀=C₀. -/
theorem endpoint_schurOperator
    (hSchur : ∀ᶠ μ in 𝓝 (0 : ℝ),
      HasSchurFactor μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) (d.S μ)) :
    equivalenceOperator (d.S 0) = (d.C 0).toContinuousLinearMap := by
  have hs := hSchur.self_of_nhds
  ext u
  simpa [equivalenceOperator] using hs u

/-- The endpoint coupling is exactly E₀⁻¹F₀C₀⁻¹b, expressed through the
primitive active block C₀ rather than an independently chosen Schur factor. -/
theorem endpoint_coupling_formula
    (hSchur : ∀ᶠ μ in 𝓝 (0 : ℝ),
      HasSchurFactor μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) (d.S μ))
    (b : U) :
    d.g b 0 = Ring.inverse (equivalenceOperator (d.E 0))
      ((d.F 0).toContinuousLinearMap (Ring.inverse (d.C 0).toContinuousLinearMap b)) := by
  rw [← d.endpoint_schurOperator hSchur]
  simp only [equivalenceOperator_inverse_apply]
  rfl

/-- Continuity of the Schur factor follows from that of the primitive blocks.
The Schur identity is required only near the endpoint. -/
theorem continuous_schurFactor
    (hC : ContinuousAt (fun μ => (d.C μ).toContinuousLinearMap) 0)
    (hD : ContinuousAt (fun μ => (d.D μ).toContinuousLinearMap) 0)
    (hE : ContinuousAt (fun μ => equivalenceOperator (d.E μ)) 0)
    (hF : ContinuousAt (fun μ => (d.F μ).toContinuousLinearMap) 0)
    (hT : ContinuousAt (fun μ => (d.T μ).toContinuousLinearMap) 0)
    (hSchur : ∀ᶠ μ in 𝓝 (0 : ℝ),
      HasSchurFactor μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) (d.S μ)) :
    ContinuousAt (fun μ => equivalenceOperator (d.S μ)) 0 := by
  have hEi := continuousAt_operator_inverse hE (equivalenceOperator_isUnit (d.E 0))
  have hc := hC.add ((continuousAt_id.pow 2).smul
    (hD.sub (hT.clm_comp (hEi.clm_comp hF))))
  apply hc.congr_of_eventuallyEq
  filter_upwards [hSchur] with μ hμ
  ext u
  simpa [equivalenceOperator] using hμ u

/-- Analyticity of the Schur factor also follows from the primitive blocks. -/
theorem analytic_schurFactor
    (hC : AnalyticAt ℝ (fun μ => (d.C μ).toContinuousLinearMap) 0)
    (hD : AnalyticAt ℝ (fun μ => (d.D μ).toContinuousLinearMap) 0)
    (hE : AnalyticAt ℝ (fun μ => equivalenceOperator (d.E μ)) 0)
    (hF : AnalyticAt ℝ (fun μ => (d.F μ).toContinuousLinearMap) 0)
    (hT : AnalyticAt ℝ (fun μ => (d.T μ).toContinuousLinearMap) 0)
    (hSchur : ∀ᶠ μ in 𝓝 (0 : ℝ),
      HasSchurFactor μ (d.C μ) (d.D μ) (d.F μ) (d.T μ) (d.E μ) (d.S μ)) :
    AnalyticAt ℝ (fun μ => equivalenceOperator (d.S μ)) 0 := by
  have hEi := analyticAt_operator_inverse hE (equivalenceOperator_isUnit (d.E 0))
  have hEF : AnalyticAt ℝ
      (fun μ => (Ring.inverse (equivalenceOperator (d.E μ))).comp
        (d.F μ).toContinuousLinearMap) 0 :=
    ((ContinuousLinearMap.compL ℝ U K K).analyticAt_bilinear _).comp₂ hEi hF
  have hTF := analyticAt_operator_comp hT hEF
  have hc := hC.add ((analyticAt_id.pow 2).smul (hD.sub hTF))
  apply hc.congr
  filter_upwards [hSchur] with μ hμ
  ext u
  simpa [equivalenceOperator] using (hμ u).symm

/-- Continuity of the actual Schur variables, derived by continuous inversion
and composition from the block data. -/
theorem continuous_coupling_variables
    (hS : ContinuousAt (fun μ => equivalenceOperator (d.S μ)) 0)
    (hE : ContinuousAt (fun μ => equivalenceOperator (d.E μ)) 0)
    (hF : ContinuousAt (fun μ => (d.F μ).toContinuousLinearMap) 0)
    (hT : ContinuousAt (fun μ => (d.T μ).toContinuousLinearMap) 0) (b : U) :
    ContinuousAt (d.p b) 0 ∧ ContinuousAt (d.g b) 0 ∧
      ContinuousAt (d.q b) 0 ∧ ContinuousAt (d.r b) 0 := by
  have hSi := continuousAt_operator_inverse hS (equivalenceOperator_isUnit (d.S 0))
  have hEi := continuousAt_operator_inverse hE (equivalenceOperator_isUnit (d.E 0))
  have hp : ContinuousAt (d.p b) 0 := by
    unfold BlockFamily.p couplingP
    simpa using hSi.clm_apply (continuousAt_const (y := b))
  have hg : ContinuousAt (d.g b) 0 := by
    unfold BlockFamily.g couplingG
    simpa [BlockFamily.p] using hEi.clm_apply (hF.clm_apply hp)
  have hq : ContinuousAt (d.q b) 0 := by
    unfold BlockFamily.q couplingQ
    simpa [BlockFamily.p, BlockFamily.g] using
      hSi.clm_apply (hp.add (hT.clm_apply (hEi.clm_apply hg)))
  have hr : ContinuousAt (d.r b) 0 := by
    unfold BlockFamily.r
    simpa using hEi.clm_apply (hF.clm_apply hq)
  exact ⟨hp, hg, hq, hr⟩

/-- Nonzero endpoint p and q follow from the adjoint and self-adjoint block
relations. Their limiting lower bounds are not independent assumptions. -/
theorem uniformBounds_of_block_continuity
    (hS : ContinuousAt (fun μ => equivalenceOperator (d.S μ)) 0)
    (hE : ContinuousAt (fun μ => equivalenceOperator (d.E μ)) 0)
    (hF : ContinuousAt (fun μ => (d.F μ).toContinuousLinearMap) 0)
    (hT : ContinuousAt (fun μ => (d.T μ).toContinuousLinearMap) 0)
    (hAdj : ∀ u v, inner ℝ u (d.T 0 v) = inner ℝ (d.F 0 u) v)
    (hSym : ∀ x y, inner ℝ (d.E 0 x) y = inner ℝ x (d.E 0 y))
    {b : U} (hb : b ≠ 0) :
    Nonempty (UniformBounds (𝓝 (0 : ℝ)) (d.p b) (d.q b) (d.g b) (d.h b) (d.r b)) := by
  obtain ⟨hp, hg, hq, hr⟩ := d.continuous_coupling_variables hS hE hF hT b
  have hp0 : d.p b 0 ≠ 0 := by simpa [p, couplingP] using hb
  have hq0 : d.q b 0 ≠ 0 := couplingQ_ne_zero _ _ _ _ hAdj hSym hb
  unfold BlockFamily.h
  simpa using uniformBounds_of_continuous hp hq hg hr hE
    (equivalenceOperator_isUnit (d.E 0)) hp0 hq0

/-- Analytic block data give analytic coupling. The external LP boundary
analyticity theorem is the input supplying these analytic block hypotheses. -/
theorem analytic_coupling
    (hS : AnalyticAt ℝ (fun μ => equivalenceOperator (d.S μ)) 0)
    (hE : AnalyticAt ℝ (fun μ => equivalenceOperator (d.E μ)) 0)
    (hF : AnalyticAt ℝ (fun μ => (d.F μ).toContinuousLinearMap) 0) (b : U) :
    AnalyticAt ℝ (d.g b) 0 := by
  have hSi := analyticAt_operator_inverse hS (equivalenceOperator_isUnit (d.S 0))
  have hEi := analyticAt_operator_inverse hE (equivalenceOperator_isUnit (d.E 0))
  have hp : AnalyticAt ℝ (d.p b) 0 := by
    unfold BlockFamily.p couplingP
    simpa using analyticAt_operator_apply hSi (analyticAt_const (v := b))
  unfold BlockFamily.g couplingG
  simpa [BlockFamily.p] using
    analyticAt_operator_apply hEi (analyticAt_operator_apply hF hp)

/-- The actual Newton-inverse law follows from continuous block data without
independently assuming uniform bounds on p, q, or g. -/
theorem exact_center_continuous_law
    {l : Filter ℝ} (hl : l ≤ 𝓝 (0 : ℝ))
    (hS : ContinuousAt (fun μ => equivalenceOperator (d.S μ)) 0)
    (hE : ContinuousAt (fun μ => equivalenceOperator (d.E μ)) 0)
    (hF : ContinuousAt (fun μ => (d.F μ).toContinuousLinearMap) 0)
    (hT : ContinuousAt (fun μ => (d.T μ).toContinuousLinearMap) 0)
    (hAdj : ∀ u v, inner ℝ u (d.T 0 v) = inner ℝ (d.F 0 u) v)
    (hSym : ∀ x y, inner ℝ (d.E 0 x) y = inner ℝ x (d.E 0 y))
    {b : U} (hb : b ≠ 0) (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹)) :
    (d.xi α b =Θ[l] (fun _ => (1 : ℝ))) ∧
      (d.rho α b =Θ[l] (fun μ => 1 + ‖d.g b μ‖ / μ ^ 2)) := by
  obtain ⟨bounds⟩ := d.uniformBounds_of_block_continuity hS hE hF hT hAdj hSym hb
  exact ⟨d.xi_tight hb hd (bounds.mono hl) hμ hα,
    d.rho_tight b hd (bounds.mono hl) hμ hα⟩

omit [FiniteDimensional ℝ U] [FiniteDimensional ℝ K] in
/-- A zero endpoint coupling gives the claimed square-root-scale upper bound
under differentiability alone. -/
theorem rho_firstOrder_bound
    {l : Filter ℝ} (hl : l ≤ 𝓝 (0 : ℝ)) {b : U}
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (bounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹))
    (hg : DifferentiableAt ℝ (d.g b) 0) (hzero : d.g b 0 = 0) :
    d.rho α b =O[l] (fun μ => μ⁻¹) := by
  have he : d.rho α b =ᶠ[l]
      filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) :=
    hd.mono fun _ h => d.rho_eq h α b
  exact he.trans_isBigO (filtering_firstOrder_bigO bounds hμ hl
    ((coupling_isBigO_of_differentiable hg hzero).mono hl) hα)

omit [FiniteDimensional ℝ U] [FiniteDimensional ℝ K] in
/-- For analytic endpoint-vanishing coupling, filtering is either exactly of
first-order divergent scale or bounded. The alternatives follow from the
actual first derivative and Taylor remainder, including identically zero g. -/
theorem rho_analytic_zero_cases
    {l : Filter ℝ} (hl : l ≤ 𝓝 (0 : ℝ)) {b : U}
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (bounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹))
    (hg : AnalyticAt ℝ (d.g b) 0) (hzero : d.g b 0 = 0) :
    (d.rho α b =Θ[l] (fun μ => μ⁻¹)) ∨
      (d.rho α b =O[l] (fun _ => (1 : ℝ))) := by
  have he : d.rho α b =ᶠ[l]
      filtering α (d.p b) (d.q b) (d.g b) (d.h b) (d.r b) :=
    hd.mono fun _ h => d.rho_eq h α b
  rcases analytic_coupling_rate_cases hg hzero with hlinear | hquadratic
  · exact Or.inl (he.isTheta.trans
      (filtering_firstOrder_theta bounds hμ hl (hlinear.mono hl) hα))
  · exact Or.inr ((d.rho_bounded_iff b hd bounds hμ hα).mpr (hquadratic.mono hl))

omit [FiniteDimensional ℝ U] [FiniteDimensional ℝ K] in
/-- For analytic endpoint-vanishing coupling, bounded filtering is equivalent
to a zero first derivative. This includes coupling identically zero nearby. -/
theorem rho_bounded_iff_deriv_zero
    {l : Filter ℝ} [l.NeBot] (hl : l ≤ 𝓝 (0 : ℝ)) {b : U}
    (hd : ∀ᶠ μ in l, d.ValidAt μ)
    (bounds : UniformBounds l (d.p b) (d.q b) (d.g b) (d.h b) (d.r b))
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ => μ⁻¹))
    (hg : AnalyticAt ℝ (d.g b) 0) (hzero : d.g b 0 = 0) :
    d.rho α b =O[l] (fun _ => (1 : ℝ)) ↔ deriv (d.g b) 0 = 0 := by
  rw [d.rho_bounded_iff b hd bounds hμ hα]
  constructor
  · intro hquad
    by_contra hderiv
    have hlin := (coupling_isTheta_of_hasDerivAt
      hg.differentiableAt.hasDerivAt hzero hderiv).mono hl
    have hbad := hlin.2.trans hquad
    have hfreq : ∃ᶠ μ in l, μ ^ 2 ≠ 0 :=
      (hμ.mono fun μ hμ => pow_ne_zero 2 hμ.ne').frequently
    exact (square_littleO_parameter hμ hl).not_isBigO hfreq hbad
  · intro hderiv
    exact (coupling_isBigO_sq_of_analytic hg hzero hderiv).mono hl

end BlockFamily
end FiniteBlocks

end QipmFormal.Coupling
