import Formal.ReciprocalAnchor.ManyProbability
import Formal.ReciprocalAnchor.ManyQuantile

/-! Fractional threshold-atom selection for arbitrary compactly supported probability laws. -/
namespace ReciprocalAnchor.ManyLeaf
open MeasureTheory Set

/-- Explicit upper-tail selection, including a fraction of any threshold atom. -/
theorem probability_threshold_selection (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q s : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hlo : μ.real (Ioi s) ≤ q) (hhi : q ≤ μ.real (Ici s)) :
    ∃ θ : ℝ → ℝ, Measurable θ ∧ (∀ x, θ x ∈ Icc (0 : ℝ) 1) ∧
      (∫ x, θ x ∂μ) = q ∧ (∫ x, x * θ x ∂μ) = q * s + probabilityCall μ s := by
  classical
  let A := μ.real (Ioi s)
  let B := μ.real {s}
  have hB : 0 ≤ B := measureReal_nonneg
  have hAB : μ.real (Ici s) = A + B := by
    have he : Ici s = Ioi s ∪ {s} := by
      ext x
      simp only [mem_Ici, mem_union, mem_Ioi, mem_singleton_iff]
      constructor <;> intro hx <;> grind
    rw [he, measureReal_union (by
      apply disjoint_left.mpr
      intro x hx hy
      have heq : x = s := hy
      have hlt : s < x := hx
      linarith) (measurableSet_singleton s)]
  have hd0 : 0 ≤ q - A := sub_nonneg.mpr hlo
  have hdB : q - A ≤ B := by rw [hAB] at hhi; linarith
  let r := (q - A) / B
  have hr0 : 0 ≤ r := div_nonneg hd0 hB
  have hr1 : r ≤ 1 := by
    by_cases hB0 : B = 0
    · simp [r, hB0]
    · exact (div_le_one (lt_of_le_of_ne hB (Ne.symm hB0))).mpr hdB
  have hrB : r * B = q - A := by
    by_cases hB0 : B = 0
    · have hd : q - A = 0 := by linarith
      simp [hB0, hd]
    · exact div_mul_cancel₀ _ hB0
  let θ : ℝ → ℝ := fun x => (Ioi s).indicator (fun _ => (1 : ℝ)) x +
    r * ({s} : Set ℝ).indicator (fun _ => (1 : ℝ)) x
  have hm : Measurable θ := by
    exact (measurable_const.indicator measurableSet_Ioi).add
      (measurable_const.mul (measurable_const.indicator (measurableSet_singleton s)))
  have he : ∀ x, θ x = if s < x then 1 else if x = s then r else 0 := by
    intro x
    simp only [θ, indicator_apply, mem_Ioi, mem_singleton_iff]
    split_ifs <;> simp_all
  have hb : ∀ x, θ x ∈ Icc (0 : ℝ) 1 := by
    intro x
    rw [he]
    split_ifs <;> exact ⟨by positivity, by first | exact hr1 | norm_num⟩
  have hmass : (∫ x, θ x ∂μ) = q := by
    have hi1 := (integrable_const (1 : ℝ)).indicator (μ := μ) (s := Ioi s) measurableSet_Ioi
    have hi2 := (integrable_const (1 : ℝ)).indicator (μ := μ) (measurableSet_singleton s)
    change (∫ x, (Ioi s).indicator (fun _ => (1 : ℝ)) x +
      r * ({s} : Set ℝ).indicator (fun _ => (1 : ℝ)) x ∂μ) = q
    rw [integral_add hi1 (hi2.const_mul r), integral_const_mul]
    simp only [integral_indicator measurableSet_Ioi, integral_indicator (measurableSet_singleton s),
      setIntegral_const, smul_eq_mul, mul_one]
    change A + r * B = q
    linarith
  refine ⟨θ, hm, hb, hmass, ?_⟩
  have hp : ∀ x, x * θ x = θ x * s + max (x - s) 0 := by
    intro x
    rw [he]
    split_ifs with hlt heq
    · rw [max_eq_left (by linarith)]
      ring
    · subst x
      simp [mul_comm]
    · rw [max_eq_right (by linarith)]
      simp [mul_comm]
  simp_rw [hp]
  rw [integral_add ((probability_selection_integrable μ θ hm.aestronglyMeasurable
    (Filter.Eventually.of_forall hb)).mul_const s) (probabilityCall_integrable μ h s),
    integral_mul_const, hmass]
  rfl

