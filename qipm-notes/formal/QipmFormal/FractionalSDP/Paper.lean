import QipmFormal.FractionalSDP.CenterOptimality
import QipmFormal.FractionalSDP.Geometry
import QipmFormal.FractionalSDP.Parameter
import QipmFormal.FractionalSDP.SpectrumBridge
import QipmFormal.FractionalSDP.LimitsEntries
import QipmFormal.FractionalSDP.SpectralCondition

/-! Manuscript statements on the whole central tail, including the metric
identification, actual spectrum, ordering, and leading constants. -/

namespace QipmFormal.FractionalSDP
noncomputable section
open Filter Set Topology

def centralPoint (m : ℝ) : Matrix (Fin 3) (Fin 3) ℝ := centerMatrix (muParameter m)
def gapCenter (y : ℝ) : Matrix (Fin 3) (Fin 3) ℝ := centerMatrix (gapParameter y)

/-- These four branches are proved to be strictly increasingly ordered near zero. -/
def eigenvalues (t : ℝ) : Fin 4 → ℝ := ![offLow t, diagLow t, offHigh t, diagHigh t]
def centralEigenvalues (m : ℝ) : Fin 4 → ℝ := eigenvalues (muParameter m)
def gapEigenvalues (y : ℝ) : Fin 4 → ℝ := eigenvalues (gapParameter y)

theorem centralPoint_feasible {m : ℝ} (hm : m ∈ Ioo (0 : ℝ) (1 / 6)) :
    (centralPoint m).PosDef ∧ (centralPoint m).trace = 1 ∧
      centralPoint m 2 2 = centralPoint m 0 1 ∧
      centralPoint m 0 2 = 0 ∧ centralPoint m 1 2 = 0 :=
  center_restricted_feasible (muParameter_spec hm.1 hm.2).1.1

theorem gapCenter_objective {y : ℝ} (hy : y ∈ Ioo (0 : ℝ) (1 / 6)) :
    gapCenter y 1 1 - optimumMatrix 1 1 = y := by
  rw [gapCenter, center_objective_gap, (gapParameter_spec hy.1 hy.2).2]

/-- The gap-indexed point is also the unique central point at its displayed positive parameter. -/
theorem gapCenter_unique_minimizer {y : ℝ} (hy : y ∈ Ioo (0 : ℝ) (1 / 6))
    {X : Matrix (Fin 3) (Fin 3) ℝ} (hX : X.PosDef)
    (htrace : X.trace = 1) (heq : X 2 2 = X 0 1) :
    (gapCenter y).PosDef ∧ 0 < mu (gapParameter y) ∧
    (-Real.log (gapCenter y).det + y / mu (gapParameter y) ≤
      -Real.log X.det + X 1 1 / mu (gapParameter y)) ∧
    (-Real.log (gapCenter y).det + y / mu (gapParameter y) =
      -Real.log X.det + X 1 1 / mu (gapParameter y) ↔ X = gapCenter y) := by
  obtain ⟨ht, he⟩ := gapParameter_spec hy.1 hy.2
  refine ⟨center_posDef ht.1, mu_pos ht.1 ht.2, ?_⟩
  simpa only [gapCenter, he] using
    center_unique_minimizer_matrix ht.1 ht.2 hX htrace heq

theorem centralPoint_unique_minimizer {m : ℝ} (hm : m ∈ Ioo (0 : ℝ) (1 / 6))
    {X : Matrix (Fin 3) (Fin 3) ℝ} (hX : X.PosDef)
    (htrace : X.trace = 1) (heq : X 2 2 = X 0 1) :
    (centralPoint m).PosDef ∧
    (-Real.log (centralPoint m).det + g (muParameter m) / m ≤
      -Real.log X.det + X 1 1 / m) ∧
    (-Real.log (centralPoint m).det + g (muParameter m) / m =
      -Real.log X.det + X 1 1 / m ↔ X = centralPoint m) := by
  obtain ⟨ht, he⟩ := muParameter_spec hm.1 hm.2
  refine ⟨center_posDef ht.1, ?_⟩
  simpa only [centralPoint, he] using
    center_unique_minimizer_matrix ht.1 ht.2 hX htrace heq

