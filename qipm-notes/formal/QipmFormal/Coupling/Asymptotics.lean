import QipmFormal.Coupling.Bounds
import Mathlib.Analysis.Asymptotics.Theta

/-! # Filtering scales derived from the exact inverse vectors

The hypotheses below bound the Schur variables and the inverse inactive block.
They do not assume bounds on the inverse Newton vectors or on filtering. The
finite estimates in `Bounds` supply those conclusions, including the lower
bound that prevents cancellation in the second inverse.
-/
open Filter Asymptotics
open scoped Topology

namespace QipmFormal.Coupling

variable {U K : Type*} [NormedAddCommGroup U] [NormedSpace ℝ U]
  [NormedAddCommGroup K] [NormedSpace ℝ K]

/-- Local data supplied by continuity of the Schur variables and invertibility
of their limiting blocks. `h = E⁻¹ g` and `r = E⁻¹ F q` in the block model. -/
structure UniformBounds (l : Filter ℝ) (p q : ℝ → U) (g h r : ℝ → K) where
  pLower : ℝ
  pUpper : ℝ
  gUpper : ℝ
  qLower : ℝ
  qUpper : ℝ
  eUpper : ℝ
  eInvUpper : ℝ
  rUpper : ℝ
  pLower_pos : 0 < pLower
  qLower_pos : 0 < qLower
  eUpper_nonneg : 0 ≤ eUpper
  eInvUpper_nonneg : 0 ≤ eInvUpper
  rUpper_nonneg : 0 ≤ rUpper
  bounds : ∀ᶠ μ in l, pLower ≤ ‖p μ‖ ∧ ‖p μ‖ ≤ pUpper ∧ ‖g μ‖ ≤ gUpper ∧
    qLower ≤ ‖q μ‖ ∧ ‖q μ‖ ≤ qUpper ∧ ‖g μ‖ ≤ eUpper * ‖h μ‖ ∧
    ‖h μ‖ ≤ eInvUpper * ‖g μ‖ ∧ ‖r μ‖ ≤ rUpper

noncomputable def firstNorm (p : ℝ → U) (g : ℝ → K) (μ : ℝ) : ℝ :=
  blockNorm (μ • p μ) (μ • -g μ)

noncomputable def secondNorm (q : ℝ → U) (h r : ℝ → K) (μ : ℝ) : ℝ :=
  blockNorm (μ ^ 2 • q μ) (-h μ - μ ^ 2 • r μ)

noncomputable def filtering (α : ℝ → ℝ) (p q : ℝ → U) (g h r : ℝ → K)
    (μ : ℝ) : ℝ := α μ * secondNorm q h r μ / firstNorm p g μ

variable {l : Filter ℝ} {p q : ℝ → U} {g h r : ℝ → K}

lemma firstNorm_theta (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) : firstNorm p g =Θ[l] (fun μ ↦ μ) := by
  constructor
  · apply isBigO_iff.2 ⟨d.pUpper + d.gUpper, ?_⟩
    filter_upwards [d.bounds, hμ] with μ hd hμ
    simpa [firstNorm, Real.norm_eq_abs, abs_of_nonneg (blockNorm_nonneg _ _),
      abs_of_pos hμ, mul_comm] using
      (firstInverse_bounds μ d.pLower d.pUpper d.gUpper (p μ) (g μ) hμ.le
        hd.1 hd.2.1 hd.2.2.1).2
  · apply isBigO_iff.2 ⟨d.pLower⁻¹, ?_⟩
    filter_upwards [d.bounds, hμ] with μ hd hμ
    have hb := (firstInverse_bounds μ d.pLower d.pUpper d.gUpper (p μ) (g μ) hμ.le
      hd.1 hd.2.1 hd.2.2.1).1
    simp only [Real.norm_eq_abs, abs_of_pos hμ,
      abs_of_nonneg (show 0 ≤ firstNorm p g μ from blockNorm_nonneg _ _)]
    exact (le_inv_mul_iff₀ d.pLower_pos).2 (by simpa [firstNorm, mul_comm] using hb)

lemma secondNorm_theta (d : UniformBounds l p q g h r) :
    secondNorm q h r =Θ[l] (fun μ ↦ ‖g μ‖ + μ ^ 2) := by
  constructor
  · apply isBigO_iff.2 ⟨d.qUpper + d.rUpper + d.eInvUpper, ?_⟩
    filter_upwards [d.bounds] with μ hd
    simpa [secondNorm, Real.norm_eq_abs, abs_of_nonneg (blockNorm_nonneg _ _),
      abs_of_nonneg (show 0 ≤ ‖g μ‖ + μ ^ 2 by positivity)] using
      (secondInverse_bounds μ d.qLower d.qUpper d.eUpper d.eInvUpper d.rUpper
        (q μ) (g μ) (h μ) (r μ) d.qLower_pos d.eUpper_nonneg d.eInvUpper_nonneg
        d.rUpper_nonneg hd.2.2.2.1 hd.2.2.2.2.1 hd.2.2.2.2.2.1
        hd.2.2.2.2.2.2.1 hd.2.2.2.2.2.2.2).2
  · apply isBigO_iff.2 ⟨d.eUpper + (d.eUpper * d.rUpper + 1) / d.qLower, ?_⟩
    filter_upwards [d.bounds] with μ hd
    simpa [secondNorm, Real.norm_eq_abs, abs_of_nonneg (blockNorm_nonneg _ _),
      abs_of_nonneg (show 0 ≤ ‖g μ‖ + μ ^ 2 by positivity)] using
      (secondInverse_bounds μ d.qLower d.qUpper d.eUpper d.eInvUpper d.rUpper
        (q μ) (g μ) (h μ) (r μ) d.qLower_pos d.eUpper_nonneg d.eInvUpper_nonneg
        d.rUpper_nonneg hd.2.2.2.1 hd.2.2.2.2.1 hd.2.2.2.2.2.1
        hd.2.2.2.2.2.2.1 hd.2.2.2.2.2.2.2).1