/-- The threshold and the attaining selector are constructed, not assumed. -/
theorem probability_upper_selection (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    ∃ s ∈ Icc a b, ∃ θ : ℝ → ℝ, Measurable θ ∧
      (∀ x, θ x ∈ Icc (0 : ℝ) 1) ∧ (∫ x, θ x ∂μ) = q ∧
      (∫ x, x * θ x ∂μ) = q * s + probabilityCall μ s := by
  obtain ⟨s, hs, hle, hge⟩ := probability_upper_tail_threshold μ hab h hq
  exact ⟨s, hs, probability_threshold_selection μ h hle hge⟩

/-- The constructed selector attains the infimum over all real thresholds. -/
theorem probability_upper_selection_isLeast (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    ∃ θ : ℝ → ℝ, Measurable θ ∧ (∀ x, θ x ∈ Icc (0 : ℝ) 1) ∧
      (∫ x, θ x ∂μ) = q ∧ IsLeast (range (fun s => q * s + probabilityCall μ s))
        (∫ x, x * θ x ∂μ) := by
  obtain ⟨s, _, θ, hm, hb, hmass, hmoment⟩ := probability_upper_selection μ hab h hq
  refine ⟨θ, hm, hb, hmass, ⟨⟨s, hmoment.symm⟩, ?_⟩⟩
  rintro _ ⟨t, rfl⟩
  simpa [hmass] using probability_selection_bound μ h θ hm.aestronglyMeasurable
    (Filter.Eventually.of_forall hb) t

/-- Realizable first moments at fixed selected mass. -/
def ProbabilitySelectable (μ : Measure ℝ) (q w : ℝ) : Prop :=
  ∃ θ : ℝ → ℝ, Measurable θ ∧ (∀ x, θ x ∈ Icc (0 : ℝ) 1) ∧
    (∫ x, θ x ∂μ) = q ∧ (∫ x, x * θ x ∂μ) = w

/-- Complementing a selector gives the complementary mass and first moment. -/
theorem ProbabilitySelectable.complement {μ : Measure ℝ} [IsProbabilityMeasure μ]
    {a b q w : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b) (hw : ProbabilitySelectable μ q w) :
    ProbabilitySelectable μ (1 - q) ((∫ x, x ∂μ) - w) := by
  obtain ⟨θ, hm, hb, hmass, hmoment⟩ := hw
  have hiθ := probability_selection_integrable μ θ hm.aestronglyMeasurable
    (Filter.Eventually.of_forall hb)
  have hiw := probability_selection_moment_integrable μ h θ hm.aestronglyMeasurable
    (Filter.Eventually.of_forall hb)
  refine ⟨fun x => 1 - θ x, measurable_const.sub hm, ?_, ?_, ?_⟩
  · intro x
    have hx := hb x
    constructor <;> linarith [hx.1, hx.2]
  · rw [integral_sub (integrable_const _) hiθ, hmass]
    simp
  · simp_rw [mul_sub, mul_one]
    rw [integral_sub (supported_integrable_id μ h) hiw, hmoment]

/-- Convex interpolation fills the entire interval, including coincident extremes. -/
theorem ProbabilitySelectable.interpolate {μ : Measure ℝ} [IsProbabilityMeasure μ]
    {a b q w₀ w₁ w : ℝ} (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (h₀ : ProbabilitySelectable μ q w₀) (h₁ : ProbabilitySelectable μ q w₁)
    (hw : w ∈ Icc w₀ w₁) : ProbabilitySelectable μ q w := by
  obtain ⟨u, v, hu, hv, huv, he⟩ := Icc_subset_segment hw
  simp only [smul_eq_mul] at he
  obtain ⟨θ₀, hm₀, hb₀, hmass₀, hmoment₀⟩ := h₀
  obtain ⟨θ₁, hm₁, hb₁, hmass₁, hmoment₁⟩ := h₁
  have hi₀ := probability_selection_integrable μ θ₀ hm₀.aestronglyMeasurable
    (Filter.Eventually.of_forall hb₀)
  have hi₁ := probability_selection_integrable μ θ₁ hm₁.aestronglyMeasurable
    (Filter.Eventually.of_forall hb₁)
  have hw₀ := probability_selection_moment_integrable μ h θ₀ hm₀.aestronglyMeasurable
    (Filter.Eventually.of_forall hb₀)
  have hw₁ := probability_selection_moment_integrable μ h θ₁ hm₁.aestronglyMeasurable
    (Filter.Eventually.of_forall hb₁)
  refine ⟨fun x => u * θ₀ x + v * θ₁ x,
    (measurable_const.mul hm₀).add (measurable_const.mul hm₁), ?_, ?_, ?_⟩
  · intro x
    have h₀ := hb₀ x
    have h₁ := hb₁ x
    constructor
    · exact add_nonneg (mul_nonneg hu h₀.1) (mul_nonneg hv h₁.1)
    · nlinarith [mul_nonneg hu (sub_nonneg.mpr h₀.2),
        mul_nonneg hv (sub_nonneg.mpr h₁.2)]
  · rw [integral_add (hi₀.const_mul u) (hi₁.const_mul v)]
    simp only [integral_const_mul, hmass₀, hmass₁]
    nlinarith [congrArg (fun z : ℝ => z * q) huv]
  · have hp : ∀ x, x * (u * θ₀ x + v * θ₁ x) =
        u * (x * θ₀ x) + v * (x * θ₁ x) := by intro x; ring
    simp_rw [hp]
    rw [integral_add (hw₀.const_mul u) (hw₁.const_mul v)]
    simpa only [integral_const_mul, hmoment₀, hmoment₁] using he

/-- Both threshold families characterize realizability on every supported law. -/
theorem probability_selection_iff (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q w : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    ProbabilitySelectable μ q w ↔ ∀ s : ℝ,
      w ≤ q * s + probabilityCall μ s ∧
      (∫ x, x ∂μ) - w ≤ (1 - q) * s + probabilityCall μ s := by
  constructor
  · intro hw s
    obtain ⟨θ, hm, hb, hmass, hmoment⟩ := hw
    have hu := probability_selection_bound μ h θ hm.aestronglyMeasurable
      (Filter.Eventually.of_forall hb) s
    have hwc : ProbabilitySelectable μ q w := ⟨θ, hm, hb, hmass, hmoment⟩
    obtain ⟨φ, hφm, hφb, hφmass, hφmoment⟩ := hwc.complement h
    have hl := probability_selection_bound μ h φ hφm.aestronglyMeasurable
      (Filter.Eventually.of_forall hφb) s
    exact ⟨by simpa [hmass, hmoment] using hu, by simpa [hφmass, hφmoment] using hl⟩
  · intro hs
    obtain ⟨s, _, θ, hm, hb, hmass, hmoment⟩ := probability_upper_selection μ hab h hq
    have hq' : 1 - q ∈ Icc (0 : ℝ) 1 := by constructor <;> linarith [hq.1, hq.2]
    obtain ⟨t, _, φ, hφm, hφb, hφmass, hφmoment⟩ := probability_upper_selection μ hab h hq'
    have hhi : ProbabilitySelectable μ q (q * s + probabilityCall μ s) :=
      ⟨θ, hm, hb, hmass, hmoment⟩
    have hcomp : ProbabilitySelectable μ (1 - q) ((1 - q) * t + probabilityCall μ t) :=
      ⟨φ, hφm, hφb, hφmass, hφmoment⟩
    have hlo : ProbabilitySelectable μ q
        ((∫ x, x ∂μ) - ((1 - q) * t + probabilityCall μ t)) := by
      simpa only [sub_sub_cancel] using hcomp.complement h
    exact hlo.interpolate h hhi ⟨by linarith [(hs t).2], (hs s).1⟩

/-- Individually admissible leaves coexist on the same law without independence. -/
theorem probability_simultaneous_selection {ι : Type*} (μ : Measure ℝ) (q w : ι → ℝ)
    (h : ∀ j, ProbabilitySelectable μ (q j) (w j)) :
    ∃ θ : ι → ℝ → ℝ, ∀ j, Measurable (θ j) ∧
      (∀ x, θ j x ∈ Icc (0 : ℝ) 1) ∧
      (∫ x, θ j x ∂μ) = q j ∧ (∫ x, x * θ j x ∂μ) = w j := by
  classical
  choose θ hθ using h
  exact ⟨θ, hθ⟩

/-- The upper selectable moment is the threshold infimum in formula (4). -/
noncomputable def probabilityUpper (μ : Measure ℝ) (q : ℝ) : ℝ :=
  sInf (range (fun s => q * s + probabilityCall μ s))

theorem probabilityUpper_isGreatest (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    IsGreatest {w | ProbabilitySelectable μ q w} (probabilityUpper μ q) := by
  obtain ⟨θ, hm, hb, hmass, hleast⟩ := probability_upper_selection_isLeast μ hab h hq
  have he : probabilityUpper μ q = ∫ x, x * θ x ∂μ := hleast.csInf_eq
  rw [he]
  refine ⟨⟨θ, hm, hb, hmass, rfl⟩, ?_⟩
  intro w hw
  obtain ⟨s, hs⟩ := hleast.1
  rw [← hs]
  exact ((probability_selection_iff μ hab h hq).mp hw s).1

/-- The lower selectable moment is the mean minus the complementary upper moment. -/
theorem probabilityLower_isLeast (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    IsLeast {w | ProbabilitySelectable μ q w}
      ((∫ x, x ∂μ) - probabilityUpper μ (1 - q)) := by
  have hq' : 1 - q ∈ Icc (0 : ℝ) 1 := by constructor <;> linarith [hq.1, hq.2]
  have hu := probabilityUpper_isGreatest μ hab h hq'
  refine ⟨?_, ?_⟩
  · change ProbabilitySelectable μ q _
    simpa only [sub_sub_cancel] using hu.1.complement h
  · intro w hw
    have hle := hu.2 (hw.complement h)
    linarith

/-- The selectable moments are exactly the full closed interval of the two extrema. -/
theorem probability_selectable_interval (μ : Measure ℝ) [IsProbabilityMeasure μ]
    {a b q w : ℝ} (hab : a ≤ b) (h : ∀ᵐ x ∂μ, x ∈ Icc a b)
    (hq : q ∈ Icc (0 : ℝ) 1) :
    ProbabilitySelectable μ q w ↔
      w ∈ Icc ((∫ x, x ∂μ) - probabilityUpper μ (1 - q)) (probabilityUpper μ q) := by
  have hlo := probabilityLower_isLeast μ hab h hq
  have hhi := probabilityUpper_isGreatest μ hab h hq
  exact ⟨fun hw => ⟨hlo.2 hw, hhi.2 hw⟩, fun hw => hlo.1.interpolate h hhi.1 hw⟩

end ReciprocalAnchor.ManyLeaf