theorem centralPoint_hessian {m : ℝ} (hm : m ∈ Ioo (0 : ℝ) (1 / 6))
    (v : TangentCoords) :
    HasDerivAt
      (deriv (fun s : ℝ => -Real.log ((centralPoint m + s • coordinateTangent v).det)))
      (frobeniusPair (coordinateTangent v)
        (coordinateTangent ((reducedOperator (muParameter m)).mulVec v))) 0 := by
  have ht := (muParameter_spec hm.1 hm.2).1.1
  exact reducedOperator_second_derivative _ _ (b_pos ht).ne' (q_pos ht).ne'

theorem centralPoint_spectrum {m r : ℝ} (hm : m ∈ Ioo (0 : ℝ) (1 / 6)) :
    r ∈ spectrum ℝ (reducedOperator (muParameter m)) ↔
      r = centralEigenvalues m 0 ∨ r = centralEigenvalues m 1 ∨
      r = centralEigenvalues m 2 ∨ r = centralEigenvalues m 3 := by
  have ht := (muParameter_spec hm.1 hm.2).1.1
  have h := mem_reduced_spectrum_iff (muParameter m) r (b_pos ht) (q_pos ht)
    (add_pos (a_pos ht) (g_pos ht))
  change r ∈ spectrum ℝ (reducedOperator (muParameter m)) ↔
    r = offLow (muParameter m) ∨ r = diagLow (muParameter m) ∨
    r = offHigh (muParameter m) ∨ r = diagHigh (muParameter m)
  exact h.trans (by tauto)

theorem centralPoint_restricted_spectrum {m r : ℝ}
    (hm : m ∈ Ioo (0 : ℝ) (1 / 6)) :
    r ∈ spectrum ℝ (diagOperator (muParameter m)) ↔
      r = centralEigenvalues m 1 ∨ r = centralEigenvalues m 3 := by
  have ht := (muParameter_spec hm.1 hm.2).1.1
  exact mem_diag_spectrum_iff (muParameter m) r (q_pos ht)

theorem transfer_mu_limit {F : ℝ → ℝ → ℝ} {L : ℝ}
    (h : Tendsto (fun t => F (mu t) t) (𝓝[>] (0 : ℝ)) (𝓝 L)) :
    Tendsto (fun m => F m (muParameter m)) (𝓝[>] (0 : ℝ)) (𝓝 L) := by
  apply (h.comp muParameter_tendsto).congr'
  filter_upwards [Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1 / 6)] with m hm
  simp only [Function.comp_apply, (muParameter_spec hm.1 hm.2).2]

theorem transfer_gap_limit {F : ℝ → ℝ → ℝ} {L : ℝ}
    (h : Tendsto (fun t => F (g t) t) (𝓝[>] (0 : ℝ)) (𝓝 L)) :
    Tendsto (fun y => F y (gapParameter y)) (𝓝[>] (0 : ℝ)) (𝓝 L) := by
  apply (h.comp gapParameter_tendsto).congr'
  filter_upwards [Ioo_mem_nhdsGT (by norm_num : (0 : ℝ) < 1 / 6)] with y hy
  simp only [Function.comp_apply, (gapParameter_spec hy.1 hy.2).2]

theorem centralEigenvalues_ordered : ∀ᶠ m : ℝ in 𝓝[>] 0,
    centralEigenvalues m 0 < centralEigenvalues m 1 ∧
    centralEigenvalues m 1 < centralEigenvalues m 2 ∧
    centralEigenvalues m 2 < centralEigenvalues m 3 := by
  exact muParameter_tendsto.eventually eventually_spectrum_ordered

theorem centralEigenvalues_positive : ∀ᶠ m : ℝ in 𝓝[>] 0,
    ∀ i, 0 < centralEigenvalues m i := by
  filter_upwards [muParameter_tendsto.eventually eventually_spectrum_positive] with m hm i
  fin_cases i <;> dsimp [centralEigenvalues, eigenvalues]
  all_goals tauto

theorem paper_first_eigenvalue :
    Tendsto (fun m => Real.sqrt m * centralEigenvalues m 0)
      (𝓝[>] (0 : ℝ)) (𝓝 (Real.sqrt 2)) :=
  transfer_mu_limit (F := fun m t => Real.sqrt m * offLow t) limit_mu_offLow