/-- The encoding factor is retained exactly: no norm-tightness is assumed. -/
lemma filtering_nontight (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) (α : ℝ → ℝ) :
    filtering α p q g h r =Θ[l] (fun μ ↦ α μ * (μ + ‖g μ‖ / μ)) := by
  have ht := ((isTheta_refl α l).mul (secondNorm_theta d)).div (firstNorm_theta d hμ)
  apply ht.trans_eventuallyEq
  filter_upwards [hμ] with μ hμ
  field_simp
  ring

lemma filtering_tight (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) :
    filtering α p q g h r =Θ[l] (fun μ ↦ 1 + ‖g μ‖ / μ ^ 2) := by
  have ht := (hα.mul (secondNorm_theta d)).div (firstNorm_theta d hμ)
  apply ht.trans_eventuallyEq
  filter_upwards [hμ] with μ hμ
  field_simp
  ring

lemma firstAmplification_tight (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) (bNorm : ℝ) (hb : bNorm ≠ 0) :
    (fun μ ↦ α μ * firstNorm p g μ / bNorm) =Θ[l] (fun _ ↦ (1 : ℝ)) := by
  have ht := (hα.mul (firstNorm_theta d hμ)).div (isTheta_refl (fun _ : ℝ ↦ bNorm) l)
  have hconst : (fun μ ↦ μ⁻¹ * μ / bNorm) =Θ[l] (fun _ ↦ (1 : ℝ)) := by
    have he : (fun μ : ℝ ↦ μ⁻¹ * μ / bNorm) =ᶠ[l] (fun _ ↦ bNorm⁻¹) := by
      filter_upwards [hμ] with μ hμ
      simp [ne_of_gt hμ]
    exact he.isTheta.trans (isTheta_const_const (inv_ne_zero hb) one_ne_zero)
  exact ht.trans hconst

omit [NormedSpace ℝ K] in
/-- The bounded-cost criterion holds without analyticity. -/
lemma profile_bounded_iff (hμ : ∀ᶠ μ in l, 0 < μ) :
    (fun μ ↦ 1 + ‖g μ‖ / μ ^ 2) =O[l] (fun _ ↦ (1 : ℝ)) ↔
      g =O[l] (fun μ ↦ μ ^ 2) := by
  constructor
  · intro hb
    obtain ⟨C, hC⟩ := isBigO_iff.1 hb
    apply isBigO_iff.2 ⟨C, ?_⟩
    filter_upwards [hC, hμ] with μ hC hμ
    have hsq : 0 < μ ^ 2 := sq_pos_of_pos hμ
    have hn : 0 ≤ ‖g μ‖ / μ ^ 2 := div_nonneg (norm_nonneg _) hsq.le
    simp only [Real.norm_eq_abs, abs_of_nonneg (by positivity : 0 ≤ 1 + ‖g μ‖ / μ ^ 2),
      norm_one, mul_one] at hC
    simp only [Real.norm_eq_abs, abs_of_nonneg hsq.le]
    exact (div_le_iff₀ hsq).1 (by linarith)
  · intro hg
    obtain ⟨C, hC⟩ := isBigO_iff.1 hg
    apply isBigO_iff.2 ⟨1 + C, ?_⟩
    filter_upwards [hC, hμ] with μ hC hμ
    have hsq : 0 < μ ^ 2 := sq_pos_of_pos hμ
    simp only [Real.norm_eq_abs, abs_of_nonneg hsq.le] at hC
    have hc := (div_le_iff₀ hsq).2 hC
    simp only [Real.norm_eq_abs, abs_of_nonneg (by positivity : 0 ≤ 1 + ‖g μ‖ / μ ^ 2),
      norm_one, mul_one]
    linarith

lemma filtering_bounded_iff (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) {α : ℝ → ℝ}
    (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) :
    filtering α p q g h r =O[l] (fun _ ↦ (1 : ℝ)) ↔
      g =O[l] (fun μ ↦ μ ^ 2) :=
  (filtering_tight d hμ hα).isBigO_congr_left.trans (profile_bounded_iff hμ)

