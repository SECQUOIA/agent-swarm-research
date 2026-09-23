import Formal.DAGSpectral.CoverCorrectness
import Formal.DAGSpectral.CoverCardinality
import Formal.DAGSpectral.NormalizationInput
import Formal.DAGSpectral.CriteriaBasic

namespace DAGSpectral
open scoped BigOperators
open Matrix NormalizationTrials

/-- A finite semantic domain for the optimization corollaries. The cover producer
does not enumerate this family. -/
def boundedEdgeLists (m : ℕ) : ℕ → Finset (List (Fin m))
  | 0 => {[]}
  | n+1 => insert [] (Finset.univ.biUnion (fun e => (boundedEdgeLists m n).image (List.cons e)))

theorem mem_boundedEdgeLists {m N : ℕ} (es : List (Fin m)) :
    es ∈ boundedEdgeLists m N ↔ es.length ≤ N := by
  induction N generalizing es with
  | zero => simp [boundedEdgeLists]
  | succ N ih =>
    cases es with
    | nil => simp [boundedEdgeLists]
    | cons e es => simp [boundedEdgeLists,ih]

noncomputable def feasiblePaths {v m : ℕ} (G : ExplicitDAG v m) (s t : Fin v) :
    Finset (List (Fin m)) := by
  classical
  exact (boundedEdgeLists m (v-1)).filter (G.Path s t)

theorem mem_feasiblePaths {v m : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (es : List (Fin m)) : es ∈ feasiblePaths G s t ↔ G.Path s t es := by
  classical
  simp only [feasiblePaths,Finset.mem_filter,mem_boundedEdgeLists]
  exact ⟨And.right,fun he => ⟨he.length_le_vertices,he⟩⟩

/-- The actual rational cover algorithm from the original prior and edge matrices.
PSD witnesses are proof-only input promises; all returned paths are computed. -/
def dagSpectralCover {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) : Finset (List (Fin m)) :=
  spectralPathSet G s t (producedData Q0 Q hQ0 hQ) η

theorem dagSpectralCover_isRelativeCover {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) :
    IsRelativeCover (η : ℝ) (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)))
      (feasiblePaths G s t) (dagSpectralCover G s t Q0 Q hQ0 hQ η) := by
  constructor
  · intro es he
    apply (mem_feasiblePaths G s t es).mpr
    exact spectralPathSet_sound G s t (producedData Q0 Q hQ0 hQ) η he
  · intro es he
    exact spectralPathSet_complete G s t (producedData Q0 Q hQ0 hQ) η hη es
      ((mem_feasiblePaths G s t es).mp he)

theorem dagSpectralCover_empty_iff {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) :
    dagSpectralCover G s t Q0 Q hQ0 hQ η = ∅ ↔ ¬ ∃ es, G.Path s t es :=
  spectralPathSet_empty_iff G s t (producedData Q0 Q hQ0 hQ) η hη

theorem dagSpectralCover_self {v m p : ℕ} (G : ExplicitDAG v m) (s : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) : dagSpectralCover G s s Q0 Q hQ0 hQ η = {[]} := by
  simp [dagSpectralCover,spectralPathSet]

theorem dagSpectralCover_kernel {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη0 : 0 < η) (hη1 : η < 1) (es : List (Fin m)) (he : G.Path s t es) :
    ∃ fs ∈ dagSpectralCover G s t Q0 Q hQ0 hQ η, G.Path s t fs ∧
      RelativeSandwich (η : ℝ)
        (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) es)
        (pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) fs) ∧
      ∀ x, pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) es *ᵥ x = 0 ↔
        pathMatrix (ratMatrixReal Q0) (fun e => ratMatrixReal (Q e)) fs *ᵥ x = 0 := by
  have hc := dagSpectralCover_isRelativeCover G s t Q0 Q hQ0 hQ η hη0
  obtain ⟨fs,hfs,hrel⟩ := hc.2 es ((mem_feasiblePaths G s t es).mpr he)
  exact ⟨fs,hfs,(mem_feasiblePaths G s t fs).mp (hc.1 hfs),hrel,
    fun x => hrel.kernel_iff (pathMatrix_psd hQ0 hQ es) (pathMatrix_psd hQ0 hQ fs)
      (by exact_mod_cast hη1) x⟩

theorem dagSpectralCover_card {v m p : ℕ} (G : ExplicitDAG v m) (s t : Fin v)
    (Q0 : Matrix (Fin p) (Fin p) ℚ) (Q : Fin m → Matrix (Fin p) (Fin p) ℚ)
    (hQ0 : (ratMatrixReal Q0).PosSemidef) (hQ : ∀ e, (ratMatrixReal (Q e)).PosSemidef)
    (η : ℚ) (hη : 0 < η) :
    (dagSpectralCover G s t Q0 Q hQ0 hQ η).card ≤
      coverCardinalityBound p (indexedFactorCount (priorAtomMatrices Q0 Q))
        (max 1 (v-1)) (η : ℝ) :=
  spectralPathSet_card G s t (producedData Q0 Q hQ0 hQ) hη

end DAGSpectral
