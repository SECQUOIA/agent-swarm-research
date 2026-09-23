import Formal.DAGSpectral.CriterionSelectEigenTrace
import Formal.DAGSpectral.CriterionSelectContrast
import Formal.DAGSpectral.CriterionSelectWeighted
import Formal.DAGSpectral.CoverWholeExecution
import Formal.DAGSpectral.Headline

namespace DAGSpectral
open Matrix NormalizationTrials
open scoped ENNReal

section Produced
variable {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
  (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
  (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
  (η : ℚ) (B : ℕ) (K F C : ℕ → ℕ)

/-- The computed candidate list, including its actual duplicate elimination.
The width budgets parameterize only the run's accounting. -/
def criterionCandidates : List (List (Fin m)) :=
  (CoverBitCost.coverBitRun G s t (producedData Q0 Q hQ0 hQ) η B K F C).1

theorem criterionCandidates_cover (hη : 0 < η) :
    IsRelativeCover (η : ℝ) (fun es => ratMatrixReal (rationalPathInformation Q0 Q es))
      (feasiblePaths G s t) (criterionCandidates G s t Q0 Q hQ0 hQ η B K F C).toFinset := by
  simpa only [criterionCandidates,CoverBitCost.coverBitRun_paths,dagSpectralCover,
    rationalPathInformation_cast] using
    dagSpectralCover_isRelativeCover G s t Q0 Q hQ0 hQ η hη

theorem criterionCandidates_length (es : List (Fin m))
    (he : es ∈ criterionCandidates G s t Q0 Q hQ0 hQ η B K F C) : es.length ≤ v-1 := by
  have hs : es ∈ spectralPathSet G s t (producedData Q0 Q hQ0 hQ) η := by
    rw [← CoverBitCost.coverBitRun_paths G s t (producedData Q0 Q hQ0 hQ) η B K F C]
    exact List.mem_toFinset.mpr he
  exact (spectralPathSet_sound G s t (producedData Q0 Q hQ0 hQ) η hs).length_le_vertices

theorem criterionCandidates_nonempty (hη : 0 < η) (hex : ∃ es, G.Path s t es) :
    criterionCandidates G s t Q0 Q hQ0 hQ η B K F C ≠ [] := by
  intro he
  obtain ⟨es,hes⟩ := hex
  obtain ⟨fs,hfs,_⟩ := (criterionCandidates_cover G s t Q0 Q hQ0 hQ η B K F C hη).2
    es ((mem_feasiblePaths G s t es).mpr hes)
  simp [he] at hfs

/-- E-selection on the list actually produced from the original graph and
matrices, with no supplied cover or supplied feasible-family enumeration. -/
theorem produced_selectEigenvalue [NeZero p] (hη : 0 < η) (hη1 : η ≤ 1)
    {b : List (Fin m)}
    (hb : selectMinimumEigenvalue (rationalPathInformation Q0 Q)
      (criterionCandidates G s t Q0 Q hQ0 hQ η B K F C) = some b) :
    G.Path s t b ∧ ∀ a, G.Path s t a →
      (1-(η : ℝ))*minimumEigenvalue (ratMatrixReal (rationalPathInformation Q0 Q a)) ≤
        minimumEigenvalue (ratMatrixReal (rationalPathInformation Q0 Q b)) := by
  have hc := criterionCandidates_cover G s t Q0 Q hQ0 hQ η B K F C hη
  have hs := hc.selectMinimumEigenvalue_guarantee
      (fun a _ => by rw [rationalPathInformation_cast]; exact pathMatrix_psd hQ0 hQ a)
      (by exact_mod_cast hη1) hb
  exact ⟨(mem_feasiblePaths G s t b).mp hs.1,
    fun a ha => hs.2 a ((mem_feasiblePaths G s t a).mpr ha)⟩

theorem produced_selectInverseTrace (hη : 0 < η) (hη1 : η < 1)
    {b : List (Fin m)}
    (hb : selectInverseTrace (rationalPathInformation Q0 Q)
      (criterionCandidates G s t Q0 Q hQ0 hQ η B K F C) = some b) :
    G.Path s t b ∧ ∀ a, G.Path s t a →
      inverseTraceCost (ratMatrixReal (rationalPathInformation Q0 Q b)) ≤
        ENNReal.ofReal ((1-(η : ℝ))⁻¹)*
          inverseTraceCost (ratMatrixReal (rationalPathInformation Q0 Q a)) := by
  have hc := criterionCandidates_cover G s t Q0 Q hQ0 hQ η B K F C hη
  have hs := hc.selectInverseTrace_guarantee
      (fun a _ => by rw [rationalPathInformation_cast]; exact pathMatrix_psd hQ0 hQ a)
      (by exact_mod_cast hη.le) (by exact_mod_cast hη1) hb
  exact ⟨(mem_feasiblePaths G s t b).mp hs.1,
    fun a ha => hs.2 a ((mem_feasiblePaths G s t a).mpr ha)⟩

theorem produced_selectContrast (hη : 0 < η) (hη1 : η < 1) (c : Fin p → ℚ)
    {b : List (Fin m)}
    (hb : selectContrast (rationalPathInformation Q0 Q) c
      (criterionCandidates G s t Q0 Q hQ0 hQ η B K F C) = some b) :
    G.Path s t b ∧ ∀ a, G.Path s t a →
      contrastCost (ratMatrixReal (rationalPathInformation Q0 Q b)) (fun i => (c i : ℝ)) ≤
        ENNReal.ofReal ((1-(η : ℝ))⁻¹)*
          contrastCost (ratMatrixReal (rationalPathInformation Q0 Q a)) (fun i => (c i : ℝ)) := by
  have hc := criterionCandidates_cover G s t Q0 Q hQ0 hQ η B K F C hη
  have hs := hc.selectContrast_guarantee
      (fun a _ => by rw [rationalPathInformation_cast]; exact pathMatrix_psd hQ0 hQ a)
      (by exact_mod_cast hη.le) (by exact_mod_cast hη1) c hb
  exact ⟨(mem_feasiblePaths G s t b).mp hs.1,
    fun a ha => hs.2 a ((mem_feasiblePaths G s t a).mpr ha)⟩

theorem produced_selectWeightedContrast {k : ℕ} (hη : 0 < η) (hη1 : η < 1)
    (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ) (hw : ∀ i, 0 ≤ ws i)
    {b : List (Fin m)}
    (hb : selectWeightedContrast (rationalPathInformation Q0 Q) cs ws
      (criterionCandidates G s t Q0 Q hQ0 hQ η B K F C) = some b) :
    G.Path s t b ∧ ∀ a, G.Path s t a →
      weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
        (ratMatrixReal (rationalPathInformation Q0 Q b)) ≤
        ENNReal.ofReal ((1-(η : ℝ))⁻¹)*
          weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
            (ratMatrixReal (rationalPathInformation Q0 Q a)) := by
  have hc := criterionCandidates_cover G s t Q0 Q hQ0 hQ η B K F C hη
  have hs := hc.selectWeightedContrast_guarantee
    (fun a _ => by rw [rationalPathInformation_cast]; exact pathMatrix_psd hQ0 hQ a)
    (by exact_mod_cast hη.le) (by exact_mod_cast hη1) cs ws hw hb
  exact ⟨(mem_feasiblePaths G s t b).mp hs.1,
    fun a ha => hs.2 a ((mem_feasiblePaths G s t a).mpr ha)⟩

end Produced

section Determinant
variable {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
  (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
  (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
  (ε : ℚ) (B : ℕ) (K F C : ℕ → ℕ)

theorem produced_selectDeterminant (hp : 0 < p) (hε : 0 < ε) (hε1 : ε ≤ 1)
    {b : List (Fin m)}
    (hb : selectDeterminant (rationalPathInformation Q0 Q)
      (criterionCandidates G s t Q0 Q hQ0 hQ (ε / p) B K F C) = some b) :
    G.Path s t b ∧ ∀ a, G.Path s t a →
      (1-(ε : ℝ))*(ratMatrixReal (rationalPathInformation Q0 Q a)).det ≤
        (ratMatrixReal (rationalPathInformation Q0 Q b)).det := by
  have hη : 0 < ε / (p : ℚ) := div_pos hε (by exact_mod_cast hp)
  have hc := criterionCandidates_cover G s t Q0 Q hQ0 hQ (ε / p) B K F C hη
  have hc' : IsRelativeCover ((ε : ℝ) / p)
      (fun es => ratMatrixReal (rationalPathInformation Q0 Q es)) (feasiblePaths G s t)
      (criterionCandidates G s t Q0 Q hQ0 hQ (ε / p) B K F C).toFinset := by
    simpa only [Rat.cast_div,Rat.cast_natCast] using hc
  have hs := hc'.selectDeterminant_guarantee
    (fun a _ => by rw [rationalPathInformation_cast]; exact pathMatrix_psd hQ0 hQ a)
    hp (by exact_mod_cast hε.le) (by exact_mod_cast hε1) hb
  exact ⟨(mem_feasiblePaths G s t b).mp hs.1,
    fun a ha => hs.2 a ((mem_feasiblePaths G s t a).mpr ha)⟩

end Determinant
end DAGSpectral