omit [NormedSpace ℝ K] in
lemma profile_scaled_limit (hμ : ∀ᶠ μ in l, 0 < μ)
    (hzero : Tendsto (fun μ : ℝ ↦ μ) l (𝓝 0)) {g₀ : K}
    (hg : Tendsto g l (𝓝 g₀)) :
    Tendsto (fun μ ↦ (1 + ‖g μ‖ / μ ^ 2) / (μ ^ 2)⁻¹) l (𝓝 ‖g₀‖) := by
  have ht : Tendsto (fun μ ↦ μ ^ 2 + ‖g μ‖) l (𝓝 ‖g₀‖) := by
    simpa using (hzero.pow 2).add hg.norm
  apply ht.congr'
  filter_upwards [hμ] with μ hμ
  field_simp

lemma filtering_full_scale (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) (hzero : Tendsto (fun μ : ℝ ↦ μ) l (𝓝 0))
    {g₀ : K} (hg : Tendsto g l (𝓝 g₀)) (hg₀ : g₀ ≠ 0)
    {α : ℝ → ℝ} (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) :
    filtering α p q g h r =Θ[l] (fun μ ↦ (μ ^ 2)⁻¹) :=
  (filtering_tight d hμ hα).trans
    (isTheta_of_div_tendsto_nhds_ne_zero (profile_scaled_limit hμ hzero hg)
      (norm_ne_zero_iff.2 hg₀)).symm

/-- With continuous coupling, strict improvement means little-o of μ⁻² and
is equivalent to zero limiting coupling. An O(μ⁻¹) rate needs regularity. -/
lemma filtering_improves_iff [NeBot l] (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) (hzero : Tendsto (fun μ : ℝ ↦ μ) l (𝓝 0))
    {g₀ : K} (hg : Tendsto g l (𝓝 g₀))
    {α : ℝ → ℝ} (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) :
    filtering α p q g h r =o[l] (fun μ ↦ (μ ^ 2)⁻¹) ↔ g₀ = 0 := by
  rw [(filtering_tight d hμ hα).isLittleO_congr_left]
  rw [isLittleO_iff_tendsto' (hμ.mono (fun μ hμ he ↦ by
    exact False.elim ((inv_ne_zero (pow_ne_zero 2 (ne_of_gt hμ))) he)))]
  constructor
  · intro ht
    exact norm_eq_zero.1 (tendsto_nhds_unique (profile_scaled_limit hμ hzero hg) ht)
  · intro he
    simpa [he] using profile_scaled_limit hμ hzero hg

lemma square_littleO_parameter (hμ : ∀ᶠ μ in l, 0 < μ)
    (hzero : Tendsto (fun μ : ℝ ↦ μ) l (𝓝 0)) :
    (fun μ : ℝ ↦ μ ^ 2) =o[l] (fun μ ↦ μ) := by
  apply isLittleO_of_tendsto' (hμ.mono (fun μ hμ he ↦ False.elim (ne_of_gt hμ he)))
  apply hzero.congr'
  filter_upwards [hμ] with μ hμ
  field_simp

lemma filtering_firstOrder_bigO (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) (hzero : Tendsto (fun μ : ℝ ↦ μ) l (𝓝 0))
    (hg : g =O[l] (fun μ ↦ μ))
    {α : ℝ → ℝ} (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) :
    filtering α p q g h r =O[l] (fun μ ↦ μ⁻¹) := by
  have hs : secondNorm q h r =O[l] (fun μ ↦ μ) :=
    (secondNorm_theta d).1.trans
      (hg.norm_left.add (square_littleO_parameter hμ hzero).isBigO)
  have ht := (hα.1.mul hs).mul (firstNorm_theta d hμ).inv.1
  have he : (fun μ : ℝ ↦ μ⁻¹ * μ * μ⁻¹) =ᶠ[l] (fun μ ↦ μ⁻¹) := by
    filter_upwards [hμ] with μ hμ
    simp [ne_of_gt hμ]
  change (fun μ ↦ α μ * secondNorm q h r μ / firstNorm p g μ) =O[l] (fun μ ↦ μ⁻¹)
  simpa only [div_eq_mul_inv] using ht.trans_eventuallyEq he

lemma filtering_firstOrder_theta (d : UniformBounds l p q g h r)
    (hμ : ∀ᶠ μ in l, 0 < μ) (hzero : Tendsto (fun μ : ℝ ↦ μ) l (𝓝 0))
    (hg : g =Θ[l] (fun μ ↦ μ))
    {α : ℝ → ℝ} (hα : α =Θ[l] (fun μ ↦ μ⁻¹)) :
    filtering α p q g h r =Θ[l] (fun μ ↦ μ⁻¹) := by
  have hs : secondNorm q h r =Θ[l] (fun μ ↦ μ) :=
    (secondNorm_theta d).trans
      (hg.norm_left.add_isLittleO (square_littleO_parameter hμ hzero))
  have ht := (hα.mul hs).div (firstNorm_theta d hμ)
  apply ht.trans_eventuallyEq
  filter_upwards [hμ] with μ hμ
  simp [ne_of_gt hμ]

end QipmFormal.Coupling