theorem paper_second_eigenvalue :
    Tendsto (fun m => m * centralEigenvalues m 1)
      (𝓝[>] (0 : ℝ)) (𝓝 1) :=
  transfer_mu_limit (F := fun m t => m * diagLow t) limit_mu_diagLow

theorem paper_third_eigenvalue :
    Tendsto (fun m => m * Real.sqrt m * centralEigenvalues m 2)
      (𝓝[>] (0 : ℝ)) (𝓝 (Real.sqrt 2)) :=
  transfer_mu_limit (F := fun m t => m * Real.sqrt m * offHigh t) limit_mu_offHigh

theorem paper_fourth_eigenvalue :
    Tendsto (fun m => m ^ 2 * centralEigenvalues m 3)
      (𝓝[>] (0 : ℝ)) (𝓝 (4 / 7)) :=
  transfer_mu_limit (F := fun m t => m ^ 2 * diagHigh t) limit_mu_diagHigh

theorem paper_mu_condition :
    Tendsto (fun m => m * Real.sqrt m * (centralEigenvalues m 3 / centralEigenvalues m 0))
      (𝓝[>] (0 : ℝ)) (𝓝 (2 * Real.sqrt 2 / 7)) :=
  transfer_mu_limit (F := fun m t => m * Real.sqrt m * (diagHigh t / offLow t))
    limit_mu_condition

theorem paper_gap_condition :
    Tendsto (fun y => y * Real.sqrt y * (gapEigenvalues y 3 / gapEigenvalues y 0))
      (𝓝[>] (0 : ℝ)) (𝓝 (3 * Real.sqrt 3 / 7)) :=
  transfer_gap_limit (F := fun y t => y * Real.sqrt y * (diagHigh t / offLow t))
    limit_gap_condition

theorem paper_mu_restricted_condition :
    Tendsto (fun m => m * (centralEigenvalues m 3 / centralEigenvalues m 1))
      (𝓝[>] (0 : ℝ)) (𝓝 (4 / 7)) :=
  transfer_mu_limit (F := fun m t => m * (diagHigh t / diagLow t))
    limit_mu_restricted_condition

theorem paper_gap_restricted_condition :
    Tendsto (fun y => y * (gapEigenvalues y 3 / gapEigenvalues y 1))
      (𝓝[>] (0 : ℝ)) (𝓝 (6 / 7)) :=
  transfer_gap_limit (F := fun y t => y * (diagHigh t / diagLow t))
    limit_gap_restricted_condition

/-- The condition numbers below use the extrema of the actual operator spectrum. -/
theorem paper_mu_spectralCondition :
    Tendsto (fun m => m * Real.sqrt m * spectralCondition (muParameter m))
      (𝓝[>] (0 : ℝ)) (𝓝 (2 * Real.sqrt 2 / 7)) :=
  transfer_mu_limit (F := fun m t => m * Real.sqrt m * spectralCondition t)
    limit_mu_spectralCondition

theorem paper_gap_spectralCondition :
    Tendsto (fun y => y * Real.sqrt y * spectralCondition (gapParameter y))
      (𝓝[>] (0 : ℝ)) (𝓝 (3 * Real.sqrt 3 / 7)) :=
  transfer_gap_limit (F := fun y t => y * Real.sqrt y * spectralCondition t)
    limit_gap_spectralCondition

theorem paper_mu_restrictedSpectralCondition :
    Tendsto (fun m => m * restrictedSpectralCondition (muParameter m))
      (𝓝[>] (0 : ℝ)) (𝓝 (4 / 7)) :=
  transfer_mu_limit (F := fun m t => m * restrictedSpectralCondition t)
    limit_mu_restrictedSpectralCondition

theorem paper_gap_restrictedSpectralCondition :
    Tendsto (fun y => y * restrictedSpectralCondition (gapParameter y))
      (𝓝[>] (0 : ℝ)) (𝓝 (6 / 7)) :=
  transfer_gap_limit (F := fun y t => y * restrictedSpectralCondition t)
    limit_gap_restrictedSpectralCondition

end
end QipmFormal.FractionalSDP
