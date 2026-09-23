import QipmFormal.QCPM.Potential
import QipmFormal.QCPM.Schedule
import QipmFormal.QCPM.NormBounds
import QipmFormal.QCPM.Clock

/-!
# QCPM manuscript correspondence

The envelope below is the supremum of the actual finite-dimensional squared-residual
potential. The schedule theorem uses the actual normalized exponential bump integral.
Both the pulled-back integral and the literal clock-time spatial supremum are defined.
Their equality uses the canonical inverse clock and positive scaling of the spatial supremum.
-/

noncomputable section
namespace QipmFormal.QCPM
open Set MeasureTheory

/-- The spatial supremum on a fixed domain. -/
def spatialEnvelope {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    (Ω : Set (Point d)) (μ : ℝ) : ℝ := sSup (potential M q μ '' Ω)

/-- The corrected norm expressed in the original time variable. -/
def paperNorm {d : ℕ} (a eta : ℝ) (M : Fin d → Fin d → ℝ) (q : Point d)
    (Ω : Set (Point d)) (mu : ℝ → ℝ) : ℝ :=
  normIntegral a eta (fun t => spatialEnvelope M q Ω (mu t)) mu

theorem spatialEnvelope_initial_lower {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} (h : Initialized M q) {Ω : Set (Point d)}
    (he : initial d ∈ Ω) (hΩ : IsCompact Ω) (μ : ℝ) :
    (d : ℝ) / 2 * (1 - μ) ^ 2 ≤ spatialEnvelope M q Ω μ :=
  initial_value_le_sup_of_compact h μ he hΩ

theorem spatialEnvelope_nonneg {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} {Ω : Set (Point d)} (hne : Ω.Nonempty) (hΩ : IsCompact Ω) (μ : ℝ) :
    0 ≤ spatialEnvelope M q Ω μ := by
  obtain ⟨z, hz⟩ := hne
  exact (potential_nonneg M q μ z).trans
    (le_csSup (hΩ.bddAbove_image (continuous_potential M q μ).continuousOn)
      (Set.mem_image_of_mem _ hz))

/-- Compactness of the spatial domain and a positive continuous schedule discharge
all integrability assumptions in the scalar norm bounds. -/
theorem envelope_quotient_intervalIntegrable {d : ℕ} (M : Fin d → Fin d → ℝ)
    (q : Point d) {Ω : Set (Point d)} (hΩ : IsCompact Ω) {mu : ℝ → ℝ}
    (hc : ContinuousOn mu (Icc (0 : ℝ) 1))
    (hp : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t) :
    IntervalIntegrable (fun t => spatialEnvelope M q Ω (mu t) / mu t ^ 3) volume 0 1 := by
  have hen : ContinuousOn (fun t => spatialEnvelope M q Ω (mu t)) (Icc (0 : ℝ) 1) :=
    (continuous_potential_sup M q hΩ).comp_continuousOn hc
  have hquot := hen.div (hc.pow 3) (fun t ht => pow_ne_zero 3 (ne_of_gt (hp t ht)))
  apply ContinuousOn.intervalIntegrable
  rw [uIcc_of_le (show (0 : ℝ) ≤ 1 by norm_num)]
  exact hquot

/-- The manuscript's factor-128 lower bound for the actual potential and Algorithm 1 schedule.
The smallness conditions are explicit and jointly possible since `normalizer > 0`. -/
theorem paperNorm_schedule_lower {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) {Ω : Set (Point d)} (he : initial d ∈ Ω) (hΩ : IsCompact Ω)
    {a eta ε : ℝ} (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε)
    (hε4 : ε ≤ 1 / 4) (hc : ε ≤ normalizer) :
    (d : ℝ) / (128 * a * eta * ε ^ 3 * Real.log (1 / ε)) ≤
      paperNorm a eta M q Ω (schedule ε) := by
  have hε1 : ε ≤ 1 := by linarith
  have hp : ∀ t ∈ Icc (0 : ℝ) 1, 0 < schedule ε t :=
    fun t ht => hε.trans_le (schedule_mem hε1 ht).1
  apply normIntegral_log_window_lower ha heta (Nat.cast_nonneg d) hε
    (endpoint_log_ge_one_quarter hε hε4)
    (envelope_quotient_intervalIntegrable M q hΩ (schedule_continuous ε).continuousOn hp)
    (fun t _ => spatialEnvelope_nonneg ⟨initial d, he⟩ hΩ (schedule ε t)) hp
  intro t ht
  have hterminal := schedule_terminal_le_quarter hε hε4 hc ht
  refine ⟨hterminal, ?_⟩
  have hhalf : schedule ε t ≤ 1 / 2 := by linarith
  have hi := initial_value_ge_dim_div_eight h hhalf
  have hs := spatialEnvelope_initial_lower h he hΩ (schedule ε t)
  rw [← potential_at_initial h (schedule ε t)] at hs
  exact hi.trans hs

/-- The norm--speed lower bound applies directly to the actual spatial envelope.
A Lipschitz speed contract supplies continuity, so no integrability assumption remains. -/
theorem paperNorm_speed_lower {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) {Ω : Set (Point d)} (he : initial d ∈ Ω) (hΩ : IsCompact Ω)
    {a eta ε L : ℝ} (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε)
    (hε4 : ε ≤ 1 / 4) (hL : 0 < L) {mu : ℝ → ℝ}
    (hstart : mu 0 = 1) (hend : mu 1 = ε)
    (hspeed : ∀ s ∈ Icc (0 : ℝ) 1, ∀ t ∈ Icc (0 : ℝ) 1,
      |mu s - mu t| ≤ L * |s - t|)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t) :
    (d : ℝ) / (64 * a * eta * L * ε ^ 2) ≤ paperNorm a eta M q Ω mu := by
  have hlip : LipschitzOnWith (⟨L, hL.le⟩ : NNReal) mu (Icc (0 : ℝ) 1) := by
    apply lipschitzOnWith_iff_dist_le_mul.mpr
    intro s hs t ht
    change |mu s - mu t| ≤ L * |s - t|
    exact hspeed s hs t ht
  exact normIntegral_speed_lower ha heta (Nat.cast_nonneg d) hε hε4 hL hstart hend hspeed
    (envelope_quotient_intervalIntegrable M q hΩ hlip.continuousOn hmu) hmu
    (fun t _ => spatialEnvelope_initial_lower h he hΩ (mu t))

