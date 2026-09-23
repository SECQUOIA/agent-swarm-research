import QipmFormal.FractionalSDP.SpectrumBridge
import QipmFormal.FractionalSDP.LimitsTransfer
import QipmFormal.FractionalSDP.Center

/-! Spectral condition numbers of the actual Frobenius Hessian operators.
The extrema are taken over the operator spectrum, rather than defined as
ratios of the separately computed eigenvalue branches. -/
namespace QipmFormal.FractionalSDP
noncomputable section
open Filter Set
open scoped Topology

def spectralCondition (t : ℝ) : ℝ :=
  sSup (spectrum ℝ (reducedOperator t)) / sInf (spectrum ℝ (reducedOperator t))

def restrictedSpectralCondition (t : ℝ) : ℝ :=
  sSup (spectrum ℝ (diagOperator t)) / sInf (spectrum ℝ (diagOperator t))

theorem reduced_spectrum_extrema {t : ℝ} (ht : 0 < t)
    (hord : offLow t < diagLow t ∧ diagLow t < offHigh t ∧ offHigh t < diagHigh t) :
    IsLeast (spectrum ℝ (reducedOperator t)) (offLow t) ∧
      IsGreatest (spectrum ℝ (reducedOperator t)) (diagHigh t) := by
  have hs := mem_reduced_spectrum_iff t
  have hspec (r : ℝ) := hs r (b_pos ht) (q_pos ht) (add_pos (a_pos ht) (g_pos ht))
  constructor
  · refine ⟨(hspec _).mpr (Or.inr (Or.inr (Or.inl rfl))), ?_⟩
    intro r hr
    rcases (hspec r).mp hr with rfl | rfl | rfl | rfl
    · exact hord.1.le
    · exact (hord.1.trans (hord.2.1.trans hord.2.2)).le
    · exact le_rfl
    · exact (hord.1.trans hord.2.1).le
  · refine ⟨(hspec _).mpr (Or.inr (Or.inl rfl)), ?_⟩
    intro r hr
    rcases (hspec r).mp hr with rfl | rfl | rfl | rfl
    · exact (hord.2.1.trans hord.2.2).le
    · exact le_rfl
    · exact (hord.1.trans (hord.2.1.trans hord.2.2)).le
    · exact hord.2.2.le

theorem restricted_spectrum_extrema {t : ℝ} (ht : 0 < t)
    (hord : diagLow t ≤ diagHigh t) :
    IsLeast (spectrum ℝ (diagOperator t)) (diagLow t) ∧
      IsGreatest (spectrum ℝ (diagOperator t)) (diagHigh t) := by
  have hspec (r : ℝ) := mem_diag_spectrum_iff t r (q_pos ht)
  constructor
  · refine ⟨(hspec _).mpr (Or.inl rfl), ?_⟩
    intro r hr
    rcases (hspec r).mp hr with rfl | rfl
    · exact le_rfl
    · exact hord
  · refine ⟨(hspec _).mpr (Or.inr rfl), ?_⟩
    intro r hr
    rcases (hspec r).mp hr with rfl | rfl
    · exact hord
    · exact le_rfl

theorem eventually_spectralCondition_eq :
    ∀ᶠ t : ℝ in 𝓝[>] 0, spectralCondition t = diagHigh t / offLow t := by
  filter_upwards [self_mem_nhdsWithin, eventually_spectrum_ordered] with t ht hord
  obtain ⟨hmin,hmax⟩ := reduced_spectrum_extrema ht hord
  exact congrArg₂ (fun x y : ℝ => x/y) hmax.csSup_eq hmin.csInf_eq

theorem eventually_restrictedSpectralCondition_eq :
    ∀ᶠ t : ℝ in 𝓝[>] 0, restrictedSpectralCondition t = diagHigh t / diagLow t := by
  filter_upwards [self_mem_nhdsWithin, eventually_spectrum_ordered] with t ht hord
  obtain ⟨hmin,hmax⟩ := restricted_spectrum_extrema ht (hord.2.1.trans hord.2.2).le
  exact congrArg₂ (fun x y : ℝ => x/y) hmax.csSup_eq hmin.csInf_eq

/-- Positivity is a property of every actual operator eigenvalue on the tail. -/
theorem eventually_actual_spectrum_positive :
    ∀ᶠ t : ℝ in 𝓝[>] 0, ∀ r ∈ spectrum ℝ (reducedOperator t), 0 < r := by
  filter_upwards [self_mem_nhdsWithin, eventually_spectrum_ordered,
    eventually_spectrum_positive] with t ht hord hp r hr
  exact lt_of_lt_of_le hp.2.2.2.1 ((reduced_spectrum_extrema ht hord).1.2 hr)

theorem limit_mu_spectralCondition :
    Tendsto (fun t => mu t * Real.sqrt (mu t) * spectralCondition t)
      (𝓝[>] 0) (𝓝 (2 * Real.sqrt 2 / 7)) := by
  apply limit_mu_condition.congr'
  filter_upwards [eventually_spectralCondition_eq] with t ht
  rw [ht]

theorem limit_gap_spectralCondition :
    Tendsto (fun t => g t * Real.sqrt (g t) * spectralCondition t)
      (𝓝[>] 0) (𝓝 (3 * Real.sqrt 3 / 7)) := by
  apply limit_gap_condition.congr'
  filter_upwards [eventually_spectralCondition_eq] with t ht
  rw [ht]

theorem limit_mu_restrictedSpectralCondition :
    Tendsto (fun t => mu t * restrictedSpectralCondition t)
      (𝓝[>] 0) (𝓝 (4 / 7 : ℝ)) := by
  apply limit_mu_restricted_condition.congr'
  filter_upwards [eventually_restrictedSpectralCondition_eq] with t ht
  rw [ht]

theorem limit_gap_restrictedSpectralCondition :
    Tendsto (fun t => g t * restrictedSpectralCondition t)
      (𝓝[>] 0) (𝓝 (6 / 7 : ℝ)) := by
  apply limit_gap_restricted_condition.congr'
  filter_upwards [eventually_restrictedSpectralCondition_eq] with t ht
  rw [ht]

end
end QipmFormal.FractionalSDP
