import Formal.MatroidSpectral.Headline
import Formal.MatroidSpectral.CriteriaSelection

namespace MatroidSpectral
open Matrix DAGSpectral DAGSpectral.NormalizationTrials
open scoped BigOperators

theorem bestBy_exists_of_nonempty {α : Type*} (better : α → α → Bool)
    (xs : List α) (hx : xs ≠ []) : ∃ x, bestBy better xs = some x := by
  cases he : bestBy better xs with
  | none => exact (hx ((bestBy_eq_none_iff better xs).mp he)).elim
  | some x => exact ⟨x,rfl⟩

section OriginalInput
variable {a m p : ℕ} (A : RationalRepresentation a m)
  (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
  (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)

theorem representedCover_list_nonempty {η : ℚ} (hη : 0 < η)
    (xs : List (Finset (Fin m)))
    (hxs : xs.toFinset = representedSpectralCover A Q0 Q hQ0 hQ η) : xs ≠ [] := by
  intro he
  have h := representedSpectralCover_nonempty A Q0 Q hQ0 hQ hη
  rw [← hxs,he] at h
  exact Finset.not_nonempty_empty h

/-- The computed D-selector returns an actual original base. The list premise
only identifies an enumeration of the computed cover; it assumes no cover or
successful-selection certificate. -/
theorem representedCover_select_D (ε : ℚ) (hε : 0 < ε) (hε1 : ε ≤ 1) (hp : 0 < p)
    (xs : List (Finset (Fin m)))
    (hxs : xs.toFinset = representedSpectralCover A Q0 Q hQ0 hQ (ε / p)) :
    ∃ B, selectDeterminant (fun S => Q0 + ∑ e ∈ S, Q e) xs = some B ∧
      IsColumnBase A B ∧ ∀ S, IsColumnBase A S →
        (1-(ε : ℝ)) * (ratMatrixReal (Q0 + ∑ e ∈ S, Q e)).det ≤
          (ratMatrixReal (Q0 + ∑ e ∈ B, Q e)).det := by
  have hmesh : 0 < ε / (p : ℚ) := by positivity
  obtain ⟨B,hB⟩ := bestBy_exists_of_nonempty
    (fun S T => determinantLE (Q0 + ∑ e ∈ S, Q e) (Q0 + ∑ e ∈ T, Q e)) xs
    (representedCover_list_nonempty A Q0 Q hQ0 hQ hmesh xs hxs)
  have hc : IsRelativeCover ((ε : ℝ) / p)
      (fun S => ratMatrixReal (information (producedData Q0 Q hQ0 hQ) S))
      (columnBases A) xs.toFinset := by
    rw [hxs]
    simpa using representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hmesh
  have hg := select_D_guarantee (producedData Q0 Q hQ0 hQ) hc hp
    (by exact_mod_cast hε.le) (by exact_mod_cast hε1) hB
  exact ⟨B,hB,(mem_columnBases A B).mp hg.1,
    fun S hS => hg.2 S ((mem_columnBases A S).mpr hS)⟩

theorem representedCover_select_E [NeZero p] (ε : ℚ) (hε : 0 < ε) (hε1 : ε ≤ 1)
    (xs : List (Finset (Fin m)))
    (hxs : xs.toFinset = representedSpectralCover A Q0 Q hQ0 hQ ε) :
    ∃ B, selectMinimumEigenvalue (fun S => Q0 + ∑ e ∈ S, Q e) xs = some B ∧
      IsColumnBase A B ∧ ∀ S, IsColumnBase A S →
        (1-(ε : ℝ)) * minimumEigenvalue (ratMatrixReal (Q0 + ∑ e ∈ S, Q e)) ≤
          minimumEigenvalue (ratMatrixReal (Q0 + ∑ e ∈ B, Q e)) := by
  obtain ⟨B,hB⟩ := bestBy_exists_of_nonempty
    (fun S T => minimumEigenvalueLE (Q0 + ∑ e ∈ S, Q e) (Q0 + ∑ e ∈ T, Q e)) xs
    (representedCover_list_nonempty A Q0 Q hQ0 hQ hε xs hxs)
  have hc : IsRelativeCover (ε : ℝ)
      (fun S => ratMatrixReal (information (producedData Q0 Q hQ0 hQ) S))
      (columnBases A) xs.toFinset := by
    rw [hxs]
    exact representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hε
  have hg := select_E_guarantee (producedData Q0 Q hQ0 hQ) hc
    (by exact_mod_cast hε1) hB
  exact ⟨B,hB,(mem_columnBases A B).mp hg.1,
    fun S hS => hg.2 S ((mem_columnBases A S).mpr hS)⟩

theorem representedCover_select_A (ε : ℚ) (hε : 0 < ε)
    (xs : List (Finset (Fin m)))
    (hxs : xs.toFinset = representedSpectralCover A Q0 Q hQ0 hQ (ε / (1 + ε))) :
    ∃ B, selectInverseTrace (fun S => Q0 + ∑ e ∈ S, Q e) xs = some B ∧
      IsColumnBase A B ∧ ∀ S, IsColumnBase A S →
        inverseTraceCost (ratMatrixReal (Q0 + ∑ e ∈ B, Q e)) ≤
          ENNReal.ofReal (1+(ε : ℝ)) *
            inverseTraceCost (ratMatrixReal (Q0 + ∑ e ∈ S, Q e)) := by
  have hmesh : 0 < ε / (1+ε) := by positivity
  obtain ⟨B,hB⟩ := bestBy_exists_of_nonempty
    (fun S T => inverseTraceCostLE (Q0 + ∑ e ∈ T, Q e) (Q0 + ∑ e ∈ S, Q e)) xs
    (representedCover_list_nonempty A Q0 Q hQ0 hQ hmesh xs hxs)
  have hc : IsRelativeCover ((ε : ℝ) / (1+ε))
      (fun S => ratMatrixReal (information (producedData Q0 Q hQ0 hQ) S))
      (columnBases A) xs.toFinset := by
    rw [hxs]
    simpa using representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hmesh
  have hg := select_A_guarantee (producedData Q0 Q hQ0 hQ) hc (by exact_mod_cast hε.le) hB
  exact ⟨B,hB,(mem_columnBases A B).mp hg.1,
    fun S hS => hg.2 S ((mem_columnBases A S).mpr hS)⟩

theorem representedCover_select_contrast {η : ℚ} (hη : 0 < η) (hη1 : η < 1)
    (c : Fin p → ℚ) (xs : List (Finset (Fin m)))
    (hxs : xs.toFinset = representedSpectralCover A Q0 Q hQ0 hQ η) :
    ∃ B, selectContrast (fun S => Q0 + ∑ e ∈ S, Q e) c xs = some B ∧
      IsColumnBase A B ∧ ∀ S, IsColumnBase A S →
        contrastCost (ratMatrixReal (Q0 + ∑ e ∈ B, Q e)) (fun i => (c i : ℝ)) ≤
          ENNReal.ofReal ((1-(η : ℝ))⁻¹) *
            contrastCost (ratMatrixReal (Q0 + ∑ e ∈ S, Q e)) (fun i => (c i : ℝ)) := by
  obtain ⟨B,hB⟩ := bestBy_exists_of_nonempty
    (fun S T => contrastCostLE (Q0 + ∑ e ∈ T, Q e) (Q0 + ∑ e ∈ S, Q e) c) xs
    (representedCover_list_nonempty A Q0 Q hQ0 hQ hη xs hxs)
  have hc : IsRelativeCover (η : ℝ)
      (fun S => ratMatrixReal (information (producedData Q0 Q hQ0 hQ) S))
      (columnBases A) xs.toFinset := by
    rw [hxs]
    exact representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hη
  have hg := select_contrast_guarantee (producedData Q0 Q hQ0 hQ) hc
    (by exact_mod_cast hη.le) (by exact_mod_cast hη1) c hB
  exact ⟨B,hB,(mem_columnBases A B).mp hg.1,
    fun S hS => hg.2 S ((mem_columnBases A S).mpr hS)⟩

theorem representedCover_select_weightedContrast {η : ℚ} (hη : 0 < η) (hη1 : η < 1)
    {k : ℕ} (cs : Fin k → Fin p → ℚ) (ws : Fin k → ℚ) (hw : ∀ i, 0 ≤ ws i)
    (xs : List (Finset (Fin m)))
    (hxs : xs.toFinset = representedSpectralCover A Q0 Q hQ0 hQ η) :
    ∃ B, selectWeightedContrast (fun S => Q0 + ∑ e ∈ S, Q e) cs ws xs = some B ∧
      IsColumnBase A B ∧ ∀ S, IsColumnBase A S →
        weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
            (ratMatrixReal (Q0 + ∑ e ∈ B, Q e)) ≤
          ENNReal.ofReal ((1-(η : ℝ))⁻¹) *
            weightedContrastCost (rationalWeights ws hw) (fun j i => (cs j i : ℝ))
              (ratMatrixReal (Q0 + ∑ e ∈ S, Q e)) := by
  obtain ⟨B,hB⟩ := bestBy_exists_of_nonempty
    (fun S T => weightedContrastCostLE (Q0 + ∑ e ∈ T, Q e) (Q0 + ∑ e ∈ S, Q e) cs ws) xs
    (representedCover_list_nonempty A Q0 Q hQ0 hQ hη xs hxs)
  have hc : IsRelativeCover (η : ℝ)
      (fun S => ratMatrixReal (information (producedData Q0 Q hQ0 hQ) S))
      (columnBases A) xs.toFinset := by
    rw [hxs]
    exact representedSpectralCover_isRelativeCover A Q0 Q hQ0 hQ hη
  have hg := select_weightedContrast_guarantee (producedData Q0 Q hQ0 hQ) hc
    (by exact_mod_cast hη.le) (by exact_mod_cast hη1) cs ws hw hB
  exact ⟨B,hB,(mem_columnBases A B).mp hg.1,
    fun S hS => hg.2 S ((mem_columnBases A S).mpr hS)⟩

end OriginalInput
end MatroidSpectral