/-- The explicit fixed-box upper certificate for any continuous schedule in `[ε,1]`. -/
theorem paperNorm_box_upper {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    {Ω : Set (Point d)} (hne : Ω.Nonempty) (hΩ : IsCompact Ω)
    {a eta ε D : ℝ} (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε) (hD : 0 ≤ D)
    (hbox : ∀ z ∈ Ω, ∀ i, 0 ≤ z i ∧ z i ≤ D) {mu : ℝ → ℝ}
    (hc : ContinuousOn mu (Icc (0 : ℝ) 1))
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, mu t ∈ Icc ε 1) :
    paperNorm a eta M q Ω mu ≤ boxCertificate M q D / (a * eta * ε ^ 3) := by
  have hp : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t := fun t ht => hε.trans_le (hmu t ht).1
  apply normIntegral_upper ha heta hε (by unfold boxCertificate; positivity)
    (envelope_quotient_intervalIntegrable M q hΩ hc hp)
    (fun t ht => (hmu t ht).1)
  intro t ht
  exact potential_sup_le_boxCertificate M q hD hne hbox (hp t ht).le (hmu t ht).2

/-- In particular, Algorithm 1 has the fixed-box upper bound claimed in the correction. -/
theorem paperNorm_schedule_box_upper {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    {Ω : Set (Point d)} (hne : Ω.Nonempty) (hΩ : IsCompact Ω)
    {a eta ε D : ℝ} (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε) (hε1 : ε ≤ 1)
    (hD : 0 ≤ D) (hbox : ∀ z ∈ Ω, ∀ i, 0 ≤ z i ∧ z i ≤ D) :
    paperNorm a eta M q Ω (schedule ε) ≤ boxCertificate M q D / (a * eta * ε ^ 3) :=
  paperNorm_box_upper M q hne hΩ ha heta hε hD hbox
    (schedule_continuous ε).continuousOn (fun _ ht => schedule_mem hε1 ht)

/-- Positive scalar rescaling commutes with the spatial supremum of this nonnegative potential. -/
theorem spatialEnvelope_div {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    {Ω : Set (Point d)} (hne : Ω.Nonempty) (hΩ : IsCompact Ω) (μ : ℝ)
    {c : ℝ} (hc : 0 < c) :
    sSup ((fun z => |potential M q μ z / c|) '' Ω) = spatialEnvelope M q Ω μ / c := by
  have hcont : Continuous (fun z => |potential M q μ z / c|) :=
    ((continuous_potential M q μ).div_const c).abs
  have hb := hΩ.bddAbove_image (continuous_potential M q μ).continuousOn
  apply le_antisymm
  · apply csSup_le (hne.image _)
    rintro _ ⟨z, hz, rfl⟩
    change |potential M q μ z / c| ≤ spatialEnvelope M q Ω μ / c
    rw [abs_of_nonneg (div_nonneg (potential_nonneg M q μ z) hc.le)]
    exact div_le_div_of_nonneg_right (le_csSup hb (Set.mem_image_of_mem _ hz)) hc.le
  · obtain ⟨z, hz, hmax⟩ :=
      hΩ.exists_sSup_image_eq hne (continuous_potential M q μ).continuousOn
    unfold spatialEnvelope
    rw [hmax]
    have hzbound := le_csSup (hΩ.bddAbove_image hcont.continuousOn)
      (Set.mem_image_of_mem (fun z => |potential M q μ z / c|) hz)
    rwa [abs_of_nonneg (div_nonneg (potential_nonneg M q μ z) hc.le)] at hzbound

/-- Literal time-integrated spatial supremum in the canonical corrected clock. -/
def clockNorm {d : ℕ} (a eta : ℝ) (M : Fin d → Fin d → ℝ) (q : Point d)
    (Ω : Set (Point d)) (mu : ℝ → ℝ) : ℝ :=
  ∫ tau in (0 : ℝ)..correctedClock a eta mu 1,
    sSup ((fun z => |potential M q (mu (correctedTime a eta mu tau)) z /
      (a * mu (correctedTime a eta mu tau) ^ 2) ^ 2|) '' Ω)

/-- Exact correspondence between the actual clock-time simulator norm and the pulled-back norm. -/
theorem clockNorm_eq_paperNorm {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    {Ω : Set (Point d)} (hne : Ω.Nonempty) (hΩ : IsCompact Ω)
    {a eta : ℝ} (ha : 0 < a) (heta : 0 < eta) {mu : ℝ → ℝ}
    (hmu : ContinuousOn mu (Icc (0 : ℝ) 1))
    (hpos : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t) :
    clockNorm a eta M q Ω mu = paperNorm a eta M q Ω mu := by
  have heq := correctedEnvelope_integral ha heta hmu hpos
    ((continuous_potential_sup M q hΩ).comp_continuousOn hmu)
  change _ = paperNorm a eta M q Ω mu at heq
  rw [← heq]
  apply intervalIntegral.integral_congr
  intro tau htau
  rw [uIcc_of_le (correctedClock_one_pos ha heta hmu hpos).le] at htau
  have ht := correctedTime_mapsTo ha heta hmu hpos htau
  have hp := hpos _ ht
  exact spatialEnvelope_div M q hne hΩ _ (by positivity)

/-- The factor-128 bound holds for the literal simulator norm, not only its pullback. -/
theorem clockNorm_schedule_lower {d : ℕ} {M : Fin d → Fin d → ℝ} {q : Point d}
    (h : Initialized M q) {Ω : Set (Point d)} (he : initial d ∈ Ω) (hΩ : IsCompact Ω)
    {a eta ε : ℝ} (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε)
    (hε4 : ε ≤ 1 / 4) (hc : ε ≤ normalizer) :
    (d : ℝ) / (128 * a * eta * ε ^ 3 * Real.log (1 / ε)) ≤
      clockNorm a eta M q Ω (schedule ε) := by
  rw [clockNorm_eq_paperNorm M q ⟨initial d, he⟩ hΩ ha heta
    (schedule_continuous ε).continuousOn
    (fun _ ht => hε.trans_le (schedule_mem (by linarith) ht).1)]
  exact paperNorm_schedule_lower h he hΩ ha heta hε hε4 hc

/-- The original derivative-bound formulation follows from the checked Lipschitz bridge. -/
theorem paperNorm_derivative_speed_lower {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} (h : Initialized M q) {Ω : Set (Point d)}
    (he : initial d ∈ Ω) (hΩ : IsCompact Ω) {a eta ε L : ℝ}
    (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε) (hε4 : ε ≤ 1 / 4) (hL : 0 < L)
    {mu : ℝ → ℝ} (hstart : mu 0 = 1) (hend : mu 1 = ε)
    (hdiff : ∀ t ∈ Icc (0 : ℝ) 1, DifferentiableAt ℝ mu t)
    (hderiv : ∀ t ∈ Icc (0 : ℝ) 1, |deriv mu t| ≤ L)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t) :
    (d : ℝ) / (64 * a * eta * L * ε ^ 2) ≤ paperNorm a eta M q Ω mu :=
  paperNorm_speed_lower h he hΩ ha heta hε hε4 hL hstart hend
    (speed_bound_of_derivative hdiff hderiv) hmu

/-- The derivative speed bound also holds for the literal simulator norm. -/
theorem clockNorm_derivative_speed_lower {d : ℕ} {M : Fin d → Fin d → ℝ}
    {q : Point d} (h : Initialized M q) {Ω : Set (Point d)}
    (he : initial d ∈ Ω) (hΩ : IsCompact Ω) {a eta ε L : ℝ}
    (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε) (hε4 : ε ≤ 1 / 4) (hL : 0 < L)
    {mu : ℝ → ℝ} (hstart : mu 0 = 1) (hend : mu 1 = ε)
    (hdiff : ∀ t ∈ Icc (0 : ℝ) 1, DifferentiableAt ℝ mu t)
    (hderiv : ∀ t ∈ Icc (0 : ℝ) 1, |deriv mu t| ≤ L)
    (hmu : ∀ t ∈ Icc (0 : ℝ) 1, 0 < mu t) :
    (d : ℝ) / (64 * a * eta * L * ε ^ 2) ≤ clockNorm a eta M q Ω mu := by
  rw [clockNorm_eq_paperNorm M q ⟨initial d, he⟩ hΩ ha heta
    (fun t ht => (hdiff t ht).continuousAt.continuousWithinAt) hmu]
  exact paperNorm_derivative_speed_lower h he hΩ ha heta hε hε4 hL
    hstart hend hdiff hderiv hmu

/-- The fixed-box upper certificate for Algorithm 1 bounds the literal simulator norm. -/
theorem clockNorm_schedule_box_upper {d : ℕ} (M : Fin d → Fin d → ℝ) (q : Point d)
    {Ω : Set (Point d)} (hne : Ω.Nonempty) (hΩ : IsCompact Ω)
    {a eta ε D : ℝ} (ha : 0 < a) (heta : 0 < eta) (hε : 0 < ε) (hε1 : ε ≤ 1)
    (hD : 0 ≤ D) (hbox : ∀ z ∈ Ω, ∀ i, 0 ≤ z i ∧ z i ≤ D) :
    clockNorm a eta M q Ω (schedule ε) ≤ boxCertificate M q D / (a * eta * ε ^ 3) := by
  rw [clockNorm_eq_paperNorm M q hne hΩ ha heta
    (schedule_continuous ε).continuousOn
    (fun _ ht => hε.trans_le (schedule_mem hε1 ht).1)]
  exact paperNorm_schedule_box_upper M q hne hΩ ha heta hε hε1 hD hbox

end QipmFormal.QCPM
